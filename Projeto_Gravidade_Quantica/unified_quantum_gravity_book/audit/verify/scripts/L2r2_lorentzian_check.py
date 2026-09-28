"""L2 round-2 re-check of sec:lorentzian_completion (ch. 12). Independent of the corrector.

Checks
 1. r(x) = 24 x^2 / (N^2 (1 + 2 x^2)), x = m_chi/m_phi: limits x->1/4 (4/3), x=1 (8), x->inf (12),
    and the Planck case x = M_P/m_phi with m_phi from a numerical slow roll of the Starobinsky potential
    normalised to A_s (oracle: ODE-free integral of the slow-roll N(phi), not the closed form).
 2. KL UV bound: for random positive Stieltjes G, the UV log-ratio -2 ln P / ln tau -> >= 4;
    negative control: the ghost symbol z + l^2 z^2 has UV d_s -> 2.
 3. Crossref metadata for the new Weinberg1995 DOI; negative control on a mutated DOI.
Negative controls must FAIL the corresponding test.
"""
import json
import math
import urllib.request

import mpmath as mp

ok = []


def check(name, cond, info=""):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + "  " + str(info))


# ---- 1. r formula -------------------------------------------------------
def n2r(x):
    return 24 * x * x / (1 + 2 * x * x)


check("x->1/4 gives 4/3", abs(n2r(0.25) - 4 / 3) < 1e-12, n2r(0.25))
check("x=1 gives 8", abs(n2r(1.0) - 8) < 1e-12, n2r(1.0))
check("x->inf gives 12", abs(n2r(1e9) - 12) < 1e-9, n2r(1e9))
xs = [0.25 + 1e-6 * 10 ** (k / 3) for k in range(0, 40)]
check("monotone increasing on (1/4, inf)", all(n2r(a) < n2r(b) for a, b in zip(xs, xs[1:])))
# negative control: swapped-mass formula 24/(N^2(x^2+2)) does not give 4/3 at x=1/4
nc = 24 / (0.25 ** 2 + 2)
check("NC swapped formula misses 4/3 (must differ)", abs(nc - 4 / 3) > 1, nc)

# m_phi from Starobinsky, independent numerical slow roll (reduced Planck units)
hbar_c = 1.973269804e-16  # GeV m  (CODATA 2018)
G = 6.67430e-11
hbar = 1.054571817e-34
c = 299792458.0
lP = math.sqrt(hbar * G / c ** 3)
MP_GeV = hbar_c / lP  # non-reduced Planck mass, GeV
Mred = MP_GeV / math.sqrt(8 * math.pi)
As = math.exp(3.044) * 1e-10
Nef = 60
mp.mp.dps = 30


def V(p):  # V/(3/4 m^2 Mred^2) with Mred=1
    return (1 - mp.e ** (-mp.sqrt(2 / 3) * p)) ** 2


def dV(p):
    return mp.diff(V, p)


def eps(p):
    return 0.5 * (dV(p) / V(p)) ** 2


p_end = mp.findroot(lambda p: eps(p) - 1, 0.9)
Nf = lambda p: mp.quad(lambda q: V(q) / dV(q), [p_end, p])
p_star = mp.findroot(lambda p: Nf(p) - Nef, 5.5)
# A_s = V/(24 pi^2 eps) with V = (3/4) m^2 V(p) in Mred=1 units
m2 = As * 24 * mp.pi ** 2 * eps(p_star) / (mp.mpf(3) / 4 * V(p_star))
m_phi = float(mp.sqrt(m2)) * Mred
ratio = MP_GeV / m_phi
check("m_phi ~ 3e13 GeV (order of magnitude)", 1e13 < m_phi < 1e14, "%.4g GeV" % m_phi)
check("M_P/m_phi ~ 4.5e5", 4.0e5 < ratio < 5.0e5, "%.4g" % ratio)
defect = 1 - n2r(ratio) / 12
check("1 - N^2 r/12 ~ 2.5e-12 at m_chi = M_P", 2.3e-12 < defect < 2.7e-12, "%.3g" % defect)
check("Planck case excludes 8/N^2 (N^2 r - 8 > 3.9)", n2r(ratio) - 8 > 3.9)
# NC: using reduced mass for m_chi gives a different defect -> the 2.5e-12 figure is M_P-specific
defect_red = 1 - n2r(Mred / m_phi) / 12
check("NC reduced-mass defect differs from 2.5e-12 (must differ)", not (2.3e-12 < defect_red < 2.7e-12), "%.3g" % defect_red)
# window at N=60
check("r window N=60", abs(4 / 3 / 3600 - 3.7e-4) < 5e-6 and abs(12 / 3600 - 3.3e-3) < 5e-5)

# ---- 2. KL UV bound -----------------------------------------------------
mp.mp.dps = 25
import random

random.seed(7)


def P_of(S, tau):
    # 4D heat-kernel diagonal up to constant: int_0^inf z e^{-tau S(z)} dz
    return mp.quad(lambda z: z * mp.e ** (-tau * S(z)), [0, 1, 10 / tau, mp.inf])


def logratio(S, tau):
    return -2 * mp.log(P_of(S, tau)) / mp.log(tau)


def dsloc(S, tau):
    h = mp.mpf("1e-4")
    return -2 * (mp.log(P_of(S, tau * mp.e ** h)) - mp.log(P_of(S, tau * mp.e ** (-h)))) / (2 * h)


worst = 10
for trial in range(6):
    w0 = random.uniform(0.2, 2)
    masses = [10 ** random.uniform(-1, 2) for _ in range(3)]
    ws = [random.uniform(0.1, 2) for _ in range(3)]
    G = lambda z, w0=w0, m=masses, w=ws: w0 / z + sum(wi / (z + mi) for wi, mi in zip(w, m))
    S = lambda z, G=G: 1 / G(z)
    d = dsloc(S, mp.mpf("1e-7"))
    worst = min(worst, float(d))
check("positive Stieltjes: UV d_s >= 4 (tau=1e-7)", worst >= 4 - 1e-3, "min %.5f" % worst)
Sg = lambda z: z + z * z  # book symbol, l=1: rho has a -1 weight
dg = float(dsloc(Sg, mp.mpf("1e-7")))
check("NC ghost symbol: UV d_s < 4 (must be ~2)", dg < 2.1, "%.5f" % dg)

# ---- 3. Crossref ---------------------------------------------------------
def crossref(doi):
    try:
        with urllib.request.urlopen("https://api.crossref.org/works/" + doi, timeout=30) as r:
            return json.load(r)["message"]
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}


m = crossref("10.1017/CBO9781139644167")
title = " ".join(m.get("title", []))
isbn = m.get("ISBN", [])
auth = [a.get("family") for a in m.get("author", [])]
print("  Crossref:", title, "|", m.get("publisher"), "|", isbn, "|", auth, "|", m.get("published", {}))
check("Weinberg DOI resolves to QFT, CUP", "Quantum Theory of Fields" in title and "Cambridge" in str(m.get("publisher")))
check("Weinberg DOI ISBN = Vol I (9780521550017 or e-ISBN)", any("9780521550017" in s.replace("-", "") or "9781139644167" in s.replace("-", "") for s in isbn), isbn)
bad = crossref("10.1017/CBO97811396441670")
check("NC mutated DOI fails", "error" in bad, bad.get("error", "")[:40])

print("\n%d/%d PASS" % (sum(ok), len(ok)))
