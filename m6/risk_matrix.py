import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def make_risk_matrix(config, risks, add_header):
    style = config["style"]
    matrix = config["matrix"]
    probabilities = matrix["probabilities"]
    severities = matrix["severities"]

    # Wider figure provides room for horizontal margins.
    fig = plt.figure(figsize=(10, 8))

    add_header(
        fig,
        config["project"]["matrix_title"],
        config["project"]["subtitle"],
        config
    )

    # Keep the matrix square and centered.
    matrix_size = 0.68
    matrix_left = (1.0 - matrix_size) / 2.0

    ax = fig.add_axes([
        matrix_left,
        0.18,
        matrix_size,
        matrix_size
    ])

    ax.set_xlim(0, len(severities))
    ax.set_ylim(0, len(probabilities))
    ax.invert_yaxis()
    ax.set_aspect("equal", adjustable="box")

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

    return fig
