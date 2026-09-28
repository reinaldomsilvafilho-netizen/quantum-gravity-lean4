"""E2 - Fakeon inflation window (Anselmi-Bianchi-Piva, JHEP 07 (2020) 211, arXiv:2005.10293).

Source formula, read in the paper text (eq. 7.3, leading order in 1/N):
    r = 24 m_chi^2 / ( N^2 (m_phi^2 + 2 m_chi^2) ),   n_R - 1 = -2/N,   r ~ -8 n_T,
consistency bound (eq. 4.9 / abstract):  m_chi > m_phi / 4.
Abstract: 4/3 < N^2 r < 12.  Text: "for N = 60 we have 0.4 < 1000 r < 3" (rounded).

Checks
  F1  m_chi -> infinity limit equals 12/N^2, and 12/N^2 is checked against an INDEPENDENT oracle:
      numerical slow-roll of the Starobinsky potential V = V0 (1 - exp(-sqrt(2/3) phi))^2
      (reduced Planck units), N^2 r -> 12 as N grows (N = 1e3, 1e4).
  F2  at m_chi = m_phi/4 the formula gives N^2 r = 4/3 exactly (abstract lower edge).
  F3  N = 60 window equals [0.37, 3.33] x 1e-3, consistent with the paper's rounded "0.4 .. 3".
  F4  inflaton mass from A_s (Planck 2018 ln(1e10 A_s) = 3.044) via the Starobinsky potential oracle,
      compared with the closed form m = sqrt(24 pi^2 A_s) M_red / N.  Dimensional check of
      l_chi = hbar c / (m_chi c^2) in metres.  Bound l < 4 hbar c / m_phi.
  F5  relative change of r for m_chi = M_Planck (the book's l = l_P): ~ m_phi^2 / (2 M_P^2).
  F6  ACT DR6 n_s = 0.974 +- 0.003 (arXiv:2503.14452 abstract) -> N = 2/(1-n_s); window at that N;
      tension of the N = 60 Starobinsky/fakeon n_s (unchanged by C^2) in sigma.
  NC1 mutated formula with m_phi <-> m_chi swapped must NOT reproduce 4/3 at m_chi = m_phi/4.
  NC2 mutated consistency bound m_chi > m_phi/2 must NOT reproduce the abstract's 4/3.
"""
import numpy as np
from scipy import integrate, optimize, constants as C

res = []


def check(name, ok, info=''):
    res.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")


def r_fakeon(N, mchi_over_mphi):
    x2 = mchi_over_mphi ** 2
    return 24 * x2 / (N ** 2 * (1 + 2 * x2))


# ---------- F1: Starobinsky oracle by slow roll ----------
a = np.sqrt(2.0 / 3.0)
V = lambda p: (1 - np.exp(-a * p)) ** 2          # V0 = 1 (drops out of eps, r)
dV = lambda p: 2 * a * np.exp(-a * p) * (1 - np.exp(-a * p))
eps = lambda p: 0.5 * (dV(p) / V(p)) ** 2
phi_end = optimize.brentq(lambda p: eps(p) - 1, 0.1, 5)


def efolds(p):  # N = int_{phi_end}^{phi} V/V' dphi
    return integrate.quad(lambda q: V(q) / dV(q), phi_end, p, limit=200)[0]


def phi_at(N):
    return optimize.brentq(lambda p: efolds(p) - N, phi_end + 1e-6, 60)


for N in (1e3, 1e4):
    p = phi_at(N)
    rN = 16 * eps(p)
    print(f"   slow-roll oracle: N = {N:.0e}: N^2 r = {N**2 * rN:.5f}")
p60 = phi_at(60); r60_sr = 16 * eps(p60)
check('F1 formula limit m_chi->inf is 12/N^2', abs(r_fakeon(60, 1e8) * 3600 - 12) < 1e-9)
check('F1b slow-roll oracle N^2 r -> 12 (N=1e4, within 0.3%)', abs(1e8 * 16 * eps(phi_at(1e4)) - 12) / 12 < 3e-3)
print(f"   slow-roll oracle at N=60: r = {r60_sr:.5f}  vs 12/N^2 = {12/3600:.5f} (O(ln N / N) correction)")

# ---------- F2, F3 ----------
check('F2 N^2 r = 4/3 at m_chi = m_phi/4', abs(r_fakeon(1, 0.25) - 4 / 3) < 1e-12, f'({r_fakeon(1, 0.25):.12f})')
lo, hi = r_fakeon(60, 0.25), r_fakeon(60, 1e9)
check('F3 N=60 window [0.370, 3.333]e-3 (paper rounds to 0.4..3)', abs(lo - 3.7037e-4) < 1e-7 and abs(hi - 3.3333e-3) < 1e-7,
      f'({lo:.4e}, {hi:.4e})')
for N in (50, 55, 60):
    print(f"   N = {N}: {r_fakeon(N, .25):.2e} < r < {r_fakeon(N, 1e9):.2e};  n_s = {1 - 2/N:.4f}")

# ---------- F4: inflaton mass ----------
As = np.exp(3.044) * 1e-10
GeV_J = C.e * 1e9
Mred_GeV = np.sqrt(C.hbar * C.c / (8 * np.pi * C.G)) * C.c ** 2 / GeV_J
MP_GeV = np.sqrt(C.hbar * C.c / C.G) * C.c ** 2 / GeV_J
hbarc_GeVm = C.hbar * C.c / GeV_J
for N in (55, 60):
    m_closed = np.sqrt(24 * np.pi ** 2 * As) * Mred_GeV / N
    # oracle: A_s = V/(24 pi^2 eps) with V0 = (3/4) m^2 M^2 -> m from slow-roll at exact phi(N)
    p = phi_at(N)
    m_sr = np.sqrt(As * 24 * np.pi ** 2 * eps(p) / (0.75 * V(p))) * Mred_GeV
    print(f"   N = {N}: m_phi closed {m_closed:.3e} GeV, slow-roll oracle {m_sr:.3e} GeV")
    if N == 60:
        mphi = m_sr
        agree = abs(m_closed / m_sr - 1) < 0.05
check('F4 m_phi(N=60) closed form vs slow-roll oracle within 5%', agree, f'(m_phi = {mphi:.3e} GeV)')
# dimensions: [hbar c] = J m, [m c^2] = J -> metres
hbar_d, c_d, E_d = np.array([1, 2, -1]), np.array([0, 1, -1]), np.array([1, 2, -2])  # (M, L, T)
dim_ok = ((hbar_d + c_d) - E_d).tolist() == [0, 1, 0]   # [hbar c / (m c^2)] = L
lmax = 4 * hbarc_GeVm / mphi
check('F4b l_chi = hbar c/(m_chi c^2) has dimension L; bound l < 4 hbar c/m_phi', dim_ok and 1e-30 < lmax < 1e-28,
      f'(l_max = {lmax:.2e} m = {lmax / 1.616255e-35:.2e} l_P; m_chi_min = {mphi / 4:.2e} GeV)')

# ---------- F5 ----------
rel = 1 - r_fakeon(60, MP_GeV / mphi) / r_fakeon(60, 1e30)
check('F5 l = l_P: relative shift of r ~ m_phi^2/(2 M_P^2)', abs(rel / (mphi ** 2 / (2 * MP_GeV ** 2)) - 1) < 1e-3,
      f'(shift = {rel:.2e})')

# ---------- F6 ----------
ns, sig = 0.974, 0.003
Nact = 2 / (1 - ns); Nlo, Nhi = 2 / (1 - (ns - sig)), 2 / (1 - (ns + sig))
t60 = (ns - (1 - 2 / 60)) / sig
print(f"   ACT DR6: N = {Nact:.1f} (1 sigma {Nlo:.1f}-{Nhi:.1f}); window at N={Nact:.0f}: "
      f"{r_fakeon(Nact, .25):.2e} < r < {r_fakeon(Nact, 1e9):.2e}; N=60 n_s is {t60:.1f} sigma low")
check('F6 ACT n_s maps to N ~ 77 and N=60 sits > 2 sigma low', 70 < Nact < 85 and t60 > 2)


# ---------- F7: single-scale reading (m_chi = m_phi = 1/l, same l in spin-0 and spin-2 sectors) ----------
l_single = hbarc_GeVm / mphi
check('F7 single scale m_chi = m_phi: N^2 r = 8 exactly; r(N=60) = 2.22e-3', abs(r_fakeon(1, 1.0) - 8) < 1e-12 and abs(r_fakeon(60, 1.0) - 8 / 3600) < 1e-12,
      f'(r(55) = {r_fakeon(55, 1):.2e}, r(60) = {r_fakeon(60, 1):.2e}, r(77) = {r_fakeon(77, 1):.2e}; l = hbar c/m_phi = {l_single:.2e} m = {l_single / 1.616255e-35:.2e} l_P)')

# ---------- negative controls ----------
r_mut = lambda N, x: 24 / (N ** 2 * (x ** 2 + 2))          # m_phi <-> m_chi swapped
check('NC1 swapped formula does not give 4/3 at m_chi = m_phi/4', abs(r_mut(1, 0.25) - 4 / 3) > 0.1,
      f'(gives {r_mut(1, .25):.3f})')
check('NC2 bound m_chi > m_phi/2 does not give 4/3', abs(r_fakeon(1, 0.5) - 4 / 3) > 0.1, f'(gives {r_fakeon(1, .5):.3f})')

print(f"\n{sum(res)}/{len(res)} checks passed")
