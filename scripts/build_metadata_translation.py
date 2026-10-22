#!/usr/bin/env python3
"""Build a deterministic translated IL2CPP global-metadata.dat.

The tool always starts from a clean metadata file, rebuilds the string-literal
database once at EOF, and rewrites the literal lookup table.  It deliberately
does not patch an already-patched output, preventing the repeated file growth
seen in older Android translation builds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


MAGIC = b"\xaf\x1b\xb1\xfa"
CJK_RE = re.compile(r"[\u3400-\u9fff]")
CSHARP_FORMAT_FIELD_RE = re.compile(r"\{(\d+)(?:,[^}:]+)?(?::[^}]+)?\}")
EXACT_FILES = ("translation_strings.json", "customlevel_strings.json", "abyss_buffs.json")
REGEX_FILES = ("translation_regexs.json", "customlevel_regexs.json")
STRUCTURED_PAIR_FILES = ("travel_buffs.json", "tips_fs.json", "tips_iz.json")

MODIFIER_CATEGORY_PREFIXES = ("祝福-", "诅咒-", "质变-")
SP_EVOLUTION_SOURCE_TITLE = "【SP进化】"
SP_EVOLUTION_TRANSLATED_TITLE = "[SP Evolution]"

# Rogue Shooting group names used by ShootingGroupBuff to construct ShootingBuffType enum names via Enum.Parse.
# These literals MUST NEVER be translated, otherwise Enum.Parse fails at runtime.
# In-level display overrides: The Gods: Evolved level titles are displayed on 2 lines on menu cards,
# but should be a single line in-game during the level.
METADATA_IN_LEVEL_OVERRIDES = {
    "诸神进化：炼狱": "The Gods: Evolved - Purgatory",
    "诸神进化：射击": "The Gods: Evolved - Shoot 'Em Up",
}

ROUGE_SHOOTING_GROUP_NAMES = frozenset({
    "业火", "交易", "光棱", "全能", "天罚", "宝藏",
    "战锤", "明月", "木桩", "烈阳", "硬化", "裂空",
})


def _load_json_data(rel_path: str):
    p = Path(__file__).resolve().parent.parent / "translation-data" / rel_path
    if p.is_file():
        with open(p, "r", encoding="utf-8") as f:
            import json
            return json.load(f)
    return {}

ANDROID_CONFIRMED_EXACT = _load_json_data("Strings/android_metadata_strings.json")
ANDROID_REQUIRED_OVERRIDE_SOURCES = set(_load_json_data("Strings/android_required_overrides.json"))
ANDROID_381_SYNERGY_ENUM_FIELDS = _load_json_data("Enums/SynergyType.json")
ANDROID_381_INVEST_ENUM_FIELDS = _load_json_data("Enums/InvestBuff.json")



@dataclass(frozen=True)
class MetadataLayout:
    lookup_offset: int
    lookup_size: int
    data_offset: int
    data_size: int


@dataclass(frozen=True)
class Literal:
    length: int
    offset: int
    raw: bytes
    text: str


@dataclass(frozen=True)
class DefinitionLayout:
    string_offset: int
    string_size: int
    field_offset: int
    field_size: int


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_metadata(data: bytes) -> tuple[MetadataLayout, list[Literal]]:
    if data[:4] != MAGIC:
        raise ValueError("not a supported IL2CPP global-metadata.dat")
    lookup_offset, lookup_size, data_offset, data_size = struct.unpack_from("<4I", data, 8)
    if lookup_size % 8:
        raise ValueError(f"literal lookup size is not divisible by 8: {lookup_size}")
    if lookup_offset + lookup_size > len(data) or data_offset > len(data):
        raise ValueError("literal table points outside the metadata file")

    literals: list[Literal] = []
    for index in range(lookup_size // 8):
        length, relative_offset = struct.unpack_from("<2I", data, lookup_offset + index * 8)
        start = data_offset + relative_offset
        end = start + length
        # Some existing fan patches append a larger translated database but
        # forget to update the header's data-size field.  Accept those files as
        # references as long as every entry remains inside the physical file.
        # Newly generated outputs always receive the correct size below.
        if end > len(data):
            raise ValueError(f"literal {index} points outside the metadata file")
        raw = data[start:end]
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"literal {index} is not valid UTF-8") from exc
        literals.append(Literal(length, relative_offset, raw, text))
    return MetadataLayout(lookup_offset, lookup_size, data_offset, data_size), literals


def parse_definition_layout(data: bytes) -> DefinitionLayout:
    magic, version = struct.unpack_from("<2I", data, 0)
    if magic != 0xFAB11BAF or version != 31:
        raise ValueError(
            f"unsupported IL2CPP metadata header for definition patch: "
            f"magic=0x{magic:08x}, version={version}"
        )
    # Metadata v31 header pairs used here:
    #   [6,7]   definition string heap offset/size
    #   [24,25] field definition table offset/size
    string_offset, string_size = struct.unpack_from("<2I", data, 24)
    field_offset, field_size = struct.unpack_from("<2I", data, 96)
    if string_offset + string_size > len(data):
        raise ValueError("definition string heap points outside the metadata file")
    if field_offset + field_size > len(data) or field_size % 12:
        raise ValueError("field definition table is invalid")
    return DefinitionLayout(string_offset, string_size, field_offset, field_size)


def read_definition_string(data: bytes, layout: DefinitionLayout, relative_offset: int) -> str:
    if not 0 <= relative_offset < layout.string_size:
        raise ValueError(f"definition string offset is out of range: {relative_offset}")
    start = layout.string_offset + relative_offset
    end = data.find(b"\0", start, layout.string_offset + layout.string_size)
    if end < 0:
        raise ValueError(f"unterminated definition string at offset {relative_offset}")
    return data[start:end].decode("utf-8")


def translate_validated_enum_fields(
    base: bytes,
    fields: dict[int, tuple[str, str]],
    label: str,
) -> tuple[bytes, list[dict[str, object]]]:
    """Rename validated display-facing enum fields without changing their values."""
    layout = parse_definition_layout(base)
    field_count = layout.field_size // 12
    output = bytearray(base)
    new_heap = bytearray(base[layout.string_offset : layout.string_offset + layout.string_size])
    changes: list[dict[str, object]] = []

    for field_index, (expected_source, translated) in fields.items():
        if field_index >= field_count:
            raise RuntimeError(
                f"{label} enum field {field_index} is outside the {field_count}-field table"
            )
        record_offset = layout.field_offset + field_index * 12
        original_name_offset = struct.unpack_from("<I", base, record_offset)[0]
        original_name = read_definition_string(base, layout, original_name_offset)
        if original_name != expected_source:
            raise RuntimeError(
                f"{label} enum validation failed at field {field_index}: "
                f"expected {expected_source!r}, found {original_name!r}"
            )
        translated_offset = len(new_heap)
        new_heap.extend(translated.encode("utf-8") + b"\0")
        struct.pack_into("<I", output, record_offset, translated_offset)
        changes.append(
            {
                "field_index": field_index,
                "source": original_name,
                "translation": translated,
                "numeric_value_unchanged": True,
            }
        )

    new_heap_offset = len(output)
    output.extend(new_heap)
    struct.pack_into("<2I", output, 24, new_heap_offset, len(new_heap))

    translated_layout = parse_definition_layout(output)
    for change in changes:
        record_offset = translated_layout.field_offset + int(change["field_index"]) * 12
        translated_offset = struct.unpack_from("<I", output, record_offset)[0]
        actual = read_definition_string(output, translated_layout, translated_offset)
        if actual != change["translation"]:
            raise RuntimeError(
                f"{label} enum round-trip validation failed at field {change['field_index']}"
            )
    return bytes(output), changes


def resolve_contiguous_enum_fields(
    data: bytes,
    expected_fields: dict[int, tuple[str, str]],
    label: str,
) -> dict[int, tuple[str, str]]:
    """Resolve a display enum by its complete ordered member-name sequence.

    The numeric keys in ``expected_fields`` document the original 3.8.1
    positions, but are not trusted for a different game build. Requiring one
    unique contiguous sequence avoids accidentally renaming an unrelated field
    that happens to share a short Chinese display name.
    """
    layout = parse_definition_layout(data)
    field_count = layout.field_size // 12
    if isinstance(expected_fields, dict):
        if expected_fields and isinstance(next(iter(expected_fields.values())), tuple):
            ordered = list(expected_fields.values())
        else:
            ordered = list(expected_fields.items())
    else:
        ordered = list(expected_fields)
    expected_names = [source for source, _translated in ordered]
    field_names = []
    for field_index in range(field_count):
        record_offset = layout.field_offset + field_index * 12
        name_offset = struct.unpack_from("<I", data, record_offset)[0]
        field_names.append(read_definition_string(data, layout, name_offset))

    starts = [
        start
        for start in range(field_count - len(expected_names) + 1)
        if field_names[start : start + len(expected_names)] == expected_names
    ]
    if len(starts) != 1:
        raise RuntimeError(
            f"{label} enum sequence resolution found {len(starts)} matches; "
            f"expected exactly one"
        )
    start = starts[0]
    return {
        start + offset: entry
        for offset, entry in enumerate(ordered)
    }


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def aligned_string_pairs(source: object, translated: object) -> Iterable[tuple[str, str]]:
    if isinstance(source, str) and isinstance(translated, str):
        yield source, translated
    elif isinstance(source, dict) and isinstance(translated, dict):
        for key, value in source.items():
            if key in translated:
                yield from aligned_string_pairs(value, translated[key])
    elif isinstance(source, list) and isinstance(translated, list):
        for source_item, translated_item in zip(source, translated):
            yield from aligned_string_pairs(source_item, translated_item)


def clean_modifier_source_title(source: str) -> str:
    """Return the unformatted Chinese title before the runtime delimiter."""
    title = re.split(r"[:：]", source, maxsplit=1)[0]
    return re.sub(r"<[^>]+>", "", title).strip()


def find_dumps_dir(strings_dir: Path) -> Path:
    for parent in strings_dir.parents:
        candidate = parent / "Dumps"
        if candidate.is_dir():
            return candidate
    return strings_dir.parents[2] / "Dumps"


def load_modifier_sources(
    strings_dir: Path,
) -> tuple[set[str], dict[str, str], dict[str, str], dict[str, list[str]]]:
    """Return modifier sources plus source-title and exact-record title maps."""
    sources: set[str] = set()
    title_translations: dict[str, str] = {}
    exact_title_translations: dict[str, str] = {}
    ambiguous_title_translations: dict[str, set[str]] = {}
    dumps_dir = find_dumps_dir(strings_dir)
    source_path = dumps_dir / "travel_buffs.json"
    translated_path = strings_dir / "travel_buffs.json"
    if not source_path.exists():
        raise FileNotFoundError(f"missing travel modifier source dump: {source_path}")
    if not translated_path.exists():
        raise FileNotFoundError(f"missing travel modifier translation: {translated_path}")
    source_payload = read_json(source_path)
    translated_payload = read_json(translated_path)
    for section, records in source_payload.items():
        if section == "investmentBuffs" or not isinstance(records, dict):
            continue
        translated_records = translated_payload.get(section, {})
        for record_id, record in records.items():
            if not isinstance(record, dict):
                continue
            description = record.get("desc")
            translated_record = translated_records.get(record_id, {})
            if isinstance(description, str) and ("：" in description or ":" in description):
                sources.add(description)
                translated_name = translated_record.get("name")
                if isinstance(translated_name, str) and translated_name:
                    source_title = clean_modifier_source_title(description)
                    prior_title = title_translations.get(source_title)
                    if prior_title is not None and prior_title != translated_name:
                        ambiguous_title_translations.setdefault(
                            source_title, {prior_title}
                        ).add(translated_name)
                        title_translations.pop(source_title, None)
                    elif source_title not in ambiguous_title_translations:
                        title_translations[source_title] = translated_name
                    exact_title_translations[description] = translated_name

    # Android 3.9 revises some bodies without updating the PC source dump.
    # Accept those exact fallbacks only when their parsed title agrees with the
    # PC record, or when the title is a reviewed 3.9-only modifier title.
    android_confirmed_path = strings_dir / "android_metadata_strings.json"
    android_confirmed = read_json(android_confirmed_path) if android_confirmed_path.is_file() else {}
    titles_file = strings_dir / "android_modifier_titles.json"
    if titles_file.is_file():
        titles_info = read_json(titles_file)
        android_39_titles = set(titles_info.get("titles", []))
        android_39_translations = titles_info.get("translations", {})
    else:
        android_39_titles = set()
        android_39_translations = {}

    for source, target in android_confirmed.items():
        if "：" not in source or ": " not in target:
            continue
        source_title = source.split("：", 1)[0]
        translated_title = target.split(": ", 1)[0]
        if (
            title_translations.get(source_title) == translated_title
            or source_title in android_39_titles
            or source_title.startswith("祝福-")
            or source_title.startswith("诅咒-")
            or source_title.startswith("质变-")
        ):
            sources.add(source)
    for source_title, translated_title in android_39_translations.items():
        if source_title not in ambiguous_title_translations:
            title_translations.setdefault(source_title, translated_title)
    title_translations[SP_EVOLUTION_SOURCE_TITLE] = SP_EVOLUTION_TRANSLATED_TITLE
    for source in sources:
        source_title = clean_modifier_source_title(source)
        if source_title in title_translations:
            exact_title_translations.setdefault(source, title_translations[source_title])
    return (
        sources,
        title_translations,
        exact_title_translations,
        {
            source_title: sorted(translated_titles)
            for source_title, translated_titles in sorted(
                ambiguous_title_translations.items()
            )
        },
        android_39_titles,
    )


def modifier_source_reason(
    source: str,
    exact_sources: set[str],
    reviewed_titles: set[str] | None = None,
) -> str | None:
    """Classify combined modifier strings without matching unrelated task text."""
    if source in exact_sources:
        return "exact_pc_or_reviewed_source"
    if "：" not in source and ":" not in source:
        return None
    source_title = clean_modifier_source_title(source)
    if source_title == SP_EVOLUTION_SOURCE_TITLE:
        return "sp_evolution"
    if source_title.startswith(MODIFIER_CATEGORY_PREFIXES):
        return "category_prefix"
    if reviewed_titles is not None and source_title in reviewed_titles:
        return "reviewed_android_title"
    return None


def normalize_modifier_translation(
    translated: str,
    preferred_title: str | None = None,
    source: str | None = None,
) -> tuple[str, bool]:
    """Preserve the runtime delimiter while matching source newline convention."""
    delimiter_index = translated.find("：")
    delimiter_length = 1
    if delimiter_index < 0:
        delimiter_index = translated.find(":")
    if delimiter_index < 0:
        raise ValueError(f"modifier translation has no title delimiter: {translated!r}")
    title = translated[:delimiter_index]
    body = translated[delimiter_index + delimiter_length:]
    title = re.sub(r"</?(?:nobr|size)(?:=[^>]+)?>", "", title.strip())
    title = re.sub(r"<[^>]+>", "", title).strip()
    if preferred_title:
        title = preferred_title.strip().rstrip(":：").strip()
    body = body.lstrip("\r\n ")
    title_variants = {title}
    for separator in (": ", " - "):
        if separator in title:
            title_variants.add(title.rsplit(separator, 1)[-1].strip())
    for title_variant in sorted(title_variants, key=len, reverse=True):
        redundant_heading = re.match(
            rf"^{re.escape(title_variant)}\s*[:：]\s*",
            body,
            flags=re.IGNORECASE,
        )
        if redundant_heading is not None:
            body = body[redundant_heading.end():].lstrip("\r\n ")
            break
    if not title or not body:
        raise ValueError(f"modifier translation has an empty title or body: {translated!r}")
    shrink_title = len(title) > 24
    title_markup = f"<nobr>{title}</nobr>"
    if shrink_title:
        title_markup = f"<size=80%>{title_markup}</size>"
    had_newline = source is not None and ("：\n" in source or ":\n" in source)
    delim = "：\n" if had_newline else "："
    return f"{title_markup}{delim}{body}", shrink_title


def load_pc_translations(
    strings_dir: Path,
) -> tuple[
    dict[str, str],
    set[str],
    list[tuple[str, str, re.Pattern[str], str]],
    dict[str, int],
]:
    exact: dict[str, str] = {}
    regex_entries: list[tuple[str, str, re.Pattern[str], str]] = []
    counts: dict[str, int] = {}

    for filename in EXACT_FILES:
        path = strings_dir / filename
        if not path.exists():
            continue
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise ValueError(f"{path} must contain a JSON object")
        added = 0
        for source, translated in payload.items():
            if (
                isinstance(source, str)
                and isinstance(translated, str)
                and CJK_RE.search(source)
                and not source.startswith("-------")
            ):
                exact[source] = translated
                added += 1
        counts[filename] = added

    dumps_dir = find_dumps_dir(strings_dir)
    for filename in STRUCTURED_PAIR_FILES:
        source_path = dumps_dir / filename
        translated_path = strings_dir / filename
        if not source_path.exists() or not translated_path.exists():
            continue
        source_payload = read_json(source_path)
        translated_payload = read_json(translated_path)
        added = 0
        for source, translated in aligned_string_pairs(source_payload, translated_payload):
            if CJK_RE.search(source) and translated and source != translated and source not in exact:
                exact[source] = translated
                added += 1
        if filename == "travel_buffs.json":
            # Android stores each modifier as one combined string and derives
            # its short card/title label from the text before the full-width
            # colon. Keep that first line solely as title metadata; the Unity
            # layout pass clips it above the description viewport so players
            # see only the larger description body below the separate title.
            for section, source_records in source_payload.items():
                translated_records = translated_payload.get(section)
                if not isinstance(source_records, dict) or not isinstance(translated_records, dict):
                    continue
                for record_id, source_record in source_records.items():
                    translated_record = translated_records.get(record_id)
                    if not isinstance(source_record, dict) or not isinstance(translated_record, dict):
                        continue
                    source_desc = source_record.get("desc")
                    translated_name = translated_record.get("name")
                    translated_desc = translated_record.get("desc")
                    if not all(isinstance(value, str) and value for value in (
                        source_desc, translated_name, translated_desc
                    )):
                        continue
                    if CJK_RE.search(source_desc):
                        exact[source_desc] = f"{translated_name}：\n{translated_desc}"
                        added += 1
        counts[f"structured:{filename}"] = added

    for filename in REGEX_FILES:
        path = strings_dir / filename
        if not path.exists():
            continue
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise ValueError(f"{path} must contain a JSON object")
        added = 0
        for pattern, translated in payload.items():
            if not isinstance(pattern, str) or not isinstance(translated, str):
                continue
            compiled = re.compile(pattern, re.DOTALL)
            cjk_runs = re.findall(r"[\u3400-\u9fff]+", pattern)
            anchor = max(cjk_runs, key=len) if cjk_runs else ""
            regex_entries.append((pattern, translated, compiled, anchor))
            added += 1
        counts[filename] = added

    # Capture provenance before Android-specific overrides and fallbacks are
    # merged. New 3.9 content may use current PC English only; this set lets
    # the final selection policy distinguish community translations from
    # older Android or hand-written fallback text.
    pc_exact_sources = set(exact)

    android_confirmed_path = strings_dir / "android_metadata_strings.json"
    android_confirmed = read_json(android_confirmed_path) if android_confirmed_path.is_file() else {}
    overrides_file = strings_dir / "android_required_overrides.json"
    android_overrides = set(read_json(overrides_file)) if overrides_file.is_file() else set()

    fallback_added = 0
    community_preferred = 0
    for source, target in android_confirmed.items():
        if source in android_overrides:
            exact[source] = target
        elif source in exact:
            community_preferred += 1
        else:
            exact[source] = target
            fallback_added += 1
    counts["android_confirmed_exact"] = len(android_confirmed)
    counts["android_required_overrides"] = len(android_overrides)
    counts["android_fallbacks_added"] = fallback_added
    counts["android_fallbacks_superseded_by_pc"] = community_preferred

    return exact, pc_exact_sources, regex_entries, counts, android_overrides


def observed_translations(
    label: str, base_path: Path, translated_path: Path
) -> tuple[dict[str, str], dict[str, object]]:
    base_data = base_path.read_bytes()
    translated_data = translated_path.read_bytes()
    _, base_literals = parse_metadata(base_data)
    _, translated_literals = parse_metadata(translated_data)
    if len(base_literals) != len(translated_literals):
        raise ValueError(
            f"reference pair {label!r} has different literal counts: "
            f"{len(base_literals)} vs {len(translated_literals)}"
        )

    mapping: dict[str, str] = {}
    conflicts = 0
    changed = 0
    accepted = 0
    for source, target in zip(base_literals, translated_literals):
        if source.raw == target.raw:
            continue
        changed += 1
        if not CJK_RE.search(source.text) or CJK_RE.search(target.text) or not target.text:
            continue
        previous = mapping.get(source.text)
        if previous is not None and previous != target.text:
            conflicts += 1
            continue
        mapping[source.text] = target.text
        accepted += 1

    stats = {
        "label": label,
        "base": str(base_path.resolve()),
        "translated": str(translated_path.resolve()),
        "changed_literal_occurrences": changed,
        "accepted_occurrences": accepted,
        "unique_mappings": len(mapping),
        "conflicts": conflicts,
    }
    return mapping, stats


def observed_translations_report(
    label: str, report_path: Path
) -> tuple[dict[str, str], dict[str, object]]:
    """Load previously validated exact Android mappings from a build report.

    This is the safe migration path when the original aligned APK pair is not
    available locally.  A mapping is accepted only when the old report records
    a Chinese source, a non-empty non-Chinese translation, and one unambiguous
    translation for that exact source string.
    """
    payload = read_json(report_path)
    if not isinstance(payload, dict) or not isinstance(payload.get("changes"), list):
        raise ValueError(f"reference report {label!r} has no changes list: {report_path}")

    choices: dict[str, set[str]] = {}
    accepted_occurrences = 0
    for change in payload["changes"]:
        if not isinstance(change, dict):
            continue
        source = change.get("source")
        target = change.get("translation")
        if (
            not isinstance(source, str)
            or not isinstance(target, str)
            or not target
            or not CJK_RE.search(source)
            or CJK_RE.search(target)
            or source == target
        ):
            continue
        choices.setdefault(source, set()).add(target)
        accepted_occurrences += 1

    conflicts = {source: values for source, values in choices.items() if len(values) != 1}
    mapping = {
        source: next(iter(values))
        for source, values in choices.items()
        if len(values) == 1
    }
    stats = {
        "label": label,
        "report": str(report_path.resolve()),
        "accepted_occurrences": accepted_occurrences,
        "unique_mappings": len(mapping),
        "conflicts": len(conflicts),
    }
    return mapping, stats


def csharp_format(template: str, values: Iterable[str]) -> str:
    values_list = list(values)
    open_token = "\0OPEN_BRACE\0"
    close_token = "\0CLOSE_BRACE\0"
    protected = template.replace("{{", open_token).replace("}}", close_token)
    has_zero = bool(re.search(r"\{0\}", protected))

    def replace(match: re.Match[str]) -> str:
        index = int(match.group(1))
        actual_index = index if has_zero else (index - 1)
        return values_list[actual_index] if 0 <= actual_index < len(values_list) else match.group(0)

    protected = re.sub(r"\{(\d+)(?:,[^}:]+)?(?::[^}]+)?\}", replace, protected)
    return protected.replace(open_token, "{").replace(close_token, "}")


def translate_csharp_template_with_pc_regex(
    text: str,
    regex_entries: list[tuple[str, str, re.Pattern[str], str]],
) -> str | None:
    """Bridge PC runtime regexes to Android's compiled C# format strings.

    The PC translator sees the final rendered text, such as
    ``保存成功，编号：0``, while IL2CPP metadata contains the pre-rendered
    template ``保存成功，编号：{0}``.  Substitute unique numeric sentinels,
    require a whole-string PC regex match, render the community translation,
    and then restore the original C# placeholders (including format specifiers
    such as ``:F0`` and ``:D2``).

    Only a single unambiguous, fully English result is accepted.  Partial
    matches are deliberately rejected so a small regex such as ``第(\\d+)页``
    cannot discard the rest of a longer Android diagnostic or UI message.
    """

    fields = list(CSHARP_FORMAT_FIELD_RE.finditer(text))
    if not fields:
        return None

    original_fields: dict[int, str] = {}
    sentinels: dict[int, str] = {}
    for field in fields:
        index = int(field.group(1))
        original = field.group(0)
        previous = original_fields.get(index)
        if previous is not None and previous != original:
            # One argument rendered with different format specifiers cannot be
            # restored safely after a regex has rearranged its capture groups.
            return None
        original_fields[index] = original
        sentinels[index] = f"927401{index:03d}683"

    sample = CSHARP_FORMAT_FIELD_RE.sub(
        lambda match: sentinels[int(match.group(1))], text
    )
    candidates: set[str] = set()
    for _pattern, template, compiled, anchor in regex_entries:
        if anchor and anchor not in sample:
            continue
        match = compiled.search(sample)
        if match is None or match.span() != (0, len(sample)):
            continue
        rendered = csharp_format(template, match.groups())
        for index, sentinel in sentinels.items():
            rendered = rendered.replace(sentinel, original_fields[index])
        if rendered != text and not CJK_RE.search(rendered):
            candidates.add(rendered)

    if len(candidates) == 1:
        return candidates.pop()
    return None


def translate_literal(
    text: str,
    exact: dict[str, str],
    pc_exact_sources: set[str],
    observed: dict[str, tuple[str, str]],
    regex_entries: list[tuple[str, str, re.Pattern[str], str]],
    required_overrides: set[str] | None = None,
) -> tuple[str, str | None]:
    def resolve_chain(value: str) -> str:
        """Resolve exact/reference outputs that are themselves source keys.

        PC regex rules sometimes normalize an Android string into a second,
        mixed-language source key. Keep resolving while CJK remains so the
        final exact community translation is not stranded halfway through.
        """
        seen = {value}
        for _ in range(8):
            if not CJK_RE.search(value):
                break
            if value in exact:
                next_value = exact[value]
            elif value in observed:
                next_value = observed[value][0]
            else:
                break
            if next_value == value or next_value in seen:
                break
            value = next_value
            seen.add(value)
        return value

    if not CJK_RE.search(text):
        return text, None
    if text in exact:
        method = (
            "pc_exact"
            if text in pc_exact_sources and (required_overrides is None or text not in required_overrides)
            else "android_confirmed_exact"
        )
        return resolve_chain(exact[text]), method
    if text in observed:
        translated, label = observed[text]
        return resolve_chain(translated), f"reference:{label}"

    for _pattern, template, compiled, anchor in regex_entries:
        if anchor and anchor not in text:
            continue
        match = compiled.search(text)
        if match is None:
            continue
        dynamic: list[str] = []
        for group in match.groups():
            if group in exact:
                dynamic.append(exact[group])
            elif group in observed:
                dynamic.append(observed[group][0])
            else:
                dynamic.append(group)
        result = csharp_format(template, dynamic)
        # A broad PC regex can legitimately produce another PC source key.
        # Example: 手推车挑战 becomes the intermediate mixed-language text
        # "Fusion Challenge: 手推车", for which the community project has a
        # more specific exact translation. Resolve that second stage before
        # accepting the regex output.
        result = resolve_chain(result)
        if result != text:
            return result, "pc_regex"

    template_result = translate_csharp_template_with_pc_regex(text, regex_entries)
    if template_result is not None:
        template_result = resolve_chain(template_result)
        return template_result, "pc_regex_csharp_template"
    return text, None


def build_metadata(base: bytes, layout: MetadataLayout, translated: list[bytes]) -> bytes:
    output = bytearray(base)
    new_data_offset = len(output)
    cursor = 0
    for index, raw in enumerate(translated):
        struct.pack_into("<2I", output, layout.lookup_offset + index * 8, len(raw), cursor)
        cursor += len(raw)
    output.extend(b"".join(translated))
    struct.pack_into("<I", output, 16, new_data_offset)
    struct.pack_into("<I", output, 20, cursor)
    return bytes(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, type=Path, help="clean official global-metadata.dat")
    parser.add_argument(
        "--previous-version-base",
        type=Path,
        help=(
            "clean metadata from the preceding official release; when supplied, "
            "Chinese literals absent from it are treated as new content and may "
            "use current PC English only"
        ),
    )
    parser.add_argument("--strings-dir", required=True, type=Path, help="PC English Strings directory")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument(
        "--reference-pair",
        action="append",
        nargs=3,
        metavar=("LABEL", "CHINESE_METADATA", "TRANSLATED_METADATA"),
        default=[],
        help="fallback mappings learned from a known Android Chinese/English pair; order sets priority",
    )
    parser.add_argument(
        "--reference-report",
        action="append",
        nargs=2,
        metavar=("LABEL", "METADATA_REPORT"),
        default=[],
        help=(
            "fallback exact mappings from a previously validated metadata build report; "
            "order sets priority after current PC/community translations"
        ),
    )
    args = parser.parse_args()

    base = args.base.read_bytes()
    layout, literals = parse_metadata(base)
    exact, pc_exact_sources, regex_entries, pc_counts, required_overrides = load_pc_translations(args.strings_dir)
    exact.update(METADATA_IN_LEVEL_OVERRIDES)
    previous_base = None
    previous_literals: list[MetadataLiteral] = []
    previous_literal_texts: set[str] = set()
    if args.previous_version_base is not None:
        previous_base = args.previous_version_base.read_bytes()
        _, previous_literals = parse_metadata(previous_base)
        previous_literal_texts = {literal.text for literal in previous_literals}
    (
        modifier_sources,
        modifier_title_translations,
        modifier_exact_title_translations,
        modifier_ambiguous_title_translations,
        modifier_reviewed_titles,
    ) = load_modifier_sources(args.strings_dir)

    observed: dict[str, tuple[str, str]] = {}
    reference_stats: list[dict[str, object]] = []
    reference_conflicts: list[dict[str, str]] = []
    for label, report_name in args.reference_report:
        mapping, stats = observed_translations_report(label, Path(report_name))
        reference_stats.append(stats)
        for source, target in mapping.items():
            if source in exact:
                continue
            if source in observed and observed[source][0] != target:
                reference_conflicts.append(
                    {
                        "source": source,
                        "kept_label": observed[source][1],
                        "kept_translation": observed[source][0],
                        "discarded_label": label,
                        "discarded_translation": target,
                    }
                )
                continue
            observed.setdefault(source, (target, label))
    for label, base_name, translated_name in args.reference_pair:
        mapping, stats = observed_translations(label, Path(base_name), Path(translated_name))
        reference_stats.append(stats)
        for source, target in mapping.items():
            if source in exact:
                continue
            if source in observed and observed[source][0] != target:
                reference_conflicts.append(
                    {
                        "source": source,
                        "kept_label": observed[source][1],
                        "kept_translation": observed[source][0],
                        "discarded_label": label,
                        "discarded_translation": target,
                    }
                )
                continue
            observed.setdefault(source, (target, label))

    translated_bytes: list[bytes] = []
    method_counts: dict[str, int] = {}
    changes: list[dict[str, object]] = []
    modifier_records: list[dict[str, object]] = []
    final_methods: list[str | None] = []
    new_39_audit: dict[str, dict[str, object]] = {}
    new_39_occurrences = 0
    new_39_pc_translated_occurrences = 0
    new_39_preserved_occurrences = 0
    preserved_new_39_indexes: set[int] = set()
    cjk_before = 0
    cjk_after = 0
    for index, literal in enumerate(literals):
        if CJK_RE.search(literal.text):
            cjk_before += 1
        if literal.text in ROUGE_SHOOTING_GROUP_NAMES:
            translated_text = literal.text
            method = "preserved_internal_identifier"
            preserved_new_39_indexes.add(index)
        else:
            translated_text, method = translate_literal(
            literal.text,
            exact,
            pc_exact_sources,
            observed,
            regex_entries,
            required_overrides,
        )
        is_new_39 = (
            args.previous_version_base is not None
            and CJK_RE.search(literal.text) is not None
            and literal.text not in previous_literal_texts
        )
        preserved_new_39 = False
        if is_new_39:
            new_39_occurrences += 1
            pc_authoritative = (
                method is not None
                and method.startswith("pc_")
                and CJK_RE.search(translated_text) is None
            )
            if pc_authoritative:
                new_39_pc_translated_occurrences += 1
                outcome = "pc_english"
            else:
                translated_text = literal.text
                method = "preserved_new_39_chinese"
                preserved_new_39 = True
                preserved_new_39_indexes.add(index)
                new_39_preserved_occurrences += 1
                outcome = "preserved_official_chinese"

            audit_record = new_39_audit.setdefault(
                literal.text,
                {
                    "source": literal.text,
                    "outcome": outcome,
                    "method": method,
                    "translation": translated_text,
                    "occurrences": 0,
                },
            )
            audit_record["occurrences"] = int(audit_record["occurrences"]) + 1
        modifier_reason = modifier_source_reason(literal.text, modifier_sources, modifier_reviewed_titles)
        if modifier_reason is not None and not (
            "：" in translated_text or ":" in translated_text
        ):
            modifier_reason = None
        if modifier_reason is not None and preserved_new_39:
            modifier_records.append(
                {
                    "index": index,
                    "source": literal.text,
                    "source_title": clean_modifier_source_title(literal.text),
                    "match_reason": modifier_reason,
                    "preferred_title": None,
                    "before": literal.text,
                    "translation": literal.text,
                    "title_shrunk": False,
                    "changed_by_final_parser": False,
                    "preserved_new_39_chinese": True,
                }
            )
        elif modifier_reason is not None:
            before_normalization = translated_text
            source_title = clean_modifier_source_title(literal.text)
            preferred_title = modifier_exact_title_translations.get(
                literal.text,
                modifier_title_translations.get(source_title),
            )
            translated_text, title_shrunk = normalize_modifier_translation(
                translated_text,
                preferred_title,
                source=literal.text,
            )
            modifier_records.append(
                {
                    "index": index,
                    "source": literal.text,
                    "source_title": source_title,
                    "match_reason": modifier_reason,
                    "preferred_title": preferred_title,
                    "before": before_normalization,
                    "translation": translated_text,
                    "title_shrunk": title_shrunk,
                    "changed_by_final_parser": translated_text != before_normalization,
                    "preserved_new_39_chinese": False,
                }
            )
        translated_text = translated_text.replace("\u2014", "-")
        final_methods.append(method)
        if CJK_RE.search(translated_text):
            cjk_after += 1
        raw = translated_text.encode("utf-8")
        translated_bytes.append(raw)
        if method is not None and raw != literal.raw:
            method_counts[method] = method_counts.get(method, 0) + 1
            changes.append(
                {
                    "index": index,
                    "method": method,
                    "source": literal.text,
                    "translation": translated_text,
                }
            )

    enums_dir = args.strings_dir.parent / "Enums"
    synergy_input = read_json(enums_dir / "SynergyType.json") if (enums_dir / "SynergyType.json").is_file() else {}
    invest_input = read_json(enums_dir / "InvestBuff.json") if (enums_dir / "InvestBuff.json").is_file() else {}

    synergy_fields = resolve_contiguous_enum_fields(
        base,
        synergy_input,
        "Android affinity display",
    )
    invest_fields = resolve_contiguous_enum_fields(
        base,
        invest_input,
        "Android Investment display",
    )
    definition_patched_base, display_enum_changes = translate_validated_enum_fields(
        base,
        {**synergy_fields, **invest_fields},
        "display enum",
    )
    synergy_enum_changes = [
        change for change in display_enum_changes
        if int(change["field_index"]) in synergy_fields
    ]
    invest_enum_changes = [
        change for change in display_enum_changes
        if int(change["field_index"]) in invest_fields
    ]
    output = build_metadata(definition_patched_base, layout, translated_bytes)
    output_layout, output_literals = parse_metadata(output)
    if [item.raw for item in output_literals] != translated_bytes:
        raise RuntimeError("self-validation failed: output literals do not match generated data")
    pc_exact_remnants = [
        {"index": index, "source": item.text, "expected": exact[item.text]}
        for index, item in enumerate(output_literals)
        if CJK_RE.search(item.text)
        and item.text in pc_exact_sources
        and exact[item.text] != item.text
        and index not in preserved_new_39_indexes
        and item.text not in ROUGE_SHOOTING_GROUP_NAMES
    ]
    if pc_exact_remnants:
        preview = json.dumps(pc_exact_remnants[:10], ensure_ascii=False)
        raise RuntimeError(
            "self-validation failed: translated output still contains PC exact source keys: "
            f"{preview}"
        )

    escaped_category_modifiers = [
        {"index": index, "source": literal.text}
        for index, literal in enumerate(literals)
        if clean_modifier_source_title(literal.text).startswith(MODIFIER_CATEGORY_PREFIXES)
        and not any(record["index"] == index for record in modifier_records)
    ]
    if escaped_category_modifiers:
        preview = json.dumps(escaped_category_modifiers[:10], ensure_ascii=False)
        raise RuntimeError(
            "self-validation failed: categorized modifiers escaped final parsing: "
            f"{preview}"
        )

    malformed_modifier_outputs: list[dict[str, object]] = []
    placeholder_re = re.compile(
        r"(?:description[_ -]?missing|translation[_ -]?missing|missing[_ -]?description|"
        r"\b(?:todo|tbd)\b|^\?+$)",
        re.IGNORECASE,
    )
    for record in modifier_records:
        if bool(record.get("preserved_new_39_chinese")):
            if record["translation"] != record["source"]:
                malformed_modifier_outputs.append(record)
            continue
        translated = str(record["translation"])
        parts = translated.split("：\n", 1) if "：\n" in translated else translated.split("：", 1)
        if len(parts) != 2:
            malformed_modifier_outputs.append(record)
            continue
        plain_title = re.sub(r"<[^>]+>", "", parts[0]).strip()
        body = parts[1].lstrip()
        title_variants = {plain_title}
        for separator in (": ", " - "):
            if separator in plain_title:
                title_variants.add(plain_title.rsplit(separator, 1)[-1].strip())
        preferred_title = record.get("preferred_title")
        if (
            not plain_title
            or not body
            or (
                isinstance(preferred_title, str)
                and preferred_title.strip().rstrip(":：").strip() != plain_title
            )
            or placeholder_re.search(plain_title) is not None
            or placeholder_re.search(body) is not None
            or any(
                re.match(
                    rf"^{re.escape(title_variant)}\s*[:：]",
                    body,
                    flags=re.IGNORECASE,
                )
                for title_variant in title_variants
            )
            or re.match(r"^.{1,24}\?*\s*:\s*(?:\n|$)", body)
        ):
            malformed_modifier_outputs.append(record)
    if malformed_modifier_outputs:
        preview = json.dumps(malformed_modifier_outputs[:10], ensure_ascii=False)
        raise RuntimeError(
            "self-validation failed: modifier title text leaked into a description: "
            f"{preview}"
        )

    recognized_modifier_indexes = {int(record["index"]) for record in modifier_records}
    missing_structured_modifier_records = [
        {"index": index, "source": literal.text}
        for index, literal in enumerate(literals)
        if literal.text in modifier_sources and index not in recognized_modifier_indexes
    ]
    if missing_structured_modifier_records:
        preview = json.dumps(missing_structured_modifier_records[:10], ensure_ascii=False)
        raise RuntimeError(
            "self-validation failed: structured PC modifier records escaped normalization: "
            f"{preview}"
        )

    sp_evolution_records = [
        {
            "index": index,
            "source": literals[index].text,
            "translation": output_literals[index].text,
            "method": final_methods[index],
            "new_39": literals[index].text not in previous_literal_texts
            if args.previous_version_base is not None
            else None,
        }
        for index in range(len(literals))
        if "【SP进化】" in literals[index].text
    ]
    if len(sp_evolution_records) != 4 or any(
        (
            record["new_39"] is True
            and record["translation"] != record["source"]
            and not (
                isinstance(record["method"], str)
                and str(record["method"]).startswith("pc_")
                and CJK_RE.search(str(record["translation"])) is None
            )
        )
        for record in sp_evolution_records
    ):
        raise RuntimeError(
            "self-validation failed: a new SP Evolution recipe did not follow PC-or-Chinese policy"
        )

    # Custom level editor enums and EventListValueType are translated via translate_validated_enum_fields above

    args.output.parent.mkdir(parents=True, exist_ok=True)
    temp_meta = args.output.with_suffix(".tmp")
    temp_meta.write_bytes(output)
    if temp_meta.exists():
        temp_meta.replace(args.output)
    report = {
        "format_version": 1,
        "base": {
            "path": str(args.base.resolve()),
            "size": len(base),
            "sha256": sha256(base),
            "literal_count": len(literals),
            "literal_data_offset": layout.data_offset,
            "literal_data_size": layout.data_size,
            "cjk_literal_occurrences": cjk_before,
        },
        "output": {
            "path": str(args.output.resolve()),
            "size": len(output),
            "sha256": sha256(output),
            "literal_count": len(output_literals),
            "literal_data_offset": output_layout.data_offset,
            "literal_data_size": output_layout.data_size,
            "cjk_literal_occurrences": cjk_after,
        },
        "pc_translation_entries": pc_counts,
        "pc_exact_source_remnants": 0,
        "new_39_translation_policy": {
            "enabled": args.previous_version_base is not None,
            "rule": (
                "Use current PC English for content introduced in 3.9; otherwise preserve "
                "the official Chinese literal"
            ),
            "previous_version_base": None
            if args.previous_version_base is None
            else {
                "path": str(args.previous_version_base.resolve()),
                "size": len(previous_base or b""),
                "sha256": sha256(previous_base or b""),
                "literal_count": len(previous_literals),
                "unique_literal_count": len(previous_literal_texts),
            },
            "new_cjk_literal_occurrences": new_39_occurrences,
            "pc_english_occurrences": new_39_pc_translated_occurrences,
            "preserved_official_chinese_occurrences": new_39_preserved_occurrences,
            "unique_records": sorted(
                new_39_audit.values(),
                key=lambda record: str(record["source"]),
            ),
        },
        "android_affinity_enum": {
            "strategy": "validated field-name rename; enum values and all IL2CPP code unchanged",
            "changed_field_count": len(synergy_enum_changes),
            "changes": synergy_enum_changes,
        },
        "android_investment_enum": {
            "strategy": "validated field-name rename; enum values and all IL2CPP code unchanged",
            "changed_field_count": len(invest_enum_changes),
            "changes": invest_enum_changes,
        },
        "reference_pairs": reference_stats,
        "reference_conflicts": reference_conflicts,
        "modifier_almanac_parser": {
            "known_source_count": len(modifier_sources),
            "known_title_translation_count": len(modifier_title_translations),
            "known_exact_title_translation_count": len(modifier_exact_title_translations),
            "ambiguous_source_titles": modifier_ambiguous_title_translations,
            "parsed_literal_occurrences": len(modifier_records),
            "title_based_literal_occurrences": sum(
                record["match_reason"] != "exact_pc_or_reviewed_source"
                for record in modifier_records
            ),
            "preferred_title_occurrences": sum(
                record["preferred_title"] is not None
                for record in modifier_records
            ),
            "shrunk_title_occurrences": sum(
                bool(record["title_shrunk"])
                for record in modifier_records
            ),
            "escaped_category_modifier_occurrences": 0,
            "changed_after_provenance_resolution": sum(
                bool(record["changed_by_final_parser"])
                for record in modifier_records
            ),
            "records": modifier_records,
        },
        "sp_evolution_recipe_occurrences": len(sp_evolution_records),
        "sp_evolution_recipe_records": sp_evolution_records,
        "method_counts": dict(sorted(method_counts.items())),
        "changed_literal_occurrences": len(changes),
        "changes": changes,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("base", "output", "method_counts", "changed_literal_occurrences")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
