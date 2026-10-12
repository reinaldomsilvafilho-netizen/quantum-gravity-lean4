"""L2b check of chap05 Proposition [Inversion] and Remark [Zeros of K^_alpha] (l. 231-252).

Numbers in the remark:
 (a) m = 1, alpha = 1, kappa(y) ~ 1/(Gamma(y+1) Gamma(2-y)) on [0,1]: e^{ik/2} K^(k) is real and
     changes sign at k ~ 6.6036;
 (b) m = 2, line k = t(1,-1): K^ real (up to a phase), no sign change for 0 < t <= 60,
     alpha in {0.5, 1, 2};
 (c) m = 2, alpha = 1: no zero of K^ in [-30,30]^2 (here: grid scan + local minimisation of |K^|^2,
     a different method from the text's winding-number scan).
Oracles: (a) mpmath adaptive quadrature at 30 digits + findroot (independent of the scipy route);
(b),(c) Duffy-mapped Gauss-Legendre tensor rule on the triangle, cross-checked against mpmath
2-D quadrature at sample points.
Negative controls: (n1) uniform density on the same triangle has a true zero on the line
(detector must see it); (n2) mutated root 6.6136 must not be a sign-change point;
(n3) for (a), the uniform density on [0,1] has its zero at 2 pi, not at 6.6036.
"""
import sys
import time
import numpy as np
import mpmath as mp
from scipy.special import gammaln
from scipy.optimize import minimize

fails = 0
t0 = time.time()
mp.mp.dps = 30

# ---------- (a) m = 1 ----------
kap1 = lambda y: mp.rgamma(y + 1) * mp.rgamma(2 - y)
Z1 = mp.quad(kap1, [0, 1])


def F1(k):  # e^{ik/2} K^(k), K^(k) = int K(y) e^{-iky} dy
    re = mp.quad(lambda y: kap1(y) * mp.cos(k * (y - mp.mpf(1) / 2)), [0, mp.mpf(1) / 2, 1]) / Z1
    im = mp.quad(lambda y: kap1(y) * mp.sin(k * (y - mp.mpf(1) / 2)), [0, mp.mpf(1) / 2, 1]) / Z1
    return re, im


ra, ia = F1(6.5)
rb, ib = F1(6.7)
root = mp.findroot(lambda k: F1(k)[0], 6.6)
ok = ra * rb < 0 and abs(ia) < 1e-25 and abs(ib) < 1e-25 and abs(root - mp.mpf('6.6036')) < 5e-5
print(f"{'PASS' if ok else 'FAIL'} (a) sign change: F(6.5)={mp.nstr(ra,6)}, F(6.7)={mp.nstr(rb,6)}, "
      f"Im ~ {mp.nstr(max(abs(ia),abs(ib)),3)}, root = {mp.nstr(root,10)} (text 6.6036)")
fails += not ok
r1, _ = F1(mp.mpf('6.6136') - mp.mpf('0.001'))
r2, _ = F1(mp.mpf('6.6136') + mp.mpf('0.001'))
okn2 = r1 * r2 > 0
print(f"{'PASS (control fails)' if okn2 else 'FAIL (control passed)'} (n2) no sign change at mutated 6.6136")
fails += not okn2
u1 = mp.quad(lambda y: mp.cos(2 * mp.pi * (y - 0.5)), [0, 1])
okn3 = abs(u1) < 1e-25 and abs(root - 2 * mp.pi) > 0.3
print(f"{'PASS (control fails)' if okn3 else 'FAIL'} (n3) uniform zero at 2pi = {mp.nstr(2*mp.pi,8)}, Beta-kernel root differs")
fails += not okn3

# ---------- (b) m = 2 ----------
def rule(alpha, N):
    x, w = np.polynomial.legendre.leggauss(N)
    x = (x + 1) / 2; w = w / 2
    U, Vv = np.meshgrid(x, x, indexing='ij')
    WU, WV = np.meshgrid(w, w, indexing='ij')
    y1 = alpha * U
    y2 = alpha * (1 - U) * Vv
    jac = alpha ** 2 * (1 - U)
    return y1.ravel(), y2.ravel(), (WU * WV * jac).ravel()


def kernel2(alpha, y1, y2, uniform=False):
    if uniform:
        return np.ones_like(y1)
    y3 = alpha - y1 - y2
    return np.exp(-(gammaln(y1 + 1) + gammaln(y2 + 1) + gammaln(y3 + 1)))


def Khat2(alpha, K1, K2, N=160, uniform=False):
    y1, y2, w = rule(alpha, N)
    dens = kernel2(alpha, y1, y2, uniform) * w
    dens = dens / dens.sum()
    out = np.empty(len(K1), complex)
    for s in range(0, len(K1), 400):
        ph = np.outer(K1[s:s+400], y1) + np.outer(K2[s:s+400], y2)
        out[s:s+400] = np.exp(-1j * ph) @ dens
    return out


# cross-check of the quadrature against mpmath 2-D quad at one point
alpha = 1.0
kp = (7.3, -2.1)
f = lambda a, b: mp.rgamma(a + 1) * mp.rgamma(b + 1) * mp.rgamma(alpha - a - b + 1)
mp.mp.dps = 15
Zm = mp.quad(lambda a: mp.quad(lambda b: f(a, b), [0, alpha - a]), [0, alpha])
re = mp.quad(lambda a: mp.quad(lambda b: f(a, b) * mp.cos(kp[0]*a + kp[1]*b), [0, alpha - a]), [0, alpha]) / Zm
im = -mp.quad(lambda a: mp.quad(lambda b: f(a, b) * mp.sin(kp[0]*a + kp[1]*b), [0, alpha - a]), [0, alpha]) / Zm
q = Khat2(alpha, np.array([kp[0]]), np.array([kp[1]]))[0]
e_cross = abs(q - complex(re, im))
ok = e_cross < 1e-9
print(f"{'PASS' if ok else 'FAIL'} quadrature vs mpmath 2-D at k={kp}: {e_cross:.1e}")
fails += not ok

for alpha in (0.5, 1.0, 2.0):
    t = np.linspace(1e-3, 60, 24001)
    N = 160 if alpha < 2 else 240
    R = Khat2(alpha, t, -t, N)
    imax = np.abs(R.imag).max()
    nsign = int(np.sum(np.sign(R.real[1:]) != np.sign(R.real[:-1])))
    # local minima of R
    i = np.where((R.real[1:-1] < R.real[:-2]) & (R.real[1:-1] < R.real[2:]))[0] + 1
    mins = [(round(t[j], 2), R.real[j]) for j in i[:3]]
    ok = nsign == 0 and imax < 1e-12 and R.real.min() > 0
    print(f"{'PASS' if ok else 'FAIL'} (b) alpha={alpha}: sign changes={nsign}, min R={R.real.min():.3e}, "
          f"|Im|max={imax:.1e}, first minima {[(a, f'{b:.2e}') for a, b in mins]}")
    fails += not ok

# n1: uniform triangle density, alpha = 1, has exact zero on the line (detector power)
t = np.linspace(1e-3, 60, 24001)
Ru = Khat2(1.0, t, -t, 160, uniform=True)
okn1 = Ru.real.min() < 1e-8 * 1 or np.any(np.sign(Ru.real[1:]) != np.sign(Ru.real[:-1]))
print(f"{'PASS (control: zero detected)' if okn1 else 'FAIL (detector has no power)'} (n1) uniform: min R = {Ru.real.min():.2e}")
fails += not okn1

# ---------- (c) 2-D scan, alpha = 1, half plane k2 >= 0 (K^(-k) = conj K^(k)) ----------
alpha = 1.0
g = np.arange(-30, 30.0001, 0.25)
g2 = np.arange(0, 30.0001, 0.25)
K1, K2 = np.meshgrid(g, g2, indexing='ij')
A = np.abs(Khat2(alpha, K1.ravel(), K2.ravel(), 120)).reshape(K1.shape)
cand = []
for a in range(1, A.shape[0] - 1):
    for b in range(1, A.shape[1] - 1):
        blk = A[a-1:a+2, b-1:b+2]
        if A[a, b] <= blk.min():
            cand.append((A[a, b], g[a], g2[b]))
cand.sort()
best = []
for val, x0, y0 in cand[:60]:
    fun = lambda z: float(np.abs(Khat2(alpha, np.array([z[0]]), np.array([z[1]]), 120)[0]) ** 2)
    res = minimize(fun, [x0, y0], method='Nelder-Mead', options={'xatol': 1e-6, 'fatol': 1e-16, 'maxiter': 400})
    best.append((np.sqrt(res.fun), res.x))
best.sort(key=lambda z: z[0])
mn = best[0][0]
ok = mn > 1e-6
print(f"{'PASS' if ok else 'FAIL'} (c) {len(cand)} grid minima, 60 smallest refined: min |K^| = {mn:.3e} at "
      f"{np.round(best[0][1], 3)}; next {best[1][0]:.3e}")
fails += not ok
print(f"elapsed {time.time()-t0:.0f}s")
sys.exit(1 if fails else 0)
