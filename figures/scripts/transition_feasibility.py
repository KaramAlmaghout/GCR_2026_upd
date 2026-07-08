from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle


FIGSIZE = (4.5, 3.0)
LW = 1.7
MS = 3.7
FONT = 8


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
            lw=0.6,
            alpha=0.45,
        )
    )


def cable(ax, pts, label, color, yoff=0.0, xoff=-0.04):
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=LW, marker="o", ms=MS)
    ax.text(pts[0, 0] + xoff, pts[0, 1] + yoff, label, ha="right", va="center")


def panel(ax, y0, blocked=False, rect=(0.10, 5.90, 1.45), rect_yoff=-0.08):
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

    rect_x, rect_w, rect_h = rect
    ax.add_patch(Rectangle((rect_x, y0 + rect_yoff), rect_w, rect_h, facecolor="0.985", edgecolor="0.75", lw=0.8))
    swept_region(ax, a, b, "0.78" if blocked else "0.84", "0.55")
    cable(ax, a, r"$C^a$", "0.15", yoff=0.12)
    cable(ax, b, r"$C^b$", "0.42", yoff=-0.10, xoff=-0.14)

    if blocked:
        obstacle = Circle((2.95, y0 + 0.59), 0.18, facecolor="0.28", edgecolor="0.10", lw=1.0)
        ax.add_patch(obstacle)
        # ax.plot([2.78, 3.12], [y0 + 0.42, y0 + 0.76], color="0.05", lw=1.2)
        # ax.plot([3.12, 2.78], [y0 + 0.42, y0 + 0.76], color="0.05", lw=1.2)
        ax.text(4.85, y0 + 1.04, r"$\chi_{\mathrm{sw}}=0$", ha="center")
        ax.text(4.85, y0 + 0.58, "obstacle inside\nswept region", ha="center")
    else:
        ax.add_patch(Circle((2.95, y0 + 0.15), 0.17, facecolor="0.28", edgecolor="0.10", lw=1.0))
        ax.text(4.85, y0 + 1.04, r"$\chi_{\mathrm{sw}}=1$", ha="center")
        ax.text(4.85, y0 + 0.58, "swept region\nis clear", ha="center")


def save(fig, filename, tight=True):
    out = Path(__file__).resolve().parents[1] / filename
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
    ax.text(1.9, 3.48, "swept envelope", ha="center")
    ax.text(1.9, 1.75, "same test with collision", ha="center")

    print(save(fig, "transition_feasibility.pdf"))
    for out in (draw_swept_region_clear_split(), draw_swept_region_blocked_split()):
        print(out)


def draw_swept_region_clear_split():
    fig, ax = plt.subplots(figsize=(4.25, 1.28))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    configure(ax, (-0.10, 6.05), (1.90, 3.55))
    panel(ax, 2.10, blocked=False, rect=(0.05, 5.85, 1.45), rect_yoff=-0.08)
    return save(fig, "A_swept_region_clear.pdf", tight=False)


def draw_swept_region_blocked_split():
    fig, ax = plt.subplots(figsize=(4.25, 1.28))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    configure(ax, (-0.10, 6.05), (0.15, 1.80))
    panel(ax, 0.35, blocked=True, rect=(0.05, 5.85, 1.45), rect_yoff=-0.08)
    return save(fig, "B_swept_region_blocked.pdf", tight=False)


if __name__ == "__main__":
    main()
