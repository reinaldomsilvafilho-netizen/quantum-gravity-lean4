"""Cap. 13, reauditoria cega: running do tilt tensorial, escalas CMB, interferometria atomica.

Oraculos: conversoes de unidade feitas com CODATA 2018 a partir de SI; escala fisica
do modo tensorial na saida do horizonte via k_phys = a H = H_inf, com H_inf obtido de
P_t = 2 H^2/(pi^2 M_red^2) = r A_s (limite BICEP/Keck 2021 r < 0.036, Planck A_s=2.1e-9).
Controles negativos: formulas mutadas devem falhar.
"""
import numpy as np
import sympy as sp

c = 299792458.0
hbar = 1.054571817e-34
h = 2 * np.pi * hbar
G = 6.67430e-11
eV = 1.602176634e-19
Mpc = 3.0856775814913673e22
u = 1.66053906660e-27
hbarc_GeVm = hbar * c / eV / 1e9
MP = np.sqrt(hbar * c / G) * c**2 / eV / 1e9
Mred = MP / np.sqrt(8 * np.pi)

# --- alpha_t = (d_s-4)/2 com Pade ---
x = sp.symbols("x", positive=True)
ds = 2 + 2 / (1 + x**2)
alpha = sp.simplify((ds - 4) / 2)
assert sp.simplify(alpha + x**2 / (1 + x**2)) == 0
assert sp.simplify(((2 + 1 / (1 + x**2)) - 4) / 2 + x**2 / (1 + x**2)) != 0  # controle negativo
print("alpha_t =", alpha, "; serie IR de d_s:", sp.series(ds, x, 0, 4))
# Pade IR: d_s = 4 - 2 x^2 ; modelo exato: d_s = 4 - 12 l^2/tau (ver ch13_heat_kernel.py)
# -> com tau ~ 1/k^2 o coeficiente e 12 vs 2: "Pade" nao casa o coeficiente, so a potencia.

# --- pivot CMB ---
k_piv = 0.05 / Mpc * hbarc_GeVm
print(f"k_pivot = {k_piv:.3e} GeV (texto ~3e-40)")
assert abs(k_piv / 3e-40 - 1) < 0.1
a_piv = (k_piv / MP) ** 2 / (1 + (k_piv / MP) ** 2)
print(f"|alpha_t|(pivot, M_*=M_P) = {a_piv:.2e} (texto 7e-118)")
assert abs(a_piv / 7e-118 - 1) < 0.05
a_piv_bad = (k_piv / MP) / (1 + (k_piv / MP))   # controle negativo: potencia 1
assert abs(a_piv_bad / 7e-118 - 1) > 1
chi_star = 13900.0  # Mpc, distancia comovel ao ultimo espalhamento (Planck 2018 ~ 13.9 Gpc)
for ell in [2, 2000, 4000]:
    kk = ell / chi_star / Mpc * hbarc_GeVm
    print(f" ell={ell}: k={ell/chi_star:.2e}/Mpc, k/M_P={kk/MP:.1e}, |alpha_t|={(kk/MP)**2:.1e}")
print(" -> faixa CMB em k/M_P: ~1e-61 a ~2e-58")
print(f" com M_*=M_red: |alpha_t|(pivot) = {(k_piv/Mred)**2:.1e}")

# --- escala fisica relevante: H_inf na saida do horizonte ---
As, r = 2.1e-9, 0.036
H_inf = np.pi * Mred * np.sqrt(As * r / 2)
print(f"\nH_inf (r<0.036) <= {H_inf:.2e} GeV ; (H_inf/M_P)^2 = {(H_inf/MP)**2:.1e} ; (H_inf/M_red)^2 = {(H_inf/Mred)**2:.1e}")
print(f" razao entre as duas estimativas: 10^{np.log10((H_inf/MP)**2/a_piv):.0f}")

# --- Interferometria atomica: l_P / lambda_dB para Sr-87 / Sr-88 ---
lP = np.sqrt(hbar * G / c**3)
for A in [87, 88]:
    m = A * u
    v_bound = 4e-26 * h / (m * lP)  # v tal que l_P/lambda = 4e-26
    print(f"\nSr-{A}: l_P/lambda_dB = 4e-26  <=>  v = {v_bound:.1f} m/s")
    for v in [0.01, 1.0, 10.0, 30.0, 44.0]:
        lam = h / (m * v)
        print(f"  v={v:6.2f} m/s: lambda_dB={lam:.2e} m, l_P/lambda={lP/lam:.1e}")
v_launch_50m = np.sqrt(2 * 9.81 * 50)
print(f" lancamento vertical a 50 m de altura: v0 = {v_launch_50m:.1f} m/s")
print(f" recuo de 1 foton 698 nm, Sr-87: {h/(87*u*698e-9)*1e3:.2f} mm/s")
print("OK")
