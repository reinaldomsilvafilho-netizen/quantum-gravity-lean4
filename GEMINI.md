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

## How to write a proof (mandatory)
Use the template `Projeto_Gravidade_Quantica/_staging/MODELO_PROVA.md`. The minimum is:
1. **A precise statement.** Spaces, dimension, regularity (C², C^{1,1}, L^p), finite or infinite dimension, and what exactly is claimed. If any word is vague ("dominates", "tames", "absorbs"), it is not yet a statement.
2. **Numbered hypotheses.** Every step says which hypothesis it uses. At the end, list any hypothesis that went unused, which is a sign of an error or of an unnecessary hypothesis.
3. **Steps small enough that each one is either:**
   - an elementary calculation written out in full;
   - a **cited** theorem, with the exact statement, the source, and a **check that each of its hypotheses holds here**;
   - a lemma proved earlier in the same file.
4. **Test on the degenerate case first:** n = 1, finite dimension, zero curvature, U(1) instead of SU(N), and so on. If the argument does not work there, it does not work.
5. **Look for a counterexample before writing the proof.** Spend at least one attempt trying to refute the statement with a small example, numerical or symbolic.
6. **Close with an obstacle report:** the hardest step, what would falsify the statement, and what is missing to turn it into a theorem.

## Recurring errors (all occurred on 2026-09-29; do not repeat them)
- **Citing a theorem without checking its hypotheses.**
  - "Bonnet–Myers" was applied to CD(K,∞). It requires finite dimension N < ∞: the Gaussian measure is CD(1,∞) and is not compact.
  - "O'Neill gives negative curvature": the formula gives **non-negative** sectional curvature on the base of a Riemannian submersion.
  - Before citing, write the theorem out in full and check its hypotheses one by one.
- **Using chapters of the book as a magic argument.** "Monoidal coherence", "algebraic evasion", "the winding numbers of chapter 9", "Nash–Kuiper corrugations", "Fuller chattering in 2D". A chapter can be cited only for a **specific statement** of that chapter (theorem number), and only if its hypotheses hold in the new setting. Proof by analogy is not a proof.
- **Tests tuned to pass.** A parameter chosen so that the `assert` passes (e.g. γ⁴ = 3) proves nothing. The parameter must come from the theory or from data, and the test must also include a case where it **should** fail.
- **Toy models presented as evidence.** A Laplacian on an interval having a gap says nothing about Yang–Mills. A toy model shows only that the argument is not absurd in that case; say that explicitly.
- **Refutations with wrong arguments.** Refuting also needs rigour: "the Gribov region is a flat polytope" is false (it is convex and bounded, with a curved boundary). Check refutations as carefully as proofs.
- **Inflated words:** "rigorously", "exactly", "proves", "definitively", "annihilates". Remove them. The status goes in the label: proved / sketch / conjecture / refuted.

## Lessons from 2026-10-06 (full list in the `prova-rigorosa` skill)
- Copy the exact hypotheses and ranges of cited theorems from the source. Wrong intervals and wrong assumptions were the most common error that day.
- Never read a minimum, extremum or crossing time off a grid, and never conclude from one seed.
- Check that control data satisfy the null of a test. Estimated nuisance parameters break exact tests.
- Headings, abstracts and Zenodo descriptions are claims: three published works said "Lean verified" on their landing pages, which was false.
- Never send the author's e-mail to any API.

## Tools for checking (use them)
The full local toolbox installed on 2026-10-07 is listed in the "Local toolbox" section of the `prova-rigorosa` skill: HiGHS, SCIP, OR-Tools CP-SAT, CasADi/IPOPT, NLopt, PICOS/CVXOPT, cvxpy, Pyomo, POT, python-flint/Arb and z3, plus native GAP 4.16.1 (`bash /c/Users/monar/tools/rodar_gap.sh script.g`) and PARI/GP 2.19 (`/c/Users/monar/tools/pari/gp64-2-19-0.exe -q script.gp`). The smoke test is `Projeto_Gravidade_Quantica/_staging/teste_solvers.py`. An optimizer's answer is evidence, not proof: certify it exactly, in Arb, or with a checked dual.
- **sympy:** symbolic algebra and differentiation; check identities and first integrals.
- **mpmath:** high precision for asymptotics and constants.
- **Numerical integration of the actual equation** (scipy `solve_ivp`), not of a simplified version.
- **Brute-force counterexample search** in small dimension (random matrices 2×2, 3×3; small graphs).
- **Lean + Mathlib**, only for short lemmas and only if it compiles without `sorry`.

## Python technique (mandatory for every numerical claim)
Start from the template `Projeto_Gravidade_Quantica/_staging/MODELO_VERIFICACAO.py`.
- **A genuinely independent oracle.** Compute the same quantity by **another method**: closed form vs quadrature, sympy vs numerics, exact integers vs floating point, Monte Carlo vs exact enumeration. Rewriting the same formula in another way is not an oracle.
- **A negative control in every script.** A mutated formula (a sign or factor changed, a hypothesis removed) must fail. Also print the result of the control.
- **A convergence study.** Refine the grid, the tolerance or N at least 3 times and report the observed rate against the expected one. A single number at a single resolution proves nothing.
- **Precision.**
  - Use relative tolerances.
  - Use `mpmath` (mp.dps ≥ 30) for asymptotics, large factorials and Gamma functions.
  - Never infer "probability zero" from `exp(-x)` underflowing in float64: compute `log` instead.
- **Solve the real equation.** For ODEs, use `scipy.integrate.solve_ivp` with `rtol` and `atol` stated, and check a conserved quantity or a known solution. For linear algebra, use `scipy.linalg.eigh` on symmetric matrices, and check the residual ‖Av − λv‖.
- **Counterexample search.** Random matrices and parameters in small dimension, with a fixed seed. Report how many cases were tested and the worst case found.
- **Symbolic.** Use `sympy.simplify(expr_a - expr_b) == 0` to check identities and derivatives, before any numerics.
- **Reproducibility.**
  - Fixed seed, written at the top.
  - Save the output to `<script>.out.txt`.
  - `sys.exit(number_of_failures)`.
  - Scripts shorter than about 20 minutes (long runs in the background, in stages that save intermediate results).
- **Honest output.** Print numbers and `ok`/`FAIL` per check, never conclusions such as "PROVED" or "the mass gap exists". The conclusion goes in the `.md`, with its label.
- **Environment (Windows).** Save scripts to files (no heredocs). **Never** run `taskkill /IM python.exe`, which kills every Python process on the machine, including other agents' jobs; stop only your own process by its PID.

## References (mandatory; you invented 4 DOIs on 2026-10-01)
- **Never write a DOI from memory.** Every DOI goes through Crossref first: copy and adapt `Projeto_Gravidade_Quantica/_staging/check_dois_grafo.py` (resolves DOIs) and `find_dois_grafo.py` (searches by title). A DOI that does not resolve is removed and the reference is cited without one.
- Check the **title, authors and year** returned by Crossref against what you wrote.
- To cite a specific result, read the theorem in the text (the arXiv PDF in `Pesquisa_e_Testes/biblioteca/pdf/`, or download it). An abstract is not enough.

## Processes and memory (mandatory)
- A time limit on every run (≤ ~20 min); intermediate results saved to disk.
- Estimate memory before running (array size × 8 bytes); above ~2 GB, reduce the problem.
- Background job: write down the PID; **before finishing, wait for it or kill it by PID** (`Stop-Process -Id <PID>`). Never leave orphaned processes. Check with `python Projeto_Gravidade_Quantica/_staging/processos_orfaos.py`.
- Never `taskkill /IM python.exe`.

## Lessons from the 2026-09-29 to 10-01 sessions (do not repeat)
- **Inconsistent labels:** the SUMMARY said "proved" while the certificates themselves listed gaps. The status in the SUMMARY must be the **worst** status among the obligations. A certificate with an open gap is not "FINAL".
- **Trivial homotopies:** two operators can always be joined by a straight line, σ_τ = (1−τ)σ₀ + τσ₁. A relation between operators only has content if it **preserves a structure** (positivity, Markov property, spectrum, d_s) or is a limit theorem with hypotheses.
- **s → 0 is not the local limit:** the fractional operator tends to the identity as s → 0 (Maz'ya–Shaposhnikova); the Laplacian appears as s → 1 (Bourgain–Brezis–Mironescu).
- **Degeneration in long texts:** the "10×10 matrix" ended in repeated words. When a text becomes a list of adjectives with no formula, stop: it has no content.
- **Fragile tests:** an integral starting at k = 0.1 to hide a divergence, a finite grid hiding L^p = ∞, a series truncated at j = 200. The negative control must be capable of failing for the right reason.

## Techniques that worked in this project (use them as models)
- **Computer-assisted proof with interval arithmetic:** reduce the statement to a positivity inequality on a compact interval, cover it with cells, certify each cell with `python-flint` (Arb) plus a Lipschitz bound between cells, and handle the tails analytically. Model: `Pesquisa_e_Testes/operadores_fracionarios/F6_pontual_d12/` (Theorem B1).
- **Adversarial search** (optimization, not random sampling): parametrize the family (atoms, weights, scales), maximize the violation with multiple starts, and certify any candidate in high precision. Model: `F5_levy_nogo/`, `F8_B_d2/`.
- **Exact reductions before attacking:** symmetrization (Steiner), dilation (ξ = nη), first integrals (Noether). Models: `F8_B_d2/`, `fluxo_minimax_curvatura/scripts/first_integral.py`.
- **Two independent oracles + a convergence study:** closed form vs quadrature vs exact integers; a refinement table with the observed rate.

## Rules specific to this model
- Do not re-introduce statements the audit already refuted. WORKPLAN §3 lists them. Examples:
  - an unconditional Yang–Mills gap;
  - the "Born rule" as a volume in CPᴺ;
  - vacuum-energy "cancellation" by ∂∂ = 0;
  - the Koide "derivation";
  - Nash–Kuiper corrugations under an L∞ bound on the second fundamental form;
  - winding numbers inside a convex region;
  - the graphon Ricci flow with sign −2κW;
  - the isotropic k² + ℓ²k⁴ symbol as ghost-free in Lorentzian signature;
  - negative curvature of the orbit space 𝒜/𝒢 "by O'Neill" (the formula gives ≥ 0);
  - Bonnet–Myers / compactness from CD(K,∞) (needs N < ∞);
  - the Gribov region as a "flat polytope" (it is convex and bounded, with a curved boundary);
  - the Yang–Mills mass gap "proved" via toy models, monoidal categories or fractals (see `_staging/gemini-2026-09-29/SUMMARY.md`).
- **Prior art.** The d_s(τ) erfc closed form is due to Sotiriou–Visser–Weinfurtner (2011). Check the literature before any novelty claim.
- **Physical predictions.** With ℓ* = ℓ_P, the effects are unobservable. Any claim of a testable prediction must state the scale used and the current experimental bound.
- **Honest labels.** Nothing you write is a "retrodiction" or "prediction" unless you count the free parameters and the observables. A quantity used as input does not count.
- **Environment.** Windows. Edit LaTeX with a proper editor or with scripts saved to files, not through shell heredocs.
