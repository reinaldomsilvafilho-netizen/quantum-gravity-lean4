# Blind layer-1 referee report: "A Functorial Bridge from Continuous Tensor Manifolds to 4-Dimensional Spacetime Cobordisms"

- Concept DOI 10.5281/zenodo.22441676. Referee: independent blind session (Claude Opus), 2026-10-06. Protocol: `unified_quantum_gravity_book/audit/verify/PROTOCOL.md`, layer 1.
- Files not read: `ADVERSARIAL_REVIEW_R7.md`, `CLAUDE_*`, `PROOF_SKELETON_R7.md`, the ledgers, WORKPLAN and CHANGELOG. `formal_proofs_lean4/CLAUDE_LEAN_AUDIT.md` was not read either.
- Scripts and outputs are in `audit/scripts/`. Every check has an independent oracle and a negative control.
  - `zenodo_check.py`, `zenodo_desc.py`: version check.
  - `math_checks.py`: checks C1–C8. Result: 0 failed checks; each counterexample is reproduced.
  - `lean_check.py`: compiles the Lean files and runs `#print axioms`, with a negative control.
  - `crossref_check.py`: resolves the DOIs, with a fake-DOI control.

## Step 0: Zenodo version

- **Versions:** Zenodo has one version, record 22441680 (DOI 10.5281/zenodo.22441680), published 2026-09-06. Its only file is `paper_functorial_tensor_field_theory.pdf`, saved as `audit/zenodo_latest.pdf`.
- **Comparison with the local source:** I compared the word sequences of the local `.tex` and the PDF text.
  - Similarity ratio: 0.869. Every non-equal block is LaTeX markup, running heads, or hyphenation; there is no difference in prose or in theorem content. Negative control (shuffled words): 0.009.
  - The local PDF against the Zenodo PDF: ratio 0.987.
  - Theorem numbering is identical: Def 2.1, Prop 2.2, Def 3.1, Lemma 5.1, Thm 5.2, Thm 5.3, Prop 5.4, Cor 5.5, Thm 5.6.
- **Verdict: MATCH.** The audit below applies to both.
- **The Zenodo landing-page description claims more than the paper.** It says the work verifies "the Atiyah-Segal cobordism sewing axiom" and that the proofs are "machine-verified with 100% rigor in Lean 4 (0 errors, 0 warnings, 0 sorry)". See item FV.

## Table

| Item | Statement (1 line) | Honest label? | Verdict | Evidence |
|---|---|---|---|---|
| Abs-1 | Abstract: "We resolve the third open frontier … constructing an exact symmetric monoidal functor". | No | PROBLEM (M) | The body does not construct a well-defined functor, and the categories involved are not categories (see A1–A8). "Unified Grand Synthesis" is never referenced. |
| Abs-2 | Abstract: morphisms include "graphon contractions". | No | PROBLEM (B) | Graphon contractions are never defined in the body. |
| Abs-3 | Abstract: the image cobordisms "satisfy the Einstein field equations". | No | PROBLEM (A) | This rests on Lemma 5.1, which is false (C4). |
| Abs-4 | Abstract: the Atiyah–Segal sewing axiom is "categorically isomorphic" to tensor contraction and to Wheeler–DeWitt. | No | PROBLEM (M) | Prop 5.4 is a heuristic dictionary with no isomorphism; its own proof is labelled "semiclassical derivation". |
| Intro | "Resolve this question completely"; "tensor contractions are strictly isomorphic to … evolution in GR"; RT/QFI/relative-entropy dualities "demonstrated". | No | PROBLEM (M) | These are overclaims, and the cited dualities carry no citations. |
| Def 2.1(a) objects | A 5-tuple (M, T, ρ, ψ, π) with a QFI immersion and ADM constraints on-shell. | n/a | PROBLEM (M) | Details below the table. |
| Def 2.1(a) j_i | j_i := +Re Tr(π† ∂_i ψ); Sec. 4.2 asserts j_i = −n^μ h_i^ν T_μν. | n/a | PROBLEM (A) | Checked with the paper's own T_μν and π = n^μ∂_μΨ: −n h T = **−**Re Tr(π† ∂_iψ) (C6; max error 3e-12; the unmutated sign misses by ≥ 2.8e-2). The momentum constraint in the on-shell condition therefore has the wrong source sign. ρ_matt = n n T is correct (C6b). |
| Def 2.1(b–d) category | Morphisms are classes of gradient flows modulo Diff⁺([0,1],∂); composition is concatenation; associativity and identities are claimed to hold. | Asserted, not proved | PROBLEM (A) | Details below the table. |
| Prop 2.2 | CTensMan is a symmetric dagger-(compact) monoidal category with ⊗ = (⊔, ⊗, ⊗, ⊔, ⊔), unit (∅,1,1,0,0) and a dual T*. | No proof given | PROBLEM (A) | Details below the table. |
| Def 3.1 Cob | Objects (Σ,h,ψ); morphisms are "equivalence classes" of Lorentzian cobordisms solving Einstein-matter; symmetric monoidal under ⊔. | n/a | PROBLEM (A) | Details below the table. |
| §4.1 QFI metric | Projected immersion ⇒ g^QFI(v,v) = 4‖d̄T(v)‖² > 0; g^QFI is invariant under x-dependent phases. | Proved here | CONFIRMS (with remark) | The computation is correct for a normalized pure-state field. Positivity is the immersion hypothesis restated, so it is not a result. The numerics confirm positive eigenvalues and that the projector matters (C7: dropping it changes g_xx from 2.15 to 3.27). The claim that bond-gauge invariance follows "by the fundamental theorem of MPS [Verstraete–Cirac 2010]" is a misattribution (B): that PRL introduces cMPS and does not prove a fundamental theorem. |
| §4.2 lapse | N = (((∂_t S_vN)² + σ₀²)/κ₀²)^{1/4} is "strictly C^∞", with N ≥ √(σ₀/κ₀). | Proved here | PROBLEM (A) | The lower bound is correct, but smoothness is false. S_vN is not differentiable where ρ changes rank. With ρ(t) = diag(1−t, t), which is smooth and admissible, ∂_tS = log((1−t)/t) → ∞ and N grows like \|log t\|^{1/2} (C2: N = 2.17, 3.04, 3.72, 4.30 at t = 1e-2…1e-8; the full-rank control stays bounded by 1.219). Also, ρ(x,t) along a flow is never defined by the flow T(t), since ρ is independent object data (M). Dimensions are consistent (κ₀ has units of 1/time). |
| §4.2 shift | N^i = h^{ij} Re Tr(ρ[Q,∂_jQ] + R†∂_jR). | Definition | PROBLEM (B), feeds A8 | Because Q ∈ u(χ) and ρ is Hermitian, Re Tr(ρ[Q,∂Q]) ≡ 0 (C1a: ≤ 2e-15; the generic-Q control is ≥ 2e-3), so that term is dead. The remaining term is Re Tr(R†∂_jR) = ½∂_j‖R‖²_HS (C1b, with h-refinement), a gradient shift. Under t → α(t), N^i does not transform as α'N^i (see A6). |
| §4.2 matter | S_matt and "canonical variation recovers ρ_matt and j_i"; Ψ is "generated along the trajectory". | Asserted | PROBLEM (M) | Ψ in the bulk is never defined. No matter field equation is imposed anywhere, so ∇_μT^{μν} = 0 is not available (see Lemma 5.1). The j_i sign is wrong (row "Def 2.1(a) j_i"). |
| §4.2 well-definedness on classes | F is defined on a representative flow and then used on the classes [Φ]. | Implicit | PROBLEM (A) | The lapse is not reparametrization-covariant: it would need to scale as N → α'N, but ((α'S')² + σ₀²)^{1/4} does not. The invariant 4-volume ∫N a³ dt of the image metric −N²dt² + a(t)²dx² on T³ depends on the representative: 2.2082 (α = t), 1.9565 (α = t²), 1.9120 (smoothstep), whereas the covariant-lapse control gives a spread of 4e-16 (C3). Hence F([Φ]) is not well defined: it is not a map on the morphisms. |
| Lemma 5.1 | If S is the pull-back of S_ADM and its "Hessian" satisfies (5.1), then the image metric and Ψ solve G + Λg = 8πG T. | "Lemma" with proof | PROBLEM (A) | Details below the table. |
| Thm 5.2(1) | F(id_T) = id_{F(T)}. | Theorem | PROBLEM (A) | Details below the table. |
| Thm 5.2(2) | F preserves composition via Darmois–Israel gluing with [K] = 0. | Theorem | PROBLEM (A) | Details below the table. |
| Thm 5.3(1) | Natural isomorphisms F(T₁) ⊔ F(T₂) ≅ F(T₁ ⊗ T₂) and ∅ ≅ F(1), with Mac Lane associativity, unitality and braiding coherence. | Theorem | PROBLEM (A) | Details below the table. |
| Thm 5.3(2) | F(T*) ≅ F(T)*. | Theorem | PROBLEM (M) | g^QFI(T*) = g^QFI(T) is correct (C7: difference 0). However, the dual object in Cob is never defined in Def 3.1; the step is asserted "in Cob". Also, T* has ψ = R† while its generators are conj(R), which violates the object constraint ψ := R (B). |
| Prop 5.4 | Under log χ ~ Area/4G_N, the sewing axiom "admits a structural dictionary" with Tr_χ(T₁T₂) and with the WDW constraints for χ ≫ 1. | No: heuristic labelled Proposition | PROBLEM (M) | Part (1) claims that CTensMan composition is "defined via bond contraction", but Def 2.1 defines it as concatenation of flows. Part (2) is an analogy ("asymptotically furnish the generator algebra"). Citations: RT gives S = Area/4G, not log χ, which is a tensor-network bound (B). Order of magnitude (C8): for Area = 1 m², log χ ≈ 9.6×10⁶⁸, i.e. χ ≈ 10^(4×10⁶⁸). Physically, "χ ≫ 1" means bond dimensions with no operational meaning. |
| Cor 5.5 | If a unitary Z: Cob^NEC → Hilb exists, then Z∘F assigns states and amplitudes ⟨Ψ₂\|e^{−iĤΔt}\|Ψ₁⟩. | Conditional corollary | PROBLEM (M) | Composing functors is trivial only if F is a functor, which it is not (A1–A8). The specific amplitude formula is not derived: in canonical GR Ĥ ≈ 0, and Δt is undefined for a cobordism. Cob^NEC has no definition as a category. |
| Thm 5.6 faithfulness | F is faithful modulo C^∞(M, SU(χ)). | Theorem | PROBLEM (M) | The proof invokes a "fundamental theorem of cMPS extended to the matter-coupled sector", which does not exist in [Verstraete–Cirac] and is not proved. It also assumes that finitely many functions (h, K, N, N^i, Ψ) reconstruct the infinite-dimensional trajectory T(t) ∈ P(H); g^QFI alone is invariant under any x-independent unitary of H. Since F is not well defined on classes (C3), the statement has no content. "Faithful modulo a gauge group" is not faithfulness. |
| Thm 5.6 NEC | T_kk = ‖k^μ∇_μΨ‖²_HS ≥ 0 for null k; then R_kk ≥ 0; this "prevents … closed timelike curves". | Theorem | Mixed | Algebraic part: **CONFIRMS** (C5: 500 random Lorentzian metrics and null vectors, relative gap ≤ 7e-14; the timelike control mismatches 500/500). R_kk = 8πG T_kk uses Lemma 5.1 (A). "Prevents CTCs" is false as a general implication (M): Gödel's dust universe satisfies the NEC and has CTCs. Since T_kk ≥ 0 holds for every Ψ of this form, Cob^NEC equals Cob for this matter, so the "embedding into Cob^NEC" is vacuous. No entropy enters, so "Entropic" is a misnomer (B). The QNEC form ħS''/2π matches Bousso et al. 2016. |
| Conclusion | Bullets: Σ are "functorial images"; cobordisms "are" gradient flows; "Matter fields and Wilson loops are continuous limits of tensor network holonomies"; "proving spacetime geometry is fundamentally a functorial manifestation…". | No | PROBLEM (M) | Wilson loops and holonomy limits never appear in the body. The other bullets depend on A1–A8. |
| FV (Formal Verification section, and the Zenodo description) | Defs 2.1 and 3.1 and Thms 5.2, 5.3, 5.6 are "formally verified in Lean 4 (v4.33.1)"; Zenodo adds "100% rigor, 0 errors, 0 warnings, 0 sorry". | No | PROBLEM (A) | Details below the table. |
| Bib | Six cited references. | n/a | PROBLEM (B) | Every DOI resolves (Crossref; the fake-DOI control gives 404). Details below the table. |

### Def 2.1(a): problems with the objects (M)

1. K_ij is not part of the object data, so the on-shell condition "its associated extrinsic curvature" is undefined.
2. The Hamiltonian constraint here has no Λ, while Lemma 5.1 uses −2Λ, so the two are inconsistent unless Λ = 0 (B).
3. "(Q,R) ∈ u(χ) × End" disagrees with the standard normalized cMPS form Q = −iK − ½R†R (B).
4. ψ := R is not invariant under bond gauge (R → gRg⁻¹), so it is not a function of the physical state (B).
5. M carries its own Riemannian metric, which is redundant beside h = g^QFI (B).

### Def 2.1(b–d): the category axioms fail (A)

- **Identity law fails.** id∘f is f(2s) followed by a constant path. f∘α can never be constant on an interval, because a non-stationary gradient-flow solution never stops: if its velocity vanished at some point, ODE uniqueness would make it a critical point and constant. Hence id∘f ≠ [f] for every non-identity f.
- **Boundary-flat reparametrizations are not diffeomorphisms.** They have α'(0) = 0. The associativity re-bracketing is a piecewise-linear homeomorphism, not an element of Diff⁺. So "strict associativity" is not established either.
- **Composition is not closed.** A concatenation is only a "piecewise gradient flow", which is not a morphism as defined.
- **The functional S is unspecified.** If S is fixed, S strictly decreases along non-trivial flows, so no non-identity morphism has an inverse and Hom(T₂,T₁) = ∅ whenever Hom(T₁,T₂) contains a non-trivial flow.
- **Flows preserve M.** Hom(T₁,T₂) = ∅ unless M₁ = M₂, so no topology change is possible. The "cobordisms" are all cylinders.
- A Moore-path or thin-homotopy construction would repair the first two points. It is not given.

### Prop 2.2: dagger-compact monoidal structure (A)

- **The tensor product leaves the category.** M₁ ⊔ M₂ is disconnected, which violates "connected" in Def 2.1.
- **The unit is not an object.** It has χ = 1 < 2 and M = ∅.
- **Type mismatch.** ρ₁⊗ρ₂ is a χ₁χ₂ × χ₁χ₂ matrix, while ψ₁ ⊔ ψ₂ are χᵢ × χᵢ matrices (M).
- **No dagger.** The dagger is not defined on morphisms. Reversing a gradient flow gives an ascent, not a morphism.
- **"Compact" is false.** It needs η: 1 → T*⊗T, but Hom(∅, −M ⊔ M) = ∅ because flows fix the manifold.
- There is no proof at all.

### Def 3.1 Cob: not a category (A)

- No composition or identity is defined, and the equivalence relation is never specified.
- **No identities.** A Lorentzian cylinder of positive duration is not a unit for gluing: M ∪ cylinder is not isometric to M. This is the standard obstruction for geometric cobordism categories (Segal).
- **Composition is not closed.** Gluing along Σ with only matching induced metrics gives a C⁰ metric with distributional curvature, which leaves the class of smooth Einstein solutions.
- Monoidal coherence is asserted only.

### Lemma 5.1: circular and false (A)

- **The proof is circular.** It says "if the constraints vanish initially **and the evolution equations hold**, then …". The ∂_tK_ij evolution equation is never derived. Condition (5.1) only re-defines K as a "Hessian".
- **Type mismatch in (5.1).** It equates a bilinear form on T(M^TT) with a 2-tensor on M (M).
- **∇T = 0 is unjustified.** The claim that it follows "from gauge covariance of the cMPS bond algebra" is a non sequitur, since no matter equation of motion is imposed.
- **The quoted ∂_tK equation is wrong** (B). It lacks the factor N on S_ij, the trace part ½h(S−ρ), and the −NΛh term.
- **Counterexample (C4).** All data the proof uses are admissible:
  - Setup: h(t) = a(t)²δ on T³, N = 1, N^i = 0 (R spatially constant ⇒ ½∂‖R‖² = 0), Ψ = const, V = 0 ⇒ T_μν = 0. The scale factor is a = 1 + 3t² − 2t³, which is monotone, so the path is a valid gradient-flow class, and boundary-flat.
  - Both endpoints are flat with K = 0, hence on-shell. On-shell at the endpoints forces Λ = 0.
  - At t = ½: G_tt = 3(ȧ/a)² = 3 ≠ 0. The sympy Einstein tensor matches the Friedmann oracle, and the de Sitter control gives residual 0.
  - Caveat: I did not construct an explicit cMPS family with QFI metric a(t)²δ. The proof never uses cMPS structure, so it is invalid regardless.

### Theorem 5.2: functoriality

**(1) F(id_T) = id_{F(T)} fails (A).**
- For the static flow the shift is N_i = ½∂_i‖R‖², which is generally non-zero. Then K_ij = (1/2N)(∂_iN_j + ∂_jN_i) ≠ 0. Example: ‖R‖² = 2 + cos x gives K_xx = −cos(x)/2 (C1c).
- So F(id) is not the static cylinder −dt² + h.
- "Normalizing N = 1 by a constant time rescaling" changes the interval [0,1] to [0,c].
- In any case, Cob has no identity morphisms (see Def 3.1).

**(2) F preserves composition: the proof fails (A).**
- It rests on Lemma 5.1, which is false.
- F is not well defined on classes (C3).
- The concatenation is not a morphism of CTensMan.
- The smoothness argument at the junction (boundary-flat ⇒ [K] = 0) is plausible for the image metric. However, the boundary-flat representatives are exactly what changes F's value (C3).
- The Israel sign convention is not stated (B).

### Theorem 5.3(1): monoidal structure (A)

- ⊗ and the unit are not objects (see Prop 2.2).
- F on product morphisms [Φ₁]⊗[Φ₂] is never defined (M).
- "Strict disjoint union so the associator is the identity": disjoint union is associative only up to canonical isomorphism (B).
- The braiding square is asserted only.

### Formal verification: the claim is false (A)

The repository is `formal_proofs_lean4`. Neither version imports Mathlib; the `Category` and `Functor` classes are home-made.

**Working tree:**
- It compiles with exit code 0.
- Every metric type is `Unit`. `QFI_NonDegenerate`, `ADM_Constraints_Satisfied`, `PositiveDefinite3D`, `ADM_Lapse_Smooth` and `Einstein_Equations_Satisfied` are all `fun _ => True`. The probe `∀ g, Einstein_Equations_Satisfied g` is proved by `trivial`.
- The build emits 15 `linter.defProp` warnings, which contradicts "0 warnings".

**Git HEAD (the pushed GitHub version):**
- It has 32 `axiom` declarations.
- `#print axioms` shows that map_id/map_comp/object_monoidal_isomorphism/braiding_naturality depend on `emergentEinsteinMap`, `tensorADM`, `emergentMetric_tensor_distrib` and others. These axioms assert the conclusions.

**What is actually verified:**
1. The free path category on a quiver is a category.
2. The induced map of free categories preserves identity and composition.
3. A sum of squares of a `List Int` is ≥ 0.

None of these concerns QFI metrics, Lorentzian geometry, the Einstein equations, the paper's quotient categories, or monoidal coherence. `braiding_naturality` is an equality of `Unit` values or axioms. The negative control (2+2=5) fails to compile, as it should.

### Bibliography details (B)

- Atiyah's actual title is "Topological quantum field theory" (singular).
- Segal's pages per Crossref are 432–575 (doi 10.1017/cbo9780511526398.019); the paper gives 421–577.
- Verstraete–Cirac is misattributed (see §4.1).
- RT is used for log χ, which it does not give (see Prop 5.4).
- Three self-citations (book, flows, Beyond the Spectrum) are never cited in the text, and they have no DOIs although the book has concept DOI 10.5281/zenodo.22290043.
- Fourès-Bruhat 1952 is correct (Acta Math 88:141–225). It is a local existence theorem; it does not show that a metric prescribed by external data satisfies the Einstein equations.
- Bousso et al. 2016 is correct.

## Summary of PROBLEMs by severity

**A: mathematical or physical errors (10)**
1. **A1.** CTensMan is not a category as defined. id∘f ≠ f modulo Diff⁺([0,1],∂); boundary-flat reparametrizations are not diffeomorphisms; concatenations are not gradient flows.
2. **A2.** The monoidal product and the unit leave CTensMan: M₁⊔M₂ is disconnected, and the unit has χ = 1 and M = ∅.
3. **A3.** The "dagger-compact" claim is false: the dagger is undefined on morphisms, and Hom(1, T*⊗T) = ∅ because flows fix M.
4. **A4.** Cob is not a category: it has no identities (finite-duration cylinders), its composition by gluing is not closed in smooth Einstein solutions, and its equivalence relation is undefined.
5. **A5.** The lapse is not smooth: it is unbounded where ρ changes rank (C2).
6. **A6.** F is not well defined on reparametrization classes, since the lapse and shift are not covariant (C3: the 4-volume depends on the representative).
7. **A7.** Lemma 5.1 is circular (it assumes the evolution equations) and false (C4: an admissible on-shell FRW counterexample).
8. **A8.** Thm 5.2 fails: F(id) ≠ id because the shift ½∂‖R‖² is non-zero and gives K ≠ 0 (C1c), and composition rests on A6–A7. Thm 5.3 fails by A2.
9. **A9.** Sign error: Eq. (2.3) gives j_i = +Re Tr(π†∂ψ), whereas −n^μh_i^νT_μν = −Re Tr(π†∂ψ) (C6).
10. **A10.** The formal-verification claim is false: no Mathlib, Unit/True placeholders, 32 axioms in the pushed version, and warnings present. Only generic free-category facts and "sum of integer squares ≥ 0" are verified.

**M: gaps or wrong labels (14)**
1. The on-shell K is undefined.
2. The functional S is unspecified.
3. Prop 2.2 has no proof.
4. ρ₁⊗ρ₂ and ψ have mismatched dimensions.
5. The Hessian condition equates objects of different types.
6. No matter equation is imposed, so ∇T = 0 is not justified.
7. ρ(x,t) along the flow is undefined.
8. F on product morphisms is undefined, and the dual in Cob is undefined.
9. Prop 5.4 is a heuristic labelled "Proposition".
10. Cor 5.5: the amplitude formula is not derived.
11. Thm 5.6: faithfulness rests on a nonexistent theorem.
12. "NEC prevents CTCs" is false; Gödel's universe is a counterexample.
13. Abstract and introduction overclaim (resolve, exact, isomorphic, sewing verified).
14. The conclusion claims things absent from the body (Wilson loops, "proving" emergence).

**B: wording or citations (12)**
1. Q ∈ u(χ) is non-standard, and the [Q,∂Q] term in the shift is identically zero.
2. Λ appears in Lemma 5.1 but not in Def 2.1.
3. The ∂_tK equation is wrong as quoted.
4. The Israel sign convention is not stated.
5. "Strict" ⊔ associativity is claimed.
6. "Graphon contractions" are undefined.
7. ψ = R is not gauge-invariant, and T* breaks ψ = R.
8. Citations: the Atiyah title, the Segal pages, the Verstraete–Cirac "fundamental theorem", RT used for log χ, three uncited self-references without DOIs, and the unreferenced "Unified Grand Synthesis".
9. The scale of χ ~ exp(10⁶⁹) for 1 m² is never discussed.
10. "Entropic" NEC involves no entropy.
11. M carries a redundant Riemannian metric.
12. The Zenodo description adds "verify the sewing axiom" and "100% rigor".

**CONFIRMS:**
- the QFI positivity computation (§4.1), given the immersion hypothesis;
- the phase invariance of g^QFI;
- g^QFI(T*) = g^QFI(T) (C7);
- ρ_matt = n n T (C6b);
- the algebraic identity T_kk = ‖k·∇Ψ‖²_HS ≥ 0 (C5);
- the lapse lower bound N ≥ √(σ₀/κ₀).

## Close (prova-rigorosa)

- **Hardest step:** Lemma 5.1. It cannot be repaired without imposing the Einstein evolution equations, together with a matter equation of motion, as part of the definition of morphisms. The functor would then be defined only on solutions, not on arbitrary gradient flows.
- **What would rescue a weaker statement:** restrict to fixed M; use Moore-path morphisms of solutions of the Einstein-matter system; use a time-covariant lapse; and define Cob with collars or a semicategory. The honest result would then be "a lax assignment from solution-flows to globally hyperbolic cylinders". That is close to tautological.
- **Literature consulted (resolved DOIs):**
  - Atiyah 1988, 10.1007/BF02698547
  - Verstraete–Cirac 2010, 10.1103/PhysRevLett.104.190405
  - Ryu–Takayanagi 2006, 10.1103/PhysRevLett.96.181602
  - Fourès-Bruhat 1952, 10.1007/BF02392131
  - Bousso et al. 2016, 10.1103/PhysRevD.93.024017
  - Segal 2004, 10.1017/cbo9780511526398.019
