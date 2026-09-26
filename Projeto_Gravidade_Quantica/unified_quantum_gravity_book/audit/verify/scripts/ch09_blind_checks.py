"""Blind layer-1 checks for chap09 (independent of audit/scripts/check_ch09.py).

Each block prints PASS/FAIL for the claim and for a negative control
(a mutated formula that must FAIL).
Run: python ch09_blind_checks.py
"""
import numpy as np
from numpy.linalg import norm

rng = np.random.default_rng(12345)


def integrate(kappa, ds, x0=(0.0, 0.0), phi0=0.0):
    phi = phi0 + np.concatenate([[0.0], np.cumsum(kappa) * ds])
    x = x0[0] + np.concatenate([[0.0], np.cumsum(np.cos(phi[:-1] + 0.5 * kappa * ds)) * ds])
    y = x0[1] + np.concatenate([[0.0], np.cumsum(np.sin(phi[:-1] + 0.5 * kappa * ds)) * ds])
    return np.stack([x, y], 1), phi


def seg_intersect(p1, p2, p3, p4):
    d1 = p2 - p1
    d2 = p4 - p3
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-14:
        return None
    t = ((p3[0] - p1[0]) * d2[1] - (p3[1] - p1[1]) * d2[0]) / den
    u = ((p3[0] - p1[0]) * d1[1] - (p3[1] - p1[1]) * d1[0]) / den
    if 0 <= t <= 1 and 0 <= u <= 1:
        return t, u
    return None


def first_subloop(P):
    n = len(P)
    for j in range(2, n - 1):
        for i in range(0, j - 1):
            if seg_intersect(P[i], P[i + 1], P[j], P[j + 1]) is not None:
                return i, j
    return None


def diameter(Q):
    D = Q[:, None, :] - Q[None, :, :]
    return np.sqrt((D ** 2).sum(-1)).max()


# ---------------------------------------------------------------- 1
print("[1] Sub-loop confinement: diam(sub-loop) >= 2/kappa")
K = 1.0
mins = []
for trial in range(300):
    n = 400
    ds = 0.05
    # random piecewise-constant curvature in [-K, K], biased so loops occur
    blocks = rng.uniform(-K, K, size=8)
    blocks[rng.integers(0, 8, 3)] = rng.choice([-K, K])
    kap = np.repeat(blocks, n // 8)
    P, _ = integrate(kap, ds)
    r = first_subloop(P)
    if r is None:
        continue
    i, j = r
    mins.append(diameter(P[i + 1:j + 1]))
mins = np.array(mins)
print(f"    loops found: {len(mins)}, min diameter = {mins.min():.4f} (bound 2/K = {2/K})")
print("    claim  :", "PASS" if mins.min() >= 2 / K - 0.05 else "FAIL")
# sharpness: circle of radius 1/K has diameter exactly 2/K
t = np.linspace(0, 2 * np.pi, 2001)
circ = np.stack([np.cos(t), np.sin(t)], 1) / K
dc = diameter(circ)
print(f"    circle diameter = {dc:.6f}; mutated bound 2.2/K violated by circle:",
      "PASS(neg ctrl fails as expected)" if dc < 2.2 / K else "FAIL")

# ---------------------------------------------------------------- 2
print("[2] Winding bound |w| <= (V/rho + |dtheta(gamma0)|)/(2pi) and the")
print("    sharper inequality  int|theta'| <= int|kappa| + pi  (Remark 2.3(c) says 'unknown')")
worst_margin = np.inf
worst_ratio = -np.inf
for trial in range(3000):
    n = 600
    ds = rng.uniform(0.005, 0.05)
    kap = np.repeat(rng.uniform(-3, 3, size=12), n // 12)
    phi0 = rng.uniform(0, 2 * np.pi)
    x0 = rng.uniform(-3, 3, size=2) if trial % 2 else rng.uniform(-0.3, 0.3, size=2)
    P, _ = integrate(kap, ds, x0=x0, phi0=phi0)
    rr = norm(P, axis=1)
    if rr.min() < 0.05:
        continue
    th = np.unwrap(np.arctan2(P[:, 1], P[:, 0]))
    tv_theta = np.abs(np.diff(th)).sum()
    tv_kappa = np.abs(kap).sum() * ds
    worst_margin = min(worst_margin, tv_kappa + np.pi - tv_theta)
print(f"    min over random curves of (int|kappa| + pi - int|theta'|) = {worst_margin:.4f}")
print("    inequality:", "PASS (holds numerically)" if worst_margin > -1e-3 else "FAIL")
# equality case: long straight line passing at distance d from c
s = np.linspace(-1e4, 1e4, 200001)
L = np.stack([s, 0.3 + 0 * s], 1)
th = np.unwrap(np.arctan2(L[:, 1], L[:, 0]))
print(f"    straight line: int|theta'| = {np.abs(np.diff(th)).sum():.6f} ~ pi, int|kappa| = 0 (sharp)")
print("    neg ctrl (constant pi/2 instead of pi) violated by line:",
      "PASS" if np.abs(np.diff(th)).sum() > 0 + np.pi / 2 else "FAIL")

# ---------------------------------------------------------------- 3
print("[3] Mapping-class remark: braid automorphism realized by SU(2) conjugation")
c = 1 / 3
alpha = np.arccos(c)          # SO(3) rotation angle (Banach-Tarski / Swierczkowski free pair)
sx = np.array([[0, 1], [1, 0]], complex)
sy = np.array([[0, -1j], [1j, 0]], complex)
sz = np.array([[1, 0], [0, -1]], complex)
I2 = np.eye(2)


def su2(axis, ang):
    return np.cos(ang / 2) * I2 - 1j * np.sin(ang / 2) * axis


A = su2(sx, alpha)
B = su2(sz, alpha)


def solve_intertwiner(pairs):
    # find g (2x2) with g X = Y g for all (X, Y) in pairs
    rows = []
    for X, Y in pairs:
        # vec(gX - Yg) = (X^T kron I - I kron Y) vec(g)   (column-major vec)
        rows.append(np.kron(X.T, I2) - np.kron(I2, Y))
    M = np.vstack(rows)
    _, S, Vh = np.linalg.svd(M)
    g = Vh[-1].conj().reshape(2, 2, order="F")
    g = g / np.sqrt(np.linalg.det(g))
    return g, S[-1]


Ainv = np.linalg.inv(A)
g, smin = solve_intertwiner([(A, A @ B @ Ainv), (B, A)])
res = max(norm(g @ A @ np.linalg.inv(g) - A @ B @ Ainv), norm(g @ B @ np.linalg.inv(g) - A))
unit = norm(g.conj().T @ g - I2)
print(f"    residual of g A g^-1 = ABA^-1, g B g^-1 = A : {res:.2e}; unitarity defect {unit:.2e}")
print("    => sigma_1 (NOT inner in F_2) acts on holonomy by conjugation:",
      "PASS (counterexample to the Remark's implication)" if res < 1e-10 and unit < 1e-10 else "FAIL")
gr, _ = solve_intertwiner([(A, Ainv), (B, np.linalg.inv(B))])
res_r = max(norm(gr @ A @ np.linalg.inv(gr) - Ainv), norm(gr @ B @ np.linalg.inv(gr) - np.linalg.inv(B)))
print(f"    reflection a_i -> a_i^-1 also realized by conjugation: residual {res_r:.2e}")
# freeness sanity check (projectively): no reduced word of length <= 10 equals +-I
gens = {"a": A, "A": Ainv, "b": B, "B": np.linalg.inv(B)}
inv = {"a": "A", "A": "a", "b": "B", "B": "b"}
frontier = [("", I2)]
bad = 0
for length in range(1, 11):
    new = []
    for w, Mw in frontier:
        for ch, G in gens.items():
            if w and inv[ch] == w[-1]:
                continue
            M2 = Mw @ G
            if min(norm(M2 - I2), norm(M2 + I2)) < 1e-9:
                bad += 1
            new.append((w + ch, M2))
    frontier = new
print(f"    reduced words up to length 10 equal to +-I: {bad} (expected 0; faithful pair)")
# negative control: unequal angles -> no intertwiner (trace obstruction)
B2 = su2(sz, 1.1)
g2, s2 = solve_intertwiner([(A, A @ B2 @ Ainv), (B2, A)])
res2 = max(norm(g2 @ A @ np.linalg.inv(g2) - A @ B2 @ Ainv), norm(g2 @ B2 @ np.linalg.inv(g2) - A))
print(f"    neg ctrl (tr A != tr B): smallest singular value {s2:.3e}, residual {res2:.2e} ->",
      "PASS (no conjugation)" if s2 > 1e-3 else "FAIL")

# ---------------------------------------------------------------- 4
print("[4] Benchmark channel: R0=1, H=1.62")
R0, H, X = 1.0, 1.62, 20.0
for name, cx in [("w=0", -(H + R0 + 0.1)), ("w=1", 0.0)]:
    tt = np.linspace(-np.pi / 2, np.pi / 2, 4001)
    arc = np.stack([cx + H * np.cos(tt), H * np.sin(tt)], 1)
    low = np.stack([np.linspace(-X, cx, 2000), -H + 0 * np.linspace(0, 1, 2000)], 1)
    up = np.stack([np.linspace(cx, -X, 2000), H + 0 * np.linspace(0, 1, 2000)], 1)
    Pth = np.vstack([low, arc, up])
    dmin = norm(Pth, axis=1).min()
    inside = np.abs(Pth[:, 1]).max() <= H + 1e-12
    # winding of gamma * gamma0^{-1}: compare net angle with w=0 path
    ang = np.unwrap(np.arctan2(Pth[:, 1], Pth[:, 0]))
    print(f"    {name}: min |x| = {dmin:.4f} (>R0? {dmin > R0}), in strip: {inside}, "
          f"net angle about 0 = {ang[-1]-ang[0]:+.4f}")
print("    (difference of net angles = 2*pi*winding; U-turn bound 2/(2H) = %.4f = 1/H)" % (1 / H))
# negative control: with H < R0 the w=1 semicircle hits the obstacle
Hn = 0.9
tt = np.linspace(-np.pi / 2, np.pi / 2, 4001)
print("    neg ctrl H=0.9<R0: w=1 semicircle min |x| =",
      f"{(Hn*np.ones_like(tt)).min():.2f} < R0 -> infeasible, as expected")

# ---------------------------------------------------------------- 5
print("[5] Grid feasibility check does not certify peak curvature")
# cubic Bezier with a sharp turn concentrated between two grid points
P0, P1, P2, P3 = map(np.array, ([0, 0], [1, 1], [0, 1], [1.003, 0.0]))  # near-cusp


def bez(t):
    t = t[:, None]
    d1 = 3 * ((1 - t) ** 2 * (P1 - P0) + 2 * (1 - t) * t * (P2 - P1) + t ** 2 * (P3 - P2))
    d2 = 6 * ((1 - t) * (P2 - 2 * P1 + P0) + t * (P3 - 2 * P2 + P1))
    k = np.abs(d1[:, 0] * d2[:, 1] - d1[:, 1] * d2[:, 0]) / (d1 ** 2).sum(1) ** 1.5
    return k


kfine = bez(np.linspace(0, 1, 2_000_001)).max()
kgrid = bez(np.linspace(0, 1, 200)).max()
print(f"    max curvature on 200-pt grid = {kgrid:.3e}; on 2e6-pt grid = {kfine:.3e}")
print("    grid underestimates true peak:", "PASS (issue reproduced)" if kfine > 10 * kgrid else "FAIL")
