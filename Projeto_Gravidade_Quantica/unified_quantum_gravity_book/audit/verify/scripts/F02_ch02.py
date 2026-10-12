"""
F-02 independent numerical audit -- Chapter 2
(chap02_geometric_flows_tensor_varieties.tex)

Every claim: independent oracle + negative control (mutated formula that
must fail). Read-only; does not edit the chapter.
"""
import numpy as np
from scipy.linalg import expm, qr
from scipy.integrate import solve_ivp

np.random.seed(0)
PASS, FAIL = [], []


def report(name, line, ok, detail):
    (PASS if ok else FAIL).append(name)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} (book line ~{line})")
    print(f"       {detail}")


# ---------------------------------------------------------------------------
# Claim 1 (line 228-233): dimension of the Tensor-Train variety
#   dim(M_r^TT) = sum_a d_a r_{a-1} r_a - sum_{a=1}^{k-1} r_a^2.
# Oracle: build the explicit multilinear parametrization map Phi (TT cores ->
# full tensor), compute its Jacobian NUMERICALLY by finite differences at a
# random full-rank point, and take its rank via SVD -- independent of the
# book's Lie-group-gauge-orbit argument.
# Negative control: the "no gauge quotient" formula sum_a d_a r_{a-1} r_a
# (omitting the subtraction) must disagree with the numeric rank.
# ---------------------------------------------------------------------------
d = (3, 3, 3)
r = (1, 2, 2, 1)  # r0=1, r1=2, r2=2, r3=1
k = 3


def shapes():
    return [(r[a], d[a], r[a + 1]) for a in range(k)]


shp = shapes()
sizes = [np.prod(s) for s in shp]
offsets = np.cumsum([0] + sizes)
n_params = int(offsets[-1])


def unpack(theta):
    cores = []
    for a in range(k):
        seg = theta[offsets[a]:offsets[a + 1]]
        cores.append(seg.reshape(shp[a]))
    return cores


def Phi(theta):
    cores = unpack(theta)
    # contract G1(i1) G2(i2) G3(i3) -> tensor of shape d
    T = np.einsum('aib,bjc,ckd->ijkd', *cores)  # d=1 trailing index (r3=1)
    return T[..., 0].reshape(-1)


theta0 = np.random.randn(n_params)


def numerical_jacobian(f, x, eps=1e-6):
    f0 = f(x)
    J = np.zeros((len(f0), len(x)))
    for i in range(len(x)):
        xp = x.copy(); xp[i] += eps
        xm = x.copy(); xm[i] -= eps
        J[:, i] = (f(xp) - f(xm)) / (2 * eps)
    return J

J = numerical_jacobian(Phi, theta0)
rank_numeric = np.linalg.matrix_rank(J, tol=1e-4)

dim_formula = sum(d[a] * r[a] * r[a + 1] for a in range(k)) - sum(r[a] ** 2 for a in range(1, k))
# feasibility check (eq. 222): r_a <= min(r_{a-1} d_a, d_{a+1} r_{a+1})
feasible = all(r[a] <= min(r[a - 1] * d[a - 1], d[a] * r[a + 1]) for a in range(1, k))

ok1 = feasible and (rank_numeric == dim_formula)
report("TT-variety dim = sum d_a r_{a-1} r_a - sum r_a^2 (numerical Jacobian rank, finite differences)",
       "228-233", ok1,
       f"feasible={feasible}, numeric Jacobian rank={rank_numeric}, formula gives {dim_formula} "
       f"(raw parameter count = {n_params}, gauge-orbit dim = {sum(r[a]**2 for a in range(1,k))})")

dim_wrong = sum(d[a] * r[a] * r[a + 1] for a in range(k))  # omit gauge subtraction
ok1_neg = dim_wrong != rank_numeric
report("NEGATIVE CONTROL: raw parameter count (no gauge subtraction) must disagree with numeric rank",
       "228-233", ok1_neg, f"raw count = {dim_wrong} vs numeric Jacobian rank = {rank_numeric}")


# ---------------------------------------------------------------------------
# Claim 2 (lines 293-332, Theorem 2.6): Toda flow dA/dt = [A, Pi_so(A)] is
# isospectral, and A(1) = Q(1)^T A0 Q(1) where exp(A0) = Q(1)R(1) (QR of the
# matrix exponential).
# Oracle: direct numerical ODE integration (solve_ivp, RK45, independent of
# the book's Lie-group / uniqueness-of-ODE argument) of the matrix ODE, plus
# an independently computed QR factorization of expm(A0) via scipy.linalg.qr.
# Negative control: replace Pi_so(A) (skew part) by the strictly-upper part
# of A with no antisymmetrization (NOT skew-symmetric, and not algebraically
# forced to coincide with +-Pi_so(A) via [A,A]=0) -- isospectrality must fail.
# ---------------------------------------------------------------------------
n = 4
A0 = np.random.randn(n, n)
A0 = (A0 + A0.T) / 2


def pi_so(A):
    L = np.tril(A, -1)
    return L - L.T


def pi_b(A):
    return A - pi_so(A)


def strictly_upper_no_antisymmetrize(A):
    # plausible bug: forgot to antisymmetrize the lower-triangular part
    # (book's correct generator is L - L^T, i.e. pi_so(A)); this returns
    # just the strictly-upper part of A, which is NOT skew-symmetric and is
    # NOT algebraically forced to equal +-pi_so(A) via [A,A]=0.
    return np.triu(A, 1)


def toda_rhs(t, Avec, generator):
    A = Avec.reshape(n, n)
    K = generator(A)
    dA = A @ K - K @ A
    return dA.reshape(-1)

sol = solve_ivp(toda_rhs, [0, 1], A0.reshape(-1), args=(pi_so,), method='RK45',
                 rtol=1e-11, atol=1e-13, dense_output=True)
A1_ode = sol.y[:, -1].reshape(n, n)

eig0 = np.sort(np.linalg.eigvalsh(A0))
eig1 = np.sort(np.linalg.eigvalsh(A1_ode))
isospectral_ok = np.allclose(eig0, eig1, atol=1e-7)

# QR of the matrix exponential, independent oracle for item (iii)
X1 = expm(A0)
Q1, R1 = qr(X1)
# fix sign convention so R has non-negative diagonal (standard QR gauge)
signs = np.sign(np.diag(R1))
signs[signs == 0] = 1
Q1 = Q1 @ np.diag(signs)
R1 = np.diag(signs) @ R1
A1_qr = Q1.T @ A0 @ Q1

ok2 = isospectral_ok and np.allclose(A1_ode, A1_qr, atol=1e-6)
report("Toda flow is isospectral and A(1)=Q(1)^T A0 Q(1) via QR of expm(A0) (independent RK45 integration + scipy QR)",
       "293-332", ok2,
       f"max|eig(A0)-eig(A(1))|={np.max(np.abs(eig0-eig1)):.2e}; "
       f"max|A1_ode-A1_qr|={np.max(np.abs(A1_ode-A1_qr)):.2e}")

sol_wrong = solve_ivp(toda_rhs, [0, 1], A0.reshape(-1), args=(strictly_upper_no_antisymmetrize,), method='RK45',
                       rtol=1e-10, atol=1e-12)
A1_wrong = sol_wrong.y[:, -1].reshape(n, n)
eig1_wrong = np.sort(np.linalg.eigvalsh(A1_wrong))
ok2_neg = not np.allclose(eig0, eig1_wrong, atol=1e-4)
report("NEGATIVE CONTROL: commutator with non-skew, non-antisymmetrized generator instead of Pi_so(A) must break isospectrality",
       "293-332", ok2_neg,
       f"max|eig(A0)-eig(A_wrong(1))| = {np.max(np.abs(eig0-eig1_wrong)):.4f} (should be >0)")


# ---------------------------------------------------------------------------
# Claim 3 (lines 419-424, Theorem 2.10): closed-form solution of the
# non-local graphon heat equation,
#   W(t) = e^{-2t} W0 + (e^{-t}-e^{-2t})(d1(x)+d2(y)) + (1-e^{-t})^2 m.
# Oracle: discretize W0 on an n x n grid, solve the resulting LINEAR matrix
# ODE dW/dt = D1 + D2^T - 2W (entrywise, D1_i = row mean, D2_j = col mean)
# by direct numerical integration (solve_ivp), independent of the book's
# spectral-projector derivation.
# Negative control: wrong decay rate e^{-t} (instead of e^{-2t}) for the W0
# term, with correspondingly mismatched cross terms.
# ---------------------------------------------------------------------------
ng = 6
W0 = np.random.rand(ng, ng)
W0 = (W0 + W0.T) / 2
d1 = W0.mean(axis=1)  # d_1(x)
d2 = W0.mean(axis=0)  # d_2(y)
m = W0.mean()


def heat_rhs(t, Wvec):
    W = Wvec.reshape(ng, ng)
    row_mean = W.mean(axis=1, keepdims=True) * np.ones((1, ng))
    col_mean = W.mean(axis=0, keepdims=True) * np.ones((ng, 1))
    dW = row_mean + col_mean - 2 * W
    return dW.reshape(-1)

t_test = 0.7
sol_heat = solve_ivp(heat_rhs, [0, t_test], W0.reshape(-1), method='RK45',
                      rtol=1e-12, atol=1e-14)
W_numeric = sol_heat.y[:, -1].reshape(ng, ng)

D1 = np.outer(d1, np.ones(ng))
D2 = np.outer(np.ones(ng), d2)
W_closed = np.exp(-2 * t_test) * W0 + (np.exp(-t_test) - np.exp(-2 * t_test)) * (D1 + D2) + (1 - np.exp(-t_test)) ** 2 * m

ok3 = np.allclose(W_numeric, W_closed, atol=1e-6)
report("Graphon heat equation closed form (independent RK45 integration of the discretized linear PDE)",
       "419-424", ok3, f"max|W_numeric - W_closed| = {np.max(np.abs(W_numeric - W_closed)):.2e}")

W_wrong = np.exp(-t_test) * W0 + (np.exp(-0.5 * t_test) - np.exp(-t_test)) * (D1 + D2) + (1 - np.exp(-0.5 * t_test)) ** 2 * m
ok3_neg = not np.allclose(W_numeric, W_wrong, atol=1e-3)
report("NEGATIVE CONTROL: wrong decay rate e^{-t} (halved exponents) must disagree with RK45 integration",
       "419-424", ok3_neg, f"max|W_numeric - W_wrong| = {np.max(np.abs(W_numeric - W_wrong)):.2e} (should be large)")


# ---------------------------------------------------------------------------
# Claim 4 (lines 615-620, Theorem 2.13(ii), the F-48 fixed Dyson/holonomy
# error bound): explicit tightness example for r=1, A=0, R_j=M: the finite-k
# error is (1+M/k^2)^k - 1, which (a) EXCEEDS the naive bound M/k for every
# k>=2, and (b) is bounded above by (M/k) e^{M/k}.
# Oracle: direct high-precision arithmetic evaluation of (1+M/k^2)^k - 1 for
# a grid of (M,k), independent of the book's Taylor/Gronwall-type proof.
# Negative control: the naive (un-fixed) bound "error <= M/k" (without the
# exponential correction) must be VIOLATED -- this is exactly the defect
# F-48 corrected.
# ---------------------------------------------------------------------------
import mpmath as mp
mp.mp.dps = 50

ok4 = True
ok4_neg = False  # we WANT to find at least one violation of the naive bound
detail4 = []
for M in (0.5, 1.0, 2.0, 5.0):
    for kk in (2, 3, 5, 10, 50, 200):
        err = (1 + mp.mpf(M) / kk ** 2) ** kk - 1
        naive_bound = mp.mpf(M) / kk
        fixed_bound = (mp.mpf(M) / kk) * mp.e ** (mp.mpf(M) / kk)
        exceeds_naive = err > naive_bound
        within_fixed = err <= fixed_bound * (1 + mp.mpf('1e-12'))
        detail4.append((M, kk, float(err), float(naive_bound), float(fixed_bound), exceeds_naive, within_fixed))
        if not (exceeds_naive and within_fixed):
            ok4 = False
        if err > naive_bound:
            ok4_neg = True

report("Dyson tightness example: (1+M/k^2)^k - 1 exceeds M/k and is <= (M/k)e^{M/k} for all tested (M,k)",
       "615-620", ok4, f"checked {len(detail4)} (M,k) pairs; sample: {detail4[:3]}")
report("NEGATIVE CONTROL: the naive un-fixed bound 'error <= M/k' (F-48 defect) is indeed violated",
       "615-620", ok4_neg, "confirmed error > M/k for the tested (M,k) grid, as the book states")


# ---------------------------------------------------------------------------
# Claim 5 (lines 602-619, Theorem 2.13(i)-(ii)): general O(1/k) convergence
# of the discrete ordered product Z_k = Tr(A_k...A_1) to the path-ordered
# holonomy Tr(Pexp(oint A)), for a genuinely non-Abelian A(s) with R_j = 0
# (M=0), for r=2.
# Oracle: (a) compute the "exact" holonomy by solving the matrix ODE
# dU/ds = A(s)U(s) with a very fine, independent high-accuracy integrator
# (solve_ivp, RK45, rtol=1e-12); (b) compute Z_k by explicit discrete matrix
# products A_j = I + A(s_j)/k for increasing k, and check the error decays
# as O(1/k) (fit the log-log slope), consistent with the bound.
# Negative control: an artificially tightened O(1/k^2) claim must fail for
# large k, since the true decay is O(1/k).
# ---------------------------------------------------------------------------
sx = np.array([[0, 1], [1, 0]], dtype=float)
sz = np.array([[1, 0], [0, -1]], dtype=float)


def Afun(s):
    return 0.7 * np.sin(2 * np.pi * s) * sx + 0.4 * np.cos(2 * np.pi * s) * sz


def ode_U(s, Uvec):
    U = Uvec.reshape(2, 2)
    dU = Afun(s) @ U
    return dU.reshape(-1)

sol_U = solve_ivp(ode_U, [0, 1], np.eye(2).reshape(-1), method='RK45', rtol=1e-13, atol=1e-14)
U_exact = sol_U.y[:, -1].reshape(2, 2)
Z_exact = np.trace(U_exact)

ks = [10, 20, 40, 80, 160, 320]
errs = []
for kk in ks:
    U_k = np.eye(2)
    for j in range(1, kk + 1):
        sj = j / kk
        Aj = np.eye(2) + Afun(sj) / kk
        U_k = Aj @ U_k
    Zk = np.trace(U_k)
    errs.append(abs(Zk - Z_exact))

log_k = np.log(ks)
log_e = np.log(errs)
slope = np.polyfit(log_k, log_e, 1)[0]  # expect slope ~ -1 (i.e. error ~ C/k)

ok5 = -1.3 < slope < -0.7
report("Discrete-to-holonomy convergence rate O(1/k) (independent high-accuracy ODE solve + log-log fit)",
       "602-619", ok5, f"errors at k={ks}: {[f'{e:.2e}' for e in errs]}; fitted log-log slope = {slope:.3f} (expect ~-1)")

ok5_neg = not (-2.3 < slope < -1.7)  # an O(1/k^2) claim would need slope ~ -2
report("NEGATIVE CONTROL: artificially tightened O(1/k^2) rate must disagree with the fitted slope",
       "602-619", ok5_neg, f"fitted slope {slope:.3f} is not compatible with a -2 (1/k^2) decay")


print()
print("=" * 70)
print(f"Chapter 2 summary: {len(PASS)} PASS, {len(FAIL)} FAIL")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("  -", f)
