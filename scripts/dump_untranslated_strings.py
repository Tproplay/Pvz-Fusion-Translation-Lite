#!/usr/bin/env python3
"""Dump all untranslated Chinese strings from global-metadata.dat and data.unity3d.

This extracts player-facing strings that still contain Chinese characters
and exports them into a structured JSON dictionary ready for translation.
"""

from __future__ import annotations

import argparse
import json
import re
import struct
from pathlib import Path

import UnityPy

CJK_RE = re.compile(r"[\u3400-\u9fff]")
TEXT_OFFSET = 88


def read_tmp_text(raw: bytes) -> str | None:
    if len(raw) < TEXT_OFFSET + 4:
        return None
    length = struct.unpack_from("<i", raw, TEXT_OFFSET)[0]
    if length <= 0 or TEXT_OFFSET + 4 + length > len(raw):
        return None
    try:
        return raw[TEXT_OFFSET + 4 : TEXT_OFFSET + 4 + length].decode("utf-8")
    except UnicodeDecodeError:
        return None


def read_metadata_literals(metadata_path: Path) -> list[str]:
    data = metadata_path.read_bytes()
    str_offset, str_size = struct.unpack_from("<II", data, 8)
    lit_offset, lit_size = struct.unpack_from("<II", data, 16)
    count = str_size // 8
    literals = []
    for i in range(count):
        length, rel_offset = struct.unpack_from("<II", data, str_offset + i * 8)
        abs_offset = lit_offset + rel_offset
        if abs_offset + length <= len(data):
            try:
                s = data[abs_offset : abs_offset + length].decode("utf-8")
                literals.append(s)
            except UnicodeDecodeError:
                pass
    return literals


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--bundle", required=True, type=Path)
    parser.add_argument("--strings-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    # Load existing translated strings
    known_translated: set[str] = set()
    exact_path = args.strings_dir / "translation_strings.json"
    if exact_path.exists():
        with exact_path.open("r", encoding="utf-8") as f:
            known_translated.update(json.load(f).keys())

    # Load existing regexes
    regex_path = args.strings_dir / "translation_regexs.json"
    compiled_regexes = []
    if regex_path.exists():
        with regex_path.open("r", encoding="utf-8") as f:
            for pat in json.load(f).keys():
                try:
                    compiled_regexes.append(re.compile(pat))
                except Exception:
                    pass

    untranslated_metadata: set[str] = set()
    untranslated_ui: set[str] = set()

    # 1. Scan metadata
    print(f"Scanning metadata {args.metadata}...")
    for lit in read_metadata_literals(args.metadata):
        if not CJK_RE.search(lit):
            continue
        if lit in known_translated:
            continue
        if any(r.search(lit) for r in compiled_regexes):
            continue
        # Filter out obvious source code paths / internal identifiers
        if "\\" in lit or "/" in lit or lit.startswith("CS$") or "::" in lit:
            continue
        untranslated_metadata.add(lit)

    # 2. Scan bundle UI
    print(f"Scanning bundle {args.bundle}...")
    env = UnityPy.load(str(args.bundle))
    for obj in env.objects:
        if obj.type.name == "MonoBehaviour":
            text = read_tmp_text(bytes(obj.get_raw_data()))
            if text and CJK_RE.search(text):
                if text not in known_translated and not any(r.search(text) for r in compiled_regexes):
                    untranslated_ui.add(text)

    # Combine unique untranslated strings
    all_untranslated = sorted(untranslated_metadata | untranslated_ui)

    dump_payload = {
        "summary": {
            "metadata_untranslated_count": len(untranslated_metadata),
            "ui_untranslated_count": len(untranslated_ui),
            "total_unique_untranslated": len(all_untranslated),
        },
        "strings": {s: "" for s in all_untranslated},
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        json.dump(dump_payload, f, ensure_ascii=False, indent=2)

    print(
        f"Dump complete! Found {len(all_untranslated)} untranslated strings "
        f"({len(untranslated_metadata)} from metadata, {len(untranslated_ui)} from UI). "
        f"Saved to {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
