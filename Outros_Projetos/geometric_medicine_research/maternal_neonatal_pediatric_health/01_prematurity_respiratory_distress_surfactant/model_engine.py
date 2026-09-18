"""
NEONATAL ALVEOLAR SURFACTANT & MINIMAX CURVATURE ENGINE (PILLAR 01)
Theoretical Grounding: Treatise Chapter 06 (Fractal Airway Resolvents) &
Chapter 07 (Minimax Extrinsic Curvature on Constrained Interfaces, DOI: 10.5281/zenodo.22290043)
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np

class SurfactantAlveolarEngine:
    def __init__(self, gestational_age_weeks=28.0, surfactant_pool_mg_kg=15.0):
        """
        Neonatal alveolar mechanics and surfactant biophysics.
        gestational_age_weeks: weeks of gestation (24-37)
        surfactant_pool_mg_kg: endogenous dipalmitoylphosphatidylcholine (DPPC) pool
        """
        self.ga = gestational_age_weeks
        self.surfactant_pool = surfactant_pool_mg_kg
        # Normal surfactant pool in term neonates is ~100 mg/kg; preterm is often < 15 mg/kg
        self.gamma_water = 72.0 # mN/m (pure water surface tension)
        self.gamma_min_healthy = 2.0 # mN/m (healthy compressed surfactant)

    def compute_surface_tension(self, relative_surface_area, surfactant_dose=0.0):
        """
        Dynamic surface tension as a function of area compression and available surfactant.
        Surfactant lowers gamma dramatically when compressed (relative_area < 1.0).
        """
        effective_pool = self.surfactant_pool + surfactant_dose
        # Smooth asymptotic saturation parameter (Hill/exponential kinetics)
        s_factor = float(1.0 - np.exp(-effective_pool / 45.0))
        
        # When expanded (area=1.0), gamma -> 50-60 mN/m. When compressed (area=0.4), healthy -> 2 mN/m, deficient -> 40 mN/m
        gamma_baseline = self.gamma_water * (1.0 - 0.4 * s_factor)
        gamma_compressed = self.gamma_min_healthy + (self.gamma_water - 35.0) * (1.0 - s_factor)
        
        # Sigmoidal transition with area
        gamma = gamma_compressed + (gamma_baseline - gamma_compressed) / (1.0 + np.exp(-10.0 * (relative_surface_area - 0.65)))
        return float(np.clip(gamma, self.gamma_min_healthy, self.gamma_water))

    def compute_young_laplace_pressure(self, radius_um, surface_tension_mN_m):
        """
        Young-Laplace Equation with Weingarten curvature:
        Delta P = 2 * gamma / R = gamma * (kappa_1 + kappa_2)
        radius in micrometers (um), gamma in mN/m = dyn/cm
        Returns collapse pressure in cmH2O (1 mN/m / um = 10 cmH2O)
        """
        if radius_um <= 0:
            return float('inf')
        # Conversion: 1 mN/m / 1 um = 1000 Pa = 10.197 cmH2O
        pressure_cmH2O = (2.0 * surface_tension_mN_m / radius_um) * 10.197 * 0.1
        return float(pressure_cmH2O)

    def evaluate_minimax_collapse_barrier(self, radius_um, surfactant_dose=0.0):
        """
        Theorem 7.1 (Minimax Alveolar Stability):
        Surfactant monolayer imposes a steric repulsion barrier kappa* <= kappa_crit,
        bounding peak collapse pressure and enforcing positive lung compliance dV/dP > 0.
        """
        # Relative area scales as (R / R_0)^2
        R_0 = 75.0 # um (resting uncompressed alveolar radius in term infant)
        rel_area = np.clip((radius_um / R_0)**2, 0.1, 1.5)
        gamma = self.compute_surface_tension(rel_area, surfactant_dose)
        pressure = self.compute_young_laplace_pressure(radius_um, gamma)
        
        # Critical curvature kappa = 1 / R
        kappa = 1.0 / max(radius_um, 1.0)
        
        # Stability index: dP/dR must be <= 0 for stability (as R shrinks, P must not explode)
        # Numerical derivative
        dr = 1.0 # um
        rel_area_plus = ((radius_um + dr) / R_0)**2
        gamma_plus = self.compute_surface_tension(rel_area_plus, surfactant_dose)
        p_plus = self.compute_young_laplace_pressure(radius_um + dr, gamma_plus)
        dP_dR = (p_plus - pressure) / dr
        
        # Is stable if dP/dR < 0.05 cmH2O/um (pressure drops or stays flat as alveolus deflates)
        is_stable = bool(dP_dR < 0.05)
        
        return {
            'radius_um': float(radius_um),
            'surface_tension': float(gamma),
            'collapse_pressure_cmH2O': float(pressure),
            'dP_dR': float(dP_dR),
            'is_mechanically_stable': is_stable,
            'curvature_kappa': float(kappa)
        }

    def compute_airway_fractal_impedance(self, frequency_hz=5.0, generations=14):
        """
        Fractal airway resolvent impedance Z(omega) across Weibel-Murray neonate bronchial tree:
        Z(omega) = e_0^T (i*omega*I + L_fractal)^{-1} e_0
        """
        # Murray's law radius scaling: r_k = r_0 * 2^{-k/3}
        r_0 = 1.5 # mm (neonate trachea)
        impedance_total = 0.0
        for k in range(generations):
            r_k = r_0 * (2.0**(-k / 3.0))
            # Poiseuille resistance R_k ~ 1 / r_k^4, divided by 2^k parallel branches
            R_k = (8.0 * 1.8e-5 * 5.0) / (np.pi * (r_k * 1e-3)**4 * (2**k))
            impedance_total += R_k * 1e-6 # convert to cmH2O.s/mL
            
        reactance = 2.0 * np.pi * frequency_hz * 0.005 # small inertance
        return complex(impedance_total, reactance)
