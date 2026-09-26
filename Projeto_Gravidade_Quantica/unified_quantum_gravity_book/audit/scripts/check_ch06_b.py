"""Chapter 6, second batch: sharper remainder of E(x), reflection formula, parity counts."""
import mpmath as mp
from math import comb
mp.mp.dps = 30

def E(x):
    x = mp.mpf(x)
    return x*(x+1) - x*mp.log(2*mp.pi) - x*mp.loggamma(x+1) + 2*mp.log(mp.barnesg(x+1))

const = 2*mp.diff(mp.zeta, -1) - mp.mpf(1)/12
print("remainder vs -(1/6)ln x + 2 zeta'(-1) - 1/12  (difference should be O(1/x))")
for x in (10, 100, 1000, 10000):
    approx = mp.mpf(x)**2/2 - mp.mpf(x)/2*mp.log(x) + (1 - mp.log(2*mp.pi)/2)*x - mp.log(x)/6 + const
    d = E(x) - approx
    print(f"  x={x}: diff={mp.nstr(d, 6)}  x*diff={mp.nstr(d*x, 6)}")
# negative control: coefficient -1/12 instead of -1/6 must fail
x = 10000
bad = E(x) - (mp.mpf(x)**2/2 - mp.mpf(x)/2*mp.log(x) + (1 - mp.log(2*mp.pi)/2)*x - mp.log(x)/12 + const)
print("  negative control (1/12 ln x):", mp.nstr(bad, 6))

print("reflection formula")
for x, y in [(2.3, 0.7), (5.5, 1.2), (-1.7, 0.4)]:
    b = mp.binomial(x, y)
    r = -(1/mp.pi)*mp.sin(mp.pi*y)*mp.sin(mp.pi*(x-y))/mp.sin(mp.pi*x)*mp.gamma(y-x)*mp.gamma(-y)/mp.gamma(-x)
    print(f"  ({x},{y}): {mp.nstr(b,12)}  {mp.nstr(r,12)}")

print("odd entries: rows n<2^k (positive) and binom(-a,j), a=1..2^k, j<2^k with a+j-1<2^k (negative)")
for k in range(1, 9):
    N = 2**k
    pos = sum(1 for n in range(N) for j in range(n+1) if comb(n, j) % 2)
    neg = sum(1 for a in range(1, N+1) for j in range(N) if a+j-1 < N and comb(a+j-1, j) % 2)
    print(f"  k={k}: pos={pos} neg={neg} 3^k={3**k}")
