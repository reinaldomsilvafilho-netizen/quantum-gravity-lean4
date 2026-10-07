# Version note: *Beyond the Spectrum II*, v3 (new major version), 2026-10-06

- **Concept DOI:** 10.5281/zenodo.22644743.
- **Previous version (v2):** record 22866175, trilogy pages 29–46. Its text is identical to record 22699282's `volume_2_geometric_measures.pdf`.
- **v3:** `paper_geometric_measures_functional_tensors.tex` / `.pdf`, 21 pages.
- **Build:** compiled 3 times, with 0 errors, 0 warnings, 0 overfull boxes and 0 undefined references.
- **Audit trail:**
  - `audit/blind_layer1.md`: blind review;
  - `audit/fixes_layer1.md`: corrections, item by item;
  - `RECONSTRUCTION_v2.md`: how the v2 source was rebuilt;
  - `audit/scripts/corrector_*.py`: checks.

## Why a major version
Several theorems of v2 are false. v3 withdraws them, replaces them with correct statements that are proved, or relabels them as classical results. The abstract, introduction and conclusion were rewritten to claim only what the body proves.

## Changes from v2, item by item

1. **Persistent entropy, Thm 3.4 in v2, now Thm 3.6.**
   - v2 claimed that persistent entropy strictly separates isospectral matrices, and that N_k ≥ 2 distinct lifetimes force different entropies. Both claims are false.
     - In v2's own 3×3 example both entropies are 0.
     - A 3×3 grid can never have two H₁ bars.
     - A reflected matrix JB′Jᵀ is isospectral to B, has the same diagram with two distinct lifetimes, and has the same entropy.
   - v3 proves the diagram separation of the 3×3 pair, and adds a 5×5 isospectral pair whose entropies differ (0.673 against 0), with a complete proof.
   - Remark 3.7 explains the limits: the step realization is not permutation-invariant, and entropy depends only on lifetimes.
2. **Step realizations, §3.** The smoothing argument was invalid, and bottleneck stability does not apply to discontinuous functions. The step realization is now defined explicitly, and the invalid argument was removed.
3. **Wavefront set, Thm 5.3 in v2, now Prop. 5.4.**
   - With v2's fixed-Gaussian-window definition, the theorem is false: every point, even far from the interface, gets 1/|ξ| decay.
   - v3 uses Hörmander's definition and proves the classical result WF = N*Γ∖0 for a jump across a smooth interface.
   - Remark 5.5 adds that grid corners carry all directions.
4. **Dixmier trace, Def 6.1 / Thm 6.2 in v2, now Prop. 6.2.** v2 defined the trace by summing singular values, which gives c∫|Φ| for sign-changing Φ. In v3 the trace is defined linearly, as in Connes, with |D|^{-d} := 0 on ker D. Connes' trace theorem (1988) is cited.
5. **Cyclic cocycles, Thm 6.3 in v2, removed.**
   - The claim that τ_d is quantized and homotopy-invariant is false: without the grading, τ₂ = −(1/2π)∫Φ₀∇Φ₁·∇Φ₂.
   - A degree-0 map gives τ₂ ≠ 0, and rotations at fixed degree change τ₂.
   - v3 proves the correct statement for d = 2 (Prop. 6.4): the graded, antisymmetrized cocycle equals −4i·deg F.
6. **QFI volume, Thm 7.2 in v2, now Thm 7.3.**
   - The claim "Vol = 0 iff ρ is constant modulo gauge (unentangled)" is false: gauge orbits have Vol > 0, and the "only if" was vacuous under v2's added hypothesis.
   - v3 proves that Vol = 0 if and only if rank dρ < d everywhere.
   - The QFI formula was missing a factor of 2; it is corrected in Lemma 7.2.
   - The link to entanglement was removed. The "entanglement contour" was renamed, since Chen–Vidal already use that term for a different object.
7. **Metric-speed bound, Thm 2.3(c).** The v2 proof used an invalid L¹→H⁻¹ step and an unstated regularity hypothesis. v3 gives a new complete proof for the kernel realization, with an explicit constant L_ψ/(π√c₀). Sharpness of the L¹ bound (b) is now proved.
8. **Bakry–Émery, Thm 2.5 in v2, now Thm 2.6.**
   - The v2 proof misapplied von Renesse–Sturm (that result needs no weight and no boundary), and relied on an unproved "convex exhaustion" argument.
   - Part (a) is now proved via McCann. Parts (b) and (c) are labelled classical, via Bakry–Émery, Bakry–Gentil–Ledoux and Caffarelli.
   - The heat flow converges to ∫u₀ dμ_A, not to "the uniform state".
9. **Kernel realization.** v2 required Σ∫ψᵢ² = 1, which contradicts orthonormality. Corrected.
10. **Willmore energy, Thm 4.4 in v2, now Props. 4.4 and 4.5.**
    - Conformal invariance is now stated with White's theorem for the convention H = κ₁ + κ₂.
    - The checkerboard scaling is a proposition about an explicit trigonometric profile: W = c*εk³(1 + O(1/k)), with c* ≈ 1.058. The matrix realization was never defined in v2.
    - Remark 4.3 is corrected: in d = 1, H ≡ 0.
11. **Besov index.** v2's s* used p = 1 only, so it gave 1 for both smooth and step realizations. v3 defines s*_p and proves s*_p = 1/p for step realizations (p > 1). The "fractal conjecture" was replaced by a proved lower bound.
12. **Cheeger.** "Cheeger–Federer" is now Cheeger's inequality, with the perimeter relative to Ω and a complete proof.
13. **Formal verification.**
    - No statement of this volume is machine-checked.
    - The Lean files distributed earlier are a placeholder skeleton without Mathlib.
    - The claim "complete Lean 4 & Mathlib proofs, 0 sorry" on the v2 landing page is false and must not be repeated.
    - The paper says this in its standard Declarations block.
14. **Front matter.**
    - Affiliation updated (PPGEE/DES, UFLA).
    - CAPES Finance Code 001 acknowledged.
    - Standard declarations added: funding, competing interests, AI use, verification status, code availability.
15. **References.**
    - Every DOI was resolved via Crossref or DataCite (`audit/scripts/doi_check_corrector.out.txt`).
    - Fixed:
      - the Benamou–Brenier DOI (v2's DOI pointed to a different paper);
      - the von Renesse–Sturm title;
      - the Vol. I DOI: v2's DOI 10.5281/zenodo.22441676 is the cobordism paper; v3 cites the concept DOI 22644743.
    - Added: Cohen-Steiner–Edelsbrunner–Harer 2007, Crawley-Boevey 2015, Connes 1988, McCann 1997, Caffarelli 2000, Bakry–Gentil–Ledoux 2014, Ambrosio–Gigli–Savaré 2008, White 1973, Cheeger 1970, Evans–Gariepy 2015, Chen–Vidal 2014, Lovász 2012, Mémoli 2011.
    - Removed unused references.
    - 2026-10-07 reference audit: bibliography expanded from 23 to 68 entries (all resolved, `audit/scripts/refs_resolve.out.txt`), each placed where its claim is made, plus a "Related work" paragraph; AGS Thm 8.3.1, Hörmander §8.1–8.2 (section level) and the Connes trace-theorem normalization (via Connes 1994, Ch. IV §2 Prop. 5) are now checked in the source text; details in `audit/references_audit.md`; now 21 pages.

## What still needs work
- **Attributions checked from metadata and standard statements, not in the full text:**
  - Caffarelli 2000: that the contraction theorem covers log-concave perturbations restricted to a convex set;
  - White 1973;
  - McCann 1997;
  - von Renesse–Sturm 2005;
  - Visintin 1991 (checked only through Lombardini);
  - Petz 1996.
- **Remark 7.4(ii)** (gauge orbits generically have Vol > 0) is supported numerically, not proved.
- **Independent human review:** none of the corrected statements has yet been checked by a human expert.
- **Pre-release fixes (2026-10-07, independent corrector):** the Declarations no longer mention earlier versions; they now say that the Lean 4 files in the author's repository associated with this work are a placeholder skeleton without Mathlib and verify none of the statements. See `audit/fixes_prerelease.md`.
- **Pre-release fixes (2026-10-07):** the Volume I citation now reads "Volume I of *Beyond the Spectrum*, Zenodo 10.5281/zenodo.22644743" and says that this record holds all three volumes.
- **Pre-release fixes (2026-10-07):** the Declarations now say that the one book without a DOI (Connes 1994) was resolved through its ISBN record at Open Library.
