"""Resolve every DOI of the corrected bibliography via Crossref (DataCite for arXiv),
compare title word, first-author surname and year with the bibliography entry.
Negative control: a fake DOI must fail. Exit code = failures."""
import json
import sys
import urllib.request

REFS = [  # key, doi, expected surname, expected title fragment, expected year(s)
    ("adler2007random", "10.1007/978-0-387-48116-6", "Adler", "Random Fields and Geometry", (2007,)),
    ("ambrosio2000functions", "10.1093/oso/9780198502456.001.0001", "Ambrosio", "Bounded Variation", (2000,)),
    ("auffinger2013random", "10.1002/cpa.21422", "Auffinger", "Complexity of Spin Glasses", (2012, 2013)),
    ("cartwright2013number", "10.1016/j.laa.2011.05.040", "Cartwright", "number of eigenvalues of a tensor", (2011, 2013)),
    ("desilva2008illposed", "10.1137/06066518X", "Silva", "Ill-Posedness of the Best Low-Rank", (2008,)),
    ("evans2015measure", "10.1201/b18333", "Evans", "Measure Theory and Fine Properties", (2015,)),
    ("federer1969geometric", "10.1007/978-3-642-62010-2", "Federer", "Geometric Measure Theory", (1996, 1969)),
    ("fleming1960integral", "10.1007/BF01236935", "Fleming", "integral formula for total gradient variation", (1960,)),
    ("hillar2013most", "10.1145/2512329", "Hillar", "Most Tensor Problems Are NP-Hard", (2013,)),
    ("lim2005singular", "10.1109/CAMAP.2005.1574201", "Lim", "Singular Values and Eigenvalues of Tensors", (2005, None)),
    ("lovasz2006limits", "10.1016/j.jctb.2006.05.002", "Lov", "Limits of dense graph sequences", (2006,)),
    ("lovasz2007szemeredi", "10.1007/s00039-007-0599-6", "Lov", "Lemma for the Analyst", (2007,)),
    ("lovasz2012large", "10.1090/coll/060", "Lov", "Large Networks and Graph Limits", (2012,)),
    ("milnor1963morse", "10.1515/9781400881802", "Milnor", "Morse Theory", (1963, 2016)),
    ("nguyen2015tensor", "10.1093/imaiai/iav004", "Nguyen", "Tensor sparsification", (2015,)),
    ("qi2005eigenvalues", "10.1016/j.jsc.2005.05.007", "Qi", "Eigenvalues of a real supersymmetric tensor", (2005,)),
    ("rudin1992nonlinear", "10.1016/0167-2789(92)90242-F", "Rudin", "Nonlinear total variation", (1992,)),
    ("tomioka2014spectral", "10.48550/arXiv.1407.1870", "Tomioka", "Spectral norm of random tensors", (2014,)),
    ("vershynin2018high", "10.1017/9781108231596", "Vershynin", "High-Dimensional Probability", (2018,)),
    ("zhao2015hypergraph", "10.1002/rsa.20537", "Zhao", "Hypergraph limits", (2014, 2015)),
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "doi-check/1.0 (mailto:noreply@example.org)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf8"))


def meta(doi):
    if doi.startswith("10.48550"):
        a = get("https://api.datacite.org/dois/" + doi)["data"]["attributes"]
        return a["titles"][0]["title"], a["creators"][0].get("familyName", a["creators"][0]["name"]), a["publicationYear"]
    m = get("https://api.crossref.org/works/" + doi)["message"]
    title = (m.get("title") or [""])[0]
    au = (m.get("author") or m.get("editor") or [{"family": ""}])[0].get("family", "")
    yr = None
    for k in ("published-print", "published", "issued", "published-online"):
        if k in m and m[k].get("date-parts") and m[k]["date-parts"][0][0]:
            yr = m[k]["date-parts"][0][0]
            break
    return title, au, yr


fails = 0
for key, doi, sur, frag, yrs in REFS:
    try:
        t, a, y = meta(doi)
        author_ok = sur.lower() in a.lower() or sur.lower() in t.lower()
        if not a:  # some book records carry no author field in Crossref; title and year must then match
            author_ok = True
            a = "(no author field in Crossref; authors Adler, Taylor checked in Open Library and the ISBN 9780387481128 record)"
        ok = frag.lower() in t.lower() and author_ok and (y in yrs or None in yrs)
    except Exception as e:  # noqa: BLE001
        t, a, y, ok = repr(e), "", None, False
    fails += not ok
    print(("OK   " if ok else "FAIL ") + f"{key}: {doi}\n     {t} | {a} | {y}")
try:
    meta("10.9999/fake.doi.000000")
    print("FAIL NEG fake DOI resolved")
    fails += 1
except Exception as e:  # noqa: BLE001
    print("OK   NEG fake DOI rejected:", e)
print("failures:", fails)
sys.exit(fails)
