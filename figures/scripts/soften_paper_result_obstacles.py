from pathlib import Path
import re

import fitz


PAPER_RESULTS = Path(__file__).resolve().parents[1] / "paper_results"

OLD_FILL = r"0\.2470588235\s+0\.2470588235\s+0\.2745098039\s+rg"
OLD_EDGE = r"0\.0941176471\s+0\.0941176471\s+0\.1058823529\s+RG"

NEW_FILL = "0.6509803922 0.6745098039 0.7254901961 rg"
NEW_EDGE = "0.4392156863 0.4705882353 0.5372549020 RG"


def soften_pdf_obstacles(pdf_path):
    doc = fitz.open(pdf_path)
    changed = False

    for page in doc:
        for xref in page.get_contents():
            stream = doc.xref_stream(xref)
            text = stream.decode("latin1")
            text, fill_count = re.subn(OLD_FILL, NEW_FILL, text)
            text, edge_count = re.subn(OLD_EDGE, NEW_EDGE, text)
            if fill_count or edge_count:
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
            print(f"softened {pdf_path}")
        else:
            print(f"unchanged {pdf_path}")


if __name__ == "__main__":
    main()
