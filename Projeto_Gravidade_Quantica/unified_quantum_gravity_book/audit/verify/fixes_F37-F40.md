# Fixes for F-37 to F-40 (ch. 7, 9, 10, 11)

**Date:** 2026-09-24. **Corrector:** a Claude session that did not write the audited text.
**Inputs:** `ch07_blind.md`, `ch09_blind.md`, `ch10_blind.md`, `ch11_blind.md`, `SUMMARY.md`, scripts in `scripts/`.
**Referee scripts re-run:** `ch07_blind_checks.py` 42/42; `ch09_blind_checks.py` blocks [1]-[5] reproduced; `ch10_counterexample.py`, `ch10_degeneracy.py`, `ch10_kfac.py`, `ch10_conjecture.py` ALL CHECKS OK; `ch11_blind_checks.py` 21/21. All negative controls failed as they should.
**Own checks:** the proofs added to the text were re-derived by hand: the ch7 C^{1,1} contact principle, the ch9 inequality ∫|θ'| ≤ ∫|κ| + π, the ch10 gap bound ≥ 1/2 and ‖2I−Q‖² ≥ d, the ch11 two-interval regularized lengths and the midpoint O(k^-2) order.
**New DOIs:** each was resolved through the Crossref API before it was added. They are Fenchel 1929, Lewicka–Peres 2020, Boone 1959, Lieutier 2004, Goroff–Sagnotti 1986, Petz 1996, Bisognano–Wichmann 1976, Casini–Huerta–Myers 2011, FLM 2013, Dong–Lewkowycz 2018, Miyaji et al. 2015, Hayden et al. 2016, Immirzi 1997, Rovelli–Thiemann 1998 and Ledoux (AMS Surv. 89).
**Compilation:** each chapter was compiled twice with `pdflatex -interaction=nonstopmode`. All four logs have 0 `! ` lines, 0 LaTeX/Package/Class warnings and 0 Overfull boxes.
**House style:** the four files contain no `audit/scripts` paths. The phrases "earlier version", "withdrawn", "corrected" and "erratum" do not occur.

## Chapter 7 (F-37)

| # | Item | Referee | Assessment | Action |
|---|---|---|---|---|
| 7.1 | Title "up to Dimension 12" | M | Agree: the body has no dimension-12 content | Title changed to "…Variational Theory, Constructive Heuristics, and Explicit Candidates" |
| 7.2 | Abstract (ii): "only obstacles curving towards Ω constrain the minimizer" | M | Agree. Referee's disk counterexample checked: the segment is excluded, and κ=0 a.e. forces a straight line | Abstract now restricts the claim to the contact point and says convex obstacles can still raise κ*. The counterexample was added after Prop. `thm:obstacle_exclusion` and to the Status section |
| 7.3 | Contact principle proved for C², applied to C^{1,1} minimizers | M | Agree. Wrote the local ess-sup/concavity proof: graph u over T_{p0}M, a.e. bound on D²u(w,w), mollification gives concavity of g(tv)−C_r t²/2, then comparison with φ=½h+o | New item (4) with eq. `eq:contact_c11`, λ_k(p0) ≤ lim_r ess sup ‖II‖. Pipeline step 5, abstract and Status now cite it |
| 7.4 | Pipeline step 4: degree r−2 profiles | M | Agree. Script [9] shows degree r−2 is impossible and 2r−3 is possible for r=2..5. Counting 2(r−1) Hermite conditions gives the same | Step 4 rewritten: clothoids give C²; C^r needs degree ≥ 2r−3; example 3τ²−2τ³ for r=3 |
| 7.5 | Prop. `thm:scaling_law`(1)/Table: "multi-plane helix" is a planar circle for any phases | B | Agree: γ = R0 e^{iωs} w, and w, iw are orthogonal of norm √m | Statement and proof now say it is a circle of radius √m R0. Remark, table row ("Diagonal circle") and subsection/outline titles renamed |
| 7.6 | `rem:slab`(a) "inequality goes the other way" | B | Agree (U-turn with Σ={p,q} gives κ*=2/w>0) | Rewritten: the identity controls II_M only on TΣ at points of Σ, and no inequality holds in either direction |
| 7.7 | Remark after `conj:saturated` applies it outside its hypothesis; uses attainment | B | Agree | Remark rewritten as the obstacle-free analogue, with attainment from Prop. `thm:existence` (d_{κ*} ≤ L) |
| 7.8 | `conj:saturated`: "active" undefined | INCERTO | Agree that it is ambiguous. No counterexample found | "Active" defined as κ* strictly larger than the value with Ω̄ replaced by ℝⁿ. "If a minimizer exists" added |
| 7.9 | Homotopy remark: item (i) ≠ conjecture | B | Agree | Now says (i) is stronger than the conjecture and explains why |
| 7.10 | Pipeline step 1 medial axis of Ω; step 2 ‖TM−TΣ‖ ill-defined | B | Agree | Step 1 uses M(ℝⁿ∖Ω)∩Ω. Step 2 recast as a prescribed conormal η0 with penalty β∫|η_M−η0|² (units of β unchanged, L^{-k}) |
| 7.11 | "Sussmann classified"; Fenchel uncited; lasry1986, azagra2007, grisvard1985 uncited | B | Agree | Sussmann sentence now reads "necessary conditions / structure result". `fenchel1929` added and cited. The three uncited items removed |
| 7.12 | `audit/scripts/check_ch07.py` in 5 places | B | Agree | Replaced with "(numerical check in the accompanying code repository)" or with the explicit short computation (Kähler curve II, circle of radius R0) |
| 7.13 | Minor: Ω bounded vs remark on unbounded Ω; table "General Frenet n≥2"; semicircle rotated relative to strip | B | Agree | Remark `rem:compactness_necessity` rewritten, adding the f=\|γ\|² convexity bound. Table row: n ≥ 2J(+1) with explicit unit-speed constraint. §6.1 parametrization now in ℝ×[0,w] from (1,0) to (−1,0) |
| 7.14 | Obs.: Langer/Breuning are for closed immersions; closed case outside formulation; two-sided ball ⇒ C^{1,1} uncited; geodesic existence for C² metric | B (obs.) | Agree | Sentence added on closed vs. boundary case. "(Σ=∅, outside the formulation)" added. `lewicka2020` cited. The proof now uses the graph curve instead of a geodesic of M |

## Chapter 9 (F-38)

| # | Item | Referee | Assessment | Action |
|---|---|---|---|---|
| 9.1 | Rem. mapping classes / abstract: "do not act by conjugation" | M | Agree. Script [3]: Świerczkowski pair with tr A = tr B, residual 3e-16. Trace argument checked: conjugation preserves traces, and σ1 sends a2 to a1 | Remark rewritten. The question is ρ∘M_* = c_g∘ρ with g not necessarily in ρ(F_m). For generic ρ (tr ρ(a1) ≠ tr ρ(a2)) σ1 is not realized; for the Świerczkowski ρ it is. Abstract adjusted |
| 9.2 | π1 ≅ F_m hypotheses insufficient | M | Agree with all three counterexamples | Ω is now a Jordan domain and each O_i a closed topological disk. §1.3 states the consequences (Schoenflies, locally contractible, homotopy equivalence of F and Ω∖O, which justifies the interchangeable notation) and lists the three counterexamples. a_i now defined by winding δ_ij. Prop. `thm:loop_bounding` uses B(c_i,ρ_i) ⊂ int O_i |
| 9.3 | Rem. 2.3(c): ∫\|κ\| ≥ ∫\|θ'\| − π "unknown" | M | Agree. Proof re-derived (ψ=φ−θ, G triangular wave in [0,π]). Script [2]: no violation, and the line is sharp | New Prop. `prop:winding_total_curvature` with proof, sharpness and the ρ_i-independent winding bound. (c) rewritten. Abstract, Alg. step 1 and Conclusion use it |
| 9.4 | Teardrop remark vs. Conclusion (open problem) | M | Agree: the strict improvement is unproved | Remark now gives only the trivial non-uniqueness construction (insert a circle of radius 1/κ*) and states that the strict improvement is open, in line with the Conclusion |
| 9.5 | Rem. higher dimensions: "CAD gives an algorithm" | M | Agree (Novikov–Boone via a 2-complex in ℝ⁵) | Rewritten: CAD gives a finite presentation, not a decision procedure, and deciding is impossible in general for n ≥ 5. `boone1959` added. Goresky–MacPherson sentence clarified |
| 9.6 | Alg. 4.1 "hence upper bounds" | M | Agree. Script [5]: 3.7e3 on the grid vs 1.19e6 true | Text now states that the grid check certifies nothing, gives the Bézier example, and says a certified bound requires e.g. interval arithmetic |
| 9.7 | Abstract "both homotopy classes"; V unspecified | B | Agree. The w ≥ 2 construction was checked: extra full turns of the radius-H circle (tangent at (0,H)) | Prop. `prop:corridor_gap` now says π1 = ℤ; lower bound for all classes; attainment for w=0,1 (embedded) and w ≥ 2 (immersed); V at least the construction length. Abstract, remark and Conclusion aligned |
| 9.8 | §1.1 "local optimizers explore only the seed class" | B | Agree | Restricted to continuous feasible deformations. Penalty/discrete steps can jump |
| 9.9 | "Smallest diameter 5.7" | B | Agree (script [1] gives 2.0002) | Removed. Sharpness via the circle stated instead |
| 9.10 | Dyson expansion omits γ̇; ordering unfixed | B | Agree | Defined via U' = U A(γ̇), U(0)=I. Expansion now has A_{γ(t)}(γ̇(t)); composition law stated |
| 9.11 | π1(Ω∖O) vs closed free space; ANR fact uncited | B | Agree | Equivalence stated in §1.3. Prop. 2.2(2) proof uses an ENR retraction (cited to Hatcher, Appendix) plus the linear homotopy |
| 9.12 | `check_ch09.py` references; overloaded "\|κ\| ≤ κ" | B | Agree | References removed or replaced by the neutral phrase. Prop. `prop:subloop` uses the constant K |
| 9.13 | Medial-axis remark endpoints; mollification changes \|γ'\| | B | Agree | `lieutier2004` cited and the endpoint treatment added. The (1+O(κε)) factor noted in Remark 5.2 |
| 9.14 | Dubins bibliographic title truncated (raised for ch10, same entry here) | B | Agree | Full title in ch7, ch9, ch10 |

## Chapter 10 (F-39)

| # | Item | Referee | Assessment | Action |
|---|---|---|---|---|
| 10.1 | Item 5: κ*_info has no length bound, and κ*=0 even when no geodesic avoids O_sing | M | Agree. `ch10_degeneracy.py` re-run: major arcs keep distance ≥ 2 from c, and the g̃-curvature 1/(√(1+λ0)R) → 0 | Definition now has L ≤ L_max. Prop. `prop:degenerate` requires a geodesic of length ≤ L_max. New Remark `rem:length_bound` gives the counterexample. Conclusion and abstract corrected |
| 10.2 | Item 18: Conj. 3.1 first half trivial; "suitable class"; Σ* may be unreachable | M | Agree. Script: λ_min = λ0; min ‖2I−Q‖² ≥ d = 5 | Conjecture restated: tanh networks of width d, depth ℓ, on O(d)^ℓ; unregularized Fisher on the tangent space; hypothesis Σ*∩O(d)^ℓ ≠ ∅; explicit polynomial rates. New remark explains each choice and the comparison with Saxe et al. |
| 10.3 | Item 20: §4 attributes constant curvature with active obstacle to ch7 | M | Agree | Attribution removed. Text states what ch7 proves (obstacle-free Dubins only), that the obstacle case is a ch7 conjecture, and that contact arcs follow ∂O |
| 10.4 | Item 4: 0.71 depends on x law; ≥ 1/2 analytically | B | Agree (script D: min = 0.5000) | Abstract: "at least 1/2 for every input law (≈0.70 for Gaussian inputs)" |
| 10.5 | Item 7: "In particular …" unproved | B | Agree | Removed from the proposition. New remark: dependence on H only through Σ* (radius √(2ε/h)) |
| 10.6 | Item 11: proof delegates to script; x law; zhang2017 misused; σ, L undefined | B | Agree | Analytic proof of gap ≥ 1/2 written, with the law of labels stated. σ and L defined. N ≥ 8 threshold derived. zhang cited only for "networks fit random labels"; key renamed `zhang2021` to match CACM 2021 |
| 10.7 | Item 13: amari1998 for leading eigendirections | B | Agree | Natural gradient = full inverse; restriction attributed to low-rank truncations |
| 10.8 | Items 16/21: quadratic variation is for the SDE limit | B | Agree | Qualified in the remark and the table |
| 10.9 | Item 17: barren plateaus need 2-designs; ReLU no dynamical isometry | B | Agree | Both hypotheses added |
| 10.10 | Item 20 (B): Frenet system written for ℝ³ | B | Agree | Noted: D−1 curvatures in dimension D |
| 10.11 | Item 21: "bounded by design" | B | Agree | Table cell rewritten |
| 10.12 | Item 22: "false in general" too broad | B | Agree | Restricted to nontrivial bounds in (κ*, N, δ) below 1/2 at κ*=0 |
| 10.13 | Item 24: Dubins title truncated; zhang key/year | B | Agree | Fixed |
| 10.14 | Item 14 (obs.): K-FAC bias and accumulation cost | B (obs.) | Agree | Both added |

## Chapter 11 (F-40, ch11 part)

| # | Item | Referee | Assessment | Action |
|---|---|---|---|---|
| 11.1 | Conj. 4.1: metric is H^d, c2 = L²/z0² | M | Agree (dz²/z² = du²; script block 9) | Conjecture restated: c1 = L², c2 = L²/z0², H^d as a constant-time slice of Poincaré AdS_{d+1}. The status remark notes that there is no time direction |
| 11.2 | Conj. 4.5: "every admissible cut converges to a minimizer" | M | Agree. Two-interval counterexample re-derived: the connected pair is shorter iff δ(2+δ) < 1 | Conjecture restated: "admissible" and the regularized area defined; part (2) says the flow converges to an extremal cut and the minimizer is the least-area limit. Remark gives the counterexample and says extremal cuts are fixed points. Table and Status aligned |
| 11.3 | Faulkner et al. 2017 scope (abstract, Rem. 3.3, Status) | B | Agree | Restricted to states prepared by Euclidean path-integral sources, to second order in the sources |
| 11.4 | Line 143 tautology + script reference; Rem. 2.3 script | B | Agree | Line deleted. Script references replaced |
| 11.5 | Rem. 2.3: "factor 1.13"; Petz uncited; Rindler type III | B | Agree | General inequality with proof (log mean < arithmetic mean). `petz1996` cited. Type III caveat added |
| 11.6 | Eq. 3.1: no BW/CHM citation | B | Agree | `bisognano1976`, `casini2011` cited |
| 11.7 | Prop. 3.1 applied to CFT balls without regularization caveat | B | Agree | Paragraph added after the proof |
| 11.8 | Thm 3.2 last sentence (FLM, Swingle–VR) inside theorem; FLM uncited | B | Agree | Moved out of the theorem statement. `faulkner2013quantum` cited |
| 11.9 | Rem. 3.3: Dong–Lewkowycz not mentioned | B (obs.) | Agree | `dong2018entropy` added |
| 11.10 | Obs. 4.2: local-excitation metric attributed to NRT | B | Agree | NRT: g_uu proposal. Miyaji et al. 2015: information metric of locally excited states, H² for d=2. `miyaji2015cmera` added |
| 11.11 | Min-cut equality for perfect tensors overstated; Hayden et al. missing | B | Agree | Restricted to connected regions in nonpositively curved tilings. `hayden2016random` added |
| 11.12 | §6: flow hypothesis "along the flow"; W0 not preserved; metric d unspecified | B | Agree (relying on the referee's reading of ch2) | All three stated. `silvafilho2026grand` cited |
| 11.13 | Rem. 6.2: Ollivier lower bound only for graph distance | B | Agree | Condition and the general bound −(J(x)+J(y))/d added |
| 11.14 | Prop. 5.2(1): O(1/k) not sharp; product order | B | Agree (script: order 1.99) | O(k^-2) with a Magnus-expansion justification. Local error corrected to O(k^-3). Ordering stated |
| 11.15 | Prop. 5.2(2): γ prefactor attributed to Rovelli–Smolin | B | Agree | Discreteness credited to RS 1995 and AL 1997; γ-dependence to Immirzi 1997 and Rovelli–Thiemann 1998 (added). "Kinematical, γ free" added in text, abstract, table and Status |
| 11.16 | Intro: "new counterterms at each loop order" | B | Agree | Power counting; one-loop on-shell finiteness; two-loop divergence (`goroff1986`) |
| 11.17 | Bibliography: maldacena1999large and silvafilho2026grand uncited; missing refs | B | Agree | maldacena1999large removed. silvafilho2026grand now cited at the ch12 cross-references. Missing references added with verified DOIs. Concentration cited to `ledoux2001` |
| 11.18 | Minor: j_e ∈ ½ℕ includes 0; Conj. 6.1 differs from ch12 | B (obs.) | Agree | j_e ∈ {1/2, 1, …}. Sentence noting that the ch11 version is stronger |
| 11.19 | "From canonical energy" for Faulkner et al. (verified only from the abstract) | INCERTO | Cannot confirm without the paper body | The unverified attribution was removed. The text now says only what the abstract supports |

## Disputed items

None. Every referee claim I checked held up, either through the referee's own script, which I re-ran, or through my own derivation. In one case I went further than the referee: for ch9 Prop. 6.1 I also state and construct attainment for all w ≥ 2 (immersed paths). The referee only suggested that this "seems" true.

## Items left open

- **F-40, ch12 part** (Conj. 5.2 of ch12 has the same MCF defect). Deferred by instruction: ch12 is not editable in this task. The ch11 remark now calls the ch12 conjecture "related", not identical.
- **`silvafilho2026flows` (ch11) has no DOI.** It is an internal preprint of this treatise; no DOI exists to add.
- **Miyaji et al. 2015 and Dong–Lewkowycz 2018 content** is stated at the level of their abstracts, as reported by the referee (H² for d=2; integrated linearized equations around arbitrary states). A reader with the full papers should confirm the finer details.
- **Referee observations that were not PROBLEM items** and that I left unchanged: ch9 Conj. 5.1 does not spell out the boundary and length constraints in F_∞, and the liminf part may be accessible; ch7 notes that "Theorem" is generous for `thm:monotonicity`. Both are optional refinements and do not affect correctness.
