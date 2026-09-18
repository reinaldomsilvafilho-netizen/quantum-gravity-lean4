"""
Master Verification Runner: Foundations of Geometric and Topological Statistical Inference
Executes all 5 standalone numerical testbeds across all 15 obligations.

Author: Reinaldo Maia Silva-Filho
Affiliation: PPGEE/DES, Universidade Federal de Lavras (UFLA)
"""

import sys
import os
import time

def main():
    print("================================================================================")
    print("  FOUNDATIONS OF GEOMETRIC AND TOPOLOGICAL STATISTICAL INFERENCE")
    print("  Master Numerical Verification Suite (All 5 Thematic Axes)")
    print("  Author: Reinaldo Maia Silva-Filho (PPGEE/DES, UFLA)")
    print("================================================================================\n")
    
    start_time = time.time()
    
    # Axis 1
    import verify_axis1_simplicial_priors as ax1
    ax1.test_axis1_simplicial_priors()
    print("\n")
    
    # Axis 2
    import verify_axis2_reach_langevin_mcmc as ax2
    ax2.test_axis2_reach_mcmc()
    print("\n")
    
    # Axis 3
    import verify_axis3_minimax_natural_gradient as ax3
    ax3.test_axis3_information_vi()
    print("\n")
    
    # Axis 4
    import verify_axis4_tensor_train_likelihood as ax4
    ax4.test_axis4_tensor_train_likelihood()
    print("\n")
    
    # Axis 5
    import verify_axis5_jarzynski_evidence_diffusion as ax5
    ax5.test_axis5_jarzynski_evidence()
    print("\n")
    
    elapsed = time.time() - start_time
    
    print("================================================================================")
    print(f"  ALL 15 OBLIGATIONS ACROSS ALL 5 AXES VERIFIED AND CERTIFIED!")
    print(f"  Total Verification Time: {elapsed:.2f} seconds")
    print("================================================================================")

if __name__ == "__main__":
    main()
