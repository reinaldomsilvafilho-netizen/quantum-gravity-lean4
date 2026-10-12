"""
F-02 independent numerical audit -- Chapter 9
(chap09_global_homotopy_covering_spaces_jordan_loops.tex)

Every claim: independent oracle + negative control. Read-only.
"""
import numpy as np

PASS, FAIL = [], []

def report(name, line, ok, detail):
    (PASS if ok else FAIL).append(name)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} (book line ~{line})")
    print(f"       {detail}")


def curvature_of_poly(gx, gy):
    """Independent curvature estimate for a planar polyline given as
    coordinate arrays, via centered finite differences -- never uses an
    analytic closed form."""
    xp = np.gradient(gx)
    yp = np.gradient(gy)
    xpp = np.gradient(xp)
    ypp = np.gradient(yp)
    speed = np.sqrt(xp ** 2 + yp ** 2)
    kappa = np.abs(xp * ypp - yp * xpp) / speed ** 3
    return kappa, speed


def min_width_bruteforce(gx, gy, n_dirs=720):
    """Independent width-in-some-direction computation via brute-force
    support function search over many directions (not assuming the curve
    is a circle)."""
    pts = np.stack([gx, gy], axis=1)
    widths = []
    for theta in np.linspace(0, np.pi, n_dirs, endpoint=False):
        d = np.array([np.cos(theta), np.sin(theta)])
        proj = pts @ d
        widths.append(proj.max() - proj.min())
    return min(widths)


# ---------------------------------------------------------------------------
# Claim 1 (line 155-167): confinement of closed sub-loops.
#   a closed C^{1,1} loop with |kappa| <= K has width >= 2/K in some
#   direction (hence diameter >= 2/K); sharp for the circle of radius 1/K.
# Oracle: an INDEPENDENT ellipse example (not the sharp circle case):
# build an ellipse with semi-axes chosen so that its max curvature equals
# a prescribed K (closed form for an ellipse's curvature extrema, a
# different computation from the book's angle/turning argument), then
# brute-force its minimal width over all directions and check it is >= 2/K.
# Negative control: the sharp circle example itself refutes any STRONGER
# claimed bound (e.g. width >= 4/K), since it attains width exactly 2/K.
# ---------------------------------------------------------------------------
def ellipse_max_curvature(a, b):
    # curvature of x=a cos t, y=b sin t is ab/(a^2 sin^2 t + b^2 cos^2 t)^{3/2}
    # max at t=0 or pi/2: kappa_max = a/b^2 if a>b (at the end of minor axis)
    return max(a / b ** 2, b / a ** 2)

ok1 = True
detail1 = []
for (a, b) in [(2.0, 1.0), (3.0, 1.5), (1.0, 0.4)]:
    t = np.linspace(0, 2 * np.pi, 4000, endpoint=False)
    gx, gy = a * np.cos(t), b * np.sin(t)
    kappa_numeric, _ = curvature_of_poly(gx, gy)
    K = kappa_numeric.max()  # independent numeric max curvature (finite differences)
    width = min_width_bruteforce(gx, gy)
    bound = 2 / K
    detail1.append((a, b, float(K), float(width), float(bound)))
    if width < bound - 1e-2:
        ok1 = False
report("Closed sub-loop confinement: width >= 2/K (independent ellipse example, "
       "brute-force support-function width + finite-difference curvature)",
       "155-167", ok1, f"(a, b, K_numeric, width, 2/K): {detail1}")

# Negative control: the sharp circle example (K=1/r, width=diam=2r=2/K exactly)
# refutes a strictly stronger universal bound width >= 4/K.
t = np.linspace(0, 2 * np.pi, 4000, endpoint=False)
r = 1.3
gx, gy = r * np.cos(t), r * np.sin(t)
K_circle = 1 / r
width_circle = min_width_bruteforce(gx, gy)
ok1_neg = width_circle < 4 / K_circle  # i.e. the stronger bound is violated
report("NEGATIVE CONTROL: stronger bound 'width >= 4/K' is violated by the sharp "
       "circle example (width = 2/K exactly there)", "155-167", ok1_neg,
       f"circle: K={K_circle:.4f}, width={width_circle:.4f}, 2/K={2/K_circle:.4f}, "
       f"4/K={4/K_circle:.4f} (width < 4/K as required)")


# ---------------------------------------------------------------------------
# Claim 2 (line 309-325): benchmark channel. With R0=1, H=1.62, the
# constructed w=1 path (semicircle of radius H centred at the origin,
# plus straight approach/exit segments) has peak curvature exactly 1/H,
# stays inside the strip |y|<=H, and avoids the obstacle disk of radius
# R0 (since H > R0).
# Oracle: explicit numerical construction of the path, curvature computed
# by independent finite-difference formula (not assumed to be 1/H), and
# distance-to-origin computed directly to check obstacle avoidance.
# Negative control: if R0 were increased past H (R0=1.8 > H=1.62), the
# same semicircular arc of radius H would NOT avoid the obstacle -- the
# construction's validity genuinely depends on H > R0.
# ---------------------------------------------------------------------------
R0, H = 1.0, 1.62

def benchmark_w1_path(H, n=4000):
    # straight segment approach along y=-H from x=-10 to x=0 is not needed
    # for curvature/obstacle checks; the essential arc is the semicircle
    # of radius H centered at the origin, from angle -pi/2 to +pi/2
    # (passing through (H,0)) connecting y=-H to y=+H.
    t = np.linspace(-np.pi / 2, np.pi / 2, n)
    gx, gy = H * np.cos(t), H * np.sin(t)
    return gx, gy

gx, gy = benchmark_w1_path(H)
kappa_numeric, _ = curvature_of_poly(gx, gy)
# finite-difference curvature is unreliable right at the array endpoints;
# use the interior
kappa_interior = kappa_numeric[5:-5]
dist_to_origin = np.sqrt(gx ** 2 + gy ** 2)

ok2 = (abs(kappa_interior.max() - 1 / H) < 1e-2 and abs(kappa_interior.min() - 1 / H) < 1e-2
       and np.all(dist_to_origin > R0 + 1e-9) and np.all(np.abs(gy) <= H + 1e-9))
report("Benchmark channel (R0=1, H=1.62): w=1 semicircular arc has curvature "
       "exactly 1/H everywhere and avoids the obstacle disk of radius R0",
       "309-325", ok2,
       f"kappa range on arc = [{kappa_interior.min():.5f}, {kappa_interior.max():.5f}] "
       f"vs 1/H = {1/H:.5f}; min distance to origin = {dist_to_origin.min():.4f} "
       f"(must exceed R0 = {R0})")

ok2_neg = True
R0_wrong = 1.8  # > H=1.62: construction should then fail to avoid the obstacle
gx2, gy2 = benchmark_w1_path(H)
dist2 = np.sqrt(gx2 ** 2 + gy2 ** 2)
# the semicircle has constant radius H < R0_wrong, so it lies ENTIRELY inside
# the (now larger) obstacle disk -- i.e. it fails to avoid it
if np.any(dist2 > R0_wrong):
    ok2_neg = False  # it should NOT avoid the bigger obstacle anywhere on the arc
report("NEGATIVE CONTROL: with R0=1.8 > H=1.62, the same semicircular arc "
       "(radius H) fails to avoid the obstacle (lies entirely inside it)",
       "309-325", ok2_neg,
       f"max distance to origin on arc = {dist2.max():.4f} < R0_wrong = {R0_wrong} "
       f"(arc entirely inside the enlarged obstacle, as required to fail)")


# ---------------------------------------------------------------------------
# Claim 3 (line 187-205): winding/total-curvature inequality
#   int |theta'| ds <= int |kappa| ds + pi,
# with the additive constant pi SHARP: a straight line passing at
# distance epsilon from c has kappa=0 and int|theta'| -> pi as length -> inf.
# Oracle: direct numerical construction of a straight line at distance
# epsilon from the origin, numerical unwrapped-angle integration of
# |theta'| via np.unwrap (independent of the analytic sign-function/Lipschitz
# argument in the book's proof), and comparison to the limit pi.
# Negative control: a tightened constant pi/2 instead of pi must fail
# (the computed value approaches pi, not pi/2).
# ---------------------------------------------------------------------------
def line_winding_integral(epsilon, half_length):
    t = np.linspace(-half_length, half_length, 400000)
    x, y = t, np.full_like(t, epsilon)
    theta = np.unwrap(np.arctan2(y, x))
    dtheta = np.diff(theta)
    return np.sum(np.abs(dtheta))

ok3 = True
detail3 = []
for eps in (0.05, 0.01, 0.002):
    val = line_winding_integral(eps, half_length=5000)
    detail3.append((eps, float(val)))
    if val > np.pi + 1e-2:  # must respect the proved upper bound (kappa=0 here)
        ok3 = False
    if abs(val - np.pi) > 0.05:  # must approach pi as epsilon/length -> extreme
        ok3 = False
report("Winding/curvature inequality sharpness: straight line at distance eps "
       "from c has int|theta'| -> pi (kappa=0, independent unwrap-based integration)",
       "187-205", ok3, f"(epsilon, int|theta'|): {detail3} (-> should -> pi = {np.pi:.4f})")

ok3_neg = True
for eps in (0.05, 0.01, 0.002):
    val = line_winding_integral(eps, half_length=5000)
    if val <= np.pi / 2 + 0.05:  # a tightened bound of pi/2 would require this
        ok3_neg = False
report("NEGATIVE CONTROL: a tightened additive constant pi/2 (instead of pi) "
       "is violated by the straight-line example", "187-205", ok3_neg,
       "computed int|theta'| approaches pi > pi/2 for all tested epsilon")


print()
print("=" * 70)
print(f"Chapter 9 summary: {len(PASS)} PASS, {len(FAIL)} FAIL")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("  -", f)
