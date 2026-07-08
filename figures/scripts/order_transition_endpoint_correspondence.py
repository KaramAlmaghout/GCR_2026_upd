from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle


FIGSIZE = (5.1, 3.0)
LW = 1.55
MS = 3.5
FONT = 8


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
    ax.plot(a[:, 0], a[:, 1], color="0.15", lw=LW, marker="o", ms=MS)
    ax.plot(b[:, 0], b[:, 1], color="0.43", lw=LW, marker="o", ms=MS, mfc="white")
    ax.text(a[0, 0] - 0.1, a[0, 1] + 0.14, r"$p_1$", ha="right")
    ax.text(a[-1, 0] + 0.08, a[-1, 1] + 0.02, r"$p_N$", ha="left")
    ax.text(b[0, 0] - 0.1, b[0, 1] - 0.18, r"$q_1$", ha="right")
    ax.text(b[-1, 0] + 0.08, b[-1, 1] - 0.12, r"$q_N$", ha="left")


def local_sweep(ax, a, b):
    envelope = np.vstack((a, b[::-1]))
    ax.add_patch(
        Polygon(
            envelope,
            closed=True,
            facecolor="0.75",
            edgecolor="0.52",
            lw=0.6,
            alpha=0.45,
        )
    )


def crossed_sweep(ax, a, b):
    ax.plot([a[0, 0], b[-1, 0]], [a[0, 1], b[-1, 1]], color="0.25", lw=2.2, alpha=0.28)
    ax.plot([a[-1, 0], b[0, 0]], [a[-1, 1], b[0, 1]], color="0.25", lw=2.2, alpha=0.28)


def obstacle(ax, xy):
    ax.add_patch(Circle(xy, 0.15, facecolor="0.28", edgecolor="0.10", lw=1.0))


def draw_swapped_panel(ax, x0=0.12, rect=(0.00, 0.55, 3.55, 2.30), text=True):
    ax.add_patch(Rectangle(rect[:2], rect[2], rect[3], facecolor="0.985", edgecolor="0.75", lw=0.8))
    rect_center_x = rect[0] + 0.5 * rect[2]
    a, b = base_curves(x0)
    crossed_sweep(ax, a, b)
    draw_cables(ax, a, b)
    obstacle(ax, (x0 + 0.38, 1.75))
    ax.text(x0 + 2.78, 2.55, r"$\Gamma=1$", ha="center")
    if text:
        ax.text(rect_center_x, 3.08, "swapped endpoints", ha="center")
        ax.text(rect_center_x, 0.22, "X-shaped sweep misses obstacle", ha="center")


def draw_preserved_panel(ax, x0=3.82, rect=(3.66, 0.55, 3.55, 2.30), text=True):
    ax.add_patch(Rectangle(rect[:2], rect[2], rect[3], facecolor="0.985", edgecolor="0.75", lw=0.8))
    rect_center_x = rect[0] + 0.5 * rect[2]
    a, b = base_curves(x0)
    local_sweep(ax, a, b)
    draw_cables(ax, a, b)
    obstacle(ax, (x0 + 0.38, 1.75))
    ax.text(x0 + 2.78, 2.55, r"$\Gamma=0$", ha="center")
    if text:
        ax.text(rect_center_x, 3.08, "preserved endpoints", ha="center")
        ax.text(rect_center_x, 0.22, "local sweep intersects obstacle", ha="center")


def save(fig, filename, tight=True):
    out = Path(__file__).resolve().parents[1] / filename
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
