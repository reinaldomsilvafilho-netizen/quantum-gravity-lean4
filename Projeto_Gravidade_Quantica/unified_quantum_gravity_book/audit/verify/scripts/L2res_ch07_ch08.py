"""L2 residual check (2026-09-25), chapters 7 and 8.

ch7: disk example, kappa* >= 1/2 via the envelope |y| <= 2 - sqrt(4-(x+1)^2).
ch8: Friedmann density bound, scope k <= 0, Lambda >= 0, failure for k = +1.

Every block has an independent oracle and mutations that must fail.
Run from the book folder: python audit/verify/scripts/L2res_ch07_ch08.py
"""
import numpy as np

FAILS = []


def check(name, cond):
    print(("OK   " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


# ---------------------------------------------------------------- ch7
# Oracle: integrate curves x' = cos phi, y' = sin phi, phi' = kappa(s) with
# |kappa| <= K from (-1,0), phi(0)=0, and record |y| where the curve first
# crosses x = -1/4 (and whether it ever enters the open disk |z| < 1/2).
rng = np.random.default_rng(20260925)


def integrate(kfun, K, ds=2e-3, smax=12.0):
    x, y, phi = -1.0, 0.0, 0.0
    ymax_at = None
    entered = False
    s = 0.0
    while s < smax:
        k = np.clip(kfun(s), -K, K)
        x_new = x + ds * np.cos(phi + 0.5 * ds * k)
        y_new = y + ds * np.sin(phi + 0.5 * ds * k)
        phi += ds * k
        if ymax_at is None and x < -0.25 <= x_new:
            t = (-0.25 - x) / (x_new - x)
            ymax_at = abs(y + t * (y_new - y))
        x, y = x_new, y_new
        if x * x + y * y < 0.25:
            entered = True
            if ymax_at is not None:
                break
        if x >= 1.0:
            break
        s += ds
    return ymax_at, entered, x


def env(u, R):
    return R - np.sqrt(R * R - u * u)


# (1) Extremal arc kappa = 1/2 achieves the envelope exactly.
ya, _, _ = integrate(lambda s: 0.5, 0.5)
check("ch7 extremal arc |kappa|=1/2 gives |y(-1/4)| = envelope 0.1459",
      abs(ya - env(0.75, 2.0)) < 2e-3 and abs(env(0.75, 2.0) - 0.14595) < 1e-4)
check("ch7 disk half-width at x=-1/4 is 0.4330", abs(np.sqrt(0.25 - 0.0625) - 0.43301) < 1e-4)

# (2) Random piecewise-constant curvature |kappa| <= 1/2: envelope never violated,
#     every curve enters the disk.
viol, not_entered = 0, 0
for trial in range(400):
    knots = rng.uniform(-0.5, 0.5, size=40)
    if trial % 4 == 0:
        knots = np.sign(knots) * 0.5  # bang-bang
    kf = (lambda kn: (lambda s: kn[min(int(s / 0.3), len(kn) - 1)]))(knots)
    ya, entered, _ = integrate(kf, 0.5)
    # envelope check along the way at x = -1/4
    if ya is not None and ya > env(0.75, 2.0) + 2e-3:
        viol += 1
    if not entered:
        not_entered += 1
check("ch7 400 random curves |kappa|<=1/2: envelope holds at x=-1/4", viol == 0)
check("ch7 400 random curves |kappa|<=1/2: all enter the disk", not_entered == 0)

# (3) Mutation of the envelope: small-angle parabola u^2/(2R) (too small) is
#     violated by the extremal arc -> must FAIL as a bound.
mut = 0.75 ** 2 / 4.0
ya, _, _ = integrate(lambda s: 0.5, 0.5)
check("ch7 mutation: parabola u^2/4 is NOT an upper bound (arc exceeds it)", ya > mut + 1e-3)
# Mutation 2: the claimed disk-free curve family with a larger curvature cap
# (negative control): a curve with |kappa| <= 4 that avoids the disk exists.


def detour(s):
    # left arc (R=1/4, 60 deg), straight at 60 deg, right arc (120 deg),
    # straight at -60 deg, left arc (60 deg): symmetric path over the disk.
    R, th = 0.25, np.pi / 3
    L = (0.5 * (2.0 - 2 * 2 * R * np.sin(th))) / np.cos(th)
    b = np.cumsum([R * th, L, 2 * R * th, L, R * th])
    ks = [4.0, 0.0, -4.0, 0.0, 4.0]
    for bi, k in zip(b, ks):
        if s < bi:
            return k
    return 0.0


ya, entered, xend = integrate(detour, 4.0, smax=4.0)
check("ch7 negative control: |kappa|<=4 detour avoids disk and reaches x=1", (not entered) and xend >= 0.99)

# (4) Sharpness remark (observation): the same argument with |kappa| <= 1 (R=1)
#     also works, so kappa* >= 1/2 is true but not sharp.
u = np.linspace(0.5, 0.999, 2000)
gap_R1 = np.sqrt(np.maximum(0.25 - (u - 1) ** 2, 0)) - env(u, 1.0)
print("     obs: with R=1 the envelope stays below the disk half-width at some x:",
      bool(np.any(gap_R1 > 0)), " max margin %.3f" % gap_R1.max())

# ---------------------------------------------------------------- ch8
hbar = 1.054571817e-34
G = 6.67430e-11
c = 299792458.0
lP2 = hbar * G / c ** 3
planck_E_density = c ** 7 / (hbar * G ** 2)
bound = 3 * c ** 4 / (8 * np.pi * G * lP2)
check("ch8 c^7/(hbar G^2) = 4.63e113 J/m^3", abs(planck_E_density / 4.63e113 - 1) < 2e-3)
check("ch8 3c^4/(8 pi G lP^2) = (3/8pi) c^7/(hbar G^2) = 5.5e112", abs(bound / (3 / (8 * np.pi) * planck_E_density) - 1) < 1e-12 and abs(bound / 5.53e112 - 1) < 5e-3)
check("ch8 mutation prefactor 1 instead of 3/8pi is rejected", abs(planck_E_density / 5.5e112 - 1) > 0.5)
# Dimensional check: [c^4/(G l^2)] = (m^4 s^-4)/(m^3 kg^-1 s^-2 m^2) = kg m^-1 s^-2 = J m^-3
dims = np.array([4, -4, 0]) - (np.array([3, -2, -1]) + np.array([2, 0, 0]))  # (m, s, kg)
check("ch8 dimension of c^4/(G lP^2) is J m^-3 = kg m^-1 s^-2", list(dims) == [-1, -2, 1])

# Scope: Friedmann H^2 = 8piG rho/3 - k c^2/a^2 + Lambda c^2/3.
# Oracle: sample rho, a, Lambda; with |H| <= c/lP check rho c^2 <= bound.
N = 200000
rho = 10 ** rng.uniform(80, 100, N)   # kg/m^3, around Planck density 5e96
a = 10 ** rng.uniform(-36, -30, N)    # m
Lam = 10 ** rng.uniform(60, 72, N)    # m^-2
for k, name, expect_ok in [(0, "k=0", True), (-1, "k=-1", True), (1, "k=+1", False)]:
    H2 = 8 * np.pi * G * rho / 3 - k * c ** 2 / a ** 2 + Lam * c ** 2 / 3
    ok = H2 >= 0
    allowed = ok & (H2 <= c ** 2 / lP2)
    violates = np.any(rho[allowed] * c ** 2 > bound * (1 + 1e-12))
    if expect_ok:
        check("ch8 scope %s, Lambda>=0: no allowed state violates the density bound" % name, not violates)
    else:
        check("ch8 mutation of scope to k=+1: violations exist (bound fails)", violates)
# Lambda < 0 also outside scope (not claimed): violations exist
H2 = 8 * np.pi * G * rho / 3 - Lam * c ** 2 / 3
allowed = (H2 >= 0) & (H2 <= c ** 2 / lP2)
print("     obs: Lambda<0, k=0 has violations:", bool(np.any(rho[allowed] * c ** 2 > bound)))

print("\nFAILURES:", FAILS if FAILS else "none")
raise SystemExit(1 if FAILS else 0)
