# Version note: *Beyond the Spectrum III*, v3 (new major version), 2026-10-06

- **Concept DOI:** 10.5281/zenodo.22644743.
- **Previous version (v2):** record 22866175, trilogy pages 49–59. Its text is identical to record 22699282's `volume_3_higher_invariants.pdf`.
- **v3:** `paper_beyond_the_spectrum_3.tex` / `.pdf`, 16 pages.
- **Build:** compiled 3 times with pdflatex: 0 errors, 0 LaTeX/package/class warnings, 0 overfull or underfull boxes, 0 undefined references. The log keeps one pdfTeX notice, "font expansion: font should be expanded before its first use". It is raised by microtype when the end-of-document address block is typeset. v2 has three of them, and Vols. I and II have them as well. I could not remove it without turning off font expansion, which creates overfull boxes.
- **Audit trail:**
  - `audit/blind_layer1.md`: blind review;
  - `audit/fixes_layer1.md`: corrections, item by item;
  - `audit/scripts/f1_corrector_checks.py` and `c2_resolve_new_dois.py`: the corrector's checks, each with an `.out.txt` file. Both exit 0.

## Why a major version

Five results of v2 are false: OBL-006, 008, 012, 014 and 018. One is a physical proposal labelled as a theorem (OBL-016), and one is ill-posed (OBL-003). The Lean claim is also false. v3 does one of three things with each of these items:

- replaces it with a correct statement and a complete proof;
- turns it into a remark with a counterexample;
- relabels it.

The abstract and introduction were rewritten to claim only what the body proves. The paper has no conclusion section.

## Changes from v2, item by item

1. **Abstract and introduction.**
   - Removed claims that had no support in the body:
     - "generalized" EH capacities $c_k$;
     - "sharp" Lipschitz stability;
     - the Cheeger limit;
     - "thermodynamic length lower-bounds $\mathcal W_2$";
     - "proving $S_R\ge2E_W$";
     - the "Barnes–Kigami residue spectrum";
     - the "verified" fractal dimension;
     - "machine-checked Lean 4";
     - "synchronized 1:1 with Lean".
   - The abstract now lists only results proved in the body or cited classical results, plus the three counterexamples.
   - $\mathcal S^n_+$ is defined once, as the positive semi-definite cone.
2. **OBL-001.**
   - The proof is now complete and elementary:
     - a first-exit argument gives $B(x_0,r_{\min})\subseteq K_t$;
     - convexity gives $K_t\subseteq\bar B(x_0,R_{\max})$;
     - monotonicity, translation invariance and $c_1^{EH}(B(r))=\pi r^2$ finish the argument.
   - The irrelevant Clarke-functional paragraph and the word "ellipsoid" were removed.
   - A new remark shows that the bound is not sharp for quadratic $\Phi$. In that case the capacity is set by the largest symplectic eigenvalue.
3. **OBL-002.**
   - Now stated as a cited classical result.
   - Adds the hypothesis $\Phi\in C^\infty$, since Hofer–Zehnder is stated for smooth boundaries.
4. **OBL-003.**
   - The ill-posed "Theorem" (Floer–Viterbo Lipschitz bound in $L^\infty(K)$) is now a remark.
   - The remark lists what a correct statement would need: a class of Hamiltonians, a homology class, and a global norm.
   - It says that the localization to $K$ is not proved.
   - The Viterbo 1992 citation was removed, since that paper does not cover this setting.
5. **OBL-004.**
   - "Mather's condition $(a_f)$" is replaced by plain transversality to each rank stratum.
   - The proof now shows why the rank strata are Whitney: there are finitely many congruence orbits, Whitney's genericity theorem applies, and the action is transitive on each orbit. It also gives the codimension.
   - Cites Gibson–Wirthmüller–du Plessis–Looijenga (LNM 552).
   - The duplicate tag on the definition was removed.
6. **OBL-005.**
   - Added the real-analytic hypotheses that Kashiwara–Schapira require.
   - The ill-defined "vanishing-cycle complex of $\det\Phi$" is replaced by any complex that is locally constant on the strata.
   - Corrected the proof: involutivity gives only coisotropy, and isotropy comes from the inclusion in the conormals.
7. **OBL-006.**
   - Kept Kashiwara's index formula, with its hypotheses: real-analytic, $\mathbb R$-constructible, compact.
   - The false formula $\chi=\sum m_r\chi(\Sigma_r)$ is replaced by the correct, proved formula $\chi=\sum\chi_c(\Sigma_r)\chi(\text{stalk})$.
   - Remark 3.5 gives the $S^1$ counterexample: 2 instead of 0.
8. **OBL-007 Lemma.**
   - Now claims only what is proved: existence of a non-negative minimizer and $\lambda>0$, with a complete proof.
   - Simplicity, positivity and $C^{1,\alpha}$ regularity are no longer claimed. The old simplicity argument (strict convexity of $|\nabla v|^p$) was invalid.
   - A remark cites Lindqvist 1990 for the unweighted case.
9. **OBL-008.**
   - The false statement $\lim_{p\to\infty}\lambda_p^{1/p}=h(A)$ is replaced by the correct one, $\lim_{p\to\infty}\lambda_p^{1/p}=1/R_\Omega$ (inradius). This holds for every weight bounded above and below.
   - The proof is complete: the weight is reduced to $\Phi\equiv1$ by comparison, the upper bound comes from the distance function, and the lower bound from a compactness argument. The argument follows Juutinen–Lindqvist–Manfredi (1999) as presented in Lindqvist's lecture notes.
   - Remark 4.5:
     - the unit disk gives the limit 1, while $h=2$;
     - the relative perimeter gives $h=0$;
     - Kawohl–Fridman is about $p\to1$ and the unweighted case (abstract read on the journal page).
10. **OBL-009.**
    - Removed "stability" from the title.
    - Corrected "inscribed radius" to "slimness constant of the ideal triangle": $\ln(1+\sqrt2)$, while the inradius is $\tfrac12\ln3$.
    - Notes that the conformal form plays no role.
11. **OBL-010.**
    - The domain is now $\mathbb R^d$; on a bounded domain the SDE exits and the claim was ill-posed.
    - Units are now stated: $k_BT=D=1$.
    - The $\mathcal W_2$ contraction is proved by synchronous coupling. Uniqueness is claimed among laws with finite second moment.
    - A remark notes that LSI ⇒ Talagrand does not by itself give the contraction.
12. **OBL-011.** Crooks' fluctuation theorem is now credited to Crooks 1999, not Jarzynski 1997. The protocol and the initial law are stated.
13. **OBL-012.**
    - The false "Theorem" $\lim\tau\Sigma=\tfrac12\mathcal L^2\ge\tfrac\kappa4\mathcal W_2^2$ is now Remark 5.4. It contains:
      - the slow-driving limit $\mathcal L^2$ (linear response, Sivak–Crooks), labelled as not proved here;
      - the dimensional inconsistency of a $\kappa\mathcal W_2^2$ bound;
      - the dragged-trap counterexample with closed form: $\tau\Sigma\to a^2$, while $\kappa=10$ requires $2.5a^2$;
      - the consistent statement of Aurell et al. 2011, minimal dissipation $=k_BT\mathcal W_2^2/(D\tau)$, checked in their arXiv text, eq. (23).
14. **OBL-013.** $\{\psi_k\}$ is now called an orthonormal family, and $\mathcal S^n_+$ is defined. No other change.
15. **OBL-014.**
    - The "Theorem" is now Proposition 6.2, with four proved parts:
      1. $\rho$ is positive semi-definite, trace class, with $\mathrm{Tr}=\mathrm{Tr}A$;
      2. $\operatorname{rank}\rho\le\sum_k m_k$ (Schmidt ranks), so $\le n$ for product frames;
      3. the *normalized* modular Hamiltonian is non-negative, and strictly positive iff the rank is $\ge2$;
      4. the regularized statement, with explicit hypotheses: compact $\Omega_i$, continuous kernels, $T_{k_1}$ injective.
    - Remark 6.3 gives the Mehler counterexample (infinite rank for $n=1$) and the unnormalized counterexample $-\log5<0$.
16. **OBL-015.**
    - Added the finite-rank hypothesis, so the spaces are finite-dimensional.
    - The proof now cites the exact equations (2.12)–(2.14) of Dutta–Faulkner, checked in their arXiv text.
17. **OBL-016.**
    - The "Theorem" is now Remark 6.5, a physical proposal: $S_R=2E_W$ at leading order in $G_N$ (Dutta–Faulkner).
    - It states that no bulk geometry is built from $K_A$.
    - Corrected the form of the relation (equality at leading order, not an inequality), and added a units sentence.
18. **Extra §7 paragraphs** (in the local `.tex` only, not in v2): **removed.** See `audit/fixes_layer1.md`, T-7a.
19. **OBL-017.** "Holomorphic for $\mathrm{Re}\,s>-\min\alpha_i$" is replaced by "**entire**", with a complete proof by uniform bounds and Morera's theorem.
20. **OBL-018.**
    - The false "Theorem" (meromorphic continuation with poles at $-\alpha_j-k$) is now Remark 7.2: $\mathcal Z_A$ has no poles, and $\Phi\equiv c$ gives $c^s$.
    - The poles belong to the Mellin transform of a vertex coordinate. New Proposition 7.3 computes it exactly, with residues and the integer cancellation case, and proves it.
21. **OBL-019.** **Removed.**
    - It was a classical result (the spectral dimension of the Sierpinski gasket) presented as a corollary of the false OBL-018, and it is unrelated to $\mathcal Z_A$.
    - I could not read the primary source (Kigami–Lapidus 1993) to check the attribution.
22. **OBL-020.**
    - Added the hypotheses that $\Sigma_t$ is compact and that $\Phi\in C^\infty$, as required by the cited dichotomy.
    - The proof now uses Federer's Thm 4.18 for positivity of the reach and Aamari et al. 2019, Thm 3.4 (local/bottleneck dichotomy), and shows that bottleneck pairs have opposite normals.
    - Proved that $d_{\rm sep}>0$.
    - Removed the false "$d_{\rm sep}=\infty$ for strictly convex".
    - Remark 8.2 adds:
      - the non-compact counterexample;
      - the ellipse, where $d_{\rm sep}=2$ and the bound equals the reach, 1/2.
23. **OBL-021.**
    - States the hypotheses and defines $H_j$ (unnormalized) and the medial axis.
    - The proof now carries out the change of variables. It uses Federer Thm 4.8 for the projection and Aamari Prop. A.1 for $|\kappa_i|\le1/R_t$.
24. **Table 1.** Restricted to this volume's invariants. The unjustified "symmetry group" column was removed. Codomains corrected: $CC$ is a Lagrangian cycle; $\mathcal Z_A$ is an entire function.
25. **Bibliography.**
    - Removed:
      - the three uncited self-references, one of which (Vol. II) carried the cobordism DOI;
      - Viterbo 1992;
      - Kigami 2001.
    - Added a citation of the trilogy record (DataCite title checked).
    - Added Crooks 1999, Lindqvist 1990, Gibson et al. 1976 and Aamari et al. 2019. Crossref title, authors and year were checked; see `c2_resolve_new_dois.out.txt`.
    - Renamed the key Aurell2012 → Aurell2011.
26. **Front matter.**
    - New affiliation line.
    - Standard declarations block.
    - `\date{}`: a fixed date avoids a first-page overfull box.
    - Section titles no longer advertise removed content ("Higher Categorical Frontier", "Floer", "Holographic Entanglement Duals", "Barnes–Kigami").

## What still needs work

The corrections above were re-checked on 2026-10-06 by a session that wrote neither the paper nor the corrections. Still open:

- **Theorem numbers in Kashiwara–Schapira Ch. IX** (9.5.6) were not checked against the book; Ch. VI (6.5.4) and Ch. VIII (8.4.1, 8.4.2) are now confirmed through secondary sources. **Federer 1959** Thm 4.8 and 4.18 are now checked in the full text.
- **Gibson et al. 1976.** The transverse-pullback and genericity statements are cited without a chapter number. I did not read the book.
- **Juutinen–Lindqvist–Manfredi 1999.** I could not open the paper (paywall). The limit $1/R$ and the proof I wrote follow Lindqvist's lecture notes (*A nonlinear eigenvalue problem*, Lemma 11) and Champion–De Pascale–Jimenez (arXiv:0811.1934), who attribute it to JLM.
- **OBL-014(4).** The hypothesis "$T_{k_1}$ injective" must be checked for any concrete kernel (for example, Gaussian kernels on compact sets).
- **OBL-020.** The $C^2$ version (instead of $C^\infty$) is expected but not proved here.
- **OBL-003.** The Floer-theoretic statement is open as formulated.
- **Weighted simplicity of the $p$-ground state.** Not proved.
- **References (2026-10-07 audit):** the bibliography grows from 19 to 72 items, and every one was resolved; see `audit/references_audit.md` and `audit/scripts/refs_resolve.py`. A related-work paragraph was added and citations were placed at the claims. Two wrong ISBNs were fixed (Gromov 1987; Bridson–Haefliger). Federer 4.8/4.18 were checked in the full text, and KS Thm 6.5.4, Prop. 8.4.1 and Thm 8.4.2 through secondary sources. "Monotonicity" in the title of OBL-015, and the sign convention in OBL-006, were flagged for an independent check and are now confirmed (`audit/L2_release.md`).
- **Pre-release fixes (2026-10-07, independent corrector):** the Declarations no longer mention earlier versions; they now say that the Lean 4 files in the author's repository associated with this work are a placeholder skeleton without Mathlib and verify none of the statements. See `audit/fixes_prerelease.md`.
- **Pre-release fixes (2026-10-07):** OBL-015 is retitled "Canonical Purification, Symmetry and the Mutual-Information Bound for the Reflected Entropy", and the statement now notes that monotonicity under partial trace fails (Hayden–Lemm–Sorce 2023, Thm 1, read in the arXiv full text).
- **Pre-release fixes (2026-10-07):** OBL-006 now states Kashiwara's index formula with his sign, χ = (−1)^{m(m+1)/2} CC·[T*_ΩΩ] with m = dim Ω, the orientation (dθ)^m and the conventions of Kashiwara 1985 §§2–3, citing Thm 4.2 there (read in the Numdam full text) with φ = 0; a consistency check for the constant sheaf is included.
- **Pre-release fixes (2026-10-07):** the Declarations now say that the three references without a DOI were resolved through Numdam, EuDML or the ISBN record.
