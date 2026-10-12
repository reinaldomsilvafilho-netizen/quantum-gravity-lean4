"""L1 blind check A4 (ch. 5, Proposition [Inversion], hypothesis  hat K_alpha(k) != 0 for all k).

Kernel (ch. 5, Def. radon_beta, m = 2): K(y) = c / (Gamma(y1+1) Gamma(y2+1) Gamma(alpha-y1-y2+1))
on the triangle Delta_2(alpha) = {y >= 0, y1 + y2 <= alpha}, normalised to mass 1.

1) Direction k = t (1,-1): by the y1 <-> y2 symmetry hat K(t(1,-1)) is REAL, so a sign
   change is a certified zero.  Root refined by brentq, then the value is re-evaluated by an
   independent oracle (scipy dblquad, adaptive) at the root.
2) Topological detector on a 2-D grid: winding number of hat K around each cell.
   Negative control: the same detector on the Gaussian transform exp(-|k|^2/2) (no zeros)
   must report 0 zeros; positive control: the unit-square indicator (zeros at k1 = 2 pi j).
3) m = 3 along k = t(1,-1,0) (real by symmetry), Gauss quadrature on the tetrahedron.
"""
import numpy as np
from scipy.special import gammaln, roots_legendre
from scipy.optimize import brentq
from scipy.integrate import dblquad

NQ = 140
xg, wg = roots_legendre(NQ)
xg = 0.5 * (xg + 1); wg = 0.5 * wg


def tri_nodes(alpha):
    # Duffy map: y1 = alpha*u, y2 = alpha*(1-u)*v, Jacobian alpha^2 (1-u)
    U, Vv = np.meshgrid(xg, xg, indexing="ij")
    W = np.outer(wg, wg) * alpha**2 * (1 - U)
    y1 = alpha * U; y2 = alpha * (1 - U) * Vv
    dens = np.exp(-(gammaln(y1 + 1) + gammaln(y2 + 1) + gammaln(alpha - y1 - y2 + 1)))
    W = W * dens
    W /= W.sum()
    return y1.ravel(), y2.ravel(), W.ravel()


def Khat(k1, k2, nodes):
    y1, y2, W = nodes
    return np.sum(W * np.exp(-1j * (k1 * y1 + k2 * y2)))


def count_zeros(F, kmax, N):
    ks = np.linspace(-kmax, kmax, N)
    G = np.array([[F(a, b) for b in ks] for a in ks])
    ph = np.angle(G)
    d = lambda a, b: (b - a + np.pi) % (2 * np.pi) - np.pi
    w = (d(ph[:-1, :-1], ph[1:, :-1]) + d(ph[1:, :-1], ph[1:, 1:]) + d(ph[1:, 1:], ph[:-1, 1:]) + d(ph[:-1, 1:], ph[:-1, :-1]))
    wn = np.rint(w / (2 * np.pi)).astype(int)
    idx = np.argwhere(wn != 0)
    return int(np.abs(wn).sum()), [(ks[i], ks[j], wn[i, j]) for i, j in idx[:6]]


for alpha in (0.5, 1.0, 2.0):
    nodes = tri_nodes(alpha)
    f = lambda t: Khat(t, -t, nodes).real
    im_max = max(abs(Khat(t, -t, nodes).imag) for t in np.linspace(0, 40, 50))
    ts = np.linspace(0.01, 40, 4000)
    vals = np.array([f(t) for t in ts])
    sc = np.where(np.sign(vals[:-1]) != np.sign(vals[1:]))[0]
    print(f"alpha={alpha}: Im hatK on k=t(1,-1) max {im_max:.1e}; sign changes for t in (0,40]: {len(sc)}")
    if len(sc):
        t0 = brentq(f, ts[sc[0]], ts[sc[0] + 1], xtol=1e-13)
        # independent oracle at the root: adaptive dblquad on the raw (unnormalised) kernel
        dens = lambda y2, y1: np.exp(-(gammaln(y1 + 1) + gammaln(y2 + 1) + gammaln(alpha - y1 - y2 + 1)))
        Z = dblquad(dens, 0, alpha, 0, lambda y1: alpha - y1, epsabs=1e-13)[0]
        re = dblquad(lambda y2, y1: dens(y2, y1) * np.cos(t0 * (y1 - y2)), 0, alpha, 0, lambda y1: alpha - y1, epsabs=1e-13)[0] / Z
        im = dblquad(lambda y2, y1: dens(y2, y1) * np.sin(t0 * (y1 - y2)), 0, alpha, 0, lambda y1: alpha - y1, epsabs=1e-13)[0] / Z
        print(f"   first zero t0={t0:.10f}, k0=({t0:.6f},{-t0:.6f}); oracle dblquad hatK(k0) = {re:.2e} + {im:.2e} i")
        assert abs(re) < 1e-9 and abs(im) < 1e-9
    if alpha == 1.0:
        nz, ex = count_zeros(lambda a, b: Khat(a, b, nodes), 30, 241)
        print(f"   winding detector on [-30,30]^2: {nz} zeros (|winding| sum); examples {[(round(a,2),round(b,2),w) for a,b,w in ex]}")

# controls for the detector (same magnitude scale ~ 1/|k| as hat K, oscillating phase)
ctrl_free = lambda a, b: np.exp(-1j * (0.4 * a + 0.3 * b)) / np.sqrt(1 + a * a + b * b)
ctrl_one = lambda a, b: ((a - 3.1) - 1j * (b - 5.2)) * np.exp(-1j * (0.4 * a + 0.3 * b)) / (1 + a * a + b * b)
nzg, _ = count_zeros(ctrl_free, 30, 241)
nz1, ex1 = count_zeros(ctrl_one, 30, 241)
print(f"negative control (zero-free, |F|~1/|k|): detector finds {nzg}")
print(f"positive control (one zero at (3.1,5.2)): detector finds {nz1} at {[(round(a,2),round(b,2)) for a,b,_ in ex1]}")
assert nzg == 0 and nz1 == 1

# The winding detector flags cells near k = t(1,-1), t(2,1), t(1,2) (the S3-symmetric lines) where
# |hat K| has deep minima; the phase turns too fast for the grid there.  Decide by local minimisation
# of |hat K|^2, and cross-check the minimum value with the independent dblquad oracle.
from scipy.optimize import minimize
alpha = 1.0
nodes = tri_nodes(alpha)
dens = lambda y2, y1: np.exp(-(gammaln(y1 + 1) + gammaln(y2 + 1) + gammaln(alpha - y1 - y2 + 1)))
Zn = dblquad(dens, 0, alpha, 0, lambda y1: alpha - y1, epsabs=1e-14)[0]
G = lambda q: abs(Khat(q[0], q[1], nodes)) ** 2
for p in [(6.5, -6.5), (12.69, -12.69), (-25.43, -18.84), (-25.37, -12.69), (12.0, -13.4)]:
    r = minimize(G, p, method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-34, "maxiter": 3000})
    q = r.x
    re = dblquad(lambda y2, y1: dens(y2, y1) * np.cos(q[0] * y1 + q[1] * y2), 0, alpha, 0, lambda y1: alpha - y1, epsabs=1e-14)[0] / Zn
    im = -dblquad(lambda y2, y1: dens(y2, y1) * np.sin(q[0] * y1 + q[1] * y2), 0, alpha, 0, lambda y1: alpha - y1, epsabs=1e-14)[0] / Zn
    print(f"   local min of |hatK| near {p}: k*=({q[0]:.6f},{q[1]:.6f}), |hatK|={np.sqrt(r.fun):.3e}; oracle |hatK(k*)|={np.hypot(re, im):.3e}")
    assert np.sqrt(r.fun) > 1e-6 and abs(np.hypot(re, im) - np.sqrt(r.fun)) < 1e-9

# minima of R(t) = hat K(t(1,-1)) (real) on (0,60]: positive, decaying like t^-4
x, w = roots_legendre(NQ); x = 0.5 * (x + 1); w = 0.5 * w
def R_line(alpha, ts, uniform=False):
    Uu, Vv = np.meshgrid(x, x, indexing="ij"); Wt = np.outer(w, w) * (1 - Uu)
    a1 = alpha * Uu; a2 = alpha * (1 - Uu) * Vv
    if not uniform:
        Wt = Wt * np.exp(-(gammaln(a1 + 1) + gammaln(a2 + 1) + gammaln(alpha - a1 - a2 + 1)))
    Wt = (Wt / Wt.sum()).ravel(); Dd = (a1 - a2).ravel()
    return np.concatenate([np.cos(np.outer(c, Dd)) @ Wt for c in np.array_split(ts, max(1, len(ts) // 500))])
ts = np.linspace(0.01, 60, 60000)
for alpha in (0.5, 1.0, 2.0):
    v = R_line(alpha, ts)
    loc = [k for k in range(1, len(v) - 1) if v[k] < v[k - 1] and v[k] < v[k + 1]]
    print(f"alpha={alpha}: R(t) sign changes on (0,60]: {np.sum(np.sign(v[:-1]) != np.sign(v[1:]))}; min R = {v.min():.3e}; "
          f"first minima {[(round(ts[k],3), float('%.2e' % v[k])) for k in loc[:4]]}")
    assert v.min() > 0
# NEGATIVE CONTROL: uniform density on the same triangle (kappa = const): R(t) = sinc^2-type, true
# double zeros at t = 2 pi j, so the same pipeline must report min |R| at round-off level.
vu = R_line(1.0, ts, uniform=True)
k = np.argmin(np.abs(vu - 0) + (np.abs(ts - 4 * np.pi) > 0.05) * 1.0)
print(f"control (uniform triangle): R(4 pi) = {R_line(1.0, np.array([4*np.pi]), uniform=True)[0]:.2e} (exact 0); grid min near 4pi {vu[k]:.2e}")
assert abs(R_line(1.0, np.array([4 * np.pi]), uniform=True)[0]) < 1e-12

# 1-D analogue (two-part Beta kernel on [0, alpha], the chapter-3 kernel): zeros exist
from scipy.integrate import quad
a1d = 1.0
d1 = lambda y: np.exp(-(gammaln(y + 1) + gammaln(a1d - y + 1)))
Z1 = quad(d1, 0, a1d)[0]
R1 = lambda t: quad(lambda y: d1(y) * np.cos(t * (y - a1d / 2)), 0, a1d, limit=200)[0] / Z1
t1 = brentq(R1, 6.0, 7.5)
print(f"1-D two-part kernel, alpha=1: e^(i t/2) hatK(t) is real and vanishes at t0={t1:.8f} (sign change certified by brentq)")

# m = 3, k = t(1,-1,0)
x3, w3 = roots_legendre(40); x3 = 0.5 * (x3 + 1); w3 = 0.5 * w3
alpha = 1.0
U, V, Wq = np.meshgrid(x3, x3, x3, indexing="ij")
y1 = alpha * U; y2 = alpha * (1 - U) * V; y3 = alpha * (1 - U) * (1 - V) * Wq
J = alpha**3 * (1 - U) ** 2 * (1 - V)
wt = np.einsum("i,j,k->ijk", w3, w3, w3) * J * np.exp(-(gammaln(y1 + 1) + gammaln(y2 + 1) + gammaln(y3 + 1) + gammaln(alpha - y1 - y2 - y3 + 1)))
wt /= wt.sum()
f3 = lambda t: np.sum(wt * np.cos(t * (y1 - y2)))
ts = np.linspace(0.01, 40, 2000)
v3 = np.array([f3(t) for t in ts])
sc3 = np.where(np.sign(v3[:-1]) != np.sign(v3[1:]))[0]
print(f"m=3, alpha=1, k=t(1,-1,0): sign changes in (0,40]: {len(sc3)}" + (f"; first zero t0={brentq(f3, ts[sc3[0]], ts[sc3[0]+1]):.6f}" if len(sc3) else ""))
