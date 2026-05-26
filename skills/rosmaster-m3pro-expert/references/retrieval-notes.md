# Retrieval Notes

The skill bundles the SQLite implementation from this repository's `sqlite-rag/` directory.

Default assets:

- Corpus: `assets/corpus/`
- Index: `assets/index/rosmaster_m3pro.sqlite`
- Query wrapper: `scripts/query_robot_docs.py`
- Rebuild wrapper: `scripts/build_index.py`

Final retrieval configuration:

- Embedding model: `BAAI/bge-small-en-v1.5`
- Index variant: heading-aware SQLite DB
- Chunking: `legacy`
- Hybrid fusion: semantic vector search plus SQLite FTS5 keyword search with Reciprocal Rank Fusion
- Heading BM25 weight: `1.0`

The skill-local scripts intentionally expose only the happy path: one model, one chunking strategy, one heading-aware schema, and hybrid retrieval. Query output is always JSON with source paths, best-effort line numbers, headings, scores, snippets, and full chunk text.

The Markdown corpus is converted from vendor/course PDFs and may contain PDF conversion artifacts. Prefer retrieved commands, file names, and headings, but phrase final answers clearly rather than copying noisy conversion text.
