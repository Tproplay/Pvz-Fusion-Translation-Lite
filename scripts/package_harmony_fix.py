#!/usr/bin/env python3
"""Package BepInEx Harmony Compatibility Fix into a standalone distribution zip."""

import os
import shutil
import zipfile
from pathlib import Path


def create_harmony_fix_zip() -> Path:
    pkg_dir = Path("build/bepinex_harmony_fix")
    if pkg_dir.exists():
        shutil.rmtree(pkg_dir)
    pkg_dir.mkdir(parents=True, exist_ok=True)

    core_dir = pkg_dir / "BepInEx" / "core"
    plugins_dir = pkg_dir / "BepInEx" / "plugins"
    core_dir.mkdir(parents=True, exist_ok=True)
    plugins_dir.mkdir(parents=True, exist_ok=True)

    harmony_src = Path(r"c:\Users\Tproplay\Games\Pvz\Fusion RH\PvZ Fusion 4.0.5 Modded\BepInEx\core\0Harmony.dll")
    compat_src = Path(r"c:\Users\Tproplay\Games\Pvz\Fusion RH\PvZ Fusion 4.0.5 Modded\BepInEx\plugins\Fusion.Android.Compatibility.dll")
    patch_script = Path("scripts/patch_bepinex_harmony.py")

    shutil.copy2(harmony_src, core_dir / "0Harmony.dll")
    if compat_src.exists():
        shutil.copy2(compat_src, plugins_dir / "Fusion.Android.Compatibility.dll")
    shutil.copy2(patch_script, pkg_dir / "patch_bepinex_harmony.py")

    readme_content = """========================================================================
 Plants vs. Zombies: Fusion 4.0.5 - BepInEx Mod Compatibility Fix
========================================================================

WHY IS THIS NEEDED?
In PvZ Fusion 4.0+, internal placement check methods were refactored
(e.g., CreatePlant.MixBombCheck was moved to PlaceRule.MixBombRule.Check).
Many community mods created for earlier versions (such as BigSuperGatling,
BloodMoonPhantomCabbage, PVZCustomization, MoonlightNightGodCabbage, etc.)
still attempt to patch CreatePlant.MixBombCheck without a Prepare() guard.
Standard HarmonyX throws a fatal ArgumentException when a target method is
missing, causing BepInEx to abort loading the entire mod.

WHAT DOES THIS FIX DO?
1. Patched 0Harmony.dll:
   Gracefully skips missing patch target methods instead of crashing plugin
   loading. All working patches (attacks, almanac, visual effects, buffs)
   continue running smoothly.
2. Fusion.Android.Compatibility.dll:
   Supplies a missing compatibility bridge for mods ported from Android.

HOW TO INSTALL:
Option A (Easiest - Drag & Drop):
  Extract the contents of this zip directly into your modded game folder
  (where PlantsVsZombiesRH.exe is located), overwriting when prompted.
  (It replaces BepInEx/core/0Harmony.dll).

Option B (Using the Python Patcher Script):
  Run `python patch_bepinex_harmony.py "path/to/BepInEx/core/0Harmony.dll"`
========================================================================
"""
    (pkg_dir / "README.txt").write_text(readme_content, encoding="utf-8")

    zip_out = Path("build/BepInEx-Harmony-Fix-v4.0.5.zip")
    with zipfile.ZipFile(zip_out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for root, dirs, files in os.walk(pkg_dir):
            for f in sorted(files):
                fp = Path(root) / f
                arc = fp.relative_to(pkg_dir).as_posix()
                z.write(fp, arc)
                print(f"  + {arc} ({fp.stat().st_size} bytes)")

    print(f"\nCreated {zip_out} ({zip_out.stat().st_size / 1024:.1f} KB)")
    return zip_out


if __name__ == "__main__":
    create_harmony_fix_zip()
