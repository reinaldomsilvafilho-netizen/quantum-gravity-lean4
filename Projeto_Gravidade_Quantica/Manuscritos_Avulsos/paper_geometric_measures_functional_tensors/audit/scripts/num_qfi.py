"""Thm 7.2 (QFI volume).
 (1) eq (7.6): paper writes g_{mu nu} = (1/2) sum 2 Re(<i|d_mu rho|j><j|d_nu rho|i>)/(l_i+l_j) for the definition
     g = (1/2) Tr(rho {L_mu, L_nu}).  Oracle A: SLD from scipy solve_sylvester. Oracle B: Bures root-fidelity
     expansion 1 - F(rho, rho + t d rho) ~ g t^2 / 8.  We find the true value is 2 * sum Re(...)/(l_i+l_j) (factor 2).
 (2) Local-tex Thm 7.2(b) 'Vol=0 iff rho constant': counterexample d=2, rho depends on x1 only -> det g == 0, rho non-constant.
 (3) 'constant modulo unitary gauge U(x)': rho(x) = U(x) rho0 U(x)^dag has g != 0, so Vol>0: gauge-orbit is NOT zero volume.
 (4) Zenodo Thm 7.2 adds 'd_mu rho linearly independent' at every x: then det g > 0 everywhere and (b) is vacuous.
Negative control: mutated formula without the factor 2 must disagree with both oracles (it does: that is the finding),
and the correct formula must agree with both."""
import numpy as np, os, sys
from scipy.linalg import solve_sylvester, sqrtm, expm
HERE = os.path.dirname(os.path.abspath(__file__))
out = []; fails = 0
def log(s):
    out.append(s); print(s)
rng = np.random.default_rng(7)
def rand_rho(n):
    G = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)); r = G @ G.conj().T + 0.3 * np.eye(n); return r / np.trace(r).real
def rand_herm_traceless(n):
    H = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)); H = (H + H.conj().T) / 2; return H - np.trace(H) / n * np.eye(n)
def sld(rho, drho):
    return solve_sylvester(rho, rho, 2 * drho)
def g_def(rho, d1, d2):
    L1, L2 = sld(rho, d1), sld(rho, d2)
    return 0.5 * np.trace(rho @ (L1 @ L2 + L2 @ L1)).real
def g_paper(rho, d1, d2, factor):
    lam, U = np.linalg.eigh(rho); A = U.conj().T @ d1 @ U; B = U.conj().T @ d2 @ U
    S = sum((A[i, j] * B[j, i]).real / (lam[i] + lam[j]) for i in range(len(lam)) for j in range(len(lam)))
    return factor * S   # paper: (1/2)*2 = 1 ; correct: 2
def bures(rho, d1, t=1e-4):
    s = rho + t * d1
    sr = sqrtm(rho); F = np.trace(sqrtm(sr @ s @ sr)).real
    return 8 * (1 - F) / t**2
for trial in range(5):
    n = 4; rho = rand_rho(n); d1 = rand_herm_traceless(n) * 0.1
    a = g_def(rho, d1, d1); b = bures(rho, d1); p = g_paper(rho, d1, d1, 1.0); c = g_paper(rho, d1, d1, 2.0)
    log("trial %d: oracle SLD %.6f | oracle Bures %.6f | paper(7.6) %.6f | 2x paper %.6f" % (trial, a, b, p, c))
    fails += not (abs(a - c) < 1e-8 * max(1, abs(a)) and abs(a - b) < 1e-3 * abs(a) and abs(a - p) > 0.4 * abs(a))
# (2) counterexample to local (b)
def rho_x(x1, x2):
    return np.diag([0.5 + 0.25 * np.sin(x1), 0.5 - 0.25 * np.sin(x1)]).astype(complex)
h = 1e-5; x1, x2 = 0.3, 0.7
d1 = (rho_x(x1 + h, x2) - rho_x(x1 - h, x2)) / (2 * h); d2 = (rho_x(x1, x2 + h) - rho_x(x1, x2 - h)) / (2 * h)
r = rho_x(x1, x2)
G = np.array([[g_def(r, d1, d1), g_def(r, d1, d2)], [g_def(r, d2, d1), g_def(r, d2, d2)]])
log("counterexample (local-tex 7.2b): rho depends on x1 only; g=%s det=%.3e ; rho non-constant (d1 rho norm %.3f) -> Vol=0 but rho not constant" % (np.round(G, 4).tolist(), np.linalg.det(G), np.linalg.norm(d1)))
fails += not (abs(np.linalg.det(G)) < 1e-10 and np.linalg.norm(d1) > 0.1)
# (3) gauge orbit
rho0 = rand_rho(3); H1 = rand_herm_traceless(3); H2 = rand_herm_traceless(3)
def rho_g(x1, x2):
    U = expm(1j * (x1 * H1 + x2 * H2)); return U @ rho0 @ U.conj().T
d1 = (rho_g(x1 + h, x2) - rho_g(x1 - h, x2)) / (2 * h); d2 = (rho_g(x1, x2 + h) - rho_g(x1, x2 - h)) / (2 * h); r = rho_g(x1, x2)
G = np.array([[g_def(r, d1, d1), g_def(r, d1, d2)], [g_def(r, d2, d1), g_def(r, d2, d2)]])
log("gauge orbit rho=U(x) rho0 U(x)^dag: det g = %.4f > 0 -> 'constant modulo gauge' does NOT give Vol=0" % np.linalg.det(G))
fails += not np.linalg.det(G) > 1e-6
txt = "\n".join(out)
open(os.path.join(HERE, "num_qfi.out.txt"), "w", encoding="utf8").write(txt + "\nfailures=%d\n" % int(fails))
sys.exit(int(fails))
