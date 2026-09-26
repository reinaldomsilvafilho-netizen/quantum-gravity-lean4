"""L2 residual check (2026-09-25), chapters 11 and 12.

ch11 (A) scalar curvature of c1 du^2 + c2 e^{2u} dx^2 (d = 2,3,4) by an own
         Riemann-tensor routine in sympy; mutations -d(d-1)/c2 and -d(d-1)c1.
ch11 (B) BKM/SLD ratio: SLD via a Sylvester solve, BKM via the integral
         int_0^inf tr(X (rho+s)^-1 X (rho+s)^-1) ds (no eigen-formula).
ch12 (C) erfc closed form of the 4D return probability vs quadrature; the
         identity I1 = (1/tau - I0)/(2 l^2); SVW (arXiv:1105.6098) eqs.
         (3.6)-(3.8) transcribed from their source vs I0 / 2.
ch12 (D) F-44: C = a 1 + b e^{i delta} P + b e^{-i delta} P^-1; eigenvalues,
         C^2, CKM for two circulant sectors (eigh, not DFT).
Run from the book folder.
"""
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.linalg import solve_sylvester, eigh
from scipy.special import erfc, erf, erfcx

FAILS = []


def check(name, cond):
    print(("OK   " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


# ---------------------------------------------------------------- (A)
def scalar_curvature(g, coords):
    n = len(coords)
    ginv = g.inv()
    Gam = [[[sp.simplify(sum(ginv[a, d] * (sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b])
                                         - sp.diff(g[b, c], coords[d])) for d in range(n)) / 2)
             for c in range(n)] for b in range(n)] for a in range(n)]
    def Riem(a, b, c, d):  # R^a_{bcd}
        r = sp.diff(Gam[a][b][d], coords[c]) - sp.diff(Gam[a][b][c], coords[d])
        r += sum(Gam[a][c][e] * Gam[e][b][d] - Gam[a][d][e] * Gam[e][b][c] for e in range(n))
        return r
    Ric = sp.Matrix(n, n, lambda b, d: sum(Riem(a, b, a, d) for a in range(n)))
    return sp.simplify(sum(ginv[b, d] * Ric[b, d] for b in range(n) for d in range(n)))


c1, c2 = sp.symbols("c1 c2", positive=True)
for d in (2, 3, 4):
    u = sp.Symbol("u")
    xs = sp.symbols("x1:%d" % d)
    coords = [u, *xs]
    g = sp.diag(c1, *([c2 * sp.exp(2 * u)] * (d - 1)))
    R = scalar_curvature(g, coords)
    check("ch11 d=%d: R = -d(d-1)/c1 for every c2" % d, sp.simplify(R + d * (d - 1) / c1) == 0)
    check("ch11 d=%d mutation R = -d(d-1)/c2 rejected" % d, sp.simplify(R + d * (d - 1) / c2) != 0)
# pull-back of L^2(dz^2+dx^2)/z^2 with z = z0 e^{-u}
L, z0, uu = sp.symbols("L z0 u", positive=True)
z = z0 * sp.exp(-uu)
gz = (L ** 2 / z ** 2) * sp.diff(z, uu) ** 2
gx = L ** 2 / z ** 2
check("ch11 pull-back gives c1 = L^2, c2 = L^2/z0^2 e^{2u}",
      sp.simplify(gz - L ** 2) == 0 and sp.simplify(gx - L ** 2 / z0 ** 2 * sp.exp(2 * uu)) == 0)

# ---------------------------------------------------------------- (B)
rng = np.random.default_rng(314159)


def sld(rho, X):
    Lm = solve_sylvester(rho, rho, 2 * X)  # rho L + L rho = 2X
    return np.real(np.trace(X @ Lm))


def bkm(rho, X):
    I = np.eye(rho.shape[0])
    def integrand(s):
        A = np.linalg.inv(rho + s * I)
        return np.real(np.trace(X @ A @ X @ A))
    # substitution s = t/(1-t)
    val, _ = quad(lambda t: integrand(t / (1 - t)) / (1 - t) ** 2, 0, 1, limit=400, epsabs=0, epsrel=1e-10)
    return val


ratios = []
for _ in range(3000):
    G = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    rho = G @ G.conj().T
    rho /= np.trace(rho).real
    H = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    X = (H + H.conj().T) / 2
    X -= np.trace(X) / 3 * np.eye(3)
    ratios.append(bkm(rho, X) / sld(rho, X))
ratios = np.array(ratios)
med, p95 = np.median(ratios), np.percentile(ratios, 95)
print("     BKM/SLD: min %.3f median %.3f p95 %.3f max %.2f" % (ratios.min(), med, p95, ratios.max()))
check("ch11 BKM >= SLD for all samples", ratios.min() >= 1 - 1e-8)
check("ch11 median about 1.16", abs(med - 1.16) < 0.02)
check("ch11 95%% of samples below 1.6", np.mean(ratios < 1.6) >= 0.95)
check("ch11 mutation: old range [1.01, 1.3] is contradicted", ratios.max() > 1.3 or ratios.min() < 1.01)
# unboundedness: p = (eps, 1/2, 1/2 - eps), X couples levels 0 and 1
vals = []
for eps in (1e-2, 1e-5, 1e-9):
    rho = np.diag([eps, 0.5, 0.5 - eps])
    X = np.zeros((3, 3)); X[0, 1] = X[1, 0] = 1.0
    vals.append(bkm(rho, X) / sld(rho, X))
print("     ratio for p1 = 1e-2, 1e-5, 1e-9:", np.round(vals, 2))
check("ch11 ratio unbounded as p_i -> 0 (monotone growth)", vals[0] < vals[1] < vals[2] and vals[2] > 5)
rho = np.diag([0.2, 0.3, 0.5]); X = np.diag([0.1, -0.3, 0.2])
check("ch11 control: commuting X gives ratio 1", abs(bkm(rho, X) / sld(rho, X) - 1) < 1e-8)

# ---------------------------------------------------------------- (C)
def P_quad(tau, l):
    # (2 pi)^-4 * 2 pi^2 * int_0^inf k^3 exp(-tau(k^2 + l^2 k^4)) dk
    v, _ = quad(lambda k: k ** 3 * np.exp(-tau * (k * k + l * l * k ** 4)), 0, np.inf, epsabs=0, epsrel=1e-12, limit=400)
    return 2 * np.pi ** 2 * v / (2 * np.pi) ** 4


def P_closed(tau, l, fn=None):
    zz = np.sqrt(tau) / (2 * l)
    term = np.sqrt(np.pi) * zz * erfcx(zz) if fn is None else np.sqrt(np.pi) * zz * np.exp(zz * zz) * fn(zz)
    return (1 - term) / (32 * np.pi ** 2 * l * l * tau)


def ds_closed(tau, l, sign=-1):
    zz = np.sqrt(tau) / (2 * l)
    return 1 + sign * tau / (2 * l * l) + 1 / (1 - np.sqrt(np.pi) * zz * erfcx(zz))


def ds_num(tau, l, h=1e-4):
    return -2 * (np.log(P_quad(tau * np.exp(h), l)) - np.log(P_quad(tau * np.exp(-h), l))) / (2 * h)


l = 1.0
taus = np.logspace(-3, 2, 11)
err_P = max(abs(P_closed(t, l) / P_quad(t, l) - 1) for t in taus)
err_ds = max(abs(ds_closed(t, l) - ds_num(t, l)) for t in taus)
print("     max rel err P: %.1e, max abs err d_s: %.1e" % (err_P, err_ds))
check("ch12 P closed form = quadrature on tau in [1e-3,1e2]", err_P < 1e-7)
check("ch12 d_s closed form = numerical log-derivative", err_ds < 1e-5)
check("ch12 d_s -> 2 (UV) and -> 4 (IR)", abs(ds_closed(1e-8, l) - 2) < 1e-3 and abs(ds_closed(1e5, l) - 4) < 1e-3)
check("ch12 IR approach d_s = 4 - 12 l^2/tau", abs((4 - ds_closed(1e4, l)) * 1e4 - 12) < 0.05)
check("ch12 mutation erf instead of erfc rejected", abs(P_closed(1.0, l, fn=erf) / P_quad(1.0, l) - 1) > 1e-2)
check("ch12 mutation +tau/(2l^2) in d_s rejected", abs(ds_closed(1.0, l, sign=+1) - ds_num(1.0, l)) > 0.1)
# identity I1 = (1/tau - I0)/(2 l^2)
for t in (0.01, 1.0, 30.0):
    I0 = quad(lambda x: np.exp(-t * (x + l * l * x * x)), 0, np.inf, epsrel=1e-12)[0]
    I1 = quad(lambda x: x * np.exp(-t * (x + l * l * x * x)), 0, np.inf, epsrel=1e-12)[0]
    check("ch12 I1 = (1/tau - I0)/(2 l^2) at tau=%g" % t, abs(I1 - (1 / t - I0) / (2 * l * l)) < 1e-9 * max(1, I1))
    check("ch12 mutation I1 = (1/tau - I0)/l^2 rejected at tau=%g" % t, abs(I1 - (1 / t - I0) / (l * l)) > 1e-4 * I1)
# SVW arXiv:1105.6098 eqs. (3.6)-(3.8) (transcribed from their LaTeX source):
# Z(s) = int k exp(-s k^2 (1 + k^2/(4K^2))) dk = (K/2) sqrt(pi/s) e^{sK^2} [1 - erf(sqrt(s K^2))]
# d_S(s) = 2 - 2 s K^2 + 2 sqrt(sK^2/pi) e^{-sK^2}/(1 - erf(sqrt(sK^2)))
for K in (0.5, 2.0):
    lK = 1 / (2 * K)
    for s in (0.05, 1.0, 5.0):
        Zq = quad(lambda k: k * np.exp(-s * k * k * (1 + k * k / (4 * K * K))), 0, np.inf, epsrel=1e-12)[0]
        Zsvw = K / 2 * np.sqrt(np.pi / s) * erfcx(np.sqrt(s) * K)
        I0 = quad(lambda x: np.exp(-s * (x + lK * lK * x * x)), 0, np.inf, epsrel=1e-12)[0]
        check("SVW (3.7) = quadrature and = I0/2 with l = 1/(2K) (K=%g, s=%g)" % (K, s),
              abs(Zsvw / Zq - 1) < 1e-8 and abs(Zq / (I0 / 2) - 1) < 1e-8)
    # their d_S vs numerical derivative, with d_S = 1 - 2 s dlnZ/ds (their exactds)
    s = 1.0; h = 1e-5
    Zf = lambda s_: K / 2 * np.sqrt(np.pi / s_) * erfcx(np.sqrt(s_) * K)
    dnum = 1 - 2 * s * (np.log(Zf(s + h)) - np.log(Zf(s - h))) / (2 * h)
    x = np.sqrt(s) * K
    dsvw = 2 - 2 * s * K * K + 2 * np.sqrt(s * K * K / np.pi) / erfcx(x)
    check("SVW (3.8) consistent with (3.7) (K=%g)" % K, abs(dnum - dsvw) < 1e-6)

# ---------------------------------------------------------------- (D) F-44
P = np.roll(np.eye(3), 1, axis=0)


def Cmat(a, b, dl):
    return a * np.eye(3) + b * np.exp(1j * dl) * P + b * np.exp(-1j * dl) * np.linalg.inv(P)


ok_eig, ok_sq, ok_perm = True, True, True
for _ in range(300):
    a, b, dl = rng.uniform(0.1, 2), rng.uniform(0, 2), rng.uniform(0, 2 * np.pi)
    C = Cmat(a, b, dl)
    ok_eig &= np.allclose(C, C.conj().T)
    ev = np.sort(np.linalg.eigvalsh(C))
    formula = np.sort([a + 2 * b * np.cos(dl + 2 * np.pi * j / 3) for j in (1, 2, 3)])
    ok_eig &= np.allclose(ev, formula)
    ok_sq &= np.allclose(np.sort(np.linalg.eigvalsh(C @ C)), np.sort(formula ** 2))
    ok_sq &= np.allclose(C @ C @ P, P @ C @ C)  # circulant
    Cu, Cd = C @ C, Cmat(*rng.uniform(0.1, 2, 2), rng.uniform(0, 2 * np.pi))
    Cd = Cd @ Cd
    _, Uu = eigh(Cu); _, Ud = eigh(Cd)
    V = np.abs(Uu.conj().T @ Ud)
    ok_perm &= np.allclose(np.sort(V.max(axis=1)), 1, atol=1e-6)
check("F-44 C Hermitian with eigenvalues a + 2b cos(delta + 2 pi j/3)", ok_eig)
check("F-44 M = C^2 circulant with eigenvalues v_j^2", ok_sq)
check("F-44 two circulant sectors: |V_CKM| is a permutation matrix", ok_perm)
a, b, dl = 1.0, 0.7, 0.3
ev = np.sort(np.linalg.eigvalsh(Cmat(a, b, dl)))
mut = np.sort([a + b * np.cos(dl + 2 * np.pi * j / 3) for j in (1, 2, 3)])
check("F-44 mutation (drop factor 2) rejected", not np.allclose(ev, mut))
Hn = rng.normal(size=(3, 3)); Hn = Hn + Hn.T
_, Uu = eigh(Cmat(1, .7, .3) @ Cmat(1, .7, .3)); _, Ud = eigh(Hn)
Vn = np.abs(Uu.T.conj() @ Ud)
check("F-44 control: non-circulant down sector gives nontrivial mixing", Vn.max(axis=1).min() < 0.95)
check("F-44 Y = (sqrt2/v) C^2 gives M = (v/sqrt2) Y = C^2", np.allclose((246.22 / np.sqrt(2)) * (np.sqrt(2) / 246.22) * (Cmat(1, .7, .3) @ Cmat(1, .7, .3)), Cmat(1, .7, .3) @ Cmat(1, .7, .3)))
# Koide
me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
Q = (me + mmu + mtau) / (np.sqrt(me) + np.sqrt(mmu) + np.sqrt(mtau)) ** 2
vv = np.sqrt([me, mmu, mtau]); a_ = vv.mean(); b2 = (np.sum(vv ** 2) - 3 * a_ ** 2) / 6
check("ch12 Koide Q = 1/3 + 2b^2/(3a^2) with PDG masses (Q=0.66666)", abs(Q - (1 / 3 + 2 * b2 / (3 * a_ ** 2))) < 1e-12 and abs(Q - 2 / 3) < 2e-5)

print("\nFAILURES:", FAILS if FAILS else "none")
raise SystemExit(1 if FAILS else 0)
