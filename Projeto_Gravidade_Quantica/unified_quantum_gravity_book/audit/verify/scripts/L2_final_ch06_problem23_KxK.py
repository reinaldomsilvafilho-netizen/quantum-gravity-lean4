"""L2 (final integration) independent check of ch6 Problem 2.3 on K x K.

Independent of the corrector's script (random addresses + 2/5 rule recursion):
  * mu is discretized deterministically: one atom of mass 3^-L at the centroid of every level-L cell;
  * harmonic functions are obtained by a direct sparse linear solve of the level-L graph Laplacian
    (Dirichlet data e_j on the three corners), checked against Kigami's renormalized energy,
    which must be the same (=2) at every level n <= L (oracle);
  * E_k(u) = c_k sum_{x,y} kappa_alpha(2^k (x-y)) |u(x)-u(y)|^2 mu(x) mu(y), c_k = 15^k.
Negative controls:
  NC1 linear interpolation instead of the harmonic solve must fail the Kigami-energy invariance;
  NC2 the cell-local form (pairs restricted to the same level-k cell) must vanish on 1_{F_1 K};
  NC3 an isotropic kernel (radial, same support radius) must give a smaller anisotropy spread than kappa.
"""
import math
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.special import gammaln

L, alpha = 7, 0.7
P = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, math.sqrt(3) / 2]])
FAIL = []


def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + ("  | " + str(info) if info != "" else ""))
    if not ok:
        FAIL.append(name)


# ---- level-L vertex graph -------------------------------------------------------------
def cells(level):
    """list of (address tuple, 3x2 vertex array)"""
    out = [((), P.copy())]
    for _ in range(level):
        new = []
        for addr, V in out:
            for i in range(3):
                new.append((addr + (i,), 0.5 * (V + V[i])))
        out = new
    return out


def vertex_graph(level):
    C = cells(level)
    key = lambda p: (round(p[0] * 2 ** (level + 2)), round(p[1] * 2 ** (level + 2) / math.sqrt(3)))
    idx, pts, edges = {}, [], set()
    for _, V in C:
        ids = []
        for p in V:
            kk = key(p)
            if kk not in idx:
                idx[kk] = len(pts); pts.append(p)
            ids.append(idx[kk])
        for a in range(3):
            for b in range(a + 1, 3):
                edges.add((min(ids[a], ids[b]), max(ids[a], ids[b])))
    return np.array(pts), np.array(sorted(edges)), C, idx, key


pts, E, C, idx, key = vertex_graph(L)
nV = len(pts)
corner = [idx[key(p)] for p in P]


def harmonic(j):
    W = sp.coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(nV, nV))
    W = (W + W.T).tocsr()
    Lap = sp.diags(np.asarray(W.sum(1)).ravel()) - W
    free = np.setdiff1d(np.arange(nV), corner)
    g = np.zeros(nV); g[corner[j]] = 1.0
    u = np.zeros(nV); u[corner] = g[corner]
    rhs = -Lap[free][:, corner] @ g[corner]
    u[free] = spla.spsolve(Lap[free][:, free].tocsc(), rhs)
    return u


def kigami_energy(u, level):
    pts_n, E_n, _, _, key_n = vertex_graph(level)
    loc = {key(p): i for i, p in enumerate(pts)}  # level-L keys (finer grid contains level-n vertices)
    vals = np.array([u[loc[key(p)]] for p in pts_n])
    return (5 / 3) ** level * np.sum((vals[E_n[:, 0]] - vals[E_n[:, 1]]) ** 2)


H = [harmonic(j) for j in range(3)]
en = [[kigami_energy(H[j], n) for n in range(0, 5)] for j in range(3)]
check("oracle: Kigami energy of h_j is 2 at levels 0..4", np.allclose(en, 2.0, atol=1e-9), np.round(en, 6).tolist())
lin = pts @ np.linalg.solve(np.c_[P, np.ones(3)].T[:2].T if False else np.eye(2), np.eye(2))[:, 0]  # x-coordinate
lin = (pts[:, 0] - 0.0)  # linear function x, harmonic data e_1 on corners would be (0,1,0.5)
en_lin = [kigami_energy(lin, n) for n in range(0, 5)]
check("NC1 linear function: Kigami energy NOT constant (control must differ)", np.ptp(en_lin) > 0.1, np.round(en_lin, 4).tolist())

# ---- mu atoms: centroids of level-L cells; function values = mean of vertex values ----
X = np.array([V.mean(0) for _, V in C])
A = np.array([a for a, _ in C])
vid = np.array([[idx[key(p)] for p in V] for _, V in C])
Hc = [h[vid].mean(1) for h in H]
ind = (A[:, 0] == 1).astype(float)  # 1_{F_1 K}, F_1 = cell at P1 = (1,0)
N = len(X); w = 1.0 / N


def Kbeta(y):
    y1, y2 = y[..., 0], y[..., 1]
    ok = (y1 >= 0) & (y2 >= 0) & (y1 + y2 <= alpha)
    out = np.zeros(y1.shape)
    a, b = y1[ok], y2[ok]
    out[ok] = np.exp(gammaln(alpha + 1) - gammaln(a + 1) - gammaln(b + 1) - gammaln(alpha - a - b + 1))
    return out


def kappa(z):
    return 0.5 * (Kbeta(z) + Kbeta(-z))


def kiso(z):
    return (np.hypot(z[..., 0], z[..., 1]) <= alpha).astype(float)


funcs = {"1_F1": ind, "h0": Hc[0], "h1": Hc[1], "h2": Hc[2]}
Ks = range(1, 5)
res = {k: {n: 0.0 for n in funcs} for k in Ks}
iso = {k: {n: 0.0 for n in funcs} for k in Ks}
loc = {k: 0.0 for k in Ks}
B = 500
for k in Ks:
    for s in range(0, N, B):
        Z = (2 ** k) * (X[s:s + B, None, :] - X[None, :, :])
        kap, ki = kappa(Z), kiso(Z)
        same = np.all(A[s:s + B, None, :k] == A[None, :, :k], axis=2)
        for n, u in funcs.items():
            d2 = (u[s:s + B, None] - u[None, :]) ** 2
            res[k][n] += np.sum(kap * d2); iso[k][n] += np.sum(ki * d2)
        loc[k] += np.sum(same * kap * (ind[s:s + B, None] - ind[None, :]) ** 2)
    for n in funcs:
        res[k][n] *= 15.0 ** k * w * w; iso[k][n] *= 15.0 ** k * w * w
    print("k=%d " % k + " ".join("%s=%.4f" % (n, res[k][n]) for n in funcs) + "  cell-local=%.1e" % loc[k])

e = [res[k]["1_F1"] for k in Ks]
r = [e[i + 1] / e[i] for i in range(len(e) - 1)]
check("not trivially false: E_k(1_F1) > 0 and grows (ratios > 1.3)", all(x > 0 for x in e) and all(x > 1.3 for x in r),
      {"E": np.round(e, 4).tolist(), "ratios": np.round(r, 3).tolist()})
check("NC2 cell-local form vanishes on 1_F1", all(loc[k] == 0 for k in Ks))
eh = np.array([[res[k][f"h{j}"] for j in range(3)] for k in Ks])
ei = np.array([[iso[k][f"h{j}"] for j in range(3)] for k in Ks])
spread, spread_iso = eh.max(1) / eh.min(1), ei.max(1) / ei.min(1)
check("harmonic E_k(h_j) bounded (max/min over k < 3)", all(eh[:, j].max() / eh[:, j].min() < 3 for j in range(3)), np.round(eh, 4).tolist())
check("anisotropy: E_k(h_j) unequal for kappa (spread > 1.2)", all(spread > 1.2), np.round(spread, 3).tolist())
check("NC3 isotropic kernel: spread close to 1 (< 1.1)", all(spread_iso < 1.1), np.round(spread_iso, 3).tolist())
print("\nFAILURES:", FAIL if FAIL else "none")
