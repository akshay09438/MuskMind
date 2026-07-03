"""
Pure chunking + merge logic for adding new source material to the
'fifth' (conversation_style) vector_db layer. No API calls, no I/O —
fully unit-testable.
"""

import numpy as np


def chunk_by_paragraphs(text: str, max_chars: int = 1600) -> list[str]:
    """
    Split text into chunks along paragraph boundaries ('\\n\\n'), never
    cutting a single paragraph in half. Greedily accumulates paragraphs
    into a chunk until adding the next one would exceed max_chars, then
    starts a new chunk. A single paragraph longer than max_chars becomes
    its own (oversized) chunk rather than being split mid-thought.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for p in paragraphs:
        added_len = len(p) + (2 if current else 0)
        if current and current_len + added_len > max_chars:
            chunks.append("\n\n".join(current))
            current = [p]
            current_len = len(p)
        else:
            current.append(p)
            current_len += added_len

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def merge_fifth_layer(
    existing_embeddings: np.ndarray,
    existing_metadata: list[dict],
    new_chunks: list[str],
    new_embeddings: list[list[float]],
    source_name: str,
) -> tuple[np.ndarray, list[dict]]:
    """
    Append newly embedded chunks to an existing layer's embeddings array
    and metadata list, preserving existing entries and their order.
    """
    new_meta = [
        {
            "id": f"{source_name}__chunk_{i:04d}",
            "content": chunk,
            "source": source_name,
            "layer": "fifth",
            "chunk_index": i,
        }
        for i, chunk in enumerate(new_chunks)
    ]
    new_emb_arr = np.array(new_embeddings, dtype=np.float32)
    merged_embeddings = np.concatenate([existing_embeddings, new_emb_arr], axis=0)
    merged_metadata = existing_metadata + new_meta
    return merged_embeddings, merged_metadata
