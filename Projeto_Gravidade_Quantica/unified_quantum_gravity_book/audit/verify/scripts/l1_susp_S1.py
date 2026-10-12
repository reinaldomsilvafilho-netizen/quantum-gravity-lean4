"""L1 blind check S1: ch.10 prop:counterexample part (2), 'gap >= 1/2 for every input distribution'.

Model: y_i uniform in {+-1} independent of x_i; theta* = pinv(X) y; clipped squared loss min((y-f)^2,1).
Oracle (independent of pinv): for x == 0 every prediction is 0, so train loss = test loss = 1, gap = 0 exactly.
Test-loss oracle: E_y min((y-f)^2,1) = (min((1-f)^2,1)+min((1+f)^2,1))/2, closed form.
Negative control: full-row-rank Gaussian X must give gap >= 1/2 (the claim's valid regime); a mutated claim
'gap >= 1/2 also for rank-deficient X' must fail.
"""
import numpy as np

rng = np.random.default_rng(20261010)
N, D, NTEST, TRIALS = 50, 200, 4000, 40


def clip_loss(y, f):
    return np.minimum((y - f) ** 2, 1.0)


def gap(sampler):
    gaps, ranks = [], []
    for _ in range(TRIALS):
        X = sampler(N)
        y = rng.choice([-1.0, 1.0], size=N)
        th = np.linalg.pinv(X) @ y
        tr = clip_loss(y, X @ th).mean()
        Xt = sampler(NTEST)
        ft = Xt @ th
        # exact expectation over the fresh label (closed-form oracle)
        te = (0.5 * (np.minimum((1 - ft) ** 2, 1) + np.minimum((1 + ft) ** 2, 1))).mean()
        gaps.append(te - tr)
        ranks.append(np.linalg.matrix_rank(X))
    return np.mean(gaps), np.min(gaps), int(np.min(ranks))


cases = {
    "gaussian (full row rank)": lambda n: rng.standard_normal((n, D)),
    "x == 0": lambda n: np.zeros((n, D)),
    "x on a line: z*e1": lambda n: np.outer(rng.standard_normal(n), np.eye(D)[0]),
    "x in a 10-dim subspace": lambda n: np.hstack([rng.standard_normal((n, 10)), np.zeros((n, D - 10))]),
}
res = {}
for name, s in cases.items():
    res[name] = gap(s)
    print(f"{name:28s} mean gap {res[name][0]:.4f}  min gap {res[name][1]:.4f}  min rank {res[name][2]}")

# oracle for x == 0: gap exactly 0
assert abs(res["x == 0"][0]) < 1e-12 and abs(res["x == 0"][1]) < 1e-12
# valid regime: full row rank -> gap >= 1/2 in every trial
assert res["gaussian (full row rank)"][2] == N and res["gaussian (full row rank)"][1] >= 0.5
# the claim 'for every distribution' fails on rank-deficient inputs
assert res["x on a line: z*e1"][1] < 0.5 and res["x in a 10-dim subspace"][1] < 0.5
# negative control: mutated claim 'gap >= 1/2 for all four distributions' must be False
mutated = all(r[1] >= 0.5 for r in res.values())
assert mutated is False
print("S1: claim fails for rank-deficient inputs; holds whenever rank X = N. PASS")
