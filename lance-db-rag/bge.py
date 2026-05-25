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


class _BGEBase(EmbeddingFunction):
    """BGE with the asymmetric query-instruction prefix BAAI recommends.

    Subclasses pin `name` and `ndims` so LanceDB can rehydrate the embedding
    function from the table schema — the registered name is what's stored.
    """

    name: str = ""

    def ndims(self) -> int:
        raise NotImplementedError

    def compute_source_embeddings(self, texts, *args, **kwargs):
        model = _get_model(self.name)
        items = _as_str_list(texts)
        return model.encode(items, normalize_embeddings=True).tolist()

    def compute_query_embeddings(self, query: Union[str, list], *args, **kwargs):
        model = _get_model(self.name)
        items = _as_str_list(query)
        prefixed = [QUERY_INSTRUCTION + s for s in items]
        return model.encode(prefixed, normalize_embeddings=True).tolist()


@register("bge-small-en-v1.5")
class BGE(_BGEBase):
    name: str = "BAAI/bge-small-en-v1.5"

    def ndims(self) -> int:
        return 384


@register("bge-large-en-v1.5")
class BGELarge(_BGEBase):
    name: str = "BAAI/bge-large-en-v1.5"

    def ndims(self) -> int:
        return 1024


VARIANTS = {"small": BGE, "large": BGELarge}


def _as_str_list(x) -> list[str]:
    """Coerce LanceDB inputs (str, list[str], pyarrow Array/StringScalar, etc.) to list[str]."""
    if isinstance(x, str):
        return [x]
    if hasattr(x, "to_pylist"):  # pyarrow.Array / ChunkedArray
        return [str(s) for s in x.to_pylist()]
    return [s.as_py() if hasattr(s, "as_py") else str(s) for s in x]
