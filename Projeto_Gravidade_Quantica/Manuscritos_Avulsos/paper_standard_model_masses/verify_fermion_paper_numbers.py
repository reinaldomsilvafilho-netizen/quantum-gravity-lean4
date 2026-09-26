"""Independent recomputation of every number in paper_fermion_mass_hierarchy.tex.

Inputs: PDG 2024 (S. Navas et al., Phys. Rev. D 110 (2024) 030001), summary
tables and CKM review, and Planck 2018 (A&A 641 (2020) A6) for H0, Omega_L.
Each block states: dimensions, value, classification (fit / prediction /
identity / known relation), and runs at least one independent oracle and one
negative control (a mutated formula that must fail the same check).

Run:  python verify_fermion_paper_numbers.py
"""
import math

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

FAIL = []


def check(name, cond):
    print(("  [ok]   " if cond else "  [FAIL] ") + name)
    if not cond:
        FAIL.append(name)


# ---------------------------------------------------------------- PDG 2024
ME, MMU = 0.51099895000, 105.6583755          # MeV
MTAU, SMTAU = 1776.93, 0.09                   # MeV
GF = 1.1663788e-5                             # GeV^-2
ALS, SALS = 0.1180, 0.0009                    # alpha_s(M_Z)
MZ = 91.1880                                  # GeV
MH, SMH = 125.20, 0.11                        # GeV
MD, SMD, MS, SMS = 4.70, 0.07, 93.5, 0.8      # MeV, MSbar at 2 GeV
MC_MC, MB_MB = 1.2730, 4.183                  # GeV, MSbar m(m)
MT_MSBAR = 162.5                              # GeV, MSbar m_t(m_t), PDG x-section
MT_POLE = 172.57                              # GeV, direct
MC_POLE, MB_POLE = 1.67, 4.78                 # GeV, PDG pole-mass notes
VUS, SVUS = 0.22431, 0.00085
VCB, VUB = 41.1e-3, 3.82e-3
S12F, S13F, S23F, DELF, SDELF = 0.22501, 0.003732, 0.04183, 1.147, 0.026
J_PDG, SJ_PDG = 3.12e-5, 0.13e-5              # global fit
SIN2_12, SS12 = 0.307, 0.013
SIN2_23, SS23 = 0.558, 0.021                  # normal order, lower error
SIN2_13, SS13 = 2.19e-2, 0.07e-2
DM2_32 = 2.455e-3                             # eV^2, normal order
GN = 6.70883e-39                              # hbar c (GeV/c^2)^-2
HBARC_GEVCM = 1.973269804e-14                 # GeV cm
GEV_IN_G = 1.78266192e-24                     # g per GeV/c^2
# Planck 2018 TT,TE,EE+lowE+lensing
H0, OMEGA_L = 67.36, 0.6847                   # km/s/Mpc

V = (math.sqrt(2) * GF) ** -0.5
print(f"v = (sqrt2 G_F)^-1/2 = {V:.3f} GeV")
check("v = 246.22 GeV", abs(V - 246.22) < 0.01)

# ---------------------------------------------------------------- 1. Koide
print("\n[1] Charged-lepton Koide ratio. Dimensionless (MeV/MeV).")
m = np.array([ME, MMU, MTAU])
Q = m.sum() / np.sqrt(m).sum() ** 2
# oracle: angle between sqrt-mass vector and (1,1,1); Q = 1/(3 cos^2 theta)
r = np.sqrt(m)
cos_t = r.sum() / (np.linalg.norm(r) * math.sqrt(3))
Q_angle = 1 / (3 * cos_t ** 2)
theta = math.degrees(math.acos(cos_t))
dQ = abs(Q - 2 / 3)
# uncertainty of Q from m_tau only (dominant)
eps = 1e-3
dQdm = ((m.sum() + eps) / (np.sqrt(m).sum() - math.sqrt(MTAU) + math.sqrt(MTAU + eps)) ** 2 - Q) / eps
sQ = abs(dQdm) * SMTAU
print(f"  Q_exp = {Q:.8f} +- {sQ:.1e};  angle = {theta:.5f} deg;  "
      f"|Q-2/3|/(2/3) = {dQ / (2 / 3) * 100:.5f} %  = {dQ / sQ:.2f} sigma")
check("Q direct == Q via angle", abs(Q - Q_angle) < 1e-12)
check("Q within 2 sigma of 2/3", dQ < 2 * sQ)
# circulant decomposition: v_j = a + 2b cos(delta + 2 pi j/3); Q = 1/3 + 2b^2/(3a^2)
a = r.mean()
b = np.linalg.norm(r - a) / math.sqrt(6)
check("Q = 1/3 + 2b^2/(3a^2)", abs(Q - (1 / 3 + 2 * b ** 2 / (3 * a ** 2))) < 1e-12)
check("negative control: Q = 1/3 + b^2/(3a^2) fails",
      abs(Q - (1 / 3 + b ** 2 / (3 * a ** 2))) > 1e-2)
print(f"  b/a = {b / a:.6f}  (1/sqrt2 = {1 / math.sqrt(2):.6f})")
# circulant parametrisation with ANY b/a is possible -> equipartition is an assumption
for ba in (0.3, 0.5, 1 / math.sqrt(2), 0.9):
    vv = np.array([1 + 2 * ba * math.cos(0.3 + 2 * math.pi * j / 3) for j in range(3)])
    print(f"    circulant with b/a={ba:.3f}: Q = {(vv ** 2).sum() / vv.sum() ** 2:.4f}")

# m_tau from Koide with (m_e, m_mu): solve Q(m_tau) = 2/3. Prediction of Koide 1982.
def koide_res(x):
    return (ME + MMU + x) / (math.sqrt(ME) + math.sqrt(MMU) + math.sqrt(x)) ** 2 - 2 / 3
mtau_brent = brentq(koide_res, 500, 5000)
# oracle: closed form. With s = sqrt(me)+sqrt(mmu), p = me+mmu, y = sqrt(m_tau):
# 3(p + y^2) = 2(s + y)^2  ->  y^2 - 4 s y + 3p - 2 s^2 = 0
s_ = math.sqrt(ME) + math.sqrt(MMU)
p_ = ME + MMU
y = 2 * s_ + math.sqrt(4 * s_ ** 2 - (3 * p_ - 2 * s_ ** 2))
mtau_closed = y ** 2
print(f"  m_tau(Koide) = {mtau_brent:.3f} MeV (closed form {mtau_closed:.3f});  "
      f"PDG {MTAU} +- {SMTAU}:  pull {(mtau_brent - MTAU) / SMTAU:+.2f} sigma")
check("m_tau Koide brentq == closed form", abs(mtau_brent - mtau_closed) < 1e-6)
check("m_tau Koide within 1 sigma of PDG 2024", abs(mtau_brent - MTAU) < SMTAU)
check("paper value 1776.88 MeV is NOT the Koide solution (|diff|>0.05)",
      abs(mtau_brent - 1776.88) > 0.05)
check("negative control: Q=0.70 gives m_tau far from PDG",
      abs(brentq(lambda x: (p_ + x) / (s_ + math.sqrt(x)) ** 2 - 0.70, 500, 5000) - MTAU) > 50)

# ---------------------------------------------------------------- 2. quark Koide
print("\n[2] Heavy-quark ratio Q_cbt. Dimensionless. Scheme dependent.")
Qq_formula = 2 / 3 * (1 + ALS / math.sqrt(3))
print(f"  (2/3)(1+alpha_s/sqrt3) = {Qq_formula:.5f}")
check("(2/3)(1+alpha_s/sqrt3) = 0.7121", abs(Qq_formula - 0.71208) < 1e-4)
check("negative control: C_F version (2/3)(1+C_F alpha_s/pi) != 0.7121",
      abs(2 / 3 * (1 + 4 / 3 * ALS / math.pi) - Qq_formula) > 5e-3)


def a_run(mu_from, a_from, mu_to, nf):
    """two-loop alpha_s/pi running"""
    b0 = (11 - 2 * nf / 3) / 4
    b1 = (102 - 38 * nf / 3) / 16
    f = lambda t, x: [-b0 * x[0] ** 2 - b1 * x[0] ** 3]
    sol = solve_ivp(f, [2 * math.log(mu_from), 2 * math.log(mu_to)], [a_from], rtol=1e-11, atol=1e-14)
    return sol.y[0, -1]


def m_run(mu_from, m_from, mu_to, a_from, nf):
    """two-loop mass running; returns (m, a) at mu_to"""
    b0 = (11 - 2 * nf / 3) / 4
    b1 = (102 - 38 * nf / 3) / 16
    g0, g1 = 1.0, (202 / 3 - 20 * nf / 9) / 16

    def f(t, x):
        aa, lm = x
        return [-b0 * aa ** 2 - b1 * aa ** 3, -g0 * aa - g1 * aa ** 2]
    sol = solve_ivp(f, [2 * math.log(mu_from), 2 * math.log(mu_to)], [a_from, math.log(m_from)],
                    rtol=1e-11, atol=1e-14)
    return math.exp(sol.y[1, -1]), sol.y[0, -1]


aZ = ALS / math.pi
a_mb = a_run(MZ, aZ, MB_MB, 5)
a_mc = a_run(MB_MB, a_mb, MC_MC, 4)
a_mt = a_run(MZ, aZ, MT_MSBAR, 5)
print(f"  alpha_s(m_b) = {a_mb * math.pi:.4f}, alpha_s(m_c) = {a_mc * math.pi:.4f}, alpha_s(m_t) = {a_mt * math.pi:.4f}")
mc_mb, _ = m_run(MC_MC, MC_MC, MB_MB, a_mc, 4)
mc_Z, _ = m_run(MB_MB, mc_mb, MZ, a_mb, 5)
mb_Z, _ = m_run(MB_MB, MB_MB, MZ, a_mb, 5)
mt_Z, _ = m_run(MT_MSBAR, MT_MSBAR, MZ, a_mt, 5)
print(f"  MSbar at M_Z (2-loop): m_c = {mc_Z:.3f}, m_b = {mb_Z:.3f}, m_t = {mt_Z:.2f} GeV")
# oracle: literature 4-loop values (Huang & Zhou, PRD 103 (2021) 016010, Table 2): 0.620, 2.839, 168.26
# two-loop truncation is known to overshoot at the charm scale (alpha_s(m_c) ~ 0.37)
check("m_c(M_Z) within 7% of 4-loop literature 0.620 (2-loop truncation)", abs(mc_Z / 0.620 - 1) < 0.07)
check("m_b(M_Z) within 3% of 4-loop literature 2.839", abs(mb_Z / 2.839 - 1) < 0.03)
check("m_t(M_Z) within 3% of 4-loop literature 168.26", abs(mt_Z / 168.26 - 1) < 0.03)


def koide(x):
    x = np.asarray(x, float)
    return x.sum() / np.sqrt(x).sum() ** 2


Q_msbar = koide([mc_Z, mb_Z, mt_Z])
Q_lit = koide([0.620, 2.839, 168.26])
Q_pole = koide([MC_POLE, MB_POLE, MT_POLE])
print(f"  Q_cbt: MSbar(M_Z) = {Q_msbar:.3f} (literature masses {Q_lit:.3f}); pole = {Q_pole:.3f}")
check("Q_cbt MSbar ~ 0.72", abs(Q_msbar - 0.72) < 0.01)
check("Q_cbt pole ~ 0.65", abs(Q_pole - 0.65) < 0.01)
print(f"  other triplets (MSbar at 2 GeV / m(m)): Q_uds = {koide([2.16e-3, 4.70e-3, 93.5e-3]):.3f}, "
      f"Q_dsb = {koide([4.70e-3, 93.5e-3, MB_MB]):.3f}, Q_uct = {koide([2.16e-3, MC_MC, MT_MSBAR]):.3f}")

# ---------------------------------------------------------------- 3. Cabibbo
print("\n[3] Gatto-Sartori-Tonin. Dimensionless (MeV/MeV, same scheme and scale).")
ratio = MD / MS
sratio = ratio * math.hypot(SMD / MD, SMS / MS)
gst = math.sqrt(ratio)
sgst = 0.5 * gst * sratio / ratio
gst_corr = gst * (1 + ALS / (4 * math.pi))
print(f"  sqrt(m_d/m_s) = {gst:.4f} +- {sgst:.4f};  x(1+alpha_s/4pi) = {gst_corr:.4f};  |V_us| = {VUS}")
print(f"  deviations from |V_us|: plain {abs(gst - VUS) / VUS * 100:.2f} %, corrected {abs(gst_corr - VUS) / VUS * 100:.2f} %")
print(f"  correction factor {ALS / (4 * math.pi) * 100:.2f} % vs input uncertainty {sgst / gst * 100:.2f} %")
check("sqrt(m_d/m_s) agrees with |V_us| within its input error", abs(gst - VUS) < math.hypot(sgst, SVUS))
check("oracle: m_s/m_ud = 27.33 consistent with m_s/m_d via m_u/m_d",
      abs(MS / ((2.16 + 4.70) / 2) - 27.33) < 0.5)
check("negative control: sqrt(m_u/m_c) (up sector) does not give V_us",
      abs(math.sqrt(2.16e-3 / MC_MC) - VUS) > 0.1)

# ---------------------------------------------------------------- 4. delta_CP, J
print("\n[4] CKM phase and Jarlskog invariant. Dimensionless.")
d_ans = math.pi / 3 + ALS / math.sqrt(3)
print(f"  pi/3 + alpha_s/sqrt3 = {d_ans:.4f} rad = {math.degrees(d_ans):.2f} deg;  PDG fit {DELF} +- {SDELF} rad "
      f"({math.degrees(DELF):.1f} deg):  pull {(d_ans - DELF) / SDELF:+.2f} sigma")


def jarlskog(s12, s23, s13, d):
    c12, c23, c13 = (math.sqrt(1 - x * x) for x in (s12, s23, s13))
    return c12 * c23 * c13 ** 2 * s12 * s23 * s13 * math.sin(d)


def jarlskog_matrix(s12, s23, s13, d):
    """oracle: J = Im(V_us V_cb V_ub* V_cs*) from the explicit PDG matrix"""
    c12, c23, c13 = (math.sqrt(1 - x * x) for x in (s12, s23, s13))
    e = np.exp(1j * d)
    Vm = np.array([[c12 * c13, s12 * c13, s13 / e],
                   [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
                   [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13]])
    check("  CKM matrix unitary", np.allclose(Vm @ Vm.conj().T, np.eye(3), atol=1e-12))
    return (Vm[0, 1] * Vm[1, 2] * np.conj(Vm[0, 2]) * np.conj(Vm[1, 1])).imag


J_paper = jarlskog(gst_corr, 0.0422, 0.00369, d_ans)
J_pdgin = jarlskog(gst_corr, S23F, S13F, d_ans)
J_fit = jarlskog(S12F, S23F, S13F, DELF)
print(f"  J(paper inputs s23=0.0422, s13=0.00369) = {J_paper:.3e}")
print(f"  J(PDG 2024 fit s23, s13; GST s12; ansatz delta) = {J_pdgin:.3e}  pull {(J_pdgin - J_PDG) / 0.12e-5:+.2f} sigma")
print(f"  J(PDG 2024 fit, all four) = {J_fit:.3e};  PDG quoted J = {J_PDG:.2e}")
check("J formula == Im of quartet (oracle)", abs(J_fit - jarlskog_matrix(S12F, S23F, S13F, DELF)) < 1e-12)
check("PDG fit reproduces quoted J within error", abs(J_fit - J_PDG) < SJ_PDG)
check("negative control: J without c13^2 and with cos(delta) fails",
      abs(0.97 * 0.999 * S12F * S23F * S13F * math.cos(DELF) - J_PDG) > SJ_PDG)
# sensitivity: fraction of J variance carried by empirical inputs s23, s13
print(f"  rel. uncertainty of J from s23 ({0.00074 / S23F * 100:.1f} %) and s13 ({0.0000875 / S13F * 100:.1f} %)")
# the closed mass formula from the book audit (F-04), for the record
mq = [2.16e-3, 4.70e-3, 93.5e-3, MC_MC, MB_MB, MT_POLE]
J_bad = math.sin(DELF) * math.sqrt(np.prod(mq)) / (6 * math.sqrt(3) * V ** 6)
print(f"  [F-04 record] sin(d) sqrt(prod m_q)/(6 sqrt3 v^6) = {J_bad:.2e} GeV^-3 (not in this paper)")
check("F-04 formula is ~1e-17, not 3e-5", J_bad < 1e-15)

# ---------------------------------------------------------------- 5. neutrinos
print("\n[5] Neutrino scale. [v^2/M] = GeV^2/GeV = GeV.")
M_GUT = 2.0e15
mnu = V ** 2 / M_GUT * 1e9
mnu_half = (V / math.sqrt(2)) ** 2 / M_GUT * 1e9
m3 = math.sqrt(DM2_32 + 7.53e-5)
print(f"  v^2/M_GUT = {mnu * 1e3:.2f} meV;  (v/sqrt2)^2/M_GUT = {mnu_half * 1e3:.2f} meV;  "
      f"sqrt(dm2_31) (NO, m1=0) = {m3 * 1e3:.1f} meV")
check("v^2/M_GUT = 30.3 meV", abs(mnu - 0.0303) < 0.0002)
check("order of magnitude matches sqrt(dm2_31)", 0.1 < mnu / m3 < 10)
check("negative control: v^2/M_Planck is not in range", not (0.1 < V ** 2 / 1.22e19 * 1e9 / m3 < 10))
M_needed = V ** 2 / (m3 * 1e-9)
print(f"  M giving m3 exactly: {M_needed:.2e} GeV (so M is a one-parameter fit)")
print("  PMNS ansatz: TBM + sin th13 = sin thC / sqrt2")
for name, th, ex, se in (("sin^2 th12", 1 / 3, SIN2_12, SS12), ("sin^2 th23", 0.5, SIN2_23, SS23)):
    print(f"    {name}: {th:.3f} vs {ex} +- {se}: pull {(th - ex) / se:+.1f} sigma")
s13_ans = gst_corr / math.sqrt(2)
s13_ex = math.sqrt(SIN2_13)
ss13 = 0.5 * SS13 / s13_ex
print(f"    sin th13 = {s13_ans:.4f} (with |V_us|: {VUS / math.sqrt(2):.4f}) vs {s13_ex:.4f} +- {ss13:.4f}: "
      f"pull {(s13_ans - s13_ex) / ss13:+.1f} sigma;  sin^2 th13 = {s13_ans ** 2:.4f} vs {SIN2_13}")
print(f"    with sin thC = |V_us|: pull {(VUS / math.sqrt(2) - s13_ex) / ss13:+.1f} sigma")
check("sin th13 ansatz excluded at > 4 sigma for both choices of sin thC",
      min(abs(s13_ans - s13_ex), abs(VUS / math.sqrt(2) - s13_ex)) / ss13 > 4)
check("negative control: pure TBM sin th13 = 0 is also excluded", s13_ex / ss13 > 5)

# ---------------------------------------------------------------- 6. vacuum energy
print("\n[6] Vacuum energy. [M_P^4] = GeV^4; exponent dimensionless.")
from math import comb
chi = sum((-1) ** k * comb(5, k + 1) for k in range(5))
chi_red = sum((-1) ** k * comb(5, k + 1) for k in range(-1, 5))
binom4 = sum((-1) ** k * comb(4, k) for k in range(5))
print(f"  sum_(k=0..4) (-1)^k C(5,k+1) = {chi} (Euler char. of Delta_4); with k=-1 term: {chi_red}; "
      f"sum (-1)^k C(4,k) = {binom4}")
check("chi(Delta_4) = 1, not 0", chi == 1)
check("reduced Euler characteristic = 0", chi_red == 0)
# volume-weighted sum: k-simplex with unit edges, Vol = sqrt(k+1)/(k! 2^(k/2))
vol = lambda k: math.sqrt(k + 1) / (math.factorial(k) * 2 ** (k / 2))
wsum = sum((-1) ** k * comb(5, k + 1) * vol(k) for k in range(5))
print(f"  sum (-1)^k C(5,k+1) Vol(Delta_k) (unit edges) = {wsum:.4f}  (not 0)")
check("volume-weighted alternating sum is not zero", abs(wsum) > 0.1)
check("sqrt5/96 = Vol(Delta_4), unit edge", abs(vol(4) - math.sqrt(5) / 96) < 1e-15)

E_inf = math.log(2) - 0.5
MP = math.sqrt(1 / GN)                       # GeV, non-reduced
MPr = MP / math.sqrt(8 * math.pi)
print(f"  E_inf = ln2 - 1/2 = {E_inf:.5f};  M_P = {MP:.4e} GeV, reduced {MPr:.4e} GeV")
aeff_formula = (1 / 24.5) / (math.sqrt(5) / 96 * 15.1)
print(f"  alpha_eff formula = {aeff_formula:.5f}")
for lab, M in (("M_P", MP), ("reduced M_P", MPr)):
    for al in (0.115, aeff_formula):
        r14 = M * math.exp(-math.pi / (2 * al * E_inf))
        print(f"    {lab:12s} alpha={al:.5f}: rho^(1/4) = {r14 * 1e12:.3f} meV, rho/M^4 = {(r14 / M) ** 4:.2e}")
# observed
H0_GeV = H0 * 1e3 / 3.0856775814913673e22 * 6.582119569e-25   # s^-1 -> GeV
rho_c = 3 * H0_GeV ** 2 / (8 * math.pi * GN)
rho_L = OMEGA_L * rho_c
# oracle: PDG rho_c = 1.05375e-5 h^2 GeV cm^-3
rho_c_or = 1.05375e-5 * (H0 / 100) ** 2 * HBARC_GEVCM ** 3
check("rho_c from G_N == PDG rho_c/h^2 formula", abs(rho_c / rho_c_or - 1) < 1e-3)
print(f"  observed rho_L = {rho_L:.3e} GeV^4 = ({rho_L ** 0.25 * 1e12:.3f} meV)^4 = "
      f"{rho_L * GEV_IN_G / HBARC_GEVCM ** 3:.2e} g/cm^3;  rho_L/M_P^4 = {rho_L / MP ** 4:.2e}, "
      f"/M_Pr^4 = {rho_L / MPr ** 4:.2e};  M_P^4 = {MP ** 4:.1e}, M_Pr^4 = {MPr ** 4:.1e} GeV^4")
p228 = (2.28e-12) ** 4
print(f"  paper: (2.28 meV)^4 = {p228:.3e} GeV^4 = {p228 * GEV_IN_G / HBARC_GEVCM ** 3:.2e} g/cm^3")
# alpha_eff required, and sensitivity
target = rho_L ** 0.25
al_need = brentq(lambda al: MP * math.exp(-math.pi / (2 * al * E_inf)) - target, 0.05, 0.3)
al_need_r = brentq(lambda al: MPr * math.exp(-math.pi / (2 * al * E_inf)) - target, 0.05, 0.3)
sens = math.pi / (2 * al_need ** 2 * E_inf)
print(f"  alpha_eff needed: {al_need:.5f} (M_P), {al_need_r:.5f} (reduced);  "
      f"d ln rho^(1/4) / d alpha = {sens:.0f}: a 1% change in alpha changes rho by a factor "
      f"{math.exp(4 * sens * 0.01 * al_need):.1f}")
C_needed = (1 / 24.5) / (math.sqrt(5) / 96 * al_need)
print(f"  C_geom needed = {C_needed:.3f}  (paper 15.1)")
check("formula alpha_eff=0.1160 misses rho_L by > factor 3",
      (MP * math.exp(-math.pi / (2 * aeff_formula * E_inf))) ** 4 / rho_L > 3)
check("negative control: E=ln2 (no -1/2) gives absurd rho",
      abs(math.log10((MP * math.exp(-math.pi / (2 * 0.115 * math.log(2)))) ** 4 / rho_L)) > 50)

# ---------------------------------------------------------------- 7. Higgs record
print("\n[7] Higgs record (book ch. 12 sec. 7; not a claim of this paper).")
lam0 = 1 / 8
mh0 = V * math.sqrt(2 * lam0)
dl = MH ** 2 / (2 * V ** 2) - lam0
print(f"  v/2 = {mh0:.2f} GeV; Delta lambda = {dl:.5f} gives m_H = {MH} (1 parameter, 1 observable)")
check("v/2 = 123.11", abs(mh0 - 123.11) < 0.01)

print("\nSUMMARY:", "all checks passed" if not FAIL else f"{len(FAIL)} FAILED: {FAIL}")
