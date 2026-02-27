#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml  # type: ignore[import-not-found]
except ImportError:
    yaml = None


MARGIN_X = 70
MARGIN_Y = 90
LAYER_GAP = 90
ROW_GAP = 26
BOX_W = 280
BOX_H = 92
HEADER_GAP = 70
BOTTOM_NOTE_GAP = 64
SECTION_TITLE_H = 28
SECTION_GAP = 42


@dataclass
class Component:
    id: str
    label: list[str]
    stroke: str = "#222"


@dataclass
class Layer:
    id: str
    name: str
    sections: list["LayerSection"]


@dataclass
class LayerSection:
    name: str
    components: list[Component]


@dataclass
class YamlLine:
    indent: int
    text: str


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_]+", "-", text.strip()).strip("-").lower()
    return slug or "component"


def parse_scalar(raw: str) -> object:
    value = raw.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value == "true":
        return True
    if value == "false":
        return False
    return value


def preprocess_yaml_lines(text: str) -> list[YamlLine]:
    lines: list[YamlLine] = []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        stripped = raw.lstrip(" ")
        if stripped.startswith("#"):
            continue
        indent = len(raw) - len(stripped)
        lines.append(YamlLine(indent=indent, text=stripped))
    return lines


def parse_yaml_node(lines: list[YamlLine], i: int, indent: int) -> tuple[object, int]:
    if i >= len(lines):
        return {}, i
    if lines[i].indent != indent:
        raise ValueError("Некорректные отступы в YAML")
    if lines[i].text.startswith("- "):
        return parse_yaml_list(lines, i, indent)
    return parse_yaml_dict(lines, i, indent)


def parse_yaml_dict(
    lines: list[YamlLine], i: int, indent: int
) -> tuple[dict[str, object], int]:
    result: dict[str, object] = {}
    while i < len(lines):
        line = lines[i]
        if line.indent < indent:
            break
        if line.indent > indent:
            raise ValueError("Некорректные отступы в YAML-объекте")
        if line.text.startswith("- "):
            break
        if ":" not in line.text:
            raise ValueError(f"Ожидалась пара key: value, получено: {line.text!r}")
        key, rest = line.text.split(":", 1)
        key = key.strip()
        rest = rest.lstrip()
        if not key:
            raise ValueError("Пустой ключ в YAML")

        if rest in ("|", ">"):
            i += 1
            block_lines: list[str] = []
            base_indent = (
                lines[i].indent if i < len(lines) and lines[i].indent > indent else None
            )
            while i < len(lines):
                nxt = lines[i]
                if nxt.indent <= indent:
                    break
                if base_indent is None:
                    base_indent = nxt.indent
                cut = base_indent if nxt.indent >= base_indent else nxt.indent
                block_lines.append((" " * (nxt.indent - cut)) + nxt.text)
                i += 1
            result[key] = "\n".join(block_lines)
            continue

        if rest:
            result[key] = parse_scalar(rest)
            i += 1
            continue

        i += 1
        if i < len(lines) and lines[i].indent > indent:
            value, i = parse_yaml_node(lines, i, lines[i].indent)
            result[key] = value
        else:
            result[key] = {}
    return result, i


def parse_yaml_list(
    lines: list[YamlLine], i: int, indent: int
) -> tuple[list[object], int]:
    result: list[object] = []
    while i < len(lines):
        line = lines[i]
        if line.indent < indent:
            break
        if line.indent != indent or not line.text.startswith("- "):
            break
        item_text = line.text[2:].lstrip()

        if not item_text:
            i += 1
            if i < len(lines) and lines[i].indent > indent:
                value, i = parse_yaml_node(lines, i, lines[i].indent)
            else:
                value = None
            result.append(value)
            continue

        is_inline_mapping = bool(re.match(r"^[A-Za-z0-9_-]+:\s*.*$", item_text))
        if is_inline_mapping:
            key, rest = item_text.split(":", 1)
            key = key.strip()
            rest = rest.lstrip()
            obj: dict[str, object] = {}
            if rest:
                obj[key] = parse_scalar(rest)
                i += 1
            else:
                i += 1
                if i < len(lines) and lines[i].indent > indent:
                    value, i = parse_yaml_node(lines, i, lines[i].indent)
                    obj[key] = value
                else:
                    obj[key] = {}

            if i < len(lines) and lines[i].indent > indent:
                extra, i = parse_yaml_node(lines, i, lines[i].indent)
                if not isinstance(extra, dict):
                    raise ValueError("Ожидался объект после элемента списка")
                obj.update(extra)
            result.append(obj)
            continue

        result.append(parse_scalar(item_text))
        i += 1
    return result, i


def load_yaml_text(text: str) -> dict:
    if yaml is not None:
        doc = yaml.safe_load(text)
    else:
        lines = preprocess_yaml_lines(text)
        if not lines:
            raise ValueError("Пустой YAML")
        doc, end = parse_yaml_node(lines, 0, lines[0].indent)
        if end != len(lines):
            raise ValueError("Не удалось разобрать YAML до конца")
    if not isinstance(doc, dict):
        raise ValueError("YAML должен быть объектом верхнего уровня")
    return doc


def parse_component(data: object, fallback_id: str) -> Component:
    if isinstance(data, str):
        return Component(id=fallback_id, label=[data])

    if not isinstance(data, dict):
        raise ValueError(f"Компонент {fallback_id!r} должен быть строкой или объектом")

    cid = str(data.get("id") or fallback_id)
    label = data.get("label")
    if label is None:
        name = data.get("name")
        if name is None:
            raise ValueError(f"У компонента {cid!r} нет поля label или name")
        label = [str(name)]
    elif isinstance(label, str):
        label = label.splitlines() if "\n" in label else [label]
    elif isinstance(label, list):
        label = [str(x) for x in label]
    else:
        raise ValueError(
            f"Поле label у компонента {cid!r} должно быть строкой или списком"
        )

    stroke = str(data.get("stroke", "#222"))
    return Component(id=cid, label=label, stroke=stroke)


def parse_layers(doc: dict) -> list[Layer]:
    raw_layers = doc.get("layers")

    if raw_layers is None:
        # Поддержка legacy-формы: layer1/layer2/... на верхнем уровне.
        raw_layers = []
        for key in sorted(doc.keys()):
            if key.startswith("layer") and isinstance(doc[key], dict):
                item = dict(doc[key])
                item.setdefault("id", key)
                raw_layers.append(item)

    if not isinstance(raw_layers, list) or not raw_layers:
        raise ValueError("Нужен непустой список layers")

    layers: list[Layer] = []
    seen_component_ids: set[str] = set()

    for idx, raw_layer in enumerate(raw_layers, start=1):
        if not isinstance(raw_layer, dict):
            raise ValueError("Каждый элемент layers должен быть объектом")

        lid = str(raw_layer.get("id") or f"layer{idx}")
        name = str(raw_layer.get("name") or lid)
        sections: list[LayerSection] = []
        raw_sections = raw_layer.get("sections")
        if raw_sections is not None:
            if not isinstance(raw_sections, list) or not raw_sections:
                raise ValueError(
                    f"Слой {lid!r}: поле sections должно быть непустым списком"
                )
            for sidx, raw_section in enumerate(raw_sections, start=1):
                if not isinstance(raw_section, dict):
                    raise ValueError(
                        f"Слой {lid!r}: секция #{sidx} должна быть объектом"
                    )
                sname = str(raw_section.get("name", "")).strip()
                raw_components = raw_section.get("components", [])
                if not isinstance(raw_components, list) or not raw_components:
                    raise ValueError(
                        f"Слой {lid!r}: секция {sname or sidx!r} должна содержать components"
                    )
                comps: list[Component] = []
                for cidx, raw_comp in enumerate(raw_components, start=1):
                    fallback = f"{lid}-s{sidx}-c{cidx}-{slugify(str(raw_comp))}"
                    comp = parse_component(raw_comp, fallback)
                    if comp.id in seen_component_ids:
                        raise ValueError(f"Повторяющийся id компонента: {comp.id}")
                    seen_component_ids.add(comp.id)
                    comps.append(comp)
                sections.append(LayerSection(name=sname, components=comps))
        else:
            raw_components = raw_layer.get("components", [])
            if not isinstance(raw_components, list) or not raw_components:
                raise ValueError(
                    f"Слой {lid!r} должен содержать непустой список components"
                )
            comps: list[Component] = []
            for cidx, raw_comp in enumerate(raw_components, start=1):
                fallback = f"{lid}-{cidx}-{slugify(str(raw_comp))}"
                comp = parse_component(raw_comp, fallback)
                if comp.id in seen_component_ids:
                    raise ValueError(f"Повторяющийся id компонента: {comp.id}")
                seen_component_ids.add(comp.id)
                comps.append(comp)
            sections.append(LayerSection(name="", components=comps))

        layers.append(Layer(id=lid, name=name, sections=sections))

    return layers


def parse_connections(doc: dict, ids: set[str]) -> list[dict[str, str]]:
    raw = doc.get("connections", [])
    if not isinstance(raw, list):
        raise ValueError("Поле connections должно быть списком")

    result: list[dict[str, str]] = []
    for i, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Связь #{i} должна быть объектом")
        src = str(item.get("from", "")).strip()
        dst = str(item.get("to", "")).strip()
        if not src or not dst:
            raise ValueError(f"Связь #{i} должна содержать from и to")
        if src not in ids:
            raise ValueError(f"В связи #{i}: неизвестный from={src!r}")
        if dst not in ids:
            raise ValueError(f"В связи #{i}: неизвестный to={dst!r}")
        result.append({"from": src, "to": dst})
    return result


def svg_text(x: int, y: int, content: str, size: int = 26, weight: str = "400") -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="#111">{esc(content)}</text>'
    )


def svg_multiline_text(
    x: int, y: int, lines: list[str], size: int = 22, weight: str = "400", lh: int = 24
) -> str:
    body = []
    for i, line in enumerate(lines):
        dy = y + i * lh
        body.append(
            f'<text x="{x}" y="{dy}" font-family="Arial, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="#111">{esc(line)}</text>'
        )
    return "\n".join(body)


def svg_box(x: int, y: int, label: list[str], stroke: str = "#222") -> str:
    rect = (
        f'<rect x="{x}" y="{y}" width="{BOX_W}" height="{BOX_H}" rx="18" ry="18" '
        f'fill="white" stroke="{stroke}" stroke-width="3"/>'
    )
    line_count = max(1, len(label))
    base_y = y + (BOX_H - (line_count - 1) * 24) // 2 + 8
    txt = svg_multiline_text(x + 14, base_y, label, size=22 if line_count <= 2 else 20)
    return rect + "\n" + txt


def svg_arrow(x1: int, y1: int, x2: int, y2: int) -> str:
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222" '
        f'stroke-width="2.5" marker-end="url(#arrow)"/>'
    )


def render(layers: list[Layer], connections: list[dict[str, str]], note: str) -> str:
    center_layer_index = len(layers) // 2

    def section_has_title(layer: Layer, section: LayerSection) -> bool:
        return len(layer.sections) > 1 and bool(section.name.strip())

    def layer_content_height(layer: Layer) -> int:
        h = 0
        for i, section in enumerate(layer.sections):
            if section_has_title(layer, section):
                h += SECTION_TITLE_H
            rows = len(section.components)
            h += rows * BOX_H + max(0, rows - 1) * ROW_GAP
            if i < len(layer.sections) - 1:
                h += SECTION_GAP
        return h

    max_content_height = max(layer_content_height(layer) for layer in layers)
    width = MARGIN_X * 2 + len(layers) * BOX_W + (len(layers) - 1) * LAYER_GAP
    height = MARGIN_Y + HEADER_GAP + max_content_height + BOTTOM_NOTE_GAP + 32

    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
    )
    parts.append(
        """
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#222"/>
  </marker>
</defs>
"""
    )
    parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="white"/>')

    by_id: dict[str, tuple[int, int, int]] = {}

    top_y = MARGIN_Y + HEADER_GAP
    for li, layer in enumerate(layers):
        x = MARGIN_X + li * (BOX_W + LAYER_GAP)

        if li > 0:
            sep_x = x - (LAYER_GAP // 2)
            parts.append(
                f'<line x1="{sep_x}" y1="{MARGIN_Y - 24}" x2="{sep_x}" y2="{height - BOTTOM_NOTE_GAP - 18}" stroke="#111" stroke-width="3"/>'
            )

        layer_name_lines = (
            layer.name.splitlines() if "\n" in layer.name else [layer.name]
        )
        parts.append(
            svg_multiline_text(
                x + 10, MARGIN_Y, layer_name_lines, size=28, weight="600", lh=30
            )
        )

        y_cursor = top_y
        for si, section in enumerate(layer.sections):
            if section_has_title(layer, section):
                parts.append(
                    svg_text(x + 8, y_cursor + 20, section.name, size=20, weight="600")
                )
                y_cursor += SECTION_TITLE_H

            for ci, comp in enumerate(section.components):
                y = y_cursor + ci * (BOX_H + ROW_GAP)
                parts.append(svg_box(x, y, comp.label, stroke=comp.stroke))
                by_id[comp.id] = (li, x, y)
            y_cursor += (
                len(section.components) * BOX_H
                + max(0, len(section.components) - 1) * ROW_GAP
            )
            if si < len(layer.sections) - 1:
                y_cursor += SECTION_GAP

    for conn in connections:
        src_l, src_x, src_y = by_id[conn["from"]]
        dst_l, dst_x, dst_y = by_id[conn["to"]]
        src_mid_y = src_y + BOX_H // 2
        dst_mid_y = dst_y + BOX_H // 2

        # Render arrows toward center layer to emphasize dependency direction.
        if abs(src_l - center_layer_index) < abs(dst_l - center_layer_index):
            src_l, dst_l = dst_l, src_l
            src_x, dst_x = dst_x, src_x
            src_mid_y, dst_mid_y = dst_mid_y, src_mid_y

        if src_l <= dst_l:
            x1 = src_x + BOX_W
            x2 = dst_x
        else:
            x1 = src_x
            x2 = dst_x + BOX_W

        parts.append(svg_arrow(x1, src_mid_y, x2, dst_mid_y))

    if note:
        note_lines = note.splitlines() if "\n" in note else [note]
        note_y = height - 24 - (len(note_lines) - 1) * 22
        parts.append(
            svg_multiline_text(
                MARGIN_X, note_y, note_lines, size=18, weight="600", lh=22
            )
        )

    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Генератор SVG-схемы layered architecture из YAML"
    )
    parser.add_argument(
        "--input",
        default="scripts/clean-architecture.yaml",
        help="Путь к YAML-конфигу",
    )
    parser.add_argument(
        "--output",
        default="src/assets/clean-architecture.svg",
        help="Путь к результирующему SVG",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    input_path = (repo_root / args.input).resolve()
    output_path = (repo_root / args.output).resolve()

    doc = load_yaml_text(input_path.read_text(encoding="utf-8"))

    layers = parse_layers(doc)
    component_ids = {
        c.id
        for layer in layers
        for section in layer.sections
        for c in section.components
    }
    connections = parse_connections(doc, component_ids)
    note = str(doc.get("note", "")).strip()

    svg = render(layers, connections, note)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg, encoding="utf-8")
    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
