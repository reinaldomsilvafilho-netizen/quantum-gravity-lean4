"""Independent verifier, claims C1 and d_s values (A item 3, 4) + counterexample to the uniqueness claim.

C1 oracle (different from the draft's 4D Hankel transform): the 1D marginal of a 4D density
has characteristic function phi(t) = exp(-tau(t^2 + l^2 t^4)); if the 4D kernel were >= 0 the
marginal would be >= 0. We compute the marginal f(x) = (1/pi) int_0^inf cos(tx) phi(t) dt with
mpmath quadosc and look for a negative value. Cross-check at one radius: 4D radial kernel via
K(r) = (1/(4 pi^2 r)) int k^2 J1(kr) e^{-tau F(k)} dk.
Negative controls: Gaussian (F = k^2) and Cauchy (F = |k|) marginals must be >= 0.

d_s: P(tau) from the book's erfc closed form vs direct quadrature; d_s = -2 dlnP/dln tau by
mpmath numerical differentiation of the closed form (not the moment identity used by the draft).

Counterexample (Tomboulis/Modesto-type entire form factor): kinetic symbol
S(k^2) = k^2 exp(Ein(l^4 k^4)/2), Ein(x) = gamma + ln x + E1(x) is entire, so exp(Ein/2) is entire
without zeros: the Lorentzian propagator 1/S has only the massless pole (no ghost), the operator is
Lorentz invariant (a function of p^2), and on the Euclidean axis S ~ e^{gamma/2} l^2 k^4 in the UV.
Check: d_s runs 4 -> 2.
"""
import mpmath as mp

mp.mp.dps = 25
ok = []


def check(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


def marginal(x, F, tau):
    return mp.quadosc(lambda t: mp.cos(t * x) * mp.e ** (-tau * F(t)), [0, mp.inf], omega=x) / mp.pi


def min_marginal(F, tau, xs):
    vals = [(x, marginal(x, F, tau)) for x in xs]
    x0, v0 = min(vals, key=lambda p: p[1])
    return x0, v0, max(v for _, v in vals)


xs = [mp.mpf(i) / 10 for i in range(1, 121)]
for tau in (mp.mpf("0.01"), mp.mpf(1), mp.mpf(10)):
    x0, v0, vmax = min_marginal(lambda t: t**2 + t**4, tau, [x * (1 + mp.sqrt(tau)) for x in xs])
    print(f"iso k^2+k^4 tau={tau}: min marginal {mp.nstr(v0, 5)} at x={mp.nstr(x0, 4)} (max {mp.nstr(vmax, 5)})")
    check(f"C1 tau={tau}: 1D marginal negative => 4D kernel not positive", v0 < -1e-8 * vmax)
x0, v0, vmax = min_marginal(lambda t: t**2 + t**6, mp.mpf("0.1"), [x * 2 for x in xs])
check(f"C1b Horava spatial k^2+k^6: marginal negative ({mp.nstr(v0/vmax, 4)})", v0 < 0)
for name, F in (("Gaussian", lambda t: t**2), ("Cauchy", lambda t: t)):
    x0, v0, vmax = min_marginal(F, mp.mpf(1), xs)
    check(f"NC {name} marginal has no negative value (min {mp.nstr(v0, 4)})", v0 > -1e-15)

# 4D radial cross-check at tau=0.01: draft says min K/max K = -1.9e-2 near r = 1.94
tau = mp.mpf("0.01")
K = lambda r: mp.quadosc(lambda k: k**2 * mp.besselj(1, k * r) * mp.e ** (-tau * (k**2 + k**4)), [0, mp.inf], omega=r) / (4 * mp.pi**2 * r)
K0 = mp.quad(lambda k: k**3 * mp.e ** (-tau * (k**2 + k**4)), [0, mp.inf]) / (8 * mp.pi**2)
ratio = K(mp.mpf("1.937")) / K0
print(f"4D kernel K(1.937)/K(0) at tau=0.01: {mp.nstr(ratio, 5)} (draft: -1.893e-2)")
check("C1c 4D kernel ratio reproduces draft value within 2%", abs(ratio / mp.mpf("-1.893e-2") - 1) < 0.02)

# d_s for the book symbol, l = 1
def P_closed(tau):
    z = mp.sqrt(tau) / 2
    return (1 - mp.sqrt(mp.pi) * z * mp.e ** (z**2) * mp.erfc(z)) / (32 * mp.pi**2 * tau)


def P_quad(tau, S=lambda k: k**2 + k**4):
    return mp.quad(lambda k: k**3 * mp.e ** (-tau * S(k)), [0, 1, 10, mp.inf]) / (8 * mp.pi**2)


def ds(P, tau):
    return -2 * tau * mp.diff(P, tau) / P(tau)


e = max(abs(P_closed(t) / P_quad(t) - 1) for t in (mp.mpf("1e-3"), mp.mpf("0.1"), mp.mpf(10), mp.mpf(1000)))
check(f"D0 book erfc closed form = quadrature (max rel err {mp.nstr(e, 3)})", e < 1e-12)
Pm = lambda tau: (1 - mp.sqrt(mp.pi) * (mp.sqrt(tau) / 2) * mp.erfc(mp.sqrt(tau) / 2)) / (32 * mp.pi**2 * tau)
check("NC mutated closed form (e^{z^2} dropped) disagrees", abs(Pm(mp.mpf(1)) / P_quad(mp.mpf(1)) - 1) > 1e-3)
uv, ir = ds(P_closed, mp.mpf("1e-8")), ds(P_closed, mp.mpf("1e8"))
print(f"book symbol: d_s(1e-8) = {mp.nstr(uv, 8)}, d_s(1e8) = {mp.nstr(ir, 8)}; IR slope check 4 - 12/tau at tau=1e4: {mp.nstr(ds(P_closed, mp.mpf(1e4)), 10)} vs {mp.nstr(4 - 12 / mp.mpf(1e4), 10)}")
check("D1 book symbol UV d_s -> 2", abs(uv - 2) < 1e-3)
check("D2 book symbol IR d_s -> 4", abs(ir - 4) < 1e-3)
check("D3 book IR approach 4 - 12 l^2/tau", abs(ds(P_closed, mp.mpf(1e4)) - (4 - 12 / mp.mpf(1e4))) < 1e-5)

# Horava z: P = (4 pi tau)^{-1/2} * (2pi)^{-3} 4 pi int k^2 e^{-tau F(k)} dk
def P_hl(tau, z):
    return (4 * mp.pi * tau) ** -0.5 * mp.quad(lambda k: k**2 * mp.e ** (-tau * (k**2 + k ** (2 * z))), [0, 1, 10, mp.inf]) / (2 * mp.pi**2)

for z in (2, 3):
    u = ds(lambda t: P_hl(t, z), mp.mpf("1e-10"))
    print(f"Horava z={z}: d_s(UV) = {mp.nstr(u, 6)} (1+3/z = {1 + 3 / z})")
    check(f"D4 Horava z={z}: UV d_s = 1 + 3/z", abs(u - (1 + mp.mpf(3) / z)) < 2e-3)
check("D5 Horava IR -> 4", abs(ds(lambda t: P_hl(t, 3), mp.mpf("1e8")) - 4) < 1e-3)

# Counterexample to 'z=3 is the only ghost-free Lorentzian realisation with UV d_s = 2'
Ein = lambda x: mp.euler + mp.log(x) + mp.e1(x) if x > 0 else mp.mpf(0)
S_nl = lambda k: k**2 * mp.e ** (Ein(k**4) / 2)
P_nl = lambda tau: P_quad(tau, S_nl)
u, i = ds(P_nl, mp.mpf("1e-7")), ds(P_nl, mp.mpf("1e7"))
# entire & zero-free: Ein has Taylor series sum (-1)^{n+1} x^n /(n n!); check series vs definition
xt = mp.mpf("2.5")
ser = mp.nsum(lambda n: (-1) ** (n + 1) * xt**n / (n * mp.factorial(n)), [1, mp.inf])
print(f"nonlocal form factor: d_s(1e-7) = {mp.nstr(u, 6)}, d_s(1e7) = {mp.nstr(i, 6)}; Ein series check {mp.nstr(ser - Ein(xt), 3)}")
check("X1 Ein entire (series = gamma+ln x+E1 x)", abs(ser - Ein(xt)) < 1e-15)
check("X1 Lorentz-invariant ghost-free (entire zero-free form factor) symbol with d_s: 4 -> 2 exists",
      abs(u - 2) < 0.05 and abs(i - 4) < 1e-3)

print(f"\nSUMMARY: {sum(ok)}/{len(ok)} PASS")
