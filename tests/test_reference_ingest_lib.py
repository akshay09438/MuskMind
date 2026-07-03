import numpy as np
from scripts.reference_ingest_lib import chunk_by_paragraphs, merge_fifth_layer


def test_chunk_by_paragraphs_keeps_small_text_as_one_chunk():
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
    chunks = chunk_by_paragraphs(text, max_chars=1600)
    assert chunks == ["First paragraph.\n\nSecond paragraph.\n\nThird paragraph."]


def test_chunk_by_paragraphs_splits_when_exceeding_max_chars():
    para_a = "A" * 900
    para_b = "B" * 900
    text = f"{para_a}\n\n{para_b}"
    chunks = chunk_by_paragraphs(text, max_chars=1000)
    assert len(chunks) == 2
    assert chunks[0] == para_a
    assert chunks[1] == para_b


def test_chunk_by_paragraphs_never_splits_a_single_paragraph():
    oversized = "X" * 5000
    text = f"short one.\n\n{oversized}\n\nshort two."
    chunks = chunk_by_paragraphs(text, max_chars=1600)
    assert oversized in chunks


def test_chunk_by_paragraphs_strips_blank_lines():
    text = "First.\n\n\n\nSecond."
    chunks = chunk_by_paragraphs(text, max_chars=1600)
    assert chunks == ["First.\n\nSecond."]


def test_merge_fifth_layer_concatenates_embeddings():
    existing_emb = np.array([[1.0, 0.0]], dtype=np.float32)
    existing_meta = [
        {"id": "old__chunk_0000", "content": "old chunk", "source": "old", "layer": "fifth", "chunk_index": 0},
    ]
    new_chunks = ["new chunk one", "new chunk two"]
    new_embeddings = [[0.5, 0.5], [0.2, 0.8]]

    merged_emb, merged_meta = merge_fifth_layer(
        existing_emb, existing_meta, new_chunks, new_embeddings, "chatgpt_reference_conversations"
    )

    assert merged_emb.shape == (3, 2)
    assert len(merged_meta) == 3
    assert merged_meta[0]["source"] == "old"
    assert merged_meta[1]["source"] == "chatgpt_reference_conversations"
    assert merged_meta[1]["id"] == "chatgpt_reference_conversations__chunk_0000"
    assert merged_meta[2]["id"] == "chatgpt_reference_conversations__chunk_0001"
    assert merged_meta[1]["content"] == "new chunk one"
