# Maintainer Handoff for AI Agents & Translators

**Target Version:** Plants vs. Zombies: Fusion **v4.1** (PC & Android)  
**Architecture Documentation:** [ARCHITECTURE.md](ARCHITECTURE.md)  
**Workflow Guide:** [WORKFLOW.md](WORKFLOW.md)  
**Release Safety & Auditing:** [RELEASE-SAFETY.md](RELEASE-SAFETY.md)

---

> [!IMPORTANT]
> **No hardcoded translations in scripts.** All Chinese→English mappings MUST be stored in JSON files under `translation-data/Strings/`. Scripts must read those files; they must never contain inline translation dictionaries. This applies to all build scripts, audit scripts, and tools.

---

## 1. Quick Start / How to Build

The repository provides single-command builders for both platforms:

### A. Build PC Version Only (local iterative testing)
Rebuilds `global-metadata.dat` and `data.unity3d` directly into the playable PC folder:
```powershell
.\.venv\Scripts\python.exe scripts\build_pc.py
```
- PC game can be launched immediately at `build/PC_PVZ-Fusion-4.1/PlantsVsZombiesRH.exe`.
- Release artifacts (`data.unity3d`, `global-metadata.dat`, reports) are saved to `build/pc-41/`.
- **Do NOT build Android APK or package ZIP during local testing.**

### B. Build Android APK (when explicitly requested)
```powershell
.\.venv\Scripts\python.exe scripts\build_android.py
```
- Output signed APK: `build/android-41/PvZ-Fusion-4.1-English-Android.apk`.

### C. Package PC ZIP for release (release only)
```powershell
.\.venv\Scripts\python.exe scripts\package_pc_zip.py
```
- Output: `build/PvZ-Fusion-4.1-English-PC.zip`

---

## 2. Repository Layout & Translation Data

All translation text is strictly organized under `translation-data/`. **Do not hardcode translation maps into Python scripts — ever.**

```text
translation-data/
  Strings/                              ← All runtime translation JSON files
    translation_strings.json            ← Exact UI strings, button labels, C# literals
    translation_regexs.json             ← Regex substitution rules (1-based group refs: {1}, $1)
    odyssey_evolution.json              ← Odyssey Evolved / Super Stack Up mode strings
    abyss_buffs.json                    ← Abyss / Realm buffs
    travel_buffs.json                   ← Investment Odyssey buff descriptions (structured)
    tips_fs.json                        ← Final Stage tips (structured)
    tips_iz.json                        ← Invasion Zone tips (structured)
    customlevel_strings.json            ← Custom level editor exact strings
    customlevel_regexs.json             ← Custom level editor regex rules
    android_metadata_strings.json       ← Android-only fallback mappings (PC translations win)
    android_required_overrides.json     ← Strings Android MUST render differently from PC
    android_modifier_titles.json        ← Android modifier card display titles
    runtime_backing_strings.json        ← Runtime nav backing fields (Back to Menu, etc.)
    in_level_overrides.json             ← In-level single-line title overrides
    shooting_group_names.json           ← Enum names NOT to translate (breaks Enum.Parse)
  Almanac/
    LawnStringsTranslate.json           ← Plant database (translated)
    ZombieStringsTranslate.json         ← Zombie database (translated)
    DetailStringsTranslate.json         ← Game mechanics entries (translated)
    LevelCreatorHelpTranslate.json      ← Level Editor tutorial chapters (translated)
    PlantType.json / ZombieType.json    ← Type→name mappings
  Enums/
    SynergyType.json                    ← Plant affinity enum (18 fields, Android only)
    InvestBuff.json                     ← Investment buff enum (42 fields, Android only)
    Event*.json                         ← Custom level editor event enums
  Dumps/                                ← Raw official game data (READ ONLY — never edit)
    LawnStrings.json, ZombieStrings.json, DetailStrings.json
    LevelCreatorHelp.json, ShootingAlmanacIndex.json
    PlantEvolutionData.json, TalentData.json
    travel_buffs.json, tips_fs.json, tips_iz.json
    AbyssBuffData.json, AchievementsText.json
    untranslated_dump_41.json           ← v4.1 untranslated string audit list
  untranslated_screenshot/              ← Drop PNGs of untranslated UI here (deleted after work)
```

---

## 3. Adding or Updating Translations

### New exact UI string or C# literal
```python
# translation-data/Strings/translation_strings.json
"中文原文": "English Translation"

# For Odyssey Evolved strings specifically:
# translation-data/Strings/odyssey_evolution.json
"轮间商店": "Round Shop"
```

### New dynamic/parametric string
```json
// translation-data/Strings/translation_regexs.json
// Use 1-based group references. $1/$2 or {1}/{2} (NOT {0})
"^攻击力加成\\s*(\\d+(?:\\.\\d+)?%)$": "Attack Bonus $1",
"^旅行进化\\s*(\\d+-\\d+),\\s*生命\\s*(\\d+)/(\\d+),\\s*难度\\s*(.+)$": "Odyssey Evolved $1, HP $2/$3, Difficulty $4"
```

### Rebuild and verify
```powershell
.\.venv\Scripts\python.exe scripts\tools\lookup_string.py "中文字符串"
.\.venv\Scripts\python.exe scripts\tools\quick_audit.py
.\.venv\Scripts\python.exe scripts\build_pc.py
```

---

## 4. Key Technical Rules for v4.1

1. **Unity Engine & Payloads**:
   - Unity 2022.3 on IL2CPP v29.
   - Two binary payloads replaced:
     - `PlantsVsZombiesRH_Data/data.unity3d` (PC) / `assets/bin/Data/data.unity3d` (Android)
     - `PlantsVsZombiesRH_Data/il2cpp_data/Metadata/global-metadata.dat` (PC) / `assets/bin/Data/Managed/Metadata/global-metadata.dat` (Android)
   - Android DEX bytecode, native ARM libraries, and manifest remain 100% official and untouched.

2. **UI Component Offsets in `data.unity3d`**:
   - **TextMesh Pro** (`script_path_id in (3797, 2359)`): Byte offset **88** for `m_text`.
   - **UnityEngine.UI.Text** (`script_path_id == 1568`): Byte offset **144** for `m_Text`.
   - Both use `<i` length-prefixed, 4-byte padded UTF-8 fields.

3. **Typography & `<size>` Tag Policy**:
   - **PC**: All `<size>` tags must be stripped from Almanac descriptions, UI text, and regex replacements.
   - **Android**: Retains calibrated mobile `<size>` tags.

4. **Regex Replacement Numbering**:
   - Always 1-based: `{1}`, `{2}` or `$1`, `$2`. **Never `{0}` as a group reference in `translation_regexs.json`.**

5. **Internal Enum Keys — Do Not Translate**:
   - Names listed in `shooting_group_names.json` are used by `Enum.Parse()` at runtime. Translating them corrupts saves and breaks game logic. They are loaded as a frozen set and explicitly excluded from the translation pass.

6. **`<nobr>` Tags on Odyssey Modifier Names**:
   - Modifier names in the built metadata use `<nobr>Name</nobr>：Description` format. The `<nobr>` wraps only the name, preventing awkward mid-name line breaks.

7. **`$1`/`$2` vs `{1}`/`{2}` in templates**:
   - `$N` style: used in PC regex translations, substituted directly by `csharp_format()`.
   - `{N}` style: used in C# format string templates (also 1-based unless the template contains `{0}`).

8. **Custom Level Creator**:
   - Help Guide is a JSON TextAsset named `LevelCreatorHelp`.
   - Dialog modals, graph check results, list item editors, and tool banners are C# dynamic UI reading string literals from `global-metadata.dat`.

---

## 5. Screenshot Translation Workflow

When untranslated text appears in the game:

1. Take a screenshot and place it in `translation-data/untranslated_screenshot/<mode-subfolder>/`.
2. Transcribe the Chinese text from the screenshot.
3. Look it up: `.\.venv\Scripts\python.exe scripts\tools\lookup_string.py "字符串"`.
4. Add the translation to the correct JSON file (never in a script).
5. Run quick audit: `.\.venv\Scripts\python.exe scripts\tools\quick_audit.py`.
6. Rebuild PC: `.\.venv\Scripts\python.exe scripts\build_pc.py`.
7. Delete the processed screenshot PNGs (keep the folder).
8. Commit with `--author="gemini-code-assist[bot] <gemini-code-assist[bot]@users.noreply.github.com>"`.
