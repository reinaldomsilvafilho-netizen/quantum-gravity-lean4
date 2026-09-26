# Fixes for F-41 (ch. 13), F-42 (ch. 12), F-43 (ch. 8), and the deferred part of F-40 (ch. 12)

Date: 2026-09-25. Corrector: a separate agent (not the author of the text and not the referee).

Files edited:
- `chap08_noneuclidean_minimax_relativity_adm.tex`
- `chap12_grand_unification_quantum_gravity_treatise.tex`
- `chap13_experimental_observational_signatures_quantum_gravity.tex`
- `audit/scripts/observability_estimates.py` and `fig_experimental_signatures.pdf` (regenerated)
- `verify_chap12_numerical.py` (battery 6)
- `verify_chap13_numerical.py` (batteries 3-6)

New evidence script:
- `audit/verify/scripts/fixes_F41_F43_checks.py` (every block has a negative control). Result: `FAILURES: none`.

Evidence also came from the referees' scripts, all re-run: `ch08_gr_blind.py`, `ch08_uturn_curved.py`, `ch12_blind_checks.py`, `ch13_gw_dispersion.py`, `ch13_tilt_atoms.py`, `ch13_heat_kernel.py`. All pass.

External checks:
- The arXiv abstract of 1105.5646 (SVW) confirms that the paper treats **2+1** dimensions and Hořava–Lifshitz dispersion.
- New DOIs were resolved via Crossref: 10.1088/0264-9381/15/4/011, 10.4310/ATMP.2007.v11.n6.a3, 10.1007/s002200100381, 10.1051/0004-6361/201833910, 10.1103/PhysRevD.85.024041, 10.1088/1475-7516/2008/01/031, 10.1103/PhysRevLett.127.151301.
- The arXiv DOI 10.48550/arXiv.1405.2933 was resolved via DataCite.

Compilation: each chapter was compiled twice with `pdflatex -interaction=nonstopmode`. Each .log shows 0 errors, 0 LaTeX/Package/Class warnings and 0 overfull boxes.

## Chapter 13 (F-41)

| # | Item | Referee | Assessment | Action |
|---|---|---|---|---|
| 1 | Eq. (5)/D_2: redshift weight (1+z) should be (1+z)^2 | A | **Agree.** Standard result (Jacob–Piran n=2; Mirshekari–Yunes–Will). The referee oracle gives text/oracle ratios of 0.66, 0.41 and 0.22. My own non-perturbative FRW root-finding oracle (verify_chap13 battery 3) agrees with (1+z)^2 to 1e-3, and (1+z)^1 fails. | D_2 now uses (1+z')^2, with both references cited (Crossref-verified DOIs). |
| 1a | N1 numbers: 4e-62, 1e-61, 3e-61 s | A (inherited) | **Agree.** Recomputed: 6.4e-62, 2.9e-61, 1.16e-60 s. | Text now gives 6e-62, 3e-61, 1.2e-60 s. The gap is now "56–57 orders" (57.2/56.5/55.9). The abstract and table now give 10^-61–10^-60 s. |
| 1b | N3: ℓ* ≈ 4.7e-7 m, 0.4 eV | B (inherited) | **Agree.** Recomputed: 2.99e-7 m and 0.66 eV. | Abstract "~3e-7 m", text "3.0e-7 m, ≈0.7 eV", caption updated. |
| 1c | Fig. 1(a) drawn with the wrong formula; reference at 1 Hz vs 10 Hz in the text | A/B | **Agree.** | Generator fixed (D_2 with (1+z)^2, reference 10 Hz, "benchmark" label) and figure regenerated. Rendered and inspected. |
| 2 | N7′: tilt running evaluated at today's comoving k | A | **Agree.** Comoving k is not invariant. The physical momentum at horizon exit is H_inf. r<0.036 (BICEP/Keck 2021) and A_s=2.1e-9 (Planck 2018) give H_inf ≤ 4.70e13 GeV and \|α_t\| ≤ 1.5e-11 (3.7e-10 with M_red). Checked by verify_chap13 battery 5, where the comoving-k control gives <1e-100. | Tilt paragraph rewritten in terms of the physical momentum p and H_inf. Abstract "≲10^-11"; table row "at horizon exit, ≲10^-11". Two references added (DOIs verified). |
| 2a | Fig. 1(b): CMB band placed at the wrong k | B | **Agree.** The band is now defined physically. | x-axis is p/M_*. Shaded region p = H_inf ≤ 4.7e13 GeV (x ≤ 3.85e-6). Caption updated. |
| 3 | "The symbol above corresponds to ξ = 1" | M | **Agree.** The Lorentzian continuation p²(1+ℓ²p²) has roots p² = 0 (ξ = 0) and p² = −1/ℓ² (ghost), confirmed by the referee's sympy check. The anisotropic operator with ξ = 1 has d_s(UV) = 5/2 (ch13_heat_kernel.py: 2.5001). | Parenthetical removed. The text now says the model does not fix ξ, gives both facts, and states that the estimates are linear in ξ, with ξ = 1/2 displayed. |
| 4 | R1: k²+ℓ²k⁴ attributed to HL anisotropic scaling and to SVW | B/M | **Agree.** HL gives d_s = 1+3/z, so 2 needs z = 3 and z = 2 gives 2.5 (verified numerically). SVW treat 2+1 CDT with HL dispersion (arXiv abstract checked). | Paragraph rewritten: the isotropic symbol gives 4→2; HL obtains 2 with z = 3; SVW is correctly described as 2+1 with HL-type dispersion. |
| 5 | C1: abstract calls the α_t postulate a "consequence" | B | Agree. | Abstract now says "ansätze ... none of which follows from the diffusion model" and "postulated". |
| 6 | C3: conclusion mixes "below reach" with "no prediction" | B | Agree. | Conclusion separates GW/CMB (below reach) from simulators/interferometers (no prediction). |
| 7 | I3: "exact result of the framework" | B | Agree. | Intro now reads "a closed form ... with an assumed two-scale symbol, an elementary integral". |
| 8 | Table without numeric instrument reach; ξ = 1/2 unjustified | B | Agree. | Table now gives "10^-4 s (benchmark)" and "LiteBIRD, CMB-S4: r ~ 10^-3". The ξ scaling is stated in the text. |
| 9 | Eq. 6 note: the Padé matches only the IR power, not the coefficient (4−2x² vs 4−12ℓ²/τ) | observation | Agree. | Text says the coefficient is not matched. The IR expansion d_s = 4 − 12ℓ_P²/τ is added. |
| 10 | N4 (INCERTO): 10^-4 s ET/CE timing not in the cited references | INCERTO | Agree that the references do not state it. | Now presented as an assumed optimistic benchmark with its derivation (~0.1 rad at ~100 Hz). The text notes that real tests fit the waveform phase. No citation claimed. |
| 11 | A2 (INCERTO): ℓ_P/λ_dB ≲ 4e-26 depends on v | INCERTO/B | **Agree.** 3.5e-27·(v/1 m/s); 1.6e-25 at 45 m/s. | Text gives the v-dependence and "< 2e-25 for v ≲ 45 m/s". Table updated. verify_chap13 battery 6 was rewritten with a control. |
| 12 | Caption references `audit/scripts/...` | convention | — | Replaced by "The script ... is in the accompanying code repository". |

## Chapter 12 (F-42, plus the deferred part of F-40)

| # | Item | Referee | Assessment | Action |
|---|---|---|---|---|
| 1 | Conj. 5.2 (RT via MCF) false as stated; two intervals | A (and F-40) | **Agree.** Extremal cuts are fixed points of the area gradient flow. For δ = 0.1 the excess is −2L log 0.21 = 3.12 L, matching the referee's [s.8c]. | Conjecture restated as in ch. 11 Conj. 4.5: the flow converges to *an* admissible extremal cut, and γ_A is the least-area extremal cut among the limits. Remark 5.3 gives the two-interval counterexample and cross-references ch. 11 Conj. 4.5. The number 5.2 is kept, since ch. 11 cites it. |
| 2 | §9.5 Fefferman–Graham: g_(2) = C_2/L² false; index/dimension errors; placed in "exact solutions" | A | **Agree.** For a flat boundary g_(2) = 0, while C_2 > 0 ([s.9a]). The g_(d) coefficient is 16πG/(d L^{d−1})⟨T⟩ + X[g_(0)] (de Haro–Skenderis–Solodukhin, DOI verified). | Subsection deleted from §9. New Remark 5.4 (after Conj. 5.2, so numbering is stable) states the correct FG facts. It explains how relative entropy enters (first law; C_2 = canonical energy, Kubo–Mori Fisher information) and states the failed identification with its counterexample. |
| 3 | Rem. 6.2: κ ≥ −2 / rate ≤ e^{−4t} depends on the metric | M | **Agree.** Discrete metric gives κ ≥ 0 (hypothesis vacuous). Euclidean metric gives κ unbounded below (−36, −372 at [s.7a]). | Remark rewritten: the metric dependence, both examples, and the unit-edge graph distance as the only setting for −2. The conclusion now calls the decay result conditional. |
| 4 | Conj. 4.3 badly specified; trivial under Thiemann; contradicts Rem. 4.4 | M | **Agree.** Thiemann's Ĥ acts at vertices via the volume operator, and the AL volume vanishes at valence ≤ 2, so Ĥ annihilates disjoint-loop states. | Conjecture now specifies H_J (disjoint smooth circles), the diffeomorphism-covariant dual H_J*, and requirements (a) non-trivial action, (b) invariance, (c) closure with the structure function ω^a. Remark 4.4 rewritten to explain the degenerate case and the crossing (4-valent) case. Thiemann QSD cited (DOI verified). Numbering 4.3 kept (cited by ch. 13). |
| 5 | §8.1: 1 in place of γ_5 in the product Dirac operator | M | **Agree.** Checked in fixes_F41_F43_checks 6a: γ_5 gives ±√(k²+m²); 1 gives ±\|k\|+m. | Operator is now D⊗1 + γ_5⊗W (Chamseddine–Connes–Marcolli, DOI verified) with the D² argument. The scalar/pseudo-scalar rationale is removed. Boundary conditions on Δ_4 are declared unspecified. "Universal Action" is described as schematic. |
| 6 | §8.2: Q_q "colour Casimir shift" has no derivation | M | **Agree.** Arithmetic is 0.71208. 1/√3 is not C_F. The scheme spread is 0.65–0.72. | Text now calls it a numerical fit with no derivation and says agreement carries no evidential weight. "Induced by QCD renormalization" removed. |
| 7 | §9.2: SVW attribution (4→2 with isotropic k²+k⁴) | M | **Agree.** Verified in the arXiv abstract: 2+1 dimensions, HL dispersion. | SVW is now correctly described. The isotropic operator is called "different", and the anisotropic d_s = 5/2 is noted. The same fix is in §2.2 and the abstract. |
| 8 | "Theorem 5.5 of [ch01]" → 5.6; "Theorem 4.1 of [ch11]" points to a conjecture | B | **Agree.** Checked in the .aux files: ch01 Kac–Rice = Thm 5.6; ch11 FGHMV = Thm 3.2. | Both references corrected. The (n, d) vs (N, k) notation is noted. |
| 9 | Matter term attributed to FGHMV; g^QFI unused | B | Agree (ch. 11 attributes it to Swingle–Van Raamsdonk). | Thm 5.1(i) is now the vacuum equation. A sentence on the matter term cites Swingle–VR (DataCite DOI). g^QFI removed. (ii) restricted to states prepared by Euclidean sources, as in ch. 11. The proof says "imported". |
| 10 | Thm 3.1 proof: "exclusively at vertices" false; K_ijK^ij called "shear" | B | **Agree.** The minimum −a² holds along the whole edge (a, −a, t). | Proof rewritten with the multi-affine argument, with the edge noted. "Shear contraction" became "quadratic invariant", and the table entry is now "Bounded Extrinsic Curvature". |
| 11 | Prop. 4.1: chronology suffices; smooth time function | B | Agree. | Now stated for chronological spacetimes, with a proof via p ∈ I^+(p). No time function needed. |
| 12 | Table 1: Israel shell is C^{0,1}, not C^{1,1}; caption/conclusion treat Thm 5.1 as proved | B | Agree. | Table entry is "Israel Thin-Shell Junctions (C^{0,1} metric)". Caption and conclusion list Thm 5.1 as imported, and the abstract says so. |
| 13a | m_H 125.25 vs PDG 2024 125.20 | B | Agree. Δλ = 0.00428 (fixes_F41_F43_checks 5a). | Text now "Δλ ≈ 0.0043 → m_H ≈ 125.2 GeV". |
| 13b | §10: D and the M_P convention undefined | B | Agree. | §10 rewritten: M_P non-reduced (reduced mass differs by factors of order 8π); D_2(z) with (1+z)² defined. The numbers now match ch. 13 (6e-62–1e-60 s, 3e-7 m, 0.7 eV). |
| 13c | Thin shell: r_min exists iff 27κ²M² < 1; "two Schwarzschild" with one M | B | **Agree.** Minimum of the cubic is 2M − 2/(3√3κ). Checked in fixes_F41_F43_checks 4a. | Setup restated (one side of mass M, proper time ℓ, K^θ_θ ansatz). The existence condition is derived in the text. |
| 13d | d = 2 divergence is logarithmic | B | Agree. | Text now reads "ε^{−(d−2)} for d ≥ 3, logarithmic for d = 2". |
| 13e | Measure dσ in I_m (projected Lebesgue vs Hausdorff, factor √m) | B | Agree (Jacobian √m). | dσ specified as in ch. 3. The √m factor is noted. |
| 13f | a, b undefined in Koide | B | Agree. | v_j = a + 2b cos(δ+2πj/3) is defined, with \|v_1\|² = 3a², \|v_2\|² = 6b², Q = 1/3 + 2b²/(3a²). |
| 13g | Prop. 2.1: d_s defined "for every τ" but proved via lim τ→0; α > 1 kernel not positive | B | Agree. | Proof computes d_s at every τ. A note on α > 1 was added. |
| 13h | Prop. 6.1: W_0 ≥ 0, t_δ ≤ T, δ range | B | Agree. | Statement made precise. |
| 13i | §9.1 Airy: "discrete spectrum" of what; units | B | Agree. | Now: the Dirichlet condition quantizes V_0 for fixed s_0; units are fixed by the postulate. |
| 13j | §10.2 "running" vs definition; M_P convention | B | Agree. | See ch. 13 item 2. §10.2 was rewritten with physical momentum and H_inf (\|α_t\| ≤ 1.5e-11). |
| 14 | §10.1: "the diffusion model has ξ = 1" | M (via ch13) | Agree. | Replaced by the same explanation as ch. 13 item 3. |
| 15 | §10.4: ℓ_P/λ_dB velocity dependence | INCERTO (ch13) | Agree. | Velocity-dependent statement, < 2e-25 for v ≲ 45 m/s. |
| 16 | §10 references `audit/scripts/...` | convention | — | Replaced by a reference to ch. 13 and the accompanying code repository. |
| 17 | INCERTO: priority of the erfc closed form | INCERTO | Not resolved. No exhaustive literature search was done. | The text makes no novelty claim ("an elementary integral that can be evaluated in closed form"). **Left open.** |

## Chapter 8 (F-43)

| # | Item | Referee | Assessment | Action |
|---|---|---|---|---|
| 1 | §3.2(3): tube about a geodesic in H^n has ‖II‖ = c coth(cd), not tanh | A | **Agree.** Metric dr² + sinh² dΩ + cosh² dt gives principal curvatures coth (×(n−2)) and tanh. Referee check 2 re-run. | Item 3 is now "equidistant from a totally geodesic hyperplane (umbilic, c tanh(cd))". New item 4 covers tubes (c coth(cd), n ≥ 3) and n = 2. Table row added. |
| 2 | Conj. 4.16: minimizer "in each W ∈ Z" false; classes empty | A | **Agree.** \|dφ/dt\| < √f/r ≤ 1/(3√3M) at r = 3M (fixes_F41_F43_checks 2a). Refinement: with φ_q − φ_p ∈ (−π, π], \|W\| < Δt/(6√3πM) + 1/2, so Δt = 100M gives \|W\| ≤ 3. The referee's "≤ 4" is a valid but looser bound. | Conjecture restricted to non-empty classes. The redundant "prescribed coordinate-time separation" is dropped (only q ∈ I^+(p) remains). New Remark gives the bound and the counterexample. |
| 3 | Def. 2.3: operator norm infinite for Lorentzian normal bundle; empty sup for timelike curves | M | **Agree.** The Minkowski sphere with ν = cosh η e_t + sinh η e_r gives sinh η/R → ∞. | Definition rewritten for cases (a) Riemannian/definite normal, (b) spacelike hypersurfaces, (c) timelike curves (\|g(v,v)\| = 1). The counterexample is stated, and codimension-2 spacelike surfaces are measured inside a slice (as in Prop. 4.6). Labelled def:opnorm. |
| 4 | §4.1: K_ij = −½L_nγ = −g(∇∂∂, n) sign | M | **Agree** (re-derived with g(n, ∂_j) = 0; Milne check). | Now K_ij = −½L_nγ = −g(∇_i n, ∂_j) = g(∇_{∂i}∂_j, n). II = −K n and the Milne example are stated. |
| 5 | Def. 4.5: θ_l = q^{ab}II·l = q^{ab}∇_a l_b sign | M | **Agree** (Minkowski sphere: +2/R vs −2/R). | θ_l := q^{ab} g(∇_{e_a} l, e_b) = −q^{ab} g(II, l), with the Minkowski sanity check. |
| 6 | Conj. 3.3 / Rem. 3.4: prove if the sketch works, including S² with w ≥ π/2 | M | **Agree that it is provable.** I proved it by a shorter route than the referee's ODE–Gronwall sketch. Along a curve, the Killing field ∂_x gives d/ds(G cos θ) = −κ G sin θ. Integrating over the sub-arc where θ runs from 0 to π gives k ≥ (G(a)+G(b))/∫_a^b G = c coth(c(b−a)/2) in H² and c cot(c(b−a)/2) in S². This needs only G > 0, so it covers S² for all w < π/c, including w ≥ π/2, with no denominator issue. Checks: identity to 1e-15 with a sign-flip control; min F = k0 on grids including S² w = 1.6, 2.4, 3.0; random search finds no U-turn at 0.98 k0 and some at 1.05 k0 (fixes_F41_F43_checks 1a–1c). | Conjecture replaced by Theorem 3.3 (label prop:space_form_uturn) with full proof. The Fermi-frame definition of a U-turn is given. The Remark explains how the holonomy is absorbed and states a general warped-tube bound. The abstract and table updated. |
| 7 | Def. 4.4: non sequitur, vacuous SEC, trivial problem (Einstein–Rosen slice K ≡ 0) | M | Agree. | Converted to Remark 4.4 (rem:minimax_slicing). It explains the degeneracy, the need for boundary conditions, the Raychaudhuri scope, and that an SEC constraint on V is empty where the SEC holds. |
| 8 | §4.9: maximal slicing "fails to prevent runaway of K_ijK^ij"; argmin trivial | M | **Agree** (Estabrook bound 4√3/(9M) from the chapter's own table, referee check 9). | ¶1 now states that maximal slicing avoids the singularity with bounded K and that its drawback is slice stretching. Item 1 requires a class C with boundary behaviour, notes the degeneracy, and leaves existence unaddressed. |
| 9 | Obs. 4.18 / Conj. 6.1 inconsistent with ch. 7 (C^{1,1} vs C²; Riemannian vs Lorentzian) | M | **Agree.** Ch. 7 conjectures inf A_r = inf A_{1,1}. | Conj. 6.1 now states inf over A_r = inf over A_{1,1} for Riemannian N (bounded Ω, C^{1,1} ∂Ω, C^∞ Σ, V), matching ch. 7. The Remark on worldlines calls the Lorentzian version an open analogue that is not covered. |
| 10 | Obs. 6.2: "reduces to the Euclidean conjecture" unargued | M | Agree. | Replaced by an explanation of why no reduction is known (global infima vs local lemma; Christoffel terms change the functional). |
| 11 | Obs. 4.21: lensing heuristic built on II of null geodesics | M | **Agree.** k ∈ k^⊥, so there is no splitting; ∇_k k = 0. | Heuristic formula and "Penrose affine parameter" removed. Remark "Null curves" states why the framework does not apply and what curvature could be used instead (optical metric). |
| 12 | P_eff ≤ c⁷/(ħG²) does not follow | M | **Agree.** p involves Ḣ (fixes_F41_F43_checks 3b). | Replaced by the bound that does follow: ρc² ≤ (3/8π)c⁷/(ħG²) ≈ 5.5e112 J m^-3 (3a). The text explains why no pressure bound follows. |
| 13 | Abstract (4) omits ρ(r0) ≥ 0 | B | Agree. | Abstract now says "when the energy density at the throat is nonnegative". The proof notes that the bound fails without the hypothesis. |
| 14 | Notation of κ*, A_r (k, V, r); table column "c" = codimension; c vs c² clash | B | Agree. | Eq. (1.1) is now κ*_r(N, g, Ω, Σ, V), with A_r and A_{1,1} defined as in ch. 7. Worldline problem written κ*_wl. Table column "codim.". Thm 3.1 uses K̄ for the ambient curvature. |
| 15 | §3.2 "saturated minimax geometries" with "κ* = ..." | B | Agree. | Sections renamed "Constant-Curvature Examples". Values given as ‖II‖_op, with an explicit statement that they are examples. |
| 16 | Thm 3.1: n ≥ 3 missing; k ≥ 3 restriction unnecessary | B | Agree. | Hypothesis n ≥ 3. The Codazzi argument is stated for k ≥ 2. |
| 17 | Prop. 4.15: endpoints not in I^±; (2),(3) outside Ω; (3) proof via radial geodesics | B | Agree. | Endpoints are in J^±, interior points in I^±. The scope of (2) and (3) is stated. (3) is proved by corner rounding. |
| 18 | Israel: sign convention opposite to §4.1 | B | Agree. | Convention K_ab = h h ∇n, with n from − to +, stated. The sign reversal under the §4.1 convention is noted. |
| 19 | Table: Minkowski hyperboloid called "uniform acceleration" | B | Agree. | Now "Milne slice (constant proper time from the origin)", with the equation given. |
| 20 | Obs. 4.20: physics inverted (GHY at the Planck scale) | B | Agree. | Rewritten: the Gibbons–Hawking computation is reliable for black holes ≫ ℓ_P and uncontrolled at the Planck scale. |
| 21 | §4.10: "direct connection"; "GHY entropy generation" | B | Agree. | Now "formal resemblance" and "GHY boundary term". |
| 22 | Obs. 4.9: C^{1,1} of ch. 7 presented as fact | B | Agree. | Dubins minimizers are C^{1,1} and not C². Optimal regularity in general is "expected there, not proved". |
| 23 | §4.9 item 3: distance to the singularity undefined | B | Agree. | Uses the areal radius r (a scalar): barrier μ ≥ r^-2, clearance min r ≥ r_0. |
| 24 | Misc.: §6 title; O'Neill sign convention; "Penrose affine parameter"; Cor 4.2 citation to ch. 12; ν(r)/r sign; "is foliate" | B | Agree. | §6 retitled "Regularity Invariance in Riemannian Backgrounds". O'Neill convention note added. Cor 4.2 made self-contained (multi-affine argument, sharpness stated). Principal curvatures ±ν/r "up to orientation". "Foliated". Lensing term removed. |
| 25 | Abstract (2): curved optimality stated as a conjecture | M | Resolved by item 6. | Abstract states the theorem. |
| 26 | Intro: L¹/L² "fail to prevent localized curvature singularities" | B | Agree. | Now: integral functionals control curvature on average and do not bound its pointwise maximum. |
| 27 | Intro §1.2: κ^{*,Phys}, κ^{*,Emb} undefined; stably causal vs chronology | B | Agree. | Symbols replaced by words (infimum over immersed = over embedded). The argument uses chronology (a CTC). Cauchy surfaces are embedded because they are achronal. |
| 28 | Obs. 4.7: "slices degenerate at the horizon" | B | Agree. | Now: the static slices meet at the bifurcation sphere, which is minimal in each. |
| 29 | Obs. 4.23: which normal n | B | **Agree** (κ̃ = κ/Ω + ñ(ln Ω)). | Both the g̃-normal and g-normal bounds are stated. |
| 30 | §4.9 item 2: gauge speed α√(fγ^{xx}) | B | Agree. | Corrected. |
| 31 | Prop. 4.6 proof: "up to sign convention" and script reference | B | Agree (with shift β^r = β and the §4.1 convention, K_ij = D_(iβ_j) exactly). | Derivation made explicit: θ_l = 2(1−β)/r. Script path replaced by "accompanying code repository". |
| 32 | Uncited bibliography items | convention | — | Removed 10 uncited items (douglas1931, willmore1965, riviere2008, dubins1957, sussmann1995, chitsaz2007, federer1959, langer1984, langer1985, penrose1965). |

## Referee claims disputed

None of substance.
- **Ch. 8, Conj. 4.16:** the referee's example bound "|W| ≤ 4 for Δt = 100M" is valid but not sharp. With φ_q − φ_p ∈ (−π, π] the bound is |W| ≤ 3. This refines the claim rather than disputing it.
- **Ch. 8, Conj. 3.3:** I agreed with the referee's conclusion that it is provable, but used a different proof (Killing-field first integral instead of ODE comparison plus Gronwall). This proof also removes the S² w ≥ π/2 denominator issue the referee flagged.

## Items left open

1. **Ch. 12 INCERTO: priority of the erfc closed form for k² + ℓ²k⁴ in 4D.** No literature search was done (candidates: SVW PRD 84 (2011) 104018; Calcagni, Modesto). The text makes no novelty claim. A search is still needed if a priority statement is ever wanted.
2. **Ch. 13 N4: the 10^-4 s timing figure for ET/CE** is now presented as an assumed benchmark with its derivation, not as a cited instrument specification. A proper reference, or a phase-based detectability criterion, would still improve it.
3. **Mathematical content that remains conjectural by design:**
   - ch. 8: Conj. 4.16 (existence in non-empty winding classes and the W = ±1 advantage) and Conj. 6.1;
   - ch. 12: Conj. 4.3 (now well specified), 5.2 and 7.1, plus the graphon condensation conjecture.
   These are correctly labelled, not open defects.
4. **Not a referee item, noticed in passing:** in ch. 8 the `adm1962` bibitem cites the 1962 Wiley chapter but carries the DOI of the 2008 GRG reprint (10.1007/s10714-008-0661-1). Left unchanged, outside the scope of F-43.
5. **The referee script `audit/verify/scripts/ch13_figure_check.py`** compares the figure with the old (1+z)^1 curves as the "text formula". It was not re-run as a pass/fail test for the new figure. The regenerated figure was checked by rendering it and by the generator's printed values.
