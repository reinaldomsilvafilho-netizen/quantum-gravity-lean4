"""Extract Volume II from the latest Zenodo trilogy PDF (record 22866175) and compare its
text with the local volume_2 PDF and with the local .tex (via the compiled local PDF).
Negative control: Volume I text must NOT match Volume II."""
import os, re, difflib, pymupdf
HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.dirname(HERE)
PAPER = os.path.dirname(AUD)
BTS = os.path.join(os.path.dirname(PAPER), "beyond_the_spectrum_files")
out = []
def norm(t):
    t = re.sub(r"\s+", " ", t)
    return t.strip()
tri = pymupdf.open(os.path.join(HERE, "zenodo_trilogy_22866175.pdf"))
# find Volume II start/end by title occurrences
starts = []
for i, p in enumerate(tri):
    tx = p.get_text()
    if "Beyond the Spectrum II" in tx and ("Abstract" in tx or "Metric Measure Geometry" in tx):
        starts.append(i)
out.append("trilogy pages %d; pages containing 'Beyond the Spectrum II' title: %s" % (len(tri), starts[:10]))
v2 = pymupdf.open(os.path.join(BTS, "volume_2_geometric_measures.pdf"))
v1 = pymupdf.open(os.path.join(BTS, "volume_1_functional_realizations.pdf"))
v2text = norm(" ".join(p.get_text() for p in v2))
v1text = norm(" ".join(p.get_text() for p in v1))
out.append("local vol2 pages %d" % len(v2))
# locate vol2 inside trilogy by matching first page text
first = norm(v2[0].get_text())[:300]
best = None
for i in range(len(tri)):
    r = difflib.SequenceMatcher(None, first, norm(tri[i].get_text())[:300]).ratio()
    if best is None or r > best[1]:
        best = (i, r)
s = best[0]
out.append("vol2 first page matches trilogy page %d ratio %.3f" % best)
trivol2 = norm(" ".join(tri[j].get_text() for j in range(s, min(s + len(v2), len(tri)))))
# save extracted volume 2
newdoc = pymupdf.open(); newdoc.insert_pdf(tri, from_page=s, to_page=min(s + len(v2), len(tri)) - 1)
newdoc.save(os.path.join(AUD, "zenodo_latest_vol2.pdf"))
def ratio(a, b):
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
# compare page by page (strip page numbers / running heads differences)
def pagewise(docA, offA, docB, n):
    rs = []
    for k in range(n):
        a = norm(docA[offA + k].get_text()); b = norm(docB[k].get_text())
        rs.append(difflib.SequenceMatcher(None, a, b).ratio())
    return rs
rs = pagewise(tri, s, v2, len(v2))
out.append("pagewise ratio Zenodo-trilogy-vol2 vs local vol2: min %.4f mean %.4f" % (min(rs), sum(rs) / len(rs)))
for k, r in enumerate(rs):
    if r < 0.98:
        a = norm(tri[s + k].get_text()); b = norm(v2[k].get_text())
        out.append(" page %d ratio %.3f" % (k + 1, r))
        for op in difflib.SequenceMatcher(None, a, b).get_opcodes():
            if op[0] != "equal":
                out.append("   %s Z:[%s] L:[%s]" % (op[0], a[op[1]:op[2]][:120], b[op[3]:op[4]][:120]))
# word-level diff of whole volume
wa = trivol2.split(); wb = v2text.split()
sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
ndiff = [op for op in sm.get_opcodes() if op[0] != "equal"]
out.append("word-level diff ops Zenodo vs local vol2: %d" % len(ndiff))
for op in ndiff[:40]:
    out.append("   %s Z:[%s] L:[%s]" % (op[0], " ".join(wa[op[1]:op[2]])[:150], " ".join(wb[op[3]:op[4]])[:150]))
# Local tex vs local vol2: check key phrases from the tex appear in the pdf text
tex = open(os.path.join(PAPER, "paper_geometric_measures_functional_tensors.tex"), encoding="utf8").read()
keys = ["Isospectral Separation Theorem", "Bottleneck Stability for Functional Realizations", "Conformal Invariance and Regularity Bounds",
        "Interface and Shock Direction Detection", "Non-Commutative Integration Formula", "Positivity and Entanglement Faithfulness",
        "Metric Properties on Matrix Varieties", "Displacement Convexity and Log-Sobolev Inequality", "Lean 4", "Atiyah--Patodi--Singer"]
for kq in keys:
    kp = kq.replace("--", "–")
    out.append("key '%s': in tex %s | in local vol2 pdf %s | in zenodo vol2 %s" % (kq, kq in tex, (kp in v2text) or (kq in v2text), (kp in trivol2) or (kq in trivol2)))
# negative control
neg = ratio(v1text[:20000], v2text[:20000])
out.append("NEGATIVE CONTROL vol1 vs vol2 ratio (must be low): %.3f" % neg)
txt = "\n".join(out); print(txt)
open(os.path.join(HERE, "compare_versions.out.txt"), "w", encoding="utf8").write(txt)
