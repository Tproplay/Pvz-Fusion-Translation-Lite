# Plants vs. Zombies: Fusion v4.0.5 — English Release (PC & Android)

A complete, unified English translation release of **Plants vs. Zombies: Fusion (植物大战僵尸: 融合版) v4.0.5** for both Windows PC and Android.

---

## Downloads

| Platform | File | Size | SHA-256 Checksum |
| :--- | :--- | :--- | :--- |
| **PC (Windows)** | `PvZ-Fusion-4.0.5-English-PC.zip` | 441.73 MB | `5d23dd55ad71b090be0ad4907c14954b2af786ff41950322b0778ccf918238dc` |
| **Android** | `PvZ-Fusion-4.0.5-English-Android.apk` | 571.08 MB | `e1e3d8a0d7ac99106bd9e3341bfeb543d985860b1b7368446c49a0ca1cba5e27` |

---

## Installation & Setup

### Windows (PC)
1. Download `PvZ-Fusion-4.0.5-English-PC.zip`.
2. Extract the archive into a folder of your choice.
3. Run `PlantsVsZombiesRH.exe` to play.
   *(No extra patching or installation required; all translation assets are already compiled and integrated).*

### Android
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
