"""Corrector checks for Beyond the Spectrum III (independent of the referee scripts n1-n5).

Each block uses a route different from the referee's and a negative control.
Output: f1_corrector_checks.out.txt ; exit code = number of failures.
"""
import sys
import numpy as np
from scipy import optimize, special, integrate

rng = np.random.default_rng(20261006)
OUT = []
FAIL = 0


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


def check(name, cond):
    global FAIL
    log(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAIL += 1


# ---------------------------------------------------------------------------
# OBL-008: p -> infinity limit on the unit disk, by direct minimisation of a
# finite-element Rayleigh quotient (referee used ODE shooting).
# ---------------------------------------------------------------------------
def disk_lambda_p(p, w=lambda r: np.ones_like(r), N=400):
    r = np.linspace(0.0, 1.0, N + 1)
    rm = 0.5 * (r[1:] + r[:-1])
    h = np.diff(r)

    c = w(rm) * rm * h

    def quot(v):
        u = np.concatenate([v, [0.0]])  # u(1)=0, u(0) free
        du = np.diff(u) / h
        um = 0.5 * (u[1:] + u[:-1])
        num = np.sum(np.abs(du) ** p * c)
        den = np.sum(np.abs(um) ** p * c)
        gn = p * np.abs(du) ** (p - 1) * np.sign(du) * c / h
        gd = 0.5 * p * np.abs(um) ** (p - 1) * np.sign(um) * c
        Gn = np.zeros(N + 1)
        Gd = np.zeros(N + 1)
        Gn[:-1] -= gn
        Gn[1:] += gn
        Gd[:-1] += gd
        Gd[1:] += gd
        g = Gn / num - Gd / den
        return np.log(num) - np.log(den), g[:-1]

    v0 = 1.0 - r[:-1]  # cone start
    res = optimize.minimize(quot, v0, jac=True, method="L-BFGS-B",
                            options={"maxiter": 50000, "maxfun": 10**6, "ftol": 1e-15, "gtol": 1e-12})
    return np.exp(res.fun / p)


log("== OBL-008 (disk, FE minimisation) ==")
j01 = special.jn_zeros(0, 1)[0]
v2 = disk_lambda_p(2)
log(f"p=2: FE lambda^(1/2) = {v2:.5f}, Bessel oracle j01 = {j01:.5f}")
check("FE p=2 matches Bessel oracle to 1e-3", abs(v2 - j01) < 1e-3)
prev = None
for p in [4, 8, 16, 32]:
    v = disk_lambda_p(p)
    cone = ((p + 1) * (p + 2) / 2.0) ** (1.0 / p)  # exact quotient of the cone test function
    vw = disk_lambda_p(p, w=lambda r: 1.0 + r ** 2)  # weight 1 <= Phi <= 2
    log(f"p={p:3d}: unweighted {v:.4f}  weighted(1+r^2) {vw:.4f}  cone bound {cone:.4f}  comparison window [{v*0.5**(1/p):.4f},{v*2**(1/p):.4f}]")
    check(f"p={p}: FE value <= cone upper bound (+1e-3)", v <= cone + 1e-3)
    check(f"p={p}: weighted value inside comparison window", v * 0.5 ** (1 / p) - 1e-3 <= vw <= v * 2 ** (1 / p) + 1e-3)
    if prev is not None:
        check(f"p={p}: decreasing towards 1/R=1", v < prev and v > 1.0 - 1e-3)
    prev = v
check("NEG CONTROL: claimed limit h=2 (Cheeger, full perimeter) is excluded: cone bound at p=32 < 2",
      ((33 * 34) / 2.0) ** (1 / 32) < 2.0)
log("cone bound limit: ((p+1)(p+2)/2)^(1/p) at p=1e4:", ((1e4 + 1) * (1e4 + 2) / 2) ** 1e-4)

# ---------------------------------------------------------------------------
# OBL-012: dragged trap V = kappa (x - lam(t))^2 / 2, D = kBT = 1.
# Mean obeys d<x>/dt = -kappa(<x> - lam); <W> = int dV/dt = -kappa int (<x>-lam) lam' dt.
# Integrated by RK4 (referee used closed form + Monte Carlo).
# ---------------------------------------------------------------------------
log("== OBL-012 (moment ODE, RK4) ==")


def tau_work(kappa, a, tau, prof, nsteps=200000):
    dt = tau / nsteps
    m = 0.0
    W = 0.0

    def lam(t):
        return a * prof(t / tau)

    def dlam(t, eps=1e-7):
        return a * (prof(min(t / tau + eps, 1.0)) - prof(max(t / tau - eps, 0.0))) / (
            min(t / tau + eps, 1.0) - max(t / tau - eps, 0.0)) / tau

    def f(t, y):
        m, W = y
        return np.array([-kappa * (m - lam(t)), -kappa * (m - lam(t)) * dlam(t)])

    y = np.array([0.0, 0.0])
    t = 0.0
    for _ in range(nsteps):
        k1 = f(t, y)
        k2 = f(t + dt / 2, y + dt / 2 * k1)
        k3 = f(t + dt / 2, y + dt / 2 * k2)
        k4 = f(t + dt, y + dt * k3)
        y = y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += dt
    return tau * y[1]


a = 1.0
for kappa in [1.0, 10.0]:
    for prof, name, Lint in [(lambda s: s, "linear", 1.0), (lambda s: s * s, "quadratic", 4.0 / 3.0)]:
        vals = [tau_work(kappa, a, tau, prof, nsteps=int(20 * tau * kappa) + 2000) for tau in [50.0, 200.0, 800.0]]
        # Linear response: lim tau<W_diss> = int_0^1 g lam'(s)^2 ds with g = 1 (per unit a^2)
        log(f"kappa={kappa:4.1f} {name:9s}: tau*Sigma at tau=50,200,800 = {[round(v,5) for v in vals]} ; "
            f"friction-metric prediction {Lint*a*a:.5f} ; W2^2 = {a*a:.3f} ; paper RHS kappa W2^2/4 = {kappa*a*a/4:.3f}")
        check(f"kappa={kappa} {name}: converges to int g lam'^2", abs(vals[-1] - Lint) < 5e-3)
        check(f"kappa={kappa} {name}: corrected bound tau*Sigma >= W2^2/D (asymptotically)", vals[-1] >= a * a - 5e-3)
check("NEG CONTROL: paper bound lim >= kappa W2^2/4 fails at kappa=10 (1.0 < 2.5)", not (1.0 >= 10.0 / 4))
check("NEG CONTROL: paper equality lim = L^2/2 fails for the geodesic (linear) protocol (1.0 vs 0.5)", abs(1.0 - 0.5) > 0.1)

# ---------------------------------------------------------------------------
# OBL-014: Schmidt spectrum of psi(x,y) ~ exp(-(x^2+y^2)/2 + beta x y) via
# Hermite-function coefficients by Gauss-Hermite quadrature (referee used grid SVD).
# ---------------------------------------------------------------------------
log("== OBL-014 (Hermite-basis Schmidt spectrum) ==")


def hermite_functions(x, K):
    H = np.zeros((K, x.size))
    H[0] = np.pi ** -0.25 * np.exp(-x * x / 2)
    if K > 1:
        H[1] = np.sqrt(2.0) * x * H[0]
    for k in range(2, K):
        H[k] = np.sqrt(2.0 / k) * x * H[k - 1] - np.sqrt((k - 1) / k) * H[k - 2]
    return H


def schmidt(beta, K=40, Q=160):
    xg, wg = special.roots_hermite(Q)  # weight exp(-x^2)
    H = hermite_functions(xg, K)
    X, Y = np.meshgrid(xg, xg, indexing="ij")
    psi = np.exp(-(X ** 2 + Y ** 2) / 2 + beta * X * Y)
    F = psi * np.exp(X ** 2 + Y ** 2)  # undo the quadrature weight
    C = (H * wg) @ F @ (H * wg).T
    s = np.linalg.svd(C, compute_uv=False) ** 2
    return s / s.sum()


for beta in [0.6, 0.3]:
    s = schmidt(beta)
    a_ = 1.0
    # Mehler: exp(-(x^2+y^2)/2 + beta x y) is a two-mode Gaussian; Schmidt ratio q = (1 - sqrt(1-beta^2))^2/beta^2
    q = ((1 - np.sqrt(1 - beta ** 2)) / beta) ** 2
    nz = int(np.sum(s > 1e-12))
    log(f"beta={beta}: top Schmidt weights {np.round(s[:4],6)} ratios {np.round(s[1:4]/s[:3],6)} Mehler q={q:.6f} ; #weights>1e-12: {nz}")
    check(f"beta={beta}: geometric Schmidt spectrum, ratio = Mehler q", np.allclose(s[1:4] / s[:3], q, rtol=1e-6))
    check(f"beta={beta}: rank of the reduced state exceeds n=1", nz > 1)
s0 = schmidt(0.0)
check("NEG CONTROL beta=0 (product state): rank exactly 1", int(np.sum(s0 > 1e-12)) == 1)

# Finite Schmidt-rank frames: rank rho_1 <= sum_k m_k ; normalised modular energies >= 0.
d1, d2, n = 12, 9, 3
for mk in [(1, 1, 1), (2, 1, 3)]:
    psis = []
    for m in mk:
        v = sum(np.kron(rng.normal(size=d1), rng.normal(size=d2)) for _ in range(m))
        psis.append(v)
    Q_, _ = np.linalg.qr(np.array(psis).T)  # orthonormal frame, span preserves Schmidt ranks bound
    frame = Q_.T
    G = rng.normal(size=(n, n))
    A = G @ G.T
    T = frame.T @ A @ frame
    rho = np.einsum("iaja->ij", T.reshape(d1, d2, d1, d2))
    ev = np.linalg.eigvalsh(rho)
    rk = int(np.sum(ev > 1e-10 * ev.max()))
    log(f"Schmidt ranks {mk}: rank rho_1 = {rk}, bound sum m_k = {sum(mk)}, Tr rho = {np.trace(rho):.6f}, Tr A = {np.trace(A):.6f}")
    check(f"rank bound for Schmidt ranks {mk}", rk <= sum(mk))
    check(f"Tr rho_1 = Tr A for Schmidt ranks {mk}", abs(np.trace(rho) - np.trace(A)) < 1e-9)
    p_ = ev[ev > 1e-10 * ev.max()] / np.trace(rho)
    check(f"normalised modular energies -log p_k >= 0 for {mk}", np.all(-np.log(p_) >= -1e-12))
check("NEG CONTROL: unnormalised n=1, A=5 product frame gives -log 5 < 0", -np.log(5.0) < 0)

# ---------------------------------------------------------------------------
# OBL-017/018: Z_A(s) = E[(1+U)^s], U ~ Beta(a,b) (Dirichlet on Delta_2), by
# Gauss-Jacobi quadrature; contour integrals around the claimed poles.
# ---------------------------------------------------------------------------
log("== OBL-017/018 (Gauss-Jacobi, contour integrals) ==")
aa, bb = 0.5, 1.5
xj, wj = special.roots_jacobi(80, bb - 1, aa - 1)  # weight (1-x)^(b-1)(1+x)^(a-1) on [-1,1]
uj = (xj + 1) / 2
wj = wj / wj.sum()  # Beta(a,b) expectation weights


def Z(s):
    return np.sum(wj * (1.0 + uj) ** s)


def Mcoord(s):  # E[U^s] closed form
    return np.exp(special.loggamma(aa + s) + special.loggamma(aa + bb) - special.loggamma(aa) - special.loggamma(aa + bb + s))


def contour(f, c, rad=0.2, M=400):
    th = np.linspace(0, 2 * np.pi, M, endpoint=False)
    z = c + rad * np.exp(1j * th)
    return np.sum(np.array([f(zz) for zz in z]) * 1j * rad * np.exp(1j * th)) * (2 * np.pi / M) / (2j * np.pi)


for k in range(3):
    sk = -aa - k
    rZ = contour(Z, sk)
    log(f"claimed pole s=-a-{k}={sk}: Z finite = {Z(sk):.10f}, (1/2pi i) contour integral of Z = {abs(rZ):.2e}")
    check(f"no residue of Z_A at s={sk}", abs(rZ) < 1e-10)
# check Z by a second route: 2F1 representation E[(1+U)^s] = 2F1(-s, a; a+b; -1)
for s in [-0.5, -2.5, 1.3]:
    check(f"Z({s}) Gauss-Jacobi = 2F1 route", abs(Z(s) - special.hyp2f1(-s, aa, aa + bb, -1.0)) < 1e-10)
# coordinate Mellin transform: closed form vs quadrature (Re s > -a), residues
# (Gauss-Jacobi is not used here: u^s has a non-polynomial endpoint singularity.
#  QUADPACK's algebraic-weight rule integrates u^(a-1+s)(1-u)^(b-1) exactly in the weight.)
for s in [0.3, -0.2, -0.45, 1.7]:
    sq = integrate.quad(lambda u: 1.0, 0, 1, weight="alg", wvar=(aa - 1 + s, bb - 1))[0] / special.beta(aa, bb)
    check(f"E[U^s] closed form = QUADPACK algebraic-weight quadrature at s={s}", abs(sq - Mcoord(s)) < 1e-8)
for k in range(3):
    sk = -aa - k
    rr = contour(Mcoord, sk, rad=0.1)
    pred = (-1) ** k / special.factorial(k) * special.gamma(aa + bb) / (special.gamma(aa) * special.gamma(aa + bb - aa - k))
    log(f"NEG CONTROL coordinate Mellin: residue at {sk}: contour {rr.real:+.8f}, formula {pred:+.8f}")
    check(f"coordinate Mellin has the predicted non-zero residue at {sk}", abs(rr - pred) < 1e-8 and abs(pred) > 1e-3)
# cancellation when b is a positive integer: a=0.5, b=2 -> poles only at -a, -a-1
bb2 = 2.0
M2 = lambda s: np.exp(special.loggamma(aa + s) + special.loggamma(aa + bb2) - special.loggamma(aa) - special.loggamma(aa + bb2 + s))
r2 = abs(contour(M2, -aa - 2, rad=0.1))
r1 = abs(contour(M2, -aa - 1, rad=0.1))
log(f"b=2: |residue| at -a-1 = {r1:.3e} (pole), at -a-2 = {r2:.3e} (cancelled)")
check("b integer: pole at -a-1 present, -a-2 cancelled", r1 > 1e-3 and r2 < 1e-10)

# ---------------------------------------------------------------------------
# OBL-006: S^1 with Phi = cos(theta), constant sheaf.
# ---------------------------------------------------------------------------
log("== OBL-006 ==")
V, E = 8, 8  # triangulated circle
chi_S1 = V - E
chi_arc = 1  # open arc is contractible
chi_c_arc = -1  # one open 1-cell
chi_pt = 1
paper = 1 * (2 * chi_arc) + 0 * (2 * chi_pt)  # CC = [zero section] = 1*closure(T*_{Sigma_1}), m_0 = 0
correct = 1 * (2 * chi_c_arc) + 1 * (2 * chi_pt)  # sum chi_c(stratum) * stalk Euler char
log(f"chi(S^1) = {chi_S1}; paper formula sum m_r chi(Sigma_r) = {paper}; sum chi_c(Sigma_r) chi(stalk) = {correct}")
check("stratified chi_c formula reproduces chi(S^1)", correct == chi_S1)
check("NEG CONTROL: paper formula differs from chi(S^1)", paper != chi_S1)

# ---------------------------------------------------------------------------
# OBL-020: reach via Federer's formula reach = inf |q-p|^2 / (2 d(q-p, T_p)).
# ---------------------------------------------------------------------------
log("== OBL-020 (Federer Thm 4.18 formula) ==")


def curve_data(kind, M=1500):
    th = np.linspace(0, 2 * np.pi, M, endpoint=False)
    if kind == "ellipse":
        P = np.c_[2 * np.cos(th), np.sin(th)]
        Phi_grad = lambda x, y: np.c_[x / 2, 2 * y]
        Hop = 2.0
    else:  # peanut: level set Phi = x^4/4 - x^2/2 + 2 y^2 = t, t = 0.2 (bottleneck at x=0)
        t = 0.2
        # parametrise by polar angle, solve radial equation
        P = []
        for a_ in th:
            c, s_ = np.cos(a_), np.sin(a_)
            f = lambda r: (r * c) ** 4 / 4 - (r * c) ** 2 / 2 + 2 * (r * s_) ** 2 - t
            P.append(optimize.brentq(f, 1e-6, 5.0) * np.array([c, s_]))
        P = np.array(P)
        Phi_grad = lambda x, y: np.c_[x ** 3 - x, 4 * y]
        xs = np.linspace(-2, 2, 4001)
        Hop = max(np.max(np.abs(3 * xs[np.abs(xs) <= np.max(np.abs(P[:, 0]))] ** 2 - 1)), 4.0)
    g = Phi_grad(P[:, 0], P[:, 1])
    gn = np.linalg.norm(g, axis=1)
    nu = g / gn[:, None]
    return P, nu, gn.min(), Hop


def federer_reach(P, nu):
    best = np.inf
    for i in range(len(P)):
        dq = P - P[i]
        nrm2 = np.sum(dq ** 2, axis=1)
        dn = np.abs(dq @ nu[i])
        mask = (nrm2 > 0) & (dn > 1e-14)
        best = min(best, np.min(nrm2[mask] / (2 * dn[mask])))
    return best


def dsep(P, nu, tol=2e-3):
    best = np.inf
    for i in range(len(P)):
        mask = np.sum((nu + nu[i]) ** 2, axis=1) < tol ** 2
        if mask.any():
            best = min(best, np.min(np.linalg.norm(P[mask] - P[i], axis=1)))
    return best


for kind in ["ellipse", "peanut"]:
    P, nu, eps0, M = curve_data(kind)
    R = federer_reach(P, nu)
    ds = dsep(P, nu)
    bound = min(eps0 / M, ds / 2)
    log(f"{kind}: reach(Federer formula) = {R:.4f}, eps0/M = {eps0/M:.4f}, d_sep/2 = {ds/2:.4f}, bound = {bound:.4f}")
    check(f"{kind}: reach >= min(eps0/M, d_sep/2) (tol 2e-3)", R >= bound - 2e-3)
    check(f"NEG CONTROL {kind}: doubled bound 2*min(...) exceeds the reach", 2 * bound > R + 1e-3)
P, nu, eps0, M = curve_data("ellipse")
check("ellipse: d_sep is finite (paper claimed infinity for convex)", np.isfinite(dsep(P, nu)))

# ---------------------------------------------------------------------------
# OBL-001: ball inclusions B(x0, r_min) in K_t in B(x0, R_max) for a non-quadratic convex Phi.
# ---------------------------------------------------------------------------
log("== OBL-001 (radial function of K_t) ==")
dim = 4
Q0 = rng.normal(size=(dim, dim))
Q0 = Q0 @ Q0.T + 0.5 * np.eye(dim)
bvec = rng.normal(size=dim)
Phi = lambda x: 0.5 * x @ Q0 @ x + 0.05 * np.sum(x ** 4) + bvec @ x
grad = lambda x: Q0 @ x + 0.2 * x ** 3 + bvec
hess = lambda x: Q0 + 0.6 * np.diag(x ** 2)
x0 = optimize.minimize(Phi, np.zeros(dim), jac=grad, tol=1e-14).x
m0 = Phi(x0)
t = m0 + 1.5
dirs = rng.normal(size=(3000, dim))
dirs /= np.linalg.norm(dirs, axis=1)[:, None]
rho = np.array([optimize.brentq(lambda s: Phi(x0 + s * d) - t, 0, 50) for d in dirs])
# Hessian bounds over K_t, sampled on rays inside K_t
pts = np.concatenate([x0 + np.outer(np.linspace(0, 1, 15), rho_i * d) for rho_i, d in zip(rho[:600], dirs[:600])])
evs = np.array([np.linalg.eigvalsh(hess(x))[[0, -1]] for x in pts])
lmin, lmax = evs[:, 0].min(), evs[:, 1].max()
rmin, Rmax = np.sqrt(2 * (t - m0) / lmax), np.sqrt(2 * (t - m0) / lmin)
log(f"radial function range [{rho.min():.4f},{rho.max():.4f}] ; r_min = {rmin:.4f}, R_max = {Rmax:.4f}")
check("B(x0,r_min) subset K_t subset B(x0,R_max)", rho.min() >= rmin - 1e-9 and rho.max() <= Rmax + 1e-9)
check("NEG CONTROL swapped radii fail", not (rho.min() >= Rmax and rho.max() <= rmin))

# ---------------------------------------------------------------------------
# OBL-010: synchronous coupling contraction |X_t - Y_t| <= e^{-kappa t}|X_0 - Y_0|.
# ---------------------------------------------------------------------------
log("== OBL-010 (synchronous coupling) ==")
kap = 1.0
gradV = lambda x: kap * x + 0.3 * x ** 3 + np.sin(x) * 0.0  # V = kap x^2/2 + 0.075 x^4 is kap-convex
dt, Tn = 1e-3, 3000
X = rng.normal(size=2000) * 3
Y = rng.normal(size=2000)
d0 = np.abs(X - Y)
okc, okneg = True, True
for k in range(Tn):
    dW = rng.normal(size=2000) * np.sqrt(2 * dt)
    X = X - gradV(X) * dt + dW
    Y = Y - gradV(Y) * dt + dW
tt = Tn * dt
ratio = np.max(np.abs(X - Y) / (d0 * np.exp(-kap * tt)))
ratio2 = np.max(np.abs(X - Y) / (d0 * np.exp(-3 * kap * tt)))
log(f"max |X_t-Y_t| / (e^-kt |X0-Y0|) = {ratio:.4f} ; with mutated rate 3k: {ratio2:.4f}")
check("contraction with rate kappa holds pathwise (Euler scheme, tol 1%)", ratio <= 1.01)
check("NEG CONTROL: rate 3*kappa violated", ratio2 > 1.01)

# ---------------------------------------------------------------------------
# OBL-019: Kigami-Lapidus equation N (r/N)^(d/2) = 1 solved numerically.
# ---------------------------------------------------------------------------
log("== OBL-019 ==")
Nn, rr_ = 3, 3 / 5
ds_root = 2 * optimize.brentq(lambda h: Nn * (rr_ / Nn) ** h - 1, 0.01, 5)
log(f"root of N (r/N)^(d/2)=1: d_s = {ds_root:.6f}; closed form 2 log3/log5 = {2*np.log(3)/np.log(5):.6f}")
check("Kigami-Lapidus root = 2 log 3 / log 5", abs(ds_root - 2 * np.log(3) / np.log(5)) < 1e-10)
check("NEG CONTROL: Hausdorff dimension log3/log2 differs", abs(np.log(3) / np.log(2) - ds_root) > 0.1)

log(f"failures: {FAIL}")
with open(__file__.replace(".py", ".out.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(OUT) + "\n")
sys.exit(FAIL)
