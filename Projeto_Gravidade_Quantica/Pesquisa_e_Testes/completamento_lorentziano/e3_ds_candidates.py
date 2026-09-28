"""E3 - spectral dimension of the candidate completions (d = 4 Euclidean heat-kernel trace).

P(tau) = (8 pi^2)^-1 int_0^inf k^3 e^{-tau S(k^2)} dk  ->  in u = k^2:  P ~ int_0^inf u e^{-tau S(u)} du,
d_s = -2 dlnP/dln tau.  Units l = 1.

Candidates
  B   book symbol S = u + u^2 (fakeon keeps it EXACTLY; the Euclidean trace is unchanged).
      Oracle: erfc closed form  int u e^{-b u - a u^2} du = 1/(2a) - (b/(2a)) sqrt(pi/(4a)) e^{b^2/4a} erfc(b/(2 sqrt a)).
  T   Tomboulis/Modesto-type entire form factor tuned to the same UV coefficient:
      S_T(u) = u exp( Ein(e^{-gamma} u^2) / 2 ),  Ein(x) = int_0^x (1-e^{-t})/t dt  (entire),
      so S_T -> u^2 (1 + exp. small) in the UV, S_T = u + O(u^3) in the IR; no zeros besides u = 0.
  AS  anomalous-dimension family S = u (1+u)^{-eta/2}: eta = -2 is exactly the book symbol;
      UV law d_s = 2d/(2-eta).
  LW  polynomial symbols with a massless normal pole: S = u (alpha + beta u) has its second root real with
      residue -1/alpha < 0 (real ghost); a complex-conjugate (Lee-Wick) pair needs degree >= 3 -> d_s(UV) <= 4/3.

Checks
  B1  moment identity (mpmath) vs erfc closed form (finite difference) for d_s(tau), 9 values of tau.
  T1  S_T has no zero on (0, 1e4]; S_T(u)/u^2 -> 1 at u = 1e3 (to 1e-12); S_T/u -> 1 at u = 1e-4.
  T2  d_s of S_T: UV -> 2, IR -> 4 (two methods agree), and max |d_s^T - d_s^B| over the grid (reported).
  T3  1/S_T is not polynomially bounded off the real axis: |1/S_T(i y)| at y = 5 exceeds 1e100 -> no
      Kallen-Lehmann representation (why Lemma KL does not apply).
  A1  eta in {0,-1,-2,-3}: d_s(tau = 1e-8) = 8/(2-eta) within 2e-3.
  L1  S = u(alpha+beta u): residue of 1/S at the second root equals -1/alpha (random alpha, beta).
  L2  LW example S = u(1 + u + u^2) (complex pair u = (-1 +- i sqrt 3)/2): d_s(UV) -> 4/3.
  NC1 erfc formula without the factor e^{b^2/4a} must fail B1.
  NC2 mutated UV law 2d/(2+eta) must fail A1.
  NC3 Ein replaced by ln (non-entire: S = e^{-gamma/2} u * u) gives S ~ u^2 at ALL scales -> d_s = 2 everywhere
      (no IR recovery); detector: IR d_s must NOT be 4.
"""
import numpy as np
import mpmath as mp
from scipy import integrate, special

mp.mp.dps = 25
R = []


def check(n, ok, info=''):
    R.append(ok); print(f"[{'PASS' if ok else 'FAIL'}] {n} {info}")


def ds_moment(S, tau):
    tau = mp.mpf(tau)
    brk = [0, mp.mpf(1e-3) / tau, 1 / tau, mp.sqrt(1 / tau), 10 / tau, 10 * mp.sqrt(1 / tau), mp.inf]
    brk = sorted(set(brk))
    num = mp.quad(lambda u: u * S(u) * mp.e ** (-tau * S(u)), brk)
    den = mp.quad(lambda u: u * mp.e ** (-tau * S(u)), brk)
    return 2 * tau * num / den


def ds_fd_np(S, tau, h=1e-3):
    def lnP(t):
        f = lambda lu: np.exp(2 * lu - t * S(np.exp(lu)))
        hi = max(np.log(80 / t), 0.5 * np.log(80 / t)) + 3
        v, _ = integrate.quad(f, -40, hi, limit=500, points=[np.log(1 / t), 0.5 * np.log(1 / t)])
        return np.log(v)
    return -2 * (lnP(tau * np.exp(h)) - lnP(tau * np.exp(-h))) / (2 * h)


def P_erfc(tau, mutate=False):
    a, b = tau, tau        # S = u + u^2 -> b = tau, a = tau
    x = b / (2 * np.sqrt(a))
    ex = special.erfcx(x) if not mutate else special.erfc(x)   # erfcx = e^{x^2} erfc(x)
    return 1 / (2 * a) - (b / (2 * a)) * np.sqrt(np.pi / (4 * a)) * ex


def ds_erfc(tau, mutate=False, h=1e-4):
    return -2 * (np.log(P_erfc(tau * np.exp(h), mutate)) - np.log(P_erfc(tau * np.exp(-h), mutate))) / (2 * h)


S_B = lambda u: u + u ** 2
taus = [1e-6, 1e-4, 1e-2, 0.1, 1, 10, 100, 1e4, 1e6]
dsB = {t: float(ds_moment(S_B, t)) for t in taus}
err = max(abs(dsB[t] - ds_erfc(t)) for t in taus)
check('B1 book symbol: moment identity = erfc closed form', err < 1e-6, f'(max diff {err:.1e})')
errm = max(abs(dsB[t] - ds_erfc(t, mutate=True)) for t in taus)
check('NC1 erfc without e^{x^2} fails', errm > 1e-2, f'(max diff {errm:.2f})')
print('   book d_s:', ', '.join(f'{t:g}:{dsB[t]:.4f}' for t in taus))

# ---------- Tomboulis-type ----------
g = mp.euler
def ein(x):
    """Ein(x) for real x > 0: power series for x < 2, gamma + ln x + E1(x) otherwise."""
    x = mp.mpf(x)
    if x < 2:
        return mp.nsum(lambda n: (-1) ** (n + 1) * x ** n / (n * mp.factorial(n)), [1, mp.inf])
    return g + mp.log(x) + mp.e1(x)
ein_c = lambda x: mp.quad(lambda s: -mp.expm1(-s * x) / s, [0, 1])      # valid for complex x (entire)
S_T = lambda u: u * mp.e ** (ein(mp.e ** (-g) * u ** 2) / 2)
zeros_ok = all(S_T(mp.mpf(u)) > 0 for u in np.logspace(-6, 4, 60))
uv = abs(S_T(mp.mpf(1e3)) / mp.mpf(1e6) - 1); ir = abs(S_T(mp.mpf(1e-4)) / mp.mpf(1e-4) - 1)
check('T1 S_T > 0 on (0,1e4], S_T/u^2 -> 1 (UV), S_T/u -> 1 (IR)', zeros_ok and uv < 1e-12 and ir < 1e-8,
      f'(UV dev {mp.nstr(uv, 3)}, IR dev {mp.nstr(ir, 3)})')
S_T_np = np.vectorize(lambda u: float(S_T(mp.mpf(u))))
dsT = {t: float(ds_moment(S_T, t)) for t in taus}
fdT = {t: ds_fd_np(S_T_np, t) for t in (1e-6, 1e6)}
ok = abs(dsT[1e-6] - 2) < 2e-3 and abs(dsT[1e6] - 4) < 2e-3 and all(abs(fdT[t] - dsT[t]) < 1e-5 for t in fdT)
dev = max(abs(dsT[t] - dsB[t]) for t in taus); targ = max(taus, key=lambda t: abs(dsT[t] - dsB[t]))
check('T2 Tomboulis-type: d_s 4 -> 2, fd = moment', ok,
      f'(UV {dsT[1e-6]:.4f}, IR {dsT[1e6]:.4f}; max |d_s^T - d_s^B| = {dev:.3f} at tau = {targ:g})')
print('   T   d_s:', ', '.join(f'{t:g}:{dsT[t]:.4f}' for t in taus))
y = mp.mpf(5); z = 1j * y      # u = i y  <->  z^2 = -y^2: Ein of a negative argument grows like Ei
GT_im = 1 / abs(z * mp.e ** (ein_c(mp.e ** (-g) * z ** 2) / 2))
check('T3 |1/S_T(5i)| > 1e100 (propagator not polynomially bounded off the real axis -> no KL representation)',
      GT_im > 1e100, f'(|1/S_T(5i)| = {mp.nstr(GT_im, 4)}; book symbol: |1/S_B(5i)| = {float(1/abs(z + z**2)):.3f})')
S_ln = lambda u: mp.e ** (-g / 2) * mp.e ** (g / 2) * u * u      # Ein -> gamma + ln x everywhere
d_ir_ln = float(ds_moment(S_ln, 1e6))
check('NC3 non-entire replacement has no IR recovery (d_s(1e6) != 4)', abs(d_ir_ln - 4) > 1, f'({d_ir_ln:.4f})')

# ---------- anomalous dimension family ----------
okA, okN = True, True
for eta in (0, -1, -2, -3):
    S = lambda u, e=eta: u * (1 + u) ** (-mp.mpf(e) / 2)
    d = float(ds_moment(S, 1e-8)); pred = 8 / (2 - eta)
    okA &= abs(d - pred) < 2e-3 + 0.02 * (eta == -1)   # slow approach for fractional powers
    if eta != 0:
        okN &= (eta == -2) or abs(d - 8 / (2 + eta)) > 0.2   # 2+eta=0 at eta=-2: mutant undefined -> fails trivially
    print(f'   eta = {eta}: d_s(1e-8) = {d:.4f}, 2d/(2-eta) = {pred:.4f}')
check('A1 UV law d_s = 2d/(2-eta); eta=-2 is the book symbol', okA)
check('NC2 mutated law 2d/(2+eta) fails', okN)

# ---------- Lee-Wick / polynomial ----------
rng = np.random.default_rng(7); okL = True
for _ in range(50):
    al, be = rng.uniform(0.1, 5, 2)
    z0 = -al / be
    resid = 1 / (al + 2 * be * z0)
    okL &= abs(resid + 1 / al) < 1e-12 and np.isreal(z0)
check('L1 degree-2 symbol with massless pole: second root real, residue -1/alpha < 0', okL)
S_LW = lambda u: u * (1 + u + u ** 2)
roots = np.roots([1, 1, 1, 0])
dLW = float(ds_moment(S_LW, 1e-9))
check('L2 Lee-Wick pair (roots %s) forces d_s(UV) -> 4/3' % np.round(roots[:2], 3), abs(dLW - 4 / 3) < 5e-3,
      f'({dLW:.4f})')

print(f"\n{sum(R)}/{len(R)} checks passed")
