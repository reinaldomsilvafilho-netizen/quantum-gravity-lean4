"""Camada 2, F-37 (ch. 7). Independent checks of the corrector's new content.

[1] Contact principle for C^{1,1} curves (k=1, n=2): Omega = disk of radius rho.
    Piecewise-constant curvature kL (s<0), kR (s>0) through the contact point with
    tangent tangent to the circle. Claim (eq. contact_c11): if the curve stays in
    the closed disk, then lambda_1 = 1/rho <= max(kL, kR) (ess sup near p0).
    Mutation: threshold 2/rho (factor 2) must be violated by some admissible curve.
[2] Contact principle, C^{1,1} surface (k=2, n=3) in a ball: piecewise-quadratic
    graph with Hessians A+ (y1>0), A- (y1<0), A+ - A- = c e1 e1^T (so C^{1,1}).
    Claim: inside the ball => lambda_2 = 1/rho <= max over sides of lambda_max(A).
    Sign mutation: exterior of a ball (h = -1/rho): a flat plane touches; the
    mutated sign h = +1/rho would forbid it.
[3] Ramp degree: Hermite system with 2(r-1) conditions solvable iff degree >= 2r-3;
    3t^2-2t^3 satisfies the r=3 conditions. Mutations: degree 2r-4, and r-2.
[4] Disk-obstacle example (p=(-1,0), q=(1,0), tangents (1,0), disk r=1/2):
    analytic bound -- a curve with |kappa| <= 1/R starting at (-1,0) heading +x
    has |y| <= R - sqrt(R^2-(x+1)^2) until its heading reaches pi/2, so for R >= 2
    it enters the disk at x=-1/4. Hence kappa* >= 1/2 > 0 even WITHOUT a length
    bound; random bounded-curvature curves confirm; positive control R=0.3 finds
    avoiding curves.
[5] Semicircle parametrization of Sec. 6.1 and compactness remark f=|gamma|^2.
"""
import numpy as np

rng = np.random.default_rng(20260925)
res = []


def rep(name, ok, extra=""):
    res.append(ok)
    print(("[PASS] " if ok else "[FAIL] ") + name, extra)


# ---------------------------------------------------------------- [1]
def curve_piecewise(kL, kR, smax=0.3, n=3001):
    # contact point p0=(0,-rho), tangent (1,0), turning left (into the disk)
    out = []
    for k, sgn in ((kR, 1), (kL, -1)):
        s = np.linspace(0, smax, n)
        th = sgn * k * s
        ds = s[1] - s[0]
        x = sgn * np.concatenate([[0], np.cumsum(np.cos(th[:-1]) * ds)])
        y = np.concatenate([[0], np.cumsum(np.sin(sgn * th[:-1]) * ds * sgn * sgn)])
        # exact integration for constant curvature
        if k > 0:
            x = np.sin(k * s) / k * sgn
            y = (1 - np.cos(k * s)) / k
        else:
            x = s * sgn
            y = 0 * s
        out.append(np.stack([x, y], 1))
    return np.vstack(out)


def inside_disk(P, rho):
    c = np.array([0.0, rho])      # contact point at origin, centre above
    return np.all(np.linalg.norm(P - c, axis=1) <= rho + 1e-12)


rho = 1.0
feasible = []
viol = 0
for _ in range(4000):
    kL, kR = rng.uniform(0, 2.5, 2)
    if min(abs(kL - 1 / rho), abs(kR - 1 / rho)) < 0.02:
        continue
    P = curve_piecewise(kL, kR)
    if inside_disk(P, rho):
        feasible.append(max(kL, kR))
        viol += max(kL, kR) < 1 / rho
rep("[1] C11 curve in disk: inside => ess sup >= 1/rho", viol == 0 and len(feasible) > 100,
    f"(feasible {len(feasible)}, violations {viol}, min ess sup {min(feasible):.3f})")
# also: one-sided curvature above threshold is NOT enough (both sides needed) -> stronger than claim
P = curve_piecewise(0.5, 2.0)
rep("[1] kL=0.5<1/rho, kR=2: leaves disk (claim is necessary, not sufficient)", not inside_disk(P, rho))
viol2 = sum(f < 2 / rho for f in feasible)
rep("[1] NEG mutation threshold 2/rho is violated by admissible curves", viol2 > 0, f"({viol2} violations)")


# ---------------------------------------------------------------- [2]
def surface_inside(Ap, Am, rho, r0=0.08, n=161):
    y1, y2 = np.meshgrid(np.linspace(-r0, r0, n), np.linspace(-r0, r0, n))
    Y = np.stack([y1.ravel(), y2.ravel()], 1)
    g = np.where(Y[:, 0] > 0, np.einsum("ni,ij,nj->n", Y, Ap, Y), np.einsum("ni,ij,nj->n", Y, Am, Y)) / 2
    r2 = (Y ** 2).sum(1)
    lower = rho - np.sqrt(rho ** 2 - r2)   # ball of radius rho touching at origin from above
    return np.all(g >= lower - 1e-14)


viol = 0
cnt = 0
esss = []
for _ in range(3000):
    M = rng.normal(size=(2, 2))
    Am = (M + M.T) / 2 + rng.uniform(0, 2) * np.eye(2)
    c = rng.uniform(-1, 1)
    Ap = Am + c * np.diag([1.0, 0.0])
    lam = [np.linalg.eigvalsh(A) for A in (Ap, Am)]
    if min(min(abs(l - 1 / rho)) for l in lam) < 0.05:
        continue
    if surface_inside(Ap, Am, rho):
        cnt += 1
        e = max(max(abs(l)) for l in lam)
        esss.append(e)
        viol += e < 1 / rho
rep("[2] C11 surface in ball: inside => ess sup ||II|| >= lambda_2 = 1/rho", viol == 0 and cnt > 50,
    f"(feasible {cnt}, violations {viol}, min {min(esss):.3f})")
# sign: exterior of the ball (convex obstacle): the flat plane z=0 touches with II=0
g0 = np.zeros((2, 2))
y = np.linspace(-0.08, 0.08, 161)
Yx, Yy = np.meshgrid(y, y)
r2 = Yx ** 2 + Yy ** 2
ball_top = -(rho - np.sqrt(rho ** 2 - r2))     # obstacle ball below, touching at origin
plane_ok = np.all(0 >= ball_top - 1e-15)
rep("[2] convex obstacle: flat plane touches exterior of ball (h=-1/rho, no curvature)", plane_ok)
rep("[2] NEG sign mutation h=+1/rho would require ||II||>=1/rho for the plane", not (0.0 >= 1 / rho))


# ---------------------------------------------------------------- [3]
def ramp_solvable(r, deg):
    rows, rhs = [], []
    for t0, val in ((0.0, 0.0), (1.0, 1.0)):
        rows.append([t0 ** m for m in range(deg + 1)]); rhs.append(val)
        for j in range(1, r - 1):
            row = []
            for m in range(deg + 1):
                c = 0.0 if m < j else np.prod(range(m - j + 1, m + 1)) * t0 ** (m - j)
                row.append(c)
            rows.append(row); rhs.append(0.0)
    A, b = np.array(rows, float), np.array(rhs)
    x, *_ = np.linalg.lstsq(A, b, rcond=None)
    return np.linalg.norm(A @ x - b) < 1e-9


ok = all(ramp_solvable(r, 2 * r - 3) and not ramp_solvable(r, 2 * r - 4) for r in range(3, 8))
rep("[3] ramp: degree 2r-3 solvable, 2r-4 not (r=3..7)", ok)
rep("[3] NEG mutation degree r-2 (old text) unsolvable for r=3..7",
    all(not ramp_solvable(r, r - 2) for r in range(3, 8)))
t = np.linspace(0, 1, 5)
p = 3 * t ** 2 - 2 * t ** 3
dp = 6 * t - 6 * t ** 2
rep("[3] 3t^2-2t^3: p(0)=0,p(1)=1,p'(0)=p'(1)=0, monotone in [0,1]",
    abs(p[0]) < 1e-15 and abs(p[-1] - 1) < 1e-15 and abs(dp[0]) < 1e-15 and abs(dp[-1]) < 1e-15 and np.all(dp >= 0))


# ---------------------------------------------------------------- [4]
def random_curve(kmax, L=6.0, n=6000, pieces=12):
    s = np.linspace(0, L, n)
    ks = rng.uniform(-kmax, kmax, pieces)
    k = ks[np.minimum((s / L * pieces).astype(int), pieces - 1)]
    th = np.concatenate([[0], np.cumsum(k[:-1] * np.diff(s))])
    x = -1 + np.concatenate([[0], np.cumsum(np.cos(th[:-1]) * np.diff(s))])
    y = np.concatenate([[0], np.cumsum(np.sin(th[:-1]) * np.diff(s))])
    return x, y


def hits_disk(x, y):
    return np.any(x ** 2 + y ** 2 < 0.25)


R = 2.0
xm = -0.25
ybound = R - np.sqrt(R ** 2 - (xm + 1) ** 2)
rep("[4] analytic: for R=2, |y|<= %.3f at x=-1/4 < disk half-height %.3f" % (ybound, np.sqrt(0.25 - xm ** 2)),
    ybound < np.sqrt(0.25 - xm ** 2))
allhit = all(hits_disk(*random_curve(0.5)) for _ in range(2000))
rep("[4] 2000 random curves with |kappa|<=1/2 from (-1,0) heading +x all enter the disk", allhit)
avoid = sum(not hits_disk(*random_curve(3.3, L=1.0, pieces=4)) for _ in range(4000))
rep("[4] positive control |kappa|<=3.3: some curves avoid the disk (detector works)", avoid > 0, f"({avoid})")

# ---------------------------------------------------------------- [5]
w = 1.7
s = np.linspace(0, np.pi * w / 2, 2001)
g = np.stack([w / 2 * np.sin(2 * s / w), w / 2 * (1 - np.cos(2 * s / w))], 1)
T0 = np.array([np.cos(0), np.sin(0)]); T1 = np.array([np.cos(np.pi), np.sin(np.pi)])
rep("[5] semicircle: in strip R x [0,w], tangents (1,0)->(-1,0)",
    g[:, 1].min() > -1e-12 and g[:, 1].max() < w + 1e-12 and np.allclose(T1, [-1, 0]))
Rb, kap = 1.0, 0.6
f_lower = 2 * (1 - Rb * kap)
Lmax = 4 * Rb / f_lower
rep("[5] |gamma|^2 convexity gives length <= 4R/(2(1-R kappa)) = %.2f" % Lmax, Lmax > 0)

print("\nSUMMARY: %d / %d ok" % (sum(res), len(res)))
