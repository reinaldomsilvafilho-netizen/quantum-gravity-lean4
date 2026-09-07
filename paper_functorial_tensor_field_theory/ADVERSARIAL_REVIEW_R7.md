# Deep Adversarial Review: Functorial Tensor Field Theory

This document contains a rigorous Phase 1 and 1.5 adversarial proof audit of the functorial construction between $\mathbf{CTensMan}$ and $\mathbf{Cob}_{3+1}^{\mathbf{Fields}}$.

### A. Hypothesis Discharge & General Rigor
- The proofs frequently invoke physical intuitions ("continuous scaling limit", "precisely matches") without the requisite mathematical derivations. 
- Discharged hypotheses often implicitly assume canonical quantization structures (e.g., Wheeler-DeWitt constraints) that are never formally constructed in the source category.

### B-F. Detailed Vulnerability Reports

## Lemma 5.1 (Dynamical Einstein-ADM Equivalence)
- **id**: 1
- **status**: INVALID
- **impact**: GLOBAL
- **category**: LOGICAL_GAP
- **location**: Section 5 / Proof of Lemma 5.1
- **statement**: "the extrinsic curvature $K_{ij} ...$ precisely matches the Hessian of the entanglement action ... the metric $g_{\mu\nu}$ identically satisfies the Einstein equations."
- **why_invalid**: The proof asserts an exact algebraic equality between the extrinsic curvature (defined via Lie derivatives and the ad-hoc lapse $N$) and the Hessian of $\mathcal{S}$ without any explicit derivation. Furthermore, defining the lapse via entropy production $\partial_t S_{\mathrm{vN}}$ does not magically solve the Hamiltonian and momentum constraints of General Relativity. In GR, constraints restrict initial data. Arbitrary gradient flows on tensor manifolds will generically violate these constraints.
- **counterexample**: CANDIDATE (Adversarial parameter scaling). Taking the limit $\kappa_0 \to \infty$ sends the lapse $N \to 0$ independently of the spatial geometry. This causes $K_{ij}$ to diverge, violently violating the Hamiltonian constraint unless the matter density scales in an exactly correlated (but unproven) manner.
- **affects**: Theorem 5.4, Theorem 5.6.
- **minimal_fix**: Restrict the objects of $\mathbf{CTensMan}$ to "on-shell" tensor states whose initial data explicitly solves the momentum/Hamiltonian constraints, and mathematically prove that the gradient flow preserves these constraints (constraint propagation).

## Theorem 5.2 (Functoriality of F)
- **id**: 2
- **status**: INVALID
- **impact**: GLOBAL
- **category**: LOGICAL_GAP
- **location**: Section 5 / Proof of Theorem 5.2
- **statement**: "Concatenated representative flow is equipped with a smooth boundary mollifier $\chi(t)$ such that all derivatives... vanish at the gluing hypersurface $t=1$... The glued metric is $C^\infty$-smooth and satisfies the Einstein equations globally"
- **why_invalid**: A morphism in $\mathbf{CTensMan}$ is defined strictly as a solution to the projected gradient flow equation $\frac{d\mathcal{T}}{dt} = -P \nabla \mathcal{S}$. If you modify the trajectory $\mathcal{T}(t)$ with a mollifier $\chi(t)$ to force derivatives to zero at the boundary, the modified path is *no longer a gradient flow*. You cannot preserve both the defining differential equation of the morphism and the $C^\infty$ gluing requirement simultaneously. 
- **counterexample**: YES. Any non-trivial gradient flow where $\partial_t \mathcal{T}(1) \neq 0$ will, upon mollification, yield $\partial_t \mathcal{T}(1) = 0$. This violates $\frac{d\mathcal{T}}{dt} = -P \nabla \mathcal{S}$ at the boundary unless the gradient is identically zero (a fixed point).
- **affects**: Functoriality (specifically, composition preservation).
- **minimal_fix**: Relax the morphism definition in $\mathbf{CTensMan}$ to be "piecewise smooth gradient flows" and change $\mathbf{Cob}$ morphisms to topological/piecewise-smooth cobordisms to allow corner defects at gluing surfaces, dropping the unphysical $C^\infty$ mollifier requirement.

## Theorem 5.3 (Dagger-Monoidal Coherence)
- **id**: 3
- **status**: UNJUSTIFIED
- **impact**: LOCAL
- **category**: HIDDEN_ASSUMPTION
- **location**: Section 5 / Proof of Theorem 5.3
- **statement**: "The Quantum Fisher Information metric decomposes into a direct sum... establishes the canonical object isomorphism"
- **why_invalid**: While $g^{\mathrm{QFI}}$ block-diagonalizes for product states, the formal definition of symmetric monoidal coherence requires verifying the Mac Lane pentagon and hexagon diagrams. The proof dismisses this as "standard Cartesian properties". However, in $\mathbf{Cob}_{3+1}^{\mathbf{Fields}}$, diffeomorphism equivalences must explicitly preserve the boundary matter configurations $\psi_\Sigma$.
- **counterexample**: NO. The result is likely true but requires proper proof.
- **affects**: Categorical rigor of the Monoidal functor.
- **minimal_fix**: Explicitly write down the natural isomorphism mapping for the matter sections and trace the coherence diagrams.

## Theorem 5.4 (Category-Theoretic Sewing and Wheeler-DeWitt)
- **id**: 4
- **status**: UNJUSTIFIED
- **impact**: GLOBAL
- **category**: UNJUSTIFIED_ASSERTION
- **location**: Section 5 / Proof of Theorem 5.4
- **statement**: "the discrete bond contraction ... passes in the continuous scaling limit to the path integral ... gluing in CTens is functorially equivalent to the complete Wheeler-DeWitt constraint system"
- **why_invalid**: The leap from a finite-dimensional tensor trace $\mathrm{Tr}_\chi$ to a Feynman path integral over Riemannian metrics requires measure-theoretic derivation that is completely absent. Furthermore, equating the tensor gauge drift to the momentum constraint $\hat{\mathcal{M}}_i |\Psi_{\mathrm{WDW}}\rangle = 0$ requires a strict isomorphism between the local $SU(\chi)$ gauge algebra of the tensor network and the spatial diffeomorphism algebra $\mathrm{Diff}(\Sigma)$, which is not established.
- **counterexample**: CANDIDATE (Dimensional Collapse). In 1 spatial dimension ($d=1$), the spatial diffeomorphism group is $\mathrm{Diff}(S^1)$ (associated with the Virasoro algebra), while the tensor network gauge group is local $SU(\chi)$ (associated with Kac-Moody algebras). These algebras have completely different representations and central charges; their constraint equations cannot be naively isomorphic.
- **affects**: Corollary 5.5, the central physical interpretation.
- **minimal_fix**: Frame this result as a physical conjecture rather than a theorem, or provide the exact Lie algebra homomorphism mapping $su(\chi)$ constraints to spatial diffeomorphisms.

## Theorem 5.6 (Faithful Embedding and NEC) - Part 1: Faithfulness
- **id**: 5
- **status**: INVALID
- **impact**: GLOBAL
- **category**: LOGICAL_GAP
- **location**: Section 5 / Proof of Theorem 5.6
- **statement**: "Since the Quantum Fisher metric uniquely determines the local state up to global phase and local gauge rotations... two gradient flow trajectories coincide up to gauge"
- **why_invalid**: The QFI metric is a pullback metric on the spatial manifold $\Sigma$ measuring the statistical distance between nearby coordinates $\mathcal{T}(x)$ and $\mathcal{T}(x+dx)$. It absolutely does *not* uniquely identify the tensor state $\mathcal{T}$ in the parameter space. Infinite sets of entirely distinct states can induce the same spatial metric. Therefore, $\mathcal{F}([\Phi_1]) = \mathcal{F}([\Phi_2])$ does NOT imply $[\Phi_1] = [\Phi_2]$ in $\mathbf{CTensMan}$. 
- **counterexample**: YES. Consider two entirely distinct translationally invariant cMPS states. Both will induce a completely flat QFI metric $h_{ij} = \delta_{ij}$ (up to scaling). They will map to identical cobordisms, but they are clearly distinct objects in the source category.
- **affects**: The claim that the functor is a faithful embedding.
- **minimal_fix**: Acknowledge that the functor is NOT faithful, or redefine the objects in the target category to carry the full tensor state parameterization, not just the induced metric.

## Theorem 5.6 (Faithful Embedding and NEC) - Part 2: NEC Compliance
- **id**: 6
- **status**: INVALID
- **impact**: GLOBAL
- **category**: UNJUSTIFIED_ASSERTION
- **location**: Section 5 / Proof of Theorem 5.6
- **statement**: "the quantum entanglement flux across the null horizon satisfies $\frac{d^2 S_{\mathrm{vN}}}{d\lambda^2} \le 0$... translates to $R_{\mu\nu} k^\mu k^\nu \ge 0$"
- **why_invalid**: The parameter $\lambda$ in the Raychaudhuri equation is the affine parameter of a 4D spacetime null geodesic $k^\mu$. However, the monotonicity of relative entropy $D(\rho(t_1) \parallel \sigma)$ and SSA properties invoked in the proof apply exclusively to the *gradient flow time* $t$. Conflating the temporal flow parameter $t$ with a bulk spacetime null parameter $\lambda$ is mathematically incorrect. 
- **counterexample**: CANDIDATE (Degeneracy). If a flow is static ($\partial_t S_{\mathrm{vN}} = 0$), $N$ is constant, and the spacetime is a static cylinder. A null geodesic $k^\mu$ moves through both space and time, but relative entropy along the time direction $t$ is exactly constant. The sign of $\frac{d^2 S_{\mathrm{vN}}}{d\lambda^2}$ across a spatial slice cannot be derived from time-monotonicity alone.
- **affects**: Proof of Null Energy Condition compliance.
- **minimal_fix**: Properly utilize the Quantum Null Energy Condition (QNEC) framework, computing the second shape derivative of entanglement entropy along lightcone cuts, rather than improperly substituting the flow parameter $t$ for $\lambda$.
