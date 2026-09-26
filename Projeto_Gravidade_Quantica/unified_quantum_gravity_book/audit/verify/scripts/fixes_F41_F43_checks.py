"""Checks written by the corrector for findings F-41..F-43 (chapters 8, 12, 13).

Each block compares a statement introduced or changed in the text with an
independent computation, and contains a negative control that must fail.
Run from the book directory:  python audit/verify/scripts/fixes_F41_F43_checks.py
"""
import numpy as np
from scipy import integrate, optimize

FAIL = []


def check(name, ok, neg_ok=True, info=""):
    tag = "OK  " if (ok and neg_ok) else "FAIL"
    if not (ok and neg_ok):
        FAIL.append(name)
    print(f"[{tag}] {name} {info}")


# ---------------------------------------------------------------------------
# 1. Chapter 8, U-turn theorem in a tube about a geodesic of H^2 / S^2 / R^2.
#    Fermi coordinates g = dy^2 + G(y)^2 dx^2; angle theta against e_x = G^-1 d_x.
#    Claimed identity: d/ds [G(y) cos theta] = -kappa G(y) sin theta  (Killing field d_x)
#    Claimed bound: any U-turn with |kappa| <= k has k >= min_{a<b in [-w/2,w/2]} F(a,b),
#    F(a,b) = (G(a)+G(b)) / int_a^b G, and min F = F(-w/2, w/2) = coth(w/2) / cot(w/2) / 2/w.
# ---------------------------------------------------------------------------
GEOM = {
    "H2": (np.cosh, np.sinh, lambda y: np.tanh(y), lambda w: 1 / np.tanh(w / 2)),
    "S2": (np.cos, np.sin, lambda y: -np.tan(y), lambda w: 1 / np.tan(w / 2)),
    "R2": (lambda y: np.ones_like(y), lambda y: y, lambda y: 0 * y, lambda w: 2 / w),
}


def rhs(s, u, kap, h):
    x, y, th = u[:3]
    # geodesic curvature in the Fermi frame (Liouville): theta' = kappa + (G'/G)(y) cos theta
    return [np.cos(th), np.sin(th), kap(s) + h(y) * np.cos(th)]


def uturn_identity(geom):
    G, _, h, _ = GEOM[geom]
    rng = np.random.default_rng(7)
    knots = np.sort(rng.uniform(0, 3, 12))
    vals = rng.uniform(-1.5, 1.5, 13)
    kap = lambda s: vals[np.searchsorted(knots, s)]
    # augmented state: I' = -kappa G(y) sin theta, integrated alongside the curve
    aug = lambda s, u: rhs(s, u[:3], kap, h) + [-kap(s) * G(u[1]) * np.sin(u[2])]
    sol = integrate.solve_ivp(aug, (0, 3), [0, -0.2, 0.3, 0.0], max_step=1e-3, rtol=1e-11, atol=1e-13)
    x, y, th, I = sol.y
    u = G(y) * np.cos(th)
    lhs = u[-1] - u[0]
    rhs_int = I[-1]
    wrong = -I[-1]                                        # negative control: opposite sign
    return abs(lhs - rhs_int), abs(lhs - wrong)


for geom in ("H2", "S2", "R2"):
    err, err_neg = uturn_identity(geom)
    check(f"1a {geom}: d/ds(G cos th) = -kappa G sin th", err < 1e-5, err_neg > 1e-2,
          f"err={err:.1e}, sign-flipped control err={err_neg:.2e}")

for geom, ws in (("H2", (0.5, 1.5, 3.0)), ("S2", (0.5, 1.2, 1.6, 2.4, 3.0)), ("R2", (1.0,))):
    G, Gint, _, k0 = GEOM[geom]
    for w in ws:
        a = np.linspace(-w / 2, w / 2, 401)
        A, B = np.meshgrid(a, a, indexing="ij")
        mask = B > A + 1e-9
        F = (G(A[mask]) + G(B[mask])) / (Gint(B[mask]) - Gint(A[mask]))
        # closed forms: coth((b-a)/2), cot((b-a)/2), 2/(b-a)
        closed = {"H2": 1 / np.tanh((B[mask] - A[mask]) / 2), "S2": 1 / np.tan((B[mask] - A[mask]) / 2),
                  "R2": 2 / (B[mask] - A[mask])}[geom]
        ok = abs(F.min() - k0(w)) < 1e-9 * max(1, k0(w)) and np.allclose(F, closed, rtol=1e-9)
        neg = F.min() < 1.03 * k0(w)       # control: a 3% stronger bound is violated
        check(f"1b {geom} w={w}: min F = k0", ok, neg, f"min F={F.min():.6f}, k0={k0(w):.6f}")


def uturn_search(geom, w, k, trials=400, seed=3):
    """Random bang-bang controls |kappa|<=k starting at y=-w/2..w/2 with theta=0; count U-turns inside the tube."""
    G, _, h, _ = GEOM[geom]
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(trials):
        y0 = rng.uniform(-w / 2, -w / 2 + 0.05 * w)
        n = rng.integers(1, 5)
        knots = np.sort(rng.uniform(0, 4 * w + 4, n))
        signs = rng.choice([1.0, 1.0, 1.0, -1.0], n + 1) * rng.uniform(0.9, 1.0, n + 1)
        kap = lambda s: k * signs[np.searchsorted(knots, s)]
        ev = lambda s, u, *a: u[2] - np.pi
        ev.terminal = True
        out = lambda s, u, *a: abs(u[1]) - w / 2 - 1e-12
        out.terminal = True
        sol = integrate.solve_ivp(rhs, (0, 6 * w + 8), [0, y0, 0], args=(kap, h), events=(ev, out),
                                  max_step=w / 200, rtol=1e-9, atol=1e-11)
        if sol.t_events[0].size and not sol.t_events[1].size:
            hits += 1
    return hits


for geom, w in (("H2", 1.0), ("S2", 2.4), ("S2", 3.0)):
    k0 = GEOM[geom][3](w)
    below = uturn_search(geom, w, 0.98 * k0)
    above = uturn_search(geom, w, 1.05 * k0)
    check(f"1c {geom} w={w}: no U-turn with 0.98 k0; some with 1.05 k0 (positive control)", below == 0, above > 0,
          f"below={below}, above={above}")

# ---------------------------------------------------------------------------
# 2. Chapter 8, winding classes for timelike equatorial curves in Schwarzschild.
#    |dphi/dt| < sqrt(f)/r <= 1/(3 sqrt3 M); |W| <= Delta t/(6 sqrt3 pi M) + 1/2.
# ---------------------------------------------------------------------------
M = 1.0
r = np.linspace(2.0001, 200, 400001)
peak = np.max(np.sqrt(1 - 2 * M / r) / r)
check("2a max sqrt(f)/r = 1/(3 sqrt3 M) at r=3M", abs(peak - 1 / (3 * np.sqrt(3) * M)) < 1e-9,
      abs(peak - 1 / (2 * np.sqrt(2) * M)) > 1e-3, f"peak={peak:.8f}")
dt = 100.0
Wmax = int(np.floor(dt / (6 * np.sqrt(3) * np.pi * M) + 0.5))
check("2b Delta t = 100 M gives |W| <= 3", Wmax == 3, Wmax != 4, f"Wmax={Wmax}")

# ---------------------------------------------------------------------------
# 3. Chapter 8, FLRW: ||K|| = |H|/c <= 1/l_P bounds only the energy density.
#    rho c^2 <= 3 c^4 / (8 pi G l_P^2) = (3/8pi) c^7/(hbar G^2).
# ---------------------------------------------------------------------------
c, hbar, Gn = 2.99792458e8, 1.054571817e-34, 6.67430e-11
lP = np.sqrt(hbar * Gn / c**3)
Hmax = c / lP
eps_max = 3 * Hmax**2 / (8 * np.pi * Gn) * c**2       # J/m^3
closed = 3 / (8 * np.pi) * c**7 / (hbar * Gn**2)
check("3a rho c^2 <= (3/8pi) c^7/(hbar G^2) ~ 5.5e112 J/m^3", abs(eps_max / closed - 1) < 1e-12,
      abs(closed - 5.5e112) / 5.5e112 < 0.02, f"{eps_max:.3e}")
# pressure depends on dH/dt: two FLRW histories with the same |H| <= 1/l_P and different p
Hval = 0.5 * Hmax
p = lambda Hdot: -(2 * Hdot + 3 * Hval**2) * c**2 / (8 * np.pi * Gn)
check("3b same H, different Hdot give different pressure (no bound on p from ||K||)",
      abs(p(0) - p(1e3 * Hmax**2)) > 1e3 * abs(p(0)), True)

# ---------------------------------------------------------------------------
# 4. Chapter 12, thin shell with constant K: turning point exists iff 27 kappa^2 M^2 < 1.
# ---------------------------------------------------------------------------
ok_all = True
for kap_, M_ in ((0.1, 1.0), (0.19, 1.0), (0.2, 1.0), (0.3, 1.0), (0.05, 3.0)):
    roots = np.roots([kap_**2, 0, -1, 2 * M_])
    has_pos = np.any((abs(roots.imag) < 1e-12) & (roots.real > 0))
    ok_all &= has_pos == (27 * kap_**2 * M_**2 < 1)
check("4a positive root of kappa^2 r^3 - r + 2M iff 27 kappa^2 M^2 < 1", ok_all,
      not all(((27 * k_**2 * m_**2 < 1) == (54 * k_**2 * m_**2 < 1)) for k_, m_ in ((0.1, 1.0), (0.15, 1.0))))

# ---------------------------------------------------------------------------
# 5. Chapter 12, Higgs: Delta lambda for m_H = 125.20 GeV (PDG 2024) with m_H = v sqrt(2 lambda).
# ---------------------------------------------------------------------------
v = 246.22
lam0 = (v / 2) ** 2 / (2 * v**2)
dlam = 125.20**2 / (2 * v**2) - lam0
check("5a Delta lambda ~ 0.0043 for 125.20 GeV", abs(dlam - 0.0043) < 5e-5,
      abs(125.25**2 / (2 * v**2) - lam0 - 0.0043) > 5e-5, f"dlam={dlam:.5f}")

# ---------------------------------------------------------------------------
# 6. Chapter 12, product Dirac operator: D_M x 1 + gamma5 x D_F has spectrum +-sqrt(k^2+m^2).
# ---------------------------------------------------------------------------
sx = np.array([[0, 1], [1, 0]]); sz = np.array([[1, 0], [0, -1]])
kk, mm = 0.5, 1.0
DM = kk * sx; g5 = sz; DF = np.array([[mm]])
good = np.kron(DM, np.eye(1)) + np.kron(g5, DF)
bad = np.kron(DM, np.eye(1)) + np.kron(np.eye(2), DF)
ev_good = np.sort(np.linalg.eigvalsh(good)); ev_bad = np.sort(np.linalg.eigvalsh(bad))
check("6a gamma5 grading gives +-sqrt(k^2+m^2)", np.allclose(ev_good, [-np.hypot(kk, mm), np.hypot(kk, mm)]),
      not np.allclose(ev_bad, [-np.hypot(kk, mm), np.hypot(kk, mm)]), f"{ev_good} vs control {ev_bad}")

print()
print("FAILURES:", FAIL if FAIL else "none")
raise SystemExit(1 if FAIL else 0)
