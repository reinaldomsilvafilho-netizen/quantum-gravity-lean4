"""Layer-2 re-check of F-55 (ch. 2, Remark after Prop. thm:ricci_neckpinch).

Written by the layer-2 verifier; does not reuse fixes_F55_checks.py.
(a) G(n,1/2): kappa^TV off-diagonal -> 1/2, cut-norm bound via operator norm,
    Hoeffding arithmetic, graph Ollivier curvature -> p (Bhattacharya-Mukherjee),
    sign/scope of kappa^square (>=0 always, <=1 only if W<=1).
(b) barbell K6-K6, lazy walk alpha=1/2, phi=1, length flow  l' = -kappa d.
(c) normalised flow 2(kappa-kbar)W with kappa=kappa^square: 2-block ODE,
    limit (1+eps) on blocks, winner-take-all instability.
Each check: independent oracle, negative control, refinement.
"""
import sys, time, itertools
import numpy as np
import sympy as sp
from scipy.optimize import linprog
from scipy.sparse.csgraph import shortest_path
from scipy.integrate import solve_ivp

T0 = time.time()
FAIL = 0
rng = np.random.default_rng(20261006)


def check(name, ok, msg=""):
    global FAIL
    print(f"[{name}] {'ok  ' if ok else 'FAIL'} {msg}", flush=True)
    if not ok:
        FAIL += 1


# ---------------------------------------------------------------- W1 oracles
def w1_primal(mu, nu, D):
    n = len(mu)
    c = D.reshape(-1)
    Aeq = np.zeros((2 * n, n * n))
    for i in range(n):
        Aeq[i, i * n:(i + 1) * n] = 1
        Aeq[n + i, i::n] = 1
    b = np.concatenate([mu, nu])
    r = linprog(c, A_eq=Aeq, b_eq=b, bounds=(0, None), method="highs")
    return r.fun


def w1_dual(mu, nu, D):
    """Kantorovich-Rubinstein: max sum f(mu-nu) s.t. f_i - f_j <= D_ij."""
    n = len(mu)
    rows, rhs = [], []
    for i in range(n):
        for j in range(n):
            if i != j:
                a = np.zeros(n); a[i] = 1; a[j] = -1
                rows.append(a); rhs.append(D[i, j])
    r = linprog(-(mu - nu), A_ub=np.array(rows), b_ub=np.array(rhs),
                bounds=[(0, 0)] + [(None, None)] * (n - 1), method="highs")
    return -r.fun


def edge_curv(adj_len, x, y, alpha, phi, w1=w1_primal):
    """Ollivier curvature of edge xy on weighted graph (lengths), lazy walk."""
    D = shortest_path(adj_len, directed=False)
    n = adj_len.shape[0]

    def meas(v):
        m = np.zeros(n)
        nb = np.nonzero(adj_len[v])[0]
        w = np.array([phi(adj_len[v, z]) for z in nb])
        m[nb] = (1 - alpha) * w / w.sum()
        m[v] += alpha
        return m
    mx, my = meas(x), meas(y)
    supp = np.nonzero((mx > 0) | (my > 0))[0]
    W = w1(mx[supp], my[supp], D[np.ix_(supp, supp)])
    return 1 - W / D[x, y], D[x, y]


# =========================================================== (a) G(n,1/2)
print("== (a) G(n,1/2): kappa^TV, cut norm, graph Ollivier curvature")
# Hoeffding arithmetic, symbolic
n_ = sp.symbols("n", positive=True)
expo = sp.simplify(2 * (2 * n_ ** sp.Rational(3, 2)) ** 2 / (2 * n_ ** 2))
check("a-hoeff", sp.simplify(expo - 4 * n_) == 0, f"2t^2/sum c^2 = {expo}")
# sum c^2 <= 2|S||T| brute force; mutation sum c^2 <= |S||T| must fail
viol, viol_mut = 0, 0
for _ in range(300):
    m = int(rng.integers(2, 12))
    S = set(np.nonzero(rng.random(m) < 0.6)[0]); T = set(np.nonzero(rng.random(m) < 0.6)[0])
    c2 = 0
    for i, j in itertools.combinations(range(m), 2):
        c = (i in S and j in T) + (j in S and i in T)
        c2 += c * c
    viol += c2 > 2 * len(S) * len(T)
    viol_mut += c2 > len(S) * len(T)
check("a-c2", viol == 0, f"sum c^2 <= 2|S||T| in 300/300 trials")
check("a-c2-NEG", viol_mut > 0, f"mutated sum c^2 <= |S||T| violated in {viol_mut} trials")

res = []
for n in [100, 200, 400, 800, 1600]:
    A = np.triu((rng.random((n, n)) < 0.5).astype(float), 1); A = A + A.T
    deg = A.sum(1); C = A @ A
    M = np.maximum.outer(deg, deg)
    kTV = C / M  # = kappa^TV of the step graphon on cells i != j (and = kappa^square)
    off = ~np.eye(n, dtype=bool)
    # independent TV oracle on a few pairs: 1 - TV of normalised rows
    ok_tv = True
    for _ in range(20):
        i, j = rng.choice(n, 2, replace=False)
        tv = 0.5 * np.abs(A[i] / deg[i] - A[j] / deg[j]).sum()
        ok_tv &= abs((1 - tv) - kTV[i, j]) < 1e-12
    L1 = np.abs(kTV[off] - 1).mean() * (n * n - n) / n ** 2 + 0  # diagonal cells: kappa=1, error 0
    U = A - 0.5  # diagonal cells: 0 - 1/2
    opn = np.linalg.norm(U, 2) / n  # >= cut norm of the step kernel
    bound = 2 / np.sqrt(n) + 1 / (2 * n)
    res.append((n, kTV[off].mean(), np.abs(kTV[off] - 0.5).max(), L1, opn, bound, ok_tv))
    print(f"   n={n:5d}: mean kTV {kTV[off].mean():.4f}, max|kTV-1/2| {np.abs(kTV[off]-0.5).max():.4f}, "
          f"||kTV - 1||_L1 {L1:.4f}, ||T_U||op {opn:.4f} (bound {bound:.4f}), TV-oracle {ok_tv}")
check("a-TV-oracle", all(r[6] for r in res), "codeg/maxdeg = 1-TV(rows) on sampled pairs")
norm = [r[2] * np.sqrt(r[0] / np.log(r[0])) for r in res]
check("a-kTV->1/2", res[-1][2] < res[0][2] / 3 and max(norm) / min(norm) < 1.6,
      f"uniform deviation decays like sqrt(log n/n): max|kTV-1/2|*sqrt(n/log n) = {np.round(norm,3)}")
check("a-L1->1/2", abs(res[-1][3] - 0.5) < 0.02, f"||kTV_Wn - kTV_1/2||_L1 = {res[-1][3]:.4f}")
check("a-cut", all(r[4] <= r[5] for r in res), "operator-norm upper bound on cut norm <= 2n^-1/2+1/(2n)")
sl = np.polyfit(np.log([r[0] for r in res]), np.log([r[4] for r in res]), 1)[0]
check("a-cut-rate", abs(sl + 0.5) < 0.1, f"slope of ||T_U||op in log n = {sl:.3f} (expected -1/2)")
check("a-NEG", abs(res[-1][1] - 1) > 0.4, "mutated limit kTV_{W_n} -> 1 rejected")

# Graph Ollivier curvature of G(n,p) edges, alpha=0, hop metric (B-M Thm 6.3(f)) -> p
print("   graph kappa_0 on G(n,1/2) edges (exact LP, primal vs dual):")
gm = []
for n in [40, 80, 160]:
    A = np.triu((rng.random((n, n)) < 0.5).astype(float), 1); A = A + A.T
    E = np.argwhere(np.triu(A, 1) > 0)
    ks, gap = [], 0.0
    for (x, y) in E[rng.choice(len(E), 15, replace=False)]:
        k1, _ = edge_curv(A, x, y, 0.0, lambda s: 1.0, w1_primal)
        k2, _ = edge_curv(A, x, y, 0.0, lambda s: 1.0, w1_dual)
        ks.append(k1); gap = max(gap, abs(k1 - k2))
    gm.append(np.mean(ks))
    print(f"   n={n}: mean kappa_0 {np.mean(ks):.4f}, primal-dual gap {gap:.1e}")
check("a-BM", abs(gm[-1] - 0.5) < abs(gm[-1] - 1) and abs(gm[-1] - 0.5) < 0.1,
      f"graph curvature near p=1/2, not 1 (n=160: {gm[-1]:.4f})")

# Scope of '0 <= kappa^square <= 1': lower bound needs only W>=0, upper bound needs W<=1
lo_viol, up_viol_big = 0, 0
for _ in range(200):
    k = 6
    B = rng.random((k, k)); B = (B + B.T) / 2
    d = B.mean(1); T = B @ B / k
    kb = T / np.maximum.outer(d, d)
    lo_viol += (kb < -1e-15).any()
    B2 = B * 3.0  # W > 1 as along the unnormalised flow (item ii)
    d2 = B2.mean(1); kb2 = (B2 @ B2 / k) / np.maximum.outer(d2, d2)
    up_viol_big += (kb2 > 1 + 1e-12).any()
check("a-ksq>=0", lo_viol == 0, "kappa^square >= 0 for every W >= 0 (200 random step graphons)")
print(f"   note: with W scaled to max 3, kappa^square > 1 in {up_viol_big}/200 cases "
      "(upper bound needs W<=1; the bridge conclusion uses only >= 0)")
# The graph curvature itself CAN be negative: barbell kappa_0 = -4/3 (outside the scope of the claim)
Bb = np.zeros((12, 12))
for i, j in itertools.combinations(range(6), 2):
    Bb[i, j] = Bb[j, i] = 1; Bb[i + 6, j + 6] = Bb[j + 6, i + 6] = 1
Bb[0, 6] = Bb[6, 0] = 1
k0, _ = edge_curv(Bb, 0, 6, 0.0, lambda s: 1.0)
k0d, _ = edge_curv(Bb, 0, 6, 0.0, lambda s: 1.0, w1_dual)
check("a-scope", abs(k0 + 4 / 3) < 1e-9 and abs(k0d + 4 / 3) < 1e-9,
      f"graph kappa_0 on K6-K6 bridge = {k0:.6f} (primal) {k0d:.6f} (dual): negative graph "
      "curvature exists; the chapter's claim is about the graphon curvatures only")
print(f"   ({time.time()-T0:.1f}s)")

# ============================================================ (b) barbell
print("== (b) barbell K6-K6, alpha=1/2, length flow l' = -kappa d")
ALPHA = 0.5
edges = [(0, 6)] + [(0, j) for j in range(1, 6)] + [(6, j) for j in range(7, 12)] + \
    [(i, j) for i, j in itertools.combinations(range(1, 6), 2)] + \
    [(i, j) for i, j in itertools.combinations(range(7, 12), 2)]
assert len(edges) == 31
orbit = np.array([0] + [1] * 10 + [2] * 20)
reps = [0, 1, 11]  # bridge, spoke, far clique edge


def lenmat(l):
    L = np.zeros((12, 12))
    for (i, j), v in zip(edges, l):
        L[i, j] = L[j, i] = v
    return L


def rhs_full(l, phi, w1=w1_primal):
    L = lenmat(l)
    out = np.empty(31)
    for e, (x, y) in enumerate(edges):
        k, d = edge_curv(L, x, y, ALPHA, phi, w1)
        out[e] = -k * d
    return out


def kappa_reps(l3, phi):
    l = np.asarray(l3)[orbit]
    L = lenmat(l)
    ks, ds = [], []
    for e in reps:
        k, d = edge_curv(L, *edges[e], ALPHA, phi)
        ks.append(k); ds.append(d)
    return np.array(ks), np.array(ds)


def rhs_red(l3, phi):
    k, d = kappa_reps(l3, phi)
    return -k * d


one = lambda s: 1.0
gauss = lambda s: np.exp(-s * s)

kb0, _ = edge_curv(Bb, 0, 6, ALPHA, one)
kb0d, _ = edge_curv(Bb, 0, 6, ALPHA, one, w1_dual)
check("b-k0", abs(kb0 + 2 / 3) < 1e-9 and abs(kb0d + 2 / 3) < 1e-9,
      f"bridge kappa_1/2(0) = {kb0:.6f} primal, {kb0d:.6f} dual; hand value -(1-a)*2(1-1/6-1/6) = -2/3")
check("b-k0-NEG", abs(kb0 - (-4 / 3)) > 0.5, "mutated value -4/3 (alpha=0) rejected for alpha=1/2")


def rk4(f, y0, h, T):
    ys = [np.array(y0, float)]; y = ys[0].copy()
    for _ in range(int(round(T / h))):
        k1 = f(y); k2 = f(y + h / 2 * k1); k3 = f(y + h / 2 * k2); k4 = f(y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); ys.append(y.copy())
    return np.array(ys)


def crossing(ts, kb):
    i = np.argmax(kb > 0)
    if kb[i] <= 0:
        return None
    return ts[i - 1] + (ts[i] - ts[i - 1]) * (-kb[i - 1]) / (kb[i] - kb[i - 1])


# Full 31-edge RK4, h=0.02, to t=10 (oracle for the symmetric reduction)
t1 = time.time()
h = 0.02
Yf = rk4(lambda l: rhs_full(l, one), np.ones(31), h, 10.0)
tsf = np.arange(len(Yf)) * h
kbf = np.array([kappa_reps(y[[0, 1, 11]], one)[0][0] for y in Yf])
spread = max(np.ptp(Yf[:, orbit == o], axis=1).max() for o in range(3))
tcf = crossing(tsf, kbf)
print(f"   full flow h=0.02 ({time.time()-t1:.0f}s): orbit spread {spread:.1e}, crossing t*={tcf:.4f}, "
      f"max bridge length {Yf[:,0].max():.4f} at t={tsf[Yf[:,0].argmax()]:.2f}, "
      f"bridge length at t=10 {Yf[-1,0]:.4f}, min length t=10 {Yf[-1].min():.2e}")
grid = kbf[::25]  # samples every 0.5
first_half = 0.5 * np.argmax(grid > 0)
print(f"   kappa_bridge at t=0,2.5,5,7.5,10: {np.round(kbf[[0,125,250,375,500]],4)}; "
      f"first positive sample on the 0.5-grid: t={first_half}")
check("b-orbit", spread < 1e-10, "automorphism orbits keep equal lengths (full flow)")

# Reduced flow refinement + independent integrator
tc, mx = {}, {}
for h in [0.04, 0.02, 0.01, 0.005]:
    Y = rk4(lambda l: rhs_red(l, one), np.ones(3), h, 10.0)
    ts = np.arange(len(Y)) * h
    kb = np.array([kappa_reps(y, one)[0][0] for y in Y])
    tc[h] = crossing(ts, kb); mx[h] = Y[:, 0].max()
    if h == 0.02:
        dev = np.abs(Y[:, 0] - Yf[:, 0]).max()
    print(f"   reduced RK4 h={h}: crossing {tc[h]:.5f}, max bridge length {mx[h]:.5f}")
check("b-red=full", dev < 1e-10, f"reduced vs full 31-edge flow at h=0.02: max |diff| {dev:.1e}")


def ev(t, y):
    return kappa_reps(y, one)[0][0]
ev.terminal = False; ev.direction = 1
sol = solve_ivp(lambda t, y: rhs_red(y, one), (0, 10), np.ones(3), method="DOP853",
                rtol=1e-10, atol=1e-12, events=ev, dense_output=True)
tev = sol.t_events[0][0]
tt = np.linspace(0, 10, 20001)
mxi = sol.sol(tt)[0].max()
print(f"   DOP853 rtol 1e-10: crossing (event) {tev:.5f}, max bridge length {mxi:.5f}")
errs = [abs(tc[h] - tev) for h in [0.04, 0.02, 0.01, 0.005]]
print(f"   |crossing_h - crossing_DOP853|: {['%.1e' % e for e in errs]}")
check("b-cross", abs(tev - 4.1) < 0.1 and abs(tc[0.02] - tev) < 0.02,
      f"crossing t* = {tev:.4f} (chapter: near 4.1)")
check("b-cross-NEG", abs(tev - 4.5) > 0.2, "mutated crossing time 4.5 (source O7) rejected")
check("b-grid", first_half == 4.5,
      "source's 4.5 = first positive sample on a 0.5-spaced output grid (crossing lies in (4.0,4.5])")
check("b-maxlen", mxi < 1.82 and mxi > 1.80, f"bridge length max {mxi:.4f} < 1.82 on [0,10]")
check("b-clique", Yf[-1, 11] < 0.05 and Yf[-1, 1] < Yf[0, 1], "clique edges contract")
Yg = rk4(lambda l: rhs_red(l, gauss), np.ones(3), 0.02, 10.0)
kbg = np.array([kappa_reps(y, gauss)[0][0] for y in Yg])
check("b-NEG-gauss", (kbg < 0).all(), f"control phi=gauss: bridge kappa stays < 0 (t=10: {kbg[-1]:.4f})")
print(f"   ({time.time()-T0:.1f}s)")

# ============================================================ (c) normalised flow
print("== (c) normalised flow dW/dt = 2(kappa^sq - kbar) W")
p, q = sp.symbols("p q", positive=True)
s = p + q
kin = (p ** 2 + q ** 2) / s; kout = 2 * p * q / s
kbar = (p * kin + q * kout) / s
check("c-sym-q", sp.simplify(2 * (kout - kbar) * q + 2 * p * q * (p - q) ** 2 / s ** 2) == 0,
      "qdot = -2pq(p-q)^2/s^2")
check("c-sym-p", sp.simplify(2 * (kin - kbar) * p - 2 * p * q * (p - q) ** 2 / s ** 2) == 0, "pdot = -qdot")
p1, p2 = sp.symbols("p1 p2", positive=True)
S = p1 + p2
kb2 = (p1 ** 2 + p2 ** 2) / S
check("c-sym-wta", sp.simplify(2 * (p1 - kb2) * p1 - 2 * p1 * p2 * (p1 - p2) / S) == 0,
      "p1dot = 2p1p2(p1-p2)/S")
Ss, uu = sp.symbols("S u", positive=True)
# p1 = S(1+u)/2, p2 = S(1-u)/2 ; udot = (p1dot - p2dot)/S = 4 p1 p2 (p1-p2)/S^2
udot = (4 * p1 * p2 * (p1 - p2) / S ** 2).subs({p1: Ss * (1 + uu) / 2, p2: Ss * (1 - uu) / 2})
lin = sp.simplify(sp.diff(udot, uu).subs(uu, 0))
check("c-sym-rate", sp.simplify(lin - Ss) == 0, f"linear growth rate of u at symmetry = {lin}")


def flow_generic(Wb):
    """Independent oracle: step graphon on k equal cells, kappa^square by matrix algebra."""
    k = Wb.shape[0]
    d = Wb.mean(1); T = Wb @ Wb / k
    kap = T / np.maximum.outer(d, d)
    kbar = (kap * Wb).sum() / Wb.sum()
    return 2 * (kap - kbar) * Wb


def rk4_mat(Wb, h, T, rec=None):
    out = []
    for i in range(int(round(T / h))):
        k1 = flow_generic(Wb); k2 = flow_generic(Wb + h / 2 * k1)
        k3 = flow_generic(Wb + h / 2 * k2); k4 = flow_generic(Wb + h * k3)
        Wb = Wb + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        out.append(Wb.copy())
    return Wb, out


eps = 0.1
k = 6
blk = np.zeros((k, k)); blk[:3, :3] = 1; blk[3:, 3:] = 1
W0 = np.where(blk > 0, 1.0, eps)
# closed-form 2-block ODE with solve_ivp
f2 = lambda t, y: [2 * y[0] * y[1] * (y[0] - y[1]) ** 2 / (y[0] + y[1]) ** 2,
                   -2 * y[0] * y[1] * (y[0] - y[1]) ** 2 / (y[0] + y[1]) ** 2]
sol2 = solve_ivp(f2, (0, 12), [1.0, eps], method="DOP853", rtol=1e-12, atol=1e-20, dense_output=True)
errs = []
for h in [0.04, 0.02, 0.01]:
    Wend, _ = rk4_mat(W0.copy(), h, 4.0)
    ref = sol2.sol(4.0)
    errs.append(max(abs(Wend[0, 0] - ref[0]), abs(Wend[0, 5] - ref[1])))
rate = np.log2(errs[0] / errs[1]), np.log2(errs[1] / errs[2])
print(f"   generic 6-cell RK4 vs reduced ODE (DOP853) at t=4: errors {['%.1e' % e for e in errs]}, "
      f"observed orders {rate[0]:.2f}, {rate[1]:.2f}")
check("c-generic", errs[-1] < 1e-9 and min(rate) > 3.0, "6-cell kappa^square flow = 2-block ODE, RK4 order ~4")
tt = np.linspace(6, 12, 61)
qq = sol2.sol(tt)[1]
fit = -np.polyfit(tt, np.log(qq), 1)[0]
pinf = sol2.sol(12)[0]
check("c-rate", abs(fit - 2 * (1 + eps)) < 1e-3, f"q decay rate {fit:.5f} vs 2(1+eps) = {2*(1+eps)}")
check("c-rate-NEG", abs(fit - (1 + eps)) > 0.5, "mutated rate (1+eps) rejected")
check("c-limit", abs(pinf - (1 + eps)) < 1e-8, f"p(12) = {pinf:.10f} -> 1+eps; not [0,1]-valued")
check("c-limit-NEG", abs(pinf - 1.0) > 0.05, "mutated limit 1 (indicator) rejected")
# mass conservation
Wend, _ = rk4_mat(W0.copy(), 0.02, 4.0)
check("c-mass", abs(Wend.sum() - W0.sum()) < 1e-10, "int W conserved")

# winner-take-all: q=0, p1 != p2, generic oracle
Sx = 2.2
for delta in [1e-6]:
    Wb = np.zeros((k, k)); Wb[:3, :3] = Sx / 2 * (1 + delta); Wb[3:, 3:] = Sx / 2 * (1 - delta)
    hs = 0.01
    _, traj = rk4_mat(Wb.copy(), hs, 10.0)
    asym = np.array([(M[0, 0] - M[5, 5]) / (M[0, 0] + M[5, 5]) for M in traj])
    tt2 = hs * (1 + np.arange(len(asym)))
    sel = tt2 < 3.0
    g = np.polyfit(tt2[sel], np.log(asym[sel]), 1)[0]
    Wl, _ = rk4_mat(traj[-1].copy(), 0.01, 30.0)
check("c-wta-rate", abs(g - Sx) < 5e-3, f"asymmetry growth rate {g:.4f} vs S = {Sx}")
check("c-wta-NEG", abs(g - Sx / 2) > 0.5, "mutated rate S/2 rejected")
check("c-wta-limit", abs(Wl[0, 0] - Sx) < 1e-6 and Wl[5, 5] < 1e-6,
      f"p1 -> {Wl[0,0]:.8f} (S), p2 -> {Wl[5,5]:.2e}")
# symmetric data stay symmetric only up to round-off; perturb the symmetric limit
Wsym = np.where(blk > 0, 1 + eps, 0.0); Wsym[:3, :3] *= 1 + 1e-9; Wsym[3:, 3:] *= 1 - 1e-9
_, tr = rk4_mat(Wsym, 0.01, 8.0)
a8 = (tr[-1][0, 0] - tr[-1][5, 5]) / (tr[-1][0, 0] + tr[-1][5, 5])
check("c-unstable", a8 > 1e-9 * np.exp(0.9 * 2.2 * 8), f"perturbation 1e-9 of (1+eps)1_blocks grows to {a8:.2e} by t=8")

print(f"total {time.time()-T0:.1f}s, failures {FAIL}")
sys.exit(FAIL)
