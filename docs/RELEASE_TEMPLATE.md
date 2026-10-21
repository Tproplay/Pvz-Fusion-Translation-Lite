# Plants vs. Zombies: Fusion v[VERSION] — English Release (PC & Android)

A complete, unified English translation release of **Plants vs. Zombies: Fusion  v[VERSION]** for both Windows PC and Android.

---

## 📥 Downloads

| Platform | File | Size | SHA-256 Checksum |
| :--- | :--- | :--- | :--- |
| **PC (Windows)** | `PvZ-Fusion-[VERSION]-English-PC.zip` | [SIZE_PC] | `[SHA256_PC]` |
| **Android** | `PvZ-Fusion-[VERSION]-English-Android.apk` | [SIZE_APK] | `[SHA256_APK]` |

### 🌐 Alternative Download Mirror (Google Drive)
If you experience slow download speeds or issues downloading from GitHub Releases, you can use the Google Drive mirror:
- **Google Drive Mirror Folder**: [Download from Google Drive](INSERT_GOOGLE_DRIVE_FOLDER_LINK_HERE)
  - 🖥️ `PvZ-Fusion-[VERSION]-English-PC.zip`
  - 📱 `PvZ-Fusion-[VERSION]-English-Android.apk`

---

## 🛠️ Installation & Setup

### Windows (PC)
1. Download `PvZ-Fusion-[VERSION]-English-PC.zip`.
2. Extract the ZIP archive into a folder of your choice.
3. Run `PlantsVsZombiesRH.exe` to play.
   *(No extra patching or mod managers required; all translation assets are already compiled and integrated).*

### Android
1. **Back up your save data** before installing (see [Safe Save Migration](#-moving-save-files-safely) below).
2. If you previously installed a manual translation or left an `il2cpp` / `global-metadata.dat` override inside:
   ```text
   /storage/emulated/0/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/il2cpp/
   ```
   **Delete the `il2cpp/` folder** so Android does not override the APK's built-in translation data with obsolete files.
3. Install `PvZ-Fusion-[VERSION]-English-Android.apk` and launch the game.

---

## 💾 Moving Save Files Safely

Do **not** overwrite an existing installation with an entire game directory or old asset caches.

### Android Save Path:
```text
/storage/emulated/0/Android/data/com.LanPiaoPiao.PlantsVsZombiesRH/files/
```

### Migration Steps:
1. Copy and backup your `files/` folder to a safe location before uninstalling or updating.
2. Install the new English APK.
3. Launch the game once to reach the main menu, then exit completely.
4. Restore **only your progress files**:
   - `playerData.json` (Main profile, level progression, unlocks, and coins)
   - *(Optional)* `Player/Saves/`, `GardenUnifiedData.json`, `CustomIZ.json`, `AutoChessSaves/`
5. **Do NOT restore**: `il2cpp/`, `global-metadata.dat`, `data.unity3d`, or shader/render caches.

---

## ✨ What's New in v[VERSION]

### 📖 Almanac & Lore
- Fully translated plant entries, descriptions, fusion recipes, and Sun costs.
- Comprehensive zombie stats, armor types, and special abilities.
- Game mechanics, environment rules, and Pantheon evolution trees.

### 🎮 UI & Game Modes
- Main menu, level select, and mode selectors.
- Mini-games, Odyssey, Vasebreaker PVP, and Zen Garden shop.
- Standardized typography and mobile layout formatting.

### 🛠️ Custom Level Editor & Tools
- Translated node descriptions, port types, canvas tools, and graph check dialogs.
- 100% save-file and level-file compatibility with official Chinese releases.

---

## ⚠️ Notes & Security Verification

- **Pure Payload Replacement**: The APK uses original official game binaries, DEX code, and permissions. Only `data.unity3d` and `global-metadata.dat` are patched.
- **Signed Release**: The Android APK is aligned and signed with standard release keys (v1, v2, and v3 signatures).
- Verify the SHA-256 checksums provided above before running the executable or installing the APK.
