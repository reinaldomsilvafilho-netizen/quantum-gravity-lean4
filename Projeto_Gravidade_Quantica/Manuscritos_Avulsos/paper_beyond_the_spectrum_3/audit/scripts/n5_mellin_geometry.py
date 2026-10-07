"""OBL-017/018: Z_A(s) = int (Phi)^s dmu_alpha on Delta_2 (Beta(a,b) law), Phi(u) = 1 + u.
 oracle 1: mpmath tanh-sinh quadrature; oracle 2: closed form 2F1(-s, a; a+b; -1).
 Evaluate at the claimed poles s = -a-k, -b-k and at s +- 1e-8: finite and continuous => no pole.
 Negative control: B(s+a, b) DOES have a pole at s = -a; the same detector must flag it.
OBL-006 step: S^1 with strata {2 points} u {2 open arcs}, constant sheaf.
OBL-020: ellipse a=2,b=1: reach by brute force (distance to medial axis) vs eps0/M; d_sep finite (=2b).
OBL-021: tube volume of the ellipse (d=2: Vol = 2 r Perimeter) by Monte Carlo; sphere S^3 exact.
OBL-019: 2 log 3 / log 5."""
import numpy as np, sys, mpmath as mp
rng = np.random.default_rng(99)
fails = 0
mp.mp.dps = 30
a, b = mp.mpf('0.5'), mp.mpf('1.5')
dens = lambda u: u ** (a - 1) * (1 - u) ** (b - 1) / mp.beta(a, b)


def Zq(s):
    return mp.quad(lambda u: (1 + u) ** s * dens(u), [0, 1])


def Zc(s):
    return mp.hyp2f1(-s, a, a + b, -1)


def detect_pole(F, s0):
    # pole of order>=1: |F(s0+e)| grows ~10x when e shrinks 10x; analytic: ratio ~1
    e = mp.mpf('1e-6')
    r1 = abs(F(s0 + e / 10)) / abs(F(s0 + e))
    r2 = abs(F(s0 - e / 10)) / abs(F(s0 - e))
    return r1 > 5 and r2 > 5


for s0 in [-a, -a - 1, -a - 2, -b, -b - 1, mp.mpf(-7.3)]:
    q, c = Zq(s0), Zc(s0)
    pole = detect_pole(Zc, s0)
    print('s=%6s  quad=%s  2F1=%s  pole detected: %s' % (mp.nstr(s0, 4), mp.nstr(q, 12), mp.nstr(c, 12), pole))
    fails += abs(q - c) > mp.mpf('1e-15') or pole
negpole = detect_pole(lambda s: mp.beta(s + a, b), -a)
print('NEG CONTROL: B(s+a,b) pole at s=-a detected:', negpole)
fails += not negpole
# OBL-006 step
chi_S1, chi_arcs, chic_arcs, chi_pts = 0, 2, -2, 2
print('OBL-006: chi(S^1)=%d ; paper RHS sum m_r chi(Sigma_r) = 1*chi(arcs)+0*chi(pts) = %d ; correct sum chi_c*stalk = %d' % (chi_S1, chi_arcs, chic_arcs + chi_pts))
fails += (chi_arcs == chi_S1) or (chic_arcs + chi_pts != chi_S1)
# OBL-020 ellipse x^2/(2 A^2) + y^2/(2 B^2) = 1/2
A, B = 2.0, 1.0
th = np.linspace(0, 2 * np.pi, 200001)[:-1]
P = np.c_[A * np.cos(th), B * np.sin(th)]
c = (A ** 2 - B ** 2) / A
med = np.linspace(-c, c, 2001)
reach = min(np.min(np.hypot(P[:, 0] - m, P[:, 1])) for m in med)
grad = np.hypot(P[:, 0] / A ** 2, P[:, 1] / B ** 2)
eps0, M = grad.min(), 1 / B ** 2
nu = np.c_[P[:, 0] / A ** 2, P[:, 1] / B ** 2] / grad[:, None]
# antipodal pairs x, -x have nu(-x) = -nu(x):
dsep_antipodal = np.min(2 * np.hypot(P[:, 0], P[:, 1]))
print('OBL-020 ellipse: brute-force reach = %.6f, eps0/M = %.6f, b^2/a = %.6f, d_sep <= %.4f (finite; paper: infinity for convex)' % (reach, eps0 / M, B ** 2 / A, dsep_antipodal))
fails += abs(reach - B ** 2 / A) > 1e-4 or reach < min(eps0 / M, dsep_antipodal / 2) - 1e-6
fails += not np.isfinite(dsep_antipodal)
fails += reach >= 2 * eps0 / M  # negative control: doubled bound must fail
# OBL-021 ellipse tube by Monte Carlo, r = 0.3 < reach 0.5
r = 0.3
per = float(mp.quad(lambda t: mp.sqrt((A * mp.sin(t)) ** 2 + (B * mp.cos(t)) ** 2), [0, 2 * mp.pi]))
Nmc = 2000000
Q = rng.uniform([-A - r, -B - r], [A + r, B + r], size=(Nmc, 2))
# distance to ellipse via dense sampling (KD tree)
from scipy.spatial import cKDTree
tree = cKDTree(P[::2])
dist, _ = tree.query(Q)
box = (2 * (A + r)) * (2 * (B + r))
vol = box * np.mean(dist < r)
se = box * np.sqrt(np.mean(dist < r) * (1 - np.mean(dist < r)) / Nmc)
print('OBL-021 ellipse tube r=0.3: MC = %.5f +- %.5f ; formula 2 r Per = %.5f ; mutated (r Per) = %.5f' % (vol, se, 2 * r * per, r * per))
fails += abs(vol - 2 * r * per) > 5 * se + 2e-3
fails += abs(vol - r * per) < 5 * se
R, rr = 1.3, 0.4
exact = np.pi ** 2 / 2 * ((R + rr) ** 4 - (R - rr) ** 4)
formula = 2 * rr * 2 * np.pi ** 2 * R ** 3 + 2 * rr ** 3 / 3 * (3 / R ** 2) * 2 * np.pi ** 2 * R ** 3
print('OBL-021 S^3 in R^4: exact %.10f formula %.10f' % (exact, formula))
fails += abs(exact - formula) > 1e-10
ds = 2 * np.log(3) / np.log(5)
print('OBL-019: 2 ln3/ln5 = %.6f' % ds)
fails += abs(ds - 1.3652) > 5e-5
print('failures:', int(fails))
sys.exit(int(fails))
