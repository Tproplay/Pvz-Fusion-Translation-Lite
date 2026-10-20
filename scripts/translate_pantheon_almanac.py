#!/usr/bin/env python3
"""Translate Pantheon Evolution Almanac UI, TextAssets, and literals."""

import json
from pathlib import Path

STRINGS_PATH = Path("translation-data/Strings/translation_strings.json")
REGEXS_PATH = Path("translation-data/Strings/translation_regexs.json")

PANTHEON_STRINGS: dict[str, str] = {
    # Top Tab Bar
    "植物图鉴": "Plant Almanac",
    "专家词条": "Specialist Modifiers",
    "其他词条": "Other Modifiers",
    "超质变": "Super Evolution",
    "战术词条": "Tactical Modifiers",
    "试炼词条": "Trial Modifiers",

    # Fix Close Button context collision
    "关闭": "Close",

    # Cards & Badges
    "基础": "Base",
    "100币": "100 Coins",
    "50币": "50 Coins",
    "诸神币": "Pantheon Coins",
    "诸神币 ": "Pantheon Coins ",
    "诸神币：": "Pantheon Coins: ",
    " 诸神币": " Pantheon Coins",
    "诸神币：{0}": "Pantheon Coins: {0}",
    "当前诸神币：{0}": "Current Pantheon Coins: {0}",
    "诸神币 2000": "Pantheon Coins 2000",

    # Middle & Right Pane Subtitles & Headers
    "基础植物 · ": "Base Plant · ",
    "终端植物 · ": "Terminal Plant · ",
    "终端植物": "Terminal Plant",
    "{0} 条进化路线 · 点击卡牌查看词条": "{0} Evolution Paths · Click card to view modifiers",
    "可获得词条  {0} 项": "Available Modifiers: {0}",
    "可获得词条 {0} 项": "Available Modifiers: {0}",
    "{0} · 最多 {1} 次{2}": "{0} · Max {1} times{2}",
    "{0} · 最多 {1} 次": "{0} · Max {1} times",
    " · 50诸神币": " · 50 Pantheon Coins",
    " · 未购买 · {0}诸神币": " · Not Purchased · {0} Pantheon Coins",
    "{0} · {1}诸神币": "{0} · {1} Pantheon Coins",
    "路线 {0}  /  {1}": "Path {0} / {1}",
    "路线 {0} / {1}": "Path {0} / {1}",
    "路线 {0}": "Path {0}",
    " · 专家植物": " · Specialist Plant",
    " · 先解锁基础植物": " · Unlock base plant first",
    " · 免费": " · Free",
    " · 已解锁": " · Unlocked",
    " · 已购买": " · Purchased",
    " · 被动": " · Passive",
    " 个词条 · 前三级免费\n": " Modifiers · First 3 tiers free\n",
    "（普通品质基准，实际增幅随品质变化）。": "(Based on Common quality; actual bonus scales with quality).",
    "普通品质基准,实际增幅随品质变化。": " based on Common quality; actual bonus scales with quality.",
    " 普通品质基准,实际增幅随品质变化。": " based on Common quality; actual bonus scales with quality.",
    "普通品质基准，实际增幅随品质变化。": " based on Common quality; actual bonus scales with quality.",

    # Specific Route Headers
    "路线 1 / Photon Splitter · 50诸神币": "Path 1 / Photon Splitter · 50 Pantheon Coins",
    "路线 2 / Berserker Snipea · 50诸神币": "Path 2 / Berserker Snipea · 50 Pantheon Coins",
    "路线 3 / Blazer Snipea · 50诸神币": "Path 3 / Blazer Snipea · 50 Pantheon Coins",

    # Plant Evolution Routes
    "机枪路线": "Gatling Route",
    "樱桃路线": "Cherry Route",
    "寒冰路线": "Ice Route",
    "毁灭路线": "Doom Route",
    "黑高路线": "Tall-nut Route",
    "灾果路线": "Jalapeno-nut Route",
    "大喷路线": "Fume Route",
    "忧郁路线": "Gloom Route",
    "魅后路线": "Hypno Queen Route",
    "火炮路线": "Fire Cannon Route",
    "浴火路线": "Rebirth Flame Route",
    "大哥路线": "Big Brother Route",
    "魅胆路线": "Hypno Scaredy Route",
    "刺果路线": "Spike-nut Route",
    "战神路线": "Warlord Route",
    "瓜炮路线": "Melon Cannon Route",
    "冰炮路线": "Ice Cannon Route",
    "大帝路线": "Emperor Route",
    "玄钢路线": "Steel Spikerock Route",
    "毁胆路线": "Doom Scaredy Route",
    "火神路线": "Vulcan Route",
    "菜炮路线": "Cabbage Cannon Route",
    "绿伞路线": "Emerald Umbrella Route",
    "剑仙路线": "Sword Immortal Route",
    "究投路线": "Ultimate Pitcher Route",
    "黑曜路线": "Obsidian Route",
    "爆竹路线": "Firecracker Route",

    # ShootingAlmanacIndex Titles, Descriptions & Conditions
    "幸运": "Luck",
    "幸运提高25，幸运可以提高好词条出现概率\n普通品质基准，实际效果随品质及当前构筑变化。": "Luck +25. Higher luck improves chance of higher quality modifiers.\nBased on Common quality; actual bonus scales with quality.",
    "抽取概率受幸运影响。\n幸运尚未达到上限时可出现。\n尚未获得“交易-孤注一掷”时可出现。": "Draw chance affected by Luck.\nAppears when Luck has not reached cap.\nAppears if 'Trade - All In' is not owned.",
    "伤害增幅": "Damage Boost",
    "全体植物获得10%伤害增幅\n普通品质基准，实际效果随品质及当前构筑变化。": "All plants gain +10% damage boost.\nBased on Common quality; actual bonus scales with quality.",
    "抽取概率受幸运影响。": "Draw chance affected by Luck.",
    "合理投资": "Sound Investment",
    "获得1次词条刷新的机会\n普通品质基准，实际效果随品质及当前构筑变化。": "Gain 1 modifier reroll chance.\nBased on Common quality; actual bonus scales with quality.",
    "抽取概率受幸运影响。\n尚未获得“交易-孤注一掷”时可出现。": "Draw chance affected by Luck.\nAppears if 'Trade - All In' is not owned.",
    "保护": "Protection",
    "全体植物获得5000护盾，复活后依然生效\n普通品质基准，实际效果随品质及当前构筑变化。": "All plants gain 5000 shield; persists after revival.\nBased on Common quality; actual bonus scales with quality.",
    "抽取概率受幸运影响。\n僵尸类型不是豌豆僵尸或随机僵尸时生效。": "Draw chance affected by Luck.\nActive when zombies are not Pea Zombies or Random Zombies.",
    "全体植物获得50000护盾，复活后依然生效\n普通品质基准，实际效果随品质及当前构筑变化。": "All plants gain 50000 shield; persists after revival.\nBased on Common quality; actual bonus scales with quality.",
    "抽取概率受幸运影响。\n僵尸类型为豌豆僵尸或随机僵尸时生效。": "Draw chance affected by Luck.\nActive when zombies are Pea Zombies or Random Zombies.",
    "复活": "Revival",
    "复活时间降低99%": "Revival time reduced by 99%.",
    "抽取概率受幸运影响。\n已获得“超质变：步步高升”时可出现。": "Draw chance affected by Luck.\nAppears if 'Super Evolution: Rising Step by Step' is owned.",
    "复活时间降低10%\n普通品质基准，实际效果随品质及当前构筑变化。": "Revival time reduced by 10%.\nBased on Common quality; actual bonus scales with quality.",
    "抽取概率受幸运影响。\n尚未获得“超质变：步步高升”时可出现。": "Draw chance affected by Luck.\nAppears if 'Super Evolution: Rising Step by Step' is not owned.",
    "碾压保护": "Crush Protection",
    "全体植物获得抵御碾压的能力，复活后依然生效，并立即获得3000护盾": "All plants gain immunity to crush; persists after revival; immediately gain 3000 shield.",
    "抽取概率受幸运影响。\n尚未获得碾压保护时可出现。": "Draw chance affected by Luck.\nAppears if Crush Protection is not owned.",
    "爆炸保护": "Blast Protection",
    "僵尸方的小丑爆炸伤害降低至1000，并立即获得3000护盾": "Zombie Jack-in-the-Box explosion damage reduced to 1000; immediately gain 3000 shield.",
    "抽取概率受幸运影响。\n尚未获得“爆炸保护”时可出现。": "Draw chance affected by Luck.\nAppears if Blast Protection is not owned.",
    "护盾保护": "Shield Ward",
    "持有护盾的植物每秒回复0.1%护盾量的生命值，并立即获得6000护盾": "Plants with shields regenerate 0.1% shield value as HP/s; immediately gain 6000 shield.",
    "抽取概率受幸运影响。\n尚未获得“护盾保护”时可出现。": "Draw chance affected by Luck.\nAppears if Shield Ward is not owned.",
    "超质变：腐化": "Super Evolution: Corruption",
    "获得词条：腐化": "Gain modifier: Corruption",
    "每次判定有 0.01% 概率进入超质变抽取。": "Each check has a 0.01% chance to enter Super Evolution draw.",
    "超质变：步步高升": "Super Evolution: Rising Step by Step",
    "所有词条一定是最高品质，且钻石词条的加成x5\n注意：部分植物攻速过快时会丢失动画导致无法攻击或攻速降低": "All modifiers guaranteed highest quality; Diamond modifier bonuses x5.\nNote: Extremely fast attack speed may drop animations and affect hits.",
    "超质变：力量会给予希望": "Super Evolution: Hope Through Strength",
    "获得词条：力量会给予希望\n获得植物：[[plant:UltimateJalaNut]]\n获得植物：[[plant:UltimateExplodeCannon]]\n[[plant:UltimateExplodeCannon]]获得600%攻击力加成": "Gain modifier: Hope Through Strength\nGain plant: [[plant:UltimateJalaNut]]\nGain plant: [[plant:UltimateExplodeCannon]]\n[[plant:UltimateExplodeCannon]] gains +600% attack power.",
    "超质变：神秘大炮": "Super Evolution: Mystery Cannon",
    "获得一个神秘大炮": "Obtain a Mystery Cannon.",
    "专家邀请": "Specialist Invitation",
    "从多个选项中自选一株专家植物": "Choose 1 Specialist Plant from several options.",
    "仍有尚未获得的专家植物时有概率出现，概率受幸运影响。": "Has a chance to appear while unowned Specialist Plants remain; affected by Luck.",
    "获得新植物：[[plant:UltimateMinigun]]\n可查看其全部专属词条。": "Obtain new plant: [[plant:UltimateMinigun]]\nView all its exclusive modifiers.",
    "尚未获得此专家植物时可选择。": "Selectable when this Specialist Plant is not yet owned.",
    "获得新植物：[[plant:UltimateBlover]]\n可查看其全部专属词条。": "Obtain new plant: [[plant:UltimateBlover]]\nView all its exclusive modifiers.",
    "获得新植物：[[plant:EmeraldUmbrella]]\n可查看其全部专属词条。": "Obtain new plant: [[plant:EmeraldUmbrella]]\nView all its exclusive modifiers.",
    "获得新植物：[[plant:UltimateStarTorch]]\n可查看其全部专属词条。": "Obtain new plant: [[plant:UltimateStarTorch]]\nView all its exclusive modifiers.",
    "获得新植物：[[plant:UltimateSniperGatling]]\n可查看其全部专属词条。": "Obtain new plant: [[plant:UltimateSniperGatling]]\nView all its exclusive modifiers.",
    "获得新植物：[[plant:SuperThreePeater_sp]]\n可查看其全部专属词条。": "Obtain new plant: [[plant:SuperThreePeater_sp]]\nView all its exclusive modifiers.",
    "通用战术": "Universal Tactics",
    "从多个选项中自选一种战术词条": "Choose 1 tactical modifier from several options.",
    "抽取通用战术时有概率出现，概率受幸运影响；可自选一种仍有可领取等级的战术。": "Has a chance to appear when drawing Universal Tactics; affected by Luck; pick any tactic with available tiers.",
    "群攻-木桩": "AoE - Stake",
    "在场上生成一个木桩僵尸，木桩僵尸会把受到伤害的60%均摊给全场僵尸，可以使用僵尸手套移动木桩僵尸\n无法转移魅惑僵尸造成的伤害": "Spawn a Stake Zombie on field that splits 60% of damage taken across all zombies. Moveable with Zombie Glove.\nCannot transfer damage dealt by hypnotized zombies.",
    "尚未获得本组战术时可出现。尚未获得此级词条。": "Appears when this tactic set is not owned. Tier not yet acquired.",
    "木桩僵尸的均摊比例提升至100%": "Stake Zombie damage split ratio increased to 100%.",
    "已获得本组前 1 级词条后可出现。尚未获得此级词条。": "Appears after acquiring Tier 1 of this set. Tier not yet acquired.",
    "在场上多生成一个木桩僵尸": "Spawn an additional Stake Zombie on the field.",
    "已获得本组前 2 级词条后可出现。尚未获得此级词条。": "Appears after acquiring Tier 2 of this set. Tier not yet acquired.",
    "木桩-弱点洞悉": "Stake - Insight",
    "木桩僵尸受到伤害时会额外对全场血量最高的僵尸造成100%伤害": "When Stake Zombie takes damage, deals additional 100% damage to the highest HP zombie.",
    "已获得本组前 3 级词条后可出现。尚未获得此级词条。需在图鉴消耗300诸神币购买本战术满阶后才可出现。": "Appears after Tier 3 of this set. Tier not yet acquired. Requires purchasing Max Tier in Almanac for 300 Pantheon Coins.",
    "群攻-烈阳": "AoE - Solar Ray",
    "在场上生成一个阳光反应器，周期性对全场僵尸造成伤害": "Spawn a Solar Reactor that periodically deals damage to all zombies.",
    "阳光反应器的攻击间隔降低50%": "Solar Reactor attack interval reduced by 50%.",
    "阳光反应器的伤害提高100%": "Solar Reactor damage increased by 100%.",
    "烈阳-撕裂长空": "Solar Ray - Sky Rend",
    "阳光反应器攻击时额外释放太阳神流星落下": "Solar Reactor summons Solar God Meteors upon attacking.",
    "不朽-战锤": "Immortal - War Hammer",
    "锤子的伤害降低，但冷却时间降低至3秒": "Hammer damage reduced, but cooldown reduced to 3s.",
    "锤子的攻击范围大幅增加": "Hammer attack range significantly increased.",
    "进一步降低锤子的冷却时间": "Further reduces Hammer cooldown.",
    "战锤-千锤百炼": "War Hammer - Tempered",
    "锤子命中僵尸后，在原地生成一个大锤子，持续对僵尸造成伤害，一段时间后消失": "When Hammer hits a zombie, creates a giant hammer at target location that deals continuous damage.",
    "支援-飞艇": "Support - Airship",
    "获得一个迷你鱼型裂空机甲": "Obtain a Mini Fish-type Rift Mech.",
    "支援-裂空": "Support - Rift Cleave",
    "迷你鱼型裂空机甲齐射所需攻击数-1": "Attacks needed for Mini Fish Rift Mech volley -1.",
    "迷你鱼型裂空机甲攻击间隔降低": "Mini Fish Rift Mech attack interval reduced.",
    "裂空-苍穹之跃": "Rift Cleave - Sky Leap",
    "迷你鱼型裂空机甲齐射时的子弹在空中可持续分裂": "Bullets from Mini Fish Rift Mech volley continuously split in mid-air.",
    "铁幕-明月": "Iron Curtain - Bright Moon",
    "在场上生成一个月光反应器，周期性为全场植物回复生命值": "Spawn a Lunar Reactor that periodically restores HP to all plants.",
    "月光反应器的恢复量大幅提高": "Lunar Reactor healing amount significantly increased.",
    "月光反应器生效时为全场植物赋予1000护盾": "Lunar Reactor grants 1000 shield to all plants when triggering.",
    "明月-照彻万川": "Bright Moon - Rivers Illumined",
    "月光反应器生效时，为全场每株植物降下月华\n月华会秒杀3x3范围内的普通僵尸，并使植物无敌一段时间": "When Lunar Reactor triggers, calls down moonlight on all plants,\ninstantly eliminating standard zombies in a 3x3 area and granting invulnerability.",
    "铁幕-硬化": "Iron Curtain - Hardening",
    "全体植物受到的伤害降低20%": "All plants take 20% reduced damage.",
    "全体植物受到的伤害降低40%": "All plants take 40% reduced damage.",
    "全体植物受到的伤害降低60%": "All plants take 60% reduced damage.",
    "硬化-坚不可摧": "Hardening - Indestructible",
    "全体植物受到的伤害降低90%，生命值降低时在原地发射一枚攻击力等同于自身最大生命值的豌豆子弹\n若拥有僵尸词条正当防卫则改为受到的伤害降低99%": "All plants take 90% reduced damage and fire a pea bullet equal to max HP when damaged.\nTakes 99% reduced damage if Self Defense modifier is owned.",
    "幸运-交易": "Luck - Trade",
    "获得一次500幸运的词条抽取机会，随后扣除你25幸运": "Gain a 500-luck modifier draw opportunity, then deducts 25 Luck.",
    "获得一次1000幸运的词条抽取机会，随后扣除你50幸运": "Gain a 1000-luck modifier draw opportunity, then deducts 50 Luck.",
    "获得一次1500幸运的词条抽取机会，随后扣除你75幸运": "Gain a 1500-luck modifier draw opportunity, then deducts 75 Luck.",
    "交易-孤注一掷": "Trade - All In",
    "立即将你的幸运设置为250，刷新机会设置为5，并使幸运上限x3，且从此不再能抽取幸运与合理投资\n每次抽取词条时，获得25幸运，并额外获得当前幸运20%的幸运（最高100），选择木头、白银、黄金/随机、钻石/棱彩/诅咒将分别扣除20/40/60/100幸运，每次刷新消耗50幸运": "Instantly sets Luck to 250, rerolls to 5, triples Luck cap, and locks Luck / Sound Investment draws.\nEach draw grants +25 Luck and +20% current Luck (max 100); picking Wood/Silver/Gold/Diamond deducts 20/40/60/100 Luck; rerolls cost 50 Luck.",
    "幸运-宝藏": "Luck - Treasure",
    "立即生成一波2倍血量和速度的僵尸，全部消灭后获得一次500幸运的词条抽取机会": "Instantly spawn a wave of zombies with 2x HP and speed. Defeat them for a 500-luck draw.",
    "立即生成一波3倍血量和速度的僵尸，全部消灭后获得一次1000幸运的词条抽取机会": "Instantly spawn a wave of zombies with 3x HP and speed. Defeat them for a 1000-luck draw.",
    "立即生成一波4倍血量和速度的僵尸，全部消灭后获得一次1500幸运的词条抽取机会": "Instantly spawn a wave of zombies with 4x HP and speed. Defeat them for a 1500-luck draw.",
    "宝藏-双倍幸运": "Treasure - Double Luck",
    "立即使你当前幸运与幸运值上限翻倍\n若为负数则取绝对值后再翻倍，如-50幸运时：-50→100": "Instantly doubles current Luck and Luck cap.\nIf negative, takes absolute value before doubling (e.g. -50 -> 100).",
    "不朽-业火": "Immortal - Hellfire",
    "点击任意地方时，在点击位置释放业火爆炸，这个技能有10秒的冷却，如果击杀了僵尸则将冷却降为1秒": "Click anywhere to trigger a Hellfire explosion (10s CD). Killing a zombie reduces CD to 1s.",
    "业火获得100%伤害加成": "Hellfire gains +100% damage bonus.",
    "业火的冷却和击杀冷却降低50%": "Hellfire base and kill reset cooldowns reduced by 50%.",
    "业火-燃尽此生": "Hellfire - Life Ablaze",
    "业火可对植物造成伤害，击杀植物后后在全场释放火爆辣椒效果并刷新冷却，伤害基于该植物拿的总词条数而提高": "Hellfire can harm plants. Killing a plant triggers a screen-wide Jalapeno effect and refreshes CD, scaling with modifiers.",
    "支援-光棱": "Support - Prism",
    "获得一艘机械飞船，持续锁定并攻击最靠左的僵尸": "Obtain a Mechanical Spaceship that locks onto and attacks leftmost zombies.",
    "机械飞船的折射次数+1": "Mechanical Spaceship refraction count +1.",
    "机械飞船的折射次数+2": "Mechanical Spaceship refraction count +2.",
    "光棱-一枪穿雲": "Prism - Cloud Piercer",
    "光凌改为无限穿透，且折射可重复命中同一目标": "Prism attacks gain infinite piercing, and refractions can hit the same target repeatedly.",
    "护航-天罚": "Escort - Divine Retribution",
    "闪电将为你作战，间歇性对场上僵尸造成伤害": "Lightning fights for you, intermittently striking zombies.",
    "闪电的持续时间提高100%": "Lightning duration increased by 100%.",
    "闪电的攻击频率提高100%": "Lightning attack frequency increased by 100%.",
    "天罚-闪电风暴": "Divine Retribution - Lightning Storm",
    "闪电风暴将不间断的发动攻击": "Lightning Storm continuously attacks without interruption.",
    "沉淀-全能": "Accumulation - Almighty",
    "幸运提高25，全体伤害增幅提高10%，获得1次刷新机会，复活时间降低10%": "Luck +25, all damage +10%, gain 1 reroll, revival time reduced by 10%.",
    "幸运提高50，全体伤害增幅提高20%，获得2次刷新机会，复活时间降低20%": "Luck +50, all damage +20%, gain 2 rerolls, revival time reduced by 20%.",
    "幸运提高75，全体伤害增幅提高30%，获得3次刷新机会，复活时间降低30%": "Luck +75, all damage +30%, gain 3 rerolls, revival time reduced by 30%.",
    "全能-无懈可击": "Almighty - Flawless",
    "在场的全体植物获得500%生命值加成，300%独立伤害增幅，200%速度增幅，60%幸运一击率，150%幸运一击伤害": "All plants on field gain +500% HP, +300% independent damage, +200% speed, +60% lucky strike rate, +150% lucky strike damage.",
    "试炼：不破不立": "Trial: Destruction & Rebirth",
    "杀死你的全部植物，并将全场植物的独立伤害增幅和速度增幅减半\n在20波后重复这一操作，但改为增幅翻倍": "Sacrifices all plants and halves damage/speed boosts.\nRepeats after 20 waves, but doubles boosts instead.",
    "仅炼狱模式可出现；尚未获得此试炼词条。\n轮回阶段不超过 1；仅第 20 / 40 / 60 / 80 波可出现。": "Appears only in Purgatory mode; requires trial modifier unowned.\nReincarnation phase <= 1; only on waves 20 / 40 / 60 / 80.",
    "试炼：两极分化": "Trial: Polarization",
    "若你的幸运低于75，则立即将幸运设置为75非保底时，你的白银、黄金词条降级为木头品质，但钻石词条升级为棱彩品质": "If Luck < 75, sets Luck to 75. Non-pity Silver/Gold modifiers downgrade to Wood, but Diamond upgrades to Prismatic.",
    "仅炼狱模式可出现；尚未获得此试炼词条。": "Appears only in Purgatory mode; requires trial modifier unowned.",
    "试炼：傲慢": "Trial: Arrogance",
    "当你的植物在僵尸上方时，额外造成30%伤害，当你的植物在僵尸下方时，少造成30%伤害，方位以屏幕上下判定": "Plants above zombies deal +30% damage; plants below deal -30% damage.",
    "试炼：嫉妒": "Trial: Envy",
    "当僵尸血量高于50%时，额外造成30%伤害，当僵尸血量低于50%时，少造成30%伤害": "Deals +30% damage when zombie HP > 50%; deals -30% damage when zombie HP < 50%."
}

PANTHEON_REGEXS: dict[str, str] = {
    # Route headers
    r"^路线\s*(\d+)\s*/\s*(.*?)\s*·\s*(\d+)诸神币$": "Path {1} / {2} · {3} Pantheon Coins",
    r"^路线\s*(\d+)\s*/\s*(.*?)\s*·\s*(.*)$": "Path {1} / {2} · {3}",
    r"^路线\s*(\d+)\s*/\s*(.*)$": "Path {1} / {2}",
    r"^路线\s*(\d+)\s*$": "Path {1}",

    # Paths & Evolution
    r"(\d+)\s*条进化路线\s*·\s*点击卡牌查看词条": "{1} Evolution Paths · Click card to view modifiers",
    r"可获得词条\s*(\d+)\s*项": "Available Modifiers: {1}",
    r"(.*?)·\s*最多\s*(\d+)\s*次(.*)": "{1}· Max {2} times{3}",

    # Upgrade bonuses
    r"(.*?)获得(\d+(?:\.\d+)?)%独立伤害增幅(.*)": "{1} gains {2}% independent damage increase {3}",
    r"(.*?)获得(\d+(?:\.\d+)?)%速度增幅(.*)": "{1} gains {2}% speed increase {3}",
    r"普通品质基准[，,]实际增幅随品质变化[。.]": "based on Common quality; actual bonus scales with quality.",

    # Currency
    r"^诸神币\s*(\d+)$": "Pantheon Coins {1}",
    r"^诸神币[：:]\s*(\d+)$": "Pantheon Coins: {1}",
    r"^(\d+)\s*诸神币$": "{1} Pantheon Coins",
    r"^(\d+)\s*币$": "{1} Coins",

    # Role prefixes
    r"^基础植物\s*·\s*(.*)$": "Base Plant · {1}",
    r"^终端植物\s*·\s*(.*)$": "Terminal Plant · {1}",
}


def main():
    with STRINGS_PATH.open("r", encoding="utf-8") as f:
        strings = json.load(f)

    with REGEXS_PATH.open("r", encoding="utf-8") as f:
        regexs = json.load(f)

    orig_str_count = len(strings)
    orig_reg_count = len(regexs)

    strings.update(PANTHEON_STRINGS)
    regexs.update(PANTHEON_REGEXS)

    with STRINGS_PATH.open("w", encoding="utf-8") as f:
        json.dump(strings, f, ensure_ascii=False, indent=2)

    with REGEXS_PATH.open("w", encoding="utf-8") as f:
        json.dump(regexs, f, ensure_ascii=False, indent=2)

    print(f"Updated translation_strings.json: {orig_str_count} -> {len(strings)} (+{len(strings) - orig_str_count})")
    print(f"Updated translation_regexs.json: {orig_reg_count} -> {len(regexs)} (+{len(regexs) - orig_reg_count})")


if __name__ == "__main__":
    main()
