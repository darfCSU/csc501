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


def read_risks(config):
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
        source["risk_register_heading"]
    )

    rows = parse_table(section)

    if not rows:
        raise ValueError(
            "No risk register table was found in the Markdown."
        )

    columns = source["risk_columns"]

    for column in columns.values():
        if column not in rows[0]:
            raise ValueError(
                f"Risk register is missing column: {column}"
            )

    risks = []

    for row in rows:
        risks.append({
            "id": clean_markdown_text(row[columns["id"]]),
            "title": clean_markdown_text(
                row[columns["description"]]
            ),
            "probability": clean_markdown_text(
                row[columns["probability"]]
            ),
            "severity": clean_markdown_text(
                row[columns["severity"]]
            ),
            "rating": clean_markdown_text(
                row[columns["rating"]]
            ),
            "owner": clean_markdown_text(
                row[columns["owner"]]
            ),
        })

    return risks


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
            raise ValueError(
                f'{risk["id"]}: Risk description is blank.'
            )

        if not risk["owner"]:
            raise ValueError(
                f'{risk["id"]}: Risk owner is blank.'
            )

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

        try:
            expected = ratings[risk["probability"]][risk["severity"]]
        except KeyError as error:
            raise ValueError(
                f'{risk["id"]}: Missing matrix rating for '
                f'{risk["probability"]} / {risk["severity"]}.'
            ) from error

        if risk["rating"] != expected:
            raise ValueError(
                f'{risk["id"]}: Register rating is {risk["rating"]}, '
                f'but the configured matrix calculates {expected}.'
            )


def make_risk_register(config, risks, add_header):
    style = config["style"]
    columns = config["register"]["columns"]

    register_height = max(
        style["register_min_height"],
        len(risks) * style["register_row_height"]
        + style["register_extra_height"]
    )

    fig, ax = plt.subplots(
        figsize=(
            style["register_figure_width"],
            register_height
        )
    )

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

    for column in columns.values():
        ax.text(
            column["x"],
            style["register_heading_y"],
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

    fig.subplots_adjust(
        left=style["register_left"],
        right=style["register_right"],
        top=style["register_top"],
        bottom=style["register_bottom"]
    )

    return fig
