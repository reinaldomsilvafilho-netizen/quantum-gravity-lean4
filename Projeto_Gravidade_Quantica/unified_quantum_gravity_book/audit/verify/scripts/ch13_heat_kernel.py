"""Cap. 13, reauditoria cega: kernel de difusao k^2 + l^2 k^4 e d_s(tau).

Oraculo independente: quadratura numerica direta de
  P(tau) = (2pi)^-4 int d^4k exp(-tau(k^2 + l^2 k^4))  (medida 2 pi^2 k^3 dk)
e derivada logaritmica por diferencas finitas (nao usa a forma fechada).
Controles negativos: formulas mutadas devem falhar.
Unidades: l = 1 (tau em unidades de l^2).
"""
import numpy as np
from scipy.integrate import quad
from scipy.special import erfcx

L = 1.0


def P_quad(tau):
    f = lambda k: 2 * np.pi**2 * k**3 * np.exp(-tau * (k**2 + L**2 * k**4)) / (2 * np.pi) ** 4
    kmax = min(1.0 / np.sqrt(tau), (1.0 / tau) ** 0.25) * 60
    return quad(f, 0, kmax, limit=500, epsabs=0, epsrel=1e-13)[0]


def P_closed(tau, mutate=None):
    z = np.sqrt(tau) / (2 * L)
    g = np.sqrt(np.pi) * z * erfcx(z)          # sqrt(pi) z e^{z^2} erfc z
    if mutate == "sign":
        g = -g
    pref = 1 / (32 * np.pi**2 * L**2 * tau)
    if mutate == "factor2":
        pref *= 2
    return pref * (1 - g)


def ds_closed(tau, mutate=None):
    z = np.sqrt(tau) / (2 * L)
    B = 1 - np.sqrt(np.pi) * z * erfcx(z)
    lin = tau / (2 * L**2)
    if mutate == "lin_sign":
        lin = -lin
    if mutate == "lin_quarter":
        lin = tau / (4 * L**2)
    return 1 - lin + 1 / B


def ds_numeric(tau, h=1e-4):
    return -2 * (np.log(P_quad(tau * np.exp(h))) - np.log(P_quad(tau * np.exp(-h)))) / (2 * h)


taus = np.logspace(-3, 2, 41)
relP = max(abs(P_closed(t) / P_quad(t) - 1) for t in taus)
absds = max(abs(ds_closed(t) - ds_numeric(t)) for t in taus)
print(f"max rel err P closed vs quad, tau in [1e-3,1e2]: {relP:.2e}")
print(f"max abs err d_s closed vs numeric derivative:   {absds:.2e}")
assert relP < 1e-6 and absds < 1e-6

# limites
print("d_s(1e-8) =", ds_closed(1e-8), " d_s(1e4) =", ds_closed(1e4))
assert abs(ds_closed(1e-8) - 2) < 1e-3 and abs(ds_closed(1e4) - 4) < 1e-2
# coeficiente IR: d_s = 4 - C l^2/tau ; previsao analitica C = 12 (3/z^2 com z^2 = tau/4l^2)
for t in [1e3, 1e4]:
    print(f"tau={t:g}: (4-d_s)*tau/l^2 = {(4-ds_closed(t))*t:.4f}  (esperado 12)")
assert abs((4 - ds_closed(1e4)) * 1e4 - 12) < 0.05
# UV: d_s - 2 ~ sqrt(pi) z (linear em sqrt(tau), NAO quadratico)
t = 1e-6
print(f"UV: (d_s-2)/(sqrt(pi) z) at tau=1e-6: {(ds_closed(t)-2)/(np.sqrt(np.pi)*np.sqrt(t)/2):.4f}")

# controles negativos
for m in ["sign", "factor2"]:
    err = max(abs(P_closed(t, m) / P_quad(t) - 1) for t in taus)
    print(f"[neg] P mutacao {m}: max rel err = {err:.2e}")
    assert err > 1e-2
for m in ["lin_sign", "lin_quarter"]:
    err = max(abs(ds_closed(t, m) - ds_numeric(t)) for t in taus)
    print(f"[neg] d_s mutacao {m}: max abs err = {err:.2e}")
    assert err > 1e-2

# ---- Nucleo anisotropico (Horava/SVW): exp(-tau(w^2 + k^2 + l^2 k^4)), 3+1 ----
# P ~ tau^{-1/2} * int k^2 exp(-tau(k^2+l^2k^4)) dk ; d_s UV = 1 + 3/2 = 2.5, IR = 4
def P_aniso(tau):
    f = lambda k: k**2 * np.exp(-tau * (k**2 + L**2 * k**4))
    kmax = min(1.0 / np.sqrt(tau), (1.0 / tau) ** 0.25) * 60
    return tau**-0.5 * quad(f, 0, kmax, limit=500, epsrel=1e-13)[0]


def ds_aniso(tau, h=1e-4):
    return -2 * (np.log(P_aniso(tau * np.exp(h))) - np.log(P_aniso(tau * np.exp(-h)))) / (2 * h)


print(f"anisotropico 3+1, z=2: d_s(UV,1e-8) = {ds_aniso(1e-8):.4f}, d_s(IR,1e5) = {ds_aniso(1e5):.4f}")
assert abs(ds_aniso(1e-8) - 2.5) < 1e-2
# Horava z=3: k^2 + l^4 k^6 -> UV d_s = 1 + 3/3 = 2
def P_aniso3(tau):
    f = lambda k: k**2 * np.exp(-tau * (k**2 + L**4 * k**6))
    kmax = min(1.0 / np.sqrt(tau), (1.0 / tau) ** (1 / 6)) * 60
    return tau**-0.5 * quad(f, 0, kmax, limit=500, epsrel=1e-13)[0]
h = 1e-4; t = 1e-9
d3 = -2 * (np.log(P_aniso3(t*np.exp(h))) - np.log(P_aniso3(t*np.exp(-h)))) / (2*h)
print(f"anisotropico 3+1, z=3: d_s(UV) = {d3:.4f}")
assert abs(d3 - 2) < 1e-2
print("OK")
