"""Corrector-side checks for suspicions A1, A2, A5 (2026-10-10).
Independent of the L1 scripts. Each check has an oracle and a negative control.
A1: box sup of a bilinear form over [0,1]^n x [0,1]^n equals the max over indicator pairs
    (oracle: exhaustive LP vertex enumeration, i.e. alternating exact maximisation from random
    starts can never exceed the indicator max). Negative control: on [-1,1] the sup exceeds it.
A2: non-circular route. A from solve_ivp of the Toda ODE; Q from the LINEAR ODE Qdot = Q K(t)
    with K(t) = Pi_so(A(t)) taken from the stored solution; compare Q^T A0 Q with A, and with the
    positive-diagonal QR of expm(t A0). Negative control: QR without sign fix.
A5: limit of the RHS of the y-PDE on y = -1 equals the numerical derivative.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm, qr
import mpmath as mp

rng = np.random.default_rng(7)

# ---------- A1 ----------
def ind_max(W):
    n = W.shape[0]
    best = 0.0
    for s in range(1 << n):
        u = np.array([(s >> i) & 1 for i in range(n)], float)
        g = u @ W
        best = max(best, abs(g[g > 0].sum()), abs(g[g < 0].sum()))
    return best

def box_sup(W, lo, trials=300):
    n = W.shape[0]
    best = 0.0
    for _ in range(trials):
        for sgn in (1.0, -1.0):
            u = rng.uniform(lo, 1, n); v = rng.uniform(lo, 1, n)
            for _ in range(50):
                g = sgn * (W @ v)
                u = np.where(g > 0, 1.0, lo)
                h = sgn * (u @ W)
                v = np.where(h > 0, 1.0, lo)
            best = max(best, abs(u @ W @ v))
        # also continuous random points (never better than vertices)
        uu = rng.uniform(lo, 1, n); vv = rng.uniform(lo, 1, n)
        best = max(best, abs(uu @ W @ vv))
    return best

a1 = []
for _ in range(6):
    n = 7
    W = rng.normal(size=(n, n)) / n**2
    c = ind_max(W)
    a1.append((box_sup(W, 0.0) - c, box_sup(W, -1.0) / c))
print("A1 box[0,1] sup - indicator max (must be <= 1e-15):", max(x[0] for x in a1))
print("A1 neg control [-1,1] sup / indicator max (must exceed 1):", min(x[1] for x in a1), max(x[1] for x in a1))

# ---------- A2 ----------
def pso(X):
    L = np.tril(X, -1)
    return L - L.T

n = 5
M = rng.normal(size=(n, n)); A0 = (M + M.T) / 2
toda = solve_ivp(lambda t, a: (lambda A: (A @ pso(A) - pso(A) @ A).ravel())(a.reshape(n, n)),
                 (0, 2), A0.ravel(), rtol=1e-12, atol=1e-13, dense_output=True)
Afun = lambda t: toda.sol(t).reshape(n, n)
lin = solve_ivp(lambda t, q: (q.reshape(n, n) @ pso(Afun(t))).ravel(), (0, 2), np.eye(n).ravel(),
                rtol=1e-12, atol=1e-13, dense_output=True)

def qr_pos(X, fix=True):
    Q, R = qr(X)
    if fix:
        s = np.sign(np.diag(R)); Q = Q * s; R = (R.T * s).T
    return Q, R

for t in (0.5, 1.0, 2.0):
    Q = lin.sol(t).reshape(n, n)
    Qq, _ = qr_pos(expm(t * A0))
    Qn, _ = qr(expm(t * A0))
    print(f"A2 t={t}: |QQ^T-I|={np.abs(Q@Q.T-np.eye(n)).max():.1e}  |Q^TA0Q - A|={np.abs(Q.T@A0@Q-Afun(t)).max():.1e}"
          f"  |Q_lin - Q_QR+|={np.abs(Q-Qq).max():.1e}  negctl |QnoFix^TA0QnoFix - A|={np.abs(Qn.T@A0@Qn-Afun(t)).max():.2f}")
print("A2 Frobenius norm conserved:", abs(np.linalg.norm(Afun(2.0)) - np.linalg.norm(A0)))

# ---------- A5 ----------
mp.mp.dps = 30
C = lambda x, y: mp.gamma(x + 1) * mp.rgamma(y + 1) * mp.rgamma(x - y + 1)
x0 = mp.mpf('0.7')
d = mp.diff(lambda y: C(x0, y), -1)
lim = mp.limit(lambda y: C(x0, y) * (mp.digamma(x0 - y + 1) - mp.digamma(y + 1)), -1)
print("A5 d/dy C(0.7,-1) =", mp.nstr(d, 15), " limit of RHS =", mp.nstr(lim, 15), " 1/1.7 =", mp.nstr(1 / mp.mpf('1.7'), 15))
mut = -lim
print("A5 negative control (bracket with opposite sign) differs from derivative by:", mp.nstr(abs(mut - d), 5))
y1 = mp.mpf('-0.4')
dg = mp.diff(lambda y: C(x0, y), y1)
rhs = C(x0, y1) * (mp.digamma(x0 - y1 + 1) - mp.digamma(y1 + 1))
mutg = C(x0, y1) * (mp.digamma(x0 - y1) - mp.digamma(y1 + 1))

# ---------- A4 side check: m = 1, alpha = 1, kernel 1/(Gamma(y+1)Gamma(2-y)) on [0,1], normalised ----------
mp.mp.dps = 20
kap = lambda y: mp.rgamma(y + 1) * mp.rgamma(2 - y)
I0 = mp.quad(kap, [0, 1])
R = lambda t: mp.quad(lambda y: kap(y) * mp.cos(t * (y - mp.mpf(1) / 2)), [0, 1]) / I0  # = e^{it/2} K^(t), real by symmetry
print("A4 m=1: R(6.5) =", mp.nstr(R(6.5), 6), " R(6.7) =", mp.nstr(R(6.7), 6), " root:", mp.nstr(mp.findroot(R, 6.6), 10))
print("A4 m=1 control (uniform density): zero at 2pi:", mp.nstr(mp.quad(lambda y: mp.cos(2 * mp.pi * (y - 0.5)), [0, 1]), 3))
print("A5 generic point (0.7,-0.4): |deriv - RHS| =", mp.nstr(abs(dg - rhs), 5), " mutant psi(x-y): ", mp.nstr(abs(dg - mutg), 5))
