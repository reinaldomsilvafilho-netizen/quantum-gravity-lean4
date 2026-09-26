"""Camada 2 (F-42, cap. 12). Oraculos independentes, cada bloco com mutacoes que devem falhar.

A. Operador de Dirac do produto D_M x 1 + gamma5 x W com gamas euclidianas 4x4 e W 3x3 (tres geracoes):
   espectro +-sqrt(|k|^2 + m_i^2); com 1 no lugar de gamma5, +-|k| + m_i.
B. d_s UV do operador anisotropico omega^2 + k^2 + l^2 k^(2z) em 3+1: 1 + 3/z (z = 2 -> 5/2, z = 3 -> 2);
   isotropico k^2 + l^2 k^4 em 4D -> 2.
C. Fefferman-Graham: g_(2) a partir de AdS_5 global em coordenadas FG (fronteira R x S^3);
   coeficiente 16 pi G/(d L^(d-1)) de g_(d) a partir da brana negra planar AdS_5 em FG e da
   termodinamica (T, s, primeira lei), sem usar a formula de de Haro et al.
D. Curvatura de Ollivier: kappa >= -2 em grafos com arestas unitarias (LP de transporte, grafos
   aleatorios) e valor proximo de -2 atingido; metrica discreta -> kappa >= 0.
E. Contraexemplo de dois intervalos (Obs. 5.3): comprimentos regularizados por quadratura.
F. Casca fina: minimo do cubico e condicao 27 kappa^2 M^2 < 1 (sympy).
G. Koide (a, b), Q_q, Delta lambda.
Rodar do diretorio do livro:  python audit/verify/scripts/L2_ch12_fg_dirac_ollivier.py
"""
import numpy as np
import sympy as sp
from scipy import integrate, optimize

FAIL = []


def check(name, ok, info=""):
    print(f"[{'OK  ' if ok else 'FAIL'}] {name} {info}")
    if not ok:
        FAIL.append(name)


def mutants_fail(name, results):
    bad = [k for k, v in results.items() if v]
    check(f"NEG {name}: all mutants rejected", not bad, f"mutants that passed: {bad}")


# ================================================================ A. Dirac
s1 = np.array([[0, 1], [1, 0]], complex); s2 = np.array([[0, -1j], [1j, 0]]); s3 = np.diag([1, -1]).astype(complex)
I2 = np.eye(2)
gam = [np.kron(s1, s) for s in (s1, s2, s3)] + [np.kron(s2, I2)]          # Euclidean Clifford, {g_a, g_b} = 2 delta
g5 = gam[0] @ gam[1] @ gam[2] @ gam[3]
check("A Clifford algebra and gamma5 anticommutes, gamma5^2 = 1",
      all(np.allclose(gam[a] @ gam[b] + gam[b] @ gam[a], 2 * (a == b) * np.eye(4)) for a in range(4) for b in range(4))
      and all(np.allclose(g5 @ g + g @ g5, 0) for g in gam) and np.allclose(g5 @ g5, np.eye(4)))
rng = np.random.default_rng(5)
k = rng.normal(size=4)
DM = sum(k[a] * gam[a] for a in range(4))                                  # Hermitian symbol of D_M
masses = np.array([0.3, 1.7, 4.0])
Ur = np.linalg.qr(rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)))[0]
W = Ur @ np.diag(masses) @ Ur.conj().T
D_good = np.kron(DM, np.eye(3)) + np.kron(g5, W)
D_bad = np.kron(DM, np.eye(3)) + np.kron(np.eye(4), W)
kn = np.linalg.norm(k)
exp_good = np.sort(np.concatenate([s * np.sqrt(kn**2 + masses**2) for s in (1, -1)] * 2))
exp_bad = np.sort(np.concatenate([s * kn + masses for s in (1, -1)] * 2))
ev_g, ev_b = np.sort(np.linalg.eigvalsh(D_good)), np.sort(np.linalg.eigvalsh(D_bad))
check("A D x 1 + gamma5 x W: spectrum +-sqrt(k^2+m^2), D^2 = D_M^2 + W^2",
      np.allclose(ev_g, exp_good) and np.allclose(D_good @ D_good, np.kron(DM @ DM, np.eye(3)) + np.kron(np.eye(4), W @ W)))
check("A with 1 in place of gamma5: spectrum +-|k| + m (no gap)", np.allclose(ev_b, exp_bad))
mutants_fail("A", {"1 x W gives +-sqrt": np.allclose(ev_b, exp_good), "gamma5 gives +-|k|+m": np.allclose(ev_g, exp_bad)})

# ================================================================ B. dimensao espectral UV
def ds_aniso(tau, zexp):
    # P ~ int dw e^{-tau w^2} * int k^2 dk e^{-tau (k^2 + k^{2z})}; d_s = -2 dlnP/dlntau
    def lnP(t):
        return 0.5 * np.log(np.pi / t) + np.log(integrate.quad(lambda q: q**2 * np.exp(-t * (q**2 + q ** (2 * zexp))), 0, np.inf,
                                                                  epsrel=1e-12, limit=400)[0])
    h = 1e-4
    return -2 * (lnP(tau * np.exp(h)) - lnP(tau * np.exp(-h))) / (2 * h)


def ds_iso(tau):
    def lnP(t):
        return np.log(integrate.quad(lambda q: q**3 * np.exp(-t * (q**2 + q**4)), 0, np.inf, epsrel=1e-12, limit=400)[0])
    h = 1e-4
    return -2 * (lnP(tau * np.exp(h)) - lnP(tau * np.exp(-h))) / (2 * h)


d2, d3, di = ds_aniso(1e-10, 2), ds_aniso(1e-12, 3), ds_iso(1e-10)
check("B anisotropic 3+1: d_s(UV) = 1 + 3/z (z=2 -> 2.5, z=3 -> 2); isotropic k^2 + k^4 in 4D -> 2",
      abs(d2 - 2.5) < 2e-3 and abs(d3 - 2.0) < 2e-3 and abs(di - 2.0) < 2e-3, f"{d2:.4f}, {d3:.4f}, {di:.4f}")
mutants_fail("B", {"d_s = 3/z + 0 (no time direction)": abs(d2 - 1.5) < 2e-2, "d_s = 1 + 2/z": abs(d2 - 2.0) < 2e-2})

# ================================================================ C. Fefferman-Graham
z, L = sp.symbols("z L", positive=True)
# global AdS_5: rho with e^rho = 2/z gives g = L^2/z^2 [dz^2 - (1+z^2/4)^2 dt^2 + (1-z^2/4)^2 dOmega_3^2]
rho = sp.log(2 / z)
gtt = sp.expand(sp.simplify((-(sp.cosh(rho) ** 2) * z**2).rewrite(sp.exp)))
gSS = sp.expand(sp.simplify(((sp.sinh(rho) ** 2) * z**2).rewrite(sp.exp)))
drho_dz = sp.diff(rho, z)
check("C global AdS_5 in FG gauge: g_zz = L^2/z^2", sp.simplify(drho_dz**2 * z**2 - 1) == 0)
g2_tt = sp.simplify(sp.diff(sp.expand(gtt), z, 2).subs(z, 0) / 2)
g2_SS = sp.simplify(sp.diff(sp.expand(gSS), z, 2).subs(z, 0) / 2)
# boundary R x S^3 (unit): R_tt = 0, R_ab = 2 g_ab on S^3, R = 6; d = 4
d = 4
formula = lambda Rij, gij, Rs: -sp.Rational(1, d - 2) * (Rij - Rs / (2 * (d - 1)) * gij)
check("C g_(2) = -1/(d-2) (R_ij - R g_ij/(2(d-1))) for R x S^3 (tt and S^3 components)",
      sp.simplify(g2_tt - formula(0, -1, 6)) == 0 and sp.simplify(g2_SS - formula(2, 1, 6)) == 0, f"g2_tt={g2_tt}, g2_S3={g2_SS}")
mutants_fail("C g_(2)", {"+1/(d-2)": sp.simplify(g2_tt + formula(0, -1, 6)) == 0 and sp.simplify(g2_SS + formula(2, 1, 6)) == 0,
                         "R/(2d)": sp.simplify(g2_SS - (-sp.Rational(1, 2) * (2 - sp.Rational(6, 8)))) == 0})
# black brane AdS_5: ds^2 = L^2/zeta^2 (-h dt^2 + dx^2 + dzeta^2/h), h = 1 - zeta^4/zh^4.
zh, z0, Gn = sp.symbols("z_h z_0 G", positive=True)
zeta = z / sp.sqrt(1 + z**4 / z0**4)
hh = 1 - zeta**4 / zh**4
# FG condition dzeta/(zeta sqrt(h)) = dz/z holds for z0 = sqrt(2) zh
cond = sp.simplify((sp.diff(zeta, z) / (zeta * sp.sqrt(hh)) - 1 / z).subs(z0, sp.sqrt(2) * zh))
check("C black brane: zeta = z/sqrt(1 + z^4/z0^4) is FG gauge with z0 = sqrt2 z_h", sp.simplify(cond) == 0 or
      abs(float(cond.subs({zh: 1.3, z: 0.7}))) < 1e-12)
g_tt_FG = sp.simplify((-(hh) * z**2 / zeta**2).subs(z0, sp.sqrt(2) * zh))
g4_tt = sp.simplify(sp.series(g_tt_FG, z, 0, 5).removeO().coeff(z, 4))
# thermodynamics: T = 1/(pi z_h), s = L^3/(4 G z_h^3); first law d(eps) = T ds, eps(z_h -> oo) = 0
Tt = 1 / (sp.pi * zh); ss = L**3 / (4 * Gn * zh**3)
eps = sp.integrate(Tt * sp.diff(ss, zh), (zh, sp.oo, zh))
coef = sp.simplify(eps / g4_tt)                                   # <T_tt> = coef * g_(4)tt
check("C <T_tt> = (d L^(d-1)/(16 pi G)) g_(d)tt from first law (d = 4)", sp.simplify(coef - d * L**3 / (16 * sp.pi * Gn)) == 0,
      f"eps={sp.simplify(eps)}, g4_tt={g4_tt}, coef={coef}")
mutants_fail("C g_(d) coefficient", {"16 pi G/L^(d-1) (no d)": sp.simplify(coef - L**3 / (16 * sp.pi * Gn)) == 0,
                                      "16 pi G/(d L^d)": sp.simplify(coef - d * L**4 / (16 * sp.pi * Gn)) == 0})
check("C flat boundary: g_(2) = 0 for the brane (state enters at z^d)",
      sp.simplify(sp.series(g_tt_FG, z, 0, 3).removeO().coeff(z, 2)) == 0)

# ================================================================ D. Ollivier
def w1(mu, nu, Dm):
    n = len(mu)
    c = Dm.flatten()
    Aeq, beq = [], []
    for i in range(n):
        row = np.zeros(n * n); row[i * n:(i + 1) * n] = 1; Aeq.append(row); beq.append(mu[i])
    for j in range(n):
        row = np.zeros(n * n); row[j::n] = 1; Aeq.append(row); beq.append(nu[j])
    return optimize.linprog(c, A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=(0, None), method="highs").fun


def graph_dist(A):
    n = len(A)
    Dm = np.where(A > 0, 1.0, np.inf); np.fill_diagonal(Dm, 0)
    for kk in range(n):
        Dm = np.minimum(Dm, Dm[:, [kk]] + Dm[[kk], :])
    return Dm


minkappa, tested = 1.0, 0
for trial in range(12):
    n = int(rng.integers(6, 11))
    A = (rng.random((n, n)) < 0.4).astype(float); A = np.triu(A, 1); A = A + A.T
    Dm = graph_dist(A)
    if np.isinf(Dm).any():
        continue
    m = A / A.sum(1, keepdims=True)                              # non-lazy uniform measures
    for x in range(n):
        for y in range(x + 1, n):
            kap = 1 - w1(m[x], m[y], Dm) / Dm[x, y]
            minkappa = min(minkappa, kap); tested += 1
check("D unit-edge graphs: Ollivier kappa >= -2 on all pairs", minkappa >= -2 - 1e-9, f"min kappa = {minkappa:.3f} over {tested} pairs")
# near-extremal: two adjacent hubs, each with q private leaves -> kappa -> -2 + O(1/q)
q = 12
n = 2 + 2 * q
A = np.zeros((n, n)); A[0, 1] = A[1, 0] = 1
for i in range(q):
    A[0, 2 + i] = A[2 + i, 0] = 1; A[1, 2 + q + i] = A[2 + q + i, 1] = 1
Dm = graph_dist(A); m = A / A.sum(1, keepdims=True)
kap_e = 1 - w1(m[0], m[1], Dm) / Dm[0, 1]
check("D bound -2 is approached (hub-hub edge, -2 + 4/(q+1))", abs(kap_e - (-2 + 4 / (q + 1))) < 1e-9, f"kappa = {kap_e:.3f}")
Ddisc = np.ones((n, n)) - np.eye(n)
kap_disc = min(1 - w1(m[x], m[y], Ddisc) for x in range(n) for y in range(n) if x != y)
check("D discrete metric: kappa >= 0 (hypothesis kappa <= -c < 0 vacuous)", kap_disc >= -1e-12, f"min = {kap_disc:.3f}")
mutants_fail("D", {"bound -1": kap_e >= -1, "discrete metric allows negative kappa": kap_disc < -1e-9})

# ================================================================ E. dois intervalos em AdS_3
def reg_len(ell, eps):
    R = ell / 2          # semicircle x^2 + z^2 = R^2, length with L = 1: 2 int_{eps}^{R} R dz/(z sqrt(R^2 - z^2))
    return 2 * integrate.quad(lambda zz: R / (zz * np.sqrt(R * R - zz * zz)), eps, R, limit=400)[0]


eps_ = 1e-6
dlt = 0.1
disc = 2 * reg_len(1.0, eps_)
conn = reg_len(2 + dlt, eps_) + reg_len(dlt, eps_)
check("E delta = 0.1: disconnected - connected = -2 log(0.21) = 3.12 L", abs(disc - conn - (-2 * np.log(0.21))) < 1e-4,
      f"{disc - conn:.5f} vs {-2*np.log(0.21):.5f}")
check("E connected smaller iff delta(2+delta) < 1", all(((reg_len(2 + d_, eps_) + reg_len(d_, eps_)) < 2 * reg_len(1, eps_)) == (d_ * (2 + d_) < 1)
                                                       for d_ in (0.1, 0.3, 0.4, 0.45, 0.6)))
mutants_fail("E", {"excess -2 log 0.1": abs(disc - conn + 2 * np.log(0.1)) < 1e-3})

# ================================================================ F. casca fina
rr, kp, M = sp.symbols("r kappa M", positive=True)
cub = kp**2 * rr**3 - rr + 2 * M
rc = sp.solve(sp.diff(cub, rr), rr)
cmin = sp.simplify(cub.subs(rr, rc[0]))
check("F cubic minimum at r = 1/(sqrt3 kappa), value 2M - 2/(3 sqrt3 kappa)",
      sp.simplify(rc[0] - 1 / (sp.sqrt(3) * kp)) == 0 and sp.simplify(cmin - (2 * M - 2 / (3 * sp.sqrt(3) * kp))) == 0)
check("F min < 0 <=> 27 kappa^2 M^2 < 1", all((float(cmin.subs({kp: a, M: b})) < 0) == (27 * a * a * b * b < 1)
                                              for a, b in ((0.1, 1), (0.19, 1), (0.2, 1), (0.3, 1), (0.05, 3), (0.06, 4))))
ansatz = sp.symbols("rdot")
check("F ansatz K^th_th = kappa squared gives rdot^2 + 1 - 2M/r = kappa^2 r^2",
      sp.simplify(((1 - 2 * M / rr + ansatz**2) / rr**2 - kp**2) * rr**2 - (ansatz**2 + 1 - 2 * M / rr - kp**2 * rr**2)) == 0)
mutants_fail("F", {"condition 54 kappa^2 M^2 < 1": all((float(cmin.subs({kp: a, M: b})) < 0) == (54 * a * a * b * b < 1)
                                                        for a, b in ((0.1, 1), (0.15, 1)))})

# ================================================================ G. Koide, Q_q, Delta lambda
a, b, dl = sp.symbols("a b delta", positive=True)
v = [a + 2 * b * sp.cos(dl + 2 * sp.pi * j / 3) for j in (1, 2, 3)]
Qk = sp.simplify(sp.expand_trig(sum(x**2 for x in v)) / sp.expand_trig(sum(v)) ** 2)
n1 = sp.simplify(sp.expand_trig(sum(v)) ** 2 / 3)
n2 = sp.simplify(sp.expand_trig(sum(x**2 for x in v)) - n1)
check("G |v1|^2 = 3a^2, |v2|^2 = 6b^2, Q = 1/3 + 2b^2/(3a^2)",
      sp.simplify(n1 - 3 * a**2) == 0 and sp.simplify(n2 - 6 * b**2) == 0 and sp.simplify(Qk - (sp.Rational(1, 3) + 2 * b**2 / (3 * a**2))) == 0)
me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
Ql = (me + mmu + mtau) / (np.sqrt(me) + np.sqrt(mmu) + np.sqrt(mtau)) ** 2
check("G Q_l (PDG) = 2/3 to 1e-5", abs(Ql - 2 / 3) < 1e-5, f"{Ql:.7f}")
Qq = 2 / 3 * (1 + 0.1180 / np.sqrt(3))
check("G (2/3)(1 + alpha_s/sqrt3) = 0.712", abs(Qq - 0.712) < 5e-4, f"{Qq:.5f}")
vH = 246.22
dlam = 125.20**2 / (2 * vH**2) - 1 / 8
check("G v/2 = 123.11 GeV and Delta lambda = 0.0043 for m_H = 125.20", abs(vH / 2 - 123.11) < 1e-9 and abs(dlam - 0.0043) < 5e-5, f"{dlam:.5f}")
mutants_fail("G", {"|v2|^2 = 3b^2": sp.simplify(n2 - 3 * b**2) == 0, "Q_q with C_F=4/3": abs(2 / 3 * (1 + 0.118 * 4 / 3) - 0.712) < 5e-4})

print("\nFALHAS:", FAIL if FAIL else "nenhuma")
raise SystemExit(1 if FAIL else 0)
