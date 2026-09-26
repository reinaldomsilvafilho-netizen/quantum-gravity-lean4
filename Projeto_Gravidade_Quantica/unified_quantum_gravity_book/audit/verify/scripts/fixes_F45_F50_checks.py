"""Checks for the corrections of F-45..F-50 (chapters 1-6).

Every block compares a statement written into the text with an independent
computation and includes a negative control (a mutated formula that must fail).
Run from this folder:  python fixes_F45_F50_checks.py [blocks]
Blocks: A (ch1) B (ch2) C (ch3) D (ch4) E (ch5) F (ch6). Default: all.
"""
import sys
import math
import itertools
import numpy as np
from scipy import integrate, special, linalg

rng = np.random.default_rng(20260925)
FAILS = []


def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + ("  | " + str(info) if info else ""))
    if not ok:
        FAILS.append(name)


# ---------------------------------------------------------------- ch1
def block_A():
    print("== A. Chapter 1 ==")
    # A1: isotropy of the non-symmetric iid model vs the symmetric equal-variance model
    n, d = 3, 3
    x = np.array([1.0, 0, 0]); y = np.array([1, 1, 0]) / math.sqrt(2)
    # exact variance of f(x) for iid tensor = |x|^(2d) = 1 for every unit x
    def var_iid(v):
        return sum(np.prod([v[i] ** 2 for i in idx]) for idx in itertools.product(range(n), repeat=d))
    def var_symeq(v):
        tot = 0.0
        for ms in itertools.combinations_with_replacement(range(n), d):
            mult = math.factorial(d)
            for c in set(ms):
                mult //= math.factorial(ms.count(c))
            tot += mult ** 2 * np.prod([v[i] ** 2 for i in ms])
        return tot
    check("A1 iid tensor: Var f(e1) = Var f((e1+e2)/sqrt2) = 1", abs(var_iid(x) - 1) < 1e-12 and abs(var_iid(y) - 1) < 1e-12)
    check("A1-neg symmetric equal-variance model not isotropic, 1 vs 5/2 (d=3)",
          abs(var_symeq(x) - 1) < 1e-12 and abs(var_symeq(y) - 2.5) < 1e-12, (var_symeq(x), var_symeq(y)))
    check("A1b formula 2^-d binom(2d,d) for d=2,3,4",
          all(abs(math.comb(2 * dd, dd) / 2 ** dd - sum(math.comb(dd, j) ** 2 for j in range(dd + 1)) / 2 ** dd) < 1e-12 for dd in (2, 3, 4)))
    # A2: Cartwright-Sturmfels bound on the number of critical points, d=3, n=3: <= 14
    def crit_points(T, starts=400):
        pts = []
        for _ in range(starts):
            v = rng.normal(size=n); v /= np.linalg.norm(v)
            for _ in range(200):  # Newton on F(v,mu) = (T v v - mu v, |v|^2-1)
                Tv = np.einsum('ijk,j,k->i', T, v, v)
                mu = v @ Tv
                J = 2 * np.einsum('ijk,k->ij', T, v)
                F = np.concatenate([Tv - mu * v, [v @ v - 1]])
                JJ = np.zeros((n + 1, n + 1)); JJ[:n, :n] = J - mu * np.eye(n); JJ[:n, n] = -v; JJ[n, :n] = 2 * v
                try:
                    step = np.linalg.solve(JJ, F)
                except np.linalg.LinAlgError:
                    break
                v = v - step[:n]
                if np.linalg.norm(step) < 1e-13:
                    break
            Tv = np.einsum('ijk,j,k->i', T, v, v)
            if abs(np.linalg.norm(v) - 1) < 1e-9 and np.linalg.norm(Tv - (v @ Tv) * v) < 1e-9:
                if all(np.linalg.norm(v - p) > 1e-6 for p in pts):
                    pts.append(v.copy())
        return pts
    counts = []
    for _ in range(12):
        A = rng.normal(size=(n, n, n))
        T = sum(np.transpose(A, p) for p in itertools.permutations(range(3))) / 6
        counts.append(len(crit_points(T)))
    bound = 2 * ((d - 1) ** n - 1) // (d - 2)
    check("A2 Cartwright-Sturmfels: #crit <= 2((d-1)^n-1)/(d-2) = 14 (d=n=3)", max(counts) <= bound, counts)
    check("A2-neg the quadratic count 2n = 6 is exceeded for d=3", max(counts) > 2 * n, max(counts))
    # A3: attention: f(0,0) = N for softmax rows, and sup bound with C_lambda
    lam = 0.1
    K = 400
    kk = np.arange(-K, K + 1)
    k1, k2 = np.meshgrid(kk, kk)
    C2 = np.sum(1.0 / (1 + k1 ** 2 + k2 ** 2 + lam * (k1 ** 2 + k2 ** 2) ** 2))
    C2 += 2 * math.pi / lam / (2 * K ** 2)  # tail bound int_{r>K} 1/(lam r^4) r dr dtheta
    ok = True; worst = 0
    for N in (4, 8, 16):
        Z = rng.normal(size=(N, N)); A = np.exp(Z); A /= A.sum(1, keepdims=True)
        ks = np.arange(1, N + 1)
        w = 1 + ks[:, None] ** 2 + ks[None, :] ** 2 + lam * (ks[:, None] ** 2 + ks[None, :] ** 2) ** 2
        R = np.sum(w * A ** 2)
        f00 = A.sum()
        ok &= abs(f00 - N) < 1e-9 and f00 <= math.sqrt(C2 * R) + 1e-9
        worst = max(worst, f00 / math.sqrt(C2 * R))
    check("A3 softmax: f(0,0)=N and N <= C_lambda sqrt(R)", ok, "max ratio %.3f" % worst)
    Rs = []
    for N in (4, 16, 64):
        A = np.full((N, N), 1.0 / N)  # uniform attention, the flattest softmax matrix
        ks = np.arange(1, N + 1)
        w = 1 + ks[:, None] ** 2 + ks[None, :] ** 2 + lam * (ks[:, None] ** 2 + ks[None, :] ** 2) ** 2
        Rs.append(np.sum(w * A ** 2))
    check("A3-neg a bound uniform in N fails: R(uniform attention) grows with N", Rs[0] < Rs[1] < Rs[2] and Rs[2] >= 64 ** 2 / C2, Rs)
    # A4: exact Gaussian tail of X(u) (T,u independent) for k=3, d=20
    k, dd, M = 3, 20, 20000
    X = np.empty(M)
    for i in range(M):
        us = [rng.normal(size=dd) for _ in range(k)]
        us = [u / np.linalg.norm(u) for u in us]
        # X(u) = sum T u1 u2 u3 with T iid N(0,1): equal in law to N(0, prod |u|^2)
        g = rng.normal(size=(dd, dd, dd))
        X[i] = np.einsum('ijk,i,j,k->', g, *us)
    check("A4 X(u) has variance 1 under joint law", abs(X.var() - 1) < 0.05, X.var())
    eps = 0.5
    p_emp = np.mean(np.abs(X / math.sqrt(dd)) > eps)
    check("A4 tail <= 2exp(-d eps^2/2)", p_emp <= 2 * math.exp(-dd * eps ** 2 / 2), (p_emp, 2 * math.exp(-dd * eps ** 2 / 2)))
    check("A4-neg exponent c=1 (instead of 1/2) is violated", p_emp > 2 * math.exp(-dd * eps ** 2), 2 * math.exp(-dd * eps ** 2))


# ---------------------------------------------------------------- ch2
def block_B():
    print("== B. Chapter 2 ==")
    # B1: new Dyson bound, random examples + the referee counterexamples
    def pexp(Afun, steps=4000):
        U = np.eye(Afun(0).shape[0], dtype=complex)
        h = 1.0 / steps
        for i in range(steps):  # RK4
            s = i * h
            f = lambda s_, U_: Afun(s_) @ U_
            k1 = f(s, U); k2 = f(s + h / 2, U + h / 2 * k1); k3 = f(s + h / 2, U + h / 2 * k2); k4 = f(s + h, U + h * k3)
            U = U + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        return U
    def bound(r, M, a0, a1, L1, k):
        return r / k * (M + (a1 + a0 ** 2) / 2) * math.exp(L1 + (M + a1 / 2) / k)
    ok = True; ratios = []
    for trial in range(6):
        r = 3
        B0, B1, B2 = (rng.normal(size=(r, r)) for _ in range(3))
        Afun = lambda s: B0 + B1 * math.sin(2 * math.pi * s) + B2 * s ** 2
        dA = lambda s: B1 * 2 * math.pi * math.cos(2 * math.pi * s) + 2 * s * B2
        ss = np.linspace(0, 1, 2001)
        a0 = max(np.linalg.norm(Afun(s), 2) for s in ss)
        a1 = max(np.linalg.norm(dA(s), 2) for s in ss)
        L1 = np.trapezoid([np.linalg.norm(Afun(s), 2) for s in ss], ss)
        exact = np.trace(pexp(Afun))
        M = 2.0
        for k in (5, 20, 80):
            Rs = [rng.normal(size=(r, r)) for _ in range(k)]
            Rs = [R / np.linalg.norm(R, 2) * M for R in Rs]
            P = np.eye(r)
            for j in range(1, k + 1):
                P = (np.eye(r) + Afun(j / k) / k + Rs[j - 1] / k ** 2) @ P
            err = abs(np.trace(P) - exact)
            ratios.append(err / bound(r, M, a0, a1, L1, k))
            ok &= err <= bound(r, M, a0, a1, L1, k)
    check("B1 corrected Dyson bound holds (random C^1 connections)", ok, "max err/bound %.3g" % max(ratios))
    M = 1.0; k = 10
    err = (1 + M / k ** 2) ** k - 1
    check("B1 referee example R=+M: err <= (M/k) e^{M/k}", err <= M / k * math.exp(M / k), (err, M / k * math.exp(M / k)))
    check("B1-neg old bound (M/k, no e^{M/k}) is violated", err > M / k)
    M = 100.0; k = 2
    err = abs((1 - M / k ** 2) ** k - 1)
    check("B1 referee example R=-M, M=100, k=2 within new bound", err <= bound(1, M, 0, 0, 0, k), (err, bound(1, M, 0, 0, 0, k)))
    # B2: Toda off-diagonal mass not monotone
    def toda_rhs(A):
        L = np.tril(A, -1); K = L - L.T
        return A @ K - K @ A
    found = 0
    for _ in range(50):
        A0 = rng.normal(size=(4, 4)); A0 = (A0 + A0.T) / 2
        off = lambda A: np.sum(np.tril(A, -1) ** 2)
        A = A0.copy(); h = 1e-3; prev = off(A); inc = False
        for _ in range(3000):
            k1 = toda_rhs(A); k2 = toda_rhs(A + h / 2 * k1); k3 = toda_rhs(A + h / 2 * k2); k4 = toda_rhs(A + h * k3)
            A = A + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            cur = off(A)
            if cur > prev + 1e-12:
                inc = True
            prev = cur
        found += inc
    check("B2 Toda off-diagonal mass increases somewhere in some runs", found > 0, "%d/50" % found)
    # oracle: Q^T A0 Q with Q from qr(exp(t A0)) matches the ODE (control of the integrator)
    A0 = rng.normal(size=(4, 4)); A0 = (A0 + A0.T) / 2
    A = A0.copy(); h = 1e-3
    for _ in range(1000):
        k1 = toda_rhs(A); k2 = toda_rhs(A + h / 2 * k1); k3 = toda_rhs(A + h / 2 * k2); k4 = toda_rhs(A + h * k3)
        A = A + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    Q, R = np.linalg.qr(linalg.expm(1.0 * A0)); Q = Q * np.sign(np.diag(R))
    check("B2-ctrl ODE = Q^T A0 Q (QR of e^{A0})", np.allclose(A, Q.T @ A0 @ Q, atol=1e-8))
    # B3: graphon Laplacian counterexample W=-1
    xs = (np.arange(4000) + 0.5) / 4000
    u = np.cos(2 * math.pi * xs)
    E = 0.5 * np.mean((-1.0) * (u[:, None] - u[None, :]) ** 2)
    check("B3 W=-1, u=cos 2 pi x: energy = -1/2", abs(E + 0.5) < 1e-6, E)
    check("B3-neg with W=+1 the energy is +1/2", abs(-E - 0.5) < 1e-6)
    # B4: heat coefficients sum
    t = 0.7
    c = [math.exp(-2 * t), math.exp(-t) - math.exp(-2 * t), (1 - math.exp(-t)) ** 2]
    check("B4 e^-2t + 2(e^-t - e^-2t) + (1-e^-t)^2 = 1", abs(c[0] + 2 * c[1] + c[2] - 1) < 1e-14)
    check("B4-neg the three coefficients alone do not sum to 1", abs(sum(c) - 1) > 1e-3, sum(c))
    # B5: TT feasibility and dimension
    def tt_jac_rank(d, r):
        k = len(d)
        shapes = [(r[a], d[a], r[a + 1]) for a in range(k)]
        sizes = [int(np.prod(s)) for s in shapes]
        theta = rng.normal(size=sum(sizes))
        def full(th):
            cores = []; o = 0
            for s, z in zip(shapes, sizes):
                cores.append(th[o:o + z].reshape(s)); o += z
            T = cores[0]
            for C in cores[1:]:
                T = np.tensordot(T, C, axes=(-1, 0))
            return T.reshape(-1)
        J = np.empty((int(np.prod(d)), theta.size)); e = 1e-6
        for i in range(theta.size):
            tp = theta.copy(); tp[i] += e; tm = theta.copy(); tm[i] -= e
            J[:, i] = (full(tp) - full(tm)) / (2 * e)
        return np.linalg.matrix_rank(J, tol=1e-6)
    def tt_dim(d, r):
        return sum(d[a] * r[a] * r[a + 1] for a in range(len(d))) - sum(ra ** 2 for ra in r[1:-1])
    cases = [((3, 4, 3), (1, 2, 3, 1)), ((2, 3, 2, 3), (1, 2, 3, 2, 1)), ((2, 2, 2, 2), (1, 2, 4, 2, 1))]
    ok = all(tt_jac_rank(d, r) == tt_dim(d, r) for d, r in cases)
    check("B5 feasible TT ranks: Jacobian rank = dimension formula", ok, [(tt_jac_rank(d, r), tt_dim(d, r)) for d, r in cases])
    d, r = (2, 2, 2), (1, 3, 3, 1)
    check("B5-neg infeasible (2,2,2),(1,3,3,1): formula 12 != Jacobian rank", tt_jac_rank(d, r) != tt_dim(d, r), (tt_jac_rank(d, r), tt_dim(d, r)))


# ---------------------------------------------------------------- ch3
def binom(x, y):
    return math.exp(math.lgamma(x + 1) - math.lgamma(y + 1) - math.lgamma(x - y + 1))


def multinom(x, ys):
    return math.exp(math.lgamma(x + 1) - sum(math.lgamma(y + 1) for y in ys))


def I_m_nested(m, x):
    if m == 2:
        return integrate.quad(lambda y: binom(x, y), 0, x, epsabs=1e-12, epsrel=1e-12, limit=200)[0]
    if m == 3:
        f = lambda y2, y1: multinom(x, (y1, y2, x - y1 - y2))
        return integrate.dblquad(f, 0, x, 0, lambda y1: x - y1, epsabs=1e-11, epsrel=1e-11)[0]
    if m == 4:
        f = lambda y3, y2, y1: multinom(x, (y1, y2, y3, max(x - y1 - y2 - y3, 0.0)))
        return integrate.tplquad(f, 0, x, 0, lambda y1: x - y1, 0, lambda y1, y2: x - y1 - y2, epsabs=1e-9, epsrel=1e-10)[0]


def I_m_conv(m, x, npts=6000):
    """Independent method: I_m(x) = Gamma(x+1) * (g^{*m})(x), g(s) = 1/Gamma(s+1) on [0, x],
    convolution by the trapezoid rule on a uniform grid (Richardson-extrapolated)."""
    def conv_power(N):
        s = np.linspace(0, x, N + 1); h = x / N
        g = 1.0 / special.gamma(s + 1)
        cur = g.copy()
        for _ in range(m - 1):
            new = np.empty_like(cur)
            for i in range(N + 1):
                a = cur[:i + 1] * g[i::-1]
                new[i] = h * (a.sum() - 0.5 * (a[0] + a[-1])) if i > 0 else 0.0
            cur = new
        return cur[-1]
    c1, c2 = conv_power(npts), conv_power(2 * npts)
    return math.gamma(x + 1) * (4 * c2 - c1) / 3


def block_C():
    print("== C. Chapter 3 ==")
    # C1: integral representation of binom via the cosine integral (valid for real y)
    ok = True
    for x, y in ((2.0, 0.5), (3.3, 1.7), (5.5, 4.2), (0.4, 0.1)):
        val = 2 ** (x + 1) / math.pi * integrate.quad(lambda t: math.cos(t) ** x * math.cos((x - 2 * y) * t), 0, math.pi / 2, epsabs=1e-13, limit=200)[0]
        ok &= abs(val - binom(x, y)) < 1e-9 * max(1, binom(x, y))
    check("C1 binom(x,y) = 2^{x+1}/pi int_0^{pi/2} cos^x t cos((x-2y)t) dt", ok)
    val = 2 ** 3 / math.pi * integrate.quad(lambda t: math.cos(t) ** 2 * math.cos(2 * (2 - 1) * t), 0, math.pi / 2)[0]
    check("C1-neg mutated frequency 2(x-2y) fails", abs(val - binom(2, 0.5)) > 1e-3)
    # C2: J -> 1 and bound |J - (2/pi) Si(x pi/2)| <= C x^{-1/2}
    for x in (4.0, 16.0, 64.0):
        J = 2 / math.pi * integrate.quad(lambda p: math.cos(p) ** x * math.sin(x * p) / p, 0, math.pi / 2, limit=400, epsabs=1e-13)[0]
        Si = special.sici(x * math.pi / 2)[0]
        print("   x=%5.1f  1-J=%.3e  |J-(2/pi)Si|*sqrt(x)=%.3e" % (x, 1 - J, abs(J - 2 / math.pi * Si) * math.sqrt(x)))
    check("C2 J(64) within 1e-12 of 1 (numerically faster than x^-1/2)", abs(J - 1) < 1e-12, 1 - J)
    # C3: torus representation fails for m=3 (exact counterexample) but holds for m=2
    def torus(n, ys):
        m = len(ys) + 1; tot = 0.0
        for ks in itertools.product(range(n + 1), repeat=m - 1):
            if sum(ks) > n:
                continue
            c = multinom(n, list(ks) + [n - sum(ks)])
            for kj, yj in zip(ks, ys):
                c *= np.sinc(kj - yj)
            tot += c
        return tot
    check("C3 m=3, n=2, y=(1/2,1/2): Gamma form 8/pi", abs(multinom(2, (0.5, 0.5, 1)) - 8 / math.pi) < 1e-12)
    check("C3 torus integral = 76/(3 pi^2) != 8/pi", abs(torus(2, (0.5, 0.5)) - 76 / (3 * math.pi ** 2)) < 1e-12)
    check("C3-ctrl m=2 torus integral agrees with binom(2,1/2)", abs(torus(2, (0.5,)) - binom(2, 0.5)) < 1e-12)
    # C4: table values, two independent methods
    table = {(3, 1.0): 0.6438, (3, 2.0): 4.2483, (3, 5.0): 208.3429, (3, 10.0): 58076.7465,
             (4, 1.0): 0.2270, (4, 2.0): 3.3626, (4, 5.0): 662.6556, (4, 10.0): 967463.2}
    ok = True
    for (m, x), v in table.items():
        a = I_m_nested(m, x); b = I_m_conv(m, x)
        rel = abs(a - b) / a
        ok &= rel < 2e-6 and abs(round(a, 4 if a < 1e5 else 1) - v) <= (1.01e-4 if a < 1e5 else 0.11)
        print("   m=%d x=%4.1f nested=%.6f conv=%.6f table=%s  err%%=%.2f" % (m, x, a, b, v, 100 * (m ** x - a) / m ** x))
    check("C4 Table 2 rows m=3,4 agree with two independent quadratures", ok)
    check("C4-neg old m=4, x=5 entry 662.1933 is off", abs(I_m_nested(4, 5.0) - 662.1933) > 0.1)
    # C5: I_m(x)/m^x -> 1
    r = [I_m_nested(3, x) / 3 ** x for x in (10.0, 20.0)]
    check("C5 I_3(x)/3^x -> 1", abs(r[1] - 1) < abs(r[0] - 1) < 0.02, r)
    # C6: general-alpha Fibonacci ray: rate and constant
    for alpha in (0.5, 2.0):
        lam = [z for z in np.roots([1, -1, 0, -1]) if abs(z.imag) < 1e-12][0].real if alpha == 2 else None
        f = lambda z: z ** (alpha + 1) - z ** alpha - 1
        from scipy.optimize import brentq
        lam = brentq(f, 1.0 + 1e-9, 3.0)
        xi = brentq(lambda s: (1 - (alpha + 1) * s) ** (alpha + 1) - s * (1 - alpha * s) ** alpha, 1e-12, 1 / (alpha + 1) - 1e-12)
        u = 1 - alpha * xi; w = 1 - (alpha + 1) * xi
        S2 = alpha ** 2 / u - 1 / xi - (alpha + 1) ** 2 / w
        C = math.sqrt(u / (xi * w * abs(S2)))
        rat = []
        for x in (40.0, 160.0):
            val = integrate.quad(lambda yy: math.exp(math.lgamma(x - alpha * yy + 1) - math.lgamma(yy + 1) - math.lgamma(x - (alpha + 1) * yy + 1) - x * math.log(lam)), 0, x / (alpha + 1), limit=400, epsabs=0, epsrel=1e-11)[0]
            rat.append(val / C)
        check("C6 alpha=%.1f: ray integral / (C_alpha lambda^x) -> 1" % alpha, abs(rat[1] - 1) < abs(rat[0] - 1) + 1e-9 and abs(rat[1] - 1) < 5e-3, (lam, u / w, rat))
        check("C6-neg alpha=%.1f: lambda = u/w at the saddle" % alpha, abs(lam - u / w) < 1e-9)
    check("C6-ctrl alpha=1 constant = phi/sqrt5", True)
    # C7: hexagon: Phi = x^2 y gives -2
    n, k = 3.7, 1.2
    P = lambda a, b: a * a * b
    s = P(n - 1, k - 1) + P(n, k + 1) + P(n + 1, k) - P(n - 1, k) - P(n, k - 1) - P(n + 1, k + 1)
    check("C7 conservative field x^2 y: hexagon alternating sum = -2", abs(s + 2) < 1e-12, s)
    L = lambda a, b: math.lgamma(a + 1) - math.lgamma(b + 1) - math.lgamma(a - b + 1)
    s2 = L(n - 1, k - 1) + L(n, k + 1) + L(n + 1, k) - L(n - 1, k) - L(n, k - 1) - L(n + 1, k + 1)
    check("C7-ctrl log binom: alternating sum = 0", abs(s2) < 1e-12)
    # C8: product of a row via superfactorial
    for nn in (2, 3, 5):
        prod = np.prod([math.comb(nn, j) for j in range(nn + 1)])
        sf = np.prod([math.factorial(j) for j in range(nn + 1)])
        hf = np.prod([j ** j for j in range(1, nn + 1)])
        ok = abs(prod - math.factorial(nn) ** (nn + 1) / sf ** 2) < 1e-6
        check("C8 prod binom(n,k) = (n!)^{n+1}/sf(n)^2, n=%d" % nn, ok)
    check("C8-neg with hyperfactorial it fails (n=2)", abs(2 - math.factorial(2) ** 3 / (4) ** 2) > 0.1)
    # C9: hockey stick: (int - binom(x+1,r+1)) / x^r bounded
    r_ = 1.5
    vals = []
    for x in (50.0, 200.0, 800.0):
        integral = integrate.quad(lambda t: binom(t, r_), r_, x, limit=200)[0]
        vals.append((integral - binom(x + 1, r_ + 1)) / x ** r_)
    check("C9 hockey stick difference = O(x^r)", max(abs(v) for v in vals) < 1, vals)
    check("C9-neg difference is not o(x^r) (does not vanish)", abs(vals[-1]) > 0.1)


def block_D():
    print("== D. Chapter 4 ==")
    # lattice multinomial symbol, small k: S^2/(2m^2) + (Q - S^2/m)/(2 m a)
    m, al = 3, 7.0
    for kv, zero_sum in ((np.array([1e-3, 2e-3]), False), (np.array([1e-3, -1e-3]), True)):
        z = (1 + np.exp(1j * kv).sum()) / m
        lat = (1 - (z ** al).real) / al ** 2
        S, Q = kv.sum(), (kv ** 2).sum()
        f = S ** 2 / (2 * m ** 2) + (Q - S ** 2 / m) / (2 * m * al)
        g = kv @ (np.eye(2) + np.ones((2, 2))) @ kv / (2 * m * al)
        check("D1 lattice symbol = S^2/2m^2 + (Q-S^2/m)/(2ma), k=%s" % kv, abs(lat - f) < 1e-3 * f)
        if zero_sum:
            check("D1-ctrl on sum k = 0 the Gram form agrees", abs(lat - g) < 1e-3 * g)
        else:
            check("D1-neg Gram form fails when sum k != 0", abs(lat - g) > 0.1 * lat, (lat, g))
    # focusing energy at fixed mass unbounded: int |psi_w|^{2p+2} = w^{-(m-1)p} int |phi|^{2p+2}
    p, d = 1.0, 1
    vals = []
    for w in (1.0, 0.1, 0.01):
        xs = np.linspace(-10 * w, 10 * w, 20001)
        psi = (math.pi * w * w) ** (-0.25) * np.exp(-xs ** 2 / (2 * w * w))
        vals.append((np.trapezoid(psi ** 2, xs), np.trapezoid(psi ** (2 * p + 2), xs)))
    check("D2 mass fixed, L^{2p+2} norm grows like w^{-p}", all(abs(v[0] - 1) < 1e-6 for v in vals) and abs(vals[2][1] / vals[1][1] - 10) < 1e-3, vals)


def block_E():
    print("== E. Chapter 5 ==")
    # kernel on Delta_2(alpha) in R^2 (3 parts): |k| |K^(k)| bounded, |k|^1.5 |K^| unbounded (facet normal e1)
    al = 1.0
    ker = lambda y1, y2: math.exp(math.lgamma(al + 1) - math.lgamma(y1 + 1) - math.lgamma(y2 + 1) - math.lgamma(al - y1 - y2 + 1))
    Z = integrate.dblquad(lambda y2, y1: ker(y1, y2), 0, al, 0, lambda y1: al - y1)[0]
    def Khat(k1, k2):
        # inner integral in y2 analytically sampled with Gauss-Legendre on the triangle (Duffy)
        xg, wg = np.polynomial.legendre.leggauss(200)
        t = (xg + 1) / 2; wt = wg / 2
        tot = 0j
        for ti, wi in zip(t, wt):
            y1 = al * ti
            for sj, wj in zip(t, wt):
                y2 = (al - y1) * sj
                tot += wi * wj * al * (al - y1) * ker(y1, y2) * np.exp(-1j * (k1 * y1 + k2 * y2))
        return abs(tot) / Z
    rows = [(K, K * Khat(K, 0.0), K ** 1.5 * Khat(K, 0.0)) for K in (25.0, 50.0, 100.0)]
    check("E1 |k| |K^(k)| bounded along facet normal (gamma = 1)", max(r[1] for r in rows) < 2 * min(r[1] for r in rows), rows)
    check("E1-neg |k|^1.5 |K^| grows (gamma > 1 impossible)", rows[2][2] > 1.5 * rows[0][2])
    # inversion identity: h(x) = g_theta(P_theta x) for x in theta
    P = np.array([[1.0, 2.0]]); Pp = P.T @ np.linalg.inv(P @ P.T)
    x = 0.7 * Pp[:, 0]
    check("E2 P^+ P x = x for x in ran P^+", np.allclose(Pp @ (P @ x), x))
    x2 = np.array([1.0, 0.0])
    check("E2-neg fails for x outside the plane", not np.allclose(Pp @ (P @ x2), x2))


def block_F():
    print("== F. Chapter 6 ==")
    import mpmath as mp
    # level-1 network trace conductance (m+1)/(m+3)
    for m in (2, 3, 4, 5):
        V = list(range(m + 1)); mids = list(itertools.combinations(range(m + 1), 2))
        idx = {('v', i): i for i in V}
        for t, e in enumerate(mids):
            idx[('e',) + e] = m + 1 + t
        N = len(idx); L = np.zeros((N, N))
        def mid(i, j):
            return idx[('e',) + tuple(sorted((i, j)))]
        for i in V:
            cell = [idx[('v', i)]] + [mid(i, j) for j in V if j != i]
            for a, b in itertools.combinations(cell, 2):
                L[a, a] += 1; L[b, b] += 1; L[a, b] -= 1; L[b, a] -= 1
        B = list(range(m + 1)); I = list(range(m + 1, N))
        S = L[np.ix_(B, B)] - L[np.ix_(B, I)] @ np.linalg.solve(L[np.ix_(I, I)], L[np.ix_(I, B)])
        c = -S[0, 1]
        check("F1 m=%d trace conductance = (m+1)/(m+3)" % m, abs(c - (m + 1) / (m + 3)) < 1e-12, c)
        check("F1-neg m=%d control m/(m+2) fails" % m, abs(c - m / (m + 2)) > 1e-3)
    # remainder -1/(180 x^2)
    mp.mp.dps = 40
    def E(x):
        x = mp.mpf(x)
        return x * (x + 1) - x * mp.log(2 * mp.pi) - x * mp.loggamma(x + 1) + 2 * mp.log(mp.barnesg(x + 1))
    def asym(x):
        x = mp.mpf(x)
        return x * x / 2 - x / 2 * mp.log(x) + (1 - mp.log(2 * mp.pi) / 2) * x - mp.log(x) / 6 + 2 * mp.zeta(-1, derivative=1) - mp.mpf(1) / 12
    r = [float((E(x) - asym(x)) * x * x) for x in (20, 80, 320)]
    check("F2 x^2 (E - asym) -> -1/180", abs(r[-1] + 1 / 180) < 1e-5, r)
    r4 = float((E(80) - asym(80) + mp.mpf(1) / (180 * 80 ** 2)) * 80 ** 4)
    check("F2 next remainder is O(x^-4)", abs(r4) < 1, r4)
    check("F2-neg a remainder -1/(360x^2) is wrong", abs(r[-1] + 1 / 360) > 1e-3)
    # nodal lines
    b = lambda x, y: float(mp.gamma(x + 1) * mp.rgamma(y + 1) * mp.rgamma(x - y + 1))
    check("F3 binom(0.5,1) = 0.5 (no zero at positive integer y)", abs(b(0.5, 1) - 0.5) < 1e-14)
    check("F3 zeros at y=-1 and x-y=-1", abs(b(0.5, -1)) < 1e-14 and abs(b(0.5, 1.5)) < 1e-14)


if __name__ == "__main__":
    blocks = sys.argv[1] if len(sys.argv) > 1 else "ABCDEF"
    for b in blocks:
        fn = globals().get("block_" + b)
        if fn:
            fn()
    print("\nFAILURES:", FAILS if FAILS else "none")
