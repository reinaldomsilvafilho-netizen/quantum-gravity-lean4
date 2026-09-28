"""Q2 step 1: band structure of the chain of level-n Sierpinski gaskets (H = -t A, t = 1).
 * oracle: Bloch spectrum at k = 2 pi j/(M a0) vs direct diagonalisation of the M-cell ring;
 * flat bands: k-independent levels, their degeneracy per cell, gap to dispersive levels;
 * integrated quantum metric (Marzari-Vanderbilt invariant spread per cell along x) of the
   flat-band manifold: Omega_I = (1/M) sum_k Tr g(k), g = (1/2) Tr[(dP/dk)^2];
   real-space check: Omega_I = Tr[P X (1-P) X]/M on a large ring (Resta form with sin).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bdg_chain as bc
import fractal_graphs as fg

HERE = os.path.dirname(os.path.abspath(__file__))
out = []
def P(*a):
    line = ' '.join(str(x) for x in a); print(line, flush=True); out.append(line)

def ring_hamiltonian(ch, M):
    N = ch.N
    H = np.zeros((N * M, N * M))
    for R in range(M):
        for (a, b, dR, t) in ch.bonds:
            i = R * N + a; j = ((R + dR) % M) * N + b
            H[i, j] += -t; H[j, i] += -t
    return H

def flat_levels(ch, M=48, tol=1e-9):
    ks = bc.kgrid(M, ch.a0)
    E = np.linalg.eigvalsh(ch.hk_vectorized(ks))  # (M, N)
    vals = np.round(E, 7)
    levels = {}
    for e in np.unique(vals):
        cnt = (np.abs(E - e) < 1e-6).sum(axis=1)
        if cnt.min() > 0 and cnt.min() == cnt.max():
            levels[float(e)] = int(cnt[0])
    flat = {}
    for e, c in levels.items():
        others = E[np.abs(E - e) > 1e-6]
        flat[e] = (c, np.min(np.abs(others - e)) if others.size else np.inf)
    return flat, E

def flat_projector(ch, k, Ef, tol=1e-6):
    E, V = np.linalg.eigh(ch.hk(k))
    S = V[:, np.abs(E - Ef) < tol]
    return S @ S.conj().T, S.shape[1]

def metric_integrated(ch, Ef, M=64, dk=1e-4):
    ks = bc.kgrid(M, ch.a0)
    tot = 0.0
    for k in ks:
        Pp, n1 = flat_projector(ch, k + dk, Ef)
        Pm, n2 = flat_projector(ch, k - dk, Ef)
        dP = (Pp - Pm) / (2 * dk)
        tot += 0.5 * np.real(np.trace(dP @ dP))
    return tot / M

def minimal_metric(ch, Ef, M=64, dk=1e-4):
    """Minimise the integrated metric over orbital positions X (Huhtinen et al. 2022).
    With U_X(k) = diag(exp(-i k X)), dP_X = U(dP_0 - i[X, P_0])U^+, so
    Tr g_X = Tr g_0 + sum_a X_a w_a + sum_ab X_a Q_ab X_b  with
    w_a = (-i[P0, D0])_aa,  Q_ab = delta_ab P_aa - |P_ab|^2  (k-averaged): a quadratic problem.
    Returns (metric at X=0, minimal metric, argmin X)."""
    c0 = Chain0(ch)
    ks = bc.kgrid(M, ch.a0)
    N = ch.N
    Q = np.zeros((N, N)); w = np.zeros(N); g0 = 0.0
    for k in ks:
        Pp, _ = flat_projector(c0, k + dk, Ef)
        Pm, _ = flat_projector(c0, k - dk, Ef)
        P0, _ = flat_projector(c0, k, Ef)
        D = (Pp - Pm) / (2 * dk)
        g0 += 0.5 * np.real(np.trace(D @ D))
        w += np.real(np.diag(-1j * (P0 @ D - D @ P0)))
        Q += np.diag(np.real(np.diag(P0))) - np.abs(P0) ** 2
    Q /= M; w /= M; g0 /= M
    X = -0.5 * np.linalg.lstsq(Q, w, rcond=None)[0]
    gmin = g0 + w @ X + X @ Q @ X
    return g0, gmin, X

def Chain0(ch):
    return bc.Chain(np.zeros(ch.N), ch.bonds, ch.a0, ch.onsite)

if __name__ == '__main__':
    P('# Bloch vs ring oracle')
    for n in (1, 2, 3):
        ch, _ = bc.gasket_chain(n)
        M = 5
        Er = np.linalg.eigvalsh(ring_hamiltonian(ch, M))
        ks = 2 * np.pi * np.arange(M) / (M * ch.a0)
        Eb = np.sort(np.linalg.eigvalsh(ch.hk_vectorized(ks)).ravel())
        P(f'  n={n}: max|E_ring - E_Bloch| = {np.max(np.abs(Er - Eb)):.2e}')
    P('# flat levels of the gasket chain (E: degeneracy per cell, gap to nearest dispersive level)')
    summary = []
    for n in range(1, 6):
        ch, _ = bc.gasket_chain(n)
        flat, E = flat_levels(ch)
        nfl = sum(c for c, g in flat.values())
        top = sorted(flat.items(), key=lambda kv: -kv[1][0])[:4]
        P(f'  n={n} N_cell={ch.N} flat states/cell={nfl} ({nfl / ch.N:.3f}); largest: ' +
          ', '.join(f'E={e:+.4f}:{c} (gap {g:.3f})' for e, (c, g) in top))
        summary.append((n, ch.N, flat))
    P('# integrated quantum metric of selected flat manifolds (per cell, units of bond length^2)')
    for n in range(1, 6):
        ch, _ = bc.gasket_chain(n)
        flat, _ = flat_levels(ch)
        for Ef in (2.0, 1.0):
            if Ef in flat:
                c, g = flat[Ef]
                if g < 1e-6:
                    P(f'  n={n} E={Ef}: touches a dispersive band (gap {g:.1e}); metric skipped')
                    continue
                Om = metric_integrated(ch, Ef)
                P(f'  n={n} E={Ef:+.1f} deg={c} gap={g:.4f}  Omega_I={Om:.6e}  Omega_I/deg={Om / c:.3e}')
    with open(os.path.join(HERE, 'out_q2_bands.txt'), 'w') as f:
        f.write('\n'.join(out) + '\n')
