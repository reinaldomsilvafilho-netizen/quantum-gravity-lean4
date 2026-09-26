"""More Chapter 3 checks: Dixon integral, variance, Barnes-G row entropy, alternating integral."""
import numpy as np
import mpmath as mp
from scipy import integrate, special

def lb(x, y):
    return special.gammaln(x + 1) - special.gammaln(y + 1) - special.gammaln(x - y + 1)

print("Dixon: x, integral / (1/2 multinomial(3x;x,x,x))")
for x in (3, 5, 8, 12, 16):
    f = lambda t: np.cos(np.pi*t)*np.exp(3*lb(2*x, x+t) - (special.gammaln(3*x+1) - 3*special.gammaln(x+1)))
    val = integrate.quad(f, -x, x, limit=2000, epsabs=0, epsrel=1e-11)[0]
    print(f"  {x}: {val/0.5:.6f}")

print("Variance of normalized continuous binomial (m=2): x, Var, x/4")
for x in (4, 10, 20, 40):
    w = lambda y: np.exp(lb(x, y) - x*np.log(2))
    Z = integrate.quad(w, 0, x)[0]
    mu = integrate.quad(lambda y: y*w(y), 0, x)[0]/Z
    v = integrate.quad(lambda y: (y-mu)**2*w(y), 0, x)[0]/Z
    print(f"  {x}: {v:.5f}  {x/4:.5f}  diff={v-x/4:+.5f}")

print("Barnes row entropy: x, numeric, formula")
for x in (1.5, 3, 7.2):
    num = integrate.quad(lambda y: lb(x, y), 0, x)[0]
    formula = x*(x+1) - x*np.log(2*np.pi) - x*special.gammaln(x+1) + 2*float(mp.log(mp.barnesg(x+1)))
    print(f"  {x}: {num:.8f}  {formula:.8f}")

print("Alternating integral A(x) = int cos(pi y) binom(x,y): x, A(x)")
for x in (3, 4, 4.5, 7, 10.3, 20.5):
    A = integrate.quad(lambda y: np.cos(np.pi*y)*np.exp(lb(x, y)), 0, x, limit=400)[0]
    print(f"  {x}: {A:+.6e}")
