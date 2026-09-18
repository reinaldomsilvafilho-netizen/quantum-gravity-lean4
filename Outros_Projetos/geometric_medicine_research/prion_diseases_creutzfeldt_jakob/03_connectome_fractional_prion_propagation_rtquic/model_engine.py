"""
FRACTIONAL CONNECTOME PRION PROPAGATION, CORTICAL RIBBONING & RT-QuIC ENGINE
Models non-local trans-synaptic sCJD spreading and ultrasensitive CSF ThT amplification
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Treatise Grounding: Chapters 01, 04, 11 & Paper 2 (Simplicial Fractional Laplacians on Networks)
"""

import numpy as np

class ConnectomeRTQuICPrionEngine:
    """
    Simulates non-local prion seed transmission along the structural human connectome
    via the Fractional Graph Laplacian (-Delta_G)^alpha and evaluates RT-QuIC biomarker kinetics.
    """
    def __init__(self, n_nodes=84, alpha_fractional=0.75):
        self.n_nodes = n_nodes
        self.alpha = alpha_fractional
        self.adj, self.laplacian, self.frac_laplacian = self.build_canonical_brain_connectome()

    def build_canonical_brain_connectome(self):
        """
        Builds a modular small-world brain connectome (84 regions: 68 neocortex, 8 basal ganglia, 8 limbic/thalamic).
        Computes the standard degree-normalized Laplacian L and fractional power L^alpha via spectral decomposition.
        """
        np.random.seed(42)
        # Block-modular connectivity: high intra-cortical, strong thalamocortical loops
        adj = np.zeros((self.n_nodes, self.n_nodes))
        
        # Intra-modular neocortical connections (nodes 0 to 67)
        for i in range(68):
            for j in range(i+1, 68):
                if abs(i - j) <= 4 or np.random.rand() < 0.08:
                    w = np.random.uniform(0.5, 2.0)
                    adj[i, j] = w
                    adj[j, i] = w
                    
        # Subcortical / Thalamic nodes (nodes 68 to 83): dense hubs
        for i in range(68, 84):
            for j in range(self.n_nodes):
                if np.random.rand() < 0.25:
                    w = np.random.uniform(1.0, 3.5)
                    adj[i, j] = w
                    adj[j, i] = w
                    
        degrees = np.sum(adj, axis=1)
        # Combinatorial Laplacian L = D - A
        L = np.diag(degrees) - adj
        
        # Symmetrized normalized Laplacian L_sym = D^-1/2 L D^-1/2
        d_inv_sqrt = np.diag(1.0 / np.sqrt(np.maximum(degrees, 1e-5)))
        L_norm = d_inv_sqrt @ L @ d_inv_sqrt
        
        # Spectral decomposition: L = V * Lambda * V^T
        eigvals, eigvecs = np.linalg.eigh(L_norm)
        eigvals_clamped = np.maximum(eigvals, 0.0)
        
        # Fractional graph Laplacian: (-Delta_G)^alpha = V * Lambda^alpha * V^T
        frac_eigvals = eigvals_clamped ** self.alpha
        L_alpha = eigvecs @ np.diag(frac_eigvals) @ eigvecs.T
        
        return adj, L_norm, L_alpha

    def simulate_connectome_propagation(self, seed_node=72, t_days=90.0, dt_days=0.5, diffusion_coeff=0.08):
        """
        Integrates non-local fractional Fisher-KPP equation:
        du/dt = - D * (-Delta_G)^alpha * u + gamma * u * (1 - u)
        Returns time trajectory and final spatial prion distribution across cortex and thalamus.
        """
        n_steps = int(t_days / dt_days)
        u = np.zeros(self.n_nodes)
        u[seed_node] = 0.85 # Initial thalamic / cortical focal seed
        gamma_logistic = 0.05
        
        for _ in range(n_steps):
            diffusion_step = - diffusion_coeff * (self.frac_laplacian @ u)
            reaction_step = gamma_logistic * u * (1.0 - u)
            u = u + dt_days * (diffusion_step + reaction_step)
            u = np.clip(u, 0.0, 1.0)
            
        # Clinical Neuroimaging Markers:
        # 1. Cortical Ribboning Index (CRI): mean burden across neocortical ribbon (nodes 0 to 67)
        cortical_ribboning = float(np.mean(u[:68]))
        # 2. Pulvinar Thalamic Sign (PTR): peak intensity in posterior thalamic hubs (nodes 76 to 83)
        pulvinar_sign = float(np.max(u[76:84]))
        
        return u, cortical_ribboning, pulvinar_sign

    def simulate_rtquic_fluorescence(self, seed_titer_pM, time_hours=60.0):
        """
        Simulates Real-Time Quaking-Induced Conversion (RT-QuIC) Thioflavin T (ThT) assay.
        Lag phase duration is inversely proportional to seed titer:
        t_lag = t_0 - beta * log10(seed + 1e-4)
        """
        s = max(1e-5, float(seed_titer_pM))
        # High sCJD seeds (10-100 pM) amplify within 8-16 hours; non-prion controls remain flat (>55 hours)
        t_lag = float(np.clip(28.0 - 6.5 * np.log10(s), 6.0, 65.0))
        
        # ThT fluorescence at time t = 24 hours (standard clinical cutoff):
        f_max = 65000.0 # Arbitrary Fluorescence Units
        f_0 = 1200.0
        t_eval = 24.0
        
        # Sigmoid ThT kinetics:
        tht_fluorescence = f_0 + (f_max - f_0) / (1.0 + np.exp(- 0.45 * (t_eval - t_lag)))
        
        # Positivity probability: positive if ThT > 10,000 AFU (t_lag < 22 hours)
        prob_positive_rtquic = float(1.0 / (1.0 + np.exp((t_lag - 22.0) / 1.2)))
        
        return {
            'seed_pM': float(seed_titer_pM),
            't_lag_hours': float(t_lag),
            'tht_24h_afu': float(tht_fluorescence),
            'prob_scjd_rtquic': float(prob_positive_rtquic)
        }
