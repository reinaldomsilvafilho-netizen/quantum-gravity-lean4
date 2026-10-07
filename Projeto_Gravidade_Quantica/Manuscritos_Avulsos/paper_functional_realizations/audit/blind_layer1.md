# Blind referee report, layer 1: *Beyond the Spectrum*, Vol. I (Functional Realizations)

Referee: independent subagent (Claude Opus), blind (I did not read the ledgers, WORKPLAN, CHANGELOG, CLAUDE_*/AUDIT_*/ADVERSARIAL_* files, or the sandbox). Date: 2026-10-06. Protocol: `unified_quantum_gravity_book/audit/verify/PROTOCOL.md`, Layer 1.

## 0. Version check

| Object | Identity | Volume I text |
|---|---|---|
| Zenodo 22644744 (v1, 2026-09-07) | Vol I PDF 690 794 B. Author shown as "M. A. R. Turing and Collaborators". | **Same text as the local `.tex`.** The word-set diff contains only LaTeX markup and PDF artefacts (`scripts/compare_tex_old.out.txt`). |
| Zenodo 22699282 (v2, 2026-09-11) | Vol I PDF 706 670 B, sha256 f6d7a671… | **Byte-identical to the local `beyond_the_spectrum_files/volume_1_functional_realizations.pdf` (2026-09-10).** |
| **Zenodo 22866175 (latest, 2026-09-21)** | Holds only `beyond_the_spectrum_trilogy.pdf` (1 391 818 B, sha256 a2eab2a0…). It is byte-identical to the local `beyond_the_spectrum_trilogy_updated.pdf`. Vol I occupies trilogy pages 8–25 and was extracted to `audit/zenodo_latest_vol1.pdf`. | Same text as v2. The only diff is the running head "Beyond the Spectrum: Complete Trilogy" (`scripts/compare_versions.out.txt`, ratio 0.9994). |

**Conclusion.** Zenodo latest Vol I = local PDF (2026-09-10) ≠ local `.tex`. The `.tex` carries the 2026-09-22 timestamp, but its text is the **older** v1 text.

Differences between the `.tex` and Zenodo latest:
1. Author and affiliation: the `.tex` has "M. A. R. Turing"; Zenodo has R. M. Silva-Filho, PPGEE/DES UFLA.
2. Theorem 5.5 (`.tex`) / 5.6 (Zenodo), critical scaling, is rewritten:
   - normalization d^{-(k-1)/2} becomes d^{-1/2};
   - a sub-Gaussian hypothesis is added;
   - a Dudley-entropy proof and a matching lower bound are added;
   - a Ginibre remark is added;
   - refs [9] Tomioka–Suzuki and [10] Nguyen–Drineas–Tran are added.
3. Kac–Rice proof: "see" becomes "after".
4. DOIs and ISBNs are added to the bibliography.

**This report audits the Zenodo latest text.** Where the `.tex` differs, the item says so.

The Lean zip `formal_proofs_bts.zip` is in v1 and v2, not in the latest record. Locally, `formal_proofs_bts/` holds only `.lake` build artefacts and no sources. I audited the v2 zip.

## 1. Item table

| Item | Statement (1 line) | Honest label? | Verdict | Evidence |
|---|---|---|---|---|
| Def 2.1 | Φ: T^k → F(Ω), a map from tensors to functions | — | CONFIRMA | Pure definition. |
| Def 2.2 | Linearity, faithfulness, boundedness, equivariance | — | PROBLEMA (B) | (ii) "ker Φ = {0}" is meaningless for nonlinear Φ. "Vanishes as a continuous function" is wrong for L^p or measure targets. |
| Constr 3.1–3.2 | f_A = xᵀAx; f_T = T(x,…,x) on S^{n-1} | — | CONFIRMA | |
| Prop 3.3 | Extrema of f_A on the sphere are λ₁ and λ_n; critical points are unit eigenvectors | Classical (Rayleigh–Ritz), no citation | CONFIRMA; label B | The Lagrange step is valid because ∇(xᵀx) = 2x ≠ 0. It is called "Euler–Lagrange", which is a misnomer. With repeated eigenvalues the claim still holds: the critical points are all unit vectors of the eigenspace. |
| Constr 3.4 | Step graphon W_A on a partition into I_i | — | CONFIRMA | |
| Constr 3.5 | Voxel field; "f_A ∉ C⁰" | — | PROBLEMA (B) | False for constant A, where f_A is constant. h_α is never defined. |
| Constr 3.6 | Polyhedral indicator = ∏Θ(b_i − ⟨a_i,x⟩) | — | CONFIRMA | |
| **Constr 3.7** | Harmonic realization f_A = (1/n)Σa e^{i k·x}; "‖f_A‖_{L²(T²)} = ‖A‖_F" | Stated as fact | **PROBLEMA (A)** | With Lebesgue measure on [0,2π)², ‖f_A‖² = (2π/n)²‖A‖_F². The oracle (grid quadrature) matches the corrected value 29.0828; the paper's value is 18.4169 (`check_harmonic.out.txt`). With normalized measure it is ‖A‖_F/n. The identity is false in every normalization for n > 1. |
| Constr 3.8 | Tensor-product B-splines; "C^{p-1} regularity" | — | PROBLEMA (B) | Indices run 0..m against P ∈ R^{m×n×3}, an off-by-one. C^{p-1} needs simple knots. |
| Constr 3.9 | T_A has ‖T_A‖_HS = ‖A‖_F / n | — | CONFIRMA | ‖W_A‖²_{L²} = Σa²/n². |
| **Thm 4.1** | E(f_A) = Σ(k₁²+k₂²)\|a\|². "Consequently" there exist permutations with energy ratio Θ(n²) | Theorem | **PROBLEMA (A)** | (1) The formula misses the factor (2π/n)². A finite-difference oracle converges at order 2.0 to the corrected value 682.72; the paper's formula gives 432.34. (2) Read with its quantifier ("Let A ≠ 0 … Consequently there exist P₁, P₂"), the ratio claim is false: for A = I_n or J_n, every one of the 720 permutations (n = 6) gives ratio 1. The proof covers only A = E₁₁. (3) Θ(n²) at fixed n has no meaning. (4) The energy is the matrix-algebra quantity c(‖DA‖²_F + ‖AD‖²_F) with D = diag(1..n), checked numerically. This contradicts the claim that it is "unreachable by matrix algebra". |
| **Ex 4.2** | Checkerboard: mass at (n,n), E = Θ(n³), "maximally rough" | Example | **PROBLEMA (A)** | Every \|a_{k}\| = 1, so the mass is spread over all (k₁,k₂). In the paper's normalization E = 2n·n(n+1)(2n+1)/6 = Θ(n⁴), and E/n⁴ → 2/3. In the true normalization E = Θ(n²). It is never n³. The all-ones matrix J has **identical** energy, so the harmonic energy cannot detect sign oscillation (`check_harmonic.out.txt`). |
| Def 4.3 | TV(f) by duality | — | CONFIRMA | |
| Thm 4.4 | TV(W_A) = (1/n)Σ\|vertical jumps\| + (1/n)Σ\|horizontal jumps\| | Theorem | CONFIRMA (proof sketchy, B) | Signs and interfaces are correct. The sign-saturation step needs continuous φ near the grid crossings; it is standard but not written out. Mollification oracle: the error halves when ε halves (order 1) and tends to the formula's value 11.75. The no-1/n mutant fails. |
| Thm 4.5 | Coarea: TV(W_A) = ∫H¹(∂*E_t)dt | Cited (Evans–Gariepy) | CONFIRMA; B | The coarea formula for BV is Fleming–Rishel / Federer, not "De Giorgi's structure theorem". The statement says "any t" while the proof says "a.e. t"; here every t works because E_t is a finite union of cells. |
| Thm 4.6 | Distinct eigenvalues: 2n critical points ±v_i, index i−1, P_{−1} = 1−(−1)^n = χ(S^{n−1}) | Theorem (classical, uncited) | CONFIRMA; label B | The Hessian 2uᵀAu − 2λ_i\|u\|² is correct. A finite-difference Hessian in exponential charts reproduces indices 0,0,1,1,… for n = 2,3,5,6. n = 1 checked. The abstract's "handlebody decompositions" appear nowhere in the body. |
| Rem 4.7 | Repeated eigenvalue (multiplicity m+1) gives a Morse–Bott S^m | — | CONFIRMA | |
| Def 4.8 | Cut norm | — | CONFIRMA | |
| Thm 4.9 | ‖W‖_□ ≤ ‖T_W‖_{∞→1} ≤ 4‖W‖_□ | Theorem (classical, Lovász book §8.2) | CONFIRMA; proof gap B | The step "∫W u₊v₊ ≤ ‖W‖_□ for [0,1]-valued u₊, v₊" (extreme points are indicators) is not stated. "Grothendieck" in the title is never used. Brute force over 300 random 7×7 step kernels: ratio ≤ 2.96. The 2×2 checkerboard attains 4, so the constant is sharp and a mutant bound of 2 fails. |
| Thm 4.10 | (W̃, δ_□) is compact; every bounded-entry matrix sequence has a subsequence converging to a "continuous limit graphon" | Cited | PROBLEMA (M) | 1. Compactness is Lovász–Szegedy, GAFA 17 (2007) 252, DOI 10.1007/s00039-007-0599-6, not the cited JCTB 2006 paper. 2. The quotient must be taken by weak isomorphism (δ_□ = 0), not by the orbits of Π̄. 3. "Bounded entries" needs symmetric matrices affinely rescaled to [0,1]. 4. The limit is measurable, not "continuous". |
| Ex 4.11 | ‖W_{I_n}‖_□ = 1/n → 0 | — | CONFIRMA | Brute force n = 4, 8, 12. |
| §5 intro | Tensor rank is NP-hard ("Hillar and Lim [5]"); low-rank sets are not closed | Cited | PROBLEMA (B) | [5] is Lim 2005, a CAMSAP paper. The right sources are Hillar–Lim, J. ACM 60 (2013), DOI 10.1145/2512329, and De Silva–Lim, SIMAX 30 (2008), DOI 10.1137/06066518X. Neither is in the bibliography. |
| Thm 5.1 | σ_max is attained on ∏S^{dα−1}; critical points satisfy the Lim equations with a common σ | Theorem (= Lim 2005) | CONFIRMA (math); label B | The proof is correct: μ_α = Φ for every α. "Strictly attained" is meaningless. The claim "eliminating … scale divergences" is only valid for rank 1 (see §6.4 below). |
| Def 5.2 | k-hypergraphon and the box cut norm ‖·‖_{□,k} | — | CONFIRMA | |
| Thm 5.3 | (i) ‖W‖ ≤ ‖T_W‖ ≤ 2^k‖W‖; (ii) (W̃_k, δ_{□,k}) is compact | Theorem; (ii) cited to "Gowers" via the Lovász book | (i) CONFIRMA; (ii) PROBLEMA (M) | (i) Same argument as Thm 4.9, same B gap. Calling it "L∞→L¹" is a misnomer for a k-linear form. (ii) No proof is given. Gowers' strong hypergraph regularity is not the relevant tool: for the weak box norm, Frieze–Kannan weak regularity plus the Lovász–Szegedy martingale argument would be. The statement is plausible, but the source is not identified. "Every bounded tensor sequence" needs symmetric tensors rescaled to [0,1]. |
| Thm 5.4 | Penalty R = Σ∫(\|∇f\|² + λ\|Δf\|²) gives sup\|f\| ≤ C√R and "suppresses hallucination" | Theorem | PROBLEMA (M) | It needs λ > 0 and C = C(λ). For λ = 0, H¹ ⊄ L^∞ in 2D: sup\|f\|/‖∇f‖ grows like √log N (0.26, 0.34, 0.42, 0.48 at N = 8…512). For softmax slices the bound is vacuous, because \|f\| ≤ (1/N)Σ\|a\| = 1 always holds. "Morrey's inequality" is a misnomer. The hallucination claim is unsupported. |
| **Thm 5.5** | Random symmetric Gaussian tensor: E\|Crit f_T\| ∼ C(d) exp(nΘ(d)) | Theorem "via Kac–Rice (after ABC)" | **PROBLEMA (A)** | ABC (CPAM 66, 2013), Remark 2.9 / eq. (2.20), proves only lim (1/N) log E Crt_N(R) = ½ log(p−1). The exponent is Θ(log d), not Θ(d), and ABC give no prefactor C(d). At d = 2 the paper's own Thm 4.6 gives exactly 2n critical points, not exponentially many. Hypothesis mismatch: ABC use iid couplings over all ordered index tuples, which make the field isotropic. A symmetric tensor with iid entries per multiset is **not** isotropic, so the cited formula does not apply as stated. |
| Thm 5.6 (Zenodo) | (i) d^{-1/2} is the unique scaling with E sup = Θ(1); (ii) P(\|f̂\| > ε) ≤ 2e^{−c_k d ε²} for Haar u | Theorem | CONFIRMA (statements); proof gaps (M) | (i) HOPM lower bounds give sup/√d ≈ 2.51, 2.64, 2.76, 2.78 for d = 8…64 (Tomioka–Suzuki ~√(kd log k)). The increment bound (5.19) holds only for u, u′ differing in one block; in general the Lipschitz constant is √k, which changes constants only. (ii) The statement is true and simpler than claimed: given u, X is sub-Gaussian with proxy 1, and for Gaussian T it is exactly N(0,1/d). Empirical tails lie below 2e^{−dε²/2}. The "inductive Herbst" proof is hand-waving. Lévy–Gromov / Bakry–Émery give d−2; the factor (d−1) needs Mueller–Weissler. |
| Thm 5.5 (local `.tex` only) | Normalization d^{-(k-1)/2} gives Θ(1) | Theorem | **PROBLEMA (A), `.tex` only** | For k ≥ 3 the quantity tends to 0: sup/d = 0.89, 0.66, 0.49, 0.35, about d^{−1/2}. Fixed in Zenodo v2 and later. |
| §6.1 | Sobolev loss "guarantees Lipschitz stability without constraining capacity"; zero-shot width scaling "eliminates training cost" | Presented as consequences of Thms 4.1/4.10 | PROBLEMA (M) | Neither claim is proved. Compactness gives only a subsequence of an arbitrary sequence, and says nothing about trained weights or the network's function. Weight matrices are not symmetric [0,1] graphons. |
| §6.2 | Kac–Rice "proves" sublevel shattering below T_c; RSB "corresponds precisely" to β₀(M_E) ≫ 1 | "Rigorous foundation" | PROBLEMA (M) | A heuristic presented as a theorem. The cross-reference "Theorem 5.1 and 5.3" points to the Weierstrass and hypergraphon theorems (B). It inherits the Θ(p) error of Thm 5.5. |
| §6.3 | δ_□ "embeds" networks of any size; time derivatives dW/dt "rigorously defined" | Claimed via Thm 4.9 | PROBLEMA (M) | Thm 4.9 is a norm equivalence. δ_□ is only a pseudometric on graphs (G and its blow-ups are at distance 0), so it is not an embedding. Items (i)–(iii) are unproved. |
| **§6.4 + abstract (4) + Table row 5** | The compact-manifold realization "circumvents the De Silva–Lim pathology … never diverges" | Claimed result | **PROBLEMA (A)** | Thm 5.1 concerns only the best rank-1 approximation (σ_max), and the rank-1 set is already closed. For r ≥ 2 the pathology is unchanged even with unit-sphere factors: for T = a⊗a⊗b + a⊗b⊗a + b⊗a⊗a, ‖T − X_t‖ = 1.73/t with \|λ\| = t → ∞. Optimization with \|λ\| ≤ L gives best errors 7.7e-2, 1.0e-2, 6.3e-4, 3.3e-5 for L = 2, 5, 20, 100: positive, and reaching 0 only as L → ∞ (`check_tensors.out.txt`). The "De Silva and Lim [5]" citation is the wrong paper (B). |
| §6.5 | TV(W_A) equals ∫H¹ dt; hence ROF discrete TV is "a precise minimal-surface formulation" | — | Identity CONFIRMA; inference PROBLEMA (B) | TV(W_A) is the anisotropic \|Δx\| + \|Δy\| sum. The common isotropic ROF discretization differs. "Fractal boundary complexity" is rhetoric. |
| Table 1 | Summary of rows | — | PROBLEMA (B) | Row 5's "De Silva–Lim resolution" is false (see §6.4). |
| Abstract | "Rigorously prove … invariants completely unreachable by pure matrix algebra"; "handlebody decompositions"; five "paradigm-shifting" implications | — | PROBLEMA (M) | The energy and TV are explicit polynomial and absolute-value expressions of the entries (‖DA‖² + ‖AD‖², finite differences), so they are reachable by matrix algebra; they are only non-invariant under permutation. Handlebodies are absent from the body. Implications (1)–(5) are not proved, and (4) is false. |
| Intro (a)–(c) | Permutation invariance; NP-hardness over R and C; border rank | — | CONFIRMA content; B citation | |
| Conclusion | Notions "arise naturally and rigorously"; open problems | — | PROBLEMA (M) | It overstates what was proved, given the A items. The open problems are reasonable; problem 1 is a quadratic-assignment problem. |
| **Formal Verification section** | "Formally verified in Lean 4 (v4.33.1) with zero sorry" | Claim | **PROBLEMA (M; misleading)** | v2 zip: `lakefile.lean` has **no Mathlib dependency** and nothing is imported. Every "theorem" either returns a field of its own hypothesis structure (`exact P.h_amp`, `exact G.h_lower`, `exact M.h_compact`, where `is_sequentially_compact : Bool := true`) or is `rfl` on its own definition (`sphereEulerChar`). The obligation numbers do not match the paper's theorem numbers. **Nothing of the paper is verified.** Only `spectral_critical_correspondence` proves anything, and that is an `omega` fact about two integers. The latest Zenodo record has no zip, and the local folder has no `.lean` sources. |
| References | DOIs resolved | — | OK; B | All 10 DOIs resolve (Crossref/DataCite; fake-DOI negative control returns 404). [6] Qi, [7] ROF and [8] Milnor are never cited in the text. De Silva–Lim 2008, Hillar–Lim 2013 and LS-GAFA 2007 are missing. ABC is CPAM 66 (2013), 165–201, correct (Crossref "issued" 2012 = online). |

## 2. Summary by severity

**A: mathematical error (5 in Zenodo latest, plus 1 only in the `.tex`)**
1. Constr 3.7: ‖f_A‖_{L²} = ‖A‖_F is false; the correct value is (2π/n)‖A‖_F.
2. Thm 4.1: the energy formula misses (2π/n)². The ratio Θ(n²) "for every A ≠ 0" is false (counterexamples I_n, J_n give ratio 1).
3. Ex 4.2: the checkerboard energy is not Θ(n³) and its mass is not at (n,n). It is Θ(n⁴) in the paper's normalization and equals the all-ones energy.
4. Thm 5.5: the Kac–Rice exponent is ½ log(d−1) (ABC eq. 2.20), not Θ(d). At d = 2 the count is 2n, and the symmetric iid model is not isotropic.
5. §6.4, abstract (4), Table 1: the claimed circumvention of the De Silva–Lim ill-posedness is false for rank r ≥ 2 (numerical demonstration).
6. (`.tex` only) Thm 5.5(i): the normalization d^{-(k-1)/2} gives → 0 for k ≥ 3. Fixed in Zenodo.

**M: gap or wrong label (9):** Thm 4.10 hypotheses and citation; Thm 5.3(ii) unproved and misattributed; Thm 5.4 needs λ > 0 and is vacuous for softmax; Thm 5.6 proof gaps; §6.1, §6.2 and §6.3 heuristics stated as proved; abstract and conclusion overclaims ("unreachable by matrix algebra", handlebodies); the Lean claim is misleading (no Mathlib, hypotheses returned as conclusions).

**B: wording or citation (about 12):** Def 2.2(ii); Constr 3.5 and 3.8; Prop 3.3, Thm 4.6 and Thm 5.1 are classical but uncited; Thm 4.4 sketch; Thm 4.5 attribution; Thm 4.9 gap and its "Grothendieck" title; wrong refs for Hillar–Lim and De Silva–Lim; cross-reference "Thm 5.1 and 5.3" in §6.2; uncited refs [6]–[8]; ROF isotropic vs anisotropic; "continuous limit graphon".

**Overlap:** book ch. 1 (`chap01_functional_realizations_matrices_tensors.tex`) is a near-verbatim revision of this volume. The first abstract paragraph, the introduction, Defs 2.1–2.2 and the constructions are identical. This is a self-plagiarism risk: each must cite the other and disclose the reuse.

## 3. Scripts (all exit 0, fixed seeds, outputs in `.out.txt`)

| Script | Purpose |
|---|---|
| `zenodo_versions.py` | List all Zenodo versions of the record. |
| `zenodo_download.py` | Download the PDFs and compare sha256 hashes. |
| `compare_versions.py`, `compare_tex_old.py` | Word-stream and word-set diffs; negative control: an injected mutation is detected. |
| `check_harmonic.py` | Grid and finite-difference oracle, order-2 refinement, paper formulas as negative control. |
| `check_tv_morse_cut.py` | Mollification oracle with order-1 refinement; exponential-chart Hessian; brute-force cut norm; mutants. |
| `check_tensors.py` | HOPM plus an unfolding upper bound; tail Monte Carlo; De Silva–Lim with bounded weights. |
| `check_refs.py` | Crossref/DataCite resolution; fake-DOI negative control. |

No background processes were left running (checked with `processos_orfaos.py`: 0 suspects).
