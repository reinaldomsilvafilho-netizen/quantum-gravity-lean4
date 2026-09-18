"""
NUMERICAL VERIFICATION BATTERIES: PILLAR 02 (Neuroscience & Mental Health)
Refractory Epilepsy, ECoG Gauge Holonomies & Seizure Onset Zone
Theoretical Grounding: Treatise Chapters 01 & 11
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np
from model_engine import EpilepsyFocusLocalizationEngine

def run_all_batteries():
    print("=" * 85)
    print("PILLAR 02 NEUROSCIENCE VERIFICATION: ECOG EPILEPSY FOCUS LOCALIZATION")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | Chapters 01 & 11")
    print("=" * 85)

    engine = EpilepsyFocusLocalizationEngine(n_channels=32, grid_dim=(4, 8))
    all_passed = True

    # Construct synthetic ictal burst originating at electrode #10 (row 1, col 2)
    # True SOZ coordinate: (10.0, 20.0) mm
    true_soz_idx = 10
    true_coord = engine.electrode_coords[true_soz_idx]
    
    t = np.linspace(0, 1.0, 500)
    ecog_burst = np.zeros((32, len(t)))
    for ch in range(32):
        dist = np.linalg.norm(engine.electrode_coords[ch] - true_coord)
        # Propagation delay + amplitude decay
        delay = dist * 0.005 # 5 ms per mm
        attenuation = np.exp(-dist / 15.0)
        # 120 Hz High-Frequency Oscillation (HFO) + 4 Hz spike-wave
        signal = attenuation * (np.sin(2 * np.pi * 120.0 * (t - delay)) + 0.5 * np.sin(2 * np.pi * 4.0 * (t - delay)))
        ecog_burst[ch] = signal

    # ---------------------------------------------------------
    # Battery 1: Source Flow Divergence Positivity
    # ---------------------------------------------------------
    print("\n[BATTERY 1/5] Pacemaker Node Flow Divergence Positivity (div(v_soz) > 0)...")
    v_field, div, energy = engine.compute_optimal_transport_velocity(ecog_burst)
    div_soz = div[true_soz_idx]
    div_mean = np.mean(div)
    
    print(f"  -> True SOZ Pacemaker Divergence: {div_soz:+.4f}")
    print(f"  -> Mean Background Divergence:    {div_mean:+.4f}")
    
    if div_soz > 0.0 and div_soz > div_mean:
        print("  -> RESULT: PASSED (Battery 1)")
    else:
        print("  -> RESULT: FAILED (Battery 1)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 2: Downstream Propagation Node Negative/Zero Divergence
    # ---------------------------------------------------------
    print("\n[BATTERY 2/5] Distant Recruited Node Flow Divergence Rejection...")
    distant_idx = 31 # Far corner electrode
    div_distant = div[distant_idx]
    
    print(f"  -> Distant Recruited Electrode (#31) Divergence: {div_distant:+.4f}")
    if div_distant <= div_soz * 0.2:
        print("  -> RESULT: PASSED (Battery 2)")
    else:
        print("  -> RESULT: FAILED (Battery 2)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 3: Non-Abelian Gauge Holonomy Circulation around Focus
    # ---------------------------------------------------------
    print("\n[BATTERY 3/5] Gauge Holonomy Phase Circulation oint v . dr...")
    circ_soz, wilson_soz = engine.compute_gauge_holonomy(v_field, center_idx=true_soz_idx)
    circ_distant, wilson_distant = engine.compute_gauge_holonomy(v_field, center_idx=0)
    
    print(f"  -> Pacemaker Circuit Circulation:  {circ_soz:.4f} | Wilson Trace: {wilson_soz:.4f}")
    print(f"  -> Baseline Distant Circulation:   {circ_distant:.4f} | Wilson Trace: {wilson_distant:.4f}")
    
    if np.abs(circ_soz) > np.abs(circ_distant):
        print("  -> RESULT: PASSED (Battery 3)")
    else:
        print("  -> RESULT: FAILED (Battery 3)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 4: Spatial Localization Sub-Millimeter Accuracy
    # ---------------------------------------------------------
    print("\n[BATTERY 4/5] SOZ Pacemaker Spatial Localization Accuracy...")
    res = engine.localize_seizure_onset_zone(ecog_burst)
    pred_coord = res['predicted_coord_mm']
    loc_error_mm = np.linalg.norm(pred_coord - true_coord)
    
    print(f"  -> True Pacemaker Coordinate:      {true_coord} mm")
    print(f"  -> Predicted Pacemaker Coordinate: {pred_coord} mm")
    print(f"  -> Spatial Localization Error:     {loc_error_mm:.2f} mm")
    
    # 0.0 mm error in 10mm grid
    if loc_error_mm < 5.0 and res['predicted_soz_idx'] == true_soz_idx:
        print("  -> RESULT: PASSED (Battery 4)")
    else:
        print("  -> RESULT: FAILED (Battery 4)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 5: Surgical Resection Boundary Discrimination
    # ---------------------------------------------------------
    print("\n[BATTERY 5/5] Resection Boundary Distinction (SOZ vs Safe Eloquent Cortex)...")
    scores = res['soz_scores']
    max_soz_score = scores[true_soz_idx]
    other_scores = np.delete(scores, true_soz_idx)
    margin = max_soz_score - np.max(other_scores)
    
    print(f"  -> SOZ Peak Score:         {max_soz_score:.4f}")
    print(f"  -> Second Highest Score:   {np.max(other_scores):.4f}")
    print(f"  -> Discrimination Margin:  {margin:.4f}")
    
    if margin > 0.15:
        print("  -> RESULT: PASSED (Battery 5)")
    else:
        print("  -> RESULT: FAILED (Battery 5)")
        all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("PILLAR 02 NEUROSCIENCE SUMMARY: 5/5 BATTERIES PASSED (0 FAILURES)")
    else:
        print("PILLAR 02 NEUROSCIENCE SUMMARY: TESTS FAILED")
    print("=" * 85)
    return all_passed

if __name__ == '__main__':
    run_all_batteries()
