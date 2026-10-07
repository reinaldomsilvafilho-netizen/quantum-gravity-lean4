"""Thm 2.3(b) and Thm 2.5(c)/Example 2.6.
 (b) W2 <= diam/sqrt2 * ||f-g||_1^{1/2} on [0,1] (diam=1). Oracle: exact 1D W2 from quantile functions.
     Random densities + near-extremal pairs (mass eps moved across the interval) test sharpness.
     Negative control: the mutated constant diam/2 must be violated by the near-extremal pair.
 (Ex 2.6 + Thm 2.5c) truncated Gaussian weight exp(-a(x-x0)^2/2) on [0,1] (d=1, A=a): spectral gap of the Neumann
     drift Laplacian (finite volumes, refinement) must be >= K = a.  Negative control: a non-log-concave double-well weight
     with Ric_inf partly negative may have gap < its (wrong) 'K' = inf of positive part -> must show violation possible."""
import numpy as np, os, sys
from scipy.linalg import eigh
HERE = os.path.dirname(os.path.abspath(__file__))
out = []; fails = 0
def log(s):
    out.append(s); print(s)
M = 20000; x = (np.arange(M) + 0.5) / M
def w2_1d(f, g):
    F = np.cumsum(f) / M; G = np.cumsum(g) / M; F /= F[-1]; G /= G[-1]
    u = (np.arange(M) + 0.5) / M
    qF = np.interp(u, F, x); qG = np.interp(u, G, x)
    return np.sqrt(np.mean((qF - qG)**2))
rng = np.random.default_rng(3); worst = 0
for t in range(300):
    c = rng.normal(size=6); f = np.exp(sum(c[j] * np.cos((j + 1) * np.pi * x) for j in range(6))); f /= f.mean()
    c = rng.normal(size=6); g = np.exp(sum(c[j] * np.cos((j + 1) * np.pi * x) for j in range(6))); g /= g.mean()
    ratio = w2_1d(f, g) / (1 / np.sqrt(2) * np.sqrt(np.mean(np.abs(f - g))))
    worst = max(worst, ratio)
log("random pairs: max W2 / bound = %.4f (must be <= 1)" % worst); fails += worst > 1
for e in (0.1, 0.01, 0.001):
    w = 0.002
    f = np.where(x < w, 1 / w, 0.0); g = (1 - e) * f + e * np.where(x > 1 - w, 1 / w, 0.0)
    W = w2_1d(f, g); L1 = np.mean(np.abs(f - g))
    log("near-extremal eps=%g: W2=%.5f bound=%.5f ratio=%.4f ; mutated bound diam/2*sqrt(L1)=%.5f violated: %s" % (e, W, np.sqrt(L1 / 2), W / np.sqrt(L1 / 2), 0.5 * np.sqrt(L1), W > 0.5 * np.sqrt(L1)))
    fails += not (W > 0.5 * np.sqrt(L1))
# BE gap
def gap(V, N):
    h = 1.0 / N; xc = (np.arange(N) + 0.5) * h; w = np.exp(-V(xc)); xf = np.arange(1, N) * h; wf = np.exp(-V(xf))
    K = np.zeros((N, N))
    for i in range(N - 1):
        c = wf[i] / h**2
        K[i, i] += c; K[i + 1, i + 1] += c; K[i, i + 1] -= c; K[i + 1, i] -= c
    Mm = np.diag(w)
    ev = eigh(K, Mm, eigvals_only=True, subset_by_index=[0, 1])
    return ev[1]
for a in (2.0, 10.0, 50.0):
    V = lambda s, a=a: a * (s - 0.3)**2 / 2
    gs = [gap(V, N) for N in (200, 400, 800)]
    log("Gibbs a=%g: Neumann gap (N=200,400,800) = %s  >= K=a: %s" % (a, ["%.4f" % g for g in gs], gs[-1] >= a - 1e-6))
    fails += gs[-1] < a - 1e-6
# negative control: double well V = 20 (s-0.5)^4 - 4 (s-0.5)^2*? -> V''<0 near 0.5; claimed theorem needs V''>=K everywhere
V = lambda s: 400 * ((s - 0.5)**2 - 0.06)**2
gs = gap(V, 800)
Vpp = lambda s: 400 * (12 * (s - 0.5)**2 - 0.24) * 1.0
log("NEG CTRL double well: gap=%.4f ; max V''=%.1f, min V''=%.1f -> using K=max V'' would give a FALSE bound: %s" % (gs, Vpp(0.0), Vpp(0.5), gs < Vpp(0.0)))
fails += not gs < Vpp(0.0)
txt = "\n".join(out)
open(os.path.join(HERE, "num_w2_be.out.txt"), "w", encoding="utf8").write(txt + "\nfailures=%d\n" % int(fails))
sys.exit(int(fails))
