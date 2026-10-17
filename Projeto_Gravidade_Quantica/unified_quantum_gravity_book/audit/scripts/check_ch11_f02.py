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
# Chapter 11 body.  Source: chap11_emergent_spacetime_tensor_networks_holonomies.tex (3.0.0)
# ======================================================================
import numpy as np
import scipy.linalg as sla
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq
from scipy.special import betainc
import mpmath as mp
import sympy as sp

rng = np.random.default_rng(20261016)


def rand_state(n, g=None):
    g = rng if g is None else g
    A = g.standard_normal((n, n)) + 1j * g.standard_normal((n, n))
    rho = A @ A.conj().T
    return rho / np.trace(rho).real


def rand_traceless(n, g=None):
    g = rng if g is None else g
    A = g.standard_normal((n, n)) + 1j * g.standard_normal((n, n))
    X = (A + A.conj().T) / 2
    return X - np.trace(X) / n * np.eye(n)


def logm_h(rho):
    w, V = np.linalg.eigh(rho)
    return (V * np.log(w)) @ V.conj().T


def vn(rho):
    w = np.linalg.eigvalsh(rho)
    return -np.sum(w * np.log(w))


def rel_ent(rho, sig):
    return np.trace(rho @ (logm_h(rho) - logm_h(sig))).real


def g_bkm_eig(rho, X):
    p, V = np.linalg.eigh(rho)
    Xe = V.conj().T @ X @ V
    P1, P2 = np.meshgrid(p, p, indexing="ij")
    with np.errstate(divide="ignore", invalid="ignore"):
        lm = np.where(np.abs(P1 - P2) > 1e-14, (np.log(P1) - np.log(P2)) / (P1 - P2), 1.0 / P1)
    return float(np.sum(lm * np.abs(Xe) ** 2))


def g_sld_eig(rho, X):
    p, V = np.linalg.eigh(rho)
    Xe = V.conj().T @ X @ V
    P1, P2 = np.meshgrid(p, p, indexing="ij")
    return float(np.sum(2.0 / (P1 + P2) * np.abs(Xe) ** 2))


def section_information():
    n = 3
    rho0 = 0.8 * rand_state(n) + 0.2 * np.eye(n) / n; X = rand_traceless(n)
    X = X / np.linalg.norm(X) * 0.3
    # first and second derivative of S(rho0 + lam X || rho0) at lam = 0 (Richardson of central differences, mpmath-free)
    F = lambda lam: rel_ent(rho0 + lam * X, rho0)
    def d1(h):
        return (F(h) - F(-h)) / (2 * h)
    def d2(h):
        return (F(h) - 2 * F(0) + F(-h)) / h ** 2
    d1v = d1(1e-4)
    d2v = (4 * d2(5e-4) - d2(1e-3)) / 3
    bkm = g_bkm_eig(rho0, X)
    sld = g_sld_eig(rho0, X)
    # integral formula
    integ = quad(lambda s: np.trace(X @ np.linalg.inv(s * np.eye(n) + rho0) @ X @ np.linalg.inv(s * np.eye(n) + rho0)).real, 0, np.inf, epsabs=1e-12, epsrel=1e-12, limit=400)[0]
    # SLD via Sylvester: rho L + L rho = 2 X ; g = Tr(L X)
    L = sla.solve_sylvester(rho0, rho0, 2 * X)
    sld2 = np.trace(L @ X).real
    claim("C11.1", "chap11.tex:149-160 (Prop relative_entropy_hessian) and 162-167 (Remark sld_vs_bkm formulas)",
          "d/dlam S(rho0+lam X||rho0)=0, d^2/dlam^2 = g^BKM(X,X) = int_0^inf Tr(X(s+rho)^-1 X (s+rho)^-1) ds = sum (log p_i - log p_j)/(p_i-p_j)|X_ij|^2; g^SLD = sum 2|X_ij|^2/(p_i+p_j) = Tr(L X) with rho L + L rho = 2X (qutrit)",
          abs(d1v) < 1e-6 and abs(d2v - bkm) / bkm < 1e-5 and abs(integ - bkm) / bkm < 1e-8 and abs(sld - sld2) / sld < 1e-10,
          "finite differences (Richardson) of the relative entropy: first derivative %s, second %s vs BKM eigenbasis %s vs resolvent integral %s; SLD eigenbasis %s vs Sylvester solution %s"
          % (up(abs(d1v), 2), up(d2v, 8), up(bkm, 8), up(integ, 8), up(sld, 8), up(sld2, 8)),
          "the SLD value must not equal the Hessian (non-commuting perturbation)",
          abs(d2v - sld) / bkm > 1e-3 and bkm >= sld, "SLD %s vs Hessian %s ; BKM >= SLD holds" % (up(sld, 6), up(d2v, 6)))

    # commuting perturbation: equality and Tr(rho^-1 X^2)
    p = np.array([0.5, 0.3, 0.2]); rho_d = np.diag(p).astype(complex)
    Xd = np.diag([0.1, -0.04, -0.06]).astype(complex)
    eq_ok = abs(g_bkm_eig(rho_d, Xd) - g_sld_eig(rho_d, Xd)) < 1e-14 and abs(g_bkm_eig(rho_d, Xd) - np.sum(np.diag(Xd).real ** 2 / p)) < 1e-14
    # unbounded ratio
    ratios = []
    ratio_scalar = lambda pi_, pj_: ((pi_ + pj_) / 2) / ((pj_ - pi_) / (np.log(pj_) - np.log(pi_)))      # arithmetic / logarithmic mean
    for eps in (1e-1, 1e-3, 1e-6):
        pp = np.array([0.5, 0.5 - eps, eps]); r_ = np.diag(pp).astype(complex)
        Xo = np.zeros((3, 3), dtype=complex); Xo[0, 2] = Xo[2, 0] = 0.01
        ratios.append(g_bkm_eig(r_, Xo) / g_sld_eig(r_, Xo))
    # statistics for Hilbert-Schmidt qutrits and traceless GUE perturbations
    gg = np.random.default_rng(2026)
    M = 200000
    rs = np.empty(M)
    for i in range(M):
        r_ = rand_state(3, gg); X_ = rand_traceless(3, gg)
        rs[i] = g_bkm_eig(r_, X_) / g_sld_eig(r_, X_)
    med = np.median(rs); p95 = np.quantile(rs, 0.95)
    frac_below = float(np.mean(rs <= 1.61)); frac_below_12 = float(np.mean(rs <= 1.2))
    # bootstrap standard errors
    bs = np.random.default_rng(1)
    meds = [np.median(bs.choice(rs, size=20000)) for _ in range(50)]
    p95s = [np.quantile(bs.choice(rs, size=20000), 0.95) for _ in range(50)]
    claim("C11.2", "chap11.tex:162-167 (Remark sld_vs_bkm)",
          "g^BKM >= g^SLD with equality iff [rho_0, X] = 0 (then both equal Tr(rho^-1 X^2)); the ratio is unbounded; for qutrits drawn from the Hilbert-Schmidt measure with random traceless Hermitian X the median ratio is about 1.16 and 95% of the samples lie below 1.61",
          eq_ok and ratios[0] > 1 and ratios[0] < ratios[1] < ratios[2] and abs(ratios[2] - ratio_scalar(1e-6, 0.5)) < 1e-9 and ratio_scalar(1e-300, 0.5) > 100 and rs.min() >= 1 - 1e-12 and abs(med - 1.16) < 0.01 and frac_below >= 0.95,
          "commuting example: equality to 1e-14; ratios for p_3 = 1e-1,1e-3,1e-6: %s (= arithmetic/logarithmic mean; it grows like (1/2) ln(1/p_3): at p_3=1e-300 it is %s, so unbounded but only logarithmically); 2e5 samples (Ginibre GG^dagger/tr for rho, GUE traceless for X): min ratio %s, median %s (bootstrap s.d. %s); the text's statement is ONE-SIDED, 'the fraction of samples below 1.61 is >= 95%%': observed fraction below 1.61 = %s (95th percentile %s < 1.61, bootstrap s.d. %s)"
          % ([up(r_, 4) for r_ in ratios], up(ratio_scalar(1e-300, 0.5), 4), dn(rs.min(), 8), up(med, 5), up(np.std(meds), 2), dn(frac_below, 5), up(p95, 5), up(np.std(p95s), 2)),
          "claiming a median of 1.5, or that 95 percent of the samples lie below 1.2, must fail",
          abs(med - 1.5) > 0.2 and frac_below_12 < 0.95, "observed median %s; fraction below 1.2 = %s < 0.95" % (up(med, 4), up(frac_below_12, 4)))

    # first law
    sig = rand_state(4); dr = rand_traceless(4) * 0.2
    S = lambda lam: vn(sig + lam * dr)
    dS = (S(1e-5) - S(-1e-5)) / 2e-5
    H = -logm_h(sig)
    first = np.trace(dr @ H).real
    claim("C11.3", "chap11.tex:179-186 (Prop first_law_entanglement)",
          "delta S = Tr(delta rho H_sigma) with H_sigma = -log sigma (full-rank finite-dimensional states)",
          abs(dS - first) < 1e-8, "central difference of the von Neumann entropy (ququart): %s vs Tr(drho H) = %s" % (up(dS, 10), up(first, 10)),
          "the sign-flipped Tr(drho log sigma) must disagree", abs(dS + first) > 1e-3, "mutated value %s" % up(-first, 8))


def section_geometry():
    # RT counterexample to 'every extremal cut flows to the minimiser'
    mp.mp.dps = 30
    def geod_len(a, b, eps):
        rho = (b - a) / 2
        phi_e = mp.asin(eps / rho)
        return mp.quad(lambda phi: 1 / mp.sin(phi), [phi_e, mp.pi / 2, mp.pi - phi_e])
    eps = mp.mpf("1e-8")
    def diff(delta):
        delta = mp.mpf(delta)
        l1 = geod_len(0, 1, eps) + geod_len(1 + delta, 2 + delta, eps)
        l2 = geod_len(0, 2 + delta, eps) + geod_len(1, 1 + delta, eps)
        return l2 - l1
    root = mp.findroot(lambda d: diff(d), 0.4)
    reg1 = 4 * mp.log(1 / eps)
    l1 = geod_len(0, 1, eps) + geod_len(1.3, 2.3, eps)
    l2 = geod_len(0, 2.3, eps) + geod_len(1, 1.3, eps)
    claim("C11.4", "chap11.tex:263-266 (Remark on continuum RT: two admissible extremal cuts in H^2)",
          "regularised lengths 4 log(1/eps) and 2 log((2+delta)/eps) + 2 log(delta/eps); the second is smaller iff delta(2+delta) < 1 i.e. delta < sqrt2 - 1",
          abs(root - (mp.sqrt(2) - 1)) < 1e-9 and abs(l1 - reg1) < 1e-6 and abs(l2 - (2 * mp.log(2.3 / eps) + 2 * mp.log(0.3 / eps))) < 1e-6,
          "exact semicircle lengths (cutoff z>=1e-8, mpmath quad): root of l2 - l1 = %s vs sqrt2 - 1 = %s; at delta=0.3: l1 - 4 log(1/eps) = %s, l2 - [...] = %s"
          % (mp.nstr(root, 12), mp.nstr(mp.sqrt(2) - 1, 12), mp.nstr(l1 - reg1, 3), mp.nstr(l2 - (2 * mp.log(2.3 / eps) + 2 * mp.log(0.3 / eps)), 3)),
          "the threshold delta<1 (from dropping the factor (2+delta)) must fail: at delta=0.6 the second pair is longer",
          diff(0.6) > 0, "l2 - l1 at delta = 0.6 is %s > 0" % mp.nstr(diff(0.6), 6))

    # scalar curvature of the cMERA metric
    rows = []
    ok = True
    u, c1, c2 = sp.symbols("u c1 c2", positive=True)
    for d in (2, 3, 4):
        xs = sp.symbols("x1:%d" % d)
        coords = [u] + list(xs)
        g = sp.diag(c1, *[c2 * sp.exp(2 * u)] * (d - 1))
        gi = g.inv()
        n = d
        Gam = [[[sum(gi[i, l] * (sp.diff(g[l, k], coords[j]) + sp.diff(g[l, j], coords[k]) - sp.diff(g[j, k], coords[l])) for l in range(n)) / 2
                 for k in range(n)] for j in range(n)] for i in range(n)]
        def Ric(j, k):
            s_ = 0
            for i in range(n):
                s_ += sp.diff(Gam[i][j][k], coords[i]) - sp.diff(Gam[i][i][k], coords[j])
                for m in range(n):
                    s_ += Gam[i][i][m] * Gam[m][j][k] - Gam[i][j][m] * Gam[m][i][k]
            return s_
        Rs = sp.simplify(sum(gi[j, j] * Ric(j, j) for j in range(n)))
        ok &= sp.simplify(Rs + d * (d - 1) / c1) == 0
        rows.append("d=%d: R = %s" % (d, Rs))
    # (R2) metric mutant, same Ricci code: g = c1 du^2 + c2 e^{u} dx^2 (d = 3)
    xs_m = sp.symbols("y1:3")
    coords_m = [u] + list(xs_m)
    g_m = sp.diag(c1, *[c2 * sp.exp(u)] * 2)
    gi_m = g_m.inv()
    n_m = 3
    Gam_m = [[[sum(gi_m[i, l] * (sp.diff(g_m[l, k], coords_m[j]) + sp.diff(g_m[l, j], coords_m[k]) - sp.diff(g_m[j, k], coords_m[l])) for l in range(n_m)) / 2
               for k in range(n_m)] for j in range(n_m)] for i in range(n_m)]

    def Ric_m(j, k):
        s_ = 0
        for i in range(n_m):
            s_ += sp.diff(Gam_m[i][j][k], coords_m[i]) - sp.diff(Gam_m[i][i][k], coords_m[j])
            for m in range(n_m):
                s_ += Gam_m[i][i][m] * Gam_m[m][j][k] - Gam_m[i][j][m] * Gam_m[m][i][k]
        return s_
    mut_R = sp.simplify(sum(gi_m[j, j] * Ric_m(j, j) for j in range(n_m)))
    mut_R_differs = sp.simplify(mut_R + 6 / c1) != 0
    claim("C11.5", "chap11.tex:228-236 (Conjecture hyperbolic metric / Remark Status)",
          "ds^2 = c1 du^2 + c2 e^{2u} sum dx^2 has scalar curvature -d(d-1)/c1 for every c2>0 (so c2 is not invariant content)",
          ok, "sympy Ricci scalar: " + "; ".join(rows),
          "the mutated METRIC c2 e^{u} dx^2 (instead of c2 e^{2u}) must NOT have R = -d(d-1)/c1",
          mut_R_differs, "d=3 mutated metric: R = %s, which differs from -6/c1" % mut_R)

    # area monotonicity under mean curvature flow (closed planar curve)
    a_, b_ = 2.0, 1.0
    n = 4000
    th = (np.arange(n) + 0.5) * 2 * np.pi / n
    x = np.stack([a_ * np.cos(th), b_ * np.sin(th)], axis=1)
    dx = np.stack([-a_ * np.sin(th), b_ * np.cos(th)], axis=1)
    ddx = np.stack([-a_ * np.cos(th), -b_ * np.sin(th)], axis=1)
    sp_ = np.linalg.norm(dx, axis=1)
    kap = (dx[:, 0] * ddx[:, 1] - dx[:, 1] * ddx[:, 0]) / sp_ ** 3
    Nrm = np.stack([-dx[:, 1], dx[:, 0]], axis=1) / sp_[:, None]           # left normal
    Hvec = kap[:, None] * Nrm * 1.0                                          # curvature vector (points inward for CCW)
    Lf = lambda P: np.sum(np.linalg.norm(np.roll(P, -1, axis=0) - P, axis=1))
    h = 1e-5
    fd = (Lf(x + h * Hvec) - Lf(x - h * Hvec)) / (2 * h)
    ds = sp_ * (2 * np.pi / n)
    formula = -np.sum(kap ** 2 * ds)
    claim("C11.6", "chap11.tex:251-256 (Prop mcf_area; closed-curve case)",
          "d/dt Area(gamma(t)) = -int |H|^2 dArea along d_t gamma = H (curve shortening for the length of an ellipse)",
          abs(fd - formula) / abs(formula) < 1e-4,
          "ellipse (2,1), 4000-vertex polygon, central difference of the length under the displacement eps*H: %s vs -int kappa^2 ds = %s" % (up(fd, 8), up(formula, 8)),
          "a missing factor (-1/2 int H^2) must disagree", abs(fd - 0.5 * formula) / abs(formula) > 0.3, "mutated value %s" % up(0.5 * formula, 6))
    unchecked("C11.5b", "chap11.tex:251-256", "the boundary-fixed hypersurface statement is the first variation of area (classical); only the closed-curve instance is checked")


def su2_gen(j):
    d = int(round(2 * j + 1))
    m = np.array([j - k for k in range(d)])
    Jz = np.diag(m).astype(complex)
    Jp = np.zeros((d, d), dtype=complex)
    for k in range(1, d):
        Jp[k - 1, k] = np.sqrt(j * (j + 1) - m[k] * (m[k] + 1))
    Jm = Jp.conj().T
    return (Jp + Jm) / 2, (Jp - Jm) / (2j), Jz


def Dmat(j, axis, ang):
    Jx, Jy, Jz = su2_gen(j)
    Jn = axis[0] * Jx + axis[1] * Jy + axis[2] * Jz
    return sla.expm(-1j * ang * Jn)


def section_lqg():
    # holonomy discretisation: midpoint rule has error O(k^-2); left-point rule O(k^-1); reversed order does not converge
    sig = [np.array([[0, 1], [1, 0]], dtype=complex), np.array([[0, -1j], [1j, 0]]), np.array([[1, 0], [0, -1]], dtype=complex)]
    Aomega = lambda s: -0.5j * (1.3 * np.cos(2 * np.pi * s) * sig[0] + 0.9 * np.sin(2 * np.pi * s) * sig[1] + (0.7 + np.sin(4 * np.pi * s)) * sig[2]) * 2.0
    sol = solve_ivp(lambda s, y: (Aomega(s) @ y.reshape(2, 2)).ravel(), [0, 1], np.eye(2, dtype=complex).ravel(), method="DOP853", rtol=1e-13, atol=1e-14)
    Uex = sol.y[:, -1].reshape(2, 2)
    ks = [10, 20, 40, 80, 160, 320, 640]
    err_mid, err_left, err_rev = [], [], []
    err_eul = []
    for k in ks:
        Pm = np.eye(2, dtype=complex); Pl = np.eye(2, dtype=complex); Pr = np.eye(2, dtype=complex); Pe = np.eye(2, dtype=complex)
        for e in range(k):
            sm = (e + 0.5) / k; sl = e / k
            hm = sla.expm(Aomega(sm) / k); hl = sla.expm(Aomega(sl) / k)
            Pm = hm @ Pm; Pl = hl @ Pl; Pr = Pr @ hm; Pe = (np.eye(2) + Aomega(sm) / k) @ Pe
        err_mid.append(abs(np.trace(Pm) - np.trace(Uex))); err_left.append(abs(np.trace(Pl) - np.trace(Uex))); err_rev.append(abs(np.trace(Pr) - np.trace(Uex))); err_eul.append(abs(np.trace(Pe) - np.trace(Uex)))
    sl_mid = np.polyfit(np.log(ks), np.log(err_mid), 1)[0]
    sl_left = np.polyfit(np.log(ks), np.log(err_left), 1)[0]
    sl_eul = np.polyfit(np.log(ks), np.log(err_eul), 1)[0]
    claim("C11.7", "chap11.tex:302-318 (Prop ashtekar_limit (1))",
          "with midpoint exp(A(gamma(s_e))gamma'(s_e)/k) and the same ordering convention as Pexp, Tr prod h_e -> Tr Pexp with error O(k^-2); observed order 2",
          abs(sl_mid + 2) < 0.1 and err_rev[-1] > 1e-3,
          "SU(2) test connection, exact holonomy DOP853 (rtol 1e-13), k=10..640: log-log slope of the midpoint error = %s; the reversed ordering stays at error %s (does not converge)" % (up(sl_mid, 4), dn(err_rev[-1], 3)),
          "a first-order factor (I + A(s_e)/k) instead of exp(A(s_e)/k) must show order 1, not 2",
          abs(sl_eul + 1) < 0.1, "Euler-factor slope = %s ; (the left-point rule, being a trapezoid rule on a periodic loop, also gives slope %s: the left-point product equals the MIDPOINT product for the shifted connection A(s - 1/2k); on a periodic loop this only moves the base point, the holonomy is conjugated and the trace is unchanged, hence O(k^-2) is not specific to the midpoint)" % (up(sl_eul, 4), up(sl_left, 4)))

    # Casimir / area spectrum building block
    ok = True
    for j in (0.5, 1, 1.5, 2, 3.5):
        Jx, Jy, Jz = su2_gen(j)
        C = Jx @ Jx + Jy @ Jy + Jz @ Jz
        ok &= np.allclose(C, j * (j + 1) * np.eye(C.shape[0]), atol=1e-12)
        comm = Jx @ Jy - Jy @ Jx - 1j * Jz
        ok &= np.abs(comm).max() < 1e-12
    claim("C11.8", "chap11.tex:302-318 (Prop ashtekar_limit (2): sqrt(J^2) = sqrt(j(j+1)) on each crossing edge)",
          "the Casimir of the spin-j representation is j(j+1) (so the regularised area operator contributes 8 pi gamma l_P^2 sqrt(j(j+1)) per crossing edge)",
          ok, "ladder-operator matrices for j=1/2,1,3/2,2,7/2: J_x^2+J_y^2+J_z^2 = j(j+1) I and [J_x,J_y]=iJ_z to 1e-12",
          "the mutated value j^2 (instead of j(j+1)) must disagree", not np.allclose(su2_gen(1)[0] @ su2_gen(1)[0] + su2_gen(1)[1] @ su2_gen(1)[1] + su2_gen(1)[2] @ su2_gen(1)[2], 1.0 * np.eye(3)),
          "DECLARED: trivial control (a constant comparison): for j=1 the Casimir is 2 I, not 1 I")

    # spin-network theta graph: gauge invariance
    from sympy.physics.wigner import wigner_3j
    js = (sp.Rational(1, 2), sp.Integer(1), sp.Rational(3, 2))
    dims = [int(2 * j + 1) for j in js]
    iota = np.zeros(dims)
    for a in range(dims[0]):
        for b in range(dims[1]):
            for c in range(dims[2]):
                m1, m2, m3 = js[0] - a, js[1] - b, js[2] - c
                iota[a, b, c] = float(wigner_3j(js[0], js[1], js[2], m1, m2, m3))
    jf = [float(j) for j in js]
    def Dg(j, g):
        # g = (axis, angle)
        return Dmat(j, g[0], g[1])
    def rand_g():
        ax = rng.standard_normal(3); ax /= np.linalg.norm(ax)
        return ax, rng.uniform(0, 4 * np.pi)
    def Psi(hs, iu, iv):
        D = [Dg(jf[e], hs[e]) for e in range(3)]
        return np.einsum("abc,xyz,ax,by,cz->", iu, iv, D[0], D[1], D[2])
    # invariance of the 3j tensor under D x D x D
    gtest = rand_g()
    Dt = [Dg(jf[e], gtest) for e in range(3)]
    inv_err = np.abs(np.einsum("abc,ax,by,cz->xyz", iota, Dt[0], Dt[1], Dt[2]) - iota).max()
    # compose group elements by matrix multiplication in the spin-1/2 rep, then rebuild higher spins from axis-angle
    def su2(g):
        return Dmat(0.5, g[0], g[1])
    def axis_angle(U):
        # U in SU(2) -> (axis, angle) with U = exp(-i angle n.sigma/2)
        w = np.real(np.trace(U)) / 2
        ang = 2 * np.arccos(np.clip(w, -1, 1))
        if abs(np.sin(ang / 2)) < 1e-12:
            return np.array([0, 0, 1.0]), ang
        sx = np.array([[0, 1], [1, 0]], dtype=complex); sy = np.array([[0, -1j], [1j, 0]]); sz = np.array([[1, 0], [0, -1]], dtype=complex)
        comp = np.array([np.imag(np.trace(U @ s_)) for s_ in (sx, sy, sz)]) / 2     # = -sin(ang/2) n  (since U = cos - i sin n.sigma)
        nvec = -comp / np.sin(ang / 2)
        return nvec / np.linalg.norm(nvec), ang
    hs = [rand_g() for _ in range(3)]
    gu, gv = rand_g(), rand_g()
    base = Psi(hs, iota, iota)
    new_hs = []
    for hg in hs:
        U = su2(gu) @ su2(hg) @ np.linalg.inv(su2(gv))
        new_hs.append(axis_angle(U))
    transformed = Psi(new_hs, iota, iota)
    # control 1: transform only one edge
    one_hs = [axis_angle(su2(gu) @ su2(hs[0]) @ np.linalg.inv(su2(gv)))] + hs[1:]
    wrong_one = Psi(one_hs, iota, iota)
    # control 2: non-invariant random vertex tensor
    rnd = rng.standard_normal(iota.shape)
    b2 = Psi(hs, rnd, iota); t2 = Psi(new_hs, rnd, iota)
    claim("C11.9", "chap11.tex:274-292 (Prop spin_net_tensor_equiv)",
          "the spin-network function of the theta graph with spins (1/2,1,3/2) and 3j intertwiners is gauge invariant: h_e -> g(s(e)) h_e g(t(e))^-1 leaves it unchanged",
          inv_err < 1e-12 and abs(base - transformed) < 1e-10 and abs(base) > 1e-3,
          "Wigner 3j tensor invariant under D^1/2 x D^1 x D^3/2 to %s; |Psi(h)| = %s, |Psi(g h g'^-1)| = %s (difference %s)"
          % (up(inv_err, 2), up(abs(base), 6), up(abs(transformed), 6), up(abs(base - transformed), 2)),
          "transforming only one edge, or replacing the intertwiners by a random tensor, must change Psi",
          abs(base - wrong_one) > 1e-3 and abs(b2 - t2) > 1e-3, "one-edge transform changes Psi by %s; random tensor changes it by %s" % (dn(abs(base - wrong_one), 3), dn(abs(b2 - t2), 3)))


def section_graph_curvature():
    import networkx as nx
    import ot
    def ollivier(Gr, x, y):
        Nx = list(Gr[x]); Ny = list(Gr[y])
        D = np.array([[nx.shortest_path_length(Gr, u, v) for v in Ny] for u in Nx], dtype=float)
        return 1 - ot.emd2(np.full(len(Nx), 1.0 / len(Nx)), np.full(len(Ny), 1.0 / len(Ny)), D)
    # trees: exact formula kappa = -2 (1 - 1/dx - 1/dy)_+
    maxerr = 0.0
    kmin = 1e9
    for seed in range(12):
        T = (nx.random_labeled_tree(40, seed=seed) if hasattr(nx, 'random_labeled_tree') else nx.random_tree(40, seed=seed))
        for (x, y) in T.edges():
            dx, dy = T.degree(x), T.degree(y)
            pred = -2 * max(0.0, 1 - 1 / dx - 1 / dy)
            val = ollivier(T, x, y)
            maxerr = max(maxerr, abs(val - pred)); kmin = min(kmin, val)
    # double star with large degrees: approaches -2
    rows = []
    for d in (3, 6, 12, 50):
        Gs = nx.Graph()
        Gs.add_edge(0, 1)
        for i in range(d - 1):
            Gs.add_edge(0, 2 + i); Gs.add_edge(1, 100 + i)
        rows.append((d, ollivier(Gs, 0, 1), -2 * (1 - 2 / d)))
    # random graphs: bound >= -2
    kg = 1e9
    for seed in range(8):
        Gr = nx.gnp_random_graph(30, 0.2, seed=seed)
        Gr = Gr.subgraph(max(nx.connected_components(Gr), key=len)).copy()
        for (x, y) in Gr.edges():
            kg = min(kg, ollivier(Gr, x, y))
    claim("C11.10", "chap11.tex:336 (Remark: Ollivier curvature of the graph distance satisfies kappa >= -2)",
          "for the simple random walk and graph distance kappa >= -2, with kappa = -2(1-1/d_x-1/d_y)_+ on tree edges (so -2 is approached but not attained)",
          maxerr < 1e-12 and kmin >= -2 and kg >= -2 and all(abs(v - p) < 1e-12 for _, v, p in rows),
          "12 random trees (40 vertices), every edge: |kappa_LP - formula| <= %s, minimum %s; double stars with degrees 3,6,12,50: %s; 8 random graphs G(30,0.2): minimum %s >= -2"
          % (up(maxerr, 2), dn(kmin, 4), [(d, up(v, 5)) for d, v, _ in rows], dn(kg, 4)),
          "the mutated bound kappa >= -1 must be violated by a tree edge",
          kmin < -1, "minimum over tree edges = %s < -1" % dn(kmin, 4))

    # L2 concentration (Levy) : f(x)=x_1 on S^{N-1}; exact tail via the regularised incomplete beta function
    best_c = 1e9
    for Nn in (10, 50, 200, 1000):
        for eps in (0.05, 0.1, 0.2, 0.4, 0.6):
            tail = betainc((Nn - 1) / 2.0, 0.5, 1 - eps ** 2)       # P(|x_1| > eps)
            if tail <= 0:
                continue
            c_here = -np.log(tail / 2) / (Nn * eps ** 2)
            best_c = min(best_c, c_here)
    # (R2) 'there exists a universal c' is existential: on a finite grid some c > 0 is always admissible, so this is an ILLUSTRATION of the cited
    # Levy concentration result (uniformity of c over N <= 1000 and the listed eps), not a verdict on the claim.
    explore("C11.11", "chap11.tex:354-360 (Prop horizon_complexity (2): Levy concentration)",
            "ILLUSTRATION of a cited result (Levy), not a PASS: f = x_1 on S^{N-1}, exact tail from the incomplete beta function for N in {10,50,200,1000}, eps in {0.05,...,0.6}: the smallest admissible constant in P(|f - E f| > eps) <= 2 exp(-c N eps^2) is c = %s (so c = 0.3 works uniformly on this grid; the grid cannot decide the existence of a universal c)" % dn(best_c, 4))

    # k = 2 landscape: critical points on the sphere are the 2N eigenvectors
    from scipy.optimize import root
    N = 6
    Jm = rng.standard_normal((N, N)); Jm = (Jm + Jm.T) / 2
    found = []
    fun = lambda x: np.concatenate([Jm @ x - (x @ Jm @ x) * x, [x @ x - 1.0]])
    for _ in range(3000):
        x = rng.standard_normal(N); x /= np.linalg.norm(x)
        res = root(fun, x, method="lm", options=dict(xtol=1e-14, ftol=1e-14, maxiter=2000))
        xx = res.x
        if np.linalg.norm(fun(xx)) < 1e-9:
            xx = xx / np.linalg.norm(xx)
            if not any(np.linalg.norm(xx - y_) < 1e-6 for y_ in found):
                found.append(xx)
    Qm, _ = np.linalg.qr(rng.standard_normal((N, N)))
    J_deg = Qm @ np.diag([2.0, 2.0, 1.0, 0.0, -1.0, -2.0]) @ Qm.T
    fun_d = lambda x: np.concatenate([J_deg @ x - (x @ J_deg @ x) * x, [x @ x - 1.0]])
    found_deg = []
    for _ in range(300):
        x = rng.standard_normal(N); x /= np.linalg.norm(x)
        res = root(fun_d, x, method="lm", options=dict(xtol=1e-14, ftol=1e-14, maxiter=2000))
        xx = res.x
        if np.linalg.norm(fun_d(xx)) < 1e-9:
            xx = xx / np.linalg.norm(xx)
            if not any(np.linalg.norm(xx - y_) < 1e-6 for y_ in found_deg):
                found_deg.append(xx)
    claim("C11.12", "chap11.tex:352-354 (Prop horizon_complexity (1), k=2)",
          "for k=2 the critical points of the quadratic form on S^{N-1} are the 2N unit eigenvectors +-v_i (generic coupling matrix)",
          len(found) == 2 * N,
          "N=6: 3000 randomised Newton solves of the stationarity system find %d distinct critical points (2N = %d)" % (len(found), 2 * N),
          "hypothesis dropped: a coupling matrix with a REPEATED eigenvalue has a circle of critical points, so the same procedure must give more than 2N distinct points and the count '2N' must fail",
          len(found_deg) > 2 * N and len(found_deg) != 2 * N, "J with eigenvalues (2,2,1,0,-1,-2): %d distinct critical points found by the same procedure (> 2N = %d)" % (len(found_deg), 2 * N))
    unchecked("C11.U1", "chap11.tex:352 (Prop horizon_complexity (1), k>=3)", "the limit (1/N) log E[Crit] = (1/2) log(k-1) is the Auffinger-Ben Arous-Cerny theorem (an asymptotic statement from Kac-Rice plus GOE large deviations); finite-N simulation cannot distinguish it from corrections of order (log N)/N")


def section_unchecked():
    unchecked("C11.U2", "chap11.tex:192-215 (Thm einstein_emergence, Remark beyond first order)", "holographic derivation (Iyer-Wald form, RT formula assumed); cited results of FGHMV, Lashkari-Van Raamsdonk, Faulkner et al., Dong-Lewkowycz; no numerical content")
    unchecked("C11.U3", "chap11.tex:111-131 (Introduction: Goroff-Sagnotti two-loop divergence, MSS bound)", "cited facts from the literature")
    unchecked("C11.U4", "chap11.tex:138-148 (Bisognano-Wichmann, local form of the ball modular Hamiltonian)", "cited theorem; the formula involves the type III algebra and has no finite-dimensional numerical counterpart")
    unchecked("C11.U5", "chap11.tex:341-348 (Remark: Ollivier expansion kappa = r^2 Ric/(2(N+2)); Hamilton's theorem)", "Ollivier's expansion would need Wasserstein distances between uniform measures on small geodesic balls to 1e-5 relative accuracy; cited result, not checked here")
    unchecked("C11.U6", "chap11.tex:241-250 (Prop mincut)", "S_A <= |C| log chi follows from the Schmidt rank argument given in the proof; no numerical content beyond the standard bound S <= log(rank)")


if __name__ == "__main__":
    section_information()
    section_geometry()
    section_lqg()
    section_graph_curvature()
    section_unchecked()
    finish("11")
