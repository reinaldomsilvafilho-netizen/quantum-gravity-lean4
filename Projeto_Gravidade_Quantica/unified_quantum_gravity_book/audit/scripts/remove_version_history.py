"""Remove version-history phrasing ("an earlier version ...") from the book text (author's convention:
what changed between versions goes in CHANGELOG.md / Zenodo notes and in audit/chXX_claims.md).
Mathematically informative counterexamples are kept as neutral remarks. Every replacement is asserted.
Usage: python audit/scripts/remove_version_history.py
"""
R = {}

R['chap03_pascal_simplex_continuous_multinomials.tex'] = [
 (r" (An earlier version asserted $\mathcal{J}(x) = 1 - \frac{1}{2x} + \dots$; that is incompatible with both this argument and the numerical values, and it is withdrawn.)",
  r" In particular, an expansion $\mathcal{J}(x) = 1 - \frac{1}{2x} + \dots$ is incompatible with both this argument and the numerical values."),
 (r" An earlier version stated the relation with an error term $\mathcal{O}(m^n/n)$; since $m^n/n \gg (m-1)^n$, that error term would have absorbed the facet term entirely. The statement is withdrawn in favour of this remark.",
  r" An error term $\mathcal{O}(m^n/n)$ would be useless here: since $m^n/n \gg (m-1)^n$, it absorbs the facet term entirely."),
 (r" An earlier version of this chapter asserted the closed form and the semigroup law $\mathcal{D}^\alpha\mathcal{D}^\beta = \mathcal{D}^{\alpha+\beta}$ for the continuous operator; both are withdrawn. They hold for the lattice operator.",
  r" Hence the closed form and the semigroup law $\mathcal{D}^\alpha\mathcal{D}^\beta = \mathcal{D}^{\alpha+\beta}$ hold for the lattice operator but fail for the continuous one."),
 (r" An earlier version of this section asserted that $\sigma \to \frac{1}{2m\alpha}\mathbf{k}^T\mathbf{G}_{m-1}\mathbf{k}$. That derivation imposed an artificial zero-sum constraint $\sum_j k_j = 0$ on the wavevector, which suppresses the contribution of the mean $\mathbb{E}[\mathbf{y}] = \frac{\alpha}{m}\mathbf{1}$. Already for $m = 2$ the correct leading term is $\frac{k^2}{2\alpha^2}\mathbb{E}[y^2] = k^2\,\frac{1+\alpha}{8\alpha}\,(1 + o(1))$ for large $\alpha$, not $\frac{k^2}{2\alpha}$. The claim is withdrawn. What survives is that the long-wavelength metric is $S_m$-invariant; the exact coefficients $a(\alpha), b(\alpha)$ are given by the second moments above.",
  r" The limit is \emph{not} $\frac{1}{2m\alpha}\mathbf{k}^T\mathbf{G}_{m-1}\mathbf{k}$: that form arises only if one imposes a zero-sum constraint $\sum_j k_j = 0$ on the wavevector, which suppresses the contribution of the mean $\mathbb{E}[\mathbf{y}] = \frac{\alpha}{m}\mathbf{1}$. Already for $m = 2$ the leading term is $\frac{k^2}{2\alpha^2}\mathbb{E}[y^2] = k^2\,\frac{1+\alpha}{8\alpha}\,(1 + o(1))$ for large $\alpha$, not $\frac{k^2}{2\alpha}$. The long-wavelength metric is $S_m$-invariant, with exact coefficients $a(\alpha), b(\alpha)$ given by the second moments above."),
 (r" An earlier version stated a Weyl law $N(\lambda) \sim C\lambda^{(m-1)/2}$ as $\lambda \to \infty$; that statement is incompatible with boundedness and is withdrawn.",
  r" In particular there is no Weyl law $N(\lambda) \sim C\lambda^{(m-1)/2}$ as $\lambda \to \infty$."),
 (r" Two corrections relative to earlier versions are essential. First, the continuous kernel does not inherit the multinomial generating function or the semigroup law of the lattice construction. Second, the resulting Laplacian is bounded, so it has no Weyl law at high energies.",
  r" Two structural facts distinguish the continuous theory from the lattice one. First, the continuous kernel does not inherit the multinomial generating function or the semigroup law of the lattice construction. Second, the resulting Laplacian is bounded, so it has no Weyl law at high energies."),
]
R['chap04_simplicial_waves_porous_transport.tex'] = [
 (r"We note two facts, in order to correct earlier statements.", r"Two facts are worth recording."),
 (r" (Earlier versions gave a closed form $\frac{1}{\alpha^2}[1 - R^\alpha\cos(\alpha\Theta)]$ and the limit $\frac{1}{2m\alpha}\mathbf{k}^T\mathbf{A}_{m-1}\mathbf{k}$; both hold for the lattice multinomial, not for this continuous kernel, and are withdrawn; see \cite{silvafilho2026simplex}.)",
  r" (The closed form $\frac{1}{\alpha^2}[1 - R^\alpha\cos(\alpha\Theta)]$ and the limit $\frac{1}{2m\alpha}\mathbf{k}^T\mathbf{A}_{m-1}\mathbf{k}$ belong to the lattice multinomial, not to this continuous kernel; see \cite{silvafilho2026simplex}.)"),
]
R['chap05_interdimensional_transforms_barnes_lie.tex'] = [
 (r"An earlier version asserted \eqref{eq:decay_gamma} with $\gamma = \alpha$, i.e.\ a smoothing gain equal to the fractional order, and deduced an ``isomorphism'' $H^s(\mathbb{R}^m) \to H^s(\mathbb{R}^n)$ at $\alpha = \frac{m-n}{2}$. Neither holds.",
  r"In general $\gamma \neq \alpha$: the smoothing gain is not the fractional order. Nor is there an ``isomorphism'' $H^s(\mathbb{R}^m) \to H^s(\mathbb{R}^n)$ at $\alpha = \frac{m-n}{2}$, since traces are never injective."),
 (r" (Earlier versions had the opposite sign.)", r""),
 (r"\begin{remark}[Ill-posedness; earlier claim withdrawn]", r"\begin{remark}[Ill-posedness]"),
 (r" An earlier version claimed that the kernel ``strictly regularizes'' the inversion and ``heavily suppresses Gibbs ringing''; the effect is the opposite, and the claim is withdrawn.",
  r" The kernel therefore does not regularize the inversion or suppress Gibbs ringing; the effect is the opposite."),
]
R['chap06_sierpinski_fractal_resolvents_spectral_reduction.tex'] = [
 (r"An earlier version stated this as a theorem, with $\alpha_k \to d_H - 1$ and the energy forms" + "\n",
  r"The direct choice, with $\alpha_k \to d_H - 1$ and the energy forms" + "\n"),
 (r"(c) The convergence of the weights to the harmonic factors was assumed rather than derived, and the choice $\alpha_k \to d_H - 1$ was not motivated.",
  r"(c) Nothing forces the weights to converge to the harmonic factors, and the choice $\alpha_k \to d_H - 1$ has no justification."),
 (r" An earlier version presented the agreement of $D_1 = \ln 2 - \frac12$ with the entropy defect $\lim_{x\to\infty}(x^2\ln 2 - \mathcal{E}(x))/x^2 = \ln 2 - \frac12$ as a confirmation. It is not independent evidence: both quantities are fixed by the same value $\int_0^1 H = \frac12$ used to choose $\sigma_0^2$.",
  r" The agreement of $D_1 = \ln 2 - \frac12$ with the entropy defect $\lim_{x\to\infty}(x^2\ln 2 - \mathcal{E}(x))/x^2 = \ln 2 - \frac12$ is not independent evidence: both quantities are fixed by the same value $\int_0^1 H = \frac12$ used to choose $\sigma_0^2$."),
]
R['chap07_minimax_extrinsic_curvature_submanifolds.tex'] = [
 (r"Several earlier statements were false and are withdrawn with counterexamples: a boundary curvature floor, a sagitta bound, the optimality of the cylinder, the helix curvatures of the old table, and an isotropy property of calibrated submanifolds. Regularity invariance,",
  r"We also give counterexamples to several natural-looking statements: a boundary curvature floor, a sagitta bound, the optimality of the cylinder spanning two circles, and an isotropy property of calibrated submanifolds. Regularity invariance,"),
 (r" (An earlier version asserted the opposite.)", r""),
 (r" (An earlier version derived existence and uniqueness from a claimed strict convexity of the area functional, which is false on spaces of submanifolds.)",
  r" (The area functional is not convex on spaces of submanifolds, so convexity arguments do not apply.)"),
 (r" (An earlier version asserted exactness for $n \le 4$, $k \le 2$ and NP-hardness for $n \ge 5$, without proof.)", r""),
 (r" (An earlier version derived $C^{1,1}$ regularity from the obstacle side alone.)", r""),
 (r" An earlier version asserted the conjecture in general ``via the Hopf maximum principle''. No such argument was given.", r""),
 (r"\begin{remark}[Correction]" + "\n" + r"An earlier version asserted $\|\II_{\partial\Omega}|_{TM}\|_{\op} \le \kappa^*$ at every contact point, and that $M^*$ cannot touch any obstacle region where $\|\II_{\partial\Omega}\|_{\op} > \kappa^*$. Both are false for convex obstacles:",
  r"\begin{remark}[Convex obstacles]" + "\n" + r"Neither $\|\II_{\partial\Omega}|_{TM}\|_{\op} \le \kappa^*$ at contact points, nor the impossibility of touching obstacle regions where $\|\II_{\partial\Omega}\|_{\op} > \kappa^*$, holds for convex obstacles:"),
 (r"\begin{remark}[Statements withdrawn from this list]", r"\begin{remark}[Bounds that fail]"),
 (r"\item[(a)] An earlier version claimed a \emph{boundary curvature floor} $\kappa^* \ge \sup_\Sigma \|\II_\Sigma\|_{\op}$. The inequality goes the other way.",
  r"\item[(a)] There is no \emph{boundary curvature floor} $\kappa^* \ge \sup_\Sigma \|\II_\Sigma\|_{\op}$; the inequality goes the other way."),
 (r"\item[(b)] A \emph{sagitta bound} $\kappa^* \ge 8d_{\min}/L^2$ was claimed. The circular arc with chord $L$ and sagitta $d$ has curvature $8d/(L^2 + 4d^2) < 8d/L^2$. For the semicircle ($d = L/2$) the arc has $2/L$, against a claimed bound of $4/L$.",
  r"\item[(b)] The \emph{sagitta bound} $\kappa^* \ge 8d_{\min}/L^2$ fails. The circular arc with chord $L$ and sagitta $d$ has curvature $8d/(L^2 + 4d^2) < 8d/L^2$; for the semicircle ($d = L/2$) this is $2/L$, against $8d/L^2 = 4/L$."),
 (r"This is a tautology. An earlier version further asserted that (i) every local minimizer contains arcs of exactly constant curvature $\kappa^*$ (``Chebyshev equioscillation''); (ii) $\kappa^*_{C^2} > \kappa^*_{C^{1,1}}$ strictly; and (iii) winding loops are strictly suboptimal in the presence of an open half-space, with an ``if and only if'' criterion. Item (i) is Conjecture~\ref{conj:saturated}. Item (ii) fails as a statement about infima whenever",
  r"This is a tautology. Three further statements are natural but unproved: (i) every local minimizer contains arcs of exactly constant curvature $\kappa^*$ (``Chebyshev equioscillation''); (ii) $\kappa^*_{C^2} > \kappa^*_{C^{1,1}}$ strictly; (iii) winding loops are strictly suboptimal in the presence of an open half-space. Item (i) is Conjecture~\ref{conj:saturated}. Item (ii) fails as a statement about infima whenever"),
 (r" Item (iii) was given without proof and is withdrawn.", r" Item (iii) is open."),
 (r" An earlier version cited Langer's theorem for the boundary problem in all dimensions.", r""),
 (r" The earlier ``proof'' did not address these (it invoked inf-sup convolutions and a ``conformal adjustment along normal fibers'' without estimates), so the statement is a conjecture.",
  r" We cannot do this in general, so the statement is a conjecture."),
 (r" An earlier version stated a theorem that minimizers ``fail to be $C^3$'' with a penalty $\ge \kappa^* + \mathcal{O}(\epsilon)$. This is vacuous as stated, and it contradicted the claimed regularity invariance.", r""),
 (r" It is a heuristic and not a theorem (an earlier version stated it as one).", r" It is a heuristic, not a theorem."),
 (r" An earlier version presented $1/R$ as the minimax value.", r" So $1/R$ is only an upper bound."),
 (r"\begin{remark}[Corrections to the earlier table]" + "\n" + r"The earlier table (``universal master classification for $2 \le n \le 12$'') had three problems. First, its multi-helix rows used amplitude $R_0/\sqrt m$ per plane, which gives curvature $1/R_0$ and not the listed $1/(\sqrt m R_0)$ (\texttt{check\_ch07.py}, item 3). Second, it called the product $3$-torus in $\C^3$ ``special Lagrangian''. That torus is Lagrangian but not minimal, and no compact minimal submanifold of $\R^n$ exists. Third, its rows for associative, coassociative, Cayley and ``calibrated $k$-cycles'' in $\R^{10}$--$\R^{12}$ listed curvature values without derivation or definition of $R$. Those rows have been removed.",
  r"\begin{remark}[Two pitfalls]" + "\n" + r"First, the amplitude matters: the curve $\frac{R_0}{\sqrt m}\sum_j e^{i\omega s}\mathbf{e}_j$ has curvature $1/R_0$, not $1/(\sqrt m R_0)$ (\texttt{check\_ch07.py}, item 3). Second, the product $3$-torus in $\C^3$ is Lagrangian but not special Lagrangian: it is not minimal, and no compact minimal submanifold of $\R^n$ exists. We do not list candidates built from calibrated geometries, since we have no curvature values derived for them."),
 (r"\begin{remark}[A withdrawn claim]" + "\n" + r"An earlier version asserted that every calibrated submanifold has ``vectorially isotropic'' second fundamental form with $\|\II\|_{\op} = \|\II\|_F/\sqrt{c}$, $c = n-k$, and minimizes $\|\II\|_{\op}$ in its homology class. This fails already",
  r"\begin{remark}[Calibration does not force isotropy]" + "\n" + r"One might expect calibrated submanifolds to have ``vectorially isotropic'' second fundamental form, $\|\II\|_{\op} = \|\II\|_F/\sqrt{c}$ with $c = n-k$, and to minimize $\|\II\|_{\op}$ in their homology class. This fails already"),
 (r" The explicit constant $(2\pi)^m$ stated in an earlier version was not derived. An earlier ``corner correction'' $\kappa^*_{C^r} = \kappa^*_{C^1} + C(r)\theta^{-(r-1)}$ has been removed: $C^1$ curves carry no curvature, and the cited elliptic corner theory \cite{grisvard1985} does not apply to this problem.",
  r" We do not know the optimal constant $c_m$."),
]
R['chap08_noneuclidean_minimax_relativity_adm.tex'] = [
 (r"An earlier version of this section attributed an extrinsic curvature $K^\theta{}_\theta = 1/r_0$ to the throat. By item (2), the throat has vanishing extrinsic curvature in its static slice, and $1/r_0$ is the square root of its \emph{intrinsic} curvature.",
  r"By item (2), the throat has vanishing extrinsic curvature in its static slice; $1/r_0$ is the square root of its \emph{intrinsic} curvature, not an extrinsic curvature $K^\theta{}_\theta$."),
 (r"Two statements in an earlier version of this section are withdrawn. The first asserted that $\sup|a|$ diverges as the pericenter approaches $3M$; the effective potential is finite there, and no divergence has been established. The second gave the estimate $\kappa^*_{W=\pm1} \approx M/(r_0^2\sqrt{1 - 3M/r_0})$; circular timelike geodesics exist for $r_0 > 3M$ and require no thrust at all, so the orbital portion of a winding manoeuvre can have $a = 0$, and the cost comes entirely from matching the boundary data.",
  r"Two tempting statements are not correct. First, $\sup|a|$ need not diverge as the pericenter approaches $3M$: the effective potential is finite there. Second, an estimate of the form $\kappa^*_{W=\pm1} \approx M/(r_0^2\sqrt{1 - 3M/r_0})$ does not hold: circular timelike geodesics exist for $r_0 > 3M$ and require no thrust at all, so the orbital portion of a winding manoeuvre can have $a = 0$, and the cost comes entirely from matching the boundary data."),
 (r"An earlier version stated this as a theorem. Its proof used the cutoff mollifier $h_\epsilon = \chi h + (1-\chi)(h * \rho_\epsilon)$, where $\chi$ switches on a layer of width $\epsilon^2$. The second derivatives of $h_\epsilon$ then contain $\chi''(h - h*\rho_\epsilon)$ and $2\chi'\,(Dh - D(h*\rho_\epsilon))$, of orders $\epsilon^{-4}\cdot\epsilon^2$ and $\epsilon^{-2}\cdot\epsilon$, which are not bounded, so the curvature estimate does not follow. The proof also relied on the Euclidean statement of Chapter~7, which is now stated there as a conjecture (Regularity Invariance).",
  r"A naive proof with the cutoff mollifier $h_\epsilon = \chi h + (1-\chi)(h * \rho_\epsilon)$, where $\chi$ switches on a layer of width $\epsilon^2$, fails: the second derivatives of $h_\epsilon$ contain $\chi''(h - h*\rho_\epsilon)$ and $2\chi'\,(Dh - D(h*\rho_\epsilon))$, of orders $\epsilon^{-4}\cdot\epsilon^2$ and $\epsilon^{-2}\cdot\epsilon$, which are not bounded. The Euclidean case is itself a conjecture (Regularity Invariance, Chapter~7)."),
]
R['chap09_global_homotopy_covering_spaces_jordan_loops.tex'] = [
 (r" An earlier version made several claims that we now withdraw: a finite winding cutoff without a length bound, conjugation invariance under mapping classes, a free fundamental group for obstacle complements in all dimensions, and a $50.6\%$ curvature gap in a benchmark channel. In that channel both homotopy classes have the same optimal curvature $1/H$.",
  r" We also show that the length bound cannot be dropped, that mapping classes do not act on holonomy by conjugation, and that in a benchmark channel with a central obstacle both homotopy classes have the same optimal curvature $1/H$."),
 (r"An earlier version claimed that in any dimension $n$ the free space retracts, by stratified Morse theory \cite{goresky1988}, onto a $1$-dimensional complex with free fundamental group. This is false.",
  r"In dimension $n \ge 3$ the free space does not in general retract onto a $1$-dimensional complex with free fundamental group, stratified Morse theory \cite{goresky1988} notwithstanding."),
 (r" An earlier version claimed $\operatorname{Hol}(M\cdot\gamma, A) = g_M \operatorname{Hol}(\gamma, A) g_M^{-1}$ for every mapping class $M$. This is false.",
  r" Hence $\operatorname{Hol}(M\cdot\gamma, A) = g_M \operatorname{Hol}(\gamma, A) g_M^{-1}$ does not hold for every mapping class $M$."),
 (r" This is a numerical convenience. (An earlier version stated it as a theorem.)", r" This is a numerical convenience."),
 (r"The earlier proof of this statement assumed a constant radius of curvature. The bound is sharp for the circle.", r"The bound is sharp for the circle."),
 (r"\begin{remark}[What was wrong before]", r"\begin{remark}[Why the length bound is needed]"),
 (r"\item[(a)] The earlier ``finite winding cutoff'' restricted the competitors to the length range $L \le \min(L_{\mathrm{base}}, \pi D_\Omega)$, on the grounds that longer paths are ``dominated''. That is unjustified, since using extra length is exactly how loops can lower curvature. Without a length bound",
  r"\item[(a)] One cannot restrict competitors to lengths $L \le \min(L_{\mathrm{base}}, \pi D_\Omega)$ on the grounds that longer paths are ``dominated'': using extra length is exactly how loops can lower curvature. Without a length bound"),
 (r"\item[(c)] The inequality $\int|\kappa| \ge \int|\theta_i'| - \pi$, used earlier, was not proved. We do not use it.",
  r"\item[(c)] We do not know whether $\int|\kappa| \ge \int|\theta_i'| - \pi$ holds in general, and we do not use it."),
 (r"An earlier version stated this as a theorem, with ``global certitude''. Its proof had four gaps." + "\n" + r"\begin{itemize}" + "\n" + r"    \item The topological part relied on the flawed finite cutoff discussed in Remark~\ref{rem:old_cutoff}." + "\n" + r"    \item The recovery sequence used density of splines in the \emph{norm} of $W^{2,\infty}$, which fails.",
  r"A proof has to overcome four difficulties." + "\n" + r"\begin{itemize}" + "\n" + r"    \item The topological reduction needs the length bound (Remark~\ref{rem:old_cutoff}), which must be built into the discrete functionals." + "\n" + r"    \item The recovery sequence cannot use density of splines in the \emph{norm} of $W^{2,\infty}$, which fails."),
 (r"    \item The barrier used only disks of radius $R_j$, inconsistent with the $C^{1,1}$ obstacles in the hypothesis.",
  r"    \item The penalty must control $\dist(\gamma, \mathcal{F})$ for general $C^{1,1}$ obstacles, not only for disks."),
 (r"    \item Equi-coercivity was not addressed.", r"    \item Equi-coercivity must be established."),
 (r" An earlier version stated a ``convexification theorem'' asserting unconditional approximation of the global minimizer. This is withdrawn.", r""),
 (r"\begin{remark}[Withdrawn benchmark claims]" + "\n" + r"An earlier version assigned the value $1/0.80 = 1.25$ to the embedded class, using an ``effective corridor clearance'' of $0.80$ that was not derived from the geometry. It assigned $1/H \approx 0.617$ to an ``immersed teardrop'' around the obstacle and reported a $50.6\%$ reduction as evidence for a strict embedded/immersed gap. The class around the obstacle is not immersed (its optimal path is embedded), and both classes have optimal value $1/H$.",
  r"\begin{remark}[No gap in this geometry]" + "\n" + r"The class around the obstacle does not need self-intersections: its optimal path is embedded, and both classes have optimal value $1/H$."),
]
R['chap10_information_geometry_minimax_deep_learning.tex'] = [
 (r"As a consequence, an earlier version's ``Hessian trace'' and ``PAC-Bayes'' bounds in terms of $\kappa^*_{\mathrm{info}}$ are false. In Gaussian linear regression with random labels, $\kappa^*_{\mathrm{info}} = 0$, the loss Hessian has positive trace, and the generalization gap is $0.71$, against a claimed bound of $0.19$",
  r"As a consequence, ``Hessian trace'' and ``PAC-Bayes'' bounds in terms of $\kappa^*_{\mathrm{info}}$ cannot hold. In Gaussian linear regression with random labels, $\kappa^*_{\mathrm{info}} = 0$, the loss Hessian has positive trace, and the generalization gap is $0.71$, against $0.19$ for such a bound"),
 (r"This is far below $\mathcal{O}(D^3)$ but not linear in $D$, as an earlier version stated.", r"This is far below $\mathcal{O}(D^3)$, though not linear in $D$."),
 (r"\begin{remark}[What was claimed]" + "\n" + r"An earlier version stated a theorem (``Wasserstein dynamics and sharpness-aware minimization'') with three items: an exploration--exploitation trade-off, the Hessian trace bound, and the PAC-Bayes bound above, all without proof. Proposition~\ref{prop:counterexample} refutes the last two. The first is a qualitative remark. The observation",
  r"\begin{remark}[Paths versus endpoints]" + "\n" + r"The observation"),
 (r"An earlier version stated this as a theorem with the bounds $T \ge \mathcal{O}(2^L)$ for unconstrained descent and $T \le \mathcal{O}(L^2/\kappa^{*2}_{\mathrm{info}})$ for the constrained one. No proof was given, and the second bound is meaningless when $\kappa^*_{\mathrm{info}} = 0$, which is common by Proposition~\ref{prop:degenerate}. It also invoked L\'evy's concentration lemma, which concerns Lipschitz functions of a uniformly random point on a high-dimensional sphere, without specifying the function or the distribution to which it applies. The abstract of that version also mentioned ``winding trajectories around Fisher singularities'' giving polynomial sample complexity. That claim did not appear in the body and is withdrawn.",
  r"A quantitative version cannot be phrased through $\kappa^*_{\mathrm{info}}$: a bound such as $T \le \mathcal{O}(L^2/\kappa^{*2}_{\mathrm{info}})$ is meaningless when $\kappa^*_{\mathrm{info}} = 0$, which is common by Proposition~\ref{prop:degenerate}. L\'evy's concentration lemma, which concerns Lipschitz functions of a uniformly random point on a high-dimensional sphere, is relevant only once the function and the distribution to which it applies are specified."),
]
R['chap11_emergent_spacetime_tensor_networks_holonomies.tex'] = [
 (r" We also correct several errors of an earlier version: a factor $2$ in the quantum Fisher metric, the sign of the graphon Ricci flow, a Kac--Rice formula that fails for $k = 2$, and the claim that relative-entropy positivity yields the nonlinear Einstein equations.",
  r" We also point out that relative-entropy positivity yields inequalities, not the nonlinear Einstein equations."),
 (r"The earlier version wrote $\frac12\Tr(\mathcal{L}_i\partial_j\rho) = \frac12\Tr(\rho\{\mathcal{L}_i,\mathcal{L}_j\})$. These two expressions differ by a factor $2$ (\texttt{audit/scripts/check\_ch11.py}, item 1).",
  r"Note that $\frac12\Tr(\mathcal{L}_i\partial_j\rho)$ is half of $g^{\mathrm{SLD}}_{ij}$ (\texttt{audit/scripts/check\_ch11.py}, item 1)."),
 (r" An earlier version asserted that the two coincide for ``reduced states of free-field vacuum perturbations on the Rindler wedge''. There is no such general commutation, and that assertion has been removed.",
  r" In particular, they do not coincide for general perturbations of Rindler-wedge vacuum states, which do not commute with the state."),
 (r" An earlier version stated that the nonlinear completion ``follows from the positivity of the second-order modular relative entropy''. That is incorrect, and the all-orders statement is open.",
  r" The all-orders statement is open."),
 (r" An earlier version stated \eqref{eq:ads_metric_cmera} as a theorem, obtained by pulling back the Fubini--Study metric to the coordinates $(x, u)$. That construction fails as stated: for a translation-invariant state,",
  r" Pulling back the Fubini--Study metric of $|\Psi(u)\rangle$ to the coordinates $(x, u)$ does not work: for a translation-invariant state,"),
 (r" The ``matching $c_2 = c_1$'' was also imposed rather than derived.", r" The equality $c_2 = c_1$ is part of the conjecture."),
 (r" The earlier ``proof'' of the equality used only the Schmidt decomposition, which gives the inequality of Proposition~\ref{prop:mincut}.",
  r" The Schmidt decomposition alone gives only the inequality of Proposition~\ref{prop:mincut}."),
 (r" (The earlier version attributed the spectrum to ``Casimir invariants of the tensor nodes'' and had an extra factor $G_N$ in $\widehat E$.)",
  r" The spectrum comes from the edges, not from the Casimirs of the nodes."),
 (r" (An earlier version of this chapter had the opposite sign, as did Chapter~12 before its correction.)", r""),
 (r"\begin{remark}[Why this is not a theorem]" + "\n" + r"An earlier version stated this as a theorem, and three obstacles stand in the way.",
  r"\begin{remark}[Why this is not a theorem]" + "\n" + r"Three obstacles stand in the way."),
 (r"The earlier version gave $\mathbb{E}[\mathcal{N}_{\mathrm{crit}}] = 2((k-1)/\pi)^{N/2}\sqrt{k-1}\,e^{N\theta(k)}$ with $\theta(k) = \frac12\log(k-1) - \frac{k-2}{2(k-1)}$. For $k = 2$ this gives $2\pi^{-N/2} \to 0$, while the exact count is $2N$ (\texttt{check\_ch11.py}, item 3). Its exponential rate $\log(k-1) - \frac12\log\pi - \frac{k-2}{2(k-1)}$ also disagrees with $\frac12\log(k-1)$. The identification",
  r"The identification"),
 (r"\begin{remark}[Corrections and the horizon reading]", r"\begin{remark}[The horizon reading]"),
]
R['chap12_grand_unification_quantum_gravity_treatise.tex'] = [
 (r" (An earlier version of this chapter used the opposite sign, which is inconsistent with Chapter~2 and would make negatively curved bottlenecks grow.)",
  r" With the opposite sign, negatively curved bottlenecks would grow."),
 (r"An earlier version of this section contained a closed formula expressing the Jarlskog invariant $J_{\mathrm{CP}}$ through quark masses and $v$. That formula was dimensionally inconsistent (it carries dimension $\mathrm{GeV}^{-3}$) and has been withdrawn. We do not currently have",
  r"We do not currently have"),
 (r" (An earlier version of this section asserted a shrinking self-similar solution $R(t) = R_0 e^{-t/L}$ with non-zero entropy production. That is incorrect, because the hemispheres have $\mathbf{H} = 0$.)",
  r" In particular there is no shrinking self-similar solution $R(t) = R_0 e^{-t/L}$ through hemispheres."),
 (r"An earlier version of this chapter proposed atom-interferometric tests of a ``Jordan-loop protection'' effect. Since the restriction",
  r"Atom interferometry does not test a ``Jordan-loop protection'' effect. The restriction"),
 (r", not a consequence of causality, and since $\ell_P/\lambda_{\mathrm{dB}} \lesssim 4 \times 10^{-26}$ for strontium interferometers, we do not propose such a test.",
  r", not a consequence of causality, and $\ell_P/\lambda_{\mathrm{dB}} \lesssim 4 \times 10^{-26}$ for strontium interferometers."),
]
R['chap13_experimental_observational_signatures_quantum_gravity.tex'] = [
 (r"\emph{Atom interferometry.}---An earlier version of this letter proposed that long-baseline atom interferometers (MAGIS-100 \cite{abe2021matter}, AION \cite{badurina2020aion}) could test a ``Jordan-loop protection'' of loop-quantum-gravity holonomies. That proposal rested on reading the restriction to non-self-intersecting loops as a consequence of chronology protection.",
  r"\emph{Atom interferometry.}---Long-baseline atom interferometers (MAGIS-100 \cite{abe2021matter}, AION \cite{badurina2020aion}) do not test a ``Jordan-loop protection'' of loop-quantum-gravity holonomies. Such a test would require the restriction to non-self-intersecting loops to follow from chronology protection."),
 (r" We therefore withdraw the proposal.", r""),
]
R['master_book_unified_quantum_gravity.tex'] = [
 (r" Their current status is stated here explicitly, because an earlier version of this preface overstated it.", r" Their status is stated here explicitly."),
]
R['DICTIONARY_TERMS_AND_SYMBOLS.tex'] = [
 (r"\textbf{Withdrawn:} the closed form $(\frac1m\sum e^{-ik_j})^\alpha$, the semigroup law, the coefficient $\frac{1}{2m\alpha}\mathbf{G}_{m-1}$, and a Weyl law at $\lambda \to \infty$. These hold only for the lattice (Gr\"unwald--Letnikov) construction or are incompatible with boundedness.",
  r"\textbf{Lattice only:} the closed form $(\frac1m\sum e^{-ik_j})^\alpha$ and the semigroup law hold for the lattice (Gr\"unwald--Letnikov) construction, not the continuous kernel; the operator is bounded, so there is no Weyl law at $\lambda \to \infty$."),
 (r"\textbf{Withdrawn:} a gain $\gamma = \alpha$ and an ``isomorphism'' at $\alpha^* = \frac{m-n}{2}$; traces are never injective.",
  r"\textbf{Note:} in general $\gamma \ne \alpha$, and traces are never injective."),
]

if __name__ == '__main__':
    import os
    os.chdir(os.path.join(os.path.dirname(__file__), '..', '..'))
    for f, reps in R.items():
        s = open(f, encoding='utf-8').read()
        for a, b in reps:
            n = s.count(a)
            if n != 1:
                if s.count(b) >= 1 and b:
                    continue  # already applied
                raise SystemExit(f'{f}: {n} matches for: {a[:90]}')
            s = s.replace(a, b)
        open(f, 'w', encoding='utf-8', newline='').write(s)
        print('ok', f, len(reps))
