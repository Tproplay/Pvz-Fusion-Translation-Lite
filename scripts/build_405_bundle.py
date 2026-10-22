#!/usr/bin/env python3
"""Build and patch the Unity data.unity3d bundle for PvZ Fusion 4.0.5 (PC & Android).

Consumes clean translation data from translation-data/ directory:
1. Almanac TextAssets (LawnStrings, ZombieStrings, DetailStrings)
2. Serialized TextMesh Pro UI strings with proper 1-based regex group substitution
3. TrueType Font payloads (English.ttf into fzcq, fzjz, and 汉仪夏日体W)
4. Localized game, menu, and particle textures
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import time
from pathlib import Path
from typing import Any

import UnityPy
from PIL import Image

CJK_RE = re.compile(r"[\u3400-\u9fff]")
SIZE_TAG_RE = re.compile(r"</?size(?:=[^>]+)?>")
TEXT_OFFSET = 88




def read_tmp_text(raw: bytes) -> tuple[str, int] | None:
    if len(raw) < TEXT_OFFSET + 4:
        return None
    length = struct.unpack_from("<i", raw, TEXT_OFFSET)[0]
    if length < 0:
        return None
    start = TEXT_OFFSET + 4
    end = start + length
    if end > len(raw):
        return None
    padded_end = end + ((-length) & 3)
    if padded_end > len(raw):
        return None
    try:
        value = raw[start:end].decode("utf-8")
    except UnicodeDecodeError:
        return None
    return value, padded_end


def replace_tmp_text(raw: bytes, value: str) -> bytes:
    parsed = read_tmp_text(raw)
    if parsed is None:
        raise ValueError("object does not contain a supported TMP text field")
    _old, old_end = parsed
    encoded = value.encode("utf-8")
    field = struct.pack("<i", len(encoded)) + encoded
    field += b"\0" * ((-len(field)) & 3)
    return raw[:TEXT_OFFSET] + field + raw[old_end:]


UI_TEXT_OFFSET = 144


def read_ui_text(raw: bytes, valid_ids: set[int] | None = None) -> tuple[str, int] | None:
    if len(raw) < UI_TEXT_OFFSET + 4:
        return None
    try:
        _file_id, script_path_id = struct.unpack_from("<iq", raw, 16)
    except Exception:
        return None
    if valid_ids is not None:
        if script_path_id not in valid_ids:
            return None
    elif script_path_id not in (1568, 1574):
        return None
    length = struct.unpack_from("<i", raw, UI_TEXT_OFFSET)[0]
    if length < 0:
        return None
    start = UI_TEXT_OFFSET + 4
    end = start + length
    if end > len(raw):
        return None
    padded_end = end + ((-length) & 3)
    if padded_end > len(raw):
        return None
    try:
        value = raw[start:end].decode("utf-8")
    except UnicodeDecodeError:
        return None
    return value, padded_end


def replace_ui_text(raw: bytes, value: str, valid_ids: set[int] | None = None) -> bytes:
    parsed = read_ui_text(raw, valid_ids)
    if parsed is None:
        raise ValueError("object does not contain a supported UI.Text field")
    _old, old_end = parsed
    encoded = value.encode("utf-8")
    field = struct.pack("<i", len(encoded)) + encoded
    field += b"\0" * ((-len(field)) & 3)
    return raw[:UI_TEXT_OFFSET] + field + raw[old_end:]


def discover_ui_script_ids(env: UnityPy.Environment) -> tuple[set[int], set[int]]:
    tmp_ids = set()
    ui_text_ids = set()
    for obj in env.objects:
        if obj.type.name == "MonoScript":
            try:
                data = obj.read()
                cls = getattr(data, "m_ClassName", "")
                ns = getattr(data, "m_Namespace", "")
                if cls in ("TextMeshPro", "TextMeshProUGUI"):
                    tmp_ids.add(obj.path_id)
                elif cls == "Text" and ns == "UnityEngine.UI":
                    ui_text_ids.add(obj.path_id)
            except Exception:
                pass
    if not tmp_ids:
        tmp_ids = {2359, 3797, 2372, 3818}
    if not ui_text_ids:
        ui_text_ids = {1568, 1574}
    return tmp_ids, ui_text_ids


def serialized_string(value: str) -> bytes:
    encoded = value.encode("utf-8")
    field = struct.pack("<i", len(encoded)) + encoded
    return field + b"\0" * ((-len(field)) & 3)


def replace_runtime_backing_text(raw: bytes, backing_map: dict[str, str]) -> tuple[bytes, str, str] | None:
    for source, target in backing_map.items():
        source_field = serialized_string(source)
        if raw.endswith(source_field):
            return raw[: -len(source_field)] + serialized_string(target), source, target
    return None


def clean_size_tags(text: str) -> str:
    return SIZE_TAG_RE.sub("", text)


def render_regex_template(
    template: str,
    match: re.Match[str],
    exact_map: dict[str, str] | None = None,
) -> str:
    """Render regex replacement template using capture groups with 1-based or 0-based indices."""
    groups = match.groups()
    if not groups:
        return template

    translated_groups = [
        exact_map.get(g, g) if exact_map and g in exact_map else g
        for g in groups
    ]

    result = template
    has_zero = bool(re.search(r"\{0\}", result))

    for idx, val in enumerate(translated_groups):
        if has_zero:
            # 0-based indexing: {0} -> group 1, {1} -> group 2
            result = result.replace(f"{{{idx}}}", val)
        else:
            # 1-based indexing: {1} -> group 1, {2} -> group 2
            result = result.replace(f"{{{idx + 1}}}", val)
            result = result.replace(f"${idx + 1}", val)

    return result


def patch_text_assets(
    env: UnityPy.Environment,
    data_dir: Path,
    platform: str = "pc",
) -> dict[str, Any]:
    stats = {"patched_assets": []}
    almanac_dir = data_dir / "Almanac"
    strings_dir = data_dir / "Strings"

    with (almanac_dir / "LawnStringsTranslate.json").open("r", encoding="utf-8") as f:
        lawn_trans = json.load(f)
    with (almanac_dir / "ZombieStringsTranslate.json").open("r", encoding="utf-8") as f:
        zombie_trans = json.load(f)
    with (almanac_dir / "DetailStringsTranslate.json").open("r", encoding="utf-8") as f:
        detail_trans = json.load(f)
    with (strings_dir / "translation_strings.json").open("r", encoding="utf-8") as f:
        exact_strings = json.load(f)

    regex_map = {}
    with (strings_dir / "translation_regexs.json").open("r", encoding="utf-8") as f:
        regex_map.update(json.load(f))
    compiled_regexs = []
    for pat, repl in regex_map.items():
        try:
            compiled_regexs.append((re.compile(pat), repl))
        except Exception:
            pass

    almanac_type_map = {}
    if (strings_dir / "almanac_type_map.json").is_file():
        with (strings_dir / "almanac_type_map.json").open("r", encoding="utf-8") as f:
            almanac_type_map = json.load(f)

    custom_iz_level_map = {}
    if (strings_dir / "custom_iz_level_map.json").is_file():
        with (strings_dir / "custom_iz_level_map.json").open("r", encoding="utf-8") as f:
            custom_iz_level_map = json.load(f)

    tips_iz = {}
    if (strings_dir / "tips_iz.json").is_file():
        with (strings_dir / "tips_iz.json").open("r", encoding="utf-8") as f:
            tips_iz = json.load(f)

    tips_fs = {}
    if (strings_dir / "tips_fs.json").is_file():
        with (strings_dir / "tips_fs.json").open("r", encoding="utf-8") as f:
            tips_fs = json.load(f)

    trans_plants_by_id = {p["seedType"]: p for p in lawn_trans["plants"]}
    trans_zombies_by_id = {z["theZombieType"]: z for z in zombie_trans["zombies"]}

    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        name = obj.peek_name()

        if name == "LawnStrings":
            data = obj.read()
            tree = json.loads(data.m_Script)
            updated = 0
            for plant in tree.get("plants", []):
                t = trans_plants_by_id.get(plant.get("seedType"))
                if t:
                    record = dict(t)
                    for k in ("introduce", "info", "cost", "description"):
                        if k in record and isinstance(record[k], str):
                            record[k] = clean_size_tags(record[k])
                    plant.update(record)
                    updated += 1
            data.m_Script = json.dumps(tree, ensure_ascii=False, indent=4)
            data.save()
            stats["patched_assets"].append({"name": name, "plants_updated": updated})

        elif name == "ZombieStrings":
            data = obj.read()
            tree = json.loads(data.m_Script)
            updated = 0
            for zombie in tree.get("zombies", []):
                t = trans_zombies_by_id.get(zombie.get("theZombieType"))
                if t:
                    record = dict(t)
                    for k in ("introduce", "info", "description"):
                        if k in record and isinstance(record[k], str):
                            record[k] = clean_size_tags(record[k])
                    zombie.update(record)
                    updated += 1
            data.m_Script = json.dumps(tree, ensure_ascii=False, indent=4)
            data.save()
            stats["patched_assets"].append({"name": name, "zombies_updated": updated})

        elif name == "DetailStrings":
            data = obj.read()
            tree = json.loads(data.m_Script)
            updated = 0
            for d in tree.get("details", []):
                orig_title = d.get("title", "")
                if orig_title in detail_trans:
                    text_val = detail_trans[orig_title]
                    if isinstance(text_val, str):
                        text_val = clean_size_tags(text_val)
                    d["text"] = text_val
                d["type"] = almanac_type_map.get(d.get("type"), d.get("type"))
                if orig_title in exact_strings:
                    d["title"] = exact_strings[orig_title]
                updated += 1
            data.m_Script = json.dumps(tree, ensure_ascii=False, indent=4)
            data.save()
            stats["patched_assets"].append({"name": name, "details_updated": updated})

        elif name == "PlantEvolutionData":
            data = obj.read()
            tree = json.loads(data.m_Script)
            updated = 0
            for item in tree.get("plants", []):
                val = item.get("value", {})
                for r in val.get("routes", []):
                    rn = r.get("routeName")
                    if rn in exact_strings:
                        r["routeName"] = exact_strings[rn]
                        updated += 1
            data.m_Script = json.dumps(tree, ensure_ascii=False, indent=4)
            data.save()
            stats["patched_assets"].append({"name": name, "routes_updated": updated})

        elif name == "ShootingAlmanacIndex":
            data = obj.read()
            tree = json.loads(data.m_Script)
            updated_entries = 0
            for e in tree.get("entries", []):
                for field in ("title", "description", "condition", "group"):
                    val = e.get(field)
                    if not val:
                        continue
                    if val in exact_strings:
                        e[field] = exact_strings[val]
                    elif CJK_RE.search(val):
                        for regex, repl in compiled_regexs:
                            m = regex.search(val)
                            if m:
                                try:
                                    e[field] = render_regex_template(repl, m, exact_strings)
                                    break
                                except Exception:
                                    pass
                updated_entries += 1

            for p in tree.get("plants", []):
                for b in p.get("buffs", []):
                    desc = b.get("descriptionOverride")
                    if not desc:
                        continue
                    if desc in exact_strings:
                        b["descriptionOverride"] = exact_strings[desc]
                    elif CJK_RE.search(desc):
                        for regex, repl in compiled_regexs:
                            m = regex.search(desc)
                            if m:
                                try:
                                    b["descriptionOverride"] = render_regex_template(repl, m, exact_strings)
                                    break
                                except Exception:
                                    pass
            data.m_Script = json.dumps(tree, ensure_ascii=False, indent=4)
            data.save()
            stats["patched_assets"].append({"name": name, "entries_updated": updated_entries})

        elif name == "Goods":
            data = obj.read()
            tree = json.loads(data.m_Script.lstrip("\ufeff"))
            updated = 0
            for item in tree.get("datas", []):
                desc = item.get("description")
                if desc in exact_strings:
                    item["description"] = exact_strings[desc]
                    updated += 1
            data.m_Script = json.dumps(tree, ensure_ascii=False, indent=4)
            data.save()
            stats["patched_assets"].append({"name": name, "goods_updated": updated})

        elif name == "TalentData":
            data = obj.read()
            tree = json.loads(data.m_Script.lstrip("\ufeff"))
            updated = 0
            for t in tree.get("talentDatas", []):
                if t.get("name") in exact_strings:
                    t["name"] = exact_strings[t["name"]]
                if t.get("description") in exact_strings:
                    t["description"] = exact_strings[t["description"]]
                updated += 1
            data.m_Script = json.dumps(tree, ensure_ascii=False, indent=4)
            data.save()
            stats["patched_assets"].append({"name": name, "talents_updated": updated})

        elif name == "LevelCreatorHelp":
            help_trans_path = almanac_dir / "LevelCreatorHelpTranslate.json"
            if help_trans_path.is_file():
                data = obj.read()
                with help_trans_path.open("r", encoding="utf-8") as f:
                    data.m_Script = json.dumps(json.load(f), ensure_ascii=False, indent=2)
                data.save()
                stats["patched_assets"].append({"name": name, "help_topics_updated": 11})

        else:
            orig_name = name
            is_renamed = False
            new_name = custom_iz_level_map.get(orig_name, orig_name)
            if new_name != orig_name:
                is_renamed = True

            tip_trans = (
                tips_iz.get(orig_name)
                or tips_iz.get(new_name)
                or tips_fs.get(orig_name)
                or tips_fs.get(new_name)
            )

            data = None
            modified = False
            if is_renamed:
                data = obj.read()
                data.m_Name = new_name
                modified = True
                stats["patched_assets"].append({"name": orig_name, "renamed_to": new_name})

            try:
                if data is None:
                    data = obj.read()
                tree = json.loads(data.m_Script)
                if isinstance(tree, dict) and "tips" in tree and tree["tips"]:
                    tip_val = tree["tips"]
                    if not tip_trans and isinstance(tip_val, str) and CJK_RE.search(tip_val):
                        for regex, repl in compiled_regexs:
                            m = regex.search(tip_val)
                            if m:
                                try:
                                    tip_trans = render_regex_template(repl, m, exact_strings)
                                    break
                                except Exception:
                                    pass
                    if tip_trans and tip_trans != tip_val:
                        tree["tips"] = tip_trans
                        data.m_Script = json.dumps(tree, ensure_ascii=False)
                        modified = True
                        stats["tips_updated"] = stats.get("tips_updated", 0) + 1
            except Exception:
                pass

            if modified and data is not None:
                data.save()

    # Update ResourceManager container for renamed CustomIZ assets
    for obj in env.objects:
        if obj.type.name == "ResourceManager":
            rm = obj.read()
            existing_keys = {k for k, _ in rm.m_Container}
            new_entries = []
            for k, v in rm.m_Container:
                for old_name, new_name in custom_iz_level_map.items():
                    old_suffix = old_name.lower()
                    if k.lower().endswith(old_suffix):
                        prefix = k[: -len(old_suffix)]
                        new_k = prefix + new_name.lower()
                        if new_k not in existing_keys:
                            new_entries.append((new_k, v))
                            existing_keys.add(new_k)
            if new_entries:
                rm.m_Container.extend(new_entries)
                rm.save()
                stats["resource_manager_entries_added"] = len(new_entries)
                print(f"Added {len(new_entries)} ResourceManager entries for CustomIZ levels")
            break

    return stats


def patch_ui_strings(
    env: UnityPy.Environment,
    data_dir: Path,
    platform: str = "pc",
) -> dict[str, Any]:
    stats = {
        "exact_matches": 0,
        "regex_matches": 0,
        "backing_fields": 0,
        "total_cjk_seen": 0,
    }

    strings_dir = data_dir / "Strings"
    dumps_dir = data_dir / "Dumps"
    almanac_dir = data_dir / "Almanac"

    exact_map = {}
    with (strings_dir / "translation_strings.json").open("r", encoding="utf-8") as f:
        exact_map.update(json.load(f))

    # Add plant and zombie names to UI exact map
    if (dumps_dir / "LawnStrings.json").exists() and (almanac_dir / "LawnStringsTranslate.json").exists():
        with (dumps_dir / "LawnStrings.json").open("r", encoding="utf-8") as f:
            d_lawn = json.load(f)
        with (almanac_dir / "LawnStringsTranslate.json").open("r", encoding="utf-8") as f:
            t_lawn = json.load(f)
        trans_plants = {p["seedType"]: p for p in t_lawn.get("plants", []) if "seedType" in p}
        for d in d_lawn.get("plants", []):
            t = trans_plants.get(d.get("seedType"))
            if t:
                cn, en = d.get("name"), t.get("name")
                if cn and en and cn not in exact_map:
                    exact_map[cn] = en

    if (dumps_dir / "ZombieStrings.json").exists() and (almanac_dir / "ZombieStringsTranslate.json").exists():
        with (dumps_dir / "ZombieStrings.json").open("r", encoding="utf-8") as f:
            d_zomb = json.load(f)
        with (almanac_dir / "ZombieStringsTranslate.json").open("r", encoding="utf-8") as f:
            t_zomb = json.load(f)
        trans_zomb = {z["theZombieType"]: z for z in t_zomb.get("zombies", []) if "theZombieType" in z}
        for d in d_zomb.get("zombies", []):
            t = trans_zomb.get(d.get("theZombieType"))
            if t:
                cn, en = d.get("name"), t.get("name")
                if cn and en and cn not in exact_map:
                    exact_map[cn] = en

    backing_file = strings_dir / "runtime_backing_strings.json"
    runtime_backing = json.load(backing_file.open("r", encoding="utf-8")) if backing_file.is_file() else {}

    for fname in ["customlevel_strings.json", "abyss_buffs.json", "travel_buffs.json"]:
        extra_path = strings_dir / fname
        if extra_path.is_file():
            try:
                extra_data = json.loads(extra_path.read_text(encoding="utf-8"))
                if isinstance(extra_data, dict):
                    exact_map.update({k: v for k, v in extra_data.items() if isinstance(v, str)})
            except Exception:
                pass

    regex_map = {}
    with (strings_dir / "translation_regexs.json").open("r", encoding="utf-8") as f:
        regex_map.update(json.load(f))
    if (strings_dir / "customlevel_regexs.json").is_file():
        with (strings_dir / "customlevel_regexs.json").open("r", encoding="utf-8") as f:
            regex_map.update(json.load(f))

    compiled_regexs = []
    for pat, repl in regex_map.items():
        try:
            compiled_regexs.append((re.compile(pat), repl))
        except Exception:
            pass

    tmp_script_ids, ui_text_script_ids = discover_ui_script_ids(env)
    print(f"Discovered UI script IDs: TMP={tmp_script_ids}, UI.Text={ui_text_script_ids}")

    for obj in env.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        raw = bytes(obj.get_raw_data())
        if len(raw) < 28:
            continue
        try:
            _file_id, script_path_id = struct.unpack_from("<iq", raw, 16)
        except Exception:
            continue

        if script_path_id in tmp_script_ids:
            parsed = read_tmp_text(raw)
            is_ui_text = False
        elif script_path_id in ui_text_script_ids:
            parsed = read_ui_text(raw, ui_text_script_ids)
            is_ui_text = True
        else:
            continue

        if parsed is None:
            continue

        text, _end = parsed
        new_raw = raw
        text_modified = False

        if CJK_RE.search(text):
            stats["total_cjk_seen"] += 1
            if is_ui_text:
                replacer = lambda r, v: replace_ui_text(r, v, ui_text_script_ids)
            else:
                replacer = replace_tmp_text
            if text in exact_map:
                val = exact_map[text]
                if platform == "pc" or is_ui_text:
                    val = clean_size_tags(val)
                new_raw = replacer(new_raw, val)
                stats["exact_matches"] += 1
                text_modified = True
            else:
                for regex, repl in compiled_regexs:
                    m = regex.search(text)
                    if m:
                        try:
                            translated_text = render_regex_template(repl, m, exact_map)
                            if platform == "pc" or is_ui_text:
                                translated_text = clean_size_tags(translated_text)
                            new_raw = replacer(new_raw, translated_text)
                            stats["regex_matches"] += 1
                            text_modified = True
                            break
                        except Exception:
                            pass

        backing_res = replace_runtime_backing_text(new_raw, runtime_backing)
        if backing_res is not None:
            new_raw, _s, _t = backing_res
            stats["backing_fields"] += 1
            text_modified = True

        if text_modified:
            obj.set_raw_data(new_raw)

    game_object_name_map = {
        name: exact_map[name] for name in ("铅笔", "橡皮") if name in exact_map
    }
    for obj in env.objects:
        if obj.type.name == "GameObject":
            try:
                data = obj.read()
                if data.m_Name in game_object_name_map:
                    data.m_Name = game_object_name_map[data.m_Name]
                    data.save()
            except Exception:
                pass

    return stats


def patch_fonts(
    env: UnityPy.Environment,
    data_dir: Path,
) -> dict[str, Any]:
    stats = {"fonts_replaced": []}
    ttf_path = data_dir / "Fonts" / "English.ttf"
    if not ttf_path.is_file():
        print(f"Warning: font file {ttf_path} not found. Skipping font payload injection.")
        return stats

    ttf_data = ttf_path.read_bytes()
    for obj in env.objects:
        if obj.type.name == "Font":
            data = obj.read()
            name = data.m_Name
            if name in ("fzcq", "fzjz", "汉仪夏日体W"):
                data.m_FontData = ttf_data
                obj.save_typetree(data)
                stats["fonts_replaced"].append(
                    {"name": name, "path_id": obj.path_id, "size": len(ttf_data)}
                )

    return stats


def patch_textures(
    env: UnityPy.Environment,
    data_dir: Path,
) -> dict[str, Any]:
    stats = {"textures_replaced": []}
    textures_dir = data_dir / "Textures"
    if not textures_dir.is_dir():
        return stats

    texture_files: dict[str, Path] = {}
    for ext in ("*.png", "*.jpg"):
        for p in textures_dir.rglob(ext):
            texture_files[p.stem] = p

    for obj in env.objects:
        if obj.type.name != "Texture2D":
            continue
        name = obj.peek_name()
        if name in texture_files:
            file_path = texture_files[name]
            try:
                img = Image.open(file_path).convert("RGBA")
                data = obj.read()
                data.image = img
                data.save()
                stats["textures_replaced"].append(
                    {"name": name, "size": list(img.size), "source": str(file_path.name)}
                )
            except Exception as e:
                print(f"Warning: failed to patch texture {name}: {e}")

    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-bundle", required=True, type=Path)
    parser.add_argument("--data-dir", default=Path("translation-data"), type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--platform", choices=("pc", "android"), default="pc")
    parser.add_argument("--packer", choices=("original", "lz4", "none"), default="lz4")
    args = parser.parse_args()

    start_time = time.time()
    print(f"Loading bundle {args.base_bundle}...")
    env = UnityPy.load(str(args.base_bundle))

    print(f"Patching TextAssets for {args.platform}...")
    text_stats = patch_text_assets(env, args.data_dir, args.platform)

    print("Patching serialized TextMesh Pro UI strings (with 1-based regex formatting)...")
    ui_stats = patch_ui_strings(env, args.data_dir, args.platform)

    print("Patching Fonts (English.ttf)...")
    font_stats = patch_fonts(env, args.data_dir)

    print("Patching textures...")
    tex_stats = patch_textures(env, args.data_dir)

    print(f"Saving output bundle to {args.output} (packer={args.packer})...")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temp_output = args.output.with_suffix(".tmp")
    with temp_output.open("wb") as out_f:
        out_f.write(env.file.save(packer=args.packer))
    if temp_output.exists():
        temp_output.replace(args.output)

    duration = time.time() - start_time
    report = {
        "base_bundle": str(args.base_bundle),
        "output_bundle": str(args.output),
        "platform": args.platform,
        "duration_seconds": round(duration, 2),
        "text_asset_stats": text_stats,
        "ui_stats": ui_stats,
        "font_stats": font_stats,
        "texture_stats": tex_stats,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Build complete in {duration:.2f}s! Report written to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
