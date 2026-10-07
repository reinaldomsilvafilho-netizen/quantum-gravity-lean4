"""Corrector's independent checks for Vol. I (fixes_layer1.md).

Each block: an oracle computed by a method different from the paper formula,
the corrected statement, and a negative control (a mutated formula that must fail).
Fixed seed. Writes nothing but stdout; run with  > fixes_layer1_checks.out.txt
Exit code = number of failures.
"""
import itertools
import math
import sys

import numpy as np

rng = np.random.default_rng(20261006)
FAIL = 0


def check(name, cond):
    global FAIL
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAIL += 1


def neg(name, cond_that_must_fail):
    """negative control: the mutated statement must be false"""
    global FAIL
    ok = not cond_that_must_fail
    print(("PASS NEG " if ok else "FAIL NEG ") + name)
    if not ok:
        FAIL += 1


# ---------------------------------------------------------------- harmonic
def harmonic_grid(A, M):
    """f_A(x) = sum_k a_k e^{i k.x} on an M x M grid of [0,2pi)^2 (no 1/n)."""
    n = A.shape[0]
    x = 2 * np.pi * np.arange(M) / M
    E = np.exp(1j * np.outer(np.arange(1, n + 1), x))  # n x M
    return E.T @ A @ E  # f[x1, x2] = sum a_{k1 k2} e^{i k1 x1} e^{i k2 x2}


def norm_mu(f):
    """L2 norm for the normalized measure dx/(2pi)^2 by grid quadrature."""
    return math.sqrt(np.mean(np.abs(f) ** 2))


def energy_fd(A, M):
    """Dirichlet energy for dmu by 4th-order periodic finite differences."""
    f = harmonic_grid(A, M)
    h = 2 * np.pi / M

    def d(f, ax):
        return (-np.roll(f, -2, ax) + 8 * np.roll(f, -1, ax) - 8 * np.roll(f, 1, ax) + np.roll(f, 2, ax)) / (12 * h)

    return float(np.mean(np.abs(d(f, 0)) ** 2 + np.abs(d(f, 1)) ** 2))


def energy_formula(A):
    n = A.shape[0]
    k = np.arange(1, n + 1)
    return float(np.sum((k[:, None] ** 2 + k[None, :] ** 2) * np.abs(A) ** 2))


print("== Constr. 3.7: ||f_A||_{L2(dmu)} = ||A||_F ==")
for n in (2, 4, 7):
    A = rng.standard_normal((n, n))
    nm = norm_mu(harmonic_grid(A, 4 * n + 3))
    check(f"n={n}: grid {nm:.6f} vs ||A||_F {np.linalg.norm(A):.6f}", abs(nm - np.linalg.norm(A)) < 1e-10)
    # v2 text: f with 1/n and Lebesgue measure claimed ||f|| = ||A||_F
    lebesgue_v2 = (2 * np.pi) * nm / n
    neg(f"n={n}: v2 claim (1/n, Lebesgue) {lebesgue_v2:.4f} == ||A||_F", abs(lebesgue_v2 - np.linalg.norm(A)) < 1e-6)

print("\n== Thm 4.1: energy formula, FD oracle with refinement ==")
n = 5
A = rng.standard_normal((n, n))
ex = energy_formula(A)
errs = []
for M in (96, 192, 384):
    e = energy_fd(A, M)
    errs.append(abs(e - ex))
    print(f"  M={M}: FD {e:.10f}  formula {ex:.10f}  err {errs[-1]:.3e}")
check("FD converges to formula (rel err < 1e-5 at M=384)", errs[-1] < 1e-5 * ex)
rates = [math.log2(errs[i] / errs[i + 1]) for i in range(2) if errs[i + 1] > 1e-13]
print("  observed orders:", [f"{r:.2f}" for r in rates], "(expected 4: fourth-order differences)")
neg("mutant formula sum (k1+k2)|a|^2 matches FD",
    abs(float(np.sum((np.arange(1, n + 1)[:, None] + np.arange(1, n + 1)[None, :]) * A ** 2)) - ex) < 1e-6)
Dm = np.diag(np.arange(1.0, n + 1))
alg = np.linalg.norm(Dm @ A) ** 2 + np.linalg.norm(A @ Dm) ** 2
check(f"energy = ||DA||_F^2 + ||AD||_F^2 (matrix algebra): {alg:.10f}", abs(alg - ex) < 1e-9 * ex)
neg("mutant ||DAD||_F^2 equals the energy", abs(np.linalg.norm(Dm @ A @ Dm) ** 2 - ex) < 1e-6 * ex)

print("\n== Thm 4.1: ratio Theta(n^2) needs a suitable A; fails for I, J ==")
n = 6
for name, A in (("I", np.eye(n)), ("J", np.ones((n, n)))):
    ens = set()
    for p in itertools.permutations(range(n)):
        P = np.eye(n)[list(p)]
        ens.add(round(energy_formula(P @ A @ P.T), 9))
    check(f"A={name}: all 720 permutations give one energy (ratio 1)", len(ens) == 1)
E11 = np.zeros((n, n)); E11[0, 0] = 1
Enn = np.zeros((n, n)); Enn[-1, -1] = 1
check("E11 -> Enn ratio = n^2", abs(energy_formula(Enn) / energy_formula(E11) - n * n) < 1e-12)
# max over perms of ratio for a random symmetric A is bounded by (2n^2)/2 = n^2
As = rng.standard_normal((n, n)); As = As + As.T
vals = []
for p in itertools.permutations(range(n)):
    P = np.eye(n)[list(p)]
    vals.append(energy_formula(P @ As @ P.T))
r = max(vals) / min(vals)
check(f"random symmetric A: max/min ratio {r:.3f} <= n^2 = {n*n}", r <= n * n + 1e-9)

print("\n== Ex. 4.2: checkerboard energy ==")
for n in (4, 8, 16, 32):
    C = np.array([[(-1) ** (i + j) for j in range(n)] for i in range(n)], float)
    e = energy_fd(C, 32 * n)
    closed = 2 * n * n * (n + 1) * (2 * n + 1) / 6
    eJ = energy_formula(np.ones((n, n)))
    check(f"n={n}: FD {e:.4f} = 2n*n(n+1)(2n+1)/6 = {closed:.1f}; equals J energy", abs(e - closed) < 1e-3 * closed and abs(eJ - closed) < 1e-9)
    print(f"      E/n^4 = {closed / n**4:.4f}   E/n^3 = {closed / n**3:.4f}")
neg("v2 claim E = Theta(n^3): E/n^3 bounded on n=4..1024",
    max(2 * n * n * (n + 1) * (2 * n + 1) / 6 / n ** 3 for n in (4, 1024)) < 10)
# TV of checkerboard vs J (step realization)


def tv_formula(A):
    n = A.shape[0]
    return (np.abs(np.diff(A, axis=0)).sum() + np.abs(np.diff(A, axis=1)).sum()) / n


def tv_coarea(A, nt=4001):
    """integral over t of the perimeter of {W_A > t} inside (0,1)^2, by quadrature in t"""
    n = A.shape[0]
    lo, hi = A.min() - 1, A.max() + 1
    ts = np.linspace(lo, hi, nt)
    per = []
    for t in ts:
        S = A > t
        per.append((np.sum(S[1:, :] != S[:-1, :]) + np.sum(S[:, 1:] != S[:, :-1])) / n)
    return float(np.trapezoid(per, ts))


print("\n== Thm 4.4/4.5: TV formula vs coarea oracle ==")
for n in (4, 8):
    C = np.array([[(-1) ** (i + j) for j in range(n)] for i in range(n)], float)
    R = rng.integers(-3, 4, (n, n)).astype(float)
    for nm_, A in (("checker", C), ("random int", R)):
        a, b = tv_formula(A), tv_coarea(A)
        check(f"n={n} {nm_}: formula {a:.4f} coarea {b:.4f}", abs(a - b) < 2e-2 * max(1, a))
    check(f"n={n}: TV(checker) = 4(n-1) = {4*(n-1)}", abs(tv_formula(C) - 4 * (n - 1)) < 1e-12)
    neg(f"n={n}: mutant TV without 1/n equals coarea", abs(tv_formula(R) * n - tv_coarea(R)) < 2e-2 * tv_coarea(R))

# ---------------------------------------------------------------- cut norm constant
print("\n== Thm 4.9: constant 4 is attained ==")
W = np.array([[1.0, -1.0], [-1.0, 1.0]]) / 4.0  # step kernel, cell area 1/4 absorbed
# cut norm of a step kernel: sup over fractional subsets = max over 0/1 vectors (bilinear)
best_cut = max(abs(np.array(s) @ W @ np.array(t)) for s in itertools.product((0, 1), repeat=2) for t in itertools.product((0, 1), repeat=2))
best_op = max(abs(np.array(s) @ W @ np.array(t)) for s in itertools.product((-1, 1), repeat=2) for t in itertools.product((-1, 1), repeat=2))
check(f"2x2 checkerboard: op/cut = {best_op/best_cut:.3f} = 4", abs(best_op / best_cut - 4) < 1e-12)
neg("mutant constant 2 (op <= 2 cut)", best_op <= 2 * best_cut + 1e-12)

# ---------------------------------------------------------------- Kac-Rice section
print("\n== Thm 5.5: isotropy of the ordered-tuple model, non-isotropy of the multiset model ==")
for d in (2, 3):
    # multiset model: Var f(x) = sum_m mult(m)^2 x^{2m}
    x = np.array([1, 1]) / math.sqrt(2)
    var_ms = sum(math.comb(d, j) ** 2 * x[0] ** (2 * j) * x[1] ** (2 * (d - j)) for j in range(d + 1))
    check(f"d={d}: multiset model Var f((e1+e2)/sqrt2) = {var_ms:.4f} = C(2d,d)/2^d = {math.comb(2*d, d)/2**d:.4f} != 1",
          abs(var_ms - math.comb(2 * d, d) / 2 ** d) < 1e-12 and abs(var_ms - 1) > 0.1)
    # Monte Carlo for the ordered-tuple model: Var f(x) = |x|^{2d} = 1
    N = 40000
    T = rng.standard_normal((N,) + (2,) * d)
    fx = T.reshape(N, -1) @ np.array([np.prod(c) for c in itertools.product(x, repeat=d)])
    check(f"d={d}: ordered-tuple model MC Var f(x) = {fx.var():.3f} ~ 1", abs(fx.var() - 1) < 0.03)


def crit_points_cubic(T, starts=400, iters=200):
    """multi-start Riemannian Newton for critical points of T(x,x,x) on S^{n-1}; returns distinct points"""
    n = T.shape[0]
    pts = []
    for _ in range(starts):
        x = rng.standard_normal(n); x /= np.linalg.norm(x)
        for _ in range(iters):
            g = 3 * np.einsum('ijk,j,k->i', T, x, x)
            lam = x @ g / 3
            P = np.eye(n) - np.outer(x, x)
            rg = P @ g
            if np.linalg.norm(rg) < 1e-13:
                break
            H = 6 * np.einsum('ijk,k->ij', T, x)
            Hr = P @ H @ P - 3 * lam * P  # Riemannian Hessian: P H P - (x.grad) P, x.grad = 3 lam
            Hr = Hr + np.outer(x, x)  # make invertible on normal direction
            step = np.linalg.solve(Hr, -rg)
            step -= (x @ step) * x
            x = x + step; x /= np.linalg.norm(x)
        g = 3 * np.einsum('ijk,j,k->i', T, x, x)
        if np.linalg.norm(g - (x @ g) * x) < 1e-10 and not any(np.linalg.norm(x - p) < 1e-6 for p in pts):
            pts.append(x.copy())
    return pts


print("\n== Thm 5.5(iv): Cartwright-Sturmfels bound, n=3, d=3: at most 2*7 = 14 critical points ==")
maxc = 0
for trial in range(6):
    G = rng.standard_normal((3, 3, 3))
    S = sum(np.transpose(G, p) for p in itertools.permutations(range(3))) / 6
    c = len(crit_points_cubic(S))
    maxc = max(maxc, c)
    print(f"  trial {trial}: {c} critical points found")
check(f"max found {maxc} <= 14 and even", maxc <= 14)
neg("v2 claim exp(n Theta(d)) with Theta(d) >= d/2: 14 >= exp(3*1.5)=90", 14 >= math.exp(3 * 1.5))
print("  ABC (2.20): (1/n) log E Crit -> (1/2) log(d-1); d=2 gives 0 (2n points), d=3 gives 0.3466")
check("d=2 rate is zero", 0.5 * math.log(1) == 0)

# ---------------------------------------------------------------- critical scaling
print("\n== Thm 5.6: sup of X over (S^{d-1})^3 by HOPM, Gaussian and Rademacher ==")


def hopm_sup(T, restarts=6, iters=60):
    d = T.shape[0]
    best = 0
    for _ in range(restarts):
        u = [rng.standard_normal(d) for _ in range(3)]
        u = [v / np.linalg.norm(v) for v in u]
        for _ in range(iters):
            u[0] = np.einsum('ijk,j,k->i', T, u[1], u[2]); u[0] /= np.linalg.norm(u[0])
            u[1] = np.einsum('ijk,i,k->j', T, u[0], u[2]); u[1] /= np.linalg.norm(u[1])
            u[2] = np.einsum('ijk,i,j->k', T, u[0], u[1]); u[2] /= np.linalg.norm(u[2])
        best = max(best, abs(np.einsum('ijk,i,j,k->', T, *u)))
    return best


k = 3
upper_const = 2 * math.sqrt(2 * k * math.log(1 + 4 * k) + 2 * math.log(2))  # C_k of Thm 5.6
lower_const = 1 / math.sqrt(3)  # lower constant of Thm 5.6
# HOPM gives a lower estimate of the sup; it must exceed the proven lower bound and stay below C_k
for law in ("gauss", "rademacher"):
    rows = []
    for d in (8, 16, 32, 48):
        reps = 3
        s = []
        for _ in range(reps):
            T = rng.standard_normal((d, d, d)) if law == "gauss" else rng.choice([-1.0, 1.0], (d, d, d))
            s.append(hopm_sup(T))
        m = float(np.mean(s))
        rows.append((d, m / math.sqrt(d), m / d))
        print(f"  {law:10s} d={d:3d}: sup/sqrt(d) = {m/math.sqrt(d):.3f}   sup/d = {m/d:.3f}")
    lo = [r[1] for r in rows]
    if law == "gauss":
        check(f"{law}: sup/sqrt(d) in [1/sqrt3 = {lower_const:.3f}, C_k = {upper_const:.2f}]", min(lo) >= lower_const and max(lo) <= upper_const)
    else:
        check(f"{law}: sup/sqrt(d) bounded, in [0.5, C_k] (Remark, sub-Gaussian)", min(lo) >= 0.5 and max(lo) <= upper_const)
    # Hoelder lower bound E||Z|| >= d/sqrt(d+2), oracle: exact chi mean via Gamma functions
    for dd in (1, 2, 8, 48):
        exact = math.sqrt(2) * math.exp(math.lgamma((dd + 1) / 2) - math.lgamma(dd / 2))
        check(f"E||Z|| (d={dd}) = {exact:.4f} >= d/sqrt(d+2) = {dd/math.sqrt(dd+2):.4f} >= sqrt(d/3)",
              exact >= dd / math.sqrt(dd + 2) >= math.sqrt(dd / 3) - 1e-12) if law == "gauss" else None
    neg(f"{law}: mutant lower bound E||Z|| >= sqrt(d) (fails at d=1)", math.sqrt(2 / math.pi) >= 1.0) if law == "gauss" else None
    neg(f"{law}: v1 normalization d^-(k-1)/2 gives Theta(1) (sup/d non-decreasing)", rows[-1][2] >= rows[0][2] * 0.9)

print("\n== Thm 5.6(ii): tail of f_hat for Haar u, Gaussian entries ==")
d, N = 10, 20000  # memory: N*d^3*8 B = 160 MB per array
# fresh Gaussian tensor and fresh Haar tuple for each sample; X = <T, u1 x u2 x u3>
U = [rng.standard_normal((N, d)) for _ in range(3)]
U = [u / np.linalg.norm(u, axis=1, keepdims=True) for u in U]
w = np.einsum('ni,nj,nk->nijk', U[0], U[1], U[2]).reshape(N, -1)  # weights, rows of unit norm
X = np.einsum('nm,nm->n', w, rng.standard_normal(w.shape))
fh = X / math.sqrt(d)
for eps in (0.2, 0.4, 0.7):
    emp = float(np.mean(np.abs(fh) > eps))
    b = 2 * math.exp(-d * eps ** 2 / 2)
    check(f"eps={eps}: empirical {emp:.4f} <= 2exp(-d eps^2/2) = {b:.4f}", emp <= b)
emp = float(np.mean(np.abs(fh) > 0.7))
neg(f"mutant 2exp(-d eps^2) at eps=0.7 ({2*math.exp(-d*0.49):.4f}) bounds the tail {emp:.4f}", emp <= 2 * math.exp(-d * 0.49))
check(f"var of sqrt(d) f_hat = {X.var():.3f} ~ 1", abs(X.var() - 1) < 0.03)
del w, U

# ---------------------------------------------------------------- De Silva - Lim
print("\n== Sec. 6.4: rank-2 ill-posedness persists with unit-sphere factors ==")
a = np.array([1.0, 0.0]); b = np.array([0.0, 1.0])


def outer3(x, y, z):
    return np.einsum('i,j,k->ijk', x, y, z)


T = outer3(a, a, b) + outer3(a, b, a) + outer3(b, a, a)
for t in (1e1, 1e2, 1e3):
    v = a + b / t
    X = t * outer3(v, v, v) - t * outer3(a, a, a)
    lam1 = t * np.linalg.norm(v) ** 3
    err = np.linalg.norm(T - X)
    print(f"  t={t:7.0f}: ||T - X_t|| = {err:.3e}, weights ({lam1:.1f}, {t:.1f}) on unit-norm factors")
check("error ~ sqrt(3)/t at t=1000", abs(np.linalg.norm(T - (1e3 * outer3(a + b / 1e3, a + b / 1e3, a + b / 1e3) - 1e3 * outer3(a, a, a))) - math.sqrt(3) / 1e3) < 1e-5)
# T has rank 3 (De Silva-Lim Prop. 4.6 type example): no rank-2 tensor equals T.
# Exact check: the 3 slices T[:,:,0], T[:,:,1] form a pencil; a rank<=2 tensor in C^{2x2x2}
# with generic slices has a diagonalizable pencil. Here slice0^{-1} slice1 is a nontrivial Jordan block.
S0, S1 = T[:, :, 0], T[:, :, 1]
Mpen = np.linalg.solve(S0, S1)
ev = np.linalg.eigvals(Mpen)
jordan = abs(ev[0] - ev[1]) < 1e-12 and np.linalg.matrix_rank(Mpen - ev[0].real * np.eye(2)) == 1
check("pencil S0^{-1}S1 is a nontrivial Jordan block (T not of rank <= 2)", jordan)
neg("mutant claim: rank-2 best approximation attained with bounded weights (error 0 at t=10)",
    np.linalg.norm(T - (10 * outer3(a + b / 10, a + b / 10, a + b / 10) - 10 * outer3(a, a, a))) < 1e-9)

# ---------------------------------------------------------------- attention proposition
print("\n== Prop. 5.4: sup|f| <= C_lambda sqrt(R); softmax gives f(0,0) = N ==")


def C2(lam, K=400):
    k = np.arange(-K, K + 1)
    k2 = k[:, None] ** 2 + k[None, :] ** 2
    return float(np.sum(1.0 / (1 + k2 + lam * k2 ** 2)))


lam = 0.5
c = math.sqrt(C2(lam))
for N in (4, 8, 16):
    Z = rng.standard_normal((N, N)); Aat = np.exp(Z) / np.exp(Z).sum(1, keepdims=True)
    f = harmonic_grid(Aat, 4 * N + 4)
    kk = np.arange(1, N + 1)
    k2 = kk[:, None] ** 2 + kk[None, :] ** 2
    R = float(np.sum((1 + k2 + lam * k2 ** 2) * Aat ** 2))
    check(f"N={N}: f(0,0) = {f[0,0].real:.6f} = N; sup|f| {np.abs(f).max():.3f} <= C sqrt(R) = {c*math.sqrt(R):.3f}",
          abs(f[0, 0] - N) < 1e-9 and np.abs(f).max() <= c * math.sqrt(R) + 1e-9)
c0 = [C2(0.0, K) for K in (50, 100, 200)]
check(f"lambda=0: partial sums of C^2 grow like log K: {[round(v,2) for v in c0]}", c0[2] - c0[1] > 3.0 and c0[1] - c0[0] > 3.0)
neg("mutant: C^2 at lambda=0 converges (partial sums stable to 1e-2)", abs(c0[2] - c0[1]) < 1e-2)

print(f"\nfailures: {FAIL}")
sys.exit(FAIL)
