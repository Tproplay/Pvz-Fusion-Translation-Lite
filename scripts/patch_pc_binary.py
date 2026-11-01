#!/usr/bin/env python3
"""Patch PC GameAssembly.dll for level title discrimination in Tower Defense levels.

PvZ Fusion 4.1's GameLevel.Tower.TowerLevelData initializes all Classic Tower
levels through a common routine that hardcodes the string literal '经典塔防：进化'
(Tower Defense: Evolution) to InGameUI.SetUniqueText.
This patch installs a small detour into the padding at the end of the .text section:
- If called by ClassicTower1 (caller return address 0x181e19553), dynamically sets
  the level title to 'ZombiesTD Classic 1' via il2cpp_string_new.
- If called by ClassicTower2 (caller return address 0x181e197ca), dynamically sets
  the level title to 'ZombiesTD Classic 2' via il2cpp_string_new.
- Otherwise, preserves the default 'Tower Defense: Evolution' string literal.
"""

from __future__ import annotations

import shutil
import struct
import sys
from pathlib import Path

CAVE_FILE_OFFSET = 0x3EC220
HOOK_FILE_OFFSET = 0x1E19CFA

# Expected original bytes at hook site:
# mov rdx, [rip + 0x16d40c7] (loads StringLiteral 16147 = 经典塔防：进化)
EXPECTED_ORIGINAL_HOOK = b"\x48\x8b\x15\xc7\x40\x6d\x01"


def assemble_level_title_cave(
    cave_rva: int,
    str_new_rva: int,
    set_text_rva: int,
    str_19754_rva: int,
) -> bytes:
    code = bytearray()

    # 1. Save InGameUI instance
    code.extend(b"\x48\x89\x44\x24\x08")  # mov [rsp + 8], rax

    # 2. Check caller return address at [rsp + 0x28]
    code.extend(b"\x0f\xb7\x54\x24\x28")  # movzx edx, word ptr [rsp + 0x28]
    code.extend(b"\x66\x81\xfa\x53\x95")  # cmp dx, 0x9553 (ClassicTower1)
    je_lvl1_idx = len(code)
    code.extend(b"\x74\x00")              # je is_level1

    code.extend(b"\x66\x81\xfa\xca\x97")  # cmp dx, 0x97ca (ClassicTower2)
    je_lvl2_idx = len(code)
    code.extend(b"\x74\x00")              # je is_level2

    # 3. Default: load original StringLiteral 19754 (Tower Defense: Evolution)
    mov_default_idx = len(code)
    code.extend(b"\x48\x8b\x15\x00\x00\x00\x00")  # mov rdx, [rip + disp_to_19754]
    jmp_call_idx = len(code)
    code.extend(b"\xeb\x00")                       # jmp call_set_text

    # is_level1:
    off_is_level1 = len(code)
    code[je_lvl1_idx + 1] = off_is_level1 - (je_lvl1_idx + 2)
    lea_lvl1_idx = len(code)
    code.extend(b"\x48\x8d\x0d\x00\x00\x00\x00")  # lea rcx, [rip + str_level1]
    call_str_new1_idx = len(code)
    code.extend(b"\xe8\x00\x00\x00\x00")          # call il2cpp_string_new
    code.extend(b"\x48\x89\xc2")                  # mov rdx, rax
    jmp_call2_idx = len(code)
    code.extend(b"\xeb\x00")                       # jmp call_set_text

    # is_level2:
    off_is_level2 = len(code)
    code[je_lvl2_idx + 1] = off_is_level2 - (je_lvl2_idx + 2)
    lea_lvl2_idx = len(code)
    code.extend(b"\x48\x8d\x0d\x00\x00\x00\x00")  # lea rcx, [rip + str_level2]
    call_str_new2_idx = len(code)
    code.extend(b"\xe8\x00\x00\x00\x00")          # call il2cpp_string_new
    code.extend(b"\x48\x89\xc2")                  # mov rdx, rax

    # call_set_text:
    off_call_set_text = len(code)
    code[jmp_call_idx + 1] = off_call_set_text - (jmp_call_idx + 2)
    code[jmp_call2_idx + 1] = off_call_set_text - (jmp_call2_idx + 2)

    code.extend(b"\x48\x8b\x4c\x24\x08")          # mov rcx, [rsp + 8] (InGameUI instance)
    code.extend(b"\x45\x33\xc0")                  # xor r8d, r8d
    call_set_text_idx = len(code)
    code.extend(b"\xe8\x00\x00\x00\x00")          # call InGameUI.SetUniqueText

    code.extend(b"\x48\x8b\x44\x24\x08")          # mov rax, [rsp + 8]
    code.extend(b"\x48\x83\xc4\x20")              # add rsp, 32
    code.extend(b"\x5b")                          # pop rbx
    code.extend(b"\xc3")                          # ret

    # Null-terminated UTF-8 strings
    off_str1 = len(code)
    code.extend(b"ZombiesTD Classic 1\x00")
    off_str2 = len(code)
    code.extend(b"ZombiesTD Classic 2\x00")

    # Relocate relative 32-bit displacements
    # 1. mov rdx, [rip + disp_to_19754]
    ins_end = cave_rva + mov_default_idx + 7
    struct.pack_into("<i", code, mov_default_idx + 3, str_19754_rva - ins_end)

    # 2. lea rcx, [rip + str_level1]
    ins_end = cave_rva + lea_lvl1_idx + 7
    struct.pack_into("<i", code, lea_lvl1_idx + 3, (cave_rva + off_str1) - ins_end)

    # 3. call il2cpp_string_new (1)
    ins_end = cave_rva + call_str_new1_idx + 5
    struct.pack_into("<i", code, call_str_new1_idx + 1, str_new_rva - ins_end)

    # 4. lea rcx, [rip + str_level2]
    ins_end = cave_rva + lea_lvl2_idx + 7
    struct.pack_into("<i", code, lea_lvl2_idx + 3, (cave_rva + off_str2) - ins_end)

    # 5. call il2cpp_string_new (2)
    ins_end = cave_rva + call_str_new2_idx + 5
    struct.pack_into("<i", code, call_str_new2_idx + 1, str_new_rva - ins_end)

    # 6. call InGameUI.SetUniqueText
    ins_end = cave_rva + call_set_text_idx + 5
    struct.pack_into("<i", code, call_set_text_idx + 1, set_text_rva - ins_end)

    return bytes(code)


def patch_gameassembly(source_path: Path, output_path: Path) -> bool:
    data = bytearray(source_path.read_bytes())

    # Verify unpatched or already-patched signature
    current_hook = bytes(data[HOOK_FILE_OFFSET : HOOK_FILE_OFFSET + len(EXPECTED_ORIGINAL_HOOK)])
    if current_hook != EXPECTED_ORIGINAL_HOOK and current_hook[0] != 0xE9:
        print(f"Warning: Unexpected hook site bytes: {current_hook.hex()}", file=sys.stderr)
        return False

    cave_rva = CAVE_FILE_OFFSET + 0xC00
    hook_rva = HOOK_FILE_OFFSET + 0xC00

    str_new_rva = 0x31B8F0
    set_text_rva = 0x1B5D2D0 + 0xC00
    str_19754_rva = 0x34EDDC8 - 0x3420800 + 0x3422000

    cave_bytes = assemble_level_title_cave(
        cave_rva=cave_rva,
        str_new_rva=str_new_rva,
        set_text_rva=set_text_rva,
        str_19754_rva=str_19754_rva,
    )

    # Install cave in .text padding
    data[CAVE_FILE_OFFSET : CAVE_FILE_OFFSET + len(cave_bytes)] = cave_bytes

    # Install hook: jmp cave (e9 disp32) + 2x nop
    hook_disp = cave_rva - (hook_rva + 5)
    hook_bytes = b"\xe9" + struct.pack("<i", hook_disp) + b"\x90\x90"
    data[HOOK_FILE_OFFSET : HOOK_FILE_OFFSET + len(hook_bytes)] = hook_bytes

    output_path.write_bytes(data)
    print(f"Successfully patched {output_path.name}: installed {len(cave_bytes)}b title detour.")
    return True


if __name__ == "__main__":
    game_dir = Path("build/PC_PVZ-Fusion-4.1")
    dll_target = game_dir / "GameAssembly.dll"
    dll_orig = game_dir / "GameAssembly.dll.orig"
    if not dll_orig.exists():
        shutil.copy2(dll_target, dll_orig)
        print(f"Created clean backup: {dll_orig}")
    patch_gameassembly(dll_orig, dll_target)
