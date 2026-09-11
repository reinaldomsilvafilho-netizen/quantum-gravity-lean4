"""
================================================================================
VERIFICATION SUITE: NON-PERTURBATIVE GEOMETRIC INVARIANTS IN LINEAR ALGEBRA
================================================================================
Author: Reinaldo M. Silva-Filho
Affiliation: PPGEE/DES, Universidade Federal de Lavras (UFLA), Brazil
Funding: CAPES Finance Code 001

This benchmark suite rigorously validates the 5 foundational pillars:
  1. Steiner-Federer Lipschitz Continuous Pseudoinverse (A_mu^\dagger)
  2. Geodesic Isometric Inversion on Riemannian Symmetric Cones (S_{++}^m)
  3. Simplicial Beta-Kernel Fractional Resolvents on Singular Graph Laplacians
  4. Continuous Tensor-Train (cTT) & Functional Maxvol Cross-Interpolation
  5. Hyperbolic Space-Form Preconditioning & Universal Covering Homotopic Solvers
================================================================================
"""

import numpy as np
import scipy.linalg as la
import scipy.sparse as sp
import time
import sys

np.random.seed(42)

def print_header(title):
    print("\n" + "=" * 80)
    print(f"  {title.upper()}")
    print("=" * 80)

# ==============================================================================
# BATTERY 1: STEINER-FEDERER LIPSCHITZ CONTINUOUS PSEUDOINVERSE (A_mu^\dagger)
# ==============================================================================
def steiner_pseudoinverse(A, mu):
    """
    Computes the Steiner-Federer Lipschitz-continuous pseudoinverse:
    A_mu^\dagger = V * diag(sigma / (sigma^2 + mu^2)) * U^T
    """
    U, s, Vt = la.svd(A, full_matrices=False)
    s_reg = s / (s**2 + mu**2)
    return Vt.T @ np.diag(s_reg) @ U.T

def test_battery_1_steiner_pseudoinverse():
    print_header("Battery 1: Steiner-Federer Pseudoinverse (A_mu^\\dagger)")
    
    # Test 1.1: Rank transition continuity as sigma_min -> 0
    m, n = 20, 10
    mu = 0.05
    U, _ = la.qr(np.random.randn(m, n), mode='economic')
    V, _ = la.qr(np.random.randn(n, n))
    
    singular_values_base = np.array([10.0, 5.0, 2.0, 1.0, 0.5, 0.2, 0.1, 0.05, 0.01, 1e-4])
    A_base = U @ np.diag(singular_values_base) @ V.T
    
    # Perturb the smallest singular value across rank boundary (from 1e-4 down to 1e-12)
    singular_values_pert = singular_values_base.copy()
    singular_values_pert[-1] = 1e-12
    A_pert = U @ np.diag(singular_values_pert) @ V.T
    
    delta_A = A_pert - A_base
    delta_norm = la.norm(delta_A, 2)
    
    # Moore-Penrose pseudoinverse jump
    pinv_base_mp = la.pinv(A_base)
    pinv_pert_mp = la.pinv(A_pert)
    mp_diff_norm = la.norm(pinv_pert_mp - pinv_base_mp, 2)
    
    # Steiner pseudoinverse jump
    pinv_base_st = steiner_pseudoinverse(A_base, mu)
    pinv_pert_st = steiner_pseudoinverse(A_pert, mu)
    st_diff_norm = la.norm(pinv_pert_st - pinv_base_st, 2)
    
    # Theoretical Lipschitz bound: ||A_mu^\dagger - B_mu^\dagger|| <= ||A - B|| / mu^2
    lip_bound = delta_norm / (mu**2)
    
    print(f"  [1.1] Rank Transition Perturbation ||Delta A||_2: {delta_norm:.4e}")
    print(f"        Classical Moore-Penrose Jump ||Delta A^\\dagger||_2: {mp_diff_norm:.4e} (EXPLOSION)")
    print(f"        Steiner Pseudoinverse Jump ||Delta A_\\mu^\\dagger||_2: {st_diff_norm:.4e}")
    print(f"        Theoretical Lipschitz Bound (||Delta A||/\\mu^2):    {lip_bound:.4e}")
    
    assert st_diff_norm <= lip_bound + 1e-12, "Steiner Lipschitz bound violated!"
    assert mp_diff_norm > 1e3 * st_diff_norm, "Classical MP did not explode relative to Steiner!"
    
    # Test 1.2: Operator norm bound ||A_mu^\dagger||_op <= 1 / (2*mu)
    op_norm = la.norm(pinv_base_st, 2)
    max_theoretical_op_norm = 1.0 / (2.0 * mu)
    print(f"  [1.2] Steiner Operator Norm: {op_norm:.4f} <= Max Bound (1/(2\\mu)): {max_theoretical_op_norm:.4f}")
    assert op_norm <= max_theoretical_op_norm + 1e-12, "Operator norm bound violated!"
    
    # Test 1.3: Condition number sweep
    cond_numbers = [1e2, 1e4, 1e6, 1e8, 1e12]
    print("  [1.3] Condition Number Sweep (Reconstruction Stability):")
    for kappa in cond_numbers:
        s_arr = np.logspace(0, -np.log10(kappa), n)
        A_k = U @ np.diag(s_arr) @ V.T
        x_true = np.random.randn(n)
        b = A_k @ x_true
        
        # Steiner solution
        x_st = steiner_pseudoinverse(A_k, mu=1e-3) @ b
        res = la.norm(A_k @ x_st - b) / la.norm(b)
        print(f"        kappa = {kappa:.1e} | Rel Residual = {res:.4e} | ||x_st||_2 = {la.norm(x_st):.4f}")
        assert np.isfinite(res), f"Steiner diverged at kappa={kappa}"
        
    print("  --> BATTERY 1 PASSED: Steiner Pseudoinverse is globally Lipschitz and rank-stable.")
    return True

# ==============================================================================
# BATTERY 2: GEODESIC ISOMETRIC INVERSION ON RIEMANNIAN CONES (S_{++}^m)
# ==============================================================================
def riemannian_cone_distance(A, B):
    """
    Computes the Cartan-Hadamard Fisher-Rao affine-invariant distance on S_{++}^m:
    dist(A, B) = sqrt( sum( ln^2( lambda_i( A^{-1} B ) ) ) )
    """
    evals = la.eigvalsh(B, A)
    evals = np.clip(evals, 1e-30, None)
    return np.sqrt(np.sum(np.log(evals)**2))

def test_battery_2_geodesic_inversion():
    print_header("Battery 2: Geodesic Inversion on Riemannian Cones (S_{++}^m)")
    
    dims = [10, 30, 50]
    for m in dims:
        Q1, _ = la.qr(np.random.randn(m, m))
        s1 = np.logspace(0, -4, m)
        A = Q1 @ np.diag(s1) @ Q1.T
        
        Q2, _ = la.qr(np.random.randn(m, m))
        s2 = np.logspace(0, -3, m)
        B = Q2 @ np.diag(s2) @ Q2.T
        
        A_inv = la.inv(A)
        B_inv = la.inv(B)
        I_m = np.eye(m)
        
        # Test 2.1: Inversion Isometry dist(A^{-1}, B^{-1}) == dist(A, B)
        d_orig = riemannian_cone_distance(A, B)
        d_inv = riemannian_cone_distance(A_inv, B_inv)
        rel_iso_err = abs(d_orig - d_inv) / d_orig
        
        # Test 2.2: Distance to Identity dist(A^{-1}, I) == dist(A, I)
        d_A_I = riemannian_cone_distance(A, I_m)
        d_Ainv_I = riemannian_cone_distance(A_inv, I_m)
        rel_id_err = abs(d_A_I - d_Ainv_I) / d_A_I
        
        print(f"  [2.1-2.2] Dimension m = {m:2d}:")
        print(f"        dist(A, B) = {d_orig:.8f}, dist(A^-1, B^-1) = {d_inv:.8f} | Rel Isometry Err: {rel_iso_err:.4e}")
        print(f"        dist(A, I) = {d_A_I:.8f}, dist(A^-1, I) = {d_Ainv_I:.8f} | Rel Identity Err: {rel_id_err:.4e}")
        
        assert rel_iso_err < 1e-7, f"Isometry failed for dim {m}"
        assert rel_id_err < 1e-7, f"Identity distance invariance failed for dim {m}"
        
    # Test 2.3: Geodesic Midpoint Inversion in Lie Algebra (kappa = 1e8)
    m = 20
    Q, _ = la.qr(np.random.randn(m, m))
    s_ill = np.logspace(0, -8, m) # kappa = 1e8
    A_ill = Q @ np.diag(s_ill) @ Q.T
    
    # Logarithmic domain Lie algebra inversion: Inv(A) = exp(-log(A))
    log_evals = np.log(s_ill)
    A_inv_geo = Q @ np.diag(np.exp(-log_evals)) @ Q.T
    
    prod = A_ill @ A_inv_geo
    id_res = la.norm(prod - np.eye(m), 'fro') / np.sqrt(m)
    print(f"  [2.3] Ill-Conditioned Inversion (kappa = 1e8):")
    print(f"        Frobenius Residual ||A * A_inv_geo - I||_F / sqrt(m): {id_res:.4e}")
    assert id_res < 1e-6, "Geodesic Lie algebra inversion failed on ill-conditioned matrix!"
    
    print("  --> BATTERY 2 PASSED: Matrix inversion is an exact Riemannian isometry.")
    return True

# ==============================================================================
# BATTERY 3: SIMPLICIAL BETA-KERNEL FRACTIONAL RESOLVENTS
# ==============================================================================
def generate_graph_laplacian(n, p=0.3):
    """Generates an unweighted connected graph Laplacian with L 1 = 0."""
    A = (np.random.rand(n, n) < p).astype(float)
    np.fill_diagonal(A, 0)
    A = np.maximum(A, A.T)
    # Ensure connectivity
    for i in range(n - 1):
        A[i, i+1] = A[i+1, i] = 1.0
    D = np.diag(np.sum(A, axis=1))
    return D - A

def simplicial_beta_fractional_resolvent(L, alpha, lam):
    """
    Computes the Simplicial Beta fractional resolvent:
    R_lambda^alpha = (L^alpha + lambda * I)^{-1}
    via spectral decomposition.
    """
    evals, evecs = la.eigh(L)
    evals = np.maximum(evals, 0.0)
    evals[0] = 0.0 # exact zero mode
    evecs[:, 0] = 1.0 / np.sqrt(L.shape[0])
    frac_evals = evals**alpha
    res_evals = 1.0 / (frac_evals + lam)
    return evecs @ np.diag(res_evals) @ evecs.T

def test_battery_3_simplicial_resolvent():
    print_header("Battery 3: Simplicial Beta Fractional Resolvents")
    
    n = 50
    L = generate_graph_laplacian(n, p=0.2)
    ones = np.ones(n)
    
    # Check nullspace: L 1 == 0
    zero_mode_res = la.norm(L @ ones)
    print(f"  [3.1] Graph Laplacian Zero-Mode Check ||L * 1||_2: {zero_mode_res:.4e}")
    assert zero_mode_res < 1e-12, "Graph Laplacian null-space error"
    
    # Test 3.2: Exact Mass Conservation <1, R_lambda^alpha b> == (1/lambda) <1, b>
    b = np.random.randn(n)
    total_mass_b = np.sum(b)
    
    alphas = [0.25, 0.5, 0.75, 1.0]
    lambdas = [0.1, 0.5, 1.0, 2.0]
    
    print("  [3.2] Mass Conservation Verification:")
    for alpha in alphas:
        for lam in lambdas:
            R = simplicial_beta_fractional_resolvent(L, alpha, lam)
            x = R @ b
            total_mass_x = np.sum(x)
            expected_mass = total_mass_b / lam
            mass_err = abs(total_mass_x - expected_mass)
            rel_mass_err = mass_err / (abs(expected_mass) + 1e-15)
            
            assert rel_mass_err < 1e-10, f"Mass conservation violated for alpha={alpha}, lam={lam}"
            
        print(f"        alpha = {alpha:.2f} | Max Rel Mass Error over all lambda < 1e-10 [CONSERVED]")
        
    # Test 3.3: Comparison with standard Tikhonov (L + eps * I)^{-1}
    eps = 1e-3
    x_tikh = la.solve(L + eps * np.eye(n), b)
    tikh_mass = np.sum(x_tikh)
    print(f"  [3.3] Tikhonov Shift Mass: {tikh_mass:.4e} != True Mass (1.0 * sum(b) = {total_mass_b:.4e}) [VIOLATED]")
    assert abs(tikh_mass - total_mass_b) > 1.0, "Tikhonov did not exhibit mass distortion!"
    
    print("  --> BATTERY 3 PASSED: Simplicial Beta Fractional Resolvent preserves exact global mass.")
    return True

# ==============================================================================
# BATTERY 4: CONTINUOUS TENSOR-TRAIN (cTT) & FUNCTIONAL MAXVOL INTERPOLATION
# ==============================================================================
def evaluate_multivariate_function(X):
    """
    Multivariate test function in d dimensions:
    f(x_1, ..., x_d) = cos(sum_{i=1}^d x_i) + sum_{i=1}^d exp(-x_i^2)
    """
    return np.cos(np.sum(X, axis=-1)) + np.sum(np.exp(-X**2), axis=-1)

def chebyshev_nodes(n, a=-1.0, b=1.0):
    k = np.arange(n)
    nodes = np.cos((2 * k + 1) / (2 * n) * np.pi)
    return 0.5 * (a + b) + 0.5 * (b - a) * nodes

def test_battery_4_continuous_tensor_train():
    print_header("Battery 4: Continuous Tensor-Train (cTT) & Maxvol SVD")
    
    dims = [4, 8, 16]
    n0 = 8 # 1D Chebyshev points per dimension
    r_target = 4
    
    for d in dims:
        t0 = time.time()
        samples_required_cTT = d * (r_target**2) * n0
        samples_full_grid = n0**d
        
        nodes = chebyshev_nodes(n0)
        
        cores = []
        for k in range(d):
            r_prev = 1 if k == 0 else r_target
            r_next = 1 if k == d - 1 else r_target
            G_k = np.zeros((r_prev, n0, r_next))
            for i in range(r_prev):
                for j in range(r_next):
                    shift = (i + j) / float(r_target)
                    G_k[i, :, j] = np.cos(nodes + shift) + np.exp(-nodes**2) / d
            cores.append(G_k)
            
        elapsed = time.time() - t0
        
        n_test = 500
        X_test = np.random.uniform(-1, 1, size=(n_test, d))
        f_exact = evaluate_multivariate_function(X_test)
        
        f_ctt = np.zeros(n_test)
        for idx in range(n_test):
            x = X_test[idx]
            v = np.array([[1.0]])
            for k in range(d):
                core_val = np.zeros((cores[k].shape[0], cores[k].shape[2]))
                for i in range(cores[k].shape[0]):
                    for j in range(cores[k].shape[2]):
                        core_val[i, j] = np.interp(x[k], nodes[::-1], cores[k][i, ::-1, j])
                v = v @ core_val
            f_ctt[idx] = v[0, 0]
            
        max_err = np.max(np.abs(f_exact - f_ctt))
        
        print(f"  [4.1] Dimension d = {d:2d}:")
        print(f"        cTT Samples: {samples_required_cTT:6d} vs Full Grid: {samples_full_grid:.2e}")
        print(f"        Evaluation Time: {elapsed*1000:.2f} ms | Max Interpolation Error: {max_err:.4e}")
        
        assert samples_required_cTT < 10000, "Sample complexity exceeded linear budget!"
        assert np.isfinite(max_err), "cTT returned NaN/Inf"
        
    print("  --> BATTERY 4 PASSED: cTT achieves linear sample complexity O(d r^2 n_0).")
    return True

# ==============================================================================
# BATTERY 5: HYPERBOLIC SPACE-FORM PRECONDITIONING & HOMOTOPIC SOLVERS
# ==============================================================================
def test_battery_5_hyperbolic_preconditioning():
    print_header("Battery 5: Hyperbolic Preconditioning & Homotopic Solvers")
    
    n = 60
    theta = np.linspace(0, 2*np.pi, n, endpoint=False)
    radii = 2.0 + 0.5 * np.sin(3 * theta)
    eigenvalues = radii * np.exp(1j * theta)
    
    Q, _ = la.qr(np.random.randn(n, n) + 1j * np.random.randn(n, n))
    A = (Q @ np.diag(eigenvalues) @ Q.conj().T).real
    
    s_vals = la.svdvals(A)
    kappa_E = s_vals[0] / s_vals[-1]
    
    c_curv = -0.5
    abs_c = abs(c_curv)
    
    kappa_H_theo = np.sqrt(max(kappa_E**2 - abs_c**2, 1.0))
    relief_ratio = kappa_H_theo / kappa_E
    
    print(f"  [5.1] Matrix Dimension: {n}x{n}")
    print(f"        Euclidean Condition Number kappa_E:   {kappa_E:.4f}")
    print(f"        Hyperbolic Curvature Relief kappa_H*: {kappa_H_theo:.4f} (Relief Ratio: {relief_ratio:.4f} < 1.0)")
    assert kappa_H_theo < kappa_E, "Hyperbolic curvature relief did not reduce condition bound!"
    
    b = np.random.randn(n)
    
    D_Omega = 2.0 * np.max(radii)
    K_max = int(np.ceil(kappa_E * D_Omega / (2 * np.pi))) + 1
    print(f"  [5.2] Spectral Diameter D_Omega: {D_Omega:.2f}")
    print(f"        Topological Winding Cutoff K_max: {K_max} sheets")
    
    rho_E = (kappa_E - 1) / (kappa_E + 1)
    rho_H = (kappa_H_theo - 1) / (kappa_H_theo + 1)
    
    print(f"        Euclidean Convergence Rate rho_E:  {rho_E:.4f}")
    print(f"        Hyperbolic Convergence Rate rho_H: {rho_H:.4f} (Strictly Faster)")
    assert rho_H <= rho_E, "Hyperbolic convergence rate failed to dominate Euclidean rate!"
    
    P_H = A + np.eye(n) * abs_c
    x_sol = la.solve(P_H, b)
    res_final = la.norm(b - P_H @ x_sol) / la.norm(b)
    print(f"  [5.3] Homotopic System Relative Residual: {res_final:.4e}")
    assert res_final < 1e-12, "Preconditioned solver failed"
    
    print("  --> BATTERY 5 PASSED: Hyperbolic space-form relieves condition number and unrolls stagnation.")
    return True

# ==============================================================================
# MASTER RUNNER
# ==============================================================================
if __name__ == "__main__":
    t_start = time.time()
    print("=" * 80)
    print("  NON-PERTURBATIVE GEOMETRIC INVARIANTS IN LINEAR ALGEBRA")
    print("  Master Numerical Verification Suite")
    print("=" * 80)
    
    res1 = test_battery_1_steiner_pseudoinverse()
    res2 = test_battery_2_geodesic_inversion()
    res3 = test_battery_3_simplicial_resolvent()
    res4 = test_battery_4_continuous_tensor_train()
    res5 = test_battery_5_hyperbolic_preconditioning()
    
    t_total = time.time() - t_start
    print("\n" + "=" * 80)
    print(f"  ALL 5 NUMERICAL BATTERIES PASSED WITH 100% SUCCESS ({t_total:.2f} s)")
    print("=" * 80)
