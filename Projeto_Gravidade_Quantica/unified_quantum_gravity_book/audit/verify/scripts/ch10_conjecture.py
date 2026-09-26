"""Camada 1 (cega), cap. 10: Conjectura 3.1 (Stiefel).

(a) A primeira parte ("lambda_min(g~) limitado inferiormente ao longo da trajetoria") e' trivial:
    g~ = g + lam0 I com g PSD => lambda_min(g~) >= lam0 para QUALQUER theta (Weyl).
    Oraculo: Fisher empirica J^T J de uma rede aleatoria (posto <= N) em varios theta.
    Controle negativo: sem lam0, lambda_min = 0 (D > N).
(b) Restricao Stiefel com camadas quadradas: rede linear profunda W_L...W_1 com W_i ortogonais
    representa so' mapas ortogonais; alvo 2I tem perda >= ||2I - Q||_F^2 min = d (Q = I) > 0.
    Logo Sigma* pode ser vazio/inalcancavel sob a restricao para eps pequeno.
"""
import numpy as np

rng = np.random.default_rng(0)
ok = True
lam0 = 1e-3
N, din, h = 5, 4, 6                      # 2-layer tanh net, scalar output, D = h*din + h
for trial in range(5):
    W1 = rng.standard_normal((h, din)) * (1 + trial); w2 = rng.standard_normal(h)
    X = rng.standard_normal((N, din))
    Z = np.tanh(X @ W1.T)                               # N x h
    # Jacobian of f(x) = w2 . tanh(W1 x) wrt (W1, w2)
    J = np.concatenate([((w2 * (1 - Z**2))[:, :, None] * X[:, None, :]).reshape(N, -1), Z], 1)
    F = J.T @ J / N
    lmin_reg = np.linalg.eigvalsh(F + lam0 * np.eye(F.shape[0])).min()
    lmin = np.linalg.eigvalsh(F).min()
    print(f"trial {trial}: D={F.shape[0]}, rank F={np.linalg.matrix_rank(F)}, "
          f"lmin(F+lam0 I)={lmin_reg:.3e} (>= lam0={lam0}), ctrl lmin(F)={lmin:.1e}")
    ok &= lmin_reg >= lam0 - 1e-12 and abs(lmin) < 1e-10

d, L = 5, 6
best = np.inf
for _ in range(2000):
    Q = np.eye(d)
    for _ in range(L):
        q, _r = np.linalg.qr(rng.standard_normal((d, d)))
        Q = q @ Q
    best = min(best, np.sum((2 * np.eye(d) - Q) ** 2))
print(f"(b) min ||2I - W_L..W_1||_F^2 sobre produtos ortogonais amostrados = {best:.3f} "
      f"(cota exata min_Q ||2I-Q||^2 = d = {d})")
ok &= best >= d - 1e-9
print("ALL CHECKS OK" if ok else "SOME CHECK FAILED")
