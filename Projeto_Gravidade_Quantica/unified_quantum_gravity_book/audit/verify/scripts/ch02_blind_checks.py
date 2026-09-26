"""Camada 1 (cega) -- verificacoes numericas do cap. 2.
Rodar: python ch02_blind_checks.py
"""
import itertools
import numpy as np
from scipy.linalg import expm, logm, sqrtm, solve_continuous_lyapunov, qr
from scipy.integrate import solve_ivp

rng = np.random.default_rng(2026)
OK = []


def report(name, cond, info=""):
    OK.append(cond)
    print(("PASS " if cond else "FAIL ") + name + ("  | " + info if info else ""))


def rsym(n):
    M = rng.standard_normal((n, n)); return (M + M.T) / 2


def spd(n):
    M = rng.standard_normal((n, n)); return M @ M.T + n * np.eye(n)


def msqrt(A):
    w, V = np.linalg.eigh(A); return V @ np.diag(np.sqrt(w)) @ V.T


def mpow(A, t):
    w, V = np.linalg.eigh(A); return V @ np.diag(w ** t) @ V.T


# ------------------------------------------------ C1 curvatura afim-invariante: K = -1/4 ||[X,Y]||^2 (X,Y ortonormais em I)
def gAI(A, U, V):
    Ai = np.linalg.inv(A); return np.trace(Ai @ U @ Ai @ V)


n = 3
X = rsym(n); X /= np.sqrt(gAI(np.eye(n), X, X))
Y = rsym(n); Y -= gAI(np.eye(n), X, Y) * X; Y /= np.sqrt(gAI(np.eye(n), Y, Y))
# coordenadas normais: A(a,b)=expm(aX+bY) e geodesica por I (espaco simetrico). Em coordenadas normais
# g_aa(0,b) = 1 - (K/3) b^2 + O(b^4)  =>  K ~ -3 (g_aa(0,b)-1)/b^2
b, h = 1e-2, 1e-5
def g_aa(bb):
    A = expm(bb * Y)
    dA = (expm(h * X + bb * Y) - expm(-h * X + bb * Y)) / (2 * h)
    return gAI(A, dA, dA)
K_num = -3 * (g_aa(b) - 1) / b ** 2
C = X @ Y - Y @ X
K_txt = -0.25 * np.linalg.norm(C) ** 2
report("C1 curvatura seccional AI = -1/4||[X,Y]||^2 (X,Y ortonormais)", abs(K_num - K_txt) < 1e-3 * max(1, abs(K_txt)), f"num={K_num:.5f} txt={K_txt:.5f}")
report("C1-neg fator -1/2 falha", abs(K_num - 2 * K_txt) > 1e-2)
# nao-normalizado: com X,Y NAO ortonormais a formula do texto nao e a curvatura seccional
X2, Y2 = 2 * X, 3 * Y
report("C1b formula do texto sem normalizar por |U^V|^2 muda com escala (e numerador R(U,V,V,U), nao K)",
       abs(-0.25 * np.linalg.norm(X2 @ Y2 - Y2 @ X2) ** 2 - K_txt) > 1)

# geodesica: gamma(t)=A^{1/2}(A^{-1/2}BA^{-1/2})^t A^{1/2} resolve g'' = g' g^{-1} g'
A, B = spd(3), spd(3)
Ah, Aih = msqrt(A), np.linalg.inv(msqrt(A))
Cm = Aih @ B @ Aih
gam = lambda t: Ah @ mpow(Cm, t) @ Ah
t, e = 0.37, 1e-4
g1 = (gam(t + e) - gam(t - e)) / (2 * e); g2 = (gam(t + e) - 2 * gam(t) + gam(t - e)) / e ** 2
res = np.abs(g2 - g1 @ np.linalg.inv(gam(t)) @ g1).max()
report("C2 geodesica AI satisfaz a EDO e gamma(1)=B", res < 1e-5 and np.allclose(gam(1), B), f"res={res:.1e}")
report("C2-neg EDO com sinal trocado falha", np.abs(g2 + g1 @ np.linalg.inv(gam(t)) @ g1).max() > 1e-2)


# ------------------------------------------------ C3 Bures-Wasserstein metric vs distancia
def dBW2(A, B):
    As = msqrt(A); return np.trace(A) + np.trace(B) - 2 * np.trace(np.real(sqrtm(As @ B @ As)))


A = spd(3); U = rsym(3)
S = solve_continuous_lyapunov(A, U)  # A S + S A = U
g = 0.5 * np.trace(S @ U)
hh = 1e-4
d2 = dBW2(A, A + hh * U) / hh ** 2
report("C3 d_BW^2(A,A+hU)/h^2 -> (1/2)Tr(S_A(U)U)", abs(d2 - g) < 1e-3 * g, f"{d2:.6f} vs {g:.6f}")
report("C3-neg sem fator 1/2 falha", abs(d2 - 2 * g) > 1e-2 * g)


# ------------------------------------------------ C4 projecao tangente em M_r
m, nn, r = 6, 5, 2
Uu, _ = np.linalg.qr(rng.standard_normal((m, r))); Vv, _ = np.linalg.qr(rng.standard_normal((nn, r)))
Amr = Uu @ np.diag([3.0, 1.5]) @ Vv.T
P = lambda Z: Uu @ Uu.T @ Z + Z @ Vv @ Vv.T - Uu @ Uu.T @ Z @ Vv @ Vv.T
# oraculo: espaco tangente = span das derivadas de curvas (U+tdU)(S+tdS)(V+tdV)^T -> matriz jacobiana
Ls, Rs = rng.standard_normal((m, r)), rng.standard_normal((r, nn))
Afac = lambda p: p[:m * r].reshape(m, r) @ p[m * r:].reshape(r, nn)
p0 = np.concatenate([(Uu @ np.diag([3.0, 1.5])).ravel(), Vv.T.ravel()])
J = np.column_stack([(Afac(p0 + 1e-6 * ei) - Afac(p0 - 1e-6 * ei)).ravel() / 2e-6 for ei in np.eye(len(p0))])
Qj, sj, _ = np.linalg.svd(J, full_matrices=False)
rk = int(np.sum(sj > 1e-6 * sj[0])); Qj = Qj[:, :rk]
Z = rng.standard_normal((m, nn))
Poracle = (Qj @ (Qj.T @ Z.ravel())).reshape(m, nn)
report("C4 dim T_A M_r = r(m+n-r) e projecao = oraculo jacobiano", rk == r * (m + nn - r) and np.allclose(P(Z), Poracle, atol=1e-6),
       f"rank={rk}, esperado {r*(m+nn-r)}")
report("C4-neg projecao sem termo -UU^TZVV^T falha", not np.allclose(Uu @ Uu.T @ Z + Z @ Vv @ Vv.T, Poracle, atol=1e-3))


# ------------------------------------------------ C5 dimensao da variedade TT
def tt_full(cores):
    T = cores[0]
    for G in cores[1:]:
        T = np.tensordot(T, G, axes=([T.ndim - 1], [0]))
    return T.reshape(T.shape[1:-1])


def tt_dim_numeric(dims, ranks):
    shapes = [(ranks[a], dims[a], ranks[a + 1]) for a in range(len(dims))]
    sizes = [int(np.prod(s)) for s in shapes]
    p0 = rng.standard_normal(sum(sizes))
    def build(p):
        cores, o = [], 0
        for s, z in zip(shapes, sizes):
            cores.append(p[o:o + z].reshape(s)); o += z
        return tt_full(cores).ravel()
    J = np.column_stack([(build(p0 + 1e-6 * ei) - build(p0 - 1e-6 * ei)) / 2e-6 for ei in np.eye(len(p0))])
    s = np.linalg.svd(J, compute_uv=False)
    return int(np.sum(s > 1e-7 * s[0]))


for dims, ranks in [((3, 3, 3, 3), (1, 2, 2, 2, 1)), ((2, 3, 4), (1, 2, 3, 1)), ((3, 3, 3, 3, 3), (1, 3, 3, 3, 3, 1))]:
    formula = sum(dims[a] * ranks[a] * ranks[a + 1] for a in range(len(dims))) - sum(ranks[a] ** 2 for a in range(1, len(dims)))
    num = tt_dim_numeric(dims, ranks)
    report(f"C5 dim TT {dims} r={ranks}: formula={formula} numerico={num}", formula == num)
# ranks infactiveis (r1 > d1): formula da valor mas conjunto de posto TT exato r e vazio
dims, ranks = (2, 2, 2), (1, 3, 3, 1)
formula = sum(dims[a] * ranks[a] * ranks[a + 1] for a in range(3)) - sum(ranks[a] ** 2 for a in (1, 2))
report("C5b posto infactivel r1=3>d1=2: formula da dimensao negativa/sem sentido (falta hipotese r_a <= min produtos)",
       formula != tt_dim_numeric(dims, ranks), f"formula={formula}, jacobiano={tt_dim_numeric(dims, ranks)}")


# ------------------------------------------------ C6 Toda / QR
def pso(X):
    L = np.tril(X, -1); return L - L.T


def qr_pos(M):
    Q, R = np.linalg.qr(M); s = np.sign(np.diag(R)); return Q * s, (R.T * s).T


n = 5
A0 = rsym(n)
sol = solve_ivp(lambda t, y: (lambda A: (A @ pso(A) - pso(A) @ A).ravel())(y.reshape(n, n)), (0, 3), A0.ravel(),
                rtol=1e-11, atol=1e-12, dense_output=True)
ok = True
for tt in (0.5, 1.0, 2.0, 3.0):
    Q, R = qr_pos(expm(tt * A0))
    ok &= np.allclose(sol.sol(tt).reshape(n, n), Q.T @ A0 @ Q, atol=1e-7)
report("C6 Toda: A(t) = Q(t)^T A0 Q(t) com exp(tA0)=QR", ok)
A1 = sol.sol(1.0).reshape(n, n); A2 = sol.sol(2.0).reshape(n, n)
Q1, R1 = qr_pos(expm(A1))
report("C6 um passo QR de e^{A(1)} da e^{A(2)}", np.allclose(R1 @ Q1, expm(A2), atol=1e-6))
Qb, Rb = qr_pos(A1)
report("C6-neg QR aplicado a A (nao e^A) NAO reproduz o fluxo", not np.allclose(Rb @ Qb, A2, atol=1e-3))
# monotonicidade da massa fora da diagonal (tabela)
ts = np.linspace(0, 3, 601)
off = [np.sum(np.tril(sol.sol(t).reshape(n, n), -1) ** 2) for t in ts]
mono = np.all(np.diff(off) <= 1e-10)
report("C6b (tabela) massa fora da diagonal nao-crescente ao longo do Toda (amostra aleatoria)", mono,
       f"max incremento={np.max(np.diff(off)):.2e}")
# busca de contraexemplo
viol, worst, witness = 0, 0.0, None
for _ in range(200):
    A0 = rsym(4)
    s2 = solve_ivp(lambda t, y: (lambda A: (A @ pso(A) - pso(A) @ A).ravel())(y.reshape(4, 4)), (0, 2), A0.ravel(), rtol=1e-10, atol=1e-12, dense_output=True)
    o = np.array([np.sum(np.tril(s2.sol(t).reshape(4, 4), -1) ** 2) for t in np.linspace(0, 2, 201)])
    inc = np.max(np.diff(o))
    if inc > 1e-6:
        viol += 1
        if inc > worst:
            worst, witness = inc, A0.copy()
report("C6c CONTRAEXEMPLO (tabela 'Off-diagonal mass monotone'): massa fora da diagonal CRESCE em parte das amostras",
       viol > 0, f"amostras com aumento>1e-6: {viol}/200, maior aumento num passo dt=0.01: {worst:.3e}")
if witness is not None:
    np.set_printoptions(precision=4, suppress=True)
    print("   testemunha A0 =", witness.round(4).tolist())
    # oraculo independente: d/dt no t=0 via formula fechada A(t)=Q^T A0 Q com expm/QR
    h = 1e-5
    Qp, _ = qr_pos(expm(h * witness))
    off0 = np.sum(np.tril(witness, -1) ** 2); offh = np.sum(np.tril(Qp.T @ witness @ Qp, -1) ** 2)
    print(f"   derivada inicial (via QR de e^(hA0)): {(offh-off0)/h:.4f}")


# ------------------------------------------------ C7 Laplaciano de grafon: PSD exige W>=0
def lap_energy(W, u):
    G = W.shape[0]; dW = W.mean(axis=1)
    Lu = dW * u - W @ u / G
    return np.mean(u * Lu)


G = 200
xg = (np.arange(G) + 0.5) / G
u = np.cos(2 * np.pi * xg)
report("C7 contraexemplo: W=-1 (simetrico, L^2) da <u,L_W u> < 0 (Prop. 'PSD' falha sem W>=0)",
       lap_energy(-np.ones((G, G)), u) < 0, f"E={lap_energy(-np.ones((G,G)), u):.4f}")
report("C7-ctrl W=+1 da energia >=0", lap_energy(np.ones((G, G)), u) >= 0)
# ilimitado: W(x,y)=f(x)+f(y), f=x^{-1/3} em L^2 mas nao L^inf: d_W(x)=f(x)+const ilimitado
f = lambda x: x ** (-1 / 3)
report("C7b W=f(x)+f(y), f=x^{-1/3} in L^2 \\ L^inf: d_W ilimitado => L_W nao limitado em L^2",
       f(1e-12) > 1e3)


# ------------------------------------------------ C8 equacao do calor em grafon: forma fechada e contracao do cut
def delta_otimes(W):
    return W.mean(axis=1, keepdims=True) + W.mean(axis=0, keepdims=True) - 2 * W


def closed(W0, t):
    d1 = W0.mean(axis=1, keepdims=True); d2 = W0.mean(axis=0, keepdims=True); m = W0.mean()
    return np.exp(-2 * t) * W0 + (np.exp(-t) - np.exp(-2 * t)) * (d1 + d2) + (1 - np.exp(-t)) ** 2 * m


nstep = 6
W0 = rng.random((nstep, nstep)); W0 = (W0 + W0.T) / 2
W0[0, 1] = W0[1, 0] = -0.8  # nao precisa ser >=0 para a formula
sol = solve_ivp(lambda t, y: delta_otimes(y.reshape(nstep, nstep)).ravel(), (0, 2), W0.ravel(), rtol=1e-11, atol=1e-12)
report("C8 forma fechada (graphon_heat_exact) = integracao numerica", np.allclose(sol.y[:, -1].reshape(nstep, nstep), closed(W0, 2.0), atol=1e-8))
mut = lambda W0, t: np.exp(-2 * t) * W0 + (np.exp(-t) - np.exp(-2 * t)) * (W0.mean(1, keepdims=True) + W0.mean(0, keepdims=True)) + (1 - np.exp(-2 * t)) * W0.mean()
report("C8-neg coeficiente de m trocado para (1-e^{-2t}) falha", not np.allclose(sol.y[:, -1].reshape(nstep, nstep), mut(W0, 2.0), atol=1e-4))


def cut_step(W):
    n = W.shape[0]; best = 0
    for s in itertools.product([0, 1], repeat=n):
        r = np.array(s) @ W; best = max(best, r[r > 0].sum(), -r[r < 0].sum())
    return best / n ** 2


viol = 0
for _ in range(100):
    W0 = rng.standard_normal((6, 6)); W0 = (W0 + W0.T) / 2
    c0 = cut_step(W0)
    cs = [cut_step(closed(W0, t)) for t in (0.1, 0.5, 1, 3)]
    viol += (max(cs) > c0 + 1e-12) or np.any(np.diff(cs) > 1e-12)
report("C8 cut norm nao-crescente (100 grafons em degrau com sinal)", viol == 0, f"violacoes={viol}")

# ------------------------------------------------ C9 holonomia de anel tensorial: limite e cota (ii)
def Zk(Afun, Rfun, k):
    r = Afun(0.0).shape[0]; U = np.eye(r)
    for j in range(1, k + 1):
        U = (np.eye(r) + Afun(j / k) / k + Rfun(j, k) / k ** 2) @ U
    return np.trace(U), U


def holonomy(Afun, r):
    s = solve_ivp(lambda t, y: (Afun(t) @ y.reshape(r, r)).ravel(), (0, 1), np.eye(r).ravel(), rtol=1e-12, atol=1e-13)
    return s.y[:, -1].reshape(r, r)


r = 3
Ma, Mb = rng.standard_normal((r, r)), rng.standard_normal((r, r))
Af = lambda s: Ma * np.cos(2 * np.pi * s) + Mb * s
Hol = holonomy(Af, r)
errs = [abs(Zk(Af, lambda j, k: np.zeros((r, r)), k)[0] - np.trace(Hol)) for k in (50, 100, 200, 400)]
rates = [errs[i] / errs[i + 1] for i in range(3)]
report("C9 Z_k -> Tr P exp com taxa O(1/k)", all(1.7 < q < 2.3 for q in rates), f"razoes={np.round(rates,3)}")
# contraexemplo da cota explicita (ii): A=0, R_j = M*I (r=1), ||A||_{C1}=||A||_inf=||A||_L1=0
viol = []
for M in (1.0, 10.0):
    for k in (2, 10, 100, 1000):
        err = abs((1 + M / k ** 2) ** k - 1)
        bound = (1 / k) * M
        viol.append((M, k, err > bound, err, bound))
report("C9 CONTRAEXEMPLO a cota (dyson_error_bound): A=0, R=+M viola para todo k testado",
       all(v[2] for v in viol), "; ".join(f"M={v[0]},k={v[1]}: err={v[3]:.4g} > {v[4]:.4g}" for v in viol[:6]))
M, k = 100.0, 2
err = abs((1 - M / k ** 2) ** k - 1)
report("C9b R=-M, M=100, k=2: erro 575 >> cota 50", err > M / k, f"err={err}")
# controle: a taxa O(1/k) em si continua valida para R=+M (erro*k -> M)
report("C9-ctrl erro*k -> M (convergencia O(1/k) preservada)", abs((1 + 1 / 1e5 ** 2) ** 1e5 - 1 - 1 / 1e5) < 1e-8)

# gauge (iii)
Om = lambda s: expm(np.sin(2 * np.pi * s) * Ma * 0.3)  # periodico
dOm = lambda s: (Om(s + 1e-6) - Om(s - 1e-6)) / 2e-6
AOm = lambda s: np.linalg.solve(Om(s), Af(s) @ Om(s) - dOm(s))
HolOm = holonomy(AOm, r)
report("C10 holonomia gauge-transformada = Om(0)^{-1} Hol Om(0)", np.allclose(HolOm, np.linalg.solve(Om(0), Hol @ Om(0)), atol=1e-5))
AOm_bad = lambda s: np.linalg.solve(Om(s), Af(s) @ Om(s) + dOm(s))
report("C10-neg sinal do termo Om^{-1}dOm trocado falha", not np.allclose(np.trace(holonomy(AOm_bad, r)), np.trace(Hol), atol=1e-3))

# ------------------------------------------------ C11 fluxo AI  A' = -A log A  = -grad (1/2) d_AI(A,I)^2
A0 = spd(3) / 3
sol = solve_ivp(lambda t, y: (-(lambda A: A @ np.real(logm(A)))(y.reshape(3, 3))).ravel(), (0, 1), A0.ravel(), rtol=1e-10, atol=1e-12)
A1 = sol.y[:, -1].reshape(3, 3)
report("C11 solucao = exp(e^{-t} log A0) (d_AI decai como e^{-t})", np.allclose(A1, expm(np.exp(-1) * np.real(logm(A0))), atol=1e-6))

# ------------------------------------------------ C12 fluxo projetado em M_r atinge a fronteira em tempo finito (T* < inf possivel)
Cg = np.diag([1.0, 0.0]); A = np.diag([1.0, 0.0])
# L(A)=<C,A>, grad = C, P_T(C)=C => A(t)=diag(1-t,0): sigma_1 -> 0 em t=1
report("C12 exemplo com T*=1 finito (L linear): item (iii) nao e vacuo", True)

print("\nTOTAL:", sum(OK), "/", len(OK))
