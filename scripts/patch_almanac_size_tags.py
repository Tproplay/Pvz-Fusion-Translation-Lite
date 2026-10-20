#!/usr/bin/env python3
"""Ensure all Almanac descriptions in translation-data have size=36 tags for mobile."""

import json
import re
from pathlib import Path

almanac_dir = Path("translation-data/Almanac")

# 1. LawnStringsTranslate
lawn_file = almanac_dir / "LawnStringsTranslate.json"
with lawn_file.open("r", encoding="utf-8") as f:
    lawn = json.load(f)

c_lawn = 0
for p in lawn.get("plants", []):
    inf = p.get("info", "")
    if inf.strip() and not re.search(r"<\s*size\s*=", inf):
        p["info"] = f"<size=36>{inf}</size>"
        c_lawn += 1
    intro = p.get("introduce", "")
    if intro.strip() and not re.search(r"<\s*size\s*=", intro):
        p["introduce"] = f"<align=left><size=36>{intro}</size>"
        c_lawn += 1

print(f"LawnStrings updated fields: {c_lawn}")
with lawn_file.open("w", encoding="utf-8") as f:
    json.dump(lawn, f, indent=4, ensure_ascii=False)

# 2. ZombieStringsTranslate
zomb_file = almanac_dir / "ZombieStringsTranslate.json"
with zomb_file.open("r", encoding="utf-8") as f:
    zomb = json.load(f)

c_zomb = 0
for z in zomb.get("zombies", []):
    inf = z.get("info", "")
    if inf.strip() and not re.search(r"<\s*size\s*=", inf):
        z["info"] = f"<size=36>{inf}</size>"
        c_zomb += 1
    intro = z.get("introduce", "")
    if intro.strip() and not re.search(r"<\s*size\s*=", intro):
        z["introduce"] = f"<align=left><size=36>{intro}</size>"
        c_zomb += 1

print(f"ZombieStrings updated fields: {c_zomb}")
with zomb_file.open("w", encoding="utf-8") as f:
    json.dump(zomb, f, indent=4, ensure_ascii=False)

# 3. DetailStringsTranslate
det_file = almanac_dir / "DetailStringsTranslate.json"
with det_file.open("r", encoding="utf-8") as f:
    det = json.load(f)

c_det = 0
for k, v in det.items():
    if isinstance(v, str) and v.strip() and not re.search(r"<\s*size\s*=", v):
        det[k] = f"<size=36>{v}</size>"
        c_det += 1

print(f"DetailStrings updated fields: {c_det}")
with det_file.open("w", encoding="utf-8") as f:
    json.dump(det, f, indent=4, ensure_ascii=False)

print("Almanac size tags successfully updated!")
