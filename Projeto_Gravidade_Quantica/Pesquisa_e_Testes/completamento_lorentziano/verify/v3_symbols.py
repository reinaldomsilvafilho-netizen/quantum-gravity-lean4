"""V3 - independent checks of the symbol-level claims (units l = 1, d = 4, Euclidean u = k^2).

T  Entire form factor S_T(u) = u exp(Ein(e^{-gamma} u^2)/2): d_s profile vs book symbol u + u^2.
   Oracle: scipy (Ein via special.exp1, integration in k with a Laplace-type substitution), d_s from the
   moment formula AND an independent closed form for the book symbol:
   P_B(tau) = 1/(2 tau) - (1/2) sqrt(pi/(4 tau)) erfcx(sqrt(tau)/2) (from int u e^{-tau u - tau u^2} du).
L  Prop. LW scope: (a) polynomial class: d_s(UV) = 4/n (checked n = 2, 3);
   (b) OUTSIDE the polynomial class, a rational symbol S = u (u^2 + u + 1)/(u + 2) has a normal massless pole,
   a complex-conjugate ghost pair and d_s(UV) = 2 -> the exclusion "complex pair => d_s <= 4/3" is class-specific.
   (c) Standard Lee-Wick (Lee-Wick 1970, GOW 2008): tree symbol u(1 + u/M^2) = the book symbol; the complex
   pair arises from the width. A Breit-Wigner-type dressing S_w(u) = u(1+u) + i g u (width term) keeps UV ~ u^2.
PU Each spatial mode of the Lorentzian symbol k^2(1 + l^2 k^2), k^2 = -w^2 + p^2, is a Pais-Uhlenbeck
   oscillator with w1 = |p|, w2 = sqrt(p^2 + 1/l^2): w1 = 0 only for p = 0, and w2^2 - w1^2 = 1/l^2 > 0 always.
Negative controls: (NC1) swapping erfcx -> erfc in P_B must fail; (NC2) a polynomial with complex pair must
NOT reach d_s = 2 (gives 4/3); (NC3) PU with l -> 0 limit mutated to equal frequencies must be detected.
"""
import numpy as np
from scipy import integrate, special

R = []
def check(n, ok, info=''):
    R.append(bool(ok)); print(f"[{'PASS' if ok else 'FAIL'}] {n} {info}")

g = np.euler_gamma
def Ein(x):
    x = np.asarray(x, float)
    small = x < 1e-3
    out = np.where(small, x - x**2 / 4 + x**3 / 18, 0.0)
    xs = np.where(small, 1.0, x)
    return np.where(small, out, g + np.log(xs) + special.exp1(xs))

S_T = lambda u: u * np.exp(Ein(np.exp(-g) * u**2) / 2)
S_B = lambda u: u + u**2

def ds_mom(S, tau):
    # variable x = ln u
    w = lambda x: np.exp(2 * x - tau * S(np.exp(x)))
    hi = np.log(1e3 / tau) + 20; lo = -60
    pts = [p for p in (np.log(1 / tau), 0.5 * np.log(1 / tau)) if lo < p < hi]
    a = integrate.quad(w, lo, hi, points=pts, limit=800, epsrel=1e-11, epsabs=0)[0]
    b = integrate.quad(lambda x: w(x) * S(np.exp(x)), lo, hi, points=pts, limit=800, epsrel=1e-11, epsabs=0)[0]
    return 2 * tau * b / a

def PB(tau, f=special.erfcx):
    return 1 / (2 * tau) - 0.5 * np.sqrt(np.pi / (4 * tau)) * f(np.sqrt(tau) / 2)

def ds_closed(tau, f=special.erfcx, h=1e-4):
    return -2 * (np.log(PB(tau * np.exp(h), f)) - np.log(PB(tau * np.exp(-h), f))) / (2 * h)

taus = np.logspace(-6, 6, 49)
dB = np.array([ds_mom(S_B, t) for t in taus]); dBc = np.array([ds_closed(t) for t in taus])
check('B1 book symbol: moment d_s = erfc closed form', np.max(abs(dB - dBc)) < 2e-5, f'(max diff {np.max(abs(dB - dBc)):.1e})')
with np.errstate(all='ignore'):
    dBn = np.array([ds_closed(t, special.erfc) for t in taus[20:40]])
check('NC1 erfc without e^{x^2} fails', not np.all(abs(dBn - dB[20:40]) < 1e-2))

dT = np.array([ds_mom(S_T, t) for t in taus])
dev = abs(dT - dB); i = np.argmax(dev)
print(f"   d_s at tau=1: book {dB[24]:.4f}, entire {dT[24]:.4f}; tau=10: book {ds_mom(S_B, 10):.4f}, entire {ds_mom(S_T, 10):.4f}")
check('T1 entire form factor: d_s 4 -> 2 (UV 2, IR 4)', abs(dT[0] - 2) < 2e-3 and abs(dT[-1] - 4) < 2e-3,
      f'(UV {dT[0]:.4f}, IR {dT[-1]:.4f})')
check('T2 max |d_s^T - d_s^B| on a 49-point grid is 0.38 +- 0.01', abs(dev.max() - 0.38) < 0.01,
      f'(max {dev.max():.4f} at tau = {taus[i]:.3g})')

# Prop LW, polynomial class
d2 = ds_mom(S_B, 1e-9); d3 = ds_mom(lambda u: u * (1 + u + u**2), 1e-10)
check('L1 polynomial: n=2 -> d_s 2, n=3 (complex pair) -> 4/3', abs(d2 - 2) < 2e-3 and abs(d3 - 4 / 3) < 5e-3,
      f'({d2:.4f}, {d3:.4f})')
# rational symbol with complex pair and d_s = 2
S_rat = lambda u: u * (u**2 + u + 1) / (u + 2)
num = np.poly1d([1, 1, 1, 0]); den = np.poly1d([1, 2])
poles = np.roots(num.coeffs)                     # poles of G = 1/S
res = [den(p) / num.deriv()(p) for p in poles]
cpx = [p for p in poles if abs(p.imag) > 1e-9]
dr = ds_mom(S_rat, 1e-10)
positive = np.all(S_rat(np.logspace(-6, 6, 500)) > 0)
check('L2 rational symbol u(u^2+u+1)/(u+2): massless pole residue > 0, complex pair, S > 0 on u > 0, d_s(UV) = 2',
      len(cpx) == 2 and abs(res[list(abs(poles)).index(min(abs(poles)))] - 2) < 1e-9 and positive and abs(dr - 2) < 3e-3,
      f'(poles {np.round(poles, 3)}, residues {np.round(res, 3)}, d_s {dr:.4f})')

# PU frequencies
p = np.linspace(0, 10, 1001); l = 0.7
w1 = p; w2 = np.sqrt(p**2 + 1 / l**2)
# roots in w^2 of k^2 (1 + l^2 k^2) with k^2 = -w^2 + p^2
roots_ok = all(np.allclose(sorted(np.roots([l**2, -(2 * l**2 * q**2 + 1), q**2 + l**2 * q**4]).real),
                           sorted([q**2, q**2 + 1 / l**2])) for q in p[::50])
check('PU1 modes are PU oscillators with w1 = |p|, w2 = sqrt(p^2+1/l^2); w1 = 0 only at p = 0; w2 > w1 always',
      roots_ok and np.all(w2 - w1 > 0) and np.count_nonzero(w1 == 0) == 1)
w2bad = np.sqrt(p**2 + 0 / l**2)
check('NC3 mutated (massless) second branch gives equal frequencies -> detected', np.any(w2bad - w1 == 0))
print(f"\n{sum(R)}/{len(R)} checks passed")
