"""Thm 5.1 / Sec 6.4 (De Silva-Lim), Thm 5.6 (critical scaling; local .tex = Thm 5.5).

(a) Scaling of sup_{u in prod S^{d-1}} T(u1,u2,u3) for iid N(0,1) T, k=3.
    Oracle 1 (lower bound): HOPM (higher-order power method), 20 random starts.
    Oracle 2 (rigorous upper bound): sup <= ||T_(1)||_op (spectral norm of the d x d^2 unfolding).
    Compare normalisations d^{-1/2} (Zenodo latest) and d^{-(k-1)/2} = d^{-1} (local .tex).
(b) Thm 5.6(ii): tail P(|f_hat|>eps) for random Haar u vs 2 exp(-d eps^2/2) (Gaussian case exact).
(c) De Silva-Lim: T = a(x)a(x)b + a(x)b(x)a + b(x)a(x)a. Rank-2 tensors
    X_t = t (a+b/t)^{(x)3} - t a^{(x)3} give ||T - X_t|| = O(1/t) with weights |lambda| = t -> inf,
    although every factor lies on the unit sphere after normalisation. Bounded-weight search:
    minimise ||T - X|| over rank-2 X with unit factors and |lambda_i| <= L (multi-start L-BFGS);
    the minimum stays > 0 and decreases with L -> compactness of prod S^{d-1} does not remove
    the pathology for rank r = 2.
Negative control: claim 'd^{-(k-1)/2} sup = Theta(1)' must fail; 'error 0 at bounded weights' must fail.
"""
import sys

import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(2)
fail = 0


def hopm(T, starts=20, iters=200):
    d = T.shape[0]
    best = 0
    for _ in range(starts):
        u = [rng.standard_normal(d) for _ in range(3)]
        u = [x / np.linalg.norm(x) for x in u]
        for _ in range(iters):
            u[0] = np.einsum("ijk,j,k->i", T, u[1], u[2]); u[0] /= np.linalg.norm(u[0])
            u[1] = np.einsum("ijk,i,k->j", T, u[0], u[2]); u[1] /= np.linalg.norm(u[1])
            u[2] = np.einsum("ijk,i,j->k", T, u[0], u[1]); u[2] /= np.linalg.norm(u[2])
        best = max(best, abs(np.einsum("ijk,i,j,k->", T, *u)))
    return best


print("== (a) scaling of the spectral norm of iid Gaussian 3-tensors ==")
print("  d   HOPM_lower  unfold_upper  lower/sqrt(d)  upper/d   lower/d")
rows = []
for d in [8, 16, 32, 64]:
    vals = []
    ups = []
    for rep in range(3):
        T = rng.standard_normal((d, d, d))
        vals.append(hopm(T, starts=10 if d == 64 else 20))
        ups.append(np.linalg.norm(T.reshape(d, d * d), 2))
    lo, up = np.mean(vals), np.mean(ups)
    rows.append((d, lo, up))
    print(f"{d:4d} {lo:10.3f} {up:12.3f} {lo / np.sqrt(d):12.3f} {up / d:9.3f} {lo / d:9.3f}")
r_sqrt = [r[1] / np.sqrt(r[0]) for r in rows]
r_lin = [r[1] / r[0] for r in rows]
print("lower/sqrt(d) roughly constant (Zenodo 1/sqrt(d) normalisation, Tomioka-Suzuki ~ sqrt(k d log k)):",
      max(r_sqrt) / min(r_sqrt) < 1.3)
print("lower/d decays like d^{-1/2} (local .tex normalisation d^{-(k-1)/2} gives -> 0):",
      [round(x, 3) for x in r_lin])
fail += not (max(r_sqrt) / min(r_sqrt) < 1.3)
fail += not (r_lin[-1] < 0.5 * r_lin[0])   # negative control: Theta(1) claim must fail

print("\n== (b) tail bound of Thm 5.6(ii) (Gaussian entries, k=3) ==")
for d in [10, 40]:
    S = 20000
    vals = np.empty(S)
    for s in range(S):
        T = rng.standard_normal((d, d, d)) if s % 200 == 0 else T
        u = [rng.standard_normal(d) for _ in range(3)]
        u = [x / np.linalg.norm(x) for x in u]
        vals[s] = np.einsum("ijk,i,j,k->", T, *u) / np.sqrt(d)
    for eps in [0.2, 0.4, 0.6]:
        emp = np.mean(np.abs(vals) > eps)
        bnd = 2 * np.exp(-d * eps ** 2 / 2)
        print(f"d={d:3d} eps={eps}: empirical {emp:.4f}  bound 2exp(-d eps^2/2) {bnd:.4f}  ok={emp <= bnd + 0.01}")
        fail += emp > bnd + 0.01

print("\n== (c) De Silva-Lim example, d=2 ==")
a = np.array([1.0, 0.0]); b = np.array([0.0, 1.0])
o3 = lambda x, y, z: np.einsum("i,j,k->ijk", x, y, z)
T = o3(a, a, b) + o3(a, b, a) + o3(b, a, a)
for t in [1, 10, 100, 1000]:
    X = t * o3(a + b / t, a + b / t, a + b / t) - t * o3(a, a, a)
    w1 = t * np.linalg.norm(a + b / t) ** 3
    print(f"t={t:5d}  ||T-X_t||={np.linalg.norm(T - X):.3e}  weights |lambda|=({w1:.1f}, {t})")


def err(p, L):
    lam = L * np.tanh(p[:2])
    vs = [p[2 + 2 * i:4 + 2 * i] for i in range(6)]
    vs = [v / np.linalg.norm(v) for v in vs]
    X = lam[0] * o3(vs[0], vs[1], vs[2]) + lam[1] * o3(vs[3], vs[4], vs[5])
    return np.linalg.norm(T - X) ** 2


prev = None
mins = []
for L in [2, 5, 20, 100]:
    best = min(minimize(err, rng.standard_normal(14), args=(L,), method="L-BFGS-B").fun for _ in range(60))
    mins.append(np.sqrt(best))
    print(f"|lambda| <= {L:4d}: best rank-2 error found = {np.sqrt(best):.4e}")
print("rank-1 best approximation (sigma_max, Thm 5.1) exists; rank-2 infimum 0 approached only as |lambda|->inf")
fail += not (mins[-1] < mins[0])
fail += mins[0] < 1e-6        # negative control: bounded weights must not reach 0

print("\nfailures:", fail)
sys.exit(int(fail))
