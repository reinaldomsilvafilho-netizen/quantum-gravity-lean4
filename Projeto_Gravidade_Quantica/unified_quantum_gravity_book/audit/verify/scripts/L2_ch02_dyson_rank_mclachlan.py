"""Camada 2, F-48 (cap. 2). Independent attempts to break the NEW statements.

D1  Dyson bound (Thm 6.2(ii)):
      |Z_k - Tr Pexp| <= (r/k)(M + (a1+a0^2)/2) exp(||A||_L1 + (M + a1/2)/k)
    adversarial search: scalar (r=1, commuting) cases with R_j = +-M, steep ramps, small k,
    and matrix cases; oracle = exact exp(int a) (scalar) or high-accuracy RK (matrix).
    Mutations: drop e^{M/k}; replace ||A||_L1 by 0; divide the constant by 4.
R1  Thm 3.3(iii): projected flow reaches a lower-rank limit in finite time
    (r=2 example: L=<C,A>, C=diag(1,1,0), A0=diag(2,1,0) -> T*=1, A*=diag(1,0,0)).
    Mutation: "limit has rank r" fails.
M1  McLachlan normal equations (Prop 6.1) on a finite-dimensional gauge-redundant family
    (normalized open MPS, 3 qubits, bond 2, complex cores):
    g degenerate; grad<H> vanishes on ker g; pseudo-inverse solution minimizes the McLachlan
    functional; d<H>/dtau = -2 thdot^T g thdot = -2 ||Pi (H-E) Psi||^2.
    Mutation: g thdot = -grad<H> (factor 1 instead of 1/2) breaks the energy identity.
"""
import math
import numpy as np
from scipy import linalg

rng = np.random.default_rng(11)
FAIL = []


def check(name, ok, info=None):
    print(("PASS " if ok else "FAIL ") + name + ("" if info is None else "  | " + str(info)))
    if not ok:
        FAIL.append(name)


def bound(r, M, a0, a1, L1, k, c=1.0, eMk=True, useL1=True):
    return r / k * c * (M + (a1 + a0 ** 2) / 2) * math.exp((L1 if useL1 else 0) + ((M if eMk else 0) + a1 / 2) / k)


# ---------------- D1 scalar adversarial cases
worst = (0, None)
mut = {"noeMk": 0, "noL1": 0, "c/4": 0}
cases = 0
for amp in (0.0, 0.5, 2.0, 5.0):
    for slope in (-6.0, -2.0, 0.0, 2.0, 6.0):
        for M in (0.0, 0.5, 3.0, 20.0):
            for sgn in (+1, -1):
                for k in (1, 2, 3, 5, 10, 40):
                    a = lambda s: amp + slope * s
                    ss = np.linspace(0, 1, 4001)
                    av = np.abs(a(ss))
                    a0 = av.max(); a1 = abs(slope); L1 = np.trapezoid(av, ss)
                    exact = math.exp(amp + slope / 2)
                    prod = 1.0
                    for j in range(1, k + 1):
                        prod *= 1 + a(j / k) / k + sgn * M / k ** 2
                    err = abs(prod - exact)
                    b = bound(1, M, a0, a1, L1, k)
                    cases += 1
                    if err / b > worst[0]:
                        worst = (err / b, (amp, slope, M, sgn, k))
                    mut["noeMk"] += err > bound(1, M, a0, a1, L1, k, eMk=False)
                    mut["noL1"] += err > bound(1, M, a0, a1, L1, k, useL1=False)
                    mut["c/4"] += err > bound(1, M, a0, a1, L1, k, c=0.25)
check("D1 scalar: bound holds in all %d adversarial cases" % cases, worst[0] <= 1.0, "max err/bound=%.3f at %s" % worst)
check("D1-mut drop e^{M/k}: violated somewhere", mut["noeMk"] > 0, mut["noeMk"])
check("D1-mut drop exp(||A||_L1): violated somewhere", mut["noL1"] > 0, mut["noL1"])
check("D1-mut constant/4: violated somewhere", mut["c/4"] > 0, mut["c/4"])


# matrix cases, R_j aligned to maximize growth
def pexp(Af, steps=6000):
    U = np.eye(Af(0).shape[0], dtype=complex); h = 1.0 / steps
    for i in range(steps):
        s = i * h
        k1 = Af(s) @ U; k2 = Af(s + h / 2) @ (U + h / 2 * k1); k3 = Af(s + h / 2) @ (U + h / 2 * k2); k4 = Af(s + h) @ (U + h * k3)
        U = U + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return U


wm = 0
for trial in range(8):
    r = 2 + trial % 3
    B0, B1 = rng.normal(size=(r, r)), rng.normal(size=(r, r)) * (1 + trial)
    Af = lambda s: B0 + B1 * np.cos(3 * s)
    dA = lambda s: -3 * B1 * np.sin(3 * s)
    ss = np.linspace(0, 1, 3001)
    a0 = max(np.linalg.norm(Af(s), 2) for s in ss); a1 = max(np.linalg.norm(dA(s), 2) for s in ss)
    L1 = np.trapezoid([np.linalg.norm(Af(s), 2) for s in ss], ss)
    ex = np.trace(pexp(Af))
    for k in (2, 6, 25):
        M = 4.0
        P = np.eye(r)
        for j in range(1, k + 1):
            P = (np.eye(r) + Af(j / k) / k + M * np.eye(r) / k ** 2) @ P  # R_j = +M I (maximal growth)
        wm = max(wm, abs(np.trace(P) - ex) / bound(r, M, a0, a1, L1, k))
check("D1 matrix cases (R_j = +M I): bound holds", wm <= 1.0, "max err/bound=%.3g" % wm)

# ---------------- R1
def proj(A, Z, r):
    U, s, Vt = np.linalg.svd(A)
    U = U[:, :r]; V = Vt[:r].T
    return U @ U.T @ Z + Z @ V @ V.T - U @ U.T @ Z @ V @ V.T


C = np.diag([1.0, 1.0, 0.0]); A = np.diag([2.0, 1.0, 0.0]); h = 1e-4; t = 0.0
while t < 0.999:
    A = A - h * proj(A, C, 2); t += h
sv = np.linalg.svd(A, compute_uv=False)
check("R1 r=2 flow: sigma_2 -> 0 as t -> T*=1, limit rank 1", abs(sv[1] - (1 - t)) < 1e-6 and abs(sv[0] - (2 - t)) < 1e-6, sv)
check("R1-mut 'limit keeps rank r' fails", sv[1] < 2e-3)
# Gronwall bound ||A(t)|| <= (||A0|| + t ||grad L(0)||) e^{Lt}, here L=0
check("R1 Gronwall bound holds (L=0)", np.linalg.norm(A) <= np.linalg.norm(np.diag([2.0, 1.0, 0])) + t * np.linalg.norm(C) + 1e-12)

# ---------------- M1 McLachlan on normalized MPS
d, D, L = 2, 2, 3
shapes = [(1, d, D), (D, d, D), (D, d, 1)]
sizes = [int(np.prod(s)) for s in shapes]
npar = 2 * sum(sizes)


def psi_raw(th):
    c = th[: npar // 2] + 1j * th[npar // 2:]
    cores = []; o = 0
    for s, z in zip(shapes, sizes):
        cores.append(c[o:o + z].reshape(s)); o += z
    T = cores[0]
    for G in cores[1:]:
        T = np.tensordot(T, G, axes=(-1, 0))
    return T.reshape(-1)


def psi(th):
    v = psi_raw(th)
    return v / np.linalg.norm(v)


Hm = rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8)); Hm = (Hm + Hm.conj().T) / 2
th = rng.normal(size=npar)
P0 = psi(th); E = np.real(P0.conj() @ Hm @ P0)
eps = 1e-6
dPsi = np.array([(psi(th + eps * e) - psi(th - eps * e)) / (2 * eps) for e in np.eye(npar)]).T
Pperp = np.eye(8) - np.outer(P0, P0.conj())
W = Pperp @ dPsi
g = np.real(W.conj().T @ W)
gradE = np.array([2 * np.real(dPsi[:, a].conj() @ (Hm - E * np.eye(8)) @ P0) for a in range(npar)])
ev, evec = np.linalg.eigh(g)
ker = evec[:, ev < 1e-8 * ev.max()]
check("M1 g degenerate (gauge + phase + normalization)", ker.shape[1] >= 2 * 2 * D * D + 2, "dim ker g = %d of %d" % (ker.shape[1], npar))
check("M1 consistency: grad<H> vanishes on ker g", np.abs(ker.T @ gradE).max() < 1e-6 * np.abs(gradE).max(), np.abs(ker.T @ gradE).max())
thdot = -0.5 * np.linalg.pinv(g, rcond=1e-9) @ gradE
# direct least-squares minimization of the McLachlan functional over real thdot
Wr = np.vstack([W.real, W.imag]); rhs = -np.concatenate([((Hm - E * np.eye(8)) @ P0).real, ((Hm - E * np.eye(8)) @ P0).imag])
thls = np.linalg.lstsq(Wr, rhs, rcond=None)[0]
check("M1 pinv solution of g thdot = -grad/2 has the same projected velocity as the LS minimizer",
      np.linalg.norm(W @ thdot - W @ thls) < 1e-6)
# energy identity
def energy(t_):
    p = psi(t_); return np.real(p.conj() @ Hm @ p)
dt = 1e-6
dEdt = (energy(th + dt * thdot) - energy(th - dt * thdot)) / (2 * dt)
PiHPsi = W @ thls  # = -Pi (H-E) Psi
check("M1 dE/dtau = -2 thdot^T g thdot = -2||Pi(H-E)Psi||^2",
      abs(dEdt + 2 * thdot @ g @ thdot) < 1e-5 and abs(dEdt + 2 * np.linalg.norm(PiHPsi) ** 2) < 1e-5,
      (dEdt, -2 * thdot @ g @ thdot, -2 * np.linalg.norm(PiHPsi) ** 2))
thbad = -1.0 * np.linalg.pinv(g, rcond=1e-9) @ gradE
dEbad = (energy(th + dt * thbad) - energy(th - dt * thbad)) / (2 * dt)
check("M1-mut factor 1 instead of 1/2: identity dE = -2||Pi(H-E)Psi||^2 fails", abs(dEbad + 2 * np.linalg.norm(PiHPsi) ** 2) > 1e-3, dEbad)
print("\nFAILURES:", FAIL if FAIL else "none")
