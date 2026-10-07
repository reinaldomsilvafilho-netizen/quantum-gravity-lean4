# Layer-2 re-check: *Beyond the Spectrum*, Vol. I (Functional Realizations)

- Verifier: an independent subagent (Claude Opus). It wrote none of the following: the volume, `blind_layer1.md`, the reconstruction, or the corrections.
- Date: 2026-10-06.
- Protocol: `unified_quantum_gravity_book/audit/verify/PROTOCOL.md`, layer 2. The skill `prova-rigorosa` was followed.
- Inputs read:
  - `blind_layer1.md`;
  - `fixes_layer1.md`, including the Declarations note;
  - `RECONSTRUCTION_v2.md`;
  - the current `.tex` and PDF;
  - the v2 text (the trilogy, and the standalone v2 PDF);
  - the v1 backup and the pure v2 reconstruction in `_arquivo/backup_tex_2026-10-06/…`;
  - `CORRECTIONS_2026-10-06.md` and `ZENODO_DESCRIPTION_VOL1.md`;
  - `_staging/DECLARACOES_PADRAO_ARTIGOS.tex`.
- Primary sources read in full text (arXiv):
  - Auffinger–Ben Arous–Černý 1003.1129: eq. (2.2), Remark 2.9, eq. (2.20);
  - Zhao 1302.1634: §3;
  - De Silva–Lim math/0607647: Prop. 4.6 and Thm 4.10;
  - Tomioka–Suzuki 1407.1870: Thm 1.

## Scripts (new, independent of `fixes_layer1_checks.py`; fixed seed; outputs in `.out.txt`; all exit 0)

| Script | Content | Result |
|---|---|---|
| `scripts/L2_reconstruction.py` | Compiles the pure v2 reconstruction. Token-stream diff (alphanumeric, numbers included) against the v2 standalone PDF (22699282) and against the trilogy Vol. I pages (22866175). Negative control: one word and one digit are mutated and must be detected. Inventory of section and theorem titles, v2 against the current file. | 0 failures |
| `scripts/L2_numerics.py` | Blocks A–I (see below). Each claim has an independent oracle and a negative control. | 0 failures, 6 min, < 0.5 GB |
| `scripts/L2_refs.py` | Every DOI in the bibliography and body, via Crossref or DataCite. Checks title, first author, year, volume and first page against the bibitem. Negative control: a fake DOI. | 0 failures |

Two of my own test designs were wrong at first, and I fixed the tests, not the tolerances to the paper's numbers:
- **Unfolding norm as an upper oracle.** The unfolding spectral norm is a rigorous but loose upper bound on ‖T‖_σ. It grows like d^{(k−2)/2}, so for k ≥ 3 and large d it exceeds C_k. It is now reported, not tested. The two-sided test uses HOPM, which is exact for k = 2, together with a restart-robustness check.
- **Mollified total variation.** Mollified TV converges at observed order 1.00. The test now compares the Richardson limit, 18.4000 against 18.4000.

No orphan processes were left (`processos_orfaos.py`: 0 suspects).

## 1. Reconstruction — CONFIRMA

- **Word-level match.** The compiled pure reconstruction agrees with the published v2 text word for word: ratio 0.99979 against both the standalone v2 and the trilogy Vol. I. The only two non-equal tokens are table-of-contents page numbers. In the TOC, §6.4 is on p. 14 in the reconstruction and on p. 15 in v2, a small layout shift. The mutated stream is detected.
- **No v2 content lost.** Every v2 title that is missing from the current file is a deliberate rename, or the removed "Formal Verification and Code Availability" section. Examples of renames:
  - "…Resolution of the Border-Rank Pathology" became "…Best Rank-One Approximation";
  - "Dirichlet Stability of Attention Fields" is now a Proposition.
- **Correct v2 content kept.** I read v2 §§5.4–8 against the current text. The correct v2 content is kept:
  - the Morse–Bott remark;
  - the Ginibre/k = 2 remark (now in Rem. 5.9);
  - Tomioka–Suzuki and Nguyen–Drineas–Tran;
  - open problems 1–3.

## 2. Audit items

### A items

| Item | Verdict | Evidence |
|---|---|---|
| A1 Constr 3.7 | **CONFIRMA** | With dμ = dx/(2π)² and no 1/n, ‖f_A‖ = ‖A‖_F. Quadrature agrees to 1e-12, and the 2π Lebesgue factor is correct. NEG: the v2 claim gives 9.93 against 6.32. No over-correction: this is the book's convention, and the Lebesgue factors are stated. |
| A2 Thm 4.1 + Rem 4.2 | **CONFIRMA** | Re-derived the identity E = ‖DA‖²+‖AD‖². Spectral-differentiation oracle agrees to 1e-8. Central differences converge at observed order 1.88/1.97/1.99 (expected 2). The bound 2‖A‖² ≤ E ≤ 2n²‖A‖² gives ratios in [n⁻², n²]: 400 random checks, plus E_nn/E_11 = 25 = n². For I_n and J_n, all 120 permutations give ratio 1. NEG: (k₁+k₂)² weight; v2's "for every A". |
| A3 Ex 4.3 | **CONFIRMA** | Checked E = 2n·n(n+1)(2n+1)/6 (n = 4, 8, 16) and E_J = E_checkerboard. E/n⁴ → 2/3, and E/n³ is unbounded (v2's Θ(n³) is the NEG). TV = 4(n−1) = 20 at n = 6, from the mollification oracle. |
| A4 Thm 5.7 | **CONFIRMA** | ABC eq. (2.20) reads lim (1/N) log E Crt_N(R) = ½ log(p−1), with Hamiltonian (2.2) = N^{−(p−1)/2} Σ over ordered tuples, as stated. The bridge H_{N,p}(√N x) = √N f_T(x) is re-derived. Re-derived from (x·y)^d: the Hessian covariance d(d−1)(1+δ_ij) and the decorrelation, Riemannian Hessian H₀ − d f I. Monte Carlo: covariance 0.3535 against (x·y)³ = 0.3536. Multiset-iid model: variances 1.005 and 2.502 against 1 and 5/2, so it is not isotropic (NEG: isotropy fails). Cartwright–Sturmfels gives 14 for n = d = 3. |
| A5 Rem 5.2, §6.4 body, abstract, Table 1 | **PROBLEMA (B, residual)** | **Correct:**<br>• The content is correct, and Rem 5.2 matches De Silva–Lim Prop. 4.6 (read in the source).<br>• ‖T−X_t‖·t equals 1.734935, 1.732080 and 1.732051 for t = 10, 100 and 1000, tending to √3; both weights are of order t.<br>• The slice pencil S₀⁻¹S₁ is a non-zero nilpotent, so the rank is greater than 2. As a control, a rank-2 tensor gives a diagonalizable pencil.<br>**Residual:** the **§6.4 heading (and TOC line) still reads "Circumventing the De Silva–Lim Pathology"**, which contradicts the body. It should be renamed, e.g. "Best Rank-One Approximation and the De Silva–Lim Pathology". |

### The corrector's partial disagreement: Theorem 5.8 (v2 Thm 5.6) — CONFIRMA

- **New findings confirmed in the v2 text** (trilogy p. 13–14):
  - The statement says "d^{1/2−β} f̂ … → 0 if β < ½ and → ∞ if β > ½". Since d^{1/2−β} f̂ = d^{−β}X and sup X ≍ √d, this is inverted. The v2 proof even states the correct direction.
  - "c_k = Θ(1/k)" is not the right constant. For Gaussian entries X(u) ~ N(0,1) exactly, and for sub-Gaussian entries the general Hoeffding inequality gives a k-free constant. Tomioka–Suzuki Lemma 1 says the same.
- **Proof re-derived line by line:**
  1. **Variance.** Var X(u) = ∏‖u^{(α)}‖² = 1.
  2. **Net step.** The telescoping X(u)−X(v) = Σ_α X(v¹..v^{α−1}, u^α−v^α, u^{α+1}..u^k) is correct (numerical check, with a dropped-term NEG). Each term is ≤ εS by homogeneity. ε = 1/(2k) gives S ≤ 2 max_net. The net has size (1+4k)^{kd}.
  3. **Maximal inequality.** E max|Z_i| ≤ √(2 log 2N) without independence: Jensen over the 2N variables ±Z_i. Monte Carlo with ρ = 0 and ρ = 0.5, N up to 2·10⁴. NEG: √(log 2N) fails.
  4. **Constant.** 2√(2kd log(1+4k)+2 log 2) ≤ C_k√d for all d ≥ 1, checked for k ≤ 8 and d < 500.
  5. **Lower bound.** Hölder with exponents (3/2, 3) is correct; E‖Z‖⁴ = d(d+2), so E‖Z‖ ≥ d/√(d+2) ≥ √(d/3) exactly when d ≥ 1. Checked against the exact χ mean for d < 2000. NEG: E‖Z‖ ≥ √d fails.
  6. **β clause.** Follows from the sandwich.
  7. **Part (ii).** Conditioning gives the exact N(0,1) law. P(|Z| > s) ≤ 2e^{−s²/2}, and ½ is sharp.
- **Numerics:**

| Check | Result |
|---|---|
| E sup f̂: k = 2 (exact SVD), d = 8–128 | 1.74 → 1.97 → 2 (Bai–Yin). Gaps shrink by a factor ≈ 0.6 per doubling. |
| E sup f̂: k = 3 (HOPM), d = 4–64 | 2.22, 2.49, 2.65, 2.70, 2.74. Stabilizes, inside [0.577, 8.19]. |
| E sup f̂: k = 4 (HOPM), d = 4–24 | 2.69–3.28, inside [0.577, 9.81]. |
| HOPM restart robustness | 4 → 24 restarts moves the estimate 2.69 → 2.75. |
| β = 0.25 (NEG: v2 clause) | d^{−β}E‖T‖ grows. |
| β = 0.75 (NEG: v2 clause) | d^{−β}E‖T‖ decays. |
| v1 normalization d^{−(k−1)/2} (NEG) | Decays: 0.88 → 0.34. |
| Rademacher entries (Rem 5.9) | 2.40–2.68. |
| (ii) law of √d f̂ | KS p = 0.47 (k = 3) and 0.96 (k = 4). |
| (ii) tail | Below 2e^{−dε²/2}. NEG: 2e^{−dε²} and the constant 1 are both violated. |

- **No over-correction.** Restricting the Theorem to Gaussian entries is a scope reduction, not a loss: the sub-Gaussian case is kept in Rem 5.9, which is honestly a Remark with a proof outline, and its outline is correct. The fourth-moment lower bound and Hoeffding are re-checked. "C_k = O(√(k log k)), same order as Tomioka–Suzuki" is correct: TS Thm 1 gives √(8σ² Σn_k log(2K/K₀)).

### Other cited claims

| Item | Verdict | Evidence |
|---|---|---|
| Rem 5.5 (Zhao) | **CONFIRMA** (minor B note) | Zhao §3 opens "we sketch the idea for 3-uniform hypergraph limits". He says Theorem 2.3 "extends with virtually no change": some subsequence converges in the vertex-cut norm (4) to a symmetric W: [0,1]³ → [0,1]. The counting lemma fails for non-linear F (K₄⁽³⁾). The limits are on [0,1]^{2^k−2} (§1). The attribution is accurate. **Optional:** Zhao states it for sequences of 3-uniform *hypergraphs*. "every sequence" of symmetric functions is a mild extension and could say "of hypergraphs". |
| Thm 4.11 (Lovász–Szegedy GAFA 2007) | **CONFIRMA** | Weak isomorphism, [m, M] rescaling, and measurable limit are all correct. DOI metadata matches. |

### M/B items

Each of the following was checked against the current text: **CONFIRMA**.
- Def 2.2(ii); Prop 3.3; Constr 3.5; Constr 3.8.
- Thm 4.5:
  - The sign-saturation proof is re-checked: disjoint supports, compact support, and |φ| ≤ 1. The weight ∫g ≥ 1/n − 4ε is even better than the stated 6ε.
  - Mollification oracle, independent of the coarea one: order 1.00, Richardson limit 18.4000 = formula. NEG: without the 1/n factor.
- Thm 4.6; Thm 4.7 (n = 1 included).
- Thm 4.10: sharpness 4 by brute force. Random 6×6 kernels give ratios ≤ 3.39. NEG: the constant 2.
- Thm 5.1, including the rank-one reduction; Thm 5.4.
- Prop 5.6:
  - f(0,0) = N; the sup bound holds for N = 4, 8, 16;
  - for λ = 0 the lattice sum diverges like log K (NEG);
  - for λ = 0.5 it converges.
- §6.1–§6.3: labelled as proposals or a conjecture.
- §6.5 body.
- The Formal Verification section is removed.

**Residual headings — PROBLEMA (B).** The text corrected the claims, but some headings still carry them:
- §4: "Emerging Invariants: **What Matrix Algebra Cannot See**". This contradicts the abstract ("not … inaccessible to matrix algebra") and Rem 4.2.
- §6.5: "…**Minimal Surface** Level Curves". "minimal-surface formulation" was removed from the body.
- §6.5 also says "essential level curves" while Thm 4.6 uses the reduced boundary ∂*.
- §6 "Deep Implications…" is rhetoric only (optional).

## 3. Front matter, back matter, house style, DOIs

| Item | Verdict | Note |
|---|---|---|
| Title, abstract, introduction, Table 1, conclusion | CONFIRMA (apart from the headings above) | Each claims only what is proved, cited or labelled. Table 1 row 5 says "rank r ≥ 2 remains ill-posed". The book overlap is disclosed in §1. |
| No formal-verification claim | CONFIRMA | |
| House style | CONFIRMA | No "earlier version", "withdrawn", "corrected", audit paths, WORKPLAN or GitHub in the `.tex`. |
| Affiliation, CAPES | CONFIRMA | "Master's student, Postgraduate Program in Statistics and Agricultural Experimentation (PPGEE/DES)…, UFLA"; CAPES Finance Code 001. |
| Declarations against `DECLARACOES_PADRAO_ARTIGOS.tex` | **PROBLEMA (B)** | Funding, competing interests, AI use (with "volume") and code availability match the standard. Verification status: "The Lean 4 files **in the author's repository**" is inaccurate. The repo (`git ls-files`) holds no Lean file for this volume. The Lean files of this volume were the zip of Zenodo v1/v2, and the repo skeletons are other projects. Use the standard wording: "The Lean 4 files that accompanied earlier versions are a placeholder skeleton without Mathlib and verify none of the mathematics." |
| DOIs | CONFIRMA | All 19 bibliography DOIs plus the body DOI 10.5281/zenodo.22644743 resolve with matching metadata (`L2_refs.out.txt`). The corrector's list missed the book DOI 10.5281/zenodo.22290043; it resolves (DataCite, Silva-Filho, 2026). |

## 4. Notes

| File | Verdict | Note |
|---|---|---|
| `CORRECTIONS_2026-10-06.md` | **PROBLEMA (B)** | The mathematical items 1–6 are accurate and verified above. Three statements need fixing:<br>(a) "the public repository named in the Code-availability statement": the statement names no repository ("on request"), and the folder is not in git. Delete it or rephrase it as "scripts on request".<br>(b) "Every item was checked again with new scripts before any change" overclaims: several B items have no script ("—" in `fixes_layer1.md`). Say "every A item and the numerical claims".<br>(c) "Layer 2 … has not been done yet" must be updated after this report. |
| `ZENODO_DESCRIPTION_VOL1.md` | CONFIRMA | It is accurate and does not overclaim. Graphon compactness and the ABC rate are presented as cited or imported, and the limits are stated. It makes no GitHub statement. **Optional:** add one line disclosing the overlap with the book's Chapter 1. |

## 5. Build — CONFIRMA

- `audit/L2_build/`: pdflatex was run 3 times. Result: 21 pp., 0 errors, 0 LaTeX/Package/Class warnings, 0 overfull, 0 underfull, 0 undefined references.
- The log has 3 lines "pdfTeX warning (font expansion): font should be expanded before its first use", from microtype with cm-super.
  - They are not counted by the project gate (`build_pdfs_safe.py` counts `(LaTeX|Package|Class) Warning`).
  - The same lines are in the shipped log.
  - They are benign. Report them if the gate is read literally.
- The output is byte-size identical to the shipped PDF (761 009 B).

## Summary

- **CONFIRMA:** 16 items:
  - the reconstruction;
  - A1–A4;
  - Thm 5.8 with the corrector's two new findings;
  - Rem 5.9;
  - Rem 5.5 (Zhao);
  - Thm 4.11;
  - the M/B body items;
  - front matter;
  - formal-verification removal and house style;
  - affiliation and CAPES;
  - DOIs;
  - Zenodo description;
  - build.
- **PROBLEMA:** 4 items, all B and none mathematical:
  1. §6.4 heading still says "Circumventing the De Silva–Lim Pathology" (residual of A5).
  2. Headings of §4 ("What Matrix Algebra Cannot See") and §6.5 ("Minimal Surface", "essential").
  3. Declarations: "Lean 4 files in the author's repository" should use the standard wording.
  4. CORRECTIONS: a nonexistent "repository named in the Code-availability statement", "every item checked with scripts", and the layer-2 status.
- **INCERTO:** 0.

Per protocol, each PROBLEMA becomes a correction for another session. A short re-check of the renamed headings and the edited sentence suffices; no re-check of the mathematics is needed.
