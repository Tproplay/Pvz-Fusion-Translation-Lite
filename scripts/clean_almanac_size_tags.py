#!/usr/bin/env python3
"""Strip all size tags from Almanac JSON files so both PC and Android use clean 18pt font."""

import json
import re
from pathlib import Path

almanac_dir = Path("translation-data/Almanac")
size_re = re.compile(r"</?size(?:=[^>]+)?>")

# 1. LawnStringsTranslate
lawn_file = almanac_dir / "LawnStringsTranslate.json"
with lawn_file.open("r", encoding="utf-8") as f:
    lawn = json.load(f)

c_lawn = 0
for p in lawn.get("plants", []):
    for k in ("introduce", "info", "cost", "description"):
        if k in p and isinstance(p[k], str) and size_re.search(p[k]):
            p[k] = size_re.sub("", p[k])
            c_lawn += 1

print(f"LawnStrings tags stripped: {c_lawn}")
with lawn_file.open("w", encoding="utf-8") as f:
    json.dump(lawn, f, indent=4, ensure_ascii=False)

# 2. ZombieStringsTranslate
zomb_file = almanac_dir / "ZombieStringsTranslate.json"
with zomb_file.open("r", encoding="utf-8") as f:
    zomb = json.load(f)

c_zomb = 0
for z in zomb.get("zombies", []):
    for k in ("introduce", "info", "description"):
        if k in z and isinstance(z[k], str) and size_re.search(z[k]):
            z[k] = size_re.sub("", z[k])
            c_zomb += 1

print(f"ZombieStrings tags stripped: {c_zomb}")
with zomb_file.open("w", encoding="utf-8") as f:
    json.dump(zomb, f, indent=4, ensure_ascii=False)

# 3. DetailStringsTranslate
det_file = almanac_dir / "DetailStringsTranslate.json"
with det_file.open("r", encoding="utf-8") as f:
    det = json.load(f)

c_det = 0
for k, v in det.items():
    if isinstance(v, str) and size_re.search(v):
        det[k] = size_re.sub("", v)
        c_det += 1

print(f"DetailStrings tags stripped: {c_det}")
with det_file.open("w", encoding="utf-8") as f:
    json.dump(det, f, indent=4, ensure_ascii=False)

print("All Almanac size tags stripped successfully!")
