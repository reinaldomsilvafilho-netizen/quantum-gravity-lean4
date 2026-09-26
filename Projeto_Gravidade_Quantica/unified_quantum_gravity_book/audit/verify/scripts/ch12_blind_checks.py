"""Camada 1 (cega) -- verificacoes numericas independentes do cap. 12.

Cada bloco compara a afirmacao do capitulo com um oraculo independente
(quadratura, forca bruta, identidade algebrica) e roda um controle negativo:
uma formula mutada tem de FALHAR no mesmo teste.

Uso: python ch12_blind_checks.py   (sai com codigo 1 se algum teste falhar)
"""
import math
import numpy as np
from scipy import integrate, special, optimize

FAIL = []


def check(name, ok, info=""):
    tag = "OK  " if ok else "FAIL"
    print(f"[{tag}] {name} {info}")
    if not ok:
        FAIL.append(name)


def neg(name, ok_mut, info=""):
    """Controle negativo: a mutacao deve ser rejeitada (ok_mut False)."""
    check("NEG " + name + " (mutacao rejeitada)", not ok_mut, info)


# ---------------------------------------------------------------- 1. d_s closed form
def P_quad(tau, lp=1.0):
    # P = (1/(2pi)^4) * 2 pi^2 * int k^3 exp(-tau(k^2+lp^2 k^4)) dk
    f = lambda k: k**3 * math.exp(-tau * (k * k + lp * lp * k**4))
    kmax = 60.0 / math.sqrt(tau) if tau < 1 else 60.0
    val, _ = integrate.quad(f, 0, kmax, limit=500, epsabs=0, epsrel=1e-12)
    return 2 * math.pi**2 / (2 * math.pi) ** 4 * val


def P_closed(tau, lp=1.0):
    z = math.sqrt(tau) / (2 * lp)
    g = math.sqrt(math.pi) * z * float(special.erfcx(z))  # erfcx = e^{z^2} erfc z
    return (1 - g) / (32 * math.pi**2 * lp**2 * tau)


def ds_closed(tau, lp=1.0, mut=None):
    z = math.sqrt(tau) / (2 * lp)
    g = math.sqrt(math.pi) * z * float(special.erfcx(z))
    if mut == "sign":
        return 1 + tau / (2 * lp**2) + 1 / (1 - g)
    if mut == "factor":
        return 1 - tau / (4 * lp**2) + 1 / (1 - g)
    return 1 - tau / (2 * lp**2) + 1 / (1 - g)


def ds_numeric(tau):
    h = 1e-4
    return -2 * (math.log(P_quad(tau * math.exp(h))) - math.log(P_quad(tau * math.exp(-h)))) / (2 * h)


taus = np.logspace(-3, 2, 26)
errP = max(abs(P_closed(t) / P_quad(t) - 1) for t in taus)
check("1a P(tau) fechada vs quadratura, tau in [1e-3,1e2]", errP < 1e-8, f"max rel err={errP:.2e}")
errD = max(abs(ds_closed(t) - ds_numeric(t)) for t in taus)
check("1b d_s(tau) fechada vs derivada numerica da quadratura", errD < 1e-5, f"max abs err={errD:.2e}")
vals = [ds_closed(t) for t in np.logspace(-4, 3, 400)]
check("1c limites 2 (UV) e 4 (IR)", abs(ds_closed(1e-8) - 2) < 1e-3 and abs(ds_closed(1e6) - 4) < 1e-4,
      f"d_s(1e-8)={ds_closed(1e-8):.5f}, d_s(1e6)={ds_closed(1e6):.6f}; obs: d_s(1e3)={ds_closed(1e3):.4f} (aproximacao lenta, ~ -12 l_P^2/tau)")
check("1d monotonia de d_s em tau", all(np.diff(vals) > -1e-9))
for m in ("sign", "factor"):
    e = max(abs(ds_closed(t, mut=m) - ds_numeric(t)) for t in taus)
    neg(f"1e d_s mutado ({m})", e < 1e-5, f"err={e:.2e}")

# ---------------------------------------------------------------- 2. homogeneous d_s = m/alpha
def ds_homog(m, a, tau):
    def P(t):
        f = lambda k: k ** (m - 1) * math.exp(-t * k ** (2 * a))
        v, _ = integrate.quad(f, 0, np.inf, limit=400)
        return v
    h = 1e-4
    return -2 * (math.log(P(tau * math.exp(h))) - math.log(P(tau * math.exp(-h)))) / (2 * h)


okh, okm = True, True
for m in (1, 2, 3, 4, 5):
    for a in (0.5, 0.75, 1.0, 1.5, 2.0, 3.0):
        for tau in (0.01, 1.0, 50.0):
            d = ds_homog(m, a, tau)
            okh &= abs(d - m / a) < 1e-5
            okm &= abs(d - m / (2 * a)) < 1e-5
check("2a d_s = m/alpha para todo tau (quadratura)", okh)
neg("2b d_s = m/(2 alpha)", okm)

# constant C(m,alpha) = Vol(S^{m-1}) Gamma(m/2a)/(2a (2pi)^m)
m, a, tau = 4, 1.3, 0.7
vol = 2 * math.pi ** (m / 2) / math.gamma(m / 2)
Cform = vol * math.gamma(m / (2 * a)) / (2 * a * (2 * math.pi) ** m)
Pq = vol / (2 * math.pi) ** m * integrate.quad(lambda k: k ** (m - 1) * math.exp(-tau * k ** (2 * a)), 0, np.inf)[0]
check("2c constante C(m,alpha)", abs(Pq / (Cform * tau ** (-m / (2 * a))) - 1) < 1e-8)

# ---------------------------------------------------------------- 3. fractional Laplacian constant (1D)
def fraclap_quad(alpha, x0=0.3, const="4"):
    # f = exp(-x^2), m=1. Multiplier: (1/2pi) int |k|^{2a} fhat(k) e^{ikx} dk with fhat = sqrt(pi) e^{-k^2/4}
    mult = integrate.quad(lambda k: abs(k) ** (2 * alpha) * math.sqrt(math.pi) * math.exp(-k * k / 4)
                          * math.cos(k * x0), -np.inf, np.inf, limit=400)[0] / (2 * math.pi)
    base = 4.0 if const == "4" else 2.0
    C = base**alpha * math.gamma(0.5 + alpha) / (math.pi**0.5 * abs(math.gamma(-alpha)))
    f = lambda x: math.exp(-x * x)
    # symmetrised PV: int_0^inf (2f(x0)-f(x0+h)-f(x0-h))/h^{1+2a} dh
    g = lambda h: (2 * f(x0) - f(x0 + h) - f(x0 - h)) / h ** (1 + 2 * alpha)
    pv = integrate.quad(g, 0, 1, limit=400)[0] + integrate.quad(g, 1, np.inf, limit=400)[0]
    return mult, C * pv


ok4 = ok2 = True
for al in (0.25, 0.5, 0.75):
    a_, b_ = fraclap_quad(al)
    ok4 &= abs(a_ / b_ - 1) < 1e-6
    a_, b_ = fraclap_quad(al, const="2")
    ok2 &= abs(a_ / b_ - 1) < 1e-6
check("3a constante C_{m,alpha} (m=1) vs multiplicador de Fourier", ok4)
neg("3b constante com 2^alpha", ok2)

# ---------------------------------------------------------------- 4. barycentric Hessian
def logbin(x, t):
    return special.gammaln(x + 1) - np.sum(special.gammaln(np.asarray(t) + 1))


x, mm = 7.3, 4
ts = np.full(mm, x / mm)
rng = np.random.default_rng(0)
v = rng.normal(size=mm); v -= v.mean()
h = 1e-3
second = (logbin(x, ts + h * v) - 2 * logbin(x, ts) + logbin(x, ts - h * v)) / h**2
Qclaim = special.polygamma(1, x / mm + 1) / 2 * np.sum(v**2)
check("4a Q(v) = psi'(x/m+1)/2 |v|^2 (diferenca finita)", abs(-second / 2 - Qclaim) / Qclaim < 1e-5,
      f"{-second/2:.8f} vs {Qclaim:.8f}")
Qmut = special.digamma(x / mm + 1) / 2 * np.sum(v**2)
neg("4b Q com psi em vez de psi'", abs(-second / 2 - Qmut) / Qmut < 1e-5)
first = (logbin(x, ts + h * v) - logbin(x, ts - h * v)) / (2 * h)
check("4c termo linear nulo no plano soma-zero", abs(first) < 1e-8)
# Cartan
roots = np.array([np.eye(mm)[j] - np.eye(mm)[j + 1] for j in range(mm - 1)])
cartan = 2 * np.eye(mm - 1) - np.eye(mm - 1, k=1) - np.eye(mm - 1, k=-1)
check("4d Gram das raizes simples = matriz de Cartan A_{m-1}", np.allclose(roots @ roots.T, cartan))
c = rng.normal(size=mm - 1); vv = c @ roots
check("4e |v|^2 = c^T A c", abs(vv @ vv - c @ cartan @ c) < 1e-12)
neg("4f |v|^2 = c^T (2I) c", abs(vv @ vv - 2 * c @ c) < 1e-12)
# large-x: psi'(z+1) ~ 1/z
check("4g psi'(x/m+1) ~ m/x", abs(special.polygamma(1, 1e4 / 4 + 1) * 1e4 / 4 - 1) < 1e-3)

# ---------------------------------------------------------------- 5. ADM
# random symmetric K, metric gamma = I (orthonormal frame)
ok = True
for _ in range(100):
    A = rng.normal(size=(3, 3)); K = (A + A.T) / 2
    trK = np.trace(K); KK = np.sum(K * K)
    sig = K - trK / 3 * np.eye(3)
    ok &= abs((KK - trK**2) - (np.sum(sig * sig) - 2 / 3 * trK**2)) < 1e-10
    # momentum form: c=1: pi = K - trK I;  pi.pi - pi^2/2 == KK - K^2
    pi = K - trK * np.eye(3)
    ok &= abs((np.sum(pi * pi) - np.trace(pi) ** 2 / 2) - (KK - trK**2)) < 1e-10
check("5a identidades K_ijK^ij-K^2 = sigma^2-2K^2/3 e forma em pi", ok)
okm = True
for _ in range(20):
    A = rng.normal(size=(3, 3)); K = (A + A.T) / 2
    trK = np.trace(K); pi = K - trK * np.eye(3)
    okm &= abs((np.sum(pi * pi) - np.trace(pi) ** 2 / 3) - (np.sum(K * K) - trK**2)) < 1e-10
neg("5b forma em pi com pi^2/3", okm)

# e2 on cube [-1,1]^3
g = np.linspace(-1, 1, 81)
L1, L2, L3 = np.meshgrid(g, g, g, indexing="ij")
e2 = L1 * L2 + L2 * L3 + L3 * L1
check("5c e2 em [-a^2, 3a^2] (grade 81^3)", abs(e2.min() + 1) < 1e-12 and abs(e2.max() - 3) < 1e-12,
      f"min={e2.min()}, max={e2.max()}")
R = -2 * e2  # R - 2Lambda - 16 pi G rho
check("5d R-2L-16piGrho em [-6a^2, 2a^2]", abs(R.min() + 6) < 1e-12 and abs(R.max() - 2) < 1e-12)
neg("5e intervalo mutado [-6a^2, 6a^2] seria atingido", abs(R.max() - 6) < 1e-12)
# minimum also attained at non-vertex points: (1,-1,t)
tt = np.linspace(-1, 1, 11)
e2edge = 1 * (-1) + (-1) * tt + tt * 1
check("5f minimo -a^2 atingido em toda a aresta (a,-a,t) (nao so em vertices)", np.allclose(e2edge, -1))
KKmax = (L1**2 + L2**2 + L3**2).max()
check("5g K_ijK^ij <= 3a^2", abs(KKmax - 3) < 1e-12)
sig2 = (L1**2 + L2**2 + L3**2) - (L1 + L2 + L3) ** 2 / 3
print(f"     obs: max sigma_ij sigma^ij no cubo = {sig2.max():.4f} (= 8/3 a^2)")

# ---------------------------------------------------------------- 6. Mandelstam SU(2)
def haar_su(n):
    Z = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / math.sqrt(2)
    Q, Rr = np.linalg.qr(Z)
    Q = Q @ np.diag(np.diag(Rr) / abs(np.diag(Rr)))
    return Q / np.linalg.det(Q) ** (1 / n)


ok2, ok3 = True, True
for _ in range(50):
    A, B = haar_su(2), haar_su(2)
    ok2 &= abs(np.trace(A) * np.trace(B) - np.trace(A @ B) - np.trace(A @ np.linalg.inv(B))) < 1e-10
    A, B = haar_su(3), haar_su(3)
    ok3 &= abs(np.trace(A) * np.trace(B) - np.trace(A @ B) - np.trace(A @ np.linalg.inv(B))) < 1e-10
check("6a identidade de Mandelstam W_a W_b = W_ab + W_ab^-1 em SU(2)", ok2)
neg("6b mesma identidade em SU(3)", ok3)

# ---------------------------------------------------------------- 7. Graphon Ollivier curvature, Euclidean metric
# W = 1 on I1xI2, I2xI1, I3xI4, I4xI3 (+eps); Ii = quarters of [0,1]
N = 4000
zs = (np.arange(N) + 0.5) / N
eps = 1e-3


def Wrow(x):
    q = min(int(x * 4), 3)
    zq = np.minimum((zs * 4).astype(int), 3)
    partner = {0: 1, 1: 0, 2: 3, 3: 2}[q]
    return np.where(zq == partner, 1.0, eps)


def W1_1d(p, q):
    return np.sum(np.abs(np.cumsum(p) - np.cumsum(q))) / N


def kappa(x, y, metric="euclid"):
    p = Wrow(x); p = p / p.sum()
    q = Wrow(y); q = q / q.sum()
    if metric == "euclid":
        return 1 - W1_1d(p, q) / abs(x - y)
    tv = 0.5 * np.sum(np.abs(p - q))
    return 1 - tv / 1.0


k_e = kappa(0.49, 0.51)
check("7a Ollivier com metrica euclidiana em [0,1]: kappa << -2 (sem cota -2)", k_e < -2, f"kappa={k_e:.2f}")
k_e2 = kappa(0.499, 0.501)
print(f"     obs: kappa(0.499,0.501)={k_e2:.1f} -> ilimitado inferiormente quando |x-y|->0")
k_d = kappa(0.49, 0.51, metric="discrete")
neg("7b com metrica discreta kappa < 0 (cap. 2 Obs. (a): kappa>=0)", k_d < 0, f"kappa_disc={k_d:.3f}")

# decay proposition: ODE with time-dependent kappa <= -c
c0 = 0.7
kap_t = lambda t: -c0 - 0.5 * (1 + math.sin(3 * t))
sol = integrate.solve_ivp(lambda t, w: 2 * kap_t(t) * w, (0, 5), [0.8], dense_output=True, rtol=1e-10, atol=1e-14)
tt = np.linspace(0, 5, 200)
check("7c W(t) <= W0 e^{-2ct}", np.all(sol.sol(tt)[0] <= 0.8 * np.exp(-2 * c0 * tt) + 1e-12))
neg("7d W(t) <= W0 e^{-4ct} (taxa dobrada)", np.all(sol.sol(tt)[0] <= 0.8 * np.exp(-4 * c0 * tt) + 1e-12))

# ---------------------------------------------------------------- 8. RT: hemisphere and two-interval counterexample to MCF conjecture
# geodesic curvature in H^2 (metric (dz^2+dx^2)/z^2, L=1) of curve (x(s),z(s)):
# k_g = z * k_E + n_x (Euclidean curvature, outward unit normal x-component) -> use formula k_g = z k_E + cos(theta)
def kg_circle(xc, R, th):
    # circle centred (xc,0) radius R; point (xc+R cos th, R sin th). Euclidean curvature 1/R, normal (cos th, sin th)
    z = R * math.sin(th)
    # conformal change g=e^{2phi} delta, phi=-ln z: k_g = e^{-phi}(k_E + d phi/dn) = z(1/R - n_z/z) sign conv.
    nz = math.sin(th)
    return z * (1 / R) - nz


okc = all(abs(kg_circle(0.0, 1.3, th)) < 1e-12 for th in np.linspace(0.1, 3.0, 30))
check("8a semicirculo centrado na fronteira tem k_g = 0 em H^2", okc)


def kg_circle_offset(zc, R, th):
    # circle centred at (0, zc) (not on the boundary): n = (cos th, sin th)
    z = zc + R * math.sin(th)
    return z / R - math.sin(th)


okn = all(abs(kg_circle_offset(0.4, 1.3, th)) < 1e-12 for th in np.linspace(0.1, 3.0, 30))
neg("8b circulo com centro fora da fronteira tambem geodesico", okn)

# two intervals [a1,b1],[a2,b2] in AdS3: regularized lengths (units L=1, cutoff eps cancels)
a1, b1, a2, b2 = 0.0, 1.0, 1.1, 2.1
Ldis = 2 * math.log(b1 - a1) + 2 * math.log(b2 - a2)
Lcon = 2 * math.log(b2 - a1) + 2 * math.log(a2 - b1)
check("8c par de intervalos: config. desconexa e estacionaria (k_g=0) mas NAO minima",
      Lcon < Ldis, f"L_dis-L_con = {Ldis-Lcon:.3f} > 0")
a1, b1, a2, b2 = 0.0, 1.0, 3.0, 4.0
Ldis = 2 * math.log(b1 - a1) + 2 * math.log(b2 - a2)
Lcon = 2 * math.log(b2 - a1) + 2 * math.log(a2 - b1)
neg("8d intervalos afastados: conexa menor (deveria ser a desconexa)", Lcon < Ldis)

# ---------------------------------------------------------------- 9. FG: g_(2) = C_2/L^2 with flat boundary
# flat boundary -> R^(0)=0 -> g_(2)=0.  C_2 = second derivative of relative entropy = Fisher info > 0.
def relent(r, s):
    er, Ur = np.linalg.eigh(r); es, Us = np.linalg.eigh(s)
    logr = Ur @ np.diag(np.log(er)) @ Ur.T; logs = Us @ np.diag(np.log(es)) @ Us.T
    return float(np.trace(r @ (logr - logs)))


sigma = np.diag([0.7, 0.3])
X = np.array([[0.1, 0.05], [0.05, -0.1]])
S = lambda lam: relent(sigma + lam * X, sigma)
hh = 1e-3
C2 = (S(hh) - 2 * S(0) + S(-hh)) / hh**2
check("9a C_2 = d^2 S(rho||sigma)/dlam^2 > 0 para perturbacao nao trivial", C2 > 1e-3, f"C2={C2:.4f}")
print("     => com fronteira plana (R^(0)=0) g_(2)=0, logo 'g_(2) = C_2/L^2' e falso.")
S0 = lambda lam: relent(sigma + lam * 0 * X, sigma)
C20 = (S0(hh) - 2 * S0(0) + S0(-hh)) / hh**2
neg("9b controle: perturbacao nula tambem daria C_2>0", C20 > 1e-3, f"C2={C20:.1e}")

# ---------------------------------------------------------------- 10. Airy
def airy_resid(s, kap=1.7, sig=0.9, V0=0.4, hb=0.8, p=1 / 3):
    beta = (kap**2 * sig / hb**2) ** p
    X = beta * (s + V0 / (kap * sig))
    ai, aip, _, _ = special.airy(X)
    psi2 = beta**2 * X * ai  # Ai'' = X Ai
    return -hb**2 / kap * psi2 + (V0 + kap * sig * s) * ai


rs = max(abs(airy_resid(s)) for s in np.linspace(-2, 2, 21))
check("10a solucao de Airy satisfaz a EDO", rs < 1e-12, f"resid={rs:.1e}")
rs2 = max(abs(airy_resid(s, p=0.5)) for s in np.linspace(-2, 2, 21))
neg("10b expoente 1/2 em vez de 1/3", rs2 < 1e-12)

# ---------------------------------------------------------------- 11. Phenomenology
me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
Q = (me + mmu + mtau) / (math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mtau)) ** 2
check("11a Koide leptons Q ~ 2/3", abs(Q - 2 / 3) < 1e-4, f"Q={Q:.6f}")
vv = np.sqrt([me, mmu, mtau]); ang = math.degrees(math.acos(vv.sum() / (math.sqrt(3) * np.linalg.norm(vv))))
check("11b angulo com (1,1,1) = 45 graus", abs(ang - 45) < 0.01, f"{ang:.4f}")
Qbad = (me + mmu + mtau) ** 0.5 / (me ** 0.5 + mmu ** 0.5 + mtau ** 0.5)
neg("11c Q definido com raiz no numerador", abs(Qbad - 2 / 3) < 1e-3)
# a,b parametrisation: v = a(1,1,1) + b*sqrt2*(cos(th+2pi j/3)) -> |v2|^2 = 3 b^2 * ... check 6b^2 convention
a_, b_, th = 1.0, 1 / math.sqrt(2), 0.2
vb = np.array([a_ + 2 * b_ * math.cos(th + 2 * math.pi * j / 3) for j in range(3)])
check("11d v=a(1,1,1)+2b cos(.) : |v2|^2=6b^2, |v1|^2=3a^2, Q=2/3 se b/a=1/sqrt2",
      abs((vb**2).sum() / vb.sum() ** 2 - 2 / 3) < 1e-12)
aS = 0.1180
Qq = 2 / 3 * (1 + aS / math.sqrt(3))
check("11e Q_q = 2/3(1+alpha_s/sqrt3) = 0.7121", abs(Qq - 0.7121) < 1e-4, f"{Qq:.5f}")
def Qf(ms):
    return sum(ms) / sum(math.sqrt(m) for m in ms) ** 2
Qmsbar = Qf([0.619, 2.89, 171.7])   # MSbar at M_Z (Xing-Zhang-Zhou type values)
Qpole = Qf([1.67, 4.78, 172.5])     # pole masses (PDG)
check("11f Q_cbt MSbar(M_Z) ~ 0.72 e polo ~ 0.65", abs(Qmsbar - 0.72) < 0.01 and abs(Qpole - 0.65) < 0.01,
      f"MSbar={Qmsbar:.4f}, polo={Qpole:.4f}")
v_ew = 246.22
lam = (125.25 / v_ew) ** 2 / 2
check("11g Higgs: v/2=123.11 e Delta lambda ~ 0.0044", abs(v_ew / 2 - 123.11) < 0.01 and abs(lam - 0.125 - 0.0044) < 1e-4,
      f"dlam={lam-0.125:.5f}")
neg("11h convencao m_H = v sqrt(lambda) daria v/2 com lambda=1/8", abs(v_ew * math.sqrt(0.125) - 123.11) < 0.01)

# ---------------------------------------------------------------- 12. Observational numbers
c = 2.99792458e8; lP = 1.616255e-35; Mpc = 3.0857e22; H0 = 70e3 / Mpc
def D2(z):
    return c / H0 * integrate.quad(lambda x: (1 + x) / math.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, z)[0]
def Dc(z):
    return c / H0 * integrate.quad(lambda x: 1 / math.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, z)[0]
def dt(ell, xi, D, f1=10, f2=1e3):
    return 6 * math.pi**2 * xi * ell**2 * D * (f2**2 - f1**2) / c**3
res = {z: (dt(lP, 0.5, Dc(z)), dt(lP, 0.5, D2(z))) for z in (1, 3, 8)}
for z, (a_, b_) in res.items():
    print(f"     z={z}: Dt(comoving)={a_:.2e} s, Dt(D2)={b_:.2e} s")
check("12a Dt ~ 1e-62..1e-61 s (ordem)", all(-63 < math.log10(v) < -60 for p in res.values() for v in p))
# group velocity: numeric derivative
k0 = 1e3; lst = 1e-5; xi = 0.5
w = lambda k: c * k * math.sqrt(1 + xi * lst**2 * k**2)
vg = (w(k0 * (1 + 1e-6)) - w(k0 * (1 - 1e-6))) / (2e-6 * k0)
check("12b v_g = c(1+3/2 xi l^2 k^2)", abs((vg / c - 1) / (1.5 * xi * lst**2 * k0**2) - 1) < 1e-3)
neg("12c v_g = c(1+1/2 xi l^2 k^2)", abs((vg / c - 1) / (0.5 * xi * lst**2 * k0**2) - 1) < 1e-3)
ell_req = lP * math.sqrt(1e-4 / dt(lP, 0.5, D2(3)))
ell_req_c = lP * math.sqrt(1e-4 / dt(lP, 0.5, Dc(3)))
E = 1.97327e-7 / ell_req
check("12d l* para 1e-4 s em z=3 ~ 5e-7 m, ~0.4 eV", 3e-7 < ell_req < 8e-7 and 0.2 < E < 0.7,
      f"l*={ell_req:.2e} m (D2), {ell_req_c:.2e} m (comovel); E={E:.2f} eV")
kpiv = 0.05 / Mpc * 1.97327e-16  # GeV
MP = 1.220890e19; MPred = 2.435e18
at = (kpiv / MP) ** 2
check("12e k_pivot ~ 3e-40 GeV, |alpha_t| ~ 7e-118 (M_P nao reduzida)", abs(kpiv / 3.2e-40 - 1) < 0.05 and 5e-118 < at < 9e-118,
      f"k={kpiv:.2e} GeV, alpha_t={at:.1e}; com M_P reduzida: {(kpiv/MPred)**2:.1e}")
# ell = 4000 : k ~ ell / chi_*, chi_* ~ 14000 Mpc
at4000 = ((4000 / 14000) / Mpc * 1.97327e-16 / MP) ** 2
check("12f l=4000: |alpha_t| < 1e-115", at4000 < 1e-115, f"{at4000:.1e}")
# atom interferometry: Sr-87 lambda_dB
mSr = 86.909 * 1.66054e-27; hP = 6.62607e-34
for vel in (0.1, 1.0, 10.0):
    lam_dB = hP / (mSr * vel)
    print(f"     Sr v={vel} m/s: lambda_dB={lam_dB:.2e} m, lP/lambda={lP/lam_dB:.1e}")
check("12g lP/lambda_dB <~ 4e-26 para v <~ 10 m/s", lP / (hP / (mSr * 10.0)) < 5e-26)

# ---------------------------------------------------------------- 13. Sierpinski
dsS = 2 * math.log(5) / math.log(7)
check("13a d_s Sierpinski m=4 = 1.654", abs(dsS - 1.654) < 5e-4, f"{dsS:.4f}")
neg("13b com ln(m+2)", abs(2 * math.log(5) / math.log(6) - 1.654) < 5e-4)

# ---------------------------------------------------------------- 14. thin shell quadrature
M, kap = 1.0, 0.3
f = lambda r: kap**2 * r**2 - 1 + 2 * M / r
rmin = optimize.brentq(f, 2.5, 50) if f(2.5) < 0 else None
roots_c = np.roots([kap**2, 0, -1, 2 * M])
print(f"     obs: raizes do cubico k^2 r^3 - r + 2M: {np.round(roots_c, 4)}")
check("14a radicando * r e cubico (integral eliptica)", len(roots_c) == 3)
# r_min > 0 (ponto de retorno) existe sse 27 kappa^2 M^2 < 1
for (M_, k_) in ((1.0, 0.3), (1.0, 0.1)):
    rr = np.roots([k_**2, 0, -1, 2 * M_])
    pos = [r.real for r in rr if abs(r.imag) < 1e-12 and r.real > 0]
    print(f"     M={M_}, kappa={k_}: 27k^2M^2={27*k_**2*M_**2:.2f}, raizes reais positivas={np.round(pos,4)}")
check("14b sem r_min>0 quando 27 k^2 M^2 > 1", not [r for r in np.roots([0.09, 0, -1, 2]) if abs(r.imag) < 1e-12 and r.real > 0])
neg("14c controle: 27k^2M^2<1 tambem sem r_min", not [r for r in np.roots([0.01, 0, -1, 2]) if abs(r.imag) < 1e-12 and r.real > 0])

# ---------------------------------------------------------------- 15. product Dirac operator: 1 vs gamma_5 (grading)
# Euclidean 2D model: D_M(k) = s1 k1 + s2 k2, grading gamma = s3; finite part = mass m (1x1).
s1 = np.array([[0, 1], [1, 0]]); s2 = np.array([[0, -1j], [1j, 0]]); s3 = np.diag([1, -1])
kvec, mF = (0.8, -0.5), 0.6
DM = kvec[0] * s1 + kvec[1] * s2
kn = math.hypot(*kvec)
ev_g = np.sort(np.linalg.eigvalsh(DM + s3 * mF))       # D_M x 1 + gamma x D_F (Connes)
ev_1 = np.sort(np.linalg.eigvalsh(DM + np.eye(2) * mF)) # D_M x 1 + 1 x D_F (cap. 12)
check("15a com grading: espectro +-sqrt(k^2+m^2) (massa fisica)", np.allclose(ev_g, [-math.hypot(kn, mF), math.hypot(kn, mF)]),
      f"{np.round(ev_g,4)}")
neg("15b com identidade (cap. 12): espectro +-sqrt(k^2+m^2)", np.allclose(ev_1, [-math.hypot(kn, mF), math.hypot(kn, mF)]),
    f"{np.round(ev_1,4)} = +-|k| + m (deslocamento, sem gap de massa)")

print()
print("FALHAS:", FAIL if FAIL else "nenhuma")
raise SystemExit(1 if FAIL else 0)
