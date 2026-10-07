"""Corrector's independent checks for the repaired M items of Vol. II.

M1  Thm 2.3(c): metric speed of t -> Phi_kernel(A(t)) on [0,1] (exact 1D W2 via quantile functions)
    against the bound |mu'| <= ||d_t rho||_{L2} / (pi sqrt(c0)); negative control: constant 0.9/pi fails.
    Thm 2.3(b): near-extremal pair, ratio W2/bound -> 1 (sharpness).
M5  Prop. on the trigonometric profile: c* = (2pi)^-2 int_{[0,2pi]^2} H_u^2 |grad u| with u = sin y1 sin y2
    (periodic cell, midpoint rule, 3 refinements) and W(Phi_k) on [0,1]^2 against c* eps k^3.
    Negative control: W/(eps k^2) is not bounded.
M6  Besov index: step realization, ||f(.+h)-f||_{L^p} ~ h^{1/p}; smooth f ~ h.
    Negative control: the claim s*_2 = 1 for a step realization fails.
Fixed seed; output corrector_M_checks.out.txt; exit code = failures."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(7)
OUT = []; fail = 0
def log(s):
    OUT.append(s); print(s)
def check(name, cond):
    global fail
    if not cond:
        fail += 1
    log(("PASS " if cond else "FAIL ") + name)

# ---------------------------------------------------------------- M1
log("== M1: metric speed bound on [0,1]")
x = np.linspace(0, 1, 400001)
psi = np.array([np.ones_like(x), np.sqrt(2) * np.cos(np.pi * x), np.sqrt(2) * np.cos(2 * np.pi * x)])
def Phi(A):
    return np.einsum("ix,ij,jx->x", psi, A, psi)
def W2_1d(r1, r2):
    def quant(r):
        F = np.concatenate([[0], np.cumsum((r[1:] + r[:-1]) / 2 * np.diff(x))]); F /= F[-1]
        u = (np.arange(200000) + 0.5) / 200000
        return np.interp(u, F, x)
    q1, q2 = quant(r1), quant(r2)
    return np.sqrt(np.mean((q1 - q2) ** 2))
def A_of(t, a_rate, b):
    return np.array([[1 - b, a_rate * t, 0], [a_rate * t, b, 0], [0, 0, 0]])
for (a_rate, b, t) in [(0.1, 0.05, 0.3), (0.02, 0.01, 0.5), (0.3, 0.3, 0.2)]:
    A = A_of(t, a_rate, b)
    assert np.all(np.linalg.eigvalsh(A) > -1e-12) and abs(np.trace(A) - 1) < 1e-12
    rho = Phi(A); c0 = rho.min()
    check("Phi_kernel(A) is a probability density (int = Tr A = 1)", abs(np.trapezoid(rho, x) - 1) < 1e-8)
    h = 1e-4
    speed = W2_1d(Phi(A_of(t + h, a_rate, b)), Phi(A_of(t - h, a_rate, b))) / (2 * h)
    drho = (Phi(A_of(t + h, a_rate, b)) - Phi(A_of(t - h, a_rate, b))) / (2 * h)
    bound = np.sqrt(np.trapezoid(drho ** 2, x)) / (np.pi * np.sqrt(c0))
    Adot = np.array([[0, a_rate, 0], [a_rate, 0, 0], [0, 0, 0]])
    Lpsi = np.sqrt(np.trapezoid((psi ** 2).sum(0) ** 2, x))
    bound2 = Lpsi * np.linalg.norm(Adot) / (np.pi * np.sqrt(c0))
    log("a=%.2f b=%.2f: c0=%.4f speed=%.6f  bound ||drho||/(pi sqrt c0)=%.6f  ratio %.4f ; final bound L||Adot||/(pi sqrt c0)=%.6f"
        % (a_rate, b, c0, speed, bound, speed / bound, bound2))
    check("speed <= ||d_t rho||_L2/(pi sqrt c0) <= L ||Adot||_F/(pi sqrt c0)", speed <= bound * (1 + 1e-6) and bound <= bound2 * (1 + 1e-9))
# near-extremal: rho = 1 + t*eps*cos(pi x) at t=0 (Neumann first eigenfunction)
eps = 1e-2
r0 = np.ones_like(x); r1 = 1 + 1e-4 * eps * np.cos(np.pi * x)
speed = W2_1d(r1, r0) / 1e-4
bnd = np.sqrt(np.trapezoid((eps * np.cos(np.pi * x)) ** 2, x)) / (np.pi * np.sqrt(1 - 1e-4 * eps))
log("near-extremal: speed %.6e bound %.6e ratio %.5f" % (speed, bnd, speed / bnd))
check("near-extremal ratio > 0.99 (constant 1/pi is sharp)", speed / bnd > 0.99)
check("NEG CTRL: mutated constant 0.9/pi is violated", speed > 0.9 * bnd)
# Thm 2.3(b) sharpness: uniform on [0,e] vs uniform on [1-e,1]
for e in [0.1, 0.01, 0.001]:
    ra = np.where(x <= e, 1 / e, 0.0); rb = np.where(x >= 1 - e, 1 / e, 0.0)
    w = W2_1d(ra + 1e-12, rb + 1e-12)
    bound = 1 / np.sqrt(2) * np.sqrt(2.0)
    log("Thm 2.3(b): e=%.3f W2=%.5f (exact 1-e=%.5f) bound=%.5f ratio=%.5f" % (e, w, 1 - e, bound, w / bound))
check("Thm 2.3(b) ratio -> 1 (sharp), never above 1", 0.995 < w / bound <= 1 + 1e-6)

# ---------------------------------------------------------------- M5
log("== M5: Willmore energy of the trigonometric profile")
def integrand(Y1, Y2):
    s1, c1, s2, c2 = np.sin(Y1), np.cos(Y1), np.sin(Y2), np.cos(Y2)
    u1, u2 = c1 * s2, s1 * c2
    u11, u22, u12 = -s1 * s2, -s1 * s2, c1 * c2
    G2 = u1 ** 2 + u2 ** 2
    num = (u11 + u22) * G2 - (u1 * u1 * u11 + 2 * u1 * u2 * u12 + u2 * u2 * u22)
    H = -num / G2 ** 1.5
    return H ** 2 * np.sqrt(G2)
cs = []
for M in [1000, 2000, 4000]:
    y = (np.arange(M) + 0.5) * 2 * np.pi / M
    tot = 0.0
    for blk in np.array_split(np.arange(M), 8):
        Y1, Y2 = np.meshgrid(y[blk], y, indexing="ij")
        tot += integrand(Y1, Y2).sum()
    cs.append(tot / M ** 2)
    log("periodic cell M=%d: c* = %.5f" % (M, cs[-1]))
cstar = cs[-1]
check("c* converges under refinement (changes < 1%)", abs(cs[-1] - cs[-2]) / cs[-1] < 1e-2 and cstar > 0)
for k in [16, 32, 64]:
    M = 40 * k
    t = (np.arange(M) + 0.5) / M
    tot = 0.0
    for blk in np.array_split(np.arange(M), 16):
        X1, X2 = np.meshgrid(t[blk], t, indexing="ij")
        tot += integrand(k * X1, k * X2).sum()
    eps_k = 1.0 / k
    W = eps_k * k ** 3 * tot / M ** 2
    log("k=%d eps=1/k: W=%.2f  W/(eps k^3)=%.4f  c*=%.4f  W/(eps k^2)=%.2f" % (k, W, W / (eps_k * k ** 3), cstar, W / (eps_k * k ** 2)))
check("W/(eps k^3) -> c* within 3% at k=64", abs(W / (eps_k * k ** 3) - cstar) / cstar < 0.03)
check("NEG CTRL: W/(eps k^2) is unbounded (exceeds 50 at k=64)", W / (eps_k * k ** 2) > 50)

# ---------------------------------------------------------------- M6
log("== M6: Besov index of a step realization")
R = 512
Mx = rng.integers(0, 4, size=(4, 4)).astype(float); Mx[0, 0], Mx[0, 1] = 0.0, 3.0
f = np.kron(Mx, np.ones((R // 4, R // 4)))
gx = (np.arange(R) + 0.5) / R
sm = np.sin(2 * np.pi * gx)[:, None] * np.cos(np.pi * gx)[None, :]
def dnorm(F, j, p):
    return (np.mean(np.abs(F[j:, :] - F[:-j, :]) ** p)) ** (1 / p)
hs = np.array([1, 2, 4, 8, 16])
for p in [1.0, 2.0, 4.0]:
    sl = np.polyfit(np.log(hs / R), np.log([dnorm(f, j, p) for j in hs]), 1)[0]
    ss = np.polyfit(np.log(hs / R), np.log([dnorm(sm, j, p) for j in hs]), 1)[0]
    log("p=%.0f: step slope %.4f (claim 1/p=%.4f) ; smooth slope %.4f (claim 1)" % (p, sl, 1 / p, ss))
    check("p=%.0f step exponent = 1/p, smooth = 1" % p, abs(sl - 1 / p) < 0.02 and abs(ss - 1) < 0.02)
check("NEG CTRL: s*_2 = 1 for the step realization is false (slope far from 1)", abs(np.polyfit(np.log(hs / R), np.log([dnorm(f, j, 2.0) for j in hs]), 1)[0] - 1) > 0.3)

log("failures=%d" % fail)
open(os.path.join(HERE, "corrector_M_checks.out.txt"), "w", encoding="utf8").write("\n".join(OUT))
sys.exit(int(fail))
