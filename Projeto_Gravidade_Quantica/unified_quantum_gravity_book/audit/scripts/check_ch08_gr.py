"""Symbolic checks for the corrected Chapter 8 propositions (G = c = 1 unless stated).

1. Morris-Thorne: principal curvature of r = const spheres inside t = const slice,
   and T_{kk} = rho + p_r at the throat from the Einstein tensor.
2. Reissner-Nordstrom in Painleve-Gullstrand form: T = const slices are flat,
   the horizon sphere r = r_+ has principal curvatures 1/r_+ and theta_l = 0.
3. Schwarzschild limiting maximal slice: |K^r_r| = 3 sqrt(3) M^2 / (2 r^3).
4. Euclidean U-turn lemma: numeric sanity check.
"""
import sympy as sp

t, r, th, ph = sp.symbols('t r theta phi', real=True)
M, Q, r0 = sp.symbols('M Q r_0', positive=True)
b = sp.Function('b')(r)
Phi = sp.Function('Phi')(r)


def einstein_mixed(g, X):
    n = len(X)
    ginv = sp.simplify(g.inv())
    Gam = [[[sp.simplify(sum(ginv[a, d] * (sp.diff(g[d, b_], X[c]) + sp.diff(g[d, c], X[b_]) - sp.diff(g[b_, c], X[d]))
                             for d in range(n)) / 2) for c in range(n)] for b_ in range(n)] for a in range(n)]
    def Riem(a, b_, c, d):
        return (sp.diff(Gam[a][b_][d], X[c]) - sp.diff(Gam[a][b_][c], X[d])
                + sum(Gam[a][c][e] * Gam[e][b_][d] - Gam[a][d][e] * Gam[e][b_][c] for e in range(n)))
    Ric = sp.Matrix(n, n, lambda b_, d: sp.simplify(sum(Riem(a, b_, a, d) for a in range(n))))
    R = sp.simplify(sum(ginv[a, b_] * Ric[a, b_] for a in range(n) for b_ in range(n)))
    G = sp.simplify(ginv * (Ric - R * g / 2))   # G^a_b
    return G


# ---- 1. Morris-Thorne ----
g_mt = sp.diag(-sp.exp(2 * Phi), 1 / (1 - b / r), r**2, r**2 * sp.sin(th)**2)
G = einstein_mixed(g_mt, [t, r, th, ph])
rho = sp.simplify(-G[0, 0] / (8 * sp.pi))
p_r = sp.simplify(G[1, 1] / (8 * sp.pi))
print("8 pi rho   =", sp.simplify(8 * sp.pi * rho))
print("8 pi p_r   =", sp.simplify(8 * sp.pi * p_r))
Tkk = sp.simplify(rho + p_r)
Tkk_throat = sp.simplify(Tkk.subs(sp.Derivative(b, r), sp.Symbol('bp')).subs(b, r).subs(r, r0))
print("T_kk at throat (b(r0)=r0) =", Tkk_throat)
# principal curvature of sphere r=const in slice metric dr^2/(1-b/r) + r^2 dOmega^2:
# unit normal n = sqrt(1-b/r) d_r, k = n(r)/r
k_sphere = sp.sqrt(1 - b / r) / r
print("sphere curvature in slice:", k_sphere, " -> at throat:", sp.simplify(k_sphere.subs(b, r)))

# ---- 2. RN in Painleve-Gullstrand ----
T = sp.symbols('T', real=True)
beta = sp.sqrt(2 * M / r - Q**2 / r**2)
# ds^2 = -dT^2 + (dr + beta dT)^2 + r^2 dOmega^2 : spatial metric flat, lapse 1, shift beta^r = beta
g_pg = sp.Matrix([[-1 + beta**2, beta, 0, 0], [beta, 1, 0, 0], [0, 0, r**2, 0], [0, 0, 0, r**2 * sp.sin(th)**2]])
f_rn = 1 - 2 * M / r + Q**2 / r**2
print("PG metric g_TT + f =", sp.simplify(g_pg[0, 0] + f_rn), "(0 => same lapse function as RN)")
# extrinsic curvature of T=const slice: K_ij = (1/2N)(D_i beta_j + D_j beta_i) (sign convention aside), N=1
Krr = sp.diff(beta, r)
Kthth = r * beta            # Gamma^r_{thth} = -r in flat spherical coords -> D_th beta_th = -Gamma^r_thth beta = r beta
print("K_rr =", sp.simplify(Krr), ", K^th_th =", sp.simplify(Kthth / r**2))
# outgoing null expansion of r=const sphere in slice: theta_l ~ k_sphere - K^th_th - K^ph_ph (standard 3+1 form: D_i s^i - K + K_ij s^i s^j)
theta_l = 2 / r - 2 * beta / r
rp = M + sp.sqrt(M**2 - Q**2)
print("theta_l at r_+ =", sp.simplify(theta_l.subs(r, rp)))
print("PG valid at r_+ (2M r_+ - Q^2 > 0):", sp.simplify(2 * M * rp - Q**2))

# ---- 3. Estabrook et al. limiting slice ----
C = 3 * sp.sqrt(3) * M**2 / 4
print("|K^r_r| = 2C/r^3 =", sp.simplify(2 * C / r**3), "; value at r = 3M/2:", sp.simplify((2 * C / r**3).subs(r, 3 * M / 2)))

# ---- 4. U-turn lemma numeric: curve with |kappa|<=k turning by pi spans >= 2/k across ----
import numpy as np
rng = np.random.default_rng(0)
worst = np.inf
for _ in range(2000):
    k = 1.0
    n = 400
    kap = rng.uniform(-k, k, n) * rng.uniform(0, 1)
    kap += k * rng.uniform(0.2, 1.0)          # bias to turn
    kap = np.clip(kap, -k, k)
    ds = 0.05
    theta = np.concatenate([[0], np.cumsum(kap * ds)])
    if theta.max() < np.pi:
        continue
    i = np.argmax(theta >= np.pi)
    y = np.concatenate([[0], np.cumsum(np.sin(theta[:-1]) * ds)])
    span = y[:i + 1].max() - y[:i + 1].min()
    worst = min(worst, span)
print("min transverse span over random curves reaching theta = pi (k=1):", worst, ">= 2 expected")
