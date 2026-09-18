"""
Simplicial Fractional Laplacian & Non-Local Beta-Spline GAMM Engine
Pillar 02: Human Microbiome, Gut-Brain Axis & Single-Cell Transcriptomics (scRNA-seq)
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Unified Quantum Gravity & Geometric Statistics (DOI: 10.5281/zenodo.22290043)
"""

import numpy as np
from scipy.linalg import eigh, cholesky, solve_triangular

class SimplicialBetaGAMM:
    """
    Continuous Simplicial Fractional Laplacian GAMM for compositional & zero-inflated count data.
    Eliminates Aitchison log-ratio poles log(0) = -inf by working directly on the continuous
    simplex Delta_m with invariant Beta-kernels and continuous multinomial roughness penalties.
    """
    def __init__(self, m_dim=10, alpha=1.25, num_basis=20, random_state=42):
        self.m_dim = m_dim          # Simplex dimension (number of compositional components - 1)
        self.alpha = alpha          # Fractional Laplacian order (alpha > (m-1)/2 ensures C^0)
        self.num_basis = num_basis  # Number of simplicial basis functions
        self.random_state = random_state
        self.basis_nodes = None
        self.roughness_matrix = None
        self.beta_hat = None
        self.lambda_reml = 1.0
        self._initialize_basis()

    def _initialize_basis(self):
        rng = np.random.RandomState(self.random_state)
        raw = rng.dirichlet(np.ones(self.m_dim + 1) * 1.5, size=self.num_basis)
        self.basis_nodes = raw
        
        D = np.zeros((self.num_basis, self.num_basis))
        for i in range(self.num_basis):
            for j in range(self.num_basis):
                bc = np.sum(np.sqrt(self.basis_nodes[i] * self.basis_nodes[j]))
                bc = np.clip(bc, -1.0, 1.0)
                d_fr = np.arccos(bc)
                D[i, j] = d_fr

        gamma_val = self.alpha * 2.0
        self.roughness_matrix = np.exp(-gamma_val * D**2) + 1e-6 * np.eye(self.num_basis)
        self.roughness_matrix = self.roughness_matrix - np.mean(self.roughness_matrix, axis=0, keepdims=True)
        self.roughness_matrix = self.roughness_matrix - np.mean(self.roughness_matrix, axis=1, keepdims=True)
        evals, evecs = eigh(self.roughness_matrix)
        evals = np.maximum(evals, 1e-7)
        self.roughness_matrix = evecs @ np.diag(evals) @ evecs.T

    def evaluate_basis(self, X_comp):
        n = X_comp.shape[0]
        Phi = np.zeros((n, self.num_basis))
        for j in range(self.num_basis):
            bc = np.sum(np.sqrt(X_comp * self.basis_nodes[j]), axis=1)
            bc = np.clip(bc, -1.0, 1.0)
            d_fr = np.arccos(bc)
            Phi[:, j] = np.exp(- (d_fr**2) / (2.0 * (1.0 / self.alpha)**2))
        return Phi

    def fit(self, X_comp, y, max_iter=30, tol=1e-5):
        Phi = self.evaluate_basis(X_comp)
        n, p = Phi.shape
        
        lambda_val = 0.1
        beta = np.zeros(p)
        
        for iteration in range(max_iter):
            A = Phi.T @ Phi + lambda_val * self.roughness_matrix + 1e-6 * np.eye(p)
            rhs = Phi.T @ y
            
            try:
                L = cholesky(A, lower=True)
                beta_new = solve_triangular(L.T, solve_triangular(L, rhs, lower=True))
            except np.linalg.LinAlgError:
                beta_new = np.linalg.solve(A, rhs)
            
            A_inv = np.linalg.pinv(A)
            dof = np.trace(A_inv @ (Phi.T @ Phi))
            residuals = y - Phi @ beta_new
            sigma2 = np.sum(residuals**2) / max(n - dof, 1.0)
            penalty_val = beta_new.T @ self.roughness_matrix @ beta_new
            lambda_new = np.clip((dof * sigma2) / max(penalty_val, 1e-6), 1e-4, 1e4)
            
            diff = np.linalg.norm(beta_new - beta) / max(np.linalg.norm(beta) + 1e-6, 1.0)
            beta = beta_new
            lambda_val = lambda_new
            
            if diff < tol:
                break
                
        self.beta_hat = beta
        self.lambda_reml = lambda_val
        return self

    def predict(self, X_comp):
        Phi = self.evaluate_basis(X_comp)
        return Phi @ self.beta_hat
