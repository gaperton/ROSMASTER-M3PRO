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

For the current corpus (~250 markdown files, ~2k chunks) **either implementation works**; the sqlite-vec version is lighter to install and gives you per-channel scores out of the box, the LanceDB version is dramatically shorter to write and has more headroom for growth. The interesting moves are:

- If we only ever serve *this* corpus: keep `sqlite-rag`. Lighter deps, single portable `.db` file, richer score display.
- If the corpus grows past ~50k chunks, or we want polyglot readers (Rust/JS), dataset versioning, or pluggable rerankers (Cohere, cross-encoder): switch to `lance-db-rag`.

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

| | sqlite-rag (current) | lance-db-rag (this design) |
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
| **Dependencies** | `sentence-transformers`, `sqlite-vec`, `numpy` | adds `lancedb` + `pyarrow` (~50 MB) + Tantivy bindings |
| **Install pain on Windows** | None observed | Occasional pyarrow wheel mismatches on bleeding-edge Python |
| **Cold-start per query** | ~1–2 s (model load) | Same (model load dominates; LanceDB connect is cheap) |
| **Per-channel score display** | Easy — we hold both `cos` and `bm25` ourselves | Harder — LanceDB exposes a single `_relevance_score`; per-channel scores require dropping below the high-level API |
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

## What surfaced during implementation

Things that turned out non-obvious once code went on the page:

- **The embedding function must be importable in both processes.** LanceDB persists *the registered name* of the embedding function in the table metadata, not the function itself. When `rag_query.py` opens the table, LanceDB looks up `"bge-small-en-v1.5"` in the registry — which is only populated if the `@register` decorator has run. That's why `bge.py` is its own module and both scripts import it (the import in `rag_query.py` is unused for symbols and would tempt a linter to drop it; it's there for the registration side effect).
- **`delete` takes a raw SQL predicate string.** LanceDB's `table.delete()` is not parameterized — you build a predicate like `file_path = 'foo.md'` as a string. Single quotes in file paths would break it, so `rag_index.py` has a small `sql_escape` helper. Not a problem for this corpus but a real footgun for general use.
- **Per-channel scores in hybrid mode are messier than I claimed in the design doc.** LanceDB's hybrid path returns `_relevance_score` (the RRF output) and *may* return `_distance` / `_score` from the underlying channels, depending on version and reranker. The query script surfaces whichever the engine actually returned, with `—` for missing. By contrast, sqlite-rag always shows `cos=…  bm25=…` because we hold both ourselves.
- **The FTS index has to be (re)built explicitly.** Unlike the sqlite-rag triggers, LanceDB's FTS index doesn't auto-update when rows are added. `rag_index.py` calls `create_fts_index("text", replace=True)` whenever new chunks were added. For 2k chunks this is fast; at large scale you'd want incremental FTS (`use_tantivy=True` plus periodic rebuilds).
- **The "files" table is a workaround.** LanceDB doesn't have an obvious primary-key constraint or upsert; the cleanest way to track per-file hashes is a second table with delete-then-insert. `table.merge_insert(...)` is the modern upsert API if you want to consolidate.

## Recommendation

Run both against the same queries before committing to one. The corpus is small enough that the engine choice is reversible; the dependency footprint and "single file vs directory" tradeoff is the most user-visible difference. If hybrid retrieval quality is roughly equivalent (likely — both fuse with RRF, both use BGE), the deciding factor is what matters to *us*: portability of the index, score introspectability, install weight, and how much we expect the corpus to grow.

The natural follow-up if we pick LanceDB as the primary: move `split_by_headings` / `chunk_section` to a shared module, drop the duplication, and demote `sqlite-rag` to a "minimal reference" demo (or delete it).
