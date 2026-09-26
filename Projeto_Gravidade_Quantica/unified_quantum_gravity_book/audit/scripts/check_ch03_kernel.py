"""Does the continuous Beta-kernel satisfy the discrete multinomial generating-function identity? (Ch. 3, Prop. 6.3)"""
import numpy as np
from scipy import integrate, special

def binom(x, y):
    return np.exp(special.gammaln(x + 1) - special.gammaln(y + 1) - special.gammaln(x - y + 1))

def I(a):
    return integrate.quad(lambda y: binom(a, y), 0, a, epsrel=1e-12)[0]

print("m=2 symbol: alpha, k, true K_hat(k) = (1/I)∫ binom e^{-iky}, claimed ((1+e^{-ik})/2)^alpha")
for a in (0.5, 1.0, 2.5, 6.0):
    for k in (0.3, 1.0, 2.0):
        re = integrate.quad(lambda y: binom(a, y)*np.cos(k*y), 0, a, epsrel=1e-12)[0]
        im = -integrate.quad(lambda y: binom(a, y)*np.sin(k*y), 0, a, epsrel=1e-12)[0]
        true = (re + 1j*im)/I(a)
        claimed = ((1 + np.exp(-1j*k))/2)**a
        print(f"  a={a:4} k={k:3}: true={true:.5f}  claimed={claimed:.5f}  |diff|={abs(true-claimed):.2e}")

print("Semigroup (Chu-Vandermonde): (K_a * K_b)(s) vs K_{a+b}(s), normalized kernels, m=2")
a, b = 1.5, 2.0
Ka = lambda y: binom(a, y)/I(a) if 0 <= y <= a else 0.0
Kb = lambda y: binom(b, y)/I(b) if 0 <= y <= b else 0.0
for s in (0.5, 1.75, 3.0):
    conv = integrate.quad(lambda y: Ka(y)*Kb(s-y), max(0, s-b), min(a, s), epsrel=1e-10)[0]
    print(f"  s={s}: conv={conv:.6f}  K_(a+b)={binom(a+b, s)/I(a+b):.6f}")

print("Integer alpha=n: discrete multinomial holds only for the lattice SUM:")
n, k = 4, 1.0
disc = sum(special.comb(n, j)*np.exp(-1j*k*j) for j in range(n+1))/2**n
print("  lattice sum:", np.round(disc, 6), " claimed:", np.round(((1+np.exp(-1j*k))/2)**n, 6))
