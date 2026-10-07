# Layer-2 re-check: *Beyond the Spectrum II*, v3 (2026-10-06)

- **Verifier:** independent session (Claude Opus 5.5). It wrote neither the volume, `blind_layer1.md`, the v2 reconstruction nor the v3 corrections.
- **Protocol:** `unified_quantum_gravity_book/audit/verify/PROTOCOL.md`, layer 2, plus the `prova-rigorosa` skill.
- **Inputs:** `blind_layer1.md`, `fixes_layer1.md`, `RECONSTRUCTION_v2.md`, `v2_reconstructed.tex`, the current `.tex`/PDF, `CORRECTIONS_2026-10-06.md`, `ZENODO_DESCRIPTION_VOL2.md`, Zenodo trilogy PDF (record 22866175).
- **New scripts:** each has an independent oracle, a negative control and, where it applies, a refinement study. All exit with code 0.

| Script | What it checks |
|---|---|
| `scripts/L2_reconstruction_check.py` | Reconstruction fidelity. Uses the pypdf extractor (the corrector used PyMuPDF). |
| `scripts/L2_A_checks.py` | Thm 3.6, Prop 6.4, Lemma 7.2 / Thm 7.3, Prop 4.5, Thm 2.3. |
| `scripts/L2_doi_check.py` | Crossref/DataCite lookup of all DOIs. |

- **Build directory:** `audit/L2_build/`.
- **Numbering:** v3 numbers, taken from the `.aux` of the fresh build.

## 1. Reconstruction fidelity: CONFIRMA

- **Overall match:** `v2_reconstructed.tex` was compiled 3× in `L2_build/v2` and compared with trilogy pages 29–46.
  - Words: 7592 against 7594.
  - Ratio **0.99974**, with 1 diff op: the PDF glues "localizewherein".
  - This is independent of the corrector's 0.9997, since a different extractor and tokenizer were used.
- **Spot checks:** these v2-only passages are present in both texts:
  - Thm 6.3 "Quantized Cyclic Cocycles…";
  - the Thm 7.2 independence hypothesis;
  - "convex domains" exhaustion;
  - "strictly contained in the interior";
  - 052320;
  - 22441676;
  - the PPGEE address.
- **Negative controls:**
  - v3 against Zenodo gives 0.29.
  - Removing 3000 characters around Thm 6.3 drops the ratio to 0.969 (detected).
- **Folder PDF:** the PDF in the folder equals a fresh build of the current `.tex` (ratio 1.000000, 0 ops).

## 2. Audit items

| Item | v3 location | Verdict | Re-derivation / evidence |
|---|---|---|---|
| **A1** entropy | Thm 3.6, Rem 3.7, abstract (2), Table 1 | **CONFIRMA** | See the four points below the table. |
| **A2** WF set | Def 5.2, Rem 5.3, Prop 5.4, Rem 5.5 | **CONFIRMA** | See the points below the table. |
| **A3** Dixmier | Def 6.1, Prop 6.2, Rem 6.3 | **CONFIRMA** | Def 6.1 is now linear (positive part, then linearity), as in Connes. \|D\|^{-d} := 0 on ker D. Principal symbol Φ‖ξ‖^{-d}Id. c_1 = 1/π and c_2 = 1/(2π) recomputed by hand from c_d = 2^{⌊d/2⌋}\|S^{d-1}\|/(d(2π)^d); they agree with the referee's singular-value numerics for Φ ≥ 0. |
| **A4** cocycle | Prop 6.4, Rem 6.5 | **CONFIRMA** | See the points below the table. |
| **A5** QFI | Lemma 7.2, Thm 7.3, Rem 7.4 | **CONFIRMA** | See the points below the table. |
| **A6** Lean | Declarations, §8, Zenodo description | **CONFIRMA** | The body has no formal-verification claim. The only Lean sentence is the standard disclaimer. The Zenodo text says "Nothing is formally verified". |
| M1 | Thm 2.3(c) | CONFIRMA | See the points below the table. |
| M2 | Thm 2.6 | CONFIRMA | (a): Brenier, McCann (entropy displacement-convex in ℝ^d), and K-convexity of V along segments in the convex Ω; the proof is complete. (b), (c) are labelled classical. Caffarelli: see §3. Var decay: d/dτ Var = −2∫\|∇P_τu\|² ≤ −2K Var. Limit ∫u₀dμ_A. vR–S only in a remark. |
| M3 | §2.1 | CONFIRMA | ψ_i ∈ L⁴, orthonormal, ∫Φ = Tr A. The bound ‖Φ(M)‖_{L²} ≤ ‖M‖_op‖Σψ_i²‖_{L²} ≤ L_ψ‖M‖_F is correct (M symmetric). |
| M4 | Def 3.2, remark after Thm 3.3 | CONFIRMA | Closed-cell max realization (u.s.c.). The uniform-limit argument is correct. |
| M5 | Prop 4.5, Rem 4.6 | CONFIRMA | See the points below the table. |
| M6 | Def 5.6, Prop 5.7, Rem 5.8 | CONFIRMA | Slab bound ‖Δ_h f‖_p^p ≤ (2‖f‖_∞)^p·2(n−1)‖h‖. Lower bound \|α−β\|(t/n)^{1/p} from adjacent cells. Note s*_1 = 1 = 1/p, so the formula holds for every p ≥ 1. The Minkowski lower bound is correct. |
| M7 | Lemma 7.2 | CONFIRMA | Proof re-derived. The factor 2 is confirmed by a Bures-fidelity oracle (§2 of the script). |
| M8 | abstract, §1, §8 | CONFIRMA | Every abstract item (1)–(6) matches a proved or cited statement. No existence, classification or "resolve" claims remain. |
| M9 | — | CONFIRMA | See §1. |
| B items | various | CONFIRMA | All checked in the text: Willmore H = κ₁+κ₂; Sard needs C^d; Rem 4.3 has H ≡ 0 in d = 1; the bound \|H\| ≤ (√d+1)‖Hess‖_F/‖∇Φ‖; Gaussian window, extended by 0; ker D; Cheeger; Crawley-Boevey; CSEH; Benamou DOI; vR–S title; Šafránek 052320; Chen–Vidal; cut distance and GW. **Prop 4.8 (Cheeger):** the proof was re-derived (median, coarea, Cauchy–Schwarz) and is correct. |
| Corrector's new findings 1–5 | — | CONFIRMA | (1) see §3. (2) Every bibitem is cited (checked key by key). (3) Thm 2.3(a) is a pull-back of a metric. (4) n = d, λ_min ≤ 1/d. (5) Sharpness: see M1. |

**A1 (entropy).**
- **Spectra (sympy).** σ(B) = σ(A) = {2±2√3, 0}. The charpoly of B′ is λ²(λ³−10λ²−54λ−54); it equals the charpoly of A′ and of C = JB′Jᵀ, and C ≠ B′.
- **H₁ persistence.** Computed by GF(2) boundary-matrix reduction on the filtered cubical complex. This is a third method, distinct from union–find and from rasterization. Results:
  - Dgm₁(B) = {(2,0)}, Dgm₁(A) = ∅;
  - Dgm₁(B′) = {(3,0),(3,1)}, Dgm₁(A′) = {(3,1)};
  - Dgm₁(C) = Dgm₁(B′);
  - no essential classes;
  - all of these are invariant under grid refinement r = 1, 2, 3.
- **Entropy.** E(B′) = 0.673012 = −(3/5)ln(3/5) − (2/5)ln(2/5). E(A′) = E(A) = E(B) = 0.
- **Negative controls.**
  - B′₄₄ = 3 gives one bar.
  - A log₂ entropy gives a value ≠ 0.673.
  - 300 random 3×3 matrices give at most 1 bar; random 5×5 matrices reach 5 bars.
- **Mayer–Vietoris lemma, re-derived.**
  - Y = K∖int W is connected, with H₁(Y) = 𝔽[∂W]. This uses H₁(K) = H₂(K) = 0 and H₁(W) = 0.
  - H₁(K∖U) = 𝔽²/𝔽(1,1). This uses H₂(K∖U) = 0, which holds for planar compact complexes.
  - The induction and the naturality step are sound.
  - K′ = [0,1]²∖[0,1/5)² is star-shaped about (1,1), and C̄₄₄ ⊂ int K′.

**A2 (wavefront set).**
- The integration by parts in Rem 5.3 is correct: V = g(−x₀)/(iξ) + O(ξ⁻²).
- Prop 5.4 was re-derived:
  - Hörmander's diffeomorphism law;
  - (ξ′)^α·(χH)^ = ((−i∂′)^α χ·H)^, bounded in L¹ by ‖∂′^α χ‖, which gives rapid decay off ±e₁;
  - non-emptiness via sing supp = π(WF);
  - the symmetry ξ → −ξ for real f, together with conicity.
- Rem 5.5 (corner): the product decay is only polynomial. Combined with the localization property (rapid decay for χ passes to φχ), this gives all directions.

**A4 (cyclic cocycle).**
- (a) G = −Φ₀γ^μγ^ν∂_μΦ₁∂_νΦ₂ and (1/(2(2π)²))·2π = 1/(4π).
- (b) γ = −iσ₁σ₂ = σ₃, and tr(σ₃σ_μσ_ν) = 2iε_{μν}.
- (c) Σ_σ sgn σ F^{σ0} dF^{σ1}∧dF^{σ2} = 2 det[F, ∂₁F, ∂₂F] dx = 2F*ω, and ∫F*ω = 4π deg F. Hence the sum is −4i deg F.
- **Numerics.**
  - The Pauli traces were checked by explicit matrix products.
  - For degrees k = 1, 2, −1 under 3 rotations, (i/4)Σ sgn σ τ₂^γ = k (error < 1e-6, N = 128/256/512). The oracle is the degree from a **signed preimage count**, which is independent of the integral.
  - The ungraded τ₂ varies with rotation at fixed degree: [0, −0.022, −0.019, −0.007, −0.052].
  - Rem 6.5 degree-0 example: τ₂ = −0.719 < 0.
  - Negative control: prefactor i/2.

**A5 (QFI).**
- Lemma 7.2 re-derived: symmetrization gives ½Σ(λ_i+λ_j)Re(L_{ij}L_{ji}).
- Thm 7.3(a)–(d) re-derived:
  - the Gram matrix under a positive weighted HS product;
  - weights 2/(λ_i+λ_j) ≥ 1;
  - continuity of det g;
  - the Jacobian law.
- Oracle: the Bures expansion d_B² = g ε²/4. Observed order 1.9–2.1; after Richardson extrapolation the relative error is ≤ 1.2e-5. Without the factor 2 the error is 0.5 (negative control).
- Rem 7.4(i): det g = 0. Rem 7.4(ii): det g > 0 in 10 random cases (min 10.2).

**M1 (Thm 2.3(c)).**
- Re-derived line by line: Lax–Milgram (Neumann, ∫∂ρ = 0); Poincaré constant 1/π on the cube; ‖∇φ‖ ≤ ‖∂ρ‖/π; v = ∇φ/ρ solves the continuity equation; ‖v‖_{L²(μ)}² ≤ ‖∂ρ‖²/(π²c₀); AGS 8.3.1.
- (b): the coupling marginals were verified. The sharpness example gives W₂ = 1−ε exactly (numerics: 0.9000 and 0.9500).
- Rem 2.4: the ratio is 0.99992 → 1.00000. With the constant 1/(2π) the bound is violated (negative control).

**M5 (Prop 4.5).**
- Critical points: Hessians ±[[0,1],[1,0]] and ±Id, so u is Morse.
- Scaling: H_{Φk}(x) = kH_u(kx) and ‖∇Φ_k‖ = εk‖∇u(kx)‖, which gives εk³·k⁻²∫_{(0,k)²}g.
- The period-cell bounds give c_*(1+O(1/k)).
- c_* = **1.0577638**, by adaptive quadrature on the quarter cell (×16, by symmetry). It is stable over tolerances 1e-6 to 1e-10. Dropping the Hessian term gives 2.28 (negative control).

## 3. Citations and DOIs

| Item | Verdict | Evidence |
|---|---|---|
| Vol. I DOI fix | **CONFIRMA** (with caveat) | 10.5281/zenodo.22644743 resolves (DataCite) to the *Beyond the Spectrum* trilogy concept record, versions 22644744/22699282/22866175. Part I of the trilogy PDF carries exactly the cited Vol. I title. The old 22441676 resolves to the cobordism paper (negative control). **Caveat:** this is also the concept DOI under which Vol. II v3 will be published. If the v3 upload does not contain Vol. I, the citation will resolve to a record without Vol. I. In that case, cite the version DOI 10.5281/zenodo.22866175 instead, or keep Vol. I in the upload. |
| All 22 DOIs (Connes 1994 has ISBN only) | CONFIRMA | All resolve, and title, authors and year match. AGS and Villani differ only because Crossref stores the short title ("Gradient Flows", "Optimal Transport"); checked by hand. The mutated DOI gives 404. The v2 Benamou DOI resolves to Bey, *Simplicial grid refinement* (negative control). |
| White 1973 | CONFIRMA (source read) | The PAMS PDF states that ∫H²dA is invariant for compact orientable surfaces, with the centre of inversion off the surface, and attributes the local invariance of (H²−K)dA to Blaschke. The paper's Prop 4.4 matches. White assumes C³ immersions; the pointwise identity needs only C². This is cosmetic. |
| Caffarelli 2000 | CONFIRMA (secondary source) | The original is not accessible. Fathi–Gozlan–Prodhomme (arXiv:1904.06053, Thm 1) restate Caffarelli's theorem: γ to e^{−W}γ with W convex, allowed to be +∞, and ν compactly supported; the Brenier map is 1-Lipschitz. This covers μ_A = f dγ_{K⁻¹} on the cube. |
| AGS Thm 8.3.1; Hörmander §8.1–8.2; Connes 1988 normalization | **INCERTO** (access) | The sources were not accessible in this session. The statements used match the standard forms: AGS 8.3.1 is the continuity-equation characterization of AC curves; Hörmander Prop 8.1.3 and Thm 8.2.4; Connes' trace theorem with 1/(d(2π)^d). The normalization agrees with the referee's d = 1, 2 numerics. Needs a reading of the texts, by a human or with library access. |

## 4. Front matter, house style, declarations

**Verdict: CONFIRMA**, with three B-level observations that do not block.

- **Claims match the body.** Title, abstract, introduction and §8 claim only what the body proves or cites. There is no formal-verification claim.
- **House style.** No "corrected", "withdrawn", "earlier version" (apart from the standard Lean sentence) or `audit/` paths.
- **Affiliation.** "Master's student, Postgraduate Program in Statistics and Agricultural Experimentation (PPGEE/DES), Department of Statistics (DES), UFLA", identical to the other companion papers. CAPES 001 is acknowledged.
- **Declarations.** Identical, after whitespace normalization, to `_staging/DECLARACOES_PADRAO_ARTIGOS.tex` (volume variant, Lean sentence included).

B-level observations:
- (i) "Functional Tensor Manifolds" in the title is never defined in the body. It is the series name; acceptable, but vague.
- (ii) The introduction says classical results are marked "classical" in their headings. Prop 6.2 is a direct application of Connes' trace theorem but is not so marked; the table does credit Connes.
- (iii) Rem 6.5's range "[−0.015, 0.037]" depends on an unspecified map and rotations, so it cannot be reproduced from the text. A different degree-1 map gives [−0.052, 0].

## 5. Notes

| File | Verdict | Remarks |
|---|---|---|
| `ZENODO_DESCRIPTION_VOL2.md` | CONFIRMA | Every listed result is in the body with the stated label. No Lean, GitHub or "pending" wording. "Besov index 1/p" omits "non-constant", which is harmless. |
| `CORRECTIONS_2026-10-06.md` | **PROBLEMA (B)** | (a) Item 1 says "a reflected matrix JBJᵀ … two distinct lifetimes": it should be JB′Jᵀ (the 5×5 B′); the 3×3 B has one bar. (b) The section "What still needs work" holds pending items: the layer-2 re-check (done here), the moves to `_arquivo/`, and "must be replaced when v3 is uploaded". Update or remove it before the note is used as the Zenodo version note. There is no GitHub-availability claim. The Zenodo-trilogy warning (v2 still on pages 29–46, false landing-page text) is accurate and important. |

## 6. Build: CONFIRMA

- The `.tex` was copied to `L2_build/v3` and compiled with pdflatex three times.
- Every run exited with code 0. The output is 18 pages.
- The log has 0 errors, 0 LaTeX warnings, 0 overfull boxes, 0 underfull boxes and 0 undefined references. Its only line matching "warning" is the `infwarerr` package banner.

## Summary

**31 items: 29 CONFIRMA, 1 PROBLEMA (B, notes), 1 INCERTO.**

- **PROBLEMA (B):** `CORRECTIONS_2026-10-06.md`, "JBJᵀ" should be "JB′Jᵀ", and the "What still needs work" section lists pending items.
- **INCERTO:** AGS Thm 8.3.1, Hörmander §8.1–8.2 and the Connes 1988 normalization were not read in the source.
- **Non-blocking observations:** the Vol. I DOI caveat (§3); the B observations (i)–(iii) of §4.

**Closing (prova-rigorosa).**
- **Hardest step:** the induction in the Mayer–Vietoris lemma of Thm 3.6. It was checked by hand and backed by a third persistence algorithm, with grid refinement.
- **What would falsify these verdicts:**
  - a reading of Caffarelli's original that excludes indicator perturbations;
  - a different normalization in Connes 1988. Excluded numerically for d = 1, 2.
- **Missing:** Prop 6.4 is checked through the trace theorem and the symbol algebra. The Dixmier trace of the graded operator was not computed directly.
- **No processes left:** `processos_orfaos.py` reports 0 suspected orphans.
