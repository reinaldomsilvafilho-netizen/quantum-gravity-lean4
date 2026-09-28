"""V2 - independent recomputation of the fakeon inflation numbers (ABP 2020, eq. 7.3 read in the arXiv text
2005.10293 by the verifier) and of the length scale l = hbar c / (m c^2), with CODATA 2018 constants.

ABP (7.3), leading order in 1/N:  A_R = m_phi^2 N^2 / (3 pi M_Pl^2)   (non-reduced M_Pl = sqrt(hbar c / G)),
                                  r   = 24 m_chi^2 / [N^2 (m_phi^2 + 2 m_chi^2)],   bound m_chi > m_phi/4.
Oracle for A_R: Starobinsky slow-roll with REDUCED Planck mass, P = V/(24 pi^2 eps M^4), V = (3/4) m^2 M^2 (1-e^{-y})^2,
integrated numerically (N from phi_end with eps=1), independent of the closed form.
Negative controls: using the reduced mass in the closed form (factor sqrt(8 pi) error) must fail; single-scale with
m_chi = m_phi/2 must not give N^2 r = 8.
Dimensional check: [hbar c] = GeV m, [m c^2] = GeV -> [l] = m.
"""
import numpy as np
from scipy import integrate, optimize

R = []
def check(n, ok, info=''):
    R.append(bool(ok)); print(f"[{'PASS' if ok else 'FAIL'}] {n} {info}")

# CODATA 2018
hbar = 1.054571817e-34      # J s
c = 299792458.0             # m/s
G = 6.67430e-11             # m^3 kg^-1 s^-2
eV = 1.602176634e-19        # J
hbarc_GeVm = hbar * c / (eV * 1e9)                     # GeV m
MPl = np.sqrt(hbar * c / G) * c**2 / (eV * 1e9)        # GeV  (sqrt(hbar c/G) is a mass in kg)
MPl = np.sqrt(hbar * c / G) * c**2 / (eV * 1e9)
lP = np.sqrt(hbar * G / c**3)
Mred = MPl / np.sqrt(8 * np.pi)
print(f"   hbar c = {hbarc_GeVm:.6e} GeV m;  M_Pl = {MPl:.6e} GeV;  M_red = {Mred:.6e} GeV;  l_P = {lP:.5e} m")

As = np.exp(3.044) * 1e-10   # Planck 2018 TT,TE,EE+lowE+lensing: ln(1e10 A_s) = 3.044
def mphi_closed(N, M=MPl):
    return np.sqrt(3 * np.pi * As) * M / N

def mphi_slowroll(N):
    # V = 3/4 m^2 M^2 (1-e^{-y})^2, y = sqrt(2/3) phi/M;  eps = (M^2/2)(V'/V)^2 = (4/3) e^{-2y}/(1-e^{-y})^2
    eps = lambda y: (4 / 3) * np.exp(-2 * y) / (1 - np.exp(-y))**2
    yend = optimize.brentq(lambda y: eps(y) - 1, 0.1, 5)
    # dN = V/(M^2 V') dphi = (1/ (M^2)) ... in y: dN = (3/4) (e^{y}-1) dy
    Nof = lambda y: integrate.quad(lambda u: 0.75 * (np.exp(u) - 1), yend, y)[0]
    y = optimize.brentq(lambda y: Nof(y) - N, yend + 1e-6, 20)
    V_over_m2 = 0.75 * Mred**2 * (1 - np.exp(-y))**2
    P_over_m2 = V_over_m2 / (24 * np.pi**2 * eps(y) * Mred**4)
    return np.sqrt(As / P_over_m2)

r = lambda N, x: 24 * x**2 / (N**2 * (1 + 2 * x**2))   # x = m_chi/m_phi
for N in (55, 60):
    mc, ms = mphi_closed(N), mphi_slowroll(N)
    print(f"   N={N}: m_phi closed {mc:.4e} GeV, slow-roll oracle {ms:.4e} GeV")
mc60, ms60 = mphi_closed(60), mphi_slowroll(60)
check('I1 m_phi(N=60) closed form (ABP 7.3, non-reduced M_Pl) vs slow-roll oracle within 6%',
      abs(mc60 / ms60 - 1) < 0.06, f'({mc60:.3e} vs {ms60:.3e} GeV)')
bad = mphi_closed(60, Mred)
check('NC1 closed form with the reduced mass is off by sqrt(8 pi) ~ 5 (must fail the 6% test)',
      abs(bad / ms60 - 1) > 0.5, f'({bad:.3e} GeV)')

check('I2 window: N^2 r = 4/3 at x = 1/4, -> 12 as x -> inf, = 8 at x = 1',
      abs(r(1, .25) - 4 / 3) < 1e-12 and abs(r(1, 1e8) - 12) < 1e-6 and abs(r(1, 1) - 8) < 1e-12)
check('NC2 x = 1/2 does not give the single-scale value 8', abs(r(1, .5) - 8) > 1, f'(N^2 r = {r(1, .5):.3f})')
for N in (55, 60, 77):
    print(f"   N={N}: window [{r(N, .25):.3e}, {12 / N**2:.3e}], single scale r = {r(N, 1):.3e}")

# length scales
for lab, m in (('single scale, m_chi = m_phi (closed, N=60)', mc60), ('single scale (slow-roll, N=60)', ms60),
               ('single scale (closed, N=55)', mphi_closed(55)), ('upper bound 4 hbar c/m_phi (closed, N=60)', mc60 / 4),
               ('upper bound (slow-roll, N=60)', ms60 / 4)):
    l = hbarc_GeVm / m
    print(f"   {lab}: m = {m:.3e} GeV -> l = {l:.3e} m = {l / lP:.3e} l_P")
l1 = hbarc_GeVm / ms60; l2 = hbarc_GeVm / mc60
check('I3 single-scale l in [6e-30, 8e-30] m (README 7.2e-30)', 6e-30 < l2 < l1 < 8e-30, f'({l2:.2e} .. {l1:.2e} m)')

# LiteBIRD significance with sigma(r) = 1e-3 (mission requirement, total error)
sig = 1e-3
for N in (55, 60, 77):
    print(f"   N={N}: single-scale r/sigma = {r(N, 1) / sig:.2f};  Starobinsky 12/N^2 - 8/N^2 = {(4 / N**2) / sig:.2f} sigma")
check('I4 single-scale r at N=60 is < 3 sigma for sigma_r = 1e-3 (not a detection)', r(60, 1) / sig < 3)
check('I5 8/N^2 vs Starobinsky 12/N^2 separated by < 1.5 sigma at N = 60', (4 / 60**2) / sig < 1.5)
# ACT
ns, dns = 0.974, 0.003
N_act = 2 / (1 - ns)
check('I6 ACT n_s -> N = 2/(1-n_s) = 76.9; N=60 is 2.4 sigma low', abs(N_act - 76.9) < 0.1 and abs(((1 - 2 / 60) - ns) / dns + 2.44) < 0.02)
print(f"\n{sum(R)}/{len(R)} checks passed")
