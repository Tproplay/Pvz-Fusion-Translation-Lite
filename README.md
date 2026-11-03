# Plants vs. Zombies: Fusion — English Translation Toolkit (PC & Android)

A unified, repeatable English translation toolkit for both the **PC (Windows)** and **Android (IL2CPP)** releases of *Plants vs. Zombies: Fusion* (植物大战僵尸：融合版).

[![Discord](https://img.shields.io/badge/Discord-Join%20Community-5865F2?logo=discord&logoColor=white)](https://discord.gg/mDeAWbfnKP)
[![GitHub Release](https://img.shields.io/github/v/release/Tproplay/Pvz-Fusion-Translation-Lite?logo=github)](https://github.com/Tproplay/Pvz-Fusion-Translation-Lite/releases)

Join our community on **[Discord (https://discord.gg/mDeAWbfnKP)](https://discord.gg/mDeAWbfnKP)** for updates, support, modding discussion, and reporting untranslated strings or bugs!

This project provides automated tools to build, test, and package complete English translations without decompiling game code or distributing proprietary game binaries.

---

## 📥 Downloads (v4.1)

| Platform | Primary Download (GitHub) | Alternative Mirror (Google Drive) |
| :--- | :--- | :--- |
| **PC (Windows)** | [GitHub Release (v4.1)](https://github.com/Tproplay/Pvz-Fusion-Translation-Lite/releases/tag/v4.1) | [Google Drive Mirror](https://drive.google.com/file/d/1icQjixqbtUE6k0XM9ehCD_hJL30vs-3R/view?usp=sharing) |
| **Android (APK)** | [GitHub Release (v4.1)](https://github.com/Tproplay/Pvz-Fusion-Translation-Lite/releases/tag/v4.1) | [Google Drive Mirror](https://drive.google.com/file/d/1iu52ubJdl3rYl-Umgw2sevTtHhAIdemU/view?usp=sharing) |

> 📁 **Google Drive Folder**: Access all v4.1 downloads in the [Version 4.1 Folder](https://drive.google.com/drive/folders/1vFkBmV5aZXHBiYlVDd9H6xjclvs_G8fk?usp=sharing).
>
> 📜 **Release Notes & Checksums**: View complete release notes, changelog, and SHA-256 verification hashes in [docs/release-notes/RELEASE-4.1-EN.md](docs/release-notes/RELEASE-4.1-EN.md).

---

## Architecture & Translation Policy

### Two-Payload Strategy
The release modifies exactly two files:
1. `data.unity3d` (Unity asset bundle containing serialized UI strings, textures, and TextAssets)
2. `global-metadata.dat` (IL2CPP compiled string literals)

On Android, the APK manifest, DEX bytecode, native ARM64/ARMv7 binaries, audio banks, and application permissions remain **100% official and untouched**.

### Upstream Authority
- **Gameplay Terminology**: Plants, zombies, buffs, recipes, and items strictly follow authoritative community translations from [Teyliu/PVZF-Translation](https://github.com/Teyliu/PVZF-Translation).
- **UI & System Text**: Generic UI, editor utilities, and system prompts use context-aware English allowlists stored in `translation-data/Strings/`.
- **Engine Stability**: Developer console logs, internal unit tests, and solver harnesses are preserved or safely handled to ensure zero crash risk.

---

## Moving Save Files Safely

Do **not** copy an old game installation's entire directory over a new installation. Restoring the entire directory can overwrite clean metadata or inject incompatible caches.

### Android Save Path:
```text
/storage/emulated/0/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/
```

### Migration Steps:
> [!TIP]
> **No Uninstall Required**: If you were previously using an English translation from this repository, you **do not need to uninstall the previous version**! All builds from this repository use our consistent release signing key, allowing you to install the updated APK directly over your existing installation without losing your save data or progression.
> *(An uninstall is only required if you are migrating from the official Chinese APK or another translator's build with a different signature).*

1. Back up your existing `files/` folder before uninstalling or updating.
2. Install the new English APK.
3. Launch the game once to the main menu, then exit completely.
4. Restore only your progress files:
   - `playerData.json` (main profile, progression, unlocks, and coins)
   - `Player/Saves/`, `GardenUnifiedData.json`, `CustomIZ.json`, `AutoChessSaves/`
5. Do **not** copy `il2cpp/`, `global-metadata.dat`, `data.unity3d`, or unknown cache files.

---

## Credits & Attribution

- **LanPiaoPiaoFly and the PvZ Fusion team:** The original game and official Chinese builds (**LanPiaoPiaoFly**, **机鱼**, **梦珞**, **蓝蝶**, and contributors).
- **Teyliu and the PC Translation Community:** English translation strings, regex rules, Almanac databases, and community terminology ([Teyliu/PVZF-Translation](https://github.com/Teyliu/PVZF-Translation)).
- **silvershadow:** Original Android translation project and font injection research ([silvershadowkat/pvzf-android-translation](https://github.com/silvershadowkat/pvzf-android-translation/releases)).
- **Joseph Franci & aha:** Pioneering early Android translation research and foundation.
- **Toolkit Contributors:** Research, deterministic builders, layout harmonization, and documentation maintenance.

---

## Documentation & Reference Links

- [Architecture & Developer Guide (Build Commands & Repo Structure)](docs/ARCHITECTURE.md)
- [Android Release Signing Key & Verification](docs/signing/SIGNING-KEY.md)
- [Release Notes Archive](docs/release-notes/)
- [Release Template](docs/RELEASE_TEMPLATE.md)
- [4.0.5 Technical Research & Binary Layout](docs/RESEARCH-4.0.5.md)
- [Maintainer & AI Agent Guide](docs/CLAUDE.md)
- [Translation Maintenance Workflow](docs/WORKFLOW.md)
- [Release Safety & Verification](docs/RELEASE-SAFETY.md)
- [Third Party Licenses](THIRD_PARTY.md)

---

*This is an independent fan-made localization project and is not affiliated with or endorsed by PopCap Games, Electronic Arts, or LanPiaoPiaoFly.*
