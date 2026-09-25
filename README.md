# Geometry, Tensors, and Quantum Gravity
## Companion repository: numerical checks and Lean 4 material

[![Zenodo: Monograph](https://zenodo.org/badge/DOI/10.5281/zenodo.22290043.svg)](https://doi.org/10.5281/zenodo.22290043)
[![Lean 4](https://img.shields.io/badge/Lean_4-v4.33.1-blue.svg)](https://github.com/leanprover/lean4)
[![Formalization](https://img.shields.io/badge/Formalization-in%20progress%20%28not%20verified%29-orange.svg)](#status-of-the-lean-4-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Author:** Reinaldo Maia Silva-Filho
**Affiliation:** Graduate Program in Statistics and Agricultural Experimentation (PPGEE/DES), Federal University of Lavras (UFLA), Lavras, MG, Brazil
**E-mail:** `reinaldo.filho1@estudante.ufla.br` | **ORCID:** [0009-0003-8068-3330](https://orcid.org/0009-0003-8068-3330)
**Funding:** CAPES, Finance Code 001

---

## About

This repository accompanies a research monograph and several companion papers archived on Zenodo. It contains the Python scripts used to check formulas and numbers in the monograph and Lean 4 files that are an early, incomplete step towards a formalization.

This is ongoing work by a single author. Comments, criticism and corrections are welcome and will be credited.

## Current status (September 2026)

The monograph and the companion papers are being revised after an independent audit. Every theorem, proposition and numerical claim is re-checked by a referee that did not write the text. Corrections are then made in a separate pass, and each correction is checked again. As a result:

- Several statements in earlier versions were **wrong** and are being corrected or withdrawn. Others turned out to be conjectures and are now labelled as such.
- **None of the papers claims a solution of the Yang–Mills mass-gap problem.** The corrected Yang–Mills paper states a *conditional* result: a gap follows from hypotheses that are not established.
- **The Lean 4 code does not verify the mathematics** (see below).
- The corrected versions will be uploaded to Zenodo as new versions of the same records. The Zenodo *concept* DOIs below always resolve to the latest version. Each new version will carry a note listing what changed.

## Works

| Work | Zenodo (concept DOI, always the latest version) | Status |
|---|---|---|
| *Geometry, Tensors, and Quantum Gravity* (monograph, 13 chapters) | [10.5281/zenodo.22290043](https://doi.org/10.5281/zenodo.22290043) | Under revision; all 13 chapters audited, corrections being verified |
| *Simplicial Quantum Gravity on Δ₄ × Δ₂* (companion paper) | [10.5281/zenodo.22704111](https://doi.org/10.5281/zenodo.22704111) | Corrected against the monograph; new version pending |
| *A Geometric and Metric-Measure Framework for the Yang–Mills Mass Gap* | [10.5281/zenodo.22301093](https://doi.org/10.5281/zenodo.22301093) | Corrected: conditional result only; new version pending |
| *An S₃-Circulant Parametrization of Fermion Masses and Mixing* | [10.5281/zenodo.22373916](https://doi.org/10.5281/zenodo.22373916) | Corrected: fits and relations with an explicit parameter count; new version pending |
| *Beyond the Spectrum* (three-volume monograph) | [10.5281/zenodo.22644743](https://doi.org/10.5281/zenodo.22644743) | Not yet audited |
| *A Functorial Bridge from Continuous Tensor Manifolds to 4-Dimensional Spacetime Cobordisms* | [10.5281/zenodo.22441676](https://doi.org/10.5281/zenodo.22441676) | Not yet audited |

[All records by the author on Zenodo](https://zenodo.org/search?q=metadata.creators.person_or_org.name:%22Silva-Filho,+Reinaldo+M.%22)

## Repository contents

| Folder | Content |
|---|---|
| [`Projeto_Gravidade_Quantica/unified_quantum_gravity_book/`](Projeto_Gravidade_Quantica/unified_quantum_gravity_book/) | `verify_chapXX_numerical.py`: numerical checks for chapters 1–13 of the monograph |
| [`Projeto_Gravidade_Quantica/formal_proofs_book/`](Projeto_Gravidade_Quantica/formal_proofs_book/) | Lean 4 files named after the monograph chapters (naming skeleton, see below) |
| [`Projeto_Gravidade_Quantica/formal_proofs_lean4/`](Projeto_Gravidade_Quantica/formal_proofs_lean4/) | Lean 4 files for the functorial-cobordism paper (same status) |
| [`Projeto_Gravidade_Quantica/paper_yang_mills_mass_gap/`](Projeto_Gravidade_Quantica/paper_yang_mills_mass_gap/) | Numerical scripts and Lean 4 files for the Yang–Mills paper (same status) |

The LaTeX sources, the audit records (findings, referee reports, correction logs) and the scripts used in the audit are not yet in this repository. They will be added with the next release.

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
```

The Lean projects can be built with `lake build` inside each Lean folder. A successful build shows that the files type-check. For the reasons above, it does not show that the mathematics is correct.

## License

The code in this repository is released under the MIT License. The monograph and papers on Zenodo are released under CC BY 4.0.
