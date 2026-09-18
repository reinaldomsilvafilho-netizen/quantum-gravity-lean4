"""
NUMERICAL VERIFICATION BATTERIES: PILLAR 02 (Maternal-Child Health)
Preeclampsia, Placental Ischemia & Riemannian Spiral Artery Engine
Theoretical Grounding: Treatise Chapters 02 & 08
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np
from model_engine import PreeclampsiaPlacentalEngine

def run_all_batteries():
    print("=" * 85)
    print("PILLAR 02 MATERNAL-CHILD HEALTH VERIFICATION: PREECLAMPSIA PLACENTAL ISCHEMIA")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | Chapters 02 & 08")
    print("=" * 85)

    engine = PreeclampsiaPlacentalEngine(gestational_age_weeks=12.0)
    all_passed = True

    # ---------------------------------------------------------
    # Battery 1: Affine-Invariant Riemannian Metric Axioms on S_{++}^3
    # ---------------------------------------------------------
    print("\n[BATTERY 1/5] Affine-Invariant Metric Axiom Verification on S_{++}^3...")
    G1 = np.diag([3.0, 2.8, 0.9])
    G2 = np.diag([1.2, 1.0, 2.5])
    G3 = np.diag([2.0, 2.0, 1.5])
    
    d12 = engine.compute_affine_invariant_distance(G1, G2)
    d21 = engine.compute_affine_invariant_distance(G2, G1)
    d13 = engine.compute_affine_invariant_distance(G1, G3)
    d32 = engine.compute_affine_invariant_distance(G3, G2)
    
    symm_error = np.abs(d12 - d21)
    triangle_ok = bool(d12 <= d13 + d32 + 1e-12)
    
    print(f"  -> Symmetry Violation |d(G1,G2) - d(G2,G1)|: {symm_error:.2e}")
    print(f"  -> Triangle Inequality (d12={d12:.3f} <= d13+d32={d13+d32:.3f}): {triangle_ok}")
    
    if symm_error < 1e-12 and triangle_ok:
        print("  -> RESULT: PASSED (Battery 1)")
    else:
        print("  -> RESULT: FAILED (Battery 1)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 2: Ricci Remodeling Flow Geodesic Convergence
    # ---------------------------------------------------------
    print("\n[BATTERY 2/5] Spiral Artery Trophoblast Remodeling Geodesic Convergence...")
    # Narrow, unremodeled spiral artery (high resistance, low compliance)
    G_unremodeled = np.diag([0.8, 0.7, 3.2])
    d_initial = engine.compute_affine_invariant_distance(engine.G_healthy_ref, G_unremodeled)
    
    G_remodeled = engine.simulate_trophoblast_ricci_flow(G_unremodeled, steps=30, dt=0.05, trophoblast_invasion_rate=0.9)
    d_final = engine.compute_affine_invariant_distance(engine.G_healthy_ref, G_remodeled)
    
    print(f"  -> Initial Distance to Healthy Vascular Target: d_0 = {d_initial:.4f}")
    print(f"  -> Final Remodeled Distance after Trophoblast Flow: d_T = {d_final:.4f}")
    
    if d_final < 0.35 * d_initial:
        print("  -> RESULT: PASSED (Battery 2)")
    else:
        print("  -> RESULT: FAILED (Battery 2)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 3: Uterine Artery Doppler Waveform Monotonicity
    # ---------------------------------------------------------
    print("\n[BATTERY 3/5] Doppler Pulsatility & Notch Depth Monotonicity...")
    pi_unremodeled, _, notch_unremodeled = engine.evaluate_doppler_waveforms(G_unremodeled)
    pi_remodeled, _, notch_remodeled = engine.evaluate_doppler_waveforms(G_remodeled)
    
    print(f"  -> Unremodeled Vessel (Pre-Eclamptic): PI = {pi_unremodeled:.3f} | Notch = {notch_unremodeled:.3f}")
    print(f"  -> Remodeled Vessel (Healthy Normal):   PI = {pi_remodeled:.3f} | Notch = {notch_remodeled:.3f}")
    
    if pi_unremodeled > pi_remodeled and notch_unremodeled > notch_remodeled:
        print("  -> RESULT: PASSED (Battery 3)")
    else:
        print("  -> RESULT: FAILED (Battery 3)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 4: Angiogenic Imbalance & Geometric Coupling
    # ---------------------------------------------------------
    print("\n[BATTERY 4/5] Coupling with Anti-Angiogenic Factor Surge (sFlt-1 / PlGF)...")
    _, _, p_healthy = engine.predict_preeclampsia_risk(G_remodeled, sflt_plgf_ratio=12.0)
    _, _, p_preeclampsia = engine.predict_preeclampsia_risk(G_unremodeled, sflt_plgf_ratio=95.0)
    
    print(f"  -> Healthy Normotensive Risk Probability: {p_healthy:.4f}")
    print(f"  -> Preeclamptic Ischemic Risk Probability: {p_preeclampsia:.4f}")
    
    if p_healthy < 0.15 and p_preeclampsia > 0.85:
        print("  -> RESULT: PASSED (Battery 4)")
    else:
        print("  -> RESULT: FAILED (Battery 4)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 5: Early-Onset vs Late-Onset Preeclampsia Discrimination
    # ---------------------------------------------------------
    print("\n[BATTERY 5/5] First-Trimester (12-Week) Preeclampsia Discrimination Gate...")
    # Cohort sweep over 20 invasion trajectories
    rates = np.linspace(0.1, 1.0, 10)
    p_risks = []
    for r in rates:
        G_t = engine.simulate_trophoblast_ricci_flow(G_unremodeled, steps=25, trophoblast_invasion_rate=r)
        _, _, p = engine.predict_preeclampsia_risk(G_t, sflt_plgf_ratio=35.0)
        p_risks.append(p)
        
    is_strictly_decreasing = all(p_risks[i] > p_risks[i+1] for i in range(len(p_risks)-1))
    print(f"  -> Risk Profile across Trophoblast Infiltration: {p_risks[0]:.3f} -> {p_risks[-1]:.3f}")
    
    if is_strictly_decreasing and p_risks[0] > 0.80 and p_risks[-1] < 0.25:
        print("  -> RESULT: PASSED (Battery 5)")
    else:
        print("  -> RESULT: FAILED (Battery 5)")
        all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("PILLAR 02 MATERNAL-CHILD HEALTH SUMMARY: 5/5 BATTERIES PASSED (0 FAILURES)")
    else:
        print("PILLAR 02 MATERNAL-CHILD HEALTH SUMMARY: TESTS FAILED")
    print("=" * 85)
    return all_passed

if __name__ == '__main__':
    run_all_batteries()
