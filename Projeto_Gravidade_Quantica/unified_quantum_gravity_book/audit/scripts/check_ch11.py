"""Chapter 11 checks: QFI normalization, SLD vs Kubo-Mori, relative-entropy Hessian, Kac-Rice formula at k=2."""
import numpy as np
from scipy.linalg import logm, solve_continuous_lyapunov

rng = np.random.default_rng(7)
d = 3

def rand_state():
    A = rng.normal(size=(d, d)) + 1j*rng.normal(size=(d, d))
    r = A @ A.conj().T
    return r/np.trace(r).real

def herm_traceless():
    B = rng.normal(size=(d, d)) + 1j*rng.normal(size=(d, d))
    B = (B + B.conj().T)/2
    return B - np.trace(B)/d*np.eye(d)

rho, X = rand_state(), herm_traceless()
X *= 0.1
# SLD: X = (rho L + L rho)/2  <=>  rho L + L rho = 2X
L = solve_continuous_lyapunov(rho, 2*X)
qfi_a = 0.5*np.trace(L @ X).real                   # the chapter's first expression  (1/2) Tr(L d rho)
qfi_b = 0.5*np.trace(rho @ (L @ L + L @ L)).real   # the chapter's second expression (1/2) Tr(rho {L, L})
print(f"1. QFI definition: (1/2)Tr(L dρ) = {qfi_a:.6e},  (1/2)Tr(ρ{{L,L}}) = {qfi_b:.6e},  ratio = {qfi_b/qfi_a:.4f} (the chapter's '=' is off by 2)")

# Kubo-Mori metric via integral representation  int_0^inf Tr(X (s+rho)^-1 X (s+rho)^-1) ds
w, V = np.linalg.eigh(rho)
Xe = V.conj().T @ X @ V
def bkm_kernel(a, b):
    return 1/a if abs(a - b) < 1e-14 else (np.log(a) - np.log(b))/(a - b)
bkm = sum(abs(Xe[i, j])**2*bkm_kernel(w[i], w[j]) for i in range(d) for j in range(d)).real
sld = np.trace(L @ X).real     # = (1/2)Tr(rho{L,L}), standard QFI
# Hessian of relative entropy S(rho + t X || rho) at t=0 by finite differences
def S(t):
    r = rho + t*X
    return np.trace(r @ (logm(r) - logm(rho))).real
h = 1e-3
hess = (S(h) - 2*S(0) + S(-h))/h**2
print(f"2. d^2/dt^2 S(ρ+tX||ρ) = {hess:.6e};  Kubo-Mori g(X,X) = {bkm:.6e};  SLD-QFI Tr(L X) = {sld:.6e}")
print(f"   Hessian matches BKM (rel. err {abs(hess-bkm)/bkm:.1e}); differs from SLD-QFI by factor {bkm/sld:.4f}")
# commuting perturbation: BKM and SLD agree
Xc = V @ np.diag(rng.normal(size=d)) @ V.conj().T; Xc -= np.trace(Xc)/d*np.eye(d); Xc *= 0.1
Lc = solve_continuous_lyapunov(rho, 2*Xc); Xce = V.conj().T @ Xc @ V
bkm_c = sum(abs(Xce[i, j])**2*bkm_kernel(w[i], w[j]) for i in range(d) for j in range(d)).real
print(f"   commuting perturbation: BKM = {bkm_c:.6e}, SLD = {np.trace(Lc @ Xc).real:.6e}")

print("3. Kac-Rice formula of the chapter at k=2 vs exact count of critical points of x^T J x on S^{N-1}")
for N in (5, 10, 20):
    k = 2
    theta = 0.5*np.log(k - 1) - (k - 2)/(2*(k - 1))
    formula = 2*((k - 1)/np.pi)**(N/2)*np.sqrt(k - 1)*np.exp(N*theta)
    print(f"   N={N}: chapter formula = {formula:.3e};  exact = 2N = {2*N} (eigenvectors ±v_i of a generic symmetric J)")
