"""L2 Round-2 re-check of Corollary cor:dixon_real (chap03), independent code.

Checks, for NON-integer real x (and x=1 edge):
  (1) full-line identity J1(x) = 1/2 Gamma(3x+1)/Gamma(x+1)^3   (Cohl-Volkmer Thm 5.1, a=0, b_j=x)
  (2) |truncated - 1/2 Gamma(3x+1)/Gamma(x+1)^3| <= 2 tau(x)    (the corollary)
  (3) the finer tail statement  int_x^inf |f_x| <= tau(x)        (Step 3 for real m)
  (4) the chapter's printed numbers at x = 5, 7.5, 10, 20 (truncated quantity)
Negative controls (must FAIL): target without the 1/2; tau replaced by tau/20;
full-line identity with Gamma(3x+2); bound applied at x=0.1 where psi(m)<0 (tau<0).
f_x(t) is built from 1/Gamma (mpmath.rgamma, entire) so no pole handling is needed.
"""
import mpmath as mp

mp.mp.dps = 50
FAILS = 0


def check(name, ok):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        FAILS += 1


def f(x, t):
    return (mp.gamma(2 * x + 1) * mp.rgamma(x + 1 + t) * mp.rgamma(x + 1 - t)) ** 3


def g(x, t):
    return mp.cos(mp.pi * t) * f(x, t)


def pts(a, b):
    """split [a,b] at integers and half-integers (oscillation nodes)."""
    p = [mp.mpf(a)]
    k = mp.floor(2 * a) / 2 + mp.mpf(1) / 2
    while k < b:
        if k > p[-1]:
            p.append(k)
        k += mp.mpf(1) / 2
    p.append(mp.mpf(b))
    return p


def truncated(x):
    return 2 * mp.quad(lambda t: g(x, t), pts(0, x))


def tail(x, S=150, absval=False):
    h = (lambda t: abs(f(x, t))) if absval else (lambda t: g(x, t))
    return mp.quad(h, pts(x, x + S))


def tail_rest_bound(x, S):
    # int_S^inf pi^-3 B(1,m)^2 B(s,m) ds <= pi^-3 m^-2 * Gamma(m) * int_S^inf s^-m ds  (B(s,m)<=Gamma(m) s^-m)
    m = 2 * x + 1
    return mp.gamma(m) * S ** (1 - m) / (mp.pi ** 3 * m ** 2 * (m - 1))


def tau(x):
    m = 2 * mp.mpf(x) + 1
    return 1 / (3 * mp.digamma(m)) + 1 / (mp.pi ** 3 * m ** 2 * (m - 1))


def target(x):
    return mp.gamma(3 * x + 1) / (2 * mp.gamma(x + 1) ** 3)


print("x | trunc-target | 2tau | ratio | int_x^inf|f| | tau | full-line rel.err")
for xs in ["1", "1.5", "2.3", "3.7", "7.7", "15.5"]:
    x = mp.mpf(xs)
    S = 150
    T = truncated(x)
    tl = tail(x, S)
    J1 = T + 2 * tl
    rest = tail_rest_bound(x, S)
    err = T - target(x)
    ta = tau(x)
    tabs = tail(x, S, absval=True) + rest
    rel = J1 / target(x) - 1
    print(xs, mp.nstr(err, 6), mp.nstr(2 * ta, 6), mp.nstr(abs(err) / (2 * ta), 4),
          mp.nstr(tabs, 6), mp.nstr(ta, 6), mp.nstr(rel, 4), " (rest<=", mp.nstr(rest, 3), ")")
    check(f"x={xs} full-line identity (|rel|<1e-12 + rest)", abs(J1 - target(x)) <= 2 * rest + mp.mpf(10) ** -12 * target(x))
    check(f"x={xs} corollary bound |err|<=2tau", abs(err) <= 2 * ta)
    check(f"x={xs} Step-3 tail int|f|<=tau", tabs <= ta)
    # negative controls
    check(f"x={xs} NEG target without 1/2 violates bound", abs(T - 2 * target(x)) > 2 * ta)
    check(f"x={xs} NEG Gamma(3x+2) identity fails", abs(J1 - mp.gamma(3 * x + 2) / (2 * mp.gamma(x + 1) ** 3)) > mp.mpf("1e-3"))

# tau/20 control: the bound must not be trivially loose everywhere
viol = []
for xs in ["1", "1.5", "2.3", "3.7"]:
    x = mp.mpf(xs)
    viol.append(abs(truncated(x) - target(x)) > 2 * tau(x) / 20)
check("NEG 2tau/20 is violated for some x in {1,1.5,2.3,3.7}", any(viol))

# psi sign: m0 ~ 1.4616; x=0.1 -> m=1.2 -> psi<0 so tau has no meaning
check("psi(3)>0 and psi(1.2)<0 (m0 threshold)", mp.digamma(3) > 0 and mp.digamma(mp.mpf("1.2")) < 0)
m0 = mp.findroot(mp.digamma, 1.46)
print("m0 =", mp.nstr(m0, 8))
check("m0 ~ 1.4616", abs(m0 - mp.mpf("1.4616")) < 1e-4)
# psi monotone increasing (does NOT change monotonicity): psi' = trigamma > 0
check("psi'=trigamma>0 at m=1.2,1.4616,3 (psi only changes SIGN at m0)",
      all(mp.psi(1, mp.mpf(v)) > 0 for v in ["1.2", "1.4616", "3"]))

# printed numbers (truncated quantity, relative)
printed = {"5": 5.1e-7, "7.5": -5.2e-11, "10": -6.0e-14, "20": -5e-28}
for xs, val in printed.items():
    x = mp.mpf(xs)
    q = truncated(x) / target(x) - 1
    print("printed x=", xs, mp.nstr(q, 4))
    check(f"printed value x={xs}", abs(q - val) <= 0.06 * abs(val))

# tau -> 0 as x -> inf (error tends to 0) and Stirling form of target
for xs in ["1e3", "1e6"]:
    print("tau(", xs, ")=", mp.nstr(tau(mp.mpf(xs)), 5))
x = mp.mpf(200)
check("target ~ sqrt3/(4 pi x) 27^x at x=200 (rel<1e-2)",
      abs(target(x) / (mp.sqrt(3) / (4 * mp.pi * x) * mp.mpf(27) ** x) - 1) < 1e-2)
print("TOTAL FAILS", FAILS)
