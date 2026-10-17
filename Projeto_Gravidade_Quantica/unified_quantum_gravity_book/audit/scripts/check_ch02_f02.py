"""Shared helpers for the F-02 re-check scripts (chapters 2, 4, 5, 8, 10, 11).

claim(...) registers one numerical claim of the book together with its negative control:
the claim PASSES only if the oracle agrees with the book AND the mutated claim FAILS.
Rounding helpers: up(x) rounds a value that is used as an upper bound upwards, dn(x) rounds a
value used as a lower bound downwards (never to nearest).
"""
import math
import sys
import time

RESULTS = []      # (id, loc, status) with status in PASS / FAIL
EXPLORE = []      # (id, loc, text)
UNCHECKED = []    # (id, loc, reason)
T0 = time.time()


def up(x, d=3):
    """Round x UP to d significant digits (for upper bounds)."""
    if x == 0 or not math.isfinite(x):
        return repr(x)
    e = math.floor(math.log10(abs(x))) - d + 1
    f = 10.0 ** e
    return "%.*g" % (d, math.ceil(x / f - 1e-12) * f)


def dn(x, d=3):
    """Round x DOWN to d significant digits (for lower bounds)."""
    if x == 0 or not math.isfinite(x):
        return repr(x)
    e = math.floor(math.log10(abs(x))) - d + 1
    f = 10.0 ** e
    return "%.*g" % (d, math.floor(x / f + 1e-12) * f)


def claim(cid, loc, text, ok, info, ctrl_text, ctrl_fails, ctrl_info):
    ok = bool(ok)
    cf = bool(ctrl_fails)
    status = "PASS" if (ok and cf) else "FAIL"
    RESULTS.append((cid, loc, status, text))
    print("[%s] %s (%s) %s" % ("PASS" if ok else "FAIL", cid, loc, text))
    print("       oracle: %s" % info)
    print("[%s] %s control: %s" % ("CONTROL-OK" if cf else "CONTROL-WEAK", cid, ctrl_text))
    print("       %s" % ctrl_info)
    sys.stdout.flush()


def explore(cid, loc, text):
    EXPLORE.append((cid, loc, text))
    print("[EXPLORE] %s (%s) %s" % (cid, loc, text))
    sys.stdout.flush()


def unchecked(cid, loc, reason):
    UNCHECKED.append((cid, loc, reason))
    print("[UNCHECKED] %s (%s) %s" % (cid, loc, reason))
    sys.stdout.flush()


def finish(chapter):
    n_pass = sum(1 for r in RESULTS if r[2] == "PASS")
    n_fail = sum(1 for r in RESULTS if r[2] == "FAIL")
    print("=" * 70)
    print("Chapter %s: claims checked=%d, passed=%d, failed=%d, explore=%d, unchecked=%d, time=%.0fs"
          % (chapter, len(RESULTS), n_pass, n_fail, len(EXPLORE), len(UNCHECKED), time.time() - T0))
    for r in RESULTS:
        if r[2] == "FAIL":
            print("  FAILED: %s (%s) %s" % (r[0], r[1], r[3]))
    sys.exit(n_fail)

# ======================================================================
# Chapter 2 body.  Source: chap02_geometric_flows_tensor_varieties.tex (3.0.0)
# ======================================================================
import itertools
import numpy as np
import scipy.linalg as sla
from scipy.integrate import solve_ivp, quad
from scipy.optimize import minimize_scalar
import sympy as sp
import mpmath as mp

rng = np.random.default_rng(20261016)


def sqrtm_spd(A):
    w, V = np.linalg.eigh(A)
    return (V * np.sqrt(w)) @ V.T


def funm_spd(A, f):
    w, V = np.linalg.eigh(A)
    return (V * f(w)) @ V.T


def rand_spd(n, scale=1.0):
    M = rng.standard_normal((n, n))
    return scale * (M @ M.T / n + 0.5 * np.eye(n))


# ---------------------------------------------------------------- A. affine-invariant curvature
def riemann_sectional(G, coords, point, U, V):
    """Sectional curvature K(U,V) at `point` for metric matrix G(coords) (sympy), via
    Christoffel symbols and R^i_{jkl} = d_k Gamma^i_{lj} - d_l Gamma^i_{kj} + ... ;
    K = R_{ijkl} U^i V^j V^k U^l / (|U|^2|V|^2 - <U,V>^2)."""
    n = len(coords)
    Gi = G.inv()
    Gam = [[[sum(Gi[i, l] * (sp.diff(G[l, k], coords[j]) + sp.diff(G[l, j], coords[k])
                             - sp.diff(G[j, k], coords[l])) for l in range(n)) / 2
             for k in range(n)] for j in range(n)] for i in range(n)]
    sub = dict(zip(coords, point))
    Gam_num = [[[sp.nsimplify(Gam[i][j][k].subs(sub)) for k in range(n)] for j in range(n)] for i in range(n)]
    Rm = {}
    Rup = [[[[0] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    t = sp.diff(Gam[i][l][j], coords[k]) - sp.diff(Gam[i][k][j], coords[l])
                    t = t.subs(sub)
                    t += sum(Gam_num[i][k][m] * Gam_num[m][l][j] - Gam_num[i][l][m] * Gam_num[m][k][j]
                             for m in range(n))
                    Rup[i][j][k][l] = t
    Gn = G.subs(sub)
    num = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    Rl = sum(Gn[i, m] * Rup[m][j][k][l] for m in range(n))
                    num += Rl * U[i] * V[j] * U[k] * V[l]
    uu = (sp.Matrix(U).T * Gn * sp.Matrix(U))[0]
    vv = (sp.Matrix(V).T * Gn * sp.Matrix(V))[0]
    uv = (sp.Matrix(U).T * Gn * sp.Matrix(V))[0]
    return sp.N(num / (uu * vv - uv ** 2), 30)


def section_A():
    # convention sanity: unit 2-sphere must give +1
    th, ph = sp.symbols("theta phi")
    Gs = sp.diag(1, sp.sin(th) ** 2)
    Ks = riemann_sectional(Gs, [th, ph], [sp.Rational(7, 10), sp.Rational(1, 3)], [1, 0], [0, 1])
    sph_ok = abs(float(Ks) - 1.0) < 1e-9

    a, b, c = sp.symbols("a b c", positive=True)
    A = sp.Matrix([[a, b], [b, c]])
    Ai = A.inv()
    E = [sp.Matrix([[1, 0], [0, 0]]), sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, 0], [0, 1]])]
    G = sp.Matrix(3, 3, lambda i, j: (Ai * E[i] * Ai * E[j]).trace())
    maxerr = 0.0
    maxerr_m = 0.0
    maxerr_p = 0.0
    kmax = -1.0
    tests = [([sp.Rational(5, 2), sp.Rational(1, 3), sp.Rational(7, 4)], [1, 0, 0], [0, 1, 0]),
             ([sp.Rational(3, 2), sp.Rational(-1, 2), sp.Rational(5, 3)], [1, sp.Rational(1, 2), -1], [0, 1, 2]),
             ([sp.Rational(2), sp.Rational(1, 5), sp.Rational(9, 4)], [2, -1, 1], [-1, 1, 3])]
    for pt, Uc, Vc in tests:
        Kexact = float(riemann_sectional(G, [a, b, c], pt, Uc, Vc))
        An = np.array([[float(pt[0]), float(pt[1])], [float(pt[1]), float(pt[2])]])
        Un = np.array([[float(Uc[0]), float(Uc[1])], [float(Uc[1]), float(Uc[2])]])
        Vn = np.array([[float(Vc[0]), float(Vc[1])], [float(Vc[1]), float(Vc[2])]])
        Ais = funm_spd(An, lambda w: w ** -0.5)
        Ut, Vt = Ais @ Un @ Ais, Ais @ Vn @ Ais
        comm = Ut @ Vt - Vt @ Ut
        Aiv = np.linalg.inv(An)
        gUU = np.trace(Aiv @ Un @ Aiv @ Un)
        gVV = np.trace(Aiv @ Vn @ Aiv @ Vn)
        gUV = np.trace(Aiv @ Un @ Aiv @ Vn)
        den = gUU * gVV - gUV ** 2
        Kform = -0.25 * np.sum(comm ** 2) / den
        maxerr = max(maxerr, abs(Kform - Kexact))
        maxerr_m = max(maxerr_m, abs(-0.5 * np.sum(comm ** 2) / den - Kexact))
        maxerr_p = max(maxerr_p, abs(+0.25 * np.sum(comm ** 2) / den - Kexact))
        kmax = max(kmax, Kexact)
    claim("C2.1", "chap02.tex:159-163 (Thm cone_curvature)",
          "sectional curvature K(U,V) = -(1/4)||[U~,V~]||_F^2/(g(U,U)g(V,V)-g(U,V)^2) <= 0 on S_{++}^2",
          sph_ok and maxerr < 1e-9 and kmax <= 1e-12,
          "sympy Christoffel/Riemann in coordinates (a,b,c) at 3 rational points (convention checked: unit S^2 gives +1); "
          "max |K_formula - K_riemann| = %s, max K_riemann = %s" % (up(maxerr, 2), up(max(kmax, 0.0), 2)),
          "coefficient -1/2 or +1/4 instead of -1/4 must disagree",
          maxerr_m > 1e-3 and maxerr_p > 1e-3,
          "max error with -1/2: %s ; with +1/4: %s" % (dn(maxerr_m, 2), dn(maxerr_p, 2)))

    # commuting case => K = 0 (equality case) : diagonal U, V at diagonal A
    Kc = float(riemann_sectional(G, [a, b, c], [sp.Rational(2), sp.Rational(0), sp.Rational(3)], [1, 0, 0], [0, 0, 1]))
    claim("C2.1b", "chap02.tex:159-163", "K = 0 exactly when U~, V~ commute (diagonal example)",
          abs(Kc) < 1e-12, "Riemann curvature of the diagonal 2-plane = %s" % up(abs(Kc), 2),
          "a non-commuting pair must give K strictly negative",
          kmax < -1e-3,
          "DECLARED: the control reuses the data of C2.1 (non-commuting pairs); "
          "largest K = %s" % up(kmax, 2))


def section_A2():
    A = rand_spd(3)
    B = rand_spd(3)
    Ah = sqrtm_spd(A)
    Ahi = np.linalg.inv(Ah)
    Mfun = Ahi @ B @ Ahi

    def gam(t):
        return Ah @ funm_spd(Mfun, lambda w: w ** t) @ Ah

    h = 1e-4
    res = 0.0
    for t in (0.2, 0.5, 0.8):
        g0, gp, gm = gam(t), gam(t + h), gam(t - h)
        g1 = (gp - gm) / (2 * h)
        g2 = (gp - 2 * g0 + gm) / h ** 2
        res = max(res, np.linalg.norm(g2 - g1 @ np.linalg.inv(g0) @ g1) / np.linalg.norm(g2))
    # control: straight line is not a geodesic
    resl = 0.0
    for t in (0.2, 0.5, 0.8):
        g0 = (1 - t) * A + t * B
        g1 = B - A
        g2 = np.zeros_like(A)
        resl = max(resl, np.linalg.norm(g2 - g1 @ np.linalg.inv(g0) @ g1) / np.linalg.norm(g1))
    # length of the curve in g^AI equals ||log(A^-1/2 B A^-1/2)||_F
    def speed(t):
        g0 = gam(t)
        d = (gam(t + 1e-6) - gam(t - 1e-6)) / 2e-6
        gi = np.linalg.inv(g0)
        return np.sqrt(np.trace(gi @ d @ gi @ d))
    L = quad(speed, 0, 1, epsabs=1e-9, epsrel=1e-9)[0]
    dAI = np.linalg.norm(funm_spd(Mfun, np.log), "fro")
    claim("C2.2", "chap02.tex:165-168 (eq cone_geodesic)",
          "gamma(t)=A^{1/2}(A^{-1/2}BA^{-1/2})^t A^{1/2} solves gamma'' = gamma' gamma^{-1} gamma' with gamma(0)=A, gamma(1)=B",
          res < 1e-5 and np.allclose(gam(0), A) and np.allclose(gam(1), B) and abs(L - dAI) < 1e-6,
          "central second differences (h=1e-4): max relative ODE residual = %s; metric length by quadrature %s vs ||log||_F %s"
          % (up(res, 2), up(L, 8), up(dAI, 8)),
          "the straight segment (1-t)A+tB must violate the geodesic equation",
          resl > 1e-2, "relative residual of the straight line = %s" % dn(resl, 2))


# ---------------------------------------------------------------- B. Bures-Wasserstein
def section_B():
    # 1D normalisation: g(u,u)=u^2/(4a) and d^2 = (sqrt a - sqrt b)^2 ; length of a(t) between a,b
    a, b = 0.7, 2.9
    length = quad(lambda s: 1 / (2 * np.sqrt(s)), a, b)[0]   # integral of sqrt(u^2/(4s)) = 1/(2 sqrt s)
    d2_1d = (np.sqrt(a) - np.sqrt(b)) ** 2
    S1 = sla.solve_continuous_lyapunov(np.array([[a]]), np.array([[1.0]]))[0, 0]
    g1 = 0.5 * S1 * 1.0
    # n x n : OT geodesic length vs formula vs Procrustes
    maxd = 0.0
    maxproc = 0.0
    for n in (2, 3):
        A, B = rand_spd(n), rand_spd(n)
        Ah = sqrtm_spd(A)
        Ahi = np.linalg.inv(Ah)
        C = sqrtm_spd(Ah @ B @ Ah)
        d2 = np.trace(A) + np.trace(B) - 2 * np.trace(C)
        T = Ahi @ C @ Ahi

        def speed(t):
            M = (1 - t) * np.eye(n) + t * T
            At = M @ A @ M
            Ad = (T - np.eye(n)) @ A @ M + M @ A @ (T - np.eye(n))
            S = sla.solve_continuous_lyapunov(At, Ad)
            return np.sqrt(0.5 * np.trace(S @ Ad))
        Lg = quad(speed, 0, 1, epsabs=1e-10, epsrel=1e-10)[0]
        maxd = max(maxd, abs(Lg ** 2 - d2))
        Bh = sqrtm_spd(B)
        nuc = np.linalg.svd(Bh @ Ah, compute_uv=False).sum()
        maxproc = max(maxproc, abs(d2 - (np.trace(A) + np.trace(B) - 2 * nuc)))
    # brute-force minimisation over O(2) for n=2 (independent of the formula)
    A, B = rand_spd(2), rand_spd(2)
    Ah, Bh = sqrtm_spd(A), sqrtm_spd(B)
    best = 1e9
    for refl in (1, -1):
        for th in np.linspace(0, 2 * np.pi, 20001):
            R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]]) @ np.diag([1, refl])
            best = min(best, np.linalg.norm(Ah - Bh @ R) ** 2)
    d2f = np.trace(A) + np.trace(B) - 2 * np.trace(sqrtm_spd(Ah @ B @ Ah))
    claim("C2.3", "chap02.tex:185-192 (Bures-Wasserstein)",
          "g^BW(U,V)=(1/2)Tr(S_A(U)V) gives u^2/(4a) in 1D and its geodesic length equals d_BW, d_BW^2 = TrA+TrB-2Tr((A^1/2 B A^1/2)^1/2)",
          abs(g1 - 1 / (4 * a)) < 1e-12 and abs(length ** 2 - d2_1d) < 1e-10 and maxd < 1e-8 and maxproc < 1e-10 and abs(best - d2f) < 1e-6,
          "1D: g=%s vs 1/(4a)=%s, length^2 %s vs d^2 %s; n=2,3: |length^2-d^2|<=%s along the optimal-transport path with the Lyapunov metric; "
          "brute-force min over O(2) of ||A^1/2-B^1/2 O||^2 = %s vs formula %s"
          % (up(g1, 8), up(1 / (4 * a), 8), up(length ** 2, 8), up(d2_1d, 8), up(maxd, 2), up(best, 7), up(d2f, 7)),
          "the normalisation g = Tr(S U) (without 1/2) must give a length differing from d_BW by factor sqrt(2)",
          abs(np.sqrt(2) * length - abs(np.sqrt(a) - np.sqrt(b))) > 0.1,
          "with the unhalved metric the 1D line element becomes u^2/(2a), length x sqrt(2) = %s vs d = %s"
          % (up(np.sqrt(2) * length, 6), up(abs(np.sqrt(a) - np.sqrt(b)), 6)))


# ---------------------------------------------------------------- C. fixed rank
def section_C():
    rows = []
    allok = True
    ctrl_all = True
    maxproj = 0.0
    minctrl = 1e9
    for (m, n, r) in [(5, 4, 2), (6, 6, 3), (4, 7, 1), (7, 5, 4)]:
        U = rng.standard_normal((m, r))
        S = rng.standard_normal((r, r))
        V = rng.standard_normal((n, r))
        cols = []
        for i in range(m):
            for j in range(r):
                dU = np.zeros((m, r)); dU[i, j] = 1
                cols.append((dU @ S @ V.T).ravel())
        for i in range(r):
            for j in range(r):
                dS = np.zeros((r, r)); dS[i, j] = 1
                cols.append((U @ dS @ V.T).ravel())
        for i in range(n):
            for j in range(r):
                dV = np.zeros((n, r)); dV[i, j] = 1
                cols.append((U @ S @ dV.T).ravel())
        J = np.array(cols).T
        sv = np.linalg.svd(J, compute_uv=False)
        rank = int((sv > 1e-9 * sv[0]).sum())
        dim = r * (m + n - r)
        allok &= (rank == dim)
        rows.append("(m,n,r)=(%d,%d,%d): Jacobian rank %d vs r(m+n-r)=%d" % (m, n, r, rank, dim))
        # projection formula against a least-squares projector onto the Jacobian column space
        A = U @ S @ V.T
        Uo, so, Vot = np.linalg.svd(A)
        Uo = Uo[:, :r]; Vo = Vot[:r].T
        Q, _ = np.linalg.qr(J[:, :], mode="reduced")
        # orthonormal basis of the column space with rank trimmed
        u, s, vt = np.linalg.svd(J, full_matrices=False)
        Bq = u[:, :rank]
        Z = rng.standard_normal((m, n))
        P_ls = (Bq @ (Bq.T @ Z.ravel())).reshape(m, n)
        P_formula = Uo @ Uo.T @ Z + Z @ Vo @ Vo.T - Uo @ Uo.T @ Z @ Vo @ Vo.T
        P_wrong = Uo @ Uo.T @ Z + Z @ Vo @ Vo.T
        maxproj = max(maxproj, np.linalg.norm(P_ls - P_formula))
        minctrl = min(minctrl, np.linalg.norm(P_ls - P_wrong))
    claim("C2.4", "chap02.tex:199-217 (Prop tangent_proj_mr)",
          "dim T_A M_r = r(m+n-r) and P(Z)=UU^TZ+ZVV^T-UU^TZVV^T is the orthogonal projector onto T_A M_r",
          allok and maxproj < 1e-10,
          "; ".join(rows) + "; max ||P_formula - P_leastsquares|| = %s" % up(maxproj, 2),
          "dropping the correction term -UU^T Z VV^T must change the projection",
          minctrl > 1e-3, "min distance of the mutated projector to the true one = %s" % dn(minctrl, 2))


# ---------------------------------------------------------------- D. tensor train
def tt_contract(cores):
    T = cores[0]
    for G in cores[1:]:
        T = np.tensordot(T, G, axes=([T.ndim - 1], [0]))
    return T.reshape([c.shape[1] for c in cores])


def tt_jacobian(cores):
    cols = []
    for a, G in enumerate(cores):
        for idx in np.ndindex(*G.shape):
            E = np.zeros_like(G); E[idx] = 1
            cs = list(cores); cs[a] = E
            cols.append(tt_contract(cs).ravel())
    return np.array(cols).T


def unfold(T, a):
    return T.reshape(int(np.prod(T.shape[:a])), -1)


def section_D():
    cfgs = [((2, 3, 2), (1, 2, 2, 1)), ((3, 3, 3, 3), (1, 2, 3, 2, 1)), ((2, 2, 2, 2, 2), (1, 2, 2, 2, 2, 1)),
            ((4, 3, 5), (1, 3, 4, 1))]
    rows = []
    okd = True
    for d, r in cfgs:
        cores = [rng.standard_normal((r[i], d[i], r[i + 1])) for i in range(len(d))]
        J = tt_jacobian(cores)
        sv = np.linalg.svd(J, compute_uv=False)
        rank = int((sv > 1e-9 * sv[0]).sum())
        k = len(d)
        formula = sum(d[i] * r[i] * r[i + 1] for i in range(k)) - sum(r[i] ** 2 for i in range(1, k))
        okd &= (rank == formula)
        rows.append("d=%s r=%s: rank %d vs %d" % (d, r, rank, formula))
    # uniform dimensions formula 2dr + (k-2)dr^2 - (k-1)r^2
    d, r, k = 3, 2, 5
    uni = 2 * d * r + (k - 2) * d * r * r - (k - 1) * r * r
    gen = sum(d * (1 if i == 0 else r) * (1 if i == k - 1 else r) for i in range(k)) - sum(r * r for _ in range(k - 1))
    okd &= (uni == gen)
    # control: raw parameter count (no gauge subtraction) differs
    cores = [rng.standard_normal((cfgs[1][1][i], cfgs[1][0][i], cfgs[1][1][i + 1])) for i in range(4)]
    raw = sum(c.size for c in cores)
    claim("C2.5", "chap02.tex:235-240 (Thm tt_manifold, eq tt_dim)",
          "dim M_r^TT = sum d_a r_{a-1} r_a - sum r_a^2 (and the uniform form 2dr+(k-2)dr^2-(k-1)r^2)",
          okd, "; ".join(rows) + "; uniform formula (d=3,r=2,k=5) %d vs general %d" % (uni, gen),
          "raw parameter count without the gauge term must overestimate the Jacobian rank",
          raw > int((np.linalg.svd(tt_jacobian(cores), compute_uv=False) > 1e-9).sum()),
          "raw count %d vs Jacobian rank of the 4-core case" % raw)

    # feasibility: d=(2,2,2), r=(1,3,3,1) is infeasible; iff-test on tensors of shape (2,3,2) with random sparse ranks
    def feasible(d, r):
        k = len(d)
        return all(r[a] <= min(r[a - 1] * d[a - 1], d[a] * r[a + 1]) for a in range(1, k))
    inf_ok = (not feasible((2, 2, 2), (1, 3, 3, 1)))
    # R2: d=(3,1,3).  Here the coupling inequalities force r1 = r2 (both unfoldings are the same 3x3 matrix up to transposition),
    # so the pairs (2,1),(1,2),(3,2) fit the unfolding SHAPES (r_a <= min(prod_{b<=a} d_b, prod_{b>a} d_b) = 3) but are infeasible.
    d = (3, 1, 3)
    seen = set()
    # (i) generic tensors of exact TT-rank (1,r1,r2,1) built from random cores, for every pair with shape bound r<=3 (the sufficiency direction)
    built = {}
    for r1 in range(1, 4):
        for r2 in range(1, 4):
            # cores of ranks (1,r1,r2,1) for d=(3,1,3): the cores always exist, but the tensor may have smaller unfolding ranks
            cs = [rng.standard_normal((1, 3, r1)), rng.standard_normal((r1, 1, r2)), rng.standard_normal((r2, 3, 1))]
            T = tt_contract(cs)
            built[(r1, r2)] = (np.linalg.matrix_rank(unfold(T, 1)), np.linalg.matrix_rank(unfold(T, 2)))
    for pair in built.values():
        seen.add(pair)
    # (ii) structured / sparse / low-rank tensors, many draws
    for _ in range(4000):
        mode = rng.integers(0, 3)
        T = np.zeros(d)
        if mode == 0:
            for _ in range(rng.integers(1, 5)):
                T += np.einsum("i,j,k->ijk", rng.standard_normal(3), rng.standard_normal(1), rng.standard_normal(3))
        elif mode == 1:
            T = np.einsum("ij,k->ijk", rng.standard_normal((3, 1)) * (rng.random((3, 1)) < 0.5), rng.standard_normal(3))
        else:
            T = rng.standard_normal(d) * (rng.random(d) < 0.4)
        seen.add((int(np.linalg.matrix_rank(unfold(T, 1))), int(np.linalg.matrix_rank(unfold(T, 2)))))
    feas = {(a, b) for a in range(0, 5) for b in range(0, 5)
            if a == 0 and b == 0 or (a >= 1 and b >= 1 and feasible(d, (1, a, b, 1)))}
    # shape-only bound (the mutant: no coupling r_a <= r_{a-1} d_a, i.e. only r_a <= min(prod d_b))
    shape_only = {(a, b) for a in range(0, 4) for b in range(0, 4) if a <= 3 and b <= 3}
    feas_pos = {p for p in feas if p != (0, 0)}
    seen_pos = {p for p in seen if p != (0, 0)}
    feas_pos_small = {p for p in feas_pos if p[0] <= 3}
    eq_ok = (seen_pos == feas_pos_small)   # both directions: every feasible pair occurs, only feasible pairs occur
    mut_admits = {(2, 1), (1, 2), (3, 2)}
    claim("C2.6", "chap02.tex:226-232 (eq tt_feasible, example d=(2,2,2), r=(1,3,3,1))",
          "M_r^TT non-empty iff r_a <= min(r_{a-1}d_a, d_{a+1}r_{a+1}); (2,2,2),(1,3,3,1) is not feasible",
          inf_ok and eq_ok,
          "d=(3,1,3): feasible pairs (coupling forces r1=r2) %s; pairs observed (4000 structured tensors + generic cores for all 9 core-rank pairs) %s; "
          "seen == feasible in BOTH directions: %s. (2,2,2),(1,3,3,1): first unfolding is 2x4 so rank<=2<3."
          % (sorted(feas_pos_small), sorted(seen_pos), eq_ok),
          "mutant 'no coupling, shape bounds only' admits (2,1),(1,2),(3,2) (they fit the 3x3 unfoldings); none of them is ever observed",
          all(m in shape_only and m not in seen_pos and not feasible(d, (1,) + m + (1,)) for m in mut_admits),
          "mutant-admitted pairs %s observed: %s" % (sorted(mut_admits), [m in seen_pos for m in sorted(mut_admits)]))

    # tangent projection formula (alternating sum), k=3
    d = (2, 3, 4)
    r = (1, 2, 3, 1)
    cores = [rng.standard_normal((r[i], d[i], r[i + 1])) for i in range(3)]
    T = tt_contract(cores)
    J = tt_jacobian(cores)
    u, s, vt = np.linalg.svd(J, full_matrices=False)
    rk = int((s > 1e-9 * s[0]).sum())
    Bq = u[:, :rk]
    Z = rng.standard_normal(d)

    def colproj(M):
        uu, ss, _ = np.linalg.svd(M, full_matrices=False)
        uu = uu[:, :(ss > 1e-10).sum()]
        return uu @ uu.T

    def rowproj(M):
        _, ss, vv = np.linalg.svd(M, full_matrices=False)
        vv = vv[:(ss > 1e-10).sum()]
        return vv.T @ vv
    P_le = {0: np.eye(1), 1: colproj(unfold(T, 1)), 2: colproj(unfold(T, 2)), 3: np.eye(1)}
    P_ge = {1: rowproj(unfold(T, 1)), 2: rowproj(unfold(T, 2)), 3: np.eye(1), 4: np.eye(1)}
    # P_{>=a+1} projects R^{d_{a+1}...d_k}; for a=0 it is the projector for index set starting at 1: identity of that size
    def apply(Z, a, with_mid):
        # Z indices (i1,i2,i3); left block = first a-1 indices (or first a if LR), mid = index a, right = after
        sh = Z.shape
        if with_mid:   # P^L_a = P_{<=a-1} (x) Id_{d_a} (x) P_{>=a+1}
            L = int(np.prod(sh[:a - 1])) if a > 1 else 1
            R = int(np.prod(sh[a:])) if a < len(sh) else 1
            M = Z.reshape(L, sh[a - 1], R)
            PL = P_le[a - 1] if a - 1 >= 1 else np.eye(1)
            PR = P_ge[a] if a < len(sh) else np.eye(1)
            return np.einsum("ij,jkl,lm->ikm", PL, M, PR.T).reshape(sh)
        else:          # P^LR_a = P_{<=a} (x) P_{>=a+1}
            L = int(np.prod(sh[:a])); R = int(np.prod(sh[a:]))
            M = Z.reshape(L, R)
            return (P_le[a] @ M @ P_ge[a].T).reshape(sh)
    Pf = sum(apply(Z, a, True) for a in (1, 2, 3)) - sum(apply(Z, a, False) for a in (1, 2))
    Pls = (Bq @ (Bq.T @ Z.ravel())).reshape(d)
    Pbad = sum(apply(Z, a, True) for a in (1, 2, 3))
    claim("C2.7", "chap02.tex:257-270 (Thm tt_tangent_proj, eq tt_proj_formula)",
          "orthogonal projector on T M_r^TT equals sum_a P^L_a - sum_a P^LR_a (k=3, d=(2,3,4), r=(1,2,3,1))",
          np.linalg.norm(Pf - Pls) < 1e-9,
          "Jacobian tangent space rank %d; ||P_formula Z - P_leastsquares Z|| = %s" % (rk, up(np.linalg.norm(Pf - Pls), 2)),
          "omitting the subtracted LR terms must break the formula",
          np.linalg.norm(Pbad - Pls) > 1e-3, "distance without LR terms = %s" % dn(np.linalg.norm(Pbad - Pls), 2))


# ---------------------------------------------------------------- E. Toda
def pi_so(X):
    L = np.tril(X, -1)
    return L - L.T


def qr_pos(X):
    Q, R = np.linalg.qr(X)
    D = np.sign(np.diag(R)); D[D == 0] = 1
    return Q * D, D[:, None] * R


def section_E():
    n = 5
    M = rng.standard_normal((n, n)); A0 = (M + M.T) / 2

    def rhs(t, y):
        A = y[:n * n].reshape(n, n); Q = y[n * n:].reshape(n, n)
        P = pi_so(A)
        return np.concatenate([(A @ P - P @ A).ravel(), (Q @ P).ravel()])
    y0 = np.concatenate([A0.ravel(), np.eye(n).ravel()])
    sol = solve_ivp(rhs, [0, 3.0], y0, method="DOP853", rtol=1e-12, atol=1e-13, t_eval=[0.7, 1.0, 2.0, 3.0])
    err_iso = err_qr = err_Q = err_step = 0.0
    err_wrong = 1e9
    for idx, t in enumerate(sol.t):
        A = sol.y[:n * n, idx].reshape(n, n); Qk = sol.y[n * n:, idx].reshape(n, n)
        Qr, Rr = qr_pos(sla.expm(t * A0))
        err_iso = max(err_iso, np.max(np.abs(np.sort(np.linalg.eigvalsh(A)) - np.sort(np.linalg.eigvalsh(A0)))))
        err_qr = max(err_qr, np.max(np.abs(A - Qr.T @ A0 @ Qr)))
        err_Q = max(err_Q, np.max(np.abs(Qk - Qr)))
        if abs(t - 1.0) < 1e-12:
            Q1, R1 = qr_pos(sla.expm(A))      # QR of e^{A(1)}? check e^{A(1)} = R(1) Q(1)
            err_step = np.max(np.abs(sla.expm(A) - Rr @ Qr))
        Qw, _ = qr_pos(t * A0 + 5 * np.eye(n))      # mutated: QR of a linear matrix instead of exp(tA0)
        err_wrong = min(err_wrong, np.max(np.abs(A - Qw.T @ A0 @ Qw)))
    claim("C2.8", "chap02.tex:302-316 (Thm toda_qr)",
          "Toda flow is isospectral, A(t)=Q(t)^T A0 Q(t) with exp(tA0)=Q R (R_ii>0), Q solves Q'=Q Pi_so(A), and e^{A(1)}=R(1)Q(1)",
          err_iso < 1e-9 and err_qr < 1e-8 and err_Q < 1e-8 and err_step < 1e-8,
          "DOP853 (rtol 1e-12) vs scipy expm+QR: eig error %s, |A_ode - Q^T A0 Q| %s, |Q_ode - Q_qr| %s, |e^{A(1)} - R Q| %s"
          % (up(err_iso, 2), up(err_qr, 2), up(err_Q, 2), up(err_step, 2)),
          "QR of tA0+5I (instead of exp(tA0)) must not reproduce the ODE solution",
          err_wrong > 1e-3, "min mismatch with the wrong QR = %s" % dn(err_wrong, 2))

    # off-diagonal mass: tends to 0 (distinct eigenvalues) and is NOT monotone for some data
    found = None
    nonmono = 0
    tends = True
    for seed in range(60):
        g = np.random.default_rng(1000 + seed)
        Mm = g.standard_normal((4, 4)); B0 = (Mm + Mm.T) / 2

        def rh(t, y):
            A = y.reshape(4, 4); P = pi_so(A)
            return (A @ P - P @ A).ravel()
        ts = np.linspace(0, 12, 481)
        so = solve_ivp(rh, [0, 12], B0.ravel(), method="DOP853", rtol=1e-11, atol=1e-12, t_eval=ts)
        off = [np.linalg.norm(y.reshape(4, 4) - np.diag(np.diag(y.reshape(4, 4)))) for y in so.y.T]
        if np.any(np.diff(off) > 1e-9):
            nonmono += 1
            if found is None:
                found = seed
        tends &= (off[-1] < 1e-3 * off[0] + 1e-6) or (off[-1] < 5e-2)
    claim("C2.9", "chap02.tex:709-722 (Table, QR row: off-diagonal mass -> 0, not monotone)",
          "for the Toda flow the off-diagonal Frobenius mass tends to 0 but is not monotone in general",
          nonmono > 0,
          "60 random symmetric 4x4 initial data: %d show an increase of the off-diagonal norm (first seed index %s)"
          % (nonmono, found),
          "the claim 'monotone for every datum' must fail",
          nonmono > 0, "counter-examples to monotonicity exist: %d of 60" % nonmono)
    explore("C2.9b", "chap02.tex:709-722", "off-diagonal norm at t=12 below 5e-2 for all 60 data: %s" % tends)


# ---------------------------------------------------------------- F. projected gradient on M_r
def section_F():
    # explicit example: L(A)=<C,A>, A0=C=E11
    E11 = np.zeros((2, 2)); E11[0, 0] = 1
    C = E11.copy()

    def proj(A, Z, r):
        U, s, Vt = np.linalg.svd(A)
        U = U[:, :r]; V = Vt[:r].T
        return U @ U.T @ Z + Z @ V @ V.T - U @ U.T @ Z @ V @ V.T

    def rhs(t, y):
        A = y.reshape(2, 2)
        return (-proj(A, C, 1)).ravel()
    sol = solve_ivp(rhs, [0, 0.99], E11.ravel(), method="DOP853", rtol=1e-12, atol=1e-14, t_eval=[0.5, 0.9, 0.99])
    errs = [abs(sol.y[0, i] - (1 - t)) + abs(sol.y[1:, i]).max() for i, t in enumerate(sol.t)]
    sig = [np.linalg.svd(sol.y[:, i].reshape(2, 2), compute_uv=False)[0] for i in range(3)]
    # random strongly non-trivial loss: energy decay identity dL/dt = -||P grad||^2
    m, n, r = 5, 4, 2
    Bt = rng.standard_normal((m, n))
    U0, s0, V0t = np.linalg.svd(rng.standard_normal((m, n)))
    A0 = (U0[:, :r] * s0[:r]) @ V0t[:r]
    L = lambda A: 0.5 * np.linalg.norm(A - Bt) ** 2

    def rhs2(t, y):
        A = y.reshape(m, n)
        return (-proj(A, A - Bt, r)).ravel()
    ts = np.linspace(0, 3, 301)
    sol2 = solve_ivp(rhs2, [0, 3], A0.ravel(), method="DOP853", rtol=1e-11, atol=1e-13, t_eval=ts)
    Ls = np.array([L(y.reshape(m, n)) for y in sol2.y.T])
    gP = np.array([np.linalg.norm(proj(y.reshape(m, n), y.reshape(m, n) - Bt, r)) ** 2 for y in sol2.y.T])
    gF = np.array([np.linalg.norm(y.reshape(m, n) - Bt) ** 2 for y in sol2.y.T])
    # integrate by Simpson
    from scipy.integrate import simpson
    drop = Ls[0] - Ls[-1]
    intP = simpson(gP, x=ts)
    intF = simpson(gF, x=ts)
    rk_drift = max(np.linalg.svd(y.reshape(m, n), compute_uv=False)[r] for y in sol2.y.T)
    claim("C2.10", "chap02.tex:362-392 (Thm rank_preservation; example A(t)=(1-t)E11, T*=1)",
          "for L=<C,A>, A0=C=E11 the projected flow is A(t)=(1-t)E11 (T*=1); in general rank stays r, dL/dt=-||P grad L||^2<=0",
          max(errs) < 1e-9 and abs(sig[-1] - 0.01) < 1e-8 and abs(drop - intP) < 1e-6 and rk_drift < 1e-7 and np.all(np.diff(Ls) <= 1e-12),
          "DOP853: |A(t)-(1-t)E11| <= %s at t=0.5,0.9,0.99 (sigma_1(0.99)=%s); random case (5x4, r=2): L-drop %s vs int ||P grad||^2 %s; "
          "sigma_{r+1} stays <= %s; L non-increasing"
          % (up(max(errs), 2), up(sig[-1], 6), up(drop, 8), up(intP, 8), up(rk_drift, 2)),
          "the full-gradient dissipation int ||grad L||^2 must NOT equal the observed drop",
          abs(drop - intF) > 1e-3, "int ||grad L||^2 = %s vs drop %s" % (up(intF, 6), up(drop, 6)))


# ---------------------------------------------------------------- G. graphon heat
def section_G():
    n = 6
    W0 = rng.random((n, n)); W0 = (W0 + W0.T) / 2

    def Delta(W):
        d1 = W.mean(axis=1)[:, None] * np.ones((1, n))
        d2 = np.ones((n, 1)) * W.mean(axis=0)[None, :]
        return d1 + d2 - 2 * W
    D = np.zeros((n * n, n * n))
    for i in range(n * n):
        e = np.zeros(n * n); e[i] = 1
        D[:, i] = Delta(e.reshape(n, n)).ravel()
    errs = 0.0
    errw = 1e9
    for t in (0.1, 0.7, 2.0, 5.0):
        Wn = (sla.expm(t * D) @ W0.ravel()).reshape(n, n)
        d1 = W0.mean(axis=1)[:, None]; d2 = W0.mean(axis=0)[None, :]; m = W0.mean()
        Wc = np.exp(-2 * t) * W0 + (np.exp(-t) - np.exp(-2 * t)) * (d1 + d2) + (1 - np.exp(-t)) ** 2 * m
        errs = max(errs, np.max(np.abs(Wn - Wc)))
        Ww = np.exp(-2 * t) * W0 + (1 - np.exp(-2 * t)) / 2 * (d1 + d2) + (1 - np.exp(-t)) ** 2 * m
        errw = min(errw, np.max(np.abs(Wn - Ww)))
    tt = sp.symbols("t", positive=True)
    ssum = sp.simplify(sp.exp(-2 * tt) + 2 * (sp.exp(-tt) - sp.exp(-2 * tt)) + (1 - sp.exp(-tt)) ** 2)
    claim("C2.11", "chap02.tex:441-447 (eq graphon_heat_exact)",
          "e^{t Delta_x} W0 = e^{-2t}W0 + (e^{-t}-e^{-2t})(d1+d2) + (1-e^{-t})^2 m, coefficients sum to 1",
          errs < 1e-12 and ssum == 1,
          "scipy expm of the discretised generator (6x6 cells) vs closed form: max error %s; sympy sum of coefficients = %s"
          % (up(errs, 2), ssum),
          "replacing (e^{-t}-e^{-2t}) by (1-e^{-2t})/2 must disagree with expm",
          errw > 1e-3, "min mismatch with the mutated coefficient = %s" % dn(errw, 2))

    # cut norm contraction, exact brute force
    def cutnorm(W):
        nn = W.shape[0]
        best = 0.0
        for mask in range(1 << nn):
            S = np.array([(mask >> i) & 1 for i in range(nn)], dtype=bool)
            c = W[S].sum(axis=0)
            best = max(best, np.maximum(c, 0).sum(), np.maximum(-c, 0).sum())
        return best / nn ** 2
    worst = 0.0
    worst_ratio_ok = True
    ratio_min = 1e9
    for trial in range(60):
        Wr = rng.standard_normal((n, n)) if trial % 2 else rng.random((n, n))
        Wr = (Wr + Wr.T) / 2
        c0 = cutnorm(Wr)
        for t in (0.05, 0.4, 1.5):
            Wt = (sla.expm(t * D) @ Wr.ravel()).reshape(n, n)
            worst = max(worst, cutnorm(Wt) - c0)
    Wc0 = np.ones((n, n)) * 0.6
    ratio_c = cutnorm((sla.expm(0.05 * D) @ Wc0.ravel()).reshape(n, n)) / cutnorm(Wc0)
    claim("C2.12", "chap02.tex:454-466 (Thm heat_smoothing (i))",
          "cut norm is non-increasing along the graphon heat flow: ||W(t)||_cut <= ||W0||_cut",
          worst <= 1e-12,
          "exact cut norm by enumeration of all 2^6 row subsets, 60 random symmetric 6x6 data, t in {0.05,0.4,1.5}: max (||W(t)||-||W0||) = %s"
          % up(worst, 2),
          "the mutated contraction ||W(t)|| <= 0.9||W0|| at t=0.05 must fail (constant kernel is invariant)",
          ratio_c > 0.99, "constant kernel: ratio ||W(0.05)||/||W0|| = %s" % dn(ratio_c, 4))

    # singular support: jump of W(t) across x=1/2 equals e^{-2t} times the jump of W0 (constant marginals)
    n8 = 8
    W8 = np.zeros((n8, n8))
    W8[:4, :4] = 1; W8[4:, 4:] = 1
    D8 = np.zeros((n8 * n8, n8 * n8))
    for i in range(n8 * n8):
        e = np.zeros(n8 * n8); e[i] = 1
        E = e.reshape(n8, n8)
        D8[:, i] = (E.mean(axis=1)[:, None] + E.mean(axis=0)[None, :] - 2 * E).ravel()
    jumps = []
    for t in (0.3, 1.0, 2.0):
        Wt = (sla.expm(t * D8) @ W8.ravel()).reshape(n8, n8)
        jumps.append((t, Wt[3, 0] - Wt[4, 0]))
    ok_j = all(abs(j - np.exp(-2 * t)) < 1e-12 for t, j in jumps)
    bad_j = all(abs(j - np.exp(-t)) > 1e-3 for t, j in jumps)
    claim("C2.13", "chap02.tex:454-466 (Thm heat_smoothing (ii))",
          "a jump discontinuity of W0 survives with amplitude e^{-2t} (marginals constant)",
          ok_j, "block kernel on 8 cells: jumps %s match e^{-2t}" % ["%s" % up(j, 8) for t, j in jumps],
          "amplitude e^{-t} must fail", bad_j, "jump vs e^{-t} differs for all t tested")

    # Dirichlet energy examples
    f = lambda x, y: -1.0 * (np.cos(2 * np.pi * x) - np.cos(2 * np.pi * y)) ** 2 / 2
    En = quad(lambda x: quad(lambda y: f(x, y), 0, 1, epsabs=1e-12)[0], 0, 1, epsabs=1e-12)[0]
    En_pos = quad(lambda x: quad(lambda y: -f(x, y), 0, 1, epsabs=1e-12)[0], 0, 1, epsabs=1e-12)[0]
    I = mp.quad(lambda u: 3 * u ** 2 * (u ** 3) ** (-mp.mpf(2) / 3), [0, 1])
    claim("C2.14", "chap02.tex:428 (Prop graphon_dirichlet_energy, counterexamples)",
          "for W=-1 and u=cos(2 pi x): E_W(u) = -1/2; f=x^{-1/3} lies in L^2 (int f^2 = 3) but not in L^infinity",
          abs(En + 0.5) < 1e-7 and abs(I - 3) < 1e-8,
          "iterated quadrature E=(1/2)iint W(u(x)-u(y))^2 = %s ; mpmath int_0^1 x^{-2/3} = %s" % (up(En, 8), mp.nstr(I, 10)),
          "the sign-sensitive claim 'E_W(u) >= 0 for every u' must fail for W=-1 and hold for W=+1 (same quadrature, W=+1 gives E=+1/2)",
          En_pos > 0.4999 and En < 0, "E(W=+1) = %s, E(W=-1) = %s" % (up(En_pos, 6), up(En, 6)))


# ---------------------------------------------------------------- H. Ricci flow remark
def step_graphon(p, q, m=12):
    """2-block step graphon on 2m cells; returns W, d, kappa(codegree ratio)."""
    n = 2 * m
    W = np.full((n, n), q, dtype=float)
    W[:m, :m] = p; W[m:, m:] = p
    d = W.mean(axis=1)
    cod = (W @ W.T) / n
    mx = np.maximum(d[:, None], d[None, :])
    return W, d, cod / mx


def section_H():
    maxerr = 0.0
    maxqd = 0.0
    maxpd = 0.0
    asym = []
    for (p, q) in [(1.0, 0.1), (0.8, 0.3), (0.6, 0.05), (0.9, 0.9 * 0.5)]:
        m = 10
        W, d, K = step_graphon(p, q, m)
        s = p + q
        maxerr = max(maxerr, np.max(np.abs(d - s / 2)))
        kin = (p * p + q * q) / s; kout = 2 * p * q / s
        maxerr = max(maxerr, abs(K[0, 1] - kin), abs(K[0, m + 1] - kout))
        kbar = (W * K).mean() / W.mean()
        formula_bar = (p * kin + q * kout) / s
        maxerr = max(maxerr, abs(kbar - formula_bar))
        rate_num = 2 * (K[0, m + 1] - kbar) * q       # q-dot from the normalised flow
        rate_formula = -2 * p * q * (p - q) ** 2 / s ** 2
        maxqd = max(maxqd, abs(rate_num - rate_formula))
        pdot_num = 2 * (K[0, 1] - kbar) * p
        maxpd = max(maxpd, abs(pdot_num + rate_formula))
    # exponential rate 2(1+eps) from the initial datum p=1, q=eps (ODE in q)
    eps = 0.1
    s = 1 + eps
    # q' = -2 p q (p-q)^2/s^2 with p = s - q
    solq = solve_ivp(lambda t, z: [-2 * (s - np.exp(z[0])) * (s - 2 * np.exp(z[0])) ** 2 / s ** 2], [0, 40], [np.log(eps)],
                     method="DOP853", rtol=1e-12, atol=1e-12, t_eval=[20, 25, 30, 35])
    lq = solq.y[0]
    slope = (lq[-1] - lq[0]) / (solq.t[-1] - solq.t[0])
    # block q=0: p1' = 2 p1 p2 (p1-p2)/S ; limit p1 -> S ; linear growth rate of asymmetry near p1=p2 equals S
    S = 1.0
    sol0 = solve_ivp(lambda t, y: [2 * y[0] * (S - y[0]) * (2 * y[0] - S) / S], [0, 200], [0.5 + 1e-6], method="DOP853",
                     rtol=1e-12, atol=1e-14, t_eval=np.linspace(0, 12, 13))
    asy = (2 * sol0.y[0] - S) / S
    grow = np.log(asy[3] / asy[1]) / (sol0.t[3] - sol0.t[1])
    final = solve_ivp(lambda t, y: [2 * y[0] * (S - y[0]) * (2 * y[0] - S) / S], [0, 60], [0.5 + 1e-6],
                      method="DOP853", rtol=1e-12, atol=1e-14).y[0, -1]
    # same formula via direct matrices for q=0 class (continuum codegree ratio)
    Wm, dm, Km = step_graphon(0.7, 0.0, 10)
    kapp = Km[0, 1]
    claim("C2.15", "chap02.tex:536-545 (Remark (c): 2-block graphon, normalised flow)",
          "d_W=s/2, kappa_in=(p^2+q^2)/s, kappa_out=2pq/s, kappa_bar=(p kin+q kout)/s, q'=-2pq(p-q)^2/s^2=-p'; rate 2(1+eps) for q; "
          "q=0 class: p1'=2p1p2(p1-p2)/S, asymmetry grows at rate S, p1->S",
          maxerr < 1e-12 and maxqd < 1e-12 and maxpd < 1e-12 and abs(slope + 2 * s) < 5e-3 and abs(grow - S) < 5e-3
          and abs(final - S) < 1e-6 and abs(kapp - 0.7) < 1e-12,
          "discretised step graphon (20 cells) codegree ratios vs formulas: max error %s; q' error %s; p' error %s; "
          "late-time slope of ln q = %s vs -2(1+eps) = %s; asymmetry growth rate %s vs S=1; p1(60)=%s"
          % (up(maxerr, 2), up(maxqd, 2), up(maxpd, 2), up(slope, 5), up(-2 * s, 5), up(grow, 5), up(final, 8)),
          "a decay rate of 2 (instead of 2(1+eps)) or growth rate 2S must disagree",
          abs(slope + 2) > 0.1 and abs(grow - 2 * S) > 0.5,
          "slope differs from -2 by %s; growth differs from 2S by %s" % (dn(abs(slope + 2), 3), dn(abs(grow - 2 * S), 3)))

    # TV curvature of G(n,1/2) -> 1/2 ; constant graphon has kappa^TV = 1
    devs = []
    for n in (200, 400, 800, 1600):
        A = (rng.random((n, n)) < 0.5).astype(float)
        A = np.triu(A, 1); A = A + A.T
        deg = A.sum(axis=1)
        M = A / deg[:, None]                       # density of m_x on the cells: A_ik/deg_i (each cell has width 1/n)
        Kmat = np.empty((n, n))
        for i in range(n):                         # kappa^TV = 1 - (1/2)||m_x - m_y||_1 = sum_k min(m_x, m_y), BY DEFINITION
            Kmat[i] = 1.0 - 0.5 * np.abs(M[i] - M).sum(axis=1)
        iu = np.triu_indices(n, 1)
        if n == 200:                               # cross-check of the codegree/max-degree identity used in the text
            cod = A @ A
            Kid = cod / np.maximum(deg[:, None], deg[None, :])
            ident_err = float(np.abs(Kid[iu] - Kmat[iu]).max())
        devs.append((n, float(np.abs(Kmat[iu] - 0.5).max()), float(np.mean(Kmat[iu]))))
    dec = all(devs[i + 1][1] < devs[i][1] for i in range(3))
    # The cut-norm bound is an ALMOST-SURE ASYMPTOTIC statement ("for all large n"); a finite n cannot decide it.  What is checkable:
    # (a) the bounded-differences constant: for F = sum_{i in S, j in T, i!=j} (A_ij - 1/2) the coefficient of the free variable A_ij (i<j)
    #     is c_ij = 1[i in S, j in T] + 1[j in S, i in T] <= 2, hence sum c_ij^2 <= 2 n^2; exact enumeration of ALL (S,T) at n = 6.
    n6 = 6
    maxsc2 = 0.0
    for ms in range(1 << n6):
        Sv = np.array([(ms >> i) & 1 for i in range(n6)], dtype=float)
        for mt in range(1 << n6):
            Tv = np.array([(mt >> i) & 1 for i in range(n6)], dtype=float)
            C = np.outer(Sv, Tv); np.fill_diagonal(C, 0.0)
            c = C + C.T
            maxsc2 = max(maxsc2, float((np.triu(c, 1) ** 2).sum()))
    # (b) Hoeffding itself against the EXACT law of F (all 2^15 graphs, S=T=everything, n=6): P(|F|>t) <= 2 exp(-2 t^2 / sum c^2)
    pairs6 = [(i, j) for i in range(n6) for j in range(i + 1, n6)]
    bits = ((np.arange(1 << len(pairs6))[:, None] >> np.arange(len(pairs6))) & 1).astype(float)
    Fv = 2.0 * (bits - 0.5).sum(axis=1)                # S=T=[n]: F = 2 sum_{i<j}(A_ij-1/2)
    sc2_full = 4.0 * len(pairs6)
    hoeff_ok = all((np.abs(Fv) > t).mean() <= 2 * np.exp(-2 * t * t / sc2_full) + 1e-15 for t in (1.0, 2.0, 4.0, 6.0, 8.0, 10.0))
    # (c) summability: sum_n 4^n e^{-4n} converges because 4/e^4 < 1 (mpmath nsum vs the geometric closed form)
    ratio = 4.0 / math.exp(4.0)
    ssum = mp.nsum(lambda k: mp.mpf(4) ** k * mp.e ** (-4 * k), [1, mp.inf])
    geom_ok = ratio < 1 and abs(ssum - mp.mpf(ratio) / (1 - ratio)) < 1e-12
    # (d) evidence only, n = 20 (bound 0.472 < 1/2 there): exact cut norm over all 2^20 subsets, 4 samples
    def cut_exact_vec(Mx):
        nn = Mx.shape[0]; best = 0.0
        ar = np.arange(1 << 16, dtype=np.int64)
        for hi in range(1 << (nn - 16)):
            m = ((ar[:, None] >> np.arange(16)) & 1).astype(float)
            hbits = ((hi >> np.arange(nn - 16)) & 1).astype(float)
            Sm = np.hstack([m, np.tile(hbits, (len(ar), 1))])
            c = Sm @ Mx
            best = max(best, np.maximum(c, 0).sum(axis=1).max(), np.maximum(-c, 0).sum(axis=1).max())
        return best / nn ** 2
    n20 = 20
    cn = []
    for _ in range(4):
        Aa = (rng.random((n20, n20)) < 0.5).astype(float); Aa = np.triu(Aa, 1); Aa = Aa + Aa.T
        cn.append(cut_exact_vec(Aa - 0.5))
    bound20 = 2 / np.sqrt(n20) + 1 / (2 * n20)
    mutC = 4.0 / math.exp(1.0)                          # mutant exponent n instead of 4n: 4/e > 1, series diverges
    claim("C2.16", "chap02.tex:526-529 (Remark (a))",
          "G(n,1/2): kappa^TV_{W_n} -> 1/2 uniformly (while kappa^TV_{1/2} = 1); the cut-norm bound rests on sum c_ij^2 <= 2n^2, Hoeffding with exponent 4n and summability of 4^n e^{-4n}",
          maxsc2 <= 2 * n6 ** 2 and maxsc2 > n6 ** 2 and hoeff_ok and geom_ok and abs(devs[-1][2] - 0.5) < 0.01 and ident_err < 1e-12,
          "kappa^TV computed from the DEFINITION 1-(1/2)||m_x-m_y||_1 (agrees with codegree/max-degree to %s at n=200); n=200,400,800,1600: max_{i!=j}|kappa^TV-1/2| = %s, mean kappa = %s; "
          "exact enumeration at n=6 of all (S,T): max sum c_ij^2 = %s (<= 2n^2 = %s, and > n^2 = %s); Hoeffding vs exact law at n=6 holds on 6 thresholds: %s; "
          "4/e^4 = %s < 1, nsum = %s; EVIDENCE ONLY (finite n): exact cut norms at n=20 over 4 samples max %s <= bound %s"
          % (up(ident_err, 2), [up(x[1], 3) for x in devs], [up(x[2], 4) for x in devs], maxsc2, 2 * n6 ** 2, n6 ** 2, hoeff_ok, up(ratio, 4), mp.nstr(ssum, 8), up(max(cn), 3), up(bound20, 3)),
          "claiming kappa^TV_{W_n} -> 1, a bounded-differences constant n^2 (half), or the exponent n (series sum 4^n e^{-n}) must fail",
          abs(devs[-1][2] - 1.0) > 0.4 and not (maxsc2 <= n6 ** 2) and mutC > 1,
          "mean kappa^TV = %s far from 1; max sum c^2 = %s exceeds n^2 = %s; 4/e = %s > 1 (diverges)" % (up(devs[-1][2], 4), maxsc2, n6 ** 2, up(mutC, 3)))
    explore("C2.16b", "chap02.tex:528", "max deviation of kappa^TV from 1/2 decreases with n: %s" % dec)


# ---------------------------------------------------------------- I. barbell Ricci flow
def barbell_flow(tmax=10.0, h=0.02, tlimit=420, weighted_walk=False):
    import ot
    from scipy.sparse.csgraph import floyd_warshall
    n = 12
    edges = [(i, j) for i in range(6) for j in range(i + 1, 6)] + [(i, j) for i in range(6, 12) for j in range(i + 1, 12)] + [(0, 6)]
    ne = len(edges)
    bridge = ne - 1

    def curvatures(ell):
        Wt = np.zeros((n, n)); Lm = np.zeros((n, n))
        for e, (i, j) in enumerate(edges):
            Wt[i, j] = Wt[j, i] = 1.0 / ell[e]
            Lm[i, j] = Lm[j, i] = ell[e]
        dist = floyd_warshall(Lm, directed=False)
        Adj = (Wt > 0).astype(float)
        P = 0.5 * np.eye(n) + 0.5 * (Wt if weighted_walk else Adj) / (Wt if weighted_walk else Adj).sum(axis=1, keepdims=True)
        kap = np.zeros(ne); dd = np.zeros(ne)
        for e, (i, j) in enumerate(edges):
            w1 = ot.emd2(P[i], P[j], dist, numItermax=200000)
            dd[e] = dist[i, j]
            kap[e] = 1 - w1 / dist[i, j]
        return kap, dd
    ell = np.ones(ne)
    t = 0.0
    traj = []
    k0, d0 = curvatures(ell)
    kb0 = k0[bridge]
    start = time.time()
    f = lambda l: (lambda kd: -kd[0] * kd[1])(curvatures(l))
    cross = None
    maxb = ell[bridge]
    last = kb0
    steps = int(round(tmax / h))
    for s in range(steps):
        if time.time() - start > tlimit:
            return dict(timeout=True, t=t, kb0=kb0)
        k1 = f(ell); k2 = f(ell + h / 2 * k1); k3 = f(ell + h / 2 * k2); k4 = f(ell + h * k3)
        ell = ell + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        t += h
        kb, _ = (lambda kd: (kd[0][bridge], 0))(curvatures(ell))
        if cross is None and last < 0 <= kb:
            cross = t - h + h * (-last) / (kb - last)
        last = kb
        maxb = max(maxb, ell[bridge])
    return dict(timeout=False, kb0=kb0, cross=cross, maxb=maxb, clique_max=float(ell[:bridge].max()), clique_min=float(ell[:bridge].min()), t=t)


def section_I():
    import ot
    from scipy.optimize import linprog
    # exact curvature of the bridge at unit lengths and cross-check of the transport solver
    n = 12
    A = np.zeros((n, n))
    for i in range(6):
        for j in range(6):
            if i != j:
                A[i, j] = 1; A[i + 6, j + 6] = 1
    A[0, 6] = A[6, 0] = 1
    from scipy.sparse.csgraph import shortest_path
    dist = shortest_path(A, unweighted=True, directed=False)
    P = 0.5 * np.eye(n) + 0.5 * A / A.sum(axis=1, keepdims=True)
    w1_ot = ot.emd2(P[0], P[6], dist)
    # linprog oracle
    c = dist.ravel()
    Aeq = np.zeros((2 * n, n * n)); beq = np.concatenate([P[0], P[6]])
    for i in range(n):
        Aeq[i, i * n:(i + 1) * n] = 1
        Aeq[n + i, i::n] = 1
    lp = linprog(c, A_eq=Aeq, b_eq=beq, bounds=(0, None), method="highs")
    kb0 = 1 - lp.fun / dist[0, 6]
    res = barbell_flow()
    res_w = barbell_flow(weighted_walk=True, tlimit=300)
    if res.get("timeout"):
        unchecked("C2.17", "chap02.tex:534", "barbell flow did not finish within the time budget (t reached %s)" % res["t"])
        return
    ok = abs(kb0 + 2 / 3) < 1e-9 and abs(1 - w1_ot / dist[0, 6] + 2 / 3) < 1e-9 and abs(res["kb0"] + 2 / 3) < 1e-9 \
        and res["cross"] is not None and 3.9 < res["cross"] < 4.3 and res["maxb"] < 1.82 and res["clique_max"] < 1.0
    # Two readings of the transition law (the text does not state it; F-65):
    #   A = lazy walk, idleness 1/2, UNIFORM over the neighbours;   B = lazy walk, step proportional to the weight 1/ell_e
    #   (literal reading of "the counterpart of (graphon_ricci) for the weights 1/ell_e", since m_x = W(x,.)/d_W(x)).
    ok_A = abs(kb0 + 2 / 3) < 1e-9 and abs(1 - w1_ot / dist[0, 6] + 2 / 3) < 1e-9 and abs(res["kb0"] + 2 / 3) < 1e-9         and res["cross"] is not None and 3.9 < res["cross"] < 4.3 and res["maxb"] < 1.82 and res["clique_max"] < 1.0
    claim("C2.17A", "chap02.tex:534 (Remark (b), barbell K6-K6), reading A (uniform over neighbours)",
          "bridge curvature = -2/3 at t=0, turns positive near t~4.1; bridge length stays below 1.82 on [0,10]; clique edges contract (RK4, h=0.02)",
          ok_A,
          "curvature(0): POT emd2 gives %s, scipy linprog (HiGHS) gives %s; RK4 h=0.02: sign change at t=%s, max bridge length on [0,10] = %s (<1.82), "
          "clique edge lengths at t=10 in [%s, %s]. REPRODUCED ONLY UNDER READING A."
          % (up(1 - w1_ot / dist[0, 6], 8), up(kb0, 8), up(res["cross"], 3) if res["cross"] else None, up(res["maxb"], 4),
             dn(res["clique_min"], 3), up(res["clique_max"], 3)),
          "mutants must fail: curvature -1/2; bridge length below 1.80 (max is %s); sign change before t=3.9 (it is %s)" % (up(res["maxb"], 4), up(res["cross"], 3) if res["cross"] else None),
          abs(kb0 + 0.5) > 0.1 and res["maxb"] > 1.80 and res["cross"] is not None and res["cross"] > 3.9,
          "curvature differs from -1/2 by %s; max bridge length %s > 1.80; crossing %s > 3.9" % (dn(abs(kb0 + 0.5), 3), dn(res["maxb"], 4), dn(res["cross"], 3) if res["cross"] else None))
    if res_w.get("timeout"):
        unchecked("C2.17B", "chap02.tex:534", "reading B (step proportional to 1/ell_e) did not finish in the time budget")
    else:
        ok_B = abs(res_w["kb0"] + 2 / 3) < 1e-9 and res_w["cross"] is not None and 3.9 < res_w["cross"] < 4.3 and res_w["maxb"] < 1.82
        # Reading B (step proportional to 1/ell_e) is an ALTERNATIVE reading, not a claim of the book: since F-65 the text says the walk is a
        # lazy simple random walk (uniform over the neighbours), i.e. reading A, which is C2.17A.  Reading B is reported as EXPLORE.
        explore("C2.17B", "chap02.tex:534 (Remark (b)), ALTERNATIVE reading B (step proportional to 1/ell_e; not the book's walk)",
                "reading B: curvature(0)=%s (the -2/3 is reproduced), sign change at t=%s (None = no sign change on [0,10]), max bridge length=%s (text: <1.82), "
                "clique lengths at t=10 in [%s,%s]; mutant 'curvature -1/2 at t=0' fails (differs by %s); ok_B=%s. The book's numbers hold under reading A only."
                % (up(res_w["kb0"], 6), res_w["cross"], up(res_w["maxb"], 4), dn(res_w["clique_min"], 3), up(res_w["clique_max"], 3),
                   dn(abs(res_w["kb0"] + 0.5), 3), bool(ok_B)))
    # reading C (the measure of Ni et al. 2019, weighted by exp(-d^p)): not tested, source not read in this round
    unchecked("C2.17C", "chap02.tex:534", "reading C (measure of Ni et al. 2019, weights exp(-d^p)) needs the primary source; not tested")


# ---------------------------------------------------------------- J. Dyson / path ordered limit
def section_J():
    r = 2
    A_fun = lambda s: np.array([[0.8 * np.sin(2 * np.pi * s), 1 + 0.5 * np.cos(2 * np.pi * s)],
                                [-0.7 + 0.3 * np.sin(4 * np.pi * s), 0.4 * np.cos(2 * np.pi * s)]], dtype=complex)
    dA_fun = lambda s: (A_fun(s + 1e-6) - A_fun(s - 1e-6)) / 2e-6

    def exact_hol():
        f = lambda s, y: (A_fun(s) @ y.reshape(r, r)).ravel()
        so = solve_ivp(f, [0, 1], np.eye(r, dtype=complex).ravel(), method="DOP853", rtol=1e-13, atol=1e-14)
        return so.y[:, -1].reshape(r, r)
    U = exact_hol()
    grid = np.linspace(0, 1, 20001)
    nA = np.array([np.linalg.norm(A_fun(s), 2) for s in grid])
    a0 = nA.max(); L1 = np.trapezoid(nA, grid)
    a1 = max(np.linalg.norm(dA_fun(s), 2) for s in grid[::50])
    out = []
    ok = True
    for M in (0.0, 1.0):
        rg = np.random.default_rng(7)
        for k in (10, 20, 40, 80, 160, 320, 640):
            Mk = np.eye(r, dtype=complex)
            for j in range(1, k + 1):
                if M > 0:
                    Q, _ = np.linalg.qr(rg.standard_normal((r, r)) + 1j * rg.standard_normal((r, r)))
                    R = M * Q
                else:
                    R = np.zeros((r, r))
                Aj = np.eye(r) + A_fun(j / k) / k + R / k ** 2
                Mk = Aj @ Mk
            err = abs(np.trace(Mk) - np.trace(U))
            bound = (r / k) * (M + (a1 + a0 ** 2) / 2) * np.exp(L1 + (M + a1 / 2) / k)
            ok &= err <= bound
            if k in (10, 640):
                out.append("M=%g k=%d err=%s <= bound=%s" % (M, k, up(err, 3), dn(bound, 3)))
    # slope for R=0
    errs = []
    ks = [20, 40, 80, 160, 320, 640, 1280]
    for k in ks:
        Mk = np.eye(r, dtype=complex)
        for j in range(1, k + 1):
            Mk = (np.eye(r) + A_fun(j / k) / k) @ Mk
        errs.append(np.linalg.norm(Mk - U, 2))
    slope = np.polyfit(np.log(ks), np.log(errs), 1)[0]
    # tightness example with exact rational arithmetic
    from fractions import Fraction
    tight = True; weak_fail = False
    for Mq in (Fraction(1, 10), Fraction(1), Fraction(10)):
        for k in (2, 3, 7, 50, 400):
            e = (1 + Mq / k ** 2) ** k - 1
            tight &= (e > Mq / k) and (float(e) <= float(Mq / k) * np.exp(float(Mq) / k) + 1e-15)
            weak_fail |= not (float(e) <= float(Mq / k))
    # gauge invariance
    gt = np.random.default_rng(3)
    Om_fun = lambda s: sla.expm(0.6 * np.array([[0, np.sin(2 * np.pi * s)], [-np.sin(2 * np.pi * s), 0]]) +
                                0.3 * np.cos(4 * np.pi * s) * np.array([[1, 0], [0, -1]]))
    dOm = lambda s: (Om_fun(s + 1e-6) - Om_fun(s - 1e-6)) / 2e-6
    AO = lambda s: np.linalg.inv(Om_fun(s)) @ A_fun(s) @ Om_fun(s) - np.linalg.inv(Om_fun(s)) @ dOm(s)
    so = solve_ivp(lambda s, y: (AO(s) @ y.reshape(r, r)).ravel(), [0, 1], np.eye(r, dtype=complex).ravel(), method="DOP853", rtol=1e-12, atol=1e-13)
    UO = so.y[:, -1].reshape(r, r)
    gdiff = abs(np.trace(UO) - np.trace(U))
    so2 = solve_ivp(lambda s, y: (A_fun(s) @ y.reshape(r, r)).ravel() * 0 + (AO(s) @ y.reshape(r, r)).ravel() + 0.5 * y, [0, 1],
                    np.eye(r, dtype=complex).ravel(), method="DOP853", rtol=1e-12, atol=1e-13)
    claim("C2.18", "chap02.tex:626-648 (Thm continuous_path_integral (i),(ii),(iii))",
          "|Z_k - Tr Pexp| <= (r/k)(M+(a1+a0^2)/2) exp(L1+(M+a1/2)/k), rate O(1/k), factor e^{M/k} needed, gauge invariance of the trace",
          ok and abs(slope + 1) < 0.05 and tight and weak_fail and gdiff < 1e-7,
          "r=2 complex test connection, exact holonomy by DOP853 (rtol 1e-13): all 14 (M,k) cases satisfy the bound (e.g. %s); "
          "R=0: log-log slope of the product error = %s; (1+M/k^2)^k-1 in exact rationals lies in (M/k, (M/k)e^{M/k}]; gauge-transformed trace differs by %s"
          % ("; ".join(out[:2]), up(slope, 4), up(gdiff, 2)),
          "a bound with the factor e^{M/k} dropped (error <= M/k) must fail, and a 1/k^2 rate must disagree with the slope",
          weak_fail and abs(slope + 2) > 0.5,
          "(1+M/k^2)^k-1 exceeds M/k in exact arithmetic; slope %s != -2" % up(slope, 4))
    bad_g = abs(np.trace(so2.y[:, -1].reshape(r, r)) - np.trace(U))
    explore("C2.18b", "chap02.tex:650-656", "mutated connection A^Omega + 0.5 I changes Z by %s (gauge identity is not vacuous)" % dn(bad_g, 3))


# ---------------------------------------------------------------- K. Table + cMPS finite-dim analogue + MCF
def section_K():
    # affine-invariant flow A' = -A log A is the AI-gradient flow of (1/2) d_AI(A,I)^2 = (1/2)||log A||_F^2
    A = rand_spd(3)
    F = lambda X: 0.5 * np.sum(funm_spd(X, np.log) ** 2)
    h = 1e-6
    gE = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            E = np.zeros((3, 3)); E[i, j] = 1; E[j, i] = 1
            if i == j:
                E = np.zeros((3, 3)); E[i, i] = 1
            val = (F(A + h * E) - F(A - h * E)) / (2 * h)
            gE[i, j] = val
    # Euclidean gradient G_ij (symmetric): directional derivative along E_ij+E_ji equals G_ij+G_ji = 2 G_ij for i!=j
    G = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            G[i, j] = gE[i, j] if i == j else gE[i, j] / 2
    G = (G + G.T) / 2
    gAI = A @ G @ A
    target = A @ funm_spd(A, np.log)
    err = np.max(np.abs(gAI - target))
    err_bad = np.max(np.abs(G - target))
    # decay of d_AI(A,I) along -A log A
    sol = solve_ivp(lambda t, y: (-(y.reshape(3, 3) @ funm_spd(y.reshape(3, 3), np.log))).ravel(), [0, 20], A.ravel(), rtol=1e-10, atol=1e-14,
                    t_eval=np.linspace(0, 20, 201))
    dsq = [2 * F((y.reshape(3, 3) + y.reshape(3, 3).T) / 2) for y in sol.y.T]
    claim("C2.19", "chap02.tex:717 (Table row 'Covariance Filtering')",
          "A' = -A log A is the AI-gradient flow of (1/2) d_AI(A,I)^2 and d_AI(A,I) decreases to 0",
          err < 1e-6 and np.all(np.diff(dsq[:21]) < 0) and np.sqrt(abs(dsq[-1])) < 1e-6,
          "central differences: |A G A - A log A| = %s (G = Euclidean gradient of (1/2)||log A||^2); d_AI^2 strictly decreasing on [0,2] (21 samples) and d_AI(t=20) = %s < 1e-6" % (up(err, 2), up(np.sqrt(abs(dsq[-1])), 3)),
          "the Euclidean gradient without the A.A conjugation must not equal A log A",
          err_bad > 1e-3, "|G - A log A| = %s" % dn(err_bad, 2))

    # finite-dimensional analogue of the McLachlan proposition (gauge-degenerate parametrisation psi = a (x) b / norm)
    rg = np.random.default_rng(11)
    Hm = rg.standard_normal((4, 4)); Hm = (Hm + Hm.T) / 2
    th = rg.standard_normal(4)

    def psi(t):
        v = np.kron(t[:2], t[2:]); return v / np.linalg.norm(v)

    def dpsi(t):
        e = 1e-6
        return np.array([(psi(t + e * np.eye(4)[i]) - psi(t - e * np.eye(4)[i])) / (2 * e) for i in range(4)]).T
    P = psi(th); D = dpsi(th)
    Pperp = np.eye(4) - np.outer(P, P)
    g = (Pperp @ D).T @ (Pperp @ D)
    E = P @ Hm @ P
    gradE = 2 * (D.T @ (Hm @ P))
    thd = -0.5 * np.linalg.pinv(g, rcond=1e-9) @ gradE
    resid = np.linalg.norm(g @ thd + 0.5 * gradE)
    # McLachlan minimiser by least squares (independent route)
    Aff = Pperp @ D
    rhs = -(Hm - E * np.eye(4)) @ P
    sol_ls = np.linalg.lstsq(Aff, rhs, rcond=1e-9)[0]
    dE_dtau = gradE @ thd
    Q, s_, _ = np.linalg.svd(Aff, full_matrices=False)
    Q = Q[:, s_ > 1e-8]
    PiHE = Q @ (Q.T @ ((Hm - E * np.eye(4)) @ P))
    rank_g = int((np.linalg.svd(g, compute_uv=False) > 1e-8).sum())
    thd_bad = -1.0 * np.linalg.pinv(g, rcond=1e-9) @ gradE
    dE_bad = gradE @ thd_bad
    claim("C2.20", "chap02.tex:581-607 (Prop cmps_energy_flow; finite-dimensional analogue)",
          "McLachlan minimiser solves g theta' = -(1/2) grad<H>, and d<H>/dtau = -2 theta'^T g theta' = -2||Pi (H-E) psi||^2 (gauge-degenerate g)",
          resid < 1e-6 and abs(dE_dtau + 2 * thd @ g @ thd) < 1e-6 and abs(dE_dtau + 2 * np.linalg.norm(PiHE) ** 2) < 1e-6
          and np.linalg.norm(Aff @ sol_ls - Aff @ thd) < 1e-6 and rank_g < 4,
          "psi=a(x)b/norm (4 parameters, rank g=%d): normal-equation residual %s; dE/dtau=%s vs -2||Pi(H-E)psi||^2=%s; "
          "lstsq McLachlan velocity gives the same projected velocity (diff %s)"
          % (rank_g, up(resid, 2), up(dE_dtau, 8), up(-2 * np.linalg.norm(PiHE) ** 2, 8), up(np.linalg.norm(Aff @ sol_ls - Aff @ thd), 2)),
          "using g theta' = -grad E (missing 1/2) must violate dE/dtau = -2||Pi(H-E)psi||^2",
          abs(dE_bad + 2 * np.linalg.norm(PiHE) ** 2) > 1e-3, "mutated dE/dtau = %s" % dn(dE_bad, 4))
    unchecked("C2.20b", "chap02.tex:581-607", "the statement is for the infinite-dimensional cMPS manifold (regularity conditions assumed, flow existence not proved); only the finite-dimensional algebra was checked")

    # level-set MCF perimeter identity, regularised analogue on the torus (spectral derivatives, 3 refinements)
    eps = 1.0
    rels = []
    fdv = fmv = None
    for N in (48, 96, 192):
        x = np.arange(N) / N
        X, Y = np.meshgrid(x, x, indexing="ij")
        u = np.sin(2 * np.pi * X) + 0.5 * np.cos(2 * np.pi * Y + 0.7) + 0.2 * np.sin(4 * np.pi * (X + Y))
        kx = 2j * np.pi * np.fft.fftfreq(N, d=1.0 / N)
        KX, KY = np.meshgrid(kx, kx, indexing="ij")
        ddx = lambda f: np.real(np.fft.ifft2(KX * np.fft.fft2(f)))
        ddy = lambda f: np.real(np.fft.ifft2(KY * np.fft.fft2(f)))
        TV = lambda f: np.mean(np.sqrt(ddx(f) ** 2 + ddy(f) ** 2 + eps ** 2))
        nrm = np.sqrt(ddx(u) ** 2 + ddy(u) ** 2 + eps ** 2)
        H = ddx(ddx(u) / nrm) + ddy(ddy(u) / nrm)
        ut = nrm * H
        hh = 1e-5
        fd1 = (TV(u + hh * ut) - TV(u - hh * ut)) / (2 * hh)
        fd2 = (TV(u + hh * ut / 2) - TV(u - hh * ut / 2)) / hh
        fdv = (4 * fd2 - fd1) / 3          # Richardson extrapolation in the time step
        fmv = -np.mean(H ** 2 * nrm)
        rels.append(abs(fdv - fmv) / abs(fmv))
    claim("C2.21", "chap02.tex:550-565 (Prop mean_curvature_coarea; regularised analogue)",
          "d/dt integral |grad u| = -integral H^2 |grad u| along u_t=|grad u| div(grad u/|grad u|)",
          rels[-1] < 1e-8,
          "regularised |grad u|_eps with eps=1 on 48,96,192-point tori, spectral derivatives, Richardson in the time step: relative differences %s; finest: finite difference %s vs formula %s"
          % ([up(r_, 2) for r_ in rels], up(fdv, 9), up(fmv, 9)),
          "the factor 2 mutation (-2 integral H^2|grad u|) must fail", abs(fdv - 2 * fmv) > 0.1 * abs(fmv),
          "mutated value %s differs from finite difference %s" % (up(2 * fmv, 6), up(fdv, 6)))
    unchecked("C2.21b", "chap02.tex:550-565", "the unregularised identity involves critical points of u (|grad u|=0) on the torus; only the eps-regularised integration by parts was tested numerically")


if __name__ == "__main__":
    section_A(); section_A2(); section_B(); section_C(); section_D(); section_E(); section_F()
    section_G(); section_H(); section_I(); section_J(); section_K()
    unchecked("C2.U1", "chap02.tex:123-126", "qualitative statements in the introduction (Hadamard manifold completeness, simple connectivity, Alexandrov curvature >= 0, Cauchy-Lipschitz/escape lemma, Fleming-Rishel coarea) are theorems or cited results without a numerical content")
    finish("2")
