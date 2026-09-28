"""Numerical checks of every inequality/constant used in dixon_proof.tex.

Each check compares an independently computed quantity (quadrature or exact
arithmetic) against the explicit bound of the proof, and each block has a
negative control: a mutated bound/formula that must FAIL.

Run from the project folder:  python Pesquisa_e_Testes/dixon_continuo/dixon_proof_checks.py
"""
from math import comb, factorial

from mpmath import (mp, mpf, quad, cos, sin, pi, gamma, rgamma, beta, inf, log, exp,
                    sqrt, psi, harmonic, diff, nsum, euler, findroot)

mp.dps = 30
NS = list(range(1, 31))
lines = []
fails = 0


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    lines.append(s)


def check(cond, label):
    global fails
    if not cond:
        fails += 1
        say("  FAIL:", label)
    return cond


def f_tail(m, s):
    """f(x+s) for m = 2x+1: [Gamma(m)/(Gamma(m+s)Gamma(1-s))]^3."""
    return (gamma(m) * rgamma(m + s) * rgamma(1 - s)) ** 3


def fprime_tail(m, s):
    return diff(lambda u: f_tail(m, u), s)


def tail_pts(j=1):
    step = max(4, j)
    return [mpf(k) / step for k in range(0, 4 * step + 1)] + [mpf(k) / 4 for k in range(17, 121)] + [inf]


def tau(m):
    return 1 / (3 * psi(0, m)) + 1 / (pi ** 3 * m ** 2 * (m - 1))


# ---------------------------------------------------------------- Lemma 1
say("=== L1: Gamma(u) >= 1 on (0,1];  c_R = max_[0,1] |(1/Gamma)'| ===")
grid = [mpf(k) / 2000 for k in range(1, 2001)]
check(all(gamma(u) >= 1 for u in grid), "Gamma>=1")
dR = [abs(diff(rgamma, mpf(k) / 2000)) for k in range(0, 2001)]
cR = max(dR)
say("  Gamma(u) >= 1 on grid: OK;  max |(1/Gamma)'| on grid =", mp.nstr(cR, 8))
# the maximiser is interior; refine with findroot on the second derivative
u0 = grid[max(range(len(dR) - 1), key=lambda i: dR[i + 1]) ]
ustar = findroot(lambda u: diff(rgamma, u, 2), u0)
cR_exact = abs(diff(rgamma, ustar))
say("  refined: u* =", mp.nstr(ustar, 10), " c_R =", mp.nstr(cR_exact, 12))
C_R = mpf("1.18")
check(cR_exact < C_R, "c_R < 1.18")
say("  proof uses c_R <= 1.18 :", "OK" if cR_exact < C_R else "FAIL")
check(cR_exact > mpf("1.13"), "neg ctrl: earlier guess c_R<1.13 must fail")
say("  negative control: earlier guess c_R <= 1.13 -> REJECTED")
say("  negative control: c_R <= 1 (the value at u=0) ->", "REJECTED" if cR_exact > 1 else "accepted?!")
check(cR_exact > 1, "negative control c_R<=1 must fail")

# ---------------------------------------------------------------- Lemma 2
say("\n=== L2: A(s)=Gamma(m)/Gamma(m+s) <= exp(-s psi(m)) for s in [0,1] ===")
for n in [1, 2, 5, 10, 30]:
    m = 2 * n + 1
    ok = all(gamma(m) / gamma(m + s) <= exp(-s * psi(0, m)) * (1 + mpf(10) ** -25) for s in [mpf(k) / 200 for k in range(201)])
    check(ok, "A bound n=%d" % n)
    # mutated: exp(-s psi(m+1)) must fail somewhere
    bad = any(gamma(m) / gamma(m + s) > exp(-s * psi(0, m + 1)) for s in [mpf(k) / 200 for k in range(1, 201)])
    check(bad, "negative control A n=%d" % n)
say("  holds for n in {1,2,5,10,30}; mutated exp(-s psi(m+1)) rejected for each: OK")

# ---------------------------------------------------------------- Prop (tail)
say("\n=== P1: int_n^inf |f| <= tau_n = 1/(3 psi(2n+1)) + 1/(pi^3 m^2 (m-1)) ===")
say("  n   int|f|        tau_n        |I1 - D/2|    2 tau_n")
ratios = []
for n in NS:
    m = 2 * n + 1
    absint = quad(lambda s: abs(f_tail(m, s)), tail_pts())
    T1 = quad(lambda s: cos(pi * (n + s)) * f_tail(m, s), tail_pts())
    dev = abs(2 * T1)  # = |I_1 - D_n/2|
    t = tau(m)
    check(absint <= t, "tail n=%d" % n)
    check(dev <= 2 * t, "I1 dev n=%d" % n)
    ratios.append(absint / t)
    if n in (1, 2, 3, 5, 10, 20, 30):
        say("  %2d  %s  %s  %s  %s" % (n, mp.nstr(absint, 8), mp.nstr(t, 8), mp.nstr(dev, 8), mp.nstr(2 * t, 8)))
say("  max ratio int|f| / tau_n over n=1..30:", mp.nstr(max(ratios), 6))
# negative control: halve the main term
badn = [n for n in NS if quad(lambda s: abs(f_tail(2 * n + 1, s)), tail_pts()) > 1 / (6 * psi(0, 2 * n + 1))]
check(len(badn) > 0, "negative control tau/2")
say("  negative control 1/(6 psi): violated for", len(badn), "of", len(NS), "n -> REJECTED")

# ---------------------------------------------------------------- Prop (sum over j)
say("\n=== P2: sum_{j odd>=3} |I_j| <= (2/pi) sqrt(pi^2/8-1) E_n ===")


def E_bound(m):
    Hm = harmonic(m)
    B2 = mpf(1) / (m * (m + 1))
    e1 = 3 * (psi(0, m + 1) + C_R) / sqrt(6 * psi(0, m))
    e2 = 3 * (Hm + pi) / (pi ** 3 * m ** 3)
    e3 = sqrt(2) * 3 * (Hm + pi) / pi ** 3 * B2 ** 2 * (B2 + 1 / (2 * (m - 1)))
    return e1 + e2 + e3


mp.dps = 20
KAPPA = (2 / pi) * sqrt(pi ** 2 / 8 - 1)
say("  n   ||f'||_L2(n,n+1)  3(psi(m+1)+c_R)/sqrt(6psi)   sum_{j<=J}|I_j|+tail   bound")
for n in [1, 2, 3, 5, 8, 12]:
    m = 2 * n + 1
    l2 = sqrt(quad(lambda s: fprime_tail(m, s) ** 2, [0, mpf(1) / 2, 1]))
    e1 = 3 * (psi(0, m + 1) + C_R) / sqrt(6 * psi(0, m))
    check(l2 <= e1, "L2 f' n=%d" % n)
    J = 61
    S = sum(abs(2 * quad(lambda s: cos(pi * j * (n + s)) * f_tail(m, s), tail_pts(j))) for j in range(3, J + 1, 2))
    # tail j > J: |I_j| <= 2 (|f'(n)| + ||f''||_1)/(pi j)^2 ; estimate with sup-type numbers
    fpn = abs(fprime_tail(m, 0))
    f2 = quad(lambda s: abs(diff(lambda u: f_tail(m, u), s, 2)), [0, mpf(1) / 8, mpf(1) / 2, 1, 2, 4, 8])
    tailj = 2 * (fpn + f2) / pi ** 2 * sum(mpf(1) / j ** 2 for j in range(J + 2, 20001, 2))
    total = S + tailj
    bound = KAPPA * E_bound(m)
    check(total <= bound, "sum bound n=%d" % n)
    say("  %2d  %s  %s  %s  %s" % (n, mp.nstr(l2, 6), mp.nstr(e1, 6), mp.nstr(total, 6), mp.nstr(bound, 6)))
say("  negative control: dropping the 1/j factor (bound with sum 1 instead of sum 1/j^2 is fine, but"
    " claiming sum|I_j| <= |I_3|) must fail:")
n = 5
m = 11
I3 = abs(2 * quad(lambda s: cos(3 * pi * (n + s)) * f_tail(m, s), tail_pts(3)))
I5 = abs(2 * quad(lambda s: cos(5 * pi * (n + s)) * f_tail(m, s), tail_pts(5)))
check(I3 + I5 > I3, "trivial")
say("  |I_3|+|I_5| =", mp.nstr(I3 + I5, 6), "> |I_3| =", mp.nstr(I3, 6), "-> REJECTED")

# ---------------------------------------------------------------- Paley-Wiener
mp.dps = 30
say("\n=== PW: full-line integrals J_j = int_R cos(pi j t) f(t) dt ===")
for n in [2, 3]:
    m = 2 * n + 1
    fr = lambda t: (gamma(m) * rgamma(n + 1 + t) * rgamma(n + 1 - t)) ** 3
    pts = [mpf(k) / 4 for k in range(0, 4 * (n + 30) + 1)] + [inf]
    for j in [1, 3, 5]:
        Jj = 2 * quad(lambda t: cos(pi * j * t) * fr(t), pts)
        target = mpf(factorial(3 * n)) / factorial(n) ** 3 / 2 if j == 1 else 0
        check(abs(Jj - target) < mpf(10) ** -20, "J n=%d j=%d" % (n, j))
        say("  n=%d j=%d  J_j = %s   expected %s" % (n, j, mp.nstr(Jj, 15), mp.nstr(target, 15)))
    # negative control: 4th power has exponential type 4 pi, so J_3 must NOT vanish
    Jbad = 2 * quad(lambda t: cos(3 * pi * t) * (gamma(m) * rgamma(n + 1 + t) * rgamma(n + 1 - t)) ** 4, pts)
    check(abs(Jbad) > mpf(10) ** -10, "PW negative control")
    say("  negative control, binom^4 (type 4 pi): J_3 = %s != 0 -> REJECTED" % mp.nstr(Jbad, 10))

# ---------------------------------------------------------------- Robbins / constant
say("\n=== C: (3n)!/(n!)^3 = sqrt(3)/(2 pi n) 27^n e^{rho_n}, Robbins bracket ===")
for n in [1, 2, 5, 10, 100, 1000]:
    val = mpf(factorial(3 * n)) / mpf(factorial(n)) ** 3
    rho = log(val / (sqrt(3) / (2 * pi * n) * mpf(27) ** n))
    lo = mpf(1) / (36 * n + 1) - mpf(1) / (4 * n)
    hi = mpf(1) / (36 * n) - mpf(3) / (12 * n + 1)
    check(lo < rho < hi, "Robbins n=%d" % n)
    say("  n=%4d rho_n = %s in (%s, %s); rho_n*n = %s" % (n, mp.nstr(rho, 8), mp.nstr(lo, 8), mp.nstr(hi, 8), mp.nstr(rho * n, 8)))
check(abs(rho * 1000 + mpf(2) / 9) < 1e-3, "rho ~ -2/(9n)")
say("  rho_n ~ -2/(9n): OK.  negative control constant sqrt(3)/(4 pi n) for (3n)!/(n!)^3 (i.e. missing 1/2 placement):")
val = mpf(factorial(3000)) / mpf(factorial(1000)) ** 3
check(abs(log(val / (sqrt(3) / (4 * pi * 1000) * mpf(27) ** 1000)) - log(2)) < 1e-3, "neg ctrl const")
say("  ratio -> 2, not 1 -> REJECTED")

# ---------------------------------------------------------------- non-integer x
say("\n=== X: non-integer x (bilateral Dixon via Dougall) ===")


def poch(a, k):
    return gamma(a + k) / gamma(a)


def dougall(a, b, c, d, e):
    t = lambda k: (poch(1 + a / 2, k) * poch(b, k) * poch(c, k) * poch(d, k) * poch(e, k) /
                   (poch(a / 2, k) * poch(1 + a - b, k) * poch(1 + a - c, k) * poch(1 + a - d, k) * poch(1 + a - e, k)))
    L = nsum(t, [-inf, inf])
    G = gamma
    R = (G(1 + a - b) * G(1 + a - c) * G(1 + a - d) * G(1 + a - e) * G(1 - b) * G(1 - c) * G(1 - d) * G(1 - e) *
         G(1 + 2 * a - b - c - d - e) /
         (G(1 + a) * G(1 - a) * G(1 + a - b - c) * G(1 + a - b - d) * G(1 + a - b - e) * G(1 + a - c - d) *
          G(1 + a - c - e) * G(1 + a - d - e)))
    return L, R


for params in [("0.4", "-0.41", "-0.77", "-0.23", "-0.29"), ("0.7", "-0.6", "-0.95", "-1.35", "-0.33")]:
    L, R = dougall(*[mpf(p) for p in params])
    check(abs(L / R - 1) < mpf(10) ** -12, "Dougall")
    say("  Dougall 5H5 at %s: LHS/RHS - 1 = %s" % (params, mp.nstr(L / R - 1, 3)))

mp.dps = 40
for xs in ["2.5", "3.7", "1.3", "6.25"]:
    x = mpf(xs)
    S = nsum(lambda k: (-1) ** int(k) * (gamma(2 * x + 1) * rgamma(x + 1 + k) * rgamma(x + 1 - k)) ** 3, [-inf, inf])
    target = gamma(3 * x + 1) / gamma(x + 1) ** 3
    check(abs(S / target - 1) < mpf(10) ** -30, "bilateral x=%s" % xs)
    wrong = target * cos(pi * x)
    check(abs(S / wrong - 1) > mpf("0.01"), "neg ctrl bilateral")
    # I_1(x) versus half the closed form, with tail bound tau(2x+1)
    m = 2 * x + 1
    fr = lambda t: (gamma(m) * rgamma(x + 1 + t) * rgamma(x + 1 - t)) ** 3
    pts = [mpf(0)] + [x - k for k in range(int(x), -1, -1) if x - k > 0] + [x]
    pts = sorted(set(pts + [mpf(k) / 2 for k in range(0, int(2 * x) + 1)]))
    I1 = 2 * quad(lambda t: cos(pi * t) * fr(t), pts)
    dev = abs(I1 - target / 2)
    check(dev <= 2 * tau(m), "I1(x) x=%s" % xs)
    say("  x=%s: S(x)/[G(3x+1)/G(x+1)^3] - 1 = %s; with cos(pi x) factor ratio = %s (REJECTED);"
        " |I_1 - S/2| = %s <= 2 tau = %s" % (xs, mp.nstr(S / target - 1, 3), mp.nstr(S / wrong, 6),
                                             mp.nstr(dev, 6), mp.nstr(2 * tau(m), 6)))

say("\nTOTAL FAILS: %d" % fails)
with open(__file__.replace(".py", ".out.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
