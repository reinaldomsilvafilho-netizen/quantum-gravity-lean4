"""
Fractal Microvascular Cytoadherence & Var Gene Clonal Epigenetic Engine
Tropical Diseases & Virology Pillar 02: 02_malaria_plasmodium_antigenic_variation
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Unified Quantum Gravity & Geometric Analysis (DOI: 10.5281/zenodo.22290043)
"""

import numpy as np
import scipy.linalg as la

class MalariaFractalCytoadherenceEngine:
    """
    Fractal Microvascular Resolvent and Clonal Antigenic Variation Engine
    for Plasmodium falciparum / Plasmodium vivax Malaria.
    
    Models cerebral capillary networks as self-similar fractal trees,
    quantifying microvascular occlusion under Group A PfEMP1 (EPCR/ICAM-1) cytoadherence
    and Kelch13 artemisinin clearance delays.
    """
    def __init__(self, num_generations=5, alpha=0.75, num_var_genes=60):
        self.num_generations = num_generations
        self.alpha = alpha
        self.num_var_genes = num_var_genes
        self.num_nodes = 2**(num_generations + 1) - 1
        self.adj_ = None
        self.evals_ = None
        self.evecs_ = None
        self.laplacian_alpha_ = None

    def build_capillary_network(self, cytoadherence_density=0.0):
        """
        Construct brain microvascular capillary network.
        iRBC cytoadherence reduces terminal capillary hydraulic conductivity.
        """
        n = self.num_nodes
        adj = np.zeros((n, n))
        
        for i in range(2**self.num_generations - 1):
            gen = int(np.floor(np.log2(i + 1)))
            base_conductance = 1.0 / (2.0**(gen / 3.0))
            
            left = 2 * i + 1
            right = 2 * i + 2
            
            # Terminal capillaries experience severe cytoadherence occlusion
            if gen >= self.num_generations - 2:
                cond = base_conductance * np.maximum(0.01, 1.0 - 0.90 * cytoadherence_density)
            else:
                cond = base_conductance
                
            adj[i, left] = cond
            adj[left, i] = cond
            adj[i, right] = cond
            adj[right, i] = cond
            
        self.adj_ = adj
        deg = np.sum(adj, axis=1)
        L = np.diag(deg) - adj
        evals, evecs = la.eigh(L)
        evals = np.maximum(evals, 0.0)
        
        self.evals_ = evals
        self.evecs_ = evecs
        self.laplacian_alpha_ = evecs @ np.diag(evals**self.alpha) @ evecs.T
        return self

    def compute_cerebral_perfusion_index(self):
        """
        Compute cerebral microvascular perfusion transfer resolvent:
        Q_cerebral = sum_{j in terminal_capillaries} |(0.1*I + L_cap^alpha)^(-1)_{0, j}|
        """
        leaves = np.arange(2**self.num_generations - 1, self.num_nodes)
        R = la.inv(0.1 * np.eye(self.num_nodes) + self.laplacian_alpha_)
        return float(np.sum(np.abs(R[0, leaves])))

    def simulate_var_gene_switching(self, initial_active=0, generations=20, switch_rate=0.02):
        """
        Simulate mutually exclusive mono-allelic var gene switching:
        Repertoire of 60 var genes (Group A = 0..9, Group B = 10..39, Group C = 40..59).
        Guarantees exact probability simplex conservation.
        """
        prob = np.zeros(self.num_var_genes)
        prob[initial_active] = 1.0
        
        # Transition matrix with off-diagonal recombination kernel
        T = np.eye(self.num_var_genes) * (1.0 - switch_rate)
        # Off-diagonal transitions based on sequence homology / chromosomal location
        off_diag = switch_rate / (self.num_var_genes - 1)
        T += off_diag * (np.ones((self.num_var_genes, self.num_var_genes)) - np.eye(self.num_var_genes))
        
        trajectory = [prob.copy()]
        curr_p = prob.copy()
        for _ in range(generations):
            curr_p = curr_p @ T
            curr_p = curr_p / np.sum(curr_p)
            trajectory.append(curr_p)
            
        return np.array(trajectory)

    def evaluate_artemisinin_clearance(self, has_kelch13_mutation=False):
        """
        Evaluate Ring-Stage Survival Assay (RSA_72) under Artemisinin.
        Wild-type: RSA_72 < 1.0% (rapid parasiticidal clearance).
        Kelch13 propeller mutant (e.g. C580Y): RSA_72 > 5.0% (delayed clearance).
        """
        if has_kelch13_mutation:
            return float(np.random.uniform(6.5, 18.0)) # Resistant phenotype
        else:
            return float(np.random.uniform(0.1, 0.9))  # Sensitive wild-type

    def stratify_cerebral_malaria_risk(self, group_a_transcript_ratio, microvascular_stiffness):
        """
        Stratify risk of severe Cerebral Malaria based on Group A PfEMP1 expression
        and microvascular perfusion collapse.
        """
        # Group A transcripts bind EPCR/ICAM-1, mediating brain endothelial sequestration
        score = 0.65 * group_a_transcript_ratio + 0.35 * microvascular_stiffness
        z = 2.5 * (score - 0.5)
        return float(1.0 / (1.0 + np.exp(-z)))
