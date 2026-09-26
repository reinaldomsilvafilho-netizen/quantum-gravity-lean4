"""L2 round 2 (independent): ch10 Conj. 3.1 restated + remark "Why the initialization is random".

Independent oracle: loss on SO(2)^2 in angle coordinates (a, b), W1 = R(a), W2 = R(b),
gradient by central finite differences only (no analytic gradient), maximizer by dense grid
+ Nelder-Mead on -L, escape counts by explicit GD in angles with step 0.05.
Also: landscape census of local minima on the torus (spurious minima would refute the
probabilistic conjecture for small delta), and Haar ball measure scaling on SO(2)^2, SO(3).
Negative controls / mutations must FAIL where marked.
Run from the book folder.
"""
import numpy as np
from scipy.optimize import minimize

FAIL = []


def check(name, ok):
    print(("OK   " if ok else "FAIL ") + name)
    if not ok:
        FAIL.append(name)


def R(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[c, -s], [s, c]])


def make(seed, t1, t2, n=40):
    rng = np.random.default_rng(seed)
    X = rng.normal(0.0, 1.5, size=(n, 2))
    Y = np.tanh(X @ R(t1).T) @ R(t2).T
    return X, Y


def L(ab, X, Y):
    a, b = ab
    return np.mean(np.sum((np.tanh(X @ R(a).T) @ R(b).T - Y) ** 2, axis=1))


def grad(ab, X, Y, h=1e-6):
    g = np.zeros(2)
    for i in range(2):
        e = np.zeros(2); e[i] = h
        g[i] = (L(ab + e, X, Y) - L(ab - e, X, Y)) / (2 * h)
    return g


def hess(ab, X, Y, h=1e-4):
    H = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            ei = np.zeros(2); ei[i] = h
            ej = np.zeros(2); ej[j] = h
            H[i, j] = (L(ab + ei + ej, X, Y) - L(ab + ei - ej, X, Y) - L(ab - ei + ej, X, Y) + L(ab - ei - ej, X, Y)) / (4 * h * h)
    return H


def gd_steps(start, X, Y, eta=0.05, tol=1e-3, nmax=5000):
    th = np.array(start, float)
    for k in range(nmax):
        if L(th, X, Y) < tol:
            return k
        th = th - eta * grad(th, X, Y)
    return None


# ---- (A) the example of the remark: teacher R(0.7), R(-0.3), seed 7 (as documented by the fixer)
X, Y = make(7, 0.7, -0.3)
check("teacher has zero loss", L(np.array([0.7, -0.3]), X, Y) < 1e-28)
g = np.linspace(-np.pi, np.pi, 241)
vals = np.array([[L(np.array([a, b]), X, Y) for b in g] for a in g])
i, j = np.unravel_index(np.argmax(vals), vals.shape)
res = minimize(lambda z: -L(z, X, Y), [g[i], g[j]], method="Nelder-Mead", options=dict(xatol=1e-12, fatol=1e-15, maxiter=5000))
tmax = res.x
Lmax = L(tmax, X, Y)
H = hess(tmax, X, Y)
ev = np.linalg.eigvalsh(H)
print("  max loss %.4f at %s, |grad| %.1e, Hessian eig %s" % (Lmax, tmax, np.linalg.norm(grad(tmax, X, Y)), ev))
check("max loss about 4.18", abs(Lmax - 4.18) < 0.005)
check("maximizer is critical", np.linalg.norm(grad(tmax, X, Y)) < 1e-5)
check("strict local max (both Hessian eig < 0)", ev.max() < 0)
check("GD from maximizer does not move", np.linalg.norm(0.05 * grad(tmax, X, Y)) < 1e-6)

# escape counts along the unstable (most negative Hessian) eigendirection and along random directions
w, V = np.linalg.eigh(H)
vdom = V[:, np.argmin(w)]
counts = [gd_steps(tmax + r * vdom, X, Y) for r in (1e-2, 1e-4, 1e-6)]
print("  steps along dominant direction +v:", counts, " -v:", [gd_steps(tmax - r * vdom, X, Y) for r in (1e-2, 1e-4, 1e-6)])
u13 = np.array([1.0, 0.3]); u13n = u13 / np.linalg.norm(u13)
c13 = [gd_steps(tmax + r * u13, X, Y) for r in (1e-2, 1e-4, 1e-6)]
print("  direction (1,0.3) unnormalized (the fixer/referee's choice):", c13)
check("48/72/96 reproduced for displacement r*(1,0.3)", c13 == [48, 72, 96])
scan = {}
for ang in np.linspace(0, 2 * np.pi, 24, endpoint=False):
    u = np.array([np.cos(ang), np.sin(ang)])
    scan[round(ang, 2)] = [gd_steps(tmax + r * u, X, Y) for r in (1e-2, 1e-4, 1e-6)]
firsts = [v[0] for v in scan.values()]
incs = [(v[1] - v[0], v[2] - v[1]) for v in scan.values()]
print("  24 directions: steps at r=1e-2 range %d..%d; increments per factor 100: %s" % (min(firsts), max(firsts), sorted(set(sum(incs, ())))))
check("every direction: increments per factor 100 in r between 20 and 30 (log(1/r) growth, asymptotic slope 24)", all(20 <= a <= 30 and 20 <= b <= 30 for a, b in incs))
fine = [gd_steps(tmax + 1e-2 * np.array([np.cos(t), np.sin(t)]), X, Y) for t in np.linspace(0, 2 * np.pi, 360, endpoint=False)]
print("  360 directions at r=1e-2: min %d, max %d steps" % (min(fine), max(fine)))
check("48 is (up to 1) the minimum over directions at r=1e-2, so 'need 48' is a lower bound", min(fine) >= 47)
# log(1/r) law: increment per factor 100 in r = ln(100)/ln(1 + eta*|lambda_min|)
pred = np.log(100) / np.log(1 + 0.05 * abs(w.min()))
print("  predicted increment per decade^2: %.2f, observed %d, %d" % (pred, counts[1] - counts[0], counts[2] - counts[1]))
check("log(1/r) law: increments match ln100/ln(1+eta|lam|)", abs(counts[1] - counts[0] - pred) < 1.0 and abs(counts[2] - counts[1] - pred) < 1.0)
# MUTATION: step size 0.1 in place of 0.05 must NOT reproduce 48/72/96
mut = [gd_steps(tmax + r * vdom, X, Y, eta=0.1) for r in (1e-2, 1e-4, 1e-6)]
check("MUTATION (eta=0.1) reproduces 48/72/96 [must FAIL]", mut == [48, 72, 96])
# MUTATION: gradient linear in r would give 1/r-type growth; counts with a sqrt law would not be equally spaced
check("MUTATION: counts equally spaced under 1/r law [must FAIL]", abs((counts[2] - counts[1]) / (counts[1] - counts[0]) - 100) < 1)

# ---- (B) landscape census on SO(2)^2: are there spurious local minima with loss > 1e-3?
def census(X, Y, n=81):
    gg = np.linspace(-np.pi, np.pi, n, endpoint=False)
    mins = []
    for a in gg:
        for b in gg:
            r = minimize(lambda z: L(z, X, Y), [a, b], method="BFGS", jac=lambda z: grad(z, X, Y), options=dict(gtol=1e-10))
            mins.append(r.fun)
    return np.array(mins)

worst = []
for seed in range(6):
    rng = np.random.default_rng(500 + seed)
    t1, t2 = rng.uniform(-np.pi, np.pi, 2)
    Xs, Ys = make(900 + seed, t1, t2)
    m = census(Xs, Ys, n=25)
    frac = np.mean(m > 1e-3)
    worst.append(frac)
    print("  teacher seed %d: fraction of 625 local descents ending with loss > 1e-3: %.3f (max end loss %.2e)" % (seed, frac, m.max()))
m7 = census(X, Y, n=25)
print("  remark example: fraction ending > 1e-3: %.3f" % np.mean(m7 > 1e-3))
check("no spurious minima observed in the census (remark example + 6 teachers)", max(worst) == 0 and np.mean(m7 > 1e-3) == 0)
# NEGATIVE CONTROL: teacher in the (-,-) component; starts in SO(2)^2 must all fail to reach 1e-3
Xr = np.random.default_rng(11).normal(0, 1.5, (40, 2))
Refl = np.array([[1, 0], [0, -1]])
Yr = np.tanh(Xr @ (Refl @ R(0.4)).T)  # W1 reflection, W2 = I : prod det = -1
mr = census(Xr, Yr, n=13)
check("CONTROL: reflection teacher reachable from SO(2)^2 [must FAIL]", np.mean(mr > 1e-3) == 0)

# ---- (C) Haar measure of balls ~ r^{dim K}
# SO(2)^2 = flat torus, normalized Haar; geodesic ball of radius r (angle metric) has measure pi r^2/(2pi)^2
rng = np.random.default_rng(5)
P = rng.uniform(-np.pi, np.pi, size=(2_000_000, 2))
for r in (0.2, 0.1, 0.05):
    emp = np.mean(np.sum(P ** 2, axis=1) < r * r)
    print("  torus r=%.2f: MC %.3e vs r^2/(4pi) %.3e" % (r, emp, r * r / (4 * np.pi)))
emps = [np.mean(np.sum(P ** 2, axis=1) < r * r) for r in (0.4, 0.2)]
check("torus: exponent log2(m(0.4)/m(0.2)) = 2 = dim K", abs(np.log2(emps[0] / emps[1]) - 2) < 0.05)
# SO(3): Haar rotation angle density (1-cos t)/pi, ball measure (r - sin r)/pi ~ r^3/(6 pi)
from scipy.spatial.transform import Rotation
ang = Rotation.random(2_000_000, random_state=6).magnitude()
e1, e2 = np.mean(ang < 0.4), np.mean(ang < 0.2)
check("SO(3): exponent log2 ratio about 3 = dim SO(3)", abs(np.log2(e1 / e2) - 3) < 0.1)
check("MUTATION: SO(3) exponent 2 [must FAIL]", abs(np.log2(e1 / e2) - 2) < 0.1)

expected_fail = {
    "MUTATION (eta=0.1) reproduces 48/72/96 [must FAIL]",
    "MUTATION: counts equally spaced under 1/r law [must FAIL]",
    "CONTROL: reflection teacher reachable from SO(2)^2 [must FAIL]",
    "MUTATION: SO(3) exponent 2 [must FAIL]",
}
unexpected = [f for f in FAIL if f not in expected_fail]
missing = [f for f in expected_fail if f not in FAIL]
print("\nunexpected failures:", unexpected)
print("controls that did not fail:", missing)
raise SystemExit(1 if unexpected or missing else 0)
