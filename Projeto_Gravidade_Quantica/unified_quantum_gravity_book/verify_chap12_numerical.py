"""
Verification Suite for Chapter 12: Emergent Spacetime, Holographic Entanglement, and Quantum Geometry
Author: Reinaldo Maia Silva-Filho

Every battery compares a closed-form statement of the chapter with an independent
computation (quadrature, finite differences, brute force), and includes a negative
control: a deliberately mutated formula that must FAIL the same check.
Runs standalone (python verify_chap12_numerical.py) or under pytest.
"""

import numpy as np
from scipy import integrate, optimize, special


def _close(a, b, rtol):
    return abs(a - b) <= rtol * max(abs(a), abs(b))


# ---------------------------------------------------------------------------
# Battery 1: closed-form d_s(tau) for the symbol k^2 + l^2 k^4 (Section 8.2)
# ---------------------------------------------------------------------------
def _P_quad(tau, prefactor=True):
    f = (lambda u: u * np.exp(-tau * (u + u * u))) if prefactor else (lambda u: np.exp(-tau * (u + u * u)))
    return integrate.quad(f, 0, np.inf, epsabs=0, epsrel=1e-12)[0] / (16 * np.pi**2)


def _P_closed(tau):
    z = np.sqrt(tau) / 2
    return (1 - np.sqrt(np.pi) * z * special.erfcx(z)) / (32 * np.pi**2 * tau)


def _ds_closed(tau):
    z = np.sqrt(tau) / 2
    return 1 - tau / 2 + 1 / (1 - np.sqrt(np.pi) * z * special.erfcx(z))


def _ds_fd(tau, prefactor=True, h=1e-4):
    lp = np.log(_P_quad(tau * np.exp(h), prefactor))
    lm = np.log(_P_quad(tau * np.exp(-h), prefactor))
    return -2 * (lp - lm) / (2 * h)


def test_battery_1_spectral_dimension_closed_form() -> None:
    print("--- Battery 1: closed-form d_s(tau) vs quadrature + finite differences ---")
    for tau in (1e-3, 1e-1, 1.0, 10.0, 100.0):
        assert _close(_P_closed(tau), _P_quad(tau), 1e-8), f"P mismatch at tau={tau}"
        assert _close(_ds_closed(tau), _ds_fd(tau), 1e-6), f"d_s mismatch at tau={tau}"
    # limits; note the closed form suffers cancellation for tau >~ 1e4 (1 - sqrt(pi) z erfcx(z) ~ 1/2z^2),
    # so the IR limit is checked at tau = 1e3 against the quadrature value
    assert abs(_ds_closed(1e-6) - 2) < 1e-2
    assert _close(_ds_closed(1e3), _ds_fd(1e3), 1e-4) and abs(_ds_closed(1e3) - 4) < 2e-2
    # negative control: dropping the polynomial prefactor u (the historical error) changes d_s
    assert not _close(_ds_fd(100.0, prefactor=False), _ds_closed(100.0), 1e-2), "control failed to fail"
    print("  [PASSED] closed form matches quadrature; mutated integrand is rejected.\n")


# ---------------------------------------------------------------------------
# Battery 2: barycentric Hessian of log multinomial and the A_{m-1} Cartan matrix (Prop. 2.2)
# ---------------------------------------------------------------------------
def _log_multinomial(x, t):
    return special.gammaln(x + 1) - np.sum(special.gammaln(np.asarray(t) + 1))


def test_battery_2_barycentric_hessian_cartan() -> None:
    print("--- Battery 2: barycentric Hessian vs (m/2x)|v|^2 and Cartan Gram identity ---")
    rng = np.random.default_rng(1)
    for m in (3, 4, 6):
        A = 2 * np.eye(m - 1) - np.eye(m - 1, k=1) - np.eye(m - 1, k=-1)
        roots = np.array([np.eye(m)[j] - np.eye(m)[j + 1] for j in range(m - 1)])
        c = rng.normal(size=m - 1)
        v = c @ roots
        assert _close(v @ v, c @ A @ c, 1e-12), "sum v_i^2 != c^T A c"
        x = 400.0
        tstar = np.full(m, x / m)
        h = 1e-2
        second = (_log_multinomial(x, tstar + h * v) - 2 * _log_multinomial(x, tstar)
                  + _log_multinomial(x, tstar - h * v)) / h**2
        Q_numeric = -second / 2
        Q_exact = special.polygamma(1, x / m + 1) / 2 * (v @ v)
        assert _close(Q_numeric, Q_exact, 1e-5), f"Hessian mismatch m={m}"
        assert _close(Q_exact, m / (2 * x) * (v @ v), 5 * m / x), "leading order m/2x"
        # negative control: the withdrawn factor m/(4x) with the Cartan form must fail
        assert not _close(Q_numeric, m / (4 * x) * (c @ A @ c), 1e-2), "control failed to fail"
    print("  [PASSED] Q = psi'(x/m+1)/2 |v|^2 = (m/2x)(1+O(1/x)) c^T A c; factor m/4x rejected.\n")


# ---------------------------------------------------------------------------
# Battery 3: range of e_2 on the cube and the constraint bounds (Theorem 3.1)
# ---------------------------------------------------------------------------
def test_battery_3_constraint_bounds() -> None:
    print("--- Battery 3: e_2 range on [-a,a]^3 by brute force; K_ij K^ij <= 3a^2 ---")
    a = 1.7
    g = np.linspace(-a, a, 61)
    L1, L2, L3 = np.meshgrid(g, g, g, indexing="ij")
    e2 = L1 * L2 + L2 * L3 + L3 * L1
    assert _close(e2.min(), -a**2, 1e-12) and _close(e2.max(), 3 * a**2, 1e-12)
    KK = L1**2 + L2**2 + L3**2
    R_minus = KK - (L1 + L2 + L3) ** 2          # = R - 2 Lambda - 16 pi G rho
    assert np.all(KK <= 3 * a**2 + 1e-12)
    assert _close(R_minus.min(), -6 * a**2, 1e-12) and _close(R_minus.max(), 2 * a**2, 1e-12)
    # negative control: a symmetric bound |R - ...| <= 2a^2 is violated
    assert R_minus.min() < -2 * a**2, "control failed to fail"
    print("  [PASSED] -6a^2 <= R - 2Lambda - 16piG rho <= 2a^2, both endpoints attained.\n")


# ---------------------------------------------------------------------------
# Battery 4: exponential decay of negatively curved graphon entries (Prop. 6.1)
# ---------------------------------------------------------------------------
def test_battery_4_graphon_decay() -> None:
    print("--- Battery 4: dW/dt = +2 kappa W with kappa <= -c: ODE solve vs bound and t_delta ---")
    rng = np.random.default_rng(2)
    c, W0, delta = 0.7, 0.9, 1e-3
    phase = rng.uniform(0, 2 * np.pi)
    kappa = lambda t: -c - 0.5 * (1 + np.sin(3 * t + phase))  # smooth, always <= -c
    t_delta = np.log(W0 / delta) / (2 * c)
    ts = np.sort(np.append(np.linspace(0, 10, 400), t_delta))
    solve = lambda sign: integrate.solve_ivp(lambda t, w: sign * 2 * kappa(t) * w, (0, 10), [W0], t_eval=ts,
                                             method="DOP853", rtol=1e-11, atol=1e-16).y[0]
    W = solve(+1)
    assert np.all(W <= W0 * np.exp(-2 * c * ts) * (1 + 1e-7))
    assert W[np.searchsorted(ts, t_delta)] <= delta * (1 + 1e-7)
    # negative control: the withdrawn sign dW/dt = -2 kappa W makes the bottleneck GROW
    W_wrong = solve(-1)
    assert W_wrong[-1] > W0, "control failed to fail"
    print(f"  [PASSED] entries fall below delta by t_delta = {t_delta:.3f}.\n")


# ---------------------------------------------------------------------------
# Battery 5: the RT hemisphere is totally geodesic in the half-plane (Section 8.3)
# ---------------------------------------------------------------------------
def _hyperbolic_curvature(x0, R, th):
    """Geodesic curvature of the circle (x0 + R cos th, R sin th) in dx^2+dz^2 / z^2.
    For g = e^{2 phi} delta: k_g = e^{-phi} (k_e + d phi / d n), n the outward normal; phi = -log z."""
    z = R * np.sin(th) if x0 == 0 else R * np.sin(th)
    n_z = np.sin(th)                       # outward normal z-component of a circle centred at (x0, 0)
    dphi_dn = -n_z / z
    return z * (1.0 / R + dphi_dn)


def test_battery_5_hemisphere_totally_geodesic() -> None:
    print("--- Battery 5: boundary-centred semicircle has zero hyperbolic curvature ---")
    th = np.linspace(0.05, np.pi - 0.05, 50)
    k = _hyperbolic_curvature(0.0, 1.3, th)
    assert np.max(np.abs(k)) < 1e-12
    # independent check: arclength-minimality, area of perturbed curves is larger
    def hyp_length(eps):
        t = np.linspace(1e-3, np.pi - 1e-3, 20001)
        r = 1 + eps * np.sin(t) ** 2
        x, zz = r * np.cos(t), r * np.sin(t)
        return integrate.trapezoid(np.hypot(np.gradient(x, t), np.gradient(zz, t)) / zz, t)
    assert hyp_length(0.1) > hyp_length(0.0) and hyp_length(-0.1) > hyp_length(0.0)
    # negative control: a circle whose centre is lifted off the boundary is NOT geodesic
    zc = 0.5
    t = np.linspace(0.3, 2.8, 20)
    zz = zc + np.sin(t)
    n_z = np.sin(t)
    k_off = zz * (1.0 + (-n_z / zz))
    assert np.max(np.abs(k_off)) > 1e-2, "control failed to fail"
    print("  [PASSED] H = 0 on the hemisphere; perturbations increase length; lifted circle rejected.\n")


# ---------------------------------------------------------------------------
# Battery 6: dispersion delay formula and magnitude (Section 9.1)
# ---------------------------------------------------------------------------
def test_battery_6_dispersion_delay() -> None:
    print("--- Battery 6: group velocity by finite differences; Planck-scale delay magnitude ---")
    c, xi, ell = 1.0, 0.5, 1e-3            # large ell to test the formula without round-off
    omega = lambda k: c * k * np.sqrt(1 + xi * ell**2 * k**2)
    for k in (1.0, 5.0, 20.0):
        h = 1e-5 * k
        vg = (omega(k + h) - omega(k - h)) / (2 * h)
        assert _close(vg - c, 1.5 * xi * ell**2 * k**2 * c, 2e-3), f"group velocity at k={k}"
    # magnitude claim of the text (Section 10.1): 6e-62 .. 1e-60 s for ell_P, xi = 1/2, 10 Hz -> 1 kHz, z = 1..8,
    # with the redshift weighting D_2(z) = (c/H0) int (1+z')^2 dz'/E(z')
    cc, hb, GN = 2.99792458e8, 1.054571817e-34, 6.67430e-11
    lP = np.sqrt(hb * GN / cc**3)
    Mpc = 3.0856775814913673e22
    H0 = 70e3 / Mpc
    D = lambda z, n: cc / H0 * integrate.quad(lambda x: (1 + x) ** n / np.sqrt(0.3 * (1 + x) ** 3 + 0.7), 0, z)[0]
    dt = lambda z, n: 6 * np.pi**2 * 0.5 * lP**2 * D(z, n) / cc**3 * (1e6 - 1e2)
    # independent oracle: non-perturbative FRW propagation. A graviton with v = c(1 + eps0 (1+z)^2)
    # (comoving k conserved) emitted at z_e reaches the observer at the redshift z_arr solving
    # int_{z_arr}^{z_e} v/H dz = int_0^{z_e} c/H dz; it arrives earlier than light by int_0^{z_arr} dz/((1+z)H).
    # A large length (30 m) makes the effect resolvable; the result is then compared with the closed form.
    Hf = lambda z: H0 * np.sqrt(0.3 * (1 + z) ** 3 + 0.7)

    def advance(z_e, eps0):
        target = integrate.quad(lambda z: cc / Hf(z), 0, z_e, epsabs=0, epsrel=1e-13)[0]
        g = lambda za: integrate.quad(lambda z: cc * (1 + eps0 * (1 + z) ** 2) / Hf(z), za, z_e,
                                      epsabs=0, epsrel=1e-13)[0] - target
        za = optimize.brentq(g, 0.0, 0.5, xtol=1e-16, rtol=1e-15)
        return integrate.quad(lambda z: 1 / ((1 + z) * Hf(z)), 0, za, epsabs=0, epsrel=1e-13)[0]

    Lbig = 30.0
    eps = lambda f: 1.5 * 0.5 * Lbig**2 * (2 * np.pi * f / cc) ** 2
    for z in (1, 3, 8):
        oracle = advance(z, eps(1e3)) - advance(z, eps(10.0))
        closed = dt(z, 2) * (Lbig / lP) ** 2
        assert _close(closed, oracle, 1e-3), f"z={z}"
        assert not _close(dt(z, 1) * (Lbig / lP) ** 2, oracle, 0.2), "control failed to fail"
    assert 5e-62 < dt(1, 2) < 7e-62 and 1.0e-60 < dt(8, 2) < 1.3e-60
    # negative control: the old claim "approaches the millisecond threshold" is inconsistent
    assert not dt(8, 2) > 1e-4, "control failed to fail"
    print(f"  [PASSED] v_g - c = (3/2) xi l^2 k^2 c; Planck-scale delay {dt(1, 2):.1e}..{dt(8, 2):.1e} s << 1e-4 s.\n")


# ---------------------------------------------------------------------------
# Battery 7: withdrawn Jarlskog formula is dimensionally and numerically wrong (Section 7)
# ---------------------------------------------------------------------------
def test_battery_7_withdrawn_jarlskog_formula() -> None:
    print("--- Battery 7: regression guard for the withdrawn J_CP formula ---")
    masses = dict(u=0.00216, c=1.27, t=172.7, d=0.00467, s=0.0934, b=4.18)
    v = 246.22
    J_old = np.sin(np.radians(63.90)) / (6 * np.sqrt(3)) * np.sqrt(np.prod(list(masses.values()))) / v**6
    # scaling all masses and v by lambda must leave a dimensionless quantity invariant; the old one scales as lambda^-3
    lam = 10.0
    J_scaled = np.sin(np.radians(63.90)) / (6 * np.sqrt(3)) * np.sqrt(np.prod([lam * m for m in masses.values()])) / (lam * v) ** 6
    assert _close(J_scaled / J_old, lam**-3, 1e-12)
    assert J_old < 1e-15
    print(f"  [PASSED] old formula scales as lambda^-3 and gives {J_old:.1e} (not 3e-5): correctly withdrawn.\n")


def run_all_tests():
    print("=" * 67)
    print("CHAPTER 12 NUMERICAL VERIFICATION (independent oracles + negative controls)")
    print("=" * 67 + "\n")
    test_battery_1_spectral_dimension_closed_form()
    test_battery_2_barycentric_hessian_cartan()
    test_battery_3_constraint_bounds()
    test_battery_4_graphon_decay()
    test_battery_5_hemisphere_totally_geodesic()
    test_battery_6_dispersion_delay()
    test_battery_7_withdrawn_jarlskog_formula()
    print("=" * 67)
    print("ALL 7 CHAPTER 12 BATTERIES PASSED")
    print("=" * 67)


if __name__ == "__main__":
    run_all_tests()
