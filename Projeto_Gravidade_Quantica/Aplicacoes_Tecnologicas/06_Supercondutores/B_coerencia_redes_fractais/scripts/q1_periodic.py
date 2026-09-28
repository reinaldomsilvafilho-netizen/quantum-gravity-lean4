"""Q1, boundary-free version.  Dirichlet boxes add a boundary-layer correction that masks the
intrinsic finite-size law; here every family is taken without an extended boundary:
  * periodic cubic / square lattices (exact k-sums), periodic carpet and Menger sponge (L^+),
  * products  F x C_L  (C_L = periodic ring, L = linear size of F) with F = gasket (3 grounded
    corners), Vicsek (4 grounded tips), gasket (d_s adds exactly: d_s(F x C) = d_s(F) + 1).
Quantity: Gbar_N = (1/N) sum_{lambda>0} 1/lambda.
Prediction (Prop. 2 of Q1_rigidez.md): Gbar_inf - Gbar_N ~ B N^{-kappa}, kappa = 1 - 2/d_s (d_s>2);
Gbar_N ~ N^{-kappa} (d_s<2); ~ ln N / (2 pi d_s) ... (d_s=2).
Estimator of kappa that needs no G_inf: successive differences
   Delta_n = Gbar_{n+1} - Gbar_n  ~  N_n^{-kappa} (geometric sizes) -> kappa = -log(Delta_{n+1}/Delta_n)/log(N_{n+1}/N_n).
Negative control: the Hausdorff dimension d_f in place of d_s.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import fractal_graphs as fg
from q1_gasket_exact import spec_decimation  # exact gasket Dirichlet spectrum

HERE = os.path.dirname(os.path.abspath(__file__))
out = []
def P(*a):
    line = ' '.join(str(x) for x in a); print(line, flush=True); out.append(line)
def save():
    with open(os.path.join(HERE, 'out_q1_periodic.txt'), 'w') as f:
        f.write('\n'.join(out) + '\n')

def ring(L):
    return 2 - 2 * np.cos(2 * np.pi * np.arange(L) / L)

def prod_mean_pinv(l1, l2):
    S = l1[:, None] + l2[None, :]
    S = S[S > 1e-12]
    return np.sum(1 / S) / (len(l1) * len(l2))

fam = {}
# periodic cubic lattice (exact); G_inf = Watson/6
W = np.sqrt(6) / (32 * np.pi ** 3) * np.prod([__import__('math').gamma(x / 24) for x in (1, 5, 7, 11)])
cu = []
for L in [8, 16, 32, 64, 128, 256]:
    r = ring(L)
    tot = 0.0
    for a in r:
        S = a + r[:, None] + r[None, :]
        S = S[S > 1e-12]
        tot += np.sum(1 / S)
    cu.append((L ** 3, tot / L ** 3))
fam['cubic'] = dict(data=cu, ds=3.0, df=3.0, Ginf=W / 6)
sq = []
for L in [16, 32, 64, 128, 256, 512, 1024, 2048]:
    sq.append((L * L, prod_mean_pinv(ring(L), ring(L))))
fam['square'] = dict(data=sq, ds=2.0, df=2.0)

# gasket x ring, gasket x gasket (exact decimation spectra)
spec = spec_decimation(9)
gr, gg = [], []
for m in range(2, 10):
    gr.append((len(spec[m]) * 2 ** m, prod_mean_pinv(spec[m], ring(2 ** m))))
for m in range(2, 8):
    gg.append((len(spec[m]) ** 2, prod_mean_pinv(spec[m], spec[m])))
dsg = 2 * np.log(3) / np.log(5); dfg = np.log(3) / np.log(2)
fam['gasket x ring'] = dict(data=gr, ds=dsg + 1, df=dfg + 1)
fam['gasket x gasket'] = dict(data=gg, ds=2 * dsg, df=2 * dfg)
P('# gasket x ring:', gr); P('# gasket x gasket:', gg); save()

# Vicsek(3) x ring
vr = []
for n in range(1, 6):
    cells, side = fg.grid_fractal(n, 2, 3, fg.vicsek_keep_factory(3))
    l1 = np.linalg.eigvalsh(fg.grid_laplacian(cells, side).toarray())
    vr.append((len(l1) * side, prod_mean_pinv(l1, ring(side))))
dfv = np.log(5) / np.log(3)
fam['Vicsek x ring'] = dict(data=vr, ds=1 + 2 * dfv / (dfv + 1), df=dfv + 1)
P('# Vicsek x ring:', vr); save()

# periodic carpet and sponge
for name, dim, keep, levels, ns, ds_ref, df in [
        ('carpet (periodic)', 2, fg.carpet_keep, [1, 2, 3, 4, 5, 6], 200, 1.8060, np.log(8) / np.log(3)),
        ('Menger sponge (periodic)', 3, fg.sponge_keep, [1, 2, 3, 4], 100, 2.5259, np.log(20) / np.log(3))]:
    data = []
    for n in levels:
        t0 = time.time()
        cells, side = fg.grid_fractal(n, dim, 3, keep)
        Lp = fg.grid_laplacian_periodic(cells, side)
        g, err = fg.mean_pinv_diag_sampled(Lp, nsamp=ns)
        data.append((len(cells), g, err))
        P(f'  {name} level {n}: N={len(cells)} Gbar={g:.6f} +- {err:.6f} ({time.time() - t0:.0f}s)'); save()
    fam[name] = dict(data=data, ds=ds_ref, df=df)

# ---------------------------------------------------------------- exponent estimates
P('# successive-difference exponent kappa_eff (last pairs) vs kappa(d_s) and kappa(d_f)')
P('  family | d_s | kappa(d_s) | kappa(d_f) | kappa_eff (sequence) | d_s implied by last kappa_eff')
for name, r in fam.items():
    N = np.array([x[0] for x in r['data']], float); G = np.array([x[1] for x in r['data']])
    if name == 'square':
        sl = np.diff(G) / np.diff(np.log(N))
        P(f'  square | 2 | 0 | 0 | dG/dlnN = {np.round(sl, 5).tolist()} -> 1/(4 pi) = {1 / (4 * np.pi):.5f}')
        continue
    D = np.diff(G)
    kap = -np.log(np.abs(D[1:]) / np.abs(D[:-1])) / np.log(N[2:] / N[1:-1])
    kd, kf = 1 - 2 / r['ds'], 1 - 2 / r['df']
    last = kap[-1]
    P(f'  {name} | {r["ds"]:.4f} | {kd:.4f} | {kf:.4f} | {np.round(kap, 4).tolist()} | {2 / (1 - last):.4f}')
    if 'Ginf' in r:
        P(f'     cubic: Gbar_N at L=256: {G[-1]:.6f}  Watson G_inf = {r["Ginf"]:.6f}  gap*L = {(r["Ginf"] - G[-1]) * N[-1] ** (1 / 3):.4f}')
save()

import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
for name, r in fam.items():
    N = np.array([x[0] for x in r['data']], float); G = np.array([x[1] for x in r['data']])
    ax[0].semilogx(N, G, 'o-', ms=3, label=f'{name} ($d_s$={r["ds"]:.3f})')
    if name != 'square':
        D = np.abs(np.diff(G))
        ax[1].loglog(N[1:], D, 'o-', ms=3, label=name)
        kd = 1 - 2 / r['ds']
        ax[1].loglog(N[1:], D[-1] * (N[1:] / N[-1]) ** (-kd), 'k:', lw=0.8)
ax[0].set_xlabel('N'); ax[0].set_ylabel(r'$\bar G_N$'); ax[0].legend(fontsize=6)
ax[1].set_xlabel('N'); ax[1].set_ylabel(r'$|\bar G_{n+1}-\bar G_n|$ (dotted: slope $-\kappa=2/d_s-1$)')
fig.tight_layout(); fig.savefig(os.path.join(HERE, '..', 'fig_q1_periodic_scaling.png'), dpi=150)
save()
