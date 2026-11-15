#!/usr/bin/env python3
"""PvZ Fusion Custom Level Converter (CLI)

Translates PvZ Fusion Custom Level JSON files between Chinese and English port
and node definitions so custom levels load and connect seamlessly in either version.

Features:
- Full bidirectional conversion (Chinese -> English or English -> Chinese).
- Recursively handles event graphs, connection lines, input defaults, and
  Unity [SerializeReference] polymorphic nodes (references.RefIds).
- Self-contained standalone tool: loads adjacent or repo mappings with embedded fallback.
- Supports single files, whole directories, and in-place overwriting with backup.

Usage:
  python convert_custom_level.py level.json
  python convert_custom_level.py -i level.json -o level_en.json
  python convert_custom_level.py my_levels/ --in-place --backup
  python convert_custom_level.py level_en.json --direction en2cn
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def find_map_file(custom_path: Path | None = None) -> Path | None:
    """Find eventnode_port_map.json across standard search paths."""
    if custom_path and custom_path.is_file():
        return custom_path

    search_dirs = [
        Path(__file__).resolve().parent,
        Path(__file__).resolve().parent.parent.parent / "translation-data" / "Strings",
        Path.cwd(),
        Path.cwd() / "translation-data" / "Strings",
    ]
    for d in search_dirs:
        candidate = d / "eventnode_port_map.json"
        if candidate.is_file():
            return candidate
    return None


def load_mappings(map_file: Path | None = None) -> tuple[dict[str, str], dict[str, str]]:
    """Load bidirectional port mappings from JSON file with standard fallbacks."""
    resolved_file = find_map_file(map_file)
    if resolved_file and resolved_file.is_file():
        try:
            with open(resolved_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            ports = data.get("ports", {})
            cn2en = ports.get("cn_to_en", {})
            en2cn = ports.get("en_to_cn", {})
            if cn2en:
                return cn2en, en2cn
        except Exception as e:
            print(f"[Warning] Failed to read {resolved_file}: {e}", file=sys.stderr)

    # Core embedded fallback dictionary (essential port mappings)
    cn2en_fallback = {
        "触发": "Trigger", "执行": "Execute", "完成": "On Complete", "创建完成": "On Complete",
        "失败": "Failed", "失败原因": "Failure Reason", "成功": "Success", "创建成功": "On Success",
        "创建失败": "On Failed", "真": "True", "假": "False", "真（触发）": "True (Trigger)",
        "假（停止）": "False (Stop)", "循环体": "Loop Body", "循环结束": "Loop End",
        "输出": "Output", "输入": "Input", "条件": "Condition", "结果": "Result",
        "列表": "List", "列表1": "List 1", "列表2": "List 2", "索引": "Index",
        "当前索引": "Current Index", "元素": "Element", "数量": "Count", "长度": "Length",
        "对象": "Object", "变量": "Variable", "变量名": "Variable Name", "值": "Value",
        "数值": "Value", "值A": "Value A", "值B": "Value B", "新值": "New Value",
        "初始值": "Initial Value", "当前值": "Current Value", "目标值": "Target Value",
        "行": "Row", "列": "Column", "列（小数）": "Column (Decimal)", "目标行": "Target Row",
        "目标列": "Target Column", "目标列（小数）": "Target Column (Decimal)", "位置": "Position",
        "坐标": "Coordinates", "X": "X", "Y": "Y", "Z": "Z", "速度": "Speed", "角度": "Angle",
        "缩放": "Scale", "大小": "Scale", "距离": "Distance", "植物": "Plant", "植物类型": "Plant Type",
        "目标植物": "Target Plant", "当前植物": "Current Plant", "僵尸": "Zombie", "僵尸类型": "Zombie Type",
        "目标僵尸": "Target Zombie", "当前僵尸": "Current Zombie", "卡牌": "Card", "卡牌对象": "Card Object",
        "子弹": "Bullet", "子弹类型": "Bullet Type", "伤害": "Damage", "伤害值": "Damage Amount",
        "血量": "Health", "回血量": "Heal Amount", "阳光": "Sun", "阳光数量": "Sun Amount",
        "金币": "Coins", "金币数量": "Coin Amount", "阳光不足": "Insufficient Sun",
        "金币不足": "Insufficient Coins", "标题": "Title", "文本": "Text", "描述": "Description",
        "名称": "Name", "名称或编号": "Name or ID", "选项列表": "Option List", "选项被点击": "Option Clicked",
        "合并列表": "Merge List", "未合并": "Unmerge", "重置": "Reset", "超时": "Timeout",
        "大于": "Greater than", "小于": "Less than", "等于": "Equal to", "不等于": "Not Equal to",
        "余数": "Remainder", "除数": "Divisor", "被除数": "Dividend", "和": "Sum", "积": "Product",
    }
    en2cn_fallback = {v: k for k, v in cn2en_fallback.items()}
    return cn2en_fallback, en2cn_fallback


class LevelConverter:
    def __init__(self, direction: str = "cn2en", map_file: Path | None = None):
        self.direction = direction
        cn2en, en2cn = load_mappings(map_file)
        self.mapping = cn2en if direction == "cn2en" else en2cn
        self.stats = {
            "files_processed": 0,
            "connections_converted": 0,
            "input_defaults_converted": 0,
            "fields_converted": 0,
            "unmapped_ports": set(),
        }

    def translate_port(self, port_name: str) -> str:
        if not isinstance(port_name, str) or not port_name:
            return port_name
        if port_name in self.mapping:
            return self.mapping[port_name]
        stripped = port_name.strip()
        if stripped in self.mapping:
            return self.mapping[stripped]
        self.stats["unmapped_ports"].add(port_name)
        return port_name

    def convert_connections(self, connections: Any) -> None:
        if not isinstance(connections, list):
            return
        for conn in connections:
            if isinstance(conn, dict):
                if "sourcePortName" in conn and isinstance(conn["sourcePortName"], str):
                    orig = conn["sourcePortName"]
                    trans = self.translate_port(orig)
                    if trans != orig:
                        conn["sourcePortName"] = trans
                        self.stats["connections_converted"] += 1
                if "targetPortName" in conn and isinstance(conn["targetPortName"], str):
                    orig = conn["targetPortName"]
                    trans = self.translate_port(orig)
                    if trans != orig:
                        conn["targetPortName"] = trans
                        self.stats["connections_converted"] += 1

    def convert_node_dict(self, node: dict[str, Any]) -> None:
        # Convert inputDefaults
        input_defs = node.get("inputDefaults")
        if isinstance(input_defs, list):
            for item in input_defs:
                if isinstance(item, dict) and "portName" in item and isinstance(item["portName"], str):
                    orig = item["portName"]
                    trans = self.translate_port(orig)
                    if trans != orig:
                        item["portName"] = trans
                        self.stats["input_defaults_converted"] += 1

        # Convert *_PortName fields
        for k, v in list(node.items()):
            if k.endswith("_PortName") and isinstance(v, str):
                trans = self.translate_port(v)
                if trans != v:
                    node[k] = trans
                    self.stats["fields_converted"] += 1

    def convert_graph(self, graph: dict[str, Any]) -> None:
        if "connections" in graph:
            self.convert_connections(graph.get("connections"))
        if "nodes" in graph and isinstance(graph["nodes"], list):
            for node in graph["nodes"]:
                if isinstance(node, dict):
                    self.convert_node_dict(node)

    def convert_references(self, refs: dict[str, Any]) -> None:
        ref_ids = refs.get("RefIds")
        if isinstance(ref_ids, list):
            for item in ref_ids:
                if isinstance(item, dict):
                    data = item.get("data")
                    if isinstance(data, dict):
                        self.convert_node_dict(data)

    def convert_payload(self, data: Any) -> Any:
        if isinstance(data, dict):
            # Check for event graph structures
            if "connections" in data and "nodes" in data:
                self.convert_graph(data)
            for k, v in list(data.items()):
                if k in ("eventNodeGraph", "eventGraph", "graph", "eventNodesGraph") and isinstance(v, dict):
                    self.convert_graph(v)
                elif k == "references" and isinstance(v, dict):
                    self.convert_references(v)
                elif isinstance(v, (dict, list)):
                    self.convert_payload(v)
        elif isinstance(data, list):
            for item in data:
                self.convert_payload(item)
        return data

    def convert_file(
        self,
        src: Path,
        dst: Path,
        dry_run: bool = False,
        backup: bool = False,
    ) -> bool:
        try:
            with open(src, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[Error] Failed reading {src}: {e}", file=sys.stderr)
            return False

        converted = self.convert_payload(data)

        if not dry_run:
            if backup and src.resolve() == dst.resolve():
                bak_path = src.with_suffix(src.suffix + ".bak")
                shutil.copy2(src, bak_path)

            dst.parent.mkdir(parents=True, exist_ok=True)
            with open(dst, "w", encoding="utf-8") as f:
                json.dump(converted, f, ensure_ascii=False, indent=2)

        self.stats["files_processed"] += 1
        return True


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="convert_custom_level",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        help="Input custom level JSON file or directory (or pass via -i / --input)",
    )
    parser.add_argument(
        "-i", "--input",
        type=Path,
        dest="input_path",
        help="Input custom level JSON file or directory",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        dest="output_path",
        help="Output JSON file or directory (defaults to *_en.json or in-place with -w)",
    )
    parser.add_argument(
        "-d", "--direction",
        choices=["cn2en", "en2cn"],
        default="cn2en",
        help="Conversion direction (default: cn2en)",
    )
    parser.add_argument(
        "-w", "--in-place",
        action="store_true",
        help="Overwrite input files in place",
    )
    parser.add_argument(
        "-b", "--backup",
        action="store_true",
        help="Create a .bak backup file before overwriting in-place",
    )
    parser.add_argument(
        "--map-file",
        type=Path,
        help="Custom path to eventnode_port_map.json",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Scan and test conversion without writing output files",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress per-file status messages",
    )

    args = parser.parse_args()
    input_path = args.input_path or args.target

    if not input_path:
        parser.print_help()
        return 1

    if not input_path.exists():
        print(f"[Error] Path does not exist: {input_path}", file=sys.stderr)
        return 1

    converter = LevelConverter(direction=args.direction, map_file=args.map_file)

    if input_path.is_file():
        if args.in_place:
            out_path = input_path
        elif args.output_path:
            out_path = args.output_path
        else:
            suffix = "_en.json" if args.direction == "cn2en" else "_cn.json"
            out_path = input_path.with_name(input_path.stem + suffix)

        if not args.quiet:
            print(f"Converting [{args.direction}]: {input_path} -> {out_path}")
        converter.convert_file(
            input_path,
            out_path,
            dry_run=args.dry_run,
            backup=args.backup,
        )
    else:
        out_dir = args.output_path or input_path
        files = sorted(list(input_path.rglob("*.json")))
        if not args.quiet:
            print(f"Scanning directory: {input_path} ({len(files)} JSON files found)")
        for f in files:
            if f.name.endswith(("_en.json", "_cn.json", ".bak")):
                continue
            rel = f.relative_to(input_path)
            target = f if args.in_place else (out_dir / rel)
            if not args.quiet:
                print(f"  -> {rel}")
            converter.convert_file(
                f,
                target,
                dry_run=args.dry_run,
                backup=args.backup,
            )

    print("\n" + "=" * 55)
    print("PvZ Fusion Custom Level Conversion Summary")
    print("=" * 55)
    print(f"Direction                : {args.direction}")
    print(f"Files Processed          : {converter.stats['files_processed']}")
    print(f"Connection Ports Updated : {converter.stats['connections_converted']}")
    print(f"Input Defaults Updated   : {converter.stats['input_defaults_converted']}")
    print(f"Node Port Fields Updated : {converter.stats['fields_converted']}")

    unmapped = sorted(list(converter.stats["unmapped_ports"]))
    if unmapped:
        print(f"\nUnmapped Ports ({len(unmapped)}):")
        for p in unmapped[:15]:
            print(f"  - {repr(p)}")
        if len(unmapped) > 15:
            print(f"  ... and {len(unmapped) - 15} more.")
    else:
        print("Unmapped Ports           : None (100% matched!)")
    print("=" * 55)

    return 0


if __name__ == "__main__":
    sys.exit(main())
