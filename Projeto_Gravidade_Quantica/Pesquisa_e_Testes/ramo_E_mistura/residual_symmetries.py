"""Ramo E, passo 1: which residual symmetries of the triangle Delta_2 give viable lepton mixing?

Setup (draft, unverified):
- Basis: the 3 vertices of Delta_2. S3 acts by permutation matrices.
- Charged leptons: M_l M_l^dagger circulant (residual Z3 = cyclic rotation), as in the fermion paper.
- Neutrinos: complex symmetric M_nu invariant under a residual Z2 generator G: G^T M_nu G = M_nu.
- PMNS = U_l^dagger U_nu. Entries of |U| that are the same for every random sample
  are fixed by the symmetry alone (the "prediction").

Candidate Z2 generators:
- vertex transpositions (elements of S3);
- vertex sign flips diag(1,-1,-1) (orientation reversal at two vertices; not in S3,
  but together with the Z3 rotation generates A4 = rotation group of the tetrahedron);
- the S4 element S*U, where U = transposition (2 3) and S = the A4 order-2 element
  written in the circulant basis (standard TM1 generator).

Independent oracle: the fixed column is compared with the closed form obtained by hand
(U_omega^dagger times the eigenvector of G with a nondegenerate eigenvalue).
Negative control: a matrix with no residual symmetry must give no fixed entries.
"""
import numpy as np

rng = np.random.default_rng(1)
w = np.exp(2j * np.pi / 3)
Uw = np.array([[1, 1, 1], [1, w, w**2], [1, w**2, w]]) / np.sqrt(3)  # diagonalizes circulants

P = {  # transpositions of the vertices
    "(12)": np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]]),
    "(23)": np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]]),
    "(13)": np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]]),
}
signs = {
    "diag(1,-1,-1)": np.diag([1, -1, -1]),
    "diag(-1,1,-1)": np.diag([-1, 1, -1]),
}
# A4 'S' generator in the basis where the Z3 generator T is the cyclic permutation:
# S = Uw diag(1,-1,-1) Uw^dagger is the usual form; build it and S*U with U=(23).
S_circ = (Uw @ np.diag([1, -1, -1]) @ Uw.conj().T).real
extra = {"S_A4(circ)": S_circ, "S_A4*U(23)": S_circ @ P["(23)"]}


def random_invariant(G):
    """Random complex symmetric M with G^T M G = M (average over the group {1,G})."""
    X = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    X = X + X.T
    return (X + G.T @ X @ G) / 2


def pmns(Mnu):
    """PMNS with charged leptons diagonalized by Uw (circulant); columns sorted by |m_nu|."""
    H = Mnu.conj().T @ Mnu
    vals, V = np.linalg.eigh(H)
    U = Uw.conj().T @ V
    return np.abs(U[:, np.argsort(vals)])


def fixed_entries(G, n=400):
    Us = np.array([pmns(random_invariant(G)) for _ in range(n)])
    # an entry is 'fixed' if it is constant across samples, up to column relabelling:
    # compare sorted column magnitudes
    cols = np.sort(Us, axis=1)  # sort within each column
    out = []
    for j in range(3):
        pass
    # search for a column that is identical (as a set of |entries|) in all samples
    ref = None
    found = []
    for s in range(n):
        cs = [tuple(np.round(np.abs(Us[s][:, j]), 6)) for j in range(3)]
        found.append(set(cs))
    common = set.intersection(*found)
    return common


def report(name, G):
    assert np.allclose(G @ G, np.eye(3)), name
    common = fixed_entries(G)
    print(f"{name:16s} fixed |column|s: {sorted(common) if common else 'none'}")
    return common


print("Charged leptons circulant (Z3 of Delta_2).  Neutrino residual Z2:")
res = {}
for d in (P, signs, extra):
    for k, G in d.items():
        res[k] = report(k, G)

# Oracle: for (23) the nondegenerate eigenvector is (0,1,-1)/sqrt2 -> column Uw^dag (0,1,-1)/sqrt2
v = np.array([0, 1, -1]) / np.sqrt(2)
col = tuple(np.round(np.abs(Uw.conj().T @ v), 6))
print("oracle (23):", col, "matches:", any(np.allclose(sorted(col), sorted(c)) for c in res["(23)"]))
# Oracle for diag(1,-1,-1): eigenvector (1,0,0) -> Uw^dag e1 = (1,1,1)/sqrt3  (trimaximal, TM2)
col = tuple(np.round(np.abs(Uw.conj().T @ np.array([1, 0, 0])), 6))
print("oracle diag(1,-1,-1):", col, "matches:",
      any(np.allclose(sorted(col), sorted(c)) for c in res["diag(1,-1,-1)"]))

# Negative control: no symmetry
Us = [pmns((lambda X: X + X.T)(rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)))) for _ in range(50)]
common = set.intersection(*[set(tuple(np.round(u[:, j], 6)) for j in range(3)) for u in Us])
print("negative control (no symmetry): fixed columns:", common if common else "none (OK)")
