"""
NUMERICAL VERIFICATION BATTERIES: PILLAR 01 (Quantum Pharmacology)
Undruggable Targets, Minimax Extrinsic Curvature & Stapled Peptidomimetics
Theoretical Grounding: Treatise Chapter 07
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np
from model_engine import UndruggablePeptidomimeticEngine

def run_all_batteries():
    print("=" * 85)
    print("PILLAR 01 PHARMACOLOGY VERIFICATION: UNDRUGGABLE TARGETS & PEPTIDOMIMETICS")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | Chapter 07")
    print("=" * 85)

    engine = UndruggablePeptidomimeticEngine(target_name="KRAS_G12D", interface_area_angstrom2=1200.0)
    all_passed = True

    # Construct synthetic flat PPI interface patch (KRAS Switch-II groove)
    np.random.seed(42)
    u = np.linspace(-5, 5, 15)
    v = np.linspace(-5, 5, 15)
    U, V = np.meshgrid(u, v)
    X = U.flatten()
    Y = V.flatten()
    # Very low curvature (flat interface): z ~ 0.01 x^2
    Z = 0.5 * (0.02 * X**2 + 0.01 * Y**2) + np.random.normal(0, 0.01, len(X))
    patch = np.column_stack([X, Y, Z])
    
    # Surrounding steric obstacles (sidechain atoms of adjacent loops)
    obstacles = np.array([
        [10.0, 10.0, 2.0],
        [-10.0, -10.0, 2.0],
        [8.0, -8.0, 3.0]
    ])

    # ---------------------------------------------------------
    # Battery 1: Weingarten Shape Operator Symmetry on PPI
    # ---------------------------------------------------------
    print("\n[BATTERY 1/5] Weingarten Shape Operator Symmetry on Flat PPI Manifold...")
    W, k1, k2, k_max = engine.compute_weingarten_ppi_curvature(patch)
    symm_err = np.abs(W[0, 1] - W[1, 0])
    
    print(f"  -> Shape Operator Matrix W:\n{W}")
    print(f"  -> Symmetry Violation ||W - W^T||: {symm_err:.2e}")
    print(f"  -> Flat PPI Peak Curvature kappa*: {k_max:.4f} Angstrom^{{-1}}")
    
    if symm_err < 1e-12 and k_max < 0.10:
        print("  -> RESULT: PASSED (Battery 1)")
    else:
        print("  -> RESULT: FAILED (Battery 1)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 2: Moreau-Yosida Steric Barrier Boundedness
    # ---------------------------------------------------------
    print("\n[BATTERY 2/5] Moreau-Yosida Steric Exclusion Barrier Continuity...")
    # Safe trajectory vs clashing trajectory
    safe_traj = np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 0.5]])
    clash_traj = np.array([[10.0, 10.0, 1.8], [9.9, 9.9, 1.9]]) # penetrates obstacle #0
    
    p_safe = engine.evaluate_moreau_yosida_obstacle_barrier(safe_traj, obstacles)
    p_clash = engine.evaluate_moreau_yosida_obstacle_barrier(clash_traj, obstacles)
    
    print(f"  -> Safe Trajectory Steric Penalty:     {p_safe:.4f}")
    print(f"  -> Penetrating Trajectory Penalty:     {p_clash:.4f}")
    
    if p_safe == 0.0 and p_clash > 0.0 and np.isfinite(p_clash):
        print("  -> RESULT: PASSED (Battery 2)")
    else:
        print("  -> RESULT: FAILED (Battery 2)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 3: Macrocyclic Staple Curvature vs Linker Length
    # ---------------------------------------------------------
    print("\n[BATTERY 3/5] Staple Minimax Curvature kappa* Monotonicity with Length...")
    lengths = [8, 10, 12, 14, 16]
    kappas = [engine.optimize_minimax_staple(linker_length_atoms=L)[0] for L in lengths]
    
    print(f"  -> Linker Lengths (atoms): {lengths}")
    print(f"  -> Minimax Curvatures kappa*: {[round(k, 4) for k in kappas]}")
    
    is_strictly_decreasing = all(kappas[i] > kappas[i+1] for i in range(len(kappas)-1))
    if is_strictly_decreasing:
        print("  -> RESULT: PASSED (Battery 3)")
    else:
        print("  -> RESULT: FAILED (Battery 3)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 4: Buried SASA & Free Energy Scaling
    # ---------------------------------------------------------
    print("\n[BATTERY 4/5] Buried Surface Area (SASA) and Binding Energy Scaling...")
    res = engine.predict_binding_affinity_and_degradation(patch, obstacles, linker_length=12)
    sasa = res['buried_sasa_A2']
    delta_g = res['delta_g_kcal_mol']
    
    print(f"  -> Buried SASA:               {sasa:.1f} Angstrom^2")
    print(f"  -> Free Energy of Binding:    {delta_g:.2f} kcal/mol")
    print(f"  -> Predicted Dissociation Kd: {res['kd_nM']:.4e} nM")
    
    if sasa > 1000.0 and delta_g < -12.0:
        print("  -> RESULT: PASSED (Battery 4)")
    else:
        print("  -> RESULT: FAILED (Battery 4)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 5: Picomolar Affinity Discrimination (Stapled vs Clashed)
    # ---------------------------------------------------------
    print("\n[BATTERY 5/5] Potent Nanomolar Peptidomimetic Discrimination...")
    # Potent stapled macrocycle (clash-free)
    res_potent = engine.predict_binding_affinity_and_degradation(patch, obstacles, linker_length=12)
    # Inactive decoy (clashes heavily with steric obstacles along staple trajectory)
    # Staple semicircle is in x-y plane with radius r ~ 5.88 Angstrom
    clashing_obstacles = np.array([[0.0, 5.88, 0.0], [4.15, 4.15, 0.0]]) # placed directly in the staple arc
    res_inactive = engine.predict_binding_affinity_and_degradation(patch, clashing_obstacles, linker_length=12)
    
    print(f"  -> Potent Peptidomimetic Binder Probability: {res_potent['prob_potent_binder']:.4f}")
    print(f"  -> Clashing Decoy Binder Probability:        {res_inactive['prob_potent_binder']:.4f}")
    
    if res_potent['prob_potent_binder'] > 0.85 and res_inactive['prob_potent_binder'] < 0.10:
        print("  -> RESULT: PASSED (Battery 5)")
    else:
        print("  -> RESULT: FAILED (Battery 5)")
        all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("PILLAR 01 PHARMACOLOGY SUMMARY: 5/5 BATTERIES PASSED (0 FAILURES)")
    else:
        print("PILLAR 01 PHARMACOLOGY SUMMARY: TESTS FAILED")
    print("=" * 85)
    return all_passed

if __name__ == '__main__':
    run_all_batteries()
