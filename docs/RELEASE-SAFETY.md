# Release safety notes

> **Historical Note:** This document records legacy release notes (3.8.1/4.0). For current 4.0.5 documentation, build pipeline, and developer guides, see [RESEARCH-4.0.5.md](RESEARCH-4.0.5.md) and [CLAUDE.md](CLAUDE.md).


## What the release audit establishes

The 3.8.1 English release is built from the official Chinese 3.8.1 Android APK
(SHA-256 `1d6789a388621f544ea1c29778acfb12645933b67153ecaed4f54a48c7fa43c0`)
by replacing
only:

- `assets/bin/Data/data.unity3d`
- `assets/bin/Data/Managed/Metadata/global-metadata.dat`

`scripts/audit_apk_release.py` compares every ZIP entry to that shell. A pass
requires the Android manifest, `classes.dex`, all native libraries, resources,
and every other non-signature entry to be byte-identical. It also checks ZIP
integrity, duplicate/path-traversal entries, package metadata, permissions, and
the exact set of changed payloads.

This is strong evidence that the translation process did not add executable
Android code. It is not an absolute guarantee about the upstream game or every
possible runtime behavior.

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

The package remains `com.LanPiaoPiao.PlantsVsZombiesRH` for compatibility with
the game's external data paths. Because the English release has a dedicated
project signature, users must back up saves and uninstall a Chinese, Joseph,
or aha build before installing it. Later releases signed with the same project
key can update this release in place.

The official signing keystore and certificate are tracked directly in the repository at [docs/signing/SIGNING-KEY.md](signing/SIGNING-KEY.md):
- **Keystore**: `docs/signing/pvz-fusion-release.keystore`
- **Certificate PEM**: `docs/signing/certificate.pem`
- **Certificate SHA-256**: `1E:08:A9:03:AE:F9:C3:A7:21:51:0B:64:EC:76:4D:01:D3:D0:94:EB:95:41:61:B6:25:44:EA:8F:18:7B:59:53`

## What maintainers must publish

- exact APK filename, size, and SHA-256;
- signing certificate SHA-256;
- source tag/commit;
- `apksigner verify --verbose --print-certs` result;
- comparative audit result;
- device models/Android versions used for smoke testing;
- a clear save-backup and uninstall warning.
