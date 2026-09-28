"""Ramo E, via 1: absolute neutrino masses from the circulant structure (draft, unverified).

Hypotheses (extensions of the fermion paper to neutrinos; not in the paper):
 H1  the neutrino root masses are the eigenvalues of a Hermitian circulant with the same
     Koide condition as the charged leptons, Q = 2/3 (b/a = 1/sqrt2). Signs of roots free.
 H2  H1 plus the same circulant phase delta as the charged leptons (no free parameter
     for the ratio dm21/dm31).
Outputs: m1, m2, m3, sum m, m_beta, m_betabeta range (TM1 mixing, free Majorana phases).

Data (CHECK against sources before citing):
  NuFIT 6.0 (Esteban et al., JHEP 12 (2024) 216), analysis IC19 without SK-atm, Table 1:
  NO: dm21 = 7.49e-5 eV^2, dm31 = 2.534e-3 eV^2;  IO: dm32 = -2.510e-3 eV^2.
  PDG 2024 charged leptons: me = 0.51099895 MeV, mmu = 105.6583755 MeV, mtau = 1776.93 MeV.
Oracle: Koide solutions found by root finding in m_lightest are re-derived from the
  circulant parametrization (a, b, delta) by an independent least-squares fit.
Negative control: all-positive roots cannot reach Q = 2/3 in NO (must report no solution);
  a mutated target Q = 0.60 must give a different sum.
"""
import itertools
import numpy as np
from scipy.optimize import brentq, least_squares

DM21, DM31_NO, DM32_IO = 7.49e-5, 2.534e-3, -2.510e-3  # NuFIT 6.0, IC19 without SK-atm (same analysis as the angles)


def masses(ml, order):
    if order == "NO":
        return np.array([ml, np.sqrt(ml**2 + DM21), np.sqrt(ml**2 + DM31_NO)])
    m2 = np.sqrt(ml**2 - DM32_IO)  # m3 = ml lightest
    return np.array([np.sqrt(m2**2 - DM21), m2, ml])


def Q(m, signs):
    r = np.array(signs) * np.sqrt(m)
    return m.sum() / r.sum() ** 2


def koide_solutions(order, target=2 / 3):
    sols = []
    grid = np.logspace(-7, 0, 4000)
    for signs in {(1, 1, 1), (-1, 1, 1), (1, -1, 1), (1, 1, -1)}:
        f = np.array([Q(masses(x, order), signs) - target for x in grid])
        for i in np.where(np.sign(f[:-1]) != np.sign(f[1:]))[0]:
            if np.isfinite(f[i]) and np.isfinite(f[i + 1]) and abs(f[i]) < 5 and abs(f[i + 1]) < 5:
                x = brentq(lambda y: Q(masses(y, order), signs) - target, grid[i], grid[i + 1], xtol=1e-16)
                sols.append((signs, x, masses(x, order)))
    return sols


def circulant_fit(roots):
    """Independent oracle: find (a, b, delta) with sorted a+2b cos(delta+2pi k/3) = sorted roots."""
    def res(p):
        a, b, d = p
        lam = np.sort(a + 2 * b * np.cos(d + 2 * np.pi * np.arange(3) / 3))
        return lam - np.sort(roots)
    best = None
    for d0 in np.linspace(0, 2 * np.pi, 13):
        r = least_squares(res, [roots.mean(), roots.std(), d0], xtol=1e-15, ftol=1e-15)
        if best is None or r.cost < best.cost:
            best = r
    a, b, d = best.x
    if b < 0:
        b, d = -b, d + np.pi
    return a, b, d % (2 * np.pi / 3), best.cost  # delta defined mod 2pi/3 (relabelling k)


# charged leptons
ml = np.array([0.51099895, 105.6583755, 1776.93])
a_l, b_l, d_l, c_l = circulant_fit(np.sqrt(ml))
print(f"charged leptons: Q = {Q(ml, (1, 1, 1)):.6f}, b/a = {b_l/a_l:.5f}, delta_l = {d_l:.5f} rad (2/9 = {2/9:.5f}); fit cost {c_l:.1e}")

# TM1 moduli of the first row (theta13 measured, theta12 from the TM1 sum rule)
s13sq = 0.02195
s12sq = 1 - 2 / (3 * (1 - s13sq))
Ue = np.array([(1 - s12sq) * (1 - s13sq), s12sq * (1 - s13sq), s13sq])  # |U_ei|^2


def mbb_range(m):
    vals = []
    for a, b in itertools.product(np.linspace(0, 2 * np.pi, 181), repeat=2):
        vals.append(abs(Ue[0] * m[0] + Ue[1] * m[1] * np.exp(1j * a) + Ue[2] * m[2] * np.exp(1j * b)))
    return min(vals), max(vals)


print("\nH1: neutrino Koide Q = 2/3")
for order in ("NO", "IO"):
    sols = koide_solutions(order)
    if not sols:
        print(f"  {order}: no solution")
    for signs, x, m in sols:
        roots = np.array(signs) * np.sqrt(m)
        a, b, d, cost = circulant_fit(roots)
        lo, hi = mbb_range(m)
        mbeta = np.sqrt((Ue * m**2).sum())
        print(f"  {order} signs={signs}: m = {np.round(m*1e3, 3)} meV, sum = {m.sum()*1e3:.1f} meV, "
              f"m_beta = {mbeta*1e3:.1f} meV, m_bb in [{lo*1e3:.1f}, {hi*1e3:.1f}] meV")
        print(f"      oracle circulant: b/a = {b/a:.5f} (1/sqrt2 = {1/np.sqrt(2):.5f}), delta_nu = {d:.4f} rad, cost {cost:.1e}")

# Negative controls
nc = [s for s in koide_solutions("NO") if s[0] == (1, 1, 1)]
print(f"\nnegative control 1 (NO, all roots positive): {'no solution (OK)' if not nc else 'SOLUTION FOUND (FAIL)'}")
alt = koide_solutions("NO", target=0.60)
print("negative control 2 (Q = 0.60): sums", [round(m.sum() * 1e3, 1) for _, _, m in alt], "meV (must differ from H1)")

# H2: same delta as the charged leptons, Q = 2/3  ->  mass ratios fixed, compare dm21/dm31
print("\nH2: neutrino circulant with b/a = 1/sqrt2 and delta_nu = delta_l (+ k pi/3 variants)")
r_data = DM21 / DM31_NO
for shift_name, shift in (("0", 0.0), ("pi/12 (Brannen)", np.pi / 12), ("pi/3", np.pi / 3), ("pi/6", np.pi / 6)):
    d = d_l + shift
    lam = 1 + np.sqrt(2) * np.cos(d + 2 * np.pi * np.arange(3) / 3)  # a = 1, 2b = sqrt2
    m = np.sort(lam**2)
    r = (m[1] ** 2 - m[0] ** 2) / (m[2] ** 2 - m[0] ** 2)
    print(f"  delta_l + {shift_name:15s}: dm21/dm31 = {r:.4g}  (data {r_data:.4g}),  m1:m2:m3 = {np.round(m/m[2], 5)}")
