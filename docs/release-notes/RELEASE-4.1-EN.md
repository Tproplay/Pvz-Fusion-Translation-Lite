# Plants vs. Zombies: Fusion v4.1 — English Release (Hotfix 4 - PC & Android)

A complete English translation release of **Plants vs. Zombies: Fusion (植物大战僵尸: 融合版) v4.1** for both Windows PC and Android.

---

## 🚨 Hotfix 4 (Nov 17, 2026)
- **Plant & Zombie Renames**:
  - Reverted Plant 1486 from Floating Chomper back to **Flytrapper** (食蝇草 / 捕蝇草).
  - Renamed Plant 1484: Gloom-shroom + Gatling Pea -> **Gatling Gloom-shroom** (机枪曾哥).
  - Renamed Plant 1487: Spikeweed + Spikerock -> **Spike King** (地刺王).
  - Renamed Plant 1492: Blover + Fume-shroom -> **Blover Fume-shroom** (三叶大喷菇).
  - Renamed Plant 1493: Flower Pot + Fume-shroom -> **Potted Fume-shroom** (大喷盆).
  - Renamed Plant 1496: Melon-pult + Peashooter -> **Melon Peashooter** (西瓜豌豆射手).
  - Renamed Plant 1497: Scaredy-shroom + Threepeater -> **Triple Scaredy-shroom** (三联胆小菇).
  - Renamed Plant 1498: Squash + Sun-shroom -> **Squash-shroom** (窝瓜菇).
  - Renamed Plant 1499: Cabbage-pult + Peashooter -> **Cabbage Peashooter** (卷心菜豌豆射手).
  - Renamed Plant 1500: Scaredy-shroom + Winter Melon -> **Scaredy-melon** (胆小西瓜).
  - Renamed Plant 5006: Doom-shroom + Shatter-shroom -> **Ultimate Shatter-shroom** (终极碎裂菇).
  - Renamed Plant 5008: Magnet-shroom + Squash Wall-nut -> **Magnetic Squash-nut** (磁力窝瓜坚果).
  - Renamed Plant 313: Parallel Torchwood -> **Parallel Torchwood** (平行火炬树桩).
  - Renamed Zombie 134: Dolphin Rider + Football + Tall-nut -> **Football Dolphin Tall-nut Zombie** (橄榄海豚高坚果僵尸).
  - Renamed Zombie 135: Cherry War God Zombie -> **Cherry War God Zombie** (樱桃战神僵尸).
- **Harvest Mode Formatting & Nomenclature**:
  - Removed `<color=#BA55D3>` purple tags from all Harvest Mode plants (Seed IDs 300 to 313) for clean, unified rendering in seed selection and Almanac.
  - Standardized all occurrences of `Mystery Mode` to **Harvest Mode** across descriptions, guides, and text entries.
- **Suburban Almanac Layout Polish**:
  - Eliminated the double blank line gap between plant descriptions and fusion/conversion recipes across all 581 plants by stripping redundant leading newlines.
  - Reduced spacing before the Travel Synergies section (`Travel Synergies:`) from 2 blank lines to a clean 1 blank line gap for tight, legible formatting.

---

## 🚨 Hotfix 3 (Nov 8, 2026)
- **In-Game Changelog Typography**:
  - Injected `English.ttf` into `黑体` (SimHei, Font 7106), ensuring the in-game changelog dialogue (`NoticePauseMenu`) cleanly renders using the English PvZ font instead of the default Chinese font.
- **Missing UI & Level Strings Localization**:
  - Localized warehouse expansion alert: `完成第5关即可扩大仓库容量` / `完成第{0}关即可扩大仓库容量` -> **Complete Level {0} to expand storage capacity**.
  - Localized Custom Level Editor action button: `删除植物` -> **Delete Plant**.
  - Refined Whims of Fate modifier strings: `命运无常` -> **Whims of Fate: Each Modifier draw randomly rolls between -27 and +33 Luck**.
  - Normalized combat statistics: `总伤害` -> **Total Damage**.
  - Polished Suburban Almanac plant and zombie descriptions, equipment terms, and travel buffs.
- **Build & System Enhancements**:
  - Added transparent UTF-8 BOM (`utf-8-sig`) decoding across all build tools to prevent encoding issues when editing translation dictionaries.
  - Updated repository issue templates to automatically assign maintainers for prompt issue tracking.

---

## 🚨 Hotfix 2 (Nov 6, 2026)
- **Ingredient Reference & Plant Inspection Localization**:
  - Fully translated the fused plant inspection tab (`素材对照  {0}` -> **Ingredient Ref  {0}** / `素材对照` -> **Ingredient Ref**).
  - Localized the inspector subheader instructions: `悬停植物或装备图标查看详情；每份原始素材单独保留。` -> **Hover over plant or gear icons to view details. Each original ingredient is preserved individually.**
  - Localized individual ingredient labels (`素材 {0:00}` -> **Ingredient 01**, **Ingredient 02**), equipped gear labels (`已种装备` -> **Planted Gear**), and sync statuses (`与出战卡一致，无需同步` -> **Matches deployed card, no sync needed** / `同步状态：暂无对应出战卡` -> **Sync Status: No matching deployed card**).
- **Almanac Buff Placeholder Fix**:
  - Resolved an issue in the bundle builder where re-reading unpatched bytes during font size layout adjustment reverted the description TextMeshProUGUI in `AlmanacBuffMenu` (`PathID 206706`) back to the default Unity editor placeholder `文本文本`.

---

## 🚨 Hotfix 1 (Nov 5, 2026)
- **The Gods: Evolved Crash Fix**:
  - Resolved `GameLevel.RogueShooting.ShootingGroupBuff` static initializer crash on startup caused by runtime reflection and `Enum.Parse(typeof(AdvBuff), ...)` attempting to resolve translated internal enum identifiers.
  - Added strict protection to guarantee all 13 internal group keys (`业火`, `交易`, `光棱`, `全能`, `天罚`, `宝藏`, `战锤`, `明月`, `木桩`, `烈阳`, `硬化`, `裂空`, `铁卫`) remain untouched in IL2CPP metadata.
- **The Gods: Almanac & Plant Stats Localization**:
  - Localized stat category headers: `当前属性` -> **Current Stats**, `战斗属性` -> **Combat Stats**.
  - Normalized stat formatting templates: `属性计数：{0}\n` -> **Stat Count: {0}\n**, `攻击间隔：{0}秒\n` -> **Attack Interval: {0}s\n**. Excluded stat templates with `{0}` from modifier card parsing to eliminate unwanted `<nobr>` wrappers and fullwidth colons.
  - Fully translated plant upgrade paths: `质变：聚能弹道` -> **Ascend: Focused Trajectory**.
  - Localized custom plant description overrides across all entries in `ShootingAlmanacIndex`.
  - Cleaned up stray passive marker `被` from appearing before translated plant names (e.g. `被Apeacalypse`).
  - Improved Suburban Almanac buff description typography, vertical layout padding, and font scaling.
- **UI & Gameplay Polish**:
  - Resized Auto Wave button text to `125%` and formatted to clean single-line labels (`Auto Wave: On`, `Auto Wave: Off`, `Auto Wave: Forced`) to prevent awkward line breaks.
  - Replaced help screen with upscaled 2800×1200 high-resolution texture (`thanks.png`) with corrected keybind instructions.
  - Added full English translations for Magic Brush image recognition prompts, status banners, and network error messages.
  - Normalized overly long zombie names in Almanac headers.

---

## 🌟 What's New in v4.1

- **Updated to Official PvZ Fusion v4.1**:
  - Full support for the newly added v4.1 game content across both PC and Android platforms.
- **New Modes & Level Titles**:
  - **Plant Tycoon** (formerly Super Stack-Up / `超级叠叠乐`).
  - **Odyssey: Evolved** (`旅行：进化`).
  - **The Gods: Evolved** (`诸神进化`).
  - **Classic Tower Defense** (`经典塔防：进化`).
  - **Magic Brush** (`神笔马良`) stage and brush mechanics translated.
- **UI & Gameplay Localization**:
  - Fully translated in-game banners and parchment instructions for Magic Brush and Auto Next Wave (`自动下一波`).
  - Translated deployment restriction alerts (*"Only 1 of each plant type can be deployed. Drag to the matching slot to replace it."*).
  - Scratch cards updated to cleaner two-line button layout (**Uncommon Card** / `Refined Card`).
  - High-tier equipment cards (Diamond / Prismatic Flower Pots, Card Readers, and Coffee Beans) adjusted and auto-scaled for clean UI alignment.
- **Visuals & Bug Fixes**:
  - Restored missing Wrench tool icon and texture assets.
  - Aligned all Almanac entries, tips (`tips_fs.json`), and custom level editor help strings.

---

## 📦 Downloads & Verification

| Platform | File | Size | SHA-256 Checksum | Google Drive Mirror |
| :--- | :--- | :--- | :--- | :--- |
| **PC (Windows)** | [`PvZ-Fusion-4.1-English-PC.zip`](https://github.com/Tproplay/Pvz-Fusion-Translation-Lite/releases/tag/v4.1) | 468.59 MB | `2747cd05e2c899cebd19c94f2d79dbe4337ab0f9a6b74ef7102b30aa6456bba3` | [PC Drive Mirror](https://drive.google.com/file/d/1icQjixqbtUE6k0XM9ehCD_hJL30vs-3R/view?usp=sharing) |
| **Android** | [`PvZ-Fusion-4.1-English-Android.apk`](https://github.com/Tproplay/Pvz-Fusion-Translation-Lite/releases/tag/v4.1) | 597.16 MB | `d217f44adbb1e7303958c6464f8d74fa4cbcfcd4aa9236745cf23b32e1eb0e0a` | [Android Drive Mirror](https://drive.google.com/file/d/1iu52ubJdl3rYl-Umgw2sevTtHhAIdemU/view?usp=sharing) |

### 🌐 Google Drive Release Folder
- [Version 4.1 Folder](https://drive.google.com/drive/folders/1vFkBmV5aZXHBiYlVDd9H6xjclvs_G8fk?usp=sharing)
