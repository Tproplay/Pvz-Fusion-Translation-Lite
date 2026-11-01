# Release safety notes

> **Current Version:** v4.1. This document covers safety requirements and audit procedures for the PvZ Fusion English translation release.

## What the release audit establishes

The v4.1 English release is built from the official Chinese 4.1 game files by replacing only:

- `PlantsVsZombiesRH_Data/data.unity3d` (PC) / `assets/bin/Data/data.unity3d` (Android)
- `PlantsVsZombiesRH_Data/il2cpp_data/Metadata/global-metadata.dat` (PC) / `assets/bin/Data/Managed/Metadata/global-metadata.dat` (Android)

`scripts/audit_apk_release.py` compares every ZIP entry to the official shell APK. A pass requires the Android manifest, `classes.dex`, all native libraries, resources, and every other non-signature entry to be byte-identical. It also checks ZIP integrity, duplicate/path-traversal entries, package metadata, permissions, and the exact set of changed payloads.

> [!CAUTION]
> **No translation logic lives in scripts.** All Chinese→English mappings are stored in JSON files under `translation-data/`. Scripts only read those files. Any script that contains inline translation dictionaries violates project policy and must be refactored before release.

This is strong evidence that the translation process did not add executable Android code. It is not an absolute guarantee about the upstream game or every possible runtime behavior.

## Permissions inherited from the base APK

- `android.permission.INTERNET`
- `android.permission.READ_EXTERNAL_STORAGE`
- `android.permission.WRITE_EXTERNAL_STORAGE`

The translation does not add or change permissions. The app targets Android
35 and requests legacy external storage behavior from the original manifest.

For release `v3.8.1-en.1`, the audit confirms that all 32 other non-signature
entries are byte-identical to the official Chinese APK, including
`classes.dex` and all eight ARM native libraries. ZIP integrity, path safety,
and alignment pass; Windows Defender reported no threats on August 11, 2026.
One malware scan is supporting evidence, not a universal safety guarantee.

## Package and updates

The package remains `com.LanPiaoPiao.PlantsVsZombiesRH` for compatibility with the game's external data paths. Because the English release has a dedicated project signature, users must back up saves and uninstall a Chinese build before installing it. Later releases signed with the same project key can update in place.

The official signing keystore and certificate are tracked in the repository at [docs/signing/SIGNING-KEY.md](signing/SIGNING-KEY.md):
- **Keystore**: `docs/signing/pvz-fusion-release.keystore`
- **Certificate PEM**: `docs/signing/certificate.pem`
- **Certificate SHA-256**: `1E:08:A9:03:AE:F9:C3:A7:21:51:0B:64:EC:76:4D:01:D3:D0:94:EB:95:41:61:B6:25:44:EA:8F:18:7B:59:53`

## What maintainers must publish for each release

- exact PC ZIP filename, size, and SHA-256
- exact APK filename, size, and SHA-256
- signing certificate SHA-256
- source tag/commit and build date
- `apksigner verify --verbose --print-certs` result
- comparative audit result (`audit_apk_release.py` pass)
- device models / Windows versions used for smoke testing
- a clear save-backup warning for Android users
