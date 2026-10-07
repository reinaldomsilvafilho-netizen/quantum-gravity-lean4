"""L2b: is each subsection of §4 'order-sensitive' (heading), and does the §6.5 display match Thm 4.6?

Order-sensitive := changes under A -> P A P^T for some permutation P.
Oracles: brute-force cut norm over unions of cells; eigen-decomposition; direct cell-boundary perimeter.
Negative controls included. Fixed seed. Exit code = failures.
"""
import sys, itertools
import numpy as np

rng = np.random.default_rng(7)
fails, out = 0, []


def report(name, ok, info=""):
    global fails
    fails += (not ok)
    s = f"[{'PASS' if ok else 'FAIL'}] {name}: {info}"
    out.append(s); print(s)


n = 4
A = rng.integers(0, 4, size=(n, n)).astype(float); A = (A + A.T) / 2
perm = np.array([2, 0, 3, 1]); P = np.eye(n)[perm]
B = P @ A @ P.T

# 4.1 Dirichlet energy (Thm 4.1 formula) -- order sensitive
D = np.diag(np.arange(1, n + 1))
E = lambda M: np.linalg.norm(D @ M) ** 2 + np.linalg.norm(M @ D) ** 2
report("4.1 Dirichlet energy changes under P", abs(E(A) - E(B)) > 1e-9, f"{E(A):.2f} vs {E(B):.2f}")


# 4.2 TV of step realization (eq. 4.14) -- order sensitive
def TV(M):
    m = len(M)
    return (np.abs(np.diff(M, axis=0)).sum() + np.abs(np.diff(M, axis=1)).sum()) / m


report("4.2 TV changes under P", abs(TV(A) - TV(B)) > 1e-9, f"{TV(A):.3f} vs {TV(B):.3f}")

# 4.3 Morse indices of x^T A x: index of eigenvector with k-th smallest eigenvalue = k-1 -> spectral only
def morse_data(M):
    w, V = np.linalg.eigh(M)
    idx = []
    for i in range(len(w)):
        v = V[:, i]
        Pt = np.eye(len(w)) - np.outer(v, v)
        H = 2 * Pt @ (M - w[i] * np.eye(len(w))) @ Pt
        ev = np.linalg.eigvalsh(H)
        idx.append(int((ev < -1e-9).sum()))
    return sorted(np.round(w, 10)), sorted(idx)


Ag = rng.normal(size=(n, n)); Ag = Ag + Ag.T; Bg = P @ Ag @ P.T
report("4.3 Morse indices and critical values identical under P (not order-sensitive)",
       morse_data(Ag) == morse_data(Bg), str(morse_data(Ag)[1]))
Cg = Ag + np.diag([0, 0, 0, 5.0])
report("4.3 control: a non-similar matrix changes critical values", morse_data(Ag)[0] != morse_data(Cg)[0], "")


# 4.4 cut distance: exact cut norm of step kernels by brute force over unions of cells
def cutnorm_step(M):
    m = len(M); best = 0
    for S in itertools.product([0, 1], repeat=m):
        r = np.array(S) @ M
        best = max(best, r[r > 0].sum(), -r[r < 0].sum())
    return best / m**2


cA, cB = A / 4, B / 4                      # graphons in [0,1]
dirct = cutnorm_step(cA - cB)
# psi = measure-preserving permutation of the n intervals: (W_B)^psi = W_A
Bpsi = cB[np.ix_(np.argsort(perm), np.argsort(perm))]
report("4.4 W_B^psi = W_A for the interval permutation psi", np.abs(Bpsi - cA).max() == 0, "")
report("4.4 hence delta_cut(W_A, W_B) = 0 (not order-sensitive)", cutnorm_step(cA - Bpsi) == 0, "")
report("4.4 control: plain cut norm ||W_A - W_B|| > 0", dirct > 1e-9, f"{dirct:.4f}")


# §6.5 display vs Thm 4.6: perimeter inside (0,1)^2 vs perimeter in R^2
def perim(M, t, include_outer):
    m = len(M); E_ = (M > t).astype(int); L = 0
    L += np.abs(np.diff(E_, axis=0)).sum() + np.abs(np.diff(E_, axis=1)).sum()
    if include_outer:
        L += E_[0, :].sum() + E_[-1, :].sum() + E_[:, 0].sum() + E_[:, -1].sum()
    return L / m


vals = np.unique(A); grid = np.concatenate([[vals.min() - 1], vals])
def coarea(include_outer):
    tot = 0
    for lo, hi in zip(grid[:-1], grid[1:]):
        tot += perim(A, (lo + hi) / 2, include_outer) * (hi - lo)
    return tot


report("6.5 Thm 4.6 reading (inside (0,1)^2) = TV formula", abs(coarea(False) - TV(A)) < 1e-12,
       f"{coarea(False):.4f} vs {TV(A):.4f}")
report("6.5 literal R^2 reading of the display (no intersection with (0,1)^2) differs from TV; for t below min A it adds 4 per unit t, so the integral over R diverges", abs(coarea(True) - TV(A)) > 1e-6,
       f"{coarea(True):.4f} vs {TV(A):.4f}")

open(__file__.replace(".py", ".out.txt"), "w", encoding="utf8").write("\n".join(out) + f"\nfailures: {fails}\n")
sys.exit(fails)
