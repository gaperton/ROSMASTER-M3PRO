"""Post-process converted ROSMASTER corpus Markdown for cleaner retrieval text.

The source corpus is Marker-converted PDF Markdown. This script keeps source
files untouched by default and can write a mirrored processed corpus for
indexing with ``--out-dir``. Use ``--in-place`` only when you deliberately want
to rewrite the source README.md files.

Examples:
    python skills/rosmaster-m3pro-expert/scripts/post_process_corpus.py --check
    python skills/rosmaster-m3pro-expert/scripts/post_process_corpus.py --out-dir skills/rosmaster-m3pro-expert/assets/processed-corpus
    python skills/rosmaster-m3pro-expert/scripts/post_process_corpus.py --in-place
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import shutil
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
DEFAULT_CORPUS = SKILL_ROOT / "assets" / "corpus"

PAGE_SPAN_RE = re.compile(r"""<span\s+[^>]*id=["']page-[^"']+["'][^>]*>\s*</span>""", re.IGNORECASE)
PAGE_ANCHOR_LINK_RE = re.compile(r"\[([^\]]+)\]\(#page-[^)]+\)")
IMAGE_RE = re.compile(r"!\[\]\(([^)]+)\)")
HEADING_BOLD_RE = re.compile(r"^(#{1,6})\s+\*\*(.+?)\*\*\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
URL_RE = re.compile(r"https?://[^\s)]+")
URL_SENTINEL = "@@URL{0}@@"


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    repl: str | Callable[[re.Match[str]], str]
    outside_code_only: bool = True


def compile_rule(name: str, pattern: str, repl: str | Callable[[re.Match[str]], str], flags: int = 0) -> Rule:
    return Rule(name=name, pattern=re.compile(pattern, flags), repl=repl)


RULES: list[Rule] = [
    compile_rule("heading_bold_wrapper", r"^(#{1,6})\s+\*\*(.+?)\*\*\s*$", r"\1 \2", re.MULTILINE),
    compile_rule("heading_chinese_comma", r"^(\s*#{1,6}\s+\d+(?:\.\d+)*)\s*[\u3001\uff0c]\s*", r"\1. ", re.MULTILINE),
    compile_rule("page_anchor_link", r"\[([^\]]+)\]\(#page-[^)]+\)", r"\1"),
    compile_rule("html_br", r"<br\s*/?>", " ", re.IGNORECASE),
    compile_rule("escaped_underscore", r"\\_", "_"),
    compile_rule("doubleclick", r"\bdoubleclick\b", "double-click", re.IGNORECASE),
    compile_rule("selfheating_point", r"\bself[-\s]*heating point\b", "hotspot", re.IGNORECASE),
    compile_rule("ctrl_c", r"\bctrl\s*\+?\s*c\b", "Ctrl+C", re.IGNORECASE),
    compile_rule("wifi", r"\bwi[\-\s]?fi\b", "Wi-Fi", re.IGNORECASE),
    compile_rule("ip_plus_port", r"\bip\s*\+\s*:8888\b", "IP address + :8888", re.IGNORECASE),
    compile_rule("lowercase_ip", r"\bip address\b", "IP address", re.IGNORECASE),
    compile_rule("standalone_ip", r"\bip\b", "IP", re.IGNORECASE),
    compile_rule("putty", r"\bputty\b", "PuTTY", re.IGNORECASE),
    compile_rule("raspberry_pi_caps", r"\bRaspberry PI\b", "Raspberry Pi"),
    compile_rule("jetson_nano_hyphen", r"\bJetson[-\s]*Nano\b", "Jetson Nano", re.IGNORECASE),
    compile_rule("orin_nano_hyphen", r"\bOrin[-\s]*Nano\b", "Orin Nano", re.IGNORECASE),
    compile_rule("orin_nx_hyphen", r"\bOrin[-\s]*NX\b", "Orin NX", re.IGNORECASE),
    compile_rule("docker_typo", r"\bDockder\b", "Docker"),
    compile_rule("docker_duplicate", r"\bDocker Docker\b", "Docker"),
    compile_rule("large_typo", r"\bLargr\b", "Large"),
    compile_rule("yolov8", r"\bYolov8\b", "YOLOv8"),
    compile_rule("lidar", r"\bLidar\b", "LiDAR"),
    compile_rule("rviz", r"\brviz\b", "RViz", re.IGNORECASE),
    compile_rule("spacing_before_punct", r"\s+([,.;:])", r"\1"),
    compile_rule("button_x", r"\[x\]", "[X]", re.IGNORECASE),
    compile_rule("servo_no_space", r"\bNo\.\s*(\d+)\b", r"No. \1"),
    compile_rule("gripper_paren_space", r"\bgripper\(([^)]+)\)", r"gripper (\1)", re.IGNORECASE),
]

MOJIBAKE_REPLACEMENTS: dict[str, str] = {
    "\u00e2\u20ac\u201d": "-",
    "\u00e2\u20ac\u201c": "-",
    "\u00e2\u20ac\u02dc": "'",
    "\u00e2\u20ac\u2122": "'",
    "\u00e2\u20ac\u0153": '"',
    "\u00e2\u20ac\u009d": '"',
    "\u00e2\u2020\u2019": "->",
    "\u00e2\u2020\u0092": "->",
    "\u00c3\u2014": "x",
    "\u00c2\u00ae": "(R)",
    "\u00c2\u00b0": " degrees",
    "\u00c2": "",
    "\u00e3\u20ac\u0081": ", ",
}


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def repair_mojibake(text: str, counts: Counter[str]) -> str:
    for bad, good in MOJIBAKE_REPLACEMENTS.items():
        n = text.count(bad)
        if n:
            text = text.replace(bad, good)
            counts["mojibake"] += n
    return text


def image_alt(match: re.Match[str]) -> str:
    path = match.group(1)
    name = Path(path).stem.strip("_")
    page = re.search(r"page[_-](\d+)", name, re.IGNORECASE)
    kind = "image"
    if re.search(r"figure", name, re.IGNORECASE):
        kind = "figure"
    elif re.search(r"picture", name, re.IGNORECASE):
        kind = "picture"
    number = re.search(r"(?:figure|picture)[_-](\d+)", name, re.IGNORECASE)

    parts = [kind.capitalize()]
    if page:
        parts.append(f"page {page.group(1)}")
    if number:
        parts.append(f"{kind} {number.group(1)}")
    return f"![{': '.join(parts)}]({path})"


def apply_rules(text: str, counts: Counter[str]) -> str:
    urls: list[str] = []

    def stash_url(match: re.Match[str]) -> str:
        urls.append(match.group(0))
        return URL_SENTINEL.format(len(urls) - 1)

    text = URL_RE.sub(stash_url, text)
    for rule in RULES:
        text, n = rule.pattern.subn(rule.repl, text)
        if n:
            counts[rule.name] += n
    for i, url in enumerate(urls):
        text = text.replace(URL_SENTINEL.format(i), url)
    text, n = IMAGE_RE.subn(image_alt, text)
    if n:
        counts["image_alt_text"] += n
    return text


def process_markdown(text: str) -> tuple[str, Counter[str]]:
    counts: Counter[str] = Counter()
    text = normalize_newlines(text)
    text, n = PAGE_SPAN_RE.subn("", text)
    if n:
        counts["page_span"] += n

    out: list[str] = []
    in_fence = False
    for line in text.split("\n"):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line.rstrip())
            continue
        if in_fence:
            out.append(line.rstrip())
            continue
        line = repair_mojibake(line, counts)
        line = apply_rules(line, counts)
        out.append(line.rstrip())

    processed = "\n".join(out)
    processed = re.sub(r"\n{4,}", "\n\n\n", processed).strip() + "\n"
    return processed, counts


def iter_readmes(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("README.md") if p.is_file())


def mirror_target(source: Path, corpus_root: Path, out_root: Path) -> Path:
    return out_root / source.relative_to(corpus_root)


def copy_json_sidecar(source: Path, corpus_root: Path, out_root: Path) -> None:
    json_path = source.with_name("README.json")
    if not json_path.exists():
        return
    target = mirror_target(json_path, corpus_root, out_root)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(json_path, target)


def copy_assets(source: Path, corpus_root: Path, out_root: Path) -> None:
    for asset in source.parent.iterdir():
        if not asset.is_file() or asset.name in {"README.md", "README.json"}:
            continue
        target = mirror_target(asset, corpus_root, out_root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(asset, target)


def show_diff(path: Path, original: str, processed: str, corpus_root: Path, max_lines: int) -> None:
    rel = path.relative_to(corpus_root).as_posix()
    diff = list(
        difflib.unified_diff(
            original.splitlines(),
            processed.splitlines(),
            fromfile=f"a/{rel}",
            tofile=f"b/{rel}",
            lineterm="",
        )
    )
    if not diff:
        return
    print(f"\n--- sample diff: {rel}")
    for line in diff[:max_lines]:
        print(line)
    if len(diff) > max_lines:
        print(f"... ({len(diff) - max_lines} more diff lines)")


def write_manifest(out_root: Path, stats: dict[str, object]) -> None:
    out_root.mkdir(parents=True, exist_ok=True)
    manifest = out_root / "postprocess_manifest.json"
    manifest.write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs", default=str(DEFAULT_CORPUS), help="Corpus root containing README.md lesson files")
    parser.add_argument("--out-dir", help="Write a mirrored processed corpus to this directory")
    parser.add_argument("--in-place", action="store_true", help="Rewrite source README.md files in place")
    parser.add_argument("--copy-assets", action="store_true", help="With --out-dir, also copy images and other assets")
    parser.add_argument("--check", action="store_true", help="Only report files that would change")
    parser.add_argument("--sample", type=int, default=3, help="Number of changed files to show sample diffs for")
    parser.add_argument("--diff-lines", type=int, default=80, help="Maximum diff lines per sample")
    parser.add_argument("--limit", type=int, help="Process only the first N README.md files")
    args = parser.parse_args()

    corpus_root = Path(args.docs).resolve()
    if not corpus_root.exists():
        raise SystemExit(f"Corpus root does not exist: {corpus_root}")
    if args.in_place and args.out_dir:
        raise SystemExit("Use either --in-place or --out-dir, not both.")
    if args.copy_assets and not args.out_dir:
        raise SystemExit("--copy-assets only applies with --out-dir.")

    files = iter_readmes(corpus_root)
    if args.limit is not None:
        files = files[: args.limit]

    total_counts: Counter[str] = Counter()
    changed = 0
    written = 0
    sampled = 0
    out_root = Path(args.out_dir).resolve() if args.out_dir else None

    for path in files:
        original = path.read_text(encoding="utf-8", errors="replace")
        processed, counts = process_markdown(original)
        if processed == original:
            continue

        changed += 1
        total_counts.update(counts)
        if sampled < args.sample:
            show_diff(path, original, processed, corpus_root, args.diff_lines)
            sampled += 1

        if args.in_place:
            path.write_text(processed, encoding="utf-8")
            written += 1
        elif out_root is not None:
            target = mirror_target(path, corpus_root, out_root)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(processed, encoding="utf-8")
            copy_json_sidecar(path, corpus_root, out_root)
            if args.copy_assets:
                copy_assets(path, corpus_root, out_root)
            written += 1

    stats = {
        "corpus_root": str(corpus_root),
        "files_scanned": len(files),
        "files_changed": changed,
        "files_written": written,
        "replacement_counts": dict(total_counts),
    }
    if out_root is not None:
        stats["out_dir"] = str(out_root)
        write_manifest(out_root, stats)

    print("\nSummary")
    print(json.dumps(stats, indent=2, sort_keys=True))
    if changed and not args.in_place and out_root is None:
        print("\nNo files written. Use --out-dir to create a processed corpus, or --in-place to rewrite source README.md files.")
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
