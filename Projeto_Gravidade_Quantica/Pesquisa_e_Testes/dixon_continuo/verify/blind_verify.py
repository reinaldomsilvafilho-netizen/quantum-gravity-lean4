"""Blind independent verification of dixon_proof.tex (four-eyes).

Independent oracles (different from the author's scripts):
  * V2: J_1 and F(omega) via Ramanujan's Fourier transform of 1/(Gamma(a+t)Gamma(b-t))
        and triple convolution (no Poisson, no Dixon identity, no quadrature of f).
  * V3: J_3 at the borderline n=1 by direct full-line quadrature with explicit tail bound.
  * V4: tail T_1 by direct quadrature of the rgamma definition (not the Beta form).
  * V6: bilateral sum for real x checked against a full-line INTEGRAL (Cohl-Volkmer Thm 5.1),
        not against Dougall.
Each block has a negative control that must fail.
Run: python verify/blind_verify.py   (writes verify/blind_verify.out.txt)
"""
from fractions import Fraction
from math import comb, factorial
import os

from mpmath import (mp, mpf, quad, cos, sin, pi, gamma, rgamma, loggamma, inf, log, exp,
                    sqrt, psi, nsum, diff, findroot, rf, fabs, sinh)

out = []
fails = 0


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    out.append(s)


def check(cond, label):
    global fails
    if not cond:
        fails += 1
        say("  ** FAIL:", label)
    return cond


def f(n, t):
    m = 2 * n + 1
    return (gamma(m) * rgamma(n + 1 + t) * rgamma(n + 1 - t)) ** 3


def tau(m):
    return 1 / (3 * psi(0, m)) + 1 / (pi ** 3 * m ** 2 * (m - 1))


mp.dps = 30

# ------------------------------------------------------------------ V1 growth / type
say("=== V1: growth bound |f(z)| <= K_n e^{3pi|Im z|} |z|^{-6n-3} for |z| >= 2n; type exactly 3pi ===")
for n in [1, 2, 3, 5]:
    K = gamma(2 * n + 1) ** 3 / pi ** 3 * (mpf(4) / 3) ** (3 * n)
    worst = mpf(0)
    for R in [2 * n, 3 * n, 7 * n, 20 * n]:
        for k in range(0, 721):
            th = 2 * pi * k / 720
            z = R * exp(1j * th)
            val = abs(f(n, z)) / (K * exp(3 * pi * abs(z.imag)) * abs(z) ** (-6 * n - 3))
            worst = max(worst, val)
    check(worst <= 1, "growth n=%d" % n)
    y = mpf(60)
    typ = log(abs(f(n, 1j * y))) / y + (6 * n + 3) * log(y) / y
    say("  n=%d: max ratio on circles R in {2n,3n,7n,20n} = %s (<=1); log|f(iy)|/y + (6n+3)log y/y at y=60 = %s (3pi=%s)"
        % (n, mp.nstr(worst, 6), mp.nstr(typ, 6), mp.nstr(3 * pi, 6)))
    # negative control: claimed type 2.9 pi must be violated on the imaginary axis
    check(abs(f(n, 1j * y)) > exp(2.9 * pi * y) * y ** (-6 * n - 3) * K, "negctl type n=%d" % n)
say("  negative control: bound with type 2.9pi is violated on iR for every n -> REJECTED")

# ------------------------------------------------------------------ V2 Ramanujan convolution oracle
say("\n=== V2: F(omega) via Ramanujan transform + triple convolution (independent of Poisson & Dixon) ===")
# Ramanujan: int e^{i xi t} dt /(Gamma(a+t)Gamma(b-t)) = (2cos(xi/2))^{a+b-2} e^{i xi (b-a)/2}/Gamma(a+b-1), |xi|<pi, else 0.
# First check the Ramanujan formula itself numerically at a=b=n+1 (n=2), xi=1.1 and xi=3.5 (must vanish).
mp.dps = 20
for n, xi in [(2, mpf("1.1")), (2, mpf("3.5")), (3, mpf("2.0"))]:
    g = lambda t: rgamma(n + 1 + t) * rgamma(n + 1 - t)
    pts = [mpf(k) / 2 for k in range(0, 2 * (n + 60) + 1)]
    num = 2 * quad(lambda t: cos(xi * t) * g(t), pts)
    ram = (2 * cos(xi / 2)) ** (2 * n) / gamma(2 * n + 1) if abs(xi) < pi else mpf(0)
    # truncation at |t|=n+60 of a t^-(2n+1) integrand limits accuracy to ~1e-9
    check(abs(num - ram) < mpf(10) ** -8, "Ramanujan n=%d xi=%s" % (n, xi))
    say("  Ramanujan transform n=%d xi=%s: quad=%s formula=%s" % (n, xi, mp.nstr(num, 12), mp.nstr(ram, 12)))

mp.dps = 25


def F_conv(n, w):
    """F(w) = int f(t) e^{iwt} dt = (2pi)^-2 * triple convolution of phi(xi)=(2cos(xi/2))^{2n} on [-pi,pi]."""
    phi = lambda s: (2 * cos(s / 2)) ** (2 * n) if abs(s) <= pi else mpf(0)

    def inner(x1):
        lo = max(-pi, w - pi - x1)
        hi = min(pi, w + pi - x1)
        if hi <= lo:
            return mpf(0)
        return quad(lambda x2: phi(x2) * phi(w - x1 - x2), [lo, hi])
    lo1 = max(-pi, w - 3 * pi)
    if lo1 >= pi:
        return mpf(0)
    return quad(lambda x1: phi(x1) * inner(x1), [lo1, (lo1 + pi) / 2, pi]) / (2 * pi) ** 2


for n in [1, 2, 3, 4, 6]:
    D = Fraction(factorial(3 * n), factorial(n) ** 3)
    J1 = F_conv(n, pi)
    check(abs(J1 / (mpf(D.numerator) / 2) - 1) < mpf(10) ** -15, "J1 conv n=%d" % n)
    # negative control: J_1 = D_n (no 1/2)
    check(abs(J1 / mpf(D.numerator) - 1) > mpf("0.4"), "negctl no-half n=%d" % n)
    say("  n=%d: J_1 (convolution) = %s ; (3n)!/(n!)^3 /2 = %s ; 'no 1/2' mutant ratio = %s -> REJECTED"
        % (n, mp.nstr(J1, 20), D.numerator / 2, mp.nstr(J1 / D.numerator, 5)))
for n in [1, 2]:
    for w in [mpf("2.9") * pi, mpf("2.99") * pi, 3 * pi, mpf("3.1") * pi]:
        Fw = F_conv(n, w)
        say("  n=%d F(%s pi) = %s" % (n, mp.nstr(w / pi, 4), mp.nstr(Fw, 6)))
        if w >= 3 * pi:
            check(Fw == 0 or abs(Fw) < mpf(10) ** -20, "F(>=3pi)=0")
        else:
            check(abs(Fw) > mpf(10) ** -35, "negctl: F(2.9pi)!=0 must be detected")
say("  => support exactly [-3pi,3pi]; F just inside (2.9pi, 2.99pi) is nonzero (negative control detects), F(3pi)=0.")

# ------------------------------------------------------------------ V3 borderline J_3 by direct full-line quadrature
say("\n=== V3: borderline J_3 (and J_5) at n=1,2 by direct quadrature of f on R, explicit tail bound ===")
mp.dps = 20
for n in [1, 2]:
    m = 2 * n + 1
    Kcut = 300
    for j in [3, 5]:
        pts = [mpf(k) / (2 * j) for k in range(0, 2 * j * 40 + 1)] + [mpf(k) for k in range(41, Kcut + 1)]
        Jj = 2 * quad(lambda t: cos(pi * j * t) * f(n, t), pts)
        # tail |f(n+s)| <= pi^-3 (Gamma(m) s^-m)^3 for s>=1
        tb = 2 * gamma(m) ** 3 / pi ** 3 * mpf(Kcut - n) ** (1 - 3 * m) / (3 * m - 1)
        check(abs(Jj) < 1e-12 + tb, "J%d n=%d" % (j, n))
        say("  n=%d j=%d: J_j = %s  (tail bound %s)" % (n, j, mp.nstr(Jj, 5), mp.nstr(tb, 3)))
    # negative control: kernel cos(2.8 pi t) (inside support) must be clearly nonzero
    pts = [mpf(k) / 6 for k in range(0, 6 * 40 + 1)] + [mpf(k) for k in range(41, Kcut + 1)]
    Jbad = 2 * quad(lambda t: cos(mpf("2.8") * pi * t) * f(n, t), pts)
    Jc = F_conv(n, mpf("2.8") * pi)
    check(abs(Jbad) > 1e-14 and abs(Jbad - Jc) < 1e-10, "negctl 2.8pi n=%d" % n)
    say("  negative control n=%d: int cos(2.8 pi t) f = %s (conv oracle %s) != 0" % (n, mp.nstr(Jbad, 8), mp.nstr(Jc, 8)))

# ------------------------------------------------------------------ V3b Dixon identity exact
say("\n=== V3b: Dixon identity in exact integers, n=0..40 ===")
okd = all(sum((-1) ** abs(k) * comb(2 * n, n + k) ** 3 for k in range(-n, n + 1)) == factorial(3 * n) // factorial(n) ** 3
          for n in range(41))
check(okd, "Dixon")
badd = [n for n in range(1, 41) if sum(comb(2 * n, n + k) ** 3 for k in range(-n, n + 1)) == factorial(3 * n) // factorial(n) ** 3]
check(not badd, "negctl Dixon no sign")
say("  Dixon holds n<=40; mutant without (-1)^k matches for", len(badd), "n -> REJECTED")

# ------------------------------------------------------------------ V4 tail and main estimate
say("\n=== V4: |I_1 - D_n/2| <= 2 tau_n with I_1 by direct quadrature on [-n,n] (rgamma definition) ===")
mp.dps = 90
say("  n   I_1 - D_n/2     2tau_n     int_n^inf|f| (direct)   tau_n")
worst = 0
for n in [1, 2, 3, 4, 5, 7, 10, 15, 20, 25, 30, 40]:
    D = factorial(3 * n) // factorial(n) ** 3
    I1 = 2 * quad(lambda t: cos(pi * t) * f(n, t), [mpf(k) / 2 for k in range(0, 2 * n + 1)])
    dev = I1 - mpf(D) / 2
    absT = quad(lambda t: abs(f(n, t)), [n + mpf(k) / 4 for k in range(0, 9)] + [n + k for k in range(3, 80)] + [inf])
    t_ = tau(2 * n + 1)
    check(abs(dev) <= 2 * t_ and absT <= t_, "main n=%d" % n)
    worst = max(worst, abs(dev) / (2 * t_))
    # negative control: bound 1/(3 psi) * (1/2) i.e. 2tau/2 must fail for dev? check the true size ~ 2/(3 log)
    say("  %2d  %s  %s  %s  %s" % (n, mp.nstr(dev, 8), mp.nstr(2 * t_, 6), mp.nstr(absT, 6), mp.nstr(t_, 6)))
say("  max |dev|/(2tau) =", mp.nstr(worst, 5))
# negative control: a mutated bound O(1/n) must fail at large n
check(abs(dev) > mpf(1) / n, "negctl 1/n")
say("  negative control: |dev| <= 1/n fails at n=40 (dev=%s > 1/40) -> REJECTED; error really decays only like 1/log n"
    % mp.nstr(abs(dev), 5))

# c_R independently: (1/Gamma)' = -psi/Gamma
say("\n=== V4b: c_R = max_[0,1] |(1/Gamma)'| via -psi(u)/Gamma(u) (limit 1 at u=0) ===")
g1 = lambda u: -psi(0, u) * rgamma(u) if u > 0 else mpf(1)
vals = [(abs(g1(mpf(k) / 10000)), k) for k in range(1, 10001)]
vmax, kmax = max(vals)
ustar = findroot(lambda u: diff(g1, u), mpf(kmax) / 10000)
say("  grid max %s at u=%s; refined c_R=%s at u*=%s" % (mp.nstr(vmax, 10), kmax / 10000, mp.nstr(abs(g1(ustar)), 12), mp.nstr(ustar, 10)))
check(abs(g1(ustar)) < 1.18, "c_R<1.18")
check(abs(g1(ustar)) > 1.17, "c_R value")

# ------------------------------------------------------------------ V5 constant
say("\n=== V5: (3n)!/(n!)^3 * 2pi n/(sqrt3 27^n) -> 1 ; so I_1 ~ sqrt3/(4 pi n) 27^n ===")
for n in [10, 100, 10000, 10 ** 6]:
    r = exp(loggamma(3 * n + 1) - 3 * loggamma(n + 1) - n * log(27)) * 2 * pi * n / sqrt(3)
    say("  n=%d ratio=%s ; (ratio-1)*n = %s (expect -2/9=-0.2222)" % (n, mp.nstr(r, 12), mp.nstr((r - 1) * n, 6)))
check(abs((r - 1) * n + mpf(2) / 9) < 1e-4, "const")
rbad = exp(loggamma(3 * n + 1) - 3 * loggamma(n + 1) - n * log(27)) * 4 * pi * n / sqrt(3)  # mutant sqrt3/(4pi n) for full D
check(abs(rbad - 1) > 0.5, "negctl const")
say("  mutant constant sqrt3/(4 pi n) for (3n)!/(n!)^3 gives ratio %s -> REJECTED" % mp.nstr(rbad, 6))

# ------------------------------------------------------------------ V6 real x
say("\n=== V6: real x: full-line integral int cos(pi t) f_x dt vs (1/2) Gamma(3x+1)/Gamma(x+1)^3 ===")
mp.dps = 20


def fx(x, t):
    m = 2 * x + 1
    return (gamma(m) * rgamma(x + 1 + t) * rgamma(x + 1 - t)) ** 3


for xs in ["1.3", "2.5", "3.7", "0.4"]:
    x = mpf(xs)
    m = 2 * x + 1
    target = gamma(3 * x + 1) / gamma(x + 1) ** 3
    pts = sorted(set([mpf(k) / 2 for k in range(0, 2 * 60 + 1)] + [x] + [x + k for k in range(1, 50)])) + [mpf(k) for k in range(61, 400)]
    Jx = 2 * quad(lambda t: cos(pi * t) * fx(x, t), pts)
    ratio = 2 * Jx / target
    check(abs(ratio - 1) < 1e-10, "real x=%s" % xs)
    check(abs(ratio / cos(pi * x) - 1) > 0.01, "negctl cos x=%s" % xs)
    # finite-interval estimate
    I1x = 2 * quad(lambda t: cos(pi * t) * fx(x, t), sorted(set([mpf(0), x] + [mpf(k) / 2 for k in range(0, int(2 * x) + 1)])))
    dev = abs(I1x - target / 2)
    okb = dev <= 2 * tau(m) if x >= 1 else True
    check(okb, "Thm real x=%s" % xs)
    say("  x=%s: 2*J/[G(3x+1)/G(x+1)^3] = %s ; cos(pi x)-mutant ratio %s REJECTED ; |I_1(x)-target/2|=%s  2tau=%s"
        % (xs, mp.nstr(ratio, 15), mp.nstr(ratio / cos(pi * x), 6), mp.nstr(dev, 6), mp.nstr(2 * tau(m), 6)))

# bilateral sum near the threshold x > -1/3 and well-poised 3H3 (a=0 Dougall) with distinct params
mp.dps = 25
for xs in ["-0.2", "0.25"]:
    x = mpf(xs)
    # (-1)^k f_x(k) = C^3 [(-x)_k/(1+x)_k]^3 (analytic in k, even in k); Euler-Maclaurin tail
    C3 = (gamma(2 * x + 1) / gamma(x + 1) ** 2) ** 3
    term = lambda k: C3 * (rf(-x, k) / rf(1 + x, k)) ** 3
    check(abs(term(3) - (-1) ** 3 * fx(x, 3)) < mpf(10) ** -20, "reflection identity x=%s" % xs)
    S = fx(x, 0) + 2 * nsum(term, [1, inf], method="euler-maclaurin")
    target = gamma(3 * x + 1) / gamma(x + 1) ** 3
    check(abs(S / target - 1) < 1e-8, "bilateral x=%s" % xs)
    say("  bilateral S(%s)/target - 1 = %s" % (xs, mp.nstr(S / target - 1, 3)))
b, c, d = mpf("-0.3"), mpf("-0.45"), mpf("-0.2")
L = nsum(lambda k: rf(b, k) * rf(c, k) * rf(d, k) / (rf(1 - b, k) * rf(1 - c, k) * rf(1 - d, k)), [-inf, inf])
R = gamma(1 - b) * gamma(1 - c) * gamma(1 - d) * gamma(1 - b - c - d) / (gamma(1 - b - c) * gamma(1 - b - d) * gamma(1 - c - d))
check(abs(L / R - 1) < 1e-15, "3H3")
say("  well-poised 3H3 (Dougall a->0, e=a/2) at b,c,d=-0.3,-0.45,-0.2: LHS/RHS-1 = %s" % mp.nstr(L / R - 1, 3))

# ------------------------------------------------------------------ V7 prior art formula (Cohl-Volkmer Thm 5.1)
say("\n=== V7: Cohl-Volkmer (Ramanujan J. 2025) Thm 5.1 at generic a,b_j (confirms prior-art reading) ===")
mp.dps = 20
a = mpf("0.3")
bs = [mpf("0.7"), mpf("1.2"), mpf("2.1")]
h = lambda t: 2 * cos(pi * t) * rgamma(bs[0] + 1 + a + t) * rgamma(bs[0] + 1 - t) * rgamma(bs[1] + 1 + a + t) * rgamma(bs[1] + 1 - t) * rgamma(bs[2] + 1 + a + t) * rgamma(bs[2] + 1 - t)
lhs = quad(h, [mpf(k) / 2 for k in range(-400, 401)])
rhs = cos(pi * a / 2) * gamma(1 + 1.5 * a + sum(bs)) / (gamma(1 + a / 2 + bs[0]) * gamma(1 + a / 2 + bs[1]) * gamma(1 + a / 2 + bs[2]) *
                                                          gamma(1 + a + bs[0] + bs[1]) * gamma(1 + a + bs[0] + bs[2]) * gamma(1 + a + bs[1] + bs[2]))
check(abs(lhs / rhs - 1) < 1e-10, "CV 5.1")
say("  LHS/RHS - 1 = %s  (a=0, b_j=n gives exactly J_1 = (3n)!/(2 (n!)^3))" % mp.nstr(lhs / rhs - 1, 3))

# ------------------------------------------------------------------ V8 book's numerical claims
say("\n=== V8: book ch.3 numeric claims: ratio I_1(x)/(Gamma(3x+1)/(2Gamma(x+1)^3)) ===")
mp.dps = 40
for xs, claim in [("5", "1.0000005"), ("7.5", "1 - 5e-11"), ("10", "1 (double)"), ("20", "1 (double)")]:
    x = mpf(xs)
    target = gamma(3 * x + 1) / gamma(x + 1) ** 3 / 2
    I1x = 2 * quad(lambda t: cos(pi * t) * fx(x, t), sorted(set([mpf(0), x] + [mpf(k) / 2 for k in range(0, int(2 * x) + 1)])))
    say("  x=%s: ratio - 1 = %s   (book claims %s)" % (xs, mp.nstr(I1x / target - 1, 6), claim))

say("\nTOTAL FAILS: %d" % fails)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "blind_verify.out.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
