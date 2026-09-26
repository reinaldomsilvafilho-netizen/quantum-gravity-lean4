"""Blind checks for chap03 (camada 1). Independent oracles: mpmath quadrature,
closed forms, finite sums. Each block has a negative control where meaningful."""
import mpmath as mp
from scipy import integrate
import numpy as np
from math import gamma, lgamma, exp, pi, sin, factorial

mp.mp.dps = 30

def C(x, y):
    return mp.gamma(x + 1) / (mp.gamma(y + 1) * mp.gamma(x - y + 1))

def I2(x):
    return mp.quad(lambda y: C(x, y), [0, x / 2, x])

def J(x):
    return 2 / mp.pi * mp.quad(lambda p: mp.cos(p) ** x * mp.sin(x * p) / p,
                               mp.linspace(0, mp.pi / 2, 20))

print("== Thm 2.1: I(x) = 2^x J(x); 2^x - I(x) range ==")
for x in [1, 2, 5, 10, 17.3]:
    i, j = I2(x), J(x)
    print(x, mp.nstr(i, 12), mp.nstr(2 ** x * j, 12), "defect", mp.nstr(2 ** x - i, 6),
          "1-erf(sqrt(x/2))*2^x", mp.nstr(2 ** x * (1 - mp.erf(mp.sqrt(x / 2))), 6))
# negative control: mutate J with sin(2 x phi)
print("mutant J(5)*32", mp.nstr(32 * 2 / mp.pi * mp.quad(lambda p: mp.cos(p) ** 5 * mp.sin(10 * p) / p, [0, mp.pi / 2]), 8))
ds = [2 ** x - I2(x) for x in np.linspace(1, 30, 59)]
print("min/max defect on [1,30]:", mp.nstr(min(ds), 5), mp.nstr(max(ds), 5))

print("== Thm 3.1: torus representation, m=3, integer x=n ==")
# For integer n, (1+e^{i t1}+e^{i t2})^n is a trig polynomial, so the torus
# integral equals sum_k multinom(n;k) sinc(pi(k1-y1)) sinc(pi(k2-y2)) exactly.
def sinc(u):
    return mp.mpf(1) if u == 0 else mp.sin(mp.pi * u) / (mp.pi * u)
def torus_rep(n, y1, y2):
    s = 0
    for k1 in range(n + 1):
        for k2 in range(n + 1 - k1):
            s += mp.factorial(n) / (mp.factorial(k1) * mp.factorial(k2) * mp.factorial(n - k1 - k2)) * sinc(k1 - y1) * sinc(k2 - y2)
    return s
def multi(x, ys):
    return mp.gamma(x + 1) / mp.fprod([mp.gamma(v + 1) for v in ys])
for (n, y1, y2) in [(2, 0.5, 0.5), (3, 0.7, 1.1), (4, 1.5, 1.2)]:
    print(n, y1, y2, "Gamma form", mp.nstr(multi(n, [y1, y2, n - y1 - y2]), 10),
          "torus", mp.nstr(torus_rep(n, y1, y2), 10))
print("exact: 8/pi =", mp.nstr(8 / mp.pi, 10), " 76/(3pi^2) =", mp.nstr(76 / (3 * mp.pi ** 2), 10))
# positive control m=2: 1D analogue must agree
def torus1(n, y):
    return sum(mp.binomial(n, k) * sinc(k - y) for k in range(n + 1))
print("m=2 control n=3,y=1.3:", mp.nstr(C(3, 1.3), 10), mp.nstr(torus1(3, 1.3), 10))

def I3(x):
    f = lambda y2, y1: float(multi(x, [y1, y2, x - y1 - y2]))
    return integrate.dblquad(f, 0, x, 0, lambda y1: x - y1, epsabs=1e-11, epsrel=1e-11)[0]
def I3_torus(n):
    f = lambda y2, y1: float(torus_rep(n, y1, y2))
    return integrate.dblquad(f, 0, n, 0, lambda y1: n - y1, epsabs=1e-10, epsrel=1e-10)[0]
for n in [2, 3]:
    print("n=%d I_3 (Gamma) = %.6f ; 3^n J_3 (torus) = %.6f" % (n, I3(n), I3_torus(n)))

print("== Table 1 values ==")
def I4(x):
    f = lambda y3, y2, y1: float(multi(x, [y1, y2, y3, x - y1 - y2 - y3]))
    return integrate.tplquad(f, 0, x, 0, lambda y1: x - y1, 0, lambda y1, y2: x - y1 - y2, epsabs=1e-9, epsrel=1e-9)[0]
for x in [1, 2, 5, 10]:
    print("x=%g I2=%.4f I3=%.4f I4=%.4f" % (x, float(I2(x)), I3(x), I4(x)))
for n in [6, 10, 14]:
    print("ratio (3^n-I3)/I2 n=%d: %.4f" % (n, (3 ** n - I3(n)) / float(I2(n))))

print("== Remark (potential interpretation): hexagon alternating sum for a generic potential ==")
hexL = lambda P, n, k: P(n - 1, k - 1) + P(n, k + 1) + P(n + 1, k)
hexR = lambda P, n, k: P(n - 1, k) + P(n, k - 1) + P(n + 1, k + 1)
lnC = lambda x, y: mp.log(C(x, y))
P2 = lambda x, y: x ** 2 * y  # smooth potential, gradient field conservative
print("ln binom, n=7.3,k=2.6: LHS-RHS =", mp.nstr(hexL(lnC, 7.3, 2.6) - hexR(lnC, 7.3, 2.6), 5))
print("Phi=x^2 y: LHS-RHS =", hexL(P2, 7.3, 2.6) - hexR(P2, 7.3, 2.6))

print("== Fibonacci / ray integrals ==")
phi = (1 + mp.sqrt(5)) / 2
for x in [20, 60, 150]:
    F = mp.quad(lambda y: C(x - y, y), mp.linspace(0, x / 2, 8))
    print(x, "F/(phi^(x+1)/sqrt5) =", mp.nstr(F / (phi ** (x + 1) / mp.sqrt(5)), 8))
for a in [0.5, 2.0]:
    lam = mp.findroot(lambda z: z ** (a + 1) - z ** a - 1, 1.5)
    rs = []
    for x in [80, 160]:
        F = mp.quad(lambda y: C(x - a * y, y), mp.linspace(0, x / (1 + a), 8))
        rs.append(F)
    print("alpha", a, "lambda", mp.nstr(lam, 10), "growth (F160/F80)^(1/80)", mp.nstr((rs[1] / rs[0]) ** (mp.mpf(1) / 80), 10))

print("== L^p norms ==")
for p in [0.5, 2, 3]:
    for x in [50, 200]:
        v = mp.quad(lambda y: C(x, y) ** p, mp.linspace(0, x, 9))
        pred = 2 ** (p * x) / ((mp.pi * x / 2) ** ((p - 1) / 2) * mp.sqrt(p))
        print("p", p, "x", x, "ratio", mp.nstr(v / pred, 8))

print("== Dixon continuous integral ==")
mp.mp.dps = 60
for x in [5, 10, 20, 7.5]:
    v = mp.quad(lambda t: mp.cos(mp.pi * t) * C(2 * x, x + t) ** 3, mp.linspace(-x, x, 41))
    half = mp.gamma(3 * x + 1) / mp.gamma(x + 1) ** 3 / 2
    print(x, "ratio to (1/2) multinom =", mp.nstr(v / half, 12))
mp.mp.dps = 30

print("== Alternating row integrals ==")
for x in [3, 5, 4, 10.3, 20.5]:
    print(x, mp.nstr(mp.quad(lambda y: mp.cos(mp.pi * y) * C(x, y), mp.linspace(0, x, 12)), 6))

print("== Hockey stick remainder R_r(x)/x^r ==")
for r in [0.5, 1.5, 3.2]:
    out = []
    for x in [10, 50, 200]:
        R = C(x + 1, r + 1) - 1 / mp.gamma(r + 2) - mp.quad(lambda t: C(t, r), [r, x])
        out.append(mp.nstr(R / x ** r, 5))
    print("r", r, out)

print("== Barnes G row entropy ==")
for x in [0.7, 3.4, 12.0]:
    lhs = mp.quad(lambda y: mp.log(C(x, y)), [0, x])
    rhs = x * (x + 1) - x * mp.log(2 * mp.pi) - x * mp.loggamma(x + 1) + 2 * mp.log(mp.barnesg(x + 1))
    mut = x * (x + 1) - x * mp.log(2 * mp.pi) - x * mp.loggamma(x + 1) + 1 * mp.log(mp.barnesg(x + 1))
    print(x, mp.nstr(lhs, 14), mp.nstr(rhs, 14), "mutant", mp.nstr(mut, 8))
# Table: prod binom(n,k) = (n!)^{n+1}/H(n)^2 ; H = hyperfactorial vs superfactorial
for n in [2, 3, 5]:
    prod = 1
    for k in range(n + 1):
        prod *= mp.binomial(n, k)
    hyper = mp.fprod([mp.mpf(k) ** k for k in range(1, n + 1)])
    superf = mp.fprod([mp.factorial(k) for k in range(n + 1)])
    print(n, "prod", prod, "with hyperfactorial", mp.factorial(n) ** (n + 1) / hyper ** 2, "with superfactorial", mp.factorial(n) ** (n + 1) / superf ** 2)

print("== Moments: Var(y_1) - (m-1)x/m^2 (m=2) ==")
for x in [5, 20, 60]:
    Z = I2(x)
    m1 = mp.quad(lambda y: y * C(x, y), mp.linspace(0, x, 9)) / Z
    m2 = mp.quad(lambda y: y * y * C(x, y), mp.linspace(0, x, 9)) / Z
    print(x, "mean-x/2", mp.nstr(m1 - x / 2, 5), "Var - x/4", mp.nstr(m2 - m1 ** 2 - x / 4, 5))
for x in [4, 8]:
    Z = I3(x)
    def mom(g):
        f = lambda y2, y1: float(g(y1, y2) * multi(x, [y1, y2, x - y1 - y2]))
        return integrate.dblquad(f, 0, x, 0, lambda y1: x - y1, epsabs=1e-10, epsrel=1e-10)[0] / Z
    e1, e11, e12 = mom(lambda a, b: a), mom(lambda a, b: a * a), mom(lambda a, b: a * b)
    print("m=3 x=%g mean-x/3=%.2e Var-2x/9=%.4f Cov+x/9=%.4f" % (x, e1 - x / 3, e11 - e1 ** 2 - 2 * x / 9, e12 - e1 ** 2 + x / 9))
    # S_m invariance of M2 under transposition 1<->3 (linear part L)
    M2 = np.array([[e11, e12], [e12, e11]])
    L = np.array([[-1.0, -1.0], [0.0, 1.0]])
    Cv = M2 - (x / 3) ** 2 * np.ones((2, 2))
    print("  |L M2 L^T - M2| =", np.abs(L @ M2 @ L.T - M2).max(), " |L Cov L^T - Cov| =", np.abs(L @ Cv @ L.T - Cv).max())

print("== Remark no-semigroup numbers ==")
G1i = mp.quad(lambda y: C(1, y) * mp.exp(-1j * y), [0, 1]) / I2(1)
print("G_1(i) =", mp.nstr(G1i, 6), " lattice:", mp.nstr((1 + mp.exp(-1j)) / 2, 6))
Kt = lambda a, y: C(a, y) / I2(a) if 0 <= y <= a else 0
conv = mp.quad(lambda s: Kt(1.5, s) * Kt(2, 0.5 - s), [0, 0.5])
print("(K1.5*K2)(0.5) =", mp.nstr(conv, 6), " K3.5(0.5) =", mp.nstr(Kt(3.5, 0.5), 6))

print("== m=2 symbol small-k: sigma/k^2 vs E[y^2]/(2 a^2) and (1+a)/(8a) ==")
for a in [5.0, 30.0]:
    Z = I2(a)
    Ey2 = mp.quad(lambda y: y * y * C(a, y), mp.linspace(0, a, 9)) / Z
    k = mp.mpf("1e-4")
    sig = mp.quad(lambda y: C(a, y) * (1 - mp.cos(k * y)), mp.linspace(0, a, 9)) / Z / a ** 2
    print(a, mp.nstr(sig / k ** 2, 8), mp.nstr(Ey2 / (2 * a ** 2), 8), mp.nstr((1 + a) / (8 * a), 8))
