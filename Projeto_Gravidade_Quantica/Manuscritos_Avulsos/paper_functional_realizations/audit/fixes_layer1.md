# Layer-1 corrections: *Beyond the Spectrum*, Vol. I

- Corrector: an independent subagent (Claude Opus). It wrote neither the paper nor `blind_layer1.md`.
- Date: 2026-10-06.
- Base text: the Zenodo v2 text, rebuilt from the PDF (`../RECONSTRUCTION_v2.md`).
- Corrected source: `../paper_functional_realizations.tex`. It compiles to 21 pp. with 0 errors, 0 warnings, 0 overfull/underfull boxes and 0 undefined references.

## Scripts

- `scripts/fixes_layer1_checks.py` (output in `.out.txt`; exit 0; 0 failures).
  - Fixed seed.
  - Oracles independent of the paper's formulas:
    - grid quadrature;
    - 4th-order finite differences, with refinement at observed order 3.99 / 4.00;
    - a coarea integral computed over thresholds;
    - brute force over permutations and over sign/indicator vectors;
    - Monte Carlo;
    - multi-start Riemannian Newton;
    - HOPM;
    - exact χ-means.
  - Every block has a negative control (a mutated formula that must fail).
  - Peak memory about 0.4 GB; runtime about 2 min.
- `scripts/fixes_refs_check.py` (output in `.out.txt`; 0 failures).
  - Crossref/DataCite check of title, first author and year for every DOI.
  - Negative control: a fake DOI gets HTTP 404.
  - Adler–Taylor has no author field in Crossref. Its authors were checked in Open Library under ISBN 9780387481128.
  - The list also covers Federer and Ambrosio–Fusco–Pallara. Neither is cited in the paper.
- Sources read directly:
  - ABC, arXiv:1003.1129: eq. (2.2), Thm 2.8, Remark 2.9 / eq. (2.20).
  - De Silva–Lim, arXiv:math/0607647: Prop. 4.6 and Thm 4.10.
  - Zhao, arXiv:1302.1634: §3.
  - Lean zip of v2: `lakefile.lean` has no Mathlib, and the theorems return fields of their own hypotheses (`exact P.h_amp`, `exact M.h_compact`, …).

## Items

| Item (v2 numbering) | Verdict | Change | Where (new text) | Check |
|---|---|---|---|---|
| Version check (§0 of the report) | Agree | `.tex` rebuilt to v2 before correcting. | whole file | word diff, `RECONSTRUCTION_v2.md` |
| Def 2.2(ii) (B) | Agree | Faithful means injective; for linear Φ, ker Φ = {0}, where "zero" is the zero element of the target space (a.e. or measure zero). | Def 2.2(ii) | — |
| Prop 3.3 (B) | Agree | Called classical Rayleigh–Ritz. "Euler–Lagrange" became the Lagrange multiplier rule, with the regularity ∇(xᵀx) ≠ 0 stated. The repeated-eigenvalue case is spelled out. | Prop 3.3 | — |
| Constr 3.5 (B) | Agree | h_α = L_α/n_α is defined. "f_A ∉ C⁰" became "continuous only when A is constant". | Constr 3.5 | — |
| **Constr 3.7 (A)** | **Agree**. Oracle: the paper's value is 5.12 against ‖A‖_F = 1.63 (n = 2). | Adopted the book's convention: no 1/n, and the normalized Haar measure dμ = dx/(2π)². Then ‖f_A‖ = ‖A‖_F exactly. A sentence gives the Lebesgue-measure factors 2π and (2π)². | Constr 3.7 | quadrature matches to 1e-10; the v2 claim fails (NEG) |
| Constr 3.8 (B) | Agree | P ∈ R^{(m+1)×(n+1)×3}. C^{p−1} only at simple knots; C^{p−μ} at a knot of multiplicity μ. | Constr 3.8 | — |
| Constr 3.9 | Agree (confirmed) | — | — | — |
| **Thm 4.1 (A)** | **Agree** on all 4 points. | (1) With dμ the formula Σ(k₁²+k₂²)\|a\|² is exact; the FD oracle converges at order 4. (2) The statement now reads "for every n ≥ 2 there exist A, P₁, P₂ with ratio exactly n²". A new bound shows ratio ∈ [n⁻², n²] for all A. A new Remark covers the counterexamples I_n and J_n (ratio 1). (3) Θ(n²) at fixed n was replaced by exact values. (4) The identity E = ‖DA‖²_F + ‖AD‖²_F is now in the statement, and the abstract no longer claims the quantity is "unreachable by matrix algebra". | Thm 4.1, Rem 4.2 | FD order 3.99/4.00; ‖DA‖²+‖AD‖² matches to 1e-9; NEG mutants (k₁+k₂) and ‖DAD‖²; all 720 permutations for I and J give one value |
| **Ex 4.2 (A)** | **Agree** | E = 2n·n(n+1)(2n+1)/6 = (2/3)n⁴ + O(n³), the maximum over entries in [−1, 1], equal to the value for J_n. TV is 4(n−1) for the checkerboard and 0 for J_n, so the step realization, not the harmonic one, sees the oscillation. | Ex 4.3 | FD at n = 4…32; NEG Θ(n³); TV via the coarea oracle |
| Def 4.3 | Agree | — | — | — |
| Thm 4.4 (B, sketch) | Agree | Sign saturation written out: an explicit C¹_c field with disjoint supports away from grid crossings, with loss (1 − 6nε). Horizontal interfaces and the boundary term are now stated. | Thm 4.5 proof | coarea oracle matches to 1e-12; NEG without 1/n |
| Thm 4.5 (B) | Agree | Coarea formula attributed to Fleming–Rishel (with Evans–Gariepy, Ch. 5). "Essential" became "reduced" boundary, intersected with the open square. Proof says a.e. t, and every t here. | Thm 4.6 | as above |
| Thm 4.6 (label B; handlebodies) | Agree | Called classical (Milnor). "Rigorously" removed. The n = 1 case is noted. Handlebodies removed from the abstract. | Thm 4.7 | — |
| Rem 4.7 | Agree | Wording only. | Rem 4.8 | — |
| Thm 4.9 (B) | Agree | Title no longer mentions Grothendieck. The step "\|∫W g h\| ≤ ‖W‖_□ for [0,1]-valued g, h" is now proved by linearity in each argument. Sharpness example (constant 4) added. | Thm 4.10 + text | 2×2 checkerboard gives ratio 4.000; NEG constant 2 |
| Thm 4.10 (M) | Agree on all 4 points | Quotient by weak isomorphism (δ_□ = 0). Symmetric matrices with entries in [m, M], affinely rescaled. The limit is an equivalence class of measurable functions. The proof cites Lovász–Szegedy, GAFA 17 (2007). | Thm 4.11 | DOI checked |
| Ex 4.11 | Agree (confirmed) | — | — | — |
| §5 intro (B) | Agree | Hillar–Lim, J. ACM 2013, and De Silva–Lim, SIMAX 2008, added and cited correctly. "Insurmountable" and "overcomes these bottlenecks" removed. | §1(c), §5 intro | DOIs checked |
| Thm 5.1 (B) | Agree | "Strictly attained" became "attained". Lagrange regularity stated. Called classical (Lim). The rank-one consequence is now proved. "Eliminating scale divergences" removed. | Thm 5.1 | — |
| Thm 5.3(i) (B) | Agree | Renamed the norm of the k-linear form, not "L^∞→L¹". The reduction to indicators is proved one variable at a time. | Thm 5.4 | — |
| Thm 5.3(ii) (M) | Agree, and stronger | Zhao §3 only sketches, for k = 3, that weak regularity plus Lovász–Szegedy extend to the box cut norm. Compactness was therefore moved out of the theorem into Remark 5.5: cited sketch, not proved, plus a statement that the counting lemma fails. Added to the open problems. | Rem 5.5, §8 item 5 | Zhao text read |
| Thm 5.4 (M) | Agree | Now a Proposition with the book's version: λ > 0 is required; C_λ² = Σ 1/(1+\|k\|²+λ\|k\|⁴) → ∞ as λ → 0. For softmax slices f(0,0) = N, so no bound is uniform in N. "Morrey" and "hallucination" removed. | Prop 5.6 | C_λ bound at N = 4, 8, 16; partial sums at λ = 0 grow like log K (NEG: convergence fails) |
| **Thm 5.5 (A)** | **Agree.** ABC eq. (2.20) reads lim (1/N) log E Crt_N(R) = ½ log(p−1), for couplings i.i.d. over ordered tuples, eq. (2.2). | Replaced by the book's statement, re-derived here. (i) Ordered-tuple model, covariance (x·y)^d, isotropic. (ii) d = 2 gives 2n points. (iii) Rate ½ log(d−1), cited with equation number, plus a scaling bridge to ABC's H_{N,p}. (iv) The multiset-i.i.d. model is not isotropic (variance 3/2 and 5/2), and the Cartwright–Sturmfels a.s. bound applies. | Thm 5.7 | Var 1.5 and 2.5 against MC 1.00; n = d = 3: at most 14 critical points found (CS bound 14); NEG for exp(nΘ(d)) |
| **Thm 5.6 (M; v1-only A)** | **Partly disagree.** The referee confirmed the statements, but the v2 statement (i) is itself wrong in its β clause: it says d^{1/2−β}f̂ → 0 for β < ½, while d^{1/2−β}f̂ = d^{−β}X ≍ d^{1/2−β} → ∞. The v2 proof repeats the inversion. Also, v2's "c_k = Θ(1/k)" is not the right constant: for Gaussian T the exponent is exactly ½, independent of k. The Dudley proof has the increment gap noted by the referee. | Restricted to Gaussian entries and given a complete proof with explicit constants: 1/√3 ≤ E sup f̂ ≤ C_k = 2√(2k log(1+4k) + 2 log 2), via an ε-net with ε = 1/(2k), the multilinear approximation S ≤ 2 max_net, the Gaussian maximal inequality, and the Hölder bound E‖Z‖ ≥ d/√(d+2). The β clause is corrected. (ii) is now the exact N(0,1) law, with tail 2e^{−dε²/2}, sharp. The sub-Gaussian case moved to Remark 5.9 (general Hoeffding, Vershynin §2.6). The ABC normalization is reconciled. | Thm 5.8, Rem 5.9 | HOPM sup/√d ∈ [2.52, 2.77] ⊂ [0.577, 8.19] for Gaussian and Rademacher; NEG: d^{−(k−1)/2} gives sup/d decreasing; exact χ-mean ≥ d/√(d+2); tail below 2e^{−dε²/2}, NEG 2e^{−dε²} violated at ε = 0.7 |
| §6.1 (M) | Agree | Stated as proposals; the permutation-symmetry caveat added. The limit is a subsequence; cell averages replace point values. | §6.1 | — |
| §6.2 (M, B) | Agree | Cross-references now point to Thms 4.7 and 5.7. Rate ½ log(p−1). The RSB–β₀ link is labelled a conjecture and listed as an open problem. NP-hardness rephrased to the tensor spectral norm (Hillar–Lim). | §6.2, §8 item 4 | — |
| §6.3 (M) | Agree | No "embedding": blow-ups are at distance 0. "Time derivatives" replaced by continuity of a curve in the quotient. Attributed to Lovász–Szegedy via Thm 4.11, not Thm 4.10. | §6.3 | — |
| **§6.4 + abstract + Table 1 (A)** | **Agree.** De Silva–Lim, Prop. 4.6, checked in the source. | §6.4 restricted to rank one. The new Remark 5.2 gives the explicit counterexample: unit-norm factors, weights ~t, error √3/t + O(t⁻²), and the tensor has rank 3. The abstract and Table 1 row 5 now say that rank r ≥ 2 remains ill-posed. The citation was corrected from Lim 2005 to De Silva–Lim 2008. | Rem 5.2, §6.4, abstract, Table 1 | error √3/t at t = 10³; the Jordan-block pencil certifies rank > 2; NEG for bounded weights |
| §6.5 (B) | Agree | Anisotropic and isotropic TV distinguished. "Fractal" and "precise minimal-surface" removed. ROF is now cited. | §6.5 | — |
| Table 1 (B) | Agree | Rows rewritten: energy identity, "proposal", rate ½ log(d−1), rank-one only. | Table 1 | — |
| Abstract (M) | Agree | Rewritten. It claims only what the body proves and labels proposals and the conjecture. | abstract | — |
| Intro (B) | Agree | Citations added; contributions reworded; overlap with the book disclosed and cited. | §1 | — |
| Conclusion (M) | Agree | Lists exactly what is proved, cited or conjectural. Open problem 1 identified as a QAP. New problems 4 (RSB) and 5 (hypergraph compactness). | §8 | — |
| **Formal Verification section (M)** | **Agree** (zip re-inspected) | Section removed. The Declarations now say no statement is formally verified, and the Lean files are a Mathlib-free placeholder skeleton that verifies nothing. | Declarations | lakefile and `exact X.h_*` lines inspected |
| References (B) | Agree | Added: De Silva–Lim, Hillar–Lim, Lovász–Szegedy GAFA, Fleming–Rishel, Zhao, Cartwright–Sturmfels, Adler–Taylor, Vershynin, and the book (self-citation for the overlap). Qi, ROF and Milnor are now cited in the text. | bibliography | `fixes_refs_check.out.txt` |
| Overlap with book ch. 1 | Agree | The paper now cites the book and states the overlap in §1. The book was not edited (out of scope). It should cite this volume in turn. | §1 | — |
| Affiliation, funding, AI, declarations | (task) | English affiliation as specified; CAPES Finance Code 001; declarations adapted from `declarations_chapter.tex`. The pointer to WORKPLAN.md became "version notes of the Zenodo record". | address, Declarations | — |

## Notes for the layer-2 verifier

- The β-clause inversion and the c_k = Θ(1/k) claim in v2 Thm 5.6 are new findings, not in `blind_layer1.md`. Please check them.
- Remark 5.5 (hypergraph compactness) relies on Zhao §3, which is a sketch. Please confirm that the wording "cited sketch, not a theorem" matches the source.
- Theorem and remark numbers in the "Where" column refer to the compiled PDF of 2026-10-06. Check them against the PDF.

## Declarations (orchestrator, 2026-10-06, author decision)
- AI-use paragraph replaced by the standard block of `_staging/DECLARACOES_PADRAO_ARTIGOS.tex` (volume); code availability: scripts on request (the folder is not in git). Verification-status paragraph kept as written by the corrector.

## L2 B items (orchestrator, 2026-10-06)
- Headings renamed: §4, §6.4, §6.5; "essential level curves" -> "reduced boundaries of the superlevel sets" (matches Thm 4.6).
- Verification status: Lean sentence -> "files that accompanied earlier versions".
- CORRECTIONS: script wording, layer-2 line, repository and declarations lines fixed.


## Round 3 (independent corrector, 2026-10-06; inputs: `L2b.md`, `L2_layer2.md`)

Backup before editing: `_arquivo/backup_tex_2026-10-06/Manuscritos_Avulsos/paper_functional_realizations/paper_functional_realizations_round3.tex`, listed in `MANIFESTO.tsv`.

| Item | Change |
|---|---|
| [M] Abstract (iii)/(iv) | The abstract now splits the four groups of results. (i) Dirichlet/Sobolev and (ii) TV/coarea change under simultaneous permutation of rows and columns, so the spectrum does not determine them. (iii) Morse indices, fixed by the order of the eigenvalues, with the Euler characteristic, and (iv) the graphon cut distance, invariant under relabelling by construction, are described as permutation-invariant readings. "Explicit functions of the entries" now refers to (i) and (ii) only. |
| Same overclaim elsewhere | Introduction, contributions 3 and 4: invariance stated. Conclusion: the list "not determined by the spectrum" no longer includes Morse indices or graphon limits; they are named as permutation-invariant readings. `ZENODO_DESCRIPTION_VOL1.md`, line 3: the same split. Table 1 already made no invariance claim for rows 3 and 4 and is unchanged. |
| [B] §4 heading | "Emerging Invariants: Spatial, Topological and Asymptotic Quantities". I read all of §4 before choosing it. A two-sentence opening paragraph says that §4.1–4.2 are permutation-sensitive and §4.3–4.4 permutation-invariant, with the reasons. |
| §6.4 heading | "Computational Multilinear Algebra: Well-Posed Rank-One Approximation and the De Silva–Lim Pathology". |
| §6.5 display | H¹(∂*{W_A > t} ∩ (0,1)²), as in Theorem 4.6. |
| `CORRECTIONS_2026-10-06.md` | Lists the final headings of §4, §6.4 and §6.5, the new §4 opening paragraph, the §6.5 display, and the abstract, introduction and conclusion change. |

**Build:** pdflatex run 3 times, exit 0 each time. 0 errors, 0 LaTeX/Package/Class warnings, 0 overfull or underfull boxes, 0 undefined references, 21 pages. As before, the log has 3 benign microtype lines "pdfTeX warning (font expansion)". .aux, .out and .toc deleted; PDF and .log kept, as shipped.

**For re-check:** the abstract paragraph 2, the §4 opening paragraph, the conclusion sentence, and the Zenodo line 3.
