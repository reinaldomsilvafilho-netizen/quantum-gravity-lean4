"""Q1, gasket: exact mean Dirichlet Green function via spectral decimation, checked against
direct diagonalisation (independent oracle), plus a mutated-rule negative control.

Decimation rule (Fukushima-Shima; re-derived here empirically for levels 1..6 and asserted):
  spec_m = { psi_+(l), psi_-(l) : l in spec_{m-1}, l != 6 }  U  { psi_+(6) = 3  for each 6 in spec_{m-1} }
           U { 5 with multiplicity (3^{m-1}+3)/2 }  U  { 6 with multiplicity dim_{m-1} },
  psi_pm(l) = (5 +- sqrt(25 - 4 l)) / 2,  dim_m = (3^{m+1} - 3)/2,  spec_1 = {2, 5, 5}.
Since 1/psi_+ + 1/psi_- = 5/l, the trace T_m = sum 1/l obeys an exact linear recursion.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sympy as s
from collections import Counter
import fractal_graphs as fg

out = []
def P(*a):
    line = ' '.join(str(x) for x in a)
    print(line, flush=True)
    out.append(line)

def dim(m):
    return (3 ** (m + 1) - 3) // 2

def spec_decimation(mmax, mutate=False):
    spec = {1: np.array([2.0, 5.0, 5.0])}
    for m in range(2, mmax + 1):
        prev = spec[m - 1]
        is6 = np.isclose(prev, 6.0)
        l = prev[~is6]
        r = np.sqrt(25 - 4 * l)
        parts = [(5 + r) / 2, (5 - r) / 2, np.full(is6.sum(), 3.0),
                 np.full((3 ** (m - 1) + 3) // 2, 5.0), np.full(dim(m - 1), 6.0)]
        if mutate:  # negative control: forget the 6 -> 3 exception (both branches of 6 kept)
            parts[2] = np.concatenate([np.full(is6.sum(), 3.0), np.full(is6.sum(), 2.0)])
        spec[m] = np.sort(np.concatenate(parts))
    return spec

def main():
    # ---- 1. decimated spectrum vs direct diagonalisation
    spec = spec_decimation(7)
    bad = spec_decimation(7, mutate=True)
    P('# 1. decimation vs direct Dirichlet spectrum')
    for m in range(1, 8):
        L, _ = fg.gasket_dirichlet_laplacian(m)
        lam = np.linalg.eigvalsh(L.toarray())
        ok = len(lam) == len(spec[m]) and np.allclose(np.sort(lam), spec[m], atol=1e-8)
        okbad = len(lam) == len(bad[m]) and np.allclose(np.sort(lam), bad[m], atol=1e-8)
        P(f'm={m} N={len(lam)} dim_formula={dim(m)} match={ok} mutated_match={okbad} '
          f'Gbar_direct={np.mean(1/lam):.10f} Gbar_dec={np.mean(1/spec[m]):.10f}')

    # ---- 2. exact recursion and closed form for T_m = Tr L_D^{-1}
    m = s.symbols('m', integer=True, positive=True)
    a, b, c = s.symbols('a b c')
    # T_m = 5 T_{m-1} - (5/6) d_{m-2} + (1/3) d_{m-2} + (3^{m-1}+3)/10 + d_{m-1}/6
    d = lambda j: (3 ** (j + 1) - 3) / s.Integer(2)
    T = {1: s.Rational(9, 10)}
    for k in range(2, 30):
        T[k] = 5 * T[k - 1] - s.Rational(1, 2) * (d(k - 2) if k >= 3 else 0) + s.Rational(3 ** (k - 1) + 3, 10) + d(k - 1) / 6
    Tm = a * 5 ** m + b * 3 ** m + c
    sol = s.solve([Tm.subs(m, k) - T[k] for k in (3, 4, 5)], [a, b, c])
    closed = s.simplify(Tm.subs(sol))
    P('# 2. closed form T_m = Tr L_D^{-1} (valid m>=2):', closed)
    P('   check m=2..29:', all(s.simplify(closed.subs(m, k) - T[k]) == 0 for k in range(2, 30)))
    P('   direct m=1..7 sums:', [round(float(np.sum(1 / spec[k])), 6) for k in range(1, 8)])
    Gm = closed / ((3 ** (m + 1) - 3) / 2)
    P('   Gbar_m = T_m/dim_m ; Gbar_m (3/5)^m ->', s.limit(Gm * s.Rational(3, 5) ** m, m, s.oo))
    for k in (5, 10, 15, 20):
        P(f'   m={k}: N={dim(k)} Gbar={float(Gm.subs(m, k)):.6e} ratio Gbar_m/Gbar_(m-1)={float(Gm.subs(m, k) / Gm.subs(m, k - 1)):.6f}')
    ds = 2 * np.log(3) / np.log(5)
    P(f'   predicted ratio N-ratio^(2/d_s - 1) = 3^(log5/log3 - 1) = {3 ** (2 / ds - 1):.6f} (=5/3)')
    df = np.log(3) / np.log(2)
    P(f'   NEGATIVE CONTROL (Hausdorff d_f in place of d_s): 3^(2/d_f-1) = {3 ** (2 / df - 1):.6f}  -> rejected')

    # ---- 3. log-periodic IDOS from level-12 decimated spectrum
    spec12 = spec_decimation(12)
    lam = spec12[12]
    N = len(lam)
    lams = np.logspace(np.log10(lam.min()) + 0.5, 0, 400)
    Nl = np.searchsorted(lam, lams) / N
    pfac = Nl / lams ** (ds / 2)
    u = np.log(lams) / np.log(5)
    np.savetxt(os.path.join(os.path.dirname(__file__), 'out_gasket_idos.txt'), np.column_stack([lams, Nl, pfac]),
               header='lambda IDOS(lambda) p=IDOS/lambda^(ds/2)  (level-12 decimated Dirichlet spectrum)')
    P('# 3. IDOS/lambda^(d_s/2): min %.4f max %.4f mean %.4f (log-periodic, period log 5)' % (pfac.min(), pfac.max(), pfac.mean()))
    try:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6, 3.2))
        ax.plot(u, pfac, lw=1)
        ax.set_xlabel(r'$\log_5\lambda$'); ax.set_ylabel(r'$\mathcal{N}(\lambda)/\lambda^{d_s/2}$')
        ax.set_title('Sierpinski gasket, level 12 (spectral decimation)')
        fig.tight_layout(); fig.savefig(os.path.join(os.path.dirname(__file__), '..', 'fig_q1_gasket_logperiodic.png'), dpi=150)
    except Exception as e:
        P('plot failed', e)

    with open(os.path.join(os.path.dirname(__file__), 'out_q1_gasket_exact.txt'), 'w') as f:
        f.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main()
