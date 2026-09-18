"""
NEONATAL GENOMIC-METABOLIC SCREENING & SIMPLEX ENGINE (PILLAR 03)
Theoretical Grounding: Treatise Chapter 03 (Continuous Multinomials on Simplexes) &
Chapter 05 (Barnes Lie Transforms & Simplicial Beta-Kernels, DOI: 10.5281/zenodo.22290043)
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np

class NeonatalMetabolicSimplexEngine:
    def __init__(self, n_analytes=8):
        """
        Newborn metabolic screening on the compositional simplex Delta_{m-1}.
        Analytes: [C0 (Free Carnitine), C2, C6, C8, C10, C14:1, Phe, Tyr]
        """
        self.m = n_analytes
        # Healthy newborn reference profile (normalized to simplex)
        # Reference baseline: C0 high, C2 moderate, C8/C10 very low, Phe/Tyr balanced
        raw_healthy = np.array([35.0, 18.0, 0.15, 0.10, 0.12, 0.15, 60.0, 75.0])
        self.p_healthy_ref = raw_healthy / np.sum(raw_healthy)

    def project_to_simplex(self, raw_concentrations):
        """
        Isometrically project raw tandem mass spectrometry (MS/MS) analyte vector to Delta_{m-1}.
        Eliminates spurious total volume dilution (dehydration, TPN infusion volume artifacts).
        """
        pos = np.maximum(raw_concentrations, 1e-6)
        total = np.sum(pos)
        return pos / total

    def compute_fisher_rao_distance(self, p, q):
        """
        Bhattacharyya spherical metric on the open simplex:
        d_FR(p, q) = 2 * arccos( sum( sqrt(p_j * q_j) ) )
        """
        bc = np.sum(np.sqrt(p * q))
        bc_clipped = np.clip(bc, 0.0, 1.0)
        return float(2.0 * np.arccos(bc_clipped))

    def evaluate_enzymatic_block(self, sample_simplex, pathway_pair_indices=(3, 4)):
        """
        Detect enzymatic pathway block by evaluating upstream/downstream flux distortion.
        e.g., MCADD causes C8 accumulation relative to downstream C10: indices (3, 4).
        """
        idx_up, idx_down = pathway_pair_indices
        ratio = sample_simplex[idx_up] / max(sample_simplex[idx_down], 1e-8)
        ref_ratio = self.p_healthy_ref[idx_up] / self.p_healthy_ref[idx_down]
        log_fold_change = np.log2(ratio / ref_ratio)
        return float(ratio), float(log_fold_change)

    def fuse_genomic_metabolomic_evidence(self, raw_ms_ms, genomic_pathogenicity_score=0.1):
        """
        Bayesian fusion of Simplex Information Divergence with Rapid Exome (rWES) Prior:
        P(IEM | Data) = sigmoid( alpha * d_FR + beta * log_FC + gamma * CADD )
        """
        p_sample = self.project_to_simplex(raw_ms_ms)
        d_fr = self.compute_fisher_rao_distance(self.p_healthy_ref, p_sample)
        ratio, lfc = self.evaluate_enzymatic_block(p_sample, pathway_pair_indices=(3, 4))
        
        # Risk logit
        # CADD / REVEL pathogenicity score normalized in [0, 1]
        cadd_norm = float(np.clip(genomic_pathogenicity_score, 0.0, 1.0))
        logit = -4.8 + 5.2 * d_fr + 1.2 * max(0.0, lfc) + 3.5 * cadd_norm
        prob_iem = 1.0 / (1.0 + np.exp(-logit))
        
        return {
            'simplex_profile': p_sample,
            'fisher_rao_dist': float(d_fr),
            'metabolite_ratio': float(ratio),
            'log_fold_change': float(lfc),
            'prob_iem': float(prob_iem)
        }
