"""Step 0: find latest Zenodo version of concept 22441676, download PDF, compare to local .tex."""
import json, os, re, sys, urllib.request, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.dirname(HERE)
PAPER = os.path.dirname(AUD)

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "audit-script"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

out = []
d = json.loads(get("https://zenodo.org/api/records?q=conceptrecid:22441676&all_versions=true&sort=mostrecent&size=25"))
hits = d["hits"]["hits"]
for h in hits:
    m = h["metadata"]
    out.append(f"id={h['id']} version={m.get('version')} date={m.get('publication_date')} title={m.get('title')}")
    for f in h.get("files", []):
        out.append(f"   file {f['key']} size={f['size']} {f['links']['self']}")
latest = max(hits, key=lambda h: (h["metadata"].get("publication_date", ""), h["id"]))
out.append(f"LATEST id={latest['id']} date={latest['metadata'].get('publication_date')}")
pdfs = [f for f in latest.get("files", []) if f["key"].lower().endswith(".pdf")]
pdfpath = os.path.join(AUD, "zenodo_latest.pdf")
if pdfs:
    open(pdfpath, "wb").write(get(pdfs[0]["links"]["self"]))
    out.append(f"downloaded {pdfs[0]['key']} -> {pdfpath}")
    out.append("description: " + re.sub("<[^>]+>", " ", latest["metadata"].get("description", ""))[:1500])

import fitz
txt = "".join(p.get_text() for p in fitz.open(pdfpath))
open(os.path.join(HERE, "zenodo_latest.txt"), "w", encoding="utf8").write(txt)
tex = open(os.path.join(PAPER, "paper_functorial_tensor_field_theory.tex"), encoding="utf8").read()

def words(s):
    s = re.sub(r"\\[a-zA-Z]+", " ", s)
    return re.findall(r"[A-Za-z]{4,}", s.lower())

wt, wp = words(tex), words(txt)
sm = difflib.SequenceMatcher(None, wt, wp, autojunk=False)
out.append(f"word-sequence similarity ratio tex vs zenodo pdf: {sm.ratio():.4f} (tex {len(wt)} words, pdf {len(wp)} words)")
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != "equal" and (i2 - i1 + j2 - j1) > 3:
        out.append(f"  {tag}: TEX[{' '.join(wt[i1:i2][:25])}] PDF[{' '.join(wp[j1:j2][:25])}]")
# negative control: similarity with shuffled text must be low
import random
random.seed(0)
sh = wp[:]; random.shuffle(sh)
out.append(f"negative control (shuffled pdf words) ratio: {difflib.SequenceMatcher(None, wt, sh, autojunk=False).ratio():.4f}")
# local pdf too
lp = os.path.join(PAPER, "paper_functorial_tensor_theory.pdf")
if os.path.exists(lp):
    lt = "".join(p.get_text() for p in fitz.open(lp))
    out.append(f"local pdf vs zenodo pdf ratio: {difflib.SequenceMatcher(None, words(lt), wp, autojunk=False).ratio():.4f}")
s = "\n".join(out)
print(s)
open(os.path.join(HERE, "zenodo_check.out.txt"), "w", encoding="utf8").write(s)
