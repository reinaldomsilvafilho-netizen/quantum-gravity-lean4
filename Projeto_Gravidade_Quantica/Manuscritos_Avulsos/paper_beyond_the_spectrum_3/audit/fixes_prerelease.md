# Pre-release fixes: *Beyond the Spectrum III* (2026-10-07)

Independent corrector; did not write the text or the flags. These fixes go to the next re-check (four eyes).
Backup: `_arquivo/backup_tex_2026-10-07/Manuscritos_Avulsos/paper_beyond_the_spectrum_3/paper_beyond_the_spectrum_3_prerelease.tex` (line in `MANIFESTO.tsv`).

## 1. OBL-015 title (flag in `references_audit.md` §5.1)
- **Verified first.** Hayden–Lemm–Sorce, arXiv:2302.10208v2 (PRA 107, L050401), full text read (`Pesquisa_e_Testes/biblioteca/pdf/HaydenLemmSorce2023_arXiv2302.10208.pdf`). Thm 1: for every α ∈ (0,2) there is a classical state on C³⊗C³⊗C² with S_R^(α)(A:BC) < S_R^(α)(A:B); α = 1 is the reflected entropy. The flag is correct.
- The statement body already claimed only non-negativity, symmetry and S_R ≥ I. Only the title overclaimed.
- **Fix.** Title → "OBL-015: Canonical Purification, Symmetry and the Mutual-Information Bound for the Reflected Entropy". One sentence added at the end of the statement: no monotonicity is asserted, with the HLS counterexample (Thm 1).
- `LEDGER.md` heading of OBL-015 changed to match.

## 2. OBL-006 sign convention (flag §5.2)
- **Verified first.** Kashiwara, Astérisque 130 (1985) 193–209, full text from Numdam (`.../pdf/Kashiwara1985_Asterisque130.pdf`):
  - §2.1: T*X is oriented by (dθ)^n; §2.2 fixes the orientation of conormal cycles; Def. 3.4 defines SS(F) (the characteristic cycle);
  - Thm 4.2: if {x ∈ supp F : φ(x) ≤ t} and Y_φ ∩ SS(F) are compact, then χ(X;F) = (−1)^{n(n+1)/2} SS(F)·Y_φ, Y_φ = graph of dφ;
  - Ex. 8.5(i): the characteristic cycle of the constant sheaf on X is [T*_X X].
- The text wrote χ = CC·[T*_ΩΩ] with no sign and no orientation convention. With Kashiwara's conventions this is wrong by (−1)^{m(m+1)/2} (m = dim Ω); with an unstated convention it is ambiguous. The flag is correct.
- **Fix.** The theorem now fixes m = dim Ω, the orientation (dθ)^m and the conventions of Kashiwara §§2–3, and states χ = (−1)^{m(m+1)/2} CC·[T*_ΩΩ]. The proof cites Thm 4.2 with φ = 0 (Y_0 = zero section) and checks both hypotheses (compactness of Ω). KS Ch. IX is kept only as the book reference, with the remark that other orientation normalizations change the sign. I could not read KS Ch. IX (not accessible), so no theorem number or sign is attributed to it.
- **Consistency check (by hand, for the re-checker).** (dθ)^m = m! (−1)^{m(m+1)/2} dx₁…dx_m dξ₁…dξ_m: (−1)^m from dξ_i∧dx_i = −dx_i∧dξ_i and (−1)^{m(m−1)/2} from the reordering. The self-intersection of the zero section in the base-then-fibre orientation is the Euler number χ(Ω). Hence for the constant sheaf the right-hand side is χ(Ω). Remark `rem:chi_counterexample` uses only multiplicities, so it is unaffected.

## 3. Declarations
- "The Lean 4 files that accompanied earlier versions…" → "The Lean 4 files in the author's repository associated with this work are a placeholder skeleton without Mathlib and verify none of the statements." (house style rule 6).
- **Extra, not in the brief.** "Every reference was resolved through Crossref, DataCite or arXiv" was inaccurate. Three items have no DOI: Kashiwara 1985 (Numdam), Kawohl–Fridman 2003 (EuDML/DML-CZ) and DLMF (ISBN). These were checked against the `.tex` bibitems and `references_audit.md`. The sentence now names them.

## 4. CORRECTIONS_2026-10-06.md
- The bibliography count (72) and the remaining claims match the `.tex`. One line was appended for each fix above.

## Build
- pdflatex ×3 gives 0 errors, 0 warnings, 0 overfull, 0 underfull and 0 undefined references, in 16 pages.
- The .aux, .out and .toc files were deleted. The PDF was kept.
