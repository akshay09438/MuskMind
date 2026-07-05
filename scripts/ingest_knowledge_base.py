"""
MindMusk Knowledge Base Ingestion — All 5 Layers
voyage-3-lite (1024-dim), numpy arrays + JSON metadata.
Runtime: ~30-60 min (Voyage free tier: 3 RPM, 10K TPM).
Run from project root: python scripts/ingest_knowledge_base.py
"""

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import voyageai
from dotenv import load_dotenv

load_dotenv()

VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
if not VOYAGE_API_KEY or VOYAGE_API_KEY.startswith("paste"):
    print("ERROR: Set VOYAGE_API_KEY in .env")
    sys.exit(1)

ROOT = Path(__file__).parent.parent
KB   = ROOT / "knowledge_base"
DB   = ROOT / "vector_db"
DB.mkdir(exist_ok=True)

FIRST_CHUNK_SIZE      = 2000
FIRST_CHUNK_OVERLAP   = 400
SECOND_CHUNK_SIZE     = 2400
SECOND_CHUNK_OVERLAP  = 480
THIRD_CHUNK_SIZE      = 2400
THIRD_CHUNK_OVERLAP   = 480
FOURTH_CHUNK_SIZE     = 2400
FOURTH_CHUNK_OVERLAP  = 480
FIFTH_CHUNK_SIZE      = 1600
FIFTH_CHUNK_OVERLAP   = 320

EMBED_MODEL = "voyage-3-lite"
EMBED_BATCH = 20
EMBED_SLEEP = 22

voyage = voyageai.Client(api_key=VOYAGE_API_KEY)


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    chunks, start = [], 0
    while start < len(text):
        chunk = text[start: start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = []
    total_batches = (len(texts) + EMBED_BATCH - 1) // EMBED_BATCH
    for batch_num, i in enumerate(range(0, len(texts), EMBED_BATCH)):
        batch = texts[i: i + EMBED_BATCH]
        print(f"    Batch {batch_num + 1}/{total_batches} ({len(batch)} chunks)...", end=" ", flush=True)
        for attempt in range(5):
            try:
                result = voyage.embed(batch, model=EMBED_MODEL, input_type="document")
                embeddings.extend(result.embeddings)
                print("OK", flush=True)
                break
            except Exception as e:
                if "rate" in str(e).lower() or "429" in str(e):
                    wait = EMBED_SLEEP * (attempt + 1)
                    print(f"rate limit, waiting {wait}s...", end=" ", flush=True)
                    time.sleep(wait)
                else:
                    if attempt == 4:
                        raise
                    print(f"error ({e}), retrying...", end=" ", flush=True)
                    time.sleep(5)
        if batch_num < total_batches - 1:
            time.sleep(EMBED_SLEEP)
    return embeddings


def save_layer(layer_name: str, texts: list[str], meta: list[dict]) -> None:
    if not texts:
        print(f"  No content for layer '{layer_name}', skipping.")
        return
    print(f"\n  Embedding {len(texts)} chunks for '{layer_name}'...")
    embeddings = embed_texts(texts)
    arr = np.array(embeddings, dtype=np.float32)
    np.save(DB / f"{layer_name}__embeddings.npy", arr)
    (DB / f"{layer_name}__metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  Saved: {layer_name}__embeddings.npy  shape={arr.shape}")
    print(f"  Saved: {layer_name}__metadata.json   entries={len(meta)}")


def ingest_md_dir(
    directory: Path,
    layer: str,
    chunk_size: int,
    overlap: int,
) -> tuple[list[str], list[dict]]:
    all_texts, all_meta = [], []
    files = sorted(directory.glob("*.md"))
    print(f"  Found {len(files)} .md files in {directory.name}/")
    for path in files:
        text = path.read_text(encoding="utf-8")
        chunks = chunk_text(text, chunk_size, overlap)
        size_kb = path.stat().st_size // 1024
        print(f"    {path.stem} ({size_kb} KB) -> {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            all_texts.append(chunk)
            all_meta.append({
                "id": f"{path.stem}__chunk_{i:04d}",
                "content": chunk,
                "source": path.stem,
                "layer": layer,
                "chunk_index": i,
            })
    return all_texts, all_meta


def ingest_conversation_style() -> tuple[list[str], list[dict]]:
    cs_dir = KB / "conversation_style"
    all_texts, all_meta = [], []

    qa_path = cs_dir / "elon_qa_pairs.jsonl"
    if qa_path.exists():
        pairs = []
        with open(qa_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        pairs.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        print(f"    elon_qa_pairs.jsonl -> {len(pairs)} pairs")
        for i, pair in enumerate(pairs):
            q = pair.get("instruction", "").strip()
            a = pair.get("response", "").strip()
            if q and a:
                text = f"Q: {q}\nA: {a}"
                all_texts.append(text)
                all_meta.append({
                    "id": f"qa_pair_{i:04d}",
                    "content": text,
                    "source": "elon_qa_pairs",
                    "layer": "fifth",
                    "chunk_index": i,
                })

    sp_path = cs_dir / "elon_speech_patterns.md"
    if sp_path.exists():
        text = sp_path.read_text(encoding="utf-8")
        chunks = chunk_text(text, FIFTH_CHUNK_SIZE, FIFTH_CHUNK_OVERLAP)
        size_kb = sp_path.stat().st_size // 1024
        print(f"    elon_speech_patterns.md ({size_kb} KB) -> {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            all_texts.append(chunk)
            all_meta.append({
                "id": f"speech_patterns__chunk_{i:04d}",
                "content": chunk,
                "source": "elon_speech_patterns",
                "layer": "fifth",
                "chunk_index": i,
            })

    return all_texts, all_meta


def main():
    print("\n" + "=" * 60)
    print("MindMusk Knowledge Base Ingestion — All 5 Layers")
    print("=" * 60)

    print("\n[1/5] First Order — Raw Book Content")
    t, m = ingest_md_dir(KB / "first_order", "first", FIRST_CHUNK_SIZE, FIRST_CHUNK_OVERLAP)
    save_layer("first", t, m)

    print("\n[2/5] Second Order — Elon Synthesis per Book")
    t, m = ingest_md_dir(KB / "second_order", "second", SECOND_CHUNK_SIZE, SECOND_CHUNK_OVERLAP)
    save_layer("second", t, m)

    print("\n[3/5] Third Order — Cross-Book Thematic Syntheses")
    t, m = ingest_md_dir(KB / "third_order", "third", THIRD_CHUNK_SIZE, THIRD_CHUNK_OVERLAP)
    save_layer("third", t, m)

    print("\n[4/5] Fourth Order — Master Mental Models")
    t, m = ingest_md_dir(KB / "fourth_order", "fourth", FOURTH_CHUNK_SIZE, FOURTH_CHUNK_OVERLAP)
    save_layer("fourth", t, m)

    print("\n[5/5] Fifth Layer — Conversation Style")
    t, m = ingest_conversation_style()
    save_layer("fifth", t, m)

    print("\n" + "=" * 60)
    print("Ingestion complete. Files in vector_db/:")
    for f in sorted(DB.iterdir()):
        print(f"  {f.name:50s}  {f.stat().st_size // 1024:>6} KB")
    print("=" * 60)


if __name__ == "__main__":
    main()
