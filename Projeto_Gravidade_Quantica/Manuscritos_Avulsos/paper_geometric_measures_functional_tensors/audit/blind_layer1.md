# Blind referee report, layer 1: *Beyond the Spectrum II* (Vol. II)

- **Work:** "Beyond the Spectrum II: Metric Measure Geometry, Persistent Homology, and Non-Commutative Invariants of Functional Tensor Manifolds"
- **Zenodo concept DOI:** 10.5281/zenodo.22644743
- **Referee:** independent blind referee (Claude Opus 5.5 subagent, clean context), 2026-10-06
- **Protocol:** `unified_quantum_gravity_book/audit/verify/PROTOCOL.md`, layer 1, plus the `prova-rigorosa` skill
- **Scripts and outputs:** `audit/scripts/*.py` and `*.out.txt`. Every numerical script has an independent oracle and a negative control.

## 0. Version check

| Source | What it is | Result |
|---|---|---|
| Zenodo latest record **22866175** (2026-09-21) | Holds only `beyond_the_spectrum_trilogy.pdf` (1 391 818 B). There is **no** separate Vol. II PDF and **no** Lean zip in this version. | md5 `8d872f4d…` is identical to the local `beyond_the_spectrum_files/beyond_the_spectrum_trilogy_updated.pdf`. |
| Vol. II extracted from that trilogy | Trilogy pages 29–46, saved as `audit/zenodo_latest_vol2.pdf` | Text is **identical** to the local `beyond_the_spectrum_files/volume_2_geometric_measures.pdf`: page-wise ratio 1.0000, 0 word-level diffs (`compare_versions.out.txt`). |
| Record 22699282 (2026-09-11) `volume_2_geometric_measures.pdf` | Earlier record | md5 `18a4603d…` is byte-identical to the local `volume_2_geometric_measures.pdf` and to the local `paper_geometric_measures_functional_tensors.pdf`. |
| Record 22644744 (2026-09-07) | First version | Contains an earlier Vol. II (793 099 B). Not audited. |
| **Local `.tex`** (modified 2026-09-22, after the PDF of 2026-09-10) | Compiled fresh in the scratchpad | It **differs** from Zenodo: similarity 0.914, 110 diff ops (`compare_tex_vs_zenodo.out.txt`). |

### What the Zenodo text has that the local `.tex` lacks

- **Thm 2.5 proof:** an approximation argument by "convex exhaustions".
- **Thm 3.4:** states the conclusion as "Dgm₁(A) = ∅ ≠ {(2,0)}". It adds a general claim, "for N_k ≥ 2 distinct lifetimes, entropies strictly differ", and a closing paragraph on "smooth generic perturbations".
- **Thm 4.4(a):** says "compact regular level hypersurface strictly in the interior".
- **§6.3:** "d+1 matrices" and a **new Theorem 6.3**, "Quantized Cyclic Cocycles and Topological Degree". In the local `.tex` this is only an unlabeled sentence.
- **Thm 7.2:** an added hypothesis, "∂_μρ linearly independent", and "almost everywhere".
- **Bibliography:** DOIs and ISBNs. The full UFLA/DES affiliation.

### What the local `.tex` has that Zenodo lacks

- **Thm 3.4:** states "E_pers⁽¹⁾(A) ≠ E_pers⁽¹⁾(B)" without qualification. It adds the paragraph "with a single normalized bar, E=0 … perturbing … (2,2.2,2.4) yields multiple bars".
- **Šafránek reference:** article number 062320. This number is wrong: see B-refs.

**Conclusion:** the published text is the Zenodo/local-PDF version. The local `.tex` is **not** its source: it is a divergent edit. The table below audits the **Zenodo version**, with numbering from the Zenodo PDF. Where the local `.tex` differs materially, this is noted.

### Zenodo landing-page description (record 22866175): claims the body does not support

1. **"Formal Verification (Lean 4 & Mathlib 4): Complete, machine-checked interactive proofs across 9 formal modules … 0 sorry, 0 admit, 0 unproven axioms".**
   - The latest record contains no Lean files.
   - The zip from record 22699282 (`audit/scripts/lean_zip/`) has these problems:
     - `lakefile.lean` has **no Mathlib dependency**.
     - `Main.lean` imports a non-existent module, `BTS3`.
     - `BTS/Volume2_GeometricMeasures.lean` works with `Nat`/`Int` toys. Examples:
       - `wasserstein_distance_sq (cost:Int) := if cost ≥ 0 then cost else 0`;
       - `log_sobolev_constant K := 2 / K`;
       - `willmore_energy_checkerboard k := k*k`.
     - Hypotheses are restated as conclusions. `bottleneck_stability_theorem (h_stability : dB ≤ dist_infty) : dB ≤ dist_infty := h_stability`. `quantized_cyclic_cocycle_degree` proves `∃ n, c*deg = c*n` with `n := deg`.
     - `critical_besov_regularity_exponent` asserts s* ≤ 1/2. This contradicts the body, where s* = 1 for steps under the p = 1 definition.
   - **None of these files formalizes any statement of the paper.** By rule 5, nothing counts.
2. **"Exhaustive empirical test batteries verifying all scaling laws …".** No scripts are in the record, and the body reports no numerics.
3. **"Riemannian, symplectic … geometry" for Vol. II.** There is no symplectic content in Vol. II.
4. **"Quantized cyclic cocycles via Connes' Dixmier trace".** False: see A4.
5. **"Faithful Quantum Fisher Information (QFI) volume".** False: see A5.
6. **"Reilly–Bochner boundary formulas on convex exhaustions".** This is only a sketch, and it misapplies a citation: see M2.
7. **"Uniform Bakry–Émery Ricci curvature lower bounds Ric∞(M) ≥ K".** This is a hypothesis, not a result.

## 1. Item table (Zenodo numbering)

| Item | Statement (1 line) | Honest label? | Verdict | Evidence |
|---|---|---|---|---|
| Def 2.1 + kernel family (2.3) | Φ(A) ≥ 0, ∫Φ(A) = Tr A = 1; Φ_kernel(A) = ψᵀAψ with "Σ∫ψᵢ² = 1 and ∫ψᵢψⱼ = δᵢⱼ" | — | **PROBLEMA (M3)** | Orthonormality gives Σ∫ψᵢ² = n, not 1, for n ≥ 2. "Partition of unity" plus orthonormal is also inconsistent. ∫Φ = Tr A does follow from orthonormality alone. |
| Def 2.2 | W₂ between μ_A and μ_B for matrices of different sizes | ok | CONFIRMA | Standard pull-back. It depends on the choice of ψ per dimension, which is not discussed (B). |
| Thm 2.3(a) | W₂ is a pseudometric on ⋃ₙ S₊ⁿ; it is a metric on classes | ok | CONFIRMA | Pull-back of a metric. The "gauge equivalence" quotient is just "same realization", so the claim is tautological. |
| Thm 2.3(b) | W₂ ≤ diam/√2 · ‖Φ(A) − Φ(B)‖₁^{1/2}, sharp | ok | CONFIRMA | `num_w2_be.out.txt`: random pairs give max ratio 0.89. Near-extremal pairs give ratio 0.997 (sharp). The mutated constant diam/2 is violated (negative control). |
| Thm 2.3(c) | Metric speed ≤ C‖Ȧ‖_F under Φ ≥ c₀ | Theorem; proof incomplete | **PROBLEMA (M1)** | The proof uses "Φ smooth with bounded derivatives", which is not a hypothesis. The step ‖∂τρ‖_{L¹} ≤ C‖Ȧ‖ ⇒ ‖∂τρ‖_{H⁻¹} ≤ C₃‖Ȧ‖ is invalid: L¹ does not embed in H⁻¹ for d ≥ 2. The bound holds if Φ is C¹ into L² (e.g. Φ_kernel), via Peyre's inequality W₂ ≤ c₀^{-1/2}‖·‖_{Ḣ⁻¹}, but the paper neither states nor cites this. "Projected gradient flow" is irrelevant. |
| Def 2.4 | Ric∞ = −∇² log Φ, κ_BE = inf of its spectrum | ok | CONFIRMA | The identity −∇² log Φ = −∇²Φ/Φ + ∇Φ⊗∇Φ/Φ² is correct. |
| Thm 2.5(a–c) | κ_BE ≥ K > 0 on convex [0,1]^d ⇒ K-displacement convexity, LSI with 2/K, Var decay e^{−2Kτ} | Labeled as theorem proved here; really a cited classical result | **PROBLEMA (M2)** in the proof; statements CONFIRMA | The statements are classical: Bakry–Émery, and McCann/Otto–Villani on convex sets. Proof defects: (i) von Renesse–Sturm (CPAM 58, 2005) treat smooth Riemannian manifolds, **unweighted and without boundary**, so the cited equivalence is outside its hypotheses. (ii) A pointwise Γ₂ ≥ KΓ cannot be deduced from an integrated Reilly identity. (iii) The Zenodo "convex exhaustion … edge contributions vanish for H² Neumann eigenfunctions" is an unproved assertion. Numerical check: the Neumann gap of the truncated Gaussian is ≥ a for a = 2, 10, 50, and the negative control (a double well) passes (`num_w2_be.out.txt`). Also, "contracts to the uniform state" is wrong: the limit is the constant ∫u dμ_A (B). |
| Ex 2.6 | Truncated Gaussian: κ_BE = λ_min(A) | ok | CONFIRMA | ∇²V = A is constant. Note κ_BE ≤ Tr A/n = 1/n under the normalization. |
| Def 3.1 + structure theorem | Super-level persistence; decomposition into intervals | Cited | CONFIRMA (B) | For tame/q-tame modules the decomposition is due to Crawley-Boevey and Chazal et al., not Edelsbrunner–Harer. |
| Thm 3.2 | d_B ≤ ‖Φ(A) − Φ(B)‖_∞ ≤ L_Φ‖A − B‖_F for tame continuous realizations | Labeled theorem; it is a classical result | CONFIRMA (B) | The interleaving X_{t+ε}(f) ⊆ X_t(g) ⊆ X_{t−ε}(f) is correct, and so is the algebraic stability theorem (Chazal et al. 2016, DOI resolved). The original result, Cohen-Steiner–Edelsbrunner–Harer, DCG 37 (2007) 103–120 (10.1007/s00454-006-1276-5), is not cited. |
| Def 3.3 | Persistent entropy E = −Σpᵢ log pᵢ, set to 0 for an empty diagram | ok | CONFIRMA | — |
| **Thm 3.4**: diagram part | An isospectral pair A = PBPᵀ (3×3) with Dgm₁(A) = ∅ ≠ {(2,0)} ⊂ Dgm₁(B) | Labeled theorem | CONFIRMA (trivial) | Spectrum {2±2√3, 0} and ‖·‖_F² = 32 are confirmed. β₁(X_t(B)) = 1 and β₁(X_t(A)) = 0 for t ∈ (0,2] on a 300² pixel grid; negative control with 2 holes gives β₁ = 2 (`num_isospectral_persistence.out.txt`). The separation is trivial: the realization is not permutation-invariant by construction. |
| **Thm 3.4**: entropy part | Zenodo: "for N_k ≥ 2 distinct lifetimes, entropies strictly differ" plus the closing paragraph. Local `.tex`: "E⁽¹⁾(A) ≠ E⁽¹⁾(B)" | Theorem; false | **PROBLEMA (A1)** | (i) In the paper's own example, E⁽¹⁾(A) = E⁽¹⁾(B) = 0 (one bar against none). In the local `.tex` the theorem's second claim is therefore **false**. (ii) The proposed fix "ring heights (2, 2.2, 2.4) give multiple bars" is false: N₁ = 1 for those heights and for all 200 random symmetric 3×3 matrices with a low centre (the max bar count is 1). (iii) The general Zenodo claim, that N_k ≥ 2 forces different entropies, is false: two realizations with the same multiset of lifetimes, e.g. any A and a translate of its pattern inside a larger grid, have equal entropy. (iv) The abstract and Table 1 claim "persistent entropy … strictly separates isospectral matrices": unsupported. |
| Thm 3.4 proof: smoothing | "‖Φ_ε − Φ‖_∞ → 0 for mollified step realizations", so the result holds "uniformly in smooth categories" | — | **PROBLEMA (M4)** | False: the sup error stays ≈ 1.4–1.5 for ε = 0.05…0.005 (`num_isospectral_persistence.out.txt`). Thm 3.2 assumes continuity and does not apply to step functions. The diagram separation still holds numerically for the mollified pair (β₁: B = 1, A = 0), but the given argument is invalid. |
| Def 4.1 | H = −div(∇Φ/\|∇Φ\|) expansion | ok | CONFIRMA | The algebra is correct. Note H = κ₁+κ₂, the sum of principal curvatures, not their mean. Sard's theorem for f: ℝ^d → ℝ needs C^d, not C²; for d = 3 this means C³ (B). |
| Def 4.2 | W = ∫∫_{Σ_t} H² = ∫H²\|∇Φ\| | ok | CONFIRMA | Coarea formula. |
| Rem 4.3 | The integrand ~1/r near a nondegenerate critical point; finite iff d ≥ 2; "log divergence for d = 1" | Remark | PROBLEMA (B) | The d ≥ 2 part is correct. For d = 1, H = −(Φ′/\|Φ′\|)′ = 0 a.e., so the integral is 0, not divergent. |
| Thm 4.4(a) | ∫(H² − K)dA is conformally invariant for closed level surfaces | Classical (Willmore/White/Chen) | CONFIRMA with B | With the paper's H = κ₁+κ₂, the pointwise identity \|Å\|² = 2(H²−K) used in the proof is **false**; it holds for the mean curvature. The integral is still invariant for closed surfaces: ∫(κ₁+κ₂)² − ∫K = 4∫(H_m² − K) + 3·2πχ, by Gauss–Bonnet. |
| Thm 4.4(b) | Checkerboard: ε = 1/k gives Dirichlet Θ(1) and W = Θ(k²); fixed ε gives W = Θ(k³) | Theorem about matrices | **PROBLEMA (M5)**; scaling CONFIRMA | The scaling W = Θ(εk³) for Φ = ε sin(kx₁) sin(kx₂) is confirmed by direct quadrature for k = 8…64: W/(εk³) ≈ 1.05 ± 5%, W/(εk²) grows like k, Dirichlet energy = 0.5 (`num_willmore_scaling.out.txt`). But the realization A_k ↦ Φ(A_k) is never defined: the "matrix" theorem is proved for a chosen sine profile. For the step realization of a checkerboard, W is undefined. |
| Def 4.5 + Cheeger claim | Isoperimetric profile and Cheeger constant; λ₁(−Δ_A) ≥ h²/4 | Cited | CONFIRMA (B) | This is Cheeger's inequality (1970), not "Cheeger–Federer". The perimeter must be relative to int Ω for the Neumann problem. "Spectral bottleneck in the matrix graph": there is no graph here. |
| Def 5.1 | Gabor transform with "g ∈ C_c^∞ … Gaussian" | — | PROBLEMA (B) | A Gaussian is not compactly supported. The extension of Φ outside Ω is unspecified. |
| **Def 5.2 + Thm 5.3** | WF(Φ(A)) = N*(Γ) for a jump across a smooth interface Γ, with WF defined by rapid decay of V(x,ξ) for a **fixed Gaussian window** | Theorem; false | **PROBLEMA (A2)** | With a fixed, non-compact window of fixed width, V(x₀,ξ) at any x₀ off Γ still sees the jump through the Gaussian tail. Numerically \|ξ\|·\|V(x₀,ξ)\| → g(−x₀) ≠ 0 at 5σ from the jump: polynomial, not rapid, decay. Under the paper's definition, (x₀, ±n) ∈ WF although x₀ ∉ Γ. Closed form (erfc) and mpmath quadrature agree. Negative controls: smooth f decays super-polynomially, and a compactly supported window (Hörmander's definition) decays rapidly (`num_wavefront_gabor.out.txt`). The proof's "integration by parts ⇒ rapid decay for x ∉ Γ" is false. The curved-Γ case (stationary phase) is not done. Grid realizations have corners, where WF contains all directions. |
| Def 5.4 + claims | s* = sup{s: [Φ]_{B^s_{1,∞}} < ∞}; "steps: s* = 1/p (in L^p)"; "fractal: s* = d − d_fractal (conjecture)" | Partly a conjecture | **PROBLEMA (M6)** | The definition fixes p = 1, so every step realization has s* = 1, the same as a smooth one: the invariant cannot separate them. "s* = 1/p" refers to a different invariant. With first differences, B¹_{1,∞} equals BV only in that sense. The "conjecture" for indicators of sets with box dimension D, s* = d − D for p = 1, is essentially known (Minkowski content / Sickel), so the label is not honest in that direction. The Lean file claims s* ≤ 1/2, which contradicts this. |
| Spectral triple (6.1) | (A_Φ, L²(T^d, S), D) | — | PROBLEMA (B) | D has a kernel on T^d (constant spinors, trivial spin structure), so \|D\|^{−d} must be defined on ker D^⊥. The APS remark is unsupported. |
| **Def 6.1 vs Thm 6.2** | Tr_ω(Φ\|D\|^{−d}) := lim (1/log N) Σ μₙ (singular values) = 2^{⌊d/2⌋}Ω_d/(d(2π)^d) ∫Φ | Theorem (Connes trace theorem) | **PROBLEMA (A3)** for sign-changing Φ; CONFIRMA for Φ ≥ 0 | The constant is verified: d = 2 gives slope 0.15915 = 1/(2π), d = 1 gives 1/π, and the mutated constants fail. But the definition uses **singular values**, so it computes c∫\|Φ\|, not c∫Φ. For f = cos 2πx: numerics give 0.2017 ≈ 2/π² against the theorem's 0. For f = 0.3 + cos: 0.2108 ≈ (1/π)∫\|f\| against 0.0955 (`num_dixmier.out.txt`). Φ(A) = ψᵀAψ with A an arbitrary real matrix changes sign, so the theorem as stated is false. (The script exits with code 1 only because numpy's int type is passed to sys.exit; it records failures = 0.) |
| **Thm 6.3 (Zenodo) / §6.3 sentence (local `.tex`)** | τ_d(A₀…A_d) = Tr_ω(Φ₀[D,Φ₁]…[D,Φ_d]\|D\|^{−d}) = c_d·deg(F_A) ∈ c_d ℤ, homotopy-invariant | Theorem; false | **PROBLEMA (A4)** | In even d (the abstract's "τ_{2k}"), tr_S(γ^{μ₁}…γ^{μ_d}) has no ε-part without the grading γ. For d = 2, tr(γ^μγ^ν) = 2δ^{μν}, so τ₂ = −(1/2π)∫Φ₀∇Φ₁·∇Φ₂, which is not topological. Numerics: a degree-1 map T²→S² composed with 5 rotations of S² keeps degree 1.0000 while τ₂ ranges over −0.018 … +0.021, stable under refinement N = 256/512/1024. Positive control: ∫F⁰dF¹∧dF² = (4π/3)·deg holds. Negative control: a constant map gives 0 (`num_cocycle_d2.out.txt`). Even in odd d, the constant in (6.7) lacks the factor 1/(d+1) and the Clifford phase. Connes' degree formula needs the grading and the antisymmetrized cocycle. Local `.tex` miscount: "tuple of d matrices (A₀,…,A_d)" (B). |
| Def 7.1 | Vol_QFI = ∫√det g^QFI | ok | CONFIRMA | — |
| Eq. (7.6)–(7.7) | g_μν = Σ Re(⟨i\|∂_μρ\|j⟩⟨j\|∂_νρ\|i⟩)/(λᵢ+λⱼ), with the inequality g_μμ ≥ ½‖∂ρ‖² | — | **PROBLEMA (M7)** | For g = ½Tr(ρ{L_μ,L_ν}), the correct value is **2**Σ…/(λᵢ+λⱼ). Two independent oracles agree with each other and with the factor 2: a Sylvester-equation SLD and the Bures root-fidelity expansion. The paper's formula is exactly half in 5 random trials (`num_qfi.out.txt`). The inequality survives, being even weaker than the truth. |
| Thm 7.2(a), (c) | Vol ≥ 0; invariant under Diff(Ω) | ok | CONFIRMA | g is a Gram/pull-back 2-tensor. |
| **Thm 7.2(b)** | Vol = 0 ⇔ ρ spatially constant **modulo unitary gauge U(x)** ("trivial unentangled product state") | Theorem; false | **PROBLEMA (A5)** | (i) A gauge orbit ρ(x) = U(x)ρ₀U(x)† has det g = 18.5 > 0, so "constant mod gauge ⇒ Vol = 0" is false. This example satisfies every Zenodo hypothesis: positive definite, with linearly independent ∂_μρ. (ii) Local `.tex` (no independence hypothesis): ρ = diag(½ ± ¼ sin x₁) in d = 2 gives det g ≡ 0 with ρ non-constant, so "Vol = 0 ⇒ constant" is false (`num_qfi.out.txt`). (iii) In the Zenodo version, the added hypothesis of linear independence at every x forces det g > 0 everywhere, so "Vol = 0" never occurs and the "only if" is vacuous. (iv) Nothing links Vol_QFI = 0 to "unentangled". |
| Rem 7.3 | QFI discontinuous at rank change (Šafránek) | Cited | CONFIRMA | PRA 95, 052320 (Zenodo) resolves correctly. The local `.tex` has 062320, which is a different paper (B). |
| Def 7.4 | Entanglement contour S_vN(ρ(x))·√det g, centroid | Definition | CONFIRMA (B) | The name collides with the established "entanglement contour" of Chen–Vidal (2014). The applications claim "detect spatial spreading at criticality" is unsupported. |
| Abstract | "We prove rigorous existence, stability, and invariance theorems for each construction, providing an exhaustive classification"; persistent entropy "strictly separates isospectral matrices"; "quantized topological cyclic cocycles τ_{2k}" | — | **PROBLEMA (M8 plus A1/A4)** | There are no existence theorems and no classification. The entropy and quantization claims are false (A1, A4). The WF claim rests on A2. |
| Introduction | "Classical matrix algebra possesses no natural, canonical metric" for matrices of different sizes | — | PROBLEMA (B) | Cut distance/graphons and Gromov–Wasserstein exist, and Vol. I itself uses cut norms. |
| §8 table and applications | "Geodesic distance between matrices"; "preventing … adversarial vulnerability"; QFI "detect … at criticality" | — | PROBLEMA (B) | W₂ is a pseudometric pulled back to matrices: there are no geodesics within the matrix space. The application claims are not supported by any result in the body. |
| Conclusion | "These invariants resolve fundamental open problems in dimensional incommensurability, isospectral ambiguity, … entanglement localization" | — | **PROBLEMA (M8)** | Overclaim. |
| Bibliography | 14 entries | — | PROBLEMA (B) | Crossref (`crossref_check.out.txt`; a mutated DOI gives 404 as negative control): (i) **Benamou–Brenier DOI 10.1007/s002110050475 resolves to Bey, "Simplicial grid refinement"**; the correct DOI is 10.1007/s002110050002. (ii) von Renesse–Sturm's title omits "entropy" ("…gradient estimates, entropy and Ricci curvature"). (iii) The local `.tex` Šafránek number 062320 is wrong. (iv) Cohen-Steiner–Edelsbrunner–Harer 2007 is missing. The other DOIs resolve and match. |
| Lean / formal claims | The body claims only future work. The landing page claims complete Lean+Mathlib proofs | — | **PROBLEMA (A6)** | See §0: no Mathlib, Nat/Int toys, hypotheses as conclusions, Main imports a missing module. Nothing counts. |
| Source management | The local `.tex` is not the source of the published PDF | — | **PROBLEMA (M9)** | See §0. Any correction must start from a reconciled source. |

## 2. Summary by severity

**A: mathematical error or false claim (6)**
- **A1.** Thm 3.4 / abstract: persistent entropy does **not** separate the exhibited isospectral pair (E = 0 for both). The "multiple bars" fix is false (N₁ ≤ 1). The general "N_k ≥ 2 ⇒ different entropies" claim is false.
- **A2.** Thm 5.3: under Def 5.2 (fixed Gaussian window) the "wavefront set" is not localized, and the theorem is false. Points off Γ have only 1/|ξ| decay.
- **A3.** Thm 6.2 vs Def 6.1: the singular-value definition yields c∫|Φ|, so the formula c∫Φ is false for sign-changing Φ(A). Numerics: 0.2017 against 0.
- **A4.** Thm 6.3 (and §6.3 in the local `.tex`): τ_d is not quantized and not homotopy-invariant. In even d, τ₂ = −(1/2π)∫Φ₀∇Φ₁·∇Φ₂, which changes under rotations of the target at fixed degree.
- **A5.** Thm 7.2(b): "Vol = 0 ⇔ constant modulo gauge" is false; the gauge orbit has Vol > 0. The local version's "only if" is refuted by the x₁-only counterexample, and the Zenodo version's "only if" is vacuous.
- **A6.** The Zenodo description's Lean claim ("complete machine-checked … 0 sorry") is false. The files are Mathlib-free placeholders, and the latest record contains none.

**M: gap or wrong label (9)**
- **M1.** Thm 2.3(c): unstated regularity hypothesis and an invalid L¹ → H⁻¹ step.
- **M2.** Thm 2.5: the statements are true (classical), but the proof misapplies von Renesse–Sturm (no weight, no boundary) and makes an invalid integrated-to-pointwise step. It should be labeled as a cited classical result.
- **M3.** Kernel realization: Σ∫ψᵢ² = 1 contradicts orthonormality.
- **M4.** Thm 3.4 proof: the mollifier L∞-convergence claim is false, and Thm 3.2 is applied to discontinuous functions.
- **M5.** Thm 4.4(b): the realization Φ(A_k) is never defined. The scaling is confirmed only for the chosen sine profile.
- **M6.** s*(A): degenerate for p = 1 (steps and smooth functions both give 1). Inconsistent "1/p" statement. The "conjecture" is essentially known.
- **M7.** QFI formula (7.6)/(7.7) is off by a factor 2.
- **M8.** The abstract and conclusion overclaim: "existence … theorems for each construction", "exhaustive classification", "resolve fundamental open problems".
- **M9.** The local `.tex` diverges from the published text.

**B: wording or citation (≈12)**
- Willmore H convention: pointwise identity wrong, integral still invariant.
- Sard needs C^d.
- Rem 4.3's d = 1 claim is wrong.
- Gaussian ∉ C_c^∞.
- Kernel of D on T^d.
- "Cheeger–Federer" misnomer and relative perimeter.
- "Uniform state".
- Structure-theorem attribution.
- Missing CSEH 2007.
- Benamou–Brenier DOI wrong.
- vR–S title incomplete.
- Local `.tex` Šafránek number and "d matrices" miscount.
- Name clash for the entanglement contour.
- Intro and applications overclaims.

**Confirmed (CONFIRMA):**
- Thm 2.3(a), (b) (sharp constant checked).
- Def 2.4.
- Thm 2.5 statements (as classical results).
- Ex 2.6.
- Thm 3.2.
- Thm 3.4 diagram part (trivial).
- Defs 4.1, 4.2.
- Thm 4.4(a) integral form.
- Thm 4.4(b) scaling for the sine profile.
- Thm 6.2 for Φ ≥ 0 (constant checked).
- Thm 7.2(a), (c).
- Rem 7.3.

## 3. Closing notes (prova-rigorosa)

- **Hardest step:** A4. The Clifford-trace argument depends on the spinor representation and on the grading. The numerical test covers d = 2 only, and the odd-d constant was checked by hand.
- **What would falsify these verdicts:**
  - For A2: a reading of Def 5.2 with a window that shrinks with |ξ|. That is not what the text says.
  - For A3: restricting to Φ(A) ≥ 0. Not stated for Thm 6.2: Def 6.1 takes A ∈ ℝ^{n×n} arbitrary.
- **Not checked:**
  - The curved-interface case of Thm 5.3.
  - Odd-d numerics for Thm 6.3.
  - Vol. I statements: none is cited by theorem number.
- **Literature consulted:** all DOIs resolved via Crossref (`crossref_check.out.txt`). Bottleneck stability: Cohen-Steiner–Edelsbrunner–Harer, 10.1007/s00454-006-1276-5. Algebraic stability: Chazal–de Silva–Glisse–Oudot, 10.1007/978-3-319-42545-0. Ricci and transport: von Renesse–Sturm, 10.1002/cpa.20060. Šafránek, 10.1103/PhysRevA.95.052320.
