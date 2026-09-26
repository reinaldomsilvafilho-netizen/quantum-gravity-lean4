"""Independent check of the connected-component obstruction (ch10, Conj. 3.1).
f(x) = W2 tanh(W1 x), W_i in O(2). Teacher W1 = R(a) diag(1,-1), W2 = I (prod det = -1).
Oracle: multistart L-BFGS over the 4 components (s1, s2) in {+1,-1}^2 parametrized by angles.
Expect: components with s1*s2 = -1 reach 0; components with s1*s2 = +1 stay bounded away.
Negative control: teacher with prod det = +1 is fitted in SO(2)^2.
"""
import numpy as np
from scipy.optimize import minimize

R = lambda a: np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
F = np.diag([1.0, -1.0])


def comp(a, s):
    return R(a) @ (F if s < 0 else np.eye(2))


for seed in (3, 11, 29):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(40, 2)) * 1.5
    net = lambda W1, W2: np.tanh(X @ W1.T) @ W2.T
    Yb = net(R(0.7) @ F, np.eye(2))
    Yg = net(R(0.7), R(-0.4))
    res = {}
    for s1 in (1, -1):
        for s2 in (1, -1):
            best = min(
                minimize(lambda p: np.mean(np.sum((net(comp(p[0], s1), comp(p[1], s2)) - Yb) ** 2, 1)),
                         rng.uniform(0, 2 * np.pi, 2), method="L-BFGS-B").fun
                for _ in range(40))
            res[(s1, s2)] = best
    good = min(minimize(lambda p: np.mean(np.sum((net(R(p[0]), R(p[1])) - Yg) ** 2, 1)),
                        rng.uniform(0, 2 * np.pi, 2), method="L-BFGS-B").fun for _ in range(40))
    print(seed, {k: round(v, 4) for k, v in res.items()}, "control", f"{good:.1e}")
    assert res[(1, -1)] < 1e-8 and res[(-1, 1)] < 1e-8
    assert res[(1, 1)] > 0.5 and res[(-1, -1)] > 0.5
    assert abs(res[(1, 1)] - res[(-1, -1)]) < 1e-6  # sign-flip symmetry
    assert good < 1e-8
print("OK")
