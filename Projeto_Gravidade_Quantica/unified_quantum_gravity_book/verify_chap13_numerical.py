"""
Verification Suite for Chapter 13: Observational Signatures of a Running Spectral Dimension
Author: Reinaldo Maia Silva-Filho

Each battery checks a number or formula quoted in the chapter against an independent
computation, and includes a negative control that must fail.
Runs standalone (python verify_chap13_numerical.py) or under pytest.
"""

import numpy as np
from scipy import integrate, optimize, special

c = 2.99792458e8
hbar = 1.054571817e-34
G = 6.67430e-11
ell_P = np.sqrt(hbar * G / c**3)
Mpc = 3.0856775814913673e22
H0 = 70e3 / Mpc
Om, OL = 0.3, 0.7
hbar_c_GeV_m = 1.973269804e-16
M_P_GeV = 1.220890e19


def _E(z):
    return np.sqrt(Om * (1 + z) ** 3 + OL)


def _D2(z, power=2):
    """Distance weighted by (1+z')^power; the text uses power = 2."""
    return c / H0 * integrate.quad(lambda zp: (1 + zp) ** power / _E(zp), 0, z)[0]


def _dt(ell, D, f1, f2, xi=0.5):
    return 6 * np.pi**2 * xi * ell**2 * D / c**3 * (f2**2 - f1**2)


def _arrival_advance(z_e, eps0):
    """Independent oracle: a particle with v = c (1 + eps0 (1+z)^2) (comoving k conserved,
    k_phys = k_obs (1+z)) emitted at z_e together with a light signal. Solve non-perturbatively
    for the redshift z_arr at which it reaches the observer's comoving position,
        int_{z_arr}^{z_e} v/H dz = int_0^{z_e} c/H dz,
    and return how much earlier than the light signal it arrives, int_0^{z_arr} dz/((1+z)H)."""
    H = lambda z: H0 * _E(z)
    target = integrate.quad(lambda z: c / H(z), 0, z_e, epsabs=0, epsrel=1e-13)[0]
    f = lambda za: integrate.quad(lambda z: c * (1 + eps0 * (1 + z) ** 2) / H(z), za, z_e,
                                  epsabs=0, epsrel=1e-13)[0] - target
    za = optimize.brentq(f, 0.0, 0.5, xtol=1e-16, rtol=1e-15)
    return integrate.quad(lambda z: 1 / ((1 + z) * H(z)), 0, za, epsabs=0, epsrel=1e-13)[0]


def _order(x):
    return int(np.floor(np.log10(abs(x))))


def test_battery_1_heat_kernel_closed_form() -> None:
    print("--- Battery 1: Eq. (1) closed form vs quadrature (l_P = 1) ---")
    for tau in (1e-3, 1e-1, 1.0, 10.0, 100.0):
        quad = integrate.quad(lambda u: u * np.exp(-tau * (u + u * u)), 0, np.inf, epsrel=1e-12)[0] / (16 * np.pi**2)
        z = np.sqrt(tau) / 2
        closed = (1 - np.sqrt(np.pi) * z * special.erfcx(z)) / (32 * np.pi**2 * tau)
        assert abs(closed / quad - 1) < 1e-6
    # negative control: dropping sqrt(pi) in the bracket breaks agreement
    closed_bad = (1 - z * special.erfcx(z)) / (32 * np.pi**2 * tau)
    assert abs(closed_bad / quad - 1) > 1e-2, "control failed to fail"
    print("  [PASSED] agreement better than 1e-6 on tau in [1e-3, 1e2].\n")


def test_battery_2_group_velocity() -> None:
    print("--- Battery 2: v_g = c(1 + 3/2 xi l^2 k^2) by finite differences ---")
    xi, ell = 0.5, 1e-3
    omega = lambda k: k * np.sqrt(1 + xi * ell**2 * k**2)
    for k in (1.0, 10.0, 30.0):
        h = 1e-5 * k
        vg = (omega(k + h) - omega(k - h)) / (2 * h)
        assert abs((vg - 1) / (1.5 * xi * ell**2 * k**2) - 1) < 5e-3
    # negative control: a coefficient 1/2 (phase velocity) is rejected
    assert abs((vg - 1) / (0.5 * xi * ell**2 * k**2) - 1) > 1, "control failed to fail"
    print("  [PASSED]\n")


def test_battery_3_redshift_weighting_oracle() -> None:
    print("--- Battery 3: (1+z)^2 weighting of D_2 vs a non-perturbative FRW propagation oracle ---")
    xi, ell = 0.5, 30.0                       # large ell so that the effect is resolvable in double precision
    f1, f2 = 10.0, 1000.0
    for z in (1.0, 3.0, 8.0):
        eps = lambda f: 1.5 * xi * ell**2 * (2 * np.pi * f / c) ** 2
        oracle = _arrival_advance(z, eps(f2)) - _arrival_advance(z, eps(f1))
        formula = _dt(ell, _D2(z, 2), f1, f2, xi)
        assert abs(formula / oracle - 1) < 1e-3, f"z={z}: formula/oracle = {formula/oracle}"
        # negative control: weighting (1+z)^1 disagrees with the oracle
        wrong = _dt(ell, _D2(z, 1), f1, f2, xi)
        assert abs(wrong / oracle - 1) > 0.2, "control failed to fail"
    print("  [PASSED] closed form with (1+z)^2 agrees with the oracle to 1e-3; (1+z)^1 is rejected.\n")


def test_battery_4_quoted_delays_and_required_scale() -> None:
    print("--- Battery 4: quoted delays 6e-62, 3e-61, 1.2e-60 s; ell_* ~ 3.0e-7 m (~0.7 eV) at z = 3 ---")
    quoted = {1: 6e-62, 3: 3e-61, 8: 1.2e-60}
    for z, q in quoted.items():
        dt = _dt(ell_P, _D2(z), 10.0, 1000.0)
        assert 0.85 * q <= dt <= 1.15 * q, f"z={z}: computed {dt:.2e} vs quoted {q:.1e}"
    gaps = [np.log10(1e-4 / _dt(ell_P, _D2(z), 10.0, 1000.0)) for z in (1, 3, 8)]
    assert 55.5 < min(gaps) and max(gaps) < 57.5, gaps
    D = _D2(3)
    ell_req = np.sqrt(1e-4 * c**3 / (6 * np.pi**2 * 0.5 * D * (1000.0**2 - 10.0**2)))
    assert abs(ell_req / 3.0e-7 - 1) < 0.03
    E_eV = hbar_c_GeV_m / ell_req * 1e9
    assert 0.6 < E_eV < 0.75
    assert abs(_dt(ell_req, D, 10.0, 1000.0) / 1e-4 - 1) < 1e-10
    # negative control: the (1+z)^1 weighting would give 4.7e-7 m, outside the quoted value
    ell_bad = np.sqrt(1e-4 * c**3 / (6 * np.pi**2 * 0.5 * _D2(3, 1) * (1000.0**2 - 10.0**2)))
    assert abs(ell_bad / 3.0e-7 - 1) > 0.3, "control failed to fail"
    print(f"  [PASSED] gaps {min(gaps):.1f}-{max(gaps):.1f} orders; ell_* = {ell_req:.2e} m, E = {E_eV:.2f} eV.\n")


def test_battery_5_tilt_running_at_horizon_exit() -> None:
    print("--- Battery 5: H_inf <= 4.7e13 GeV from r < 0.036; |alpha_t| ~ (H_inf/M_P)^2 <= 1.5e-11 ---")
    M_red = M_P_GeV / np.sqrt(8 * np.pi)
    r, A_s = 0.036, 2.1e-9
    # oracle: tensor power spectrum P_t = (8/M_red^2)(H/2pi)^2, solved for H by root finding
    H = optimize.brentq(lambda h: 8 / M_red**2 * (h / (2 * np.pi)) ** 2 - r * A_s, 1e8, 1e18, rtol=1e-14)
    assert abs(H / 4.7e13 - 1) < 0.01
    # alpha_t from the Pade d_s evaluated directly, (d_s - 4)/2
    d_s = lambda x: 2 + 2 / (1 + x**2)
    alpha = lambda p, M: (d_s(p / M) - 4) / 2
    assert abs(-alpha(H, M_P_GeV) / 1.5e-11 - 1) < 0.02
    assert abs(-alpha(H, M_red) / 3.7e-10 - 1) < 0.02
    # negative control: today's comoving pivot k = 0.05/Mpc gives ~7e-118, off by ~1e106
    k_pivot = 0.05 / Mpc * hbar_c_GeV_m
    assert -alpha(k_pivot, M_P_GeV) < 1e-100, "control failed to fail"
    print(f"  [PASSED] H_inf = {H:.2e} GeV, |alpha_t| = {-alpha(H, M_P_GeV):.1e} (M_P), {-alpha(H, M_red):.1e} (M_red).\n")


def test_battery_6_atom_interferometry_ratio() -> None:
    print("--- Battery 6: l_P / lambda_dB = 3.5e-27 (v / 1 m/s) for Sr-87; < 2e-25 for v <= 45 m/s ---")
    m_Sr = 87 * 1.66053906660e-27
    ratio = lambda v: ell_P / (2 * np.pi * hbar / (m_Sr * v))
    assert abs(ratio(1.0) / 3.5e-27 - 1) < 0.02
    assert ratio(45.0) < 2e-25
    # negative control: the ratio at 45 m/s exceeds 4e-26, so a velocity-free bound 4e-26 would be false
    assert ratio(45.0) > 4e-26, "control failed to fail"
    print(f"  [PASSED] ratio(1 m/s) = {ratio(1.0):.2e}, ratio(45 m/s) = {ratio(45.0):.1e}.\n")


def run_all_tests():
    print("=" * 67)
    print("CHAPTER 13 NUMERICAL VERIFICATION (independent oracles + negative controls)")
    print("=" * 67 + "\n")
    test_battery_1_heat_kernel_closed_form()
    test_battery_2_group_velocity()
    test_battery_3_redshift_weighting_oracle()
    test_battery_4_quoted_delays_and_required_scale()
    test_battery_5_tilt_running_at_horizon_exit()
    test_battery_6_atom_interferometry_ratio()
    print("=" * 67)
    print("ALL 6 CHAPTER 13 BATTERIES PASSED")
    print("=" * 67)


if __name__ == "__main__":
    run_all_tests()
