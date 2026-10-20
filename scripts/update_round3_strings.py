#!/usr/bin/env python3
"""Add Round 3 translations for Tactical Modifiers, Conditions, Zombie stats, and UI buttons."""

from __future__ import annotations

import json
from pathlib import Path

ROUND3_EXACT = {
    # Tactical Modifiers (Image 1)
    "前三级免费 · ": "First 3 Tiers Free · ",
    "前三级免费": "First 3 Tiers Free",
    "满阶": "Max Tier",
    "满阶已购买": "Max Tier Purchased",
    "\n点击中栏此词条，可永久解锁该组的满阶战术。": "\nClick this modifier in the middle pane to permanently unlock this set's max-tier tactic.",
    "第 ": "Tier ",
    " 级": "",

    # Conditions & Descriptions (Images 1 & 2)
    "出现条件": "Requirements: ",
    "出现条件：": "Requirements: ",
    "查看完整描述与出现条件": "View Full Description & Requirements",
    "{0} · {1} / {2} 项": "{0} · {1} / {2}",

    # Zombie Almanac stats (Image 3)
    "<color=#3D1400>出怪等级：</color><color=red>{0}</color>\n": "<color=#3D1400>Spawn Level: </color><color=red>{0}</color>\n",
    "<color=#3D1400>出怪权重：</color><color=red>{0}</color>": "<color=#3D1400>Spawn Weight: </color><color=red>{0}</color>",
    "出怪等级：": "Spawn Level: ",
    "出怪等级": "Spawn Level: ",
    "出怪权重：": "Spawn Weight: ",
    "出怪权重": "Spawn Weight: ",
    "出怪等级：{0}": "Spawn Level: {0}",
    "出怪权重：{0}": "Spawn Weight: {0}",
    "出怪等级 {0}": "Spawn Level {0}",
    "出怪权重 {0}": "Spawn Weight {0}",

    # UI buttons / UnityEngine.UI.Text (Image 4 & others)
    "切换关卡组": "Switch Level Group",
    "返回索引": "Back to Index",
    "确认配装": "Confirm Loadout",
    "前往商店": "Go to Shop",
    "确定": "Confirm",
}

ROUND3_REGEXS = {
    r"^(.*?)第\s*(\d+)\s*级(.*)$": "{1}Tier {2}{3}",
    r"^第\s*(\d+)\s*级$": "Tier {1}",
    r"^(.*?)·\s*第\s*(\d+)\s*级\s*·(.*)$": "{1}· Tier {2} ·{3}",
    r"^(.*?)满阶(.*)$": "{1}Max Tier{2}",
    r"^前三级免费\s*·\s*(.*)$": "First 3 Tiers Free · {1}",
    r"^前三级免费$": "First 3 Tiers Free",
    r"^(.*?)·\s*(\d+)\s*/\s*(\d+)\s*项$": "{1}· {2} / {3}",
    r"^(\d+)\s*/\s*(\d+)\s*项$": "{1} / {2}",
    r"^(\d+)\s*项$": "{1} items",
    r"^出怪等级[：:\s]*(\d+)$": "Spawn Level: {1}",
    r"^出怪权重[：:\s]*(\d+)$": "Spawn Weight: {1}",
    r"^<color=([^>]+)>出怪等级[：:]?</color><color=([^>]+)>(\d+)</color>(\s*)$": "<color={1}>Spawn Level: </color><color={2}>{3}</color>{4}",
    r"^<color=([^>]+)>出怪权重[：:]?</color><color=([^>]+)>(\d+)</color>(\s*)$": "<color={1}>Spawn Weight: </color><color={2}>{3}</color>{4}",
}


def main() -> None:
    strings_file = Path("translation-data/Strings/translation_strings.json")
    regexs_file = Path("translation-data/Strings/translation_regexs.json")

    with strings_file.open("r", encoding="utf-8") as f:
        exact_data = json.load(f)
    with regexs_file.open("r", encoding="utf-8") as f:
        regex_data = json.load(f)

    orig_exact_len = len(exact_data)
    exact_data.update(ROUND3_EXACT)
    new_exact_len = len(exact_data)

    orig_regex_len = len(regex_data)
    regex_data.update(ROUND3_REGEXS)
    new_regex_len = len(regex_data)

    with strings_file.open("w", encoding="utf-8") as f:
        json.dump(exact_data, f, ensure_ascii=False, indent=2)
    with regexs_file.open("w", encoding="utf-8") as f:
        json.dump(regex_data, f, ensure_ascii=False, indent=2)

    print(f"Updated translation_strings.json: {orig_exact_len} -> {new_exact_len} (+{new_exact_len - orig_exact_len})")
    print(f"Updated translation_regexs.json: {orig_regex_len} -> {new_regex_len} (+{new_regex_len - orig_regex_len})")


if __name__ == "__main__":
    main()
