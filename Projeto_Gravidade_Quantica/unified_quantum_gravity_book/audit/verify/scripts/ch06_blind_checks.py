"""Cap. 6 -- verificacoes cegas independentes (camada 1).

 A. Forma fechada de E(x) (via cap. 3) contra quadratura direta (mpmath) e expansao
    assintotica da Prop. 3.1; controles negativos: -ln(x)/12, sem a constante -1/12.
 B. Fator de renormalizacao r_m=m+3 do simplexo de Sierpinski:
    (i) condutancia rho=(m+3)/(m+1) por traco de rede (Schur complement);
    (ii) lambda_1 do laplaciano de grafo nivel k escala por ~ m+3.
    Controle negativo: rho=(m+2)/m nao reproduz a rede.
 C. Formula de reflexao (eq. reflection) em pontos aleatorios; controle: sinal trocado.
    Afirmacao 'linhas nodais inteiras y in Z': binom(0.5,1)=0.5 != 0.
 D. Pascal mod 2: #P_k=3^k, autossemelhanca P_k = U Phi_i(P_{k-1}); piramide m: (m+1)^k.
 E. Legendre da parabola tau(q) e int_0^1 H = 1/2.
"""
import itertools
import numpy as np
import mpmath as mp

mp.mp.dps = 40


def E_closed(x):
    x = mp.mpf(x)
    return x * (x + 1) - x * mp.log(2 * mp.pi) - x * mp.loggamma(x + 1) + 2 * mp.log(mp.barnesg(x + 1))


def E_quad(x):
    x = mp.mpf(x)
    return mp.quad(lambda y: mp.loggamma(x + 1) - mp.loggamma(y + 1) - mp.loggamma(x - y + 1), [0, x / 2, x])


def E_asym(x, c_log=-mp.mpf(1) / 6, const=True):
    x = mp.mpf(x)
    r = x ** 2 / 2 - x / 2 * mp.log(x) + (1 - mp.log(2 * mp.pi) / 2) * x + c_log * mp.log(x)
    if const:
        r += 2 * mp.zeta(-1, derivative=1) - mp.mpf(1) / 12
    return r


def block_A():
    print("== A. Entropia de linha ==")
    for x in [0.5, 1, 3.7, 10]:
        print(f" x={x}: fechada-quadratura = {mp.nstr(E_closed(x) - E_quad(x), 5)}")
    print(" x, resto R=E-asym, x^2*R, ctrl(-ln/12), ctrl(sem const)")
    for x in [10, 100, 1000, 10000]:
        R = E_closed(x) - E_asym(x)
        print(f" {x:6d} {mp.nstr(R, 6):>14} {mp.nstr(R * x * x, 6):>10} {mp.nstr(E_closed(x) - E_asym(x, -mp.mpf(1) / 12), 5):>10} {mp.nstr(E_closed(x) - E_asym(x, const=False), 5):>10}")
    print(" E(x)/x^2 em x=1e4:", mp.nstr(E_closed(10000) / 10000 ** 2, 8))


def sierpinski_graph(m, k):
    """vertices = pontos de F_w(v_j), arestas = arestas dos simplexos do nivel k (coordenadas inteiras 2^k)."""
    V = np.eye(m + 1, dtype=np.int64)  # coordenadas baricentricas *1
    cells = [tuple(map(tuple, V))]
    for lev in range(k):
        new = []
        for c in cells:
            c = np.array(c) * 2
            for j in range(m + 1):
                new.append(tuple(map(tuple, (c + c[j]) // 2)))
        cells = new
    idx = {}
    edges = set()
    for c in cells:
        ids = []
        for p in c:
            if p not in idx:
                idx[p] = len(idx)
            ids.append(idx[p])
        for a, b in itertools.combinations(ids, 2):
            edges.add((min(a, b), max(a, b)))
    n = len(idx)
    L = np.zeros((n, n))
    for a, b in edges:
        L[a, a] += 1; L[b, b] += 1; L[a, b] -= 1; L[b, a] -= 1
    corners = [idx[tuple(v)] for v in (V * 2 ** k)] if k > 0 else list(range(m + 1))
    return L, corners


def schur_trace(L, B):
    I = [i for i in range(len(L)) if i not in B]
    return L[np.ix_(B, B)] - L[np.ix_(B, I)] @ np.linalg.solve(L[np.ix_(I, I)], L[np.ix_(I, B)])


def block_B():
    print("== B. Renormalizacao de Kigami ==")
    for m in [2, 3, 4, 5]:
        L1, cor = sierpinski_graph(m, 1)
        T = schur_trace(L1, cor)
        L0, _ = sierpinski_graph(m, 0)
        rho = L0[0, 1] / T[0, 1]   # fator de condutancia para que traco(rho*L1) = L0
        print(f" m={m}: rho numerico={rho:.6f}  (m+3)/(m+1)={(m + 3) / (m + 1):.6f}  ctrl (m+2)/m={(m + 2) / m:.6f}  r_m=(m+1)rho={(m + 1) * rho:.6f}")
    for m, ks in [(2, [3, 4, 5, 6]), (3, [2, 3, 4, 5])]:
        lam = []
        for k in ks:
            L, _ = sierpinski_graph(m, k)
            ev = np.linalg.eigvalsh(L)
            lam.append(ev[1])
        rat = [lam[i] / lam[i + 1] for i in range(len(lam) - 1)]
        print(f" m={m}: lambda_1(k)/lambda_1(k+1) = {np.round(rat, 5)}  (esperado -> m+3 = {m + 3})")
        ds = 2 * np.log(m + 1) / np.log(m + 3)
        print(f"   d_s = 2 ln(m+1)/ln(m+3) = {ds:.6f}")


def block_C():
    print("== C. Reflexao e linhas nodais ==")
    rng = np.random.default_rng(7)
    worst = 0; worst_bad = 0
    for _ in range(200):
        x = mp.mpf(rng.uniform(-6, 6)); y = mp.mpf(rng.uniform(-6, 6))
        lhs = mp.gamma(x + 1) / (mp.gamma(y + 1) * mp.gamma(x - y + 1))
        rhs = -1 / mp.pi * mp.sin(mp.pi * y) * mp.sin(mp.pi * (x - y)) / mp.sin(mp.pi * x) * mp.gamma(y - x) * mp.gamma(-y) / mp.gamma(-x)
        worst = max(worst, abs(lhs - rhs) / abs(lhs)); worst_bad = max(worst_bad, abs(lhs + rhs) / abs(lhs))
    print(f" max erro relativo = {mp.nstr(worst, 3)}; controle com sinal trocado = {mp.nstr(worst_bad, 3)}")
    b = lambda x, y: mp.gamma(x + 1) * mp.rgamma(y + 1) * mp.rgamma(x - y + 1)
    print(" binom(0.5,1) =", b(0.5, 1), "; binom(2.3,1) =", mp.nstr(b(2.3, 1), 6), "; binom(0.5,-1) =", b(0.5, -1),
          "; binom(0.5,1.5)=", b(0.5, 1.5), "; binom(0.5, 2.5)=", mp.nstr(b(0.5, 2.5), 6))


def block_D():
    print("== D. Pascal mod 2 ==")
    from math import comb
    for k in range(1, 10):
        Pk = {(n, j) for n in range(2 ** k) for j in range(n + 1) if comb(n, j) % 2}
        Pk1 = {(n, j) for n in range(2 ** (k - 1)) for j in range(n + 1) if comb(n, j) % 2}
        h = 2 ** (k - 1)
        rec = Pk1 | {(n + h, j) for n, j in Pk1} | {(n + h, j + h) for n, j in Pk1}
        neg = {(a, j) for a in range(1, 2 ** k + 1) for j in range(0, 2 ** k + 1 - a) if ((-1) ** j * comb(a + j - 1, j)) % 2}
        print(f" k={k}: #P_k={len(Pk)} 3^k={3 ** k} recursao={'ok' if rec == Pk else 'FALHA'} #neg={len(neg)}")
    # piramide multinomial mod 2 (m coordenadas = m partes): contagem (m+1)^k
    from math import factorial
    for m in [3, 4]:
        for k in [1, 2, 3, 4]:
            cnt = 0
            for n in range(2 ** k):
                for parts in itertools.product(range(n + 1), repeat=m - 1):
                    if sum(parts) <= n:
                        last = n - sum(parts)
                        c = factorial(n)
                        for p in parts + (last,):
                            c //= factorial(p)
                        cnt += c % 2
            print(f" piramide m={m} (multinomial de {m} partes), k={k}: #impares={cnt}, (m+1)^k={(m + 1) ** k}")
    # box counting grosseiro para k=10
    k = 10
    pts = np.array([(n, j) for n in range(2 ** k) for j in range(n + 1) if (j & n) == j], float) / 2 ** k
    for e in [4, 5, 6, 7]:
        boxes = len({(int(p[0] * 2 ** e), int(p[1] * 2 ** e)) for p in pts})
        print(f"  escala 2^-{e}: N={boxes}, log N/log 2^e = {np.log(boxes) / (e * np.log(2)):.4f} (ln3/ln2={np.log(3) / np.log(2):.4f})")


def block_E():
    print("== E. Parabola multifractal ==")
    s2 = 0.5
    tau = lambda q: (q - 1) * np.log(2) - s2 / 2 * q ** 2
    q = np.linspace(-60, 60, 1200001)
    for al in [-0.5, 0.0, 0.3, np.log(2), 1.0, 1.5]:
        fnum = np.min(q * al - tau(q))
        fth = np.log(2) - (al - np.log(2)) ** 2 / (2 * s2)
        qstar = (np.log(2) - al) / s2
        print(f" alpha={al:.3f}: f num={fnum:.6f} formula={fth:.6f} q*={qstar:.3f}")
    print(" tau(1) =", tau(1), " tau'(1) =", np.log(2) - s2, " int H =", float(mp.quad(lambda t: -t * mp.log(t) - (1 - t) * mp.log(1 - t), [0, 1])))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1: [globals()["block_" + c]() for c in sys.argv[1]]; sys.exit()
    block_A(); block_B(); block_C(); block_D(); block_E()
