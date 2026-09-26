# Geometry, Tensors, and Quantum Gravity
## Companion repository: numerical checks and Lean 4 material

[![Zenodo: Monograph](https://zenodo.org/badge/DOI/10.5281/zenodo.22290043.svg)](https://doi.org/10.5281/zenodo.22290043)
[![Lean 4](https://img.shields.io/badge/Lean_4-v4.33.1-blue.svg)](https://github.com/leanprover/lean4)
[![Formalization](https://img.shields.io/badge/Formalization-in%20progress%20%28not%20verified%29-orange.svg)](#status-of-the-lean-4-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Author:** Reinaldo Maia Silva-Filho
**Affiliation:** Master's student, Postgraduate Program in Statistics and Agricultural Experimentation (PPGEE/DES), Federal University of Lavras (UFLA), Lavras, MG, Brazil
**E-mail:** `reinaldo.filho1@estudante.ufla.br` | **ORCID:** [0009-0003-8068-3330](https://orcid.org/0009-0003-8068-3330)
**Funding:** CAPES, Finance Code 001

---

## About

This repository accompanies a research monograph and several companion papers archived on Zenodo. It contains:
- the LaTeX sources;
- the records of an independent audit of the whole text;
- the Python scripts used to check formulas and numbers;
- Lean 4 files that are an early, incomplete step towards a formalization.

This is ongoing work by a single author. Comments, criticism and corrections are welcome and will be credited.

## Current status (26 September 2026)

All 13 chapters of the monograph and three companion papers have been through an independent audit, carried out in three steps:

1. **Blind referee review.** A referee who did not write the text checks every theorem, proposition and numerical claim. The referee has not seen earlier reviews.
2. **Separate correction.** A different pass corrects what the referee found.
3. **Targeted re-check.** Each correction is checked again.

The protocol is in [`audit/verify/PROTOCOL.md`](Projeto_Gravidade_Quantica/unified_quantum_gravity_book/audit/verify/PROTOCOL.md). The status of every finding is tracked in [`WORKPLAN.md`](Projeto_Gravidade_Quantica/unified_quantum_gravity_book/WORKPLAN.md).

Outcomes:

- **Errors in earlier versions.** Several statements were **wrong**. They have been corrected or withdrawn, and others are now labelled as conjectures. The corrected versions are released as new Zenodo versions. Each carries a note listing what changed and what still needs updating.
- **New proofs.** The audit also produced new proofs. Examples: the asymptotics of continuous multinomial integrals, an inversion formula for the Radon–Beta transform, and U-turn curvature bounds in constant-curvature spaces.
- **Yang–Mills.** **None of the papers claims a solution of the Yang–Mills mass-gap problem.** The Yang–Mills paper states a *conditional* result: a gap follows from hypotheses that are not established.
- **Lean 4.** **The Lean 4 code does not verify the mathematics** (see below).

## Works

| Work | Zenodo (concept DOI, always the latest version) | Status |
|---|---|---|
| *Geometry, Tensors, and Quantum Gravity* (monograph, 13 chapters) | [10.5281/zenodo.22290043](https://doi.org/10.5281/zenodo.22290043) | Audited and corrected (September 2026); final consistency pass awaiting re-check |
| *Simplicial Quantum Gravity on Δ₄ × Δ₂* (companion paper) | [10.5281/zenodo.22704111](https://doi.org/10.5281/zenodo.22704111) | Corrected against the monograph; second check pending |
| *A Geometric and Metric-Measure Framework for the Yang–Mills Mass Gap* | [10.5281/zenodo.22301093](https://doi.org/10.5281/zenodo.22301093) | Corrected: conditional result only; second check pending |
| *An S₃-Circulant Parametrization of Fermion Masses and Mixing* | [10.5281/zenodo.22373916](https://doi.org/10.5281/zenodo.22373916) | Corrected: fits and relations with an explicit parameter count; second check pending |
| *Beyond the Spectrum* (three-volume monograph) | [10.5281/zenodo.22644743](https://doi.org/10.5281/zenodo.22644743) | Not yet audited |
| *A Functorial Bridge from Continuous Tensor Manifolds to 4-Dimensional Spacetime Cobordisms* | [10.5281/zenodo.22441676](https://doi.org/10.5281/zenodo.22441676) | Not yet audited |

[All records by the author on Zenodo](https://zenodo.org/search?q=metadata.creators.person_or_org.name:%22Silva-Filho,+Reinaldo+M.%22)

## Repository contents

| Folder | Content |
|---|---|
| [`Projeto_Gravidade_Quantica/unified_quantum_gravity_book/`](Projeto_Gravidade_Quantica/unified_quantum_gravity_book/) | LaTeX sources of the 13 chapters, the dictionary and the master volume; `verify_chapXX_numerical.py`; `CHANGELOG.md`; `WORKPLAN.md` (register of every finding and its status) |
| [`…/unified_quantum_gravity_book/audit/`](Projeto_Gravidade_Quantica/unified_quantum_gravity_book/audit/) | Audit records: per-chapter claim ledgers, blind referee reports and correction logs (`audit/verify/`), and the scripts used as independent checks |
| [`Projeto_Gravidade_Quantica/submission_package_jhep_scipost/`](Projeto_Gravidade_Quantica/submission_package_jhep_scipost/) | LaTeX source, corrections note and check scripts of *Simplicial Quantum Gravity on Δ₄ × Δ₂* |
| [`Projeto_Gravidade_Quantica/Manuscritos_Avulsos/`](Projeto_Gravidade_Quantica/Manuscritos_Avulsos/) | LaTeX sources, corrections notes and check scripts of the Yang–Mills and fermion-mass papers |
| [`Projeto_Gravidade_Quantica/formal_proofs_book/`](Projeto_Gravidade_Quantica/formal_proofs_book/) | Lean 4 files named after the monograph chapters (naming skeleton, see below) |
| [`Projeto_Gravidade_Quantica/formal_proofs_lean4/`](Projeto_Gravidade_Quantica/formal_proofs_lean4/) | Lean 4 files for the functorial-cobordism paper (same status) |
| [`Projeto_Gravidade_Quantica/Manuscritos_Avulsos/paper_yang_mills_mass_gap/`](Projeto_Gravidade_Quantica/Manuscritos_Avulsos/paper_yang_mills_mass_gap/) | Numerical scripts and Lean 4 files for the Yang–Mills paper (same status) |

### What still needs updating

- **Lean 4.** The files remain a skeleton. A real formalization in Mathlib is not started beyond a few lemmas, and `formal_proofs_lean4/SpectralDimension.lean` states a formula that differs from the monograph.
- **Python checks for chapters 1–11.** These scripts predate the audit and do not yet follow the independent-oracle standard. The checks used during the audit are in `audit/scripts/` and `audit/verify/scripts/`.
- **Final consistency check.** The last integration pass (titles, cross-references, notation) has not yet had its own independent re-check.
- **Build.** The master volume is still assembled from per-chapter PDFs rather than compiled from a single source.
- **Other works.** *Beyond the Spectrum* and the functorial-cobordism paper have not been audited.
- **Open conjectures.** They are listed, with suggested proof strategies, in the monograph and in `WORKPLAN.md`.

## Status of the Lean 4 code

The Lean 4 files in this repository **do not verify the mathematics of the monograph or the papers**:

- They do not import Mathlib.
- Most "theorems" are fields of a `structure` returned as the conclusion: the hypothesis *is* the statement, so the "proof" is trivial and says nothing about the mathematics.
- Counts such as "N/N obligations" or "0 sorry" in earlier versions of this README did not measure mathematical verification. They have been removed.

The files are a naming skeleton for a future formalization. A genuine formalization, with statements in Mathlib and no `sorry` or `axiom`, has started for a few elementary lemmas. It will be reported result by result, with a table linking each formalized statement to the corresponding result in the text.

## Status of the Python scripts

The scripts check formulas and numbers. For chapters 12 and 13 they were rewritten so that every check compares against an independent computation (for example, a closed form against numerical quadrature) and includes a negative control, a deliberately altered formula that must fail. The scripts for chapters 1–11 are still being revised to this standard. Until then, treat a passing run as a consistency check only.

## Running the checks

Requirements: Python 3.10+ with `numpy`, `scipy`, `sympy` and `mpmath`. Lean 4 is optional (via `elan`; toolchain `v4.33.1`).

```bash
cd Projeto_Gravidade_Quantica/unified_quantum_gravity_book
python verify_chap12_numerical.py
python verify_chap13_numerical.py
python audit/verify/scripts/L2_ch03_laplace_rays_table.py   # example of an audit check
```

Each audit script compares a claim against an independent computation. It also runs a negative control: a deliberately altered formula that must fail the check.

To rebuild the PDFs you need a LaTeX distribution with `pdflatex`. Run `python Projeto_Gravidade_Quantica/build_pdfs_safe.py`. It compiles every chapter, the dictionary, the master volume and the three papers, and it replaces a PDF only if the compilation succeeds.

The Lean projects can be built with `lake build` inside each Lean folder. A successful build shows that the files type-check. For the reasons above, it does not show that the mathematics is correct.

## License

The code in this repository is released under the MIT License. The monograph and papers on Zenodo are released under CC BY 4.0.
