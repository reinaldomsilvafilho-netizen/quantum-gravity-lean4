"""L1 blind check A2 (ch. 2, thm:toda_qr).

Oracle 1: integrate the Toda ODE dA/dt = [A, Pi_so(A)] with solve_ivp.
Oracle 2: QR of expm(t A0) with positive diagonal R, A_qr = Q^T A0 Q.
Non-circular route: given the Toda solution A(t), solve the LINEAR ODE
dQ/dt = Q K(t), K = Pi_so(A(t)), Q(0) = I; then B = Q^T A0 Q must equal A.
Negative controls: QR of expm(-t A0); Toda with the opposite sign.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm, qr

rng = np.random.default_rng(7)
n = 5
X = rng.normal(size=(n, n))
A0 = (X + X.T) / 2


def pso(A):
    L = np.tril(A, -1)
    return L - L.T


def toda(t, a, sign=1):
    A = a.reshape(n, n)
    K = pso(A)
    return (sign * (A @ K - K @ A)).ravel()


def qr_pos(M):
    Q, R = qr(M)
    D = np.diag(np.sign(np.diag(R)))
    return Q @ D, D @ R


ts = [0.3, 1.0, 2.0]
sol = solve_ivp(toda, (0, 2.0), A0.ravel(), t_eval=ts, rtol=1e-11, atol=1e-12)
solneg = solve_ivp(lambda t, a: toda(t, a, -1), (0, 2.0), A0.ravel(), t_eval=ts, rtol=1e-11, atol=1e-12)
for i, t in enumerate(ts):
    A = sol.y[:, i].reshape(n, n)
    Q, _ = qr_pos(expm(t * A0))
    Qm, _ = qr_pos(expm(-t * A0))
    e_ok = np.abs(A - Q.T @ A0 @ Q).max()
    e_neg1 = np.abs(A - Qm.T @ A0 @ Qm).max()
    e_neg2 = np.abs(solneg.y[:, i].reshape(n, n) - Q.T @ A0 @ Q).max()
    e_spec = np.abs(np.sort(np.linalg.eigvalsh(A)) - np.sort(np.linalg.eigvalsh(A0))).max()
    print(f"t={t}: |A_toda - Q^T A0 Q| = {e_ok:.2e}; spectrum err {e_spec:.2e}; "
          f"neg ctrl exp(-tA0): {e_neg1:.2e}; neg ctrl sign flip: {e_neg2:.2e}")
    assert e_ok < 1e-7 and e_spec < 1e-8 and e_neg1 > 1e-2 and e_neg2 > 1e-2

# non-circular route: linear ODE for Q driven by the GIVEN solution
dense = solve_ivp(toda, (0, 2.0), A0.ravel(), dense_output=True, rtol=1e-11, atol=1e-12)
def qode(t, q):
    Qm = q.reshape(n, n)
    return (Qm @ pso(dense.sol(t).reshape(n, n))).ravel()
qs = solve_ivp(qode, (0, 2.0), np.eye(n).ravel(), t_eval=[2.0], rtol=1e-11, atol=1e-12)
Q2 = qs.y[:, 0].reshape(n, n)
err = np.abs(Q2.T @ A0 @ Q2 - dense.sol(2.0).reshape(n, n)).max()
print(f"linear-ODE route: |Q^T A0 Q - A(2)| = {err:.2e}; |Q^T Q - I| = {np.abs(Q2.T @ Q2 - np.eye(n)).max():.2e}")
assert err < 1e-7
# integer-time QR step on e^{A}
A1 = dense.sol(1.0).reshape(n, n); A2 = dense.sol(2.0).reshape(n, n)
Q1, R1 = qr_pos(expm(A1))
print(f"QR step: |expm(A(2)) - R1 Q1| = {np.abs(expm(A2) - R1 @ Q1).max():.2e}")
print("A2 PASS: statements (i)-(iii) are true; the issue is only the logic of the proof.")
