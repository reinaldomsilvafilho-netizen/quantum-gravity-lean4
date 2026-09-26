"""L2 residual check (2026-09-25), chapter 10, Conjecture 3.1 and its remark.

(A) Reflection teacher, d = l = 2, f(x) = W2 tanh(W1 x), 40 inputs N(0, 2.25 I):
    minimum loss per connected component of O(2)^2 (own parametrization by
    angles, dense grid + local polish, not the corrector's L-BFGS multistart).
    Claims: components with prod det = -1 reach 0; SO(2)^2 and (-,-) have
    equal minima, between 1.3 and 2.1.
(B) Sign-flip symmetry preserves prod det, and maps (+,+) to (-,-).
(C) New: the component hypothesis is still not sufficient for the conclusion
    "the trajectory reaches Sigma*" from an arbitrary theta_0: the loss
    maximizer on the component is a fixed point of Riemannian GD.
Run from the book folder.
"""
import numpy as np
from scipy.optimize import minimize

FAILS = []


def check(name, cond):
    print(("OK   " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def rot(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[c, -s], [s, c]])


def refl(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[c, s], [s, -c]])


MAKE = {+1: rot, -1: refl}


def loss(W1, W2, X, Y):
    return np.mean(np.sum((np.tanh(X @ W1.T) @ W2.T - Y) ** 2, axis=1))


def comp_min(s1, s2, X, Y, n=121):
    ts = np.linspace(0, 2 * np.pi, n, endpoint=False)
    best = (np.inf, None)
    for a in ts:
        W1 = MAKE[s1](a)
        H = np.tanh(X @ W1.T)
        for b in ts:
            v = np.mean(np.sum((H @ MAKE[s2](b).T - Y) ** 2, axis=1))
            if v < best[0]:
                best = (v, (a, b))
    f = lambda p: loss(MAKE[s1](p[0]), MAKE[s2](p[1]), X, Y)
    r = minimize(f, best[1], method="Nelder-Mead", options=dict(xatol=1e-10, fatol=1e-14, maxiter=4000))
    return r.fun


def comp_max(s1, s2, X, Y, n=121):
    ts = np.linspace(0, 2 * np.pi, n, endpoint=False)
    best = (-np.inf, None)
    for a in ts:
        for b in ts:
            v = loss(MAKE[s1](a), MAKE[s2](b), X, Y)
            if v > best[0]:
                best = (v, (a, b))
    f = lambda p: -loss(MAKE[s1](p[0]), MAKE[s2](p[1]), X, Y)
    r = minimize(f, best[1], method="Nelder-Mead", options=dict(xatol=1e-12, fatol=1e-15, maxiter=4000))
    return -r.fun, r.x


mins_pp = []
for seed in range(6):
    rng = np.random.default_rng(1000 + seed)
    X = rng.normal(0, 1.5, size=(40, 2))
    W1t, W2t = refl(0.7), np.eye(2)
    Y = np.tanh(X @ W1t.T) @ W2t.T
    m = {(s1, s2): comp_min(s1, s2, X, Y) for s1 in (1, -1) for s2 in (1, -1)}
    print("     seed %d: (+,+) %.4f  (-,-) %.4f  (-,+) %.2e  (+,-) %.2e" % (seed, m[(1, 1)], m[(-1, -1)], m[(-1, 1)], m[(1, -1)]))
    check("ch10 seed %d: prod det=-1 components reach 0" % seed, m[(-1, 1)] < 1e-8 and m[(1, -1)] < 1e-8)
    check("ch10 seed %d: min over SO(2)^2 equals min over (-,-)" % seed, abs(m[(1, 1)] - m[(-1, -1)]) < 1e-6)
    mins_pp.append(m[(1, 1)])
print("     SO(2)^2 minima:", np.round(mins_pp, 3))
check("ch10 SO(2)^2 minima all in [1.3, 2.1] (text: 'between 1.3 and 2.1 in the samples we drew')",
      all(1.3 <= v <= 2.1 for v in mins_pp))
# Mutation: the claim 'stuck loss' would be false for a teacher in SO(2)^2.
rng = np.random.default_rng(7)
X = rng.normal(0, 1.5, size=(40, 2))
Y = np.tanh(X @ rot(0.7).T) @ rot(-0.3).T
check("ch10 negative control: teacher in SO(2)^2 is fitted in SO(2)^2", comp_min(1, 1, X, Y) < 1e-8)

# (B) symmetry: flip sign of hidden unit 0
S = np.diag([-1.0, 1.0])
W1, W2 = rot(0.4), rot(1.1)
check("ch10 sign flip: f unchanged", np.allclose(np.tanh(X @ (S @ W1).T) @ (W2 @ S).T, np.tanh(X @ W1.T) @ W2.T))
check("ch10 sign flip: each det flips, product preserved",
      np.isclose(np.linalg.det(S @ W1), -1) and np.isclose(np.linalg.det(W2 @ S), -1))
# mutation: flipping only the incoming weights changes f
check("ch10 mutation: flipping only W1 changes f", not np.allclose(np.tanh(X @ (S @ W1).T) @ W2.T, np.tanh(X @ W1.T) @ W2.T))

# (C) critical-point obstruction. Teacher in SO(2)^2 => Sigma* meets the
# component of any theta_0 in SO(2)^2. Take theta_0 = argmax of the loss on
# SO(2)^2. Riemannian GD on SO(2)^2 in angle coordinates (flat metric) is
# plain GD on the torus: theta <- theta - eta * grad.
Lmax, pmax = comp_max(1, 1, X, Y)
f = lambda p: loss(rot(p[0]), rot(p[1]), X, Y)


def grad(p, h=1e-6):
    return np.array([(f(p + h * e) - f(p - h * e)) / (2 * h) for e in np.eye(2)])


g0 = np.linalg.norm(grad(pmax))
print("     loss max on SO(2)^2 = %.4f, |grad| there = %.1e" % (Lmax, g0))
check("ch10 NEW: the loss maximizer on SO(2)^2 is a critical point (|grad| < 1e-6, loss > eps)", g0 < 1e-6 and Lmax > 0.5)
# At an exact critical point theta - eta*grad = theta: the GD trajectory is constant
# (analytic). Numerically, the escape time from distance r grows like log(1/r):
# control: from a generic start GD reaches ~0
p = np.array([2.0, -1.0])
for _ in range(4000):
    p = p - 0.05 * grad(p)
check("ch10 control: GD from a generic start in SO(2)^2 reaches loss < 1e-6", f(p) < 1e-6)
# steps needed from starts at distance r from the maximizer grow without bound
steps = []
for r in (1e-2, 1e-4, 1e-6):
    p = pmax + r * np.array([1.0, 0.3])
    n = 0
    while f(p) > 1e-3 and n < 200000:
        p = p - 0.05 * grad(p)
        n += 1
    steps.append(n)
    print("     start at distance %.0e from maximizer: %d steps to loss < 1e-3" % (r, n))
check("ch10 NEW: steps to reach Sigma* increase as theta_0 -> maximizer (no uniform step bound)",
      steps[0] < steps[1] < steps[2])

# (D) Remark rem:length_bound annulus: Fisher metric (1+l0) I + grad psi grad psi^T,
# cond = 1 + |grad psi|^2/(1+l0) >= Lmax  <=>  |psi'(r)| >= sqrt((Lmax-1)(1+l0)).
from scipy.optimize import brentq
dpsi = lambda r: 60 * r * (1 - r * r) ** 2
thr = np.sqrt(0.5 * 1.1)
rpk = 1 / np.sqrt(5)  # max of r(1-r^2)^2
r_in = brentq(lambda r: dpsi(r) - thr, 1e-9, rpk)
r_out = brentq(lambda r: dpsi(r) - thr, rpk, 1 - 1e-12)
print("     annulus: %.4f <= |theta-c| <= %.4f" % (r_in, r_out))
check("ch10 annulus 0.012 <= |theta-c| <= 0.941", round(r_in, 3) == 0.012 and round(r_out, 3) == 0.941)
r_in_m = brentq(lambda r: dpsi(r) - np.sqrt(0.5), 1e-9, rpk)
check("ch10 mutation (drop 1+lambda0): inner radius changes", round(r_in_m, 4) != round(r_in, 4))

print("\nFAILURES:", FAILS if FAILS else "none")
raise SystemExit(1 if FAILS else 0)
