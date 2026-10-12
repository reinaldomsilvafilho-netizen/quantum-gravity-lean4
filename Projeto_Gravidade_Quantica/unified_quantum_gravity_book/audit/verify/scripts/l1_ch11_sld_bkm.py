"""L1 check of a sentence in rem:sld_vs_bkm (chap11_emergent_spacetime_tensor_networks_holonomies.tex).

Claim under test (book text): for rho0 = sum_i p_i |i><i| full rank and X = X^dagger,
  g^BKM(X,X) = g^SLD(X,X)  iff  [rho0, X] = 0,
"in that case both reduce to the classical Fisher-Rao metric sum_i X_ii^2 / p_i",
with X_ii read in the eigenbasis |i> of rho0 fixed at the start of the sentence.

Writer's finding (LIVRO_B7): the reduction to sum_i X_ii^2/p_i fails when rho0 has a degenerate
eigenvalue and the eigenbasis does not diagonalise X. Proposed correct forms:
  (a) in an eigenbasis of rho0 that also diagonalises X, both equal sum_i x_i^2/p_i
      (x_i the eigenvalues of X), and
  (b) basis-free: both equal Tr(rho0^{-1} X^2).

Independent oracles (none uses the eigenbasis formulas of the remark):
  * SLD: solve the Sylvester equation X = (rho L + L rho)/2 with scipy, g^SLD = Tr(rho L^2).
  * BKM: (i) the integral int_0^inf Tr(X (s+rho)^-1 X (s+rho)^-1) ds by quadrature;
         (ii) second derivative of S(rho + t X || rho) by central finite differences with logm.
Negative controls (must FAIL): the literal sentence on a degenerate commuting sample, and the
basis-free identity (b) applied to a NON-commuting X.
Exit code is non-zero if a test fails or a control passes.
"""
import sys

import numpy as np
from scipy import integrate, linalg

RNG = np.random.default_rng(20261010)
TOL = 1e-7
failures = 0


def report(name, ok, detail, expect=True):
    """Print PASS/FAIL; expect=False marks a negative control, which must come out False."""
    global failures
    ok = bool(ok)
    if expect:
        tag = "PASS" if ok else "FAIL"
        failures += 0 if ok else 1
    else:
        tag = "PASS (control fails as required)" if not ok else "FAIL (control passed: no power)"
        failures += 0 if not ok else 1
    print(f"{tag}: {name} | {detail}")


def g_sld(rho, X):
    L = linalg.solve_sylvester(rho / 2, rho / 2, X)
    return float(np.real(np.trace(rho @ L @ L)))


def g_bkm_integral(rho, X):
    n = rho.shape[0]
    eye = np.eye(n)

    def f(s):
        R = linalg.inv(s * eye + rho)
        return float(np.real(np.trace(X @ R @ X @ R)))

    # substitute s = u/(1-u) on [0,1) for the infinite range
    val, err = integrate.quad(lambda u: f(u / (1 - u)) / (1 - u) ** 2, 0, 1, limit=400,
                              epsabs=1e-12, epsrel=1e-11)
    return val


def rel_ent(r, s):
    return float(np.real(np.trace(r @ (linalg.logm(r) - linalg.logm(s)))))


def g_bkm_fd(rho, X, h=1e-3):
    # S(rho+tX||rho) has value 0 and slope 0 at t=0 (Tr X = 0); central second difference
    return (rel_ent(rho + h * X, rho) - 2 * 0.0 + rel_ent(rho - h * X, rho)) / h ** 2


def basis_free(rho, X):
    return float(np.real(np.trace(linalg.inv(rho) @ X @ X)))


def literal(p, X):
    return float(sum(np.real(X[i, i]) ** 2 / p[i] for i in range(len(p))))


def rand_herm_traceless(n):
    A = RNG.normal(size=(n, n)) + 1j * RNG.normal(size=(n, n))
    H = (A + A.conj().T) / 2
    return H - np.trace(H) / n * np.eye(n)


def rand_unitary(n):
    Q, R = np.linalg.qr(RNG.normal(size=(n, n)) + 1j * RNG.normal(size=(n, n)))
    return Q * (np.diag(R) / abs(np.diag(R)))


# ---------------------------------------------------------------- T0: oracles agree
rho = np.diag([0.2, 0.3, 0.5]).astype(complex)
U = rand_unitary(3)
rho_r = U @ rho @ U.conj().T
Xr = rand_herm_traceless(3) * 0.1
bi, bf = g_bkm_integral(rho_r, Xr), g_bkm_fd(rho_r, Xr)
report("T0 BKM integral vs relative-entropy Hessian (generic X)", abs(bi - bf) < 1e-4 * abs(bi),
       f"integral={bi:.10f} fd={bf:.10f}")
report("T0' BKM >= SLD on a generic non-commuting X", bi > g_sld(rho_r, Xr) + 1e-9,
       f"BKM={bi:.10f} SLD={g_sld(rho_r, Xr):.10f}")

# ---------------------------------------------------------------- T1: writer's counterexample
p = np.array([0.5, 0.5])
rho = np.diag(p).astype(complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
comm = np.linalg.norm(rho @ X - X @ rho)
s, b = g_sld(rho, X), g_bkm_integral(rho, X)
report("T1a [rho0,X]=0 for p=(1/2,1/2), X=sigma_x", comm < TOL, f"||[rho,X]||={comm:.2e}")
report("T1b SLD = BKM = 4", abs(s - 4) < TOL and abs(b - 4) < 1e-8, f"SLD={s:.12f} BKM={b:.12f}")
report("T1c basis-free Tr(rho^-1 X^2) = 4", abs(basis_free(rho, X) - 4) < TOL,
       f"{basis_free(rho, X):.12f}")
lit = literal(p, X)
report("CONTROL literal sentence sum X_ii^2/p_i equals the common value (degenerate case)",
       abs(lit - s) < TOL, f"literal={lit:.3f} vs {s:.3f}", expect=False)
w, V = np.linalg.eigh(X)  # an eigenbasis of rho0 (= I/2) that also diagonalises X
Xd = V.conj().T @ X @ V
report("T1d corrected (a): in a joint eigenbasis sum x_i^2/p_i = 4",
       abs(literal(p, Xd) - 4) < TOL, f"x={np.round(w, 12)} value={literal(p, Xd):.12f}")

# ---------------------------------------------------------------- T2: random degenerate commuting samples
max_dev_a = max_dev_b = 0.0
lit_gap = 0.0
for _ in range(200):
    q = RNG.dirichlet([1, 1])
    p = np.array([q[0] / 2, q[0] / 2, q[1]])           # degenerate pair
    rho = np.diag(p).astype(complex)
    B = rand_herm_traceless(2) + RNG.normal() * np.eye(2)
    X = np.zeros((3, 3), dtype=complex)
    X[:2, :2] = B
    X[2, 2] = RNG.normal()
    X -= np.trace(X) / 3 * np.diag([1, 1, 1])        # traceless, still block diagonal: commutes
    s, b = g_sld(rho, X), g_bkm_integral(rho, X)
    bf = basis_free(rho, X)
    max_dev_b = max(max_dev_b, abs(s - bf) / bf, abs(b - bf) / bf)
    # joint eigenbasis
    V = np.eye(3, dtype=complex)
    V[:2, :2] = np.linalg.eigh(X[:2, :2])[1]
    Xd = V.conj().T @ X @ V
    max_dev_a = max(max_dev_a, abs(literal(p, Xd) - s) / s)
    lit_gap = max(lit_gap, abs(literal(p, X) - s) / s)
report("T2a 200 degenerate commuting samples: SLD = BKM = Tr(rho^-1 X^2)", max_dev_b < 1e-7,
       f"max rel dev={max_dev_b:.2e}")
report("T2b same samples: corrected (a) in a joint eigenbasis", max_dev_a < 1e-7,
       f"max rel dev={max_dev_a:.2e}")
report("CONTROL literal sentence on the same samples (fixed eigenbasis of rho0)", lit_gap < 1e-7,
       f"max rel dev={lit_gap:.3f}", expect=False)

# ---------------------------------------------------------------- T3: non-degenerate commuting: sentence holds
dev = 0.0
for _ in range(100):
    p = RNG.dirichlet([1, 1, 1])
    rho = np.diag(p).astype(complex)
    x = RNG.normal(size=3)
    x -= x.mean()
    X = np.diag(x).astype(complex)
    s, b = g_sld(rho, X), g_bkm_integral(rho, X)
    dev = max(dev, abs(s - literal(p, X)) / s, abs(b - literal(p, X)) / b)
report("T3 non-degenerate spectrum: commuting X is diagonal and sum X_ii^2/p_i holds", dev < 1e-7,
       f"max rel dev={dev:.2e}")

# ---------------------------------------------------------------- CONTROL: basis-free form for non-commuting X
p = np.array([0.25, 0.75])
rho = np.diag(p).astype(complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
s, b, bf = g_sld(rho, X), g_bkm_integral(rho, X), basis_free(rho, X)
report("CONTROL Tr(rho^-1 X^2) equals SLD and BKM for non-commuting X",
       abs(s - bf) < TOL and abs(b - bf) < TOL, f"SLD={s:.6f} BKM={b:.6f} Tr={bf:.6f}", expect=False)
report("T4 non-commuting p=(1/4,3/4), X=sigma_x: SLD = 4 < BKM (Lean witness_strict)",
       abs(s - 4) < TOL and b > s + 1e-6, f"SLD={s:.12f} BKM={b:.12f}")

print("failures:", failures)
sys.exit(1 if failures else 0)
