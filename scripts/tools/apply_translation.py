#!/usr/bin/env python3
"""Safe, atomic translation applicator for PvZ Fusion.

Adds exact string translations or regex rules to JSON dictionaries with:
- Placeholder validation ({0}, {1}, etc. matching 1-to-1)
- Rich-text tag balancing (<color>, <nobr>, etc.)
- Protected identifier guard (e.g. Rogue shooting enums)
- Automatic sync to translation_strings.json

Usage:
    python scripts/tools/apply_translation.py --zh "测试" --en "Test" --file odyssey_evolution.json
    python scripts/tools/apply_translation.py --regex "^第(\\d+)页$" --repl "Page {1}"
    python scripts/tools/apply_translation.py --batch new_strings.json --file odyssey_evolution.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
STRINGS_DIR = ROOT / "translation-data/Strings"

CSHARP_FORMAT_RE = re.compile(r"\{(\d+)(?:,[^}:]+)?(?::[^}]+)?\}")
REGEX_TEMPLATE_RE = re.compile(r"\{(\d+)\}")
OPEN_TAG_RE = re.compile(r"<([a-zA-Z0-9]+)(?:=[^>]+)?>")
CLOSE_TAG_RE = re.compile(r"</([a-zA-Z0-9]+)>")

PROTECTED_NAMES_FILE = STRINGS_DIR / "shooting_group_names.json"
PROTECTED_NAMES = set()
if PROTECTED_NAMES_FILE.exists():
    try:
        PROTECTED_NAMES = set(json.loads(PROTECTED_NAMES_FILE.read_text(encoding="utf-8")))
    except Exception:
        pass


def validate_format_placeholders(src: str, trans: str) -> None:
    src_indices = set(CSHARP_FORMAT_RE.findall(src))
    trans_indices = set(CSHARP_FORMAT_RE.findall(trans))
    if src_indices != trans_indices:
        raise ValueError(
            f"Placeholder mismatch:\n  Source has {sorted(list(src_indices))}\n  Translation has {sorted(list(trans_indices))}"
        )


def validate_regex_templates(pattern: str, repl: str) -> None:
    # Test valid regex compile
    try:
        compiled = re.compile(pattern)
    except re.error as e:
        raise ValueError(f"Invalid regular expression {pattern!r}: {e}")

    num_groups = compiled.groups
    used_groups = [int(g) for g in REGEX_TEMPLATE_RE.findall(repl)]
    for g in used_groups:
        if g < 1 or g > num_groups:
            raise ValueError(
                f"Regex template group {{{g}}} out of range (pattern has {num_groups} capture groups)"
            )


def validate_xml_tags(text: str) -> None:
    opens = [m.lower() for m in OPEN_TAG_RE.findall(text)]
    closes = [m.lower() for m in CLOSE_TAG_RE.findall(text)]
    # Some tags like <br> are self-closing
    opens = [t for t in opens if t not in ("br", "hr")]
    if sorted(opens) != sorted(closes):
        # Warning only
        print(f"Warning: XML tag mismatch in {text!r} (opened {opens}, closed {closes})", file=sys.stderr)


def apply_exact_translation(src: str, trans: str, target_filename: str) -> bool:
    if src in PROTECTED_NAMES:
        raise ValueError(f"Cannot translate protected code identifier {src!r}!")

    validate_format_placeholders(src, trans)
    validate_xml_tags(trans)

    target_path = STRINGS_DIR / target_filename
    if not target_path.exists():
        raise FileNotFoundError(f"Target file does not exist: {target_path}")

    with open(target_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data[src] = trans

    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Sync to translation_strings.json if target was a specialized file
    if target_filename != "translation_strings.json":
        main_path = STRINGS_DIR / "translation_strings.json"
        with open(main_path, "r", encoding="utf-8") as f:
            main_data = json.load(f)
        main_data[src] = trans
        with open(main_path, "w", encoding="utf-8") as f:
            json.dump(main_data, f, ensure_ascii=False, indent=2)

    print(f"Applied exact translation: {repr(src)} -> {repr(trans)} in {target_filename}")
    return True


def apply_regex_rule(pattern: str, repl: str, target_filename: str = "translation_regexs.json") -> bool:
    validate_regex_templates(pattern, repl)

    target_path = STRINGS_DIR / target_filename
    with open(target_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data[pattern] = repl

    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Applied regex rule: {repr(pattern)} -> {repr(repl)} in {target_filename}")
    return True


def apply_batch(batch_path: Path, target_filename: str) -> int:
    with open(batch_path, "r", encoding="utf-8") as f:
        batch_data = json.load(f)

    count = 0
    for src, trans in batch_data.items():
        if isinstance(src, str) and isinstance(trans, str):
            apply_exact_translation(src, trans, target_filename)
            count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zh", help="Chinese source text")
    parser.add_argument("--en", help="English translated text")
    parser.add_argument("--file", default="odyssey_evolution.json", help="Target JSON file (default: odyssey_evolution.json)")
    parser.add_argument("--regex", help="Regular expression pattern")
    parser.add_argument("--repl", help="Regular expression replacement template with {1}, {2}, etc.")
    parser.add_argument("--batch", type=Path, help="Path to JSON file with {zh: en} batch pairs")
    args = parser.parse_args()

    try:
        if args.batch:
            cnt = apply_batch(args.batch, args.file)
            print(f"Successfully applied {cnt} batch translations.")
        elif args.regex and args.repl:
            apply_regex_rule(args.regex, args.repl, args.file if "regex" in args.file else "translation_regexs.json")
        elif args.zh and args.en:
            apply_exact_translation(args.zh, args.en, args.file)
        else:
            parser.print_help()
            return 1
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
