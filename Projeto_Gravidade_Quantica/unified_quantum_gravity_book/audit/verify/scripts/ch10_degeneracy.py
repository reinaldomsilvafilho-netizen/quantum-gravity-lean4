"""Camada 1 (cega), cap. 10: degenerescencia de kappa*_info alem da Prop. 2.1.

Modelo com metrica de Fisher legitima: y ~ N(m(theta), I_3), m(theta) = (theta1, theta2, psi(theta)),
psi = A (1 - r^2)^3 em r = |theta - c| < 1 (c = (2,0)), 0 fora. Fisher = I + grad psi grad psi^T;
regularizada: g = (1+lam0) I + grad psi grad psi^T, cond(g) = 1 + |grad psi|^2/(1+lam0).
O_sing = {cond > Lmax} e' um anel dentro do disco |theta - c| < 1.
theta0 = 0, Sigma* = disco de raio 0.1 em p = (4,0).

(1) Tiro de geodesicas (Christoffel Gamma^k_ij = psi_k psi_ij/(a+|grad psi|^2), a = 1+lam0) a partir de
    theta0 em todos os angulos: nenhuma chega a Sigma* sem entrar em O_sing -> hipotese da Prop. 2.1 falha.
(2) Familia de arcos circulares de raio R (grande) por theta0 e p, pelo lado de cima (arco maior), que
    ficam fora do suporte de psi (metrica euclidiana -> aceleracao covariante = 1/R). Logo
    kappa*_info <= 1/R -> 0: kappa*_info = 0 (nao atingido), embora nenhuma geodesica sirva.
    Isto porque a definicao nao limita o comprimento L (o cap. 7 limita: 'length at most L').
Controle negativo: o arco menor do mesmo circulo e o segmento reto entram em O_sing.
"""
import numpy as np
from scipy.integrate import solve_ivp

A, lam0, Lmax = 10.0, 0.1, 1.5
a = 1 + lam0
c = np.array([2.0, 0.0]); p = np.array([4.0, 0.0]); rS = 0.1


def grad_hess(th):
    d = th - c; r2 = d @ d
    if r2 >= 1:
        return np.zeros(2), np.zeros((2, 2))
    u = 1 - r2
    g = -6 * A * u ** 2 * d
    H = -6 * A * (u ** 2 * np.eye(2) - 4 * u * np.outer(d, d))
    return g, H


def cond(th):
    g, _ = grad_hess(th)
    return 1 + g @ g / a


def in_sing(th):
    return cond(th) > Lmax


def rhs(s, z):
    th, v = z[:2], z[2:]
    g, H = grad_hess(th)
    acc = -g * (v @ H @ v) / (a + g @ g)
    return np.concatenate([v, acc])


def check_hessian_fd():
    rng = np.random.default_rng(3)
    th = c + 0.3 * rng.standard_normal(2); h = 1e-6
    psi = lambda t: A * max(0.0, 1 - (t - c) @ (t - c)) ** 3
    gfd = np.array([(psi(th + h*e) - psi(th - h*e)) / (2*h) for e in np.eye(2)])
    g, H = grad_hess(th)
    Hfd = np.array([(grad_hess(th + h*e)[0] - grad_hess(th - h*e)[0]) / (2*h) for e in np.eye(2)])
    return np.abs(gfd - g).max(), np.abs(Hfd - H).max()


def shoot(angle, smax=6.0):
    v0 = np.array([np.cos(angle), np.sin(angle)]) / np.sqrt(a)   # g-unit speed outside bump
    sol = solve_ivp(rhs, (0, smax * np.sqrt(a)), np.concatenate([[0, 0], v0]),
                    max_step=0.01, rtol=1e-9, atol=1e-11)
    pts = sol.y[:2].T
    hit_sing = np.array([in_sing(q) for q in pts])
    hit_S = np.linalg.norm(pts - p, axis=1) <= rS
    first_S = np.argmax(hit_S) if hit_S.any() else None
    first_sing = np.argmax(hit_sing) if hit_sing.any() else None
    good = first_S is not None and (first_sing is None or first_sing > first_S)
    return good, first_S is not None


def main():
    ok = True
    e1, e2 = check_hessian_fd()
    print(f"grad/Hess psi vs finite differences: {e1:.1e}, {e2:.1e}")
    ok &= e1 < 1e-5 and e2 < 1e-4
    rr = np.linspace(0, 1, 2001)
    cmax = max(cond(c + np.array([r, 0])) for r in rr)
    ring = [r for r in rr if cond(c + np.array([r, 0])) > Lmax]
    print(f"max cond = {cmax:.1f}; O_sing = anel r in [{min(ring):.3f}, {max(ring):.3f}]")

    # (1) geodesic shooting: only angles within asin(1/2) can meet the bump; others are straight rays
    angles = np.concatenate([np.linspace(-0.53, 0.53, 531), np.linspace(0.38, 0.53, 301), -np.linspace(0.38, 0.53, 301)])  # |angle|>asin(1/2) nunca toca o suporte
    res = [shoot(t) for t in angles]
    n_good = sum(r[0] for r in res); n_reach = sum(r[1] for r in res)
    print(f"(1) geodesicas disparadas: {len(angles)}; chegam a Sigma*: {n_reach}; "
          f"chegam sem tocar O_sing: {n_good}")
    ok &= n_good == 0

    # (2) arcs: circle through 0 and p with centre (2, h), major arc over the top
    for h in [2.0, 5.0, 20.0, 100.0]:
        R = np.hypot(2, h); ctr = np.array([2.0, h])
        a0 = np.arctan2(-h, -2); a1 = np.arctan2(-h, 2)     # angles of theta0 and p
        # major arc: go from a0 clockwise (decreasing angle) the long way to a1
        ts = np.linspace(0, 1, 20001)
        # minor arc passes through the bottom point (2, h-R); major arc is the complement
        angs_minor = a0 + ((a1 - a0) % (2*np.pi)) * ts
        angs_major = a0 - ((a0 - a1) % (2*np.pi)) * ts
        pm = ctr + R * np.stack([np.cos(angs_minor), np.sin(angs_minor)], 1)
        pM = ctr + R * np.stack([np.cos(angs_major), np.sin(angs_major)], 1)
        if np.min(np.linalg.norm(pm - c, axis=1)) > np.min(np.linalg.norm(pM - c, axis=1)):
            pm, pM = pM, pm
        dmin = np.min(np.linalg.norm(pM - c, axis=1))
        sing_major = any(in_sing(q) for q in pM[::10])
        sing_minor = any(in_sing(q) for q in pm[::10])
        # curvature of the arc in the g-metric (Euclidean scaled by a outside bump): 1/(sqrt(a) R)
        # numerical check via discrete Frenet: angle change / length
        seg = np.diff(pM, axis=0); L = np.linalg.norm(seg, axis=1).sum()
        tang = np.arctan2(seg[:, 1], seg[:, 0]); dtheta = np.abs(np.diff(np.unwrap(tang)))
        kap = np.max(dtheta / np.linalg.norm(seg[1:], axis=1))
        print(f"(2) h={h:6.1f}: R={R:8.2f}  arco maior: dist min ao suporte {dmin:.3f} (>1), "
              f"toca O_sing? {sing_major}; kappa_euc={kap:.4f} (1/R={1/R:.4f}), g-curv={kap/np.sqrt(a):.4f}; "
              f"comprimento {L:.1f} | ctrl arco menor toca O_sing? {sing_minor}")
        ok &= (not sing_major) and dmin > 1 and sing_minor and abs(kap - 1/R) < 1e-3
    seg_line = np.linspace(0, 1, 4001)[:, None] * p
    ctrl_line = any(in_sing(q) for q in seg_line)
    print(f"ctrl: segmento reto theta0->p toca O_sing? {ctrl_line}")
    ok &= ctrl_line
    print("ALL CHECKS OK" if ok else "SOME CHECK FAILED")


if __name__ == "__main__":
    main()
