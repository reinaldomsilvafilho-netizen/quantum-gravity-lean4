"""
NON-LINEAR NUCLEATED POLYMERIZATION & CURVATURE-INDUCED FIBRIL FRAGMENTATION ENGINE
Simulates explosive exponential PrPSc replication and amyloid fibril kinetics in sCJD
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Chapters 04 & 06 (Simplicial Transport, Kigami Fractal Resolvents & Curvature Stress)
"""

import numpy as np

class PrionPolymerizationKineticsEngine:
    """
    Solves the coupled non-linear moment equations of Knowles-Griffith nucleated polymerization
    with mechanical bending curvature fragmentation:
    dP/dt = k_n * m^n_c + k_2 * m^n_2 * M + k_-(kappa*) * M
    dM/dt = 2 * k_+ * m * P
    dm/dt = - dM/dt
    """
    def __init__(self, m_total_uM=10.0, k_plus=2.0e3, k_n=1e-12, k_2=1.0, k_minus_base=2.5e-9):
        self.m0 = m_total_uM * 1e-6 # Monomer concentration in Molar
        self.k_plus = k_plus        # Elongation rate (M^-1 s^-1)
        self.k_n = k_n              # Primary nucleation rate (M^(1-nc) s^-1)
        self.n_c = 3                # Primary critical nucleus size
        self.k_2 = k_2              # Secondary surface nucleation rate (M^-n2 s^-1)
        self.n_2 = 2                # Secondary nucleus order
        self.k_minus_base = k_minus_base # Base spontaneous fragmentation rate (s^-1)

    def compute_curvature_fragmentation_rate(self, kappa_star=0.08, kappa_0=0.02):
        """
        Theorem 6.2: Extrinsic bending curvature kappa* induces mechanical shear stress sigma = E * I * kappa*.
        Fibril fracture rate scales quadratically with curvature:
        k_-(kappa*) = k_minus_base * (1.0 + 4.5 * (kappa* / kappa_0)^2)
        """
        kappa_ratio = max(0.0, float(kappa_star)) / kappa_0
        rate = self.k_minus_base * (1.0 + 4.5 * (kappa_ratio ** 2))
        return float(rate)

    def compute_analytical_exponential_growth_rate(self, kappa_star=0.08):
        """
        In the seed-limited regime (m ~ m0), the coupled system satisfies:
        d^2 M / dt^2 = kappa_eff^2 * M, where:
        kappa_eff = sqrt(2 * k_+ * m0 * (k_-(kappa*) + k_2 * m0^n_2))
        Doubling time: t_double = ln(2) / kappa_eff (in hours)
        """
        k_minus = self.compute_curvature_fragmentation_rate(kappa_star)
        inside = 2.0 * self.k_plus * self.m0 * (k_minus + self.k_2 * (self.m0 ** self.n_2))
        kappa_eff = np.sqrt(max(inside, 1e-18)) # in s^-1
        
        t_double_s = np.log(2.0) / kappa_eff
        t_double_hours = t_double_s / 3600.0
        return float(kappa_eff), float(t_double_hours)

    def simulate_polymerization_trajectory(self, t_max_hours=48.0, n_steps=200, 
                                           seed_fraction=1e-5, kappa_star=0.08):
        """
        Integrates the non-linear coupled system over time via 4th-order Runge-Kutta.
        Returns time array (hours), monomer m(t), fibril number P(t), and fibril mass M(t).
        """
        t_max_s = t_max_hours * 3600.0
        dt = t_max_s / n_steps
        times = np.linspace(0, t_max_hours, n_steps)
        
        # Initial conditions:
        M_init = self.m0 * seed_fraction
        P_init = M_init / 100.0 # Average initial seed length = 100 monomers
        m_init = self.m0 - M_init
        
        k_minus = self.compute_curvature_fragmentation_rate(kappa_star)
        
        m_arr = [m_init]
        P_arr = [P_init]
        M_arr = [M_init]
        
        m_curr = m_init
        P_curr = P_init
        M_curr = M_init
        
        def derivatives(m, P, M):
            m_clamped = max(0.0, m)
            dP = self.k_n * (m_clamped**self.n_c) + self.k_2 * (m_clamped**self.n_2) * M + k_minus * M
            dM = 2.0 * self.k_plus * m_clamped * P
            # Conservation clamp: cannot convert more than remaining monomer
            dM = min(dM, m_clamped / dt)
            dm = - dM
            return dm, dP, dM

        for _ in range(n_steps - 1):
            dm1, dP1, dM1 = derivatives(m_curr, P_curr, M_curr)
            dm2, dP2, dM2 = derivatives(m_curr + 0.5*dt*dm1, P_curr + 0.5*dt*dP1, M_curr + 0.5*dt*dM1)
            dm3, dP3, dM3 = derivatives(m_curr + 0.5*dt*dm2, P_curr + 0.5*dt*dP2, M_curr + 0.5*dt*dM2)
            dm4, dP4, dM4 = derivatives(m_curr + dt*dm3, P_curr + dt*dP3, M_curr + dt*dM3)
            
            m_next = m_curr + (dt / 6.0) * (dm1 + 2*dm2 + 2*dm3 + dm4)
            P_next = P_curr + (dt / 6.0) * (dP1 + 2*dP2 + 2*dP3 + dP4)
            M_next = M_curr + (dt / 6.0) * (dM1 + 2*dM2 + 2*dM3 + dM4)
            
            # Physical conservation enforcement
            M_next = np.clip(M_next, 0.0, self.m0)
            m_next = self.m0 - M_next
            
            m_arr.append(m_next)
            P_arr.append(P_next)
            M_arr.append(M_next)
            
            m_curr = m_next
            P_curr = P_next
            M_curr = M_next
            
        return times, np.array(m_arr), np.array(P_arr), np.array(M_arr)

    def classify_amyloid_kinetics(self, doubling_time_hours):
        """
        Classifies kinetic profile:
        - Explosive Prion (sCJD): t_double < 3.5 hours (rapid lethal progression)
        - Slow Non-Prion Amyloid: t_double > 5.0 hours
        """
        prob_explosive_prion = float(1.0 / (1.0 + np.exp((doubling_time_hours - 4.5) / 0.8)))
        return prob_explosive_prion
