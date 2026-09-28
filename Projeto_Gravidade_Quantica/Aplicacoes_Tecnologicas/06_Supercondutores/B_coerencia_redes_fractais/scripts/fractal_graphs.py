"""Graph constructions and Dirichlet Laplacians for the B line (Q1, Q2).

All Laplacians are combinatorial: L = D - A (+ grounding), with unit bond weight.
Dirichlet ("grounded") convention:
  * grid fractals (carpet, sponge, Vicsek, square/cubic boxes): every missing neighbour that lies
    OUTSIDE the bounding box is a grounded ghost site (theta = 0); holes inside are Neumann.
  * Sierpinski gasket: the 3 corner vertices are grounded (removed).
"""
import numpy as np
import scipy.sparse as sp


# ---------------------------------------------------------------- Sierpinski gasket
def gasket(n):
    """Level-n Sierpinski gasket graph. Returns (xy, edges, corners).
    Coordinates are exact integers on a triangular lattice: point = a*e1 + b*e2, stored as (a, b)."""
    tri = {(0, 0): 0, (1, 0): 1, (0, 1): 2}
    pts = [(0, 0), (1, 0), (0, 1)]
    edges = {(0, 1), (0, 2), (1, 2)}
    for level in range(n):
        s = 2 ** level
        newpts, index, newedges = [], {}, set()
        for (sa, sb) in [(0, 0), (s, 0), (0, s)]:
            loc = []
            for (a, b) in pts:
                key = (a + sa, b + sb)
                if key not in index:
                    index[key] = len(newpts)
                    newpts.append(key)
                loc.append(index[key])
            for (i, j) in edges:
                u, v = loc[i], loc[j]
                newedges.add((min(u, v), max(u, v)))
        pts, edges = newpts, newedges
    s = 2 ** n
    index = {p: k for k, p in enumerate(pts)}
    corners = [index[(0, 0)], index[(s, 0)], index[(0, s)]]
    ab = np.array(pts, dtype=float)
    xy = np.column_stack([ab[:, 0] + 0.5 * ab[:, 1], ab[:, 1] * np.sqrt(3) / 2])
    return xy, np.array(sorted(edges)), corners


def adjacency(nv, edges, weights=None):
    w = np.ones(len(edges)) if weights is None else weights
    A = sp.coo_matrix((w, (edges[:, 0], edges[:, 1])), shape=(nv, nv))
    return (A + A.T).tocsr()


def gasket_dirichlet_laplacian(n):
    xy, e, c = gasket(n)
    A = adjacency(len(xy), e)
    L = sp.diags(np.asarray(A.sum(1)).ravel()) - A
    keep = np.setdiff1d(np.arange(len(xy)), c)
    return L[keep][:, keep].tocsc(), xy[keep]


# ---------------------------------------------------------------- grid-based fractals
def _digits_ok(coords, s, n, keep_fn):
    ok = np.ones(len(coords), bool)
    c = coords.copy()
    for _ in range(n):
        ok &= keep_fn(c % s)
        c //= s
    return ok


def grid_fractal(n, dim, s, keep_fn):
    """Cells of an s^n grid in `dim` dimensions kept iff keep_fn(digits) at every level."""
    side = s ** n
    grids = np.indices((side,) * dim).reshape(dim, -1).T
    ok = _digits_ok(grids, s, n, keep_fn)
    cells = grids[ok]
    return cells, side


def carpet_keep(d):
    return ~((d[:, 0] == 1) & (d[:, 1] == 1))


def sponge_keep(d):  # Menger sponge: remove cells with >=2 middle digits
    return (d == 1).sum(1) < 2


def vicsek_keep_factory(s):
    m = s // 2

    def keep(d):
        return (d == m).sum(1) >= d.shape[1] - 1  # cross: at most one non-middle coordinate
    return keep


def full_keep(d):
    return np.ones(len(d), bool)


def grid_laplacian(cells, side):
    """Grounded-outer-boundary Laplacian of a set of grid cells (nearest neighbours)."""
    dim = cells.shape[1]
    lin = np.ravel_multi_index(cells.T, (side,) * dim)
    order = np.argsort(lin)
    lin_sorted = lin[order]
    N = len(cells)
    rows, cols = [], []
    diag = np.zeros(N)
    for ax in range(dim):
        for sgn in (+1, -1):
            nb = cells.copy()
            nb[:, ax] += sgn
            outside = (nb[:, ax] < 0) | (nb[:, ax] >= side)
            diag += outside  # grounded ghost
            inside = ~outside
            nbl = np.ravel_multi_index(nb[inside].T, (side,) * dim)
            pos = np.searchsorted(lin_sorted, nbl)
            pos[pos >= N] = 0
            found = lin_sorted[pos] == nbl
            src = np.nonzero(inside)[0][found]
            dst = order[pos[found]]
            rows.append(src)
            cols.append(dst)
            diag[src] += 1
    rows = np.concatenate(rows)
    cols = np.concatenate(cols)
    A = sp.coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(N, N)).tocsr()
    L = sp.diags(diag) - A
    return L.tocsc()


def grid_laplacian_periodic(cells, side):
    """Laplacian of the grid-cell graph with periodic identification of opposite outer faces
    (no grounding; one zero mode)."""
    dim = cells.shape[1]
    lin = np.ravel_multi_index(cells.T, (side,) * dim)
    order = np.argsort(lin)
    lin_sorted = lin[order]
    N = len(cells)
    rows, cols = [], []
    for ax in range(dim):
        nb = cells.copy()
        nb[:, ax] = (nb[:, ax] + 1) % side
        nbl = np.ravel_multi_index(nb.T, (side,) * dim)
        pos = np.searchsorted(lin_sorted, nbl)
        pos[pos >= N] = 0
        found = lin_sorted[pos] == nbl
        src = np.nonzero(found)[0]
        dst = order[pos[found]]
        rows += [src, dst]
        cols += [dst, src]
    rows = np.concatenate(rows); cols = np.concatenate(cols)
    A = sp.coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(N, N)).tocsr()
    return (sp.diags(np.asarray(A.sum(1)).ravel()) - A).tocsr()


def mean_pinv_diag_sampled(L, nsamp=100, seed=0, rtol=1e-10):
    """(1/N) Tr L^+ for a connected graph Laplacian: dense if small, else sampled L^+_xx via CG on
    the consistent singular system L y = e_x - 1/N (y has zero mean -> y_x = L^+_xx)."""
    import scipy.sparse.linalg as spla
    N = L.shape[0]
    if N <= 5000:
        lam = np.linalg.eigvalsh(L.toarray())
        return np.mean(1 / lam[1:]) * (N - 1) / N, 0.0
    rng = np.random.default_rng(seed)
    xs = rng.choice(N, size=nsamp, replace=False)
    Minv = sp.diags(1 / L.diagonal())
    vals = []
    for x in xs:
        b = -np.ones(N) / N
        b[x] += 1
        y, info = spla.cg(L, b, rtol=rtol, maxiter=200000, M=Minv)
        y -= y.mean()
        vals.append(y[x])
    vals = np.array(vals)
    return vals.mean(), vals.std(ddof=1) / np.sqrt(nsamp)


def grid_adjacency_free(cells, side):
    """Adjacency (free boundary) for Monte Carlo / tight binding."""
    L = grid_laplacian(cells, side)
    A = -(L - sp.diags(L.diagonal()))
    return A.tocsr()


def chain_dirichlet_eigs(L):
    k = np.arange(1, L + 1)
    return 2 - 2 * np.cos(np.pi * k / (L + 1))


# ---------------------------------------------------------------- mean Green function
def mean_green_dense(L):
    """(1/N) Tr L^{-1} and eigenvalues, dense (small graphs)."""
    Ld = L.toarray() if sp.issparse(L) else L
    lam = np.linalg.eigvalsh(Ld)
    return np.mean(1.0 / lam), lam


def mean_green_sampled(L, nsamp=200, seed=0, exact_if_below=0):
    """Estimate (1/N) Tr L^{-1} by exact G(x,x) at uniformly random sites x (sparse LU).
    Returns (mean, standard error)."""
    import scipy.sparse.linalg as spla
    N = L.shape[0]
    if N <= exact_if_below:
        g, _ = mean_green_dense(L)
        return g, 0.0
    rng = np.random.default_rng(seed)
    xs = rng.choice(N, size=min(nsamp, N), replace=False)
    lu = spla.splu(L.tocsc())
    vals = []
    for x in xs:
        b = np.zeros(N)
        b[x] = 1.0
        vals.append(lu.solve(b)[x])
    vals = np.array(vals)
    return vals.mean(), vals.std(ddof=1) / np.sqrt(len(vals))
