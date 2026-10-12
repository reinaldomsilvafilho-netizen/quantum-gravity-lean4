"""L2 directed check S2: ch.12 thm:neckpinch_condensation, as now stated.

Current text (chap12, l.405-413): conclusion changed to
  "W(t,x,y) <= delta for almost every (x,y) in B and all t in [t_delta, T]"
(was: "the entries on B are at most delta at all times", i.e. pointwise everywhere).
Proof now ends with the explicit a.e. step: W_0 <= ||W_0||_{L^inf(B)} a.e. on B.

Independent oracle: solve_ivp (scipy), per-point ODE dW/dt = 2*kappa(t,x)*W(t,x),
kappa(t,x) <= -c for all t, with a representative with one exceptional point.
"""
import numpy as np
from scipy.integrate import solve_ivp

c, T, delta = 1.0, 6.0, 0.05
pts = np.linspace(0.0, 1.0, 201)
p_idx = 83  # the single exceptional point (measure zero in the continuum limit)
W0 = np.ones_like(pts)
W0[p_idx] = 50.0
ess_sup = 1.0  # L^infty(B) ignores the single point
true_sup = W0.max()

extra = 0.4 * pts  # kappa <= -c for all x, with varying slack -> hypothesis holds everywhere


def kappa(t, i):
    return -c - 0.6 * np.sin(2.7 * t) ** 2 - extra[i]


t_delta = np.log(ess_sup / delta) / (2 * c)
assert t_delta <= T
ts = np.linspace(t_delta, T, 40)
sols = np.array([
    solve_ivp(lambda t, w, i=i: 2 * kappa(t, i) * w, (0, T), [W0[i]],
              t_eval=ts, rtol=1e-11, atol=1e-14).y[0]
    for i in range(len(pts))
])

mask_ae = np.ones(len(pts), bool)
mask_ae[p_idx] = False

# current text: holds a.e. on B (off the single exceptional point) for t >= t_delta
assert sols[mask_ae].max() <= delta * (1 + 1e-7)
print(f"current statement (a.e.): max W off exceptional point = {sols[mask_ae].max():.5f} <= delta={delta}  CONFIRMA")

# the exceptional point itself violates the OLD ("every point") reading
print(f"exceptional point: W(t_delta,p) = {sols[p_idx,0]:.4f} > delta -> old 'every (x,y)' wording would be false")
assert sols[p_idx, 0] > delta

# not an under-correction: with sup_B W0 (true sup, not ess sup) the pointwise bound DOES hold
# everywhere, so the proposition's inequality (line before, "0 <= W <= W0 e^{-2ct}") -- which the
# fix left untouched -- is still pointwise-exact and not weakened beyond what's needed.
bound_pointwise = W0[:, None] * np.exp(-2 * c * ts)[None, :]
assert np.all(sols <= bound_pointwise * (1 + 1e-7))
print("pointwise inequality 0<=W<=W0 e^{-2ct} (untouched by the fix) holds everywhere: no over-correction there")

# mutation 1: decay rate doubled (4c instead of 2c) must fail
mut_rate = W0[:, None] * np.exp(-4 * c * ts)[None, :]
assert np.any(sols > mut_rate * (1 + 1e-6))
print("mutation (rate 4c): violated as expected")

# mutation 2: claim "<=delta for EVERY (x,y) in B" (not a.e.) with ess sup -- must fail at p
mutated_every_point_holds = bool(sols[:, 0].max() <= delta * (1 + 1e-7))
assert mutated_every_point_holds is False
print("mutation ('every point' instead of 'a.e.'): violated at exceptional point, as expected")

print("S2 L2: new a.e. statement matches the proof; underlying pointwise inequality unaffected. CONFIRMA")
