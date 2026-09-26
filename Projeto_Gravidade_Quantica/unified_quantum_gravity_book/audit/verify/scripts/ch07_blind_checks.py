"""Blind re-audit checks for chap07 (camada 1). Independent oracles + negative controls.

Run: python audit/verify/scripts/ch07_blind_checks.py
Each check prints PASS/FAIL; negative controls (mutated formulas) must FAIL, reported as 'NEG-OK'.
"""
import numpy as np
import sympy as sp

rng = np.random.default_rng(0)
results = []


def report(name, ok):
    results.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")


def neg(name, ok_mutated):
    # mutated formula must NOT agree with the oracle
    results.append((name, not ok_mutated))
    print(f"[{'NEG-OK' if not ok_mutated else 'NEG-FAIL'}] {name}")


# ---------------------------------------------------------------- helpers
def curvature_numeric(gamma, s, h=1e-4):
    """curvature of a (not nec. unit speed) curve via finite differences."""
    d1 = (gamma(s + h) - gamma(s - h)) / (2 * h)
    d2 = (gamma(s + h) - 2 * gamma(s) + gamma(s - h)) / h**2
    v2 = d1 @ d1
    acc_perp = d2 - (d2 @ d1) / v2 * d1
    return np.linalg.norm(acc_perp) / v2


# --------------------------------------------------- 1. multi-plane helix
for m in (2, 3, 5):
    R0 = 1.3
    om = 1 / (np.sqrt(m) * R0)
    phi = rng.uniform(0, 2 * np.pi, m)

    def g(s, phi=phi, m=m, R0=R0, om=om):
        out = np.zeros(2 * m)
        out[0::2] = R0 * np.cos(om * s + phi)
        out[1::2] = R0 * np.sin(om * s + phi)
        return out

    ks = [curvature_numeric(g, s) for s in np.linspace(0, 10, 7)]
    report(f"helix m={m}: curvature = 1/(sqrt m R0)", np.allclose(ks, 1 / (np.sqrt(m) * R0), rtol=1e-5))
    neg(f"helix m={m}: mutated curvature 1/R0", np.allclose(ks, 1 / R0, rtol=1e-5))
    # planarity for RANDOM phases: rank of centred samples
    P = np.array([g(s) for s in np.linspace(0, 50, 200)])
    sv = np.linalg.svd(P - P.mean(0), compute_uv=False)
    rank = int((sv > 1e-9 * sv[0]).sum())
    report(f"helix m={m}, random phases: curve lies in a 2-plane (rank={rank})", rank == 2)
    radius = np.linalg.norm(P, axis=1)
    report(f"helix m={m}: |gamma| = sqrt(m) R0 (circle of radius sqrt m R0)", np.allclose(radius, np.sqrt(m) * R0))

# --------------------------------------------------- 2. Clifford / product torus
def product_torus_opnorm(m, R, n_dir=4000):
    r = R / np.sqrt(m)
    # II(e_j,e_j) = -(1/r) nu_j, mutually orthogonal, II(e_i,e_j)=0 (i!=j)
    best = 0
    for _ in range(n_dir):
        v = rng.normal(size=m)
        v /= np.linalg.norm(v)
        best = max(best, np.sqrt(np.sum(v**4)) / r)
    for j in range(m):
        e = np.zeros(m); e[j] = 1
        best = max(best, np.sqrt(np.sum(e**4)) / r)
    return best

for m in (2, 3, 4):
    R = 2.0
    report(f"product torus m={m}: ||II||op = sqrt(m)/R", np.isclose(product_torus_opnorm(m, R), np.sqrt(m) / R))
    neg(f"product torus m={m}: mutated 1/(sqrt m R)", np.isclose(product_torus_opnorm(m, R), 1 / (np.sqrt(m) * R)))

# independent check via embedding second derivatives (Clifford, m=2)
R = 1.7
u, v = 0.4, 1.1
X = lambda u, v: R / np.sqrt(2) * np.array([np.cos(u), np.sin(u), np.cos(v), np.sin(v)])
h = 1e-4
Xuu = (X(u + h, v) - 2 * X(u, v) + X(u - h, v)) / h**2
Xvv = (X(u, v + h) - 2 * X(u, v) + X(u, v - h)) / h**2
Xuv = (X(u + h, v + h) - X(u + h, v - h) - X(u - h, v + h) + X(u - h, v - h)) / (4 * h**2)
g = R**2 / 2
best = 0
for t in np.linspace(0, np.pi, 2001):
    a, b = np.cos(t) / np.sqrt(g), np.sin(t) / np.sqrt(g)
    best = max(best, np.linalg.norm(a * a * Xuu + 2 * a * b * Xuv + b * b * Xvv))  # all 2nd derivs are normal here
report("Clifford torus via finite differences: sqrt2/R", np.isclose(best, np.sqrt(2) / R, rtol=1e-4))

# --------------------------------------------------- 3. bulged surface of revolution
def bulge_max_curv(a, R=1.0, H=10.0, N=20001):
    z = np.linspace(0, H, N)
    r = R + a * np.sin(np.pi * z / H)
    rp = a * np.pi / H * np.cos(np.pi * z / H)
    rpp = -a * (np.pi / H) ** 2 * np.sin(np.pi * z / H)
    k_mer = np.abs(rpp) / (1 + rp**2) ** 1.5
    k_par = 1 / (r * np.sqrt(1 + rp**2))
    return max(k_mer.max(), k_par.max())

for a, claimed in ((1, 0.954), (3, 0.728)):
    val = bulge_max_curv(a)
    report(f"bulge a={a}: max principal curvature {val:.4f} ~ {claimed}", abs(val - claimed) < 5e-4)
# negative control: forget the 1/sqrt(1+r'^2) factor -> would give 1.0 (no improvement)
neg("bulge a=3 with parallel curvature 1/r (mutated)", abs(1 / 1.0 - 0.728) < 5e-4)

# --------------------------------------------------- 4. complex curve w = z^2 : ||II||op vs ||II||F
def graph_II(z0):
    # surface (x,y,Re z^2, Im z^2) in R^4 at z0 = x+iy
    x, y = sp.symbols('x y', real=True)
    F = sp.Matrix([x, y, x**2 - y**2, 2 * x * y])
    Fx, Fy = F.diff(x), F.diff(y)
    subs = {x: z0.real, y: z0.imag}
    Fx_, Fy_ = np.array(Fx.subs(subs), float).ravel(), np.array(Fy.subs(subs), float).ravel()
    sec = {k: np.array(F.diff(*k).subs(subs), float).ravel() for k in [(x, x), (x, y), (y, y)]}
    T = np.stack([Fx_, Fy_], 1)
    Q, _ = np.linalg.qr(T)
    Pn = np.eye(4) - Q @ Q.T
    G = T.T @ T
    Ginv_half = np.linalg.inv(np.linalg.cholesky(G)).T  # columns: coefficients of an orthonormal basis
    e = [Ginv_half[:, 0], Ginv_half[:, 1]]
    def II(a, b):
        return Pn @ (a[0] * b[0] * sec[(x, x)] + (a[0] * b[1] + a[1] * b[0]) * sec[(x, y)] + a[1] * b[1] * sec[(y, y)])
    F2 = sum(np.linalg.norm(II(e[i], e[j])) ** 2 for i in range(2) for j in range(2))
    op = max(np.linalg.norm(II(np.cos(t) * e[0] + np.sin(t) * e[1], np.cos(t) * e[0] + np.sin(t) * e[1]))
             for t in np.linspace(0, np.pi, 4001))
    K = II(e[0], e[0]) @ II(e[1], e[1]) - np.linalg.norm(II(e[0], e[1])) ** 2
    return op, np.sqrt(F2), K

for z0 in (0.3 + 0.2j, 1.0 - 0.7j):
    op, F, K = graph_II(z0)
    report(f"w=z^2 at {z0}: ||II||op = ||II||F/2", np.isclose(op, F / 2, rtol=1e-5))
    neg(f"w=z^2 at {z0}: 'isotropy' ||II||op = ||II||F/sqrt2", np.isclose(op, F / np.sqrt(2), rtol=1e-5))
    report(f"w=z^2 at {z0}: K = -2 ||II||op^2 (pointwise sharpness of Gauss-Bonnet K >= -2 kappa^2)",
           np.isclose(K, -2 * op**2, rtol=1e-5))

# --------------------------------------------------- 5. Gauss equation bounds, random II in codim c
worst_lo, worst_hi = np.inf, -np.inf
for _ in range(20000):
    c = rng.integers(1, 5)
    A, B, C = rng.normal(size=(3, c))  # II11, II12, II22
    ts = np.linspace(0, np.pi, 721)
    op = max(np.linalg.norm(np.cos(t)**2 * A + 2 * np.sin(t) * np.cos(t) * B + np.sin(t)**2 * C) for t in ts[::8])
    K = A @ C - B @ B
    worst_lo = min(worst_lo, K / op**2)
    worst_hi = max(worst_hi, K / op**2)
report(f"Gauss eq.: -2 <= K/||II||op^2 <= 1 on random samples (min {worst_lo:.3f}, max {worst_hi:.3f})",
       worst_lo >= -2 - 0.05 and worst_hi <= 1 + 0.05)

# --------------------------------------------------- 6. sagitta arc
L_, d_ = sp.symbols('L d', positive=True)
Rarc = (L_**2 / 4 + d_**2) / (2 * d_)
report("sagitta arc curvature 8d/(L^2+4d^2)", sp.simplify(1 / Rarc - 8 * d_ / (L_**2 + 4 * d_**2)) == 0)
report("semicircle d=L/2 gives 2/L", sp.simplify((1 / Rarc).subs(d_, L_ / 2) - 2 / L_) == 0)

# --------------------------------------------------- 7. helix
a_, b_, s_ = sp.symbols('a b s', positive=True)
c_ = sp.sqrt(a_**2 + b_**2)
gam = sp.Matrix([a_ * sp.cos(s_ / c_), a_ * sp.sin(s_ / c_), b_ * s_ / c_])
k2 = sp.simplify((gam.diff(s_, 2).T * gam.diff(s_, 2))[0])
report("helix curvature a/(a^2+b^2)", sp.simplify(sp.sqrt(k2) - a_ / (a_**2 + b_**2)) == 0)

# --------------------------------------------------- 8. U-turn bound: numeric search (negative control)
def uturn_height(kprof, L=10, N=20000):
    s = np.linspace(0, L, N)
    th = np.concatenate([[0], np.cumsum((kprof(s[1:]) + kprof(s[:-1])) / 2 * np.diff(s))])
    y = np.concatenate([[0], np.cumsum((np.sin(th[1:]) + np.sin(th[:-1])) / 2 * np.diff(s))])
    return th, y

k = 2.0  # |kappa| <= 2 => need w >= 1
worst = np.inf
for _ in range(300):
    # random bang-bang-ish profile with |kappa|<=k that achieves a U-turn
    knots = rng.uniform(-0.3, 1, 12) * k
    prof = lambda s, knots=knots: np.interp(s, np.linspace(0, 10, 12), knots)
    th, y = uturn_height(prof)
    idx = np.where(np.abs(th) >= np.pi)[0]
    if len(idx) == 0:
        continue
    i = idx[0]
    worst = min(worst, y[:i + 1].max() - y[:i + 1].min())
report(f"U-turn: random |kappa|<=2 curves need height >= 2/k = 1 (min seen {worst:.4f})", worst >= 1 - 1e-3)

# --------------------------------------------------- 9. transition polynomial degree
# C^r curve needs curvature in C^{r-2}; a monotone Hermite ramp 0 -> kappa with
# derivatives up to order r-2 vanishing at both ends needs degree 2(r-2)+1 = 2r-3.
t = sp.symbols('t')
for r in (2, 3, 4, 5):
    q = r - 2  # match derivatives 0..q ... at t=0 value 0, t=1 value 1
    deg_claimed = r - 2
    coeffs = sp.symbols(f'c0:{deg_claimed + 1}')
    p = sum(cc * t**i for i, cc in enumerate(coeffs))
    eqs = [p.subs(t, 0), p.subs(t, 1) - 1] + [p.diff(t, j).subs(t, 0) for j in range(1, q + 1)] + \
          [p.diff(t, j).subs(t, 1) for j in range(1, q + 1)]
    sol = sp.solve(eqs, coeffs, dict=True)
    # oracle: minimal degree 2q+1
    coeffs2 = sp.symbols(f'd0:{2 * q + 2}')
    p2 = sum(cc * t**i for i, cc in enumerate(coeffs2))
    eqs2 = [p2.subs(t, 0), p2.subs(t, 1) - 1] + [p2.diff(t, j).subs(t, 0) for j in range(1, q + 1)] + \
           [p2.diff(t, j).subs(t, 1) for j in range(1, q + 1)]
    sol2 = sp.solve(eqs2, coeffs2, dict=True)
    print(f"   r={r}: degree r-2={deg_claimed} solvable? {bool(sol)}; degree 2r-3={2*q+1} solvable? {bool(sol2)}")
    report(f"transition r={r}: degree r-2 profile impossible, degree 2r-3 possible", (not sol) and bool(sol2))

# --------------------------------------------------- 10. contact principle sign (disk vs exterior)
# Omega = disk radius rho (h = +1/rho): a circle of radius r<rho internally tangent has kappa=1/r >= 1/rho.
# Omega = exterior of disk (h = -1/rho): the tangent line (kappa=0) touches.
rho = 0.5
# internal tangent circle radius r must satisfy r <= rho
for r in (0.1, 0.3, 0.5):
    th = np.linspace(0, 2 * np.pi, 2000)
    pts = np.stack([(rho - r) + r * np.cos(th), r * np.sin(th)], 1)
    inside = np.all(np.linalg.norm(pts, axis=1) <= rho + 1e-12)
    report(f"contact: circle r={r} tangent inside disk rho={rho} stays in Omega and 1/r >= 1/rho", inside and 1 / r >= 1 / rho)
r = 0.8
pts = np.stack([(rho - r) + r * np.cos(th), r * np.sin(th)], 1)
neg("contact: circle with 1/r < 1/rho tangent inside disk stays in Omega (must fail)",
    bool(np.all(np.linalg.norm(pts, axis=1) <= rho + 1e-12)))
x = np.linspace(-5, 5, 1001)
line = np.stack([x, np.full_like(x, rho)], 1)
report("contact: tangent line to obstacle disk stays in exterior Omega (kappa=0 contact)",
       np.all(np.linalg.norm(line, axis=1) >= rho - 1e-12))

print("\nSUMMARY:", sum(ok for _, ok in results), "/", len(results), "ok")
