"""
Fractional Non-Local Vector-Host & Antibody-Dependent Enhancement (ADE) Engine
Tropical Diseases & Virology Pillar 01: 01_arboviruses_dengue_zika_ade
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Unified Quantum Gravity & Geometric Analysis (DOI: 10.5281/zenodo.22290043)
"""

import numpy as np
import scipy.linalg as la

class ArbovirusFractionalADEEngine:
    """
    Non-Local Fractional Vector-Host Transmission and Antibody-Dependent Enhancement (ADE) Engine
    for Dengue (DENV-1..4), Zika, and Chikungunya arboviruses.
    
    Combines fractional graph Laplacians L_G^alpha for anomalous mosquito-human dispersion
    with Fisher-Rao cross-reactive antigenic distance and sub-neutralizing ADE risk landscapes.
    """
    def __init__(self, alpha=0.75, gamma_ade_max=5.0, ade_peak_titer=160.0, ade_width=0.6):
        self.alpha = alpha                      # Fractional dispersion exponent (0 < alpha <= 1)
        self.gamma_ade_max = gamma_ade_max      # Maximum ADE viremia fold-amplification
        self.ade_peak_titer = ade_peak_titer    # Antibody titer of peak enhancement
        self.ade_width = ade_width              # Log10 width of sub-neutralizing window
        self.adj_ = None
        self.evals_ = None
        self.evecs_ = None
        self.laplacian_alpha_ = None

    def build_urban_mobility_laplacian(self, adjacency_matrix):
        """
        Construct fractional graph Laplacian L_G^alpha = V Lambda^alpha V^T
        modeling anomalous super-diffusive mosquito flight and human urban commuting.
        """
        deg = np.sum(adjacency_matrix, axis=1)
        L = np.diag(deg) - adjacency_matrix
        evals, evecs = la.eigh(L)
        evals = np.maximum(evals, 0.0)
        
        self.adj_ = adjacency_matrix
        self.evals_ = evals
        self.evecs_ = evecs
        self.laplacian_alpha_ = evecs @ np.diag(evals**self.alpha) @ evecs.T
        return self

    def compute_antigenic_distance(self, coords_1, coords_2):
        """
        Compute Riemannian Fisher-Rao distance on viral envelope glycoprotein antigenic space:
        d_FR(s1, s2) = ||theta_1 - theta_2||_2
        """
        c1 = np.array(coords_1, dtype=float)
        c2 = np.array(coords_2, dtype=float)
        return float(np.linalg.norm(c1 - c2))

    def compute_ade_enhancement_factor(self, antibody_titer, antigenic_distance=1.0):
        """
        Compute Antibody-Dependent Enhancement (ADE) multiplier:
        gamma(titer, d) = 1 + (gamma_max - 1) * exp(-0.5 * ((log10(titer) - peak)/width)^2) * w(d).
        Peaks in the sub-neutralizing antibody window; vanishes at zero or high neutralizing titers.
        """
        titer = np.maximum(antibody_titer, 1.0)
        log_t = np.log10(titer)
        peak_log = np.log10(self.ade_peak_titer)
        
        # Bell-shaped curve in sub-neutralizing titer window
        titer_factor = np.exp(-0.5 * ((log_t - peak_log) / self.ade_width)**2)
        
        # Antigenic cross-reactivity weight: optimal ADE occurs at moderate cross-reactivity
        # (identical serotype neutralizes; highly divergent serotype does not bind)
        antigenic_factor = np.exp(-0.5 * ((antigenic_distance - 1.2) / 0.8)**2)
        
        enhancement = 1.0 + (self.gamma_ade_max - 1.0) * titer_factor * antigenic_factor
        return float(enhancement)

    def simulate_multiserotype_transmission(self, initial_infected, time_steps=10, dt=0.1, ade_boost=1.0):
        """
        Simulate spatial fractional epidemic spread across urban neighborhoods:
        u(t+dt) = exp(-dt * ade_boost * L_G^alpha) u(t)
        Preserves total infected load while capturing super-diffusive jumps.
        """
        trajectory = [initial_infected.copy()]
        curr_u = initial_infected.copy()
        
        for _ in range(time_steps):
            coeffs = self.evecs_.T @ curr_u
            decay = np.exp(-dt * ade_boost * self.evals_**self.alpha)
            next_u = self.evecs_ @ (coeffs * decay)
            next_u = np.maximum(0.0, next_u)
            # Mass conservation
            next_u = next_u / (np.sum(next_u) + 1e-8) * np.sum(initial_infected)
            trajectory.append(next_u)
            curr_u = next_u
            
        return np.array(trajectory)

    def predict_severe_dengue_risk(self, pre_existing_titer, primary_serotype, secondary_serotype, serotype_map):
        """
        Predict probability of Severe Dengue (Dengue Hemorrhagic Fever / Shock Syndrome)
        based on cross-reactive titer and antigenic distance between serotypes.
        """
        coords_1 = serotype_map[primary_serotype]
        coords_2 = serotype_map[secondary_serotype]
        d_antigenic = self.compute_antigenic_distance(coords_1, coords_2)
        
        if primary_serotype == secondary_serotype:
            # Homologous re-challenge: sterilizing immunity, zero ADE risk
            return 0.01
            
        ade_factor = self.compute_ade_enhancement_factor(pre_existing_titer, d_antigenic)
        # Logistic risk mapping
        z = 1.5 * (ade_factor - 2.5)
        return float(1.0 / (1.0 + np.exp(-z)))
