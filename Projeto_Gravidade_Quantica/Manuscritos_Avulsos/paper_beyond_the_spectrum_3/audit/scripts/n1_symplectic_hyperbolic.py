"""OBL-001 (EH bound on quadratic Phi) and OBL-009 (slim constant of ideal triangle).
Oracle 1: symplectic eigenvalues via eig(J Q) and via eig(Q^1/2 J Q^1/2) (independent route).
Oracle 2: hyperbolic distance point->geodesic by direct minimisation over the geodesic.
Negative controls: swapped EH bound must fail; 'inradius' constant ln3/2 is not the slim constant."""
import numpy as np, sys
from scipy.linalg import sqrtm
from scipy.optimize import minimize_scalar
rng = np.random.default_rng(12345)
fails = 0


def J(n):
    return np.block([[np.zeros((n, n)), np.eye(n)], [-np.eye(n), np.zeros((n, n))]])


viol, neg_fail = 0, 0
for trial in range(2000):
    n = rng.integers(1, 4)
    X = rng.normal(size=(2 * n, 2 * n))
    Q = X @ X.T + 0.1 * np.eye(2 * n)
    t = 1.7
    lam = np.linalg.eigvalsh(Q)
    d1 = np.sort(np.abs(np.linalg.eigvals(J(n) @ Q).imag))[-1]
    S = np.real(sqrtm(Q))
    d2 = np.sort(np.abs(np.linalg.eigvals(S @ J(n) @ S).imag))[-1]
    if abs(d1 - d2) > 1e-8 * d1:
        fails += 1
    c1 = 2 * np.pi * t / d1  # c1 of ellipsoid {x^T Q x/2 <= t}
    lo, hi = 2 * np.pi * t / lam[-1], 2 * np.pi * t / lam[0]
    if not (lo - 1e-9 <= c1 <= hi + 1e-9):
        viol += 1
    if not (2 * np.pi * t / lam[0] <= c1 + 1e-9):  # mutated (swapped) lower bound
        neg_fail += 1
print('OBL-001 quadratic test: violations of paper bound =', viol, '/2000 ; mutated bound fails in', neg_fail, '/2000')
fails += (viol != 0) + (neg_fail == 0)


# OBL-009: ideal triangle with vertices -1, 1, infinity in upper half-plane
def dH(z, w):
    return np.arccosh(1 + abs(z - w) ** 2 / (2 * z.imag * w.imag))


def dist_to_vertical(z, x0):
    f = lambda ly: dH(z, complex(x0, np.exp(ly)))
    return minimize_scalar(f, bounds=(-12, 12), method='bounded', options={'xatol': 1e-12}).fun


best = 0
for th in np.linspace(0.01, np.pi - 0.01, 2001):
    z = complex(np.cos(th), np.sin(th))
    best = max(best, min(dist_to_vertical(z, -1), dist_to_vertical(z, 1)))
print('OBL-009 slim constant (numeric) = %.6f ; ln(1+sqrt2) = %.6f ; inradius ln3/2 = %.6f' % (best, np.log(1 + np.sqrt(2)), np.log(3) / 2))
fails += abs(best - np.log(1 + np.sqrt(2))) > 1e-4
fails += abs(best - np.log(3) / 2) < 1e-2  # negative control: must differ from inradius
print('failures:', fails)
sys.exit(int(fails))
