"""L2 check of the v2 reconstruction fidelity (independent of rebuild_v2_diff.py).

Extractor: pypdf (the corrector used PyMuPDF). Comparison: word-level
SequenceMatcher after Unicode NFKC normalisation and removal of whitespace
artefacts, plus a page-by-page character ratio.
Oracle: published Zenodo trilogy pages 29-46 (record 22866175).
Negative controls: (1) compare against the compiled v3 (must be clearly lower);
(2) delete the v2-only Theorem 6.3 block from the rebuilt text (must be detected).
Also: v3 PDF in the folder vs a fresh L2 build of the v3 .tex (must be identical).
"""
import sys, re, unicodedata, difflib, os
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.dirname(HERE)
ROOT = os.path.dirname(AUD)
fails = 0

def text(path, pages=None):
    r = PdfReader(path)
    idx = range(len(r.pages)) if pages is None else pages
    return " ".join(r.pages[i].extract_text() or "" for i in idx)

def words(t):
    t = unicodedata.normalize("NFKC", t)
    t = t.replace("-\n", "").replace("­", "")
    t = re.sub(r"\s+", " ", t)
    # keep alphanumeric tokens only, so spacing around math glyphs is ignored
    return re.findall(r"[A-Za-z0-9]+", t)

def sim(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
    return sm.ratio(), ops

zen = words(text(os.path.join(HERE, "zenodo_trilogy_22866175.pdf"), range(28, 46)))
v2 = words(text(os.path.join(AUD, "L2_build", "v2", "v2_reconstructed.pdf")))
v3 = words(text(os.path.join(AUD, "L2_build", "v3", "paper_geometric_measures_functional_tensors.pdf")))
v3_folder = words(text(os.path.join(ROOT, "paper_geometric_measures_functional_tensors.pdf")))

r, ops = sim(zen, v2)
print(f"zenodo words {len(zen)}  rebuilt-v2 words {len(v2)}  ratio {r:.5f}  diff ops {len(ops)}")
for tag, i1, i2, j1, j2 in ops[:20]:
    print(f"  {tag}: ZEN[{' '.join(zen[max(0,i1-4):i2+4])}]  V2[{' '.join(v2[max(0,j1-4):j2+4])}]")
if r < 0.999:
    fails += 1; print("FAIL fidelity below 0.999")

# spot checks of reconstructed passages listed in RECONSTRUCTION_v2.md
spots = ["Quantized Cyclic Cocycles and Topological Degree",
         "linearly independent in the Hilbert Schmidt inner product",
         "exhausting sequence of smooth convex domains",
         "strictly contained in the interior",
         "052320", "22441676",
         "Programa de P"]
zs, vs = " ".join(zen), " ".join(v2)
for s in spots:
    w = " ".join(words(s))
    inz, inv = w in zs, w in vs
    print(f"  spot '{s}': zenodo {inz} rebuilt {inv}")
    if inz != inv:
        fails += 1; print("  FAIL spot mismatch")

# negative control 1: v3 must differ substantially
r3, _ = sim(zen, v3)
print(f"NEG zenodo vs v3 ratio {r3:.4f} (must be < 0.9)")
if r3 >= 0.9:
    fails += 1
# negative control 2: delete the Thm 6.3 block from the rebuilt text
k = vs.find(" ".join(words("Quantized Cyclic Cocycles")))
mut = (vs[:k] + vs[k + 3000:]).split() if k >= 0 else v2
rm, _ = sim(zen, mut)
print(f"NEG mutated rebuilt (3000 chars removed) ratio {rm:.5f} (must be < {r:.5f} - 0.01)")
if not rm < r - 0.01:
    fails += 1

# folder PDF vs fresh build
rf, opsf = sim(v3_folder, v3)
print(f"v3 folder PDF vs fresh L2 build: ratio {rf:.6f}, ops {len(opsf)}")
for tag, i1, i2, j1, j2 in opsf[:5]:
    print(f"  {tag}: FOLDER[{' '.join(v3_folder[max(0,i1-3):i2+3])}] BUILD[{' '.join(v3[max(0,j1-3):j2+3])}]")
if rf < 0.9999:
    fails += 1
print("failures", fails)
sys.exit(int(fails))
