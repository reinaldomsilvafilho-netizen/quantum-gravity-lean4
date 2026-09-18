"""
================================================================================
RIEMANNIAN CONNECTOME ENGINE: DYNAMIC FUNCTIONAL CONNECTIVITY & ALZHEIMER'S (ADNI)
Manifold: Riemannian Cone (S^q_{++}, g_{AI}) of Symmetric Positive-Definite Matrices
Target: Zero Swelling, Invariant Fréchet Means, Geodesic Tangent Vector Fields
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Unified Quantum Gravity & Geometric Analysis (DOI: 10.5281/zenodo.22290043)
================================================================================
"""

import numpy as np
import scipy.linalg as la
from typing import List, Tuple, Optional

class RiemannianConnectomeEngine:
    """
    High-Performance Riemannian Manifold Engine for Brain Connectomes and fMRI/dMRI.
    Operates on the Cartan-Hadamard Riemannian cone (S_{++}^q, g_{AI}) with non-positive
    sectional curvature K <= 0.
    """
    
    def __init__(self, tol: float = 1e-6, max_iter: int = 100):
        self.tol = tol
        self.max_iter = max_iter
        self.frechet_mean_: Optional[np.ndarray] = None
        
    @staticmethod
    def matrix_sqrt(A: np.ndarray) -> np.ndarray:
        w, v = la.eigh(A)
        w = np.maximum(w, 1e-12)
        return v @ np.diag(np.sqrt(w)) @ v.T

    @staticmethod
    def matrix_inv_sqrt(A: np.ndarray) -> np.ndarray:
        w, v = la.eigh(A)
        w = np.maximum(w, 1e-12)
        return v @ np.diag(1.0 / np.sqrt(w)) @ v.T

    @staticmethod
    def matrix_log(A: np.ndarray) -> np.ndarray:
        w, v = la.eigh(A)
        w = np.maximum(w, 1e-12)
        return v @ np.diag(np.log(w)) @ v.T

    @staticmethod
    def matrix_exp(A: np.ndarray) -> np.ndarray:
        w, v = la.eigh(A)
        w = np.clip(w, -50, 50)
        return v @ np.diag(np.exp(w)) @ v.T

    def distance_affine_invariant(self, A: np.ndarray, B: np.ndarray) -> float:
        """
        Computes the exact affine-invariant Riemannian distance:
        d_AI(A, B) = || log(A^(-1/2) B A^(-1/2)) ||_F
        """
        A_isqrt = self.matrix_inv_sqrt(A)
        M = A_isqrt @ B @ A_isqrt
        log_M = self.matrix_log(M)
        return float(la.norm(log_M, 'fro'))

    def compute_frechet_mean(self, matrices: List[np.ndarray], weights: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Computes the unique Riemannian Fréchet Mean (Karcher Center of Mass)
        via Riemannian gradient descent on the manifold (S_{++}^q, g_{AI}).
        """
        N = len(matrices)
        q = matrices[0].shape[0]
        if weights is None:
            weights = np.ones(N) / N
        else:
            weights = weights / np.sum(weights)
            
        # Initialization: Euclidean average projected onto S^q_{++}
        G = np.mean(matrices, axis=0)
        G = 0.5 * (G + G.T) + 1e-4 * np.eye(q)
        
        for it in range(self.max_iter):
            G_sqrt = self.matrix_sqrt(G)
            G_isqrt = self.matrix_inv_sqrt(G)
            
            # Riemannian gradient on tangent space T_G S^q_{++}
            tangent_sum = np.zeros((q, q))
            for i in range(N):
                M_i = G_isqrt @ matrices[i] @ G_isqrt
                log_M_i = self.matrix_log(M_i)
                tangent_sum += weights[i] * log_M_i
                
            grad_norm = la.norm(tangent_sum, 'fro')
            if grad_norm < self.tol:
                break
                
            # Geodesic update step
            step_matrix = self.matrix_exp(tangent_sum)
            G = G_sqrt @ step_matrix @ G_sqrt
            G = 0.5 * (G + G.T)
            
        self.frechet_mean_ = G
        return G

    def project_to_tangent_space(self, G_ref: np.ndarray, A: np.ndarray) -> np.ndarray:
        """
        Computes the Riemannian Logarithmic Map Log_{G_ref}(A) to map
        a covariance matrix A in S^q_{++} to the tangent space T_{G_ref} S^q_{++}.
        """
        G_isqrt = self.matrix_inv_sqrt(G_ref)
        M = G_isqrt @ A @ G_isqrt
        return self.matrix_log(M)

    def compute_swelling_factor(self, matrices: List[np.ndarray], mean_matrix: np.ndarray) -> float:
        """
        Computes the determinant distortion ratio (swelling factor):
        Swelling = det(mean_matrix) / prod(det(A_i))^(1/N)
        For Riemannian Fréchet Mean, Swelling == 1.0 (Zero Swelling).
        For Euclidean Average, Swelling >> 1.0 (Severe Artificial Inflation).
        """
        N = len(matrices)
        log_dets = [np.linalg.slogdet(A)[1] for A in matrices]
        mean_log_det = np.mean(log_dets)
        log_det_mean = np.linalg.slogdet(mean_matrix)[1]
        return float(np.exp(log_det_mean - mean_log_det))
