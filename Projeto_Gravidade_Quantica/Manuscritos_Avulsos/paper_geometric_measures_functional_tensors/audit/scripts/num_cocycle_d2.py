"""Thm 6.3 (Zenodo only) / Sec 6.3 (local tex): tau_d = Tr_w(Phi0 [D,Phi1]...[D,Phid] |D|^{-d}) is claimed
to equal c_d * deg(F).  For d=2 (2x2 spinors), Connes' trace theorem gives
   tau_2 = (1/(2(2pi)^2)) * int_{S^1} tr_S( Phi0 (i gamma.dPhi1)(i gamma.dPhi2) ) = -(1/(2 pi)) * int Phi0 grad Phi1 . grad Phi2,
because tr(gamma^mu gamma^nu) = 2 delta^{mu nu} (no epsilon term in even d without the grading).
Oracle: degree computed independently as (1/4pi) int F.(F_x x F_y).  Test: compose a degree-1 map F:T^2->S^2 with
rotations R of S^2: degree is invariant, but I_sym(R) = int F0 gradF1.gradF2 changes => tau_2 is NOT topological.
Positive control: the antisymmetric integral int F0 (dF1 ^ dF2) equals (4pi/3) deg for every R.
Negative control: constant map -> all zero. Refinement: N = 256, 512, 1024."""
import numpy as np, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
out = []; fails = 0
def log(s):
    out.append(s); print(s)
def smooth_step(t):
    t = np.clip(t, 0, 1)
    return t - np.sin(2 * np.pi * t) / (2 * np.pi)   # s(0)=0,s(1)=1, s'(1)=0, s'(0)=0
def Fmap(N):
    x = (np.arange(N) + 0.5) / N
    X, Y = np.meshgrid(x, x, indexing="ij")
    px, py = X - 0.5, Y - 0.5
    rho = np.clip(2 * np.sqrt(px**2 + py**2), 0, 1)
    th = np.pi * smooth_step(rho); ph = np.arctan2(py, px)
    return np.stack([np.cos(th), np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph)]), 1.0 / N
def grad(f, h):
    fx = (np.roll(f, -1, 0) - np.roll(f, 1, 0)) / (2 * h)
    fy = (np.roll(f, -1, 1) - np.roll(f, 1, 1)) / (2 * h)
    return fx, fy
def rot(a, b, c):
    Rz = lambda t: np.array([[np.cos(t), -np.sin(t), 0], [np.sin(t), np.cos(t), 0], [0, 0, 1]])
    Ry = lambda t: np.array([[np.cos(t), 0, np.sin(t)], [0, 1, 0], [-np.sin(t), 0, np.cos(t)]])
    return Rz(a) @ Ry(b) @ Rz(c)
rng = np.random.default_rng(1)
rots = [np.eye(3)] + [rot(*rng.uniform(0, np.pi, 3)) for _ in range(4)]
for N in (256, 512, 1024):
    F0, h = Fmap(N)
    vals = []
    for R in rots:
        F = np.tensordot(R, F0, axes=1)
        gx = [grad(F[i], h)[0] for i in range(3)]; gy = [grad(F[i], h)[1] for i in range(3)]
        cross = np.cross(np.stack(gx), np.stack(gy), axis=0)
        deg = (F * cross).sum(0).sum() * h * h / (4 * np.pi)
        anti = (F[0] * (gx[1] * gy[2] - gy[1] * gx[2])).sum() * h * h
        sym = (F[0] * (gx[1] * gx[2] + gy[1] * gy[2])).sum() * h * h
        vals.append((deg, anti, sym))
    log("N=%d" % N)
    for d, a, s in vals:
        log("   deg=%+.4f  antisym int=%+.4f (4pi/3*deg=%+.4f)  tau_2 ~ -(1/2pi)*sym = %+.5f" % (d, a, 4 * np.pi / 3 * d, -s / (2 * np.pi)))
    syms = np.array([v[2] for v in vals]); degs = np.array([v[0] for v in vals]); antis = np.array([v[1] for v in vals])
    log("   spread of tau_2 over rotations (same degree): %.4f ; spread of degree: %.2e" % (np.ptp(-syms / (2 * np.pi)), np.ptp(degs)))
fails += not (np.ptp(degs) < 1e-2 and np.ptp(syms / (2 * np.pi)) > 1e-2 and np.allclose(antis, 4 * np.pi / 3 * degs, atol=2e-2))
# negative control: constant map
Fc = np.zeros((3, 64, 64)); Fc[0] = 1
gx = [grad(Fc[i], 1 / 64)[0] for i in range(3)]
log("NEG CTRL constant map: sym=%g" % (Fc[0] * (gx[1] * gx[2])).sum())
txt = "\n".join(out)
open(os.path.join(HERE, "num_cocycle_d2.out.txt"), "w", encoding="utf8").write(txt + "\nfailures=%d\n" % int(fails))
sys.exit(int(fails))
