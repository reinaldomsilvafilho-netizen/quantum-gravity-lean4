"""Minimal quantum metric of flat manifolds (gasket chain E=+2; sawtooth; cross-stitch),
checked by direct evaluation of the metric at the optimal positions (independent route:
metric_integrated with the optimised X) and a mutated control (random X must not go below)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import bdg_chain as bc
from q2_bands import minimal_metric, metric_integrated, flat_levels

HERE = os.path.dirname(os.path.abspath(__file__))
out = []
def P(*a):
    line = ' '.join(str(x) for x in a); print(line, flush=True); out.append(line)

def sawtooth():
    return bc.Chain([0.0, 0.5], [(0, 0, 1, 1.0), (1, 0, 0, np.sqrt(2)), (1, 0, 1, np.sqrt(2))], 1.0)

rng = np.random.default_rng(3)
cases = [('cross-stitch', bc.cross_stitch(5.0), 5.0), ('sawtooth', sawtooth(), 2.0)]
for n in range(1, 6):
    cases.append((f'gasket n={n}', bc.gasket_chain(n)[0], 2.0))
for name, ch, Ef in cases:
    g0, gmin, X = minimal_metric(ch, Ef)
    chX = bc.Chain(X, ch.bonds, ch.a0, ch.onsite)
    gdirect = metric_integrated(chX, Ef)
    gphys = metric_integrated(ch, Ef)
    grand = min(metric_integrated(bc.Chain(X + 0.3 * rng.standard_normal(ch.N), ch.bonds, ch.a0), Ef) for _ in range(3))
    deg = flat_levels(ch)[0][Ef][0]
    P(f'{name}: deg={deg} metric(phys)={gphys:.6f} metric(x0)={g0:.6f} minimal={gmin:.6f} '
      f'direct@Xmin={gdirect:.6f} perturbed-X min={grand:.6f}  minimal/deg={gmin / deg:.5f} minimal*a0={gmin * ch.a0:.5f}')
with open(os.path.join(HERE, 'out_q2_minmetric.txt'), 'w') as f:
    f.write('\n'.join(out) + '\n')
