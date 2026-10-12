"""L2 check of fix A1 (chap01, proof of thm:grothendieck_cutnorm and thm:hypergraphon_compactness (i)).

Claim (new step): for W in L^1 and 0 <= u, v <= 1, with g(x) = int W(x,y) v(y) dy,
  |int W u v| <= |int 1_S g| for S = {g>0} OR S = {g<0}  (the better of the two),
and iterating in v: |int W u v| <= cut norm.  k-linear: same with 2^k orthants.
Oracle: step kernels on an n x n grid; cut norm by brute force over all 2^n x 2^n
index sets; box supremum approached by random sampling plus projected gradient ascent
(never uses indicators).
Negative controls:
  (c1) mutated step "S = {g>0} always" must fail on some instance;
  (c2) box [-1,1] instead of [0,1]: sup/cut > 1 must occur (decomposition needed).
"""
import itertools
import sys
import numpy as np

rng = np.random.default_rng(20261010)
n = 6
fails = 0


def cut_norm(W):
    best = 0.0
    sets = [np.array(s, float) for s in itertools.product([0, 1], repeat=W.shape[0])]
    S = np.array(sets)
    M = S @ W @ S.T / W.shape[0] ** 2
    return float(np.abs(M).max())


def box_sup(W, lo, iters=300, starts=40):
    m = W.shape[0]
    best = 0.0
    for _ in range(starts):
        u = rng.uniform(lo, 1, m)
        v = rng.uniform(lo, 1, m)
        sgn = rng.choice([-1, 1])
        for _ in range(iters):
            u = np.clip(u + 0.5 * sgn * (W @ v) / m, lo, 1)
            v = np.clip(v + 0.5 * sgn * (W.T @ u) / m, lo, 1)
        best = max(best, abs(u @ W @ v) / m ** 2)
    return best


worst_ratio_01 = 0.0
worst_ratio_pm = 0.0
mutant_fail = False
step_ok = True
for trial in range(8):
    W = rng.normal(size=(n, n))
    W = (W + W.T) / 2
    c = cut_norm(W)
    s01 = box_sup(W, 0.0)
    spm = box_sup(W, -1.0)
    worst_ratio_01 = max(worst_ratio_01, s01 / c)
    worst_ratio_pm = max(worst_ratio_pm, spm / c)
    # the literal step of the proof on random (u, v)
    for _ in range(200):
        u = rng.uniform(0, 1, n)
        v = rng.uniform(0, 1, n)
        g = W @ v / n
        lhs = abs(u @ g) / n
        r_pos = abs(g[g > 0].sum()) / n
        r_neg = abs(g[g < 0].sum()) / n
        if lhs > max(r_pos, r_neg) + 1e-12:
            step_ok = False
        if lhs > r_pos + 1e-12:
            mutant_fail = True
    if spm > 4 * c + 1e-9:
        step_ok = False

print(f"box[0,1] sup / cut  max over trials = {worst_ratio_01:.6f}  (claim <= 1)")
ok1 = worst_ratio_01 <= 1 + 1e-9 and step_ok
print("PASS" if ok1 else "FAIL", "A1 bilinear step and constant 4")
fails += not ok1
print(f"control c2: box[-1,1] sup / cut max = {worst_ratio_pm:.4f}  (must exceed 1)")
okc2 = worst_ratio_pm > 1.01
print("PASS (control fails as required)" if okc2 else "FAIL (control has no power)")
fails += not okc2
print("PASS (control c1 'S={g>0} only' fails)" if mutant_fail else "FAIL (control c1 passed)")
fails += not mutant_fail

# trilinear k = 3, n = 4, constant 2^3, and box[0,1] sup equals indicator max
n3 = 4
W3 = rng.normal(size=(n3, n3, n3))
sets = [np.array(s, float) for s in itertools.product([0, 1], repeat=n3)]
cut3 = max(abs(np.einsum('ijk,i,j,k->', W3, a, b, c)) for a in sets for b in sets for c in sets) / n3 ** 3
best01 = 0.0
bestpm = 0.0
for lo in (0.0, -1.0):
    for _ in range(3000):
        a, b, c = (rng.uniform(lo, 1, n3) for _ in range(3))
        val = abs(np.einsum('ijk,i,j,k->', W3, a, b, c)) / n3 ** 3
        if lo == 0.0:
            best01 = max(best01, val)
        else:
            bestpm = max(bestpm, val)
ok3 = best01 <= cut3 + 1e-12 and bestpm <= 8 * cut3 + 1e-12
print(f"k=3: sup01/cut = {best01/cut3:.4f}, sup[-1,1]/cut = {bestpm/cut3:.4f} (<= 8)")
print("PASS" if ok3 else "FAIL", "A1 trilinear")
fails += not ok3
sys.exit(1 if fails else 0)
