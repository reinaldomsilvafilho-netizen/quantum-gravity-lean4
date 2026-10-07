"""
Independent check of the claim in audit/references_audit.md:

  "Open problem 1 looks trivially solvable."
  min_pi in S_n  sum_{i,j} (pi(i)^2 + pi(j)^2) a_ij^2
  = min_pi sum_i pi(i)^2 w_i,  w_i = sum_j (a_ij^2 + a_ji^2)

  solved exactly by the rearrangement inequality: pair the largest w_i
  with the smallest square 1, the second largest with 4, etc.

Method (independent oracle): brute force over ALL n! permutations for n<=8,
computing the objective directly from A (no use of the w_i decomposition,
no use of sorting) via itertools.permutations. Compare the brute-force
minimum against the value produced by the sort-based formula.

Negative control: a permutation that is NOT the sorted one must give a
strictly larger objective on a random instance (checked by picking the
worst-scoring non-optimal permutation found during brute force and
confirming it exceeds the sorted value).
"""
import itertools
import numpy as np
import sys

rng = np.random.default_rng(20261007)

def objective_direct(A, perm):
    # perm is a tuple with perm[i] = pi(i), using 1-indexed values 1..n
    n = A.shape[0]
    total = 0.0
    for i in range(n):
        for j in range(n):
            total += (perm[i]**2 + perm[j]**2) * A[i, j]**2
    return total

def brute_force_min(A):
    n = A.shape[0]
    best = None
    best_perm = None
    worst_nonopt = None
    worst_nonopt_perm = None
    for p in itertools.permutations(range(1, n + 1)):
        val = objective_direct(A, p)
        if best is None or val < best:
            best = val
            best_perm = p
    # find a non-optimal permutation (differs from best_perm) to serve as
    # the negative-control candidate; take one that's just a transposition
    # away from best_perm so it's a "plausible but wrong" guess
    for p in itertools.permutations(range(1, n + 1)):
        if p != best_perm:
            val = objective_direct(A, p)
            if worst_nonopt is None or val < worst_nonopt:
                # we want the BEST among non-optimal perms (hardest negative
                # control: the closest competitor to the true optimum)
                worst_nonopt = val
                worst_nonopt_perm = p
    return best, best_perm, worst_nonopt, worst_nonopt_perm

def sort_formula_min(A):
    n = A.shape[0]
    w = np.array([sum(A[i, j]**2 + A[j, i]**2 for j in range(n)) for i in range(n)])
    # rearrangement inequality: pair largest w with smallest square 1^2,...,n^2
    order = np.argsort(-w)  # indices sorted by w descending
    squares = np.array([k**2 for k in range(1, n + 1)])  # ascending 1,4,9,...
    val = 0.0
    perm = [0] * n
    for rank, idx in enumerate(order):
        perm[idx] = rank + 1  # pi(idx) = rank+1 (1-indexed), smallest squares to largest w
        val += squares[rank] * w[idx]
    return val, tuple(perm)

def mutated_formula_min(A):
    """Negative control formula: pair largest w with LARGEST square instead
    of smallest (the wrong rearrangement direction). This mutated formula
    must FAIL to match the brute-force minimum in general."""
    n = A.shape[0]
    w = np.array([sum(A[i, j]**2 + A[j, i]**2 for j in range(n)) for i in range(n)])
    order = np.argsort(-w)  # descending w
    squares = np.array([k**2 for k in range(1, n + 1)])  # ascending
    # WRONG pairing: largest w with largest square (similarly sorted -> maximizes, not minimizes)
    val = 0.0
    perm = [0] * n
    for rank, idx in enumerate(order):
        sq_rank = n - 1 - rank  # largest square to largest w
        perm[idx] = sq_rank + 1
        val += squares[sq_rank] * w[idx]
    return val, tuple(perm)

def run_case(n, trial, tol=1e-9):
    A = rng.normal(size=(n, n))
    brute_min, brute_perm, best_nonopt, best_nonopt_perm = brute_force_min(A)
    sort_min, sort_perm = sort_formula_min(A)
    mutated_min, mutated_perm = mutated_formula_min(A)

    ok_match = abs(brute_min - sort_min) < tol * max(1.0, abs(brute_min))
    # negative control 1: the mutated (wrong-direction) formula must NOT
    # match the brute-force minimum, except in degenerate symmetric cases.
    mutated_fails = abs(mutated_min - brute_min) > tol * max(1.0, abs(brute_min))
    # negative control 2: the best non-optimal permutation found by brute
    # force must be strictly worse than the sorted optimum.
    nonopt_worse = (best_nonopt is None) or (best_nonopt > sort_min + tol * max(1.0, abs(sort_min)))

    print(f"n={n} trial={trial}: brute_min={brute_min:.6f} sort_min={sort_min:.6f} "
          f"match={ok_match} mutated_min={mutated_min:.6f} mutated_fails_as_expected={mutated_fails} "
          f"best_nonopt={best_nonopt:.6f} nonopt_strictly_worse={nonopt_worse}")

    return ok_match, mutated_fails, nonopt_worse

def main():
    failures = 0
    trials_per_n = {2: 3, 3: 3, 4: 3, 5: 2, 6: 2, 7: 1, 8: 1}
    for n, ntrials in trials_per_n.items():
        for t in range(ntrials):
            ok_match, mutated_fails, nonopt_worse = run_case(n, t)
            if not ok_match:
                print(f"FAIL: brute force vs sort formula mismatch at n={n} trial={t}")
                failures += 1
            if n >= 3 and not mutated_fails:
                # for n<=2 the two squares {1,4} are forced into one pairing
                # up to symmetry when w_1==w_2, so skip strictness there
                print(f"FAIL: negative control (mutated formula) unexpectedly matched at n={n} trial={t}")
                failures += 1
            if not nonopt_worse:
                print(f"FAIL: negative control (non-optimal permutation) not strictly worse at n={n} trial={t}")
                failures += 1

    # Degenerate case by hand: n=1. Only one permutation exists (pi(1)=1),
    # objective = 2*1^2*a_11^2, trivially the (only, hence optimal) value.
    A1 = np.array([[2.5]])
    brute_min1, _, _, _ = brute_force_min(A1)
    sort_min1, _ = sort_formula_min(A1)
    print(f"n=1 degenerate: brute={brute_min1:.6f} sort={sort_min1:.6f}")
    if abs(brute_min1 - sort_min1) > 1e-9:
        print("FAIL: n=1 degenerate case mismatch")
        failures += 1

    with open('verify_op1_sorting.out.txt', 'w') as f:
        f.write(f"failures={failures}\n")

    print(f"TOTAL FAILURES: {failures}")
    sys.exit(failures)

if __name__ == '__main__':
    main()
