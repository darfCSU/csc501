#!/usr/bin/env python3

import json
import re
import sys
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def load_config(filename):
    with open(filename, "r", encoding="utf-8") as file:
        config = json.load(file)

    required = ["source", "project", "matrix", "style", "register", "output"]

    for key in required:
        if key not in config:
            raise ValueError(f"Missing configuration section: {key}")

    return config


def parse_table(lines):
    rows = []

    for line in lines:
        line = line.strip()

        if not line.startswith("|"):
            if rows:
                break
            continue

        cells = [cell.strip() for cell in line.strip("|").split("|")]

        # Ignore Markdown separator rows.
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
                if following.startswith("#"):
                    break
                section_lines.append(following)

            return section_lines

    raise ValueError(f"Markdown section not found: {heading}")


def clean_markdown_text(value):
    value = value.strip()
    value = re.sub(r"^\*\*(.*?)\*\*$", r"\1", value)
    value = re.sub(r"^\*(.*?)\*$", r"\1", value)
    return value


def extract_swot(lines, config):
    source = config["source"]

    section = extract_section(
        lines,
        source["swot_heading"]
    )

    rows = parse_table(section)

    columns = source["swot_columns"]
    category_column = columns["category"]
    factors_column = columns["factors"]

    swot = {}

    for row in rows:
        category = clean_markdown_text(row[category_column])
        key = category.lower()

        if key not in ("strengths", "weaknesses", "opportunities", "threats"):
            raise ValueError(f"Unknown SWOT category: {category}")

        if key in swot:
            raise ValueError(f"Duplicate SWOT category: {category}")

        swot[key] = clean_markdown_text(row[factors_column])

    required = ("strengths", "weaknesses", "opportunities", "threats")
    missing = [category for category in required if category not in swot]

    if missing:
        raise ValueError(
            f"Missing SWOT categories in Markdown: {', '.join(missing)}"
        )

    return swot


def read_markdown(config):
    source = config["source"]
    source_file = Path(source["markdown_file"])

    if not source_file.is_file():
        raise FileNotFoundError(f"Markdown file not found: {source_file}")

    lines = source_file.read_text(encoding="utf-8").splitlines()

    register_lines = extract_section(
        lines,
        source["risk_register_heading"]
    )

    risk_rows = parse_table(register_lines)

    if not risk_rows:
        raise ValueError("No risk register table was found in the Markdown.")

    risk_columns = source["risk_columns"]

    for column in risk_columns.values():
        if column not in risk_rows[0]:
            raise ValueError(
                f"Risk register is missing column: {column}"
            )

    parsed_risks = []

    for row in risk_rows:
        risk = {
            "id": clean_markdown_text(row[risk_columns["id"]]),
            "title": clean_markdown_text(row[risk_columns["description"]]),
            "probability": clean_markdown_text(
                row[risk_columns["probability"]]
            ),
            "severity": clean_markdown_text(
                row[risk_columns["severity"]]
            ),
            "rating": clean_markdown_text(row[risk_columns["rating"]]),
            "owner": clean_markdown_text(row[risk_columns["owner"]]),
        }

        parsed_risks.append(risk)

    swot = extract_swot(lines, config)

    return parsed_risks, swot


def validate_risks(risks, config):
    probabilities = config["matrix"]["probabilities"]
    severities = config["matrix"]["severities"]
    ratings = config["matrix"]["ratings"]
    colors = config["style"]["risk_colors"]

    if not risks:
        raise ValueError("No risks were found in the Markdown register.")

    seen_ids = set()

    for risk in risks:
        if not risk["id"]:
            raise ValueError("A risk is missing its ID.")

        if risk["id"] in seen_ids:
            raise ValueError(f'Duplicate risk ID: {risk["id"]}')

        seen_ids.add(risk["id"])

        if not risk["title"]:
            raise ValueError(f'{risk["id"]}: Risk description is blank.')

        if not risk["owner"]:
            raise ValueError(f'{risk["id"]}: Risk owner is blank.')

        if risk["probability"] not in probabilities:
            raise ValueError(
                f'{risk["id"]}: Invalid probability: '
                f'{risk["probability"]}'
            )

        if risk["severity"] not in severities:
            raise ValueError(
                f'{risk["id"]}: Invalid severity: '
                f'{risk["severity"]}'
            )

        if risk["rating"] not in colors:
            raise ValueError(
                f'{risk["id"]}: Missing color for rating: '
                f'{risk["rating"]}'
            )

        expected = ratings[risk["probability"]][risk["severity"]]

        if risk["rating"] != expected:
            raise ValueError(
                f'{risk["id"]}: Register rating is {risk["rating"]}, '
                f'but the configured matrix calculates {expected}.'
            )


def apply_style(config):
    style = config["style"]

    plt.rcParams.update({
        "figure.facecolor": style["background"],
        "axes.facecolor": style["background"],
        "axes.edgecolor": style["grid_color"],
        "axes.labelcolor": style["text_color"],
        "text.color": style["text_color"],
        "xtick.color": style["text_color"],
        "ytick.color": style["text_color"],
        "font.family": style["font_family"],
        "font.size": style["font_size"],
    })


def add_header(fig, title, subtitle, config):
    style = config["style"]

    fig.text(
        style["header_x"],
        style["header_y"],
        title,
        fontsize=style["title_font_size"],
        fontweight="bold",
        color=style["title_color"],
        va="top"
    )

    fig.text(
        style["header_x"],
        style["subtitle_y"],
        subtitle,
        fontsize=style["subtitle_font_size"],
        color=style["subtitle_color"],
        va="top"
    )


def make_risk_matrix(config, risks):
    style = config["style"]
    matrix = config["matrix"]
    probabilities = matrix["probabilities"]
    severities = matrix["severities"]

    fig, ax = plt.subplots(
        figsize=style["matrix_figure_size"]
    )

    add_header(
        fig,
        config["project"]["matrix_title"],
        config["project"]["subtitle"],
        config
    )

    ax.set_xlim(0, len(severities))
    ax.set_ylim(0, len(probabilities))
    ax.invert_yaxis()
    ax.set_aspect("equal")

    risk_colors = style["risk_colors"]

    for row, probability in enumerate(probabilities):
        for col, severity in enumerate(severities):
            rating = matrix["ratings"][probability][severity]
            color = risk_colors[rating]

            ax.add_patch(Rectangle(
                (col, row),
                1,
                1,
                facecolor=color,
                edgecolor=style["grid_color"],
                linewidth=style["cell_border_width"]
            ))

            cell_risks = [
                risk["id"]
                for risk in risks
                if risk["probability"] == probability
                and risk["severity"] == severity
            ]

            text_color = style["rating_text_colors"][rating]

            ax.text(
                col + 0.5,
                row + 0.28,
                rating.upper(),
                ha="center",
                va="center",
                fontsize=style["rating_font_size"],
                fontweight="bold",
                color=text_color
            )

            if cell_risks:
                ax.text(
                    col + 0.5,
                    row + 0.67,
                    style["risk_separator"].join(cell_risks),
                    ha="center",
                    va="center",
                    fontsize=style["risk_id_font_size"],
                    fontweight="bold",
                    color=text_color
                )

    ax.set_xticks([
        index + 0.5 for index in range(len(severities))
    ])
    ax.set_xticklabels(
        severities,
        fontsize=style["axis_font_size"],
        fontweight="bold"
    )

    ax.set_yticks([
        index + 0.5 for index in range(len(probabilities))
    ])
    ax.set_yticklabels(
        probabilities,
        fontsize=style["axis_font_size"],
        fontweight="bold"
    )

    ax.set_xlabel(
        matrix["severity_axis_label"],
        fontsize=style["axis_label_font_size"],
        fontweight="bold",
        labelpad=style["axis_label_padding"]
    )

    ax.set_ylabel(
        matrix["probability_axis_label"],
        fontsize=style["axis_label_font_size"],
        fontweight="bold",
        labelpad=style["axis_label_padding"]
    )

    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.subplots_adjust(
        left=style["matrix_left"],
        right=style["matrix_right"],
        top=style["matrix_top"],
        bottom=style["matrix_bottom"]
    )

    return fig


def make_swot(config, swot):
    style = config["style"]

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

    quadrants = config["swot"]["quadrants"]

    for item in quadrants:
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

        item_text = textwrap.fill(
            swot[key],
            width=style["swot_wrap_width"]
        )

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


def make_risk_register(config, risks):
    style = config["style"]
    columns = config["register"]["columns"]

    register_height = max(
        style["register_min_height"],
        len(risks) * style["register_row_height"]
        + style["register_extra_height"]
    )

    figure_width = style["register_figure_width"]

    fig, ax = plt.subplots(
        figsize=(figure_width, register_height)
    )

    # Reserve a dedicated header area above the table.
    add_header(
        fig,
        config["project"]["register_title"],
        config["project"]["subtitle"],
        config
    )

    ax.set_xlim(
        style["register_x_min"],
        style["register_x_max"]
    )
    ax.set_ylim(
        len(risks) - 0.5,
        -1.0
    )
    ax.axis("off")

    # Column headings occupy their own row above the risk entries.
    for column in columns.values():
        ax.text(
            column["x"],
            -0.55,
            column["label"],
            fontsize=style["register_heading_font_size"],
            fontweight="bold",
            ha="center",
            va="center"
        )

    for index, risk in enumerate(risks):
        color = style["risk_colors"][risk["rating"]]

        ax.add_patch(Rectangle(
            (
                style["register_bar_x"],
                index - style["register_bar_height"] / 2
            ),
            style["register_bar_width"],
            style["register_bar_height"],
            facecolor=color,
            edgecolor="none"
        ))

        title = textwrap.fill(
            f'{risk["id"]} — {risk["title"]}',
            width=style["register_wrap_width"]
        )

        ax.text(
            columns["risk"]["x"],
            index,
            title,
            fontsize=style["register_text_font_size"],
            fontweight="bold",
            va="center"
        )

        ax.text(
            columns["probability_severity"]["x"],
            index,
            (
                f'{risk["probability"]}\n'
                f'{risk["severity"]}'
            ),
            fontsize=style["register_detail_font_size"],
            va="center",
            ha="center"
        )

        ax.text(
            columns["owner"]["x"],
            index,
            risk["owner"],
            fontsize=style["register_owner_font_size"],
            va="center",
            ha="center"
        )

        ax.text(
            columns["rating"]["x"],
            index,
            risk["rating"].upper(),
            fontsize=style["register_rating_font_size"],
            fontweight="bold",
            color=color,
            va="center",
            ha="center"
        )

        if index < len(risks) - 1:
            ax.plot(
                [
                    style["register_line_start"],
                    style["register_line_end"]
                ],
                [index + 0.5, index + 0.5],
                color=style["register_divider_color"],
                linewidth=style["register_divider_width"]
            )

    # Place the chart title and subtitle in a separate figure-level area.
    fig.subplots_adjust(
        left=style["register_left"],
        right=style["register_right"],
        top=style["register_top"],
        bottom=style["register_bottom"]
    )

    return fig


def save_figure(fig, filename, config):
    output = Path(config["output"]["directory"])
    output.mkdir(parents=True, exist_ok=True)

    path = output / filename

    fig.savefig(
        path,
        dpi=config["style"]["output_dpi"],
        bbox_inches="tight",
        facecolor=config["style"]["background"]
    )

    print(f"Created: {path}")
    plt.close(fig)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} risk_config.json")
        return 1

    try:
        config = load_config(sys.argv[1])
        risks, swot = read_markdown(config)

        validate_risks(risks, config)
        apply_style(config)

        save_figure(
            make_risk_matrix(config, risks),
            config["output"]["risk_matrix"],
            config
        )

        save_figure(
            make_swot(config, swot),
            config["output"]["swot"],
            config
        )

        save_figure(
            make_risk_register(config, risks),
            config["output"]["risk_register"],
            config
        )

    except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
