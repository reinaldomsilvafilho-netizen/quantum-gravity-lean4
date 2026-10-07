"""Layer-2 re-check of Remark 5.4 (OBL-012) and Thm 8.1 (OBL-020), new routes.

OBL-012, dragged trap V_s = kappa (x - s a)^2 / 2, k_B T = D = 1:
  (a) mean dissipated work by solve_ivp of the full (mean, variance) moment system and
      the work integral, vs the closed form a^2 (1 - (1 - e^{-kappa tau})/(kappa tau)) / tau;
  (b) friction metric g = int_0^inf Cov(dV/ds(X_0), dV/ds(X_t)) dt by quadrature of the
      OU autocovariance -> a^2 for every kappa;
  (c) Aurell et al.: the optimal (jump) protocol lambda(t) = a t/tau + a/(kappa tau) on (0,tau),
      reaching mu_B at time tau, has tau <W_diss> = a^2 = W_2^2 for every finite tau, while the
      dragged trap at finite tau has tau Sigma < a^2 but does not reach mu_B;
  (d) dimensions: exponents of [time] for tau Sigma, L^2, W_2^2, kappa W_2^2.
  Negative controls: the v2 bound kappa/4 W_2^2 (kappa = 10) and the v2 factor 1/2 L^2.
OBL-020, Cassini oval |z-1||z+1| = c (peanut, c slightly > 1):
  reach by Federer's formula inf |q-p|^2 / (2 dist(q-p, T_p)) on dense samples (3 refinements),
  eps0, M, d_sep by sampling; check reach >= min(eps0/M, d_sep/2).
  Negative control: the mutated bound reach >= d_sep/2 must fail for at least one oval
  (first run used 2 x bound, which did not discriminate; see note in the code).
"""
import sys
import numpy as np
from scipy.integrate import solve_ivp, quad

fails = 0
out = []


def log(s):
    print(s)
    out.append(s)


def check(name, ok):
    global fails
    log(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        fails += 1


a = 1.3
log("== OBL-012 ==")
for kappa in (1.0, 10.0):
    for tau in (0.5, 5.0, 200.0):
        lam = lambda t: a * t / tau

        def rhs(t, y):
            m, v, w = y
            # dm = -kappa (m - lam) dt ; dv = (-2 kappa v + 2) dt ; dW = dV/dt = -kappa (x - lam) a/tau
            return [-kappa * (m - lam(t)), -2 * kappa * v + 2, -kappa * (m - lam(t)) * a / tau]
        sol = solve_ivp(rhs, (0, tau), [0.0, 1 / kappa, 0.0], rtol=1e-11, atol=1e-13)
        W = sol.y[2, -1]
        closed = a ** 2 * (1 - (1 - np.exp(-kappa * tau)) / (kappa * tau)) / tau
        log(f"kappa={kappa:5.1f} tau={tau:6.1f}: tau<W> ODE={tau * W:.10f} closed={tau * closed:.10f} final mean={sol.y[0, -1]:.5f} (target {a})")
        check(f"closed form, kappa={kappa}, tau={tau}", abs(W - closed) < 1e-8 * max(1, closed))
        if tau < 100:
            check(f"dragged trap at finite tau does not reach mu_B (kappa={kappa}, tau={tau})",
                  abs(sol.y[0, -1] - a) > 1e-6)
            check(f"tau Sigma < W_2^2 at finite tau (consistent with Aurell, which needs mu_B at tau)",
                  tau * W < a ** 2)
    g, _ = quad(lambda t: kappa ** 2 * a ** 2 * (1 / kappa) * np.exp(-kappa * t), 0, np.inf)
    log(f"kappa={kappa}: friction metric g = {g:.12f} (a^2 = {a ** 2})")
    check(f"g_fric = a^2 independent of kappa={kappa}", abs(g - a ** 2) < 1e-10)
    check(f"slow limit tau Sigma -> L^2 = a^2 (tau=200, kappa={kappa})", abs(tau * W - a ** 2) < 0.01 * a ** 2 / kappa + 1e-3)
    check(f"negative control: v2 factor 1/2 L^2 fails (kappa={kappa})", abs(tau * W - 0.5 * g) > 0.3)
    if kappa == 10.0:
        check("negative control: v2 bound tau Sigma >= kappa/4 W_2^2 fails at kappa=10",
              not (tau * W >= kappa / 4 * a ** 2))
    # Aurell optimal protocol: trap centre jumps to a/(kappa tau), moves at speed a/tau, jumps to a
    for tau2 in (0.5, 5.0):
        lam2 = lambda t: a * t / tau2 + a / (kappa * tau2)

        def rhs2(t, y):
            m, w = y
            return [-kappa * (m - lam2(t)), -kappa * (m - lam2(t)) * a / tau2]
        s2 = solve_ivp(rhs2, (0, tau2), [0.0, 0.0], rtol=1e-11, atol=1e-13)
        # jump works: <V_new - V_old> at the current state (variance terms cancel)
        j0 = kappa / 2 * ((0 - lam2(0)) ** 2 - 0.0)
        mT = s2.y[0, -1]
        j1 = kappa / 2 * ((mT - a) ** 2 - (mT - lam2(tau2)) ** 2)
        Wopt = s2.y[1, -1] + j0 + j1
        log(f"   Aurell optimal protocol kappa={kappa} tau={tau2}: final mean={mT:.8f}, tau<W>={tau2 * Wopt:.10f} (W_2^2={a ** 2:.4f})")
        check(f"optimal protocol reaches mu_B and tau W_diss = W_2^2 (kappa={kappa}, tau={tau2})",
              abs(mT - a) < 1e-8 and abs(tau2 * Wopt - a ** 2) < 1e-8)

# dimensions: [x]^2 = [t] (D = 1), energies dimensionless (k_B T = 1)
dims = {"tau*Sigma": 1, "L^2": 1, "W2^2": 1, "kappa": -1}
log(f"time exponents: {dims}; kappa*W2^2 -> {dims['kappa'] + dims['W2^2']}")
check("tau Sigma, L^2, W_2^2 have the same dimension", dims["tau*Sigma"] == dims["L^2"] == dims["W2^2"])
check("negative control: kappa W_2^2 is dimensionally different", dims["kappa"] + dims["W2^2"] != dims["tau*Sigma"])

log("== OBL-020: Cassini ovals |z-1||z+1| = c ==")


def oval(c, N):
    # polar form of the lemniscate family: r^2 = cos 2t + sqrt(c^4 - sin^2 2t)
    t = np.linspace(0, 2 * np.pi, N, endpoint=False)
    r = np.sqrt(np.cos(2 * t) + np.sqrt(c ** 4 - np.sin(2 * t) ** 2))
    P = np.c_[r * np.cos(t), r * np.sin(t)]
    return P


def Phi_grad_hess(P):
    x, y = P[:, 0], P[:, 1]
    # Phi = ((x-1)^2+y^2)((x+1)^2+y^2) = (x^2+y^2)^2 - 2(x^2-y^2) + 1
    s = x ** 2 + y ** 2
    gx = 4 * x * s - 4 * x
    gy = 4 * y * s + 4 * y
    hxx = 4 * s + 8 * x ** 2 - 4
    hyy = 4 * s + 8 * y ** 2 + 4
    hxy = 8 * x * y
    return np.c_[gx, gy], hxx, hyy, hxy


def reach_federer(P, T):
    best = np.inf
    n = len(P)
    for i0 in range(0, n, 500):
        p = P[i0:i0 + 500, None, :]
        tp = T[i0:i0 + 500, None, :]
        d = P[None, :, :] - p
        dd = np.sum(d * d, axis=2)
        tang = np.sum(d * tp, axis=2)
        nrm = np.sqrt(np.maximum(dd - tang ** 2, 0))
        with np.errstate(divide="ignore", invalid="ignore"):
            val = dd / (2 * nrm)
        val[dd < 1e-20] = np.inf
        val[~np.isfinite(val)] = np.inf
        best = min(best, val.min())
    return best


twice_fails = 0
for c in (1.05, 1.2, 1.6):
    res = []
    for N in (1000, 2000, 4000):
        P = oval(c, N)
        G, hxx, hyy, hxy = Phi_grad_hess(P)
        gn = np.linalg.norm(G, axis=1)
        nu = G / gn[:, None]
        T = np.c_[-nu[:, 1], nu[:, 0]]
        eps0 = gn.min()
        M = max(np.max(np.abs(np.linalg.eigvalsh(np.array([[hxx[i], hxy[i]], [hxy[i], hyy[i]]]))))
                for i in range(N))
        # opposite normals: angle of nu; pairs with angle difference pi
        ang = np.arctan2(nu[:, 1], nu[:, 0])
        dsep = np.inf
        for i in range(N):
            diff = np.abs(np.angle(np.exp(1j * (ang - ang[i] - np.pi))))
            mask = diff < 2 * np.pi / N * 3
            if mask.any():
                dsep = min(dsep, np.min(np.linalg.norm(P[mask] - P[i], axis=1)))
        R = reach_federer(P, T)
        bound = min(eps0 / M, dsep / 2)
        res.append((N, R, eps0 / M, dsep / 2, bound))
        log(f"c={c} N={N}: reach={R:.5f} eps0/M={eps0 / M:.5f} dsep/2={dsep / 2:.5f} bound={bound:.5f}")
    R, bound = res[-1][1], res[-1][4]
    check(f"c={c}: reach >= bound (finest grid)", R >= bound - 1e-3)
    check(f"c={c}: reach stable under refinement (<1e-3)", abs(res[-1][1] - res[-2][1]) < 1e-3)
    twice_fails += R < res[-1][3] - 1e-3
# NOTE: the first run used "2 x bound" as control; on these ovals eps0/M is far from sharp,
# so that control did not discriminate (all three passed it).  It is replaced by the
# mutation that drops the curvature term, reach >= d_sep/2, which is not a theorem.
check("negative control: mutated bound reach >= d_sep/2 (curvature term dropped) fails for some oval",
      twice_fails > 0)

log(f"failures: {fails}")
with open(__file__.replace(".py", ".out.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
sys.exit(fails)
