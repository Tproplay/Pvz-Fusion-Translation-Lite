#!/usr/bin/env python3
"""Patch BepInEx 0Harmony.dll to gracefully skip missing target methods instead of crashing plugin loads.

In PvZ Fusion 4.0+, methods like CreatePlant.MixBombCheck were refactored into PlaceRule.MixBombRule.Check.
Mods written for older versions (e.g. BigSuperGatling, BloodMoonPhantomCabbage, etc.) still declare
[HarmonyPatch(typeof(CreatePlant), "MixBombCheck")] without a Prepare() check.
Standard HarmonyX throws ArgumentException on missing methods, causing BepInEx to fail loading the entire plugin.

This script patches PatchWithAttributes in 0Harmony.dll so that if a target method is missing (lastOriginal == null),
it jumps directly to the enumerator MoveNext instead of throwing, gracefully skipping the invalid patch and
allowing all remaining working patches (attacks, almanac, visuals, buffs) of the mod to load cleanly.
"""

import sys
import shutil
from pathlib import Path


def patch_0harmony(dll_path: Path) -> bool:
    if not dll_path.exists():
        print(f"File not found: {dll_path}")
        return False

    bak_path = dll_path.with_suffix(".dll.orig")
    if not bak_path.exists():
        shutil.copy2(dll_path, bak_path)
        print(f"Created backup at {bak_path}")

    with open(dll_path, "rb") as f:
        data = bytearray(f.read())

    # Signature: ldstr "Undefined target method for patch method " (token 0x70000d65)
    sig = b"\x72\x65\x0d\x00\x70"
    idx = data.find(sig)
    if idx == -1:
        # Check if already patched
        if b"\x2b\x2c" in data:
            print(f"{dll_path.name} appears to already be patched.")
            return True
        print(f"Could not find patch target signature in {dll_path}")
        return False

    if data[idx + 31] != 0x7A:  # 0x7a = throw
        print(f"Unexpected byte at throw position ({hex(data[idx + 31])}), aborting.")
        return False

    # Replace throw sequence with `br.s 0x2c` (jump +44 bytes directly to MoveNext) followed by NOPs (0x00)
    data[idx] = 0x2B
    data[idx + 1] = 0x2C
    for i in range(idx + 2, idx + 32):
        data[i] = 0x00

    with open(dll_path, "wb") as f:
        f.write(data)

    print(f"Successfully patched {dll_path}")
    return True


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"c:\Users\Tproplay\Games\Pvz\Fusion RH\PVZ-Fusion-4.0.5-MOD-ADDON+MAGNETAR-CLIENT-V2\BepInEx\core\0Harmony.dll")
    patch_0harmony(target)
