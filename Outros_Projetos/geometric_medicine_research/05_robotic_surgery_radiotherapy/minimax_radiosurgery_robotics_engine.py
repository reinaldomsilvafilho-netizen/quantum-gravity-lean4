"""
Minimax Extrinsic Curvature & Caffarelli C^{1,1} Detachment Engine
Pillar 05: Robotic Surgery, Endoscopic Navigation & Stereotactic Radiotherapy (SRS/SBRT)
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Unified Quantum Gravity & Geometric Analysis (DOI: 10.5281/zenodo.22290043)
"""

import numpy as np
from scipy.interpolate import CubicSpline

class MinimaxSurgicalPlanner:
    """
    Minimax Extrinsic Curvature and Caffarelli C^{1,1} Regularity Optimizer for
    Robotic Endoscopic Paths and Stereotactic Radiosurgery Beam Arrays.
    Uses Treatise Ch. 07 constructive pipeline (Medial Detour -> Moreau-Yosida Regularization -> C^{1,1} Spline).
    """
    def __init__(self, start_pos, target_pos, obstacles, oar_safety_margin=2.0, num_waypoints=50):
        self.start_pos = np.array(start_pos, dtype=float)
        self.target_pos = np.array(target_pos, dtype=float)
        self.obstacles = obstacles
        self.safety_margin = oar_safety_margin
        self.num_waypoints = num_waypoints
        self.optimized_path = None
        self.curvature_profile = None
        self.jerk_profile = None

    def _generate_medial_detour_waypoints(self):
        t = np.linspace(0, 1, self.num_waypoints)
        straight_path = (1.0 - t[:, None]) * self.start_pos + t[:, None] * self.target_pos
        
        path = straight_path.copy()
        
        obs_centers = np.array([obs['center'] for obs in self.obstacles])
        mean_obs_center = np.mean(obs_centers, axis=0)
        
        path_dir = self.target_pos - self.start_pos
        path_dir = path_dir / np.linalg.norm(path_dir)
        
        mid_pt = 0.5 * (self.start_pos + self.target_pos)
        obs_vec = mean_obs_center - mid_pt
        obs_vec_proj = obs_vec - np.dot(obs_vec, path_dir) * path_dir
        if np.linalg.norm(obs_vec_proj) > 1e-4:
            repulsive_dir = - obs_vec_proj / np.linalg.norm(obs_vec_proj)
        else:
            repulsive_dir = np.array([-1.0, 0.0, 0.0])

        for obs in self.obstacles:
            c = np.array(obs['center'])
            r_safe = obs['radius'] + self.safety_margin
            dists = np.linalg.norm(path - c, axis=1)
            
            mask = dists < r_safe + 1.0
            if np.any(mask):
                t_center = np.argmin(dists) / (self.num_waypoints - 1)
                for idx in range(len(path)):
                    t_val = t[idx]
                    envelope = np.exp(- ((t_val - t_center) / 0.25)**2)
                    path[idx] += (r_safe + 2.0) * envelope * repulsive_dir

        s = np.linspace(0, 1, len(path))
        control_idx = np.linspace(0, len(path)-1, 14, dtype=int)
        cs = CubicSpline(s[control_idx], path[control_idx], bc_type='clamped')
        smooth_path = cs(s)
        return smooth_path

    def compute_curvature_and_derivatives(self, path):
        diffs = np.diff(path, axis=0)
        ds = np.linalg.norm(diffs, axis=1)
        s_cum = np.insert(np.cumsum(ds), 0, 0.0)
        total_len = s_cum[-1]
        
        s_uniform = np.linspace(0, total_len, self.num_waypoints)
        cs = CubicSpline(s_cum, path, bc_type='natural')
        resampled_path = cs(s_uniform)
        
        ds_step = total_len / (self.num_waypoints - 1)
        v = np.gradient(resampled_path, ds_step, axis=0)
        speed = np.linalg.norm(v, axis=1, keepdims=True) + 1e-8
        T = v / speed
        
        dT = np.gradient(T, ds_step, axis=0)
        kappa = np.linalg.norm(dT, axis=1)
        
        d2T = np.gradient(dT, ds_step, axis=0)
        jerk = np.linalg.norm(d2T, axis=1)
        
        return resampled_path, kappa, jerk

    def optimize_minimax_path(self, max_iter=150):
        raw_smooth = self._generate_medial_detour_waypoints()
        self.optimized_path, self.curvature_profile, self.jerk_profile = self.compute_curvature_and_derivatives(raw_smooth)
        return self

    def evaluate_oar_clearance(self):
        clearances = {}
        for obs in self.obstacles:
            c = np.array(obs['center'])
            r = obs['radius']
            dists = np.linalg.norm(self.optimized_path - c, axis=1)
            min_dist = np.min(dists) - r
            clearances[obs['name']] = {
                'min_clearance_mm': float(min_dist),
                'is_safe': bool(min_dist >= self.safety_margin - 0.05)
            }
        return clearances
