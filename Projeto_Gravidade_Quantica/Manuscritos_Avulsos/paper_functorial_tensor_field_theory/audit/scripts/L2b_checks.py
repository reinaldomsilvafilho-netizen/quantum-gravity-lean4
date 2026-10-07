"""L2b re-check of round-2 fixes (functorial tensor paper).

Independent of round2_checks.py: different test fields, different oracles.
Each check has an oracle and a negative control. Fixed seed. Exit code = failures.
"""
import sys, re, json, urllib.request, urllib.error
import numpy as np
import sympy as sp

rng = np.random.default_rng(20261006)
fails = 0
out = []


def report(name, ok, info=""):
    global fails
    if not ok:
        fails += 1
    line = f"[{'PASS' if ok else 'FAIL'}] {name}: {info}"
    out.append(line)
    print(line)


# ---------------- B1: A7 display, two routes ----------------
t, N0, Lam = sp.symbols('t N0 Lambda', positive=True)
a = sp.Function('a')(t)
X = sp.symbols('x1:4')
coords = (t,) + X
g = sp.diag(-N0**2, a**2, a**2, a**2)
gi = g.inv()
n = 4
Gam = [[[sum(gi[l, m] * (sp.diff(g[m, i], coords[j]) + sp.diff(g[m, j], coords[i])
                         - sp.diff(g[i, j], coords[m])) for m in range(n)) / 2
         for j in range(n)] for i in range(n)] for l in range(n)]


def ricci(i, j):
    return sp.simplify(sum(sp.diff(Gam[l][i][j], coords[l]) for l in range(n))
                       - sum(sp.diff(Gam[l][i][l], coords[j]) for l in range(n))
                       + sum(Gam[l][l][m] * Gam[m][i][j] for l in range(n) for m in range(n))
                       - sum(Gam[l][j][m] * Gam[m][i][l] for l in range(n) for m in range(n)))


Ric = sp.Matrix(4, 4, lambda i, j: ricci(i, j))
Rs = sp.simplify(sum(gi[i, j] * Ric[i, j] for i in range(n) for j in range(n)))
Gtt = sp.simplify(Ric[0, 0] - Rs * g[0, 0] / 2)
nn_lhs = sp.simplify((Gtt + Lam * g[0, 0]) / N0**2)   # n^t = 1/N0
paper = 3 * sp.diff(a, t)**2 / (N0**2 * a**2) - Lam
report("B1 symbolic: n.n.(G+Lambda g) equals paper display", sp.simplify(nn_lhs - paper) == 0,
       f"diff {sp.simplify(nn_lhs - paper)}")
# independent numerical route: Gauss equation for the Hamiltonian constraint
# 2 G(n,n) = R(h) + K^2 - K_ij K^ij, flat slices, K_ij = a adot / N0 delta_ij
av, adv, N0v, Lv = 0.7, 0.31, 1.3, 0.45
Kij = av * adv / N0v * np.eye(3)
hinv = np.eye(3) / av**2
Kmix = hinv @ Kij
K = np.trace(Kmix)
Gnn_gauss = 0.5 * (0.0 + K**2 - np.trace(Kmix @ Kmix))
num_paper = 3 * adv**2 / (N0v**2 * av**2) - Lv
report("B1 Gauss-equation oracle matches display", abs(Gnn_gauss - Lv - num_paper) < 1e-13,
       f"{Gnn_gauss - Lv:.12f} vs {num_paper:.12f}")
old = 3 * adv**2 / (N0v**2 * av**2)
report("B1 control: display without -Lambda fails", abs(Gnn_gauss - Lv - old) > 1e-3,
       f"gap {Gnn_gauss - Lv - old:.3f}")
# conclusion: at the ends (adot=0), constraint holds iff Lambda = 0
report("B1 conclusion: at ends n.n.(G+Lg) = -Lambda", sp.simplify(paper.subs(sp.diff(a, t), 0) + Lam) == 0, "")


# ---------------- common QFI tools ----------------
def qfi_fid(T, x, h=1e-4):
    """QFI from fidelity: 1-|<T(x),T(x+dx)>|^2 ~ (1/4) h_ij dx^i dx^j; oracle independent of eq. (2.1)."""
    d = len(x)
    def F(dx):  # symmetrised: odd orders cancel, error O(h^2)
        return 1 - (abs(np.vdot(T(x), T(x + dx)))**2 + abs(np.vdot(T(x), T(x - dx)))**2) / 2
    G = np.zeros((d, d))
    E = np.eye(d) * h
    for i in range(d):
        G[i, i] = 4 * F(E[i]) / h**2
    for i in range(d):
        for j in range(i + 1, d):
            G[i, j] = G[j, i] = 2 * (F(E[i] + E[j]) - F(E[i]) - F(E[j])) / h**2
    return G


def qfi_formula(T, x, h=1e-6):
    d = len(x)
    v = T(x)
    P = np.eye(len(v)) - np.outer(v, v.conj())
    D = [(T(x + h * e) - T(x - h * e)) / (2 * h) for e in np.eye(d)]
    return np.array([[4 * np.real(np.vdot(D[i], P @ D[j])) for j in range(d)] for i in range(d)])


# ---------------- B2: M11 with a different datum (random entangled field in C^5) ----------------
A = [rng.normal(size=(5, 5)) + 1j * rng.normal(size=(5, 5)) for _ in range(3)]
A = [(M + M.conj().T) / 2 for M in A]
v0 = rng.normal(size=5) + 1j * rng.normal(size=5)
v0 /= np.linalg.norm(v0)
from scipy.linalg import expm


def Tfield(x, t):
    # x in R^3 (chart), t-dependent via a sitting smooth path c(t)
    U = expm(1j * (x[0] * A[0] + x[1] * A[1] + (x[2] + 0.3 * c(t)) * A[2]))
    return U @ v0


def sstep(s):
    s = np.clip(s, 0, 1)
    f = lambda u: np.where(u > 0, np.exp(-1 / np.maximum(u, 1e-300)), 0.0)
    return f(s) / (f(s) + f(1 - s))


L, eps = 2.0, 0.3
c = lambda tt: float(sstep((tt - eps) / (L - 2 * eps)))
b = lambda tt: float(np.pi * sstep((tt - eps) / 0.2) * sstep((L - eps - tt) / 0.2))
x0 = rng.uniform(-1, 1, 3)
Tp = lambda x, tt: np.exp(1j * b(tt)) * Tfield(x, tt)
ends = [0, 0.1, eps, L - eps, L - 0.05, L]
ed = max(np.linalg.norm(Tp(x0, tt) - Tfield(x0, tt)) for tt in ends)
report("B2 T' = T on sitting intervals (same Hom-set)", ed == 0.0, f"max {ed:.1e}")
md = np.linalg.norm(Tp(x0, L / 2) - Tfield(x0, L / 2))
report("B2 b(L/2)=pi and ||T'-T|| = 2 at L/2", abs(b(L / 2) - np.pi) < 1e-15 and abs(md - 2) < 1e-12, f"{md:.15f}")
dh = max(np.max(np.abs(qfi_fid(lambda x: Tp(x, tt), x0) - qfi_fid(lambda x: Tfield(x, tt), x0)))
         for tt in np.linspace(0, L, 9))
hscale = np.max(np.abs(qfi_fid(lambda x: Tfield(x, L / 2), x0)))
report("B2 h(t) unchanged (fidelity oracle)", dh < 1e-6 * max(1, hscale), f"max dh {dh:.1e}, |h| {hscale:.2f}")
mineig = min(np.linalg.eigvalsh(qfi_formula(lambda x: Tp(x, tt), x0)).min() for tt in np.linspace(0, L, 9))
report("B2 T'(.,t) projectively immersed (min eig > 0)", mineig > 1e-3, f"min eig {mineig:.3f}")
# control: fixed unitary changes the endpoints (different hom-set)
Ufix = expm(1j * A[0] * 0.7)
cd = np.linalg.norm(Ufix @ Tfield(x0, 0) - Tfield(x0, 0))
report("B2 control: fixed unitary moves the endpoint", cd > 1e-2, f"{cd:.3f}")
# control: a non-global (relative) t-phase does change h
Pm = np.diag([1, 0, 0, 0, 0]).astype(complex)
Tr = lambda x: expm(1j * x[0] * Pm) @ Tfield(x, L / 2)  # x-dependent relative phase
cr = np.max(np.abs(qfi_fid(Tr, x0) - qfi_fid(lambda x: Tfield(x, L / 2), x0)))
report("B2 control: relative phase changes h", cr > 1e-2, f"{cr:.3f}")


# ---------------- B3: Lemma 2.8 ----------------
# (a) random smooth fields into C^2 and C^1: QFI singular. Oracle: rank of real 3x(2dimP) projected Jacobian.
def rand_field(dim):
    W = [rng.normal(size=(dim, 4)) + 1j * rng.normal(size=(dim, 4)) for _ in range(3)]
    w0 = rng.normal(size=dim) + 1j * rng.normal(size=dim)
    def T(x):
        f = w0 + sum(np.sin(x[k] * np.arange(1, 5) + k) @ W[k].T for k in range(3))
        return f / np.linalg.norm(f)
    return T


ratios2, ratios1, ratios3 = [], [], []
for _ in range(20):
    x = rng.uniform(-2, 2, 3)
    for dim, store in ((1, ratios1), (2, ratios2), (3, ratios3)):
        e = np.linalg.eigvalsh(qfi_formula(rand_field(dim), x))
        store.append(e[0] / max(e[-1], 1e-300) if e[-1] > 1e-12 else 0.0)
report("B3a dim H=2: QFI singular at all 20 samples", max(ratios2) < 1e-7, f"max eig ratio {max(ratios2):.1e}")
report("B3a dim H=1: QFI singular", max(ratios1) < 1e-7, f"max {max(ratios1):.1e}")
report("B3a control: dim H=3 random field is immersed", min(ratios3) > 1e-4, f"min ratio {min(ratios3):.1e}")


# (b) construction with an immersion whose radial direction is tangent; e0 is essential
def iota(x):  # immersion near 0 of R^3 into R^3, with d iota(d1) parallel to iota
    return (2 + x[0]) * np.array([1.0, x[1], x[2]])


def make_T(with_e0):
    def T(x):
        f = np.concatenate([[1.0 if with_e0 else 0.0], iota(x)]).astype(complex)
        return f / np.linalg.norm(f)
    return T


def h_analytic(x):
    f = np.concatenate([[1.0], iota(x)])
    J = np.zeros((4, 3))
    J[1:, 0] = [1.0, x[1], x[2]]
    J[2, 1] = 2 + x[0]
    J[3, 2] = 2 + x[0]
    nf = np.linalg.norm(f)
    u = f / nf
    PJ = J - np.outer(u, u @ J)
    return 4 * PJ.T @ PJ / nf**2


errs, mins, mins0 = [], [], []
for _ in range(15):
    x = rng.uniform(-0.5, 0.5, 3)
    hn = qfi_fid(make_T(True), x)
    errs.append(np.max(np.abs(hn - h_analytic(x))))
    mins.append(np.linalg.eigvalsh(hn).min())
    mins0.append(np.linalg.eigvalsh(qfi_formula(make_T(False), x)).min())
report("B3b construction QFI = analytic formula (fidelity oracle)", max(errs) < 1e-5, f"max err {max(errs):.1e}")
xr = np.array([0.2, -0.3, 0.4])
ers = [np.max(np.abs(qfi_fid(make_T(True), xr, h=hh) - h_analytic(xr))) for hh in (4e-3, 2e-3, 1e-3)]
rates = [np.log2(ers[0] / ers[1]), np.log2(ers[1] / ers[2])]
report("B3b fidelity-oracle convergence rate ~2", all(1.7 < r < 2.3 for r in rates), f"errs {ers}, rates {rates}")
report("B3b construction immersed (min eig > 0)", min(mins) > 1e-3, f"min eig {min(mins):.3f}")
report("B3b control: without e0 the field is not immersed", max(mins0) < 1e-7, f"max min-eig {max(mins0):.1e}")



# ---------------- B4: N4 ----------------
s = np.linspace(0, 1, 200001)
worst = 0
gmin = 9
for s0 in np.linspace(0.001, 0.999, 999):
    ap = 1 + 0.5 * ((1 - 2 * s) * (s - s0) + s * (1 - s))      # derivative of alpha, original form
    closed = min(1 - s0 / 2, (1 + s0) / 2)
    worst = max(worst, abs(ap.min() - closed))
    gmin = min(gmin, ap.min())
report("B4 min alpha' = min(1-s0/2,(1+s0)/2) on [0,1]", worst < 1e-12, f"max err {worst:.1e}")
report("B4 infimum over s0 is 1/2, never attained", 0.5 < gmin < 0.5 + 1e-3, f"min {gmin:.6f}")
ap = 1 + 0.5 * ((1 - 2 * s) * (s - 0.5) + s * (1 - s))
integ = np.sum((ap[1:] + ap[:-1]) / 2) * (s[1] - s[0])
report("B4 s0=1/2: alpha' in [3/4,9/8], int = 1",
       abs(ap.min() - 0.75) < 1e-12 and abs(ap.max() - 1.125) < 1e-9 and abs(integ - 1) < 1e-9,
       f"[{ap.min():.6f},{ap.max():.6f}], int {integ:.12f}")
ap_s = sp.expand(sp.diff(sp.Symbol('s') + sp.Rational(1, 2) * sp.Symbol('s') * (1 - sp.Symbol('s')) * (sp.Symbol('s') - sp.Symbol('s0')), sp.Symbol('s')))
paper_ap = sp.expand(1 + sp.Rational(1, 2) * (-3 * sp.Symbol('s')**2 + 2 * (1 + sp.Symbol('s0')) * sp.Symbol('s') - sp.Symbol('s0')))
report("B4 paper's expanded alpha' is the derivative (sympy)", sp.simplify(ap_s - paper_ap) == 0, "")
ap01 = 1 + 0.5 * ((1 - 2 * s) * (s - 0.01) + s * (1 - s))
report("B4 control: old-style bound 0.6 is violated (s0=0.01)", ap01.min() < 0.6, f"{ap01.min():.4f}")


# ---------------- B5: Crossref Choquet-Bruhat ----------------
def cr(doi):
    try:
        with urllib.request.urlopen("https://api.crossref.org/works/" + doi, timeout=30) as r:
            return json.load(r)["message"]
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return str(e)


m = cr("10.1093/acprof:oso/9780199230723.001.0001")
okb = isinstance(m, dict) and m["title"][0] == "General Relativity and the Einstein Equations" \
    and m["author"][0]["family"] == "Choquet-Bruhat" and "9780199230723" in m.get("ISBN", [])
report("B5 book DOI resolves; title, author, ISBN match", okb, str(m.get("issued")) if isinstance(m, dict) else str(m))
ch = cr("10.1093/acprof:oso/9780199230723.003.0006")
okc = isinstance(ch, dict) and ch["title"][0] == "Local Cauchy Problem" and ch.get("page") == "142-178"
abst = ch.get("abstract", "") if isinstance(ch, dict) else ""
report("B5 Ch. VI = 'Local Cauchy Problem' pp.142-178; abstract lists wave gauges, local existence, field sources",
       okc and "local existence" in abst and "field sources" in abst and "wave gauges" in abst, "")
report("B5 Crossref gives no theorem number (abstract has none)", not re.search(r"Theorem\s*\d", abst), "")
fake = cr("10.1093/acprof:oso/9780199230723.003.9999")
report("B5 control: fake chapter DOI is 404", fake == 404, str(fake))

# ---------------- B6: declarations block ----------------
base = r"C:/Users/monar/Documents/antigravity/resilient-turing/Projeto_Gravidade_Quantica/"
std = open(base + "_staging/DECLARACOES_PADRAO_ARTIGOS.tex", encoding="utf8").read()
tex = open(base + "Manuscritos_Avulsos/paper_functorial_tensor_field_theory/paper_functorial_tensor_field_theory.tex",
           encoding="utf8").read()
std_body = std[std.index(r"\section*{Declarations}"):]
std_body = std_body.replace("[paper/volume]", "paper").replace("[If Lean files exist:] ", "")
norm = lambda z: " ".join(z.split())
blk = tex[tex.index(r"\section*{Declarations}"):tex.index(r"\raggedright", tex.index(r"\section*{Declarations}"))]
report("B6 declarations block = standard (paper variant)", norm(blk) == norm(std_body),
       f"len {len(norm(blk))} vs {len(norm(std_body))}")
report("B6 control: mutated block differs", norm(blk.replace("CAPES", "CNPq")) != norm(std_body), "")
report("B6 no GitHub URL / old AI statement left in .tex",
       "github" not in tex.lower() and "solely for" not in tex, "")

# ---------------- B7: notes ----------------
pdir = base + "Manuscritos_Avulsos/paper_functorial_tensor_field_theory/"
corr = open(pdir + "CORRECTIONS_2026-10-06.md", encoding="utf8").read()
zen = open(pdir + "ZENODO_DESCRIPTION.md", encoding="utf8").read()
for nm, txt in (("CORRECTIONS", corr), ("ZENODO_DESCRIPTION", zen)):
    report(f"B7 {nm}: no GitHub claim", "github" not in txt.lower(), "")
    report(f"B7 {nm}: no 'pending'", "pending" not in txt.lower(), "")
report("B7 ZENODO: no 'dagger-compact'", "dagger-compact" not in zen.lower(), "")
report("B7 CORRECTIONS item 9 uses e^{ib(t)} argument", "e^{ib(t)}" in corr and "fixed unitary would not do" in corr, "")
desc = zen.split("## Description")[1].split("## Keywords")[0]
nw = len(re.findall(r"[A-Za-z0-9\u00C0-\u024F'’\-–=≥·‖²]+", desc.split("\n", 1)[1]))
report("B7 description <= 250 words", nw <= 250, f"{nw} words")

open(__file__.replace(".py", ".out.txt"), "w", encoding="utf8").write("\n".join(out) + f"\nfailures: {fails}\n")
sys.exit(fails)
