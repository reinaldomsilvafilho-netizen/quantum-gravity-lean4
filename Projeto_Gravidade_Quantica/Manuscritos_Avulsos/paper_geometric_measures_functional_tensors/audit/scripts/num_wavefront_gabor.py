"""Def 5.2 / Thm 5.3: with a FIXED Gaussian window g (not compactly supported, width independent of xi),
the paper's 'wavefront set' condition sup_{x in U, xi in Gamma}(1+|xi|)^N |V(x,xi)| < inf fails at points x FAR from the jump.
d=1, f = Heaviside H(y) (jump at 0).  Closed form (oracle 1): V(x,xi) = int_0^inf g(y-x) e^{-i xi y} dy, g Gaussian sigma=0.1.
Oracle 2: direct quadrature with mpmath.  We show |xi| * |V(x0,xi)| -> g(x0)=g(-x0) != 0 for x0 = 0.5 (5 sigma away),
i.e. only 1/|xi| decay -> (x0, xi) would lie in the paper's WF though x0 is not on the interface.
Negative control 1: smooth f (Gaussian) -> super-polynomial decay.
Negative control 2: compactly supported smooth window centred at x0 (Hormander's definition) -> rapid decay."""
import mpmath as mp, numpy as np, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
mp.mp.dps = 40
s = mp.mpf("0.1")
def g(y):
    return mp.e**(-(y)**2 / (2 * s**2)) / mp.sqrt(mp.sqrt(mp.pi) * s)  # L2-normalised Gaussian
def V_closed(x, xi):
    # int_0^inf c e^{-(y-x)^2/(2s^2)} e^{-i xi y} dy = c * e^{-i xi x} * s*sqrt(pi/2) * e^{-s^2 xi^2/2} * erfc(-(x - i s^2 xi)/(s sqrt2))
    c = 1 / mp.sqrt(mp.sqrt(mp.pi) * s)
    z = -(x - 1j * s**2 * xi) / (s * mp.sqrt(2))
    return c * mp.e**(-1j * xi * x) * s * mp.sqrt(mp.pi / 2) * mp.e**(-s**2 * xi**2 / 2) * mp.erfc(z)
def V_quad(x, xi):
    return mp.quad(lambda y: g(y - x) * mp.e**(-1j * xi * y), [0, x, x + 2, mp.inf], maxdegree=10)
out = []; fails = 0
def log(t):
    out.append(t); print(t)
x0 = mp.mpf("0.5")
log("x0=0.5 (5 window widths from the jump at 0); g(-x0)=%s" % mp.nstr(g(-x0), 6))
for xi in (10, 100, 1000, 10000, 100000):
    vc = V_closed(x0, xi)
    line = "xi=%7d |V|=%s  |xi||V|=%s" % (xi, mp.nstr(abs(vc), 6), mp.nstr(xi * abs(vc), 6))
    if xi <= 1000:
        vq = V_quad(x0, xi); line += "  quad|V|=%s" % mp.nstr(abs(vq), 6)
        if abs(vq - vc) > 1e-6 * abs(vc): fails += 1; line += " MISMATCH"
    log(line)
lim = 100000 * abs(V_closed(x0, 100000))
log("limit |xi||V| -> %s vs g(-x0)=%s: polynomial (1/xi) decay => (x0,xi) in WF per paper's definition although x0 not in Gamma" % (mp.nstr(lim, 6), mp.nstr(g(-x0), 6)))
fails += not (abs(lim - g(-x0)) < 1e-3 * g(-x0))
# negative control 1: smooth f = Gaussian centred at 0 width 0.3
def V_smooth(x, xi):
    a = mp.mpf("0.3")
    return mp.quad(lambda y: mp.e**(-y**2 / (2 * a**2)) * g(y - x) * mp.e**(-1j * xi * y), [-mp.inf, -1, 0, x, 1, mp.inf])
for xi in (10, 40, 80, 120):
    v = V_smooth(x0, xi); log("NEG CTRL smooth f: xi=%d |V|=%s xi^4|V|=%s" % (xi, mp.nstr(abs(v), 6), mp.nstr(xi**4 * abs(v), 6)))
vs = abs(V_smooth(x0, 120)); fails += not (120**4 * vs < 1e-6)
# negative control 2: compactly supported bump window around x0 (radius 0.2) on Heaviside
def bump(y):
    r = mp.mpf("0.2"); u = (y - x0) / r
    return mp.e**(-1 / (1 - u**2)) if abs(u) < 1 else mp.mpf(0)
cv = []
for xi in (10, 100, 1000, 3000):
    v = mp.quad(lambda y: bump(y) * mp.e**(-1j * xi * y), list(mp.linspace(x0 - mp.mpf("0.2"), x0 + mp.mpf("0.2"), 400)))
    cv.append(xi**4 * abs(v))
    log("NEG CTRL compact window (Hormander): xi=%d |V|=%s xi^4|V|=%s" % (xi, mp.nstr(abs(v), 6), mp.nstr(xi**4 * abs(v), 6)))
txt = "\n".join(out)
open(os.path.join(HERE, "num_wavefront_gabor.out.txt"), "w", encoding="utf8").write(txt + "\nfailures=%d\n" % fails)
sys.exit(fails)
