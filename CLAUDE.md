# Project hand-off: Geometry, Tensors, and Quantum Gravity

Compact state for any model continuing this project. Read this first, then `Projeto_Gravidade_Quantica/AGENT_PROTOCOL.md` (token economy, model routing, prompt templates) and `Projeto_Gravidade_Quantica/unified_quantum_gravity_book/WORKPLAN.md` (§3 findings, §9 diary).

## What this is
- **Author:** Reinaldo M. Silva-Filho, master's student, PPGEE/DES, UFLA (CAPES, Finance Code 001). He works alone and publishes frequently on Zenodo. He writes in Portuguese; answer him in Portuguese.
- **Main work:** a 13-chapter monograph that mixes proved mathematics (Parts I–III) with conjectures on emergent spacetime (Parts IV–V).
- **Companion papers:** Simplicial QG on Δ₄×Δ₂, a conditional Yang–Mills result, and an S₃-circulant fermion-mass parametrization.
- **Zenodo concept DOIs:**
  - book 10.5281/zenodo.22290043
  - Simplicial QG 22704111
  - Yang–Mills 22301093
  - fermion masses 22373916
  - *Beyond the Spectrum* 22644743 (not audited)
  - cobordisms 22441676 (not audited)
- **GitHub:** `origin` = quantum-gravity-lean4 (branch `main`). It holds sources, audit records and scripts. PDFs go to Zenodo only.

## Where things are (`Projeto_Gravidade_Quantica/`)
- `unified_quantum_gravity_book/`:
  - `chapNN_*.tex`, the dictionary, `master_book_unified_quantum_gravity.tex`, `declarations_chapter.tex`
  - `WORKPLAN.md`: status register, the single source of truth
  - `CHANGELOG.md`
  - `verify_chapNN_numerical.py`
- `…/audit/`:
  - `chNN_claims.md`: ledgers
  - `verify/PROTOCOL.md`: audit protocol
  - `verify/chNN_blind.md`: blind referee reports
  - `verify/fixes_*.md`: correction logs
  - `verify/L2_*.md`: re-checks
  - `scripts/` and `verify/scripts/`: independent checks
- `submission_package_jhep_scipost/`, `Manuscritos_Avulsos/`: companion papers, each with `CORRECTIONS_2026-09-25.md`.
- `build_pdfs_safe.py`: compiles everything and replaces a PDF only on success.
- `zenodo_upload_AAAA-MM-DD/`: release bundle (PDFs, notes, descriptions).
- The author's Claude Docs:
  - *Árvore de Conjecturas*: open conjectures, proof routes, relevance
  - *Guia do Projeto*: full workflow, gates, stop criteria

## Non-negotiable conventions
1. **Four eyes.** Whoever writes a proof or a correction never verifies it. Status "verificado" requires a blind referee report (layer 1), an independent correction, and a targeted re-check (layer 2).
2. **Honest labels.** "Theorem" means a complete proof. Otherwise the label is conjecture, heuristic, or a cited classical result. Abstracts and conclusions claim only what the body proves.
3. **Numerics.** Every check uses an independent oracle plus a negative control: a mutated formula that must fail. Never "expected = computed".
4. **Physics.** Every physical number gets a dimensional check and an order-of-magnitude estimate (CODATA).
5. **Lean.** Only Mathlib statements without `sorry` or `axiom` count. The current `formal_proofs_*` files are a Bool-placeholder skeleton that verifies nothing. Never claim otherwise.
6. **House style.** Chapters state only current mathematics: no "earlier version", "withdrawn", "corrected", and no `audit/` paths. History goes to CHANGELOG, Zenodo notes and audit files. A failed claim becomes a neutral remark with its counterexample.
7. **References.** Every DOI is resolved via Crossref or DataCite. Attributions are checked against the paper, not only the abstract.
8. **Build gate.** 0 errors, 0 warnings, 0 overfull boxes, 0 undefined references.
9. **Environment.** Edit LaTeX with the Edit tool or saved scripts; Git Bash heredocs eat `\\`. Avoid parentheses in shell arguments, because a cmd.exe hook breaks them. Update statuses with `audit/scripts/update_workplan_status.py`, which rejects duplicate IDs.

## Current status (2026-09-26)
- **Audit coverage:** all 13 chapters and 3 companion papers are audited. Chapters 1–13 are corrected and have had layer-2 re-checks.
- **Findings:** 21 are verified in WORKPLAN.
- **Build:** clean; the master volume has 191 pages.
- **Release:** v2.3 is bundled in `zenodo_upload_2026-09-26/` and pushed to GitHub (commit 45a2dbc).
- **Key facts to keep straight:**
  - The d_s(τ) erfc closed form is prior art: Sotiriou–Visser–Weinfurtner, PRD 84 (2011) 104018.
  - Observational effects are 10⁵⁶ times or more below reach.
  - The Yang–Mills result is conditional only.
  - A circulant flavour ansatz gives a trivial CKM matrix.

## Next steps
1. **Phase 1 (close errors):**
   - layer-2 check of the final integration pass (F-46/47/48/50/51, F-20);
   - second check of the three papers;
   - Python checks for ch. 1–11 (F-02);
   - Lean clean-up (F-01, F-24);
   - single-source build (F-19);
   - author confirmation of the AI/conflict declarations (F-21, F-29);
   - audit of *Beyond the Spectrum* and the cobordism paper.
2. **Phase 2 (research cycle per conjecture):** choose → literature → formulate → Python → prove → Lean → adversarial → integrate and publish. Suggested order:
   1. continuous Dixon for integer x, via Poisson summation plus contour shift (I₃/I₁ ≈ e^{−3x} numerically);
   2. regularity invariance for curves;
   3. Γ-convergence of the discretization;
   4. planar relativistic slingshot.

   Physics conjectures (cMERA metric, RT via MCF, graphon condensation, Kac–Rice horizon entropy, Jordan loops) first need precise definitions.
3. **Stop criteria:** solution, refutation, or a documented plateau. A plateau requires 3 routes tried, the literature confirming the problem is open, the obstacle stated precisely, and a weaker case proved.
