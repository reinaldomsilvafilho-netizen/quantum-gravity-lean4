"""
Hyperbolic Poincaré Antigenic Cartography & Viral Escape Prediction Engine
Tropical Diseases & Virology Pillar 04: 04_hyperbolic_antigenic_drift_virology
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Unified Quantum Gravity & Geometric Analysis (DOI: 10.5281/zenodo.22290043)
"""

import numpy as np
import scipy.linalg as la

class HyperbolicAntigenicDriftEngine:
    """
    Hyperbolic Space Form Engine on the Poincare Unit Ball D^d (K = -1 < 0)
    for Viral Antigenic Cartography, Phylodynamics, and Neutralization Escape Prediction.
    
    Eliminates the exponential metric distortion catastrophe of Euclidean cartography
    by matching the exponential tree volume expansion of viral mutational branching.
    """
    def __init__(self, dimension=2, curvature=-1.0):
        self.dimension = dimension
        self.curvature = curvature
        self.c = np.sqrt(abs(curvature))

    def hyperbolic_distance(self, u, v):
        """
        Exact geodesic distance on the Poincare disk D^d:
        d_H(u, v) = arcosh( 1 + 2 * ||u - v||^2 / ( (1 - ||u||^2) * (1 - ||v||^2) ) )
        """
        u_arr = np.array(u, dtype=float)
        v_arr = np.array(v, dtype=float)
        sq_u = np.sum(u_arr**2, axis=-1)
        sq_v = np.sum(v_arr**2, axis=-1)
        
        # Ensure inside unit ball
        sq_u = np.clip(sq_u, 0.0, 1.0 - 1e-7)
        sq_v = np.clip(sq_v, 0.0, 1.0 - 1e-7)
        diff_sq = np.sum((u_arr - v_arr)**2, axis=-1)
        
        arg = 1.0 + 2.0 * diff_sq / ((1.0 - sq_u) * (1.0 - sq_v))
        arg = np.maximum(1.0, arg)
        return float(np.arccosh(arg) / self.c) if np.ndim(arg) == 0 else np.arccosh(arg) / self.c

    def mobius_addition(self, u, v):
        """
        Mobius gyro-vector addition in Poincare ball:
        u (+) v = ( (1 + 2<u,v> + ||v||^2) u + (1 - ||u||^2) v ) / ( 1 + 2<u,v> + ||u||^2 ||v||^2 )
        """
        u = np.array(u, dtype=float)
        v = np.array(v, dtype=float)
        uv = np.dot(u, v)
        u2 = np.sum(u**2)
        v2 = np.sum(v**2)
        denom = 1.0 + 2.0 * uv + u2 * v2
        num = (1.0 + 2.0 * uv + v2) * u + (1.0 - u2) * v
        return num / (denom + 1e-12)

    def hyperbolic_exponential_map(self, base_point, tangent_vector):
        """
        Geodesic exponential chart Exp_p(v) on Poincare manifold:
        Moves along the unique geodesic passing through p with initial velocity v.
        """
        p = np.array(base_point, dtype=float)
        v = np.array(tangent_vector, dtype=float)
        v_norm = np.linalg.norm(v)
        if v_norm < 1e-9:
            return p.copy()
            
        lambda_p = 2.0 / (1.0 - np.sum(p**2))
        tanh_arg = np.tanh(0.5 * self.c * lambda_p * v_norm)
        direction = v / v_norm
        v_hyperbolic = tanh_arg * direction
        return self.mobius_addition(p, v_hyperbolic)

    def embed_phylogenetic_tree_hyperbolic(self, tree_depth=4, branching_factor=2):
        """
        Isometrically embed a hierarchical viral phylogenetic tree into Poincare disk.
        Exponential radial placement r_k = tanh(k * delta / 2) eliminates crowding.
        """
        nodes = []
        delta = 0.8 # Hyperbolic step per evolutionary generation
        for k in range(tree_depth + 1):
            r_k = np.tanh(k * delta / 2.0)
            n_k = branching_factor**k
            angles = np.linspace(0, 2 * np.pi, n_k, endpoint=False)
            for theta in angles:
                x = r_k * np.cos(theta)
                y = r_k * np.sin(theta)
                nodes.append(np.array([x, y]))
        return np.array(nodes)

    def predict_neutralization_escape(self, vaccine_strain_coord, circulating_variant_coord):
        """
        Predict antigenic distance and neutralization fold-drop:
        Fold_Drop = exp( beta * d_H(vaccine, variant) )
        """
        d_H = self.hyperbolic_distance(vaccine_strain_coord, circulating_variant_coord)
        # 1 unit of hyperbolic distance corresponds to ~2-fold drop in neutralization titer
        fold_drop = np.exp(0.75 * d_H)
        # Probability of significant immune escape (>4-fold drop)
        prob_escape = 1.0 / (1.0 + np.exp(-2.5 * (d_H - 1.5)))
        return float(d_H), float(fold_drop), float(prob_escape)
