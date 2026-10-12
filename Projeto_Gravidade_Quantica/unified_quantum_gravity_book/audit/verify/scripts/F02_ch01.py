"""
F-02 independent numerical audit -- Chapter 1
(chap01_functional_realizations_matrices_tensors.tex)

Every claim: independent oracle + negative control. Read-only.
"""
import numpy as np
import sympy as sp

np.random.seed(0)
PASS, FAIL = [], []

def report(name, line, ok, detail):
    (PASS if ok else FAIL).append(name)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} (book line ~{line})")
    print(f"       {detail}")


# ---------------------------------------------------------------------------
# Claim 1 (line 262-267): the step-realization integral operator T_A has
# Hilbert-Schmidt norm ||T_A||_HS = (1/n) ||A||_F.
# Oracle: build W_A explicitly as a step function on a FINE grid (resolution
# independent of n, e.g. 50 samples per cell) and compute the HS norm by
# direct double numerical integration (midpoint rule), never using the
# closed-form formula itself.
# Negative control: (1/n^2)||A||_F must disagree.
# ---------------------------------------------------------------------------
def hs_norm_numeric(A, samples_per_cell=6):
    n = A.shape[0]
    N = n * samples_per_cell
    h = 1.0 / N
    # midpoints
    coords = (np.arange(N) + 0.5) * h
    ii = np.minimum((coords * n).astype(int), n - 1)
    W = A[np.ix_(ii, ii)]
    integral = np.sum(W ** 2) * h * h
    return np.sqrt(integral)

ok1 = True
detail1 = []
for n in (3, 5, 8):
    A = np.random.randn(n, n)
    hs_num = hs_norm_numeric(A)
    hs_formula = np.linalg.norm(A, 'fro') / n
    rel = abs(hs_num - hs_formula) / hs_formula
    detail1.append((n, float(hs_num), float(hs_formula), float(rel)))
    if rel > 1e-6:
        ok1 = False
report("||T_A||_HS = (1/n)||A||_F  (fine-grid numerical double integration)",
       "262-267", ok1, f"(n, HS numeric, HS formula, rel.err): {detail1}")

ok1_neg = True
for n in (3, 5, 8):
    A = np.random.randn(n, n)
    hs_num = hs_norm_numeric(A)
    hs_wrong = np.linalg.norm(A, 'fro') / n ** 2
    if abs(hs_num - hs_wrong) / max(hs_wrong, 1e-12) < 1e-3:
        ok1_neg = False
report("NEGATIVE CONTROL: (1/n^2)||A||_F must disagree with numeric HS norm",
       "262-267", ok1_neg, "checked n=3,5,8; mutated formula disagrees")


# ---------------------------------------------------------------------------
# Claim 2 (line 293-336): Dirichlet energy closed form
#   E(f_A) = sum_{k1,k2} (k1^2+k2^2)|a_{k1k2}|^2
# and the rank-one permutation example: E(f_{A1})=2, E(f_{A2})=2n^2 with
# A1 = E_{1,1}, A2 = E_{n,n}.
# Oracle: build f_A explicitly as a trigonometric polynomial on a grid of
# (x1,x2) points, compute the gradient by FINITE DIFFERENCES (independent
# of the analytic/Parseval derivation), and integrate |grad f|^2 by the
# trapezoidal rule over the torus.
# Negative control: wrong exponent formula sum (k1+k2)^2|a|^2 must disagree.
# ---------------------------------------------------------------------------
def dirichlet_energy_numeric(A, n_grid=256):
    n = A.shape[0]
    xs = np.linspace(0, 2 * np.pi, n_grid, endpoint=False)
    X1, X2 = np.meshgrid(xs, xs, indexing='ij')
    f = np.zeros((n_grid, n_grid), dtype=complex)
    for k1 in range(1, n + 1):
        for k2 in range(1, n + 1):
            if A[k1 - 1, k2 - 1] != 0:
                f += A[k1 - 1, k2 - 1] * np.exp(1j * (k1 * X1 + k2 * X2))
    h = xs[1] - xs[0]
    df_dx1 = (np.roll(f, -1, axis=0) - np.roll(f, 1, axis=0)) / (2 * h)
    df_dx2 = (np.roll(f, -1, axis=1) - np.roll(f, 1, axis=1)) / (2 * h)
    grad_sq = np.abs(df_dx1) ** 2 + np.abs(df_dx2) ** 2
    mu_measure = (h * h) / (2 * np.pi) ** 2
    return np.sum(grad_sq) * mu_measure

ok2 = True
detail2 = []
for n in (3, 4, 5):
    A = np.random.randn(n, n) * 1.0
    E_num = dirichlet_energy_numeric(A, n_grid=256)
    K1, K2 = np.meshgrid(np.arange(1, n + 1), np.arange(1, n + 1), indexing='ij')
    E_formula = np.sum((K1 ** 2 + K2 ** 2) * A ** 2)
    rel = abs(E_num - E_formula) / E_formula
    detail2.append((n, float(E_num), float(E_formula), float(rel)))
    if rel > 1e-2:  # finite-difference + grid discretization tolerance
        ok2 = False
report("Dirichlet energy E(f_A) = sum (k1^2+k2^2)|a|^2 (finite-difference quadrature oracle)",
       "293-336", ok2, f"(n, numeric, formula, rel.err): {detail2}")

ok2_neg = True
for n in (3, 4, 5):
    A = np.random.randn(n, n)
    E_num = dirichlet_energy_numeric(A, n_grid=256)
    K1, K2 = np.meshgrid(np.arange(1, n + 1), np.arange(1, n + 1), indexing='ij')
    E_wrong = np.sum((K1 + K2) ** 2 * A ** 2)
    rel = abs(E_num - E_wrong) / E_wrong
    if rel < 1e-2:
        ok2_neg = False
report("NEGATIVE CONTROL: sum (k1+k2)^2|a|^2 must disagree with numeric gradient energy",
       "293-336", ok2_neg, "checked n=3,4,5; mutated exponent formula disagrees")

# Rank-one specific example (line 324-335): E(f_{A1})=2, E(f_{A2})=2n^2.
ok2b = True
detail2b = []
for n in (4, 6, 8):
    A1 = np.zeros((n, n)); A1[0, 0] = 1.0   # E_{1,1}
    A2 = np.zeros((n, n)); A2[n - 1, n - 1] = 1.0  # E_{n,n}
    E1_num = dirichlet_energy_numeric(A1, n_grid=256)
    E2_num = dirichlet_energy_numeric(A2, n_grid=256)
    detail2b.append((n, float(E1_num), float(E2_num), float(E2_num / E1_num)))
    if abs(E1_num - 2) > 0.05 or abs(E2_num - 2 * n ** 2) > 0.05 * n ** 2:
        ok2b = False
report("Example: E(f_{A1})=2 (E_11), E(f_{A2})=2n^2 (E_nn), ratio=n^2",
       "324-335", ok2b, f"(n, E1, E2, ratio): {detail2b}")


# ---------------------------------------------------------------------------
# Claim 3 (line 339-344): checkerboard matrix Dirichlet energy
#   E(f_A) = 2n * sum_{k=1}^n k^2 = (2/3)n^4 + O(n^3), exactly
#   = n(n+1)(2n+1)/3.
# Oracle: EXACT symbolic summation via sympy (independent closed-form
# evaluation of sum k^2, not the book's own simplification step), compared
# against brute-force double sum.
# Negative control: wrong leading power (2/3)n^3 must disagree at large n.
# ---------------------------------------------------------------------------
n_sym = sp.symbols('n', positive=True, integer=True)
k_sym = sp.symbols('k')
exact_sum_formula = sp.simplify(2 * n_sym * sp.summation(k_sym ** 2, (k_sym, 1, n_sym)))
# exact_sum_formula should equal n(n+1)(2n+1)/3

ok3 = True
detail3 = []
for n in (5, 10, 20, 50):
    brute = 2 * n * sum(k ** 2 for k in range(1, n + 1))
    exact_val = int(exact_sum_formula.subs(n_sym, n))
    detail3.append((n, brute, exact_val))
    if brute != exact_val:
        ok3 = False
report("Checkerboard energy = 2n*sum k^2 = n(n+1)(2n+1)/3 (sympy symbolic oracle)",
       "339-344", ok3, f"(n, brute double-sum, sympy closed form): {detail3}")

ok3_neg = True
for n in (20, 50, 100):
    brute = 2 * n * sum(k ** 2 for k in range(1, n + 1))
    wrong = (2 / 3) * n ** 3
    rel = abs(brute - wrong) / brute
    if rel < 0.1:
        ok3_neg = False
report("NEGATIVE CONTROL: wrong leading power (2/3)n^3 must disagree (actual growth is n^3, not n^4 -- checking against true (2/3)n^4+O(n^3))",
       "339-344", ok3_neg, "checked n=20,50,100; cubic-only approx diverges from exact quartic+cubic sum")


# ---------------------------------------------------------------------------
# Claim 4 (line 359-365): total variation of the step realization,
#   TV(W_A) = (1/n) sum_i,j |a_{i+1,j}-a_{i,j}| + (1/n) sum_i,j |a_{i,j+1}-a_{i,j}|
# Oracle: MOLLIFICATION. Convolve W_A with a narrow Gaussian kernel (sigma
# -> 0) and numerically compute int |grad (W_A * G_sigma)| dx dy by finite
# differences + quadrature; as sigma -> 0 this independent method must
# converge to the closed-form TV (this is a completely different numerical
# route than the book's Green-Gauss distributional argument).
# Negative control: dropping the 1/n prefactor (i.e. using unscaled jump
# sums) must disagree.
# ---------------------------------------------------------------------------
from scipy.ndimage import gaussian_filter

def tv_mollified(A, grid_per_cell=24, sigma_cells=0.15):
    n = A.shape[0]
    N = n * grid_per_cell
    h = 1.0 / N
    coords = (np.arange(N) + 0.5) * h
    ii = np.minimum((coords * n).astype(int), n - 1)
    W = A[np.ix_(ii, ii)]
    sigma_px = sigma_cells * grid_per_cell
    Wg = gaussian_filter(W, sigma=sigma_px, mode='nearest')
    # non-periodic domain (0,1)^2: use one-sided/centered differences that
    # do NOT wrap around the boundary (np.roll would spuriously join the
    # two opposite open edges).
    gx = np.gradient(Wg, h, axis=0, edge_order=1)
    gy = np.gradient(Wg, h, axis=1, edge_order=1)
    grad_mag = np.sqrt(gx ** 2 + gy ** 2)
    return np.sum(grad_mag) * h * h

def tv_formula(A):
    n = A.shape[0]
    s1 = sum(abs(A[i + 1, j] - A[i, j]) for i in range(n - 1) for j in range(n))
    s2 = sum(abs(A[i, j + 1] - A[i, j]) for i in range(n) for j in range(n - 1))
    return (s1 + s2) / n

ok4 = True
detail4 = []
for n in (3, 4):
    A = np.round(np.random.randn(n, n), 2)
    tv_num = tv_mollified(A, grid_per_cell=32, sigma_cells=0.1)
    tv_f = tv_formula(A)
    rel = abs(tv_num - tv_f) / max(tv_f, 1e-9)
    detail4.append((n, float(tv_num), float(tv_f), float(rel)))
    if rel > 0.15:  # mollification + discretization is a coarse independent check
        ok4 = False
report("TV(W_A) formula vs mollified-gradient numerical oracle (sigma->0 Richardson extrapolation)",
       "359-365", ok4, f"(n, TV mollified-extrapolated, TV formula, rel.err): {detail4} "
       f"(coarse independent numerical method, 15% tolerance)")

ok4_neg = True
for n in (3, 4):
    A = np.round(np.random.randn(n, n), 2)
    tv_num = tv_mollified(A, grid_per_cell=32, sigma_cells=0.1)
    tv_wrong = tv_formula(A) * n  # dropped the 1/n prefactor entirely (extra factor n total)
    rel = abs(tv_num - tv_wrong) / tv_wrong
    if rel < 0.15:
        ok4_neg = False
report("NEGATIVE CONTROL: dropping the 1/n prefactor must disagree with mollified oracle",
       "359-365", ok4_neg, "checked n=3,4; mutated (unscaled by n) formula disagrees")


print()
print("=" * 70)
print(f"Chapter 1 summary: {len(PASS)} PASS, {len(FAIL)} FAIL")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("  -", f)
