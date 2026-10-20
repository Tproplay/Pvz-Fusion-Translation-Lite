#!/usr/bin/env python3
"""Batch 2: Add List, Variable, Undo/Redo, and How-to-use editor UI strings."""

from __future__ import annotations

import json
from pathlib import Path

NEW_STRINGS_2 = {
    # Image 1: Tabs & List types
    "已显示": "Shown",
    "已隐藏": "Hidden",
    "整数": "Integer",
    "小数": "Float",
    "布尔": "Boolean",
    "字符串": "String",
    "植物类型": "Plant Type",
    "僵尸类型": "Zombie Type",
    "对象": "Object",
    "列表": "List",
    "+ 整数": "+ Integer",
    "+ 小数": "+ Float",
    "+ 布尔": "+ Boolean",
    "+ 字符串": "+ String",
    "+ 列表": "+ List",
    "+ 对象": "+ Object",

    # Image 2: List editing dialog
    "列表初值 · ": "Initial List Values · ",
    "列表初值": "Initial List Values",
    "元素类型": "Element Type",
    "添加一项": "Add Item",
    "先删除列表全部元素，再修改元素类型；已有内容不会被自动丢弃。": "Delete all list elements first before changing element type; existing content will not be discarded automatically.",
    "列表为空，点击上方“添加一项”填写默认值。": "List is empty, click \"Add Item\" above to fill in default values.",
    "列表为空,点击上方“添加一项”填写默认值。": "List is empty, click \"Add Item\" above to fill in default values.",
    "第{0}/{1}页 · 共{2}项 · 类型：{3}": "Page {0}/{1} · Total {2} items · Type: {3}",
    "第{0}/{1}页 · 共{2}项 · 类型 {3}": "Page {0}/{1} · Total {2} items · Type: {3}",
    "修改立即写入当前关卡草稿；关闭后可用撤销恢复。": "Edits immediately save to level draft; undo after closing to revert.",
    "修改立即写入当前关卡草稿 关闭后可用撤销恢复。": "Edits immediately save to level draft; undo after closing to revert.",
    "修改立即写入当前关卡草稿，关闭后可用撤销恢复。": "Edits immediately save to level draft; undo after closing to revert.",
    "{0} · {1} / {2} 项": "{0} · {1} / {2} Items",
    "{0} 个变量": "{0} Variables",
    "列表元素{0}": "List Element {0}",
    "列表已达到512项上限。": "List has reached the 512 item limit.",
    "第{0}项已更新": "Item {0} updated",
    "第{0}项格式无效，保留上一次有效值。": "Item {0} format invalid; previous valid value retained.",
    "共享列表": "Shared List",
    "分类节点列表": "Categorized Node List",
    "源列表": "Source List",
    "目标列表": "Target List",
    "用源列表的内容替换目标列表，之后两份容器独立。": "Replace target list contents with source list; containers remain independent afterwards.",
    "移除共享列表全部内容。": "Remove all contents from shared list.",
    "读取共享列表当前元素个数。": "Read current element count of shared list.",
    "读取共享列表指定位置的值。": "Read value at specified position in shared list.",
    "已添加：": "Added: ",
    "添加：": "Add: ",

    # Image 3: Undo/Redo banners
    "没有可重做的记录": "No redo history available",
    "没有可撤销的记录": "No undo history available",
    "修改后不能重做原来的分支": "Original branch cannot be redone after modification",
    "重做": "Redo",
    "撤销": "Undo",

    # Image 4: How to use
    "怎么用": "How to Use",
    "\n\n<b>怎么用</b>\n": "\n\n<b>How to Use</b>\n",
    "<b>怎么用</b>": "<b>How to Use</b>",
    "这栏怎么用": "How to Use This Column",

    # Additional actions & editor strings
    "解锁后查看详情": "Unlock to view details",
    "遍历僵尸列表": "Iterate Zombie List",
    "向当前卡槽添加僵尸卡牌，可指定价格和冷却。": "Add zombie card to current seed slot with custom cost and cooldown.",
    "删除当前卡槽里指定类型的所有僵尸卡牌。": "Remove all zombie cards of specified type from current seed slot.",
    "删除指定索引的一项，后续元素自动前移。": "Delete item at specified index; subsequent elements shift forward.",
    "将整数值追加到共享列表中。": "Append integer value to shared list.",
    "将小数值追加到共享列表中。": "Append float value to shared list.",
    "将布尔值追加到共享列表中。": "Append boolean value to shared list.",
    "将字符串值追加到共享列表中。": "Append string value to shared list.",
    "将植物类型值追加到共享列表中。": "Append plant type value to shared list.",
    "将僵尸类型值追加到共享列表中。": "Append zombie type value to shared list.",
    "将对象值追加到共享列表中。": "Append object value to shared list.",
}


def main() -> None:
    path = Path("translation-data/Strings/translation_strings.json")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    data.update(NEW_STRINGS_2)

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {path} with {len(NEW_STRINGS_2)} strings (Total: {len(data)})")


if __name__ == "__main__":
    main()
