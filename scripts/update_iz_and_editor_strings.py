#!/usr/bin/env python3
"""Update translation_strings.json and tips_iz.json with I,Zombie level translations and super level editor strings/enums."""

from __future__ import annotations

import json
from pathlib import Path

STRINGS_PATH = Path("translation-data/Strings/translation_strings.json")
TIPS_IZ_PATH = Path("translation-data/Strings/tips_iz.json")

# 1. Custom Level Editor Enums & Types
ENUM_STRINGS = {
    # Bullet Property
    "寒冷秒数": "Chill Duration",
    "红温": "Overheat",
    "余烬": "Ember",
    "中毒秒数": "Poison Duration",
    "蒜值": "Garlic Value",
    "水草值": "Kelp Value",
    "冻结值": "Freeze Value",
    "冻结秒数": "Freeze Duration",
    "传送秒数": "Teleport Duration",
    # Zombie Property
    "攻击力": "Attack Power",
    "一类防具血量": "Armor 1 HP",
    "二类防具血量": "Armor 2 HP",
    "基础移速": "Base Move Speed",
    "体型": "Size",
    "本体血量": "Base HP",
    "本体最大血量": "Base Max HP",
    # Item Type
    "无": "None",
    "铲子": "Shovel",
    "手套": "Glove",
    "锤子": "Hammer",
    "小推车": "Lawn Mower",
    "金咖啡豆": "Golden Coffee Bean",
    "桶": "Bucket",
    "加农炮目标": "Cannon Target",
    "植物预览": "Plant Preview",
    "僵尸预览": "Zombie Preview",
    "其他": "Other",
    # Math Operation
    "加": "Add",
    "减": "Subtract",
    "乘": "Multiply",
    "除": "Divide",
    "取余": "Modulo",
    # Special Plant
    "寒冰菇": "Ice-shroom",
    "火爆辣椒": "Jalapeno",
    # Grid Obstacle
    "墓碑": "Grave",
    "弹坑": "Crater",
    "梯子": "Ladder",
    "冰块": "Ice Block",
    # Particle / Transform Property
    "大小倍率": "Size Multiplier",
    "方向角度": "Direction Angle",
    # Buff Category
    "普通词条": "Common Modifier",
    "究极词条": "Ultimate Modifier",
    "僵尸词条": "Zombie Modifier",
    # EventListValueType
    "整数": "Integer",
    "小数": "Float",
    "布尔": "Boolean",
    "字符串": "String",
    "植物类型": "Plant Type",
    "僵尸类型": "Zombie Type",
    "对象": "Object",
    # Modes
    "弹幕模式": "Danmaku Mode",
    "点赞模式": "Like Mode",
    "送礼模式": "Gift Mode",
}

# 2. Level Editor Node & Port Descriptions from Screenshots
EDITOR_STRINGS = {
    # Projectile firing & node actions
    "在指定格子或鼠标位置向给定方向发射子弹。": "Fires a projectile in a given direction at the specified grid tile or mouse position.",
    "在指定格子或鼠标位置向给定方向发射子弹": "Fires a projectile in a given direction at the specified grid tile or mouse position.",
    # Board coordinate explanation (all spacing/punctuation variants)
    "棋盘坐标从0开始：第一行/第一列填0，第二行/第二列填1。": "Board coordinates start from 0: enter 0 for Row 1 / Column 1, enter 1 for Row 2 / Column 2.",
    "棋盘坐标从0开始 第一行/第一列填0,第二行/第二列填1。": "Board coordinates start from 0: enter 0 for Row 1 / Column 1, enter 1 for Row 2 / Column 2.",
    "棋盘坐标从0开始 第一行/第一列填0，第二行/第二列填1。": "Board coordinates start from 0: enter 0 for Row 1 / Column 1, enter 1 for Row 2 / Column 2.",
    "棋盘坐标从0开始: 第一行/第一列填0, 第二行/第二列填1.": "Board coordinates start from 0: enter 0 for Row 1 / Column 1, enter 1 for Row 2 / Column 2.",
    "棋盘坐标从0开始：第一行/第一列填0，第二行/第二列填1": "Board coordinates start from 0: enter 0 for Row 1 / Column 1, enter 1 for Row 2 / Column 2.",
    # Port types & categories
    "子弹种类": "Projectile Type",
    "子弹种类列表": "Projectile Type List",
    "子弹对象": "Projectile Object",
    "奖励选项列表": "Reward Option List",
    "植物种类": "Plant Category",
    "植物种类列表": "Plant Category List",
    "僵尸种类": "Zombie Category",
    "僵尸种类列表": "Zombie Category List",
    "完整数值": "Full Value",
    "完整数值 · ": "Full Value · ",
    "完整数值…": "Full Value…",
    "完整数值编辑": "Edit Full Value",
    "对有限小数计算幂或指定底数的对数。": "Calculates powers or logarithms of finite decimals.",
    "已连接：由上游提供": "Connected: Provided by upstream",
    "把僵尸以名称绑定到本局，例如首领；重复名称替换绑定": "Binds zombie by name to this match (e.g. Boss); duplicate names overwrite binding.",
    "把植物以名称绑定到本局，例如守护目标；重复名称替换绑定": "Binds plant by name to this match (e.g. Guard Target); duplicate names overwrite binding.",
    "获取全场僵尸": "Get All Zombies on Field",
    "设置僵尸状态": "Set Zombie Status",
    "在同地形地图之间切换昼夜背景，保留棋盘实体与冰道。": "Switches between day and night backgrounds of the same terrain, preserving board entities and ice trails.",
    "小数运算溢出，原值保留": "Decimal calculation overflow; original value retained",
    "整数运算溢出，原值保留": "Integer calculation overflow; original value retained",
    "存在数值依赖环": "Numeric dependency loop detected",
    "存在空植物配置或无效植物类型。": "Empty plant config or invalid plant type detected.",
}

# 3. I, Zombie Level Titles
IZOMBIE_TITLES = {
    # Chapter 1
    "1：光茵荏苒": "1: Lawn of Time",
    "1光茵荏苒": "1: Lawn of Time",
    "1-3教程": "1-3 Tutorial",
    "1-6教程": "1-6 Tutorial",
    "1-7教程": "1-7 Tutorial",
    # Chapter 2
    "2：菇泛远影": "2: Shroomshade",
    "2菇泛远影": "2: Shroomshade",
    "2-2教程": "2-2 Tutorial",
    "2-6教程": "2-6 Tutorial",
    "2-7教程": "2-7 Tutorial",
    "2-8教程": "2-8 Tutorial",
    # Chapter 3
    "3：推波助澜": "3: Making Waves",
    "3推波助澜": "3: Making Waves",
    "3-2教程": "3-2 Tutorial",
    "3-3教程": "3-3 Tutorial",
    "3-6教程": "3-6 Tutorial",
    "3-7教程": "3-7 Tutorial",
    # Chapter 4
    "4：磁荧流转": "4: Magnetic Flux",
    "4磁荧流转": "4: Magnetic Flux",
    "4-1教程": "4-1 Tutorial",
    "4-2教程": "4-2 Tutorial",
    "4-3教程": "4-3 Tutorial",
    "4-6教程": "4-6 Tutorial",
    "4-7教程": "4-7 Tutorial",
    "4-10教程": "4-10 Tutorial",
    # Chapter 5
    "5：殊途同归": "5: Different Paths",
    "5殊途同归": "5: Different Paths",
    "5-2教程": "5-2 Tutorial",
    "5-3教程": "5-3 Tutorial",
    # Special / Hints
    "特别感谢": "Special Thanks",
    "3-10提示": "3-10 Hint",
}

# TextAsset names to rename in data.unity3d and aliases in tips_iz.json
CUSTOM_IZ_TEXTASSET_MAP = {
    "101CustomIZ1：光茵荏苒": "101CustomIZ1: Lawn of Time",
    "104CustomIZ1-3教程": "104CustomIZ1-3 Tutorial",
    "110CustomIZ1-6教程": "110CustomIZ1-6 Tutorial",
    "112CustomIZ1-7教程": "112CustomIZ1-7 Tutorial",
    "201CustomIZ2：菇泛远影": "201CustomIZ2: Shroomshade",
    "203CustomIZ2-2教程": "203CustomIZ2-2 Tutorial",
    "210CustomIZ2-6教程": "210CustomIZ2-6 Tutorial",
    "212CustomIZ2-7教程": "212CustomIZ2-7 Tutorial",
    "214CustomIZ2-8教程": "214CustomIZ2-8 Tutorial",
    "301CustomIZ3：推波助澜": "301CustomIZ3: Making Waves",
    "303CustomIZ3-2教程": "303CustomIZ3-2 Tutorial",
    "305CustomIZ3-3教程": "305CustomIZ3-3 Tutorial",
    "311CustomIZ3-6教程": "311CustomIZ3-6 Tutorial",
    "313CustomIZ3-7教程": "313CustomIZ3-7 Tutorial",
    "401CustomIZ4：磁荧流转": "401CustomIZ4: Magnetic Flux",
    "402CustomIZ4-1教程": "402CustomIZ4-1 Tutorial",
    "404CustomIZ4-2教程": "404CustomIZ4-2 Tutorial",
    "406CustomIZ4-3教程": "406CustomIZ4-3 Tutorial",
    "412CustomIZ4-6教程": "412CustomIZ4-6 Tutorial",
    "414CustomIZ4-7教程": "414CustomIZ4-7 Tutorial",
    "418CustomIZ4-10教程": "418CustomIZ4-10 Tutorial",
    "501CustomIZ5：殊途同归": "501CustomIZ5: Different Paths",
    "503CustomIZ5-2教程": "503CustomIZ5-2 Tutorial",
    "505CustomIZ5-3教程": "505CustomIZ5-3 Tutorial",
    "601CustomIZ特别感谢": "601CustomIZSpecial Thanks",
    "602CustomIZ3-10提示": "602CustomIZ3-10 Hint",
}


def update_translation_strings() -> None:
    with STRINGS_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    before = len(data)
    data.update(ENUM_STRINGS)
    data.update(EDITOR_STRINGS)
    data.update(IZOMBIE_TITLES)
    after = len(data)

    with STRINGS_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {STRINGS_PATH}: {before} -> {after} (+{after - before} entries)")


def update_tips_iz() -> None:
    with TIPS_IZ_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    added = 0
    for old_k, new_k in CUSTOM_IZ_TEXTASSET_MAP.items():
        if old_k in data and new_k not in data:
            data[new_k] = data[old_k]
            added += 1

    with TIPS_IZ_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Updated {TIPS_IZ_PATH}: added {added} English alias keys")


def main() -> None:
    update_translation_strings()
    update_tips_iz()


if __name__ == "__main__":
    main()
