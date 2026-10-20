# PvZ Fusion 4.0.5 Translation Architecture & Research Guide

This document records the architectural findings, binary layout specifications, and asset structures discovered during the development of the **Plants vs. Zombies: Fusion v4.0.5** dual-platform (PC & Android) English translation toolkit. It is intended for maintainers and automated coding agents continuing work on subsequent releases.

---

## 1. Engine & Binary Environment

| Component | Specification |
|---|---|
| **Game Title** | *Plants vs. Zombies: Fusion* (植物大战僵尸：融合版) |
| **Target Version** | v4.0.5 |
| **Engine** | Unity 2022.3.62f1 |
| **Scripting Backend** | IL2CPP (64-bit Windows PC & 64-bit / 32-bit ARM Android) |
| **IL2CPP Metadata Version** | Version 29 (32-bit integer header format) |
| **Data Payloads** | Exactly two primary payloads control 99%+ of all game text: <br>1. `data.unity3d` (Unity asset bundle)<br>2. `global-metadata.dat` (IL2CPP compiled string literals) |

---

## 2. Unity Bundle Architecture (`data.unity3d`)

The main Unity asset archive (`PlantsVsZombiesRH_Data/data.unity3d` on PC, `assets/bin/Data/data.unity3d` on Android) stores serialized assets, database `TextAsset` files, UI fonts, and in-game textures.

### A. Serialized UI Text Components
UI strings in PvZ Fusion are serialized across two distinct Unity component types:

1. **TextMesh Pro MonoBehaviours**:
   - `m_Script` PathIDs: `3797` and `2359` (and occasional variant 4104).
   - Serialized `m_text` field location: Byte offset **88** within the raw MonoBehaviour byte stream.
   - Serialization format: `<i` (4-byte signed length of UTF-8 encoded text) + `raw UTF-8 bytes` + `4-byte null padding alignment` (`(-len) & 3`).
   - Splicing: Component data can be sliced at `[TEXT_OFFSET : padded_end]` and replaced with a newly formatted length-prefixed, padded byte field without invoking full type-tree deserialization.

2. **UnityEngine.UI.Text MonoBehaviours**:
   - `m_Script` PathID: `1568`.
   - Serialized `m_Text` field location: Byte offset **144** within the raw byte stream.
   - Splicing: Follows the same length-prefixed, 4-byte aligned structure as TMP components.
   - Used for several primary level-selection and navigation buttons (`切换关卡组`, `返回索引`, `确认配装`, `前往商店`, `确定`, etc.).

3. **Runtime Navigation Backing Fields**:
   - Several UI components append raw serialized string fields at the tail of the raw MonoBehaviour byte buffer (e.g., `返回菜单` -> `Back to Menu`, `上一页` -> `Previous Page`, `下一页` -> `Next Page`, `回到索引` -> `Back to Index`).
   - These are patched using `replace_runtime_backing_text()` by checking for `endswith(serialized_string(source))`.

### B. TextAsset Databases
PvZ Fusion stores core gameplay databases as JSON `TextAsset` objects inside `data.unity3d`:

| TextAsset Name | PathID | Contents & Scope | Notes |
|---|---|---|---|
| `LawnStrings` | 1883 | 720 Plants (`plants` array) | Contains plant names, costs, cooldowns, and introductions. |
| `ZombieStrings` | 2773 | 235 Zombies (`zombies` array) | Contains zombie names, toughness, damage, and descriptions. |
| `DetailStrings` | 2356 | 47 Mechanics (`details` array) | Mechanics Almanac entries. Category types mapped via `TYPE_MAP`. |
| `LevelCreatorHelp` | 3378 | 11 Tutorial Topics (`topics` array) | **New in 4.0.5.** Tutorial guide for the Custom Level Editor. |
| `PlantEvolutionData` | 1297 | 27 Evolution Routes | Pantheon Evolution tree routes (`routeName` field). |
| `ShootingAlmanacIndex` | 2137 | 74 Almanac entries + Buff overrides | Tactical index title, description, condition, and `descriptionOverride`. |
| `Goods` | 3169 | Zen Garden Shop items | Shop item descriptions (`datas` array). |
| `TalentData` | 3218 | 47 Talents (`talentDatas` array) | Talent names and descriptions. |

### C. Typography & Font Transplantation
The game uses a hybrid TMP and TrueType font setup:
- **Dynamic TMP FontAsset**: Located at PathID `187676`. When patched, its glyph table and character table are updated, and its font texture is synchronized with `English.ttf`.
- **TrueType Font Asset**: Located at PathID `197479` (`English.ttf`).
- **Platform Sizing Rules**:
  - **PC**: Strips `<size=...>` tags from Almanac entries, UI text, and button regexes. Because PC renders at high desktop resolutions, mobile `<size>` tags cause oversized, clipped text.
  - **Android**: Retains calibrated mobile font sizes to ensure readability on small handheld displays.

### D. Localized Textures
Textures are replaced directly inside `data.unity3d` by matching Texture2D names and byte dimensions:
- **Wave Start Banners**: `StartPlant`, `StartReady`, `StartSet`, `HugeWave`, `FinalWave`.
- **Comic Action Particles**: `Doom`, `Pow`, `Dong`, `guang`, `Sproing`, `SunExplosionPowie`, `ExplosionPowie`, `ExplosionSpudow`.
- **Menu Graphics**: `MainMenu3.0travel2`, `SZW`, `travel`, `版本更新`, and various wood button states.

---

## 3. IL2CPP Metadata Architecture (`global-metadata.dat`)

`global-metadata.dat` contains all compiled C# string literals used across game assemblies.

### A. Header Layout (Metadata v29)
In Unity 2022.3 IL2CPP v29, the string literal tables are indexed at byte offset **8** of the metadata header:
```python
# struct.unpack_from('<4I', data, 8)
lookup_offset, lookup_size, data_offset, data_size = struct.unpack_from("<4I", data, 8)
```
- `lookup_offset` / `lookup_size`: The literal lookup index table (array of pairs: `uint32 length, uint32 relative_offset`).
- `data_offset` / `data_size`: The contiguous UTF-8 byte buffer holding literal text.

### B. Append-and-Redirect Translation Strategy
To prevent file corruption and maintain absolute binary stability:
1. The builder never mutates the original data segment in-place.
2. A newly rebuilt string literal buffer is appended once at **EOF** (End-of-File).
3. The lookup index table is rewritten so that each entry points to the new relative offset and byte length.
4. The header fields (`data_offset`, `data_size`, and file length) are updated cleanly.
5. In 4.0.5, **3,434 C# string literals** are successfully translated using this deterministic method.

### C. Dynamic Enum & Perk Renaming
Two critical gameplay features in 4.0.5 store English-facing text inside compiled metadata definitions:
1. **Plant Synergy Enums (`SynergyType`)**: 18 synergy display enums located dynamically by definition offset and renamed without changing their numeric enum values or memory layouts.
2. **Investment Odyssey Perks (`InvestBuff`)**: 42 perks located dynamically and renamed into English.

---

## 4. Custom Level Editor Architecture (4.0.5 Additions)

A major feature of v4.0.5 is the **Custom Level Editor** (关卡制作器 / 事件规则工具). Translating this feature revealed key architectural lessons:

1. **Dual UI Instantiation**:
   - Top-level toolbar buttons and mode entries (`经典塔防模式`) exist as serialized TextMesh Pro MonoBehaviours in `data.unity3d`.
   - Node inspectors, modal dialogs, check results, and list element selectors are **dynamically created by C# scripts at runtime**.
   - These dynamic UI strings come exclusively from `global-metadata.dat` string literals.

2. **Key Translated Subsystems**:
   - **Help Documentation**: 11 chapters stored in `LevelCreatorHelp` TextAsset.
   - **Graph Verification**: `图检查（点击问题定位节点）` ("Graph Check"), `检查通过：节点、端口、变量、默认值和同步循环均未发现问题。` ("Check passed...").
   - **More Tools Modal**: `查看全图` ("View Full Graph"), `查看执行记录` ("View Execution Log"), `保存节点草稿` ("Save Node Draft"), `恢复节点草稿` ("Restore Node Draft"), `旧关卡兼容设置` ("Legacy Level Compatibility").
   - **List & Variable Editor**: `列表初值` ("Initial List Values"), `元素类型` ("Element Type"), `添加一项` ("Add Item"), `应用` ("Apply"), `清除` ("Clear"), and all data type identifiers (`整数`, `小数`, `布尔`, `字符串`, `列表`, `对象`, `植物类型`, `僵尸类型`).
   - **Undo/Redo State Banners**: `没有可重做的记录` ("No redo history available"), `已经是最早记录` ("Already at earliest record").

---

## 5. Regex & Translation Conventions

1. **1-Based Indexing**:
   - Regex replacement templates in `translation-data/Strings/translation_regexs.json` must use 1-based indexing (`{1}`, `{2}`) to map capture groups consistently.
2. **Almanac Typography & Size Tags**:
   - **Almanac Description Font Size**: TextMeshPro Almanac description components (`Description` under `AlmanacPlantWindow/InroduceScroll/Viewport/Content`, path ID 201854) have a native base font size of **18pt** (`m_fontSize = 18.0`).
   - **The `<size=36>` Bug**: Legacy PC translations previously embedded `<size=36>` in text assets. On Android and PC, this forced TextMeshPro to double the font size from 18pt to 36pt, resulting in massive text where only 2–3 words fit per line.
   - **Unified Typography Rule**: The build pipeline (`clean_size_tags` in `scripts/build_405_bundle.py`) strips all `<size>` tags across all platforms. Without `<size>` tag overrides, TextMeshPro renders cleanly at its native 18pt font, fitting 6–8 words per line with normal proportions matching the official game layout.
3. **Platform MonoScript Path IDs**:
   - PC and Android bundles have different `path_id` assignments for UI scripts:
     - **PC**: `TextMeshPro` = 2359, `TextMeshProUGUI` = 3797, `UnityEngine.UI.Text` = 1568.
     - **Android**: `TextMeshPro` = 2372, `TextMeshProUGUI` = 3818, `UnityEngine.UI.Text` = 1574.
   - The build tool dynamically discovers script IDs via `discover_ui_script_ids(env)` from `MonoScript` objects rather than hardcoding them, ensuring 100% of serialized UI elements (settings screen, checkboxes, buttons, modal dialogs) are matched on every platform.
4. **Double Spacing Delimiters**:
   - Chinese UI text in 4.0.5 often uses double spaces around bullet delimiters (e.g., `滚轮或拖动右侧滚动条阅读  ·  Esc关闭`). Always verify literal whitespace when adding exact entries.
5. **C# Enums in Dropdowns (`EventListValueType`)**:
   - Unity dropdowns populated via `Enum.GetNames(typeof(EventListValueType))` pull their option strings directly from the IL2CPP metadata identifier string table (`stringOffset`), completely bypassing the String Literal table.
   - The 7 member names for `EventListValueType` (`整数`, `小数`, `布尔`, `字符串`, `植物类型`, `僵尸类型`, `对象`) occupy 64 contiguous bytes in the identifier table.
   - `scripts/build_metadata_translation.py` patches these 64 bytes in-place to `Integer\0Float\0Boolean\0String\0Plant Type\0Zombie Type\0Object\0` and updates the 7 corresponding `FieldDefinition.nameIndex` records (PC field offset `9355392`, Android field offset `9308396`), translating the dropdown on both platforms without altering any subsequent metadata table offsets.

---

## 6. Build & Automation Commands

- **PC Translation Only**:
  ```powershell
  python scripts/build_pc.py
  ```
- **Full Dual-Platform (PC + Android Signed APK)**:
  ```powershell
  python scripts/build_all.py
  ```
