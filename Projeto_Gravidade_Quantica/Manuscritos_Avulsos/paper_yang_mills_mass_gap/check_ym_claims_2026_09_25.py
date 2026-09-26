"""Independent checks of quick claims in paper_yang_mills_mass_gap.tex (2026-09-25).

Each check compares a formula of the manuscript with an independent oracle
(quadrature, finite differences, closed forms from the literature, symbolic
algebra) and, where meaningful, includes a negative control: a mutated
formula that must fail.  Run:  python check_ym_claims_2026_09_25.py
Exit status is 0 only if every check behaves as documented.
"""
import sys
import numpy as np
import sympy as sp
from scipy import integrate, special, linalg, optimize

RESULTS = []


def record(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"[{'OK ' if ok else 'FAIL'}] {name}: {detail}")


rng = np.random.default_rng(20260925)

# ---------------------------------------------------------------------------
# 1. beta-function coefficients (standard: b0 = 11N/3/(16 pi^2), b1 = 34N^2/3/(16 pi^2)^2)
# ---------------------------------------------------------------------------
N = sp.symbols("N", positive=True)
b0_paper = 11 * N / (48 * sp.pi**2)
b1_paper = 34 * N**2 / (3 * (16 * sp.pi**2) ** 2)
b0_std = sp.Rational(11, 3) * N / (16 * sp.pi**2)
b1_std = sp.Rational(34, 3) * N**2 / (16 * sp.pi**2) ** 2
record("beta0, beta1 match standard values",
       sp.simplify(b0_paper - b0_std) == 0 and sp.simplify(b1_paper - b1_std) == 0)

# two-loop Lambda is RG invariant to the stated order
g, mu = sp.symbols("g mu", positive=True)
b0, b1 = sp.symbols("b0 b1", positive=True)
lnLam = sp.log(mu) - b1 / (2 * b0**2) * sp.log(b0 * g**2) - 1 / (2 * b0 * g**2)
beta = -b0 * g**3 - b1 * g**5
dlnLam = sp.simplify(sp.diff(lnLam, mu) * mu + sp.diff(lnLam, g) * beta)
ser = sp.series(dlnLam, g, 0, 4).removeO()
record("two-loop Lambda: d ln Lambda / d ln mu = O(g^4) (three-loop order)",
       sp.simplify(ser) == 0, f"d lnLambda/d ln mu = {sp.simplify(dlnLam)}")
# negative control: wrong sign of the two-loop exponent leaves an O(g^2) residue
lnLam_bad = sp.log(mu) + b1 / (2 * b0**2) * sp.log(b0 * g**2) - 1 / (2 * b0 * g**2)
d_bad = sp.simplify(sp.diff(lnLam_bad, mu) * mu + sp.diff(lnLam_bad, g) * beta)
c2 = sp.simplify(sp.series(d_bad, g, 0, 4).removeO().coeff(g, 2))
record("  negative control: flipped two-loop exponent leaves O(g^2)", c2 != 0,
       f"g^2 coefficient = {c2}")

# ---------------------------------------------------------------------------
# 2. Mandelstam / Cayley-Hamilton identities hold identically as functions
# ---------------------------------------------------------------------------
def haar_su(n):
    z = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    q = q @ np.diag(np.diag(r) / np.abs(np.diag(r)))
    return q / np.linalg.det(q) ** (1.0 / n)


err = 0.0
err_bad = 0.0
for _ in range(200):
    U1, U2 = haar_su(2), haar_su(2)
    lhs = np.trace(U1) * np.trace(U2)
    err = max(err, abs(lhs - np.trace(U1 @ U2) - np.trace(U1 @ U2.conj().T)))
    err_bad = max(err_bad, abs(lhs - np.trace(U1 @ U2) + np.trace(U1 @ U2.conj().T)))
record("SU(2) Mandelstam tr A tr B = tr AB + tr AB^-1", err < 1e-12, f"max err {err:.1e}")
record("  negative control: sign flip fails", err_bad > 1e-2, f"max err {err_bad:.2f}")

err = 0.0
for _ in range(200):
    U = haar_su(3)
    e1 = np.trace(U)
    e2 = (np.trace(U) ** 2 - np.trace(U @ U)) / 2
    CH = U @ U @ U - e1 * U @ U + e2 * U - np.linalg.det(U) * np.eye(3)
    err = max(err, np.abs(CH).max())
record("SU(3) Cayley-Hamilton U^3 - e1 U^2 + e2 U - det U = 0", err < 1e-12,
       f"max err {err:.1e}; as a function of U it is the zero function, so the "
       "ideal it generates in L^2 is {0}")

# ---------------------------------------------------------------------------
# 3. -D^* D is negative semidefinite, so "M_A = -D_A^* D_A > 0" is impossible
# ---------------------------------------------------------------------------
D = rng.normal(size=(40, 30))
ev = np.linalg.eigvalsh(-D.T @ D)
record("-D^T D <= 0 for any D", ev.max() < 1e-10, f"max eigenvalue {ev.max():.2e}")

# ---------------------------------------------------------------------------
# 4. Operator AM-GM: T + c T^-1 >= 2 sqrt(c) needs the SAME operator T
# ---------------------------------------------------------------------------
c = 2.3
X = rng.normal(size=(20, 20))
T = X @ X.T + 0.05 * np.eye(20)
m_same = np.linalg.eigvalsh(T + c * np.linalg.inv(T)).min()
record("AM-GM with the same T holds", m_same >= 2 * np.sqrt(c) - 1e-9,
       f"min eig {m_same:.4f} >= {2*np.sqrt(c):.4f}")
# counterexample: two different positive operators
T1 = np.diag([0.01, 100.0])
S1 = np.diag([100.0, 0.01])  # T1 small where S1^-1 is small
m_diff = np.linalg.eigvalsh(T1 + c * np.linalg.inv(S1)).min()
record("  AM-GM fails for different operators T, S (counterexample)",
       m_diff < 2 * np.sqrt(c), f"min eig {m_diff:.4f} < {2*np.sqrt(c):.4f}")

# ---------------------------------------------------------------------------
# 5. Knife-edge remark: D(k) = k^2/(k^4+g^4) turns over at k = gamma
# ---------------------------------------------------------------------------
k, gam = sp.symbols("k gamma", positive=True)
Dk = k**2 / (k**4 + gam**4)
record("Gribov propagator maximum at k = gamma",
       sp.simplify(sp.diff(Dk, k).subs(k, gam)) == 0)

# ---------------------------------------------------------------------------
# 6. Cartan directions: ad(H) != 0, so the horizon term does not vanish there
# ---------------------------------------------------------------------------
H = np.diag([1j, -1j]) / 2
E = np.array([[0, 1], [-1, 0]], dtype=complex) / 2
adH_E = H @ E - E @ H
record("ad(H) acts non-trivially for H in the Cartan subalgebra of su(2)",
       np.abs(adH_E).max() > 0.1, f"|[H,E]| = {np.abs(adH_E).max():.2f}")

# ---------------------------------------------------------------------------
# 7. Gap-equation integral: int d^4k/(2pi)^4 1/(k^4+l^4) up to Lambda (log divergent)
# ---------------------------------------------------------------------------
lam, Lam = 1.0, 50.0
quad = integrate.quad(lambda q: q**3 / (q**4 + lam**4), 0, Lam, limit=200)[0] * 2 * np.pi**2 / (2 * np.pi) ** 4
closed = np.log((Lam**4 + lam**4) / lam**4) / (32 * np.pi**2)
record("gap integral = ln(1+Lambda^4/lambda^4)/(32 pi^2) (UV log divergent)",
       abs(quad - closed) < 1e-10, f"quad {quad:.8f} closed {closed:.8f}")

# ---------------------------------------------------------------------------
# 8. Horizon along A = a cos(2 pi x1/L) T^1 dx2 for SU(2) on T^3_L
#    ghost sector e^{i p x2}: -u'' + p^2 u - s g p a cos(k x) u, k = 2 pi/L
#    oracle A: Mathieu characteristic value; oracle B: finite differences
# ---------------------------------------------------------------------------
gcoup = 1.0


def lam_min_fd(a, L, n, M=400):
    x = np.arange(M) * L / M
    h = L / M
    p = 2 * np.pi * n / L
    main = 2 / h**2 + p**2 - gcoup * p * a * np.cos(2 * np.pi * x / L)
    Hm = np.diag(main) - np.diag(np.ones(M - 1), 1) / h**2 - np.diag(np.ones(M - 1), -1) / h**2
    Hm[0, -1] = Hm[-1, 0] = -1 / h**2
    return np.linalg.eigvalsh(Hm)[0]


def a_crit_mathieu(L, nmax=6):
    best = np.inf
    for n in range(1, nmax + 1):
        qn = optimize.brentq(lambda q: special.mathieu_a(0, q) + 4 * n**2, 1e-6, 500)
        best = min(best, qn * np.pi / (gcoup * n * L))
    return best


def a_crit_fd(L, nmax=3):
    best = np.inf
    for n in range(1, nmax + 1):
        hi = 1.0
        while lam_min_fd(hi, L, n) > 0:
            hi *= 2
        best = min(best, optimize.brentq(lambda a: lam_min_fd(a, L, n), 0, hi, xtol=1e-10))
    return best


Ls = [1.0, 2.0, 4.0, 8.0]
am = np.array([a_crit_mathieu(L) for L in Ls])
af = np.array([a_crit_fd(L) for L in Ls])
record("critical amplitude: Mathieu oracle vs finite differences",
       np.max(np.abs(am - af) / am) < 2e-3, f"rel diff {np.max(np.abs(am-af)/am):.1e}")
record("critical amplitude scales as 1/(gL)", np.ptp(am * np.array(Ls)) < 1e-9,
       f"a_crit*g*L = {am[0]*Ls[0]:.4f} (paper: pi/sqrt(N) = {np.pi/np.sqrt(2):.4f} for N=2)")
norms = am * np.array(Ls) ** 1.5 / np.sqrt(2)
slope = np.polyfit(np.log(Ls), np.log(norms), 1)[0]
record("L^2(T^3) distance to horizon along this ray grows like L^{1/2}",
       abs(slope - 0.5) < 1e-6, f"log-log slope {slope:.6f}")
# small-amplitude behaviour is quadratic, not linear as in the paper
L0, a_small = 2.0, 0.05
p0 = 2 * np.pi / L0
shift = lam_min_fd(a_small, L0, 1) - p0**2
paper_shift = -gcoup * np.sqrt(2) * a_small * np.pi / L0
quad_pred = -(gcoup * p0 * a_small) ** 2 / (2 * (2 * np.pi / L0) ** 2)
record("eigenvalue shift is second order in a (paper: first order)",
       abs(shift - quad_pred) / abs(quad_pred) < 2e-2 and abs(shift) < 0.05 * abs(paper_shift),
       f"shift {shift:.2e}, 2nd-order prediction {quad_pred:.2e}, paper's linear term {paper_shift:.2e}")

# ---------------------------------------------------------------------------
# 9. Dimensions (mass exponents, hbar=c=1, 4D fields with [A]=1)
# ---------------------------------------------------------------------------
dim_A = 1
dim_L2_sigma = 2 * dim_A - 3          # int d^3x A^2
dim_reach = dim_L2_sigma / 2          # ||A||_{L^2(Sigma)}
dim_kappa = -dim_reach
dim_sigma_formula = 2 * dim_kappa     # (pi/2) kappa^2
record("paper's reach = ||A||_{L^2(Sigma)} has mass dimension -1/2, not -1",
       dim_reach == -0.5, f"[reach] = {dim_reach}")
record("then sigma = (pi/2) kappa*^2 has dimension 1, but a string tension has dimension 2",
       dim_sigma_formula != 2, f"[sigma formula] = {dim_sigma_formula}")
# paper's own intermediate: ||A||^2 = pi^2 L/(2 g^2 N) with L = 2/Lambda
Lq, gq, Nq, Lamq = sp.symbols("L g N Lambda", positive=True)
expr = (sp.pi**2 * Lq / (2 * gq**2 * Nq)).subs(Lq, 2 / Lamq)
record("paper's ||A||^2 with L = 2/Lambda is pi^2/(g^2 N Lambda), not pi^2/(g^2 N Lambda^2)",
       sp.simplify(expr - sp.pi**2 / (gq**2 * Nq * Lamq)) == 0, f"= {expr}")

# ---------------------------------------------------------------------------
# 10. Flux tube: int_0^inf x K0(x)^2 dx = 1/2, energy per length pi E0^2/(2 kappa^2)
# ---------------------------------------------------------------------------
I = integrate.quad(lambda x: x * special.k0(x) ** 2, 0, np.inf, limit=400)[0]
record("int_0^inf x K0(x)^2 dx = 1/2", abs(I - 0.5) < 1e-8, f"{I:.10f}")
kap, E0 = 1.7, 0.9
tension = integrate.quad(lambda r: 2 * np.pi * r * 0.5 * (E0 * special.k0(kap * r)) ** 2, 0, np.inf, limit=400)[0]
record("energy per length = pi E0^2/(2 kappa^2)", abs(tension - np.pi * E0**2 / (2 * kap**2)) < 1e-8)
flux = integrate.quad(lambda r: 2 * np.pi * r * special.k0(kap * r), 0, np.inf)[0]
record("flux of K0 profile = 2 pi/kappa^2 -> with flux g: sigma = g^2 kappa^2/(8 pi)",
       abs(flux - 2 * np.pi / kap**2) < 1e-8,
       "E0 is fixed by the flux normalization, not by E0 = kappa^2")

# ---------------------------------------------------------------------------
# 11. Ground-state representation: gap of H is LINEAR in the Dirichlet-form gap
#     H = -1/2 d^2 + V; psi0^-1 (H-E0) psi0 = 1/2 (-d^2 + 2W' d), W = -ln psi0
# ---------------------------------------------------------------------------
def fd_H(V, x):
    h = x[1] - x[0]
    M = len(x)
    return np.diag(1 / h**2 + V(x)) - np.diag(np.ones(M - 1), 1) / (2 * h**2) - np.diag(np.ones(M - 1), -1) / (2 * h**2)


x = np.linspace(-8, 8, 1601)
h = x[1] - x[0]
for label, V in [("harmonic w=3", lambda y: 0.5 * 9 * y**2), ("anharmonic", lambda y: 0.25 * y**4 + 0.5 * y**2)]:
    ev, evec = linalg.eigh(fd_H(V, x))
    gap = ev[1] - ev[0]
    psi0 = np.abs(evec[:, 0])
    # independent: weighted Dirichlet form int |f'|^2 psi0^2 vs int f^2 psi0^2 on midpoints
    wmid = 0.5 * (psi0[1:] ** 2 + psi0[:-1] ** 2)
    Dm = (np.eye(len(x))[1:] - np.eye(len(x))[:-1]) / h
    A = Dm.T @ np.diag(wmid) @ Dm * h
    B = np.diag(psi0**2) * h + 1e-300 * np.eye(len(x))
    mask = psi0**2 > 1e-14 * psi0.max() ** 2
    lamW = linalg.eigh(A[np.ix_(mask, mask)], B[np.ix_(mask, mask)], eigvals_only=True)
    lam1 = lamW[1]
    record(f"ground-state rep ({label}): lambda1(L_W) = 2*gap (linear)",
           abs(lam1 - 2 * gap) / (2 * gap) < 1e-2, f"gap {gap:.4f}, lambda1 {lam1:.4f}")
    record(f"  negative control ({label}): gap = sqrt(lambda1) fails",
           abs(np.sqrt(lam1) - gap) / gap > 0.05, f"sqrt(lambda1) {np.sqrt(lam1):.4f}")

# ---------------------------------------------------------------------------
# 12. Fractional coupling: g~ = g_nl mu^{2 alpha} obeys d g~/d ln mu = +2 alpha g~
# ---------------------------------------------------------------------------
al, gnl, m = sp.symbols("alpha g_nl mu", positive=True)
gt = gnl * m ** (2 * al)
record("d g~/d ln mu = +2 alpha g~ (paper wrote -2 alpha)",
       sp.simplify(sp.diff(gt, m) * m - 2 * al * gt) == 0)
# dimension of the Riesz-kernel coupling: [F]=2, [d^4x d^4y]=-8, [|x|^{-(4+2a)}]=4+2a
record("[g_nl] = -2 alpha (so the kernel itself has dimension 4+2 alpha, not 2 alpha)",
       sp.simplify(-(2 + 2 - 8 + 4 + 2 * al) - (-2 * al)) == 0)

# ---------------------------------------------------------------------------
# 13. Floer claim: d|n> = |n-1> gives d^2 |n> = |n-2> != 0
# ---------------------------------------------------------------------------
n_s = 9
S = np.diag(np.ones(n_s - 1), -1)  # |n> -> |n-1> on a window
record("shift operator squared is non-zero, so d|n>=|n-1> contradicts d^2=0",
       np.abs(S @ S).max() == 1.0)
# tight-binding theta vacua on a ring of n_s sectors
Hb = -1.0 * (np.roll(np.eye(n_s), 1, axis=0) + np.roll(np.eye(n_s), -1, axis=0))
evs = np.sort(np.linalg.eigvalsh(Hb))
pred = np.sort(-2 * np.cos(2 * np.pi * np.arange(n_s) / n_s))
record("tight-binding E(theta) = E0 - 2 Delta cos(theta)", np.abs(evs - pred).max() < 1e-12)

# ---------------------------------------------------------------------------
# 14. Convexity of the Gribov region (M(A) affine in A) => Federer reach = infinity
# ---------------------------------------------------------------------------
M0 = np.diag(np.arange(1, 7, dtype=float))
Ms = [(lambda Y: (Y + Y.T) / 2)(rng.normal(size=(6, 6))) for _ in range(3)]


def inside(a):
    return np.linalg.eigvalsh(M0 + sum(ai * Mi for ai, Mi in zip(a, Ms))).min() > 0


pts = [a for a in rng.normal(scale=1.5, size=(4000, 3)) if inside(a)]
viol = 0
for _ in range(3000):
    i, j = rng.integers(len(pts), size=2)
    t = rng.random()
    viol += not inside(t * pts[i] + (1 - t) * pts[j])
record("{a : M0 + sum a_i M_i > 0} is convex (no midpoint violations)", viol == 0,
       f"{len(pts)} interior points, {viol} violations; convex closed sets have infinite reach")

# ---------------------------------------------------------------------------
# 15. Order of magnitude: m(0++)/Lambda_MSbar in SU(3)
#     r0 m(0++) = 4.21(11) [Morningstar-Peardon 1999]; r0 Lambda_MSbar = 0.602(48) [ALPHA 1999]
# ---------------------------------------------------------------------------
ratio = 4.21 / 0.602
record("m(0++)/Lambda_MSbar ~ 7 for SU(3)", 6.0 < ratio < 8.0, f"{ratio:.2f}")
c0 = (3 - 1) / (2 * 3)
C0_implied = 6.8**2 / (2 * (1 - c0))
record("fitting C_N = 6.8 fixes gamma_G/Lambda = sqrt(C0) (a fit, not a bound)", True,
       f"C0 = {C0_implied:.1f}, gamma_G = {np.sqrt(C0_implied):.2f} Lambda_MSbar")

bad = [r for r in RESULTS if not r[1]]
print(f"\n{len(RESULTS) - len(bad)}/{len(RESULTS)} checks behave as documented")
sys.exit(1 if bad else 0)
