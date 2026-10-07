"""Def 6.1 / Thm 6.2 (Dixmier trace).  Oracle: direct singular values of the truncated operator M_f |D|^{-d}
in the Fourier basis on the torus (kernel k=0 removed), slope of S(N)=sum_{n<=N} mu_n against log N.
 (1) d=2, f=1: constant 2^{floor(d/2)} Omega_d / (d (2pi)^d) = 1/(2pi)  (lattice count).
 (2) d=1, f=1: constant 1/pi  (positive control of the d=1 normalisation).
 (3) d=1, f=cos(2 pi x): Thm 6.2 predicts (1/pi) * int f = 0, but Def 6.1 uses SINGULAR VALUES,
     which give (1/pi) * int |f| = 2/pi^2 = 0.2026.  Mismatch => Thm 6.2 false for sign-changing Phi(A)
     with the paper's own definition.
 (4) d=1, f = 0.3 + cos: Def gives (1/pi) int|f|, theorem gives 0.3/pi.
Negative control: mutating the constant (dropping 1/d or the 2^{floor(d/2)}) must disagree with (1)."""
import numpy as np, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
out = []; fails = 0
def log(s):
    out.append(s); print(s)
def slope(mu, lo, hi):
    mu = np.sort(mu)[::-1]; S = np.cumsum(mu)
    n = np.arange(1, len(mu) + 1)
    sel = (n >= lo) & (n <= hi)
    return np.polyfit(np.log(n[sel]), S[sel], 1)[0]
# (1) d=2 f=1
R = 400
k = np.arange(-R, R + 1); KX, KY = np.meshgrid(k, k)
r = np.sqrt(KX**2 + KY**2).ravel(); r = r[(r > 0) & (r <= R)]
mu = np.repeat(1 / (2 * np.pi * r)**2, 2)  # spinor dim 2
s2 = slope(mu, 2000, len(mu) // 2)
log("d=2 f=1: slope %.5f  vs paper constant 1/(2pi)=%.5f" % (s2, 1 / (2 * np.pi)))
fails += abs(s2 - 1 / (2 * np.pi)) > 0.01
for name, c in (("drop 1/d", 2 * 2 * np.pi / (4 * np.pi**2)), ("drop 2^{d/2}", 2 * np.pi / (2 * 4 * np.pi**2))):
    log("   NEG CTRL mutated constant (%s) = %.5f -> differs: %s" % (name, c, abs(s2 - c) > 0.01))
    fails += not abs(s2 - c) > 0.01
# d=1 operators
def op_svals(fhat, K):
    ks = np.array([j for j in range(-K, K + 1) if j != 0])
    Mf = np.zeros((len(ks), len(ks)), complex)
    for a, ka in enumerate(ks):
        for b, kb in enumerate(ks):
            Mf[a, b] = fhat.get(ka - kb, 0)
    T = Mf @ np.diag(1 / (2 * np.pi * np.abs(ks)))
    return np.linalg.svd(T, compute_uv=False)
K = 1500
for name, fhat, intf, intabs in (
        ("f=1", {0: 1.0}, 1.0, 1.0),
        ("f=cos(2pi x)", {1: 0.5, -1: 0.5}, 0.0, 2 / np.pi),
        ("f=0.3+cos(2pi x)", {0: 0.3, 1: 0.5, -1: 0.5}, 0.3, None)):
    if intabs is None:
        x = (np.arange(200000) + 0.5) / 200000; intabs = np.mean(np.abs(0.3 + np.cos(2 * np.pi * x)))
    sv = op_svals(fhat, K)
    s1 = slope(sv, 50, K // 2)
    log("d=1 %-18s slope %.4f | Thm 6.2 predicts (1/pi)int f = %.4f | (1/pi) int|f| = %.4f" % (name, s1, intf / np.pi, intabs / np.pi))
    if name == "f=1":
        fails += abs(s1 - 1 / np.pi) > 0.01
    else:
        fails += not (abs(s1 - intabs / np.pi) < 0.01 and abs(s1 - intf / np.pi) > 0.03)
txt = "\n".join(out)
open(os.path.join(HERE, "num_dixmier.out.txt"), "w", encoding="utf8").write(txt + "\nfailures=%d\n" % fails)
sys.exit(fails)
