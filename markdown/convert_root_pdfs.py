"""Convert root course PDFs (00-23) into a Markdown tree.

Output layout:
  markdown/<source path>/README.md

If a source folder contains multiple PDFs directly, each PDF gets its own
lesson folder under markdown so images cannot collide.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
import time
import traceback
from collections import Counter
from pathlib import Path

import pymupdf
import pymupdf4llm


ROOT = Path(__file__).resolve().parent.parent
DST_ROOT = ROOT / "markdown"
COURSE_PREFIXES = tuple(f"{i:02d}." for i in range(24))
NUMBERED_HEADING_RE = re.compile(r"^\s*(\d+(?:\.\d+)*)\s*(?:[、.,)]\s*)?(?:\S.*)?$")
DOTTED_NUMBERED_LINE_RE = re.compile(r"^\s*(\d{1,2}(?:\.\d{1,2})+)\s*(?:[、.,):：]\s*)?\S.*$")
IMAGE_LINK_PREFIX_RE = re.compile(r"!\[\]\((?:[^()\n]*/)?([^/()\\]+?\.(?:jpe?g|png))\)")
HEADING_BOLD_RE = re.compile(r"^(#{1,6})\s+\*\*(.+?)\*\*\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
BOLD_LINE_RE = re.compile(r"^\*\*(.+?)\*\*\s*$")


def collect_pdfs() -> list[Path]:
    pdfs: list[Path] = []
    for course_dir in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        if not course_dir.name.startswith(COURSE_PREFIXES):
            continue
        pdfs.extend(sorted(course_dir.rglob("*.pdf")))
        pdfs.extend(sorted(course_dir.rglob("*.PDF")))
    return sorted(set(pdfs))


def direct_pdf_counts(pdfs: list[Path]) -> Counter[Path]:
    return Counter(p.parent for p in pdfs)


def target_dir_for(pdf: Path, counts: Counter[Path]) -> Path:
    rel_parent = pdf.parent.relative_to(ROOT)
    if counts[pdf.parent] == 1:
        return DST_ROOT / rel_parent
    return DST_ROOT / rel_parent / pdf.stem


def has_output(pdf: Path, counts: Counter[Path]) -> bool:
    out_md = target_dir_for(pdf, counts) / "README.md"
    return out_md.exists() and out_md.stat().st_size > 0


def document_title_size(pdf: Path) -> float:
    """Use the largest bold span on page 1 as the non-numbered title size."""
    try:
        with pymupdf.open(pdf) as doc:
            if doc.page_count == 0:
                return 16.0
            page = doc[0]
            sizes: list[float] = []
            for block in page.get_text("dict").get("blocks", []):
                for line in block.get("lines", []):
                    text = "".join(span.get("text", "") for span in line.get("spans", [])).strip()
                    if NUMBERED_HEADING_RE.match(text):
                        continue
                    for span in line.get("spans", []):
                        if is_bold_span(span) and span.get("text", "").strip():
                            sizes.append(float(span.get("size", 0)))
            return max(sizes, default=16.0)
    except Exception:
        return 16.0


def is_bold_span(span: dict) -> bool:
    return "Bold" in span.get("font", "") or bool(span.get("flags", 0) & 16)


def make_header_detector(title_size: float):
    title_threshold = max(13.0, title_size - 0.5)

    def header_detector(span: dict, page=None) -> str:
        text = span.get("text", "").strip()
        if not text or not is_bold_span(span):
            return ""

        match = NUMBERED_HEADING_RE.match(text)
        if match:
            depth = match.group(1).count(".") + 1
            return f"{'#' * min(6, depth + 1)} "

        if page is not None and page.number == 0 and float(span.get("size", 0)) >= title_threshold:
            return "# "

        return ""

    return header_detector


def cleanup_markdown(markdown: str) -> str:
    markdown = markdown.replace("\r\n", "\n").replace("\r", "\n")
    markdown = IMAGE_LINK_PREFIX_RE.sub(r"![](\1)", markdown)
    markdown = merge_wrapped_numbered_headings(markdown)
    markdown = normalize_heading_lines(markdown)
    markdown = promote_standalone_dotted_numbered_lines(markdown)
    markdown = re.sub(r"[ \t]+\n", "\n", markdown)
    markdown = re.sub(r"\n{4,}", "\n\n\n", markdown)
    return markdown.strip() + "\n"


def clean_heading_text(text: str) -> str:
    text = text.strip()
    while text.startswith("**") and text.endswith("**") and len(text) >= 4:
        text = text[2:-2].strip()
    return text.replace("**", "").strip()


def heading_level_for(title: str, fallback_level: int, seen_heading: bool) -> int:
    if not seen_heading:
        return 1
    numbered = NUMBERED_HEADING_RE.match(title)
    if numbered:
        return min(6, numbered.group(1).count(".") + 2)
    return fallback_level


def split_fused_heading_text(text: str) -> list[str]:
    raw_parts = text.split("** **")
    parts = [clean_heading_text(part) for part in raw_parts if clean_heading_text(part)]
    if not parts:
        return [clean_heading_text(text)]

    groups: list[str] = []
    for part in parts:
        if groups and NUMBERED_HEADING_RE.match(part):
            groups.append(part)
        elif groups:
            groups[-1] = f"{groups[-1]} {part}".strip()
        else:
            groups.append(part)
    return groups


def normalize_heading_lines(markdown: str) -> str:
    out: list[str] = []
    seen_heading = False
    for line in markdown.split("\n"):
        heading = HEADING_RE.match(line)
        if not heading:
            out.append(line)
            continue

        fallback_level = len(heading.group(1))
        for title in split_fused_heading_text(heading.group(2)):
            level = heading_level_for(title, fallback_level, seen_heading)
            out.append(f"{'#' * level} {title}")
            seen_heading = True
    return "\n".join(out)


def promote_standalone_dotted_numbered_lines(markdown: str) -> str:
    lines = markdown.split("\n")
    out: list[str] = []
    in_fence = False

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append(line)
            continue

        if (
            in_fence
            or not stripped
            or stripped.startswith("#")
            or stripped.startswith("|")
            or stripped.startswith("!")
            or stripped.startswith("- ")
        ):
            out.append(line)
            continue

        match = DOTTED_NUMBERED_LINE_RE.match(stripped)
        if not match:
            out.append(line)
            continue

        prev_blank_or_heading = index == 0 or not lines[index - 1].strip() or lines[index - 1].lstrip().startswith("#")
        next_blank = index + 1 >= len(lines) or not lines[index + 1].strip()
        if not (prev_blank_or_heading and next_blank):
            out.append(line)
            continue

        level = min(6, match.group(1).count(".") + 2)
        out.append(f"{'#' * level} {stripped}")

    return "\n".join(out)


def merge_wrapped_numbered_headings(markdown: str) -> str:
    lines = markdown.split("\n")
    out: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        heading = HEADING_BOLD_RE.match(line)
        if not heading:
            out.append(line)
            index += 1
            continue

        title = heading.group(2)
        numbered = NUMBERED_HEADING_RE.match(title)
        if not numbered or title.count("(") <= title.count(")"):
            out.append(line)
            index += 1
            continue

        parts = [title]
        cursor = index + 1
        skipped_blanks = 0
        while cursor < len(lines) and not lines[cursor].strip():
            skipped_blanks += 1
            cursor += 1

        while cursor < len(lines):
            continuation = BOLD_LINE_RE.match(lines[cursor].strip())
            if not continuation:
                break
            parts.append(continuation.group(1))
            cursor += 1
            while cursor < len(lines) and not lines[cursor].strip():
                cursor += 1
            if " ".join(parts).count("(") <= " ".join(parts).count(")"):
                break

        if len(parts) == 1:
            out.append(line)
            out.extend([""] * skipped_blanks)
            index += 1
            continue

        out.append(f"{heading.group(1)} **{' '.join(parts)}**")
        index = cursor
    return "\n".join(out)


def move_generated_files(temp_dir: Path, final_dir: Path, md_text: str) -> None:
    if final_dir.exists():
        for old_image in final_dir.glob("*.jpeg"):
            old_image.unlink()
        for old_image in final_dir.glob("*.jpg"):
            old_image.unlink()
        for old_image in final_dir.glob("*.png"):
            old_image.unlink()

    final_dir.mkdir(parents=True, exist_ok=True)
    for generated in temp_dir.iterdir():
        if generated.is_file() and generated.suffix.lower() in {".jpeg", ".jpg", ".png"}:
            shutil.copy2(generated, final_dir / generated.name)
    (final_dir / "README.md").write_text(md_text, encoding="utf-8")


def convert_one(pdf: Path, out_dir: Path) -> None:
    title_size = document_title_size(pdf)
    header_detector = make_header_detector(title_size)

    with tempfile.TemporaryDirectory(prefix="rosmaster_pymupdf_", dir="C:\\") as tmp_name:
        tmp_dir = Path(tmp_name)
        started = time.time()
        markdown = pymupdf4llm.to_markdown(
            str(pdf),
            hdr_info=header_detector,
            image_format="jpeg",
            image_path=str(tmp_dir),
            show_progress=False,
            table_strategy="lines_strict",
            write_images=True,
        )
        markdown = cleanup_markdown(markdown)
        move_generated_files(tmp_dir, out_dir, markdown)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Regenerate existing README.md outputs")
    parser.add_argument("--limit", type=int, help="Convert only the first N pending PDFs")
    parser.add_argument("--pdf", action="append", help="Convert only this PDF path, relative to the repo root")
    parser.add_argument("--cleanup-existing", action="store_true", help="Apply Markdown cleanup to existing README.md files only")
    return parser.parse_args()


def cleanup_existing_readmes() -> int:
    readmes = [
        path
        for path in DST_ROOT.rglob("README.md")
        if "_converter_tests" not in path.parts
    ]
    changed = 0
    for path in readmes:
        original = path.read_text(encoding="utf-8", errors="replace")
        cleaned = cleanup_markdown(original)
        if cleaned == original:
            continue
        path.write_text(cleaned, encoding="utf-8")
        changed += 1
    print(f"Cleaned {changed} of {len(readmes)} README.md files.", flush=True)
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    pymupdf4llm.use_layout(False)
    args = parse_args()
    if args.cleanup_existing:
        return cleanup_existing_readmes()

    all_pdfs = [pdf.resolve() for pdf in collect_pdfs()]
    pdfs = [ROOT / path for path in args.pdf] if args.pdf else all_pdfs
    pdfs = [pdf.resolve() for pdf in pdfs]
    missing = [pdf for pdf in pdfs if not pdf.exists()]
    if missing:
        for pdf in missing:
            print(f"MISSING: {pdf}", flush=True)
        return 1

    counts = direct_pdf_counts(all_pdfs)
    todo = pdfs if args.force else [pdf for pdf in pdfs if not has_output(pdf, counts)]
    if args.limit is not None:
        todo = todo[: args.limit]

    print(f"Found {len(all_pdfs)} PDFs under root course folders 00-23.", flush=True)
    print(f"{len(todo)} PDFs to convert ({len(pdfs) - len(todo)} skipped).", flush=True)
    if not todo:
        return 0

    failures: list[tuple[str, str]] = []
    batch_started = time.time()
    for index, pdf in enumerate(todo, 1):
        rel = pdf.relative_to(ROOT)
        out_dir = target_dir_for(pdf, counts)
        print(f"[{index}/{len(todo)}] {rel}", flush=True)
        try:
            item_started = time.time()
            convert_one(pdf, out_dir)
            out_rel = (out_dir / "README.md").relative_to(ROOT)
            print(f"  -> {out_rel} ({time.time() - item_started:.1f}s)", flush=True)
        except Exception as exc:
            print(f"  !! FAILED: {exc}", flush=True)
            traceback.print_exc()
            failures.append((str(rel), str(exc)))

    print(f"Finished batch in {(time.time() - batch_started) / 60:.1f} min.", flush=True)
    if failures:
        print(f"Failures ({len(failures)}):", flush=True)
        for rel, err in failures:
            print(f"  {rel}: {err}", flush=True)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
