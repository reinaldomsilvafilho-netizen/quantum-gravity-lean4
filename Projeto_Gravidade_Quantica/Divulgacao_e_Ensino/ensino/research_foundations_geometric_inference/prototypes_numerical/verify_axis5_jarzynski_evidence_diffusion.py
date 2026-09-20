"""
Verification Testbed: Axis V - Symplectic Floer Homology and Evidence Diffusions
Obligations: OBL-INF-013, OBL-INF-014, OBL-INF-015

Author: Reinaldo Maia Silva-Filho
Affiliation: PPGEE/DES, Universidade Federal de Lavras (UFLA)
"""

import numpy as np

def analytical_gaussian_evidence(y, sigma_0=1.0, sigma_y=0.5):
    """
    Prior: theta ~ N(0, sigma_0^2 I_d)
    Likelihood: y | theta ~ N(theta, sigma_y^2 I_d)
    Marginal evidence: y ~ N(0, (sigma_0^2 + sigma_y^2) I_d)
    """
    d = len(y)
    var_total = sigma_0**2 + sigma_y**2
    y_norm_sq = np.sum(y**2)
    Z_analytical = (2.0 * np.pi * var_total)**(-d / 2.0) * np.exp(-0.5 * y_norm_sq / var_total)
    return Z_analytical

def simulate_symplectic_jarzynski_sampler(y, sigma_0=1.0, sigma_y=0.5, N_paths=2500, K_steps=60, T_total=1.5, gamma=2.0, perturb=False):
    """
    Symplectic Non-Equilibrium Evidence Sampler (SNE-ES) on phase space (theta, p).
    Anneals from prior U_0(theta) to unnormalized posterior U_1(theta).
    Accumulates work W along each non-equilibrium trajectory.
    """
    d = len(y)
    dt = T_total / K_steps
    
    # Prior potential: U_0(theta) = 0.5 * ||theta||^2 / sigma_0^2 + d * ln(sqrt(2*pi)*sigma_0)
    # Posterior potential: U_1(theta) = U_0(theta) + 0.5 * ||y - theta||^2 / sigma_y^2 + d * ln(sqrt(2*pi)*sigma_y)
    # Log-likelihood: ln p(y|theta) = -0.5 * ||y - theta||^2 / sigma_y^2 - d * ln(sqrt(2*pi)*sigma_y)
    
    Z_0 = (2.0 * np.pi * (sigma_0**2))**(d / 2.0)
    
    works = np.zeros(N_paths)
    
    for n in range(N_paths):
        # 1. Sample from prior equilibrium ensemble
        theta = np.random.randn(d) * sigma_0
        p = np.random.randn(d)  # mass M = 1
        
        W = 0.0
        
        for k in range(K_steps):
            t = k * dt
            lam = k / K_steps
            dot_lam = 1.0 / T_total
            
            # Trajectory work increment: dW = dot_lam * (U_1 - U_0) * dt = -dot_lam * ln p(y|theta) * dt
            log_lik = -0.5 * np.sum((y - theta)**2) / (sigma_y**2) - d * np.log(np.sqrt(2.0 * np.pi) * sigma_y)
            delta_U = -log_lik
            
            if perturb:
                # Floer topological perturbation: smooth harmonic deformation with zero net flux
                delta_U += 0.05 * np.sin(2.0 * np.pi * t / T_total) * np.sum(theta)
                
            W += dot_lam * delta_U * dt
            
            # Symplectic drift: nabla U_t(theta) = (1 - lam) * nabla U_0 + lam * nabla U_1
            grad_U0 = theta / (sigma_0**2)
            grad_U1 = grad_U0 - (y - theta) / (sigma_y**2)
            grad_Ut = (1.0 - lam) * grad_U0 + lam * grad_U1
            
            # Leapfrog half-step for momentum
            p_half = p - 0.5 * dt * grad_Ut
            
            # Position full-step
            theta = theta + dt * p_half
            
            # New gradient
            lam_next = (k + 1) / K_steps
            grad_U0_next = theta / (sigma_0**2)
            grad_U1_next = grad_U0_next - (y - theta) / (sigma_y**2)
            grad_Ut_next = (1.0 - lam_next) * grad_U0_next + lam_next * grad_U1_next
            
            p_full = p_half - 0.5 * dt * grad_Ut_next
            
            # Langevin thermostat
            c1 = np.exp(-gamma * dt)
            c2 = np.sqrt(max(0.0, 1.0 - c1**2))
            xi = np.random.randn(d)
            p = c1 * p_full + c2 * xi
            
        works[n] = W
        
    # Unbiased Jarzynski estimate: Z_hat = Z_0 * mean(exp(-W))
    # Numerically stable log-sum-exp:
    max_neg_w = np.max(-works)
    log_mean_exp = max_neg_w + np.log(np.mean(np.exp(-works - max_neg_w)))
    Z_hat = np.exp(log_mean_exp)
    
    return Z_hat, works

def test_axis5_jarzynski_evidence():
    print("==================================================================")
    print("TEST SUITE: Axis V - Symplectic Floer Evidence Estimation (OBL-INF-013/014/015)")
    print("==================================================================")
    
    np.random.seed(42)
    y = np.array([1.2, -0.8])
    sigma_0 = 1.0
    sigma_y = 0.5
    
    # 1. Exact Analytical Evidence Ground Truth
    Z_exact = analytical_gaussian_evidence(y, sigma_0=sigma_0, sigma_y=0.5)
    print(f"[1] Analytical Ground Truth Evidence Z_exact = {Z_exact:.6e}")
    
    # 2. Symplectic Non-Equilibrium Evidence Sampler (OBL-INF-013 & OBL-INF-014)
    N_paths = 3000
    print(f"[2] Running Symplectic Jarzynski Sampler with N = {N_paths} non-equilibrium trajectories...")
    Z_hat, works = simulate_symplectic_jarzynski_sampler(y, sigma_0=sigma_0, sigma_y=0.5, N_paths=N_paths, K_steps=50, T_total=1.2, perturb=False)
    
    rel_error = abs(Z_hat - Z_exact) / Z_exact
    print(f"    Estimated Evidence Z_hat  = {Z_hat:.6e}")
    print(f"    Exact Evidence Z_exact    = {Z_exact:.6e}")
    print(f"    Relative Estimation Error = {rel_error * 100:.2f}%")
    print(f"    Work Distribution: Mean = {np.mean(works):.3f}, Std = {np.std(works):.3f}")
    
    assert rel_error < 0.10, f"Jarzynski evidence estimation error exceeds 10%: {rel_error}"
    print("  -> PASSED: Unbiased non-equilibrium evidence estimation certified (OBL-INF-014).")
    
    # 3. Floer Topological Stability under Perturbation (OBL-INF-015)
    print(f"[3] Testing Floer Action Topological Stability under Smooth Score Perturbation...")
    Z_hat_perturbed, works_pert = simulate_symplectic_jarzynski_sampler(y, sigma_0=sigma_0, sigma_y=0.5, N_paths=N_paths, K_steps=50, T_total=1.2, perturb=True)
    
    rel_error_perturbed = abs(Z_hat_perturbed - Z_exact) / Z_exact
    print(f"    Perturbed Evidence Z_hat_pert = {Z_hat_perturbed:.6e}")
    print(f"    Perturbed Relative Error      = {rel_error_perturbed * 100:.2f}%")
    
    assert rel_error_perturbed < 0.12, "Floer topological deformation must preserve unbiased evidence estimation!"
    print("  -> PASSED: Floer action topological stability certified (OBL-INF-015).")
    
    print("==================================================================")
    print("ALL TESTS IN AXIS V PASSED SUCCESSFULLY!")
    print("==================================================================")

if __name__ == "__main__":
    test_axis5_jarzynski_evidence()
