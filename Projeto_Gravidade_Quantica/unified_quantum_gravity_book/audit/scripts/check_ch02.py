"""Independent checks for Chapter 2 (audit 2026-09-24)."""
import numpy as np
from scipy.linalg import expm, qr, logm
from scipy.integrate import solve_ivp

rng = np.random.default_rng(0)

# 1. Graphon heat equation: exact solution vs numerical ODE on an n x n step graphon
n = 12
W0 = rng.uniform(0, 1, (n, n)); W0 = (W0 + W0.T) / 2
def rhs(t, w):
    W = w.reshape(n, n)
    d = W.mean(axis=1)
    return (d[:, None] + d[None, :] - 2 * W).ravel()
t = 0.7
num = solve_ivp(rhs, (0, t), W0.ravel(), rtol=1e-12, atol=1e-14).y[:, -1].reshape(n, n)
d0 = W0.mean(axis=1); m = W0.mean()
exact = np.exp(-2*t)*W0 + (np.exp(-t)-np.exp(-2*t))*(d0[:, None]+d0[None, :]) + (1-np.exp(-t))**2*m
print("heat exact-vs-ODE max err:", np.abs(num-exact).max())

# cut norm (step graphon, exact by enumeration over unions of blocks is 2^n x 2^n; use n small)
def cutnorm(W):
    k = W.shape[0]; best = 0.0
    for s in range(1, 2**k):
        S = np.array([(s >> i) & 1 for i in range(k)], bool)
        r = W[S].sum(axis=0) / k**2
        best = max(best, r[r > 0].sum(), -r[r < 0].sum())
    return best
k = 8
V0 = rng.normal(size=(k, k)); V0 = (V0 + V0.T) / 2
dv = V0.mean(axis=1); mv = V0.mean()
vals = []
for tt in (0, 0.2, 0.5, 1, 2, 5):
    Wt = np.exp(-2*tt)*V0 + (np.exp(-tt)-np.exp(-2*tt))*(dv[:, None]+dv[None, :]) + (1-np.exp(-tt))**2*mv
    vals.append(cutnorm(Wt))
print("cut norms along flow (signed kernel):", np.round(vals, 5), "non-increasing:", all(np.diff(vals) <= 1e-12))

# 2. Toda flow vs QR of exp(t A0)
A0 = rng.normal(size=(5, 5)); A0 = (A0 + A0.T) / 2
def pi_so(X):
    L = np.tril(X, -1); return L - L.T
def toda(t, a):
    A = a.reshape(5, 5); P = pi_so(A); return (A @ P - P @ A).ravel()
T = 1.0
At = solve_ivp(toda, (0, T), A0.ravel(), rtol=1e-12, atol=1e-12).y[:, -1].reshape(5, 5)
Q, R = qr(expm(T * A0)); S = np.diag(np.sign(np.diag(R))); Q = Q @ S
print("Toda A(1) vs Q^T A0 Q (Q from QR of e^{A0}):", np.abs(At - Q.T @ A0 @ Q).max())
Qa, Ra = qr(A0); Sa = np.diag(np.sign(np.diag(Ra))); Qa, Ra = Qa @ Sa, Sa @ Ra
print("Toda A(1) vs one unshifted QR step on A0 (R Q):", np.abs(At - Ra @ Qa).max())
Qe, Re = qr(expm(A0)); Se = np.diag(np.sign(np.diag(Re))); Qe, Re = Qe @ Se, Se @ Re
print("exp(A(1)) vs one QR step on e^{A0}:", np.abs(expm(At) - Re @ Qe).max())

# 3. Trace ordering: Tr(A1...Ak) vs Tr(P exp) with dU/ds = A U
r = 3; kk = 4000
Afun = lambda s: np.array([[0, 1+s, 0], [0, 0, s], [s*s, 0, 0.5]])
mats = [np.eye(r) + Afun((j+1)/kk)/kk for j in range(kk)]
fwd = np.eye(r); bwd = np.eye(r)
for M_ in mats: fwd = fwd @ M_     # A1 A2 ... Ak
for M_ in mats: bwd = M_ @ bwd     # Ak ... A1
U = solve_ivp(lambda s, u: (Afun(s) @ u.reshape(r, r)).ravel(), (0, 1), np.eye(r).ravel(), rtol=1e-12, atol=1e-12).y[:, -1].reshape(r, r)
print("Tr(Ak...A1) - Tr(Pexp):", np.trace(bwd) - np.trace(U), "| Tr(A1...Ak) - Tr(Pexp):", np.trace(fwd) - np.trace(U))

# 4. Affine-invariant gradient flow of 1/2 d(A,I)^2 in the scalar case
a = 5.0; f = lambda x: 0.5*np.log(x)**2
grad_ai = a**2 * (np.log(a)/a)   # g = u^2/a^2  => grad = a^2 f'
print("AI gradient of 1/2 log^2 at a=5:", grad_ai, "= a log a:", a*np.log(a))
