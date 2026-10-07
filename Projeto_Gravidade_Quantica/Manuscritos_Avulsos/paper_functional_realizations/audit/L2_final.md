# Vol. I (Functional Realizations): final layer-2 check of Round 3

- **Checker:** independent Claude session (Opus), 2026-10-06. I wrote neither the volume, the audits nor the Round-3 corrections.
- **Inputs:**
  - `L2b.md`;
  - `fixes_layer1.md`, section "Round 3";
  - the current `.tex` and PDF;
  - `CORRECTIONS_2026-10-06.md` and `ZENODO_DESCRIPTION_VOL1.md`.
- **Scripts** (each writes an `.out.txt`):
  - `scripts/L2_final_checks.py`: 0 failures.
  - `scripts/L2_final_build.py`: output in `L2_build_paper_functional_realizations.out.txt`.
  - `scripts/L2_final_text_refs.py`: output in `L2_final_text_refs_paper_functional_realizations.out.txt`.
- **Processes:** no background jobs; `processos_orfaos.py` finds 0 suspects.

## Verdicts

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Abstract ¶2, items (i)–(iv) | **CONFIRMA** | Only (i) and (ii) are now called non-spectral. (iii) and (iv) are called permutation-invariant. "Explicit functions of the entries" is restricted to (i) and (ii).<br>Checked with `L2_final_checks.py`, $n=5$, fixed seed:<br>• **Dirichlet energy:** the Fourier sum, a torus quadrature of $\lvert\nabla f_A\rvert^2$ and $\lVert DA\rVert^2+\lVert AD\rVert^2$ agree. It changes under $A\mapsto PAP^T$ (396.45 vs 952.26) with an equal spectrum.<br>• **TV** changes (7.69 vs 10.49).<br>• **Morse indices** from the Riemannian Hessian are $[0,1,2,3,4]$ for both, and recover $\chi(S^4)=2$.<br>• **Cut distance:** the cut norm of $W_A-W_B^\psi$ is 0 after the explicit relabelling, against 0.0435 without it. Control: an orthogonally similar $C$ (same spectrum) has $\delta_\square\ge0.0367>0$.<br>The claim "factor $n^2$ for suitable rank-one matrices" matches Thm 4.1 ($E_{11}$ against $E_{nn}$). |
| 2 | Introduction, contributions 3–4 | **CONFIRMA** | Morse indices are "fixed by the order of the eigenvalues"; the cut distance is "invariant under relabelling". This is consistent with Thm 4.7(ii) and Thm 4.11. Contributions 1–2 are restricted to the permutation-sensitive quantities. |
| 3 | Conclusion | **CONFIRMA** | The "not determined by the spectrum" list now contains only smoothness, TV and level-curve perimeter. Morse indices and graphon limits are named as permutation-invariant readings. |
| 4 | §4 title "Emerging Invariants: Spatial, Topological and Asymptotic Quantities" and opening paragraph | **CONFIRMA** | The title no longer claims order-sensitivity. The opening paragraph is correct: §4.1–4.2 are permutation-sensitive, §4.3–4.4 permutation-invariant, and it gives the reasons. |
| 5 | §6.4 title "Computational Multilinear Algebra: Well-Posed Rank-One Approximation and the De Silva–Lim Pathology" | **CONFIRMA** | It no longer suggests that the pathology occurs at rank one. The body is unchanged and correct. |
| 6 | §6.5 display $\int\mathcal H^1(\partial^*\{W_A>t\}\cap(0,1)^2)\,dt$ | **CONFIRMA** | It matches Thm 4.6. The interior level-set perimeter integrated over $t$ equals the jump formula (7.6917 vs 7.6919 on a $t$-grid with 40 001 points; same for $PAP^T$). Negative control: without $\cap(0,1)^2$ the value on the window $[\min-1,\max+1]$ is 20.07. |
| 7 | `CORRECTIONS_2026-10-06.md` | **CONFIRMA** | It lists the final §4, §6.4 and §6.5 headings, the §4 opening paragraph, the §6.5 display, and the abstract/introduction/conclusion change, all matching the `.tex`. No GitHub, no "pending", no "layer 2 not done". "Volumes II and III: corrected separately in the same release" is accurate: Vol. III `L2_layer2.md` is done. |
| 8 | `ZENODO_DESCRIPTION_VOL1.md`, line 3 | **CONFIRMA** | Same split as the abstract. Dirichlet energy and TV change under relabelling; Morse indices and cut distance are permutation-invariant. No GitHub, no "pending". |
| 9 | Build (`audit/L2_build_final/`, pdflatex ×3) | **CONFIRMA** | Exit codes 0/0/0. 0 errors, 0 LaTeX/Package/Class warnings, 0 overfull, 0 underfull, 0 undefined. 21 pages. Three pre-existing pdfTeX notices, "font expansion: font should be expanded before its first use" (microtype + cm-super), which the gate accepts. pdftotext of the shipped PDF is identical to the fresh build. |
| 10 | House style, affiliation, DOIs (spot re-run) | **CONFIRMA** | The body contains none of the forbidden words or claims, and the affiliation is correct. All 19 DOIs resolve. Six metadata differences are benign:<br>• online-first years: Auffinger 2012/2013, Zhao 2014/2015;<br>• missing Crossref fields: Lim 2005 has no year, Adler–Taylor has no author;<br>• subtitle differences: Milnor, Vershynin. |

**Totals: 10 CONFIRMA, 0 PROBLEMA, 0 INCERTO.**

**Residual cosmetic note** (outside the Round-3 scope, already in `L2b.md`): the Verification-status paragraph says "No statement of this **paper**", while the AI paragraph says "**volume**". The longer Verification paragraph differs from the standard block by author decision, as `L2b.md` already confirmed.

**Close:** Vol. I is ready for the MAJOR version.
