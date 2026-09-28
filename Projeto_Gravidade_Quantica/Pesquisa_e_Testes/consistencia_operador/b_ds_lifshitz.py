"""Branch (b): anisotropic (Horava-Lifshitz type) operator, second order in time.

Euclidean heat kernel of  -d_t^2 + F(-Lap_3),  F(k^2) = k^2 + a k^4/M^2 + k^{2z}/M^{2z-2}   (M = 1):
    P(tau) = (4 pi tau)^{-1/2} * (1/(2 pi^2)) int_0^inf k^2 exp(-tau F(k^2)) dk
    d_s(tau) = -2 dlnP/dln tau.
Two independent evaluations of d_s:
    method 1: centred finite difference of ln P in ln tau (P by scipy quad on a log-substituted integrand)
    method 2: moment identity d_s = 1 + 2 tau <F>, <F> = int k^2 F e^{-tau F} / int k^2 e^{-tau F}
              (evaluated with mpmath at 30 digits, different quadrature library)
Oracle for the limits: exact scaling  d_s(UV) = 1 + D/z  (D = 3), d_s(IR) = 1 + D = 4.
Negative control: mutated z = 2 (the book's 'anisotropic k^4' operator) must FAIL the d_s -> 2 test
(it must go to 5/2).  Extra: the book's isotropic closed form (B0) against quadrature, with a
mutated closed form (prefactor u dropped) that must fail.
"""
import numpy as np
import mpmath as mp
from scipy.integrate import quad
from scipy.special import erfcx

mp.mp.dps = 30
PASS = []


def check(name, cond):
    PASS.append((name, bool(cond)))
    print(('PASS ' if cond else 'FAIL ') + name)


def F(k, z, a=0.0):
    return k**2 + a * k**4 + k**(2 * z)


def lnP_scipy(tau, z, a=0.0):
    # substitute k = e^x to cover many decades robustly
    f = lambda x: np.exp(3 * x - tau * F(np.exp(x), z, a))
    # integrand support: F(k) ~ 1/tau
    kc = min(tau**-0.5, tau**(-1 / (2 * z)))
    x0 = np.log(kc)
    val, _ = quad(f, x0 - 40, x0 + 6, limit=500, epsabs=0, epsrel=1e-12, points=[x0])
    return -0.5 * np.log(4 * np.pi * tau) + np.log(val / (2 * np.pi**2))


def ds_fd(tau, z, a=0.0, h=1e-3):
    return -2 * (lnP_scipy(tau * np.exp(h), z, a) - lnP_scipy(tau * np.exp(-h), z, a)) / (2 * h)


def ds_moment(tau, z, a=0.0):
    tau = mp.mpf(tau)
    Fm = lambda k: k**2 + a * k**4 + k**(2 * z)
    kc = min(tau**-0.5, tau**(-mp.mpf(1) / (2 * z)))
    pts = [0, kc / 10, kc, 10 * kc, 100 * kc, mp.inf]
    num = mp.quad(lambda k: k**2 * Fm(k) * mp.e**(-tau * Fm(k)), pts)
    den = mp.quad(lambda k: k**2 * mp.e**(-tau * Fm(k)), pts)
    return float(1 + 2 * tau * num / den)


print('--- d_s(tau) for z = 3 (Horava branch), M = 1 ---')
taus = np.logspace(-9, 6, 16)
rows = []
for t in taus:
    d1, d2 = ds_fd(t, 3), ds_moment(t, 3)
    rows.append((t, d1, d2))
    print(f'tau={t:9.2e}  d_s(FD)={d1:.6f}  d_s(moment)={d2:.6f}  diff={abs(d1 - d2):.1e}')
check('B1 two independent evaluations agree (|diff| < 1e-5)', max(abs(r[1] - r[2]) for r in rows) < 1e-5)
check('B2 UV limit z=3: d_s(1e-9) within 1e-3 of 1 + 3/3 = 2', abs(rows[0][2] - 2.0) < 1e-3)
check('B3 IR limit: d_s(1e6) within 1e-3 of 4', abs(rows[-1][2] - 4.0) < 1e-3)
mono = all(rows[i][2] <= rows[i + 1][2] + 1e-9 for i in range(len(rows) - 1))
check('B4 d_s monotone non-decreasing in tau for z=3', mono)

# UV approach rate: d_s - 2 ~ C tau^{2/3} (from tau k^2 with k ~ tau^{-1/6})
t1, t2 = 1e-9, 1e-7
e1, e2 = ds_moment(t1, 3) - 2, ds_moment(t2, 3) - 2
slope = np.log(e2 / e1) / np.log(t2 / t1)
print(f'UV approach exponent d ln(d_s-2)/d ln tau = {slope:.4f} (expected 2/3)')
check('B5 UV correction scales as tau^{2/3}', abs(slope - 2 / 3) < 1e-2)

print('\n--- z = 3 with an extra quartic term a k^4 (a = +-0.5): UV value unchanged ---')
for a in (0.5, -0.5 * 0.99):
    # a < 0 only allowed while F > 0 for all k: k^2 + a k^4 + k^6 > 0 iff a > -2
    dUV = ds_moment(1e-9, 3, a)
    print(f'a={a:+.3f}: d_s(1e-9)={dUV:.5f}, d_s(1e6)={ds_moment(1e6, 3, a):.5f}')
    check(f'B6 quartic admixture a={a:+.2f} keeps UV d_s = 2', abs(dUV - 2) < 2e-3)

print('\n--- negative control: mutated z = 2 ---')
d_mut = ds_moment(1e-9, 2)
print(f'z=2: d_s(1e-9)={d_mut:.5f} (exact scaling 1+3/2 = 2.5)')
check('NC1 z=2 must fail the d_s->2 test', abs(d_mut - 2.0) > 0.4)
check('NC1b z=2 reproduces the book statement d_s -> 5/2', abs(d_mut - 2.5) < 2e-3)
print('\nGeneral z: UV value vs 1 + 3/z')
for z in (1, 2, 3, 4, 6):
    d = ds_moment(1e-12, z) if z > 1 else ds_moment(1e-3, 1)
    print(f'z={z}: d_s(UV)={d:.4f}  1+3/z={1 + 3 / z:.4f}')
    check(f'B7 z={z}: d_s(UV) = 1+3/z within 5e-3', abs(d - (1 + 3 / z)) < 5e-3)

# ---------- B0: isotropic book closed form ----------------------------------
print('\n--- B0: isotropic 4D symbol k^2 + l^2 k^4 (book Prop.), l = 1 ---')


def P_iso_quad(tau):
    f = lambda u: u * np.exp(-tau * (u + u**2))
    uc = min(1 / tau, tau**-0.5)
    v, _ = quad(f, 0, np.inf, points=None, limit=400, epsrel=1e-12) if uc > 50 else \
        quad(f, 0, 200 * uc + 50, limit=400, epsrel=1e-12)
    return v / (16 * np.pi**2)


def P_iso_closed(tau):
    zz = np.sqrt(tau) / 2
    return (1 - np.sqrt(np.pi) * zz * erfcx(zz)) / (32 * np.pi**2 * tau)


def P_iso_mut(tau):  # prefactor u dropped (a plausible slip): int e^{-tau(u+u^2)} du
    zz = np.sqrt(tau) / 2
    return np.sqrt(np.pi) * erfcx(zz) / (2 * np.sqrt(tau)) / (16 * np.pi**2)


e_ok, e_mut = [], []
for t in np.logspace(-3, 2, 11):
    q = P_iso_quad(t)
    e_ok.append(abs(q - P_iso_closed(t)) / q)
    e_mut.append(abs(q - P_iso_mut(t)) / q)
print('max rel err closed form:', '%.1e' % max(e_ok), ' mutant:', '%.1e' % min(e_mut))
check('B0 book closed form matches quadrature (rel < 1e-8)', max(e_ok) < 1e-8)
check('NC2 mutated closed form rejected', min(e_mut) > 1e-2)

print('\nSUMMARY: %d/%d PASS' % (sum(c for _, c in PASS), len(PASS)))
