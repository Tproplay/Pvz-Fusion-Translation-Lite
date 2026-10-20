import json
from pathlib import Path

strings_path = Path("translation-data/Strings/translation_strings.json")
with strings_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

# Enum names to remove from translation_strings.json so they never get replaced in metadata literals or save parsers
enum_members_to_remove = [
    "整数", "小数", "布尔", "字符串", "植物类型", "僵尸类型", "对象",
    "加", "减", "乘", "除", "取余",
    "无", "铲子", "手套", "锤子", "小推车", "金咖啡豆", "桶", "加农炮目标", "植物预览", "僵尸预览", "其他",
    "寒冰菇", "火爆辣椒", "墓碑", "弹坑", "梯子", "冰块",
    "寒冷秒数", "红温", "余烬", "中毒秒数", "蒜值", "水草值", "冻结值", "冻结秒数", "传送秒数",
    "攻击力", "一类防具血量", "二类防具血量", "基础移速", "体型", "本体血量", "本体最大血量",
    "普通词条", "究极词条", "僵尸词条",
    "大小倍率", "方向角度",
]

removed_count = 0
for k in enum_members_to_remove:
    if k in data:
        del data[k]
        removed_count += 1

# Ensure UI display strings are properly translated
ui_strings_to_add = {
    "网格：关": "Grid: Off",
    "网格：开": "Grid: On",
    "网格 关": "Grid: Off",
    "网格 开": "Grid: On",
    "网格": "Grid",
    "铅笔": "Pencil",
    "橡皮": "Eraser",
    "笔宽": "Brush Width",
    "笔宽 {0}": "Brush Width {0}",
    "笔宽 {1}": "Brush Width {1}",
    "{0}  /  笔宽 {1}  /  256 × 256": "{0}  /  Brush Width {1}  /  256 × 256",
    "铅笔 / 笔宽 6 / 256 × 256": "Pencil / Brush Width 6 / 256 × 256",
}

data.update(ui_strings_to_add)

with strings_path.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Removed {removed_count} enum members. Total strings: {len(data)}")
