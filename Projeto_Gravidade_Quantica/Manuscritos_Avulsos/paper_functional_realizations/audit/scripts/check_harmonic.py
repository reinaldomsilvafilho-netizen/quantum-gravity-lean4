"""Checks of the harmonic realization (Construction 3.7, Thm 4.1, Example 4.2, Thm 5.4).

f_A(x) = (1/n) sum_{k1,k2=1..n} a_{k1k2} exp(i(k1 x1 + k2 x2)) on T^2 = [0,2pi)^2, Lebesgue measure.

Oracle (independent of Parseval): sample f on an M x M grid, compute ||f||_2^2 and
||grad f||_2^2 by the rectangle rule with the gradient from centred finite differences
(not from the Fourier formula); refinement study in M.
Negative control: the paper's formulas ||f||=||A||_F and E = sum (k1^2+k2^2)|a|^2 must fail.
"""
import sys
import numpy as np

rng = np.random.default_rng(0)
fail = 0


def sample(A, M):
    n = A.shape[0]
    x = 2 * np.pi * np.arange(M) / M
    k = np.arange(1, n + 1)
    E = np.exp(1j * np.outer(x, k))           # M x n
    return (E @ A @ E.T) / n, x               # f[x1,x2]


def norms_fd(A, M):
    f, x = sample(A, M)
    h = 2 * np.pi / M
    fx = (np.roll(f, -1, 0) - np.roll(f, 1, 0)) / (2 * h)
    fy = (np.roll(f, -1, 1) - np.roll(f, 1, 1)) / (2 * h)
    L2 = np.sum(abs(f) ** 2) * h * h
    Dir = np.sum(abs(fx) ** 2 + abs(fy) ** 2) * h * h
    return L2, Dir


def paper_E(A):
    n = A.shape[0]
    k = np.arange(1, n + 1)
    W = k[:, None] ** 2 + k[None, :] ** 2
    return np.sum(W * abs(A) ** 2)


n = 5
A = rng.standard_normal((n, n))
print("== Construction 3.7 / Thm 4.1, random 5x5 A ==")
prev = None
errs = []
for M in [64, 128, 256, 512, 1024]:
    L2, Dir = norms_fd(A, M)
    errs.append(abs(Dir - (2 * np.pi) ** 2 / n ** 2 * paper_E(A)))
    print(f"M={M:4d}  ||f||^2={L2:.8f}  E_fd={Dir:.8f}  err_vs_corrected={errs[-1]:.3e}")
print("observed FD convergence orders:", [round(float(np.log2(errs[i] / errs[i + 1])), 2) for i in range(len(errs) - 1)], "(expected 2)")
true_L2 = (2 * np.pi) ** 2 / n ** 2 * np.sum(A ** 2)
true_E = (2 * np.pi) ** 2 / n ** 2 * paper_E(A)
print("corrected ||f||^2 = (2pi/n)^2 ||A||_F^2 =", true_L2)
print("paper     ||f||^2 = ||A||_F^2           =", np.sum(A ** 2))
print("corrected E = (2pi/n)^2 sum(k1^2+k2^2)a^2 =", true_E)
print("paper     E = sum(k1^2+k2^2)a^2            =", paper_E(A))
L2, Dir = norms_fd(A, 1024)
ok_corr = abs(L2 - true_L2) < 1e-8 * true_L2 and abs(Dir - true_E) < 1e-3 * true_E
paper_ok = abs(L2 - np.sum(A ** 2)) < 1e-6 * L2 or abs(Dir - paper_E(A)) < 1e-3 * Dir
print("corrected formulas match oracle:", ok_corr, "| paper formulas match oracle (neg. control, must be False):", paper_ok)
fail += (not ok_corr) + paper_ok

# matrix-algebra expression: sum (i^2+j^2) a_ij^2 = ||D A||_F^2 + ||A D||_F^2
D = np.diag(np.arange(1, n + 1))
alg = np.linalg.norm(D @ A) ** 2 + np.linalg.norm(A @ D) ** 2
print("sum (k1^2+k2^2)a^2 == ||DA||^2+||AD||^2 :", np.isclose(alg, paper_E(A)))
fail += not np.isclose(alg, paper_E(A))

print("\n== Thm 4.1 'consequently' for general A: permutation-invariant counterexamples ==")
for name, B in [("I_n", np.eye(6)), ("J_n", np.ones((6, 6)))]:
    ratios = []
    import itertools
    for p in itertools.permutations(range(6)):
        P = np.eye(6)[list(p)]
        ratios.append(paper_E(P @ B @ P.T) / paper_E(B))
    print(f"{name}: max ratio over all 720 permutations = {max(ratios):.3f}, min = {min(ratios):.3f}")
    fail += not np.isclose(max(ratios), 1.0)
print("E_11 vs E_nn ratio (paper's example), n=10:",
      paper_E(np.diag([0] * 9 + [1.0])) / paper_E(np.diag([1.0] + [0] * 9)))

print("\n== Example 4.2 checkerboard ==")
print(" n   E(checker)   E(J)   E/n^3   E/n^4  (paper's normalisation)")
for n in [8, 16, 32, 64, 128]:
    i = np.arange(1, n + 1)
    C = (-1.0) ** (i[:, None] + i[None, :])
    J = np.ones((n, n))
    ec, ej = paper_E(C), paper_E(J)
    print(f"{n:4d} {ec:12.1f} {ej:12.1f} {ec / n**3:8.3f} {ec / n**4:8.4f}")
    fail += not np.isclose(ec, ej)
print("closed form 2n * n(n+1)(2n+1)/6 at n=128:", 2 * 128 * 128 * 129 * 257 / 6)
print("checkerboard and all-ones J have identical energy -> 'maximally rough' claim fails;"
      " growth is n^4 (paper normalisation) or n^2 (true normalisation), never n^3")

print("\n== Thm 5.4: lambda = 0 makes the 'uniform' sup bound fail (H^1 not in L^inf in 2D) ==")
for N in [8, 32, 128, 512]:
    k = np.arange(1, N + 1)
    K2 = k[:, None] ** 2 + k[None, :] ** 2
    a = N / K2                     # coefficients c_k = a/N = 1/|k|^2
    c = a / N
    sup = c.sum()                  # attained at x = 0
    grad2 = (2 * np.pi) ** 2 * np.sum(K2 * c ** 2)
    lap2 = (2 * np.pi) ** 2 * np.sum(K2 ** 2 * c ** 2)
    print(f"N={N:4d}  sup|f|/||grad f|| = {sup / np.sqrt(grad2):.4f}   sup|f|/||Lap f|| = {sup / np.sqrt(lap2):.4f}")
print("(first ratio grows like sqrt(log N): no uniform C when lambda=0; second stays bounded)")
# softmax rows: entries in [0,1] summing to 1 per row -> |f| <= (1/N) sum |a| = 1 trivially
N = 64
Q = rng.standard_normal((N, 8)); Kk = rng.standard_normal((N, 8))
S = Q @ Kk.T / np.sqrt(8); S = np.exp(S - S.max(1, keepdims=True)); S /= S.sum(1, keepdims=True)
f, _ = sample(S, 256)
print("softmax slice N=64: sup|f| on grid =", abs(f).max(), "<= 1 (trivial bound)")
fail += abs(f).max() > 1 + 1e-12

print("\nfailures:", fail)
sys.exit(int(fail))
