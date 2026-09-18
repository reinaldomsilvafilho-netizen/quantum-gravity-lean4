"""
Riemannian Connectome & Gut-Brain Axis Engine for Alzheimer's & Mental Health
Global Health Pillar 03: 03_neurodegeneration_alzheimer_mental_health
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Unified Quantum Gravity & Geometric Analysis (DOI: 10.5281/zenodo.22290043)
"""

import numpy as np
import scipy.linalg as la

class RiemannianConnectomeEngine:
    """
    Riemannian Manifold Engine on the Cartan-Hadamard Cone (S_{++}^q, g_AI).
    Eliminates Euclidean swelling distortion (det(mean) >> prod det^{1/N})
    and captures early synaptic dysconnection in ADNI and HCP neuroimaging cohorts.
    """
    def __init__(self, q_rois=60, max_iter=50, tol=1e-6):
        self.q = q_rois
        self.max_iter = max_iter
        self.tol = tol
        self.frechet_mean_ = None

    def affine_invariant_distance(self, S1, S2):
        """
        Geodesic distance on (S_{++}^q, g_AI):
        d_AI(S1, S2) = ||logm(S1^{-1/2} S2 S1^{-1/2})||_F
        """
        L1 = la.cholesky(S1, lower=True)
        L1_inv = la.inv(L1)
        C = L1_inv @ S2 @ L1_inv.T
        evals = la.eigvalsh(C)
        log_evals = np.log(np.maximum(evals, 1e-12))
        return float(np.sqrt(np.sum(log_evals**2)))

    def frechet_mean(self, matrices, weights=None):
        """
        Compute Riemannian Fréchet mean via Karcher flow:
        M_{t+1} = M_t^{1/2} exp(sum_i w_i logm(M_t^{-1/2} S_i M_t^{-1/2})) M_t^{1/2}
        """
        N = len(matrices)
        if weights is None:
            weights = np.ones(N) / N
            
        # Initial guess: Euclidean mean normalized to positive definite
        M = np.mean(matrices, axis=0)
        M = 0.5 * (M + M.T)
        evals, evecs = la.eigh(M)
        evals = np.maximum(evals, 1e-4)
        M = evecs @ np.diag(evals) @ evecs.T

        for it in range(self.max_iter):
            # Compute matrix square root and inverse
            evals_M, evecs_M = la.eigh(M)
            evals_M = np.maximum(evals_M, 1e-6)
            M_sqrt = evecs_M @ np.diag(np.sqrt(evals_M)) @ evecs_M.T
            M_isqrt = evecs_M @ np.diag(1.0 / np.sqrt(evals_M)) @ evecs_M.T
            
            # Riemannian tangent vector accumulation
            tangent_sum = np.zeros_like(M)
            for i in range(N):
                S = matrices[i]
                C = M_isqrt @ S @ M_isqrt
                evals_c, evecs_c = la.eigh(C)
                evals_c = np.maximum(evals_c, 1e-12)
                log_C = evecs_c @ np.diag(np.log(evals_c)) @ evecs_c.T
                tangent_sum += weights[i] * log_C
                
            norm_grad = float(np.linalg.norm(tangent_sum, 'fro'))
            if norm_grad < self.tol:
                break
                
            # Geodesic update: Exp_M(tangent_sum)
            evals_t, evecs_t = la.eigh(tangent_sum)
            exp_T = evecs_t @ np.diag(np.exp(evals_t)) @ evecs_t.T
            M = M_sqrt @ exp_T @ M_sqrt
            M = 0.5 * (M + M.T)

        self.frechet_mean_ = M
        return M

    def tangent_space_project(self, S, ref_mean=None):
        """
        Logarithmic map: Log_{ref}(S) = ref^{1/2} logm(ref^{-1/2} S ref^{-1/2}) ref^{1/2}
        Vectorized into symmetric half-vector representation.
        """
        if ref_mean is None:
            ref_mean = self.frechet_mean_
            
        evals_M, evecs_M = la.eigh(ref_mean)
        evals_M = np.maximum(evals_M, 1e-6)
        M_isqrt = evecs_M @ np.diag(1.0 / np.sqrt(evals_M)) @ evecs_M.T
        
        C = M_isqrt @ S @ M_isqrt
        evals_c, evecs_c = la.eigh(C)
        evals_c = np.maximum(evals_c, 1e-12)
        log_C = evecs_c @ np.diag(np.log(evals_c)) @ evecs_c.T
        
        # Extract upper triangle with sqrt(2) weighting on off-diagonals (isometry)
        q = self.q
        idx = np.triu_indices(q)
        vec = log_C[idx].copy()
        # Scale off-diagonals
        off_diag_mask = idx[0] != idx[1]
        vec[off_diag_mask] *= np.sqrt(2.0)
        return vec
