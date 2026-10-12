"""
F-02 independent numerical audit -- Chapter 8
(chap08_noneuclidean_minimax_relativity_adm.tex)

Every claim: independent oracle + negative control (mutated formula that
must fail). Read-only; does not edit the chapter. Includes dimensional /
order-of-magnitude sanity where the claim is a physics formula (the chapter
itself has no dimensionful CODATA-scale numbers to compare against: all
quantities below are geometric, in natural/geometrized units, consistent
with the chapter's own conventions).
"""
import numpy as np
import sympy as sp
from scipy.optimize import minimize

rng = np.random.default_rng(7)
PASS, FAIL = [], []


# ---------------------------------------------------------------------------
# Shared symbolic differential-geometry helpers (3D Riemannian), used below
# to independently re-derive Claims 3 and 5 directly from the metric
# components via Christoffel/Riemann tensors -- rather than evaluating the
# book's own already-stated closed forms, which was the tautology flagged
# by L2 for both claims.
# ---------------------------------------------------------------------------
def sym_christoffels(g, coords):
    n = len(coords)
    ginv = g.inv()
    Gamma = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = sp.S(0)
                for d in range(n):
                    s += ginv[a, d] * (sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b]) - sp.diff(g[b, c], coords[d]))
                Gamma[a][b][c] = sp.simplify(s / 2)
    return Gamma


def sym_riemann(Gamma, coords):
    n = len(coords)
    R = [[[[sp.S(0)] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    term = sp.diff(Gamma[a][b][d], coords[c]) - sp.diff(Gamma[a][b][c], coords[d])
                    s = sp.S(0)
                    for e in range(n):
                        s += Gamma[a][c][e] * Gamma[e][b][d] - Gamma[a][d][e] * Gamma[e][b][c]
                    R[a][b][c][d] = sp.simplify(term + s)
    return R


def report(name, line, ok, detail):
    (PASS if ok else FAIL).append(name)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} (book line ~{line})")
    print(f"       {detail}")


# ---------------------------------------------------------------------------
# Claim 1 (lines 172-184, Theorem "Sectional-Extrinsic Coupling"):
# K_M = Kbar + kappa^2 for an umbilical hypersurface of a space form.
# Oracle: explicit embedding of a small 2-sphere (geodesic radius r) in
# S^3(c^2) <- R^4 (flat ambient), using NON-symmetric stereographic
# coordinates (u,v) so the metric is not trivially constant; compute first
# and second fundamental forms via FINITE DIFFERENCES of the embedding
# (independent of the book's Gauss-equation-with-umbilical-ansatz proof),
# and sum the Gauss formula over the codimension-2 normal bundle in flat
# R^4 -- a completely different (purely Euclidean, codim-2 Gauss) route to
# K_M that does not use the book's curved-ambient Gauss equation.
# Negative control: the mutated relation K_M = Kbar - kappa^2 must disagree.
# ---------------------------------------------------------------------------
def small_sphere_curvatures(c_val, r_val, u0, v0, h=1e-4):
    rho = np.sin(c_val * r_val) / c_val
    h4 = np.cos(c_val * r_val) / c_val
    R_val = 1.0 / c_val

    def X(u, v):
        d = 1 + u ** 2 + v ** 2
        return np.array([rho * 2 * u / d, rho * 2 * v / d, rho * (u ** 2 + v ** 2 - 1) / d, h4])

    Xu = (X(u0 + h, v0) - X(u0 - h, v0)) / (2 * h)
    Xv = (X(u0, v0 + h) - X(u0, v0 - h)) / (2 * h)
    Xuu = (X(u0 + h, v0) - 2 * X(u0, v0) + X(u0 - h, v0)) / h ** 2
    Xvv = (X(u0, v0 + h) - 2 * X(u0, v0) + X(u0, v0 - h)) / h ** 2
    Xuv = (X(u0 + h, v0 + h) - X(u0 + h, v0 - h) - X(u0 - h, v0 + h) + X(u0 - h, v0 - h)) / (4 * h ** 2)

    E, F, G = Xu @ Xu, Xu @ Xv, Xv @ Xv
    n_amb = X(u0, v0) / R_val
    n_amb = n_amb / np.linalg.norm(n_amb)
    A = np.vstack([Xu, Xv, n_amb])
    _, _, Vt = np.linalg.svd(A)
    nu = Vt[-1] / np.linalg.norm(Vt[-1])

    L1, M1, N1 = Xuu @ n_amb, Xuv @ n_amb, Xvv @ n_amb
    L2, M2, N2 = Xuu @ nu, Xuv @ nu, Xvv @ nu
    denom = E * G - F ** 2
    K1 = (L1 * N1 - M1 ** 2) / denom  # ambient (S^3) contribution -> should equal Kbar = c^2
    K2 = (L2 * N2 - M2 ** 2) / denom  # own-codimension contribution -> should equal kappa^2
    return K1, K2, K1 + K2


c_val, r_val = 1.3, 0.6
K1, K2, KM_numeric = small_sphere_curvatures(c_val, r_val, 0.3, 0.5)
Kbar = c_val ** 2
kappa_formula = c_val / np.tan(c_val * r_val)
KM_formula = Kbar + kappa_formula ** 2

ok1 = abs(KM_numeric - KM_formula) < 1e-5 * abs(KM_formula) and abs(K1 - Kbar) < 1e-5 * Kbar
report("K_M = Kbar + kappa^2 for a small 2-sphere in S^3 (finite-difference embedding + flat-ambient codim-2 Gauss formula)",
       "172-184", ok1,
       f"K1 (ambient contribution)={K1:.6f} vs Kbar={Kbar:.6f}; K2 (own contribution)={K2:.6f} vs kappa^2={kappa_formula**2:.6f}; "
       f"K_M numeric={KM_numeric:.6f} vs Kbar+kappa^2={KM_formula:.6f}")

KM_wrong = Kbar - kappa_formula ** 2
ok1_neg = abs(KM_numeric - KM_wrong) > abs(KM_numeric - KM_formula) * 3
report("NEGATIVE CONTROL: mutated relation K_M = Kbar - kappa^2 must disagree with the embedding-based computation",
       "172-184", ok1_neg, f"K_M numeric={KM_numeric:.6f}; correct Kbar+kappa^2={KM_formula:.6f}; mutated Kbar-kappa^2={KM_wrong:.6f}")


# ---------------------------------------------------------------------------
# Claim 2 (lines 220-244, Theorem "U-turns in tubes of space forms"): the
# optimal U-turn curvature bound k >= c*coth(cw/2) in H^2(-c^2) [resp.
# c*cot(cw/2) in S^2(+c^2)], derived from the identity
#   cosh(ca)+cosh(cb) = 2cosh(c(a+b)/2)cosh(c(b-a)/2),  int_a^b cosh(cy)dy = (2/c)cosh(c(a+b)/2)sinh(c(b-a)/2)
# so that [cosh(ca)+cosh(cb)]/int_a^b cosh(cy)dy = c*coth(c(b-a)/2), minimized
# over the box -w/2<=a<b<=w/2 exactly at b-a=w.
# Oracle: direct numerical identity check (random a,b,c) + independent
# numerical constrained minimization (scipy.optimize) of the ratio, instead
# of the book's monotonicity argument.
# Negative control: a wrong hyperbolic sum identity must fail the same check.
# ---------------------------------------------------------------------------
def ratio_H2(a, b, c):
    return (np.cosh(c * a) + np.cosh(c * b)) / ((np.sinh(c * b) - np.sinh(c * a)) / c)


ident_ok = True
for _ in range(50):
    a, b, c = rng.uniform(-2, 2, 3)
    c = abs(c) + 0.1
    lhs = np.cosh(c * a) + np.cosh(c * b)
    rhs = 2 * np.cosh(c * (a + b) / 2) * np.cosh(c * (b - a) / 2)
    if abs(lhs - rhs) > 1e-9 * max(1, abs(lhs)):
        ident_ok = False
    lhs2 = ratio_H2(a, b, c)
    rhs2 = c / np.tanh(c * (b - a) / 2) if b != a else np.inf
    if b != a and abs(lhs2 - rhs2) > 1e-6 * max(1, abs(rhs2)):
        ident_ok = False

w_test, c_test = 1.4, 0.9


def neg_ratio(ab):
    a, b = ab
    if not (-w_test / 2 <= a < b <= w_test / 2):
        return 1e6
    return ratio_H2(a, b, c_test)


best = None
for _ in range(200):
    a0 = rng.uniform(-w_test / 2, 0)
    b0 = rng.uniform(0, w_test / 2)
    res = minimize(neg_ratio, [a0, b0], method='Nelder-Mead')
    if best is None or res.fun < best:
        best = res.fun

bound_formula = c_test / np.tanh(c_test * w_test / 2)
ok2 = ident_ok and abs(best - bound_formula) < 1e-3 * bound_formula
report("Hyperbolic sum-to-product identity holds, and numerical minimization of the ratio over the box matches c*coth(cw/2)",
       "220-244", ok2, f"identity check over 50 random (a,b,c): {ident_ok}; numeric min of ratio={best:.6f} vs formula c*coth(cw/2)={bound_formula:.6f}")

wrong_lhs_vs_sinh = all(abs((np.sinh(c * a) + np.sinh(c * b)) -
                            2 * np.cosh(c * (a + b) / 2) * np.cosh(c * (b - a) / 2)) < 1e-9
                         for a, b, c in [(0.3, 1.1, 0.7), (-0.5, 0.9, 1.2)])
ok2_neg = not wrong_lhs_vs_sinh
report("NEGATIVE CONTROL: wrong identity sinh(ca)+sinh(cb) = 2cosh(.)cosh(.) must fail",
       "220-244", ok2_neg, f"mutated sinh-identity holds for the tested (a,b,c): {wrong_lhs_vs_sinh} (should be False)")


# ---------------------------------------------------------------------------
# Claim 3 (lines 331-345, Proposition "Horizon Curvature in Painleve-
# Gullstrand Slicing"): r_+ = M+sqrt(M^2-Q^2) satisfies beta(r_+)^2 =
# 1-f(r_+) = 1 exactly, and the null expansion theta_l = 2(1-beta)/r
# vanishes exactly at r = r_+ (MOTS condition).
#
# L2 fix: the ORIGINAL "oracle" just plugged numbers into the book's own
# ALREADY-STATED closed form theta_l=2(1-beta)/r (only f(r+)=0, beta(r+)=1
# were genuinely independent algebra) -- the derivation of theta_l itself
# via D_i beta_j and K_ij was never tested. Here theta_l is RE-DERIVED from
# first principles via sympy, directly from the PG metric's lapse=1, shift
# N^r=beta, flat spatial metric h=dr^2+r^2dOmega^2: Christoffel symbols of h
# are computed symbolically, giving K_ij = D_(i N_j) (symmetrized covariant
# derivative of the shift one-form) and the divergence D_i s^i of the
# outward unit normal, combined via theta_l = D_i s^i - K + K_ij s^i s^j
# (the general MOTS formula quoted in the book's own proof, but now
# EVALUATED via an independent symbolic covariant-derivative computation
# rather than by hand-simplifying to 2(1-beta)/r and plugging in numbers).
# Negative control: the wrong horizon radius r_wrong = M (omitting the
# sqrt(M^2-Q^2) term) must NOT satisfy theta_l(r_wrong) = 0 for Q != 0.
# ---------------------------------------------------------------------------
r_s, theta_s, phi_s, M_s, Q_s = sp.symbols('r theta phi M Q', positive=True, real=True)
coords3 = [r_s, theta_s, phi_s]
beta_sym = sp.sqrt(2 * M_s / r_s - Q_s ** 2 / r_s ** 2)
h_flat = sp.diag(1, r_s ** 2, r_s ** 2 * sp.sin(theta_s) ** 2)
Gamma_h = sym_christoffels(h_flat, coords3)

N_up = [beta_sym, sp.S(0), sp.S(0)]               # shift vector N^i (lapse N=1)
N_low = [h_flat[i, i] * N_up[i] for i in range(3)]  # one-form N_i (diagonal metric)


def covariant_grad(vlow, Gamma, coords):
    n = len(coords)
    D = [[sp.S(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            val = sp.diff(vlow[j], coords[i])
            for k in range(n):
                val -= Gamma[k][i][j] * vlow[k]
            D[i][j] = val
    return D


D_N = covariant_grad(N_low, Gamma_h, coords3)
K_ij = [[sp.simplify((D_N[i][j] + D_N[j][i]) / 2) for j in range(3)] for i in range(3)]
h_inv = h_flat.inv()
K_trace = sp.simplify(sum(h_inv[i, i] * K_ij[i][i] for i in range(3)))

s_up = [sp.S(1), sp.S(0), sp.S(0)]  # outward unit normal to r=const (h_rr=1)
sqrt_h = sp.sqrt(h_flat.det())
div_s = sp.simplify(sp.diff(sqrt_h * s_up[0], r_s) / sqrt_h)
K_ss = K_ij[0][0] * s_up[0] * s_up[0]

theta_l_sym = sp.simplify(div_s - K_trace + K_ss)
f_RN_sym = 1 - 2 * M_s / r_s + Q_s ** 2 / r_s ** 2
theta_l_fn = sp.lambdify((r_s, M_s, Q_s), theta_l_sym, 'numpy')
f_RN_fn = sp.lambdify((r_s, M_s, Q_s), f_RN_sym, 'numpy')
beta_fn = sp.lambdify((r_s, M_s, Q_s), beta_sym, 'numpy')

cases = [(1.0, 0.0), (1.0, 0.6), (2.0, 1.5), (1.5, 0.9)]
ok3 = True
detail3 = []
for M, Q in cases:
    rp = M + np.sqrt(M ** 2 - Q ** 2)
    fval = f_RN_fn(rp, M, Q)
    b2 = beta_fn(rp, M, Q) ** 2
    th = theta_l_fn(rp, M, Q)
    th_out = theta_l_fn(rp * 1.1, M, Q)
    detail3.append((M, Q, rp, fval, b2, th, th_out))
    if not (abs(fval) < 1e-10 and abs(b2 - 1) < 1e-10 and abs(th) < 1e-8 and th_out > 1e-6):
        ok3 = False

report("RN apparent horizon: theta_l RE-DERIVED symbolically (sympy Christoffel symbols of the flat PG spatial "
       "metric, K_ij=D_(i)N_j), not plugged into the book's own closed form; theta_l(r+)=0, theta_l(1.1 r+)>0",
       "331-345", ok3,
       f"(M,Q,r+,f(r+),beta^2(r+),theta_l(r+),theta_l(1.1r+)): "
       f"{[(round(float(x), 8) if isinstance(x, (int, float, np.floating)) else x) for t in detail3 for x in t]}")

ok3_neg = True
for M, Q in cases:
    if Q == 0:
        continue
    r_wrong = M  # omits sqrt(M^2-Q^2)
    th_wrong = theta_l_fn(r_wrong, M, Q)
    if abs(th_wrong) < 1e-6:
        ok3_neg = False
report("NEGATIVE CONTROL: wrong horizon radius r=M (dropping sqrt(M^2-Q^2)) does not satisfy the symbolically "
       "re-derived MOTS condition theta_l=0",
       "331-345", ok3_neg, "checked for all Q != 0 test cases")


# ---------------------------------------------------------------------------
# Claim 4 (lines 284-294, Corollary "Pointwise Bounds on Slices of Bounded
# Extrinsic Curvature"): e2(lambda) = l1 l2+l2 l3+l3 l1 ranges EXACTLY over
# [-kappa^2, 3 kappa^2] for lambda in [-kappa,kappa]^3, giving the stated
# bounds on R^(gamma).
# Oracle: brute-force dense grid search + local optimization over the cube
# [-kappa,kappa]^3 (independent of the book's "affine in each variable ->
# extremum at a vertex" argument).
# Negative control: a mutated, wrong range [-3kappa^2, kappa^2] must be
# contradicted by the brute-force extrema.
# ---------------------------------------------------------------------------
kappa_t = 1.7


def e2(l):
    l1, l2, l3 = l
    return l1 * l2 + l2 * l3 + l3 * l1


grid = np.linspace(-kappa_t, kappa_t, 61)
L1g, L2g, L3g = np.meshgrid(grid, grid, grid, indexing='ij')
vals = L1g * L2g + L2g * L3g + L3g * L1g
e2_min, e2_max = vals.min(), vals.max()

ok4 = abs(e2_min - (-kappa_t ** 2)) < 1e-6 and abs(e2_max - 3 * kappa_t ** 2) < 1e-6
report("e2(lambda) ranges exactly over [-kappa^2, 3kappa^2] on the cube (brute-force dense grid search)",
       "284-294", ok4, f"grid min={e2_min:.6f} (expect {-kappa_t**2:.6f}), grid max={e2_max:.6f} (expect {3*kappa_t**2:.6f})")

wrong_range = (-3 * kappa_t ** 2, kappa_t ** 2)
ok4_neg = not (abs(e2_min - wrong_range[0]) < 1e-6 and abs(e2_max - wrong_range[1]) < 1e-6)
report("NEGATIVE CONTROL: mutated wrong range [-3kappa^2, kappa^2] must be contradicted by the grid extrema",
       "284-294", ok4_neg, f"grid extrema ({e2_min:.4f},{e2_max:.4f}) vs mutated claimed range {wrong_range}")


# ---------------------------------------------------------------------------
# Claim 5 (lines 367-393, Proposition "Throat Geometry and the Null Energy
# Bound"): for the Morris-Thorne metric dr^2/(1-b(r)/r)+r^2 dOmega^2, the
# spheres {r=const} have principal curvatures +-sqrt(1-b(r)/r)/r, vanishing
# at the throat r0 (b(r0)=r0), with intrinsic Gauss curvature 1/r0^2.
#
# L2 fix: the ORIGINAL "FD Lie-derivative" check only finite-differenced
# g_thth=r^2 (giving 2/r trivially, for ANY b(r)) and then multiplied by
# nu_r=sqrt(1-b/r) TYPED DIRECTLY from the formula under test -- tautological.
#
# Independent route (Gauss equation): for the sphere {r=r_fixed} inside the
# 3-metric gamma = dr^2/(1-b(r)/r) + r^2 dOmega^2, the GAUSS EQUATION relates
# its INTRINSIC curvature (trivially 1/r^2, a round sphere of that radius)
# to the ambient sectional curvature K_ambient(theta,phi) of gamma in the
# (theta,phi)-plane and to the square of its principal curvature kappa:
#     1/r^2 = K_ambient(theta,phi) + kappa^2.
# K_ambient is computed here from the FULL RIEMANN TENSOR of gamma (for the
# concrete profile b(r)=r0^3/r^2), via sympy Christoffel/Riemann symbols --
# a route that does not touch sqrt(1-b/r) at all until the very end, where
# kappa is SOLVED FOR via the Gauss equation, not substituted in.
# Sanity check: setting r0=0 (flat space, b=0) gives K_ambient=0, as it must.
# Negative control: the mutated formula kappa = sqrt(1-b(r)/r) (missing the
# 1/r factor) must disagree with the Gauss-equation-derived kappa.
# ---------------------------------------------------------------------------
r_s5, theta_s5, phi_s5, r0_s = sp.symbols('r theta phi r0', positive=True, real=True)
coords5 = [r_s5, theta_s5, phi_s5]
b_sym = r0_s ** 3 / r_s5 ** 2  # concrete flare-out profile, b(r0)=r0, b'(r0)=-2<1
f_sym = 1 - b_sym / r_s5
gamma_mt = sp.diag(1 / f_sym, r_s5 ** 2, r_s5 ** 2 * sp.sin(theta_s5) ** 2)
Gamma_mt = sym_christoffels(gamma_mt, coords5)
Riem_mt = sym_riemann(Gamma_mt, coords5)
R_thphthph = sp.simplify(sum(gamma_mt[1, e] * Riem_mt[e][2][1][2] for e in range(3)))
K_ambient_sym = sp.simplify(R_thphthph / (gamma_mt[1, 1] * gamma_mt[2, 2]))

# sanity check: flat space (r0=0) must give K_ambient = 0
assert sp.simplify(K_ambient_sym.subs(r0_s, 0)) == 0, "flat-space sanity check failed"

kappa_sq_sym = sp.simplify(1 / r_s5 ** 2 - K_ambient_sym)
kappa_sym = sp.sqrt(kappa_sq_sym)
kappa_fn = sp.lambdify((r_s5, r0_s), kappa_sym, 'numpy')
K_ambient_fn = sp.lambdify((r_s5, r0_s), K_ambient_sym, 'numpy')

r0_t = 2.0
r_test_vals = [2.0, 2.5, 3.0, 3.5, 4.0]  # physical range r >= r0 = 2.0 for this shape function
ok5 = True
detail5 = []
for rr in r_test_vals:
    kappa_gauss = float(kappa_fn(rr, r0_t))
    kappa_formula5 = np.sqrt(max(1 - (r0_t ** 3 / rr ** 2) / rr, 0)) / rr
    detail5.append((rr, kappa_gauss, kappa_formula5))
    if abs(kappa_gauss - kappa_formula5) > 1e-6:
        ok5 = False
kappa_at_throat = float(kappa_fn(r0_t, r0_t))
gauss_curv_throat = 1.0 / r0_t ** 2
if abs(kappa_at_throat) > 1e-6:
    ok5 = False

report("Morris-Thorne principal curvature kappa, SOLVED FOR via the Gauss equation 1/r^2 = K_ambient + kappa^2 "
       "with K_ambient computed from the full symbolic Riemann tensor of the 3-metric (sympy), independent of "
       "sqrt(1-b/r) -- matches sqrt(1-b(r)/r)/r and vanishes at throat; intrinsic Gauss curv=1/r0^2",
       "367-393", ok5, f"(r, kappa from Gauss eq., formula sqrt(1-b/r)/r): "
       f"{[(round(x,6) if isinstance(x,float) else x) for t in detail5 for x in t]}; "
       f"kappa at throat={kappa_at_throat:.2e} (should be ~0); Gauss curvature 1/r0^2={gauss_curv_throat:.6f}")

ok5_neg = True
for rr in [2.5, 3.0, 3.5, 4.0]:
    kappa_gauss = float(kappa_fn(rr, r0_t))
    kappa_wrong = np.sqrt(max(1 - (r0_t ** 3 / rr ** 2) / rr, 0))  # missing 1/r factor
    if abs(kappa_gauss - kappa_wrong) < 1e-4:
        ok5_neg = False
report("NEGATIVE CONTROL: mutated formula kappa = sqrt(1-b/r) (missing 1/r) must disagree with the "
       "Gauss-equation-derived kappa",
       "367-393", ok5_neg, "checked for r != r0 in the test grid")


print()
print("=" * 70)
print(f"Chapter 8 summary: {len(PASS)} PASS, {len(FAIL)} FAIL")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("  -", f)
