"""V1 - independent check of Lemma KL, in a STRONGER (pointwise) form.

Claim to test: if G(z) = w0/z + sum_i r_i/(z+m_i) with w0 >= 0, r_i >= 0 (positive Kallen-Lehmann
measure, Euclidean z = k^2), then the heat-kernel spectral dimension of the symbol S = 1/G,
    P(tau) = int_0^inf z exp(-tau S(z)) dz   (d = 4),   d_s(tau) = -2 dlnP/dln tau,
satisfies d_s(tau) >= 4 for EVERY tau (not only liminf as tau -> 0).

Proof sketch (verifier's, independent of the README): zG nondecreasing => S/z nonincreasing =>
the inverse h = S^{-1} has h(s)/s nondecreasing. Substituting s = S(z): P = tau int q(s) e^{-tau s} ds,
q = h^2/2 = s^2 m(s) with m nondecreasing. Then -dlnP/dln tau = -1 + <tau s>_q and, by Chebyshev's
association inequality under the Gamma(3) density s^2 e^{-tau s}, <tau s>_q >= 3. Hence d_s >= 4.

Oracle: P(tau) computed in the variable x = ln z with scipy.quad (different quadrature and variable
from the author's mpmath moment identity), d_s by the moment formula
    d_s = 2 tau <S>, <.> w.r.t. z e^{-tau S} dz,
cross-checked with a central finite difference of ln P.
Negative controls: (NC1) book symbol S = z + z^2 (weight -1) must dip below 4;
(NC2) one flipped residue in a random positive measure must dip below 4 somewhere or break S/z monotonic.
"""
import numpy as np
from scipy import integrate

rng = np.random.default_rng(20260928)
R = []


def check(name, ok, info=''):
    R.append(bool(ok)); print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")


def make_S(w0, r, m):
    def G(z):
        return w0 / z + np.sum(r / (z + m))
    return lambda z: 1.0 / G(z)


def moments(S, tau):
    # integrate in x = ln z: dz = z dx; weights shifted by S0 = S(0+) to avoid underflow (gapped case)
    S0 = S(1e-200)
    f0 = lambda x: np.exp(2 * x - tau * (S(np.exp(x)) - S0))
    f1 = lambda x: np.exp(2 * x - tau * (S(np.exp(x)) - S0)) * tau * S(np.exp(x))
    lo, hi = -60.0, np.log(1e3 / tau) + 25
    pts = [np.log(1 / tau), 0.5 * np.log(1 / tau)]
    pts = [p for p in pts if lo < p < hi]
    a, _ = integrate.quad(f0, lo, hi, points=pts, limit=800, epsabs=0, epsrel=1e-11)
    b, _ = integrate.quad(f1, lo, hi, points=pts, limit=800, epsabs=0, epsrel=1e-11)
    return a, b


def ds(S, tau):
    a, b = moments(S, tau)
    return 2 * b / a


def ds_fd(S, tau, h=1e-4):
    ap, _ = moments(S, tau * np.exp(h)); am, _ = moments(S, tau * np.exp(-h))
    return -2 * (np.log(ap) - np.log(am)) / (2 * h)


taus = np.logspace(-6, 6, 25)
mins, fd_err = [], 0.0
for trial in range(40):
    n = rng.integers(1, 5)
    m = 10 ** rng.uniform(-3, 3, n); r = 10 ** rng.uniform(-2, 2, n)
    w0 = rng.choice([0.0, 10 ** rng.uniform(-2, 1)])
    if w0 == 0.0:
        w0 = 1e-12  # keep S(0)=0 finite limit; w0=0 case handled below separately
    S = make_S(w0, r, m)
    d = [ds(S, t) for t in taus]
    mins.append(min(d))
    if trial < 5:
        fd_err = max(fd_err, max(abs(ds_fd(S, t) - ds(S, t)) for t in taus[::6]))
check('K1 pointwise d_s(tau) >= 4 on 25 tau in [1e-6,1e6] for 40 random positive measures',
      min(mins) > 4 - 1e-6, f'(min d_s = {min(mins):.6f})')
check('K2 moment formula = finite difference of ln P (independent route)', fd_err < 1e-5,
      f'(max diff {fd_err:.1e})')

# gapped case w0 = 0: massive positive spectral measure only -> still d_s >= 4
S = make_S(0.0, np.array([1.0, 3.0]), np.array([1.0, 50.0]))
dmin = min(ds(S, t) for t in taus)
check('K3 gapped positive measure (w0 = 0): d_s >= 4 pointwise', dmin > 4 - 1e-6, f'(min {dmin:.6f})')

# NC1 book symbol
SB = lambda z: z + z * z
dB = [ds(SB, t) for t in taus]
check('NC1 book symbol (weight -1) violates the bound', min(dB) < 3.9, f'(min d_s = {min(dB):.4f})')

# NC2 flipped residue: G = 1/z + 2/(z+1) - 1.5/(z+4)  (still positive G on z>0)
Gf = lambda z: 1 / z + 2 / (z + 1) - 1.5 / (z + 4)
zz = np.logspace(-4, 4, 2000)
positive = np.all(Gf(zz) > 0)
Sf = lambda z: 1 / Gf(z)
mono = np.all(np.diff(Sf(zz) / zz) <= 1e-14)
dF = [ds(Sf, t) for t in taus]
check('NC2 flipped residue: detector fires (S/z non-monotone or d_s < 4)', positive and ((not mono) or min(dF) < 4 - 1e-4),
      f'(S/z monotone: {mono}; min d_s = {min(dF):.5f})')

print(f"\n{sum(R)}/{len(R)} checks passed")
