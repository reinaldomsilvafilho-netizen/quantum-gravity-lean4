# Gemini rules for this project (Geometry, Tensors, and Quantum Gravity)

Read first, in this order:
1. `CLAUDE.md`: project state, conventions, next steps.
2. `Projeto_Gravidade_Quantica/unified_quantum_gravity_book/WORKPLAN.md`: §3 findings and their status, §9 diary.
3. `Projeto_Gravidade_Quantica/ORGANIZACAO_E_VERSOES.md`: folders, versions, archive.
The book chapters (`chapNN_*.tex`) are the source of truth. The previous audit found many errors produced by AI tools, including earlier Gemini sessions, so treat anything you produce as a draft.

## Where you may write
- **Only** in `Projeto_Gravidade_Quantica/_staging/gemini-AAAA-MM-DD/` (create it with today's date), or on a git branch `tool/gemini-AAAA-MM-DD`.
- **Never** edit the canonical chapters, `WORKPLAN.md`, `CHANGELOG.md`, `README.md`, `CLAUDE.md`, the papers in `Manuscritos_Avulsos/` or `submission_package_jhep_scipost/`, or anything in `releases/` or `_arquivo/`.
- **Never** commit to `main`, push, or upload to Zenodo.

Your work enters the book only after the author asks Claude to audit it: a blind referee, an independent correction, then a re-check (`audit/verify/PROTOCOL.md`).

## What a session must produce
In the staging folder:
- one `.md` or `.tex` file per topic, updated in place (no `_v2` or `_final` copies);
- a Python script for every numerical claim, with an independent oracle and a negative control;
- a `SUMMARY.md` written at the end of the session, with a table: claim | status (**proved / proof sketch / conjecture / numerical only / refuted**) | hypotheses | file | what needs independent checking.

## Rules specific to this model
- Do not re-introduce statements the audit already refuted. WORKPLAN §3 lists them. Examples:
  - an unconditional Yang–Mills gap;
  - the "Born rule" as a volume in CPᴺ;
  - vacuum-energy "cancellation" by ∂∂ = 0;
  - the Koide "derivation";
  - Nash–Kuiper corrugations under an L∞ bound on the second fundamental form;
  - winding numbers inside a convex region;
  - the graphon Ricci flow with sign −2κW;
  - the isotropic k² + ℓ²k⁴ symbol as ghost-free in Lorentzian signature.
- **Prior art.** The d_s(τ) erfc closed form is due to Sotiriou–Visser–Weinfurtner (2011). Check the literature before any novelty claim.
- **Physical predictions.** With ℓ* = ℓ_P, the effects are unobservable. Any claim of a testable prediction must state the scale used and the current experimental bound.
- **Honest labels.** Nothing you write is a "retrodiction" or "prediction" unless you count the free parameters and the observables. A quantity used as input does not count.
- **Environment.** Windows. Edit LaTeX with a proper editor or with scripts saved to files, not through shell heredocs.
