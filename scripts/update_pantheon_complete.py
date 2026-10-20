#!/usr/bin/env python3
"""Add comprehensive Pantheon and Almanac translations to translation files."""

from __future__ import annotations

import json
from pathlib import Path

NEW_EXACT_STRINGS = {
    # Generic format templates & fragments
    "{0}获得{1:F0}%": "{0} gains {1:F0}% ",
    "独立伤害增幅": "Independent Damage Bonus",
    "速度增幅": "Speed Bonus",
    "伤害增幅": "Damage Bonus",
    "获得了{0:F0}%力量增幅": "Gained {0:F0}% Power bonus",
    "获得了{0:F0}%速度增幅": "Gained {0:F0}% Speed bonus",
    "当前增幅：{0:F0}%": "Current bonus: {0:F0}%",
    "（普通品质基准，实际增幅随品质变化）。": " (Based on Common quality; actual bonus scales with quality).",
    "普通品质基准,实际增幅随品质变化。": " (Based on Common quality; actual bonus scales with quality).",
    "普通品质基准，实际效果随品质及当前构筑变化。": "Common quality baseline; actual effect scales with quality and current build.",
    " 普通品质基准,实际增幅随品质变化。": " (Based on Common quality; actual bonus scales with quality).",
    " 普通品质基准，实际效果随品质及当前构筑变化。": " (Common quality baseline; actual effect scales with quality and current build).",

    # Currency & Badges
    "诸神币": "Pantheon Coins",
    "诸神币 ": "Pantheon Coins ",
    "诸神币 {0}": "Pantheon Coins: {0}",
    "诸神币: {0}": "Pantheon Coins: {0}",
    "诸神币:{0}": "Pantheon Coins: {0}",
    "诸神币 2000": "Pantheon Coins 2000",
    "诸神币：0": "Pantheon Coins: 0",
    "当前诸神币：0": "Current Pantheon Coins: 0",
    "【诸神币】": "[Pantheon Coins]",
    "50诸神币": "50 Pantheon Coins",
    "100诸神币": "100 Pantheon Coins",
    "300诸神币": "300 Pantheon Coins",
    " · 50诸神币": " · 50 Pantheon Coins",
    " · 未购买 · {0}诸神币": " · Not Purchased · {0} Pantheon Coins",
    "满阶未购买 · {0}诸神币": "Max Tier Not Purchased · {0} Pantheon Coins",
    "基础": "Base",
    "100币": "100 Coins",
    "50币": "50 Coins",
    "专家": "Specialist",
    "终端": "Terminal",
    "质变": "Mutation",
    "随机品质": "Random Quality",

    # Almanac headers & structure
    "基础植物 · ": "Base Plant · ",
    "终端植物": "Terminal Plant",
    "终端植物 · ": "Terminal Plant · ",
    "进化途中的植物": "Evolving Plant",
    "{0} · 最多 {1} 次{2}": "{0} · Max {1} times{2}",
    "{0} · 最多 {1} 次": "{0} · Max {1} times",
    "最多 {0} 次": "Max {0} times",
    "最多{0}次": "Max {0} times",
    "最多 {1} 次": "Max {1} times",
    "最多{1}次": "Max {1} times",
    "最多 1000 次": "Max 1000 times",
    "最多 50 次": "Max 50 times",
    "最多 10 次": "Max 10 times",
    "最多 1 次": "Max 1 time",
    "{0} 条进化路线 · 点击卡牌查看词条": "{0} Evolution Paths · Click card to view modifiers",
    "7 条进化路线 · 点击卡牌查看词条": "7 Evolution Paths · Click card to view modifiers",
    "可获得词条  {0} 项": "Available Modifiers: {0}",
    "可获得词条 {0} 项": "Available Modifiers: {0}",
    "可获得词条 5 项": "Available Modifiers: 5",
    "可获得词条  5 项": "Available Modifiers: 5",
    "{0} · 可选词条 {1} 项\n{2}": "{0} · Available Modifiers: {1}\n{2}",
    "路线 {0}  /  {1}": "Path {0} / {1}",
    "路线 {0} / {1}": "Path {0} / {1}",
    "\n同时解锁首条进化路线：\n": "\nAlso unlocks the first evolution route:\n",
    "暂无基础植物": "No base plant available",
    "该专家植物暂无专属词条": "This specialist plant has no exclusive modifiers",
    "该终端植物暂无专属词条": "This terminal plant has no exclusive modifiers",
    "请先解锁这条路线的基础植物。": "Please unlock the base plant for this route first.",
    "搜索专家植物": "Search Specialist Plant",
    "尚未解锁的专家植物": "Locked Specialist Plant",
    "尚未解锁的词条": "Locked Modifier",
    "没有匹配的专家植物": "No matching specialist plants",
    "没有匹配的战术": "No matching tactics",
    "没有匹配的词条": "No matching modifiers",

    # Unlocking & Prompts
    "专家植物可直接使用，无需购买。": "Specialist plants can be used directly without purchase.",
    "仅战术满阶词条需要购买，1至3级可直接使用。": "Only max-tier tactical modifiers require purchase; Tiers 1-3 can be used directly.",
    "是否消耗 {0} 诸神币永久解锁“{1}”？\n\n{2}": "Spend {0} Pantheon Coins to permanently unlock \"{1}\"?\n\n{2}",
    "是否消耗 {0} 诸神币解锁植物“{1}”？": "Spend {0} Pantheon Coins to unlock plant \"{1}\"?",
    "是否消耗 {0} 诸神币解锁该升级路线？\n{1}": "Spend {0} Pantheon Coins to unlock this upgrade route?\n{1}",
    "是否消耗 100 诸神币解锁该植物？": "Spend 100 Pantheon Coins to unlock this plant?",
    "是否消耗 50 诸神币解锁该升级路线？": "Spend 50 Pantheon Coins to unlock this upgrade route?",
    "点击路线中的卡牌，解锁后查看植物词条": "Click cards in the route to unlock and view plant modifiers",
    "沿路线继续进化，点击终端卡牌查看可获得的词条。": "Continue evolving along the route. Click terminal cards to view available modifiers.",
    "解锁升级路线": "Unlock Upgrade Route",
    "解锁后可查看植物词条": "Unlock to view plant modifiers",
    "解锁后可查看词条效果": "Unlock to view modifier effects",
    "解锁后可查看词条效果。": "Unlock to view modifier effects.",
    "解锁后查看详情": "Unlock to view details",
    "解锁满阶战术": "Unlock Max-Tier Tactics",
    "该升级路线不在可解锁目录中。": "This upgrade route is not in the unlock catalog.",
    "该升级路线已经解锁。": "This upgrade route is already unlocked.",
    "该战术满阶已经解锁。": "This max-tier tactic is already unlocked.",
    "该植物不在可解锁目录中。": "This plant is not in the unlock catalog.",
    "该植物已经解锁。": "This plant is already unlocked.",
    "诸神币不足": "Not enough Pantheon Coins",
    "诸神币不足，还需要 {0} 诸神币": "Not enough Pantheon Coins. Need {0} more Pantheon Coins",
    "诸神币不足，需要 {0} 诸神币。": "Not enough Pantheon Coins. Requires {0} Pantheon Coins.",
    "从已购买的植物中任选一个\n更多植物可前往「图鉴 → 诸神图鉴」购买解锁": "Choose from purchased plants.\nMore plants can be unlocked in \"Almanac → The Gods Almanac\"",
    "当前没有可选词条，可继续战斗\n更多植物和路线可前往「图鉴 → 诸神图鉴」购买解锁": "No modifiers currently available, continue battle.\nMore plants and routes can be unlocked in \"Almanac → The Gods Almanac\"",
    "获取更多植物：图鉴 → 诸神图鉴\n在图鉴中消耗诸神币可购买\n购买一次之后不再显示该界面": "Get more plants: Almanac → The Gods Almanac\nCan be purchased with Pantheon Coins\nThis screen will not appear again after purchase",
    "同一植物只能选择一个质变词条。": "Only one mutation modifier can be chosen per plant.",
    "添加诸神模式植物配置后将自动显示": "Will be displayed automatically once Pantheon mode plant configuration is added",

    # Reincarnation & Round rewards
    "1次轮回，最终面临僵王的挑战\n通关获得75诸神币\n\n": "1 reincarnation; final boss: Dr. Zomboss\nClearing awards 75 Pantheon Coins\n\n",
    "2次轮回，最终面临黄金僵王的挑战\n通关获得100诸神币\n\n": "2 reincarnations; final boss: Golden Dr. Zomboss\nClearing awards 100 Pantheon Coins\n\n",
    "最终面临大帅的挑战\n通关获得50诸神币\n\n": "Final challenge: the Archduke\nClearing awards 50 Pantheon Coins\n\n",
    "无尽模式，你能撑到第几轮？\n每完成一轮获得25诸神币\n\n最大轮数：{0}": "Endless Mode: how many rounds can you survive?\nClearing each round awards 25 Pantheon Coins\n\nMax Rounds: {0}",
    "本局获得：{0} 诸神币": "Earned this run: {0} Pantheon Coins",
    "第{0}轮完成，获得{1}诸神币": "Round {0} complete, awarded {1} Pantheon Coins",
    "每完成一轮获得25诸神币，未完成的轮次不发放奖励。": "Clearing each round awards 25 Pantheon Coins; incomplete rounds grant no reward.",
    "主动放弃不发放诸神币。": "Voluntary surrender does not grant Pantheon Coins.",
    "当前模式未配置诸神币奖励。": "No Pantheon Coin rewards configured for the current mode.",
    "通关奖励已存入诸神存档。": "Clear rewards saved to Pantheon save file.",

    # Error handling & persistence
    "解锁保存失败，诸神币未扣除，请重试。": "Failed to save unlock. Pantheon Coins were not deducted, please try again.",
    "诸神币保存失败，将自动重试：": "Failed to save Pantheon Coins, retrying automatically: ",
    "诸神币暂未保存，正在等待重试。": "Pantheon Coins not yet saved, awaiting retry.",
    "诸神老玩家补偿保存失败，将在下次读档时重试：": "Failed to save veteran player compensation, will retry on next load: ",
    "当前无法保存解锁，请稍后重试。": "Cannot save unlock at this time, please try again later.",
    "正在保存本次解锁，请稍后再试。": "Saving unlock in progress, please try again later.",
    "抽取词条时发生错误：": "Error occurred while drawing modifiers: ",
    "诸神进化路线存在循环：{0}。": "The Gods evolution route has a loop: {0}.",
    "诸神进化路线缺少植物配置：{0}。": "The Gods evolution route is missing plant configuration: {0}.",

    # Groups from ShootingAlmanacIndex
    "业火": "Hellfire",
    "烈阳": "Blazing Sun",
    "战锤": "Warhammer",
    "明月": "Bright Moon",
    "天罚": "Heaven's Wrath",
    "全能": "All-Mighty",
    "宝藏": "Treasure",
    "硬化": "Hardening",
    "木桩": "Wooden Post",
    "光棱": "Prism",
    "交易": "Trade",
    "裂空": "Void Rift",
}

NEW_REGEXS = {
    r"^诸神币[：:\s]*(\d+)$": "Pantheon Coins: {1}",
    r"^最多\s*(\d+)\s*次$": "Max {1} times",
    r"^(.*?)·\s*最多\s*(\d+)\s*次(.*)$": "{1}· Max {2} times{3}",
    r"^(.*?)获得\s*(\d+(?:\.\d+)?|\{.*?\})%独立伤害增幅(.*)$": "{1} gains {2}% independent damage increase {3}",
    r"^(.*?)获得\s*(\d+(?:\.\d+)?|\{.*?\})%速度增幅(.*)$": "{1} gains {2}% speed increase {3}",
    r"^路线\s*(\d+)\s*/\s*(.*?)\s*·\s*(\d+)\s*诸神币$": "Path {1} / {2} · {3} Pantheon Coins",
    r"^路线\s*(\d+)\s*/\s*(.*?)$": "Path {1} / {2}",
    r"^(\d+)\s*条进化路线\s*·\s*点击卡牌查看词条$": "{1} Evolution Paths · Click card to view modifiers",
    r"^可获得词条\s*(\d+)\s*项$": "Available Modifiers: {1}",
}


def main() -> None:
    strings_file = Path("translation-data/Strings/translation_strings.json")
    regexs_file = Path("translation-data/Strings/translation_regexs.json")

    with strings_file.open("r", encoding="utf-8") as f:
        exact_data = json.load(f)
    with regexs_file.open("r", encoding="utf-8") as f:
        regex_data = json.load(f)

    orig_exact_len = len(exact_data)
    exact_data.update(NEW_EXACT_STRINGS)
    new_exact_len = len(exact_data)

    orig_regex_len = len(regex_data)
    regex_data.update(NEW_REGEXS)
    new_regex_len = len(regex_data)

    with strings_file.open("w", encoding="utf-8") as f:
        json.dump(exact_data, f, ensure_ascii=False, indent=2)
    with regexs_file.open("w", encoding="utf-8") as f:
        json.dump(regex_data, f, ensure_ascii=False, indent=2)

    print(f"Updated translation_strings.json: {orig_exact_len} -> {new_exact_len} (+{new_exact_len - orig_exact_len})")
    print(f"Updated translation_regexs.json: {orig_regex_len} -> {new_regex_len} (+{new_regex_len - orig_regex_len})")


if __name__ == "__main__":
    main()
