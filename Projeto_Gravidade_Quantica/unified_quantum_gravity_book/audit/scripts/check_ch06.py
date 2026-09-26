"""Chapter 6 checks: asymptotics of the row entropy E(x) (Barnes G) and Kigami constants."""
import mpmath as mp
mp.mp.dps = 30

def E(x):
    x = mp.mpf(x)
    return x*(x+1) - x*mp.log(2*mp.pi) - x*mp.loggamma(x+1) + 2*mp.log(mp.barnesg(x+1))

print("x, E(x) - [x^2/2 - (x/2) ln x + (1 - ln(2pi)/2) x], / ln x")
for x in (10, 50, 200, 1000):
    approx = mp.mpf(x)**2/2 - mp.mpf(x)/2*mp.log(x) + (1 - mp.log(2*mp.pi)/2)*x
    r = E(x) - approx
    print(f"  {x}: {mp.nstr(r, 8)}   {mp.nstr(r/mp.log(x), 6)}")

# Kigami constants for the Sierpinski m-simplex (m+1 cells, ratio 1/2)
for m in (2, 3, 4):
    dH = mp.log(m+1)/mp.log(2); ds = 2*mp.log(m+1)/mp.log(m+3)
    print(f"m={m}: d_H={mp.nstr(dH,6)}, d_s={mp.nstr(ds,6)}, d_w=2 d_H/d_s={mp.nstr(2*dH/ds,6)} = log2(m+3)={mp.nstr(mp.log(m+3)/mp.log(2),6)}")
