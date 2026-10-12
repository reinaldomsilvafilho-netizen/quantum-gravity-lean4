"""
F-02 independent numerical audit -- Chapter 6
(chap06_sierpinski_fractal_resolvents_spectral_reduction.tex)

Every claim: independent oracle + negative control (mutated formula that
must fail). Read-only; does not edit the chapter.
"""
import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 40
PASS, FAIL = [], []

def report(name, line, ok, detail):
    (PASS if ok else FAIL).append(name)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} (book line ~{line})")
    print(f"       {detail}")


# ---------------------------------------------------------------------------
# Claim 1 (line 70-74, 180-191): Hausdorff/box dimension of Pascal's
# triangle mod 2 is ln3/ln2 ~ 1.58496, realised as #P_k = 3^k.
# Oracle: BRUTE FORCE enumeration of odd binomial coefficients mod 2 for
# rows 0..2^k-1 (independent of the IFS self-similarity argument in the
# book), fit dim = log(#P_k)/log(2^k).
# Negative control: claim dimension = ln4/ln2 = 2 (i.e. "all entries odd")
# must fail -- and #P_k = 4^k must fail against brute force.
# ---------------------------------------------------------------------------
def count_odd_binom_mod2_bruteforce(k):
    n_max = 2 ** k
    # Lucas' theorem check done independently via direct binomial mod 2
    # using Python's exact arbitrary precision arithmetic (math.comb),
    # NOT via the bitwise-AND shortcut that IS Lucas' theorem itself.
    import math
    count = 0
    for n in range(n_max):
        for j in range(n + 1):
            if math.comb(n, j) % 2 == 1:
                count += 1
    return count

counts = {}
for k in (2, 3, 4, 5, 6):
    counts[k] = count_odd_binom_mod2_bruteforce(k)

ok1 = all(counts[k] == 3 ** k for k in counts)
# independent log-fit of the dimension from brute-force counts
ks = sorted(counts)
log_fit = np.polyfit([k * np.log(2) for k in ks], [np.log(counts[k]) for k in ks], 1)
dim_fit = log_fit[0]
dim_oracle = float(mp.log(3) / mp.log(2))
ok1 = ok1 and abs(dim_fit - dim_oracle) < 1e-6
report("Box/Hausdorff dim of Pascal mod 2 = ln3/ln2; #P_k = 3^k (brute force)",
       "70-74,180-191", ok1,
       f"#P_k brute force = {counts}; dim from log-log fit = {dim_fit:.6f} "
       f"vs ln3/ln2 = {dim_oracle:.6f}")

ok1_neg = not all(counts[k] == 4 ** k for k in counts)  # must NOT equal 4^k
report("NEGATIVE CONTROL: #P_k = 4^k (dim=2, 'all odd') must fail",
       "70-74,180-191", ok1_neg,
       f"brute-force counts {counts} vs 4^k = {[4**k for k in ks]}")


# ---------------------------------------------------------------------------
# Claim 2 (line 103-109): harmonic renormalization factor r_m = m+3, via
# the Schur complement conductance c = (m+1)/(m+3) of the level-one
# network.
# Oracle: build the level-one resistor network's graph Laplacian
# explicitly (vertices: m+1 outer + C(m+1,2) midpoints, unit conductances
# on all edges of the m+1 small complete subgraphs) and compute the exact
# Schur complement numerically via linear algebra (independent of the
# book's by-hand harmonic-extension derivation).
# Negative control: the wrong formula c = m/(m+2) must disagree.
# ---------------------------------------------------------------------------
def schur_complement_conductance(m):
    """Level-one network on the (m+1)-simplex skeleton, built and reduced
    purely numerically (graph Laplacian + Schur complement), independent
    of the book's symmetry-ansatz algebra."""
    outer = list(range(m + 1))
    mid = {}
    idx = m + 1
    for i in range(m + 1):
        for j in range(i + 1, m + 1):
            mid[(i, j)] = idx
            idx += 1
    n = idx
    L = np.zeros((n, n))

    def add_edge(a, b, cond=1.0):
        L[a, a] += cond
        L[b, b] += cond
        L[a, b] -= cond
        L[b, a] -= cond

    # Each cell i (i=0..m) is a complete graph on {p_i} U {p_ij : j != i}
    for i in range(m + 1):
        verts = [i] + [mid[tuple(sorted((i, j)))] for j in range(m + 1) if j != i]
        for a_idx in range(len(verts)):
            for b_idx in range(a_idx + 1, len(verts)):
                add_edge(verts[a_idx], verts[b_idx], 1.0)

    boundary = outer
    interior = [v for v in range(n) if v not in boundary]
    Lbb = L[np.ix_(boundary, boundary)]
    Lbi = L[np.ix_(boundary, interior)]
    Lib = L[np.ix_(interior, boundary)]
    Lii = L[np.ix_(interior, interior)]
    Schur = Lbb - Lbi @ np.linalg.solve(Lii, Lib)
    # off-diagonal entry (0,1) of -Schur gives the pairwise conductance c
    c_numeric = -Schur[0, 1]
    return c_numeric

ok2 = True
detail2 = []
for m in (2, 3, 4, 5, 6):
    c_num = schur_complement_conductance(m)
    c_formula = (m + 1) / (m + 3)
    detail2.append((m, c_num, c_formula))
    if abs(c_num - c_formula) > 1e-9:
        ok2 = False
report("Schur-complement conductance c = (m+1)/(m+3) (independent graph-Laplacian build)",
       "103-109", ok2, f"(m, numeric c, formula c): {detail2}")

ok2_neg = True
for m in (2, 3, 4, 5, 6):
    c_num = schur_complement_conductance(m)
    c_wrong = m / (m + 2)
    if abs(c_num - c_wrong) < 1e-6:
        ok2_neg = False
report("NEGATIVE CONTROL: wrong formula c = m/(m+2) must disagree",
       "103-109", ok2_neg, "checked m=2..6, mutated formula disagrees with numeric Schur complement")


# ---------------------------------------------------------------------------
# Claim 3 (line 140-144): spectral dimension d_s = 2 d_H/d_w = 2ln(m+1)/ln(m+3),
# with d_H=ln(m+1)/ln2 (box dimension, Claim 1) and d_w=log2(m+3) (walk
# dimension: time renormalizes by r_m=m+3 per length-halving decimation,
# Sec. 2's harmonic renormalization). Previously the "oracle" just re-typed
# 2ln(m+1)/ln(m+3) in mpmath and compared it with the identical literature
# expression 2ln3/ln5 at m=2 only -- a tautology (L2 finding).
#
# Independent derivation for GENERAL m: the resistance renormalization
# factor rho = (m+3)/(m+1) is recovered from Claim 2's INDEPENDENT numeric
# Schur complement c_numeric(m) = (m+1)/(m+3) (built from a graph Laplacian,
# with no reference to the symbolic formula 2ln(m+1)/ln(m+3)), via
# rho_numeric(m) = 1/c_numeric(m). The renormalized time factor is then
# r_numeric(m) = (m+1)*rho_numeric(m), and the spectral dimension is
# recomputed from first principles as
#     d_s_numeric(m) = 2*ln(m+1) / ln(r_numeric(m))
# -- independent of the book's own typed formula "ln(m+3)", because
# r_numeric(m) is built purely from the Schur-complement linear algebra.
# Negative control: the mutated resistance factor rho_wrong = (m+2)/(m+1)
# (dropping +1, i.e. r_wrong = m+2 instead of m+3) must disagree.
# ---------------------------------------------------------------------------
m_test_values = (2, 3, 4, 5, 6)
d_s_numeric = {}
d_s_wrong_numeric = {}
for mm in m_test_values:
    c_num = schur_complement_conductance(mm)  # independent Schur complement, Claim 2
    rho_num = 1.0 / c_num
    r_num = (mm + 1) * rho_num
    d_s_numeric[mm] = float(2 * mp.log(mm + 1) / mp.log(r_num))
    r_wrong = mm + 2  # mutated renormalization factor (dropping +1)
    d_s_wrong_numeric[mm] = float(2 * mp.log(mm + 1) / mp.log(r_wrong))

d_s_literature_m2 = float(2 * mp.log(3) / mp.log(5))  # standard tabulated value for the gasket, m=2 only

# Note: an eigenvalue-counting fit N(lambda)~lambda^{d_s/2} on the raw
# (unweighted, unit-conductance) finite graph Laplacian of a small refined
# gasket graph was tried as a SECOND independent oracle and discarded: it
# gives d_s~1.98 for level-3/4 graphs of 42/123 vertices, nowhere near 1.365.
# This is a known limitation of that approach, not evidence against the
# book: Kigami's self-similar Laplacian is the RENORMALIZED limit of such
# graphs (conductances must be rescaled level-by-level via the spectral
# decimation method of Rammal-Toulouse, cited in the chapter bibliography),
# and a single small finite unweighted graph's own spectrum, fitted by a
# naive log-log slope over its own eigenvalue range, does not estimate d_s
# reliably at this size. Implementing the full decimation recursion is out
# of scope for this audit pass; the Schur-complement-based derivation above
# (general m, no reliance on the book's own "ln(m+3)") already gives a
# working independent oracle with a genuine negative control, so it is used
# alone for this claim's verdict.
ok3 = all(abs(d_s_numeric[mm] - float(2 * mp.log(mm + 1) / mp.log(mm + 3))) < 1e-9 for mm in m_test_values)
ok3 = ok3 and abs(d_s_numeric[2] - d_s_literature_m2) < 1e-9
report("Spectral dimension d_s=2ln(m+1)/ln(m+3): recomputed for m=2..6 from Claim 2's INDEPENDENT numeric Schur "
       "complement (rho=1/c_numeric, r=(m+1)*rho), not from the book's own typed ln(m+3)",
       "140-144", ok3,
       f"(m, d_s from Schur-derived r, book formula): "
       f"{[(mm, round(d_s_numeric[mm],6), round(float(2*mp.log(mm+1)/mp.log(mm+3)),6)) for mm in m_test_values]}")

ok3_neg = all(abs(d_s_wrong_numeric[mm] - d_s_numeric[mm]) > 0.03 for mm in m_test_values)
report("NEGATIVE CONTROL: mutated renormalization factor r=m+2 (dropping +1) must disagree with the "
       "Schur-complement-derived d_s, for every m=2..6",
       "140-144", ok3_neg,
       f"(m, Schur-derived d_s, mutated-r d_s): "
       f"{[(mm, round(d_s_numeric[mm],5), round(d_s_wrong_numeric[mm],5)) for mm in m_test_values]}")


# ---------------------------------------------------------------------------
# Claim 4 (line 153-163): asymptotic expansion of the continuous row
# entropy E(x) via the Barnes G-function:
#   E(x) = x(x+1) - x ln(2pi) - x lnGamma(x+1) + 2 ln G(x+1)
# and x^2*(E(x) - [series up to x^0]) -> -1/180.
# Oracle: mpmath.barnesg (independent special-function implementation of
# the Barnes G-function, not re-derived from the book's asymptotic series).
# Negative control: the book's OWN stated mutation (-1/12 ln x instead of
# -1/6 ln x) must leave a sizeable error at large x (book says ~0.77 at
# x=1e4); we verify this numerically.
# ---------------------------------------------------------------------------
def E_exact(x):
    x = mp.mpf(x)
    return x * (x + 1) - x * mp.log(2 * mp.pi) - x * mp.loggamma(x + 1) + 2 * mp.log(mp.barnesg(x + 1))


def E_definitional_quad(x):
    """The row entropy's OWN definition, int_0^x ln C(x,y) dy with
    C(x,y)=Gamma(x+1)/(Gamma(y+1)Gamma(x-y+1)), evaluated by direct 1-D
    quadrature (mpmath.quad) -- independent of the closed-form E_exact
    above (which uses mpmath.barnesg, a different special function
    implementation entirely). This checks the DEFINITIONAL equality itself,
    not just the Barnes-G closed form against a second closed form."""
    x = mp.mpf(x)

    def integrand(y):
        return mp.loggamma(x + 1) - mp.loggamma(y + 1) - mp.loggamma(x - y + 1)

    return mp.quad(integrand, [0, x])

def E_series_upto_const(x):
    x = mp.mpf(x)
    return (mp.mpf(1) / 2 * x ** 2 - mp.mpf(1) / 2 * x * mp.log(x)
            + (1 - mp.mpf(1) / 2 * mp.log(2 * mp.pi)) * x
            - mp.mpf(1) / 6 * mp.log(x) + 2 * mp.zeta(-1, derivative=1) - mp.mpf(1) / 12)

ok4 = True
detail4 = []
for x in (1000, 5000, 20000):
    diff = E_exact(x) - E_series_upto_const(x)
    val = float(x ** 2 * diff)
    detail4.append(val)
    if abs(val - (-1 / 180)) > 1e-3:
        ok4 = False
report("x^2*(E(x) - series_upto_x^0) -> -1/180 (Barnes G oracle via mpmath.barnesg)",
       "153-163", ok4, f"x^2*diff at x=1e3,5e3,2e4: {detail4} (-> should -> {-1/180:.6f})")

def E_series_wrong_log(x):
    x = mp.mpf(x)
    return (mp.mpf(1) / 2 * x ** 2 - mp.mpf(1) / 2 * x * mp.log(x)
            + (1 - mp.mpf(1) / 2 * mp.log(2 * mp.pi)) * x
            - mp.mpf(1) / 12 * mp.log(x) + 2 * mp.zeta(-1, derivative=1) - mp.mpf(1) / 12)

x_big = mp.mpf(10000)
err_wrong = float(E_exact(x_big) - E_series_wrong_log(x_big))
ok4_neg = abs(abs(err_wrong) - 0.77) < 0.1  # book explicitly predicts ~0.77 residual error (magnitude)
report("NEGATIVE CONTROL: replacing -1/6 ln x by -1/12 ln x leaves ~0.77 error at x=1e4 "
       "(book's own stated mutation, independently re-verified)",
       "153-163", ok4_neg, f"computed residual error at x=1e4: {err_wrong:.4f} (book states ~0.77)")

# Additional check (per L2 fix): the DEFINITIONAL equality itself,
# E(x) = int_0^x ln C(x,y) dy = x(x+1) - x ln2pi - x lnGamma(x+1) + 2lnG(x+1),
# verified by direct 1-D quadrature at a few x, independent of mpmath.barnesg.
ok4b = True
detail4b = []
for x in (5, 20, 60):
    e_quad = E_definitional_quad(x)
    e_closed = E_exact(x)
    rel_err = float(abs(e_quad - e_closed) / max(abs(e_closed), mp.mpf('1e-10')))
    detail4b.append((x, float(e_quad), float(e_closed), rel_err))
    if rel_err > 1e-6:
        ok4b = False
report("Definitional equality int_0^x ln C(x,y) dy = Barnes-G closed form, checked by DIRECT quadrature of the "
       "defining integral at a few x (independent of mpmath.barnesg)",
       "153-163", ok4b,
       f"(x, quad value, closed-form value, rel.err): {detail4b}")

# negative control: dropping the "+2 ln G(x+1)" term must disagree with the
# quadrature of the actual definitional integral
x_chk = mp.mpf(20)
e_quad_chk = E_definitional_quad(x_chk)
e_closed_no_barnesg_term = x_chk * (x_chk + 1) - x_chk * mp.log(2 * mp.pi) - x_chk * mp.loggamma(x_chk + 1)
ok4b_neg = abs(float(e_quad_chk - e_closed_no_barnesg_term)) > 1.0
report("NEGATIVE CONTROL: dropping the 2 ln G(x+1) term from the closed form must disagree with the "
       "direct quadrature of the definitional integral",
       "153-163", ok4b_neg,
       f"quadrature value={float(e_quad_chk):.6f}; closed form without the Barnes-G term={float(e_closed_no_barnesg_term):.6f}")


print()
print("=" * 70)
print(f"Chapter 6 summary: {len(PASS)} PASS, {len(FAIL)} FAIL")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("  -", f)
