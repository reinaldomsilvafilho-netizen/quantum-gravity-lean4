"""Independent verifier, B claims 1-2: exact (sympy) classification of the involutions of B3
with circulant (DFT-diagonalized) charged leptons. No random sampling (the draft sampled).

For G a real symmetric involution, G^T M G = M  <=>  [M, G] = 0, hence [M^dag M, G] = 0 and a
nondegenerate eigenvector v of G is an eigenvector of M^dag M: it is a PMNS column up to phases,
|U_col| = |Uw^dag v|. Oracle: exact |.|^2 in sympy. Numerical cross-check: a random G-invariant
Majorana matrix, diagonalized with numpy, must contain that column.
Negative control: G = identity / a 3-cycle (not an involution) must be rejected; a random matrix
without symmetry must not contain the column.
"""
import itertools
import numpy as np
import sympy as sp

w = sp.exp(2 * sp.pi * sp.I / 3)
Uw = sp.Matrix(3, 3, lambda i, j: w ** (i * j)) / sp.sqrt(3)
ok = []


def check(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


classes = {}
n_inv = 0
for perm in itertools.permutations(range(3)):
    for sg in itertools.product([1, -1], repeat=3):
        G = sp.zeros(3)
        for i, j in enumerate(perm):
            G[i, j] = sg[i]
        if G * G != sp.eye(3) or G == sp.eye(3) or G == -sp.eye(3):
            continue
        n_inv += 1
        for val, mult, vecs in G.eigenvects():
            if mult == 1:
                v = vecs[0] / vecs[0].norm()
                col = Uw.H * v
                mod2 = tuple(sorted((sp.nsimplify(sp.simplify(sp.Abs(x) ** 2)) for x in col), reverse=True))
                kind = "transposition" if perm != (0, 1, 2) and len(set(sg)) == 1 else (
                    "sign flips only" if perm == (0, 1, 2) else "transposition x signs")
                classes.setdefault(mod2, []).append((perm, sg, kind))
print("non-trivial involutions of B3 (excluding +-1):", n_inv)
check("18 non-trivial involutions besides -1 (19 incl. -1)", n_inv == 18)
for k, v in classes.items():
    print(f"|col|^2 = {k}: {len(v)} generators, kinds {sorted(set(x[2] for x in v))}")
check("exactly three fixed columns, 6 generators each",
      len(classes) == 3 and all(len(v) == 6 for v in classes.values()))
check("pure vertex transpositions give (1/2,1/2,0): a zero PMNS entry",
      all(x[2] != "transposition" or k == (sp.Rational(1, 2), sp.Rational(1, 2), 0) for k, v in classes.items() for x in v)
      and (sp.Rational(1, 2), sp.Rational(1, 2), 0) in classes)
check("sign flips only -> TM2 column (1/3,1/3,1/3)",
      all(x[2] == "sign flips only" for x in classes[(sp.Rational(1, 3),) * 3]))
check("transposition x opposite sign on the swapped pair -> TM1 column (2/3,1/6,1/6)",
      (sp.Rational(2, 3), sp.Rational(1, 6), sp.Rational(1, 6)) in classes)
# also: the transposition class includes (23) with signs (-1,-1,-1)... i.e. -P : same eigvectors
# analytic: Uw^dag (0,1,-1)/sqrt2 has entry k=0 equal to (1-1)/sqrt6 = 0 for every labelling
v = sp.Matrix([0, 1, -1]) / sp.sqrt(2)
check("analytic zero: first entry of Uw^dag (0,1,-1)/sqrt2 is exactly 0", sp.simplify((Uw.H * v)[0]) == 0)

# numerical cross-check
rng = np.random.default_rng(7)
Uwn = np.array(Uw.evalf(), dtype=complex)


def contains(G, target):
    X = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    X = X + X.T
    M = (X + G @ X @ G) / 2 if G is not None else X
    _, V = np.linalg.eigh(M.conj().T @ M)
    U = Uwn.conj().T @ V
    return any(np.allclose(sorted(np.abs(U[:, j]) ** 2), sorted(target), atol=1e-9) for j in range(3))


G_tm1 = np.array([[1, 0, 0], [0, 0, -1], [0, -1, 0]], float)
check("numeric: random G_TM1-invariant M_nu has a (2/3,1/6,1/6) column (20 samples)",
      all(contains(G_tm1, [2 / 3, 1 / 6, 1 / 6]) for _ in range(20)))
check("NC: random M_nu without symmetry has no such column", not any(contains(None, [2 / 3, 1 / 6, 1 / 6]) for _ in range(20)))
C3 = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
check("NC: 3-cycle is not an involution (filtered out)", C3 * C3 != sp.eye(3))
print(f"\nSUMMARY: {sum(ok)}/{len(ok)} PASS")
