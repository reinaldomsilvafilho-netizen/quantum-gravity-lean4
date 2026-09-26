# Corrections, 2026-09-25: *A Metric-Measure Framework for the Gribov–Zwanziger Formulation of Yang–Mills Theory*

This note lists the changes made to `paper_yang_mills_mass_gap.tex` in this correction pass, and it is also the Zenodo version note.

**Previous title:** *A Geometric and Metric-Measure Framework for the Yang-Mills Mass Gap, Gribov-Zwanziger Horizon Regularization, and Confinement on Gauge Orbit Varieties*.

**New title:** *A Metric-Measure Framework for the Gribov–Zwanziger Formulation of Yang–Mills Theory: Conditional Mass-Gap Criteria and Open Problems*.

**Summary.** The previous version stated a mass gap, an area law with an explicit string tension, vacuum uniqueness and a resolution of the strong CP problem. None of these is proved in the paper. The Yang–Mills existence and mass-gap problem is open, and the paper now says so.

What remains:
- one conditional theorem, whose hypotheses are stated explicitly;
- seven proved or classical propositions;
- the Vafa–Witten inequality, cited as classical;
- one conjecture (the area law).

Evidence:
- `check_ym_claims_2026_09_25.py`: 33 checks, each with an independent oracle and, where meaningful, a negative control. Output is in `check_ym_claims_2026_09_25.out`.
- `check_dois_2026_09_25.py`: all 39 DOIs resolve through Crossref, or through doi.org for the two Zenodo DOIs. Output is in `check_dois_2026_09_25.out`.

**Build.** `pdflatex -interaction=nonstopmode`, run twice, gives 11 pages, 0 errors, 0 warnings and 0 overfull boxes.

## Counts

| Category | Count |
|---|---|
| Correct as stated (kept, citation added where classical) | 8 |
| Fixed (numbers, signs, dimensions, definitions, attributions, framing) | 14 |
| Demoted to conditional statement or conjecture | 5 |
| Removed (false or unsupported; replaced by a neutral remark where useful) | 10 |
| Left open | 8 |

## Item table

Numbering: "old" refers to the environment numbers of the file before this pass.

| # | Item | Problem | Evidence | Action |
|---|---|---|---|---|
| 1 | Title, abstract (i)–(vi) | Claimed a cutoff-independent mass gap $\Delta\ge C_N\Lambda_{\overline{\rm MS}}$, an area law with $\sigma=\frac\pi2\kappa^{*2}$, vacuum uniqueness via Floer homology, and CP invariance. None of these is proved (items 9–17). | reading; items below | **Fixed.** New title and abstract. The only main result is the conditional criterion; the open problems are listed. |
| 2 | Introduction, Remark 1.1; Conclusion §9.1 | Claimed a gauge-Laplacian gap $\lambda_1=2.450$ on $\Delta_4\times\Delta_2$, Gribov copies "topologically excluded", and the physical problem "fundamentally resolved". The monograph (Ch. 12) defines the $\Delta_4\times\Delta_2$ action only schematically and contains no gauge measure, no gap and no Gribov analysis. The number appears only in an unaudited research draft. Contractibility does not exclude Gribov copies (Singer 1978). | `grep` over `unified_quantum_gravity_book/chap*.tex`; Ch. 12 §7 | **Removed.** Replaced by neutral Remark 1.1: the simplicial framework is not used. |
| 3 | $\beta_0,\beta_1$, two-loop $\Lambda_{\overline{\rm MS}}$ | Correct. | SymPy: residual $O(g^4)$; flipped exponent leaves $O(g^2)$ | **Correct**, kept. |
| 4 | Lattice numbers ($m_{0^{++}}\approx1.7$ GeV, $\sqrt\sigma\approx440$ MeV, ratio 6.8) | The values are right in order of magnitude. The paper "calibrated" $C_N$ in a lower bound to the measured mass, which is a fit, not a bound. Teper 1998 is about 2+1 dimensions (its title was misquoted), and Lüscher 1986 is not a source for these values. | $r_0m=4.21$ (Morningstar–Peardon), $r_0\Lambda=0.602$ (Capitani et al.) give $7.0$ | **Fixed.** Ratio $\approx7.0$ with sources; Athenodorou–Teper 2020 cited; Teper 1998 and Lüscher 1986 removed; stated as empirical input. |
| 5 | Old Hyp. 2.1 (GZ measure on $\Omega\subset\mathcal A/\mathcal G$) | Mixed a 4D Euclidean action with a Hilbert space of 3D spatial connections. | reading | **Fixed.** Now Hyp. 2.1: a ground-state measure $\mu_0$ on the spatial Gribov region, with measurable holonomies. |
| 6 | Old Def. 2.3 (Mandelstam ideal) and Thm. 2.4 (Hilbert space $=L^2/\overline{\mathcal I}$) | The Mandelstam identities hold identically as functions, so the "ideal" is $\{0\}$ in $L^2$ and the quotient is trivial. The Cayley–Hamilton relation was misstated. Spin networks are orthonormal for Haar measure, not for $\mu_0$. | Haar-random SU(2)/SU(3) check; sign-flip control fails | **Demoted and fixed.** Prop. 2.3 (conditional on Hyp. 2.1): separability and Gauss law with a complete proof. The Mandelstam material is now Remark 2.4. |
| 7 | Old Thm. 3.1 (RG irrelevance, microcausality) | The flow had the wrong sign ($-2\alpha$ instead of $+2\alpha$). The kernel dimension was given as $2\alpha$ (it is $4+2\alpha$; the coupling has $-2\alpha$). A dimensionless $O(\cdot)$ was added to a dimension-4 density. The operator was not gauge covariant. Exact microcausality was claimed, although power suppression does not give it. The spectral-dimension statement disagreed with Ch. 12 (a homogeneous symbol has constant $d_s=4/\alpha$). | SymPy | **Fixed** (Prop. 3.1, tree level, covariant $(-D^2)^\alpha$). The exact-microcausality claim is **removed** (Remark 3.2). Now consistent with Ch. 12: UV value $4/(1+\alpha)$. |
| 8 | Old Gribov-region definition | Wrote $\mathcal M_A=-D_A^*D_A>0$. That operator is $\le0$ for every $A$, and $D_A^*D_A\ge0$ has no horizon. It also placed $\Omega$ in $\mathcal A/\mathcal G$ and conflated the Gribov region with the fundamental modular region. | $-D^TD\le0$ numerically; reading | **Fixed.** Def. 4.1: $\mathcal M(A)=-\partial\cdot D(A)$ on the transverse slice; $\Lambda_{\rm mod}\subset\Omega$ distinguished (van Baal 1992). |
| 9 | Federer reach of $\Omega$ (old Thm. 6.1, abstract (v)) | $\Omega$ is convex because $\mathcal M(A)$ is affine in $A$, so its reach is $+\infty$. The quantity computed was a distance to the horizon. | random convex combinations: 0 violations; Federer 1959 §4 | **Removed.** Replaced by Prop. 4.2(d) ($\mathrm{reach}=\infty$, classical) and Prop. 6.1. |
| 10 | Horizon-distance computation (old Thm. 6.1 proof) | The mode $\sin(\pi x/L)$ is not periodic on $T^3_L$. The eigenvalue shift was taken as linear in the amplitude (it is quadratic) with a spurious $\sqrt N$. With $L=2/\Lambda$, the paper's own $\|A\|^2=\pi^2L/(2g^2N)$ equals $\pi^2/(g^2N\Lambda)$, not $\pi^2/(g^2N\Lambda^2)$: $\|A\|_{L^2(\Sigma)}$ has mass dimension $-\frac12$. The distance scales as $L^{1/2}$ and diverges as $L\to\infty$, so it gives no intrinsic scale. | Mathieu vs finite differences (agreement $10^{-5}$); $a_cgL=11.97$; log-log slope $0.500000$; second-order onset | **Removed.** Replaced by Prop. 6.1 (exact $L^{1/2}$ scaling, proved) and Remark 6.2 (explicit SU(2) ray). |
| 11 | String tension $\sigma=\frac\pi2\kappa^{*2}=\frac{g^2N}{2\pi}\Lambda^2$ (old Thm. 6.1 (2)–(3)) | $E_0=\kappa^{*2}$ was asserted without derivation. With the $\kappa^*$ above, $\sigma$ has mass dimension 1, not 2. In the London flux tube, $E_0$ is fixed by flux quantization. The integral $\int xK_0^2=\frac12$ and the energy per length $\pi E_0^2/(2m^2)$ are correct. | quadrature | **Removed.** Remark 6.3 keeps the correct integrals as a dual-superconductor model (Nambu; Mandelstam; 't Hooft). |
| 12 | Wilson area law (old Thm. 6.1 (4)) | Not proved. It is the open confinement problem. | literature (Osterwalder–Seiler 1978: strong-coupling lattice only) | **Demoted** to Conjecture 6.4. |
| 13 | Old Hyp. 4.1 and Thm. 4.2 ($\mathrm{Ric}_\infty\ge K_{\rm QCD}$, Savvidy "resolution") | (i) The AM-GM step applied $T+\gamma^4T^{-1}\ge2\gamma^2$ to two *different* operators (1-form Laplacian vs. $\mathcal M^{-1}$); the $2\times2$ check fails. (ii) From $\mathrm{Hess}\ge K-\varepsilon$ the proof concluded $\ge K$. (iii) The Ricci curvature of $\mathcal A/\mathcal G$ is only formal: an infinite trace (Singer 1981; Babelon–Viallet 1981). (iv) Log-concavity of $e^{-S_{\rm GZ}}$ is not established. (v) The measure relevant to the Hamiltonian is the ground-state measure, not $e^{-S_{\rm GZ}}$. | counterexample min eig $0.033<3.03$; reading | **Removed** as a theorem. The correct part is Prop. 4.4 (tree level, $A=0$). The obstacles are listed neutrally in Remark 4.5. Hypothesis restated as Hyp. 5.3 (item 15). |
| 14 | Old Remark "Cartan directions: horizon term vanishes" | False: $\mathrm{ad}(A)\ne0$ for $A$ in a Cartan subalgebra, and $[A_\mu,A_\mu]=0$ holds for every $A$. | $\lvert[H,E]\rvert=0.5$ | **Removed.** Now Remark 4.5(iv). |
| 15 | Old Hyp. 5.1 ($\Delta\ge\sqrt{\lambda_1(\mathcal L)}$ via $(\hat H-E_0)^2\sim\mathcal L$) | Not a known relation. The ground-state representation gives $H-E_0\cong\frac\varepsilon2\mathcal L$, which is **linear**. The square root was introduced to make the dimensions of $K\sim\gamma^2$ come out right. The Parisi–Wu generator acts in fictitious time. | harmonic ($\omega=3$) and anharmonic oscillators: $\lambda_1=2\Delta$ to $10^{-4}$; $\sqrt{\lambda_1}$ control fails | **Removed.** Replaced by Prop. 5.1 (classical: ground-state representation plus Bakry–Émery, finite dimensions, sharp) and Remark 5.2. |
| 16 | Old Thm. 5.2 (mass gap $\Delta\ge\sqrt{K_{\rm QCD}}=C_N\Lambda$) | Rested on items 13 and 15. $c_0=(N-1)/(2N)$ was never derived, and $C_N$ was fitted to the lattice. | — | **Demoted** to Conditional Theorem 5.4 under Hyp. 5.3 (uniform $\mathrm{CD}(K_n,\infty)$ for regularized ground-state measures plus strong resolvent convergence), with a complete proof (Reed–Simon VIII.24). The bound is $g^2K/2$. |
| 17 | Old Thm. 7.1 (Floer homology, vacuum uniqueness) | $\mathcal A/\mathcal G_0$ is connected (it is not a union of components labelled by winding). $\partial|n\rangle=|n-1\rangle$ implies $\partial^2|n\rangle=|n-2\rangle\ne0$. Floer homology uses irreducible flat connections, and on $S^3$ the only flat connection is trivial. Charge-1 SU(2) moduli have dimension 8, not 1. Minimizing $E(\theta)$ says nothing about uniqueness at fixed $\theta$ (superselection). | shift-matrix check; literature | Floer part **removed**. Tight-binding $E(\theta)=E_0-2\Delta\cos\theta$ is **correct** (Prop. 7.1, Callan–Dashen–Gross, Jackiw–Rebbi). Vacuum uniqueness **demoted** to open (Remark 7.2). |
| 18 | Old Thm. 8.1 (Vafa–Witten, strong CP) | The inequality is Vafa–Witten's, but the proof invoked reflection positivity and Cauchy–Schwarz, where the actual argument is positivity of the $\theta=0$ measure. "Resolving the strong CP problem without an axion" is false, because $\theta$ is a parameter. Reflection positivity of the localized GZ measure was asserted but is unknown, and the ghost reflection assignments were arbitrary. | reading | Inequality **correct**, cited as classical (Thm. 8.1) with the correct proof. The strong-CP and GZ reflection-positivity claims are **removed** (Remark 8.2). |
| 19 | Old Def. of $S_{\rm GZ}$ and gap equation | Used $\int_\Sigma d^3x$ in a 4D action, omitted $g^2$, and had coefficient $Ng^2/(N^2-1)$ instead of $\frac34Ng^2$. The UV log divergence was not mentioned. $\gamma$ was confused with $\lambda$ ($\lambda^4=2g^2N\gamma^4$). | quadrature vs closed form $\ln(1+\Lambda^4/\lambda^4)/(32\pi^2)$ | **Fixed** (Def. 4.3, following Zwanziger 1989 and Vandersickel–Zwanziger 2012). |
| 20 | Knife-edge remark ($k^2+\gamma^4/k^2\ge2\gamma^2$, saturated at the propagator maximum) | Correct at tree level, $A=0$. | SymPy $D'(\lambda)=0$ | **Correct**. Now Prop. 4.4 with proof. |
| 21 | O'Neill formula $K=\frac34\lVert[X,Y]^{\rm vert}\rVert^2$ | Correct but formal on $\mathcal A/\mathcal G$. It was attributed to Lott–Villani and to the author's own work. | literature | **Correct**. Now cited to O'Neill, Singer 1981 and Babelon–Viallet 1981 (Remark 4.5(v)). |
| 22 | RGZ remark | Claimed "the gap is preserved in RGZ because the condensates add positive mass terms", with no proof. Lattice papers were named but not cited. | reading | **Fixed.** Credit is now to Dudal–Sorella–Vandersickel–Verschelde (PRD 77, 2008) and Dudal–Gracey–Sorella–Vandersickel–Verschelde (PRD 78, 2008); Cucchieri–Mendes 2008 and Bogolubsky et al. 2009 cited; the gap claim is removed. |
| 23 | Prior-art credit (Gribov 1978, Zwanziger 1982/1989, Vandersickel–Zwanziger 2012) | The framework was presented as a synthesis that "we establish". The convexity and boundedness of $\Omega$ (Zwanziger 1982; Dell'Antonio–Zwanziger 1989, 1991) and the Gribov-copy facts (van Baal 1992) were not credited. | Crossref | **Fixed** (Introduction, Prop. 4.2). |
| 24 | Bibliography metadata | Wrong or incomplete entries: Dudal et al. PRD 78 title; Vafa–Witten title and pages (535–538, correct 535–536); Singer 1978 pages (7–20, correct 7–12); Vandersickel–Zwanziger issue; Morningstar–Peardon title; Teper 1998 title. The "Beyond the Spectrum" volumes were cited for the Floer construction, the dual superconductor and $\mathrm{Ric}\ge0$; those claims are removed. | `check_dois_2026_09_25.out` (39/39 resolve) | **Fixed.** Self-citations reduced to the monograph and the $\Delta_4\times\Delta_2$ preprint. |
| 25 | Numerical table (12 "PASS" rows) | Named scripts (`verify_yang_mills_*.py`) are not in the folder. The rows tested the paper's formulas against themselves: for example, row 1 "$\mathrm{Ric}\ge2\gamma^2=K$" contradicted $K=2(1-c_0)\gamma^2$. | folder listing | **Removed.** Replaced by Table 1 of independent checks (`check_ym_claims_2026_09_25.py`). |
| 26 | Declarations | The AI statement ("strictly for language editing … exclusive intellectual creation") did not reflect actual use, as found in monograph finding F-21. Competing-interest, verification-status and availability statements were missing. | monograph `declarations_chapter.tex` | **Fixed.** Aligned with the monograph's declarations. **Author must confirm.** |
| 27 | Intro/abstract dimensional and label hygiene | Hard-coded "Hypothesis 2.1/5.1" and "Theorem 4.2"; "this monograph" used for a paper. | reading | **Fixed** (`\label`/`\ref`). |

Tally used in the counts above:
- Correct: 3, 4 (values), 11 (integrals), 17 (tight-binding), 18 (inequality), 20, 21, plus the Millennium-problem remark (now Remark 5.6) kept.
- Fixed: 1, 4, 5, 7, 8, 19, 22, 23, 24, 26, 27, plus three definitional fixes inside 6, 10 and 13 (spin-network labels, $\Lambda_{\rm mod}$, Hessian conventions).
- Demoted: 6, 12, 16, vacuum uniqueness (17), and the curvature hypothesis restated as Hyp. 5.3.
- Removed: 2, 7 (exact microcausality), 9, 10, 11 (formula for $\sigma$), 13 (theorem), 14, 15, 17 (Floer), 18 (strong CP / reflection positivity), 25. Counted as 10, since items 9 and 10 describe one removed theorem.

## Items left open

1. **Hypothesis 2.1** (existence of the ground-state measure) and **Hypothesis 5.3** (uniform $\mathrm{CD}(K,\infty)$ for regularized ground-state measures). Nothing in the paper supports either beyond the tree-level Prop. 4.4, and Remark 4.5 lists the obstacles.
2. **Wilson area law** (Conjecture 6.4), **vacuum uniqueness at fixed $\theta$**, and **Osterwalder–Schrader reflection positivity** of the GZ/RGZ measure for gauge-invariant observables.
3. **The ratio $\lambda/\Lambda_{\overline{\rm MS}}$** from the renormalized gap equation is not computed. It is scheme dependent.
4. **Second, independent check** of this correction pass (four-eyes rule of the monograph's WORKPLAN §8) has not been done.
5. **Lean folder `formal_proofs_yang_mills/`** has not been audited in this pass. The paper now states that it does not verify the paper's mathematics (same pattern as monograph findings F-01/F-24).
6. **Historical audit files in this folder** still claim "PASSED/FINAL/CERTIFIED": `AUDIT_CERTIFICATE.md`, `PROOF_AUDIT_YANG_MILLS_*.md`, `RELEASE_NOTES_v2.0.md`, `LEDGER_YANG_MILLS.md`, `CLAUDE_YANG_MILLS_AUDIT_REPORT.md`, `REFEREE_REPORT_*.md`, `proof_audit_report.tex`. They are not evidence and should be moved to an archive folder by the author (not done here, per the one-file edit scope).
7. **Source of the $\lambda_1=2.450$ claim** in `Pesquisa_e_Testes/research_master_universe_lagrangian/paper_master_universe_lagrangian.tex` (lines ~385, ~522). It has the same unsupported content as item 2. It is outside this paper and was not edited.
8. **"Beyond the Spectrum" volumes (Zenodo 22441676)**: the content they were cited for was not checked. The citations were dropped because the claims they supported are removed. The author should decide whether any of it is still needed.

## New one-sentence claim of the abstract

*If the ground-state measures of regularized Yang–Mills Hamiltonians on the Gribov region satisfy a uniform Bakry–Émery bound $\mathrm{CD}(K,\infty)$ and the Hamiltonians converge in the strong resolvent sense, then the continuum Hamiltonian has a gap of at least $g^2K/2$ above the vacuum; whether the Gribov–Zwanziger construction supplies such a bound is open, so no mass gap is established here.*
