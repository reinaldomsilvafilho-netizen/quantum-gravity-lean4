"""Layer-2 text checks for a volume: DOIs (Crossref / DataCite metadata vs the bibitem),
declarations block vs _staging/DECLARACOES_PADRAO_ARTIGOS.tex (volume variant),
affiliation, house style, forbidden claims, and the release notes.

usage: python L2_text_refs.py <paper.tex> <notes1.md> [<notes2.md> ...]
Negative controls: a mutated DOI must fail to resolve; a mutated declarations block
(one word changed) must fail the equality test.
"""
import sys
import re
import json
import difflib
import unicodedata
import urllib.request
from pathlib import Path

fails = 0
out = []


def log(s):
    print(s.encode("ascii", "replace").decode())
    out.append(s)


def check(name, ok):
    global fails
    log(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        fails += 1


tex_path = Path(sys.argv[1])
notes = [Path(p) for p in sys.argv[2:]]
tex = tex_path.read_text(encoding="utf-8")
root = Path(__file__).resolve().parents[4]
std = (root / "_staging" / "DECLARACOES_PADRAO_ARTIGOS.tex").read_text(encoding="utf-8")


def fetch(doi):
    for url in (f"https://api.crossref.org/works/{doi}", f"https://api.datacite.org/dois/{doi}"):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "L2-check/1.0"})
            with urllib.request.urlopen(req, timeout=40) as r:
                d = json.load(r)
            if "crossref" in url:
                m = d["message"]
                return ("crossref", (m.get("title") or [""])[0],
                        (m.get("author") or [{}])[0].get("family", ""),
                        (m.get("issued", {}).get("date-parts") or [[None]])[0][0])
            a = d["data"]["attributes"]
            return ("datacite", a["titles"][0]["title"], a["creators"][0].get("name", ""),
                    a.get("publicationYear"))
        except Exception:
            continue
    return None


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = re.sub(r"\\[a-zA-Z]+|[{}$\\^_~'`\"]", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


log(f"== DOIs in {tex_path.name} ==")
bib = tex[tex.find("\\begin{thebibliography}"):]
items = re.split(r"\\bibitem\{", bib)[1:]
for it in items:
    key = it[:it.find("}")]
    m = re.search(r"doi\.org/([^}\s]+)\}", it)
    title_m = re.search(r"\\emph\{(.+?)\},", it, re.S)
    btitle = title_m.group(1) if title_m else ""
    if not m:
        url = re.search(r"\\(?:href|url)\{([^}]+)\}", it)
        log(f"{key}: no DOI; link {url.group(1) if url else None}")
        continue
    doi = m.group(1)
    md = fetch(doi)
    if md is None:
        check(f"{key} {doi} resolves", False)
        continue
    sim = difflib.SequenceMatcher(None, norm(btitle), norm(md[1])).ratio()
    year_ok = str(md[3]) in it
    auth_ok = norm(md[2].split(",")[0]).split()[-1] in norm(it) if md[2] else False
    log(f"{key}: {md[0]} '{md[1][:70]}' {md[2]} {md[3]} | title sim {sim:.2f} year-in-item {year_ok} author-in-item {auth_ok}")
    check(f"{key}: resolves, title sim >= 0.85, year and first author match",
          sim >= 0.85 and year_ok and auth_ok)
check("negative control: mutated DOI does not resolve", fetch("10.1103/PhysRevLett.78.26909999") is None)

log("== Declarations ==")


def block(s):
    i = s.find("\\section*{Declarations}")
    j = s.find("\\begin{thebibliography}", i) if "\\begin{thebibliography}" in s[i:] else len(s)
    b = s[i:j]
    b = re.sub(r"%[^\n]*", "", b)
    return re.sub(r"\s+", " ", b).strip()


s_std = block(std).replace("[paper/volume]", "volume").replace("[If Lean files exist:] ", "")
s_tex = block(tex)
# the paper block may carry extra trailing material (e.g. licence line); compare the standard prefix
check("declarations block equals the standard (volume variant, Lean sentence)", s_tex.startswith(s_std))
if not s_tex.startswith(s_std):
    sm = difflib.SequenceMatcher(None, s_std, s_tex)
    for op in sm.get_opcodes():
        if op[0] != "equal":
            log(f"   diff {op[0]}: std='{s_std[op[1]:op[2]]}' tex='{s_tex[op[3]:op[4]]}'")
extra = s_tex[len(s_std):].strip() if s_tex.startswith(s_std) else ""
log(f"   extra text after the standard block: '{extra[:200]}'")
check("negative control: mutated block fails", not s_tex.startswith(s_std.replace("extensively", "occasionally")))

log("== Affiliation ==")
aff = re.search(r"\\address\{([^}]*)\}", tex)
aff = aff.group(1) if aff else ""
log(f"   {aff}")
check("affiliation: Master's student, PPGEE/DES, UFLA, Statistics and Agricultural Experimentation",
      aff.startswith("Master's student, Postgraduate Program in Statistics and Agricultural Experimentation (PPGEE/DES)")
      and "UFLA" in aff)

log("== House style / forbidden claims in the .tex body (outside Declarations) ==")
body = tex[:tex.find("\\section*{Declarations}")]
body_nc = re.sub(r"(?<!\\)%[^\n]*", "", body)
pats = [r"earlier version", r"withdrawn", r"\bcorrected\b", r"audit/", r"machine-checked", r"formally verified",
        r"\bLean\b", r"GitHub", r"pending", r"\bv2\b", r"previous version", r"rigorously", r"definitively"]
for p in pats:
    hits = [(m.start(), body_nc[max(0, m.start() - 40):m.end() + 40].replace("\n", " "))
            for m in re.finditer(p, body_nc, re.I)]
    for h in hits:
        log(f"   '{p}': ...{h[1]}...")
    check(f"no '{p}' in body", not hits)

log("== Notes ==")
for nf in notes:
    t = nf.read_text(encoding="utf-8")
    for p in (r"github", r"pending", r"TODO", r"layer 2", r"layer-2"):
        hits = [t[max(0, m.start() - 60):m.end() + 60].replace("\n", " ") for m in re.finditer(p, t, re.I)]
        for h in hits:
            log(f"   {nf.name} '{p}': ...{h}...")
        check(f"{nf.name}: no '{p}'", not hits)

log(f"failures: {fails}")
outp = Path(__file__).with_suffix("").as_posix() + "_" + tex_path.stem + ".out.txt"
Path(outp).write_text("\n".join(out) + "\n", encoding="utf-8")
sys.exit(fails)
