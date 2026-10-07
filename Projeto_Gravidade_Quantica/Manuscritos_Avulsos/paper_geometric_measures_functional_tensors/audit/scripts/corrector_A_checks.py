"""Corrector's independent checks for the A items of Vol. II (and the replacement statements).

A1  persistent homology / entropy of step realizations: two independent methods
    (M1: union-find on low cells with Alexander duality and the elder rule;
     M2: pixel rasterisation + scipy.ndimage.label of the complement, beta_1 per threshold).
A2  fixed-Gaussian-window Gabor decay off the interface (asymptotic g(-x0)/xi vs QAWF quadrature);
    Hormander cut-off definition for a half-plane (rapid decay off the conormal, 1/t on it).
A3  Dixmier trace on T^1: linear (diagonal) version vs singular-value version.
A4  Clifford traces (sympy), ungraded tau_2 counterexample with degree 0, graded antisymmetrised
    cocycle equal to -4i deg F for rotated degree-1 maps.
A5  QFI metric: Kronecker-solved SLD oracle vs corrected formula 2 sum/(l_i+l_j);
    det g = 0 iff the derivatives are linearly dependent.
Every block has a negative control. Fixed seed. Output in corrector_A_checks.out.txt; exit code = failures.
"""
import os, sys, itertools
import numpy as np
from scipy import ndimage, integrate, linalg
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20261006)
OUT = []
fail = 0
def log(s):
    OUT.append(s); print(s)
def check(name, cond):
    global fail
    if not cond:
        fail += 1
    log(("PASS " if cond else "FAIL ") + name)

# ---------------------------------------------------------------- A1
def dgm1_unionfind(M):
    """H1 diagram of the super-level filtration of the closed-cell step realization of M.
    By Alexander duality, H1 classes of X_t = holes = components of {M < t} (4-adjacency)
    not touching the border. Cells enter the low set in increasing value; elder rule."""
    k = M.shape[0]
    OUTS = k * k
    parent = list(range(k * k + 1)); birth = {OUTS: -np.inf}
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    bars = []
    active = np.zeros((k, k), bool)
    order = sorted(((M[i, j], i, j) for i in range(k) for j in range(k)))
    # cells with equal values enter together: process by value groups
    for v, grp in itertools.groupby(order, key=lambda z: z[0]):
        grp = list(grp)
        for _, i, j in grp:
            c = i * k + j; active[i, j] = True; birth[c] = v
        for _, i, j in grp:
            c = i * k + j
            nbrs = []
            if i in (0, k - 1) or j in (0, k - 1):
                nbrs.append(OUTS)
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a, b = i + di, j + dj
                if 0 <= a < k and 0 <= b < k and active[a, b]:
                    nbrs.append(a * k + b)
            for nb in nbrs:
                r1, r2 = find(c), find(nb)
                if r1 == r2:
                    continue
                # elder survives; younger (larger birth) dies at value v
                if birth[r1] < birth[r2] or (birth[r1] == birth[r2] and r1 == OUTS):
                    old, young = r1, r2
                else:
                    old, young = r2, r1
                if v > birth[young]:
                    bars.append((float(v), float(birth[young])))  # hole for t in (birth, v]
                parent[young] = old
    return sorted(bars)

def beta1_pixels(M, t, R=24):
    img = np.kron(M, np.ones((R, R)))
    low = img < t
    pad = np.pad(low, 1, constant_values=True)
    lab, n = ndimage.label(pad)  # 4-connectivity
    outside = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    return len(set(range(1, n + 1)) - outside)

def entropy(bars):
    if not bars:
        return 0.0
    l = np.array([b - d for b, d in bars]); p = l / l.sum()
    return float(-(p * np.log(p)).sum())

def dgm_from_pixels(M):
    vals = np.unique(M)
    mids = list((vals[:-1] + vals[1:]) / 2) + [vals[-1] - 1e-9]
    return {round(float(t), 6): beta1_pixels(M, t) for t in mids}

log("== A1: original 3x3 pair")
B3 = np.full((3, 3), 2.0); B3[1, 1] = 0
P3 = np.eye(3)[[1, 0, 2]]; A3 = P3 @ B3 @ P3.T
dB, dA = dgm1_unionfind(B3), dgm1_unionfind(A3)
log("Dgm1(B)=%s Dgm1(A)=%s E(B)=%.4f E(A)=%.4f" % (dB, dA, entropy(dB), entropy(dA)))
check("3x3: Dgm1(B)={(2,0)}, Dgm1(A)=empty", dB == [(2.0, 0.0)] and dA == [])
check("3x3: E(B)=E(A)=0 (entropy does NOT separate this pair)", entropy(dB) == 0 == entropy(dA))
check("3x3 pixel cross-check beta1: B=1, A=0 on (0,2]", beta1_pixels(B3, 1.0) == 1 and beta1_pixels(A3, 1.0) == 0)

log("== A1: replacement 5x5 pair")
B5 = np.full((5, 5), 3.0); B5[1, 1] = 0.0; B5[3, 3] = 1.0
P5 = np.eye(5)[[1, 0, 2, 3, 4]]; A5 = P5 @ B5 @ P5.T
check("5x5: A=PBP^T symmetric, isospectral", np.allclose(A5, A5.T) and np.allclose(np.linalg.eigvalsh(A5), np.linalg.eigvalsh(B5)))
check("5x5: A has its 0 at the corner (1,1)", A5[0, 0] == 0 and A5[3, 3] == 1)
dB, dA = dgm1_unionfind(B5), dgm1_unionfind(A5)
EB, EA = entropy(dB), entropy(dA)
Eexp = -(0.6 * np.log(0.6) + 0.4 * np.log(0.4))
log("Dgm1(B)=%s Dgm1(A)=%s E(B)=%.6f (expected %.6f) E(A)=%.6f" % (dB, dA, EB, Eexp, EA))
check("5x5: Dgm1(B)={(3,0),(3,1)}", dB == [(3.0, 0.0), (3.0, 1.0)])
check("5x5: Dgm1(A)={(3,1)}", dA == [(3.0, 1.0)])
check("5x5: E(B)=-0.6ln0.6-0.4ln0.4 > 0 = E(A)", abs(EB - Eexp) < 1e-12 and EA == 0.0)
pb, pa = dgm_from_pixels(B5), dgm_from_pixels(A5)
log("pixel beta1(t) B: %s  A: %s" % (pb, pa))
check("5x5 pixel cross-check: B beta1 = 1 on (0,1), 2 on (1,3); A = 0 on (0,1), 1 on (1,3)",
      pb[0.5] == 1 and pb[2.0] == 2 and pa[0.5] == 0 and pa[2.0] == 1)
log("== A1: reflection pair (equal entropies with N_1 = 2 distinct lifetimes)")
J = np.eye(5)[::-1]; C5 = J @ B5 @ J.T
dC = dgm1_unionfind(C5)
check("reflection: C=JBJ^T != B, isospectral, Dgm1(C)=Dgm1(B), N_1=2 distinct lifetimes, E equal",
      not np.allclose(C5, B5) and dC == dgm1_unionfind(B5) and len({b - d for b, d in dC}) == 2 and entropy(dC) == EB)
# negative control: a mutated entropy (births instead of lifetimes) must NOT reproduce E(B)
Emut = entropy([(b, 0.0) for b, d in dB])
check("NEG CTRL: entropy built from births differs from E(B)", abs(Emut - EB) > 1e-3)
# random isospectral pairs: union-find vs pixel beta1 agreement (method cross-validation)
agree = True
for _ in range(40):
    k = 5
    Mr = rng.integers(0, 4, size=(k, k)).astype(float); Mr = np.maximum(Mr, Mr.T)
    bars = dgm1_unionfind(Mr)
    for t in [0.5, 1.5, 2.5, 3.5]:
        n_uf = sum(1 for b, d in bars if d < t <= b)
        if n_uf != beta1_pixels(Mr, t, R=8):
            agree = False
check("union-find barcode reproduces pixel beta1 on 40 random symmetric 5x5 matrices", agree)

# ---------------------------------------------------------------- A2
log("== A2: fixed Gaussian window, f = Heaviside, x0 off the jump")
s = 0.1
g = lambda y: (np.pi * s * s) ** -0.25 * np.exp(-y * y / (2 * s * s))
x0 = 0.5
for xi in [200.0, 1000.0, 3000.0]:
    re = integrate.quad(lambda y: g(y - x0), 0, 60 * s + x0, weight="cos", wvar=xi, limit=2000)[0]
    im = integrate.quad(lambda y: g(y - x0), 0, 60 * s + x0, weight="sin", wvar=xi, limit=2000)[0]
    V = abs(complex(re, -im))
    log("xi=%g |V|=%.4e xi|V|=%.4e  g(-x0)=%.4e" % (xi, V, xi * V, g(-x0)))
check("fixed window: xi|V(x0,xi)| -> g(-x0) != 0 (only 1/xi decay off the interface)", abs(xi * V / g(-x0) - 1) < 1e-2)
log("== A2: Hormander cut-off, half-plane H(y1), product bump chi=b(y1)b(y2)")
def bump(y, c=0.0, r=0.3):
    z = (y - c) / r
    out = np.zeros_like(np.asarray(y, float))
    m = np.abs(z) < 1
    out[m] = np.exp(-1.0 / (1 - z[m] ** 2))
    return out
def ft1(fun, a, bnd, t):
    re = integrate.quad(fun, a, bnd, weight="cos", wvar=t, limit=4000)[0]
    im = integrate.quad(fun, a, bnd, weight="sin", wvar=t, limit=4000)[0]
    return complex(re, -im)
b0 = float(bump(np.array([0.0]))[0])
import mpmath as mp
mp.mp.dps = 40
def ft_bump_mp(t, a=-0.3, bnd=0.3, pieces=400):
    f = lambda y: mp.e ** (-1 / (1 - (y / mp.mpf("0.3")) ** 2)) * mp.e ** (-1j * t * y)
    pts = [a + (bnd - a) * mp.mpf(i) / pieces for i in range(pieces + 1)]
    return abs(mp.quad(f, pts))
vals = []
for t in [100.0, 400.0, 1600.0]:
    Fn = ft1(lambda y: bump(np.array([y]))[0], 0.0, 0.3, t)          # normal direction: b * H
    vals.append((t, abs(Fn) * t))
    log("t=%g  t|FT(bH)(t)|=%.4e (b(0)=%.4e)" % (t, abs(Fn) * t, b0))
check("on the conormal: t|FT| -> b(0) (not rapid)", abs(vals[-1][1] / b0 - 1) < 2e-2)
tv = []
for t in [50, 200, 800, 1600]:
    Ft = ft_bump_mp(t)  # tangential factor: smooth compactly supported bump, mpmath at 40 digits
    tv.append(float(Ft) * t ** 4)
    log("t=%d  t^4 |FT(b)(t)| = %.3e" % (t, tv[-1]))
check("off the conormal (tangential factor): t^4|FT(b)| decreases by > 1e3 from t=50 to t=1600", tv[-1] < 1e-3 * tv[0])
# negative control: a smooth f (no jump) with the SAME fixed Gaussian window decays fast
Vs = abs(ft1(lambda y: g(y - x0) * np.exp(-(y - 0.7) ** 2 / 0.02), -3, 4, 200.0))
check("NEG CTRL fixed window on a smooth function: |V| at xi=200 below 1e-12", Vs < 1e-12)

# ---------------------------------------------------------------- A3
log("== A3: Dixmier trace on T^1, T = M_f |D|^{-1} (|D|^{-1}:=0 on ker D)")
def dixmier_slopes(fhat, N):
    n = np.arange(-N, N + 1)
    T = np.zeros((2 * N + 1, 2 * N + 1), complex)
    for a, m in enumerate(n):
        for c, k in fhat.items():
            col = m - c
            if -N <= col <= N and col != 0:
                T[a, col + N] = k / (2 * np.pi * abs(col))
    sv = np.sort(linalg.svdvals(T))[::-1]
    dg = np.array([T[a, a].real for a in range(2 * N + 1)])
    # order the diagonal by the eigenvalue order of |D| (|n| increasing)
    idx = np.argsort(np.abs(n), kind="stable"); dg = dg[idx]
    Ns = np.array([N // 4, N // 2, N])
    cs_sv = np.cumsum(sv); cs_dg = np.cumsum(dg)
    def slope(cs):
        return np.polyfit(np.log(Ns), cs[Ns - 1], 1)[0]
    return slope(cs_dg), slope(cs_sv)
N = 1200
for name, fh, intf, intabs in [("f=1", {0: 1.0}, 1.0, 1.0),
                              ("f=cos2pix", {1: 0.5, -1: 0.5}, 0.0, 2 / np.pi),
                              ("f=0.3+cos2pix", {0: 0.3, 1: 0.5, -1: 0.5}, 0.3, None)]:
    sd, ss = dixmier_slopes(fh, N)
    log("%-14s linear(diagonal) slope %.4f vs (1/pi)int f = %.4f | singular-value slope %.4f" % (name, sd, intf / np.pi, ss))
    check("%s: linear Dixmier = (1/pi) int f" % name, abs(sd - intf / np.pi) < 5e-3)
    if intabs is not None:
        check("%s: singular-value sum gives (1/pi) int|f| (within 2%%)" % name, abs(ss - intabs / np.pi) < 0.02 * max(intabs / np.pi, 0.05) + 0.004)
sd, ss = dixmier_slopes({1: 0.5, -1: 0.5}, N)
check("NEG CTRL: for f=cos the singular-value version is NOT (1/pi)int f = 0", ss > 0.1)

# ---------------------------------------------------------------- A4
log("== A4: Clifford traces in d=2")
s1 = sp.Matrix([[0, 1], [1, 0]]); s2 = sp.Matrix([[0, -sp.I], [sp.I, 0]]); gam = -sp.I * s1 * s2
G = [s1, s2]
ok_sym = all(sp.simplify((G[m] * G[n]).trace() - 2 * (1 if m == n else 0)) == 0 for m in range(2) for n in range(2))
eps = {(0, 1): 1, (1, 0): -1, (0, 0): 0, (1, 1): 0}
ok_gr = all(sp.simplify((gam * G[m] * G[n]).trace() - 2 * sp.I * eps[(m, n)]) == 0 for m in range(2) for n in range(2))
check("tr(g^mu g^nu) = 2 delta (no epsilon part without grading)", ok_sym)
check("gamma = -i g1 g2 = sigma3 and tr(gamma g^mu g^nu) = 2i eps^{mu nu}", ok_gr and gam == sp.Matrix([[1, 0], [0, -1]]))
check("NEG CTRL: tr(gamma g^1 g^2) != 0 while tr(g^1 g^2) == 0", (gam * s1 * s2).trace() != 0 and (s1 * s2).trace() == 0)

n = 1024
x = (np.arange(n) + 0.5) / n
X1, X2 = np.meshgrid(x, x, indexing="ij")
def grad(F):
    k = 2 * np.pi * np.fft.fftfreq(n, d=1.0 / n)
    Fh = np.fft.fft2(F)
    return np.real(np.fft.ifft2(1j * k[:, None] * Fh)), np.real(np.fft.ifft2(1j * k[None, :] * Fh))
def tau_ungraded(F0, F1, F2):  # -(1/2pi) int F0 grad F1 . grad F2
    a1, b1 = grad(F1); a2, b2 = grad(F2)
    return -np.mean(F0 * (a1 * a2 + b1 * b2)) / (2 * np.pi)
def tau_graded(F0, F1, F2):    # -(i/2pi) int F0 dF1 ^ dF2
    a1, b1 = grad(F1); a2, b2 = grad(F2)
    return -1j * np.mean(F0 * (a1 * b2 - b1 * a2)) / (2 * np.pi)
def antisym(F):
    return sum(np.sign(np.linalg.det(np.eye(3)[list(p)])) * tau_graded(F[p[0]], F[p[1]], F[p[2]]) for p in itertools.permutations(range(3)))
def degree(F):
    g1 = [grad(c) for c in F]
    d1 = np.array([q[0] for q in g1]); d2 = np.array([q[1] for q in g1])
    return np.mean(np.einsum("ixy,ixy->xy", np.array(F), np.cross(d1, d2, axis=0))) / (4 * np.pi)
# degree-0 counterexample (analytic): F = (sqrt(1-s^2cos^2), s cos/sqrt2, s cos/sqrt2)
sa = 0.8
c = np.cos(2 * np.pi * X1)
F0 = np.sqrt(1 - sa ** 2 * c ** 2); F1 = sa * c / np.sqrt(2); F2 = F1.copy()
t_exact = -(1 / (2 * np.pi)) * np.mean(F0 * (sa * 2 * np.pi * np.sin(2 * np.pi * X1)) ** 2 / 2)
tu = tau_ungraded(F0, F1, F2)
log("degree-0 map: deg=%.2e  tau_2(ungraded)=%.6f (direct quadrature %.6f)" % (degree([F0, F1, F2]), tu, t_exact))
check("ungraded tau_2 != 0 = c_2 deg for a degree-0 map", abs(degree([F0, F1, F2])) < 1e-10 and tu < -0.1 and abs(tu - t_exact) < 1e-8)
# degree-1 map T^2 -> S^2 (collapse the boundary of the square to the south pole)
u1, u2 = 2 * X1 - 1, 2 * X2 - 1
r = np.sqrt(u1 ** 2 + u2 ** 2); phi = np.arctan2(u2, u1)
sm = lambda z: np.where(z <= 0, 0, np.where(z >= 1, 1, z ** 3 * (10 - 15 * z + 6 * z * z)))
th = np.pi * sm(r / 0.9)
Fd = np.array([np.sin(th) * np.cos(phi), np.sin(th) * np.sin(phi), np.cos(th)])
def rot(a, b, cc):
    Rz = lambda q: np.array([[np.cos(q), -np.sin(q), 0], [np.sin(q), np.cos(q), 0], [0, 0, 1]])
    Ry = lambda q: np.array([[np.cos(q), 0, np.sin(q)], [0, 1, 0], [-np.sin(q), 0, np.cos(q)]])
    return Rz(a) @ Ry(b) @ Rz(cc)
taus, degs, anti = [], [], []
for _ in range(5):
    R = rot(*rng.uniform(0, 2 * np.pi, 3))
    Fr = np.einsum("ij,jxy->ixy", R, Fd)
    degs.append(degree(list(Fr))); taus.append(tau_ungraded(*Fr)); anti.append(antisym(list(Fr)))
log("rotated degree-1 maps: deg %s" % np.round(degs, 4))
log("   ungraded tau_2: %s" % np.round(taus, 4))
log("   (i/4) * antisymmetrised graded tau: %s" % np.round([(1j / 4 * a) for a in anti], 4))
check("degree = 1 for all rotations (to 1e-2)", np.allclose(degs, 1, atol=1e-2))
check("ungraded tau_2 varies at fixed degree (spread > 1e-2)", np.ptp(taus) > 1e-2)
check("(i/4) sum_sigma sgn tau^gamma = deg F (to 1e-2)", np.allclose([(1j / 4 * a).real for a in anti], 1, atol=1e-2) and max(abs((1j / 4 * a).imag) for a in anti) < 1e-8)
const = [np.ones((n, n)), np.zeros((n, n)), np.zeros((n, n))]
check("NEG CTRL constant map: graded cocycle 0", abs(antisym(const)) < 1e-12)

# ---------------------------------------------------------------- A5
log("== A5: QFI metric")
def herm(k):
    M = rng.normal(size=(k, k)) + 1j * rng.normal(size=(k, k)); return (M + M.conj().T) / 2
def sld_kron(rho, drho):
    k = rho.shape[0]; I = np.eye(k)
    Mop = 0.5 * (np.kron(I, rho) + np.kron(rho.T, I))  # vec(rho L + L rho)/2, column-major
    L = np.linalg.solve(Mop, drho.reshape(-1, order="F")).reshape(k, k, order="F")
    return L
def g_oracle(rho, ds):
    Ls = [sld_kron(rho, d) for d in ds]
    return np.array([[0.5 * np.trace(rho @ (La @ Lb + Lb @ La)).real for Lb in Ls] for La in Ls])
def g_formula(rho, ds, factor=2.0):
    lam, U = np.linalg.eigh(rho)
    Dt = [U.conj().T @ d @ U for d in ds]
    den = lam[:, None] + lam[None, :]
    return np.array([[factor * np.sum((Da * Db.T).real / den) for Db in Dt] for Da in Dt])
ok = True; okneg = True
for _ in range(5):
    k = 4
    W = rng.normal(size=(k, k)) + 1j * rng.normal(size=(k, k)); rho = W @ W.conj().T + 0.2 * np.eye(k); rho /= np.trace(rho).real
    ds = []
    for _ in range(3):
        h = herm(k); h -= np.trace(h) / k * np.eye(k); ds.append(h)
    go, gf, gh = g_oracle(rho, ds), g_formula(rho, ds), g_formula(rho, ds, 1.0)
    ok &= np.allclose(go, gf, rtol=1e-10, atol=1e-12)
    okneg &= not np.allclose(go, gh, rtol=1e-3)
check("g = 2 sum Re(<i|d_mu rho|j><j|d_nu rho|i>)/(l_i+l_j) equals the SLD oracle (5 random states)", ok)
check("NEG CTRL: the formula without the factor 2 disagrees with the oracle", okneg)
# rank criterion
k = 3
W = rng.normal(size=(k, k)) + 1j * rng.normal(size=(k, k)); rho0 = W @ W.conj().T + 0.3 * np.eye(k); rho0 /= np.trace(rho0).real
h1, h2 = herm(k), herm(k)
for hh in (h1, h2):
    hh -= np.trace(hh) / k * np.eye(k)
# gauge orbit rho(x) = U(x) rho0 U(x)^dag, U = exp(i(x1 h1 + x2 h2)); derivatives at x=0: i[h_mu, rho0]
dg = [1j * (h1 @ rho0 - rho0 @ h1), 1j * (h2 @ rho0 - rho0 @ h2)]
detg = np.linalg.det(g_formula(rho0, dg))
check("gauge orbit: det g > 0 (constant modulo gauge does not give Vol = 0)", detg > 1e-6)
# rho depending on x1+x2 only: both partials nonzero but linearly dependent
dd = [h1, h1]
check("rho(x)=R(x1+x2): d_1 rho, d_2 rho nonzero and det g = 0", np.linalg.norm(h1) > 0.1 and abs(np.linalg.det(g_formula(rho0, dd))) < 1e-12)
# random: det g > 0 iff the d derivatives are linearly independent (real span of Hermitian matrices)
ok = True
for _ in range(30):
    dep = rng.random() < 0.5
    a = herm(k); a -= np.trace(a) / k * np.eye(k)
    b = herm(k); b -= np.trace(b) / k * np.eye(k)
    if dep:
        b = 0.7 * a
    dgm = np.linalg.det(g_formula(rho0, [a, b]))
    ok &= (dgm > 1e-9) == (not dep)
check("det g > 0 iff {d_mu rho} linearly independent (30 random cases)", ok)

log("failures=%d" % fail)
open(os.path.join(HERE, "corrector_A_checks.out.txt"), "w", encoding="utf8").write("\n".join(OUT))
sys.exit(int(fail))
