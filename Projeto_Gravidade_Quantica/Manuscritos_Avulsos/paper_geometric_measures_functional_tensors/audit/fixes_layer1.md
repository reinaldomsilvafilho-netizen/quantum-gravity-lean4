# Fixes for the layer-1 report on *Beyond the Spectrum II* (2026-10-06)

- **Corrector:** independent session (Claude Opus 5.5). It wrote neither the work nor `blind_layer1.md`.
- **Base:** v2 source rebuilt from the Zenodo PDF (`audit/v2_reconstructed.tex`; see `RECONSTRUCTION_v2.md`). The corrected file is `paper_geometric_measures_functional_tensors.tex`, called v3.
- **Numbering:** "Zenodo" numbers refer to v2; "v3" numbers refer to the corrected PDF.

## Scripts

All exit with code 0, `failures=0`, and each has a negative control.

| Script | What it does |
|---|---|
| The referee's eight `num_*.py` and `crossref_check.py` | Re-run unchanged; outputs reproduced. `num_dixmier.py` exits with code 1 because it passes a numpy integer to `sys.exit`, but it prints `failures=0`; this is not a failed check. |
| `corrector_A_checks.py` (new) | Independent checks for A1–A5 and their replacement statements. |
| `corrector_M_checks.py` (new) | Checks for M1, M5, M6 and the sharpness in Thm 2.3(b). |
| `doi_check_corrector.py` (new) | Crossref/DataCite lookup of every reference in v3, plus the Zenodo DOIs. |
| `rebuild_v2_diff.py` (new) | Word diff between the rebuilt v2 and the Zenodo PDF. |

## A items

| Item | Verdict | Independent check | Change in v3 | Where |
|---|---|---|---|---|
| **A1**: persistent entropy does not separate the isospectral pair; the "multiple bars" fix is false; "N_k ≥ 2 ⇒ different entropies" is false | **Agree** | `corrector_A_checks`, two methods: union–find with Alexander duality, and pixel rasterization with `ndimage.label`. 3×3 pair: Dgm₁(B) = {(2,0)}, Dgm₁(A) = ∅, both E = 0. A 3×3 grid has one interior cell, so β₁ ≤ 1 for any heights. Counterexample to the general claim: C = JB'J^T (reversal) has the same diagram as B', with N₁ = 2 distinct lifetimes, and equal E. The two methods agree on 40 random 5×5 matrices. NEG: an entropy built from births instead of lifetimes differs. | Thm 3.6 rewritten. (a) 3×3 pair: diagrams differ, entropies are equal (0). (b) **New 5×5 isospectral pair** B' (0 and 1 on the interior diagonal, 3 elsewhere), A' = P'B'P'^T: Dgm₁ = {(3,0),(3,1)} against {(3,1)}, and E = 0.673 against 0. Complete proof via a Mayer–Vietoris lemma. Remark 3.7: entropy depends only on lifetimes (reflection example); the step realization is not permutation-invariant, so the separation is expected. | §3.3, Thm 3.6, Rem 3.7; abstract (2); Table 1 |
| **A2**: the wavefront set under a fixed Gaussian window is not localized | **Agree** | `corrector_A_checks`: QAWF quadrature gives ξ\|V(x₀,ξ)\| → g(−x₀) at x₀ = 5s. Integration by parts gives the same exactly: V = g(−x₀)/(iξ) + O(ξ⁻²). Hörmander cut-off for the half-plane: t\|FT\| → β(0) on the conormal, and rapid decay in the tangential factor (mpmath at 40 digits). NEG: a smooth f under the same fixed window decays below 1e-12. | Def 5.2 now uses Hörmander's definition with C_c^∞ cut-offs. Rem 5.3 states the fixed-window counterexample. Prop 5.4 (labelled classical): WF of a jump across a smooth interface = N*Γ∖0, with a complete proof (tangential integration by parts; WF closed and symmetric; singular support; diffeomorphism law). Rem 5.5: grid vertices (quadrant model): all directions. | §5.2 |
| **A3**: the singular-value definition gives c∫\|Φ\|, not c∫Φ | **Agree** | `corrector_A_checks`: on T¹ the linear (diagonal) Dixmier trace gives slopes 0.3183, 0.0000, 0.0955, equal to (1/π)∫f for f = 1, cos 2πx, 0.3 + cos 2πx. Singular values give 0.3177, 0.2024, 0.2115, equal to (1/π)∫\|f\|. NEG: for cos, the singular-value slope is ≠ 0. | Def 6.1: Tr_ω on positive operators, extended by linearity. \|D\|^{−d} := 0 on ker D (constant spinors). Prop 6.2 (Connes' trace theorem, Connes 1988, now cited): c_d∫Φ for real smooth Φ. Rem 6.3 states the \|T\| issue. The constant c_d is unchanged; the referee checked it for d = 1, 2. | §6.1–6.2 |
| **A4**: τ_d is not quantized and not homotopy-invariant | **Agree** | `corrector_A_checks`: sympy gives tr(γ^μγ^ν) = 2δ, and tr(σ₃γ^μγ^ν) = 2iε. **Analytic counterexample** F = (√(1−s²c²), sc/√2, sc/√2): deg 0, while τ₂ = −0.9166 ≠ 0. A degree-1 map composed with 5 rotations: τ₂ ∈ [−0.015, 0.037], while (i/4)Σ sgn σ τ₂^γ = 1.000 every time. NEG: a constant map gives 0. | Old Thm 6.3 removed. **Prop 6.4 (d = 2, proved):** (a) τ₂ = −(1/2π)∫Φ₀∇Φ₁·∇Φ₂; (b) the graded τ₂^γ = −(i/2π)∫Φ₀ dΦ₁∧dΦ₂; (c) (i/4)Σ_σ sgn σ τ₂^γ = deg F ∈ ℤ for F: T² → S². Rem 6.5 gives the counterexamples. Higher d are not treated. | §6.3; abstract (5) |
| **A5**: Thm 7.2(b) is false; gauge orbits have Vol > 0 | **Agree** | `corrector_A_checks`: the gauge orbit has det g > 0. ρ = R(x₁+x₂) has both partials ≠ 0 and det g = 0. In 30 random cases, det g > 0 ⇔ the ∂_μρ are linearly independent. | Thm 7.3 (new, proved): g is the Gram matrix of the ∂_μρ in a positive-definite weighted Hilbert–Schmidt product. Vol = 0 ⇔ rank dρ < d everywhere. Invariance holds under all C¹ diffeomorphisms (with \|det J\|). The claim "unentangled" was removed (Rem 7.4(iii)). | §7.2 |
| **A6**: the Lean + Mathlib claim is false | **Agree** (the referee's inspection of `lean_zip` was not redone; nothing in v3 depends on it) | — | The body contains no formal-verification claim. The "Lean 4 formalization" sentence was removed from the conclusion. The standard Declarations block states that the Lean files of earlier versions are a Mathlib-free placeholder skeleton that verifies nothing. `ZENODO_DESCRIPTION_VOL2.md` makes no Lean claim. | Declarations; §8 |

## M items

| Item | Verdict | Check | Change in v3 | Where |
|---|---|---|---|---|
| **M1**: Thm 2.3(c) | **Agree** | `corrector_M_checks`: exact 1D W₂ via quantiles on 3 curves. Speed/bound ratios 0.98, 0.99, 0.92, all ≤ 1. Near-extremal ratio 1.00000. NEG: the constant 0.9/π is violated. | Hypotheses are now the kernel realization, a C¹ curve, and ρ ≥ c₀. **New complete proof:** weak Neumann problem; Poincaré constant 1/π on the cube; v = ∇φ/ρ; AGS Thm 8.3.1. Bound: \|μ̇\| ≤ ‖∂_τρ‖_{L²}/(π√c₀) ≤ L_ψ‖Ȧ‖_F/(π√c₀). | Thm 2.3(c), Rem 2.4 |
| **M2**: Thm 2.5 proof misapplies von Renesse–Sturm | **Agree** | Referee's `num_w2_be` reproduced. | Now Thm 2.6. (a) is proved: McCann 1997 plus K-convexity of V along displacement interpolation on a convex Ω. (b), (c) are labelled classical, via Bakry–Émery / Bakry–Gentil–Ledoux and Caffarelli's contraction (μ_A is a log-concave perturbation of a Gaussian restricted to the cube). The Reilly/"convex exhaustion" argument was removed. vR–S is cited only in a remark, within its scope. (c) now says "converges to ∫u₀ dμ_A". | §2.3 |
| **M3**: Σ∫ψ_i² = 1 contradicts orthonormality | **Agree** | trivial (Σ∫ψ_i² = n) | Kernel realization: orthonormal ψ_i ∈ L⁴; ∫Φ = Tr A. Added ‖Φ(M)‖_{L²} ≤ L_ψ‖M‖_F. | §2.1 |
| **M4**: mollifier argument; Thm 3.2 applied to step functions | **Agree** | Referee's sup error ≈ 1.4–1.5 reproduced. Also analytic: a uniform limit of continuous functions is continuous. | Step realization defined explicitly (Def 3.2, closed cells, u.s.c.). The mollifier argument was removed. Remark after Thm 3.3 states that stability does not apply. | §3.1–3.2 |
| **M5**: Thm 4.4(b): realization undefined | **Agree** | `corrector_M_checks`: c* = 1.05778 on a periodic cell (stable over 3 refinements). W/(εk³) = 1.084, 1.062, 1.058 for k = 16, 32, 64. NEG: W/(εk²) is unbounded. | Prop 4.5 (proved) concerns the explicit profile Φ_k = ε sin(kx₁)sin(kx₂): Dirichlet energy = ε²k²/2·(1+O(1/k)), W = c*εk³(1+O(1/k)), 0 < c* < ∞. Rem 4.6: the link to matrices is only a model; W is undefined for step realizations. | §4.2 |
| **M6**: s* degenerate for p = 1; "1/p" inconsistent; "conjecture" known | **Agree** | `corrector_M_checks`: step slopes 1.010, 0.505, 0.253 (p = 1, 2, 4); smooth slopes ≈ 1. NEG: s*₂ = 1 for steps fails. | s*_p defined for each p. Prop 5.7 (proved): s*_p = 1 for C¹; for non-constant step realizations, 1/p (p > 1) and 1 (p = 1). The "fractal" conjecture was removed. A remark proves only the lower bound s*₁ ≥ d − dim_M ∂E. | §5.3 |
| **M7**: QFI formula off by a factor 2 | **Agree** | `corrector_A_checks`: Kronecker-solve SLD oracle = 2Σ…/(λ_i+λ_j). NEG: the formula without the 2 fails. | Lemma 7.2 with proof. The bound is now g_μμ ≥ ‖∂_μρ‖²_HS. | §7.2 |
| **M8**: abstract and conclusion overclaim | **Agree** | — | Abstract rewritten (only proved or cited statements). The introduction has a "what is new" paragraph. §8 table lists what is established; open questions; applications marked as not studied. | abstract, §1, §8 |
| **M9**: local .tex ≠ published | **Agree** | `rebuild_v2_diff`: similarity 0.9997, 1 typographic op. | v2 rebuilt first, then corrected. | `RECONSTRUCTION_v2.md` |

## B items

All agreed and fixed:

- **Willmore H convention.** Prop 4.4 uses H = κ₁+κ₂. It invokes White 1973 for ∫(H²/4 − K), and Gauss–Bonnet for ∫(H² − K). The Möbius pole must lie off Σ.
- **Sard needs C^d.** Stated (§4.1).
- **Rem 4.3, d = 1.** Corrected (H ≡ 0). The integrability argument was made precise: \|H\| ≤ (√d+1)‖Hess‖/‖∇Φ‖, finite for Morse Φ.
- **Gaussian ∉ C_c^∞.** The window is a Gaussian (Schwartz); Φ is extended by 0.
- **ker D on T^d.** \|D\|^{−d} := 0 on ker D. The APS sentence was removed.
- **"Cheeger–Federer".** Now Cheeger's inequality, with perimeter relative to Ω and a complete coarea proof (Prop 4.8). "Matrix graph" removed.
- **"Uniform state".** Now ∫u₀ dμ_A.
- **Structure theorem.** Attributed to Crawley-Boevey 2015 (pointwise finite-dimensional modules).
- **CSEH 2007.** Cited.
- **Benamou–Brenier DOI.** Now 10.1007/s002110050002, which Crossref confirms as the right paper.
- **vR–S title.** "…, entropy and Ricci curvature".
- **Šafránek and "d matrices".** Fixed during reconstruction.
- **Entanglement contour.** Renamed "QFI-weighted entropy density", with Chen–Vidal 2014 cited as distinct.
- **Introduction overclaims.** "No canonical metric" replaced; cut distance and Gromov–Wasserstein are cited. The applications list was removed.

## New findings by the corrector (not in the layer-1 report)

1. **Wrong Vol. I DOI.** v2 cites Vol. I with DOI 10.5281/zenodo.22441676, which DataCite resolves to *"A Functorial Bridge … 4-Dimensional Spacetime Cobordisms"*. v3 cites the *Beyond the Spectrum* concept DOI 10.5281/zenodo.22644743.
2. **Unused references removed:** Bengtsson–Życzkowski, Edelsbrunner–Harer, Willmore 1993, and the book DOI.
3. **Thm 2.3(a).** "Realization kernel gauge equivalence" was tautological. Replaced by the quotient by Φ(A) = Φ(B) a.e.
4. **Example 2.8 (Gaussian realization).** It needs n = d, and gives κ_BE = λ_min ≤ 1/d under Tr A = 1. Stated.
5. **Thm 2.3(b) sharpness.** The referee found a numerical ratio of 0.997. v3 proves the constant is sharp: the ratio is 1 − ε for an explicit kernel realization.

## Disagreements

None on substance. One nuance: the referee wrote "Thm 6.2 CONFIRMA for Φ ≥ 0". That is right, but only because μ_n(T) = μ_n(\|T\|) and \|T\| has the same principal symbol when Φ ≥ 0. v3 states the definition by linearity, so the sign restriction is unnecessary.

## L2 note items (orchestrator, 2026-10-06)
- CORRECTIONS: "JBJ^T" -> "JB′J^T"; "What still needs work" reduced to open attributions, Remark 7.4(ii) and human review (layer 2 done; upload and archiving steps are release tasks, not version-note content).
