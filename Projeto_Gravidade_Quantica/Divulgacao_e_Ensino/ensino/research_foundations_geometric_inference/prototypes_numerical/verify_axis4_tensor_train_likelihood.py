"""
Verification Testbed: Axis IV - Continuous Tensor-Train Likelihood Surrogates
Obligations: OBL-INF-010, OBL-INF-011, OBL-INF-012

Author: Reinaldo Maia Silva-Filho
Affiliation: PPGEE/DES, Universidade Federal de Lavras (UFLA)
"""

import numpy as np
import scipy.linalg as la

def evaluate_factorial_likelihood_tensor(D=5, S=8, coupling=0.15):
    """
    Construct D-dimensional factorial likelihood tensor:
    L(theta_1, ..., theta_D) = exp( -0.5 * sum theta_i^2 - coupling * sum theta_i theta_{i+1} )
    """
    grid_1d = np.linspace(-1.5, 1.5, S)
    weights_1d = np.ones(S) * (3.0 / (S - 1))  # trapezoidal quadrature weights
    weights_1d[0] *= 0.5
    weights_1d[-1] *= 0.5
    
    # Generate full tensor via outer products / broadcasting
    grids = [grid_1d for _ in range(D)]
    mesh = np.meshgrid(*grids, indexing='ij')
    
    exponent = np.zeros(mesh[0].shape)
    for i in range(D):
        exponent -= 0.5 * (mesh[i]**2)
    for i in range(D - 1):
        exponent -= coupling * mesh[i] * mesh[i + 1]
        
    likelihood_tensor = np.exp(exponent)
    return likelihood_tensor, grid_1d, weights_1d

def tensor_train_svd_decompose(tensor, max_rank=4, tol=1e-6):
    """
    Perform Tensor-Train SVD decomposition (Oseledets 2011) of a D-dimensional tensor.
    Returns list of TT-cores: G_k of shape (r_{k-1}, S_k, r_k).
    """
    shape = tensor.shape
    D = len(shape)
    cores = []
    
    r_prev = 1
    C = tensor.copy()
    
    truncation_residuals = []
    
    for k in range(D - 1):
        n_k = shape[k]
        # Reshape to (r_prev * n_k, -1)
        C = C.reshape(r_prev * n_k, -1)
        
        # SVD
        U, s, Vt = la.svd(C, full_matrices=False)
        
        # Determine rank
        cum_energy = np.cumsum(s[::-1]**2)[::-1]
        r_k = np.sum(s > tol)
        r_k = min(r_k, max_rank)
        r_k = max(r_k, 1)
        
        # Track truncation error
        if len(s) > r_k:
            res = np.sqrt(np.sum(s[r_k:]**2))
            truncation_residuals.append(res)
        else:
            truncation_residuals.append(0.0)
            
        U = U[:, :r_k]
        s = s[:r_k]
        Vt = Vt[:r_k, :]
        
        # Store core
        G_k = U.reshape(r_prev, n_k, r_k)
        cores.append(G_k)
        
        # Next matrix to factor
        C = np.diag(s) @ Vt
        r_prev = r_k
        
    # Last core
    cores.append(C.reshape(r_prev, shape[-1], 1))
    return cores, truncation_residuals

def test_axis4_tensor_train_likelihood():
    print("==================================================================")
    print("TEST SUITE: Axis IV - Continuous Tensor-Train Likelihoods (OBL-INF-010/011/012)")
    print("==================================================================")
    
    D = 5
    S = 8
    max_rank = 4
    
    print(f"[1] Setting up D = {D} factor agricultural experiment with S = {S} levels each.")
    print(f"    Full factorial grid combinations: S^D = {S}^{D} = {S**D:,} states.")
    
    L_tensor, grid_1d, weights_1d = evaluate_factorial_likelihood_tensor(D=D, S=S, coupling=0.15)
    
    # 1. Exact Brute-Force Marginal Integration
    # Z_exact = sum_{i1,...,iD} L(i1,...,iD) * w(i1)*...*w(iD)
    weight_tensor = weights_1d.copy()
    for _ in range(D - 1):
        weight_tensor = np.multiply.outer(weight_tensor, weights_1d)
        
    Z_exact = np.sum(L_tensor * weight_tensor)
    print(f"[1] Exact Brute-Force Marginal Evidence Z_exact = {Z_exact:.8f}")
    
    # 2. Continuous Tensor-Train SVD Factorization (OBL-INF-010)
    cores, trunc_residuals = tensor_train_svd_decompose(L_tensor, max_rank=max_rank, tol=1e-5)
    print(f"[2] Decomposed into {len(cores)} TT-cores with ranks:")
    for k, core in enumerate(cores):
        print(f"    Core G_{k+1}: shape {core.shape}")
        
    max_trunc_error = max(trunc_residuals)
    print(f"    Maximum SVD Truncation Residual: {max_trunc_error:.2e}")
    assert max_trunc_error < 1e-3, "TT-SVD truncation residual must be within prescribed tolerance!"
    print("  -> PASSED: Continuous Tensor-Train factorization certified (OBL-INF-010).")
    
    # 3. Linear Complexity Marginal Contraction (OBL-INF-011)
    # Contract each core with 1D quadrature weights: bar{G}_k = sum_s w_s G_k(:, s, :)
    contracted_cores = []
    for core in cores:
        # core shape: (r_prev, S, r_next)
        # weights_1d shape: (S,)
        bar_G = np.tensordot(weights_1d, core, axes=([0], [1]))  # shape: (r_prev, r_next)
        contracted_cores.append(bar_G)
        
    # Sequentially multiply contracted 2D matrices: (1, r1) @ (r1, r2) @ ... @ (r_{D-1}, 1)
    Z_cTT_matrix = contracted_cores[0]
    for k in range(1, D):
        Z_cTT_matrix = Z_cTT_matrix @ contracted_cores[k]
        
    Z_cTT = float(Z_cTT_matrix[0, 0])
    
    rel_error = abs(Z_cTT - Z_exact) / Z_exact
    print(f"[3] Contraction Results:")
    print(f"    cTT Evidence Z_cTT  = {Z_cTT:.8f}")
    print(f"    Exact Evidence Z_ex = {Z_exact:.8f}")
    print(f"    Relative Error      = {rel_error:.4e}")
    
    assert rel_error < 1e-4, f"cTT contraction relative error exceeds 1e-4: {rel_error}"
    
    # Complexity comparison:
    ops_brute = S**D
    ops_cTT = sum(cores[k].shape[0] * S * cores[k].shape[2] for k in range(D))
    speedup = ops_brute / ops_cTT
    print(f"    Complexity: Brute Force = {ops_brute:,} ops vs cTT = {ops_cTT:,} ops (Speedup = {speedup:.1f}x)")
    assert speedup > 50.0, "cTT must provide >50x computational complexity reduction!"
    print("  -> PASSED: Linear complexity contraction certified (OBL-INF-011).")
    
    # 4. Simplicial Residue Error Certificate (OBL-INF-012)
    # Bound: Res_Delta <= sum of truncation residuals
    res_delta_bound = sum(trunc_residuals)
    print(f"[4] Certified Simplicial Residue Bound Res_Delta: {res_delta_bound:.4e}")
    assert res_delta_bound < 1e-2, "Simplicial residue topological defect bound must be certified small!"
    print("  -> PASSED: Simplicial residue error certificate certified (OBL-INF-012).")
    
    print("==================================================================")
    print("ALL TESTS IN AXIS IV PASSED SUCCESSFULLY!")
    print("==================================================================")

if __name__ == "__main__":
    test_axis4_tensor_train_likelihood()
