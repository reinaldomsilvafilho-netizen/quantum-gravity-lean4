"""L2b check of the new proof of thm:toda_qr (chap02, ~l. 301-354).

Claims: A' = [A, Pi_so(A)], A(0) = A0 symmetric:
 (0) solution exists for all real t (also t < 0), stays symmetric;
 (i) isospectral, ||A||_F constant;
 (ii) Q' = Q Pi_so(A), Q(0) = I gives Q orthogonal and A = Q^T A0 Q;
 (iii) exp(t A0) = Q R with diag R > 0 gives the same Q; e^{A(t+1)} = R1 Q1 when e^{A(t)} = Q1 R1.
Oracles (different routes from the text): own fixed-step RK4 for the coupled (A, Q)
system (no scipy ODE solver); exp(t A0) via the eigendecomposition V e^{t L} V^T;
QR via numpy with an explicit sign fix.  Edge cases: A0 with a repeated eigenvalue, A0 = c I.
Negative controls:
 (c1) Pi mutated to the strictly UPPER part X_{>0} - X_{>0}^T: QR identity must fail;
 (c2) QR without the sign fix: Q must disagree at some t;
 (c3) e^{A(t+1)} = Q1 R1 (wrong order) must fail.
"""
import sys
import numpy as np

rng = np.random.default_rng(7)
fails = 0


def pi_so(X):
    L = np.tril(X, -1)
    return L - L.T


def pi_so_mut(X):
    U = np.triu(X, 1)
    return U - U.T


def rk4(A0, T, h, pi=pi_so):
    n = A0.shape[0]
    A = A0.copy()
    Q = np.eye(n)
    steps = int(round(abs(T) / h))
    hh = np.sign(T) * h

    def f(A, Q):
        K = pi(A)
        return A @ K - K @ A, Q @ K

    for _ in range(steps):
        k1 = f(A, Q)
        k2 = f(A + hh / 2 * k1[0], Q + hh / 2 * k1[1])
        k3 = f(A + hh / 2 * k2[0], Q + hh / 2 * k2[1])
        k4 = f(A + hh * k3[0], Q + hh * k3[1])
        A = A + hh / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        Q = Q + hh / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    return A, Q


def expm_sym(A, t):
    L, V = np.linalg.eigh(A)
    return (V * np.exp(t * L)) @ V.T


def qr_pos(X):
    Q, R = np.linalg.qr(X)
    s = np.sign(np.diag(R))
    s[s == 0] = 1
    return Q * s, (R.T * s).T


def check(A0, label, ts=(0.5, 1.0, 2.0, -1.5)):
    global fails
    worst = 0.0
    for t in ts:
        A, Q = rk4(A0, t, 1e-3)
        Qq, Rq = qr_pos(expm_sym(A0, t))
        e = max(np.abs(A - A.T).max(),
                np.abs(np.sort(np.linalg.eigvalsh((A + A.T) / 2)) - np.sort(np.linalg.eigvalsh(A0))).max(),
                abs(np.linalg.norm(A) - np.linalg.norm(A0)),
                np.abs(Q @ Q.T - np.eye(len(A0))).max(),
                np.abs(Q.T @ A0 @ Q - A).max(),
                np.abs(Q - Qq).max())
        worst = max(worst, e)
    ok = worst < 1e-8
    print(f"{'PASS' if ok else 'FAIL'} {label}: worst defect over t in {ts} = {worst:.2e}")
    fails += not ok


n = 5
A0 = rng.normal(size=(n, n)); A0 = (A0 + A0.T) / 2
check(A0, "random A0 n=5")
V = np.linalg.qr(rng.normal(size=(n, n)))[0]
A0r = V @ np.diag([1.0, 1.0, -0.5, 2.0, 2.0]) @ V.T
check(A0r, "repeated eigenvalues")
check(3.0 * np.eye(n), "A0 = 3 I (stationary)")

# time-shift / QR step at non-integer t
t = 0.7
At, _ = rk4(A0, t, 1e-3)
At1, _ = rk4(A0, t + 1, 1e-3)
Q1, R1 = qr_pos(expm_sym((At + At.T) / 2, 1.0))
e_step = np.abs(expm_sym((At1 + At1.T) / 2, 1.0) - R1 @ Q1).max()
ok = e_step < 1e-8
print(f"{'PASS' if ok else 'FAIL'} e^(A(t+1)) = R1 Q1 at t=0.7: {e_step:.2e}")
fails += not ok
e_c3 = np.abs(expm_sym((At1 + At1.T) / 2, 1.0) - Q1 @ R1).max()
okc3 = e_c3 > 1e-3
print(f"{'PASS (control fails)' if okc3 else 'FAIL (control passed)'} c3 wrong order Q1R1: {e_c3:.3f}")
fails += not okc3

# c1: mutated projection
Am, Qm = rk4(A0, 1.0, 1e-3, pi=pi_so_mut)
Qq, _ = qr_pos(expm_sym(A0, 1.0))
e_c1 = np.abs(Qm - Qq).max()
okc1 = e_c1 > 1e-3
print(f"{'PASS (control fails)' if okc1 else 'FAIL (control passed)'} c1 upper-part Pi: |Q-Q_QR| = {e_c1:.3f}")
fails += not okc1

# c2: QR without sign fix
dmax = 0.0
for tt in (0.3, 0.5, 1.0, 2.0):
    _, Qr = rk4(A0, tt, 1e-3)
    Qraw, _ = np.linalg.qr(expm_sym(A0, tt))
    dmax = max(dmax, np.abs(Qraw - Qr).max())
okc2 = dmax > 1e-3
print(f"{'PASS (control fails)' if okc2 else 'FAIL (control passed)'} c2 no sign fix: max |Q_raw - Q| = {dmax:.3f}")
fails += not okc2

# Pi_so fixes skew, kills upper triangular (used in the proof)
S = rng.normal(size=(n, n)); S = S - S.T
Ub = np.triu(rng.normal(size=(n, n)))
e_pi = max(np.abs(pi_so(S) - S).max(), np.abs(pi_so(Ub)).max())
ok = e_pi < 1e-14
print(f"{'PASS' if ok else 'FAIL'} Pi_so fixes so(n), kills b: {e_pi:.1e}")
fails += not ok
sys.exit(1 if fails else 0)
