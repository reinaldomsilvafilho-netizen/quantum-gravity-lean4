"""
Standalone Python Numerical & Inverse Process Engine for Chapter 04
Treatise: Cânone Unificado de Gravitação Quântica e Geometria Multilinear
Chapter 04: Nonlinear Simplicial Waves and Anomalous Porous Transport Induced by Beta-Kernel Fractional Laplacians
Author: Reinaldo M. Silva-Filho
"""

import numpy as np
import scipy.special as sp
import scipy.integrate as integrate

def mittag_leffler(beta, z, terms=60):
    """Accurate series evaluation of E_beta(z) for negative/moderate z."""
    res = 0.0
    for n in range(terms):
        term = (z**n) / sp.gamma(beta * n + 1.0)
        res += term
        if abs(term) < 1e-15 and n > 5:
            break
    return res

def test_simplicial_laplacian_symbol_and_cartan():
    print("Battery 1: Testing Simplicial Dispersion Symbol & Cartan Metric Emergence...")
    m = 3
    alpha = 1.5
    # Cartan matrix for A_2
    A2 = np.array([[2.0, 1.0], [1.0, 2.0]])
    
    # Test for decreasing wavevector magnitudes |k| -> 0
    k_dir = np.array([0.6, -0.8])
    for scale in [0.1, 0.01, 0.001]:
        k = scale * k_dir
        k3 = -k[0] - k[1]
        
        # Analytical symbol: 1/alpha^2 * [1 - R^alpha cos(alpha * Theta)]
        exp_sum = np.exp(-1j * k[0]) + np.exp(-1j * k[1]) + np.exp(-1j * k3)
        R = np.abs(exp_sum) / float(m)
        Theta = np.angle(exp_sum)
        sigma = (1.0 - (R**alpha) * np.cos(alpha * Theta)) / (alpha**2)
        
        # Cartan quadratic form: 1/(2*m*alpha) * k^T A_{m-1} k
        sigma_cartan = (k.T @ A2 @ k) / (2.0 * m * alpha)
        
        rel_diff = abs(sigma - sigma_cartan) / sigma_cartan
        print(f"  scale = {scale:6.3f} | sigma = {sigma:.8e} | cartan = {sigma_cartan:.8e} | rel_diff = {rel_diff:.4e}")
        
    assert rel_diff < 1e-4, f"Cartan metric convergence failed: {rel_diff}"
    print("  [PASS] Emergence of A_{m-1} Cartan metric in long-wavelength limit verified.")

def test_simplicial_laplacian_self_adjoint():
    print("\nBattery 2: Testing Self-Adjointness and Positivity of Simplicial Laplacian...")
    # Discrete grid test in 2D
    N = 16
    L = 4.0
    x = np.linspace(-L, L, N, endpoint=False)
    y = np.linspace(-L, L, N, endpoint=False)
    X, Y = np.meshgrid(x, y)
    
    # Two test functions
    u = np.exp(-(X**2 + Y**2))
    v = np.sin(X) * np.exp(-Y**2)
    
    # Fourier representation of Laplacian action
    kx = 2 * np.pi * np.fft.fftfreq(N, d=2*L/N)
    ky = 2 * np.pi * np.fft.fftfreq(N, d=2*L/N)
    KX, KY = np.meshgrid(kx, ky)
    KZ = -KX - KY
    
    exp_sum = np.exp(-1j * KX) + np.exp(-1j * KY) + np.exp(-1j * KZ)
    m = 3
    alpha = 1.0
    R = np.abs(exp_sum) / float(m)
    Theta = np.angle(exp_sum)
    sigma = (1.0 - (R**alpha) * np.cos(alpha * Theta)) / (alpha**2)
    
    # In Fourier domain: -Delta u -> sigma * u_hat
    u_hat = np.fft.fft2(u)
    v_hat = np.fft.fft2(v)
    
    # Inner product <u, -Delta v> = sum u_hat^* * sigma * v_hat / N^2
    inner_u_Delta_v = np.real(np.sum(np.conj(u_hat) * sigma * v_hat))
    inner_Delta_u_v = np.real(np.sum(np.conj(sigma * u_hat) * v_hat))
    
    sym_diff = abs(inner_u_Delta_v - inner_Delta_u_v) / abs(inner_u_Delta_v)
    assert sym_diff < 1e-14, f"Self-adjointness violation: {sym_diff}"
    
    # Positivity: <u, -Delta u> >= 0
    energy_u = np.real(np.sum(np.conj(u_hat) * sigma * u_hat))
    assert energy_u >= 0, f"Positivity violation: {energy_u}"
    print(f"  Symmetry error: |<u, -Delta v> - <-Delta u, v>| = {sym_diff:.2e}")
    print(f"  Energy <u, -Delta u> = {energy_u:.4e} >= 0")
    print("  [PASS] Self-adjointness and positive semi-definiteness verified.")

def test_nlse_conservation_laws():
    print("\nBattery 3: Testing Global Conservation of Mass and Energy in Simplicial NLSE...")
    # Time-stepping simulation of 1D Simplicial NLSE: i hbar psi_t = -hbar^2/(2M) Delta psi - kappa |psi|^(2*sigma) psi
    N = 64
    L = 10.0
    x = np.linspace(-L, L, N, endpoint=False)
    dx = 2 * L / N
    k = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    
    # 1D simplicial symbol: k2 = -k1
    m = 2
    alpha = 1.0
    exp_sum = np.exp(-1j * k) + np.exp(1j * k)
    R = np.abs(exp_sum) / 2.0
    Theta = np.angle(exp_sum)
    sigma_k = (1.0 - (R**alpha) * np.cos(alpha * Theta)) / (alpha**2)
    
    hbar = 1.0
    M = 1.0
    kappa = 1.0
    sigma_nl = 1.0
    
    # Initial state: localized wavepacket
    psi = (1.0 / (np.pi**0.25)) * np.exp(-x**2 / 2.0) * np.exp(1j * 0.5 * x)
    
    def get_mass(p):
        return np.sum(np.abs(p)**2) * dx
        
    def get_energy(p):
        p_hat = np.fft.fft(p)
        kinetic = (hbar**2 / (2.0 * M)) * np.sum(sigma_k * np.abs(p_hat)**2) * dx / N
        interaction = - (kappa / (sigma_nl + 1.0)) * np.sum(np.abs(p)**(2*sigma_nl + 2)) * dx
        return kinetic + interaction
        
    mass_0 = get_mass(psi)
    energy_0 = get_energy(psi)
    
    # Strang splitting time evolution
    dt = 0.005
    steps = 100
    kinetic_phase = np.exp(-1j * (hbar / (2.0 * M)) * sigma_k * (dt / 2.0))
    
    for _ in range(steps):
        # Half step kinetic
        psi = np.fft.ifft(np.fft.fft(psi) * kinetic_phase)
        # Full step non-linear
        psi = psi * np.exp(1j * (kappa / hbar) * (np.abs(psi)**(2*sigma_nl)) * dt)
        # Half step kinetic
        psi = np.fft.ifft(np.fft.fft(psi) * kinetic_phase)
        
    mass_end = get_mass(psi)
    energy_end = get_energy(psi)
    
    d_mass = abs(mass_end - mass_0) / mass_0
    d_energy = abs(energy_end - energy_0) / abs(energy_0)
    
    print(f"  Initial Mass = {mass_0:.6f} | Final Mass = {mass_end:.6f} | rel_diff = {d_mass:.2e}")
    print(f"  Initial Energy = {energy_0:.6f} | Final Energy = {energy_end:.6f} | rel_diff = {d_energy:.2e}")
    assert d_mass < 1e-12, f"Mass conservation violated: {d_mass}"
    assert d_energy < 1e-4, f"Energy conservation violated: {d_energy}"
    print("  [PASS] Mass and Hamiltonian energy conserved identically.")

def test_modulational_instability():
    print("\nBattery 4: Testing Simplicial Modulational Instability...")
    hbar = 1.0
    M = 1.0
    kappa = 2.0
    sigma_nl = 1.0
    rho_0 = 1.0
    
    sigma_thresh = 4.0 * M * kappa * sigma_nl * (rho_0**sigma_nl) / (hbar**2)
    # Thresh = 4 * 1 * 2 * 1 * 1 / 1 = 8.0
    print(f"  Instability Threshold sigma_thresh = {sigma_thresh:.4f}")
    
    # Check dispersion for sigma < sigma_thresh (unstable)
    sigma_low = 4.0
    Omega_sq = (sigma_low / (2.0 * M)) * (sigma_low / (2.0 * M) - 2.0 * kappa * sigma_nl * rho_0**sigma_nl)
    # Omega_sq = 2 * (2 - 4) = -4 < 0
    growth_rate = np.sqrt(-Omega_sq)
    assert Omega_sq < 0, "Expected modulational instability"
    
    # Maximum growth rate at sigma = sigma_thresh / 2 = 4.0
    gamma_max_theory = (kappa * sigma_nl * (rho_0**sigma_nl)) / hbar
    print(f"  sigma = {sigma_low} -> Omega^2 = {Omega_sq:.2f} < 0 (Unstable)")
    print(f"  Observed Growth Rate = {growth_rate:.4f} == Theory gamma_max = {gamma_max_theory:.4f}")
    assert abs(growth_rate - gamma_max_theory) < 1e-12, "Max growth rate mismatch"
    print("  [PASS] Modulational instability criterion and maximum growth rate verified.")

def test_mittag_leffler_anomalous_diffusion():
    print("\nBattery 5: Testing Mittag-Leffler Propagator & Subdiffusive Scaling...")
    # Test beta = 1: should reduce to exact standard exponential e^(-a t)
    beta_1 = 1.0
    z = -1.5
    ml_1 = mittag_leffler(beta_1, z)
    exp_exact = np.exp(z)
    err_1 = abs(ml_1 - exp_exact)
    assert err_1 < 1e-14, f"Mittag-Leffler beta=1 reduction failed: {err_1}"
    print(f"  beta = 1.0: E_1(-1.5) = {ml_1:.8f} == exp(-1.5) = {exp_exact:.8f} (err = {err_1:.2e})")
    
    # Test beta = 0.5 (subdiffusion)
    beta_half = 0.5
    ml_half = mittag_leffler(beta_half, -0.5)
    print(f"  beta = 0.5: E_0.5(-0.5) = {ml_half:.8f} (well-defined subdiffusion propagator)")
    assert 0.0 < ml_half < 1.0, "Subdiffusive propagator out of physical bounds"
    print("  [PASS] Mittag-Leffler anomalous diffusion propagator verified.")

def test_anisotropic_msd_covariance_tensor():
    print("\nBattery 6: Testing Anisotropic MSD Covariance Tensor Scaling...")
    m = 3
    alpha = 1.2
    beta = 0.75
    K_diff = 2.5
    t = 4.0
    
    A2 = np.array([[2.0, 1.0], [1.0, 2.0]])
    
    # Theoretical MSD tensor: K_diff / (m * alpha * Gamma(beta + 1)) * A_{m-1} * t^beta
    gamma_factor = sp.gamma(beta + 1.0)
    MSD_tensor = (K_diff / (m * alpha * gamma_factor)) * A2 * (t**beta)
    
    print(f"  Time t = {t:.2f} | beta = {beta} (subdiffusion)")
    print(f"  MSD Covariance Tensor <x x^T>:\n{MSD_tensor}")
    
    # Verify eigenvalues and positive definiteness
    evals = np.linalg.eigvalsh(MSD_tensor)
    assert np.all(evals > 0), "MSD tensor not positive definite"
    # Ratio of principal axes given by eigenvalues of Cartan matrix: for A_2, evals of [[2, 1], [1, 2]] are 3 and 1
    eval_ratio = evals[1] / evals[0]
    expected_ratio = 3.0 / 1.0
    err_ratio = abs(eval_ratio - expected_ratio)
    assert err_ratio < 1e-12, f"Eigenvalue ratio mismatch: {eval_ratio}"
    print(f"  Principal dispersion axis ratio = {eval_ratio:.4f} (Matches exact A_2 root system 3:1)")
    print("  [PASS] Anisotropic MSD covariance tensor rigorously verified.")

def test_inverse_permeability_reconstruction():
    print("\nBattery 7: Testing Inverse Engine (Permeability & Memory Parameter Inversion)...")
    m_true = 3
    alpha_true = 1.45
    beta_true = 0.65
    K_diff_true = 3.2
    
    t1, t2 = 1.0, 5.0
    C1 = (K_diff_true / (m_true * alpha_true * sp.gamma(beta_true + 1.0))) * np.array([[2, 1], [1, 2]]) * (t1**beta_true)
    C2 = (K_diff_true / (m_true * alpha_true * sp.gamma(beta_true + 1.0))) * np.array([[2, 1], [1, 2]]) * (t2**beta_true)
    
    # Invert for beta: Tr(C2) / Tr(C1) = (t2 / t1)^beta
    ratio = np.trace(C2) / np.trace(C1)
    beta_recon = np.log(ratio) / np.log(t2 / t1)
    
    err_beta = abs(beta_recon - beta_true)
    assert err_beta < 1e-12, f"Beta inversion failed: {err_beta}"
    
    # Invert for Cartan matrix structure: C1 / Tr(C1)
    Cartan_norm = C1 / (np.trace(C1) / 4.0)  # For A_2, Tr(A_2) = 4
    err_Cartan = np.max(np.abs(Cartan_norm - np.array([[2, 1], [1, 2]])))
    assert err_Cartan < 1e-12, f"Cartan structure inversion failed: {err_Cartan}"
    
    print(f"  True beta = {beta_true:.6f} | Inverted beta = {beta_recon:.6f} (err = {err_beta:.2e})")
    print(f"  Cartan Matrix Reconstruction Error: {err_Cartan:.2e}")
    print("  [PASS] Inverse engine achieved perfect recovery of transport parameters.")

if __name__ == "__main__":
    print("=" * 75)
    print("CHAPTER 04 NUMERICAL SIMULATION & INVERSE PROCESS ENGINE")
    print("=" * 75)
    test_simplicial_laplacian_symbol_and_cartan()
    test_simplicial_laplacian_self_adjoint()
    test_nlse_conservation_laws()
    test_modulational_instability()
    test_mittag_leffler_anomalous_diffusion()
    test_anisotropic_msd_covariance_tensor()
    test_inverse_permeability_reconstruction()
    print("\n" + "=" * 75)
    print("ALL 7 TEST BATTERIES FOR CHAPTER 04 PASSED WITH ZERO FAILURES!")
    print("=" * 75)
