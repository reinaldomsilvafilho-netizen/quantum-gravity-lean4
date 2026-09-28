"""Mean-field attractive-Hubbard BdG on 1D periodic chains of arbitrary unit cells (Q2).

Conventions (e = hbar = 1, t = 1):
  H0 = sum_bonds -t_ij (c_i^dag c_j + h.c.),  bonds (a, b, dR, t) connect orbital a in cell R
  to orbital b in cell R + dR.  Positions X_a are Cartesian x-coordinates along the chain; the
  cell length is a0.  A uniform vector potential A along x enters by Peierls substitution
  t_ij -> t_ij exp(i A (X_i - X_j)); in the periodic-position Bloch gauge this is h(k) -> h(k - A).
  BdG in Nambu basis (c_{k up}, c^dag_{-k down}):
        H_BdG(k) = [[h(k - A) - mu, Delta], [Delta^*, -(h(k + A) - mu)]]
  Grand potential per cell at T = 0 (constants dropped):
        Omega/M = (1/M) sum_k [ sum_{E<0} E  + Tr(h(k+A) - mu) ] + sum_a |Delta_a|^2 / U
  Superfluid weight per unit length: D_s = (1/a0) d^2(Omega/M)/dA^2 (grand canonical, fixed mu).
"""
import numpy as np


class Chain:
    def __init__(self, X, bonds, a0, onsite=None):
        self.X = np.asarray(X, float)
        self.N = len(self.X)
        self.bonds = bonds  # list of (a, b, dR, t)
        self.a0 = float(a0)
        self.onsite = np.zeros(self.N) if onsite is None else np.asarray(onsite, float)

    def hk(self, k):
        """Bloch Hamiltonian, periodic-position gauge: h_ab = sum -t exp(-i k (X_a - X_b - dR a0))."""
        h = np.diag(self.onsite).astype(complex)
        for (a, b, dR, t) in self.bonds:
            ph = np.exp(-1j * k * (self.X[a] - (self.X[b] + dR * self.a0)))
            h[a, b] += -t * ph
            h[b, a] += -t * np.conj(ph)
        return h

    def hk_vectorized(self, ks):
        ks = np.atleast_1d(ks)
        a = np.array([b[0] for b in self.bonds])
        b = np.array([bb[1] for bb in self.bonds])
        dR = np.array([bb[2] for bb in self.bonds], float)
        t = np.array([bb[3] for bb in self.bonds], float)
        d = self.X[a] - (self.X[b] + dR * self.a0)
        H = np.zeros((len(ks), self.N, self.N), complex)
        H[:, np.arange(self.N), np.arange(self.N)] = self.onsite
        ph = -t[None, :] * np.exp(-1j * ks[:, None] * d[None, :])
        for j in range(len(a)):
            H[:, a[j], b[j]] += ph[:, j]
            H[:, b[j], a[j]] += np.conj(ph[:, j])
        return H


def kgrid(M, a0):
    return 2 * np.pi * (np.arange(M) + 0.5) / (M * a0)


def bdg_step(ch, Delta, mu, A, ks, U, hp=None, hm=None):
    """One evaluation: returns (Omega per cell, new Delta, density per orbital)."""
    N = ch.N
    if hp is None:
        hp = ch.hk_vectorized(ks - A)
        hm = ch.hk_vectorized(ks + A)
    M = len(ks)
    Hb = np.zeros((M, 2 * N, 2 * N), complex)
    Hb[:, :N, :N] = hp - mu * np.eye(N)
    Hb[:, N:, N:] = -(hm - mu * np.eye(N))
    Hb[:, :N, N:] = np.diag(Delta)
    Hb[:, N:, :N] = np.diag(np.conj(Delta))
    E, V = np.linalg.eigh(Hb)
    neg = E < 0
    Omega = (np.sum(E[neg]) + np.sum(np.real(np.trace(hm, axis1=1, axis2=2))) - M * N * mu) / M
    if U > 0:
        Omega += np.sum(np.abs(Delta) ** 2) / U
    u = V[:, :N, :]
    v = V[:, N:, :]
    pos = ~neg
    # F_a = <c_{k up a} c_{-k down a}> = sum_{E>0} u_a v_a^*
    F = np.einsum('kan,kan,kn->a', u, np.conj(v), pos) / M
    nup = np.einsum('kan,kn->a', np.abs(u) ** 2, neg) / M
    ndn = 1 - np.einsum('kan,kn->a', np.abs(v) ** 2, neg) / M
    return Omega, U * F, nup + ndn


def solve_sc(ch, mu, A, ks, U, Delta0, tol=1e-11, maxit=3000, mix=1.0):
    hp = ch.hk_vectorized(ks - A)
    hm = ch.hk_vectorized(ks + A)
    D = np.array(Delta0, complex)
    for it in range(maxit):
        Om, Dn, n = bdg_step(ch, D, mu, A, ks, U, hp, hm)
        err = np.max(np.abs(Dn - D))
        D = (1 - mix) * D + mix * Dn
        if err < tol:
            break
    Om, Dn, n = bdg_step(ch, D, mu, A, ks, U, hp, hm)
    return D, Om, n, it, err


def superfluid_weight(ch, mu, ks, U, Delta_sc, dA=None, relax=True, tol=1e-11):
    """Five-point second derivative of Omega/M in A, divided by a0. Returns (Ds, Omega values)."""
    if dA is None:
        dA = 0.02 / ch.a0
    As = dA * np.array([-2, -1, 0, 1, 2])
    Om = []
    for A in As:
        if relax:
            D, O, _, _, _ = solve_sc(ch, mu, A, ks, U, Delta_sc, tol=tol)
        else:
            O, _, _ = bdg_step(ch, Delta_sc, mu, A, ks, U)
        Om.append(O)
    Om = np.array(Om)
    d2 = (-Om[0] + 16 * Om[1] - 30 * Om[2] + 16 * Om[3] - Om[4]) / (12 * dA ** 2)
    return d2 / ch.a0, Om


def total_density(ch, mu, ks, U, Delta0):
    D, O, n, it, err = solve_sc(ch, mu, 0.0, ks, U, Delta0)
    return np.sum(n), D


# ------------------------------------------------------------------ lattices
def gasket_chain(n):
    """Chain of level-n gaskets joined corner-to-corner along x (right-bottom corner of cell R
    identified with left-bottom corner of cell R+1). Unit cell = gasket minus its right-bottom corner."""
    import fractal_graphs as fg
    xy, edges, corners = fg.gasket(n)
    c0, c1, c2 = corners
    keep = [i for i in range(len(xy)) if i != c1]
    idx = {v: j for j, v in enumerate(keep)}
    bonds = []
    for (u, v) in edges:
        if u == c1 or v == c1:
            w = v if u == c1 else u
            bonds.append((idx[w], idx[c0], +1, 1.0))
        else:
            bonds.append((idx[u], idx[v], 0, 1.0))
    X = xy[keep, 0]
    a0 = 2.0 ** n
    return Chain(X, bonds, a0), xy[keep]


def cross_stitch(tperp=1.0, t=1.0, sameX=True):
    """Cross-stitch ladder: orbitals a, b in each cell; a-b rung tperp; a-a, b-b, a-b', b-a' hops t.
    The antisymmetric combination (a-b)/sqrt2 is an exact flat band of strictly one-cell CLS."""
    X = [0.0, 0.0] if sameX else [0.0, 0.3]
    bonds = [(0, 1, 0, tperp), (0, 0, 1, t), (1, 1, 1, t), (0, 1, 1, t), (1, 0, 1, t)]
    return Chain(X, bonds, 1.0)


def disconnected_cells(ch):
    """Same unit cell with every inter-cell bond removed (trivially D_s = 0)."""
    return Chain(ch.X, [b for b in ch.bonds if b[2] == 0], ch.a0, ch.onsite)
