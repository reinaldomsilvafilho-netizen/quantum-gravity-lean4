"""Camada 2, F-49 (cap. 5).

G1 gamma = 1 (Rem 3.2(c)), independent oracle: along the facet normal e1 the transform reduces to
   the 1D transform of g(y1) = int kappa(y1, y2) dy2 (kernel on Delta_2(alpha) in R^2, 3 parts),
   which jumps from 0 to g(0) > 0 at y1 = 0 and vanishes at y1 = alpha.  Hence
   |t| |K^(t e1)| -> g(0) exactly.  Mutation: |t|^{1.5}|K^| grows (gamma > 1 impossible).
   Also the integration-by-parts bound of the text, |K^(k)| <= (||kappa||_inf,bd * perimeter +
   ||d_j kappa||_L1)/|k_j|, is evaluated and must dominate |K^| for random k.
G2 Inversion (Prop 5.1) for m=2, n=1: h(x) = g_theta(P_theta x) for theta = span(x), and
   h^(k) = K^(-k) f^(k) by direct 2D quadrature.  Mutation: K^(+k) fails (kernel not symmetric).
G3 Mass conservation factor R(1_Omega) on Gamma: = 1 under the interface condition, < 1 without
   (1D toy with m=2 -> n=1 geometry).
"""
import math
import numpy as np
from scipy import integrate

FAIL = []


def check(name, ok, info=None):
    print(("PASS " if ok else "FAIL ") + name + ("" if info is None else "  | " + str(info)))
    if not ok:
        FAIL.append(name)


al = 1.0
lg = math.lgamma
kap_raw = lambda y1, y2: math.exp(lg(al + 1) - lg(y1 + 1) - lg(y2 + 1) - lg(al - y1 - y2 + 1))
Z = integrate.dblquad(lambda y2, y1: kap_raw(y1, y2), 0, al, 0, lambda y1: al - y1, epsabs=1e-13)[0]
kap = lambda y1, y2: kap_raw(y1, y2) / Z
g = lambda y1: integrate.quad(lambda y2: kap(y1, y2), 0, al - y1, epsabs=1e-14)[0]
g0 = g(0.0)
yy = np.linspace(0, al, 4001); gv = np.array([g(y) for y in yy])


def Khat_e1(t):
    re = integrate.quad(lambda y: g(y), 0, al, weight="cos", wvar=t, limit=400)[0]
    im = -integrate.quad(lambda y: g(y), 0, al, weight="sin", wvar=t, limit=400)[0]
    return complex(re, im)


rows = [(t, abs(t * Khat_e1(t)), abs(t) ** 1.5 * abs(Khat_e1(t))) for t in (25.0, 100.0, 400.0, 1600.0)]
print("   g(0) =", round(g0, 6), " |t K^(t e1)|:", [round(r[1], 6) for r in rows])
check("G1 |t| |K^(t e1)| -> g(0) (facet jump), so gamma <= 1 and the corrector's 1.84 at alpha=1 is g(0)", abs(rows[-1][1] - g0) < 2e-3 * g0 and abs(g0 - 1.84) < 0.01, g0)
check("G1-mut |t|^{1.5}|K^| grows", rows[-1][2] > 5 * rows[0][2])
# IBP bound of the text vs |K^| at random k
per = 2 * al + al * math.sqrt(2)
ys = [(a, b) for a in np.linspace(0, al, 201) for b in np.linspace(0, al, 201) if a + b <= al]
kinf_bd = max(kap(a, 0) for a in np.linspace(0, al, 201))
kinf_bd = max(kinf_bd, max(kap(0, b) for b in np.linspace(0, al, 201)), max(kap(a, al - a) for a in np.linspace(0, al, 201)))
h = 1e-5
dk1 = integrate.dblquad(lambda y2, y1: abs(kap(y1 + h, y2) - kap(y1 - h, y2)) / (2 * h), 0, al, 0, lambda y1: al - y1, epsabs=1e-8)[0]
dk2 = integrate.dblquad(lambda y2, y1: abs(kap(y1, y2 + h) - kap(y1, y2 - h)) / (2 * h), 0, al, 0, lambda y1: al - y1, epsabs=1e-8)[0]
rng = np.random.default_rng(5); ok = True; worst = 0
for _ in range(12):
    k = rng.normal(size=2) * rng.uniform(5, 200)
    re = integrate.dblquad(lambda y2, y1: kap(y1, y2) * math.cos(k[0] * y1 + k[1] * y2), 0, al, 0, lambda y1: al - y1, epsabs=1e-10)[0]
    im = integrate.dblquad(lambda y2, y1: kap(y1, y2) * math.sin(k[0] * y1 + k[1] * y2), 0, al, 0, lambda y1: al - y1, epsabs=1e-10)[0]
    j = int(np.argmax(np.abs(k)))
    B = (kinf_bd * per + (dk1, dk2)[j]) / abs(k[j])
    ok &= math.hypot(re, im) <= B
    worst = max(worst, math.hypot(re, im) / B)
check("G1 IBP bound (||kappa||_inf,bd * H^1(bd) + ||d_j kappa||_L1)/|k_j| dominates |K^(k)| (12 random k)", ok, "max ratio %.3f" % worst)

# G2 inversion identity and deconvolution
f = lambda x1, x2: math.exp(-((x1 - 0.4) ** 2 + (x2 + 0.3) ** 2) / 0.5)


def h(x):
    return integrate.dblquad(lambda y2, y1: kap(y1, y2) * f(x[0] + y1, x[1] + y2), 0, al, 0, lambda y1: al - y1, epsabs=1e-12)[0]


x = np.array([0.6, 1.2]); u = x / np.linalg.norm(x)
P = u[None, :]; Pp = P.T @ np.linalg.inv(P @ P.T)
gtheta = lambda z: integrate.dblquad(lambda y2, y1: kap(y1, y2) * f(Pp[0, 0] * z + y1, Pp[1, 0] * z + y2), 0, al, 0, lambda y1: al - y1, epsabs=1e-12)[0]
check("G2 h(x) = g_theta(P_theta x) for theta = span(x)", abs(h(x) - gtheta(float((P @ x)[0]))) < 1e-10)
# Fourier: h^(k) = K^(-k) f^(k), with F(k) = int e^{-ik.x}
k = np.array([1.3, -0.7])
fhat = math.pi * 0.5 * np.exp(-0.5 * (k @ k) / 4 * 1) * np.exp(-1j * (k @ np.array([0.4, -0.3])))  # Gaussian, variance param 0.5
fhat = (math.pi * 0.5) * np.exp(-(k @ k) * 0.5 / 4) * np.exp(-1j * (k @ np.array([0.4, -0.3])))


def Khat(kv):
    re = integrate.dblquad(lambda y2, y1: kap(y1, y2) * math.cos(kv[0] * y1 + kv[1] * y2), 0, al, 0, lambda y1: al - y1, epsabs=1e-12)[0]
    im = -integrate.dblquad(lambda y2, y1: kap(y1, y2) * math.sin(kv[0] * y1 + kv[1] * y2), 0, al, 0, lambda y1: al - y1, epsabs=1e-12)[0]
    return complex(re, im)


L = 6.0
hhat_re = integrate.dblquad(lambda b, a: h((a, b)) * math.cos(k[0] * a + k[1] * b), -L, L, -L, L, epsabs=1e-7)[0] if False else None
# h^ by the convolution theorem computed WITHOUT assuming it: h^(k) = int int kappa(y) f(x+y) e^{-ikx} dy dx
#   = int kappa(y) e^{+iky} dy * f^(k)  -> we verify numerically the kernel factor equals K^(-k)
fac = complex(integrate.dblquad(lambda y2, y1: kap(y1, y2) * math.cos(k[0] * y1 + k[1] * y2), 0, al, 0, lambda y1: al - y1)[0],
              integrate.dblquad(lambda y2, y1: kap(y1, y2) * math.sin(k[0] * y1 + k[1] * y2), 0, al, 0, lambda y1: al - y1)[0])
check("G2 kernel factor of h^ = K^(-k)", abs(fac - Khat(-k)) < 1e-10)
check("G2-mut K^(+k) differs (kernel not even)", abs(fac - Khat(k)) > 1e-2, abs(fac - Khat(k)))
# brute-force check of h^ at k on a grid (independent of the factorization)
xg, wg = np.polynomial.legendre.leggauss(40); tq = (xg + 1) / 2; wq = wg / 2
Y1, Y2, WQ = [], [], []
for ti, wi in zip(tq, wq):          # Duffy map of the triangle
    for sj, wj in zip(tq, wq):
        y1 = al * ti; y2 = (al - y1) * sj
        Y1.append(y1); Y2.append(y2); WQ.append(wi * wj * al * (al - y1) * kap(y1, y2))
Y1, Y2, WQ = map(np.array, (Y1, Y2, WQ))
n = 241; grid = np.linspace(-4, 5, n); dx = grid[1] - grid[0]
A, Bm = np.meshgrid(grid, grid, indexing="ij")
fv = lambda a, b: np.exp(-((a - 0.4) ** 2 + (b + 0.3) ** 2) / 0.5)
H = sum(w * fv(A + y1, Bm + y2) for y1, y2, w in zip(Y1, Y2, WQ))
check("G2 vectorized h agrees with adaptive h at x", abs(sum(w * fv(x[0] + a, x[1] + b) for a, b, w in zip(Y1, Y2, WQ)) - h(x)) < 1e-8)
hh = np.sum(H * np.exp(-1j * (k[0] * A + k[1] * Bm))) * dx * dx
check("G2 brute-force h^(k) = K^(-k) f^(k)", abs(hh - Khat(-k) * fhat) < 1e-4 * abs(fhat), (hh, Khat(-k) * fhat))

# G3 R(1_Omega) under / without the interface condition (m=2 -> n=1 geometry, Omega = disc radius 2)
inside = lambda p: p[0] ** 2 + p[1] ** 2 < 4.0
def R1(z):
    return integrate.dblquad(lambda y2, y1: kap(y1, y2) * (1.0 if inside((z + y1, y2)) else 0.0), 0, al, 0, lambda y1: al - y1, epsabs=1e-9)[0]
check("G3 R(1_Omega)=1 when z e1 + Delta_2(alpha) subset Omega (z=0.2)", abs(R1(0.2) - 1) < 1e-8)
check("G3-ctrl R(1_Omega)<1 near the boundary (z=1.5): interface condition is needed", R1(1.5) < 0.99, R1(1.5))
print("\nFAILURES:", FAIL if FAIL else "none")
