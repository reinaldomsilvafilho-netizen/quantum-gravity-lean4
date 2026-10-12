"""
F-02 independent numerical audit -- Chapter 11
(chap11_emergent_spacetime_tensor_networks_holonomies.tex)

Every claim: independent oracle + negative control (mutated formula that
must fail). Read-only; does not edit the chapter. Includes a dimensional
check and CODATA order-of-magnitude estimate for the one dimensionful
physical quantity in the chapter (the Planck length in the LQG area
spectrum, eq. area_spectrum).
"""
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.linalg import solve_continuous_lyapunov
from scipy.constants import hbar, G, c, physical_constants

rng = np.random.default_rng(99)
PASS, FAIL = [], []


def report(name, line, ok, detail):
    (PASS if ok else FAIL).append(name)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} (book line ~{line})")
    print(f"       {detail}")


# ---------------------------------------------------------------------------
# Claim 1 (lines 156-159, Remark "SLD versus Kubo-Mori"): in an eigenbasis
# of rho0 = diag(p), g^BKM(X,X) >= g^SLD(X,X) for every traceless Hermitian
# X, with equality iff [rho0,X]=0 (X diagonal in that basis).
# Oracle: direct numerical evaluation of the two stated closed-form sums
# over many random (p, X) -- independent of the book's logarithmic-mean <=
# arithmetic-mean argument.
# Negative control: the reversed inequality g^SLD >= g^BKM must fail for
# generic non-commuting X.
# ---------------------------------------------------------------------------
def logmean(a, b):
    if abs(a - b) < 1e-13 * max(a, b, 1e-300):
        return a
    return (a - b) / (np.log(a) - np.log(b))


def g_sld(p, X):
    d = len(p)
    total = 0.0
    for i in range(d):
        for j in range(d):
            total += (2.0 / (p[i] + p[j])) * abs(X[i, j]) ** 2
    return total


def g_bkm(p, X):
    d = len(p)
    total = 0.0
    for i in range(d):
        for j in range(d):
            total += (1.0 / logmean(p[i], p[j])) * abs(X[i, j]) ** 2
    return total


d_dim = 4
ineq_ok = True
for _ in range(300):
    p = rng.dirichlet(np.ones(d_dim))
    H = rng.standard_normal((d_dim, d_dim)) + 1j * rng.standard_normal((d_dim, d_dim))
    H = (H + H.conj().T) / 2
    X = H - np.trace(H).real / d_dim * np.eye(d_dim)
    sld = g_sld(p, X)
    bkm = g_bkm(p, X)
    if bkm < sld - 1e-9:
        ineq_ok = False

p_eq = rng.dirichlet(np.ones(d_dim))
X_diag = np.diag(rng.standard_normal(d_dim) - np.mean(rng.standard_normal(d_dim)))
X_diag = X_diag - np.trace(X_diag).real / d_dim * np.eye(d_dim)
sld_eq, bkm_eq = g_sld(p_eq, X_diag), g_bkm(p_eq, X_diag)

ok1 = ineq_ok and abs(sld_eq - bkm_eq) < 1e-9 * max(1, abs(sld_eq))
report("g^BKM(X,X) >= g^SLD(X,X) always, with equality for diagonal (commuting) X (direct evaluation, 300 random trials)",
       "156-159", ok1, f"inequality held in all 300 random trials: {ineq_ok}; commuting-case equality: SLD={sld_eq:.6f}, BKM={bkm_eq:.6f}")

reversed_violations = 0
for _ in range(50):
    p = rng.dirichlet(np.ones(d_dim))
    H = rng.standard_normal((d_dim, d_dim)) + 1j * rng.standard_normal((d_dim, d_dim))
    H = (H + H.conj().T) / 2
    X = H - np.trace(H).real / d_dim * np.eye(d_dim)
    if g_sld(p, X) < g_bkm(p, X) - 1e-9:
        reversed_violations += 1
ok1_neg = reversed_violations > 40
report("NEGATIVE CONTROL: the reversed inequality g^SLD >= g^BKM fails for most generic non-commuting X",
       "156-159", ok1_neg, f"reversed inequality violated in {reversed_violations}/50 generic random trials (should be most of them)")


# ---------------------------------------------------------------------------
# Additional cross-check (per L2 fix): the eigenbasis closed-form sums for
# g^SLD and g^BKM used throughout this script are themselves checked against
# their DEFINING equations, independent of the sum formulas:
#   - g^SLD(X,X) = Tr(X L), where L solves the (continuous) Lyapunov equation
#     rho L + L rho = 2X (the defining equation of the symmetric logarithmic
#     derivative), solved here by scipy.linalg.solve_continuous_lyapunov --
#     an independent linear-algebra solver, not the eigenbasis sum.
#   - g^BKM(X,X) = Tr(X, int_0^inf (rho+s)^-1 X (rho+s)^-1 ds), using the
#     integral representation 1/logmean(a,b) = int_0^inf ds/((a+s)(b+s)),
#     evaluated here by direct numerical quadrature (scipy.integrate.quad)
#     of the resolvent integral, not the eigenbasis sum.
# ---------------------------------------------------------------------------
rng_cross = np.random.default_rng(42)
p_cross = rng_cross.dirichlet(np.ones(d_dim))
rho_cross = np.diag(p_cross).astype(complex)
X_cross = sample_traceless_hermitian = None
H_cross = rng_cross.standard_normal((d_dim, d_dim)) + 1j * rng_cross.standard_normal((d_dim, d_dim))
H_cross = (H_cross + H_cross.conj().T) / 2
X_cross = H_cross - np.trace(H_cross).real / d_dim * np.eye(d_dim)

sld_sum = g_sld(p_cross, X_cross)
bkm_sum = g_bkm(p_cross, X_cross)

# Lyapunov equation: rho @ L + L @ rho = 2*X_cross (rho Hermitian = rho^H)
L_lyap = solve_continuous_lyapunov(rho_cross, 2 * X_cross)
sld_lyap = np.trace(X_cross @ L_lyap).real

# resolvent integral for BKM: Tr(X (rho+s)^-1 X (rho+s)^-1) integrated over s
I_mat = np.eye(d_dim)


def bkm_integrand(s):
    Rinv = np.diag(1.0 / (p_cross + s))
    M = Rinv @ X_cross @ Rinv @ X_cross
    return np.trace(M).real


bkm_quad, _ = quad(bkm_integrand, 0, np.inf, limit=200)

ok1b = abs(sld_lyap - sld_sum) < 1e-9 * max(1, abs(sld_sum)) and abs(bkm_quad - bkm_sum) < 1e-6 * max(1, abs(bkm_sum))
report("Cross-check: the eigenbasis SLD/BKM sums agree with their DEFINING equations -- the continuous Lyapunov "
       "equation rho*L+L*rho=2X for SLD, and the resolvent integral int_0^inf (rho+s)^-1 X (rho+s)^-1 ds for BKM "
       "(independent of the eigenbasis-sum formulas used elsewhere in this script)",
       "156-159", ok1b,
       f"g_SLD: eigenbasis sum={sld_sum:.10f} vs Lyapunov-equation value={sld_lyap:.10f}; "
       f"g_BKM: eigenbasis sum={bkm_sum:.10f} vs resolvent-quadrature value={bkm_quad:.10f}")

# negative control: solving the WRONG Lyapunov equation rho@L - L@rho = 2X
# (sign flip) must disagree with the eigenbasis SLD sum
try:
    L_wrong = solve_continuous_lyapunov(rho_cross, 2 * X_cross) if False else None
except Exception:
    L_wrong = None
# build the sign-flipped equation directly: this is solve_continuous_lyapunov
# for A=rho, Q=2X but applied to the ANTI-symmetrized map rho@L - L@rho,
# which is singular/ill-posed for Hermitian rho (no unique solution acting
# the same way) -- use instead a clearly wrong closed form: Tr(X, 2*inv(rho)*X)
# as the mutated "SLD-like" quantity (replacing the Lyapunov solve by a
# naive single-resolvent guess)
sld_wrong_guess = np.trace(X_cross @ (2 * np.linalg.inv(rho_cross) @ X_cross)).real
ok1b_neg = abs(sld_wrong_guess - sld_sum) > 0.1 * max(1, abs(sld_sum))
report("NEGATIVE CONTROL: a naive mutated guess Tr(X, 2*rho^-1*X) (not solving the actual Lyapunov equation) "
       "must disagree with the eigenbasis SLD sum",
       "156-159", ok1b_neg,
       f"eigenbasis SLD sum={sld_sum:.10f}; mutated naive guess={sld_wrong_guess:.10f}")


# ---------------------------------------------------------------------------
# Claim 2 (line 158, Remark): qutrit (d=3) numerical check -- for rho0 drawn
# from the Hilbert-Schmidt measure and random traceless Hermitian X, the
# ratio g^BKM/g^SLD has median ~1.16, and about 95% of samples lie below
# 1.61 (the book's CURRENT, corrected statement -- F02_ch11.py previously
# tested the stale pre-correction wording "95th percentile < 1.6", which the
# book no longer states; see audit/verify/L2_F02.md).
# Oracle: independent Monte Carlo simulation using the standard
# Ginibre-matrix construction of the Hilbert-Schmidt measure
# (rho = GG^dagger / Tr(GG^dagger) for G a d x d complex Ginibre matrix),
# unrelated to any formula the book quotes for the ratio's statistics.
# Negative control: a naive UNIFORM-eigenvalue ensemble (p ~ Dirichlet(1,..,1)
# with HAAR eigenvectors only, i.e. NOT the Ginibre/HS construction) gives a
# visibly different median, showing the specific HS measure matters. A
# SECOND negative control uses the mutated threshold 1.55 (instead of 1.61):
# "about 95% of samples below 1.55" must fail against the same simulation.
# ---------------------------------------------------------------------------
def sample_hs_rho(d, rng):
    G_mat = rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))
    M = G_mat @ G_mat.conj().T
    return M / np.trace(M).real


def sample_traceless_hermitian(d, rng):
    H = rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))
    H = (H + H.conj().T) / 2
    return H - np.trace(H).real / d * np.eye(d)


def ratio_trial(d, rng, rho_sampler):
    rho = rho_sampler(d, rng)
    p, U = np.linalg.eigh(rho)
    p = np.clip(p, 1e-12, None)
    X = sample_traceless_hermitian(d, rng)
    X_eig = U.conj().T @ X @ U
    sld = g_sld(p, X_eig)
    bkm = g_bkm(p, X_eig)
    return bkm / sld


n_mc = 200000
ratios_hs = np.array([ratio_trial(3, rng, sample_hs_rho) for _ in range(n_mc)])
median_hs = np.median(ratios_hs)
p95_hs = np.percentile(ratios_hs, 95)
frac_below_161 = np.mean(ratios_hs < 1.61)
frac_below_155 = np.mean(ratios_hs < 1.55)  # for the negative control below

ok2 = abs(median_hs - 1.16) < 0.03 and abs(frac_below_161 - 0.95) < 0.01
report("Qutrit Hilbert-Schmidt Monte Carlo: median(BKM/SLD) ~ 1.16, about 95% of samples below 1.61 (book's current "
       "text) -- independent Ginibre-matrix simulation",
       "158", ok2,
       f"{n_mc} trials: median={median_hs:.4f} (book: ~1.16); fraction below 1.61 = {frac_below_161:.4f} "
       f"(book: ~0.95); 95th percentile = {p95_hs:.4f}")

ok2_neg_threshold = abs(frac_below_155 - 0.95) > 0.01
report("NEGATIVE CONTROL: the mutated threshold 1.55 ('95% below 1.55') must disagree with the simulation",
       "158", ok2_neg_threshold,
       f"fraction below the mutated threshold 1.55 = {frac_below_155:.4f} (should be well short of 0.95)")


def sample_uniform_eig_rho(d, rng):
    p = rng.dirichlet(np.ones(d))
    # Haar-random eigenvectors via QR of a complex Ginibre matrix
    Z = rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))
    Q, R = np.linalg.qr(Z)
    phases = np.diag(R) / np.abs(np.diag(R))
    Q = Q * phases
    return Q @ np.diag(p) @ Q.conj().T


ratios_uniform = np.array([ratio_trial(3, rng, sample_uniform_eig_rho) for _ in range(n_mc)])
median_uniform = np.median(ratios_uniform)
ok2_neg = abs(median_uniform - 1.16) > 0.03
report("NEGATIVE CONTROL: a uniform-eigenvalue (non-Hilbert-Schmidt) ensemble gives a visibly different median ratio",
       "158", ok2_neg, f"uniform-eigenvalue median={median_uniform:.4f} vs Hilbert-Schmidt median={median_hs:.4f} (book: ~1.16)")


# ---------------------------------------------------------------------------
# Claim 3 (lines 235-241, Proposition "Min-cut bound"): S_A <= |C| log(chi)
# for a tensor-network state with a cut of |C| bonds of dimension chi.
# Oracle: explicit construction of a small random MPS chain (3 sites,
# bond dimension chi across a single cut, |C|=1) via numpy einsum, with the
# entanglement entropy computed by direct SVD of the state -- an
# independent linear-algebra computation, not the book's Schmidt-rank
# counting argument.
#
# L2 fix: the ORIGINAL construction used A = {site 1} alone with physical
# dimension d_phys = chi = 5, so dim H_A = chi already, and S_A <= log(chi)
# followed trivially from dim H_A = chi regardless of the min-cut theorem
# (not discriminating). Here A = {site 1, site 2} (dim H_A = d^2 = 9) and
# B = {site 3} (dim H_B = d = 3), separated by a SINGLE cut of bond
# dimension chi = 2 (|C| = 1). Since dim H_A = 9 > chi = 2 and
# dim H_B = 3 > chi = 2, the dimension bound log(9) (or log(3)) is NOT
# binding -- only the actual min-cut/bond-dimension bound log(2) can be;
# the test genuinely exercises the min-cut theorem rather than the trivial
# Schmidt-rank-vs-dimension fact.
# Negative control: an artificially tightened bound log(chi) - 0.3 must be
# violated when the tensors are chosen to nearly saturate the bound.
# ---------------------------------------------------------------------------
def mps_entropy(chi, d_phys, chi_internal, rng, saturate=False):
    """3-site chain, bond dims (chi_internal between sites 1-2, chi between
    sites 2-3 = the single cut separating A={1,2} from B={3}). chi_internal
    is NOT the cut and does not enter the min-cut bound at all -- it is
    present only so that A has nontrivial internal structure (dim H_A =
    d_phys^2, unconstrained by chi)."""
    if saturate:
        # choose the CUT tensor T2 close to a maximally-entangling isometry
        # (on the (chi_internal*d_phys) x chi matricization) to approach
        # the bound log(chi) as closely as possible
        shape2 = (chi_internal, d_phys, chi)
        base = np.zeros((chi_internal * d_phys, chi), dtype=complex)
        for i in range(min(chi_internal * d_phys, chi)):
            base[i, i] = 1.0
        T2 = base.reshape(shape2) + 0.05 * (rng.standard_normal(shape2) + 1j * rng.standard_normal(shape2))
    else:
        T2 = rng.standard_normal((chi_internal, d_phys, chi)) + 1j * rng.standard_normal((chi_internal, d_phys, chi))
    T1 = rng.standard_normal((d_phys, chi_internal)) + 1j * rng.standard_normal((d_phys, chi_internal))
    T3 = rng.standard_normal((chi, d_phys)) + 1j * rng.standard_normal((chi, d_phys))
    Psi = np.einsum('ia,ajb,bk->ijk', T1, T2, T3)  # i=site1, j=site2 (both in A), k=site3 (B)
    PsiA = Psi.reshape(d_phys * d_phys, d_phys)  # rows: combined A index (i,j); cols: B index k
    PsiA = PsiA / np.linalg.norm(PsiA)
    s = np.linalg.svd(PsiA, compute_uv=False)
    p = s ** 2
    p = p[p > 1e-14]
    p = p / p.sum()
    return -np.sum(p * np.log(p)), len(p)


chi_t, dphys_t, chi_int_t = 2, 3, 4
dimHA, dimHB = dphys_t ** 2, dphys_t
assert dimHA > chi_t and dimHB > chi_t, "dimension bound must NOT be the binding constraint"
ent_random, rank_random = mps_entropy(chi_t, dphys_t, chi_int_t, rng, saturate=False)
ent_sat, rank_sat = mps_entropy(chi_t, dphys_t, chi_int_t, rng, saturate=True)
bound = np.log(chi_t)

ok3 = (ent_random <= bound + 1e-9) and (ent_sat <= bound + 1e-9) and (ent_sat > 0.75 * bound) and rank_random <= chi_t and rank_sat <= chi_t
report("MPS min-cut bound S_A <= |C| log(chi) holds for random and near-saturating tensors, with dim H_A=9 > "
       "chi=2 and dim H_B=3 > chi=2 so the bound is NOT implied by the dimension alone (independent SVD-based "
       "entropy)",
       "235-241", ok3, f"log(chi)={bound:.4f}; dim H_A={dimHA}, dim H_B={dimHB} (both > chi={chi_t}); "
       f"random-tensor S_A={ent_random:.4f} (rank {rank_random}); "
       f"near-saturating S_A={ent_sat:.4f} (rank {rank_sat}, should approach the bound)")

wrong_bound = bound - 0.3
ok3_neg = ent_sat > wrong_bound
report("NEGATIVE CONTROL: artificially tightened bound log(chi)-0.3 is violated by the near-saturating construction",
       "235-241", ok3_neg, f"near-saturating S_A={ent_sat:.4f} vs mutated tightened bound={wrong_bound:.4f}")

# second negative control: using the dimension-only bound log(dim H_A)=log(9)
# in place of the min-cut bound log(chi)=log(2) would be satisfied trivially
# and would NOT discriminate -- confirm the min-cut bound is strictly
# tighter here, so the test is not vacuous
ok3_neg2 = bound < np.log(dimHA) - 0.5
report("NEGATIVE CONTROL (non-vacuity check): the min-cut bound log(chi) must be strictly tighter than the "
       "dimension-only bound log(dim H_A), otherwise this test would not discriminate the two",
       "235-241", ok3_neg2, f"log(chi)={bound:.4f} vs log(dim H_A)={np.log(dimHA):.4f} (must be strictly smaller)")


# ---------------------------------------------------------------------------
# Claim 4 (lines 296-300, Proposition "Discrete holonomies", item 1): the
# MIDPOINT-rule discretization of a Wilson line converges with error
# O(k^-2) (one order better than the naive endpoint rule of Chapter 2,
# which is O(k^-1)).
# Oracle: independent high-accuracy ODE integration (solve_ivp) of the
# exact SU(2) parallel transport dU/ds = A(s)U(s), compared against the
# explicit midpoint-rule discrete product for increasing k, with a
# log-log fit of the convergence rate.
# Negative control: fitting the NAIVE (non-midpoint, left-endpoint) rule
# used in Chapter 2 on the SAME connection must give a visibly worse
# (O(k^-1), i.e. slope ~-1, not ~-2) rate, confirming the two propositions
# describe genuinely different convergence orders.
# ---------------------------------------------------------------------------
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)


def Afun11(s):
    # anti-Hermitian su(2)-valued connection (so exp(.) in SU(2))
    return 1j * (0.6 * np.sin(2 * np.pi * s) * sx + 0.5 * np.cos(2 * np.pi * s) * sy + 0.3 * sz)


def ode_U11(s, Uvec):
    U = Uvec.reshape(2, 2)
    dU = Afun11(s) @ U
    return dU.reshape(-1)


sol_U11 = solve_ivp(ode_U11, [0, 1], np.eye(2, dtype=complex).reshape(-1), method='RK45', rtol=1e-13, atol=1e-14)
U_exact11 = sol_U11.y[:, -1].reshape(2, 2)
Z_exact11 = np.trace(U_exact11)

from scipy.linalg import expm

ks11 = [10, 20, 40, 80, 160]
errs_mid, errs_naive = [], []
for kk in ks11:
    Uk_mid = np.eye(2, dtype=complex)
    Uk_naive = np.eye(2, dtype=complex)
    for j in range(1, kk + 1):
        s_left = (j - 1) / kk
        s_mid = (j - 0.5) / kk
        Aj_mid = expm(Afun11(s_mid) / kk)
        Aj_naive = np.eye(2, dtype=complex) + Afun11(s_left) / kk
        Uk_mid = Aj_mid @ Uk_mid
        Uk_naive = Aj_naive @ Uk_mid * 0 + Aj_naive @ Uk_naive  # keep naive product independent
    errs_mid.append(abs(np.trace(Uk_mid) - Z_exact11))
    errs_naive.append(abs(np.trace(Uk_naive) - Z_exact11))

slope_mid = np.polyfit(np.log(ks11), np.log(errs_mid), 1)[0]
slope_naive = np.polyfit(np.log(ks11), np.log(errs_naive), 1)[0]

ok4 = (-2.4 < slope_mid < -1.6) and (-1.4 < slope_naive < -0.6) and (slope_mid < slope_naive - 0.4)
report("Midpoint-rule holonomy product converges as O(k^-2), strictly faster than the naive O(k^-1) rule (same connection)",
       "296-300", ok4, f"midpoint errors at k={ks11}: {[f'{e:.2e}' for e in errs_mid]}, slope={slope_mid:.3f} (expect ~-2); "
       f"naive errors: {[f'{e:.2e}' for e in errs_naive]}, slope={slope_naive:.3f} (expect ~-1)")

ok4_neg = not (-2.4 < slope_naive < -1.6)
report("NEGATIVE CONTROL: claiming the naive (non-midpoint) rule is ALSO O(k^-2) is contradicted by its fitted slope",
       "296-300", ok4_neg, f"naive rule fitted slope={slope_naive:.3f}, not compatible with a -2 (k^-2) decay")


# ---------------------------------------------------------------------------
# Claim 5 (line 304, eq:area_spectrum): dimensional check and CODATA
# order-of-magnitude estimate for the Planck length l_P^2 = G_N*hbar
# (geometrized units, c=1) entering the LQG area spectrum. We check that
# in SI units l_P = sqrt(hbar*G/c^3) reproduces the standard CODATA Planck
# length (~1.616e-35 m), and verify the dimensional exponents of mass,
# length, time explicitly cancel to give [length]^2 for hbar*G/c^3.
# Oracle: scipy.constants' independently tabulated CODATA 'Planck length'
# entry, plus explicit SI-unit dimensional-exponent bookkeeping.
# Negative control: the mutated combination hbar*G/c^2 (wrong power of c)
# does NOT have dimensions of length^2 and does not match the Planck length.
# ---------------------------------------------------------------------------
lP_from_formula = np.sqrt(hbar * G / c ** 3)
lP_codata, lP_unit, lP_unc = physical_constants['Planck length']

ok5a = abs(lP_from_formula - lP_codata) / lP_codata < 1e-6

# dimensional bookkeeping: units (mass M, length L, time T) exponents
# [hbar] = M L^2 T^-1 ; [G] = M^-1 L^3 T^-2 ; [c] = L T^-1
hbar_dim = np.array([1, 2, -1])
G_dim = np.array([-1, 3, -2])
c_dim = np.array([0, 1, -1])
combo_dim = hbar_dim + G_dim - 3 * c_dim  # hbar*G/c^3
ok5b = np.array_equal(combo_dim, np.array([0, 2, 0]))  # pure L^2, mass and time cancel

ok5 = ok5a and ok5b
report("l_P = sqrt(hbar G/c^3) matches CODATA Planck length (~1.616e-35 m); dimensional exponents of hbar*G/c^3 = L^2 exactly",
       "304", ok5, f"computed l_P={lP_from_formula:.6e} m vs CODATA={lP_codata:.6e} m; "
       f"dimension exponents (mass,length,time) of hbar*G/c^3 = {tuple(combo_dim)} (expect (0,2,0))")

combo_dim_wrong = hbar_dim + G_dim - 2 * c_dim  # hbar*G/c^2 (wrong power)
lP_wrong_formula = np.sqrt(hbar * G / c ** 2)
ok5_neg = (not np.array_equal(combo_dim_wrong, np.array([0, 2, 0]))) and \
          (abs(lP_wrong_formula - lP_codata) / lP_codata > 1e-3)
report("NEGATIVE CONTROL: mutated combination hbar*G/c^2 is NOT dimensionless-length^2 and numerically misses the Planck length",
       "304", ok5_neg, f"dimension exponents of hbar*G/c^2 = {tuple(combo_dim_wrong)} (not (0,2,0)); "
       f"numeric value sqrt(hbar G/c^2)={lP_wrong_formula:.6e} m vs CODATA Planck length={lP_codata:.6e} m")


print()
print("=" * 70)
print(f"Chapter 11 summary: {len(PASS)} PASS, {len(FAIL)} FAIL")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("  -", f)
