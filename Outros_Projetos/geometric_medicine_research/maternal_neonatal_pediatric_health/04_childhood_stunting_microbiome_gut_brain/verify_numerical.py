"""
NUMERICAL VERIFICATION BATTERIES: PILLAR 04 (Maternal-Child Health)
Childhood Stunting, Microbiome Simplexes & Gut-Brain Axis IGF-1
Theoretical Grounding: Treatise Chapter 04 & Paper 2
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np
from model_engine import StuntingMicrobiomeEngine

def run_all_batteries():
    print("=" * 85)
    print("PILLAR 04 MATERNAL-CHILD HEALTH VERIFICATION: CHILDHOOD STUNTING & MICROBIOME")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | Chapter 04 & Paper 2")
    print("=" * 85)

    engine = StuntingMicrobiomeEngine()
    all_passed = True

    # ---------------------------------------------------------
    # Battery 1: Simplex Conservation and Metric Symmetry
    # ---------------------------------------------------------
    print("\n[BATTERY 1/5] Simplex Conservation sum(p) = 1 and Metric Symmetry...")
    p1 = engine.p_healthy_basin
    p2 = engine.p_stunted_basin
    
    sum1 = np.abs(np.sum(p1) - 1.0)
    sum2 = np.abs(np.sum(p2) - 1.0)
    d12 = engine.compute_bhattacharyya_distance(p1, p2)
    d21 = engine.compute_bhattacharyya_distance(p2, p1)
    
    print(f"  -> Normalization Sum Errors: {sum1:.2e}, {sum2:.2e}")
    print(f"  -> Metric Symmetry Discrepancy |d(p1,p2) - d(p2,p1)|: {abs(d12-d21):.2e}")
    print(f"  -> Inter-Basin Geodesic Separation: d = {d12:.4f} rad")
    
    if sum1 < 1e-12 and sum2 < 1e-12 and abs(d12 - d21) < 1e-12 and d12 > 0.5:
        print("  -> RESULT: PASSED (Battery 1)")
    else:
        print("  -> RESULT: FAILED (Battery 1)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 2: Ecological Bistable Attractor Convergence
    # ---------------------------------------------------------
    print("\n[BATTERY 2/5] Ecological Multi-Stability and Basin Trapping...")
    # Perturbed near healthy
    p_init_healthy = engine.project_to_simplex(engine.p_healthy_basin + np.random.normal(0, 0.02, 10))
    p_end_healthy = engine.simulate_microbiome_relaxation(p_init_healthy, steps=25)
    
    # Perturbed near stunted
    p_init_stunted = engine.project_to_simplex(engine.p_stunted_basin + np.random.normal(0, 0.02, 10))
    p_end_stunted = engine.simulate_microbiome_relaxation(p_init_stunted, steps=25)
    
    d_h_to_healthy = engine.compute_bhattacharyya_distance(p_end_healthy, engine.p_healthy_basin)
    d_s_to_stunted = engine.compute_bhattacharyya_distance(p_end_stunted, engine.p_stunted_basin)
    
    print(f"  -> Healthy Trajectory Final Distance to Target: {d_h_to_healthy:.4f}")
    print(f"  -> Stunted Trajectory Final Distance to Target: {d_s_to_stunted:.4f}")
    
    if d_h_to_healthy < 0.15 and d_s_to_stunted < 0.15:
        print("  -> RESULT: PASSED (Battery 2)")
    else:
        print("  -> RESULT: FAILED (Battery 2)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 3: Microbiota-Directed Complementary Food (MDCF) Rescue
    # ---------------------------------------------------------
    print("\n[BATTERY 3/5] Targeted MDCF Nutritional Intervention Separatrix Crossing...")
    # Attempting to rescue the stunted profile with healthy-directed prebiotic/probiotic flux
    mdcf_vector = engine.p_healthy_basin - engine.p_stunted_basin
    p_rescued = engine.simulate_microbiome_relaxation(engine.p_stunted_basin, steps=35, mdcf_intervention=mdcf_vector)
    
    d_rescued_to_healthy = engine.compute_bhattacharyya_distance(p_rescued, engine.p_healthy_basin)
    d_rescued_to_stunted = engine.compute_bhattacharyya_distance(p_rescued, engine.p_stunted_basin)
    
    print(f"  -> Rescued State Distance to Healthy Basin: {d_rescued_to_healthy:.4f}")
    print(f"  -> Rescued State Distance to Stunted Basin: {d_rescued_to_stunted:.4f}")
    
    # After intervention, state should be decisively closer to healthy basin
    if d_rescued_to_healthy < d_rescued_to_stunted:
        print("  -> RESULT: PASSED (Battery 3)")
    else:
        print("  -> RESULT: FAILED (Battery 3)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 4: Gut-Brain Endotoxin & Plasma IGF-1 Suppression Monotonicity
    # ---------------------------------------------------------
    print("\n[BATTERY 4/5] Endotoxemia & Plasma IGF-1 Suppression Monotonicity...")
    pathobiont_fractions = [0.02, 0.10, 0.25, 0.45, 0.60]
    igf1_levels = []
    for pb in pathobiont_fractions:
        p_test = np.copy(engine.p_healthy_basin)
        p_test[6] = pb
        p_test = engine.project_to_simplex(p_test)
        res = engine.predict_stunting_and_igf1(p_test)
        igf1_levels.append(res['predicted_igf1_ng_ml'])
        
    print(f"  -> Enterobacteriaceae Load: {pathobiont_fractions}")
    print(f"  -> Circulating IGF-1 Levels (ng/mL): {[round(x, 1) for x in igf1_levels]}")
    
    is_strictly_decreasing = all(igf1_levels[i] > igf1_levels[i+1] for i in range(len(igf1_levels)-1))
    if is_strictly_decreasing:
        print("  -> RESULT: PASSED (Battery 4)")
    else:
        print("  -> RESULT: FAILED (Battery 4)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 5: Severe Linear Stunting (HAZ < -2) Risk Discrimination
    # ---------------------------------------------------------
    print("\n[BATTERY 5/5] 24-Month Chronic Stunting (HAZ < -2) Risk Discrimination...")
    res_healthy = engine.predict_stunting_and_igf1(engine.p_healthy_basin)
    res_stunted = engine.predict_stunting_and_igf1(engine.p_stunted_basin)
    
    print(f"  -> Healthy Infant Stunting Risk Probability: {res_healthy['prob_stunting']:.4f}")
    print(f"  -> Dysbiotic Infant Stunting Risk Probability: {res_stunted['prob_stunting']:.4f}")
    
    if res_healthy['prob_stunting'] < 0.10 and res_stunted['prob_stunting'] > 0.90:
        print("  -> RESULT: PASSED (Battery 5)")
    else:
        print("  -> RESULT: FAILED (Battery 5)")
        all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("PILLAR 04 MATERNAL-CHILD HEALTH SUMMARY: 5/5 BATTERIES PASSED (0 FAILURES)")
    else:
        print("PILLAR 04 MATERNAL-CHILD HEALTH SUMMARY: TESTS FAILED")
    print("=" * 85)
    return all_passed

if __name__ == '__main__':
    run_all_batteries()
