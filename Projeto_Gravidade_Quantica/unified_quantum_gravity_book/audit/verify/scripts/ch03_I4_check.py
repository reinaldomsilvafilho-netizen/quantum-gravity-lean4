"""Independent check of I_4(x) (Table 1, m=4) with Duffy-mapped Gauss-Legendre
product rules at two orders (convergence = oracle), plus I_3 as control."""
import numpy as np
from scipy.special import gammaln

def integrand(x, ys):
    last = x - ys.sum(axis=0)
    return np.exp(gammaln(x + 1) - gammaln(ys + 1).sum(axis=0) - gammaln(last + 1))

def I_simplex(x, d, n):
    g, w = np.polynomial.legendre.leggauss(n)
    u = (g + 1) / 2; w = w / 2
    grids = np.meshgrid(*([u] * d), indexing="ij")
    W = np.ones_like(grids[0])
    for wi in np.meshgrid(*([w] * d), indexing="ij"):
        W = W * wi
    # Duffy / stick-breaking: y1 = x u1, y2 = (x-y1) u2, ...
    rem = np.full_like(grids[0], float(x)); ys = []; jac = np.ones_like(grids[0])
    for gi in grids:
        yi = rem * gi; jac = jac * rem; ys.append(yi); rem = rem - yi
    ys = np.array(ys)
    return (W * jac * integrand(x, ys)).sum()

for x in [1, 2, 5, 10]:
    print("x=%g  I3(n=60)=%.6f I3(n=120)=%.6f  I4(n=60)=%.6f I4(n=100)=%.6f" % (
        x, I_simplex(x, 2, 60), I_simplex(x, 2, 120), I_simplex(x, 3, 60), I_simplex(x, 3, 100)))
print("table I4: 0.2270, 3.3633, 662.1933, 968904.8")
