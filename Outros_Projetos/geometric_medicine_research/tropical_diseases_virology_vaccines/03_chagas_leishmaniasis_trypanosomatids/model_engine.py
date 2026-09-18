"""
Riemannian Myocardial Strain & Vectorcardiographic Manifold Engine
Tropical Diseases & Virology Pillar 03: 03_chagas_leishmaniasis_trypanosomatids
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Unified Quantum Gravity & Geometric Analysis (DOI: 10.5281/zenodo.22290043)
"""

import numpy as np
import scipy.linalg as la

class ChagasRiemannianCardiomyopathyEngine:
    """
    Riemannian Manifold Engine on S_{++}^q for Chronic Chagas Cardiomyopathy (CCC)
    and Trypanosomatid Interstitial Fibrosis Detection.
    
    Processes 3D speckle-tracking myocardial strain tensors and 12-lead vectorcardiographic
    spatiotemporal loops via Affine-Invariant and Log-Euclidean metrics, eliminating
    eigenvalue swelling and detecting micro-fibrotic myocardial disarray.
    """
    def __init__(self, tensor_dim=3):
        self.tensor_dim = tensor_dim

    def affine_invariant_distance(self, P, Q):
        """
        Compute Affine-Invariant Riemannian metric d_AI on S_{++}^q:
        d_AI(P, Q) = ||logm(P^(-1/2) Q P^(-1/2))||_F
        GL(q) invariant and isometric under coordinate rotations.
        """
        P_sqrt = la.sqrtm(P)
        P_inv_sqrt = la.inv(P_sqrt)
        M = P_inv_sqrt @ Q @ P_inv_sqrt
        # Eigenvalue formulation for speed and precision
        evals = np.maximum(la.eigvalsh(M), 1e-12)
        return float(np.sqrt(np.sum(np.log(evals)**2)))

    def log_euclidean_distance(self, P, Q):
        """
        Compute Log-Euclidean metric d_LE on S_{++}^q:
        d_LE(P, Q) = ||logm(P) - logm(Q)||_F
        """
        logP = self.matrix_log(P)
        logQ = self.matrix_log(Q)
        return float(la.norm(logP - logQ, 'fro'))

    def matrix_log(self, P):
        evals, evecs = la.eigh(P)
        evals = np.maximum(evals, 1e-12)
        return evecs @ np.diag(np.log(evals)) @ evecs.T

    def matrix_exp(self, S):
        evals, evecs = la.eigh(S)
        return evecs @ np.diag(np.exp(evals)) @ evecs.T

    def compute_frechet_mean(self, matrices):
        """
        Compute exact Log-Euclidean Fréchet Mean:
        P_mean = exp( 1/N sum_i log(P_i) )
        Guarantees zero determinant swelling (swelling ratio = 1.000).
        """
        N = len(matrices)
        sum_log = np.zeros_like(matrices[0], dtype=float)
        for P in matrices:
            sum_log += self.matrix_log(P)
        return self.matrix_exp(sum_log / N)

    def extract_vcg_planarity(self, qrs_loop_coordinates):
        """
        Compute Vectorcardiographic 3D QRS spatial loop thickness / planarity:
        Eigenvalues lambda_1 >= lambda_2 >= lambda_3 of spatial covariance.
        Planarity thickness = lambda_3 / (lambda_1 + lambda_2 + lambda_3).
        Fibrotic myocardial scarring breaks planar depolarization, inflating thickness.
        """
        cov = np.cov(qrs_loop_coordinates, rowvar=False)
        evals = np.sort(np.maximum(la.eigvalsh(cov), 1e-12))[::-1]
        thickness = evals[2] / (np.sum(evals) + 1e-12)
        return float(thickness)

    def stratify_chagas_cardiomyopathy_risk(self, strain_tensor, healthy_ref_tensor, vcg_thickness):
        """
        Stratify probability of early Chronic Chagas Cardiomyopathy:
        Combines intrinsic Riemannian strain distance with VCG loop thickness.
        """
        d_riemannian = self.affine_invariant_distance(strain_tensor, healthy_ref_tensor)
        score = 0.55 * d_riemannian + 0.45 * (vcg_thickness * 100.0)
        z = 1.8 * (score - 2.0)
        return float(1.0 / (1.0 + np.exp(-z)))
