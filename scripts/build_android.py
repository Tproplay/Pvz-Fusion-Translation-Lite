#!/usr/bin/env python3
"""Build Android English translation release for PvZ Fusion 4.0.5.

Pipeline:
1. Android Metadata: global-metadata.dat (aligned with Android base)
2. Android Unity Bundle: data.unity3d (mobile size tags, textures, font)
3. Package Unsigned APK: package_apk_payload.py
4. Sign APK: uber-apk-signer.jar (zipalign + v1/v2/v3 signing)
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path


def run_command(cmd: list[str], desc: str) -> None:
    print(f"\n--> {desc}...")
    res = subprocess.run(cmd)
    if res.returncode != 0:
        raise RuntimeError(f"{desc} failed with exit code {res.returncode}")


def build_android(
    data_dir: Path,
    base_apk: Path,
    output_dir: Path,
    tools_dir: Path,
) -> int:
    total_start = time.time()
    print("=" * 70)
    print("PvZ Fusion 4.0.5 — Android Translation Release Builder")
    print("=" * 70)

    py_exe = sys.executable
    scripts_dir = Path(__file__).resolve().parent

    android_output = output_dir / "android-405"
    android_output.mkdir(parents=True, exist_ok=True)

    meta_orig = android_output / "global-metadata.dat.orig"
    bundle_orig = android_output / "base-data.unity3d"

    if not meta_orig.exists() or not bundle_orig.exists():
        if not base_apk.exists():
            raise FileNotFoundError(f"Base APK not found at {base_apk}")
        print(f"Extracting base data files from {base_apk}...")
        import zipfile
        with zipfile.ZipFile(base_apk, "r") as z:
            if not meta_orig.exists():
                with meta_orig.open("wb") as f:
                    f.write(z.read("assets/bin/Data/Managed/Metadata/global-metadata.dat"))
                print(f"Extracted {meta_orig}")
            if not bundle_orig.exists():
                with bundle_orig.open("wb") as f:
                    f.write(z.read("assets/bin/Data/data.unity3d"))
                print(f"Extracted {bundle_orig}")

    # 1. Android Metadata
    meta_target = android_output / "global-metadata.dat"
    meta_report = android_output / "metadata-report.json"
    cmd_android_meta = [
        py_exe,
        str(scripts_dir / "build_metadata_translation.py"),
        "--base", str(meta_orig),
        "--strings-dir", str(data_dir / "Strings"),
        "--output", str(meta_target),
        "--report", str(meta_report),
    ]
    run_command(cmd_android_meta, "Building Android global-metadata.dat")

    # 2. Android Unity Bundle
    bundle_target = android_output / "data.unity3d"
    bundle_report = android_output / "bundle-report.json"
    cmd_android_bundle = [
        py_exe,
        str(scripts_dir / "build_405_bundle.py"),
        "--base-bundle", str(bundle_orig),
        "--data-dir", str(data_dir),
        "--output", str(bundle_target),
        "--report", str(bundle_report),
        "--platform", "android",
        "--packer", "lz4",
    ]
    run_command(cmd_android_bundle, "Building Android data.unity3d")

    # 3. Package Unsigned APK
    unsigned_apk = android_output / "unsigned-pvzrh4.0.5.apk"
    pkg_report = android_output / "package-report.json"
    cmd_pkg = [
        py_exe,
        str(scripts_dir / "package_apk_payload.py"),
        "--base-apk", str(base_apk),
        "--data-bundle", str(bundle_target),
        "--metadata", str(meta_target),
        "--output", str(unsigned_apk),
        "--report", str(pkg_report),
    ]
    run_command(cmd_pkg, "Packaging APK payload (data.unity3d + metadata)")

    # 4. Sign APK
    signer_jar = tools_dir / "uber-apk-signer.jar"
    if not signer_jar.exists():
        signer_jar = Path("temp/uber-apk-signer.jar")
    if not signer_jar.exists():
        raise FileNotFoundError(f"uber-apk-signer.jar not found in {tools_dir}")

    signed_dir = android_output / "signed"
    signed_dir.mkdir(parents=True, exist_ok=True)

    keystore_path = Path("docs/signing/pvz-fusion-release.keystore")
    cmd_sign = [
        "java", "-jar", str(signer_jar),
        "--apks", str(unsigned_apk),
        "--out", str(signed_dir),
    ]
    if keystore_path.exists():
        cmd_sign.extend([
            "--ks", str(keystore_path),
            "--ksAlias", "androiddebugkey",
            "--ksPass", "android",
            "--ksKeyPass", "android",
        ])

    run_command(cmd_sign, "Signing Android APK (v1, v2, v3)")

    # 5. Move and name final signed APK
    final_signed_name = "PvZ-Fusion-4.0.5-English-Android.apk"
    final_signed_path = android_output / final_signed_name

    matched_apks = list(signed_dir.glob("*-aligned-*.apk"))
    if matched_apks:
        shutil.move(str(matched_apks[0]), str(final_signed_path))
        print(f"-> Signed APK ready: {final_signed_path}")
    else:
        raise RuntimeError(f"Could not locate signed APK in {signed_dir}")

    elapsed = round(time.time() - total_start, 2)
    print("\n" + "=" * 70)
    print(f"ANDROID BUILD COMPLETE in {elapsed}s!")
    print(f"Android APK: {final_signed_path}")
    print("=" * 70)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("translation-data"),
        help="Path to translation-data directory (default: translation-data)",
    )
    parser.add_argument(
        "--base-apk",
        type=Path,
        default=Path("build/pvzrh4.0.5.apk"),
        help="Path to clean official base Android APK (default: build/pvzrh4.0.5.apk)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("build"),
        help="Base output build directory (default: build)",
    )
    parser.add_argument(
        "--tools-dir",
        type=Path,
        default=Path("build/tools"),
        help="Path to tools directory containing uber-apk-signer.jar (default: build/tools)",
    )

    args = parser.parse_args()
    try:
        return build_android(
            data_dir=args.data_dir,
            base_apk=args.base_apk,
            output_dir=args.output_dir,
            tools_dir=args.tools_dir,
        )
    except Exception as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
