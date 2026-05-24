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
EMBED_DIM = 384
CHUNK_TARGET_CHARS = 1800
CHUNK_OVERLAP_CHARS = 300

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DOCS = SCRIPT_DIR.parent / "markdown"
DEFAULT_DB = SCRIPT_DIR / "rag_index.db"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def split_by_headings(text: str) -> list[tuple[list[str], str]]:
    """Split markdown into (heading_path, body) sections.

    heading_path is the stack of H1..Hn titles leading to that section.
    """
    sections: list[tuple[list[str], str]] = []
    stack: list[str] = []
    cursor = 0
    current_heading_stack: list[str] = []

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
        current_heading_stack = [s for s in stack if s]

        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip()
        if body:
            sections.append((list(current_heading_stack), body))

    return [(h, b) for h, b in sections if b]


def chunk_section(heading: list[str], body: str) -> list[tuple[list[str], str]]:
    """If a section body is too long, slice with overlap."""
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


def chunk_markdown(text: str) -> list[tuple[list[str], str]]:
    out: list[tuple[list[str], str]] = []
    for heading, body in split_by_headings(text):
        out.extend(chunk_section(heading, body))
    return out


def serialize_f32(vec: np.ndarray) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec.astype(np.float32).tolist())


def open_db(db_path: Path) -> sqlite3.Connection:
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
            embedding float[{EMBED_DIM}]
        );
        """
    )
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
) -> int:
    rel = file_path.relative_to(docs_root).as_posix()
    new_hash = sha256_file(file_path)
    row = conn.execute("SELECT hash FROM files WHERE path = ?", (rel,)).fetchone()
    if row and row[0] == new_hash:
        return 0

    if row:
        drop_file(conn, rel)

    text = file_path.read_text(encoding="utf-8", errors="replace")
    chunks = chunk_markdown(text)
    if not chunks:
        conn.execute("INSERT INTO files(path, hash) VALUES (?, ?)", (rel, new_hash))
        return 0

    texts = [body for _, body in chunks]
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
    ap.add_argument("--rebuild", action="store_true", help="Wipe the DB and re-embed everything")
    args = ap.parse_args()

    docs_root = Path(args.docs).resolve()
    db_path = Path(args.db).resolve()
    if not docs_root.exists():
        print(f"Docs folder not found: {docs_root}", file=sys.stderr)
        return 2

    if args.rebuild and db_path.exists():
        db_path.unlink()

    print(f"Loading model {args.model} (first run downloads ~130MB) ...", flush=True)
    model = SentenceTransformer(args.model)

    conn = open_db(db_path)
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
        added = index_file(conn, model, docs_root, f)
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
