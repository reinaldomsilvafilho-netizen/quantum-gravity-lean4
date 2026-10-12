"""Independent checks for F-55 (ch. 2, graphon Ollivier-Ricci remarks).

C1  discrete-metric graphon curvature 1-TV on G(n,1/2) step graphons -> 1/2,
    while the cut-norm limit W=1/2 has 1-TV = 1; spectral norm of (A-J/2)/n -> 0
    (upper bound for the cut norm). Graph Ollivier kappa_0 on edges -> 1/2
    (oracle: exact W1 by LP), and codegree ratio -> 1/2.
C2  normalised flow dW = 2(kappa_box - kbar) W, kbar = int kappa W / int W:
    generic step-graphon integrator (8x8 grid, kappa_box by matrix products)
    vs reduced 2-block ODE; limit (1+eps) on blocks, rate 2(1+eps).
    Negative control: limit equal to the indicator (value 1) must fail.
C3  winner-take-all: asymmetric diagonal blocks, q=0; growth rate S.
    Negative control: rate S/2 must fail.
C4  barbell K6-K6, lazy walk alpha=1/2, phi=1, length flow dl = -kappa d:
    bridge curvature at t=0 equals -2/3 (hand computation; oracle LP vs POT),
    negative control -4/3 (alpha=0 value) must fail; bridge curvature sign
    along the flow (numerical observation).
Seed fixed. Exit code = number of failures.
"""
import sys
import time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse.csgraph import shortest_path
from scipy.integrate import solve_ivp
import ot

rng = np.random.default_rng(20261006)
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


def w1_lp(mu, nu, D):
    """Exact W1 by linear programming (oracle independent of POT)."""
    m, k = len(mu), len(nu)
    c = D.reshape(-1)
    Aeq = []
    beq = []
    for i in range(m):
        row = np.zeros(m * k); row[i * k:(i + 1) * k] = 1; Aeq.append(row); beq.append(mu[i])
    for j in range(k):
        row = np.zeros(m * k); row[j::k] = 1; Aeq.append(row); beq.append(nu[j])
    res = linprog(c, A_eq=np.array(Aeq), b_eq=np.array(beq), bounds=(0, None), method="highs")
    return res.fun


# ---------------- C1 ----------------
log("C1: G(n,1/2)")
for n in (100, 400, 1600):
    A = (rng.random((n, n)) < 0.5).astype(float)
    A = np.triu(A, 1); A = A + A.T
    deg = A.sum(1)
    P = A / deg[:, None]
    idx = rng.choice(n, size=(200, 2))
    idx = idx[idx[:, 0] != idx[:, 1]]
    tv = 0.5 * np.abs(P[idx[:, 0]] - P[idx[:, 1]]).sum(1)
    ktv = 1 - tv
    cod = (A[idx[:, 0]] * A[idx[:, 1]]).sum(1) / np.maximum(deg[idx[:, 0]], deg[idx[:, 1]])
    spec = np.linalg.norm((A - 0.5 * (np.ones((n, n)) - np.eye(n))) / n, 2)
    log(f"  n={n}: mean 1-TV = {ktv.mean():.4f}, mean codegree ratio = {cod.mean():.4f}, ||A-J/2||/n = {spec:.4f}")
    if n == 1600:
        check("1-TV on G(n,1/2) near 1/2 (n=1600)", abs(ktv.mean() - 0.5) < 0.02)
        check("NEG: 1-TV on G(n,1/2) near the limit value 1 must fail", not (abs(ktv.mean() - 1.0) < 0.1))
        check("spectral (>= cut) norm of W_n - 1/2 small", spec < 0.05)
    if n == 100:
        # graph Ollivier kappa_0 on edges, exact LP oracle and POT
        Dg = shortest_path(A, unweighted=True)
        E = np.argwhere(np.triu(A, 1) > 0)
        sel = E[rng.choice(len(E), 20, replace=False)]
        k_lp, k_pot = [], []
        for x, y in sel:
            Nx = np.flatnonzero(A[x]); Ny = np.flatnonzero(A[y])
            mu = np.full(len(Nx), 1 / len(Nx)); nu = np.full(len(Ny), 1 / len(Ny))
            D = Dg[np.ix_(Nx, Ny)]
            k_lp.append(1 - w1_lp(mu, nu, D)); k_pot.append(1 - ot.emd2(mu, nu, D))
        k_lp = np.array(k_lp); k_pot = np.array(k_pot)
        log(f"  n=100 graph kappa_0 on 20 edges: mean {k_lp.mean():.4f}; LP vs POT max diff {np.abs(k_lp-k_pot).max():.1e}")
        check("graph Ollivier kappa_0 on G(100,1/2) near 1/2", abs(k_lp.mean() - 0.5) < 0.06)
        check("LP oracle agrees with POT", np.abs(k_lp - k_pot).max() < 1e-8)


# ---------------- C2/C3: generic step graphon integrator ----------------
def kbox(Wm):
    """kappa_box for a step graphon on an N-cell uniform partition."""
    N = Wm.shape[0]
    d = Wm.mean(1)
    T = Wm @ Wm / N
    return T / np.maximum(d[:, None], d[None, :])


def rhs_norm(t, w, N):
    Wm = w.reshape(N, N)
    K = kbox(Wm)
    kbar = (K * Wm).sum() / Wm.sum()
    return (2 * (K - kbar) * Wm).reshape(-1)


N = 8
h = N // 2
eps = 0.1
log("C2: normalised flow, symmetric blocks, eps=0.1")
W0 = np.full((N, N), eps); W0[:h, :h] = 1; W0[h:, h:] = 1
sol = solve_ivp(rhs_norm, (0, 12), W0.reshape(-1), args=(N,), rtol=1e-11, atol=1e-14, dense_output=True)
WT = sol.y[:, -1].reshape(N, N)
# symmetric part: round-off asymmetry between the two blocks grows at rate S
# (winner-take-all, C3), so compare the block average with 1+eps
pT, qT = 0.5 * (WT[0, 0] + WT[-1, -1]), WT[0, -1]
log(f"  t=12: block average {pT:.10f}, bridge value {qT:.3e}, "
    f"round-off block asymmetry {WT[0,0]-WT[-1,-1]:.2e} (grows at rate S, see C3)")
check("block value -> 1+eps", abs(pT - (1 + eps)) < 1e-8)
check("NEG: block value -> 1 (indicator) must fail", not (abs(pT - 1) < 1e-3))
ts = np.array([6.0, 10.0])
qs = np.array([sol.sol(t).reshape(N, N)[0, -1] for t in ts])
rate = -np.log(qs[1] / qs[0]) / (ts[1] - ts[0])
log(f"  bridge decay rate {rate:.5f} (theory 2(1+eps) = {2*(1+eps):.5f})")
check("bridge rate 2(1+eps)", abs(rate - 2 * (1 + eps)) < 1e-3)


# reduced ODE oracle
def red(t, y):
    p, q = y; s = p + q
    dq = -2 * (p - q) ** 2 * p * q / s ** 2
    return [-dq, dq]


r = solve_ivp(red, (0, 3), [1, eps], rtol=1e-12, atol=1e-14)
g = solve_ivp(rhs_norm, (0, 3), W0.reshape(-1), args=(N,), rtol=1e-12, atol=1e-14)
diff = abs(r.y[1, -1] - g.y[:, -1].reshape(N, N)[0, -1])
log(f"  reduced vs generic at t=3: {diff:.1e}")
check("reduced 2-block ODE matches generic integrator", diff < 1e-8)

log("C3: winner-take-all, q=0, p1=p2=1.1 with relative asymmetry 1e-9")
W0 = np.zeros((N, N)); W0[:h, :h] = 1.1 * (1 + 1e-9); W0[h:, h:] = 1.1 * (1 - 1e-9)
S = 2.2
sol = solve_ivp(rhs_norm, (0, 40), W0.reshape(-1), args=(N,), rtol=1e-12, atol=1e-30, dense_output=True)
u = lambda t: (lambda M: (M[0, 0] - M[-1, -1]) / S)(sol.sol(t).reshape(N, N))
rate = np.log(u(4.0) / u(1.0)) / 3.0
WT = sol.y[:, -1].reshape(N, N)
log(f"  fitted asymmetry growth rate {rate:.4f} (theory S={S}); t=40: p1={WT[0,0]:.6f}, p2={WT[-1,-1]:.2e}")
check("asymmetry grows at rate S", abs(rate - S) < 1e-3)
check("NEG: rate S/2 must fail", not (abs(rate - S / 2) < 1e-2))
check("one block absorbs the mass: p1 -> S", abs(WT[0, 0] - S) < 1e-6)


# ---------------- C4: barbell ----------------
log("C4: barbell K6-K6, alpha=1/2, phi=1")
nV = 12
edges = [(i, j) for i in range(6) for j in range(i + 1, 6)] + \
        [(6 + i, 6 + j) for i in range(6) for j in range(i + 1, 6)] + [(0, 6)]
bridge = len(edges) - 1
nbr = [[] for _ in range(nV)]
for e, (x, y) in enumerate(edges):
    nbr[x].append(y); nbr[y].append(x)
alpha = 0.5


def curv(ell, solver):
    G = np.zeros((nV, nV))
    for e, (x, y) in enumerate(edges):
        G[x, y] = G[y, x] = ell[e]
    Dm = shortest_path(G, directed=False)
    K = np.empty(len(edges)); dd = np.empty(len(edges))
    for e, (x, y) in enumerate(edges):
        sx = [x] + nbr[x]; sy = [y] + nbr[y]
        mx = np.array([alpha] + [(1 - alpha) / len(nbr[x])] * len(nbr[x]))
        my = np.array([alpha] + [(1 - alpha) / len(nbr[y])] * len(nbr[y]))
        D = Dm[np.ix_(sx, sy)]
        w1 = solver(mx, my, D)
        dd[e] = Dm[x, y]
        K[e] = 1 - w1 / dd[e]
    return K, dd


ell0 = np.ones(len(edges))
k_lp, _ = curv(ell0, w1_lp)
k_pot, _ = curv(ell0, lambda a, b, D: ot.emd2(a, b, D))
log(f"  t=0 bridge curvature: LP {k_lp[bridge]:.12f}, POT {k_pot[bridge]:.12f}")
check("bridge kappa_{1/2}(0) = -2/3", abs(k_lp[bridge] + 2 / 3) < 1e-9 and abs(k_pot[bridge] + 2 / 3) < 1e-9)
check("NEG: bridge kappa_{1/2}(0) = -4/3 must fail", not abs(k_lp[bridge] + 4 / 3) < 1e-3)

pot = lambda a, b, D: ot.emd2(a, b, D)


def F(ell):
    K, dd = curv(ell, pot)
    return -K * dd, K


hstep = 0.02
ell = ell0.copy()
t0 = time.time()
first_pos = None
lmax_bridge = 0.0
rec = {}
for kstep in range(int(round(10 / hstep)) + 1):
    t = kstep * hstep
    f1, K = F(ell)
    lmax_bridge = max(lmax_bridge, ell[bridge])
    if first_pos is None and K[bridge] > 0:
        first_pos = t
    for tt in (0, 2.5, 5, 7.5, 10):
        if abs(t - tt) < 1e-9:
            rec[tt] = (K[bridge], ell[bridge], ell.min())
    if kstep == int(round(10 / hstep)):
        break
    f2, _ = F(ell + 0.5 * hstep * f1)
    f3, _ = F(ell + 0.5 * hstep * f2)
    f4, _ = F(ell + hstep * f3)
    ell = ell + hstep / 6 * (f1 + 2 * f2 + 2 * f3 + f4)
for tt, (kb, lb, lm) in rec.items():
    log(f"  t={tt:5.2f}: bridge kappa {kb:+.4f}, bridge length {lb:.4f}, min length {lm:.2e}")
log(f"  first t with bridge kappa > 0: {first_pos}; max bridge length on [0,10]: {lmax_bridge:.4f}; "
    f"RK4 time {time.time()-t0:.1f}s")
check("bridge curvature becomes positive along the flow (persistence of kappa<=-c fails)",
      first_pos is not None)

log(f"FAILURES: {fails}")
with open(__file__.replace(".py", ".out.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
sys.exit(fails)
