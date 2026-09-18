"""
MINIMAX EXTRINSIC CURVATURE END-CAPPING & PHARMACOLOGICAL CHAPERONE ENGINE
Models targeted arrest of sCJD replication via cross-beta fibril capping and PrPC stabilization
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Chapters 07 & 11 (Minimax Obstacle Bounds & Caffarelli Detachment Barriers)
"""

import numpy as np

class AntiPrionTherapeuticsEngine:
    """
    Simulates dual-action anti-prion therapeutics:
    1. Cross-beta fibril end-capping macrocycles (blocking elongation & secondary nucleation)
    2. Native PrPC alpha-fold pharmacological chaperones (elevating activation barrier Delta G^dagger)
    """
    def __init__(self, t_kelvin=310.15):
        self.T = t_kelvin
        self.RT = 0.0019872 * self.T # ~ 0.616 kcal/mol
        self.kappa_fibril_target = 0.08 # Target cross-beta terminal strand curvature (A^-1)

    def compute_capping_affinity(self, kappa_peptidomimetic, kd_optimal_nM=0.25):
        """
        Theorem 7.2: Minimax curvature matching.
        Binding affinity Kd degrades exponentially with curvature mismatch:
        Kd = Kd_0 * exp(gamma * (kappa* - kappa_target)^2)
        """
        curvature_mismatch = abs(float(kappa_peptidomimetic) - self.kappa_fibril_target)
        # Bending penalty parameter gamma ~ 450 A^2
        kd_nM = float(kd_optimal_nM * np.exp(450.0 * (curvature_mismatch ** 2)))
        return min(kd_nM, 1e7)

    def compute_fibril_capping_fraction(self, drug_conc_nM, kd_nM):
        """
        Langmuir adsorption isotherm for terminal cross-beta capping:
        theta_cap = [Drug] / ([Drug] + Kd)
        """
        c = max(0.0, float(drug_conc_nM))
        theta = float(c / (c + kd_nM + 1e-12))
        return np.clip(theta, 0.0, 1.0)

    def compute_monomer_stabilization_delta_g(self, chaperone_conc_uM, kd_fold_uM=0.50):
        """
        Thermodynamic linkage relation for PrPC alpha-fold stabilization:
        Delta Delta G_stab = RT * ln(1 + [Chaperone] / Kd_fold)
        Elevates the misfolding barrier Delta G^dagger, freezing spontaneous conversion.
        """
        c = max(0.0, float(chaperone_conc_uM))
        delta_delta_g = float(self.RT * np.log(1.0 + c / kd_fold_uM))
        return delta_delta_g

    def evaluate_anti_prion_therapeutic_efficacy(self, drug_conc_nM, kappa_peptidomimetic,
                                                 chaperone_conc_uM=10.0):
        """
        Calculates total replication inhibition percentage and clinical neuroprotective rescue:
        v_elong / v_0 = (1 - theta_cap)
        k_conv / k_0 = exp(- Delta Delta G_stab / RT)
        Net Replication Flux: J = (1 - theta_cap) * exp(- Delta Delta G_stab / RT)
        """
        kd_cap_nM = self.compute_capping_affinity(kappa_peptidomimetic)
        theta_cap = self.compute_fibril_capping_fraction(drug_conc_nM, kd_cap_nM)
        delta_g_stab = self.compute_monomer_stabilization_delta_g(chaperone_conc_uM)
        
        # Residual replication flux:
        residual_flux = (1.0 - theta_cap) * np.exp(- delta_g_stab / self.RT)
        inhibition_pct = float((1.0 - residual_flux) * 100.0)
        
        # Survival prolongation factor:
        survival_extension_ratio = float(1.0 / (max(residual_flux, 1e-4) ** 0.6))
        
        # Probability of complete therapeutic arrest / sCJD rescue:
        prob_rescue = float(1.0 / (1.0 + np.exp(-(inhibition_pct - 85.0) / 4.0)))
        
        return {
            'capping_kd_nM': float(kd_cap_nM),
            'capping_fraction': float(theta_cap),
            'stabilization_delta_g_kcal': float(delta_g_stab),
            'inhibition_percent': float(inhibition_pct),
            'survival_extension_factor': float(survival_extension_ratio),
            'prob_scjd_rescue': float(prob_rescue)
        }
