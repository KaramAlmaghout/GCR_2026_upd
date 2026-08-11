from pathlib import Path
import re

import fitz


PAPER_RESULTS = Path(__file__).resolve().parents[1] / "paper_results"
OBSTACLE_FILL = (0.6509803922, 0.6745098039, 0.7254901961)
LABEL_COLOR = (0.18, 0.20, 0.25)
LABEL_HEX_PATTERN = re.compile(r"\[<(?P<hex>4f[0-9a-fA-F]+)>\]TJ")


def close_rgb(a, b, tol=1e-3):
    return a is not None and all(abs(x - y) <= tol for x, y in zip(a, b))


def obstacle_rects(page):
    rects = []
    for drawing in page.get_drawings():
        if close_rgb(drawing.get("fill"), OBSTACLE_FILL):
            rects.append(drawing["rect"])
    return sorted(rects, key=lambda r: (r.x0, r.y0))


def label_font_size(rect):
    return max(7.5, min(14.0, min(rect.width, rect.height) * 0.34))


def existing_obstacle_label_count(page):
    return len(re.findall(r"\bO\d+\b", page.get_text("text")))


def label_stream_text(doc, xref):
    stream = doc.xref_stream(xref)
    if len(stream) > 300:
        return None

    text = stream.decode("latin1", errors="replace")
    if "/helv" not in text or ".18 .2 .25" not in text:
        return None

    match = LABEL_HEX_PATTERN.search(text)
    if not match:
        return None

    try:
        label = bytes.fromhex(match.group("hex")).decode("ascii")
    except ValueError:
        return None

    if re.fullmatch(r"O\d+", label):
        return label
    return None


def remove_duplicate_label_streams(doc, page):
    seen = {}
    for xref in page.get_contents():
        label = label_stream_text(doc, xref)
        if label is not None:
            seen.setdefault(label, []).append(xref)

    changed = False
    for xrefs in seen.values():
        for xref in xrefs[:-1]:
            doc.update_stream(xref, b"\n")
            changed = True
    return changed


def annotate_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    changed = False

    for page in doc:
        changed = remove_duplicate_label_streams(doc, page) or changed
        rects = obstacle_rects(page)
        if not rects:
            continue
        if existing_obstacle_label_count(page) >= len(rects):
            continue

        for i, rect in enumerate(rects, start=1):
            fontsize = label_font_size(rect)
            cx = 0.5 * (rect.x0 + rect.x1)
            cy = 0.5 * (rect.y0 + rect.y1)
            label = f"O{i}"
            text_width = fitz.get_text_length(label, fontname="helv", fontsize=fontsize)
            page.insert_text(
                fitz.Point(cx - 0.5 * text_width, cy + 0.36 * fontsize),
                label,
                fontsize=fontsize,
                fontname="helv",
                color=LABEL_COLOR,
                overlay=True,
            )
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
        if annotate_pdf(pdf_path):
            print(f"annotated {pdf_path}")
        else:
            print(f"unchanged {pdf_path}")


if __name__ == "__main__":
    main()
