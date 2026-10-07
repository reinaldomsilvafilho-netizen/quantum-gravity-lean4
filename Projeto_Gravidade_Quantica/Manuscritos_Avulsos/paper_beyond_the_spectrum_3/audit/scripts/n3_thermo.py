"""OBL-011 (Jarzynski) and OBL-012 (dissipation vs W2) on Gaussian protocols.
Units: k_B T = 1, mobility 1 (SDE dX = -V' dt + sqrt2 dW), so [x]^2 = [t].
OBL-012 test: dragged trap V_s(x) = kappa (x - s a)^2 / 2, W2(mu_A, mu_B) = |a|.
 oracle 1: closed form tau<W> = a^2 (1 - (1 - e^{-kappa tau})/(kappa tau));
 oracle 2: Euler-Maruyama Monte Carlo;
 oracle 3: friction metric g = int Cov(d_sV(X_0), d_sV(X_t)) dt computed by quadrature of the OU covariance.
Paper: lim tau Sigma = L^2/2 >= kappa W2^2/4. Negative control: kappa=1 (claim true) vs kappa=10 (false).
OBL-011: Phi_s(x) = Tr_s sqrt(k_s/2pi) exp(-k_s x^2/2) so Z(A_s)=Tr_s; check E[e^{-W}] = Tr_B/Tr_A."""
import numpy as np, sys
from scipy.integrate import quad
rng = np.random.default_rng(2024)
fails = 0
a = 1.0
for kappa in [1.0, 10.0]:
    print('--- kappa =', kappa)
    for tau in [10.0, 100.0, 1000.0]:
        exact = a ** 2 * (1 - (1 - np.exp(-kappa * tau)) / (kappa * tau))
        print('tau=%7.1f  tau*Sigma (closed form) = %.6f' % (tau, exact))
    # Monte Carlo at tau = 20, dt refinement
    tau = 20.0
    for dt in [0.01, 0.005]:
        N, steps = 20000, int(tau / dt)
        x = rng.normal(0, 1 / np.sqrt(kappa), N)
        W = np.zeros(N)
        cdot = a / tau
        for i in range(steps):
            c = cdot * i * dt
            W += -kappa * (x - c) * cdot * dt
            x += -kappa * (x - c) * dt + np.sqrt(2 * dt) * rng.normal(size=N)
        ex = a ** 2 * (1 - (1 - np.exp(-kappa * tau)) / (kappa * tau))
        print('MC tau=20 dt=%.3f: tau<W> = %.4f +- %.4f  (closed form %.4f)' % (dt, tau * W.mean(), tau * W.std() / np.sqrt(N), ex))
        fails += abs(tau * W.mean() - ex) > 5 * tau * W.std() / np.sqrt(N) + 0.02
    # friction metric: d_sV = -kappa a (x - s a); Cov(x0, xt) = e^{-kappa t}/kappa
    g = quad(lambda t: (kappa * a) ** 2 * np.exp(-kappa * t) / kappa, 0, np.inf)[0]
    L2 = g  # linear schedule, constant g: L^2 = g
    lim = a ** 2
    claim_eq = 0.5 * L2
    claim_lb = kappa / 4 * a ** 2
    print('friction metric g = %.6f -> L^2 = %.6f; observed lim tau*Sigma = %.6f; paper: L^2/2 = %.4f, kappa W2^2/4 = %.4f' % (g, L2, lim, claim_eq, claim_lb))
    print('   paper equality lim = L^2/2 holds?', abs(lim - claim_eq) < 1e-9, '; paper bound lim >= kappa W2^2/4 holds?', lim >= claim_lb - 1e-12)
    if kappa == 1.0:
        fails += not (lim >= claim_lb)       # control: claim holds at small kappa
    else:
        fails += (lim >= claim_lb)           # counterexample expected
    fails += abs(lim - L2) > 1e-9            # oracle 3 consistent with oracle 1
# OBL-011 Jarzynski
TrA, TrB, k0, k1, tau = 2.0, 5.0, 1.0, 3.0, 1.0
for dt in [2e-3, 1e-3]:
    N = 100000
    steps = int(tau / dt)
    x = rng.normal(0, 1 / np.sqrt(k0), N)
    W = np.zeros(N)
    # V_s = -log Tr_s - 0.5 log(k_s/2pi) + k_s x^2/2 with Tr_s, k_s linear in s=t/tau
    for i in range(steps):
        s = i * dt / tau
        Tr, k = TrA + (TrB - TrA) * s, k0 + (k1 - k0) * s
        dV = (-(TrB - TrA) / Tr - 0.5 * (k1 - k0) / k + 0.5 * (k1 - k0) * x ** 2) / tau
        W += dV * dt
        x += -k * x * dt + np.sqrt(2 * dt) * rng.normal(size=N)
    est = np.exp(-W).mean()
    err = np.exp(-W).std() / np.sqrt(N)
    print('Jarzynski dt=%.0e: E[e^-W] = %.4f +- %.4f ; Tr_B/Tr_A = %.4f ; mutated Tr_A/Tr_B = %.4f' % (dt, est, err, TrB / TrA, TrA / TrB))
    fails += abs(est - TrB / TrA) > 5 * err + 0.02
    fails += abs(est - TrA / TrB) < 5 * err + 0.02
print('failures:', fails)
sys.exit(int(fails))
