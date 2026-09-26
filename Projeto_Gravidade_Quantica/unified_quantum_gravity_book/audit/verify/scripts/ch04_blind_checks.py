"""Blind checks for chap04 (camada 1). m=2 (1D) unless stated."""
import mpmath as mp
import numpy as np

mp.mp.dps = 25

def C(x, y):
    return mp.gamma(x + 1) / (mp.gamma(y + 1) * mp.gamma(x - y + 1))

def make_sigma(a):
    Z = mp.quad(lambda y: C(a, y), [0, a / 2, a])
    return lambda k: mp.quad(lambda y: C(a, y) * (1 - mp.cos(k * y)), mp.linspace(0, a, 12)) / Z / a ** 2

a = 2.0
sig = make_sigma(a)

print("== symbol range, large-k limit ==")
ks = np.linspace(0.01, 40, 400)
vals = [float(sig(k)) for k in ks]
print("sup sigma on grid", max(vals), " 1/a^2", 1 / a ** 2, " 2/a^2", 2 / a ** 2, " sigma(40)", vals[-1])

print("== Modulational instability: numerical Jacobian vs formula ==")
hbar, M, kap, p, rho0 = 1.0, 1.0, 0.3, 1.5, 0.8
mu0 = -kap * rho0 ** p
def rhs(w, s):  # rotating frame, single Fourier mode cos(kx) evaluated at x=0; w = perturbation amplitude (complex)
    psi = np.sqrt(rho0) + w
    lin = -(hbar ** 2 / (2 * M)) * (-s) * w          # -hbar^2/2M * Delta acting on w cos(kx)
    nl = -kap * abs(psi) ** (2 * p) * psi + kap * rho0 ** p * np.sqrt(rho0)  # subtract background
    return (lin + nl - mu0 * w) / (1j * hbar)
for k in [0.5, 1.5, 4.0]:
    s = float(sig(k)); e = 1e-7
    J = np.zeros((2, 2))
    for col, dw in enumerate([e, 1j * e]):
        d = (rhs(dw, s) - rhs(-dw, s)) / (2 * e)
        J[0, col], J[1, col] = d.real, d.imag
    lam = np.linalg.eigvals(J)           # e^{lam t} = e^{-i Omega t} -> Omega^2 = -lam^2
    Om2_num = -(lam[0] ** 2).real
    eps = hbar ** 2 * s / (2 * M)
    Om2_th = eps * (eps - 2 * kap * p * rho0 ** p) / hbar ** 2
    Om2_mut = eps * (eps - kap * p * rho0 ** p) / hbar ** 2
    print("k", k, "Omega^2 numeric", Om2_num, "formula", Om2_th, "mutant(no 2)", Om2_mut)
print("gamma_max formula", kap * p * rho0 ** p / hbar)

print("== Energy unbounded below at fixed mass (ground-state existence) ==")
# psi = Gaussian of width w in d=1, mass N=1. Kinetic <= hbar^2/(2M) * (2/a^2) * N.
for w in [1.0, 0.1, 0.01]:
    L4 = (1 / (np.sqrt(np.pi) * w)) ** (p + 1) * np.sqrt(np.pi) * w / np.sqrt(p + 1)  # int |psi|^{2p+2}
    Ebound = hbar ** 2 / (2 * M) * 2 / a ** 2 - kap / (p + 1) * L4
    print("w", w, "E <=", Ebound)

print("== Lattice multinomial symbol vs (1/(2 m a)) k^T G k (m=3) ==")
m, al = 3, 7.0  # note: al=m+1 is a coincidence point where both forms agree
for kv in [np.array([1e-3, 2e-3]), np.array([1e-3, -1e-3])]:
    z = (1 + np.exp(1j * kv).sum()) / m
    s_lat = (1 - (z ** al).real) / al ** 2
    G = np.eye(2) + np.ones((2, 2))
    S, Q = kv.sum(), (kv ** 2).sum()
    print("k", kv, "lattice", s_lat, " (1/2ma)kGk", kv @ G @ kv / (2 * m * al),
          " S^2/2m^2+(Q-S^2/m)/(2ma)", S ** 2 / (2 * m ** 2) + (Q - S ** 2 / m) / (2 * m * al))

print("== MSD: Hessian of E_beta(-K sigma t^beta) at k=0 ==")
Kd, beta, t = 0.7, 0.6, 3.0
Z = mp.quad(lambda y: C(a, y), [0, a])
Ey2 = mp.quad(lambda y: y * y * C(a, y), [0, a]) / Z
uhat = lambda k: mp.mittag_leffler(-Kd * sig(k) * t ** beta, beta) if hasattr(mp, 'mittag_leffler') else None
def ML(z, b, N=200):
    return mp.nsum(lambda n: z ** n / mp.gamma(b * n + 1), [0, mp.inf])
h = mp.mpf("1e-3")
f = lambda k: ML(-Kd * sig(k) * t ** beta, beta)
msd_num = -(f(h) - 2 * f(0) + f(-h)) / h ** 2
msd_th = Kd / (a ** 2 * mp.gamma(beta + 1)) * Ey2 * t ** beta
msd_mut = Kd / (a ** 2 * mp.gamma(beta)) * Ey2 * t ** beta
print("numeric", mp.nstr(msd_num, 8), "theorem", mp.nstr(msd_th, 8), "mutant Gamma(beta)", mp.nstr(msd_mut, 8))
print("delta-mass remaining at t: E_beta(-K t^b/a^2) =", mp.nstr(ML(-Kd * t ** beta / a ** 2, beta), 6))
