"""Layer-2 numerical re-check of the corrected Vol. I (2026-10-06).

Independent of the corrector's fixes_layer1_checks.py (no code reused). Every block
has an oracle that does not evaluate the paper's formula, and a negative control
(a mutated formula or the superseded v2 claim) that must FAIL.

Blocks
  A  Constr 3.7   Parseval on (T^2, dmu)            oracle: tensor-grid quadrature
  B  Thm 4.1      E = ||DA||^2+||AD||^2, ratio range  oracle: spectral differentiation on grid
  C  Ex 4.3       checkerboard energy and TV           oracle: B-oracle; mollified-gradient TV
  D  Thm 4.5      TV formula                           oracle: Gaussian mollification, refinement
  E  Thm 4.10     sharp constant 4                      oracle: brute force over cell unions
  F  Rem 5.2      De Silva-Lim sequence, rank > 2       oracle: direct tensor norm; slice pencil
  G  Thm 5.7(iv)  non-isotropy of multiset-iid model   oracle: Monte Carlo
  H  Thm 5.8      two-sided bound, beta clause, tail    oracle: SVD (k=2), HOPM lower /
                                                           unfolding upper bounds (k=3,4),
                                                           exact chi mean, Monte Carlo
  I  Prop 5.6     attention sup bound, f(0,0) = N       oracle: grid evaluation, lattice sums
Seeds fixed; runtime a few minutes; peak memory < 0.5 GB.
"""
import itertools
import math
import sys

import numpy as np
from scipy import ndimage, special, stats

rng = np.random.default_rng(20261006)
FAIL = 0


def check(name, ok, info=""):
    global FAIL
    print(("PASS " if ok else "FAIL ") + name + ("  " + info if info else ""))
    if not ok:
        FAIL += 1


def neg(name, mutant_ok, info=""):
    """mutant_ok must be False (the mutated claim must fail)."""
    check("NEG " + name, not mutant_ok, info)


# ---------------------------------------------------------------- A
def harmonic_grid(A, M):
    n = A.shape[0]
    x = 2 * np.pi * np.arange(M) / M
    X1, X2 = np.meshgrid(x, x, indexing="ij")
    f = np.zeros((M, M), complex)
    for k1 in range(1, n + 1):
        for k2 in range(1, n + 1):
            f += A[k1 - 1, k2 - 1] * np.exp(1j * (k1 * X1 + k2 * X2))
    return f


print("== A  Construction 3.7")
n = 4
A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
f = harmonic_grid(A, 64)
L2 = math.sqrt(np.mean(np.abs(f) ** 2))  # normalized measure, exact for M > 2n
check("||f_A||_{L2(dmu)} = ||A||_F", abs(L2 - np.linalg.norm(A)) < 1e-10, f"{L2:.12f} vs {np.linalg.norm(A):.12f}")
L2leb = L2 * 2 * np.pi
check("Lebesgue factor 2pi", abs(L2leb - 2 * np.pi * np.linalg.norm(A)) < 1e-9)
neg("v2 claim ||(1/n) sum ..||_{L2(dx)} = ||A||_F", abs(L2leb / n - np.linalg.norm(A)) < 1e-6,
    f"{L2leb / n:.4f} vs {np.linalg.norm(A):.4f}")

# ---------------------------------------------------------------- B
def energy_oracle(A, M):
    """grad by FFT spectral differentiation of grid samples, then grid mean of |grad|^2."""
    f = harmonic_grid(A, M)
    F = np.fft.fft2(f)
    k = np.fft.fftfreq(M, 1.0 / M)
    K1, K2 = np.meshgrid(k, k, indexing="ij")
    g1 = np.fft.ifft2(1j * K1 * F)
    g2 = np.fft.ifft2(1j * K2 * F)
    return float(np.mean(np.abs(g1) ** 2 + np.abs(g2) ** 2))


def energy_fd(A, M):
    """second-order central differences: an approximate oracle with a refinement study."""
    f = harmonic_grid(A, M)
    h = 2 * np.pi / M
    g1 = (np.roll(f, -1, 0) - np.roll(f, 1, 0)) / (2 * h)
    g2 = (np.roll(f, -1, 1) - np.roll(f, 1, 1)) / (2 * h)
    return float(np.mean(np.abs(g1) ** 2 + np.abs(g2) ** 2))


print("== B  Theorem 4.1")
n = 5
A = rng.normal(size=(n, n))
D = np.diag(np.arange(1, n + 1))
paper = np.linalg.norm(D @ A) ** 2 + np.linalg.norm(A @ D) ** 2
orc = energy_oracle(A, 32)
check("E(f_A) spectral oracle = ||DA||^2+||AD||^2", abs(orc - paper) < 1e-8 * paper, f"{orc:.8f} vs {paper:.8f}")
errs = []
for M in (32, 64, 128, 256):
    errs.append(abs(energy_fd(A, M) - paper))
rates = [math.log2(errs[i] / errs[i + 1]) for i in range(3)]
check("FD refinement converges to the formula at order 2", all(abs(r - 2) < 0.15 for r in rates),
      "observed orders " + ", ".join(f"{r:.3f}" for r in rates))
mut = sum((i + j) ** 2 * A[i - 1, j - 1] ** 2 for i in range(1, n + 1) for j in range(1, n + 1))
neg("mutant weight (k1+k2)^2", abs(orc - mut) < 1e-6 * paper, f"{mut:.3f} vs {orc:.3f}")
neg("v2 Lebesgue reading with 1/n: (2pi/n)^2-free value differs", abs(orc * (2 * np.pi / n) ** 2 - paper) < 1e-6 * paper)
# ratio range over random A and random permutations
worst_hi, worst_lo = 0, 1e9
for _ in range(400):
    A = rng.normal(size=(n, n)); A = A + A.T
    p1, p2 = rng.permutation(n), rng.permutation(n)
    e1 = energy_oracle(A[np.ix_(p1, p1)], 16); e2 = energy_oracle(A[np.ix_(p2, p2)], 16)
    worst_hi = max(worst_hi, e2 / e1); worst_lo = min(worst_lo, e2 / e1)
check("random ratios inside [n^-2, n^2]", n ** -2 <= worst_lo and worst_hi <= n ** 2,
      f"range [{worst_lo:.3f}, {worst_hi:.3f}] vs [{n ** -2:.3f}, {n ** 2}]")
E11 = np.zeros((n, n)); E11[0, 0] = 1
Enn = np.zeros((n, n)); Enn[-1, -1] = 1
r = energy_oracle(Enn, 16) / energy_oracle(E11, 16)
check("E_nn / E_11 ratio = n^2", abs(r - n ** 2) < 1e-9, f"{r:.6f}")
for name, B in (("I_n", np.eye(n)), ("J_n", np.ones((n, n)))):
    vals = {round(energy_oracle(B[np.ix_(p, p)], 16), 8) for p in itertools.permutations(range(n))}
    check(f"{name}: all {math.factorial(n)} permutations give one energy (ratio 1)", len(vals) == 1)
vI = [energy_oracle(np.eye(n)[np.ix_(p, p)], 16) for p in itertools.permutations(range(n))]
neg("v2 'exists ratio n^2 for every A != 0' on A = I_n", max(vI) / min(vI) >= n ** 2 - 1e-9,
    f"max ratio {max(vI) / min(vI):.6f}")

# ---------------------------------------------------------------- C, D
def tv_mollified(A, sub, sigma_cells):
    """sample W_A on a fine grid of (n*sub)^2 cell centres, Gaussian-mollify with width
    sigma_cells*h (h = 1/(n*sub)) using reflecting boundary, then integrate |grad|."""
    n = A.shape[0]
    W = np.kron(A, np.ones((sub, sub)))
    Wm = ndimage.gaussian_filter(W.astype(float), sigma=sigma_cells, mode="nearest")
    h = 1.0 / (n * sub)
    gx = np.gradient(Wm, h, axis=0); gy = np.gradient(Wm, h, axis=1)
    return float(np.sum(np.sqrt(gx ** 2 + gy ** 2)) * h * h)


def tv_formula(A):
    n = A.shape[0]
    return (np.abs(np.diff(A, axis=0)).sum() + np.abs(np.diff(A, axis=1)).sum()) / n


print("== C  Example 4.3")
for n in (4, 8, 16):
    C = np.array([[(-1) ** (i + j) for j in range(1, n + 1)] for i in range(1, n + 1)], float)
    e = energy_oracle(C, 4 * n + 4)
    closed = 2 * n * n * (n + 1) * (2 * n + 1) / 6
    check(f"n={n}: checkerboard energy = 2n*n(n+1)(2n+1)/6", abs(e - closed) < 1e-7 * closed, f"{e:.4f}")
    eJ = energy_oracle(np.ones((n, n)), 4 * n + 4)
    check(f"n={n}: J_n energy identical", abs(eJ - e) < 1e-7 * e)
e_big = [energy_oracle(np.array([[(-1) ** (i + j) for j in range(n)] for i in range(n)], float), 4 * n + 4) / n ** 4
         for n in (8, 16, 32)]
check("E/n^4 -> 2/3", abs(e_big[-1] - 2 / 3) < 0.06, ", ".join(f"{v:.4f}" for v in e_big))
e3 = [v * n for v, n in zip(e_big, (8, 16, 32))]
neg("v2 claim E = Theta(n^3): E/n^3 bounded", e3[-1] / e3[0] < 2, f"E/n^3 = {[round(v, 2) for v in e3]}")
n = 6
C = np.array([[(-1) ** (i + j) for j in range(n)] for i in range(n)], float)
check("TV(checkerboard) formula = 4(n-1)", abs(tv_formula(C) - 4 * (n - 1)) < 1e-12)

print("== D  Theorem 4.5 (TV of the step realization)")
n = 5
A = rng.integers(-3, 4, size=(n, n)).astype(float)
target = tv_formula(A)
vals = []
for sub in (8, 16, 32, 64):
    vals.append(tv_mollified(A, sub, sigma_cells=2.0))  # mollifier width 2h -> 0 with h
errs = [abs(v - target) for v in vals]
rates = [math.log2(errs[i] / errs[i + 1]) for i in range(3)]
# first-order convergence (the mollifier width is 2h): Richardson extrapolation 2 v_h - v_2h
rich = 2 * vals[-1] - vals[-2]
check("mollified TV -> formula: order ~1 and Richardson limit matches", all(abs(r - 1) < 0.15 for r in rates[1:])
      and abs(rich - target) < 0.005 * target,
      f"target {target:.4f}; values {', '.join(f'{v:.4f}' for v in vals)}; orders {', '.join(f'{r:.2f}' for r in rates)}; Richardson {rich:.4f}")
neg("mutant without 1/n", abs(rich - target * n) < 0.05 * target * n)
vC = [tv_mollified(C, sub, 2.0) for sub in (32, 64)]
richC = 2 * vC[1] - vC[0]
check("checkerboard TV by mollification (Richardson) = 4(n-1)", abs(richC - 4 * (C.shape[0] - 1)) < 0.01 * 4 * (C.shape[0] - 1), f"{vC[1]:.4f} -> {richC:.4f}")

# ---------------------------------------------------------------- E
print("== E  Theorem 4.10 sharpness")
Wc = np.array([[1, -1], [-1, 1]], float)
# cut norm of a step kernel: sup over fractional cell weights in [0,1]^m; bilinear -> vertices
best = 0
for s in itertools.product((0, 1), repeat=2):
    for t in itertools.product((0, 1), repeat=2):
        best = max(best, abs(np.array(s) @ Wc @ np.array(t)) / 4)
uv = np.array([1, -1])
inf1 = abs(uv @ Wc @ uv) / 4
check("cut norm 1/4, L_inf->L_1 value 1, ratio 4", abs(best - 0.25) < 1e-15 and abs(inf1 - 1) < 1e-15)
neg("mutant constant 2", inf1 <= 2 * best)
worst = 0
for _ in range(300):
    m = 6
    W = rng.normal(size=(m, m)); W = (W + W.T) / 2
    S01 = np.array(list(itertools.product((0, 1), repeat=m)), float)
    Spm = np.array(list(itertools.product((-1, 1), repeat=m)), float)
    cut = np.abs(S01 @ W @ S01.T).max() / m ** 2
    inf = np.abs(Spm @ W @ Spm.T).max() / m ** 2
    worst = max(worst, inf / cut)
    if not (cut <= inf + 1e-12 and inf <= 4 * cut + 1e-12):
        worst = 99
check("random 6x6 step kernels: cut <= ||T||_{inf->1} <= 4 cut", worst <= 4, f"max ratio {worst:.3f}")

# ---------------------------------------------------------------- F
print("== F  Remark 5.2")
a, b = np.eye(2)
def outer3(x, y, z): return np.einsum("i,j,k->ijk", x, y, z)
T = outer3(a, a, b) + outer3(a, b, a) + outer3(b, a, a)
for t in (10.0, 100.0, 1000.0):
    w = a + b / t
    lam1 = t * np.linalg.norm(w) ** 3
    v = w / np.linalg.norm(w)
    X = lam1 * outer3(v, v, v) - t * outer3(a, a, a)
    err = np.linalg.norm(T - X)
    check(f"t={t:g}: ||T - X_t|| * t -> sqrt(3)", abs(err * t - math.sqrt(3)) < 2 / t, f"{err * t:.6f}; weights {lam1:.3g}, {t:g}")
S0, S1 = T[:, :, 0], T[:, :, 1]
Mp = np.linalg.solve(S0, S1)
nilpotent = np.allclose(Mp @ Mp, 0) and not np.allclose(Mp, 0)
check("slice pencil S0^-1 S1 is a nonzero nilpotent (not diagonalizable) => rank > 2", nilpotent)
U2 = outer3(a, a, np.array([1.0, 1.0])) + outer3(b, b, np.array([1.0, -1.0]))  # rank 2, invertible slice
P2 = np.linalg.solve(U2[:, :, 0], U2[:, :, 1])
neg("control: a rank-2 tensor gives a nilpotent pencil", np.allclose(P2 @ P2, 0) and not np.allclose(P2, 0))

# ---------------------------------------------------------------- G
print("== G  Theorem 5.7(i),(iv)")
d, nn, NS = 3, 2, 200000
x1 = np.array([1.0, 0.0]); x2 = np.array([1.0, 1.0]) / math.sqrt(2)
# multiset-iid symmetric tensor: one N(0,1) per multiset, copied to every ordering
ms = list(itertools.combinations_with_replacement(range(nn), d))
G = rng.normal(size=(NS, len(ms)))
def form_vals(x):
    out = np.zeros(NS)
    for c, m in enumerate(ms):
        mult = math.factorial(d) // math.prod(math.factorial(m.count(i)) for i in set(m))
        out += G[:, c] * mult * math.prod(x[i] for i in m)
    return out
v1, v2 = form_vals(x1).var(), form_vals(x2).var()
check("Var f(e1) = 1, Var f((e1+e2)/sqrt2) = 5/2 (d=3)", abs(v1 - 1) < 0.02 and abs(v2 - 2.5) < 0.05, f"{v1:.4f}, {v2:.4f}")
neg("isotropy of the multiset-iid model", abs(v2 - v1) < 0.05)
# ordered-tuple model: covariance (x.y)^d by MC
Tn = rng.normal(size=(NS, nn, nn, nn))
fx = np.einsum("sijk,i,j,k->s", Tn, x1, x1, x1); fy = np.einsum("sijk,i,j,k->s", Tn, x2, x2, x2)
cov = np.mean(fx * fy)
check("ordered-tuple model: Cov = (x.y)^3", abs(cov - (x1 @ x2) ** 3) < 0.01, f"{cov:.4f} vs {(x1 @ x2) ** 3:.4f}")
check("Var at x2 = 1 (isotropic)", abs(fy.var() - 1) < 0.02)
cs = 2 * ((d - 1) ** 3 - 1) // (d - 2)
check("Cartwright-Sturmfels bound for n=d=3 is 14", cs == 14)

# ---------------------------------------------------------------- H
print("== H  Theorem 5.8")
def hopm(T, restarts, iters=60):
    k = T.ndim; dd = T.shape[0]; best = 0
    for _ in range(restarts):
        us = [rng.normal(size=dd) for _ in range(k)]
        us = [u / np.linalg.norm(u) for u in us]
        for _ in range(iters):
            for a_ in range(k):
                idx = [i for i in range(k) if i != a_]
                v = np.einsum(T, list(range(k)), *sum(([us[i], [i]] for i in idx), []), [a_])
                nv = np.linalg.norm(v)
                if nv > 0:
                    us[a_] = v / nv
        val = abs(np.einsum(T, list(range(k)), *sum(([us[i], [i]] for i in range(k)), []), []))
        best = max(best, val)
    return best


def unfold_upper(T):
    k = T.ndim; dd = T.shape[0]
    return min(np.linalg.norm(np.moveaxis(T, a_, 0).reshape(dd, -1), 2) for a_ in range(k))


Ck = lambda k: 2 * math.sqrt(2 * k * math.log(1 + 4 * k) + 2 * math.log(2))
check("C_3 = 8.19 as stated in the notes", abs(Ck(3) - 8.19) < 0.01, f"C_2={Ck(2):.3f}, C_3={Ck(3):.3f}, C_4={Ck(4):.3f}")
# arithmetic step: 2 sqrt(2kd log(1+4k) + 2 log 2) <= C_k sqrt(d) for d >= 1
ok = all(2 * math.sqrt(2 * k * d * math.log(1 + 4 * k) + 2 * math.log(2)) <= Ck(k) * math.sqrt(d) + 1e-12
         for k in range(2, 9) for d in range(1, 500))
check("net bound <= C_k sqrt(d) for all d >= 1", ok)
# lower-bound chain with the exact chi mean
chi_mean = lambda d: math.sqrt(2) * math.exp(special.gammaln((d + 1) / 2) - special.gammaln(d / 2))
ok = all(chi_mean(d) >= d / math.sqrt(d + 2) - 1e-12 and d / math.sqrt(d + 2) >= math.sqrt(d / 3) - 1e-12
         for d in range(1, 2000))
check("E||Z|| (exact chi mean) >= d/sqrt(d+2) >= sqrt(d/3), d = 1..1999", ok)
neg("mutant lower bound E||Z|| >= sqrt(d)", all(chi_mean(d) >= math.sqrt(d) for d in range(1, 50)))
# Gaussian maximal inequality, independent and equicorrelated
for rho in (0.0, 0.5):
    for N in (10, 1000, 20000):
        R = 400 if N > 1000 else 2000
        Z = math.sqrt(1 - rho) * rng.normal(size=(R, N)) + math.sqrt(rho) * rng.normal(size=(R, 1))
        em = np.abs(Z).max(axis=1).mean()
        check(f"E max|Z_i| <= sqrt(2 log 2N)  (rho={rho}, N={N})", em <= math.sqrt(2 * math.log(2 * N)), f"{em:.3f} <= {math.sqrt(2 * math.log(2 * N)):.3f}")
Z = rng.normal(size=(400, 20000))
neg("mutant sqrt(log 2N)", np.abs(Z).max(axis=1).mean() <= math.sqrt(math.log(40000)))
# telescoping identity of the net step (k = 3)
d = 7
T3 = rng.normal(size=(d, d, d))
u = [rng.normal(size=d) for _ in range(3)]; v = [rng.normal(size=d) for _ in range(3)]
Xf = lambda w: np.einsum("ijk,i,j,k->", T3, *w)
lhs = Xf(u) - Xf(v)
rhs = Xf([u[0] - v[0], u[1], u[2]]) + Xf([v[0], u[1] - v[1], u[2]]) + Xf([v[0], v[1], u[2] - v[2]])
check("telescoping X(u)-X(v) = sum_alpha X(v..,u_a - v_a,u..)", abs(lhs - rhs) < 1e-10)
neg("mutant telescoping without the last term", abs(lhs - rhs + Xf([v[0], v[1], u[2] - v[2]])) < 1e-10)

# expectation of the spectral norm: k = 2 exact, k = 3, 4 bracketed by HOPM (lower) and unfolding (upper)
results = {}
for k, ds, reps in ((2, (8, 16, 32, 64, 128), 200), (3, (4, 8, 16, 32, 64), 40), (4, (4, 8, 16, 24), 20)):
    for d in ds:
        lo, hi = [], []
        for _ in range(reps):
            T = rng.normal(size=(d,) * k)
            if k == 2:
                s = np.linalg.norm(T, 2); lo.append(s); hi.append(s)
            else:
                lo.append(hopm(T, restarts=6 if d <= 32 else 4, iters=40)); hi.append(unfold_upper(T))
        results[(k, d)] = (np.mean(lo) / math.sqrt(d), np.mean(hi) / math.sqrt(d))
        L, U = results[(k, d)]
        # HOPM is a lower estimate of the true sup (exact for k = 2); the unfolding norm is a
        # rigorous but loose upper bound (it grows like d^{(k-2)/2}), reported only.
        check(f"k={k} d={d}: 1/sqrt3 <= E sup f_hat (HOPM) <= C_k", 1 / math.sqrt(3) <= L <= Ck(k),
              f"HOPM/sqrt(d) {L:.3f}, unfolding upper/sqrt(d) {U:.3f} (loose), C_k {Ck(k):.2f}")
# HOPM robustness at k = 3, d = 32: 4 vs 24 restarts on the same tensors
Ts = [rng.normal(size=(32, 32, 32)) for _ in range(8)]
h4 = np.mean([hopm(T, 4, 40) for T in Ts]); h24 = np.mean([hopm(T, 24, 40) for T in Ts])
# tolerance 5%: the margin to C_3 is a factor ~3, so a 5% under-estimate cannot change the verdict
check("HOPM estimate stable under 6x more restarts (< 5%) and still <= C_3", abs(h24 - h4) < 0.05 * h24 and h24 / math.sqrt(32) <= Ck(3), f"{h4 / math.sqrt(32):.4f} vs {h24 / math.sqrt(32):.4f}")
# refinement study for k = 2: E||G||/sqrt(d) -> 2 (Bai-Yin), differences shrink
k2 = [results[(2, d)][0] for d in (8, 16, 32, 64, 128)]
gaps = [2 - x for x in k2]
check("k=2: E||G||/sqrt(d) increases to 2, gaps shrink", all(g > 0 for g in gaps) and all(gaps[i + 1] < gaps[i] for i in range(4)),
      "gaps " + ", ".join(f"{g:.4f}" for g in gaps) + "; ratios " + ", ".join(f"{gaps[i + 1] / gaps[i]:.3f}" for i in range(4)))
k3 = [results[(3, d)][0] for d in (8, 16, 32, 64)]
check("k=3: HOPM E sup/sqrt(d) stabilizes (successive changes shrink)", abs(k3[3] - k3[2]) < abs(k3[1] - k3[0]) + 0.02,
      ", ".join(f"{x:.3f}" for x in k3))
# beta clause and superseded normalizations
for beta, expect in ((0.25, "inf"), (0.75, "zero")):
    seq = [results[(3, d)][0] * d ** (0.5 - beta) for d in (8, 16, 32, 64)]
    grows = seq[-1] > seq[0] * 1.5
    check(f"beta={beta}: d^-beta E||T|| -> {expect}", grows if expect == "inf" else seq[-1] < seq[0] / 1.5, ", ".join(f"{s:.3f}" for s in seq))
    neg(f"v2 beta clause at beta={beta}", (not grows) if beta < 0.5 else grows)
seq = [results[(3, d)][0] * math.sqrt(d) / d for d in (8, 16, 32, 64)]
neg("superseded v1 normalization d^-(k-1)/2 stays Theta(1) for k=3", seq[-1] > 0.5 * seq[0], ", ".join(f"{s:.3f}" for s in seq))
# Rademacher entries (Remark 5.9): still bounded
for d in (8, 16, 32):
    vals = [hopm(rng.choice([-1.0, 1.0], size=(d, d, d)), 4, 40) / math.sqrt(d) for _ in range(20)]
    check(f"Rademacher k=3 d={d}: E sup f_hat in [1/sqrt3, C_3] (Remark 5.9)", 1 / math.sqrt(3) <= np.mean(vals) <= Ck(3), f"{np.mean(vals):.3f}")

# (ii) exact N(0,1) law and tail
for k, d in ((3, 10), (4, 6)):
    NS = 20000
    out = np.empty(NS)
    for s in range(NS):
        T = rng.normal(size=(d,) * k)
        us = [rng.normal(size=d) for _ in range(k)]; us = [x / np.linalg.norm(x) for x in us]
        out[s] = np.einsum(T, list(range(k)), *sum(([us[i], [i]] for i in range(k)), []), [])
    ks = stats.kstest(out, "norm")
    check(f"(ii) k={k} d={d}: sqrt(d) f_hat ~ N(0,1) (KS p > 0.01)", ks.pvalue > 0.01, f"KS p = {ks.pvalue:.3f}")
    fh = out / math.sqrt(d)
    eps = np.linspace(0.05, 1.2, 24)
    emp = np.array([np.mean(np.abs(fh) > e) for e in eps])
    bound = 2 * np.exp(-d * eps ** 2 / 2)
    check(f"(ii) k={k} d={d}: empirical tail <= 2 exp(-d eps^2/2)", np.all(emp <= bound + 3 * np.sqrt(bound / NS) + 1e-4))
    mut = 2 * np.exp(-d * eps ** 2)
    neg(f"(ii) k={k} d={d}: mutant tail 2exp(-d eps^2)", np.all(emp <= mut), f"max emp/mut {np.max(emp / mut):.2f}")
    mutk = 2 * np.exp(-d * eps ** 2 * 2)  # a k-independent constant larger than 1/2 must fail too
    neg(f"(ii) k={k} d={d}: mutant constant 1 > 1/2", np.all(emp <= mutk))

# ---------------------------------------------------------------- I
print("== I  Proposition 5.6")
def C_lam(lam, K):
    k = np.arange(-K, K + 1)
    K1, K2 = np.meshgrid(k, k, indexing="ij")
    r2 = K1 ** 2 + K2 ** 2
    return math.sqrt(np.sum(1.0 / (1 + r2 + lam * r2 ** 2)))
lam = 0.5
Cl = math.sqrt(C_lam(lam, 400) ** 2 + 2 * math.pi / (lam * 400 ** 2))  # tail bound of the lattice sum
for N in (4, 8, 16):
    Lg = rng.normal(size=(N, N)) * 2
    S = np.exp(Lg); S /= S.sum(axis=1, keepdims=True)
    f = harmonic_grid(S, 8 * N)
    check(f"N={N}: f(0,0) = N", abs(f[0, 0] - N) < 1e-10)
    kk = np.arange(1, N + 1)
    K1, K2 = np.meshgrid(kk, kk, indexing="ij")
    R = np.sum((1 + K1 ** 2 + K2 ** 2 + lam * (K1 ** 2 + K2 ** 2) ** 2) * S ** 2)
    check(f"N={N}: sup|f| <= C_lam sqrt(R)", np.abs(f).max() <= Cl * math.sqrt(R), f"{np.abs(f).max():.3f} <= {Cl * math.sqrt(R):.3f}")
c0 = [C_lam(0.0, K) ** 2 for K in (50, 100, 200, 400)]
neg("lambda = 0: lattice sum converges", c0[-1] - c0[-2] < 0.1 * (c0[1] - c0[0]), "partial sums " + ", ".join(f"{c:.3f}" for c in c0))
cl = [C_lam(lam, K) ** 2 for K in (50, 100, 200, 400)]
check("lambda = 0.5: lattice sum converges (increments shrink ~K^-2)", cl[-1] - cl[-2] < 0.3 * (cl[1] - cl[0]), ", ".join(f"{c:.5f}" for c in cl))

print("failures:", FAIL)
sys.exit(FAIL)
