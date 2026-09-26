"""Camada 2, F-46 (cap. 4).

E1 Energy at fixed mass is unbounded below (Remark after Conj 3.3), with the ACTUAL symbol
   (m=2, i.e. R^1, alpha=2; hbar=M=kappa=1, p=1): Gaussians psi_w of unit mass.
   Kinetic term computed from sigma(k) by quadrature, checked against the bound N/alpha^2
   (hbar^2/M * N/alpha^2 with hbar=M=1).
   Mutation (control of the mechanism): with the LOCAL symbol k^2 the same family has
   E -> +infinity (1D, p=1 subcritical), so unboundedness really comes from sup sigma < inf.
E2 Prop 2.3 "vanishes iff u=0": for u a unit-mass Gaussian of width w, the form is > 0 and
   -> 0 only as w -> infinity (no non-zero L^2 minimizer), sanity check of Plancherel identity.
E3 Grisvard remark: corner-singularity exponents pi/omega for the Dirichlet Laplacian;
   r^{pi/omega} sin(pi theta/omega) is in H^4 near the corner iff pi/omega > 3 or pi/omega is
   an integer (then it is a harmonic polynomial). Hence H^4 regularity of the Navier problem
   holds for the square (omega=pi/2) and the equilateral triangle (omega=pi/3), fails for a
   generic triangle (e.g. angles 80/60/40 deg).  This tests the new sentence
   'Only for smooth boundary does the domain equal the H^4 Navier space'.
"""
import math
import numpy as np
from scipy import integrate

FAIL = []


def check(name, ok, info=None):
    print(("PASS " if ok else "FAIL ") + name + ("" if info is None else "  | " + str(info)))
    if not ok:
        FAIL.append(name)


alpha = 2.0
lb = lambda x, y: math.lgamma(x + 1) - math.lgamma(y + 1) - math.lgamma(x - y + 1)
Ia = integrate.quad(lambda y: math.exp(lb(alpha, y)), 0, alpha)[0]


def sigma(k):
    return integrate.quad(lambda y: math.exp(lb(alpha, y)) / Ia * (1 - math.cos(k * y)), 0, alpha, limit=400)[0] / alpha ** 2


kk = np.linspace(0, 400, 16001)
sig = np.array([sigma(k) for k in kk])
check("E1 0 <= sigma <= 2/alpha^2 and sigma -> 1/alpha^2", sig.min() >= -1e-14 and sig.max() <= 2 / alpha ** 2 and abs(sig[-1] - 1 / alpha ** 2) < 0.01, (sig.max(), sig[-1]))


def energy(w, local=False, p=1):
    # unitary FT of unit-mass Gaussian width w: |psi^(k)|^2 = (w/sqrt(pi)) exp(-w^2 k^2); even in k
    dens = lambda k: w / math.sqrt(math.pi) * math.exp(-w * w * k * k)
    if local:
        kin = 0.5 * integrate.quad(lambda k: k * k * dens(k), -np.inf, np.inf)[0]
    else:
        m = kk <= 60 / w
        kin = 0.5 * 2 * np.trapezoid(sig[m] * np.array([dens(k) for k in kk[m]]), kk[m])
    # int |psi|^{2p+2} for psi = (pi w^2)^{-1/4} exp(-x^2/(2w^2))
    pot = (math.pi * w * w) ** (-(p + 1) / 2) * math.sqrt(2 * math.pi * w * w / (2 * p + 2))
    return kin - pot / (p + 1), kin


Es = [energy(w) for w in (3.0, 1.0, 0.3, 0.1, 0.03)]
print("   nonlocal E(w):", [round(e, 4) for e, _ in Es])
check("E1 kinetic <= (hbar^2/2M)(2/alpha^2) N = 0.25 for all w", all(k <= 0.25 + 1e-9 for _, k in Es), [round(k, 4) for _, k in Es])
check("E1 E(psi_w) -> -infinity as w -> 0 at fixed mass", Es[-1][0] < -5 and Es[-1][0] < Es[-2][0] < Es[-3][0])
El = [energy(w, local=True)[0] for w in (3.0, 1.0, 0.3, 0.1, 0.03)]
check("E1-mut local symbol k^2 (1D, p=1): same family has E -> +infinity", El[-1] > 100 and El[-1] > El[-2], [round(e, 3) for e in El])

# E2
vals = []
for w in (0.5, 2.0, 8.0, 32.0):
    dens = lambda k: w / math.sqrt(math.pi) * math.exp(-w * w * k * k)
    m = kk <= 60 / w
    vals.append(2 * np.trapezoid(sig[m] * np.array([dens(k) for k in kk[m]]), kk[m]))
check("E2 quadratic form >0 for u != 0, decreasing to 0 only as the mass spreads out", all(v > 0 for v in vals) and vals == sorted(vals, reverse=True), [f"{v:.2e}" for v in vals])


# E3 corner exponents
def h4_ok(omega):
    lam = math.pi / omega
    return abs(lam - round(lam)) < 1e-12 or lam > 3  # r^lam sin(lam theta) in H^s iff s < lam+1 unless polynomial


check("E3 square (omega=pi/2): leading corner function is a polynomial -> H^4 Navier regularity holds", h4_ok(math.pi / 2))
check("E3 equilateral triangle (omega=pi/3): H^4 holds", h4_ok(math.pi / 3))
gen = [80, 60, 40]
check("E3 generic triangle 80/60/40 deg: H^4 fails at the 80 deg corner (pi/omega = 2.25 < 3)", not h4_ok(math.radians(80)), math.pi / math.radians(80))
print("   => 'in general fails on a simplex' is correct; 'ONLY for smooth boundary' is too strong (square, equilateral triangle).")
print("\nFAILURES:", FAIL if FAIL else "none")
