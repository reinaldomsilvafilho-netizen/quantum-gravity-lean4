"""L2 re-check of ch12 sec:lorentzian_completion numbers (independent of e1-e3, v1-v3).

Oracles: direct quadrature of heat-kernel traces; numerical slow-roll of the exact
Starobinsky potential (not the closed form) for m_phi; CODATA 2018 constants.
Each block has a negative control (mutated formula) that must FAIL.
"""
import numpy as np
from scipy import integrate, optimize

PASS = []


def check(name, cond, info=""):
    PASS.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + "  " + info)


# ---------- heat kernel d_s for a symbol S(z), z=k^2, 4D: P ~ int z e^{-tau S} dz
def ds(S, tau):
    # work in x = ln z for accuracy over many decades
    f = lambda x, t: np.exp(2 * x) * np.exp(-t * S(np.exp(x)))
    g = lambda x, t: np.exp(2 * x) * S(np.exp(x)) * np.exp(-t * S(np.exp(x)))
    lo, hi = -60.0, 60.0
    P = integrate.quad(f, lo, hi, args=(tau,), limit=800, points=[-np.log(tau)])[0]
    Q = integrate.quad(g, lo, hi, args=(tau,), limit=800, points=[-np.log(tau)])[0]
    return 2 * tau * Q / P  # d_s = -2 dlnP/dln tau


taus = np.logspace(-6, 6, 25)

# 1. Kallen-Lehmann: random positive spectral measures -> d_s >= 4 pointwise
# (mpmath quadrature in z with breakpoints at the masses; weight shifted by S(0)
#  so gapped cases do not underflow; <S> is shift-invariant)
import mpmath as mp
mp.mp.dps = 30
rng = np.random.default_rng(7)
worst = 10.0
for trial in range(12):
    w0 = rng.uniform(0, 1) if trial % 3 else 0.0
    mus = 10 ** rng.uniform(-3, 3, size=4)
    ws = rng.uniform(0.1, 1, size=4)
    S = lambda z, w0=w0, mus=mus, ws=ws: 1 / (w0 / z + mp.fsum(mp.mpf(w) / (z + mp.mpf(u)) for w, u in zip(ws, mus))) if z > 0 else (0 if w0 > 0 else 1 / mp.fsum(mp.mpf(w) / mp.mpf(u) for w, u in zip(ws, mus)))
    S0 = S(mp.mpf(0))
    brk = sorted(set([mp.mpf(0)] + [mp.mpf(u) for u in mus] + [mp.mpf(10) ** k for k in range(-9, 10)])) + [mp.inf]
    for t in np.logspace(-4, 4, 9):
        t = mp.mpf(t)
        P = mp.quad(lambda z: z * mp.e ** (-t * (S(z) - S0)), brk)
        Q = mp.quad(lambda z: z * S(z) * mp.e ** (-t * (S(z) - S0)), brk)
        worst = min(worst, float(2 * t * Q / P))
check("KL positive rho: min d_s over tau >= 4", worst >= 4 - 1e-6, f"min={worst:.6f}")
# negative control: the book symbol (rho has a -1 weight) must go below 4
book = lambda z: z * (1 + z)
m = min(ds(book, t) for t in taus)
check("NC book symbol k^2+k^4 violates the bound", m < 3.9, f"min d_s={m:.4f}")

# 2. degree-2 polynomial WITHOUT massless pole, complex roots: d_s(UV) = 2 (not <= 4/3)
cp = lambda z: z * z + z + 1.0
v = ds(cp, 1e-8)
check("z^2+z+1 (complex pair, n=2, no massless pole) has d_s(UV)=2", abs(v - 2) < 0.01, f"{v:.4f}")
cpm = lambda z: z * (z * z + z + 1.0)
v2 = ds(cpm, 1e-10)
check("z(z^2+z+1) (with massless pole) has d_s(UV)=4/3", abs(v2 - 4 / 3) < 0.01, f"{v2:.4f}")

# 3. ABP 2020 eq 7.3 window
N = 60
Nr = lambda x: 24 * x**2 / (1 + 2 * x**2)  # x = m_chi/m_phi
lo, hi, one = Nr(0.25) / N**2, 12 / N**2, Nr(1.0) / N**2
check("window lower 3.7e-4", abs(lo - 3.7e-4) < 0.05e-4, f"{lo:.4e}")
check("window upper 3.3e-3", abs(hi - 3.33e-3) < 0.05e-3, f"{hi:.4e}")
check("one-scale r=8/N^2=2.2e-3", abs(one - 2.22e-3) < 0.01e-3, f"{one:.4e}")
check("2.2 sigma at dr=1e-3", abs(one / 1e-3 - 2.2) < 0.05, f"{one/1e-3:.3f}")
check("1.1 sigma from 12/N^2", abs((hi - one) / 1e-3 - 1.1) < 0.05, f"{(hi-one)/1e-3:.3f}")
# NC: swapped masses in denominator must not give 4/3 at the bound
Nr_bad = lambda x: 24 * x**2 / (2 + x**2)
check("NC swapped-mass formula fails the 4/3 edge", abs(Nr_bad(0.25) - 4 / 3) > 0.1, f"{Nr_bad(0.25):.3f}")

# 4. m_phi by numerical slow roll of V = 3/4 m^2 M^2 (1-e^{-sqrt(2/3)phi/M})^2, M = reduced Planck
hbar_c = 1.973269804e-16          # GeV m (CODATA 2018)
G_N = 6.67430e-11; hbar = 1.054571817e-34; c = 299792458.0
lP = np.sqrt(hbar * G_N / c**3)    # 1.616255e-35 m
MPl = np.sqrt(hbar * c / G_N) * c**2 / 1.602176634e-10   # GeV, non-reduced
Mred = MPl / np.sqrt(8 * np.pi)
As = np.exp(3.044) * 1e-10         # Planck 2018


def m_phi(N):
    a = np.sqrt(2 / 3)
    eps = lambda p: 0.5 * (a * 2 * np.exp(-a * p) / (1 - np.exp(-a * p)))**2  # M=1
    pend = optimize.brentq(lambda p: eps(p) - 1, 0.1, 5)
    Vp_over_V = lambda p: 2 * a * np.exp(-a * p) / (1 - np.exp(-a * p))
    Nf = lambda p: integrate.quad(lambda q: 1 / Vp_over_V(q), pend, p)[0]
    pst = optimize.brentq(lambda p: Nf(p) - N, pend + 0.01, 20)
    Vhat = 0.75 * (1 - np.exp(-a * pst))**2   # V/(m^2 M^2)
    # A_s = V/(24 pi^2 eps M^4) = m^2 Vhat /(24 pi^2 eps M^2)
    return Mred * np.sqrt(As * 24 * np.pi**2 * eps(pst) / Vhat)


mphi = m_phi(60)
ell = hbar_c / mphi
check("m_phi(N=60) ~ 2.7-2.9e13 GeV", 2.6e13 < mphi < 3.0e13, f"{mphi:.3e} GeV")
check("ell ~ 7e-30 m", 6.5e-30 < ell < 7.5e-30, f"{ell:.3e} m")
check("ell/l_P ~ 4.4e5 (4.2-4.6)", 4.2e5 < ell / lP < 4.6e5, f"{ell/lP:.3e}")
check("4 ell < 2.9e-29 m (rounding)", 4 * ell < 2.95e-29, f"{4*ell:.3e} m")
# order-of-magnitude: m_phi/M_Pl ~ 1e-6..1e-5
check("OoM m_phi/MPl in 1e-6..1e-5", 1e-6 < mphi / MPl < 1e-5, f"{mphi/MPl:.2e}")
# NC: using non-reduced M_Pl in the A_s formula must be off by sqrt(8 pi)
bad = mphi * np.sqrt(8 * np.pi)
check("NC non-reduced Planck mass gives ell outside 6.5-7.5e-30", not (6.5e-30 < hbar_c / bad < 7.5e-30), f"{hbar_c/bad:.3e}")

# 5. Consistency: if ell_P = 1/m_2 literally (conjecture), m_chi = M_Pl, x = MPl/mphi
x = MPl / mphi
dev = 1 - Nr(x) / 12
check("literal ell_P=1/m_2 => r = Starobinsky to ~2.5e-12", 1e-12 < dev < 5e-12, f"x={x:.3e}, 1-N^2r/12={dev:.2e}")
check("... so the one-scale 8/N^2 case is excluded under the conjecture", abs(Nr(x) - 8) > 3.9, f"N^2r={Nr(x):.6f}")

print(f"\n{sum(PASS)}/{len(PASS)} checks passed")
