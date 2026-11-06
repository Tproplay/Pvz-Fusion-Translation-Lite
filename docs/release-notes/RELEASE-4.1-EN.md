# Plants vs. Zombies: Fusion v4.1 — English Release (Hotfix 2 - PC & Android)

A complete English translation release of **Plants vs. Zombies: Fusion (植物大战僵尸: 融合版) v4.1** for both Windows PC and Android.

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
| **PC (Windows)** | [`PvZ-Fusion-4.1-English-PC.zip`](https://github.com/Tproplay/Pvz-Fusion-Translation-Lite/releases/tag/v4.1) | 467.48 MB | `637aa89c32ea6f5c7f1a93bde4e0cc009796302e6ff7b3feb15ba881b9fd0895` | [PC Drive Mirror](https://drive.google.com/file/d/1icQjixqbtUE6k0XM9ehCD_hJL30vs-3R/view?usp=sharing) |
| **Android** | [`PvZ-Fusion-4.1-English-Android.apk`](https://github.com/Tproplay/Pvz-Fusion-Translation-Lite/releases/tag/v4.1) | 599.88 MB | `901382841cec2bc5c733d740f3b7dadd419c11ba342f41348e622b636ca140d7` | [Android Drive Mirror](https://drive.google.com/file/d/1iu52ubJdl3rYl-Umgw2sevTtHhAIdemU/view?usp=sharing) |

### 🌐 Google Drive Release Folder
- [Version 4.1 Folder](https://drive.google.com/drive/folders/1vFkBmV5aZXHBiYlVDd9H6xjclvs_G8fk?usp=sharing)
