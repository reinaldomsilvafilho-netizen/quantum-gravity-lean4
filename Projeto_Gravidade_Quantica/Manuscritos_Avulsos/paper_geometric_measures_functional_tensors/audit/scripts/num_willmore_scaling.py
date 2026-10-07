"""Thm 4.4(b): Phi_k = eps sin(k x1) sin(k x2) on [0,1]^2 (the d=3 statement is this times a unit x3-interval).
W = int H^2 |grad Phi| dx with H = -div(grad Phi/|grad Phi|) computed from exact derivatives:
   H = -(Lap Phi)/|g| + Hess(g,g)/|g|^3.
Direct quadrature (midpoint, M points per unit length, refinement M -> 2M -> 4M) for k = 8, 16, 32, 64.
Claim: W = Theta(eps k^3).  Check W/(eps k^3) ~ const; negative control: W/(eps k^2) must grow ~k.
Also Dirichlet energy int |grad Phi|^2 with eps=1/k must be Theta(1)."""
import numpy as np, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
out = []; fails = 0
def log(s):
    out.append(s); print(s)
def W_and_D(k, eps, M, chunk=256):
    x = (np.arange(M) + 0.5) / M
    W = 0.0; D = 0.0
    for s in range(0, M, chunk):
        X, Y = np.meshgrid(x[s:s + chunk], x, indexing="ij")
        sx, cx, sy, cy = np.sin(k * X), np.cos(k * X), np.sin(k * Y), np.cos(k * Y)
        fx = eps * k * cx * sy; fy = eps * k * sx * cy
        fxx = -eps * k * k * sx * sy; fyy = fxx; fxy = eps * k * k * cx * cy
        g2 = fx**2 + fy**2; g = np.sqrt(g2)
        H = -(fxx + fyy) / g + (fxx * fx**2 + 2 * fxy * fx * fy + fyy * fy**2) / g**3
        W += np.sum(H**2 * g); D += np.sum(g2)
    return W / M**2, D / M**2
ratios = []
for k in (8, 16, 32, 64):
    eps = 1.0 / k
    row = []
    for M in (k * 20, k * 40, k * 80):
        W, D = W_and_D(k, eps, M); row.append(W)
    log("k=%3d eps=1/k: W(M=20k,40k,80k) = %s ; W/(eps k^3) = %.4f ; W/(eps k^2) = %.3f ; Dirichlet = %.4f" % (k, ["%.2f" % w for w in row], row[-1] / (eps * k**3), row[-1] / (eps * k**2), D))
    ratios.append(row[-1] / (eps * k**3))
spread = (max(ratios) - min(ratios)) / np.mean(ratios)
log("relative spread of W/(eps k^3): %.3f (Theta(eps k^3) confirmed if small)" % spread)
fails += spread > 0.1
txt = "\n".join(out)
open(os.path.join(HERE, "num_willmore_scaling.out.txt"), "w", encoding="utf8").write(txt + "\nfailures=%d\n" % int(fails))
sys.exit(int(fails))
