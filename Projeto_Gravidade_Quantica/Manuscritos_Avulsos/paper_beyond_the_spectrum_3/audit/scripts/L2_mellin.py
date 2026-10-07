"""Layer-2 re-check of Prop. 7.1 (Z_A entire), Remark 7.2 and new Prop. 7.3.

Prop 7.3: M_j(s) = Gamma(a0) Gamma(aj+s) / (Gamma(aj) Gamma(a0+s)); poles s = -aj-k,
  residue (-1)^k/k! * Gamma(a0)/(Gamma(aj) Gamma(bj-k)) when bj = a0-aj not integer;
  if bj in Z>0: rational, simple poles exactly at -aj-k, 0 <= k <= bj-1.
Oracles (independent of the Beta reduction used in the proof):
  (1) M_1(s) for Re s > -a1 by a *2-dimensional* integral over Delta_3 (nested QUADPACK,
      algebraic weights), alpha = (0.7, 1.3, 2.25), several real s.
  (2) Analytic continuation for Re s < -a1 by the subtracted integral (series tail on [0,1/2])
        int_0^1 u^{s+a-1} [(1-u)^{b-1} - sum_{i<K} c_i u^i] du + sum_{i<K} c_i/(s+a+i),
      c_i = Taylor coefficients of (1-u)^{b-1} computed by mpmath.taylor (numerical
      differentiation), divided by B(a,b); compared with the Gamma formula at complex s.
  (3) Residues: c_k / B(a,b) (from the Taylor coefficients) vs the stated closed form;
      also the contour integral of the Gamma formula around each pole.
  (4) Integer b = 2: contour integrals around -a-k vanish for k >= 2, are non-zero for k = 0, 1.
  Negative controls: residue with (-1)^{k+1}; residue with Gamma(b+k) in place of Gamma(b-k).
Prop 7.1: Z_A(s) = int Phi^s dmu_alpha for Phi = 1 + u1 + 0.5 sin(3 u2) on Delta_3:
  contour integrals around the v2 "poles" -a_j - k vanish; |Z(s)| <= max(c1^Re s, c2^Re s);
  negative control: the same contour routine detects the residue of M_1 at -a1.
"""
import sys
import numpy as np
import mpmath as mp
from scipy import integrate
from scipy.special import roots_jacobi

mp.mp.dps = 30
fails = 0
out = []


def log(s):
    print(s)
    out.append(s)


def check(name, ok):
    global fails
    log(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        fails += 1


al = [0.7, 1.3, 2.25]
a0 = sum(al)
norm = float(mp.gamma(a0) / (mp.gamma(al[0]) * mp.gamma(al[1]) * mp.gamma(al[2])))


def M_formula(s, aj, a0):
    return mp.gamma(a0) * mp.gamma(aj + s) / (mp.gamma(aj) * mp.gamma(a0 + s))


log("== (1) 2D integral over Delta_3 vs Gamma formula ==")
for s in (1.7, 0.5, -0.4, -0.65):
    def inner(u1, s=s):
        r = 1 - u1
        # int_0^r u2^{a2-1} (r-u2)^{a3-1} du2, algebraic weight on [0, r]
        v, _ = integrate.quad(lambda u2: 1.0, 0, r, weight="alg", wvar=(al[1] - 1, al[2] - 1),
                              epsabs=1e-14, epsrel=1e-13)
        return v
    val, err = integrate.quad(lambda u1: inner(u1), 0, 1, weight="alg",
                              wvar=(s + al[0] - 1, 0.0), epsabs=1e-13, epsrel=1e-12, limit=200)
    val *= norm
    ref = float(M_formula(s, al[0], a0))
    log(f"s={s:+.2f}: 2D quad={val:.12f}  formula={ref:.12f}")
    check(f"2D integral = formula at s={s}", abs(val - ref) < 1e-9 * max(1, abs(ref)))

log("== (2)-(3) continuation and residues, b non-integer ==")
a, b = al[0], a0 - al[0]
B = mp.beta(a, b)
K = 6
c = mp.taylor(lambda u: (1 - u) ** (b - 1), 0, K)


# binomial-series coefficients by the recurrence from (1-u) f' = -(b-1) f (no Gamma):
NT = 400
cr = [mp.mpf(1)]
for i in range(NT):
    cr.append(cr[-1] * (i - (b - 1)) / (i + 1))


def M_cont(s):
    # [0,1/2]: tail sum_{i>=K} c_i u^i integrated termwise (avoids cancellation near 0);
    # [1/2,1]: subtracted integrand by quadrature.  NOTE: a first version integrated the
    # subtracted integrand on [0,1] directly and failed by catastrophic cancellation near
    # u = 0 (u^{Re s + a - 1} with Re s + a < -1); the fix changes the oracle, not a tolerance.
    tail = sum(cr[i] * mp.mpf(0.5) ** (s + a + i) / (s + a + i) for i in range(K, NT))
    f = lambda u: u ** (s + a - 1) * ((1 - u) ** (b - 1) - sum(cr[i] * u ** i for i in range(K)))
    I = mp.quad(f, [0.5, 0.75, 1])
    return (tail + I + sum(cr[i] / (s + a + i) for i in range(K))) / B


for s in (mp.mpc(-a - 1.5, 0.3), mp.mpc(-a - 3.2, -0.7), mp.mpc(-a - 0.5, 0)):
    v = M_cont(s)
    ref = M_formula(s, a, a0)
    log(f"s={mp.nstr(s, 6)}: continuation={mp.nstr(v, 14)} formula={mp.nstr(ref, 14)}")
    check(f"continuation = formula at s={mp.nstr(s, 4)}", abs(v - ref) < 1e-10 * max(1, abs(ref)))


def res_formula(k, aj, a0, mut=None):
    bj = a0 - aj
    sgn = (-1) ** (k + 1) if mut == "sign" else (-1) ** k
    g = mp.gamma(bj + k) if mut == "gamma" else mp.gamma(bj - k)
    return sgn / mp.factorial(k) * mp.gamma(a0) / (mp.gamma(aj) * g)


def contour(f, z0, r=0.2, n=256):
    th = [2 * mp.pi * i / n for i in range(n)]
    return sum(f(z0 + r * mp.e ** (1j * t)) * r * mp.e ** (1j * t) for t in th) / n


for k in range(5):
    r_taylor = c[k] / B
    r_form = res_formula(k, a, a0)
    r_cont = contour(lambda s: M_formula(s, a, a0), -a - k)
    log(f"k={k}: Taylor c_k/B={mp.nstr(r_taylor, 12)} formula={mp.nstr(r_form, 12)} contour={mp.nstr(mp.re(r_cont), 12)}")
    check(f"residue k={k}: Taylor route = formula", abs(r_taylor - r_form) < 1e-10)
    check(f"residue k={k}: contour = formula", abs(r_cont - r_form) < 1e-10)
    check(f"residue k={k}: formula non-zero", abs(r_form) > 1e-6)
    if k >= 1:
        check(f"negative control k={k}: (-1)^(k+1) fails", abs(res_formula(k, a, a0, "sign") - r_form) > 1e-6)
    check(f"negative control k={k}: Gamma(b+k) fails" if k else "negative control k=0 Gamma(b+k) (identical at k=0, skipped)",
          k == 0 or abs(res_formula(k, a, a0, "gamma") - r_form) > 1e-6)

log("== (4) integer b = 2 (alpha = (0.7, 0.9, 1.1)): poles only at k = 0, 1 ==")
al2 = [0.7, 0.9, 1.1]
a02 = sum(al2)
for k in range(5):
    rc = contour(lambda s: M_formula(s, al2[0], a02), -al2[0] - k)
    log(f"b=2 k={k}: contour residue = {mp.nstr(rc, 10)}")
    if k <= 1:
        expect = res_formula(k, al2[0], a02)
        check(f"b=2 k={k}: residue = formula", abs(rc - expect) < 1e-10 and abs(expect) > 1e-6)
    else:
        check(f"b=2 k={k}: no pole (cancellation)", abs(rc) < 1e-12)

log("== Prop 7.1: Z_A entire ==")
# tensor Gauss-Jacobi rule on Delta_3: u1 = x, u2 = (1-x) y, u3 = (1-x)(1-y)
# density u1^{a1-1} u2^{a2-1} u3^{a3-1} du1 du2 = x^{a1-1}(1-x)^{a2+a3-1} y^{a2-1}(1-y)^{a3-1} dx dy
nq = 60
tx, wx = roots_jacobi(nq, al[1] + al[2] - 1, al[0] - 1)   # weight (1-t)^alpha (1+t)^beta on [-1,1]
ty, wy = roots_jacobi(nq, al[2] - 1, al[1] - 1)
x = (1 + tx) / 2
wx = wx / 2 ** (al[0] + al[1] + al[2] - 1)
y = (1 + ty) / 2
wy = wy / 2 ** (al[1] + al[2] - 1)
X, Y = np.meshgrid(x, y, indexing="ij")
Wt = np.outer(wx, wy) * norm
U1, U2 = X, (1 - X) * Y
Phi = 1 + U1 + 0.5 * np.sin(3 * U2)
check("quadrature integrates the Dirichlet density to 1", abs(Wt.sum() - 1) < 1e-12)
c1, c2 = Phi.min(), Phi.max()
logPhi = np.log(Phi)


def Z(s):
    return complex(np.sum(Wt * np.exp(complex(s) * logPhi)))


def contour_np(f, z0, r=0.2, n=256):
    th = 2 * np.pi * np.arange(n) / n
    z = z0 + r * np.exp(1j * th)
    return np.mean([f(zz) * r * np.exp(1j * t) for zz, t in zip(z, th)])


maxres = 0
for j in range(3):
    for k in range(4):
        z0 = -al[j] - k
        rc = contour_np(Z, z0)
        maxres = max(maxres, abs(rc))
        zv = Z(z0)
        bound = max(c1 ** z0, c2 ** z0)
        check(f"|Z({z0:.2f})| = {abs(zv):.4f} <= max(c1^s, c2^s) = {bound:.4f}", abs(zv) <= bound + 1e-12)
log(f"max |contour integral of Z| around the 12 claimed poles = {maxres:.2e}")
check("Z_A has no residue at any claimed pole (|.| < 1e-12)", maxres < 1e-12)
ctrl = contour(lambda s: M_formula(s, al[0], a0), -al[0])
log(f"control: same contour routine on M_1 at -a1 gives {mp.nstr(ctrl, 10)}")
check("negative control: contour routine detects the pole of M_1", abs(ctrl) > 1e-3)
Zc = Z(1.0)
check("Z(1) = E[Phi] matches independent 2D QUADPACK",
      abs(Zc - norm * integrate.dblquad(
          lambda u2, u1: (1 + u1 + 0.5 * np.sin(3 * u2)) * u1 ** (al[0] - 1) * u2 ** (al[1] - 1)
          * max(1 - u1 - u2, 0) ** (al[2] - 1), 0, 1, 0, lambda u1: 1 - u1, epsabs=1e-10)[0]) < 1e-6)

log(f"failures: {fails}")
with open(__file__.replace(".py", ".out.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
sys.exit(fails)
