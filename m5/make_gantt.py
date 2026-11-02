#!/usr/bin/env python3

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
from openpyxl import load_workbook


def load_config(config_path):
    """Load JSON configuration and resolve paths relative to it."""

    config_path = Path(config_path).expanduser().resolve()

    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    base_directory = config_path.parent

    workbook_path = Path(config["workbook"]).expanduser()
    if not workbook_path.is_absolute():
        workbook_path = base_directory / workbook_path

    output_directory = Path(config["chart"]["output_directory"]).expanduser()
    if not output_directory.is_absolute():
        output_directory = base_directory / output_directory

    config["_workbook_path"] = workbook_path.resolve()
    config["_output_directory"] = output_directory.resolve()

    return config


def normalize_date(value, description):
    """Convert Excel date values into Python date objects."""

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    raise ValueError(
        f"Invalid {description}: {value!r}. "
        "Expected an Excel date cell."
    )


def normalize_phase(phase):
    """Remove an existing numeric prefix from a phase name."""

    phase = str(phase).strip()
    return re.sub(r"^\s*\d+\.\s*", "", phase)


def read_schedule(config):
    """Read project phases and team assignments from Excel."""

    workbook_path = config["_workbook_path"]

    if not workbook_path.is_file():
        raise FileNotFoundError(f"Excel workbook not found: {workbook_path}")

    workbook = load_workbook(workbook_path, data_only=True)

    try:
        worksheet_name = config["worksheet"]

        if worksheet_name not in workbook.sheetnames:
            raise ValueError(
                f"Worksheet {worksheet_name!r} not found. "
                f"Available worksheets: {', '.join(workbook.sheetnames)}"
            )

        worksheet = workbook[worksheet_name]

        columns = config["columns"]
        first_row = config["first_data_row"]

        schedule = []

        for row_number in range(first_row, worksheet.max_row + 1):
            phase = worksheet[f'{columns["phase"]}{row_number}'].value
            start = worksheet[f'{columns["start_date"]}{row_number}'].value
            end = worksheet[f'{columns["end_date"]}{row_number}'].value

            teams_column = columns.get("teams")
            teams = (
                worksheet[f'{teams_column}{row_number}'].value
                if teams_column else None
            )

            # Ignore completely blank rows.
            if phase is None and start is None and end is None:
                continue

            if not phase or start is None or end is None:
                raise ValueError(
                    f"Incomplete schedule entry on worksheet row {row_number}."
                )

            start = normalize_date(start, f"start date on row {row_number}")
            end = normalize_date(end, f"end date on row {row_number}")

            if end < start:
                raise ValueError(
                    f"End date precedes start date on row {row_number}."
                )

            schedule.append({
                "phase": normalize_phase(phase),
                "start": start,
                "end": end,
                "teams": str(teams).strip() if teams else "",
                "duration": (end - start).days + 1
            })

    finally:
        workbook.close()

    if not schedule:
        raise ValueError("No project schedule entries were found.")

    return schedule


def get_bar_label(item, label_type):
    """Build the text displayed inside a Gantt bar."""

    if label_type == "phase":
        return item["phase"]

    if label_type == "teams":
        return item["teams"]

    if label_type == "phase_and_teams":
        if item["teams"]:
            return f'{item["phase"]}\n{item["teams"]}'
        return item["phase"]

    if label_type == "none":
        return ""

    raise ValueError(
        f"Invalid bar_label setting: {label_type!r}. "
        "Use phase, teams, phase_and_teams, or none."
    )


def text_width(renderer, text, font_properties):
    """Return the rendered width of text in pixels."""

    width, _, _ = renderer.get_text_width_height_descent(
        text,
        font_properties,
        ismath=False
    )
    return width


def wrap_paragraph(paragraph, max_width, renderer, font_properties):
    """Wrap a paragraph to fit an actual rendered pixel width."""

    words = paragraph.split()

    if not words:
        return [""]

    lines = []
    current_line = ""

    for word in words:
        candidate = f"{current_line} {word}".strip()

        if text_width(renderer, candidate, font_properties) <= max_width:
            current_line = candidate
            continue

        if current_line:
            lines.append(current_line)
            current_line = ""

        # Split individual words that are wider than the bar.
        remaining = word

        while remaining:
            if text_width(renderer, remaining, font_properties) <= max_width:
                current_line = remaining
                remaining = ""
            else:
                fitting = ""

                for character in remaining:
                    candidate = fitting + character

                    if text_width(renderer, candidate, font_properties) > max_width:
                        break

                    fitting = candidate

                if not fitting:
                    fitting = remaining[0]

                lines.append(fitting)
                remaining = remaining[len(fitting):]

    if current_line:
        lines.append(current_line)

    return lines


def wrap_bar_label(label, max_width, renderer, font_properties):
    """Wrap all paragraphs in a bar label to the available width."""

    lines = []

    for paragraph in label.split("\n"):
        lines.extend(
            wrap_paragraph(
                paragraph,
                max_width,
                renderer,
                font_properties
            )
        )

    return "\n".join(lines)


def generate_chart(config, schedule):
    """Generate the configured Gantt chart and save requested formats."""

    settings = config["chart"]

    phases = [item["phase"] for item in schedule]
    starts = [item["start"] for item in schedule]

    colors = settings["colors"]

    bar_label = settings.get("bar_label", "none")
    label_fontsize = settings.get("bar_label_fontsize", 8)
    label_color = settings.get("bar_label_color", "white")
    show_phase_axis_labels = settings.get("show_phase_axis_labels", True)
    number_phases = settings.get("number_phases", False)

    time_scale = settings.get("time_scale", "months").lower()

    if not colors:
        raise ValueError("At least one bar color must be configured.")

    if time_scale not in ("months", "weeks"):
        raise ValueError(
            "Invalid time_scale setting. Use 'months' or 'weeks'."
        )

    if label_fontsize <= 0:
        raise ValueError("bar_label_fontsize must be greater than zero.")

    figure, axis = plt.subplots(
        figsize=(
            settings["figure_width"],
            settings["figure_height"]
        )
    )

    positions = list(range(len(schedule)))

    # Draw the bars first.
    for index, item in enumerate(schedule):
        start_number = mdates.date2num(item["start"])

        axis.barh(
            index,
            item["duration"],
            left=start_number,
            height=settings["bar_height"],
            color=colors[index % len(colors)],
            edgecolor="black"
        )

    axis.set_yticks(positions)

    if show_phase_axis_labels:
        if number_phases:
            phase_labels = [
                f"{index + 1}. {phase}"
                for index, phase in enumerate(phases)
            ]
        else:
            phase_labels = phases

        axis.set_yticklabels(phase_labels)
        axis.set_ylabel("Project Phase")
    else:
        axis.set_yticklabels([])
        axis.set_ylabel("")

    axis.invert_yaxis()

    axis.set_title(
        settings["title"],
        fontsize=16,
        fontweight="bold",
        pad=20
    )

    if settings.get("subtitle"):
        axis.text(
            0.5,
            1.02,
            settings["subtitle"],
            transform=axis.transAxes,
            ha="center",
            fontsize=10
        )

    earliest = min(starts)
    latest = max(item["end"] for item in schedule)

    axis.set_xlim(
        mdates.date2num(earliest) - 2,
        mdates.date2num(latest + timedelta(days=2))
    )

    # Configure the date axis.
    if time_scale == "months":
        axis.xaxis.set_major_locator(mdates.MonthLocator())
    else:
        axis.xaxis.set_major_locator(
            mdates.WeekdayLocator(
                byweekday=mdates.MO,
                interval=1
            )
        )

    axis.xaxis.set_major_formatter(
        mdates.DateFormatter(settings["date_format"])
    )

    if settings["show_grid"]:
        axis.grid(
            axis="x",
            linestyle="--",
            alpha=0.5
        )

    axis.set_axisbelow(True)
    axis.set_xlabel("Project Timeline")

    # Establish the final axis dimensions before measuring label widths.
    figure.tight_layout()
    figure.canvas.draw()

    renderer = figure.canvas.get_renderer()
    font_properties = FontProperties(
        size=label_fontsize,
        weight="bold"
    )

    # Add labels using the actual rendered width of each bar.
    for index, item in enumerate(schedule):
        label = get_bar_label(item, bar_label)

        if not label:
            continue

        start_number = mdates.date2num(item["start"])
        end_number = mdates.date2num(item["end"] + timedelta(days=1))

        left_pixel = axis.transData.transform(
            (start_number, index)
        )[0]

        right_pixel = axis.transData.transform(
            (end_number, index)
        )[0]

        # Leave a small margin inside each bar.
        available_width = max(1, right_pixel - left_pixel - 12)

        wrapped_label = wrap_bar_label(
            label,
            available_width,
            renderer,
            font_properties
        )

        axis.text(
            start_number + item["duration"] / 2,
            index,
            wrapped_label,
            ha="center",
            va="center",
            color=label_color,
            fontsize=label_fontsize,
            fontweight="bold"
        )

    output_directory = config["_output_directory"]
    output_directory.mkdir(parents=True, exist_ok=True)

    basename = settings["output_basename"]

    for output_format in settings["output_formats"]:
        output_format = output_format.lower().lstrip(".")

        if output_format not in ("png", "pdf"):
            raise ValueError(
                f"Unsupported output format: {output_format}"
            )

        output_path = output_directory / f"{basename}.{output_format}"

        figure.savefig(
            output_path,
            format=output_format,
            dpi=settings["dpi"],
            bbox_inches="tight"
        )

        print(f"Created: {output_path}")

    plt.close(figure)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Gantt chart from an Excel project schedule."
    )

    parser.add_argument(
        "config",
        help="Path to the JSON configuration file."
    )

    args = parser.parse_args()

    try:
        config = load_config(args.config)
        schedule = read_schedule(config)
        generate_chart(config, schedule)

    except (
        FileNotFoundError,
        KeyError,
        ValueError,
        json.JSONDecodeError
    ) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

