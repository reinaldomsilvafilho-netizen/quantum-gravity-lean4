# Zenodo landing page

- **Suggested version:** 2.0.0 (major). Replaces version 1, record 22441680.
- **Title:** Quantum Fisher Geometry of Continuous Matrix Product State Fields and Lorentzian Cylinders: A Moore-Path Functor and Obstructions to a Cobordism Functor

## Description (≤ 250 words)

This paper tests the proposal of reading a spatial metric off the quantum Fisher information (QFI) metric of a field of continuous matrix product states (cMPS), and a Lorentzian metric off paths of such fields, aiming at a functor to spacetime cobordisms.

**Proved:**
- The QFI metric of a projectively immersed field is Riemannian. It is invariant under local phases, fixed unitaries, complex conjugation and cMPS gauge transformations.
- For matrix-valued scalar matter: the ADM energy and momentum densities, with the correct sign of the momentum density, and the identity T(k,k) = ‖k·∂Ψ‖² ≥ 0 for null k.
- The entropy-rate lapse is smooth where the bond density matrix has constant rank, and it can diverge where the rank changes.
- On Moore paths with sitting instants, the construction is a functor into a category of Lorentzian cylinders. Einstein solutions form a subcategory. This result is close to tautological.

**Shown to fail, with counterexamples:**
- The image metrics need not solve the Einstein equations.
- The construction depends on the parametrization of paths.
- Gradient-flow paths modulo reparametrization do not form a category.
- Lorentzian cobordisms up to isometry have no identities.
- The proposed monoidal and compact structures do not exist as stated.

**Open:**
- whether non-constant cMPS paths can produce Einstein spacetimes;
- monoidal structure, topology change, and amplitudes.

No result is formally verified. The Lean files that accompanied the first version are a placeholder skeleton without Mathlib and verify nothing.

## Keywords

continuous matrix product states; quantum Fisher information; Fubini–Study metric; ADM formalism; null energy condition; Moore paths; Lorentzian cobordisms; emergent spacetime; tensor networks; category theory

## Notes

Paste the contents of `CORRECTIONS_2026-10-06.md` into the "Notes" field. Remove the version-1 claims "verifies the Atiyah–Segal sewing axiom" and "100% rigor in Lean 4".
