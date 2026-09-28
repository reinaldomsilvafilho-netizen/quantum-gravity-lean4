"""L2 re-check (2026-09-28) of the ch3 Dixon correction and the ch12/ch13/SQG operator correction.

Independent code (mpmath direct quadrature; own cosmology integral), with negative controls.
Run: python L2_dixon_operator_numbers.py
"""
import mpmath as mp

mp.mp.dps = 50
FAILS = 0


def check(name, ok):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        FAILS += 1


# ---------------------------------------------------------------- Dixon
def f(x, t):
    return (mp.gamma(2 * x + 1) * mp.rgamma(x + 1 + t) * mp.rgamma(x + 1 - t)) ** 3


def integral(x, a, b, j=1):
    pts = [a] + [mp.mpf(k) for k in range(int(mp.ceil(a)), int(mp.floor(b)) + 1) if a < k < b] + [b]
    return mp.quad(lambda t: mp.cos(j * mp.pi * t) * f(x, t), pts)


def target(x):
    return mp.gamma(3 * x + 1) / mp.gamma(x + 1) ** 3 / 2


def tau(x):
    m = 2 * x + 1
    return 1 / (3 * mp.digamma(m)) + 1 / (mp.pi ** 3 * m ** 2 * (m - 1))


print("== Dixon: ratio - 1, truncated [-x,x] vs full line ==")
claimed = {5: 5.1e-7, 7.5: -5.2e-11, 10: -6.0e-14, 20: -5e-28}
res = {}
for x in [5, 7.5, 10, 20]:
    X = mp.mpf(x)
    tr = integral(X, -X, X)
    L = X + 40
    full = integral(X, -L, L)
    rt = tr / target(X) - 1
    rf = full / target(X) - 1
    res[x] = (rt, rf)
    print(f"x={x}: trunc ratio-1 = {mp.nstr(rt, 4)} ; full-line ratio-1 = {mp.nstr(rf, 4)} ;"
          f" |trunc-target| = {mp.nstr(abs(tr - target(X)), 4)} <= 2tau = {mp.nstr(2 * tau(X), 4)}")
    c = claimed[x]
    check(f"x={x} truncated matches text value {c} to 2 sig. digits",
          abs(rt - c) <= 0.06 * abs(c))
    check(f"x={x} full-line ratio-1 ~ 0 (Cohl-Volkmer exact) |rf|<1e-35", abs(rf) < mp.mpf('1e-35'))
    check(f"x={x} tail bound 2tau(x) holds", abs(tr - target(X)) <= 2 * tau(X))
# negative control 1: the text attributes the numbers to 2*int_R ...; full-line values do NOT match
nc1 = all(abs(res[x][1] - claimed[x]) <= 0.06 * abs(claimed[x]) for x in claimed)
check("NEG: full-line integral reproduces the quoted numbers (must be False)", not nc1)
# negative control 2: drop the 1/2 in the target
x = mp.mpf(10)
check("NEG: target without 1/2 rejected", abs(integral(x, -x, x) / (2 * target(x)) - 1) > 0.4)
# double precision check at x=10
rt10 = res[10][0]
check("x=10: |ratio-1| exceeds double eps 2.2e-16 (sentence 'not 1 in double precision' true)",
      abs(rt10) > 2.3e-16)

print("== Dixon integer theorem: |int_{-n}^n cos f - 1/2 (3n)!/(n!)^3| <= 2 tau_n ==")
worst = 0
negfail = False
for n in range(1, 16):
    N = mp.mpf(n)
    tr = integral(N, -N, N)
    D = sum((-1) ** k * mp.binomial(2 * n, n + k) ** 3 for k in range(-n, n + 1))
    check(f"n={n} Dixon sum = (3n)!/(n!)^3", D == mp.factorial(3 * n) / mp.factorial(n) ** 3)
    err = abs(tr - D / 2)
    worst = max(worst, err / (2 * tau(N)))
    if err > 2 * tau(N) / 4:
        negfail = True
    # higher harmonic j=3 bound
    I3 = integral(N, -N, N, j=3)
    check(f"n={n} |I_3| <= 2 tau_n", abs(I3) <= 2 * tau(N))
print("max err/(2 tau_n) =", mp.nstr(worst, 4))
check("NEG: bound tau_n/2 (i.e. 2tau/4) is violated for some n (bound not trivially loose)", negfail)

# ------------------------------------------------------------ Operator numbers
print("== Operator: v_g sign, M* window, rescaled delay ==")
for xi, expect_super in [(0.5, True), (-0.5, False)]:
    w = lambda k: mp.sqrt(k ** 2 * (1 + xi * k ** 2))  # c = l = 1
    vg = mp.diff(w, mp.mpf('0.3'))
    check(f"xi={xi}: v_g>c is {expect_super} (v_g={mp.nstr(vg, 6)})", (vg > 1) == expect_super)

# CODATA 2018
hbar = mp.mpf('1.054571817e-34'); c = mp.mpf(299792458); G = mp.mpf('6.67430e-11')
eV = mp.mpf('1.602176634e-19')
lP = mp.sqrt(hbar * G / c ** 3)
EP_GeV = mp.sqrt(hbar * c ** 5 / G) / eV / 1e9
print("l_P =", mp.nstr(lP, 6), "m ; E_P =", mp.nstr(EP_GeV, 6), "GeV")
for Mstar in [1e16, 1e15, 1e10]:
    ls = hbar * c / (Mstar * 1e9 * eV)
    print(f"M*={Mstar:g} GeV: l*={mp.nstr(ls, 4)} m = {mp.nstr(ls / lP, 4)} l_P")
r = (EP_GeV / 1e10) ** 2
print("(l*/l_P)^2 for M*=1e10 GeV:", mp.nstr(r, 4))
check("(l*/l_P)^2 ~ 1.5e18", abs(r / mp.mpf('1.5e18') - 1) < 0.02)
check("l* range 1e3-1e9 l_P for M* 1e16-1e10 (order of magnitude)",
      2.5 < mp.log10(EP_GeV / 1e16) < 3.5 and 8.5 < mp.log10(EP_GeV / 1e10) < 9.5)

Mpc = mp.mpf('3.0856775814913673e22'); H0 = 70e3 / Mpc; Om, OL = mp.mpf('0.3'), mp.mpf('0.7')


def D2(z):
    return c / H0 * mp.quad(lambda s: (1 + s) ** 2 / mp.sqrt(Om * (1 + s) ** 3 + OL), [0, z])


def dt(ell, z, xi=mp.mpf('0.5'), f1=10, f2=1000):
    # dimensions: m^2 / (m^3 s^-3) * m * s^-2 = s
    return 6 * mp.pi ** 2 * xi * ell ** 2 / c ** 3 * D2(z) * (f2 ** 2 - f1 ** 2)


lstar = hbar * c / (mp.mpf(1e10) * 1e9 * eV)
out = {}
for z in [1, 3, 8]:
    a, b = dt(lP, z), dt(lstar, z)
    out[z] = (a, b)
    print(f"z={z}: dt(l_P)={mp.nstr(a, 3)} s ; dt(l*)={mp.nstr(b, 3)} s ; orders below 1e-4 s: "
          f"{mp.nstr(mp.log10(mp.mpf('1e-4') / b), 4)}")
check("dt(l_P) z=1 ~6e-62, z=8 ~1.2e-60", abs(out[1][0] / 6e-62 - 1) < 0.15 and abs(out[8][0] / 1.2e-60 - 1) < 0.15)
lo, hi = out[1][1], out[8][1]
check("rescaled delays in 1e-43..1e-42 range (order)", -44 < mp.log10(lo) < -42.5 and -42.5 < mp.log10(hi) < -41.5)
orders = [mp.log10(mp.mpf('1e-4') / out[z][1]) for z in out]
check("'some 38 orders': min orders in [37.5,38.5]", 37.5 <= min(orders) <= 38.5)
print("orders range:", mp.nstr(min(orders), 4), "-", mp.nstr(max(orders), 4))
# negative control: linear rescaling in l (wrong) gives ~47 orders, rejected
lin = [mp.log10(mp.mpf('1e-4') / (out[z][0] * mp.sqrt(r))) for z in out]
check("NEG: linear-in-l rescaling does not give ~38 orders", min(lin) > 42)

print("TOTAL FAILS:", FAILS)
