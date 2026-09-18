"""
NUMERICAL VERIFICATION BATTERIES: PILLAR 06
Spatiotemporal Epidemiology, Fractional Laplacians & Wastewater Early Warning
Theoretical Grounding: Treatise Chapters 04 & 11
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np
from model_engine import FractionalEpidemiologyEngine

def run_all_batteries():
    print("=" * 85)
    print("PILLAR 06 TROPICAL VERIFICATION: FRACTIONAL METAPOPULATION EPIDEMIOLOGY")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | Chapters 04 & 11")
    print("=" * 85)

    n_nodes = 20
    engine = FractionalEpidemiologyEngine(n_nodes=n_nodes, alpha=0.70)
    all_passed = True

    # Construct synthetic 2-cluster network with a single bridge
    np.random.seed(42)
    adj = np.zeros((n_nodes, n_nodes))
    # Cluster 1: nodes 0..9
    for i in range(10):
        for j in range(i + 1, 10):
            if np.random.rand() < 0.6:
                adj[i, j] = adj[j, i] = 1.0
    # Cluster 2: nodes 10..19
    for i in range(10, 20):
        for j in range(i + 1, 20):
            if np.random.rand() < 0.6:
                adj[i, j] = adj[j, i] = 1.0
    # Long-range transmission bottleneck bridge between node 4 and node 15
    adj[4, 15] = adj[15, 4] = 1.0

    # ---------------------------------------------------------
    # Battery 1: Fractional Graph Laplacian Positive Semi-Definiteness
    # ---------------------------------------------------------
    print("\n[BATTERY 1/5] Fractional Laplacian Semi-Definiteness and Nullspace...")
    L, L_norm = engine.construct_mobility_laplacian(adj)
    L_alpha, eig_frac = engine.compute_fractional_laplacian(L_norm)
    
    min_eig = np.min(eig_frac)
    symm_error = np.linalg.norm(L_alpha - L_alpha.T)
    
    print(f"  -> Minimum Fractional Eigenvalue: {min_eig:.4e}")
    print(f"  -> Symmetry Violation ||L^alpha - (L^alpha)^T||: {symm_error:.2e}")
    
    if min_eig >= -1e-12 and symm_error < 1e-12:
        print("  -> RESULT: PASSED (Battery 1)")
    else:
        print("  -> RESULT: FAILED (Battery 1)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 2: Anomalous Power-Law Diffusion vs Classical Heat Diffusion
    # ---------------------------------------------------------
    print("\n[BATTERY 2/5] Anomalous Fractional Super-Diffusion vs Local Diffusion...")
    # Compare heat kernel propagator: e^{-t L} vs e^{-t L^alpha}
    t_diff = 1.5
    prop_classic = np.linalg.matrix_power(np.eye(n_nodes) - 0.1 * L_norm, 10)
    prop_frac = np.linalg.matrix_power(np.eye(n_nodes) - 0.1 * L_alpha, 10)
    
    # Distance between distant nodes (node 0 and node 19)
    transfer_classic = prop_classic[0, 19]
    transfer_frac = prop_frac[0, 19]
    
    print(f"  -> Classical Local 10-step Transfer (0 -> 19):  {transfer_classic:.4e}")
    print(f"  -> Fractional Non-Local Transfer (0 -> 19):     {transfer_frac:.4e}")
    
    # Fractional propagator must exhibit significantly heavier tail transfer
    if transfer_frac > transfer_classic:
        print("  -> RESULT: PASSED (Battery 2)")
    else:
        print("  -> RESULT: FAILED (Battery 2)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 3: Ollivier-Ricci Curvature Bottleneck Detection
    # ---------------------------------------------------------
    print("\n[BATTERY 3/5] Ollivier-Ricci Curvature & Bottleneck Bridge Identification...")
    # Intra-cluster edge (e.g. 1-2) vs Inter-cluster bridge (4-15)
    kappa_intra = engine.compute_ollivier_ricci_curvature(adj, 1, 2)
    kappa_bridge = engine.compute_ollivier_ricci_curvature(adj, 4, 15)
    
    print(f"  -> Intra-Cluster Edge Curvature kappa_OR(1, 2):   {kappa_intra:+.4f}")
    print(f"  -> Inter-Cluster Bridge Curvature kappa_OR(4, 15): {kappa_bridge:+.4f}")
    
    # Bottleneck bridge must have distinctly lower/negative curvature than tightly coupled cluster
    if kappa_bridge < kappa_intra and kappa_bridge <= 0.0:
        print("  -> RESULT: PASSED (Battery 3)")
    else:
        print("  -> RESULT: FAILED (Battery 3)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 4: Wastewater Deconvolution Inversion Accuracy
    # ---------------------------------------------------------
    print("\n[BATTERY 4/5] Wastewater Metagenomic Resolvent Deconvolution...")
    T = 30
    true_burden = np.exp(-0.5 * ((np.arange(T) - 14) / 4.0)**2)
    delay_kernel = np.array([0.4, 0.35, 0.15, 0.10])
    convolved = np.convolve(true_burden, delay_kernel)[:T]
    noisy_wastewater = convolved + np.random.normal(0, 0.02, T)
    
    recovered_burden = engine.deconvolve_wastewater_signal(noisy_wastewater, delay_kernel)
    reconstruction_corr = np.corrcoef(true_burden, recovered_burden)[0, 1]
    
    print(f"  -> True vs Recovered Signal Pearson Correlation: r = {reconstruction_corr:.4f}")
    if reconstruction_corr > 0.95:
        print("  -> RESULT: PASSED (Battery 4)")
    else:
        print("  -> RESULT: FAILED (Battery 4)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 5: Early Warning Lead-Time Discrimination
    # ---------------------------------------------------------
    print("\n[BATTERY 5/5] Outbreak Early Warning Index (Subcritical vs Supercritical)...")
    # Subcritical regime: low infection
    I_sub = np.full(n_nodes, 0.01)
    lambda_sub, ewi_sub = engine.compute_early_warning_index(I_sub, L_alpha)
    
    # Supercritical regime: sudden localized surge (seed in node 4)
    I_super = np.copy(I_sub)
    I_super[4] = 0.65
    lambda_super, ewi_super = engine.compute_early_warning_index(I_super, L_alpha)
    
    print(f"  -> Subcritical Regime:   lambda_max = {lambda_sub:+.4f} | EWI = {ewi_sub:.4f}")
    print(f"  -> Supercritical Regime: lambda_max = {lambda_super:+.4f} | EWI = {ewi_super:.4f}")
    
    if ewi_sub < 0.20 and ewi_super > 0.80:
        print("  -> RESULT: PASSED (Battery 5)")
    else:
        print("  -> RESULT: FAILED (Battery 5)")
        all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("PILLAR 06 TROPICAL VERIFICATION SUMMARY: 5/5 BATTERIES PASSED (0 FAILURES)")
    else:
        print("PILLAR 06 TROPICAL VERIFICATION SUMMARY: TESTS FAILED")
    print("=" * 85)
    return all_passed

if __name__ == '__main__':
    run_all_batteries()
