"""L1 blind check A1 (ch. 1, thm:grothendieck_cutnorm, thm:hypergraphon_compactness (i)).

Claim needed by the proof: for 0 <= u, v <= 1 (box, not indicators),
    |<W u, v>| <= ||W||_cut,
i.e. the sup of the bilinear (k-linear) form over the box [0,1]^n is attained at
0/1 vectors (indicators).  Step kernels on an n x n grid, cell weight 1/n^2.

Oracle: cut norm by brute force over all subset pairs (indicators).
Independent check: box sup by multistart L-BFGS-B (never uses indicators).
Negative control: on the box [-1,1]^n the sup EXCEEDS the cut norm, so the
indicator step is not vacuous; and the mutated bound ||T|| <= 1*cut fails.
"""
import itertools
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(1)


def cut_norm_bruteforce(W):
    n = W.shape[0]
    best = 0.0
    vecs = [np.array(s, float) for s in itertools.product([0, 1], repeat=n)]
    for a in vecs:
        r = a @ W
        for b in vecs:
            best = max(best, abs(r @ b))
    return best / n**2


def box_sup(W, lo, hi, starts=60):
    n = W.shape[0]
    best = 0.0
    for sgn in (1, -1):
        f = lambda z: -sgn * (z[:n] @ W @ z[n:]) / n**2
        g = lambda z: -sgn * np.concatenate([W @ z[n:], W.T @ z[:n]]) / n**2
        for _ in range(starts):
            z0 = rng.uniform(lo, hi, 2 * n)
            res = minimize(f, z0, jac=g, method="L-BFGS-B", bounds=[(lo, hi)] * (2 * n))
            best = max(best, -res.fun)
    return best


worst_gap = 0.0
neg_ratio = []
for trial in range(8):
    n = 6
    W = rng.normal(size=(n, n))
    W = (W + W.T) / 2
    c = cut_norm_bruteforce(W)
    b01 = box_sup(W, 0.0, 1.0)
    bpm = box_sup(W, -1.0, 1.0)
    worst_gap = max(worst_gap, b01 - c)
    neg_ratio.append(bpm / c)
    assert b01 <= c + 1e-9, (b01, c)
    assert bpm <= 4 * c + 1e-9
print("A1 bilinear: max(box[0,1] sup - cut) =", worst_gap, "(<=0 up to 1e-9 => extreme-point step true)")
print("A1 negative control: sup over [-1,1] / cut ratios:", np.round(neg_ratio, 3))
assert max(neg_ratio) > 1.05, "negative control failed to separate"
print("A1 negative control: mutated bound ||T||<=1*cut FAILS as expected")

# trilinear (k = 3) analogue for thm:hypergraphon_compactness (i)
n = 4
T = rng.normal(size=(n, n, n))
vecs = [np.array(s, float) for s in itertools.product([0, 1], repeat=n)]
cut3 = max(abs(np.einsum("ijk,i,j,k->", T, a, b, d)) for a in vecs for b in vecs for d in vecs) / n**3
best = 0.0
for _ in range(400):
    z = rng.uniform(0, 1, 3 * n)
    # coordinate ascent: each step is linear in one factor -> optimum at 0/1 with continuous start
    for it in range(30):
        a, b, d = z[:n], z[n:2 * n], z[2 * n:]
        val = np.einsum("ijk,i,j,k->", T, a, b, d)
        s = 1 if val >= 0 else -1
        a = (s * np.einsum("ijk,j,k->i", T, b, d) > 0).astype(float) * 0.5 + 0.5 * a  # damped, stays in box
        z = np.concatenate([a, b, d])
    best = max(best, abs(np.einsum("ijk,i,j,k->", T, z[:n], z[n:2 * n], z[2 * n:])) / n**3)
rand_best = max(abs(np.einsum("ijk,i,j,k->", T, *(rng.uniform(0, 1, (3, n))))) / n**3 for _ in range(20000))
print("A1 trilinear: cut3 =", round(cut3, 6), " box sup (search) =", round(max(best, rand_best), 6))
assert max(best, rand_best) <= cut3 + 1e-12
print("A1 PASS: the step holds; it is a true but unstated step of the proof.")
