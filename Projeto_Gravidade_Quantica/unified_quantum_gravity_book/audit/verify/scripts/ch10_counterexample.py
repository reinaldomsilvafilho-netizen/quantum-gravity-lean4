"""Camada 1 (cega), cap. 10: reimplementacao independente da Prop. 2.2.

Verifica, sem usar audit/scripts/check_ch10.py:
  A. Fisher do modelo gaussiano linear = E[x x^T] (oraculo: Monte Carlo do score), constante em theta.
  B. Hessiana da NLL = X^T X / N (oraculo: diferencas finitas), Tr > 0.
  C. Gap de generalizacao do interpolante de norma minima com rotulos aleatorios +-1 e perda
     quadratica truncada em [0,1], varios (N, D), varias sementes, e duas escalas de x.
  D. Limite inferior analitico: para y uniforme em {+-1} independente de x, qualquer preditor f
     tem E min((y-f)^2,1) >= 1/2, logo gap >= 1/2 para qualquer interpolante.
  E. Valor do "bound" sqrt(ln(2/delta)/(2N)) e controle negativo (mutacao /N em vez de /2N).
  F. Controle negativo: professor linear verdadeiro, N >> D -> gap ~ 0 (abaixo do bound).
"""
import numpy as np


def clipped(r):
    return np.minimum(r ** 2, 1.0)


def gap_random_labels(N, D, seed, scale=1.0, ntest=200_000):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((N, D)) * scale
    y = rng.choice([-1.0, 1.0], size=N)
    theta = np.linalg.pinv(X) @ y
    train = clipped(y - X @ theta).mean()
    Xt = rng.standard_normal((ntest, D)) * scale
    yt = rng.choice([-1.0, 1.0], size=ntest)
    test = clipped(yt - Xt @ theta).mean()
    return train, test, test - train, float(theta @ theta)


def fisher_mc(theta, D, rng, M=400_000):
    x = rng.standard_normal((M, D))
    y = x @ theta + rng.standard_normal(M)
    s = x * (y - x @ theta)[:, None]          # score of log N(y; x^T theta, 1)
    return s.T @ s / M


def main():
    ok = True
    rng = np.random.default_rng(12345)
    # A. Fisher constancy
    D = 4
    F1 = fisher_mc(np.zeros(D), D, rng)
    F2 = fisher_mc(3 * rng.standard_normal(D), D, rng)
    errA = max(np.abs(F1 - np.eye(D)).max(), np.abs(F2 - np.eye(D)).max())
    print(f"A. max|Fisher_MC - E[xx^T]| at two thetas = {errA:.3e}")
    ok &= errA < 0.03
    # negative control for A: heteroscedastic mutated model sigma(theta) -> Fisher depends on theta
    # (score for mean only, noise var 1+|theta|^2): Fisher = E[xx^T]/(1+|theta|^2)
    th = 3 * np.ones(D)
    x = rng.standard_normal((200_000, D)); s2 = 1 + th @ th
    yv = x @ th + np.sqrt(s2) * rng.standard_normal(200_000)
    sc = x * ((yv - x @ th) / s2)[:, None]
    Fm = sc.T @ sc / 200_000
    print(f"A-ctrl. mutated heteroscedastic model: Fisher diag mean {np.diag(Fm).mean():.4f} (!=1)")
    ok &= abs(np.diag(Fm).mean() - 1) > 0.5

    # B. Hessian by finite differences
    N, D = 7, 12
    X = rng.standard_normal((N, D)); y = rng.standard_normal(N)
    nll = lambda t: 0.5 * np.mean((y - X @ t) ** 2)
    t0 = rng.standard_normal(D); h = 1e-4; H = np.zeros((D, D)); E = np.eye(D)
    for i in range(D):
        for j in range(D):
            H[i, j] = (nll(t0 + h*E[i] + h*E[j]) - nll(t0 + h*E[i] - h*E[j])
                       - nll(t0 - h*E[i] + h*E[j]) + nll(t0 - h*E[i] - h*E[j])) / (4*h*h)
    errB = np.abs(H - X.T @ X / N).max()
    print(f"B. max|H_fd - X^TX/N| = {errB:.2e}; Tr H = {np.trace(H):.3f} ; ||X||_F^2/N = {np.sum(X**2)/N:.3f}")
    ok &= errB < 1e-5 and np.trace(H) > 0
    errBmut = np.abs(H - X.T @ X).max()
    print(f"B-ctrl. mutated (no 1/N): max err = {errBmut:.2f} (must be large)")
    ok &= errBmut > 0.1

    # C. random-label gaps
    print("C. random labels, x ~ N(0, I_D), clipped square loss")
    for (N, D) in [(50, 200), (20, 100), (100, 400), (50, 60), (200, 800), (50, 1000)]:
        gaps = []; norms = []
        for seed in [1, 7, 2024, 31337, 99]:
            tr, te, g, nrm = gap_random_labels(N, D, seed)
            assert tr < 1e-20
            gaps.append(g); norms.append(nrm)
        print(f"   N={N:4d} D={D:5d}: gap mean {np.mean(gaps):.3f} [min {min(gaps):.3f}, max {max(gaps):.3f}]"
              f"  ||theta||^2 mean {np.mean(norms):.3f} (Wishart pred N/(D-N-1)={N/(D-N-1):.3f})")
        ok &= min(gaps) >= 0.5
    print("C'. same (N,D)=(50,200) but x ~ N(0, I/D) (escala de x nao especificada no texto)")
    gs = [gap_random_labels(50, 200, s, scale=1/np.sqrt(200))[2] for s in [1, 7, 2024]]
    print(f"   gaps {np.round(gs, 3)}  -> invariante por escala (X^+ escala por 1/c); sempre >= 0.5")

    # D. analytic lower bound: min over f of E_y min((y-f)^2,1)
    f = np.linspace(-3, 3, 60001)
    val = 0.5 * (np.minimum((1 - f) ** 2, 1) + np.minimum((1 + f) ** 2, 1))
    print(f"D. min_f E_y clipped loss = {val.min():.4f} at f = {f[val.argmin()]:.3f}")
    ok &= abs(val.min() - 0.5) < 1e-6

    # E. bound
    delta, N = 0.05, 50
    b = np.sqrt(np.log(2 / delta) / (2 * N))
    bmut = np.sqrt(np.log(2 / delta) / N)
    bmaurer = np.sqrt(np.log(2 * np.sqrt(N) / delta) / (2 * N))
    print(f"E. bound sqrt(ln(2/d)/2N) = {b:.4f}; mutated /N = {bmut:.4f}; Maurer ln(2sqrtN/d) = {bmaurer:.4f}")
    ok &= abs(b - 0.19) < 0.005 and abs(bmut - 0.19) > 0.05

    # F. negative control: true linear teacher, N >> D
    rs = np.random.default_rng(5)
    N, D = 5000, 20
    th = rs.standard_normal(D) / np.sqrt(D)
    X = rs.standard_normal((N, D)); y = X @ th + 0.1 * rs.standard_normal(N)
    t = np.linalg.lstsq(X, y, rcond=None)[0]
    Xt = rs.standard_normal((200_000, D)); yt = Xt @ th + 0.1 * rs.standard_normal(200_000)
    g = clipped(yt - Xt @ t).mean() - clipped(y - X @ t).mean()
    print(f"F. teacher control N={N}, D={D}: gap = {g:.4f} (bound at this N: {np.sqrt(np.log(40)/(2*N)):.4f})")
    ok &= abs(g) < np.sqrt(np.log(40) / (2 * N))
    print("ALL CHECKS OK" if ok else "SOME CHECK FAILED")


if __name__ == "__main__":
    main()
