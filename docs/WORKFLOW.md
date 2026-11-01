# Repeatable update workflow

> **Current Version:** v4.1 (PC & Android). This document describes the repeatable translation maintenance workflow for PvZ Fusion 4.1. For architecture details see [ARCHITECTURE.md](ARCHITECTURE.md). For AI agent/maintainer handoff see [CLAUDE.md](CLAUDE.md).

> [!IMPORTANT]
> **No hardcoded translations in scripts.** All translation text MUST live in JSON files under `translation-data/`. Scripts must read from those files at runtime. Never embed Chinese→English mappings, display strings, or UI labels directly in Python source code.


## 1. Preserve clean inputs

Keep the official game files (`global-metadata.dat` and `data.unity3d`) unchanged in their `.orig` backup form. Generated translated files must never become the baseline for a future patch run — always start from the clean originals.

Record the size and SHA-256 of every input. This makes it possible to identify silent upstream replacements and prevents applying a patch to the wrong game version.

## 2. Update translation data

All translation data lives under `translation-data/`. The metadata builder consumes these files at runtime — **never hardcode Chinese→English mappings in Python scripts**:

**Exact string files** (`translation-data/Strings/`):
- `translation_strings.json` — exact UI strings, button labels, C# literals
- `odyssey_evolution.json` — Odyssey Evolved (Super Stack Up) mode strings
- `abyss_buffs.json` — Abyss / Realm modifier strings
- `customlevel_strings.json` — custom level editor strings

**Regex pattern files** (`translation-data/Strings/`):
- `translation_regexs.json` — dynamic regex rules (use `{1}`, `{2}` 1-based indexing or `$1`, `$2`)
- `customlevel_regexs.json` — regex for custom level editor strings

**Structured pair files** (`translation-data/Strings/`):
- `travel_buffs.json` — Travel / Investment Odyssey buff descriptions
- `tips_fs.json` — Final Stage tips
- `tips_iz.json` — Invasion Zone tips

**Android-specific override files** (`translation-data/Strings/`):
- `android_metadata_strings.json` — confirmed Android-only exact mappings (fallback; PC translations win)
- `android_required_overrides.json` — strings where Android semantics require a different rendering than PC
- `android_modifier_titles.json` — Android modifier display titles
- `runtime_backing_strings.json` — runtime navigation backing fields (Back to Menu, etc.)

**Enum translations** (`translation-data/Enums/`):
- `SynergyType.json`, `InvestBuff.json` — Android IL2CPP definition-string heap enum field renames
- Various event enum files for the custom level editor

**Almanac databases** (`translation-data/Almanac/`):
- `LawnStringsTranslate.json` — plant entries
- `ZombieStringsTranslate.json` — zombie entries
- `DetailStringsTranslate.json` — mechanics entries
- `LevelCreatorHelpTranslate.json` — level editor tutorial chapters

**Reference dumps** (`translation-data/Dumps/`) — raw official game files used as source references:
- `LawnStrings.json`, `ZombieStrings.json`, `DetailStrings.json`, `LevelCreatorHelp.json`
- `ShootingAlmanacIndex.json`, `PlantEvolutionData.json`, `TalentData.json`
- `travel_buffs.json`, `tips_fs.json`, `tips_iz.json`, `AbyssBuffData.json`
- `untranslated_dump_41.json` — v4.1 untranslated string audit list

## 3. Adding new translations

When a new untranslated string is found (via screenshot or dump):

1. Identify the string in the game using `scripts/tools/lookup_string.py "string text"`.
2. Add the translation to the appropriate JSON file in `translation-data/Strings/` — **never in a script**.
3. For dynamic/parametric strings, add a regex rule to `translation_regexs.json` with 1-based group references (`{1}`, `{2}` or `$1`, `$2`).
4. Verify with `scripts/tools/quick_audit.py`.
5. Rebuild PC with `scripts/build_pc.py`.

> [!CAUTION]
> Do not blindly translate every CJK-bearing string. Debug/test messages, internal enum keys, and configuration identifiers whose mutation can break game behavior or save files must be left untouched. Only promote strings that are confirmed player-facing.

## 4. Generate metadata deterministically

Run `scripts/build_pc.py` which invokes `scripts/build_metadata_translation.py` against the clean `.orig` metadata. Inspect the generated JSON report at `build/pc-41/metadata-report.json` for:

- input and output hashes
- unchanged vs. translated literal count
- translations grouped by source method (`pc_exact`, `pc_regex`, `pc_regex_csharp_template`, `android_confirmed_exact`)
- remaining CJK-bearing literals

Run `scripts/audit_remaining_cjk.py` after every build.

## 5. Patch `data.unity3d`

Run `scripts/build_405_bundle.py` (invoked automatically by `build_pc.py`) to patch:

1. Almanac text databases (`LawnStrings`, `ZombieStrings`, `DetailStrings`, `LevelCreatorHelp`) replaced with translated versions.
2. Dynamic UI `TextAsset` objects translated in-place.
3. Serialized `MonoBehaviour` UI components (TMP and legacy `UI.Text`) translated at their byte offsets.
4. Font injected for full Latin coverage.
5. Localized textures replaced by asset name (wave banners, comic particles).

The bundle builder reads all replacement content from JSON files — never from inline Python dicts.

## 6. Test locally (PC only during development)

```powershell
.\.venv\Scripts\python.exe scripts\build_pc.py
```

- Game runs immediately from `build/PC_PVZ-Fusion-4.1/PlantsVsZombiesRH.exe`.
- Do **not** build Android APK or package ZIP during iterative testing.

Test at minimum:
- main menu, adventure and challenge selection
- Odyssey Evolved mode selection and difficulty cards
- Round Shop, augment (hex) system, investment strategies
- Almanac plants, zombies, and mechanics
- Custom level editor and tutorials
- Font rendering, rich-text tags (`<color>`, `<size>`, `<nobr>`), line wrapping
- Save/load and relaunch

## 7. Release build (GitHub + Google Drive)

Only when ready for a public release, build **both platforms**:

```powershell
# PC build + ZIP
.\.venv\Scripts\python.exe scripts\build_pc.py
.\.venv\Scripts\python.exe scripts\package_pc_zip.py

# Android APK (signed)
.\.venv\Scripts\python.exe scripts\build_android.py
```

Then publish:
```powershell
.\.venv\Scripts\python.exe scripts\publish_github_release.py
```

Update Google Drive file IDs in-place with `gdrive mutate update`. Compute and publish SHA-256 checksums for all release artifacts.

## 8. Safety: what maintainers must verify before release

- metadata literal count and round-trip validation (checked automatically by builder)
- Unity TextAsset root/schema validation
- Almanac entry/title coverage
- remaining CJK inventory (`audit_remaining_cjk.py`)
- APK audit confirming only the two payloads changed (`audit_apk_release.py`)
- physical smoke test on device or PC executable
