"""Camada 2 (F-37..F-40): citation consistency and DOI resolution.

1. For each chapter, every \\cite key must have a \\bibitem and every \\bibitem must be cited.
2. Every DOI newly added by the corrector is resolved through the Crossref API
   (DataCite for 10.48550/10.5281); title/authors/year are printed and compared
   with the bibitem by token overlap.
Negative control: a mutated DOI (last char changed) must NOT resolve, and a
wrong title must fail the overlap test.
"""
import json
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CHAPS = {
    "ch07": "chap07_minimax_extrinsic_curvature_submanifolds.tex",
    "ch09": "chap09_global_homotopy_covering_spaces_jordan_loops.tex",
    "ch10": "chap10_information_geometry_minimax_deep_learning.tex",
    "ch11": "chap11_emergent_spacetime_tensor_networks_holonomies.tex",
}
# DOIs added (or keys renamed) by the corrector, per fixes_F37-F40.md
NEW = {
    "ch07": ["fenchel1929", "lewicka2020"],
    "ch09": ["boone1959", "lieutier2004"],
    "ch10": ["zhang2021"],
    "ch11": ["goroff1986", "petz1996", "bisognano1976", "casini2011",
             "faulkner2013quantum", "dong2018entropy", "miyaji2015cmera",
             "hayden2016random", "immirzi1997", "rovelli1998immirzi", "ledoux2001"],
}


def bib_entries(tex):
    body = tex.split("\\begin{thebibliography}")[1]
    parts = re.split(r"\\bibitem\{([^}]+)\}", body)
    out = {}
    for i in range(1, len(parts), 2):
        out[parts[i]] = parts[i + 1]
    return out


def cites(tex):
    main = tex.split("\\begin{thebibliography}")[0]
    keys = set()
    for m in re.finditer(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", main):
        keys.update(k.strip() for k in m.group(1).split(","))
    return keys


def fetch(doi):
    url = "https://api.crossref.org/works/" + doi
    try:
        with urllib.request.urlopen(urllib.request.Request(
                url, headers={"User-Agent": "L2-verifier (mailto:none@example.org)"}), timeout=30) as r:
            m = json.load(r)["message"]
            title = " ".join(m.get("title", [""]))
            auth = ", ".join(a.get("family", "") for a in m.get("author", []))
            yr = (m.get("issued", {}).get("date-parts", [[None]])[0] or [None])[0]
            yr = f"{yr} vol {m.get('volume','-')} pp {m.get('page','-')} {(m.get('container-title') or ['-'])[0][:40]}"
            return "crossref", title, auth, yr
    except urllib.error.HTTPError as e:
        if e.code != 404:
            return "error %d" % e.code, "", "", None
    try:
        with urllib.request.urlopen("https://api.datacite.org/dois/" + doi, timeout=30) as r:
            a = json.load(r)["data"]["attributes"]
            title = a["titles"][0]["title"]
            auth = ", ".join(c.get("familyName", c.get("name", "")) for c in a["creators"])
            return "datacite", title, auth, a.get("publicationYear")
    except Exception:
        return "unresolved", "", "", None


def toks(s):
    s = re.sub(r"\\[a-zA-Z]+|[{}$\\\"'`~^]", " ", s.lower())
    return {w for w in re.findall(r"[a-z]{4,}", s)}


def overlap(bib_title, cr_title):
    a, b = toks(bib_title), toks(cr_title)
    return len(a & b) / max(1, len(b))


bad = 0
for ch, fn in CHAPS.items():
    tex = (ROOT / fn).read_text(encoding="utf8")
    bib = bib_entries(tex)
    c = cites(tex)
    missing, unused = sorted(c - set(bib)), sorted(set(bib) - c)
    print(f"[{ch}] cited-not-in-bib: {missing}  bib-not-cited: {unused}")
    bad += bool(missing) + bool(unused)
    for key in NEW[ch]:
        entry = bib.get(key, "")
        m = re.search(r"doi\.org/([^}\s]+)\}", entry) or re.search(r"\\doi\{([^}]+)\}", entry)
        tm = re.search(r"\\emph\{(.+?)\},\s*\n", entry, re.S)
        btitle = tm.group(1) if tm else entry[:120]
        if not m:
            print(f"   {key}: NO DOI in bibitem")
            bad += 1
            continue
        doi = m.group(1)
        src, t, a, y = fetch(doi)
        ov = overlap(btitle, t)
        ok = src in ("crossref", "datacite") and ov >= 0.6
        bad += not ok
        print(f"   {key}: {doi} [{src}] {y} | {a[:60]} | '{t[:90]}' | title-overlap {ov:.2f} -> {'OK' if ok else 'CHECK'}")
        time.sleep(0.3)

# negative controls
src, tt, aa, _ = fetch("10.1007/BF01454837")      # mutated Fenchel DOI
ovm = overlap("Uber Krummung und Windung geschlossener Raumkurven", tt)
print("NEG mutated DOI 10.1007/BF01454837 ->", src, repr(tt[:60]), aa[:30], "overlap", round(ovm, 2),
      "-> must be < 0.6:", ovm < 0.6)
_, t, _, _ = fetch("10.1007/BF01454836")
print("NEG wrong-title overlap:", round(overlap("Holographic quantum error correcting codes", t), 2),
      "-> must be < 0.6:", overlap("Holographic quantum error correcting codes", t) < 0.6)
print("TOTAL ISSUES:", bad)
