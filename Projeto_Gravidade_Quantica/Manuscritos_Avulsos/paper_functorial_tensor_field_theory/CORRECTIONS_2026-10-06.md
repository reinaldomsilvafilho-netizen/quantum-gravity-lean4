# Version 2.0.0 (2026-10-06): notes on changes

Concept DOI 10.5281/zenodo.22441676. Previous version: 1 (record 22441680, 2026-09-06).

This is a major version. An independent blind review found that the central claims of version 1 are false. This version keeps what is correct, proves a weaker statement, and records each failure with its counterexample.

## New title

- **Old:** "A Functorial Bridge from Continuous Tensor Manifolds to 4-Dimensional Spacetime Cobordisms"
- **New:** "Quantum Fisher Geometry of Continuous Matrix Product State Fields and Lorentzian Cylinders: A Moore-Path Functor and Obstructions to a Cobordism Functor"

The old title claimed a functor to spacetime cobordisms, and no such functor is constructed.

## Withdrawn claims

These claims of version 1 are withdrawn, and the reasons are given.

1. **"CTensMan is a category"** (Def. 2.1). Morphisms were gradient-flow paths modulo reparametrization, and the identity was the constant path. This fails:
   - a non-constant flow line is never constant on an interval, so composing with the identity changes the class (now Prop. 6.4);
   - "boundary-flat" reparametrizations are not diffeomorphisms;
   - concatenated flow lines are not flow lines.
2. **"CTensMan is symmetric dagger-compact monoidal"** (Prop. 2.2). No proof was given, and the statement is false:
   - the product of connected manifolds is disconnected;
   - the unit (empty manifold, χ = 1) is not an object;
   - matrix sizes do not match;
   - no morphism from the unit to T*⊗T exists, because paths keep the manifold fixed (now Remark 6.6).
3. **"Cob is a category"** (Def. 3.1). Lorentzian cobordisms up to isometry have no identities. Volume doubles under self-gluing, so e∘e = e is impossible (now Prop. 6.7). Gluing smooth solutions was not closed either.
4. **Lemma 5.1 ("Einstein equations follow").** The proof assumed the evolution equations it was meant to derive. Counterexample (now Example 6.1): a field of product qubit states with QFI metric sin²(2θ)δ on T³ gives an FRW image. The constraints hold at both ends, and n·n·G = 3ȧ²/(N₀²a²) ≠ 0 inside. This example is not a cMPS.
5. **Theorem 5.2 (functoriality).**
   - The lapse is not reparametrization-covariant, so the map was not well defined on classes. An analytic proof (Jensen) is now Prop. 6.3, and Prop. 6.2 shows that no covariant lapse can be positive on constant paths.
   - The image of a "constant" path is not static: the shift ½∂‖R‖² gives K ≠ 0 (now Remark 6.8).
6. **Theorem 5.3 (monoidal and dagger functor).** Withdrawn; see items 2 and 3.
7. **Proposition 5.4 (sewing ↔ bond contraction ↔ Wheeler–DeWitt).**
   - This was a heuristic and is now an unnumbered paragraph.
   - It includes an order-of-magnitude estimate: ln χ ≥ 4.8×10⁶⁸ for a 1 m² surface.
   - Ryu–Takayanagi is cited only for S = Area/4G.
8. **Corollary 5.5 (amplitudes).** Withdrawn, because the amplitude formula was not derived.
9. **Theorem 5.6.**
   - "Faithful modulo gauge" rested on a theorem that does not exist. The new F is shown not to be faithful (Remark 5.6(b)): multiplying the field by a time-dependent phase e^{ib(t)}, with b = 0 near both ends, keeps the endpoints and the image but changes the morphism. A fixed unitary would not do, since it changes the endpoints and hence the hom-set.
   - "NEC prevents closed timelike curves" is false: Gödel's universe is a counterexample (Remark 3.3).
   - The algebraic identity T_kk = ‖k·∂Ψ‖² ≥ 0 is kept (Prop. 3.2).
10. **"Formally verified in Lean 4."** False. The Lean files do not use Mathlib, their predicates are `True` placeholders, and the pushed version used axioms that assert the conclusions. The paper now says the files are a placeholder skeleton that verifies nothing.

## Corrected errors

- **Momentum density sign:** j_i = −Re Tr(π†∂_iψ), not +. Proof in Prop. 3.1.
- **Lapse smoothness:** "strictly C^∞" was false where the bond density matrix changes rank (counterexample diag(1−t, t)). The lapse is now proved smooth under locally constant rank (Prop. 4.2), and ρ(x,t) is part of the path data.
- **Shift:** with Q anti-Hermitian, the commutator term vanishes identically (Prop. 4.3). The restriction Q ∈ u(χ) is dropped, since it conflicts with the standard cMPS normalization.
- **Matter field:** ψ := R is not gauge invariant, so the matter field is now an independent datum (Remark 2.7).
- **Misattribution:** Verstraete–Cirac was cited for a "fundamental theorem of MPS" that their paper does not contain. It is now cited for the cMPS definition, gauge invariance, normalization and the block-entropy bound, all checked in the paper's text.
- **Bibliography:**
  - Atiyah's title fixed per Crossref.
  - Segal removed, as it is no longer cited.
  - Uncited self-references removed.
  - The book cited with its DOI.
  - Gödel 1949 added.
  - Every DOI resolved via Crossref or DataCite.
  - References expanded and checked: 8 → 42, with a "Related work" subsection and citations placed where each claim is made; Atiyah's title restored to the printed "Topological quantum field theories"; Segal is cited again, in Related work.
- **Wording:** undefined "graphon contractions", "Unified Grand Synthesis", Wilson loops, and the "Entropic" NEC name removed.
- **Affiliation and declarations:** affiliation updated; competing-interests and verification-status statements added.

## What is proved now

- **QFI metric:** it is Riemannian for projectively immersed fields, and invariant under local phases, fixed unitaries, complex conjugation, and pointwise cMPS gauge transformations (Prop. 2.3, Lemma 2.4, Cor. 2.6).
- **ADM densities and null energy identity:** Props. 3.1–3.2.
- **Lapse and image metric:** the lapse lower bound and smoothness under constant rank; the image metric is Lorentzian (Props. 4.2–4.4).
- **Functor:** a strict functor from Moore paths with sitting instants to Lorentzian cylinders (Thm. 5.4). Einstein solutions form a subcategory (Cor. 5.5). The theorem is close to tautological, and the paper says so.

## What still needs work

- **Open problem 7.1 (central):** does any non-constant cMPS path have an Einstein image?
- **Open problems 7.2–7.4:** monoidal structure, topology change and duals, and amplitudes.

## Review

The corrections were independently re-checked by a separate AI session, which confirmed the new proofs (Prop. 4.2(b), Prop. 6.3, Thm. 5.4). Its remaining remarks were then fixed by another AI session:
- Example 6.1 now displays n·n·(G + Λg) = 3ȧ²/(N₀²a²) − Λ; the conclusion (no Λ works) is unchanged.
- New Lemma 2.8: projectively immersed fields exist when dim H = ∞ (more precisely, when M immerses in R^m and dim H ≥ m + 1), and never when dim H ≤ 2. Prop. 6.3 states this hypothesis.
- Prop. 6.2: the sharp bound α′ ≥ ½ is given, and the continuity used at the endpoints is now an explicit hypothesis.
- Local existence for Einstein equations with field sources is now also cited from Choquet-Bruhat, *General Relativity and the Einstein Equations* (OUP 2009), Ch. VI.
- The declarations are replaced by the project's standard statement on the use of generative AI tools.

## Pre-release fix (2026-10-07, independent corrector)

The Declarations no longer mention earlier versions; they now say that the Lean 4 files in the author's repository associated with this work are a placeholder skeleton without Mathlib and verify none of the statements. See `audit/fixes_prerelease.md`.

## Scripts

The numerical check scripts are available from the author on request:

- `fixes_checks.py`: V1–V9, each with an oracle and a negative control;
- `math_checks.py`: the referee's checks C1–C8, re-run;
- `doi_check_v2.py`;
- `L2_checks.py` and `round2_checks.py`: the checks of the re-check and of the final fixes.
