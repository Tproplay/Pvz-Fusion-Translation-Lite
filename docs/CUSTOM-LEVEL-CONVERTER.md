# Custom Level Port Converter

A standalone CLI tool that translates PvZ Fusion **custom level JSON files** between Chinese and English port/node names, so community-made levels load and connect correctly in the English build.

### 📥 Downloads
- **GitHub Release (Direct ZIP)**: [PvZ-Fusion-Custom-Level-Converter.zip](https://github.com/Tproplay/Pvz-Fusion-Translation-Lite/releases/download/v4.1/PvZ-Fusion-Custom-Level-Converter.zip)
- **Google Drive Mirror**: [Google Drive Link](https://drive.google.com/file/d/1-IDkf0dmqLkaIBYpWeSGc36VwwVnNsDd/view?usp=sharing)

---

## Why This Tool Exists

PvZ Fusion's level editor stores every node connection and port reference by its **display name** — there is no separate internal key. When you load a level made in the Chinese game into the English build, the port names in the saved JSON file (e.g. `"触发"`, `"行"`, `"完成"`) no longer match what the compiled English binary expects (e.g. `"Trigger"`, `"Row"`, `"On Complete"`), so:

- **Connection wires snap off** — the visual lines between nodes break and display as disconnected.
- **Events never fire** — trigger outputs fail to route to their target node inputs at runtime.
- **Input defaults silently revert** — node parameters fall back to zero/null instead of their configured values.
- **The validator logs false warnings** — `"Wired port does not exist; may be from a different version"`.

This tool fixes all of that by translating port names in the JSON before you import the level.

---

## What It Converts

The converter touches **three places** inside a custom level JSON file:

| Field | Location | Example |
|---|---|---|
| `sourcePortName` / `targetPortName` | `eventNodeGraph.connections[]` | `"触发"` → `"Trigger"` |
| `portName` | `nodes[].inputDefaults[]` | `"行"` → `"Row"` |
| `*_PortName` fields | `references.RefIds[].data` | `"trigger_PortName": "触发"` → `"Trigger"` |

It recursively scans the entire JSON structure and handles any nesting depth, including:
- Flat `eventNodeGraph` / `eventGraph` / `graph` objects
- Unity `[SerializeReference]` polymorphic data inside `references.RefIds`

---

## Usage

### Option 1 — Drag & Drop (Windows)

Drag one or more `.json` level files (or a folder containing levels) onto **`convert_level.bat`**. The script will convert them and keep the terminal window open so you can read the summary.

```
convert_level.bat my_level.json
convert_level.bat path\to\levels_folder\
```

---

### Option 2 — Command Line

Requires **Python 3.9+**. No extra packages needed — the script is self-contained.

```bash
# Convert a single file (outputs my_level_en.json by default)
python convert_custom_level.py my_level.json

# Specify an explicit output file
python convert_custom_level.py -i my_level.json -o my_level_translated.json

# Convert a whole folder (outputs *_en.json copies next to each original)
python convert_custom_level.py path/to/levels/

# Overwrite the originals in-place, with automatic .bak backups
python convert_custom_level.py path/to/levels/ --in-place --backup

# Reverse convert: English to Chinese (for round-trip testing)
python convert_custom_level.py my_level_en.json --direction en2cn

# Dry run: scan and report matches without writing any files
python convert_custom_level.py my_level.json --dry-run

# Quiet mode: suppress per-file lines, only show final summary
python convert_custom_level.py path/to/levels/ -q
```

---

### Full Flag Reference

```
usage: convert_custom_level [-h] [-i INPUT] [-o OUTPUT]
                            [-d {cn2en,en2cn}] [-w] [-b]
                            [--map-file PATH] [--dry-run] [-q]
                            [target]

positional arguments:
  target               Level JSON file or directory (alternative to -i)

options:
  -i, --input PATH     Input level JSON file or directory
  -o, --output PATH    Output JSON file or directory
                       (default: *_en.json beside the original)
  -d, --direction      cn2en  Chinese to English  (default)
                       en2cn  English to Chinese
  -w, --in-place       Overwrite the input files directly
  -b, --backup         Write a .bak copy before overwriting (use with -w)
  --map-file PATH      Custom path to eventnode_port_map.json
                       (auto-detected from the script's folder by default)
  --dry-run            Test the conversion without writing any output files
  -q, --quiet          Suppress per-file status lines
  -h, --help           Show full help
```

---

## Example Output

```
Converting [cn2en]: 101CustomIZ1_level.json -> 101CustomIZ1_level_en.json

=======================================================
PvZ Fusion Custom Level Conversion Summary
=======================================================
Direction                : cn2en
Files Processed          : 1
Connection Ports Updated : 23
Input Defaults Updated   : 4
Node Port Fields Updated : 7
Unmapped Ports           : None (100% matched!)
=======================================================
```

If the tool prints **Unmapped Ports**, those are port strings that have no entry in `eventnode_port_map.json`. The level file still converts (all matched ports are updated), but unmapped ports are left as-is. You can add missing entries to the port map and re-run.

---

## Files

| File | Purpose |
|---|---|
| `convert_custom_level.py` | Main CLI script — Python 3.9+, no extra dependencies |
| `convert_level.bat` | Windows drag-and-drop launcher |
| `eventnode_port_map.json` | Port and node name translation dictionary (728 ports, 272 node types) |
| `generate_eventnode_map.py` | Regenerates `eventnode_port_map.json` from the game's `dump.cs` (maintainers only) |

The script searches for `eventnode_port_map.json` in:
1. The same folder as `convert_custom_level.py`
2. `translation-data/Strings/` relative to the repo root
3. The current working directory

If none is found, a built-in fallback dictionary of ~80 essential ports is used automatically.

---

## Port Map Coverage (v4.1)

The included `eventnode_port_map.json` covers all **272 EventNode classes** and **728 unique port mappings** extracted from the PvZ Fusion 4.1 `GameAssembly.dll`, including:

- All execution flow ports: `触发`, `完成`, `失败`, `循环体`, `循环结束`, etc.
- All data ports: `行`, `列`, `植物`, `僵尸`, `伤害`, `血量`, `阳光`, etc.
- All `*_PortName` serialized field values from `BranchNode`, `MovePlantNode`, `WhileLoopNode`, and all other `EventNodeBase` subclasses
- Hardcoded ports from hybrid nodes (`MoveZombieNode`, `CreateZombieNode`, `MergeMultipleChoiceOptionListsNode`, etc.)

---

## Limitations

- **Does not translate node display labels or `customName`** — only port wiring names and serialized field names are modified.
- **Does not translate level metadata** (level name, tip text, zombie descriptions). Use the main translation build pipeline for those.
- **Round-trip fidelity**: `en2cn` uses canonical reverse mappings for common ambiguous ports (e.g. `"Value"` always reverses to `"值"`, not `"数值"`). Edge cases involving uncommon synonyms may not round-trip exactly.
