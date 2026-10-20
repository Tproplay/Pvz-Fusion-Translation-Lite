#!/usr/bin/env python3
"""Build both PC and Android English translation releases for PvZ Fusion 4.0.5.

Pipeline:
1. PC Build:
   - il2cpp_data/Metadata/global-metadata.dat
   - data.unity3d (Almanac, Help guide, UI text, textures, PC typography)
2. Android Build:
   - global-metadata.dat (mobile-aligned)
   - data.unity3d (mobile size tags, textures)
   - package_apk_payload.py (replace payloads in official base APK)
   - uber-apk-signer.jar (zipalign + v1/v2/v3 signing)
"""

from __future__ import annotations

import argparse
import glob
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


def build_all(
    pc_dir: Path,
    data_dir: Path,
    base_apk: Path,
    output_dir: Path,
    tools_dir: Path,
) -> int:
    total_start = time.time()
    print("=" * 70)
    print("PvZ Fusion 4.0.5 — Full Dual-Platform Translation Release Builder")
    print("=" * 70)

    py_exe = sys.executable
    scripts_dir = Path(__file__).resolve().parent

    pc_output = output_dir / "pc-405"
    android_output = output_dir / "android-405"
    pc_output.mkdir(parents=True, exist_ok=True)
    android_output.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------------
    # 1. BUILD PC VERSION
    # -------------------------------------------------------------
    print("\n" + "#" * 60)
    print(" STEP 1: Building PC Version")
    print("#" * 60)
    cmd_pc = [
        py_exe,
        str(scripts_dir / "build_pc.py"),
        "--pc-dir", str(pc_dir),
        "--data-dir", str(data_dir),
        "--output-dir", str(pc_output),
    ]
    run_command(cmd_pc, "Building PC English release")

    # -------------------------------------------------------------
    # 2. BUILD ANDROID VERSION
    # -------------------------------------------------------------
    print("\n" + "#" * 60)
    print(" STEP 2: Building Android Version")
    print("#" * 60)

    # Ensure base assets for Android exist
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

    # A. Android Metadata
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

    # B. Android Unity Bundle
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

    # C. Package Unsigned APK
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

    # D. Sign APK
    signer_jar = tools_dir / "uber-apk-signer.jar"
    if not signer_jar.exists():
        signer_jar = Path("temp/uber-apk-signer.jar")
    if not signer_jar.exists():
        raise FileNotFoundError(f"uber-apk-signer.jar not found in {tools_dir}")

    signed_dir = android_output / "signed"
    signed_dir.mkdir(parents=True, exist_ok=True)
    cmd_sign = [
        "java", "-jar", str(signer_jar),
        "--apks", str(unsigned_apk),
        "--out", str(signed_dir),
    ]
    run_command(cmd_sign, "Signing Android APK (v1, v2, v3)")

    # E. Move and name final signed APK
    final_signed_name = "PvZ-Fusion-4.0.5-English-Android.apk"
    final_signed_path = android_output / final_signed_name

    matched_apks = list(signed_dir.glob("*-aligned-debugSigned.apk"))
    if matched_apks:
        shutil.move(str(matched_apks[0]), str(final_signed_path))
        print(f"-> Signed APK ready: {final_signed_path}")
    else:
        print(f"WARNING: Could not locate signed APK in {signed_dir}")

    elapsed = round(time.time() - total_start, 2)
    print("\n" + "=" * 70)
    print(f"DUAL-PLATFORM BUILD COMPLETE in {elapsed}s!")
    print(f"PC Executable:    {pc_dir / 'PlantsVsZombiesRH.exe'}")
    print(f"Android APK:      {final_signed_path}")
    print("=" * 70)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pc-dir",
        type=Path,
        default=Path("build/PC_PVZ-Fusion-4.0.5"),
        help="Path to PC game folder (default: build/PC_PVZ-Fusion-4.0.5)",
    )
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
        return build_all(
            pc_dir=args.pc_dir,
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
