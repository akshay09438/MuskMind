import json
import numpy as np
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def tiny_db(tmp_path):
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
    with patch("backend.retriever.voyageai.Client") as MockVoyage:
        mock_client = MagicMock()
        mock_result = MagicMock()
        mock_result.embeddings = [query_vec]
        mock_client.embed.return_value = mock_result
        MockVoyage.return_value = mock_client

        from backend.retriever import Retriever
        r = Retriever(vector_db_path=str(db_path), api_key="fake-key")
        r._voyage = mock_client
    return r


def test_loads_both_layers(tiny_db):
    r = make_retriever(tiny_db, [1.0] + [0.0] * 1023)
    assert "first" in r._layers
    assert "second" in r._layers
    assert r._layers["first"]["embeddings"].shape == (2, 1024)


def test_returns_top_k_per_layer(tiny_db):
    r = make_retriever(tiny_db, [1.0] + [0.0] * 1023)
    results = r.retrieve("anything", top_k=1, threshold=0.0)
    assert len(results) == 2
    first_hits = [c for c in results if c["layer"] == "first"]
    assert first_hits[0]["content"] == "First A"


def test_filters_by_threshold(tiny_db):
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
