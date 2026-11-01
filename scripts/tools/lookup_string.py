#!/usr/bin/env python3
"""High-speed string locator and diagnostic tool for PvZ Fusion translation.

Searches:
1. global-metadata.dat.orig (IL2CPP string literals)
2. translation-data/Strings/ (active translation dictionaries and regexes)
3. translation-data/Dumps/ (source data dumps)

Usage:
    python scripts/tools/lookup_string.py "进入商店"
    python scripts/tools/lookup_string.py --query "轮间商店" --json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import struct
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
METADATA_PATH = ROOT / "build/PC_PVZ-Fusion-4.1/PlantsVsZombiesRH_Data/il2cpp_data/Metadata/global-metadata.dat.orig"
STRINGS_DIR = ROOT / "translation-data/Strings"
DUMPS_DIR = ROOT / "translation-data/Dumps"

CSHARP_FORMAT_RE = re.compile(r"\{(\d+)(?:,[^}:]+)?(?::[^}]+)?\}")
XML_TAG_RE = re.compile(r"<[^>]+>")


def load_metadata_literals(meta_file: Path) -> list[str]:
    if not meta_file.exists():
        return []
    data = meta_file.read_bytes()
    if len(data) < 24:
        return []
    magic = struct.unpack_from("<I", data, 0)[0]
    if magic != 0xFAB11BAF:
        return []
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


def load_all_json_files(directory: Path) -> dict[str, dict]:
    res = {}
    if not directory.exists():
        return res
    for f in directory.glob("*.json"):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                res[f.name] = json.load(fp)
        except Exception:
            pass
    return res


def analyze_placeholders(text: str) -> dict:
    csharp_fields = set(CSHARP_FORMAT_RE.findall(text))
    xml_tags = XML_TAG_RE.findall(text)
    newlines = []
    if "\r\r\n" in text:
        newlines.append("CRCRLF")
    elif "\r\n" in text:
        newlines.append("CRLF")
    elif "\n" in text:
        newlines.append("LF")
    return {
        "format_placeholders": sorted(list(csharp_fields), key=int),
        "xml_tags": xml_tags,
        "newlines": newlines,
    }


def search_all(query: str, exact: bool = False) -> dict:
    res = {
        "query": query,
        "metadata_matches": [],
        "strings_matches": {},
        "regex_matches": [],
        "dump_matches": {},
    }

    # 1. Metadata
    literals = load_metadata_literals(METADATA_PATH)
    seen_meta = set()
    for s in literals:
        if (query == s if exact else query in s) and s not in seen_meta:
            seen_meta.add(s)
            res["metadata_matches"].append({
                "literal": s,
                "analysis": analyze_placeholders(s),
            })

    # 2. Translation Strings
    active_strings = load_all_json_files(STRINGS_DIR)
    for fname, payload in active_strings.items():
        if fname in ("translation_regexs.json", "customlevel_regexs.json"):
            for pat, repl in payload.items():
                if query in pat or query in repl:
                    res["regex_matches"].append({"file": fname, "pattern": pat, "replacement": repl})
                else:
                    # Test if pattern matches query
                    try:
                        if re.search(pat, query):
                            res["regex_matches"].append({"file": fname, "pattern": pat, "replacement": repl, "matches_query": True})
                    except Exception:
                        pass
        elif isinstance(payload, dict):
            matched_pairs = {}
            for k, v in payload.items():
                if isinstance(v, str):
                    if query == k if exact else (query in k or query in v):
                        matched_pairs[k] = v
                elif isinstance(v, dict):
                    # Check nested like travel_buffs
                    for sub_k, sub_v in v.items():
                        if isinstance(sub_v, dict):
                            name = sub_v.get("name", "")
                            desc = sub_v.get("desc", "")
                            if (query in name or query in desc) if not exact else (query == name or query == desc):
                                matched_pairs[f"{sub_k}:{name}"] = desc
            if matched_pairs:
                res["strings_matches"][fname] = matched_pairs

    # 3. Dumps
    dumps = load_all_json_files(DUMPS_DIR)
    for fname, payload in dumps.items():
        found = False
        serialized = json.dumps(payload, ensure_ascii=False)
        if query in serialized:
            res["dump_matches"][fname] = True

    return res


def print_human_report(res: dict) -> None:
    q = res["query"]
    print("=" * 60)
    print(f"STRING LOOKUP REPORT FOR: {repr(q)}")
    print("=" * 60)

    # Metadata
    meta = res["metadata_matches"]
    print(f"\n[1] IL2CPP Metadata Literals ({len(meta)} found):")
    if not meta:
        print("  (None found)")
    else:
        for idx, m in enumerate(meta[:10], 1):
            s = m["literal"]
            analysis = m["analysis"]
            print(f"  {idx}. {repr(s)}")
            if analysis["format_placeholders"]:
                print(f"     Format parameters: {analysis['format_placeholders']}")
            if analysis["xml_tags"]:
                print(f"     XML tags: {analysis['xml_tags']}")
        if len(meta) > 10:
            print(f"  ... and {len(meta) - 10} more.")

    # Active Strings
    str_matches = res["strings_matches"]
    print(f"\n[2] Active Translations in Strings/ ({sum(len(v) for v in str_matches.values())} entries):")
    if not str_matches:
        print("  (None found — string is UNTRANSLATED in exact dictionaries)")
    else:
        for fname, entries in str_matches.items():
            print(f"  In {fname}:")
            for k, v in list(entries.items())[:5]:
                print(f"    - {repr(k)} -> {repr(v)}")
            if len(entries) > 5:
                print(f"    ... and {len(entries) - 5} more.")

    # Regexes
    regexes = res["regex_matches"]
    print(f"\n[3] Matching Regexes ({len(regexes)} found):")
    if not regexes:
        print("  (None found)")
    else:
        for r in regexes:
            flag = " [MATCHES QUERY]" if r.get("matches_query") else ""
            print(f"  Pattern: {repr(r['pattern'])}{flag}")
            print(f"  Replacement: {repr(r['replacement'])}")

    # Dumps
    dm = res["dump_matches"]
    print(f"\n[4] Found in Dumps: {', '.join(dm.keys()) if dm else '(None)'}")
    print("=" * 60)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Text to search for")
    parser.add_argument("--exact", action="store_true", help="Match exact text only")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    res = search_all(args.query, exact=args.exact)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print_human_report(res)
    return 0


if __name__ == "__main__":
    sys.exit(main())
