# A: REBCO tape coils under curvature limits

## Physical problem
REBCO tapes (typically 4–12 mm wide, ~0.1 mm thick) have strain limits:
- **Easy-way bending** (about the wide axis): minimum radius set by the tolerable strain in the superconducting layer. Order of magnitude: a few mm to cm; *confirm with datasheets*.
- **Hard-way bending** (in the plane of the tape): very restrictive; essentially forbidden.
- **Torsion** per unit length is also limited.

Non-planar coils (stellarators) and compact magnets must follow a path that produces the desired field while respecting these limits.

## Mathematical translation
The tape is a curve γ with a Frenet or Bishop frame. The constraints are:
- normal curvature ≤ κ_easy;
- geodesic curvature ≤ κ_hard ≈ 0;
- torsion ≤ τ_max.

This is an L∞ problem on the curvatures, the setting of ch. 7–8. Tape that cannot bend the hard way is a **developable strip**: the curve must admit a ribbon of zero geodesic curvature. That links to rectifying developables and to "Sadowsky / Wunderlich" strips.

## Questions
1. What exists already?
   - Stellarator coil optimization: FOCUS, REGCOIL, SIMSOPT; papers on HTS stellarator coils such as those of Paz-Soldan et al. and the "HTS stellarator" studies.
   - Which constraints do they impose, and how: L² penalties or hard constraints?
2. Is there a benefit to imposing the constraint **in L∞** (minimax) rather than as an L² penalty? The expected answer is yes: an L² penalty lets the curvature spike locally, and a spike is what breaks the tape.
3. Does the C^{1,1} regularity of ch. 7 give a guarantee of existence and structure (bang-bang arcs, equioscillation) of the optimal coil?
4. A minimal model problem: a closed curve on a torus, linking the plasma, with |κ| ≤ κ* and |τ| ≤ τ*, minimizing a field error. What does the optimal curve look like?

## Steps
1. Literature (sonnet agent): `literatura.md`.
2. Real parameters from tape datasheets: `parametros.md`.
3. Toy problem in Python: planar or toroidal curve, comparing the L² penalty with the L∞ constraint, measuring the curvature peak and the field error. Include an oracle and a negative control.
4. If the L∞ version wins clearly: a theorem (existence plus structure) and a short paper.
