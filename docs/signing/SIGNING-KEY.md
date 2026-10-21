# Public Android Release Signing Key & Verification

This document records the official public signing key and certificate used to sign the Android releases of the **PvZ Fusion English Translation Toolkit**.

---

## 1. Why the Signing Key is Public

On Android, updating an existing app without uninstalling requires the new APK to be signed by the **exact same signing certificate** as the currently installed one. If the key changes, Android displays:
```text
INSTALL_FAILED_UPDATE_INCOMPATIBLE: Existing package com.LanPiaoPiao.PlantsVsZombiesRH signatures do not match newer version
```

By making this signing key public and permanently tracked in the repository:
1. **Seamless Updates**: Users who install `v4.0.5` can directly install `v4.1` (and all future updates) without having to backup saves, uninstall, or reinstall.
2. **Community Reproducibility**: Any contributor or developer building from source will generate APKs that are 100% compatible with existing player installations.
3. **Public Verification**: Anyone can inspect and verify that a downloaded APK originates from this project and has not been altered by third parties.

---

## 2. Key & Certificate Details

| Property | Value |
| :--- | :--- |
| **Keystore File** | `docs/signing/pvz-fusion-release.keystore` |
| **Public Certificate** | `docs/signing/certificate.pem` |
| **Keystore Format** | JKS |
| **Key Alias** | `androiddebugkey` |
| **Keystore Password** | `android` |
| **Key Password** | `android` |
| **Signature Algorithm** | `SHA256withRSA` (2048-bit RSA) |
| **Valid Until** | March 11, 2044 |

### Certificate Fingerprints
* **SHA-256**: `1E:08:A9:03:AE:F9:C3:A7:21:51:0B:64:EC:76:4D:01:D3:D0:94:EB:95:41:61:B6:25:44:EA:8F:18:7B:59:53`
* **SHA-1**: `5D:08:26:4B:44:E0:E5:3F:BC:CC:70:B4:F0:16:47:4C:C6:C5:AB:5C`
* **Public Key SHA-256**: `35:3A:10:27:74:90:7F:E7:6F:DC:23:87:26:1A:21:CB:48:D1:81:A8:64:EF:12:5B:74:81:6F:AC:F0:A1:77:DF`

---

## 3. How to Sign an APK

### Method A: Automated via Toolkit (Recommended)
Running the repository builder uses this keystore automatically:
```powershell
python scripts/build_all.py
```

### Method B: Manual Signing via `uber-apk-signer`
```powershell
java -jar build/tools/uber-apk-signer.jar `
  --apks path/to/unsigned.apk `
  --ks docs/signing/pvz-fusion-release.keystore `
  --ksAlias androiddebugkey `
  --ksPass android `
  --ksKeyPass android `
  --out build/signed/
```

### Method C: Manual Signing via Android SDK `apksigner`
```powershell
# 1. Align the APK
zipalign -p -f -v 4 unsigned.apk aligned.apk

# 2. Sign with apksigner (v1, v2, v3)
apksigner sign `
  --ks docs/signing/pvz-fusion-release.keystore `
  --ks-key-alias androiddebugkey `
  --ks-pass pass:android `
  --key-pass pass:android `
  --out final-signed.apk `
  aligned.apk
```

---

## 4. How to Verify an APK's Signature

To confirm an APK was signed with the official project key:

### Using Android SDK `apksigner`:
```powershell
apksigner verify --print-certs path/to/PvZ-Fusion-4.0.5-English-Android.apk
```
Look for:
```text
Signer #1 certificate SHA-256 digest: 1e08a903aef9c3a721510b64ec764d01d3d094eb954161b62544ea8f187b5953
```

### Using `uber-apk-signer`:
```powershell
java -jar build/tools/uber-apk-signer.jar --onlyVerify --apks path/to/PvZ-Fusion-4.0.5-English-Android.apk --verbose
```
