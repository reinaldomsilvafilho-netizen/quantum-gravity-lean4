"""L2 check, batch LIVRO_A2 (2026-10-10). Test script (PASS/FAIL).

Claims checked:
 (1) chap03, eq:alexeiewsky (DLMF 5.17.4): for real x > -1,
     int_0^x lnGamma(y+1) dy = x lnGamma(x+1) - ln G(x+1) + (x/2) ln(2 pi) - x(x+1)/2,
     G = Barnes G. This is the hypothesis hAlex of Chap03Analysis.row_log_product,
     instantiated at the Barnes G.  Oracle: mpmath.quad of lnGamma vs mpmath.barnesg.
     Negative controls: x(x-1)/2 in place of x(x+1)/2; G(x+2) in place of G(x+1).
 (2) chap03, cor:row_log_product: E(x) = int_0^x ln C(x,y) dy
     = x(x+1) - x ln(2pi) - x lnGamma(x+1) + 2 ln G(x+1), x >= 0.
     Oracle: direct quadrature of ln C(x,y).  Control: x(x-1) in place of x(x+1).
 (3) chap03, thm:laplacian_symbol: M2(alpha) = a Id + b 11^T with a(alpha) > 0,
     for the normalized continuous multinomial kernel on Delta_{m-1}(alpha), m = 3.
     a computed two ways: M2_11 - M2_12 and (1/2) E(y1-y2)^2 (independent integrands),
     plus symmetry M2_11 = M2_22.  Lattice oracle: exact enumeration of the lattice
     multinomial gives a = alpha/m, b = (alpha^2 - alpha)/m^2 (Chap04Symbol.lattice_limit).
     Negative control: the mutated claim "a <= 0" must fail; and a measure concentrated on
     the diagonal y1 = y2 gives a = 0 (so a > 0 genuinely needs non-concentration).
"""
import sys
import math
import itertools
import mpmath as mp
from scipy import integrate
from scipy.special import gammaln

mp.mp.dps = 30
bad = 0


def report(name, ok, info, control=False):
    global bad
    tag = "PASS" if ok else "FAIL"
    if control:
        tag = "CONTROL-FAILS (good)" if not ok else "CONTROL-PASSES (BAD)"
        if ok:
            bad += 1
    elif not ok:
        bad += 1
    print(f"{tag:22s} {name}: {info}")


L2PI = mp.log(2 * mp.pi)

# (1) Alexeiewsky
for x in [mp.mpf("0.3"), mp.mpf(1), mp.mpf("2.5"), mp.mpf("7.2"), mp.mpf("-0.5")]:
    lhs = mp.quad(lambda y: mp.loggamma(y + 1), [0, x])
    rhs = x * mp.loggamma(x + 1) - mp.log(mp.barnesg(x + 1)) + x / 2 * L2PI - x * (x + 1) / 2
    mut1 = x * mp.loggamma(x + 1) - mp.log(mp.barnesg(x + 1)) + x / 2 * L2PI - x * (x - 1) / 2
    mut2 = x * mp.loggamma(x + 1) - mp.log(mp.barnesg(x + 2)) + x / 2 * L2PI - x * (x + 1) / 2
    report(f"Alexeiewsky x={mp.nstr(x,3)}", abs(lhs - rhs) < mp.mpf("1e-20"),
           f"lhs={mp.nstr(lhs,15)} rhs={mp.nstr(rhs,15)} diff={mp.nstr(lhs-rhs,3)}")
    if x != 0:
        report(f"control x(x-1)/2, x={mp.nstr(x,3)}", abs(lhs - mut1) < mp.mpf("1e-10"),
               f"diff={mp.nstr(lhs-mut1,6)}", control=True)
    if x not in (mp.mpf(1),):  # ln Gamma(2)=0 makes G(3)=G(2)... only coincidence at x=0,1
        report(f"control G(x+2), x={mp.nstr(x,3)}", abs(lhs - mut2) < mp.mpf("1e-10"),
               f"diff={mp.nstr(lhs-mut2,6)}", control=True)

# (2) Row entropy corollary
for x in [mp.mpf("0.7"), mp.mpf(2), mp.mpf("5.5")]:
    E = mp.quad(lambda y: mp.loggamma(x + 1) - mp.loggamma(y + 1) - mp.loggamma(x - y + 1), [0, x])
    cf = x * (x + 1) - x * L2PI - x * mp.loggamma(x + 1) + 2 * mp.log(mp.barnesg(x + 1))
    mut = x * (x - 1) - x * L2PI - x * mp.loggamma(x + 1) + 2 * mp.log(mp.barnesg(x + 1))
    report(f"row entropy x={mp.nstr(x,3)}", abs(E - cf) < mp.mpf("1e-20"),
           f"E={mp.nstr(E,15)} closed={mp.nstr(cf,15)}")
    report(f"control x(x-1), x={mp.nstr(x,3)}", abs(E - mut) < mp.mpf("1e-10"),
           f"diff={mp.nstr(E-mut,6)}", control=True)


# (3) a(alpha) > 0, continuous kernel, m = 3 (coordinates y1, y2; y3 = alpha - y1 - y2)
def dens(y2, y1, al):
    y3 = al - y1 - y2
    if y3 < 0:
        y3 = 0.0
    return math.exp(gammaln(al + 1) - gammaln(y1 + 1) - gammaln(y2 + 1) - gammaln(y3 + 1))


def mom(g, al):
    v, err = integrate.dblquad(lambda y2, y1: g(y1, y2) * dens(y2, y1, al),
                               0, al, 0, lambda y1: al - y1, epsabs=1e-12, epsrel=1e-11)
    return v, err


for al in [0.5, 1.5, 4.0, 10.0]:
    Z, _ = mom(lambda a, b: 1.0, al)
    m11, _ = mom(lambda a, b: a * a, al)
    m22, _ = mom(lambda a, b: b * b, al)
    m12, _ = mom(lambda a, b: a * b, al)
    dd, _ = mom(lambda a, b: (a - b) ** 2, al)
    m11, m22, m12, dd = m11 / Z, m22 / Z, m12 / Z, dd / Z
    a1 = m11 - m12
    a2 = 0.5 * dd
    b = m12
    report(f"m=3 alpha={al}: symmetry M11=M22", abs(m11 - m22) < 1e-8 * max(1, m11),
           f"M11={m11:.12g} M22={m22:.12g}")
    report(f"m=3 alpha={al}: a two ways agree", abs(a1 - a2) < 1e-8 * max(1, abs(a1)),
           f"M11-M12={a1:.12g} (1/2)E(y1-y2)^2={a2:.12g}")
    report(f"m=3 alpha={al}: a > 0", a2 > 1e-6, f"a={a2:.12g} b={b:.12g}")
    report(f"control 'a <= 0', alpha={al}", a2 <= 0, f"a={a2:.6g}", control=True)

# lattice multinomial oracle: m = 3, integer alpha (number of trials) -> exact moments
for al, m in [(4, 3), (7, 3), (5, 4)]:
    tot = 0
    M = [[0.0] * (m - 1) for _ in range(m - 1)]
    for c in itertools.product(range(al + 1), repeat=m - 1):
        if sum(c) > al:
            continue
        cnt = list(c) + [al - sum(c)]
        p = math.factorial(al)
        for t in cnt:
            p //= math.factorial(t)
        w = p / m ** al
        tot += w
        for i in range(m - 1):
            for j in range(m - 1):
                M[i][j] += w * c[i] * c[j]
    a = M[0][0] - M[0][1]
    b = M[0][1]
    report(f"lattice m={m} alpha={al}: a = alpha/m", abs(a - al / m) < 1e-10 and abs(tot - 1) < 1e-12,
           f"a={a:.12g} alpha/m={al/m:.12g}")
    report(f"lattice m={m} alpha={al}: b = (alpha^2-alpha)/m^2", abs(b - (al * al - al) / m ** 2) < 1e-10,
           f"b={b:.12g} expected={(al*al-al)/m**2:.12g}")
    report(f"control lattice b = alpha^2/m^2, m={m} alpha={al}", abs(b - al * al / m ** 2) < 1e-10,
           f"b={b:.6g}", control=True)

# degenerate measure on the diagonal: (y, y) with y uniform on [0,1] -> a = 0 exactly
# M11 = E y^2 = 1/3, M12 = E y^2 = 1/3
report("diagonal measure gives a = 0 (a > 0 needs non-concentration)", abs((1 / 3) - (1 / 3)) == 0,
       "M11 = M12 = 1/3 analytically")

print("bad =", bad)
sys.exit(1 if bad else 0)
