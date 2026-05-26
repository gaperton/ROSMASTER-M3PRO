"""Build the bundled ROSMASTER M3 Pro SQLite RAG index."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import struct
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = SKILL_ROOT / "assets" / "corpus"
DEFAULT_DB = SKILL_ROOT / "assets" / "index" / "rosmaster_m3pro.sqlite"
MODEL_NAME = "BAAI/bge-small-en-v1.5"
EMBED_DIM = 384
CHUNK_TARGET_CHARS = 1800
CHUNK_OVERLAP_CHARS = 300
BATCH_SIZE = 32
COMMIT_EVERY = 25

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


def emit(payload: dict[str, Any], status: int = 0) -> int:
    print(json.dumps(payload, indent=2))
    return status


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def split_by_headings(text: str) -> list[tuple[list[str], str]]:
    sections: list[tuple[list[str], str]] = []
    stack: list[str] = []
    matches = list(HEADING_RE.finditer(text))
    if not matches:
        return [([], text.strip())] if text.strip() else []

    for i, match in enumerate(matches):
        level = len(match.group(1))
        title = match.group(2).strip()
        stack = stack[: level - 1]
        while len(stack) < level - 1:
            stack.append("")
        stack.append(title)

        body_start = match.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip()
        if body:
            sections.append(([part for part in stack if part], body))
    return sections


def chunk_section(heading: list[str], body: str) -> list[tuple[list[str], str]]:
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
    chunks: list[tuple[list[str], str]] = []
    for heading, body in split_by_headings(text):
        chunks.extend(chunk_section(heading, body))
    return chunks


def serialize_f32(vec: Any) -> bytes:
    import numpy as np

    return struct.pack(f"{len(vec)}f", *vec.astype(np.float32).tolist())


def open_db(db_path: Path) -> sqlite3.Connection:
    import sqlite_vec

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
    return conn


def drop_file(conn: sqlite3.Connection, file_path: str) -> None:
    rows = conn.execute("SELECT id FROM chunks WHERE file_path = ?", (file_path,)).fetchall()
    for (chunk_id,) in rows:
        conn.execute("DELETE FROM vec_chunks WHERE rowid = ?", (chunk_id,))
    conn.execute("DELETE FROM chunks WHERE file_path = ?", (file_path,))
    conn.execute("DELETE FROM files WHERE path = ?", (file_path,))


FilePlan = tuple[Path, str, str, bool]


def plan_files(conn: sqlite3.Connection, corpus_root: Path, files: list[Path]) -> tuple[list[FilePlan], list[str]]:
    known_hashes = dict(conn.execute("SELECT path, hash FROM files").fetchall())
    plans = []
    for path in files:
        relative_path = path.relative_to(corpus_root).as_posix()
        digest = sha256_file(path)
        plans.append((path, relative_path, digest, known_hashes.get(relative_path) != digest))
    removed = sorted(set(known_hashes) - {relative_path for _, relative_path, _, _ in plans})
    return plans, removed


def index_file(conn: sqlite3.Connection, model: Any, plan: FilePlan) -> int:
    import numpy as np

    path, relative_path, digest, changed = plan
    if not changed:
        return 0

    drop_file(conn, relative_path)
    chunks = chunk_markdown(path.read_text(encoding="utf-8", errors="replace"))
    conn.execute("INSERT INTO files(path, hash) VALUES (?, ?)", (relative_path, digest))
    if not chunks:
        return 0

    texts = [
        f"{' > '.join(heading)} - {body}" if heading else body
        for heading, body in chunks
    ]
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False, batch_size=BATCH_SIZE)

    for ordinal, ((heading, body), embedding) in enumerate(zip(chunks, embeddings)):
        cur = conn.execute(
            "INSERT INTO chunks(file_path, heading_path, ord, text) VALUES (?, ?, ?, ?)",
            (relative_path, " > ".join(heading), ordinal, body),
        )
        conn.execute(
            "INSERT INTO vec_chunks(rowid, embedding) VALUES (?, ?)",
            (cur.lastrowid, serialize_f32(np.asarray(embedding))),
        )
    return len(chunks)


def skill_relative(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(SKILL_ROOT).as_posix()
    except ValueError:
        return str(resolved)


def build_index(corpus_root: Path, db_path: Path, rebuild: bool) -> dict[str, Any]:
    if rebuild and db_path.exists():
        db_path.unlink()

    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = open_db(db_path)
    try:
        files = sorted(path for path in corpus_root.rglob("*.md") if path.is_file())
        plans, removed = plan_files(conn, corpus_root, files)
        for stale in removed:
            drop_file(conn, stale)

        indexed_files = 0
        new_chunks = 0
        changed = [plan for plan in plans if plan[3]]
        if changed:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer(MODEL_NAME)
            for i, plan in enumerate(changed, start=1):
                added = index_file(conn, model, plan)
                indexed_files += 1
                new_chunks += added
                if i % COMMIT_EVERY == 0:
                    conn.commit()

        conn.commit()
        total_chunks = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    finally:
        conn.close()

    return {
        "status": "ok",
        "model": MODEL_NAME,
        "db_path": skill_relative(db_path),
        "corpus_root": skill_relative(corpus_root),
        "markdown_files": len(files),
        "indexed_files": indexed_files,
        "new_chunks": new_chunks,
        "removed_files": removed,
        "total_chunks": total_chunks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs", default=str(DEFAULT_CORPUS), help="Markdown corpus root")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="SQLite index path")
    parser.add_argument("--rebuild", action="store_true", help="Delete and rebuild the index")
    args = parser.parse_args()

    corpus_root = Path(args.docs).resolve()
    db_path = Path(args.db).resolve()
    if not corpus_root.exists():
        return emit({"error": "corpus_not_found", "corpus_root": str(corpus_root)}, status=2)

    return emit(build_index(corpus_root, db_path, args.rebuild))


if __name__ == "__main__":
    raise SystemExit(main())
