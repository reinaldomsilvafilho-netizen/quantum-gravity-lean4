"""Camada 2 (F-45..F-50): resolve every NEW DOI of chapters 1-6 via the Crossref API
and compare title / first-author family name / year / volume with the bibliography entry.

Negative control: a mutated DOI (last character changed) must NOT resolve to the same
title, and a deliberately wrong expected title must be flagged as a mismatch.
Run from the book folder:  python audit/verify/scripts/L2_ch01_ch06_crossref.py
"""
import json
import re
import unicodedata
import urllib.parse
import urllib.request

# (chapter, doi, expected title fragment, expected first-author family, year, volume)
ENTRIES = [
    ("ch1", "10.1016/j.laa.2011.05.040", "number of eigenvalues of a tensor", "Cartwright", 2013, "438"),
    ("ch1", "10.1007/BF01236935", "integral formula for total gradient variation", "Fleming", 1960, "11"),
    ("ch1", "10.1007/s00039-007-0599-6", "lemma for the analyst", "Lov", 2007, "17"),
    ("ch2", "10.1080/00268976400100041", "variational solution of the time-dependent", "McLachlan", 1964, "8"),
    ("ch2", "10.1137/090752286", "tensor-train decomposition", "Oseledets", 2011, "33"),
    ("ch2", "10.2969/aspm/05710463", "wasserstein geometry of gaussian measures", "Takatsu", 2010, None),
    ("ch3", "10.1080/00150517.1971.12431015", "hidden hexagon squares", "Hoggatt", 1971, "9"),
    ("ch3", "10.1016/C2010-0-64839-5", "table of integrals, series, and products", None, 2015, None),
    ("ch4", "10.1017/S0308210512001783", "spectrum of two different fractional operators", "Servadei", 2014, "144"),
    ("ch4", "10.1137/1.9781611972030", "elliptic problems in nonsmooth domains", "Grisvard", 2011, None),
    ("ch4", "10.1007/978-3-642-12245-3", "polyharmonic boundary value problems", "Gazzola", 2010, None),
    ("ch6", "10.1007/BF02097233", "weyl's problem for the spectral distribution", "Kigami", 1993, "158"),
]


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


def fetch(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": "book-audit/1.0 (mailto:noreply@example.org)"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)["message"]


def compare(msg, title, fam, year, vol):
    t = " ".join(norm((msg.get("title") or [""])[0]))
    ok_t = " ".join(norm(title)) in t
    authors = msg.get("author") or msg.get("editor") or []
    fams = [a.get("family", "") for a in authors]
    ok_a = fam is None or any(f.lower().startswith(fam.lower()) or fam.lower() in f.lower() for f in fams)
    yrs = []
    for key in ("published-print", "issued", "published-online", "published"):
        dp = (msg.get(key) or {}).get("date-parts") or [[None]]
        if dp[0][0]:
            yrs.append(dp[0][0])
    ok_y = year in yrs
    ok_v = vol is None or msg.get("volume") == vol
    return ok_t, ok_a, ok_y, ok_v, t[:70], fams[:3], yrs, msg.get("volume"), msg.get("page")


fails = []
for ch, doi, title, fam, year, vol in ENTRIES:
    try:
        m = fetch(doi)
    except Exception as e:  # noqa: BLE001
        print("ERR ", ch, doi, e)
        fails.append(doi)
        continue
    ok_t, ok_a, ok_y, ok_v, t, fams, yrs, v, pg = compare(m, title, fam, year, vol)
    flag = "OK  " if (ok_t and ok_a and ok_y and ok_v) else "MISM"
    if flag != "OK  ":
        fails.append(doi)
    print(flag, ch, doi, "| title:", t, "| authors:", fams, "| years:", yrs, "| vol", v, "pp", pg,
          "| checks t/a/y/v:", ok_t, ok_a, ok_y, ok_v)

# negative controls
print("-- negative controls --")
m = fetch("10.1007/BF02097233")
ok_t, *_ = compare(m, "number of eigenvalues of a tensor", "Cartwright", 1993, "158")
print("NEG wrong expected title flagged:", not ok_t)
try:
    m2 = fetch("10.1007/BF02097234")
    ok_t2, *_ = compare(m2, "weyl's problem for the spectral distribution", "Kigami", 1993, "158")
    print("NEG mutated DOI does not give the Kigami-Lapidus title:", not ok_t2, "|", (m2.get("title") or [""])[0][:60])
except Exception as e:  # noqa: BLE001
    print("NEG mutated DOI does not resolve:", True, "|", e)
print("\nMISMATCHES/ERRORS:", fails if fails else "none")
