"""
Ingest knowledge_base/conversation_style/chatgpt_reference_conversations.md
into vector_db's existing 'fifth' layer (append-only — does not touch
elon_qa_pairs.jsonl or elon_speech_patterns.md, and does not re-embed
the existing chunks already in fifth__embeddings.npy).
Run from project root: python -m scripts.ingest_chatgpt_reference
"""

import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import voyageai
from dotenv import load_dotenv

from scripts.reference_ingest_lib import chunk_by_paragraphs, merge_fifth_layer

load_dotenv()

VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
if not VOYAGE_API_KEY or VOYAGE_API_KEY.startswith("paste"):
    print("ERROR: Set VOYAGE_API_KEY in .env")
    sys.exit(1)

ROOT = Path(__file__).parent.parent
SOURCE_FILE = ROOT / "knowledge_base" / "conversation_style" / "chatgpt_reference_conversations.md"
DB = ROOT / "vector_db"
SOURCE_NAME = "chatgpt_reference_conversations"
EMBED_MODEL = "voyage-3-lite"
EMBED_BATCH = 20
EMBED_SLEEP = 22
MAX_CHUNK_CHARS = 1600

voyage = voyageai.Client(api_key=VOYAGE_API_KEY)


def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = []
    total_batches = (len(texts) + EMBED_BATCH - 1) // EMBED_BATCH
    for batch_num, i in enumerate(range(0, len(texts), EMBED_BATCH)):
        batch = texts[i: i + EMBED_BATCH]
        print(f"  Batch {batch_num + 1}/{total_batches} ({len(batch)} chunks)...", end=" ", flush=True)
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


def main():
    if not SOURCE_FILE.exists():
        print(f"ERROR: {SOURCE_FILE} not found. Run Task 1 first.")
        sys.exit(1)

    text = SOURCE_FILE.read_text(encoding="utf-8")
    if "---" not in text:
        print("ERROR: source file missing '---' divider between header and body.")
        sys.exit(1)
    text = text.split("---", 1)[1]

    chunks = chunk_by_paragraphs(text, max_chars=MAX_CHUNK_CHARS)
    print(f"Chunked into {len(chunks)} pieces from {SOURCE_FILE.name}")

    new_embeddings = embed_texts(chunks)

    existing_emb_path = DB / "fifth__embeddings.npy"
    existing_meta_path = DB / "fifth__metadata.json"
    existing_embeddings = np.load(existing_emb_path).astype(np.float32)
    existing_metadata = json.loads(existing_meta_path.read_text(encoding="utf-8"))
    print(f"Existing fifth layer: {existing_embeddings.shape[0]} chunks")

    merged_embeddings, merged_metadata = merge_fifth_layer(
        existing_embeddings, existing_metadata, chunks, new_embeddings, SOURCE_NAME
    )

    np.save(existing_emb_path, merged_embeddings)
    existing_meta_path.write_text(
        json.dumps(merged_metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"Merged fifth layer: {merged_embeddings.shape[0]} chunks total "
        f"({len(chunks)} new from {SOURCE_NAME})"
    )


if __name__ == "__main__":
    main()
