"""Chapter 10 counterexample: the claimed curvature-based Hessian and PAC-Bayes bounds fail.

Model: Gaussian linear regression y = x.theta + noise (sigma = 1). Its Fisher metric is the constant
matrix X^T X / N, so the regularized Fisher metric g = X^T X/N + lambda0 I is constant, all Christoffel
symbols vanish, and straight lines have zero covariant acceleration. Hence kappa*_info = 0 for any target
reachable by a straight segment (the condition number of g is the same everywhere, so the obstacle
O_sing = {cond > Lambda_max} is empty for Lambda_max > cond(g)).
"""
import numpy as np

rng = np.random.default_rng(0)
N, D, Ntest = 50, 200, 5000
X = rng.normal(size=(N, D)) / np.sqrt(D)
y = rng.choice([-1.0, 1.0], size=N)              # random labels: nothing to generalize
Xt = rng.normal(size=(Ntest, D)) / np.sqrt(D)
yt = rng.choice([-1.0, 1.0], size=Ntest)

theta_star = np.linalg.pinv(X) @ y               # interpolating least-squares solution
lam0 = 1e-3
g = X.T @ X / N + lam0*np.eye(D)                 # regularized Fisher metric (constant)

# straight path theta(s) = s * theta_star / |theta_star|_g : covariant acceleration = ordinary second derivative = 0
s = np.linspace(0, 1, 11)
path = s[:, None]*theta_star[None, :]
acc = np.diff(path, 2, axis=0)
print(f"max |second difference| along straight path = {np.abs(acc).max():.2e}  -> kappa*_info = 0")
print(f"cond(g) = {np.linalg.cond(g):.3e} (same at every theta, so no obstacle for Lambda_max above it)")

loss = lambda Xm, ym, th: np.minimum(1.0, (Xm @ th - ym)**2)   # loss clipped to [0,1]
train, test = loss(X, y, theta_star).mean(), loss(Xt, yt, theta_star).mean()
H = X.T @ X / N                                   # Hessian of the (unclipped) squared loss / 2
print(f"train loss = {train:.4f}, test loss = {test:.4f}, generalization gap = {test - train:.4f}")
delta = 0.05
bound_pac = np.sqrt((D*np.log(1 + 0.0) + np.log(2/delta))/(2*N))
print(f"claimed PAC-Bayes bound with kappa* = 0: {bound_pac:.4f}  (violated: {test - train > bound_pac})")
print(f"Tr(H) = {np.trace(H):.4f} > 0, claimed bound D*lambda_max*kappa* = 0  (violated: {np.trace(H) > 0})")
# negative control: with true labels from a linear teacher and N >> D the gap is small
Nb = 5000; Xb = rng.normal(size=(Nb, 20))/np.sqrt(20); tb = rng.normal(size=20)
yb = Xb @ tb + 0.1*rng.normal(size=Nb); thb = np.linalg.lstsq(Xb, yb, rcond=None)[0]
Xbt = rng.normal(size=(Ntest, 20))/np.sqrt(20); ybt = Xbt @ tb + 0.1*rng.normal(size=Ntest)
print(f"control (N>>D, true teacher): gap = {loss(Xbt, ybt, thb).mean() - loss(Xb, yb, thb).mean():.4f}")
