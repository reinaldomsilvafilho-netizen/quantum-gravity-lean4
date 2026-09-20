# Adversarial Audit Report — Round 6
## "Post-Spectral Graph Theory II: Informational Completeness, Chen Iterated Holonomies, and Inverse Geometric Synthesis of Hypergraphs"

I worked through every new theorem in Sections 6–7 plus a re-verification pass on Sections 2–5 (since the request asks whether Theorems 2.1, 2.2, 3.1, 3.3, 4.1, 4.2, 5.1 and Prop. 3.2 remain airtight). Below are the defects found, ranked by severity, each checked by direct symbolic computation where possible rather than by reading the prose alone.

---

### CRITICAL — INV-01: The core identity in the proof of Theorem 3.3 is false

The proof of Theorem 3.3 (Multiscale Invertibility) rests on the claimed inclusion–exclusion identity:
$$\mathbb{I}(e=e') = \sum_{S\subseteq e}(-1)^{r-|S|}\,\mathbb{I}(S\subseteq e').$$

Test the identity at $e'=e$ (the case that matters most). Since $S\subseteq e$ and $S\subseteq e'=e$ are the same condition, the RHS reduces to $\sum_{S\subseteq e}(-1)^{r-|S|} = (-1)^r\sum_{S\subseteq e}(-1)^{|S|} = (-1)^r\cdot\mathbb{I}(e=\emptyset) = 0$ (since $|e|=r\ge1$, $e\ne\emptyset$). But the LHS is $\mathbb{I}(e=e)=1$. So the identity asserts $0=1$ for **every** hyperedge — it is false unconditionally, not just in an edge case.

The correct identity (derivable the same way) is
$$\sum_{S\subseteq e}(-1)^{r-|S|}\mathbb{I}(S\subseteq e') = (-1)^r\,\mathbb{I}(e\cap e'=\emptyset),$$
which is a statement about *disjointness*, not equality. This is not what the proof needs.

Consequently the claim "$\ker(M_{\le r})=\{0\}$" is **not established** by the argument given. The theorem's conclusion (full column rank of the stacked multiscale cut matrix) may still be true — this is a plausible fact provable via genuine Möbius inversion on the subset lattice or via the eigenvalue decomposition of the Johnson scheme referenced in Prop. 3.2 — but as written, the proof is invalid and must be redone.

---

### CRITICAL — INV-01: Theorem 3.1's quotient-space claim is a category error

Theorem 3.1 is proved correctly as an algebraic identity on **labeled** graphs: $2w(i,j) = S(\{i\})+S(\{j\})-S(\{i,j\})$ — I re-derived this independently and it checks out.

But the theorem (and the abstract) then claims $\mathcal{S}_2$ "is strictly injective on the graph orbit space $\mathcal{H}_{n,2}/S_n$," and calls this a "strict topological embedding on the graph orbit space." This is not a minor wording slip — $\mathcal{S}_2(w)$ is indexed by vertex labels $i,j$, and it is **not** $S_n$-equivariant in the way needed to descend to a function on the quotient ($\mathcal{S}_2(\sigma\cdot w)$ permutes the coordinates of $\mathcal{S}_2(w)$ rather than fixing them). A map that is not constant on orbits does not factor through the quotient at all, so "injective on $\mathcal{H}_{n,2}/S_n$" is meaningless as stated. What is actually proved is injectivity on the **labeled** space $\mathcal{H}_{n,2}\cong\mathbb{R}^{\binom{n}{2}}$. This overclaim propagates verbatim into the abstract.

---

### CRITICAL — VAC-04 / GAP-02: Theorem 2.2 (Chen holonomy) presents a normalization-dependent number as an exact universal constant

Theorem 2.2 asserts $\mathcal{I}_{\mathrm{Chen}}(H_1)=+2.0000$ and $\mathcal{I}_{\mathrm{Chen}}(H_2)=-2.0000$ *exactly*, for a general statement about "a pair of cospectral, co-walk-regular CFI hypergraphs on $n=12$." But $\omega_1,\omega_2$ are harmonic 1-forms "dual to independent generating cycles" — no normalization (inner product, scaling, sign/orientation convention) is fixed. The Chen iterated integral $\int\omega_1\omega_2-\int\omega_2\omega_1$ scales quadratically under $\omega_i \mapsto c\,\omega_i$ and flips sign under $a\leftrightarrow b$ or orientation reversal. Without a canonical normalization, "$+2.0000$" is not a mathematical constant — it is an artifact of one particular (unspecified) implementation choice. The "proof" ("the lift bounds an unoriented surface of signature $+2$... conjugating the holonomy to $-2$") is narrative, not derivation: "signature" is invoked without defining a quadratic/intersection form, and no computation shows why the magnitude must be exactly 2 rather than some other nonzero value.

The qualitative point (a Chen-type invariant can break the CFI degeneracy because it detects non-abelian/second-order holonomy invisible to Abelian circulations) is directionally plausible and mirrors known facts about CFI's cohomological character. But the theorem as stated overclaims a specific, unnormalized numeral as an exact universal separation constant. This defect is inherited by Section 6, since $\Omega_{\mathrm{Chen}}$ is then used as a *predicate* in the Adaptive Invariant Sieve (Def. 6.1) — a predicate whose sign is convention-dependent cannot serve as a well-defined graph invariant.

---

### HIGH — CIRC-05: Theorem 6.3's proof is circular

The proof of Theorem 6.3 (Bijective Arithmetization) states: "Since the sieve terminates with singleton leaves $|\mathcal{M}(u)|=1$ for all non-isomorphic classes, $\Phi$ is strictly injective." But *whether the sieve always terminates in singleton leaves for every $n$* is precisely the open completeness question the paper is trying to resolve (it is the generalization of the Incompleteness Theorem 2.1 to an adaptive, unboundedly-extended invariant pool). The proof assumes its own success condition as a premise. Section 7's benchmarks only check $n\in\{3,4,5\}$ — this is evidence for small cases, not a proof of the general claim "$\Phi(G_1)=\Phi(G_2)\iff G_1\cong G_2$" asserted for all $n$.

Combined with the sign-ambiguity of $\Omega_{\mathrm{Chen}}$ above, it is not even clear the sieve's predicates are well-defined functions on isomorphism classes $\mathcal{M}(u)$ in general, which the tree structure (Def. 6.1) requires.

---

### MEDIUM — GAP-02: Proposition 3.2's illustrative example is a non-sequitur

The proof states: "when $n=6, r=3, k=1$, the matrix $M_1\in\mathbb{R}^{6\times20}$ has rank at most 6." This is true, but it is true *trivially* because $M_1$ only has 6 rows (rank ≤ min(rows,cols) always) — it has nothing to do with the Johnson-scheme eigenvalue $\lambda_r=-r$ argument being illustrated, and does not exhibit the claimed "parity balance condition" $\sum_j(-1)^j\binom{r}{j}\binom{n-r}{k-j}=0$ (which is asserted but never derived from the association-scheme decomposition). The general claim (single-scale cuts have rank defect for $r\ge3$) is plausible and connects to real literature on inclusion matrices, but the specific derivation given does not support it.

---

### MEDIUM — NOT-07: Citation misapplied (Erdős–Rényi, Theorem 4.1)

Theorem 4.1's dimension argument invokes "the Erdős–Rényi theorem on asymmetric graphs" to claim $\mathcal{U}_{n,r}=\{w:\Aut(w)=\{\mathrm{id}\}\}$ is "open and dense in $\mathcal{H}_{n,r}$, with complement of Lebesgue measure zero." Erdős–Rényi (1963) is a statement about the **discrete uniform/counting measure** on the finite set $\{0,1\}^{\binom{n}{2}}$ (almost all *labeled graphs* are asymmetric) — it says nothing about Lebesgue measure on the continuous weight space $\mathbb{R}^{\binom{n}{r}}$. The needed continuous-genericity fact is actually easy to prove directly (the fixed-point set of any nontrivial $\sigma\in S_n$ is a proper linear subspace, hence measure zero, and a finite union of such is still measure zero) — but that is a different, simpler argument than the one cited, and attributing it to Erdős–Rényi is a citation-precision error. (The two other primary citations under scrutiny — Sabidussi 1960, Vizing 1963, Brouwer–Cohen–Neumaier 1989, Cai–Fürer–Immerman 1992, Chen 1977 — check out against the real literature and are used appropriately.)

---

### MEDIUM — GAP-02: Section 5's reach functional depends on an undefined embedding

$\kappa_u(W)$ is defined in terms of vertex coordinates $\bm{x}_v$, described only as coming from "the spectral-effective resistance metric $d_R(u,v)=\sqrt{R_{uv}}$" — but the actual map $W\mapsto\{\bm{x}_v(W)\}$ (e.g., an MDS/diffusion embedding via eigenvectors of a resistance-derived matrix) is never specified. Eigenvector maps are generically algebraic but multivalued with branch points at eigenvalue crossings; Theorem 5.1 part (2) asserts $\mathcal{L}_{\mathrm{inv}}$ is "real-semialgebraic," which is the load-bearing hypothesis for invoking the Kurdyka–Łojasiewicz theorem — but this cannot be checked without pinning down the embedding map, and eigenvector-based embeddings are not obviously semialgebraic at crossing loci. This is a genuine gap in the well-posedness argument, not just missing detail.

---

### LOW/COSMETIC — TYPO-06 / NOT-07

- **Numbering mismatch with the audit brief itself**: counting all shared-counter environments in Section 6 in document order — Def. 6.1 (sieve tree), Def. 6.2 (graph number), Thm 6.3 (bijection), Def. 6.4 (Cartesian product, unlabeled), Def. 6.5 (Cartesian prime, unlabeled), **Thm 6.6** (Sabidussi–Vizing) — the Sabidussi–Vizing theorem is actually **Theorem 6.6**, not "Theorem 6.4" as both the audit brief and the informal framing suggest. Two unlabeled `definition` environments intervene and consume counter numbers. Worth fixing (or labeling those definitions) before final compilation so cross-references in any accompanying text/README are correct.
- "$\mathcal{M}_{n,r}$ ... is an orbispaces of real dimension" — grammatical error (singular/plural), Theorem 4.1.
- Battery 5's worked example gives $\Phi(H_1)=3,\ \Phi(H_2)=2$. Applying the paper's own formulas literally ($\pi_u(G)=\mathbb{I}(I_u(G)\le\theta_u)$, $\theta_u=0$, $\Omega_{\mathrm{Chen}}(H_1)=+2$, $\Omega_{\mathrm{Chen}}(H_2)=-2$, single deciding bit) gives bit$(H_1)=0$, bit$(H_2)=1$, hence $\Phi(H_1)=2^1+0=2$ and $\Phi(H_2)=2^1+1=3$ — the **opposite** assignment from what's printed. Either the convention differs from what's stated or the benchmark numbers are wrong; as written it's an internal inconsistency.

---

### UNC-03: Unverifiable formal/numerical claims

The claims of "13 Lean 4 modules, 37 theorems verified, 0 sorry, 0 axioms, 0 vacuous implications, 0 tautologies" and the various $10^{-13}$–$10^{-15}$ numerical agreement figures in Section 7 cannot be checked against the manuscript text alone — no Lean source or benchmark scripts were provided for this audit. Given that the identity underlying Theorem 3.3 is demonstrably false (see above), a "0 sorry / 0 axioms" Lean claim for a module named `Volume2_BooleanInversion.lean` should be treated with particular skepticism until the actual Lean source (not just the manuscript's informal restatement of the theorem) is produced and inspected — it's possible the Lean formalization states something subtly different (and correct) from the LaTeX theorem, or that it inherits the same error.

---

## Summary Table

| # | Location | Class | Severity |
|---|---|---|---|
| 1 | Thm 3.3 proof | INV-01 | Critical — false identity |
| 2 | Thm 3.1 / Abstract | INV-01 | Critical — category error (quotient) |
| 3 | Thm 2.2 | VAC-04/GAP-02 | Critical — unnormalized "exact" invariant |
| 4 | Thm 6.3 proof | CIRC-05 | High — circular completeness assumption |
| 5 | Prop 3.2 proof | GAP-02 | Medium — non-sequitur example |
| 6 | Thm 4.1 | NOT-07 | Medium — misapplied citation |
| 7 | Thm 5.1 / §5.1 | GAP-02 | Medium — undefined embedding |
| 8 | §6 numbering | TYPO-06 | Low |
| 9 | Battery 5 | TYPO-06 | Low — inconsistent worked example |
| 10 | §7, Lean claims | UNC-03 | Unverifiable |

---

## VERDICT: REVISE

Two of the four new headline results in this round (Theorem 3.3's proof, and the quotient-space overclaim wrapped around Theorem 3.1) contain outright mathematical errors verifiable by direct computation, not merely stylistic gaps. The signature new contribution of Section 6 — the Adaptive Invariant Sieve and its bijection Theorem 6.3 — is proved circularly and rests on a predicate (the Chen holonomy sign) whose well-definedness was never established in Section 2. The Sabidussi–Vizing material (Theorem 6.6, mislabeled as 6.4) is itself sound and correctly cited, but it is not actually connected by any theorem to the $\Phi$-arithmetization, so the abstract's claim of "bridging" the two constructions into a unified "Graph Number Theory" is not supported by the body. This round cannot pass; the two INV-01 items in particular need to be fixed at the level of the mathematics, not just the prose.