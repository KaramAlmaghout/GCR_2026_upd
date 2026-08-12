from pathlib import Path
import re

import fitz


PAPER_RESULTS = Path(__file__).resolve().parents[1] / "paper_results"

OLD_FILL = r"0\.2470588235\s+0\.2470588235\s+0\.2745098039\s+rg"
OLD_EDGE = r"0\.0941176471\s+0\.0941176471\s+0\.1058823529\s+RG"
SOFT_EDGE = r"0\.4392156863\s+0\.4705882353\s+0\.5372549020\s+RG"
GRAY_FILL = r"0\.6509803922\s+0\.6745098039\s+0\.7254901961\s+rg"
GRAY_EDGE = r"0\.6509803922\s+0\.6745098039\s+0\.7254901961\s+RG"
RED_FILL = r"0\.9568627451\s+0\.6745098039\s+0\.6745098039\s+rg"
RED_EDGE = r"0\.9568627451\s+0\.6745098039\s+0\.6745098039\s+RG"
BLUE_FILL = r"0\.6980392157\s+0\.8470588235\s+0\.9686274510\s+rg"
BLUE_EDGE = r"0\.6980392157\s+0\.8470588235\s+0\.9686274510\s+RG"
GREEN_FILL = r"0\.7333333333\s+0\.8941176471\s+0\.7607843137\s+rg"
GREEN_EDGE = r"0\.7333333333\s+0\.8941176471\s+0\.7607843137\s+RG"

NEW_FILL = "0.7215686275 0.6980392157 0.6666666667 rg"
NEW_EDGE = "0.7215686275 0.6980392157 0.6666666667 RG"
LABEL_HEX_PATTERN = re.compile(r"\[<(?P<hex>4f[0-9a-fA-F]+)>\]TJ")


def is_obstacle_label_stream(text):
    if len(text) > 300:
        return False
    if "/helv" not in text or ".18 .2 .25" not in text:
        return False

    match = LABEL_HEX_PATTERN.search(text)
    if not match:
        return False

    try:
        label = bytes.fromhex(match.group("hex")).decode("ascii")
    except ValueError:
        return False

    return re.fullmatch(r"O\d+", label) is not None


def soften_pdf_obstacles(pdf_path):
    doc = fitz.open(pdf_path)
    changed = False

    for page in doc:
        for xref in page.get_contents():
            stream = doc.xref_stream(xref)
            text = stream.decode("latin1")
            if is_obstacle_label_stream(text):
                doc.update_stream(xref, b"\n")
                changed = True
                continue

            text, fill_count = re.subn(OLD_FILL, NEW_FILL, text)
            text, edge_count = re.subn(OLD_EDGE, NEW_EDGE, text)
            text, soft_edge_count = re.subn(SOFT_EDGE, NEW_EDGE, text)
            text, gray_fill_count = re.subn(GRAY_FILL, NEW_FILL, text)
            text, gray_edge_count = re.subn(GRAY_EDGE, NEW_EDGE, text)
            text, red_fill_count = re.subn(RED_FILL, NEW_FILL, text)
            text, red_edge_count = re.subn(RED_EDGE, NEW_EDGE, text)
            text, blue_fill_count = re.subn(BLUE_FILL, NEW_FILL, text)
            text, blue_edge_count = re.subn(BLUE_EDGE, NEW_EDGE, text)
            text, green_fill_count = re.subn(GREEN_FILL, NEW_FILL, text)
            text, green_edge_count = re.subn(GREEN_EDGE, NEW_EDGE, text)
            if (
                fill_count
                or edge_count
                or soft_edge_count
                or gray_fill_count
                or gray_edge_count
                or red_fill_count
                or red_edge_count
                or blue_fill_count
                or blue_edge_count
                or green_fill_count
                or green_edge_count
            ):
                doc.update_stream(xref, text.encode("latin1"))
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
    files = sorted(PAPER_RESULTS.glob("scenario_*_no_legend.pdf"))
    files.append(PAPER_RESULTS / "paper_plot_legend.pdf")

    for pdf_path in files:
        if soften_pdf_obstacles(pdf_path):
            print(f"cleaned {pdf_path}")
        else:
            print(f"unchanged {pdf_path}")


if __name__ == "__main__":
    main()
