"""L1 blind check A3 (ch. 2, prop:tangent_proj_mr).

Oracle: velocities of explicit curves t -> A(t) in M_r (finite differences),
and the dimension of span{velocities} computed by SVD (no use of the formula).
Checks: P idempotent, self-adjoint, rank = r(m+n-r), P fixes velocities,
P kills (I-UU^T) Z (I-VV^T).  Negative control: mutated P' = UU^T Z + Z VV^T.
"""
import numpy as np

rng = np.random.default_rng(3)
m, n, r = 6, 5, 2
U, _ = np.linalg.qr(rng.normal(size=(m, r)))
V, _ = np.linalg.qr(rng.normal(size=(n, r)))
S = np.diag([3.0, 1.5])
A = U @ S @ V.T
PU, PV = U @ U.T, V @ V.T


def P(Z):
    return PU @ Z + Z @ PV - PU @ Z @ PV


def Pbad(Z):
    return PU @ Z + Z @ PV


def matrix_of(op):
    M = np.zeros((m * n, m * n))
    for i in range(m * n):
        E = np.zeros(m * n); E[i] = 1
        M[:, i] = op(E.reshape(m, n)).ravel()
    return M


Pm, Pb = matrix_of(P), matrix_of(Pbad)
print("idempotent:", np.abs(Pm @ Pm - Pm).max(), " symmetric:", np.abs(Pm - Pm.T).max())
print("rank P =", np.linalg.matrix_rank(Pm), " expected r(m+n-r) =", r * (m + n - r))
vel = []
h = 1e-6
for _ in range(200):
    X, Y, Ssm = rng.normal(size=(m, r)), rng.normal(size=(n, r)), rng.normal(size=(r, r))
    Ah = (U + h * X) @ (S + h * Ssm) @ (V + h * Y).T
    Amh = (U - h * X) @ (S - h * Ssm) @ (V - h * Y).T
    vel.append(((Ah - Amh) / (2 * h)).ravel())
vel = np.array(vel)
sv = np.linalg.svd(vel, compute_uv=False)
dim = int((sv > 1e-6 * sv[0]).sum())
print("dim span of curve velocities (oracle) =", dim)
print("max |P(v) - v| over velocities:", np.abs(vel @ Pm.T - vel).max())
Z = rng.normal(size=(m, n))
N = (np.eye(m) - PU) @ Z @ (np.eye(n) - PV)
print("|P(normal)| =", np.abs(P(N)).max())
assert np.abs(Pm @ Pm - Pm).max() < 1e-12 and dim == r * (m + n - r)
bad = np.abs(Pb @ Pb - Pb).max()
print("negative control, mutated P' idempotency defect:", bad)
assert bad > 1e-2
print("A3 PASS: the statement is correct; only the proof/citation is missing.")
