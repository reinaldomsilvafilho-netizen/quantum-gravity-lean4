"""Layer-2 re-check of OBL-008 (Thm 4.4): lim_{p->inf} lambda_p(A)^{1/p} = 1/R_Omega
for every weight with 0 < c0 <= Phi <= C0.

Routes (independent of the corrector's radial FE on the disk and the referee's shooting):
 (1) 1D interval (0,1), R = 1/2: closed form lambda_p = (p-1) pi_p^p,
     pi_p = 2 pi / (p sin(pi/p))  (Otani; Lindqvist). Oracle for the FE code.
     NOTE: a first run used a wrong closed form with an extra (p-1)^{1/p} in pi_p;
     the FE code (converging at order 2 and N-independent) exposed it.  That wrong
     form is now the negative control.
 (2) 1D *weighted* FE minimisation of the Rayleigh quotient (L-BFGS, analytic gradient),
     two different weights, p up to 64, mesh refinement.  Must lie in the comparison
     window [(c0/C0) lam_p, (C0/c0) lam_p]^{1/p} and approach 2 = 1/R.
 (3) Unit square, rigorous two-sided bounds without any FE:
        lower: lambda_p(square) >= lambda_p(interval of length 1)   (slice Poincare)
        upper: |Omega|^{1/p} / ||dist(.,bdry)||_p                     (test function)
     both -> 2 = 1/R; weighted versions multiply by (c0/C0)^{1/p}, (C0/c0)^{1/p}.
 Negative controls: Cheeger constant of the square h = 2 + sqrt(pi) (claimed value of v2)
     and the mutated limits 1/(2R), 2/R must be excluded by the rigorous bounds;
     FE code with a wrong closed form (pi_p without (p-1)^{1/p}) must disagree at p=4.
"""
import sys
import numpy as np
from scipy.optimize import minimize
import mpmath as mp

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


def lam_interval(p, L=1.0):
    pip = 2 * np.pi / (p * np.sin(np.pi / p))
    return (p - 1) * (pip / L) ** p


def lam_interval_wrong(p, L=1.0):  # mutated: extra factor (p-1)^{1/p} in pi_p
    pip = 2 * np.pi * (p - 1) ** (1 / p) / (p * np.sin(np.pi / p))
    return (p - 1) * (pip / L) ** p


def fe_lambda_1d(p, N, w):
    """P1 FE on (0,1), Dirichlet; weight w(x). Returns lambda (weighted quotient)."""
    x = np.linspace(0, 1, N + 1)
    h = 1.0 / N
    xm = 0.5 * (x[:-1] + x[1:])
    we = w(xm)                      # element weight (midpoint)
    # mass: p-th power integrated by 3-point Gauss on each element, exact enough
    gp = np.array([-np.sqrt(3 / 5), 0, np.sqrt(3 / 5)])
    gw = np.array([5 / 9, 8 / 9, 5 / 9])
    lam0 = 0.5 * (1 - gp)
    lam1 = 0.5 * (1 + gp)
    wq = w(x[:-1][:, None] + h * lam1[None, :])  # weight at quad points

    def unpack(v):
        u = np.zeros(N + 1)
        u[1:-1] = v
        return u

    def f(v):
        u = unpack(v)
        du = np.diff(u) / h
        a = np.abs(du)
        num = np.sum(we * a ** p) * h
        uq = u[:-1, None] * lam0[None, :] + u[1:, None] * lam1[None, :]
        den = np.sum(wq * np.abs(uq) ** p * gw[None, :]) * h / 2
        # gradients
        gnum_e = we * p * a ** (p - 2) * du  # d num / d du_e * (1/h) * h
        gnum = np.zeros(N + 1)
        gnum[:-1] -= gnum_e
        gnum[1:] += gnum_e
        t = wq * p * np.abs(uq) ** (p - 2) * uq * gw[None, :] * h / 2
        gden = np.zeros(N + 1)
        gden[:-1] += np.sum(t * lam0[None, :], axis=1)
        gden[1:] += np.sum(t * lam1[None, :], axis=1)
        # minimise log R for scale invariance
        val = np.log(num) - np.log(den)
        g = gnum / num - gden / den
        return val, g[1:-1]

    v0 = np.sin(np.pi * x[1:-1]) + 0.05 * x[1:-1] ** 2
    res = minimize(f, v0, jac=True, method="L-BFGS-B",
                   options={"maxiter": 20000, "maxcor": 30, "ftol": 1e-15, "gtol": 1e-11})
    return float(np.exp(res.fun))


w1 = lambda x: 1.0 + 0.0 * x
wA = lambda x: 1.0 + 0.8 * np.sin(5 * x) ** 2          # c0 = 1,   C0 = 1.8
wB = lambda x: np.exp(1.2 * x - 0.6)                    # c0 = e^-.6, C0 = e^.6
bounds = {"wA": (1.0, 1.8), "wB": (np.exp(-0.6), np.exp(0.6))}

log("== (1) FE oracle check: unweighted interval vs closed form ==")
for p in (2, 4, 8):
    exact = lam_interval(p)
    errs = []
    for N in (100, 200, 400):
        lam = fe_lambda_1d(p, N, w1)
        errs.append(abs(lam - exact) / exact)
        log(f"p={p:3d} N={N:4d} FE={lam:.8g} exact={exact:.8g} relerr={errs[-1]:.2e}")
    rate = np.log2(errs[0] / errs[1]), np.log2(errs[1] / errs[2])
    log(f"   observed orders {rate[0]:.2f}, {rate[1]:.2f} (P1 eigenvalue: expect ~2)")
    check(f"FE matches closed form at p={p} (relerr<1e-4 at N=400)", errs[-1] < 1e-4)
    check(f"FE error decreases under refinement at p={p}", errs[2] < errs[1] < errs[0])
lamw = fe_lambda_1d(4, 400, w1)
check("negative control: mutated closed form (extra (p-1)^{1/p}) disagrees with FE at p=4",
      abs(lamw - lam_interval_wrong(4)) / lamw > 1e-2)

log("== (2) weighted 1D: lambda_p(A)^{1/p} in comparison window and -> 1/R = 2 ==")
for name, w in (("wA", wA), ("wB", wB)):
    c0, C0 = bounds[name]
    prev = None
    vals = []
    for p in (2, 4, 8, 16, 32, 64):
        N = 400 if p <= 16 else 800
        lam = fe_lambda_1d(p, N, w)
        lam2 = fe_lambda_1d(p, N // 2, w)
        r = lam ** (1 / p)
        r2 = lam2 ** (1 / p)
        lo = ((c0 / C0) * lam_interval(p)) ** (1 / p)
        hi = ((C0 / c0) * lam_interval(p)) ** (1 / p)
        vals.append(r)
        log(f"{name} p={p:3d} lam^(1/p)={r:.6f} (N/2: {r2:.6f}) window=[{lo:.6f},{hi:.6f}]")
        check(f"{name} p={p} inside comparison window", lo - 1e-6 <= r <= hi + 1e-6)
    check(f"{name}: distance to 2 decreases monotonically in p (2..64)",
          all(abs(vals[i + 1] - 2) < abs(vals[i] - 2) for i in range(len(vals) - 1)))
    check(f"{name}: mutated weight-dependent limit 2*(C0/c0) excluded at p=64",
          abs(vals[-1] - 2 * C0 / c0) > 0.1)

log("== (3) unit square: rigorous bounds, no FE ==")
mp.mp.dps = 30


def delta_norm_p(p):
    # ||delta||_p^p over unit square = 4 * int_0^{1/2} x^p (1-2x) dx
    return 4 * mp.quad(lambda x: x ** p * (1 - 2 * x), [0, 0.5])


h_sq = 2 + np.sqrt(np.pi)  # Cheeger constant of the unit square
R = 0.5
for (c0, C0) in ((1.0, 1.0), (0.5, 2.0)):
    for p in (8, 64, 512, 4096):
        lower = (c0 / C0) ** (1 / p) * float(lam_interval(p)) ** (1 / p) if p < 600 else \
            float((c0 / C0) ** (1 / mp.mpf(p)) * mp.mpf(p - 1) ** (1 / mp.mpf(p))
                  * 2 * mp.pi / (p * mp.sin(mp.pi / p)))
        upper = float((C0 / c0) ** (1 / mp.mpf(p)) / delta_norm_p(p) ** (1 / mp.mpf(p)))
        log(f"weight ratio {C0 / c0:.1f}, p={p:5d}: {lower:.6f} <= lam^(1/p) <= {upper:.6f}")
    check(f"rigorous bounds at p=4096 both within 0.01 of 1/R=2 (ratio {C0 / c0})",
          lower <= upper and abs(lower - 2) < 0.01 and abs(upper - 2) < 0.01)
    check("negative control: Cheeger h=2+sqrt(pi) excluded (above upper bound)", h_sq > upper)
    check("negative control: 1/(2R)=1 excluded (below lower bound)", 1 / (2 * R) < lower)
    check("negative control: 2/R=4 excluded (above upper bound)", 2 / R > upper)

log(f"failures: {fails}")
with open(__file__.replace(".py", ".out.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
sys.exit(fails)
