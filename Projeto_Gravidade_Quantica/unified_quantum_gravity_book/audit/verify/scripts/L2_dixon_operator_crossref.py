"""L2 2026-09-28: resolve the 7 DOIs added by the Dixon and operator corrections via Crossref,
and compare with the bibitem data. Negative control: a mutated DOI must fail to resolve."""
import json
import urllib.request

DOIS = {
    "cohlvolkmer2025": ("10.1007/s11139-025-01064-z", "Cohl", "67"),
    "modesto2012": ("10.1103/PhysRevD.86.044005", "Modesto", "86"),
    "blas2009extra": ("10.1088/1126-6708/2009/10/029", "Blas", "2009"),
    "blas2011models": ("10.1007/JHEP04(2011)018", "Blas", "2011"),
    "pospelov2012lorentz": ("10.1103/PhysRevD.85.105001", "Pospelov", "85"),
    "calcagni2013probing": ("10.1103/PhysRevD.87.124028", "Calcagni", "87"),
    "marcinkiewicz1939": ("10.1007/BF01210677", "Marcinkiewicz", "44"),
    "NEG_mutated": ("10.1103/PhysRevD.85.105999", "Pospelov", "85"),
}


def get(doi):
    req = urllib.request.Request("https://api.crossref.org/works/" + doi,
                                 headers={"User-Agent": "L2-check (mailto:none@example.org)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["message"]


fails = 0
for key, (doi, author, vol) in DOIS.items():
    try:
        m = get(doi)
        authors = ", ".join(a.get("family", "") for a in m.get("author", []))
        ok = author in authors and vol in str(m.get("volume"))
        print(f"{key} | {doi} | {m.get('title', [''])[0]} | {authors} | "
              f"{(m.get('container-title') or [''])[0]} | vol {m.get('volume')} issue {m.get('issue')} "
              f"page {m.get('page')} art {m.get('article-number')} | {m.get('issued', {}).get('date-parts')}"
              f" | {'OK' if ok else 'MISMATCH'}")
        if key.startswith("NEG"):
            print("FAIL negative control resolved")
            fails += 1
        elif not ok:
            fails += 1
    except Exception as e:
        if key.startswith("NEG"):
            print(f"{key} | {doi} | does not resolve (expected): {e}")
        else:
            print(f"{key} | {doi} | FAIL {e}")
            fails += 1
print("TOTAL FAILS:", fails)
