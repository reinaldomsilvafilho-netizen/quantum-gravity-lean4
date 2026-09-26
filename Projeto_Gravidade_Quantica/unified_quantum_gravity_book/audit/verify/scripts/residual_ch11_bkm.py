"""BKM/SLD ratio for Hilbert-Schmidt random qutrits, random traceless Hermitian tangent X.
Oracle for BKM: numerical second derivative of relative entropy S(rho+tX || rho) (independent of the
log-mean formula). SLD from the closed form 2/(p_i+p_j). Negative control: commuting X gives ratio 1.
Also: the ratio is unbounded (explicit family p -> 0).
"""
import numpy as np
from scipy.linalg import logm

rng = np.random.default_rng(7)


def hs_state(n=3):
    G = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    r = G @ G.conj().T
    return r / np.trace(r).real


def herm_traceless(n=3):
    A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    H = (A + A.conj().T) / 2
    return H - np.trace(H) / n * np.eye(n)


def S(a, b):
    return np.trace(a @ (logm(a) - logm(b))).real


def bkm_fd(rho, X, t=1e-4):
    return 2 * S(rho + t * X, rho) / t**2  # S = t^2/2 g + O(t^3)


def sld(rho, X):
    p, U = np.linalg.eigh(rho)
    Xe = U.conj().T @ X @ U
    return sum(2 / (p[i] + p[j]) * abs(Xe[i, j]) ** 2 for i in range(3) for j in range(3))


def bkm(rho, X):
    p, U = np.linalg.eigh(rho)
    Xe = U.conj().T @ X @ U
    tot = 0
    for i in range(3):
        for j in range(3):
            c = 1 / p[i] if abs(p[i] - p[j]) < 1e-14 else (np.log(p[i]) - np.log(p[j])) / (p[i] - p[j])
            tot += c * abs(Xe[i, j]) ** 2
    return tot


# oracle agreement on a few samples
for _ in range(5):
    r, X = hs_state(), herm_traceless()
    assert abs(bkm_fd(r, X) / bkm(r, X) - 1) < 1e-3
ratios = []
for _ in range(5000):
    r, X = hs_state(), herm_traceless()
    ratios.append(bkm(r, X) / sld(r, X))
ratios = np.array(ratios)
print("min %.3f median %.3f p95 %.3f max %.3f" % (ratios.min(), np.median(ratios),
                                                 np.percentile(ratios, 95), ratios.max()))
assert ratios.min() >= 1 - 1e-12
# negative control: commuting perturbation -> ratio exactly 1
r = hs_state(); p, U = np.linalg.eigh(r)
Xc = U @ np.diag([0.1, -0.05, -0.05]) @ U.conj().T
print("commuting ratio", bkm(r, Xc) / sld(r, Xc))
assert abs(bkm(r, Xc) / sld(r, Xc) - 1) < 1e-12
# unbounded family
for e in (1e-2, 1e-4, 1e-8):
    rho = np.diag([e, 0.5 - e / 2, 0.5 - e / 2]).astype(complex)
    X = np.zeros((3, 3), complex); X[0, 1] = X[1, 0] = 1
    print("eps", e, "ratio %.2f" % (bkm(rho, X) / sld(rho, X)))
print("OK")
