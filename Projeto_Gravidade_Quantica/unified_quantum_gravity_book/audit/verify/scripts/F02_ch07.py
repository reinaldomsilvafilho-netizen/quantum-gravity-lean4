"""
F-02 independent numerical audit -- Chapter 7
(chap07_minimax_extrinsic_curvature_submanifolds.tex)

Every claim: independent oracle + negative control. Read-only.
"""
import numpy as np
import sympy as sp

PASS, FAIL = [], []

def report(name, line, ok, detail):
    (PASS if ok else FAIL).append(name)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} (book line ~{line})")
    print(f"       {detail}")


# ---------------------------------------------------------------------------
# Claim 1 (line 132-142): Fary-Milnor / Fenchel knotting curvature gap
#   kappa*_K(L) >= 4 pi / L   (knotted closed curves, Fary-Milnor)
#   kappa*_Imm(L) = 2 pi / L  (all closed curves, Fenchel, tight at circle)
# Oracle: explicit numerical curves, total curvature computed by a
# DIFFERENT method than citing the theorems -- direct numerical
# integration of |kappa(s)| ds via the general space-curve curvature
# formula kappa = |g' x g''| / |g'|^3 (finite differences on a fine
# parameter grid, independent of any analytic argument).
# Negative control: an UNKNOTTED closed curve with total curvature < 4 pi
# must exist (showing 4pi is not a bound for ALL closed curves, only
# knotted ones) -- the plain circle, total curvature exactly 2 pi.
# ---------------------------------------------------------------------------
def total_curvature(gamma_func, t0, t1, N=20000):
    t = np.linspace(t0, t1, N, endpoint=False)
    dt = (t1 - t0) / N
    g = gamma_func(t)
    gp = np.gradient(g, dt, axis=0, edge_order=2)
    gpp = np.gradient(gp, dt, axis=0, edge_order=2)
    cross = np.cross(gp, gpp)
    speed = np.linalg.norm(gp, axis=1)
    kappa = np.linalg.norm(cross, axis=1) / speed ** 3
    ds = speed * dt
    return np.sum(kappa * ds)

def trefoil(t):
    x = np.sin(t) + 2 * np.sin(2 * t)
    y = np.cos(t) - 2 * np.cos(2 * t)
    z = -np.sin(3 * t)
    return np.stack([x, y, z], axis=1)

def circle(t):
    x = np.cos(t)
    y = np.sin(t)
    z = np.zeros_like(t)
    return np.stack([x, y, z], axis=1)

tc_trefoil = total_curvature(trefoil, 0, 2 * np.pi)
tc_circle = total_curvature(circle, 0, 2 * np.pi)

ok1 = (tc_trefoil > 4 * np.pi) and abs(tc_circle - 2 * np.pi) < 1e-3
report("Fary-Milnor: total curvature of a trefoil (knotted) curve exceeds 4*pi; "
       "Fenchel: round circle total curvature = 2*pi exactly",
       "132-142", ok1,
       f"total curvature trefoil = {tc_trefoil:.4f} (must be > 4pi={4*np.pi:.4f}); "
       f"total curvature circle = {tc_circle:.6f} (must equal 2pi={2*np.pi:.6f})")

# Negative control: the round circle is UNKNOTTED and has total curvature
# 2*pi < 4*pi -- i.e. 4*pi is NOT a universal bound for all closed curves,
# only for knotted ones. If we mistakenly claimed "every closed curve has
# total curvature >= 4*pi" that mutated claim must fail on the circle.
ok1_neg = tc_circle < 4 * np.pi
report("NEGATIVE CONTROL: mutated claim 'every closed curve has total curvature "
       ">= 4pi' fails on the (unknotted) circle", "132-142", ok1_neg,
       f"circle total curvature = {tc_circle:.4f} < 4pi = {4*np.pi:.4f}")


# ---------------------------------------------------------------------------
# Claim 2 (line 432-435): planar U-turn semicircle of radius w/2 has
# constant curvature kappa = 2/w.
# Oracle: sympy symbolic curvature formula for a general planar curve,
# kappa = (x'y'' - y'x'') / (x'^2+y'^2)^(3/2), applied directly to the
# book's own parametrization but evaluated by a completely generic,
# independent symbolic pipeline (not assuming "it's a circle of radius
# w/2").
# Negative control: wrong constant 1/w must disagree.
# ---------------------------------------------------------------------------
s, w = sp.symbols('s w', positive=True)
x_uturn = (w / 2) * sp.sin(2 * s / w)
y_uturn = (w / 2) * (1 - sp.cos(2 * s / w))
xp, yp = sp.diff(x_uturn, s), sp.diff(y_uturn, s)
xpp, ypp = sp.diff(xp, s), sp.diff(yp, s)
kappa_uturn = sp.simplify((xp * ypp - yp * xpp) / (xp ** 2 + yp ** 2) ** sp.Rational(3, 2))

ok2 = sp.simplify(kappa_uturn - 2 / w) == 0
report("Planar U-turn semicircle: kappa = 2/w (generic symbolic curvature formula)",
       "432-435", ok2, f"sympy curvature formula simplifies to: {kappa_uturn}")

ok2_neg = sp.simplify(kappa_uturn - 1 / w) != 0
report("NEGATIVE CONTROL: wrong constant kappa=1/w disagrees with symbolic computation",
       "432-435", ok2_neg, f"kappa - 1/w = {sp.simplify(kappa_uturn - 1/w)} (nonzero => disagrees, as required)")


# ---------------------------------------------------------------------------
# Claim 3 (line 443-446): circular helix curvature kappa = a/(a^2+b^2),
# torsion tau = b/(a^2+b^2).
# Oracle: generic symbolic space-curve curvature/torsion formulas
#   kappa = |g' x g''| / |g'|^3,
#   tau   = (g' x g'') . g''' / |g' x g''|^2,
# applied with sympy to the explicit helix parametrization (independent
# of the book's own simplification).
# Negative control: wrong formula kappa = a/(a+b)^2 must disagree.
# ---------------------------------------------------------------------------
a_s, b_s, c_s, t_s = sp.symbols('a b c t', positive=True)
c_val = sp.sqrt(a_s ** 2 + b_s ** 2)
gx = a_s * sp.cos(t_s / c_val)
gy = a_s * sp.sin(t_s / c_val)
gz = b_s * t_s / c_val
g_vec = sp.Matrix([gx, gy, gz])
gp_vec = sp.diff(g_vec, t_s)
gpp_vec = sp.diff(gp_vec, t_s)
gppp_vec = sp.diff(gpp_vec, t_s)
cross_vec = gp_vec.cross(gpp_vec)
kappa_helix = sp.simplify(cross_vec.norm() / gp_vec.norm() ** 3)
tau_helix = sp.simplify((cross_vec.dot(gppp_vec)) / cross_vec.dot(cross_vec))

kappa_expected = a_s / (a_s ** 2 + b_s ** 2)
tau_expected = b_s / (a_s ** 2 + b_s ** 2)

ok3 = (sp.simplify(kappa_helix - kappa_expected) == 0) and (sp.simplify(tau_helix - tau_expected) == 0)
report("Circular helix: kappa=a/(a^2+b^2), tau=b/(a^2+b^2) (generic Frenet formulas)",
       "443-446", ok3, f"kappa computed = {kappa_helix}; tau computed = {tau_helix}")

kappa_wrong = a_s / (a_s + b_s) ** 2
ok3_neg = sp.simplify(kappa_helix - kappa_wrong) != 0
report("NEGATIVE CONTROL: wrong formula kappa=a/(a+b)^2 disagrees",
       "443-446", ok3_neg, f"kappa - a/(a+b)^2 = {sp.simplify(kappa_helix - kappa_wrong)} (nonzero => disagrees)")


# ---------------------------------------------------------------------------
# Claim 4 (line 454-459): Clifford torus shape operator norm ||II||=sqrt(2)/R.
# Oracle: NUMERICAL second fundamental form computed from finite
# differences of the explicit embedding X(u,v) in R^4 -- independent of
# the book's hand-derived shape-operator matrix: compute the embedding's
# first and second partial derivatives numerically, project onto a chosen
# unit normal direction, and read off the principal curvatures via
# Weingarten (numerically diagonalized), for several normal angles phi.
# Negative control: wrong value 1/R must disagree.
# ---------------------------------------------------------------------------
def clifford_torus_shape_operator_norm(R=1.0, h=1e-4):
    def X(u, v):
        c = R / np.sqrt(2)
        return np.array([c * np.cos(u), c * np.sin(u), c * np.cos(v), c * np.sin(v)])

    def partial(f, u, v, h, axis):
        if axis == 0:
            return (f(u + h, v) - f(u - h, v)) / (2 * h)
        else:
            return (f(u, v + h) - f(u, v - h)) / (2 * h)

    u0, v0 = 0.37, 1.21  # arbitrary point (should not matter: flat torus)
    Xu = partial(X, u0, v0, h, 0)
    Xv = partial(X, u0, v0, h, 1)
    Xuu = (X(u0 + h, v0) - 2 * X(u0, v0) + X(u0 - h, v0)) / h ** 2
    Xvv = (X(u0, v0 + h) - 2 * X(u0, v0) + X(u0, v0 - h)) / h ** 2
    Xuv = (X(u0 + h, v0 + h) - X(u0 + h, v0 - h) - X(u0 - h, v0 + h) + X(u0 - h, v0 - h)) / (4 * h ** 2)

    # metric
    E = Xu @ Xu; F = Xu @ Xv; G = Xv @ Xv
    g = np.array([[E, F], [F, G]])

    # normal space basis: orthogonal complement of {Xu, Xv} in R^4
    tangent = np.stack([Xu, Xv], axis=1)  # 4x2
    Q, _ = np.linalg.qr(np.concatenate([tangent, np.eye(4)], axis=1))
    # take the last two orthonormal columns as a normal frame
    normal_basis = Q[:, 2:4]

    max_op_norm = 0.0
    for phi in np.linspace(0, 2 * np.pi, 37):
        nu = np.cos(phi) * normal_basis[:, 0] + np.sin(phi) * normal_basis[:, 1]
        L = Xuu @ nu; M = Xuv @ nu; N = Xvv @ nu
        II = np.array([[L, M], [M, N]])
        ginv = np.linalg.inv(g)
        shape_op = ginv @ II
        eigs = np.linalg.eigvals(shape_op)
        max_op_norm = max(max_op_norm, np.max(np.abs(eigs)))
    return max_op_norm

ok4 = True
detail4 = []
for R in (1.0, 2.5, 5.0):
    val = clifford_torus_shape_operator_norm(R)
    expected = np.sqrt(2) / R
    rel = abs(val - expected) / expected
    detail4.append((R, float(val), float(expected), float(rel)))
    if rel > 1e-2:
        ok4 = False
report("Clifford torus ||II||_op = sqrt(2)/R (numerical finite-difference second fundamental form)",
       "454-459", ok4, f"(R, numeric, formula, rel.err): {detail4}")

ok4_neg = True
for R in (1.0, 2.5, 5.0):
    val = clifford_torus_shape_operator_norm(R)
    wrong = 1.0 / R
    if abs(val - wrong) / wrong < 1e-2:
        ok4_neg = False
report("NEGATIVE CONTROL: wrong value 1/R (missing sqrt2) disagrees with numeric computation",
       "454-459", ok4_neg, "checked R=1,2.5,5; mutated formula disagrees")


# ---------------------------------------------------------------------------
# Claim 5 (line 459, table line 477): hypercylinder S^2(R) x R has
# ||II||_op = 1/R.
# Oracle: numerical second fundamental form of the explicit embedding
# (R sin(theta)cos(phi), R sin(theta) sin(phi), R cos(theta), z) in R^4,
# via finite differences, independent of the book's shape-operator claim.
# Negative control: wrong value 2/R must disagree.
# ---------------------------------------------------------------------------
def hypercylinder_shape_operator_norm(R=1.0, h=1e-4):
    def X(theta, phi, z):
        return np.array([R * np.sin(theta) * np.cos(phi), R * np.sin(theta) * np.sin(phi),
                          R * np.cos(theta), z])
    th0, ph0, z0 = 1.1, 0.6, 0.3
    Xth = (X(th0 + h, ph0, z0) - X(th0 - h, ph0, z0)) / (2 * h)
    Xph = (X(th0, ph0 + h, z0) - X(th0, ph0 - h, z0)) / (2 * h)
    Xz = (X(th0, ph0, z0 + h) - X(th0, ph0, z0 - h)) / (2 * h)
    tangent = np.stack([Xth, Xph, Xz], axis=1)
    Q, _ = np.linalg.qr(np.concatenate([tangent, np.eye(4)], axis=1))
    nu = Q[:, 3]
    # fix sign so nu points outward radially in the (x,y,z)-S^2 part
    if nu[:3] @ np.array([np.sin(th0) * np.cos(ph0), np.sin(th0) * np.sin(ph0), np.cos(th0)]) < 0:
        nu = -nu

    def XX(theta, phi, z):
        return X(theta, phi, z)

    Xthth = (XX(th0 + h, ph0, z0) - 2 * XX(th0, ph0, z0) + XX(th0 - h, ph0, z0)) / h ** 2
    Xphph = (XX(th0, ph0 + h, z0) - 2 * XX(th0, ph0, z0) + XX(th0, ph0 - h, z0)) / h ** 2
    Xzz = (XX(th0, ph0, z0 + h) - 2 * XX(th0, ph0, z0) + XX(th0, ph0, z0 - h)) / h ** 2
    Xthph = (XX(th0 + h, ph0 + h, z0) - XX(th0 + h, ph0 - h, z0) - XX(th0 - h, ph0 + h, z0) + XX(th0 - h, ph0 - h, z0)) / (4 * h ** 2)
    Xthz = (XX(th0 + h, ph0, z0 + h) - XX(th0 + h, ph0, z0 - h) - XX(th0 - h, ph0, z0 + h) + XX(th0 - h, ph0, z0 - h)) / (4 * h ** 2)
    Xphz = (XX(th0, ph0 + h, z0 + h) - XX(th0, ph0 + h, z0 - h) - XX(th0, ph0 - h, z0 + h) + XX(th0, ph0 - h, z0 - h)) / (4 * h ** 2)

    g = np.array([[Xth @ Xth, Xth @ Xph, Xth @ Xz],
                  [Xth @ Xph, Xph @ Xph, Xph @ Xz],
                  [Xth @ Xz, Xph @ Xz, Xz @ Xz]])
    II = np.array([[Xthth @ nu, Xthph @ nu, Xthz @ nu],
                   [Xthph @ nu, Xphph @ nu, Xphz @ nu],
                   [Xthz @ nu, Xphz @ nu, Xzz @ nu]])
    shape_op = np.linalg.inv(g) @ II
    eigs = np.linalg.eigvals(shape_op)
    return np.max(np.abs(eigs))

ok5 = True
detail5 = []
for R in (1.0, 2.0, 4.0):
    val = hypercylinder_shape_operator_norm(R)
    expected = 1.0 / R
    rel = abs(val - expected) / expected
    detail5.append((R, float(val), float(expected), float(rel)))
    if rel > 1e-2:
        ok5 = False
report("Hypercylinder S^2(R) x R: ||II||_op = 1/R (numerical second fundamental form)",
       "459,477", ok5, f"(R, numeric, formula, rel.err): {detail5}")

ok5_neg = True
for R in (1.0, 2.0, 4.0):
    val = hypercylinder_shape_operator_norm(R)
    wrong = 2.0 / R
    if abs(val - wrong) / wrong < 1e-2:
        ok5_neg = False
report("NEGATIVE CONTROL: wrong value 2/R disagrees with numeric computation",
       "459,477", ok5_neg, "checked R=1,2,4; mutated formula disagrees")


print()
print("=" * 70)
print(f"Chapter 7 summary: {len(PASS)} PASS, {len(FAIL)} FAIL")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("  -", f)
