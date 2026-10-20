#!/usr/bin/env python3
"""Batch update translation_strings.json with Custom Level Editor and UI strings."""

from __future__ import annotations

import json
from pathlib import Path

NEW_STRINGS = {
    # 1. Back to Menu and Skins
    "返回菜单": "Back to Menu",
    "皮肤可在图鉴中切换": "You can switch skins in the Almanac.",

    # 2. Guide footer (Image 2) - covering all spacing variations:
    "滚轮或拖动右侧滚动条阅读  ·  Esc关闭  ·  阅读指南不会修改关卡": "Scroll or drag scrollbar to read · Esc to Close · Reading guide will not modify level",
    "滚轮或拖动右侧滚动条阅读 · Esc关闭 · 阅读指南不会修改关卡": "Scroll or drag scrollbar to read · Esc to Close · Reading guide will not modify level",
    "滚轮或拖动右侧滚动条阅读·Esc关闭·阅读指南不会修改关卡": "Scroll or drag scrollbar to read · Esc to Close · Reading guide will not modify level",
    "滚轮或拖动右侧滚动条阅读 · Esc关闭": "Scroll or drag scrollbar to read · Esc to Close",
    "滚轮或拖动右侧滚动条阅读  ·  Esc关闭": "Scroll or drag scrollbar to read · Esc to Close",
    "阅读指南不会修改关卡": "Reading guide will not modify level",
    "阅读滚动条": "Read Scrollbar",

    # 3. Image 3: Graph Check & Header
    "先选择一个节点，再编辑输入默认值": "Select a node first, then edit its default input values",
    "先选择一个节点,再编辑输入默认值": "Select a node first, then edit its default input values",
    "图检查（点击问题定位节点）": "Graph Check (Click issue to locate node)",
    "图检查 点击问题定位节点": "Graph Check: Click issue to locate node",
    "图检查": "Graph Check",
    "点击问题定位节点": "Click issue to locate node",
    "检查通过：节点、端口、变量、默认值和同步循环均未发现问题。": "Check passed: No issues found in nodes, ports, variables, default values, or sync loops.",
    "检查通过 节点、端口、变量、默认值和同步循环均未发现问题。": "Check passed: No issues found in nodes, ports, variables, default values, or sync loops.",

    # 4. Image 4: Creation Guide
    "制作指南": "Creation Guide",
    "关卡制作指南": "Level Creation Guide",
    "关卡制作指南入口": "Level Creation Guide Entry",
    "返回制作指南": "Back to Creation Guide",

    # 5. Image 5: More Tools & Modal Buttons
    "更多工具：需要排查问题或恢复编辑内容时再使用": "More Tools: Use when troubleshooting issues or restoring edits",
    "更多工具 需要排查问题或恢复编辑内容时再使用": "More Tools: Use when troubleshooting issues or restoring edits",
    "更多工具": "More Tools",
    "查看全图": "View Full Graph",
    "全图": "Full Graph",
    "把全部节点移回屏幕内，找回拖远的节点。": "Move all nodes back into view to find nodes dragged far away.",
    "把全部节点移回屏幕内,找回拖远的节点。": "Move all nodes back into view to find nodes dragged far away.",
    "查看执行记录": "View Execution Log",
    "执行记录": "Execution Log",
    "先开启记录，再试玩；回来查看哪些节点执行了。": "Enable logging first, then test play; return to check which nodes executed.",
    "先开启记录,再试玩 回来看哪些节点执行了。": "Enable logging first, then test play; return to check which nodes executed.",
    "先开启记录，再试玩 回来看哪些节点执行了。": "Enable logging first, then test play; return to check which nodes executed.",
    "保存节点草稿": "Save Node Draft",
    "只备份事件节点。整关仍用底部“保存并生成关卡”。": "Only backs up event nodes. Still use \"Save & Generate Level\" at bottom.",
    "只备份事件节点。整关仍用底部\"保存并生成关卡\"。": "Only backs up event nodes. Still use \"Save & Generate Level\" at bottom.",
    "恢复节点草稿": "Restore Node Draft",
    "恢复草稿": "Restore Draft",
    "恢复这张图上次保存的节点草稿，可撤销。": "Restore last saved node draft for this graph; can be undone.",
    "恢复这张图上次保存的节点草稿,可撤销。": "Restore last saved node draft for this graph; can be undone.",
    "恢复本关卡上次保存的事件草稿，可用撤销返回当前内容。": "Restore last saved event draft for this level; undo to revert.",
    "旧关卡兼容设置": "Legacy Level Compatibility",
    "旧关卡保持原设置即可。这里决定等待后读取哪次事件的数据。": "Keep original settings for older levels. Determines which event's data is read after waiting.",

    # 6. Additional Editor UI & Node Description panel text
    "点击画布上的节点，查看用途。\n\n上方“节点说明”提供端口解释和连接例子。\n\n第一次制作？打开右上角“制作指南”。": "Click a node on canvas to view its purpose.\n\n\"Node Description\" above provides port explanations and connection examples.\n\nFirst time? Open \"Creation Guide\" in top right.",
    "节点草稿已保存。保存整关请点击底部“保存并生成关卡”": "Node draft saved. To save whole level, click \"Save & Generate Level\" at bottom.",
    "<b>右侧输出：可以拿来做什么</b>": "<b>Right Output: What it can be used for</b>",
    "<b>左侧输入：需要接什么</b>": "<b>Left Input: What needs to be connected</b>",
    "<b>填写数值</b>\n节点本身的文本框和下拉框可以直接编辑。未连接的基础输入，可选中节点后点“填写输入值”。连线值优先；清除填写值后沿用节点原设置。\n": "<b>Enter Values</b>\nInput fields and dropdowns on nodes can be edited directly. For unconnected basic inputs, select node and click \"Enter Input Value\". Wired values take priority; clearing values restores defaults.\n",
    "<b>试玩验证</b>\n保存并生成关卡后再进入关卡。先只测试这一条规则，确认触发时机、执行次数与目标，再连接其他规则。\n": "<b>Test Verification</b>\nSave & generate level before entering game. Test this rule alone first to confirm trigger timing, execution count, and targets before connecting other rules.\n",
    "<size=20>排查时可使用节点编号：": "<size=20>Node ID for troubleshooting: ",
    "填写输入值：不用添加常量节点；已经连线的输入由上游提供": "Enter Input Value: No need to add constant nodes; connected inputs are provided upstream",
    "填写输入值": "Enter Input Value",
    "节点说明": "Node Description",
    "检查连线": "Verify Connections",
    "保存并试玩": "Save & Test",
    "只修改当前关卡的该类型数值；重新生成的实体使用新值。": "Only modifies values for this type in current level; newly spawned entities use new values.",
    "只有走到这个结果分支才发出执行信号，连到后续动作的触发输入。": "Only sends execution signal when branching to this result; connect to trigger inputs of downstream actions.",
    "同一数据输入有多个来源，旧节点只读取第一个": "Multiple sources for same data input; legacy nodes only read the first",
    "图中有无法恢复的节点，请保留原关卡文件，不要覆盖保存": "Graph contains unrecoverable nodes. Please keep original level file and do not overwrite save",
    "字符串变量": "String Variable",
    "整数变量": "Int Variable",
    "小数变量": "Float Variable",
    "真假变量": "Boolean Variable",
    "真假条件：true表示是，false表示否。可接比较结果或布尔值节点。": "Boolean condition: true or false. Connect comparison result or boolean node.",
    "存在空连线": "Empty connection exists",
    "存在重复连线；旧图保留原来的重复执行语义": "Duplicate connection exists; legacy graph preserves original repeated execution semantics",
    "完整数值编辑": "Full Stats Editing",
    "已恢复编辑记录 {0}/{1}": "Restored edit history {0}/{1}",
    "已更新：{0} = {1}（当前关卡）": "Updated: {0} = {1} (current level)",
    "当前未连接；未单独填写输入值。": "Currently unconnected; no individual input value entered.",
    "当前：保留触发时的数据。\n例如：先点第2行，等待时又点第4行，第一条规则结束等待后仍读取第2行。\n切换玩法阶段会停止上一阶段的等待和周期。变量仍读取当前值，植物或僵尸仍可能在等待期间死亡。": "Current: Preserve trigger-time data.\nExample: Clicking row 2 first, then row 4 while waiting; rule 1 still reads row 2 after waiting.\nSwitching phases cancels previous waits/loops. Variables read current values; entities may die during wait.",
    "当前：沿用旧关卡方式，等待结束后读取最近发生的事件。\n例如：先点第2行，等待时又点第4行，第一条规则结束等待后也读取第4行。\n改为保留触发数据后，第一条规则仍读取第2行；切换玩法阶段会停止上一阶段的等待和周期。修改后请试玩。": "Current: Legacy mode; reads most recent event after wait ends.\nExample: Clicking row 2 first, then row 4 while waiting; rule 1 also reads row 4 after wait.\nPreserving trigger data keeps row 2. Phase switch cancels waits/loops. Test play after editing.",
    "我的模板 {0}/{1} 页": "My Templates Page {0}/{1}",
    "执行超过限制，请检查触发环、循环次数或重复事件": "Execution limit exceeded; check trigger loops, iteration count, or recurring events",
    "按名称读取本局绑定的僵尸；对象销毁后存在输出为假": "Get bound zombie by name; output false if object destroyed",
    "按名称读取本局绑定的植物；对象销毁后存在输出为假": "Get bound plant by name; output false if object destroyed",
    "按指定间隔检查条件，成立时继续后续流程。": "Check condition at set intervals; proceed when satisfied.",
    "按照植物原有沉默规则暂停行动。": "Pause actions following plant's standard silence rules.",
    "收到OnPlantMix时输出融合后的植物": "Output fused plant when receiving OnPlantMix",
    "文本，可接字符串节点或在未连接时填写输入值。": "Text; connect string node or enter input value when unconnected.",
    "新执行模式保留事件实体或鼠标的行列，等待后仍读取触发当时位置": "New execution mode preserves event entity/mouse row & column; reads trigger-time position after wait",
    "新的变量": "New Variable",
    "无匹配节点": "No matching nodes",
    "无法创建节点类型: ": "Cannot create node type: ",
    "暂无描述信息\n\n<b>节点ID:</b> ": "No description available\n\n<b>Node ID:</b> ",
    "有效输入自动保存到关卡草稿；无效输入保留原值。": "Valid input automatically saves to level draft; invalid input retains original value.",
    "未找到节点ID: ": "Node ID not found: ",
    "未知的节点类型: ": "Unknown node type: ",
    "未知节点": "Unknown Node",
    "模板包含无法恢复的节点": "Template contains unrecoverable nodes",
    "模板名称为空或含有无效文件名字符": "Template name is empty or contains invalid characters",
    "模板已保存，变量会在每次插入时独立复制": "Template saved; variables copy independently on each insert",
    "模板检查未通过：": "Template validation failed: ",
    "模板读取失败，原文件保留：": "Failed to read template; original file kept: ",
    "此节点没有可填写的基础类型输入；对象和变量需要连线。": "This node has no editable basic input types; objects and variables require wires.",
    "没有可连接的节点": "No connectable nodes",
    "没有输入口。事件节点会在对应事件发生时触发；常量节点在取值时提供数据。": "No inputs. Event nodes fire on events; constant nodes supply data on evaluate.",
    "没有输出口。": "No outputs.",
    "端口方向或类型不匹配": "Port direction or type mismatch",
    "端口类型不兼容！{0} → {1}": "Incompatible port types! {0} → {1}",
    "等待后的取值方式：已有旧关卡建议保持原设置": "Value evaluation after wait: Legacy levels should keep original settings",
    "索引从0开始；数字或枚举名均可输入。对象初值填写本局的对象绑定名。": "0-indexed; numbers or enum names accepted. For objects, enter bound entity name.",
    "编辑{0}列表 · {1}项": "Edit {0} List · {1} items",
    "编辑列表初值": "Edit Initial List Values",
    "节点ID为空或重复": "Node ID empty or duplicate",
    "节点ID为空，无法跳转": "Node ID empty, cannot jump",
    "节点UI为空，无法跳转": "Node UI empty, cannot jump",
    "节点不存在": "Node does not exist",
    "节点不属于当前运行图": "Node does not belong to current graph",
    "节点分类": "Node Categories",
    "草稿包含无法恢复的节点": "Draft contains unrecoverable nodes",
    "解析数字、枚举名称或枚举编号，并输出是否成功。": "Parse number, enum name, or enum ID, and output success status.",
    "触发后修改共享字符串变量。": "Modify shared string variable when triggered.",
    "该连线会产生同步循环": "This wire creates a synchronous loop",
    "请先断开该输入的连线": "Please disconnect this input wire first",
    "请先选中要复用的节点；仅保存内部连线": "Select nodes to reuse first; only internal wires will be saved",
    "读取共享字符串变量当前保存的文字。": "Read text currently stored in shared string variable.",
    "输入不合法": "Invalid input",
    "输入僵尸本体血量低于或等于比例后触发一次；默认0.5，不含护甲，换目标后重新检测": "Triggers once when zombie HP reaches ratio (default 0.5, ignores armor; resets on new target)",
    "输入无效": "Invalid input",
    "输入默认值无效：": "Invalid default input value: ",
    "输出匹配值第一次出现的位置，以及列表是否包含该值。": "Output first matching index and whether list contains value.",
    "运行日志（返回编辑后仍保留最近256条）": "Execution Log (retains last 256 entries after returning to edit)",
    "这两个端口已经连接": "These two ports are already connected",
    "这份说明对应选中的节点。\n\n向下滚动查看：\n\n用途与操作\n输入输出\n当前连接与填写值\n连接例子\n常见错误": "Description for selected node.\n\nScroll down to view:\n\nUsage & Actions\nInputs & Outputs\nCurrent Connections & Values\nConnection Examples\nCommon Errors",
    "这是一个列表，可能为空；需要逐个处理时接相应的遍历节点。": "This is a list, possibly empty; connect to iterator node to process elements.",
    "这是场上的具体对象，与植物/僵尸种类不同。可连接创建、事件或查询节点；对象可能为空或已死亡。": "Specific entity on lawn, distinct from type. Connect to creation, event, or query nodes; may be null or dead.",
    "这是种类，连接对应类型节点；不能代替场上的具体对象。": "This is a type; connect to type nodes. Cannot substitute for specific lawn entities.",
    "连接“奖励选择”分类的选项或菜单节点；不能连接普通物品对象。": "Connect to \"Reward Selection\" options or menu nodes; cannot connect generic items.",
    "连接变量引用或设置变量的变量出口；需要数字/真假时，先经过“获取变量值”节点。": "Connect to variable reference or variable set output; route through \"Get Variable Value\" for numbers/bools.",
    "连接相同类型的输入口。": "Connect to input port of matching type.",
    "连接相同类型的输出口。": "Connect to output port of matching type.",
    "连线两端的类型不一致": "Incompatible wire endpoint types",
    "连线引用的端口不存在，可能来自不同版本": "Wired port does not exist; may be from a different version",
    "连线引用的节点不存在": "Wired node does not exist",
    "选择道具种类，供查询、冷却和比较节点使用。": "Select item type for query, cooldown, and comparison nodes.",
    "递归拆分融合配方，输出基础组成植物类型列表。": "Recursively decompose fusion recipe into base plant types list.",
    "通过MultipleChoiceMenu显示专用选项列表；旧多选节点仍保留": "Display options menu via MultipleChoiceMenu; legacy multichoice nodes retained",
    "首次触发后关闭；重置输入为真时仅重置，下次才执行": "Deactivates after first trigger; reset input resets state for next execution",
}


def main() -> None:
    path = Path("translation-data/Strings/translation_strings.json")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    data.update(NEW_STRINGS)

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {path} with {len(NEW_STRINGS)} strings (Total: {len(data)})")


if __name__ == "__main__":
    main()
