"""
================================================================================
CIG-LANGEVIN CLINICAL ONCOLOGY ENGINE: SURVIVAL & RARE EVENT SEPARATION (TCGA)
Manifold: Smooth Weighted Metric-Measure Space (R^p, g, e^{-U} d theta)
Curvature: Uniform Bakry-Émery Ricci Curvature Lower Bound CD(K*, infty)
Target: Ergodic MCMC Sampling under Complete Clinical Separation & Liquid Biopsy
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Unified Quantum Gravity & Geometric Analysis (DOI: 10.5281/zenodo.22290043)
================================================================================
"""

import numpy as np
import scipy.linalg as la
from typing import Tuple, Optional

class CIGLangevinOncologyEngine:
    """
    Curvature-Informed Geometric Langevin (CIG-Langevin) Sampler for Precision Oncology.
    Enforces a uniform Ricci lower bound Ric_infty >= lambda_0 * I > 0 via Geometrically
    Conjugate Information Priors, eliminating MCMC metastability in separated trials.
    """
    
    def __init__(
        self,
        lambda_0: float = 0.5,
        kappa_0: float = 0.1,
        gamma: float = 0.02,
        n_samples: int = 1000,
        burn_in: int = 200,
        n_chains: int = 2
    ):
        self.lambda_0 = lambda_0
        self.kappa_0 = kappa_0
        self.gamma = gamma
        self.n_samples = n_samples
        self.burn_in = burn_in
        self.n_chains = n_chains
        self.chains_: Optional[np.ndarray] = None
        
    def _compute_potential_and_grad(self, theta: np.ndarray, X: np.ndarray, y: np.ndarray) -> Tuple[float, np.ndarray, np.ndarray]:
        eta = X @ theta
        p = 1.0 / (1.0 + np.exp(-np.clip(eta, -35, 35)))
        w = p * (1.0 - p)
        
        # Log-likelihood
        log1p = np.maximum(0, eta) + np.log1p(np.exp(-np.abs(eta)))
        lik = np.sum(y * eta - log1p)
        
        # Geometrically conjugate prior
        XTX_theta = X.T @ (X @ theta)
        prior = -0.5 * (self.lambda_0 * float(theta.T @ theta) + self.kappa_0 * float(theta.T @ XTX_theta))
        U = -(lik + prior)
        
        # Gradient
        grad_lik = -X.T @ (y - p)
        grad_prior = self.lambda_0 * theta + self.kappa_0 * XTX_theta
        grad_U = grad_lik + grad_prior
        
        return U, grad_U, w

    def fit(self, X: np.ndarray, y: np.ndarray) -> "CIGLangevinOncologyEngine":
        """
        Samples the posterior distribution using Woodbury-accelerated CIG-Langevin.
        X: shape (n, p)
        y: shape (n,) binary clinical response / survival status
        """
        n, p = X.shape
        XXT = X @ X.T
        all_chains = []
        
        for c in range(self.n_chains):
            np.random.seed(500 + c)
            theta = np.zeros(p)
            samples = []
            
            for s in range(self.n_samples):
                U, grad_U, w = self._compute_potential_and_grad(theta, X, y)
                
                # Woodbury Accelerated Inversion: O(n^3 + n^2 p) instead of O(p^3)
                # G^-1 = (1/lambda_0) I - (1/lambda_0^2) X^T [ (W + kappa_0 I)^-1 + (1/lambda_0) XXT ]^-1 X
                W_inv = 1.0 / (w + self.kappa_0)
                M_inner = np.diag(W_inv) + (1.0 / self.lambda_0) * XXT
                L_inner = la.cholesky(M_inner, lower=True)
                
                X_grad = X @ grad_U
                v_inner = la.cho_solve((L_inner, True), X_grad)
                G_inv_grad = (1.0 / self.lambda_0) * grad_U - (1.0 / (self.lambda_0**2)) * (X.T @ v_inner)
                
                # Riemannian natural gradient drift
                m_drift = theta - self.gamma * G_inv_grad
                
                # Stabilized Riemannian Brownian increment
                xi = np.random.randn(p)
                xi_proj = (1.0 / np.sqrt(self.lambda_0)) * xi
                theta_prop = m_drift + np.sqrt(2.0 * self.gamma) * xi_proj
                
                theta = theta_prop
                samples.append(theta.copy())
                
            all_chains.append(samples)
            
        self.chains_ = np.array(all_chains)
        return self

    def get_posterior_mean(self) -> np.ndarray:
        if self.chains_ is None:
            raise ValueError("Engine must be fitted before computing posterior statistics.")
        post_samples = self.chains_[:, self.burn_in:, :]
        return np.mean(post_samples, axis=(0, 1))

    def get_credible_intervals(self, alpha: float = 0.05) -> Tuple[np.ndarray, np.ndarray]:
        if self.chains_ is None:
            raise ValueError("Engine must be fitted before computing credible intervals.")
        post_samples = self.chains_[:, self.burn_in:, :].reshape(-1, self.chains_.shape[2])
        low = np.percentile(post_samples, 100 * (alpha / 2.0), axis=0)
        high = np.percentile(post_samples, 100 * (1.0 - alpha / 2.0), axis=0)
        return low, high
