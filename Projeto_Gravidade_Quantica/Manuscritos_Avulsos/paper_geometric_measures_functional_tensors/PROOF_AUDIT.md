# Proof Audit: "Beyond the Spectrum II" — Adversarial Review

## 1. Executive Summary & Publishability Verdict

**Status: Major Revision (not Reject, not Ready).**

The manuscript is ambitious and stylistically fluent, correctly invoking real theorems (Benamou–Brenier, Bakry–Émery/von Renesse–Sturm, Chazal et al. algebraic stability, Connes' trace theorem, Cheeger–Federer) in plausible settings. However, the audit surfaced **one outright false worked example** (Theorem 3.2's proof does not produce the topology it claims), **one internally self-contradictory hypothesis/scaling argument** (Theorem 4.1(b)), **one well-known false equivalence in quantum information geometry** (Theorem 6.2(b)), and **a global domain inconsistency** between the flat-cube setting fixed in Section 2 and the "closed spin manifold" silently assumed in Section 6. Several other theorems (2.1, 2.2, 3.1, 4.1(a)) have real but repairable regularity/hypothesis gaps (boundary conditions, tameness, non-degeneracy). None of these are fatal to the underlying *ideas* — most are fixable with added hypotheses or corrected constants — but as written, at least two theorems make claims their own proofs do not establish, which is disqualifying for publication in the target venues without revision.

Novelty/depth: genuinely interesting synthesis (optimal transport + TDA + GMT + microlocal + NCG + QI applied to a "functional realization" of matrices), but the six sections are largely independent transplants of standard machinery into a new setting, each requiring the *hard* regularity work (non-degeneracy, boundary conditions, tameness) that is currently glossed over.

---

## 2. Structured Issue Ledger

**Issue 1**
- status: INVALID
- impact: GLOBAL
- category: CASE_INCOMPLETE
- location: Section 3, Theorem 3.2 (Isospectral Separation Theorem), proof
- statement: The proof claims that for $B = PAP^T$, the cells of magnitude $\ge 1$ — located at grid positions $(1,1), (3,3), (1,3), (3,1)$ — "form four isolated corners... creating a non-contractible topological ring enclosing the central low-value pit," giving $H_1(X_t(B);\mathbb Z_2)\cong\mathbb Z_2$.
- why_invalid_or_gap: With $\Omega_{ij} = [\frac{i-1}4,\frac i4]\times[\frac{j-1}4,\frac j4]$, the four "hot" cells sit at grid coordinates that are each *two cells apart* in every direction (e.g. $(1,1)$ and $(1,3)$ are separated by cell $(1,2)=0$; $(1,1)$ and $(3,1)$ by $(2,1)=0$), and none share even a corner point. The text's own description — "four **isolated** corners" — is definitionally a disconnected union of four contractible squares ($\beta_0 = 4$, $\beta_1 = 0$), not a connected annulus. A ring requires connected material enclosing a hole; four mutually disjoint blobs cannot produce one. This is a direct self-contradiction inside the proof (it asserts "isolated" and "ring" of the same configuration).
- counterexample: YES — recomputation of $B=PAP^T$ from the given $A$ and $P$ (swap indices 2,3) confirms $B_{11}=2,B_{33}=2,B_{13}=B_{31}=1,B_{22}=B_{44}=-1$, all other entries 0, placing the four high-value cells at mutually non-adjacent grid positions.
- affects: The entire proof strategy of Theorem 3.2, the paper's flagship claim that "functional topological invariants strictly separate isospectral matrices" via $H_1$/persistent entropy in degree 1; also undermines confidence in Table 1's row for $\mathrm{Dgm}_k(A)$ "breaks isospectrality."
- minimal_fix: Either (i) choose a permutation that genuinely produces an adjacent 4-cycle of high-value cells around a low central cell (e.g. place the off-diagonal high entries at $(1,2),(2,3),(3,4),(4,1)$-type adjacent pattern), or (ii) abandon the $H_1$ argument and instead prove separation via $H_0$ (the number of connected components already differs: $\beta_0(X_t(A))=1$ vs. $\beta_0(X_t(B))=4$ for small $t>0$), redefining the theorem to use $E_{\mathrm{pers}}^{(0)}$ instead of $E_{\mathrm{pers}}^{(1)}$.

**Issue 2**
- status: OVERSTATED
- impact: GLOBAL
- category: CONSTANT_DEPENDENCE_HIDDEN
- location: Section 4, Theorem 4.1(b) and its proof
- statement: "$A_k$ ... represents checkerboard oscillations of frequency $k$ and **fixed amplitude $\epsilon$**," with $\|A_k\|_F = O(1)$, and $\mathcal W(\Phi(A_k)) = \Theta(k^2)$.
- why_invalid_or_gap: The proof computes $\mathcal W(\Phi(A_k)) \sim \epsilon k^3$ for genuinely fixed $\epsilon$, then silently substitutes $\epsilon \sim 1/k$ ("to keep gradient $L^1$ bounded") to land on $\Theta(k^2)$. But the hypothesis explicitly says $\epsilon$ is *fixed*, and separately asserts $\|A_k\|_F = O(1)$ — with genuinely fixed pointwise amplitude $\epsilon$ and grid size scaling with $k$ (needed to represent frequency $k$), $\|A_k\|_F$ actually grows with $k$, not $O(1)$. The two hypotheses ("fixed $\epsilon$" and "$\|A_k\|_F=O(1)$") are mutually inconsistent, and the proof needs the second (Frobenius-normalization) reading to get its stated rate. With truly fixed $\epsilon$, the correct rate is $\Theta(k^3)$, not $\Theta(k^2)$.
- counterexample: YES — direct substitution of fixed $\epsilon$ into the proof's own scaling chain yields $\Theta(k^3)$, contradicting the theorem statement.
- affects: The claimed comparison "Willmore energy penalizes wrinkling more strictly than $H^1$ Dirichlet energy" (the exponent itself is wrong under the stated hypotheses); the applications section's claim about Willmore regularization in deep learning implicitly relies on this rate.
- minimal_fix: Replace "fixed amplitude $\epsilon$" with "Frobenius-normalized amplitude $\epsilon_k = \Theta(1/k)$ so that $\|A_k\|_F = \Theta(1)$," and state the theorem for that normalization; note the (also true, but different) $\Theta(k^3)$ result for literally fixed pointwise amplitude.

**Issue 3**
- status: UNJUSTIFIED
- impact: GLOBAL
- category: HIDDEN_ASSUMPTION
- location: Section 6, Theorem 6.2(b), proof
- statement: "$g^{\mathrm{QFI}}_{\mu\mu}(x) = 0$ if and only if $\partial_\mu \rho(x) = 0$."
- why_invalid_or_gap: This equivalence fails whenever $\rho(x)$ is rank-deficient. In the eigenbasis $\rho = \sum_i \lambda_i |i\rangle\langle i|$, $g^{\mathrm{QFI}}_{\mu\mu} = \sum_{i,j:\,\lambda_i+\lambda_j>0} \frac{2|\langle i|\partial_\mu\rho|j\rangle|^2}{\lambda_i+\lambda_j}$ — terms with $\lambda_i=\lambda_j=0$ (both in the kernel of $\rho$) are excluded from the sum entirely, regardless of whether $\langle i|\partial_\mu\rho|j\rangle \ne 0$ there. This is the well-documented discontinuity/degeneracy of the QFI (Bures) metric at the boundary of state space (rank changes), so $g^{\mathrm{QFI}}_{\mu\mu}$ can vanish or misbehave even with $\partial_\mu\rho \ne 0$ supported in directions tangent to rank changes. The claimed iff requires an unstated full-rank ($\rho(x) \succ 0$ for all $x$) hypothesis.
- counterexample: CANDIDATE — any smooth family $\rho(x)$ that changes rank at some $x_0$ (e.g. purifying/depurifying a bond dimension) produces a direction where $\partial_\mu\rho \ne 0$ is concentrated in the emerging kernel block, with $g^{\mathrm{QFI}}_{\mu\mu}(x_0)$ not reflecting it correctly.
- affects: Theorem 6.2(b)'s characterization of "entanglement faithfulness," and by extension Definition 6.3's entanglement contour, which multiplies $S_{\mathrm{vN}}(x)$ by $\sqrt{\det g^{\mathrm{QFI}}(x)}$ — at rank-deficient points this product can misrepresent local entanglement.
- minimal_fix: Add hypothesis $\rho(x) \succ 0$ (full rank / no spectral gap closing) for all $x \in \Omega$, or explicitly restrict Theorem 6.2 to the interior of the manifold of full-rank density matrices and cite the QFI-discontinuity literature (e.g. Šafránek, *Discontinuities of the quantum Fisher information and the Bures metric*) for the boundary case.

**Issue 4**
- status: UNJUSTIFIED
- impact: GLOBAL
- category: HIDDEN_ASSUMPTION
- location: Section 6 (whole section), especially Theorem 6.1
- statement: "Let $(\Omega, g)$ be a compact $d$-dimensional spin Riemannian manifold," with $\mathcal D = i\gamma^\mu\nabla_\mu^{\mathbb S}$ self-adjoint with discrete spectrum, feeding into the Dixmier trace/Connes integration formula.
- why_invalid_or_gap: $\Omega = [0,1]^d$ was fixed globally in Section 2 as the flat cube with boundary and is used unchanged through Sections 2–5. A cube with boundary is not a closed manifold; the Atiyah–Singer Dirac operator on a manifold with boundary is not self-adjoint without imposing boundary conditions (e.g. APS/chiral bag conditions), and the standard Connes trace theorem / Weyl asymptotics used in the proof of Theorem 6.1 are stated for *closed* manifolds. This is never reconciled: either $\Omega$ silently changes meaning (e.g. becomes the flat torus $\mathbb T^d$) or the entire construction needs boundary conditions that are never specified.
- counterexample: NO (this is a scope/domain gap, not a numerical counterexample)
- affects: Theorem 6.1's integration formula, and the cyclic cocycle / winding number construction $\tau_d$ in Section 6.2, both of which inherit the ill-posedness of $\mathcal D$ on $[0,1]^d$.
- minimal_fix: Explicitly redefine $\Omega$ as $\mathbb T^d = (\R/\Z)^d$ (periodic identification of the cube) for Section 6 only, and note this is a different domain convention than Sections 2–5; or specify APS boundary conditions on $[0,1]^d$ and redo the trace-formula computation with the associated boundary correction terms.

**Issue 5**
- status: UNJUSTIFIED
- impact: LOCAL
- category: NORMALIZATION_MISMATCH
- location: Section 2, Theorem 2.1(b) and its proof
- statement: $\mathcal{W}_2(A,B) \le \sqrt{\diam(\Omega)}\,\|\Phi(A)-\Phi(B)\|_{L^1(\Omega)}^{1/2}$.
- why_invalid_or_gap: The proof itself derives $\mathcal{W}_2^2 \le \diam(\Omega)^2 \cdot \frac12\|\Phi(A)-\Phi(B)\|_{L^1}$, i.e. $\mathcal{W}_2 \le \frac{\diam(\Omega)}{\sqrt2}\|\Phi(A)-\Phi(B)\|_{L^1}^{1/2}$ — a coefficient of $\diam(\Omega)$ (dimension: length), not $\sqrt{\diam(\Omega)}$ (dimension: length$^{1/2}$). The stated theorem and its own proof disagree; the error is numerically masked only because $\diam([0,1]^d) = \sqrt d$ is a fixed number the paper treats unit-free.
- counterexample: NO (algebraic inconsistency, not a specific numeric counterexample)
- affects: Any downstream use of the exact constant in Theorem 2.1(b) (none currently, but it is cited as a clean structural fact in the taxonomy table).
- minimal_fix: Correct the theorem statement to $\mathcal{W}_2(A,B) \le \frac{\diam(\Omega)}{\sqrt2}\|\Phi(A)-\Phi(B)\|_{L^1(\Omega)}^{1/2}$, matching the proof.

**Issue 6**
- status: UNDERSTATED
- impact: LOCAL
- category: HIDDEN_ASSUMPTION
- location: Section 2, Theorem 2.1(c) and Theorem 2.2 (Bakry–Émery), proofs
- statement: (c) "$|\dot\mu_A|(t) \le C\|\dot A(t)\|_F$" via "elliptic reconstruction"; (2.2) $\Gamma_2 \ge K\Gamma$ criterion applied on $\Omega=[0,1]^d$.
- why_invalid_or_gap: The constants $C_2,C_3$ in (c) implicitly require $\rho_t = \Phi(A(t))$ bounded away from $0$ (uniform ellipticity) — without this, the weighted $\dot H^{-1}(\rho)$ norm used by Otto calculus is not comparable to the plain $H^{-1}$ norm invoked in the proof, and the constant can blow up as $\rho_t \to 0$ somewhere (which happens whenever $A(t)$ approaches the boundary of $\mathcal S_+^n$, a generic occurrence for gradient flows). Separately, Theorem 2.2's Bochner/$\Gamma_2$-calculus argument on a domain with boundary ($[0,1]^d$) requires either Neumann boundary conditions plus convexity of $\Omega$ (true for the cube, luckily) to avoid a boundary curvature defect term in the integrated Bochner formula — this convexity/Neumann assumption is never stated, only implicitly relied upon.
- counterexample: NO (regularity gap, not a concrete failing instance)
- affects: The precise constants in Theorem 2.1(c); the validity of the LSI/displacement-convexity chain in Theorem 2.2 whenever boundary effects are non-negligible.
- minimal_fix: State explicitly: (i) $\inf_{t,x}\rho_t(x) > 0$ (uniform non-degeneracy) for Theorem 2.1(c); (ii) Neumann boundary conditions for $\Delta_A$ on $\partial\Omega$, justified by convexity of the cube, for Theorem 2.2.

**Issue 7**
- status: UNCLEAR
- impact: LOCAL
- category: SCOPE_OVERCLAIM
- location: Section 2, Theorem 2.2 hypothesis ($\kappa_{\mathrm{BE}}(A) \ge K > 0$)
- statement: Theorem assumes existence of $A \in \mathcal S_+^n$ with smooth positive realization and $\kappa_{\mathrm{BE}}(A) \ge K > 0$.
- why_invalid_or_gap: No example is given, and for the canonical kernel realization $\Phi_{\mathrm{kernel}}(A)(x) = \psi(x)^TA\psi(x)$, $-\log\Phi_{\mathrm{kernel}}(A)$ is generically *not* uniformly convex (quadratic forms have flat/degenerate directions and can approach $0$ near the boundary of the cone, making $-\log$ blow up rather than stay uniformly convex). The theorem may apply to a very restricted or even empty class of realizations as defined in Section 2.1.
- counterexample: NO
- affects: Perceived generality of Theorem 2.2; readers may assume it applies broadly to matrices in $\mathcal S_+^n$ via the canonical kernel realization when it may not apply to any of them.
- minimal_fix: Exhibit at least one explicit family of realizations (e.g. Gaussian-mixture-type $\Phi(A)$) satisfying $\kappa_{\mathrm{BE}} \ge K>0$, or restate the theorem conditionally as "whenever such $A$ exists."

**Issue 8**
- status: UNDERSTATED
- impact: GLOBAL
- category: REGULARITY_GAP
- location: Section 3, Theorem 3.1 (Bottleneck Stability), hypotheses
- statement: Hypotheses are only $L^\infty$-boundedness and Lipschitz dependence $\|\Phi(A)-\Phi(B)\|_\infty \le L_\Phi\|A-B\|_F$.
- why_invalid_or_gap: The persistence diagram $\mathrm{Dgm}_k(\Phi(A))$ and the cited Algebraic Stability Theorem (Chazal et al.) require the filtration to be "tame" (finitely many critical/homological events, essentially Morse-type behavior) for the diagram to be a well-defined finite multiset and for interleaving $\Rightarrow$ bottleneck-bound to apply cleanly. Mere continuity/Lipschitz control of $\Phi(A)$ does not guarantee tameness.
- counterexample: NO
- affects: The literal applicability of Theorem 3.1 to arbitrary continuous functional realizations; also feeds into Theorem 3.2's persistent-entropy computations, which implicitly assume finite diagrams.
- minimal_fix: Add "$\Phi(A)$ is Morse (or has finitely many critical values) on $\Omega$" as an explicit standing hypothesis, or invoke $q$-tameness directly and cite the appropriate generalized stability result.

**Issue 9**
- status: UNDERSTATED
- impact: LOCAL
- category: INTEGRABILITY_GAP
- location: Section 4, Definition (Integrated Willmore Energy), Eq. \eqref{eq:willmore_volume}
- statement: $\mathcal{W}(\Phi(A)) = \int_\Omega |\mathrm{div}(\nabla\Phi/\|\nabla\Phi\|)|^2\|\nabla\Phi\|\,dx$, obtained via coarea formula.
- why_invalid_or_gap: Near non-degenerate critical points of $\Phi(A)$ (where $\nabla\Phi = 0$, unavoidable on a compact domain), $H_t \sim \|\mathrm{Hess}\Phi\| / \|\nabla\Phi\| \sim 1/r$ (with $r$ = distance to the critical point), so the integrand $H_t^2\|\nabla\Phi\| \sim 1/r$. Integrating $1/r$ over a $d$-ball gives $\int_0^\epsilon r^{d-2}\,dr$: finite for $d \ge 2$ but **logarithmically divergent for $d=1$** (the dimensional-collapse edge case explicitly required by this audit). The paper never restricts to $d \ge 2$ or assumes Morse non-degeneracy to control this.
- counterexample: CANDIDATE — any $\Phi(A)$ on $\Omega=[0,1]$ with a non-degenerate interior critical point produces a log-divergent $\mathcal{W}(\Phi(A))$.
- affects: Well-posedness of $\mathcal{W}(\Phi(A))$ as a finite invariant in low dimension; Theorem 4.1 itself is stated only for $d=3$, so it survives, but the *Definition* is presented for general $d$.
- minimal_fix: Restrict the definition to $d \ge 2$, or add a Morse non-degeneracy hypothesis on critical points and note the $d=1$ exceptional/divergent case explicitly.

**Issue 10**
- status: UNDERSTATED
- impact: LOCAL
- category: REGULARITY_GAP
- location: Section 4, Theorem 4.1(a)
- statement: Conformal invariance of $\int_{\Sigma_t}(H^2-K)\,d\mathcal H^2$ under $\psi \in \mathrm{Conf}(\R^3)$.
- why_invalid_or_gap: The classical Willmore/Chen conformal invariance theorem is for *closed* surfaces (or with prescribed boundary behavior). Here $\Sigma_t \cap \Omega$ generically has boundary where the level set meets $\partial\Omega = \partial[0,1]^3$; conformal invariance of the bulk integrand then requires an additional boundary term (geodesic curvature integral along $\partial\Sigma_t \cap \partial\Omega$, per the boundary Gauss–Bonnet/Willmore formula), which is neither stated nor shown to vanish or transform invariantly.
- counterexample: NO
- affects: Precise validity of Theorem 4.1(a) as stated for level sets confined to a bounded box.
- minimal_fix: State the invariance for $\Sigma_t$ closed (i.e. entirely interior to $\Omega$, not meeting $\partial\Omega$), or add the boundary correction term explicitly.

**Issue 11**
- status: UNCLEAR
- impact: COSMETIC
- category: HIDDEN_ASSUMPTION
- location: Throughout (cf. CLAUDE.md protocol item 5: distinguishing flow parameters from other parameters)
- statement: The symbol $t$ is overloaded: a Wasserstein-geodesic/gradient-flow time parameter in Section 2, and a static super-/sub-level-set threshold in Sections 3–4. Similarly $\Omega$ denotes the flat cube $[0,1]^d$ (Sections 2–5) and an abstract closed spin Riemannian manifold (Section 6, cf. Issue 4).
- why_invalid_or_gap: Not mathematically fatal within each section, but violates the project's own stated rigor protocol of keeping flow/threshold parameters and domain conventions unambiguous across a unified treatise.
- counterexample: NO
- affects: Readability; risk of confusion when cross-referencing the master taxonomy table.
- minimal_fix: Use distinct symbols (e.g. $\tau$ for the transport-flow time, $t$ reserved for level thresholds) and explicitly flag the Section 6 domain change (see Issue 4's fix).

**Issue 12**
- status: UNJUSTIFIED
- impact: COSMETIC
- category: UNJUSTIFIED_ASSERTION
- location: Section 5, end of §5.3 (Fractional Besov Exponents)
- statement: "For fractal or self-similar matrices ... $s^*(A) = d - d_{\mathrm{fractal}}$."
- why_invalid_or_gap: Asserted in prose with no proof or citation; plausible by analogy with known Besov-regularity/box-counting-dimension relations but not established here.
- counterexample: NO
- affects: Only the closing remark of §5.3; no theorem depends on it.
- minimal_fix: Either prove it for a specific fractal family (e.g. Sierpiński/Cantor-type step matrices already used elsewhere in the author's corpus) or cite the relevant Besov-dimension theorem and mark this as a conjecture/remark rather than a stated fact.

**Issue 13**
- status: UNCLEAR
- impact: COSMETIC
- category: HIDDEN_ASSUMPTION
- location: Section 3, Definition (Persistent Entropy)
- statement: $p_i \coloneqq \ell_i/L_k(A)$, $E_{\mathrm{pers}}^{(k)}(A) = -\sum p_i\log p_i$.
- why_invalid_or_gap: The convention for $N_k = 0$ (empty diagram, $L_k(A)=0$) is never stated; it is used implicitly in Theorem 3.2's proof ("$E_{\mathrm{pers}}^{(1)}(A) = 0$" for $\mathrm{Dgm}_1(\Phi(A))=\emptyset$), relying on the empty-sum convention without division by zero ever being triggered, but this should be spelled out.
- counterexample: NO
- affects: Cosmetic clarity only.
- minimal_fix: Add "by convention, $E_{\mathrm{pers}}^{(k)}(A) \coloneqq 0$ if $N_k = 0$" to the definition.

---

## 3. Section-by-Section Detailed Review

**Section 2 (Optimal Transport & Bakry–Émery).** Theorem 2.1(a) is standard and fine. (b) has a genuine statement/proof mismatch (Issue 5). (c) and Theorem 2.2 both rest on unstated non-degeneracy/boundary hypotheses (Issue 6) and Theorem 2.2's hypothesis may be vacuous for the paper's own canonical realization (Issue 7). The $\Gamma_2$-calculus citation of Bakry–Émery and von Renesse–Sturm is appropriate in spirit but the transfer to a *bounded domain with boundary* is the load-bearing step left unproven.

**Section 3 (Persistent Homology).** Theorem 3.1's inclusion-chain algebra is correctly verified (I re-derived $X_{t+\epsilon}(f)\subseteq X_t(g)\subseteq X_{t-\epsilon}(f)$ directly from the $L^\infty$ bound and it holds). The gap is the unstated tameness hypothesis (Issue 8). Theorem 3.2's worked counterexample is the single most serious finding in the manuscript (Issue 1): recomputing $B = PAP^T$ explicitly shows the four elevated cells are mutually non-adjacent, so the claimed $H_1$-ring does not exist as constructed — the theorem's conclusion is very likely still true (via $H_0$/component-count separation, which does hold for this example) but the proof as written is invalid.

**Section 4 (Willmore/GMT).** The core differential identities (mean curvature formula, coarea reduction) are correctly derived — I checked the divergence identity for $\mathrm{div}(\nabla\Phi/\|\nabla\Phi\|)$ and it matches the standard formula. Theorem 4.1(a) needs a boundary correction (Issue 10); (b)'s scaling argument is internally inconsistent about what is held fixed, and the stated rate $\Theta(k^2)$ contradicts a literal reading of its own hypotheses (Issue 2, the second strongest finding here). The Willmore energy's well-posedness has an integrability edge case at $d=1$ (Issue 9).

**Section 5 (Microlocal).** Theorem 5.1 is the most solid result in the paper — it is essentially the classical fact that conormal/jump singularities have wavefront set equal to the conormal bundle, correctly argued via the 1D Heaviside Fourier transform $\widehat H(\xi_1) = \frac{1}{i\xi_1}+\pi\delta(\xi_1)$ and tangential rapid decay. No significant issues found beyond the unproven closing remark on fractal Besov exponents (Issue 12).

**Section 6 (NCG & Quantum Information).** Theorem 6.1 correctly restates Connes' trace theorem with the right normalization constants, *but* is built on a domain ($\Omega=[0,1]^d$) that is incompatible with the closed-manifold requirement for the Dirac operator machinery (Issue 4) — this is a global, unaddressed inconsistency inherited by the cyclic-cocycle construction $\tau_d$. Theorem 6.2(a),(c) are correct (PSD sum argument, tensor-density transformation). Theorem 6.2(b) states a well-known-false equivalence at points of rank degeneracy of $\rho(x)$ (Issue 3) — this is a textbook pitfall in quantum estimation theory (QFI/Bures-metric discontinuity) that any referee from the quantum information community would immediately flag.

---

## 4. Strategic Recommendations

- **Target journals:** Given the breadth (six essentially independent transplant results) and the current gap density, this reads more like a *survey/framework* paper than a single tightly-refereed result. *Journal of Geometric Analysis* or *Ann. Henri Poincaré* would tolerate the broad multi-topic structure better than CMP/JMP, which typically expect a single deep, fully rigorous result rather than six loosely-coupled sketches. Adv. Theor. Math. Phys. is a reasonable fit for the NCG/QI sections specifically if split off.
- **Splitting recommendation:** Consider splitting into two or three papers — (i) Optimal transport + persistent homology (Sections 2–3, after fixing Issues 1, 5–8), (ii) GMT + microlocal (Sections 4–5, after fixing Issues 2, 9–10, 12), (iii) NCG + QI (Section 6, after resolving the domain issue (Issue 4) and the QFI degeneracy issue (Issue 3)). Each would then meet the depth bar of a focused paper rather than a survey.
- **arXiv classification:** Cross-list math.DG (primary), math.AT (persistent homology), math-ph/quant-ph (Sections 5–6), matching the subject classes already listed.
- **Positioning vs. Volume I:** The "Beyond the Spectrum" framing (permutation/dimension blindness of classical invariants) is a good hook and is used consistently; keep it, but the introduction's claims of "rigorous existence, stability, and invariance theorems for each construction" should be softened until Issues 1–4 are resolved, since as written not all six families currently have a fully rigorous theorem behind them.
- **Highest-priority fixes before resubmission:** Issue 1 (redo the isospectral counterexample or switch to $H_0$), Issue 2 (fix the amplitude-scaling contradiction), Issue 3 (add full-rank hypothesis to QFI theorem), Issue 4 (resolve $\Omega$'s domain for Section 6). These four are the ones a referee would almost certainly catch and that currently make specific theorem statements false as written.
