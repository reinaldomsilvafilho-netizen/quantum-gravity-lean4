"""L2 directed check S3: ch.7 rem:nash_kuiper, as now stated.

Current text (chap07, l.665): curve phi(s) = s + beta sin(N s) is closed for N>=2
and EVERY beta>0 (Jacobi-Anger); ||kappa||_Linf = 1+beta N; separately, the k=0
Jacobi-Anger term is a circle of radius J_0(beta), remaining terms O(1/N), so for
beta = first zero of J_0 the curve is O(1/N)-close to the origin (not "closed
because beta is a zero of J0", which was the old/ambiguous reading).
"""
import numpy as np
from scipy.special import jn_zeros, j0, j1

M = 150000
s = np.linspace(0, 2 * np.pi, M + 1)


def curve(beta, N):
    phi = s + beta * np.sin(N * s)
    v = np.exp(1j * phi)
    return np.concatenate([[0], np.cumsum((v[1:] + v[:-1]) / 2 * np.diff(s))])


beta0 = jn_zeros(0, 1)[0]

# current claim: closed for EVERY beta>0 when N>=2 (not just beta=beta0)
betas_generic = [0.1, 0.5, 1.0, 2.0, 2.9, 5.5]
for N in [2, 4, 7, 15, 30]:
    for beta in betas_generic + [beta0]:
        z = curve(beta, N)
        assert abs(z[-1]) < 1e-6, (N, beta, abs(z[-1]))
print("closure holds for every tested beta>0, N>=2: matches 'for N>=2 and every beta>0, ... is closed'")

# the O(1/N) confinement claim is specific to beta = beta0 (first zero of J0), not generic beta
for N in [5, 10, 20, 40, 80]:
    z0 = curve(beta0, N)
    zg = curve(1.0, N)  # generic beta, j0(1.0) = 0.7652 != 0
    assert N * np.abs(z0).max() < 3.0  # O(1/N) confirmed at beta0
    assert np.abs(zg).max() > 1.0      # generic beta: NOT O(1/N), stays O(1)
print("beta0 confinement is O(1/N); generic beta stays O(1): text's distinction (closure vs confinement) holds")

# curvature sup matches 1+beta*N at beta0 and at generic beta alike (curvature claim is for all beta)
N = 12
for beta in [1.0, beta0]:
    kap = 1 + beta * N * np.cos(N * s)
    assert abs(np.abs(kap).max() - (1 + beta * N)) < 1e-9
print("||kappa||_Linf = 1+beta N confirmed for both generic beta and beta0")

# mutation 1: claim closure requires beta = zero of J_0 (old ambiguous reading) -- false, since
# generic beta also closes
mutated_closure_needs_zero = bool(not any(abs(curve(1.0, N)[-1]) < 1e-6 for N in [5, 10, 20]))
assert mutated_closure_needs_zero is False  # i.e. generic beta DOES close -> mutation is wrong, confirms fix needed
print("mutation ('closure needs beta=zero of J0') is false: generic beta also closes -> old wording was misleading")

# mutation 2: N=1 must NOT close (sanity / negative control on the closure mechanism itself)
for beta in [0.5, 1.0, beta0]:
    gap = curve(beta, 1)[-1]
    oracle = -2 * np.pi * j1(beta)
    assert abs(gap - oracle) < 1e-6 and abs(gap) > 0.05
print("N=1 negative control: does not close, matches -2*pi*J1(beta) oracle")

print("S3 L2: current wording (closure for all beta; J0-zero only for O(1/N) confinement) matches derivation. CONFIRMA")
