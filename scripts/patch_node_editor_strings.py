#!/usr/bin/env python3
"""Add custom level editor node descriptions, port tooltips, and editor buttons to translation_strings.json."""

import json
from pathlib import Path

strings_path = Path("translation-data/Strings/translation_strings.json")
with strings_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

new_translations = {
    # Node description headers & structural labels
    "<b>用来做什么</b>\n": "<b>What It Does</b>\n",
    "<b>用来做什么</b>": "<b>What It Does</b>",
    "用来做什么": "What It Does",
    "<b>怎么使用</b>\n": "<b>How to Use</b>\n",
    "<b>怎么使用</b>": "<b>How to Use</b>",
    "怎么使用": "How to Use",
    "执行信号": "Execution Signal",
    "接事件或动作的执行出口。收到信号后才执行。": "Connect to an event or action execution output. Only executes upon receiving signal.",
    "从相同类型的输出口连到输入口。带触发输入的节点需要执行连线才能工作。只有数据连线不会执行动作。": "Connect outputs to inputs of the same type. Nodes with trigger inputs must be connected to execute. Data connections alone will not perform actions.",
    "当前连接": "Current Connection",
    "当前连接：": "Current Connection: ",
    "当前连接 ": "Current Connection ",
    "当前填写": "Current Value",
    "当前填写：": "Current Value: ",
    "当前填写 ": "Current Value ",
    "当前未连接触发信号。": "Currently no trigger signal connected.",
    "说明": "Description",
    "说明内容": "Description Content",
    "共触发": "Total Triggers",
    "关卡包含无法恢复的事件节点，已阻止覆盖原文件": "Level contains unrecoverable event nodes; overwriting original file blocked.",
    "变量创建网格": "Variable Creation Grid",
    "变量引用": "Variable Reference",
    "变量引用未绑定，请重新从属性面板拖入": "Variable reference unbound; please drag again from inspector.",
    "节点预制体未设置！": "Node prefab is not set!",
    "子弹参数越界或类型未加载": "Projectile parameter out of bounds or type not loaded.",
    "存在同步触发环，请通过等待或周期安排下一次执行": "Synchronous trigger loop detected; please schedule subsequent executions via Wait or Cycle.",
    "控制本局僵尸进家是否触发原有失败判定。": "Controls whether zombies entering the house triggers the default defeat condition.",
    "普通出怪流程SpawnOver之后，全场敌人清空时，每波触发一次；不适用于未发布SpawnOver的自定义出怪器": "Triggers once per wave when all enemies are cleared after standard SpawnOver; does not apply to custom spawners without SpawnOver.",
    "进入指定名称的阶段时触发，同名阶段不会重复进入": "Triggers upon entering the named phase; will not re-enter phases of the same name.",
    "在战场左键点击存活僵尸时触发。": "Triggers when left-clicking a living zombie on the lawn.",
    "移动和缩放创建场景对象节点生成的标记。": "Move and scale markers created by the Spawn Scene Object node.",
    "直接尝试触发植物的金咖啡豆大招。": "Directly attempts to trigger the plant's Golden Coffee Bean ultimate.",
    "对指定植物调用实际投喂金咖啡豆流程。": "Triggers the Golden Coffee Bean feeding routine for the specified plant.",

    # Buttons from screenshots
    "改为读取最新事件（旧版）": "Switch to Read Latest Event (Legacy)",
    "改为读取最新事件 (旧版)": "Switch to Read Latest Event (Legacy)",
    "改为读取最新事件 旧版": "Switch to Read Latest Event (Legacy)",
    "改为读取最新事件": "Switch to Read Latest Event",
    "改为保留触发数据": "Switch to Preserve Trigger Data",

    # Port descriptions & datatypes
    "可带小数的数值，例如0.5、5。整数口需要先经“整数转浮点数”；具体单位见用法和注意事项。": "Decimal numbers (e.g. 0.5, 5). Integer outputs must first pass through \"Integer to Float\". See usage and notes for specific units.",
    "可带小数的数值,例如0.5,5。整数口需要先经“整数转浮点数” 具体单位见用法和注意事项。": "Decimal numbers (e.g. 0.5, 5). Integer outputs must first pass through \"Integer to Float\". See usage and notes for specific units.",
    "整数，例如1、25。可连接整数常量、计数器或整数运算结果。": "Integers (e.g. 1, 25). Can connect to integer constants, counters, or arithmetic results.",
    "整数，例如1,25。可连接整数常量、计数器或整数运算结果。": "Integers (e.g. 1, 25). Can connect to integer constants, counters, or arithmetic results.",
    "一次触发直接给共享变量加、减、乘、除或取余。": "When triggered, adds, subtracts, multiplies, divides, or modulo the shared variable.",
    "一般物品对象。旧多选菜单也使用此类型传选项列表，搭配时请看下方例子，不要混接。": "General entity object. Legacy multichoice menus also used this type for option lists; see examples below and do not mix connections.",
    "专用选项列表类型，点击时保留本次事件上下文": "Dedicated option list type; preserves event context when clicked.",
    "两个整数取模（被除数 % 除数）": "Modulo of two integers (dividend % divisor).",
    "两个整数相乘（A × B）": "Multiplies two integers (A × B).",
    "两个整数相减（被减数 - 减数）": "Subtracts two integers (minuend - subtrahend).",
    "两个整数相加（A + B）": "Adds two integers (A + B).",
    "两个整数相除（被除数 ÷ 除数，整除）": "Divides two integers (dividend ÷ divisor, integer division).",
    "从布尔变量中获取当前存储的布尔值": "Gets the boolean value currently stored in a boolean variable.",
    "从整数变量中获取当前存储的整数值": "Gets the integer value currently stored in an integer variable.",
    "从植物类型列表中删除指定的植物类型，输出结果列表和是否成功": "Removes the specified plant type from a plant type list; outputs result list and success status.",
    "从植物类型列表中随机获取一个植物类型": "Gets a random plant type from a plant type list.",
    "从浮点数变量中获取当前存储的浮点数值": "Gets the float value currently stored in a float variable.",
    "依次输出列表中的每只存活僵尸，遍历结束后触发完成。": "Sequentially outputs each living zombie in the list; triggers completion when iteration finishes.",
    "值无效：枚举可填成员名，布尔使用true/false，浮点使用小数点": "Invalid value: Enums accept member names, booleans use true/false, floats use decimal points.",
    "不能连接相同方向的端口！": "Cannot connect ports of the same direction!",
    "删除全部信息卡，或输入对象对应的一张信息卡。": "Deletes all info cards, or a single info card corresponding to the input object.",
    "删除当前事件图创建的场景标记。": "Deletes scene markers created by the current event graph.",
    "删除指定格子的墓碑、弹坑、梯子或冰块。": "Deletes tombstones, craters, ladders, or ice blocks from the specified grid tile.",
    "合并两个专用选项列表": "Merges two dedicated option lists.",
    "将0～127的ASCII码转换为一个字符。": "Converts an ASCII code (0–127) into a character.",
    "将三个小数组合为世界坐标。": "Combines three floats into a world coordinate vector.",
    "将僵尸类型值插入到共享列表中。": "Inserts a zombie type value into a shared list.",
    "将僵尸类型值替换到共享列表中。": "Replaces a zombie type value in a shared list.",
    "将僵尸转换为场景对象引用。": "Converts a zombie to a scene object reference.",
    "将字符串值插入到共享列表中。": "Inserts a string value into a shared list.",
    "将字符串值替换到共享列表中。": "Replaces a string value in a shared list.",
    "将对象值插入到共享列表中。": "Inserts an object value into a shared list.",
    "将对象值替换到共享列表中。": "Replaces an object value in a shared list.",
    "将小数值插入到共享列表中。": "Inserts a float value into a shared list.",
    "将小数值替换到共享列表中。": "Replaces a float value in a shared list.",
    "将布尔值插入到共享列表中。": "Inserts a boolean value into a shared list.",
    "将布尔值替换到共享列表中。": "Replaces a boolean value in a shared list.",
    "将数值或枚举转换为可读文字。": "Converts a number or enum into readable text.",
    "将整数值插入到共享列表中。": "Inserts an integer value into a shared list.",
    "将整数值替换到共享列表中。": "Replaces an integer value in a shared list.",
    "将植物类型值插入到共享列表中。": "Inserts a plant type value into a shared list.",
    "将植物类型值替换到共享列表中。": "Replaces a plant type value in a shared list.",
    "将植物转换为场景对象引用。": "Converts a plant to a scene object reference.",
    "按从0开始的行列查询主植物、支撑或飞行层，越界返回空列表": "Queries main, shell, carrier, or flying plants by 0-indexed row and column; returns empty list if out of bounds.",
    "获取当前棋盘仍存活的僵尸快照。": "Gets a snapshot of all living zombies on the current lawn.",
    "获取鼠标当前持有的物品对象及种类。": "Gets the item object and type currently held by the mouse.",
    "设置僵尸卡冷却": "Set Zombie Card Cooldown",
    "设置僵尸战斗数值": "Set Zombie Combat Stats",
    "设置指定僵尸的状态、持续秒数或层数。": "Sets the status, duration (seconds), or stacks of the specified zombie.",
    "设置指定植物自身的基础攻击间隔。": "Sets the base attack interval of the specified plant.",
    "设置攻击力、防具血量、基础移速或体型。": "Sets attack power, armor HP, base movement speed, or size.",
    "设置植物技能、成长或吞咽等使用的属性倒计时。": "Sets countdown timers used for plant skills, growth, swallowing, etc.",
    "点击画布上的节点，查看用途。\n\n上方“节点说明”提供端口解释和连接例子。\n\n第一次制作？打开右上角“制作指南”。": "Click a node on the canvas to view its purpose.\n\n\"Node Description\" above provides port explanations and connection examples.\n\nFirst time creating? Open the \"Creation Guide\" in the top right.",
    "\n\n点击上方“节点说明”查看端口与连接例子。": "\n\nClick \"Node Description\" above to view ports and connection examples.",
}

data.update(new_translations)
with strings_path.open("w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Added {len(new_translations)} node editor translations successfully!")
