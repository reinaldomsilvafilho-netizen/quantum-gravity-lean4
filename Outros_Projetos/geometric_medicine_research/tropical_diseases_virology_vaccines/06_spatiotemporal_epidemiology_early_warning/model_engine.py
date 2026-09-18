"""
FRACTIONAL METAPOPULATION EPIDEMIOLOGY & RICCI EARLY WARNING ENGINE (PILLAR 06)
Theoretical Grounding: Treatise Chapter 04 (Simplicial Fractional Laplacians) &
Chapter 11 (Ricci Flow Surgery on Complex Networks, DOI: 10.5281/zenodo.22290043)
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np

class FractionalEpidemiologyEngine:
    def __init__(self, n_nodes=50, alpha=0.65, beta_contact=0.35, gamma_recovery=0.10):
        """
        Metapopulation epidemiological system on complex mobility networks.
        alpha: fractional spectral diffusion exponent in (0, 1] (Lévy flight index)
        """
        self.n_nodes = n_nodes
        self.alpha = alpha
        self.beta = beta_contact
        self.gamma = gamma_recovery

    def construct_mobility_laplacian(self, adjacency_matrix):
        """
        Compute standard graph Laplacian L and normalized Laplacian L_norm = D^{-1/2} L D^{-1/2}.
        """
        degrees = np.sum(adjacency_matrix, axis=1)
        degrees_safe = np.maximum(degrees, 1e-12)
        D = np.diag(degrees)
        L = D - adjacency_matrix
        
        D_inv_sqrt = np.diag(1.0 / np.sqrt(degrees_safe))
        L_norm = D_inv_sqrt @ L @ D_inv_sqrt
        return L, L_norm

    def compute_fractional_laplacian(self, L_norm):
        """
        Fractional graph Laplacian via spectral decomposition:
        L_norm^alpha = V * diag(lambda_k^alpha) * V^T
        """
        eigvals, eigvecs = np.linalg.eigh(L_norm)
        eigvals_clipped = np.maximum(eigvals, 0.0)
        eigvals_frac = np.power(eigvals_clipped, self.alpha)
        L_alpha = eigvecs @ np.diag(eigvals_frac) @ eigvecs.T
        return L_alpha, eigvals_frac

    def compute_ollivier_ricci_curvature(self, adjacency_matrix, node_i, node_j):
        """
        Compute discrete Ollivier-Ricci curvature on mobility edge (i, j):
        kappa_OR(i, j) = 1 - W_1(m_i, m_j) / d(i, j)
        For connected neighbors, d(i, j) = 1.
        Negative curvature indicates bridging bottlenecks (super-spreading bridges).
        """
        deg_i = np.sum(adjacency_matrix[node_i])
        deg_j = np.sum(adjacency_matrix[node_j])
        if deg_i == 0 or deg_j == 0:
            return 0.0
            
        prob_i = adjacency_matrix[node_i] / deg_i
        prob_j = adjacency_matrix[node_j] / deg_j
        
        # Simplified 1-Wasserstein proxy on 1-hop neighborhood:
        common_neighbors = np.sum(np.minimum(prob_i, prob_j))
        # More common neighbors -> positive curvature (cluster). Disjoint neighborhoods -> negative curvature (bottleneck bridge)
        kappa_proxy = 2.0 * common_neighbors - 1.0 + (1.0 / max(deg_i, deg_j))
        return float(kappa_proxy)

    def deconvolve_wastewater_signal(self, wastewater_signal, transit_delay_kernel, regularization_lambda=1e-3):
        """
        Recover latent community viral burden I(t) from wastewater genomic copies C(t):
        C(t) = (K * I)(t) + noise  =>  I_hat = (K^T K + lambda * L^alpha)^{-1} K^T C
        """
        T = len(wastewater_signal)
        K_mat = np.zeros((T, T))
        K_len = len(transit_delay_kernel)
        for i in range(T):
            for j in range(max(0, i - K_len + 1), i + 1):
                K_mat[i, j] = transit_delay_kernel[i - j]
                
        # Tikhonov regularization with fractional identity
        reg_mat = regularization_lambda * np.eye(T)
        reconstructed_I = np.linalg.solve(K_mat.T @ K_mat + reg_mat, K_mat.T @ wastewater_signal)
        return np.maximum(reconstructed_I, 0.0)

    def compute_early_warning_index(self, active_infections, L_alpha, diffusion_rate=0.05):
        """
        Compute Early Warning Outbreak Index (EWI):
        Leading eigenvalue of fractional epidemic Jacobian J = beta*diag(I) - gamma*I - D*L^alpha.
        Positive leading eigenvalue indicates supercritical epidemic branching.
        """
        diag_J = self.beta * active_infections - self.gamma
        J_matrix = np.diag(diag_J) - diffusion_rate * L_alpha
        
        eigvals = np.linalg.eigvals(J_matrix)
        leading_real_part = float(np.max(np.real(eigvals)))
        # Early warning trigger: leading eigenvalue crosses zero into supercritical regime
        ewi_score = 1.0 / (1.0 + np.exp(-25.0 * leading_real_part))
        return float(leading_real_part), float(ewi_score)
