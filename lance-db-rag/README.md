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

For the current corpus (~250 markdown files, ~2k chunks) **sqlite-rag is the better fit** — confirmed by end-to-end testing on both engines (see [Validated on this corpus](#validated-on-this-corpus) below). Same top-1 hit on every query we ran, but sqlite-rag installs in ~10 MB vs ~82 MB, exposes per-channel scores next to every result, and produces a single portable `.db` file instead of a directory tree.

The LanceDB version stays in the repo as a working comparison. It becomes the better choice when:

- corpus grows past ~50k chunks (linear scan vs the HNSW/IVF index path LanceDB enables),
- you want polyglot readers (Rust/JS) over the same dataset,
- you want first-class dataset versioning / time-travel,
- you want to swap rerankers (Cohere, cross-encoder) without writing the plumbing.

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
| **Hybrid + RRF** | ~40 LOC we wrote | `query_type="hybrid"` + `RRFReranker()` |
| **Embedding pipeline** | Manual `model.encode` + serialize | Embedding registry; declared on the schema, auto-runs |
| **Asymmetric query prefix (BGE)** | Hand-coded in the query script | Hand-coded inside the custom `EmbeddingFunction` (same idea, different home) |
| **Reranker swap** | Rewrite the fusion code | One-line: `.rerank(CrossEncoderReranker(...))` |
| **Schema migrations** | Manual `ALTER TABLE` | Dataset versions; can checkout / restore prior versions |
| **Polyglot reads** | Python only (or DIY SQLite reader) | Lance format readable from Rust, JS, DuckDB, etc. |
| **Dependencies (measured)** | `sentence-transformers`, `sqlite-vec`, `numpy` — ~10 MB of new wheels | adds `lancedb` 51 MB + `pyarrow` 27 MB + `tantivy` 4 MB |
| **Install pain on Windows** | None observed | Wheels available for Python 3.12; older Pythons may need fallback |
| **Cold-start per query** | ~1–2 s (model load) | Same (model load dominates; LanceDB connect is cheap) |
| **Per-channel score display** | Easy — we hold both `cos` and `bm25` ourselves | Hard — confirmed in testing: hybrid mode returns only `_relevance_score`; per-channel scores require running channels separately |
| **Snippet centering + highlights** | Built in via FTS5 `snippet()`, Porter-stemmed | Client-side helper in `rag_query.py` (~30 LOC), exact-match only |
| **Good fit when** | Small/medium corpus, want one portable file, want SQL alongside vectors | Large corpus, want versioning, want polyglot readers, want pluggable rerankers |

## What we'd lose by switching

- **Single-file portability.** The single `rag_index.db` is genuinely nice — you can email it, drop it on a USB stick, gitignore one path. A Lance directory is fine but less satisfying.
- **Direct SQL.** With sqlite-vec we can `SELECT ... WHERE heading_path LIKE '%MoveIt2%'` from any SQLite client. LanceDB has SQL via DuckDB but it's a separate path.
- **Per-channel score readability.** The current display (`rrf=…  cos=…  bm25=…`) is genuinely useful for debugging "why did this rank." LanceDB's `_relevance_score` is a single fused number; getting the components back means running the channels separately, which gives up the engine's built-in fusion path.
- **Featherweight install.** pyarrow alone is ~50 MB and historically the most common source of "pip install failed on Windows" reports in this ecosystem.

## What we'd gain by switching

- **~Half the boilerplate**: no `serialize_f32`, no FTS triggers, no manual fusion. Less surface area to maintain.
- **A real ANN index path** when we need it. `create_index(metric="cosine")` builds IVF_PQ; queries unchanged.
- **Reranker plug points**: swap RRF for a cross-encoder, Cohere, or hand-written reranker by changing one line in the query script.
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
- Retrieval quality: top-1 hit matches sqlite-rag on every comparison query we ran. Lower-ranked hits diverge slightly because LanceDB's hybrid ranking uses different intermediate scores; both engines find the same "right" documents, sometimes in different orders.

## Recommendation

For *this* corpus and the questions we're asking of it, **sqlite-rag is the better choice** — confirmed by side-by-side testing. The wins:

- **Score transparency**: per-channel `cos=…  bm25=…` next to every result makes ranking debuggable. With LanceDB you see only the fused RRF score.
- **Lighter install** (~10 MB vs ~82 MB).
- **Single portable `.db` file** vs a directory tree.
- **Stemmed snippet highlighting** for free via FTS5's `snippet()`.

LanceDB earns its weight when the corpus or operational requirements grow: ≥50k chunks (linear scan starts to feel slow → opt into HNSW/IVF), polyglot readers, dataset versioning, pluggable rerankers. None of those apply here.

The natural follow-up if we ever pick LanceDB as the primary: move `split_by_headings` / `chunk_section` (currently duplicated between the two `rag_index.py` files) to a shared module, drop the duplication, and demote `sqlite-rag` to a "minimal reference" demo.
