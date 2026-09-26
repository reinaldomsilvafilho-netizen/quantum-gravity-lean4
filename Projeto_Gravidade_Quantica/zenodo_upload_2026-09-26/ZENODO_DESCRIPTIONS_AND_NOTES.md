# Zenodo: descriptions and version notes (2026-09-26)

Paste each "Description" into the record's description field and each "Version note" into the version notes (or at the top of the description). Plain text, ready to paste.

---

## 1. Geometry, Tensors, and Quantum Gravity (monograph)
Concept DOI: 10.5281/zenodo.22290043 · File: Geometry_Tensors_and_Quantum_Gravity.pdf (191 pp.)

### Description
A thirteen-chapter monograph on geometric and analytic structures that recur in quantum gravity. The chapters range from functional realizations of matrices and tensors to emergent spacetime. Each chapter separates proved results from conjectures and heuristic proposals, and states that status explicitly.

Part I (Ch. 1–2) studies functional realizations of matrices and tensors and geometric flows on matrix, tensor and graphon spaces.

Part II (Ch. 3–6) covers:
- the analytic continuation of Pascal's simplex;
- Beta-kernel operators;
- interdimensional transforms;
- analysis on Sierpiński simplices.

Proved results in Part II include:
- the asymptotics of continuous multinomial integrals;
- an expansion of the continuous row entropy via the Barnes G-function;
- an inversion formula for the Radon–Beta transform.

Part III (Ch. 7–10) develops the L∞ minimax extrinsic-curvature problem for submanifolds and curves in obstacle domains. Its proved results include:
- existence for curves;
- a contact principle;
- sharp U-turn bounds in Euclidean and constant-curvature spaces;
- finiteness of homotopy classes under a length bound.

Part III also treats applications to ADM slicings and relativistic trajectories. It shows the limits of transferring the problem to information geometry.

Part IV (Ch. 11–12) reviews established links between entanglement, tensor networks and gravity, with sources (linearized Einstein equations from the entanglement first law, min-cut bounds, the loop-quantum-gravity area spectrum). It formulates the open questions as conjectures.

Part V (Ch. 13) is an order-of-magnitude assessment. It concludes that Planck-suppressed signatures of the two-scale spectral-dimension model lie far below current and planned sensitivities.

The Lean 4 files in the companion repository are a naming skeleton and do not verify the mathematics. LaTeX sources, numerical checks, audit records and the register of findings are in the repository: https://github.com/reinaldomsilvafilho-netizen/quantum-gravity-lean4

### Version note
This version follows an independent audit of the whole volume. Every chapter was re-checked by a referee who had not written it, corrected in a separate pass, and checked again. Main changes:
- Several statements of earlier versions were incorrect and have been corrected or withdrawn. Others are now labelled as conjectures. Headline claims such as a derivation of the non-linear Einstein equations, UV finiteness and observable Planck-scale signatures are no longer made.
- Ch. 13: corrected redshift dependence of the gravitational-wave dispersion delay (~10⁻⁶¹ s); tensor-tilt running evaluated at the horizon-exit scale (|α_t| ≲ 10⁻¹¹). Both are unobservable. The figure has been regenerated.
- Ch. 12: the closed form of the spectral dimension d_s(τ) was already given by Sotiriou, Visser and Weinfurtner (2011) and is credited to them.
- New proofs, among others: the asymptotics I_m(x) ~ m^x, the Radon–Beta inversion formula, the U-turn bound in constant-curvature spaces, the contact principle for C^{1,1} submanifolds, and a winding bound for planar curves.
- The Lean 4 material is described as a skeleton that verifies no mathematics.
- A full list of changes is in the attached CHANGELOG.

Still to be updated in a later version: an independent re-check of the final consistency pass (titles, cross-references, notation); Python checks for chapters 1–11 rewritten to the independent-oracle standard; a Lean/Mathlib formalization; a single-source build of the volume. Several conjectures remain open and are marked as such in the text. Sources, audit records and the register of findings are in the repository.

---

## 2. Simplicial Quantum Gravity on Δ₄ × Δ₂
Concept DOI: 10.5281/zenodo.22704111 · File: manuscript_simplicial_quantum_gravity_master.pdf (15 pp.)

### Description
A companion paper to the monograph *Geometry, Tensors, and Quantum Gravity*. It studies a two-scale spectral-dimension model and L∞-minimax foliations, and it formulates conjectures on gauge and flavour structure on the product Δ₄ × Δ₂. The results, proved or cited as classical, are:
- a closed form for the spectral dimension of the two-scale diffusion symbol k² + ℓ²k⁴, flowing from 2 in the ultraviolet to 4 in the infrared; the closed form was first given by Sotiriou, Visser and Weinfurtner;
- pointwise bounds on shear and scalar curvature for ADM slices of bounded extrinsic curvature;
- order-of-magnitude estimates showing that the model's observational signatures are far below reach.

The following are stated as conjectures, remarks or phenomenological fits, with explicit hypotheses:
- a Yang–Mills gap on the Gribov region;
- flavour relations (Koide, Cabibbo) with a parameter count;
- a Dirac–Kähler treatment of fermions;
- graphon condensation.

### Version note
Corrected against the audited monograph. The earlier title claimed non-perturbative UV regularization and Standard Model gauge condensation; the title now describes what the paper establishes. The printed closed form for d_s(τ) was wrong (it did not reach d_s = 2 in the UV) and has been replaced. The following were incorrect and are now negative remarks or have been removed:
- a vacuum-energy "cancellation";
- a geometric "Born rule";
- a Koide "derivation";
- a Planck-pressure value;
- the double-copy claim.

The Yang–Mills gap is now a conditional conjecture. Observational numbers are updated. The detailed list is in the attached notes.

Still to be updated: an independent second check of these corrections; the Beta-Laplacian defined in the paper, which differs from the monograph's operators, has not been analysed; the paper's own Beta-kernel does not produce the assumed dispersion symbol, which is therefore an assumption.

---

## 3. A Geometric and Metric-Measure Framework for the Yang–Mills Mass Gap
Concept DOI: 10.5281/zenodo.22301093 · File: paper_yang_mills_mass_gap.pdf (11 pp.)

### Description
This paper proves no mass gap. Its main result is a conditional theorem, and the existence of a mass gap in four-dimensional Yang–Mills theory remains open.

The conditional theorem assumes two things:
1. the ground-state measures of regularized Yang–Mills Hamiltonians on the Gribov region satisfy a uniform Bakry–Émery curvature-dimension bound CD(K,∞);
2. the Hamiltonians converge in the strong resolvent sense.

Under these hypotheses, the continuum Hamiltonian has a spectral gap of at least g²K/2 above the vacuum. Whether the Gribov–Zwanziger construction supplies such a bound is open.

The paper recalls the Gribov and refined Gribov–Zwanziger frameworks with their sources, and it states the area law as a conjecture.

### Version note
The earlier version presented an unconditional mass gap. That claim is withdrawn: the main result is now a conditional theorem with explicit hypotheses. The following were incorrect and have been removed:
- a Ricci-positivity argument;
- the relation Δ ≥ √λ₁;
- a string-tension formula derived from Federer reach;
- a Floer-homology construction;
- a "strong CP" resolution.

The Faddeev–Popov operator, the Gribov-region setting and the Gribov–Zwanziger action have been corrected. Attributions to the Gribov–Zwanziger and refined-GZ literature are now complete. The Lean files are not claimed to verify anything. Details are in the attached notes.

Still to be updated: an independent second check of these corrections; the Lean folder of this paper has not been audited; the hypotheses of the conditional theorem (existence of the ground-state measure, a uniform CD(K,∞) bound, reflection positivity of the Gribov–Zwanziger measure) remain open.

---

## 4. An S₃-Circulant Parametrization of Fermion Masses and Mixing and a Simplicial Vacuum-Energy Ansatz
Concept DOI: 10.5281/zenodo.22373916 · File: paper_fermion_mass_hierarchy.pdf (9 pp.)

### Description
A phenomenological study of an S₃-circulant parametrization of charged-fermion masses, mixing relations and a simplicial vacuum-energy ansatz. Every relation is classified as an identity, a known relation (Koide, the Gatto–Sartori–Tonin relation for the Cabibbo angle), an ansatz or a fit.

The parameter count is explicit: 9 continuous inputs (4 free) and at least 8 discrete choices, against 12 observables. That leaves 6 genuine tests:
- the two that pass (m_τ and |V_us|) are known relations;
- the one new sharp relation, for the reactor angle θ₁₃, is disfavoured by more than 4σ.

Two structural limitations are stated:
- if both quark sectors are circulant, the CKM matrix is trivial;
- the vacuum-energy formula works only as a finely tuned one-parameter fit.

All numbers use PDG 2024 inputs and are reproducible with the accompanying script.

### Version note
The earlier title and text described a geometric derivation of the fermion mass hierarchy. The paper is now presented as a parametrization with an explicit parameter count. Corrections:
- the Koide value of m_τ is 1776.969 MeV;
- the Koide "derivation" was circular and is now a proposition with its status stated;
- the circulant ansatz produces no Cabibbo mixing;
- the vacuum-energy identity was false and the related theorem is withdrawn;
- claims of formal (Lean) verification are removed.

Details and the parameter table are in the attached notes.

Still to be updated: an independent second check of these corrections; a mixing mechanism beyond the circulant ansatz, which by itself gives a trivial CKM matrix; the companion cover letters and older auxiliary files, which still describe the previous claims.
