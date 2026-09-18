"""
CHILDHOOD STUNTING & SIMPLICIAL MICROBIOME-GUT-BRAIN ENGINE (PILLAR 04)
Theoretical Grounding: Treatise Chapter 04 (Simplicial Waves & Fractional Transport) &
Paper 2 (Simplicial Fractional Laplacians on Simplexes, DOI: 10.5281/zenodo.22290043)
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np

class StuntingMicrobiomeEngine:
    def __init__(self, n_taxa=10, alpha_fractional=0.75):
        """
        Microbiome developmental dynamics on the 10-dimensional simplex Delta_9.
        Taxa: [Bifidobacterium, Bacteroides, Faecalibacterium, Roseburia, 
               Ruminococcus, Prevotella, Enterobacteriaceae, Clostridium, Lactobacillus, Akkermansia]
        """
        self.m = n_taxa
        self.alpha = alpha_fractional
        
        # Healthy mature attractor (age 24 months): enriched in Faecalibacterium, Bacteroides, Roseburia
        raw_healthy = np.array([0.15, 0.20, 0.18, 0.14, 0.08, 0.06, 0.02, 0.05, 0.04, 0.08])
        self.p_healthy_basin = raw_healthy / np.sum(raw_healthy)
        
        # Stunted/dysbiotic attractor: collapsed diversity, high Enterobacteriaceae/pathobionts
        raw_stunted = np.array([0.05, 0.04, 0.01, 0.02, 0.03, 0.05, 0.55, 0.15, 0.08, 0.02])
        self.p_stunted_basin = raw_stunted / np.sum(raw_stunted)

    def project_to_simplex(self, relative_abundances):
        """
        Strict simplex projection on Delta_{m-1}.
        """
        pos = np.maximum(relative_abundances, 1e-6)
        return pos / np.sum(pos)

    def compute_bhattacharyya_distance(self, p, q):
        """
        Information distance on the simplex:
        d(p, q) = arccos( sum( sqrt(p_j * q_j) ) )
        """
        bc = np.clip(np.sum(np.sqrt(p * q)), 0.0, 1.0)
        return float(np.arccos(bc))

    def simulate_microbiome_relaxation(self, initial_p, steps=30, dt=0.04, mdcf_intervention=None):
        """
        Ecological basin dynamical relaxation on Delta_{m-1}:
        dp/dt = - grad V(p) + mdcf_forcing
        Bistable potential with separatrix between stunted dysbiotic state and mature healthy state.
        """
        p = np.copy(initial_p)
        for _ in range(steps):
            d_h = self.compute_bhattacharyya_distance(p, self.p_healthy_basin)
            d_s = self.compute_bhattacharyya_distance(p, self.p_stunted_basin)
            
            # Attractor forces
            force_healthy = (self.p_healthy_basin - p) / max(d_h, 0.1)
            force_stunted = (self.p_stunted_basin - p) / max(d_s, 0.1)
            
            # Non-linear bistable vector field
            net_force = 1.2 * force_stunted * np.exp(-2.0 * d_s) + 1.2 * force_healthy * np.exp(-2.0 * d_h)
            
            if mdcf_intervention is not None:
                net_force += 2.2 * mdcf_intervention
                
            p = p + dt * net_force
            p = self.project_to_simplex(p)
            
        return p

    def predict_stunting_and_igf1(self, microbiome_profile, age_months=12.0):
        """
        Predict gut barrier endotoxemia, plasma IGF-1 (ng/mL) and linear growth failure risk (HAZ < -2).
        """
        p = self.project_to_simplex(microbiome_profile)
        d_h = self.compute_bhattacharyya_distance(p, self.p_healthy_basin)
        d_s = self.compute_bhattacharyya_distance(p, self.p_stunted_basin)
        
        # Pathobiont overload (index 6 = Enterobacteriaceae)
        endotoxemia_score = float(p[6] * 10.0)
        
        # Plasma IGF-1 prediction (healthy norm at 12m is ~70-110 ng/mL; stunting drops to <35 ng/mL)
        igf1_ng_ml = float(np.clip(110.0 - 55.0 * d_h - 4.5 * endotoxemia_score, 15.0, 140.0))
        
        # Stunting risk probability
        stunting_logit = -2.5 + 4.2 * d_h - 2.8 * d_s + 0.6 * endotoxemia_score
        prob_stunting = 1.0 / (1.0 + np.exp(-stunting_logit))
        
        return {
            'dist_healthy': float(d_h),
            'dist_stunted': float(d_s),
            'endotoxemia_score': endotoxemia_score,
            'predicted_igf1_ng_ml': igf1_ng_ml,
            'prob_stunting': float(prob_stunting)
        }
