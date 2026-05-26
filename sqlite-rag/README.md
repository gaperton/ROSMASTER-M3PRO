# sqlite-rag

SQLite-backed local hybrid retrieval over [`../markdown/`](../markdown/). This is the lighter of the two RAG implementations: one portable `.db` file, SQLite FTS5 for keyword search, sqlite-vec for vector search, and no background service.

For research conclusions and final benchmark numbers, see the root [README](../README.md) and [PS-LEDGER.md](../PS-LEDGER.md).

## Use

```powershell
pip install -r sqlite-rag/rag_requirements.txt

# Final research index: heading-aware schema, BGE-small, legacy chunking.
python sqlite-rag/rag_index.py --db sqlite-rag/rag_index.h.db --model BAAI/bge-small-en-v1.5 --chunking legacy --rebuild

# Query the final index.
python sqlite-rag/rag_query.py --db sqlite-rag/rag_index.h.db "How do I make the robot map a room?"
python sqlite-rag/rag_query.py --db sqlite-rag/rag_index.h.db "How do I send a velocity command from the terminal?"
```

Default paths still work for ad-hoc local indexing:

```powershell
python sqlite-rag/rag_index.py
python sqlite-rag/rag_query.py "ros2 topic list"
```

Useful options:

| Command | Option | Meaning |
|---|---|---|
| `rag_index.py` | `--docs` | Markdown root, default `../markdown` |
| `rag_index.py` | `--db` | SQLite index path |
| `rag_index.py` | `--chunking legacy\|boundary` | Final default is `legacy`; `boundary` preserves the NX9 experiment |
| `rag_query.py` | `--mode hybrid\|semantic\|keyword` | Retrieval mode, default `hybrid` |
| `rag_query.py` | `--bm25-heading-weight` | Heading BM25 weight for heading-aware indexes; final value is `1.0` |
| `rag_query.py` | `--full` | Print full chunk text |

## Implementation Notes

- Final model: `BAAI/bge-small-en-v1.5`.
- Final index variant: `rag_index.h.db`.
- Semantic search embeds `heading_path + body` and query text with the BGE query instruction.
- Keyword search uses FTS5 over heading and body text, with stop-word-filtered OR queries.
- Hybrid search fuses semantic and keyword ranks with Reciprocal Rank Fusion.
- A narrow local query-profile layer expands a few beginner intents and applies small post-fusion route boosts.

## Files

```text
sqlite-rag/
|-- rag_index.py          # build / refresh the SQLite index
|-- rag_query.py          # query the SQLite index
|-- rag_requirements.txt  # Python dependencies
|-- rag_index.db          # default generated index
`-- rag_index.h.db        # final heading-aware research index
```
