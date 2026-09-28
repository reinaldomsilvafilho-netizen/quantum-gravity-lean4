"""Ramo E, passo 2 (draft, unverified).

Group: signed permutations of the 3 vertices of Delta_2 (hyperoctahedral B3, 48 elements):
the S3 of the triangle plus an orientation sign at each vertex.
Charged leptons: circulant (residual Z3). Neutrinos: residual Z2 = an involution G in B3.
For each G with a nondegenerate eigenvector v, the PMNS matrix has the fixed column
|Uw^dagger v|. The two remaining columns are free: an angle t and a phase p.
We fit (t, p) to the measured angles, for every assignment of the fixed column to
nu1/nu2/nu3 and every labelling of charged-lepton rows (e, mu, tau), and report the
best chi^2 and the predicted sin^2(theta12) and delta_CP.

Data (normal ordering, 1 sigma, symmetrized; CHECK against source before citing):
  NuFIT 6.0 (JHEP 12 (2024) 216), analysis IC19 without SK-atm:
  s12^2 = 0.307(12), s13^2 = 0.02195(58), s23^2 = 0.561(14).
  (IC24 with SK-atm has s23^2 = 0.470, lower octant: see tm1_delta.py for delta in both octants.)
Oracle: closed-form sum rules TM1  cos^2(t12) cos^2(t13) = 2/3,
        TM2  sin^2(t12) cos^2(t13) = 1/3, evaluated independently of the scan.
Negative control: a wrong fixed column (1,0,0) must be excluded by chi^2.
"""
import itertools
import numpy as np

w = np.exp(2j * np.pi / 3)
Uw = np.array([[1, 1, 1], [1, w, w**2], [1, w**2, w]]) / np.sqrt(3)
DATA = {"s12": (0.307, 0.012), "s13": (0.02195, 0.00058), "s23": (0.561, 0.014)}


def signed_perms():
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product([1, -1], repeat=3):
            G = np.zeros((3, 3))
            for i, j in enumerate(perm):
                G[i, j] = sg[i]
            yield perm, sg, G


def nondegenerate_vectors(G):
    vals, V = np.linalg.eigh(G)  # G symmetric for involutions in B3
    out = []
    for lam in (1, -1):
        idx = np.where(np.isclose(vals, lam))[0]
        if len(idx) == 1:
            out.append(V[:, idx[0]])
    return out


def angles(U):
    s13 = abs(U[0, 2]) ** 2
    c13 = 1 - s13
    s12 = abs(U[0, 1]) ** 2 / c13
    s23 = abs(U[1, 2]) ** 2 / c13
    J = np.imag(U[0, 0] * U[1, 1] * np.conj(U[0, 1]) * np.conj(U[1, 0]))
    c12, c23 = 1 - s12, 1 - s23
    denom = 2 * np.sqrt(s12 * c12 * s23 * c23 * s13)
    cosd = (abs(U[1, 0]) ** 2 - s12 * c23 - c12 * s23 * s13) / denom if denom > 0 else np.nan
    sind = J / (np.sqrt(s12 * c12 * s23 * c23 * s13) * c13) if denom > 0 else np.nan
    d = np.degrees(np.arctan2(sind, np.clip(cosd, -1, 1))) % 360
    return s12, s13, s23, d


def family(col, pos, row_perm, n=181, m=73):
    """All unitaries with |fixed column| = col at column index pos, rows permuted."""
    v = np.array(col, dtype=complex)[list(row_perm)]
    v /= np.linalg.norm(v)
    # orthonormal basis of v-perp
    Q, _ = np.linalg.qr(np.column_stack([v, np.eye(3)[:, 0], np.eye(3)[:, 1]]))
    if np.linalg.matrix_rank(np.column_stack([v, np.eye(3)[:, :2]])) < 3:
        Q, _ = np.linalg.qr(np.column_stack([v, np.eye(3)[:, 1], np.eye(3)[:, 2]]))
    a, b = Q[:, 1], Q[:, 2]
    for t in np.linspace(0, np.pi, n):
        for p in np.linspace(0, 2 * np.pi, m, endpoint=False):
            x = np.cos(t) * a + np.sin(t) * np.exp(1j * p) * b
            y = -np.sin(t) * np.exp(-1j * p) * a + np.cos(t) * b
            cols = [x, y]
            cols.insert(pos, v)
            yield np.column_stack(cols)


def chi2(s12, s13, s23):
    return sum(((val - DATA[k][0]) / DATA[k][1]) ** 2 for k, val in (("s12", s12), ("s13", s13), ("s23", s23)))


def best_fit(col):
    best = (np.inf, None)
    for pos in range(3):
        for rp in set(itertools.permutations(range(3))):
            for U in family(col, pos, rp):
                s12, s13, s23, d = angles(U)
                c = chi2(s12, s13, s23)
                if c < best[0]:
                    best = (c, (pos, rp, s12, s13, s23, d))
    return best


# 1. classify fixed columns produced by involutions of B3
cols = {}
for perm, sg, G in signed_perms():
    if not np.allclose(G @ G, np.eye(3)) or np.allclose(G, np.eye(3)) or np.allclose(G, -np.eye(3)):
        continue
    for v in nondegenerate_vectors(G):
        c = tuple(sorted(np.round(np.abs(Uw.conj().T @ v), 6), reverse=True))
        name = f"perm={perm} signs={sg}"
        cols.setdefault(c, []).append(name)

print("Fixed PMNS columns from involutions of B3 (circulant charged leptons):")
for c, names in cols.items():
    print(f"  |col| = {c}   from {len(names)} generators, e.g. {names[0]}")

# 2. confront each with data
print("\nBest fit per fixed column (chi^2 over s12^2, s13^2, s23^2; 3 data, 2 free params):")
for c in cols:
    chi, info = best_fit(c)
    pos, rp, s12, s13, s23, d = info
    print(f"  {c}: chi2_min = {chi:8.2f}  at nu{pos+1}, rows {rp}:  s12^2={s12:.4f} s13^2={s13:.5f} s23^2={s23:.3f} delta={d:.0f} deg")

# 3. oracle: closed-form sum rules at the measured s13^2
s13 = DATA["s13"][0]
tm1 = 1 - 2 / (3 * (1 - s13))
tm2 = 1 / (3 * (1 - s13))
print(f"\nOracle sum rules at s13^2={s13}: TM1 s12^2 = {tm1:.4f}  ({(tm1-0.307)/0.012:+.1f} sigma)"
      f";  TM2 s12^2 = {tm2:.4f}  ({(tm2-0.307)/0.012:+.1f} sigma)")

# 4. negative control
chi, _ = best_fit((1.0, 0.0, 0.0))
print(f"Negative control, fixed column (1,0,0): chi2_min = {chi:.0f} (must be huge)")
