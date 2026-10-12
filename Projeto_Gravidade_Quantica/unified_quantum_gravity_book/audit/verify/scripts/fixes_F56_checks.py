"""F-56 check: ch. 3 closed form of E(x) = int_0^x ln binom(x,y) dy via Barnes G.

Oracle: direct mpmath quadrature of ln Gamma terms (no Barnes G involved).
Also checks DLMF 5.17.4 (Alexeiewsky) by quadrature.
Negative control: the mutated closed form with -2 ln G(x+1) must fail.
"""
import sys
import mpmath as mp

mp.mp.dps = 30
fails = 0
out = []


def log(s):
    print(s); out.append(s)


def lnbinom(x, y):
    return mp.loggamma(x + 1) - mp.loggamma(y + 1) - mp.loggamma(x - y + 1)


def closed(x, sgn=1):
    return x * (x + 1) - x * mp.log(2 * mp.pi) - x * mp.loggamma(x + 1) + sgn * 2 * mp.log(mp.barnesg(x + 1))


for x in (mp.mpf("0.5"), mp.mpf(1), mp.mpf("2.7"), mp.mpf(7), mp.mpf("15.3")):
    quad = mp.quad(lambda y: lnbinom(x, y), [0, x / 2, x])
    err = abs(quad - closed(x))
    neg = abs(quad - closed(x, -1))
    alex_lhs = mp.quad(lambda t: mp.loggamma(t + 1), [0, x])
    alex_rhs = x / 2 * mp.log(2 * mp.pi) - x * (x + 1) / 2 + x * mp.loggamma(x + 1) - mp.log(mp.barnesg(x + 1))
    aerr = abs(alex_lhs - alex_rhs)
    log(f"x={mp.nstr(x,4)}: E quad={mp.nstr(quad,15)} closed err={mp.nstr(err,3)} NEG err={mp.nstr(neg,3)} DLMF5.17.4 err={mp.nstr(aerr,3)}")
    if not err < mp.mpf("1e-20"):
        fails += 1; log("  FAIL closed form")
    if not aerr < mp.mpf("1e-20"):
        fails += 1; log("  FAIL DLMF 5.17.4")
    if x > 1 and not neg > mp.mpf("1e-3"):
        fails += 1; log("  FAIL negative control not rejected")
log(f"FAILURES: {fails}")
with open(__file__.replace(".py", ".out.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
sys.exit(fails)
