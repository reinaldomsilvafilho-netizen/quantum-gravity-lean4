"""Resolve the paper's bibliography via Crossref (title/authors/year/pages)."""
import json, os, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
DOIS = {
    "atiyah1988topological": "10.1007/BF02698547",
    "verstraete2010continuous": "10.1103/PhysRevLett.104.190405",
    "ryu2006holographic": "10.1103/PhysRevLett.96.181602",
    "choquet1952": "10.1007/BF02392131",
    "bousso2016": "10.1103/PhysRevD.93.024017",
}
QUERIES = {"segal2004definition": "Segal The definition of conformal field theory Topology geometry and quantum field theory"}

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "audit-script (mailto:none@example.org)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

out = []
for key, doi in DOIS.items():
    try:
        m = get("https://api.crossref.org/works/" + doi)["message"]
        auth = "; ".join(f"{a.get('given','')} {a.get('family','')}" for a in m.get("author", []))
        yr = m.get("issued", {}).get("date-parts", [[None]])[0][0]
        out.append(f"{key}: DOI {doi} OK | {m.get('title',[''])[0]} | {auth} | {m.get('container-title',[''])[0]} {m.get('volume')} ({yr}) p.{m.get('page')} art.{m.get('article-number')}")
    except Exception as e:
        out.append(f"{key}: DOI {doi} FAILED {e}")
for key, q in QUERIES.items():
    m = get("https://api.crossref.org/works?rows=3&query.bibliographic=" + urllib.parse.quote(q))["message"]["items"]
    for it in m:
        yr = it.get("issued", {}).get("date-parts", [[None]])[0][0]
        out.append(f"{key} candidate: {it.get('DOI')} | {it.get('title',[''])[0]} | {it.get('container-title',[''])[0]} ({yr}) p.{it.get('page')}")
# negative control: a fabricated DOI must fail
try:
    get("https://api.crossref.org/works/10.1103/PhysRevLett.999.999999")
    out.append("NEGATIVE CONTROL FAILED: fake DOI resolved")
except Exception as e:
    out.append(f"negative control (fake DOI) correctly fails: {e}")
s = "\n".join(out)
print(s)
open(os.path.join(HERE, "crossref_check.out.txt"), "w", encoding="utf8").write(s)
