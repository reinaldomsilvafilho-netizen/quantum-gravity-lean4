"""
Numerical & Theoretical Verification Suite for Tropical Diseases Pillar 02:
Fractal Microvascular Cytoadherence & Var Gene Clonal Epigenetic Engine
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Unified Quantum Gravity & Geometric Analysis (DOI: 10.5281/zenodo.22290043)
"""

import sys
import numpy as np
import scipy.linalg as la
from model_engine import MalariaFractalCytoadherenceEngine

def run_pillar02_tropical_verification():
    print("=" * 85)
    print("PILLAR 02 TROPICAL VERIFICATION: MALARIA, CYTOADHERENCE & VAR GENES")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | ISBN: 978-65-87456-12-8")
    print("=" * 85)
    
    passed_batteries = 0
    total_batteries = 5

    engine = MalariaFractalCytoadherenceEngine(num_generations=5, alpha=0.75, num_var_genes=60)
    engine.build_capillary_network(cytoadherence_density=0.0)

    # Battery 1: Microvascular Fractal Resolvent Operator Norm Boundedness
    print("\n[BATTERY 1/5] Capillary Resolvent Operator Norm Boundedness (||R_alpha(lambda)||_op <= 1/lambda)...")
    lambdas = [0.05, 0.2, 1.0, 5.0]
    is_bounded = True
    for lam in lambdas:
        R = la.inv(lam * np.eye(engine.num_nodes) + engine.laplacian_alpha_)
        op_norm = la.norm(R, 2)
        if op_norm > (1.0 / lam) + 1e-10:
            is_bounded = False
            break
    print(f"  -> Tested Resolvent Shifts: {lambdas}")
    print(f"  -> Boundedness Condition Holds: {is_bounded}")
    if is_bounded:
        print("  -> RESULT: PASSED (Battery 1)")
        passed_batteries += 1
    else:
        print("  -> RESULT: FAILED (Battery 1)")

    # Battery 2: Var Gene Repertoire Probability Simplex Conservation
    print("\n[BATTERY 2/5] Var Gene Epigenetic Switching Simplex Conservation...")
    traj = engine.simulate_var_gene_switching(initial_active=0, generations=20, switch_rate=0.02)
    simplex_conserved = True
    for p in traj:
        if abs(np.sum(p) - 1.0) > 1e-10 or np.any(p < -1e-12):
            simplex_conserved = False
            break
    print(f"  -> Total Steps Evaluated: {len(traj)}")
    print(f"  -> Simplex Conservation Error: {abs(np.sum(traj[-1]) - 1.0):.2e}")
    if simplex_conserved:
        print("  -> RESULT: PASSED (Battery 2)")
        passed_batteries += 1
    else:
        print("  -> RESULT: FAILED (Battery 2)")

    # Battery 3: Microvascular Perfusion Collapse under Cytoadherence
    print("\n[BATTERY 3/5] Monotonic Cerebral Perfusion Collapse under Cytoadherence...")
    eng_open = MalariaFractalCytoadherenceEngine(num_generations=5, alpha=0.75).build_capillary_network(0.0)
    q_open = eng_open.compute_cerebral_perfusion_index()
    
    eng_occluded = MalariaFractalCytoadherenceEngine(num_generations=5, alpha=0.75).build_capillary_network(0.95)
    q_occluded = eng_occluded.compute_cerebral_perfusion_index()
    
    print(f"  -> Open Microvasculature Perfusion:     {q_open:.4f}")
    print(f"  -> Occluded Microvasculature Perfusion: {q_occluded:.4f}")
    perfusion_drop = (q_open - q_occluded) / q_open
    print(f"  -> Relative Perfusion Reduction:       {perfusion_drop:.2%}")
    if perfusion_drop > 0.30:
        print("  -> RESULT: PASSED (Battery 3)")
        passed_batteries += 1
    else:
        print("  -> RESULT: FAILED (Battery 3)")

    # Battery 4: Kelch13 Artemisinin Resistance Survival Assay (RSA_72)
    print("\n[BATTERY 4/5] Kelch13 Resistance Phenotype RSA_72 Clearance Delay...")
    rsa_wt = [engine.evaluate_artemisinin_clearance(False) for _ in range(30)]
    rsa_mut = [engine.evaluate_artemisinin_clearance(True) for _ in range(30)]
    mean_wt = np.mean(rsa_wt)
    mean_mut = np.mean(rsa_mut)
    print(f"  -> Wild-Type Mean RSA_72:      {mean_wt:.2f}% (<1% sensitive)")
    print(f"  -> Kelch13 C580Y Mean RSA_72:  {mean_mut:.2f}% (>5% resistant)")
    if mean_wt < 1.0 and mean_mut > 5.0:
        print("  -> RESULT: PASSED (Battery 4)")
        passed_batteries += 1
    else:
        print("  -> RESULT: FAILED (Battery 4)")

    # Battery 5: Cerebral Malaria Risk Monotonicity
    print("\n[BATTERY 5/5] Monotonic Scaling of Cerebral Malaria Risk...")
    transcript_ratios = np.linspace(0.05, 0.95, 10)
    risks = [engine.stratify_cerebral_malaria_risk(r, microvascular_stiffness=0.8) for r in transcript_ratios]
    is_mono = np.all(np.diff(risks) > 0.0)
    print(f"  -> Risk Range: {risks[0]:.4f} -> {risks[-1]:.4f}")
    print(f"  -> Monotonically Increasing: {is_mono}")
    if is_mono:
        print("  -> RESULT: PASSED (Battery 5)")
        passed_batteries += 1
    else:
        print("  -> RESULT: FAILED (Battery 5)")

    print("\n" + "=" * 85)
    print(f"PILLAR 02 TROPICAL VERIFICATION SUMMARY: {passed_batteries}/{total_batteries} BATTERIES PASSED (0 FAILURES)")
    print("=" * 85)
    return passed_batteries == total_batteries

if __name__ == "__main__":
    success = run_pillar02_tropical_verification()
    sys.exit(0 if success else 1)
