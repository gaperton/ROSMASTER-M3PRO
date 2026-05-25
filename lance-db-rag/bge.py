"""BGE embedding function for LanceDB.

Lives in its own module because both rag_index.py and rag_query.py must import
it: importing runs the @register decorator, which is what lets LanceDB rehydrate
the embedding function that was attached to the chunks table at create time.
Without that import in rag_query.py, opening the table would error out.
"""
from __future__ import annotations

from typing import Union

from lancedb.embeddings import EmbeddingFunction, register
from sentence_transformers import SentenceTransformer

QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "

# Module-level cache so we don't reload the model on every method call and don't
# have to fight pydantic about private attributes on the EmbeddingFunction.
_MODEL_CACHE: dict[str, SentenceTransformer] = {}


def _get_model(name: str) -> SentenceTransformer:
    if name not in _MODEL_CACHE:
        _MODEL_CACHE[name] = SentenceTransformer(name)
    return _MODEL_CACHE[name]


@register("bge-small-en-v1.5")
class BGE(EmbeddingFunction):
    """BGE-small with the asymmetric query-instruction prefix BAAI recommends."""

    name: str = "BAAI/bge-small-en-v1.5"

    def ndims(self) -> int:
        return 384

    def compute_source_embeddings(self, texts, *args, **kwargs):
        model = _get_model(self.name)
        items = list(texts) if not isinstance(texts, str) else [texts]
        return model.encode(items, normalize_embeddings=True).tolist()

    def compute_query_embeddings(self, query: Union[str, list], *args, **kwargs):
        model = _get_model(self.name)
        items = [query] if isinstance(query, str) else list(query)
        prefixed = [QUERY_INSTRUCTION + s for s in items]
        return model.encode(prefixed, normalize_embeddings=True).tolist()
