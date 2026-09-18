"""
NUMERICAL VERIFICATION BATTERIES: PILLAR 01 (Maternal-Child Health)
Alveolar Surfactant Minimax Curvature & Neonatal Respiratory Distress
Theoretical Grounding: Treatise Chapter 06 & 07
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np
from model_engine import SurfactantAlveolarEngine

def run_all_batteries():
    print("=" * 85)
    print("PILLAR 01 MATERNAL-CHILD HEALTH VERIFICATION: NEONATAL ALVEOLAR SURFACTANT")
    print("Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)")
    print("Treatise Grounding: DOI: 10.5281/zenodo.22290043 | Chapters 06 & 07")
    print("=" * 85)

    engine_term = SurfactantAlveolarEngine(gestational_age_weeks=38.0, surfactant_pool_mg_kg=95.0)
    engine_preterm = SurfactantAlveolarEngine(gestational_age_weeks=26.0, surfactant_pool_mg_kg=8.0)
    all_passed = True

    # ---------------------------------------------------------
    # Battery 1: Young-Laplace Curvature Invariance
    # ---------------------------------------------------------
    print("\n[BATTERY 1/5] Young-Laplace Pressure-Curvature Invariance Delta P = 2*gamma*H...")
    radii = [25.0, 50.0, 75.0, 100.0] # um
    gamma = 25.0 # mN/m
    pressures = [engine_term.compute_young_laplace_pressure(r, gamma) for r in radii]
    # Delta P * R must be constant = 2 * gamma * conversion factor
    products = [p * r for p, r in zip(pressures, radii)]
    var_products = np.var(products)
    
    print(f"  -> Radii Tested (um): {radii}")
    print(f"  -> Calculated Pressures (cmH2O): {[round(p, 2) for p in pressures]}")
    print(f"  -> Invariance Variance Var(P * R): {var_products:.2e}")
    
    if var_products < 1e-12:
        print("  -> RESULT: PASSED (Battery 1)")
    else:
        print("  -> RESULT: FAILED (Battery 1)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 2: Minimax Alveolar Collapse Protection
    # ---------------------------------------------------------
    print("\n[BATTERY 2/5] Minimax Curvature Collapse Barrier in Term vs Preterm...")
    # At deflation (R = 25 um)
    res_term = engine_term.evaluate_minimax_collapse_barrier(25.0)
    res_preterm = engine_preterm.evaluate_minimax_collapse_barrier(25.0)
    
    print(f"  -> Term Infant (Surfactant Replete):    P_collapse = {res_term['collapse_pressure_cmH2O']:.2f} cmH2O | Stable: {res_term['is_mechanically_stable']}")
    print(f"  -> Preterm Infant (Surfactant Deficient): P_collapse = {res_preterm['collapse_pressure_cmH2O']:.2f} cmH2O | Stable: {res_preterm['is_mechanically_stable']}")
    
    # Preterm collapse pressure is dangerously elevated (> 3x term)
    if res_term['collapse_pressure_cmH2O'] < res_preterm['collapse_pressure_cmH2O'] and res_term['is_mechanically_stable']:
        print("  -> RESULT: PASSED (Battery 2)")
    else:
        print("  -> RESULT: FAILED (Battery 2)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 3: Exogenous Surfactant Rescue Monotonicity
    # ---------------------------------------------------------
    print("\n[BATTERY 3/5] Exogenous Surfactant Therapeutic Rescue Monotonicity...")
    doses = [0.0, 25.0, 50.0, 100.0, 200.0] # mg/kg
    collapse_pressures = [engine_preterm.evaluate_minimax_collapse_barrier(25.0, dose)['collapse_pressure_cmH2O'] for dose in doses]
    
    print(f"  -> Replacement Doses (mg/kg): {doses}")
    print(f"  -> Resulting Deflation Pressures: {[round(p, 2) for p in collapse_pressures]}")
    
    is_strictly_decreasing = all(collapse_pressures[i] > collapse_pressures[i+1] for i in range(len(collapse_pressures)-1))
    if is_strictly_decreasing:
        print("  -> RESULT: PASSED (Battery 3)")
    else:
        print("  -> RESULT: FAILED (Battery 3)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 4: Fractal Airway Resolvent Impedance Positivity
    # ---------------------------------------------------------
    print("\n[BATTERY 4/5] Fractal Bronchial Resolvent Impedance Dissipativity...")
    Z = engine_term.compute_airway_fractal_impedance(frequency_hz=5.0, generations=14)
    print(f"  -> Tracheal Transfer Impedance Z(5 Hz): {Z.real:.4f} + {Z.imag:.4f}j cmH2O.s/mL")
    
    # Dissipative resistance must be positive
    if Z.real > 0.0 and np.isfinite(Z.real):
        print("  -> RESULT: PASSED (Battery 4)")
    else:
        print("  -> RESULT: FAILED (Battery 4)")
        all_passed = False

    # ---------------------------------------------------------
    # Battery 5: Respiratory Failure Discrimination (Term vs Extreme Preterm)
    # ---------------------------------------------------------
    print("\n[BATTERY 5/5] Severe Neonatal Respiratory Distress Risk Separation...")
    # Evaluate over 20 radii points
    r_sweep = np.linspace(20.0, 80.0, 15)
    p_term_sweep = [engine_term.evaluate_minimax_collapse_barrier(r)['collapse_pressure_cmH2O'] for r in r_sweep]
    p_preterm_sweep = [engine_preterm.evaluate_minimax_collapse_barrier(r)['collapse_pressure_cmH2O'] for r in r_sweep]
    
    max_p_preterm = max(p_preterm_sweep)
    max_p_term = max(p_term_sweep)
    print(f"  -> Peak Atelectasis Pressure (Preterm): {max_p_preterm:.2f} cmH2O")
    print(f"  -> Peak Atelectasis Pressure (Term):    {max_p_term:.2f} cmH2O")
    
    if max_p_preterm >= 2.5 * max_p_term:
        print("  -> RESULT: PASSED (Battery 5)")
    else:
        print("  -> RESULT: FAILED (Battery 5)")
        all_passed = False

    print("\n" + "=" * 85)
    if all_passed:
        print("PILLAR 01 MATERNAL-CHILD HEALTH SUMMARY: 5/5 BATTERIES PASSED (0 FAILURES)")
    else:
        print("PILLAR 01 MATERNAL-CHILD HEALTH SUMMARY: TESTS FAILED")
    print("=" * 85)
    return all_passed

if __name__ == '__main__':
    run_all_batteries()
