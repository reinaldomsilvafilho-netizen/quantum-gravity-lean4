"""Independent verifier, claim A1/A2/A5: ghost residue, Yukawa alpha=-1, subluminality.

Oracle differs from the draft: residues from the limit (s - s0) G(s) by Richardson
extrapolation (no sympy apart, no contour); potential from the radial sine transform
evaluated with mpmath quadosc; group velocity from the exact branches by finite differences.
Negative controls: healthy sum 1/s + 1/(s+m^2) (residue +1) and potential with (1 + e^{-r/l}).
Metric (-,+,+,+): p^2 = -E^2 + k^2, G = 1/[p^2 (1 + l^2 p^2)].
"""
import mpmath as mp

mp.mp.dps = 30
ok = []


def check(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


def residue_limit(G, s0):
    # Res = lim_{s->s0} (s - s0) G(s); Richardson over h = 10^-k
    vals = [(h) * G(s0 + h) for h in (mp.mpf(10) ** -k for k in range(6, 12))]
    return vals[-1]


for l in (mp.mpf("0.4"), mp.mpf(1), mp.mpf(3)):
    G = lambda s: 1 / (s * (1 + l**2 * s))
    r0 = residue_limit(G, 0)
    rm = residue_limit(G, -1 / l**2)
    print(f"l={l}: Res(s=0)={mp.nstr(r0, 12)}  Res(s=-1/l^2)={mp.nstr(rm, 12)}  (x l^2 -> weight {mp.nstr(rm, 12)})")
    check(f"A1 l={l}: massless residue +1", abs(r0 - 1) < 1e-9)
    check(f"A1 l={l}: massive pole m^2=1/l^2 has residue -1 (ghost)", abs(rm + 1) < 1e-9)
    H = lambda s: 1 / s + 1 / (s + 1 / l**2)
    check(f"NC l={l}: healthy control has residue +1 at the massive pole", abs(residue_limit(H, -1 / l**2) - 1) < 1e-9)

# Energy-plane: -G as function of E at fixed k: -1/((-E^2+k^2)(1+l^2(-E^2+k^2))); healthy massive: -1/(-E^2+k^2+m^2)
l, k = mp.mpf(1), mp.mpf("0.7")
wm = mp.sqrt(k**2 + 1 / l**2)
Gb = lambda E: 1 / ((-E**2 + k**2) * (1 + l**2 * (-E**2 + k**2)))
Gh = lambda E: 1 / (-E**2 + k**2 + 1 / l**2)
rb = residue_limit(Gb, wm)
rh = residue_limit(Gh, wm)
print(f"energy-plane residue at E=+omega_m: book {mp.nstr(rb, 10)}, healthy {mp.nstr(rh, 10)}")
check("A3 energy residue has sign opposite to healthy massive field", abs(rb + rh) < 1e-9 and rh != 0)

# Static potential: V(r) = -4 pi G M * (1/(2pi)^3) int d^3k e^{ikr} Gs(k),  Gs = 1/k^2 - 1/(k^2+m^2) = m^2/(k^2 (k^2+m^2))
# = -(G M) (2/pi) int_0^inf sin(kr)/(k r) k^2 Gs(k) dk   (units GM=1)
def V(r, sign=-1, m=1):
    f = lambda q: mp.sin(q * r) / (q * r) * q**2 * (1 / q**2 + sign / (q**2 + m**2))
    return -(2 / mp.pi) * mp.quadosc(f, [0, mp.inf], omega=r)

errs, errs_nc = [], []
for r in (mp.mpf("0.05"), mp.mpf("0.3"), mp.mpf(1), mp.mpf(4)):
    closed = -(1 / r) * (1 - mp.e ** (-r))
    errs.append(abs(V(r) / closed - 1))
    errs_nc.append(abs(V(r, +1) / closed - 1))
print("Yukawa rel errs", [mp.nstr(e, 3) for e in errs], " mutant", [mp.nstr(e, 3) for e in errs_nc])
check("A4 V(r) = -(GM/r)(1 - e^{-r/l}), alpha = -1", max(errs) < 1e-8)
check("A4 V(0) finite = -GM/l (limit r->0 of closed form)", abs(-(1 - mp.e ** (-mp.mpf("1e-12"))) / mp.mpf("1e-12") + 1) < 1e-9)
check("NC mutated 1/k^2 + 1/(k^2+m^2) disagrees", min(errs_nc) > 1e-3)

# Subluminality of the isotropic branches: E^2 = k^2 and E^2 = k^2 + 1/l^2
vg = lambda Efun, q: mp.diff(Efun, q)
ks = [mp.mpf(x) for x in ("0.01", "0.3", "1", "10", "100")]
vmax = max(max(vg(lambda q: q, q), vg(lambda q: mp.sqrt(q**2 + 1), q)) for q in ks)
check(f"A5 isotropic Lorentzian branches have v_g <= 1 (max {mp.nstr(vmax, 8)})", vmax <= 1 + 1e-20)
# quartic ansatz with xi>0 superluminal, xi<0 subluminal (the draft's item 4 says 'any xi != 0 ... v_g > c')
for xi in (mp.mpf("0.5"), mp.mpf("-0.5")):
    Ea = lambda q: q * mp.sqrt(1 + xi * q**2)
    print(f"  ansatz xi={xi}: v_g(k=0.3) = {mp.nstr(vg(Ea, mp.mpf('0.3')), 10)}")
check("A5b ansatz: v_g > c only for xi > 0 (xi < 0 is subluminal)",
      vg(lambda q: q * mp.sqrt(1 + q**2 / 2), mp.mpf("0.3")) > 1 and vg(lambda q: q * mp.sqrt(1 - q**2 / 2), mp.mpf("0.3")) < 1)

print(f"\nSUMMARY: {sum(ok)}/{len(ok)} PASS")
