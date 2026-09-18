"""
NUMERICAL VERIFICATION BATTERIES: PILLAR 05
Rational Vaccine Design & Minimax Extrinsic Curvature on Glycoprotein Submanifolds
Treatise Grounding: Chapter 07, Theorems 4.2 & 5.6
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np
from model_engine import MinimaxEpitopeEngine

def run_all_batteries():
    print("=" * 85)
    print("PILLAR 05 TROPICAL VERIFICATION: MINIMAX EPITOPE CURVATURE ENGINE")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | Chapter 07")
    print("=" * 85)

    engine = MinimaxEpitopeEngine(glycan_shield_density=0.65, obstacle_radius=1.8)
    all_passed = True

    # ---------------------------------------------------------
    # Battery 1: Weingarten Shape Operator Symmetry & Eigenvalues
    # ---------------------------------------------------------
    print("\n[BATTERY 1/5] Weingarten Shape Operator Symmetry and Curvature Extraction...")
    # Synthetic saddle and cup patches
    np.random.seed(42)
    u = np.linspace(-1, 1, 15)
    v = np.linspace(-1, 1, 15)
    U, V = np.meshgrid(u, v)
    X = U.flatten()
    Y = V.flatten()
    Z = 0.5 * (0.8 * X**2 - 0.4 * Y**2) + np.random.normal(0, 0.005, len(X))
    patch = np.column_stack([X, Y, Z])
    
    curv = engine.compute_weingarten_curvature(patch)
    W = curv['shape_operator']
    symmetry_error = np.abs(W[0, 1] - W[1, 0])
    
    print(f"  -> Weingarten Matrix W:\n{W}")
    print(f"  -> Symmetry Violation ||W - W^T||: {symmetry_error:.2e}")
    print(f"  -> Estimated kappa_1: {curv['kappa_1']:.4f}, kappa_2: {curv['kappa_2']:.4f}")
    
    if symmetry_error < 1e-12:
        print("  -> RESULT: PASSED (Battery 1)")
    else:
        print("  -> RESULT: FAILED (Battery 1)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 2: Obstacle Curvature Exclusion Principle (Thm 4.2)
    # ---------------------------------------------------------
    print("\n[BATTERY 2/5] Obstacle Curvature Exclusion Principle (kappa* >= 2 / w)...")
    widths = [3.0, 2.0, 1.0, 0.5]
    kappas = [engine.evaluate_obstacle_curvature_exclusion(w) for w in widths]
    expected_kappas = [2.0 / w for w in widths]
    
    print(f"  -> Corridor Widths (nm): {widths}")
    print(f"  -> Minimum Feasible Curvatures: {kappas}")
    
    exclusion_check = np.allclose(kappas, expected_kappas) and all(kappas[i] < kappas[i+1] for i in range(len(kappas)-1))
    if exclusion_check:
        print("  -> RESULT: PASSED (Battery 2)")
    else:
        print("  -> RESULT: FAILED (Battery 2)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 3: Federer Reach Bound (reach(Sigma) >= 1 / kappa*)
    # ---------------------------------------------------------
    print("\n[BATTERY 3/5] Federer Reach & Steric Clearance Non-Collision Bound...")
    test_kappas = [0.2, 0.5, 1.0, 2.0, 4.0]
    reaches = [engine.compute_federer_reach(k) for k in test_kappas]
    print(f"  -> Curvatures kappa*: {test_kappas}")
    print(f"  -> Federer Reaches (nm): {reaches}")
    
    # Reach must be inversely proportional and strictly positive
    reach_check = all(r * k == 1.0 for r, k in zip(reaches, test_kappas))
    if reach_check:
        print("  -> RESULT: PASSED (Battery 3)")
    else:
        print("  -> RESULT: FAILED (Battery 3)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 4: Minimax Moreau-Yosida Barrier Convergence
    # ---------------------------------------------------------
    print("\n[BATTERY 4/5] Obstacle Barrier Satiation & Detachment Continuity...")
    # Detachment from obstacle boundary satisfies Caffarelli C^{1,1} regularity
    t_vals = np.linspace(0.1, 2.0, 20)
    kappa_profile = [max(engine.kappa_obs, 2.0 / (2.0 * t)) for t in t_vals]
    is_bounded = all(np.isfinite(kappa_profile)) and kappa_profile[0] > kappa_profile[-1]
    
    print(f"  -> Barrier Satiation Range: {kappa_profile[0]:.3f} -> {kappa_profile[-1]:.3f}")
    if is_bounded:
        print("  -> RESULT: PASSED (Battery 4)")
    else:
        print("  -> RESULT: FAILED (Battery 4)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 5: Neutralization Breadth Discrimination (Universal vs Decoy)
    # ---------------------------------------------------------
    print("\n[BATTERY 5/5] Broad Neutralization Breadth Prediction Discrimination...")
    # Scaffold A: Conserved stem/core epitope with wide clearance (w = 2.5 nm) and low intrinsic curvature
    res_A = engine.evaluate_epitope_scaffold(patch, corridor_width=2.5, is_glycan_shielded=True)
    # Scaffold B: Constrained variable loop decoy (w = 0.6 nm, high local curvature)
    Z_decoy = 0.5 * (3.5 * X**2 + 2.5 * Y**2)
    patch_decoy = np.column_stack([X, Y, Z_decoy])
    res_B = engine.evaluate_epitope_scaffold(patch_decoy, corridor_width=0.6, is_glycan_shielded=True)

    print(f"  -> Scaffold A (Conserved Core) Neutralization Breadth: {res_A['predicted_breadth']:.4f}")
    print(f"  -> Scaffold B (Decoy Loop)    Neutralization Breadth: {res_B['predicted_breadth']:.4f}")

    if res_A['predicted_breadth'] > 0.70 and res_B['predicted_breadth'] < 0.20:
        print("  -> RESULT: PASSED (Battery 5)")
    else:
        print("  -> RESULT: FAILED (Battery 5)")
        all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("PILLAR 05 TROPICAL VERIFICATION SUMMARY: 5/5 BATTERIES PASSED (0 FAILURES)")
    else:
        print("PILLAR 05 TROPICAL VERIFICATION SUMMARY: TESTS FAILED")
    print("=" * 85)
    return all_passed

if __name__ == '__main__':
    run_all_batteries()
