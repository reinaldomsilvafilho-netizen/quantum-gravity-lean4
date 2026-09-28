"""Q2 step 3: exact two-body problem projected onto the flat band (leading order in U/gap),
a check of the mean-field result that does not use BCS.

For a flat band at E_f with Bloch projector P(k) (orbital basis), a singlet pair of total momentum
K bound by -U sum_a n_a,up n_a,dn has energies E(K) = 2E_f - U * eig Lambda(K),
     Lambda_ab(K) = (1/M) sum_k P_ab(k+K) P_ab(-k)
(Gram matrix of the projected on-site pair states).  Pair band flat in K  <=>  pair obstructed
(infinite mass, zero stiffness at order U).  Oracle: brute-force two-particle diagonalisation on a
small ring (independent code path).  Also: the gasket graph is checked to be the line graph of
the Hanoi graph with three pendant edges (so E=+2t is the line-graph flat band, A=-2).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import networkx as nx
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import bdg_chain as bc
import fractal_graphs as fg
from q2_bands import flat_levels, ring_hamiltonian

HERE = os.path.dirname(os.path.abspath(__file__))
out = []
def P(*a):
    line = ' '.join(str(x) for x in a); print(line, flush=True); out.append(line)
def save():
    with open(os.path.join(HERE, 'out_q2_twobody.txt'), 'w') as f:
        f.write('\n'.join(out) + '\n')

# ---------------- line-graph check
def hanoi(n):
    G = nx.Graph()
    if n == 0:
        G.add_node(()); return G, {0: (), 1: (), 2: ()}
    # vertices: words in {0,1,2}^n ; Sierpinski graph S(n,3) with triangles at the bottom level
    import itertools
    for w in itertools.product(range(3), repeat=n):
        G.add_node(w)
    for w in itertools.product(range(3), repeat=n - 1):
        for i in range(3):
            for j in range(i + 1, 3):
                G.add_edge(w + (i,), w + (j,))
    for l in range(1, n):  # bridges between level-l copies: prefix p, then i j^(n-l-1)... ~ j i^(...)
        for p in itertools.product(range(3), repeat=n - l - 1):
            for i in range(3):
                for j in range(i + 1, 3):
                    G.add_edge(p + (i,) + (j,) * l, p + (j,) + (i,) * l)
    extremes = {i: (i,) * n for i in range(3)}
    return G, extremes

P('# gasket graph == line graph of (Hanoi graph + 3 pendant edges)?')
for n in range(1, 5):
    H, ext = hanoi(n)
    for i, v in ext.items():
        H.add_edge(v, ('pendant', i))
    LG = nx.line_graph(H)
    xy, e, _ = fg.gasket(n)
    Gs = nx.Graph(); Gs.add_edges_from(map(tuple, e))
    P(f'  n={n}: |V(gasket)|={Gs.number_of_nodes()} |V(L(H))|={LG.number_of_nodes()} isomorphic={nx.is_isomorphic(Gs, LG)}')
save()

# ---------------- projected two-body problem
def flat_P(ch, k, Ef, tol=1e-6):
    E, V = np.linalg.eigh(ch.hk(k))
    S = V[:, np.abs(E - Ef) < tol]
    return S @ S.conj().T

def pair_bands(ch, Ef, M=48, nK=25):
    ks = bc.kgrid(M, ch.a0)
    Pk = np.array([flat_P(ch, k, Ef) for k in ks])
    Pmk = np.array([flat_P(ch, -k, Ef) for k in ks])
    Ks = np.linspace(0, np.pi / ch.a0, nK)
    bands = []
    for K in Ks:
        PK = np.array([flat_P(ch, k + K, Ef) for k in ks])
        Lam = np.mean(PK * Pmk, axis=0)
        bands.append(np.linalg.eigvalsh(Lam)[::-1])
    return Ks, np.array(bands)

def brute_pair(ch, M, U, Ef, nev=6):
    """Lowest two-particle (up, down) energies on an M-cell ring, H1 = +A (flat band = bottom)."""
    H1 = -ring_hamiltonian(ch, M)  # ring_hamiltonian builds -t A ; flip sign -> +A
    Nn = H1.shape[0]
    I = sp.identity(Nn)
    H1s = sp.csr_matrix(H1)
    diag = np.zeros(Nn * Nn); diag[np.arange(Nn) * Nn + np.arange(Nn)] = -U
    H2 = sp.kron(H1s, I) + sp.kron(I, H1s) + sp.diags(diag)
    vals = spla.eigsh(H2.tocsc(), k=nev, sigma=2 * Ef - 3 * U, which='LM')[0]
    return np.sort(vals)

def sawtooth():
    return bc.Chain([0.0, 0.5], [(0, 0, 1, 1.0), (1, 0, 0, np.sqrt(2)), (1, 0, 1, np.sqrt(2))], 1.0)

P('# oracle: projected pair energies 2E_f - U*eig(Lambda) vs brute-force two-body ring (H1=+A, E_f=-2)')
for name, ch, M in [('gasket n=1', bc.gasket_chain(1)[0], 6), ('gasket n=2', bc.gasket_chain(2)[0], 4)]:
    chm = bc.Chain(ch.X, [(a, b, dR, -t) for (a, b, dR, t) in ch.bonds], ch.a0)  # H1 = +A
    Ks = 2 * np.pi * np.arange(M) / (M * ch.a0)
    ksr = 2 * np.pi * np.arange(M) / (M * ch.a0)
    Pk = {round(k, 12): flat_P(chm, k, -2.0) for k in np.concatenate([ksr, -ksr])}
    def PP(k):
        kk = (k + np.pi / ch.a0) % (2 * np.pi / ch.a0) - np.pi / ch.a0
        return flat_P(chm, k, -2.0)
    for U in (0.02,):
        proj = []
        for K in Ks:
            Lam = np.mean([PP(k + K) * PP(-k) for k in ksr], axis=0)
            proj += list(-4 - U * np.linalg.eigvalsh(Lam))
        proj = np.sort(proj)
        br = brute_pair(ch, M, U, -2.0, nev=4)
        P(f'  {name} M={M} U={U}: projected lowest {np.round(proj[:4], 6).tolist()}  brute {np.round(br, 6).tolist()}')
save()

P('# pair bands (leading order): lambda_j(K), j = most bound first. width = max_K - min_K')
res = {}
cases = [('cross-stitch', bc.cross_stitch(5.0), 5.0), ('sawtooth', sawtooth(), 2.0)]
for n in range(1, 6):
    cases.append((f'gasket n={n}', bc.gasket_chain(n)[0], 2.0))
for name, ch, Ef in cases:
    Ks, B = pair_bands(ch, Ef)
    top = B[:, 0]
    width = top.max() - top.min()
    dK = Ks[1] - Ks[0]
    curv = (2 * top[1] - 2 * top[0]) / dK ** 2  # symmetric in K: lambda(dK)+lambda(-dK)-2lambda(0)
    # most mobile band among the 5 most bound
    widths = B[:, :6].max(0) - B[:, :6].min(0)
    P(f'  {name}: lambda_max(K=0)={top[0]:.5f} width(top band)={width:.3e}  '
      f'1/m* = -U*curv, curv={curv:.4e}; widths of 6 most-bound pair bands: {np.round(widths, 5).tolist()}')
    res[name] = (Ks, B)
    save()

import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 3, figsize=(11, 3.4))
for ax, name in zip(axs, ['sawtooth', 'gasket n=2', 'gasket n=4']):
    Ks, B = res[name]
    ch_a0 = 1.0 if name == 'sawtooth' else 2 ** int(name[-1])
    for j in range(min(8, B.shape[1])):
        ax.plot(Ks * ch_a0, B[:, j], lw=1)
    ax.set_title(name); ax.set_xlabel(r'$K a_0$'); ax.set_ylabel(r'$\lambda_j(K)$  [$E=2E_f-U\lambda$]')
fig.tight_layout(); fig.savefig(os.path.join(HERE, '..', 'fig_q2_pair_bands.png'), dpi=150)
save()
