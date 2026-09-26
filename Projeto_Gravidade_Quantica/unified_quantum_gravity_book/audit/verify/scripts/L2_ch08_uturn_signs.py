"""Camada 2 (F-43, cap. 8). Oraculos independentes das coordenadas de Fermi usadas pelo corretor.

A. Teorema 3.3 (U-turn em tubos de H^2 e S^2): curvas integradas nos modelos MERGULHADOS
   (S^2 de raio 1/c em R^3; hiperboloide de raio 1/c em R^{2,1}), com o angulo medido contra o
   campo de Killing (rotacao / boost) normalizado. Curvatura constante k a partir de y = -w/2:
   o ponto onde a tangente vira -e_x deve estar em y = +w/2 exatamente quando k = k0; busca
   aleatoria bang-bang com |kappa| <= 0.98 k0 nao pode produzir U-turn dentro do tubo.
   Identidades do passo final da prova (sympy). Mutacoes de k0 devem falhar.
B. Tubo em torno de geodesica (coth) versus equidistante de hiperplano (tanh) em H^3, sympy:
   curvatura seccional -1 e curvaturas principais.
C. Cota de winding |W| < dt/(6 sqrt3 pi M) + 1/2 e nitidez (curva temporal com |W| = 3 em dt = 100M).
D. Sinais: K_ij (Milne), II = -K n, theta_l (esfera de Minkowski e horizonte PG, calculado em 4D),
   Israel (casca estatica de poeira: densidade positiva).
E. Def. 2.3: contraexemplo da esfera de Minkowski com normal lorentziana.
F. Cota de densidade de energia: dimensao e valor.
Rodar do diretorio do livro:  python audit/verify/scripts/L2_ch08_uturn_signs.py
"""
import numpy as np
import sympy as sp
from scipy import integrate

FAIL = []


def check(name, ok, info=""):
    print(f"[{'OK  ' if ok else 'FAIL'}] {name} {info}")
    if not ok:
        FAIL.append(name)


def mutants_fail(name, results):
    bad = [k for k, v in results.items() if v]
    check(f"NEG {name}: all mutants rejected", not bad, f"mutants that passed: {bad}")


# =============================================================== A. U-turn, modelos mergulhados
ETA = np.diag([-1.0, 1.0, 1.0])


class Sphere:
    def __init__(self, c):
        self.c, self.R = c, 1 / c

    def ip(self, a, b):
        return a @ b

    def start(self, y0):
        R = self.R
        return np.array([R * np.cos(y0 / R), 0.0, R * np.sin(y0 / R)]), np.array([0.0, 1.0, 0.0])

    def frame(self, P):
        n = P / np.linalg.norm(P)
        ex = np.cross([0, 0, 1.0], P); ex /= np.linalg.norm(ex)       # rotation Killing field, normalized
        ey = np.cross(n, ex)                                            # points to increasing latitude
        return ex, ey

    def normal(self, P, T):
        return np.cross(P / np.linalg.norm(P), T)

    def y(self, P):
        return self.R * np.arcsin(np.clip(P[2] / self.R, -1, 1))

    def acc(self, P):          # geodesic acceleration
        return -self.c**2 * P


class Hyperboloid:
    def __init__(self, c):
        self.c, self.R = c, 1 / c

    def ip(self, a, b):
        return a @ ETA @ b

    def start(self, y0):
        R = self.R
        return np.array([R * np.cosh(y0 / R), 0.0, R * np.sinh(y0 / R)]), np.array([0.0, 1.0, 0.0])

    def unit(self, v):
        return v / np.sqrt(self.ip(v, v))

    def frame(self, P):
        X = np.array([P[1], P[0], 0.0])                                 # boost Killing field
        ex = self.unit(X)
        ey = self.unit(ETA @ np.cross(P, ex))                           # eta-orthogonal to P and ex
        if ey[2] < 0:
            ey = -ey
        return ex, ey

    def normal(self, P, T):
        N = self.unit(ETA @ np.cross(P, T))
        ex, ey = self.frame(P)
        # orientation: same handedness as (ex, ey)
        s = np.sign(self.ip(N, ey) * self.ip(T, ex) - self.ip(N, ex) * self.ip(T, ey))
        return s * N

    def y(self, P):
        return self.R * np.arcsinh(P[2] / self.R)

    def acc(self, P):
        return self.c**2 * P


def run(M, w, kappa_fn, smax):
    P0, T0 = M.start(-w / 2)

    def rhs(s, u):
        P, T = u[:3], u[3:]
        return np.concatenate([T, M.acc(P) + kappa_fn(s) * M.normal(P, T)])

    def theta(u):
        ex, ey = M.frame(u[:3])
        return np.arctan2(M.ip(u[3:], ey), M.ip(u[3:], ex))

    ss = np.linspace(0, smax, int(smax / (w / 2000)) + 2)
    far = lambda s_, u: M.y(u[:3]) ** 2 - w**2          # smooth stop once clearly outside the tube
    far.terminal = True
    sol = integrate.solve_ivp(rhs, (0, smax), np.concatenate([P0, T0]), t_eval=ss, events=far,
                              rtol=1e-11, atol=1e-13, max_step=w / 400)
    ss = sol.t
    U_ = sol.y
    ys = np.array([M.y(U_[:3, i]) for i in range(U_.shape[1])])
    sn = np.array([M.ip(U_[3:, i], M.frame(U_[:3, i])[1]) for i in range(U_.shape[1])])
    cs = np.array([M.ip(U_[3:, i], M.frame(U_[:3, i])[0]) for i in range(U_.shape[1])])
    idx_turn = None
    for i in range(1, len(ss) - 1):
        if cs[i] < -0.99 and sn[i] * sn[i + 1] <= 0:
            idx_turn = i
            break
    outs = np.nonzero(np.abs(ys) > w / 2 + 1e-7)[0]
    first_out = outs[0] if outs.size else None
    ok_uturn = idx_turn is not None and (first_out is None or first_out > idx_turn)
    left = first_out is not None and (idx_turn is None or first_out <= idx_turn)
    if idx_turn is not None:
        lam = sn[idx_turn] / (sn[idx_turn] - sn[idx_turn + 1]) if sn[idx_turn] != sn[idx_turn + 1] else 0.0
        y_end = ys[idx_turn] + lam * (ys[idx_turn + 1] - ys[idx_turn])
        ok_uturn = ok_uturn and abs(abs(theta(U_[:, idx_turn])) - np.pi) < 1e-2
    else:
        y_end = np.nan
    return ok_uturn and not left, y_end, ys.max(), left


def k0(geom, c, w):
    return c / np.tanh(c * w / 2) if geom == "H2" else c / np.tan(c * w / 2)


cases = [("H2", 1.0, 0.5), ("H2", 1.0, 1.5), ("H2", 2.0, 1.5), ("S2", 1.0, 0.5), ("S2", 1.0, 1.6),
         ("S2", 1.0, 2.4), ("S2", 1.0, 3.0), ("S2", 0.5, 5.0)]
for geom, c, w in cases:
    M = Hyperboloid(c) if geom == "H2" else Sphere(c)
    k = k0(geom, c, w)
    ok, yend, ymax, out = run(M, w, lambda s: k, np.pi / k + 2 * w)
    check(f"A {geom} c={c} w={w}: constant kappa=k0 turns exactly at y=+w/2", ok and abs(yend - w / 2) < 1e-5,
          f"k0={k:.6f}, y_end={yend:.8f}, w/2={w/2}")
    _, yend_lo, _, out_lo = run(Hyperboloid(c) if geom == "H2" else Sphere(c), w + 1.0 if False else w,
                                lambda s: 0.99 * k, np.pi / k + 2 * w)
    check(f"A {geom} c={c} w={w}: kappa = 0.99 k0 leaves the tube", out_lo)
    mut = {"2/w": 2 / w, "c coth(cw)" if geom == "H2" else "c cot(cw)": (c / np.tanh(c * w) if geom == "H2" else c / np.tan(c * w)),
           "c tanh(cw/2)": c * np.tanh(c * w / 2), "0.97 k0": 0.97 * k}
    res = {}
    for lab, km in mut.items():
        if km <= 0:
            res[lab] = False
            continue
        okm, ym, _, _ = run(M, w, lambda s, km=km: km, np.pi / km + 2 * w)
        res[lab] = okm and abs(ym - w / 2) < 1e-4
    mutants_fail(f"A {geom} c={c} w={w} (alternative k0)", res)

# random bang-bang controls, |kappa| <= 0.98 k0, embedded models
rng = np.random.default_rng(11)
for geom, c, w in (("H2", 1.0, 1.0), ("S2", 1.0, 2.4), ("S2", 1.0, 3.0)):
    M = Hyperboloid(c) if geom == "H2" else Sphere(c)
    k = k0(geom, c, w)
    hits = {0.98: 0, 1.05: 0}
    for fac in hits:
        for _ in range(40):
            n = rng.integers(1, 5)
            knots = np.sort(rng.uniform(0, 4 * w + 4, n))
            sg = rng.choice([1.0, 1.0, 1.0, -1.0], n + 1) * rng.uniform(0.9, 1.0, n + 1)
            ok, yend, ymax, out = run(M, w, lambda s: fac * k * sg[np.searchsorted(knots, s)], 3 * w + 6)
            if ok and not out:
                hits[fac] += 1
    check(f"A {geom} w={w}: random controls, no U-turn at 0.98 k0; some at 1.05 k0 (positive control)",
          hits[0.98] == 0 and hits[1.05] > 0, f"hits={hits}")

# symbolic identities used in the last step of the proof
a_, b_, c_ = sp.symbols("a b c", real=True)
id1 = sp.simplify((sp.cosh(c_ * a_) + sp.cosh(c_ * b_)) / sp.integrate(sp.cosh(c_ * sp.Symbol("y")), (sp.Symbol("y"), a_, b_))
                  - c_ * sp.coth(c_ * (b_ - a_) / 2))
id2 = sp.simplify((sp.cos(c_ * a_) + sp.cos(c_ * b_)) / sp.integrate(sp.cos(c_ * sp.Symbol("y")), (sp.Symbol("y"), a_, b_))
                  - c_ * sp.cot(c_ * (b_ - a_) / 2))
num = [float(id1.subs({a_: -0.3, b_: 0.9, c_: 1.7})), float(sp.N(id2.subs({a_: -1.1, b_: 1.4, c_: 1.0})))]
check("A proof identities (G(a)+G(b))/int G = c coth / c cot of c(b-a)/2", max(abs(v) for v in num) < 1e-12, f"{num}")
wrong = float(sp.N(((sp.cosh(-0.3) + sp.cosh(0.9)) / (sp.sinh(0.9) - sp.sinh(-0.3))) - sp.tanh(0.6)))
check("NEG A identity with tanh in place of coth fails", abs(wrong) > 1e-3, f"{wrong:.3f}")
# cos(c(a+b)/2) > 0 on the S^2 tube for all w < pi/c
grid = np.linspace(-np.pi / 2 + 1e-9, np.pi / 2 - 1e-9, 2001)
A, B = np.meshgrid(grid, grid)
check("A S^2: cos((a+b)/2) > 0 for a, b in [-w/2, w/2], w < pi (c = 1)", np.all(np.cos((A + B) / 2) > 0))
check("A comparison x coth x > 1 > x cot x on (0, pi/2)", np.all(grid[grid > 0] / np.tanh(grid[grid > 0]) > 1) and
      np.all(grid[(grid > 0)] / np.tan(grid[grid > 0]) < 1))

# =============================================================== B. tubo versus equidistante em H^3
r, ph, t, d, uu, vv = sp.symbols("r phi t d u v", positive=True)


def riemann_sectional(g, X):
    n = len(X)
    ginv = g.inv()
    Gam = [[[sp.simplify(sum(ginv[i, l] * (sp.diff(g[l, j], X[k]) + sp.diff(g[l, k], X[j]) - sp.diff(g[j, k], X[l]))
                             for l in range(n)) / 2) for k in range(n)] for j in range(n)] for i in range(n)]

    def Riem(i, j, k, l):  # R^i_{jkl}
        e = sp.diff(Gam[i][l][j], X[k]) - sp.diff(Gam[i][k][j], X[l])
        e += sum(Gam[i][k][m] * Gam[m][l][j] - Gam[i][l][m] * Gam[m][k][j] for m in range(n))
        return e

    secs = []
    for a in range(n):
        for b in range(a + 1, n):
            Rabab = sum(g[a, m] * Riem(m, b, a, b) for m in range(n))
            secs.append(sp.simplify(Rabab / (g[a, a] * g[b, b] - g[a, b] ** 2)))
    return secs


g_tube = sp.diag(1, sp.sinh(r) ** 2, sp.cosh(r) ** 2)          # H^3 about a geodesic (t along it)
secs = riemann_sectional(g_tube, [r, ph, t])
check("B metric dr^2 + sinh^2 r dphi^2 + cosh^2 r dt^2 has sectional curvature -1", all(abs(float(s.subs(r, rv)) + 1) < 1e-12 for s in secs for rv in (0.3, 1.1, 2.5)), str(secs))
shape_tube = [sp.simplify(sp.diff(g_tube[i, i], r) / (2 * g_tube[i, i])) for i in (1, 2)]
check("B tube r = d: principal curvatures coth d (phi), tanh d (t); max = coth d",
      sp.simplify(shape_tube[0] - sp.coth(r)) == 0 and sp.simplify(shape_tube[1] - sp.tanh(r)) == 0, str(shape_tube))
g_eq = sp.diag(1, sp.cosh(r) ** 2, sp.cosh(r) ** 2 * sp.sinh(uu) ** 2)   # H^3 as warped product over H^2 (u, v)
g_eq_full = sp.diag(1, sp.cosh(r) ** 2, sp.cosh(r) ** 2 * sp.sinh(uu) ** 2)
secs_eq = riemann_sectional(g_eq_full, [r, uu, vv])
check("B metric dr^2 + cosh^2 r g_{H^2} has sectional curvature -1", all(abs(float(s.subs({r: rv, uu: 0.7})) + 1) < 1e-12 for s in secs_eq for rv in (0.3, 1.1, 2.5)), str(secs_eq))
shape_eq = [sp.simplify(sp.diff(g_eq_full[i, i], r) / (2 * g_eq_full[i, i])) for i in (1, 2)]
check("B equidistant r = d from a hyperplane: umbilic, tanh d", all(sp.simplify(s - sp.tanh(r)) == 0 for s in shape_eq))
dval = 0.7
mutants_fail("B", {"tube norm = tanh d": abs(max(float(e.subs(r, dval)) for e in shape_tube) - np.tanh(dval)) < 1e-9,
                   "equidistant norm = coth d": abs(float(shape_eq[0].subs(r, dval)) - 1 / np.tanh(dval)) < 1e-9})

# =============================================================== C. winding
M_ = sp.symbols("M", positive=True)
rr = sp.symbols("r", positive=True)
h = sp.sqrt(1 - 2 * M_ / rr) / rr
crit = sp.solve(sp.diff(h ** 2, rr), rr)
hmax = sp.simplify(h.subs(rr, crit[0]))
check("C max_{r>2M} sqrt(f)/r = 1/(3 sqrt3 M) at r = 3M", crit == [3 * M_] and sp.simplify(hmax - 1 / (3 * sp.sqrt(3) * M_)) == 0,
      f"crit={crit}, max={hmax}")
dt = 100.0
bound = dt / (6 * np.sqrt(3) * np.pi) + 0.5
Wmax = int(np.ceil(bound) - 1)
check("C Delta t = 100 M: |W| < 3.56 so |W| <= 3", Wmax == 3, f"bound={bound:.4f}")
# sharpness: a circular worldline at r = 3M with dphi/dt = 0.999 sqrt(f)/r is timelike and winds 3 times in 100 M
om = 0.999 / (3 * np.sqrt(3))
f3 = 1 - 2 / 3
norm = -f3 + (3.0**2) * om**2
turns = om * dt / (2 * np.pi)
check("C bound nearly attained: timelike circular worldline at r=3M makes > 3 turns in 100 M", norm < 0 and turns > 3,
      f"g(u,u) ~ {norm:.2e} dt^2, turns={turns:.3f}")
mutants_fail("C", {"max at r=4M": abs(float(h.subs({M_: 1, rr: 4})) - 1 / (3 * np.sqrt(3))) < 1e-9,
                   "bound without 2 pi": int(np.ceil(dt / (3 * np.sqrt(3)) + 0.5) - 1) == 3})

# =============================================================== D. sinais
tau, chi, th, phv = sp.symbols("tau chi theta phi", positive=True)
Xm = [tau, chi, th, phv]
gM = sp.diag(-1, tau**2, tau**2 * sp.sinh(chi) ** 2, tau**2 * sp.sinh(chi) ** 2 * sp.sin(th) ** 2)   # Milne


def christoffel(g, X):
    n = len(X)
    gi = g.inv()
    return [[[sp.simplify(sum(gi[i, l] * (sp.diff(g[l, j], X[k]) + sp.diff(g[l, k], X[j]) - sp.diff(g[j, k], X[l]))
                              for l in range(n)) / 2) for k in range(n)] for j in range(n)] for i in range(n)]


Gm = christoffel(gM, Xm)
gam = gM[1:, 1:]
K_lie = sp.simplify(-sp.Rational(1, 2) * sp.diff(gam, tau))                     # n = d_tau, -1/2 L_n gamma
K_dd_n = sp.Matrix(3, 3, lambda i, j: sp.simplify(Gm[0][i + 1][j + 1] * gM[0, 0]))  # g(nabla_i d_j, n), n = d_tau
K_dn = sp.Matrix(3, 3, lambda i, j: -sp.simplify(sum(Gm[m][i + 1][0] * gM[m, j + 1] for m in range(4))))  # -g(nabla_i n, d_j)
check("D Milne: -1/2 L_n gamma = -g(nabla_i n, d_j) = g(nabla_i d_j, n) = -gamma/tau",
      sp.simplify(K_lie - K_dd_n) == sp.zeros(3) and sp.simplify(K_lie - K_dn) == sp.zeros(3)
      and sp.simplify(K_lie + gam / tau) == sp.zeros(3))
II_normal_coeff = sp.Matrix(3, 3, lambda i, j: Gm[0][i + 1][j + 1])               # normal part of nabla_i d_j = coeff * n
check("D II(d_i, d_j) = -K_ij n", sp.simplify(II_normal_coeff + K_lie) == sp.zeros(3))
mutants_fail("D Milne", {"K = +1/2 L_n gamma matches g(nabla d, n)": sp.simplify(-K_lie - K_dd_n) == sp.zeros(3)})

# theta_l for the sphere t=0, r=R in Minkowski (spherical coordinates), l = d_t + d_r
T_, R_ = sp.symbols("t R", positive=True)
Xs = [T_, rr, th, phv]
gS = sp.diag(-1, 1, rr**2, rr**2 * sp.sin(th) ** 2)
Gs = christoffel(gS, Xs)
l = [1, 1, 0, 0]


def cov_l(Gam, lvec, a):  # (nabla_a l)^i for constant components
    return [sum(Gam[i][a][m] * lvec[m] for m in range(4)) for i in range(4)]


def theta_null(g, Gam, lvec):
    tot = 0
    for a in (2, 3):
        v = cov_l(Gam, lvec, a)
        tot += sum(g[a, i] * v[i] for i in range(4)) / g[a, a]
    return sp.simplify(tot)


th_mink = theta_null(gS, Gs, l)
II_l = sum(Gs[1][a][a] * gS[1, 1] * l[1] / gS[a, a] for a in (2, 3))     # q^{ab} g(II(e_a,e_b), l), II = normal part of nabla e_a e_a (r-component)
check("D Minkowski sphere: q^{ab} g(nabla_a l, e_b) = 2/r = -q^{ab} g(II, l)",
      sp.simplify(th_mink - 2 / rr) == 0 and sp.simplify(-II_l - 2 / rr) == 0, f"{th_mink}, {sp.simplify(II_l)}")
mutants_fail("D theta_l", {"theta_l = +q g(II, l)": sp.simplify(II_l - 2 / rr) == 0})

# PG horizon: theta_l computed in 4D from the Christoffel symbols
Mq, Q = sp.symbols("M Q", positive=True)
beta = sp.sqrt(2 * Mq / rr - Q**2 / rr**2)
Xp = [T_, rr, th, phv]
gP = sp.Matrix([[-1 + beta**2, beta, 0, 0], [beta, 1, 0, 0], [0, 0, rr**2, 0], [0, 0, 0, rr**2 * sp.sin(th) ** 2]])
Gp = christoffel(gP, Xp)


def theta_general(g, Gam, lvec, X):
    tot = 0
    for a in (2, 3):
        v = [sp.diff(lvec[i], X[a]) + sum(Gam[i][a][m] * lvec[m] for m in range(4)) for i in range(4)]
        tot += sum(g[a, i] * v[i] for i in range(4)) / g[a, a]
    return sp.simplify(tot)


n_up = [1, -beta, 0, 0]                           # lapse 1, shift beta^r = beta
s_up = [0, 1, 0, 0]
l_up = [n_up[i] + s_up[i] for i in range(4)]
norm_n = sp.simplify(sum(gP[i, j] * n_up[i] * n_up[j] for i in range(4) for j in range(4)))
null_l = sp.simplify(sum(gP[i, j] * l_up[i] * l_up[j] for i in range(4) for j in range(4)))
thP = theta_general(gP, Gp, l_up, Xp)
check("D PG: n unit timelike, l null, theta_l = 2(1 - beta)/r", norm_n == -1 and null_l == 0 and sp.simplify(thP - 2 * (1 - beta) / rr) == 0,
      f"theta_l={thP}")
vals = [(1, 0), (1, 0.5), (1, 0.9), (2, 1)]
zs = [float(thP.subs({Mq: m, Q: q, rr: m + np.sqrt(m * m - q * q)})) for m, q in vals]
check("D PG: theta_l(r_+) = 0", max(abs(z) for z in zs) < 1e-12, f"{zs}")
mutants_fail("D PG", {"shift sign flipped": abs(float(theta_general(gP, Gp, [1, 1 + beta, 0, 0], Xp).subs({Mq: 1, Q: 0, rr: 2}))) < 1e-9})

# Israel: static dust shell at r = R0, Minkowski inside, Schwarzschild (mass M) outside, G = 1.
# K_ab = h h nabla_a n_b with n from - (inside) to + (outside); sigma = S_ab u^a u^b = -S^t_t.
R0, Ms = sp.symbols("R0 M_s", positive=True)
fout = 1 - 2 * Ms / R0
Kth_in, Kth_out = 1 / R0, sp.sqrt(fout) / R0                    # K^theta_theta = sqrt(f)/r
Ktt_in, Ktt_out = 0, sp.diff(1 - 2 * Ms / rr, rr).subs(rr, R0) / (2 * sp.sqrt(fout))  # K^t_t = f'/(2 sqrt f)
jKtt, jKth = Ktt_out - Ktt_in, Kth_out - Kth_in
jK = jKtt + 2 * jKth
Stt = -(jKtt - jK) / (8 * sp.pi)                                   # S^t_t = -(1/8pi)([K^t_t] - [K])
sigma = sp.simplify(-Stt)
check("D Israel sign: static dust shell has sigma = (1 - sqrt(1-2M/R))/(4 pi R) > 0",
      sp.simplify(sigma - (1 - sp.sqrt(fout)) / (4 * sp.pi * R0)) == 0 and float(sigma.subs({Ms: 1, R0: 5})) > 0)
mutants_fail("D Israel", {"opposite sign gives sigma > 0": float((-sigma).subs({Ms: 1, R0: 5})) > 0})

# =============================================================== E. Def. 2.3 counterexample
eta_ = sp.symbols("eta", positive=True)
IIvec = [0, -1 / R_, 0, 0]                        # II(e_th, e_th) for the sphere t=0, r=R (normal part of nabla, r-component)
nu = [sp.cosh(eta_), sp.sinh(eta_), 0, 0]
gmink = sp.diag(-1, 1, 1, 1)
pair = sp.simplify(sum(gmink[i, i] * IIvec[i] * nu[i] for i in range(4)))
check("E Minkowski sphere: |g(II, nu)| = sinh(eta)/R (unbounded), |II| = 1/R, nu unit timelike",
      sp.simplify(pair + sp.sinh(eta_) / R_) == 0 and sp.simplify(-sp.cosh(eta_) ** 2 + sp.sinh(eta_) ** 2 + 1) == 0)

# =============================================================== F. densidade de energia
from sympy.physics import units as U
expr = U.speed_of_light**7 / (U.hbar * U.gravitational_constant**2)
val = U.convert_to(expr, U.joule / U.meter**3)
num = float(sp.N(val / (U.joule / U.meter**3)))
check("F c^7/(hbar G^2) is an energy density ~4.63e113 J/m^3", abs(num / 4.633e113 - 1) < 2e-3, f"{val}")
check("F (3/8pi) c^7/(hbar G^2) ~ 5.5e112 J/m^3", abs(3 / (8 * np.pi) * num / 5.5e112 - 1) < 0.01, f"{3/(8*np.pi)*num:.3e}")
lP2 = U.hbar * U.gravitational_constant / U.speed_of_light**3
same = sp.simplify(U.convert_to(3 * U.speed_of_light**4 / (8 * sp.pi * U.gravitational_constant * lP2) - 3 / (8 * sp.pi) * expr, U.joule / U.meter**3))
check("F 3c^4/(8 pi G l_P^2) = (3/8pi) c^7/(hbar G^2)", same == 0, str(same))
mutants_fail("F", {"prefactor 1 instead of 3/8pi": abs(num / 5.5e112 - 1) < 0.01,
                   "c^5 instead of c^7": abs(float(U.convert_to(U.speed_of_light**5 / (U.hbar * U.gravitational_constant**2),
                                                                    U.joule / U.meter**3).args[0] if False else 0) - 4.6e113) < 1e110})

print("\nFALHAS:", FAIL if FAIL else "nenhuma")
raise SystemExit(1 if FAIL else 0)
