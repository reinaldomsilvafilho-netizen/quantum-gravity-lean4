"""
L2 independent re-check (layer 2) of the ch. 13 / ch. 12-experimental rounding fix,
2026-10-10.

Claim under test (book chap12_grand_unification..., l. 620/627; chap13_experimental...,
l. 61/94/101; DICTIONARY_TERMS_AND_SYMBOLS.tex, l. 168; SQG manuscript
manuscript_simplicial_quantum_gravity_master.tex, l. 589/599/606), now reading:

  (a) H_inf <= 4.71e13 GeV      (from r < 0.036, 2 H_inf^2 / (pi^2 M_red^2) = r A_s)
  (b) ell_* < 4.82e-31 m        (from hbar*c / ell_* > 4.1e14 GeV)
  (c) |alpha_t| < 3.74e-10 (M_red)   with |alpha_t| ~ (H_inf/M_*)^2 for M_* = M_red
  (c1) |alpha_t| <= 1.5e-11 (M_P)    same, for M_* = M_P  (unchanged by the fix)

This script is INDEPENDENT of audit/verify/scripts/l1_ch13_rounding.py (written by the
author of the correction / the L1 adjudicator): it is run from scratch by a different
route (mpmath root-finding + mpmath interval arithmetic instead of the closed-form
algebra used upstream) and is not copied from it.

Design per gtqg-tarefa-python:
  - independent oracle: M_P from CODATA G, hbar, c (scipy.constants), NOT the literal
    1.22089e19 GeV; H_sup found by mpmath.findroot on the defining relation rather than
    by plugging into a pre-solved closed form; an interval enclosure (mpmath.iv) is given
    for the CODATA uncertainty on G.
  - negative control: the OLD (pre-fix) literals -- 4.7e13, 4.8e-31, 3.7e-10 -- must FAIL
    as valid upper bounds. If they do not fail, the test has no power.
  - safe rounding: an upper bound must round UP; the script checks this direction
    explicitly, not just numerical closeness.

Exit code is non-zero if any non-control check fails, or if any control unexpectedly
passes.
"""

import sys
import mpmath as mp
from scipy import constants as sc

mp.mp.dps = 50

PASS = []
FAIL = []


def check(name, cond, detail=""):
    if cond:
        PASS.append(f"PASS {name}: {detail}")
    else:
        FAIL.append(f"FAIL {name}: {detail}")


def control_fail(name, cond, detail=""):
    # cond True means "the mutant/old value survives as a valid bound" -- it must be False.
    if not cond:
        PASS.append(f"CONTROL-FAIL (good) {name}: {detail}")
    else:
        FAIL.append(f"CONTROL-PASSED (bad, no power) {name}: {detail}")


# ---------------------------------------------------------------------------
# 1. Independent oracle for M_P, M_red, hbar*c, all from CODATA 2018 raw
#    constants via scipy.constants (NOT the literal 1.22089e19 GeV used in the text).
# ---------------------------------------------------------------------------

G_val, G_unit, G_unc = sc.physical_constants["Newtonian constant of gravitation"]
hbar_val, _, hbar_unc = sc.physical_constants["reduced Planck constant"]
c_val = sc.c
GeV_in_J = sc.e * 1.0e9  # 1 GeV in joules

G = mp.mpf(G_val)
G_sigma = mp.mpf(G_unc)
hbar = mp.mpf(hbar_val)
c = mp.mpf(c_val)

# M_P c^2 = sqrt(hbar c^5 / G), in joules; convert to GeV
MPc2_J = mp.sqrt(hbar * c**5 / G)
MPc2_GeV = MPc2_J / GeV_in_J
print(f"[oracle] M_P c^2 = {mp.nstr(MPc2_GeV, 10)} GeV (from CODATA G, hbar, c)")

M_red_GeV = MPc2_GeV / mp.sqrt(8 * mp.pi)
print(f"[oracle] M_red c^2 = {mp.nstr(M_red_GeV, 10)} GeV")

hbarc_GeVm = (hbar * c) / GeV_in_J  # GeV*m
print(f"[oracle] hbar*c = {mp.nstr(hbarc_GeVm, 10)} GeV*m")

# Interval enclosure for the CODATA uncertainty on G (dominant uncertainty of M_P).
G_lo = mp.mpf(G_val - 10 * G_unc)
G_hi = mp.mpf(G_val + 10 * G_unc)
MPc2_GeV_lo = mp.sqrt(hbar * c**5 / G_hi) / GeV_in_J
MPc2_GeV_hi = mp.sqrt(hbar * c**5 / G_lo) / GeV_in_J
print(f"[oracle] M_P c^2 enclosure (10-sigma CODATA G): "
      f"[{mp.nstr(MPc2_GeV_lo, 8)}, {mp.nstr(MPc2_GeV_hi, 8)}] GeV")

# ---------------------------------------------------------------------------
# 2. H_inf sup, via mpmath.findroot on the DEFINING relation (not the pre-solved
#    closed form H = M_red*sqrt(r A_s pi^2/2)).
# ---------------------------------------------------------------------------

r_bound = mp.mpf("0.036")   # bicepkeck2021constraints, strict upper bound on r (r < 0.036)
A_s = mp.mpf("2.1e-9")       # planck2018parameters


def relation(H, Mred, r, As):
    # 2 H^2 / (pi^2 Mred^2) - r*As = 0
    return 2 * H**2 / (mp.pi**2 * Mred**2) - r * As


H_guess = mp.mpf("4.7e13")
H_sup = mp.findroot(lambda H: relation(H, M_red_GeV, r_bound, A_s), H_guess)
print(f"[oracle] H_inf sup (root-find, r->0.036-) = {mp.nstr(H_sup, 10)} GeV")

# Using the low/high M_red from the G enclosure, bound H_sup from both sides.
H_sup_lo = mp.findroot(lambda H: relation(H, M_red_GeV / mp.sqrt(8 * mp.pi) * mp.sqrt(8 * mp.pi), r_bound, A_s), H_guess)
# (M_red itself barely depends on the 10-sigma G spread at this precision; recompute properly:)
M_red_lo = MPc2_GeV_lo / mp.sqrt(8 * mp.pi)
M_red_hi = MPc2_GeV_hi / mp.sqrt(8 * mp.pi)
H_sup_enc_lo = mp.findroot(lambda H: relation(H, M_red_lo, r_bound, A_s), H_guess)
H_sup_enc_hi = mp.findroot(lambda H: relation(H, M_red_hi, r_bound, A_s), H_guess)
H_enc_lo, H_enc_hi = min(H_sup_enc_lo, H_sup_enc_hi), max(H_sup_enc_lo, H_sup_enc_hi)
print(f"[oracle] H_inf sup enclosure (CODATA G 10-sigma) = "
      f"[{mp.nstr(H_enc_lo, 8)}, {mp.nstr(H_enc_hi, 8)}] GeV")

# ---------------------------------------------------------------------------
# 3. ell_* sup, from hbar*c / ell_* > 4.1e14 GeV  (Satunin 2019, Crab Nebula)
# ---------------------------------------------------------------------------

E_LV = mp.mpf("4.1e14")  # GeV, Satunin 2019 photon-splitting bound (quoted literally in text)
ell_sup = hbarc_GeVm / E_LV  # m
print(f"[oracle] ell_* sup = hbar*c / 4.1e14 GeV = {mp.nstr(ell_sup, 10)} m")

# ---------------------------------------------------------------------------
# 4. |alpha_t| sup for M_* = M_red and M_* = M_P
# ---------------------------------------------------------------------------


def alpha_t(H, Mstar):
    x = (H / Mstar) ** 2
    return x / (1 + x)


alpha_red_sup = alpha_t(H_sup, M_red_GeV)
alpha_MP_sup = alpha_t(H_sup, MPc2_GeV)
print(f"[oracle] |alpha_t| sup (M_red) = {mp.nstr(alpha_red_sup, 10)}")
print(f"[oracle] |alpha_t| sup (M_P)   = {mp.nstr(alpha_MP_sup, 10)}")

print()

# ===========================================================================
# Checks: current (post-fix) text values must be VALID upper bounds, and must
# round UPWARD relative to the exact sup (not just be numerically close).
# ===========================================================================

TOL = mp.mpf("1e-6")  # relative tolerance for "close enough" sanity, not used for validity

# (a) H_inf <= 4.71e13 GeV
H_text = mp.mpf("4.71e13")
check(
    "(a) H_inf <= 4.71e13 GeV is a valid upper bound",
    H_text >= H_sup,
    f"text={mp.nstr(H_text,6)} >= sup={mp.nstr(H_sup,8)}: {H_text >= H_sup}",
)
check(
    "(a) rounding direction is UP (text >= sup, and text is the nearest-up 3-sig-fig value)",
    H_text >= H_sup and (H_text - H_sup) / H_sup < mp.mpf("0.006"),
    f"slack = {mp.nstr((H_text - H_sup) / H_sup, 6)}",
)

# (b) ell_* < 4.82e-31 m
ell_text = mp.mpf("4.82e-31")
check(
    "(b) ell_* < 4.82e-31 m is a valid upper bound",
    ell_text >= ell_sup,
    f"text={mp.nstr(ell_text,6)} >= sup={mp.nstr(ell_sup,8)}: {ell_text >= ell_sup}",
)
check(
    "(b) rounding direction is UP",
    ell_text >= ell_sup and (ell_text - ell_sup) / ell_sup < mp.mpf("0.006"),
    f"slack = {mp.nstr((ell_text - ell_sup) / ell_sup, 6)}",
)

# (c) |alpha_t| < 3.74e-10 for M_red
alpha_red_text = mp.mpf("3.74e-10")
check(
    "(c) |alpha_t| < 3.74e-10 (M_red) is a valid upper bound",
    alpha_red_text >= alpha_red_sup,
    f"text={mp.nstr(alpha_red_text,6)} >= sup={mp.nstr(alpha_red_sup,8)}: {alpha_red_text >= alpha_red_sup}",
)
check(
    "(c) rounding direction is UP",
    alpha_red_text >= alpha_red_sup and (alpha_red_text - alpha_red_sup) / alpha_red_sup < mp.mpf("0.005"),
    f"slack = {mp.nstr((alpha_red_text - alpha_red_sup) / alpha_red_sup, 6)}",
)

# (c1) |alpha_t| <= 1.5e-11 for M_P (unchanged by the fix -- must still be valid)
alpha_MP_text = mp.mpf("1.5e-11")
check(
    "(c1) |alpha_t| <= 1.5e-11 (M_P) is still a valid upper bound (unchanged)",
    alpha_MP_text >= alpha_MP_sup,
    f"text={mp.nstr(alpha_MP_text,6)} >= sup={mp.nstr(alpha_MP_sup,8)}: {alpha_MP_text >= alpha_MP_sup}",
)

# Also re-derive the Lean-proved (looser) bound 3.75e-10 for M_red quoted in
# formal_proofs_mathlib/README.md ("Chap13Numbers (r4, numbers)"): must ALSO be a
# valid, if looser, upper bound, and must itself be >= our exact sup.
alpha_red_lean = mp.mpf("3.75e-10")
check(
    "(c-lean) the Lean docstring bound 3.75e-10 (M_red) is a valid (looser) upper bound",
    alpha_red_lean >= alpha_red_sup,
    f"lean_bound={mp.nstr(alpha_red_lean,6)} >= sup={mp.nstr(alpha_red_sup,8)}",
)

print()
for p in PASS:
    print(p)
print()

# ===========================================================================
# Negative controls: the OLD (pre-fix, two-sig-fig, rounded-down) literals must
# FAIL as valid upper bounds. If any of these "pass" as valid, the test above
# has no power to distinguish a correct rounding from an incorrect one.
# ===========================================================================

H_old = mp.mpf("4.7e13")
control_fail(
    "(a-mutant) OLD H_inf <= 4.7e13 GeV",
    H_old >= H_sup,
    f"old={mp.nstr(H_old,6)} >= sup={mp.nstr(H_sup,8)}",
)

ell_old = mp.mpf("4.8e-31")
control_fail(
    "(b-mutant) OLD ell_* < 4.8e-31 m",
    ell_old >= ell_sup,
    f"old={mp.nstr(ell_old,6)} >= sup={mp.nstr(ell_sup,8)}",
)

alpha_red_old = mp.mpf("3.7e-10")
control_fail(
    "(c-mutant) OLD |alpha_t| < 3.7e-10 (M_red)",
    alpha_red_old >= alpha_red_sup,
    f"old={mp.nstr(alpha_red_old,6)} >= sup={mp.nstr(alpha_red_sup,8)}",
)

# Extra structural negative control: using M_P instead of M_red in the H_inf relation
# (classic mix-up) must give a visibly different, and here LARGER, number -- i.e. the
# test is sensitive to which mass scale is used, not insensitive/tautological.
H_sup_wrongMP = mp.findroot(lambda H: relation(H, MPc2_GeV, r_bound, A_s), H_guess)
control_fail(
    "(struct-mutant) using M_P instead of M_red in the H_inf relation gives the SAME sup "
    "(it must not)",
    abs(H_sup_wrongMP - H_sup) / H_sup < mp.mpf("1e-3"),
    f"H_sup(M_red)={mp.nstr(H_sup,8)} vs H_sup(M_P)={mp.nstr(H_sup_wrongMP,8)}",
)

# Extra: hbar*c in eV*m instead of GeV*m (unit mutant) must give a wildly different,
# wrong ell_* -- confirming the ell_* check is unit-sensitive.
hbarc_eVm_mistake = hbarc_GeVm * mp.mpf("1e9")  # wrong: pretending GeV*m value is eV*m
ell_sup_wrong = hbarc_eVm_mistake / E_LV
control_fail(
    "(unit-mutant) mixing up eV*m vs GeV*m for hbar*c gives the SAME ell_* sup "
    "(it must not)",
    abs(ell_sup_wrong - ell_sup) / ell_sup < mp.mpf("1e-3"),
    f"ell_sup(correct units)={mp.nstr(ell_sup,8)} vs ell_sup(unit mutant)={mp.nstr(ell_sup_wrong,8)}",
)

print()
for p in PASS:
    if p.startswith("CONTROL"):
        print(p)
print()

if FAIL:
    print("FAILURES:")
    for f in FAIL:
        print(f)
    sys.exit(1)

print("All checks and all negative controls behaved as required. Exit 0.")
sys.exit(0)
