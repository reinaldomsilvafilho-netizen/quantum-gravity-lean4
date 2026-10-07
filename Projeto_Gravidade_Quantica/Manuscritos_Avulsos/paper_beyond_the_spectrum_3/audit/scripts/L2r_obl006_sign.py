"""L2r: sign in OBL-006, (d theta)^m = m! (-1)^{m(m+1)/2} dx_1..dx_m dxi_1..dxi_m.

Oracle: the Pfaffian of the matrix Om_ab = omega(e_a, e_b), omega = sum_i dxi_i ^ dx_i,
in the ordered basis (dx_1..dx_m, dxi_1..dxi_m), computed by brute-force expansion
over perfect matchings (no closed formula used). omega^m / m! = Pf(Om) e^1^..^e^{2m}.
Negative controls: (-1)^{m(m-1)/2} and (-1)^m must disagree for some m.
Constant-sheaf sanity: with RHS sign s_m and self-intersection of the zero
section in the (d theta)^m orientation equal to s_m * chi (base-then-fibre value chi),
chi(X) = s_m * s_m * chi = chi; for the mutated sign it gives -chi when m = 2 (S^2: -2).
Exit code = number of failures.
"""
import sys
from fractions import Fraction

out, fail = [], 0


def log(s):
    out.append(s)
    print(s)


def pfaffian(M):
    n = len(M)
    if n == 0:
        return Fraction(1)
    total = Fraction(0)
    # expand along first row: Pf = sum_j (-1)^{j+1} M[0][j] Pf(M without 0, j)  (j 1-based offset)
    for j in range(1, n):
        if M[0][j] == 0:
            continue
        idx = [k for k in range(n) if k not in (0, j)]
        sub = [[M[a][b] for b in idx] for a in idx]
        total += (-1) ** (j + 1) * M[0][j] * pfaffian(sub)
    return total


for m in range(1, 7):
    n = 2 * m
    Om = [[Fraction(0)] * n for _ in range(n)]
    for i in range(m):
        x, xi = i, m + i
        # omega = dxi ^ dx : omega(e_x, e_xi) = dxi(e_x)dx(e_xi) - dxi(e_xi)dx(e_x) = -1
        Om[x][xi] = Fraction(-1)
        Om[xi][x] = Fraction(1)
    pf = pfaffian(Om)
    claimed = (-1) ** (m * (m + 1) // 2)
    ok = pf == claimed
    fail += not ok
    log(f"m={m}: Pf={pf} claimed (-1)^(m(m+1)/2)={claimed} {'ok' if ok else 'FAIL'}")

# sanity: Pfaffian routine on standard symplectic J (e_i, e_{m+i}) -> +1 for the
# pairing omega(e_x, e_xi)=+1, i.e. dx^dxi: Pf must be (-1)^{m(m-1)/2}
for m in range(1, 5):
    n = 2 * m
    J = [[Fraction(0)] * n for _ in range(n)]
    for i in range(m):
        J[i][m + i], J[m + i][i] = Fraction(1), Fraction(-1)
    ok = pfaffian(J) == (-1) ** (m * (m - 1) // 2)
    fail += not ok
    log(f"routine check m={m}: Pf(sum dx^dxi) = (-1)^(m(m-1)/2): {'ok' if ok else 'FAIL'}")

mut1 = [m for m in range(1, 7) if (-1) ** (m * (m - 1) // 2) != (-1) ** (m * (m + 1) // 2)]
mut2 = [m for m in range(1, 7) if (-1) ** m != (-1) ** (m * (m + 1) // 2)]
log(f"negative control (-1)^(m(m-1)/2) differs at m={mut1}; (-1)^m differs at m={mut2}")
if not mut1 or not mut2:
    fail += 1

# constant sheaf on S^2 (m=2, chi=2), T^2 (chi=0), S^4 (m=4, chi=2), RP^2 handled via
# local coefficients (chi=1, m=2)
for name, m, chi in (("S^2", 2, 2), ("T^2", 2, 0), ("RP^2", 2, 1), ("S^4", 4, 2), ("S^6", 6, 2)):
    s = (-1) ** (m * (m + 1) // 2)
    self_int = s * chi  # zero section . zero section in (d theta)^m orientation
    rhs = s * self_int
    rhs_unsigned = self_int  # pre-fix formula without sign
    ok = rhs == chi
    fail += not ok
    log(f"{name}: (-1)^(m(m+1)/2) CC.[0] = {rhs} vs chi={chi} {'ok' if ok else 'FAIL'};"
        f" unsigned formula gives {rhs_unsigned}{' (wrong)' if rhs_unsigned != chi else ''}")
log(f"failures={fail}")
with open(__file__.replace(".py", ".out.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
sys.exit(fail)
