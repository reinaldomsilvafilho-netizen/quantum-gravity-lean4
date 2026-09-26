"""L2 round 2 (independent): ch9 teardrop remark (l. 241) and Culler-Shalen citation.

(A) Teardrop insertion. A straight piece along the x-axis; a closed disk of radius 1/k tangent
    to it at P = (x0, 0), centre (x0, 1/k). Insert the boundary circle at P, traversed so that
    the tangent at P is +x (counterclockwise). Checks on a sampled curve:
      - length increases by exactly 2 pi/k, so admissibility needs slack >= 2 pi/k;
      - tangent continuous at both junctions (C^1), curvature in {0, k} (C^{1,1}, sup = k);
      - the inserted loop has winding 0 about any obstacle point outside the disk (null-homotopic
        in the free space when the closed disk lies in the free space).
    Mutations that must FAIL: slack 2 pi/k - 0.01 keeps length <= V; radius 0.9/k keeps sup <= k;
    clockwise traversal keeps C^1; obstacle point inside the disk gives winding 0.
(B) Crossref: DOI 10.2307/2006973 must match Culler-Shalen, Ann. Math. 117 (1983) no. 1, 109-146.
    Negative control: neighbouring DOI 10.2307/2006972 must not match.
Run from the book folder.
"""
import json
import urllib.request
import numpy as np

FAIL = []


def check(name, ok):
    print(("OK   " if ok else "FAIL ") + name)
    if not ok:
        FAIL.append(name)


def build(k, x0=1.0, seg=3.0, radius=None, ccw=True, n=20001):
    rad = 1.0 / k if radius is None else radius
    a = np.linspace(0, x0, n)
    p1 = np.stack([a, 0 * a], 1)
    t = np.linspace(0, 2 * np.pi, n)
    sgn = 1.0 if ccw else -1.0
    # circle through P=(x0,0), centre (x0, sgn*rad); start angle -pi/2 (resp. +pi/2)
    cx, cy = x0, sgn * rad
    circ = np.stack([cx + rad * np.cos(-sgn * np.pi / 2 + sgn * t) * 1.0, cy + rad * np.sin(-sgn * np.pi / 2 + sgn * t)], 1)
    if not ccw:  # clockwise traversal of the same (upper) disk: mirror parametrisation direction
        cy = rad
        circ = np.stack([cx + rad * np.cos(-np.pi / 2 - t), cy + rad * np.sin(-np.pi / 2 - t)], 1)
    b = np.linspace(x0, seg, n)
    p2 = np.stack([b, 0 * b], 1)
    return p1, circ, p2, (cx, cy, rad)


def length(*pieces):
    return sum(np.sum(np.linalg.norm(np.diff(p, axis=0), axis=1)) for p in pieces)


def unit_tangent(p, end):
    d = p[1] - p[0] if end == "start" else p[-1] - p[-2]
    return d / np.linalg.norm(d)


def curvature(p):
    d1 = np.gradient(p, axis=0)
    d2 = np.gradient(d1, axis=0)
    num = np.abs(d1[:, 0] * d2[:, 1] - d1[:, 1] * d2[:, 0])
    return num[5:-5] / np.linalg.norm(d1[5:-5], axis=1) ** 3


def winding(loop, q):
    ang = np.unwrap(np.arctan2(loop[:, 1] - q[1], loop[:, 0] - q[0]))
    return (ang[-1] - ang[0]) / (2 * np.pi)


k = 2.0
p1, circ, p2, (cx, cy, rad) = build(k)
L0 = length(p1, p2)
L1 = length(p1, circ, p2)
print("  length before %.6f after %.6f increase %.6f vs 2pi/k %.6f" % (L0, L1, L1 - L0, 2 * np.pi / k))
check("insertion adds exactly 2 pi/k", abs(L1 - L0 - 2 * np.pi / k) < 1e-6)
V = L0 + 2 * np.pi / k
check("slack = 2 pi/k: new length <= V (admissible)", L1 <= V + 1e-6)
check("MUTATION slack 2pi/k - 0.01: still admissible [must FAIL]", L1 <= L0 + 2 * np.pi / k - 0.01 + 1e-6)
tj1 = np.dot(unit_tangent(p1, "end"), unit_tangent(circ, "start"))
tj2 = np.dot(unit_tangent(circ, "end"), unit_tangent(p2, "start"))
check("C^1 at both junctions (tangent dot = 1)", tj1 > 1 - 1e-6 and tj2 > 1 - 1e-6)
kc = curvature(circ)
check("curvature on circle = k, so sup kappa unchanged (= kappa*)", np.allclose(kc, k, rtol=1e-4))
q_out = np.array([cx + 3 * rad, cy])  # obstacle point outside the disk
check("inserted loop has winding 0 about an obstacle outside the disk", abs(winding(circ, q_out)) < 1e-9)
# mutations
_, c09, _, _ = build(k, radius=0.9 / k)
check("MUTATION radius 0.9/k: sup kappa <= k [must FAIL]", curvature(c09).max() <= k * (1 + 1e-4))
p1c, ccw_c, p2c, _ = build(k, ccw=False)
check("MUTATION clockwise traversal: C^1 at junction [must FAIL]", np.dot(unit_tangent(p1c, "end"), unit_tangent(ccw_c, "start")) > 1 - 1e-6)
check("MUTATION obstacle inside the disk: winding 0 [must FAIL]", abs(winding(circ, np.array([cx, cy]))) < 1e-9)

# ---- (B) Crossref
def crossref(doi):
    req = urllib.request.Request("https://api.crossref.org/works/" + doi, headers={"User-Agent": "book-audit/1.0 (mailto:reinaldo.msilvafilho@gmail.com)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["message"]


def matches(m):
    title = " ".join(m.get("title", [])).lower()
    fam = [a.get("family", "").lower() for a in m.get("author", [])]
    year = (m.get("issued", {}).get("date-parts", [[None]])[0][0])
    return ("varieties of group representations" in title and "splittings" in title
            and "culler" in fam and "shalen" in fam and m.get("volume") == "117"
            and m.get("page") in ("109", "109-146") and year == 1983)


try:
    m = crossref("10.2307/2006973")
    print("  Crossref:", m.get("title"), [a.get("family") for a in m.get("author", [])], m.get("container-title"), m.get("volume"), m.get("issue"), m.get("page"), m.get("issued"))
    check("DOI 10.2307/2006973 = Culler-Shalen, Ann. Math. 117 (1983) 109-146", matches(m))
    try:
        m2 = crossref("10.2307/2006972")
        print("  neighbour:", m2.get("title"), m2.get("page"))
        check("CONTROL neighbour DOI 10.2307/2006972 matches [must FAIL]", matches(m2))
    except Exception as e:  # a non-resolving neighbour also counts as a non-match
        print("  neighbour lookup error:", e)
        check("CONTROL neighbour DOI 10.2307/2006972 matches [must FAIL]", False)
except Exception as e:
    print("  Crossref unreachable:", e)
    check("Crossref reachable", False)

# ---- (C) chapter text: citation now without a proposition number, remark has the 2pi/kappa* slack
tex = open("chap09_global_homotopy_covering_spaces_jordan_loops.tex", encoding="utf-8").read()
check("no 'Proposition 1.5.2' left in ch9", "1.5.2" not in tex)
check("culler1983 cited plainly", "are conjugate \\cite{culler1983}" in tex)
check("remark states slack at least 2pi/kappa*", "at least $2\\pi/\\kappa^*$ below the length bound" in tex)
check("MUTATION text still says only 'there is slack' [must FAIL]", "there is slack in the length bound" in tex)

expected = {f for f in [
    "MUTATION slack 2pi/k - 0.01: still admissible [must FAIL]",
    "MUTATION radius 0.9/k: sup kappa <= k [must FAIL]",
    "MUTATION clockwise traversal: C^1 at junction [must FAIL]",
    "MUTATION obstacle inside the disk: winding 0 [must FAIL]",
    "CONTROL neighbour DOI 10.2307/2006972 matches [must FAIL]",
    "MUTATION text still says only 'there is slack' [must FAIL]",
]}
unexpected = [f for f in FAIL if f not in expected]
missing = [f for f in expected if f not in FAIL]
print("\nunexpected failures:", unexpected)
print("controls that did not fail:", missing)
raise SystemExit(1 if unexpected or missing else 0)
