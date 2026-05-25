# sqlite-rag

Local, file-based RAG retrieval over the repo's markdown course material. No background services, no network calls after the first model download, no external vector DB. The whole index is a single SQLite file you can copy, gitignore, or delete.

Default retrieval is **hybrid**: semantic (sentence-transformer + sqlite-vec) and keyword (SQLite FTS5 / BM25) are run in parallel and fused with Reciprocal Rank Fusion.

## When to use it

You have a folder of markdown and you want to ask natural-language questions like *"how do I unlock the controller buttons"* or *"moveit2 pick and place"* and get back the most relevant chunks with file paths and heading breadcrumbs. Retrieval only — no LLM answer synthesis (you read the chunks yourself, or pipe them somewhere else).

## How to use

```powershell
pip install -r sqlite-rag/rag_requirements.txt

# (Re)build the index. First run downloads the ~130 MB BGE model into your
# HuggingFace cache; subsequent runs are incremental (sha256 per file).
python sqlite-rag/rag_index.py

# Ask a question (default mode is hybrid).
python sqlite-rag/rag_query.py "how do I unlock the controller buttons"
python sqlite-rag/rag_query.py "moveit2 pick and place" -k 5
python sqlite-rag/rag_query.py "lidar setup" --full

# Pick a single channel when you want to.
python sqlite-rag/rag_query.py "ros2 topic list"   --mode keyword    # FTS5 / BM25 only
python sqlite-rag/rag_query.py "what is a quaternion" --mode semantic
```

Defaults resolve relative to the script location, so the commands work from any cwd:
- `--docs` → `<repo>/markdown`
- `--db`   → `<repo>/sqlite-rag/rag_index.db`
- `--model` → `BAAI/bge-small-en-v1.5` (384-dim, English)

## Design

### Two scripts, one file

The system splits cleanly along read/write lines:

- [rag_index.py](rag_index.py) — write side. Walks the docs folder, chunks, embeds, writes to SQLite.
- [rag_query.py](rag_query.py) — read side. Embeds the query, runs semantic + keyword search, fuses with RRF, prints results.

Everything they share lives in **one SQLite file** (`rag_index.db`). That file is the entire index: text, metadata, and vectors. It's portable, diffable-ish, and easy to back up or throw away. No daemon, no lock files, no migration system.

### Storage layout

The index uses four tables in a single SQLite database. The [`sqlite-vec`](https://github.com/asg017/sqlite-vec) extension is loaded at runtime for the vector virtual table; FTS5 ships with stock SQLite and needs no extension:

```
files(path PRIMARY KEY, hash)                       -- one row per markdown file, sha256 of contents
chunks(id PK, file_path, heading_path, ord, text)   -- one row per chunk, with H1>H2>H3 breadcrumb
vec_chunks(rowid, embedding float[384])             -- vec0 virtual table; rowid matches chunks.id
fts_chunks(text)                                    -- FTS5 (porter+unicode61); external content over chunks.text
```

`chunks.id`, `vec_chunks.rowid`, and `fts_chunks.rowid` are kept in 1:1 correspondence so a single id identifies the same chunk in all three. `fts_chunks` is an *external content* FTS5 table (`content='chunks'`, `content_rowid='id'`), so the chunk text is stored once in `chunks` and indexed by reference. AFTER INSERT / DELETE / UPDATE triggers on `chunks` keep the FTS index in sync — the indexer never touches `fts_chunks` directly, which makes the existing `drop_file` and chunk-insert paths work unchanged.

`files.hash` is what makes indexing incremental: on each run we compare the on-disk sha256 to the stored hash and skip files that haven't changed. Deleted files are detected by set-difference (`in_db - on_disk`) and pruned. If you open an older DB that pre-dates FTS, `open_db` backfills `fts_chunks` from `chunks` on first connect.

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

### Retrieval — hybrid by default

A query runs both channels and fuses them. Each channel pulls a *pool* of candidates (default `max(top_k * 4, 30)`, override with `--pool`), then RRF picks the top-k.

**Semantic channel (`vec_chunks`)**

1. Embed the query (with the BGE instruction prefix), L2-normalize.
2. `SELECT rowid, distance FROM vec_chunks WHERE embedding MATCH ? AND k = ?` — sqlite-vec returns the nearest rowids and their L2 distances.
3. Convert L2 distance to cosine similarity for display. Since the vectors are unit-normalized, `||a−b||² = 2 − 2·cos(a,b)`, so `cos = 1 − distance²/2`. Ranking is unaffected (L2 is monotonic in cosine for unit vectors); the conversion only makes the printed number interpretable as a similarity.

**Keyword channel (`fts_chunks`)**

1. The natural-language query is tokenized with `\w+`, each token is double-quoted (neutralizing FTS5 operator characters), and tokens are joined with `OR`. Example: `"moveit2 pick and place"` → `"moveit2" OR "pick" OR "and" OR "place"`. The OR-join produces ranked recall instead of forcing every token to appear.
2. `SELECT rowid, bm25(fts_chunks) FROM fts_chunks WHERE fts_chunks MATCH ? ORDER BY bm25(fts_chunks) LIMIT ?` — FTS5's BM25 ranker returns negated scores (more-negative = better), so the display layer flips the sign so higher = better.

**Fusion (Reciprocal Rank Fusion)**

Each channel produces an ordered list of chunk ids. RRF assigns each chunk a fused score:

```
score(doc) = sum over channels of 1 / (k + rank_in_that_channel)     where k = 60
```

Chunks that don't appear in a channel contribute nothing from that channel — so a doc found by both will outrank one found by only one, even if the lone-channel rank is slightly higher. RRF doesn't need score calibration between channels (it only uses ranks), which is why it's the dominant choice for cheap hybrid retrieval.

Results are sorted by fused score descending; for each one the printer also shows the per-channel scores (`cos=…`, `bm25=…`, with `—` if a channel didn't surface that chunk) so you can see *why* something ranked.

**Single-channel modes**

`--mode semantic` or `--mode keyword` skips fusion and ranks by the channel's native score. Useful when you want to A/B compare, or when you know your query is purely semantic (e.g. *"what is a quaternion"*) or purely token-driven (e.g. *"ros2 topic list"*).

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
- **Reading the scores.** In hybrid mode the primary number is the RRF score (small, typically ~0.01–0.05; only meaningful relative to other RRF scores in the same result set). The `cos=…` and `bm25=…` extras tell you which channel found the chunk and how strongly. In single-channel mode the primary is the channel's native score: cosine (higher = better, >0.7 is strong for BGE) or BM25 (sign-flipped so higher = better, magnitudes depend on corpus statistics). A `—` means the chunk wasn't in that channel's top pool — bump `--pool` if you want a wider net before fusion.
- **FTS5 tokenizer is `porter unicode61`.** That means English stemming (`controllers` matches `controller`) and Unicode-aware case folding, but no stop-word removal — short function words like *and*, *the*, *is* still match. If you index non-English markdown, swap to the `unicode61` tokenizer alone (no Porter) or `trigram` for CJK content, and `--rebuild`.
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
