# Beyond the Spectrum III: blind referee report, layer 1

- Referee: independent Claude subagent (Opus), clean context. I did not read LEDGER, CLAUDE_*, AUDIT_*, ADVERSARIAL_*, PROOF_SKELETON*, the sandbox, WORKPLAN or CHANGELOG.
- Date: 2026-10-06.
- Protocol: `unified_quantum_gravity_book/audit/verify/PROTOCOL.md`, Camada 1.
- Work: *Beyond the Spectrum III: Higher Invariants, Bipartite Kernels, and Non-Equilibrium Geometry of Functional Realizations*. Zenodo concept DOI 10.5281/zenodo.22644743.

## 0. Version check

Script: `scripts/v0_zenodo_versions.py` (output in `.out.txt`), Zenodo REST API.

| Record | Date | Files |
|---|---|---|
| 22644744 | 2026-09-07 | vol 1–3 PDFs, trilogy, `formal_proofs_bts.zip` (old hashes, not local) |
| 22699282 | 2026-09-11 | `beyond_the_spectrum_trilogy_updated.pdf`, `volume_3_higher_invariants.pdf` (md5 48959e0d…), `formal_proofs_bts.zip` |
| **22866175** (latest) | 2026-09-21 | only `beyond_the_spectrum_trilogy.pdf`, 1 391 818 B, md5 8d872f4d98a616fd97873deb230ee5f5 |

What the hashes show:

- The latest record is byte-identical (md5) to the local `beyond_the_spectrum_files/beyond_the_spectrum_trilogy_updated.pdf`. The other referee's finding is **confirmed**.
- The local `volume_3_higher_invariants.pdf` is byte-identical to the Vol. III file of record 22699282.
- The local `beyond_the_spectrum_trilogy.pdf` (md5 78d447d5…) matches no Zenodo file.

**Text comparison** (`scripts/v1_extract_compare.py`, `scripts/v2_substantive_diff.py`):

- Vol. III starts at page 49 of the 59-page trilogy PDF.
- Its extracted text is word-for-word identical to `volume_3_higher_invariants.pdf` (similarity 1.0000, 0 differing blocks). Negative control, Vol. III vs Vol. I: 0.05.
- Extracted texts: `audit/zenodo_22866175_vol3_extracted.txt` and `audit/volume_3_pdf_extracted.txt`.

The local `.tex` differs from the Zenodo text in one substantive way:

- The `.tex` adds three paragraphs at the start of §7 (lines 417–419). They cover the $H_0^s(\Delta_m,d\mu_\alpha)$ domain, a "barrier potential $B_\alpha$ acting as a self-adjoint Friedrichs operator", and the UV bi-Laplacian with clamped $H_0^2$ conditions and "$\alpha_i-3/2\ge-1/2$".
- **None of these paragraphs is on Zenodo.**
- All other differences are artefacts: math macros, hyphenation, title block, and the position of the table float.
- All 21 OBL tags, every statement and every formula are the same in both.

The audit below therefore applies to the Zenodo version. The three extra `.tex` paragraphs are judged separately (item T-7a).

Zenodo record 22866175 contains **no Lean files**. The latest Zenodo text still claims "machine-checked Lean 4 specifications".

## 1. Item table

Severity: **A** = mathematical or physical error, **M** = gap or wrong label, **B** = wording or citation.

| Item | Statement (1 line) | Honest label? | Verdict | Evidence |
|---|---|---|---|---|
| Abs/intro numerical claims | $\Delta F=-\log(\mathrm{Tr}B/\mathrm{Tr}A)$; $d_s=2\log3/\log5\approx1.3652$; "21 results"; "machine-checked Lean 4" | Partly | **PROBLEMA (A/M)** | See §2: the Lean claim is false, the Cheeger and $\mathcal W_2$ claims are false, and several "proving" claims are overclaims. 1.3652 is arithmetically right (n5). |
| OBL-001 Thm | $2\pi(t-\min\Phi)/\lambda_{\max}\le c_1^{EH}(K_t)\le 2\pi(t-\min\Phi)/\lambda_{\min}$ | Yes (elementary) | **CONFIRMA** (B notes) | Taylor expansion with Hessian bounds on the convex $K_t$ gives balls $B(x_0,r_{\min})\subset K_t\subset B(x_0,R_{\max})$, then monotonicity and translation invariance. Notes: (i) these are balls, not "ellipsoids", and the conformality axiom is not needed; (ii) the Clarke dual functional plays no role, and its stated form ($H^*(\dot z)$ instead of $H^*(-J\dot z)$) is non-standard; (iii) inner inclusion needs the first-exit argument along a segment, because $\lambda_{\max}$ is only a sup over $K_t$; this holds but is not said. Quadratic test, 2000 random $Q$: symplectic eigenvalues by two routes, 0 violations; swapped bound fails 2000/2000 (n1). |
| OBL-002 Prop | $c_{HZ}$ is symplectically invariant and equals the minimal action of closed characteristics on convex $\partial K_t$ | Cited classical (Hofer–Zehnder 1994) | **CONFIRMA** (B) | Invariance is a capacity axiom. The min-action formula for convex bodies with smooth boundary is in the HZ book (ch. 3). "$\psi^*\lambda=\lambda+df$" holds on $\mathbb R^{2n}$ because $H^1=0$. No chapter or theorem number is cited. |
| OBL-003 Thm | $\lvert c(a,\Phi_A)-c(a,\Phi_B)\rvert\le\lVert\Phi_A-\Phi_B\rVert_{L^\infty(K)}$ | No | **PROBLEMA (M)** | The statement is ill-posed: "spectral cutoff" is undefined; $H_*(\mathbb R^{2n};\mathbb Z_2)$ is $\mathbb Z_2$ in degree 0 only; the class of Hamiltonians for which $c(a,\cdot)$ exists is not specified (the growth bound $c_1\lvert x\rvert^2\le\Phi\le c_2\lvert x\rvert^2$ allows resonant slopes, where filtered Floer homology changes); and "convex growth" never uses convexity. The standard Lipschitz property uses the **global** Hofer oscillation. The localisation to $L^\infty(K)$ is asserted without proof: continuation-map energy estimates involve the whole Floer cylinder, not $K$. Viterbo 1992 concerns generating functions of compactly supported Hamiltonians and Lagrangians, not this setting. |
| OBL-004 Def | Rank strata $\Sigma_r$ | – | CONFIRMA | – |
| OBL-004 Prop | Transversality to the rank stratification of $\mathrm{Sym}_n$ ⇒ $\{\Sigma_r\}$ is Whitney (A),(B) | Proof by citation, no reference | **CONFIRMA** (B) | The codimension $\binom{n-r+1}{2}$ is correct. The rank stratification is Whitney (homogeneous under congruence, finitely many orbits). Transverse pull-back preserves Whitney regularity (Gibson–Wirthmüller–du Plessis–Looijenga, *Topological stability of smooth mappings*, LNM 552, ch. I). "Mather's condition $(a_f)$" is a different notion (Thom's $a_f$ for maps), so the term is misused. No reference is given. The same tag OBL-004 is used for two items. |
| OBL-005 Lemma | $SS(\mathcal F_A)\subseteq\bigcup\overline{T^*_{\Sigma_r}\Omega}$, closed conic Lagrangian | Overstated | **PROBLEMA (M)** | (i) $\mathcal F_A$ is ill-defined: "vanishing cycles of $\det\Phi$" of *which* sheaf, and they live on $\{\det\Phi=0\}$, not on $\Omega$. (ii) KS ch. 8 (R-constructibility, Lagrangian micro-support, Thm 8.4.2) needs a **real-analytic** manifold and subanalytic strata; here $\Phi$ is only $C^\infty$. (iii) The proof says involutivity gives "isotropic and coisotropic". Involutivity (KS Thm 6.5.4) gives only the coisotropic half; isotropy comes from the inclusion in the conormals. The inclusion itself (KS Prop. 8.4.1) is fine once constructibility with respect to $\{\Sigma_r\}$ is *assumed*, as it is here. |
| OBL-006 Thm | $\chi(\Omega,\mathcal F_A)=CC\cdot[T^*_\Omega\Omega]=\sum_r m_r\chi(\Sigma_r)$ | No | **PROBLEMA (A)** | The first equality is Kashiwara's index theorem (KS Thm 9.5.6, real-analytic $X$, R-constructible, compact support), hypotheses not stated. The **second equality, and the proof's general step "$CC=\sum m_r[\overline{T^*_{\Sigma_r}}]$ ⇒ $CC\cdot[0]=\sum m_r\chi(\Sigma_r)$", is false.** Counterexample: $\Omega=S^1$, $\Phi(\theta)=\cos\theta$ ($n=1$, transverse), constant sheaf. $\chi(S^1)=0$, but $\sum m_r\chi(\Sigma_r)=1\cdot\chi(\text{2 open arcs})=2$. The correct stratified formula is $\chi=\sum_\alpha\chi_c(\Sigma_\alpha)\,\chi(F_{x_\alpha})$ $=-2+2=0$ (n5). For non-closed strata, conormal–zero-section intersections involve local Euler obstructions, not $\chi(\Sigma_r)$. "Local Milnor multiplicities" $m_r$ are never defined. The identity is unproven for $\mathcal F_A$ itself. |
| OBL-007 Def | Weighted Rayleigh–Finsler quotient | – | CONFIRMA | – |
| OBL-007 Lemma | The first $p$-eigenvalue is attained by a unique positive $u_p\in C^{1,\alpha}$, $\lambda_1^{(p)}>0$ | True (classical: Lindqvist 1990, weighted variants) | **PROBLEMA (M)** proof gap | Existence and positivity are OK (replace $u$ by $\lvert u\rvert$, then Harnack). **Simplicity is mis-proved**: the Rayleigh quotient is not convex, and strict convexity of $v\mapsto\lvert\nabla v\rvert^p$ does not by itself give uniqueness. One needs Lindqvist's hidden-convexity argument $((u^p+v^p)/2)^{1/p}$ or a Picone identity. "Unique" should read "unique up to positive multiples". $C^{1,\alpha}$ holds only locally (interior). No citation is given. |
| OBL-008 Thm | $\lim_{p\to\infty}(\lambda_1^{(p)})^{1/p}=h(A)$ (weighted Cheeger) | **No** | **PROBLEMA (A), false** | (1) The known limit is $\Lambda_\infty=1/\text{inradius}$ (Juutinen–Lindqvist–Manfredi 1999), not the Cheeger constant. **Unit disk, $\Phi\equiv1$** (admissible): the radial shooting solution gives $\lambda_p^{1/p}=2.405,1.957,1.596,1.359,1.212,1.123$ for $p=2,\dots,64$. This sits under the rigorous test-function bound $((p+1)(p+2)/2)^{1/p}\to1$ and tends to $1$, while the Cheeger constant of the disk is $2$ (n2; $p=2$ oracle $j_{0,1}$ matched to $10^{-8}$). (2) With the paper's **relative** perimeter $\partial^*E\cap\Omega$, taking $E=\Omega$ gives $h(A)=0$ for every $A$, so the stated identity fails even more plainly. (3) **Misattribution**: Kawohl–Fridman 2003 prove $\lambda_p\to h$ as **$p\to1$** (abstract checked on DML-CZ). It is an unweighted result and contains no "$\Lambda_\infty=h$". The quoted "Theorem 1.1 and Section 2" content does not exist as described. |
| OBL-009 Thm | Simply connected complete, $\mathrm{Sec}\le-\kappa_0$ ⇒ $\delta\le\ln(1+\sqrt2)/\sqrt{\kappa_0}$ | Classical corollary (Cartan–Hadamard, CAT($-\kappa$), B–H III.H.1) | **CONFIRMA** (B) | The constant is right: the numeric slim constant of the ideal triangle is 0.881374 $=\ln(1+\sqrt2)$ (n1). The proof calls it the "inscribed radius". The inradius is $\tfrac12\ln3=0.5493$, a different number (negative control). The conformal structure $\Phi^{2/d}\delta$ plays no role, and "stability" in the title is unjustified. |
| OBL-010 Prop | $V_A$ $\kappa$-convex ⇒ unique invariant $\mu_A=\Phi/\mathrm{Tr}A$, CD($\kappa,\infty$), $\mathcal W_2$-contraction $e^{-\kappa t}$ | True on $\mathbb R^d$ | **PROBLEMA (M)** | The statement is true for $\Omega=\mathbb R^d$ (synchronous coupling). (i) $\Omega$ is a "domain" with no boundary condition, so on a bounded $\Omega$ the SDE exits and the claim is ill-posed. (ii) Non sequitur: LSI ⇒ Talagrand does **not** imply $\mathcal W_2(\mu_t,\mu_A)\le e^{-\kappa t}\mathcal W_2(\mu_0,\mu_A)$. One needs coupling or EVI/$\kappa$-convexity of the entropy. |
| OBL-011 Thm | Jarzynski: $\mathbb E[e^{-W}]=Z(B)/Z(A)=\mathrm{Tr}B/\mathrm{Tr}A$ | Cited classical + normalisation by hypothesis | **CONFIRMA** (B) | The signs are right ($F=-\log Z$, $e^{-\Delta F}=Z_B/Z_A$). Monte Carlo on a Gaussian protocol with $Z(A_s)=\mathrm{Tr}A_s$ gives $2.5013\pm0.0033$ (dt refined: 2.5017) vs $2.5$; mutated ratio $0.4$ rejected (n3). "Tr" enters only through the assumption $\int\Phi(A)=\mathrm{Tr}A$. The Crooks relation is credited to Jarzynski 1997 instead of Crooks 1999. Units $k_BT=1$ are implicit. |
| OBL-012 Thm | $\lim\tau\inf\Sigma_{\rm irr}=\tfrac12\mathcal L^2\ge\tfrac\kappa4\mathcal W_2^2$ | **No** | **PROBLEMA (A), false** | **Counterexample**: dragged trap $V_s=\kappa(x-sa)^2/2$, $\mathcal W_2=\lvert a\rvert$. Closed form $\tau\langle W\rangle=a^2(1-(1-e^{-\kappa\tau})/(\kappa\tau))\to a^2$, confirmed by Monte Carlo. The friction metric from the paper's own formula gives $g=a^2$, $\mathcal L^2=a^2$. For $\kappa=10$ the claimed bound needs $\ge2.5a^2$, but the true limit is $a^2$. (ii) The equality "$=\tfrac12\mathcal L^2$" contradicts the paper's own expansion: Cauchy–Schwarz gives $\mathcal L^2$, observed $1$ vs claimed $0.5$. (iii) **Dimensional inconsistency** (units $k_BT=1$, $D=1$): $\tau\Sigma$ and $\mathcal L^2$ have dimension time = length², while $\kappa\mathcal W_2^2$ is dimensionless. The physically correct statement is $\lim\tau\Sigma\ge\mathcal W_2^2/D$ (Aurell et al. 2011), with no $\kappa$. The proof's "$\int e^{-\kappa t}=1/\kappa$" would give an *upper* bound on the friction, and "$g_{\rm fric}\ge\frac\kappa2 g_{\rm Otto}$" is asserted with no proof (n3; the control with $\kappa=1$ passes). |
| OBL-013 Prop | $K_A=\sum\lambda_j\phi_j\bar\phi_j$, $T_A\ge0$, $\mathrm{Tr}\,T_A=\mathrm{Tr}A$, diagonal $=\Phi_{\rm scalar}$ | Yes | **CONFIRMA** (B) | Direct algebra, checked numerically to $10^{-15}$ (n4). The notation $\mathcal S^n_+$ means "positive definite" in §2 and "positive semidefinite" here. |
| OBL-014 Thm | $\rho_{\Omega_1}=\mathrm{Tr}_2K_A$ has **rank $r\le n$**; $K_{\Omega_1}=-\log\rho$ is **strictly positive**; regularised version has $\ker=\{0\}$ | **No** | **PROBLEMA (A)** | (1) **False rank bound.** $\mathrm{Tr}_2\lvert v\rangle\langle v\rvert$ has the Schmidt rank of $v$, which is infinite for non-product $v$. Example $n=1$, $\psi\propto e^{-(x^2+y^2)/2+0.6xy}$: Schmidt eigenvalues are geometric with ratio $q=0.111111$, matching Mehler exactly, so the rank is infinite (n4; separable control gives rank 1; stable under $N=200,400,800$). The bound holds only if every $\psi_k$ is a finite sum of products, e.g. product eigenfunctions. The paper allows "localized wavelet packets". (2) $\rho_{\Omega_1}$ is **unnormalised** ($\mathrm{Tr}=\mathrm{Tr}A$), so $p_k>1$ is possible and $E_k=-\log p_k<0$: $n=1$, $A=5$ gives $E=-1.609$. Even after normalisation, rank 1 gives $E=0$, not strictly positive. (3) "Strictly p.d. reproducing kernel ⇒ integral operator injective" needs integral strict positive definiteness (B). |
| OBL-015 Thm | $S_R\ge0$, symmetric, $S_R\ge I(\Omega_1:\Omega_2)$ | Cited (Dutta–Faulkner 2021) | **CONFIRMA** (B) | Correct: $S_R=I(A:BB^*)\ge I(A:B)$ by monotonicity. 300 random states: 0 violations of $S_R\ge I$ or $S_R\le2\min(S_A,S_B)$; symmetric; two computational routes agree. Mutated $S_R\ge2I$ fails 234/300 (n4). In infinite dimension, finiteness of the entropies is not addressed. |
| OBL-016 Thm | Holographic $S_R\ge2E_W=\min\mathrm{Area}/(2G_N)$ | **No** | **PROBLEMA (M)** | This is a holographic-duality *proposal* (Dutta–Faulkner: $S_R=2E_W$ at leading order in $G_N$, derived by a gravitational replica argument assuming AdS/CFT). It is not a theorem. "Functional bulk geometry $(M,g_A)$" and "boundary dual $\rho_A$" are never constructed from $K_A$. The label should be conjecture or physical heuristic. The factor ($E_W=\mathrm{Area}/4G_N$) is consistent. The abstract says "proving". |
| OBL-017 Prop | $\mathcal Z_A(s)$ holomorphic for $\mathrm{Re}\,s>-\min\alpha_i$ | True but mis-stated | **PROBLEMA (M)** | $0<c_1\le\Phi\le c_2$ and $\mu_\alpha$ is a probability measure, so $\mathcal Z_A$ is **entire**. The half-plane condition is spurious, and the proof's "density integrable for $\mathrm{Re}\,s>-\min\alpha_i$" confuses $s$ with the density, which does not depend on $s$. |
| OBL-018 Thm | Meromorphic continuation with simple poles at $s=-\alpha_j-k$, non-zero residues | **No** | **PROBLEMA (A), false** | $\mathcal Z_A$ is entire (see OBL-017), so it has no poles. The trivial counterexample $\Phi\equiv c$ gives $\mathcal Z=c^s$. Numerically, $\Delta_2$, $\alpha=(1/2,3/2)$, $\Phi=1+u$: $\mathcal Z$ is finite and continuous at all claimed poles. Quadrature agrees with ${}_2F_1(-s,a;a+b;-1)$, and the pole detector flags $B(s+a,b)$ (negative control) (n5). The proof confuses $\int\Phi^s d\mu$ with $\int u^{s+\alpha-1}$. |
| OBL-019 Cor | $d_s=2\log N/\log(N/\rho)$; SG $=2\log3/\log5\approx1.3652$ | Cited classical, mislabelled "Corollary" | **PROBLEMA (M)** | The formula is the classical result (Kigami–Lapidus 1993; Fukushima–Shima 1992), and the arithmetic is right (n5). It does **not** follow from OBL-017/018: $\mathcal Z_A$ is entire and unrelated to the fractal heat trace. The sign convention $s_0=-d_s/2$ is unexplained (the Mellin transform of the heat trace has its pole at $+d_s/2$). The SG heat trace has log-periodic oscillations, so "scales as $t^{-d_s/2}$" holds only up to a bounded oscillating factor. "Verified on the benchmark" is just a substitution. |
| OBL-020 Thm | $\mathrm{reach}(\Sigma_t)\ge\min(\epsilon_0/M,\tfrac12d_{\rm sep})$; strictly convex ⇒ $d_{\rm sep}=\infty$ | Partly | **PROBLEMA (M)** | The main bound is OK **for compact $\Sigma_t$**, using the characterisation reach $=\min(1/\kappa_{\max},\tfrac12$ bottleneck$)$ (Aamari et al. 2019, not Federer 1959). The relevant bottleneck pairs have antiparallel normals, so the paper's $d_{\rm sep}$ is $\le$ the bottleneck and the bound follows. (i) Compactness and closedness of $\Sigma_t$ are missing. Counterexample: $\Phi(x,y)=y$ on $\Omega=(0,1)^2$ gives $\Sigma_t$ an open segment, reach $0$, while the bound gives $\infty$. (ii) **"$d_{\rm sep}=\infty$ for strictly convex" is false**: antipodal points of an ellipse or sphere have antiparallel normals, and the ellipse $(2,1)$ has $d_{\rm sep}\le2b=2$. The convex conclusion reach $\ge\epsilon_0/M$ is still true (Blaschke rolling). Brute-force reach $0.5=b^2/a=\epsilon_0/M$ (n5). (iii) The citation of Federer 1959 for the bottleneck characterisation is wrong. |
| OBL-021 Thm | For $r<$ reach: $U_r\cap$ medial axis $=\emptyset$, projection Lipschitz, $\mathrm{Vol}(U_r)=\sum\frac{2r^{2k+1}}{2k+1}\int H_{2k}$ | Classical (Weyl; Federer Thm 4.8) | **CONFIRMA** (B) | Exact for $S^3\subset\mathbb R^4$. Ellipse tube by Monte Carlo agrees with $2r\cdot$Per; mutated factor rejected (n5). Missing hypotheses: compact, orientable $\Sigma_t$. $H_{2k}$ means the *unnormalised* elementary symmetric functions. "$\mathrm{Unp}(\Sigma_t)^c$" is Federer's notation but should be explained. |
| T-7a (`.tex` only, not on Zenodo) | $H_0^s$ domain, "barrier potential … Friedrichs operator annihilates boundary support", "$\alpha_i-3/2\ge-1/2$" | – | **PROBLEMA (M)** | Undefined objects ($B_\alpha$, $s$, "Dirac–Kähler fields"). "$\alpha_i-3/2\ge-1/2$" silently assumes $\alpha_i\ge1$, which OBL-017 does not assume. None of it is used anywhere. |
| Table 1 | Taxonomy, "Codomain" column | – | B | $CC(\mathcal F_A)$ is not $\mathrm{Sym}_n$-valued, and $\mathcal Z_A(s)$ is not "$\Delta_m$"-valued. The symmetry groups are unjustified. |
| Bibliography | 17 entries | – | **PROBLEMA (B)** | All DOIs resolve via Crossref/DataCite (script c1; mutated-DOI control fails). Problems: **SilvaFilho2026c (Vol. II) carries DOI 22441676, which is the cobordism paper**; SilvaFilho2026b's title does not match DataCite ("Geometry, Tensors, and Quantum Gravity"); SilvaFilho2026a/b/c are never cited; key "Aurell2012" points to the 2011 paper; Kawohl–Fridman is misattributed (see OBL-008); Viterbo 1992 is cited for Floer spectral invariants of quadratic Hamiltonians, which it does not cover. |
| Lean claim | "All 21 results … aligned with machine-checked Lean 4 specifications", "synchronized 1:1" | **No** | **PROBLEMA (A)** for the claim | The local folders `formal_proofs_bts3/` and `formal_proofs_bts/` contain **only `.lake` build artefacts, no sources**. The zip from record 22699282 (copied to `audit/lean_zenodo/`) has **no `import Mathlib`**. The "structures" have `Nat` fields such as `work_ratio : Nat` with `work_ratio_exact` as a field. The theorems return their own hypotheses: `thermo_length_geodesic_w2 (h_bound : X) : X := h_bound`, `jarzynski_free_energy_id … := proto.work_ratio_exact`. It even encodes the false OBL-012 bound as an assumption. It verifies nothing. The latest Zenodo record carries no Lean at all. |

## 2. Abstract and introduction vs body

| Claim in abstract or introduction | What the body gives |
|---|---|
| "generalized Ekeland–Hofer capacities $c_k^{EH}$" | Only $c_1$ is treated. |
| "sharp $C^0$-Lipschitz stability" | OBL-003 is ill-posed and unproven; "sharp" is unproven. |
| "rigorously establishing the Kawohl–Fridman Cheeger limit … through two-sided variational bounds" | **False** (OBL-008). No two-sided bounds appear anywhere. |
| "proving … Whitney … via Mather" | Correct modulo citation. |
| "$CC$ computes global Euler characteristics" | The second formula is false (OBL-006). |
| "thermodynamic length lower-bounds $\mathcal W_2$" | **False as stated** (OBL-012). |
| "proving $S_R\ge2E_W$" | Conjecture-level physics (OBL-016). |
| "extracting the discrete Barnes–Kigami residue spectrum" | There are no poles (OBL-018). |
| "proving the exact fractal spectral dimension identity (verified on the Sierpinski gasket benchmark)" | A classical result cited; not proved here, not verified. |
| "machine-checked Lean 4" | False. |
| "21 theoretical results" | Tags OBL-004 and OBL-007 are each used twice (definition + result). |

Non-equilibrium physics (dimensional check, units $k_BT=1$, $D=1$, $[x]^2=[t]$):

- $V$, $W$, $\Delta F$ are dimensionless. **Correct.**
- In OBL-012, $\tau\Sigma$ and $\mathcal L^2$ have dimension length², while $\kappa\mathcal W_2^2$ is dimensionless. **Inconsistent.**
- The paper gives no physical numbers, so no CODATA estimate applies.

## 3. Summary by severity

**A: mathematical or physical errors (7)**

1. OBL-006: the stratified Euler formula $\sum m_r\chi(\Sigma_r)$ is false (counterexample on $S^1$).
2. OBL-008: $\lim\lambda_p^{1/p}$ is the reciprocal inradius, not $h(A)$. The unit disk gives 1 vs 2, and the relative-perimeter $h$ is $0$. The theorem is misattributed: Kawohl–Fridman is about $p\to1$.
3. OBL-012: $\tfrac12\mathcal L^2\ge\frac\kappa4\mathcal W_2^2$ is false (dragged trap, $\kappa=10$) and dimensionally inconsistent. The factor $\tfrac12$ contradicts the paper's own expansion.
4. OBL-014: "rank $\le n$" fails for non-product frames (Mehler example, infinite rank). "$K_{\Omega_1}$ strictly positive" fails for an unnormalised $\rho$.
5. OBL-018: $\mathcal Z_A$ is entire, so the claimed poles and residue spectrum do not exist.
6. The Lean "machine-checked" claim is false: no Mathlib, `Nat` placeholders, hypotheses returned as conclusions, no sources locally or in the latest record.
7. The abstract states results 2–5 as proved.

**M: gaps or wrong labels (10)**

- OBL-003: ill-posed, local $L^\infty(K)$ unproven.
- OBL-005: real-analytic hypothesis missing; $\mathcal F_A$ ill-defined.
- OBL-007 Lemma: simplicity proof invalid.
- OBL-010: domain or boundary unspecified; Talagrand ⇏ $\mathcal W_2$ contraction.
- OBL-016: physics proposal labelled "Theorem".
- OBL-017: "half-plane" when the function is entire; wrong reasoning.
- OBL-019: classical result labelled a corollary of a false theorem.
- OBL-020: compactness missing; "$d_{\rm sep}=\infty$ for convex" false.
- T-7a: undefined `.tex`-only paragraphs.
- Abstract overclaims ($c_k$, "sharp", "verified").

**B: wording or citations**

- OBL-001 ("ellipsoid", Clarke functional)
- OBL-002 (no theorem number)
- OBL-004 ("$(a_f)$" misuse, no reference, duplicate tags)
- OBL-009 ("inscribed radius")
- OBL-011 (Crooks credited to Jarzynski)
- OBL-013 ($\mathcal S_+^n$ notation)
- OBL-015 (infinite-dimensional finiteness)
- OBL-021 (missing hypotheses)
- Table 1
- Bibliography: wrong Vol. II DOI, title mismatch, uncited self-references.

**Confirmed (8):** OBL-001, 002, 004 (Def + Prop), 007 (Def), 009, 011, 013, 015, 021, all with B notes.

## 4. Scripts

Folder: `audit/scripts/`; every script has an `.out.txt`; all exit 0. Each check uses an independent oracle and a negative control.

| Script | What it checks |
|---|---|
| `v0_zenodo_versions.py` | Zenodo API and md5 hashes |
| `v1_extract_compare.py`, `v2_substantive_diff.py` | Text extraction and diff; control Vol. I |
| `c1_resolve_dois.py` | Crossref/DataCite resolution; control: mutated DOI |
| `n1_symplectic_hyperbolic.py` | OBL-001 (two routes to symplectic eigenvalues; swapped bound control), OBL-009 (slim constant vs inradius) |
| `n2_cheeger_p_infinity.py` | OBL-008. Oracles: $p=2$ Bessel zero, rigorous test-function bound. Refinement over two tolerances and two start radii. Control: the claimed value 2 |
| `n3_thermo.py` | OBL-011/012. Closed form, Monte Carlo (dt refinement) and friction-metric quadrature. Controls: $\kappa=1$, mutated ratio |
| `n4_kernel_entropy.py` | OBL-013/014/015. Mehler oracle with $N$ refinement; separable control; $S_R\ge2I$ control |
| `n5_mellin_geometry.py` | OBL-006/017/018/019/020/021. ${}_2F_1$ oracle; Beta-pole control; brute-force reach; Monte Carlo tube; doubled-bound and halved-tube controls |

On its first run, n5's pole detector was too lax: it did not flag the negative-control pole. I replaced it with a growth-ratio test, after which the control was flagged and no claimed pole of $\mathcal Z_A$ was. The tolerances were not tuned to make the run pass.

The Lean sources inspected are in `audit/lean_zenodo/` (from record 22699282's `formal_proofs_bts.zip`, md5 a98a98ee…).

## 5. Hardest step, what is missing, literature

- **Hardest step to judge:** OBL-003. A counterexample to the local $L^\infty(K)$ Lipschitz bound would need an explicit Floer computation, which was not attempted. The verdict is "unproven and ill-posed", not "false".
- **What would overturn the A verdicts:**
  - a different definition of $h(A)$, with full perimeter and $p\to1$;
  - restricting OBL-014 to product frames with normalised $\rho$;
  - restating OBL-012 as $\lim\tau\Sigma=\mathcal L^2\ge\mathcal W_2^2$;
  - an $\mathcal F_A$ for which the $\chi(\Sigma_r)$ formula happens to hold. For $n=2$ the vanishing-cycle sheaf lives on the closed stratum $\Sigma_0$ and the identity holds there. The proof's general step remains false.
- **Literature consulted:**
  - Kawohl–Fridman, CMUC 44 (2003): DML-CZ abstract, the $p\to1$ result.
  - Juutinen–Lindqvist–Manfredi, ARMA 148 (1999), DOI 10.1007/s002050050157: $\Lambda_\infty=1/R$. I could not open the abstract online (Springer redirect), so this rests on the referee's knowledge plus the numerics in n2.
  - Kashiwara–Schapira 1990: Prop. 8.4.1, Thms 6.5.4, 8.4.2, 9.5.6.
  - Aurell et al., PRL 106 (2011) 250601.
  - Dutta–Faulkner, JHEP 03 (2021) 178.
  - Aamari et al., EJS 13 (2019), on reach and bottleneck.
  - Kigami–Lapidus, CMP 158 (1993).
