"""
PREECLAMPSIA PLACENTAL ISCHEMIA & RIEMANNIAN SPIRAL ARTERY ENGINE (PILLAR 02)
Theoretical Grounding: Treatise Chapter 02 (Geometric Flows on Tensor Manifolds) &
Chapter 08 (Space Forms and ADM Decomposition, DOI: 10.5281/zenodo.22290043)
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np
from scipy.linalg import logm, expm

class PreeclampsiaPlacentalEngine:
    def __init__(self, gestational_age_weeks=12.0):
        """
        Placental vascular hemodynamics and uterine spiral artery remodeling.
        """
        self.ga = gestational_age_weeks
        # Canonical reference tensor for completely remodeled, low-resistance term spiral artery
        self.G_healthy_ref = np.diag([3.5, 3.2, 0.8]) # High radial/circumferential compliance, low axial resistance

    def compute_affine_invariant_distance(self, G1, G2):
        """
        Geodesic distance on the Riemannian symmetric cone S_{++}^3:
        d_AI(G1, G2) = || log( G1^{-1/2} G2 G1^{-1/2} ) ||_F
        """
        w1, v1 = np.linalg.eigh(G1)
        w1_safe = np.maximum(w1, 1e-12)
        G1_inv_sqrt = v1 @ np.diag(1.0 / np.sqrt(w1_safe)) @ v1.T
        
        M = G1_inv_sqrt @ G2 @ G1_inv_sqrt
        w_m = np.linalg.eigvalsh(M)
        w_m_safe = np.maximum(w_m, 1e-12)
        log_eigs = np.log(w_m_safe)
        dist = np.sqrt(np.sum(log_eigs**2))
        return float(dist)

    def simulate_trophoblast_ricci_flow(self, G_initial, steps=20, dt=0.05, trophoblast_invasion_rate=0.8):
        """
        Simulate spiral artery endovascular remodeling:
        dG/dt = - 2 * Ric(G) + invasion_rate * (G_healthy - G)
        Under successful invasion, vessel dilates and loss of muscularis layer expands lumen.
        """
        G = np.copy(G_initial)
        for _ in range(steps):
            # Effective vascular Ricci curvature relaxation
            dG = trophoblast_invasion_rate * (self.G_healthy_ref - G)
            G = G + dt * dG
            # Ensure positive definiteness
            w, v = np.linalg.eigh(G)
            w = np.maximum(w, 0.05)
            G = v @ np.diag(w) @ v.T
        return G

    def evaluate_doppler_waveforms(self, impedance_tensor):
        """
        Derive clinical uterine artery Doppler velocimetry parameters:
        Pulsatility Index (PI), Resistive Index (RI), and Diastolic Notch Depth.
        """
        # Axial flow conductance is inversely related to G[2, 2]
        r_axial = impedance_tensor[2, 2]
        c_radial = impedance_tensor[0, 0]
        
        # Peak Systolic Velocity (PSV) and End-Diastolic Velocity (EDV)
        psv = 85.0 / np.sqrt(r_axial)
        edv = psv * (c_radial / (c_radial + 2.5 * r_axial))
        
        v_mean = (psv + 2.0 * edv) / 3.0
        pi = (psv - edv) / max(v_mean, 1.0)
        ri = (psv - edv) / max(psv, 1.0)
        
        # Early diastolic notch depth: elevated when radial compliance is low
        notch_depth = max(0.0, 1.0 - (c_radial / 2.0))
        return float(pi), float(ri), float(notch_depth)

    def predict_preeclampsia_risk(self, patient_tensor, sflt_plgf_ratio=15.0):
        """
        Integrated Preeclampsia Risk Index (PRI):
        Combines Riemannian distance to healthy remodeling with angiogenic biomarker imbalance.
        """
        d_riemann = self.compute_affine_invariant_distance(self.G_healthy_ref, patient_tensor)
        pi, _, notch = self.evaluate_doppler_waveforms(patient_tensor)
        
        # High sFlt-1/PlGF ratio (>38 in 2nd trimester or >85 in 3rd trimester marks severe endothelial damage)
        angiogenic_score = np.log1p(max(0.0, sflt_plgf_ratio))
        
        # Risk logit
        risk_logit = -4.5 + 1.2 * d_riemann + 0.8 * pi + 1.5 * notch + 0.4 * angiogenic_score
        prob_preeclampsia = 1.0 / (1.0 + np.exp(-risk_logit))
        return float(d_riemann), float(pi), float(prob_preeclampsia)
