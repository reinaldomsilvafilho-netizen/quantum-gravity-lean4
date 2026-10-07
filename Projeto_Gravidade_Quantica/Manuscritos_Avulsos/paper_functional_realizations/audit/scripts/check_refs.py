"""Resolve every DOI of the Zenodo Volume I bibliography (Crossref, DataCite for 10.48550)
plus the references that the text should cite (De Silva-Lim, Hillar-Lim, Lovasz-Szegedy GAFA).
Prints title / first author / year / container. Negative control: a fake DOI must fail."""
import json
import sys
import urllib.request

DOIS = {
    "[1] Auffinger-BenArous-Cerny": "10.1002/cpa.21422",
    "[2] Evans-Gariepy": "10.1201/b18333",
    "[3] Lovasz-Szegedy 2006": "10.1016/j.jctb.2006.05.002",
    "[4] Lovasz book": "10.1090/coll/060",
    "[5] Lim 2005": "10.1109/CAMAP.2005.1574201",
    "[6] Qi 2005": "10.1016/j.jsc.2005.05.007",
    "[7] Rudin-Osher-Fatemi": "10.1016/0167-2789(92)90242-F",
    "[8] Milnor": "10.1515/9781400881802",
    "[9] Tomioka-Suzuki (arXiv)": "10.48550/arXiv.1407.1870",
    "[10] Nguyen-Drineas-Tran": "10.1093/imaiai/iav004",
    "missing: De Silva-Lim 2008": "10.1137/06066518X",
    "missing: Hillar-Lim 2013": "10.1145/2512329",
    "missing: Lovasz-Szegedy GAFA 2007": "10.1007/s00039-007-0599-6",
    "NEG CONTROL fake": "10.9999/fake.doi.000000",
}


def crossref(doi):
    url = "https://api.crossref.org/works/" + doi
    req = urllib.request.Request(url, headers={"User-Agent": "audit-script (mailto:none@example.org)"})
    with urllib.request.urlopen(req, timeout=40) as r:
        m = json.load(r)["message"]
    au = m.get("author", [{}])[0]
    yr = (m.get("issued", {}).get("date-parts", [[None]])[0] or [None])[0]
    return f"{m.get('title', [''])[0]} | {au.get('family', '')} | {yr} | {(m.get('container-title') or [''])[0]} | vol {m.get('volume')} pp {m.get('page')}"


def datacite(doi):
    with urllib.request.urlopen("https://api.datacite.org/dois/" + doi, timeout=40) as r:
        a = json.load(r)["data"]["attributes"]
    return f"{a['titles'][0]['title']} | {a['creators'][0]['name']} | {a['publicationYear']} | DataCite"


fails = 0
for k, doi in DOIS.items():
    try:
        out = datacite(doi) if doi.startswith("10.48550") else crossref(doi)
        print(f"OK   {k}: {doi}\n     {out}")
        if "NEG" in k:
            fails += 1
    except Exception as e:
        print(f"FAIL {k}: {doi} -> {e}")
        if "NEG" not in k:
            fails += 1
print("failures:", fails)
sys.exit(fails)
