# Round 9 Adversarial Audit Report — "Post-Spectral Graph Theory II"

## 1. Verification of the Four Claimed Round 8 Remediations

**Remediation 1 (`Volume2_BooleanInversion.lean`) — VERIFIED CORRECT.**
`hits_all target e := target.all (fun u => e.contains u)` correctly encodes $\prod_j \mathbb{I}(u_j\in e')$ (target $\subseteq$ e). `cap_r` correctly sums weights via `filter`+`foldl`. I hand-checked `filter_isolates_target` and `cap_r_evaluates_exactly_to_target` against `sample_edges`/`sample_w`: only `[0,1,2]` contains all of `{0,1,2}`, so the filter and `rfl` reduction are legitimate (no vacuous predicate, no hidden default-case escape). `filter_collapse`/`cap_r_collapse` are a correctly structured induction (`List.Mem.head`/`tail` case split, no `sorry`). This closes the Round 8 finding about the fabricated `other_intersecting_edges_sum = 0` field — the new code computes the filter, it does not assert its output.

**Remediation 2 (`Volume2_DimensionBound.lean`) — ARITHMETIC VERIFIED, BUT SEE §2 below.**
I independently expanded `double_fix_dim k + double_defect_dim k`: $k^2+3k+4 + 2k+2 = k^2+5k+6 = (k+3)(k+2) =$ `double_ambient_dim k`. ✓. Converting to non-doubled, un-parametrized form and substituting $n=k+3$ reproduces exactly the LaTeX claim $\dim\mathrm{Fix}(\tau)=\binom{n}{2}-(n-2)$ for $n=4$ (4) and $n=5$ (7), matching both the `order4_*`/`order5_*` Lean benchmarks and the hand computation in the paper. `edge_02_is_moved_by_transposition`/`edge_02_not_fixed` are valid concrete witnesses. **However**, this module — like the LaTeX proof it backs — only ever formalizes the **transposition, $r=2$ case**. See finding below; this is not new to Round 9, but it is not resolved by it either.

**Remediation 3 (LaTeX typos) — the "21 cuts" and Theorem 3.1/3.3 cross-reference content is present.** I recomputed the theorem-numbering (theorem/lemma/proposition/corollary/definition/remark share one counter per section, per the `\newtheorem{...}[theorem]{...}` preamble). Section 3 order is: Thm 3.1 (`completeness`), Prop 3.2 (`single_scale_defect`), Thm 3.3 (`hypergraph_inversion`) — so "Theorem 3.1 (graphs) and Theorem 3.3 (hypergraphs)" is numerically correct. **Note:** the changelog's own pointer ("Section 5.2, Theorem 5.3") is wrong — that proof text actually lives in §6.2 as Theorem 6.3 (`graph_number_bijection`); Section 5 has only one theorem (5.1). This is a bookkeeping slip in the *changelog*, not in the manuscript body itself (which uses `\ref`), so it's cosmetic, not a manuscript defect.

**Remediation 4 (Lean suite compiles, 0 sorry/axioms)** — consistent with what's shown; no `sorry`, no `axiom`, no `Classical.choice`-style admits, and no vacuously-true implications spotted in any of the four modules (checked each hypothesis is actually dischargeable and used).

## 2. New Finding: Generality Gap in Theorem 4.1 (`dimension_bound`), Part 2

This is the substantive issue an adversarial pass must flag. Theorem 4.1 claims, **for general $r$-uniform hypergraphs and general $n$**, that $\dim_\mathbb{R}(\mathcal M_{n,r}) = \binom{n}{r}$, which requires $\mathcal S_{\mathrm{sym}}=\bigcup_{\sigma\neq \mathrm{id}}\mathrm{Fix}(\sigma)$ to be measure zero — i.e., $\mathrm{Fix}(\sigma)\subsetneq \mathcal H_{n,r}$ for **every** non-identity $\sigma\in S_n$ and **every** $r$.

The proof, however, only computes this **for a transposition $\tau=(ij)$ in the graph case $r=2$**, then states "Thus, $\mathrm{Fix}(\sigma)$ is a proper linear subspace... for all $n\ge 3$" — jumping from a single computed case to the fully general claim without justification. The companion Lean module (`Volume2_DimensionBound.lean`) mirrors exactly this restriction: `double_fix_dim`/`double_defect_dim`/`double_ambient_dim` are all parametrized only by $k$ with ambient dimension $(k+3)(k+2) = 2\binom{n}{2}$ — i.e., strictly the $r=2$ edge space. Nothing in the formal suite touches $r\ge3$ or non-transposition $\sigma$ (3-cycles, products of disjoint transpositions, etc.).

The same pattern recurs in Theorem 4.2's proof: the bound $\sum_{\sigma\neq\mathrm{id}}2^{c_r(\sigma)}\le n^2 2^{\binom{n}{r}-n+2}$ is justified by computing $c_2(\tau)=\binom{n}{2}-(n-2)$ for a transposition at $r=2$, then asserted for general $r,\sigma$ via a citation to Babai/Erdős–Rényi without an explicit general-$r$, general-$\sigma$ derivation.

**This gap is real but easily closable**: the general claim is true and provable by a one-line orbit-counting argument (any $\sigma\neq\mathrm{id}$ moves some point of $[n]$, hence moves some $r$-subset whenever $n>r$, so $\sigma$ has at least one non-trivial orbit on $\binom{[n]}{r}$, forcing $\#\text{orbits} <\binom{n}{r}$, i.e. $\dim\mathrm{Fix}(\sigma)<\binom{n}{r}$ strictly) — which is actually *simpler* than the transposition-specific eigenspace computation currently given. The paper should either (a) replace/supplement the transposition-specific argument with this general orbit-counting lemma, applicable to all $\sigma\ne\mathrm{id}$ and all $r$, or (b) explicitly restrict Theorem 4.1's dimension claim to $r=2$ if that's genuinely all that's formalized. As written, the theorem statement's generality ($r$-uniform, general $\sigma$) outruns its proof's generality (transposition, $r=2$).

## 3. Minor Finding: Missing Hypothesis in Proposition 3.2

The Johnson-scheme decomposition $\mathbb{R}^{\binom{n}{r}}\cong\bigoplus_{j=0}^r V_j$ used in Proposition 3.2 (`single_scale_defect`) is only valid as stated (indexed up to $j=r$, with $V_r$ being the "top" module) when $n\ge 2r$; for $n<2r$ the decomposition truncates at $j=n-r<r$. Theorem 3.3 explicitly states "$n\ge 2r$" but Proposition 3.2 does not. Per the repo's own Strict Rigor Rule item 1 ("hypothesis discharge for every theorem/lemma application"), Proposition 3.2 should carry this hypothesis explicitly.

## 4. Confirmed-Sound Items (no issues found)

- Theorem 3.1 algebraic inversion, its Lean mirror `boolean_edge_recovery_algebra`/`edge_weight_unique`/`edge_weight_pos_of_strict_submodular` — correct, non-vacuous, `omega`-closeable.
- Chen holonomy numerics: I independently recomputed `chen_iterated_anti` on both `commutator_walk` and `twisted_commutator_walk` term-by-term; both match the paper's hand computation exactly (+2 / −2, gap 4). Function definition structurally matches the stated $\sum_{i<j}$ formula.
- Cartesian-product/prime-graph module: `IsPrime`, `mul_ge_two_gt`, `prime_order_is_cartesian_prime` are correct and non-vacuous (the `CartesianProduct` structure's `≥2` fields make the falsity derivation meaningful, not a vacuous-hypothesis trick).
- $c_r(\tau)=\binom{n-2}{r}+\binom{n-2}{r-2}+\binom{n-2}{r-1}=\binom{n}{r}-\binom{n-2}{r-1}$ — I verified this via Pascal/Vandermonde decomposition of $\binom{n}{r}$ by intersection-with-$\{i,j\}$ count; correct.
- OEIS graph counts (4, 11, 34 for $n=3,4,5$) match A000088.

## Verdict

The four specific Round 8 remediations are genuinely and correctly implemented — this is real progress, not cosmetic. But the audit surfaces one substantive, previously-unflagged proof-completeness gap (Theorem 4.1's generality) and one missing-hypothesis issue (Proposition 3.2), both straightforward to fix but currently unaddressed in the manuscript and unmirrored (indeed, reproduced) in the Lean suite.

**VERDICT: REVISE**

Required for Round 10: (1) extend Theorem 4.1's proper-subspace argument from "transposition, $r=2$" to a general orbit-counting lemma covering all $\sigma\neq\mathrm{id}$ and all $r$ (and correspondingly generalize the Lean dimension-bound module beyond the $r=2$ edge space, or explicitly narrow the theorem's stated scope to match its proof); (2) add the $n\ge 2r$ hypothesis to Proposition 3.2; (3) correct the changelog's internal cross-reference ("Section 5.2, Theorem 5.3" → "Section 6.2, Theorem 6.3") for consistency, though this is cosmetic only.