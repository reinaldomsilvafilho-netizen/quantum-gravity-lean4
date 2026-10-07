"""Layer-2 check of the v2 reconstruction (2026-10-06).

1. Token-stream diff (alphanumeric tokens, case-folded) between
   - the compiled pure reconstruction (L2_build/recon/..._v2_reconstructed.pdf), and
   - the published v2 standalone PDF (zenodo_v22699282_vol1.pdf) and the Vol. I pages
     of the latest trilogy (zenodo_latest_vol1.pdf).
   Running heads/page numbers are removed by dropping the tokens that make up them.
2. Negative control: one mutated word (and one mutated digit) in the reconstruction
   stream must be detected.
3. Content inventory: section titles and titled environments of the reconstruction
   vs the current .tex; every v2 item missing from the current file is listed.
"""
import difflib
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.dirname(HERE)
RECON_PDF = os.path.join(AUD, "L2_build", "recon", "paper_functional_realizations_v2_reconstructed.pdf")
RECON_TEX = os.path.join(AUD, "L2_build", "recon", "paper_functional_realizations_v2_reconstructed.tex")
CUR_TEX = os.path.join(AUD, "..", "paper_functional_realizations.tex")
V2 = os.path.join(AUD, "zenodo_v22699282_vol1.pdf")
TRI = os.path.join(AUD, "zenodo_latest_vol1.pdf")

HEADS = {"beyond", "the", "spectrum", "reinaldo", "silva", "filho", "complete", "trilogy"}


def toks(path):
    doc = pymupdf.open(path)
    out = []
    for p in doc:
        lines = p.get_text().splitlines()
        # drop running-head lines (short lines made only of head words / digits)
        for ln in lines:
            w = re.findall(r"[a-z0-9]+", ln.lower())
            if w and all(x in HEADS or x.isdigit() for x in w) and len(w) <= 6:
                continue
            out.extend(w)
    return out


def diff(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
    return sm.ratio(), ops


fails = 0
r = toks(RECON_PDF)
for name, path in (("v2 standalone 22699282", V2), ("trilogy 22866175 Vol I", TRI)):
    z = toks(path)
    if name.startswith("trilogy"):
        # the extracted trilogy pages start one page early and may end late: align on the abstract/end
        s = next(i for i in range(len(z)) if z[i:i + 3] == ["finite", "dimensional", "multilinear"])
        z = z[s:]
        rs = next(i for i in range(len(r)) if r[i:i + 3] == ["finite", "dimensional", "multilinear"])
        rr = r[rs:]
        # cut at the last token of the reconstruction (the e-mail line)
        e = max(i for i in range(len(z)) if z[i:i + 2] == ["ufla", "br"]) + 2 if any(
            z[i:i + 2] == ["ufla", "br"] for i in range(len(z))) else len(z)
        z = z[:e]
    else:
        rr = r
    ratio, ops = diff(rr, z)
    print(f"== recon vs {name}: tokens {len(rr)} vs {len(z)}, ratio {ratio:.5f}, non-equal blocks {len(ops)}")
    sm_a, sm_b = rr, z
    for tag, i1, i2, j1, j2 in ops[:40]:
        print(f"   {tag:7s} recon[{' '.join(sm_a[i1:i2])[:70]}]  pdf[{' '.join(sm_b[j1:j2])[:70]}]")
    # word-level differences that are not pure math-glyph splits
    words_r = {t for t in rr if t.isalpha() and len(t) >= 4}
    words_z = {t for t in z if t.isalpha() and len(t) >= 4}
    only_z = sorted(words_z - words_r)
    only_r = sorted(words_r - words_z)
    print("   words (len>=4) only in published:", only_z[:40])
    print("   words (len>=4) only in recon    :", only_r[:40])
    if name.startswith("v2") and (only_z or only_r):
        print("   NOTE: inspect the word lists above")
    # negative control
    m = list(rr)
    k = len(m) // 2
    while not m[k].isalpha():
        k += 1
    m[k] = m[k] + "x"
    j = next(i for i in range(len(m) // 3, len(m)) if m[i].isdigit())
    m[j] = str(int(m[j]) + 1)
    _, ops_m = diff(m, z)
    if len(ops_m) <= len(ops):
        print("   NEG FAIL: mutations not detected")
        fails += 1
    else:
        print(f"   NEG ok: mutated stream gives {len(ops_m)} blocks > {len(ops)}")


def inventory(path):
    s = open(path, encoding="utf-8").read()
    s = s.split("\\begin{document}", 1)[1]
    items = re.findall(r"\\(section|subsection)\*?\{([^}]*)\}", s)
    items += re.findall(r"\\begin\{(theorem|proposition|lemma|corollary|definition|example|remark|construction)\}\[([^\]]*)\]", s)
    return [(a, re.sub(r"\s+", " ", b)) for a, b in items]


v2 = inventory(RECON_TEX)
cur = inventory(CUR_TEX)
cur_titles = {b.lower() for _, b in cur}
print("\n== v2 items whose title is absent from the current .tex:")
for a, b in v2:
    if b.lower() not in cur_titles:
        print(f"   {a}: {b}")
print("== current items whose title is absent from v2:")
v2_titles = {b.lower() for _, b in v2}
for a, b in cur:
    if b.lower() not in v2_titles:
        print(f"   {a}: {b}")
print("\nfailures:", fails)
sys.exit(fails)
