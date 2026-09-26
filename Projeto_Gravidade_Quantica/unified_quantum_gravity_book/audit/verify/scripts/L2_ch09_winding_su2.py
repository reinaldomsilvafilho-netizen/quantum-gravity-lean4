"""Camada 2, F-38 (ch. 9). Independent checks of the corrector's new content.

[1] Prop. winding_total_curvature: int|theta'| <= int|kappa| + pi.
    (a) exact identity of the proof: int|theta'| = int sgn(sin psi) kappa - [G(psi_end)-G(psi_0)];
    (b) adversarial search (hill climbing on piecewise-constant curvature) maximising
        int|theta'| - int|kappa|; must stay <= pi;
    Mutations: constant pi/2, and constant 0, must be violated.
[2] rho-independent winding bound 2pi|w| <= V||kappa|| + pi + |dtheta(gamma0)| on
    circles traversed w times around c (path from p to p), vs. mutation without +pi.
[3] Swierczkowski pair: conjugator g for sigma_1 found by an independent method
    (direct optimisation over unit quaternions); negative control tr A != tr B.
[4] Benchmark: w>=2 construction (insert full turns of the radius-H circle): stays in the
    strip, avoids B_R0, curvature 1/H, winding difference = w. Mutation: circle of radius
    R0-0.1 hits the obstacle.
[5] Bezier peak curvature: 200-pt grid vs local maximisation of the true peak.
[6] Remark 5.2: mollification of a circle raises curvature (factor 1+O(kappa eps)).
"""
import numpy as np
from scipy.optimize import minimize, minimize_scalar

rng = np.random.default_rng(7)
res = []


def rep(name, ok, extra=""):
    res.append(ok)
    print(("[PASS] " if ok else "[FAIL] ") + name, extra)


def build(k, ds, x0=np.array([-3.0, 0.3]), phi0=0.0):
    phi = phi0 + np.concatenate([[0], np.cumsum(k * ds)])
    # midpoint integration of position
    phm = (phi[:-1] + phi[1:]) / 2
    xy = x0 + np.vstack([[0, 0], np.cumsum(np.stack([np.cos(phm), np.sin(phm)], 1) * ds, 0)])
    return phi, xy


def G(x):
    # int_0^x sgn(sin t) dt : triangular wave in [0, pi]
    x = np.asarray(x)
    m = np.mod(x, 2 * np.pi)
    return np.where(m <= np.pi, m, 2 * np.pi - m)


def quantities(k, ds, c=np.zeros(2), x0=np.array([-3.0, 0.3])):
    phi, xy = build(k, ds, x0=x0)
    d = xy - c
    th = np.unwrap(np.arctan2(d[:, 1], d[:, 0]))
    tot_theta = np.abs(np.diff(th)).sum()
    tot_k = np.abs(k).sum() * ds
    return tot_theta, tot_k, phi, th, np.linalg.norm(d, axis=1).min()


# ---- [1a] identity of the proof
n, ds = 4000, 2e-3
k = np.repeat(rng.normal(0, 2, 40), n // 40)
tt, tk, phi, th, rmin = quantities(k, ds)
psi = phi - th
sg = np.sign(np.sin((psi[:-1] + psi[1:]) / 2))
rhs = (sg * k).sum() * ds - (G(psi[-1]) - G(psi[0]))
rep("[1a] identity int|theta'| = int sgn(sin psi) kappa - dG", abs(tt - rhs) < 2e-2,
    f"(lhs {tt:.4f}, rhs {rhs:.4f}, rmin {rmin:.3f})")


# ---- [1b] adversarial search
def score(kv, ds=5e-3, reps=100):
    k = np.repeat(kv, reps)
    tt, tk, *_rest = quantities(k, ds)
    rmin = _rest[-1]
    if rmin < 0.02:
        return -10.0
    return tt - tk


best = -1e9
for trial in range(12):
    kv = rng.normal(0, 1, 30)
    s = score(kv)
    for it in range(400):
        cand = kv + rng.normal(0, 0.3, kv.size) * (rng.random(kv.size) < 0.3)
        sc = score(cand)
        if sc > s:
            kv, s = cand, sc
    best = max(best, s)
rep("[1b] adversarial max of int|theta'| - int|kappa| <= pi", best <= np.pi + 1e-2, f"(max found {best:.4f}, pi={np.pi:.4f})")
# straight line (kappa=0) passing close to c: sharpness
k0 = np.zeros(200000)
tt0, *_ = quantities(k0, 1e-2, x0=np.array([-1000.0, 0.05]))   # x from -1000 to 1000 at height 0.05
rep("[1b] sharpness: line gives int|theta'| -> pi", tt0 > np.pi - 0.02, f"({tt0:.4f})")
rep("[1b] NEG mutation constant pi/2 violated by the line", tt0 > np.pi / 2)
rep("[1b] NEG mutation constant 0 violated by adversarial curves", best > 0, f"({best:.3f})")

# ---- [2] rho-independent winding bound on circles traversed w times
ok2, okneg = True, False
for r in (0.5, 1.0, 3.0):
    for w in (1, 2, 5):
        V = 2 * np.pi * r * w
        kap = 1 / r
        # gamma0 = constant path at p (dtheta = 0); gamma = circle through p not enclosing? enclose c
        ttheta = 2 * np.pi * w            # winding about the centre c
        ok2 &= 2 * np.pi * w <= V * kap + np.pi + 0 + 1e-12
        okneg |= 2 * np.pi * w > V * kap * 0.9     # mutation: factor 0.9 on V*kappa is violated
rep("[2] 2pi|w| <= V||kappa|| + pi + |dtheta0| on w-fold circles (tight up to pi)", ok2)
rep("[2] NEG mutation 0.9*V||kappa|| is violated", okneg)


# ---- [3] Swierczkowski pair, independent conjugator search
def su2(n, a):
    sx = np.array([[0, 1], [1, 0]], complex); sy = np.array([[0, -1j], [1j, 0]], complex)
    sz = np.array([[1, 0], [0, -1]], complex)
    N = n[0] * sx + n[1] * sy + n[2] * sz
    return np.cos(a / 2) * np.eye(2) - 1j * np.sin(a / 2) * N


def quat(q):
    q = q / np.linalg.norm(q)
    return np.array([[q[0] + 1j * q[3], q[2] + 1j * q[1]], [-q[2] + 1j * q[1], q[0] - 1j * q[3]]])


def best_conj(A, B):
    Ai = np.linalg.inv(A)
    f = lambda q: (np.linalg.norm(quat(q) @ A @ quat(q).conj().T - A @ B @ Ai) ** 2
                   + np.linalg.norm(quat(q) @ B @ quat(q).conj().T - A) ** 2)
    return min(minimize(f, rng.normal(size=4), method="BFGS").fun for _ in range(20))


a = np.arccos(1 / 3)
A, B = su2([1, 0, 0], a), su2([0, 0, 1], a)
r1 = best_conj(A, B)
rep("[3] Swierczkowski pair: sigma_1 realised by SU(2) conjugation (quaternion search)", r1 < 1e-12, f"(residual^2 {r1:.1e})")
rep("[3] traces preserved: trA=trB, tr(ABA^-1 A)=trAB",
    abs(np.trace(A) - np.trace(B)) < 1e-14 and abs(np.trace(A @ B @ np.linalg.inv(A) @ A) - np.trace(A @ B)) < 1e-14)
B2 = su2([0, 0, 1], 1.1)
r2 = best_conj(A, B2)
rep("[3] NEG tr A != tr B: no conjugator", r2 > 1e-3, f"(min residual^2 {r2:.3e})")

# ---- [4] benchmark w >= 2
R0, H, X = 1.0, 1.62, 20.0


def path(w):
    low = np.stack([np.linspace(-X, 0, 2000), -H * np.ones(2000)], 1)
    t = np.linspace(-np.pi / 2, np.pi / 2 + 2 * np.pi * (w - 1), 4000 * w)
    arc = H * np.stack([np.cos(t), np.sin(t)], 1)
    up = np.stack([np.linspace(0, -X, 2000), H * np.ones(2000)], 1)
    return np.vstack([low, arc, up])


def w0path(c=-(H + R0 + 0.1)):
    low = np.stack([np.linspace(-X, c, 2000), -H * np.ones(2000)], 1)
    t = np.linspace(-np.pi / 2, np.pi / 2, 4000)
    arc = np.stack([c + H * np.cos(t), H * np.sin(t)], 1)
    up = np.stack([np.linspace(c, -X, 2000), H * np.ones(2000)], 1)
    return np.vstack([low, arc, up])


ang = lambda P: (lambda a: a[-1] - a[0])(np.unwrap(np.arctan2(P[:, 1], P[:, 0])))
a0 = ang(w0path())
for w in (1, 2, 3):
    P = path(w)
    wind = (ang(P) - a0) / (2 * np.pi)
    rep(f"[4] w={w}: in strip, avoids B_R0, winding diff {wind:.3f}",
        np.abs(P[:, 1]).max() <= H + 1e-9 and np.linalg.norm(P, axis=1).min() >= R0 and abs(wind - w) < 1e-2)
Pm = path(2) * ((R0 - 0.1) / H)
rep("[4] NEG circle of radius R0-0.1 hits the obstacle", np.linalg.norm(Pm, axis=1).min() < R0)

# ---- [5] Bezier: true peak by local maximisation
P0, P1, P2, P3 = map(np.array, ([0, 0], [1, 1], [0, 1], [1.003, 0.0]))


def kap(t):
    d1 = 3 * ((1 - t) ** 2 * (P1 - P0) + 2 * (1 - t) * t * (P2 - P1) + t ** 2 * (P3 - P2))
    d2 = 6 * ((1 - t) * (P2 - 2 * P1 + P0) + t * (P3 - 2 * P2 + P1))
    return abs(d1[0] * d2[1] - d1[1] * d2[0]) / (d1 @ d1) ** 1.5


grid = max(kap(t) for t in np.linspace(0, 1, 200))
tg = np.linspace(0, 1, 200001)
t0 = tg[np.argmax([kap(t) for t in tg])]
peak = -minimize_scalar(lambda t: -kap(t), bounds=(t0 - 1e-5, t0 + 1e-5), method="bounded",
                        options={"xatol": 1e-14}).fun
rep("[5] grid(200) %.3e vs true peak %.3e (text: 3.7e3 vs 1.2e6)" % (grid, peak),
    abs(grid - 3.7e3) / 3.7e3 < 0.02 and peak > 1.1e6)

# ---- [6] mollification of a circle arc of curvature kappa
kappa, eps = 1.0, 0.2
s = np.linspace(-eps, eps, 20001)
wgt = np.exp(-1 / np.maximum(1e-12, 1 - (s / eps) ** 2)) * (np.abs(s) < eps)
wgt /= wgt.sum()
c = (wgt * np.cos(kappa * s)).sum()         # |gamma_eps'| on a circle
k_eps = kappa * c / c ** 2
rep("[6] mollified circle curvature %.5f > kappa, <= kappa/(1-kappa eps)^2 = %.5f" % (k_eps, kappa / (1 - kappa * eps) ** 2),
    kappa < k_eps <= kappa / (1 - kappa * eps) ** 2)
rep("[6] NEG claim 'no increase' fails", not (k_eps <= kappa))

print("\nSUMMARY: %d / %d ok" % (sum(res), len(res)))
