# sqlite-rag

Local, file-based RAG retrieval over the repo's markdown course material. No background services, no network calls after the first model download, no external vector DB. The whole index is a single SQLite file you can copy, gitignore, or delete.

## When to use it

You have a folder of markdown and you want to ask natural-language questions like *"how do I unlock the controller buttons"* or *"moveit2 pick and place"* and get back the most relevant chunks with file paths and heading breadcrumbs. Retrieval only — no LLM answer synthesis (you read the chunks yourself, or pipe them somewhere else).

## How to use

```powershell
pip install -r sqlite-rag/rag_requirements.txt

# (Re)build the index. First run downloads the ~130 MB BGE model into your
# HuggingFace cache; subsequent runs are incremental (sha256 per file).
python sqlite-rag/rag_index.py

# Ask a question.
python sqlite-rag/rag_query.py "how do I unlock the controller buttons"
python sqlite-rag/rag_query.py "moveit2 pick and place" -k 5
python sqlite-rag/rag_query.py "lidar setup" --full
```

Defaults resolve relative to the script location, so the commands work from any cwd:
- `--docs` → `<repo>/markdown`
- `--db`   → `<repo>/sqlite-rag/rag_index.db`
- `--model` → `BAAI/bge-small-en-v1.5` (384-dim, English)

## Design

### Two scripts, one file

The system splits cleanly along read/write lines:

- [rag_index.py](rag_index.py) — write side. Walks the docs folder, chunks, embeds, writes to SQLite.
- [rag_query.py](rag_query.py) — read side. Embeds the query, runs ANN search, prints results.

Everything they share lives in **one SQLite file** (`rag_index.db`). That file is the entire index: text, metadata, and vectors. It's portable, diffable-ish, and easy to back up or throw away. No daemon, no lock files, no migration system.

### Storage layout

The index uses three tables in a single SQLite database, with the [`sqlite-vec`](https://github.com/asg017/sqlite-vec) extension loaded at runtime for the vector virtual table:

```
files(path PRIMARY KEY, hash)                       -- one row per markdown file, sha256 of contents
chunks(id PK, file_path, heading_path, ord, text)   -- one row per chunk, with H1>H2>H3 breadcrumb
vec_chunks(rowid, embedding float[384])             -- vec0 virtual table; rowid matches chunks.id
```

`chunks.id` and `vec_chunks.rowid` are kept in 1:1 correspondence; the query joins them by id. `files.hash` is what makes indexing incremental: on each run we compare the on-disk sha256 to the stored hash and skip files that haven't changed. Deleted files are detected by set-difference (`in_db - on_disk`) and pruned.

### Chunking

Markdown is split heading-aware, then size-clamped:

1. `split_by_headings` walks `#`/`##`/... matches and emits `(heading_path, body)` sections, where `heading_path` is the stack of ancestor titles (so a chunk under `## Lidar > ### Calibration` carries both).
2. Sections longer than `CHUNK_TARGET_CHARS = 1800` are sliced with `CHUNK_OVERLAP_CHARS = 300` of overlap so a paragraph straddling a chunk boundary is still recoverable.
3. Short sections are kept whole. Empty sections are dropped.

The breadcrumb is stored as a single `" > "`-joined string in `chunks.heading_path` and is printed with every search result so you know *where* in the doc the chunk lives, not just which file.

### Embeddings

- Model: `BAAI/bge-small-en-v1.5`, 384-dim, L2-normalized.
- Documents are embedded as-is.
- Queries are prefixed with `"Represent this sentence for searching relevant passages: "` — BGE-v1.5's recommended instruction for the asymmetric (query→passage) retrieval setting.
- Encoding is batched (`batch_size=32`) so the SentenceTransformer call amortizes well over a long file.

### Retrieval

The query path is:

1. Embed the query (with the BGE instruction prefix), L2-normalize.
2. `SELECT ... WHERE embedding MATCH ? AND k = ?` against `vec_chunks` — sqlite-vec returns the top-k nearest rowids and their L2 distances.
3. Join back to `chunks` for `file_path`, `heading_path`, and `text`.
4. Convert L2 distance to cosine similarity for display. Since the vectors are unit-normalized, `||a−b||² = 2 − 2·cos(a,b)`, so `cos = 1 − distance²/2`. Ranking is unaffected (L2 is monotonic in cosine for unit vectors); the conversion only makes the printed number interpretable as a similarity.

### Incremental indexing

The whole indexer is idempotent and incremental:

- Unchanged files: hash matches → skip entirely (no read, no embed).
- Changed files: old chunks + vectors are dropped (`drop_file`) and re-inserted.
- Deleted files: set-difference between `files` table and on-disk listing, then `drop_file`.
- Interruption-safe: commits every 25 files, and the next run re-embeds anything that didn't make it in because the hash row won't have been written.

`--rebuild` is the nuclear option: deletes the DB file and starts over.

## Things to know

- **Schema is dim-locked to the model.** `vec_chunks` is declared `float[384]` at create time. If you swap `--model` for one with a different embedding dimension (e.g. `bge-base-en-v1.5` at 768-dim), you must also pass `--rebuild` — otherwise inserts will fail against the existing schema. The script does not auto-detect this.
- **Cold start per query is ~1–2 s.** Each `rag_query.py` invocation reloads the embedding model. That's the price of "no services". If you query interactively a lot, the natural next step is a tiny REPL that keeps the model in memory; that crosses the "no services" line but is a 30-line change.
- **Score is cosine similarity, displayed as `cos=...`.** Values above ~0.7 usually indicate a strong match for BGE; 0.5–0.7 is loosely related; below 0.5 is often noise. The k-nearest result set always returns *something*, even for nonsense queries, so use the score as a sanity gate.
- **Pure semantic, no keyword fallback.** For queries dominated by exact tokens (ROS topic names, CLI flags, model numbers), BGE alone can under-recall. Adding BM25 over `chunks.text` and fusing with Reciprocal Rank Fusion is the obvious upgrade — both `rank_bm25` and SQLite's built-in FTS5 would fit cleanly into the same DB.
- **`enable_load_extension` requirement.** The Python interpreter must be built with loadable-SQLite-extension support. Stock CPython on Windows and most Linux distros has it; some hardened or minimal builds (e.g. older system Python on macOS) don't, and you'll see a clear error at index time.
- **Embedding model is English-only.** If you index non-English markdown, swap to `BAAI/bge-m3` (multilingual, 1024-dim) and `--rebuild`.

## File layout

```
sqlite-rag/
├── README.md             # this file
├── rag_index.py          # build / refresh the index
├── rag_query.py          # query the index
├── rag_requirements.txt  # sentence-transformers, sqlite-vec, numpy
└── rag_index.db          # generated; gitignore this
```
