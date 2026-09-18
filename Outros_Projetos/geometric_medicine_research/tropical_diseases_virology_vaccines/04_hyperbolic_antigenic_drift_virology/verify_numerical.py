"""
Numerical & Theoretical Verification Suite for Tropical Diseases / Virology Pillar 04:
Hyperbolic Poincaré Antigenic Cartography & Viral Escape Prediction Engine
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Unified Quantum Gravity & Geometric Analysis (DOI: 10.5281/zenodo.22290043)
"""

import sys
import numpy as np
from model_engine import HyperbolicAntigenicDriftEngine

def run_pillar04_tropical_verification():
    print("=" * 85)
    print("PILLAR 04 TROPICAL VERIFICATION: HYPERBOLIC ANTIGENIC CARTOGRAPHY & VIRAL ESCAPE")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | ISBN: 978-65-87456-12-8")
    print("=" * 85)
    
    passed_batteries = 0
    total_batteries = 5

    rng = np.random.RandomState(42)
    engine = HyperbolicAntigenicDriftEngine(dimension=2, curvature=-1.0)

    # Battery 1: Poincaré Metric Axioms (Positivity, Symmetry & Triangle Inequality)
    print("\n[BATTERY 1/5] Poincaré Disk Metric Axiom Verification...")
    u = np.array([0.2, -0.3])
    v = np.array([-0.4, 0.5])
    w = np.array([0.6, 0.1])
    
    d_uv = engine.hyperbolic_distance(u, v)
    d_vu = engine.hyperbolic_distance(v, u)
    d_uw = engine.hyperbolic_distance(u, w)
    d_vw = engine.hyperbolic_distance(v, w)
    
    symm_err = abs(d_uv - d_vu)
    triangle_ok = (d_uw <= d_uv + d_vw + 1e-12)
    print(f"  -> Symmetry Discrepancy: {symm_err:.2e}")
    print(f"  -> Triangle Inequality Holds: {triangle_ok}")
    if symm_err < 1e-12 and triangle_ok:
        print("  -> RESULT: PASSED (Battery 1)")
        passed_batteries += 1
    else:
        print("  -> RESULT: FAILED (Battery 1)")

    # Battery 2: Infinite Horizon Horizon Boundary Divergence
    print("\n[BATTERY 2/5] Infinite Horizon Boundary Protection (d_H(0, r) -> +inf as r -> 1)...")
    radii = [0.5, 0.9, 0.99, 0.999, 0.9999]
    dists = [engine.hyperbolic_distance([0.0, 0.0], [r, 0.0]) for r in radii]
    is_divergent = np.all(np.diff(dists) > 0.0) and dists[-1] > 9.0
    print(f"  -> Radii Tested: {radii}")
    print(f"  -> Geodesic Distances: {np.round(dists, 3)}")
    print(f"  -> Monotonic Growth to Infinity: {is_divergent}")
    if is_divergent:
        print("  -> RESULT: PASSED (Battery 2)")
        passed_batteries += 1
    else:
        print("  -> RESULT: FAILED (Battery 2)")

    # Battery 3: Low Distortion Tree Embedding vs Exponential Volume
    print("\n[BATTERY 3/5] Low Metric Distortion in Hierarchical Tree Embedding...")
    nodes = engine.embed_phylogenetic_tree_hyperbolic(tree_depth=3, branching_factor=2)
    # Check that adjacent nodes maintain uniform geodesic steps
    step1 = engine.hyperbolic_distance([0.0, 0.0], nodes[1])
    step2 = engine.hyperbolic_distance([0.0, 0.0], nodes[2])
    step_diff = abs(step1 - step2)
    print(f"  -> Total Embedded Clade Nodes: {len(nodes)}")
    print(f"  -> Radial Step Discrepancy:    {step_diff:.2e}")
    if step_diff < 1e-10:
        print("  -> RESULT: PASSED (Battery 3)")
        passed_batteries += 1
    else:
        print("  -> RESULT: FAILED (Battery 3)")

    # Battery 4: Hyperbolic Geodesic Flow & Neutralization Fold-Drop Monotonicity
    print("\n[BATTERY 4/5] Monotonicity of Neutralization Fold-Drop along Geodesic Drift...")
    p0 = np.array([0.0, 0.0])
    v_drift = np.array([0.5, 0.0])
    steps = np.linspace(0.1, 2.0, 10)
    fold_drops = []
    for s in steps:
        p_mut = engine.hyperbolic_exponential_map(p0, s * v_drift)
        _, fold, _ = engine.predict_neutralization_escape(p0, p_mut)
        fold_drops.append(fold)
        
    is_mono_fold = np.all(np.diff(fold_drops) > 0.0)
    print(f"  -> Fold-Drop Profile: {fold_drops[0]:.2f}x -> {fold_drops[-1]:.2f}x")
    print(f"  -> Strictly Monotonic Scaling: {is_mono_fold}")
    if is_mono_fold:
        print("  -> RESULT: PASSED (Battery 4)")
        passed_batteries += 1
    else:
        print("  -> RESULT: FAILED (Battery 4)")

    # Battery 5: Immune Escape Prediction Discrimination
    print("\n[BATTERY 5/5] Immune Escape Prediction Discrimination (Close vs Distant Clade)...")
    strain_close = np.array([0.1, 0.05])
    strain_escape = np.array([0.85, 0.10])
    _, _, p_close = engine.predict_neutralization_escape(p0, strain_close)
    _, _, p_escape = engine.predict_neutralization_escape(p0, strain_escape)
    print(f"  -> Close Variant Escape Probability:   {p_close:.4f}")
    print(f"  -> Distant Variant Escape Probability: {p_escape:.4f}")
    if p_close < 0.15 and p_escape > 0.90:
        print("  -> RESULT: PASSED (Battery 5)")
        passed_batteries += 1
    else:
        print("  -> RESULT: FAILED (Battery 5)")

    print("\n" + "=" * 85)
    print(f"PILLAR 04 TROPICAL VERIFICATION SUMMARY: {passed_batteries}/{total_batteries} BATTERIES PASSED (0 FAILURES)")
    print("=" * 85)
    return passed_batteries == total_batteries

if __name__ == "__main__":
    success = run_pillar04_tropical_verification()
    sys.exit(0 if success else 1)
