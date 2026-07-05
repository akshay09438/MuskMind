# MindMusk Working Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a working chat demo where a user types a message and gets a streaming Elon Musk response grounded in the 5-layer knowledge base.

**Architecture:** FastAPI backend embeds the query with Voyage AI, retrieves top-k chunks from each layer of the numpy vector store in parallel, appends them to the system prompt, then streams a response from `claude-haiku-4-5`. A Next.js 14 frontend sends messages to the backend and renders the SSE stream in real time.

**Tech Stack:** Python 3.11+, FastAPI, voyageai (voyage-3-lite / 1024-dim), numpy, anthropic SDK (claude-haiku-4-5), Next.js 14 (App Router), Tailwind CSS.

## Global Constraints

- Platform: Windows 11 ARM64 — NO chromadb. Vector store = numpy `.npy` + JSON metadata only.
- Voyage AI embedding model: `voyage-3-lite` (1024-dimensional vectors). Never use a different model.
- Response model: `claude-haiku-4-5` via Anthropic Python SDK. Never call Cerebras for real-time chat.
- Vector store: `vector_db/` directory at project root `C:\Users\Akshay\OneDrive\Desktop\MindMusk\`
- Knowledge base: `knowledge_base/` at project root
- `.env` file: project root (loaded with `load_dotenv()` — no path arg needed when run from root)
- Required `.env` keys: `VOYAGE_API_KEY`, `ANTHROPIC_API_KEY`
- Backend port: 8000 (uvicorn). Frontend port: 3000 (Next.js dev).
- Similarity threshold: `0.35` (voyage-3-lite cosine scores are lower than OpenAI; 0.35 is the right floor)
- Top-k per layer: `3` chunks
- `SYSTEM_PROMPT` constant in `backend/llm/prompts.py` must NOT be modified — it is final
- No auth, no payments, no database, no persistent chat history in this plan

---

### Task 1: Update ingest script for all 5 layers and run it

**Files:**
- Modify: `scripts/ingest_knowledge_base.py` (full rewrite)

The existing script only handles 5 hardcoded books across 3 layers. Rewrite it to:
1. Auto-discover ALL `.md` files in `first_order/` and `second_order/` (dynamically, no hardcoding)
2. Keep `third_order/` (4 theme files — glob them too)
3. Add `fourth_order/` (5 mental model files — glob)
4. Add `conversation_style/` (elon_qa_pairs.jsonl as individual chunks + elon_speech_patterns.md normally)

No unit tests for this task — it is a data pipeline script. Verification is checking output files.

**Note:** Runtime is 30–60 minutes due to Voyage free tier (3 RPM). Do not interrupt after starting.

- [ ] **Step 1: Overwrite `scripts/ingest_knowledge_base.py`**

```python
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
    """Glob all *.md in directory, chunk, return (texts, metadata)."""
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
    """Ingest elon_qa_pairs.jsonl (one chunk per pair) + elon_speech_patterns.md."""
    cs_dir = KB / "conversation_style"
    all_texts, all_meta = [], []

    # Q&A pairs — each pair becomes its own retrieval chunk
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

    # Speech pattern analysis — chunk the markdown normally
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

    print("\n[5/5] Fifth Layer — Conversation Style (Q&A + Speech)")
    t, m = ingest_conversation_style()
    save_layer("fifth", t, m)

    print("\n" + "=" * 60)
    print("Ingestion complete. Files in vector_db/:")
    for f in sorted(DB.iterdir()):
        print(f"  {f.name:50s}  {f.stat().st_size // 1024:>6} KB")
    print("=" * 60)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the script (expect 30-60 min)**

```powershell
cd C:\Users\Akshay\OneDrive\Desktop\MindMusk
$env:PYTHONIOENCODING = "utf-8"
python scripts/ingest_knowledge_base.py
```

Let it run to completion. Do not interrupt.

- [ ] **Step 3: Verify output — expect 10 files**

```powershell
Get-ChildItem vector_db\ | Format-Table Name, @{L="KB"; E={[int]($_.Length / 1024)}}
```

Expected: 10 files — `first__embeddings.npy`, `first__metadata.json`, `second__embeddings.npy`, `second__metadata.json`, `third__embeddings.npy`, `third__metadata.json`, `fourth__embeddings.npy`, `fourth__metadata.json`, `fifth__embeddings.npy`, `fifth__metadata.json`. Each `.npy` is several MB.

- [ ] **Step 4: Spot-check metadata**

```powershell
python -c "
import json
from pathlib import Path
for layer in ['first','second','third','fourth','fifth']:
    meta = json.loads(Path(f'vector_db/{layer}__metadata.json').read_text())
    print(f'{layer}: {len(meta)} chunks, e.g. source={meta[0][\"source\"]}')
"
```

Expected: all 5 layers print a non-zero chunk count and a recognizable source name.

- [ ] **Step 5: Commit**

```powershell
git add scripts/ingest_knowledge_base.py
git commit -m "feat: update ingest for all 5 layers with auto-discovery"
```

---

### Task 2: Build `backend/retriever.py` (TDD)

**Files:**
- Create: `backend/__init__.py`
- Create: `backend/retriever.py`
- Create: `tests/__init__.py`
- Create: `tests/test_retriever.py`

Loads numpy arrays from `vector_db/`, embeds a query with Voyage AI, computes cosine similarity against every layer, returns the top-k chunks per layer above a threshold — all in a single `retrieve()` call.

**Interfaces:**
- Produces: `Retriever(vector_db_path: str, api_key: str)` with `retrieve(query: str, top_k: int = 3, threshold: float = 0.35) -> list[dict]`
- Each returned dict: `{id, content, source, layer, chunk_index, score: float}`

- [ ] **Step 1: Create `backend/__init__.py`**

```python
```

(empty file)

- [ ] **Step 2: Create `tests/__init__.py`**

```python
```

(empty file)

- [ ] **Step 3: Write failing tests `tests/test_retriever.py`**

```python
import json
import numpy as np
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def tiny_db(tmp_path):
    """Minimal vector DB: 2 chunks in 'first', 2 in 'second'. All 1024-dim."""
    emb_first = np.array([
        [1.0] + [0.0] * 1023,
        [0.0, 1.0] + [0.0] * 1022,
    ], dtype=np.float32)
    meta_first = [
        {"id": "book_a__chunk_0000", "content": "First A", "source": "book_a", "layer": "first", "chunk_index": 0},
        {"id": "book_b__chunk_0000", "content": "First B", "source": "book_b", "layer": "first", "chunk_index": 0},
    ]
    emb_second = np.array([
        [0.9, 0.1] + [0.0] * 1022,
        [0.0, 0.0, 1.0] + [0.0] * 1021,
    ], dtype=np.float32)
    meta_second = [
        {"id": "synth_a__chunk_0000", "content": "Second A", "source": "synth_a", "layer": "second", "chunk_index": 0},
        {"id": "synth_b__chunk_0000", "content": "Second B", "source": "synth_b", "layer": "second", "chunk_index": 0},
    ]
    np.save(tmp_path / "first__embeddings.npy", emb_first)
    (tmp_path / "first__metadata.json").write_text(json.dumps(meta_first))
    np.save(tmp_path / "second__embeddings.npy", emb_second)
    (tmp_path / "second__metadata.json").write_text(json.dumps(meta_second))
    return tmp_path


def make_retriever(db_path, query_vec):
    """Build a Retriever with a mocked Voyage client returning query_vec."""
    with patch("backend.retriever.voyageai.Client") as MockVoyage:
        mock_client = MagicMock()
        mock_result = MagicMock()
        mock_result.embeddings = [query_vec]
        mock_client.embed.return_value = mock_result
        MockVoyage.return_value = mock_client

        from backend.retriever import Retriever
        r = Retriever(vector_db_path=str(db_path), api_key="fake-key")
        r._voyage = mock_client  # keep the mock for retrieve() calls
    return r


def test_loads_both_layers(tiny_db):
    r = make_retriever(tiny_db, [1.0] + [0.0] * 1023)
    assert "first" in r._layers
    assert "second" in r._layers
    assert r._layers["first"]["embeddings"].shape == (2, 1024)
    assert len(r._layers["first"]["metadata"]) == 2


def test_returns_top_k_per_layer(tiny_db):
    # Query [1,0,...] — closest to chunk 0 of first, chunk 0 of second
    r = make_retriever(tiny_db, [1.0] + [0.0] * 1023)
    results = r.retrieve("anything", top_k=1, threshold=0.0)
    # 1 result per layer × 2 layers = 2 total
    assert len(results) == 2
    first_hits = [c for c in results if c["layer"] == "first"]
    assert first_hits[0]["content"] == "First A"


def test_filters_by_threshold(tiny_db):
    # Query [0,0,1,...] — exactly matches second chunk 1 only (score ≈ 1.0)
    r = make_retriever(tiny_db, [0.0, 0.0, 1.0] + [0.0] * 1021)
    results = r.retrieve("anything", top_k=3, threshold=0.9)
    assert all(c["score"] >= 0.9 for c in results)


def test_score_in_each_chunk(tiny_db):
    r = make_retriever(tiny_db, [1.0] + [0.0] * 1023)
    results = r.retrieve("anything", top_k=2, threshold=0.0)
    for chunk in results:
        assert "score" in chunk
        assert 0.0 <= chunk["score"] <= 1.0


def test_results_sorted_by_score_desc(tiny_db):
    r = make_retriever(tiny_db, [1.0] + [0.0] * 1023)
    results = r.retrieve("anything", top_k=2, threshold=0.0)
    scores = [c["score"] for c in results]
    assert scores == sorted(scores, reverse=True)
```

- [ ] **Step 4: Run tests — verify they fail**

```powershell
cd C:\Users\Akshay\OneDrive\Desktop\MindMusk
python -m pytest tests/test_retriever.py -v 2>&1 | Select-Object -First 15
```

Expected: `ModuleNotFoundError: No module named 'backend.retriever'`

- [ ] **Step 5: Create `backend/retriever.py`**

```python
"""
Retriever: loads all numpy layers from vector_db/, embeds queries via Voyage AI,
returns top-k chunks per layer sorted by cosine similarity descending.
"""

import json
import numpy as np
import voyageai
from pathlib import Path


class Retriever:
    def __init__(self, vector_db_path: str, api_key: str):
        self._db = Path(vector_db_path)
        self._voyage = voyageai.Client(api_key=api_key)
        self._layers: dict[str, dict] = {}
        self._load()

    def _load(self) -> None:
        for emb_path in sorted(self._db.glob("*__embeddings.npy")):
            layer_name = emb_path.stem.replace("__embeddings", "")
            meta_path = self._db / f"{layer_name}__metadata.json"
            if not meta_path.exists():
                continue
            embeddings = np.load(emb_path).astype(np.float32)
            # Pre-normalize rows so retrieval is a dot product
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            norms = np.where(norms == 0, 1.0, norms)
            self._layers[layer_name] = {
                "embeddings": embeddings / norms,
                "metadata": json.loads(meta_path.read_text(encoding="utf-8")),
            }

    def retrieve(self, query: str, top_k: int = 3, threshold: float = 0.35) -> list[dict]:
        """Embed query, search all layers, return top-k per layer above threshold."""
        result = self._voyage.embed([query], model="voyage-3-lite", input_type="query")
        q = np.array(result.embeddings[0], dtype=np.float32)
        norm = np.linalg.norm(q)
        if norm > 0:
            q = q / norm

        chunks: list[dict] = []
        for layer_name, layer in self._layers.items():
            scores = layer["embeddings"] @ q  # cosine similarity (pre-normalized)
            top_indices = np.argsort(scores)[::-1][:top_k]
            for idx in top_indices:
                score = float(scores[idx])
                if score >= threshold:
                    chunk = dict(layer["metadata"][idx])
                    chunk["score"] = score
                    chunk["layer"] = layer_name
                    chunks.append(chunk)

        chunks.sort(key=lambda c: c["score"], reverse=True)
        return chunks
```

- [ ] **Step 6: Run tests — verify they pass**

```powershell
python -m pytest tests/test_retriever.py -v
```

Expected:
```
tests/test_retriever.py::test_loads_both_layers PASSED
tests/test_retriever.py::test_returns_top_k_per_layer PASSED
tests/test_retriever.py::test_filters_by_threshold PASSED
tests/test_retriever.py::test_score_in_each_chunk PASSED
tests/test_retriever.py::test_results_sorted_by_score_desc PASSED
5 passed
```

- [ ] **Step 7: Commit**

```powershell
git add backend/__init__.py backend/retriever.py tests/__init__.py tests/test_retriever.py
git commit -m "feat: add Retriever with Voyage cosine similarity search across all layers"
```

---

### Task 3: Build `backend/pipeline.py` + update prompts (TDD)

**Files:**
- Create: `backend/pipeline.py`
- Create: `tests/test_pipeline.py`
- Modify: `backend/llm/prompts.py` — add `fourth` and `fifth` labels to `build_context_block`

**Interfaces:**
- Consumes: `Retriever.retrieve(query, top_k, threshold)` from Task 2
- Consumes: `SYSTEM_PROMPT` and `build_context_block(chunks)` from `backend/llm/prompts.py`
- Produces: `stream_response(user_message, history, retriever, anthropic_client) -> Generator[str, None, None]`

- [ ] **Step 1: Update `backend/llm/prompts.py` — add fourth/fifth labels**

Find this section (around line 101–110) in `backend/llm/prompts.py`:

```python
        if layer == "first":
            label = f"[Raw Book — {source}]"
        elif layer == "second":
            label = f"[Elon's Synthesis — {source}]"
        elif layer == "third":
            label = f"[Cross-Book Theme — {source}]"
        else:
            label = f"[{source}]"
```

Replace it with:

```python
        if layer == "first":
            label = f"[Raw Book — {source}]"
        elif layer == "second":
            label = f"[Elon's Synthesis — {source}]"
        elif layer == "third":
            label = f"[Cross-Book Theme — {source}]"
        elif layer == "fourth":
            label = f"[Mental Model — {source}]"
        elif layer == "fifth":
            label = f"[Voice Pattern — {source}]"
        else:
            label = f"[{source}]"
```

- [ ] **Step 2: Write failing tests `tests/test_pipeline.py`**

```python
from unittest.mock import MagicMock


def make_fake_retriever(chunks: list[dict]):
    r = MagicMock()
    r.retrieve.return_value = chunks
    return r


def make_fake_anthropic(stream_texts: list[str]):
    """Simulate Anthropic streaming: stream_texts is list of text chunks yielded."""
    mock_client = MagicMock()
    events = []
    for text in stream_texts:
        evt = MagicMock()
        evt.type = "content_block_delta"
        evt.delta = MagicMock()
        evt.delta.text = text
        events.append(evt)
    mock_stream = MagicMock()
    mock_stream.__iter__ = lambda self: iter(events)
    mock_stream.__enter__ = lambda self: self
    mock_stream.__exit__ = MagicMock(return_value=False)
    mock_client.messages.stream.return_value = mock_stream
    return mock_client


def test_yields_text_chunks():
    from backend.pipeline import stream_response

    retriever = make_fake_retriever([
        {"content": "rockets cost too much", "source": "book_a", "layer": "first", "score": 0.8}
    ])
    client = make_fake_anthropic(["Well,", " the thing is..."])

    result = list(stream_response(
        user_message="How do you think about cost?",
        history=[],
        retriever=retriever,
        anthropic_client=client,
    ))

    assert result == ["Well,", " the thing is..."]


def test_calls_retrieve_with_correct_args():
    from backend.pipeline import stream_response

    retriever = make_fake_retriever([])
    client = make_fake_anthropic(["ok"])

    list(stream_response("What about Mars?", [], retriever, client))

    retriever.retrieve.assert_called_once_with("What about Mars?", top_k=3, threshold=0.35)


def test_includes_history_in_messages():
    from backend.pipeline import stream_response

    retriever = make_fake_retriever([])
    client = make_fake_anthropic(["sure"])

    history = [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello."},
    ]

    list(stream_response("Follow-up", history, retriever, client))

    call_kwargs = client.messages.stream.call_args.kwargs
    messages_sent = call_kwargs["messages"]
    assert any(m["content"] == "Hi" for m in messages_sent)
    assert any(m["content"] == "Follow-up" for m in messages_sent)


def test_skips_non_delta_events():
    from backend.pipeline import stream_response

    retriever = make_fake_retriever([])
    mock_client = MagicMock()

    good_evt = MagicMock()
    good_evt.type = "content_block_delta"
    good_evt.delta = MagicMock()
    good_evt.delta.text = "hello"

    bad_evt = MagicMock()
    bad_evt.type = "message_start"  # not content_block_delta

    mock_stream = MagicMock()
    mock_stream.__iter__ = lambda self: iter([bad_evt, good_evt])
    mock_stream.__enter__ = lambda self: self
    mock_stream.__exit__ = MagicMock(return_value=False)
    mock_client.messages.stream.return_value = mock_stream

    result = list(stream_response("hi", [], retriever, mock_client))
    assert result == ["hello"]


def test_trims_history_to_last_6_turns():
    from backend.pipeline import stream_response

    retriever = make_fake_retriever([])
    client = make_fake_anthropic(["ok"])

    # 10 turns of history (20 messages)
    history = []
    for i in range(10):
        history.append({"role": "user", "content": f"user msg {i}"})
        history.append({"role": "assistant", "content": f"assistant msg {i}"})

    list(stream_response("new question", history, retriever, client))

    call_kwargs = client.messages.stream.call_args.kwargs
    messages_sent = call_kwargs["messages"]
    # 6 turns × 2 = 12 history messages + 1 new user message = 13 max
    assert len(messages_sent) <= 13
```

- [ ] **Step 3: Run tests — verify they fail**

```powershell
python -m pytest tests/test_pipeline.py -v 2>&1 | Select-Object -First 15
```

Expected: `ModuleNotFoundError: No module named 'backend.pipeline'`

- [ ] **Step 4: Create `backend/pipeline.py`**

```python
"""
Pipeline: retrieves context chunks, builds full prompt, streams Claude response.
"""

from typing import Generator
from backend.retriever import Retriever
from backend.llm.prompts import SYSTEM_PROMPT, build_context_block

MAX_HISTORY_TURNS = 6  # keep last 6 turns (12 messages) to control token cost


def stream_response(
    user_message: str,
    history: list[dict],
    retriever: Retriever,
    anthropic_client,
) -> Generator[str, None, None]:
    """
    Retrieve relevant chunks, assemble prompt, stream text from claude-haiku-4-5.
    history: list of {role: "user"|"assistant", content: str}
    Yields text strings (not SSE-formatted — caller adds data: prefix).
    """
    chunks = retriever.retrieve(user_message, top_k=3, threshold=0.35)
    context_block = build_context_block(chunks)

    system = SYSTEM_PROMPT.rstrip()
    if context_block:
        system = system + "\n" + context_block

    recent_history = history[-(MAX_HISTORY_TURNS * 2):]
    messages = list(recent_history) + [{"role": "user", "content": user_message}]

    with anthropic_client.messages.stream(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=system,
        messages=messages,
    ) as stream:
        for event in stream:
            if event.type == "content_block_delta":
                text = getattr(event.delta, "text", "")
                if text:
                    yield text
```

- [ ] **Step 5: Run tests — verify they pass**

```powershell
python -m pytest tests/test_pipeline.py -v
```

Expected:
```
tests/test_pipeline.py::test_yields_text_chunks PASSED
tests/test_pipeline.py::test_calls_retrieve_with_correct_args PASSED
tests/test_pipeline.py::test_includes_history_in_messages PASSED
tests/test_pipeline.py::test_skips_non_delta_events PASSED
tests/test_pipeline.py::test_trims_history_to_last_6_turns PASSED
5 passed
```

- [ ] **Step 6: Commit**

```powershell
git add backend/pipeline.py backend/llm/prompts.py tests/test_pipeline.py
git commit -m "feat: add pipeline with context retrieval and claude-haiku-4-5 streaming"
```

---

### Task 4: Build `backend/main.py` FastAPI app (TDD)

**Files:**
- Create: `backend/main.py`
- Create: `backend/requirements.txt`
- Create: `tests/test_main.py`

Single endpoint: `POST /chat` accepts `{message, history}`, streams SSE. `GET /health` returns `{"status": "ok"}`.

**Interfaces:**
- Consumes: `stream_response(...)` from `backend/pipeline.py` (Task 3)
- Consumes: `Retriever` from `backend/retriever.py` (Task 2)
- Produces: `GET /health` → `{"status": "ok"}` and `POST /chat` → `text/event-stream`
- SSE format: `data: <text>\n\n` per chunk, `data: [DONE]\n\n` at end

- [ ] **Step 1: Create `backend/requirements.txt`**

```
fastapi==0.115.0
uvicorn[standard]==0.30.6
voyageai==0.2.3
anthropic==0.40.0
numpy==1.26.4
python-dotenv==1.0.1
httpx==0.27.0
pytest==8.3.3
```

Install:

```powershell
cd C:\Users\Akshay\OneDrive\Desktop\MindMusk
pip install -r backend/requirements.txt
```

- [ ] **Step 2: Write failing tests `tests/test_main.py`**

```python
import pytest
from unittest.mock import MagicMock, patch


def build_mock_stream(texts: list[str]):
    events = []
    for text in texts:
        evt = MagicMock()
        evt.type = "content_block_delta"
        evt.delta = MagicMock()
        evt.delta.text = text
        events.append(evt)
    mock_stream = MagicMock()
    mock_stream.__iter__ = lambda self: iter(events)
    mock_stream.__enter__ = lambda self: self
    mock_stream.__exit__ = MagicMock(return_value=False)
    return mock_stream


def get_test_client(stream_texts=None):
    if stream_texts is None:
        stream_texts = ["The answer is 42."]

    # Must patch before importing app to prevent real API calls at startup
    with patch("backend.main.Retriever") as MockRetriever, \
         patch("backend.main.anthropic_lib.Anthropic") as MockAnthropic:

        mock_retriever = MagicMock()
        mock_retriever.retrieve.return_value = []
        MockRetriever.return_value = mock_retriever

        mock_client = MagicMock()
        mock_client.messages.stream.return_value = build_mock_stream(stream_texts)
        MockAnthropic.return_value = mock_client

        import importlib
        import backend.main as main_module
        importlib.reload(main_module)

        from fastapi.testclient import TestClient
        return TestClient(main_module.app)


def test_health():
    client = get_test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_chat_200():
    client = get_test_client(["Hello"])
    resp = client.post("/chat", json={"message": "Hi", "history": []})
    assert resp.status_code == 200


def test_chat_content_type_is_sse():
    client = get_test_client(["Hello"])
    resp = client.post("/chat", json={"message": "Hi", "history": []})
    assert "text/event-stream" in resp.headers["content-type"]


def test_chat_body_contains_text_and_done():
    client = get_test_client(["First", " second"])
    resp = client.post("/chat", json={"message": "Hi", "history": []})
    body = resp.text
    assert "First" in body
    assert "second" in body
    assert "[DONE]" in body


def test_chat_rejects_empty_message():
    client = get_test_client()
    resp = client.post("/chat", json={"message": "", "history": []})
    assert resp.status_code == 422


def test_chat_accepts_history():
    client = get_test_client(["ok"])
    resp = client.post("/chat", json={
        "message": "What next?",
        "history": [
            {"role": "user", "content": "What about Mars?"},
            {"role": "assistant", "content": "It matters."},
        ]
    })
    assert resp.status_code == 200
```

- [ ] **Step 3: Run tests — verify they fail**

```powershell
python -m pytest tests/test_main.py -v 2>&1 | Select-Object -First 15
```

Expected: `ModuleNotFoundError: No module named 'backend.main'`

- [ ] **Step 4: Create `backend/main.py`**

```python
"""
MindMusk FastAPI backend.
GET  /health  — liveness check
POST /chat    — SSE streaming response
"""

import os
from typing import AsyncGenerator

import anthropic as anthropic_lib
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, field_validator

from backend.retriever import Retriever
from backend.pipeline import stream_response

load_dotenv()

app = FastAPI(title="MindMusk API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

_retriever: Retriever | None = None
_anthropic: anthropic_lib.Anthropic | None = None


@app.on_event("startup")
def startup() -> None:
    global _retriever, _anthropic
    vector_db = os.getenv("VECTOR_DB_PATH", "vector_db")
    _retriever = Retriever(
        vector_db_path=vector_db,
        api_key=os.getenv("VOYAGE_API_KEY", ""),
    )
    _anthropic = anthropic_lib.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
    print(f"[startup] {len(_retriever._layers)} layers loaded from {vector_db}/")


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("message cannot be empty")
        return v


async def sse_generator(user_message: str, history: list[dict]) -> AsyncGenerator[str, None]:
    for text in stream_response(user_message, history, _retriever, _anthropic):
        yield f"data: {text}\n\n"
    yield "data: [DONE]\n\n"


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat")
async def chat(req: ChatRequest) -> StreamingResponse:
    return StreamingResponse(
        sse_generator(req.message, req.history),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```

- [ ] **Step 5: Run tests — verify they pass**

```powershell
python -m pytest tests/test_main.py -v
```

Expected:
```
tests/test_main.py::test_health PASSED
tests/test_main.py::test_chat_200 PASSED
tests/test_main.py::test_chat_content_type_is_sse PASSED
tests/test_main.py::test_chat_body_contains_text_and_done PASSED
tests/test_main.py::test_chat_rejects_empty_message PASSED
tests/test_main.py::test_chat_accepts_history PASSED
6 passed
```

- [ ] **Step 6: Run all tests**

```powershell
python -m pytest tests/ -v
```

Expected: 16 tests, all PASSED.

- [ ] **Step 7: Smoke-test the live backend**

```powershell
# Terminal 1
cd C:\Users\Akshay\OneDrive\Desktop\MindMusk
uvicorn backend.main:app --reload --port 8000
```

```powershell
# Terminal 2
Invoke-WebRequest -Uri http://localhost:8000/health -Method GET | Select-Object -ExpandProperty Content
```

Expected: `{"status":"ok"}`

Then test chat (will make a real API call — costs ~$0.002):

```powershell
Invoke-WebRequest -Uri http://localhost:8000/chat `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"message":"How do you think about cost reduction?","history":[]}' | `
  Select-Object -ExpandProperty Content
```

Expected: SSE stream with `data: <text chunk>` lines and a final `data: [DONE]`.

- [ ] **Step 8: Commit**

```powershell
git add backend/main.py backend/requirements.txt tests/test_main.py
git commit -m "feat: add FastAPI app with SSE /chat endpoint"
```

---

### Task 5: Build Next.js 14 frontend chat UI

**Files:**
- Create: `frontend/` (scaffolded via create-next-app then customized)
- Modify: `frontend/app/globals.css`
- Replace: `frontend/app/layout.tsx`
- Replace: `frontend/app/page.tsx`
- Create: `frontend/components/ChatInterface.tsx`
- Create: `frontend/.env.local`

Minimal dark chat UI: scrollable message list, fixed input bar at bottom, Elon label on assistant messages, streaming text rendered as it arrives.

No unit tests for the frontend in this plan — verify by running it in the browser.

- [ ] **Step 1: Scaffold Next.js app**

```powershell
cd C:\Users\Akshay\OneDrive\Desktop\MindMusk
npx create-next-app@14 frontend --typescript --tailwind --app --no-eslint --no-src-dir --import-alias "@/*"
```

Answer "No" to all optional prompts except `--tailwind` (already passed as flag).

- [ ] **Step 2: Create `frontend/.env.local`**

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

- [ ] **Step 3: Replace `frontend/app/globals.css`**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

html, body {
  height: 100%;
  margin: 0;
}
```

- [ ] **Step 4: Replace `frontend/app/layout.tsx`**

```tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "MindMusk",
  description: "Think with Elon",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-black text-white h-full`}>
        {children}
      </body>
    </html>
  );
}
```

- [ ] **Step 5: Create `frontend/components/ChatInterface.tsx`**

```tsx
"use client";

import { useState, useRef, useEffect, FormEvent } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const userMessage = input.trim();
    if (!userMessage || loading) return;

    setInput("");
    const newMessages: Message[] = [
      ...messages,
      { role: "user", content: userMessage },
    ];
    setMessages([...newMessages, { role: "assistant", content: "" }]);
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMessage,
          history: newMessages
            .slice(-12)
            .map((m) => ({ role: m.role, content: m.content })),
        }),
      });

      if (!response.ok || !response.body) {
        throw new Error(`HTTP ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split("\n");
        buffer = lines.pop() ?? "";

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const chunk = line.slice(6);
          if (chunk === "[DONE]") break;
          setMessages((prev) => {
            const updated = [...prev];
            const last = updated[updated.length - 1];
            updated[updated.length - 1] = {
              ...last,
              content: last.content + chunk,
            };
            return updated;
          });
        }
      }
    } catch (err) {
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          content: `Connection error. Is the backend running at ${API_URL}?`,
        };
        return updated;
      });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <div className="border-b border-zinc-800 px-6 py-4 flex-shrink-0">
        <h1 className="text-lg font-semibold tracking-tight">MindMusk</h1>
        <p className="text-xs text-zinc-500 mt-0.5">Think with Elon</p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6">
        {messages.length === 0 && (
          <div className="text-center text-zinc-600 mt-20">
            <p className="text-2xl font-bold mb-2">
              What problem are you actually solving?
            </p>
            <p className="text-sm">Ask Elon anything.</p>
          </div>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-2xl px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${
                msg.role === "user"
                  ? "bg-zinc-800 text-white"
                  : "bg-transparent text-zinc-100"
              }`}
            >
              {msg.role === "assistant" && (
                <p className="text-xs text-zinc-500 mb-1 font-medium tracking-widest">
                  ELON
                </p>
              )}
              {msg.content}
              {loading &&
                i === messages.length - 1 &&
                msg.role === "assistant" &&
                msg.content === "" && (
                  <span className="text-zinc-500 animate-pulse">▋</span>
                )}
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <form
        onSubmit={handleSubmit}
        className="border-t border-zinc-800 px-6 py-4 flex gap-3 flex-shrink-0"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
          placeholder="Ask anything..."
          className="flex-1 bg-zinc-900 border border-zinc-700 rounded-xl px-4 py-3 text-sm text-white placeholder-zinc-600 focus:outline-none focus:border-zinc-500 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="bg-white text-black px-5 py-3 rounded-xl text-sm font-medium hover:bg-zinc-200 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? "..." : "Send"}
        </button>
      </form>
    </div>
  );
}
```

- [ ] **Step 6: Replace `frontend/app/page.tsx`**

```tsx
import ChatInterface from "@/components/ChatInterface";

export default function Home() {
  return <ChatInterface />;
}
```

- [ ] **Step 7: TypeScript build check**

```powershell
cd C:\Users\Akshay\OneDrive\Desktop\MindMusk\frontend
npm run build
```

Expected: `✓ Compiled successfully` with no TypeScript errors.

- [ ] **Step 8: Run dev server and test in browser**

```powershell
# Ensure backend is still running on port 8000 (from Task 4 smoke test)

cd C:\Users\Akshay\OneDrive\Desktop\MindMusk\frontend
npm run dev
```

Open http://localhost:3000. Verify the golden path:
1. Empty state shows "What problem are you actually solving?"
2. Type a message → user bubble appears right-aligned in zinc-800
3. "ELON" label appears above blank assistant area immediately
4. Text streams in progressively (not all at once)
5. Chat scrolls to bottom automatically
6. Button shows "..." during loading, "Send" after
7. Button is disabled while loading

Also test edge case: send a second message while the first is still rendering — should be blocked (button disabled).

- [ ] **Step 9: Commit**

```powershell
cd C:\Users\Akshay\OneDrive\Desktop\MindMusk
git add frontend/
git commit -m "feat: add Next.js 14 chat UI with SSE streaming"
```

---

## Summary — What This Produces

After all 5 tasks complete:

| What | Where |
|---|---|
| 5-layer vector store (all books + Q&A + speech) | `vector_db/` |
| Backend running | `http://localhost:8000` |
| Frontend running | `http://localhost:3000` |
| All 16 unit tests passing | `tests/` |

The working demo is done. Next steps (not in this plan): deploy to Railway + Vercel, add Stripe payments, add user auth.
