"""Build a local RAG index over a folder of markdown files.

Stores everything in a single SQLite file (sqlite-vec virtual table for
embeddings + regular tables for chunk text and file hashes). Incremental:
re-embeds only files whose sha256 changed since the last run.

Usage (from repo root or from inside sqlite-rag/):
    python sqlite-rag/rag_index.py            # indexes ../markdown into sqlite-rag/rag_index.db
    python rag_index.py --docs other_dir --db other.db
    python rag_index.py --rebuild             # wipe and re-embed everything
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sqlite3
import struct
import sys
from pathlib import Path

import numpy as np
import sqlite_vec
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"
CHUNK_TARGET_CHARS = 1800
CHUNK_OVERLAP_CHARS = 300

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
PAGE_SPAN_RE = re.compile(r"""<span\s+[^>]*id=["']page-[^"']+["'][^>]*>\s*</span>""", re.IGNORECASE)
PAGE_ANCHOR_LINK_RE = re.compile(r"\[([^\]]+)\]\(#page-[^)]+\)")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")
SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9`*_\"'])")

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DOCS = SCRIPT_DIR.parent / "markdown"
DEFAULT_DB = SCRIPT_DIR / "rag_index.db"

# Embed dim is baked into the vec0 virtual table schema, so swapping models
# requires a fresh DB file at a different path. Keep the lookup tight to the
# bge family we actually use.
MODEL_DIMS = {
    "BAAI/bge-small-en-v1.5": 384,
    "BAAI/bge-large-en-v1.5": 1024,
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def clean_markdown(text: str) -> str:
    """Remove PDF-conversion litter before chunking, embedding, and display."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = PAGE_SPAN_RE.sub("", text)
    text = PAGE_ANCHOR_LINK_RE.sub(r"\1", text)
    return "\n".join(line.rstrip() for line in text.split("\n")).strip()


def split_by_headings(text: str) -> list[tuple[list[str], str]]:
    """Split markdown into (heading_path, body) sections.

    heading_path is the stack of H1..Hn titles leading to that section.
    """
    sections: list[tuple[list[str], str]] = []
    stack: list[str] = []

    matches = list(HEADING_RE.finditer(text))
    if not matches:
        return [([], text)]

    if matches[0].start() > 0:
        sections.append(([], text[: matches[0].start()].strip()))

    for i, m in enumerate(matches):
        level = len(m.group(1))
        title = m.group(2).strip()
        stack = stack[: level - 1]
        while len(stack) < level - 1:
            stack.append("")
        stack.append(title)
        heading_path = [s for s in stack if s]

        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip()
        if body:
            sections.append((heading_path, body))

    return [(h, b) for h, b in sections if b]


def is_fence_start(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith("```") or stripped.startswith("~~~")


def is_table_start(lines: list[str], i: int) -> bool:
    return (
        "|" in lines[i]
        and i + 1 < len(lines)
        and TABLE_SEPARATOR_RE.match(lines[i + 1].strip()) is not None
    )


def section_blocks(body: str) -> list[tuple[str, bool]]:
    """Return (text, atomic) blocks; atomic blocks are never split."""
    blocks: list[tuple[str, bool]] = []
    paragraph: list[str] = []
    lines = body.split("\n")
    i = 0

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(("\n".join(paragraph).strip(), False))
            paragraph = []

    while i < len(lines):
        line = lines[i]
        if is_fence_start(line):
            flush_paragraph()
            fence = [line]
            i += 1
            while i < len(lines):
                fence.append(lines[i])
                if is_fence_start(lines[i]):
                    i += 1
                    break
                i += 1
            blocks.append(("\n".join(fence).strip(), True))
            continue

        if is_table_start(lines, i):
            flush_paragraph()
            table = []
            while i < len(lines) and lines[i].strip() and "|" in lines[i]:
                table.append(lines[i])
                i += 1
            blocks.append(("\n".join(table).strip(), True))
            continue

        if not line.strip():
            flush_paragraph()
        else:
            paragraph.append(line)
        i += 1

    flush_paragraph()
    return [(text, atomic) for text, atomic in blocks if text]


def hard_split_text(text: str, max_chars: int) -> list[str]:
    pieces: list[str] = []
    text = text.strip()
    while len(text) > max_chars:
        cut = max(text.rfind("\n", 0, max_chars + 1), text.rfind(" ", 0, max_chars + 1))
        if cut < max_chars // 2:
            cut = max_chars
        pieces.append(text[:cut].strip())
        text = text[cut:].strip()
    if text:
        pieces.append(text)
    return pieces


def split_prose_block(text: str) -> list[str]:
    """Split oversized prose by sentence first, then by character fallback."""
    if len(text) <= CHUNK_TARGET_CHARS:
        return [text]

    pieces: list[str] = []
    current = ""
    for sentence in SENTENCE_BOUNDARY_RE.split(text):
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(sentence) > CHUNK_TARGET_CHARS:
            if current:
                pieces.append(current)
                current = ""
            pieces.extend(hard_split_text(sentence, CHUNK_TARGET_CHARS))
            continue
        candidate = f"{current} {sentence}".strip() if current else sentence
        if len(candidate) <= CHUNK_TARGET_CHARS:
            current = candidate
        else:
            pieces.append(current)
            current = sentence
    if current:
        pieces.append(current)
    return pieces


def joined_len(parts: list[str]) -> int:
    return len("\n\n".join(parts))


def overlap_tail(parts: list[str]) -> list[str]:
    out: list[str] = []
    for part in reversed(parts):
        candidate = [part, *out]
        if joined_len(candidate) > CHUNK_OVERLAP_CHARS:
            break
        out = candidate
    return out


def legacy_chunk_section(heading: list[str], body: str) -> list[tuple[list[str], str]]:
    """NX8/NX10 baseline chunker: fixed-size sliding window with overlap."""
    if len(body) <= CHUNK_TARGET_CHARS:
        return [(heading, body)]

    chunks: list[tuple[list[str], str]] = []
    step = CHUNK_TARGET_CHARS - CHUNK_OVERLAP_CHARS
    for start in range(0, len(body), step):
        piece = body[start : start + CHUNK_TARGET_CHARS].strip()
        if piece:
            chunks.append((heading, piece))
        if start + CHUNK_TARGET_CHARS >= len(body):
            break
    return chunks


def boundary_chunk_section(heading: list[str], body: str) -> list[tuple[list[str], str]]:
    """Chunk by paragraph/sentence boundaries without splitting fences or tables."""
    units: list[str] = []
    for block, atomic in section_blocks(body):
        units.extend([block] if atomic else split_prose_block(block))

    if not units:
        return []

    chunks: list[tuple[list[str], str]] = []
    current: list[str] = []
    for unit in units:
        if len(unit) > CHUNK_TARGET_CHARS:
            if current:
                chunks.append((heading, "\n\n".join(current)))
                current = []
            chunks.append((heading, unit))
            continue

        if current and joined_len(current + [unit]) > CHUNK_TARGET_CHARS:
            chunks.append((heading, "\n\n".join(current)))
            current = overlap_tail(current)
            if current and joined_len(current + [unit]) > CHUNK_TARGET_CHARS:
                current = []
        current.append(unit)

    if current:
        chunks.append((heading, "\n\n".join(current)))
    return chunks


def chunk_markdown(text: str, chunking: str = "legacy") -> list[tuple[list[str], str]]:
    out: list[tuple[list[str], str]] = []
    source = clean_markdown(text) if chunking == "boundary" else text
    chunker = boundary_chunk_section if chunking == "boundary" else legacy_chunk_section
    for heading, body in split_by_headings(source):
        out.extend(chunker(heading, body))
    return out


def serialize_f32(vec: np.ndarray) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec.astype(np.float32).tolist())


def open_db(db_path: Path, embed_dim: int) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    conn.executescript(
        f"""
        CREATE TABLE IF NOT EXISTS files (
            path TEXT PRIMARY KEY,
            hash TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            heading_path TEXT NOT NULL,
            ord INTEGER NOT NULL,
            text TEXT NOT NULL,
            FOREIGN KEY (file_path) REFERENCES files(path) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_chunks_file ON chunks(file_path);
        CREATE VIRTUAL TABLE IF NOT EXISTS vec_chunks USING vec0(
            embedding float[{embed_dim}]
        );
        -- Two-column FTS5: heading first, body second. Query-time BM25 can
        -- tune the heading column weight without rebuilding the index.
        -- Pre-NX8 single-column DBs use the legacy `fts_chunks(text)`
        -- shape; rag_query.py detects column count and degrades gracefully.
        CREATE VIRTUAL TABLE IF NOT EXISTS fts_chunks USING fts5(
            heading_path,
            text,
            content='chunks',
            content_rowid='id',
            tokenize='porter unicode61'
        );
        CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
            INSERT INTO fts_chunks(rowid, heading_path, text) VALUES (new.id, new.heading_path, new.text);
        END;
        CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
            INSERT INTO fts_chunks(fts_chunks, rowid, heading_path, text) VALUES('delete', old.id, old.heading_path, old.text);
        END;
        CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
            INSERT INTO fts_chunks(fts_chunks, rowid, heading_path, text) VALUES('delete', old.id, old.heading_path, old.text);
            INSERT INTO fts_chunks(rowid, heading_path, text) VALUES (new.id, new.heading_path, new.text);
        END;
        """
    )
    # Backfill FTS for any pre-existing chunks (older DB built before FTS was added).
    fts_count = conn.execute("SELECT COUNT(*) FROM fts_chunks").fetchone()[0]
    chunk_count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    if chunk_count > 0 and fts_count == 0:
        conn.execute(
            "INSERT INTO fts_chunks(rowid, heading_path, text) SELECT id, heading_path, text FROM chunks"
        )
        conn.commit()
    return conn


def drop_file(conn: sqlite3.Connection, file_path: str) -> None:
    rows = conn.execute("SELECT id FROM chunks WHERE file_path = ?", (file_path,)).fetchall()
    for (cid,) in rows:
        conn.execute("DELETE FROM vec_chunks WHERE rowid = ?", (cid,))
    conn.execute("DELETE FROM chunks WHERE file_path = ?", (file_path,))
    conn.execute("DELETE FROM files WHERE path = ?", (file_path,))


def index_file(
    conn: sqlite3.Connection,
    model: SentenceTransformer,
    docs_root: Path,
    file_path: Path,
    chunking: str,
) -> int:
    rel = file_path.relative_to(docs_root).as_posix()
    new_hash = sha256_file(file_path)
    row = conn.execute("SELECT hash FROM files WHERE path = ?", (rel,)).fetchone()
    if row and row[0] == new_hash:
        return 0

    if row:
        drop_file(conn, rel)

    text = file_path.read_text(encoding="utf-8", errors="replace")
    chunks = chunk_markdown(text, chunking)
    if not chunks:
        conn.execute("INSERT INTO files(path, hash) VALUES (?, ?)", (rel, new_hash))
        return 0

    # Embed `heading_path — body` so the dense vector carries topical context.
    # Matches the format the cross-encoder reranker already uses, and is the
    # NX8 first-stage parity for what NX2 showed bge-large was reconstructing
    # from body alone.
    texts = [
        (" > ".join(h) + " — " + b) if h else b
        for h, b in chunks
    ]
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
        batch_size=32,
    )

    conn.execute("INSERT INTO files(path, hash) VALUES (?, ?)", (rel, new_hash))
    for ord_, ((heading, body), emb) in enumerate(zip(chunks, embeddings)):
        cur = conn.execute(
            "INSERT INTO chunks(file_path, heading_path, ord, text) VALUES (?, ?, ?, ?)",
            (rel, " > ".join(heading), ord_, body),
        )
        cid = cur.lastrowid
        conn.execute(
            "INSERT INTO vec_chunks(rowid, embedding) VALUES (?, ?)",
            (cid, serialize_f32(np.asarray(emb))),
        )
    return len(chunks)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--docs", default=str(DEFAULT_DOCS), help=f"Folder to index (default: {DEFAULT_DOCS})")
    ap.add_argument("--db", default=str(DEFAULT_DB), help=f"SQLite index path (default: {DEFAULT_DB})")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"Embedding model (default: {DEFAULT_MODEL})")
    ap.add_argument(
        "--chunking",
        choices=("legacy", "boundary"),
        default="legacy",
        help="Chunking strategy: legacy NX8/NX10 sliding windows or boundary-aware NX9 (default: legacy)",
    )
    ap.add_argument("--rebuild", action="store_true", help="Wipe the DB and re-embed everything")
    args = ap.parse_args()

    docs_root = Path(args.docs).resolve()
    db_path = Path(args.db).resolve()
    if not docs_root.exists():
        print(f"Docs folder not found: {docs_root}", file=sys.stderr)
        return 2

    if args.model not in MODEL_DIMS:
        print(f"Unknown model {args.model}. Add its dim to MODEL_DIMS first.", file=sys.stderr)
        return 2
    embed_dim = MODEL_DIMS[args.model]

    if args.rebuild and db_path.exists():
        db_path.unlink()

    print(f"Loading model {args.model} (first run downloads the weights) ...", flush=True)
    model = SentenceTransformer(args.model)

    conn = open_db(db_path, embed_dim)
    md_files = sorted(p for p in docs_root.rglob("*.md") if p.is_file())
    print(f"Found {len(md_files)} markdown files under {docs_root}")

    on_disk = {p.relative_to(docs_root).as_posix() for p in md_files}
    in_db = {row[0] for row in conn.execute("SELECT path FROM files").fetchall()}
    for stale in in_db - on_disk:
        drop_file(conn, stale)
        print(f"  removed (deleted): {stale}")

    new_chunks = 0
    indexed_files = 0
    for i, f in enumerate(md_files, 1):
        added = index_file(conn, model, docs_root, f, args.chunking)
        if added > 0:
            indexed_files += 1
            new_chunks += added
            print(f"  [{i}/{len(md_files)}] +{added:3d} chunks  {f.relative_to(docs_root)}")
        if i % 25 == 0:
            conn.commit()

    conn.commit()
    total_chunks = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    conn.close()

    print(f"\nDone. Re-indexed {indexed_files} files (+{new_chunks} chunks). Index now holds {total_chunks} chunks at {db_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
