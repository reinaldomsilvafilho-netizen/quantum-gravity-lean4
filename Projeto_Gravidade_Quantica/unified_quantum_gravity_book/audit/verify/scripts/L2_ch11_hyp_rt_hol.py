"""Camada 2, F-40 (ch. 11 part). Independent checks of the corrector's new content.

[1] Conj. 4.1: with z = z0 e^{-u}, L^2(dz^2+dx^2)/z^2 = L^2 du^2 + (L^2/z0^2) e^{2u} dx^2 (sympy).
    Scalar curvature of c1 du^2 + c2 e^{2u} (dx^2+dy^2) (d=3) is -6/c1 for EVERY c2>0:
    c2 only fixes the normalization of x, it carries no separate curvature radius.
    Mutation: c2 = L^2 fails the pull-back identity unless z0 = 1.
[2] Two-interval remark in H^2: exact cut-off geodesic lengths vs 2 log(l/eps); the connected
    pair is shorter iff delta(2+delta) < 1, i.e. delta < sqrt2-1. Mutation delta(1+delta)<1.
[3] Prop. 5.2(1): midpoint product of SU(2) exponentials converges with order 2 (O(k^-2)),
    exact holonomy by RK4 on U' = U A. Mutations: left-endpoint rule (order 1) and reversed
    product order (no convergence).
[4] Remark 2.3: BKM >= SLD, equality iff [rho,X]=0; ratio range for random qutrits.
    Mutation: SLD >= BKM fails.
[5] Remark 6.2: Ollivier curvature >= -(J(x)+J(y))/d(x,y) on random weighted metric graphs
    (W1 by LP). Mutation: -(J(x)+J(y))/(2d) is violated.
"""
import numpy as np
import sympy as sp
from scipy.linalg import expm, logm
from scipy.optimize import linprog
from scipy.sparse.csgraph import shortest_path

rng = np.random.default_rng(11)
res = []


def rep(name, ok, extra=""):
    res.append(ok)
    print(("[PASS] " if ok else "[FAIL] ") + name, extra)


# [1]
u, x, y, L, z0, c1, c2 = sp.symbols("u x y L z0 c1 c2", positive=True)
z = z0 * sp.exp(-u)
dz_du = sp.diff(z, u)
g_uu = sp.simplify(L ** 2 * dz_du ** 2 / z ** 2)
g_xx = sp.simplify(L ** 2 / z ** 2)
rep("[1] pull-back: g_uu = L^2, g_xx = (L^2/z0^2) e^{2u}",
    sp.simplify(g_uu - L ** 2) == 0 and sp.simplify(g_xx - L ** 2 / z0 ** 2 * sp.exp(2 * u)) == 0)
rep("[1] NEG mutation c2 = L^2 fails unless z0 = 1",
    sp.simplify(g_xx - L ** 2 * sp.exp(2 * u)) != 0 and sp.simplify((g_xx - L ** 2 * sp.exp(2 * u)).subs(z0, 1)) == 0)

coords = [u, x, y]
G = sp.diag(c1, c2 * sp.exp(2 * u), c2 * sp.exp(2 * u))
Gi = G.inv()
n = 3
Gam = [[[sum(Gi[a, e] * (sp.diff(G[e, b], coords[c]) + sp.diff(G[e, c], coords[b]) - sp.diff(G[b, c], coords[e]))
             for e in range(n)) / 2 for c in range(n)] for b in range(n)] for a in range(n)]


def Ric(b, c):
    return sp.simplify(sum(sp.diff(Gam[a][b][c], coords[a]) - sp.diff(Gam[a][b][a], coords[c])
                           + sum(Gam[a][a][e] * Gam[e][b][c] - Gam[a][c][e] * Gam[e][b][a] for e in range(n))
                           for a in range(n)))


Rs = sp.simplify(sum(Gi[b, c] * Ric(b, c) for b in range(n) for c in range(n)))
rep("[1] scalar curvature = -6/c1, independent of c2", sp.simplify(Rs + 6 / c1) == 0, f"(R = {Rs})")

# [2]
def cut_len(ell, eps):
    a = ell / 2
    # semicircle radius a, hyperbolic length from height eps to eps: 2 arccosh? exact: 2*log((a+sqrt(a^2-eps^2))/eps)
    t = np.linspace(np.arcsin(eps / a), np.pi - np.arcsin(eps / a), 400001)
    xs, zs = a * np.cos(t), a * np.sin(t)
    ds = np.hypot(np.diff(xs), np.diff(zs)) / ((zs[:-1] + zs[1:]) / 2)
    return ds.sum()


eps = 1e-3
ok = all(abs(cut_len(l, eps) - 2 * np.log(l / eps)) < 1e-3 for l in (0.3, 1.0, 2.5))
rep("[2] geodesic cut-off length = 2 log(l/eps) + O(eps^2)", ok)
dstar = None
for dl in np.linspace(0.05, 1.0, 96):
    disc = 2 * cut_len(1.0, eps)
    conn = cut_len(2 + dl, eps) + cut_len(dl, eps)
    if conn < disc:
        dstar = dl
rep("[2] connected pair shorter iff delta < sqrt2-1 = %.4f (numerical last delta %.3f)" % (np.sqrt(2) - 1, dstar),
    abs(dstar - (np.sqrt(2) - 1)) < 0.011)
dmut = (-1 + np.sqrt(5)) / 2       # root of delta(1+delta)=1
rep("[2] NEG mutation delta(1+delta)<1 gives threshold %.3f != numerical" % dmut, abs(dmut - dstar) > 0.1)

# [3]
sig = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]], complex), np.array([[1, 0], [0, -1]], complex)]
coef = rng.normal(size=(3, 3, 2))


def Adot(s):   # su(2)-valued A(gamma(s)) gamma'(s) along the loop, smooth periodic
    c = [coef[i, j, 0] * np.cos((j + 1) * 2 * np.pi * s) + coef[i, j, 1] * np.sin((j + 1) * 2 * np.pi * s) for i in range(3) for j in range(3)]
    a = [sum(c[3 * i: 3 * i + 3]) for i in range(3)]
    return -0.5j * sum(a[i] * sig[i] for i in range(3))


def exact(nst=40000, T=1.0):
    U = np.eye(2, dtype=complex); h = T / nst
    for i in range(nst):
        s = i * h
        k1 = U @ Adot(s); k2 = (U + h / 2 * k1) @ Adot(s + h / 2)
        k3 = (U + h / 2 * k2) @ Adot(s + h / 2); k4 = (U + h * k3) @ Adot(s + h)
        U = U + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return U


Uex = exact()


def disc_hol(k, rule="mid", reverse=False, T=1.0):
    fac = [expm(T * Adot(T * (e + (0.5 if rule == "mid" else 0.0)) / k) / k) for e in range(k)]
    if reverse:
        fac = fac[::-1]
    U = np.eye(2, dtype=complex)
    for F in fac:
        U = U @ F
    return U


ks = [16, 32, 64, 128]
err = [abs(np.trace(disc_hol(k)) - np.trace(Uex)) for k in ks]
order = np.polyfit(np.log(ks), np.log(err), 1)[0]
rep("[3] midpoint trace error order %.2f (claim O(k^-2))" % -order, -order > 1.8)
# on a periodic loop the left rule is also 2nd order (commutator-dominated), so the order
# detector is tested on an open arc [0, 0.7]: midpoint must give 2, left endpoint 1
Uo = exact(T=0.7)
eM = [np.linalg.norm(disc_hol(k, T=0.7) - Uo) for k in ks]
eL = [np.linalg.norm(disc_hol(k, "left", T=0.7) - Uo) for k in ks]
oM = -np.polyfit(np.log(ks), np.log(eM), 1)[0]; oL = -np.polyfit(np.log(ks), np.log(eL), 1)[0]
rep("[3] open arc: midpoint order %.2f" % oM, oM > 1.8)
rep("[3] NEG left-endpoint rule on open arc: order %.2f < 1.5" % oL, oL < 1.5)
errM = [np.linalg.norm(disc_hol(k) - Uex) for k in ks]
errR = [np.linalg.norm(disc_hol(k, reverse=True) - Uex) for k in ks]
rep("[3] NEG reversed product order does not converge (matrix error %.2e vs %.2e)" % (errR[-1], errM[-1]),
    errR[-1] > 100 * errM[-1])

# [4]
def gs(p, X):
    P = p[:, None] + p[None, :]
    return (2 / P * abs(X) ** 2).sum()


def gb(p, X):
    lp = np.log(p)
    D = p[:, None] - p[None, :]
    with np.errstate(divide="ignore", invalid="ignore"):
        c = np.where(np.abs(D) > 1e-14, (lp[:, None] - lp[None, :]) / D, 1 / p[:, None])
    return (c * abs(X) ** 2).sum()


ratios = []
for _ in range(2000):
    p = rng.dirichlet(np.ones(3))
    M = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    X = M + M.conj().T; X -= np.trace(X) / 3 * np.eye(3)
    ratios.append(gb(p, X) / gs(p, X))
ratios = np.array(ratios)
Xd = np.diag([0.3, -0.1, -0.2]).astype(complex); p = np.array([0.5, 0.3, 0.2])
rep("[4] BKM >= SLD always; equality for diagonal X",
    ratios.min() >= 1 - 1e-12 and abs(gb(p, Xd) / gs(p, Xd) - 1) < 1e-12,
    f"(ratio range {ratios.min():.3f}..{np.percentile(ratios, 99.5):.3f}, max {ratios.max():.2f})")
rep("[4] NEG mutation SLD >= BKM fails", np.any(ratios > 1 + 1e-6))

# [5]
viol, violm, tested = 0, 0, 0
for trial in range(60):
    nv = 7
    W = rng.uniform(0.05, 2.0, (nv, nv)); W = (W + W.T) / 2
    Adj = (rng.random((nv, nv)) < 0.5); Adj = np.triu(Adj, 1); Adj = Adj | Adj.T
    for i in range(nv - 1):
        Adj[i, i + 1] = Adj[i + 1, i] = True
    Dm = shortest_path(np.where(Adj, W, 0), directed=False)
    def m(xv):
        nb = np.where(Adj[xv])[0]
        mu = np.zeros(nv); mu[nb] = 1 / len(nb); return mu
    def W1(a, b):
        cst = Dm.ravel()
        Aeq = []
        for i in range(nv):
            r = np.zeros((nv, nv)); r[i, :] = 1; Aeq.append(r.ravel())
        for j in range(nv):
            r = np.zeros((nv, nv)); r[:, j] = 1; Aeq.append(r.ravel())
        return linprog(cst, A_eq=np.array(Aeq), b_eq=np.concatenate([a, b]), bounds=(0, None), method="highs").fun
    for xv in range(nv):
        for yv in range(xv + 1, nv):
            kap = 1 - W1(m(xv), m(yv)) / Dm[xv, yv]
            J = lambda v: (m(v) * Dm[v]).sum()
            lb = -(J(xv) + J(yv)) / Dm[xv, yv]
            tested += 1
            viol += kap < lb - 1e-9
            violm += kap < lb / 2 - 1e-9
rep("[5] Ollivier kappa >= -(J(x)+J(y))/d on %d pairs" % tested, viol == 0)
# tight example: path a-x-y-b, |ax|=|yb|=1, |xy|=dd, walks m_x = delta_a, m_y = delta_b
for dd in (0.5, 0.1, 0.01):
    W1 = 2 + dd; kap = 1 - W1 / dd; lb = -(1 + 1) / dd
    tight = abs(kap - lb) < 1e-12
    violm += kap < lb / 2
rep("[5] tight example: kappa = -2/d attains the bound, unbounded as d->0", tight)
rep("[5] NEG mutation -(J(x)+J(y))/(2d) violated (%d cases)" % violm, violm > 0)

print("\nSUMMARY: %d / %d ok" % (sum(res), len(res)))

# [4b] ratio range under the Hilbert-Schmidt (Ginibre) measure used by the referee
rr = []
for _ in range(5000):
    Gm = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    p = np.linalg.eigvalsh(Gm @ Gm.conj().T); p = p / p.sum()
    M = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    X = M + M.conj().T; X -= np.trace(X) / 3 * np.eye(3)
    rr.append(gb(p, X) / gs(p, X))
rr = np.array(rr)
print("[4b] HS-random qutrits, 5000 samples: ratio min %.3f, median %.3f, 95%% %.3f, max %.2f"
      % (rr.min(), np.median(rr), np.percentile(rr, 95), rr.max()))
