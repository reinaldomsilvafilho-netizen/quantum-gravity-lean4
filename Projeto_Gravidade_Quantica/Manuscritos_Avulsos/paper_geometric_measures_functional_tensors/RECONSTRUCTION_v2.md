# Reconstruction of the Zenodo v2 source of *Beyond the Spectrum II* (2026-10-06)

## Sources

- **Published text (v2):** Vol. II pages of the Zenodo trilogy PDF, record 22866175, `audit/scripts/zenodo_trilogy_22866175.pdf`.
  - Vol. II is trilogy pages 29–46. They were extracted to `audit/zenodo_latest_vol2.pdf` (18 pages).
  - Their text is identical to `Manuscritos_Avulsos/beyond_the_spectrum_files/volume_2_geometric_measures.pdf`.
  - Below, "p. N" means page N of the 18-page Vol. II; trilogy page = N + 28.
- **Local source before this work:** `paper_geometric_measures_functional_tensors.tex`, modified 2026-09-22. It was not the source of v2: word similarity 0.914, 110 diff operations (`audit/scripts/compare_tex_vs_zenodo.out.txt`).
- **Backup of the local source:** `_arquivo/backup_tex_2026-10-06/Manuscritos_Avulsos/paper_geometric_measures_functional_tensors/paper_geometric_measures_functional_tensors.tex`, logged in `_arquivo/backup_tex_2026-10-06/MANIFESTO.tsv`.

## Method

1. Extract the words of both PDFs with PyMuPDF.
2. Diff them with `difflib`, word by word, over the whole text.
3. Edit the `.tex` with the Edit tool until a fresh compile matches v2.

Final check, `audit/scripts/rebuild_v2_diff.py` (output `rebuild_v2_diff.out.txt`):
- 7175 words (v2) against 7177 words (rebuilt);
- **1 diff operation; similarity 0.9997.**
- The single remaining difference is spacing around `×` in `Ω11 = [0,1/3]×[0,1/3]`, which the extractor splits differently. It is typographic only.

The rebuilt v2 source is frozen as `audit/v2_reconstructed.tex`. The corrected version (v3) was then built on top of it.

## Reconstructed passages

| # | Passage | v2 page | How it was rebuilt |
|---|---|---|---|
| 1 | Proof of Thm 2.5: "Reilly–Bochner formula on *domains* with boundary"; "II denotes the second fundamental form of the boundary"; the paragraph on "exhausting sequence of smooth convex domains Ω_ε ↗ Ω … edge/corner contributions vanish for H² Neumann eigenfunctions" | 6 | Typed from the extracted text. The math symbols (Ω_ε, II_{∂Ω_ε} ≥ 0, ∫_{∂Ω_ε} II ≥ 0, H²) were set to match the PDF glyphs. |
| 2 | Thm 3.4 statement: "continuous topological persistence diagrams strictly separate them: Dgm₁(A) ≠ Dgm₁(B) with Dgm₁(A) = ∅ ≠ {(2,0)} ⊂ Dgm₁(B)", plus the sentence "for realizations with N_k ≥ 2 distinct persistence lifetimes, their persistent entropies strictly differ" | 8 | Typed from the extracted text. It replaced the local statement "Dgm₁(A) ≠ Dgm₁(B) and E⁽¹⁾(A) ≠ E⁽¹⁾(B)". |
| 3 | Thm 3.4 proof: v2 has no paragraph "with a single normalized bar … heights (2, 2.2, 2.4) …" and no clause "by the empty-diagram convention E⁽¹⁾(A) = 0" | 9 | Both local-only passages were deleted. |
| 4 | Thm 3.4 proof, closing sentence: "Furthermore, under smooth generic perturbations breaking cell degeneracies into N_k ≥ 2 bars of unequal lifetimes, … yielding strict entropy discrimination." | 9 | Typed from the extracted text. |
| 5 | Thm 4.4(a): "for each compact regular level hypersurface Σ_t ⊂ int(Ω) strictly contained in the interior (with Σ_t ∩ ∂Ω = ∅)" | 10 | Typed. It replaced the local "closed level set Σ_t ⊂ Ω (or under transformations preserving ∂Ω)". |
| 6 | §6.3: "For a tuple of d + 1 matrices" | 14 | Changed "d" to "d+1". |
| 7 | **Theorem 6.3** "Quantized Cyclic Cocycles and Topological Degree" (statement (a), (b) and proof). The local file had only an unlabeled sentence. | 14 | Typed in full from the extracted text. Display (6.7) was rebuilt as `\frac{2^{\lfloor d/2 \rfloor} \Omega_d}{d (2\pi)^d} \int_\Omega F_A^* \mathrm{vol}_{\mathbb{S}^d} = c_d \cdot \deg(F_A) \in c_d \cdot \mathbb{Z}`. The local "**quantized topological charge**" sentence was removed. |
| 8 | Thm 7.2: the added hypothesis "Suppose further that the directional tangent derivatives {∂_μρ(x)} are linearly independent in the Hilbert–Schmidt inner product (non-degenerate spatial variation)" | 15 | Typed. |
| 9 | Thm 7.2 proof: the sentence "By the non-degeneracy condition … strictly positive definite whenever any spatial gradient exists", and "almost everywhere" in place of "everywhere" | 15 | Typed. |
| 10 | §7.1: "canonical fiber bundle structure" without the literal `**` | 14 | In the v2 PDF the phrase is set in italic font (SFTI). It was rebuilt as `\emph{fiber bundle structure}`. The `**where**` of §7.3 was rebuilt as plain "where" (roman in v2). The literal `**spectral bottleneck**` was kept, because v2 prints the asterisks too (p. 11). |
| 11 | Bibliography | 17–18 | Every entry was rebuilt to the v2 wording: full journal names; ISBNs; DOIs as `\href`; "Berlin, Heidelberg"; "Clarendon Press". The Šafránek entry became no. 5, 052320 (the local file had 062320). The Vol. I entry gained DOI 10.5281/zenodo.22441676. |
| 12 | Author address: "Departamento de Estatística (DES), Programa de Pós-Graduação em Estatística e Experimentação Agropecuária (PPGEE/DES), Universidade Federal de Lavras (UFLA), Lavras, MG, Brazil" | 18 | Typed. It replaced the local "PPGEEAA/DES" address. |
| 13 | Date "September 10, 2026" | 1 | `\date{September 10, 2026}`, in place of `\today`. |

## Local-only material (in the 2026-09-22 `.tex`, not in v2): decision

| Local passage | Correct? | Kept? |
|---|---|---|
| Thm 3.4 claim E⁽¹⁾(A) ≠ E⁽¹⁾(B) for the 3×3 pair | **False**: both entropies are 0 (`corrector_A_checks.out.txt`). | No. Thm 3.6(a) of v3 now states E(A) = E(B) = 0. |
| "Perturbing the boundary values into heights (2, 2.2, 2.4) yields multiple bars" | **False**: a 3×3 grid has one interior cell, so β₁ ≤ 1. | No. Replaced by Remark 3.7(iii) of v3, which states the fact. |
| "E⁽¹⁾(A) = 0 by the empty-diagram convention" | True. | Content kept in Thm 3.6(a) of v3. |
| Šafránek article number 062320 | **Wrong**: that DOI is Gigena–Rossignoli. | No. The correct entry is 052320. |
| Thm 4.4(a) "closed level set … or under transformations preserving ∂Ω" | Imprecise. | No. The v2 wording was used, then corrected (v3 Prop. 4.4: the Möbius pole must lie off Σ). |
| §6.3 "tuple of d matrices (A₀,…,A_d)" and the sentence "τ_d computes the integer Brouwer degree" | Miscount; the claim is false (A4). | No. |
| Thm 7.2 without the independence hypothesis | **False**: the field ρ(x₁) gives Vol = 0 with ρ non-constant. | No. Replaced by the rank criterion, Thm 7.3 of v3. |
| Address "PPGEEAA/DES" | Outdated. | No. Replaced by the affiliation the author specified. |
| Abbreviated journal names; no DOIs | Formatting only. | No. The v2 form was used, then corrected. |

Nothing local-only was both correct and absent from v3.
