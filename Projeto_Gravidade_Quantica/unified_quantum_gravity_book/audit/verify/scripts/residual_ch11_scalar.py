"""Scalar curvature of c1 du^2 + c2 e^{2u} |dx|^2 on R x R^{d-1} (d total dims).
Oracle: direct Christoffel/Riemann computation in sympy. Claim: R = -d(d-1)/c1 for all c2 > 0.
Negative control: the mutated claim R = -d(d-1)/c2 must fail."""
import sympy as sp

for d in (2, 3, 4):
    c1, c2 = sp.symbols("c1 c2", positive=True)
    u = sp.Symbol("u")
    xs = sp.symbols("x1:%d" % d)
    co = [u, *xs]
    g = sp.diag(c1, *[c2 * sp.exp(2 * u)] * (d - 1))
    gi = g.inv()
    n = d
    Gam = [[[sum(gi[a, e] * (sp.diff(g[e, b], co[c]) + sp.diff(g[e, c], co[b]) - sp.diff(g[b, c], co[e]))
                 for e in range(n)) / 2 for c in range(n)] for b in range(n)] for a in range(n)]
    def Riem(a, b, c, e):  # R^a_{bce}
        r = sp.diff(Gam[a][b][e], co[c]) - sp.diff(Gam[a][b][c], co[e])
        r += sum(Gam[a][c][f] * Gam[f][b][e] - Gam[a][e][f] * Gam[f][b][c] for f in range(n))
        return r
    Ric = sp.Matrix(n, n, lambda b, e: sum(Riem(a, b, a, e) for a in range(n)))
    R = sp.simplify(sum(gi[b, e] * Ric[b, e] for b in range(n) for e in range(n)))
    print(d, R)
    assert sp.simplify(R + d * (d - 1) / c1) == 0
    assert sp.simplify(R + d * (d - 1) / c2) != 0
print("OK")
