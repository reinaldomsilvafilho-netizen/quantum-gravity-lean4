"""Cap. 13, reauditoria cega: le os vetores de fig_experimental_signatures.pdf
(sem usar o script gerador) e compara as curvas com as formulas do texto.

Painel (a): curvas azuis (l_P, z=1,3,8) e vermelha (l=4.7e-7 m, z=3), 'relativo a 1 Hz'.
  Compara com Dt = 6 pi^2 xi l^2 D_n(z) (f^2 - 1)/c^3, n=1 (texto) e n=2 (correto).
Painel (b): faixa verde 'CMB scales' vs faixa fisica ell=2..4000.
Controle negativo: a hipotese n=2 deve falhar nas curvas se elas foram geradas com n=1
  (e vice-versa), com discrepancia >> precisao de leitura.
"""
import re
import zlib
import numpy as np
from scipy.integrate import quad

PDF = __file__.replace("\\", "/").split("/audit/")[0] + "/fig_experimental_signatures.pdf"
raw = open(PDF, "rb").read()
T = max((zlib.decompress(m.group(1)).decode("latin1")
         for m in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.S)
         if m.group(1)[:2] in (b"x\x9c", b"x\xda", b"x^")), key=len)


def tick_labels(axis_x0, axis_x1, horizontal):
    """Extrai ticks maiores (comprimento 3.5) e o expoente do rotulo 10^e."""
    out = []
    if horizontal:
        pat = re.compile(r"([\d.]+) 43\.884687 m\n\1 40\.384687 l\n\nB\n1 w\nq\n(.*?)ET", re.S)
    else:
        pat = re.compile(rf"{axis_x0} ([\d.]+) m\n{axis_x1} \1 l\n\nB\n1 w\nq\n(.*?)ET", re.S)
    for m in pat.finditer(T):
        pos = float(m.group(1))
        body = m.group(2)
        small = body.split("/F1 10 Tf")[1]
        digits = "".join(re.findall(r"\((\d)\) Tj", small.split("4.13 Td")[1]))
        neg = re.search(r"/F3 7 Tf\n\(.\) Tj", small, re.S) is not None  # glifo de menos (fonte F3)
        out.append((pos, (-1 if neg else 1) * int(digits)))
    return out


def fit(ticks):
    p = np.array([t[0] for t in ticks]); e = np.array([t[1] for t in ticks])
    a, b = np.polyfit(p, e, 1)
    assert np.max(np.abs(a * p + b - e)) < 1e-3
    return lambda pos: a * pos + b


xa = fit([t for t in tick_labels(None, None, True) if t[0] < 360])
xb = fit([t for t in tick_labels(None, None, True) if t[0] > 400])
ya = fit(tick_labels("61.4", "57.9", False))

# polilinhas apos cada troca de cor
curves = []
for m in re.finditer(r"([\d.]+\s+[\d.]+\s+[\d.]+) RG[ \n]/DeviceRGB\s+cs\n+((?:-?[\d.]+ -?[\d.]+ [ml]\n)+)", T):
    col = " ".join(m.group(1).split())
    pts = np.array([[float(v) for v in ln.split()[:2]] for ln in m.group(2).strip().split("\n")])
    curves.append((col, pts))

c = 299792458.0; hbar = 1.054571817e-34; G = 6.67430e-11
Mpc = 3.0856775814913673e22; lP = np.sqrt(hbar * G / c**3); H0 = 70e3 / Mpc
E = lambda z: np.sqrt(0.3 * (1 + z) ** 3 + 0.7)
D = lambda z, n: c / H0 * quad(lambda x: (1 + x) ** n / E(x), 0, z)[0]
model = lambda f, z, ell, n: 6 * np.pi**2 * 0.5 * ell**2 / c**3 * D(z, n) * (f**2 - 1.0)

labels = [(lP, 1), (lP, 3), (lP, 8), (4.7e-7, 3)]
panel_a = [cv for cv in curves if cv[1][:, 0].max() < 360 and len(cv[1]) > 5]
print(f"{len(panel_a)} curvas no painel (a)")
res = {1: [], 2: []}
for (col, pts), (ell, z) in zip(panel_a, labels):
    sel = pts[(pts[:, 1] > 44) & (10 ** xa(pts[:, 0]) > 2)]
    f = 10 ** xa(sel[:, 0]); y = ya(sel[:, 1])
    for n in (1, 2):
        dev = np.max(np.abs(y - np.log10(model(f, z, ell, n))))
        res[n].append(dev)
    print(f" cor {col[:6]} l={ell:.2e} z={z}: max|dlog10| vs n=1: {res[1][-1]:.3f} ; vs n=2: {res[2][-1]:.3f}")
assert max(res[1]) < 0.02, "curvas nao seguem a formula do texto"
assert max(res[2]) > 0.1   # controle negativo: a formula correta (1+z)^2 nao e a plotada

# painel (b)
g = re.search(r"0\.6274509804 0\.1725490196 rg\n\n([\d.]+) [\d.]+ m\n([\d.]+) [\d.]+ l", T)
lo, hi = 10 ** xb(float(g.group(1))), 10 ** xb(float(g.group(2)))
MP_GeV = 1.2209e19; hbarc = 1.97327e-16  # GeV m
to_kMpc = lambda x: x * MP_GeV / hbarc * Mpc
print(f"faixa verde: k/M_P in [{lo:.1e}, {hi:.1e}]  = k in [{to_kMpc(lo):.1e}, {to_kMpc(hi):.1e}] Mpc^-1")
print(f"|alpha_t| na borda direita da faixa: {hi**2:.0e}")
phys = (2 / 13900.0, 4000 / 13900.0)
print(f"CMB fisico ell=2..4000: k in [{phys[0]:.1e}, {phys[1]:.1e}] Mpc^-1")
assert to_kMpc(hi) > 100 * phys[1]
print("OK")
