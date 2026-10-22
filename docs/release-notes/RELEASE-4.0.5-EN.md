# Plants vs. Zombies: Fusion v4.0.5 — English Release (PC & Android)

A complete, unified English translation release of **Plants vs. Zombies: Fusion (植物大战僵尸: 融合版) v4.0.5** for both Windows PC and Android.

---

## 🚨 Hotfix 2 (Oct 22, 2026)
- **Rogue Shooting Crash Fix**: Resolved `ShootingGroupBuff` initialization crash caused by missing enum parsing for `Shooting_Wooden Post1` when opening buff selection menus.
- **The Gods: Evolved Localization & Polish**:
  - Fully translated reroll modifiers, difficulty multiplier descriptions, defeat reward calculation formulas, and classic clear reward text.
  - Translated new plant banners ("New Plant Obtained").
  - Fixed empty first line on modifier parchment cards by preserving newline layout.
  - Refined level title layout: cleanly wraps on stage selection cards while displaying on a single line in gameplay level headers.
- **Custom Level Editor**: Translated `TMP_InputField` placeholders in custom level settings ("Set Sun Amount" and "Plant Sun Drops").

## 🚨 Hotfix 1 (Oct 22, 2026)
- **Suburban Almanac Headers**: Fixed title text wrapping onto two lines in Plant, Zombie, and Index Almanac views by enforcing single-line formatting (`<nobr><size=70%>...</size></nobr>`).
- **Difficulty Text Sizing**: Scaled "Purgatory Difficulty" to 85% and "Evolved Difficulty" to 90% for clean button fit.
- **HP Display Buttons**: Scaled "Toggle Plant HP (Q)" to 80% and "Toggle Zombie HP (W/R)" to 70% to fit within stone tablet frames on PC.
- **Odyssey One Sign**: Fixed "Odyssey" wrapping the letter "y" onto a separate line in the Grand Garden minecart station.
- **Profile Creation**: Fully translated save creation ("Save [name] created successfully") and save management notifications.
- **Android Compatibility**: Fixed startup crash and removed trailing blank lines from Starbound challenge strings.

---

## Downloads

| Platform | File | Size | SHA-256 Checksum | Mirror (Google Drive) |
| :--- | :--- | :--- | :--- | :--- |
| **PC (Windows)** | [`PvZ-Fusion-4.0.5-English-PC.zip`](https://github.com/Tproplay/Pvz-Fusion-Translation-Lite/releases/tag/v4.0.5) | 442.64 MB | `d6d90a52f5a366bd14b3f03167df414870ba14c070ac86a05ff0e89018074c82` | [PC Drive Mirror](https://drive.google.com/file/d/1tthm97SKriP5Ix8KRSakh1mOA5TWT2jd/view?usp=sharing) |
| **Android** | [`PvZ-Fusion-4.0.5-English-Android.apk`](https://github.com/Tproplay/Pvz-Fusion-Translation-Lite/releases/tag/v4.0.5) | 571.11 MB | `07bf0e7c2dd4283b0338de650340804dafbcf57c20af8b3ba013d10710137605` | [Android Drive Mirror](https://drive.google.com/file/d/1AFrHBVx1wnsnwjDy74zSeFT2I5Ri0rMe/view?usp=drive_link) |

### 🌐 Alternative Download Mirror (Google Drive)
If you experience slow download speeds or issues downloading from GitHub Releases, download directly from Google Drive:
- 🖥️ **PC Version (Windows ZIP)**: [Google Drive Download](https://drive.google.com/file/d/1tthm97SKriP5Ix8KRSakh1mOA5TWT2jd/view?usp=sharing)
- 📱 **Android Version (Signed APK)**: [Google Drive Download](https://drive.google.com/file/d/1AFrHBVx1wnsnwjDy74zSeFT2I5Ri0rMe/view?usp=drive_link)

---

## Installation & Setup

### Windows (PC)
1. Download `PvZ-Fusion-4.0.5-English-PC.zip`.
2. Extract the archive into a folder of your choice.
3. Run `PlantsVsZombiesRH.exe` to play.
   *(No extra patching or installation required; all translation assets are already compiled and integrated).*

### Android
> [!TIP]
> **No Uninstall Required**: If you were previously using an English translation from this repository, you **do not need to uninstall the previous version**! Because all builds from this repository use our consistent release signing key, you can install the updated APK directly over your existing installation and your saves and progress will be preserved automatically.
> *(An uninstall is only needed if you are migrating from the official Chinese version or another build with a different signature).*

1. **Back up your save data** before installing.
2. If you previously placed a manual `il2cpp` or `global-metadata.dat` override inside `Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/il2cpp`, remove that folder so Android does not override the APK's new 4.0.5 translation data.
3. Install `PvZ-Fusion-4.0.5-English-Android.apk` and launch the game.

---

## What's New & Highlighted Features in v4.0.5

### 1. Complete Almanac & Tactical Databases
- **720 Plants (`LawnStrings`)**: Fully translated plant names, lore, descriptions, fusion recipes, Sun costs, cooldowns, and synergy types.
- **235 Zombies (`ZombieStrings`)**: Comprehensive enemy statistics, armor mechanics, and special abilities.
- **47 Mechanics & Game Rules (`DetailStrings`)**: Thorough explanations of game systems, projectile interactions, environmental effects, and special modes.
- **27 Evolution Routes (`PlantEvolutionData`)**: Full Pantheon evolution trees with role descriptions, stat bonuses, and unlock conditions.
- **74 Tactical Index Entries (`ShootingAlmanacIndex`)**: Modifiers, weapon types, and buff interactions.
- **Mobile Almanac Typography**: Normalized TextMeshPro font sizing across mobile and desktop so card text fits cleanly without truncation or oversized fonts.

### 2. Super Level Editor & Custom Content Support
- **100% Save-File Compatibility**: Internal IL2CPP enum bindings have been preserved in their original engine definitions. Custom levels and existing save files load seamlessly with zero risk of corruption.
- **Editor Localization**: Fully translated node description headers, subtitles, error dialogs, and input/output data port types (*Plant Entity*, *Item Object*, *3D Coordinates*, *Execution Signal*).
- **Canvas Tools**: Magic brush tools (*Pencil*, *Eraser*, *Brush Width*), and grid toggles (*Grid: On* / *Grid: Off*) fully translated.

### 3. Odyssey, Mini-Games & UI
- **Odyssey Gacha & Evolution**: Complete translation of luck stats, upgrade mechanics, reincarnation levels, and round progression.
- **Vasebreaker PVP**: Real-time notifications, turn counters, and RMB trigger toggles localized.
- **Zen Garden Tool Shop**: Dynamic price and quantity formatting with ultrawide display compatibility.
- **Difficulty Selector**: Full numbered six-tier difficulty scale (*0: Easy Mode* through *5: Are You Sure?*).
- **High-Resolution UI & Textures**: "Let's Rock!" start button, main menu buttons, and gameplay HUD elements cleanly rendered.

---

## Building from Source

This repository contains the complete automated toolchain to rebuild both PC and Android versions:

```powershell
# Build Windows PC version only
python scripts/build_pc.py

# Build dual-platform release (PC game + signed Android APK)
python scripts/build_all.py
```
