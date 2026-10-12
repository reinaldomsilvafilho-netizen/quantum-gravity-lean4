"""
F-02 independent numerical audit -- Chapter 10
(chap10_information_geometry_minimax_deep_learning.tex)

Every claim: independent oracle + negative control (mutated formula that
must fail). Read-only; does not edit the chapter. This chapter is pure
statistics/ML (no physical dimensionful quantities), so no CODATA check
applies here.
"""
import numpy as np
import mpmath as mp
from scipy.optimize import minimize_scalar, minimize

rng = np.random.default_rng(123)
mp.mp.dps = 40
PASS, FAIL = [], []


def report(name, line, ok, detail):
    (PASS if ok else FAIL).append(name)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} (book line ~{line})")
    print(f"       {detail}")


# ---------------------------------------------------------------------------
# Claim 1 (line 121, Proposition "Counterexample"): the PAC-Bayes-type bound
# at kappa*_info=0 reduces to sqrt(ln(2/delta)/(2N)), which equals 0.19 for
# N=50, delta=0.05, and is below 1/2 for all N>=8 at delta=0.05 (threshold
# N > 2 ln(40) ~ 7.4).
# Oracle: direct high-precision arithmetic evaluation (mpmath), independent
# of the chapter's own derivation.
# Negative control: the mutated formula sqrt(ln(1/delta)/(2N)) (dropping the
# factor 2 inside the log) must give a different numerical value at N=50.
# ---------------------------------------------------------------------------
def bound_at_zero(N, delta):
    return float(mp.sqrt(mp.log(2 / delta) / (2 * N)))


val_50 = bound_at_zero(50, 0.05)
val_N7 = bound_at_zero(7, 0.05)
val_N8 = bound_at_zero(8, 0.05)
threshold = float(2 * mp.log(40))

ok1 = (abs(val_50 - 0.19) < 0.005) and (val_N7 >= 0.5) and (val_N8 < 0.5) and (7 < threshold < 8)
report("PAC-Bayes bound at kappa*=0: sqrt(ln(2/delta)/2N) = 0.19 at N=50,delta=0.05; below 1/2 for all N>=8",
       "121,127", ok1,
       f"value at N=50: {val_50:.6f} (book: 0.19); value at N=7: {val_N7:.6f} (>=0.5); "
       f"value at N=8: {val_N8:.6f} (<0.5); exact threshold N* = 2ln(40) = {threshold:.4f}")

val_wrong = bound_at_zero.__wrapped__ if False else float(mp.sqrt(mp.log(1 / 0.05) / (2 * 50)))
ok1_neg = abs(val_wrong - 0.19) > 0.01
report("NEGATIVE CONTROL: mutated formula sqrt(ln(1/delta)/2N) (missing the factor 2 in the log) disagrees with 0.19",
       "121,127", ok1_neg, f"mutated value at N=50: {val_wrong:.6f} vs book's 0.19 (correct value {val_50:.6f})")


# ---------------------------------------------------------------------------
# Claim 2 (lines 121,127, proof of Proposition "Counterexample" item 2): the
# generalization gap of a random-label $\pm1$ regression is >= 1/2 for
# EVERY distribution of the inputs, because for every real f,
#   (1/2)[min((1-f)^2,1) + min((1+f)^2,1)] >= 1/2, with equality at f=+-1.
# Oracle: independent numerical global minimization (scipy.optimize) over f,
# rather than the book's case-split algebraic argument.
# Negative control: the mutated functional WITHOUT the [0,1] clipping,
# (1/2)[(1-f)^2+(1+f)^2] = 1+f^2, has a different minimum (1, at f=0, not
# 1/2 at f=+-1) -- clipping is essential to the 1/2 bound.
# ---------------------------------------------------------------------------
def g_clipped(f):
    return 0.5 * (min((1 - f) ** 2, 1) + min((1 + f) ** 2, 1))


fs = np.linspace(-4, 4, 20001)
vals = [g_clipped(f) for f in fs]
g_min = min(vals)
f_argmin = fs[int(np.argmin(vals))]

ok2 = abs(g_min - 0.5) < 1e-3 and abs(abs(f_argmin) - 1) < 0.01
report("Clipped expected test loss >= 1/2, with equality at f=+-1 (independent dense-grid global minimization)",
       "121,127", ok2, f"grid-search min = {g_min:.6f} (book: 1/2) attained at f = {f_argmin:.4f} (book: +-1)")


def g_unclipped(f):
    return 0.5 * ((1 - f) ** 2 + (1 + f) ** 2)


vals_u = [g_unclipped(f) for f in fs]
g_min_u = min(vals_u)
ok2_neg = abs(g_min_u - 1.0) < 1e-6 and abs(g_min_u - 0.5) > 0.1
report("NEGATIVE CONTROL: without the [0,1] clipping the minimum is 1 (at f=0), not 1/2 -- clipping is essential",
       "121,127", ok2_neg, f"unclipped grid-search min = {g_min_u:.6f} (expected 1.0, not 0.5)")


# ---------------------------------------------------------------------------
# Claim 3 (lines 66, 121, 127, Proposition "Counterexample"): full Monte
# Carlo REPRODUCTION of the headline numbers. Gaussian linear regression
# with D > N, random +-1 labels, minimum-norm interpolant theta* = X^+ y:
# (a) Tr(X^T X / N) > 0 (trivial but checked); (b) the OUT-OF-SAMPLE
# generalization gap (clipped squared loss on a fresh random-label test
# point) is close to the book's stated ~0.70 for N=50, D=200, Gaussian
# inputs; (c) with a genuine linear teacher and N >> D the gap is close to 0.
# Oracle: direct Monte Carlo simulation (least-squares pseudo-inverse via
# numpy.linalg.lstsq, independent random data) -- a full, independent
# reproduction of the numerical experiment described in the chapter, not a
# symbolic re-derivation.
# Negative control: a trivial predictor f=0 (c.f. theta=0, ignoring the
# training data) must give a generalization gap close to 1 (since y=+-1
# always gives squared loss 1), clearly different from theta*'s ~0.70.
# ---------------------------------------------------------------------------
def run_random_label_trial(N, D, n_test, rng):
    X = rng.standard_normal((N, D))
    y = rng.choice([-1.0, 1.0], size=N)
    theta_star, *_ = np.linalg.lstsq(X, y, rcond=None)
    Xtest = rng.standard_normal((n_test, D))
    ytest = rng.choice([-1.0, 1.0], size=n_test)
    preds = Xtest @ theta_star
    loss = np.minimum((ytest - preds) ** 2, 1.0)
    return loss.mean(), X, y, theta_star


N3, D3, n_test3, n_trials = 50, 200, 2000, 60
gaps = []
trH_vals = []
for _ in range(n_trials):
    gap, X, y, theta_star = run_random_label_trial(N3, D3, n_test3, rng)
    gaps.append(gap)
    trH_vals.append(np.trace(X.T @ X / N3))

mean_gap = np.mean(gaps)
se_gap = np.std(gaps) / np.sqrt(n_trials)
mean_trH = np.mean(trH_vals)

ok3a = mean_trH > 0

# near-zero case: genuine linear teacher, N >> D, small noise
N3b, D3b, n_test3b = 4000, 10, 4000
theta_true = rng.standard_normal(D3b)
Xb = rng.standard_normal((N3b, D3b))
yb = Xb @ theta_true + 0.01 * rng.standard_normal(N3b)
theta_hat_b, *_ = np.linalg.lstsq(Xb, yb, rcond=None)
Xtest_b = rng.standard_normal((n_test3b, D3b))
ytest_b = Xtest_b @ theta_true + 0.01 * rng.standard_normal(n_test3b)
loss_b = np.minimum((ytest_b - Xtest_b @ theta_hat_b) ** 2, 1.0)
gap_b = loss_b.mean()

ok3 = ok3a and abs(mean_gap - 0.70) < 0.06 and gap_b < 0.05
report("Monte Carlo reproduction: Tr(X^TX/N)>0; random-label gap ~0.70 at N=50,D=200; linear-teacher gap ~0 at N>>D",
       "66,121,127", ok3,
       f"mean Tr(H)={mean_trH:.3f} (>0); random-label gap over {n_trials} trials = {mean_gap:.4f} +- {se_gap:.4f} (book: ~0.70); "
       f"linear-teacher (N={N3b}>>D={D3b}) gap = {gap_b:.5f} (book: close to 0)")

f0_loss = np.minimum((np.array([-1.0, 1.0])) ** 2, 1.0)
ok3_neg = abs(f0_loss.mean() - 1.0) < 1e-9 and abs(f0_loss.mean() - mean_gap) > 0.2
report("NEGATIVE CONTROL: trivial predictor f=0 gives generalization gap = 1 (clearly different from theta*'s ~0.70)",
       "66,121,127", ok3_neg, f"f=0 gap = {f0_loss.mean():.4f} vs theta* Monte Carlo gap = {mean_gap:.4f}")


# ---------------------------------------------------------------------------
# Claim 4 (lines 144, Remark "On the formulation"): for d=l=2, a reflection
# teacher f(x) = W2 tanh(W1 x) with W1 a reflection (det=-1) and W2=I,
# fit by Q2 tanh(Q1 x) with Q1,Q2 constrained to SO(2) (det=+1), 40 inputs
# ~ N(0, 2.25 I_2): the minimum mean-squared loss over SO(2)^2 lies in
# [1.3, 2.1] for such samples.
# Oracle: independent grid+local optimization over the 2 rotation angles
# (an exhaustive 2D search, unrelated to the book's own numerical run) on
# freshly drawn samples.
# Negative control: searching over the FULL O(2)^2 (allowing reflections,
# i.e. the teacher's own component) must reach ~0, very different from the
# [1.3,2.1] range found when restricted to SO(2)^2.
# ---------------------------------------------------------------------------
def rot(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])


def refl():
    return np.array([[1.0, 0.0], [0.0, -1.0]])


def mse_loss(angles, X, Y, allow_reflection_Q1=False):
    th1, th2 = angles
    Q1 = rot(th1) @ refl() if allow_reflection_Q1 else rot(th1)
    Q2 = rot(th2)
    pred = (Q2 @ np.tanh(Q1 @ X.T)).T
    return np.mean(np.sum((pred - Y) ** 2, axis=1))


n_in = 40
X_in = rng.normal(0, 1.5, size=(n_in, 2))  # N(0, 2.25 I_2) => std = 1.5
W1_teacher, W2_teacher = refl(), np.eye(2)
Y_teacher = (W2_teacher @ np.tanh(W1_teacher @ X_in.T)).T

best_SO2 = np.inf
for th1_0 in np.linspace(0, 2 * np.pi, 12, endpoint=False):
    for th2_0 in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        res = minimize(mse_loss, [th1_0, th2_0], args=(X_in, Y_teacher, False), method='Nelder-Mead')
        if res.fun < best_SO2:
            best_SO2 = res.fun

ok4 = 1.3 <= best_SO2 <= 2.1
report("Reflection-teacher loss minimized over SO(2)^2 lies in [1.3,2.1] (independent 2D grid+local search, 40 fresh samples)",
       "144", ok4, f"minimum MSE over SO(2)^2 found = {best_SO2:.4f} (book's stated range: [1.3, 2.1])")

best_O2 = np.inf
for th1_0 in np.linspace(0, 2 * np.pi, 12, endpoint=False):
    for th2_0 in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        res = minimize(mse_loss, [th1_0, th2_0], args=(X_in, Y_teacher, True), method='Nelder-Mead')
        if res.fun < best_O2:
            best_O2 = res.fun

ok4_neg = best_O2 < 0.05 and (best_SO2 - best_O2) > 1.0
report("NEGATIVE CONTROL: allowing the teacher's own reflection component (full O(2)^2) reaches ~0, unlike SO(2)^2's [1.3,2.1]",
       "144", ok4_neg, f"minimum MSE over full O(2)^2 = {best_O2:.5f} (should be ~0, far below SO(2)^2's {best_SO2:.4f})")


print()
print("=" * 70)
print(f"Chapter 10 summary: {len(PASS)} PASS, {len(FAIL)} FAIL")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("  -", f)
