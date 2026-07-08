from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle


FIGSIZE = (5.1, 3.0)
LW = 2.05
MS = 4.6
FONT = 9
BLUE = "#1f77b4"
ORANGE = "#d95f02"
PURPLE = "#6a3d9a"
SWEEP_FILL = "#8fd19e"
CROSSED = "#6a3d9a"
RED = "#c44e52"
RED_EDGE = "#7f1d1d"
PANEL_FILL = "#f7fbff"
PANEL_EDGE = "#9bb6c8"


def configure(ax, xlim=(-0.30, 7.55), ylim=(-0.32, 3.75)):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)


def base_curves(x0):
    a = np.array(
        [
            (x0 + 0.32, 2.12),
            (x0 + 0.82, 2.30),
            (x0 + 1.34, 2.18),
            (x0 + 1.88, 2.32),
            (x0 + 2.42, 2.12),
            (x0 + 2.92, 1.88),
        ]
    )
    b = np.array(
        [
            (x0 + 0.44, 1.48),
            (x0 + 0.96, 1.40),
            (x0 + 1.50, 1.05),
            (x0 + 2.02, 1.56),
            (x0 + 2.50, 1.58),
            (x0 + 3.02, 1.42),
        ]
    )
    return a, b


def draw_cables(ax, a, b):
    ax.plot(a[:, 0], a[:, 1], color=BLUE, lw=LW, marker="o", ms=MS)
    ax.plot(b[:, 0], b[:, 1], color=ORANGE, lw=LW, marker="o", ms=MS, mfc="white")
    ax.text(a[0, 0] - 0.1, a[0, 1] + 0.14, r"$p_1$", color=BLUE, ha="right")
    ax.text(a[-1, 0] + 0.08, a[-1, 1] + 0.02, r"$p_N$", color=BLUE, ha="left")
    ax.text(b[0, 0] - 0.1, b[0, 1] - 0.18, r"$q_1$", color=ORANGE, ha="right")
    ax.text(b[-1, 0] + 0.08, b[-1, 1] - 0.12, r"$q_N$", color=ORANGE, ha="left")


def local_sweep(ax, a, b):
    envelope = np.vstack((a, b[::-1]))
    ax.add_patch(
        Polygon(
            envelope,
            closed=True,
            facecolor=SWEEP_FILL,
            edgecolor="#2ca25f",
            lw=0.9,
            alpha=0.45,
        )
    )


def crossed_sweep(ax, a, b):
    ax.plot([a[0, 0], b[-1, 0]], [a[0, 1], b[-1, 1]], color=CROSSED, lw=2.6, alpha=0.28)
    ax.plot([a[-1, 0], b[0, 0]], [a[-1, 1], b[0, 1]], color=CROSSED, lw=2.6, alpha=0.28)


def obstacle(ax, xy):
    ax.add_patch(Circle(xy, 0.16, facecolor=RED, edgecolor=RED_EDGE, lw=1.1))


def draw_swapped_panel(ax, x0=0.12, rect=(0.00, 0.55, 3.55, 2.30), text=True):
    ax.add_patch(Rectangle(rect[:2], rect[2], rect[3], facecolor=PANEL_FILL, edgecolor=PANEL_EDGE, lw=1.0))
    a, b = base_curves(x0)
    crossed_sweep(ax, a, b)
    draw_cables(ax, a, b)
    obstacle(ax, (x0 + 0.38, 1.75))


def draw_preserved_panel(ax, x0=3.82, rect=(3.66, 0.55, 3.55, 2.30), text=True):
    ax.add_patch(Rectangle(rect[:2], rect[2], rect[3], facecolor=PANEL_FILL, edgecolor=PANEL_EDGE, lw=1.0))
    a, b = base_curves(x0)
    local_sweep(ax, a, b)
    draw_cables(ax, a, b)
    obstacle(ax, (x0 + 0.38, 1.75))


def save(fig, filename, tight=True):
    path = Path(filename)
    out = Path(__file__).resolve().parents[1] / f"{path.stem}_colored{path.suffix}"
    if tight:
        fig.savefig(out, bbox_inches="tight", pad_inches=0.04)
    else:
        fig.savefig(out)
    plt.close(fig)
    return out


def draw_swapped_endpoints_split():
    fig, ax = plt.subplots(figsize=(3.15, 1.85))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    configure(ax, (-0.02, 3.68), (0.66, 2.90))
    draw_swapped_panel(ax, rect=(0.12, 0.76, 3.45, 2.04), text=False)
    return save(fig, "A_swapped_endpoints.pdf", tight=False)


def draw_preserved_endpoints_split():
    fig, ax = plt.subplots(figsize=(3.15, 1.85))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    configure(ax, (3.70, 7.48), (0.66, 2.90))
    draw_preserved_panel(ax, rect=(3.82, 0.76, 3.55, 2.04), text=False)
    return save(fig, "B_preserved_endpoints.pdf", tight=False)


def main():
    plt.rcParams.update(
        {
            "font.size": FONT,
            "font.family": "DejaVu Sans",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    fig, ax = plt.subplots(figsize=FIGSIZE)
    configure(ax)

    draw_swapped_panel(ax)
    draw_preserved_panel(ax)

    print(save(fig, "order_transition_endpoint_correspondence.pdf"))
    for out in (draw_swapped_endpoints_split(), draw_preserved_endpoints_split()):
        print(out)


if __name__ == "__main__":
    main()
