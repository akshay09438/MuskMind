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
            scores = layer["embeddings"] @ q
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
