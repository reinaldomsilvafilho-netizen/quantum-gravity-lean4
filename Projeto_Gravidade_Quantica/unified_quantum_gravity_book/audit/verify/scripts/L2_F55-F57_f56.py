"""Layer-2 re-check of F-56 (ch. 3, Alexeiewsky's theorem and Cor. cor:row_log_product).

Oracles: (1) mpmath.quad of int_0^x ln C(x,y) dy, independent of G;
(2) mpmath.barnesg; (3) for integer x, G(n+1) = prod_{k<n} k! exactly (no barnesg);
(4) Adamchik's form int_0^z log Gamma(t) dt = z(1-z)/2 + z/2 log 2pi + z log Gamma(z) - log G(z+1).
Negative controls: sign flip on 2 ln G; coefficient x/2 ln 2pi in E; DLMF with -1/2 z(z-1).
Refinement: quadrature at dps 15, 25, 40 (error must decrease).
"""
import sys
import mpmath as mp

FAIL = 0


def check(name, ok, msg=""):
    global FAIL
    print(f"[{name}] {'ok  ' if ok else 'FAIL'} {msg}", flush=True)
    if not ok:
        FAIL += 1


def E_quad(x):
    f = lambda y: mp.loggamma(x + 1) - mp.loggamma(y + 1) - mp.loggamma(x - y + 1)
    return mp.quad(f, [0, x / 2, x])


def E_closed(x, G=None):
    lg = mp.log(mp.barnesg(x + 1)) if G is None else mp.log(G)
    return x * (x + 1) - x * mp.log(2 * mp.pi) - x * mp.loggamma(x + 1) + 2 * lg


def E_neg_sign(x):
    return x * (x + 1) - x * mp.log(2 * mp.pi) - x * mp.loggamma(x + 1) - 2 * mp.log(mp.barnesg(x + 1))


def E_neg_coef(x):
    return x * (x + 1) - x / 2 * mp.log(2 * mp.pi) - x * mp.loggamma(x + 1) + 2 * mp.log(mp.barnesg(x + 1))


def dlmf_lhs(z):
    return mp.quad(lambda t: mp.loggamma(t + 1), [0, z])


def dlmf_rhs(z):
    return z / 2 * mp.log(2 * mp.pi) - z * (z + 1) / 2 + z * mp.loggamma(z + 1) - mp.log(mp.barnesg(z + 1))


mp.mp.dps = 40
xs = [mp.mpf("0.3"), mp.mpf(1), mp.mpf("2.5"), mp.mpf("7.25"), mp.mpf("15.3")]
print("== Corollary: E(x) quadrature vs closed form (dps 40)")
worst, negs, negc = 0, 0, 0  # mutation rejected if it fails at some x (ln G(2)=0 at x=1)
for x in xs:
    a, b = E_quad(x), E_closed(x)
    worst = max(worst, abs(a - b))
    negs = max(negs, abs(a - E_neg_sign(x)))
    negc = max(negc, abs(a - E_neg_coef(x)))
    print(f"   x={mp.nstr(x,5):>6}: quad {mp.nstr(a,25)}  closed {mp.nstr(b,25)}  diff {mp.nstr(abs(a-b),3)}")
check("cor", worst < mp.mpf(10) ** -30, f"max diff {mp.nstr(worst,3)}")
check("cor-NEG-sign", negs > 1e-3, f"sign flip on 2 ln G: max diff {mp.nstr(negs,5)}")
check("cor-NEG-coef", negc > 1e-3, f"coefficient x/2 ln 2pi: max diff {mp.nstr(negc,5)}")

print("== DLMF 5.17.4 as displayed in the chapter (eq:alexeiewsky)")
worst, neg = 0, mp.inf
for z in xs + [mp.mpf("-0.5"), mp.mpf("-0.9")]:
    l = dlmf_lhs(z); r = dlmf_rhs(z)
    worst = max(worst, abs(l - r))
    neg = min(neg, abs(l - (r + z * (z + 1) / 2 - z * (z - 1) / 2)))
    print(f"   z={mp.nstr(z,4):>6}: diff {mp.nstr(abs(l-r),3)}")
check("dlmf", worst < mp.mpf(10) ** -30, "valid also for -1 < x < 0 (chapter says x > -1)")
check("dlmf-NEG", neg > 1e-3, "mutated -z(z-1)/2 rejected")

print("== Adamchik Sec. 6 form (int log Gamma(t)) is equivalent")
worst = 0
for z in xs:
    l = mp.quad(lambda t: mp.loggamma(t), [0, z])
    r = z * (1 - z) / 2 + z / 2 * mp.log(2 * mp.pi) + z * mp.loggamma(z) - mp.log(mp.barnesg(z + 1))
    worst = max(worst, abs(l - r))
check("adamchik", worst < mp.mpf(10) ** -28, f"max diff {mp.nstr(worst,3)}; differs from DLMF form by z ln z - z")

print("== Integer x: G(n+1) = prod_{k<n} k!, no barnesg; discrete product identity")
worst = 0
for n in range(0, 12):
    Gn1 = mp.mpf(1)
    for k in range(n):
        Gn1 *= mp.factorial(k)
    worst = max(worst, abs(E_closed(mp.mpf(n), G=Gn1) - E_quad(mp.mpf(n))) if n > 0 else 0)
    prod = 1
    for k in range(n + 1):
        prod *= mp.binomial(n, k)
    sf = mp.mpf(1)
    for k in range(n + 1):
        sf *= mp.factorial(k)
    assert abs(prod - mp.factorial(n) ** (n + 1) / sf ** 2) < 1e-20 * abs(prod)
    assert abs(sf - mp.barnesg(n + 2)) < 1e-25 * sf
check("integer", worst < mp.mpf(10) ** -30, f"factorial-product G, max diff {mp.nstr(worst,3)}; prod C(n,k) = (n!)^(n+1)/sf(n)^2, sf(n)=G(n+2) for n<12")

print("== refinement: quadrature error vs working precision, x = 7.25")
x = mp.mpf("7.25")
mp.mp.dps = 60
ref = E_closed(x)
errs = []
for d in [15, 25, 40]:
    mp.mp.dps = d
    e = E_quad(x)
    mp.mp.dps = 60
    errs.append(abs(e - ref))
    print(f"   dps {d}: |quad - closed(dps60)| = {mp.nstr(errs[-1],3)}")
check("refine", errs[0] > errs[1] > errs[2], "error decreases with precision")
sys.exit(FAIL)
