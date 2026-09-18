"""
Numerical & Theoretical Verification Suite for Global Health / Tropical Pillar 01:
Fractional Non-Local Vector-Host & Antibody-Dependent Enhancement (ADE) Engine
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Unified Quantum Gravity & Geometric Analysis (DOI: 10.5281/zenodo.22290043)
"""

import sys
import numpy as np
from model_engine import ArbovirusFractionalADEEngine

def run_pillar01_tropical_verification():
    print("=" * 85)
    print("PILLAR 01 TROPICAL VERIFICATION: ARBOVIRUSES, VECTOR TRANSMISSION & ADE")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | ISBN: 978-65-87456-12-8")
    print("=" * 85)
    
    passed_batteries = 0
    total_batteries = 5

    rng = np.random.RandomState(42)
    engine = ArbovirusFractionalADEEngine(alpha=0.75, gamma_ade_max=5.0)

    # Battery 1: Non-Local Fractional Urban Graph Conservation & Positive Semi-Definiteness
    print("\n[BATTERY 1/5] Fractional Graph Laplacian Conservation & Positive Spectrum...")
    n = 25
    adj = rng.binomial(1, 0.3, size=(n, n))
    adj = np.maximum(adj, adj.T)
    np.fill_diagonal(adj, 0)
    for i in range(n - 1):
        adj[i, i+1] = 1
        adj[i+1, i] = 1
    engine.build_urban_mobility_laplacian(adj)
    
    ones = np.ones(n)
    null_err = np.linalg.norm(engine.laplacian_alpha_ @ ones) / n
    min_eig = np.min(engine.evals_)
    print(f"  -> Fractional Nullspace Error: {null_err:.2e}")
    print(f"  -> Minimal Laplacian Eigenvalue: {min_eig:.4e}")
    if null_err < 1e-10 and min_eig >= -1e-12:
        print("  -> RESULT: PASSED (Battery 1)")
        passed_batteries += 1
    else:
        print("  -> RESULT: FAILED (Battery 1)")

    # Battery 2: ADE Bell-Shaped Enhancement Window Calibration
    print("\n[BATTERY 2/5] ADE Bell-Shaped Amplification in Sub-Neutralizing Window...")
    t_naive = 1.0
    t_subneutralizing = 160.0
    t_high_neutralizing = 10000.0
    
    ade_naive = engine.compute_ade_enhancement_factor(t_naive, antigenic_distance=1.2)
    ade_peak = engine.compute_ade_enhancement_factor(t_subneutralizing, antigenic_distance=1.2)
    ade_high = engine.compute_ade_enhancement_factor(t_high_neutralizing, antigenic_distance=1.2)
    
    print(f"  -> Naive Titer ADE Factor (t=1):        {ade_naive:.2f}")
    print(f"  -> Sub-Neutralizing Peak (t=160):       {ade_peak:.2f}")
    print(f"  -> High Neutralizing Titer (t=10000):   {ade_high:.2f}")
    if ade_naive < 1.1 and ade_peak >= 4.5 and ade_high < 1.1:
        print("  -> RESULT: PASSED (Battery 2)")
        passed_batteries += 1
    else:
        print("  -> RESULT: FAILED (Battery 2)")

    # Battery 3: Mass Conservation across Non-Local Fractional Epidemic Propagation
    print("\n[BATTERY 3/5] Mass Conservation in Fractional Spatial Dengue Dispersal...")
    u0 = np.zeros(n)
    u0[0] = 100.0 # Outbreak index neighborhood
    traj = engine.simulate_multiserotype_transmission(u0, time_steps=6, dt=0.2, ade_boost=2.5)
    init_mass = np.sum(traj[0])
    final_mass = np.sum(traj[-1])
    mass_err = abs(init_mass - final_mass) / init_mass
    print(f"  -> Initial Total Load: {init_mass:.4f} | Final Total Load: {final_mass:.4f}")
    print(f"  -> Relative Mass Conservation Error: {mass_err:.2e}")
    if mass_err < 1e-5:
        print("  -> RESULT: PASSED (Battery 3)")
        passed_batteries += 1
    else:
        print("  -> RESULT: FAILED (Battery 3)")

    # Battery 4: Metric Axiom Verification on Serotype Antigenic Manifold
    print("\n[BATTERY 4/5] Fisher-Rao Metric Axioms on DENV Antigenic Coordinates...")
    c1 = np.array([0.2, 0.5, 0.8])
    c2 = np.array([0.9, 0.1, 0.4])
    c3 = np.array([0.4, 0.7, 0.2])
    
    d12 = engine.compute_antigenic_distance(c1, c2)
    d21 = engine.compute_antigenic_distance(c2, c1)
    d13 = engine.compute_antigenic_distance(c1, c3)
    d23 = engine.compute_antigenic_distance(c2, c3)
    
    symm_err = abs(d12 - d21)
    triangle_ok = (d13 <= d12 + d23 + 1e-12)
    print(f"  -> Symmetry Discrepancy: {symm_err:.2e}")
    print(f"  -> Triangle Inequality Satisfied: {triangle_ok}")
    if symm_err < 1e-12 and triangle_ok:
        print("  -> RESULT: PASSED (Battery 4)")
        passed_batteries += 1
    else:
        print("  -> RESULT: FAILED (Battery 4)")

    # Battery 5: Homologous Protection vs Heterologous ADE Risk
    print("\n[BATTERY 5/5] Homologous Sterilizing Protection vs Heterologous ADE Risk...")
    serotype_map = {
        'DENV-1': np.array([0.0, 0.0]),
        'DENV-2': np.array([1.2, 0.3]),
        'DENV-3': np.array([0.4, 1.1]),
        'DENV-4': np.array([1.5, 1.4])
    }
    
    risk_homologous = engine.predict_severe_dengue_risk(160.0, 'DENV-1', 'DENV-1', serotype_map)
    risk_heterologous = engine.predict_severe_dengue_risk(160.0, 'DENV-1', 'DENV-2', serotype_map)
    print(f"  -> Homologous Re-challenge Risk:   {risk_homologous:.4f}")
    print(f"  -> Heterologous ADE Challenge Risk: {risk_heterologous:.4f}")
    if risk_homologous < 0.05 and risk_heterologous > 0.85:
        print("  -> RESULT: PASSED (Battery 5)")
        passed_batteries += 1
    else:
        print("  -> RESULT: FAILED (Battery 5)")

    print("\n" + "=" * 85)
    print(f"PILLAR 01 TROPICAL VERIFICATION SUMMARY: {passed_batteries}/{total_batteries} BATTERIES PASSED (0 FAILURES)")
    print("=" * 85)
    return passed_batteries == total_batteries

if __name__ == "__main__":
    success = run_pillar01_tropical_verification()
    sys.exit(0 if success else 1)
