# Layer-2b targeted re-check: L2 B items (*Beyond the Spectrum*, Vol. I)

- **Checker:** independent session (Claude Opus), 2026-10-06. I wrote neither the volume, the audits nor the fixes.
- **Inputs:**
  - `L2_layer2.md`, items A5 heading, residual headings, Declarations and CORRECTIONS;
  - `fixes_layer1.md`, sections "Declarations" and "L2 B items";
  - the current `.tex` and `CORRECTIONS_2026-10-06.md`;
  - `_staging/DECLARACOES_PADRAO_ARTIGOS.tex`.
- **Scripts:**
  - `scripts/L2b_headings.py` → `.out.txt`: 9 checks, **0 failures**. The oracles are a brute-force cut norm over unions of cells, eigen-decomposition with the projected Hessian, and a direct cell-boundary perimeter. Each check has a negative control.
  - `scripts/L2b_build.py` → `L2b_build.out.txt`.
- No background jobs. `processos_orfaos.py`: 0 suspects.

## Items

| Item | Verdict | Evidence |
|---|---|---|
| **§4 heading** "Emerging Invariants: Order-Sensitive Quantities" | **PROBLEMA (B)** | It is accurate for §4.1 and §4.2: the Dirichlet energy and the TV change under A ↦ PAPᵀ (1066 vs 1144; 8.5 vs 6.5). It is **not** accurate for §4.3 or §4.4:<br>• **§4.3:** f_{PAPᵀ}(x) = f_A(Pᵀx), so the critical values and Morse indices are identical; they are spectral.<br>• **§4.4:** W_{PAPᵀ} = W_A^ψ for the interval permutation ψ, so δ_□ = 0; graphon distances are permutation-invariant by design.<br>Checked numerically, with a control: the plain cut norm ‖W_A − W_B‖_□ = 0.078 > 0.<br>**Related, and more important (M):** abstract ¶2 says the realizations "produce quantities that are not functions of the spectrum or of other permutation-invariant data", and its list includes "(iii) Morse indices … and the Euler characteristic of spheres; and (iv) the cut-norm topology of graphons". By Thm 4.7(ii) (index of ±v_i = i−1) and by the definition of δ_□ in Thm 4.11, (iii) and (iv) *are* permutation-invariant. The L2 report marked the abstract CONFIRMA, but this sentence overclaims against the body (house rule 2).<br>**Fix:** restrict the claim to (i) and (ii), and present (iii) and (iv) as further geometric or topological readings; rename §4, e.g. "Emerging Invariants: Spatial, Topological and Asymptotic Quantities". |
| **§6.4 heading** "Computational Multilinear Algebra: The De Silva–Lim Pathology in the Rank-One Case" | **PROBLEMA (cosmetic)** | The body is correct: the rank-one problem is well posed, and the pathology persists for r ≥ 2. But the heading reads as if the pathology occurred in the rank-one case, where it does not. **Fix:** e.g. "Best Rank-One Approximation and the De Silva–Lim Pathology", the wording proposed in L2. |
| **§6.5 heading** "Biomedical Imaging: Hausdorff Perimeters of Level Sets" | **CONFIRMA** | It no longer says "minimal surface". The body uses superlevel sets, and "level sets" is an acceptable loose heading. |
| **§6.5 "reduced boundaries" wording vs Thm 4.6** | **CONFIRMA (text); one cosmetic display issue** | The prose "reduced boundaries of the superlevel sets" matches Thm 4.6 (∂*E_t, De Giorgi).<br>**Display issue:** the §6.5 display writes H¹(∂*{W_A>t}) without "∩ (0,1)²", while Thm 4.6 has it. Read literally in R², the outer square boundary is added. For t < min A that adds 4 per unit t, so the integral over R diverges: on a finite t-window the value is 21.0 against TV = 8.5. The Thm 4.6 reading equals the TV formula (8.5 = 8.5). **Fix:** add "∩ (0,1)²". |
| **Lean sentence** | **CONFIRMA** | "The Lean 4 files that accompanied earlier versions are a placeholder skeleton without Mathlib and verify none of the statements here." This is accurate: the Lean files were in the Zenodo v1/v2 zip, and the repository holds none for this volume. It is the standard wording ("statements here" instead of "mathematics"; immaterial). "earlier versions" is close to house rule 6, as in the standard block. |
| **Declarations block** | **CONFIRMA** | Funding, competing interests, AI use (with "volume") and code availability equal the standard, modulo line breaks. The Verification-status paragraph is the corrector's longer version, kept by author decision (`fixes_layer1.md`). It is accurate, and it contains the standard Lean sentence. The appended Zenodo DOI and licence line is fine. **Cosmetic:** this paragraph says "paper" while the AI paragraph says "volume". |
| **`CORRECTIONS_2026-10-06.md`** | **CONFIRMA, one consequential note** | The three L2 issues are fixed:<br>• no repository claim;<br>• "every item checked before any change, the numerical ones with new scripts";<br>• no "layer 2 not done".<br>No "pending". The theorem and section numbers match the `.aux`: Constr. 3.7, Thm 4.1, 4.5, 4.7, 4.10, 4.11, Rem. 5.2, 5.5, 5.9, Prop. 5.6, Thm 5.7, 5.8.<br>**Note:** it quotes the §4 and §6.4 headings and says the abstract claims "only what is proved"; both change if the §4/abstract fix above is made.<br>**Not verified:** "Volumes II and III: corrected separately in the same release". This is outside my inputs. |

## Build

`audit/L2b_build/`, pdflatex ×3:
- every run exited with code 0;
- 0 errors, 0 LaTeX/Package/Class warnings, 0 overfull boxes, 0 underfull boxes, 0 undefined references;
- 21 pages.

As in L2, the log has 3 benign lines "pdfTeX warning (font expansion): font should be expanded before its first use", from microtype with cm-super. The project gate does not count them.

## Close

- **Hardest step:** deciding whether "order-sensitive" fits §4.3 and §4.4. It does not, by an explicit invariance argument plus a numerical check.
- **Must fix before release:**
  - the abstract (iii)/(iv) sentence (M);
  - the §4 heading (B).
- **Cosmetic:** the §6.4 heading and the §6.5 display ∩ (0,1)².
