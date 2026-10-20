# Maintainer Handoff for AI Agents & Translators

**Target Version:** Plants vs. Zombies: Fusion v4.0.5 (PC & Android)  
**Primary Architecture Documentation:** [RESEARCH-4.0.5.md](RESEARCH-4.0.5.md)  
**Workflow Guide:** [WORKFLOW.md](WORKFLOW.md)  
**Release Safety & Auditing:** [RELEASE-SAFETY.md](RELEASE-SAFETY.md)

---

## 1. Quick Start / How to Build

The repository provides automated, single-command builders for both platforms:

### A. Build PC Version Only
Rebuilds `global-metadata.dat` and `data.unity3d` directly into the playable PC folder (`build/PC_PVZ-Fusion-4.0.5/`):
```powershell
python scripts/build_pc.py
```
- PC game can be launched immediately at `build/PC_PVZ-Fusion-4.0.5/PlantsVsZombiesRH.exe`.
- Release artifacts (`data.unity3d`, `global-metadata.dat`, reports) are saved to `build/pc-405/`.

### B. Build Both Versions (PC + Android Signed APK)
Rebuilds the PC release, the Android metadata/bundle, packages the APK payload, and signs with v1/v2/v3 signatures:
```powershell
python scripts/build_all.py
```
- Output signed APK: `build/android-405/PvZ-Fusion-4.0.5-English-Android.apk`.

---

## 2. Repository Layout & Translation Data

All translation text is strictly organized under `translation-data/`. **Do not hardcode translation maps into Python scripts.**

```text
translation-data/
  Strings/
    translation_strings.json   <- Exact UI strings, button labels, C# literals
    translation_regexs.json    <- Regex substitution rules (1-based index)
    customlevel_strings.json   <- Custom level and Odyssey strings
    abyss_buffs.json           <- Abyss / Realm buffs
  Almanac/
    LawnStringsTranslate.json       <- 720 Plants database
    ZombieStringsTranslate.json     <- 235 Zombies database
    DetailStringsTranslate.json     <- 47 Game mechanics entries
    LevelCreatorHelpTranslate.json  <- 11 Level Editor tutorial topics
  Dumps/
    LawnStrings.json           <- Raw official plant dump
    ZombieStrings.json         <- Raw official zombie dump
    DetailStrings.json         <- Raw official mechanics dump
    LevelCreatorHelp.json      <- Raw official help guide dump
    untranslated_dump_405.json <- Raw 4.0.5 dumped strings (diagnostics/tests)
```

---

## 3. Key Findings & Architectural Rules for 4.0.5

1. **Unity Engine & Payloads**:
   - Unity 2022.3.62f1 on IL2CPP v29.
   - Exact binary payloads replaced:
     - `PlantsVsZombiesRH_Data/data.unity3d` (PC) / `assets/bin/Data/data.unity3d` (Android)
     - `PlantsVsZombiesRH_Data/il2cpp_data/Metadata/global-metadata.dat` (PC) / `assets/bin/Data/Managed/Metadata/global-metadata.dat` (Android)
   - Android DEX bytecode, native ARM libraries, and manifest remain 100% official and untouched.

2. **UI Component Offsets in `data.unity3d`**:
   - **TextMesh Pro** (`script_path_id in (3797, 2359)`): Byte offset **88** for `m_text`.
   - **UnityEngine.UI.Text** (`script_path_id == 1568`): Byte offset **144** for `m_Text`.
   - Both use `<i` length-prefixed, 4-byte padded UTF-8 fields.

3. **Typography & `<size>` Tag Policy**:
   - **PC**: All `<size>` tags must be stripped from Almanac descriptions, UI text, and regex replacements. High desktop resolutions with mobile `<size>` tags cause oversized, clipped text.
   - **Android**: Retains calibrated mobile `<size>` tags for readable scaling on phone screens.

4. **Regex Replacement Numbering**:
   - All regex replacement strings in `translation_regexs.json` must use 1-based indexing (`{1}`, `{2}`).

5. **Custom Level Editor (New in 4.0.5)**:
   - Help Guide is a JSON TextAsset named `LevelCreatorHelp` (11 chapters).
   - Dialog modals, graph check results, list item editors, and tool banners are C# dynamic UI elements reading string literals from `global-metadata.dat`.

---

## 4. How to Update or Add Translations

1. **New UI or System String**:
   - Add `"ChineseText": "EnglishText"` to `translation-data/Strings/translation_strings.json`.
2. **New Regex Pattern**:
   - Add `"^Pattern": "Replacement {1}"` to `translation-data/Strings/translation_regexs.json` using 1-based index.
3. **Rebuild**:
   - Run `python scripts/build_pc.py` to test on PC immediately.
   - Run `python scripts/build_all.py` when ready for full dual-platform release.
