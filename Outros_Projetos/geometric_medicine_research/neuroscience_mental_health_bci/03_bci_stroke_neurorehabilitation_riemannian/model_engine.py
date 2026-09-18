"""
RIEMANNIAN BCI & STROKE NEUROREHABILITATION ENGINE (PILLAR 03)
Theoretical Grounding: Treatise Chapter 02 (Geometric Flows on Tensor Varieties) &
Paper 3 (Affine-Invariant Geodesic Optimization on S_{++}^q, DOI: 10.5281/zenodo.22290043)
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np
from scipy.linalg import logm, expm

class RiemannianBCIEngine:
    def __init__(self, n_channels=8):
        """
        Sensorimotor EEG covariance manifold S_{++}^q (q=8 channels).
        """
        self.q = n_channels

    def compute_affine_invariant_distance(self, C1, C2):
        """
        Geodesic distance on S_{++}^q:
        d_AI(C1, C2) = || log( C1^{-1/2} C2 C1^{-1/2} ) ||_F
        """
        w1, v1 = np.linalg.eigh(C1)
        w1_safe = np.maximum(w1, 1e-12)
        C1_inv_sqrt = v1 @ np.diag(1.0 / np.sqrt(w1_safe)) @ v1.T
        
        M = C1_inv_sqrt @ C2 @ C1_inv_sqrt
        w_m = np.linalg.eigvalsh(M)
        w_m_safe = np.maximum(w_m, 1e-12)
        return float(np.sqrt(np.sum(np.log(w_m_safe)**2)))

    def compute_frechet_mean(self, cov_list, max_iter=25, tol=1e-5):
        """
        Compute Riemannian Fréchet / Karcher barycenter on S_{++}^q:
        C* = argmin_C sum_i d_AI(C, C_i)^2
        """
        # Initialize with Euclidean mean projected to SPD
        C = np.mean(cov_list, axis=0)
        w, v = np.linalg.eigh(C)
        C = v @ np.diag(np.maximum(w, 0.05)) @ v.T
        
        for _ in range(max_iter):
            w, v = np.linalg.eigh(C)
            w_safe = np.maximum(w, 1e-12)
            C_sqrt = v @ np.diag(np.sqrt(w_safe)) @ v.T
            C_inv_sqrt = v @ np.diag(1.0 / np.sqrt(w_safe)) @ v.T
            
            # Compute tangent space step
            tangent_sum = np.zeros_like(C)
            for Ci in cov_list:
                M = C_inv_sqrt @ Ci @ C_inv_sqrt
                wm, vm = np.linalg.eigh(M)
                log_M = vm @ np.diag(np.log(np.maximum(wm, 1e-12))) @ vm.T
                tangent_sum += log_M
                
            tangent_mean = tangent_sum / len(cov_list)
            step_norm = np.linalg.norm(tangent_mean)
            
            # Retraction / Exponential map
            wt, vt = np.linalg.eigh(tangent_mean)
            exp_T = vt @ np.diag(np.exp(wt)) @ vt.T
            C = C_sqrt @ exp_T @ C_sqrt
            
            if step_norm < tol:
                break
                
        return C

    def project_to_tangent_space(self, C, C_ref):
        """
        Logarithmic map: Log_{C_ref}(C) = C_ref^{1/2} * log( C_ref^{-1/2} C C_ref^{-1/2} ) * C_ref^{1/2}
        Unfolds the non-linear Riemannian manifold into a flat Euclidean tangent vector.
        """
        w, v = np.linalg.eigh(C_ref)
        C_ref_sqrt = v @ np.diag(np.sqrt(np.maximum(w, 1e-12))) @ v.T
        C_ref_inv_sqrt = v @ np.diag(1.0 / np.sqrt(np.maximum(w, 1e-12))) @ v.T
        
        M = C_ref_inv_sqrt @ C @ C_ref_inv_sqrt
        wm, vm = np.linalg.eigh(M)
        log_M = vm @ np.diag(np.log(np.maximum(wm, 1e-12))) @ vm.T
        
        # Half-vectorize upper triangular elements with sqrt(2) weights for off-diagonals
        dim = self.q
        feat = []
        for i in range(dim):
            feat.append(log_M[i, i])
            for j in range(i + 1, dim):
                feat.append(np.sqrt(2.0) * log_M[i, j])
        return np.array(feat)

    def classify_motor_imagery(self, trial_cov, mean_left, mean_right):
        """
        Minimum Distance to Riemannian Mean (MDRM) classification:
        Decodes whether the stroke patient intended to move the paretic hand vs rest.
        """
        d_left = self.compute_affine_invariant_distance(trial_cov, mean_left)
        d_right = self.compute_affine_invariant_distance(trial_cov, mean_right)
        
        # Softmax probability for Left vs Right hand intention
        prob_left = 1.0 / (1.0 + np.exp(2.5 * (d_left - d_right)))
        predicted_class = int(d_left < d_right) # 1 = Left, 0 = Right
        return predicted_class, float(prob_left), float(d_left), float(d_right)
