from pathlib import Path
import math
import re

import fitz


PAPER_RESULTS = Path(__file__).resolve().parents[1] / "paper_results"

TICK_SIZE = 20.0
AXIS_LABEL_SIZE = 23.0
PROFILE_NUMBER_SIZE = 14.0
PROFILE_MARKER_RADIUS = 8.0
LEFT_MARGIN = 56.0
BOTTOM_MARGIN = 16.0
Y_AXIS_LABEL_X = -22.0
X_TICK_LABEL_Y = 21.0
NUMBER = r"-?\d+(?:\.\d+)?"

TEXT_BLOCK = re.compile(
    r"q\n"
    r"(?P<a>-?\d+(?:\.\d+)?) (?P<b>-?\d+(?:\.\d+)?) "
    r"(?P<c>-?\d+(?:\.\d+)?) (?P<d>-?\d+(?:\.\d+)?) "
    r"(?P<x>-?\d+(?:\.\d+)?) (?P<y>-?\d+(?:\.\d+)?) cm\n"
    r"BT\n"
    r"/(?P<font>F[12]) (?P<size>\d+(?:\.\d+)?) Tf\n"
    r"0 0 Td\n"
    r"\[ \((?P<label>[^()]*)\) \] TJ\n"
    r"ET\n"
    r"Q"
)

PROFILE_MARKER_BLOCK = re.compile(
    rf"(?P<style>/A7 gs [^\n]+\n[^\n]+\n\n)"
    rf"(?P<path>(?:{NUMBER}(?: {NUMBER})+ [mc]\n)+h\n\nB\n)"
    rf"(?P<text>/A2 gs 1 g 1 j 1 w 1 G 1 g\n"
    rf"q\n"
    rf"1 0 -?0 1 {NUMBER} {NUMBER} cm\n"
    rf"BT\n"
    rf"/F2 {NUMBER} Tf\n"
    rf"0 0 Td\n"
    rf"\[ \(\d+\) \] TJ\n"
    rf"ET\n"
    rf"Q)"
)


def text_width(label, size):
    return fitz.get_text_length(label, fontname="helv", fontsize=size)


def fmt(value):
    return f"{value:.6f}".rstrip("0").rstrip(".")


def profile_marker_path(cx, cy, radius):
    delta = math.pi / 4.0
    alpha = 4.0 / 3.0 * math.tan(delta / 4.0)
    theta = -math.pi / 2.0
    lines = [f"{fmt(cx)} {fmt(cy - radius)} m"]

    for _ in range(8):
        next_theta = theta + delta
        p0 = (cx + radius * math.cos(theta), cy + radius * math.sin(theta))
        p3 = (cx + radius * math.cos(next_theta), cy + radius * math.sin(next_theta))
        c1 = (
            p0[0] + alpha * radius * -math.sin(theta),
            p0[1] + alpha * radius * math.cos(theta),
        )
        c2 = (
            p3[0] - alpha * radius * -math.sin(next_theta),
            p3[1] - alpha * radius * math.cos(next_theta),
        )
        lines.append(
            f"{fmt(c1[0])} {fmt(c1[1])} "
            f"{fmt(c2[0])} {fmt(c2[1])} "
            f"{fmt(p3[0])} {fmt(p3[1])} c"
        )
        theta = next_theta

    return "\n".join(lines) + "\nh\n\nB\n"


def path_bounds(path):
    xs = []
    ys = []
    for line in path.splitlines():
        parts = line.split()
        if not parts or parts[-1] not in {"m", "c"}:
            continue

        values = [float(value) for value in parts[:-1]]
        xs.extend(values[0::2])
        ys.extend(values[1::2])

    if not xs or not ys:
        return None

    return min(xs), min(ys), max(xs), max(ys)


def update_profile_marker(match):
    bounds = path_bounds(match.group("path"))
    if bounds is None:
        return match.group(0)

    x0, y0, x1, y1 = bounds
    radius = max(x1 - x0, y1 - y0) / 2.0
    if radius >= PROFILE_MARKER_RADIUS - 1e-3:
        return match.group(0)

    cx = 0.5 * (x0 + x1)
    cy = 0.5 * (y0 + y1)
    return match.group("style") + profile_marker_path(cx, cy, PROFILE_MARKER_RADIUS) + match.group("text")


def adjusted_position(label, font, old_size, new_size, matrix, x, y):
    a, b, c, d = matrix
    horizontal = abs(a - 1.0) < 1e-6 and abs(b) < 1e-6 and abs(c) < 1e-6 and abs(d - 1.0) < 1e-6
    rotated_y_label = abs(a) < 1e-6 and abs(b - 1.0) < 1e-6 and abs(c + 1.0) < 1e-6 and abs(d) < 1e-6

    if font == "F1" and label in {"x [m]", "y [m]"}:
        if label == "x [m]":
            x -= 0.5 * (text_width(label, new_size) - text_width(label, old_size))
            y += 0.25 * (new_size - old_size)
        elif rotated_y_label:
            x = Y_AXIS_LABEL_X
        return x, y

    if font == "F1" and re.fullmatch(r"\d\.\d", label) and horizontal:
        width_delta = text_width(label, new_size) - text_width(label, old_size)
        if y < 40:
            x -= 0.5 * width_delta
        elif x < 35:
            x -= width_delta
        if y < 40:
            y = X_TICK_LABEL_Y
        return x, y

    if font == "F2" and label.isdigit() and horizontal:
        width_delta = text_width(label, new_size) - text_width(label, old_size)
        x -= 0.5 * width_delta
        y -= 0.35 * (new_size - old_size)
        return x, y

    return x, y


def update_text_block(match):
    label = match.group("label")
    font = match.group("font")
    old_size = float(match.group("size"))

    new_size = None
    if font == "F1" and re.fullmatch(r"\d\.\d", label):
        a, b, c, d = [float(match.group(key)) for key in ("a", "b", "c", "d")]
        x = float(match.group("x"))
        y = float(match.group("y"))
        horizontal = abs(a - 1.0) < 1e-6 and abs(b) < 1e-6 and abs(c) < 1e-6 and abs(d - 1.0) < 1e-6
        if old_size < TICK_SIZE - 1e-6:
            new_size = TICK_SIZE
        elif horizontal and y < 40 and abs(y - X_TICK_LABEL_Y) > 1e-6:
            new_size = old_size
    elif font == "F1" and label in {"x [m]", "y [m]"} and old_size < AXIS_LABEL_SIZE - 1e-6:
        new_size = AXIS_LABEL_SIZE
    elif font == "F1" and label == "y [m]" and abs(old_size - AXIS_LABEL_SIZE) < 1e-6:
        x = float(match.group("x"))
        if abs(x - Y_AXIS_LABEL_X) > 1e-6:
            new_size = AXIS_LABEL_SIZE
    elif font == "F2" and label.isdigit() and old_size < PROFILE_NUMBER_SIZE - 1e-6:
        new_size = PROFILE_NUMBER_SIZE

    if new_size is None:
        return match.group(0)

    matrix = [float(match.group(key)) for key in ("a", "b", "c", "d")]
    x = float(match.group("x"))
    y = float(match.group("y"))
    x, y = adjusted_position(label, font, old_size, new_size, matrix, x, y)

    return (
        "q\n"
        f"{fmt(matrix[0])} {fmt(matrix[1])} {fmt(matrix[2])} {fmt(matrix[3])} {fmt(x)} {fmt(y)} cm\n"
        "BT\n"
        f"/{font} {fmt(new_size)} Tf\n"
        "0 0 Td\n"
        f"[ ({label}) ] TJ\n"
        "ET\n"
        "Q"
    )


def ensure_left_margin(page):
    box = page.mediabox
    target = fitz.Rect(-LEFT_MARGIN, -BOTTOM_MARGIN, box.x1, box.y1)
    if all(abs(a - b) < 1e-3 for a, b in zip(box, target)):
        return False

    page.set_mediabox(target)
    return True


def enlarge_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    changed = False

    for page in doc:
        changed = ensure_left_margin(page) or changed
        for xref in page.get_contents():
            stream = doc.xref_stream(xref)
            text = stream.decode("latin1", errors="replace")
            new_text = TEXT_BLOCK.sub(update_text_block, text)
            new_text = PROFILE_MARKER_BLOCK.sub(update_profile_marker, new_text)
            if new_text != text:
                doc.update_stream(xref, new_text.encode("latin1"))
                changed = True

    if not changed:
        doc.close()
        return False

    tmp_path = pdf_path.with_suffix(".tmp.pdf")
    doc.save(tmp_path, garbage=4, deflate=True)
    doc.close()
    tmp_path.replace(pdf_path)
    return True


def main():
    for pdf_path in sorted(PAPER_RESULTS.glob("scenario_*_no_legend.pdf")):
        if enlarge_pdf_text(pdf_path):
            print(f"enlarged {pdf_path}")
        else:
            print(f"unchanged {pdf_path}")


if __name__ == "__main__":
    main()
