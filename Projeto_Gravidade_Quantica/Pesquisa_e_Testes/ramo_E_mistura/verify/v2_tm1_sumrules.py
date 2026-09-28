"""Independent verifier, B claim 2: TM1 sum rules, with an explicit PDG-convention extraction.

Construction (different from the draft): U = U_TBM . R23(theta, phi) (Albright-Rodejohann 2009,
eq. before (25)), random theta, phi. Angles from PDG: s13 = |Ue3|, s12^2 = |Ue2|^2/c13^2,
s23^2 = |Umu3|^2/c13^2; cos(delta) from |U_mu1|^2 (PDG: U_mu1 = -s12 c23 - c12 s23 s13 e^{i delta});
sin(delta) from the Jarlskog invariant J = Im(U_e1 U_mu2 U_e2* U_mu1*) = s12c12s23c23s13c13^2 sin(delta).
Checks: sin^2 t12 = 1 - 2/(3 c13^2); cos d = -cot(2 t23)(1 - 5 s13^2)/(2 sqrt2 s13 sqrt(1 - 3 s13^2)).
Also the rephasing-invariant consistency cos^2 + sin^2 = 1 of the extracted delta.
Negative control: TM2 matrices (U_TBM . R13) must violate both TM1 relations.
Then numbers at NuFIT 6.0 and JUNO 2025.
"""
import numpy as np

rng = np.random.default_rng(3)
ok = []


def check(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


s2, s3, s6 = np.sqrt(2), np.sqrt(3), np.sqrt(6)
UTBM = np.array([[2 / s6, 1 / s3, 0], [-1 / s6, 1 / s3, -1 / s2], [-1 / s6, 1 / s3, 1 / s2]])


def R23(t, p):
    return np.array([[1, 0, 0], [0, np.cos(t), np.sin(t) * np.exp(-1j * p)], [0, -np.sin(t) * np.exp(1j * p), np.cos(t)]])


def R13(t, p):
    return np.array([[np.cos(t), 0, np.sin(t) * np.exp(-1j * p)], [0, 1, 0], [-np.sin(t) * np.exp(1j * p), 0, np.cos(t)]])


def extract(U):
    A = np.abs(U) ** 2
    s13 = A[0, 2]
    c13 = 1 - s13
    s12, s23 = A[0, 1] / c13, A[1, 2] / c13
    c12, c23 = 1 - s12, 1 - s23
    root = np.sqrt(s12 * c12 * s23 * c23 * s13)
    cosd = (A[1, 0] - s12 * c23 - c12 * s23 * s13) / (2 * root)
    J = np.imag(U[0, 0] * U[1, 1] * np.conj(U[0, 1]) * np.conj(U[1, 0]))
    sind = J / (root * c13)
    return s12, s13, s23, cosd, sind


def tm1_cos(s13, s23):
    t23 = np.arcsin(np.sqrt(s23))
    return -(1 / np.tan(2 * t23)) * (1 - 5 * s13) / (2 * s2 * np.sqrt(s13) * np.sqrt(1 - 3 * s13))


e1 = e2 = e3 = 0
for _ in range(2000):
    t, p = rng.uniform(0.02, 0.3), rng.uniform(0, 2 * np.pi)
    s12, s13, s23, cd, sd = extract(UTBM @ R23(t, p))
    e1 = max(e1, abs(s12 - (1 - 2 / (3 * (1 - s13)))))
    e2 = max(e2, abs(cd - tm1_cos(s13, s23)))
    e3 = max(e3, abs(cd**2 + sd**2 - 1))
check(f"TM1 s12^2 sum rule (max err {e1:.1e})", e1 < 1e-12)
check(f"TM1 cos(delta) formula, PDG convention (max err {e2:.1e})", e2 < 1e-9)
check(f"extracted delta consistent: cos^2+sin^2=1 (max err {e3:.1e})", e3 < 1e-9)
bad1 = bad2 = 0
for _ in range(200):
    t, p = rng.uniform(0.05, 0.3), rng.uniform(0.3, 2 * np.pi - 0.3)
    s12, s13, s23, cd, sd = extract(UTBM @ R13(t, p))
    bad1 = max(bad1, abs(s12 - (1 - 2 / (3 * (1 - s13)))))
    bad2 = max(bad2, abs(cd - tm1_cos(s13, s23)))
check(f"NC TM2 violates TM1 relations (s12 dev {bad1:.2f}, cos dev {bad2:.2f})", bad1 > 1e-2 and bad2 > 1e-2)

s13 = 0.02195
tm1 = 1 - 2 / (3 * (1 - s13))
tm2 = 1 / (3 * (1 - s13))
print(f"TM1 s12^2 = {tm1:.4f}, TM2 s12^2 = {tm2:.4f}")
print(f"  vs NuFIT 6.0 (IC19 w/o SK) 0.307 +0.012: TM1 {(tm1-0.307)/0.012:+.2f} sigma, TM2 {(tm2-0.307)/0.012:+.2f} sigma")
print(f"  vs JUNO 2025 0.3092 +- 0.0087:         TM1 {(tm1-0.3092)/0.0087:+.2f} sigma, TM2 {(tm2-0.3092)/0.0087:+.2f} sigma")
s13b = 0.02215  # IC24 with SK
tm1b = 1 - 2 / (3 * (1 - s13b))
print(f"  (with s13^2 = 0.02215, IC24+SK: TM1 s12^2 = {tm1b:.4f}, {(tm1b-0.3092)/0.0087:+.2f} sigma vs JUNO)")
check("TM1 s12^2 = 0.318 (+0.9 sigma NuFIT)", abs(tm1 - 0.3184) < 5e-4 and 0.85 < (tm1 - 0.307) / 0.012 < 1.0)
for s23 in (0.561, 0.47):
    c = tm1_cos(s13, s23)
    d = np.degrees(np.arccos(c))
    print(f"s23^2={s23}: cos d = {c:+.3f}, delta = {d:.1f} or {360-d:.1f} deg")
check("delta ~74/286 deg at s23^2=0.561 and ~98/262 at 0.47",
      abs(np.degrees(np.arccos(tm1_cos(s13, 0.561))) - 74.3) < 0.5 and abs(np.degrees(np.arccos(tm1_cos(s13, 0.47))) - 97.6) < 0.5)
print(f"\nSUMMARY: {sum(ok)}/{len(ok)} PASS")
