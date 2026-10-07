"""OBL-008 counterexample: unit disk, weight Phi(A) = 1 (admissible: C^1, >= c0 > 0).
lambda_p^{1/p} = R1(p), first zero of radial solution with lambda = 1 (homogeneity scaling).
Oracle A: p = 2 -> j_{0,1}. Oracle B: rigorous test-function bound with u = 1 - r:
   lambda_p <= (p+1)(p+2)/2.
Paper claims limit = h(A). Dirichlet Cheeger constant (full perimeter) of the unit disk = 2;
with the paper's relative perimeter (boundary excluded) h = 0 (take E = Omega).
Known (Juutinen-Lindqvist-Manfredi 1999): limit = 1/inradius = 1.
Refinement: two tolerance levels and two starting radii."""
import numpy as np, sys
from scipy.integrate import solve_ivp
from scipy.special import jn_zeros
fails = 0


def R1(p, rtol, r0):
    q = 1.0 / (p - 1)

    def f(r, y):
        u, w = y
        s = w / r
        up = -abs(s) ** q if s < 0 else abs(s) ** q
        return [up, -r * np.sign(u) * abs(u) ** (p - 1)]

    ev = lambda r, y: y[0]
    ev.terminal, ev.direction = True, -1
    y0 = [1.0 - (p - 1) / p * (r0 / 2) ** (p / (p - 1)) * 2 ** 0, -r0 ** 2 / 2]
    sol = solve_ivp(f, [r0, 50], y0, events=ev, rtol=rtol, atol=rtol * 1e-3, method='LSODA')
    return sol.t_events[0][0]


print('p=2 check: R1 = %.8f, j01 = %.8f' % (R1(2, 1e-11, 1e-8), jn_zeros(0, 1)[0]))
fails += abs(R1(2, 1e-11, 1e-8) - jn_zeros(0, 1)[0]) > 1e-5
print(' p    R1(tol1e-8,r0=1e-6)  R1(tol1e-11,r0=1e-8)  upper bound  |claim h=2 (full perim)')
last = None
for p in [2, 4, 8, 16, 32, 64]:
    a = R1(p, 1e-8, 1e-6)
    b = R1(p, 1e-11, 1e-8)
    ub = ((p + 1) * (p + 2) / 2) ** (1 / p)
    print('%3d   %.6f            %.6f              %.6f' % (p, a, b, ub))
    fails += abs(a - b) > 1e-4 * b
    fails += b > ub + 1e-9  # numeric must respect rigorous bound
    last = b
print('lambda_64^(1/64) = %.4f ; claim (h=2) requires -> 2 ; JLM value 1/R = 1' % last)
fails += not (last < 1.2)   # consistent with limit 1
fails += (abs(last - 2) < 0.5)  # negative control: the paper's claim would sit here
print('failures:', fails)
sys.exit(int(fails))
