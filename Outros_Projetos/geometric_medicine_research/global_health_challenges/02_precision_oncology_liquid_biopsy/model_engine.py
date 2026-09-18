"""
CIG-Langevin & Minimax Precision Oncology Engine
Global Health Pillar 02: 02_precision_oncology_liquid_biopsy
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Unified Quantum Gravity & Geometric Analysis (DOI: 10.5281/zenodo.22290043)
"""

import numpy as np
import scipy.linalg as la

class CIGLangevinLiquidBiopsy:
    """
    Curvature-Informed Geometrically Conjugate (CIG) Langevin Engine for
    Ultra-Rare Variant Liquid Biopsies (ctDNA) and Pan-Cancer Survival Models.
    Enforces a strict Bakry-Emery Ricci curvature floor Ric_infty >= lambda_0 I > 0
    via information priors and Woodbury O(n^3 + n^2 p) inversion.
    """
    def __init__(self, lambda_0=0.5, kappa_0=0.1, gamma=0.02, num_samples=600, burn_in=150, random_state=42):
        self.lambda_0 = lambda_0
        self.kappa_0 = kappa_0
        self.gamma = gamma
        self.num_samples = num_samples
        self.burn_in = burn_in
        self.random_state = random_state
        self.samples = None
        self.posterior_mean = None

    def _compute_potential_and_grad(self, theta, X, y):
        eta = np.clip(X @ theta, -35, 35)
        p = 1.0 / (1.0 + np.exp(-eta))
        w = p * (1.0 - p)
        
        XTX_theta = X.T @ (X @ theta)
        grad_lik = -X.T @ (y - p)
        grad_prior = self.lambda_0 * theta + self.kappa_0 * XTX_theta
        grad_U = grad_lik + grad_prior
        return grad_U, w

    def sample(self, X, y):
        rng = np.random.RandomState(self.random_state)
        n, p = X.shape
        theta = np.zeros(p)
        chain = []
        XXT = X @ X.T
        
        for it in range(self.num_samples + self.burn_in):
            grad_U, w = self._compute_potential_and_grad(theta, X, y)
            
            # Woodbury accelerated Riemannian natural gradient
            W_inv = 1.0 / (w + self.kappa_0)
            M_inner = np.diag(W_inv) + (1.0 / self.lambda_0) * XXT
            # Stabilize M_inner
            M_inner += 1e-6 * np.eye(n)
            L_inner = la.cholesky(M_inner, lower=True)
            
            X_grad = X @ grad_U
            v_inner = la.cho_solve((L_inner, True), X_grad)
            G_inv_grad = (1.0 / self.lambda_0) * grad_U - (1.0 / (self.lambda_0**2)) * (X.T @ v_inner)
            
            # Drift and Riemannian Brownian motion
            m_drift = theta - self.gamma * G_inv_grad
            xi = rng.normal(0, 1, size=p)
            xi_proj = (1.0 / np.sqrt(self.lambda_0)) * xi
            theta = m_drift + np.sqrt(2.0 * self.gamma) * xi_proj
            
            if it >= self.burn_in:
                chain.append(theta.copy())
                
        self.samples = np.array(chain)
        self.posterior_mean = np.mean(self.samples, axis=0)
        return self

    def predict_recurrence_risk(self, X_new):
        logits = np.clip(X_new @ self.posterior_mean, -30.0, 30.0)
        return 1.0 / (1.0 + np.exp(-logits))
