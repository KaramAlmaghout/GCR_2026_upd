from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle


FIGSIZE = (4.5, 3.0)
BIG_FIGSIZE = (3.15, 1.85)
LW = 2.05
MS = 4.6
FONT = 9
BLUE = "#1f77b4"
ORANGE = "#d95f02"
GREEN_FILL = "#8fd19e"
AMBER_FILL = "#f4c76b"
GREEN_EDGE = "#2ca25f"
AMBER_EDGE = "#c49000"
RED = "#c44e52"
RED_EDGE = "#7f1d1d"
PANEL_FILL = "#f7fbff"
PANEL_EDGE = "#9bb6c8"


def configure(ax, xlim=(-0.2, 6.2), ylim=(-0.2, 3.65)):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)


def swept_region(ax, a, b, facecolor, edgecolor):
    envelope = np.vstack((a, b[::-1]))
    ax.add_patch(
        Polygon(
            envelope,
            closed=True,
            facecolor=facecolor,
            edgecolor=edgecolor,
            lw=0.9,
            alpha=0.45,
        )
    )


def cable(ax, pts, label, color, yoff=0.0, xoff=-0.04):
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=LW, marker="o", ms=MS)
    ax.text(pts[0, 0] + xoff, pts[0, 1] + yoff, label, color=color, ha="right", va="center")


def panel(ax, y0, blocked=False, rect=(0.10, 5.90, 1.45), rect_yoff=-0.08):
    x_shift = 0.72
    a = np.array(
        [
            (0.55, y0 + 0.82),
            (1.15, y0 + 1.05),
            (1.82, y0 + 0.94),
            (2.48, y0 + 1.08),
            (3.12, y0 + 0.92),
            (3.78, y0 + 0.72),
        ]
    )
    b = np.array(
        [
            (0.70, y0 + 0.32),
            (1.25, y0 + 0.48),
            (1.90, y0 + 0.38),
            (2.55, y0 + 0.58),
            (3.18, y0 + 0.45),
            (3.86, y0 + 0.36),
        ]
    )
    a[:, 0] += x_shift
    b[:, 0] += x_shift

    rect_x, rect_w, rect_h = rect
    ax.add_patch(Rectangle((rect_x, y0 + rect_yoff), rect_w, rect_h, facecolor=PANEL_FILL, edgecolor=PANEL_EDGE, lw=1.0))
    swept_region(ax, a, b, AMBER_FILL if blocked else GREEN_FILL, AMBER_EDGE if blocked else GREEN_EDGE)
    cable(ax, a, r"$C^a$", BLUE, yoff=0.12)
    cable(ax, b, r"$C^b$", ORANGE, yoff=-0.10, xoff=-0.14)

    if blocked:
        obstacle = Circle((2.95 + x_shift, y0 + 0.59), 0.18, facecolor=RED, edgecolor=RED_EDGE, lw=1.0)
        ax.add_patch(obstacle)
    else:
        ax.add_patch(Circle((2.95 + x_shift, y0 + 0.15), 0.17, facecolor=RED, edgecolor=RED_EDGE, lw=1.0))


def compact_panel(ax, blocked=False):
    a = np.array(
        [
            (0.58, 1.36),
            (0.98, 1.58),
            (1.44, 1.48),
            (1.90, 1.62),
            (2.36, 1.43),
            (2.82, 1.22),
        ]
    )
    b = np.array(
        [
            (0.66, 0.72),
            (1.08, 0.92),
            (1.52, 0.82),
            (1.98, 1.06),
            (2.44, 0.92),
            (2.90, 0.78),
        ]
    )

    ax.add_patch(Rectangle((0.15, 0.20), 3.10, 1.60, facecolor=PANEL_FILL, edgecolor=PANEL_EDGE, lw=1.0))
    swept_region(ax, a, b, AMBER_FILL if blocked else GREEN_FILL, AMBER_EDGE if blocked else GREEN_EDGE)
    cable(ax, a, r"$C^a$", BLUE, yoff=0.14)
    cable(ax, b, r"$C^b$", ORANGE, yoff=-0.14, xoff=-0.14)

    center = (2.32, 1.02) if blocked else (2.32, 0.54)
    ax.add_patch(Circle(center, 0.20, facecolor=RED, edgecolor=RED_EDGE, lw=1.1))


def save(fig, filename, tight=True):
    path = Path(filename)
    out = Path(__file__).resolve().parents[1] / f"{path.stem}_colored{path.suffix}"
    if tight:
        fig.savefig(out, bbox_inches="tight", pad_inches=0.04)
    else:
        fig.savefig(out)
    plt.close(fig)
    return out


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
    panel(ax, 2.02, blocked=False)
    panel(ax, 0.28, blocked=True)

    print(save(fig, "transition_feasibility.pdf"))
    for out in (draw_swept_region_clear_split(), draw_swept_region_blocked_split()):
        print(out)


def draw_swept_region_clear_split():
    fig, ax = plt.subplots(figsize=BIG_FIGSIZE)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    configure(ax, (0.0, 3.40), (0.0, 2.00))
    compact_panel(ax, blocked=False)
    return save(fig, "A_swept_region_clear.pdf", tight=False)


def draw_swept_region_blocked_split():
    fig, ax = plt.subplots(figsize=BIG_FIGSIZE)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    configure(ax, (0.0, 3.40), (0.0, 2.00))
    compact_panel(ax, blocked=True)
    return save(fig, "B_swept_region_blocked.pdf", tight=False)


if __name__ == "__main__":
    main()
