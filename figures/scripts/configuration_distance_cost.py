from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle


FIGSIZE = (4.8, 3.15)
LW = 1.45
MS = 3.4
FONT = 7


def configure(ax, xlim=(-0.1, 6.55), ylim=(-0.15, 4.15)):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)


def panel(ax, xy, wh, title=None):
    x, y = xy
    w, h = wh
    ax.add_patch(Rectangle((x, y), w, h, facecolor="0.985", edgecolor="0.72", lw=0.8))
    if title is not None:
        ax.text(x + 0.08, y + h - 0.12, title, ha="left", va="top")


def draw_cable(ax, pts, label=None, color="0.15", ls="-", marker_face=None, lw=LW, label_xy=None):
    kwargs = {"color": color, "lw": lw, "ls": ls, "marker": "o", "ms": MS}
    if marker_face is not None:
        kwargs["mfc"] = marker_face
    ax.plot(pts[:, 0], pts[:, 1], **kwargs)
    if label is not None:
        if label_xy is None:
            label_xy = (pts[:, 0].mean(), pts[:, 1].min() - 0.15)
        ax.text(label_xy[0], label_xy[1], label, ha="center", va="center")


def arrow(ax, p, q, text=None, text_xy=None, color="0.32", lw=0.8, ms=7, both=False):
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
        ax.text(xy[0], xy[1], text, ha="center", va="center")


def cable_shape(center, scale=1.0, bend=0.0, tilt=0.0):
    x = np.linspace(-1.0, 1.0, 5)
    y = 0.14 * np.sin(np.linspace(0.0, np.pi, 5)) + bend * np.sin(np.linspace(0.0, 2.0 * np.pi, 5))
    pts = np.column_stack((x, y)) * scale
    rot = np.array([[np.cos(tilt), -np.sin(tilt)], [np.sin(tilt), np.cos(tilt)]])
    return pts @ rot.T + np.asarray(center)


def save(fig, filename):
    out = Path(__file__).resolve().parents[1] / filename
    fig.savefig(out, bbox_inches="tight", pad_inches=0.04)
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

    panel(ax, (0.15, 2.35), (6.15, 1.42), r"A  edge distance")
    ci = np.array([(0.78, 2.86), (1.44, 3.04), (2.12, 2.98), (2.78, 3.12), (3.46, 2.96)])
    cj = np.array([(1.02, 2.66), (1.72, 2.76), (2.42, 2.74), (3.10, 2.86), (3.86, 2.78)])
    draw_cable(ax, ci, r"$C_i$", color="0.13", label_xy=(2.15, 3.25))
    draw_cable(ax, cj, r"$C_{i+1}$", color="0.50", ls="--", marker_face="white", lw=1.2, label_xy=(2.50, 2.50))

    for idx in [0, 2, 4]:
        arrow(ax, ci[idx], cj[idx], color="0.60", lw=0.65, ms=6)
    imax = 4
    arrow(ax, ci[imax], cj[imax], color="0.08", lw=1.25, ms=8, both=True)
    ax.text(4.86, 3.18, r"$d(C_i,C_{i+1})$", ha="center")
    ax.text(4.86, 2.92, r"$=\max_n\|p_n^i-p_n^{i+1}\|$", ha="center")

    panel(ax, (0.15, 0.35), (6.15, 1.50), r"B  accumulated path cost")
    centers = [(0.75, 1.02), (2.05, 1.20), (3.35, 1.00), (4.65, 1.18), (5.72, 1.00)]
    labels = [r"$C_0$", r"$C_1$", r"$C_2$", r"$C_3$", r"$C_K$"]
    bends = [0.00, 0.08, -0.06, 0.06, 0.00]
    tilts = [0.07, -0.04, 0.12, -0.10, 0.02]
    curves = [cable_shape(c, scale=0.34, bend=b, tilt=t) for c, b, t in zip(centers, bends, tilts)]
    for pts, label in zip(curves, labels):
        draw_cable(ax, pts, label, color="0.15", lw=1.25)

    for i, (p, q) in enumerate(zip(centers[:-1], centers[1:])):
        arrow(ax, (p[0] + 0.40, p[1] + 0.08), (q[0] - 0.40, q[1] + 0.08), color="0.28", lw=0.85, ms=8)
        ax.text(0.5 * (p[0] + q[0]), 1.42, rf"$c_{i}$", ha="center", va="top")

    ax.text(2.66, 0.52, r"$c_i=d(C_i,C_{i+1})+\alpha_{\mathrm{def}}E_{\mathrm{def}}(C_{i+1},C_i)$", ha="center")
    ax.text(5.27, 0.52, r"$J(\mathcal{P})=\sum_i c_i$", ha="center")

    print(save(fig, "configuration_distance_cost.pdf"))
    for out in (draw_edge_distance_split(), draw_accumulated_path_cost_split()):
        print(out)


def draw_edge_distance_split():
    fig, ax = plt.subplots(figsize=(4.55, 1.42))
    configure(ax, (0.05, 6.40), (2.30, 3.72))

    panel(ax, (0.15, 2.36), (6.15, 1.26))
    ci = np.array([(0.78, 2.86), (1.44, 3.04), (2.12, 2.98), (2.78, 3.12), (3.46, 2.96)])
    cj = np.array([(1.02, 2.66), (1.72, 2.76), (2.42, 2.74), (3.10, 2.86), (3.86, 2.78)])
    draw_cable(ax, ci, r"$C_i$", color="0.13", label_xy=(2.15, 3.25))
    draw_cable(ax, cj, r"$C_{i+1}$", color="0.50", ls="--", marker_face="white", lw=1.2, label_xy=(2.50, 2.50))

    for idx in [0, 2, 4]:
        arrow(ax, ci[idx], cj[idx], color="0.60", lw=0.65, ms=6)
    imax = 4
    arrow(ax, ci[imax], cj[imax], color="0.08", lw=1.25, ms=8, both=True)
    ax.text(4.86, 3.18, r"$d(C_i,C_{i+1})$", ha="center")
    ax.text(4.86, 2.92, r"$=\max_n\|p_n^i-p_n^{i+1}\|$", ha="center")

    return save(fig, "A_edge_distance.pdf")


def draw_accumulated_path_cost_split():
    fig, ax = plt.subplots(figsize=(4.55, 1.25))
    configure(ax, (0.05, 6.40), (0.28, 1.70))

    panel(ax, (0.15, 0.35), (6.15, 1.22))
    centers = [(0.75, 1.02), (2.05, 1.20), (3.35, 1.00), (4.65, 1.18), (5.72, 1.00)]
    labels = [r"$C_0$", r"$C_1$", r"$C_2$", r"$C_3$", r"$C_K$"]
    bends = [0.00, 0.08, -0.06, 0.06, 0.00]
    tilts = [0.07, -0.04, 0.12, -0.10, 0.02]
    curves = [cable_shape(c, scale=0.34, bend=b, tilt=t) for c, b, t in zip(centers, bends, tilts)]
    for pts, label in zip(curves, labels):
        draw_cable(ax, pts, label, color="0.15", lw=1.25)

    for i, (p, q) in enumerate(zip(centers[:-1], centers[1:])):
        arrow(ax, (p[0] + 0.40, p[1] + 0.08), (q[0] - 0.40, q[1] + 0.08), color="0.28", lw=0.85, ms=8)
        ax.text(0.5 * (p[0] + q[0]), 1.42, rf"$c_{i}$", ha="center", va="top")

    ax.text(2.66, 0.52, r"$c_i=d(C_i,C_{i+1})+\alpha_{\mathrm{def}}E_{\mathrm{def}}(C_{i+1},C_i)$", ha="center")
    ax.text(5.27, 0.52, r"$J(\mathcal{P})=\sum_i c_i$", ha="center")

    return save(fig, "B_accumulated_path_cost.pdf")


if __name__ == "__main__":
    main()
