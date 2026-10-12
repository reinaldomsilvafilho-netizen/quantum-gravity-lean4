"""L2 (final integration) check of F-20 on the book side (ch12, ch13, Dictionary).
Oracle: P(tau) by direct radial quadrature of (2pi)^-4 int_R4 exp(-tau(k^2 + l^2 k^4)) d^4k, and
d_s = -2 dlnP/dlntau by a centred finite difference; compared with the erfc closed form printed
identically in ch12 eq. analytical_ds_formula, ch13 eq. ds_tau and Dictionary Box 6.
Negative controls: mutated closed forms (exp(tau/2l^2); 1 - tau/l^2) must fail.
Also: alpha_t = (d_s(p)-4)/2 equals -x/(1+x), x = (p/M)^2 (and the old ch12 form -1/(1+x^-1));
magnitude (H_inf/M_P)^2 with H_inf from 2H^2/(pi^2 Mred^2) = r A_s.  Units: l = 1 (tau in l^2)."""
import math
import numpy as np
from scipy.integrate import quad
from scipy.special import erfcx

FAIL = []


def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + ("  | " + str(info) if info != "" else ""))
    if not ok:
        FAIL.append(name)


def P_quad(tau, l=1.0):
    # d^4k = 2 pi^2 k^3 dk
    f = lambda k: 2 * math.pi ** 2 * k ** 3 * math.exp(-tau * (k * k + l * l * k ** 4))
    return quad(f, 0, np.inf, limit=400, epsabs=0, epsrel=1e-13)[0] / (2 * math.pi) ** 4


def ds_oracle(tau, h=1e-4):
    return -2 * (math.log(P_quad(tau * math.exp(h))) - math.log(P_quad(tau * math.exp(-h)))) / (2 * h)


def ds_book(tau, l=1.0):
    z = math.sqrt(tau) / (2 * l)
    return 1 - tau / (2 * l * l) + 1 / (1 - math.sqrt(math.pi) * z * erfcx(z))  # erfcx(z) = e^{z^2} erfc z


def ds_mut1(tau, l=1.0):
    z = math.sqrt(tau) / (2 * l)
    return 1 - tau / (2 * l * l) + 1 / (1 - math.sqrt(math.pi) * z * erfcx(z) * math.exp(z * z))


def ds_mut2(tau, l=1.0):
    z = math.sqrt(tau) / (2 * l)
    return 1 - tau / (l * l) + 1 / (1 - math.sqrt(math.pi) * z * erfcx(z))


def P_book(tau, l=1.0):
    z = math.sqrt(tau) / (2 * l)
    return (1 - math.sqrt(math.pi) * z * erfcx(z)) / (32 * math.pi ** 2 * l * l * tau)


taus = [1e-3, 1e-2, 0.1, 1, 4, 10, 30]
errP = max(abs(P_book(t) / P_quad(t) - 1) for t in taus)
check("P(tau) closed form = quadrature", errP < 1e-7, f"max rel err {errP:.1e}")
err = max(abs(ds_book(t) - ds_oracle(t)) for t in taus)
check("d_s(tau) closed form = -2 dlnP/dlntau (quadrature)", err < 1e-5, f"max abs err {err:.1e}")
check("limits: d_s -> 2 (tau->0), 4 (tau->inf)", abs(ds_book(1e-8) - 2) < 1e-3 and abs(ds_book(1e5) - 4) < 2e-4,
      (round(ds_book(1e-8), 5), round(ds_book(1e5), 6)))
for name, f in [("NC exp(tau/2l^2) mutation", ds_mut1), ("NC 1 - tau/l^2 mutation", ds_mut2)]:
    e = max(abs(f(t) - ds_oracle(t)) for t in taus)
    check(name + " must fail", e > 1e-2, f"max abs err {e:.2e}")

x = np.logspace(-6, 4, 50)
dsp = 2 + 2 / (1 + x)
check("alpha_t = (d_s(p)-4)/2 = -x/(1+x)", np.allclose((dsp - 4) / 2, -x / (1 + x), rtol=1e-14))
check("old ch12 form -1/(1+x^-1) is the same function", np.allclose(-1 / (1 + 1 / x), -x / (1 + x), rtol=1e-12))
check("NC Lean-header form 2+2/(1+sqrt x) differs", not np.allclose(2 + 2 / (1 + np.sqrt(x)), dsp))
# Pade form vs closed form: same limits, different function (tau ~ p^-2 identification, l = 1/M)
pade = lambda tau: 2 + 2 / (1 + 1 / tau)
dev = max(abs(pade(t) - ds_book(t)) for t in taus)
check("Pade d_s(p) with tau = p^-2 is NOT the closed form (text calls it an interpolation)", dev > 0.05, f"max dev {dev:.3f}")

# magnitude (GeV; CODATA/PDG: M_P = 1.22091e19 GeV, M_red = M_P/sqrt(8 pi))
MP = 1.22091e19; Mred = MP / math.sqrt(8 * math.pi)
r, As = 0.036, 2.1e-9
H = math.pi * Mred * math.sqrt(r * As / 2)
a = (H / MP) ** 2
check("H_inf ~ 4.7e13 GeV", abs(H / 4.7e13 - 1) < 0.02, f"{H:.3e} GeV")
check("|alpha_t| ~ (H/M_P)^2 <~ 1.5e-11 (dimensionless)", abs(a / 1.5e-11 - 1) < 0.03, f"{a:.3e}")
check("NC: using M_red instead of M_P gives a different magnitude", abs((H / Mred) ** 2 / 1.5e-11 - 1) > 0.5, f"{(H/Mred)**2:.2e}")
print("\nFAILURES:", FAIL if FAIL else "none")
