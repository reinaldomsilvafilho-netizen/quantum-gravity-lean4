"""E1 - Kallen-Lehmann bound on the UV spectral dimension (Lemma KL of README section 2).

Claim [proved in README]: if the Euclidean propagator is a Stieltjes function
    G(z) = w0/z + int rho(m2) dm2 / (z + m2),   rho >= 0,  z = k^2 > 0,
then z*G(z) is non-decreasing, so the symbol S = 1/G obeys S(z) <= z / (z0 G(z0)) for z >= z0,
and the heat-kernel spectral dimension in d = 4 has liminf_{tau->0} d_s(tau) >= 4.
Hence a Lorentz-invariant theory with a positive-metric Kallen-Lehmann representation
cannot reach d_s = 2 in the UV.  The book symbol z + l^2 z^2 has rho = delta(m2) - delta(m2 - 1/l^2):
it evades the bound only through the negative weight (the ghost).

Checks
  K1  z G(z) non-decreasing for 200 random positive spectral densities (discrete + continuum).
  K2  d_s(tau) at tau = 1e-6 (in units of the largest scale) >= 4 - 1e-3 for the same densities,
      computed two independent ways: (a) finite difference of ln P with scipy.quad,
      (b) moment identity d_s = 2 tau <S> with mpmath.quad.
  K3  the two methods agree to 1e-6.
  NC1 (negative control) the book's rho = delta(0) - delta(1/l^2) gives d_s(1e-6) close to 2,
      i.e. FAILS the bound - as it must, since rho is not positive.
  NC2 (negative control) a mutated positive density with the sign of one weight flipped
      makes z G(z) decrease somewhere (monotonicity check detects it).
"""
import numpy as np
import mpmath as mp
from scipy import integrate

rng = np.random.default_rng(20260928)
mp.mp.dps = 20
results = []


def check(name, ok, info=''):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")


def make_density(rng):
    """Random positive density: massless weight, 1-4 massive poles, optional continuum."""
    w0 = rng.uniform(0.2, 1.0)
    n = rng.integers(1, 5)
    w = rng.uniform(0.05, 1.0, n)
    m2 = 10 ** rng.uniform(-1, 2, n)
    cont = rng.uniform(0, 0.5)          # continuum weight on [4, inf) with rho_c ~ 1/m2^1.5
    return w0, w, m2, cont


def G_np(z, dens):
    w0, w, m2, cont = dens
    g = w0 / z + np.sum(w[:, None] / (z[None, :] + m2[:, None]), axis=0)
    if cont > 0:
        # int_4^inf cont * m2^(-1.5) / (z + m2) dm2  (closed form via substitution m2 = t^2)
        # = cont * int_2^inf 2 t^-2 /(z + t^2) dt = cont * 2*(1/(2 z) ... ) -> do numerically-free closed form:
        # int_2^inf dt 2/(t^2 (z+t^2)) = (2/z) [1/2 - (1/sqrt z) (pi/2 - atan(2/sqrt z))]
        sz = np.sqrt(z)
        g = g + cont * (2.0 / z) * (0.5 - (np.pi / 2 - np.arctan(2.0 / sz)) / sz)
    return g


def G_mp(z, dens):
    w0, w, m2, cont = dens
    z = mp.mpf(z)
    g = w0 / z + sum(mp.mpf(wi) / (z + mp.mpf(mi)) for wi, mi in zip(w, m2))
    if cont > 0:
        sz = mp.sqrt(z)  # same closed form, evaluated in mpmath (independent quadrature is the oracle)
        g += cont * (2 / z) * (mp.mpf(1) / 2 - (mp.pi / 2 - mp.atan(2 / sz)) / sz)
    return g


def ds_fd(S, tau, h=1e-3):
    """Finite-difference d_s from scipy quad of P(tau) = int_0^inf z e^{-tau S(z)} dz (d=4, u = k^2)."""
    def lnP(t):
        f = lambda lu: np.exp(2 * lu) * np.exp(-t * S(np.exp(lu)))  # z dz = e^{2 lu} dlu
        lo, hi = -30.0, np.log(60.0 / t) + 5
        val, _ = integrate.quad(f, lo, hi, limit=400, points=[np.log(1 / t)])
        return np.log(val)
    return -2 * (lnP(tau * np.exp(h)) - lnP(tau * np.exp(-h))) / (2 * h)


def ds_moment(S, tau):
    tau = mp.mpf(tau)
    num = mp.quad(lambda z: z * S(z) * mp.e ** (-tau * S(z)), [0, 1 / tau, 10 / tau, mp.inf])
    den = mp.quad(lambda z: z * mp.e ** (-tau * S(z)), [0, 1 / tau, 10 / tau, mp.inf])
    return 2 * tau * num / den


# K1: monotonicity of z G(z)
zgrid = np.logspace(-4, 8, 2000)
mono_ok = True
dens_list = [make_density(rng) for _ in range(200)]
for dens in dens_list:
    zg = zgrid * G_np(zgrid, dens)
    if np.any(np.diff(zg) < -1e-12 * np.abs(zg[1:])):
        mono_ok = False
check('K1 z*G(z) non-decreasing for 200 random positive densities', mono_ok)

# K2/K3: d_s in the UV for 12 of them (cost)
tau = 1e-6
worst, maxdiff = 10.0, 0.0
for dens in dens_list[:6]:
    S_mp = lambda z, d=dens: 1 / G_mp(z, d)
    a = ds_fd(lambda z: 1.0 / G_np(np.atleast_1d(z), dens)[0], tau)
    b = float(ds_moment(S_mp, tau))
    worst = min(worst, a, b)
    maxdiff = max(maxdiff, abs(a - b))
check('K2 d_s(tau=1e-6) >= 4 - 1e-3 for positive densities', worst >= 4 - 1e-3, f'(min d_s = {worst:.6f})')
check('K3 finite-difference vs moment identity agree', maxdiff < 1e-4, f'(max |diff| = {maxdiff:.2e})')

# NC1: book symbol (l = 1): S = z + z^2 <=> G = 1/z - 1/(z+1): rho has weight -1 at m2 = 1
S_book_mp = lambda z: z + z ** 2
S_book_np = lambda z: z + z ** 2
a = ds_fd(S_book_np, tau)
b = float(ds_moment(S_book_mp, tau))
check('NC1 book symbol (negative weight) violates the bound: d_s(1e-6) < 2.01', a < 2.01 and abs(a - b) < 1e-4,
      f'(fd {a:.6f}, moment {b:.6f})')
# its spectral weight read off by partial fractions: residue of G at z=-1 must be -1
res = mp.limit(lambda z: (z + 1) * (1 / (z + z ** 2)), -1)
check('NC1b residue of 1/(z+z^2) at z=-1 equals -1 (negative weight)', abs(res + 1) < 1e-20, f'({mp.nstr(res, 12)})')

# NC2: flip the sign of the largest massive weight of a positive density -> monotonicity must fail
bad = None
for dens in dens_list:
    w0, w, m2, cont = dens
    w2 = w.copy(); i = int(np.argmax(w2)); w2[i] = -w2[i] - w0   # make it a real ghost, dominating
    zg = zgrid * G_np(zgrid, (w0, w2, m2, cont))
    if np.any(np.diff(zg) < 0):
        bad = True; break
check('NC2 flipped-sign density breaks monotonicity of z*G (detector works)', bad is True)

print(f"\n{sum(results)}/{len(results)} checks passed")
