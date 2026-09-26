"""Camada 2, F-47 (cap. 1). Independent checks of the NEW statements, each with a mutation.

K1  Kac-Rice ingredients for the i.i.d. (non-symmetric) model, computed EXACTLY from the
    coefficient tensors (f and its derivatives are linear in T, so covariances are inner
    products of coefficient tensors): Cov(grad) = d I, E[(H0)_ij^2] = d(d-1)(1+delta_ij),
    H0 uncorrelated with f and grad.  Mutation: coefficient d-1 instead of d.
K2  Riemannian Hessian on the sphere = H0 - d f I (second derivative along great circles).
    Mutation: H0 - (d-1) f I.
K3  equal-variance symmetric model: Monte Carlo Var f((e1+e2)/sqrt2) = 2^-d C(2d,d).
K4  Cartwright-Sturmfels bound on the circle (n=2): critical points <= 2d, attained.
    Mutation: bound 2n is exceeded.
C1  growth of C_lambda^2 = sum_{k in Z^2} 1/(1+|k|^2+lam|k|^4) as lam -> 0:
    C^2 - pi log(1/lam) stays bounded (logarithmic growth), sqrt(lam) C -> 0.
    Mutation: the referee's C ~ c lam^{-1/2} (sqrt(lam) C constant) fails.
"""
import itertools
import math
import numpy as np

rng = np.random.default_rng(7)
FAIL = []


def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + ("  | " + str(info) if not (isinstance(info, str) and info == "") else ""))
    if not ok:
        FAIL.append(name)


def outer(vs):
    t = vs[0]
    for v in vs[1:]:
        t = np.multiply.outer(t, v)
    return t


def coef_f(x, d):
    return outer([x] * d)


def coef_grad(x, d, i):
    n = len(x); e = np.eye(n)[i]
    return sum(outer([e if p == q else x for q in range(d)]) for p in range(d))


def coef_hess(x, d, i, j):
    n = len(x); ei, ej = np.eye(n)[i], np.eye(n)[j]
    tot = 0
    for p, q in itertools.permutations(range(d), 2):
        tot = tot + outer([ei if s == p else ej if s == q else x for s in range(d)])
    return tot


def ip(a, b):
    return float(np.sum(a * b))


# ---------------- K1
for d, n in ((3, 4), (4, 3), (2, 4)):
    x = np.zeros(n); x[0] = 1.0  # tangent directions e_1..e_{n-1} (indices 1..n-1)
    T = range(1, n)
    G = np.array([[ip(coef_grad(x, d, i), coef_grad(x, d, j)) for j in T] for i in T])
    H = {(i, j): coef_hess(x, d, i, j) for i in T for j in T}
    varH = np.array([[ip(H[i, j], H[i, j]) for j in T] for i in T])
    target = d * (d - 1) * (np.ones((n - 1, n - 1)) + np.eye(n - 1))
    corr_f = max(abs(ip(H[i, j], coef_f(x, d))) for i in T for j in T)
    corr_g = max(abs(ip(H[i, j], coef_grad(x, d, k))) for i in T for j in T for k in T)
    check(f"K1 d={d} n={n}: Cov(grad)=dI", np.allclose(G, d * np.eye(n - 1)), np.diag(G))
    check(f"K1 d={d} n={n}: E[H0_ij^2]=d(d-1)(1+delta)", np.allclose(varH, target), varH[0, :2])
    check(f"K1 d={d} n={n}: H0 uncorrelated with f and grad", corr_f < 1e-12 and corr_g < 1e-12)
    check(f"K1-mut d={d}: coefficient (d-1) for Cov(grad) fails", not np.allclose(G, (d - 1) * np.eye(n - 1)))

# ---------------- K2
def f_val(Tt, x):
    out = Tt
    for _ in range(Tt.ndim):
        out = out @ x if out.ndim == 1 else np.tensordot(out, x, axes=([out.ndim - 1], [0]))
    return float(out)


for d, n in ((3, 4), (4, 3), (5, 3)):
    Tt = rng.normal(size=(n,) * d)
    x = rng.normal(size=n); x /= np.linalg.norm(x)
    Q, _ = np.linalg.qr(np.column_stack([x, rng.normal(size=(n, n - 1))]))
    B = Q[:, 1:]  # orthonormal tangent basis
    # ambient Hessian and gradient by exact polynomial differentiation (coefficient tensors)
    grad = np.array([ip(Tt, coef_grad(x, d, i)) for i in range(n)])
    Hamb = np.array([[ip(Tt, coef_hess(x, d, i, j)) for j in range(n)] for i in range(n)])
    H0 = B.T @ Hamb @ B
    fx = f_val(Tt, x)
    # oracle: second derivatives along geodesics  gamma(t) = cos t x + sin t v, polarized
    h = 1e-3
    def g2(v):
        return (f_val(Tt, math.cos(h) * x + math.sin(h) * v) - 2 * fx + f_val(Tt, math.cos(h) * x - math.sin(h) * v)) / h ** 2
    Hr = np.zeros((n - 1, n - 1))
    for a in range(n - 1):
        for b in range(n - 1):
            va, vb = B[:, a], B[:, b]
            if a == b:
                Hr[a, a] = g2(va)
            else:
                Hr[a, b] = (g2((va + vb) / math.sqrt(2)) - g2((va - vb) / math.sqrt(2))) / 2
    err_d = np.abs(Hr - (H0 - d * fx * np.eye(n - 1))).max()
    err_dm1 = np.abs(Hr - (H0 - (d - 1) * fx * np.eye(n - 1))).max()
    check(f"K2 d={d}: Riem. Hessian = H0 - d f I (Euler: x.grad f = d f)", err_d < 1e-4 and abs(x @ grad - d * fx) < 1e-9, err_d)
    check(f"K2-mut d={d}: H0 - (d-1) f I fails", err_dm1 > 1e-2, err_dm1)

# ---------------- K3 Monte Carlo for the equal-variance symmetric model
for d in (2, 3):
    n = 2
    ms = list(itertools.combinations_with_replacement(range(n), d))
    mult = [math.factorial(d) // np.prod([math.factorial(m.count(c)) for c in set(m)]) for m in ms]
    x = np.array([1, 1]) / math.sqrt(2)
    mono = np.array([np.prod([x[i] for i in m]) for m in ms])
    N = 400000
    Z = rng.normal(size=(N, len(ms)))
    vals = Z @ (np.array(mult) * mono)
    v1 = (Z @ (np.array(mult) * np.array([1.0 if m == (0,) * d else 0.0 for m in ms]))).var()
    target = math.comb(2 * d, d) / 2 ** d
    check(f"K3 d={d}: Var f(e1)=1, Var f((e1+e2)/sqrt2)=2^-d C(2d,d)={target}", abs(v1 - 1) < 0.02 and abs(vals.var() - target) < 0.03 * target, (round(v1, 3), round(vals.var(), 3)))

# ---------------- K4 CS bound on the circle
for d in (3, 4, 5):
    best = 0
    for _ in range(300):
        Tt = rng.normal(size=(2,) * d)
        th = np.linspace(0, 2 * math.pi, 20001)[:-1]
        X = np.stack([np.cos(th), np.sin(th)])
        vals = np.einsum(Tt, list(range(d)), *sum([[X, [i, d]] for i in range(d)], []), [d])
        df = np.gradient(vals, th)
        s = np.sign(df)
        cnt = int(np.sum(s != np.roll(s, 1)))
        best = max(best, cnt)
    bound = 2 * ((d - 1) ** 2 - 1) // (d - 2)
    check(f"K4 n=2 d={d}: max #crit {best} <= CS bound {bound}", best <= bound)
    check(f"K4-mut n=2 d={d}: count 2n=4 exceeded", best > 4)

# ---------------- C1 growth of C_lambda
def C2(lam):
    K = int(min(40 / math.sqrt(lam), 6000))
    k = np.arange(-K, K + 1, dtype=float)
    tot = 0.0
    for k1 in k:
        r2 = k1 * k1 + k * k
        m = r2 <= K * K
        tot += np.sum(1.0 / (1 + r2[m] + lam * r2[m] ** 2))
    tail = math.pi / (lam * K * K)  # int_{r>K} 2 pi r dr /(lam r^4)
    return tot + tail


rows = []
for lam in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5):
    c2 = C2(lam)
    rows.append((lam, c2, c2 - math.pi * math.log(1 / lam), math.sqrt(lam * c2)))
    print("   lam=%.0e  C^2=%.4f  C^2 - pi log(1/lam)=%.4f  sqrt(lam)*C=%.4f" % rows[-1])
diffs = [r[2] for r in rows]
check("C1 C_lambda^2 - pi log(1/lambda) bounded (log growth)", max(abs(v) for v in diffs) < 1.5 and max(diffs[2:]) - min(diffs[2:]) < 0.1, diffs)
check("C1 sqrt(lambda) C_lambda -> 0", rows[-1][3] < 0.2 * rows[0][3], [round(r[3], 4) for r in rows])
check("C1-mut referee C ~ c lambda^{-1/2} (sqrt(lam) C constant) fails", rows[-1][3] / rows[0][3] < 0.5)
print("\nFAILURES:", FAIL if FAIL else "none")
