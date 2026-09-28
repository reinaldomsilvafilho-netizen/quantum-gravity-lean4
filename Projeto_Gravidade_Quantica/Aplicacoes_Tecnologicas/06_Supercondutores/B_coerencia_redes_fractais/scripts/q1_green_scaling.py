"""Q1: mean Dirichlet Green function Gbar(N) = (1/N) Tr L_D^{-1} (= <dtheta^2> J/T in the harmonic
XY model) versus size for several graph families, plus d_s from an independent route
(face-to-face resistance scaling, or exact values), and a fit of the finite-size law
      Gbar(N) = G_inf + B * N^{-kappa},   kappa = 1 - 2/d_s   (kappa < 0: divergence).
Negative control: the same law with the Hausdorff dimension d_f in place of d_s.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.optimize import curve_fit
import fractal_graphs as fg

HERE = os.path.dirname(os.path.abspath(__file__))
out = []
def P(*a):
    line = ' '.join(str(x) for x in a)
    print(line, flush=True)
    out.append(line)

def save():
    with open(os.path.join(HERE, 'out_q1_green_scaling.txt'), 'w') as f:
        f.write('\n'.join(out) + '\n')

results = {}

# ------------------------------------------------ separable boxes (exact from 1D spectra)
def box_gbar(L, dim):
    l1 = fg.chain_dirichlet_eigs(L)
    if dim == 1:
        return np.mean(1 / l1)
    if dim == 2:
        return np.mean(1 / (l1[:, None] + l1[None, :]))
    tot = 0.0
    for a in l1:
        tot += np.sum(1 / (a + l1[:, None] + l1[None, :]))
    return tot / L ** 3

P('# oracle check: separable formula vs direct inverse (small boxes)')
for dim, L in [(2, 12), (3, 7)]:
    cells, side = fg.grid_fractal(1, dim, L, fg.full_keep)
    Lap = fg.grid_laplacian(cells, side)
    direct = np.mean(np.diag(np.linalg.inv(Lap.toarray())))
    P(f'  dim={dim} L={L}: separable={box_gbar(L, dim):.12f} direct={direct:.12f}')

sq = [(L * L, box_gbar(L, 2)) for L in [8, 16, 32, 64, 128, 256, 512, 1024]]
cu = [(L ** 3, box_gbar(L, 3)) for L in [8, 12, 16, 24, 32, 48, 64, 96, 128]]
results['square (d_s=2)'] = dict(data=sq, ds_ref=2.0, df=2.0)
results['cubic (d_s=3)'] = dict(data=cu, ds_ref=3.0, df=3.0)
P('# square lattice: Gbar vs N;  slope dGbar/dlnN (expect 1/(4pi)=%.5f):' % (1 / (4 * np.pi)))
for (N1, g1), (N2, g2) in zip(sq[:-1], sq[1:]):
    P(f'  N={N2:8d} Gbar={g2:.6f} slope={(g2 - g1) / np.log(N2 / N1):.5f}')
W = np.sqrt(6) / (32 * np.pi ** 3) * np.prod([__import__('math').gamma(x / 24) for x in (1, 5, 7, 11)])
P(f'# cubic lattice: Watson integral oracle G_inf = W/6 = {W / 6:.6f} (W = Watson 1.516386)')
for N, g in cu:
    P(f'  N={N:8d} Gbar={g:.6f}')

# ------------------------------------------------ gasket (exact closed form, q1_gasket_exact.py)
gas = []
for m in range(3, 16):
    T = 5 ** m / 4 - 3 ** m / 20 - 0.2
    Nn = (3 ** (m + 1) - 3) // 2
    gas.append((Nn, T / Nn))
results['gasket (d_s=1.365)'] = dict(data=gas, ds_ref=2 * np.log(3) / np.log(5), df=np.log(3) / np.log(2))

# ------------------------------------------------ grid fractals: sampled Gbar + resistance
def resistance_faces(cells, side, axis=0):
    """Resistance between the two faces orthogonal to `axis` (other outer faces insulating)."""
    A = fg.grid_adjacency_free(cells, side)
    deg = np.asarray(A.sum(1)).ravel()
    left = cells[:, axis] == 0
    right = cells[:, axis] == side - 1
    # ghost bonds to electrode at potential 1 (left) and 0 (right), unit conductance
    Lp = sp.diags(deg + left + right) - A
    b = left.astype(float)
    V = spla.spsolve(Lp.tocsc(), b) if len(cells) < 60000 else spla.cg(Lp, b, rtol=1e-12, maxiter=200000)[0]
    I = np.sum(1 - V[left])
    return 1.0 / I

def gbar_grid(cells, side, nsamp):
    Lap = fg.grid_laplacian(cells, side)
    N = Lap.shape[0]
    if N <= 5000:
        return fg.mean_green_dense(Lap)[0], 0.0
    if cells.shape[1] == 2 or N < 60000:
        return fg.mean_green_sampled(Lap, nsamp=nsamp)
    # 3D large: Jacobi-preconditioned CG per sampled site
    rng = np.random.default_rng(1)
    xs = rng.choice(N, size=nsamp, replace=False)
    Minv = sp.diags(1 / Lap.diagonal())
    vals = []
    for x in xs:
        bvec = np.zeros(N); bvec[x] = 1
        sol, info = spla.cg(Lap, bvec, rtol=1e-10, maxiter=100000, M=Minv)
        vals.append(sol[x])
    vals = np.array(vals)
    return vals.mean(), vals.std(ddof=1) / np.sqrt(nsamp)

def family(name, dim, s, keep, levels, nsamp, df):
    data, R = [], []
    for n in levels:
        t0 = time.time()
        cells, side = fg.grid_fractal(n, dim, s, keep)
        g, err = gbar_grid(cells, side, nsamp)
        r = resistance_faces(cells, side)
        data.append((len(cells), g))
        R.append(r)
        P(f'  {name} level {n}: N={len(cells)} Gbar={g:.6f} +- {err:.6f}  R_face={r:.6f}  ({time.time() - t0:.1f}s)')
        save()
    m = s ** dim if keep is fg.full_keep else len(fg.grid_fractal(1, dim, s, keep)[0])
    rho = R[-1] / R[-2]
    dw = np.log(m * rho) / np.log(s)
    ds_res = 2 * np.log(m) / np.log(m * rho)
    P(f'  {name}: resistance ratio rho={rho:.5f} (prev {R[-2] / R[-3]:.5f}) -> d_w={dw:.4f}, d_s(resistance)={ds_res:.4f}, d_f={df:.4f}')
    results[name] = dict(data=data, ds_ref=ds_res, df=df, ds_note='resistance')

P('# Sierpinski carpet (2D)')
family('carpet', 2, 3, fg.carpet_keep, [1, 2, 3, 4, 5, 6], 300, np.log(8) / np.log(3))
P('# Menger sponge (3D)')
family('Menger sponge', 3, 3, fg.sponge_keep, [1, 2, 3, 4], 120, np.log(20) / np.log(3))

# ------------------------------------------------ product graphs: d_s = d_s(G) + 1 exactly
def vicsek_eigs(n, s=3):
    cells, side = fg.grid_fractal(n, 2, s, fg.vicsek_keep_factory(s))
    return np.linalg.eigvalsh(fg.grid_laplacian(cells, side).toarray()), side

def product_gbar(l1, l2):
    return np.mean(1 / (l1[:, None] + l2[None, :]))

P('# products with a Dirichlet chain of matching linear size (d_s adds exactly)')
vp = []
for n in range(1, 6):
    l1, side = vicsek_eigs(n)
    l2 = fg.chain_dirichlet_eigs(side)
    vp.append((len(l1) * len(l2), product_gbar(l1, l2)))
    P(f'  Vicsek(3) x chain level {n}: N={vp[-1][0]} Gbar={vp[-1][1]:.6f}')
dfv = np.log(5) / np.log(3)
results['Vicsek x chain (d_s=2.188)'] = dict(data=vp, ds_ref=1 + 2 * dfv / (dfv + 1), df=dfv + 1)
gp = []
for m in range(1, 8):
    L, _ = fg.gasket_dirichlet_laplacian(m)
    l1 = np.linalg.eigvalsh(L.toarray())
    l2 = fg.chain_dirichlet_eigs(2 ** m)
    gp.append((len(l1) * len(l2), product_gbar(l1, l2)))
    P(f'  gasket x chain level {m}: N={gp[-1][0]} Gbar={gp[-1][1]:.6f}')
results['gasket x chain (d_s=2.365)'] = dict(data=gp, ds_ref=1 + 2 * np.log(3) / np.log(5), df=1 + np.log(3) / np.log(2))
save()

# ------------------------------------------------ fits
def law(N, Ginf, B, kappa):
    return Ginf + B * N ** (-kappa)

P('# fits Gbar = G_inf + B N^-kappa on the largest sizes; d_s(fit) = 2/(1-kappa)')
P('  family | d_s(ref) | kappa_pred | kappa_fit | d_s(fit) | G_inf | rms(pred d_s) | rms(d_f control)')
fitrows = []
for name, r in results.items():
    N = np.array([x[0] for x in r['data']], float)
    G = np.array([x[1] for x in r['data']])
    if name.startswith('square'):
        c = np.polyfit(np.log(N[-4:]), G[-4:], 1)
        P(f'  {name}: log law Gbar = {c[0]:.5f} ln N + {c[1]:.5f}  (1/(4pi)={1/(4*np.pi):.5f})')
        continue
    sel = slice(-5, None) if len(N) >= 5 else slice(None)
    Ns, Gs = N[sel], G[sel]
    kp = 1 - 2 / r['ds_ref']
    kf = 1 - 2 / r['df']
    try:
        p, _ = curve_fit(law, Ns, Gs, p0=[Gs[-1], -1.0 if kp > 0 else 0.1, kp], maxfev=20000)
    except Exception:
        p = [np.nan, np.nan, np.nan]
    def rms_fixed(kappa):
        X = np.column_stack([np.ones_like(Ns), Ns ** (-kappa)])
        coef, *_ = np.linalg.lstsq(X, Gs, rcond=None)
        return np.sqrt(np.mean((X @ coef - Gs) ** 2)) / np.mean(np.abs(Gs))
    row = (name, r['ds_ref'], kp, p[2], 2 / (1 - p[2]), p[0], rms_fixed(kp), rms_fixed(kf))
    fitrows.append(row)
    P('  %s | %.4f | %.4f | %.4f | %.4f | %.4f | %.2e | %.2e' % row)
save()

# ------------------------------------------------ figure
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6.4, 4.2))
for name, r in results.items():
    N = np.array([x[0] for x in r['data']], float); G = np.array([x[1] for x in r['data']])
    ax.loglog(N, G, 'o-', ms=3, label=name)
ax.set_xlabel('N (sites)'); ax.set_ylabel(r'$\bar G_N=\frac{1}{N}\mathrm{Tr}\,L_D^{-1}=\frac{J}{T}\langle\delta\theta^2\rangle$')
ax.legend(fontsize=7); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig(os.path.join(HERE, '..', 'fig_q1_green_vs_size.png'), dpi=150)
save()
