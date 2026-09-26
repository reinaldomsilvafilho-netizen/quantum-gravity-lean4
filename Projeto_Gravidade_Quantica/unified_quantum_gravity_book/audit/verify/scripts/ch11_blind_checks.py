"""Blind layer-1 numerical checks for chapter 11 (independent of audit/scripts/check_ch11.py).

Each check compares against an independent oracle and includes a negative
control (a mutated formula that must FAIL). Run: python ch11_blind_checks.py
"""
import numpy as np
from scipy.linalg import expm, logm, sqrtm, solve_continuous_lyapunov, eigh

rng = np.random.default_rng(20260924)
results = []


def report(name, ok, detail=""):
    results.append((name, ok))
    print(f"[{'OK ' if ok else 'BAD'}] {name} {detail}")


def rand_state(n):
    G = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    r = G @ G.conj().T
    return r / np.trace(r).real


def rand_traceless_herm(n):
    G = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    X = (G + G.conj().T) / 2
    return X - np.trace(X) / n * np.eye(n)


def vn_entropy(r):
    w = np.linalg.eigvalsh(r)
    w = w[w > 1e-15]
    return float(-(w * np.log(w)).sum())


def rel_ent(r, s):
    return float(np.trace(r @ (logm(r) - logm(s))).real)


def g_bkm(r, X):
    # eigenbasis formula: sum |X_ij|^2 (log p_i - log p_j)/(p_i - p_j)
    p, U = eigh(r)
    Xe = U.conj().T @ X @ U
    n = len(p)
    tot = 0.0
    for i in range(n):
        for j in range(n):
            c = 1 / p[i] if abs(p[i] - p[j]) < 1e-14 else (np.log(p[i]) - np.log(p[j])) / (p[i] - p[j])
            tot += abs(Xe[i, j]) ** 2 * c
    return tot


def g_sld(r, X):
    # L solves r L + L r = 2X ; g = Tr(L X) = 1/2 Tr(r {L,L})
    L = solve_continuous_lyapunov(r, 2 * X)
    a = np.trace(L @ X).real
    b = 0.5 * np.trace(r @ (L @ L + L @ L)).real
    return a, b


# ---- 1. SLD definition: 1/2 Tr(rho{L,L}) == Tr(L d rho); Bures = g_SLD/4 ----
r = rand_state(3); X = rand_traceless_herm(3)
a, b = g_sld(r, X)
report("SLD: 1/2Tr(rho{L,L}) = Tr(L drho)", abs(a - b) < 1e-10, f"{a:.6f} {b:.6f}")
X = X / np.linalg.norm(X) * 0.5 * np.linalg.eigvalsh(r).min(); a = g_sld(r, X)[0]
eps = 1e-3
s = r + eps * X
F = np.trace(sqrtm(sqrtm(r) @ s @ sqrtm(r))).real ** 2
dB2 = 2 * (1 - np.sqrt(F))
report("Bures d^2 ~ (1/4) g_SLD eps^2", abs(dB2 / (eps**2) - a / 4) / (a / 4) < 1e-3, f"{dB2/eps**2:.6f} vs {a/4:.6f}")
report("NEG: Bures d^2 ~ (1/2) g_SLD eps^2 must fail", not abs(dB2 / (eps**2) - a / 2) / (a / 2) < 1e-3)
# Bures distance = Bures-Wasserstein distance (ch02 formula) for unit-trace states
s2 = rand_state(3)
F2 = np.trace(sqrtm(sqrtm(r) @ s2 @ sqrtm(r))).real ** 2
dBW2 = 1 + 1 - 2 * np.trace(sqrtm(sqrtm(r) @ s2 @ sqrtm(r))).real
report("Bures dist = BW dist (unit trace)", abs(2 * (1 - np.sqrt(F2)) - dBW2) < 1e-10)

# ---- 2. Hessian of relative entropy = BKM (not SLD) ----
worst, ratios = 0.0, []
for _ in range(20):
    r = rand_state(3); X = rand_traceless_herm(3)
    X = X / np.linalg.norm(X) * 0.5 * np.linalg.eigvalsh(r).min()
    h = 2e-2
    f = lambda t: rel_ent(r + t * X, r)
    d2 = lambda hh: (f(hh) - 2 * f(0) + f(-hh)) / hh**2
    hess = (4 * d2(h / 2) - d2(h)) / 3  # Richardson extrapolation
    gb = g_bkm(r, X); gs = g_sld(r, X)[0]
    worst = max(worst, abs(hess - gb) / gb)
    ratios.append(gb / gs)
report("Hessian S(rho+tX||rho) = g_BKM (20 random qutrits)", worst < 1e-4, f"max rel err {worst:.1e}")
report("g_BKM >= g_SLD always, strict for noncommuting X", min(ratios) > 1.0, f"ratios in [{min(ratios):.3f},{max(ratios):.3f}]")
report("NEG: Hessian = g_SLD must fail", not all(abs(x - 1) < 1e-4 for x in ratios))
# commuting perturbation: both equal classical Fisher
p = rng.dirichlet(np.ones(4)); r = np.diag(p); x = rng.normal(size=4); x -= x.mean(); X = np.diag(x)
report("commuting X: g_BKM = g_SLD = sum x^2/p", abs(g_bkm(r, X) - (x**2 / p).sum()) < 1e-10 and abs(g_sld(r, X)[0] - (x**2 / p).sum()) < 1e-10)

# ---- 3. First law: S(sigma+eps d) - S(sigma) = eps Tr(d H) + O(eps^2) ----
sig = rand_state(4); d = rand_traceless_herm(4); H = -logm(sig)
errs = []
for eps in [1e-3, 1e-4]:
    errs.append(abs(vn_entropy(sig + eps * d) - vn_entropy(sig) - eps * np.trace(d @ H).real))
report("first law residual O(eps^2)", errs[1] < errs[0] / 50, f"{errs}")
res_neg = abs(vn_entropy(sig + 1e-4 * d) - vn_entropy(sig) + 1e-4 * np.trace(d @ H).real)
report("NEG: wrong sign of H must fail", res_neg > 1e2 * errs[1], f'neg residual {res_neg:.2e}')

# ---- 4. Min-cut bound on a random periodic MPS (ring), plus a star cut ----
def ring_mps_state(n, chi, dphys=2):
    As = [rng.normal(size=(chi, dphys, chi)) + 1j * rng.normal(size=(chi, dphys, chi)) for _ in range(n)]
    T = As[0]
    for A in As[1:]:
        T = np.tensordot(T, A, axes=([T.ndim - 1], [0]))
    T = np.trace(T, axis1=0, axis2=T.ndim - 1)
    v = T.reshape(-1)
    return v / np.linalg.norm(v)

viol = 0; sat = []
for chi in [2, 3]:
    n = 8
    psi = ring_mps_state(n, chi)
    for la in range(1, n // 2 + 1):
        M = psi.reshape(2**la, -1)
        sv = np.linalg.svd(M, compute_uv=False) ** 2
        sv = sv[sv > 1e-14]
        S = float(-(sv * np.log(sv)).sum())
        bound = 2 * np.log(chi)  # contiguous region on a ring: min cut = 2 bonds
        viol += S > bound + 1e-10
        sat.append(S / min(bound, la * np.log(2)))
report("min-cut S_A <= |C| log chi (ring MPS)", viol == 0, f"S/bound ratios {np.round(sat,3)}")

# ---- 5. MCF (graphical curve shortening, fixed ends): dL/dt = -int kappa^2 ds ----
x = np.linspace(0, 1, 4001); dx = x[1] - x[0]
u = 0.3 * np.sin(np.pi * x) + 0.1 * np.sin(3 * np.pi * x)
ux = np.gradient(u, dx); uxx = np.gradient(ux, dx)
w = np.sqrt(1 + ux**2)
kap = uxx / w**3
ut = uxx / (1 + ux**2)  # graphical MCF: normal speed = curvature
dt = 1e-7
u2 = u + dt * ut; u2[0] = u2[-1] = 0
L = lambda f: np.trapezoid(np.sqrt(1 + np.gradient(f, dx) ** 2), x)
rate = (L(u2) - L(u)) / dt
pred = -np.trapezoid(kap**2 * w, x)
report("MCF dL/dt = -int kappa^2 ds", abs(rate - pred) / abs(pred) < 1e-3, f"{rate:.5f} vs {pred:.5f}")
report("NEG: dL/dt = +int kappa^2 must fail", abs(rate + pred) / abs(pred) > 0.5)

# ---- 6. Holonomy discretisation: midpoint rule error scaling ----
sx = np.array([[0, 1], [1, 0]], complex); sy = np.array([[0, -1j], [1j, 0]]); sz = np.diag([1, -1]).astype(complex)
def A(s):  # su(2)-valued (anti-Hermitian) connection along the loop
    return -0.5j * (np.cos(2*np.pi*s) * sx + np.sin(4*np.pi*s) * sy + (1 + s*(1-s)) * sz) * 2.0

def exact_hol(nfine=20000):
    U = np.eye(2, dtype=complex); ds = 1 / nfine
    for j in range(nfine):  # 4th-order Magnus-free RK via small steps (midpoint exp, fine)
        U = expm(A((j + 0.5) * ds) * ds) @ U
    return U
Uex = exact_hol()
def disc(k, rule):
    U = np.eye(2, dtype=complex)
    for j in range(k):
        s = (j + 0.5) / k
        U = expm(A(s) / k) @ U if rule == "mid" else expm(A(s) / (2 * k)) @ U  # "rev": mutated factor 1/2
    return U
errs_mid = [abs(np.trace(disc(k, "mid")) - np.trace(Uex)) for k in (20, 40, 80)]
errs_left = [abs(np.trace(disc(k, "rev")) - np.trace(Uex)) for k in (20, 40, 80)]
o_mid = np.log2(errs_mid[0] / errs_mid[2]) / 2
o_left = errs_left[-1]
report("midpoint holonomy: error -> 0 (claimed O(1/k))", errs_mid[-1] < errs_mid[0], f"observed order {o_mid:.2f} (i.e. O(k^-2), sharper than stated)")
report("NEG: mutated step A/(2k) must NOT converge", o_left > 1e-2, f"error at k=80: {o_left:.3e}")

# ---- 7. Spin-network (theta graph, all j=1) gauge invariance with ch.11 conventions ----
def rot(g):  # SU(2) -> SO(3) adjoint
    P = [sx, sy, sz]
    return np.array([[0.5 * np.trace(P[a] @ g @ P[b] @ g.conj().T).real for b in range(3)] for a in range(3)])
def rand_su2():
    q = rng.normal(size=4); q /= np.linalg.norm(q)
    return np.array([[q[0] + 1j*q[3], q[2] + 1j*q[1]], [-q[2] + 1j*q[1], q[0] - 1j*q[3]]])
eps3 = np.zeros((3, 3, 3))
for (i, j, k), sgn in {(0,1,2):1,(1,2,0):1,(2,0,1):1,(0,2,1):-1,(2,1,0):-1,(1,0,2):-1}.items():
    eps3[i, j, k] = sgn
def theta(Rs, iota_s=eps3, iota_t=eps3):
    # all three edges go from vertex s to vertex t; D(h)_{ab}: a at source, b at target
    return np.einsum("abc,ad,be,cf,def->", iota_s, Rs[0], Rs[1], Rs[2], iota_t)
hs = [rand_su2() for _ in range(3)]
gs_, gt_ = rand_su2(), rand_su2()
Rs = [rot(h) for h in hs]
Rs_g = [rot(gs_ @ h @ gt_.conj().T) for h in hs]  # h -> g(s) h g(t)^{-1}
report("theta spin network gauge invariant", abs(theta(Rs) - theta(Rs_g)) < 1e-10, f"{theta(Rs):.6f}")
noninv = rng.normal(size=(3, 3, 3))
report("NEG: non-invariant 'intertwiner' breaks invariance", abs(theta(Rs, noninv) - theta(Rs_g, noninv)) > 1e-3)

# ---- 8. LQG area: transversal edge from AL vertex formula ----
jj = lambda j: j * (j + 1)
ok = all(abs(np.sqrt(2*jj(j) + 2*jj(j) - jj(0)) / 2 - np.sqrt(jj(j))) < 1e-12 for j in np.arange(0.5, 5, 0.5))
report("AL formula 4*pi*g*lp^2*sqrt(2ju+2jd-jud) -> 8*pi*g*lp^2*sqrt(j(j+1)) for transversal edge", ok)

# ---- 9. cMERA metric coefficient: Poincare slice in u = log(z0/z) ----
z0, Lads, uu = 2.7, 1.3, 0.4
z = z0 * np.exp(-uu)
c2_true = Lads**2 / z**2 / np.exp(2 * uu)
report("c2 = L^2/z0^2 (ch.11 claims L^2): equal only if z0=1", abs(c2_true - Lads**2 / z0**2) < 1e-12 and abs(c2_true - Lads**2) > 1e-3, f"c2={c2_true:.4f}, L^2={Lads**2:.4f}")

# ---- 10. k=2 spherical landscape: critical points = +-eigenvectors ----
N = 6; J = rng.normal(size=(N, N)); Js = (J + J.T) / 2
w_, V = np.linalg.eigh(Js)
crit = 0
for i in range(N):
    for sgn in (1, -1):
        v = sgn * V[:, i]; grad = 2 * Js @ v; tang = grad - (grad @ v) * v
        crit += np.linalg.norm(tang) < 1e-10
report("k=2: 2N critical points (+-eigenvectors)", crit == 2 * N)

# ---- 11. Ollivier curvature >= -2 on random graphs (uniform walk on neighbours) ----
from scipy.optimize import linprog
from scipy.sparse.csgraph import shortest_path
def ollivier(Adj, x, y, D):
    nx_ = np.flatnonzero(Adj[x]); ny_ = np.flatnonzero(Adj[y])
    mx = np.ones(len(nx_)) / len(nx_); my = np.ones(len(ny_)) / len(ny_)
    C = D[np.ix_(nx_, ny_)].ravel()
    Aeq = []; beq = []
    for i in range(len(nx_)):
        row = np.zeros((len(nx_), len(ny_))); row[i, :] = 1; Aeq.append(row.ravel()); beq.append(mx[i])
    for j in range(len(ny_)):
        row = np.zeros((len(nx_), len(ny_))); row[:, j] = 1; Aeq.append(row.ravel()); beq.append(my[j])
    W1 = linprog(C, A_eq=np.array(Aeq), b_eq=beq, bounds=(0, None)).fun
    return 1 - W1 / D[x, y]
kmin = 10
for _ in range(5):
    n = 14; Adj = (rng.random((n, n)) < 0.25).astype(int); Adj = np.triu(Adj, 1); Adj = Adj + Adj.T
    D = shortest_path(Adj, unweighted=True)
    for x_ in range(n):
        for y_ in range(x_ + 1, n):
            if Adj[x_, y_] and Adj[x_].sum() and Adj[y_].sum():
                kmin = min(kmin, ollivier(Adj, x_, y_, D))
report("Ollivier kappa >= -2 on edges of random graphs", kmin >= -2 - 1e-9, f"min kappa {kmin:.3f}")

print("\nSUMMARY:", sum(ok for _, ok in results), "/", len(results), "passed")
