# Round 5 Certification Audit — "Post-Spectral Graph Theory II"

## 1. Verification of Round 4 Remediations

**Finding #1 (Scoping of Theorem 2.1) — VERIFIED RESOLVED.**
The abstract now reads "for any fixed finite-dimensional invariant tuple drawn from bounded-order spectral moments, 1-dimensional persistent homology barcodes, and local subgraph counting statistics," and Theorem 2.1's hypothesis is symmetrically restated: "bounded-degree spectral moments $(\Tr(L^m))_{m=1}^k$, 1-dimensional persistent homology barcodes $\dgm_1$, and local subgraph counting profiles of order at most $k$." This scoping is now consistent throughout Sections 1–2 and no longer contradicts the cut-profile completeness of Theorem 3.1 (which uses a *different*, non-bounded-order invariant — the full $2^{n-1}-1$-dimensional cut spectrum). The logical arc (finite/local invariants incomplete → global cut profile complete) is now coherent.

**Finding #2 (Proposition 3.2(2) direct read-off) — VERIFIED RESOLVED.**
The closed-form identity $\CapOp(\{u_1\},\dots,\{u_r\}) = w(u_1,\dots,u_r)$ is now stated first and explicitly, followed by the column-rank argument (identity block embedded in $M_{\le r}$) and the regularized least-squares inversion formula. I independently re-checked the least-squares formula: with $M_{\le r}$ full column rank $\binom{n}{r}$, $w = 4G_{\mathrm{eff}}(M_{\le r}^T M_{\le r})^{-1}M_{\le r}^T \mathcal{S}_{\le r}$ is the correct normal-equations solution to $M_{\le r} w = 4G_{\mathrm{eff}}\mathcal{S}_{\le r}$. Correct.

**Finding #3 (private anchor vertices) — VERIFIED RESOLVED.**
The proof of Theorem 2.1 now explicitly states that each gadget edge is lifted to an $r$-uniform hyperedge via $r-2$ *dedicated, private* anchor vertices unique to that hyperedge. This closes the automorphism loophole: since anchors have degree 1 and belong to exactly one hyperedge, no automorphism of $H_1$ or $H_2$ can permute anchors across gadgets, so the parity-counting argument in the non-isomorphism proof goes through unchanged for $r\ge 3$.

## 2. Independent Re-Derivation Checks (Round 5)

I did not simply trust the Round 4 sign-off; I recomputed the load-bearing arithmetic independently:

- **Chen iterated integral (Thm 2.2/proof):** Recomputed $\mathcal{I}^{(2)}_{\mathrm{Chen}}(\omega_1,\omega_2;\Gamma)$ from the four-interval step-function representation directly (not from the paper's tallied contributions) and independently obtained $+1$; the reverse-order integral independently obtained $-1$; antisymmetric combination $=+2$. Matches the manuscript.
- **Reversal identity:** Independently derived $\mathcal{I}^{(2)}(\omega_1,\omega_2;\Gamma^{-1}) = \mathcal{I}^{(2)}(\omega_2,\omega_1;\Gamma)$ via the substitution $t_1=1-s_2,\,t_2=1-s_1$ on the reversed path's iterated integral — confirms $\Delta_{\mathrm{Chen}}=4$ is not a numerical coincidence but follows from a general reversal identity for Chen integrals.
- **Boolean graph inversion (Thm 3.1):** Re-derived $2w(i,j)=\CapOp(\partial\{i\})+\CapOp(\partial\{j\})-\CapOp(\partial\{i,j\})$ from first principles; algebraically exact.
- **Burnside cycle count (Thm 4.1(3)):** Independently derived $c(\tau)=\binom{n}{r}-\binom{n-2}{r-1}$ for a transposition via the Pascal-triangle split $\binom{n}{r}=\binom{n-2}{r}+2\binom{n-2}{r-1}+\binom{n-2}{r-2}$ — confirms the stated formula exactly.

All spot-checked computations are correct.

## 3. New Residual Observation (not previously flagged)

**Proposition 3.2, item (1)** asserts that "any linear combination of single-scale partition cuts from $(r-1)$-subsets $\sum_{I\subset e,|I|=r-1} S(\pi_I)$ produces a coefficient matrix of the form $rI + A_{J(n,r)}$." Two issues:

- The objects $\pi_I$ and $S(\pi_I)$ (the partition/cut associated to an $(r-1)$-subset) are never formally defined anywhere in the manuscript.
- No proof is given for this claim — it is asserted directly inside the proposition statement rather than derived in a `\begin{proof}` block. (The heuristic is plausible: each $r$-subset $e$ has $r$ distinct $(r-1)$-subsets, and each such subset is shared by exactly the Johnson-adjacent hyperedges, which would indeed generate $rI+A_{J(n,r)}$ — but this reasoning is nowhere written out.)

This is **not load-bearing**: the paper's actual reconstruction machinery (used later in Theorem 5.1 and Numerical Battery 2) is item (2)'s direct singleton read-off plus full-rank $M_{\le r}$, which is proven independently and correctly. Item (1) functions only as motivating context for *why* single-scale cuts alone fail. I flag it as a minor expository/rigor gap for a future revision (either supply the definition of $\pi_I$ and a short proof, or demote item (1) to a Remark), but it does not undermine the soundness of any theorem the paper depends on.

## 4. Disposition

- Findings #1, #2, #3 from Round 4: **fully and correctly implemented**, verified against the actual LaTeX source rather than the change description alone.
- All independently spot-checked derivations (Chen holonomy arithmetic, reversal identity, graph inversion algebra, Burnside cycle count) are **exact**.
- One new minor, non-load-bearing exposition gap identified in Proposition 3.2(1) (undefined notation, missing proof) — recommended for a future micro-revision but does not block certification, since no downstream theorem relies on it.

VERDICT: PASS