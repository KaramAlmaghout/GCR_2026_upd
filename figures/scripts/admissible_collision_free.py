from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle


LW = 1.55
MS = 3.5
FONT = 7.5


def configure(ax, xlim, ylim):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)


def panel(ax, xy, wh, title=None):
    x, y = xy
    w, h = wh
    ax.add_patch(Rectangle((x, y), w, h, facecolor="0.985", edgecolor="0.72", lw=0.8))
    if title is not None:
        ax.text(x + 0.08, y + h - 0.12, title, ha="left", va="top", fontweight="bold")


def draw_cable(ax, pts, color="0.15", ls="-", marker_face=None, lw=LW):
    pts = np.asarray(pts)
    kwargs = {"color": color, "lw": lw, "ls": ls, "marker": "o", "ms": MS}
    if marker_face is not None:
        kwargs["mfc"] = marker_face
    ax.plot(pts[:, 0], pts[:, 1], **kwargs)


def arrow(ax, p, q, text=None, text_xy=None, color="0.15", both=False, lw=0.9, ms=8, shrink=1):
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
        ax.text(xy[0], xy[1], text, ha="center", va="center")


def tip_to_tip_arrow(ax, p, q, text, text_xy, color="0.08", lw=1.1, ms=9):
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
    ax.text(text_xy[0], text_xy[1], text, ha="center", va="center")


def draw_obstacle(ax, center, radius=0.2):
    ax.add_patch(Circle(center, radius, facecolor="0.35", edgecolor="0.12", lw=0.9))


def setup_style():
    plt.rcParams.update(
        {
            "font.size": FONT,
            "font.family": "DejaVu Sans",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def save(fig, filename):
    out = Path(__file__).resolve().parents[1] / filename
    fig.savefig(out, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    return out


def draw_accepted():
    fig, ax = plt.subplots(figsize=(4.8, 1.10))
    configure(ax, (-0.1, 6.55), (2.40, 3.60))

    panel(ax, (0.15, 2.44), (6.15, 1.05))
    ax.text(0.42, 3.27, r"inside $\mathcal{W}$, below $\delta_\ell$, no collision", ha="left")
    for c, r in [((4.90, 2.98), 0.20), ((5.56, 3.20), 0.16)]:
        draw_obstacle(ax, c, r)
    cref = np.array([(0.64, 2.78), (1.20, 2.96), (1.78, 2.90), (2.38, 3.05), (2.98, 2.88), (3.58, 2.98)])
    cand = np.array([(0.64, 2.68), (1.20, 2.84), (1.78, 2.78), (2.38, 2.92), (2.98, 2.76), (3.58, 2.87)])
    draw_cable(ax, cref, color="0.56", ls="--", marker_face="white", lw=1.15)
    draw_cable(ax, cand, color="0.12")
    ax.text(4.36, 2.52, r"$C\in\mathcal{C}_{\mathrm{free}}(C^{\mathrm{ref}})$", ha="center")

    return save(fig, "A_accepted.pdf")


def draw_deformation_bound_fails():
    fig, ax = plt.subplots(figsize=(2.95, 1.05))
    configure(ax, (0.05, 3.25), (0.50, 1.72))

    panel(ax, (0.15, 0.55), (3.00, 1.08))
    tail = np.array((0.64, 0.82))
    v_c = np.array((1.05, 0.12))
    v_cref = np.array((0.72, 0.62))
    arrow(ax, tail, tail + v_c, r"$C$", (1.22, 0.74), color="0.12", lw=1.1, shrink=0)
    arrow(ax, tail, tail + v_cref, r"$C^{\mathrm{ref}}$", (0.95, 1.30), color="0.52", shrink=0)
    delta_start = tail + v_c
    delta_end = tail + v_cref
    tip_to_tip_arrow(
        ax,
        delta_start,
        delta_end,
        r"$\|\Delta v_k\|>\delta_\ell$",
        (2.18, 1.10),
        color="0.08",
        lw=1.1,
        ms=9,
    )

    return save(fig, "B_deformation_bound_fails.pdf")


def draw_collision_fails():
    fig, ax = plt.subplots(figsize=(2.9, 1.20))
    configure(ax, (3.25, 6.40), (0.32, 1.72))

    panel(ax, (3.35, 0.39), (2.95, 1.20))
    obs_center = (4.77, 0.92)
    draw_obstacle(ax, obs_center, 0.27)
    coll = np.array([(3.72, 0.70), (4.20, 0.82), (4.74, 0.93), (5.25, 1.08), (5.76, 0.96)])
    draw_cable(ax, coll, color="0.15")
    ax.text(4.85, 0.45, r"$s_k(C)\cap\mathcal{O}\ne\emptyset$", ha="center")

    return save(fig, "C_collision_fails.pdf")


def draw_combined():
    fig, ax = plt.subplots(figsize=(4.8, 3.15))
    configure(ax, (-0.1, 6.55), (-0.1, 4.2))

    panel(ax, (0.15, 2.38), (6.15, 1.38), r"A  accepted")
    ax.text(0.42, 3.24, r"inside $\mathcal{W}$, below $\delta_\ell$, no collision", ha="left")
    for c, r in [((4.90, 2.98), 0.20), ((5.56, 3.20), 0.16)]:
        draw_obstacle(ax, c, r)
    cref = np.array([(0.64, 2.78), (1.20, 2.96), (1.78, 2.90), (2.38, 3.05), (2.98, 2.88), (3.58, 2.98)])
    cand = np.array([(0.64, 2.68), (1.20, 2.84), (1.78, 2.78), (2.38, 2.92), (2.98, 2.76), (3.58, 2.87)])
    draw_cable(ax, cref, color="0.56", ls="--", marker_face="white", lw=1.15)
    draw_cable(ax, cand, color="0.12")
    ax.text(4.36, 2.52, r"$C\in\mathcal{C}_{\mathrm{free}}(C^{\mathrm{ref}})$", ha="center")

    panel(ax, (0.15, 0.35), (3.00, 1.60), r"B  deformation bound fails")
    tail = np.array((0.64, 0.82))
    v_c = np.array((1.05, 0.12))
    v_cref = np.array((0.72, 0.62))
    arrow(ax, tail, tail + v_c, r"$C$", (1.22, 0.74), color="0.12", lw=1.1, shrink=0)
    arrow(ax, tail, tail + v_cref, r"$C^{\mathrm{ref}}$", (0.95, 1.30), color="0.52", shrink=0)
    delta_start = tail + v_c
    delta_end = tail + v_cref
    tip_to_tip_arrow(
        ax,
        delta_start,
        delta_end,
        r"$\|\Delta v_k\|>\delta_\ell$",
        (2.18, 1.10),
        color="0.08",
        lw=1.1,
        ms=9,
    )

    panel(ax, (3.35, 0.35), (2.95, 1.60), r"C  collision fails")
    obs_center = (4.77, 0.92)
    draw_obstacle(ax, obs_center, 0.27)
    coll = np.array([(3.72, 0.70), (4.20, 0.82), (4.74, 0.93), (5.25, 1.08), (5.76, 0.96)])
    draw_cable(ax, coll, color="0.15")
    ax.text(4.85, 0.45, r"$s_k(C)\cap\mathcal{O}\ne\emptyset$", ha="center")

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
