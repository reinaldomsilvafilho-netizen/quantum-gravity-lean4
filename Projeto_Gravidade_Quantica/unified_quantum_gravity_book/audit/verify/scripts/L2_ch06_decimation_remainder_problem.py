"""Camada 2, F-50 (cap. 6).

S1 r_m = m+3 (Prop 2.2) by an INDEPENDENT method: effective resistance between two boundary
   vertices (Laplacian pseudo-inverse) on the level-n networks of the Sierpinski m-simplex,
   n = 0, 1, 2 (m = 2, 3, 4). Ratio R_{n+1}/R_n = rho = (m+3)/(m+1) at every level
   (self-similarity), and the harmonic value a = 2/(m+3) at the midpoints.
   Mutation: rho = (m+2)/m fails.
S2 Remainder of Prop 3.1: x^2 (E - asym) -> -1/180, and my own derivation of the next term:
   Stirling x^-5 coefficient 1/1260 (times -x) and Barnes B_6/(4*2*3) = 1/1008 (times 2) give
   +1/840 x^-4.  Mutations: -1/90, -1/360 fail; next coefficient -1/840 fails.
S3 Problem 2.3 (recast open problem) -- cell locality.  For u = 1_{F_1(K)} (gasket, m=2):
   (a) every form E_k of eq. (beta_forms), k >= 1, vanishes identically on u, for ANY alpha_k, c_k
       (checked with mu-samples carrying addresses);
   (b) u is not in the domain of Kigami's form: renormalized graph energies (5/3)^n sum over
       level-n edges of the indicator grow like 4 (5/3)^n; control: a harmonic function has
       constant energy.
   Since each E_k is a bounded form on L^2(mu) (bounded kernel), Mosco's liminf condition
   liminf E_k(u_k) >= E_K(u) fails already for u_k = u.  Mutation: a NON cell-local form (pairs
   in different level-k cells within the kernel range) is > 0 on u.
"""
import itertools
import math
import numpy as np
import mpmath as mp

FAIL = []


def check(name, ok, info=None):
    print(("PASS " if ok else "FAIL ") + name + ("" if info is None else "  | " + str(info)))
    if not ok:
        FAIL.append(name)


# ---------------- S1
def network(m, n):
    """vertices of level-n Sierpinski m-simplex as exact rational tuples; edges = complete graph per n-cell"""
    V0 = [tuple(1 if i == j else 0 for i in range(m + 1)) for j in range(m + 1)]  # barycentric
    cells = [V0]
    for _ in range(n):
        new = []
        for c in cells:
            for i in range(m + 1):
                new.append([tuple((a + b) / 2 for a, b in zip(c[i], v)) for v in c])
        cells = new
    idx = {}
    for c in cells:
        for v in c:
            idx.setdefault(v, len(idx))
    Lp = np.zeros((len(idx), len(idx)))
    for c in cells:
        for a, b in itertools.combinations(c, 2):
            i, j = idx[a], idx[b]
            Lp[i, i] += 1; Lp[j, j] += 1; Lp[i, j] -= 1; Lp[j, i] -= 1
    return Lp, idx, V0


for m in (2, 3, 4):
    Rs = []
    for n in (0, 1, 2):
        Lp, idx, V0 = network(m, n)
        G = np.linalg.pinv(Lp)
        i, j = idx[V0[0]], idx[V0[1]]
        Rs.append(G[i, i] + G[j, j] - 2 * G[i, j])
    rho = [Rs[1] / Rs[0], Rs[2] / Rs[1]]
    check(f"S1 m={m}: R_(n+1)/R_n = (m+3)/(m+1) at n=0,1", all(abs(r - (m + 3) / (m + 1)) < 1e-10 for r in rho), [round(r, 12) for r in rho])
    check(f"S1-mut m={m}: (m+2)/m fails", all(abs(r - (m + 2) / m) > 1e-3 for r in rho))
    # harmonic value at midpoints p_1j for boundary data (1,0,...,0)
    Lp, idx, V0 = network(m, 1)
    B = [idx[v] for v in V0]; I = [k for k in range(len(idx)) if k not in B]
    ub = np.zeros(len(B)); ub[0] = 1
    uI = np.linalg.solve(Lp[np.ix_(I, I)], -Lp[np.ix_(I, B)] @ ub)
    inv = {v: k for k, v in idx.items()}
    mid1 = [uI[t] for t, k in enumerate(I) if inv[k][0] == 0.5]
    check(f"S1 m={m}: harmonic value at p_1j is a = 2/(m+3); total energy m(1-a) = m(m+1)/(m+3)",
          np.allclose(mid1, 2 / (m + 3)) and abs(ub @ (Lp[np.ix_(B, B)] @ ub + Lp[np.ix_(B, I)] @ uI) - m * (m + 1) / (m + 3)) < 1e-12)

# ---------------- S2
mp.mp.dps = 50


def E(x):
    x = mp.mpf(x)
    return x * (x + 1) - x * mp.log(2 * mp.pi) - x * mp.loggamma(x + 1) + 2 * mp.log(mp.barnesg(x + 1))


def asym(x):
    x = mp.mpf(x)
    return x * x / 2 - x / 2 * mp.log(x) + (1 - mp.log(2 * mp.pi) / 2) * x - mp.log(x) / 6 + 2 * mp.zeta(-1, derivative=1) - mp.mpf(1) / 12


r2 = [float((E(x) - asym(x)) * x ** 2) for x in (50, 200, 800)]
r4 = [float((E(x) - asym(x) + mp.mpf(1) / (180 * x ** 2)) * x ** 4) for x in (50, 200, 800)]
print("   x^2 R:", r2, "  x^4 (R + 1/(180x^2)):", r4, "  1/840 =", 1 / 840)
check("S2 x^2 (E - asym) -> -1/180", abs(r2[-1] + 1 / 180) < 1e-7)
check("S2 next term +1/(840 x^4) (own derivation, independent of the text)", abs(r4[-1] - 1 / 840) < 1e-6)
check("S2-mut -1/90 and -1/360 fail", abs(r2[-1] + 1 / 90) > 1e-3 and abs(r2[-1] + 1 / 360) > 1e-3)
check("S2-mut next coefficient -1/840 fails", abs(r4[-1] + 1 / 840) > 1e-3)
check("S2 Barnes x^-2 coefficient = B_4/8 = -1/240", abs(float(mp.bernoulli(4)) / 8 + 1 / 240) < 1e-15)

# ---------------- S3
rng = np.random.default_rng(1)
P = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, math.sqrt(3) / 2]])
Nw, depth = 3000, 18
W = rng.integers(0, 3, size=(Nw, depth))
X = np.zeros((Nw, 2))
for j in range(depth - 1, -1, -1):
    X = 0.5 * X + 0.5 * P[W[:, j]]
u = (W[:, 0] == 0).astype(float)          # indicator of F_1(K)
uc = X[:, 0]                               # control function
alpha_k = 0.7
lg = math.lgamma
Zk = None


def kappa(z):  # symmetrized Beta kernel on Delta_2(alpha) in R^2 (3 parts), unnormalized
    def K(y):
        y1, y2 = y[..., 0], y[..., 1]
        ok = (y1 >= 0) & (y2 >= 0) & (y1 + y2 <= alpha_k)
        v = np.zeros(y1.shape)
        yy1, yy2 = y1[ok], y2[ok]
        v[ok] = np.exp(lg(alpha_k + 1) - np.array([lg(a + 1) + lg(b + 1) + lg(alpha_k - a - b + 1) for a, b in zip(yy1, yy2)]))
        return v
    return 0.5 * (K(z) + K(-z))


res = {}
for k in (1, 2, 3, 4):
    same = np.all(W[:, None, :k] == W[None, :, :k], axis=2)
    np.fill_diagonal(same, False)
    Zmat = (2 ** k) * (X[:, None, :] - X[None, :, :])       # F_w^{-1}x - F_w^{-1}y = 2^k (x-y)
    kap = kappa(Zmat)
    Eu = np.sum(same * kap * (u[:, None] - u[None, :]) ** 2) / Nw ** 2
    Ec = np.sum(same * kap * (uc[:, None] - uc[None, :]) ** 2) / Nw ** 2
    nonlocal_pairs = (~same) & (kap > 0)
    Eu_nl = np.sum(nonlocal_pairs * kap * (u[:, None] - u[None, :]) ** 2) / Nw ** 2
    res[k] = (Eu, Ec, Eu_nl)
    print("   k=%d  E_k(1_F1)=%.3e  E_k(x-coord)=%.3e  non-cell-local form on 1_F1=%.3e" % (k, Eu, Ec, Eu_nl))
check("S3a E_k(1_{F_1 K}) = 0 for k = 1..4 (cell-local forms), any alpha_k, c_k", all(r[0] == 0 for r in res.values()))
check("S3a-ctrl E_k(x-coordinate) > 0 (the sampler sees the kernel)", all(r[1] > 0 for r in res.values()))
check("S3-mut non-cell-local version is > 0 on 1_{F_1 K}", all(r[2] > 0 for r in res.values()))


# (b) Kigami renormalized energies of the indicator vs a harmonic function
def sg_energy(n):
    cells = [[(0, 0), (1, 0), (0.5, math.sqrt(3) / 2)]]
    addr = [()]
    for _ in range(n):
        nc, na = [], []
        for c, a in zip(cells, addr):
            for i in range(3):
                nc.append([tuple((np.array(c[i]) + np.array(v)) / 2) for v in c]); na.append(a + (i,))
        cells, addr = nc, na
    # indicator of F_1: value 1 at points of cells with first address 0 (junction points belong to F_1)
    pts_in_F1 = set()
    for c, a in zip(cells, addr):
        if a and a[0] == 0:
            for v in c:
                pts_in_F1.add(tuple(np.round(v, 12)))
    Eind = 0.0
    for c in cells:
        for p, q in itertools.combinations(c, 2):
            up = 1.0 if tuple(np.round(p, 12)) in pts_in_F1 else 0.0
            uq = 1.0 if tuple(np.round(q, 12)) in pts_in_F1 else 0.0
            Eind += (up - uq) ** 2
    return (5 / 3) ** n * Eind


def harmonic_energy(n):
    # harmonic extension of boundary data (1,0,0) by the 1/5-2/5 rule; energy is n-independent
    cells = [((1.0, 0.0, 0.0))]
    for _ in range(n):
        nc = []
        for (a, b, c) in cells:
            ab, bc, ca = (2 * a + 2 * b + c) / 5, (a + 2 * b + 2 * c) / 5, (2 * a + b + 2 * c) / 5
            nc += [(a, ab, ca), (ab, b, bc), (ca, bc, c)]
        cells = nc
    return (5 / 3) ** n * sum((a - b) ** 2 + (b - c) ** 2 + (c - a) ** 2 for a, b, c in cells)


Ei = [sg_energy(n) for n in range(1, 7)]
Eh = [harmonic_energy(n) for n in range(1, 7)]
print("   Kigami E_n(1_F1):", [round(e, 3) for e in Ei], "  E_n(harmonic):", [round(e, 6) for e in Eh])
check("S3b indicator: E_n = 4 (5/3)^n -> infinity (not in Kigami's domain)", all(abs(e - 4 * (5 / 3) ** n) < 1e-9 for e, n in zip(Ei, range(1, 7))))
check("S3b-ctrl harmonic function: E_n constant = 2", all(abs(e - 2) < 1e-12 for e in Eh))
print("   => Mosco liminf fails for u_k = u: liminf E_k(u) = 0 < infinity = E_K(u), for every choice of alpha_k, c_k.")
print("\nFAILURES:", FAIL if FAIL else "none")
