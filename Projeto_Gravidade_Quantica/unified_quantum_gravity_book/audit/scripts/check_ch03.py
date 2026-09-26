"""Independent checks for Chapter 3 (audit 2026-09-24)."""
import numpy as np
from scipy import integrate, special

def binom(x, y):
    return np.exp(special.gammaln(x + 1) - special.gammaln(y + 1) - special.gammaln(x - y + 1))

def I2(x):
    return integrate.quad(lambda y: binom(x, y), 0, x, limit=400, epsabs=0, epsrel=1e-12)[0]

def J_trig(x):
    return 2/np.pi*integrate.quad(lambda p: np.cos(p)**x*np.sin(x*p)/p if p > 0 else x, 0, np.pi/2, limit=800, epsabs=0, epsrel=1e-12)[0]

print("2D row integral: x, I/2^x, J_trig, 1-1/(2x), 2^x - I")
for x in (1, 2, 3.5, 5, 10, 20, 30):
    I = I2(x)
    print(f"  {x:5}: {I/2**x:.8f}  {J_trig(x):.8f}  {1-1/(2*x):.6f}  {2**x - I:.6f}")

def I3(x):
    f = lambda y2, y1: np.exp(special.gammaln(x+1)-special.gammaln(y1+1)-special.gammaln(y2+1)-special.gammaln(x-y1-y2+1))
    return integrate.dblquad(f, 0, x, 0, lambda y1: x - y1, epsabs=0, epsrel=1e-10)[0]

print("m=3: n, I3/3^n, 3^n - I3, (3/2) I2(n), (3^n/n)")
for n_ in (2, 4, 6, 8, 10, 12, 14):
    a = I3(n_)
    print(f"  {n_:3}: {a/3**n_:.8f}  {3**n_ - a:12.4f}  {1.5*I2(n_):12.4f}  {3**n_/n_:12.1f}")

# Fibonacci diagonal
phi = (1+5**0.5)/2
print("Fibonacci diagonal: x, F_cont / (phi^(x+1)/sqrt5)")
for x in (5, 10, 20, 40):
    F = integrate.quad(lambda y: binom(x-y, y), 0, x/2, limit=400)[0]
    print(f"  {x}: {F/(phi**(x+1)/5**0.5):.6f}")

# Star of David at non-integer points
n, k = 7.3, 2.6
lhs = binom(n-1, k-1)*binom(n, k+1)*binom(n+1, k); rhs = binom(n-1, k)*binom(n, k-1)*binom(n+1, k+1)
print("Star of David rel diff:", abs(lhs/rhs-1))
