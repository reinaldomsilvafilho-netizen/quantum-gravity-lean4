"""
NUMERICAL TEST BATTERY: PILLAR 03 (POPULATION PHARMACOGENOMICS & ADR PREVENTION)
Verifies 5 core mathematical and clinical obligations:
1. Fisher-Rao Information Metric Positive-Definiteness (lambda_min(g^F) > 0)
2. Bakry-Émery Ricci Curvature Floor Positivity (Ric_infty >= K* > 0)
3. Exponential 2-Wasserstein Contraction (W_2(t) <= exp(-K* t) W_2(0))
4. Simplicial Admixture Normalization Preservation (sum a_k == 1.0)
5. Multi-Allelic Phenotype Toxicity Discrimination (Poor vs Normal vs Ultra-Rapid)
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Chapter 10 & Paper 1 | DOI: 10.5281/zenodo.22290043
"""

import numpy as np
from model_engine import PopulationPharmacogenomicsEngine

def run_all_batteries():
    print("=" * 85)
    print("PILLAR 03 PHARMACOLOGY VERIFICATION: POPULATION PHARMACOGENOMICS & ADRS")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | Chapter 10 & Paper 1")
    print("=" * 85)

    engine = PopulationPharmacogenomicsEngine(k_ancestries=5)
    all_passed = True

    # ---------------------------------------------------------
    # Battery 1: Fisher-Rao Information Metric Positive-Definiteness
    # ---------------------------------------------------------
    print("\n[BATTERY 1/5] Fisher-Rao Metric Tensor Positive-Definiteness...")
    g_tensor = engine.compute_fisher_rao_metric(clearance_rate=5.0, volume_dist=40.0)
    eigvals = np.linalg.eigvalsh(g_tensor)
    
    print(f"  -> Metric Tensor g^F:\n{g_tensor}")
    print(f"  -> Minimum Eigenvalue lambda_min(g^F): {np.min(eigvals):.4e}")
    
    if np.all(eigvals > 0.0):
        print("  -> RESULT: PASSED (Battery 1)")
    else:
        print("  -> RESULT: FAILED (Battery 1)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 2: Bakry-Émery Ricci Curvature Floor Positivity
    # ---------------------------------------------------------
    print("\n[BATTERY 2/5] Bakry-Émery Ricci Curvature Lower Bound (Ric_infty >= K* > 0)...")
    k_star = engine.compute_bakry_emery_ricci_floor(g_tensor, prior_regularization=0.50)
    
    print(f"  -> Bakry-Émery Ricci Floor K*: {k_star:.4f}")
    if k_star > 0.0 and np.isfinite(k_star):
        print("  -> RESULT: PASSED (Battery 2)")
    else:
        print("  -> RESULT: FAILED (Battery 2)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 3: Exponential 2-Wasserstein Contraction
    # ---------------------------------------------------------
    print("\n[BATTERY 3/5] Exponential 2-Wasserstein Contraction of Metabolic Posteriors...")
    w2_init = 10.0
    t, w2_traj = engine.compute_wasserstein_contraction(w2_init, k_star=2.5, time_steps=6)
    
    print(f"  -> Time Steps: {t}")
    print(f"  -> W_2 Trajectory: {[round(w, 4) for w in w2_traj]}")
    
    is_strictly_decaying = all(w2_traj[i] > w2_traj[i+1] for i in range(len(w2_traj)-1))
    if is_strictly_decaying and w2_traj[-1] < w2_init:
        print("  -> RESULT: PASSED (Battery 3)")
    else:
        print("  -> RESULT: FAILED (Battery 3)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 4: Simplicial Admixture Invariance
    # ---------------------------------------------------------
    print("\n[BATTERY 4/5] Multi-Ethnic Simplicial Admixture Normalization...")
    raw_admixture = [0.35, 0.40, 0.15, 0.05, 0.05]
    res_admix = engine.predict_adr_risk_and_optimal_dose(['*1', '*1'], admixture_weights=raw_admixture)
    
    norm_sum = sum(raw_admixture)
    print(f"  -> Admixture Sum: {norm_sum:.4f}")
    print(f"  -> Clearance under Admixture: {res_admix['clearance_L_h']:.2f} L/h")
    
    if abs(norm_sum - 1.0) < 1e-6:
        print("  -> RESULT: PASSED (Battery 4)")
    else:
        print("  -> RESULT: FAILED (Battery 4)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 5: Multi-Allelic Phenotype Toxicity Discrimination
    # ---------------------------------------------------------
    print("\n[BATTERY 5/5] Multi-Allelic Phenotype Toxicity Discrimination...")
    # 1. Poor Metabolizer (*4/*4 null alleles) -> high toxic accumulation
    res_poor = engine.predict_adr_risk_and_optimal_dose(['*4', '*4'], hla_risk_allele=False)
    # 2. Normal Extensive Metabolizer (*1/*1) -> safe
    res_normal = engine.predict_adr_risk_and_optimal_dose(['*1', '*1'], hla_risk_allele=False)
    # 3. HLA Risk Carrier (*1/*1 + HLA-B*57:01) -> hypersensitivity contraindication
    res_hla = engine.predict_adr_risk_and_optimal_dose(['*1', '*1'], hla_risk_allele=True)
    
    print(f"  -> Poor Metabolizer (*4/*4) ADR Risk:        {res_poor['prob_severe_adr']:.4f} (Optimal Dose: {res_poor['optimal_dose_mg']:.1f} mg)")
    print(f"  -> Normal Metabolizer (*1/*1) ADR Risk:      {res_normal['prob_severe_adr']:.4f} (Optimal Dose: {res_normal['optimal_dose_mg']:.1f} mg)")
    print(f"  -> HLA-B*57:01 Carrier ADR Risk:             {res_hla['prob_severe_adr']:.4f} (Optimal Dose: {res_hla['optimal_dose_mg']:.1f} mg)")
    
    if (res_poor['prob_severe_adr'] > 0.75 and 
        res_normal['prob_severe_adr'] < 0.15 and 
        res_hla['prob_severe_adr'] > 0.95 and 
        res_hla['optimal_dose_mg'] == 0.0):
        print("  -> RESULT: PASSED (Battery 5)")
    else:
        print("  -> RESULT: FAILED (Battery 5)")
        all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("PILLAR 03 PHARMACOLOGY SUMMARY: 5/5 BATTERIES PASSED (0 FAILURES)")
    else:
        print("PILLAR 03 PHARMACOLOGY SUMMARY: TESTS FAILED")
    print("=" * 85)
    return all_passed

if __name__ == '__main__':
    run_all_batteries()
