# Beyond the Spectrum III: layer-2 re-check

- **Checker:** independent Claude session (Opus), 2026-10-06. I wrote none of the volume, `blind_layer1.md`, `fixes_layer1.md` or the notes.
- **Protocol:** `unified_quantum_gravity_book/audit/verify/PROTOCOL.md`, Camada 2, and the `prova-rigorosa` skill.
- **Inputs:**
  - `blind_layer1.md` and `fixes_layer1.md`;
  - the current `.tex` and PDF;
  - the pre-fix backup in `_arquivo/backup_tex_2026-10-06/…` (diffed section by section);
  - `CORRECTIONS_2026-10-06.md` and `ZENODO_DESCRIPTION_VOL3.md`;
  - `_staging/DECLARACOES_PADRAO_ARTIGOS.tex`.
- **Evidence scripts:** I re-ran the corrector's `f1_corrector_checks.py`. It exits 0, and its output is byte-identical to the shipped `.out.txt`.
- **New scripts** (`scripts/L2_*.py`, each with an `.out.txt`; all exit 0, fixed seeds). Every check uses a route different from both the referee's (n1–n5) and the corrector's (f1), plus a negative control:

| Script | Checks | Result |
|---|---|---|
| `L2_obl008_inradius.py` | Thm 4.4 | 0 failures |
| `L2_obl006_euler.py` | Thm 3.4, Rem 3.5 | 0 failures |
| `L2_obl014_partial_trace.py` | Prop 6.2, Rem 6.3 | 0 failures |
| `L2_mellin.py` | Props 7.1 and 7.3, Rem 7.2 | 0 failures |
| `L2_thermo_reach.py` | Rem 5.4, Thm 8.1 | 0 failures |
| `L2_text_refs.py` | DOIs, declarations, affiliation, house style, notes | 1 failure: the notes, see item 33 |
| `L2_build.py` | build gate | 0 failures |

- **Two first-run failures, both in my own oracles and both disclosed in the scripts:**
  1. In `L2_obl008`, my closed form for the 1D $p$-eigenvalue carried a spurious $(p-1)^{1/p}$. The FE code, which converges at order 2, exposed it. The wrong form is now the negative control.
  2. In `L2_mellin`, the subtracted-integral continuation lost precision by cancellation near $u=0$. I replaced the oracle with a termwise series tail on $[0,1/2]$.
- **One control replaced:** in `L2_thermo_reach`, the "2 × bound" control did not discriminate on Cassini ovals. I replaced it with the mutation "reach ≥ $d_{\rm sep}/2$".
- **No tolerance was loosened.**
- **Processes:** no background jobs; `processos_orfaos.py` finds 0 suspects.

## Verdicts

### Priority items (new proofs)

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | **OBL-008, Thm 4.4:** $\lim\lambda_p(A)^{1/p}=1/R_\Omega$ for every weight with $0<c_0\le\Phi\le C_0$ | **CONFIRMA** | **Line by line:** see "OBL-008: notes on the re-derivation" below.<br>**Numerics:**<br>• 1D FE matches the Ōtani closed form at order 2 (p = 2, 4, 8).<br>• For two weighted 1D cases ($C_0/c_0=1.8$ and $e^{1.2}$, p = 2…64), every value lies in the comparison window, and the distance to $1/R=2$ decreases monotonically (2.137 at p = 64; N-stable to $10^{-5}$).<br>• For the unit square, rigorous two-sided bounds with no FE: slice Poincaré from below, $\delta$ test function from above. At p = 4096 they enclose $\lambda_p^{1/p}\in[2.0041,2.0079]$ unweighted, and $[2.0034,2.0086]$ with weight ratio 4.<br>• Excluded: the Cheeger value $2+\sqrt\pi$, $1/(2R)$ and $2/R$. |
| 2 | **OBL-006, Thm 3.4:** $\chi=\sum\chi_c(\Sigma_r)\chi(\text{stalk})$, plus the $S^1$ counterexample (Rem 3.5) | **CONFIRMA** | **Proof:** open/closed additivity of $\chi_c$. The ordering by increasing rank is right, because $\{\operatorname{rank}\le k\}$ is closed. $\chi_c(S;\mathcal L)=\chi_c(S)\operatorname{rank}\mathcal L$ by triangulation, and $\chi=\chi_c$ on compact $\Omega$.<br>**Counterexample:** $\chi_c$(two arcs) $=-2$ and $\chi_c$(two points) $=2$, giving 0, while the v2 formula gives 2.<br>**Numerics:** cohomology computed as ranks of simplicial coboundaries ($H^*(X)$, $H^*(X,Z)$, $H^*(Z)$), against $\chi_c$ by open-cell counting. Four sheaves ($k_X$, $j_!k_U$, $i_*k_Z$, $k_X\oplus i_*k_Z[-1]$) on three spaces: $S^1$ with $\cos$; $S^1$ with $\operatorname{diag}(\cos,\cos+\frac12)$, $n=2$; and $S^2$. All 12 agree. The v2 formula fails on both $S^1$ cases (2 vs 0, 4 vs 0); on $S^2$ it agrees by coincidence. |
| 3 | **OBL-014, Prop 6.2 (1)–(4) and Rem 6.3:** rank ≤ $\sum m_k$; normalized $K\ge0$, $>0$ iff rank ≥ 2; Mehler; $-\log5$ | **CONFIRMA** | **(1)** $\rho=\sum\lambda_j\Phi_j\Phi_j^*$ with $\operatorname{Tr}\Phi_j\Phi_j^*=\lVert\phi_j\rVert^2$.<br>**(2)** The range of each $\Phi_j$ lies in $\operatorname{span}\{a_{kl}\}$.<br>**(3)** With $\sum p_k=1$ and at least two positive eigenvalues, every $p_k<1$.<br>**(4)** $c=\int k_2(z,z)>0$, since $\lvert k_2(x,y)\rvert^2\le k_2(x,x)k_2(y,y)$; then $\rho^\epsilon\ge\epsilon cT_{k_1}$, which is injective.<br>**Mehler:** $q=t^2$ with $2t/(1+t^2)=\beta$, so $q=1/9$ at $\beta=0.6$. New route: Rényi moments $\operatorname{Tr}\rho^k$, $k=2…6$, as $2k$-dimensional Gaussian determinants, equal the geometric law to $10^{-12}$ for $\beta=0.6,0.3,-0.45$. The mutation $q\to\sqrt q$ fails. Nyström on 80/160/320 Gauss–Legendre nodes: first 8 eigenvalues $>0$, all ratios $=1/9$.<br>**Finite-dimensional frames (300 trials):**<br>• 0 violations of rank ≤ $\sum m_k$;<br>• the bound is attained 86 times;<br>• "rank ≤ n" (v2) fails 262 times;<br>• $\operatorname{Tr}\rho=\operatorname{Tr}A$;<br>• $E_k\ge0$, and $E_k>0$ iff rank ≥ 2;<br>• $A=(5)$ gives $-\log5<0$. |
| 4 | **Prop 7.3:** exact poles and residues of $M_j$, the integer-$b$ case, and $\mathcal Z_A$ entire (Prop 7.1, Rem 7.2) | **CONFIRMA** | **Re-derivation:** $u_j\sim\mathrm{Beta}(\alpha_j,b_j)$; the residue is $(-1)^k/k!\cdot\Gamma(\alpha_0)/(\Gamma(\alpha_j)\Gamma(b_j-k))$; it is non-zero iff $b_j-k\notin-\mathbb N_0$. For integer $b$, $\Gamma(z)/\Gamma(z+b)=\prod_{i<b}(z+i)^{-1}$.<br>**Numerics:**<br>• A 2D QUADPACK integral over $\Delta_3$ equals the formula at $s=1.7,0.5,-0.4,-0.65$.<br>• The continuation by series tail plus subtracted integral equals the Γ-formula at $s=-2.2+0.3i$ and $-3.9-0.7i$.<br>• Residues for $k=0…4$ agree by three routes: Taylor coefficients $c_k/B$, a contour integral, and the formula.<br>• For $b=2$: residues 1.19 and −1.19 at $k=0,1$, and $<2\cdot10^{-16}$ for $k\ge2$.<br>• Mutations $(-1)^{k+1}$ and $\Gamma(b+k)$ fail.<br>• **$\mathcal Z_A$:** $\Phi=1+u_1+\frac12\sin3u_2$; the contour integrals around all 12 v2 "poles" are $\le1.0\cdot10^{-17}$; the same routine on $M_1$ gives 1.8167; and $\lvert\mathcal Z(s)\rvert\le\max(c_1^s,c_2^s)$. Morera proof re-read: correct. |

### Other items

| # | Item | Verdict | Evidence / note |
|---|---|---|---|
| 5 | Title and abstract | **CONFIRMA** | Every sentence matches a proved or cited body statement. The three counterexamples are Rem 3.5, Rem 5.4 and Rem 6.3, and $S_R=2E_W$ is called a proposal. Note: the abstract says "weight bounded above and below", while Thm 4.4 assumes $C^1$; the proof uses only the bounds, so this is harmless. |
| 6 | Introduction | **PROBLEMA (B)** | It says that in Vols. I–II "the realization $\Phi(A)$ was strictly a scalar field … or a Radon probability measure". Vol. I has operator-valued realizations (Family IV, integral operators $T_A$ with kernel $W_A$; its abstract says "operator-valued realization families"). Suggested fix: "mostly scalar fields or measures". The Vol. II topics listed (OT, Bakry–Émery, persistence, Willmore, Dixmier) match Vol. II's current sections. |
| 7 | Lean / formal-verification claim | **CONFIRMA** | No such claim remains in the body. The Declarations carry the standard placeholder sentence. |
| 8 | OBL-001 and Rem 2.2 | **CONFIRMA** | The first-exit argument and the outer ball are correct, and $\pi r_{\min}^2=2\pi(t-m)/\lambda_{\max}$. Remark: $c_1^{EH}=2\pi t/\nu_{\max}$, with symplectic eigenvalues in $[\lambda_{\min},\lambda_{\max}]$. |
| 9 | OBL-002 | **CONFIRMA** | Cited classical result, with hypotheses. |
| 10 | OBL-003 (now a remark) | **CONFIRMA** | Honest. No over-correction, since no proof exists. |
| 11 | OBL-004 | **CONFIRMA** | Dimension $r(2n-r+1)/2$ and codimension $\binom{n-r+1}2$ re-derived. The orbit-invariance argument for Whitney (B) is correct. Gibson et al. are cited without a chapter number (B, already noted in CORRECTIONS). |
| 12 | OBL-005 | **CONFIRMA** | Isotropy from the conormal inclusion, coisotropy from involutivity. Note: KS 8.4.1 is stated for μ-stratifications; for Whitney (B) stratifications the inclusion is standard. Chapter-level citation is acceptable. |
| 13 | OBL-007 Lemma and Rem 4.3 | **CONFIRMA** | Complete proof (comparison, Poincaré, Rellich, weak lsc, $\lvert u\rvert$). Dropping simplicity is not an over-correction: the old argument was invalid. The weighted Lindqvist/Picone argument could restore it in a later version (optional). |
| 14 | OBL-009 and remark | **CONFIRMA** | $\ln(1+\sqrt2)$ is the slimness constant of the ideal triangle, distinct from $\frac12\ln3$. |
| 15 | OBL-010 and Rem 5.2 | **CONFIRMA** | Synchronous coupling, uniqueness, and $CD(\kappa,\infty)$ all correct. Units stated. |
| 16 | OBL-011 | **CONFIRMA** | Signs right; Crooks credited. |
| 17 | OBL-012, Rem 5.4 | **PROBLEMA (B)** | **Numbers correct:**<br>• new solve_ivp moment route = closed form to $10^{-8}$;<br>• $g_{\rm fric}=a^2$ for $\kappa=1,10$;<br>• $\tau\Sigma\to a^2$;<br>• the $\frac\kappa4\mathcal W_2^2$ and $\frac12\mathcal L^2$ mutations fail;<br>• the Aurell jump protocol reaches $\mu_B$ with $\tau W_{\rm diss}=\mathcal W_2^2$ exactly at finite $\tau$, while the dragged trap at finite $\tau$ has $\tau\Sigma<a^2$ but does not reach $\mu_B$, which is consistent with the text;<br>• dimensions consistent.<br>**Wording:** "Thus the slow-driving limit equals $\mathcal L^2$" holds only for constant-speed paths. It should read "is at least $\mathcal L^2$, with equality for constant-speed paths (not $\frac12\mathcal L^2$)". "$g_{\rm fric}=1$ per unit $(\dot sa)^2$" is awkward; suggested: "$g_{\rm fric}(\dot s)=a^2\dot s^2$". |
| 18 | OBL-013 | **CONFIRMA** | – |
| 19 | OBL-015 | **CONFIRMA** | $S_R=S(11^*)=I(11^*:2)\ge I(1:2)$. The finite-rank hypothesis makes it rigorous. |
| 20 | OBL-016, now a remark | **CONFIRMA** | Labelled a physical proposal. $\mathrm{Area}/G_N$ is dimensionless for $\hbar=c=1$. |
| 21 | T-7a: removal of the three §7 paragraphs | **CONFIRMA** | Diff against the backup: the paragraphs defined nothing ($s$, $B_\alpha$, Dirac–Kähler fields), "$\alpha_i-3/2\ge-1/2$" assumed $\alpha_i\ge1$, and nothing used them. They were not on Zenodo. Removal is justified. |
| 22 | OBL-018 → Rem 7.2; OBL-019 removed | **CONFIRMA** | OBL-019 was classical and unrelated to $\mathcal Z_A$. Removing it loses no proved content. |
| 23 | OBL-020 and Rem 8.2 | **CONFIRMA** | **Proof:** in the bottleneck case $z_0$ has two nearest points, so $d(z_0,\Sigma)=\tau$ and the open ball misses $\Sigma$; the sign argument gives $\nu(q_1)=-\nu(q_2)$. $d_{\rm sep}>0$ by uniform continuity.<br>**Ellipse:** $\epsilon_0=1$, $M=2$, $d_{\rm sep}=2$, reach $1/2$.<br>**New Cassini ovals** ($c=1.05,1.2,1.6$): Federer-formula reach is 0.3202, 0.6539 and 1.0593, all $\ge$ the bound and stable under refinement. At $c=1.05$ the reach equals $d_{\rm sep}/2$ (neck). |
| 24 | OBL-021 | **CONFIRMA** | The change of variables and the even-power expansion are correct. |
| 25 | Table 1 | **CONFIRMA** | – |
| 26 | Bibliography and DOIs | **CONFIRMA** | 18/18 DOIs resolve (Crossref/DataCite), with matching title, year and first author; the mutated-DOI control fails.<br>Kawohl–Fridman has no DOI. The EuDML link returns 403 to scripts. DML-CZ handle 10338.dmlcz/119420 confirms the title, pp. 659–667, and $p\to1$ in the abstract.<br>Minor (B): the standard sentence "Every reference was resolved through Crossref, DataCite or arXiv" does not literally cover this EuDML item. |
| 27 | Declarations | **CONFIRMA** | Identical to the standard block, volume variant, with the Lean sentence (whitespace-normalized). A one-word mutation fails. |
| 28 | Affiliation | **CONFIRMA** | "Master's student, Postgraduate Program in Statistics and Agricultural Experimentation (PPGEE/DES) … UFLA". |
| 29 | House style | **CONFIRMA** | The body contains none of: earlier version, withdrawn, corrected, audit/, machine-checked, formally verified, Lean, GitHub, pending, v2, rigorously. "earlier versions" appears only in the standard block. |
| 30 | Physical statements: dimensions | **CONFIRMA** | $k_BT=D=1$; $\tau\Sigma$, $\mathcal L^2$, $\mathcal W_2^2$ ~ time; $\kappa$ ~ 1/time; $\mathrm{Area}/G_N$ dimensionless. The volume contains no physical numbers, so no CODATA estimate applies. |
| 31 | Build (`L2_build_final/`, pdflatex ×3) | **CONFIRMA** | Exit codes 0/0/0. 0 errors, 0 LaTeX/Package/Class warnings, 0 overfull, 0 underfull, 0 undefined. 13 pages. One pre-existing pdfTeX notice, "font expansion: font should be expanded before its first use" (microtype), which the gate accepts. |
| 32 | Shipped PDF = current `.tex` | **CONFIRMA** | pdftotext of the shipped PDF is identical to the fresh build. |
| 33 | `CORRECTIONS_2026-10-06.md` | **PROBLEMA (B)** | Items 1–26 are accurate against the diff and the body. But "What still needs work" still lists "**Layer 2.** A targeted re-check …". After this report that is stale and reads as pending. It should be replaced by a line saying the layer-2 re-check was done on 2026-10-06. Cosmetic: item 26 says "`\date{}`: a fixed date", but `\date{}` is an empty date. |
| 34 | `ZENODO_DESCRIPTION_VOL3.md` | **CONFIRMA** | Matches the body. No GitHub, no "pending". History is kept in the note, not in the text. |

**Totals: 31 CONFIRMA, 3 PROBLEMA (all B), 0 INCERTO.** The PROBLEMA items are 6 (introduction), 17 (Rem 5.4 wording) and 33 (stale "Layer 2" line). None is mathematical. After these one-line fixes the volume is ready for the MAJOR version; they can go to a corrector without another full re-check.

## OBL-008: notes on the re-derivation

- **Step 1** is elementary and complete for any measurable weight with $0<c_0\le\Phi\le C_0$. The weighted extension is therefore **proved in the paper itself** and does not rest on JLM, which is cited only for the unweighted limit. The wording "This unweighted statement is due to Juutinen, Lindqvist and Manfredi" is accurate.
- **Step 2:** $\delta\in W^{1,p}_0$, $\lvert\nabla\delta\rvert=1$ a.e., and $\lVert\delta\rVert_p\to R$.
- **Step 3:**
  - Hölder bounds hold for $q<p_j$.
  - Morrey and Arzelà–Ascoli apply to functions supported in $\bar\Omega$.
  - Weak lower semicontinuity gives $\lVert\nabla u_\infty\rVert_q\le\lvert\Omega\rvert^{1/q}L$, hence $u_\infty$ is $L$-Lipschitz on $\mathbb R^d$.
  - $\lVert u_j\rVert_\infty\ge\lvert\Omega\rvert^{-1/p_j}$, and $u_\infty=0$ on $\partial\Omega$, so $1\le LR$.
  - No hypothesis is missing. Connectedness and the Lipschitz boundary are not even needed.
- **Literature:**
  - I could not read JLM, ARMA 148 (1999) 89–105, DOI 10.1007/s002050050157, either: Springer requires login, Semantic Scholar has the abstract elided by the publisher, and the zbMATH API returned 503.
  - I read Lindqvist, *A nonlinear eigenvalue problem* (lqvist.folk.ntnu.no/nonlineigen.pdf): §4 item VI states $\lim\lambda_p^{1/p}=1/\max\operatorname{dist}(x,\partial\Omega)$, and Lemma 11 gives the same two-step proof (distance test function; compactness with diagonal subsequence). It attributes the result to ref. [27], JLM, *The ∞-eigenvalue problem*.
  - The paper's Step 3 is a slightly more direct variant: a Lipschitz bound instead of the $\Lambda_\infty$ quotient. It is correct.
- **Residual:** the attribution to JLM is confirmed only through Lindqvist's own notes. Lindqvist is a co-author of JLM, so this is a strong secondary source.

## Close

- **Hardest step:** OBL-008 Step 3, the passage from $\lVert\nabla u_\infty\rVert_q\le\lvert\Omega\rvert^{1/q}L$ to a global $L$-Lipschitz bound. It uses that $u_\infty$ is in $W^{1,\infty}(\mathbb R^d)$ with zero extension, which holds.
- **What would falsify the confirmed results:** a bounded domain where the weighted $\lambda_p^{1/p}$ leaves the comparison window. That is impossible by Step 1.
- **Not done:** I did not open the KS, Federer or Gibson et al. books (chapter-level citations), and I did not read JLM directly.
- **Literature consulted:**
  - Lindqvist's notes, §4 VI and Lemma 11;
  - Kawohl–Fridman, abstract via DML-CZ;
  - Crossref/DataCite metadata for all 18 DOIs.
