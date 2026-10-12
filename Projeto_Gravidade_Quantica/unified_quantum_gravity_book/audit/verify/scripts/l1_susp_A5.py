"""L1 blind check A5 (ch. 3, Digamma PDE system).

Oracle: mpmath numerical derivative of binom(x,y) = Gamma(x+1) rgamma(y+1) rgamma(x-y+1)
(rgamma = entire 1/Gamma), compared with the PDE right-hand sides.
At y = -1 (allowed by the chapter's definition: y in C), the RHS reads 0 * infinity.
Negative control: mutated PDE with psi(x) in place of psi(x+1) must fail.
"""
import mpmath as mp

mp.mp.dps = 30
B = lambda x, y: mp.gamma(x + 1) * mp.rgamma(y + 1) * mp.rgamma(x - y + 1)

for (x, y) in [(mp.mpf("2.3"), mp.mpf("0.7")), (mp.mpf("0.4"), mp.mpf("-0.3")), (mp.mpf("3.1"), mp.mpf("-1.6"))]:
    dx = mp.diff(lambda s: B(s, y), x)
    dy = mp.diff(lambda s: B(x, s), y)
    rx = B(x, y) * (mp.digamma(x + 1) - mp.digamma(x - y + 1))
    ry = B(x, y) * (mp.digamma(x - y + 1) - mp.digamma(y + 1))
    bad = B(x, y) * (mp.digamma(x) - mp.digamma(x - y + 1))
    print(f"(x,y)=({x},{y}): err_x={mp.nstr(abs(dx-rx),3)} err_y={mp.nstr(abs(dy-ry),3)} mutant_err={mp.nstr(abs(dx-bad),3)}")
    assert abs(dx - rx) < 1e-15 and abs(dy - ry) < 1e-15 and abs(dx - bad) > 1e-3

x = mp.mpf("0.7")
y = mp.mpf(-1)
dy = mp.diff(lambda s: B(x, s), y)
print("at y=-1: B =", B(x, y), " dB/dy (oracle) =", mp.nstr(dy, 15), " 1/(x+1) =", mp.nstr(1 / (x + 1), 15))
try:
    val = B(x, y) * (mp.digamma(x - y + 1) - mp.digamma(y + 1))
    print("RHS as written:", val)
except Exception as e:  # digamma has a pole at 0
    print("RHS as written is undefined (0 * inf):", type(e).__name__, e)
# limit of the RHS: rgamma(z)*digamma(z) = -(d/dz) rgamma(z), entire
lim = mp.limit(lambda s: B(x, s) * (mp.digamma(x - s + 1) - mp.digamma(s + 1)), y)
print("limit of RHS as y->-1:", mp.nstr(lim, 15))
assert abs(lim - dy) < 1e-10 and abs(dy) > 0.1
print("A5: identity true where psi-arguments avoid Z_{<=0}; extends continuously; literal RHS undefined on y in Z_<0, x-y in Z_<0.")
