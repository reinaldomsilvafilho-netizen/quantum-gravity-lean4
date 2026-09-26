"""L2 residual check (2026-09-25): new DOIs on Crossref, cite/bibitem
consistency, revision-history wording and audit/ paths, and presence of
content confirmed in earlier L2 reports (chapters 7-12).
Run from the book folder.
"""
import glob
import json
import re
import urllib.request

FAILS = []


def check(name, cond):
    print(("OK   " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def crossref(doi):
    req = urllib.request.Request("https://api.crossref.org/works/" + doi,
                                 headers={"User-Agent": "book-audit/1.0 (mailto:none@example.org)"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.load(r)["message"]
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


def words(s):
    return set(re.findall(r"[a-z]+", s.lower())) - {"of", "the", "a", "and", "on", "to", "in"}


def jacc(a, b):
    A, B = words(a), words(b)
    return len(A & B) / max(1, len(A | B))


NEW = {
    "10.1016/S1385-7258(58)50051-1": ("On a free group of rotations of the Euclidean space", "Świerczkowski", "61", 1958),
    "10.2307/2006973": ("Varieties of group representations and splittings of 3-manifolds", "Culler", "117", 1983),
    "10.1103/PhysRevD.84.104018": ("From dispersion relations to spectral dimension---and back again", "Sotiriou", "84", 2011),
}
for doi, (title, author, vol, year) in NEW.items():
    m = crossref(doi)
    if "error" in m:
        check("DOI %s resolves" % doi, False)
        continue
    t = (m.get("title") or [""])[0]
    fam = " ".join(a.get("family", "") for a in m.get("author", []))
    y = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
    print("     %s -> %s | %s | vol %s | %s | pages %s" % (doi, t, fam, m.get("volume"), y, m.get("page")))
    check("DOI %s: title matches" % doi, jacc(t, title) > 0.6)
    check("DOI %s: first author matches" % doi, author.lower()[1:6] in fam.lower() or author.lower() in fam.lower())
    check("DOI %s: volume %s, year %s" % (doi, vol, year), str(m.get("volume")) == vol and y == year)
# negative control: neighbouring DOI must not match the SVW title
m = crossref("10.1103/PhysRevD.84.104017")
t = (m.get("title") or [""])[0]
check("negative control: 10.1103/PhysRevD.84.104017 does not match SVW title", jacc(t, NEW["10.1103/PhysRevD.84.104018"][0]) < 0.3)

files = sorted(glob.glob("chap0[7-9]_*.tex") + glob.glob("chap1[0-2]_*.tex"))
BAD = re.compile(r"earlier version|previous version|withdrawn|erratum|corrected|revised|was wrong|we now|audit/|\.py\b|F-\d\d", re.I)
for f in files:
    s = open(f, encoding="utf-8").read()
    body = s
    cites = set()
    for grp in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]*)\}", body):
        cites |= {c.strip() for c in grp.split(",")}
    bib = set(re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", body))
    check("%s: every \\cite has a \\bibitem" % f[:6], cites <= bib)
    check("%s: every \\bibitem is cited" % f[:6], bib <= cites)
    hits = []
    for i, line in enumerate(s.splitlines(), 1):
        if line.lstrip().startswith("%"):
            continue
        for mm in BAD.finditer(line):
            if mm.group(0).lower() == "we now" and "We now link" in line:
                continue  # expository, not revision history (checked by hand)
            hits.append((i, mm.group(0)))
    if hits:
        print("     %s hits:" % f[:6], hits[:10])
    check("%s: no revision-history wording / audit paths" % f[:6], not hits)

# presence of content confirmed in the earlier L2 reports (spot list)
KEEP = {
    "chap07": ["2r-3", "Courant", "Dubins", "lewicka2020", "fenchel1929"],
    "chap08": ["coth", "3\\sqrt3","Estabrook", "Milne", "Israel"],
    "chap09": ["\\int|\\kappa| + \\pi", "boone1959", "lieutier2004", "Schoenflies", "\\arccos(1/3)"],
    "chap10": ["5d - 4\\operatorname{tr}Q", "saxe2014", "zhang2021", "0.70", "K-FAC"],
    "chap11": ["petz1996", "bisognano1976", "goroff1986", "Magnus", "hayden2016random"],
    "chap12": ["Mandelstam", "Airy", "erfc", "27", "Koide"],
}
for f in files:
    s = open(f, encoding="utf-8").read()
    for key in KEEP[f[:6]]:
        check("%s still contains '%s'" % (f[:6], key), key in s)

print("\nFAILURES:", FAILS if FAILS else "none")
raise SystemExit(1 if FAILS else 0)
