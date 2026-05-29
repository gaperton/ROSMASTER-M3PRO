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
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
BOLD_PARAGRAPH_RE = re.compile(r"^\*\*(.+?)\*\*$")
NUMBERED_HEADING_RE = re.compile(r"^(?P<num>\d+(?:\.\d+)*)(?:[.),]\s*|\s+)(?P<title>.+)$")
TOC_ITEM_RE = re.compile(r"^\s*-\s+\d+(?:\.\d+)*[.,)]?\s+.+$")
STANDALONE_NUMBERED_LINE_RE = re.compile(r"^(?P<num>\d+)\.\s+(?P<title>\S.+)$")
ORPHAN_NUMBERED_LIST_RE = re.compile(r"^\\?(?P<num>\d+(?:\.\d+)*)(?P<punct>[.)]?)\s+(?P<title>\S.+)$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
URL_RE = re.compile(r"https?://[^\s)]+")
URL_SENTINEL = "@@URL{0}@@"
CODE_COMMENT_RE = re.compile(r"^(\s*(?:#|//)\s*)(.*?)(\s*)$")
NON_ENGLISH_RE = re.compile(r"[\u3400-\u9fff\u0080-\u009f\u00e9\u00e7\u00e3\u00e2\u00c2\u00bd\u00b5\u00b3\u00c6]")
NON_ASCII_RE = re.compile(r"[^\x00-\x7f]")
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
MAC_RE = re.compile(r"\b[0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5}\b")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)+\|?\s*$")


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
    compile_rule("heading_number_comma", r"^(\s*#{1,6}\s+\d+(?:\.\d+)*),\s*", r"\1. ", re.MULTILINE),
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
    compile_rule("vnc_to", r"\bvncTo\b", "VNC Viewer to", re.IGNORECASE),
    compile_rule("vnc", r"\bvnc\b", "VNC", re.IGNORECASE),
    compile_rule("gnome", r"\bGnome\b", "GNOME"),
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
    "\u00e2\u02c6\u0161": "the check mark",
    "\u221a": "the check mark",
    "\u00c3\u2014": "x",
    "\u00c2\u00ae": "(R)",
    "\u00c2\u00b0": " degrees",
    "\u00c2": "",
    "\u00e3\u20ac\u0081": ", ",
    "\u00e8\u017d\u00b7\u00e5\u008f\u2013": "Get",
    "\u00e7\u00a7\u2019": "s",
    "\u00f0\u0178\u2014\u201d": "",
    "\u00f0\u0178\u201d\u00ba": "",
}

COMMENT_TRANSLATIONS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?:\u914d\u7f6e|\u00e9\u2026\u008d\u00e7\u00bd\u00ae)\s*VNC\s*server", re.IGNORECASE), "Configure VNC server"),
]


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def repair_mojibake(text: str, counts: Counter[str]) -> str:
    for bad, good in MOJIBAKE_REPLACEMENTS.items():
        n = text.count(bad)
        if n:
            text = text.replace(bad, good)
            counts["mojibake"] += n
    return text


def clean_code_comment(line: str, counts: Counter[str]) -> str:
    match = CODE_COMMENT_RE.match(line)
    if not match:
        return line.rstrip()

    prefix, body, suffix = match.groups()
    if not NON_ENGLISH_RE.search(body):
        return line.rstrip()

    cleaned = body.strip()
    for pattern, replacement in COMMENT_TRANSLATIONS:
        cleaned, n = pattern.subn(replacement, cleaned)
        if n:
            counts["code_comment_translation"] += n

    if NON_ENGLISH_RE.search(cleaned):
        parts = [part.strip() for part in re.split(r"\s+/\s+", cleaned) if part.strip()]
        english_parts = [part for part in parts if re.search(r"[A-Za-z]", part) and not NON_ENGLISH_RE.search(part)]
        if english_parts:
            cleaned = english_parts[-1]
            counts["code_comment_english_side"] += 1

    if NON_ENGLISH_RE.search(cleaned):
        cleaned = NON_ENGLISH_RE.sub("", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip(" -:/")
        counts["code_comment_non_english_removed"] += 1

    return f"{prefix}{cleaned}{suffix}".rstrip() if cleaned else prefix.rstrip()


def clean_code_line(line: str, counts: Counter[str]) -> str:
    comment_match = CODE_COMMENT_RE.match(line)
    if comment_match:
        return clean_code_comment(line, counts)
    if not NON_ENGLISH_RE.search(line) and not NON_ASCII_RE.search(line):
        return line.rstrip()
    cleaned = repair_mojibake(line, counts)
    cleaned = cleaned.replace("\u83b7\u53d6", "Get").replace("\u79d2", "s")
    cleaned = re.sub(r"[\U0001f300-\U0001faff]", "", cleaned)
    if NON_ASCII_RE.search(cleaned):
        cleaned = NON_ASCII_RE.sub("", cleaned)
        counts["code_line_non_english_removed"] += 1
    return cleaned.rstrip()


def split_table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def clean_table_cell(cell: str) -> str:
    cell = re.sub(r"<[^>]+>", "", cell)
    cell = NON_ASCII_RE.sub("", cell)
    cell = re.sub(r"\s+", " ", cell).strip()
    return cell


def clean_table_row(line: str, counts: Counter[str]) -> list[str] | None:
    if not line.lstrip().startswith("|"):
        return None

    cells = split_table_cells(line)
    has_ip_header = any(cell.strip().casefold() == "ip" for cell in cells)
    has_mac_text = any("MAC" in cell.upper() for cell in cells)
    if has_ip_header and has_mac_text and not IPV4_RE.search(line):
        counts["scanner_table_header"] += 1
        return [
            "| Status | Name | IP address | MAC address | Notes |",
            "|---|---|---|---|---|",
        ]

    if IPV4_RE.search(line) and MAC_RE.search(line):
        cleaned = [clean_table_cell(cell) for cell in cells[:5]]
        while len(cleaned) < 5:
            cleaned.append("")
        counts["scanner_table_row"] += 1
        return ["| " + " | ".join(cleaned) + " |"]

    if not NON_ENGLISH_RE.search(line):
        return None

    counts["non_english_table_noise_removed"] += 1
    return []


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


def normalize_heading_level(
    line: str,
    heading_count: int,
    last_level: int,
    numbered_parent_level: int,
    document_title: str,
    counts: Counter[str],
) -> tuple[str, int | None, bool, bool]:
    match = HEADING_RE.match(line)
    if not match:
        return line, None, False, False

    original_level = len(match.group(1))
    title = match.group(2).strip()
    target_level = original_level
    numbered = NUMBERED_HEADING_RE.match(title)
    is_numbered = numbered is not None

    if heading_count == 0:
        target_level = 1
    else:
        if numbered:
            number_depth = numbered.group("num").count(".") + 1
            if numbered_parent_level:
                target_level = min(6, numbered_parent_level + number_depth)
            else:
                target_level = min(6, number_depth + 1)
        elif last_level and original_level > last_level + 1:
            target_level = last_level + 1

    if target_level != original_level:
        counts["heading_hierarchy"] += 1
    is_duplicate_title = bool(document_title) and title.casefold() == document_title.casefold()
    return f"{'#' * target_level} {title}", target_level, is_numbered, is_duplicate_title


def normalize_title_for_compare(title: str) -> str:
    title = PAGE_ANCHOR_LINK_RE.sub(r"\1", title)
    title = re.sub(r"[*_`\\]", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title.casefold()


def is_toc_line(line: str) -> bool:
    return TOC_ITEM_RE.match(line) is not None


def is_command_like_heading(title: str) -> bool:
    stripped = title.strip()
    if not stripped:
        return False
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9 ]*:", stripped):
        return False
    if re.fullmatch(r"[A-Za-z0-9_.:/+-]+", stripped) and " " not in stripped:
        return True
    return False


def is_shell_command(text: str) -> bool:
    stripped = text.strip()
    if not stripped or len(stripped) > 160:
        return False
    if re.match(
        r"^(?:sudo\s+)?(?:apt(?:-get)?|pip3?|python3?|ros2?|colcon|git|cd|ls|mkdir|cp|mv|rm|chmod|chown|"
        r"systemctl|gsettings|ifconfig|ip|ping|ssh|scp|docker|source|echo|cat|tar|nano|vim|vi)\b",
        stripped,
    ):
        return True
    return False


def convert_bold_commands(lines: list[str], counts: Counter[str]) -> list[str]:
    out: list[str] = []
    in_fence = False
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        match = BOLD_PARAGRAPH_RE.match(line.strip())
        if match and is_shell_command(match.group(1)):
            out.extend(["```bash", match.group(1).strip(), "```"])
            counts["bold_command_to_code"] += 1
        else:
            out.append(line)
    return out


def strip_bold_paragraphs(lines: list[str], counts: Counter[str]) -> list[str]:
    out: list[str] = []
    in_fence = False
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        match = BOLD_PARAGRAPH_RE.match(line.strip())
        if match:
            out.append(match.group(1).strip())
            counts["bold_paragraph_unwrapped"] += 1
        else:
            out.append(line)
    return out


def convert_standalone_commands(lines: list[str], counts: Counter[str]) -> list[str]:
    out: list[str] = []
    in_fence = False
    for i, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        stripped = line.strip()
        prev_blank = i == 0 or not lines[i - 1].strip()
        next_blank = i + 1 >= len(lines) or not lines[i + 1].strip()
        if prev_blank and next_blank and is_shell_command(stripped):
            out.extend(["```bash", stripped, "```"])
            counts["standalone_command_to_code"] += 1
        else:
            out.append(line)
    return out


def infer_code_language(block: list[str]) -> str:
    nonblank = [line.strip() for line in block if line.strip()]
    if not nonblank:
        return ""

    joined = "\n".join(nonblank)
    if re.search(r"^(?:import|from|class|def)\s", joined, re.MULTILINE) or "rclpy." in joined:
        return "python"

    command_like = 0
    checked = 0
    for line in nonblank:
        if line.startswith("#"):
            continue
        checked += 1
        if is_shell_command(line):
            command_like += 1
    if command_like and command_like >= max(1, checked // 2):
        return "bash"

    return ""


def annotate_code_fence_languages(lines: list[str], counts: Counter[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not FENCE_RE.match(line):
            out.append(line)
            i += 1
            continue
        if line.strip() != "```":
            out.append(line)
            i += 1
            while i < len(lines):
                out.append(lines[i])
                if FENCE_RE.match(lines[i]):
                    i += 1
                    break
                i += 1
            continue

        end = i + 1
        while end < len(lines) and not FENCE_RE.match(lines[end]):
            end += 1
        if end >= len(lines):
            out.append(line)
            i += 1
            continue

        block = lines[i + 1 : end]
        language = infer_code_language(block)
        out.append(f"```{language}" if language else line)
        if language:
            counts[f"code_fence_{language}"] += 1
        out.extend(block)
        out.append(lines[end])
        i = end + 1
    return out


def fix_command_reference_rows(lines: list[str], counts: Counter[str]) -> list[str]:
    out: list[str] = []
    in_fence = False
    current_heading = ""
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            stripped = line.strip()
            if current_heading == "6.1. ros2 service list" and stripped == "ros2 interface show interface_name":
                out.append("ros2 service list")
                counts["ros2_service_command_fix"] += 1
                continue
            if current_heading == "6.2. ros2 service call" and stripped == "ros2 interface call service_name service_Type arguments":
                out.append("ros2 service call service_name service_type arguments")
                counts["ros2_service_command_fix"] += 1
                continue
            out.append(line)
            continue

        heading = HEADING_RE.match(line)
        if heading:
            current_heading = heading.group(2).strip()
            if current_heading == "4.5. ros2 topic pub":
                out.append(f"{heading.group(1)} 4.6. ros2 topic pub")
                counts["topic_pub_heading_number"] += 1
                current_heading = "4.6. ros2 topic pub"
                continue

        inline_format = re.match(r"^Format:\s+(.+)$", line.strip())
        if inline_format and is_shell_command(inline_format.group(1)):
            out.extend(["Format:", "", "```bash", inline_format.group(1).strip(), "```"])
            counts["inline_format_command_to_code"] += 1
            continue

        stripped = line.strip()
        if current_heading == "6.1. ros2 service list" and stripped == "ros2 interface show interface_name":
            out.append("ros2 service list")
            counts["ros2_service_command_fix"] += 1
            continue
        if current_heading == "6.2. ros2 service call" and stripped == "ros2 interface call service_name service_Type arguments":
            out.append("ros2 service call service_name service_type arguments")
            counts["ros2_service_command_fix"] += 1
            continue

        out.append(line)
    return out


def numbered_heading_depth(title: str) -> int | None:
    match = NUMBERED_HEADING_RE.match(title)
    if not match:
        return None
    return match.group("num").count(".") + 1


def remove_duplicate_title_and_toc(lines: list[str], counts: Counter[str]) -> list[str]:
    first_heading_index = next((i for i, line in enumerate(lines) if HEADING_RE.match(line)), None)
    if first_heading_index is None:
        return lines

    first_match = HEADING_RE.match(lines[first_heading_index])
    assert first_match is not None
    title_key = normalize_title_for_compare(first_match.group(2))
    remove: set[int] = set()

    i = first_heading_index + 1
    while i < len(lines) and not lines[i].strip():
        i += 1

    if i < len(lines):
        second_match = HEADING_RE.match(lines[i])
        if second_match and normalize_title_for_compare(second_match.group(2)) == title_key:
            remove.add(i)
            counts["duplicate_title_heading"] += 1
            i += 1
            while i < len(lines) and not lines[i].strip():
                remove.add(i)
                i += 1

    toc_start = i
    while i < len(lines) and is_toc_line(lines[i]):
        remove.add(i)
        i += 1
    if i > toc_start:
        while i < len(lines) and not lines[i].strip():
            remove.add(i)
            i += 1
        counts["toc_lines_removed"] += i - toc_start

    if not remove:
        return lines
    return [line for idx, line in enumerate(lines) if idx not in remove]


def previous_nonblank(lines: list[str], index: int) -> str:
    for i in range(index - 1, -1, -1):
        if lines[i].strip():
            return lines[i]
    return ""


def convert_command_headings(lines: list[str], counts: Counter[str]) -> list[str]:
    out: list[str] = []
    for i, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match:
            out.append(line)
            continue

        title = match.group(2).strip()
        prev = previous_nonblank(lines, i).casefold()
        if is_command_like_heading(title) and re.search(r"\b(command|terminal|enter|run|execute)\b", prev):
            out.extend(["```bash", title, "```"])
            counts["command_heading_to_code"] += 1
        else:
            out.append(line)
    return out


def has_top_level_numbered_heading(lines: list[str]) -> bool:
    for line in lines:
        match = HEADING_RE.match(line)
        if not match:
            continue
        title = match.group(2).strip()
        numbered = NUMBERED_HEADING_RE.match(title)
        if numbered and numbered.group("num").count(".") == 0:
            return True
    return False


def promote_standalone_numbered_steps(lines: list[str], counts: Counter[str]) -> list[str]:
    if not has_top_level_numbered_heading(lines):
        return lines

    out: list[str] = []
    in_fence = False
    for i, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        if HEADING_RE.match(line):
            out.append(line)
            continue

        match = STANDALONE_NUMBERED_LINE_RE.match(line)
        if not match:
            out.append(line)
            continue

        prev_blank = i == 0 or not lines[i - 1].strip()
        next_blank = i + 1 >= len(lines) or not lines[i + 1].strip()
        if prev_blank and next_blank:
            out.append(f"## {match.group('num')}. {match.group('title').strip()}")
            counts["numbered_line_to_heading"] += 1
        else:
            out.append(line)
    return out


def normalize_orphan_numbered_list_items(lines: list[str], counts: Counter[str]) -> list[str]:
    out: list[str] = []
    in_fence = False
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence or HEADING_RE.match(line) or line.lstrip().startswith("- "):
            out.append(line)
            continue

        match = ORPHAN_NUMBERED_LIST_RE.match(line.strip())
        if match and (match.group("punct") or "." in match.group("num")):
            out.append(f"- {match.group('num')}. {match.group('title').strip()}")
            counts["orphan_numbered_line_to_list"] += 1
        else:
            out.append(line)
    return out


def process_markdown(
    text: str,
    normalize_heading_levels: bool = False,
    remove_toc: bool = True,
    convert_commands: bool = True,
    promote_numbered_steps: bool = True,
) -> tuple[str, Counter[str]]:
    counts: Counter[str] = Counter()
    text = normalize_newlines(text)
    text, n = PAGE_SPAN_RE.subn("", text)
    if n:
        counts["page_span"] += n

    normalized_lines: list[str] = []
    in_fence = False
    for line in text.split("\n"):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            normalized_lines.append(line.rstrip())
            continue
        if in_fence:
            normalized_lines.append(clean_code_line(line, counts))
            continue
        table_rows = clean_table_row(line, counts)
        if table_rows is not None:
            normalized_lines.extend(table_rows)
            continue
        if TABLE_SEPARATOR_RE.match(line) and (
            not normalized_lines or not normalized_lines[-1].lstrip().startswith("|")
        ):
            counts["orphan_table_separator_removed"] += 1
            continue
        line = repair_mojibake(line, counts)
        line = apply_rules(line, counts)
        normalized_lines.append(line.rstrip())

    if remove_toc:
        normalized_lines = remove_duplicate_title_and_toc(normalized_lines, counts)
    if promote_numbered_steps:
        normalized_lines = promote_standalone_numbered_steps(normalized_lines, counts)
    else:
        normalized_lines = normalize_orphan_numbered_list_items(normalized_lines, counts)
    if convert_commands:
        normalized_lines = convert_bold_commands(normalized_lines, counts)
        normalized_lines = strip_bold_paragraphs(normalized_lines, counts)
        normalized_lines = convert_standalone_commands(normalized_lines, counts)
        normalized_lines = convert_command_headings(normalized_lines, counts)
        normalized_lines = annotate_code_fence_languages(normalized_lines, counts)
        normalized_lines = fix_command_reference_rows(normalized_lines, counts)

    out: list[str] = []
    heading_count = 0
    last_heading_level = 0
    pending_numbered_parent_level = 0
    active_numbered_parent_level = 0
    document_title = ""
    in_fence = False
    for line in normalized_lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line.rstrip())
            continue
        if in_fence:
            out.append(line.rstrip())
            continue
        if normalize_heading_levels:
            raw_heading = HEADING_RE.match(line)
            raw_title = raw_heading.group(2).strip() if raw_heading else ""
            raw_numbered_depth = numbered_heading_depth(raw_title)
            raw_heading_level = len(raw_heading.group(1)) if raw_heading else 0
            if raw_numbered_depth is not None and active_numbered_parent_level and raw_heading_level:
                if raw_heading_level < active_numbered_parent_level:
                    active_numbered_parent_level = 0
                    pending_numbered_parent_level = 0
            parent_level = active_numbered_parent_level
            if raw_numbered_depth is not None:
                if (
                    active_numbered_parent_level == 0
                    and pending_numbered_parent_level
                    and raw_numbered_depth == 1
                    and raw_title.startswith("1")
                ):
                    active_numbered_parent_level = pending_numbered_parent_level
                    parent_level = active_numbered_parent_level
                elif active_numbered_parent_level == 0:
                    pending_numbered_parent_level = 0

            normalized, heading_level, is_numbered_heading, is_duplicate_title = normalize_heading_level(
                line, heading_count, last_heading_level, parent_level, document_title, counts
            )
            if heading_level is not None:
                title_match = HEADING_RE.match(normalized)
                title = title_match.group(2).strip() if title_match else ""
                heading_count += 1
                last_heading_level = heading_level
                if heading_count == 1:
                    document_title = title
                    pending_numbered_parent_level = 0
                    active_numbered_parent_level = 0
                elif is_numbered_heading:
                    pass
                elif heading_level > 1 and not is_duplicate_title and not is_command_like_heading(title):
                    pending_numbered_parent_level = heading_level
                    active_numbered_parent_level = 0
                elif not is_command_like_heading(title):
                    pending_numbered_parent_level = 0
                    active_numbered_parent_level = 0
            line = normalized
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
    parser.add_argument(
        "--normalize-heading-levels",
        action="store_true",
        help="Normalize numbered Markdown heading levels after removing duplicate TOC/title noise.",
    )
    parser.add_argument("--keep-toc", action="store_true", help="Keep duplicate title/table-of-contents blocks")
    parser.add_argument("--keep-command-headings", action="store_true", help="Keep command-like headings as headings")
    parser.add_argument("--keep-numbered-lines", action="store_true", help="Keep standalone numbered step lines as paragraphs")
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
        processed, counts = process_markdown(
            original,
            normalize_heading_levels=args.normalize_heading_levels,
            remove_toc=not args.keep_toc,
            convert_commands=not args.keep_command_headings,
            promote_numbered_steps=not args.keep_numbered_lines,
        )
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
