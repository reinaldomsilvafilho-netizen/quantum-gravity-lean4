"""Extract Volume I from the latest Zenodo trilogy and compare word streams with
the local .tex, the local Volume I PDF (= Zenodo 22699282) and the 2026-09-07 Volume I.

Method: alphabetic word tokens (len>=3, lowercased) from PDF text (PyMuPDF) and from
the .tex with LaTeX commands stripped; difflib opcodes on token lists.
Negative control: a mutated copy of the tex token stream (one word replaced) must
produce a non-empty diff.
"""
import difflib
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.dirname(HERE)
TEX = os.path.join(AUD, "..", "paper_functional_realizations.tex")
TRIL = os.path.join(AUD, "zenodo_latest_trilogy_22866175.pdf")


def pdf_pages_text(path):
    doc = pymupdf.open(path)
    return doc, [p.get_text() for p in doc]


def words(s):
    return re.findall(r"[a-z]{3,}", s.lower())


def tex_words(path):
    s = open(path, encoding="utf-8").read()
    s = s.split("\\begin{document}", 1)[1]
    s = re.sub(r"(?m)%.*$", "", s)
    s = re.sub(r"\\(label|ref|eqref|cite|begin|end|url|bibitem|newcommand)\{[^}]*\}", " ", s)
    s = re.sub(r"\\[A-Za-z]+", " ", s)
    return words(s)


doc, pages = pdf_pages_text(TRIL)
start = next(i for i, t in enumerate(pages) if "Finite-dimensional multilinear algebra" in t)
end = next(i for i, t in enumerate(pages) if i > start and "Volume II: Metric Measure Geometry" in t
           and "Part II" in t or (i > start and re.search(r"Part\s+II", t)))
print("trilogy pages for Vol I (0-based):", start, "to", end - 1, "of", len(pages))
out = pymupdf.open()
out.insert_pdf(doc, from_page=start - 1, to_page=end - 1)
out.save(os.path.join(AUD, "zenodo_latest_vol1.pdf"))
z = words("\n".join(pages[start:end]))

def pdfwords(p):
    d, pg = pdf_pages_text(p)
    return words("\n".join(pg))

local_pdf = pdfwords(os.path.join(AUD, "zenodo_v22699282_vol1.pdf"))
old_pdf = pdfwords(os.path.join(AUD, "zenodo_v22644744_vol1.pdf"))
t = tex_words(TEX)


def report(name_a, a, name_b, b, show=25):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
    print(f"\n== {name_a} ({len(a)}) vs {name_b} ({len(b)}): ratio={sm.ratio():.4f}, non-equal blocks={len(ops)}")
    for tag, i1, i2, j1, j2 in ops[:show]:
        print(f"  {tag}: A[{' '.join(a[i1:i2][:15])}]  B[{' '.join(b[j1:j2][:15])}]")
    return ops


report("zenodo_latest_vol1(trilogy)", z, "local_tex", t)
report("zenodo_latest_vol1(trilogy)", z, "local_vol1_pdf=zenodo22699282", local_pdf)
report("local_vol1_pdf", local_pdf, "zenodo22644744_vol1(2026-09-07)", old_pdf, show=40)

# negative control
mut = list(t)
k = mut.index("dirichlet")
mut[k] = "neumann"
ops = report("local_tex", t, "mutated_tex", mut, show=3)
failures = 0 if len(ops) >= 1 else 1
print("negative control detected mutation:", failures == 0)
sys.exit(failures)
