"""Layer-2 re-check of OBL-014 (Prop. 6.2) and Remark 6.3.

(A) Mehler counterexample, psi(x,y) ~ exp(-(x^2+y^2)/2 + beta x y):
    Oracle 1 (new): Renyi moments Tr rho^k, k = 2..6, as *Gaussian determinants*
      Tr rho^k = int prod_{i} psi(x_i, y_i) psi(x_{i+1}, y_i) / N^k   (cyclic),
      a 2k-dimensional Gaussian integral = (2 pi)^k / sqrt(det Q_k) / (pi/sqrt(1-b^2))^k.
      Compared with the geometric law p_n = (1-q) q^n, q = ((1-sqrt(1-b^2))/b)^2:
      sum p_n^k = (1-q)^k / (1-q^k).
    Oracle 2: Nystrom eigenvalues of rho on Gauss-Legendre grids, 3 refinements,
      successive ratios p_{n+1}/p_n vs q, first 8 eigenvalues all > 0.
    Negative control: q' = sqrt(q) (Schmidt coefficient instead of probability) fails.
(B) Rank bound rank rho <= sum_k m_k (finite Schmidt ranks), finite-dimensional model
    C^{d1} (x) C^{d2}; frames built from random products and orthonormalised, the
    Schmidt rank of each final psi_k measured by SVD. 300 random trials; also the
    bound is attained generically.  Negative control: "rank <= n" fails.
(C) Normalised modular Hamiltonian: E_k = -log p_k >= 0, and > 0 for all k iff rank >= 2.
    Negative control: unnormalised rho (A = 5, product frame) gives -log 5 < 0.
(D) Trace: Tr rho = Tr A for random A >= 0.
"""
import sys
import numpy as np
from numpy.polynomial.legendre import leggauss

rng = np.random.default_rng(20261006)
fails = 0
out = []


def log(s):
    print(s)
    out.append(s)


def check(name, ok):
    global fails
    log(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        fails += 1


def q_of(beta):
    return ((1 - np.sqrt(1 - beta ** 2)) / beta) ** 2


def renyi_gauss(beta, k):
    """Tr rho^k via a 2k-dim Gaussian integral; variables x_1..x_k, y_1..y_k.
    rho(x,x') = int psi(x,y) psi(x',y) dy; Tr rho^k = int prod_i rho(x_i, x_{i+1})."""
    n = 2 * k
    Q = np.zeros((n, n))
    # each factor psi(x_i,y_i) psi(x_{i+1},y_i): exponent -(1/2)[x_i^2+y_i^2-2b x_i y_i]
    #                                                 -(1/2)[x_{i+1}^2+y_i^2-2b x_{i+1} y_i]
    for i in range(k):
        xi, yi, xj = i, k + i, (i + 1) % k
        for (a, b_) in ((xi, yi), (xj, yi)):
            Q[a, a] += 1
            Q[b_, b_] += 1
            Q[a, b_] -= beta
            Q[b_, a] -= beta
    val = (2 * np.pi) ** (n / 2) / np.sqrt(np.linalg.det(Q))
    norm = 2 * np.pi / np.sqrt(1 - beta ** 2)  # int psi^2 = 2pi/sqrt(det M), M=[[1,-b],[-b,1]]... squared form
    # int psi^2 dx dy = int exp(-(x^2+y^2) + 2 b x y) = pi / sqrt(1-b^2)
    norm = np.pi / np.sqrt(1 - beta ** 2)
    return val / norm ** k


log("== (A) Mehler counterexample ==")
for beta in (0.6, 0.3, -0.45):
    q = q_of(beta)
    for k in range(2, 7):
        g = renyi_gauss(beta, k)
        geo = (1 - q) ** k / (1 - q ** k)
        qw = np.sqrt(q)
        wrong = (1 - qw) ** k / (1 - qw ** k)
        log(f"beta={beta:+.2f} k={k} Tr rho^k: Gaussian-det={g:.12f} geometric={geo:.12f} mutated={wrong:.6f}")
        check(f"beta={beta} k={k}: moments match geometric law (1e-10)", abs(g - geo) < 1e-10)
        check(f"beta={beta} k={k}: negative control q'=sqrt(q) fails", abs(g - wrong) > 1e-4)
    if beta == 0.6:
        check("beta=0.6 gives q = 1/9", abs(q - 1 / 9) < 1e-14)

beta = 0.6
q = q_of(beta)
prev = None
for M in (80, 160, 320):
    L = 12.0
    t, w = leggauss(M)
    x = L * t
    w = L * w
    X, Y = np.meshgrid(x, x, indexing="ij")
    psi = np.exp(-(X ** 2 + Y ** 2) / 2 + beta * X * Y)
    psi /= np.sqrt(np.sum(w[:, None] * w[None, :] * psi ** 2))
    # rho(x,x') = sum_y w_y psi(x,y) psi(x',y);  symmetric Nystrom: W^1/2 rho W^1/2
    rho = (psi * w[None, :]) @ psi.T
    S = np.sqrt(w)[:, None] * rho * np.sqrt(w)[None, :]
    ev = np.sort(np.linalg.eigvalsh(S))[::-1][:8]
    ratios = ev[1:] / ev[:-1]
    log(f"Nystrom M={M}: eig={np.array2string(ev, precision=3)} ratios={np.array2string(ratios, precision=8)}")
    if prev is not None:
        log(f"   change vs previous grid: {np.max(np.abs(ev - prev)):.2e}")
    prev = ev
check("Nystrom: first 8 eigenvalues positive (no finite rank <= 7)", np.all(prev > 1e-8))
check("Nystrom: ratios equal q = 1/9 to 1e-6", np.max(np.abs(ratios - q)) < 1e-6)
check("Nystrom: trace of rho = 1 (normalised psi)", abs(np.trace(S) - 1) < 1e-10)

log("== (B)-(D) finite-dimensional frames ==")


def schmidt_rank(v, d1, d2, tol=1e-10):
    s = np.linalg.svd(v.reshape(d1, d2), compute_uv=False)
    return int(np.sum(s > tol * s[0]))


def partial_trace_1(T, d1, d2):
    T4 = T.reshape(d1, d2, d1, d2)
    return np.einsum("ajbj->ab", T4)


viol, attained, n_trials, rank_gt_n = 0, 0, 300, 0
energy_ok = True
iff_ok = True
trace_ok = True
for trial in range(n_trials):
    d1, d2 = rng.integers(6, 14), rng.integers(6, 14)
    n = int(rng.integers(1, 5))
    m = rng.integers(1, 4, size=n)
    vecs = []
    for k in range(n):
        v = np.zeros(d1 * d2, complex)
        for _ in range(m[k]):
            a = rng.normal(size=d1) + 1j * rng.normal(size=d1)
            b = rng.normal(size=d2) + 1j * rng.normal(size=d2)
            v += np.kron(a, b)
        vecs.append(v)
    Q, _ = np.linalg.qr(np.array(vecs).T)  # orthonormal family psi_k (columns)
    mk = [schmidt_rank(Q[:, k], d1, d2) for k in range(n)]
    G = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    A = G @ G.conj().T
    if trial % 3 == 0:  # rank-deficient A as well
        A = np.outer(G[:, 0], G[:, 0].conj())
    T = Q @ A @ Q.conj().T  # kernel K_A as an operator on C^{d1 d2}
    rho = partial_trace_1(T, d1, d2)
    r = np.linalg.matrix_rank(rho, tol=1e-9 * np.linalg.norm(rho, 2))
    viol += r > sum(mk)
    attained += r == min(sum(mk), d1) and trial % 3 != 0
    rank_gt_n += r > n
    trace_ok &= abs(np.trace(rho) - np.trace(A)) < 1e-8 * abs(np.trace(A))
    p = np.linalg.eigvalsh(rho / np.trace(A).real)
    p = p[p > 1e-12]
    E = -np.log(p)
    energy_ok &= bool(np.all(E >= -1e-12))
    iff_ok &= (bool(np.all(E > 1e-12)) == (len(p) >= 2))
log(f"trials={n_trials}: violations of rank <= sum m_k: {viol}; bound attained (full-rank A): {attained}; rank > n: {rank_gt_n}")
check("rank rho <= sum_k m_k in all trials", viol == 0)
check("Tr rho = Tr A in all trials", trace_ok)
check("normalised E_k >= 0 in all trials", energy_ok)
check("E_k > 0 for all k  iff  rank >= 2, in all trials", iff_ok)
check("negative control: 'rank <= n' (v2) fails for some frame of Schmidt rank > 1", rank_gt_n > 0)
# product frame, rank-1 normalised -> E = 0 ; unnormalised A=5 -> -log 5
a = rng.normal(size=5); a /= np.linalg.norm(a)
b = rng.normal(size=4); b /= np.linalg.norm(b)
T = 5 * np.outer(np.kron(a, b), np.kron(a, b))
rho = partial_trace_1(T, 5, 4)
pu = np.max(np.linalg.eigvalsh(rho))
log(f"product frame, A=(5): top eigenvalue of rho = {pu:.12f}; -log = {-np.log(pu):.6f}")
check("negative control: unnormalised modular energy -log 5 < 0", -np.log(pu) < 0 and abs(pu - 5) < 1e-12)
check("normalised rank-1 energy equals 0", abs(-np.log(pu / 5)) < 1e-12)

log(f"failures: {fails}")
with open(__file__.replace(".py", ".out.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
sys.exit(fails)
