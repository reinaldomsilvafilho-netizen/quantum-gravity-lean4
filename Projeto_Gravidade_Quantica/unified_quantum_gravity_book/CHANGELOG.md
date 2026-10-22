# Changelog — *Geometry, Tensors, and Quantum Gravity*

## v3.1.0 (2026-10-17) — contact components (ch. 7), dual certificate (ch. 9), exact numerical statements, F-02 checks, declarations

Findings F-01, F-02, F-12, F-21, F-23, F-24, F-28, F-29, F-64, F-65, F-66, F-67 in `WORKPLAN.md`. All versions: concept DOI `10.5281/zenodo.22290043`. The master volume has 250 pages.

### Chapter 7
- New subsection "Contact Sets of Planar Minimizers" at the end of Section 4.
  - Remark (computer-assisted, with a figure): the notched disc, an obstacle with two-sided positive reach whose unique minimizer at the tight length budget has infinitely many contact components. With slack, the same behaviour is shown numerically in a second-order model, and certified in that model for a convex variant at two values of the curvature level; the exact geometry with slack is supported by numerical evidence only. The remark also states, without proof, the supporting-disc mechanism and the separation of contacts on opposite sides under positive reach.
  - Proposition with proof: for a disc obstacle with $RK \le 1$, consecutive contacts of a curve with curvature at most $K$ are more than $\pi\sqrt{R/K}$ apart, and more than $\pi/K$ after an interior contact; finitely many such discs give finitely many contact components. A remark gives the sharpness at $RK = 1$ and a counterexample for $RK > 1$.
  - The abstract, the outline and the summary of status were updated to match.

### Chapter 9
- Remark after the search pipeline: a dual system (a costate of bounded variation and a contact measure, with the sign $D\lambda = +\nu\mu$) whose solutions satisfy a quantitative $\infty$-elastica inequality under an exterior-ball condition, and which exists for minimizers with finitely many isolated contacts on disjoint discs. Both statements are given as remarks with their mechanism, not as theorems. New reference: Moser, Amer. J. Math. 144 (2022).

### Chapters 2 and 10 — numerical statements made exact (F-65, F-66)
- Chapter 2: the transition law of the random walk is stated (simple lazy walk, uniform over neighbours, weights only through the distance); under the literal reading with step proportional to $1/\ell_e$ the quoted numbers are not reproduced.
- Chapter 10: the seeds (1000–1005 and 7), the teacher and the loss normalization are stated; the reported range is 1.57–1.75, inside the earlier 1.3–2.1.

### Numerical checks (F-02) and declarations (F-21, F-29)
- Checks of all thirteen chapters use an independent oracle and a negative control per claim. For Chapters 2, 4, 5, 8, 10, 11 the scripts were iterated against blind critiques until convergence: 71 statements verified, 0 failures, 10 exploratory, 27 not numerically checkable.
- Declarations confirmed by the author, with two added sentences: Lean toolchain and kernel replay; audit files.
- Layer-2 status pass: F-01, F-12, F-23, F-24, F-28 verified (Lean skeleton folders labelled; Theorem 3.1 of Chapter 12 with explicit constants; five DOIs resolved).

### Wording (F-67)
- Title page: a single subtitle, *From Simplicial Fractional Calculus and Minimax Foliations to Emergent Holographic Spacetime and Observational Signatures* (also in the PDF metadata).
- Decorative adverbs removed in Chapters 1 and 2 and in the preface; the text no longer refers to an internal repository file for the status of results (the Results Index is the reference).

### Build
- `build_pdfs_safe.py` now copies every `fig_*.pdf` and `fig_*.png` of the book folder into the single-source master build.

## v3.0.0 (2026-10-11) — chapter 14 salvage, operator consistency, statement repairs, references, single-source build

This version follows the previous correction release, v2.3 (2026-09-26). All versions: concept DOI `10.5281/zenodo.22290043`.
Full details, with evidence and scripts, are in `WORKPLAN.md` (findings F-01, F-02, F-15, F-19, F-20, F-24, F-46 to F-52, F-58, F-59 to F-63).

### Chapter 7
- The abandoned Chapter 14 material (written outside the master volume, see F-52) was salvaged in three pieces, each integrated and layer-2 checked separately:
  - A proposition bounding the extrinsic curvature of a closed submanifold confined to a ball ("Closed submanifolds cannot be squeezed") and an accompanying remark that an $L^\infty$ bound on the second fundamental form rules out Nash–Kuiper-type corrugations, with the compactness results of Langer and Breuning cited for the regularity this gives.
  - A chattering block: a lemma on the structure of time-optimal trajectories against a wall constraint, with a full proof, a definition of the associated boundary-contact problem, and a conjecture on the non-existence of time-optimal chattering controls for that problem. The order-3 chattering phenomenon is credited to Robbins (1980), with further prior art from Fuller, Zelikin–Borisov, Sussmann and others.
  - The regularity-invariance conjecture of Chapter 7 is refuted as it was previously stated (an explicit obstacle example at the threshold length $V_0$ gives a non-empty $C^{1,1}$ class and an empty $C^r$ class for every $r \ge 2$) and restated for $V > V_0$. New results proved alongside it: a smoothing lemma away from the obstacle; regularity invariance for curves without obstacles, for every regularity class and for both embedded and immersed curves; a classification of $C^2$ minimizers of the planar Dubins-type problem; and a bound tying the $C^2$ excess curvature to a Lipschitz constraint on the curvature's derivative, with numerically fitted rates by Dubins word type.
- References: 2 new co-attributions (Fáry, Radó) and a page-range correction (Sussmann 1995).

### Chapter 9
- A proposition on an embedded "teardrop" U-turn through a narrow mouth into a convex balloon-shaped region, salvaged from the abandoned Chapter 14 material. The depth formula used in the construction is the classical Omega-turn depth and is cited as such, not claimed as new; the chapter's own contribution is the minimality statement inside the balloon and the corridor scenario built on it.

### Chapters 2, 11, 12, 13 and the Dictionary — operator consistency
Propagation, across these chapters and the Dictionary, of results on the two-scale symbol $k^2 + \ell^2 k^4$ used for the spectral-dimension model:
- The heat-kernel argument for the model is restricted to a reading in four Euclidean dimensions; nothing in the chapters or in the simplicial construction of this book supplies the symbol with Lorentzian dynamics.
- A no-go statement: no refinement or rescaling of the book's simplicial Beta-kernel operators (Chapters 3–4) produces the quartic term, because their symbols remain negative definite; the two-scale symbol is an assumption, not a derivation.
- A Källén–Lehmann positivity obstruction, using the classical Källén–Lehmann representation and the Osterwalder–Schrader reconstruction theorem, rules out a local, ghost-free, Lorentz-invariant completion of the symbol with a positive spectral weight.
- A Lee–Wick/fakeon-type completion is recorded as the remaining route that is local and Lorentz-invariant: it gives up positivity of the spectral weight instead.
- Corrected bounds on the mass scale $M_\ast$: in the anisotropic $z=3$ realization, $M_\ast$ cannot be the Planck mass, and the bounds that apply to it are stated using GW170817, GWTC-3, LHAASO and Crab-nebula constraints.
- The graphon-condensation conjecture (Chapters 11, 12 and the Dictionary; Chapter 2 supplies the underlying flow) is restated with an explicit hypothesis on the initial kernel's degree, leaving the choice of metric on $[0,1]$ defining the curvature as a hypothesis that one exists rather than an explicit metric, together with a remark giving the precise reasons it is not a theorem (cut-metric limits of graphons carry no differentiable structure, and sparse graphs converge to the zero kernel, where the flow is undefined).
- An unpublished "niche" result on Ollivier curvature of graphons, previously cited in Chapter 2, was removed from the citation; the chapter now states the expected limit as an explicit, unproved expectation instead.

### Chapters 7, 10 and 12 — statement repairs (F-59)
Three statements were found, while preparing Lean formalizations, to claim more than their proofs give; each was repaired, and the repair independently re-checked:
- **Chapter 10**, Proposition `prop:counterexample`, item (2): the lower bound 1/2 on the generalization gap of the interpolating least-squares solution was stated for every distribution of the inputs. It fails for degenerate inputs (for x ≡ 0 the gap is 0). The proposition now assumes that the data matrix has full row rank N, and item (2) holds for every input distribution under which this happens almost surely, for instance any distribution with a density; the chapter abstract was changed to match, and the degenerate case is recorded in the text as an example.
- **Chapter 12**, Theorem `thm:neckpinch_condensation`: the conclusion that the kernel stays below δ on B now holds for almost every point of B (and all times after t_δ), not at every point; the proof's last step, W₀ ≤ ‖W₀‖_{L∞(B)}, holds only almost everywhere.
- **Chapter 7**, Remark `rem:nash_kuiper`: the corrugated example closes up for every amplitude β > 0 and every N ≥ 2 (by the Jacobi–Anger expansion); the first zero of J₀ is needed only for confinement at distance O(1/N). The remark previously attributed closure to that zero.

### Chapters 1–5 and the Dictionary — further statement repairs (F-60)
Six further statements, found while continuing the Lean inventory, were repaired, each independently re-checked:
- **Chapter 1**: the Grothendieck/hypergraphon argument was missing the step bounding the maximum over indicator functions; the step was added.
- **Chapter 2**, Theorem `thm:toda_qr`: the proof was circular and gave no uniqueness statement; a new proof is given, with uniqueness.
- **Chapter 2**, Proposition `prop:tangent_proj_mr`: stated without proof or citation; a citation (Vandereycken 2013) and a proof sketch were added.
- **Chapter 5**, the Inversion theorem: carried an unnecessary hypothesis $\hat K \neq 0$; removed, using an argument from the zero set of an entire function ($\hat K$ entire, $\hat K(0) = 1$).
- **Chapter 3**: the PDE for the Digamma function did not state its domain; a domain and the holomorphic extension are now given.
- **Chapter 4**, the modulational-instability theorem: the stability criterion was missing the lower bound $0 < \sigma$; a wavevector with $\sigma(\mathbf k) = 0$ gives $\Omega = 0$, not instability. The criterion now reads $0 < \sigma(\mathbf k) < 4M\kappa p\rho_0^p/\hbar^2$.
The Dictionary entries touched by these chapters were aligned to match.

### Chapters 12 and 13 — rounding of three upper bounds
Three literal upper bounds quoted to two significant figures did not in fact bound the quantities they were attached to, because the exact supremum rounds to a higher two-figure value: $H_{\mathrm{inf}} \le 4.7 \times 10^{13}$ GeV, $\ell_\ast < 4.8 \times 10^{-31}$ m, and $|\alpha_t| \le 3.7 \times 10^{-10}$ (for $M_{\mathrm{red}}$). All three are restated to three significant figures, rounded upward as an upper bound requires: $4.71 \times 10^{13}$ GeV, $4.82 \times 10^{-31}$ m, and $3.74 \times 10^{-10}$. The fourth bound in the same passage, $|\alpha_t| \le 1.5 \times 10^{-11}$ for $M_P$, was already valid and is unchanged. No physical conclusion changes; the affected places are Chapter 12 (Experimental Signatures section) and Chapter 13, and the corresponding entry of the Dictionary.

### References
All 13 chapters were re-audited for citations against Crossref, DataCite, zbMATH and arXiv. Corrections include wrong JFM identifiers (Barnes 1900, Dixon 1891), wrong page ranges (Källén 1952, Israel 1966, Lucas 1878, Radó 1930), DOIs attached to the wrong edition (ADM 1962, Muirhead 2009), and an overclaimed attribution (Zhao 2015, downgraded to its correct chain of sources). Over 20 references were added or corrected in total, including new co-citations for results in Chapters 1, 2, 5, 6, 7, 8, 10, 11, 12 and 13.

### Numerical checks
The four chapter-level verification scripts flagged by the previous layer-2 check (Ch. 4, 6, 8, 11) had a tautological or stale check each; all four were rewritten with an oracle independent of the formula under test (direct quadrature of the stated definitions, symbolic re-derivation via computer algebra, or an independent Monte Carlo), each with a negative control confirmed to fail. Every chapter's numerical suite now uses an independent oracle and a negative control for every claim checked (F-02).

### Preface and declarations
- The preface and the Dictionary no longer point to an unpublished, non-public folder as the home of the Mathlib formalization effort (F-58); both now state that a formalization against Mathlib already covers selected results, listed with their axiom check in `formal_proofs_mathlib/README.md`, and continues to grow, and that only results published with their Lean statement and axiom check should be regarded as machine-checked.
- A real, if partial, Mathlib formalization of selected results now exists in `formal_proofs_mathlib` in the public repository, covering Chapters 1, 2, 3, 7, 9 and 12 (Chapter 3: Stifel's identity, the Star of David identity, zero counts, positivity, row sums; Chapter 12: the constraint bounds, at the level of a matrix inequality with the ADM constraint taken as a hypothesis; Chapters 1, 2, 7 and 9: the Dirichlet-energy blindness ratio, the finite-graph Dirichlet energy, the curve ball bound and the mouth half-turn, each a declared special case) and five companion works (Simplicial Quantum Gravity, Yang-Mills, fermion masses, Beyond the Spectrum I-III, Functorial Bridge). Since 2026-10-09 the formalization also covers, for Chapter 9, the bound ∫|θ'| ≤ ∫|κ| + π with sharp constant (`prop:winding_total_curvature`, for C² curves; the winding bound is conditional on the identity of `thm:loop_bounding`(1)), and, for Chapter 8, the pointwise algebraic part of the Sectional-Extrinsic Coupling theorem and of `prop:raychaudhuri`, `prop:rn_horizon`(2), `prop:wormhole_throat`(2)–(3) and `prop:proper_accel`, with the Gauss, Raychaudhuri and Einstein equations taken as named hypotheses. The declarations now list Chapters 1, 2, 3, 7, 8, 9 and 12. The declarations block of every chapter was updated to state this precisely and is now aligned with the Leiden Declaration on Artificial Intelligence and Mathematics.

### Chapter 11 (F-62)
- Remark "SLD versus Kubo--Mori" (`rem:sld_vs_bkm`): the claim that the commuting-case common value of the two metrics reduces to the classical Fisher–Rao form $\sum_i X_{ii}^2/p_i$ is corrected to give the basis-free value $\operatorname{Tr}(\rho_0^{-1}X^2)$ first; for a repeated eigenvalue of $\rho_0$, an $X$ commuting with $\rho_0$ need not be diagonal in the chosen eigenbasis (counterexample $p=(1/2,1/2)$, $X=\sigma_x$: 4 against 0). The gap was found by the Lean formalization (batch B7) and independently re-checked.

### Lean coverage update (batches A3 and B7)
The Mathlib formalization in `formal_proofs_mathlib` was extended to further results of Chapters 1, 2, 4 and 5, and to selected results of Chapter 11: the linear-algebra half of the minimum-cut entanglement-entropy bound (the tensor-network factorization taken as a hypothesis), the commuting-case Hessian identity of the relative-entropy/first-law proposition, and the BKM $\ge$ SLD inequality for full-rank $\rho_0$ in its eigenbasis. The declarations block of every chapter now lists Chapters 1–9 and 11–13. A further round of batches (B1–B9, A1–A3, A-B2 to A-B5, and the final hypergraphon/fermion round) extended the coverage to Chapter 6 and to Chapter 10 (`Chap10Generalization`), so that selected results of Chapters 1–13 are now covered; the preface states this as "selected results of Chapters 1–12 and the numerical bounds of Chapter 13", each at the level declared in `formal_proofs_mathlib/README.md`.

### Chapter 2 (F-63)
The worked example after Theorem `thm:continuous_path_integral`(ii), showing that the factor $e^{M/k}$ in the error bound cannot be dropped, set $\mathcal{R}_j \equiv M$ without requiring $M > 0$. At $M = 0$ the claimed strict excess of the error over $M/k$ fails (the error is exactly $0 = M/k$). The example now reads $\mathcal{R}_j \equiv M > 0$; neither the bound (2.54) nor parts (i) and (iii) are affected. Found and independently re-checked (exact-rational oracle; negative control at $M=0$) during the book-closing pass below.

### Book-closing pass (Dictionary, Results Index, Part titles, single-source front matter)
Following the project's closing procedure for a book version:
- The Dictionary of terms and symbols (`DICTIONARY_TERMS_AND_SYMBOLS.tex`) was checked entry by entry against the current chapters and rewritten: hypotheses, constants and statements touched by F-59 to F-63 were updated; new rows were added for symbols used repeatedly but previously undocumented ($\mathcal{H}$, $\mathcal{E}$, $\mathcal{M}^{\mathrm{TT}}_{\mathbf r}$, $\gamma_A$, $\rho_A$, $\Sigma_t$, $\mathscr{H}_J$); and entries were added for the material salvaged from the unintegrated draft chapter (the teardrop/balloon U-turn, the wall-structure lemma, the ball bound).
- A new backmatter appendix, "Results Index and Verification Status" (`appendix_results_index.tex`, generated by `gen_results_index.py`), lists all 112 Theorem/Proposition/Lemma/Corollary environments of Chapters 1–12, one row per result, with its proof status (text, cited as classical, or sketch), its numerical check if any, its Lean module and declared reduction (taken verbatim from `formal_proofs_mathlib/README.md`), and its WORKPLAN verification status. An independent layer-2 re-check of the index (`audit/verify/L2_FECHAMENTO_LIVRO_2026-10-11.md`) found one cell overstating a proof (Chapter 1's hypergraphon-compactness theorem, cited from Lovász–Szegedy, was marked "text" instead of "cited"); corrected, together with two related wording refinements.
- The titles of Part IV and Part V were softened to "Emergent Spacetime: Established Results, Conjectures, and Heuristics" and "Observational Signatures: Order-of-Magnitude Estimates", to match the conjectural status of their content.
- The preface's "Principal Results" and "Status of the Verification Material" sections, and the Declarations, are now drawn from the single live source used by the master build, rather than from a hand-kept copy in the structural template, so the front matter cannot drift from the chapters again.
- Two residual defects were fixed: an orphaned footnote marker at the opening of Chapter 8 (a leftover `\thanks` with no `\maketitle` to anchor it in the master), and three places where a cross-chapter reference printed the standalone-chapter-PDF numbering instead of the master's own numbering (a new `\xref` macro resolves to the right number in each context).

### Build
The master volume is now assembled by a single-source pipeline (`\input` of the 13 chapter sources into one document with one preamble and one bibliography) rather than by stitching together 13 separately compiled PDFs (F-19). After the statement repairs and the book-closing pass above, the master is 248 pages; it compiles with 0 errors, 0 warnings, 0 overfull boxes and 0 undefined references. A legacy build mode that reproduces the old stitched assembly remains available.

## v2.3 (2026-09-24) — correction release

This version corrects errors found in a reaudit of v2.2 (Zenodo version DOI `10.5281/zenodo.22888334`, 2026-09-22). All versions: concept DOI `10.5281/zenodo.22290043`.
Full details, with evidence and scripts, are in `WORKPLAN.md` (findings F-01 to F-32).

### Corrections of mathematical and physical content
- **Ch. 12** now separates proved results (Propositions/Theorems) from conjectures throughout, and its title, abstract, introduction and conclusion were rewritten to match.
  - Spectral dimension: $d_s = m/\alpha$ for a homogeneous symbol is constant; running requires a two-scale symbol. Prior art is now cited (Hořava 2009; Sotiriou–Visser–Weinfurtner 2011; Carlip 2017). The closed form for $d_s(\tau)$ is unchanged and was verified by quadrature.
  - Barycentric Hessian / $A_{m-1}$: corrected factor ($m/2x$), explicit root coordinates, and the "emergence of gauge symmetry" reading removed.
  - ADM constraint bounds: matter term $16\pi G\rho$ added; "avoids crushing singularities" removed (it assumed $\kappa^*<\infty$).
  - Jordan loops / LQG: chronology constrains timelike curves only. The restriction to Jordan loops is now a conjecture (Conj. 4.3), and the Mandelstam identity is corrected.
  - Ryu–Takayanagi via mean curvature flow and Kac–Rice/horizon entropy are now conjectures. The claim that SYK-type models saturate the chaos bound at finite coupling was corrected.
  - Graphon Ricci flow: sign made consistent with Ch. 2 ($\partial_t W = 2\kappa W$); the impossible hypothesis $\kappa \le -c/\epsilon$ was removed (Ollivier curvature is bounded below); "condensation into a 4D Einstein manifold" is now a conjecture.
  - §7: the Jarlskog-invariant formula was **withdrawn**: it was dimensionally inconsistent and evaluated to $10^{-17}$. The free-parameter count is now stated, and the Higgs value is labelled as a fit.
  - §8.3: the RT hemisphere is totally geodesic ($H=0$); the claimed shrinking self-similar solution was incorrect and has been removed.
  - §8.6: the Jacobi closed form was replaced by the elliptic quadrature; "stabilized/minimized exotic matter" removed.
- **Ch. 13** was rewritten as an order-of-magnitude assessment. With $\ell_\ast=\ell_P$, the GW dispersion delay is $\sim10^{-61}$ s (v2.2 said "approaches the millisecond threshold"), and the tensor-tilt running is $\lesssim10^{-115}$ at CMB scales (v2.2 said "testable by LiteBIRD/CMB-S4"). The atom-interferometry proposal was withdrawn. The figure is now generated by `audit/scripts/observability_estimates.py`.
- **Ch. 8**: every statement that previously had no proof is now proved, corrected, cited as classical, or marked as a conjecture.
  - New proofs: space-form coupling, Euclidean U-turn bound $2/w$, pointwise ADM bounds, Raychaudhuri obstruction, proper acceleration $=\mathrm{II}$, topology of multi-black-hole slices, causal constraints.
  - Corrected: the wormhole throat is a *minimal* surface of its static slice, with an NEC bound through its intrinsic curvature; the horizon curvature $1/r_+$ holds for RN/Schwarzschild in Painlevé–Gullstrand slicing and is slicing-dependent; winding classes about horizons exist only for planar motion; the GHY bound was missing a factor of 3.
- **Ch. 1**: the "roughest checkerboard" example was misleading (a matrix with the same Dirichlet energy exists); the claim of bypassing the De Silva–Lim ill-posedness is false for rank $\ge 2$; the explicit Kac–Rice constant did not match Auffinger–Ben Arous–Černý and was removed; tensor-graphon compactness now cites Zhao 2015.
- **Ch. 2**: Toda at integer times is QR on $e^{A_0}$ (not on $A_0$); Bures–Wasserstein metric off by a factor 2; the proof of cut-norm contraction for the graphon heat equation was invalid and is replaced by an exact solution; the graphon "neckpinch" is now a conditional proposition; the cMPS gradient flow converges to stationary points, not necessarily the ground state; trace order in the tensor-ring holonomy corrected.
- **Ch. 3**: the expansion $\mathcal J(x) = 1 - 1/(2x) + \dots$ is false ($\mathcal J \to 1$ faster than any power); the "exact boundary defect relation" is now a heuristic remark; the closed symbol, the semigroup law and the "Cartan" long-wavelength limit hold only for the lattice construction and were withdrawn for the continuous kernel; the matrix is the Gram matrix of $A_{m-1}$ roots; the continuous Laplacian is bounded, so the stated Weyl law was withdrawn.
- **Ch. 4**: the spectral fractional Laplacian does not coincide with the integral one on bounded domains, and its square has Navier (not clamped) conditions; the symbol and mean-square-displacement coefficient inherited from Ch. 3 were corrected; the $S_m$-soliton theorem is now a conjecture.
- **Ch. 5**: dimension mismatch in the Radon–Beta kernel fixed; the trace gain equals the fractional order only for $\alpha \le 1$ (general rate $\gamma$ now explicit); the "isomorphism" at $\alpha^*$ was withdrawn (traces are never injective); the sign of the dual extension was wrong; inversion is ill-posed (the kernel does not suppress Gibbs ringing).
- **Ch. 6**: the chapter did not compile (missing conjecture environment); the Weyl law holds with two-sided bounds, not as an asymptotic equivalence; the row-entropy expansion now has its exact $-\frac16\ln x + 2\zeta'(-1) - \frac1{12}$ term; the resolvent convergence to Kigami's Laplacian is a conjecture; the multifractal spectrum is a heuristic (its "confirmation" was circular); Pascal mod 2 now has a proof by self-similarity.
- **Ch. 7** (largely rewritten): withdrawn as false, with counterexamples: the boundary curvature floor (inequality reversed), the obstacle exclusion principle (fails for convex obstacles; replaced by a proved contact principle with the correct sign), the sagitta bound, the optimality of the cylinder, the isotropy of calibrated submanifolds, the helix curvatures and the calibrated rows of the $n \le 12$ table, the "corner correction". Regularity invariance, discrete $\Gamma$-convergence and the positivity of the saturated set are now conjectures. New proofs: existence for curves, knot curvature gap, Dubins duality, Gauss–Bonnet floor.
- **Ch. 8** (second pass): the non-Euclidean regularity invariance is a conjecture (its proof was invalid); the table lists candidates, not minimizers (AdS row removed; FLRW value is $H$, not $3H$).
- **Ch. 9** (largely rewritten): the finite winding cutoff without a length bound is false (finiteness is now proved under a length bound); mapping classes do not act by conjugation on holonomy; obstacle complements in $n \ge 3$ do not retract onto a free 1-complex; the $\Gamma$-convergence "global certitude" theorem and the "Frenet convexification" theorem are withdrawn (conjecture / remark); **the 50.6% embedded-vs-immersed benchmark gap is false**: both classes have optimal curvature $1/H$.
- **Ch. 10** (rewritten): the Hessian-trace and PAC-Bayes generalization bounds in terms of $\kappa^*_{\mathrm{info}}$ are false (counterexample: linear regression with random labels); the Stiefel/polynomial-time statement is a conjecture; K-FAC cost corrected.
- **Ch. 11** (rewritten, new title): QFI definition off by a factor 2; the relative-entropy Hessian is the Kubo–Mori metric, not the SLD metric; the linearized Einstein theorem is attributed to Faulkner–Guica–Hartman–Myers–Van Raamsdonk, and the nonlinear completion does not follow from positivity; the cMERA AdS metric, continuum Ryu–Takayanagi via MCF and graphon condensation are conjectures; graphon Ricci flow sign corrected; the Kac–Rice formula was wrong (fails at $k=2$) and is replaced by the Auffinger–Ben Arous–Černý rate.
- **Dictionary** updated to match: every core formulation is now labelled proved, conjectural or ansatz.

### Independent verification (2026-09-25/26)
Every chapter was re-audited by a referee that did not write it, corrected in a separate pass, and re-checked. Main results of this round:
- **Ch. 13**: the GW dispersion delay carries a factor (1+z)² (delays 6×10⁻⁶²–1.2×10⁻⁶⁰ s at z = 1–8); the tensor-tilt running is evaluated at the horizon-exit scale H_inf (|α_t| ≲ 1.5×10⁻¹¹). Both remain far below observability. Figure regenerated.
- **Ch. 12**: the closed form of d_s(τ) was already given by Sotiriou–Visser–Weinfurtner (2011) and is now credited to them; Fefferman–Graham coefficients corrected; the RT/mean-curvature-flow and Jordan-loop conjectures restated; the circulant flavour ansatz stated as an assumption (it gives a trivial CKM matrix).
- **Ch. 8**: tube curvature in Hⁿ is c·coth(cd); the U-turn bound in H² and S² is now a theorem with proof; sign conventions fixed; winding classes of timelike curves are finite.
- **Ch. 1–6**: Kac–Rice restated for the isotropic model (rate ½log(d−1)); a corrected Dyson error bound; the torus representation of the continuous multinomial removed and I_m(x) ~ m^x proved; energy of the simplicial NLS unbounded below at fixed mass; a correct inversion formula for the Radon–Beta transform; r_m = m+3 proved; the Kigami convergence problem reformulated.
- **Ch. 7, 9–11**: new proofs (contact principle for C^{1,1}, winding bound ∫|θ'| ≤ ∫|κ| + π); several conjectures restated so they are not trivially true or false; attributions corrected (Miyaji et al. 2015, Immirzi, Faulkner et al. 2017).
- Chapter titles and cross-references unified across the volume.

### Verification material and declarations
- The preface no longer claims "144 machine-checked obligations". The Lean modules in `formal_proofs_book/Book` are disclosed as a naming skeleton that verifies no mathematics.
- The numerical tests for Ch. 12–13 were rewritten with independent oracles and negative controls.
- Added declarations (funding, competing interests, detailed use of generative AI tools, code/data availability) to the master volume and to every chapter. The license statement is now consistent with Zenodo (CC BY 4.0).
- The chapter texts no longer describe their own revision history; this file and `audit/chXX_claims.md` record it.
- References: 171 bibliography entries were checked against Crossref/DataCite. Corrected DOIs or titles: Koide 1982, LiteBIRD 2019, Willmore 1965, Hirani 2003, Azagra–Ferrera 2006, Samko et al. 1993, Falconer 2014, Ambjørn–Jurkiewicz–Loll 2005, Ryu–Takayanagi 2006, Langer 1985 (Ch. 7–9), Wardetzky et al. 2007. New references are verified.

### Known open issues (see WORKPLAN.md)
- All chapters have been re-audited once; the corrections still await an independent second check (see WORKPLAN.md, four-eyes rule).
- Real Lean/Mathlib formalization and the Python tests for Ch. 1–11 are still pending.
- The master volume is still assembled from per-chapter PDFs.
