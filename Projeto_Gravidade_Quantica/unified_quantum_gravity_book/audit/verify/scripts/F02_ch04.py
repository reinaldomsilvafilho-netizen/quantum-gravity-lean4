"""
F-02 independent numerical audit -- Chapter 4
(chap04_simplicial_waves_porous_transport.tex)

Every claim: independent oracle + negative control (mutated formula that
must fail). Read-only; does not edit the chapter. Includes the F-46
ground-state issue (energy unbounded below -> no energy-minimizing ground
state).
"""
import numpy as np
from scipy import integrate
from math import gamma

np.random.seed(0)
PASS, FAIL = [], []


def report(name, line, ok, detail):
    (PASS if ok else FAIL).append(name)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} (book line ~{line})")
    print(f"       {detail}")


# ---------------------------------------------------------------------------
# Shared machinery: the continuous multinomial Beta-kernel on Delta_{m-1}(alpha)
# for m = 3 (two free coordinates y1, y2), computed by DIRECT numerical
# double quadrature -- an oracle independent of the book's symbolic Fourier
# analysis / Taylor expansion of sigma.
# ---------------------------------------------------------------------------
ALPHA = 3.0
M_SIMPLEX = 3  # m = 3 => y in R^2


def binom_kernel(y1, y2, alpha=ALPHA):
    y3 = alpha - y1 - y2
    if y3 < -1e-12 or y1 < -1e-12 or y2 < -1e-12:
        return 0.0
    y3 = max(y3, 0.0)
    return gamma(alpha + 1) / (gamma(y1 + 1) * gamma(y2 + 1) * gamma(y3 + 1))


I_m, _ = integrate.dblquad(lambda y2, y1: binom_kernel(y1, y2), 0, ALPHA,
                            lambda y1: 0, lambda y1: ALPHA - y1, epsabs=1e-11, epsrel=1e-11)


def sigma_direct(k1, k2, alpha=ALPHA):
    """sigma^alpha_{Delta_m}(k) via DIRECT double quadrature of the integral
    definition (eq. dispersion theorem, line 146-148) -- independent of the
    book's small-k Taylor expansion."""
    integrand = lambda y2, y1: binom_kernel(y1, y2) * (1 - np.cos(k1 * y1 + k2 * y2))
    val, _ = integrate.dblquad(integrand, 0, alpha, lambda y1: 0, lambda y1: alpha - y1,
                                epsabs=1e-10, epsrel=1e-10)
    return val / (alpha ** 2 * I_m)


# ---------------------------------------------------------------------------
# Claim 1 (lines 144-154, Theorem "Dispersion Symbol"): 0 <= sigma(k) <=
# 2/alpha^2, and the small-k expansion is sigma(k) = (1/(2 alpha^2)) k^T M2 k
# + O(|k|^4), where the book DEFINES M2 as "the second-moment matrix of the
# normalized kernel" -- i.e. M2_ij = (1/I_m) * int y_i y_j * binom(alpha,y) dy
# over the simplex, NOT as "whatever matrix makes the Taylor expansion of
# sigma come out right". We compute M2 from THIS definition, by its own
# direct 2D quadrature (independent of sigma_direct's quadrature, which
# integrates a different integrand: (1-cos(k.y)) rather than y_i*y_j), and
# only THEN compare the resulting prediction (1/(2 alpha^2)) k^T M2 k against
# sigma_direct(k) for small k. This removes the earlier circularity, where
# M2 had been defined as alpha^2 * (the finite-difference Hessian of sigma
# itself), making the "Taylor expansion" check tautological (Taylor's
# theorem applied to itself).
# Negative control: the mutated small-k formula sigma ~ (1/alpha^2) k^T M2 k
# (dropping the stated factor 1/2) must disagree with sigma_direct. A second,
# independent negative control replaces the Beta-kernel density by the
# UNIFORM density on the same simplex in the M2 quadrature (wrong kernel):
# the resulting M2_uniform must differ substantially from M2 (M2 is a
# property of the specific Beta-kernel, not of the simplex's shape alone).
# ---------------------------------------------------------------------------
rng = np.random.default_rng(1)
bound_ok = True
samples = []
for _ in range(15):
    k1, k2 = rng.uniform(-6, 6, size=2)
    s = sigma_direct(k1, k2)
    samples.append((k1, k2, s))
    if not (-1e-8 <= s <= 2 / ALPHA ** 2 + 1e-6):
        bound_ok = False


def moment_matrix(weight_fn):
    """M2_ij = (1/I_w) * int y_i y_j * weight_fn(y1,y2) dy over Delta_{m-1}(alpha),
    I_w = int weight_fn dy. Independent of sigma_direct: a different integrand
    (y_i*y_j instead of 1-cos(k.y)) and, for weight_fn=binom_kernel, the SAME
    definition the book states in words ("second-moment matrix of the
    normalized kernel"), evaluated by direct quadrature rather than inferred
    from sigma's own Taylor coefficients."""
    I_w, _ = integrate.dblquad(lambda y2, y1: weight_fn(y1, y2), 0, ALPHA,
                                lambda y1: 0, lambda y1: ALPHA - y1, epsabs=1e-11, epsrel=1e-11)
    m11, _ = integrate.dblquad(lambda y2, y1: y1 * y1 * weight_fn(y1, y2), 0, ALPHA,
                                lambda y1: 0, lambda y1: ALPHA - y1, epsabs=1e-10, epsrel=1e-10)
    m22, _ = integrate.dblquad(lambda y2, y1: y2 * y2 * weight_fn(y1, y2), 0, ALPHA,
                                lambda y1: 0, lambda y1: ALPHA - y1, epsabs=1e-10, epsrel=1e-10)
    m12, _ = integrate.dblquad(lambda y2, y1: y1 * y2 * weight_fn(y1, y2), 0, ALPHA,
                                lambda y1: 0, lambda y1: ALPHA - y1, epsabs=1e-10, epsrel=1e-10)
    return m11 / I_w, m22 / I_w, m12 / I_w


M2_11, M2_22, M2_12 = moment_matrix(binom_kernel)
struct_ok = abs(M2_11 - M2_22) < 0.02 * abs(M2_11)  # equal diagonal entries (a*Id+b*11^T structure)

ok1 = bound_ok and struct_ok
report("sigma(k) in [0, 2/alpha^2], and M2 (second-moment matrix of the Beta-kernel, computed DIRECTLY from its "
       "definition int y y^T K(y) dy / I_m, independent of sigma's own Taylor expansion) has the a*Id+b*11^T "
       "structure (equal diagonal entries)",
       "144-154", ok1,
       f"bound holds on 15 random k (sup 2/alpha^2={2/ALPHA**2:.4f}); M2 (direct moment quadrature): "
       f"M2_11={M2_11:.5f}, M2_22={M2_22:.5f}, M2_12={M2_12:.5f}")

# small-k check: does sigma_direct's OWN independent quadrature (integrand
# 1-cos(k.y)) agree with the prediction built from M2 (integrand y_i*y_j)?
# These are two genuinely different integrals of the same density.
k_small = 0.15
s_small = sigma_direct(k_small, 0)
pred_correct = (1 / (2 * ALPHA ** 2)) * M2_11 * k_small ** 2
pred_wrong = (1 / ALPHA ** 2) * M2_11 * k_small ** 2  # dropped the factor 1/2 (mutation)
ok1_neg = abs(s_small - pred_wrong) > abs(s_small - pred_correct) * 3
report("NEGATIVE CONTROL: dropping the 1/2 factor in sigma ~ (1/alpha^2) k^T M2 k must disagree with the direct "
       "quadrature of sigma, using M2 from its OWN direct moment quadrature (not from sigma's Taylor coefficients)",
       "144-154", ok1_neg,
       f"sigma({k_small},0)={s_small:.6e}; correct 1/2-factor prediction={pred_correct:.6e}; "
       f"mutated (no 1/2) prediction={pred_wrong:.6e}")

# second negative control: wrong kernel (uniform density on the same simplex
# instead of the Beta-kernel) must give a visibly different M2 -- M2 is a
# property of the specific stated kernel, not just of the domain's shape.
M2_11_uniform, M2_22_uniform, M2_12_uniform = moment_matrix(lambda y1, y2: 1.0 if (y1 >= -1e-12 and y2 >= -1e-12 and y1 + y2 <= ALPHA + 1e-12) else 0.0)
ok1_neg2 = abs(M2_11_uniform - M2_11) > 0.05 * abs(M2_11)
report("NEGATIVE CONTROL: replacing the Beta-kernel by the uniform density on the same simplex in the moment "
       "quadrature must give a visibly different M2_11",
       "144-154", ok1_neg2,
       f"M2_11 (Beta-kernel)={M2_11:.6f}; M2_11 (uniform density on same simplex)={M2_11_uniform:.6f}")


# ---------------------------------------------------------------------------
# Claim 2 (lines 291-324, Theorem "Anisotropic Mean Squared Displacement"):
# <xx^T>(t) = K_diff/(alpha^2 Gamma(beta+1)) * M2(alpha) * t^beta EXACTLY,
# via <x_i x_j>(t) = -d^2/dk_i dk_j [E_beta(-K sigma(k) t^beta)] at k=0.
# Oracle: evaluate E_beta(z) by its OWN series definition (as stated in the
# chapter, line 272) but differentiate NUMERICALLY (finite differences in
# k-space) rather than via the book's symbolic chain rule -- this isolates
# and independently re-derives the claimed closed form.
# Negative control: dropping the 1/alpha^2 prefactor must disagree.
# ---------------------------------------------------------------------------
def mittag_leffler(z, beta, nterms=60):
    z = complex(z)
    total = 0.0 + 0.0j
    term = 1.0 + 0.0j
    for n in range(nterms):
        total += z ** n / gamma(beta * n + 1)
    return total.real


BETA = 0.6
K_DIFF = 1.7
T_TEST = 1.3


def F_hat(k1, k2):
    s = sigma_direct(k1, k2)
    return mittag_leffler(-K_DIFF * s * T_TEST ** BETA, BETA)


h = 0.05
F00 = F_hat(0, 0)  # should be 1 (E_beta(0)=1)
Fp1 = F_hat(h, 0); Fm1 = F_hat(-h, 0)
Fp2 = F_hat(0, h); Fm2 = F_hat(0, -h)
Fpp = F_hat(h, h); Fpm = F_hat(h, -h); Fmp = F_hat(-h, h); Fmm = F_hat(-h, -h)

msd11_numeric = -(Fp1 - 2 * F00 + Fm1) / h ** 2
msd22_numeric = -(Fp2 - 2 * F00 + Fm2) / h ** 2
msd12_numeric = -(Fpp - Fpm - Fmp + Fmm) / (4 * h ** 2)

# closed-form prediction uses M2 from its OWN direct moment quadrature
# (computed above in Claim 1, int y y^T K(y) dy / I_m), NOT from a
# finite-difference Hessian of sigma -- removing the second tautology
# flagged by L2 (there, M2 had been *defined* as alpha^2*H_FD, so the
# 1/alpha^2 prefactor cancelled by construction).
pref = K_DIFF / (ALPHA ** 2 * gamma(BETA + 1)) * T_TEST ** BETA
msd11_formula = pref * M2_11
msd22_formula = pref * M2_22
msd12_formula = pref * M2_12

ok2 = (abs(msd11_numeric - msd11_formula) < 0.02 * abs(msd11_formula) and
       abs(msd22_numeric - msd22_formula) < 0.02 * abs(msd22_formula) and
       abs(msd12_numeric - msd12_formula) < 0.02 * max(abs(msd12_formula), 1e-6) + 1e-5)
report("MSD tensor <xx^T>(t) = K/(alpha^2 Gamma(beta+1)) M2 t^beta (independent FD second derivative of E_beta(-K sigma t^beta))",
       "291-324", ok2,
       f"numeric (11,22,12)=({msd11_numeric:.6f},{msd22_numeric:.6f},{msd12_numeric:.6f}); "
       f"formula=({msd11_formula:.6f},{msd22_formula:.6f},{msd12_formula:.6f})")

pref_wrong = K_DIFF / gamma(BETA + 1) * T_TEST ** BETA  # missing 1/alpha^2
msd11_wrong = pref_wrong * M2_11
ok2_neg = abs(msd11_numeric - msd11_wrong) > abs(msd11_numeric - msd11_formula) * 3
report("NEGATIVE CONTROL: dropping the 1/alpha^2 prefactor must disagree with the FD-computed MSD",
       "291-324", ok2_neg, f"numeric={msd11_numeric:.6f}; correct formula={msd11_formula:.6f}; "
       f"mutated (no 1/alpha^2) formula={msd11_wrong:.6f}")


# ---------------------------------------------------------------------------
# Claim 3 (F-46; lines 243-245, Remark after the solitary-wave Conjecture):
# in the focusing case, the energy at fixed mass is unbounded below (-> no
# energy minimizer / no "ground state" in the usual sense), because the
# kinetic term is BOUNDED (0 <= kinetic <= (hbar^2/(M alpha^2)) N[psi]) while
# the focusing nonlinear term -> -infinity under the scaling psi_w(x) =
# w^{-(m-1)/2} phi(x/w) as w -> 0 (mass N[psi_w] is w-independent).
# Oracle: DIRECT 2D numerical integration (independent of the change-of-
# variables algebra in the remark) of N[psi_w] and of the quartic term for
# a decreasing sequence of w, with a log-log power-law fit of the exponent.
# Negative control: the wrong predicted exponent -(m-1)(p+1) (instead of
# -(m-1)p) must disagree with the fitted exponent.
# ---------------------------------------------------------------------------
P_EXP = 1.0  # nonlinearity exponent p


def phi2d(x1, x2):
    return np.exp(-(x1 ** 2 + x2 ** 2) / 2)


def mass_integral(w):
    f = lambda x2, x1: (w ** -1 * phi2d(x1 / w, x2 / w)) ** 2
    val, _ = integrate.dblquad(f, -8 * w, 8 * w, lambda x1: -8 * w, lambda x1: 8 * w,
                                epsabs=1e-10, epsrel=1e-9)
    return val


def quartic_integral(w):
    f = lambda x2, x1: (w ** -1 * phi2d(x1 / w, x2 / w)) ** (2 * P_EXP + 2)
    val, _ = integrate.dblquad(f, -8 * w, 8 * w, lambda x1: -8 * w, lambda x1: 8 * w,
                                epsabs=1e-12, epsrel=1e-10)
    return val


ws = [1.0, 0.5, 0.25, 0.125]
masses = [mass_integral(w) for w in ws]
quartics = [quartic_integral(w) for w in ws]

mass_const_ok = max(masses) / min(masses) < 1.01  # mass should be w-independent

log_w = np.log(ws)
log_q = np.log(quartics)
fit_slope = np.polyfit(log_w, log_q, 1)[0]
predicted_slope = -(M_SIMPLEX - 1) * P_EXP  # -(m-1)*p = -2

ok3 = mass_const_ok and abs(fit_slope - predicted_slope) < 0.05
report("F-46: N[psi_w] is w-independent (mass conserved under rescaling) and nonlinear term ~ w^{-(m-1)p} -> infinity as w->0",
       "243-245", ok3,
       f"masses at w={ws}: {[f'{m:.6f}' for m in masses]} (ratio max/min={max(masses)/min(masses):.5f}); "
       f"fitted log-log slope of quartic term = {fit_slope:.4f} (predicted {predicted_slope:.1f})")

predicted_slope_wrong = -(M_SIMPLEX - 1) * (P_EXP + 1)  # -(m-1)(p+1) = -4, the wrong mutated exponent
ok3_neg = abs(fit_slope - predicted_slope_wrong) > 0.3
report("NEGATIVE CONTROL: wrong exponent -(m-1)(p+1) must disagree with the fitted power-law slope",
       "243-245", ok3_neg, f"fitted slope={fit_slope:.4f} vs wrong prediction={predicted_slope_wrong:.1f}")


# ---------------------------------------------------------------------------
# Claim 4 (lines 170-207, Theorem "Global Conservation of Mass and Energy"):
# full nonlinear-dynamics check via an independent split-step Fourier
# pseudo-spectral simulation (m=2, i.e. 1D NLSE with the Beta-kernel symbol)
# of eq. (nlse_main). Each split-step substep is a pure phase multiplication
# (unitary), so mass is conserved to machine precision; energy is conserved
# up to the known O(dt^2) Strang-splitting error, which must shrink by ~4x
# when dt is halved.
# Negative control: replace the unitary split-step scheme by a naive
# first-order explicit Euler step (same dt, same total time) -- mass
# conservation must then visibly FAIL.
# ---------------------------------------------------------------------------
ALPHA1 = 3.0  # m=2 case (1D), independent 1D simplex integral


def binom1d(y, alpha=ALPHA1):
    y2 = alpha - y
    if y < -1e-12 or y2 < -1e-12:
        return 0.0
    y2 = max(y2, 0.0)
    return gamma(alpha + 1) / (gamma(y + 1) * gamma(y2 + 1))


I2, _ = integrate.quad(binom1d, 0, ALPHA1, epsabs=1e-12, epsrel=1e-12)


def sigma1d(k, alpha=ALPHA1):
    val, _ = integrate.quad(lambda y: binom1d(y, alpha) * (1 - np.cos(k * y)), 0, alpha,
                             epsabs=1e-12, epsrel=1e-12)
    return val / (alpha ** 2 * I2)


Ngrid = 128
Ldom = 12.0
dx = 2 * Ldom / Ngrid
xgrid = -Ldom + dx * np.arange(Ngrid)
kgrid = 2 * np.pi * np.fft.fftfreq(Ngrid, d=dx)
sigma_vals = np.array([sigma1d(k) for k in kgrid])

HBAR = 1.0
MASS = 1.0
KAPPA = 0.25
PNL = 1.0

psi0 = np.exp(-xgrid ** 2 / 2) * np.exp(0.3j * xgrid)
psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0) ** 2) * dx)


def mass_of(psi):
    return np.sum(np.abs(psi) ** 2) * dx


def energy_of(psi):
    psi_hat = np.fft.fft(psi) * dx
    kinetic = (HBAR ** 2 / (2 * MASS)) * np.sum(sigma_vals * np.abs(psi_hat) ** 2) / (Ngrid * dx)
    nonlin = -(KAPPA / (PNL + 1)) * np.sum(np.abs(psi) ** (2 * PNL + 2)) * dx
    return kinetic + nonlin


def split_step(psi, dt, nsteps):
    lin_phase = np.exp(-1j * dt * (HBAR / (2 * MASS)) * sigma_vals)
    masses, energies = [mass_of(psi)], [energy_of(psi)]
    for _ in range(nsteps):
        # half nonlinear step (unitary phase rotation, exact mass-preserving)
        psi = psi * np.exp(1j * KAPPA * np.abs(psi) ** (2 * PNL) * (dt / 2) / HBAR)
        # full linear step in Fourier space (unitary)
        psi_hat = np.fft.fft(psi)
        psi_hat *= lin_phase
        psi = np.fft.ifft(psi_hat)
        # half nonlinear step
        psi = psi * np.exp(1j * KAPPA * np.abs(psi) ** (2 * PNL) * (dt / 2) / HBAR)
        masses.append(mass_of(psi))
        energies.append(energy_of(psi))
    return np.array(masses), np.array(energies)


dt1 = 0.01
m1, e1 = split_step(psi0.copy(), dt1, 200)
dt2 = dt1 / 2
m2, e2 = split_step(psi0.copy(), dt2, 400)

mass_drift1 = np.max(np.abs(m1 - m1[0])) / m1[0]
energy_drift1 = np.max(np.abs(e1 - e1[0])) / abs(e1[0])
energy_drift2 = np.max(np.abs(e2 - e2[0])) / abs(e2[0])

mass_conserved_ok = mass_drift1 < 1e-10
energy_shrinks_ok = energy_drift2 < energy_drift1 / 2.5  # expect ~4x shrink (2nd order), allow margin

ok4 = mass_conserved_ok and energy_shrinks_ok
report("Full split-step spectral simulation of the NLSE: mass conserved to machine precision; "
       "energy drift shrinks ~O(dt^2) under splitting",
       "170-207", ok4,
       f"mass drift @dt={dt1}: {mass_drift1:.2e}; energy drift @dt={dt1}: {energy_drift1:.2e}, "
       f"@dt={dt2}: {energy_drift2:.2e} (ratio {energy_drift1/energy_drift2:.2f}x, expect ~4x)")


def euler_step(psi, dt, nsteps):
    masses = [mass_of(psi)]
    for _ in range(nsteps):
        psi_hat = np.fft.fft(psi)
        lin_term = np.fft.ifft(1j * (HBAR / (2 * MASS)) * sigma_vals * psi_hat)
        nonlin_term = -1j * (KAPPA / HBAR) * np.abs(psi) ** (2 * PNL) * psi
        psi = psi + dt * (lin_term + nonlin_term)
        masses.append(mass_of(psi))
    return np.array(masses)

m_euler = euler_step(psi0.copy(), dt1, 200)
euler_drift = np.max(np.abs(m_euler - m_euler[0])) / m_euler[0]
ok4_neg = euler_drift > 1e-4  # naive non-unitary Euler scheme must visibly violate mass conservation
report("NEGATIVE CONTROL: naive explicit-Euler integrator (non-unitary) must visibly violate mass conservation",
       "170-207", ok4_neg, f"explicit-Euler mass drift = {euler_drift:.2e} (should be >>1e-10, unlike the split-step scheme)")


# Second negative control for Claim 4 (per L2 fix): the energy drift check
# above only shows O(dt^2) shrinkage for the CORRECT energy functional
# (nonlin = -(KAPPA/(PNL+1)) * ...). A mutated energy using KAPPA/PNL in
# place of KAPPA/(PNL+1) (i.e. the wrong normalization constant, NOT a
# conserved quantity of the split-step scheme) must show an O(1) drift
# that does NOT shrink as dt -> dt/2.
def energy_of_wrong(psi):
    psi_hat = np.fft.fft(psi) * dx
    kinetic = (HBAR ** 2 / (2 * MASS)) * np.sum(sigma_vals * np.abs(psi_hat) ** 2) / (Ngrid * dx)
    nonlin_wrong = -(KAPPA / PNL) * np.sum(np.abs(psi) ** (2 * PNL + 2)) * dx  # wrong prefactor (mutation)
    return kinetic + nonlin_wrong


def split_step_wrong_energy(psi, dt, nsteps):
    lin_phase = np.exp(-1j * dt * (HBAR / (2 * MASS)) * sigma_vals)
    energies = [energy_of_wrong(psi)]
    for _ in range(nsteps):
        psi = psi * np.exp(1j * KAPPA * np.abs(psi) ** (2 * PNL) * (dt / 2) / HBAR)
        psi_hat = np.fft.fft(psi)
        psi_hat *= lin_phase
        psi = np.fft.ifft(psi_hat)
        psi = psi * np.exp(1j * KAPPA * np.abs(psi) ** (2 * PNL) * (dt / 2) / HBAR)
        energies.append(energy_of_wrong(psi))
    return np.array(energies)


e1_wrong = split_step_wrong_energy(psi0.copy(), dt1, 200)
e2_wrong = split_step_wrong_energy(psi0.copy(), dt2, 400)
drift1_wrong = np.max(np.abs(e1_wrong - e1_wrong[0])) / abs(e1_wrong[0])
drift2_wrong = np.max(np.abs(e2_wrong - e2_wrong[0])) / abs(e2_wrong[0])
# the correct functional's drift shrinks by ~4x when dt halves (O(dt^2));
# the mutated functional is simply not the conserved quantity of this
# scheme, so its drift should stay O(1) (not shrink by ~4x) under dt -> dt/2
ratio_wrong = drift1_wrong / drift2_wrong if drift2_wrong > 0 else np.inf
ok4_neg2 = drift1_wrong > 1e-3 and not (3.0 < ratio_wrong < 5.0)
report("NEGATIVE CONTROL: mutated energy functional (kappa/p instead of kappa/(p+1)) must show an O(1) drift that "
       "does NOT shrink ~4x when dt is halved, unlike the correctly-normalized energy",
       "170-207", ok4_neg2,
       f"mutated-energy drift @dt={dt1}: {drift1_wrong:.2e}, @dt={dt2}: {drift2_wrong:.2e} (ratio {ratio_wrong:.2f}x, "
       f"expect NOT ~4x); correct-energy ratio was {energy_drift1/energy_drift2:.2f}x")


print()
print("=" * 70)
print(f"Chapter 4 summary: {len(PASS)} PASS, {len(FAIL)} FAIL")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("  -", f)
