"""Build a local LanceDB RAG index over a folder of markdown files.

Mirrors sqlite-rag/rag_index.py: same chunking, same embedding model, same
incremental sha256-based skip behavior. The chunking helpers are intentionally
duplicated from the sqlite-rag version so the two implementations stay
independent for the comparison; share them later once we pick a winner.

Usage (from repo root or from inside lance-db-rag/):
    python lance-db-rag/rag_index.py            # indexes ../markdown into lance-db-rag/index.lance
    python rag_index.py --docs other_dir --db other.lance
    python rag_index.py --rebuild               # wipe and re-embed everything
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
from pathlib import Path

import lancedb
from lancedb.pydantic import LanceModel, Vector

from bge import VARIANTS

CHUNK_TARGET_CHARS = 1800
CHUNK_OVERLAP_CHARS = 300

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
PAGE_SPAN_RE = re.compile(r"""<span\s+[^>]*id=["']page-[^"']+["'][^>]*>\s*</span>""", re.IGNORECASE)
PAGE_ANCHOR_LINK_RE = re.compile(r"\[([^\]]+)\]\(#page-[^)]+\)")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")
SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9`*_\"'])")

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DOCS = SCRIPT_DIR.parent / "markdown"
DEFAULT_DB = SCRIPT_DIR / "index.lance"


def make_chunk_model(variant: str):
    """Build a Chunk LanceModel pinned to the chosen BGE variant's vector dim.

    The class is constructed per call because Vector(ndims) bakes the dim into
    the pydantic schema at class definition time, and LanceDB stores it.

    Schema note: `text` carries body-only chunk text for display; `embed_source`
    carries `"<heading_path> — <body>"` and is what the embedding model sees
    (via SourceField). FTS is built on `embed_source` so the keyword channel
    also sees headings. Pre-NX8 indexes are still readable because rag_query.py
    only consumes `text`, `heading_path`, and the auto-built `vector` column.
    """
    bge = VARIANTS[variant].create()

    class Chunk(LanceModel):
        chunk_id: str
        file_path: str
        heading_path: str
        ord: int
        text: str
        embed_source: str = bge.SourceField()
        vector: Vector(bge.ndims()) = bge.VectorField()

    return Chunk


class FileHash(LanceModel):
    path: str
    hash: str


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


def sql_escape(s: str) -> str:
    """LanceDB delete() takes a raw predicate string; quote single-quotes."""
    return s.replace("'", "''")


def open_db(db_path: Path, variant: str):
    db = lancedb.connect(str(db_path))
    Chunk = make_chunk_model(variant)
    chunks_t = db.create_table("chunks", schema=Chunk, exist_ok=True)
    files_t = db.create_table("files", schema=FileHash, exist_ok=True)
    return db, chunks_t, files_t


def load_file_hashes(files_t) -> dict[str, str]:
    tbl = files_t.to_arrow()
    if tbl.num_rows == 0:
        return {}
    paths = tbl.column("path").to_pylist()
    hashes = tbl.column("hash").to_pylist()
    return dict(zip(paths, hashes))


def build_chunk_rows(docs_root: Path, file_path: Path, chunking: str) -> list[dict]:
    rel = file_path.relative_to(docs_root).as_posix()
    text = file_path.read_text(encoding="utf-8", errors="replace")
    sections = chunk_markdown(text, chunking)
    rows: list[dict] = []
    for ord_, (heading, body) in enumerate(sections):
        heading_str = " > ".join(heading)
        embed_source = f"{heading_str} — {body}" if heading_str else body
        rows.append(
            {
                "chunk_id": f"{rel}::{ord_}",
                "file_path": rel,
                "heading_path": heading_str,
                "ord": ord_,
                "text": body,
                "embed_source": embed_source,
            }
        )
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--docs", default=str(DEFAULT_DOCS), help=f"Folder to index (default: {DEFAULT_DOCS})")
    ap.add_argument("--db", default=str(DEFAULT_DB), help=f"LanceDB directory (default: {DEFAULT_DB})")
    ap.add_argument(
        "--variant",
        choices=tuple(VARIANTS),
        default="small",
        help="BGE variant: small (384-dim) or large (1024-dim). Must match the table's stored schema on re-open.",
    )
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

    if args.rebuild and db_path.exists():
        shutil.rmtree(db_path)

    print(f"Opening LanceDB at {db_path} (variant={args.variant}, embedding model loads lazily) ...", flush=True)
    db, chunks_t, files_t = open_db(db_path, args.variant)

    md_files = sorted(p for p in docs_root.rglob("*.md") if p.is_file())
    print(f"Found {len(md_files)} markdown files under {docs_root}")

    on_disk = {p.relative_to(docs_root).as_posix(): p for p in md_files}
    in_db = load_file_hashes(files_t)

    stale = set(in_db) - set(on_disk)
    if stale:
        stale_list = ", ".join(f"'{sql_escape(s)}'" for s in stale)
        chunks_t.delete(f"file_path IN ({stale_list})")
        for s in stale:
            files_t.delete(f"path = '{sql_escape(s)}'")
            print(f"  removed (deleted): {s}")

    to_index: list[Path] = []
    for rel, p in on_disk.items():
        new_hash = sha256_file(p)
        if in_db.get(rel) == new_hash:
            continue
        to_index.append(p)

    new_chunks = 0
    indexed_files = 0
    for i, f in enumerate(to_index, 1):
        rel = f.relative_to(docs_root).as_posix()
        if rel in in_db:
            chunks_t.delete(f"file_path = '{sql_escape(rel)}'")
            files_t.delete(f"path = '{sql_escape(rel)}'")
        rows = build_chunk_rows(docs_root, f, args.chunking)
        if rows:
            chunks_t.add(rows)
            new_chunks += len(rows)
            indexed_files += 1
            print(f"  [{i}/{len(to_index)}] +{len(rows):3d} chunks  {rel}")
        files_t.add([{"path": rel, "hash": sha256_file(f)}])

    # NX8: FTS on `embed_source` (heading + body) so the keyword channel sees
    # the heading text the same way the dense channel does.
    if new_chunks > 0:
        print("Rebuilding FTS index over chunks.embed_source ...", flush=True)
        chunks_t.create_fts_index("embed_source", replace=True)
    elif "embed_source_idx" not in {ix.name for ix in chunks_t.list_indices()}:
        print("Creating initial FTS index over chunks.embed_source ...", flush=True)
        chunks_t.create_fts_index("embed_source", replace=True)

    total_chunks = chunks_t.count_rows()
    print(
        f"\nDone. Re-indexed {indexed_files} files (+{new_chunks} chunks). "
        f"Index now holds {total_chunks} chunks at {db_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
