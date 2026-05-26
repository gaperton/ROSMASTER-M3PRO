# lance-db-rag

LanceDB-backed local hybrid retrieval over [`../markdown/`](../markdown/). This implementation is kept in parallel with [`../sqlite-rag/`](../sqlite-rag/) so engine behavior can be compared under the same chunking, embedding model, query processing, and evaluation harness.

For research conclusions and final benchmark numbers, see the root [README](../README.md) and [PS-LEDGER.md](../PS-LEDGER.md).

## Use

```powershell
pip install -r lance-db-rag/rag_requirements.txt

# Final research index: heading-aware schema, BGE-small, legacy chunking.
python lance-db-rag/rag_index.py --db lance-db-rag/index.h.lance --variant small --chunking legacy --rebuild

# Query the final index.
python lance-db-rag/rag_query.py --db lance-db-rag/index.h.lance "How do I make the robot map a room?"
python lance-db-rag/rag_query.py --db lance-db-rag/index.h.lance "How do I send a velocity command from the terminal?"
```

Default paths still work for ad-hoc local indexing:

```powershell
python lance-db-rag/rag_index.py
python lance-db-rag/rag_query.py "ros2 topic list"
```

Useful options:

| Command | Option | Meaning |
|---|---|---|
| `rag_index.py` | `--docs` | Markdown root, default `../markdown` |
| `rag_index.py` | `--db` | LanceDB directory |
| `rag_index.py` | `--variant small\|large` | Embedding variant; final default is `small` |
| `rag_index.py` | `--chunking legacy\|boundary` | Final default is `legacy`; `boundary` preserves the NX9 experiment |
| `rag_query.py` | `--mode hybrid\|semantic\|keyword` | Retrieval mode, default `hybrid` |
| `rag_query.py` | `--rerank` | Optional cross-encoder reranking; off by default because experiments 6-8 were net negative |
| `rag_query.py` | `--full` | Print full chunk text |

## Implementation Notes

- Final model: `BAAI/bge-small-en-v1.5`.
- Final index variant: `index.h.lance`.
- LanceDB stores the index as a directory, not a single file.
- `bge.py` must remain importable by both the indexer and query script because LanceDB restores the registered embedding function by name.
- Hybrid search is orchestrated manually for parity with sqlite-rag: vector search, stop-word-filtered FTS, widened candidate pools, Python-side RRF, then the same narrow route-boost layer.
- Reranking remains available for experiments, but it is not part of the final recommended pipeline.

## Files

```text
lance-db-rag/
|-- bge.py                # registered BGE embedding functions
|-- rag_index.py          # build / refresh the LanceDB index
|-- rag_query.py          # query the LanceDB index
|-- rag_requirements.txt  # Python dependencies
|-- index.lance/          # default generated index
`-- index.h.lance/        # final heading-aware research index
```
