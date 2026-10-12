"""L1 blind check S3: ch.7 rem:nash_kuiper, curve with tangent angle phi(s) = s + beta sin(N s), s in [0, 2pi].

Hand derivation: e^{i beta sin(Ns)} = sum_k J_k(beta) e^{ikNs}, so the closure integral
  int_0^{2pi} e^{i phi} ds = 2pi sum_k J_k(beta) [1 + kN = 0] = 0 for every beta when N >= 2.
Position z(s) = sum_k J_k(beta) (e^{i(1+kN)s} - 1) / (i(1+kN)); the k = 0 term is a circle of radius J_0(beta),
so the curve stays O(1/N)-close to the origin iff J_0(beta) = 0 (up to O(1/N)).
Oracle: direct quadrature (independent of the Bessel series). Negative controls: N = 1 must NOT close
(gap = 2pi J_1(beta)); beta not a zero of J_0 must NOT give max|z| = O(1/N).
"""
import numpy as np
from scipy.special import jn_zeros, j0, j1

M = 200000
s = np.linspace(0, 2 * np.pi, M + 1)


def curve(beta, N):
    phi = s + beta * np.sin(N * s)
    v = np.exp(1j * phi)
    z = np.concatenate([[0], np.cumsum((v[1:] + v[:-1]) / 2 * np.diff(s))])
    return z


beta0 = jn_zeros(0, 1)[0]
print("beta0 =", beta0)
for N in [2, 3, 5, 10, 20, 40]:
    for beta in [0.3, 1.0, beta0, 3.7]:
        z = curve(beta, N)
        assert abs(z[-1]) < 1e-6, (N, beta, abs(z[-1]))  # closed for every beta
    zb = curve(beta0, N)
    zr = curve(1.0, N)
    print(f"N={N:3d} closed for all beta; max|z| beta0: {np.abs(zb).max():.4f} (N*max|z|={N*np.abs(zb).max():.3f}); "
          f"beta=1: {np.abs(zr).max():.4f}; kappa*R(beta0) = {(1+beta0*N)*np.abs(zb).max():.3f}")
    assert (1 + beta0 * N) * np.abs(zb).max() >= 1  # consistent with prop:ball_bound (ball centred at 0)
# O(1/N) at beta0
assert 40 * np.abs(curve(beta0, 40)).max() < 3
# negative control 1: beta = 1 (J_0(1) = 0.765) leaves an O(1) circle
assert np.abs(curve(1.0, 40)).max() > 1.0
# negative control 2: N = 1 does not close; oracle 2 pi J_{-1}(beta) = -2 pi J_1(beta)
for beta in [0.3, 1.0, beta0]:
    gap = curve(beta, 1)[-1]
    assert abs(gap - (-2 * np.pi * j1(beta))) < 1e-6 and abs(gap) > 0.1
# curvature sup
N = 10; kap = 1 + beta0 * N * np.cos(N * s)
print("max|kappa| =", np.abs(kap).max(), " 1+beta0 N =", 1 + beta0 * N, " J0(beta0) =", j0(beta0))
print("S3: closure holds for every beta (N>=2); J_0(beta)=0 is needed only for the O(1/N) confinement. PASS")
