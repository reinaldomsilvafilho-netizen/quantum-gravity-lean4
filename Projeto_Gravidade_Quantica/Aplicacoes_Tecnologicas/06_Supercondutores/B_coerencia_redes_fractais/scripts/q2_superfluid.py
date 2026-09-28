"""Q2 step 2: mean-field superfluid weight of the half-filled E=+2 flat band of the gasket chain,
with self-consistent (relaxed, complex, site-dependent) Delta and with Delta frozen, for two
embeddings of the orbitals (physical x positions / all orbitals at x=0).  The relaxed D_s must
not depend on the embedding (gauge check); the frozen-Delta D_s does.

Controls:
  * disconnected gasket cells (no inter-cell bond): relaxed D_s must be 0;
  * cross-stitch ladder (flat band of one-cell CLS, zero minimal metric): D_s/U -> 0 as U -> 0;
  * sawtooth chain t' = sqrt2 t (flat band with CLS overlapping two cells): D_s/U finite (positive control).
Usage: python q2_superfluid.py [nmax]
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bdg_chain as bc
from q2_bands import flat_levels, metric_integrated

HERE = os.path.dirname(os.path.abspath(__file__))
nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
out = []
def P(*a):
    line = ' '.join(str(x) for x in a); print(line, flush=True); out.append(line)
def save():
    with open(os.path.join(HERE, f'out_q2_superfluid_n{nmax}.txt'), 'w') as f:
        f.write('\n'.join(out) + '\n')

def find_mu(ch, U, ks, target, Ef, D0):
    lo, hi = Ef - 0.5 * U - 0.3, Ef + 0.5 * U + 0.3
    D = D0
    for _ in range(40):
        mu = 0.5 * (lo + hi)
        D, O, n, it, err = bc.solve_sc(ch, mu, 0.0, ks, U, D if np.max(np.abs(D)) > 1e-4 * U else D0, tol=1e-12)
        if np.sum(n) < target:
            lo = mu
        else:
            hi = mu
        if hi - lo < 1e-10:
            break
    D, O, n, it, err = bc.solve_sc(ch, mu, 0.0, ks, U, D, tol=1e-13)
    return mu, D, np.sum(n)

def analyse(name, ch, Ef, U, M=16, embed_zero=True):
    ks = bc.kgrid(M, ch.a0)
    E = np.linalg.eigvalsh(ch.hk_vectorized(ks))
    nbelow = np.mean(np.sum(E < Ef - 1e-6, axis=1))
    deg = np.mean(np.sum(np.abs(E - Ef) < 1e-6, axis=1))
    target = 2 * nbelow + deg
    rng = np.random.default_rng(0)
    D0 = 0.3 * U * (1 + 0.1 * rng.random(ch.N))
    t0 = time.time()
    mu, Dsc, ntot = find_mu(ch, U, ks, target, Ef, D0)
    res = {}
    for emb in (['phys', 'x0'] if embed_zero else ['phys']):
        c = ch if emb == 'phys' else bc.Chain(np.zeros(ch.N), ch.bonds, ch.a0, ch.onsite)
        # Delta for the other embedding: gauge-transform is unnecessary at A=0 (same h(k) up to U(k))
        Dr, _ = bc.superfluid_weight(c, mu, ks, U, Dsc, relax=True, tol=1e-13)
        Df, _ = bc.superfluid_weight(c, mu, ks, U, Dsc, relax=False)
        res[emb] = (Dr, Df)
    P(f'  {name}: U={U:.3f} mu={mu:.6f} n={ntot:.6f}/{target:.1f} |Delta|mean={np.mean(np.abs(Dsc)):.4e} '
      + ' '.join(f'[{e}] Ds_relaxed={r[0]:+.4e} Ds_frozen={r[1]:+.4e}' for e, r in res.items())
      + f'  ({time.time() - t0:.0f}s)')
    save()
    return mu, Dsc, res

def sawtooth():
    X = [0.0, 0.5]
    bonds = [(0, 0, 1, 1.0), (1, 0, 0, np.sqrt(2)), (1, 0, 1, np.sqrt(2))]
    return bc.Chain(X, bonds, 1.0)

P('# controls')
cs = bc.cross_stitch(tperp=5.0)
fl, _ = flat_levels(cs)
P('  cross-stitch flat levels:', fl)
st = sawtooth()
fl2, _ = flat_levels(st)
P('  sawtooth flat levels:', fl2)
Ef_st = [e for e in fl2][0]
P('  sawtooth metric (phys):', metric_integrated(st, Ef_st),
  ' (x0):', metric_integrated(bc.Chain(np.zeros(2), st.bonds, 1.0), Ef_st))
for U in (0.05, 0.1, 0.2):
    analyse('cross-stitch', cs, 5.0, U, M=32)
for U in (0.05, 0.1, 0.2):
    analyse('sawtooth', st, Ef_st, U, M=32)
g1, _ = bc.gasket_chain(2)
analyse('gasket n=2 DISCONNECTED cells', bc.disconnected_cells(g1), 2.0, 0.2)

P('# gasket chain, E=+2 flat band, half filled')
for n in range(1, nmax + 1):
    ch, xy = bc.gasket_chain(n)
    chx0 = bc.Chain(np.zeros(ch.N), ch.bonds, ch.a0)
    P(f' n={n}: metric(phys)={metric_integrated(ch, 2.0):.5e} metric(x0)={metric_integrated(chx0, 2.0):.5e}')
    for U in (0.1, 0.2, 0.4):
        analyse(f'gasket n={n}', ch, 2.0, U, M=12 if n >= 4 else 16)
save()
