# Fixes for F-45 (ch. 3), F-46 (ch. 4), F-47 (ch. 1), F-48 (ch. 2), F-49 (ch. 5), F-50 (ch. 6)

Date: 2026-09-25/26. Corrector: a separate agent (not the author of the text and not the referee).

Files edited (only these):
- `chap01_functional_realizations_matrices_tensors.tex`
- `chap02_geometric_flows_tensor_varieties.tex`
- `chap03_pascal_simplex_continuous_multinomials.tex`
- `chap04_simplicial_waves_porous_transport.tex`
- `chap05_interdimensional_transforms_barnes_lie.tex`
- `chap06_sierpinski_fractal_resolvents_spectral_reduction.tex`

New evidence scripts:
- `audit/verify/scripts/fixes_F45_F50_checks.py`, with blocks A–F (ch1–ch6). Every block has a negative control. Result: every check passes (`FAILURES: none`).
- `audit/verify/scripts/fixes_F45_F50_crossref.py` and `fixes_F45_F50_crossref_search.py` resolve DOIs through the Crossref API.
- `audit/verify/scripts/_apply.py` and `_compile.sh` are the edit and compile helpers that were used.

Referee scripts re-run: `ch01`–`ch06_blind_checks.py`. All pass (ch01 26/26, ch02 32/32; ch03–ch06 produced the values quoted in the reports).

New references. Each DOI was resolved through `api.crossref.org/works/<doi>`, and author, title, journal, volume and pages were compared with the entry:
- ch1: Cartwright–Sturmfels 2013, 10.1016/j.laa.2011.05.040; Fleming–Rishel 1960, 10.1007/BF01236935; Lovász–Szegedy 2007 (GAFA), 10.1007/s00039-007-0599-6.
- ch2: McLachlan 1964, 10.1080/00268976400100041; Oseledets 2011, 10.1137/090752286; Takatsu, ASPM 57, 10.2969/aspm/05710463.
- ch3: Hoggatt–Hansell 1971, 10.1080/00150517.1971.12431015; Gradshteyn–Ryzhik 8th ed., 10.1016/C2010-0-64839-5.
- ch4: Servadei–Valdinoci 2014, 10.1017/S0308210512001783; Grisvard, 10.1137/1.9781611972030; Gazzola–Grunau–Sweers, 10.1007/978-3-642-12245-3.
- ch6: Kigami–Lapidus 1993, 10.1007/BF02097233.

Compilation: each chapter was compiled three times with `pdflatex -interaction=nonstopmode`. Every .log shows 0 errors, 0 LaTeX/Package/Class warnings, 0 overfull boxes and 0 undefined references.

Numbering constraints respected: ch1 Kac–Rice remains Theorem 5.6 (cited by ch12), ch3 Remark 6.5 and Theorem 7.2 keep their numbers (cited by ch4, ch5 and ch12), and ch3 Remark 7.3 is cited from ch4. Where a statement changed type, the shared counter keeps the number.

No references to `audit/` remain in chapters 1–6, and no revision-history wording was introduced.

## Chapter 1 (F-47)

| # | Item | Referee | Assessment | Action |
|---|---|---|---|---|
| 1 | Thm 5.6 Kac–Rice: false for d=2; rate Θ(d); i.i.d. symmetric field not isotropic; Hessian −(d−1)fI | A | **Agree** on all four points. T6/T6b/T6c re-run. My own check A1 shows that the non-symmetric i.i.d. tensor has Var f = 1 on the whole sphere, while the equal-variance symmetric model gives 1 vs 5/2 (d=3). By Euler's identity the Riemannian Hessian is H₀ − d f I. | Theorem rewritten (label and number unchanged): (i) isotropic model = non-symmetric i.i.d. tensor (equivalently the symmetric tensor with variance 1/mult), covariance (x·y)^d; (ii) d=2: exactly 2n critical points; (iii) d≥3: lim (1/n) log E = ½ log(d−1) (ABČ, with the rescaling argument); (iv) for the equal-variance symmetric model: non-isotropy shown by the formula 2^{−d}C(2d,d), and the a.s. Cartwright–Sturmfels bound 2((d−1)^n−1)/(d−2) (check A2: counts ≤ 14 for d=n=3; control: 2n=6 exceeded). The proof gives the correct Kac–Rice ingredients: gradient covariance dI, H₀ GOE-type with variance d(d−1)(1+δ), Hessian H₀ − d f I. |
| 2 | Thm 5.5 attention/Sobolev "uniform in N" | M | **Agree.** f(0,0)=N (A3). | Now Proposition 5.5 with normalized measure and explicit C_λ² = Σ(1+|k|²+λ|k|⁴)^{−1}, with C_λ → ∞ as λ → 0. Item (ii) proves f(0,0)=N and R ≥ N²/C_λ². The text states that the bound is only the Sobolev embedding and is not uniform in N. |
| 2a | Referee: C_λ ~ λ^{−1/2} | (remark inside M) | **Partly disputed.** The series gives C_λ² ≈ π log(1/λ) as λ→0 (the integral ∫2πr dr/(1+r²+λr⁴)), so the growth is logarithmic, not λ^{−1/2}. | The text states only that C_λ depends on λ and diverges as λ→0. |
| 3 | Thm 5.7(ii): probability space unspecified; proof does not close | M | **Agree.** | Statement now under the joint law of (T,u) with u independent of T: √d f̂ is exactly N(0,1), so the bound holds with c = ½ for all k. Sharpness follows from the Gaussian tail. The proof is replaced (A4; control c=1 fails). |
| 4 | §6.1 "dense weight matrices converge" | M | **Agree.** | Rewritten: only a subsequence converges, under symmetric and bounded entries; point values of the limit are not defined, so cell averages are used; width, not parameters; stated as a proposal. |
| 5 | Abstract: handlebody, "corrects", "inaccessible" | B | Agree. | Abstract rewritten. |
| 6 | Thm 4.7 title (Grothendieck); Thm 4.8 quotient and citation | B | Agree. | Title changed. The quotient is now by δ_□ = 0 (weak isomorphism). Compactness is attributed to Lovász–Szegedy 2007 (GAFA), and only a subsequence is claimed. |
| 7 | Thm 4.4 "sub-level", De Giorgi | B | Agree. | Now "super-level"; coarea formula of Fleming–Rishel (new reference); De Giorgi is cited only for identifying the perimeter. |
| 8 | Thm 5.4(ii) hypergraphon normalization | B | Agree. | Statement now for symmetric tensors with affine normalization; symmetrization noted. |
| 9 | Spline indices | B | Agree. | P ∈ R^{(m+1)×(n+1)×3}; C^{p−1} at simple knots; knot multiplicity noted. |
| 10 | §6.2 Θ(p) and "phase transitions"; §6.3 time derivatives; §6.4 "CP-ALS diverge" | B | Agree. | ½log(p−1) and the ABČ ground-state/threshold reading; continuity in δ_□ (derivatives need representatives); degeneracy and swamps. |
| 11 | Qi 2005 cited for singular values | B | Agree. | Lim for singular values; Lim–Qi for Z-eigenvalues. |
| 12 | Thm 4.3: Γ^h undefined (observation) | B | Agree. | Γ^h and the normals defined; outer boundary noted. |
| 13 | Thm 5.1 "strictly attained"; Table 1 row; conclusion "rigorously" | B | Agree. | Fixed. |

## Chapter 2 (F-48)

| # | Item | Referee | Assessment | Action |
|---|---|---|---|---|
| 1 | Thm 6.2(ii) Dyson error bound false | A | **Agree** (C9, C9b re-run). | New bound, proved in full: \|Z_k − Tr P exp\| ≤ (r/k)(M + (a₁+a₀²)/2) exp(‖A‖_{L¹} + (M + a₁/2)/k). The factor e^{M/k} and the true L¹ norm are included; the Riemann sum is compared with the integral via the Lipschitz constant a₁ of ‖A(s)‖. Rate O(1/k) kept. The referee's example is stated as showing that e^{M/k} is needed. Check B1: random C¹ connections give max error/bound = 0.016; both referee examples lie within the new bound; the old bound fails. |
| 2 | Prop 4.2 graphon Laplacian | M | **Agree** (C7). | Hypothesis 0 ≤ W ∈ L^∞ added, with a proof (norm ≤ 2‖W‖_∞) and the two counterexamples (B3). |
| 3 | Table 2: Toda off-diagonal mass monotone | M | **Agree.** My own run: increases in 31/50 random 4×4 cases (B2), with an integrator control against Q^T A₀ Q. | Row now reads "spectrum invariant; off-diagonal mass → 0 as t→∞ (not monotone)". |
| 4 | Thm 6.1 cMPS, Remark, abstract | M | **Agree.** | Now "Proposition (formal derivation)". It uses the McLachlan functional (new reference), gives the normal equations g θ̇ = −½∇⟨H⟩ for **both** Q and R, and explains that g is degenerate (x-dependent GL(r) gauge, phase and normalization), that the system is consistent, and that the pseudo-inverse or a fixed gauge gives the same ray evolution. Energy identity with (H−E). The remark lists what is not proved (existence, regularity, stationarity of limit points). Abstract updated. |
| 5 | Thm 3.3(iii) tautological, proof incomplete | M | **Agree.** | Restated: if T* < ∞, then A(t) → A* with rank A* < r. Proof: Lipschitz gradient, Grönwall, Cauchy limit, escape lemma. Example with T* = 1 given. |
| 6 | Thm 2.2 curvature normalization; "strictly"; intro "negative" | B | Agree (C1). | Formula written as R(U,V,V,U)/\|U∧V\|²; equality iff the matrices commute; intro says "non-positive". |
| 7 | Thm 2.4 TT feasibility and gauge; Thm 2.5 P^L | B | Agree (C5b). | Feasibility r_α ≤ min(r_{α−1}d_α, d_{α+1}r_{α+1}) added, with the infeasible example; the proof now uses the free GL action and constant rank, and the residual gauge O(r_α). P^L_α and P^{LR}_α defined as in LOV. B5: Jacobian rank equals the formula for feasible ranks and differs (8 vs 12) for the infeasible case. |
| 8 | Thm 4.3 "three coefficients sum to 1" | B | Agree. | Stated as the convex combination of W₀, d₁, d₂, m (B4). |
| 9 | Prop 5.3 domain; "we proved coarea" | B | Agree. | Set on the torus T², with periodic extension and mollification, and a note on boundary terms; "recalled the classical coarea formula of Fleming–Rishel". |
| 10 | Table Ricci row; Rem 6.3 "exactly"; "operator norm" for a scalar | B | Agree. | Row is now conditional, on non-negative kernels; "converges as k→∞ for cores of form (6.x)"; the operator-norm statement is made for the matrix product. |
| 11 | TT/MPS citation; audit path in proof; Takatsu missing | B | Agree. | Oseledets 2011 cited; script references removed; Takatsu cited for curvature ≥ 0. |
| 12 | Companion title in bibliography differs from ch1 title | B | Agree that they differ. | **Left open** (see list below). |

## Chapter 3 (F-45)

| # | Item | Referee | Assessment | Action |
|---|---|---|---|---|
| 1 | Thm 3.2 torus representation false for m ≥ 3 | A | **Agree.** Recomputed by hand and in C3: 8/π vs 76/(3π²); the m=2 control agrees. | Representation removed. Remark 3.3 now states the failure, gives the counterexample, and explains why (the zero at y₁ = n+1). |
| 1a | I_m ~ m^x unproved | M | **Proved** rather than downgraded. | New proof of Thm 3.2 (J_m := m^{−x}I_m → 1) by Laplace's method / local limit theorem: uniform Stirling on the central region \|δ\| ≤ x^{3/5}, Gaussian density identified exactly, outer region bounded via Γ(z+1) ≥ c₀(z/e)^z and Pinsker. C5: I₃/3^x = 0.9835, 0.99975. |
| 2 | Thm 2.1 "faster than any power" proof invalid | M | **Agree.** | New complete proof of \|J − (2/π)Si(πx/2)\| ≤ C x^{−1/2} (integration by parts, Bernoulli). The O(2^{−x}) behaviour is now a remark stated as numerical only. The Cauchy-formula step is replaced by the classical cosine integral (Gradshteyn–Ryzhik §3.631), checked in C1 with a control. |
| 3 | Thm 5.10 moments: proof only gives O(x) | M | **Agree.** | Mean proved exactly by the S_m symmetry. Covariance proved to leading order (1+o(1)) via the local limit argument. The O(1) corrections are stated numerically in a remark, with the reason the absorption argument fails. |
| 4 | Rem 5.2 "discrete Stokes" reading | M | **Agree** (C7: Φ = x²y gives −2). | Replaced by the real reason (Φ = f(x)+g(y)+h(x−y)) and the counterexample. Subsection title, Table 1 and abstract updated. |
| 5 | Rem 7.3 "S_m-invariant" | M | **Agree** (\|LM₂Lᵀ−M₂\| = 5.33; covariance invariant). | Remark states S_{m−1} and k ↦ −k invariance; transpositions with y_m preserve Cov but not M₂. Abstract fixed; ch4 Conj 3.3 made consistent. |
| 6 | Abstract promises Chu–Vandermonde | M | Agree. | Removed; abstract rewritten. |
| 7 | Thm 5.4, 5.5 without proof | M | Agree. | 5.4 (L^p) proved by the same Laplace argument. 5.5 (Dixon) is now **Conjecture 5.5** with numerical ratios. The remark gives the Poisson-summation reformulation and shows that the Gaussian approximation cannot decide the question (64^x e^{−π²x/12} ≫ 27^x). |
| 8 | Thm 5.3 general α unproved; C_α unspecified | M | **Proved.** | Concavity via Cauchy–Schwarz, unique saddle, S* = ln(u/w), λ_α = u/w, explicit C_α. C6: ratios → 1 for α = 0.5 and 2 (error < 1e−7). |
| 9 | Thm 5.9 hockey stick vacuous | M | Agree. | Now Proposition 5.9: ∫ = C(x+1,r+1) + O(x^r), both terms ~x^{r+1}/Γ(r+2); proved. C9: difference/x^r → −0.376 (not o(x^r)). |
| 10 | Table 2 m=4 rows wrong | B | **Agree.** Two independent methods of mine (nested Gauss–Kronrod; Γ(x+1)·g^{*m} convolution with Richardson) agree to 7+ digits (C4). | 3.3626, 662.6556, 967463.2; errors 35.29%, 7.74%. Methods now described in the text. |
| 11 | Table 1 H(n); "Thm 5.2"; Stokes row | B | Agree (C8: superfactorial works, hyperfactorial fails). | sf(n) = G(n+2) defined; \ref labels used; rows updated for the new statuses. |
| 12 | Gould → Hoggatt–Hansell | B | Agree. | Hoggatt–Hansell 1971 cited (DOI verified); Gould kept for the gcd property. |
| 13 | Rem 5.6 "exact counterpart"; D^α called fractional operator on C¹([0,∞)) | B | Agree. | Asymptotic wording; operators renamed "averaging", defined on bounded continuous functions on R. |
| 14 | "Meromorphic continuation to C²"; Prop 1.4 zeros need x ∉ Z_{<0} | B | Agree. | Points of indeterminacy mentioned; hypothesis added. |
| 15 | Rem 7.4 (observation): essential spectrum {1/α²} | obs. | Agree. | Added, with the Hilbert–Schmidt argument. |
| 16 | Podlubny key "1998" vs year 1999 | B (cosmetic) | Key is not visible in output. | No change. |

## Chapter 4 (F-46)

| # | Item | Referee | Assessment | Action |
|---|---|---|---|---|
| 1 | Conj 3.3 "ground states exist" false | M | **Agree** (bounded kinetic term; D2 scaling check). | Conjecture restated as existence of a non-trivial L²∩L^∞ solution invariant under S_{m−1}×Z₂. The remark proves that inf E at fixed mass is −∞ for every p > 0 and says that "ground state" must come from another principle (e.g. Nehari). |
| 2 | Conj 3.3 symmetry group = S_{m−1}×Z₂ | INCERTO | Agree that maximality is unproved. | Now "this group preserves the operator; we do not know whether it is the whole linear symmetry group"; the ch3 Remark 7.3 fact is cited. |
| 3 | Rem 2.5(b) H⁴ with Navier on a simplex | M | **Agree.** | Domain = {u ∈ H²∩H¹₀ : Δu ∈ H²∩H¹₀} on convex domains (Grisvard); H⁴ only for smooth boundaries; Gazzola–Grunau–Sweers cited. The label on the Remark renamed. |
| 4 | Thm 2.6: (1/2mα)kᵀAk needs Σk = 0 | B | **Agree** (D1, both directions). | Parenthetical now gives the lattice formula S²/2m² + (Q−S²/m)/(2mα) and the constraint; "real-analytic" → "entire". |
| 5 | Def 2.1 u ∈ H² | B | Agree. | L². |
| 6 | Prop 2.3 "iff u constant" | B | Agree. | "iff u = 0", with a Plancherel proof. |
| 7 | α dimensionless and a length | B | Agree. | Dimensional convention (fixed unit ℓ₀) added to Rem 2.2. |
| 8 | Thm 3.2: V ≡ 0, k ≠ 0, "torus" title, resonant set | B | Agree. | All fixed; the non-emptiness condition stated precisely. |
| 9 | Thm 3.1 Fourier normalization; V time-independent | B | Agree. | Unitary FT convention and hypothesis stated. |
| 10 | Thm 4.2 atom of the propagator | B | Agree. | Atom E_β(−Kt^β/α²)δ described. |
| 11 | Rem 2.5(a) without reference | B | Agree. | Servadei–Valdinoci 2014 cited. |

## Chapter 5 (F-49)

| # | Item | Referee | Assessment | Action |
|---|---|---|---|---|
| 1 | Prop 5.1 inversion formula false | A | **Agree.** The data are restrictions g_θ(z) = h(P⁺_θ z), not n-plane integrals (referee block C). | Section retitled "Reconstruction from Restriction Data". New Proposition 5.1 (proved): h(x) = g_θ(P_θ x) for any θ ∋ x, and f = F⁻¹[ĥ/K̂(−·)]. The remark explains why FBP does not apply, with the referee's numbers. E2 checks the identity P⁺P x = x (control off-plane). |
| 2 | Thm 4.2 mass conservation hypothesis; label | M | **Agree.** | Interface condition Γ + Δ₃(α) ⊂ Ω (and Σ + Δ₂(β) ⊂ Γ) added. The operators are then shown to act within the domains and the adjoint relation holds exactly. Now "Proposition …; formal computation", with Neumann conditions stated. |
| 3 | Def 6.1 link to R; abstract (iii) | M | **Agree.** | Φ_α is now an independent construction (Dirichlet mean, user-chosen grouping); the text says it is not derived from R. The theorem is called a Lipschitz bound with sharp constant, and the absence of a lower bound is stated. Abstract rewritten. |
| 4 | Grassmannian promised in title and abstract | M | **Agree.** | Title now "… and Matrix Beta-Kernels"; §7 retitled and labelled as recalled classical facts; abstract (iv) rewritten. The ch6 bibliography entry updated. |
| 5 | γ = 1 not proved | M | **Agree; proved.** | Remark 3.2(c): proof by integration by parts on the polytope. Consequences given (R: L² → H^{1/2}), and used in the energy proof. E1: \|k\|\|K̂\| ≈ 1.84 constant for \|k\| = 25–100; control \|k\|^{1.5}\|K̂\| grows. Conclusion updated. |
| 6 | Eq. 1.1 indices vs Def 2.1 | B | Agree. | y_m defined; the one-dimension-higher convention of §2 stated. |
| 7 | "Definition~\ref{eq:…}" | B | Agree. | Label def:radon_beta added and references fixed. |
| 8 | §5 title "Gibbs Artifact Suppression" | B | Agree. | Retitled. |
| 9 | "Fourier Multiplier Representation" | B | Agree. | "Fourier Representation". |

## Chapter 6 (F-50)

| # | Item | Referee | Assessment | Action |
|---|---|---|---|---|
| 1 | Conj 2.3 vacuous | M | **Agree.** | Recast as **Problem 2.3** with explicit non-local forms on (K, μ): kernel κ_{α_k}(F_w⁻¹x − F_w⁻¹y) (symmetrized Beta kernel on Δ_m ⊂ R^m), integrated against μ⊗μ, with Mosco convergence to Kigami's form. The text explains why fixing the Beta kernel excludes the trivial answer. References updated. |
| 2 | Nodal lines of the reflection formula | B | **Agree** (F3: C(0.5,1) = 0.5). | Zeros only on y ∈ Z_{<0}, x−y ∈ Z_{<0}; parallelograms; triangles only with the pole lines. |
| 3 | R^{m−1} vs R^m | B | Agree. | Def 2.1 and Rem 2.4 use the kernel on Δ_m(α) ⊂ R^m, with the convention explained. |
| 4 | r_m = m+3 as "assumption" | B | **Agree; proved.** | Now Proposition 2.2 with a proof (symmetric harmonic extension: a = 2/(m+3), trace conductance (m+1)/(m+3)). F1: Schur complement gives exactly (m+1)/(m+3) for m = 2–5; control m/(m+2) fails. Label kept. Section title changed from "Homotopy" to "Decimations". |
| 5 | Kigami–Lapidus 1993 missing | B | Agree. | Added (DOI verified). |
| 6 | Rem 3.2: "α < ln 2" unnecessary; D₁ in nats | B | Agree (referee block E). | Restriction removed; the normalized value 1 − 1/(2 ln 2) given. |
| 7 | Prop 3.1 remainder | obs. | **Agree; derived.** | Remainder now −1/(180x²) + O(x⁻⁴), derived from the x⁻³ Stirling term and the B₄/8 Barnes term. F2: x²·(E − asym) → −0.0055555; the next remainder is O(x⁻⁴). Abstract and conclusion updated. |
| 8 | Audit script cited in text | B | Agree. | Removed. |

## Counts

| Chapter | Items | Fixed | Disputed | Open |
|---|---|---|---|---|
| 1 (F-47) | 13 (+1 sub-point) | 13 | 1 partial (C_λ growth is logarithmic, not λ^{−1/2}; text avoids the rate) | 0 in the chapter (see cross-chapter list) |
| 2 (F-48) | 12 | 11 | 0 | 1 (companion title) |
| 3 (F-45) | 16 | 15 | 0 | 1 cosmetic (Podlubny key, no visible effect) |
| 4 (F-46) | 11 | 11 (incl. the INCERTO item) | 0 | 0 |
| 5 (F-49) | 9 | 9 | 0 | 0 |
| 6 (F-50) | 8 | 8 | 0 | 0 |

## Items left open

1. **Companion title (ch2, B).** The ch2 bibliography cites ch1 as "Beyond the Spectrum: Functional Realizations of Matrices and Tensors, Emerging Invariants, and Geometric Measures" (the Zenodo record, DOI 10.5281/zenodo.22699282). The chapter title is "Functional Realizations of Matrices and Hypertensors: Emergent Invariants and Geometric Measures". The same entry appears in ch11, ch12 and ch13, which I may not edit, and the master book uses the chapter title. The author must choose one canonical title. Not changed.
2. **Chapters 7–13 (not editable here) that depend on changed statements:**
   - ch12 §(line ~436) writes the Kac–Rice complexity as exp(Nθ(k)). The ch1 Theorem 5.6 it cites (number unchanged) now gives θ(k) = ½ log(k−1) for k ≥ 3, for the isotropic (non-symmetric i.i.d.) model, and 2N critical points for k = 2.
   - ch12 (line ~150) states I_m(x) = m^x J_m(x) with lim J_m = 1. This is now true by definition, since ch3 defines J_m := m^{−x}I_m and proves the limit. The ch12 sentence should not suggest an oscillatory-integral representation.
   - ch12 (line ~172) says the Sierpiński value "rests on an imported decimation constant". The constant m+3 is now proved in ch6, Proposition 2.2.
3. **Master book chapter titles** (`master_book_unified_quantum_gravity.tex`, not in my file list) differ from the chapter files. For example, ch5 is listed as "Interdimensional Transforms, Barnes G-Function, and A_{m−1} Lie Algebra". They should be aligned with the chapter titles, including the new ch5 title.
4. **Open mathematics recorded in the text** (no fix possible): the O(2^{−x}) rate of 1 − J(x); the exponential rate of 1 − J_m(x); the O(1) corrections to the ch3 moments; the continuous Dixon asymptotics (Conjecture 5.5); the maximality of S_{m−1}×Z₂ and existence of solitary waves (ch4); Problem 2.3 (ch6).
5. **Podlubny bibkey `podlubny1998` vs year 1999** (ch3/ch4). This is cosmetic and invisible in the PDF, so it was left.
