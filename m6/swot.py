import re
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def parse_table(lines):
    rows = []

    for line in lines:
        line = line.strip()

        if not line.startswith("|"):
            if rows:
                break
            continue

        cells = [cell.strip() for cell in line.strip("|").split("|")]

        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue

        rows.append(cells)

    if len(rows) < 2:
        return []

    headers = rows[0]
    results = []

    for row in rows[1:]:
        if len(row) != len(headers):
            continue

        results.append(dict(zip(headers, row)))

    return results


def extract_section(lines, heading):
    target = heading.strip().lower()

    for index, line in enumerate(lines):
        if line.strip().lower() == target:
            section_lines = []

            for following in lines[index + 1:]:
                if following.lstrip().startswith("#"):
                    break

                section_lines.append(following)

            return section_lines

    raise ValueError(f"Markdown section not found: {heading}")


def clean_markdown_text(value):
    value = value.strip()
    value = re.sub(r"^\*\*(.*?)\*\*$", r"\1", value)
    value = re.sub(r"^\*(.*?)\*$", r"\1", value)
    return value


def split_factors(value):
    """Turn the contents of a SWOT table cell into separate factors."""
    value = clean_markdown_text(value)

    parts = re.split(
        r"(?:<br\s*/?>|\n)+",
        value,
        flags=re.IGNORECASE
    )

    factors = []

    for part in parts:
        part = part.strip()

        if not part:
            continue

        part = re.sub(r"^\s*[-*+]\s+", "", part)

        sentences = re.split(r"(?<=[.!?])\s+", part)

        for sentence in sentences:
            sentence = sentence.strip()

            if sentence:
                factors.append(sentence)

    return factors


def read_swot(config):
    source = config["source"]
    source_file = Path(source["markdown_file"])

    if not source_file.is_file():
        raise FileNotFoundError(
            f"Markdown file not found: {source_file}"
        )

    lines = source_file.read_text(
        encoding="utf-8"
    ).splitlines()

    section = extract_section(
        lines,
        source["swot_heading"]
    )

    rows = parse_table(section)

    if not rows:
        raise ValueError("No SWOT table was found in the Markdown.")

    columns = source["swot_columns"]
    category_column = columns["category"]
    factors_column = columns["factors"]

    for column in (category_column, factors_column):
        if column not in rows[0]:
            raise ValueError(
                f"SWOT table is missing column: {column}"
            )

    swot = {}

    for row in rows:
        category = clean_markdown_text(row[category_column])
        key = category.lower()

        if key not in (
            "strengths",
            "weaknesses",
            "opportunities",
            "threats",
        ):
            raise ValueError(f"Unknown SWOT category: {category}")

        if key in swot:
            raise ValueError(f"Duplicate SWOT category: {category}")

        swot[key] = split_factors(row[factors_column])

    required = (
        "strengths",
        "weaknesses",
        "opportunities",
        "threats",
    )

    missing = [category for category in required if category not in swot]

    if missing:
        raise ValueError(
            f"Missing SWOT categories in Markdown: {', '.join(missing)}"
        )

    for category in required:
        if not swot[category]:
            raise ValueError(
                f"SWOT category has no factors: {category}"
            )

    return swot


def make_swot(config, swot, add_header):
    style = config["style"]
    swot_config = config["swot"]

    fig, ax = plt.subplots(
        figsize=style["swot_figure_size"]
    )

    add_header(
        fig,
        config["project"]["swot_title"],
        config["project"]["subtitle"],
        config
    )

    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.axis("off")

    bullet = swot_config["bullet"]

    for item in swot_config["quadrants"]:
        key = item["key"]
        x = item["x"]
        y = item["y"]
        color = item["color"]
        title = item["title"]
        text_color = item["text_color"]

        ax.add_patch(Rectangle(
            (x, y),
            1,
            1,
            facecolor=color,
            edgecolor=style["background"],
            linewidth=style["swot_border_width"]
        ))

        ax.text(
            x + style["swot_text_padding"],
            y + style["swot_title_y"],
            title,
            fontsize=style["swot_title_font_size"],
            fontweight="bold",
            color=text_color,
            va="top"
        )

        bullet_points = []

        for factor in swot[key]:
            wrapped = textwrap.fill(
                factor,
                width=style["swot_wrap_width"],
                initial_indent=f"{bullet} ",
                subsequent_indent="  "
            )

            bullet_points.append(wrapped)

        item_text = "\n".join(bullet_points)

        ax.text(
            x + style["swot_text_padding"],
            y + style["swot_body_y"],
            item_text,
            fontsize=style["swot_body_font_size"],
            color=text_color,
            va="top",
            linespacing=style["swot_line_spacing"]
        )

    fig.subplots_adjust(
        left=style["swot_left"],
        right=style["swot_right"],
        top=style["swot_top"],
        bottom=style["swot_bottom"]
    )

    return fig
