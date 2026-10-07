"""Compare local .tex with each Zenodo Volume I using a content-word set difference
(robust to hyphenation and LaTeX labels): words that occur in one and not the other."""
import os, re, collections
import pymupdf
HERE = os.path.dirname(os.path.abspath(__file__)); AUD = os.path.dirname(HERE)
def w(s): return re.findall(r"[a-z]{4,}", s.lower())
def pdfw(p): return w(re.sub(r"-\n", "", "\n".join(pg.get_text() for pg in pymupdf.open(p))))
s = open(os.path.join(AUD, "..", "paper_functional_realizations.tex"), encoding="utf-8").read()
s = re.sub(r"\[A-Za-z]+", " ", s)
T = collections.Counter(w(s))
for name in ["zenodo_v22644744_vol1.pdf", "zenodo_latest_vol1.pdf"]:
    P = collections.Counter(pdfw(os.path.join(AUD, name)))
    only_pdf = sorted(k for k in P if k not in T)
    only_tex = sorted(k for k in T if k not in P)
    print("==", name)
    print(" words only in PDF:", len(only_pdf), only_pdf)
    print(" words only in TEX:", len(only_tex), only_tex)
