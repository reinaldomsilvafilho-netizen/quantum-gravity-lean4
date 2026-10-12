"""
L1 check, book ch. 2, thm:continuous_path_integral (ii), sharpness example.
File: unified_quantum_gravity_book/chap02_geometric_flows_tensor_varieties.tex

Claim (book): for r = 1, A == 0, R_j == M, the error |Z_k - Tr Pexp| equals
(1 + M/k^2)^k - 1, exceeds M/k for every k >= 2, and is at most (M/k) e^{M/k}.

Finding under adjudication (writer of Lean batch LIVRO_A_B5): the sentence
needs M > 0; at M = 0 the error is 0 = M/k, so "exceeds" fails.

Oracle: Z_k is computed from its definition, the trace of the ordered product
of the k scalar cores A_j = 1 + (1/k)*0 + (1/k^2)*M, with mpmath at 50 digits,
and the holonomy of A == 0 is 1 (U' = 0, U(0) = 1). The closed form is never
used on the oracle side. Inequalities are checked with exact rationals for
the strict lower bound and with mpmath for the exponential upper bound.

Negative controls (must FAIL):
  C1  M = 0, k = 2: strict inequality error > M/k.
  C2  k = 1, M = 1: strict inequality (equality holds, so strict fails).
  C3  the bound without the factor e^{M/k}: error <= M/k.
"""
from fractions import Fraction
import sys

import mpmath as mp

mp.mp.dps = 50


def to_mpf(M):
    M = Fraction(M)
    return mp.mpf(M.numerator) / M.denominator


def Z_k_oracle(M, k):
    # ordered product of the k cores, from the definition eq:transfer_generator
    M = to_mpf(M)
    prod = mp.mpf(1)
    for _ in range(k):
        core = mp.mpf(1) + mp.mpf(1) / k * 0 + mp.mpf(1) / k**2 * M
        prod = core * prod
    return prod  # r = 1: Tr = the scalar itself


def closed_form(M, k):
    return (1 + to_mpf(M) / k**2) ** k - 1


def error_exact(M, k):
    M = Fraction(M)
    return (1 + M / k**2) ** k - 1


results = []


def check(name, ok, detail, control=False):
    tag = "CONTROL-" + ("FAIL" if not ok else "PASS") if control else ("PASS" if ok else "FAIL")
    print(f"{tag:13s} {name}: {detail}")
    results.append((name, ok, control))


Ms = [Fraction(1, 100), Fraction(1, 2), 1, 2, 5, 10, 50]
ks = list(range(2, 41))

# 1. closed form equals the oracle (holonomy of A == 0 is 1)
worst = mp.mpf(0)
for M in Ms:
    for k in ks:
        d = abs((Z_k_oracle(M, k) - 1) - closed_form(M, k))
        worst = max(worst, d)
check("closed form = Z_k - 1 (oracle: ordered product)", worst < mp.mpf("1e-40"),
      f"max |diff| = {mp.nstr(worst, 5)} over {len(Ms)}x{len(ks)} cases")

# 2. strict lower bound, exact rationals, M > 0, k >= 2
bad = [(M, k) for M in Ms for k in ks if not (error_exact(M, k) > Fraction(M) / k)]
check("error > M/k for M > 0, k >= 2 (exact)", not bad, f"violations: {bad}")

# 3. upper bound (M/k) e^{M/k}
bad = []
margin = mp.mpf("inf")
for M in Ms:
    for k in ks:
        lhs = closed_form(M, k)
        rhs = to_mpf(M) / k * mp.e ** (to_mpf(M) / k)
        margin = min(margin, rhs - lhs)
        if not (lhs <= rhs):
            bad.append((M, k))
check("error <= (M/k) e^{M/k}", not bad, f"violations: {bad}; min slack = {mp.nstr(margin, 5)}")

# 4. the degenerate case the finding is about
e0 = error_exact(0, 2)
check("M = 0: error is exactly 0 = M/k (so 'exceeds' fails)", e0 == 0,
      f"error(M=0,k=2) = {e0}")

# Negative controls
check("C1 strict bound at M = 0, k = 2", error_exact(0, 2) > Fraction(0) / 2,
      f"{error_exact(0, 2)} > 0 ?", control=True)
check("C2 strict bound at k = 1, M = 1", error_exact(1, 1) > Fraction(1) / 1,
      f"{error_exact(1, 1)} > 1 ?", control=True)
c3 = all(closed_form(M, k) <= to_mpf(M) / k for M in Ms for k in ks)
check("C3 bound without e^{M/k}: error <= M/k", c3,
      f"e.g. M=1,k=2: {mp.nstr(closed_form(1, 2), 6)} <= 0.5 ?", control=True)

fails = [n for n, ok, c in results if not c and not ok]
ctrl_pass = [n for n, ok, c in results if c and ok]
print()
print("SUMMARY:", "ALL PASS" if not fails and not ctrl_pass else "PROBLEM",
      f"| failing checks: {fails} | controls that passed (bad): {ctrl_pass}")
sys.exit(0 if not fails and not ctrl_pass else 1)
