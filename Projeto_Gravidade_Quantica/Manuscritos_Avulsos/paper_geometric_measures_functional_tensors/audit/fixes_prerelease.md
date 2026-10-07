# Pre-release fixes: *Beyond the Spectrum II* (2026-10-07)

Independent corrector. These fixes go to the next re-check.
Backup: `_arquivo/backup_tex_2026-10-07/Manuscritos_Avulsos/paper_geometric_measures_functional_tensors/paper_geometric_measures_functional_tensors_prerelease.tex` (line in `MANIFESTO.tsv`).

1. **Declarations, Lean.** Flag §5.1 confirmed. "…files that accompanied earlier versions…" → "The Lean 4 files in the author's repository associated with this work are a placeholder skeleton without Mathlib and verify none of the statements."
2. **Volume I citation.** Flag §5.2 confirmed: DataCite returns the title "Beyond the Spectrum: The Complete Three-Volume Monograph…" for 10.5281/zenodo.22644743. The bibitem `silvafilho2026beyond` now reads "Volume I of *Beyond the Spectrum*, Zenodo 10.5281/zenodo.22644743, 2026; this Zenodo record holds all three volumes of the series."
3. **"Every reference" sentence.** Flag §5.3 confirmed: `connes1994noncommutative` is ISBN-only (Open Library), and it is the only entry with neither a DOI nor an arXiv id. The sentence now says "…or, for the one book without a DOI, through its ISBN record at Open Library."
4. **CORRECTIONS_2026-10-06.md.**
   - The counts check out: 23 → 68 bibitems.
   - One line was appended for each fix.
   - Nothing there claims a step that was not done. The audit itself still lists six sources as unchecked in full text, and CORRECTIONS does not claim otherwise.
5. **Build.** pdflatex ×3 gives 0 errors, 0 warnings, 0 overfull, 0 underfull and 0 undefined references, in 21 pages. The .aux, .out and .toc files were deleted.
