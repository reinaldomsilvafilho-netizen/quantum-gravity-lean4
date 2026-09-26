"""Camada 2, F-45 (cap. 3). Independent checks of the NEW proofs, with mutations.

Independent oracle for I_2: the trigonometric representation of Thm 2.1,
   I_2(z) = 2^z J(z),  J(z) = (2/pi) int_0^{pi/2} cos^z(p) sin(z p)/p dp.
Higher m by the exact reduction  multinom(x; y1..ym) = binom(x,y1) multinom(x-y1; y2..ym):
   I_3(x) = int_0^x binom(x,s) I_2(s) ds,   I_4(x) = int_0^x binom(x,s) I_2(s) I_2(x-s) ds
(the latter from I_4 = Gamma(x+1) (g*g)*(g*g), g = 1/Gamma(.+1), g*g(s) = I_2(s)/Gamma(s+1)).
These are different from the corrector's nested cubature and trapezoid convolution.

T1 Thm 2.1 rate: sqrt(x)|J-(2/pi)Si| bounded; mutation x^{3/2}|...| unbounded at even x.
   Also the two ingredient bounds of the proof.
T2 Thm 3.2: J_3(x) = I_3/3^x -> 1 up to x=80, J_4 -> 1; Gaussian constants; c0 bound; Pinsker.
   Mutation: I_m ~ m^x / sqrt(x) fails.
T3 Thm 5.3 general alpha: lambda_alpha and C_alpha for alpha = 0.3, 1 (C_1 = phi/sqrt5), 3.7.
   Mutation: C_alpha without the factor u_* fails.
T4 Thm 5.4 L^p: ratios -> 1 for p = 0.5, 1.7, 3; mutation sqrt(p) -> p fails.
T5 Thm 5.10 moments (m=3): Var(y1)/(2x/9) -> 1 and Cov(y1,y2)/(-x/9) -> 1; mutation (m-1)x/m fails.
T6 Prop 5.9 hockey stick for r = 0.5, 2.5: (int - binom(x+1,r+1))/x^r bounded and nonzero.
T7 Table 2 (m = 2, 3, 4): values, error %, defect column.  Mutation: old m=4 entries fail.
T8 Star of David at random real (n,k); Rem 7.3 number 5.33.
"""
import math
import numpy as np
from scipy import integrate, special, optimize

FAIL = []


def check(name, ok, info=None):
    print(("PASS " if ok else "FAIL ") + name + ("" if info is None else "  | " + str(info)))
    if not ok:
        FAIL.append(name)


def lb(x, y):
    return math.lgamma(x + 1) - math.lgamma(y + 1) - math.lgamma(x - y + 1)


def J(z):
    if z == 0:
        return 1.0
    return 2 / math.pi * integrate.quad(lambda p: math.cos(p) ** z * math.sin(z * p) / p if p > 0 else z,
                                        0, math.pi / 2, limit=500, epsabs=1e-14, epsrel=1e-13)[0]


def I2(z):
    return 2 ** z * J(z)


# ---------------- T1
xs = [4, 8, 16, 32, 64, 128, 256]
d12 = []; d32 = []
for x in xs:
    Jx = J(x)
    diff = abs(Jx - 2 / math.pi * special.sici(math.pi * x / 2)[0])
    d12.append(diff * math.sqrt(x)); d32.append(diff * x ** 1.5)
check("T1 sqrt(x)|J-(2/pi)Si(pi x/2)| bounded (x=4..256)", max(d12) < 0.2, [round(v, 4) for v in d12])
check("T1-mut x^{3/2}|J-(2/pi)Si| grows (so a rate x^{-3/2} would be false)", d32[-1] > 5 * d32[0], [round(v, 3) for v in d32])
ok = True
for x in (1.0, 2.5, 7.0, 30.0, 100.0):
    lhs = x * integrate.quad(lambda p: math.cos(p) ** (x - 1), 0, math.pi / 2)[0]
    rhs = math.sqrt(math.pi) / 2 * x * math.exp(math.lgamma(x / 2) - math.lgamma((x + 1) / 2))
    m_int = integrate.quad(lambda p: min(1.0, x * p * p / 2) / (p * p) if p > 0 else x / 2, 0, math.pi / 2, points=[math.sqrt(2 / x)] if math.sqrt(2 / x) < math.pi / 2 else None)[0]
    ok &= abs(lhs - rhs) < 1e-8 * rhs and m_int <= math.sqrt(2 * x) + 1e-12
check("T1 proof ingredients: x int cos^{x-1} = (sqrt(pi)/2) x Gamma(x/2)/Gamma((x+1)/2); int min(1,x p^2/2)/p^2 <= sqrt(2x)", ok)

# ---------------- T2
def I3(x):
    return integrate.quad(lambda s: math.exp(lb(x, s)) * I2(s), 0, x, limit=400, epsrel=1e-11)[0]


def I4(x):
    return integrate.quad(lambda s: math.exp(lb(x, s)) * I2(s) * I2(x - s), 0, x, limit=400, epsrel=1e-11)[0]


J3 = {x: I3(x) / 3 ** x for x in (10.0, 20.0, 40.0, 80.0)}
J4 = {x: I4(x) / 4 ** x for x in (10.0, 20.0, 40.0)}
print("   J_3:", {k: round(v, 10) for k, v in J3.items()}, " J_4:", {k: round(v, 8) for k, v in J4.items()})
check("T2 J_3(x) -> 1 monotonically (x=10..80)", 0 < 1 - J3[80.0] < 1 - J3[40.0] < 1 - J3[20.0] < 1 - J3[10.0] and 1 - J3[80.0] < 1e-12)
check("T2 J_4(x) -> 1", 0 < 1 - J4[40.0] < 1 - J4[20.0] < 1 - J4[10.0] and 1 - J4[40.0] < 1e-4)
check("T2 relative defect ~ ((m-1)/m)^x for m=3: (1-J3(40))/(2/3)^40 of order 1", 0.05 < (1 - J3[40.0]) / (2 / 3) ** 40 < 20, (1 - J3[40.0]) / (2 / 3) ** 40)
check("T2-mut I_3 ~ 3^x/sqrt(x) fails", abs(I3(40.0) / (3 ** 40 / math.sqrt(40)) - 1) > 1)
for m in (3, 4, 5):
    x = 7.3
    S = x * (np.eye(m - 1) / m - np.ones((m - 1, m - 1)) / m ** 2)
    ok1 = np.allclose(np.linalg.inv(S), m / x * (np.eye(m - 1) + np.ones((m - 1, m - 1))))
    ok2 = abs(np.linalg.det(S) - x ** (m - 1) / m ** m) < 1e-10 * x ** (m - 1)
    check(f"T2 m={m}: Sigma^-1 and det Sigma as stated", ok1 and ok2)
c0 = optimize.minimize_scalar(special.gamma, bounds=(1, 2), method="bounded").fun
zz = np.concatenate([np.linspace(1e-9, 3, 30001), np.linspace(3, 60, 2000)])
check("T2 c0=min_[1,2] Gamma > 0.88 and Gamma(z+1) >= c0 (z/e)^z on [0,60]",
      c0 > 0.88 and np.all(special.gammaln(zz + 1) >= math.log(c0) + zz * (np.log(zz) - 1) - 1e-12), c0)
rng = np.random.default_rng(3); okp = True
for _ in range(2000):
    m = rng.integers(2, 6); xi = rng.dirichlet(np.ones(m) * 0.3)
    D = np.sum(xi * np.log(np.where(xi > 0, m * xi, 1)))
    okp &= D >= 0.5 * np.sum((xi - 1 / m) ** 2) - 1e-12
check("T2 Pinsker D(xi) >= |xi - u|_2^2 / 2 (2000 random xi)", okp)

# ---------------- T3
phi = (1 + 5 ** 0.5) / 2
for alpha in (0.3, 1.0, 3.7):
    lam = optimize.brentq(lambda z: z ** (alpha + 1) - z ** alpha - 1, 1 + 1e-12, 5)
    xi = optimize.brentq(lambda s: (1 - (alpha + 1) * s) ** (alpha + 1) - s * (1 - alpha * s) ** alpha, 1e-14, 1 / (alpha + 1) - 1e-14)
    u, w = 1 - alpha * xi, 1 - (alpha + 1) * xi
    S2 = alpha ** 2 / u - 1 / xi - (alpha + 1) ** 2 / w
    Ca = math.sqrt(u / (xi * w * abs(S2)))
    Cbad = math.sqrt(1 / (xi * w * abs(S2)))
    x = 300.0
    val = integrate.quad(lambda y: math.exp(lb(x - alpha * y, y) - x * math.log(lam)), 0, x / (1 + alpha), limit=500, epsrel=1e-12, epsabs=0)[0]
    check(f"T3 alpha={alpha}: u*/w* = lambda_alpha and ray/(C_alpha lambda^x) -> 1 (x=300)", abs(u / w - lam) < 1e-10 and abs(val / Ca - 1) < 2e-3, (lam, round(val / Ca, 6)))
    if alpha == 1.0:
        check("T3 C_1 = phi/sqrt5 from the general formula", abs(Ca - phi / 5 ** 0.5) < 1e-12, Ca)
    check(f"T3-mut alpha={alpha}: C_alpha without u* fails", abs(val / Cbad - 1) > 1e-2)

# ---------------- T4
for p in (0.5, 1.7, 3.0):
    r = []
    for x in (200.0, 800.0):
        v = integrate.quad(lambda y: math.exp(p * lb(x, y) - p * x * math.log(2)), 0, x, points=[x / 2], limit=400, epsrel=1e-11)[0]
        pred = 1 / ((math.pi * x / 2) ** ((p - 1) / 2) * math.sqrt(p))
        predbad = 1 / ((math.pi * x / 2) ** ((p - 1) / 2) * p)
        r.append((v / pred, v / predbad))
    check(f"T4 p={p}: L^p ratio -> 1", abs(r[1][0] - 1) < abs(r[0][0] - 1) + 1e-12 and abs(r[1][0] - 1) < 2e-3, [round(a, 5) for a, _ in r])
    check(f"T4-mut p={p}: sqrt(p) -> p fails", abs(r[1][1] - 1) > 0.1)

# ---------------- T5
for x in (10.0, 40.0, 120.0):
    w0 = lambda s: math.exp(lb(x, s) - x * math.log(3)) * I2(x - s)
    Z = integrate.quad(w0, 0, x, limit=400, epsrel=1e-11)[0]
    m1 = integrate.quad(lambda s: s * w0(s), 0, x, limit=400, epsrel=1e-11)[0] / Z
    m2 = integrate.quad(lambda s: s * s * w0(s), 0, x, limit=400, epsrel=1e-11)[0] / Z
    var = m2 - m1 ** 2
    cov = -var / 2  # Var(y1+y2+y3)=0 and exchangeability
    print("   x=%5.1f  <y1>-x/3=%.2e  Var/(2x/9)=%.6f  Cov/(-x/9)=%.6f" % (x, m1 - x / 3, var / (2 * x / 9), cov / (-x / 9)))
check("T5 <y1> = x/3 exactly", abs(m1 - x / 3) < 1e-6 * x)
check("T5 Var(y1)/(2x/9) -> 1", abs(var / (2 * x / 9) - 1) < 0.01)
check("T5-mut Var ~ (m-1)x/m fails", abs(var / (2 * x / 3) - 1) > 0.5)

# ---------------- T6
for r_ in (0.5, 2.5):
    vals = []
    for x in (100.0, 400.0, 1600.0):
        I = integrate.quad(lambda t: math.exp(lb(t, r_)), r_, x, limit=400)[0]
        vals.append((I - math.exp(lb(x + 1, r_ + 1))) / x ** r_)
    check(f"T6 r={r_}: (int - binom(x+1,r+1))/x^r converges to a nonzero constant", abs(vals[2] - vals[1]) < abs(vals[1] - vals[0]) + 1e-9 and abs(vals[2]) > 0.05, [round(v, 5) for v in vals])

# ---------------- T7
table = {(2, 1.0): (1.1790, 41.05, 1.0), (2, 2.0): (3.2608, 18.48, 3.0), (2, 5.0): (31.3749, 1.95, 31.0), (2, 10.0): (1023.4546, 0.05, 1023.0),
         (3, 1.0): (0.6438, 78.54, 1.2315), (3, 2.0): (4.2483, 52.80, 4.1088), (3, 5.0): (208.3429, 14.26, 195.9376), (3, 10.0): (58076.7465, 1.65, 57513.8181),
         (4, 1.0): (0.2270, 94.33, 2.7124), (4, 2.0): (3.3626, 78.98, 7.5034), (4, 5.0): (662.6556, 35.29, 607.3142), (4, 10.0): (967463.2, 7.74, 932422.5)}
Ifun = {2: I2, 3: I3, 4: I4}
okv = okp = okd = True
for (m, x), (v, pct, dm) in table.items():
    a = Ifun[m](x)
    dig = 4 if a < 1e5 else 1
    okv &= abs(a - v) <= 0.6 * 10 ** (-dig)
    okp &= abs(100 * (m ** x - a) / m ** x - pct) <= 0.006
    prev = {2: lambda z: 1.0, 3: I2, 4: I3}[m](x)
    okd &= abs(m ** x - m / 2 * prev - dm) <= 0.6 * 10 ** (-dig)
    print("   m=%d x=%4.1f  I=%.6f table=%s  err%%=%.3f  defect=%.4f" % (m, x, a, v, 100 * (m ** x - a) / m ** x, m ** x - m / 2 * prev))
check("T7 Table 2 values (third independent method)", okv)
check("T7 Table 2 error-% column", okp)
check("T7 Table 2 defect column m^x - (m/2) I_{m-1}", okd)
check("T7-mut old m=4 entries 3.3633/662.1933/968904.8 fail", abs(I4(2.0) - 3.3633) > 5e-4 and abs(I4(5.0) - 662.1933) > 0.1 and abs(I4(10.0) - 968904.8) > 1)
check("T7 text: heuristic errs by ~563 at m=3,x=10 while 3^x - I_3 ~ 972",
      abs(abs(57513.8181 - I3(10.0)) - 563) < 1 and abs(3 ** 10 - I3(10.0) - 972) < 1)

# ---------------- T8
ok = True
for _ in range(200):
    n, k = rng.uniform(3, 20), rng.uniform(1.5, 2.5)
    L_ = lb(n - 1, k - 1) + lb(n, k + 1) + lb(n + 1, k); R_ = lb(n - 1, k) + lb(n, k - 1) + lb(n + 1, k + 1)
    ok &= abs(L_ - R_) < 1e-10
check("T8 Star of David at 200 random real (n,k)", ok)
Lm = np.array([[-1, -1], [0, 1]]); D1 = Lm @ np.ones((2, 2)) @ Lm.T - np.ones((2, 2))
dev = 16 / 9 * D1
check("T8 Rem 7.3: 5.33 = max-entry norm of L M2 L^T - M2 (alpha=4, m=3); spectral norm differs",
      abs(np.abs(dev).max() - 16 / 3) < 1e-12 and abs(np.linalg.norm(dev, 2) - 16 / 3) > 1, (np.abs(dev).max(), np.linalg.norm(dev, 2)))
print("\nFAILURES:", FAIL if FAIL else "none")
