# PvZ Fusion Translation Toolkit (v4.0.5 — PC & Android)

A unified, repeatable English translation toolkit for both the **PC (Windows)** and **Android (IL2CPP)** releases of *Plants vs. Zombies: Fusion* (植物大战僵尸：融合版) **v4.0.5**.

This project provides automated tools to build, test, and package complete English translations without decompiling game code or distributing proprietary game binaries.

---

## 1. Quick Start / Build Commands

Prerequisites: Python 3.10+ with `UnityPy` and `Pillow` (see `requirements.txt`), plus Java (JDK 17+) for APK signing.

```powershell
# Install requirements
pip install -r requirements.txt

# 1. Build PC Version (Immediate Windows Testing)
python scripts/build_pc.py

# 2. Build Both Versions (PC Game + Signed Android APK)
python scripts/build_all.py
```

### Outputs
- **PC Executable**: `build/PC_PVZ-Fusion-4.0.5/PlantsVsZombiesRH.exe` (runnable immediately on Windows).
- **PC Release Artifacts**: `build/pc-405/` (`data.unity3d`, `global-metadata.dat`, build reports).
- **Android Signed APK**: `build/android-405/PvZ-Fusion-4.0.5-English-Android.apk` (aligned and signed with v1, v2, and v3 schemes).

---

## 2. What's Included in 4.0.5

The 4.0.5 release brings unified parity between PC and Android:

- **Almanac Databases**:
  - **720 Plants** (`LawnStrings`): Fully translated names, descriptions, costs, and cooldowns.
  - **235 Zombies** (`ZombieStrings`): Complete enemy stats, abilities, and lore.
  - **47 Mechanics** (`DetailStrings`): Plant systems, zombie shields, environmental rules, and game modes.
  - **27 Evolution Routes** (`PlantEvolutionData`): Translated Pantheon evolution trees.
  - **74 Tactical Index Entries** (`ShootingAlmanacIndex`): Modifiers, conditions, and buff overrides.
- **Custom Level Creator & Event Rule Tools (New in 4.0.5)**:
  - **11 Tutorial Chapters** (`LevelCreatorHelp`): Comprehensive English beginner and advanced guide.
  - **Dynamic Editor UI**: Graph Check dialogs, List Initial Value modals, Node Description panels, element type selectors (`Integer`, `Float`, `Boolean`, `String`, `List`, `Object`, etc.), and undo/redo state banners.
- **Serialized UI & MonoBehaviours**:
  - Over **1,900 UI elements** translated in-place (TextMesh Pro at byte offset 88, `UnityEngine.UI.Text` at byte offset 144).
  - Runtime navigation backing fields (`Back to Menu`, `Previous Page`, `Next Page`, `Back to Index`).
- **Typography & Layout Optimization**:
  - **PC**: All `<size>` tags stripped to eliminate oversized/clipped text on desktop resolutions.
  - **Android**: Retains calibrated mobile sizing for optimal readability on handheld displays.
  - **Regex Rules**: Strict 1-based index templating (`{1}`, `{2}`) ensuring stable variable interpolation.
- **Localized Textures**:
  - Wave start banners (`StartPlant`, `StartReady`, `StartSet`, `HugeWave`, `FinalWave`).
  - Comic action particles (`Doom`, `Pow`, `Dong`, `guang`, `Sproing`, `SunExplosionPowie`, etc.).

---

## 3. Repository Structure

All translation data is strictly separated from build scripts:

```text
├── translation-data/
│   ├── Strings/
│   │   ├── translation_strings.json   # Exact UI strings & C# literals
│   │   ├── translation_regexs.json    # 1-based regex substitution rules
│   │   ├── customlevel_strings.json   # Custom level strings
│   │   └── abyss_buffs.json           # Realm / Abyss modifier strings
│   ├── Almanac/
│   │   ├── LawnStringsTranslate.json       # 720 Plants database
│   │   ├── ZombieStringsTranslate.json     # 235 Zombies database
│   │   ├── DetailStringsTranslate.json     # 47 Mechanics database
│   │   └── LevelCreatorHelpTranslate.json  # 11 Level Editor tutorial topics
│   └── Dumps/
│       ├── LawnStrings.json           # Raw official plant dump
│       ├── ZombieStrings.json         # Raw official zombie dump
│       ├── DetailStrings.json         # Raw official mechanics dump
│       └── LevelCreatorHelp.json      # Raw official help guide dump
├── scripts/
│   ├── build_pc.py                    # Dedicated PC build script
│   ├── build_all.py                   # Dual PC + Android build script
│   ├── build_metadata_translation.py  # Deterministic IL2CPP metadata builder
│   ├── build_405_bundle.py            # Unified Unity data.unity3d patcher
│   └── package_apk_payload.py         # Surgical APK payload replacer
├── docs/
│   ├── RESEARCH-4.0.5.md              # In-depth 4.0.5 engine & binary research
│   ├── CLAUDE.md                      # AI agent maintainer handoff guide
│   ├── WORKFLOW.md                    # Step-by-step translation maintenance
│   ├── RELEASE-SAFETY.md              # APK safety & hash verification
│   └── TRANSLATION-MAINTENANCE.md     # Upstream synchronization rules
├── build/                             # Generated releases and game folders (git-ignored)
└── README.md
```

---

## 4. Architecture & Translation Policy

### Two-Payload Strategy
The release modifies exactly two files:
1. `data.unity3d` (Unity asset bundle)
2. `global-metadata.dat` (IL2CPP compiled string literals)

On Android, the APK manifest, DEX bytecode, native ARM64/ARMv7 binaries, audio banks, and application permissions remain **100% official and untouched**.

### Upstream Authority
- Gameplay terminology (plants, zombies, buffs, recipes, and items) strictly follows authoritative community translations from [Teyliu/PVZF-Translation](https://github.com/Teyliu/PVZF-Translation).
- Generic UI and editor utility prompts use context-aware English allowlists stored in `translation-data/Strings/`.
- Developer console logs, internal unit tests, and solver harnesses are excluded from player-facing translation to preserve engine stability.

---

## 5. Moving Save Files Safely

Do **not** copy an old game installation's entire directory over a new installation. Restoring the entire directory can overwrite clean metadata or inject incompatible caches.

### Android Save Path:
```text
/storage/emulated/0/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/
```

### Migration Steps:
1. Back up your existing `files/` folder before uninstalling.
2. Install the new English APK.
3. Launch the game once to the main menu, then exit completely.
4. Restore only your progress files:
   - `playerData.json` (main profile, progression, unlocks, and coins)
   - Optional: `Player/Saves/`, `GardenUnifiedData.json`, `CustomIZ.json`, `AutoChessSaves/`
5. Do **not** copy `il2cpp/`, `global-metadata.dat`, `data.unity3d`, or unknown cache files.

---

## 6. Credits & Attribution

- **LanPiaoPiaoFly and the PvZ Fusion team:** The original game and official Chinese builds (**LanPiaoPiaoFly**, **机鱼**, **梦珞**, **蓝蝶**, and contributors).
- **Teyliu and the PC Translation Community:** English translation strings, regex rules, Almanac databases, and community terminology ([Teyliu/PVZF-Translation](https://github.com/Teyliu/PVZF-Translation)).
- **Joseph Franci & aha & silvershadow:** Pioneering early Android translation research and font injection techniques.
- **Toolkit Contributors:** Research, deterministic builders, layout harmonization, and documentation maintenance.

---

## 7. Documentation & Reference Links

- [4.0.5 Technical Research & Binary Layout](docs/RESEARCH-4.0.5.md)
- [Maintainer & AI Agent Guide](docs/CLAUDE.md)
- [Translation Maintenance Workflow](docs/WORKFLOW.md)
- [Release Safety & Verification](docs/RELEASE-SAFETY.md)
- [Third Party Licenses](THIRD_PARTY.md)

*This is an independent fan-made localization project and is not affiliated with or endorsed by PopCap Games, Electronic Arts, or LanPiaoPiaoFly.*
