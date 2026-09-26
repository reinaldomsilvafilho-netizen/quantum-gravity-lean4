"""Independent checks for the 2026-09-25 correction pass of the SQG manuscript.

Each block compares a manuscript statement with an independent oracle and includes a
negative control (a mutated formula must fail).
Usage: python check_sqg_formulas.py   (exit code 0 iff all checks behave as expected)
"""
import math
import sys

import numpy as np
from scipy import integrate, special
from scipy.constants import G, c, hbar

fail = []


def check(name, cond):
    print(('ok   ' if cond else 'FAIL ') + name)
    if not cond:
        fail.append(name)


# 1. Spectral dimension of the two-scale symbol k^2 + l^2 k^4 in 4D (l = 1).
def P_quad(t):
    # oracle: radial quadrature, P = (1/16 pi^2) int_0^inf u exp(-t u - t u^2) du
    return integrate.quad(lambda u: u * np.exp(-t * u - t * u * u), 0, np.inf, limit=200)[0] / (16 * np.pi ** 2)


def P_book(t):
    z = np.sqrt(t) / 2
    return (1 - np.sqrt(np.pi) * z * special.erfcx(z)) / (32 * np.pi ** 2 * t)


def P_old(t):  # formula printed in the manuscript before this pass
    z = np.sqrt(t) / 2
    return special.erfcx(z) / (16 * np.pi ** 2 * t ** 2)


def ds_num(P, t, h=1e-5):
    return -2 * (np.log(P(t * np.exp(h))) - np.log(P(t * np.exp(-h)))) / (2 * h)


def ds_book(t):
    z = np.sqrt(t) / 2
    return 1 - t / 2 + 1 / (1 - np.sqrt(np.pi * t) / 2 * special.erfcx(z))


def ds_old(t):
    z = np.sqrt(t) / 2
    return 4 - np.sqrt(t / np.pi) / special.erfcx(z) + t / 2


ts = [1e-3, 1e-2, 0.1, 1, 10, 100]
check('closed-form P matches quadrature', all(abs(P_book(t) / P_quad(t) - 1) < 1e-6 for t in ts))
check('closed-form d_s matches numerical log-derivative of quadrature',
      all(abs(ds_book(t) - ds_num(P_quad, t)) < 1e-4 for t in ts))
check('d_s(1e-6) ~ 2 and d_s(1e4) ~ 4', abs(ds_book(1e-6) - 2) < 1e-2 and abs(ds_book(1e4) - 4) < 1e-2)
check('IR tail d_s = 4 - 12/tau', abs((4 - ds_book(1e3)) * 1e3 - 12) < 0.5)
check('NEG: previously printed P disagrees with quadrature', not all(abs(P_old(t) / P_quad(t) - 1) < 1e-2 for t in ts))
check('NEG: previously printed d_s(tau->0) is not 2', abs(ds_old(1e-6) - 2) > 1)

# 2. Planck energy density / pressure c^7/(hbar G^2).
Pp = c ** 7 / (hbar * G ** 2)
check('c^7/(hbar G^2) = 4.63e113 Pa', abs(Pp / 4.63e113 - 1) < 2e-3)
check('NEG: c^7/(hbar G^2 16 pi^2) is not 4.63e113', abs(Pp / (16 * np.pi ** 2) / 4.63e113 - 1) > 0.5)
rho_max = 3 / (8 * np.pi) * Pp
check('density ceiling 3/(8 pi) c^7/(hbar G^2) = 5.5e112 J/m^3', abs(rho_max / 5.5e112 - 1) < 0.01)
# dimensional check: [c^7/(hbar G^2)] = m^7 s^-7 / (J s * m^6 kg^-2 s^-4) = kg^2 m s^-3 / J = kg m^-1 s^-2 = Pa
check('dimension: exponents of (kg, m, s) are (1, -1, -2)',
      tuple(np.array([0, 7, -7]) - np.array([1, 2, -1]) - 2 * np.array([-1, 3, -2])) == (1, -1, -2))

# 3. Koide: Tr P / ||P||_F^2 for the projector onto the standard representation.
Pm = np.eye(3) - np.ones((3, 3)) / 3
check('Tr P / ||P||_F^2 = 1 (not 2/3)', abs(np.trace(Pm) / np.sum(Pm * Pm) - 1) < 1e-12)
me, mmu, mtau = 0.51099895, 105.6583755, 1776.86  # PDG, MeV
Q = (me + mmu + mtau) / (math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mtau)) ** 2
check('empirical Q_l = 0.66666 (PDG masses)', abs(Q - 2 / 3) < 2e-5)
# Foot parametrisation with b/a = 1/sqrt2 gives 2/3 for every delta and v0 (so it assumes Koide)
rng = np.random.default_rng(1)
qs = []
for _ in range(20):
    d, v0 = rng.uniform(0, 2 * np.pi), rng.uniform(0.1, 10)
    s = v0 * (1 + math.sqrt(2) * np.cos(d + 2 * np.pi * np.arange(3) / 3))
    qs.append(np.sum(s ** 2) / np.sum(s) ** 2)
check('Foot parametrisation gives 2/3 for all (delta, v0): Koide is an input', np.allclose(qs, 2 / 3))
s = 1 + 1.2 * np.cos(0.3 + 2 * np.pi * np.arange(3) / 3)
check('NEG: amplitude 1.2 instead of sqrt2 gives Q != 2/3', abs(np.sum(s ** 2) / np.sum(s) ** 2 - 2 / 3) > 0.05)

# 4. Alternating sum of facet volumes of the standard 4-simplex.
V = np.eye(5)


def vol(pts):
    E = pts[1:] - pts[0]
    return math.sqrt(np.linalg.det(E @ E.T)) / math.factorial(len(E))


f = [vol(np.delete(V, i, axis=0)) for i in range(5)]
alt = sum((-1) ** i * fi for i, fi in enumerate(f))
check('alternating facet-volume sum equals one facet volume (not 0)', abs(alt - f[0]) < 1e-12 and alt > 0)
# chain-level identity d o d = 0 on the 4-simplex (boundary matrices)
from itertools import combinations
faces = {k: list(combinations(range(5), k + 1)) for k in range(5)}


def bd(k):
    M = np.zeros((len(faces[k - 1]), len(faces[k])))
    for j, s in enumerate(faces[k]):
        for i in range(len(s)):
            M[faces[k - 1].index(s[:i] + s[i + 1:]), j] = (-1) ** i
    return M


check('chain identity d3 d4 = 0', np.allclose(bd(3) @ bd(4), 0))
check('NEG: unsigned boundary gives d3 d4 != 0', not np.allclose(np.abs(bd(3)) @ np.abs(bd(4)), 0))

# 5. Born-rule regions B_n: FS volume fraction is 1/N, independent of the state.
N, M = 4, 400000
z = rng.normal(size=(M, N)) + 1j * rng.normal(size=(M, N))
frac = np.bincount(np.argmax(np.abs(z), axis=1), minlength=N) / M
check('FS volume of each B_n is 1/N', np.allclose(frac, 1 / N, atol=3e-3))
cs = np.array([0.8, 0.5, 0.3, math.sqrt(1 - 0.64 - 0.25 - 0.09)])
check('NEG: |c_n|^2 for a generic state differs from 1/N', not np.allclose(cs ** 2, 1 / N, atol=3e-3))

# 6. ADM bounds: e2 on [-a,a]^3 ranges over [-a^2, 3a^2]; (ii) R >= 16 pi G rho - 2K^2/3 needs no bound.
lam = rng.uniform(-1, 1, size=(200000, 3))
e2 = lam[:, 0] * lam[:, 1] + lam[:, 1] * lam[:, 2] + lam[:, 2] * lam[:, 0]
check('e2 in [-1, 3] on the unit cube', e2.min() >= -1 - 1e-12 and e2.max() <= 3 + 1e-12)
lam = rng.normal(scale=50, size=(200000, 3))  # no bound at all
K = lam.sum(1)
KK = (lam ** 2).sum(1)
sig = KK - K ** 2 / 3
R = KK - K ** 2  # vacuum, Lambda = 0: R = K_ij K^ij - K^2
check('R >= -2K^2/3 holds without any curvature bound', np.all(R >= -2 * K ** 2 / 3 - 1e-9) and np.all(sig >= -1e-9))
check('NEG: R >= 0 fails in general', not np.all(R >= 0))

# 7. FLRW: Hdot = -4 pi G (rho + P) (c = 1); at H = 0 with rho + P > 0 one has Hdot < 0.
# check with de Sitter-free dust: a ~ t^(2/3), H = 2/(3t), rho = 1/(6 pi G t^2), P = 0.
Gn = 1.0
t = 2.0
H = lambda t: 2 / (3 * t)
Hdot = (H(t + 1e-6) - H(t - 1e-6)) / 2e-6
rho = 1 / (6 * np.pi * Gn * t ** 2)
check('dust: Hdot = -4 pi G rho', abs(Hdot + 4 * np.pi * Gn * rho) < 1e-6)
check('NEG: Hdot = +4 pi G rho fails', abs(Hdot - 4 * np.pi * Gn * rho) > 1e-3)

# 8. Observability numbers (ch. 13): GW delay and required scale; strontium l_P / lambda_dB.
lP = math.sqrt(hbar * G / c ** 3)
H0 = 70e3 / 3.0857e22
Om, OL = 0.3, 0.7


def D2(zz):
    return c / H0 * integrate.quad(lambda x: (1 + x) ** 2 / math.sqrt(Om * (1 + x) ** 3 + OL), 0, zz)[0]


def dt(zz, l, xi=0.5, f1=10, f2=1e3):
    return 6 * np.pi ** 2 * xi * l ** 2 / c ** 3 * D2(zz) * (f2 ** 2 - f1 ** 2)


d1, d3, d8 = dt(1, lP), dt(3, lP), dt(8, lP)
print(f'     GW delays z=1,3,8: {d1:.2e} {d3:.2e} {d8:.2e} s')
check('GW delays 6e-62 .. 1.2e-60 s', 5e-62 < d1 < 7e-62 and 1e-60 < d8 < 1.4e-60)
lreq = lP * math.sqrt(1e-4 / d3)
print(f'     required l* = {lreq:.2e} m, hbar c / l* = {hbar * c / lreq / 1.602176634e-19:.2f} eV')
check('required l* ~ 3.0e-7 m, ~0.7 eV', 2.8e-7 < lreq < 3.2e-7)
check('NEG: 4.7e-7 m does not give 1e-4 s at z=3', abs(dt(3, 4.7e-7) / 1e-4 - 1) > 0.5)
mSr = 86.909 * 1.66053907e-27
ratio = mSr * 1.0 * lP / (2 * np.pi * hbar)
check('Sr l_P/lambda_dB = 3.5e-27 (v/1 m/s)', abs(ratio / 3.5e-27 - 1) < 0.03)

# 9. Tensor tilt at horizon exit: H_inf bound and |alpha_t|.
MP = 1.220890e19  # GeV
Mred = MP / math.sqrt(8 * np.pi)
Hinf = math.sqrt(0.036 * 2.1e-9 * np.pi ** 2 * Mred ** 2 / 2)
print(f'     H_inf <= {Hinf:.2e} GeV, |alpha_t| <= {(Hinf / MP) ** 2:.2e}')
check('H_inf <= 4.7e13 GeV and |alpha_t| <= 1.5e-11', abs(Hinf / 4.7e13 - 1) < 0.03 and abs((Hinf / MP) ** 2 / 1.5e-11 - 1) < 0.05)

print('FAILURES:', fail if fail else 'none')
sys.exit(1 if fail else 0)
