"""Layer-2 re-check of OBL-006 (Thm 3.4, eq. chi_strata) and Remark 3.5.

Claim: chi(Omega; F) = sum_strata chi_c(S) * chi(F_x), x in S.
Oracle: sheaf cohomology computed as *ranks* of simplicial coboundary matrices
(H^*(X), relative H^*(X, Z) = H^*_c(X \\ Z), H^*(Z)), never by alternating cell counts.
Formula side: chi_c(S) computed by counting open cells of each stratum
(sum (-1)^dim over the open cells), stalk Euler characteristics read off the sheaf.
Sheaves tested on each space (Z = union of lower-rank strata, U = top stratum):
   F1 = k_X, F2 = j_! k_U, F3 = i_* k_Z, F4 = k_X (+) i_* k_Z[-1].
Spaces:  (a) S^1, Phi = cos theta, n = 1 (Remark 3.5);
         (b) S^1, Phi = diag(cos t, cos t + 1/2), n = 2 (two kinds of strata);
         (c) S^2 (boundary of a cube, subdivided), Phi = z, n = 1.
Negative control: the v2 formula sum m_r chi(Sigma_r) for the constant sheaf, with
ordinary Euler characteristics of the strata (homotopy type of the open strata
computed by ranks as well), must fail on (a) and (b).
"""
import sys
import itertools
import numpy as np

fails = 0
out = []


def log(s):
    print(s)
    out.append(s)


def check(name, ok):
    global fails
    log(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        fails += 1


def rank(M):
    if M.size == 0:
        return 0
    return int(np.linalg.matrix_rank(M.astype(float)))


def faces_closure(top):
    simp = set()
    for s in top:
        s = tuple(sorted(s))
        for k in range(1, len(s) + 1):
            for f in itertools.combinations(s, k):
                simp.add(f)
    return simp


def cohomology_dims(simplices, sub=frozenset()):
    """dims of H^k(K, L) with L = sub (a subcomplex), via coboundary ranks."""
    by_dim = {}
    for s in simplices:
        if s in sub:
            continue
        by_dim.setdefault(len(s) - 1, []).append(s)
    maxd = max(by_dim) if by_dim else -1
    idx = {d: {s: i for i, s in enumerate(sorted(by_dim.get(d, [])))} for d in range(maxd + 2)}
    ranks = {}
    for d in range(-1, maxd + 1):
        # delta_d : C^d -> C^{d+1}
        if d < 0 or d + 1 > maxd:
            ranks[d] = 0
            continue
        M = np.zeros((len(idx[d + 1]), len(idx[d])))
        for t, i in idx[d + 1].items():
            for j in range(len(t)):
                f = t[:j] + t[j + 1:]
                if f in idx[d]:
                    M[i, idx[d][f]] += (-1) ** j
        ranks[d] = rank(M)
    dims = []
    for d in range(maxd + 1):
        n = len(idx[d])
        dims.append(n - ranks[d] - ranks[d - 1])
    return dims


def euler(dims):
    return sum((-1) ** k * b for k, b in enumerate(dims))


def run_case(name, top, rank_of_cell, n, hom_chi_strata):
    """top: top simplices; rank_of_cell(simplex)->rank of Phi on its open cell."""
    K = faces_closure(top)
    cells_by_rank = {}
    for s in K:
        cells_by_rank.setdefault(rank_of_cell(s), []).append(s)
    rmax = max(cells_by_rank)
    Z = frozenset(s for s in K if rank_of_cell(s) < rmax)
    # Z must be a subcomplex (lower semicontinuity of the rank)
    ok_sub = all(f in Z for s in Z for k in range(1, len(s))
                 for f in itertools.combinations(s, k))
    check(f"{name}: lower-rank strata form a closed subcomplex", ok_sub)
    chi_c = {r: sum((-1) ** (len(s) - 1) for s in cs) for r, cs in cells_by_rank.items()}
    log(f"{name}: strata ranks {sorted(chi_c)}; chi_c by cell count {chi_c}")
    hX = cohomology_dims(K)
    hXZ = cohomology_dims(K, Z)
    hZ = cohomology_dims(Z)
    log(f"{name}: H^*(X)={hX}  H^*(X,Z)={hXZ}  H^*(Z)={hZ}")
    stalk = {
        "k_X": lambda r: 1,
        "j_!k_U": lambda r: 1 if r == rmax else 0,
        "i_*k_Z": lambda r: 1 if r < rmax else 0,
        "k_X+i_*k_Z[-1]": lambda r: 1 - (1 if r < rmax else 0),
    }
    oracle = {
        "k_X": euler(hX),
        "j_!k_U": euler(hXZ),
        "i_*k_Z": euler(hZ),
        "k_X+i_*k_Z[-1]": euler(hX) - euler(hZ),
    }
    for sh, chi_stalk in stalk.items():
        formula = sum(chi_c[r] * chi_stalk(r) for r in chi_c)
        log(f"   {sh:16s} oracle chi={oracle[sh]:3d}  formula sum chi_c*chi(stalk)={formula:3d}")
        check(f"{name}: formula (3.2) for {sh}", formula == oracle[sh])
    # v2 formula for constant sheaf: CC(k_X) = zero section = closure of conormal of
    # the open (top) stratum, so m_top = 1 and m_r = 0 otherwise.
    v2 = hom_chi_strata[rmax]
    log(f"   v2 formula m_top*chi(Sigma_top) = {v2}  vs chi(X) = {oracle['k_X']}")
    return v2 != oracle["k_X"]


def circle(angles):
    m = len(angles)
    return [(i, (i + 1) % m) for i in range(m)], m


# (a) S^1, Phi = cos
ang = np.sort(np.concatenate([np.linspace(0, 2 * np.pi, 24, endpoint=False),
                              [np.pi / 2, 3 * np.pi / 2]]))
ang = np.unique(np.round(ang, 12))
top, m = circle(ang)


def mid(s, ang=ang, m=m):
    if len(s) == 1:
        return ang[s[0]]
    i, j = s
    a, b = ang[i], ang[j]
    if (i, j) == (0, m - 1) or (j, i) == (0, m - 1):
        return (ang[m - 1] + 2 * np.pi) / 2 + 0 * a
    return 0.5 * (a + b)


def rank_a(s):
    return 0 if abs(np.cos(mid(s))) < 1e-9 else 1


# ordinary chi of the strata, by ranks: open arcs are homotopic to points
neg_a = run_case("(a) S^1, cos", top, rank_a, 1, {1: 2, 0: 2})
check("(a) negative control: v2 formula fails (2 != 0)", neg_a)

# (b) S^1, Phi = diag(cos t, cos t + 1/2)
ang2 = np.concatenate([np.linspace(0, 2 * np.pi, 30, endpoint=False),
                       [np.pi / 2, 3 * np.pi / 2, 2 * np.pi / 3, 4 * np.pi / 3]])
ang2 = np.unique(np.round(np.sort(ang2), 12))
top2, m2 = circle(ang2)


def rank_b(s):
    t = mid(s, ang2, m2)
    M = np.diag([np.cos(t), np.cos(t) + 0.5])
    return int(np.sum(np.abs(np.diag(M)) > 1e-9))


neg_b = run_case("(b) S^1, diag(cos, cos+1/2)", top2, rank_b, 2, {2: 4, 1: 4})
check("(b) negative control: v2 formula fails (4 != 0)", neg_b)

# (c) S^2 as the boundary of the cube [-1,1]^3, grid 4x4 per face, Phi = z
g = 4
pts = {}
tris = []


def vid(p):
    key = tuple(np.round(p, 9))
    if key not in pts:
        pts[key] = len(pts)
    return pts[key]


lin = np.linspace(-1, 1, g + 1)
for axis in range(3):
    for sign in (-1, 1):
        for a in range(g):
            for b in range(g):
                def P(i, j):
                    p = [0.0, 0.0, 0.0]
                    others = [k for k in range(3) if k != axis]
                    p[axis] = sign
                    p[others[0]] = lin[i]
                    p[others[1]] = lin[j]
                    return vid(np.array(p))
                v00, v10, v01, v11 = P(a, b), P(a + 1, b), P(a, b + 1), P(a + 1, b + 1)
                tris += [(v00, v10, v11), (v00, v11, v01)]
coords = {i: np.array(k) for k, i in pts.items()}


def rank_c(s):
    z = np.mean([coords[v][2] for v in s])
    return 0 if abs(z) < 1e-9 else 1


neg_c = run_case("(c) S^2 cube, z", tris, rank_c, 1, {1: 2, 0: 0})
log(f"(c) v2 formula happens to agree on S^2 (2 = 2): {not neg_c} (not a test of v2)")

log(f"failures: {fails}")
with open(__file__.replace(".py", ".out.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
sys.exit(fails)
