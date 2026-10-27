# PvZ Fusion Translation Project Rules

## Build & Release Protocol

### 1. Local Testing & Iterative Development
* **Default Target**: Build **only the PC version** to `build/PC_PVZ-Fusion-4.0.5/` using `scripts/build_pc.py`.
* **Constraint**: Do not build the Android APK during iterative testing or debugging unless explicitly asked by the user.

### 2. Releasing to GitHub & Google Drive
* **Default Target**: Always build and package **both platforms**:
  * **PC Build**: Run `scripts/build_pc.py`, then package via `scripts/package_pc_zip.py` (`build/PvZ-Fusion-4.0.5-English-PC.zip`).
  * **Android Build**: Run `scripts/build_android.py` to compile mobile metadata/bundles, assemble the APK, and sign with `uber-apk-signer.jar` (`build/android-405/PvZ-Fusion-4.0.5-English-Android.apk`).
  * **Harmony Fix**: Package via `scripts/package_harmony_fix.py` (`build/BepInEx-Harmony-Fix-v4.0.5.zip`) if applicable.
* **Documentation & Verification**: Compute SHA256 checksums and file sizes, update `docs/release-notes/RELEASE-4.0.5-EN.md`, commit, and push to `origin/main`.
* **Distribution Mirrors**:
  * **Google Drive**: Update existing file IDs in-place using `gdrive mutate update`.
  * **GitHub Release**: Update release metadata and assets for `v4.0.5` using `scripts/publish_github_release.py`.
