"""Independent numerical / symbolic checks for the blind layer-1 audit of
'A Functorial Bridge from Continuous Tensor Manifolds to 4D Spacetime Cobordisms'.
Each check: oracle + negative control (mutation must fail); refinement where relevant.
Fixed seed. Exit code = number of failed checks (a 'counterexample found' is a PASS of the check)."""
import sys, os
import numpy as np
import sympy as sp
from scipy.integrate import quad

rng = np.random.default_rng(20261006)
HERE = os.path.dirname(os.path.abspath(__file__))
log, fails = [], 0
def rep(name, ok, msg):
    global fails
    log.append(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}")
    if not ok: fails += 1

def cplx(n, m=None):
    m = n if m is None else m
    return rng.normal(size=(n, m)) + 1j * rng.normal(size=(n, m))

# ---------------------------------------------------------------- C1 shift formula
# Claim used implicitly: the shift N^i = h^ij Re Tr(rho[Q,d_jQ] + R^dag d_jR).
# Check (a) Re Tr(rho[Q,dQ]) = 0 when Q in u(chi) (anti-Hermitian), rho Hermitian;
#       (b) Re Tr(R^dag dR) = (1/2) d ||R||_HS^2 (finite-difference oracle).
chi = 4
vals, ctrl = [], []
for _ in range(200):
    A = cplx(chi); Q = A - A.conj().T          # anti-Hermitian
    B = cplx(chi); dQ = B - B.conj().T
    P = cplx(chi); rho = P @ P.conj().T; rho /= np.trace(rho).real
    vals.append(abs(np.trace(rho @ (Q @ dQ - dQ @ Q)).real))
    Qg, dQg = cplx(chi), cplx(chi)              # generic (mutation: not anti-Hermitian)
    ctrl.append(abs(np.trace(rho @ (Qg @ dQg - dQg @ Qg)).real))
rep("C1a Re Tr(rho[Q,dQ])=0 for Q in u(chi)", max(vals) < 1e-12 and min(ctrl) > 1e-6,
    f"max over 200 samples {max(vals):.2e}; negative control (generic Q) min {min(ctrl):.2e}")
R0, R1 = cplx(chi), cplx(chi)
Rf = lambda x: R0 + x * R1 + x**2 * R0.conj()
x0 = 0.3
errs = []
for hstep in [1e-2, 1e-3, 1e-4]:
    dR = (Rf(x0 + hstep) - Rf(x0 - hstep)) / (2 * hstep)
    lhs = np.trace(Rf(x0).conj().T @ dR).real
    nrm = lambda x: np.linalg.norm(Rf(x)) ** 2
    rhs = 0.5 * (nrm(x0 + hstep) - nrm(x0 - hstep)) / (2 * hstep)
    errs.append(abs(lhs - rhs))
rep("C1b Re Tr(R^dag dR) = (1/2) d||R||^2", errs[-1] < 1e-6, f"errors over h-refinement {['%.1e'%e for e in errs]}")
# consequence: the static (identity) flow has shift N_i = (1/2) d_i ||R||^2, generally non-zero,
# so K_ij = (1/2N) L_N h_ij = (1/2N)(d_i N_j + d_j N_i) != 0 for flat h with ||R||^2 = 2 + cos x.
x = sp.symbols("x")
f = 2 + sp.cos(x)                    # ||R(x)||^2 along one coordinate
Nx = sp.Rational(1, 2) * sp.diff(f, x)
Kxx = sp.simplify(2 * sp.diff(Nx, x) / 2)  # N = 1
rep("C1c identity flow gives K_xx != 0 (F(id) is not the static cylinder)", sp.simplify(Kxx) != 0,
    f"K_xx = {Kxx}  (control: ||R|| constant gives K_xx = {sp.diff(sp.Rational(1,2)*sp.diff(sp.Integer(3),x),x)})")

# ---------------------------------------------------------------- C2 lapse smoothness
# rho(t) = diag(1-t, t): smooth, PSD, trace 1.  dS/dt = log((1-t)/t) -> infinity as t->0+.
def S(p): return -(p * np.log(p) + (1 - p) * np.log(1 - p))
def lapse(t, sig=1.0, kap=1.0, dt=None):
    dS = np.log((1 - t) / t)              # analytic derivative
    return ((dS**2 + sig**2) / kap**2) ** 0.25
ts = [1e-2, 1e-4, 1e-6, 1e-8]
Ns = [lapse(t) for t in ts]
# oracle for dS/dt: central finite difference of the entropy itself
fd = [(S(t * 1.001) - S(t * 0.999)) / (0.002 * t) for t in ts]
an = [np.log((1 - t) / t) for t in ts]
rel = max(abs(a - b) / abs(a) for a, b in zip(fd, an))
# negative control: eigenvalues bounded away from 0, rho = diag(0.75 - t/2, 0.25 + t/2)
Nctrl = [((np.log((0.75 - t/2) / (0.25 + t/2)))**2 + 1) ** 0.25 for t in ts]
rep("C2 lapse N unbounded (not smooth) at a rank change of rho", Ns[-1] > Ns[0] * 1.3 and rel < 1e-4 and max(Nctrl) <= (np.log(3)**2 + 1) ** 0.25 + 1e-12,
    f"N(t) for t={ts}: {['%.3f'%v for v in Ns]} (grows like |log t|^(1/2)); FD-vs-analytic rel err {rel:.1e}; control N max {max(Nctrl):.3f}")

# ---------------------------------------------------------------- C3 reparametrization (non-)invariance
# Image metric of a flow on T^3 (unit coordinate volume): -N^2 dt^2 + a(t)^2 dx^2, shift 0.
# Invariant under isometries rel boundary: 4-volume V = int N a^3 dt.
# Flow data: a(s) and entropy S(s) as functions of the flow parameter s; representative t -> s = alpha(t).
a_of = lambda s: 1 + 0.5 * np.sin(np.pi * s) ** 2
S_of = lambda s: 0.3 * np.sin(np.pi * s)          # entropy along the flow
dS_of = lambda s: 0.3 * np.pi * np.cos(np.pi * s)
alphas = {"identity": (lambda t: t, lambda t: 1.0),
          "t^2": (lambda t: t**2, lambda t: 2 * t),
          "smoothstep": (lambda t: 3*t**2 - 2*t**3, lambda t: 6*t - 6*t**2)}
def vol(alpha, dalpha, covariant=False):
    def integrand(t):
        s = alpha(t)
        if covariant:   # mutation that SHOULD be invariant: N -> alpha' * N0(s)
            N = dalpha(t) * ((dS_of(s)**2 + 1.0) ** 0.25)
        else:           # paper's lapse: N = ((d_t S)^2 + sigma^2)^(1/4), d_t S = alpha' S'(s)
            N = ((dalpha(t) * dS_of(s))**2 + 1.0) ** 0.25
        return N * a_of(s) ** 3
    return quad(integrand, 0, 1, epsabs=1e-13, epsrel=1e-13, limit=200)[0]
Vp = {k: vol(*v) for k, v in alphas.items()}
Vc = {k: vol(*v, covariant=True) for k, v in alphas.items()}
spread_p = max(Vp.values()) - min(Vp.values())
spread_c = max(Vc.values()) - min(Vc.values())
rep("C3 F not well defined on reparametrization classes", spread_p > 1e-2 and spread_c < 1e-9,
    f"paper lapse 4-volumes {{{', '.join(f'{k}: {v:.6f}' for k,v in Vp.items())}}}; covariant-lapse control spread {spread_c:.1e}")

# ---------------------------------------------------------------- C4 Lemma 5.1 counterexample (Einstein eqs)
t, Nn, Lam = sp.symbols("t N Lambda", positive=True)
X = sp.symbols("x1 x2 x3")
a = sp.Function("a")(t)
coords = [t, *X]
def einstein(g):
    gi = g.inv()
    n = 4
    Gam = [[[sum(gi[i, l] * (sp.diff(g[l, j], coords[k]) + sp.diff(g[l, k], coords[j]) - sp.diff(g[j, k], coords[l]))
                 for l in range(n)) / 2 for k in range(n)] for j in range(n)] for i in range(n)]
    Ric = sp.zeros(n)
    for j in range(n):
        for k in range(n):
            Ric[j, k] = sp.simplify(sum(sp.diff(Gam[i][j][k], coords[i]) - sp.diff(Gam[i][j][i], coords[k])
                         + sum(Gam[i][i][p] * Gam[p][j][k] - Gam[i][k][p] * Gam[p][j][i] for p in range(n))
                         for i in range(n)))
    Rs = sp.simplify(sum(gi[i, j] * Ric[i, j] for i in range(n) for j in range(n)))
    return sp.simplify(Ric - Rs * g / 2)
g = sp.diag(-Nn**2, a**2, a**2, a**2)
G = einstein(g)
Gtt = sp.simplify(G[0, 0])
oracle = 3 * sp.diff(a, t)**2 / a**2            # textbook Friedmann G_tt for flat FRW with lapse N
rep("C4a sympy Einstein tensor matches Friedmann oracle", sp.simplify(Gtt - oracle) == 0, f"G_tt = {Gtt}")
# Image data: Psi = const matrix, V = 0  =>  T_mu nu = 0.  Need G_tt + Lam g_tt = 0.
a_ce = 1 + 3 * t**2 - 2 * t**3     # monotone 1 -> 2 (admissible as a gradient-flow class), a'(0)=a'(1)=0
res = sp.simplify((Gtt + Lam * g[0, 0]).subs(a, a_ce).doit())
at0 = sp.simplify(res.subs(t, 0)); athalf = sp.simplify(res.subs(t, sp.Rational(1, 2)))
at1 = sp.simplify(res.subs(t, 1))
# endpoints on-shell (K=0, flat) force Lam = 0 from G_tt(0) = 0 -> then interior residual must vanish
rep("C4b Lemma 5.1 fails: endpoints on-shell, interior violates G_tt + Lam g_tt = 8 pi G T_tt = 0",
    sp.simplify(at0.subs(Lam, 0)) == 0 and sp.simplify(at1.subs(Lam, 0)) == 0 and sp.simplify(athalf.subs(Lam, 0)) != 0,
    f"residual at t=0: {at0}; at t=1 {at1}; at t=1/2 with Lam=0: {sp.nsimplify(athalf.subs(Lam,0))} = {float(athalf.subs({Lam:0, Nn:1})):.4f} (N=1)")
# negative control: de Sitter a = e^{H t}, Lam = 3H^2, N=1 solves vacuum + Lam
H = sp.symbols("H", positive=True)
ctrl = sp.simplify((Gtt + Lam * g[0, 0]).subs(a, sp.exp(H * t)).doit().subs({Lam: 3 * H**2, Nn: 1}))
rep("C4c control: de Sitter satisfies the same test", ctrl == 0, f"residual {ctrl}")

# ---------------------------------------------------------------- C5 NEC algebra (Thm 5.6, algebraic part)
def lorentz_metric():
    N = 0.5 + rng.random(); sh = rng.normal(size=3); P = rng.normal(size=(3, 3)); h = P @ P.T + 0.5 * np.eye(3)
    g = np.zeros((4, 4)); g[0, 0] = -N**2 + sh @ h @ sh; g[0, 1:] = g[1:, 0] = h @ sh; g[1:, 1:] = h
    return g
def null_vec(g):
    while True:
        v = rng.normal(size=3); # solve g(k,k)=0 for k0 with k=(k0,v)
        A, B, C = g[0, 0], 2 * g[0, 1:] @ v, v @ g[1:, 1:] @ v
        if B * B - 4 * A * C >= 0 and abs(A) > 1e-3: break
    k0 = (-B - np.sqrt(B * B - 4 * A * C)) / (2 * A)
    return np.array([k0, *v])
worst, gap, ctrl_bad = np.inf, 0.0, 0
for _ in range(500):
    g = lorentz_metric(); gi = np.linalg.inv(g); k = null_vec(g)
    assert abs(k @ g @ k) < 1e-8 * (k @ k) and np.all(np.isfinite(k))
    assert np.sum(np.linalg.eigvalsh(g) < 0) == 1
    D = [cplx(3) for _ in range(4)]                       # nabla_mu Psi
    Vh = cplx(3); Vh = Vh + Vh.conj().T                   # Hermitian potential value
    X = np.array([[np.trace(D[m].conj().T @ D[n]).real for n in range(4)] for m in range(4)])
    T = X - 0.5 * g * (np.sum(gi * X) + np.trace(Vh).real)
    Tkk = k @ T @ k
    kD = sum(k[m] * D[m] for m in range(4))
    hs = np.linalg.norm(kD) ** 2
    gap = max(gap, abs(Tkk - hs) / max(1, hs)); worst = min(worst, Tkk)
    # negative control: timelike vector u (g(u,u)<0) => T_uu != ||u.D||^2 in general
    u = np.linalg.solve(g, np.array([-1.0, 0, 0, 0]))
    uD = sum(u[m] * D[m] for m in range(4))
    if abs(u @ T @ u - np.linalg.norm(uD) ** 2) > 1e-6: ctrl_bad += 1
rep("C5 T_kk = ||k.nabla Psi||_HS^2 >= 0 for null k (algebraic NEC)", gap < 1e-9 and worst > -1e-9 and ctrl_bad > 450,
    f"max rel gap {gap:.1e}; min T_kk {worst:.3e}; control (timelike) mismatches {ctrl_bad}/500")

# ---------------------------------------------------------------- C6 sign of j_i (Def 2.1 vs Sec 4.2)
# With pi = n^mu d_mu Psi and n^mu = (1/N, -N^i/N), check -n^mu h_i^nu T_mu nu vs +Re Tr(pi^dag d_i psi).
errs_plus, errs_minus = [], []
for _ in range(200):
    N = 0.5 + rng.random(); sh = rng.normal(size=3); P = rng.normal(size=(3, 3)); h = P @ P.T + 0.5 * np.eye(3)
    g = np.zeros((4, 4)); g[0, 0] = -N**2 + sh @ h @ sh; g[0, 1:] = g[1:, 0] = h @ sh; g[1:, 1:] = h
    gi = np.linalg.inv(g)
    D = [cplx(3) for _ in range(4)]
    X = np.array([[np.trace(D[m].conj().T @ D[n]).real for n in range(4)] for m in range(4)])
    T = X - 0.5 * g * np.sum(gi * X)
    n_up = np.array([1 / N, *(-sh / N)])
    proj = np.eye(4) + np.outer(n_up, n_up @ g)            # h^nu_mu = delta + n^nu n_mu ; use spatial index i -> columns 1..3
    pi = sum(n_up[m] * D[m] for m in range(4))
    for i in range(3):
        hi = proj[:, 1 + i]                                 # h^nu_i (vector index nu)
        j_geom = -(n_up @ T @ hi)
        j_paper = np.trace(pi.conj().T @ D[1 + i]).real
        errs_plus.append(abs(j_geom - j_paper)); errs_minus.append(abs(j_geom + j_paper))
rep("C6 j_i sign: -n h T equals -Re Tr(pi^dag d_i psi), opposite to Eq. (2.3)",
    max(errs_minus) < 1e-9 and min(errs_plus) > 1e-6,
    f"max|j_geom + j_paper| = {max(errs_minus):.1e}; min|j_geom - j_paper| = {min(errs_plus):.1e}")

# rho_matt check: n n T = (1/2)(|pi|^2 + h^ij Re Tr d_i psi^dag d_j psi) (V=0)
errs = []
for _ in range(100):
    N = 0.5 + rng.random(); sh = rng.normal(size=3); P = rng.normal(size=(3, 3)); h = P @ P.T + 0.5 * np.eye(3)
    g = np.zeros((4, 4)); g[0, 0] = -N**2 + sh @ h @ sh; g[0, 1:] = g[1:, 0] = h @ sh; g[1:, 1:] = h
    gi = np.linalg.inv(g); hi = np.linalg.inv(h)
    D = [cplx(3) for _ in range(4)]
    X = np.array([[np.trace(D[m].conj().T @ D[n]).real for n in range(4)] for m in range(4)])
    T = X - 0.5 * g * np.sum(gi * X)
    n_up = np.array([1 / N, *(-sh / N)]); pi = sum(n_up[m] * D[m] for m in range(4))
    rho_g = n_up @ T @ n_up
    rho_p = 0.5 * (np.linalg.norm(pi)**2 + sum(hi[i, j] * np.trace(D[1+i].conj().T @ D[1+j]).real for i in range(3) for j in range(3)))
    errs.append(abs(rho_g - rho_p))
rep("C6b rho_matt = n n T matches Eq. (2.2) (V=0)", max(errs) < 1e-9, f"max err {max(errs):.1e}")

# ---------------------------------------------------------------- C7 QFI invariance under conjugation
def qfi(states, dx):
    psi = states[1]; dpsi = [(states[2 + 2*i] - states[3 + 2*i]) / (2 * dx) for i in range(2)]
    Pp = np.eye(len(psi)) - np.outer(psi, psi.conj())
    return np.array([[4 * (dpsi[i].conj() @ Pp @ dpsi[j]).real for j in range(2)] for i in range(2)])
M1 = cplx(6); M2 = cplx(6); v0 = cplx(6, 1)[:, 0]
def state(x, y):
    w = np.exp(1j * (x * (M1 + M1.conj().T) + y * (M2 + M2.conj().T)) / 5) @ v0 if False else \
        __import__("scipy.linalg", fromlist=["expm"]).expm(1j * (x * (M1 + M1.conj().T) + y * (M2 + M2.conj().T)) / 5) @ v0
    return w / np.linalg.norm(w)
dx = 1e-5; x0, y0 = 0.2, -0.1
S1 = [None, state(x0, y0), state(x0+dx, y0), state(x0-dx, y0), state(x0, y0+dx), state(x0, y0-dx)]
S2 = [None] + [s.conj() for s in S1[1:]]
G1, G2 = qfi(S1, dx), qfi(S2, dx)
# negative control: dropping the projector changes g (Berry term)
psi = S1[1]; d0 = (S1[2] - S1[3]) / (2 * dx)
noproj = 4 * (d0.conj() @ d0).real
rep("C7 g_QFI(T*) = g_QFI(T); projector matters", np.max(abs(G1 - G2)) < 1e-6 and abs(noproj - G1[0, 0]) > 1e-4 and np.all(np.linalg.eigvalsh(G1) > 0),
    f"max diff {np.max(abs(G1-G2)):.1e}; eig {np.linalg.eigvalsh(G1)}; control unprojected g_xx {noproj:.4f} vs {G1[0,0]:.4f}")

# ---------------------------------------------------------------- C8 holographic scaling order of magnitude
lP2 = 1.616255e-35 ** 2   # CODATA 2018 Planck length^2 [m^2]
for A in [1e-30, 1.0, 4 * np.pi * (6.371e6) ** 2]:
    log_chi = A / (4 * lP2)
    log.append(f"[INFO] C8 Area {A:.2e} m^2 -> log chi ~ {log_chi:.2e} (chi ~ 10^{log_chi/np.log(10):.2e})")

s = "\n".join(log) + f"\nFAILED CHECKS: {fails}"
print(s)
open(os.path.join(HERE, "math_checks.out.txt"), "w", encoding="utf8").write(s)
sys.exit(fails)
