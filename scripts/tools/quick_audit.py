#!/usr/bin/env python3
"""Quick translation auditor for PvZ Fusion.

Checks:
1. Pending untranslated screenshots in translation-data/untranslated_screenshot/
2. Health and integrity of translation JSON files (valid JSON syntax, placeholder checks)
3. Build status: timestamp and CJK counts in the PC build

Usage:
    python scripts/tools/quick_audit.py
"""

from __future__ import annotations

import glob
import json
import os
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCREENSHOTS_DIR = ROOT / "translation-data/untranslated_screenshot"
STRINGS_DIR = ROOT / "translation-data/Strings"
PC_BUILD_DIR = ROOT / "build/PC_PVZ-Fusion-4.1"

CJK_RE = re.compile(r"[\u3400-\u9fff]")
CSHARP_FORMAT_RE = re.compile(r"\{(\d+)(?:,[^}:]+)?(?::[^}]+)?\}")


def audit_screenshots() -> list[Path]:
    if not SCREENSHOTS_DIR.is_dir():
        return []
    return list(SCREENSHOTS_DIR.glob("*.png")) + list(SCREENSHOTS_DIR.glob("*.jpg"))


def audit_json_files() -> dict:
    results = {}
    for jf in STRINGS_DIR.glob("*.json"):
        try:
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)
            count = len(data) if isinstance(data, (dict, list)) else 0
            mismatches = 0
            if isinstance(data, dict) and "regex" not in jf.name:
                for k, v in data.items():
                    if isinstance(k, str) and isinstance(v, str):
                        sk = set(CSHARP_FORMAT_RE.findall(k))
                        sv = set(CSHARP_FORMAT_RE.findall(v))
                        if sk != sv:
                            mismatches += 1
            results[jf.name] = {"count": count, "valid": True, "placeholder_mismatches": mismatches}
        except Exception as e:
            results[jf.name] = {"valid": False, "error": str(e)}
    return results


def audit_build() -> dict:
    meta_path = PC_BUILD_DIR / "PlantsVsZombiesRH_Data/il2cpp_data/Metadata/global-metadata.dat"
    bundle_path = PC_BUILD_DIR / "PlantsVsZombiesRH_Data/data.unity3d"
    res = {}
    if meta_path.exists():
        data = meta_path.read_bytes()
        str_offset, str_size = struct.unpack_from("<II", data, 8)
        lit_offset, lit_size = struct.unpack_from("<II", data, 16)
        count = str_size // 8
        cjk_count = 0
        for i in range(count):
            length, rel_offset = struct.unpack_from("<II", data, str_offset + i * 8)
            abs_offset = lit_offset + rel_offset
            if abs_offset + length <= len(data):
                try:
                    s = data[abs_offset : abs_offset + length].decode("utf-8")
                    if CJK_RE.search(s):
                        cjk_count += 1
                except:
                    pass
        res["metadata"] = {"exists": True, "total_literals": count, "cjk_literals": cjk_count}
    else:
        res["metadata"] = {"exists": False}

    if bundle_path.exists():
        res["bundle"] = {"exists": True, "size_mb": round(bundle_path.stat().st_size / (1024 * 1024), 2)}
    else:
        res["bundle"] = {"exists": False}
    return res


def main() -> int:
    print("=" * 60)
    print("PvZ Fusion Translation — Quick Health & Status Audit")
    print("=" * 60)

    # 1. Screenshots
    shots = audit_screenshots()
    print(f"\n[1] Pending Screenshots in translation-data/untranslated_screenshot/: {len(shots)}")
    for s in shots:
        print(f"  - {s.name}")
    if not shots:
        print("  (None — no pending screenshot work)")

    # 2. JSON Files
    print("\n[2] Translation Dictionaries Integrity:")
    j_res = audit_json_files()
    all_ok = True
    for fname, info in j_res.items():
        if not info.get("valid"):
            print(f"  [FAIL] {fname}: {info.get('error')}")
            all_ok = False
        else:
            mismatches = info.get("placeholder_mismatches", 0)
            status = "OK" if mismatches == 0 else f"WARN ({mismatches} placeholder mismatches)"
            print(f"  [{status}] {fname}: {info['count']} entries")
    if all_ok:
        print("  All JSON files are structurally sound.")

    # 3. Build Status
    print("\n[3] Current PC Build Status:")
    b_res = audit_build()
    if b_res["metadata"]["exists"]:
        meta = b_res["metadata"]
        print(f"  global-metadata.dat: {meta['total_literals']} literals ({meta['cjk_literals']} CJK remaining)")
    else:
        print("  global-metadata.dat: NOT FOUND")

    if b_res["bundle"]["exists"]:
        print(f"  data.unity3d: {b_res['bundle']['size_mb']} MB")
    else:
        print("  data.unity3d: NOT FOUND")

    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
