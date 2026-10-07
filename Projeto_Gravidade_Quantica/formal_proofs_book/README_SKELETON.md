# NAMING SKELETON: THIS LEAN CODE VERIFIES NO MATHEMATICS

**Read this before citing anything in this folder.**

- These files are a **naming skeleton**. The results of the text are recorded as named Lean structures and
  "theorems" whose content is a Bool, Float or Nat placeholder, a field projection (the hypothesis *is* the
  conclusion) or toy arithmetic on `Nat`/`Int`/`List`.
- They **verify no mathematical content** of the monograph or of the papers. A successful `lake build` here
  only shows that the files type-check.
- Statements such as "PROVEN", "Certified", "100% PASS", "0 sorry" or "N/N obligations" printed by a
  `Main.lean` or written in comments do **not** measure mathematical verification.
- The genuine formalization (Lean 4 + Mathlib, no `sorry`, no `axiom`, with `#print axioms` and negative
  controls) is in [`../formal_proofs_mathlib/`](../formal_proofs_mathlib/). Only the statements listed in its `README.md` are machine-checked.

The files are kept for transparency, because earlier Zenodo versions referred to them.

## This folder

- `Book/Chap01`–`Chap13`, `ChapFermionHierarchy`, `ChapLinearAlgebra` and `ChapUniverseLagrangian` do not
  import Mathlib. Their structures carry 271 Bool/Float fields, and each "theorem" returns one of them.
- `BookReal/Chap01/FunctionalRealizationsReal.lean` imports Mathlib and contains exactly two genuine but
  trivial lemmas:
  - `perm_preserves_frob_norm`: `x₁² + x₂² = x₂² + x₁²` for reals (commutativity of addition);
  - `dirichlet_energy_nonneg`: `(x₁ − x₂)² ≥ 0`.

  They are correct and free of `sorry`/`axiom`, but they do not formalize any theorem of Chapter 1. In
  particular they are **not** the "Spectral Blindness" theorem, despite a comment in that file. `BookReal`
  is not published and is not part of the Lean code that counts.
- The constraint bounds of Chapter 12 and the Chapter 3 results that are actually formalized are in
  `../formal_proofs_mathlib/`.
