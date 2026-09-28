"""Branch (a): isotropic symbol k^2 + l^2 k^4 continued to Lorentzian signature.

Checks (units l = 1 unless stated; metric mostly plus, p^2 = -p0^2 + |p|^2):
  A1  partial fractions of G(s) = 1/(s(1 + l^2 s)), s = p^2:
      oracle 1 = sympy.apart, oracle 2 = numerical contour integral (mpmath) around
      each pole in the complex s plane.  Expected: Res_{s=0} = +1, Res_{s=-1/l^2} = -1.
  A2  spectral (Kallen-Lehmann) weight: G(s) = sum_i Z_i/(s + m_i^2) with Z = (+1, -1),
      m^2 = (0, 1/l^2).  Z_ghost < 0  <=> negative-norm state.  Checked for several l.
  A3  energy-plane residue at p0 = +omega_m (omega_m^2 = k^2 + 1/l^2) of the Feynman-like
      propagator D(p0) = 1/(p^2 (1 + l^2 p^2)): numerical contour vs closed form
      -1/(2 omega_m) * (-1) ... sign compared with a healthy massive field.
  A4  static potential: V(r) = -(1/(2 pi^2 r)) int_0^inf k sin(kr) /(k^2 + l^2 k^4) dk * (4 pi G M)
      vs closed form -(GM/r)(1 - exp(-r/l)); oracle = scipy quad (QAWF) vs closed form.
  Negative controls (each must FAIL the corresponding test):
      NC1 healthy mutant G = 1/s + 1/(s+1)  -> ghost test must report 'no ghost'.
      NC2 sign-flipped mutant 1/(s(1 - l^2 s)) -> pole must NOT be at s = -1/l^2 (it is tachyonic).
      NC3 mutated closed-form potential -(GM/r)(1 + exp(-r/l)) must disagree with quadrature.
"""
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.integrate import quad

PASS = []


def check(name, cond):
    PASS.append((name, bool(cond)))
    print(('PASS ' if cond else 'FAIL ') + name)


def contour_residue(f, z0, rad=1e-3):
    """Residue via (1/2 pi i) closed-circle integral (independent of sympy)."""
    g = lambda t: f(z0 + rad * mp.e ** (1j * t)) * 1j * rad * mp.e ** (1j * t)
    return mp.quad(g, [0, mp.pi / 2, mp.pi, 3 * mp.pi / 2, 2 * mp.pi]) / (2j * mp.pi)


# ---------- A1 -------------------------------------------------------------
s = sp.symbols('s')
l = sp.symbols('ell', positive=True)
G = 1 / (s * (1 + l**2 * s))
apart = sp.apart(G, s)
print('sympy apart:', apart)
res_sym = {sp.Integer(0): sp.residue(G, s, 0), -1 / l**2: sp.residue(G, s, -1 / l**2)}
print('sympy residues:', res_sym)
for lval in [1.0, 0.3, 2.5]:
    f = lambda z, L=lval: 1 / (z * (1 + L**2 * z))
    r0 = complex(contour_residue(f, 0))
    rg = complex(contour_residue(f, -1 / lval**2, rad=1e-3 / lval**2))
    s0 = float(res_sym[sp.Integer(0)].subs(l, lval))
    sg = float(res_sym[-1 / l**2].subs(l, lval))
    print(f'l={lval}: contour Res(0)={r0.real:+.12f}, Res(-1/l^2)={rg.real:+.12f}; sympy {s0:+.1f},{sg:+.1f}')
    check(f'A1 residues agree sympy vs contour (l={lval})',
          abs(r0 - s0) < 1e-10 and abs(rg - sg) < 1e-10)
    check(f'A2 ghost weight Z=-1 at m^2=1/l^2 (l={lval})', rg.real < -0.999999)

# ---------- A3: energy-plane residue ------------------------------------------
# Healthy massive scalar (mostly plus) : D_h(p0) = 1/(-p0^2 + w^2), Res_{p0=+w} = -1/(2w).
# Book operator: D(p0) = 1/(P (1 + l^2 P)), P = -p0^2 + k^2.
lval, k = 1.0, 0.7
w = np.sqrt(k**2 + 1 / lval**2)
D = lambda p0: 1 / ((-p0**2 + k**2) * (1 + lval**2 * (-p0**2 + k**2)))
Dh = lambda p0: 1 / (-p0**2 + w**2)
rD = complex(contour_residue(D, w))
rH = complex(contour_residue(Dh, w))
print(f'A3 energy-plane residue at p0=+omega_m: book {rD.real:+.10f}, healthy massive {rH.real:+.10f}')
check('A3 book residue = -(healthy residue)  (opposite sign => ghost)', abs(rD + rH) < 1e-10)

# ---------- A4: static potential ---------------------------------------------
def V_quad(r, L):
    # V/(G M) = -(4 pi) * (1/(2 pi^2 r)) int_0^inf k sin(kr) G(k^2) dk ; G = 1/(k^2 + L^2 k^4)
    # use k*G = 1/(k (1 + L^2 k^2)); int_0^inf sin(kr)/(k(1+L^2k^2)) dk via QAWF (weight sin)
    a = 1.0
    v1, _ = quad(lambda kk: np.sinc(kk * r / np.pi) * r / (1 + L**2 * kk**2), 0, a,
                 epsabs=1e-14, epsrel=1e-12, limit=400)
    v2, _ = quad(lambda kk: 1 / (kk * (1 + L**2 * kk**2)), a, np.inf,
                 weight='sin', wvar=r, limlst=200)
    val = v1 + v2
    return -(4 * np.pi) / (2 * np.pi**2 * r) * val


V_closed = lambda r, L: -(1 / r) * (1 - np.exp(-r / L))
V_mut = lambda r, L: -(1 / r) * (1 + np.exp(-r / L))
rs = [0.05, 0.3, 1.0, 3.0, 10.0]
errs = [abs(V_quad(r, 1.0) - V_closed(r, 1.0)) / abs(V_closed(r, 1.0)) for r in rs]
errs_m = [abs(V_quad(r, 1.0) - V_mut(r, 1.0)) / abs(V_mut(r, 1.0)) for r in rs]
print('A4 rel.err quad vs closed:', ['%.1e' % e for e in errs])
check('A4 V(r) = -(GM/r)(1 - e^{-r/l}) (Yukawa alpha=-1, finite at r=0: V(0) = -GM/l)',
      max(errs) < 1e-6)
print('NC3 rel.err quad vs mutant:', ['%.1e' % e for e in errs_m])
check('NC3 mutated potential (1+e^{-r/l}) is rejected (disagrees for r <~ l)', max(errs_m) > 1e-2)

# ---------- Negative controls on the ghost test -----------------------------
def ghost_poles(expr):
    """Return list of (pole, residue) with negative residue among poles of expr in s."""
    num, den = sp.fraction(sp.together(expr))
    out = []
    for p in sp.roots(sp.Poly(den, s)).keys():
        r = sp.residue(expr, s, p)
        out.append((p, r))
    return out


healthy = 1 / s + 1 / (s + 1)
hp = ghost_poles(healthy)
print('NC1 healthy mutant poles/residues:', hp)
check('NC1 healthy mutant flagged ghost-free (ghost test must not fire)',
      all(float(r) > 0 for _, r in hp))
book = ghost_poles(G.subs(l, 1))
check('A2b ghost test fires on book operator', any(float(r) < 0 for _, r in book))
flip = 1 / (s * (1 - s))
fp = ghost_poles(flip)
print('NC2 sign-flipped mutant poles/residues:', fp)
check('NC2 mutant pole not at s=-1/l^2 (tachyon at s=+1/l^2 instead)',
      all(p != -1 for p, _ in fp) and any(p == 1 for p, _ in fp))

# ---------- A5: Lorentzian group velocities of the two branches -------------
# massless branch omega = k (v_g = 1); ghost branch omega^2 = k^2 + 1/l^2 (v_g = k/omega < 1).
kk = np.logspace(-3, 3, 13)
vg_ghost = kk / np.sqrt(kk**2 + 1.0)
check('A5 isotropic Lorentzian branches are not superluminal (v_g <= 1)', np.all(vg_ghost <= 1))
# the phenomenological ansatz omega^2 = k^2 (1 + xi l^2 k^2), xi > 0, IS superluminal:
xi = 0.5
vg_ans = (1 + 2 * xi * kk**2) / np.sqrt(1 + xi * kk**2)
check('A5b ansatz omega^2=k^2(1+xi l^2 k^2), xi>0, has v_g > 1 (needs preferred frame)',
      np.all(vg_ans > 1))

print('\nSUMMARY: %d/%d PASS' % (sum(c for _, c in PASS), len(PASS)))
