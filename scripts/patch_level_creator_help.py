#!/usr/bin/env python3
"""Translate LevelCreatorHelp TextAsset and add custom level editor UI strings."""

from __future__ import annotations

import json
from pathlib import Path

HELP_TOPICS = [
    {
        "title": "Creating Your First Level",
        "body": (
            "<b>Start with a basic playable level first, then add special rules.</b>\n\n"
            "1. In Basic Settings, fill in Level Name and Number, select a Map, and set Starting Sun and Total Waves. "
            "(Input range: 10–100 waves; start with 10 for testing).\n"
            "2. In \"Spawn Settings\", select available zombie types, then go to the Wave Spawns page to configure fixed enemy waves.\n"
            "3. On the Cards page, configure available plants and seed slots. After modifying costs and cooldowns, click Save Changes on that page.\n"
            "4. Set the Win Condition. For your first level, use standard Victory; keep special modes disabled for now.\n"
            "5. Click \"Save & Generate Level\" at the bottom, then start the game to test planting, zombie spawns, and level completion.\n"
            "6. Once the basic level works properly, go to the Events page to add prompts, timed sun, reward choices, and custom rules.\n\n"
            "<b>Event nodes are optional</b>\n"
            "Basic levels do not require nodes. Only use Event Rules when you need \"something to happen under specific conditions\".\n\n"
            "<b>Recommended first exercise</b>\n"
            "On the Events page, click \"Add Rule Template\" and select \"Gain Sun Every 5s\". "
            "Select the nodes to view descriptions and edit values, then save and test."
        ),
    },
    {
        "title": "Map, Rules & Win Conditions",
        "body": (
            "<b>The map determines the battlefield; rules determine the gameplay.</b>\n\n"
            "Basic Settings: Level Name, Number, Map, Starting Sun, and Total Waves.\n"
            "Modes Page: Disable natural spawns, sky sun, lawn mowers, or enable special modes like Conveyor, Rain of Seeds, I, Zombie, etc.\n"
            "Victory Page: Choose Standard Victory or I, Zombie Victory.\n\n"
            "<b>Tips for beginners:</b>\n"
            "Start by adjusting only starting sun and spawns. Test after toggling each mode switch to see how it affects gameplay.\n"
            "\"Disable Natural Spawns\" stops regular wave enemies; if enabled, you must script enemy spawns manually."
        ),
    },
    {
        "title": "Cards & Zombie Spawns",
        "body": (
            "<b>Card Settings</b>\n"
            "Configure pre-selected cards, seed slots, and custom costs/cooldowns. "
            "Click Save Changes on the page after editing before saving the whole level; unsaved input field edits will not persist.\n\n"
            "<b>Two Spawn Settings</b>\n"
            "\"Spawn Settings\" selects zombie types for random spawning.\n"
            "\"Wave Spawns\" scripts specific enemies and lanes per wave.\n"
            "Both serve different purposes. If unexpected enemies appear, verify random candidates, wave spawns, and event triggers."
        ),
    },
    {
        "title": "Pre-placed Plants & Setup",
        "body": (
            "<b>Pre-placed Plants & Vases</b>\n"
            "Enter the setup battlefield to place plants or vases. Exit to apply changes to your draft, then save the level. "
            "Pre-placed plants exist before event graphs start, so \"On Plant\" will not trigger for them. "
            "To process them, use \"Level Start → Get All Plants on Lawn → Iterate Plant List\".\n\n"
            "<b>Planting rules still apply</b>\n"
            "Water, roof tiles, plant carriers, and occupied tiles affect creation. "
            "\"Create Plant\" checks standard rules by default; connect error-handling branches if creation fails."
        ),
    },
    {
        "title": "How to Connect Nodes",
        "body": (
            "<b>A rule = When (Trigger) → Condition (Check) → Action (Do)</b>\n\n"
            "Example: \"Show tip when Wave 5 begins\".\n"
            "Level Wave Advances → Branch → Show Text defines execution order.\n"
            "Wave Count → Int Comparison (= 5) → Branch Condition provides data.\n\n"
            "<b>Two Wire Types</b>\n"
            "Execution flow: Connects Trigger outputs to Trigger inputs. Without it, actions will not run.\n"
            "Data wires: Passes numbers, text, plant objects, etc. Connecting data alone does not trigger actions.\n"
            "Drag from right-side outputs to left-side inputs."
        ),
    },
    {
        "title": "Follow-Along: Timed Sun",
        "body": (
            "<b>Goal: After level starts, gain 25 Sun every 5 seconds.</b>\n\n"
            "Method 1: Events page → Add Rule Template → \"Gain Sun Every 5s\". "
            "The template will place pre-wired nodes automatically.\n\n"
            "Method 2: Manual setup.\n"
            "1. Right-click to add \"Level Officially Starts\", \"Timer Switch\", and \"Add Sun\".\n"
            "2. Connect Level Start \"Trigger\" to Timer Switch \"Trigger\".\n"
            "3. Connect Timer Switch \"Periodic Event\" to Add Sun \"Trigger\".\n"
            "4. Select Timer Switch, click \"Enter Input Value\", set interval to 5.\n"
            "5. Select Add Sun, set Sun amount to 25.\n"
            "6. Click \"Verify Connections\", ensure no errors, then save and test."
        ),
    },
    {
        "title": "How to Use the Toolbar",
        "body": (
            "<b>The top bar contains the Event Rule Tools.</b>\n"
            "It helps you build, edit, and check rules; it does not add effects to the level on its own.\n\n"
            "<b>Common Actions:</b>\n"
            "Add Rule Template: Inserts pre-wired rule snippets into the canvas.\n"
            "Node Description: Select a node to view its function, port specs, and examples.\n"
            "Enter Input Value: Directly enter unconnected inputs (delay seconds, sun count, etc.).\n"
            "Verify Connections: Checks for missing nodes, type mismatches, and infinite loops.\n"
            "Undo / Redo: Revert mistakes or reapply edits."
        ),
    },
    {
        "title": "Saving, Testing & Debugging",
        "body": (
            "<b>Three types of saving:</b>\n"
            "Page \"Save Changes\": Submits local edits on that page (cards, spawns, etc.).\n"
            "\"Save Node Draft\": Backs up the event graph for node editing recovery.\n"
            "Bottom \"Save & Generate Level\": Exports the complete level including event graph and all page settings.\n\n"
            "<b>Testing Checklist:</b>\n"
            "Can you pick cards, plant, and fight zombies? Do waves advance? Do win/loss triggers work? "
            "Do events fire at the right time? Do one-time rewards repeat? "
            "When delayed target plants die, does logic handle it cleanly? "
            "Exit and re-enter once to ensure counters reset."
        ),
    },
    {
        "title": "What's New in This Update",
        "body": (
            "<b>New Capabilities:</b>\n\n"
            "1. Insert templates directly (\"Wave 5 Tip\", \"5s Timed Sun\", \"Pick 1 of 3 Rewards\") to skip repetitive node wiring.\n"
            "2. Use Phase nodes to organize combat and reward flows; use \"Run Once\" to avoid duplicate rewards.\n"
            "3. Name targets on the lawn (e.g. \"Boss\") to reference them elsewhere; listen for fusions, boss HP thresholds, or check plant layers.\n"
            "4. Use dedicated Reward Selection nodes for 3-choice menus, preventing wire errors.\n"
            "5. Undo/Redo, Input Value Entry, Node Descriptions, and Connection Checking make debugging much easier."
        ),
    },
    {
        "title": "Strings, Lists & Objects",
        "body": (
            "Level Variables now include \"+ String\" and \"+ List\". Strings support read/write and conversion. "
            "Lists support editing initial values for ints, floats, booleans, strings, plant types, zombie types, and objects. "
            "Up to 512 items per list (8 per page, 0-indexed).\n\n"
            "Use matching list nodes for Append, Insert, Replace, Get, and Find. "
            "Find returns first index and contains bool (-1 if not found). Deletion shifts elements left; cloning creates independent elements.\n\n"
            "Object Binding gives lawn entities queryable names. Strings match the bound name; objects are acquired upon entity creation. "
            "If target entity dies or is dug up, subsequent calls evaluate to invalid targets."
        ),
    },
    {
        "title": "Combat Rule Limitations",
        "body": (
            "Mode Settings now includes \"Zombie In-House Defeat\" (enabled by default; older levels retain default rules). "
            "Disabling lets events handle win/loss conditions; other defeat conditions (e.g. protect target) remain active.\n\n"
            "Card Advanced Mode → Full Stats: Customize HP, damage, intervals, armor, etc. (applies only to current level; must save level).\n\n"
            "Zombie spawn & movement supports fractional columns (e.g. 2.5 is between columns 3 and 4). If left blank, defaults to integer lanes.\n\n"
            "Wait Condition and Loop Until Condition re-evaluate periodically (default 0.1s); loops do not freeze frames and terminate cleanly on phase change or level exit."
        ),
    },
]

NEW_STRINGS = {
    # Image 1: Mode button
    "经典塔防模式": "Classic Tower Defense Mode",

    # Image 2: Guide titles & modal
    "第一次做关卡": "Creating Your First Level",
    "地图、规则与胜负": "Map, Rules & Win Conditions",
    "卡牌与出怪": "Cards & Zombie Spawns",
    "布置植物与特殊设置": "Pre-placed Plants & Setup",
    "节点怎么连接": "How to Connect Nodes",
    "跟做：定时给阳光": "Follow-Along: Timed Sun",
    "跟做 定时给阳光": "Follow-Along: Timed Sun",
    "工具栏怎么用": "How to Use the Toolbar",
    "保存、试玩与排错": "Saving, Testing & Debugging",
    "这次增加了什么": "What's New in This Update",
    "字符串、列表与对象": "Strings, Lists & Objects",
    "新增战斗规则的使用边界": "Combat Rule Limitations",
    "滚轮或拖动右侧滚动条阅读 · Esc关闭 · 阅读指南不会修改关卡": "Scroll or drag the scrollbar to read · Esc to Close · Reading the guide will not modify the level",
    "滚轮或拖动右侧滚动条阅读 · Esc关闭": "Scroll or drag the scrollbar to read · Esc to Close",
    "阅读指南不会修改关卡": "Reading the guide will not modify the level",
    "先做一关能正常游玩的普通关，再加特殊规则。": "Start with a basic playable level first, then add special rules.",
    "先做一关能正常游玩的普通关,再加特殊规则。": "Start with a basic playable level first, then add special rules.",

    # Image 3: Rule template popup
    "事件规则工具  ·  ": "Event Rule Tool · ",
    "事件规则工具 · 先添加规则模版 选中节点看说明、改数值 检查连线 保存并试玩": "Event Rule Tool · Add rule templates first, select nodes to view info/edit values, verify connections, then save & test",
    "先添加规则模板 → 选中节点看说明、改数值 → 检查连线 → 保存并试玩": "Add rule templates first → Select nodes to view info/edit values → Verify connections → Save & test",
    "规则模板：插入副本，各次插入的变量相互独立": "Rule Templates: Insert copy; variables in each instance are independent",
    "规则模版 插入副本，各次插入的变量相互独立": "Rule Templates: Insert copy; variables in each instance are independent",
    "规则模板": "Rule Templates",
    "规则模版": "Rule Templates",
    "每5秒获得阳光": "Gain Sun Every 5s",
    "清场后三选一奖励": "Choose 1 of 3 Rewards After Clear",
    "我的规则": "My Rule",
    "保存选中节点为模板": "Save Selected Nodes as Template",
    "保存选中节点为模版": "Save Selected Nodes as Template",
    "添加规则模板": "Add Rule Template",
    "添加规则模版": "Add Rule Template",
}


def main() -> None:
    # 1. Save LevelCreatorHelpTranslate.json
    almanac_dir = Path("translation-data/Almanac")
    almanac_dir.mkdir(parents=True, exist_ok=True)
    out_help = almanac_dir / "LevelCreatorHelpTranslate.json"
    with out_help.open("w", encoding="utf-8") as f:
        json.dump({"topics": HELP_TOPICS}, f, ensure_ascii=False, indent=2)
    print(f"Saved {out_help} ({len(HELP_TOPICS)} topics)")

    # 2. Update translation_strings.json
    strings_file = Path("translation-data/Strings/translation_strings.json")
    with strings_file.open("r", encoding="utf-8") as f:
        exact = json.load(f)
    exact.update(NEW_STRINGS)
    with strings_file.open("w", encoding="utf-8") as f:
        json.dump(exact, f, ensure_ascii=False, indent=2)
    print(f"Updated {strings_file} with {len(NEW_STRINGS)} new strings")


if __name__ == "__main__":
    main()
