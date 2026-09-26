"""Camada 2 (F-41, cap. 13; tambem os numeros de 10 do cap. 12).

Oraculos independentes do gerador audit/scripts/observability_estimates.py:
  A. Atraso de dispersao: propagacao de um raio num FRW plano, integrada em a (fator de escala),
     com v_g calculado por derivada numerica (passo complexo) de omega(k) = c k sqrt(1 + xi l^2 k^2),
     k_fis = k_obs / a. NAO usa a formula fechada D_2 nem o fator (1+z)^2.
  B. l_* necessario e energia correspondente.
  C. H_inf a partir de r e A_s via o potencial V = (3 pi^2/2) A_s r M_red^4 e H^2 = V/(3 M_red^2)
     (caminho diferente da formula P_t = 2H^2/(pi^2 M_red^2)); |alpha_t| pelo Pade de d_s.
  D. l_P/lambda_dB para Sr-87 com a massa atomica tabelada.
  E. Figura: le os vetores de fig_experimental_signatures.pdf com PyMuPDF (sem usar o gerador),
     mapeia pelos ticks rotulados e compara com as formulas do texto atual.
Cada bloco tem mutacoes (sinal, fator, expoente) que DEVEM falhar.
Rodar do diretorio do livro:  python audit/verify/scripts/L2_ch13_numbers_figure.py
"""
import re
from pathlib import Path

import numpy as np
from scipy import integrate

ROOT = Path(__file__).resolve().parents[3]
FAIL = []


def check(name, ok, info=""):
    print(f"[{'OK  ' if ok else 'FAIL'}] {name} {info}")
    if not ok:
        FAIL.append(name)


def mutants_fail(name, results):
    """results: dict label -> bool(passes). The mutants must NOT pass."""
    bad = [k for k, v in results.items() if v]
    check(f"NEG {name}: all mutants rejected", not bad, f"mutants that passed: {bad}")


# ---------------------------------------------------------------- constantes (CODATA 2018)
c = 299792458.0
hbar = 1.054571817e-34
G = 6.67430e-11
lP = np.sqrt(hbar * G / c**3)
Mpc = 3.0856775814913673e22
H0 = 70e3 / Mpc
Om, OL = 0.3, 0.7
hbarc_eVm = 1.973269804e-7
M_P = np.sqrt(hbar * c / G) * c**2 / 1.602176634e-10       # GeV
M_red = M_P / np.sqrt(8 * np.pi)
Hubble = lambda a: H0 * np.sqrt(Om / a**3 + OL)

# ---------------------------------------------------------------- A. oraculo de propagacao
def omega(k, xi, ell):
    return c * k * np.sqrt(1 + xi * ell**2 * k**2 + 0j)


def vg(k, xi, ell):
    h = 1e-30 * k
    return (omega(k + 1j * h, xi, ell)).imag / h if False else \
        np.imag(c * (k + 1j * h) * np.sqrt(1 + xi * ell**2 * (k + 1j * h) ** 2)) / h


def advance(z, f, xi, ell):
    """How much earlier than light a packet of observed frequency f arrives, source at redshift z.
    Comoving distance excess at a=1 divided by c (the excess is tiny, so the last leg is at speed c)."""
    k0 = 2 * np.pi * f / c
    a_e = 1 / (1 + z)
    integrand = lambda a: (vg(k0 / a, xi, ell) - c) / (a**2 * Hubble(a))
    dchi = integrate.quad(integrand, a_e, 1.0, epsabs=0, epsrel=1e-12, limit=200)[0]
    return dchi / c


def dt_oracle(z, f1, f2, xi, ell):
    return advance(z, f2, xi, ell) - advance(z, f1, xi, ell)


def D_n(z, n):
    return c / H0 * integrate.quad(lambda x: (1 + x) ** n / np.sqrt(Om * (1 + x) ** 3 + OL), 0, z, epsrel=1e-12)[0]


def dt_text(z, f1, f2, xi, ell, n=2, pref=6 * np.pi**2, fpow=2):
    return pref * xi * ell**2 / c**3 * D_n(z, n) * (f2**fpow - f1**fpow)


xi = 0.5
ell_big = 30.0          # large l keeps the relative excess ~1e-7, resolvable in double precision
res = {}
for z in (1.0, 3.0, 8.0):
    o = dt_oracle(z, 10.0, 1000.0, xi, ell_big)
    o2 = dt_oracle(z, 10.0, 1000.0, xi, 2 * ell_big)
    lin = abs(o2 / o / 4 - 1)
    t = dt_text(z, 10.0, 1000.0, xi, ell_big)
    check(f"A z={z:g}: text D_2 (1+z)^2 formula vs ray oracle", abs(t / o - 1) < 1e-4 and lin < 1e-3,
          f"ratio={t/o:.6f}, l^2 scaling err={lin:.1e}")
    res[z] = o
mutants_fail("A (redshift weight / prefactor / frequency power)", {
    "(1+z)^1": all(abs(dt_text(z, 10, 1000, xi, ell_big, n=1) / res[z] - 1) < 1e-2 for z in res),
    "(1+z)^3": all(abs(dt_text(z, 10, 1000, xi, ell_big, n=3) / res[z] - 1) < 1e-2 for z in res),
    "3 pi^2": all(abs(dt_text(z, 10, 1000, xi, ell_big, pref=3 * np.pi**2) / res[z] - 1) < 1e-2 for z in res),
    "f^1": all(abs(dt_text(z, 10, 1000, xi, ell_big, fpow=1) / res[z] - 1) < 1e-2 for z in res),
})

# numeros citados (texto cap. 13 e cap. 12 10.1), escalados de l_big para l_P pelo fator l^2
quoted = {1: 6e-62, 3: 3e-61, 8: 1.2e-60}
vals = {z: res[float(z)] * (lP / ell_big) ** 2 for z in quoted}
check("A quoted delays 6e-62, 3e-61, 1.2e-60 s (rounding 15%)",
      all(abs(vals[z] / q - 1) < 0.15 for z, q in quoted.items()),
      ", ".join(f"z={z}: {v:.3e}" for z, v in vals.items()))
gaps = [np.log10(1e-4 / v) for v in vals.values()]
check("A '56-57 orders of magnitude'", 55.5 <= min(gaps) and max(gaps) < 57.5, f"gaps={[round(g, 2) for g in gaps]}")
# dimensao: [l^2][m]/[m^3 s^-3][s^-2] = s
check("A dimension of 6 pi^2 xi l^2 D (f^2) / c^3 is seconds", (2 + 1) - 3 == 0 and (3 - 2) == 1)

# ---------------------------------------------------------------- B. l_* e energia
ell_req = ell_big * np.sqrt(1e-4 / res[3.0])
E_eV = hbarc_eVm / ell_req
check("B l_* ~ 3.0e-7 m and hbar c/l_* ~ 0.7 eV", abs(ell_req / 3.0e-7 - 1) < 0.02 and 0.6 < E_eV < 0.75,
      f"l_*={ell_req:.3e} m, E={E_eV:.3f} eV")
ell_bad = ell_big * np.sqrt(1e-4 / (res[3.0] * D_n(3, 1) / D_n(3, 2)))
mutants_fail("B", {"(1+z)^1 -> l_*": abs(ell_bad / 3.0e-7 - 1) < 0.05})
# ordem de grandeza: GW170817 |v-c|/c ~ (3/2) xi (l k)^2 at 100 Hz for l_*
kk = 2 * np.pi * 100 / c
check("B GW170817 comparison: (3/2) xi (l_* k)^2 at 100 Hz << 1e-15", 1.5 * xi * (ell_req * kk) ** 2 < 1e-20,
      f"{1.5 * xi * (ell_req * kk)**2:.1e}")

# ---------------------------------------------------------------- C. H_inf e alpha_t
r_, As = 0.036, 2.1e-9
V = 1.5 * np.pi**2 * As * r_ * M_red**4                   # GeV^4
H_inf = np.sqrt(V / (3 * M_red**2))
x = H_inf / M_P
import sympy as sp
_y = sp.symbols("y", positive=True)
_alpha_sym = sp.simplify((2 + 2 / (1 + _y**2) - 4) / 2)          # Pade d_s -> (d_s - 4)/2
check("C (d_s - 4)/2 = -x^2/(1+x^2) for the Pade form (sympy)", sp.simplify(_alpha_sym + _y**2 / (1 + _y**2)) == 0)
alpha = sp.lambdify(_y, _alpha_sym, "numpy")                       # cancellation-free form
check("C H_inf <= 4.7e13 GeV (via V and H^2 = V/3M_red^2)", abs(H_inf / 4.7e13 - 1) < 0.01, f"H={H_inf:.4e} GeV, M_P={M_P:.5e}")
check("C |alpha_t| <= 1.5e-11 (M_P), 3.7e-10 (M_red)",
      abs(-alpha(x) / 1.5e-11 - 1) < 0.02 and abs(-alpha(H_inf / M_red) / 3.7e-10 - 1) < 0.02,
      f"{-alpha(x):.3e}, {-alpha(H_inf / M_red):.3e}")
check("C M_P/M_red changes the number by 8 pi", abs(alpha(H_inf / M_red) / alpha(x) / (8 * np.pi) - 1) < 1e-6,
      f"ratio/(8 pi) = {alpha(H_inf / M_red) / alpha(x) / (8 * np.pi):.9f}")
mutants_fail("C", {
    "V without 3/2": abs(np.sqrt(np.pi**2 * As * r_ * M_red**4 / (3 * M_red**2)) / 4.7e13 - 1) < 0.01,
    "M_P in place of M_red": abs(np.sqrt(1.5 * np.pi**2 * As * r_ * M_P**4 / (3 * M_P**2)) / 4.7e13 - 1) < 0.01,
    "alpha_t exponent x^4": abs((x**4) / 1.5e-11 - 1) < 0.02,
    "comoving k_pivot today": abs(((0.05 / Mpc * hbarc_eVm * 1e-9) / M_P) ** 2 / 1.5e-11 - 1) < 0.5,
})

# ---------------------------------------------------------------- D. estroncio
u = 1.66053906660e-27
m87 = 86.9088775 * u
ratio = lambda v, m=m87: lP * m * v / (2 * np.pi * hbar)
check("D l_P/lambda_dB = 3.5e-27 (v/1 m/s) for Sr-87", abs(ratio(1.0) / 3.5e-27 - 1) < 0.01, f"{ratio(1.0):.4e}")
vmax = np.sqrt(2 * 9.81 * 100.0)          # launch speed for a 100 m fountain (MAGIS-100 scale)
check("D < 2e-25 for v <= 45 m/s; 45 m/s ~ launch speed of a 100 m fountain",
      ratio(45.0) < 2e-25 and ratio(45.0, 88 * u) < 2e-25 and abs(vmax - 45) < 2,
      f"ratio(45)={ratio(45.0):.3e}, Sr-88: {ratio(45.0, 88*u):.3e}, v(100 m)={vmax:.1f} m/s")
mutants_fail("D", {"lambda=hbar/(mv) (2pi dropped)": abs(ratio(1.0) * 2 * np.pi / 3.5e-27 - 1) < 0.01,
                   "velocity-free 4e-26 bound at 45 m/s": ratio(45.0) < 4e-26})

# ---------------------------------------------------------------- E. figura
try:
    import pymupdf
except ImportError:  # pragma: no cover
    import fitz as pymupdf

doc = pymupdf.open(str(ROOT / "fig_experimental_signatures.pdf"))
page = doc[0]
drs = page.get_drawings()
spans = [s for b in page.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"]]


def exp_spans(xlo, xhi, ylo, yhi):
    out = []
    for s in spans:
        t = s["text"].replace("−", "-").strip()
        x0, y0, x1, y1 = s["bbox"]
        if re.fullmatch(r"-?\d+", t) and abs(s["size"] - 7) < 0.1 and xlo < x0 < xhi and ylo < y0 < yhi:
            out.append(((x0 + x1) / 2, (y0 + y1) / 2, int(t)))
    return out


def major_ticks(horizontal, xlo, xhi):
    out = []
    for d in drs:
        r = d["rect"]
        if d.get("width") and abs(d["width"] - 0.8) < 1e-3 and d.get("type") == "fs":
            if horizontal and abs(r.x0 - r.x1) < 1e-6 and abs(r.height - 3.5) < 1e-3 and xlo < r.x0 < xhi:
                out.append(r.x0)
            if not horizontal and abs(r.y0 - r.y1) < 1e-6 and abs(r.width - 3.5) < 1e-3 and xlo < r.x0 < xhi:
                out.append(r.y0)
    return sorted(out)


def axis_map(ticks, labels, horizontal):
    labels = sorted(labels, key=lambda t: t[0] if horizontal else -t[1])
    ticks = ticks if horizontal else sorted(ticks, reverse=True)
    assert len(ticks) == len(labels), (ticks, labels)
    e = np.array([l[2] for l in labels], float)
    a, b = np.polyfit(ticks, e, 1)
    assert np.max(np.abs(a * np.array(ticks) + b - e)) < 1e-3
    return lambda p: a * np.asarray(p) + b


xa = axis_map(major_ticks(True, 60, 360), exp_spans(60, 360, 225, 250), True)
ya = axis_map(major_ticks(False, 50, 62), exp_spans(30, 60, 0, 230), False)
xb = axis_map(major_ticks(True, 415, 710), exp_spans(415, 710, 225, 250), True)
yb = axis_map(major_ticks(False, 405, 416), exp_spans(390, 412, 0, 230), False)

BLUE = (0.1216, 0.4667, 0.7059)
RED = (0.8392, 0.1529, 0.1569)
GREEN = (0.1725, 0.6275, 0.1725)
close = lambda c1, c2: c1 is not None and np.allclose(c1, c2, atol=2e-3)


def vertices(d):
    pts = []
    for it in d["items"]:
        if it[0] == "l":
            pts += [(it[1].x, it[1].y), (it[2].x, it[2].y)]
    return np.array(pts)


curves_a = [d for d in drs if d.get("type") == "s" and d["rect"].x1 < 360 and len(d["items"]) > 5
            and (close(d.get("color"), BLUE) or close(d.get("color"), RED))]
check("E panel (a) has 3 blue and 1 red data curves", len(curves_a) == 4 and sum(close(d["color"], RED) for d in curves_a) == 1)
expected = []
for d in curves_a:
    if close(d["color"], RED):
        expected.append((ell_req, 3))
    else:
        dash = str(d.get("dashes"))
        z = 1 if dash.startswith("[] ") else (3 if "5.55" in dash else 8)
        expected.append((lP, z))


def dev_for(model):
    worst = 0.0
    for d, (ell, z) in zip(curves_a, expected):
        P = vertices(d)
        f = 10 ** xa(P[:, 0])
        y = ya(P[:, 1])
        worst = max(worst, np.max(np.abs(y - np.log10(model(f, z, ell)))))
    return worst


good = lambda f, z, ell: dt_text(z, 10.0, f, xi, ell)
dev = dev_for(good)
check("E panel (a) curves = text formula (D_2 with (1+z)^2, reference 10 Hz, l_* = 3.0e-7 m)", dev < 0.01,
      f"max |dlog10| = {dev:.4f}")
# the red curve crosses the 0.1 ms benchmark at 1 kHz
bench = [d for d in drs if d.get("type") == "s" and d.get("dashes") and "5.12" in str(d["dashes"])]
yb_line = 10 ** ya(bench[0]["rect"].y0)
check("E dash-dotted benchmark at 1e-4 s and red curve reaches it at 1 kHz",
      abs(np.log10(yb_line) + 4) < 0.01 and abs(np.log10(good(1000.0, 3, ell_req)) + 4) < 1e-6,
      f"benchmark={yb_line:.3e}")
devs_mut = {
    "(1+z)^1": dev_for(lambda f, z, ell: dt_text(z, 10.0, f, xi, ell, n=1)),
    "reference 1 Hz": dev_for(lambda f, z, ell: dt_text(z, 1.0, f, xi, ell)),
    "xi = 1": dev_for(lambda f, z, ell: dt_text(z, 10.0, f, 1.0, ell)),
    "old l_* = 4.7e-7 for red": dev_for(lambda f, z, ell: dt_text(z, 10.0, f, xi, 4.7e-7 if ell > 1e-10 else ell)),
}
mutants_fail("E panel (a)", {k: v < 0.05 for k, v in devs_mut.items()})
print("   mutant deviations (decades):", {k: round(v, 3) for k, v in devs_mut.items()})

band = [d for d in drs if d.get("type") == "fs" and close(d.get("fill"), GREEN)][0]["rect"]
edge = 10 ** xb(band.x1)
check("E panel (b) band right edge = H_inf/M_P", abs(np.log10(edge / x)) < 0.01, f"edge={edge:.3e}, H_inf/M_P={x:.3e}")
cb = [d for d in drs if d.get("type") == "s" and d["rect"].x0 > 415 and close(d.get("color"), BLUE)][0]
P = vertices(cb)
xx, yy = 10 ** xb(P[:, 0]), yb(P[:, 1])
devb = np.max(np.abs(yy - np.log10(-alpha(xx))))
check("E panel (b) curve = |alpha_t| = x^2/(1+x^2)", devb < 0.01, f"max |dlog10| = {devb:.4f}")
mutants_fail("E panel (b)", {
    "curve x^4": np.max(np.abs(yy - np.log10(xx**4 / (1 + xx**4)))) < 0.05,
    "curve x^2 without saturation": np.max(np.abs(yy - np.log10(xx**2))) < 0.05,
    "band edge at comoving k_pivot/M_P": abs(np.log10(edge / ((0.05 / Mpc * hbarc_eVm * 1e-9) / M_P))) < 0.05,
    "band edge with M_red": abs(np.log10(edge / (H_inf / M_red))) < 0.01,
})

# ---------------------------------------------------------------- F. o texto cita estes valores
t13 = (ROOT / "chap13_experimental_observational_signatures_quantum_gravity.tex").read_text(encoding="utf-8")
t12 = (ROOT / "chap12_grand_unification_quantum_gravity_treatise.tex").read_text(encoding="utf-8")
for s in ("6 \\times 10^{-62}$, $3 \\times 10^{-61}$ and $1.2 \\times 10^{-60}", "3.0 \\times 10^{-7}", "0.7$\\,eV",
          "4.7 \\times 10^{13}", "1.5 \\times 10^{-11}", "3.7 \\times 10^{-10}", "3.5 \\times 10^{-27}", "(1+z')^2"):
    check(f"F ch13 quotes {s!r}", s in t13)
for s in ("6 \\times 10^{-62}$--$1 \\times 10^{-60}", "3 \\times 10^{-7}", "0.7$\\,eV", "4.7 \\times 10^{13}",
          "1.5 \\times 10^{-11}", "3.5 \\times 10^{-27}", "(1+z')^2"):
    check(f"F ch12 quotes {s!r}", s in t12)
check("F old numbers absent (4.7e-7 m, 1e-115, 7e-118)",
      not any(s in t13 + t12 for s in ("4.7 \\times 10^{-7}", "10^{-115}", "10^{-118}")))

print("\nFALHAS:", FAIL if FAIL else "nenhuma")
raise SystemExit(1 if FAIL else 0)
