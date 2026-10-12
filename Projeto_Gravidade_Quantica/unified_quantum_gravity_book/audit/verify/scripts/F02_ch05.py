"""
F-02 independent numerical audit -- Chapter 5
(chap05_interdimensional_transforms_barnes_lie.tex)

Every claim: independent oracle + negative control (mutated formula that
must fail). Read-only; does not edit the chapter.
"""
import numpy as np
from scipy import integrate
from scipy.signal import fftconvolve
from scipy.stats import beta as beta_dist
from math import gamma as Gamma

rng = np.random.default_rng(42)
PASS, FAIL = [], []


def report(name, line, ok, detail):
    (PASS if ok else FAIL).append(name)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} (book line ~{line})")
    print(f"       {detail}")


# ---------------------------------------------------------------------------
# Claim 1 (lines 258-291, Theorem "Barycentric Lipschitz Bound with Sharp
# Constant"): dist(Phi_a(c1),Phi_a(c2)) <= alpha/(alpha+m) dist(c1,c2), with
# equality for the identity grouping (n=m).
# Oracle: direct brute-force evaluation of Phi_alpha and the L1/2 distance
# on random simplex points and random groupings -- independent of the
# book's triangle-inequality algebra.
# Negative control: a mutated, over-tight constant alpha/(alpha+2m) must be
# VIOLATED by the exact identity-grouping case.
# ---------------------------------------------------------------------------
def dist_delta(c1, c2):
    return 0.5 * np.sum(np.abs(c1 - c2))


def Phi(c, groups, alpha, m):
    n = len(groups)
    out = np.zeros(n)
    for k, G in enumerate(groups):
        out[k] = (alpha * np.sum(c[G]) + len(G)) / (alpha + m)
    return out


def random_partition(m, n, rng):
    labels = rng.integers(0, n, size=m)
    while len(set(labels)) < n:
        labels = rng.integers(0, n, size=m)
    return [np.where(labels == k)[0] for k in range(n)]


m, n, alpha = 6, 3, 2.7
bound_ok = True
worst_ratio = 0.0
for _ in range(500):
    groups = random_partition(m, n, rng)
    c1 = rng.dirichlet(np.ones(m))
    c2 = rng.dirichlet(np.ones(m))
    p1, p2 = Phi(c1, groups, alpha, m), Phi(c2, groups, alpha, m)
    ratio_num = dist_delta(p1, p2)
    ratio_den = dist_delta(c1, c2)
    if ratio_den > 1e-12:
        r = ratio_num / ratio_den
        worst_ratio = max(worst_ratio, r)
    if ratio_num > alpha / (alpha + m) * ratio_den + 1e-9:
        bound_ok = False

# exact equality case: n = m, identity grouping
groups_id = [np.array([j]) for j in range(m)]
c1 = rng.dirichlet(np.ones(m))
c2 = rng.dirichlet(np.ones(m))
p1, p2 = Phi(c1, groups_id, alpha, m), Phi(c2, groups_id, alpha, m)
ratio_identity = dist_delta(p1, p2) / dist_delta(c1, c2)
equality_ok = abs(ratio_identity - alpha / (alpha + m)) < 1e-10

ok1 = bound_ok and equality_ok
report("Barycentric Lipschitz bound dist(Phi c1,Phi c2) <= alpha/(alpha+m) dist(c1,c2), sharp for n=m identity",
       "258-291", ok1,
       f"500 random (groups,c1,c2): max observed ratio={worst_ratio:.6f} <= alpha/(alpha+m)={alpha/(alpha+m):.6f}; "
       f"identity-grouping ratio={ratio_identity:.10f} (exact match required)")

wrong_const = alpha / (alpha + 2 * m)
ok1_neg = ratio_identity > wrong_const + 1e-9  # tighter wrong bound must be violated
report("NEGATIVE CONTROL: over-tight mutated constant alpha/(alpha+2m) must be violated by the exact identity case",
       "258-291", ok1_neg, f"identity ratio={ratio_identity:.6f} vs mutated constant={wrong_const:.6f}")


# ---------------------------------------------------------------------------
# Claim 2 (lines 144-154, Remark on gamma): the Fourier transform of the
# Beta-kernel decays EXACTLY like |k|^-1 in a facet-normal direction (gamma
# = 1 exactly, not faster).
# Oracle: direct 2D numerical quadrature (independent of the book's
# integration-by-parts argument) of the (complex) Fourier transform of the
# m=2 continuous Beta-kernel along the facet normal k=(k,0), with a log-log
# fit of the decay slope.
# Negative control: a mutated claim gamma=2 (decay ~|k|^-2) must disagree
# with the fitted slope.
# ---------------------------------------------------------------------------
ALPHA5 = 2.5


def binom2(y1, y2, alpha=ALPHA5):
    y3 = alpha - y1 - y2
    if y1 < -1e-12 or y2 < -1e-12 or y3 < -1e-12:
        return 0.0
    y3 = max(y3, 0.0)
    return Gamma(alpha + 1) / (Gamma(y1 + 1) * Gamma(y2 + 1) * Gamma(y3 + 1))


I_2d, _ = integrate.dblquad(lambda y2, y1: binom2(y1, y2), 0, ALPHA5,
                             lambda y1: 0, lambda y1: ALPHA5 - y1, epsabs=1e-11, epsrel=1e-11)


def K_hat(k1, k2):
    re, _ = integrate.dblquad(lambda y2, y1: binom2(y1, y2) * np.cos(k1 * y1 + k2 * y2) / I_2d,
                               0, ALPHA5, lambda y1: 0, lambda y1: ALPHA5 - y1,
                               epsabs=1e-9, epsrel=1e-8)
    im, _ = integrate.dblquad(lambda y2, y1: -binom2(y1, y2) * np.sin(k1 * y1 + k2 * y2) / I_2d,
                               0, ALPHA5, lambda y1: 0, lambda y1: ALPHA5 - y1,
                               epsabs=1e-9, epsrel=1e-8)
    return complex(re, im)


ks = [8.0, 16.0, 32.0, 64.0]
mags = [abs(K_hat(k, 0.0)) for k in ks]
log_k = np.log(ks)
log_mag = np.log(mags)
slope2 = np.polyfit(log_k, log_mag, 1)[0]

ok2 = -1.35 < slope2 < -0.65
report("Fourier decay of the m=2 Beta-kernel along the facet normal ~ |k|^-1 (gamma=1, direct 2D quadrature + log-log fit)",
       "144-154", ok2, f"|K_hat(k,0)| at k={ks}: {[f'{v:.3e}' for v in mags]}; fitted slope={slope2:.3f} (expect ~-1)")

ok2_neg = not (-2.3 < slope2 < -1.7)
report("NEGATIVE CONTROL: mutated claim gamma=2 (decay |k|^-2) must disagree with the fitted slope",
       "144-154", ok2_neg, f"fitted slope {slope2:.3f} is not compatible with a -2 decay")


# ---------------------------------------------------------------------------
# Claim 3 (lines 228-240, Proposition "Inversion"): hat h(k) = K_hat_alpha(-k)
# hat f(k), so f = IFFT[hat h(k) / K_hat_alpha(-k)] recovers f exactly (for
# the trivial case m=n, where R is plain convolution with the kernel).
# Oracle: an independent FFT-based discrete convolution/deconvolution on a
# fine grid (a numerical method entirely different from the book's Fourier
# analytic convolution-theorem proof).
# Negative control: dividing by K_hat_alpha(+k) (wrong sign; the kernel is
# NOT symmetric, since it is supported only on y >= 0) must fail to recover f.
# ---------------------------------------------------------------------------
Ngrid = 256
Ldom = 12.0
dxg = 2 * Ldom / Ngrid
xg = -Ldom + dxg * np.arange(Ngrid)
X1, X2 = np.meshgrid(xg, xg, indexing='ij')

f_true = np.exp(-(X1 ** 2 + X2 ** 2) / 2.0)

ALPHA3 = 2.0
Kgrid = np.zeros((Ngrid, Ngrid))
for i in range(Ngrid):
    for j in range(Ngrid):
        Kgrid[i, j] = binom2(xg[i], xg[j], ALPHA3) if (0 <= xg[i] <= ALPHA3 and 0 <= xg[j] <= ALPHA3 and xg[i] + xg[j] <= ALPHA3) else 0.0
I3 = np.sum(Kgrid) * dxg ** 2
Kgrid = Kgrid / I3  # normalized continuous kernel, sampled on the grid

# h(x) = integral K(y) f(x+y) dy = (K(-.) * f)(x): convolution with reflected kernel
Kref = Kgrid[::-1, ::-1]
h = fftconvolve(f_true, Kref, mode='same') * dxg ** 2

Fh = np.fft.fft2(h)
FK = np.fft.fft2(np.fft.ifftshift(Kgrid)) * dxg ** 2  # hat K(k), DFT convention aligned with the grid's own frequency grid
# hat K(-k) via conjugate-reversal trick on the DFT grid
FK_neg = np.conj(FK)  # valid since Kgrid is REAL: hatK(-k) = conj(hatK(k))

f_recovered = np.real(np.fft.ifft2(Fh / FK_neg))
err_correct = np.max(np.abs(f_recovered - f_true)) / np.max(f_true)

ok3 = err_correct < 0.03
report("Deconvolution f = IFFT[hat h(k)/K_hat(-k)] recovers f (independent FFT convolution/deconvolution on a fine grid)",
       "228-240", ok3, f"max relative error of recovered f vs true f = {err_correct:.4f}")

f_recovered_wrong = np.real(np.fft.ifft2(Fh / FK))  # wrong sign: divide by hat K(+k)
err_wrong = np.max(np.abs(f_recovered_wrong - f_true)) / np.max(f_true)
ok3_neg = err_wrong > 5 * err_correct
report("NEGATIVE CONTROL: dividing by hat K(+k) instead of hat K(-k) must fail to recover f (kernel not symmetric)",
       "228-240", ok3_neg, f"max relative error with wrong sign = {err_wrong:.4f} vs correct-sign error = {err_correct:.4f}")


# ---------------------------------------------------------------------------
# Claim 4 (lines 300-317, Theorem "Invariance and Spherical Harmonic
# Eigenfunctions", classical Siegel-Wishart result): scalar (m=1) special
# case. For X=1, G_{a,b} x^n = (a)_n/(a+b)_n, i.e. E[Y^n] for Y~Beta(a,b) is
# the Pochhammer ratio (a)_n/(a+b)_n.
# Oracle: Monte Carlo sampling from scipy.stats.beta (an independent
# implementation of the Beta law, unrelated to the book's Siegel integral
# derivation) and empirical moment estimation.
# Negative control: the mutated ratio (a)_n/(a+b+n)_n must disagree with the
# Monte Carlo estimate outside its statistical error bars.
# ---------------------------------------------------------------------------
def pochhammer_ratio(a, b, n):
    return (Gamma(a + n) / Gamma(a)) / (Gamma(a + b + n) / Gamma(a + b))


Nsamp = 4_000_000
ok4 = True
detail4 = []
for (a_par, b_par, n_pow) in [(2.3, 3.1, 1), (2.3, 3.1, 2), (4.0, 1.5, 3)]:
    samples = beta_dist.rvs(a_par, b_par, size=Nsamp, random_state=rng)
    mc_mean = np.mean(samples ** n_pow)
    mc_se = np.std(samples ** n_pow) / np.sqrt(Nsamp)
    formula = pochhammer_ratio(a_par, b_par, n_pow)
    detail4.append((a_par, b_par, n_pow, mc_mean, mc_se, formula))
    if abs(mc_mean - formula) > 6 * mc_se:
        ok4 = False

report("G_{a,b} x^n = (a)_n/(a+b)_n for X=1 (m=1 Siegel-Wishart special case = classical Beta moment, Monte Carlo oracle)",
       "300-317", ok4, f"(a,b,n,MC mean,MC s.e.,formula): {[(round(x,4) if isinstance(x,float) else x) for t in detail4 for x in t]}")

ok4_neg = True
for (a_par, b_par, n_pow, mc_mean, mc_se, formula) in detail4:
    wrong = pochhammer_ratio(a_par, b_par + n_pow, n_pow)  # mutated: (a)_n/(a+b+n)_n instead of (a)_n/(a+b)_n
    if abs(mc_mean - wrong) <= 6 * mc_se:
        ok4_neg = False
report("NEGATIVE CONTROL: mutated ratio (a)_n/(a+b+n)_n must disagree with the Monte Carlo moment estimates",
       "300-317", ok4_neg, "checked for all three (a,b,n) triples")


print()
print("=" * 70)
print(f"Chapter 5 summary: {len(PASS)} PASS, {len(FAIL)} FAIL")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("  -", f)
