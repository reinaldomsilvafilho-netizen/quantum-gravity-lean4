"""Camada 1 (cega) -- verificacoes numericas do cap. 1.
Cada teste usa oraculo independente e, quando cabe, controle negativo.
Rodar: python ch01_blind_checks.py
"""
import itertools
import numpy as np

rng = np.random.default_rng(12345)
OK = []


def report(name, cond, info=""):
    OK.append(cond)
    print(("PASS " if cond else "FAIL ") + name + ("  | " + info if info else ""))


# ---------------------------------------------------------------- T1 Dirichlet energy (Thm dirichlet_blindness)
def dirichlet_quadrature(A, G=64):
    """Oraculo: derivadas por FFT numerica em grade G x G e media sobre o toro."""
    n = A.shape[0]
    x = 2 * np.pi * np.arange(G) / G
    X1, X2 = np.meshgrid(x, x, indexing="ij")
    d1 = np.zeros_like(X1, dtype=complex)
    d2 = np.zeros_like(X1, dtype=complex)
    for k1 in range(1, n + 1):
        for k2 in range(1, n + 1):
            e = np.exp(1j * (k1 * X1 + k2 * X2))
            d1 += 1j * k1 * A[k1 - 1, k2 - 1] * e
            d2 += 1j * k2 * A[k1 - 1, k2 - 1] * e
    return np.mean(np.abs(d1) ** 2 + np.abs(d2) ** 2)


def dirichlet_formula(A):
    n = A.shape[0]
    k = np.arange(1, n + 1)
    return np.sum((k[:, None] ** 2 + k[None, :] ** 2) * np.abs(A) ** 2)


def dirichlet_mutant(A):  # controle negativo: peso (k1+k2)^2
    n = A.shape[0]
    k = np.arange(1, n + 1)
    return np.sum((k[:, None] + k[None, :]) ** 2 * np.abs(A) ** 2)


A = rng.standard_normal((5, 5))
q = dirichlet_quadrature(A)
report("T1 energia de Dirichlet = formula (eq. dirichlet_energy_formula)", abs(q - dirichlet_formula(A)) < 1e-8 * q,
       f"quad={q:.6f} formula={dirichlet_formula(A):.6f}")
report("T1-neg formula mutada (k1+k2)^2 falha", abs(q - dirichlet_mutant(A)) > 1e-3 * q)
for n in (3, 7, 12):
    E11 = np.zeros((n, n)); E11[0, 0] = 1
    Enn = np.zeros((n, n)); Enn[-1, -1] = 1
    r = dirichlet_formula(Enn) / dirichlet_formula(E11)
    report(f"T1 razao E(A2)/E(A1) = n^2 (n={n})", abs(r - n * n) < 1e-12, f"{r}")
# checkerboard
for n in (4, 9):
    C = np.array([[(-1) ** (i + j) for j in range(n)] for i in range(n)], float)
    ev = np.sort(np.linalg.eigvalsh(C))
    closed = 2 * n * n * (n + 1) * (2 * n + 1) / 6
    report(f"T1 tabuleiro: espectro {{n,0..}} e energia 2n*sum k^2 (n={n})",
           abs(ev[-1] - n) < 1e-9 and np.allclose(ev[:-1], 0, atol=1e-9) and abs(dirichlet_formula(C) - closed) < 1e-9)


# ---------------------------------------------------------------- T2 TV formula (Thm tv_matrix) vs coarea oracle
def tv_formula(A):
    n = A.shape[0]
    return (np.abs(np.diff(A, axis=0)).sum() + np.abs(np.diff(A, axis=1)).sum()) / n


def tv_coarea_oracle(A, nt=20001):
    """Oraculo independente: integra em t o perimetro relativo (dentro de (0,1)^2)
    do conjunto {W_A > t}, contado como comprimento de arestas internas entre celulas
    dentro/fora do conjunto (cada aresta tem comprimento 1/n)."""
    n = A.shape[0]
    lo, hi = A.min() - 1, A.max() + 1
    ts = np.linspace(lo, hi, nt)
    per = []
    for t in ts:
        S = A > t
        per.append((np.sum(S[1:, :] != S[:-1, :]) + np.sum(S[:, 1:] != S[:, :-1])) / n)
    return np.trapezoid(per, ts)


A = rng.integers(-3, 4, size=(6, 6)).astype(float)
f, o = tv_formula(A), tv_coarea_oracle(A)
report("T2 TV(W_A) formula = integral de perimetros (coarea)", abs(f - o) < 2e-3 * max(1, f), f"formula={f:.4f} oracle={o:.4f}")
report("T2-neg formula sem fator 1/n falha", abs(f * A.shape[0] - o) > 0.1)
n = 8
C = np.array([[(-1) ** (i + j) for j in range(n)] for i in range(n)], float)
report("T2 TV do tabuleiro = 4(n-1)", abs(tv_formula(C) - 4 * (n - 1)) < 1e-12)


# ---------------------------------------------------------------- T3 cut norm vs L_inf->L1 (Thm grothendieck_cutnorm)
def cut_norm_step(A):
    # para W_A em degraus o sup e atingido em unioes de celulas (bilinear nas fracoes)
    n = A.shape[0]
    best = 0
    for s in itertools.product([0, 1], repeat=n):
        r = np.array(s) @ A  # soma sobre S das linhas
        best = max(best, r[r > 0].sum(), -r[r < 0].sum())
    return best / n ** 2


def inf_to_one_step(A):
    n = A.shape[0]
    best = 0
    for s in itertools.product([-1, 1], repeat=n):
        best = max(best, np.abs(np.array(s) @ A).sum())
    return best / n ** 2


ratios = []
for _ in range(200):
    A = rng.standard_normal((6, 6))
    c, g = cut_norm_step(A), inf_to_one_step(A)
    ratios.append(g / c)
report("T3 cut <= ||T||_{inf->1} <= 4 cut (200 amostras)", min(ratios) >= 1 - 1e-12 and max(ratios) <= 4 + 1e-12,
       f"razao min={min(ratios):.3f} max={max(ratios):.3f}")

# ---------------------------------------------------------------- T4 Fredholm HS norm
n = 5
A = rng.standard_normal((n, n))
G = 400
xs = (np.arange(G) + 0.5) / G
idx = np.minimum((xs * n).astype(int), n - 1)
W = A[np.ix_(idx, idx)]
hs = np.sqrt(np.mean(W ** 2))
report("T4 ||T_A||_HS = ||A||_F / n", abs(hs - np.linalg.norm(A) / n) < 1e-10)


# ---------------------------------------------------------------- T5 Morse indices (Thm morse_matrix)
def riem_hess_fd(A, x, h=1e-4):
    n = len(x)
    Q, _ = np.linalg.qr(np.column_stack([x, rng.standard_normal((n, n - 1))]))
    B = Q[:, 1:]
    f = lambda y: y @ A @ y
    H = np.zeros((n - 1, n - 1))
    for a in range(n - 1):
        for b in range(n - 1):
            def g(s, t):
                v = s * B[:, a] + t * B[:, b]
                nv = np.linalg.norm(v)
                y = x if nv == 0 else np.cos(nv) * x + np.sin(nv) * v / nv  # exp map
                return f(y)
            H[a, b] = (g(h, h) - g(h, -h) - g(-h, h) + g(-h, -h)) / (4 * h * h)
    return H


n = 6
M = rng.standard_normal((n, n)); A = (M + M.T) / 2
lam, V = np.linalg.eigh(A)
idxs = []
for i in range(n):
    Hi = riem_hess_fd(A, V[:, i])  # uma unica base por ponto
    idxs.append(int(np.sum(np.linalg.eigvalsh((Hi + Hi.T) / 2) < 0)))
report("T5 indice de Morse de v_i = i-1", idxs == list(range(n)), str(idxs))
chi = sum(2 * (-1) ** k for k in idxs)
report("T5 P_{-1} = 1-(-1)^n", chi == 1 - (-1) ** n)

# ---------------------------------------------------------------- T6 Kac-Rice theorem: d=2 contraexemplo
# Para d=2 e A simetrica gaussiana, autovalores distintos q.c. => exatamente 2n pontos criticos (Thm morse_matrix),
# crescimento linear, nao exp(n*c).
counts = []
for n in (5, 10, 20, 40):
    M = rng.standard_normal((n, n)); A = (M + M.T) / 2
    ev = np.linalg.eigvalsh(A)
    counts.append((n, 2 * len(np.unique(np.round(ev, 12)))))
report("T6 d=2: #Crit = 2n (nao exponencial) -- contradiz Thm kac_rice_tensors p/ d=2", all(c == 2 * n for n, c in counts), str(counts))


# T6b nao-isotropia: tensor simetrico com entradas independentes de MESMA variancia
def var_f_symmetric_equal_var(x, d):
    """Var f(x) exata quando cada multi-indice ordenado m tem T_m ~ N(0,1) e T e simetrizado
    (todas as permutacoes iguais). f(x) = sum_m mult(m) T_m x^m."""
    n = len(x)
    from math import factorial
    tot = 0.0
    for m in itertools.combinations_with_replacement(range(n), d):
        cnt = np.bincount(m, minlength=n)
        mult = factorial(d) / np.prod([factorial(c) for c in cnt])
        tot += (mult * np.prod(x ** cnt)) ** 2
    return tot


for d in (2, 3):
    n = 3
    e1 = np.array([1.0, 0, 0]); u = np.array([1.0, 1, 0]) / np.sqrt(2)
    v1, v2 = var_f_symmetric_equal_var(e1, d), var_f_symmetric_equal_var(u, d)
    report(f"T6b d={d}: Var f(e1) != Var f((e1+e2)/sqrt2) => campo NAO isotropico sob a hipotese do texto",
           abs(v1 - v2) > 1e-6, f"{v1:.4f} vs {v2:.4f}")
    # controle: variancia 1/mult(m) (modelo ABC simetrizado) => isotropico
    def var_iso(x):
        from math import factorial
        tot = 0.0
        for m in itertools.combinations_with_replacement(range(len(x)), d):
            cnt = np.bincount(m, minlength=len(x))
            mult = factorial(d) / np.prod([factorial(c) for c in cnt])
            tot += mult * np.prod(x ** cnt) ** 2
        return tot
    report(f"T6b-ctrl d={d}: com Var T_m = 1/mult(m) o campo e isotropico", abs(var_iso(e1) - var_iso(u)) < 1e-12)


# T6c coeficiente do termo -c f I na Hessiana riemanniana: deve ser d (Euler), nao d-1
def sym_tensor(n, d):
    T = rng.standard_normal((n,) * d)
    S = np.zeros_like(T)
    perms = list(itertools.permutations(range(d)))
    for p in perms:
        S += np.transpose(T, p)
    return S / len(perms)


n, d = 5, 3
T = sym_tensor(n, d)
fT = lambda y: np.einsum("ijk,i,j,k->", T, y, y, y)
# ponto critico por iteracao de potencia (SS-HOPM) com shift
x = rng.standard_normal(n); x /= np.linalg.norm(x)
for _ in range(5000):
    g = np.einsum("ijk,j,k->i", T, x, x) + 3.0 * x
    x = g / np.linalg.norm(g)
grad = 3 * np.einsum("ijk,j,k->i", T, x, x)
tang = grad - (grad @ x) * x
Q, _ = np.linalg.qr(np.column_stack([x, rng.standard_normal((n, n - 1))]))
B = Q[:, 1:]
Heuc = 6 * np.einsum("ijk,k->ij", T, x)
Ht = B.T @ Heuc @ B
Hfd = np.zeros((n - 1, n - 1)); h = 1e-4
for a in range(n - 1):
    for b in range(n - 1):
        def g2(s, t):
            v = s * B[:, a] + t * B[:, b]; nv = np.linalg.norm(v)
            y = x if nv == 0 else np.cos(nv) * x + np.sin(nv) * v / nv
            return fT(y)
        Hfd[a, b] = (g2(h, h) - g2(h, -h) - g2(-h, h) + g2(-h, -h)) / (4 * h * h)
fx = fT(x)
err_d = np.abs(Hfd - (Ht - d * fx * np.eye(n - 1))).max()
err_dm1 = np.abs(Hfd - (Ht - (d - 1) * fx * np.eye(n - 1))).max()
report("T6c Hess_S = Hess_eucl|_T - d f I (coef. d)", np.linalg.norm(tang) < 1e-8 and err_d < 1e-5, f"err={err_d:.2e}, |grad_T|={np.linalg.norm(tang):.1e}")
report("T6c-neg coef. (d-1) do texto falha", err_dm1 > 1e-2, f"err={err_dm1:.3f}, f(x)={fx:.3f}")


# ---------------------------------------------------------------- T7 critical scaling (Thm critical_scaling)
def sup_multilinear(T, iters=200, restarts=5):
    d = T.shape[0]
    best = 0
    for _ in range(restarts):
        u = [rng.standard_normal(d) for _ in range(3)]
        u = [w / np.linalg.norm(w) for w in u]
        for _ in range(iters):
            u[0] = np.einsum("ijk,j,k->i", T, u[1], u[2]); u[0] /= np.linalg.norm(u[0])
            u[1] = np.einsum("ijk,i,k->j", T, u[0], u[2]); u[1] /= np.linalg.norm(u[1])
            u[2] = np.einsum("ijk,i,j->k", T, u[0], u[1]); u[2] /= np.linalg.norm(u[2])
        best = max(best, abs(np.einsum("ijk,i,j,k->", T, *u)))
    return best


vals = []
for d in (8, 16, 32, 48):
    s = np.mean([sup_multilinear(rng.standard_normal((d, d, d))) for _ in range(4)]) / np.sqrt(d)
    vals.append((d, round(s, 3)))
report("T7(i) E sup |f_hat| ~ constante em d (k=3)", max(v for _, v in vals) / min(v for _, v in vals) < 1.3, str(vals))
# (ii) probabilidade conjunta (T e u aleatorios): f_hat*sqrt(d) ~ N(0,1) exatamente
d, k, N = 20, 3, 200000
Xs = rng.standard_normal(N)  # por rotacao-invariancia, X(u) ~ N(0,1) para u fixo e T gaussiano
# verificacao direta com T e u independentes:
Xd = []
for _ in range(4000):
    T = rng.standard_normal((d, d, d)); us = [rng.standard_normal(d) for _ in range(3)]; us = [w / np.linalg.norm(w) for w in us]
    Xd.append(np.einsum("ijk,i,j,k->", T, *us))
Xd = np.array(Xd)
report("T7(ii) X(u) com T,u aleatorios tem variancia 1 (logo P(|f_hat|>e) = P(|Z|>e sqrt d) <= 2exp(-d e^2/2))",
       abs(Xd.var() - 1) < 0.08, f"var={Xd.var():.3f}")
# controle da escala: com normalizacao 1/d em vez de 1/sqrt d o sup vai a 0
report("T7-neg escala alpha=1 da sup -> 0", vals[-1][1] / np.sqrt(vals[-1][0]) < 0.5 * vals[0][1] / np.sqrt(vals[0][0]))


# ---------------------------------------------------------------- T8 attention theorem
def softmax_rows(Z):
    Z = Z - Z.max(axis=1, keepdims=True)
    E = np.exp(Z)
    return E / E.sum(axis=1, keepdims=True)


rows = []
for N in (8, 16, 32, 64):
    Aatt = softmax_rows(rng.standard_normal((N, N)) * 2)
    f00 = Aatt.sum()  # f_A(0,0) = sum de todas as entradas
    k = np.arange(1, N + 1)
    K1, K2 = np.meshgrid(k, k, indexing="ij")
    lam = 1.0
    R = (2 * np.pi) ** 2 * np.sum((1 + K1 ** 2 + K2 ** 2 + lam * (K1 ** 2 + K2 ** 2) ** 2) * Aatt ** 2)
    rows.append((N, f00, R))
report("T8 sup|f_A| >= f_A(0,0) = N para toda atencao softmax (cresce com N)", all(abs(f - N) < 1e-9 for N, f, _ in rows),
       str([(N, round(f, 6)) for N, f, _ in rows]))
Rs = np.array([r for _, _, r in rows]); Ns = np.array([N for N, _, _ in rows])
slope = np.polyfit(np.log(Ns), np.log(Rs), 1)[0]
report("T8 R_Attn cresce polinomialmente em N (nao ha limite uniforme em N)", slope > 3, f"expoente ~ {slope:.2f}")

print("\nTOTAL:", sum(OK), "/", len(OK))
