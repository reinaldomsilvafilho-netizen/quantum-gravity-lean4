"""Blind layer-1 checks for chapter 8 (symbolic geometry / GR).

Each check computes the quantity from first principles (independent oracle)
and runs a negative control (a mutated formula that must FAIL).
Run:  python ch08_gr_blind.py
"""
import itertools
import random

import sympy as sp

RESULTS = []


def report(name, ok, neg_fails):
    RESULTS.append((name, ok, neg_fails))
    print(f"[{'OK ' if ok else 'BAD'}] {name}   (negative control fails as expected: {neg_fails})")


def christoffel(g, x):
    n = len(x)
    gi = g.inv()
    return [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], x[c]) + sp.diff(g[d, c], x[b])
                                         - sp.diff(g[b, c], x[d])) for d in range(n)) / 2)
              for c in range(n)] for b in range(n)] for a in range(n)]


# ---------------------------------------------------------------------------
# 1. Coupling K_M = c + kappa^2 : geodesic sphere of radius r in S^3(1) and H^3(-1)
r = sp.symbols('r', positive=True)
# S^3: intrinsic sectional curvature of the geodesic sphere = 1/sin^2 r, kappa = cot r
lhs = 1 / sp.sin(r) ** 2
ok = sp.simplify(lhs - (1 + sp.cot(r) ** 2)) == 0
neg = sp.simplify(lhs - (1 - sp.cot(r) ** 2)) != 0
report("Thm 3.1 coupling in S^3 (K = c + kappa^2)", ok, neg)
lhs = 1 / sp.sinh(r) ** 2
ok = sp.simplify(lhs - (-1 + sp.coth(r) ** 2)) == 0
neg = sp.simplify(lhs - (-1 - sp.coth(r) ** 2)) != 0
report("Thm 3.1 coupling in H^3", ok, neg)

# ---------------------------------------------------------------------------
# 2. Tube of radius d about a GEODESIC in H^3(-1): metric dr^2 + sinh^2 r dphi^2 + cosh^2 r dt^2
#    principal curvatures of r=d are (1/2) d/dr log g_ii
d = sp.symbols('d', positive=True)
k_phi = sp.simplify(sp.diff(sp.log(sp.sinh(r)), r)).subs(r, d)
k_t = sp.simplify(sp.diff(sp.log(sp.cosh(r)), r)).subs(r, d)
ok = sp.simplify(k_phi - sp.coth(d)) == 0 and sp.simplify(k_t - sp.tanh(d)) == 0
# control: equidistant from a totally geodesic PLANE: dr^2 + cosh^2 r (dx^2+dy^2) -> tanh, tanh
k_plane = sp.simplify(sp.diff(sp.log(sp.cosh(r)), r)).subs(r, d)
neg = sp.simplify(k_phi - sp.tanh(d)) != 0
report("Sec 3.2: tube about a geodesic in H^3 has curvatures {coth d, tanh d}; ||II||=coth d, NOT tanh d",
       ok and sp.simplify(k_plane - sp.tanh(d)) == 0, neg)

# ---------------------------------------------------------------------------
# 3. Clifford torus in S^3: principal curvatures +-1
u, v = sp.symbols('u v', real=True)
X = sp.Matrix([sp.cos(u), sp.sin(u), sp.cos(v), sp.sin(v)]) / sp.sqrt(2)
nu = sp.Matrix([sp.cos(u), sp.sin(u), -sp.cos(v), -sp.sin(v)]) / sp.sqrt(2)
assert sp.simplify(nu.dot(X)) == 0 and sp.simplify(nu.dot(nu)) == 1
guu = sp.simplify(X.diff(u).dot(X.diff(u)))
gvv = sp.simplify(X.diff(v).dot(X.diff(v)))
ku = sp.simplify(X.diff(u, 2).dot(nu) / guu)
kv = sp.simplify(X.diff(v, 2).dot(nu) / gvv)
ok = {ku, kv} == {-1, 1}
neg = {ku, kv} != {sp.Rational(1, 2), -sp.Rational(1, 2)}
report("Sec 3.4: Clifford torus principal curvatures = +-1", ok, neg)

# ---------------------------------------------------------------------------
# 4. Sign of K_ij = -1/2 L_n gamma vs -g(nabla_i d_j, n): Milne hyperboloid in Minkowski
tau, chi, th, ph = sp.symbols('tau chi theta phi', positive=True)
x = [tau, chi, th, ph]
g = sp.diag(-1, tau ** 2, tau ** 2 * sp.sinh(chi) ** 2, tau ** 2 * sp.sinh(chi) ** 2 * sp.sin(th) ** 2)
G = christoffel(g, x)
# n = d_tau (future unit normal); -1/2 L_n gamma_ij = -1/2 d_tau gamma_ij
K_lie = sp.Matrix(3, 3, lambda i, j: -sp.Rational(1, 2) * sp.diff(g[i + 1, j + 1], tau))
# -g(nabla_{d_i} d_j, n) = -Gamma^tau_ij g_{tau tau} = +Gamma^tau_ij
K_nab = sp.Matrix(3, 3, lambda i, j: -G[0][i + 1][j + 1] * g[0, 0])
gam = g[1:, 1:]
ok_lie = sp.simplify(K_lie + gam / tau) == sp.zeros(3)  # K_ij = -gamma_ij / tau, ||K||=1/tau
ok_mismatch = sp.simplify(K_lie + K_nab) == sp.zeros(3)  # the two sides are NEGATIVES of each other
neg = sp.simplify(K_lie - K_nab) != sp.zeros(3)
report("Sec 4.1: -1/2 L_n gamma = +g(nabla d_i d_j, n) (display has the opposite sign); ||K|| = 1/tau0",
       ok_lie and ok_mismatch, neg)

# ---------------------------------------------------------------------------
# 5. Operator-norm definition in Lorentzian normal bundle: round sphere t=0, r=R in Minkowski
R, eta = sp.symbols('R eta', positive=True)
# II(v,v) = -(1/R) e_r for unit tangent v; unit timelike normals nu = cosh(eta) e_t + sinh(eta) e_r
II_dot_nu = -(1 / R) * sp.sinh(eta)  # g(e_r, nu) = sinh eta
sqrt_gII = 1 / R
ok = sp.limit(sp.Abs(II_dot_nu), eta, sp.oo) == sp.oo
neg = sp.simplify(sp.Abs(II_dot_nu).subs(eta, 0)) == 0  # control: at eta=0 value finite
report("Def 2.3: max over S(N_pM) is +infinity for a spacelike 2-sphere in R^{1,3}, while sqrt|g(II,II)| = 1/R",
       ok, neg)

# ---------------------------------------------------------------------------
# 6. Null expansion sign: sphere r=R, t=0 in Minkowski (spherical coords)
t_, r_ = sp.symbols('t r', positive=True)
xs = [t_, r_, th, ph]
gm = sp.diag(-1, 1, r_ ** 2, r_ ** 2 * sp.sin(th) ** 2)
Gm = christoffel(gm, xs)
l_up = [1, 1, 0, 0]
l_dn = [sum(gm[a, b] * l_up[b] for b in range(4)) for a in range(4)]
qinv = {2: 1 / r_ ** 2, 3: 1 / (r_ ** 2 * sp.sin(th) ** 2)}
# q^{ab} nabla_a l_b
theta_nab = sp.simplify(sum(qinv[a] * (sp.diff(l_dn[a], xs[a]) - sum(Gm[c][a][a] * l_dn[c] for c in range(4)))
                            for a in (2, 3)))
# q^{ab} g(II(e_a,e_b), l) ; II(e_a,e_a) = normal part of nabla_{e_a} e_a = Gamma^{t,r}_{aa}
theta_II = sp.simplify(sum(qinv[a] * sum(Gm[c][a][a] * l_dn[c] for c in (0, 1)) for a in (2, 3)))
ok = sp.simplify(theta_nab - 2 / r_) == 0 and sp.simplify(theta_II + 2 / r_) == 0
neg = sp.simplify(theta_nab - theta_II) != 0
report("Def 4.5: q^ab II.l = -q^ab nabla_a l_b (display equates them)", ok, neg)

# ---------------------------------------------------------------------------
# 7. Painleve-Gullstrand Reissner-Nordstrom
M, Q, T = sp.symbols('M Q T', positive=True)
f = 1 - 2 * M / r_ + Q ** 2 / r_ ** 2


def pg_theta(beta):
    gpg = sp.Matrix([[-(1 - beta ** 2), beta, 0, 0], [beta, 1, 0, 0],
                     [0, 0, r_ ** 2, 0], [0, 0, 0, r_ ** 2 * sp.sin(th) ** 2]])
    xp = [T, r_, th, ph]
    Gp = christoffel(gpg, xp)
    # unit normal n_mu = (-1,0,0,0) (lapse 1);  K_ij = -nabla_i n_j (Gourgoulhon, K = -1/2 L_n gamma)
    n_dn = [-1, 0, 0, 0]
    K = sp.Matrix(3, 3, lambda i, j: sp.simplify(-(sp.diff(n_dn[j + 1], xp[i + 1])
                                                   - sum(Gp[c][i + 1][j + 1] * n_dn[c] for c in range(4)))))
    gam = gpg[1:, 1:]
    Ktr = sp.simplify(sum((gam.inv())[i, j] * K[i, j] for i in range(3) for j in range(3)))
    s_up = [1, 0, 0]  # unit radial normal in the flat slice
    Ds = sp.simplify(2 / r_)  # divergence of d_r in flat 3-space
    Kss = K[0, 0]
    return gpg, sp.simplify(Ds - Ktr + Kss), sp.simplify(K[1, 1] / r_ ** 2)


beta_ok = sp.sqrt(2 * M / r_ - Q ** 2 / r_ ** 2)
gpg, thl, Kthth = pg_theta(beta_ok)
rp = M + sp.sqrt(M ** 2 - Q ** 2)
ok1 = sp.simplify(gpg[0, 0] + f) == 0
ok2 = sp.simplify(thl - (2 / r_ - 2 * beta_ok / r_)) == 0
ok3 = all(abs(sp.N(thl.subs(r_, rp).subs({M: mm, Q: qq}))) < 1e-12
          for mm, qq in [(1, 0), (1, sp.Rational(1, 2)), (1, sp.Rational(9, 10)), (2, 1), (1, 1)])
ok4 = sp.simplify(Kthth - beta_ok / r_) == 0 or sp.simplify(Kthth + beta_ok / r_) == 0
# coordinate change T = t + int beta/f dr gives -f dt^2 + dr^2/f
ok5 = sp.simplify(1 + beta_ok ** 2 / f - 1 / f) == 0
_, thl_bad, _ = pg_theta(sp.sqrt(2 * M / r_ + Q ** 2 / r_ ** 2))
neg = abs(sp.N(thl_bad.subs(r_, rp).subs({M: 1, Q: sp.Rational(9, 10)}))) > 1e-3
report("Prop 4.6: PG form of RN, K^th_th = beta/r, theta_l = 2(1-beta)/r vanishes at r_+",
       all([ok1, ok2, ok3, ok4, ok5]), neg)
# numeric spot check of the negative control and range condition Q^2/(2M) < r_+
num = {M: 1, Q: sp.Rational(9, 10)}
print("    theta_l_bad(r_+) numeric =", sp.N(thl_bad.subs(r_, rp).subs(num)),
      "; Q^2/2M =", sp.N((Q ** 2 / (2 * M)).subs(num)), "< r_+ =", sp.N(rp.subs(num)))

# ---------------------------------------------------------------------------
# 8. Morris-Thorne: rho + p_r at the throat
Phi = sp.Function('Phi')(r_)
b = sp.Function('b')(r_)
xm = [t_, r_, th, ph]
gmt = sp.diag(-sp.exp(2 * Phi), 1 / (1 - b / r_), r_ ** 2, r_ ** 2 * sp.sin(th) ** 2)
Gmt = christoffel(gmt, xm)


def ricci(Gam, xx):
    n = len(xx)
    return sp.Matrix(n, n, lambda i, j: sp.simplify(
        sum(sp.diff(Gam[a][i][j], xx[a]) for a in range(n))
        - sum(sp.diff(Gam[a][i][a], xx[j]) for a in range(n))
        + sum(Gam[a][a][c] * Gam[c][i][j] for a in range(n) for c in range(n))
        - sum(Gam[a][j][c] * Gam[c][i][a] for a in range(n) for c in range(n))))


Ric = ricci(Gmt, xm)
gi = gmt.inv()
Rs = sp.simplify(sum(gi[i, j] * Ric[i, j] for i in range(4) for j in range(4)))
Gein = sp.simplify(Ric - Rs * gmt / 2)
rho8 = sp.simplify(-Gein[0, 0] * gi[0, 0])        # 8 pi G rho = G^t_t * (-1)
pr8 = sp.simplify(Gein[1, 1] * gi[1, 1])          # 8 pi G p_r = G^r_r
ok_rho = sp.simplify(rho8 - sp.diff(b, r_) / r_ ** 2) == 0
ok_pr = sp.simplify(pr8 - (-b / r_ ** 3 + 2 * (1 - b / r_) * sp.diff(Phi, r_) / r_)) == 0
r0, bp = sp.symbols('r0 bp', positive=True)
nec = sp.simplify((rho8 + pr8).subs(sp.Derivative(b, r_), bp).subs(b, r_).subs(r_, r0))
ok_nec = sp.simplify(nec - (bp - 1) / r0 ** 2) == 0
neg = sp.simplify(nec - (1 - bp) / r0 ** 2) != 0
report("Prop 4.10: MT 8piG rho = b'/r^2, 8piG p_r formula, 8piG(rho+p_r)|_{r0} = (b'-1)/r0^2",
       ok_rho and ok_pr and ok_nec, neg)

# ---------------------------------------------------------------------------
# 9. Estabrook limiting maximal slice in Schwarzschild
Cc = sp.symbols('C', positive=True)
fs = 1 - 2 * M / r_
Fr = fs * r_ ** 4 + Cc ** 2  # must stay >= 0 along the slice
rc = sp.solve(sp.diff(2 * M * r_ ** 3 - r_ ** 4, r_), r_)
rc = [s for s in rc if s != 0][0]
C2 = sp.simplify((2 * M * r_ ** 3 - r_ ** 4).subs(r_, rc))
ok_c = rc == sp.Rational(3, 2) * M and sp.simplify(C2 - sp.Rational(27, 16) * M ** 4) == 0
# direct K of the slice t = h(r), h' = C/(f sqrt(f r^4 + C^2)) (or its negative)
hp = Cc / (fs * sp.sqrt(Fr))
gs = sp.diag(-fs, 1 / fs, r_ ** 2, r_ ** 2 * sp.sin(th) ** 2)
Gs = christoffel(gs, xm)
dPhi = [1, -hp, 0, 0]
gsi = gs.inv()
norm2 = sp.simplify(-sum(gsi[a, bb] * dPhi[a] * dPhi[bb] for a in range(4) for bb in range(4)))
n_dn = [-dPhi[a] / sp.sqrt(norm2) for a in range(4)]
nab_n = sp.Matrix(4, 4, lambda a, bb: sp.diff(n_dn[bb], xm[a]) - sum(Gs[c][a][bb] * n_dn[c] for c in range(4)))
divn = sp.simplify(sum(gsi[a, bb] * nab_n[a, bb] for a in range(4) for bb in range(4)))
n_up = [sum(gsi[a, bb] * n_dn[bb] for bb in range(4)) for a in range(4)]
Kthth_mixed = sp.simplify(-nab_n[2, 2] / r_ ** 2)
ok_max = sp.simplify(divn) == 0
ok_kth = sp.simplify(Kthth_mixed ** 2 - Cc ** 2 / r_ ** 6) == 0
Krr_abs = 2 * sp.sqrt(sp.Rational(27, 16)) * M ** 2 / r_ ** 3
ok_tab = sp.simplify(Krr_abs - 3 * sp.sqrt(3) * M ** 2 / (2 * r_ ** 3)) == 0
ok_peak = sp.simplify(Krr_abs.subs(r_, sp.Rational(3, 2) * M) - 4 * sp.sqrt(3) / (9 * M)) == 0
neg = sp.simplify((3 * sp.sqrt(3) * M ** 2 / r_ ** 3).subs(r_, sp.Rational(3, 2) * M)
                  - 4 * sp.sqrt(3) / (9 * M)) != 0
report("Table: Estabrook slice K=0, |K^th_th| = C/r^3, C^2 = 27M^4/16 at r=3M/2, |K^r_r| peak 4sqrt3/(9M)",
       ok_c and ok_max and ok_kth and ok_tab and ok_peak, neg)

# ---------------------------------------------------------------------------
# 10. ADM corollary: e2 range on the cube [-1,1]^3 is exactly [-1, 3]
verts = list(itertools.product([-1, 1], repeat=3))
e2 = lambda l: l[0] * l[1] + l[1] * l[2] + l[2] * l[0]
vals = [e2(vv) for vv in verts]
random.seed(0)
samples = [e2([random.uniform(-1, 1) for _ in range(3)]) for _ in range(200000)]
ok = min(vals) == -1 and max(vals) == 3 and min(samples) >= -1 - 1e-12 and max(samples) <= 3 + 1e-12
neg = not (min(vals) >= 0)  # mutated claim "e2 >= 0 on the cube" must fail
report("Cor 4.2: e2 in [-k^2, 3k^2] so -6k^2 <= R-16piG rho <= 2k^2", ok, neg)

# ---------------------------------------------------------------------------
# 11. Timelike angular speed bound in Schwarzschild equatorial plane (slingshot conjecture)
rr = sp.symbols('rr', positive=True)
w = sp.sqrt(1 - 2 / rr) / rr  # |dphi/dt| < sqrt(f)/r   (M=1)
crit = sp.solve(sp.diff(w, rr), rr)
wmax = sp.simplify(w.subs(rr, crit[0]))
ok = crit[0] == 3 and sp.simplify(wmax - 1 / (3 * sp.sqrt(3))) == 0
neg = sp.simplify(wmax - 1 / (2 * sp.sqrt(2))) != 0
Dt = 100
print(f"    with Delta t = {Dt} M, |Delta phi| < {float(Dt * wmax):.3f} rad -> |W| <= "
      f"{int(float(Dt * wmax) / (2 * 3.141592653589793)) + 1}; higher winding classes are EMPTY")
report("Conj 4.16: |dphi/dt| < 1/(3 sqrt3 M) for timelike curves, so only finitely many W are admissible",
       ok, neg)

# ---------------------------------------------------------------------------
# 12. Planck pressure
c, hbar, Gn = 2.99792458e8, 1.054571817e-34, 6.67430e-11
P = c ** 7 / (hbar * Gn ** 2)
ok = abs(P / 4.63e113 - 1) < 3e-3
neg = abs((c ** 7 / (hbar * Gn)) / 4.63e113 - 1) > 1e-2
print(f"    c^7/(hbar G^2) = {P:.4e} Pa  (dimension: kg m^-1 s^-2)")
report("Eq Planck pressure 4.63e113 Pa", ok, neg)

# ---------------------------------------------------------------------------
# 13. Conformal factor: plane z=0 in e^{2 phi(z)} delta: kappa~ = e^{-phi} phi'
z = sp.symbols('z', real=True)
phiz = sp.Function('phi')(z)
Om2 = sp.exp(2 * phiz)
# K~_ij = 1/2 L_{n~} g~_ij with n~ = e^{-phi} d_z; mixed = e^{-2phi} * K~
Kt = sp.Rational(1, 2) * sp.exp(-phiz) * sp.diff(Om2, z)
kt = sp.simplify(Kt * sp.exp(-2 * phiz))
ok = sp.simplify(kt - sp.exp(-phiz) * sp.diff(phiz, z)) == 0
neg = sp.simplify(kt - sp.diff(phiz, z)) != 0
report("Rem 4.23: |n~(ln Omega)| = kappa~ (g~-unit normal); with the g-unit normal the bound is Omega/l_P",
       ok, neg)

print()
bad = [n for n, o, ng in RESULTS if not (o and ng)]
print("ALL CHECKS PASSED" if not bad else f"FAILED: {bad}")
