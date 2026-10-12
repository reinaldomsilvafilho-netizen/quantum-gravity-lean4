r"""l1_ch13_rounding.py -- independent check of rounded bounds in book ch. 13 (and ch. 12 sec:experimental).

Claims checked (chap13_experimental_observational_signatures_quantum_gravity.tex, l. 61, 94, 101;
chap12_grand_unification_quantum_gravity_treatise.tex, l. 620, 627):

 (a) r < 0.036, A_s ~ 2.1e-9 and 2 H^2 / (pi^2 M_red^2) = r A_s, M_red = M_P / sqrt(8 pi)
     "give the bound H_inf <= 4.7e13 GeV".
 (c) |alpha_t| ~ (H_inf/M_P)^2 <= 1.5e-11 and (H_inf/M_red)^2 <= 3.7e-10  (same text, l. 101 / 627).
 (b) hbar c / l_* > 4.1e14 GeV  (Satunin 2019, photon splitting) "i.e. l_* < 4.8e-31 m".
 (d) window M_* >= 4.1e14 GeV: |alpha_t| = x/(1+x), x = (H/M_*)^2, "at most of order 1e-2".

Each claim is a supremum: H_sup = sup{H : r < 0.036} (not attained), l_sup = hbar c / 4.1e14 GeV.
An upper bound quoted in the text is valid iff  quoted >= sup.

Oracle (independent of the Lean file and of the book's closed form):
  * M_P from CODATA G, hbar, c, e (scipy.constants), converted to GeV -- not the literal 1.22089e19;
  * H_sup by root finding (mpmath.findroot) on the defining relation, not by the closed form;
  * an interval (mpmath.iv) enclosure of H_sup and l_sup so the comparison with the quoted value
    is certified, not a float accident.
Negative control: a mutated relation that forgets the reduced Planck mass (uses M_P instead of
M_red) must FAIL to reproduce the oracle value of H_sup.
Sensitivity: Planck 2018 central A_s = exp(3.044)/1e10 instead of the rounded 2.1e-9.

Run from the project folder:  python unified_quantum_gravity_book/audit/verify/scripts/l1_ch13_rounding.py
Exit code != 0 iff a non-control check fails or the control passes.
"""
import sys
import math

import mpmath as mp
from scipy import constants as C

mp.mp.dps = 40
failures = []


def check(name, ok, detail, control=False):
    ok = bool(ok)
    tag = "PASS" if ok else "FAIL"
    if control:
        tag = "CONTROL-FAILS (good)" if not ok else "CONTROL-PASSES (BAD)"
        if ok:
            failures.append(name)
    elif not ok:
        failures.append(name)
    print(f"[{tag}] {name}: {detail}")


def finding(name, quoted, sup, kind):
    """kind='upper': the quoted number is an upper bound, valid iff quoted >= sup."""
    valid = quoted >= sup
    print(f"[FINDING] {name}: quoted {quoted:.4g}, exact sup {sup:.6g} -> "
          f"{'valid as an upper bound' if valid else 'NOT a valid upper bound (rounded the wrong way)'}")
    return valid


def round_up(x, sig):
    e = math.floor(math.log10(x))
    f = 10 ** (e - sig + 1)
    return math.ceil(x / f - 1e-12) * f


# ---------------------------------------------------------------- constants (CODATA via scipy)
hbar, c, G, e = (mp.mpf(C.hbar), mp.mpf(C.c), mp.mpf(C.G), mp.mpf(C.e))
GeV = e * mp.mpf(10) ** 9                        # J
M_P_GeV = mp.sqrt(hbar * c / G) * c ** 2 / GeV     # Planck energy, GeV
hbar_c_GeV_m = hbar * c / GeV                      # GeV m
import scipy
print(f"scipy {scipy.__version__} (CODATA constants); "
      f"M_P c^2 = {mp.nstr(M_P_GeV, 8)} GeV, hbar c = {mp.nstr(hbar_c_GeV_m, 10)} GeV m")

# order-of-magnitude / dimension sanity (CODATA 2018: 1.220890e19 GeV, 1.973269804e-16 GeV m)
check("M_P order of magnitude", abs(M_P_GeV / mp.mpf("1.22089e19") - 1) < 1e-4,
      f"{mp.nstr(M_P_GeV, 7)} GeV vs CODATA 1.22089e19")
check("hbar c value", abs(hbar_c_GeV_m / mp.mpf("1.973269804e-16") - 1) < 1e-8,
      f"{mp.nstr(hbar_c_GeV_m, 10)} GeV m")

r_max = mp.mpf("0.036")
A_s = mp.mpf("2.1e-9")


def H_sup_root(Mp, As, r, reduced=True):
    """Solve 2 H^2/(pi^2 M^2) = r As for H > 0 by Newton iteration (dimensionless relation)."""
    M = Mp / mp.sqrt(8 * mp.pi) if reduced else Mp
    f = lambda H: 2 * H ** 2 / (mp.pi ** 2 * M ** 2) - r * As
    return mp.findroot(f, mp.mpf("1e13"))


# ---------------------------------------------------------------- (a) H_inf
H_sup = H_sup_root(M_P_GeV, A_s, r_max)
H_closed_lean = math.sqrt(0.036 * 2.1e-9 * math.pi / 16) * 1.22089e19   # book/Lean closed form
check("(a) oracle root vs closed form 16H^2=pi r As M_P^2", abs(H_sup / H_closed_lean - 1) < 1e-5,
      f"root {mp.nstr(H_sup, 7)} GeV, closed {H_closed_lean:.7g} GeV")
# certified enclosure with interval arithmetic (M_P taken as the CODATA interval 1.220890(14)e19)
iv = mp.iv
iv.dps = 30
Mp_iv = iv.mpf(["1.220876e19", "1.220904e19"])
H_iv = iv.sqrt(iv.mpf("0.036") * iv.mpf("2.1e-9") * iv.pi / 16) * Mp_iv
print(f"    certified enclosure of H_sup (CODATA 1-sigma on M_P): [{mp.nstr(H_iv.a, 8)}, {mp.nstr(H_iv.b, 8)}] GeV")
check("(a) H_sup > 4.70e13 certified", H_iv.a > mp.mpf("4.70e13"), f"lower end {mp.nstr(H_iv.a, 8)}")
check("(a) H_sup < 4.71e13 certified", H_iv.b < mp.mpf("4.71e13"), f"upper end {mp.nstr(H_iv.b, 8)}")
okA = finding("(a) H_inf <= 4.7e13 GeV", 4.7e13, float(H_sup), "upper")
print(f"    safe 2-sig-fig upper bound: {round_up(float(H_sup), 2):.2g}; 3 sig figs: {round_up(float(H_sup), 3):.3g}")
# values with r < 0.036 actually exceed 4.7e13: r needed for H = 4.702e13
r_at = 16 * mp.mpf("4.702e13") ** 2 / (mp.pi * M_P_GeV ** 2 * A_s)
check("(a) H = 4.702e13 GeV is reached with r < 0.036", r_at < r_max, f"r = {mp.nstr(r_at, 6)}")
# sensitivity: Planck 2018 central A_s
A_s_pl = mp.e ** mp.mpf("3.044") / mp.mpf(10) ** 10
H_sup_pl = H_sup_root(M_P_GeV, A_s_pl, r_max)
print(f"    sensitivity: A_s = {mp.nstr(A_s_pl, 5)} (Planck 2018 central) -> H_sup = {mp.nstr(H_sup_pl, 6)} GeV "
      f"({'still > 4.7e13' if H_sup_pl > mp.mpf('4.7e13') else '<= 4.7e13'})")

# negative control: forgetting the reduced Planck mass must not reproduce the oracle
H_mut = H_sup_root(M_P_GeV, A_s, r_max, reduced=False)
check("control: relation with M_P instead of M_red", abs(H_mut / H_sup - 1) < 1e-3,
      f"mutant {mp.nstr(H_mut, 6)} GeV vs oracle {mp.nstr(H_sup, 6)}", control=True)

# ---------------------------------------------------------------- (c) alpha_t
x_P = (H_sup / M_P_GeV) ** 2
x_red = (H_sup / (M_P_GeV / mp.sqrt(8 * mp.pi))) ** 2
a_P, a_red = x_P / (1 + x_P), x_red / (1 + x_red)
check("(c) |alpha_t| = x/(1+x) ~ x (relative gap < 1e-9)", abs(a_P / x_P - 1) < 1e-9, f"x = {mp.nstr(x_P, 6)}")
okC1 = finding("(c1) |alpha_t| <= 1.5e-11 (M_* = M_P)", 1.5e-11, float(a_P), "upper")
okC2 = finding("(c2) |alpha_t| <= 3.7e-10 (M_* = M_red)", 3.7e-10, float(a_red), "upper")
print(f"    safe 2-sig-fig upper bound for (c2): {round_up(float(a_red), 2):.2g}; 3 sig figs: {round_up(float(a_red), 3):.3g}")
x_red_at = (mp.mpf("4.702e13") / (M_P_GeV / mp.sqrt(8 * mp.pi))) ** 2
check("(c2) reachable value with r < 0.036 exceeds 3.7e-10", x_red_at / (1 + x_red_at) > mp.mpf("3.7e-10"),
      f"|alpha_t|(H = 4.702e13) = {mp.nstr(x_red_at / (1 + x_red_at), 6)}")

# ---------------------------------------------------------------- (d) window
x_w = (H_sup / mp.mpf("4.1e14")) ** 2
check("(d) window M_* >= 4.1e14: |alpha_t| < 0.014 ('order 1e-2')", x_w / (1 + x_w) < mp.mpf("0.014"),
      f"{mp.nstr(x_w / (1 + x_w), 5)}")

# ---------------------------------------------------------------- (b) photon bound
E_LV = mp.mpf("4.1e14")   # GeV, Satunin 2019 abstract, photon splitting, superluminal
l_sup = hbar_c_GeV_m / E_LV
l_iv = iv.mpf(["1.9732698039e-16", "1.9732698041e-16"]) / iv.mpf("4.1e14")
print(f"    l_sup = hbar c / 4.1e14 GeV = {mp.nstr(l_sup, 8)} m, enclosure [{mp.nstr(l_iv.a, 8)}, {mp.nstr(l_iv.b, 8)}]")
check("(b) dimension: GeV m / GeV = m and l_sup ~ 1e-31 m", 1e-32 < l_sup < 1e-30, f"{mp.nstr(l_sup, 5)} m")
check("(b) l_sup > 4.81e-31 certified", l_iv.a > mp.mpf("4.81e-31"), f"lower end {mp.nstr(l_iv.a, 8)}")
okB = finding("(b) l_* < 4.8e-31 m", 4.8e-31, float(l_sup), "upper")
print(f"    safe upper bound: 2 sig figs {round_up(float(l_sup), 2):.2g} m; 3 sig figs {round_up(float(l_sup), 3):.3g} m")
# oracle 2: via Planck units, l_sup = l_P * (E_P / E_LV)
l_P = mp.sqrt(hbar * G / c ** 3)
check("(b) oracle via l_P * E_P / E_LV", abs(l_P * M_P_GeV / E_LV / l_sup - 1) < 1e-12,
      f"{mp.nstr(l_P * M_P_GeV / E_LV, 8)} m")
check("control: hbar c taken in eV m (factor 1e9 error) reproduces l_sup",
      abs(hbar * c / e / E_LV / l_sup - 1) < 1e-3, f"{mp.nstr(hbar * c / e / E_LV, 4)} m", control=True)

print()
print("Summary of findings (quoted upper bound valid?):",
      {"a H<=4.7e13": okA, "c1 1.5e-11": okC1, "c2 3.7e-10": okC2, "b l<4.8e-31": okB})
if failures:
    print("CHECK FAILURES:", failures)
    sys.exit(1)
print("All checks and controls behaved as expected.")
