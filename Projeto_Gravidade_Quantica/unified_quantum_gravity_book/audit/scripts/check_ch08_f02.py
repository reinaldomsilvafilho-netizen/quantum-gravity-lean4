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
# Chapter 8 body.  Source: chap08_noneuclidean_minimax_relativity_adm.tex (3.0.0)
# ======================================================================
import itertools
from fractions import Fraction
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import minimize, minimize_scalar
from scipy import constants as sc

rng = np.random.default_rng(20261016)


def sect(G, coords, point, U, V):
    """Sectional curvature of the plane (U,V) at `point` (convention checked on the unit S^2: +1)."""
    n = len(coords)
    Gi = G.inv()
    Gam = [[[sum(Gi[i, l] * (sp.diff(G[l, k], coords[j]) + sp.diff(G[l, j], coords[k]) - sp.diff(G[j, k], coords[l])) for l in range(n)) / 2
             for k in range(n)] for j in range(n)] for i in range(n)]
    sub = dict(zip(coords, point))
    Gn = G.subs(sub)
    Gamn = [[[Gam[i][j][k].subs(sub) for k in range(n)] for j in range(n)] for i in range(n)]
    # explicit loop with index lowering
    Rup = {}
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    t = sp.diff(Gam[i][l][j], coords[k]).subs(sub) - sp.diff(Gam[i][k][j], coords[l]).subs(sub)
                    t += sum(Gamn[i][k][m] * Gamn[m][l][j] - Gamn[i][l][m] * Gamn[m][k][j] for m in range(n))
                    Rup[(i, j, k, l)] = t
    num = 0
    for i, j, k, l in itertools.product(range(n), repeat=4):
        Rl = sum(Gn[i, m] * Rup[(m, j, k, l)] for m in range(n))
        num += Rl * U[i] * V[j] * U[k] * V[l]
    uu = (sp.Matrix(U).T * Gn * sp.Matrix(U))[0]
    vv = (sp.Matrix(V).T * Gn * sp.Matrix(V))[0]
    uv = (sp.Matrix(U).T * Gn * sp.Matrix(V))[0]
    return sp.N(num / (uu * vv - uv ** 2), 25)


def section_forms():
    th, ph = sp.symbols("th ph")
    ks = float(sect(sp.diag(1, sp.sin(th) ** 2), [th, ph], [sp.Rational(7, 10), sp.Rational(1, 3)], [1, 0], [0, 1]))
    r, phi, tt = sp.symbols("r phi t", positive=True)
    rows = []
    allok = True
    for c in (sp.Rational(1), sp.Rational(3, 2)):
        # tube metric about a geodesic in H^3(-c^2)
        Gt = sp.diag(1, sp.sinh(c * r) ** 2 / c ** 2, sp.cosh(c * r) ** 2)
        # equidistant metric: dr^2 + cosh^2(cr) (dx^2+dy^2)/(c^2 y^2)  (coords r,x,y)
        x_, y_ = sp.symbols("x y", positive=True)
        Ge = sp.diag(1, sp.cosh(c * r) ** 2 / (c ** 2 * y_ ** 2), sp.cosh(c * r) ** 2 / (c ** 2 * y_ ** 2))
        pt_t = [sp.Rational(7, 10), sp.Rational(1, 2), 0]
        pt_e = [sp.Rational(7, 10), sp.Rational(1, 3), sp.Rational(5, 4)]
        Ks = []
        for (U, V) in [([1, 0, 0], [0, 1, 0]), ([1, 0, 0], [0, 0, 1]), ([0, 1, 0], [0, 0, 1]), ([1, 2, -1], [0, 1, 3])]:
            Ks.append(float(sect(Gt, [r, phi, tt], pt_t, U, V)))
            Ks.append(float(sect(Ge, [r, x_, y_], pt_e, U, V)))
        ok1 = max(abs(k + float(c) ** 2) for k in Ks) < 1e-9
        allok &= ok1
        # principal curvatures (1/2) d_r ln g_ii at the same r
        rv = sp.Rational(7, 10)
        pc_tube = [float(sp.Rational(1, 2) * sp.diff(sp.log(Gt[1, 1]), r).subs(r, rv)), float(sp.Rational(1, 2) * sp.diff(sp.log(Gt[2, 2]), r).subs(r, rv))]
        pc_eq = float(sp.Rational(1, 2) * sp.diff(sp.log(Ge[1, 1]), r).subs(r, rv))
        cf = float(c)
        okp = abs(pc_tube[0] - cf / np.tanh(cf * 0.7)) < 1e-9 and abs(pc_tube[1] - cf * np.tanh(cf * 0.7)) < 1e-9 and abs(pc_eq - cf * np.tanh(cf * 0.7)) < 1e-9
        allok &= okp
        rows.append("c=%g: 8 sectional curvatures of the tube/equidistant ambient metrics all equal -c^2 (max dev %s); principal curvatures c coth(cd), c tanh(cd), c tanh(cd) at d=0.7 reproduced"
                    % (cf, up(max(abs(k + cf ** 2) for k in Ks), 2)))
    # horosphere in the upper half space: z = z0 ; kappa = c ; intrinsic curvature 0
    z0 = sp.symbols("z0", positive=True)
    c_ = sp.Rational(3, 2)
    g_xx = 1 / (c_ ** 2 * z0 ** 2)
    kap_h = sp.simplify(-sp.Rational(1, 2) * (c_ * z0) * sp.diff(g_xx, z0) / g_xx)   # unit normal nu = c z d_z
    # Clifford torus in S^3 by embedding
    u, v = sp.symbols("u v")
    X = sp.Matrix([sp.cos(u), sp.sin(u), sp.cos(v), sp.sin(v)]) / sp.sqrt(2)
    nu = sp.Matrix([sp.cos(u), sp.sin(u), -sp.cos(v), -sp.sin(v)]) / sp.sqrt(2)
    Xu, Xv = X.diff(u), X.diff(v)
    g = sp.Matrix([[Xu.dot(Xu), Xu.dot(Xv)], [Xv.dot(Xu), Xv.dot(Xv)]])
    II = sp.Matrix([[X.diff(u, 2).dot(nu), X.diff(u).diff(v).dot(nu)], [X.diff(u).diff(v).dot(nu), X.diff(v, 2).dot(nu)]])
    S = sp.simplify(g.inv() * II)
    eig = sorted([float(e) for e in S.eigenvals().keys()])
    Kint = float(sp.simplify(1 + S.det()))
    claim("C8.1", "chap08.tex:174-190, 192-205 (Thm sectional_extrinsic; hyperbolic and spherical examples)",
          "K_M = Kbar + kappa^2; horosphere kappa=c, K_M=0; equidistant c tanh(cd); tube c coth(cd) (mult. n-2) and c tanh(cd); Clifford torus principal curvatures +-1, K=0",
          abs(ks - 1) < 1e-9 and allok and abs(abs(float(kap_h)) - float(c_)) < 1e-12 and abs(eig[0] + 1) < 1e-12 and abs(eig[1] - 1) < 1e-12 and abs(Kint) < 1e-12,
          "sympy Riemann tensors of the explicit ambient metrics (convention: unit S^2 gives %s); %s; horosphere z=z0 of H^3(-9/4): |kappa| = %s = c; Clifford torus eigenvalues of the shape operator %s, intrinsic K = Kbar + det = %s"
          % (up(ks, 6), " ; ".join(rows), up(abs(float(kap_h)), 6), eig, up(abs(Kint), 2)),
          "the mutated coupling K_M = Kbar - kappa^2 must give a non-zero curvature for the horosphere and the Clifford torus",
          abs((-float(c_) ** 2) - float(c_) ** 2) > 1 and abs(1 - (-1)) > 1,
          "horosphere: -c^2 - c^2 = %s != 0 ; Clifford torus: 1 - det... = 2 != 0" % up(-2 * float(c_) ** 2, 4))

    # small spheres (cot) by embedding : circle of geodesic radius R on S^2 of radius 1/c
    cc = 1.7
    R = 0.6
    sphereR = 1 / cc
    s = sp.symbols("s")
    # circle of colatitude theta0 = c R on the sphere of radius 1/c
    th0 = cc * R
    P = sp.Matrix([sphereR * sp.sin(th0) * sp.cos(s), sphereR * sp.sin(th0) * sp.sin(s), sphereR * sp.cos(th0)])
    acc = P.diff(s, 2)
    Nn = P / sphereR
    tang = acc - acc.dot(Nn) * Nn
    kg = float(sp.sqrt(tang.dot(tang)).subs(s, 0.3) / sp.sqrt(P.diff(s).dot(P.diff(s))).subs(s, 0.3) ** 2)
    claim("C8.2", "chap08.tex:214-216, 573 (small spheres, table row Sph^n)",
          "geodesic circle of radius R in S^2(+c^2) has curvature c cot(cR), -> 1/R as R->0",
          abs(kg - cc / np.tan(cc * R)) < 1e-10,
          "embedding in R^3 (sphere of radius 1/c, c=1.7, R=0.6): tangential acceleration / speed^2 = %s vs c cot(cR) = %s" % (up(kg, 10), up(cc / np.tan(cc * R), 10)),
          "c tan(cR) instead of c cot(cR) must disagree", abs(kg - cc * np.tan(cc * R)) > 0.1, "c tan(cR) = %s" % up(cc * np.tan(cc * R), 6))


# ---------------- U-turns ----------------
def make_geometry(kind, c):
    if kind == "R2":
        return (lambda y: 1.0 + 0 * y), (lambda y: 0.0 * y), (lambda w: 2.0 / w)
    if kind == "H2":
        return (lambda y: np.cosh(c * y)), (lambda y: c * np.sinh(c * y)), (lambda w: c / np.tanh(c * w / 2))
    return (lambda y: np.cos(c * y)), (lambda y: -c * np.sin(c * y)), (lambda w: c / np.tan(c * w / 2))


def simulate(kappas, L, y0, G, Gp, nsub=4):
    N = len(kappas)
    h = L / N / nsub
    y, th = y0, 0.0
    ys = []
    for k in kappas:
        for _ in range(nsub):
            f = lambda yy, tt: (np.sin(tt), k + Gp(yy) / G(yy) * np.cos(tt))
            a1 = f(y, th); a2 = f(y + h / 2 * a1[0], th + h / 2 * a1[1])
            a3 = f(y + h / 2 * a2[0], th + h / 2 * a2[1]); a4 = f(y + h * a3[0], th + h * a3[1])
            y += h / 6 * (a1[0] + 2 * a2[0] + 2 * a3[0] + a4[0]); th += h / 6 * (a1[1] + 2 * a2[1] + 2 * a3[1] + a4[1])
            ys.append(y)
    return np.array(ys), th


def section_uturn():
    # (a) geodesic half-circle: constant curvature c coth(cw/2) from y=-w/2 stays at distance w/2 from the centre
    def halfcircle(kind, c, w, kap):
        G, Gp, bound = make_geometry(kind, c)
        hh = 1e-3
        y, th, x = -w / 2, 0.0, 0.0
        dmax = 0.0
        steps = 0
        while th < np.pi and steps < 400000:
            f = lambda yy, tt, xx: (np.sin(tt), kap + Gp(yy) / G(yy) * np.cos(tt), np.cos(tt) / G(yy))
            a1 = f(y, th, x); a2 = f(y + hh / 2 * a1[0], th + hh / 2 * a1[1], x + hh / 2 * a1[2])
            a3 = f(y + hh / 2 * a2[0], th + hh / 2 * a2[1], x + hh / 2 * a2[2]); a4 = f(y + hh * a3[0], th + hh * a3[1], x + hh * a3[2])
            y += hh / 6 * (a1[0] + 2 * a2[0] + 2 * a3[0] + a4[0]); th += hh / 6 * (a1[1] + 2 * a2[1] + 2 * a3[1] + a4[1]); x += hh / 6 * (a1[2] + 2 * a2[2] + 2 * a3[2] + a4[2])
            steps += 1
            # geodesic distance from the origin of Fermi coordinates (x=0,y=0)
            if kind == "H2":
                d = np.arccosh(np.cosh(c * y) * np.cosh(c * x)) / c
            else:
                d = np.arccos(np.cos(c * y) * np.cos(c * x)) / c
            if th < np.pi:
                dmax = max(dmax, abs(d - w / 2))
        return dmax, y, bound(w)
    rows = []
    allok = True
    for kind, c, w in [("H2", 1.0, 1.3), ("H2", 2.0, 0.9), ("S2", 1.0, 2.0), ("S2", 1.5, 1.0)]:
        dmax, y, kap = halfcircle(kind, c, w, make_geometry(kind, c)[2](w))
        allok &= dmax < 2e-5 and abs(y - w / 2) < 2e-3
        rows.append("%s c=%g w=%g: kappa=%s, max | dist(centre) - w/2 | = %s, end y = %s" % (kind, c, w, up(kap, 6), up(dmax, 2), up(y, 5)))
    # (R2) control with the SAME integrator: the Euclidean curvature 2/w on H^2 (c=1, w=1.3) must leave the circle
    dmax_bad, y_bad, kap_good = halfcircle("H2", 1.0, 1.3, 2 / 1.3)
    claim("C8.3", "chap08.tex:224-246 (Thm space_form_uturn, equality case)",
          "the half geodesic circle of radius w/2 centred on sigma has constant curvature c coth(cw/2) (H^2) / c cot(cw/2) (S^2) and runs from y=-w/2 to y=w/2",
          allok, "; ".join(rows) + " (integration of theta' = kappa + (G'/G) cos theta in Fermi coordinates vs the closed-form geodesic distance from the centre)",
          "the SAME Fermi integrator with the Euclidean curvature 2/w on H^2 (c=1, w=1.3) must leave the circle: max |dist - w/2| > 1e-2 or end height != w/2",
          dmax_bad > 1e-2 or abs(y_bad - 1.3 / 2) > 1e-2,
          "kappa=2/w=%s: max |dist(centre) - w/2| = %s, end y = %s (vs w/2 = 0.65; the true kappa is %s)" % (up(2 / 1.3, 5), dn(dmax_bad, 3), up(y_bad, 5), up(kap_good, 5)))

    # (b) optimal control: minimise the peak curvature of U-turns in the tube (piecewise-constant curvature, SLSQP, 3 starts)
    out = []
    ok = True
    ctrl = True
    mut09 = True
    mut_info = []
    for kind, c, w in [("R2", 0.0, 1.0), ("H2", 1.0, 1.3), ("S2", 1.0, 2.0)]:
        G, Gp, bound = make_geometry(kind, c)
        bnd = bound(w)
        N = 24
        best = 1e9
        for start in range(3):
            fac = [1.25, 1.6, 2.2][start]
            kap0 = bnd * fac
            v0 = np.concatenate([[kap0, np.pi / kap0 * 1.05, -w / 2 * 0.5 + (start - 1) * 0.05], np.full(N, kap0) * (1 + 0.05 * rng.standard_normal(N))])
            def cons_ineq(v):
                t, L, y0 = v[0], v[1], v[2]
                ks = v[3:]
                ys, th = simulate(ks, L, y0, G, Gp, nsub=3)
                return np.concatenate([t - ks, t + ks, w / 2 - ys, w / 2 + ys])
            def cons_eq(v):
                t, L, y0 = v[0], v[1], v[2]
                ys, th = simulate(v[3:], L, y0, G, Gp, nsub=3)
                return np.array([th - np.pi])
            res = minimize(lambda v: v[0], v0, method="SLSQP",
                           constraints=[dict(type="ineq", fun=cons_ineq), dict(type="eq", fun=cons_eq)],
                           bounds=[(0.05, 20), (0.2, 20), (-w / 2, w / 2)] + [(-20, 20)] * N, options=dict(maxiter=400, ftol=1e-12))
            viol = max(0.0, -cons_ineq(res.x).min(), abs(cons_eq(res.x)[0]))
            if viol < 1e-6:
                best = min(best, res.x[0])
        out.append("%s: SLSQP optimum %s vs closed-form bound %s" % (kind, up(best, 6), up(bnd, 6)))
        ok &= best >= bnd * (1 - 1e-6) and best <= bnd * 1.02
        ctrl &= (best > 0.98 * bnd) and (best < 1.1 * bnd)
        mut09 &= not (best >= 0.9*bnd*(1-1e-6) and best <= 0.9*bnd*1.02)    # mutant 'the minimum is 0.9 x bound' (bound 0.9*c*coth(cw/2)): the optimiser must NOT reach 0.9 x bound
        mut_info.append('%s: optimum/bound = %s' % (kind, up(best / bnd, 5)))    # the optimiser finds FEASIBLE U-turns below 1.1 x bound, so the mutant 'minimum = 1.1 x bound' is false
    claim("C8.4", "chap08.tex:224-246 and 248-253 (U-turn minimality; 'search with 0.98k finds none')",
          "the minimal peak curvature of U-turns in the tube T_w is 2/w (R^2), c coth(cw/2) (H^2), c cot(cw/2) (S^2); no U-turn exists with 0.98 of it",
          ok, "; ".join(out) + " (24 constant-curvature pieces, free length and start height, 3 starts each; feasible solutions only, violation < 1e-6)",
          "EVIDENCE (SLSQP is an optimiser, not a certificate; the proof is in the text).  Mutants: 0.9 x bound and 0.98 x bound must be unattainable (optimum > 0.98 x bound), and the upward mutant 'the minimum is 1.1 x bound' must be false (a feasible U-turn with peak < 1.1 x bound exists)",
          ctrl and mut09, "optimum in (0.98, 1.1) x bound in all three geometries; mutant 'bound = 0.9 x c coth(cw/2)' is not attained by the optimiser (optimum > 0.9 x bound): " + '; '.join(mut_info))
    return


# ---------------- ADM corollary ----------------
def section_adm():
    kap = Fraction(7, 3)
    vals = []
    for signs in itertools.product((-1, 1), repeat=3):
        lam = [s * kap for s in signs]
        e2 = lam[0] * lam[1] + lam[1] * lam[2] + lam[2] * lam[0]
        vals.append(e2)
    lo, hi = min(vals), max(vals)
    ok = lo == -kap ** 2 and hi == 3 * kap ** 2
    # random interior points and identity R - 16 pi G rho = -2 e2 = sum lam^2 - (sum lam)^2
    worst_lo, worst_hi = 1e9, -1e9
    idok = True
    sig_ok = True
    for _ in range(20000):
        lam = rng.uniform(-1, 1, 3) * float(kap)
        e2 = lam[0] * lam[1] + lam[1] * lam[2] + lam[2] * lam[0]
        R_minus = np.sum(lam ** 2) - np.sum(lam) ** 2
        idok &= abs(R_minus + 2 * e2) < 1e-12
        worst_lo = min(worst_lo, -2 * e2); worst_hi = max(worst_hi, -2 * e2)
        sig = np.sum(lam ** 2) - np.sum(lam) ** 2 / 3
        sig_ok &= sig <= 3 * float(kap) ** 2 - np.sum(lam) ** 2 / 3 + 1e-12 and np.sum(lam ** 2) <= 3 * float(kap) ** 2 + 1e-12
    inside = worst_lo >= -6 * float(kap) ** 2 - 1e-9 and worst_hi <= 2 * float(kap) ** 2 + 1e-9
    claim("C8.5", "chap08.tex:290-303 (Cor adm_bounds)",
          "if |lambda_i| <= kappa then K_ij K^ij <= 3 kappa^2, sigma sigma <= 3kappa^2 - K^2/3 and 16 pi G rho - 6 kappa^2 <= R <= 16 pi G rho + 2 kappa^2 with all bounds sharp",
          ok and idok and sig_ok and inside and (-2 * hi == -6 * kap ** 2) and (-2 * lo == 2 * kap ** 2),
          "exact rational enumeration of the 8 cube vertices (kappa=7/3): e2 in [%s, %s] = [-kappa^2, 3kappa^2]; 20000 random points: R-16 pi G rho in [%s, %s] subset of [-6 kappa^2, 2 kappa^2] = [%s, %s]"
          % (lo, hi, dn(worst_lo, 5), up(worst_hi, 5), -6 * kap ** 2, 2 * kap ** 2),
          "the mutated upper bound R <= 16 pi G rho + kappa^2 (instead of 2 kappa^2) must be violated at a vertex",
          -2 * lo > kap ** 2, "DECLARED: the control compares the exactly enumerated vertex value 2 kappa^2 = %s with the mutant constant kappa^2 = %s" % (2 * kap ** 2, kap ** 2))


# ---------------- Minkowski hyperboloid, Schwarzschild maximal slice ----------------
def section_gr():
    # hyperboloid t^2 - x^2 = tau0^2 : K_ij = -gamma_ij/tau0 (finite differences of the unit normal in Minkowski space)
    tau0 = 1.7
    def X(chi, a, b):
        return np.array([tau0 * np.cosh(chi), tau0 * np.sinh(chi) * np.sin(a) * np.cos(b), tau0 * np.sinh(chi) * np.sin(a) * np.sin(b), tau0 * np.sinh(chi) * np.cos(a)])
    eta = np.diag([-1.0, 1, 1, 1])
    p = np.array([0.8, 1.1, 0.5])
    h = 1e-5
    E = []
    for i in range(3):
        d = np.zeros(3); d[i] = h
        E.append((X(*(p + d)) - X(*(p - d))) / (2 * h))
    nvec = lambda q: X(*q) / tau0
    K = np.zeros((3, 3)); gam = np.zeros((3, 3))
    for i in range(3):
        d = np.zeros(3); d[i] = h
        dn_ = (nvec(p + d) - nvec(p - d)) / (2 * h)
        for j in range(3):
            K[i, j] = -(dn_ @ eta @ E[j])
            gam[i, j] = E[i] @ eta @ E[j]
    err = np.max(np.abs(K + gam / tau0))
    claim("C8.6", "chap08.tex:271-273, 573 (K_ij = -gamma_ij/tau for hyperboloids; table row Minkowski)",
          "hyperboloid t^2-|x|^2=tau_0^2 has K_ij = -gamma_ij/tau_0, so ||II||_op = 1/tau_0",
          err < 1e-6, "finite differences of the unit normal n=x/tau_0 in R^{1,3} (tau_0=1.7): max |K_ij + gamma_ij/tau_0| = %s" % up(err, 2),
          "K_ij = +gamma_ij/tau_0 (opposite sign) must disagree", np.max(np.abs(K - gam / tau0)) > 0.1, "mutated error %s" % dn(np.max(np.abs(K - gam / tau0)), 3))

    # Painleve-Gullstrand horizon
    r, M, Q = sp.symbols("r M Q", positive=True)
    f = 1 - 2 * M / r + Q ** 2 / r ** 2
    beta = sp.sqrt(2 * M / r - Q ** 2 / r ** 2)
    # (i) PG -> RN: dT = dt + beta/f dr
    dt_, dr_ = sp.symbols("dt dr")
    dT = dt_ + beta / f * dr_
    ds2 = sp.simplify(-dT ** 2 + (dr_ + beta * dT) ** 2)
    ds2_expected = -f * dt_ ** 2 + dr_ ** 2 / f
    diff_ds = sp.simplify(sp.expand(ds2 - ds2_expected))
    # (ii) (R2) theta_l from the FULL 4D Painleve-Gullstrand metric in (T,r,theta,phi): g_TT=-(1-beta^2), g_Tr=beta, g_rr=1.
    #      Outgoing null vector l = d_T + (1-beta) d_r.  theta_l = q^{ab} nabla_a l_b with q the projector on the 2-sphere (angular block), and
    #      second route theta_l = div(l) - kappa_l (kappa_l = inaffinity: l^nu nabla_nu l^mu = kappa_l l^mu).
    Tt, rv, thv, phv = sp.symbols("T rv thv phv", positive=True)
    bfun = sp.Function("beta")(rv)
    X4 = [Tt, rv, thv, phv]
    g4 = sp.Matrix([[-(1 - bfun ** 2), bfun, 0, 0], [bfun, 1, 0, 0], [0, 0, rv ** 2, 0], [0, 0, 0, rv ** 2 * sp.sin(thv) ** 2]])
    g4i = sp.simplify(g4.inv())
    G4 = [[[sp.simplify(sum(g4i[i, l] * (sp.diff(g4[l, k], X4[j]) + sp.diff(g4[l, j], X4[k]) - sp.diff(g4[j, k], X4[l])) for l in range(4)) / 2)
            for k in range(4)] for j in range(4)] for i in range(4)]

    def expansion(lvec):
        lv = sp.Matrix(lvec)                       # contravariant l^mu
        low = g4 * lv                              # l_mu
        nab = lambda a_, b_: sp.diff(low[b_], X4[a_]) - sum(G4[m_][a_][b_] * low[m_] for m_ in range(4))
        th_proj = sp.simplify(g4i[2, 2] * nab(2, 2) + g4i[3, 3] * nab(3, 3))
        divl = sp.simplify(sum(sp.diff(lv[m_], X4[m_]) for m_ in range(4)) + sum(G4[m_][m_][n_] * lv[n_] for m_ in range(4) for n_ in range(4)))
        acc = [sp.simplify(sum(lv[n_] * sp.diff(lv[m_], X4[n_]) for n_ in range(4)) + sum(G4[m_][n_][q_] * lv[n_] * lv[q_] for n_ in range(4) for q_ in range(4))) for m_ in range(4)]
        kap_l = sp.simplify(acc[0] / lv[0])
        return th_proj, sp.simplify(divl - kap_l), sp.simplify((lv.T * g4 * lv)[0, 0]), acc, lv
    lout = [1, 1 - bfun, 0, 0]
    th_proj, th_div, gll, acc_out, lvo = expansion(lout)
    acc_ratio_ok = all(sp.simplify(acc_out[m_] * lvo[0] - acc_out[0] * lvo[m_]) == 0 for m_ in range(4))   # acceleration parallel to l
    chk = sp.simplify(th_proj - 2 * (1 - bfun) / rv)
    chk2 = sp.simplify(th_div - 2 * (1 - bfun) / rv)
    nullchk = sp.simplify(gll)
    # ingoing null vector n = d_T - (1+beta) d_r: theta_n = -2(1+beta)/r (does NOT vanish at r_+) -- used as the control
    nin = [1, -(1 + bfun), 0, 0]
    th_in, _, gnn, _, _ = expansion(nin)
    th_in_ok = sp.simplify(th_in + 2 * (1 + bfun) / rv) == 0 and sp.simplify(gnn) == 0
    # principal curvatures of the sphere r = const in the slice T = const: induced slice metric gamma = diag(1, r^2, r^2 sin^2), unit normal d_r
    gam3 = sp.diag(1, rv ** 2, rv ** 2 * sp.sin(thv) ** 2)
    II_ang = [sp.simplify(sp.diff(gam3[a_, a_], rv) / 2 / gam3[a_, a_]) for a_ in (1, 2)]
    curv_ok = all(sp.simplify(c_ - 1 / rv) == 0 for c_ in II_ang)
    # horizon: beta(r_+) = 1 for several (M,Q)
    okh = True
    rows = []
    for Mv, Qv in [(1.0, 0.0), (1.0, 0.6), (2.0, 1.99)]:
        rp = Mv + np.sqrt(Mv ** 2 - Qv ** 2)
        b = float(beta.subs({M: Mv, Q: Qv, r: rp}))
        okh &= abs(b - 1) < 1e-12 and rp > Qv ** 2 / (2 * Mv)
        rows.append("(M,Q)=(%g,%g): r_+=%s beta(r_+)=%s, Q^2/2M=%s" % (Mv, Qv, up(rp, 6), up(b, 12), up(Qv ** 2 / (2 * Mv), 4)))
    # time-independent flat slice: gamma_ij = diag(1, r^2, r^2 sin^2) is flat (Riemann zero)
    rr, tth, pph = sp.symbols("rr tth pph", positive=True)
    Gs = sp.diag(1, rr ** 2, rr ** 2 * sp.sin(tth) ** 2)
    k_flat = max(abs(float(sect(Gs, [rr, tth, pph], [sp.Rational(3, 2), sp.Rational(7, 10), sp.Rational(1, 3)], U, V)))
                 for U, V in [([1, 0, 0], [0, 1, 0]), ([0, 1, 0], [0, 0, 1]), ([1, 0, 0], [0, 0, 1]), ([1, 1, 0], [0, 1, 2])])
    claim("C8.7", "chap08.tex:337-352 (Prop rn_horizon)",
          "PG line element reproduces RN (g_TT=-f), T=const slices are flat, theta_l = 2(1-beta)/r vanishes at r_+ (beta(r_+)=1), horizon curvature 1/r_+; r_+ lies in the validity range r > Q^2/(2M)",
          diff_ds == 0 and chk == 0 and chk2 == 0 and nullchk == 0 and okh and k_flat < 1e-9 and curv_ok and th_in_ok and acc_ratio_ok,
          "sympy on the full 4D PG metric: ds^2_PG(T=t+int beta/f) - ds^2_RN = %s ; theta_l = q^ab nabla_a l_b minus 2(1-beta)/r = %s ; theta_l = div l - kappa_l minus 2(1-beta)/r = %s ; g(l,l) = %s ; "
          "acceleration l^nu nabla_nu l parallel to l: %s ; principal curvatures of r=const in the slice (1/2) gamma^aa d_r gamma_aa = 1/r (checked symbolically): %s ; %s ; slice sectional curvatures max |K| = %s"
          % (diff_ds, chk, chk2, nullchk, acc_ratio_ok, curv_ok, " | ".join(rows), up(k_flat, 2)),
          "the INGOING null vector n = d_T - (1+beta) d_r (null; same machinery) has theta_n = -2(1+beta)/r, which must NOT vanish at r_+ (it is -4/r_+ there)",
          th_in_ok and abs(float((-2 * (1 + beta) / r).subs({M: 1.0, Q: 0.6, r: 1 + np.sqrt(1 - 0.36)}))) > 1.0,
          "theta_n(r_+) = %s" % up(float((-2 * (1 + beta) / r).subs({M: 1.0, Q: 0.6, r: 1 + np.sqrt(1 - 0.36)})), 5))

    # Schwarzschild limiting maximal slice
    Cc = sp.symbols("C", positive=True)
    rr_ = sp.symbols("rr_", positive=True)
    poly = sp.expand(rr_ ** 4 * (1 - 2 * M / rr_) + Cc ** 2)
    crit = [c_ for c_ in sp.solve(sp.diff(poly, rr_), rr_) if c_ != 0]
    r_star = crit[0]
    Cval = sp.sqrt(-(r_star ** 4 - 2 * M * r_star ** 3))
    Kmax = sp.simplify(2 * Cval / r_star ** 3 - 4 * sp.sqrt(3) / (9 * M))
    kappa_f = sp.Function("kappa")
    rs = sp.symbols("rs", positive=True)
    ode = sp.Eq(-2 * kappa_f(rs).diff(rs) + 2 / rs * (-2 * kappa_f(rs) - kappa_f(rs)), 0)
    sol = sp.dsolve(ode, kappa_f(rs))
    hh = 1 - 2 * M / rs + Cc ** 2 / rs ** 4
    Rgamma = sp.simplify(2 * (1 - hh - rs * sp.diff(hh, rs)) / rs ** 2)
    KK = sp.simplify(6 * (Cc / rs ** 3) ** 2)
    ham = sp.simplify(Rgamma - KK)
    claim("C8.8", "chap08.tex:517, 573 (maximal slicing; table row Schwarzschild)",
          "the limiting maximal slice sits at r=3M/2 with C=3 sqrt3 M^2/4, |K^r_r| = 3 sqrt3 M^2/(2 r^3) <= 4 sqrt3/(9M), attained at r=3M/2",
          sp.simplify(r_star - 3 * M / 2) == 0 and sp.simplify(Cval - 3 * sp.sqrt(3) * M ** 2 / 4) == 0 and Kmax == 0 and ham == 0 and sp.simplify(sol.rhs * rs ** 3 - sp.Symbol("C1")) == 0,
          "sympy: double root of r^4 f + C^2 at r*=%s, C=%s; momentum constraint for the trace-free K gives kappa ~ r^{-3} (%s); Hamiltonian constraint R^(gamma) = K_ij K^ij = 6C^2/r^6: residual %s; |K^r_r|(3M/2) = 2C/r*^3 = 4 sqrt3/(9M)"
          % (r_star, Cval, sol.rhs, ham),
          "a different limiting radius r=2M must not be a double root of r^4 f + C^2 (derivative non-zero there)",
          sp.simplify(sp.diff(poly, rr_).subs(rr_, 2 * M)) != 0, "d/dr (r^4 f) at r=2M = %s != 0" % sp.simplify(sp.diff(poly, rr_).subs(rr_, 2 * M)))


# ---------------- wormhole ----------------
def section_wormhole():
    t, r, th, ph = sp.symbols("t r theta phi")
    b = sp.Function("b")(r)
    Phi = sp.Function("Phi")(r)
    coords = [t, r, th, ph]
    g = sp.diag(-sp.exp(2 * Phi), 1 / (1 - b / r), r ** 2, r ** 2 * sp.sin(th) ** 2)
    gi = g.inv()
    n = 4
    Gam = [[[sum(gi[i, l] * (sp.diff(g[l, k], coords[j]) + sp.diff(g[l, j], coords[k]) - sp.diff(g[j, k], coords[l])) for l in range(n)) / 2
             for k in range(n)] for j in range(n)] for i in range(n)]
    def Ric(j, k):
        s_ = 0
        for i in range(n):
            s_ += sp.diff(Gam[i][j][k], coords[i]) - sp.diff(Gam[i][i][k], coords[j])
            for m in range(n):
                s_ += Gam[i][i][m] * Gam[m][j][k] - Gam[i][j][m] * Gam[m][i][k]
        return sp.simplify(s_)
    Rm = sp.Matrix(4, 4, lambda j, k: Ric(j, k) if j == k else 0)
    Rs = sp.simplify(sum(gi[i, i] * Rm[i, i] for i in range(4)))
    Gmix = sp.Matrix(4, 4, lambda j, k: sp.simplify(gi[j, j] * Rm[j, k] - (Rs / 2 if j == k else 0)))
    rho8 = sp.simplify(-Gmix[0, 0])          # 8 pi G rho = -G^t_t
    pr8 = sp.simplify(Gmix[1, 1])            # 8 pi G p_r = G^r_r
    rho_exp = sp.diff(b, r) / r ** 2
    pr_exp = -b / r ** 3 + 2 * (1 - b / r) * sp.diff(Phi, r) / r
    e1 = sp.simplify(rho8 - rho_exp)
    e2 = sp.simplify(pr8 - pr_exp)
    # (R2) throat: substitute b(r0)=r0 into the symbolic Einstein tensor and compare with -(1-b')/(8 pi G r0^2); K_Gauss from the geometry of the 2-sphere
    r0, bp0 = sp.symbols("r0 bp0", positive=True)
    sum8 = sp.simplify(rho8 + pr8)
    sum8_thr = sp.simplify(sum8.subs(sp.Derivative(b, r), bp0).subs(b, r).subs(r, r0))
    thr_ok = sp.simplify(sum8_thr + (1 - bp0) / r0 ** 2) == 0
    th0, ph0 = sp.symbols("th0 ph0", positive=True)
    Gsph_num = sp.diag(sp.Rational(13, 10) ** 2, sp.Rational(13, 10) ** 2 * sp.sin(th0) ** 2)
    KG = float(sect(Gsph_num, [th0, ph0], [sp.Rational(7, 10), sp.Rational(1, 3)], [1, 0], [0, 1]))   # Gauss curvature of the round sphere of radius r0=1.3
    r0v = 1.3
    ok_ineq = abs(KG - 1 / r0v ** 2) < 1e-9
    for bp in np.linspace(0.0, 0.999, 500):
        lhs = float(sum8_thr.subs({bp0: bp, r0: r0v}))          # 8 pi G (rho + p_r) at the throat, from the symbolic tensor
        rhs = -KG                                                  # -8 pi G * K_Gauss/(8 pi G)
        ok_ineq &= lhs >= rhs - 1e-12 and (abs(lhs - rhs) < 1e-12) == (bp == 0.0)
    lhs_bad = float(sum8_thr.subs({bp0: -0.5, r0: r0v}))
    kcurv = sp.simplify(sp.sqrt(1 - b / r) / r)
    pc_ok = sp.simplify(kcurv.subs(b, r)) == 0
    claim("C8.9", "chap08.tex:381-400 (Prop wormhole_throat)",
          "Morris-Thorne: 8 pi G rho = b'/r^2, 8 pi G p_r = -b/r^3 + 2(1-b/r)Phi'/r; at the throat rho+p_r = -(1-b')/(8 pi G r0^2) >= -K_Gauss/(8 pi G) iff 0<=b'(r0)<1 (equality iff b'=0)",
          e1 == 0 and e2 == 0 and thr_ok and ok_ineq and pc_ok,
          "sympy Einstein tensor of the metric with arbitrary b(r), Phi(r): 8 pi G rho - b'/r^2 = %s ; 8 pi G p_r - (...) = %s ; with b(r0)=r0 the symbolic 8 pi G(rho+p_r) + (1-b')/r0^2 = 0: %s ; "
          "K_Gauss of the round 2-sphere of radius r0=1.3 computed from its metric = %s (1/r0^2 = %s); on 500 values b' in [0,0.999], 8 pi G(rho+p_r) >= -K_Gauss with equality only at b'=0: %s ; throat principal curvature sqrt(1-b/r)/r vanishes at b=r: %s"
          % (e1, e2, thr_ok, up(KG, 8), up(1 / r0v ** 2, 8), ok_ineq, pc_ok),
          "for b' = -0.5 the SYMBOLIC result must violate the bound: 8 pi G(rho+p_r) < -K_Gauss",
          lhs_bad < -KG - 1e-3, "b'=-0.5: 8 pi G(rho+p_r) = %s < -K_Gauss = %s" % (up(lhs_bad, 6), up(-KG, 6)))


# ---------------- numbers: slingshot, Planck, conformal ----------------
def section_numbers():
    # slingshot remark
    f_ = lambda r: np.sqrt(1 - 2 / r) / r        # M = 1
    res = minimize_scalar(lambda r: -f_(r), bounds=(2.0, 20.0), method="bounded", options=dict(xatol=1e-12))
    mx = -res.fun
    ang = 1 / (3 * np.sqrt(3))
    # random timelike worldlines: |dphi/dt| < sqrt(f)/r
    worst = 0.0
    for _ in range(200000):
        r = 2 + 10 ** rng.uniform(-3, 2)
        fr = 1 - 2 / r
        rdot = rng.uniform(-1, 1) * fr           # dr/dt
        # timelike: -f + rdot^2/f + r^2 phidot^2 < 0  -> r^2 phidot^2 < f - rdot^2/f
        lim = np.sqrt(max(fr - rdot ** 2 / fr, 0)) / r
        worst = max(worst, lim / (np.sqrt(fr) / r))
    Wmax = 100 / (6 * np.sqrt(3) * np.pi) + 0.5
    # brute force: windings W with |dphi| = |phi_q - phi_p + 2 pi W| < dt/(3 sqrt3), phi_q-phi_p in (-pi, pi]
    cnt = set()
    for dphi0 in np.linspace(-np.pi + 1e-9, np.pi, 4001):
        for W in range(-10, 11):
            if abs(dphi0 + 2 * np.pi * W) < 100 * ang:
                cnt.add(abs(W))
    claim("C8.10", "chap08.tex:458-466 (Remark: finitely many winding classes)",
          "max_{r>2M} sqrt(f)/r = 1/(3 sqrt3 M) at r=3M; |W| < dt/(6 sqrt3 pi M) + 1/2, so |W| <= 3 for dt=100M",
          abs(mx - ang) < 1e-12 and abs(res.x - 3.0) < 1e-4 and worst <= 1 + 1e-12 and Wmax < 4 and max(cnt) == 3,
          "bounded 1-D maximisation: max = %s at r=%s (1/(3 sqrt3) = %s); 2e5 random timelike velocities never exceed sqrt(f)/r (largest ratio %s); bound %s => |W|<=3; brute-force admissible |W| over the whole range of phi_q-phi_p: max %d"
          % (up(mx, 12), up(res.x, 6), up(ang, 12), up(worst, 6), up(Wmax, 4), max(cnt)),
          "a maximum at r=2M or the value 1/(2 sqrt3 M)... (r=4M) must fail", abs(f_(4.0) - ang) > 1e-3 and abs(f_(2.0001) - ang) > 0.1,
          "sqrt(f)/r at r=4M is %s and at r~2M is %s, both below 1/(3 sqrt3)=%s" % (up(f_(4.0), 6), up(f_(2.0001), 6), up(ang, 6)))

    # Planck density chain
    c = sc.c; hbar = sc.hbar; G = sc.G
    lP2 = hbar * G / c ** 3
    rhoP = c ** 7 / (hbar * G ** 2)
    bound = 3 * c ** 4 / (8 * np.pi * G * lP2)
    chain = 3 / (8 * np.pi) * rhoP
    # dimension check via exponent vectors (m, kg, s)
    dim = lambda m_, kg_, s_: np.array([m_, kg_, s_])
    dc, dh, dG = dim(1, 0, -1), dim(2, 1, -1), dim(3, -1, -2)
    d_rho = 7 * dc - dh - 2 * dG
    pascal = dim(-1, 1, -2)
    claim("C8.11", "chap08.tex:540-542 (Planck density bound)",
          "rho c^2 <= 3c^4/(8 pi G l_P^2) = 3/(8 pi) c^7/(hbar G^2) ~ 5.5e112 J m^-3, a fraction 3/(8 pi) of c^7/(hbar G^2) ~ 4.63e113 J m^-3 (Pa)",
          abs(bound / chain - 1) < 1e-12 and 5.45e112 < chain < 5.55e112 and 4.625e113 < rhoP < 4.635e113 and (d_rho == pascal).all(),
          "scipy.constants (CODATA): l_P^2 = hbar G/c^3 = %s m^2; c^7/(hbar G^2) = %s; 3/(8 pi) of it = %s; exponent vector of c^7 hbar^-1 G^-2 = (m,kg,s) %s = Pa" % (up(lP2, 5), up(rhoP, 5), up(chain, 4), list(d_rho)),
          "the Planck density without the 3/(8 pi) factor (4.63e113) must not equal 5.5e112",
          abs(rhoP / chain - 1) > 5, "ratio c^7/(hbar G^2) / bound = %s" % dn(rhoP / chain, 4))

    # conformal rescaling of principal curvatures: Poincare ball
    rows = []
    allok = True
    wrong = 1e9
    for R in (0.2, 0.5, 0.8):
        Om = lambda x: 2 / (1 - x ** 2)
        dOm = lambda x: 4 * x / (1 - x ** 2) ** 2
        kt = (1 / Om(R)) * (1 / R + dOm(R) / Om(R))
        rho_h = 2 * np.arctanh(R)
        allok &= abs(kt - 1 / np.tanh(rho_h)) < 1e-12
        wrong = min(wrong, abs(1 / (Om(R) * R) - 1 / np.tanh(rho_h)))
        rows.append("R=%g: %s vs coth(2 artanh R)=%s" % (R, up(kt, 10), up(1 / np.tanh(rho_h), 10)))
    claim("C8.12", "chap08.tex:546 (Remark conformal factor)",
          "under g~ = Omega^2 g principal curvatures transform as kappa~_i = kappa_i/Omega + n~(ln Omega) with n~ = Omega^{-1} n",
          allok, "Poincare disc/ball (Omega=2/(1-r^2)): Euclidean sphere of radius R has hyperbolic curvature coth(2 artanh R): " + "; ".join(rows),
          "dropping the n~(ln Omega) term must disagree", wrong > 1e-2, "min mismatch without the log-derivative term = %s" % dn(wrong, 3))

    # Israel thin shell: static shell, flat inside / Schwarzschild outside ; sign of the displayed formula
    Rsh = 5.0
    out = []
    ok = True
    for Mv in (1e-4, 0.3, 1.0):
        f = 1 - 2 * Mv / Rsh
        Kth_p = np.sqrt(f) / Rsh            # K^theta_theta = nabla_theta n_theta/r^2 outside (Israel convention K_ab = nabla_a n_b, n outward)
        Kth_m = 1.0 / Rsh
        Ktau_p = Mv / (Rsh ** 2 * np.sqrt(f))   # K^tau_tau = (f'/2)/sqrt f  with f' = 2M/R^2
        Ktau_m = 0.0
        jump_t, jump_th = Ktau_p - Ktau_m, Kth_p - Kth_m
        jump_K = jump_t + 2 * jump_th
        S_tautau = -(1 / (8 * np.pi)) * (jump_t - jump_K)          # displayed formula (Israel convention), G=1
        sigma = -S_tautau
        sigma_known = (1 - np.sqrt(f)) / (4 * np.pi * Rsh)         # Poisson's Toolkit (G=1)
        ok &= abs(sigma - sigma_known) < 1e-14 * max(1, abs(sigma_known)) * 1e3
        out.append("M=%g: sigma=%s (known %s), 4 pi R^2 sigma/M = %s" % (Mv, up(sigma, 8), up(sigma_known, 8), up(4 * np.pi * Rsh ** 2 * sigma / Mv, 6)))
    sigma_unrev = jump_th / (4 * np.pi)          # Sec. 4.1 convention K' = -K used with the UNREVERSED sign: negative energy density
    claim("C8.13", "chap08.tex:360-368 (Thm israel_junction and the stated sign reversal)",
          "with K_ab = h h nabla n (Israel) S_ab = -(1/8 pi G)([K_ab]-h_ab[K]); with the convention K_ab = -h h nabla n of Sec. 4.1 the sign is reversed (static shell, flat inside / Schwarzschild outside)",
          ok,
          "; ".join(out) + " (sigma>0 and the Newtonian limit 4 pi R^2 sigma -> M)",
          "the opposite sign (without reversing K) gives negative surface energy density",
          sigma_unrev < 0, "unreversed formula with K' = -K gives sigma = %s < 0" % up(sigma_unrev, 6))


def section_unchecked():
    unchecked("C8.U1", "chap08.tex:302-312 (Prop raychaudhuri)", "algebraic consequence of the cited Raychaudhuri equation (theta=0, omega=0 gives R_mn V V = -sigma^2); no numerical content beyond the identity itself")
    unchecked("C8.U2", "chap08.tex:430-437, 440-451 (Props bh_topology, causal_constraints)", "homotopy-theoretic and causal-structure statements (wedge of spheres, J^-(I+) transitivity); not numerical")
    unchecked("C8.U3", "chap08.tex:453-456, 470-476, 579-583 (Conjectures slingshot, regularity invariance; Remarks on status)", "open conjectures and heuristic remarks; the only numerical content (the winding bound) is C8.10")
    unchecked("C8.U4", "chap08.tex:481-509 (Bona-Masso barrier, GHY boundary action)", "conjectural; the displayed inequality |I_GHY| <= 3 K* Vol/(8 pi G) is the triangle inequality |tr K| <= 3||K||_op (rigorous by C8.5's cube argument: |sum lambda_i| <= 3 kappa)")
    unchecked("C8.U5", "chap08.tex:523-530 (Remark null curves)", "definitional (k lies in its own orthogonal complement)")
    unchecked("C8.U6", "chap08.tex:511-520 (LQC remark)", "phenomenological parallel with the effective Friedmann equation; no claim with numerical content")


if __name__ == "__main__":
    section_forms()
    section_uturn()
    section_adm()
    section_gr()
    section_wormhole()
    section_numbers()
    section_unchecked()
    finish("8")
