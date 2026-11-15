#!/usr/bin/env python3
"""Generate comprehensive EventNodes node and port translation mapping.

Extracts:
1. All 272 EventNode classes from dump.cs
2. All 118 *_PortName fields and port definitions
3. Node descriptions and Chinese titles from LevelCreatorHelp.json
4. All port string literals (CN <-> EN)
Outputs: translation-data/Strings/eventnode_port_map.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DUMP_CS = Path(r"c:\Users\Tproplay\Desktop\Programming\REA\Projects\Pvz Fusion 4.1\Il2Cpp Dumper\dump.cs")
HELP_JSON = REPO_ROOT / "translation-data" / "Dumps" / "LevelCreatorHelp.json"
STRINGS_JSON = REPO_ROOT / "translation-data" / "Strings" / "translation_strings.json"
OUTPUT_JSON = REPO_ROOT / "translation-data" / "Strings" / "eventnode_port_map.json"

# Canonical General Port Translations (Chinese -> English)
CANONICAL_PORTS = {
    # Execution Triggers
    "触发": "Trigger",
    "执行": "Execute",
    "完成": "On Complete",
    "创建完成": "On Complete",
    "失败": "Failed",
    "失败原因": "Failure Reason",
    "成功": "Success",
    "真": "True",
    "假": "False",
    "循环体": "Loop Body",
    "循环结束": "Loop End",
    "点击卡牌时触发": "Trigger on Card Click",
    "点击": "On Click",
    "进家失败": "Defeat on House Entry",
    
    # Common Data Inputs / Outputs
    "输出": "Output",
    "输入": "Input",
    "条件": "Condition",
    "结果": "Result",
    "列表": "List",
    "列表A": "List A",
    "列表B": "List B",
    "索引": "Index",
    "当前索引": "Current Index",
    "元素": "Element",
    "数量": "Count",
    "长度": "Length",
    "对象": "Object",
    "变量": "Variable",
    "变量名": "Variable Name",
    "值": "Value",
    "初始值": "Initial Value",
    "当前值": "Current Value",
    "目标值": "Target Value",
    
    # Comparisons & Math
    "大于": "Greater than",
    "小于": "Less than",
    "等于": "Equal to",
    "不等于": "Not Equal to",
    "大于等于": "Greater than or Equal to",
    "小于等于": "Less than or Equal to",
    "A": "A",
    "B": "B",
    "操作数A": "Operand A",
    "操作数B": "Operand B",
    "底数": "Base",
    "指数": "Exponent",
    "乘数": "Multiplier",
    "比例": "Ratio",
    "小数位数": "Decimals",
    
    # Game Entities
    "植物": "Plant",
    "植物类型": "Plant Type",
    "植物列表": "Plant List",
    "当前植物": "Current Plant",
    "当前植物类型": "Current Plant Type",
    "目标植物": "Target Plant",
    "僵尸": "Zombie",
    "僵尸类型": "Zombie Type",
    "僵尸列表": "Zombie List",
    "当前僵尸": "Current Zombie",
    "目标僵尸": "Target Zombie",
    "卡牌": "Card",
    "卡牌对象": "Card Object",
    "子弹": "Bullet",
    "子弹类型": "Bullet Type",
    "障碍物": "Obstacle",
    "坑洞": "Pit",
    "冰道": "Ice Trail",
    "冰块": "Ice Block",
    
    # Grid & Transform
    "行": "Row",
    "列": "Column",
    "列（小数）": "Column (Decimal)",
    "目标行": "Target Row",
    "目标列": "Target Column",
    "目标列（小数）": "Target Column (Decimal)",
    "位置": "Position",
    "坐标": "Coordinates",
    "X": "X",
    "Y": "Y",
    "Z": "Z",
    "X坐标": "X Position",
    "Y坐标": "Y Position",
    "Z坐标": "Z Position",
    "速度": "Speed",
    "角度": "Angle",
    "旋转": "Rotation",
    "缩放": "Scale",
    "大小": "Scale",
    "距离": "Distance",
    
    # Combat & Stats
    "伤害": "Damage",
    "血量": "Health",
    "最大血量": "Max Health",
    "当前血量": "Current Health",
    "治疗量": "Heal Amount",
    "护盾值": "Shield Amount",
    "死亡原因": "Death Reason",
    "原因": "Reason",
    "持续时间": "Duration",
    "间隔": "Interval",
    "延迟": "Delay",
    "冷却": "Cooldown",
    "概率": "Probability",
    "等级": "Level",
    "目标等级": "Target Level",
    "升至目标等级": "Upgrade to Target Level",
    
    # Economy & Resources
    "阳光": "Sun",
    "阳光数量": "Sun Amount",
    "金币": "Coins",
    "金币数量": "Coin Amount",
    "费用": "Cost",
    
    # UI & Audio
    "标题": "Title",
    "大标题": "Main Title",
    "小标题": "Subtitle",
    "文本": "Text",
    "默认文本": "Default Text",
    "描述": "Description",
    "音效": "Sound Effect",
    "音效ID": "Sound ID",
    "音乐": "Music",
    "波次": "Wave",
    "阶段": "Stage",
    
    # Lists & Collections
    "合并列表": "Merge List",
    "未合并": "Unmerge",
    "选项列表": "Option List",
    "选中的选项": "Selected Option",
    "发放": "Grant",
    "发放卡牌": "Grant Card",
    "发放数量": "Grant Count",
    "击杀并发奖励": "Kill and Grant Reward",
    
    # Additional Core Ports & Operators
    "数值": "Value",
    "名称或编号": "Name or ID",
    "名称": "Name",
    "值A": "Value A",
    "值B": "Value B",
    "新值": "New Value",
    "列表1": "List 1",
    "列表2": "List 2",
    "植物类型A": "Plant Type A",
    "植物类型B": "Plant Type B",
    "条件A": "Condition A",
    "条件B": "Condition B",
    "真（触发）": "True (Trigger)",
    "假（停止）": "False (Stop)",
    "创建成功": "On Success",
    "创建失败": "On Failed",
    "消耗成功": "On Success",
    "退出时触发": "On Exit",
    "选项被点击": "Option Clicked",
    "金币不足": "Insufficient Coins",
    "阳光不足": "Insufficient Sun",
    "间隔秒数": "Interval (Seconds)",
    "等待时间": "Wait Time",
    "周期事件": "Periodic Event",
    "周期间隔": "Periodic Interval",
    "伤害值": "Damage Amount",
    "回血量": "Heal Amount",
    "余数": "Remainder",
    "除数": "Divisor",
    "被除数": "Dividend",
    "和": "Sum",
    "积": "Product",
    "随机浮点数": "Random Float",
    "植物编号": "Plant ID",
    "每次循环": "Each Loop",
    "重置": "Reset",
    "超时": "Timeout",
    "计数": "Count",
    "包含": "Contains",
    "相同": "Same",
    "有效": "Valid",
    "最大值": "Max Value",
    "最小值": "Min Value",
    "最多检查次数": "Max Check Count",
    "循环次数": "Loop Count",
}

# Node Type Display Names (Class Name -> Chinese & English titles)
NODE_METADATA_FALLBACKS = {
    "OnBoardStartNode": {"cn": "关卡开始", "en": "On Board Start", "category": "Events"},
    "OnGameStartNode": {"cn": "关卡正式开始", "en": "On Game Start", "category": "Events"},
    "OnWaveClearedNode": {"cn": "波次清除", "en": "On Wave Cleared", "category": "Events"},
    "OnZombieHealthBelowNode": {"cn": "僵尸血量低于", "en": "On Zombie Health Below", "category": "Events"},
    "OnPlantClickNode": {"cn": "植物被点击", "en": "On Plant Clicked", "category": "Events"},
    "OnPlantCreateNode": {"cn": "植物被种植", "en": "On Plant Planted", "category": "Events"},
    "OnPlantDieNode": {"cn": "植物死亡时", "en": "On Plant Dying", "category": "Events"},
    "OnPlantDeathCompleteNode": {"cn": "植物死亡完成", "en": "On Plant Death Complete", "category": "Events"},
    "OnZombieSpawnNode": {"cn": "僵尸生成", "en": "On Zombie Spawned", "category": "Events"},
    "OnZombieDieNode": {"cn": "僵尸死亡", "en": "On Zombie Died", "category": "Events"},
    "OnKeyPressNode": {"cn": "按键按下", "en": "On Key Press", "category": "Events"},
    "OnMouseClickNode": {"cn": "鼠标点击", "en": "On Mouse Click", "category": "Events"},
    "WhileLoopNode": {"cn": "While循环", "en": "While Loop", "category": "Flow Control"},
    "BranchNode": {"cn": "分支", "en": "Branch", "category": "Flow Control"},
    "DoOnceNode": {"cn": "仅执行一次", "en": "Do Once", "category": "Flow Control"},
    "RandomTriggerNode": {"cn": "随机触发", "en": "Random Trigger", "category": "Flow Control"},
    "SequenceNode": {"cn": "序列", "en": "Sequence", "category": "Flow Control"},
    "DelayNode": {"cn": "延迟", "en": "Delay", "category": "Flow Control"},
    "CompareNode": {"cn": "比较", "en": "Compare", "category": "Logic"},
    "NotNode": {"cn": "非", "en": "Not", "category": "Logic"},
    "AndNode": {"cn": "与", "en": "And", "category": "Logic"},
    "OrNode": {"cn": "或", "en": "Or", "category": "Logic"},
    "AddPlantCardNode": {"cn": "添加植物卡牌", "en": "Add Plant Card", "category": "Actions"},
    "AddZombieCardNode": {"cn": "添加僵尸卡牌", "en": "Add Zombie Card", "category": "Actions"},
    "CreateZombieNode": {"cn": "生成僵尸", "en": "Create Zombie", "category": "Actions"},
    "MovePlantNode": {"cn": "移动植物", "en": "Move Plant", "category": "Actions"},
    "MoveZombieNode": {"cn": "移动僵尸", "en": "Move Zombie", "category": "Actions"},
    "DamagePlantNode": {"cn": "伤害植物", "en": "Damage Plant", "category": "Actions"},
    "DamageZombieNode": {"cn": "伤害僵尸", "en": "Damage Zombie", "category": "Actions"},
    "HealPlantNode": {"cn": "治疗植物", "en": "Heal Plant", "category": "Actions"},
    "DiePlantNode": {"cn": "杀死植物", "en": "Kill Plant", "category": "Actions"},
    "KillZombieNode": {"cn": "杀死僵尸", "en": "Kill Zombie", "category": "Actions"},
    "PowerNode": {"cn": "幂运算", "en": "Power", "category": "Math"},
    "GetObjectTransformNode": {"cn": "获取对象变换", "en": "Get Object Transform", "category": "Transform"},
    "SetZombieHouseRuleNode": {"cn": "设置僵尸进家规则", "en": "Set Zombie House Rule", "category": "Rules"},
    "UpgradeEventPlantNode": {"cn": "升级事件植物", "en": "Upgrade Event Plant", "category": "Actions"},
    "CreateInfoCardNode": {"cn": "创建信息卡", "en": "Create Info Card", "category": "UI"},
}


def main():
    print("Generating eventnode_port_map.json...")

    # Load Help JSON if available
    help_map = {}
    if HELP_JSON.is_file():
        with open(HELP_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            for node in data.get("nodes", []):
                t = node.get("type")
                if t:
                    help_map[t] = node

    # Load translation strings
    dict_strings = {}
    if STRINGS_JSON.is_file():
        with open(STRINGS_JSON, "r", encoding="utf-8") as f:
            dict_strings = json.load(f)

    # Parse dump.cs for EventNode classes and fields
    classes = {}
    if DUMP_CS.is_file():
        current_cls = None
        in_event_nodes = False
        with open(DUMP_CS, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                ls = line.strip()
                if "Namespace: GameLevel.EventNodes" in ls:
                    in_event_nodes = True
                    continue
                if in_event_nodes and ls.startswith("// Namespace:") and "GameLevel.EventNodes" not in ls:
                    in_event_nodes = False
                    continue
                if in_event_nodes:
                    m = re.match(r"public class (\w+)(?: : (\w+))?", ls)
                    if m:
                        current_cls = m.group(1)
                        parent = m.group(2)
                        classes[current_cls] = {
                            "parent": parent,
                            "fields": [],
                        }
                        continue
                    if current_cls and "_PortName;" in ls:
                        fm = re.search(r"public string (\w+_PortName);", ls)
                        if fm:
                            classes[current_cls]["fields"].append(fm.group(1))

    # Build node mapping
    nodes_out = {}
    for cls_name, info in sorted(classes.items()):
        meta = NODE_METADATA_FALLBACKS.get(cls_name, {})
        h = help_map.get(cls_name, {})
        
        cn_name = meta.get("cn") or h.get("purpose", "").split("，")[0].split("。")[0] or cls_name
        en_name = meta.get("en") or dict_strings.get(cn_name, cls_name)
        category = meta.get("category", "General")
        
        nodes_out[cls_name] = {
            "name_cn": cn_name,
            "name_en": en_name,
            "category": category,
            "parent": info.get("parent"),
            "port_fields": info.get("fields", []),
        }

    # Bidirectional port dictionary
    ports_cn2en = dict(CANONICAL_PORTS)
    # augment from dict_strings
    for cn, en in dict_strings.items():
        if 1 <= len(cn) <= 15 and cn not in ports_cn2en:
            # check if common port suffix
            if any(cn.endswith(sfx) for sfx in ["触发", "完成", "列表", "对象", "植物", "僵尸", "卡牌", "数量", "血量", "行", "列", "大小", "位置"]):
                ports_cn2en[cn] = en

    ports_en2cn = {en: cn for cn, en in ports_cn2en.items()}
    canonical_priorities = {
        "Value": "值", "On Complete": "完成", "Trigger": "触发", "Execute": "执行",
        "Output": "输出", "Input": "输入", "List": "列表", "Count": "数量",
        "Length": "长度", "Object": "对象", "Variable": "变量", "Row": "行",
        "Column": "列", "Plant": "植物", "Zombie": "僵尸", "Card": "卡牌",
        "Bullet": "子弹", "Damage": "伤害", "Health": "血量", "Heal Amount": "治疗量",
        "Sun": "阳光", "Coins": "金币", "Scale": "缩放", "Title": "标题",
        "Text": "文本", "Description": "描述", "Name or ID": "名称或编号",
    }
    ports_en2cn.update(canonical_priorities)

    result = {
        "_metadata": {
            "version": "4.1",
            "description": "PvZ Fusion Custom Level EventNodes translation mapping between Chinese and English (nodes, port names, directions, and field identifiers).",
            "total_nodes": len(nodes_out),
            "total_port_mappings": len(ports_cn2en),
        },
        "nodes": nodes_out,
        "ports": {
            "cn_to_en": ports_cn2en,
            "en_to_cn": ports_en2cn,
        },
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Generated {OUTPUT_JSON} successfully ({len(nodes_out)} nodes, {len(ports_cn2en)} ports).")


if __name__ == "__main__":
    main()
