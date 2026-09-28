"""Branch (c) support: is exp(-tau psi(-Lap)) a probability (Markov) kernel?

K_tau(r) = (2 pi)^{-d/2} r^{1-d/2} int_0^inf k^{d/2} J_{d/2-1}(kr) exp(-tau psi(k)) dk.
Cases:
  iso4  : d = 4, psi = k^2 + k^4           (book's isotropic symbol, l = 1)
  hl3   : d = 3, psi = k^2 + k^6           (spatial part of the z = 3 branch, M = 1)
  gauss : d = 4, psi = k^2                 (NEGATIVE CONTROL: exact Gaussian, must stay >= 0)
Oracle 1: mpmath (30 digits), oracle 2: scipy quad.  Gaussian also checked against the exact
closed form (4 pi tau)^{-2} exp(-r^2/(4 tau)).
Theory (proved in README, Prop. C1): by Schoenberg/Bochner, exp(-tau psi) is positive definite
for ALL tau > 0 iff psi is negative definite, and a continuous negative-definite psi obeys
|psi(k)| <= C (1 + |k|^2); psi = k^2 + k^4 violates this, so K_tau < 0 somewhere for some tau.
Also reported: the total negative mass  int max(-K,0) d^dx  (normalisation int K = 1).
"""
import numpy as np
import mpmath as mp
from scipy.integrate import quad
from scipy.special import jv

mp.mp.dps = 30
PASS = []


def check(name, cond):
    PASS.append((name, bool(cond)))
    print(('PASS ' if cond else 'FAIL ') + name)


def K_mp(r, tau, d, psi):
    nu = mp.mpf(d) / 2 - 1
    kmax = 60 / tau**0.25 if d == 4 else 30 / tau**(1 / 6.)
    f = lambda k: k**(mp.mpf(d) / 2) * mp.besselj(nu, k * r) * mp.e**(-tau * psi(k))
    n = 40
    pts = [kmax * i / n for i in range(n + 1)]
    val = mp.quad(f, pts)
    return float(val / ((2 * mp.pi)**(mp.mpf(d) / 2) * r**nu))


def K_sp(r, tau, d, psi):
    nu = d / 2 - 1
    kmax = 60 / tau**0.25 if d == 4 else 30 / tau**(1 / 6.)
    f = lambda k: k**(d / 2) * jv(nu, k * r) * np.exp(-tau * psi(k))
    step = min(kmax / 40, 10 * np.pi / r)
    edges = np.arange(0, kmax + step, step)
    val = sum(quad(f, a, b, limit=200, epsabs=0, epsrel=1e-12)[0] for a, b in zip(edges[:-1], edges[1:]))
    return val / ((2 * np.pi)**(d / 2) * r**nu)


area = {3: 4 * np.pi, 4: 2 * np.pi**2}
cases = {
    'iso4': (4, lambda k: k**2 + k**4, lambda k: k**2 + k**4),
    'hl3': (3, lambda k: k**2 + k**6, lambda k: k**2 + k**6),
    'gauss': (4, lambda k: k**2, lambda k: k**2),
}

results = {}
for name, (d, psi_mp, psi_np) in cases.items():
    for tau in (0.01, 1.0):
        if name == 'gauss':
            L = np.sqrt(tau)
        elif name == 'iso4':
            L = max(tau**0.25, np.sqrt(tau))
        else:
            L = max(tau**(1 / 6.), np.sqrt(tau))
        rs = np.linspace(1e-3 * L, 30 * L, 1500)
        Ks = np.array([K_sp(r, tau, d, psi_np) for r in rs])
        imin = int(np.argmin(Ks))
        kmin_mp = K_mp(rs[imin], tau, d, psi_mp)
        agree = abs(kmin_mp - Ks[imin]) <= 1e-7 * np.max(np.abs(Ks)) + 1e-12
        w = area[d] * rs**(d - 1)
        mass = np.trapezoid(w * Ks, rs)
        negmass = np.trapezoid(w * np.clip(-Ks, 0, None), rs)
        ratio = Ks[imin] / np.max(Ks)
        results[(name, tau)] = (ratio, negmass, mass, agree)
        print(f'{name:5s} tau={tau:5.2f}: min K / max K = {ratio:+.3e} at r={rs[imin]:.3f}; '
              f'int K = {mass:.5f}; negative mass = {negmass:.3e}; mpmath vs scipy agree: {agree}')
        check(f'{name} tau={tau}: two quadratures agree at the minimum', agree)
        if name == 'gauss':
            exact = (4 * np.pi * tau)**-2 * np.exp(-rs**2 / (4 * tau))
            relerr = np.max(np.abs(Ks - exact)) / np.max(exact)
            print(f'      Gaussian vs exact closed form: max rel err {relerr:.1e}')
            check(f'NC gauss tau={tau}: matches exact heat kernel', relerr < 1e-8)
            check(f'NC gauss tau={tau}: no negative values (control must NOT show negativity)',
                  np.min(Ks) > -1e-14 * np.max(Ks))
        else:
            check(f'{name} tau={tau}: normalisation int K d^dx = 1 (to 1e-3)', abs(mass - 1) < 1e-3)
            check(f'{name} tau={tau}: kernel takes negative values (not a probability density)',
                  ratio < -1e-4)

print('\nSUMMARY: %d/%d PASS' % (sum(c for _, c in PASS), len(PASS)))
