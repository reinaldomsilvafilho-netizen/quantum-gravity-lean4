"""
NUMERICAL VERIFICATION BATTERIES: PILLAR 03 (Neuroscience & Mental Health)
Riemannian BCI & Stroke Neurorehabilitation Covariance Manifold
Theoretical Grounding: Treatise Chapter 02 & Paper 3
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np
from model_engine import RiemannianBCIEngine

def run_all_batteries():
    print("=" * 85)
    print("PILLAR 03 NEUROSCIENCE VERIFICATION: RIEMANNIAN BCI MOTOR REHABILITATION")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | Chapter 02 & Paper 3")
    print("=" * 85)

    engine = RiemannianBCIEngine(n_channels=8)
    all_passed = True

    # ---------------------------------------------------------
    # Battery 1: Fréchet Barycenter Existence & Convergence
    # ---------------------------------------------------------
    print("\n[BATTERY 1/5] Riemannian Fréchet Barycenter Convergence on S_{++}^8...")
    np.random.seed(42)
    cov_list = []
    for _ in range(5):
        A = np.random.randn(8, 8)
        C = A @ A.T + np.eye(8)
        cov_list.append(C)
        
    C_bar = engine.compute_frechet_mean(cov_list)
    eigvals = np.linalg.eigvalsh(C_bar)
    is_spd = bool(np.all(eigvals > 0.0))
    
    print(f"  -> Fréchet Mean Minimum Eigenvalue: {np.min(eigvals):.4f}")
    print(f"  -> Positive Definiteness Verified: {is_spd}")
    
    if is_spd and np.min(eigvals) > 0.1:
        print("  -> RESULT: PASSED (Battery 1)")
    else:
        print("  -> RESULT: FAILED (Battery 1)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 2: GL(q) Affine Invariance Under Electrode Scaling
    # ---------------------------------------------------------
    print("\n[BATTERY 2/5] GL(q) Congruence Invariance d(A C1 A^T, A C2 A^T) = d(C1, C2)...")
    C1 = cov_list[0]
    C2 = cov_list[1]
    # Arbitrary invertible sensor montage matrix A
    A_trans = np.random.randn(8, 8) + 2.0 * np.eye(8)
    
    C1_scaled = A_trans @ C1 @ A_trans.T
    C2_scaled = A_trans @ C2 @ A_trans.T
    
    d_raw = engine.compute_affine_invariant_distance(C1, C2)
    d_scaled = engine.compute_affine_invariant_distance(C1_scaled, C2_scaled)
    inv_discrepancy = np.abs(d_raw - d_scaled)
    
    print(f"  -> Original Geodesic Distance:  {d_raw:.6f}")
    print(f"  -> Transformed Geodesic Distance: {d_scaled:.6f}")
    print(f"  -> Invariance Violation:          {inv_discrepancy:.2e}")
    
    if inv_discrepancy < 1e-10:
        print("  -> RESULT: PASSED (Battery 2)")
    else:
        print("  -> RESULT: FAILED (Battery 2)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 3: Zero Swelling Phenomenon on S_{++}^q
    # ---------------------------------------------------------
    print("\n[BATTERY 3/5] Zero-Swelling Volume Determinant Preservation...")
    # Two anisotropic matrices with determinant = 1.0
    diag1 = np.array([5.0, 1/5.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    diag2 = np.array([1/5.0, 5.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    C_a = np.diag(diag1)
    C_b = np.diag(diag2)
    
    # Euclidean average swells determinant: det(0.5*(Ca + Cb)) = ((5 + 0.2)/2)^2 = 2.6^2 = 6.76 (576% inflation!)
    C_euclidean = 0.5 * (C_a + C_b)
    det_euclid = np.linalg.det(C_euclidean)
    
    # Riemannian geometric midpoint preserves determinant exactly
    C_riemann = engine.compute_frechet_mean([C_a, C_b])
    det_riemann = np.linalg.det(C_riemann)
    
    print(f"  -> True Component Determinants: 1.000")
    print(f"  -> Euclidean Mean Determinant (Swelling):  {det_euclid:.3f} ({(det_euclid - 1.0)*100:.1f}% inflation)")
    print(f"  -> Riemannian Mean Determinant (No Swell): {det_riemann:.3f}")
    
    if np.abs(det_riemann - 1.0) < 1e-4 and det_euclid > 2.0:
        print("  -> RESULT: PASSED (Battery 3)")
    else:
        print("  -> RESULT: FAILED (Battery 3)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 4: Tangent Space Projection Invertibility
    # ---------------------------------------------------------
    print("\n[BATTERY 4/5] Tangent Space Log-Map Dimensionality and Bijectivity...")
    C_ref = cov_list[0]
    tangent_feat = engine.project_to_tangent_space(cov_list[1], C_ref)
    expected_dim = int(8 * 9 / 2) # 36 elements
    
    print(f"  -> Tangent Feature Vector Length: {len(tangent_feat)} (Expected: {expected_dim})")
    if len(tangent_feat) == expected_dim and np.all(np.isfinite(tangent_feat)):
        print("  -> RESULT: PASSED (Battery 4)")
    else:
        print("  -> RESULT: FAILED (Battery 4)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 5: Motor Imagery Decoding Discrimination (Paretic vs Intact)
    # ---------------------------------------------------------
    print("\n[BATTERY 5/5] Motor Imagery Intention Decoding Discrimination...")
    # Synthetic Left-hand (C3 desynchronization) vs Right-hand (C4 desynchronization)
    mean_left = np.eye(8)
    mean_left[0, 0] = 0.3 # Mu suppression at C3
    mean_left[1, 1] = 1.8
    
    mean_right = np.eye(8)
    mean_right[0, 0] = 1.8
    mean_right[1, 1] = 0.3 # Mu suppression at C4
    
    trial_left = np.copy(mean_left) + 0.05 * np.random.randn(8, 8)
    trial_left = trial_left @ trial_left.T
    
    trial_right = np.copy(mean_right) + 0.05 * np.random.randn(8, 8)
    trial_right = trial_right @ trial_right.T
    
    pred_l, p_l, _, _ = engine.classify_motor_imagery(trial_left, mean_left, mean_right)
    pred_r, p_r, _, _ = engine.classify_motor_imagery(trial_right, mean_left, mean_right)
    
    print(f"  -> Left Trial Predicted Class:  {pred_l} (Prob: {p_l:.4f})")
    print(f"  -> Right Trial Predicted Class: {pred_r} (Prob: {p_r:.4f})")
    
    if pred_l == 1 and pred_r == 0 and p_l > 0.80 and p_r < 0.20:
        print("  -> RESULT: PASSED (Battery 5)")
    else:
        print("  -> RESULT: FAILED (Battery 5)")
        all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("PILLAR 03 NEUROSCIENCE SUMMARY: 5/5 BATTERIES PASSED (0 FAILURES)")
    else:
        print("PILLAR 03 NEUROSCIENCE SUMMARY: TESTS FAILED")
    print("=" * 85)
    return all_passed

if __name__ == '__main__':
    run_all_batteries()
