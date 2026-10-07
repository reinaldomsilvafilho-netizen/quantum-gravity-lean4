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
  controls) is in [`../../../../formal_proofs_mathlib/`](../../../../formal_proofs_mathlib/). Only the statements listed in its `README.md` are machine-checked.

The files are kept for transparency, because earlier Zenodo versions referred to them.

## This folder

Audit copy of the Lean archive attached to an earlier Zenodo version of *Beyond the Spectrum*. It does not
use Mathlib. The "theorems" are field projections or arithmetic in `Nat`/`Int`. For example,
`wasserstein_w2_identity` proves `cost = 0 → wasserstein_distance_sq cost = 0`.
