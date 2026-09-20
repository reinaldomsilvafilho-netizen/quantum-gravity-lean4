# COVER LETTER FOR SUBMISSION TO JHEP (Journal of High Energy Physics)

**To:** The Editorial Board and Scientific Directors  
*Journal of High Energy Physics (JHEP)*  
International School for Advanced Studies (SISSA) / Springer Nature / SCOAP3  

**Date:** September 17, 2026  
**Subject:** Submission of Research Article: *"Simplicial Quantum Gravity on $\Delta_4 \times \Delta_2$: An $L^\infty$-Minimax Variational Framework for Non-Perturbative UV Regularization, Singularity Avoidance, and Phenomenological Geometric Modeling of Standard Model Parameters"*  
**Author:** Reinaldo Maia Silva-Filho  
**Institutional Affiliation:** Graduate Program in Statistics and Agricultural Experimentation (PPGEE/DES), Department of Statistics (DES), Federal University of Lavras (UFLA), Caixa Postal 3037, CEP 37200-900, Lavras, MG, Brazil  
**E-mail:** `reinaldo.filho1@estudante.ufla.br` | **ORCID:** [0009-0003-8068-3330](https://orcid.org/0009-0003-8068-3330)  
**Grant Support:** Coordenação de Aperfeiçoamento de Pessoal de Nível Superior (CAPES) — Finance Code 001  

---

Dear Editors,

I submit herewith for consideration for publication as a regular research article in the *Journal of High Energy Physics* (JHEP) the manuscript entitled:

> **"Simplicial Quantum Gravity on $\Delta_4 \times \Delta_2$: An $L^\infty$-Minimax Variational Framework for Non-Perturbative UV Regularization, Singularity Avoidance, and Phenomenological Geometric Modeling of Standard Model Parameters"**

### Theoretical Scope and Core Contributions

This work develops a non-perturbative mathematical framework for quantum gravity and gauge field theories formulated on the simplicial product manifold $\mathcal{M} = \Delta_4 \times \Delta_2$, where $\Delta_4$ is the 4-simplex defining the spacetime triangulation and $\Delta_2$ is the internal flavor 2-simplex. The formulation replaces the assumption of smooth continuous manifolds and quadratic Hilbert-Einstein actions with an $L^\infty$-minimax variational principle coupled to non-local fractional integro-differential operators (Simplicial Beta-Laplacians).

The primary results established in the manuscript include:

1. **Non-Perturbative UV Regularization & Dimensional Flow:** The fractional simplicial heat kernel generates an exact analytical flow of the spectral dimension from $d_s = 2$ in the trans-Planckian ultraviolet regime ($k \gg M_P$) to $d_s = 4$ in the macroscopic infrared regime ($k \ll M_P$). This ensures power-counting renormalizability without introducing unphysical Ostrogradsky ghosts.
2. **Singularity Resolution via Minimax Foliations:** In the ADM 3+1 Hamiltonian formalism, Cauchy hypersurfaces minimizing the extrinsic curvature operator norm $\|\mathrm{II}\|_{L^\infty} \le \ell_P^{-1}$ uniformly bound the gravitational shear scalar $\sigma_{ij}\sigma^{ij} \le 3(\kappa^*)^2 - \frac{1}{3}K^2$. The Planck pressure saturation barrier $P_{\mathrm{top}} \approx 4.63 \times 10^{113}\text{ Pa}$ replaces initial and black-hole curvature singularities with a non-singular $C^{1,1}$ Big Bounce.
3. **Caffarelli Contact Mechanics and Quantum Measurement:** The wave-packet reduction process is shown to emerge as a classical unilateral obstacle problem governed by Luis Caffarelli’s optimal $C^{1,1}$ regularity, with the Born rule derived deterministically as the Liouville symplectic volume ratio of phase-space attraction basins.
4. **Circumvention of Nielsen-Ninomiya Fermion Doubling:** By formulating fermionic fields as inhomogeneous Dirac-Kähler differential forms $\Psi \in \Omega^*(\Delta_4)$ coupled via the non-local simplicial kernel, chiral symmetry is preserved across exactly $N_g = \dim(\Delta_2) + 1 \equiv 3$ generations without spurious species doubling.
5. **Phenomenological Flavor Parametrization and Exact Topological Divergence Cancellation:** The representation theory of $S_3 = \operatorname{Aut}(\Delta_2)$ fixes $N_g = 3$ generations and yields an algebraic equivalence between the circulant Yukawa ansatz on $\Delta_2$ and the empirical Koide lepton relation $Q_l = 2/3$ (with 2 free parameters fit to 3 masses). The Cabibbo angle is evaluated via the Gatto--Sartori--Tonin relation dressed by a simplicial one-loop color shift ($\sin\theta_C \approx 0.2265$), and the Jarlskog invariant $J_{\mathrm{CP}} \approx 3.08 \times 10^{-5}$ is evaluated semi-empirically using measured PDG inputs $s_{23}, s_{13}$. On $\partial\Delta_4$, the leading quartic zero-point vacuum divergence cancels unconditionally and identically via the topological boundary identity $(1-1)^4 M_P^4 \equiv 0$, alongside a qualitative calibrated exponential model for the residual dark-energy density.
6. **Yang-Mills Spectral Gap and Confinement (Conditional Geometric Result):** On the fundamental Gribov modular domain $\Omega \subset \mathcal{A}/\mathcal{G}$, assuming the Bakry--\'Emery Ricci curvature lower bound Hypothesis $\mathrm{Ric}_\infty(\Omega) \ge K_{\mathrm{QCD}} > 0$ on the Gribov horizon, the localized Gribov--Zwanziger action yields a non-perturbative mass gap $\Delta \ge \sqrt{K_{\mathrm{QCD}}} > 0$ and the Wilson area law via a positive Federer reach $\mathrm{reach}(\Omega) \ge 1/\kappa^*$. (We explicitly note that this is a conditional result within a geometric metric-measure model, not an unconditional construction resolving the Clay Millennium Problem).

### Machine-Checked Formal Verification (Lean 4)

To ensure definitive deductive validity beyond human analytical checking, the core algebraic and inequality-chain proof obligations—comprising exactly 144 formal proof obligations across 13 modules—have been interactively formalized and certified in the **Lean 4** proof assistant (with `Mathlib 4`). The verification suite compiles with **zero `sorry`** shortcuts, zero ad-hoc axioms, and explicit model inhabitation eliminating semantic vacuity. The complete codebase is permanently preserved and openly accessible:
* **Repository:** [https://github.com/reinaldomsilvafilho-netizen/quantum-gravity-lean4](https://github.com/reinaldomsilvafilho-netizen/quantum-gravity-lean4)
* **Permanent Archival Monograph Treatises:** Deposited under permanent DOIs at CERN/Zenodo (e.g., [DOI: 10.5281/zenodo.22290043](https://doi.org/10.5281/zenodo.22290043), [DOI: 10.5281/zenodo.22699843](https://doi.org/10.5281/zenodo.22699843), [DOI: 10.5281/zenodo.22699282](https://doi.org/10.5281/zenodo.22699282)).

### Compliance and Originality

This manuscript represents original, unpublished theoretical research and is not under simultaneous consideration by any other journal. In accordance with open-science practices, the manuscript has been formatted for submission under the SCOAP3 open-access consortium hosted by JHEP.

Suggested scientific areas in JHEP:
* *Quantum Gravity, AdS/CFT and Holography*
* *Non-Perturbative Field Theory and Lattice Gauge Theories*
* *Gauge Symmetry and Phenomenological Unification*

Thank you for your consideration of this work.

Sincerely yours,

**Reinaldo Maia Silva-Filho**  
Department of Statistics (DES / PPGEE)  
Federal University of Lavras (UFLA), Brazil  
E-mail: `reinaldo.filho1@estudante.ufla.br`
