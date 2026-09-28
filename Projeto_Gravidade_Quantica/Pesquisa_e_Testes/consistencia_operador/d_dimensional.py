"""Dimensional check and orders of magnitude: M* vs l* for both branches (CODATA via scipy.constants).

Dimension vectors are exponents of (L, T, Mass).  Checks:
  D1  l* = hbar/(M* c) is a length; mutant l* = hbar/(M* c^2) must fail.
  D2  z=3 dispersion in SI: omega^2 = c^2 k^2 + c^2 l*^4 k^6 is homogeneous (T^-2);
      natural-unit form (hbar omega)^2 = (hbar c k)^2 + (hbar c k)^6/(M* c^2)^4 agrees numerically.
  D3  isotropic symbol k^2 + l*^2 k^4 homogeneous (L^-2); mutant l*^4 k^4 must fail.
  D4  Planck values two routes: l_P = sqrt(hbar G/c^3) vs hbar/(M_P c), M_P = sqrt(hbar c/G).
Orders of magnitude: fractional GW group-velocity shift at 100 Hz for
  z=2-type ansatz (ch.13):  dv/c = (3/2) xi (l* k)^2
  z=3 branch:               dv/c = (5/2) (l* k)^4
for M* = M_P, 1e16 GeV, 1e10 GeV, and the l* ceilings implied by GW170817 (|dv|/c < 3e-15, conservative
using 1e-15 lower side is not needed).
"""
import numpy as np
from scipy import constants as C

PASS = []


def check(name, cond):
    PASS.append((name, bool(cond)))
    print(('PASS ' if cond else 'FAIL ') + name)


dim = {'hbar': np.array([2, -1, 1]), 'c': np.array([1, -1, 0]), 'M': np.array([0, 0, 1]),
       'k': np.array([-1, 0, 0]), 'omega': np.array([0, -1, 0]), 'G': np.array([3, -2, -1])}
l_dim = dim['hbar'] - dim['M'] - dim['c']
check('D1 l* = hbar/(M* c) has dimension L', np.array_equal(l_dim, [1, 0, 0]))
l_mut = dim['hbar'] - dim['M'] - 2 * dim['c']
check('NC1 mutant hbar/(M* c^2) is NOT a length', not np.array_equal(l_mut, [1, 0, 0]))
t1 = 2 * dim['c'] + 2 * dim['k']
t2 = 2 * dim['c'] + 4 * l_dim + 6 * dim['k']
check('D2 omega^2 = c^2k^2 + c^2 l*^4 k^6 homogeneous (T^-2)',
      np.array_equal(t1, 2 * dim['omega']) and np.array_equal(t2, 2 * dim['omega']))
check('D3 k^2 + l*^2 k^4 homogeneous (L^-2)', np.array_equal(2 * l_dim + 4 * dim['k'], 2 * dim['k']))
check('NC2 mutant l*^4 k^4 is not homogeneous with k^2',
      not np.array_equal(4 * l_dim + 4 * dim['k'], 2 * dim['k']))

hbar, c, G = C.hbar, C.c, C.G
GeV = 1e9 * C.e
M_P = np.sqrt(hbar * c / G)
lP1 = np.sqrt(hbar * G / c**3)
lP2 = hbar / (M_P * c)
print(f'CODATA: M_P c^2 = {M_P * c**2 / GeV:.5e} GeV, l_P = {lP1:.6e} m')
check('D4 l_P two routes agree (rel 1e-12)', abs(lP1 - lP2) / lP1 < 1e-12)
check('D4b order of magnitude: M_P c^2 ~ 1.22e19 GeV, l_P ~ 1.616e-35 m',
      abs(M_P * c**2 / GeV / 1.22e19 - 1) < 0.01 and abs(lP1 / 1.616e-35 - 1) < 0.01)

# D2 numerical agreement of the SI and natural-unit forms
Mstar = 1e16 * GeV / c**2
lstar = hbar / (Mstar * c)
k = 1e18  # m^-1, arbitrary
w2_SI = c**2 * k**2 + c**2 * lstar**4 * k**6
w2_nat = ((hbar * c * k)**2 + (hbar * c * k)**6 / (Mstar * c**2)**4) / hbar**2
check('D2b SI and natural-unit z=3 dispersion agree (rel 1e-12)', abs(w2_SI - w2_nat) / w2_SI < 1e-12)

f = 100.0
kGW = 2 * np.pi * f / c
print(f'\nGW at f = {f} Hz: k = {kGW:.3e} 1/m')
print(f'{"M* [GeV]":>12s} {"l* [m]":>12s} {"(3/2)(l k)^2 [z=2 ansatz, xi=1]":>34s} {"(5/2)(l k)^4 [z=3]":>20s}')
for MG in (M_P * c**2 / GeV, 1e16, 1e15, 1e10):
    ls = hbar * c / (MG * GeV)
    print(f'{MG:12.3e} {ls:12.3e} {1.5 * (ls * kGW)**2:34.3e} {2.5 * (ls * kGW)**4:20.3e}')
bound = 3e-15
l_z2 = np.sqrt(bound / 1.5) / kGW
l_z3 = (bound / 2.5)**0.25 / kGW
print(f'\nGW170817 |dv|/c < {bound:g} at 100 Hz  =>  l* < {l_z2:.2e} m (z=2 ansatz, xi=1);'
      f'  l* < {l_z3:.2e} m (z=3)')
print(f'   i.e. M* > {hbar * c / l_z2 / C.e:.2e} eV (z=2), M* > {hbar * c / l_z3 / C.e:.2e} eV (z=3)')
# sanity: the z=3 bound must be much weaker than the z=2 bound (quartic suppression)
check('O1 GW170817 bound is far weaker for z=3 than for the z=2 ansatz', l_z3 > 1e3 * l_z2)
# Horava consistency window (cited, BPS 2011; Pospelov-Shang 2012): 1e10 <~ M* <~ 1e15-16 GeV
for MG, lab in ((1e10, 'Pospelov-Shang ceiling / BPS photon-LV floor'), (1e16, 'BPS weak-coupling ceiling')):
    print(f'M* = {MG:.0e} GeV ({lab}): l* = {hbar * c / (MG * GeV):.2e} m = {hbar * c / (MG * GeV) / lP1:.1e} l_P')
check('O2 M* = M_P lies above the BPS weak-coupling ceiling 1e16 GeV', M_P * c**2 / GeV > 1e16)

print('\nSUMMARY: %d/%d PASS' % (sum(c for _, c in PASS), len(PASS)))
