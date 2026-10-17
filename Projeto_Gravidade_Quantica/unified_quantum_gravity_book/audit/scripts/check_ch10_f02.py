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
# Chapter 10 body.  Source: chap10_information_geometry_minimax_deep_learning.tex (3.0.0)
# ======================================================================
import numpy as np
import mpmath as mp
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

rng = np.random.default_rng(20261016)


# ---------------- A. Remark length_bound: annulus, circles, shooting ----------------
def psi_grad(x):
    s = np.sum(x ** 2, axis=-1)
    inside = s <= 1.0
    g = -60.0 * (1 - s)[..., None] ** 2 * x
    return np.where(inside[..., None], g, 0.0)


def psi_hess(x):
    s = np.sum(x ** 2, axis=-1)
    inside = (s <= 1.0)[..., None, None]
    I = np.eye(2)
    H = -60.0 * ((1 - s) ** 2)[..., None, None] * I + 240.0 * (1 - s)[..., None, None] * x[..., :, None] * x[..., None, :]
    return np.where(inside, H, 0.0)


def metric(x, lam0=0.1):
    gp = psi_grad(x)
    return (1 + lam0) * np.eye(2) + gp[..., :, None] * gp[..., None, :]


def section_length_bound():
    lam0, Lmax = 0.1, 1.5
    # annulus radii: |grad psi|^2 = (1+lam0)(Lmax-1)  with |grad psi| = 60 r (1-r^2)^2
    target = np.sqrt((1 + lam0) * (Lmax - 1))
    r_sym = sp.symbols("r")
    polys = sp.Poly(sp.expand((60 * r_sym * (1 - r_sym ** 2) ** 2) ** 2 - sp.nsimplify((1 + lam0) * (Lmax - 1), rational=True)), r_sym)
    roots = [complex(x) for x in sp.Poly(polys, r_sym).nroots(n=30)]
    real_pos = sorted(x.real for x in roots if abs(x.imag) < 1e-12 and x.real > 0 and x.real < 1)
    # numerical cond-based root finding with actual matrices
    cond = lambda r: np.linalg.cond(metric(np.array([r, 0.0]), lam0))
    r_lo = brentq(lambda r: cond(r) - Lmax, 1e-4, 0.3, xtol=1e-14)
    r_hi = brentq(lambda r: cond(r) - Lmax, 0.5, 0.999, xtol=1e-14)
    sample = np.array([cond(r) for r in np.linspace(0, 1.2, 2401)])
    inside_set = np.linspace(0, 1.2, 2401)[sample > Lmax]
    claim("C10.1", "chap10.tex:97 (Remark length_bound): annulus 0.012 <= |theta-c| <= 0.941",
          "with lambda_0=0.1 and Lambda_max=1.5, O_sing = {cond(g~) > 1.5} is the annulus 0.012 <~ |theta-c| <~ 0.941 (g~ = (1+lambda_0)I + grad psi grad psi^T, psi = 10(1-|x|^2)^3)",
          abs(real_pos[0] - r_lo) < 1e-9 and abs(real_pos[-1] - r_hi) < 1e-9 and round(r_lo, 3) == 0.012 and round(r_hi, 3) == 0.941
          and abs(inside_set.min() - r_lo) < 1e-3 and abs(inside_set.max() - r_hi) < 1e-3,
          "polynomial roots of (60 r (1-r^2)^2)^2 = (1+lambda_0)(Lambda-1): r_1=%s, r_2=%s; Brent on numpy.linalg.cond of the actual 2x2 metric: %s and %s; scan of cond on a 2401-point grid: O_sing = [%s, %s]"
          % (up(real_pos[0], 8), up(real_pos[-1], 8), up(r_lo, 8), up(r_hi, 8), dn(inside_set.min(), 4), up(inside_set.max(), 4)),
          "the mutated threshold Lambda_max=2.5 must give a different annulus (outer radius not 0.941)",
          abs(brentq(lambda r: cond(r) - 2.5, 0.5, 0.999, xtol=1e-12) - 0.941) > 0.005,
          "outer radius for Lambda_max=2.5 is %s" % up(brentq(lambda r: cond(r) - 2.5, 0.5, 0.999, xtol=1e-12), 5))

    # circles through theta_0 and (4,0), centres (2,h): major arcs stay at distance >= 2 from c, acceleration 1/(sqrt(1+lam0) R_h)
    rows = []
    ok = True
    mind = []
    mut_acc_gap = []
    for h in (0.5, 3.0, 40.0, 1000.0):
        R = np.sqrt(4 + h ** 2)
        phi0 = np.arctan2(0 - h, 0 - 2)            # (0,0) seen from the centre (2,h)
        phi1 = np.arctan2(0 - h, 4 - 2)            # (4,0)
        ang = np.linspace(phi0, phi1 - 2 * np.pi, 20001)      # clockwise through the top: the major arc
        pts = np.stack([2 + R * np.cos(ang), h + R * np.sin(ang)], axis=1)
        dist = np.hypot(pts[:, 0] - 2, pts[:, 1])
        mind.append(dist.min())
        # covariant acceleration in the constant metric (1+lam0) I: finite differences of a g-unit-speed parametrisation
        s = np.linspace(0, 1, 5)
        a_ = 1 + lam0
        sp_e = 1 / np.sqrt(a_)                      # Euclidean speed for g-unit speed
        t0 = 0.37
        gam = lambda t: np.array([2 + R * np.cos(ang[0] + t * sp_e / R), h + R * np.sin(ang[0] + t * sp_e / R)])
        hh = 1e-2 * R
        acc_e = (gam(t0 + hh) - 2 * gam(t0) + gam(t0 - hh)) / hh ** 2
        acc_norm = np.sqrt(a_) * np.linalg.norm(acc_e)
        pred = 1 / (np.sqrt(a_) * R)
        mut_acc_gap.append(abs(acc_norm - 1 / R) / (1 / R))
        ok &= dist.min() >= 2 - 1e-7 and abs(acc_norm - pred) / pred < 1e-3 and abs(pts[0, 0]) < 1e-9 and abs(pts[-1, 0] - 4) < 1e-9
        rows.append("h=%g: min distance to c = %s, acceleration %s vs 1/(sqrt(1+lambda_0) R_h) = %s, length of the major arc ~ %s" % (h, dn(dist.min(), 6), up(acc_norm, 6), up(pred, 6), up(R * abs(ang[-1] - ang[0]), 5)))
    claim("C10.2", "chap10.tex:97 (Remark length_bound): major arcs of circles through theta_0 and (4,0) with centres (2,h)",
          "the major arcs stay at distance >= 2 from c = (2,0) (outside the unit disk) and have covariant acceleration 1/(sqrt(1+lambda_0) R_h), R_h = sqrt(4+h^2) -> 0 as h -> infinity with lengths -> infinity",
          ok, "; ".join(rows),
          "the mutant acceleration 1/R_h (WITHOUT the factor 1/sqrt(1+lambda_0)) must disagree with the finite-difference acceleration, and a distance bound >= 2.5 must fail",
          max(mind) < 2.5 and max(mut_acc_gap) > 0.02,
          "largest minimal distance over the four circles = %s < 2.5; relative gap of the mutant acceleration 1/R_h from the computed one: %s" % (up(max(mind), 8), dn(max(mut_acc_gap), 3)))

    # shooting of geodesics from theta_0 (EXPLORE): minimal distance to the ball B((4,0),0.1) among rays that avoid O_sing
    Nr = 4001
    phis = np.linspace(-np.pi / 2, np.pi / 2, Nr)
    c0 = np.array([2.0, 0.0])
    x = np.zeros((Nr, 2)) + 0.0
    v = np.stack([np.cos(phis), np.sin(phis)], axis=1) / np.sqrt(1 + lam0)

    def acc(x, v):
        xx = x - c0
        g = metric(xx, lam0)
        gi = np.linalg.inv(g)
        gp = psi_grad(xx)
        H = psi_hess(xx)
        # dg_ij/dx_k = H_ik gp_j + gp_i H_jk  (dgk[n,i,j,k])
        dgk = np.einsum("nik,nj->nijk", H, gp) + np.einsum("ni,njk->nijk", gp, H)
        # direct assembly (clear but slower): loop over indices
        G = np.zeros((x.shape[0], 2, 2, 2))
        for l in range(2):
            for i in range(2):
                for j in range(2):
                    s_ = 0
                    for m in range(2):
                        s_ = s_ + gi[:, l, m] * (dgk[:, m, j, i] + dgk[:, m, i, j] - dgk[:, i, j, m])
                    G[:, l, i, j] = 0.5 * s_
        return -np.einsum("nlij,ni,nj->nl", G, v, v)

    ds = 0.005
    best = np.full(Nr, 1e9)
    entered = np.zeros(Nr, dtype=bool)
    mind_free = np.full(Nr, 1e9)
    steps = int(14 / ds)
    for _ in range(steps):
        def f(x_, v_):
            return v_, acc(x_, v_)
        k1x, k1v = f(x, v)
        k2x, k2v = f(x + ds / 2 * k1x, v + ds / 2 * k1v)
        k3x, k3v = f(x + ds / 2 * k2x, v + ds / 2 * k2v)
        k4x, k4v = f(x + ds * k3x, v + ds * k3v)
        x = x + ds / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        v = v + ds / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        cnd = np.linalg.cond(metric(x - c0, lam0))
        entered |= cnd > Lmax
        d = np.linalg.norm(x - np.array([4.0, 0.0]), axis=1)
        mind_free = np.where(~entered, np.minimum(mind_free, d), mind_free)
    speed_drift = np.max(np.abs(np.einsum("ni,nij,nj->n", v, metric(x - c0, lam0), v) - 1.0))
    n_enter = int(entered.sum())
    ok_shoot = mind_free.min() > 0.1
    claim("C10.3", "chap10.tex:97 (Remark length_bound): 'numerical shooting of geodesics finds none that reaches Sigma* outside O_sing'",
          "no geodesic from theta_0=0 reaches B((4,0),0.1) without meeting O_sing",
          ok_shoot and speed_drift < 5e-3,
          "4001 geodesics (initial angles in [-pi/2,pi/2], RK4 ds=0.005, g-length 14): %d meet O_sing; among the others the closest approach to (4,0) is %s (> 0.1 = radius of Sigma*); max drift of the g-speed %s"
          % (n_enter, dn(mind_free.min(), 4), up(speed_drift, 2)),
          "the straight segment from 0 to (4,0) (angle 0) must be among the rays that DO meet O_sing",
          bool(entered[Nr // 2]), "ray with phi=%s meets O_sing: %s" % (up(abs(phis[Nr // 2]), 3), bool(entered[Nr // 2])))
    explore("C10.3b", "chap10.tex:97", "shooting is numerical evidence only: rays that avoid the annulus are straight lines outside the disc (the metric is constant there), and any ray entering the disc of radius 0.941 must cross O_sing")


# ---------------- B. counterexample proposition ----------------
def section_counter():
    # gap for Gaussian inputs: Monte Carlo on fresh test points vs quadrature over f ~ N(0, |theta*|^2)
    N_, D_ = 50, 200
    reps = 300
    gaps_mc = []
    gaps_q = []
    s2 = []
    for r in range(reps):
        X = rng.standard_normal((N_, D_))
        y = rng.choice([-1.0, 1.0], size=N_)
        th = np.linalg.lstsq(X, y, rcond=None)[0]          # min-norm interpolant (D > N)
        assert np.linalg.norm(X @ th - y) < 1e-8
        s2.append(th @ th)
        # fresh test inputs
        Xt = rng.standard_normal((4000, D_))
        yt = rng.choice([-1.0, 1.0], size=4000)
        gaps_mc.append(np.mean(np.minimum((yt - Xt @ th) ** 2, 1.0)))
        sig = np.sqrt(th @ th)
        gaps_q.append(quad(lambda t: np.exp(-t * t / (2 * sig ** 2)) / (sig * np.sqrt(2 * np.pi)) * 0.5 * (min((1 - t) ** 2, 1) + min((1 + t) ** 2, 1)), -8 * sig, 8 * sig, points=[-2, -1, 0, 1, 2], limit=200)[0])
    gm, gq = np.mean(gaps_mc), np.mean(gaps_q)
    se = np.std(gaps_mc) / np.sqrt(reps)
    pred_s2 = N_ / (D_ - N_ - 1)
    f_grid = np.linspace(-6, 6, 400001)
    pair = np.minimum((1 - f_grid) ** 2, 1) + np.minimum((1 + f_grid) ** 2, 1)
    thr = np.sqrt(np.log(40) / (2 * 50))
    Nmin = int(np.floor(2 * np.log(40))) + 1
    ok_N = all(np.sqrt(np.log(40) / (2 * n)) < 0.5 for n in range(Nmin, 400)) and not any(np.sqrt(np.log(40) / (2 * n)) < 0.5 for n in range(1, Nmin))
    claim("C10.4", "chap10.tex:117-135 (Prop counterexample (2)): gap >= 1/2; about 0.70 for Gaussian inputs N=50, D=200; 0.19 for the PAC-Bayes-type bound; below 1/2 for all N >= 8",
          "for random +-1 labels the clipped-square-loss gap of the min-norm interpolant is >= 1/2 (about 0.70 at N=50, D=200 with Gaussian inputs); sqrt(ln(2/delta)/(2N)) = 0.19 at N=50, delta=0.05 and < 1/2 iff N >= 8",
          pair.min() >= 1 - 1e-12 and abs(gm - gq) < 5 * se + 2e-3 and 0.69 < gm < 0.72 and abs(np.mean(s2) - pred_s2) < 0.01 and abs(thr - 0.19) < 0.005 and Nmin == 8 and ok_N,
          "300 replicates: Monte Carlo test gap %s +- %s (s.e.) vs quadrature over f~N(0,|theta*|^2) %s; E|theta*|^2 = %s vs N/(D-N-1) = %s; min over a 4e5-point grid of min((1-f)^2,1)+min((1+f)^2,1) = %s (>= 1, equality at |f|=1); sqrt(ln40/100) = %s ; smallest N with bound < 1/2: %d"
          % (up(gm, 4), up(se, 2), up(gq, 4), up(np.mean(s2), 4), up(pred_s2, 4), dn(pair.min(), 8), up(thr, 5), Nmin),
          "a claimed gap of 0.19 (the PAC-Bayes value) or of 0.5 for the Gaussian example must be rejected",
          abs(gm - 0.19) > 0.3 and abs(gm - 0.5) > 0.1, "observed gap %s differs from 0.19 and from 0.5" % up(gm, 4))
    # Weyl remark: lambda_min(g + lambda_0 I) >= lambda_0
    ok = True
    for _ in range(2000):
        A_ = rng.standard_normal((6, 6)); g = A_ @ A_.T
        ok &= np.linalg.eigvalsh(g + 0.1 * np.eye(6)).min() >= 0.1 - 1e-12
    claim("C10.5", "chap10.tex:139-141 (Remark on the formulation: Weyl)",
          "lambda_min(g + lambda_0 I) >= lambda_0 for PSD g", ok, "2000 random 6x6 PSD matrices: bound never violated",
          "the strict bound lambda_min > 2 lambda_0 must fail", not all(np.linalg.eigvalsh(np.zeros((3, 3)) + 0.1 * np.eye(3)).min() > 0.2 for _ in range(1)),
          "DECLARED: constant control (Weyl is a theorem): g = 0 gives lambda_min = 0.1 = lambda_0, not above 0.2")


# ---------------- C. Stiefel remarks (d = l = 2) ----------------
def rot(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s], [s, c]])


def section_stiefel():
    # 5d - 4 tr Q >= d on O(d)
    ok = True
    for d in (2, 3, 5):
        for _ in range(500):
            Q, _ = np.linalg.qr(rng.standard_normal((d, d)))
            ok &= np.linalg.norm(2 * np.eye(d) - Q) ** 2 >= d - 1e-12 and abs(np.linalg.norm(2 * np.eye(d) - Q) ** 2 - (5 * d - 4 * np.trace(Q))) < 1e-10
    # ------------------------------------------------------------------------------------------------------------
    # (R2) The claims are tested AS STATED.  The data the book used are recorded in audit/verify/scripts/L2res_ch10_conj.py (seeds 1000..1005,
    # teacher W1 = reflection 0.7, W2 = I, 40 inputs N(0,2.25 I_2), loss = mean over samples of the squared error summed over the 2 outputs) and in
    # audit/verify/scripts/L2res2_ch10_conj.py (seed 7, teacher R(0.7), R(-0.3), eta = 0.05, tol 1e-3).  Own implementation: ANALYTIC gradient
    # (rotation derivative R'(t) = R(t + pi/2)), cross-checked against central differences.
    def refl(t):
        c, s_ = np.cos(t), np.sin(t)
        return np.array([[c, s_], [s_, -c]])
    MK = {1: rot, -1: refl}

    def lossab(W1, W2, X, Y, norm=1.0):
        return norm * np.mean(np.sum((np.tanh(X @ W1.T) @ W2.T - Y) ** 2, axis=1))

    def comp_min(s1, s2, X, Y, n=121):
        ts = np.linspace(0, 2 * np.pi, n, endpoint=False)
        best = (np.inf, None)
        for a in ts:
            H = np.tanh(X @ MK[s1](a).T)
            for b in ts:
                v = np.mean(np.sum((H @ MK[s2](b).T - Y) ** 2, axis=1))
                if v < best[0]:
                    best = (v, (a, b))
        from scipy.optimize import minimize as mnz
        r_ = mnz(lambda p_: lossab(MK[s1](p_[0]), MK[s2](p_[1]), X, Y), best[1], method="Nelder-Mead", options=dict(xatol=1e-10, fatol=1e-14, maxiter=4000))
        return r_.fun

    mins_pp, sym_ok, zero_ok = [], True, True
    for seed in range(6):
        g_ = np.random.default_rng(1000 + seed)
        X = g_.normal(0, 1.5, size=(40, 2))
        Yt = np.tanh(X @ refl(0.7).T) @ np.eye(2).T
        m_pp = comp_min(1, 1, X, Yt); m_mm = comp_min(-1, -1, X, Yt)
        zero_ok &= comp_min(-1, 1, X, Yt) < 1e-8 and comp_min(1, -1, X, Yt) < 1e-8
        sym_ok &= abs(m_pp - m_mm) < 1e-6
        mins_pp.append(m_pp)
    mins_pp = np.array(mins_pp)
    in_interval = bool(((mins_pp >= 1.57) & (mins_pp <= 1.75)).all())
    mutA = bool(((mins_pp >= 1.58) & (mins_pp <= 1.75)).all())   # critique r5 mutant 1.58-1.75: seed 1004 must fall outside
    mutB = bool(((mins_pp >= 1.57) & (mins_pp <= 1.74)).all())   # mutant 1.57-1.74: seed 1005 must fall outside
    # mutants: (i) loss summed over samples instead of averaged (x40) ; (ii) the seed set 300..311 of the earlier screen (printed as EXPLORE below)
    mut_scaled = mins_pp * 40
    stats300 = []
    for seed in range(12):
        g_ = np.random.default_rng(300 + seed)
        X = 1.5 * g_.standard_normal((40, 2))
        Yt = np.tanh(X @ np.diag([1.0, -1.0]).T)
        stats300.append(comp_min(1, 1, X, Yt, n=91))
    claim("C10.6", "chap10.tex:141-143 (Remark on the formulation, d=l=2 example)",
          "||2I - Q||_F^2 = 5d - 4 tr Q >= d on O(d); for d=l=2, teacher W1 = reflection, W2 = I, 40 inputs N(0,2.25 I_2): zero loss on O(2)^2 (teacher component), the minimum over SO(2)^2 equals the minimum over the component det W1 = det W2 = -1, and it lies between 1.57 and 1.75 in the six samples (seeds 1000..1005)",
          ok and sym_ok and zero_ok and in_interval,
          "500 random orthogonal matrices for d=2,3,5: identity and bound hold; RECORDED samples (seeds 1000..1005 of L2res_ch10_conj.py, mean over samples of the squared error summed over outputs): "
          "teacher components reach 0 (<1e-8): %s; min over SO(2)^2 equals min over (-,-) to 1e-6: %s; minima over SO(2)^2 = %s, all in [1.57, 1.75]: %s"
          % (zero_ok, sym_ok, [up(m_, 4) for m_ in mins_pp], in_interval),
          "mutants must not reproduce the interval: the loss summed over samples (x40) instead of averaged; and 'SO(2)^2 reaches zero loss' must fail; interval mutants 1.58-1.75 and 1.57-1.74 must fail",
          not bool(((mut_scaled >= 1.57) & (mut_scaled <= 1.75)).any()) and mins_pp.min() > 1e-3 and (not mutA) and (not mutB),
          "x40 loss: minima %s all outside [1.57, 1.75]; smallest minimum over SO(2)^2 = %s > 0; mutant 1.58-1.75 fails (excludes seed 1004 = %s): %s; mutant 1.57-1.74 fails (excludes seed 1005 = %s): %s" % ([dn(v, 3) for v in mut_scaled], dn(mins_pp.min(), 3), up(mins_pp[4], 4), not mutA, up(mins_pp[5], 4), not mutB))
    explore("C10.6b", "chap10.tex:141-143", "OTHER seeds (300..311, not the ones used by the book): minima over SO(2)^2 = %s; they are NOT all in [1.57, 1.75] (min %s), so the interval is sample-dependent, as the text says ('in the samples we drew')" % ([up(m_, 3) for m_ in stats300], dn(min(stats300), 3)))

    # ---- C10.7 on the recorded sample (seed 7): loss maximum 4.18, strict local maximum, escape counts 48, 72, 96
    def make7(seed, t1, t2, n=40, norm=1.0):
        g_ = np.random.default_rng(seed)
        X = g_.normal(0.0, 1.5, size=(n, 2))
        Y = np.tanh(X @ rot(t1).T) @ rot(t2).T
        return X, Y, norm

    def L7(ab, X, Y, norm=1.0):
        return norm * np.mean(np.sum((np.tanh(X @ rot(ab[0]).T) @ rot(ab[1]).T - Y) ** 2, axis=1))

    def G7(ab, X, Y, norm=1.0):          # analytic gradient with R'(t) = R(t + pi/2)
        H = np.tanh(X @ rot(ab[0]).T)
        E = H @ rot(ab[1]).T - Y
        da = np.mean(np.sum(2 * E * (((1 - H ** 2) * (X @ rot(ab[0] + np.pi / 2).T)) @ rot(ab[1]).T), axis=1))
        db = np.mean(np.sum(2 * E * (H @ rot(ab[1] + np.pi / 2).T), axis=1))
        return norm * np.array([da, db])

    def steps7(start, X, Y, eta=0.05, norm=1.0, tol=1e-3, nmax=3000):
        th = np.array(start, float)
        for k in range(nmax):
            if L7(th, X, Y, norm) < tol:
                return k
            th = th - eta * G7(th, X, Y, norm)
        return None

    def max_and_steps(seed, norm=1.0, eta=0.05, ndir=180):
        X, Y, _ = make7(seed, 0.7, -0.3)
        grid_ = np.linspace(-np.pi, np.pi, 241)
        vals = np.array([[L7(np.array([a_, b_]), X, Y, norm) for b_ in grid_] for a_ in grid_])
        i_, j_ = np.unravel_index(np.argmax(vals), vals.shape)
        from scipy.optimize import minimize as mnz
        tm_ = mnz(lambda z: -L7(z, X, Y, norm), [grid_[i_], grid_[j_]], method="Nelder-Mead", options=dict(xatol=1e-12, fatol=1e-15, maxiter=5000)).x
        e_ = 1e-4
        Hs = np.zeros((2, 2))
        for p_ in range(2):
            for q_ in range(2):
                ep, eq = e_ * np.eye(2)[p_], e_ * np.eye(2)[q_]
                Hs[p_, q_] = (L7(tm_ + ep + eq, X, Y, norm) - L7(tm_ + ep - eq, X, Y, norm) - L7(tm_ - ep + eq, X, Y, norm) + L7(tm_ - ep - eq, X, Y, norm)) / (4 * e_ * e_)
        mins_dir = []
        for r_ in (1e-2, 1e-4, 1e-6):
            cs = [steps7(tm_ + r_ * np.array([np.cos(t_), np.sin(t_)]), X, Y, eta, norm) for t_ in np.linspace(0, 2 * np.pi, ndir, endpoint=False)]
            mins_dir.append(min(cs))
        disp = [steps7(tm_ + r_ * np.array([1.0, 0.3]), X, Y, eta, norm) for r_ in (1e-2, 1e-4, 1e-6)]
        return X, Y, tm_, L7(tm_, X, Y, norm), np.linalg.eigvalsh(Hs), mins_dir, disp

    X7, Y7, tm7, Lmax7, ev7, mind7, disp7 = max_and_steps(7)
    gfd = np.array([(L7(tm7 + 1e-6 * np.eye(2)[i], X7, Y7) - L7(tm7 - 1e-6 * np.eye(2)[i], X7, Y7)) / 2e-6 for i in range(2)])
    p_test = np.array([0.3, -1.1])
    gfd2 = np.array([(L7(p_test + 1e-6 * np.eye(2)[i], X7, Y7) - L7(p_test - 1e-6 * np.eye(2)[i], X7, Y7)) / 2e-6 for i in range(2)])
    grad_ok = np.abs(G7(p_test, X7, Y7) - gfd2).max() < 1e-6
    ok_max = abs(Lmax7 - 4.18) < 0.005 and np.linalg.norm(G7(tm7, X7, Y7)) < 1e-6 and ev7.max() < 0 and L7(np.array([0.7, -0.3]), X7, Y7) < 1e-24
    ok_cnt = all(abs(a_ - b_) <= 1 for a_, b_ in zip(mind7, [48, 72, 96])) and disp7 == [48, 72, 96]
    # mutants: eta = 0.1; loss averaged over the 2 outputs as well (x1/2, so max 2.09 != 4.18); another seed
    _, _, _, Lmax_h, _, mind_eta, disp_eta = max_and_steps(7, eta=0.1, ndir=24)
    _, _, _, Lmax_half, _, _, _ = max_and_steps(7, norm=0.5, ndir=4)
    _, _, _, Lmax_s8, _, mind_s8, disp_s8 = max_and_steps(8, ndir=24)
    mut_fail = (disp_eta != [48, 72, 96]) and abs(Lmax_half - 4.18) > 0.5 and (abs(Lmax_s8 - 4.18) > 0.005 or disp_s8 != [48, 72, 96])
    # 1/r law mutant: steps(r) proportional to 1/r would predict, from the observed 48 steps at r=1e-2, the increments x100 each time
    pred_inv = [48 * 100, 48 * 10000]
    claim("C10.7", "chap10.tex:147 (Why the initialization is random): maximum about 4.18; steps about 48, 72, 96",
          "teacher in SO(2)^2 (R(0.7), R(-0.3)), 40 inputs N(0,2.25 I_2), mean squared loss (summed over the 2 outputs): the loss vanishes at the teacher, its maximum over SO(2)^2 is about 4.18 at a strict local maximum; with step 0.05, starts at distance 1e-2, 1e-4, 1e-6 need at least about 48, 72, 96 steps to reach loss < 1e-3 (minima over the direction of the start)",
          ok_max and ok_cnt and grad_ok,
          "RECORDED sample (seed 7 of L2res2_ch10_conj.py), own implementation with analytic gradient (agrees with central differences to <1e-6: %s): loss at teacher %s; max over SO(2)^2 = %s at (%s) with |grad| = %s and Hessian eigenvalues %s (both negative: strict local max); "
          "steps to reach loss < 1e-3 from distance 1e-2, 1e-4, 1e-6: minimum over 180 unit directions = %s, along the displacement r(1,0.3) = %s (book: about 48, 72, 96; tolerance +-1 on the minima, exact on the displacement)"
          % (grad_ok, up(L7(np.array([0.7, -0.3]), X7, Y7), 2), up(Lmax7, 5), ", ".join(up(v, 5) for v in tm7), up(np.linalg.norm(G7(tm7, X7, Y7)), 2), [up(v, 4) for v in ev7], mind7, disp7),
          "mutants must NOT reproduce: eta = 0.1; loss averaged over the outputs too; another seed (8).  And a 1/r escape time (steps proportional to 1/r) would predict increments of thousands, not 24",
          mut_fail and (pred_inv[0] - 48 > 100) and (disp7[1] - disp7[0] < 40),
          "eta=0.1: counts %s (!= 48,72,96); loss/2: max %s (!= 4.18); seed 8: max %s, counts %s; 1/r law predicts %s vs observed %s" % (disp_eta, up(Lmax_half, 4), up(Lmax_s8, 4), disp_s8, pred_inv, disp7))

    # ---- EXPLORE: the structural log(1/r) law on OTHER samples (not the book's), as in the first round
    rows = []
    incs = []
    for seed in range(6):
        g = np.random.default_rng(500 + seed)
        X = 1.5 * g.standard_normal((40, 2))
        a_t = g.uniform(0, 2 * np.pi, 2)
        Yt = np.tanh(X @ rot(a_t[0]).T) @ rot(a_t[1]).T
        L = lambda t: L7(t, X, Yt)
        grid = np.linspace(0, 2 * np.pi, 181)[:-1]
        Lg = np.array([[L(np.array([a, b])) for b in grid] for a in grid])
        i, j = np.unravel_index(np.argmax(Lg), Lg.shape)
        from scipy.optimize import minimize as mnz
        tm = mnz(lambda t: -L(t), [grid[i], grid[j]], method="Nelder-Mead", options=dict(xatol=1e-12, fatol=1e-14)).x
        e = 1e-4
        Hs = np.zeros((2, 2))
        for p in range(2):
            for q in range(2):
                ep, eq = e * np.eye(2)[p], e * np.eye(2)[q]
                Hs[p, q] = (L(tm + ep + eq) - L(tm + ep - eq) - L(tm - ep + eq) + L(tm - ep - eq)) / (4 * e * e)
        mu = -np.linalg.eigvalsh(Hs).min()
        steps_pred = np.log(100) / np.log(1 + 0.05 * mu)
        res_r = [min(steps7(tm + r * np.array([np.cos(2 * np.pi * k / 36), np.sin(2 * np.pi * k / 36)]), X, Yt) for k in range(36)) for r in (1e-2, 1e-4, 1e-6)]
        incs.append((res_r[1] - res_r[0], res_r[2] - res_r[1], steps_pred))
        rows.append("seed %d: Lmax=%s, mu=%s, steps %s, predicted increment %s" % (500 + seed, up(L(tm), 3), up(mu, 3), res_r, up(steps_pred, 3)))
    lin = all(abs(b_ - p_) <= 1.5 and abs(a_ - p_) <= 8 for a_, b_, p_ in incs)
    explore("C10.7s", "chap10.tex:147", "log(1/r) escape law on OTHER samples (seeds 500..505, not the book's): increment per factor 100 vs ln100/ln(1+0.05 mu) within tolerance for all seeds: %s | %s" % (lin, " | ".join(rows)))


def section_unchecked():
    unchecked("C10.U1", "chap10.tex:84-90 (K-FAC cost statements)", "operation counts O(d_in^3 + d_out^3), O(d_in d_out (d_in+d_out)), O(B(d_in^2+d_out^2)) are complexity statements about an algorithm, not numerical claims")
    unchecked("C10.U2", "chap10.tex:139-141 (Conjecture Stiefel-constrained training)", "open conjecture; its only numerical side remarks are checked in C10.6/C10.7")
    unchecked("C10.U3", "chap10.tex:104-112 (Prop degenerate, Remark on Hessian)", "a geodesic has D gamma'/ds = 0 by definition; no numerical content")
    unchecked("C10.U4", "chap10.tex:90-95 and 175-190 (Frenet schedule and table)", "design heuristic and a qualitative comparison table; no quantitative claim")


if __name__ == "__main__":
    section_length_bound()
    section_counter()
    section_stiefel()
    section_unchecked()
    finish("10")
