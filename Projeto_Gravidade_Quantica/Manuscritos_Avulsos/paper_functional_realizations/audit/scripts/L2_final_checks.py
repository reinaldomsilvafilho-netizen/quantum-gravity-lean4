"""Final layer-2 check of the Round-3 statements of Vol. I (abstract (i)-(iv), §4 opening,
§6.5 display).  New routes, fixed seed.

(i)  Dirichlet energy E = ||DA||_F^2 + ||AD||_F^2 changes under A -> P A P^T: computed
     here from the Fourier definition sum (k1^2 + k2^2) |a_k|^2 (the formula is checked
     against a direct quadrature of |grad f_A|^2 on the torus).
(ii) TV of the step realization changes under A -> P A P^T (TV by the jump formula, and
     independently by integrating the interior level-set perimeter over t).
(iii) Morse indices of f_A(x) = x^T A x on S^{n-1}: computed from the Riemannian Hessian
     at the critical points of A and of P A P^T (critical points P v_i): identical index lists.
(iv) cut distance: delta_box(W_A, W_{PAP^T}) = 0, shown by the explicit relabelling
     (cut norm of W_A - W_B^psi computed exactly over unions of cells = 0); negative
     control: a matrix with the same spectrum but a different mean entry has
     delta_box >= |t(K2,W_A) - t(K2,W_B)| > 0.
§6.5: TV(W_A) = int H^1(d*{W_A > t} cap (0,1)^2) dt; without "cap (0,1)^2" the integral
     over a t-window below min A adds 4 per unit t (negative control: must differ).
"""
import sys
import itertools
import numpy as np

rng = np.random.default_rng(7)
fails = 0
out = []


def log(s):
    print(s)
    out.append(s)


def check(name, ok):
    global fails
    log(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        fails += 1


n = 5
A = rng.normal(size=(n, n))
A = (A + A.T) / 2
A[0, 0] += 6.0                      # localized mass so that permutation matters
perm = np.array([4, 2, 0, 3, 1])
P = np.eye(n)[perm]
B = P @ A @ P.T


def dirichlet(M):
    k = np.arange(1, n + 1)
    return float(np.sum((k[:, None] ** 2 + k[None, :] ** 2) * M ** 2))


def dirichlet_quad(M, g=64):
    # f(x) = sum a_k e^{i k.x} on the torus with normalized measure; |grad f|^2 averaged
    x = 2 * np.pi * np.arange(g) / g
    X1, X2 = np.meshgrid(x, x, indexing="ij")
    k = np.arange(1, n + 1)
    f1 = np.zeros_like(X1, complex)
    f2 = np.zeros_like(X1, complex)
    for i, k1 in enumerate(k):
        for j, k2 in enumerate(k):
            e = M[i, j] * np.exp(1j * (k1 * X1 + k2 * X2))
            f1 += 1j * k1 * e
            f2 += 1j * k2 * e
    return float(np.mean(np.abs(f1) ** 2 + np.abs(f2) ** 2))


D = np.diag(np.arange(1, n + 1))
for M, name in ((A, "A"), (B, "PAP^T")):
    e1, e2, e3 = dirichlet(M), dirichlet_quad(M), np.linalg.norm(D @ M) ** 2 + np.linalg.norm(M @ D) ** 2
    log(f"Dirichlet {name}: Fourier sum {e1:.6f}, torus quadrature {e2:.6f}, ||DA||^2+||AD||^2 {e3:.6f}")
    check(f"Dirichlet routes agree for {name}", abs(e1 - e2) < 1e-8 * e1 and abs(e1 - e3) < 1e-8 * e1)
check("(i) Dirichlet energy changes under permutation conjugation", abs(dirichlet(A) - dirichlet(B)) > 1e-3)
check("(i) spectra equal (control that the comparison is fair)",
      np.allclose(np.linalg.eigvalsh(A), np.linalg.eigvalsh(B)))


def tv_jump(M):
    return (np.abs(np.diff(M, axis=0)).sum() + np.abs(np.diff(M, axis=1)).sum()) / len(M)


def tv_coarea(M, restrict=True, pad=1.0, nt=200001):
    lo, hi = M.min() - pad, M.max() + pad
    ts = np.linspace(lo, hi, nt)
    dt = ts[1] - ts[0]
    m = len(M)
    tot = 0.0
    # interior perimeter of {W > t}: cell edges between neighbours on opposite sides of t
    pairs = [(M[:-1, :], M[1:, :]), (M[:, :-1], M[:, 1:])]
    for t in ts[:-1] + dt / 2:
        per = 0.0
        for a, b in pairs:
            per += np.sum((a > t) != (b > t)) / m
        if not restrict:   # outer square boundary: cells on the border inside {W > t}
            per += (np.sum(M[0, :] > t) + np.sum(M[-1, :] > t) + np.sum(M[:, 0] > t) + np.sum(M[:, -1] > t)) / m
        tot += per * dt
    return tot


for M, name in ((A, "A"), (B, "PAP^T")):
    j, c = tv_jump(M), tv_coarea(M, nt=40001)
    log(f"TV {name}: jump formula {j:.6f}, coarea with cap (0,1)^2 {c:.6f}")
    check(f"§6.5 display (with cap (0,1)^2) equals TV for {name}", abs(j - c) < 1e-3 * j)
cu = tv_coarea(A, restrict=False, nt=40001)
log(f"TV A without cap (0,1)^2 on the window [min-1, max+1]: {cu:.6f}")
check("negative control: display without cap (0,1)^2 differs from TV", abs(cu - tv_jump(A)) > 1.0)
check("(ii) TV changes under permutation conjugation", abs(tv_jump(A) - tv_jump(B)) > 1e-3)


def morse_indices(M):
    w, V = np.linalg.eigh(M)
    idx = []
    for i in range(len(M)):
        v = V[:, i]
        # Riemannian Hessian of x^T M x on the sphere at v: 2 (M - w_i I) restricted to v^perp
        Q = np.linalg.qr(np.c_[v, rng.normal(size=(len(M), len(M) - 1))])[0][:, 1:]
        H = Q.T @ (2 * (M - w[i] * np.eye(len(M)))) @ Q
        idx.append(int(np.sum(np.linalg.eigvalsh(H) < 0)))
    return idx


iA, iB = morse_indices(A), morse_indices(B)
log(f"Morse indices (eigenvalues ascending): A {iA}, PAP^T {iB}")
check("(iii) Morse indices equal for A and PAP^T, and equal i-1", iA == iB == list(range(n)))
chi = sum(2 * (-1) ** k for k in iA)
check("(iii) Morse count recovers chi(S^{n-1}) = 1 + (-1)^{n-1}", chi == 1 + (-1) ** (n - 1))


def cut_norm_cells(Dm):
    m = len(Dm)
    best = 0.0
    for S in itertools.product([0, 1], repeat=m):
        s = np.array(S, bool)
        if not s.any():
            continue
        r = Dm[s, :].sum(axis=0)
        best = max(best, r[r > 0].sum(), -r[r < 0].sum())
    return best / m ** 2


An = (A - A.min()) / (A.max() - A.min())
Bn = P @ An @ P.T
Bpsi = P.T @ Bn @ P           # relabel B back: W_B^psi with psi the interval permutation
c0 = cut_norm_cells(An - Bpsi)
cplain = cut_norm_cells(An - Bn)
log(f"cut norm ||W_A - W_B^psi|| = {c0:.3e}; plain ||W_A - W_B|| = {cplain:.4f}")
check("(iv) delta_box(W_A, W_{PAP^T}) = 0 via explicit relabelling", c0 < 1e-12)
check("(iv) plain cut norm without relabelling is > 0 (relabelling matters)", cplain > 1e-3)
Q, _ = np.linalg.qr(rng.normal(size=(n, n)))
C = Q @ A @ Q.T
Cn = (C - A.min()) / (A.max() - A.min())
lb = abs(An.mean() - Cn.mean())
log(f"control: orthogonally similar C (same spectrum): delta_box >= |edge density diff| = {lb:.4f}")
check("negative control: same spectrum but delta_box > 0 for a non-permutation conjugate", lb > 1e-3)

log(f"failures: {fails}")
with open(__file__.replace(".py", ".out.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
sys.exit(fails)
