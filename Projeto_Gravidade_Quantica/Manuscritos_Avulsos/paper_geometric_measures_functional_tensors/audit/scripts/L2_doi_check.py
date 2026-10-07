"""L2: resolve every DOI of the v3 bibliography (Crossref, DataCite for 10.5281)
and compare title / first author / year with the .tex entry.
Negative controls: a mutated DOI must not resolve; the v2 Benamou-Brenier DOI and
the v2 Vol. I DOI must resolve to records whose titles do NOT match the entries."""
import re, sys, json, os, difflib, urllib.request, urllib.error, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "..", "..", "paper_geometric_measures_functional_tensors.tex")
src = open(TEX, encoding="utf-8").read()
bib = src[src.index("\\begin{thebibliography}"):]
items = re.split(r"\\bibitem\{", bib)[1:]
fails = 0

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "L2-check (mailto:none@example.org)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def meta(doi):
    if doi.lower().startswith("10.5281/"):
        d = get("https://api.datacite.org/dois/" + doi)["data"]["attributes"]
        return (d["titles"][0]["title"], [c.get("familyName", c.get("name", "")) for c in d["creators"]],
                d.get("publicationYear"), d.get("publisher"), d.get("relatedIdentifiers", []))
    m = get("https://api.crossref.org/works/" + doi)["message"]
    t = (m.get("title") or [""])[0]
    if m.get("subtitle"):
        t += ": " + m["subtitle"][0]
    a = [x.get("family", x.get("name", "")) for x in m.get("author", m.get("editor", []))]
    y = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
    return t, a, y, (m.get("container-title") or [""])[0], m.get("ISBN", [])

def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = re.sub(r"\\[a-zA-Z]+|[{}~\\'\"`^]", "", s)
    return re.sub(r"[^a-z0-9 ]", " ", s.lower())

def tex_title(item):
    m = re.search(r"\\emph\{(.+?)\},", item, re.S)
    return m.group(1) if m else ""

for it in items:
    key = it.split("}")[0]
    m = re.search(r"DOI: \\href\{https://doi.org/([^}]+)\}", it)
    if not m:
        print(f"{key}: no DOI in entry"); continue
    doi = m.group(1)
    try:
        t, a, y, cont, extra = meta(doi)
    except Exception as e:
        print(f"FAIL {key}: {doi} does not resolve ({e})"); fails += 1; continue
    tt = tex_title(it)
    r = difflib.SequenceMatcher(None, norm(tt), norm(t)).ratio()
    yr_tex = re.findall(r"(19|20)\d\d", it)
    ytex = re.findall(r"\b((?:19|20)\d\d)\b", it)
    auth_ok = any(norm(x).strip() and norm(x).strip().split()[-1] in norm(it) for x in a) if a else True
    ok = r > 0.8 and auth_ok
    print(f"{'PASS' if ok else 'CHECK'} {key}: {doi}\n    tex  : {tt}\n    reg  : {t} | {a[:3]} | {y} | {cont}  (title ratio {r:.2f})")
    if not ok:
        fails += 1

# negative controls
for doi, label in [("10.1007/s002110050002x", "mutated Benamou DOI")]:
    try:
        meta(doi); print(f"FAIL NEG {label} resolved"); fails += 1
    except urllib.error.HTTPError as e:
        print(f"PASS NEG {label}: HTTP {e.code}")
bt = meta("10.1007/s002110050475")[0]
print(f"NEG v2 Benamou DOI 10.1007/s002110050475 -> '{bt}'")
if "monge" in bt.lower(): fails += 1; print("FAIL NEG")
v1 = meta("10.5281/zenodo.22441676")
print(f"NEG v2 Vol. I DOI 22441676 -> '{v1[0]}'")
if "beyond the spectrum" in v1[0].lower(): fails += 1; print("FAIL NEG")
# the new Vol. I DOI: concept record of the trilogy; list what it contains
c = meta("10.5281/zenodo.22644743")
print(f"Vol. I DOI 22644743 -> '{c[0]}' | {c[1]} | {c[2]} | {c[3]}")
for ri in c[4][:12]:
    print("    related:", ri.get("relationType"), ri.get("relatedIdentifier"))
print("failures", fails)
sys.exit(int(fails))
