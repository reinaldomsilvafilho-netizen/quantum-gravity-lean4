# Module 03: Unified Simplicial Quantum Gravity vs. Causal Dynamical Triangulations (CDT) & Causal Sets

**Author**: Reinaldo M. Silva-Filho  
**Institution**: PPGEE/DES, Universidade Federal de Lavras (UFLA)  
**Support**: CAPES Finance Code 001  
**Monograph DOI**: [10.5281/zenodo.22290043](https://doi.org/10.5281/zenodo.22290043)  

---

## 1. Executive Summary: The Discrete Geometric Family

Causal Dynamical Triangulations (CDT), Causal Sets, and Unified Simplicial Quantum Gravity belong to the discrete, relational school of quantum spacetime. All three reject smooth differential manifolds at the fundamental scale, building spacetime from discrete elements:
- **CDT (Ambjørn, Jurkiewicz, Loll)**: Uses discrete 4-simplices glued along tetrahedral faces, evaluating the path integral via numerical Monte Carlo simulations over causal foliations.
- **Causal Sets (Sorkin, Bombelli, Dowker)**: Uses locally finite partially ordered sets (posets) governed solely by causal precedence ($x \prec y$), where number equals volume ($N \sim V$).
- **Unified Simplicial Quantum Gravity**: Formulates an analytical, continuous variational theory on the simplicial product $\Delta_4 \times \Delta_2$, utilizing fractional Beta-Laplacians and Graphon limits to bridge the discrete Planck lattice with smooth macroscopic general relativity.

---

## 2. In-Depth Analysis of CDT and Causal Sets

### A. Causal Dynamical Triangulations (CDT)
#### Core Strengths:
1. **Dynamic Generation of 4D Spacetime**:
   Prior to CDT, Euclidean dynamical triangulations collapsed into either an unphysical 2D "branched polymer" phase or an infinite-dimensional "crumpled" phase. By enforcing a causal arrow of time (a strict global foliation $t \in \mathbb{R}$), CDT became the first lattice quantum gravity model to dynamically produce a macroscopic, 4-dimensional de Sitter-like universe.
2. **Discovery of Dimensional Flow ($d_s = 4 \to 2$)**:
   In 2005, Ambjørn, Jurkiewicz, and Loll demonstrated numerically via diffusion processes that spacetime changes its spectral dimension:
   $$d_s(\text{macro}) \approx 4.02 \pm 0.10 \quad \longrightarrow \quad d_s(\text{Planck}) \approx 1.80 \pm 0.25$$
   This dimensional reduction provided the first evidence that quantum gravity might be non-perturbatively renormalizable at high energies.

#### Structural Vulnerabilities:
1. **Dependence on Numerical Monte Carlo Simulations**:
   CDT lacks a closed, analytical formulation of its continuum limit. All claims rely on statistical averaging over finite ensembles of triangulations (typically $N \sim 10^5 - 10^6$ simplices) running on computer clusters.
2. **The Matter Coupling Impasse**:
   Coupling non-Abelian gauge fields and chiral fermions to CDT lattices induces severe numerical instabilities and fermion doubling / sign problems. CDT remains predominantly a theory of pure quantum gravity.
3. **Absence of Standard Model Unification**:
   CDT provides no mechanism to explain why the low-energy world contains three generations of quarks and leptons, why the gauge group is $\mathrm{SU}(3) \times \mathrm{SU}(2) \times \mathrm{U}(1)$, or why particle masses have specific values.

---

### B. Causal Set Theory
#### Core Strengths:
1. **Extreme Conceptual Minimalism**:
   Based on Malament's theorem (causal structure + volume element determines spacetime metric), Causal Set Theory posits that spacetime is simply a locally finite partially ordered set $(C, \prec)$:
   $$\text{Order} + \text{Number} = \text{Geometry}$$
2. **Strict Lorentz Invariance Without Lattice Artifacts**:
   By using random Poisson sprinkling of points into a manifold, Causal Sets avoids the preferred frame issues common to regular spatial lattices, preserving Lorentz invariance on average.
3. **Prediction of the Cosmological Constant Order of Magnitude**:
   Sorkin (1991) predicted that Poissonian fluctuations in the number of spacetime elements $N$ within a causal horizon volume would induce a fluctuating dark energy density:
   $$\rho_\Lambda \sim \frac{M_P^4}{\sqrt{N}} \sim 10^{-122} M_P^4$$
   anticipating the order of magnitude of the cosmological constant before its 1998 observational discovery.

#### Structural Vulnerabilities:
1. **The Hauptvermutung (Main Conjecture) Remains Unproven**:
   It has never been mathematically proven that two distinct continuous spacetimes cannot approximate the same discrete causal set. Reconstructing local 4D Riemannian manifolds from generic posets without prior embedding remains an unsolved inverse problem.
2. **Noisy Differential Operators**:
   Constructing the d'Alembertian operator $\Box_{\mathrm{CS}}$ on a causal set requires non-local sums over multiple layers of causal predecessors. The resulting operator is plagued by high-amplitude Poissonian fluctuations that must be artificially smoothed out.
3. **Fermion and Gauge Field Sterility**:
   Formulating chiral fermions and Yang-Mills gauge theories on a discrete poset without a continuous bundle structure is an open, highly resistant mathematical problem.

---

## 3. Side-by-Side Architectural Comparison

| Feature | Causal Dynamical Triangulations | Causal Sets | Unified Simplicial Quantum Gravity |
| :--- | :--- | :--- | :--- |
| **Spacetime Ontology** | Sum over glued 4-simplices $\sum e^{i S_{\mathrm{Regge}}}$ | Partially ordered set $(C, \prec)$ with Poisson sprinkling | Continuous variational functional on $\Delta_4 \times \Delta_2$ |
| **Methodology** | Numerical Monte Carlo lattice simulations | Combinatorial graph and order theory | Analytical functional analysis & Lean 4 verification |
| **Spectral Dimension Flow** | Discovered numerically: $d_s \to 2$ in the UV | Not easily defined; non-integer Hausdorff dimension | Derived analytically from Beta-Laplacian heat kernel: $d_s(k) = 2 \to 4$ |
| **Matter Coupling** | Extremely difficult; unaddressed Standard Model | Unsolved; fermions require non-local discrete layers | Native: gauge forms on $\partial \Delta_4$, fermions as Dirac–Kähler forms |
| **Particle Generations** | None | None | Exactly 3 generations from internal flavor simplex $\Delta_2$ |
| **Continuum Limit** | Deduced from numerical finite-size scaling | Unproven (Hauptvermutung barrier) | Proven via Graphon Ricci flow and Trotter-Kato resolvents |
| **Cosmological Constant** | Tuned as a bare lattice parameter | Heuristic Poisson fluctuation $\sim 1/\sqrt{N}$ | Exact analytical value: $\rho_\Lambda \approx (2.28\text{ meV})^4$ (Barnes $G$-defect) |
| **Singularity Resolution** | Volume bounces in ensemble averages | Poset discreteness truncates singularity | Topological quantum vortex pressure $P_{\mathrm{top}} \sim 4.63 \times 10^{113}\text{ Pa}$ |

---

## 4. Advantages of the Simplicial Framework over CDT and Causal Sets

1. **Analytical Tractability vs. Monte Carlo Simulations**:
   CDT's dimensional reduction was an empirical numerical discovery without an exact analytical derivation. In our framework, the running spectral dimension $d_s(t) = 2 \to 4$ is proven analytically (Theorem 2.1, Chapter 12) from the asymptotic scaling of the heat kernel return probability of the fractional Beta-Laplacian $(-\Delta_{\Delta_4})^\alpha$.
2. **Resolution of the Continuum Limit Barrier**:
   While Causal Sets struggles with the Hauptvermutung and CDT relies on numerical extrapolation, the Simplicial Framework employs the mathematical theory of **Graphon Ricci Flow**. By defining an $L^\infty$-minimax reach bound $\kappa^* \le 1/\ell_P$, microscopic simplicial networks are proven to converge unconditionally to smooth, $C^{1,1}$-regular Einstein spacetimes.
3. **Full Standard Model Unification**:
   Neither CDT nor Causal Sets can explain the existence of electrons, quarks, photons, or gluons. The Simplicial Framework natively generates the $\mathrm{SU}(3) \times \mathrm{SU}(2) \times \mathrm{U}(1)$ gauge group, derives the Koide lepton ratio $K_l = 2/3$, and explains the 3 fermion generations via the symmetry group $S_3 = \operatorname{Aut}(\Delta_2)$.

---

## 5. Honest Limitations & Challenges of the Simplicial Framework Relative to CDT and Causal Sets

1. **Large-Scale Lattice Path Integral Validation**: CDT has run trillions of Monte Carlo sweeps over decades, confirming that statistical ensembles of simplices spontaneously generate macroscopic 4D de Sitter spheres without fine-tuning. The Simplicial Framework relies on variational minimax principles; large-scale stochastic path integral simulations of our specific Beta-Laplacian action across billions of simplices have not yet been executed on supercomputing clusters.
2. **Lorentz Invariance Validation**: Causal Sets' Poisson sprinkling guarantees Lorentz invariance with mathematical elegance. In our simplicial framework, Lorentz invariance is emergent at scales $r \gg \ell_P$ through the Graphon limit, but microscopic Lorentz invariance is broken at the single-simplex scale, requiring ongoing precision experimental bounds on non-commutative dephasing.
3. **Community Validation of Sorkin's Fluctuation Idea**: Sorkin's cosmological constant heuristic remains one of the most celebrated conceptual insights in discrete gravity. While our Barnes $G$-defect derivation gives an exact numerical value ($2.28\text{ meV}$), Causal Set theorists argue that dark energy should exhibit observable temporal fluctuations ($d\rho_\Lambda/dt \ne 0$), a feature that differs from our static topological defect.
