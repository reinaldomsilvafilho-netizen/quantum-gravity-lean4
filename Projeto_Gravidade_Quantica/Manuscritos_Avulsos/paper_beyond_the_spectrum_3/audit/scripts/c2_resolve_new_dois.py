"""Resolve the DOIs added in the corrected version (Crossref / DataCite), with a mutated-DOI control."""
import sys
import json
import urllib.request

DOIS = {
    "Crooks1999": "10.1103/PhysRevE.60.2721",
    "KigamiLapidus1993": "10.1007/BF02097233",
    "Aamari2019": "10.1214/19-EJS1551",
    "Lindqvist1990": "10.1090/S0002-9939-1990-1007505-7",
    "GibsonEtAl1976": "10.1007/BFb0095244",
    "SilvaFilhoBTS": "10.5281/zenodo.22644743",
}
OUT = []


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "doi-check (mailto:none@example.org)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def resolve(doi):
    if doi.startswith("10.5281"):
        d = get("https://api.datacite.org/dois/" + doi)["data"]["attributes"]
        return ("datacite", d["titles"][0]["title"], d["creators"][0]["name"], d.get("publicationYear"),
                d.get("publisher"))
    m = get("https://api.crossref.org/works/" + doi)["message"]
    year = (m.get("published-print") or m.get("published-online") or m.get("issued"))["date-parts"][0][0]
    return ("crossref", m["title"][0], m["author"][0]["family"] if m.get("author") else None, year,
            (m.get("container-title") or [""])[0], m.get("volume"), m.get("page"))


fails = 0
for k, doi in DOIS.items():
    try:
        r = resolve(doi)
        OUT.append(f"== {k} | {doi}\n    {r}")
    except Exception as e:  # noqa: BLE001
        OUT.append(f"== {k} | {doi}\n    UNRESOLVED {e}")
        fails += 1
try:
    resolve("10.1103/PhysRevE.60.2721999")
    OUT.append("NEG CONTROL mutated DOI -> resolved (BAD)")
    fails += 1
except Exception:  # noqa: BLE001
    OUT.append("NEG CONTROL mutated DOI -> FAIL (expected)")
OUT.append(f"unresolved: {fails}")
print("\n".join(OUT))
with open(__file__.replace(".py", ".out.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(OUT) + "\n")
sys.exit(fails)
