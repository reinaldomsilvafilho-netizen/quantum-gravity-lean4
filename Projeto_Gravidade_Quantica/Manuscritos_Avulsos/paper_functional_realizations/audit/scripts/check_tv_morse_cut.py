"""Thm 4.4 (TV of step realization), Thm 4.6 (Morse indices), Thm 4.9 / Ex 4.11 (cut norm).

TV oracle: mollify W_A with a Gaussian of width eps on an M x M pixel grid of (0,1)^2,
compute int |grad (W*rho_eps)| (isotropic) restricted to the interior, refine eps, M.
Morse oracle: index from finite-difference Hessian of f(exp_x(t u)) in a random tangent basis.
Cut-norm oracle: brute force over unions of cells (exact for step kernels by linearity in
|S cap I_i|) and over sign vectors for the L^inf->L^1 norm.
Negative controls: TV formula without 1/n; Morse index n-i instead of i-1; cut/op ratio bound 2.
"""
import itertools
import sys

import numpy as np
from scipy.ndimage import gaussian_filter

rng = np.random.default_rng(1)
fail = 0

# ---------------- TV ----------------
def tv_formula(A):
    n = A.shape[0]
    return (np.abs(np.diff(A, axis=0)).sum() + np.abs(np.diff(A, axis=1)).sum()) / n


def tv_mollified(A, M, eps):
    n = A.shape[0]
    W = np.kron(A, np.ones((M // n, M // n)))
    h = 1.0 / M
    # reflect padding: BV on the open square; mollifier does not see outside jumps
    Ws = gaussian_filter(W, sigma=eps / h, mode="reflect")
    gx, gy = np.gradient(Ws, h)
    return np.sum(np.sqrt(gx ** 2 + gy ** 2)) * h * h


n = 4
A = rng.integers(-3, 4, size=(n, n)).astype(float)
print("== Thm 4.4 TV, A =\n", A)
exact = tv_formula(A)
print("formula TV =", exact, "| no-1/n mutant =", exact * n)
errs = []
for M, eps in [(256, 0.02), (512, 0.01), (1024, 0.005), (2048, 0.0025)]:
    v = tv_mollified(A, M, eps)
    errs.append(abs(v - exact))
    print(f"M={M:5d} eps={eps:.4f} TV_moll={v:.5f}  |err|={errs[-1]:.2e}")
print("error ratios per halving of eps:", [round(errs[i] / errs[i + 1], 2) for i in range(len(errs) - 1)])
ok = errs[-1] < 0.02 * exact and errs[-1] < errs[0]
mut = abs(tv_mollified(A, 2048, 0.0025) - exact * n) < 0.02 * exact * n
print("TV formula confirmed:", ok, "| mutant confirmed (must be False):", mut)
fail += (not ok) + mut

# ---------------- Morse ----------------
def morse_index(A, x, h=1e-4):
    nn = len(x)
    Q, _ = np.linalg.qr(np.column_stack([x, rng.standard_normal((nn, nn - 1))]))
    U = Q[:, 1:]
    f = lambda y: y @ A @ y
    def g(s):  # point on sphere from tangent coords via exponential map
        v = U @ s
        r = np.linalg.norm(v)
        return x if r == 0 else np.cos(r) * x + np.sin(r) * v / r
    m = nn - 1
    H = np.zeros((m, m))
    for i in range(m):
        for j in range(m):
            ei = np.eye(m)[i] * h; ej = np.eye(m)[j] * h
            H[i, j] = (f(g(ei + ej)) - f(g(ei - ej)) - f(g(-ei + ej)) + f(g(-ei - ej))) / (4 * h * h)
    ev = np.linalg.eigvalsh(H)
    return int(np.sum(ev < 0)), np.min(np.abs(ev))


print("\n== Thm 4.6 Morse indices ==")
for nn in [1, 2, 3, 5, 6]:
    B = rng.standard_normal((nn, nn)); A2 = (B + B.T) / 2
    lam, V = np.linalg.eigh(A2)
    if nn == 1:
        print("n=1: S^0 = 2 points, chi=2, formula 1-(-1)^1 =", 1 - (-1) ** 1)
        continue
    idx = []
    for i in range(nn):
        for s in [1, -1]:
            k, gap = morse_index(A2, s * V[:, i])
            idx.append(k)
            fail += (k != i)
    chi = sum((-1) ** k for k in idx)
    print(f"n={nn}: indices {idx}  sum(-1)^ind={chi}  1-(-1)^n={1 - (-1) ** nn}  mutant(n-i) would give {[nn - 1 - i for i in range(nn)]}")
    fail += chi != 1 - (-1) ** nn
# gradient check: random x is not critical
B = rng.standard_normal((4, 4)); A2 = (B + B.T) / 2
x = rng.standard_normal(4); x /= np.linalg.norm(x)
gr = 2 * A2 @ x - 2 * (x @ A2 @ x) * x
print("Riemannian gradient tangent (x.grad=0):", abs(x @ gr) < 1e-12)

# ---------------- cut norm ----------------
def cut_norm_step(A):
    n = A.shape[0]
    best = 0.0
    for s in itertools.product([0, 1], repeat=n):
        r = np.array(s) @ A  # row-sums over S
        best = max(best, r[r > 0].sum(), -r[r < 0].sum())
    return best / n ** 2


def op_norm_step(A):
    n = A.shape[0]
    best = 0.0
    for s in itertools.product([-1, 1], repeat=n):
        best = max(best, np.abs(np.array(s) @ A).sum())
    return best / n ** 2


print("\n== Thm 4.9 cut norm vs L^inf->L^1 norm (step kernels, n=7) ==")
rmax = 0
for t in range(300):
    A3 = rng.standard_normal((7, 7))
    c, o = cut_norm_step(A3), op_norm_step(A3)
    rmax = max(rmax, o / c)
    fail += not (c <= o + 1e-12 and o <= 4 * c + 1e-12)
print("max op/cut over 300 random kernels:", round(rmax, 3), "(theorem: in [1,4]; mutant bound 2 violated:", rmax > 2, ")")
A4 = np.array([[1, -1], [-1, 1]], float)
print("checker 2x2: cut =", cut_norm_step(A4), " op =", op_norm_step(A4), " ratio", op_norm_step(A4) / cut_norm_step(A4))
for nI in [4, 8, 12]:
    print(f"Ex 4.11: ||W_I||_cut for n={nI}:", cut_norm_step(np.eye(nI)), "= 1/n:", np.isclose(cut_norm_step(np.eye(nI)), 1 / nI))
    fail += not np.isclose(cut_norm_step(np.eye(nI)), 1 / nI)

print("\nfailures:", fail)
sys.exit(int(fail))
