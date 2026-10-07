"""Resolve every DOI cited in the revised paper via Crossref or DataCite and print
title / authors / year / venue, plus the abstract when available, for attribution checks.
Negative control: a fabricated DOI must fail to resolve. Exit code = number of failures."""
import json, sys, os, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
CROSSREF = {
    "atiyah1988": "10.1007/BF02698547",
    "verstraete2010": "10.1103/PhysRevLett.104.190405",
    "ryu2006": "10.1103/PhysRevLett.96.181602",
    "fouresbruhat1952": "10.1007/BF02392131",
    "bousso2016": "10.1103/PhysRevD.93.024017",
    "godel1949": "10.1103/RevModPhys.21.447",
}
DATACITE = {"silvafilho_book": "10.5281/zenodo.22290043"}
FAKE = "10.1103/PhysRevLett.999.999999"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "doi-check/1.0 (mailto:none)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf8"))


out, fails = [], 0
for key, doi in CROSSREF.items():
    try:
        m = get(f"https://api.crossref.org/works/{doi}")["message"]
        au = "; ".join(f"{a.get('given', '')} {a.get('family', '')}".strip() for a in m.get("author", []))
        yr = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
        out.append(f"{key}: OK {doi} | {m.get('title', [''])[0]} | {au} | {(m.get('container-title') or [''])[0]} "
                   f"{m.get('volume', '')} ({yr}) p.{m.get('page', '')} art.{m.get('article-number', '')}")
        if m.get("abstract"):
            out.append(f"    abstract: {m['abstract'][:900]}")
    except Exception as e:  # noqa: BLE001
        fails += 1
        out.append(f"{key}: FAIL {doi} {e}")
for key, doi in DATACITE.items():
    try:
        a = get(f"https://api.datacite.org/dois/{doi}")["data"]["attributes"]
        out.append(f"{key}: OK {doi} | {a['titles'][0]['title']} | "
                   f"{'; '.join(c['name'] for c in a['creators'])} | {a.get('publisher')} ({a.get('publicationYear')})")
    except Exception as e:  # noqa: BLE001
        fails += 1
        out.append(f"{key}: FAIL {doi} {e}")
try:
    get(f"https://api.crossref.org/works/{FAKE}")
    fails += 1
    out.append("negative control FAILED: fake DOI resolved")
except urllib.error.HTTPError as e:
    out.append(f"negative control OK: fake DOI -> {e}")
s = "\n".join(out) + f"\nFAILURES: {fails}"
print(s)
open(os.path.join(HERE, "doi_check_v2.out.txt"), "w", encoding="utf8").write(s)
sys.exit(fails)
