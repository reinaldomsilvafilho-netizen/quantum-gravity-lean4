"""Layer-2 checks of the v3 replacement statements (independent of corrector_*.py).

1. Thm 3.6: exact spectra (sympy), H1 persistence by boundary-matrix reduction
   over GF(2) on the filtered cubical complex (not union-find / Alexander duality,
   not rasterisation), grid refinement r = 1, 2, 3, entropies from lifetimes.
2. Prop 6.4: Pauli traces by explicit matrix products; (i/4) sum sgn tau^gamma by
   quadrature vs the degree computed by signed preimage counting (independent).
3. Lemma 7.2 / Thm 7.3: QFI factor 2 vs Bures fidelity expansion; rank examples.
4. Prop 4.5: c_* by adaptive quadrature on a quarter cell (paper: midpoint grid).
5. Thm 2.3(c): exact 1D W2 (quantiles) speed vs bound; sharpness of 1/pi.
Each block has a negative control. Fixed seed. Exit code = number of failures.
"""
import sys, itertools, math
import numpy as np
import sympy as sp
from scipy import integrate, linalg

rng = np.random.default_rng(20261006)
fails = 0
def check(name, ok):
    global fails
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        fails += 1

# ---------------------------------------------------------------- 1. persistence
print("== Thm 3.6 ==")
def mat(n, entries, default):
    M = sp.Matrix(n, n, lambda i, j: default)
    for (i, j), v in entries.items():
        M[i, j] = v
    return M
def perm(n, a, b):
    P = sp.eye(n); P.row_swap(a, b); return P
B = mat(3, {(1, 1): 0}, 2); P = perm(3, 0, 1); A = P * B * P.T
Bp = mat(5, {(1, 1): 0, (3, 3): 1}, 3); Pp = perm(5, 0, 1); Ap = Pp * Bp * Pp.T
J = sp.Matrix(5, 5, lambda i, j: 1 if i + j == 4 else 0); C = J * Bp * J.T
lam = sp.symbols("lam")
evB = B.eigenvals()
print("eig B", evB, " eig A", A.eigenvals())
check("3x3 spectrum = {2+2sqrt3, 2-2sqrt3, 0}",
      set(sp.nsimplify(e) for e in evB) == {2 + 2*sp.sqrt(3), 2 - 2*sp.sqrt(3), 0}
      and B.charpoly(lam) == A.charpoly(lam) and B.is_symmetric() and A.is_symmetric())
print("charpoly B'", sp.factor(Bp.charpoly(lam).as_expr()))
check("5x5 isospectral, symmetric", Bp.charpoly(lam) == Ap.charpoly(lam) and Ap.is_symmetric()
      and Ap[0, 0] == 0 and Ap[3, 3] == 1 and Ap[1, 1] == 3)
check("C = J B' J^T isospectral and != B'", C.charpoly(lam) == Bp.charpoly(lam) and C != Bp)

def h1_diagram(Mv, r=1):
    """Super-level H1 persistence of the closed-cell step realization, refined r times."""
    M = np.array(Mv, dtype=float); n = M.shape[0]; m = n * r
    val = np.kron(M, np.ones((r, r)))          # value of square (i,j), i along x1
    cells = []                                  # (filtration key, dim, id)
    # vertices (a,b) a,b in 0..m ; edges; squares
    def sq_vals(i0, j0, i1, j1):
        vs = [val[i, j] for i in range(i0, i1) for j in range(j0, j1) if 0 <= i < m and 0 <= j < m]
        return max(vs)
    idx = {}
    for a in range(m + 1):
        for b in range(m + 1):
            idx[("v", a, b)] = sq_vals(a - 1, b - 1, a + 1, b + 1)
    for a in range(m):
        for b in range(m + 1):
            idx[("ex", a, b)] = sq_vals(a, b - 1, a + 1, b + 1)     # edge [a,a+1]x{b}
    for a in range(m + 1):
        for b in range(m):
            idx[("ey", a, b)] = sq_vals(a - 1, b, a + 1, b + 1)     # edge {a}x[b,b+1]
    for a in range(m):
        for b in range(m):
            idx[("s", a, b)] = val[a, b]
    dimof = {"v": 0, "ex": 1, "ey": 1, "s": 2}
    order = sorted(idx, key=lambda c: (-idx[c], dimof[c[0]], c))
    pos = {c: k for k, c in enumerate(order)}
    def bd(c):
        t, a, b = c
        if t == "v": return []
        if t == "ex": return [("v", a, b), ("v", a + 1, b)]
        if t == "ey": return [("v", a, b), ("v", a, b + 1)]
        return [("ex", a, b), ("ex", a, b + 1), ("ey", a, b), ("ey", a + 1, b)]
    cols = [set(pos[f] for f in bd(c)) for c in order]
    low_inv = {}; pairs = []
    for k, col in enumerate(cols):
        while col:
            lo = max(col)
            if lo in low_inv:
                col ^= cols[low_inv[lo]]
            else:
                low_inv[lo] = k; pairs.append((lo, k)); break
        cols[k] = col
    dgm = []
    for lo, k in pairs:
        if dimof[order[lo][0]] == 1:
            b_, d_ = idx[order[lo]], idx[order[k]]
            if b_ > d_:
                dgm.append((b_, d_))
    # essential H1 classes: unpaired edges with zero column
    paired = set(lo for lo, _ in pairs) | set(k for _, k in pairs)
    ess = [order[k] for k in range(len(order)) if k not in paired and dimof[order[k][0]] == 1]
    return sorted(dgm, reverse=True), len(ess)

def entropy(dgm):
    L = [b - d for b, d in dgm]
    if len(L) == 0: return 0.0
    p = np.array(L) / sum(L)
    return float(-(p * np.log(p)).sum())

for r in (1, 2, 3):
    dB, eB = h1_diagram(B, r); dA, eA = h1_diagram(A, r)
    dBp, e1 = h1_diagram(Bp, r); dAp, e2 = h1_diagram(Ap, r); dC, e3 = h1_diagram(C, r)
    print(f"r={r}: B {dB} A {dA} B' {dBp} A' {dAp} C {dC} essential {eB,eA,e1,e2,e3}")
    check(f"r={r} 3x3 diagrams", dB == [(2.0, 0.0)] and dA == [] and eB == eA == 0)
    check(f"r={r} 5x5 diagrams", dBp == [(3.0, 1.0), (3.0, 0.0)] and dAp == [(3.0, 1.0)]
          and dC == dBp and e1 == e2 == e3 == 0)
EB, EA = entropy(h1_diagram(Bp)[0]), entropy(h1_diagram(Ap)[0])
exact = float(-(sp.Rational(3, 5) * sp.log(sp.Rational(3, 5)) + sp.Rational(2, 5) * sp.log(sp.Rational(2, 5))))
print(f"E(B')={EB:.6f}  exact {exact:.6f}  E(A')={EA}  E(B)={entropy(h1_diagram(B)[0])} E(A)={entropy(h1_diagram(A)[0])}")
check("entropies 0.673 vs 0; 3x3 both 0", abs(EB - exact) < 1e-12 and abs(exact - 0.673) < 5e-4 and EA == 0
      and entropy(h1_diagram(B)[0]) == 0 and entropy(h1_diagram(A)[0]) == 0)
# negative controls
Bneg = mat(5, {(1, 1): 0, (3, 3): 3}, 3)
check("NEG B'_44=3 gives one bar (entropy 0)", entropy(h1_diagram(Bneg)[0]) == 0)
p = np.array([3, 2]) / 5.0
check("NEG mutated entropy (log base 2) differs from stated 0.673", abs(-(p * np.log2(p)).sum() - 0.673) > 0.1)
mx = 0
for _ in range(300):
    R = rng.integers(0, 10, (3, 3)); R = R + R.T
    mx = max(mx, len(h1_diagram(R)[0]))
check(f"3x3 random symmetric: max #H1 bars = {mx} <= 1", mx <= 1)
mx5 = 0
for _ in range(100):
    R = rng.integers(0, 10, (5, 5)); R = R + R.T
    mx5 = max(mx5, len(h1_diagram(R)[0]))
check(f"NEG/sanity 5x5 random can have >=2 bars (max {mx5})", mx5 >= 2)

# ---------------------------------------------------------------- 2. cocycles d=2
print("== Prop 6.4 ==")
s1 = np.array([[0, 1], [1, 0]], complex); s2 = np.array([[0, -1j], [1j, 0]]); s3 = np.diag([1, -1]).astype(complex)
g = [s1, s2]; gam = -1j * s1 @ s2
check("grading -i g1 g2 = sigma3", np.allclose(gam, s3))
check("gamma anticommutes with gamma^mu", all(np.allclose(gam @ x + x @ gam, 0) for x in g))
T1 = np.array([[np.trace(g[m] @ g[n]) for n in range(2)] for m in range(2)])
T2 = np.array([[np.trace(gam @ g[m] @ g[n]) for n in range(2)] for m in range(2)])
check("tr(g^mu g^nu) = 2 delta", np.allclose(T1, 2 * np.eye(2)))
check("tr(gamma g^mu g^nu) = 2i eps", np.allclose(T2, 2j * np.array([[0, 1], [-1, 0]])))

def smooth_step(t):
    t = np.clip(t, 0, 1)
    a = np.where(t > 0, np.exp(-1 / np.maximum(t, 1e-300)), 0)
    b = np.where(t < 1, np.exp(-1 / np.maximum(1 - t, 1e-300)), 0)
    return a / (a + b)
def Fmap(x1, x2, k, Rot):
    X, Y = x1 - 0.5, x2 - 0.5; r = np.hypot(X, Y); ph = k * np.arctan2(Y, X)
    th = np.pi * smooth_step(2.2 * r)            # north pole near centre, south pole for r>=1/2.2
    F = np.stack([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)])
    return np.einsum("ij,j...->i...", Rot, F)
def tau_terms(N, k, Rot):
    h = 1.0 / N; x = (np.arange(N) + 0.5) * h; X1, X2 = np.meshgrid(x, x, indexing="ij")
    F = Fmap(X1, X2, k, Rot)
    # spectral derivatives (periodic; F is constant near the boundary of the cell)
    kk = 2j * np.pi * np.fft.fftfreq(N, d=h)
    d1 = np.real(np.fft.ifft(kk[:, None] * np.fft.fft(F, axis=1), axis=1))
    d2 = np.real(np.fft.ifft(kk[None, :] * np.fft.fft(F, axis=2), axis=2))
    def tau(a, b, c):        # ungraded, formula (a), via explicit Pauli products
        trG = np.zeros_like(F[0])
        trgG = np.zeros_like(F[0], dtype=complex)
        dd = [d1, d2]
        for m in range(2):
            for n in range(2):
                coef = -F[a] * dd[m][b] * dd[n][c]
                trG = trG + coef * np.real(np.trace(g[m] @ g[n]))
                trgG = trgG + coef * np.trace(gam @ g[m] @ g[n])
        return trG.sum() * h * h / (4 * np.pi), trgG.sum() * h * h / (4 * np.pi)
    ung = tau(0, 1, 2)[0]
    S = sum(np.linalg.det(np.eye(3)[list(s)]) * tau(*s)[1] for s in itertools.permutations(range(3)))
    return ung, (1j / 4) * S, F
def degree_by_preimages(k, Rot, N=2001):
    """Signed count of preimages of a regular value (independent of the integral)."""
    # regular value: image of a generic point; count solutions on a fine grid via sign of Jacobian
    yv = Rot @ np.array([np.sin(1.1) * np.cos(0.3), np.sin(1.1) * np.sin(0.3), np.cos(1.1)])
    # in local polar coords, F^{-1}(yv): theta = 1.1 -> r fixed; phi = 0.3 mod 2pi/k -> k points
    # orientation sign from the Jacobian determinant F.(d1F x d2F) at those points
    from scipy.optimize import brentq
    rr = brentq(lambda r: np.pi * smooth_step(2.2 * r) - 1.1, 1e-6, 1 / 2.2)
    tot = 0
    for j in range(abs(k)):
        ang = (0.3 + 2 * np.pi * j) / k
        p = np.array([0.5 + rr * np.cos(ang), 0.5 + rr * np.sin(ang)])
        e = 1e-6
        Fp = Fmap(p[0], p[1], k, Rot); Fa = Fmap(p[0] + e, p[1], k, Rot); Fb = Fmap(p[0], p[1] + e, k, Rot)
        assert np.allclose(Fp, yv, atol=1e-8)
        tot += np.sign(np.dot(Fp, np.cross((Fa - Fp) / e, (Fb - Fp) / e)))
    return int(tot)
def rand_rot():
    Q, R = np.linalg.qr(rng.normal(size=(3, 3))); Q = Q * np.sign(np.diag(R))
    return Q if np.linalg.det(Q) > 0 else -Q
rots = [np.eye(3)] + [rand_rot() for _ in range(4)]
for k in (1, 2, -1):
    for N in (128, 256, 512):
        vals = [tau_terms(N, k, Q)[:2] for Q in rots[:3]]
        degs = [degree_by_preimages(k, Q) for Q in rots[:3]]
        print(f"k={k} N={N}: deg(preimage)={degs} graded={[np.round(v[1],6) for v in vals]} ungraded={[round(float(v[0]),5) for v in vals]}")
    ok = all(abs(v[1] - d) < 1e-6 for v, d in zip(vals, degs)) and degs[0] == k
    check(f"(i/4) sum sgn tau^gamma = deg F for k={k}", ok)
ung = [tau_terms(256, 1, Q)[0] for Q in rots]
print("ungraded tau_2 over 5 rotations (deg 1):", np.round(ung, 5))
check("ungraded tau_2 varies under rotations at fixed degree", np.ptp(ung) > 1e-3)
v = tau_terms(256, 1, rots[1])
# negative control: ungraded antisymmetrisation (tr g^mu g^nu instead of tr gamma g^mu g^nu) gives 0, not deg
h = 1.0 / 256
check("NEG prefactor i/2 instead of i/4 gives 2*deg (fails)", abs(2 * v[1] - 1) > 0.5)
# degree-0 example of Remark 6.5
s = 0.7; x = (np.arange(512) + 0.5) / 512; X1, X2 = np.meshgrid(x, x, indexing="ij")
c = np.cos(2 * np.pi * X1); P1 = s * c / np.sqrt(2); P0 = np.sqrt(1 - s**2 * c**2)
dP1 = -s * 2 * np.pi * np.sin(2 * np.pi * X1) / np.sqrt(2)
tau0 = -(1 / (2 * np.pi)) * np.mean(P0 * dP1 * dP1)
check(f"Rem 6.5: degree-0 map, tau_2 = {tau0:.4f} < 0", tau0 < -0.1)

# ---------------------------------------------------------------- 3. QFI
print("== Lemma 7.2 / Thm 7.3 ==")
def rand_rho(n):
    G = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)); R = G @ G.conj().T + 0.2 * np.eye(n)
    return R / np.trace(R).real
def herm0(n):
    X = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)); X = X + X.conj().T
    return X - np.trace(X) / n * np.eye(n)
def qfi_formula(rho, dr, factor=2.0):
    lam, U = np.linalg.eigh(rho); D = [U.conj().T @ x @ U for x in dr]
    W = 1 / (lam[:, None] + lam[None, :])
    return np.array([[factor * np.real(np.sum(W * D[m] * D[n].T)) for n in range(len(dr))] for m in range(len(dr))])
def bures_g(rho, X, eps=1e-3):
    """g(X,X) from the Bures distance: d_B^2 = 2(1-sqrt F) = g eps^2/4 + O(eps^3)."""
    def fid(r1, r2):
        w, V = np.linalg.eigh(r1); s = (V * np.sqrt(w)) @ V.conj().T
        M = s @ r2 @ s; M = (M + M.conj().T) / 2
        return np.sum(np.sqrt(np.clip(np.linalg.eigvalsh(M), 0, None))) ** 2
    vals = []
    for e in (eps, eps / 2):
        F = fid(rho, rho + e * X); vals.append(8 * (1 - np.sqrt(F)) / e**2)
    return 2 * vals[1] - vals[0]       # Richardson
err2, err1 = [], []
for _ in range(5):
    n = 3; rho = rand_rho(n); X = herm0(n)
    gbs = [bures_g(rho, X, e) for e in (4e-3, 2e-3, 1e-3)]; order = np.log2((gbs[1] - gbs[0]) / (gbs[2] - gbs[1])); gb = (4 * gbs[2] - gbs[1]) / 3
    print(f'  observed order {order:.2f}, extrapolated {gb:.8f}, formula {qfi_formula(rho, [X])[0, 0]:.8f}')
    print('  Bures refinement eps=4e-3,2e-3,1e-3:', np.round(gbs, 8))
    g2 = qfi_formula(rho, [X])[0, 0]; g1 = qfi_formula(rho, [X], 1.0)[0, 0]
    err2.append(abs(gb - g2) / gb); err1.append(abs(gb - g1) / gb)
print("rel err factor 2:", np.round(err2, 7), " factor 1:", np.round(err1, 4))
check("QFI formula with factor 2 matches Bures oracle", max(err2) < 1e-4)
check("NEG formula without factor 2 fails", min(err1) > 0.4)
rho0 = rand_rho(3); Rd = herm0(3)
gR = qfi_formula(rho0, [Rd, Rd]); check(f"Rem 7.4(i): rho=R(x1+x2) det g = {np.linalg.det(gR):.2e} = 0", abs(np.linalg.det(gR)) < 1e-10)
dets = []
for _ in range(10):
    rho0 = rand_rho(3); h1, h2 = herm0(3), herm0(3)
    dets.append(np.linalg.det(qfi_formula(rho0, [1j * (h1 @ rho0 - rho0 @ h1), 1j * (h2 @ rho0 - rho0 @ h2)])))
check(f"Rem 7.4(ii): gauge orbit det g > 0 (min {min(dets):.3e})", min(dets) > 0)
check("Thm 7.3(a): g_mumu >= ||d rho||_HS^2", all(qfi_formula(r, [x])[0, 0] >= np.linalg.norm(x)**2
      for r, x in [(rand_rho(4), herm0(4)) for _ in range(20)]))

# ---------------------------------------------------------------- 4. c_*
print("== Prop 4.5 ==")
def gfun(y1, y2, hess=True):
    u1 = np.cos(y1) * np.sin(y2); u2 = np.sin(y1) * np.cos(y2)
    u11 = -np.sin(y1) * np.sin(y2); u22 = u11; u12 = np.cos(y1) * np.cos(y2)
    G = math.hypot(u1, u2)
    if G == 0: return 0.0
    H = -(u11 + u22) / G + (hess * (u11 * u1 * u1 + 2 * u12 * u1 * u2 + u22 * u2 * u2)) / G**3
    return H * H * G
res = []
for tol in (1e-6, 1e-8, 1e-10):
    val, err = integrate.nquad(lambda a, b: gfun(a, b), [[0, np.pi / 2], [0, np.pi / 2]],
                               opts={"epsabs": tol, "epsrel": tol, "limit": 200})
    res.append(16 * val / (4 * np.pi**2))
print("c_* (adaptive quarter-cell, tol 1e-6/1e-8/1e-10):", [round(r, 7) for r in res])
check("c_* = 1.0578 (paper 1.058)", abs(res[-1] - 1.0578) < 1e-3 and abs(res[-1] - res[-2]) < 1e-5)
valn, _ = integrate.nquad(lambda a, b: gfun(a, b, False), [[0, np.pi / 2], [0, np.pi / 2]], opts={"limit": 200})
check(f"NEG H without Hessian term gives {16*valn/(4*np.pi**2):.4f} != c_*", abs(16 * valn / (4 * np.pi**2) - res[-1]) > 0.05)

# ---------------------------------------------------------------- 5. Thm 2.3(b),(c)
print("== Thm 2.3 ==")
def w2_1d(rho, sig, M=200001):
    x = np.linspace(0, 1, M)
    Fr = integrate.cumulative_trapezoid(rho(x), x, initial=0); Fs = integrate.cumulative_trapezoid(sig(x), x, initial=0)
    q = np.linspace(0, 1, 20001)[1:-1]
    return math.sqrt(np.mean((np.interp(q, Fr / Fr[-1], x) - np.interp(q, Fs / Fs[-1], x))**2))
for eps in (0.1, 0.05):
    w = w2_1d(lambda x: (x <= eps) / eps, lambda x: (x >= 1 - eps) / eps)
    print(f"sharpness eps={eps}: W2={w:.5f} (1-eps={1-eps}), rhs=1")
    check(f"(b) sharpness ratio = 1-eps at eps={eps}", abs(w - (1 - eps)) < 2e-3)
ratios = []
for e in (0.2, 0.1, 0.05):
    h = 1e-3
    w = w2_1d(lambda x: 1 + 0 * x, lambda x: 1 + h * e * np.cos(np.pi * x))
    speed = w / h; c0 = 1 - h * e
    bound = (e / math.sqrt(2)) / (math.pi * math.sqrt(c0))
    ratios.append(speed / bound)
print("speed/bound for rho=1+tau*eps*cos(pi x):", np.round(ratios, 5))
check("(c) bound holds and is attained (ratio -> 1)", all(r <= 1 + 1e-3 for r in ratios) and abs(ratios[-1] - 1) < 5e-3)
check("NEG constant 1/(2 pi) violated", all(r * 2 > 1.5 for r in ratios))

print("failures", fails)
sys.exit(int(fails))
