"""Q1: classical XY model H = -J sum_<ij> cos(theta_i - theta_j), J = 1, Monte Carlo
(vectorised Metropolis + over-relaxation on the colour classes of a proper graph colouring).

 (a) gasket, free boundary, levels 3..7: MC magnetisation m = |sum e^{i theta}|/N vs the
     spin-wave prediction m_sw = (1/N) sum_x exp(-T L^+_xx / 2) (the formula under test;
     MC is the independent oracle). Negative control: the same formula with the square-lattice
     value of L^+_xx at equal N must fail.
 (b) Menger sponge (periodic, levels 2, 3) and cubic lattice (periodic, L = 8, 16): Binder
     cumulant U4 = 2 - <m^4>/<m^2>^2 vs T; crossing -> T_c. Compared with the large-n estimate
     T_n = J/(n Gbar_inf), n = 2.
Usage: python q1_xy_mc.py gasket | sponge | cubic
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import scipy.sparse as sp
import networkx as nx
import fractal_graphs as fg

HERE = os.path.dirname(os.path.abspath(__file__))
mode = sys.argv[1] if len(sys.argv) > 1 else 'gasket'
out = []
def P(*a):
    line = ' '.join(str(x) for x in a); print(line, flush=True); out.append(line)
def save():
    with open(os.path.join(HERE, f'out_q1_xy_mc_{mode}.txt'), 'w') as f:
        f.write('\n'.join(out) + '\n')

def colour_classes(A):
    G = nx.from_scipy_sparse_array(A)
    col = nx.greedy_color(G, strategy='largest_first')
    c = np.array([col[i] for i in range(A.shape[0])])
    return [np.nonzero(c == k)[0] for k in range(c.max() + 1)]

def run_xy(A, T, nequil, nmeas, seed=0, theta0=None):
    rng = np.random.default_rng(seed)
    N = A.shape[0]
    A = A.tocsr()
    classes = colour_classes(A)
    th = rng.uniform(0, 2 * np.pi, N) if theta0 is None else theta0.copy()
    step = min(np.pi, 2.0 * np.sqrt(T))
    ms = []
    es = []
    acc_tot = 0; prop_tot = 0
    for sweep in range(nequil + nmeas):
        c, s = np.cos(th), np.sin(th)
        for cl in classes:  # Metropolis
            hx = A[cl] @ c; hy = A[cl] @ s
            new = th[cl] + rng.uniform(-step, step, len(cl))
            dE = -(hx * np.cos(new) + hy * np.sin(new)) + (hx * c[cl] + hy * s[cl])
            accept = rng.random(len(cl)) < np.exp(-np.clip(dE, 0, None) / T)
            th[cl] = np.where(accept, new, th[cl])
            c[cl] = np.cos(th[cl]); s[cl] = np.sin(th[cl])
            acc_tot += accept.sum(); prop_tot += len(cl)
        for _ in range(2):  # over-relaxation: reflect about the local field
            for cl in classes:
                hx = A[cl] @ c; hy = A[cl] @ s
                phi = np.arctan2(hy, hx)
                th[cl] = 2 * phi - th[cl]
                c[cl] = np.cos(th[cl]); s[cl] = np.sin(th[cl])
        if sweep >= nequil:
            mx, my = c.mean(), s.mean()
            ms.append(np.hypot(mx, my))
            es.append(-(c @ (A @ c) + s @ (A @ s)) / (2 * N))
    ms = np.array(ms)
    return ms, np.array(es), acc_tot / prop_tot, th

def blocks_err(x, nb=20):
    b = np.array_split(x, nb)
    mb = np.array([bb.mean() for bb in b])
    return mb.std(ddof=1) / np.sqrt(nb)

if mode == 'gasket':
    P('# gasket XY: MC <m> vs spin-wave prediction m_sw = mean_x exp(-T L+_xx/2)')
    rows = []
    for n in range(3, 8):
        xy, e, _ = fg.gasket(n)
        A = fg.adjacency(len(xy), e)
        L = sp.diags(np.asarray(A.sum(1)).ravel()) - A
        lam, V = np.linalg.eigh(L.toarray())
        Lp = (V[:, 1:] / lam[1:]) @ V[:, 1:].T
        dLp = np.diag(Lp)
        Nn = len(xy)
        # square-lattice control: periodic L x L with L^2 ~ N
        Ls = int(round(np.sqrt(Nn)))
        r = 2 - 2 * np.cos(2 * np.pi * np.arange(Ls) / Ls)
        S = (r[:, None] + r[None, :]).ravel()[1:]
        gsq = np.sum(1 / S) / Ls ** 2
        for T in (0.05, 0.1, 0.2, 0.4):
            t0 = time.time()
            # ordered start: a random start can trap metastable twisted loops at low T
            ms, es, acc, _ = run_xy(A, T, 1000, 4000, seed=n, theta0=np.zeros(A.shape[0]))
            msw = np.mean(np.exp(-T * dLp / 2))
            mctrl = np.exp(-T * gsq / 2)
            rows.append((n, Nn, T, ms.mean(), blocks_err(ms), msw, mctrl))
            P(f'  n={n} N={Nn} T={T}: <m>_MC={ms.mean():.4f}+-{blocks_err(ms):.4f}  m_sw={msw:.4f}  '
              f'control(square G)={mctrl:.4f}  mean L+_xx={dLp.mean():.3f} acc={acc:.2f} ({time.time() - t0:.0f}s)')
            save()
    np.savetxt(os.path.join(HERE, 'out_q1_xy_mc_gasket_table.txt'), np.array(rows),
               header='n N T m_MC err m_spinwave m_control_square')
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    R = np.array(rows)
    fig, ax = plt.subplots(figsize=(6, 4))
    for T in (0.05, 0.1, 0.2, 0.4):
        s = R[:, 2] == T
        ax.errorbar(R[s, 1], R[s, 3], R[s, 4], fmt='o', ms=4, label=f'MC T={T}')
        ax.plot(R[s, 1], R[s, 5], 'k--', lw=0.8)
    ax.set_xscale('log'); ax.set_xlabel('N (gasket sites)'); ax.set_ylabel(r'$\langle m\rangle$')
    ax.set_title('XY on the Sierpinski gasket: MC (points) vs spin waves (dashed)')
    ax.legend(fontsize=7); fig.tight_layout()
    fig.savefig(os.path.join(HERE, '..', 'fig_q1_xy_gasket_mc.png'), dpi=150)

else:
    if mode == 'sponge':
        systems = []
        for lev in (2, 3):
            cells, side = fg.grid_fractal(lev, 3, 3, fg.sponge_keep)
            Lp = fg.grid_laplacian_periodic(cells, side)
            A = -(Lp - sp.diags(Lp.diagonal()))
            systems.append((f'sponge level {lev}', A.tocsr()))
        Ts = np.round(np.arange(1.30, 2.21, 0.1), 3)
    else:
        systems = []
        for Lc in (8, 16):
            cells, side = fg.grid_fractal(1, 3, Lc, fg.full_keep)
            Lp = fg.grid_laplacian_periodic(cells, side)
            A = -(Lp - sp.diags(Lp.diagonal()))
            systems.append((f'cubic L={Lc}', A.tocsr()))
        Ts = np.round(np.arange(1.9, 2.51, 0.1), 3)
    res = {}
    for name, A in systems:
        res[name] = []
        th = None
        for T in Ts[::-1]:  # anneal from high T
            t0 = time.time()
            ms, es, acc, th = run_xy(A, T, 1500, 6000, seed=int(100 * T), theta0=th)
            m2, m4 = np.mean(ms ** 2), np.mean(ms ** 4)
            U4 = 2 - m4 / m2 ** 2
            # jackknife-free block error for U4
            bl = np.array_split(ms, 20)
            Ub = [2 - np.mean(b ** 4) / np.mean(b ** 2) ** 2 for b in bl]
            res[name].append((T, ms.mean(), U4, np.std(Ub, ddof=1) / np.sqrt(20)))
            P(f'  {name} N={A.shape[0]} T={T}: <m>={ms.mean():.4f} U4={U4:.4f}+-{res[name][-1][3]:.4f} acc={acc:.2f} ({time.time() - t0:.0f}s)')
            save()
    names = list(res)
    a = np.array(sorted(res[names[0]])); b = np.array(sorted(res[names[1]]))
    d = a[:, 2] - b[:, 2]
    idx = np.nonzero(np.sign(d[:-1]) != np.sign(d[1:]))[0]
    for i in idx:
        Tc = a[i, 0] - d[i] * (a[i + 1, 0] - a[i, 0]) / (d[i + 1] - d[i])
        P(f'  Binder crossing {names[0]} / {names[1]}: T_c ~ {Tc:.3f}')
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(5, 3.5))
    for nm in names:
        r = np.array(sorted(res[nm]))
        ax.errorbar(r[:, 0], r[:, 2], r[:, 3], fmt='o-', ms=3, label=nm)
    ax.set_xlabel('T/J'); ax.set_ylabel('Binder $U_4$'); ax.legend(); fig.tight_layout()
    fig.savefig(os.path.join(HERE, '..', f'fig_q1_xy_binder_{mode}.png'), dpi=150)
save()
