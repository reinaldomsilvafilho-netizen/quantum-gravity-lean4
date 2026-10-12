"""L2 checks of A5 (chap03 Digamma PDE system, l. 105-120) and of the ch. 4 MI fix (l. 216-231).

A5 claims: on the open set, d_x C = C[psi(x+1)-psi(x-y+1)], d_y C = C[psi(x-y+1)-psi(y+1)];
extended products hold for all x not in Z_<0, y in C; at y = -1, d_y C = 1/(x+1);
transport literal on x-y in Z_<0 when y+1 not in Z_<=0.
Oracle: mpmath numerical differentiation of Gamma(x+1) rgamma(y+1) rgamma(x-y+1) (entire in y).
Controls: (m1) psi(x) instead of psi(x+1) must fail; (m2) value 1/(x+2) at y=-1 must fail.

ch.4 claims: hbar^2 Omega^2 = eps(eps - 2 kappa p rho^p), eps = hbar^2 sigma/(2M); Omega^2 < 0 iff
0 < sigma < 4 M kappa p rho^p / hbar^2; Omega = 0 where sigma = 0; gamma_max = kappa p rho^p/hbar
at sigma = 2 M kappa p rho^p/hbar^2; sigma(k) > 0 for k != 0 (needed for "every k != 0 unstable").
Oracle: sympy linearisation of the NLSE i hbar psi_t = (hbar^2/2M) sigma psi - kappa |psi|^{2p} psi
around the plane wave (independent derivation), eigenvalues of the 2x2 system.
Control: old criterion "sigma < 4M kappa p rho^p/hbar^2" (no lower bound) must fail at sigma = 0.
"""
import sys
import mpmath as mp
import sympy as sp
import numpy as np

fails = 0
mp.mp.dps = 30
C = lambda x, y: mp.gamma(x + 1) * mp.rgamma(y + 1) * mp.rgamma(x - y + 1)
pts = [(mp.mpf('0.7'), mp.mpf('-0.4')), (mp.mpc('1.3', '0.4'), mp.mpc('-2.6', '0.2')), (mp.mpf('2.5'), mp.mpf('1.1'))]
worst = 0; worst_mut = 1e9
for x, y in pts:
    dx = mp.diff(lambda s: C(s, y), x)
    dy = mp.diff(lambda s: C(x, s), y)
    rx = C(x, y) * (mp.digamma(x + 1) - mp.digamma(x - y + 1))
    ry = C(x, y) * (mp.digamma(x - y + 1) - mp.digamma(y + 1))
    worst = max(worst, abs(dx - rx), abs(dy - ry))
    worst_mut = min(worst_mut, abs(dx - C(x, y) * (mp.digamma(x) - mp.digamma(x - y + 1))))
ok = worst < 1e-20
print(f"{'PASS' if ok else 'FAIL'} A5 PDEs at generic points: {mp.nstr(worst,3)}")
fails += not ok
okm1 = worst_mut > 1e-3
print(f"{'PASS (control fails)' if okm1 else 'FAIL'} m1 psi(x) mutant: min error {mp.nstr(worst_mut,3)}")
fails += not okm1

# extension at y = -1 and on x - y = -2
for x in (mp.mpf('0.7'), mp.mpc('-0.5', '1.2')):
    dy = mp.diff(lambda s: C(x, s), -1)
    ext = -mp.gamma(x + 1) * mp.rgamma(x - (-1) + 1) * mp.diff(mp.rgamma, 0) + 0  # -C psi(y+1) extended; C psi(x-y+1) = 0
    e1 = abs(dy - 1 / (x + 1)); e2 = abs(dy + ext * 0 - (-(-mp.gamma(x + 1) * mp.rgamma(x + 2) * mp.diff(mp.rgamma, 0))))
    ok = e1 < 1e-20 and e2 < 1e-20
    print(f"{'PASS' if ok else 'FAIL'} A5 d_y C at (x={mp.nstr(x,4)}, y=-1) = {mp.nstr(dy,12)} vs 1/(x+1): {mp.nstr(e1,3)}")
    fails += not ok
    okm2 = abs(dy - 1 / (x + 2)) > 1e-3
    print(f"{'PASS (control fails)' if okm2 else 'FAIL'} m2 1/(x+2) mutant")
    fails += not okm2
x = mp.mpf('0.3'); y = x + 2  # x - y = -2, y + 1 = 3.3
lhs = mp.diff(lambda s: C(x + s, y + s), 0)
rhs = C(x, y) * (mp.digamma(x + 1) - mp.digamma(y + 1))
ok = abs(lhs) < 1e-20 and abs(rhs) < 1e-20
print(f"{'PASS' if ok else 'FAIL'} A5 transport literal on x-y=-2: lhs={mp.nstr(lhs,3)}, rhs={mp.nstr(rhs,3)}")
fails += not ok

# ---------- ch. 4 ----------
hb, M, kap, p, rho, s, Om = sp.symbols('hbar M kappa p rho0 sigma Omega', positive=True)
du, dv = sp.symbols('du dv')
# psi = (sqrt(rho)+du+i dv) e^{-i mu t/hbar}, mu = -kappa rho^p; linear terms of
# i hbar psi_t = (hbar^2/2M) sigma psi - kappa |psi|^{2p} psi  (Fourier mode, V = 0)
mu = -kap * rho ** p
a = sp.sqrt(rho)
eps = hb ** 2 * s / (2 * M)
# |psi|^2 = rho + 2 a du + O(2);  |psi|^{2p} = rho^p (1 + 2 p du / a)
# real part: hbar dv_t = -(eps) du ... derive: i hbar (du_t + i dv_t) + mu (a+du+i dv) = eps (du + i dv) - kap rho^p (a+du+i dv) - kap rho^p 2p du/a * a
# collect: real: -hbar dv_t + mu du = eps du - kap rho^p du - 2 p kap rho^p du ; imag: hbar du_t + mu dv = eps dv - kap rho^p dv
dut = sp.symbols('dut'); dvt = sp.symbols('dvt')
eq_re = sp.Eq(-hb * dvt + mu * du, eps * du - kap * rho ** p * du - 2 * p * kap * rho ** p * du)
eq_im = sp.Eq(hb * dut + mu * dv, eps * dv - kap * rho ** p * dv)
sol = sp.solve([eq_re, eq_im], [dut, dvt])
Mlin = sp.Matrix([[sp.diff(sol[dut], du), sp.diff(sol[dut], dv)], [sp.diff(sol[dvt], du), sp.diff(sol[dvt], dv)]])
# modes e^{-i Omega t}: -i Omega is an eigenvalue => Omega^2 = -lambda^2
lam2 = sp.simplify((Mlin.eigenvals().popitem()[0]) ** 2)
Om2_oracle = sp.simplify(-lam2)
Om2_text = eps * (eps - 2 * kap * p * rho ** p) / hb ** 2
ok = sp.simplify(Om2_oracle - Om2_text) == 0
print(f"{'PASS' if ok else 'FAIL'} ch4 dispersion relation (sympy linearisation)")
fails += not ok
f = sp.lambdify((s,), Om2_text.subs({hb: 1, M: 1, kap: 0.8, p: 1.5, rho: 0.9}))
thr = 4 * 1 * 0.8 * 1.5 * 0.9 ** 1.5
grid = np.linspace(0, 1.5 * thr, 3001)
vals = np.array([f(g) for g in grid])
crit_new = (grid > 0) & (grid < thr)
crit_old = grid < thr
ok = bool(np.all((vals < 0) == crit_new)) and abs(f(0.0)) < 1e-15
print(f"{'PASS' if ok else 'FAIL'} ch4 new criterion 0<sigma<4M kappa p rho^p/hbar^2 matches sign(Omega^2) on grid; Omega(0)=0")
fails += not ok
okc = not bool(np.all((vals < 0) == crit_old))
print(f"{'PASS (control fails)' if okc else 'FAIL (control passed)'} old criterion without lower bound")
fails += not okc
gmax = np.sqrt(-vals.min())
ok = abs(gmax - 0.8 * 1.5 * 0.9 ** 1.5) < 1e-6 and abs(grid[vals.argmin()] - thr / 2) < 2 * (grid[1] - grid[0])
print(f"{'PASS' if ok else 'FAIL'} ch4 gamma_max = kappa p rho^p/hbar = {gmax:.6f}, at sigma = thr/2")
fails += not ok
# sigma(k) > 0 for k != 0 (m = 3: Delta_2(alpha) in R^2), alpha = 1, small and large k
xg, wg = np.polynomial.legendre.leggauss(80); xg = (xg + 1) / 2; wg = wg / 2
U, V = np.meshgrid(xg, xg, indexing='ij'); WU, WV = np.meshgrid(wg, wg, indexing='ij')
y1 = U.ravel(); y2 = ((1 - U) * V).ravel(); w = (WU * WV * (1 - U)).ravel()
from scipy.special import gammaln
dens = np.exp(-(gammaln(y1 + 1) + gammaln(y2 + 1) + gammaln(1 - y1 - y2 + 1))) * w
rng = np.random.default_rng(1)
ks = np.vstack([rng.normal(size=(2000, 2)) * sc for sc in (1e-2, 1, 10, 40)])
sig = (dens * (1 - np.cos(ks[:, :1] * y1 + ks[:, 1:] * y2))).sum(1) / dens.sum()
ok = sig.min() > 0
print(f"{'PASS' if ok else 'FAIL'} ch4 sigma(k) > 0 on {len(ks)} random k != 0 (m=3, alpha=1): min {sig.min():.2e}")
fails += not ok
sys.exit(1 if fails else 0)
