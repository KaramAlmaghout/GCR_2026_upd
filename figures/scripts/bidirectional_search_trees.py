from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle


FIGSIZE = (6.7, 3.8)
LW = 1.55
MS = 3.7
FONT = 11


def configure(ax):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-0.05, 8.10)
    ax.set_ylim(0.05, 4.45)


def edge(ax, p, q, color="0.45", lw=1.55, ls="-"):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, ls=ls, zorder=1)


def arrow(ax, p, q, text=None, text_xy=None, color="0.18", lw=0.9, ms=8, ls="-"):
    ax.add_patch(
        FancyArrowPatch(
            p,
            q,
            arrowstyle="-|>",
            mutation_scale=ms,
            lw=lw,
            linestyle=ls,
            color=color,
            shrinkA=2,
            shrinkB=2,
            zorder=3,
        )
    )
    if text is not None:
        xy = text_xy if text_xy is not None else (0.5 * (p[0] + q[0]), 0.5 * (p[1] + q[1]))
        ax.text(xy[0], xy[1], text, ha="center", va="center")


def cable_icon(ax, center, scale=0.18, color="0.15", filled=True, bend=0.0, label=None, label_xy=None):
    x = np.linspace(-1.0, 1.0, 5)
    y = 0.18 * np.sin(np.linspace(0.0, np.pi, 5)) + bend * np.sin(np.linspace(0.0, 2.0 * np.pi, 5))
    pts = np.column_stack((x, y)) * scale + np.asarray(center)
    marker_face = color if filled else "white"
    ax.plot(
        pts[:, 0],
        pts[:, 1],
        color=color,
        lw=LW,
        marker="o",
        ms=MS,
        mfc=marker_face,
        mec=color,
        zorder=4,
    )
    if label is not None:
        xy = label_xy if label_xy is not None else (center[0], center[1] - 0.34)
        ax.text(xy[0], xy[1], label, ha="center", va="top")


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

    ax.add_patch(Rectangle((0.06, 0.20), 7.92, 4.02, facecolor="0.985", edgecolor="0.72", lw=1.0))
    ax.text(0.24, 4.00, r"two trees of cable configurations", ha="left", va="top")
    for xy, wh in [((3.10, 2.75), (0.75, 0.55)), ((3.95, 1.32), (0.85, 0.60))]:
        ax.add_patch(Rectangle(xy, wh[0], wh[1], facecolor="0.78", edgecolor="0.25", lw=1.5))
    ax.add_patch(Circle((5.35, 3.05), 0.29, facecolor="0.70", edgecolor="0.25", lw=1.5))

    start = (0.78, 1.72)
    cnew = (4.02, 2.28)
    goal = (7.37, 2.00)
    cconn = (4.64, 2.24)
    start_tree = {
        "root": start,
        "s1": (1.38, 2.70),
        "s2": (1.48, 0.98),
        "s3": (2.18, 3.18),
        "s4": (2.34, 2.24),
        "s5": (2.50, 0.66),
        "s6": (3.05, 2.80),
        "s7": (3.28, 2.00),
        "new": cnew,
    }
    goal_tree = {
        "root": goal,
        "g1": (6.72, 2.85),
        "g2": (6.56, 1.36),
        "g3": (6.00, 3.55),
        "g4": (5.90, 2.42),
        "g5": (5.88, 0.88),
        "g6": (5.35, 3.58),
        "g7": (5.24, 2.08),
        "conn": cconn,
    }
    start_edges = [
        ("root", "s1"),
        ("root", "s2"),
        ("s1", "s3"),
        ("s1", "s4"),
        ("s2", "s5"),
        ("s4", "s6"),
        ("s4", "s7"),
        ("s7", "new"),
    ]
    goal_edges = [
        ("root", "g1"),
        ("root", "g2"),
        ("g1", "g3"),
        ("g1", "g4"),
        ("g2", "g5"),
        ("g4", "g6"),
        ("g4", "g7"),
        ("g7", "conn"),
    ]

    for parent, child in start_edges:
        edge(ax, start_tree[parent], start_tree[child], color="0.25")
    for parent, child in goal_edges:
        edge(ax, goal_tree[parent], goal_tree[child], color="0.55")
    edge(ax, cnew, cconn, color="0.08", lw=2.7, ls="--")

    cable_icon(ax, start, color="0.12", filled=True, bend=0.00, label=r"$C_{\mathrm{start}}$", label_xy=(0.78, 1.48))
    for c, b in [
        (start_tree["s1"], 0.08),
        (start_tree["s2"], -0.05),
        (start_tree["s3"], 0.04),
        (start_tree["s4"], -0.04),
        (start_tree["s5"], 0.06),
        (start_tree["s6"], 0.02),
        (start_tree["s7"], -0.06),
        (cnew, -0.08),
    ]:
        cable_icon(ax, c, scale=0.19, color="0.12", filled=True, bend=b)
    cable_icon(ax, goal, color="0.45", filled=False, bend=0.00, label=r"$C_{\mathrm{goal}}$", label_xy=(7.46, 2.42))
    for c, b in [
        (goal_tree["g1"], -0.04),
        (goal_tree["g2"], 0.06),
        (goal_tree["g3"], -0.06),
        (goal_tree["g4"], 0.05),
        (goal_tree["g5"], -0.02),
        (goal_tree["g6"], 0.04),
        (goal_tree["g7"], -0.05),
        (cconn, 0.05),
    ]:
        cable_icon(ax, c, scale=0.19, color="0.45", filled=False, bend=b)

    ax.text(1.50, 0.42, r"start tree $T_s$", ha="center", va="bottom")
    ax.text(6.30, 0.42, r"goal tree $T_g$", ha="center", va="bottom")
    ax.text(4.36, 2.42, r"$C_{\mathrm{conn}}$", ha="center", va="bottom")

    out = Path(__file__).resolve().parents[1] / "bidirectional_search_trees.pdf"
    fig.savefig(out, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


if __name__ == "__main__":
    main()
