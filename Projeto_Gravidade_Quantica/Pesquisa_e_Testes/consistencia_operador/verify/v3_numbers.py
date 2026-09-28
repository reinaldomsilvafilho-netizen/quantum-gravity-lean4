"""Independent verifier: M* windows -> l*, delay rescaling, '10^56 -> 10^38', GW170817 l* bounds.

Oracle: delay recomputed from the book's formula |dt| = 6 pi^2 xi l^2 / c^3 * D2(z) (f2^2 - f1^2)
with scipy quad (the draft only rescaled the quoted numbers). CODATA 2018 via scipy.constants.
Dimensional check done by hand in VERIFICACAO.md: [l^2/c^3 * m * s^-2] = m^2 s^3 m^-3 m s^-2 = s.
Negative control: using l instead of l^2 (linear rescaling) must not reproduce the book numbers.
"""
import numpy as np
from scipy import constants as C
from scipy.integrate import quad

ok = []


def check(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


hbar, c, G = C.hbar, C.c, C.G
GeV = 1e9 * C.e
lP = np.sqrt(hbar * G / c**3)
MPc2 = np.sqrt(hbar * c**5 / G) / GeV
print(f"l_P = {lP:.6e} m, M_P c^2 = {MPc2:.5e} GeV")
check("CODATA l_P ~ 1.616e-35 m, M_P ~ 1.221e19 GeV", abs(lP / 1.616255e-35 - 1) < 1e-5 and abs(MPc2 / 1.22089e19 - 1) < 1e-4)

H0 = 70e3 / 3.0856775814913673e22
Om = 0.3


def dt(z, lstar, xi=0.5, f1=10.0, f2=1e3):
    D2 = c / H0 * quad(lambda x: (1 + x) ** 2 / np.sqrt(Om * (1 + x) ** 3 + 1 - Om), 0, z)[0]
    return 6 * np.pi**2 * xi * lstar**2 / c**3 * D2 * (f2**2 - f1**2)


book = {1: 6e-62, 3: 3e-61, 8: 1.2e-60}
for z, v in book.items():
    print(f"z={z}: dt(l_P) = {dt(z, lP):.2e} s (book {v:.1e})")
check("book delays 6e-62, 3e-61, 1.2e-60 s reproduced (to 1 significant figure)",
      all(abs(dt(z, lP) / v - 1) < 0.1 for z, v in book.items()))

for M in (1e10, 1e15, 1e16):
    ls = hbar * c / (M * GeV)
    r = ls / lP
    d1, d8 = dt(1, ls), dt(8, ls)
    print(f"M*={M:.0e} GeV: l* = {ls:.3e} m = {r:.3e} l_P, (l*/l_P)^2 = {r**2:.3e}; dt = {d1:.2e} .. {d8:.2e} s;"
          f" orders below 1e-4 s: {np.log10(1e-4/d8):.1f} .. {np.log10(1e-4/d1):.1f}")
    if M == 1e10:
        check("draft: l* = 2e-26 m ~ 1.2e9 l_P at 1e10 GeV", abs(ls / 1.973e-26 - 1) < 1e-3 and abs(r / 1.2e9 - 1) < 0.03)
        check("draft: (l*/l_P)^2 ~ 1.5e18", abs(r**2 / 1.5e18 - 1) < 0.02)
        check("draft: delays ~1e-43 .. 2e-42 s (rounded; exact 9e-44 .. 1.8e-42)", 5e-44 < d1 < 2e-43 and 1e-42 < d8 < 3e-42)
        check("draft: 38-40 orders below 1e-4 s", 37.5 < np.log10(1e-4 / d8) and np.log10(1e-4 / d1) < 40.5)
        check("NC linear rescaling (l instead of l^2) does not give ~1e-43", abs(np.log10(dt(1, lP) * r) - np.log10(d1)) > 5)
    if M == 1e16:
        check("draft 7.3: at M*=1e16 GeV factor ~1.5e6 and ~50 orders", abs(r**2 / 1.5e6 - 1) < 0.02 and 49 < np.log10(1e-4 / d8) < 52)
check("M_P above the BPS weak-coupling ceiling 1e15-1e16 GeV", MPc2 > 1e16)
print("10^56 -> ? : 56 - log10(1.49e18) =", round(56 - np.log10((hbar * c / (1e10 * GeV) / lP) ** 2), 1))

# GW170817 bounds (|dv|/c < 3e-15 at 100 Hz)
k = 2 * np.pi * 100 / c
l2 = np.sqrt(3e-15 / 1.5) / k      # xi=1 quartic: dv/c = (3/2)(lk)^2
l3 = (3e-15 / 2.5) ** 0.25 / k     # z=3: dv/c = (5/2)(lk)^4
print(f"GW170817: l* < {l2:.2e} m (quartic, xi=1), l* < {l3:.1f} m (z=3)")
check("draft: l* < 2e-2 m (quartic) and < 89 m (z=3)", abs(l2 / 2.13e-2 - 1) < 0.02 and abs(l3 / 88.8 - 1) < 0.02)
# group velocity coefficient check for omega = k sqrt(1 + x^4): v = (1+3x^4)/sqrt(1+x^4) ~ 1 + 5/2 x^4
x = 1e-2
check("z=3 group velocity excess (5/2)x^4", abs(((1 + 3 * x**4) / np.sqrt(1 + x**4) - 1) / (2.5 * x**4) - 1) < 1e-6)
print(f"\nSUMMARY: {sum(ok)}/{len(ok)} PASS")
