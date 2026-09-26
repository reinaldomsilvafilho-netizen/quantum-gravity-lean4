"""Blind check of the U-turn material of chapter 8 (Lemma 3.2, eq. (3.x), Conjecture 3.3).

Fermi coordinates about a geodesic sigma (c = 1):
   H^2 : g = dy^2 + cosh(y)^2 dx^2 ;  S^2 : g = dy^2 + cos(y)^2 dx^2 ;  R^2 : g = dy^2 + dx^2.
theta = angle of the unit tangent w.r.t. the frame e1 = d_x/|d_x|, e2 = d_y, which is parallel along
sigma and along the normal geodesics x = const (so it is "parallel transport along sigma").
Liouville's formula gives   theta' = kappa + (E_y / 2E) cos(theta),   y' = sin(theta),
   E_y/2E = tanh y (H^2), -tan y (S^2), 0 (R^2).   In the code theta' = kappa - HOL(y) cos(theta),
   HOL = -E_y/2E.  (Sign fixed by check A: the opposite sign does NOT reproduce geodesic circles.)

Checks
 A. The formula is validated by an independent oracle: the constant-curvature curve kappa = coth(rho)
    (resp. cot rho) started at (y=-rho, theta=0) must be the geodesic circle of radius rho, i.e. reach
    theta = pi exactly at y = +rho.  Negative control: flipping the sign of the holonomy term fails.
 B. Comparison ODE dY/dtheta = sin(theta) / (k - HOL(Y) cos(theta)), Y(0) = -w/2.
    For k = k0(w) (coth(w/2), cot(w/2), 2/w) one gets Y(pi) = w/2; for k < k0, Y(pi) > w/2.
    Together with the Gronwall argument in the report this is a proof sketch of Conjecture 3.3.
 C. Random search for a counterexample (U-turn inside the band with max |kappa| = 0.97 k0).
    Positive control: the same search with k = 1.03 k0 does find U-turns.
"""
import numpy as np
from scipy.integrate import solve_ivp

HOL = {
    "H2": lambda y: -np.tanh(y),
    "S2": lambda y: np.tan(y),
    "R2": lambda y: 0.0 * y,
}
K0 = {
    "H2": lambda w: 1 / np.tanh(w / 2),
    "S2": lambda w: 1 / np.tan(w / 2),
    "R2": lambda w: 2 / w,
}


def circle_top(space, rho, sign=1.0):
    k = K0[space](2 * rho)

    def rhs(s, u):
        y, th = u
        return [np.sin(th), k - sign * HOL[space](y) * np.cos(th)]

    ev = lambda s, u: u[1] - np.pi
    ev.terminal = True
    sol = solve_ivp(rhs, [0, 50], [-rho, 0.0], events=ev, rtol=1e-11, atol=1e-12, max_step=0.01)
    if sol.t_events[0].size == 0:
        return np.nan
    return sol.y_events[0][0][0]


def comparison(space, w, k):
    def rhs(th, Y):
        den = k - HOL[space](Y[0]) * np.cos(th)
        return [np.sin(th) / den if den > 0 else 1e6]

    sol = solve_ivp(rhs, [0, np.pi], [-w / 2], rtol=1e-11, atol=1e-12, max_step=0.01)
    return sol.y[0, -1]


def random_search(space, w, k, n=4000, steps=4000, ds=None, seed=1):
    rng = np.random.default_rng(seed)
    ds = ds or (w / 400)
    y = rng.uniform(-w / 2, w / 2, n)
    y[: n // 4] = -w / 2  # many start on the lower edge
    th = np.zeros(n)
    alive = np.ones(n, bool)
    success = np.zeros(n, bool)
    # piecewise-constant controls, switching with random intervals; include pure +k / -k
    ctrl = rng.uniform(-1, 1, n) * k
    ctrl[:200] = k
    ctrl[200:400] = -k
    switch_p = rng.uniform(0, 0.05, n)
    switch_p[:400] = 0.0
    hol = HOL[space]
    for _ in range(steps):
        sw = rng.random(n) < switch_p
        ctrl[sw] = rng.choice([-k, k, 0.0], sw.sum()) * rng.uniform(0.5, 1, sw.sum()) ** 0.1
        dth = ctrl - hol(y) * np.cos(th)
        y_new = y + ds * np.sin(th)
        th_new = th + ds * dth
        alive &= np.abs(y_new) <= w / 2 + 1e-9
        y, th = np.where(alive, y_new, y), np.where(alive, th_new, th)
        success |= alive & (np.abs(th) >= np.pi)
        alive &= ~success
    return int(success.sum())


if __name__ == "__main__":
    allok = True
    print("A. geodesic-curvature formula validated on circles (top reached at y = rho):")
    for space in ("H2", "S2", "R2"):
        for rho in (0.3, 0.7, 1.1):
            top = circle_top(space, rho)
            bad = circle_top(space, rho, sign=-1.0) if space != "R2" else np.nan
            ok = abs(top - rho) < 1e-6
            neg = space == "R2" or not (abs(bad - rho) < 1e-3)
            allok &= ok and neg
            print(f"   {space} rho={rho}: y_top={top:.8f}  (flipped-sign control y_top={bad})  ok={ok} neg={neg}")

    print("B. comparison ODE: Y(pi) with k=k0 and k=0.97 k0 (must be = w/2 and > w/2):")
    for space, ws in (("H2", (0.5, 1.5, 3.0)), ("S2", (0.5, 1.2, 1.5)), ("R2", (1.0,))):
        for w in ws:
            k0 = K0[space](w)
            y_eq = comparison(space, w, k0)
            y_lo = comparison(space, w, 0.97 * k0)
            ok = abs(y_eq - w / 2) < 1e-6 and y_lo > w / 2 + 1e-4
            allok &= ok
            print(f"   {space} w={w}: Y_k0(pi)={y_eq:.8f} (w/2={w/2}), Y_0.97k0(pi)={y_lo:.6f}  ok={ok}")

    print("C. random search for U-turns in the band:")
    for space, w in (("H2", 1.0), ("H2", 3.0), ("S2", 1.0), ("S2", 2.4), ("R2", 1.0)):
        k0 = K0[space](w)
        below = random_search(space, w, 0.97 * k0)
        above = random_search(space, w, 1.03 * k0)
        ok = below == 0 and above > 0
        allok &= ok
        print(f"   {space} w={w}: successes with 0.97k0: {below}; positive control 1.03k0: {above}  ok={ok}")

    print("ALL CHECKS PASSED" if allok else "SOME CHECK FAILED")
