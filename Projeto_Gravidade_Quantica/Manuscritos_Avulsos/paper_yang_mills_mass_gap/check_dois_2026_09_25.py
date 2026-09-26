"""Resolve every DOI of the Yang-Mills manuscript against Crossref (DataCite via doi.org for Zenodo).

Usage: python check_dois_2026_09_25.py  -> prints DOI | status | first author | year | title
"""
import json
import re
import sys
import urllib.parse
import urllib.request

TEX = "paper_yang_mills_mass_gap.tex"
dois = sorted(set(re.findall(r"\\href\{https://doi\.org/([^}]+)\}", open(TEX, encoding="utf-8").read())))
bad = 0
for d in dois:
    if d.startswith("10.5281/zenodo"):
        req = urllib.request.Request("https://doi.org/" + d, method="HEAD")
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                print(f"{d} | {r.status} | (DataCite/Zenodo) | {r.geturl()}")
        except Exception as e:  # noqa: BLE001
            bad += 1
            print(f"{d} | ERROR {e}")
        continue
    url = "https://api.crossref.org/works/" + urllib.parse.quote(d, safe="")
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            m = json.load(r)["message"]
        au = (m.get("author") or [{}])[0].get("family", "?")
        yr = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
        ti = (m.get("title") or ["?"])[0]
        print(f"{d} | 200 | {au} | {yr} | {ti}")
    except Exception as e:  # noqa: BLE001
        bad += 1
        print(f"{d} | ERROR {e}")
print(f"{len(dois)} DOIs, {bad} unresolved")
sys.exit(1 if bad else 0)
