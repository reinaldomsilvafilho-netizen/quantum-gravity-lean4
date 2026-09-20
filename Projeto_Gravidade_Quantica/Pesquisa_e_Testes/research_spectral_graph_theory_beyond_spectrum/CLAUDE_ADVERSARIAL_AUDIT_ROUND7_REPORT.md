# ROUND 7 ADVERSARIAL AUDIT — Post-Spectral Graph Theory II

**Auditor posture:** I re-derived every claimed identity from its stated definitions rather than accepting the Round 6→7 remediation narrative at face value, and I diffed the Lean modules against the *current* LaTeX mathematics (not the Round 6 mathematics they were originally written against). Two of the ten "resolved" findings do not actually close, and I found one new critical defect that survived all prior rounds untouched.

---

## PART 1 — STATUS OF THE 10 ROUND-6 FINDINGS

| # | Claim | Verdict |
|---|---|---|
| 2 | Thm 3.1 reworded to labeled-space isomorphism / orbit-space permutation statement | **RESOLVED.** Statement and proof are now scoped correctly; no orbit-embedding overclaim remains. |
| 4 | Thm 6.3 non-circular induction via completeness | **RESOLVED** (mod a citation slip, see §3 below). Induction on shrinking $\mathcal M(u)$ using an independently-proved completeness result is sound and no longer bootstraps its own conclusion. |
| 5 | Prop 3.2 Johnson-scheme/Schur's-Lemma rank defect | **RESOLVED.** The Gelfand-pair decomposition $\mathbb R^{\binom nr}\cong\bigoplus_{j=0}^r V_j$ is standard, $M_k$ is genuinely $S_n$-equivariant (its indicator depends only on $|e\cap S|$, invariant under the diagonal action), and $S_n$ acts faithfully on $r$-subsets for $0<r<n$, so $\mathrm{Fix}$-type / Schur's-Lemma argument goes through cleanly. |
| 6 | Thm 4.1 measure-zero argument replacing Erdős–Rényi | **RESOLVED.** Faithfulness of the $S_n$-action on $r$-subsets $\Rightarrow$ every $\mathrm{Fix}(\sigma)$, $\sigma\neq\mathrm{id}$, is a proper subspace; finite union of proper subspaces is null; complement is open dense. Erdős–Rényi is now cited only in Thm 4.2 for discrete counting, correctly. |
| 7 | Rational $L^\dagger$, semialgebraic reach barrier | **RESOLVED.** $(L(W)+\tfrac1nJ)^{-1}$ is genuinely rational in $W$ via Cramer's rule on a PD matrix; hinge-squared terms are piecewise polynomial. Real-semialgebraicity claim is legitimate. |
| 8, 9 | Numbering / sign-convention cleanup | **RESOLVED.** Verified consistent throughout (Def 6.4/6.5/Thm 6.6 labels; $\pi(H_1){=}1\to\Phi{=}3$, $\pi(H_2){=}0\to\Phi{=}2$ is internally consistent). |
| 1 | Thm 3.3 replaces flawed inclusion–exclusion with direct $\mathrm{Cap}_r$ read-off | **PARTIALLY RESOLVED — see Finding A and Finding B below.** The LaTeX replacement is *correct* but *tautological* (Finding A), and the Lean suite still formalizes the **old, abandoned** inclusion–exclusion identity rather than the new one (Finding B) — this is a genuine non-closure. |
| 3 | Thm 2.2 canonical Chen normalization | **NOT FULLY RESOLVED — see Finding C.** Formal cochain machinery is now stated, but proof step (2) still *asserts* $\mathcal I_{\mathrm{Chen}}=\pm2$ by narrative ("the spanning 2-cell has trivial monodromy... accumulating $1-(-1)=+2$") rather than *computing* it from the double sum in eq. (2.5) on an actual $\Gamma=(e_1,\dots,e_L)$. This is the same VAC-04 gap under new notation. |
| 10 | Complete Lean bundle, 0 sorry / 0 axioms | **MISLEADING AS STATED — see Finding D.** "0 sorry, 0 axioms" is true but does not mean what Finding #10 implies. Three of four modules formalize *hypothesized* linear relations and trivially discharge them with `omega`; they verify no actual graph, hypergraph, or representation-theoretic content. |

---

## PART 2 — NEW / SURVIVING CRITICAL FINDINGS

### Finding A (CRITICAL — new): Theorem 3.1's boxed formula does not follow from its own proof

The proof correctly derives, directly from Definition (2.1) ($S(A):=\sum_{i\in A,j\notin A}w(i,j)$):
$$S(\{i\})+S(\{j\}) = 2w(i,j) + S(\{i,j\}) \;\Rightarrow\; 2w(i,j) = S(\{i\})+S(\{j\})-S(\{i,j\}).$$
This is airtight. But the theorem then states — and the very next sentence in the proof asserts it "gives" — the formula
$$w(i,j) = 2G_{\mathrm{eff}}\big[S(\{i\})+S(\{j\})-S(\{i,j\})\big].$$
Comparing: the derivation gives $w(i,j)=\tfrac12[\cdots]$; the boxed formula gives $w(i,j)=2G_{\mathrm{eff}}[\cdots]$. These agree **only if $G_{\mathrm{eff}}=1/4$**, a value never fixed anywhere in the paper ($G_{\mathrm{eff}}$ is introduced as a free "effective gravitational coupling"). Under no reading of Def. (2.1) — whether $S(A)$ denotes the raw weight-sum or the holographic area — does "recalling the normalization" licenses inserting a *multiplicative* $2G_{\mathrm{eff}}$ factor; I checked both readings and both are inconsistent with the boxed formula unless $G_{\mathrm{eff}}$ is silently pinned to $1/4$. This is a self-contradiction within a single proof paragraph in the paper's central completeness theorem, restated verbatim in the Abstract. It is either a copy-paste leftover from an earlier draft's normalization or an uncaught algebra slip — either way it must be fixed (state $G_{\mathrm{eff}}=1/4$ explicitly, or drop the factor and write $w(i,j)=\tfrac12[S(i)+S(j)-S(i,j)]$).

### Finding B (CRITICAL — new): Lean Module 1 formalizes the *abandoned* identity, not the Round-7 fix

Round 6 Finding #1 says the flawed inclusion–exclusion identity for $r\ge3$ was **eliminated** and replaced by the direct read-off $w(e)=\mathrm{Cap}_r(\{u_1\},\dots,\{u_r\})$. Yet `Volume2_BooleanInversion.lean` still contains:

```
structure Hyperedge3CutProfile where
  ...
  h_mobius : (c_u + c_v + c_w) - (c_uv + c_uw + c_vw) + c_uvw = 3 * w_uvw
```

This is precisely the old inclusion–exclusion Möbius-type formula the LaTeX explicitly discarded as unsound for $r\geq3$. `hyperedge_mobius_recovery` and `hyperedge_weight_injectivity` re-certify this dead identity as if it were current mathematics. The formal suite was **not updated** to reflect the surgical fix claimed in Finding #1 — it verifies a superseded, previously-rejected construction. This directly contradicts the audit payload's framing that the bundled Lean modules represent the Round-7 mathematics.

### Finding C (MEDIUM — new): The Thm 3.3 fix is correct but tautological, which weakens the "completeness" claim

$\mathrm{Cap}_r(\{u_1\},\dots,\{u_r\})$ is *defined* as the total weight of hyperedges hitting all $r$ singletons; for $r$-uniform hyperedges this uniquely picks out $e=\{u_1,\dots,u_r\}$ itself. So "$w(e) = \mathrm{Cap}_r(\dots)$" is very close to restating the definition of $\mathrm{Cap}_r$ rather than *inverting* an independent lower-order observation — unlike Thm 3.1's genuine inversion (recovering $w(i,j)$ from three *distinct* cut measurements $S(\{i\}), S(\{j\}), S(\{i,j\})$ none of which individually equals $w(i,j)$). The paper should be transparent that this is a definitional read-off, not a non-trivial reconstruction, or the "informational completeness" framing in the Abstract overstates the result for $r\ge3$.

### Finding D (HIGH — new/systemic): Lean Modules 1–3 assume their conclusions

Across `Volume2_BooleanInversion.lean`, `Volume2_ChenHolonomy.lean`, and `Volume2_DimensionBound.lean`, the pattern is: define a structure whose *field* is exactly the identity to be "proved" (`h_cut_uv`, `h_mobius`, `h_transcendence`, `h_pos`), then discharge the "theorem" with `omega` on that hypothesis. E.g. `chen_gap_strictly_positive` and `cfi_concrete_gap_four` never derive $\mathrm{val}=2$ from any cochain/walk data — it is asserted via `h2 : tp.val = 2`. `InvariantOrbitSpace` never derives $\mathrm{trdeg}=\binom nr$ from Artin's theorem — `h_transcendence` just posits it, and hardcodes $r=2$ only ($n(n-1)/2$), not the general-$r$ claim of Thm 4.1. None of these modules define an actual `SimpleGraph`/hypergraph, a cut-capacity function over `Finset`s, a Laplacian, or an $S_n$-representation. "0 sorry, 0 axioms" is therefore compiler-trivial and provides essentially no evidential weight toward the paper's mathematical claims. By contrast, `GraphNumberTheory.lean`'s `dyadic_val_injective` (real structural induction) and the Cartesian-product vertex-count lemmas are genuine, substantive, non-circular Lean proofs — this module should be held up as the standard the other three need to meet.

### Finding E (LOW): Cross-reference imprecision in Thm 6.3

The proof of Thm 6.3 (for $\mathcal F\subset \mathcal G_n/S_n$, i.e. ordinary graphs, $r=2$) cites Theorem 3.3 (`thm:hypergraph_inversion`, the general $r\ge3$ multiscale result) as its completeness input. The directly applicable statement is Theorem 3.1 (`thm:completeness`, $r=2$). Not fatal (Thm 3.3 does specialize correctly to $r=2$), but should be corrected for precision.

---

## PART 3 — REQUIRED REMEDIATION FOR ROUND 8

1. Fix the $G_{\mathrm{eff}}$ factor in Thm 3.1 (either pin $G_{\mathrm{eff}}=1/4$ explicitly and justify it, or correct the boxed formula to $\tfrac12[S(i)+S(j)-S(i,j)]$) — propagate the correction to the Abstract and to whatever code produced the Battery 2 numerics, and re-report that benchmark.
2. Delete or explicitly mark `Hyperedge3CutProfile`/`hyperedge_mobius_recovery`/`hyperedge_weight_injectivity` in `Volume2_BooleanInversion.lean` as superseded, and add a Lean module that actually formalizes the current $\mathrm{Cap}_r$ direct-readoff construction.
3. Either compute $\mathcal I_{\mathrm{Chen}}(\Gamma)=\pm2$ explicitly from eq. (2.5) on a concrete, fully specified $n=12$ CFI complex (edge sequence, $\gamma_a,\gamma_b$), or concede this remains a numerically-verified (not analytically-derived) claim.
4. Rewrite `Volume2_ChenHolonomy.lean` and `Volume2_DimensionBound.lean` to encode actual combinatorial/representation-theoretic objects rather than positing the conclusion as a structure field.
5. Add a sentence acknowledging the tautological nature of the $r\ge3$ $\mathrm{Cap}_r$ inversion (Finding C).
6. Fix the Thm 6.3 citation to Theorem 3.1.

---

`VERDICT: REVISE`