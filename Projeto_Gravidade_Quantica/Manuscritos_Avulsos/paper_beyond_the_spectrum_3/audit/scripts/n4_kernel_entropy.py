"""OBL-013/014/015.
OBL-013: random frame (QR of random matrix, discrete L^2) -> diagonalisation, trace, diagonal.
OBL-014 counterexample: n = 1, psi(x1,x2) non-separable Gaussian on [-L,L]^2.
  rank(rho_1) claimed <= n = 1. Oracle: Mehler -- Schmidt ratios geometric with
  q = beta/(alpha + sqrt(alpha^2-beta^2)), alpha = A - B^2/(2A), beta = B^2/(2A).
  Negative control: B = 0 (separable) gives rank 1. Refinement: grid N = 200, 400, 800.
  Sign: unnormalised rho_1 = Tr(A)|chi><chi| with Tr A = 5 gives K = -log 5 < 0.
OBL-015: random states, S_R >= I, symmetry, S_R <= 2 min(S_A,S_B); control S_R >= 2I must fail."""
import numpy as np, sys
from scipy.linalg import sqrtm, eigh
rng = np.random.default_rng(7)
fails = 0
# OBL-013
M, n = 300, 5
Psi, _ = np.linalg.qr(rng.normal(size=(M, n)) + 1j * rng.normal(size=(M, n)))
X = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
A = X @ X.conj().T
K = Psi @ A @ Psi.conj().T
lam, U = np.linalg.eigh(A)
Phi = Psi @ U
K2 = (Phi * lam) @ Phi.conj().T
e1 = np.abs(K - K2).max(); e2 = abs(np.trace(K) - np.trace(A)); e3 = np.abs(np.diag(K) - np.einsum('ij,jk,ik->i', Psi, A, Psi.conj())).max()
print('OBL-013: |K - sum lam phi phi*| = %.1e, |TrK - TrA| = %.1e, diag err %.1e, min eig K = %.2e' % (e1, e2, e3, np.linalg.eigvalsh(K).min()))
fails += max(e1, e2, e3) > 1e-10
# OBL-014
Aq, L = 1.0, 8.0
for B in [0.6, 0.0]:
    alpha, beta = Aq - B ** 2 / (2 * Aq), B ** 2 / (2 * Aq)
    q = beta / (alpha + np.sqrt(alpha ** 2 - beta ** 2)) if B else 0.0
    for N in [200, 400, 800]:
        x = np.linspace(-L, L, N); h = x[1] - x[0]
        P = np.exp(-Aq * (x[:, None] ** 2 + x[None, :] ** 2) / 2 + B * x[:, None] * x[None, :])
        P /= np.sqrt((P ** 2).sum() * h * h)
        s = np.linalg.svd(P * h, compute_uv=False) ** 2  # eigenvalues of rho_1 (trace 1)
        nz = (s > 1e-12).sum()
        ratios = s[1:4] / s[0:3]
        print('B=%.1f N=%d: #eig>1e-12 = %d, top eigs %s, ratios %s, Mehler q = %.6f' % (B, N, nz, np.array2string(s[:4], precision=5), np.array2string(ratios, precision=6), q))
    if B:
        fails += nz <= 1 or np.abs(ratios - q).max() > 1e-6
    else:
        fails += nz != 1
print('Unnormalised n=1 example: Tr A = 5 -> modular energy -log 5 = %.4f (paper: strictly positive)' % -np.log(5))


# OBL-015
def S(r):
    w = np.linalg.eigvalsh(r); w = w[w > 1e-14]
    return float(-(w * np.log(w)).sum())


def ptrace(r, dims, keep):
    k = len(dims)
    r = r.reshape(dims + dims)
    idx = list(range(k)); idx2 = [i + k for i in range(k)]
    for i in sorted(set(range(k)) - set(keep), reverse=True):
        r = np.trace(r, axis1=i, axis2=i + r.ndim // 2)
    d = int(np.prod([dims[i] for i in keep]))
    return r.reshape(d, d)


def SR(rho, da, db):
    sq = sqrtm(rho)  # |sqrt rho> in AB (x) A*B*: vector components sq[(a,b),(a',b')]
    v = sq.reshape(da, db, da, db)  # a b a* b*
    sig = np.einsum('abcd,ebfd->acef', v, v.conj()).reshape(da * da, da * da)  # trace out b, b*
    return S(sig)


def SR_alt(rho, da, db):
    # independent route: build full pure state with kron/explicit indices then partial trace via ptrace
    sq = sqrtm(rho)
    psi = sq.reshape(-1)  # ordering (a,b,a*,b*)
    full = np.outer(psi, psi.conj())
    return S(ptrace(full, [da, db, da, db], [0, 2]))


viol = viol2 = sym = 0; neg = 0
for t in range(300):
    da, db = rng.integers(2, 4), rng.integers(2, 4)
    r = rng.integers(1, da * db + 1)
    G = rng.normal(size=(da * db, r)) + 1j * rng.normal(size=(da * db, r))
    rho = G @ G.conj().T; rho /= np.trace(rho).real
    sr, sr2 = SR(rho, da, db), SR_alt(rho, da, db)
    rhoA = ptrace(rho, [da, db], [0]); rhoB = ptrace(rho, [da, db], [1])
    I = S(rhoA) + S(rhoB) - S(rho)
    rho_sw = rho.reshape(da, db, da, db).transpose(1, 0, 3, 2).reshape(da * db, da * db)
    srs = SR(rho_sw, db, da)
    viol += sr < I - 1e-8
    viol2 += sr > 2 * min(S(rhoA), S(rhoB)) + 1e-8
    sym += abs(sr - srs) > 1e-7 or abs(sr - sr2) > 1e-7
    neg += sr < 2 * I - 1e-8
print('OBL-015: S_R<I violations %d, S_R>2min violations %d, asym/route mismatches %d, mutated S_R>=2I fails in %d/300' % (viol, viol2, sym, neg))
fails += viol + viol2 + sym + (neg == 0)
print('failures:', fails)
sys.exit(int(fails))
