"""Chapter 7 checks (minimax extrinsic curvature). Each block prints a verdict with a negative control."""
import numpy as np

def op_and_frob(II):
    """II: array (k,k,N) of normal vectors II(e_i,e_j). Return sup_{|v|=1}|II(v,v)| (sampled) and Frobenius norm."""
    k = II.shape[0]
    best = 0.0
    rng = np.random.default_rng(0)
    for _ in range(20000):
        v = rng.normal(size=k); v /= np.linalg.norm(v)
        best = max(best, np.linalg.norm(np.einsum('i,j,ijn->n', v, v, II)))
    return best, np.sqrt((II**2).sum())

def second_fundamental_form(X, u, h=1e-4):
    """Numerical II of a parametrized k-surface X: R^k -> R^n at u, in an orthonormal tangent frame."""
    k = len(u)
    E = np.eye(k)
    d1 = np.array([(X(u + h*E[i]) - X(u - h*E[i]))/(2*h) for i in range(k)])
    d2 = np.array([[(X(u + h*E[i] + h*E[j]) - X(u + h*E[i] - h*E[j]) - X(u - h*E[i] + h*E[j]) + X(u - h*E[i] - h*E[j]))/(4*h*h)
                    for j in range(k)] for i in range(k)])
    Q, _ = np.linalg.qr(d1.T)             # orthonormal basis of tangent space (columns)
    P = np.eye(len(X(u))) - Q @ Q.T       # normal projector
    G = d1 @ d1.T
    L = np.linalg.cholesky(np.linalg.inv(G))  # change to orthonormal frame: e = L^T d
    II_coord = np.einsum('ijn,mn->ijm', d2, P)
    return np.einsum('ai,bj,ijn->abn', L.T, L.T, II_coord)

print("1. Calibrated 'isotropy' claim ||II||_op = ||II||_F/sqrt(c): holomorphic curve w=z^2 in C^2 = R^4")
X = lambda u: np.array([u[0], u[1], u[0]**2 - u[1]**2, 2*u[0]*u[1]])
II = second_fundamental_form(X, np.array([0.3, 0.2]))
op, fr = op_and_frob(II)
print(f"   op={op:.6f}  F={fr:.6f}  op/F={op/fr:.4f}  (claim 1/sqrt2={1/np.sqrt(2):.4f}; complex-curve value 1/2)")

print("2. Clifford torus (R/sqrt2)(cos u, sin u, cos v, sin v), R=1.7: ||II||_op should be sqrt2/R")
R = 1.7
X = lambda u: R/np.sqrt(2)*np.array([np.cos(u[0]), np.sin(u[0]), np.cos(u[1]), np.sin(u[1])])
op, _ = op_and_frob(second_fundamental_form(X, np.array([0.4, 1.1])))
print(f"   op={op:.6f}  sqrt2/R={np.sqrt(2)/R:.6f}  (negative control 1/R={1/R:.6f})")

print("3. Table k=1 rows: (R0/sqrt m) sum_j e^{i w s} e_j has curvature 1/R0, not 1/(sqrt m R0)")
for m in (2, 3, 4, 5, 6):
    R0 = 1.0
    amp = R0/np.sqrt(m); w = 1/(np.sqrt(m)*amp)   # unit speed: m amp^2 w^2 = 1
    kappa = np.sqrt(m)*amp*w**2
    kappa_thm = 1/(np.sqrt(m)*R0)                  # theorem's helix uses amplitude R0 per plane
    print(f"   m={m}: table-parametrization curvature={kappa:.6f}  table value={1/(np.sqrt(m)*R0):.6f}  theorem helix={kappa_thm:.6f}")

print("4. Sagitta: circle through chord ends (chord L) with sagitta d has curvature 8d/(L^2+4d^2) < 8d/L^2")
for L, d in [(1, 0.05), (1, 0.25), (1, 0.5)]:
    print(f"   L={L}, d={d}: circle={8*d/(L**2+4*d**2):.4f}  claimed lower bound={8*d/L**2:.4f}")

print("5. Cylinder r=R spanning two coaxial circles is not optimal for tall H: bulge r=R+a sin(pi z/H)")
R, H = 1.0, 10.0
z = np.linspace(0, H, 20001)
def maxcurv(a):
    r = R + a*np.sin(np.pi*z/H); rp = a*np.pi/H*np.cos(np.pi*z/H); rpp = -a*(np.pi/H)**2*np.sin(np.pi*z/H)
    k1 = np.abs(rpp)/(1 + rp**2)**1.5; k2 = 1/(r*np.sqrt(1 + rp**2))
    return np.max(np.maximum(k1, k2))
for a in (0.0, 0.5, 1.0, 2.0, 3.0):
    print(f"   a={a}: max principal curvature={maxcurv(a):.6f}  (cylinder: {1/R})")

print("6. Obstacle exclusion: a straight line tangent to a ball of radius rho touches it with II=0")
rho = 0.01
t = np.linspace(-1, 1, 200001); pts = np.stack([t, rho*np.ones_like(t)], 1)
print(f"   min distance to ball centre = {np.min(np.linalg.norm(pts, axis=1)):.6f} (= rho {rho}); obstacle curvature 1/rho={1/rho}, line curvature 0")

print("7. U-turn in a slab of R^3 needs no curvature bound in the slab direction: circle in the x-z plane")
s = np.linspace(0, np.pi, 1001); c = np.stack([np.sin(s), 0.3*np.ones_like(s), 1 - np.cos(s)], 1)
print(f"   y-range = {np.ptp(c[:,1]):.3f} (slab width may be 0+), start tangent (1,0,0), end tangent (-1,0,0), curvature 1")

print("8. Planar U-turn bound y-range >= 2/k: random curvature profiles with |kappa|<=1 turning by pi")
rng = np.random.default_rng(1)
worst = np.inf
for _ in range(2000):
    n = 4000; ds = 5*np.pi/n
    kap = rng.uniform(-1, 1, n); kap = np.clip(kap + 0.6, -1, 1)
    th = np.concatenate([[0], np.cumsum(kap*ds)])
    idx = np.argmax(th >= np.pi)
    if th[idx] < np.pi: continue
    y = np.concatenate([[0], np.cumsum(np.sin(th[:-1])*ds)])[:idx+1]
    worst = min(worst, np.ptp(y))
print(f"   min y-range over sampled U-turns = {worst:.4f} (bound 2.0)")
