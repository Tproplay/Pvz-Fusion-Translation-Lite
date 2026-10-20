#!/usr/bin/env python3
"""Consolidate and organize all translation data into a clean canonical tree.

1. Merges base Teyliu strings, manual translations, and previously hardcoded Python data.
2. Converts regex capture group indexes in templates from 0-based to standard 1-based ({0}->{1}, {1}->{2}).
3. Exports hardcoded Python enums (SynergyType, InvestBuff) to clean JSON files under translation-data/Enums/.
4. Copies and organizes fonts, dumps, almanacs, strings, and textures under translation-data/.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from build_metadata_translation import (
    ANDROID_381_INVEST_ENUM_FIELDS,
    ANDROID_381_SYNERGY_ENUM_FIELDS,
    ANDROID_CONFIRMED_EXACT,
)


def increment_regex_groups(template: str) -> str:
    """Convert {0}->{1}, {1}->{2}, etc. so regex templates use standard 1-based indexing."""
    return re.sub(r"\{(\d+)\}", lambda m: f"{{{int(m.group(1)) + 1}}}", template)


def main() -> int:
    target_data_dir = ROOT / "translation-data"
    source_repo_dir = ROOT / "translation-data" / "4.0.5 repo"

    strings_out = target_data_dir / "Strings"
    almanac_out = target_data_dir / "Almanac"
    dumps_out = target_data_dir / "Dumps"
    enums_out = target_data_dir / "Enums"
    fonts_out = target_data_dir / "Fonts"
    textures_out = target_data_dir / "Textures"

    for d in (strings_out, almanac_out, dumps_out, enums_out, fonts_out, textures_out):
        d.mkdir(parents=True, exist_ok=True)

    print("1. Exporting enums to clean JSON...")
    synergy_map = {src: tgt for _, (src, tgt) in sorted(ANDROID_381_SYNERGY_ENUM_FIELDS.items())}
    (enums_out / "SynergyType.json").write_text(
        json.dumps(synergy_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    invest_map = {src: tgt for _, (src, tgt) in sorted(ANDROID_381_INVEST_ENUM_FIELDS.items())}
    (enums_out / "InvestBuff.json").write_text(
        json.dumps(invest_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print("2. Copying font...")
    src_font = source_repo_dir / "English.ttf"
    if src_font.is_file():
        shutil.copy2(src_font, fonts_out / "English.ttf")

    print("3. Consolidating Dumps...")
    src_dumps = source_repo_dir / "Dumps"
    if src_dumps.is_dir():
        for f in src_dumps.iterdir():
            if f.is_file():
                shutil.copy2(f, dumps_out / f.name)

    print("4. Consolidating Almanac...")
    base_almanac = source_repo_dir / "English" / "Almanac"
    manual_almanac = source_repo_dir / "Manually Translated" / "English" / "Almanac"
    for filename in ("LawnStringsTranslate.json", "ZombieStringsTranslate.json", "DetailStringsTranslate.json", "PlantType.json", "ZombieType.json"):
        src = None
        if (manual_almanac / filename).is_file():
            src = manual_almanac / filename
        elif (base_almanac / filename).is_file():
            src = base_almanac / filename
        if src:
            shutil.copy2(src, almanac_out / filename)

    print("5. Consolidating Textures...")
    base_textures = source_repo_dir / "English" / "Textures"
    manual_textures = source_repo_dir / "Manually Translated" / "English" / "Textures"
    if base_textures.is_dir():
        shutil.copytree(base_textures, textures_out, dirs_exist_ok=True)
    if manual_textures.is_dir():
        shutil.copytree(manual_textures, textures_out, dirs_exist_ok=True)

    print("6. Consolidating Strings and converting regex 0-based to 1-based indexing...")
    base_strings = source_repo_dir / "English" / "Strings"
    manual_strings = source_repo_dir / "Manually Translated" / "English" / "Strings"

    # Merge translation_strings.json
    all_strings = {}
    if (base_strings / "translation_strings.json").is_file():
        all_strings.update(json.loads((base_strings / "translation_strings.json").read_text(encoding="utf-8")))
    if (manual_strings / "translation_strings.json").is_file():
        all_strings.update(json.loads((manual_strings / "translation_strings.json").read_text(encoding="utf-8")))
    # Add previously hardcoded Python exact strings
    all_strings.update(ANDROID_CONFIRMED_EXACT)
    (strings_out / "translation_strings.json").write_text(
        json.dumps(all_strings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # Merge & convert translation_regexs.json
    all_regexs = {}
    if (base_strings / "translation_regexs.json").is_file():
        all_regexs.update(json.loads((base_strings / "translation_regexs.json").read_text(encoding="utf-8")))
    if (manual_strings / "translation_regexs.json").is_file():
        all_regexs.update(json.loads((manual_strings / "translation_regexs.json").read_text(encoding="utf-8")))
    converted_regexs = {pat: increment_regex_groups(repl) for pat, repl in all_regexs.items()}
    (strings_out / "translation_regexs.json").write_text(
        json.dumps(converted_regexs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # Convert customlevel_regexs.json
    if (base_strings / "customlevel_regexs.json").is_file():
        cl_regexs = json.loads((base_strings / "customlevel_regexs.json").read_text(encoding="utf-8"))
        if (manual_strings / "customlevel_regexs.json").is_file():
            cl_regexs.update(json.loads((manual_strings / "customlevel_regexs.json").read_text(encoding="utf-8")))
        conv_cl = {pat: increment_regex_groups(repl) for pat, repl in cl_regexs.items()}
        (strings_out / "customlevel_regexs.json").write_text(
            json.dumps(conv_cl, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    # Copy remaining string files
    for fn in ("customlevel_strings.json", "custom_level_data.json", "travel_buffs.json", "abyss_buffs.json", "tips_fs.json", "tips_iz.json", "changelog.txt"):
        src = (manual_strings / fn) if (manual_strings / fn).is_file() else (base_strings / fn)
        if src.is_file():
            shutil.copy2(src, strings_out / fn)

    print("Consolidation finished successfully!")
    print(f"Total merged exact strings: {len(all_strings)}")
    print(f"Total merged & converted regexes: {len(converted_regexs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
