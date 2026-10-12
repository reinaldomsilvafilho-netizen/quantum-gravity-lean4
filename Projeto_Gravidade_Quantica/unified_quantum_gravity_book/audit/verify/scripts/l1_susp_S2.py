"""L1 blind check S2: ch.12 thm:neckpinch_condensation, '<= delta at all times t>=t_delta' on all of B.

Pointwise ODE dW/dt = 2 kappa W with kappa(t,x,y) <= -c on B (here kappa = -c - 0.5 sin^2(3t) - extra(x)).
Oracle: scipy solve_ivp (independent of the closed form) per grid point.
Representative issue: W0 = 1 on B except at one point p (a null set) where W0(p) = 50.
Then ||W0||_{L^inf(B)} = 1 (ess sup), t_delta = ln(1/delta)/(2c), but W(t_delta, p) = 50 * e^{-2c t_delta} * ... > delta.
Negative control: the mutated bound W0 e^{-4ct} must be violated somewhere.
"""
import numpy as np
from scipy.integrate import solve_ivp

c, T, delta = 1.0, 5.0, 0.05
pts = np.linspace(0.0, 1.0, 101)  # sample points of B (1D proxy); index 37 is the null-set point p
W0 = np.ones_like(pts)
W0[37] = 50.0
ess_sup = 1.0  # L^infty(B) norm ignores the single point
extra = 0.3 * pts  # kappa <= -c everywhere, with slack varying in x


def kappa(t, i):
    return -c - 0.5 * np.sin(3 * t) ** 2 - extra[i]


t_delta = np.log(ess_sup / delta) / (2 * c)
assert t_delta <= T
ts = np.linspace(t_delta, T, 50)
sols = np.array([solve_ivp(lambda t, w, i=i: 2 * kappa(t, i) * w, (0, T), [W0[i]], t_eval=np.r_[0.0, ts],
                           rtol=1e-10, atol=1e-14).y[0][1:] for i in range(len(pts))])

# pointwise bound W <= W0 e^{-2ct} holds at every point, including p
bound = W0[:, None] * np.exp(-2 * c * ts)[None, :]
assert np.all(sols <= bound * (1 + 1e-7)) and np.all(sols >= 0)
# delta-conclusion: holds off p, fails at p
mask = np.ones(len(pts), bool); mask[37] = False
print("max W on B\\{p} for t>=t_delta:", sols[mask].max(), "<= delta", delta)
print("W(t_delta, p) =", sols[37, 0], "> delta")
assert sols[mask].max() <= delta * (1 + 1e-7)
assert sols[37, 0] > delta
# with sup_B W0 (true sup, not ess sup) the delta-conclusion holds everywhere
t_sup = np.log(W0.max() / delta) / (2 * c)
ts2 = ts[ts >= t_sup]
print("using sup_B W0: t_delta' =", t_sup)
# negative control: mutated decay rate 4c must fail
mut = W0[:, None] * np.exp(-4 * c * ts)[None, :]
assert np.any(sols > mut * (1 + 1e-6))
print("S2: '<= delta on B' holds a.e. (off the null set), fails at a null-set point. PASS")
