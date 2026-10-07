"""L2r (release re-check) of Prop. 'Optimal permutation for the Dirichlet energy' (BtS I).

Independent of verify_op1_sorting.py (not read before writing this).
Oracle chain:
  (a) E(f_B) by grid quadrature of |grad f_B|^2 on the torus (exact for trig
      polynomials when the grid has M > n-1 points per axis; we use 2n+3), checked against
      ||DB||^2+||BD||^2 on random instances;
  (b) brute force over all n! permutation MATRICES P (built explicitly,
      P e_j = e_{pi(j)}), B = P A P^T, n = 1..8;
  (c) claimed minimum sum_k k^2 w_{tau(k)} and claimed minimizer pi = tau^{-1}.
Negative controls (must fail): ascending pairing; row-only weights; pi = tau
instead of tau^{-1}; claimed 'QAP-hard' i.e. minimum != sorted value is never
observed so we also test a mutated energy with a genuinely coupled coefficient
(i*j instead of i^2+j^2), for which sorting must NOT always give the optimum.
Seed 20261007. Exit code = number of failures.
"""
import itertools
import sys

import numpy as np

SEED = 20261007
rng = np.random.default_rng(SEED)
out = []
fail = 0


def log(s):
    out.append(s)
    print(s)


def perm_matrix(p):
    n = len(p)
    P = np.zeros((n, n))
    for j in range(n):
        P[p[j], j] = 1.0  # P e_j = e_{p(j)}
    return P


def energy_matrix(B):
    n = B.shape[0]
    D = np.diag(np.arange(1, n + 1, dtype=float))
    return np.linalg.norm(D @ B) ** 2 + np.linalg.norm(B @ D) ** 2


def energy_grid(B, M=None):
    """Dirichlet energy by quadrature of |grad f|^2, f = sum a_k e^{i(k1 x1 + k2 x2)}."""
    n = B.shape[0]
    M = M or (2 * n + 3)
    x = 2 * np.pi * np.arange(M) / M
    X1, X2 = np.meshgrid(x, x, indexing="ij")
    k = np.arange(1, n + 1)
    f1 = np.zeros_like(X1, dtype=complex)
    f2 = np.zeros_like(X1, dtype=complex)
    for a in range(n):
        for b in range(n):
            e = np.exp(1j * (k[a] * X1 + k[b] * X2))
            f1 += 1j * k[a] * B[a, b] * e
            f2 += 1j * k[b] * B[a, b] * e
    return float(np.mean(np.abs(f1) ** 2 + np.abs(f2) ** 2))


# (a) quadrature oracle vs matrix formula
for n in range(1, 6):
    ok = True
    for _ in range(3):
        A = rng.standard_normal((n, n))
        eg, em = energy_grid(A), energy_matrix(A)
        ok = ok and abs(eg - em) <= 1e-9 * max(1, em)
    fail += not ok
    log(f"(a) n={n}: grid quadrature == ||DA||^2+||AD||^2 : {'ok' if ok else 'FAIL'}")
# negative control for (a): aliased grid (M = 2 < n, frequency differences up to n-1 alias)
A = rng.standard_normal((4, 4))
bad = abs(energy_grid(A, M=2) - energy_matrix(A)) > 1e-6
log(f"(a-neg) aliased grid M=2 disagrees: {'ok (control fails as expected)' if bad else 'FAIL'}")
fail += not bad


def claimed(A):
    w = (A ** 2).sum(1) + (A ** 2).sum(0)
    tau = np.argsort(-w, kind="stable")  # tau[k-1] = index with k-th largest w
    val = sum((k + 1) ** 2 * w[tau[k]] for k in range(len(w)))
    tau_inv = np.empty_like(tau)
    tau_inv[tau] = np.arange(len(w))
    return val, tau, tau_inv, w


neg = {"ascending": 0, "row_only": 0, "pi_eq_tau": 0, "coupled_ij": 0}
neg_cases = 0
coupled_cases = 0
ninst = 0
for n in range(1, 9):
    reps = 6 if n <= 6 else (3 if n == 7 else 2)
    for r in range(reps):
        if r == 0 and n >= 3:
            A = rng.integers(-1, 2, size=(n, n)).astype(float)  # ties likely
        else:
            A = rng.standard_normal((n, n))
        ninst += 1
        best = np.inf
        best_ij = np.inf
        Ws = np.arange(1, n + 1, dtype=float)
        for p in itertools.permutations(range(n)):
            P = perm_matrix(p)
            B = P @ A @ P.T
            e = energy_matrix(B)
            best = min(best, e)
            # mutated, genuinely coupled energy sum_ij i*j*b_ij^2
            best_ij = min(best_ij, float(Ws @ (B ** 2) @ Ws))
        val, tau, tau_inv, w = claimed(A)
        # claimed minimizer pi = tau^{-1}: pi(i) = position of i in tau (0-based)
        e_min = energy_matrix(perm_matrix(tau_inv) @ A @ perm_matrix(tau_inv).T)
        tol = 1e-9 * max(1.0, best)
        ok = abs(val - best) <= tol and abs(e_min - best) <= tol
        fail += not ok
        log(f"(b) n={n} rep={r}: brute={best:.10g} claimed={val:.10g} E(pi=tau^-1)={e_min:.10g} {'ok' if ok else 'FAIL'}")
        if n >= 2 and np.ptp(w) > 1e-12:
            neg_cases += 1
            # mutation 1: ascending pairing
            asc = np.argsort(w, kind="stable")
            v_asc = sum((k + 1) ** 2 * w[asc[k]] for k in range(n))
            neg["ascending"] += abs(v_asc - best) > tol
            # mutation 2: row-only weights
            wr = (A ** 2).sum(1)
            t2 = np.argsort(-wr, kind="stable")
            ti2 = np.empty_like(t2)
            ti2[t2] = np.arange(n)
            e2 = energy_matrix(perm_matrix(ti2) @ A @ perm_matrix(ti2).T)
            neg["row_only"] += abs(e2 - best) > tol
            # mutation 3: pi = tau instead of tau^{-1}
            e3 = energy_matrix(perm_matrix(tau) @ A @ perm_matrix(tau).T)
            neg["pi_eq_tau"] += abs(e3 - best) > tol
        if n >= 3:
            coupled_cases += 1
            # sorting heuristic for coupled energy: same sorted-weight permutation
            Bt = perm_matrix(tau_inv) @ A @ perm_matrix(tau_inv).T
            v_ij = float(Ws @ (Bt ** 2) @ Ws)
            neg["coupled_ij"] += abs(v_ij - best_ij) > 1e-9 * max(1, best_ij)

log(f"instances: {ninst}")
log(f"negative-control detections over {neg_cases} non-degenerate instances: "
    f"ascending={neg['ascending']}, row_only={neg['row_only']}, pi=tau={neg['pi_eq_tau']}")
log(f"coupled i*j energy (genuine QAP-type): sorting misses optimum in {neg['coupled_ij']}/{coupled_cases}")
# Requirements: ascending must fail in every non-degenerate case;
# row_only, pi=tau and coupled must fail at least once (they can coincide by chance).
if neg["ascending"] != neg_cases:
    fail += 1
    log("FAIL: ascending control did not always fail")
for key in ("row_only", "pi_eq_tau", "coupled_ij"):
    if neg[key] == 0:
        fail += 1
        log(f"FAIL: control {key} never detected")
log(f"failures={fail}")
with open(__file__.replace(".py", ".out.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
sys.exit(fail)
