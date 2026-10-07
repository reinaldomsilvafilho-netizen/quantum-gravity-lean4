"""Render selected pages of zenodo_latest_vol1.pdf to PNG for visual reading."""
import os, sys, pymupdf
AUD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
doc = pymupdf.open(os.path.join(AUD, "zenodo_latest_vol1.pdf"))
os.makedirs(os.path.join(AUD, "png"), exist_ok=True)
for i, p in enumerate(doc):
    t = p.get_text()
    print(i, len(t), t[:60].replace("\n", " | "))
for a in sys.argv[1:]:
    i = int(a)
    doc[i].get_pixmap(dpi=110).save(os.path.join(AUD, "png", f"p{i:02d}.png"))
