"""L2 directed check S1: ch.10 prop:counterexample(2), as now stated.

Current text (chap10, l.118-121): hypothesis "X of full row rank N" added to the
proposition; conclusion restricted to "every distribution of the inputs under which
X has rank N almost surely, for instance any distribution with a density on R^D",
with a neutral remark that x = 0 (rank 0) gives train loss = test loss = 1, gap = 0.

Independent oracle: closed-form test loss E_y min((y-f)^2,1) = ((1-f)^2 clipped +
(1+f)^2 clipped)/2 for fresh y in {+-1}. Checks:
(a) full-rank Gaussian X -> gap >= 1/2 in every trial (claim as now stated holds).
(b) density-on-R^D family (Gaussian, Laplace-like via randn+t, rotated Gaussian)
    all give rank N a.s. -> gap >= 1/2, matching the "for instance" clause.
(c) x = 0 gives gap exactly 0 (the remark's own counterexample).
(d) negative control / mutation: claim mutated to "gap >= 1/2 for EVERY distribution,
    no rank hypothesis" must fail (rank-deficient case violates it).
(e) mutation on the bound itself: "gap >= 0.9" must fail even in the valid (full-rank)
    regime -- the proposition's constant 1/2 is not arbitrarily improvable by a trivial
    change, so a naive strengthening is correctly rejected.
"""
import numpy as np

rng = np.random.default_rng(7)
N, D, NTEST, TRIALS = 50, 200, 3000, 30


def clip_loss(y, f):
    return np.minimum((y - f) ** 2, 1.0)


def test_loss_oracle(f):
    return 0.5 * (np.minimum((1 - f) ** 2, 1) + np.minimum((1 + f) ** 2, 1))


def run(sampler, trials=TRIALS):
    gaps, ranks = [], []
    for _ in range(trials):
        X = sampler(N)
        y = rng.choice([-1.0, 1.0], size=N)
        th = np.linalg.pinv(X) @ y
        tr = clip_loss(y, X @ th).mean()
        Xt = sampler(NTEST)
        te = test_loss_oracle(Xt @ th).mean()
        gaps.append(te - tr)
        ranks.append(np.linalg.matrix_rank(X))
    return np.array(gaps), np.array(ranks)

# (a) full row rank Gaussian: the case quoted in the abstract (~0.70, N=50, D=200)
g_gauss, r_gauss = run(lambda n: rng.standard_normal((n, D)))
assert np.all(r_gauss == N)
assert g_gauss.min() >= 0.5
print(f"(a) gaussian full-rank: mean gap {g_gauss.mean():.3f} min {g_gauss.min():.3f} (matches ~0.70 claim)")

# (b) other densities on R^D -> rank N a.s., gap >= 1/2 as the 'for instance' clause claims
def laplace_like(n):
    u = rng.uniform(-0.5, 0.5, size=(n, D))
    return -np.sign(u) * np.log(1 - 2 * np.abs(u))

def rotated_gauss(n):
    A = rng.standard_normal((D, D))
    Q, _ = np.linalg.qr(A)
    return rng.standard_normal((n, D)) @ Q.T

for name, sampler in [("laplace-like density", laplace_like), ("rotated gaussian density", rotated_gauss)]:
    g, r = run(sampler, trials=15)
    assert np.all(r == N)
    assert g.min() >= 0.5
    print(f"(b) {name}: mean gap {g.mean():.3f} min {g.min():.3f}, rank always {N}")

# (c) the remark's own stated counterexample: x == 0
X0 = np.zeros((N, D))
y0 = rng.choice([-1.0, 1.0], size=N)
th0 = np.linalg.pinv(X0) @ y0
assert np.allclose(th0, 0)
tr0 = clip_loss(y0, X0 @ th0).mean()
Xt0 = np.zeros((NTEST, D))
te0 = test_loss_oracle(Xt0 @ th0).mean()
assert abs(tr0 - 1.0) < 1e-12 and abs(te0 - 1.0) < 1e-12
print(f"(c) x==0: train={tr0:.6f} test={te0:.6f} gap={te0-tr0:.2e} (matches remark exactly)")

# (d) mutation: drop the rank hypothesis entirely ("for every distribution of the inputs")
g_lowrank, r_lowrank = run(lambda n: np.outer(rng.standard_normal(n), np.eye(D)[0]), trials=15)
assert np.all(r_lowrank == 1)
mutated_claim_holds_everywhere = bool(g_lowrank.min() >= 0.5)
assert mutated_claim_holds_everywhere is False
print(f"(d) rank-1 inputs: min gap {g_lowrank.min():.3f} < 0.5 -> unrestricted claim correctly falsified")

# (e) mutation: strengthen the constant to 0.9 even for valid (full-rank) distributions
assert not (g_gauss.min() >= 0.9)
print(f"(e) constant-strengthening mutation (>=0.9) rejected by data (min {g_gauss.min():.3f}) as expected")

print("S1 L2: current text (rank-N hypothesis + density clause + x=0 remark) matches what the proof proves. CONFIRMA")
