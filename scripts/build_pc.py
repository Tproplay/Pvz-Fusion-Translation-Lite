#!/usr/bin/env python3
"""Build PC English translation for PvZ Fusion 4.0.5.

Rebuilds:
1. IL2CPP string literal metadata (global-metadata.dat)
2. Unity data bundle (data.unity3d) including TextAssets, serialized UI, textures, and font
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path


def ensure_orig_backup(target: Path, orig: Path) -> None:
    if not orig.exists():
        if target.exists():
            shutil.copy2(target, orig)
            print(f"Created clean base backup: {orig}")
        else:
            raise FileNotFoundError(f"Neither {orig} nor {target} found.")


def build_pc(
    pc_dir: Path,
    data_dir: Path,
    output_dir: Path,
    skip_bundle: bool = False,
    skip_metadata: bool = False,
) -> int:
    start_time = time.time()
    print("=" * 60)
    print("PvZ Fusion 4.0.5 — PC Translation Builder")
    print("=" * 60)

    py_exe = sys.executable
    scripts_dir = Path(__file__).resolve().parent

    meta_target = pc_dir / "PlantsVsZombiesRH_Data/il2cpp_data/Metadata/global-metadata.dat"
    meta_orig = pc_dir / "PlantsVsZombiesRH_Data/il2cpp_data/Metadata/global-metadata.dat.orig"
    bundle_target = pc_dir / "PlantsVsZombiesRH_Data/data.unity3d"
    bundle_orig = pc_dir / "PlantsVsZombiesRH_Data/data.unity3d.orig"

    ensure_orig_backup(meta_target, meta_orig)
    ensure_orig_backup(bundle_target, bundle_orig)

    output_dir.mkdir(parents=True, exist_ok=True)
    meta_report = output_dir / "metadata-report.json"
    bundle_report = output_dir / "bundle-report.json"

    # 1. Build Metadata
    if not skip_metadata:
        print("\n[1/2] Building PC global-metadata.dat...")
        cmd_meta = [
            py_exe,
            str(scripts_dir / "build_metadata_translation.py"),
            "--base", str(meta_orig),
            "--strings-dir", str(data_dir / "Strings"),
            "--output", str(meta_target),
            "--report", str(meta_report),
        ]
        res = subprocess.run(cmd_meta)
        if res.returncode != 0:
            print(f"ERROR: Metadata build failed with code {res.returncode}")
            return res.returncode
        # Copy to output release directory
        shutil.copy2(meta_target, output_dir / "global-metadata.dat")
        print(f"-> Metadata built successfully: {meta_target}")
    else:
        print("\n[1/2] Skipping metadata build (--skip-metadata)")

    # 2. Build Unity Bundle
    if not skip_bundle:
        print("\n[2/2] Building PC data.unity3d...")
        cmd_bundle = [
            py_exe,
            str(scripts_dir / "build_405_bundle.py"),
            "--base-bundle", str(bundle_orig),
            "--data-dir", str(data_dir),
            "--output", str(bundle_target),
            "--report", str(bundle_report),
            "--platform", "pc",
            "--packer", "lz4",
        ]
        res = subprocess.run(cmd_bundle)
        if res.returncode != 0:
            print(f"ERROR: Bundle build failed with code {res.returncode}")
            return res.returncode
        # Copy to output release directory
        shutil.copy2(bundle_target, output_dir / "data.unity3d")
        print(f"-> Bundle built successfully: {bundle_target}")
    else:
        print("\n[2/2] Skipping bundle build (--skip-bundle)")

    elapsed = round(time.time() - start_time, 2)
    print("\n" + "=" * 60)
    print(f"PC Build Complete in {elapsed}s!")
    print(f"PC Game Location: {pc_dir / 'PlantsVsZombiesRH.exe'}")
    print(f"Artifacts Saved to: {output_dir}")
    print("=" * 60)
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
        "--output-dir",
        type=Path,
        default=Path("build/pc-405"),
        help="Path to output release artifacts directory (default: build/pc-405)",
    )
    parser.add_argument("--skip-bundle", action="store_true", help="Skip rebuilding data.unity3d")
    parser.add_argument("--skip-metadata", action="store_true", help="Skip rebuilding global-metadata.dat")

    args = parser.parse_args()
    return build_pc(
        pc_dir=args.pc_dir,
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        skip_bundle=args.skip_bundle,
        skip_metadata=args.skip_metadata,
    )


if __name__ == "__main__":
    sys.exit(main())
