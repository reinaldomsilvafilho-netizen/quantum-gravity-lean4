# Beyond the Spectrum III: layer-1 corrections

- **Corrector:** an independent Claude session (Opus). It wrote neither the paper nor `blind_layer1.md`. `LEDGER.md` and the `CLAUDE_*`/`AUDIT_*` files were not used.
- **Date:** 2026-10-06.
- **Backup of the pre-correction `.tex`:** `_arquivo/backup_tex_2026-10-06/Manuscritos_Avulsos/paper_beyond_the_spectrum_3/`, listed in that folder's `MANIFESTO.tsv`.
- **Corrector scripts:** in `scripts/`; each writes an `.out.txt` and exits with its failure count. Both exit 0.
  - `f1_corrector_checks.py`. Every check uses a route different from the referee's n1–n5 and has a negative control.
  - `c2_resolve_new_dois.py`: Crossref/DataCite, with a mutated-DOI control.
- **Referee scripts:** n1–n5 and c1 were re-read, and their outputs agree with the referee's report.
- **One script failure, explained.** On the first run, one check in f1 failed: $E[U^{0.3}]$ by Gauss–Jacobi quadrature. Gauss–Jacobi does not integrate the non-polynomial endpoint singularity $u^{0.3}$ accurately. I replaced that oracle with QUADPACK's algebraic-weight rule, which treats $u^{a-1+s}$ exactly in the weight, and kept the tolerance at $10^{-8}$. The tolerance was not loosened.

Verdict key: **agree** means the referee's finding is confirmed and the text was changed; **disagree** means no edit was made, with the reason given.

| Item | Verdict | Change | Where in v3 | Check |
|---|---|---|---|---|
| Abstract/intro overclaims (A) | agree | Rewritten. The abstract lists only proved or cited results, plus the counterexamples. The Lean sentence was removed and $\mathcal S^n_+$ defined. Section titles no longer advertise removed content. | abstract, §1 | – |
| Lean claim (A) | agree | Every formal-verification claim removed. The declarations block states that the Lean files are a placeholder skeleton. | §1, Declarations | referee inspection of `lean_zenodo/` (not repeated) |
| OBL-001 (B) | agree | Complete first-exit and convexity proof with round balls; Clarke paragraph removed. New remark: not sharp for quadratic $\Phi$. | Thm 2.1, Rem 2.2 | f1 "OBL-001": radial function of $K_t$ for a non-quadratic convex $\Phi$ in $\mathbb R^4$, 3000 rays, lies in $[r_{\min},R_{\max}]$; swapped radii fail |
| OBL-002 (B) | agree | Stated as a cited classical result; added the hypothesis $\Phi\in C^\infty$. | Prop 2.3 | – |
| OBL-003 (M) | agree | The ill-posed theorem is now a remark: what a statement would need, and that it is not proved. Viterbo citation removed. | Rem 2.4 | – (no Floer computation attempted) |
| OBL-004 (B) | agree | "$(a_f)$" replaced by transversality. Proof: finite congruence orbits, Whitney genericity, transitive action. Codimension computed. Gibson et al. 1976 cited. Duplicate tag dropped. | Def 3.1, Prop 3.2 | – |
| OBL-005 (M) | agree | Real-analytic and subanalytic hypotheses added; $\mathcal F_A$ is now any complex that is locally constant on the strata. Proof: isotropy from the conormal inclusion, coisotropy from involutivity. | Lem 3.3 | – |
| OBL-006 (A) | agree | Index formula kept with its hypotheses. The false $\sum m_r\chi(\Sigma_r)$ is replaced by the proved $\sum\chi_c(\Sigma_r)\chi(\text{stalk})$, via the open/closed long exact sequence and rank lower semicontinuity. | Thm 3.4, Rem 3.5 | f1 "OBL-006": $\chi(S^1)=0$ by triangulation; the paper's formula gives 2 (negative control), the $\chi_c$ formula gives 0 |
| OBL-007 Lemma (M) | agree | Claim reduced to existence of a non-negative minimizer and $\lambda>0$, with a complete proof. Simplicity not claimed; Lindqvist 1990 cited for the unweighted case. | Lem 4.2, Rem 4.3 | – |
| OBL-008 (A) | agree | Replaced by $\lim\lambda_p^{1/p}=1/R_\Omega$ for every weight with $0<c_0\le\Phi\le C_0$, with a complete proof (weight comparison, distance-function upper bound, compactness lower bound). Disk, relative perimeter and Kawohl–Fridman ($p\to1$) in a remark. | Thm 4.4, Rem 4.5 | f1 "OBL-008": radial FE minimization (not shooting); $p=2$ matches $j_{0,1}$; $p=4,\dots,32$ decreasing towards 1 and below the cone bound; the weighted value lies in the comparison window; the claimed $h=2$ is excluded |
| OBL-009 (B) | agree | "Inscribed radius" corrected to slimness constant; "stability" dropped; remark that the conformal form is unused. | Thm 4.6, Rem 4.7 | referee n1 (0.881374 vs $\tfrac12\ln3$) |
| OBL-010 (M) | agree | $\Omega=\mathbb R^d$ and units stated. Contraction proved by synchronous coupling; uniqueness among laws with finite second moment. Remark that LSI/Talagrand does not give the contraction. | Prop 5.1, Rem 5.2 | f1 "OBL-010": coupled Euler paths, $\max|X_t-Y_t|/(e^{-\kappa t}|X_0-Y_0|)=0.70\le1$; rate $3\kappa$ violated (284) |
| OBL-011 (B) | agree | Crooks 1999 credited; protocol and initial law stated. | Thm 5.3 | referee n3 (Monte Carlo $2.5013\pm0.0033$ vs 2.5) |
| OBL-012 (A) | agree | Now a remark: slow-driving limit $\mathcal L^2$ (not $\tfrac12\mathcal L^2$), the dimensional argument, the dragged-trap counterexample, and the Aurell et al. statement (checked in arXiv:1012.2037, eq. 23). | Rem 5.4 | f1 "OBL-012": moment ODE by RK4 (not closed form or Monte Carlo); linear and quadratic protocols with $\kappa=1,10$ converge to $\int g\dot\lambda^2$ (1 and 4/3) and $\ge\mathcal W_2^2$; paper's bound at $\kappa=10$ and the $\tfrac12$ factor fail |
| OBL-013 (B) | agree | $\mathcal S^n_+$ defined as PSD; "orthonormal family". | §6, Prop 6.1 | referee n4 |
| OBL-014 (A) | agree | Now a proposition with four proved parts: PSD, trace class, $\mathrm{Tr}=\mathrm{Tr}A$; rank $\le\sum m_k$; normalized $K\ge0$, $>0$ iff rank $\ge2$; regularized version with explicit hypotheses. Counterexamples in a remark. | Prop 6.2, Rem 6.3 | f1 "OBL-014": Schmidt spectrum from the Hermite-coefficient matrix by Gauss–Hermite quadrature (not a grid SVD) has ratio = Mehler $q$ for $\beta=0.6,0.3$; product state has rank 1; random frames with Schmidt ranks (1,1,1) and (2,1,3) give rank 3 and 6 = bound, $\mathrm{Tr}\rho=\mathrm{Tr}A$, normalized energies $\ge0$ |
| OBL-015 (B) | agree | Finite-rank hypothesis added; proof cites DF eqs. (2.12)–(2.14), read in arXiv:1905.00577. | Thm 6.4 | referee n4 (300 random states) |
| OBL-016 (M) | agree | Now a remark: physical proposal $S_R=2E_W$ at leading order, no bulk geometry constructed, units noted. | Rem 6.5 | – |
| T-7a (M) | agree: **removed** | See the decision below. | – | – |
| OBL-017 (M) | agree | "Half-plane" replaced by **entire**; proof by uniform bound, Fubini and Morera. | Prop 7.1 | f1: Gauss–Jacobi quadrature agrees with the $_2F_1$ route at $s=-0.5,-2.5,1.3$ |
| OBL-018 (A) | agree | Now a remark (no poles, $\Phi\equiv c$). New Prop 7.3 computes the vertex-coordinate Mellin transform exactly, with residues and the integer-$b$ cancellation. | Rem 7.2, Prop 7.3 | f1: contour integrals of $\mathcal Z_A$ around the claimed poles are $<10^{-17}$; the negative control $M_j$ has residues matching the formula to $10^{-8}$ ($0.6366,-0.3183,-0.0796$); for $b=2$ the pole at $-a-2$ cancels; closed form = QUADPACK at four values of $s$ |
| OBL-019 (M) | agree: **removed** | A classical result, unrelated to $\mathcal Z_A$. Primary source (Kigami–Lapidus 1993) not accessible to check the attribution. | – | f1: root of $N(r/N)^{d/2}=1$ gives $2\ln3/\ln5$ (arithmetic only) |
| OBL-020 (M) | agree | Compact $\Sigma_t$ and $\Phi\in C^\infty$ assumed. Proof via Federer 4.18 (reach $>0$) and Aamari Thm 3.4, read in arXiv:1705.04565; bottleneck pairs shown to have opposite normals; $d_{\rm sep}>0$ proved; "$d_{\rm sep}=\infty$" removed. Remark: non-compact counterexample, ellipse. | Thm 8.1, Rem 8.2 | f1 "OBL-020": reach by Federer's formula (not brute-force projection). Ellipse: 0.5000, bound 0.5000. Peanut with neck: reach 0.3162, bound 0.2100. Doubled bound fails for both; ellipse $d_{\rm sep}$ finite |
| OBL-021 (B) | agree | Hypotheses stated, $H_j$ unnormalized and defined, medial axis defined; change-of-variables proof (Federer 4.8, Aamari Prop A.1). | Thm 8.3 | referee n5 ($S^3$ exact, ellipse Monte Carlo) |
| Table 1 (B) | agree | Restricted to Vol. III; symmetry column removed; codomains corrected. | Table 1 | – |
| Bibliography (B) | agree | Wrong Vol. II DOI and uncited self-references removed; trilogy record cited. Viterbo and Kigami removed. Crooks, Lindqvist, Gibson et al. and Aamari et al. added and resolved. Key Aurell2012 → Aurell2011. Kawohl–Fridman attribution corrected ($p\to1$; abstract read on the CMUC page). | References | c2 and referee c1 |
| Affiliation, declarations | – | Affiliation replaced. Standard block inserted verbatim, with "volume" and the Lean sentence. No other declaration text existed. | front matter, Declarations | – |

**Disagreements: none.** Each referee finding that I re-checked held up, either by a different numerical route or in the source text.

## T-7a: the three extra §7 paragraphs (local `.tex` only, not on Zenodo)

**Decision: removed.** They were audited to the layer-1 standard.

1. "$H_0^s(\Delta_m,d\mu_\alpha)$" for "wave functions and Dirac–Kähler fields". The index $s$ is not defined (it clashes with the Mellin variable), and Dirac–Kähler fields appear nowhere else.
2. "Barrier potential $B_\alpha$ … self-adjoint Friedrichs operator that annihilates the boundary support". $B_\alpha$ is not defined. A potential is a multiplication operator, not a Friedrichs extension, and "annihilates the boundary support" has no precise meaning.
3. Bi-Laplacian on $H_0^2(\Delta_m)$ with clamped conditions, and "$\alpha_i-3/2\ge-1/2>-1$ guarantees strict integrability". No bi-Laplacian appears in the volume. The inequality silently assumes $\alpha_i\ge1$, which OBL-017 does not assume. The integrability of $\prod u_i^{\alpha_i-1}$ needs only $\alpha_i>0$.

None of this is used by any statement. Keeping it would add undefined objects and a false-generality hypothesis. Nothing in it is both correct and useful enough to repair.

## Literature consulted by the corrector

| Source | What was checked | Access |
|---|---|---|
| Kawohl–Fridman, CMUC 44 (2003) 659–667 | Abstract: $p\to1$, unweighted | CMUC page |
| Juutinen–Lindqvist–Manfredi, ARMA 148 (1999), DOI 10.1007/s002050050157 | Limit $1/R$. Not read directly (paywall); taken from Lindqvist's notes (folk.ntnu.no/lqvist/nonlineigen.pdf, Lemma 11 and (6.5)) and Champion–De Pascale–Jimenez, arXiv:0811.1934 | secondary |
| Lindqvist 1990, Proc. AMS 109 | Uniqueness for bounded domains (via the notes, item III, ref. [33]) | secondary |
| Aurell et al. | eq. (23), $W_{\rm diss}=\langle\lvert\xi_f-\Psi\rvert^2\rangle\,\tau/T$ (mobility $\tau^{-1}$) | arXiv:1012.2037 |
| Dutta–Faulkner | eqs. (2.12)–(2.17) | arXiv:1905.00577 |
| Aamari et al. | Thm 2.2 (= Federer 4.18), Thm 3.4, Prop A.1 | arXiv:1705.04565 |

Not checked against the books: the theorem numbers in Kashiwara–Schapira, Federer 4.8, and Gibson et al. These are cited at chapter level or as in Aamari et al.

## L2 B items (orchestrator, 2026-10-06)
- Introduction: "strictly a scalar field" -> "mostly a scalar field (Vol. I also uses integral operators)".
- Rem 5.4 example: g_fric(s-dot) = a^2 s-dot^2; "for this constant-speed protocol".
- CORRECTIONS: stale layer-2 line replaced by a statement that the re-check was done.
