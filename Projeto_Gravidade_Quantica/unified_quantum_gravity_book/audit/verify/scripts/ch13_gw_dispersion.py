"""Cap. 13, reauditoria cega: atraso de dispersao de ondas gravitacionais.

Oraculo independente: propagacao numerica em FRW plana (LCDM) de dois pacotes
com velocidade de grupo exata v_g(k_phys), k_phys = k_obs (1+z) (k comovel conservado),
resolvendo o tempo conforme de chegada por busca de raiz. Nao usa a formula D_2.
Compara com a formula do texto  Dt = 6 pi^2 xi l^2 D(z) (f2^2-f1^2)/c^3  com
  D_n(z) = (c/H0) int_0^z (1+z')^n dz'/E(z')   para n = 1 (texto) e n = 2.
Controle negativo: a variante errada deve falhar contra o oraculo.
CODATA 2018: c, hbar, G exatos/recomendados.
"""
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

c = 299792458.0
hbar = 1.054571817e-34
G = 6.67430e-11
eV = 1.602176634e-19
Mpc = 3.0856775814913673e22
lP = np.sqrt(hbar * G / c**3)
MP_GeV = np.sqrt(hbar * c / G) * c**2 / eV / 1e9
print(f"l_P = {lP:.4e} m ; M_P c^2 = {MP_GeV:.4e} GeV (texto: 1.22e19)")
assert abs(MP_GeV / 1.22e19 - 1) < 0.01

H0 = 70e3 / Mpc
Om, OL = 0.3, 0.7
E = lambda z: np.sqrt(Om * (1 + z) ** 3 + OL)


def D(z, n):
    return c / H0 * quad(lambda x: (1 + x) ** n / E(x), 0, z)[0]


# --- group velocity (simbolico) ---
k, l, xi, cc = sp.symbols("k l xi c", positive=True)
w = cc * k * sp.sqrt(1 + xi * l**2 * k**2)
vg = sp.diff(w, k)
ser = sp.series(vg / cc, l, 0, 4).removeO()
print("v_g/c =", sp.simplify(ser))
assert sp.simplify(ser - (1 + sp.Rational(3, 2) * xi * l**2 * k**2)) == 0
# 4D covariante: p^2 (1 + l^2 p^2) = 0 -> p^2 = 0 (sem dispersao) ou p^2=-1/l^2 (fantasma)
p2 = sp.symbols("p2")
print("raizes do simbolo covariante p^2+l^2p^4:", sp.solve(p2 + l**2 * p2**2, p2))


def delay_formula(z, ell, xi_, f1, f2, n):
    return 6 * np.pi**2 * xi_ * ell**2 / c**3 * D(z, n) * (f2**2 - f1**2)


def delay_oracle(z, ell, xi_, f1, f2):
    """Tempo conforme: d chi / d eta = v_g/c * c; eta(z) = int_0^z dz'/H (em s)."""
    def eta_of_z(zz):  # tempo conforme entre z e hoje (a0=1), em segundos
        return quad(lambda x: 1 / (H0 * E(x)), 0, zz, epsrel=1e-13)[0]

    def travel(f):
        kobs = 2 * np.pi * f / c
        # chi = int v_g(k_phys)/c * c d eta = c * int_0^z (v/c) dz/H
        def eps(x):
            X = xi_ * ell**2 * (kobs * (1 + x)) ** 2
            s1 = np.sqrt(1 + X)
            return (2 * X - X / (s1 + 1)) / s1   # (1+2X)/sqrt(1+X) - 1, forma estavel
        # v_g/c - 1 = eps (exato para w = ck sqrt(1+xi l^2 k^2))
        return quad(lambda x: eps(x) / (H0 * E(x)), 0, z, epsrel=1e-13)[0]
    # para 1a ordem em eps, delta eta_o = int eps d eta ; a0=1 -> delta t_o = delta eta_o
    return travel(f2) - travel(f1)


# Oraculo com l grande (efeito resolvivel) mas ainda perturbativo
ell_big = 1.0
for z in [1, 3, 8]:
    o = delay_oracle(z, ell_big, 0.5, 10.0, 1e3)
    t1 = delay_formula(z, ell_big, 0.5, 10.0, 1e3, 1)
    t2 = delay_formula(z, ell_big, 0.5, 10.0, 1e3, 2)
    print(f"z={z}: oraculo {o:.4e} s | formula (1+z)^2 {t2:.4e} | texto (1+z)^1 {t1:.4e} | razao texto/oraculo {t1/o:.3f}")
    assert abs(t2 / o - 1) < 1e-6
    # controle negativo: a formula do texto deve FALHAR contra o oraculo
    assert abs(t1 / o - 1) > 0.3

# Checagem cruzada do oraculo por integracao em tempo cosmico (solucao de chi)
# -- com l enorme, resolvendo t de chegada exatamente (nao-perturbativo) --
def arrival_exact(z, ell, xi_, f):
    kobs = 2 * np.pi * f / c
    vg_over_c = lambda x: (1 + 2 * xi_ * ell**2 * (kobs*(1+x))**2) / np.sqrt(1 + xi_ * ell**2 * (kobs*(1+x))**2)
    chi_light = c * quad(lambda x: 1 / (H0 * E(x)), 0, z, epsrel=1e-13)[0]
    # onda com v_g: emitida em z, chega em z_arr<0 (futuro) ; resolver chi(z_arr)=chi_light
    # d chi = v dt / a ;  a(t) extrapolado para z<0 com a mesma E(z)
    def chi_of(zarr):
        return c * quad(lambda x: vg_over_c(x) / (H0 * E(x)), zarr, z, epsrel=1e-13)[0]
    zarr = brentq(lambda y: chi_of(y) - chi_light, -1e-3, 1e-3, xtol=1e-18)
    # tempo apos hoje: t = int_zarr^0 dz/((1+z)H)
    return quad(lambda x: 1 / ((1 + x) * H0 * E(x)), zarr, 0, epsrel=1e-13)[0]
ell_huge = 30.0
o_ex = arrival_exact(3, ell_huge, 0.5, 1e3) - arrival_exact(3, ell_huge, 0.5, 10.0)
print(f"z=3 l=30 m: chegada exata {o_ex:.4e} s vs formula (1+z)^2 {-delay_formula(3, ell_huge, 0.5, 10, 1e3, 2):.4e} s")
assert abs(-o_ex / delay_formula(3, ell_huge, 0.5, 10, 1e3, 2) - 1) < 1e-3

# --- numeros do texto (l = l_P, xi=1/2, 10 Hz - 1 kHz) ---
print("\nValores com l_* = l_P:")
for z in [1, 3, 8]:
    t1 = delay_formula(z, lP, 0.5, 10, 1e3, 1)
    t2 = delay_formula(z, lP, 0.5, 10, 1e3, 2)
    print(f" z={z}: texto(1+z) {t1:.2e} s ; correto(1+z)^2 {t2:.2e} s ; log10(1e-4/t) = {np.log10(1e-4/t1):.1f} / {np.log10(1e-4/t2):.1f}")

for n in [1, 2]:
    t = delay_formula(3, lP, 0.5, 10, 1e3, n)
    ell_req = lP * np.sqrt(1e-4 / t)
    Escale = hbar * c / ell_req / eV
    print(f" n={n}: l_* p/ 1e-4 s em z=3 = {ell_req:.3e} m ; hbar c/l = {Escale:.3f} eV")
# figura: relativo a 1 Hz ate 1 kHz
t_fig = delay_formula(3, 4.7e-7, 0.5, 1.0, 1e3, 1)
print(f" figura (texto D_1): l=4.7e-7, z=3, 1 Hz->1 kHz: {t_fig:.3e} s")

# --- GW170817: |v-c|/c para l=4.7e-7 m a 100 Hz ---
kk = 2 * np.pi * 100 / c
print(f"\n(3/2) xi (l k)^2 a 100 Hz, l=4.7e-7 m: {1.5*0.5*(4.7e-7*kk)**2:.1e}  (limite GW170817 ~1e-15)")
# --- LISA: f ~ 1e-3..1e-1 Hz ---
r = (1e-1**2) / (1e3**2)
print(f"LISA: (f2^2) para f2=0.1 Hz vs 1 kHz: razao {r:.0e}")
print("OK")
