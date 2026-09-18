"""
REFRACTORY EPILEPSY & ECOG GAUGE HOLONOMY SOZ ENGINE (PILLAR 02)
Theoretical Grounding: Treatise Chapter 01 (Metric Spaces & Tensors) &
Chapter 11 (Non-Abelian Gauge Holonomies & Optimal Transport Flows, DOI: 10.5281/zenodo.22290043)
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
"""

import numpy as np

class EpilepsyFocusLocalizationEngine:
    def __init__(self, n_channels=32, grid_dim=(4, 8)):
        """
        Cortical subdural ECoG electrode grid.
        n_channels: 32 electrodes placed on a 4x8 planar cortical patch.
        """
        self.n_channels = n_channels
        self.grid_dim = grid_dim
        # 2D coordinates of electrodes in millimeters (10 mm spacing)
        rows, cols = grid_dim
        coords = []
        for r in range(rows):
            for c in range(cols):
                coords.append([r * 10.0, c * 10.0])
        self.electrode_coords = np.array(coords)

    def compute_optimal_transport_velocity(self, ecog_signal_window):
        """
        Derive the instantaneous cortical phase velocity field v(x, y)
        from spatio-temporal phase gradients across the electrode grid.
        ecog_signal_window: (n_channels, n_timepoints)
        """
        # Phase across electrodes via Hilbert-like temporal derivative
        signal_grad_t = np.gradient(ecog_signal_window, axis=1)
        phase_energy = np.mean(signal_grad_t**2, axis=1)
        
        # Spatial gradient of energy across 2D grid: nabla E
        grid_energy = phase_energy.reshape(self.grid_dim)
        grad_y, grad_x = np.gradient(grid_energy, 10.0) # spacing 10 mm
        
        # Velocity field v = - grad E
        vx = -grad_x.flatten()
        vy = -grad_y.flatten()
        velocity_field = np.column_stack([vx, vy])
        
        # Compute divergence: div(v) = d(vx)/dx + d(vy)/dy
        div_x = np.gradient(vx.reshape(self.grid_dim), 10.0, axis=1).flatten()
        div_y = np.gradient(vy.reshape(self.grid_dim), 10.0, axis=0).flatten()
        divergence = div_x + div_y
        
        return velocity_field, divergence, phase_energy

    def compute_gauge_holonomy(self, velocity_field, center_idx=10):
        """
        Compute discrete Wilson loop holonomy along a closed 4-electrode circuit:
        W = exp( i * oint v . dr )
        Non-zero circulation indicates a topological phase vortex / pacemaker core.
        """
        r = center_idx // self.grid_dim[1]
        c = center_idx % self.grid_dim[1]
        if r >= self.grid_dim[0] - 1 or c >= self.grid_dim[1] - 1:
            return 0.0, 1.0 # boundary
            
        # Circuit: (r, c) -> (r, c+1) -> (r+1, c+1) -> (r+1, c) -> (r, c)
        i1 = r * self.grid_dim[1] + c
        i2 = r * self.grid_dim[1] + (c + 1)
        i3 = (r + 1) * self.grid_dim[1] + (c + 1)
        i4 = (r + 1) * self.grid_dim[1] + c
        
        # Line integral oint v . dr
        circulation = (
            velocity_field[i1, 0] * 10.0 +
            velocity_field[i2, 1] * 10.0 -
            velocity_field[i3, 0] * 10.0 -
            velocity_field[i4, 1] * 10.0
        )
        wilson_trace = np.cos(circulation / 100.0) # gauge trace
        return float(circulation), float(wilson_trace)

    def localize_seizure_onset_zone(self, ecog_signal_window):
        """
        Localize true Seizure Onset Zone (SOZ) pacemaker:
        Combines positive flow divergence (source) with high local energy and topological circulation.
        """
        v_field, divergence, energy = self.compute_optimal_transport_velocity(ecog_signal_window)
        
        # Pacemaker score: high divergence + high energy
        # True pacemaker emits energy (div > 0), downstream nodes absorb (div <= 0)
        norm_div = (divergence - np.mean(divergence)) / max(np.std(divergence), 1e-6)
        norm_energy = (energy - np.mean(energy)) / max(np.std(energy), 1e-6)
        
        soz_scores = 0.6 * np.maximum(norm_div, 0.0) + 0.4 * norm_energy
        predicted_soz_idx = int(np.argmax(soz_scores))
        predicted_coord_mm = self.electrode_coords[predicted_soz_idx]
        
        circ, wilson = self.compute_gauge_holonomy(v_field, center_idx=predicted_soz_idx)
        
        return {
            'predicted_soz_idx': predicted_soz_idx,
            'predicted_coord_mm': predicted_coord_mm,
            'soz_scores': soz_scores,
            'pacemaker_divergence': float(divergence[predicted_soz_idx]),
            'holonomy_circulation': float(circ),
            'wilson_trace': float(wilson)
        }
