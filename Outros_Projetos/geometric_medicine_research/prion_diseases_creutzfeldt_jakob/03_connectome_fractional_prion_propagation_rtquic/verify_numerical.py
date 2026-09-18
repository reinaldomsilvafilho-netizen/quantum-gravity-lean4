"""
NUMERICAL TEST BATTERY: PILLAR 03 (CONNECTOME FRACTIONAL SPREAD & RT-QuIC)
Verifies 5 core mathematical and neuroimaging obligations:
1. Fractional Graph Laplacian Spectral Non-Negativity (lambda_i^alpha >= 0)
2. Superdiffusive Connectome Acceleration (alpha=0.75 faster than alpha=1.0)
3. Spongiform Damage Monotonicity under Fractional Transport
4. RT-QuIC Inverse Logarithmic Lag Phase Scaling
5. sCJD vs Rapid Dementia Mimic Discrimination (RT-QuIC + Cortical Ribboning)
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Chapters 01, 04, 11 & Paper 2 | DOI: 10.5281/zenodo.22290043
"""

import numpy as np
from model_engine import ConnectomeRTQuICPrionEngine

def run_all_batteries():
    print("=" * 85)
    print("PILLAR 03 PRION VERIFICATION: FRACTIONAL CONNECTOME SPREAD & RT-QuIC")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | Chapters 01, 04, 11 & Paper 2")
    print("=" * 85)

    engine = ConnectomeRTQuICPrionEngine(n_nodes=84, alpha_fractional=0.75)
    all_passed = True

    # ---------------------------------------------------------
    # Battery 1: Fractional Graph Laplacian Spectral Positivity
    # ---------------------------------------------------------
    print("\n[BATTERY 1/5] Fractional Graph Laplacian Spectral Non-Negativity...")
    eigvals = np.linalg.eigvalsh(engine.frac_laplacian)
    min_eig = float(np.min(eigvals))
    max_eig = float(np.max(eigvals))
    
    print(f"  -> Minimum Eigenvalue lambda_min: {min_eig:.2e}")
    print(f"  -> Maximum Eigenvalue lambda_max: {max_eig:.4f}")
    
    if min_eig >= -1e-10 and max_eig > 0.0:
        print("  -> RESULT: PASSED (Battery 1)")
    else:
        print("  -> RESULT: FAILED (Battery 1)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 2: Superdiffusive Accelerated Spreading
    # ---------------------------------------------------------
    print("\n[BATTERY 2/5] Superdiffusive Accelerated Propagation (alpha=0.75 vs 1.0)...")
    # Fractional connectome spread
    _, cri_frac, _ = engine.simulate_connectome_propagation(seed_node=70, t_days=30.0)
    
    # Classical connectome spread (alpha=1.0)
    engine_classic = ConnectomeRTQuICPrionEngine(n_nodes=84, alpha_fractional=1.0)
    _, cri_classic, _ = engine_classic.simulate_connectome_propagation(seed_node=70, t_days=30.0)
    
    print(f"  -> Fractional Cortical Ribboning Index (alpha=0.75): {cri_frac:.4f}")
    print(f"  -> Classical Cortical Ribboning Index  (alpha=1.00): {cri_classic:.4f}")
    
    if cri_frac >= cri_classic - 1e-4:
        print("  -> RESULT: PASSED (Battery 2)")
    else:
        print("  -> RESULT: FAILED (Battery 2)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 3: Total Spongiform Damage Evolution
    # ---------------------------------------------------------
    print("\n[BATTERY 3/5] Temporal Progression of Spongiform Connectome Burden...")
    u_early, _, _ = engine.simulate_connectome_propagation(seed_node=70, t_days=20.0)
    u_late, _, _ = engine.simulate_connectome_propagation(seed_node=70, t_days=80.0)
    
    mean_early = float(np.mean(u_early))
    mean_late = float(np.mean(u_late))
    print(f"  -> Mean Brain Prion Burden (Day 20): {mean_early:.4f}")
    print(f"  -> Mean Brain Prion Burden (Day 80): {mean_late:.4f}")
    
    if mean_late > mean_early and mean_late <= 1.0:
        print("  -> RESULT: PASSED (Battery 3)")
    else:
        print("  -> RESULT: FAILED (Battery 3)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 4: RT-QuIC Inverse Logarithmic Lag Scaling
    # ---------------------------------------------------------
    print("\n[BATTERY 4/5] RT-QuIC Inverse Logarithmic Lag Phase Scaling...")
    titers = [0.01, 0.1, 1.0, 10.0, 100.0]
    lags = [engine.simulate_rtquic_fluorescence(t)['t_lag_hours'] for t in titers]
    
    print(f"  -> Seed Titers (pM):     {titers}")
    print(f"  -> Lag Phase Times (h):  {[round(l, 2) for l in lags]}")
    
    is_strictly_decreasing = all(lags[i] > lags[i+1] for i in range(len(lags)-1))
    if is_strictly_decreasing and lags[-1] < 20.0:
        print("  -> RESULT: PASSED (Battery 4)")
    else:
        print("  -> RESULT: FAILED (Battery 4)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 5: sCJD vs Rapid Dementia Mimic Discrimination
    # ---------------------------------------------------------
    print("\n[BATTERY 5/5] sCJD vs Rapid Dementia Mimic Discrimination...")
    # sCJD patient: high CSF seeds (50 pM) -> fast RT-QuIC lag + high cortical ribboning
    res_scjd = engine.simulate_rtquic_fluorescence(seed_titer_pM=50.0)
    # Mimic (autoimmune encephalitis): zero prion seeds -> flat RT-QuIC
    res_mimic = engine.simulate_rtquic_fluorescence(seed_titer_pM=0.0)
    
    print(f"  -> sCJD Patient: Lag = {res_scjd['t_lag_hours']:.1f}h (sCJD Probability: {res_scjd['prob_scjd_rtquic']:.4f})")
    print(f"  -> Mimic Patient: Lag = {res_mimic['t_lag_hours']:.1f}h (sCJD Probability: {res_mimic['prob_scjd_rtquic']:.4f})")
    
    if res_scjd['prob_scjd_rtquic'] > 0.95 and res_mimic['prob_scjd_rtquic'] < 0.01:
        print("  -> RESULT: PASSED (Battery 5)")
    else:
        print("  -> RESULT: FAILED (Battery 5)")
        all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("PILLAR 03 PRION SUMMARY: 5/5 BATTERIES PASSED (0 FAILURES)")
    else:
        print("PILLAR 03 PRION SUMMARY: TESTS FAILED")
    print("=" * 85)
    return all_passed

if __name__ == '__main__':
    run_all_batteries()
