from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle


FIGSIZE = (4.8, 3.15)
BIG_FIGSIZE = (3.70, 1.85)
LW = 2.05
MS = 4.6
FONT = 9
BLUE = "#1f77b4"
ORANGE = "#d95f02"
GREEN = "#009e73"
PURPLE = "#6a3d9a"
PANEL_FILL = "#f7fbff"
PANEL_EDGE = "#9bb6c8"


def configure(ax, xlim=(-0.1, 6.55), ylim=(-0.15, 4.15)):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)


def panel(ax, xy, wh, title=None):
    x, y = xy
    w, h = wh
    ax.add_patch(Rectangle((x, y), w, h, facecolor=PANEL_FILL, edgecolor=PANEL_EDGE, lw=1.0))


def draw_cable(ax, pts, label=None, color=BLUE, ls="-", marker_face=None, lw=LW, label_xy=None):
    kwargs = {"color": color, "lw": lw, "ls": ls, "marker": "o", "ms": MS}
    if marker_face is not None:
        kwargs["mfc"] = marker_face
    ax.plot(pts[:, 0], pts[:, 1], **kwargs)
    if label is not None:
        if label_xy is None:
            label_xy = (pts[:, 0].mean(), pts[:, 1].min() - 0.15)
        ax.text(label_xy[0], label_xy[1], label, color=color, ha="center", va="center")


def arrow(ax, p, q, text=None, text_xy=None, color=GREEN, lw=1.2, ms=11, both=False):
    ax.add_patch(
        FancyArrowPatch(
            p,
            q,
            arrowstyle="<->" if both else "-|>",
            mutation_scale=ms,
            lw=lw,
            color=color,
            shrinkA=1,
            shrinkB=1,
        )
    )
    if text is not None:
        xy = text_xy if text_xy is not None else (0.5 * (p[0] + q[0]), 0.5 * (p[1] + q[1]))
        ax.text(xy[0], xy[1], text, color=color, ha="center", va="center")


def cable_shape(center, scale=1.0, bend=0.0, tilt=0.0):
    x = np.linspace(-1.0, 1.0, 5)
    y = 0.14 * np.sin(np.linspace(0.0, np.pi, 5)) + bend * np.sin(np.linspace(0.0, 2.0 * np.pi, 5))
    pts = np.column_stack((x, y)) * scale
    rot = np.array([[np.cos(tilt), -np.sin(tilt)], [np.sin(tilt), np.cos(tilt)]])
    return pts @ rot.T + np.asarray(center)


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

    panel(ax, (0.15, 2.35), (6.15, 1.42))
    ci = np.array([(0.78, 2.86), (1.44, 3.04), (2.12, 2.98), (2.78, 3.12), (3.46, 2.96)])
    cj = np.array([(1.02, 2.66), (1.72, 2.76), (2.42, 2.74), (3.10, 2.86), (3.86, 2.78)])
    ci[:, 0] += 0.65
    cj[:, 0] += 0.65
    draw_cable(ax, ci, r"$C_i$", color=BLUE, label_xy=(2.80, 3.25))
    draw_cable(ax, cj, r"$C_{i+1}$", color=ORANGE, ls="--", marker_face="white", lw=1.2, label_xy=(3.15, 2.50))

    imax = int(np.linalg.norm(cj - ci, axis=1).argmax())
    for idx in range(len(ci)):
        if idx == imax:
            arrow(ax, ci[idx], cj[idx], r"$d(C_i,C_{i+1})$", (4.78, 3.02), color=PURPLE, lw=1.1, ms=8, both=True)
        else:
            arrow(ax, ci[idx], cj[idx], color=GREEN, lw=0.9, ms=7, both=True)

    panel(ax, (0.15, 0.35), (6.15, 1.50))
    centers = [(0.75, 1.02), (2.05, 1.20), (3.35, 1.00), (4.65, 1.18), (5.72, 1.00)]
    bends = [0.00, 0.08, -0.06, 0.06, 0.00]
    tilts = [0.07, -0.04, 0.12, -0.10, 0.02]
    curves = [cable_shape(c, scale=0.34, bend=b, tilt=t) for c, b, t in zip(centers, bends, tilts)]
    for pts in curves:
        draw_cable(ax, pts, color=BLUE, lw=1.25)

    for i, (p, q) in enumerate(zip(centers[:-1], centers[1:])):
        arrow(ax, (p[0] + 0.40, p[1] + 0.08), (q[0] - 0.40, q[1] + 0.08), rf"$c_{i}$", (0.5 * (p[0] + q[0]), 1.42), color=GREEN, lw=0.85, ms=8)
    ax.text(5.10, 0.60, r"$J(\mathcal{P})=\sum_i c_i$", color=PURPLE, ha="center", va="center")

    print(save(fig, "configuration_distance_cost.pdf"))
    for out in (draw_edge_distance_split(), draw_accumulated_path_cost_split()):
        print(out)


def draw_edge_distance_split():
    fig, ax = plt.subplots(figsize=BIG_FIGSIZE)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    configure(ax, (0.0, 4.00), (0.0, 2.00))

    panel(ax, (0.15, 0.20), (3.70, 1.60))
    ci = np.array([(0.55, 1.26), (1.12, 1.47), (1.70, 1.38), (2.28, 1.57), (2.92, 1.36)])
    cj = np.array([(0.72, 0.86), (1.32, 1.00), (1.90, 0.92), (2.52, 1.10), (3.42, 0.95)])
    draw_cable(ax, ci, r"$C_i$", color=BLUE, label_xy=(1.82, 1.62))
    draw_cable(ax, cj, r"$C_{i+1}$", color=ORANGE, ls="--", marker_face="white", lw=1.75, label_xy=(2.02, 0.7))

    imax = int(np.linalg.norm(cj - ci, axis=1).argmax())
    for idx in range(len(ci)):
        if idx == imax:
            arrow(ax, ci[idx], cj[idx], r"$d(C_i,C_{i+1})$", (3.5, 1.25), color=PURPLE, lw=1.35, ms=12, both=True)
        else:
            arrow(ax, ci[idx], cj[idx], color=GREEN, lw=1.2, ms=11, both=True)

    return save(fig, "A_edge_distance.pdf", tight=False)


def draw_accumulated_path_cost_split():
    fig, ax = plt.subplots(figsize=BIG_FIGSIZE)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    configure(ax, (0.0, 4.00), (0.0, 2.00))

    panel(ax, (0.15, 0.20), (3.70, 1.60))
    centers = [(0.55, 0.98), (1.28, 1.18), (2.02, 0.96), (2.76, 1.14), (3.42, 0.98)]
    bends = [0.00, 0.08, -0.06, 0.06, 0.00]
    tilts = [0.07, -0.04, 0.12, -0.10, 0.02]
    curves = [cable_shape(c, scale=0.24, bend=b, tilt=t) for c, b, t in zip(centers, bends, tilts)]
    for pts in curves:
        draw_cable(ax, pts, color=BLUE, lw=1.85)

    for i, (p, q) in enumerate(zip(centers[:-1], centers[1:])):
        arrow(
            ax,
            (p[0] + 0.30, p[1] + 0.10),
            (q[0] - 0.30, q[1] + 0.10),
            rf"$c_{i}$",
            (0.5 * (p[0] + q[0]), 1.52),
            color=GREEN,
            lw=1.25,
            ms=11,
        )
    # ax.text(3.05, 0.48, r"$J(\mathcal{P})=\sum_i c_i$", color=PURPLE, ha="center", va="center")

    return save(fig, "B_accumulated_path_cost.pdf", tight=False)


if __name__ == "__main__":
    main()
