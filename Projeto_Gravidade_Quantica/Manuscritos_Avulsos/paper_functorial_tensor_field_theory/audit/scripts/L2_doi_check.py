"""Layer-2 DOI check: resolve every DOI of the revised paper via Crossref (DataCite for Zenodo) and compare
title words, first-author surname, year, volume and first page with the bibliography as printed.
Negative controls: a fake DOI must 404; a mutated expected volume must be detected. Exit = failures."""
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "L2-doi-check (mailto:none@example.org)"}
# (doi, title fragment, author surname, year, volume, first page) as printed in the .tex
BIB = [
    ("10.5281/zenodo.22290043", "geometry, tensors, and quantum gravity", "silva-filho", 2026, None, None),
    ("10.1007/BF02698547", "topological quantum field theory", "atiyah", 1988, "68", "175"),
    ("10.1103/PhysRevLett.104.190405", "continuous matrix product states for quantum fields", "verstraete", 2010, "104", "190405"),
    ("10.1103/PhysRevLett.96.181602", "holographic derivation of entanglement entropy", "ryu", 2006, "96", "181602"),
    ("10.1007/BF02392131", "théorème d'existence pour certains systèmes", "bruhat", 1952, "88", "141"),
    ("10.1103/PhysRevD.93.024017", "proof of the quantum null energy condition", "bousso", 2016, "93", "024017"),
    ("10.1103/RevModPhys.21.447", "an example of a new type of cosmological solutions", "del", 1949, "21", "447"),
]


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.loads(r.read().decode("utf8"))


def meta(doi):
    if doi.startswith("10.5281"):
        a = get(f"https://api.datacite.org/dois/{doi}")["data"]["attributes"]
        return (a["titles"][0]["title"], a["creators"][0]["name"], int(a["publicationYear"]), None, None)
    m = get(f"https://api.crossref.org/works/{doi}")["message"]
    y = (m.get("published-print") or m.get("published-online") or m.get("issued"))["date-parts"][0][0]
    page = (m.get("page") or m.get("article-number") or "").split("-")[0]
    return (m["title"][0], m["author"][0]["family"], y, m.get("volume"), page)


def match(rec, exp):
    t, a, y, v, p = rec
    _, tf, au, ye, vo, pg = exp
    return (tf in t.lower().replace("–", "-") and au in a.lower() and y == ye
            and (vo is None or v == vo) and (pg is None or p == pg))


log, fails = [], 0
for e in BIB:
    try:
        rec = meta(e[0])
        ok = match(rec, e)
        log.append(f"[{'PASS' if ok else 'FAIL'}] {e[0]}: {rec}")
        fails += 0 if ok else 1
        if e[0] == "10.1007/BF02698547":
            mut = (e[0], e[1], e[2], e[3], "69", e[5])
            okc = not match(rec, mut)
            log.append(f"[{'PASS' if okc else 'FAIL'}] control: mutated volume 69 detected = {okc}")
            fails += 0 if okc else 1
    except Exception as ex:  # noqa: BLE001
        log.append(f"[FAIL] {e[0]}: {ex}"); fails += 1
try:
    get("https://api.crossref.org/works/10.1103/PhysRevLett.999.999999")
    log.append("[FAIL] control: fake DOI resolved"); fails += 1
except Exception as ex:  # noqa: BLE001
    log.append(f"[PASS] control: fake DOI -> {ex}")
out = "\n".join(log) + f"\nFAILED CHECKS: {fails}"
print(out)
open(os.path.join(HERE, "L2_doi_check.out.txt"), "w", encoding="utf8").write(out)
sys.exit(fails)
