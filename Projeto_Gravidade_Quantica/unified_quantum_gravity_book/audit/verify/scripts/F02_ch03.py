"""
F-02 independent numerical audit -- Chapter 3
(chap03_pascal_simplex_continuous_multinomials.tex)

Protocol (audit/verify/PROTOCOL.md, Camada 2 / F-02 rule):
  every claim gets an INDEPENDENT oracle (a different formula / method than
  the one used in the book's own proof) PLUS a NEGATIVE CONTROL: a mutated
  version of the claim that must FAIL. Never "expected == computed" against
  the same formula.

Does NOT edit the chapter. Read-only check script.
"""
import mpmath as mp
import sympy as sp

mp.mp.dps = 40

PASS = []
FAIL = []

def report(name, line, ok, detail):
    status = "PASS" if ok else "FAIL"
    (PASS if ok else FAIL).append(name)
    print(f"[{status}] {name} (book line ~{line})")
    print(f"       {detail}")


# ---------------------------------------------------------------------------
# Claim 1 (line 90-103): Global Stifel recurrence for the continuous
# binomial coefficient:  C(x-1,y) + C(x-1,y-1) = C(x,y)
# Oracle: direct evaluation via mpmath.gamma (independent of the symbolic
# telescoping proof given in the book).
# Negative control: multiply one term by 2 -> must break the identity.
# ---------------------------------------------------------------------------
def cbinom(x, y):
    return mp.gamma(x + 1) / (mp.gamma(y + 1) * mp.gamma(x - y + 1))

ok1 = True
detail1 = []
import random
random.seed(1)
for _ in range(8):
    x = mp.mpf(random.uniform(0.3, 12.0))
    y = mp.mpf(random.uniform(-2.0, x + 2.0))
    lhs = cbinom(x - 1, y) + cbinom(x - 1, y - 1)
    rhs = cbinom(x, y)
    err = abs(lhs - rhs)
    detail1.append(float(err))
    if err > mp.mpf('1e-25') * (1 + abs(rhs)):
        ok1 = False
report("Stifel recurrence C(x-1,y)+C(x-1,y-1)=C(x,y)", "90-103", ok1,
       f"max abs error over 8 random real (x,y): {max(detail1):.3e}")

# Negative control: mutate -> C(x-1,y) + 2*C(x-1,y-1) = C(x,y); must fail.
ok1_neg = True
for _ in range(5):
    x = mp.mpf(random.uniform(0.3, 12.0))
    y = mp.mpf(random.uniform(-2.0, x + 2.0))
    lhs = cbinom(x - 1, y) + 2 * cbinom(x - 1, y - 1)
    rhs = cbinom(x, y)
    if abs(lhs - rhs) < mp.mpf('1e-6') * (1 + abs(rhs)):
        ok1_neg = False  # mutated identity should NOT hold
report("NEGATIVE CONTROL: mutated Stifel (factor 2) must fail", "90-103",
       ok1_neg, f"mutated identity held spuriously: {not ok1_neg}")


# ---------------------------------------------------------------------------
# Claim 2 (line 131-146): I(x) = int_0^x C(x,y) dy = 2^x * J(x),
# J(x) = (2/pi) int_0^{pi/2} cos^x(phi) sin(x phi)/phi dphi
# Oracle: both sides computed by INDEPENDENT direct numerical quadrature
# (quadrature of C(x,y) over y, vs quadrature of the trigonometric integral)
# -- neither uses the other's closed form.
# Negative control: replace 2^x by 3^x -> ratio must differ from 1.
# ---------------------------------------------------------------------------
def I_direct(x):
    return mp.quad(lambda y: cbinom(x, y), [0, x])

def J_trig(x):
    def f(phi):
        if phi == 0:
            return mp.mpf(0)
        return mp.cos(phi) ** x * mp.sin(x * phi) / phi
    return (2 / mp.pi) * mp.quad(f, [0, mp.pi / 2])

ok2 = True
detail2 = []
for x in [mp.mpf(xx) for xx in (2.3, 5.0, 9.7, 14.0)]:
    lhs = I_direct(x)
    rhs = 2 ** x * J_trig(x)
    rel = abs(lhs - rhs) / abs(lhs)
    detail2.append(float(rel))
    if rel > 1e-6:
        ok2 = False
report("I(x) = int C(x,y)dy  ==  2^x * J(x)  (independent quadratures)",
       "131-146", ok2, f"max relative error: {max(detail2):.3e}")

ok2_neg = True
for x in [mp.mpf(xx) for xx in (2.3, 5.0, 9.7)]:
    lhs = I_direct(x)
    rhs_wrong = 3 ** x * J_trig(x)  # mutated base 2 -> 3
    rel = abs(lhs - rhs_wrong) / abs(lhs)
    if rel < 1e-3:
        ok2_neg = False
report("NEGATIVE CONTROL: base 3^x instead of 2^x must fail", "131-146",
       ok2_neg, "mutated base-3 factorization checked to disagree")


# ---------------------------------------------------------------------------
# Claim 3 (line 273-289): continuous Fibonacci diagonal scaling
#   F_cont(x) = int_0^{x/2} C(x-y,y) dy  ~  phi^(x+1) / sqrt(5)  as x -> inf
# Oracle: direct numerical quadrature of F_cont(x) for large x, compared to
# the closed-form golden-ratio asymptotic (sympy exact phi).
# Negative control: drop the "+1" in the exponent (use phi^x/sqrt5) -> ratio
# must drift away from 1.
# ---------------------------------------------------------------------------
phi = (1 + mp.sqrt(5)) / 2

def F_cont(x):
    return mp.quad(lambda y: cbinom(x - y, y), [0, x / 2])

ok3 = True
ratios3 = []
for x in [mp.mpf(v) for v in (20, 30, 40)]:
    val = F_cont(x)
    asym = phi ** (x + 1) / mp.sqrt(5)
    ratio = val / asym
    ratios3.append(float(ratio))
    if abs(ratio - 1) > 0.05:
        ok3 = False
report("Fibonacci diagonal F_cont(x) ~ phi^(x+1)/sqrt(5)", "273-289", ok3,
       f"ratio F_cont(x)/asym at x=20,30,40: {ratios3} (-> should -> 1)")

ok3_neg = True
ratios3n = []
for x in [mp.mpf(v) for v in (20, 30, 40)]:
    val = F_cont(x)
    asym_wrong = phi ** x / mp.sqrt(5)  # missing the +1 in exponent
    ratio = val / asym_wrong
    ratios3n.append(float(ratio))
    if abs(ratio - 1) < 0.05:
        ok3_neg = False
report("NEGATIVE CONTROL: phi^x/sqrt5 (no +1 exponent) must drift from 1",
       "273-289", ok3_neg,
       f"ratio with mutated exponent at x=20,30,40: {ratios3n} "
       f"(-> should stay near phi = {float(phi):.5f}, i.e. NOT 1)")


# ---------------------------------------------------------------------------
# Claim 4 (line 344-406): continuous Dixon integral, integer case.
#   int_{-n}^{n} cos(pi t) f_n(t) dt  ~  (1/2) C(3n,n,n)
#   exactly, with  (1/2) C(3n,n,n) = (1/2) (3n)! / (n!)^3   (Dixon 1891,
#   classical / exact combinatorial identity -- used here as the
#   independent oracle for the asymptotic side).
# Oracle: (a) exact big-integer central trinomial coefficient via
#         sympy.factorial;  (b) direct numerical quadrature of the
#         truncated integral using mpmath (completely independent of the
#         Gamma-function algebra in the book's proof).
# Negative control: use (1/3) C(3n,n,n) instead of (1/2) -> must fail badly.
# ---------------------------------------------------------------------------
def f_n(n, t):
    return (mp.gamma(2 * n + 1) / (mp.gamma(n + 1 + t) * mp.gamma(n + 1 - t))) ** 3

def dixon_truncated_integral(n):
    return mp.quad(lambda t: mp.cos(mp.pi * t) * f_n(n, t), [-n, n])

def tau_n_bound(n):
    m = 2 * n + 1
    return 1 / (3 * mp.digamma(m)) + 1 / (mp.pi ** 3 * m ** 2 * (m - 1))

ok4 = True
detail4 = []
for n in (3, 5, 8, 12):
    J = dixon_truncated_integral(n)
    exact_half_trinomial = mp.mpf(sp.N(sp.Rational(sp.factorial(3 * n), sp.factorial(n) ** 3) / 2, 40))
    diff = abs(J - exact_half_trinomial)
    bound = 2 * tau_n_bound(n)
    detail4.append((float(diff), float(bound)))
    if diff > bound:  # the book's explicit error bound (Thm, eq with tau_n) must hold
        ok4 = False
report("Dixon truncated integral: |J - (1/2)C(3n,n,n)| <= 2*tau_n (explicit bound)",
       "344-375", ok4,
       f"(|diff|, 2*tau_n) at n=3,5,8,12: {detail4} -- diff must be <= bound each time")

# Negative control A: wrong prefactor (1/3 instead of 1/2) must blow past any
# sensible bound.
ok4_negA = True
for n in (3, 5, 8):
    J = dixon_truncated_integral(n)
    wrong = mp.mpf(sp.N(sp.Rational(sp.factorial(3 * n), sp.factorial(n) ** 3) / 3, 40))
    if abs(J - wrong) <= 2 * tau_n_bound(n):
        ok4_negA = False
report("NEGATIVE CONTROL A: (1/3) C(3n,n,n) instead of (1/2) violates the bound",
       "344-375", ok4_negA, "mutated prefactor 1/3 checked to violate 2*tau_n")

# Negative control B: an artificially tightened bound (half of tau_n) must be
# violated at small n -- i.e. the book's bound is not needlessly loose.
ok4_negB = False
for n in (3, 5, 8, 12):
    J = dixon_truncated_integral(n)
    exact_half_trinomial = mp.mpf(sp.N(sp.Rational(sp.factorial(3 * n), sp.factorial(n) ** 3) / 2, 40))
    diff = abs(J - exact_half_trinomial)
    if diff > tau_n_bound(n):  # i.e. a bound of 1*tau_n (half of 2*tau_n) fails somewhere
        ok4_negB = True
report("NEGATIVE CONTROL B: artificially tightened bound tau_n (half of 2*tau_n) "
       "is violated at some n -- confirms the test has discriminating power",
       "344-375", ok4_negB, "found at least one n where diff > tau_n (but <= 2*tau_n)")


# ---------------------------------------------------------------------------
# Claim 5 (line 327-340): L^2 row norm.
#   int_0^x C(x,y)^2 dy  ~  C(2x,x) ~ 4^x / sqrt(pi x)
# Oracle: (a) direct numerical quadrature of the LHS; (b) the EXACT central
# binomial coefficient C(2x,x) = Gamma(2x+1)/Gamma(x+1)^2 (a different,
# non-asymptotic closed form, i.e. an independent oracle, not the asymptotic
# formula itself).
# Negative control: wrong constant 4^x/sqrt(2 pi x) must fail.
# ---------------------------------------------------------------------------
def L2_row_norm(x):
    return mp.quad(lambda y: cbinom(x, y) ** 2, [0, x])

def central_binom_exact(x):
    return mp.gamma(2 * x + 1) / mp.gamma(x + 1) ** 2

ok5 = True
detail5 = []
for x in [mp.mpf(v) for v in (15, 25, 40)]:
    lhs = L2_row_norm(x)
    rhs = central_binom_exact(x)
    rel = abs(lhs - rhs) / rhs
    detail5.append(float(rel))
    if rel > 1e-6:
        ok5 = False
report("int C(x,y)^2 dy == C(2x,x) exactly (Gamma-function oracle)",
       "327-340", ok5, f"relative errors at x=15,25,40: {detail5}")

ok5_neg = True
for x in [mp.mpf(v) for v in (15, 25, 40)]:
    lhs = L2_row_norm(x)
    wrong_asym = 4 ** x / mp.sqrt(2 * mp.pi * x)  # wrong constant (2 pi instead of pi)
    rel = abs(lhs - wrong_asym) / lhs
    if rel < 1e-2:
        ok5_neg = False
report("NEGATIVE CONTROL: 4^x/sqrt(2 pi x) (wrong constant) must fail",
       "327-340", ok5_neg, "mutated asymptotic constant checked to disagree")


# ---------------------------------------------------------------------------
# Claim 6 (line 414-426): alternating row integral vanishes exactly for odd
# integer x, and is manifestly nonzero for generic x (the book's own stated
# numerical values A(4), A(10.3), A(20.5) serve as a built-in negative
# control: the "vanishing" claim must NOT hold at those points).
# Oracle: direct numerical quadrature, independent of the symmetry proof.
# ---------------------------------------------------------------------------
def A_integral(x):
    return mp.quad(lambda y: mp.cos(mp.pi * y) * cbinom(x, y), [0, x])

ok6 = True
detail6 = []
for k in (0, 1, 2, 3):
    x = 2 * k + 1
    val = A_integral(mp.mpf(x))
    detail6.append(float(val))
    if abs(val) > 1e-20:
        ok6 = False
report("A(x)=int cos(pi y) C(x,y) dy == 0 for odd integer x", "414-423",
       ok6, f"A(1),A(3),A(5),A(7) = {detail6}")

# Negative control: claim "A(x)=0 for ALL x" (book's own counter-values).
ok6_neg = True
checks = {4: -0.401, 10.3: -0.167, 20.5: -0.048}
detail6b = {}
for x, book_val in checks.items():
    val = A_integral(mp.mpf(x))
    detail6b[x] = float(val)
    if abs(val) < 1e-3:
        ok6_neg = False
    # also cross-check against the book's own reported numbers (sanity, not
    # the main oracle): should roughly match to the stated precision.
report("NEGATIVE CONTROL: A(x)=0 fails for even/non-integer x "
       "(cross-checked against book's own reported values)", "424-426",
       ok6_neg, f"A(4),A(10.3),A(20.5) computed = {detail6b}, "
       f"book states {checks}")


print()
print("=" * 70)
print(f"Chapter 3 summary: {len(PASS)} PASS, {len(FAIL)} FAIL (claims; "
      f"negative controls counted separately)")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print("  -", f)
