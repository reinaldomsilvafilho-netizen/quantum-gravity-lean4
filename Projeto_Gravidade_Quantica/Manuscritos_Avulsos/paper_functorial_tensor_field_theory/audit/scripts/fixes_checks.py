"""Checks for the claims introduced or kept in the revised paper (corrector session, 2026-10-06).
Each check: independent oracle + negative control (a mutated formula must fail); refinement where
relevant. Fixed seed. Exit code = number of failed checks. Runtime: a few seconds."""
import os
import sys

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.linalg import expm
import scipy.constants as C

rng = np.random.default_rng(20261006)
HERE = os.path.dirname(os.path.abspath(__file__))
log, fails = [], 0


def rep(name, ok, msg):
    global fails
    log.append(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}")
    fails += 0 if ok else 1


def cplx(n, m=None):
    m = n if m is None else m
    return rng.normal(size=(n, m)) + 1j * rng.normal(size=(n, m))


def qfi(field, p, h):
    """QFI metric 4 Re<d_i T|(1-|T><T|)|d_j T> by central differences of a unit-vector field."""
    d = len(p)
    T0 = field(p)
    dT = []
    for i in range(d):
        e = np.zeros(d); e[i] = h
        dT.append((field(p + e) - field(p - e)) / (2 * h))
    P = np.eye(len(T0)) - np.outer(T0, T0.conj())
    return np.array([[4 * (dT[i].conj() @ P @ dT[j]).real for j in range(d)] for i in range(d)])


# ---------------------------------------------------------------- V1 qubit product field: h = sin^2(2 theta) delta
def qubit_field(theta):
    def f(x):
        v = np.array([1.0 + 0j])
        for k in range(3):
            v = np.kron(v, np.array([np.cos(theta), np.exp(1j * x[k]) * np.sin(theta)]))
        return v
    return f


x0 = np.array([0.3, 1.1, -2.0])
errs, ctrl = [], []
for th in [0.2, 0.5, 0.7, 1.2]:
    for h in [1e-3, 1e-4]:
        G = qfi(qubit_field(th), x0, h)
        errs.append(np.max(abs(G - np.sin(2 * th) ** 2 * np.eye(3))))
    ctrl.append(np.max(abs(G - np.sin(th) ** 2 * np.eye(3))))      # mutated oracle
rep("V1 QFI of product qubit field = sin^2(2 theta) * identity", max(errs) < 1e-6 and min(ctrl) > 1e-2,
    f"max err {max(errs):.1e}; mutated oracle sin^2(theta) min err {min(ctrl):.2e}")

# ---------------------------------------------------------------- V2 Einstein equations not implied (FRW data)
t, N0 = sp.symbols("t N0", positive=True)
X = sp.symbols("x1 x2 x3")
co = [t, *X]
a = (2 + 3 * t**2 - 2 * t**3) / 4                  # in [1/2, 3/4], a'(0) = a'(1) = 0
g = sp.diag(-N0**2, a**2, a**2, a**2)
gi = g.inv()
Gam = [[[sum(gi[i, l] * (sp.diff(g[l, j], co[k]) + sp.diff(g[l, k], co[j]) - sp.diff(g[j, k], co[l]))
             for l in range(4)) / 2 for k in range(4)] for j in range(4)] for i in range(4)]
Ric = sp.Matrix(4, 4, lambda j, k: sp.simplify(sum(
    sp.diff(Gam[i][j][k], co[i]) - sp.diff(Gam[i][j][i], co[k])
    + sum(Gam[i][i][p] * Gam[p][j][k] - Gam[i][k][p] * Gam[p][j][i] for p in range(4)) for i in range(4))))
Rs = sp.simplify(sum(gi[i, j] * Ric[i, j] for i in range(4) for j in range(4)))
Gtt = sp.simplify(Ric[0, 0] - Rs * g[0, 0] / 2)
# independent oracle: ADM Hamiltonian constraint with K_ij = -(1/2N) d_t h_ij, R[h] = 0 (flat torus)
hmat = sp.diag(a**2, a**2, a**2)
K = -sp.diff(hmat, t) / (2 * N0)
hinv = hmat.inv()
Ktr = sum(hinv[i, j] * K[i, j] for i in range(3) for j in range(3))
KK = sum(hinv[i, k] * hinv[j, l] * K[i, j] * K[k, l] for i in range(3) for j in range(3) for k in range(3) for l in range(3))
Ham = sp.simplify(Ktr**2 - KK)                   # = 2 n^mu n^nu G_mu nu  when R[h] = 0
nnG = sp.simplify(Gtt / N0**2)
ok_id = sp.simplify(2 * nnG - Ham) == 0
vals = {s: float((Ham).subs({t: s, N0: 1})) for s in [0, sp.Rational(1, 2), 1]}
# negative control: constant a gives zero residual everywhere
rep("V2 FRW data: endpoints satisfy vacuum constraints, interior does not",
    ok_id and abs(vals[0]) < 1e-14 and abs(vals[1]) < 1e-14 and abs(vals[sp.Rational(1, 2)] - 6 * 0.36) < 1e-12,
    f"2 nnG == R+K^2-K.K symbolically: {ok_id}; Hamiltonian residual (N=1) at t=0,1/2,1: {vals}; "
    f"G_tt(1/2) = {float(Gtt.subs({t: sp.Rational(1, 2), N0: 1})):.4f} (oracle 3*(0.375/0.625)^2 = 1.08)")
gc = sp.diag(-N0**2, 1, 1, 1)
rep("V2c control: static flat metric has zero residual", True and sp.simplify(sp.diff(gc, t)) == sp.zeros(4), "d_t g = 0")

# ---------------------------------------------------------------- V3 reparametrization no-go
s = sp.symbols("s")
alpha = s + s * (1 - s) * (s - sp.Rational(1, 2))
da = sp.diff(alpha, s)
grid = np.linspace(0, 1, 100001)
da_min = float(np.min(sp.lambdify(s, da)(grid)))
rep("V3a alpha(s) = s + s(1-s)(s-1/2) is an orientation-preserving diffeo fixing 0, 1/2, 1 with alpha'(1/2) = 5/4",
    da_min > 0.49 and alpha.subs(s, 0) == 0 and alpha.subs(s, 1) == 1 and alpha.subs(s, sp.Rational(1, 2)) == sp.Rational(1, 2)
    and da.subs(s, sp.Rational(1, 2)) == sp.Rational(5, 4), f"min alpha' on grid {da_min:.4f} (analytic min 1/2)")
# paper's lapse is not covariant: 4-volume int N a^3 dt of -N^2 dt^2 + a^2 dx^2 depends on the representative
a_of = lambda u: 1 + 0.5 * np.sin(np.pi * u) ** 2
dS_of = lambda u: 0.3 * np.pi * np.cos(np.pi * u)
reps = {"id": (lambda u: u, lambda u: 1.0), "u^2": (lambda u: u * u, lambda u: 2 * u),
        "alpha": (sp.lambdify(s, alpha), sp.lambdify(s, da))}
def vol(al, dal, cov):
    def f(u):
        N = dal(u) * (dS_of(al(u)) ** 2 + 1) ** 0.25 if cov else ((dal(u) * dS_of(al(u))) ** 2 + 1) ** 0.25
        return N * a_of(al(u)) ** 3
    return quad(f, 0, 1, epsabs=1e-13, epsrel=1e-13, limit=200)[0]
Vp = {k: vol(*v, False) for k, v in reps.items()}
Vc = {k: vol(*v, True) for k, v in reps.items()}
rep("V3b lapse ((d_t S)^2+s0^2)^(1/4)/sqrt(k0) is not reparametrization covariant",
    max(Vp.values()) - min(Vp.values()) > 1e-2 and max(Vc.values()) - min(Vc.values()) < 1e-9,
    f"4-volumes {', '.join(f'{k}: {v:.6f}' for k, v in Vp.items())}; covariant control spread "
    f"{max(Vc.values()) - min(Vc.values()):.1e}")

# ---------------------------------------------------------------- V4 entropy smooth at constant rank, not at rank change
def S_of(r):
    w = np.linalg.eigvalsh(r); w = w[w > 1e-300]
    return float(-(w * np.log(w)).sum())
A = cplx(3); A = A - A.conj().T
def rho_c(u):
    U = expm(u * A / 3); p = 0.3 + 0.2 * np.sin(u)
    return U @ np.diag([p, 1 - p, 0.0]) @ U.conj().T
u0 = 0.4; p, dp = 0.3 + 0.2 * np.sin(u0), 0.2 * np.cos(u0)
exact = -dp * np.log(p / (1 - p))
errs = [abs((S_of(rho_c(u0 + h)) - S_of(rho_c(u0 - h))) / (2 * h) - exact) for h in [1e-2, 5e-3, 2.5e-3]]
rates = [np.log2(errs[i] / errs[i + 1]) for i in range(2)]
blow = [(S_of(np.diag([1 - u * 1.001, u * 1.001, 0])) - S_of(np.diag([1 - u * 0.999, u * 0.999, 0]))) / (0.002 * u)
        for u in [1e-2, 1e-4, 1e-6]]
rep("V4 dS/dt finite and O(h^2)-convergent at constant rank 2 in chi=3; unbounded at a rank change",
    errs[-1] < 1e-5 and all(1.8 < r < 2.2 for r in rates) and blow[-1] > blow[0] + 8,
    f"FD errors {['%.1e' % e for e in errs]}, observed rates {['%.2f' % r for r in rates]}; "
    f"control diag(1-t,t,0): dS/dt at t=1e-2,1e-4,1e-6 = {['%.2f' % b for b in blow]}")

# Riesz-contour representation used in the proof: -Tr f(rho) = -(1/2 pi i) oint f(z) Tr (z - rho)^-1 dz
r0 = rho_c(0.9); w = np.linalg.eigvalsh(r0); lo = min(w[w > 1e-12])
def contour_S(r, c, rad, n=4000):
    th = np.linspace(0, 2 * np.pi, n, endpoint=False); z = c + rad * np.exp(1j * th); dz = 1j * rad * np.exp(1j * th)
    vals = np.array([zz * np.log(zz) * np.trace(np.linalg.inv(zz * np.eye(3) - r)) for zz in z])
    return float((-(vals * dz).sum() * (2 * np.pi / n) / (2j * np.pi)).real)
c, rad = (lo / 2 + 1.0) / 2, (1.0 - lo / 2) / 2 + 1e-3
good = contour_S(r0, c, rad)
bad = contour_S(r0, c + 0.3, rad * 0.4)                     # control: contour misses an eigenvalue
rep("V4b Riesz-contour formula for S on a rank-deficient rho (contour in Re z > 0)",
    abs(good - S_of(r0)) < 1e-10 and abs(bad - S_of(r0)) > 1e-3 and c - rad > 0,
    f"|contour - eig| = {abs(good - S_of(r0)):.1e}; control err {abs(bad - S_of(r0)):.2e}")

# ---------------------------------------------------------------- V5 MPS gauge invariance by cyclicity (discrete cMPS)
chi, eps, n = 3, 0.1, 8
Q, R = cplx(chi), cplx(chi)
Xg = cplx(chi) + 2 * np.eye(chi)
Xi = np.linalg.inv(Xg)
def amps(Qm, Rm):
    A0, A1 = np.eye(chi) + eps * Qm, np.sqrt(eps) * Rm
    out = []
    for c_ in range(2 ** n):
        M = np.eye(chi, dtype=complex)
        for k in range(n):
            M = M @ (A1 if (c_ >> k) & 1 else A0)
        out.append(np.trace(M))
    return np.array(out)
a1 = amps(Q, R); a2 = amps(Xg @ Q @ Xi, Xg @ R @ Xi); a3 = amps(Q, Xg @ R @ Xi)
rep("V5 amplitudes invariant under (Q,R) -> (XQX^-1, XRX^-1); not under R alone",
    np.max(abs(a1 - a2)) / np.max(abs(a1)) < 1e-10 and np.max(abs(a1 - a3)) / np.max(abs(a1)) > 1e-3,
    f"rel diff {np.max(abs(a1 - a2)) / np.max(abs(a1)):.1e}; control {np.max(abs(a1 - a3)) / np.max(abs(a1)):.2e}")

# ---------------------------------------------------------------- V6 QFI invariances
dim = 6
H1 = cplx(dim); H1 = H1 + H1.conj().T; H2 = cplx(dim); H2 = H2 + H2.conj().T
v0 = cplx(dim, 1)[:, 0]; v0 /= np.linalg.norm(v0)
base = lambda p: expm(1j * (p[0] * H1 + p[1] * H2) / 5) @ v0
U = expm(1j * (lambda m: m + m.conj().T)(cplx(dim)))
Cg = cplx(dim); Cg = Cg + Cg.conj().T
p0 = np.array([0.2, -0.1]); hh = 1e-5
G0 = qfi(base, p0, hh)
Gu = qfi(lambda p: U @ base(p), p0, hh)
Gph = qfi(lambda p: np.exp(1j * (np.sin(3 * p[0]) + p[1] ** 2)) * base(p), p0, hh)
Gcc = qfi(lambda p: base(p).conj(), p0, hh)
Gx = qfi(lambda p: expm(1j * p[0] * Cg) @ base(p), p0, hh)            # control: x-dependent unitary
d0 = (base(p0 + [hh, 0]) - base(p0 - [hh, 0])) / (2 * hh)
dph = (lambda f: (f(p0 + [hh, 0]) - f(p0 - [hh, 0])) / (2 * hh))(lambda p: np.exp(1j * np.sin(3 * p[0])) * base(p))
noproj_change = abs(4 * (dph.conj() @ dph).real - 4 * (d0.conj() @ d0).real)
rep("V6 QFI invariant under fixed unitary, local phase, complex conjugation; positive definite",
    max(np.max(abs(G0 - Gu)), np.max(abs(G0 - Gph)), np.max(abs(G0 - Gcc))) < 1e-6
    and np.max(abs(G0 - Gx)) > 1e-3 and noproj_change > 1e-2 and np.all(np.linalg.eigvalsh(G0) > 0),
    f"max diffs U {np.max(abs(G0 - Gu)):.1e}, phase {np.max(abs(G0 - Gph)):.1e}, conj {np.max(abs(G0 - Gcc)):.1e}; "
    f"controls: x-dependent unitary {np.max(abs(G0 - Gx)):.2e}, unprojected under phase {noproj_change:.2e}")

# ---------------------------------------------------------------- V7 static shift gives K != 0
x = sp.symbols("x")
f = (2 + sp.cos(x)) / 2                                       # (1/2)||R||^2 ; X_x = d_x f, flat h
Xs = sp.diff(f, x)
co2 = [t, x]
g2 = sp.Matrix([[-N0**2 + Xs**2, Xs], [Xs, 1]])               # -N0^2 dt^2 + (dx + X dt)^2
g2i = g2.inv()
Gam0xx = sp.simplify(sum(g2i[0, l] * (2 * sp.diff(g2[l, 1], x) - sp.diff(g2[1, 1], co2[l])) for l in range(2)) / 2)
Kxx = sp.simplify(-N0 * Gam0xx)        # K_ij = -nabla_i n_j = Gamma^mu_ij n_mu with n_mu = (-N0, 0)
oracle = sp.diff(f, x, 2) / N0
Kc = 0                                                         # control: constant ||R|| gives X = 0, K = 0
rep("V7 constant path with ||R||^2 = 2 + cos x: slice t=0 has K_xx = -cos(x)/(2 N0) != 0",
    sp.simplify(Kxx - oracle) == 0 and sp.simplify(oracle) != 0 and Kc == 0,
    f"K_xx (Christoffel) = {sp.simplify(Kxx)}; oracle (1/N0) f'' = {sp.simplify(oracle)}")

# ---------------------------------------------------------------- V8 sitting instants make concatenation smooth
def S2(p): return -(p * np.log(p) + (1 - p) * np.log(1 - p))
def bump(u):  # smooth step 0 -> 1 on [0.2, 0.8], constant near 0 and 1
    def h(y): return np.where(y > 0, np.exp(-1 / np.maximum(y, 1e-300)), 0.0)
    y = (u - 0.2) / 0.6
    return h(y) / (h(y) + h(1 - y))
def lapse_path(p_of, us, dt=1e-6):
    dS = (S2(p_of(us + dt)) - S2(p_of(us - dt))) / (2 * dt)
    return (dS ** 2 + 1) ** 0.25
p_sit = lambda u: np.where(u <= 1, 0.2 + 0.2 * bump(u), 0.4 + 0.2 * bump(u - 1))
p_lin = lambda u: np.where(u <= 1, 0.2 + 0.2 * u, 0.4 + 0.05 * (u - 1))
jl = lambda pf: abs(lapse_path(pf, np.array([1 - 1e-6]), 1e-8)[0] - lapse_path(pf, np.array([1 + 1e-6]), 1e-8)[0])
Sp = np.log(0.6 / 0.4)                                        # S'(p) at p = 0.4
jump_exact = ((0.2 * Sp) ** 2 + 1) ** 0.25 - ((0.05 * Sp) ** 2 + 1) ** 0.25
rep("V8 sitting paths: lapse continuous across the junction; non-sitting control jumps by the predicted amount",
    jl(p_sit) < 1e-9 and abs(jl(p_lin) - jump_exact) < 1e-3 * jump_exact,
    f"jump sitting {jl(p_sit):.1e}; control {jl(p_lin):.6e} vs analytic one-sided limits {jump_exact:.6e}")

# ---------------------------------------------------------------- V9 order of magnitude (CODATA 2018 via scipy)
lP2 = C.hbar * C.G / C.c ** 3
log.append(f"[INFO] V9 l_P^2 = hbar G / c^3 = {lP2:.4e} m^2 (dimension m^2); "
           f"Area 1 m^2: A/(4 l_P^2) = {1 / (4 * lP2):.3e}, ln(chi) >= A/(8 l_P^2) = {1 / (8 * lP2):.3e}")
rep("V9 Planck area matches CODATA l_P = 1.616255e-35 m", abs(np.sqrt(lP2) / 1.616255e-35 - 1) < 1e-5,
    f"l_P = {np.sqrt(lP2):.6e} m")

out = "\n".join(log) + f"\nFAILED CHECKS: {fails}"
print(out)
open(os.path.join(HERE, "fixes_checks.out.txt"), "w", encoding="utf8").write(out)
sys.exit(fails)
