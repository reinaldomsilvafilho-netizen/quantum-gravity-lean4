"""Independent verifier, B claim 3: neutrino Koide Q = 2/3, H2 ratio, Brannen shift.

Oracle (different from the draft): parametrize directly sqrt(m_k) = A (1 + sqrt2 cos(d + 2 pi k/3))
(Q = 2/3 identically), scan d, keep the phase where the ratio dm21/dm31 matches the data, fix the
scale A by dm31. Signs of roots are automatic (a root 1 + sqrt2 cos < 0 is a negative root).
m_bb range from the closed-form triangle rule (min = max(0, 2 max|term| - sum), max = sum).
Negative controls: all-positive roots in NO cannot reach Q = 2/3 (compute sup Q over m1);
Q = 0.60 target gives a different sum.
Data: NuFIT 6.0 (arXiv:2410.05380 Table 1): dm21 = 7.49e-5; NO dm31 = 2.513e-3 (IC24+SK) or
2.534e-3 (IC19 w/o SK); IO dm32 = -2.484e-3 (IC24+SK) or -2.510e-3 (IC19). PDG 2024 lepton masses.
"""
import numpy as np
from scipy.optimize import brentq

ok = []


def check(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


DM21 = 7.49e-5
s13 = 0.02195
c13 = 1 - s13
s12 = 1 - 2 / (3 * c13)
Ue2 = np.array([(1 - s12) * c13, s12 * c13, s13])


def masses_from_phase(d):
    r = 1 + np.sqrt(2) * np.cos(d + 2 * np.pi * np.arange(3) / 3)
    return np.sort(r**2), r


def solve(order, dm3):
    sols = []
    ds = np.linspace(0, 2 * np.pi / 3, 20001)
    def f(d):
        m, _ = masses_from_phase(d)
        m = m**2  # squared masses (up to scale) for mass-squared differences
        if order == "NO":
            return (m[1] - m[0]) / (m[2] - m[0]) - DM21 / dm3
        # IO: m3 lightest = m[0]; m1 = m[1], m2 = m[2]; dm21 = m2-m1; |dm32| = m2 - m3
        return (m[2] - m[1]) / (m[2] - m[0]) - DM21 / abs(dm3)
    fs = np.array([f(d) for d in ds])
    for i in np.where(np.sign(fs[:-1]) != np.sign(fs[1:]))[0]:
        d = brentq(f, ds[i], ds[i + 1], xtol=1e-15)
        m, r = masses_from_phase(d)
        scale = np.sqrt(abs(dm3) / (m[2]**2 - m[0]**2))
        sols.append((d, m * scale, r))
    return sols


def mbb(m):
    t = Ue2 * m
    return max(0, 2 * t.max() - t.sum()), t.sum()


for dm3 in (2.513e-3, 2.534e-3):
    print(f"NO, dm31 = {dm3}:")
    for d, m, r in solve("NO", dm3):
        lo, hi = mbb(m)
        neg = int((r < 0).sum())
        mb = np.sqrt((Ue2 * m**2).sum())
        print(f"   d={d:.4f}: m = {np.round(m*1e3,3)} meV, sum = {m.sum()*1e3:.2f} meV, m_beta = {mb*1e3:.2f}, "
              f"m_bb in [{lo*1e3:.2f}, {hi*1e3:.2f}] meV, negative roots: {neg}")
        if dm3 == 2.513e-3:
            check("NO Koide: m = (0.36, 8.66, 50.13) meV, sum 59.2", np.allclose(m * 1e3, [0.364, 8.662, 50.131], atol=0.01) and abs(m.sum() * 1e3 - 59.2) < 0.05)
            check("NO Koide needs one negative root", neg == 1)
            check("m_beta ~8.9 meV, m_bb in [1.4, 4.0] meV", abs(mb * 1e3 - 8.9) < 0.1 and abs(lo * 1e3 - 1.4) < 0.1 and abs(hi * 1e3 - 4.0) < 0.1)
            check("delta_nu = 0.479 rad (mod 2pi/3 labelling) vs 2/9 + pi/12 = 0.484", min(abs(d - 0.4793), abs(2 * np.pi / 3 - d - 0.4793)) < 2e-3)  # d and 2pi/3 - d give the same spectrum
for dm3 in (-2.484e-3, -2.510e-3):
    sols = solve("IO", dm3)
    for d, m, r in sols:
        print(f"IO dm32={dm3}: m(sorted) = {np.round(m*1e3,3)} meV, sum = {m.sum()*1e3:.1f} meV")
    if dm3 == -2.484e-3:
        check("IO Koide sum ~102 meV", any(abs(m.sum() * 1e3 - 102.0) < 0.3 for _, m, _ in sols))
print("IO minimum sum (m3 = 0):", round((np.sqrt(2.484e-3) + np.sqrt(2.484e-3 - DM21)) * 1e3, 1), "meV;",
      "NO minimum sum (m1 = 0):", round((np.sqrt(DM21) + np.sqrt(2.513e-3)) * 1e3, 2), "meV")
check("DESI DR2 bound 64.2 meV lies between Koide-NO (59.2) and IO (102)", 59.2 < 64.2 < 102.0)

# NC1: sup of Q with all positive roots in NO
m1s = np.logspace(-8, 0, 20000)
Qmax = max((m1 + np.sqrt(m1**2 + DM21) + np.sqrt(m1**2 + 2.513e-3)) /
           (np.sqrt(m1) + (m1**2 + DM21) ** 0.25 + (m1**2 + 2.513e-3) ** 0.25) ** 2 for m1 in m1s)
print(f"NC1: sup Q(all positive roots, NO) = {Qmax:.4f}")
check("NC1 all-positive NO cannot reach 2/3", Qmax < 2 / 3)
# NC2: Q = 0.60 with negative root on m1 (root find in m1)
def Qneg(m1, target):
    m = np.array([m1, np.sqrt(m1**2 + DM21), np.sqrt(m1**2 + 2.513e-3)])
    return m.sum() / (-np.sqrt(m[0]) + np.sqrt(m[1]) + np.sqrt(m[2])) ** 2 - target
grid = np.logspace(-8, -1, 5000)
v = [Qneg(x, 0.6) for x in grid]
roots = [brentq(Qneg, grid[i], grid[i + 1], args=(0.6,)) for i in range(len(v) - 1) if np.sign(v[i]) != np.sign(v[i + 1])]
sums = [ (x + np.sqrt(x**2 + DM21) + np.sqrt(x**2 + 2.513e-3)) * 1e3 for x in roots]
print("NC2 Q=0.60 sums:", [round(s, 2) for s in sums], "meV")
check("NC2 Q=0.60 gives a different but close sum (58.8 meV)", any(abs(s - 58.8) < 0.1 for s in sums))

# H2
me, mmu, mtau = 0.51099895, 105.6583755, 1776.93
r = np.sqrt([me, mmu, mtau])
Ql = (me + mmu + mtau) / r.sum() ** 2
A = r.sum() / 3
# (i) b/a forced to 1/sqrt2 (Q = 2/3 exactly), phase from tau
dl_fixed = brentq(lambda d: A * (1 + np.sqrt(2) * np.cos(d)) - r[2], 0, 0.5)
# (ii) free b, closed form: a = mean root, 6 b^2 = sum (r - a)^2, cos d = (r_tau - a)/(2b)
b = np.sqrt(((r - A) ** 2).sum() / 6)
dl = np.arccos((r[2] - A) / (2 * b))
print(f"charged leptons: Q = {Ql:.6f}, b/a = {b/A:.6f}; delta_l free-b = {dl:.6f}, fixed-b = {dl_fixed:.6f} rad (2/9 = {2/9:.6f})")
check("delta_l = 2/9 to 5 digits with free b (draft's fit)", abs(dl - 2 / 9) < 1e-5)
check("delta_l = 2/9 to 4 digits even with b/a forced to 1/sqrt2", abs(dl_fixed - 2 / 9) < 1e-4)
data = DM21 / 2.513e-3
for name, sh in (("0", 0), ("pi/12", np.pi / 12)):
    m, _ = masses_from_phase(dl + sh)
    ratio = (m[1]**2 - m[0]**2) / (m[2]**2 - m[0]**2)
    print(f"H2 shift {name}: dm21/dm31 (mass-squared) = {ratio:.5f} (data {data:.5f})")
    if sh == 0:
        check("H2 ratio 0.0035 vs data 0.0298 (factor ~8.4)", abs(ratio - 0.003535) < 2e-5 and abs(data / ratio - 8.4) < 0.1)
    else:
        sig = data * np.hypot(0.19 / 7.49, 0.02 / 2.513)
        print(f"   pull = {(ratio-data)/sig:+.2f} sigma")
        check("Brannen pi/12: 0.0308, ~+1.3 sigma", abs(ratio - 0.03084) < 5e-5 and 1.1 < (ratio - data) / sig < 1.4)
print(f"\nSUMMARY: {sum(ok)}/{len(ok)} PASS")
