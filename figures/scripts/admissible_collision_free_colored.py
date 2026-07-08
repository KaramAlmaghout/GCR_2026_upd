from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle


LW = 2.05
MS = 4.6
FONT = 9
BIG_FIGSIZE = (3.70, 1.85)
SMALL_FIGSIZE = (3.15, 1.85)
BLUE = "#1f77b4"
ORANGE = "#d95f02"
PURPLE = "#6a3d9a"
RED = "#c44e52"
RED_EDGE = "#7f1d1d"
PANEL_FILL = "#f7fbff"
PANEL_EDGE = "#9bb6c8"


def configure(ax, xlim, ylim):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)


def panel(ax, xy, wh, title=None):
    x, y = xy
    w, h = wh
    ax.add_patch(Rectangle((x, y), w, h, facecolor=PANEL_FILL, edgecolor=PANEL_EDGE, lw=1.0))


def draw_cable(ax, pts, color=BLUE, ls="-", marker_face=None, lw=LW):
    pts = np.asarray(pts)
    kwargs = {"color": color, "lw": lw, "ls": ls, "marker": "o", "ms": MS}
    if marker_face is not None:
        kwargs["mfc"] = marker_face
    ax.plot(pts[:, 0], pts[:, 1], **kwargs)


def arrow(ax, p, q, text=None, text_xy=None, color=PURPLE, both=False, lw=1.25, ms=11, shrink=1):
    ax.add_patch(
        FancyArrowPatch(
            p,
            q,
            arrowstyle="<->" if both else "-|>",
            mutation_scale=ms,
            lw=lw,
            color=color,
            shrinkA=shrink,
            shrinkB=shrink,
        )
    )
    if text is not None:
        xy = text_xy if text_xy is not None else (0.5 * (p[0] + q[0]), 0.5 * (p[1] + q[1]))
        ax.text(xy[0], xy[1], text, color=color, ha="center", va="center")


def tip_to_tip_arrow(ax, p, q, text, text_xy, color=PURPLE, lw=1.35, ms=12):
    """Draw a double-headed difference marker with heads at both vector tips."""
    p = np.asarray(p)
    q = np.asarray(q)
    mid = 0.5 * (p + q)
    ax.add_patch(
        FancyArrowPatch(
            mid,
            p,
            arrowstyle="-|>",
            mutation_scale=ms,
            lw=lw,
            color=color,
            shrinkA=0,
            shrinkB=0,
            zorder=5,
        )
    )
    ax.text(text_xy[0], text_xy[1], text, color=color, ha="center", va="center")
    ax.add_patch(
        FancyArrowPatch(
            mid,
            q,
            arrowstyle="-|>",
            mutation_scale=ms,
            lw=lw,
            color=color,
            shrinkA=0,
            shrinkB=0,
            zorder=5,
        )
    )


def draw_obstacle(ax, center, radius=0.2):
    ax.add_patch(Circle(center, radius, facecolor=RED, edgecolor=RED_EDGE, lw=1.1))


def setup_style():
    plt.rcParams.update(
        {
            "font.size": FONT,
            "font.family": "DejaVu Sans",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def save(fig, filename, tight=True):
    path = Path(filename)
    out = Path(__file__).resolve().parents[1] / f"{path.stem}_colored{path.suffix}"
    if tight:
        fig.savefig(out, bbox_inches="tight", pad_inches=0.04)
    else:
        fig.savefig(out)
    plt.close(fig)
    return out


def draw_accepted():
    fig, ax = plt.subplots(figsize=BIG_FIGSIZE)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    configure(ax, (0.0, 4.00), (0.0, 2.00))

    panel(ax, (0.15, 0.20), (3.70, 1.60))
    for c, r in [((3.10, 0.92), 0.22), ((3.50, 1.22), 0.16)]:
        draw_obstacle(ax, c, r)
    cref = np.array([(0.62, 1.05), (1.07, 1.24), (1.52, 1.18), (1.98, 1.34), (2.44, 1.15), (2.80, 1.25)])
    cand = np.array([(0.62, 0.86), (1.07, 1.02), (1.52, 0.96), (1.98, 1.10), (2.44, 0.94), (2.80, 1.04)])
    draw_cable(ax, cref, color=ORANGE, ls="--", marker_face="white", lw=1.75)
    draw_cable(ax, cand, color=BLUE)
    ax.text(0.65, 1.14, r"$C^{\mathrm{ref}}$", color=ORANGE, ha="right", va="center")
    ax.text(0.51, 0.75, r"$C$", color=BLUE, ha="right", va="center")

    return save(fig, "A_accepted.pdf", tight=False)


def draw_deformation_bound_fails():
    fig, ax = plt.subplots(figsize=SMALL_FIGSIZE)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    configure(ax, (0.0, 3.40), (0.0, 2.00))

    panel(ax, (0.15, 0.20), (3.10, 1.60))
    tail = np.array((0.70, 0.82))
    v_c = np.array((1.05, 0.12))
    v_cref = np.array((0.72, 0.62))
    arrow(ax, tail, tail + v_c, r"$v_k(C)$", (1.22, 0.74), color=BLUE, lw=1.45, ms=12, shrink=0)
    arrow(ax, tail, tail + v_cref, r"$v_k(C^{\mathrm{ref}})$", (1.0, 1.34), color=ORANGE, lw=1.45, ms=12, shrink=0)
    delta_start = tail + v_c
    delta_end = tail + v_cref
    tip_to_tip_arrow(
        ax,
        delta_start,
        delta_end,
        r"$\|\Delta v_k\|>\delta_\ell$",
        (2.04, 1.2),
        color=PURPLE,
        lw=1.35,
        ms=12,
    )

    return save(fig, "B_deformation_bound_fails.pdf", tight=False)


def draw_collision_fails():
    fig, ax = plt.subplots(figsize=SMALL_FIGSIZE)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    configure(ax, (0.0, 3.40), (0.0, 2.00))

    panel(ax, (0.15, 0.20), (3.10, 1.60))
    obs_center = (1.72, 1.02)
    draw_obstacle(ax, obs_center, 0.27)
    coll = np.array([(0.65, 0.80), (1.18, 0.92), (1.70, 1.03), (2.22, 1.18), (2.75, 1.06)])
    draw_cable(ax, coll, color=BLUE)

    return save(fig, "C_collision_fails.pdf", tight=False)


def draw_combined():
    fig, ax = plt.subplots(figsize=(4.8, 3.15))
    configure(ax, (-0.1, 6.55), (-0.1, 4.2))

    panel(ax, (0.15, 2.38), (6.15, 1.38))
    for c, r in [((4.90, 2.98), 0.20), ((5.56, 3.20), 0.16)]:
        draw_obstacle(ax, c, r)
    cref = np.array([(0.64, 2.78), (1.20, 2.96), (1.78, 2.90), (2.38, 3.05), (2.98, 2.88), (3.58, 2.98)])
    cand = np.array([(0.64, 2.68), (1.20, 2.84), (1.78, 2.78), (2.38, 2.92), (2.98, 2.76), (3.58, 2.87)])
    draw_cable(ax, cref, color=ORANGE, ls="--", marker_face="white", lw=1.15)
    draw_cable(ax, cand, color=BLUE)
    ax.text(0.52, 2.86, r"$C^{\mathrm{ref}}$", color=ORANGE, ha="right", va="center")
    ax.text(0.52, 2.62, r"$C$", color=BLUE, ha="right", va="center")

    panel(ax, (0.15, 0.35), (3.00, 1.60))
    tail = np.array((0.64, 0.82))
    v_c = np.array((1.05, 0.12))
    v_cref = np.array((0.72, 0.62))
    arrow(ax, tail, tail + v_c, r"$v_k(C)$", (1.22, 0.74), color=BLUE, lw=1.1, shrink=0)
    arrow(ax, tail, tail + v_cref, r"$v_k(C^{\mathrm{ref}})$", (1.05, 1.34), color=ORANGE, shrink=0)
    delta_start = tail + v_c
    delta_end = tail + v_cref
    tip_to_tip_arrow(
        ax,
        delta_start,
        delta_end,
        r"$\|\Delta v_k\|>\delta_\ell$",
        (2.18, 1.10),
        color=PURPLE,
        lw=1.1,
        ms=9,
    )

    panel(ax, (3.35, 0.35), (2.95, 1.60))
    obs_center = (4.77, 0.92)
    draw_obstacle(ax, obs_center, 0.27)
    coll = np.array([(3.72, 0.70), (4.20, 0.82), (4.74, 0.93), (5.25, 1.08), (5.76, 0.96)])
    draw_cable(ax, coll, color=BLUE)

    return save(fig, "admissible_collision_free.pdf")


def main():
    setup_style()
    for out in (
        draw_combined(),
        draw_accepted(),
        draw_deformation_bound_fails(),
        draw_collision_fails(),
    ):
        print(out)


if __name__ == "__main__":
    main()
