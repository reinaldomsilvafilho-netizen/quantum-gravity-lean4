"""Shared helpers for the F-02 re-check scripts (chapters 2, 4, 5, 8, 10, 11).

claim(...) registers one numerical claim of the book together with its negative control:
the claim PASSES only if the oracle agrees with the book AND the mutated claim FAILS.
Rounding helpers: up(x) rounds a value that is used as an upper bound upwards, dn(x) rounds a
value used as a lower bound downwards (never to nearest).
"""
import math
import sys
import time

RESULTS = []      # (id, loc, status) with status in PASS / FAIL
EXPLORE = []      # (id, loc, text)
UNCHECKED = []    # (id, loc, reason)
T0 = time.time()


def up(x, d=3):
    """Round x UP to d significant digits (for upper bounds)."""
    if x == 0 or not math.isfinite(x):
        return repr(x)
    e = math.floor(math.log10(abs(x))) - d + 1
    f = 10.0 ** e
    return "%.*g" % (d, math.ceil(x / f - 1e-12) * f)


def dn(x, d=3):
    """Round x DOWN to d significant digits (for lower bounds)."""
    if x == 0 or not math.isfinite(x):
        return repr(x)
    e = math.floor(math.log10(abs(x))) - d + 1
    f = 10.0 ** e
    return "%.*g" % (d, math.floor(x / f + 1e-12) * f)


def claim(cid, loc, text, ok, info, ctrl_text, ctrl_fails, ctrl_info):
    ok = bool(ok)
    cf = bool(ctrl_fails)
    status = "PASS" if (ok and cf) else "FAIL"
    RESULTS.append((cid, loc, status, text))
    print("[%s] %s (%s) %s" % ("PASS" if ok else "FAIL", cid, loc, text))
    print("       oracle: %s" % info)
    print("[%s] %s control: %s" % ("CONTROL-OK" if cf else "CONTROL-WEAK", cid, ctrl_text))
    print("       %s" % ctrl_info)
    sys.stdout.flush()


def explore(cid, loc, text):
    EXPLORE.append((cid, loc, text))
    print("[EXPLORE] %s (%s) %s" % (cid, loc, text))
    sys.stdout.flush()


def unchecked(cid, loc, reason):
    UNCHECKED.append((cid, loc, reason))
    print("[UNCHECKED] %s (%s) %s" % (cid, loc, reason))
    sys.stdout.flush()


def finish(chapter):
    n_pass = sum(1 for r in RESULTS if r[2] == "PASS")
    n_fail = sum(1 for r in RESULTS if r[2] == "FAIL")
    print("=" * 70)
    print("Chapter %s: claims checked=%d, passed=%d, failed=%d, explore=%d, unchecked=%d, time=%.0fs"
          % (chapter, len(RESULTS), n_pass, n_fail, len(EXPLORE), len(UNCHECKED), time.time() - T0))
    for r in RESULTS:
        if r[2] == "FAIL":
            print("  FAILED: %s (%s) %s" % (r[0], r[1], r[3]))
    sys.exit(n_fail)

# ======================================================================
# Chapter 4 body.  Source: chap04_simplicial_waves_porous_transport.tex (3.0.0)
# ======================================================================
import numpy as np
import scipy.linalg as sla
from scipy.special import gammaln, rgamma, gamma as Gam
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss
import mpmath as mp
import sympy as sp

rng = np.random.default_rng(20261016)
mp.mp.dps = 30


# ---------------- 1D (m=2) and 2D (m=3) Beta kernel ----------------
def kern1(alpha):
    f = lambda y: float(Gam(alpha + 1) * rgamma(y + 1) * rgamma(alpha - y + 1))
    I = quad(f, 0, alpha, epsabs=1e-13, epsrel=1e-13)[0]
    return f, I


def sigma1(k, alpha):
    f, I = kern1(alpha)
    val = quad(lambda y: f(y) * (1 - np.cos(k * y)), 0, alpha, epsabs=1e-13, epsrel=1e-13, limit=400)[0]
    return val / (alpha ** 2 * I)


def sigma1_mp(k, alpha):
    alpha = mp.mpf(alpha)
    f = lambda y: mp.gamma(alpha + 1) / (mp.gamma(y + 1) * mp.gamma(alpha - y + 1))
    I = mp.quad(f, mp.linspace(0, alpha, 5))
    val = mp.quad(lambda y: f(y) * (1 - mp.cos(k * y)), mp.linspace(0, alpha, 9))
    return val / (alpha ** 2 * I)


def tri_nodes(alpha, N):
    x, w = leggauss(N)
    u = (x + 1) / 2; wu = w / 2
    U, V = np.meshgrid(u, u, indexing="ij")
    WU, WV = np.meshgrid(wu, wu, indexing="ij")
    y1 = alpha * U; y2 = alpha * (1 - U) * V
    J = alpha ** 2 * (1 - U)
    return y1.ravel(), y2.ravel(), (WU * WV * J).ravel()


def kernel2(alpha, N=120):
    y1, y2, w = tri_nodes(alpha, N)
    y3 = alpha - y1 - y2
    K = Gam(alpha + 1) * rgamma(y1 + 1) * rgamma(y2 + 1) * rgamma(y3 + 1)
    w = w * K
    return y1, y2, w / w.sum(), w.sum()


def section_symbol():
    # --- m=2: symbol range, large-k limit, small-k expansion (two independent quadratures: scipy vs mpmath)
    alpha = 1.7
    ks = np.concatenate([np.linspace(0, 60, 601), np.linspace(60, 600, 541)])
    sg = np.array([sigma1(k, alpha) for k in ks])
    smax = sg.max()
    s_mp = sigma1_mp(3.1, alpha)
    cross = abs(float(s_mp) - sigma1(3.1, alpha))
    f, I = kern1(alpha)
    M2 = quad(lambda y: f(y) * y ** 2, 0, alpha, epsabs=1e-13)[0] / I
    k0 = 1e-3
    small = sigma1(k0, alpha) / (0.5 * k0 ** 2 * M2 / alpha ** 2)
    big = np.mean(sg[-200:] * alpha ** 2)
    claim("C4.1", "chap04.tex:145-165 (Thm dispersion): symbol in [0, 2/alpha^2], long-wavelength M_2, large-k limit 1/alpha^2",
          "sigma(k)=(1/(alpha^2 I))int K(1-cos ky)dy lies in [0,2/alpha^2], sigma ~ k^2 M_2/(2 alpha^2) as k->0, and sigma -> 1/alpha^2 as k->infinity (m=2, alpha=1.7)",
          sg.min() >= -1e-12 and smax * alpha ** 2 <= 2 and abs(small - 1) < 1e-5 and abs(big - 1) < 2e-2 and cross < 1e-10,
          "scipy quad vs mpmath quad at k=3.1 agree to %s; scan of 1142 values of k in [0,600]: min sigma=%s, max alpha^2 sigma=%s (<=2); "
          "sigma/(k^2 M_2/(2 alpha^2)) at k=1e-3 equals %s; mean alpha^2 sigma over k in the last 200 samples = %s"
          % (up(cross, 2), up(sg.min(), 2), up(smax * alpha ** 2, 5), up(small, 8), up(big, 4)),
          "the mutated bound alpha^2 sigma <= 1 (half the claimed range) and the limit 2/alpha^2 must fail",
          smax * alpha ** 2 > 1.0 and abs(big - 2) > 0.5,
          "max alpha^2 sigma = %s > 1; mean alpha^2 sigma = %s is not 2" % (dn(smax * alpha ** 2, 4), up(big, 4)))

    # --- m=3: second-moment matrix structure a Id + b 11^T, small-k expansion
    alpha = 2.3
    y1, y2, w, Itot = kernel2(alpha)
    Y = np.stack([y1, y2])
    M2m = (Y * w) @ Y.T
    a_ = M2m[0, 0] - M2m[0, 1]
    b_ = M2m[0, 1]
    sym = abs(M2m[0, 0] - M2m[1, 1])
    kvec = np.array([0.4e-2, -0.3e-2])
    sig = float(np.sum(w * (1 - np.cos(kvec[0] * y1 + kvec[1] * y2))) / alpha ** 2)
    quad_form = 0.5 * kvec @ M2m @ kvec / alpha ** 2
    # independent: self-normalised Monte Carlo from uniform proposals on the simplex, 20 batches -> standard errors
    nb, per = 20, 400_000
    est = []
    for _ in range(nb):
        u = rng.random((per, 2)) * alpha
        uu = u[u.sum(axis=1) <= alpha]
        dens = Gam(alpha + 1) * rgamma(uu[:, 0] + 1) * rgamma(uu[:, 1] + 1) * rgamma(alpha - uu.sum(axis=1) + 1)
        est.append(((uu * (dens / dens.sum())[:, None]).T @ uu))
    est = np.array(est)
    M2mc = est.mean(axis=0)
    se = est.std(axis=0, ddof=1) / np.sqrt(nb)
    mc_ok = bool((np.abs(M2mc - M2m) < 5 * se).all())
    mc_z = float((np.abs(M2mc - M2m) / se).max())
    # (R2) CORE MUTANT: the asymmetric weight 1/(Gamma(y1+1) Gamma(y2+2) Gamma(y3+1)) must destroy the S_{m-1} structure
    yy1, yy2, ww = tri_nodes(alpha, 120)
    yy3 = alpha - yy1 - yy2
    Kmut = Gam(alpha + 1) * rgamma(yy1 + 1) * rgamma(yy2 + 2) * rgamma(yy3 + 1)
    wm = ww * Kmut; wm = wm / wm.sum()
    Ym = np.stack([yy1, yy2]); M2mut = (Ym * wm) @ Ym.T
    mut_asym = abs(M2mut[0, 0] - M2mut[1, 1])
    # (R2) second dimension m = 4: M_2 is 3x3 with equal diagonal entries and equal off-diagonal entries (3D Duffy quadrature)
    al4 = 2.9
    xg, wg = leggauss(40); ug = (xg + 1) / 2; wug = wg / 2
    U_, V_, W_ = np.meshgrid(ug, ug, ug, indexing="ij")
    WU_, WV_, WW_ = np.meshgrid(wug, wug, wug, indexing="ij")
    z1 = al4 * U_; z2 = al4 * (1 - U_) * V_; z3 = al4 * (1 - U_) * (1 - V_) * W_
    jac = al4 ** 3 * (1 - U_) ** 2 * (1 - V_)
    z1, z2, z3, wq = z1.ravel(), z2.ravel(), z3.ravel(), (WU_ * WV_ * WW_ * jac).ravel()
    z4 = al4 - z1 - z2 - z3
    wq = wq * Gam(al4 + 1) * rgamma(z1 + 1) * rgamma(z2 + 1) * rgamma(z3 + 1) * rgamma(z4 + 1)
    wq = wq / wq.sum()
    Z3 = np.stack([z1, z2, z3]); M4 = (Z3 * wq) @ Z3.T
    dg = np.diag(M4); off = M4[np.triu_indices(3, 1)]
    spread4 = max(dg.max() - dg.min(), off.max() - off.min())
    claim("C4.2", "chap04.tex:145-165 (Thm dispersion): M_2(alpha) = a(alpha) Id + b(alpha) 11^T (m=3 and m=4)",
          "second-moment matrix of the normalised kernel has the form a Id + b 11^T (m=3: 2x2; m=4: 3x3) and sigma ~ (1/(2 alpha^2)) k^T M_2 k",
          sym < 1e-10 and abs(sig / quad_form - 1) < 1e-5 and mc_ok and spread4 < 1e-8 and abs(b_) > 0.1,
          "m=3 Gauss-Duffy 120x120 at alpha=2.3: M_2[0,0]-M_2[1,1]=%s, a=%s, b=%s; sigma(k)/(quadratic form) at |k|~5e-3 = %s; "
          "Monte Carlo (20 batches x 4e5 proposals) agrees with M_2 within %s standard errors (needs < 5); "
          "m=4 (3D Duffy 40^3, alpha=2.9): spread of the 3 diagonal entries and of the 3 off-diagonal entries = %s, M_2 diag %s off %s"
          % (up(sym, 2), up(a_, 6), up(b_, 6), up(sig / quad_form, 8), up(mc_z, 3), up(spread4, 2), up(dg.mean(), 6), up(off.mean(), 6)),
          "CORE MUTANTS: (i) the asymmetric weight 1/(G(y1+1)G(y2+2)G(y3+1)) must give M_2[0,0] != M_2[1,1]; (ii) the claim 'b(alpha) = 0' must fail",
          mut_asym > 1e-2 and abs(b_) > 0.1,
          "mutated-kernel asymmetry |M2[0,0]-M2[1,1]| = %s; b(alpha) = %s" % (dn(mut_asym, 3), dn(abs(b_), 4)))

    # lattice multinomial remark: small-k limit S^2/(2 m^2) + (Q - S^2/m)/(2 m alpha), integer alpha, m=3
    mm, al = 3, 4
    kv = np.array([2.0e-3, -1.1e-3, 0.7e-3])      # k1,k2,k3 with k_m included
    z = np.mean(np.exp(1j * kv))
    exact = (1 - (z ** al).real) / al ** 2
    S = kv.sum(); Q = (kv ** 2).sum()
    formula = S ** 2 / (2 * mm ** 2) + (Q - S ** 2 / mm) / (2 * mm * al)
    wrong = S ** 2 / (2 * mm ** 2) + (Q - S ** 2 / mm) / (2 * al)
    Ssym, Qsym, msym, asym_ = sp.symbols("S Q m alpha", positive=True)
    red = sp.simplify((Ssym ** 2 / (2 * msym ** 2) + (Qsym - Ssym ** 2 / msym) / (2 * msym * asym_)).subs(Ssym, 0))
    claim("C4.3", "chap04.tex:160 (Thm dispersion, lattice remark)",
          "lattice multinomial: sigma -> S^2/(2m^2) + (Q - S^2/m)/(2 m alpha); with S=0 it equals Q/(2 m alpha)",
          abs(exact / formula - 1) < 1e-3 and sp.simplify(red - Qsym / (2 * msym * asym_)) == 0,
          "exact lattice symbol (1/alpha^2)(1-Re((1/m sum e^{ik_j})^alpha)) at |k|~2e-3 (m=3, alpha=4): %s vs formula %s; sympy S=0 reduction -> %s"
          % (up(exact, 6), up(formula, 6), red),
          "dropping the factor 1/m in the second term must disagree",
          abs(wrong / exact - 1) > 0.1, "mutated formula %s vs exact %s" % (up(wrong, 5), up(exact, 5)))
    return alpha


# ---------------- NLSE ----------------
def section_nlse():
    N = 64
    Lx = 2 * np.pi
    x = np.arange(N) * Lx / N
    kk = 2 * np.pi * np.fft.fftfreq(N, d=Lx / N)
    alpha = 1.7
    # symbol from the 1D Beta kernel (even, bounded)
    cache = {}
    def sg(k):
        k = abs(k)
        if k not in cache:
            cache[k] = sigma1(k, alpha)
        return cache[k]
    sigma = np.array([sg(round(k, 12)) for k in kk])
    hbar, M, kappa, p = 1.0, 1.0, 0.8, 1
    V = 0.3 * np.cos(x)

    def rhs(psi):
        kin = np.fft.ifft(sigma * np.fft.fft(psi))
        return (-1j / hbar) * ((hbar ** 2 / (2 * M)) * kin + V * psi - kappa * np.abs(psi) ** (2 * p) * psi)

    def energy(psi, mutated=False):
        ph = np.fft.fft(psi) / N
        ekin = hbar ** 2 / (2 * M) * Lx * np.sum(sigma * np.abs(ph) ** 2)
        epot = np.sum(V * np.abs(psi) ** 2) * Lx / N
        eint = np.sum(np.abs(psi) ** (2 * p + 2)) * Lx / N
        return ekin + epot - (kappa if mutated else kappa / (p + 1)) * eint

    psi = (0.6 + 0.2 * np.cos(2 * x) + 0.1j * np.sin(3 * x)).astype(complex)
    mass0 = np.sum(np.abs(psi) ** 2) * Lx / N
    e0 = energy(psi); em0 = energy(psi, True)
    dt = 2e-3
    dm = de = dem = 0.0
    for step in range(1500):
        k1 = rhs(psi); k2 = rhs(psi + dt / 2 * k1); k3 = rhs(psi + dt / 2 * k2); k4 = rhs(psi + dt * k3)
        psi = psi + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if step % 50 == 0:
            dm = max(dm, abs(np.sum(np.abs(psi) ** 2) * Lx / N - mass0))
            de = max(de, abs(energy(psi) - e0))
            dem = max(dem, abs(energy(psi, True) - em0))
    claim("C4.4", "chap04.tex:172-195 (Thm nlse_conservation)",
          "mass and the energy E = (hbar^2/2M) int sigma|psi^|^2 + int V|psi|^2 - kappa/(p+1) int |psi|^{2p+2} are conserved by the NLSE with the Beta symbol",
          dm < 1e-9 and de < 1e-8,
          "RK4 dt=2e-3, T=3, 64-point periodic grid, symbol sigma_alpha=1.7 from quadrature, V=0.3 cos x, kappa=0.8, p=1: max |dN|=%s, max |dE|=%s"
          % (up(dm, 2), up(de, 2)),
          "the energy with kappa instead of kappa/(p+1) in the interaction term must drift",
          dem > 1e-4, "mutated energy drift = %s" % dn(dem, 2))

    # modulational instability: Jacobian of the full nonlinear RHS at the plane wave
    N2 = 8
    kk2 = 2 * np.pi * np.fft.fftfreq(N2, d=2 * np.pi / N2)       # integer wavenumbers
    sig2 = np.array([sg(abs(float(k))) for k in kk2])
    rho, kap, pp = 1.3, 0.03, 2
    mu0 = -kap * rho ** pp

    def F(phi_ri):
        phi = phi_ri[:N2] + 1j * phi_ri[N2:]
        kin = np.fft.ifft(sig2 * np.fft.fft(phi))
        # rotating frame: i hbar phi_t = (hbar^2/2M) sigma phi - kappa|phi|^{2p} phi - mu0 phi
        d = (-1j / hbar) * ((hbar ** 2 / (2 * M)) * kin - kap * np.abs(phi) ** (2 * pp) * phi - mu0 * phi)
        return np.concatenate([d.real, d.imag])
    x0 = np.concatenate([np.full(N2, np.sqrt(rho)), np.zeros(N2)])
    h = 1e-6
    Jm = np.zeros((2 * N2, 2 * N2))
    for i in range(2 * N2):
        e = np.zeros(2 * N2); e[i] = h
        Jm[:, i] = (F(x0 + e) - F(x0 - e)) / (2 * h)
    lam = np.linalg.eigvals(Jm)
    lam2 = np.sort(np.real(lam ** 2))
    eps = hbar ** 2 * sig2 / (2 * M)
    c_ = kap * pp * rho ** pp
    Om2 = eps * (eps - 2 * c_)            # hbar^2 Omega^2 with hbar = 1 ; lambda^2 = -Omega^2
    pred = np.sort(np.concatenate([-Om2, -Om2]))
    bad = np.sort(np.concatenate([-eps * (eps - c_), -eps * (eps - c_)]))
    # (R2) unstable set and maximal rate taken from the EIGENVALUES of the Jacobian, not from the Omega^2 formula:
    #  (i) sweep rho: the number of eigenvalues with Re>0 equals the number of modes with 0 < sigma < thresh(rho);
    #  (ii) sweep the period Lx (continuous set of wavenumbers): sup of Re(eigenvalue) is kappa p rho^p (from below).
    def jac_eigs(rho_, Lx_, N_=8):
        kk_ = 2 * np.pi * np.fft.fftfreq(N_, d=Lx_ / N_)
        sg_ = np.array([sg(abs(float(k))) for k in kk_])
        mu_ = -kap * rho_ ** pp

        def F_(v):
            phi = v[:N_] + 1j * v[N_:]
            kin = np.fft.ifft(sg_ * np.fft.fft(phi))
            d_ = (-1j / hbar) * ((hbar ** 2 / (2 * M)) * kin - kap * np.abs(phi) ** (2 * pp) * phi - mu_ * phi)
            return np.concatenate([d_.real, d_.imag])
        x0_ = np.concatenate([np.full(N_, np.sqrt(rho_)), np.zeros(N_)])
        J_ = np.zeros((2 * N_, 2 * N_))
        for i in range(2 * N_):
            e = np.zeros(2 * N_); e[i] = 1e-6
            J_[:, i] = (F_(x0_ + e) - F_(x0_ - e)) / 2e-6
        return np.linalg.eigvals(J_), sg_
    count_ok = True
    counts = []
    for rho_ in (0.6, 1.0, 1.6, 2.4, 3.5, 5.0):
        ev, sg_ = jac_eigs(rho_, 2 * np.pi)
        n_pos = int((ev.real > 1e-6).sum())
        thr_ = 4 * M * kap * pp * rho_ ** pp / hbar ** 2
        n_pred = int(((sg_ > 1e-12) & (sg_ < thr_)).sum())
        counts.append((rho_, n_pos, n_pred))
        count_ok &= (n_pos == n_pred)
    gmax_J = 0.0
    for Lx_ in np.linspace(2.0, 40.0, 77):
        ev, _ = jac_eigs(rho, Lx_)
        gmax_J = max(gmax_J, float(ev.real.max()))
    gmax_ok = (gmax_J <= c_ * (1 + 1e-6)) and (gmax_J >= 0.97 * c_)
    nontrivial = min(c[1] for c in counts) == 0 and max(c[1] for c in counts) >= 3
    claim("C4.5", "chap04.tex:219-240 (Thm modulational_instability)",
          "hbar^2 Omega^2 = eps (eps - 2 kappa p rho^p), eps = hbar^2 sigma/(2M); unstable iff 0 < sigma < 4 M kappa p rho^p/hbar^2; gamma_max = kappa p rho^p/hbar",
          np.max(np.abs(lam2 - pred)) < 1e-6 and count_ok and nontrivial and gmax_ok,
          "finite-difference Jacobian of the full nonlinear RHS (8 modes, p=2, kappa=0.03, rho=1.3; sigma values %s): eigenvalue lambda^2 vs -Omega^2 max difference %s; "
          "(rho, #eigenvalues with Re>0, #modes with 0<sigma<thresh) over a rho sweep: %s; sup of Re(eigenvalue) over 77 periods Lx in [2,40]: %s vs kappa p rho^p = %s"
          % (str([up(v_, 3) for v_ in sig2]), up(np.max(np.abs(lam2 - pred)), 2), counts, up(gmax_J, 6), up(c_, 6)),
          "using 2 kappa p rho^p -> kappa p rho^p in the bracket must disagree with the Jacobian, and a mutated maximal rate 1.5 kappa p rho^p must be rejected",
          np.max(np.abs(lam2 - bad)) > 1e-3 and not (gmax_J >= 1.5 * c_),
          "mutated prediction differs by %s; sup Re(lambda) = %s < 1.5 kappa p rho^p = %s" % (dn(np.max(np.abs(lam2 - bad)), 2), up(gmax_J, 5), up(1.5 * c_, 5)))


# ---------------- Mittag-Leffler and MSD ----------------
def ml(beta, z, dps=80, terms=400):
    with mp.workdps(dps):
        z = mp.mpf(z)
        return sum(z ** n / mp.gamma(beta * n + 1) for n in range(terms))


def section_ml():
    mp.mp.dps = 40
    # classical special cases
    e1 = abs(ml(1, mp.mpf(-2.3)) - mp.e ** (-2.3))
    z = mp.mpf("1.9")
    e2 = abs(ml(2, -z ** 2) - mp.cos(z))
    x = mp.mpf("1.4")
    e3 = abs(ml(mp.mpf(1) / 2, -x) - mp.e ** (x ** 2) * mp.erfc(x))
    # Laplace inversion of s^{beta-1}/(s^beta + a)
    beta, a, t = mp.mpf("0.6"), mp.mpf("1.3"), mp.mpf("1.7")
    inv = mp.invertlaplace(lambda s: s ** (beta - 1) / (s ** beta + a), t, method="talbot")
    ser = ml(beta, -a * t ** beta)
    # Caputo derivative of u(t)=E_beta(-a t^beta) equals -a u(t)
    def du(tau):
        return sum(n * (-a) ** n * tau ** (beta * n - 1) * beta / mp.gamma(beta * n + 1) for n in range(1, 160))
    # Caputo derivative via substitution tau = t(1-w^{1/(1-beta)}) to remove the singular kernel
    cap = mp.quad(lambda tau: (t - tau) ** (-beta) * du(tau), [0, t / 2, t]) / mp.gamma(1 - beta)
    ode_err = abs(cap + a * ser)
    # asymptotics E_beta(-x) ~ 1/(Gamma(1-beta) x)
    xx = mp.mpf(30)
    E30 = ml(beta, -xx, dps=500, terms=4000)
    asym3 = sum((-1) ** (k + 1) * xx ** (-k) / mp.gamma(1 - beta * k) for k in (1, 2, 3))
    asym_ratio = E30 / asym3
    asym_lead = E30 * mp.gamma(1 - beta) * xx
    claim("C4.6", "chap04.tex:274-290 (Thm frequency_closed_form)",
          "E_beta(-a t^beta) is the inverse Laplace transform of s^{beta-1}/(s^beta+a), solves the Caputo equation D^beta u = -a u, "
          "and E_beta(-x) ~ 1/(Gamma(1-beta) x) (atom decaying like t^{-beta})",
          e1 < 1e-30 and e2 < 1e-30 and e3 < 1e-25 and abs(inv - ser) < 1e-12 and ode_err < 1e-6 and abs(asym_ratio - 1) < 1e-4 and abs(asym_lead - 1) < 5e-2,
          "series vs closed forms E_1=exp, E_2(-z^2)=cos z, E_{1/2}(-x)=e^{x^2}erfc x: errors %s, %s, %s; Talbot inversion vs series: %s; "
          "Caputo integral of the termwise derivative + a u = %s; at x=30: E / (3-term asymptotic series) = %s, x Gamma(1-beta) E = %s"
          % (mp.nstr(e1, 2), mp.nstr(e2, 2), mp.nstr(e3, 2), mp.nstr(abs(inv - ser), 2), mp.nstr(ode_err, 2), mp.nstr(asym_ratio, 8), mp.nstr(asym_lead, 5)),
          "the exponential e^{-a t^beta} (wrong propagator) must differ from the inverse Laplace transform",
          abs(mp.e ** (-a * t ** beta) - inv) > 1e-2,
          "difference %s" % mp.nstr(abs(mp.e ** (-a * t ** beta) - inv), 3))

    # MSD: second moment = -d^2/dk^2 E_beta(-K sigma(k) t^beta) at 0  = K t^beta M2/(alpha^2 Gamma(beta+1))
    alpha = mp.mpf("1.7")
    Kd, beta, tt = mp.mpf("0.9"), mp.mpf("0.7"), mp.mpf("2.2")
    f = lambda y: mp.gamma(alpha + 1) / (mp.gamma(y + 1) * mp.gamma(alpha - y + 1))
    I = mp.quad(f, mp.linspace(0, alpha, 5))
    M2 = mp.quad(lambda y: f(y) * y ** 2, mp.linspace(0, alpha, 5)) / I
    sig = lambda k: mp.quad(lambda y: f(y) * (1 - mp.cos(k * y)), mp.linspace(0, alpha, 9)) / (alpha ** 2 * I)
    g = lambda k: ml(beta, -Kd * sig(k) * tt ** beta, dps=30, terms=80)
    h = mp.mpf("1e-3")
    d2 = (g(h) - 2 * g(0) + g(-h)) / h ** 2
    msd_num = -d2
    msd_formula = Kd * tt ** beta * M2 / (alpha ** 2 * mp.gamma(beta + 1))
    d1 = (g(h) - g(-h)) / (2 * h)
    msd_wrong = Kd * tt ** beta * M2 / (alpha ** 2 * mp.gamma(beta + 1) * 2)
    msd_noG = Kd * tt ** beta * M2 / alpha ** 2                      # the mutant without Gamma(beta+1)
    claim("C4.7", "chap04.tex:297-325 (Thm msd)",
          "<x> = 0 and <x x^T>(t) = K t^beta M_2/(alpha^2 Gamma(beta+1)) exactly (m=2, alpha=1.7, beta=0.7, K=0.9, t=2.2)",
          abs(msd_num - msd_formula) / msd_formula < 1e-5 and abs(d1) < 1e-15,
          "second central difference (h=1e-3, mpmath, 30 digits) of E_beta(-K sigma(k) t^beta) with sigma from quadrature: %s vs formula %s; first derivative at 0: %s"
          % (mp.nstr(msd_num, 10), mp.nstr(msd_formula, 10), mp.nstr(d1, 2)),
          "a formula missing Gamma(beta+1) or with an extra factor 1/2 must disagree",
          abs(msd_wrong - msd_num) / msd_num > 0.3 and abs(msd_noG - msd_num) / msd_num > 0.05,
          "mutated values: factor 1/2 -> %s ; without Gamma(beta+1) -> %s (numerical %s)" % (mp.nstr(msd_wrong, 8), mp.nstr(msd_noG, 8), mp.nstr(msd_num, 8)))


def section_misc():
    # remark on energy minimisation at fixed mass, psi_w = w^{-d/2} phi(x/w).  (R2) computed numerically with the symbol of C4.1:
    #  (a) mass independent of w;  (b) int |psi_w|^{2p+2} = w^{-dp} int |phi|^{2p+2};  (c) (hbar^2/2M) int sigma |psi^_w|^2 <= hbar^2 N/(M alpha^2).
    #  Space-side quantities by quadrature in x; the kinetic term from the FFT of the SAMPLED psi_w and the symbol sigma (d = 1, m = 2, alpha = 1.7).
    d_, p_, al_ = 1, 2, 1.7
    xg_, wg_ = leggauss(800)
    yq = (xg_ + 1) / 2 * al_; wq_ = wg_ / 2 * al_
    fq = Gam(al_ + 1) * rgamma(yq + 1) * rgamma(al_ - yq + 1)
    Iq = (wq_ * fq).sum()

    def sigma_vec(k):
        return ((wq_ * fq)[None, :] * (1 - np.cos(np.outer(k, yq)))).sum(axis=1) / (al_ ** 2 * Iq)
    cross_s = max(abs(float(sigma_vec(np.array([kk]))[0]) - sigma1(kk, al_)) for kk in (0.7, 3.1, 25.0, 90.0))
    L_, Ng = 80.0, 2 ** 14
    xs = (np.arange(Ng) - Ng // 2) * (L_ / Ng)
    kf = 2 * np.pi * np.fft.fftfreq(Ng, d=L_ / Ng)
    sgf = np.concatenate([sigma_vec(kf[i:i + 2048]) for i in range(0, Ng, 2048)])
    phi = lambda x: np.pi ** (-0.25) * np.exp(-x ** 2 / 2)            # normalised: int |phi|^2 = 1
    mass, ints, kin = [], [], []
    ws = [0.1, 0.3, 1.0, 3.0]
    for w_ in ws:
        psi = w_ ** (-d_ / 2) * phi(xs / w_)
        dxg = L_ / Ng
        mass.append(float(np.sum(np.abs(psi) ** 2) * dxg))
        ints.append(float(np.sum(np.abs(psi) ** (2 * p_ + 2)) * dxg))
        ph = np.fft.fft(psi) * dxg                                    # continuous FT, up to phase
        kin.append(0.5 * float(np.sum(sgf * np.abs(ph) ** 2) * (kf[1] - kf[0]) / (2 * np.pi)))   # hbar = M = 1
    mass = np.array(mass); ints = np.array(ints); kin = np.array(kin)
    slope_fit = np.polyfit(np.log(ws), np.log(ints), 1)[0]
    ratio_i = ints * np.array(ws) ** (d_ * p_) / (ints[2] * 1.0 ** (d_ * p_))   # should be 1 for every w
    bound_k = mass / al_ ** 2                                          # hbar^2 N/(M alpha^2), hbar = M = 1
    dsym, psym = sp.symbols("d p", positive=True)
    expo = sp.simplify(-dsym * (psym + 1) + dsym)
    okC48 = (np.abs(mass - 1).max() < 1e-9 and np.abs(ratio_i - 1).max() < 1e-6 and abs(slope_fit + d_ * p_) < 1e-6
             and (kin <= bound_k + 1e-12).all() and cross_s < 1e-9)
    wrong_slope = -d_ * (p_ + 1)
    claim("C4.8", "chap04.tex:249-252 (Remark on energy at fixed mass)",
          "for psi_w = w^{-d/2} phi(x/w): mass independent of w, int |psi_w|^{2p+2} = w^{-d p} int|phi|^{2p+2}, kinetic term <= hbar^2 N/(M alpha^2)",
          okC48,
          "d=1, p=2, alpha=1.7, Gaussian phi, w in %s: masses %s; int|psi_w|^{6} * w^{dp} / (same at w=1) = %s; fitted log-log exponent %s vs -dp = %s; "
          "kinetic term (FFT of the sampled psi_w, symbol of C4.1; cross-check against scipy quad of the symbol %s) %s <= bound hbar^2 N/(M alpha^2) = %s; sympy exponent -d(p+1)+d = %s"
          % (ws, [up(m_, 9) for m_ in mass], [up(r_, 9) for r_ in ratio_i], up(slope_fit, 9), -d_ * p_, up(cross_s, 2),
             [up(k_, 5) for k_ in kin], [up(b_, 5) for b_ in bound_k], expo),
          "mutants: the exponent -d(p+1) (forgetting w^d) must disagree with the numerical slope; the bound 0.4 N/alpha^2 must be violated at w=0.1",
          abs(slope_fit - wrong_slope) > 0.5 and kin[0] > 0.4 * bound_k[0],
          "fitted slope %s vs mutated %s ; kinetic term at w=0.1 is %s > 0.4 * bound = %s" % (up(slope_fit, 6), wrong_slope, dn(kin[0], 5), up(0.4 * bound_k[0], 5)))
    unchecked("C4.U1", "chap04.tex:128-143 (Remark spectral_fractional)",
              "statements about Dirichlet spectral fractional Laplacians, domain H^2 cap H^1_0, Navier conditions and corner regularity r^{pi/omega} are cited functional-analysis facts (Grisvard, Servadei-Valdinoci); no numerical content")
    unchecked("C4.U2", "chap04.tex:240-255 (Conjecture on solitary waves, Nehari remark)",
              "existence/symmetry of solitary waves is a conjecture; the only checkable part (scaling of the interaction term) is C4.8")
    unchecked("C4.U3", "chap04.tex:105-118 (Prop self_adjoint_positive)",
              "positivity of -Delta follows from the non-negative symbol (checked in C4.1) and Plancherel; the 'vanishes iff u=0' step is a measure-theoretic argument")


if __name__ == "__main__":
    section_symbol()
    section_nlse()
    section_ml()
    section_misc()
    finish("4")
