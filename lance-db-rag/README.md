# lance-db-rag

A LanceDB-backed parallel implementation of [`../sqlite-rag/`](../sqlite-rag/), built for head-to-head comparison. Same chunking, same embedding model (BGE-small-en-v1.5), same `--mode {hybrid,semantic,keyword}` CLI surface — different storage engine and a much shorter pipeline thanks to LanceDB's embedding registry and built-in hybrid search.

## How to use

```powershell
pip install -r lance-db-rag/rag_requirements.txt

# (Re)build the index. First run downloads the ~130 MB BGE model into your
# HuggingFace cache; subsequent runs are incremental (sha256 per file).
python lance-db-rag/rag_index.py

# Ask a question (default mode is hybrid).
python lance-db-rag/rag_query.py "how do I unlock the controller buttons"
python lance-db-rag/rag_query.py "moveit2 pick and place" -k 5
python lance-db-rag/rag_query.py "lidar setup" --full

# Single-channel modes.
python lance-db-rag/rag_query.py "ros2 topic list"     --mode keyword
python lance-db-rag/rag_query.py "what is a quaternion" --mode semantic
```

Defaults resolve relative to the script location, so commands work from any cwd:
- `--docs` → `<repo>/markdown`
- `--db`   → `<repo>/lance-db-rag/index.lance` (a directory, not a single file)

## TL;DR comparison

After two rounds of testing and tuning, the two engines are **functionally equivalent on retrieval quality for this corpus**. Both produce the same top-1 hit on every labeled case and converge to nearly identical results across the 30 unlabeled noob questions in `../tests/noob_questions.txt`.

Earlier versions of this README said "sqlite-rag is the better fit" because LanceDB's default hybrid path under-performed on diffuse queries. That gap turned out to be a *configuration parity* issue, not an engine-quality issue:

1. Lance was receiving the raw natural-language string for FTS; sqlite was stop-word-filtering + OR-joining tokens before BM25 ranking.
2. Lance's built-in hybrid used a smaller candidate pool than sqlite's `max(top_k*4, 30)` before RRF fusion.

[`rag_query.py`](rag_query.py) now applies both fixes manually (see `run_search` / `to_lance_fts_query`) and Lance lands at parity. See [`../tests/README.md`](../tests/README.md#findings-corpus-247-docs-2198-chunks) for the side-by-side numbers.

The pragmatic decision now is *operational*, not quality-based:

- **sqlite-rag wins on**: ~10 MB install vs ~82 MB; single portable `.db` file vs directory tree; ~2× faster queries (~37 ms vs ~80 ms); per-channel score transparency in the CLI.
- **lance-db-rag wins on**: future growth headroom (HNSW/IVF index path) when corpus passes ~50k chunks; polyglot readers (Rust/JS) over the same dataset; first-class dataset versioning / time-travel; pluggable rerankers (the `--rerank` flag — see "Reranker exploration" below).

## What LanceDB changes

LanceDB is an embedded, file-based vector DB built on the Arrow-native [Lance](https://github.com/lancedb/lance) columnar format. Same "no service" property as sqlite-vec, different design center: vectors first, columnar storage, designed for ML pipelines rather than as a SQL extension.

Three pieces of LanceDB are interesting for us:

1. **Embedding registry.** Declare an embedding function once, attach it to a column, and inserts/queries auto-embed. The `serialize_f32`, manual `model.encode`, and "remember to L2-normalize" steps disappear from the call site.
2. **Built-in FTS.** `table.create_fts_index("text")` builds a Tantivy index colocated with the table. No separate triggers, no manual sync.
3. **Hybrid search + rerankers.** `table.search(text, query_type="hybrid").rerank(RRFReranker())` does both channels and fuses in one call. Switching to a cross-encoder or Cohere reranker is a one-line change to `.rerank(...)`.

## Storage model

A LanceDB "database" is a directory; each table is a subdirectory of `.lance` data files plus a manifest with version history. Two tables would cover us:

```
lance-db-rag/index.lance/
├── chunks.lance/        # id, file_path, heading_path, ord, text, vector(384)
└── files.lance/         # path, hash
```

We lose the "one portable file" property of sqlite-vec, but versioning comes free: every `add` / `delete` produces a new manifest version, and you can `table.checkout(version)` to roll back an indexing change.

## Code sketch — indexer

The reusable chunking code (`split_by_headings`, `chunk_section`) ports as-is, intentionally duplicated from `sqlite-rag/rag_index.py` so the two implementations stay independent for the comparison. Everything around chunking collapses:

```python
# lance-db-rag/rag_index.py  (sketch)
import lancedb
from lancedb.embeddings import EmbeddingFunction, register
from lancedb.pydantic import LanceModel, Vector
from sentence_transformers import SentenceTransformer

@register("bge-small-en-v1.5")
class BGE(EmbeddingFunction):
    """Custom EF so query and source use different inputs (BGE asymmetric retrieval)."""
    name: str = "BAAI/bge-small-en-v1.5"
    _model: object = None

    def ndims(self):
        return 384

    def _m(self):
        if self._model is None:
            self._model = SentenceTransformer(self.name)
        return self._model

    def compute_source_embeddings(self, texts, *a, **kw):
        return self._m().encode(list(texts), normalize_embeddings=True).tolist()

    def compute_query_embeddings(self, query, *a, **kw):
        q = [query] if isinstance(query, str) else list(query)
        prefixed = ["Represent this sentence for searching relevant passages: " + s for s in q]
        return self._m().encode(prefixed, normalize_embeddings=True).tolist()

bge = BGE()

class Chunk(LanceModel):
    id: int
    file_path: str
    heading_path: str
    ord: int
    text: str = bge.SourceField()       # tells LanceDB this column feeds the embedding
    vector: Vector(384) = bge.VectorField()

class FileHash(LanceModel):
    path: str
    hash: str

db = lancedb.connect("lance-db-rag/index.lance")
chunks_t = db.create_table("chunks", schema=Chunk, exist_ok=True)
files_t  = db.create_table("files",  schema=FileHash, exist_ok=True)

# ... walk docs, hash, chunk, build per-file rows ...
chunks_t.delete(f"file_path = '{rel}'")     # remove stale chunks for changed/deleted files
chunks_t.add(new_rows)                      # auto-embeds text -> vector via BGE

# Idempotent FTS index over the text column.
chunks_t.create_fts_index("text", replace=False)
```

What we no longer write: `serialize_f32`, the chunks/vec_chunks join, the FTS triggers, the manual backfill. About 30–40 fewer lines.

## Code sketch — query

```python
# lance-db-rag/rag_query.py  (sketch)
import lancedb
from lancedb.rerankers import RRFReranker

db = lancedb.connect("lance-db-rag/index.lance")
t = db.open_table("chunks")

if args.mode == "hybrid":
    res = (t.search(args.query, query_type="hybrid")
            .rerank(RRFReranker(K=60))
            .limit(args.top_k)
            .to_list())
elif args.mode == "semantic":
    res = t.search(args.query, query_type="vector").limit(args.top_k).to_list()
else:
    res = t.search(args.query, query_type="fts").limit(args.top_k).to_list()

for i, r in enumerate(res, 1):
    score = r.get('_relevance_score', r.get('_distance'))
    print(f"[{i}] {score:.4f}  {r['file_path']}  ::  {r['heading_path']}")
    print("    " + r['text'][:400])
```

The whole `to_fts5_query` / `rrf_fuse` / `search_semantic` / `search_keyword` apparatus from the sqlite-vec version compresses into the `.search().rerank().limit()` chain.

## Head-to-head

| | sqlite-rag | lance-db-rag |
|---|---|---|
| **Storage** | One `.db` file | Directory tree of `.lance` files |
| **Vector index** | Linear scan (sqlite-vec) | Linear scan by default; HNSW/IVF_PQ available via `create_index` |
| **Keyword index** | SQLite FTS5 (porter+unicode61) | Tantivy (richer tokenizer set, better multilingual story) |
| **Hybrid + RRF** | ~40 LOC we wrote | Originally `query_type="hybrid"` + `RRFReranker()` — but we ended up reimplementing it in `run_search` for parity (see "What surfaced" below). Net LOC similar to sqlite. |
| **Embedding pipeline** | Manual `model.encode` + serialize | Embedding registry; declared on the schema, auto-runs |
| **Asymmetric query prefix (BGE)** | Hand-coded in the query script | Hand-coded inside the custom `EmbeddingFunction` (same idea, different home) |
| **Reranker swap** | Rewrite the fusion code | `--rerank` flag; opt-in cross-encoder via `sentence_transformers.CrossEncoder` (we bypass `lancedb.rerankers`). See "Reranker exploration" below. |
| **Schema migrations** | Manual `ALTER TABLE` | Dataset versions; can checkout / restore prior versions |
| **Polyglot reads** | Python only (or DIY SQLite reader) | Lance format readable from Rust, JS, DuckDB, etc. |
| **Dependencies (measured)** | `sentence-transformers`, `sqlite-vec`, `numpy` — ~10 MB of new wheels | adds `lancedb` 51 MB + `pyarrow` 27 MB + `tantivy` 4 MB |
| **Install pain on Windows** | None observed | Wheels available for Python 3.12; older Pythons may need fallback |
| **Cold-start per query** | ~1–2 s (model load) | Same (model load dominates; LanceDB connect is cheap) |
| **Per-channel score display** | Easy — we hold both `cos` and `bm25` ourselves | Hard — confirmed in testing: hybrid mode returns only `_relevance_score`; per-channel scores require running channels separately |
| **Snippet centering + highlights** | Built in via FTS5 `snippet()`, Porter-stemmed | Client-side helper in `rag_query.py` (~30 LOC), exact-match only |
| **Good fit when** | Small/medium corpus, want one portable file, want SQL alongside vectors | Large corpus, want versioning, want polyglot readers, want pluggable rerankers |

## What we'd lose by switching to Lance

- **Single-file portability.** The single `rag_index.db` is genuinely nice — you can email it, drop it on a USB stick, gitignore one path. A Lance directory is fine but less satisfying.
- **Direct SQL.** With sqlite-vec we can `SELECT ... WHERE heading_path LIKE '%MoveIt2%'` from any SQLite client. LanceDB has SQL via DuckDB but it's a separate path.
- **Featherweight install.** ~10 MB of new wheels for sqlite-rag vs ~82 MB for lance-db-rag. pyarrow has historically been the most common "pip install failed on Windows" issue in this ecosystem.
- **~2× faster queries** (~37 ms vs ~80 ms median, hybrid mode).

## What we'd gain by switching to Lance

- **A real ANN index path** when we need it. `create_index(metric="cosine")` builds IVF_PQ; queries unchanged. Matters past ~50k chunks.
- **Pluggable rerankers** via the `--rerank` flag — opt-in cross-encoder reranking is a config swap, not a code-write. (See "Reranker exploration" — neither reranker we tried helped on this corpus, but the plumbing is there for a domain-tuned reranker.)
- **Dataset versioning for free.** Re-index introduces a bad chunking change? `table.restore(version=N)` rolls back without re-embedding.
- **Cross-language reads.** Same dataset usable from a Rust ingest script or a JS web tool if that ever matters.

The "we'd save boilerplate" pitch from the original design doc didn't hold up: LanceDB's built-in hybrid path needed bypassing for configuration-parity reasons (see "Reranker exploration"), and the manual orchestration we wrote is comparable in size to sqlite's hybrid code. Net code volume is roughly equal.
- **Versioning for free.** Re-index introduces a bad chunking change? `table.restore(version=N)` rolls back without re-embedding.
- **Cross-language reads.** Same dataset usable from a Rust ingest script or a JS web tool, if that ever matters.

## What surfaced during implementation and testing

Things that were non-obvious at design time and only showed up once code ran against the real corpus. Most of these cost ~10 minutes of debugging each on the way to a working build.

- **The embedding function must be importable in both processes.** LanceDB persists *the registered name* of the embedding function in the table metadata, not the function itself. When `rag_query.py` opens the table, LanceDB looks up `"bge-small-en-v1.5"` in the registry — which is only populated if the `@register` decorator has run. That's why `bge.py` is its own module and both scripts import it (the import in `rag_query.py` is unused for symbols and would tempt a linter to drop it; it's there for the registration side effect).
- **`BGE.create()`, not `BGE()`.** LanceDB ≥0.13 requires embedding-function instances to be constructed via the `EmbeddingFunction.create()` classmethod — direct constructor calls produce `ValueError: EmbeddingFunction was not created with EmbeddingFunction.create()` at table-creation time, when LanceDB tries to serialize the function into table metadata via `safe_model_dump()`.
- **Embedding inputs arrive as pyarrow `StringScalar`, not `str`.** When LanceDB auto-embeds rows on insert, it passes a column slice straight into `compute_source_embeddings`, and the elements are `pyarrow.StringScalar` objects. `sentence_transformers.encode` rejects them with `Unsupported input type: StringScalar`. The `_as_str_list` helper in `bge.py` coerces anything LanceDB might hand us into a plain `list[str]`.
- **Embedding-function errors trigger an exponential-backoff retry loop.** A bug in `BGE` doesn't surface as a fast failure — LanceDB silently retries the embed call seven times with delays of ~1s, 4s, 12s, 40s, 117s, 253s, 985s (totaling ~25 min before the final error). Watch the indexer's log on the first run; kill it if you see `Retrying in N seconds`.
- **`delete` takes a raw SQL predicate string.** LanceDB's `table.delete()` is not parameterized — you build a predicate like `file_path = 'foo.md'` as a string. Single quotes in file paths would break it, so `rag_index.py` has a small `sql_escape` helper. Not a problem for this corpus but a real footgun for general use.
- **`.to_pandas()` pulls pandas (not in `rag_requirements.txt`).** First written that way in `load_file_hashes`; replaced with `.to_arrow().column(name).to_pylist()` to keep the install lean. Worth knowing because most LanceDB examples reach for `.to_pandas()` and silently add the dependency.
- **Per-channel scores in hybrid mode are not exposed.** Confirmed by testing: `table.search(..., query_type="hybrid").rerank(RRFReranker()).to_list()` returns `_relevance_score` (the RRF output) but no `_distance` / `_score` from the underlying channels in this version. The display shows `rrf=N.NNNN` only. By contrast, sqlite-rag always shows `cos=…  bm25=…` because we hold both scores ourselves. Getting them back from LanceDB means running the channels separately, which gives up the engine's built-in fusion path.
- **Snippet centering is client-side and unstemmed.** Unlike SQLite's FTS5 `snippet()` function (which stems via Porter), Tantivy's snippet API isn't exposed by LanceDB at this version. `rag_query.py` has its own `centered_snippet` helper that finds the first content-token match in the chunk text and slices around it with `[[…]]` markers. It uses exact word-boundary matching, so `quaternions` won't highlight when the query was `quaternion` — that gap is the limit of doing it without a stemmer.
- **The FTS index has to be (re)built explicitly.** Unlike the sqlite-rag triggers, LanceDB's FTS index doesn't auto-update when rows are added. `rag_index.py` calls `create_fts_index("text", replace=True)` whenever new chunks were added. For 2k chunks this is fast; at large scale you'd want incremental FTS or a less frequent rebuild cadence.
- **The "files" table is a workaround.** LanceDB doesn't have an obvious primary-key constraint or upsert; the cleanest way to track per-file hashes is a second table with delete-then-insert. `table.merge_insert(...)` is the modern upsert API if you want to consolidate.

## Validated on this corpus

End-to-end tested against the repo's `markdown/` folder on Windows / Python 3.12 / LanceDB 0.30.2:

- **247 markdown files → 2198 chunks**, directory size **~12 MB** (vs sqlite-rag's 8 MB single file).
- Cold index build: a few minutes on CPU, same order as sqlite-rag. The 25-min hidden-retry trap (above) added significant wasted time during initial debugging.
- Install footprint: ~82 MB of wheels (lancedb 51 MB + pyarrow 27 MB + tantivy 4 MB) plus sentence-transformers' stack.
- Query latency: ~1–2 s end-to-end, model-load-bound (same as sqlite-rag).
- Retrieval quality: at parity with sqlite-rag on every comparison query we ran (labeled cases + 30 unlabeled noob questions in `../tests/noob_questions.txt`). Same top-1 hit; lower-rank order matches to within RRF tie-breaking noise.

## Reranker exploration

`run_search` accepts a `rerank` flag and `rag_query.py` exposes it as `--rerank`. **Default is off** after side-by-side testing showed neither cross-encoder we tried reliably improves retrieval on this corpus.

What we tried and what happened:

| Reranker | Labeled chunk MRR | Open noob queries | Latency |
|---|---|---|---|
| None (RRF only) | 0.529 | matches sqlite | 80 ms |
| `cross-encoder/ms-marco-MiniLM-L-6-v2`, input `(query, text)` | 0.558 (+5%) | regressed on diffuse queries | 157 ms |
| same model, input `(query, heading_path + text)` | 0.558 | regressed differently | 157 ms |
| `BAAI/bge-reranker-base`, input `(query, heading + text)` | 0.533 | fixed 3 hard queries, broke 5 easy ones | 440 ms |

Why the rerankers underperformed: ms-marco-MiniLM is trained on web QA passages and over-fits to surface keyword density in our markdown chunks (especially short header-rich chunks). BGE-reranker is better-matched to passage retrieval and *did* fix the diffuse queries (Q4 "map a room", Q6 "Jetson vs Pi", Q9 "install ROS2 on laptop") that originally exposed Lance's weaknesses — but it introduced new failures on queries where RRF was already correctly anchoring the right doc (the cross-encoder's re-scoring became noise).

Hypothesis: **rerankers help most when retrieval is *ambiguous* (many plausible docs, the right one buried by noise). For clean queries where one doc obviously answers, re-scoring adds entropy without value.** This corpus is a mix, so any reranker is a net wash. A specialized fine-tuned reranker on a labeled domain dataset would likely do better, but that's a bigger investment.

To experiment with reranking yourself:

```powershell
# BGE-reranker, on the diffuse queries it actually helps
python lance-db-rag/rag_query.py "how do I map a room" --rerank

# Disable for the queries where it hurts
python lance-db-rag/rag_query.py "what's the default WiFi password"  # rerank off by default
```

The model downloads (~280 MB) into your HuggingFace cache on first use.

## Recommendation

**Either engine is a defensible choice for this corpus** — the original "sqlite is clearly better" verdict reversed once we matched Lance's hybrid configuration to sqlite's. The remaining differences are operational, not quality:

- Pick **sqlite-rag** if you value: lighter install, single portable file, faster queries, per-channel score transparency, less code complexity.
- Pick **lance-db-rag** if you value or anticipate: corpus past ~50k chunks (HNSW), polyglot readers, dataset versioning, an experimental playground for rerankers/cross-encoders.

The natural follow-up if you pick one as the primary: move `split_by_headings` / `chunk_section` (currently duplicated between the two `rag_index.py` files) to a shared module, drop the duplication, and demote the other to a "minimal reference" demo.
