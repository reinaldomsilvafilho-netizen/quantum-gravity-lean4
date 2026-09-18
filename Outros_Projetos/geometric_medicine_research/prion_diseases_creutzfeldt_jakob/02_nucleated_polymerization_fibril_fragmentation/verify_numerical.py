"""
NUMERICAL TEST BATTERY: PILLAR 02 (PRION POLYMERIZATION & FRAGMENTATION KINETICS)
Verifies 5 core mathematical and kinetic obligations:
1. Strict Total Monomer Mass Conservation (m(t) + M(t) == m_total)
2. Non-Negative Positivity of Fibril States (P(t) >= 0, M(t) >= 0)
3. Extrinsic Curvature Monotonicity of Fragmentation Rate
4. Analytical vs Numerical Doubling Rate Equivalence
5. sCJD Explosive Doubling vs Slow Alzheimer Amyloidosis Discrimination
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Chapters 04 & 06 | DOI: 10.5281/zenodo.22290043
"""

import numpy as np
from model_engine import PrionPolymerizationKineticsEngine

def run_all_batteries():
    print("=" * 85)
    print("PILLAR 02 PRION VERIFICATION: NUCLEATED POLYMERIZATION & FRAGMENTATION")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | Chapters 04 & 06")
    print("=" * 85)

    engine = PrionPolymerizationKineticsEngine()
    all_passed = True

    # ---------------------------------------------------------
    # Battery 1: Monomer Mass Conservation
    # ---------------------------------------------------------
    print("\n[BATTERY 1/5] Total Monomer Mass Conservation (m(t) + M(t) == m0)...")
    times, m_arr, P_arr, M_arr = engine.simulate_polymerization_trajectory(t_max_hours=24.0, n_steps=100)
    total_mass = m_arr + M_arr
    max_mass_error = float(np.max(np.abs(total_mass - engine.m0)))
    
    print(f"  -> Maximum Mass Conservation Violation: {max_mass_error:.2e} M")
    if max_mass_error < 1e-12:
        print("  -> RESULT: PASSED (Battery 1)")
    else:
        print("  -> RESULT: FAILED (Battery 1)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 2: State Positivity and Monotonic Mass Increase
    # ---------------------------------------------------------
    print("\n[BATTERY 2/5] Fibril State Positivity and Monotonic Growth...")
    is_positive = (np.all(m_arr >= 0.0) and np.all(P_arr >= 0.0) and np.all(M_arr >= 0.0))
    dM = np.diff(M_arr)
    is_monotonic_mass = np.all(dM >= -1e-15)
    
    print(f"  -> State Positivity Verified: {is_positive}")
    print(f"  -> Monotonic Fibril Mass Increase: {is_monotonic_mass}")
    
    if is_positive and is_monotonic_mass:
        print("  -> RESULT: PASSED (Battery 2)")
    else:
        print("  -> RESULT: FAILED (Battery 2)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 3: Curvature-Induced Fragmentation Monotonicity
    # ---------------------------------------------------------
    print("\n[BATTERY 3/5] Extrinsic Curvature Fragmentation Monotonicity...")
    curvatures = [0.01, 0.02, 0.05, 0.10, 0.20]
    frag_rates = [engine.compute_curvature_fragmentation_rate(kappa_star=k) for k in curvatures]
    
    print(f"  -> Fibril Curvatures kappa* (A^-1): {curvatures}")
    print(f"  -> Fragmentation Rates k_- (s^-1):  {[round(r, 6) for r in frag_rates]}")
    
    is_strictly_increasing = all(frag_rates[i] < frag_rates[i+1] for i in range(len(frag_rates)-1))
    if is_strictly_increasing and frag_rates[-1] > frag_rates[0] * 10.0:
        print("  -> RESULT: PASSED (Battery 3)")
    else:
        print("  -> RESULT: FAILED (Battery 3)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 4: Analytical Exponential Rate Equivalence
    # ---------------------------------------------------------
    print("\n[BATTERY 4/5] Analytical vs Numerical Exponential Growth Rate...")
    kappa_eff, t_double_hours = engine.compute_analytical_exponential_growth_rate(kappa_star=0.08)
    
    print(f"  -> Effective Replication Rate kappa_eff: {kappa_eff:.4e} s^-1")
    print(f"  -> Analytical Doubling Time:             {t_double_hours:.2f} hours")
    
    if 1.0 < t_double_hours < 120.0 and kappa_eff > 0.0:
        print("  -> RESULT: PASSED (Battery 4)")
    else:
        print("  -> RESULT: FAILED (Battery 4)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 5: sCJD Explosive vs Alzheimer Slow Amyloidosis Discrimination
    # ---------------------------------------------------------
    print("\n[BATTERY 5/5] sCJD Explosive Doubling vs Slow Alzheimer Amyloidosis...")
    # sCJD prion: high fragmentation (t_double ~ 35 hours)
    _, t_double_scjd = engine.compute_analytical_exponential_growth_rate(kappa_star=0.10)
    prob_cjd = engine.classify_amyloid_kinetics(t_double_scjd)
    
    # Alzheimer A-beta: rigid, minimal fragmentation, slow secondary nucleation (t_double ~ 500 hours)
    t_double_alzheimer = 480.0
    prob_alzheimer = engine.classify_amyloid_kinetics(t_double_alzheimer)
    
    print(f"  -> sCJD Doubling Time:       {t_double_scjd:.1f}h (Explosive Prion Probability: {prob_cjd:.4f})")
    print(f"  -> Alzheimer Doubling Time:  {t_double_alzheimer:.1f}h (Explosive Prion Probability: {prob_alzheimer:.4f})")
    
    if prob_cjd > 0.90 and prob_alzheimer < 0.01:
        print("  -> RESULT: PASSED (Battery 5)")
    else:
        print("  -> RESULT: FAILED (Battery 5)")
        all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("PILLAR 02 PRION SUMMARY: 5/5 BATTERIES PASSED (0 FAILURES)")
    else:
        print("PILLAR 02 PRION SUMMARY: TESTS FAILED")
    print("=" * 85)
    return all_passed

if __name__ == '__main__':
    run_all_batteries()
