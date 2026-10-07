# Fix log — Open problem 1 (2026-10-07)

Independent corrector (did not write the volume or the flag). Flag source: `audit/references_audit.md`, "Findings for the author", item 1: "Open problem 1 looks trivially solvable. The text says it is 'a quadratic assignment problem'."

## Statement verified

Open problem 1 (old text, §7, "Optimal Realization Bounds"): for $A \in \R^{n\times n}$, find $\inf_{\pi\in\mathcal S_n}\mathcal E(f_{P_\pi A P_\pi^T}) = \min_\pi \sum_{i,j}(\pi(i)^2+\pi(j)^2)a_{ij}^2$, called there "a quadratic assignment problem" whose relaxations were asked about.

## Verification

Expanding the double sum: $\sum_{i,j}(\pi(i)^2+\pi(j)^2)a_{ij}^2 = \sum_i \pi(i)^2 w_i$, with $w_i=\sum_j(a_{ij}^2+a_{ji}^2)$ (derivation re-checked independently; matches the audit note exactly). Since $\{\pi(i)^2\}_i$ is always the fixed multiset $\{1^2,\dots,n^2\}$, this is a one-dimensional linear assignment, not a genuine QAP (no term couples $\pi(i)$ and $\pi(j)$ jointly). The rearrangement inequality gives the exact minimizer: pair the largest $w_i$ with the smallest square. Closed form: $\sum_k k^2 w_{\tau(k)}$ with $\tau$ sorting $w$ descending. Cost $O(n\log n)$.

**Label:** proved (Proposition, elementary — rearrangement inequality, a classical cited fact).

## Numerical check

`audit/scripts/verify_op1_sorting.py` (independent oracle: brute force over all $n!$ permutations via `itertools.permutations`, n = 1..8, 18 random Gaussian instances, fixed seed 20261007):
- Brute-force minimum matches the sort-formula value to $10^{-9}$ relative tolerance in every instance (18/18).
- Negative control 1 (mutated formula: pairs largest $w_i$ with the **largest** square instead of the smallest — the wrong rearrangement direction): fails to match the brute-force minimum in every non-degenerate instance ($n\ge2$; for $n=1$ there is only one permutation).
- Negative control 2: the best-scoring non-optimal permutation found by brute force is strictly worse than the sorted optimum in every instance.
- Degenerate case $n=1$ checked by hand and in code: only one permutation exists, trivially optimal.
- Output: `audit/scripts/verify_op1_sorting.out.txt` (`failures=0`). No background process left running; run was synchronous, well under the 10-minute limit (a few seconds).

## Text fix

Edited `paper_functional_realizations.tex` with the Edit tool (no shell heredocs):
1. Added **Proposition (Optimal permutation for the Dirichlet energy)**, `\label{prop:optimal_permutation}`, with proof, in §4.1 (Spatiality vs. Spectrum), right after the "ratio is 1" remark and before the checkerboard example.
2. Added **Remark (This is not a genuine quadratic assignment problem)**, `\label{rem:not_qap}`, explaining the separable-coefficient reason the resemblance to a QAP is only superficial.
3. Removed open problem 1 from the enumerated open-problems list in §7 (Conclusion and Open Problems); replaced by one sentence stating it is resolved, pointing to the Proposition and Remark. Remaining open problems renumber automatically (LaTeX `enumerate`).
4. Updated the Conclusion's sentence listing proved results to include "optimal-permutation".
5. Updated Table 1, row 1 ($A\in\R^{n\times n}$, Dirichlet energy), to note the optimal permutation is solved by sorting, citing the Proposition.

Checked and found no other mention of "quadratic assignment" / "Optimal Realization Bounds" in the abstract, introduction, or elsewhere (`grep` over the full `.tex`; only the §4.1 and §7 occurrences existed before this fix).

## Build

Compiled 3× with `pdflatex -interaction=nonstopmode` (no `.bib`/`.bbl`; bibliography is an inline `thebibliography`). Final pass: 0 errors, 0 LaTeX warnings, 0 overfull/underfull boxes, 0 undefined references. The 4 pdfTeX "font expansion" notices are pre-existing (microtype/cm-super), unchanged from before this fix. Page count 24 -> 25 (new Proposition/proof/Remark content). `.aux`/`.out`/`.toc` deleted after the final pass.

## Backup

Pre-edit copy saved to `_arquivo/backup_tex_2026-10-07/Manuscritos_Avulsos/paper_functional_realizations/paper_functional_realizations_op1.tex`; `origin	backup` appended to `_arquivo/backup_tex_2026-10-07/MANIFESTO.tsv`.

## Four-eyes note

This fix was made by a session that did not write the original volume or the flag. It still needs the next-reader re-check (layer 2) per the project's four-eyes rule, since the corrector (this session) must not be the one who verifies its own correction.
