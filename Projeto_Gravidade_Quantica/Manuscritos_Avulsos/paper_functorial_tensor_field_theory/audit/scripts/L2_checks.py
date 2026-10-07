"""Layer-2 re-check (independent session, 2026-10-06) of the new proofs of the revised paper.
Each check: independent oracle + negative control (mutated formula/hypothesis must fail); refinement
where numerical. Fixed seed. Exit code = number of failed checks. Runtime: < 1 min, memory < 100 MB.

L1  Prop 4.2(b) contour geometry: centre c=(1+l/4)/2, radius r=(1-l/4)/2+l/8 (symbolic) -> crossings l/8 and
    1+l/8, distance >= l/8 from {0} u [l/2,1]. Control: radius without the +l/8 term touches the eigenvalue 1.
L2  Prop 4.2(b) contour formula vs eigen-decomposition on random constant-rank rho (chi=4, rank 2,3), with
    quadrature refinement (trapezoid on a circle: exponential convergence). Control: f(z)=+z log z.
L3  Prop 4.2(b) smoothness at constant rank: second t-derivative of S along a rank-2 path in chi=4, FD with
    3 refinements (rate 2) against an independent analytic oracle (eigenvalues known). Control: rank change.
L4  Prop 6.3: phi'' symbolic; alpha' range [3/4, 9/8]; Vol(alpha) < Vol(id) by direct quadrature where the
    lapse is computed from an actual rho(s) (p(s) solved by root finding, S by eigenvalues, d/ds by FD) - an
    oracle independent of the closed form phi. Control: c = sigma0/2 (phi convex on alpha' range) reverses.
L5  Prop 6.2: min alpha' over s0, s >= 1/2 (paper's bound 3/8 is weaker but valid); alpha'(s0) != 1.
L6  Thm 5.4: functoriality on a toy datum (product qubit field on T^3, sitting bump paths): image of the
    concatenation == concatenation of images on a grid incl. the junction; associativity of concatenation.
    Control: non-sitting paths -> lapse of the concatenation is discontinuous at the junction.
L7  Remark 5.6(b): the paper's fixed-U construction changes source/target (not a faithfulness counterexample);
    a t-dependent U(t)=exp(i b(t) H) with b=0 near both ends keeps endpoints and h(t) - a valid counterexample.
    Control: x-dependent unitary changes h.
L8  Example 6.1: n n (G + Lambda g) = 3 adot^2/(N0^2 a^2) - Lambda (sympy, Christoffel route) vs the paper's
    display (no -Lambda): equal only at Lambda = 0. Conclusion 'no Lambda' still holds.
L9  Order of magnitude: l_P^2 and A/(8 l_P^2) for 1 m^2 (CODATA via scipy) vs paper 2.61e-70, 4.8e68.
"""
import os
import sys

import numpy as np
import sympy as sp
import mpmath as mp
from scipy.linalg import expm
from scipy.optimize import brentq
from scipy.integrate import quad
import scipy.constants as C

rng = np.random.default_rng(31415)
HERE = os.path.dirname(os.path.abspath(__file__))
log, fails = [], 0


def rep(name, ok, msg):
    global fails
    log.append(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}")
    fails += 0 if ok else 1


def S_eig(r):
    w = np.linalg.eigvalsh(r)
    w = w[w > 1e-14]
    return float(-(w * np.log(w)).sum())


# ------------------------------------------------------------------ L1 contour geometry (symbolic)
l = sp.symbols("l", positive=True)
c = (1 + l / 4) / 2
r = (1 - l / 4) / 2 + l / 8
ok = sp.simplify(c - r - l / 8) == 0 and sp.simplify(c + r - 1 - l / 8) == 0
d0 = sp.simplify(c - r)                         # distance from 0 (0 outside, left of the circle)
d_lo = sp.simplify(r - (c - l / 2))             # distance of l/2 to the circle (inside)
d_hi = sp.simplify(r - (1 - c))                 # distance of 1 to the circle (inside)
ok = ok and sp.simplify(d0 - l / 8) == 0 and sp.simplify(d_lo - 3 * l / 8) == 0 and sp.simplify(d_hi - l / 8) == 0
vals = [(float(d0.subs(l, v)), float(d_lo.subs(l, v)), float(d_hi.subs(l, v))) for v in [1e-6, 0.1, 0.5, 1.0]]
ok = ok and all(min(t3) >= v / 8 - 1e-15 for t3, v in zip(vals, [1e-6, 0.1, 0.5, 1.0]))
r_bad = (1 - l / 4) / 2
ctrl = sp.simplify(r_bad - (1 - c))             # distance of eigenvalue 1 to mutated circle
rep("L1 Prop 4.2(b) contour: crossings l/8, 1+l/8; distance >= l/8 from {0} u [l/2,1]",
    ok and ctrl == 0,
    f"c-r={d0}, dist(l/2)={d_lo}, dist(1)={d_hi}; r=1/2 exactly: {sp.simplify(r)}; "
    f"control radius without +l/8 passes through eigenvalue 1 (distance {ctrl})")


# ------------------------------------------------------------------ L2 contour formula, quadrature refinement
def contour_S(rho, lam, n, sign=-1):
    cc, rr = (1 + lam / 4) / 2, (1 - lam / 4) / 2 + lam / 8
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    z = cc + rr * np.exp(1j * th)
    dz = 1j * rr * np.exp(1j * th)
    I = np.eye(rho.shape[0])
    tr = np.array([np.trace(np.linalg.inv(zz * I - rho)) for zz in z])
    val = (sign * z * np.log(z) * tr * dz).sum() * (2 * np.pi / n) / (2j * np.pi)
    return float(val.real)


def rand_rho(chi, rank):
    U = np.linalg.qr(rng.normal(size=(chi, chi)) + 1j * rng.normal(size=(chi, chi)))[0]
    p = rng.uniform(0.2, 1.0, size=rank); p /= p.sum()
    return U @ np.diag(np.r_[p, np.zeros(chi - rank)]) @ U.conj().T, min(p)


errs_all, ctrl_all = [], []
for rank in [2, 3, 4]:
    rho, lam = rand_rho(4, rank)
    ex = S_eig(rho)
    errs = [abs(contour_S(rho, lam, n) - ex) for n in [64, 256, 1024]]
    errs_all.append(errs)
    ctrl_all.append(abs(contour_S(rho, lam, 1024, sign=+1) - ex))
ok = all(e[-1] < 1e-10 and e[-1] <= e[0] for e in errs_all) and min(ctrl_all) > 1e-2
rep("L2 contour integral = -sum lam log lam (zero eigenvalues outside Gamma), n = 64/256/1024 nodes",
    ok, f"errors per rank 2,3,4: {[[f'{x:.1e}' for x in e] for e in errs_all]}; control (+z log z) min err {min(ctrl_all):.2e}")

# ------------------------------------------------------------------ L3 smoothness at constant rank (FD refinement)
A = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4)); A = A - A.conj().T


def rho_path(t):
    U = expm(t * A / 4)
    p = 0.35 + 0.15 * np.sin(2 * t)
    return U @ np.diag([p, 1 - p, 0, 0]) @ U.conj().T


t0 = 0.37
pp = lambda t: 0.35 + 0.15 * np.sin(2 * t)
# oracle: S(t) = H2(p(t)); S'' = -p''log(p/(1-p)) - p'^2/(p(1-p))
p_, d1, d2 = pp(t0), 0.3 * np.cos(2 * t0), -0.6 * np.sin(2 * t0)
S2_exact = -d2 * np.log(p_ / (1 - p_)) - d1 ** 2 / (p_ * (1 - p_))
hs = [4e-2, 2e-2, 1e-2, 5e-3]
fd = [(S_eig(rho_path(t0 + h)) - 2 * S_eig(rho_path(t0)) + S_eig(rho_path(t0 - h))) / h ** 2 for h in hs]
e = [abs(f - S2_exact) for f in fd]
rates = [np.log2(e[i] / e[i + 1]) for i in range(3)]
# control: rank change diag(1-t, t, 0, 0) at t -> 0: second derivative -1/(t(1-t)) unbounded
ctrlv = [abs((S_eig(np.diag([1 - t - h, t + h, 0, 0])) - 2 * S_eig(np.diag([1 - t, t, 0, 0]))
              + S_eig(np.diag([1 - t + h, t - h, 0, 0]))) / h ** 2) for t, h in [(1e-1, 1e-3), (1e-2, 1e-4), (1e-3, 1e-5)]]
rep("L3 S''(t) at constant rank 2 (chi=4) converges at rate 2 to the analytic oracle; unbounded at rank change",
    e[-1] < 1e-4 and all(1.8 < q < 2.2 for q in rates) and ctrlv[-1] > 50 * ctrlv[0],
    f"FD errors {[f'{x:.1e}' for x in e]}, rates {[f'{q:.2f}' for q in rates]}; control |S''| {[f'{x:.1f}' for x in ctrlv]}")

# ------------------------------------------------------------------ L4 Prop 6.3 Jensen
u, cs, s0s, k0 = sp.symbols("u c sigma0 kappa0", positive=True)
phi = k0 ** sp.Rational(-1, 2) * (cs ** 2 * u ** 2 + s0s ** 2) ** sp.Rational(1, 4)
phi2_paper = sp.Rational(1, 2) * cs ** 2 * k0 ** sp.Rational(-1, 2) * (cs ** 2 * u ** 2 + s0s ** 2) ** sp.Rational(-7, 4) \
    * (s0s ** 2 - cs ** 2 * u ** 2 / 2)
ok_phi = sp.simplify(sp.diff(phi, u, 2) - phi2_paper) == 0
s = sp.symbols("s")
alpha = s + sp.Rational(1, 2) * s * (1 - s) * (s - sp.Rational(1, 2))
da = sp.expand(sp.diff(alpha, s))
grid = np.linspace(0, 1, 200001)
dav = sp.lambdify(s, da)(grid)
ok_al = abs(dav.min() - 0.75) < 1e-9 and abs(dav.max() - 9 / 8) < 1e-9 and sp.integrate(da, (s, 0, 1)) == 1


def vol_from_rho(sigma0, c_, chi, al, dal, kappa0=1.0, h=1e-5):
    """4-volume per unit Vol_h of the image of P o al, lapse built from an actual rho(s)."""
    def S_of_p(p):
        q = (1 - p) / (chi - 1)
        return S_eig(np.diag([p] + [q] * (chi - 1)))
    def p_of(sv):  # invert S on (1/chi, 1)
        return brentq(lambda p: S_of_p(p) - sv, 1 / chi + 1e-15, 1 - 1e-15, xtol=1e-15, rtol=1e-15)
    S_line = lambda sv: S_of_p(p_of(0.25 + c_ * sv))   # S(rho(s)) via the actual matrices
    def N(sv):
        # central FD of s -> S(rho(al(s))); al is a polynomial, so al(s +- h) is defined just outside [0,1]
        dS = (S_line(al(sv + h)) - S_line(al(sv - h))) / (2 * h)
        return ((dS ** 2 + sigma0 ** 2) / kappa0 ** 2) ** 0.25
    return quad(N, 0, 1, epsabs=1e-10, epsrel=1e-10, limit=200)[0]


al_f = sp.lambdify(s, alpha)
dal_f = sp.lambdify(s, da)
res, ctrl_res = [], []
for sigma0 in [0.05, 0.3, 1.0]:
    chi = 2
    while np.log(chi) <= 2 * sigma0 + 0.5:
        chi += 1
    c_ = 2 * sigma0
    Vid = vol_from_rho(sigma0, c_, chi, lambda x: x, lambda x: 1.0)
    Val = vol_from_rho(sigma0, c_, chi, al_f, dal_f)
    closed_id = (c_ ** 2 + sigma0 ** 2) ** 0.25
    closed_al = quad(lambda x: (c_ ** 2 * dal_f(x) ** 2 + sigma0 ** 2) ** 0.25, 0, 1, epsabs=1e-13)[0]
    res.append((sigma0, chi, Vid, Val, abs(Vid - closed_id), abs(Val - closed_al)))
    # control: c = sigma0/2 -> c^2 u^2 <= (9/8)^2 sigma0^2 /4 < 2 sigma0^2 -> phi convex on [3/4, 9/8]
    cc_ = sigma0 / 2
    ctrl_res.append(quad(lambda x: (cc_ ** 2 * dal_f(x) ** 2 + sigma0 ** 2) ** 0.25, 0, 1, epsabs=1e-14)[0]
                    - (cc_ ** 2 + sigma0 ** 2) ** 0.25)
ok4 = ok_phi and ok_al and all(v[3] < v[2] and v[4] < 1e-6 and v[5] < 1e-6 for v in res) and all(x > 0 for x in ctrl_res)
rep("L4 Prop 6.3: phi'' formula; alpha' in [3/4,9/8], int alpha' = 1; Vol(alpha) < Vol(id) from actual rho(s)",
    ok4, f"phi'' symbolic match {ok_phi}; alpha' range [{dav.min():.6f},{dav.max():.6f}]; "
         + "; ".join(f"sigma0={v[0]}, chi={v[1]}: Vol(id)={v[2]:.8f} Vol(alpha)={v[3]:.8f} (|closed-form diff| {v[4]:.1e},{v[5]:.1e})" for v in res)
         + f"; control c=sigma0/2 (convex): Vol(alpha)-Vol(id) = {[f'{x:.2e}' for x in ctrl_res]} (>0, Jensen reversed)")

# ------------------------------------------------------------------ L5 Prop 6.2 alpha'
mins, dev = [], []
for s0 in np.linspace(0.01, 0.99, 99):
    dv = 1 + 0.5 * ((1 - 2 * grid[::20]) * (grid[::20] - s0) + grid[::20] * (1 - grid[::20]))
    mins.append(dv.min())
    dev.append(abs(0.5 * s0 * (1 - s0)))
rep("L5 Prop 6.2: alpha' >= 1/2 > 3/8 for all s0; alpha'(s0) - 1 = s0(1-s0)/2 != 0",
    min(mins) >= 0.5 - 1e-12 and min(dev) > 0, f"min alpha' over s0 grid {min(mins):.4f}; min |alpha'(s0)-1| {min(dev):.4f}")


# ------------------------------------------------------------------ L6 Thm 5.4 functoriality (toy datum)
def bump(x):
    def hh(y):
        return np.exp(-1 / y) if y > 0 else 0.0
    y = (x - 0.25) / 0.5
    return hh(y) / (hh(y) + hh(1 - y))


def field(theta):
    def f(xv):
        v = np.array([1.0 + 0j])
        for k in range(3):
            v = np.kron(v, np.array([np.cos(theta), np.exp(1j * xv[k]) * np.sin(theta)]))
        return v
    return f


def qfi(fn, p, h=1e-4):
    T0 = fn(p); dT = []
    for i in range(3):
        e_ = np.zeros(3); e_[i] = h
        dT.append((fn(p + e_) - fn(p - e_)) / (2 * h))
    P = np.eye(len(T0)) - np.outer(T0, T0.conj())
    return np.array([[4 * (dT[i].conj() @ P @ dT[j]).real for j in range(3)] for i in range(3)])


H2 = lambda p: -(p * np.log(p) + (1 - p) * np.log(1 - p))
sig0, kap0 = 0.4, 1.0


def make_path(L, th0, th1, p0, p1, sitting=True):
    """datum path on [0,L]: theta(t), p(t) (rho=diag(p,1-p)), R(x,t)=r(t)(2+cos x1)^(1/2) E11, Q=0."""
    w = (lambda t: bump(t / L)) if sitting else (lambda t: t / L)
    return {"L": L, "theta": lambda t: th0 + (th1 - th0) * w(t), "p": lambda t: p0 + (p1 - p0) * w(t),
            "r": lambda t: 1.0 + 0.5 * w(t)}


def concat(P1, P2):
    L1 = P1["L"]
    pick = lambda key: (lambda t: P1[key](t) if t <= L1 else P2[key](t - L1))
    return {"L": L1 + P2["L"], "theta": pick("theta"), "p": pick("p"), "r": pick("r")}


def image(P, t, x, dt=1e-6):
    """(h_11, N, N^1) at (x,t): h from numeric QFI, N from FD of S, N^1 from h^{11} Re Tr(R^dag d_1 R)."""
    h = qfi(field(P["theta"](t)), x)
    t_lo, t_hi = max(t - dt, 0), min(t + dt, P["L"])
    dS = (H2(P["p"](t_hi)) - H2(P["p"](t_lo))) / (t_hi - t_lo)
    N = ((dS ** 2 + sig0 ** 2) / kap0 ** 2) ** 0.25
    rr = P["r"](t)
    ReTr = 0.5 * rr ** 2 * (-np.sin(x[0]))      # (1/2) d_1 ||R||^2, ||R||^2 = r^2 (2+cos x1)
    Nsh = np.linalg.solve(h, np.array([ReTr, 0, 0]))[0]
    return np.array([h[0, 0], N, Nsh])


x0 = np.array([0.7, -1.3, 2.2])
P1 = make_path(1.0, 0.3, 0.5, 0.2, 0.35)
P2 = make_path(0.7, 0.5, 0.25, 0.35, 0.3)
P3 = make_path(1.3, 0.25, 0.6, 0.3, 0.4)
P12 = concat(P1, P2)
ts = [0.0, 0.1, 0.5, 0.95, 1.0 - 1e-4, 1.0, 1.0 + 1e-4, 1.2, 1.69, 1.7]
dif = max(np.max(abs(image(P12, t, x0) - (image(P1, t, x0) if t <= 1 else image(P2, t - 1, x0)))) for t in ts)
lhs, rhs = concat(concat(P1, P2), P3), concat(P1, concat(P2, P3))
assoc = max(abs(lhs[k](t) - rhs[k](t)) for k in ["theta", "p", "r"] for t in np.linspace(0, 3.0, 301))
N0 = np.sqrt(sig0 / kap0)
endN = abs(image(P12, 0.0, x0)[1] - N0) + abs(image(P12, 1.7, x0)[1] - N0)
# control: non-sitting paths -> lapse jumps at the junction
Q1, Q2 = make_path(1.0, 0.3, 0.5, 0.2, 0.35, False), make_path(0.7, 0.5, 0.25, 0.35, 0.3, False)
Q12 = concat(Q1, Q2)
jump = abs(image(Q12, 1.0 - 1e-5, x0)[1] - image(Q12, 1.0 + 1e-5, x0)[1])
jump_s = abs(image(P12, 1.0 - 1e-5, x0)[1] - image(P12, 1.0 + 1e-5, x0)[1])
Hp = np.log(0.65 / 0.35)                                 # H2'(p) at p = 0.35
NN = lambda dS: ((dS ** 2 + sig0 ** 2) / kap0 ** 2) ** 0.25
jump_exact = abs(NN(Hp * 0.15 / 1.0) - NN(Hp * (-0.05) / 0.7))   # analytic one-sided limits (linear paths)
rep("L6 Thm 5.4: F(concat) = concat(F) incl. junction; strict associativity; sitting ends give N = N0",
    dif < 1e-8 and assoc == 0 and endN < 1e-8 and jump_s < 1e-8 and abs(jump - jump_exact) < 1e-3 * jump_exact,
    f"max |F(D12)-concat| {dif:.1e}; assoc diff {assoc}; |N(end)-N0| {endN:.1e}; lapse jump sitting {jump_s:.1e}, "
    f"control non-sitting {jump:.4e} vs analytic one-sided jump {jump_exact:.4e}")

# ------------------------------------------------------------------ L7 Remark 5.6(b) faithfulness
Hd = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8)); Hd = Hd + Hd.conj().T
Ufix = expm(1j * Hd)
th = 0.4
T = field(th)
src_changed = np.linalg.norm(Ufix @ T(x0) - T(x0))           # paper's construction: source datum changes
bfun = lambda t: np.sin(np.pi * bump(t)) * 1.0             # 0 near t=0 and t=1 (bump = 0 or 1 there)
Ut = lambda t: expm(1j * bfun(t) * Hd)
end_same = max(np.linalg.norm(Ut(t) @ T(x0) - T(x0)) for t in [0.0, 0.1, 0.9, 1.0])
mid_diff = np.linalg.norm(Ut(0.5) @ T(x0) - T(x0))
hdiff = max(np.max(abs(qfi(lambda xv: Ut(t) @ T(xv), x0) - qfi(T, x0))) for t in [0.3, 0.5, 0.7])
Cg = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8)); Cg = Cg + Cg.conj().T
hctrl = np.max(abs(qfi(lambda xv: expm(1j * xv[0] * Cg) @ T(xv), x0) - qfi(T, x0)))
rep("L7 Remark 5.6(b): fixed U changes source/target (no faithfulness test); U(t) sitting at I is a valid one",
    src_changed > 1e-3 and end_same < 1e-12 and mid_diff > 1e-2 and hdiff < 1e-6 and hctrl > 1e-3,
    f"|U T(0) - T(0)| = {src_changed:.2f} (paper's morphism lies in Hom(UD,UD')); U(t): end diff {end_same:.1e}, "
    f"mid diff {mid_diff:.2f}, max QFI diff {hdiff:.1e}; control x-dependent unitary {hctrl:.2e}")

# ------------------------------------------------------------------ L8 Example 6.1 with Lambda
t_, N0s, Lam = sp.symbols("t N0 Lambda", positive=True)
af = sp.Function("a")(t_)
X = sp.symbols("x1:4")
co = [t_, *X]
g = sp.diag(-N0s ** 2, af ** 2, af ** 2, af ** 2)
gi = g.inv()
Gam = [[[sum(gi[i, m] * (sp.diff(g[m, j], co[k]) + sp.diff(g[m, k], co[j]) - sp.diff(g[j, k], co[m])) for m in range(4)) / 2
         for k in range(4)] for j in range(4)] for i in range(4)]
Ric = sp.Matrix(4, 4, lambda j, k: sp.simplify(sum(sp.diff(Gam[i][j][k], co[i]) - sp.diff(Gam[i][j][i], co[k])
                                                   + sum(Gam[i][i][q] * Gam[q][j][k] - Gam[i][k][q] * Gam[q][j][i] for q in range(4)) for i in range(4))))
Rs = sp.simplify(sum(gi[i, j] * Ric[i, j] for i in range(4) for j in range(4)))
nn = sp.simplify((Ric[0, 0] - Rs * g[0, 0] / 2 + Lam * g[0, 0]) / N0s ** 2)
true_form = 3 * sp.diff(af, t_) ** 2 / (N0s ** 2 * af ** 2) - Lam
paper_form = 3 * sp.diff(af, t_) ** 2 / (N0s ** 2 * af ** 2)
ok8 = sp.simplify(nn - true_form) == 0 and sp.simplify(nn - paper_form) != 0 and sp.simplify((nn - paper_form).subs(Lam, 0)) == 0
rep("L8 Example 6.1: n n (G + Lambda g) = 3 adot^2/(N0^2 a^2) - Lambda; paper's display omits -Lambda (true at Lambda=0 only)",
    ok8, f"sympy: {sp.simplify(nn)}; conclusion (no Lambda works) unaffected: Lambda != 0 fails where adot = 0, Lambda = 0 fails where adot != 0")

# ------------------------------------------------------------------ L9 order of magnitude
lP2 = C.hbar * C.G / C.c ** 3
ok9 = abs(lP2 / 2.61e-70 - 1) < 5e-3 and abs((1 / (8 * lP2)) / 4.8e68 - 1) < 5e-3 and abs((1 / (4 * lP2)) / 4.8e68 - 1) > 0.5
rep("L9 l_P^2 = 2.61e-70 m^2; A/(8 l_P^2) = 4.8e68 for 1 m^2 (dimensionless)", ok9,
    f"l_P^2 = {lP2:.4e} m^2; A/(8 l_P^2) = {1 / (8 * lP2):.4e}; control A/(4 l_P^2) = {1 / (4 * lP2):.3e} differs")

out = "\n".join(log) + f"\nFAILED CHECKS: {fails}"
print(out)
open(os.path.join(HERE, "L2_checks.out.txt"), "w", encoding="utf8").write(out)
sys.exit(fails)
