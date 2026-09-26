"""Cap. 5 -- verificacoes cegas independentes (camada 1).

Blocos:
 A. Prop. 2.2 (representacao de Fourier), m=2, n=1, P nao ortonormal.
    Controle negativo: sem o fator sqrt(det PP^T) e com Khat(+k) no lugar de Khat(-k).
 B. Decaimento de Fourier do nucleo Beta (gamma): |k| |Khat(k)| ao longo das normais
    de facetas (nao tende a 0 => gamma<=1) e limitado (=> gamma=1 vale).
 C. Prop. 4.1 (formula de inversao): FBP com filtro |xi|^{m-n} aplicado aos dados de
    RESTRICAO g_theta(z)=h(P^+ z) (a definicao do capitulo) nao reproduz h.
    Controle positivo: os mesmos passos com dados de PROJECAO (integrais de linha) reproduzem (2pi)^2 h.
 D. Teorema 5.2 (contracao baricentrica): testes aleatorios + caso de igualdade;
    controle negativo com constante 0.99*alpha/(alpha+m).
 E. Teorema 6.2 (autovalores (a)_lambda/(a+b)_lambda) por Monte Carlo com m=2,
    polinomios zonais C_(2), C_(1,1). Controle negativo: Pochhammer sem o deslocamento -(j-1)/2.
 F. Lema de fibra do teorema do traco: int_{R^d}(1+A+|eta|^2)^{-s} = pi^{d/2}Gamma(s-d/2)/Gamma(s) (1+A)^{d/2-s}.
"""
import numpy as np
from scipy.special import gammaln, rgamma, gamma as G
from numpy.polynomial.legendre import leggauss

rng = np.random.default_rng(12345)


# ---------- nucleo Beta normalizado em Delta_2(alpha) subset R^2 ----------
def tri_nodes(alpha, N):
    x, w = leggauss(N)
    u = (x + 1) / 2; wu = w / 2
    U, V = np.meshgrid(u, u, indexing="ij")
    WU, WV = np.meshgrid(wu, wu, indexing="ij")
    y1 = alpha * U
    y2 = alpha * (1 - U) * V
    J = alpha ** 2 * (1 - U)
    return y1.ravel(), y2.ravel(), (WU * WV * J).ravel()


def kernel_nodes(alpha, N=80):
    y1, y2, w = tri_nodes(alpha, N)
    y3 = alpha - y1 - y2
    K = G(alpha + 1) * rgamma(y1 + 1) * rgamma(y2 + 1) * rgamma(y3 + 1)
    w = w * K
    return y1, y2, w / w.sum()


def block_A():
    print("== A. Representacao de Fourier (m=2,n=1) ==")
    alpha = 1.3
    y1, y2, wk = kernel_nodes(alpha, 60)
    P = np.array([1.0, 2.0]); detPPt = P @ P
    Pplus = P / detPPt
    a = np.array([0.7, -0.4])
    f = lambda X1, X2: np.exp(-((X1 - a[0]) ** 2 + (X2 - a[1]) ** 2) / 2)
    fhat = lambda k1, k2: 2 * np.pi * np.exp(-1j * (k1 * a[0] + k2 * a[1])) * np.exp(-(k1 ** 2 + k2 ** 2) / 2)
    Khat = lambda k1, k2: np.sum(wk[None, :] * np.exp(-1j * (np.outer(k1, y1) + np.outer(k2, y2))), axis=1)
    z = np.linspace(-45, 45, 9001); dz = z[1] - z[0]
    Rf = np.array([np.sum(wk * f(Pplus[0] * zz + y1, Pplus[1] * zz + y2)) for zz in z])
    u = np.array([2.0, -1.0]) / np.sqrt(5)
    t = np.linspace(-9, 9, 3601); dt = t[1] - t[0]
    ok = True
    for xi in [0.3, 0.8, 1.7]:
        lhs = np.sum(np.exp(-1j * xi * z) * Rf) * dz
        k1 = P[0] * xi + t * u[0]; k2 = P[1] * xi + t * u[1]
        integ = fhat(k1, k2)
        rhs = (2 * np.pi) ** (1 - 2) * np.sqrt(detPPt) * np.sum(integ * Khat(-k1, -k2)) * dt
        bad1 = rhs / np.sqrt(detPPt)
        bad2 = (2 * np.pi) ** (-1) * np.sqrt(detPPt) * np.sum(integ * Khat(k1, k2)) * dt
        e0 = abs(lhs - rhs) / abs(lhs); e1 = abs(lhs - bad1) / abs(lhs); e2 = abs(lhs - bad2) / abs(lhs)
        print(f" xi={xi}: LHS={lhs:.6f} RHS={rhs:.6f} relerr={e0:.1e} | ctrl sem sqrtdet={e1:.2f} | ctrl Khat(+k)={e2:.2f}")
        ok &= e0 < 1e-6 and e1 > 0.1 and e2 > 0.01
    print(" A:", "OK" if ok else "FALHOU")


def block_B():
    print("== B. Decaimento |k||Khat(k)| do nucleo Beta (m=2) ==")
    for alpha in [0.5, 1.0, 3.0]:
        y1, y2, wk = kernel_nodes(alpha, 400)
        dirs = {"e1 (normal faceta y1=0)": np.array([1.0, 0.0]),
                "(1,1)/sqrt2 (normal faceta y1+y2=alpha)": np.array([1.0, 1.0]) / np.sqrt(2),
                "generica (1,0.37)": np.array([1.0, 0.37]) / np.hypot(1, 0.37)}
        for name, d in dirs.items():
            vals = []
            for T in [25, 50, 100, 200]:
                ts = np.linspace(T, T * 1.05, 12)
                kh = np.array([np.sum(wk * np.exp(-1j * tt * (d[0] * y1 + d[1] * y2))) for tt in ts])
                vals.append(np.max(np.abs(kh) * ts))
            print(f" alpha={alpha} dir={name}: max |k||Khat| em janelas T=25,50,100,200 ->", np.round(vals, 4))


def block_C():
    print("== C. Formula de inversao (m=2,n=1): dados de restricao vs projecao ==")
    alpha = 1.0
    y1, y2, wk = kernel_nodes(alpha, 16)
    a = np.array([1.5, 0.0])
    f = lambda X1, X2: np.exp(-((X1 - a[0]) ** 2 + (X2 - a[1]) ** 2) / 2)
    def h(X1, X2, ch=20000):
        out = np.empty(len(X1))
        for i in range(0, len(X1), ch):
            a1 = X1[i:i + ch]; a2 = X2[i:i + ch]
            out[i:i + ch] = np.sum(wk[None, :] * f(a1[:, None] + y1[None, :], a2[:, None] + y2[None, :]), axis=1)
        return out
    nth = 120
    th = (np.arange(nth) + 0.5) * np.pi / nth; dth = np.pi / nth
    z = np.linspace(-12, 12, 481); dz = z[1] - z[0]
    xi = np.linspace(-10, 10, 801); dxi = xi[1] - xi[0]
    E = np.exp(-1j * np.outer(xi, z))
    ghat_res = []; ghat_proj = []
    s = np.linspace(-12, 12, 241); ds = s[1] - s[0]
    for t in th:
        c, sn = np.cos(t), np.sin(t)
        gres = h(z * c, z * sn)                       # restricao a reta span(theta) (definicao do cap.)
        ghat_res.append(E @ gres * dz)
        # projecao: integral de h ao longo de theta_perp, deslocamento z
        ZZ, SS = np.meshgrid(z, s, indexing="ij")
        X1 = (ZZ * c - SS * sn).ravel(); X2 = (ZZ * sn + SS * c).ravel()
        gproj = h(X1, X2).reshape(ZZ.shape).sum(axis=1) * ds
        ghat_proj.append(E @ gproj * dz)
    ghat_res = np.array(ghat_res); ghat_proj = np.array(ghat_proj)
    pts = [(1.5, 0.0), (0.0, 1.5), (-1.0, 0.5), (2.5, 1.0)]
    print(" x        h(x)      B_restr/h    B_proj/h   (esperado constante; (2pi)^2=%.4f)" % (4 * np.pi ** 2))
    for (x1, x2) in pts:
        hx = h(np.array([x1]), np.array([x2]))[0]
        Br = 0; Bp = 0
        for i, t in enumerate(th):
            ph = np.exp(1j * xi * (np.cos(t) * x1 + np.sin(t) * x2)) * np.abs(xi)
            Br += np.sum(ph * ghat_res[i]) * dxi * dth
            Bp += np.sum(ph * ghat_proj[i]) * dxi * dth
        print(f" {x1:5.2f},{x2:5.2f}  {hx:.5f}  {(Br / hx).real:10.4f}  {(Bp / hx).real:10.4f}")


def block_D():
    print("== D. Contracao baricentrica ==")
    worst = 0; eq_hits = 0; neg_fail = 0
    for trial in range(20000):
        m = rng.integers(2, 8); n = rng.integers(1, m + 1)
        pi = np.concatenate([np.arange(n), rng.integers(0, n, m - n)]); rng.shuffle(pi)
        alpha = rng.uniform(0.01, 50)
        c1 = rng.dirichlet(np.ones(m)); c2 = rng.dirichlet(np.ones(m))
        Phi = lambda c: np.array([(alpha * c[pi == k].sum() + (pi == k).sum()) / (alpha + m) for k in range(n)])
        p1, p2 = Phi(c1), Phi(c2)
        assert abs(p1.sum() - 1) < 1e-12 and (p1 >= 0).all()
        r = 0.5 * np.abs(p1 - p2).sum() / (0.5 * np.abs(c1 - c2).sum())
        worst = max(worst, r / (alpha / (alpha + m)))
        # caso de igualdade: c1-c2 sem troca de sinal nas fibras -> use n=m
        if n == m:
            eq_hits += abs(r - alpha / (alpha + m)) < 1e-12
            if r > 0.99 * alpha / (alpha + m) + 1e-12:
                neg_fail += 1
    print(f" max razao/(alpha/(alpha+m)) = {worst:.12f} (<=1 esperado)")
    print(f" igualdade exata nos casos n=m: {eq_hits}; controle negativo (0.99*const) violado em {neg_fail} casos")
    alpha = 3.0; m = 4; pi = np.array([0, 0, 1, 1])
    c1 = np.array([.5, 0, .5, 0]); c2 = np.array([0, .5, 0, .5])
    Phi = lambda c: np.array([(alpha * c[pi == k].sum() + (pi == k).sum()) / (alpha + m) for k in range(2)])
    print(" exemplo do texto: Phi(c1)-Phi(c2) =", Phi(c1) - Phi(c2))
    # Media de Dirichlet(alpha c +1) empurrada: Monte Carlo
    c = np.array([0.1, 0.2, 0.3, 0.4]); pi = np.array([0, 1, 1, 0])
    S = rng.dirichlet(alpha * c + 1, 400000)
    mc = np.array([S[:, pi == k].sum(1).mean() for k in range(2)])
    print(" Dirichlet MC", mc, " formula", Phi(c) if False else np.array([(alpha * c[pi == k].sum() + (pi == k).sum()) / (alpha + 4) for k in range(2)]))


def poch(a, lam, shift=True):
    out = 1.0
    for j, l in enumerate(lam, start=1):
        b = a - (j - 1) / 2 if shift else a
        out *= np.exp(gammaln(b + l) - gammaln(b))
    return out


def block_E():
    print("== E. Siegel-Wishart: eigenvalores zonais, m=2 (Monte Carlo) ==")
    m = 2; a, b = 2.0, 1.5   # 2a=4, 2b=3 graus de liberdade inteiros
    N = 400000
    A = rng.standard_normal((N, 4, m)); B = rng.standard_normal((N, 3, m))
    WA = np.einsum("nij,nik->njk", A, A); WB = np.einsum("nij,nik->njk", B, B)
    S = WA + WB
    L = np.linalg.cholesky(S)  # S = L L^T
    Li = np.linalg.inv(L)
    Y = Li @ WA @ np.transpose(Li, (0, 2, 1))   # Beta_m(a,b) (Muirhead Def. 3.3.2)
    X = np.array([[2.0, 0.7], [0.7, 1.0]])
    w, V = np.linalg.eigh(X); Xh = V @ np.diag(np.sqrt(w)) @ V.T
    M = Xh @ Y @ Xh
    ev = np.linalg.eigvalsh(M)
    x1, x2 = ev[:, 0], ev[:, 1]
    lx = np.linalg.eigvalsh(X)
    zon = {(1, 0): (lambda p, q: p + q), (2, 0): (lambda p, q: p ** 2 + q ** 2 + 2 / 3 * p * q), (1, 1): (lambda p, q: 4 / 3 * p * q)}
    for lam, Z in zon.items():
        vals = Z(x1, x2)
        mc = vals.mean(); se = vals.std() / np.sqrt(N)
        pred = poch(a, lam) / poch(a + b, lam) * Z(*lx)
        bad = poch(a, lam, False) / poch(a + b, lam, False) * Z(*lx)
        print(f" lambda={lam}: MC={mc:.5f}+-{se:.5f}  formula={pred:.5f} (z={(mc - pred) / se:.2f})  ctrl sem -(j-1)/2: {bad:.5f} (z={(mc - bad) / se:.1f})")


def block_F():
    print("== F. Lema de fibra do traco ==")
    from scipy.integrate import quad
    for d, s, A in [(1, 1.2, 3.0), (2, 1.7, 10.0), (3, 2.5, 0.5)]:
        num = quad(lambda r: (1 + A + r * r) ** (-s) * r ** (d - 1), 0, np.inf)[0] * 2 * np.pi ** (d / 2) / G(d / 2)
        th = np.pi ** (d / 2) * G(s - d / 2) / G(s) * (1 + A) ** (d / 2 - s)
        print(f" d={d} s={s}: num={num:.8f} teoria={th:.8f}  ctrl expoente -s+d: {(1 + A) ** (d - s) * np.pi ** (d / 2) * G(s - d / 2) / G(s):.4f}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'C':
        block_C()
    else:
        block_A(); block_B(); block_D(); block_E(); block_F(); block_C()
