"""Merge extra translation strings and remove redundant files."""

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
STRINGS_DIR = BASE_DIR / "translation-data" / "Strings"
DUMPS_DIR = BASE_DIR / "translation-data" / "Dumps"

CUSTOM_LEVEL_REGEXS = {
    r"^<size=20>点击格子的植物所在区域面积为：([^\s]+)": r"<size=20>Area of plant at clicked tile: $1",
    r"^<size=20>在<color=yellow>第([^\s]+)波</color>时，检测所有地刺花盆上的植物面积：\n如果该植物所在的区域面积<color=red>不为([^\s]+)，则在对应地刺花盆上产生3次小丑爆炸\n</color>你可以随时按<color=yellow>H键</color>来重新显示这条信息": r"<size=20>At <color=yellow>Wave $1</color>, check the area of plants on all Spikeweed Flower Pots:\nIf the plant's area is <color=red>not $2, Jack-in-the-box will explode 3 times on that Spikeweed Flower Pot.\n</color>Press <color=yellow>H</color> anytime to show this info again.",
    r"^<size=20>点击格子的植物所在区域面积为：([^\s]+)<size=20>距离下次面积判定剩余波次：([^\s]+)<size=20>    下次判定的需求面积：([^\s]+)": r"<size=20>Area of plant at clicked tile: $1 <size=20>Waves until next area check: $2 <size=20>   Required area for next check: $3",
    r"^<size=20>点击格子的植物所在区域面积为：([^\s]+)\n<size=20>距离下次面积判定剩余波次：([^\s]+)<size=20>    下次判定的需求面积：([^\s]+)": r"<size=20>Area of plant at clicked tile: $1\n<size=20>Waves until next area check: $2 <size=20>   Required area for next check: $3",
}

CUSTOM_LEVEL_STRINGS = {
    "<size=22>受事件机制影响，该关卡无法在第10列种植植物": "<size=22>Due to event rules, plants cannot be planted in column 10 in this level.",
    "<size=18>......你是自己融合了一个地刺花盆吗，你要知道地刺花盆是不会参与面积计算的\n而且，到了特定波次<color=red>所有地刺花盆</color>上的植物都会进行面积判定，所以我觉得你最好还是把它铲了.......": "<size=18>...Did you fuse a Spikeweed Flower Pot yourself? You should know Spikeweed Flower Pots don't count toward area calculations.\nAlso, at specific waves, plants on <color=red>ALL Spikeweed Flower Pots</color> will undergo area checks, so you really should shovel it...",
    "<size=20>受事件影响，此关卡禁用玩偶南瓜": "<size=20>Due to event rules, Jack-in-the-box Pumpkin is disabled in this level.",
    "<size=18><size=18>......如果你没听懂的话，这个关卡融合地刺花盆是没有任何好处的\n它不仅没有攻击力还会给你多添加一个面积负担......懂了吗": "<size=18>...In case you didn't understand, fusing a Spikeweed Flower Pot gives you zero benefit in this level.\nIt has no attack power and only adds an extra area burden... Understood?",
    "<size=18>lol那就随你了，我到底为什么要浪费时间给地刺花盆写这么多提示": "<size=18>lol fine, suit yourself. Why did I even waste my time writing so many hints for Spikeweed Flower Pot...",
    "<size=20>进行面积判定时可能会略有卡顿，请稍作等候": "<size=20>There may be slight lag during area calculations, please wait a moment.",
    "<size=18>tip：小丑爆炸不会伤害到地刺花盆，保护好你自己种植的植物即可\n另外，地刺花盆<color=red>不会</color>参与面积计算，所有空格子的面积均视为0": "<size=18>Tip: Jack-in-the-box explosions won't damage Spikeweed Flower Pots; just protect your planted plants.\nAlso, Spikeweed Flower Pots <color=red>do not</color> count toward area calculations, and empty tiles have an area of 0.",
    "<size=18>tip：你可以使用南瓜或者花盆这类可叠种的植物来灵活调整面积": "<size=18>Tip: You can use stackable plants like Pumpkins or Flower Pots to adjust area flexibly.",
    "<size=18>如果在第5波前没有进行任何右键操作，游戏将开启<color=#79FF79>兼容模式</color>\n兼容模式启用后，你将可以通过种植植物卡片来测量特定格子的面积": "<size=18>If no right-click action is performed before Wave 5, <color=#79FF79>Compatibility Mode</color> will be enabled.\nOnce enabled, you can measure tile area by planting plant cards.",
    "<size=18><color=#79FF79>兼容模式已开启</color>\n你可以通过种植<color=#CF9E9E>多功能南瓜</color>来查看植物面积": "<size=18><color=#79FF79>Compatibility Mode Enabled</color>\nYou can plant <color=#CF9E9E>Multifunctional Pumpkin</color> to check plant area.",
}

TALENT_TITLES = {
    "0_0\n梦的开始": "0_0\nDream Begins",
    "1_1\n更多阳光": "1_1\nMore Sun",
    "2_2\n光合作用": "2_2\nPhotosynthesis",
    "3_2\n精打细算": "3_2\nCareful Budgeting",
    "4_1\n射击训练": "4_1\nShooting Practice",
    "5_2\n精准打击": "5_2\nPrecision Strike",
    "6_2\n绝对力量": "6_2\nAbsolute Power",
    "7_1\n坚不可摧": "7_1\nIndestructible",
    "8_2\n正当防卫": "8_2\nSelf Defense",
    "9_2\n铜墙铁壁": "9_2\nIron Wall",
    "10_1\n人工栽培": "10_1\nArtificial Cultivation",
    "11_2\n全息制冷": "11_2\nHolographic Cooling",
    "12_2\n至极手速": "12_2\nExtreme Hand Speed",
    "13_3\n光合作用II": "13_3\nPhotosynthesis II",
    "14_5\n光合作用III": "14_5\nPhotosynthesis III",
    "15_3\n精打细算II": "15_3\nCareful Budgeting II",
    "16_5\n精打细算III": "16_5\nCareful Budgeting III",
    "17_3\n精准打击II": "17_3\nPrecision Strike II",
    "18_5\n精准打击III": "18_5\nPrecision Strike III",
    "19_3\n绝对力量II": "19_3\nAbsolute Power II",
    "20_5\n绝对力量III": "20_5\nAbsolute Power III",
    "21_3\n正当防卫II": "21_3\nSelf Defense II",
    "22_5\n正当防卫III": "22_5\nSelf Defense III",
    "23_3\n铜墙铁壁II": "23_3\nIron Wall II",
    "24_5\n铜墙铁壁III": "24_5\nIron Wall III",
    "25_3\n全息制冷II": "25_3\nHolographic Cooling II",
    "26_5\n全息制冷III": "26_5\nHolographic Cooling III",
    "27_3\n至极手速II": "27_3\nExtreme Hand Speed II",
    "28_5\n至极手速III": "28_5\nExtreme Hand Speed III",
    "29_5\n返璞归真I": "29_5\nReturn to Simplicity I",
    "30_10\n返璞归真II": "30_10\nReturn to Simplicity II",
    "31_15\n返璞归真III": "31_15\nReturn to Simplicity III",
    "32_5\n勤能补拙": "32_5\nDiligence Makes Up",
    "33_10\n超光速提拔": "33_10\nFTL Promotion",
    "34_15\n超级-白天": "34_15\nSuper - Day",
    "35_15\n超级-黑夜": "35_15\nSuper - Night",
    "36_10\n超级-泳池": "36_10\nSuper - Pool",
    "37_5\n超级-浓雾": "37_5\nSuper - Fog",
    "38_30\n超级-屋顶": "38_30\nSuper - Roof",
    "39_0\n深度探索": "39_0\nDeep Exploration",
    "40_0\n新的开始": "40_0\nNew Beginning",
    "41_5\n疾速狂热": "41_5\nSpeed Frenzy",
    "42_5\n疾速狂热II": "42_5\nSpeed Frenzy II",
    "43_10\n爽快射击": "43_10\nExhilarating Shooting",
    "44_5\n生命偷取": "44_5\nLifesteal",
    "45_5\n生命偷取II": "45_5\nLifesteal II",
    "46_10\n燃血": "46_10\nBlood Burn",
}

GAMEPLAY_PROMPTS = {
    "<color=red>旅行羁绊：": "<color=red>Travel Synergies: ",
    "\n\n尚未拥有这个词条": "\n\nModifier not yet owned",
    "\n\n该词条已拥有{0}个": "\n\nAlready owned: {0}",
    "\n<color=yellow>奖励：": "\n<color=yellow>Reward: ",
    "\n<size=85%>本局获得：{0}诸神币": "\n<size=85%>Earned this run: {0} God Coins",
    "\n不死": "\nUndying",
    "\n不死：{0}秒": "\nUndying: {0}s",
    "\n冷却：{0}秒": "\nCooldown: {0}s",
    "\n\n点击上方“节点说明”查看端口与连接例子。": "\n\nClick 'Node Info' above to view ports and connection examples.",
    "\n\n但": "\n\nBut",
    "\n但也开到了一些僵尸": "\nBut also uncovered some zombies",
    " 第{0}轮": " Round {0}",
    "仓库可用容量不足": "Insufficient storage capacity",
    "仓库等级：{0}     容量：{1}": "Storage Level: {0}     Capacity: {1}",
    "不可重命名默认存档": "Cannot rename default save",
    "不能使用默认存档名称": "Cannot use default save name",
    "下载关卡 ": "Download Level ",
    "主场景": "Main Scene",
    "{0}：剩余时间：{1:F0}秒": "{0}: Remaining Time: {1:F0}s",
    "产生阳光：{0}": "Produce Sun: {0}",
    "击杀僵尸：{0}": "Kill Zombies: {0}",
    "平均伤害：{0}": "Average Damage: {0}",
    "消耗阳光：{0}": "Spend Sun: {0}",
    "种植植物：{0}": "Plant Plants: {0}",
    "死亡植物：{0}": "Lost Plants: {0}",
    "铲除植物：{0}": "Shovel Plants: {0}",
    "魅惑僵尸：{0}": "Charm Zombies: {0}",
    "全体植物获得{0:F0}%伤害增幅\n当前增幅：{1:F0}%": "All plants gain {0:F0}% damage bonus\nCurrent Bonus: {1:F0}%",
    "相似度：{0:P1}\n强度：{1:F2}\n选择这株植物": "Similarity: {0:P1}\nPower: {1:F2}\nSelect this plant",
    "获得植物：{0}\n强度 = {1:F2}\n相似度 = {2}": "Obtain Plant: {0}\nPower = {1:F2}\nSimilarity = {2}",
}

GODS_EVOLVED_MODS = {
    "【倒反天罡】：究极系列植物的攻击与韧性减少90%，其他植物的攻击与韧性增加39倍，速度增加2倍": "[Reversal of Heaven]: Ultimate series plants have attack and toughness reduced by 90%; other plants have attack and toughness increased by 39x, and speed increased by 2x.",
    "【净化】：可以在查看词条界面消除1个非领袖僵尸词条\n※使用后可再次获取": "[Purify]: You can remove 1 non-leader zombie modifier in the modifier view screen.\n* Can be obtained again after use.",
    "【动量同调】：植物每拥有1%攻速加成，就获得1%攻击力加成": "[Momentum Sync]: For every 1% attack speed bonus a plant has, it gains 1% attack power.",
    "【定时炸弹】：魅惑僵尸死亡时会产生爆炸，对附近僵尸造成自身1.5倍韧性的伤害": "[Time Bomb]: When a charmed zombie dies, it explodes, dealing damage equal to 1.5x its toughness to nearby zombies.",
    "【排山倒海】：一种种一列": "[Overwhelming Force]: Plant an entire column at once.",
    "【爽快射击】：植物射击50次后（投手需要的次数减半），接下来的1秒内获得无限射速": "[Exhilarating Shooting]: After a plant shoots 50 times (halved for lobbed-shot plants), it gains infinite attack speed for the next 1 second.",
    "【生命偷取】：植物获得1%生命偷取，作用于全场血量百分比最低的植物": "[Lifesteal]: Plants gain 1% lifesteal, applied to the plant with the lowest HP percentage.",
    "【绝对力量】：当本类型植物造成的总伤害为全场最高时，每次攻击额外造成30%原伤害的真实伤害": "[Absolute Power]: When this plant type has dealt the highest total damage, each attack deals an additional 30% of original damage as true damage.",
    "【缩小射线】：迷你小鬼国王将会随同作战。每10秒将一定数量的僵尸转化为鸡骑士或鸡快艇。与原型领袖共场时，转化数量上限翻倍。本系列词条只会生效一个": "[Shrink Ray]: Mini Imp King will join the battle. Every 10s, converts a number of zombies into Chicken Riders or Chicken Speedboats. Maximum converted count is doubled when on field with the original Leader. Only one modifier from this series can be active.",
    "【缩小射线】：迷你渊海三叉戟将会随同作战。每5秒向前方投出三叉戟，在穿刺及爆炸时伤害僵尸。与原型领袖共场时，每10秒在每行投出4个三叉戟。本系列词条只会生效一个": "[Shrink Ray]: Mini Abyssal Trident will join the battle. Every 5s, hurls tridents forward, damaging zombies upon piercing and exploding. Every 10s, hurls 4 tridents in each row when on field with the original Leader. Only one modifier from this series can be active.",
    "【缩小射线】：迷你玩偶匣皇后将会随同作战。每15秒随机触发一种：召唤小丑王僵尸、向前方扔出大量玩偶匣炸弹、在每个僵尸脚下引发玩偶匣爆炸。本系列词条只会生效一个": "[Shrink Ray]: Mini Jack-in-the-box Queen will join the battle. Every 15s, randomly triggers one: summons Clown King Zombie, throws a barrage of Jack-in-the-box bombs forward, or triggers a Jack-in-the-box explosion under every zombie. Only one modifier from this series can be active.",
    "【缩小射线】：迷你雪原女皇将会随同作战。每3秒甩出雪球和小冰锥，伤害随场上寒冷与冻结的僵尸数量增加。与原型领袖共场时，发射的小冰锥无限穿透。本系列词条只会生效一个": "[Shrink Ray]: Mini Snowfield Queen will join the battle. Every 3s, flings snowballs and small ice spikes whose damage increases with the number of chilled and frozen zombies. Ice spikes gain infinite piercing when on field with the original Leader. Only one modifier from this series can be active.",
    "【缩小射线】：迷你鱼型裂空机甲将会随同作战。使植物方飞艇炸弹伤害增加。每1.5秒发射炮弹，每3次在每行发射。与原型领袖共场时，自身攻速翻倍。本系列词条只会生效一个": "[Shrink Ray]: Mini Fishborne Sky-Cleaver Mech will join the battle. Increases plant Airship Bomb damage. Fires cannonballs every 1.5s, firing in every row every 3 shots. Attack speed is doubled when on field with the original Leader. Only one modifier from this series can be active.",
    "【缩小射线】：迷你黑曜石巨人将会随同作战。大范围锤击会损伤植物并暂时提供90%减伤，且以此增加对僵尸的威力。与原型领袖共场时，锤击频率提升。本系列词条只会生效一个": "[Shrink Ray]: Mini Obsidian Gargantuar will join the battle. Wide-range smashes damage plants while granting them temporary 90% damage reduction, boosting smash power against zombies. Smash frequency increases when on field with the original Leader. Only one modifier from this series can be active.",
    "【缩小射线】：迷你黑橄榄大帅将会随同作战。快速发射小铁豆。每20秒召唤一列迷你战马冲杀僵尸并生成巫毒虚影。与原型领袖共场时，召唤战马所需时间减半。本系列词条只会生效一个": "[Shrink Ray]: Mini Black Olive Supreme Commander will join the battle. Rapidly fires small iron peas. Every 20s, summons a column of mini warhorses to charge through zombies and create voodoo phantoms. Summon cooldown is halved when on field with the original Leader. Only one modifier from this series can be active.",
    "【缩小射线】：迷你黑橄榄将军将会随同作战。在血量比例最低的植物处摇旗，使附近植物回复血量、僵尸受伤增加。与原型领袖共场时，将提供回血改为提供护盾。本系列词条只会生效一个": "[Shrink Ray]: Mini Black Olive General will join the battle. Waves flag at the plant with the lowest HP percentage, healing nearby plants and increasing damage taken by zombies. Grants shields instead of healing when on field with the original Leader. Only one modifier from this series can be active.",
    "【诸神黄昏】：获得究极剑仙杨桃的使用权限": "[Ragnarok]: Unlock access to Ultimate Sword Immortal Starfruit.",
    "【贪婪诅咒】：植物卡牌不再消耗冷却，但阳光消耗x15且每次使用后损失当前阳光的一半": "[Curse of Greed]: Plant cards have no cooldown, but Sun cost is multiplied by 15x and half of your current Sun is lost after each use.",
    "【过载】：僵尸一段时间没有受到攻击后，下次受到的伤害大幅增加": "[Overload]: If a zombie has not taken damage for a period of time, the next damage it receives is drastically increased.",
    "三尺之寒：\n僵尸解除冻结时受到30%当前生命值的伤害": "Extreme Frost:\nWhen a zombie unfreezes, it takes damage equal to 30% of its current HP.",
    "不屈：阿尔法僵尸小队能无限次从濒死中复苏": "Indomitable: Alpha Zombie Squad can revive from near-death infinitely.",
    "不朽-业火：业火的冷却和击杀冷却降低50%": "Immortal - Hellfire: Hellfire's cooldown and kill cooldown are reduced by 50%.",
    "不朽-业火：业火获得100%伤害加成": "Immortal - Hellfire: Hellfire gains +100% damage bonus.",
    "不朽-业火：点击任意地方时，在点击位置释放业火爆炸，这个技能有10秒的冷却，如果击杀了僵尸则将冷却降为1秒": "Immortal - Hellfire: Clicking anywhere unleashes a Hellfire explosion at that location with a 10s cooldown. If it kills a zombie, the cooldown is reduced to 1s.",
    "不朽-战锤：进一步降低锤子的冷却时间": "Immortal - War Hammer: Further reduces Mallet cooldown.",
    "不朽-战锤：锤子的伤害降低，但冷却时间降低至3秒": "Immortal - War Hammer: Mallet damage is reduced, but cooldown is reduced to 3s.",
    "不朽-战锤：锤子的攻击范围大幅增加": "Immortal - War Hammer: Mallet attack range is drastically increased.",
    "不死图腾：下一次僵尸进家时，无视僵尸进家，持续3秒，并强制击退全场僵尸至底线": "Undying Totem: The next time a zombie enters the house, ignore defeat for 3s and knock back all zombies to the spawn line.",
    "业火-燃尽此生：业火可对植物造成伤害，击杀植物后后在全场释放火爆辣椒效果并刷新冷却，伤害基于该植物拿的总词条数而提高": "Hellfire - Burning Life: Hellfire can damage plants. Killing a plant triggers a Jalapeno effect across the whole field and refreshes cooldown, with damage scaled by the total modifiers that plant possessed.",
    "全副武装：游戏过程中可以在背包选择你的植物": "Fully Armed: You can choose your plants in your backpack during the game.",
    "全息制冷：卡牌冷却减半": "Holographic Cooling: Card cooldowns are halved.",
    "共生之礼：当你首次获得两个一样的植物时，额外获得一个该植物卡牌": "Gift of Symbiosis: When you obtain two identical plants for the first time, gain an extra card of that plant.",
    "关卡特性：手推车冷却降低至3秒": "Level Trait: Lawnmower cooldown reduced to 3s.",
    "内讯不达：植物显血功能将被禁用": "Internal Blindness: Plant HP display will be disabled.",
    "冷冻冬眠：植物复活后被强制冻结3秒": "Cryo Hibernation: Plants are forcefully frozen for 3s upon reviving.",
    "力大砖飞：\n植物方造成的樱桃爆炸伤害x3": "Brute Force:\nPlant Cherry explosions deal 3x damage.",
    "势不可挡：樱桃机枪读报僵尸愤怒的时候会无视植物\n未选取时，究极Z教授获得1份备用报纸": "Unstoppable: Cherry Gatling Newspaper Zombie ignores plants when enraged.\nWhen not chosen, Ultimate Professor Z gains 1 spare newspaper.",
    "受击保护：僵尸前100次受伤后，在0.2秒内免疫不高于上次受伤值的伤害": "Hit Protection: After taking damage for the first 100 times, zombies become immune to damage not exceeding the previous damage value for 0.2s.",
    "合金舞台：究极舞台巡演车获得50%减伤": "Alloy Stage: Ultimate Stage Tour Bus gains 50% damage reduction.",
    "国王特权：究极小鬼国王闪避伤害时回复500点生命值": "King's Privilege: Ultimate Imp King recovers 500 HP when dodging damage.",
    "复制中心：模仿者冷却时间降低至50秒": "Cloning Center: Imitater cooldown reduced to 50s.",
    "小丑派对：僵尸血量低于5%时受击则立即自爆（对领袖和boss无效）": "Clown Party: When a zombie's HP falls below 5%, taking damage instantly triggers self-destruction (ineffective against Leaders and Bosses).",
    "小鬼当家：非boss僵尸的生命值和体型降低30%，但速度提高100%": "Home Alone: Non-boss zombies have HP and size reduced by 30%, but speed increased by 100%.",
    "幸运-宝藏：立即生成一波2倍血量和速度的僵尸，全部消灭后获得一次500幸运的词条抽取机会": "Lucky - Treasure: Instantly spawns a wave of zombies with 2x HP and speed; defeating all grants 1 modifier draw with 500 Luck.",
    "幸运-宝藏：立即生成一波3倍血量和速度的僵尸，全部消灭后获得一次1000幸运的词条抽取机会": "Lucky - Treasure: Instantly spawns a wave of zombies with 3x HP and speed; defeating all grants 1 modifier draw with 1000 Luck.",
    "幸运-宝藏：立即生成一波4倍血量和速度的僵尸，全部消灭后获得一次1500幸运的词条抽取机会": "Lucky - Treasure: Instantly spawns a wave of zombies with 4x HP and speed; defeating all grants 1 modifier draw with 1500 Luck.",
    "幽灵舞步：舞王指挥官的滑步会无视植物阻挡": "Ghost Step: Dancing Commander's slide ignores plant obstacles.",
    "应有尽有：获得一个南瓜箱子，里面装有非常多的究极植物": "Everything You Need: Gain a Pumpkin Chest containing numerous Ultimate plants.",
    "强化统领：领袖僵尸获得30%血量和速度加成": "Enhanced Command: Leader zombies gain +30% HP and speed bonus.",
    "强尸健体：僵尸每轮的韧性成长倍率由20%增加至30%": "Zombie Fitness: Zombie toughness growth rate per round increases from 20% to 30%.",
    "强心针：植物受到治疗后，3秒内每秒回复5%韧性的血量，此效果期间不会重复触发": "Adrenaline Shot: After being healed, plants recover 5% max toughness HP per second for 3s (does not re-trigger during this effect).",
    "忍无可忍：僵尸被同一种控制异常连续停止行动5秒后，在3秒内免疫任何控制异常": "At Wit's End: If a zombie is immobilized by the same crowd control for 5 consecutive seconds, it becomes immune to all CC for 3s.",
    "怒不可遏：樱桃机枪读报僵尸免疫绝大多数状态异常\n未选取时，究极Z教授获得1份备用报纸": "Uncontainable Rage: Cherry Gatling Newspaper Zombie is immune to most status anomalies.\nWhen not chosen, Ultimate Professor Z gains 1 spare newspaper.",
    "急行军：第一波僵尸刷新时间降低至5秒，僵尸刷新间隔降低至15秒": "Forced March: First wave spawn delay reduced to 5s; wave spawn interval reduced to 15s.",
    "战个痛快：刷新间隔缩短，每次刷新僵尸时，有概率重新刷新本波僵尸，概率随波次增加": "Fight to the Fullest: Spawn interval shortened; each wave has a chance to re-spawn, with chance increasing with waves.",
    "战力飙升：获得一个随机的究极植物，每一波僵尸出现时，该植物获得25%伤害加成，25%血量加成，10%速度加成": "Surging Power: Gain a random Ultimate plant; whenever a zombie wave appears, this plant gains +25% damage, +25% HP, and +10% speed.",
    "战锤-千锤百炼：锤子命中僵尸后，在原地生成一个大锤子，持续对僵尸造成伤害，一段时间后消失": "War Hammer - Masterforged: When Mallet hits a zombie, creates a giant hammer at that location that continuously damages zombies before vanishing.",
    "承载上限：你的植物数量不能超过120": "Carrying Limit: Your plant count cannot exceed 120.",
    "护航-天罚：闪电将为你作战，间歇性对场上僵尸造成伤害": "Escort - Divine Punishment: Lightning fights for you, intermittently striking zombies on the field.",
    "拆分：植物手套原地点击已选取的植物时，会花费500阳光将其按融合路线拆解成卡牌，冷却20秒": "Disassemble: Clicking a selected plant in place with Plant Glove spends 500 Sun to disassemble it into cards along its fusion tree (20s cooldown).",
    "拱卫：每只黑橄榄巨象在场时，都会使全体领袖僵尸获得100点护甲": "Bulwark: Each Black Olive Mammoth on the field grants +100 armor to all Leader zombies.",
    "支援-光棱：获得一艘机械飞船，持续锁定并攻击最靠左的僵尸": "Support - Prism: Gain a mechanical airship that continuously locks onto and attacks the leftmost zombie.",
    "敌情不明：僵尸显血功能将被禁用": "Unknown Enemy: Zombie HP display will be disabled.",
    "斗转星移：每5波，使你的植物移动到随机位置": "Cosmic Shift: Every 5 waves, moves your plants to random positions.",
    "普适性威胁：非究极类僵尸获得100%血量和伤害加成，50%速度加成": "Universal Threat: Non-Ultimate zombies gain +100% HP and damage, and +50% speed.",
    "木桩-弱点洞悉：木桩僵尸受到伤害时会额外对全场血量最高的僵尸造成100%伤害": "Target Dummy - Weakness Insight: When Target Dummy takes damage, deals an additional 100% damage to the zombie with the highest HP.",
    "极速战备：手套的冷却速度翻倍，僵尸手套能且优先移动领袖僵尸": "Rapid Readiness: Glove cooldown speed doubled; Zombie Glove can and prioritizes moving Leader zombies.",
    "株连草芥：植物被击杀时，对3x3范围植物造成等同于自身韧性的伤害": "Guilt by Association: When a plant is destroyed, deals damage equal to its toughness to plants in a 3x3 area.",
    "格挡反击：僵尸闪避时对附近植物造成100%反伤，冷却3秒": "Parry Counter: When a zombie dodges, reflects 100% damage to nearby plants (3s cooldown).",
    "榜样激励：伤害统计面板排名第一的植物造成70%的原伤害，其他植物造成110%原伤害": "Role Model: The #1 plant on the damage scoreboard deals 70% of its normal damage; other plants deal 110%.",
    "正当防卫：僵尸受到伤害时，原地生成一个僵尸方的诅咒子弹，伤害为自身攻击力的50%，最低100，0.02秒内最多触发1次": "Self Defense: When a zombie takes damage, creates a zombie curse projectile at its tile dealing 50% of its attack power (min 100, max once per 0.02s).",
    "永久创伤：植物受到伤害后，会扣除伤害量10%的韧性，最多扣到基础韧性的40%（每轮刷新）": "Permanent Trauma: After taking damage, plants lose max toughness equal to 10% of damage taken, down to 40% of base toughness (refreshed each round).",
    "永眠之地：开局场上获得三列墓碑，旗帜波时，墓碑将会召唤本波僵尸": "Resting Place: The battle starts with 3 columns of graves; on flag waves, graves summon zombies of that wave.",
    "沉淀-全能：幸运提高25，全体伤害增幅提高10%，获得1次刷新机会，复活时间降低10%": "Precipitation - Versatile: +25 Luck, +10% all plant damage, +1 refresh chance, -10% revive time.",
    "沉淀-全能：幸运提高50，全体伤害增幅提高20%，获得2次刷新机会，复活时间降低20%": "Precipitation - Versatile: +50 Luck, +20% all plant damage, +2 refresh chances, -20% revive time.",
    "沉淀-全能：幸运提高75，全体伤害增幅提高30%，获得3次刷新机会，复活时间降低30%": "Precipitation - Versatile: +75 Luck, +30% all plant damage, +3 refresh chances, -30% revive time.",
    "烈阳-撕裂长空：阳光反应器攻击时额外释放太阳神流星落下": "Blazing Sun - Tear the Sky: Solar Reactor releases Ra's falling meteors when attacking.",
    "煞气爆发：千年尸王死亡时的爆炸会造成物理伤害": "Malice Eruption: Thousand-Year Corpse King's death explosion deals physical damage.",
    "爆炸保护：僵尸方的小丑爆炸伤害降低至1000": "Explosion Protection: Zombie Jack-in-the-box explosion damage is capped at 1000.",
    "生化危机：植物消失时，在原地生成一只随机僵尸，该僵尸获得额外的血量和速度加成": "Biohazard: When a plant disappears, spawns a random zombie at its tile with extra HP and speed bonuses.",
    "百鬼夜行：每一波出现的僵尸数量最大值增加到100": "Night Parade of 100 Demons: Maximum zombie count per wave increased to 100.",
    "真正的樱桃炸弹：植物方的樱桃爆炸伤害不会低于1800，范围扩大且造成灰烬伤害": "True Cherry Bomb: Plant Cherry explosion damage is never lower than 1800, has larger radius, and deals ash damage.",
    "硬化-坚不可摧：全体植物受到的伤害降低90%，生命值降低时在原地发射一枚攻击力等同于自身最大生命值的豌豆子弹\n若拥有僵尸词条正当防卫则改为受到的伤害降低99%": "Hardening - Indestructible: All plants take 90% reduced damage and fire a pea projectile with damage equal to their max HP whenever HP decreases.\nIf zombie modifier Self Defense is active, damage reduction is increased to 99% instead.",
    "究极大喷菇专精II：魅惑僵尸的啃咬伤害×3": "Ultimate Fume-shroom Specialization II: Charmed zombie bite damage is multiplied by 3x.",
    "等价交换：\n超过持有上限的金钱会按照2:1的比例转化为阳光": "Equivalent Exchange:\nCoins exceeding capacity are converted into Sun at a 2:1 ratio.",
    "精英部队：每一轮出现的僵尸数量上限减半，但所有僵尸血量、攻击力x2": "Elite Force: Max zombie count per round halved, but all zombies have HP and attack doubled.",
    "终极时刻：植物造成的伤害翻倍": "Ultimate Hour: Plant damage is doubled.",
    "缓冲保护：僵尸受到的前50次伤害降低至1": "Buffer Protection: The first 50 instances of damage taken by zombies are reduced to 1.",
    "群攻-木桩：在场上多生成一个木桩僵尸": "AoE - Target Dummy: Spawns an extra Target Dummy on the field.",
    "群攻-木桩：在场上生成一个木桩僵尸，木桩僵尸会把受到伤害的60%均摊给全场僵尸，可以使用僵尸手套移动木桩僵尸\n无法转移魅惑僵尸造成的伤害": "AoE - Target Dummy: Spawns a Target Dummy that shares 60% of damage taken equally across all zombies. Can be moved with Zombie Glove.\nCannot transfer damage dealt by charmed zombies.",
    "群攻-木桩：木桩僵尸的均摊比例提升至100%": "AoE - Target Dummy: Target Dummy's shared damage ratio increases to 100%.",
    "群攻-烈阳：在场上生成一个阳光反应器，周期性对全场僵尸造成伤害": "AoE - Blazing Sun: Spawns a Solar Reactor that periodically damages all zombies.",
    "群攻-烈阳：阳光反应器的伤害提高100%": "AoE - Blazing Sun: Solar Reactor damage increased by 100%.",
    "群攻-烈阳：阳光反应器的攻击间隔降低50%": "AoE - Blazing Sun: Solar Reactor attack interval reduced by 50%.",
    "肉身成圣：魅惑僵尸获得500%啃咬伤害加成和80%减伤": "Flesh Ascendance: Charmed zombies gain +500% bite damage and 80% damage reduction.",
    "腐化契约：现在获得一张究极忧郁菇卡牌，如果种下他则视为接受挑战：\n在每行召唤3~6个随机的究极僵尸（包含一切可能）\n全部击败后，获得词条【腐化】": "Corrupted Pact: Gain an Ultimate Gloom-shroom card. Planting it accepts the challenge:\nSummons 3-6 random Ultimate zombies in every row.\nDefeating all grants modifier [Corruption].",
    "膨胀危机：非boss僵尸的生命值和体型提高60%，但速度降低60%": "Inflation Crisis: Non-boss zombies have HP and size increased by 60%, but speed reduced by 60%.",
    "至极手速：植物手套挪动植物不再消耗冷却；僵尸手套冷却-10秒，能且优先移动领袖僵尸": "Extreme Hand Speed: Plant Glove has no cooldown; Zombie Glove cooldown reduced by 10s, can move and prioritizes Leader zombies.",
    "致命一击：僵尸受到超过1800的伤害（减伤后）时额外受到1800伤害": "Fatal Strike: When a zombie takes over 1800 damage (after reductions), it takes an additional 1800 damage.",
    "英雄契约：现在获得一张多功能南瓜卡牌，如果种下他则视为接受挑战：\n在接下来的20波内，全体僵尸的数量翻倍\n随后将该植物所在格的全部植物升至3星": "Hero's Pact: Gain a Multifunctional Pumpkin card. Planting it accepts the challenge:\nFor the next 20 waves, all zombie counts are doubled.\nAfterwards, all plants on its tile are promoted to 3 Stars.",
    "英雄登场：获得一个超级寒冰机枪射手，他额外具有1500%伤害、血量加成，1000%速度加成，并获得一个极寒冰豆": "Hero's Arrival: Gain a Super Ice Gatling Peashooter with +1500% damage/HP, +1000% speed, and a Frost Bean.",
    "虎狼之师：非领袖僵尸获得30%血量和速度加成": "Fierce Army: Non-leader zombies gain +30% HP and speed bonus.",
    "融合召唤：使用手套将一个植物移动到其他同星级同类型的植物上时，会将该植物提升1级": "Fusion Summon: Moving a plant onto another plant of the same star tier and type using Glove upgrades it by 1 tier.",
    "规则之力：将全场僵尸击退至底线，然后秒杀全场僵尸": "Power of Rules: Knocks back all zombies to the spawn line, then instantly eliminates them.",
    "质变-小鬼当家：魅惑黑曜石巨人砸击时会生成魅惑黑曜石小鬼僵尸": "Qualitative Leap - Home Alone: Charmed Obsidian Gargantuar smashes spawn charmed Obsidian Imps.",
    "质变-毁灭：毁灭大嘴花攻击时没有吞噬僵尸也将释放爆炸，吞下则释放两次": "Qualitative Leap - Doom: Doom Chomper releases an explosion even without swallowing; releases two if swallowed.",
    "质变-火海：火神的子弹命中地面时也会生成火海，命中僵尸最多额外分裂2次": "Qualitative Leap - Sea of Fire: Vulcan projectiles create a sea of fire on ground impact, splitting up to 2 extra times on zombie hit.",
    "质变-神枪手：死神猎手每一发子弹都会造成爆头伤害": "Qualitative Leap - Sharpshooter: Every shot from Reaper Hunter deals headshot damage.",
    "质变-迸发：炮台在释放大招过程中额外释放4次火爆辣椒效果，每次造成50段伤害，每次伤害对敌方随机单体造成等同于炮台10000%攻击力的伤害": "Qualitative Leap - Outburst: Turret unleashes 4 additional Jalapeno blasts during its ultimate, each dealing 50 multi-hits of 10,000% turret ATK to a random target.",
    "起死回生：在僵尸进家的1.5秒内击杀这个僵尸，则不会使游戏失败": "Resurrection: Killing a zombie within 1.5s of entering the house prevents game over.",
    "轨迹多端：超级三叉戟僵尸现在无视伞类吸引，且随机挑选目标攻击": "Unpredictable Trajectory: Super Trident Zombie ignores umbrella redirection and attacks random targets.",
    "运斤如风：锤子冷却降低为6秒": "Swift Hammer: Mallet cooldown reduced to 6s.",
    "进阶空降：蹦极僵尸获得90%减伤，且有概率在第四列或更右侧空投究极僵尸": "Advanced Airdrop: Bungee Zombie gains 90% damage reduction and a chance to drop Ultimate zombies in column 4 or further right.",
    "远距离锁定：镭射幽浮的激光将攻击范围内最远处的植物": "Long-Range Lock-on: Laser UFO targets the furthest plant within range.",
    "连连看：两株相同植物位于邻行同列时获得50%攻击力加成和50%减伤": "Match-3: Two identical plants in adjacent rows of the same column gain +50% ATK and 50% damage reduction.",
    "适应之力：僵尸每次受到高于100（减伤后）的伤害时，获得1点护甲,最多获得1000": "Adaptability: When a zombie takes over 100 damage (after reductions), gains 1 armor (up to 1000).",
    "重症难题：植物受到的治疗量和护盾量减半": "Critical Dilemma: Healing and shields received by plants are halved.",
    "重装空袭：飞行僵尸获得100%血量加成": "Heavy Airstrike: Flying zombies gain +100% HP bonus.",
    "铁幕-明月：在场上生成一个月光反应器，周期性为全场植物回复生命值": "Iron Curtain - Moon: Spawns a Moonlight Reactor that periodically heals all plants.",
    "铁幕-明月：月光反应器生效时为全场植物赋予1000护盾": "Iron Curtain - Moon: Moonlight Reactor grants 1000 shield to all plants when active.",
    "铁幕-硬化：全体植物受到的伤害降低20%": "Iron Curtain - Hardening: All plants take 20% reduced damage.",
    "铁幕-硬化：全体植物受到的伤害降低40%": "Iron Curtain - Hardening: All plants take 40% reduced damage.",
    "铁幕-硬化：全体植物受到的伤害降低60%": "Iron Curtain - Hardening: All plants take 60% reduced damage.",
    "震地呼唤：特种武装巨人锤击会生成外表对应的武装小鬼僵尸": "Earthquake Call: Armed Gargantuar smashes spawn matching Armed Imps.",
    "饱和投射：超级三叉戟僵尸、冰封三叉戟僵尸攻击额外散射两发": "Saturation Barrage: Super Trident and Frozen Trident Zombies fire 2 extra scattered projectiles.",
    "高效恢复：植物获得20%治疗加成": "Efficient Recovery: Plants gain +20% healing bonus.",
    "黯淡无光：令你的阳光数归零": "Dim and Lightless: Sets your Sun to 0.",
}

REDUNDANT_FILES = [
    DUMPS_DIR / "custom_level_data.json",
    DUMPS_DIR / "custom_level_strings.json",
    DUMPS_DIR / "MD5Convert.txt",
    DUMPS_DIR / "MD5.json",
    DUMPS_DIR / "CustomLevels.json",
]

def main():
    # 1. Update translation_regexs.json
    regex_file = STRINGS_DIR / "translation_regexs.json"
    with open(regex_file, "r", encoding="utf-8") as f:
        regex_data = json.load(f)
    
    initial_regex_count = len(regex_data)
    regex_data.update(CUSTOM_LEVEL_REGEXS)
    with open(regex_file, "w", encoding="utf-8") as f:
        json.dump(regex_data, f, ensure_ascii=False, indent=2)
    print(f"Updated {regex_file}: {initial_regex_count} -> {len(regex_data)} regexes")

    # 2. Update translation_strings.json
    strings_file = STRINGS_DIR / "translation_strings.json"
    with open(strings_file, "r", encoding="utf-8") as f:
        strings_data = json.load(f)
    
    initial_strings_count = len(strings_data)
    strings_data.update(CUSTOM_LEVEL_STRINGS)
    strings_data.update(TALENT_TITLES)
    strings_data.update(GAMEPLAY_PROMPTS)
    strings_data.update(GODS_EVOLVED_MODS)

    with open(strings_file, "w", encoding="utf-8") as f:
        json.dump(strings_data, f, ensure_ascii=False, indent=2)
    print(f"Updated {strings_file}: {initial_strings_count} -> {len(strings_data)} strings")

    # 3. Remove redundant files
    removed_count = 0
    for file_path in REDUNDANT_FILES:
        if file_path.exists():
            file_path.unlink()
            print(f"Removed redundant file: {file_path.name}")
            removed_count += 1
        else:
            print(f"File already absent: {file_path.name}")
    print(f"Removed {removed_count} redundant files.")

if __name__ == "__main__":
    main()
