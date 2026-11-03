#!/usr/bin/env python3

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt

from risk_matrix import make_risk_matrix
from swot import read_swot, make_swot
from risk_register import read_risks, validate_risks, make_risk_register


def load_config(filename):
    with open(filename, "r", encoding="utf-8") as file:
        config = json.load(file)

    required = [
        "source",
        "project",
        "matrix",
        "swot",
        "register",
        "style",
        "output",
    ]

    for key in required:
        if key not in config:
            raise ValueError(f"Missing configuration section: {key}")

    return config


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

        risks = read_risks(config)
        swot = read_swot(config)

        validate_risks(risks, config)

        apply_style(config)

        save_figure(
            make_risk_matrix(config, risks, add_header),
            config["output"]["risk_matrix"],
            config
        )

        save_figure(
            make_swot(config, swot, add_header),
            config["output"]["swot"],
            config
        )

        save_figure(
            make_risk_register(config, risks, add_header),
            config["output"]["risk_register"],
            config
        )

    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        IndexError,
    ) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
