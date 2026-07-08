from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle


FIGSIZE = (4.8, 3.05)
LW = 1.55
MS = 3.7
FONT = 7


def configure(ax, xlim=(-0.15, 6.45), ylim=(-0.1, 4.05)):
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


def draw_cable(ax, pts, color="0.15", ls="-", marker_face=None, lw=LW, zorder=2):
    kwargs = {"color": color, "lw": lw, "ls": ls, "marker": "o", "ms": MS, "zorder": zorder}
    if marker_face is not None:
        kwargs["mfc"] = marker_face
    ax.plot(pts[:, 0], pts[:, 1], **kwargs)


def arrow(ax, p, q, text=None, text_xy=None, color="0.20", lw=0.9, ms=8, both=False):
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

    panel(ax, (0.15, 2.25), (6.1, 1.55), r"A  segment vector")
    draw_cable(ax, ca, color="0.15")
    draw_cable(ax, cb, color="0.50", ls="--", marker_face="white", lw=1.25)
    ax.text(ca[0, 0] - 0.08, ca[0, 1] + 0.08, r"$C^a$", ha="right", color="0.15")
    ax.text(cb[0, 0] - 0.08, cb[0, 1] - 0.15, r"$C^b$", ha="right", color="0.38")

    k = 2
    ax.plot(ca[k : k + 2, 0], ca[k : k + 2, 1], color="0.02", lw=2.7)
    ax.plot(cb[k : k + 2, 0], cb[k : k + 2, 1], color="0.36", lw=2.2, ls="--")
    arrow(ax, ca[k], ca[k + 1], r"$v_k(C^a)$", (2.18 + x_shift, 3.36), color="0.10", lw=1.0)
    arrow(ax, cb[k], cb[k + 1], r"$v_k(C^b)$", (2.24 + x_shift, 2.56), color="0.38", lw=1.0)

    panel(ax, (0.15, 0.35), (2.95, 1.45), r"B  segment-vector change")
    tail = np.array((0.90, 0.83))
    va = np.array((0.98, 0.28))
    vb = np.array((0.76, 0.62))
    arrow(ax, tail, tail + va, color="0.12", lw=1.1)
    ax.text(1.52, 0.79, r"$v_k(C^a)$", ha="center", va="center")
    arrow(ax, tail, tail + vb, r"$v_k(C^b)$", (1.16, 1.34), color="0.45", lw=1.1)
    arrow(
        ax,
        tail + vb,
        tail + va,
        color="0.08",
        lw=1.0,
        both=True,
    )
    ax.text(2.17, 1.23, r"$\Delta v_k$", ha="center", va="center")
    ax.text(1.62, 0.44, r"$\Delta v_k=v_k(C^a)-v_k(C^b)$", ha="center")

    panel(ax, (3.30, 0.35), (2.95, 1.45), r"C  bending change")
    tri_a = np.array([(3.80, 0.78), (4.55, 1.34), (5.35, 0.92)])
    tri_b = np.array([(3.80, 0.70), (4.55, 0.98), (5.35, 0.82)])
    draw_cable(ax, tri_a, color="0.15", lw=1.5)
    draw_cable(ax, tri_b, color="0.50", ls="--", marker_face="white", lw=1.15)
    arrow(ax, (4.55, 0.98), (4.55, 1.34), r"$\Delta b_k$", (5.10, 1.28), color="0.08", both=True)
    ax.text(4.78, 0.48, r"$\Delta b_k=b_k(C^a)-b_k(C^b)$", ha="center")

    print(save(fig, "local_deformation_measures.pdf"))
    for out in (
        draw_segment_vector_split(),
        draw_segment_vector_change_split(),
        draw_bending_change_split(),
    ):
        print(out)


def draw_segment_vector_split():
    fig, ax = plt.subplots(figsize=(3.55, 1.22))
    configure(ax, (0.05, 4.25), (2.34, 3.58))

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

    panel(ax, (0.20, 2.42), (3.95, 1.04))
    draw_cable(ax, ca, color="0.15")
    draw_cable(ax, cb, color="0.50", ls="--", marker_face="white", lw=1.25)
    ax.text(ca[0, 0] - 0.08, ca[0, 1] + 0.08, r"$C^a$", ha="right", color="0.15")
    ax.text(cb[0, 0] - 0.08, cb[0, 1] - 0.15, r"$C^b$", ha="right", color="0.38")

    k = 2
    ax.plot(ca[k : k + 2, 0], ca[k : k + 2, 1], color="0.02", lw=2.7)
    ax.plot(cb[k : k + 2, 0], cb[k : k + 2, 1], color="0.36", lw=2.2, ls="--")
    arrow(ax, ca[k], ca[k + 1], r"$v_k(C^a)$", (2.18, 3.30), color="0.10", lw=1.0)
    arrow(ax, cb[k], cb[k + 1], r"$v_k(C^b)$", (2.24, 2.56), color="0.38", lw=1.0)

    return save(fig, "A_segment_vector.pdf")


def draw_segment_vector_change_split():
    fig, ax = plt.subplots(figsize=(2.55, 1.30))
    configure(ax, (0.28, 2.92), (0.20, 1.66))

    panel(ax, (0.38, 0.30), (2.44, 1.22))
    tail = np.array((0.90, 0.83))
    va = np.array((0.98, 0.28))
    vb = np.array((0.76, 0.62))
    arrow(ax, tail, tail + va, color="0.12", lw=1.1)
    ax.text(1.52, 0.79, r"$v_k(C^a)$", ha="center", va="center")
    arrow(ax, tail, tail + vb, r"$v_k(C^b)$", (1.16, 1.34), color="0.45", lw=1.1)
    arrow(
        ax,
        tail + vb,
        tail + va,
        color="0.08",
        lw=1.0,
        both=True,
    )
    ax.text(2.17, 1.23, r"$\Delta v_k$", ha="center", va="center")
    ax.text(1.60, 0.40, r"$\Delta v_k=v_k(C^a)-v_k(C^b)$", ha="center")

    return save(fig, "B_segment_vector_change.pdf")


def draw_bending_change_split():
    fig, ax = plt.subplots(figsize=(2.75, 1.18))
    configure(ax, (3.20, 6.35), (0.35, 1.68))

    panel(ax, (3.30, 0.40), (2.95, 1.16))
    tri_a = np.array([(3.80, 0.78), (4.55, 1.34), (5.35, 0.92)])
    tri_b = np.array([(3.80, 0.70), (4.55, 0.98), (5.35, 0.82)])
    draw_cable(ax, tri_a, color="0.15", lw=1.5)
    draw_cable(ax, tri_b, color="0.50", ls="--", marker_face="white", lw=1.15)
    arrow(ax, (4.55, 0.98), (4.55, 1.34), r"$\Delta b_k$", (5.10, 1.28), color="0.08", both=True)
    ax.text(4.78, 0.48, r"$\Delta b_k=b_k(C^a)-b_k(C^b)$", ha="center")

    return save(fig, "C_bending_change.pdf")


if __name__ == "__main__":
    main()
