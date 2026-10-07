"""Round-2 checks for the functorial tensor paper (A7, M11, N1, N4).

Each check has an independent oracle and a negative control. Fixed seed.
Output: round2_checks.out.txt. Exit code = number of failures.
"""
import sys
import numpy as np
import sympy as sp

rng = np.random.default_rng(20261006)
fails = 0
out = []


def report(name, ok, msg):
    global fails
    out.append(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}")
    if not ok:
        fails += 1


# ---------- R1 (A7): n n (G + Lambda g) for -N0^2 dt^2 + a^2 delta ----------
t, N0, Lam = sp.symbols("t N0 Lambda", positive=True)
x = sp.symbols("x1:4")
a = sp.Function("a")(t)
X = (t,) + x
g = sp.diag(-N0**2, a**2, a**2, a**2)
gi = g.inv()
Gam = [[[sp.simplify(sum(gi[l, m] * (sp.diff(g[m, i], X[j]) + sp.diff(g[m, j], X[i])
                                        - sp.diff(g[i, j], X[m])) for m in range(4)) / 2)
         for j in range(4)] for i in range(4)] for l in range(4)]


def ricci(i, j):
    r = 0
    for l in range(4):
        r += sp.diff(Gam[l][i][j], X[l]) - sp.diff(Gam[l][i][l], X[j])
        for m in range(4):
            r += Gam[l][l][m] * Gam[m][i][j] - Gam[l][j][m] * Gam[m][i][l]
    return sp.simplify(r)


Ric = sp.Matrix(4, 4, lambda i, j: ricci(i, j))
Rs = sp.simplify(sum(gi[i, j] * Ric[i, j] for i in range(4) for j in range(4)))
G = Ric - Rs * g / 2
n = sp.Matrix([1 / N0, 0, 0, 0])
lhs = sp.simplify((n.T * (G + Lam * g) * n)[0])
claimed = 3 * sp.diff(a, t)**2 / (N0**2 * a**2) - Lam
old = 3 * sp.diff(a, t)**2 / (N0**2 * a**2)
report("R1 nn(G+Lg) = 3adot^2/(N0^2a^2) - Lambda", sp.simplify(lhs - claimed) == 0, str(lhs))
report("R1 control: display without -Lambda fails", sp.simplify(lhs - old) != 0,
       f"difference {sp.simplify(lhs - old)}")


# ---------- helpers: QFI by formula and by fidelity (independent oracle) ----------
def qfi_formula(T, x0, h=1e-5):
    v = T(x0)
    d = len(x0)
    dT = []
    for i in range(d):
        e = np.zeros(d); e[i] = h
        dT.append((T(x0 + e) - T(x0 - e)) / (2 * h))
    gm = np.zeros((d, d))
    for i in range(d):
        for j in range(d):
            pj = dT[j] - np.vdot(v, dT[j]) * v
            gm[i, j] = 4 * np.real(np.vdot(dT[i], pj))
    return gm


def qfi_fidelity(T, x0, h=1e-4):
    # g(u,u) = lim 8 (1 - |<T(x),T(x+hu)>|) / h^2 ; polarize for off-diagonals
    d = len(x0)
    v = T(x0)

    def q(u):
        f = abs(np.vdot(v, T(x0 + h * u)))
        f2 = abs(np.vdot(v, T(x0 - h * u)))
        return 4 * ((1 - f) + (1 - f2)) / h**2
    E = np.eye(d)
    gm = np.zeros((d, d))
    for i in range(d):
        gm[i, i] = q(E[i])
    for i in range(d):
        for j in range(i + 1, d):
            gm[i, j] = gm[j, i] = (q(E[i] + E[j]) - gm[i, i] - gm[j, j]) / 2
    return gm


# ---------- R2 (M11): t-dependent phase leaves endpoints and h fixed ----------
def bump(s):
    return np.where(s > 0, np.exp(-1 / np.maximum(s, 1e-300)), 0.0)


def smoothstep(s):  # 0 for s<=0, 1 for s>=1, C^infty
    return bump(s) / (bump(s) + bump(1 - s))


L, eps = 1.0, 0.25
theta = lambda tt: 0.3 + 0.4 * smoothstep((tt - eps) / (L - 2 * eps))   # sits near ends
bfun = lambda tt: np.pi * smoothstep((tt - eps) / 0.1) * smoothstep((L - eps - tt) / 0.1)


def T_prod(th, phase=0.0, xdep=False):
    def T(xv):
        vec = np.array([1.0 + 0j])
        for k in range(3):
            ph = np.exp(1j * phase * np.cos(xv[0])) if (xdep and k == 0) else 1.0
            f = np.array([np.cos(th), np.exp(1j * xv[k]) * np.sin(th) * ph])
            vec = np.kron(vec, f)
        return vec if xdep else np.exp(1j * phase) * vec
    return T


x0 = rng.uniform(0, 2 * np.pi, 3)
end_diff = max(np.linalg.norm(T_prod(theta(tt), bfun(tt))(x0) - T_prod(theta(tt))(x0))
               for tt in [0.0, 0.1, 0.9, 1.0])
mid = L / 2
mid_diff = np.linalg.norm(T_prod(theta(mid), bfun(mid))(x0) - T_prod(theta(mid))(x0))
report("R2 endpoints/sitting intervals unchanged", end_diff < 1e-14, f"max diff {end_diff:.2e}")
report("R2 morphism changed at t=L/2", abs(mid_diff - 2.0) < 1e-12, f"|T'-T| = {mid_diff:.6f} (oracle 2)")
qd = max(np.max(np.abs(qfi_formula(T_prod(theta(tt), bfun(tt)), x0)
                       - qfi_formula(T_prod(theta(tt)), x0))) for tt in np.linspace(0, 1, 11))
report("R2 h(t) unchanged (formula)", qd < 1e-8, f"max |dh| {qd:.2e}")
oracle = np.sin(2 * theta(mid))**2 * np.eye(3)
qf = qfi_fidelity(T_prod(theta(mid), bfun(mid)), x0)
report("R2 h(L/2) = sin^2(2 theta) delta via fidelity oracle", np.max(np.abs(qf - oracle)) < 1e-5,
       f"err {np.max(np.abs(qf - oracle)):.2e}")
qc = np.max(np.abs(qfi_formula(T_prod(theta(mid), bfun(mid), xdep=True), x0) - oracle))
report("R2 control: x-dependent phase changes h", qc > 1e-2, f"|dh| {qc:.3f}")


# ---------- R3 (N1): Lemma construction T = (e0 + sum iota_k e_k)/sqrt(1+|iota|^2) ----------
def iota(xv):
    return np.concatenate([np.cos(xv), np.sin(xv)])  # immersion T^3 -> R^6


def T_lemma(xv):
    f = np.concatenate([[1.0], iota(xv)]).astype(complex)
    return f / np.linalg.norm(f)


mins, errs = [], []
for _ in range(50):
    xv = rng.uniform(0, 2 * np.pi, 3)
    gF = qfi_formula(T_lemma, xv)
    gO = qfi_fidelity(T_lemma, xv)
    mins.append(np.linalg.eigvalsh(gF).min())
    errs.append(np.max(np.abs(gF - gO)))
# analytic oracle: |iota|^2 = 3 constant, so T = f/2 and P dT = dT/2 -> g = 4*(1/4)*delta = delta
gA = qfi_formula(T_lemma, np.array([0.3, 1.1, 2.0]))
report("R3 Lemma field projectively immersed (min eig > 0)", min(mins) > 0.5, f"min eig {min(mins):.4f}")
report("R3 formula vs fidelity oracle", max(errs) < 1e-5, f"max err {max(errs):.2e}")
report("R3 analytic oracle g = delta", np.max(np.abs(gA - np.eye(3))) < 1e-8, f"err {np.max(np.abs(gA - np.eye(3))):.2e}")


def T_c2(xv):  # dim H = 2: the ray map lands in a 2-dim manifold
    v = np.array([np.cos(xv[0] + 0.3 * xv[2]), np.exp(1j * (xv[1] + xv[2])) * np.sin(xv[0] + 0.3 * xv[2])])
    return v


m2 = min(np.linalg.eigvalsh(qfi_formula(T_c2, rng.uniform(0.2, 1.2, 3))).min() for _ in range(20))
report("R3 control: C^2 field is never immersed (min eig ~ 0)", abs(m2) < 1e-6, f"min eig {m2:.2e}")

# ---------- R4 (N4): alpha'(s) >= 1/2 on [0,1]^2, sharp ----------
S, S0 = np.meshgrid(np.linspace(0, 1, 2001), np.linspace(0, 1, 2001))
ap = 1 + 0.5 * ((1 - 2 * S) * (S - S0) + S * (1 - S))
closed = np.minimum(1 - S0[:, 0] / 2, (1 + S0[:, 0]) / 2)
report("R4 min_s alpha' = min(1 - s0/2, (1+s0)/2)", np.max(np.abs(ap.min(axis=1) - closed)) < 1e-12,
       f"err {np.max(np.abs(ap.min(axis=1) - closed)):.1e}")
report("R4 global min = 1/2", abs(ap.min() - 0.5) < 1e-12, f"min {ap.min():.12f}")
report("R4 control: bound 0.6 is violated", ap.min() < 0.6, f"min {ap.min():.3f}")
mid2 = 1 + 0.5 * ((1 - 2 * S[0]) * (S[0] - 0.5) + S[0] * (1 - S[0]))
report("R4 s0=1/2: alpha' in [3/4, 9/8]", abs(mid2.min() - 0.75) < 1e-12 and abs(mid2.max() - 1.125) < 1e-6,
       f"[{mid2.min():.6f}, {mid2.max():.6f}]")

txt = "\n".join(out) + f"\nfailures: {fails}\n"
print(txt)
with open(__file__.replace(".py", ".out.txt"), "w", encoding="utf-8") as fh:
    fh.write(txt)
sys.exit(fails)
