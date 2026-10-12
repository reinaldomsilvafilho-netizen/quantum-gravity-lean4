r"""l1_ch4_mi.py -- independent check of the modulational-instability criterion, book ch. 4.

Source: chap04_simplicial_waves_porous_transport.tex, Theorem "Simplicial Modulational
Instability" (no \label), Section "Modulational Instability".

Book claim (focusing, kappa > 0, c := kappa p rho0^p > 0, eps := hbar^2 sigma(k) / (2M)):
  (D) hbar^2 Omega^2(k) = eps (eps - 2c);
  (C) "the plane wave is modulationally unstable (Omega^2 < 0) for wavevectors satisfying
       sigma(k) < 4 M c / hbar^2";
  (G) max growth rate gamma_max = c / hbar, attained where sigma = 2Mc/hbar^2.

Finding under adjudication: (C) omits 0 < sigma; at k = 0, sigma(0) = 0 < 4Mc/hbar^2 but
Omega^2 = 0, which is not < 0.  Since sigma >= 0 always and sigma(k) > 0 for k != 0, the
corrected criterion is: Omega^2 < 0  <=>  k != 0 and sigma(k) < 4Mc/hbar^2.

Oracle (independent of the book's derivation): m = 2 (x in R), alpha = 1.5.
  * sigma(k) computed by quadrature of the DEFINITION of the operator applied to cos(kx)
    (second difference against the continuous binomial kernel on [0, alpha]);
  * the 2x2 real Jacobian of the full nonlinear NLSE right-hand side (rotating frame) at the
    plane wave, obtained by central finite differences of the nonlinearity |psi|^{2p} psi,
    with p = 1.5 (non-integer, so no polynomial shortcut); its eigenvalues lambda give
    Omega^2 = -lambda^2.
Negative controls (must FAIL): (N1) dispersion with +2c; (N2) criterion with threshold
2Mc/hbar^2 stated as an iff; (N3) growth rate 2c/hbar.
Dimensionless units hbar = M = 1 (the book's convention: sigma in units of l0^-2, so
hbar^2 sigma / 2M and kappa rho0^p are both energies; the check is purely algebraic).
"""
import sys
import numpy as np
from scipy.integrate import quad
from scipy.special import gammaln

ALPHA = 1.5
HBAR, MASS = 1.0, 1.0
P, RHO0 = 1.5, 0.8

fails = []


def report(name, ok, detail, control=False):
    ok = bool(ok)
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {'(control) ' if control else ''}{name}: {detail}")
    if control and ok:
        fails.append("control passed: " + name)
    if not control and not ok:
        fails.append(name)


def kernel(y):
    # continuous binomial Gamma(a+1) / (Gamma(y+1) Gamma(a-y+1)), m = 2
    return np.exp(gammaln(ALPHA + 1) - gammaln(y + 1) - gammaln(ALPHA - y + 1))


I_NORM = quad(kernel, 0.0, ALPHA)[0]


def minus_lap_cos(k):
    """(-Delta)cos(k x) at x = 0, from the definition (second difference)."""
    f = lambda y: kernel(y) * (np.cos(k * y) - 2.0 + np.cos(-k * y))
    val = quad(f, 0.0, ALPHA, limit=200)[0] / (2 * ALPHA**2 * I_NORM)
    return -val


def jacobian(k, kappa):
    """Real 2x2 Jacobian d/dt (u, v) of the rotating-frame NLSE at the plane wave."""
    mu0 = -kappa * RHO0**P
    s = minus_lap_cos(k)
    J = np.zeros((2, 2))
    h = 1e-6
    for col, dirn in enumerate([1.0, 1j]):
        def rhs(d):
            psi = np.sqrt(RHO0) + d * dirn          # value at x = 0 of the perturbed field
            lin = (HBAR**2 / (2 * MASS)) * s * d * dirn  # -(hbar^2/2M) Delta acting on the mode
            nonlin = -kappa * abs(psi) ** (2 * P) * psi
            return (lin + nonlin - mu0 * psi) / (1j * HBAR)
        dF = (rhs(h) - rhs(-h)) / (2 * h)
        J[0, col], J[1, col] = dF.real, dF.imag
    return J, s


def omega2_oracle(k, kappa):
    J, s = jacobian(k, kappa)
    lam = np.linalg.eigvals(J)
    # Omega = i lambda  =>  Omega^2 = -lambda^2 ; both eigenvalues give the same value
    om2 = -(lam[0] ** 2)
    return om2.real, abs(om2.imag), s


# ---------- sigma sanity: sigma(0)=0, 0 < sigma <= 2/alpha^2 for k != 0 ----------
ks = np.concatenate([[0.0], np.linspace(0.05, 40.0, 800)])
sig = np.array([minus_lap_cos(k) for k in ks])
supsig = sig.max()
report("sigma(0) = 0", abs(sig[0]) < 1e-12, f"sigma(0) = {sig[0]:.3e}")
report("0 < sigma(k) <= 2/alpha^2 for k != 0", (sig[1:] > 0).all() and (sig <= 2 / ALPHA**2 + 1e-12).all(),
       f"min_k!=0 = {sig[1:].min():.4e}, max = {supsig:.6f}, 2/alpha^2 = {2/ALPHA**2:.6f}")

# choose kappa so that 2Mc/hbar^2 < sup sigma < 4Mc/hbar^2 is NOT forced: take 4Mc/hbar^2 = 0.8 sup
c = 0.8 * supsig * HBAR**2 / (4 * MASS)
kappa = c / (P * RHO0**P)
thr4 = 4 * MASS * c / HBAR**2
thr2 = 2 * MASS * c / HBAR**2
print(f"alpha = {ALPHA}, p = {P}, rho0 = {RHO0}, kappa = {kappa:.6f}, c = {c:.6f}, "
      f"4Mc/hbar^2 = {thr4:.6f}, sup sigma (grid) = {supsig:.6f}")

om2 = []
maxdev = 0.0
maxdev_mut = 0.0
for k, s in zip(ks, sig):
    o2, im, s2 = omega2_oracle(k, kappa)
    om2.append(o2)
    eps = HBAR**2 * s / (2 * MASS)
    book = eps * (eps - 2 * c) / HBAR**2
    mut = eps * (eps + 2 * c) / HBAR**2
    maxdev = max(maxdev, abs(o2 - book))
    maxdev_mut = max(maxdev_mut, abs(o2 - mut))
om2 = np.array(om2)

# (D) dispersion relation
report("(D) hbar^2 Omega^2 = eps(eps - 2c) vs Jacobian oracle", maxdev < 1e-6, f"max |diff| = {maxdev:.3e}")
report("(N1) mutated dispersion eps(eps + 2c)", maxdev_mut < 1e-6, f"max |diff| = {maxdev_mut:.3e}", control=True)

# (C) book criterion, literal: sigma < 4Mc/hbar^2  =>  Omega^2 < 0
lit_viol = [(k, s, o) for k, s, o in zip(ks, sig, om2) if s < thr4 and not (o < -1e-12)]
print(f"book literal criterion: {len(lit_viol)} violation(s); first: "
      + (f"k = {lit_viol[0][0]}, sigma = {lit_viol[0][1]:.3e}, Omega^2 = {lit_viol[0][2]:.3e}" if lit_viol else "none"))
lit_ok = len(lit_viol) == 0
print(f"[{'HOLDS' if lit_ok else 'FALSE'}] (C-literal) book criterion as printed "
      f"(expected FALSE, exactly at k = 0)")
if lit_ok or any(k != 0.0 for k, _, _ in lit_viol):
    fails.append("C-literal: expected exactly one violation, at k = 0")

# (C') corrected criterion: Omega^2 < 0  <=>  0 < sigma < 4Mc/hbar^2 (i.e. k != 0)
pred = (sig > 0) & (sig < thr4)
unst = om2 < -1e-12
report("(C') Omega^2 < 0 <=> 0 < sigma(k) < 4Mc/hbar^2", (pred == unst).all(),
       f"{int(unst.sum())} unstable / {len(ks)} grid points, mismatches = {int((pred != unst).sum())}")
pred2 = (sig > 0) & (sig < thr2)
report("(N2) mutated iff with threshold 2Mc/hbar^2", (pred2 == unst).all(),
       f"mismatches = {int((pred2 != unst).sum())}", control=True)

# all k != 0 unstable when sup sigma < 4Mc/hbar^2
c_big = 1.1 * supsig * HBAR**2 / (4 * MASS)
kap_big = c_big / (P * RHO0**P)
allu = all(omega2_oracle(k, kap_big)[0] < 0 for k in ks[1:])
report("every k != 0 unstable when 4Mc/hbar^2 > sup sigma", allu, f"c = {c_big:.6f}")

# (G) growth rate
gam = np.sqrt(np.maximum(-om2, 0.0))
# refine near the resonance sigma = 2Mc/hbar^2 by bisection on the oracle sigma
idx = int(np.argmax(sig > thr2))          # first grid point above the resonance level
lo, hi = ks[idx - 1], ks[idx]
for _ in range(60):
    mid = 0.5 * (lo + hi)
    if minus_lap_cos(mid) < thr2:
        lo = mid
    else:
        hi = mid
g_res = np.sqrt(max(-omega2_oracle(0.5 * (lo + hi), kappa)[0], 0.0))
report("(G) gamma_max = c/hbar attained at sigma = 2Mc/hbar^2",
       abs(g_res - c / HBAR) < 1e-6 and gam.max() <= c / HBAR + 1e-9,
       f"gamma(resonance) = {g_res:.9f}, grid max = {gam.max():.9f}, c/hbar = {c/HBAR:.9f}")
report("(N3) mutated gamma_max = 2c/hbar", abs(g_res - 2 * c / HBAR) < 1e-6,
       f"gamma(resonance) = {g_res:.9f} vs {2*c/HBAR:.9f}", control=True)

print("RESULT:", "ALL OK" if not fails else "FAILURES: " + "; ".join(fails))
sys.exit(1 if fails else 0)
