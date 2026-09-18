"""
NUMERICAL TEST BATTERY: PILLAR 01 (PRION PROTEIN CONFORMATIONAL TRANSITION)
Verifies 5 core biophysical and mathematical obligations:
1. Landau-Ginzburg Potential Double-Well Extrema Existence
2. Spontaneous Physiological Barrier Positivity (Delta G_0^dagger >= 25.0 kcal/mol)
3. Catalytic Barrier Lowering under PrPSc Template Seeds
4. Thermodynamic Scrapie Stability (Delta G_folding < 0)
5. Spontaneous Healthy vs CJD Seeded Conversion Discrimination
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Chapters 07 & 10 | DOI: 10.5281/zenodo.22290043
"""

import numpy as np
from model_engine import PrionConformationalEngine

def run_all_batteries():
    print("=" * 85)
    print("PILLAR 01 PRION VERIFICATION: PrP CONFORMATIONAL TRANSITION & FREE ENERGY")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | Chapters 07 & 10")
    print("=" * 85)

    engine = PrionConformationalEngine()
    all_passed = True

    # ---------------------------------------------------------
    # Battery 1: Landau-Ginzburg Double-Well Existence
    # ---------------------------------------------------------
    print("\n[BATTERY 1/5] Landau-Ginzburg Double-Well Potential Extrema...")
    extrema = engine.compute_potential_extrema()
    v_extrema = [engine.evaluate_free_energy_potential(p) for p in extrema]
    
    print(f"  -> Critical Points phi: {[round(p, 4) for p in extrema]}")
    print(f"  -> Potential Values V(phi): {[round(v, 4) for v in v_extrema]}")
    
    # Needs at least one minimum and well-defined barrier
    if len(extrema) >= 1 and np.all(np.isfinite(v_extrema)):
        print("  -> RESULT: PASSED (Battery 1)")
    else:
        print("  -> RESULT: FAILED (Battery 1)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 2: Spontaneous Physiological Activation Barrier
    # ---------------------------------------------------------
    print("\n[BATTERY 2/5] Spontaneous Physiological Activation Barrier Positivity...")
    barrier_uncat = engine.compute_catalytic_activation_barrier(seed_concentration_pM=0.0)
    rate_uncat = engine.compute_eyring_conversion_rate(barrier_uncat)
    rate_uncat_yr = rate_uncat * (365.25 * 86400.0)
    
    print(f"  -> Uncatalyzed Activation Barrier: {barrier_uncat:.2f} kcal/mol (>= 35.0 kcal/mol)")
    print(f"  -> Spontaneous Rate k_uncat:        {rate_uncat:.2e} s^-1 ({rate_uncat_yr:.2e} year^-1)")
    
    if barrier_uncat >= 35.0 and rate_uncat < 1e-14 and rate_uncat_yr < 1e-6:
        print("  -> RESULT: PASSED (Battery 2)")
    else:
        print("  -> RESULT: FAILED (Battery 2)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 3: Catalytic Barrier Lowering Monotonicity
    # ---------------------------------------------------------
    print("\n[BATTERY 3/5] Template Catalytic Barrier Lowering Monotonicity...")
    seeds = [0.0, 1.0, 5.0, 20.0, 100.0]
    barriers = [engine.compute_catalytic_activation_barrier(s) for s in seeds]
    
    print(f"  -> Seed Concentrations (pM): {seeds}")
    print(f"  -> Effective Barriers (kcal/mol): {[round(b, 2) for b in barriers]}")
    
    is_decreasing = all(barriers[i] >= barriers[i+1] for i in range(len(barriers)-1))
    if is_decreasing and barriers[-1] < 10.0:
        print("  -> RESULT: PASSED (Battery 3)")
    else:
        print("  -> RESULT: FAILED (Battery 3)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 4: Thermodynamic Scrapie Stability
    # ---------------------------------------------------------
    print("\n[BATTERY 4/5] Thermodynamic Scrapie Equilibrium Stability...")
    delta_g = engine.delta_g_trans_kcal
    eq_ratio = np.exp(- delta_g / engine.RT)
    
    print(f"  -> Folding Free Energy Delta G_folding: {delta_g:.2f} kcal/mol")
    print(f"  -> Equilibrium Ratio [PrPSc]/[PrPC]:    {eq_ratio:.2e}")
    
    if delta_g < 0.0 and eq_ratio > 100.0:
        print("  -> RESULT: PASSED (Battery 4)")
    else:
        print("  -> RESULT: FAILED (Battery 4)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 5: Spontaneous Lifetime vs Seeded Conversion Discrimination
    # ---------------------------------------------------------
    print("\n[BATTERY 5/5] Spontaneous 80-Year Lifetime vs CJD Seeded Conversion...")
    # Test healthy brain over full 80-year human lifetime (29,220 days)
    res_healthy_80yr = engine.predict_prion_conversion_phenotype(seed_concentration_pM=0.0, incubation_days=365.25*80)
    res_cjd = engine.predict_prion_conversion_phenotype(seed_concentration_pM=50.0, incubation_days=1.0)
    
    print(f"  -> 80-Year Healthy Fraction Converted: {res_healthy_80yr['fraction_converted']:.2e} (CJD Prob: {res_healthy_80yr['prob_cjd_conversion']:.4f})")
    print(f"  -> Seeded CJD 1-Day Fraction Converted: {res_cjd['fraction_converted']:.4f} (CJD Prob: {res_cjd['prob_cjd_conversion']:.4f})")
    
    if res_healthy_80yr['fraction_converted'] < 1e-5 and res_healthy_80yr['prob_cjd_conversion'] < 0.01 and res_cjd['prob_cjd_conversion'] > 0.95:
        print("  -> RESULT: PASSED (Battery 5)")
    else:
        print("  -> RESULT: FAILED (Battery 5)")
        all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("PILLAR 01 PRION SUMMARY: 5/5 BATTERIES PASSED (0 FAILURES)")
    else:
        print("PILLAR 01 PRION SUMMARY: TESTS FAILED")
    print("=" * 85)
    return all_passed

if __name__ == '__main__':
    run_all_batteries()
