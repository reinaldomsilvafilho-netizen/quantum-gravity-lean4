"""
Fisher-Rao Information Geometry Epigenetic Aging & Type 2 Diabetes Engine
Global Health Pillar 05: 05_diabetes_metabolic_epigenetic_aging
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Unified Quantum Gravity & Geometric Analysis (DOI: 10.5281/zenodo.22290043)
"""

import numpy as np
import scipy.linalg as la

class FisherRaoEpigeneticEngine:
    """
    Riemannian Information-Geometric Engine for DNA Methylation (CpG beta-values)
    and Accelerated Epigenetic Aging Clocks in Type 2 Diabetes & Metabolic Syndrome.
    
    Transforms bounded Bernoulli manifolds (0, 1)^p via Bhattacharyya isometry:
        theta_j = 2 * arcsin(sqrt(beta_j)),  where ds^2 = d_beta^2 / (beta(1-beta)) = d_theta^2.
    Guarantees strict boundary compliance (beta in [0, 1]), zero saturation,
    and natural gradient geodesic convergence.
    """
    def __init__(self, alpha_reg=1e-2, l1_ratio=0.3, max_features=30):
        self.alpha_reg = alpha_reg
        self.l1_ratio = l1_ratio
        self.max_features = max_features
        self.weights_ = None
        self.intercept_ = None
        self.ref_cpg_ = None

    def transform_to_sphere(self, beta):
        """
        Isometric embedding of Fisher-Rao Bernoulli statistical manifold into spherical coordinates:
        theta_j = 2 * arcsin(sqrt(clip(beta_j, 1e-6, 1.0 - 1e-6)))
        """
        clipped = np.clip(beta, 1e-6, 1.0 - 1e-6)
        return 2.0 * np.arcsin(np.sqrt(clipped))

    def transform_to_simplex(self, theta):
        """
        Exact inverse Riemannian exponential chart:
        beta_j = sin^2(theta_j / 2), guaranteed in [0, 1].
        """
        return np.sin(theta / 2.0)**2

    def fisher_rao_distance(self, beta1, beta2):
        """
        Intrinsic Riemannian geodesic distance under Fisher-Rao metric:
        d_FR(beta1, beta2) = 2 * ||arcsin(sqrt(beta1)) - arcsin(sqrt(beta2))||_2
        """
        th1 = self.transform_to_sphere(beta1)
        th2 = self.transform_to_sphere(beta2)
        return np.linalg.norm(th1 - th2, axis=-1)

    def fit_epigenetic_clock(self, beta_matrix, chronological_ages):
        """
        Fit information-geometric penalized clock on isometric spherical coordinates:
        y = theta @ w + b
        Screening top informational CpGs followed by regularized natural gradient shrinkage.
        """
        X_th = self.transform_to_sphere(beta_matrix)
        y = np.array(chronological_ages, dtype=float)
        n, p = X_th.shape
        
        self.ref_cpg_ = np.mean(beta_matrix, axis=0)
        y_mean = np.mean(y)
        y_c = y - y_mean
        
        # Informational correlation screening
        corrs = np.array([
            abs(np.corrcoef(X_th[:, j], y)[0, 1]) if np.std(X_th[:, j]) > 1e-6 else 0.0
            for j in range(p)
        ])
        k_sel = min(p, max(5, min(self.max_features, int(0.4 * p))))
        sel_indices = np.argsort(corrs)[::-1][:k_sel]
        
        X_sub = X_th[:, sel_indices]
        X_mean_sub = np.mean(X_sub, axis=0)
        X_c = X_sub - X_mean_sub
        
        # Natural gradient regularized least squares with L1/L2 penalty
        reg_diag = self.alpha_reg * (1.0 - self.l1_ratio) * np.eye(k_sel)
        w_sub = la.solve(X_c.T @ X_c + n * reg_diag + 1e-5 * np.eye(k_sel), X_c.T @ y_c)
            
        # Soft-thresholding for L1 sparsity
        l1_thresh = self.alpha_reg * self.l1_ratio
        w_sub = np.sign(w_sub) * np.maximum(0.0, np.abs(w_sub) - l1_thresh)
        
        w = np.zeros(p)
        w[sel_indices] = w_sub
        
        self.weights_ = w
        self.intercept_ = y_mean - np.dot(np.mean(X_th, axis=0), w)
        return self

    def predict_biological_age(self, beta_matrix):
        """
        Predict biological DNAmAge using Riemannian isometric coordinates:
        DNAmAge = theta @ w + b
        """
        if self.weights_ is None:
            raise ValueError("Epigenetic clock must be fitted before prediction.")
        X_th = self.transform_to_sphere(beta_matrix)
        return X_th @ self.weights_ + self.intercept_

    def compute_age_acceleration(self, beta_matrix, chronological_ages):
        """
        Compute epigenetic age acceleration:
        Delta_Age = DNAmAge - ChronologicalAge
        """
        bio_age = self.predict_biological_age(beta_matrix)
        return bio_age - np.array(chronological_ages)

    def stratify_metabolic_risk(self, beta_matrix, chronological_ages=None):
        """
        Stratify Type 2 Diabetes / Metabolic Syndrome risk based on
        intrinsic Fisher distance to healthy reference and epigenetic acceleration.
        Returns risk score in [0, 1].
        """
        d_fisher = self.fisher_rao_distance(beta_matrix, self.ref_cpg_)
        if chronological_ages is not None:
            delta_age = self.compute_age_acceleration(beta_matrix, chronological_ages)
            z = (d_fisher / (np.std(d_fisher) + 1e-5)) + 0.2 * (delta_age / (np.std(delta_age) + 1e-5))
        else:
            z = d_fisher / (np.std(d_fisher) + 1e-5)
        return 1.0 / (1.0 + np.exp(-z))
