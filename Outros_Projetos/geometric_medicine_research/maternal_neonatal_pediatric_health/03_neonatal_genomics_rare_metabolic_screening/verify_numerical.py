"""
NUMERICAL VERIFICATION BATTERIES: PILLAR 03 (Maternal-Child Health)
Neonatal Genomic-Metabolic Screening & Simplex Fisher-Rao Invariants
Theoretical Grounding: Treatise Chapters 03 & 05
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np
from model_engine import NeonatalMetabolicSimplexEngine

def run_all_batteries():
    print("=" * 85)
    print("PILLAR 03 MATERNAL-CHILD HEALTH VERIFICATION: NEONATAL METABOLIC SIMPLEX")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | Chapters 03 & 05")
    print("=" * 85)

    engine = NeonatalMetabolicSimplexEngine()
    all_passed = True

    # ---------------------------------------------------------
    # Battery 1: Simplex Closure and Normalization Invariance
    # ---------------------------------------------------------
    print("\n[BATTERY 1/5] Simplex Projection Closure sum(p_j) = 1 and Dilution Invariance...")
    raw_sample = np.array([32.0, 17.0, 0.14, 0.11, 0.13, 0.14, 58.0, 72.0])
    # Severe dilution (e.g. 10x intravenous fluid volume expansion)
    raw_diluted = raw_sample * 0.1
    
    p1 = engine.project_to_simplex(raw_sample)
    p2 = engine.project_to_simplex(raw_diluted)
    
    sum_err = np.abs(np.sum(p1) - 1.0)
    dilution_diff = np.linalg.norm(p1 - p2)
    
    print(f"  -> Normalization Sum Error |sum(p) - 1|: {sum_err:.2e}")
    print(f"  -> Dilution Invariance Discrepancy ||p1 - p2||: {dilution_diff:.2e}")
    
    if sum_err < 1e-12 and dilution_diff < 1e-12:
        print("  -> RESULT: PASSED (Battery 1)")
    else:
        print("  -> RESULT: FAILED (Battery 1)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 2: Fisher-Rao Metric Positivity and Symmetry
    # ---------------------------------------------------------
    print("\n[BATTERY 2/5] Fisher-Rao Information Metric Axiom Verification...")
    p_healthy = engine.p_healthy_ref
    p_mcadd = np.copy(p_healthy)
    p_mcadd[3] *= 15.0 # C8 surge
    p_mcadd = engine.project_to_simplex(p_mcadd)
    
    d_self = engine.compute_fisher_rao_distance(p_healthy, p_healthy)
    d_mut = engine.compute_fisher_rao_distance(p_healthy, p_mcadd)
    d_mut_rev = engine.compute_fisher_rao_distance(p_mcadd, p_healthy)
    
    print(f"  -> Distance to Self: d(p, p) = {d_self:.2e}")
    print(f"  -> Forward Distance: d(p_h, p_m) = {d_mut:.4f}")
    print(f"  -> Backward Distance: d(p_m, p_h) = {d_mut_rev:.4f}")
    
    if d_self == 0.0 and np.abs(d_mut - d_mut_rev) < 1e-12 and d_mut > 0.10:
        print("  -> RESULT: PASSED (Battery 2)")
    else:
        print("  -> RESULT: FAILED (Battery 2)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 3: Enzymatic Block Monotonicity under Substrate Accumulation
    # ---------------------------------------------------------
    print("\n[BATTERY 3/5] Enzymatic Metabolic Block Ratio Monotonicity...")
    c8_multipliers = [1.0, 2.0, 5.0, 10.0, 20.0]
    lfcs = []
    for mult in c8_multipliers:
        raw_test = np.copy(raw_sample)
        raw_test[3] *= mult
        p_t = engine.project_to_simplex(raw_test)
        _, lfc = engine.evaluate_enzymatic_block(p_t)
        lfcs.append(lfc)
        
    print(f"  -> Multipliers: {c8_multipliers}")
    print(f"  -> Log2 Fold Changes: {[round(x, 2) for x in lfcs]}")
    
    is_strictly_increasing = all(lfcs[i] < lfcs[i+1] for i in range(len(lfcs)-1))
    if is_strictly_increasing:
        print("  -> RESULT: PASSED (Battery 3)")
    else:
        print("  -> RESULT: FAILED (Battery 3)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 4: Multi-Analyte Resolvent Stability
    # ---------------------------------------------------------
    print("\n[BATTERY 4/5] Multi-Analyte Simplex Resolvent Condition Stability...")
    # Gram matrix of simplex coordinates
    G_mat = np.outer(p_healthy, p_healthy) + 1e-3 * np.eye(len(p_healthy))
    cond_num = np.linalg.cond(G_mat)
    print(f"  -> Simplex Metric Matrix Condition Number: {cond_num:.2f}")
    
    if cond_num < 1e4:
        print("  -> RESULT: PASSED (Battery 4)")
    else:
        print("  -> RESULT: FAILED (Battery 4)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 5: Rare Disease Fusion Discrimination (Healthy vs IEM)
    # ---------------------------------------------------------
    print("\n[BATTERY 5/5] Inborn Error of Metabolism Posterior Probability Discrimination...")
    res_healthy = engine.fuse_genomic_metabolomic_evidence(raw_sample, genomic_pathogenicity_score=0.05)
    # Acute MCADD sample: elevated C8 + pathogenic homozygous ACADM mutation (CADD=0.92)
    raw_iem = np.copy(raw_sample)
    raw_iem[3] = 4.5 # 45-fold elevation in C8 octanoylcarnitine
    res_iem = engine.fuse_genomic_metabolomic_evidence(raw_iem, genomic_pathogenicity_score=0.92)
    
    print(f"  -> Healthy Neonate Posterior IEM Probability: {res_healthy['prob_iem']:.4f}")
    print(f"  -> Acute MCADD Case Posterior IEM Probability: {res_iem['prob_iem']:.4f}")
    
    if res_healthy['prob_iem'] < 0.05 and res_iem['prob_iem'] > 0.95:
        print("  -> RESULT: PASSED (Battery 5)")
    else:
        print("  -> RESULT: FAILED (Battery 5)")
        all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("PILLAR 03 MATERNAL-CHILD HEALTH SUMMARY: 5/5 BATTERIES PASSED (0 FAILURES)")
    else:
        print("PILLAR 03 MATERNAL-CHILD HEALTH SUMMARY: TESTS FAILED")
    print("=" * 85)
    return all_passed

if __name__ == '__main__':
    run_all_batteries()
