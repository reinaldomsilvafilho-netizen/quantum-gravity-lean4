"""L2 check of the new proof of prop:tangent_proj_mr (chap02, l. 199-217).

Claims: curve c(t) = (U + t Up S^-1)(S + t M)(V + t Vp S^-1)^T has rank r and velocity
U M V^T + Up V^T + U Vp^T; inverse formulas M = U^T X V, Up = (I-UU^T) X V,
Vp = (I-VV^T) X^T U; P(Z) = Z - (I-UU^T) Z (I-VV^T) is the orthogonal projector onto T,
dim T = r(m+n-r).
Oracle: orthonormal basis of T from the image of random (M, Up, Vp) (SVD), projector B B^T;
velocity by central finite differences.
Negative controls: (c1) P' = UU^T Z + Z VV^T (no correction) is not idempotent;
(c2) curve without Sigma^-1 has a different velocity (Sigma != I).
"""
import sys
import numpy as np

rng = np.random.default_rng(3)
m, n, r = 7, 5, 2
fails = 0
U = np.linalg.qr(rng.normal(size=(m, r)))[0]
V = np.linalg.qr(rng.normal(size=(n, r)))[0]
S = np.diag([3.0, 0.7])
Pu, Pv = U @ U.T, V @ V.T


def tang(M, Up, Vp):
    return U @ M @ V.T + Up @ V.T + U @ Vp.T


def rand_params():
    M = rng.normal(size=(r, r))
    Up = (np.eye(m) - Pu) @ rng.normal(size=(m, r))
    Vp = (np.eye(n) - Pv) @ rng.normal(size=(n, r))
    return M, Up, Vp


vecs = np.array([tang(*rand_params()).ravel() for _ in range(200)])
sv = np.linalg.svd(vecs, compute_uv=False)
dim = int((sv > 1e-9 * sv[0]).sum())
_, _, Vt = np.linalg.svd(vecs, full_matrices=False)
B = Vt[:dim].T
Porc = B @ B.T


def P(Z):
    return Z - (np.eye(m) - Pu) @ Z @ (np.eye(n) - Pv)


Pmat = np.array([P(e.reshape(m, n)).ravel() for e in np.eye(m * n)]).T
e_proj = np.abs(Pmat - Porc).max()
ok = dim == r * (m + n - r) and e_proj < 1e-10
print(f"{'PASS' if ok else 'FAIL'} dim T = {dim} (claim {r*(m+n-r)}), |P - oracle projector| = {e_proj:.1e}")
fails += not ok

Mx, Upx, Vpx = rand_params()
X = tang(Mx, Upx, Vpx)
e_inv = max(np.abs(U.T @ X @ V - Mx).max(), np.abs((np.eye(m) - Pu) @ X @ V - Upx).max(),
            np.abs((np.eye(n) - Pv) @ X.T @ U - Vpx).max())
ok = e_inv < 1e-12
print(f"{'PASS' if ok else 'FAIL'} inverse formulas for (M, Up, Vp): {e_inv:.1e}")
fails += not ok

Si = np.linalg.inv(S)
A = U @ S @ V.T


def curve(t, si=Si):
    return (U + t * Upx @ si) @ (S + t * Mx) @ (V + t * Vpx @ si).T


h = 1e-5
vel = (curve(h) - curve(-h)) / (2 * h)
rk = np.linalg.matrix_rank(curve(0.05), tol=1e-10)
e_vel = np.abs(vel - X).max()
ok = e_vel < 1e-8 and rk == r
print(f"{'PASS' if ok else 'FAIL'} curve velocity defect {e_vel:.1e}, rank {rk}")
fails += not ok
vel2 = (curve(h, np.eye(r)) - curve(-h, np.eye(r))) / (2 * h)
okc2 = np.abs(vel2 - X).max() > 1e-3
print(f"{'PASS (control fails)' if okc2 else 'FAIL (control passed)'} c2 curve without Sigma^-1: {np.abs(vel2 - X).max():.3f}")
fails += not okc2


def Pm(Z):
    return Pu @ Z + Z @ Pv


Z = rng.normal(size=(m, n))
d = np.abs(Pm(Pm(Z)) - Pm(Z)).max()
okc1 = d > 1e-3
print(f"{'PASS (control fails)' if okc1 else 'FAIL (control passed)'} c1 P' idempotency defect {d:.3f}")
fails += not okc1
sys.exit(1 if fails else 0)
