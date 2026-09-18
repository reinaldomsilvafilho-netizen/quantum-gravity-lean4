"""
NUMERICAL VERIFICATION BATTERIES: PILLAR 01 (Neuroscience & Mental Health)
Treatment-Resistant Depression, Fisher-Rao Information Curvature & Suicide Risk
Theoretical Grounding: Treatise Chapter 10
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np
from model_engine import DepressionAttractorEngine

def run_all_batteries():
    print("=" * 85)
    print("PILLAR 01 NEUROSCIENCE VERIFICATION: TREATMENT-RESISTANT DEPRESSION ATTRACTOR")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | Chapter 10")
    print("=" * 85)

    engine = DepressionAttractorEngine(n_regions=8)
    all_passed = True

    # ---------------------------------------------------------
    # Battery 1: Fisher-Rao Information Curvature Positivity
    # ---------------------------------------------------------
    print("\n[BATTERY 1/5] Fisher-Rao Information Metric Curvature Positivity...")
    cov_identity = np.eye(8)
    curv, rigidity, cross = engine.compute_fisher_rao_information_curvature(cov_identity)
    
    print(f"  -> Information Curvature Scalar: {curv:.4f}")
    print(f"  -> Baseline Rigidity Index:      {rigidity:.4f}")
    
    if curv > 0.0 and np.isfinite(curv):
        print("  -> RESULT: PASSED (Battery 1)")
    else:
        print("  -> RESULT: FAILED (Battery 1)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 2: DMN Hyper-Rigidity Divergence in TRD
    # ---------------------------------------------------------
    print("\n[BATTERY 2/5] DMN Hyper-Rigidity Attractor Depth in TRD vs Healthy...")
    # Healthy connectome: balanced DMN and CEN
    cov_healthy = np.eye(8)
    cov_healthy[:4, :4] += 0.35 # moderate DMN co-activation
    cov_healthy[4:, 4:] += 0.35 # moderate CEN co-activation
    cov_healthy[:4, 4:] += 0.20 # healthy cross-talk
    cov_healthy[4:, :4] = cov_healthy[:4, 4:].T
    
    # Pathological TRD connectome: hyper-rigid DMN, decoupled CEN
    cov_trd = np.eye(8)
    cov_trd[:4, :4] += 0.85 # extreme pathological DMN rumination lock
    cov_trd[4:, 4:] += 0.15 # hypoactive CEN
    cov_trd[:4, 4:] += 0.02 # decoupled frontoparietal control
    cov_trd[4:, :4] = cov_trd[:4, 4:].T
    
    _, rig_healthy, _ = engine.compute_fisher_rao_information_curvature(cov_healthy)
    _, rig_trd, _ = engine.compute_fisher_rao_information_curvature(cov_trd)
    
    print(f"  -> Healthy Brain Rigidity Index:     {rig_healthy:.4f}")
    print(f"  -> Treatment-Resistant TRD Rigidity: {rig_trd:.4f}")
    
    if rig_trd > 2.5 * rig_healthy:
        print("  -> RESULT: PASSED (Battery 2)")
    else:
        print("  -> RESULT: FAILED (Battery 2)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 3: Post-Ketamine Dynamical Reset
    # ---------------------------------------------------------
    print("\n[BATTERY 3/5] Rapid Ketamine/TMS Attractor Dissolution...")
    cov_post = engine.simulate_rapid_ketamine_remission(cov_trd, ketamine_dose_effect=0.9)
    _, rig_post, cross_post = engine.compute_fisher_rao_information_curvature(cov_post)
    
    print(f"  -> Post-Intervention Rigidity Index: {rig_post:.4f} (Drop from {rig_trd:.4f})")
    print(f"  -> Restored DMN-CEN Cross-Talk:      {cross_post:.4f}")
    
    if rig_post < 0.5 * rig_trd and cross_post > 0.10:
        print("  -> RESULT: PASSED (Battery 3)")
    else:
        print("  -> RESULT: FAILED (Battery 3)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 4: Acute Suicide Risk Index Monotonicity
    # ---------------------------------------------------------
    print("\n[BATTERY 4/5] Acute Suicide Crisis Risk Monotonicity across Attractor States...")
    res_trd = engine.predict_treatment_response_and_suicide_risk(cov_trd)
    res_post = engine.predict_treatment_response_and_suicide_risk(cov_post)
    res_healthy = engine.predict_treatment_response_and_suicide_risk(cov_healthy)
    
    p_sui_trd = res_trd['prob_suicide_crisis']
    p_sui_post = res_post['prob_suicide_crisis']
    p_sui_healthy = res_healthy['prob_suicide_crisis']
    
    print(f"  -> Pre-Treatment TRD Suicide Risk:  {p_sui_trd:.4f}")
    print(f"  -> Post-Ketamine 24h Suicide Risk:  {p_sui_post:.4f}")
    print(f"  -> Healthy Control Baseline Risk:   {p_sui_healthy:.4f}")
    
    if p_sui_trd > 0.85 and p_sui_post < 0.15 and p_sui_healthy < 0.15 and p_sui_trd > p_sui_post:
        print("  -> RESULT: PASSED (Battery 4)")
    else:
        print("  -> RESULT: FAILED (Battery 4)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 5: Rapid Treatment Response Discrimination
    # ---------------------------------------------------------
    print("\n[BATTERY 5/5] Rapid Therapeutic Remission Discrimination...")
    # Responders preserve latent plastic cross-talk capacity; non-responders have structural calcification
    cov_nonresponder = np.copy(cov_trd)
    cov_nonresponder[4:, 4:] = 0.05 * np.eye(4) # complete executive failure
    
    res_resp = engine.predict_treatment_response_and_suicide_risk(cov_post)
    res_non = engine.predict_treatment_response_and_suicide_risk(cov_nonresponder)
    
    print(f"  -> Plastic Responder Remission Probability:     {res_resp['prob_treatment_response']:.4f}")
    print(f"  -> Structural Non-Responder Remission Probability: {res_non['prob_treatment_response']:.4f}")
    
    if res_resp['prob_treatment_response'] > 0.75 and res_non['prob_treatment_response'] < 0.20:
        print("  -> RESULT: PASSED (Battery 5)")
    else:
        print("  -> RESULT: FAILED (Battery 5)")
        all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("PILLAR 01 NEUROSCIENCE SUMMARY: 5/5 BATTERIES PASSED (0 FAILURES)")
    else:
        print("PILLAR 01 NEUROSCIENCE SUMMARY: TESTS FAILED")
    print("=" * 85)
    return all_passed

if __name__ == '__main__':
    run_all_batteries()
