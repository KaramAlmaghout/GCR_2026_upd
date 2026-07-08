from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle


FIGSIZE = (4.8, 3.05)
BIG_FIGSIZE = (3.70, 1.85)
SMALL_FIGSIZE = (3.15, 1.85)
LW = 2.05
MS = 4.6
FONT = 9
BLUE = "#1f77b4"
ORANGE = "#d95f02"
PURPLE = "#6a3d9a"
PANEL_FILL = "#f7fbff"
PANEL_EDGE = "#9bb6c8"


def configure(ax, xlim=(-0.15, 6.45), ylim=(-0.1, 4.05)):
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)


def panel(ax, xy, wh, title=None):
    x, y = xy
    w, h = wh
    ax.add_patch(Rectangle((x, y), w, h, facecolor=PANEL_FILL, edgecolor=PANEL_EDGE, lw=1.0))


def draw_cable(ax, pts, color=BLUE, ls="-", marker_face=None, lw=LW, zorder=2):
    kwargs = {"color": color, "lw": lw, "ls": ls, "marker": "o", "ms": MS, "zorder": zorder}
    if marker_face is not None:
        kwargs["mfc"] = marker_face
    ax.plot(pts[:, 0], pts[:, 1], **kwargs)


def arrow(ax, p, q, text=None, text_xy=None, color=PURPLE, lw=1.25, ms=11, both=False):
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
            zorder=6,
        )
    )
    if text is not None:
        xy = text_xy if text_xy is not None else (0.5 * (p[0] + q[0]), 0.5 * (p[1] + q[1]))
        ax.text(xy[0], xy[1], text, color=color, ha="center", va="center", zorder=7)


def offset_segment(p, q, amount):
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    v = q - p
    n = np.array([-v[1], v[0]], dtype=float)
    norm = np.linalg.norm(n)
    if norm == 0:
        return p, q
    n = amount * n / norm
    return p + n, q + n


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

    ca = np.array(
        [
            (0.55, 3.02),
            (1.18, 3.15),
            (1.86, 3.08),
            (2.54, 3.24),
            (3.20, 3.06),
            (3.88, 3.13),
        ]
    )
    cb = np.array(
        [
            (0.55, 2.63),
            (1.18, 2.86),
            (1.86, 2.70),
            (2.54, 2.98),
            (3.20, 2.80),
            (3.88, 2.92),
        ]
    )
    x_shift = 0.95
    ca[:, 0] += x_shift
    cb[:, 0] += x_shift

    panel(ax, (0.15, 2.25), (6.1, 1.55))
    draw_cable(ax, ca, color=BLUE)
    draw_cable(ax, cb, color=ORANGE, ls="--", marker_face="white", lw=1.25)
    ax.text(ca[0, 0] - 0.08, ca[0, 1] + 0.08, r"$C^a$", color=BLUE, ha="right")
    ax.text(cb[0, 0] - 0.08, cb[0, 1] - 0.15, r"$C^b$", color=ORANGE, ha="right")

    k = 2
    ax.plot(ca[k : k + 2, 0], ca[k : k + 2, 1], color=BLUE, lw=2.7)
    ax.plot(cb[k : k + 2, 0], cb[k : k + 2, 1], color=ORANGE, lw=2.2, ls="--")
    pa, qa = offset_segment(ca[k], ca[k + 1], 0.08)
    pb, qb = offset_segment(cb[k], cb[k + 1], -0.07)
    arrow(ax, pa, qa, r"$v_k(C^a)$", (2.18 + x_shift, 3.39), color=BLUE, lw=1.15)
    arrow(ax, pb, qb, r"$v_k(C^b)$", (2.24 + x_shift, 2.50), color=ORANGE, lw=1.15)

    panel(ax, (0.15, 0.35), (2.95, 1.45))
    tail = np.array((1.02, 0.83))
    va = np.array((0.98, 0.28))
    vb = np.array((0.76, 0.62))
    arrow(ax, tail, tail + va, r"$v_k(C^a)$", (1.52, 0.79), color=BLUE, lw=1.1)
    arrow(ax, tail, tail + vb, r"$v_k(C^b)$", (1.16, 1.34), color=ORANGE, lw=1.1)
    arrow(
        ax,
        tail + vb,
        tail + va,
        r"$\Delta v_k$",
        (2.17, 1.23),
        color=PURPLE,
        lw=1.0,
        both=True,
    )

    panel(ax, (3.30, 0.35), (2.95, 1.45))
    tri_a = np.array([(3.80, 0.78), (4.55, 1.34), (5.35, 0.92)])
    tri_b = np.array([(3.80, 0.70), (4.55, 0.98), (5.35, 0.82)])
    draw_cable(ax, tri_a, color=BLUE, lw=1.5)
    draw_cable(ax, tri_b, color=ORANGE, ls="--", marker_face="white", lw=1.15)
    arrow(ax, (4.55, 0.98), (4.55, 1.34), r"$\Delta b_k$", (4.90, 1.22), color=PURPLE, both=True)

    print(save(fig, "local_deformation_measures.pdf"))
    for out in (
        draw_segment_vector_split(),
        draw_segment_vector_change_split(),
        draw_bending_change_split(),
    ):
        print(out)


def draw_segment_vector_split():
    fig, ax = plt.subplots(figsize=BIG_FIGSIZE)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    configure(ax, (0.0, 4.00), (0.0, 2.00))

    ca = np.array(
        [
            (0.62, 1.28),
            (1.16, 1.42),
            (1.72, 1.34),
            (2.30, 1.54),
            (2.88, 1.34),
            (3.42, 1.44),
        ]
    )
    cb = np.array(
        [
            (0.62, 0.74),
            (1.16, 0.92),
            (1.72, 0.82),
            (2.30, 1.08),
            (2.88, 0.92),
            (3.42, 1.04),
        ]
    )

    panel(ax, (0.15, 0.20), (3.70, 1.60))
    draw_cable(ax, ca, color=BLUE)
    draw_cable(ax, cb, color=ORANGE, ls="--", marker_face="white", lw=1.75)
    ax.text(ca[0, 0] - 0.08, ca[0, 1] + 0.05, r"$C^a$", color=BLUE, ha="right")
    ax.text(cb[0, 0] - 0.08, cb[0, 1] - 0.14, r"$C^b$", color=ORANGE, ha="right")

    k = 2
    # ax.plot(ca[k : k + 2, 0], ca[k : k + 2, 1], color=BLUE, lw=3.1)
    # ax.plot(cb[k : k + 2, 0], cb[k : k + 2, 1], color=ORANGE, lw=2.7, ls="--")
    pa, qa = offset_segment(ca[k], ca[k + 1], 0.045)
    pb, qb = offset_segment(cb[k], cb[k + 1], -0.045)
    arrow(ax, pa, qa, r"$v_k(C^a)$", (1.90, 1.62), color=BLUE, lw=1.45, ms=12)
    arrow(ax, pb, qb, r"$v_k(C^b)$", (2.18, 0.76), color=ORANGE, lw=1.45, ms=12)

    return save(fig, "A_segment_vector.pdf", tight=False)


def draw_segment_vector_change_split():
    fig, ax = plt.subplots(figsize=SMALL_FIGSIZE)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    configure(ax, (0.0, 3.40), (0.0, 2.00))

    panel(ax, (0.15, 0.20), (3.10, 1.60))
    tail = np.array((1.15, 0.82))
    va = np.array((0.98, 0.28))
    vb = np.array((0.76, 0.62))
    arrow(ax, tail, tail + va, r"$v_k(C^a)$", (1.76, 0.80), color=BLUE, lw=1.45, ms=12)
    arrow(ax, tail, tail + vb, r"$v_k(C^b)$", (1.38, 1.32), color=ORANGE, lw=1.45, ms=12)
    arrow(
        ax,
        tail + vb,
        tail + va,
        r"$\Delta v_k$",
        (2.23, 1.34),
        color=PURPLE,
        lw=1.35,
        ms=12,
        both=True,
    )

    return save(fig, "B_segment_vector_change.pdf", tight=False)


def draw_bending_change_split():
    fig, ax = plt.subplots(figsize=SMALL_FIGSIZE)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    configure(ax, (0.0, 3.40), (0.0, 2.00))

    panel(ax, (0.15, 0.20), (3.10, 1.60))
    tri_a = np.array([(0.65, 0.72), (1.60, 1.48), (2.65, 0.84)])
    tri_b = np.array([(0.65, 0.60), (1.60, 0.98), (2.65, 0.70)])
    draw_cable(ax, tri_a, color=BLUE, lw=2.05)
    draw_cable(ax, tri_b, color=ORANGE, ls="--", marker_face="white", lw=1.75)
    arrow(ax, (1.60, 0.98), (1.60, 1.48), r"$\Delta b_k$", (1.8, 1.20), color=PURPLE, lw=1.35, ms=12, both=True)

    return save(fig, "C_bending_change.pdf", tight=False)


if __name__ == "__main__":
    main()
