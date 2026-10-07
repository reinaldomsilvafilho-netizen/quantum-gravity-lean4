"""Theorem 3.4 (Isospectral Separation). Independent checks:
 (1) spectra of A,B (numpy eigvalsh vs claimed closed form);
 (2) beta_1 of superlevel sets X_t of the step realization on a fine pixel grid, computed independently by
     counting bounded components of the complement (planar Alexander duality) with scipy.ndimage.label;
 (3) H1 bar count N_1 for B with ring heights perturbed to (2,2.2,2.4,...): paper claims 'multiple distinct bars',
     hence E_pers(B)>0; we count bars by scanning t;
 (4) mollified step realization (Gaussian blur): L_infinity distance to the step function does NOT go to 0
     (paper claims ||Phi_eps - Phi||_inf -> 0).
Negative control: a matrix with TWO interior low cells on a 4x4 grid must give beta_1 = 2 (counter works)."""
import numpy as np, sys, os
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__))
out = []; fails = 0
def log(s):
    out.append(s); print(s)
B = np.array([[2, 2, 2], [2, 0, 2], [2, 2, 2]], float)
P = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]], float)
A = P @ B @ P.T
log("A=\n%s" % A)
ev = np.sort(np.linalg.eigvalsh(B)); claim = np.sort([2 + 2 * np.sqrt(3), 2 - 2 * np.sqrt(3), 0])
log("eig B %s claim %s match %s; eig A %s" % (ev, claim, np.allclose(ev, claim), np.sort(np.linalg.eigvalsh(A))))
fails += not np.allclose(ev, claim)
log("||A||_F^2=%g ||B||_F^2=%g" % ((A**2).sum(), (B**2).sum()))

def step_image(M, res):
    n = M.shape[0]
    idx = np.minimum((np.arange(res) * n) // res, n - 1)
    return M[np.ix_(idx, idx)]

def beta1(mask):
    # holes = components of complement not touching the border (4-connectivity complement vs 8-connectivity set)
    comp = ~mask
    lab, nlab = ndimage.label(comp, structure=[[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    return nlab - len(border)

def bars_H1(img, ts):
    # track beta_1 as t decreases; count births (increments) - crude bar counting
    b = [beta1(img >= t) for t in ts]
    births = []
    prev = 0
    for t, x in zip(ts, b):
        if x > prev:
            births += [t] * (x - prev)
        prev = x
    return b, births

res = 300
ts = np.linspace(2.6, -0.05, 400)
for name, M in (("B", B), ("A", A)):
    img = step_image(M, res)
    b, births = bars_H1(img, ts)
    log("%s: beta1(X_t) for t in (0,2]: %s ; H1 births at %s" % (name, sorted(set(b[i] for i, t in enumerate(ts) if 0 < t <= 2)), births))
# expected: B -> {1}, A -> {0}
bB = beta1(step_image(B, res) >= 1.0); bA = beta1(step_image(A, res) >= 1.0)
fails += not (bB == 1 and bA == 0)
# (3) perturbed ring heights
Bp = np.array([[2.0, 2.2, 2.4], [2.4, 0.0, 2.2], [2.2, 2.0, 2.4]])
b, births = bars_H1(step_image(Bp, res), np.linspace(2.6, -0.05, 800))
log("perturbed ring B' (heights 2,2.2,2.4): number of H1 bars N_1 = %d (births %s) -> E_pers^(1)(B') = 0 since a single bar" % (len(births), births))
# random perturbations of ring
rng = np.random.default_rng(0); maxbars = 0
for trial in range(200):
    R = 2 + rng.random((3, 3)); R[1, 1] = rng.random() * 0.5
    R = (R + R.T) / 2
    _, br = bars_H1(step_image(R, 150), np.linspace(3.1, -0.05, 400))
    maxbars = max(maxbars, len(br))
log("200 random symmetric 3x3 with low centre: max number of H1 bars = %d (so E_pers^(1) = 0 always)" % maxbars)
# negative control: 4x4 with two separated interior low cells -> beta1 = 2
C = 2 * np.ones((5, 5)); C[1, 1] = 0; C[3, 3] = 0
bc = beta1(step_image(C, 250) >= 1)
log("NEGATIVE CONTROL two interior holes: beta1 = %d (must be 2)" % bc); fails += bc != 2
# (4) mollification does not converge in L_inf
for eps in (0.05, 0.02, 0.01, 0.005):
    img = step_image(B, 1200)
    sm = ndimage.gaussian_filter(img, sigma=eps * 1200, mode="nearest")
    log("eps=%.3f  ||Phi_eps - Phi||_inf = %.3f (paper: ->0)" % (eps, np.abs(sm - img).max()))
    # check smooth version topology anyway
    smA = ndimage.gaussian_filter(step_image(A, 1200), sigma=eps * 1200, mode="nearest")
    bb = sorted(set(beta1(sm[::4, ::4] >= t) for t in np.linspace(0.05, 1.95, 60)))
    ba = sorted(set(beta1(smA[::4, ::4] >= t) for t in np.linspace(0.05, 1.95, 60)))
    log("    mollified: beta1 values over t in [0.05,1.95]: B %s, A %s" % (bb, ba))
txt = "\n".join(out)
open(os.path.join(HERE, "num_isospectral_persistence.out.txt"), "w", encoding="utf8").write(txt + "\nfailures=%d\n" % fails)
sys.exit(fails)
