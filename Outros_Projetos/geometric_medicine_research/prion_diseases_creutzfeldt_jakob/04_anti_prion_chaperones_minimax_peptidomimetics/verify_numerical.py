"""
NUMERICAL TEST BATTERY: PILLAR 04 (ANTI-PRION THERAPEUTICS & MINIMAX CAPPING)
Verifies 5 core mathematical and pharmacological obligations:
1. Langmuir Capping Saturation Asymptote (theta_cap -> 1.0 as [Drug] -> infty)
2. Minimax Curvature Matching Optimality (d Kd / d |kappa - kappa0| > 0)
3. Monotonic Thermodynamic Monomer Stabilization (Delta Delta G_stab >= 0)
4. Potent Dual-Action Replication Quenching (Inhibition > 95%)
5. Nanomolar Capping Drug vs Inactive Decoy Rescue Discrimination
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Chapters 07 & 11 | DOI: 10.5281/zenodo.22290043
"""

import numpy as np
from model_engine import AntiPrionTherapeuticsEngine

def run_all_batteries():
    print("=" * 85)
    print("PILLAR 04 PRION VERIFICATION: ANTI-PRION THERAPEUTICS & MINIMAX PEPTIDOMIMETICS")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | Chapters 07 & 11")
    print("=" * 85)

    engine = AntiPrionTherapeuticsEngine()
    all_passed = True

    # ---------------------------------------------------------
    # Battery 1: Langmuir Capping Saturation
    # ---------------------------------------------------------
    print("\n[BATTERY 1/5] Langmuir Cross-Beta Capping Saturation (theta -> 1.0)...")
    doses = [0.1, 1.0, 10.0, 100.0, 1000.0]
    thetas = [engine.compute_fibril_capping_fraction(d, kd_nM=1.0) for d in doses]
    
    print(f"  -> Doses (nM):              {doses}")
    print(f"  -> Capping Fractions theta: {[round(t, 4) for t in thetas]}")
    
    is_saturating = all(thetas[i] < thetas[i+1] for i in range(len(thetas)-1))
    if is_saturating and thetas[-1] > 0.99:
        print("  -> RESULT: PASSED (Battery 1)")
    else:
        print("  -> RESULT: FAILED (Battery 1)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 2: Minimax Curvature Matching Optimality
    # ---------------------------------------------------------
    print("\n[BATTERY 2/5] Minimax Curvature Matching Optimality...")
    kappas = [0.08, 0.09, 0.11, 0.14]
    kds = [engine.compute_capping_affinity(k) for k in kappas]
    
    print(f"  -> Curvatures kappa (A^-1): {kappas}")
    print(f"  -> Dissociation Kds (nM):   {[round(k, 3) for k in kds]}")
    
    is_strictly_increasing_kd = all(kds[i] < kds[i+1] for i in range(len(kds)-1))
    if is_strictly_increasing_kd and kds[0] < 0.50:
        print("  -> RESULT: PASSED (Battery 2)")
    else:
        print("  -> RESULT: FAILED (Battery 2)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 3: Monomeric Stabilization Monotonicity
    # ---------------------------------------------------------
    print("\n[BATTERY 3/5] Native PrPC Alpha-Fold Thermodynamic Stabilization...")
    chaperone_doses = [0.0, 1.0, 5.0, 20.0, 50.0]
    delta_gs = [engine.compute_monomer_stabilization_delta_g(c) for c in chaperone_doses]
    
    print(f"  -> Chaperone Concentrations (uM): {chaperone_doses}")
    print(f"  -> Delta Delta G_stab (kcal/mol):  {[round(g, 3) for g in delta_gs]}")
    
    is_monotonic_stab = all(delta_gs[i] <= delta_gs[i+1] for i in range(len(delta_gs)-1))
    if is_monotonic_stab and delta_gs[-1] > 2.0:
        print("  -> RESULT: PASSED (Battery 3)")
    else:
        print("  -> RESULT: FAILED (Battery 3)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 4: Dual-Action Replication Quenching
    # ---------------------------------------------------------
    print("\n[BATTERY 4/5] Dual-Action Combination Replication Quenching...")
    res_comb = engine.evaluate_anti_prion_therapeutic_efficacy(drug_conc_nM=25.0, kappa_peptidomimetic=0.08, chaperone_conc_uM=10.0)
    
    print(f"  -> Capping Occupancy:      {res_comb['capping_fraction'] * 100:.1f}%")
    print(f"  -> Alpha-Stabilization:    {res_comb['stabilization_delta_g_kcal']:.2f} kcal/mol")
    print(f"  -> Net Inhibition:         {res_comb['inhibition_percent']:.2f}%")
    print(f"  -> Survival Extension:     {res_comb['survival_extension_factor']:.1f}x")
    
    if res_comb['inhibition_percent'] > 98.0 and res_comb['survival_extension_factor'] > 50.0:
        print("  -> RESULT: PASSED (Battery 4)")
    else:
        print("  -> RESULT: FAILED (Battery 4)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 5: Picomolar Drug vs Inactive Decoy Discrimination
    # ---------------------------------------------------------
    print("\n[BATTERY 5/5] Picomolar Drug vs Inactive Decoy Rescue Discrimination...")
    # Active drug: curvature matched (kappa=0.08), high dose (50 nM), chaperone
    res_active = engine.evaluate_anti_prion_therapeutic_efficacy(drug_conc_nM=50.0, kappa_peptidomimetic=0.08, chaperone_conc_uM=15.0)
    # Inactive decoy: curvature mismatch (kappa=0.20), low affinity, no chaperone
    res_decoy = engine.evaluate_anti_prion_therapeutic_efficacy(drug_conc_nM=1.0, kappa_peptidomimetic=0.20, chaperone_conc_uM=0.0)
    
    print(f"  -> Active Drug Rescue Probability: {res_active['prob_scjd_rescue']:.4f}")
    print(f"  -> Inactive Decoy Rescue Prob:     {res_decoy['prob_scjd_rescue']:.4f}")
    
    if res_active['prob_scjd_rescue'] > 0.95 and res_decoy['prob_scjd_rescue'] < 0.01:
        print("  -> RESULT: PASSED (Battery 5)")
    else:
        print("  -> RESULT: FAILED (Battery 5)")
        all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("PILLAR 04 PRION SUMMARY: 5/5 BATTERIES PASSED (0 FAILURES)")
    else:
        print("PILLAR 04 PRION SUMMARY: TESTS FAILED")
    print("=" * 85)
    return all_passed

if __name__ == '__main__':
    run_all_batteries()
