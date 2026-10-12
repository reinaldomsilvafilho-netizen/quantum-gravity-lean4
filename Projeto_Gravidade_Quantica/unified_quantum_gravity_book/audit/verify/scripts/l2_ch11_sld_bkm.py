"""L2 independent re-check of F-62 (chap11, rem:sld_vs_bkm, corrected sentence).

Corrected book sentence under test (chap11_emergent_spacetime_tensor_networks_holonomies.tex,
l. 159): "... with equality if and only if X_ij = 0 whenever p_i != p_j, i.e. [rho0, X] = 0;
in that case both equal Tr(rho0^{-1}X^2), which in an eigenbasis of rho0 that also
diagonalizes X is the classical Fisher-Rao metric sum_i X_ii^2/p_i."

This script is independent of audit/verify/scripts/l1_ch11_sld_bkm.py:
  * it does NOT use scipy.linalg.solve_sylvester, scipy.integrate.quad, or logm;
  * its oracle is the direct eigenbasis double sum that defines g^SLD and g^BKM in the
    remark itself (g^SLD = sum_ij 2/(p_i+p_j)|X_ij|^2, g^BKM = sum_ij m(p_i,p_j)|X_ij|^2,
    m(a,b) = (log a - log b)/(a-b), m(a,a)=1/a), evaluated after diagonalising a RANDOM
    (non-diagonal) rho0 with `numpy.linalg.eigh`, never assuming rho0 is given diagonal;
  * X is built to commute with rho0 by construction (block-diagonal in rho0's own
    eigenbasis, rotated by rho0's own eigenvectors), not by solving any equation.

Negative controls (must FAIL):
  (a) the corrected basis-free value with the WRONG power, Tr(rho0^{-2} X^2), against the
      double-sum oracle (mutation of the exponent in the corrected sentence);
  (b) the final clause "= sum_i X_ii^2/p_i" evaluated in an eigenbasis of rho0 that does
      NOT also diagonalize X (the exact failure mode F-62 reports), for degenerate rho0.

Exit code is non-zero if a required test fails or a negative control passes.
"""
import sys

import numpy as np

RNG = np.random.default_rng(5562026)
TOL = 1e-9
failures = 0


def report(name, ok, detail, expect=True):
    global failures
    ok = bool(ok)
    if expect:
        tag = "PASS" if ok else "FAIL"
        failures += 0 if ok else 1
    else:
        tag = "PASS (control fails as required)" if not ok else "FAIL (control passed: no power)"
        failures += 0 if not ok else 1
    print(f"{tag}: {name} | {detail}")


def logmean(a, b):
    if abs(a - b) < 1e-13:
        return 1.0 / a
    return (np.log(a) - np.log(b)) / (a - b)


def g_sum(p, X, mode):
    """Double-sum formula from the remark itself, in the basis where X is given and p is diag."""
    n = len(p)
    tot = 0.0
    for i in range(n):
        for j in range(n):
            w = (2.0 / (p[i] + p[j])) if mode == "sld" else logmean(p[i], p[j])
            tot += w * abs(X[i, j]) ** 2
    return tot


def basis_free(rho0, X, power=1):
    rho_inv = np.linalg.matrix_power(np.linalg.inv(rho0), power)
    return float(np.real(np.trace(rho_inv @ X @ X)))


def literal_diag(p, X):
    return float(sum(np.real(X[i, i]) ** 2 / p[i] for i in range(len(p))))


def random_degenerate_rho_and_commuting_X(n_block, n_rest, seed_shift):
    """rho0 with a repeated eigenvalue block of size n_block (+ n_rest simple ones), a
    random eigenbasis U, and X built block-diagonal in THAT basis (so [rho0,X]=0 by
    construction) but with the off-diagonal part inside the degenerate block kept, i.e.
    X is not required to be diagonal in rho0's eigenbasis."""
    n = n_block + n_rest
    p_block = RNG.uniform(0.05, 0.2)
    p_rest = np.sort(RNG.uniform(0.3, 1.0, size=n_rest))
    p = np.concatenate([[p_block] * n_block, p_rest])
    p = p / p.sum()
    A = RNG.normal(size=(n, n)) + 1j * RNG.normal(size=(n, n))
    U, _ = np.linalg.qr(A)
    rho0 = (U * p) @ U.conj().T
    rho0 = (rho0 + rho0.conj().T) / 2
    # X block-diagonal in the U-basis: a Hermitian block on the degenerate indices (not
    # necessarily diagonal) plus independent diagonal entries elsewhere -> commutes with rho0.
    Xb = RNG.normal(size=(n_block, n_block)) + 1j * RNG.normal(size=(n_block, n_block))
    Xb = (Xb + Xb.conj().T) / 2
    Xd = np.zeros((n, n), dtype=complex)
    Xd[:n_block, :n_block] = Xb
    for k in range(n_rest):
        Xd[n_block + k, n_block + k] = RNG.normal()
    X_eigbasis = Xd  # X in the U-eigenbasis of rho0
    X = U @ Xd @ U.conj().T  # X in the ambient basis
    return rho0, X, p, X_eigbasis, U


# ---------------------------------------------------------------- T1: oracle self-consistency
# Generic (non-commuting) random rho0, X: BKM >= SLD, both from the double-sum oracle after
# diagonalising a random rho0 (never given diagonal).
n = 4
p_vals = RNG.dirichlet(np.ones(n))
Uq, _ = np.linalg.qr(RNG.normal(size=(n, n)) + 1j * RNG.normal(size=(n, n)))
rho_generic = (Uq * p_vals) @ Uq.conj().T
rho_generic = (rho_generic + rho_generic.conj().T) / 2
Araw = RNG.normal(size=(n, n)) + 1j * RNG.normal(size=(n, n))
X_amb = (Araw + Araw.conj().T) / 2
w_eig, V_eig = np.linalg.eigh(rho_generic)
X_in_eig = V_eig.conj().T @ X_amb @ V_eig
bkm1 = g_sum(w_eig, X_in_eig, "bkm")
sld1 = g_sum(w_eig, X_in_eig, "sld")
report("T1 BKM >= SLD, double-sum oracle after diagonalising a random (non-diagonal) rho0",
       bkm1 >= sld1 - 1e-12, f"BKM={bkm1:.10f} SLD={sld1:.10f}")

# ---------------------------------------------------------------- T2: commuting degenerate case
for trial in range(50):
    rho0, X, p, X_eig, U = random_degenerate_rho_and_commuting_X(2, 2, trial)
    comm = np.linalg.norm(rho0 @ X - X @ rho0)
    if comm > 1e-9:
        report(f"T2.{trial} [rho0,X]=0 by construction", False, f"||comm||={comm:.2e}")
        continue
    w, V = np.linalg.eigh(rho0)
    Xw = V.conj().T @ X @ V
    bkm = g_sum(w, Xw, "bkm")
    sld = g_sum(w, Xw, "sld")
    tr = basis_free(rho0, X, power=1)
    ok = abs(bkm - sld) < 1e-7 * max(1, abs(sld)) and abs(bkm - tr) < 1e-7 * max(1, abs(tr))
    if trial == 0:
        report("T2 (sample) commuting degenerate rho0: SLD = BKM = Tr(rho0^-1 X^2)", ok,
               f"SLD={sld:.10f} BKM={bkm:.10f} Tr={tr:.10f}")
    if not ok:
        failures += 1
        print(f"FAIL: T2.{trial} mismatch SLD={sld} BKM={bkm} Tr={tr}")

# ---------------------------------------------------------------- T3: final clause needs a JOINT eigenbasis
rho0, X, p, X_eig, U = random_degenerate_rho_and_commuting_X(3, 1, 999)
w, V = np.linalg.eigh(rho0)  # an eigenbasis of rho0 -- not guaranteed to diagonalise X
Xw = V.conj().T @ X @ V
sld_val = g_sum(w, Xw, "sld")
lit_arbitrary = literal_diag(w, Xw)
# a joint eigenbasis: diagonalise the degenerate block of Xw separately
wX_block, VX_block = np.linalg.eigh(Xw[:3, :3])
Vjoint = np.eye(4, dtype=complex)
Vjoint[:3, :3] = VX_block
Xjoint = Vjoint.conj().T @ Xw @ Vjoint
lit_joint = literal_diag(w, Xjoint)
report("T3a joint eigenbasis: sum_i X_ii^2/p_i = common value", abs(lit_joint - sld_val) < 1e-7,
       f"literal(joint)={lit_joint:.10f} common value={sld_val:.10f}")
report("CONTROL (b): final clause in an eigenbasis of rho0 that does NOT diagonalise X "
       "(degenerate block kept off-diagonal)", abs(lit_arbitrary - sld_val) < 1e-7,
       f"literal(arbitrary)={lit_arbitrary:.6f} vs common value={sld_val:.6f}", expect=False)

# ---------------------------------------------------------------- CONTROL (a): wrong power mutant
tr_wrong_power = basis_free(rho0, X, power=2)  # Tr(rho0^-2 X^2), mutated exponent
report("CONTROL (a): mutated basis-free value Tr(rho0^-2 X^2) equals the common value",
       abs(tr_wrong_power - sld_val) < 1e-7, f"Tr(rho0^-2 X^2)={tr_wrong_power:.6f} vs {sld_val:.6f}",
       expect=False)

print("failures:", failures)
sys.exit(1 if failures else 0)
