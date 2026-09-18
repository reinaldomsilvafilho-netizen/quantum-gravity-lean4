"""
MINIMAX EXTRINSIC CURVATURE EPITOPE ENGINE (PILLAR 05)
Theoretical Grounding: Treatise Chapter 07 (Minimax Extrinsic Curvature on Submanifolds
under Obstacle Environments, DOI: 10.5281/zenodo.22290043)
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np

class MinimaxEpitopeEngine:
    def __init__(self, glycan_shield_density=0.65, obstacle_radius=1.8):
        """
        Glycoprotein surface manifold with glycan obstacle shields.
        obstacle_radius: characteristic radius of N-linked glycan steric shield (in nm)
        """
        self.glycan_density = glycan_shield_density
        self.r_obs = obstacle_radius
        self.kappa_obs = 1.0 / obstacle_radius

    def compute_weingarten_curvature(self, patch_coords):
        """
        Compute the Weingarten shape operator W = -dN and principal curvatures (kappa_1, kappa_2)
        on a local 2D glycoprotein surface patch embedded in R^3.
        patch_coords: (N, 3) points representing local amino acid residue C-alpha coordinates.
        """
        # Fit local quadratic osculating paraboloid: z = 0.5 * (a*x^2 + 2*b*x*y + c*y^2)
        centroid = np.mean(patch_coords, axis=0)
        centered = patch_coords - centroid
        
        # SVD for local tangent plane (e1, e2) and normal n
        _, _, vh = np.linalg.svd(centered)
        u_tangent = centered @ vh[:2].T
        h_normal = centered @ vh[2]

        # Fit quadratic form [x^2, 2xy, y^2] -> z
        X_design = np.column_stack([
            u_tangent[:, 0]**2,
            2 * u_tangent[:, 0] * u_tangent[:, 1],
            u_tangent[:, 1]**2
        ])
        
        coeffs, _, _, _ = np.linalg.lstsq(X_design, h_normal, rcond=None)
        a, b, c = coeffs
        
        # Shape operator matrix W
        W = np.array([[a, b], [b, c]])
        eigvals = np.linalg.eigvalsh(W)
        kappa_1, kappa_2 = eigvals[0], eigvals[1]
        mean_curvature = 0.5 * (kappa_1 + kappa_2)
        gauss_curvature = kappa_1 * kappa_2
        extrinsic_norm = np.max(np.abs(eigvals))

        return {
            'shape_operator': W,
            'kappa_1': float(kappa_1),
            'kappa_2': float(kappa_2),
            'mean_curvature': float(mean_curvature),
            'gauss_curvature': float(gauss_curvature),
            'extrinsic_norm': float(extrinsic_norm)
        }

    def evaluate_obstacle_curvature_exclusion(self, corridor_width):
        """
        Theorem 4.2 (Obstacle Curvature Exclusion Principle):
        Any continuous C^2 path or paratope interface navigating between glycan shields
        of clearance w must satisfy: kappa* >= 2 / corridor_width.
        """
        if corridor_width <= 0:
            return float('inf')
        kappa_star_min = 2.0 / corridor_width
        return float(kappa_star_min)

    def compute_federer_reach(self, kappa_star):
        """
        Federer reach bound: reach(Sigma) >= 1 / kappa_star.
        Ensures normal bundle injectivity and prevents steric Fab self-clash.
        """
        if kappa_star <= 0:
            return float('inf')
        return float(1.0 / kappa_star)

    def evaluate_epitope_scaffold(self, patch_coords, corridor_width, is_glycan_shielded=True):
        """
        Evaluate candidate vaccine scaffold epitope:
        Returns minimax curvature kappa*, reach, accessibility, and predicted neutralization breadth.
        """
        curv_data = self.compute_weingarten_curvature(patch_coords)
        raw_kappa = curv_data['extrinsic_norm']
        
        if is_glycan_shielded:
            corridor_barrier = self.evaluate_obstacle_curvature_exclusion(corridor_width)
            effective_kappa = max(raw_kappa, corridor_barrier)
        else:
            effective_kappa = raw_kappa

        reach = self.compute_federer_reach(effective_kappa)
        
        # Broad neutralization requires smooth scaffold (low kappa) and sufficient reach for Fab approach (reach >= 1.2 nm)
        # Steric clash penalty activates when reach drops below clearance threshold (1.2 nm)
        steric_penalty = np.exp(max(0.0, 1.2 - reach)) - 1.0
        breadth_logit = 3.5 - 1.8 * effective_kappa - 2.0 * steric_penalty
        predicted_breadth = 1.0 / (1.0 + np.exp(-breadth_logit))

        return {
            'effective_kappa': float(effective_kappa),
            'federer_reach': float(reach),
            'steric_penalty': float(steric_penalty),
            'predicted_breadth': float(predicted_breadth),
            'curv_data': curv_data
        }
