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

Lean skeleton for the paper *Quantum Fisher Geometry of Continuous Matrix Product State Fields and
Lorentzian Cylinders* (formerly *A Functorial Bridge*, Zenodo 10.5281/zenodo.22441676). It does not use
Mathlib.
- The geometric objects (`AbstractMetric`, `LorentzianMetric`, the ADM and Einstein predicates) are
  placeholders. The functor built on them says nothing about metrics or cobordisms.
- `NullEnergy.null_energy_condition` states only that a sum of squares in `List Int` is nonnegative.
- `SpectralDimension.lean` uses a formula `d_s = (4+2k)/(1+k)` that differs from the monograph.
- The messages printed by `Main.lean` ("PROVEN", "100% PASS") are not mathematical verification.
