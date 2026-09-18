"""
TREATMENT-RESISTANT DEPRESSION & FISHER-RAO DMN ATTRACTOR ENGINE (PILLAR 01)
Theoretical Grounding: Treatise Chapter 10 (Information Geometry & Statistical Manifolds,
DOI: 10.5281/zenodo.22290043)
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np

class DepressionAttractorEngine:
    def __init__(self, n_regions=8):
        """
        Brain functional connectome statistical manifold.
        Nodes 0..3: Default Mode Network (DMN: mPFC, PCC, Bilateral Angular)
        Nodes 4..7: Central Executive Network (CEN: Bilateral dlPFC, dACC, Parietal)
        """
        self.n_nodes = n_regions

    def compute_fisher_rao_information_curvature(self, covariance_matrix):
        """
        Information metric curvature on the Gaussian statistical manifold:
        g^F = 0.5 * (Sigma^{-1} tensor Sigma^{-1})
        The trace norm of the Fisher-Rao Riemannian curvature tensor quantifies
        the depth and rigidity of the cognitive rumination attractor well.
        """
        # Regularize
        cov_safe = covariance_matrix + 1e-5 * np.eye(self.n_nodes)
        cov_inv = np.linalg.inv(cov_safe)
        
        # Information metric scalar curvature proxy: Tr(cov_inv^2)
        curvature_scalar = np.trace(cov_inv @ cov_inv) / (self.n_nodes**2)
        
        # DMN internal hyper-coupling ratio
        dmn_cov = cov_safe[:4, :4]
        cen_cov = cov_safe[4:, 4:]
        cross_cov = cov_safe[:4, 4:]
        
        dmn_strength = np.mean(np.abs(dmn_cov))
        cen_strength = np.mean(np.abs(cen_cov))
        cross_strength = np.mean(np.abs(cross_cov))
        
        rigidity_index = dmn_strength / max(cross_strength, 1e-4)
        return float(curvature_scalar), float(rigidity_index), float(cross_strength)

    def simulate_rapid_ketamine_remission(self, initial_cov, ketamine_dose_effect=0.8):
        """
        Ketamine / Psilocybin / TMS dynamical isometry reset:
        Disrupts hyper-rigid DMN attractor by injecting neural entropy and restoring DMN-CEN cross-talk.
        """
        cov = np.copy(initial_cov)
        # Entropy injection weakens pathological DMN hyper-synchrony and restores prefrontal CEN control
        cov[:4, :4] *= (1.0 - 0.55 * ketamine_dose_effect)
        cov[:4, 4:] += 0.20 * ketamine_dose_effect * np.ones((4, 4))
        cov[4:, :4] = cov[:4, 4:].T
        
        # Guarantee positive definiteness
        w, v = np.linalg.eigh(cov)
        w = np.maximum(w, 0.05)
        return v @ np.diag(w) @ v.T

    def predict_treatment_response_and_suicide_risk(self, cov_matrix, baseline_madrs=38.0):
        """
        Predict probability of rapid clinical response (>=50% MADRS drop at 24h)
        and Acute Suicide Crisis Risk Index.
        """
        curv, rigidity, cross = self.compute_fisher_rao_information_curvature(cov_matrix)
        
        # High rumination rigidity + low cognitive CEN cross-talk drives high suicide crisis risk
        suicide_logit = np.clip(-3.2 + 0.15 * rigidity - 3.5 * cross + 0.05 * (baseline_madrs - 30.0), -40.0, 40.0)
        prob_suicide_crisis = 1.0 / (1.0 + np.exp(-suicide_logit))
        
        # Response to ketamine is highest when DMN rigidity is reversible (rigidity drops, cross-talk restored)
        response_logit = np.clip(3.5 - 0.25 * rigidity + 6.0 * cross, -40.0, 40.0)
        prob_response = 1.0 / (1.0 + np.exp(-response_logit))
        
        return {
            'information_curvature': float(curv),
            'dmn_rigidity_index': float(rigidity),
            'cen_cross_talk': float(cross),
            'prob_suicide_crisis': float(prob_suicide_crisis),
            'prob_treatment_response': float(prob_response)
        }
