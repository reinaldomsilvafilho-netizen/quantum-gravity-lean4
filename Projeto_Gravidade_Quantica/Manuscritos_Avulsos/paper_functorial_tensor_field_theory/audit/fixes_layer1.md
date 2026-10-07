# Layer-1 fixes: functorial tensor paper (concept DOI 10.5281/zenodo.22441676)

- **Corrector:** independent session (Claude Opus), 2026-10-06. I wrote neither the paper nor `blind_layer1.md`. I did not read the R7 or `CLAUDE_*` files.
- **Backup of the original source:** `_arquivo/backup_tex_2026-10-06/Manuscritos_Avulsos/paper_functorial_tensor_field_theory/paper_functorial_tensor_field_theory.tex`, logged in `MANIFESTO.tsv`.
- **Scripts:**
  - `scripts/math_checks.py` (referee): re-run, exit 0. All of C1–C8 reproduce.
  - `scripts/fixes_checks.py` (new): V1–V9, exit 0, output in `fixes_checks.out.txt`. Every check has an oracle and a negative control; V4 includes an h-refinement with observed rate 2.00.
  - `scripts/doi_check_v2.py` (new): 7 DOIs resolved through Crossref or DataCite, and the fake-DOI control returns 404.
- **Lean:** I checked by grep. No `formal_proofs_lean4/*.lean` file imports Mathlib, the lakefile has no `require`, and `Cobordism.lean` and `CTensMan.lean` contain `fun _ => True` placeholders.
- **Attribution checks against source text:**
  - Verstraete–Cirac (arXiv:1002.1824v1, full text read). It defines the cMPS, states the gauge invariance Q→XQX⁻¹, R→XRX⁻¹, and gives the normalization Q = −½R†R − iH and the block-entropy bound 2 log₂D. It contains no "fundamental theorem".
  - Bousso et al. (arXiv abstract): the QNEC is proved for free and superrenormalizable bosonic theories.
- **Numbering:** item labels in the first column use the referee's numbering of the old paper. The "Change" and "Where" columns use the numbering of the new source.
- **Verdict:** I agree with all 36 items and disagree with none. One nuance (A7): the referee's counterexample now lies inside the paper's own data class. It is realized by an explicit product-state field, though not by a cMPS.

## A items

| Item | Agree? | Change | Where | Check |
|---|---|---|---|---|
| A1 CTensMan is not a category | Agree | Gradient-flow classes are dropped. Prop 6.4 proves that the identity law fails, and Remark 6.5 lists the remaining defects. The repair is the Moore-path category `Path_M` with sitting instants, proved in Lemma 5.2. | §5, §6.3 | C-proof; V8 (junction smoothness, with a non-sitting control) |
| A2 ⊗ and unit leave the category | Agree | Remark 6.6. No monoidal claim remains. | §6.4 | — |
| A3 dagger-compact false | Agree | Remark 6.6: no morphism 1 → T*⊗T exists. Remark 5.6(e): path reversal is a dagger on `Path_M`, but it differs from geometric time reversal by the sign of the shift. | §5, §6.4 | — |
| A4 Cob not a category | Agree | Prop 6.7 proves "no identities" by a volume argument. The target is now `Cyl_M`, with sitting collars, concatenation and smooth gluing. | §5, §6.5 | — |
| A5 lapse not smooth | Agree | Prop 4.2: (a) the lower bound; (b) proof of smoothness under locally constant rank, by a Riesz contour; (c) the referee's counterexample. | §4 | V4, V4b; referee C2 |
| A6 F ill-defined on classes | Agree | Prop 6.3 is an analytic proof by strict Jensen; the referee's version was numerical only. Prop 6.2 adds a no-go: a covariant lapse vanishes on constant paths. | §6.2 | V3a, V3b; C3 |
| A7 Lemma 5.1 circular and false | Agree | The lemma is deleted. Example 6.1 uses a product-qubit field with QFI metric sin²(2θ)δ and FRW image: the constraints hold at the ends and fail in the interior. It is stated that this is not a cMPS realization. Open problem 7.1 records the remaining question. | §6.1, §7 | V1, V2; C4 |
| A8 Thm 5.2 and 5.3 fail | Agree | Both theorems are deleted. Thm 5.4 (Moore functor) is proved, and Cor 5.5 (Einstein subcategory) is proved. Remark 6.8 shows that a constant path of positive length is not static, with K_xx = −cos x/(2N₀). | §5, §6.5 | V7; C1c |
| A9 sign of j_i | Agree | Prop 3.1 gives j_i = −Re Tr(π†∂_iψ), with proof. The constraint (3.4) uses it. | §3 | C6 |
| A10 formal-verification claim false | Agree | The section is removed. The Declarations say the Lean files are a placeholder skeleton without Mathlib that verifies nothing. | Declarations | grep (above); referee `lean_check.py` |

## M items

| Item | Agree? | Change | Where |
|---|---|---|---|
| M1 on-shell K undefined | Agree | The on-shell object condition is removed. K is defined from the path, eq. (3.4) context. | §3 |
| M2 S unspecified | Agree | Gradient flows are dropped; Remark 6.5(c). | §6.3 |
| M3 Prop 2.2 has no proof | Agree | Deleted; Remark 6.6. | §6.4 |
| M4 dimension mismatch of ρ₁⊗ρ₂ and ψ | Agree | Remark 6.6(b). | §6.4 |
| M5 Hessian condition type mismatch | Agree | Deleted together with the lemma. | — |
| M6 ∇T = 0 unjustified | Agree | No conservation is claimed. Open problem 7.1 asks for the matter equation. | §7 |
| M7 ρ(x,t) undefined | Agree | ρ(x,t) is now part of the path data (Def 4.1). | §4 |
| M8 F on products and dual in Cob undefined | Agree | No such claim remains; Open problems 7.2–7.3. | §7 |
| M9 Prop 5.4 is a heuristic | Agree | Now an unnumbered heuristic paragraph with an order-of-magnitude estimate: ln χ ≥ A/(8ℓ_P²) = 4.8×10⁶⁸ for 1 m², using the VC block bound 2 log χ. | §6.6 |
| M10 Cor 5.5 amplitude not derived | Agree | Deleted. Open problem 7.4 notes only that Z∘F is a functor by Thm 5.4. | §7 |
| M11 faithfulness unproved | Agree | Deleted. Remark 5.6(b) proves that F is not faithful, using global-unitary invariance (Prop 2.3(c)). | §5 |
| M12 "NEC prevents CTCs" false | Agree | Remark 3.3(b) gives the Gödel counterexample (DOI checked). | §3 |
| M13 abstract and introduction overclaim | Agree | Both are rewritten to state the proved results and the failures. | Abstract, §1 |
| M14 conclusion claims absent things | Agree | Rewritten. Wilson loops and "proving emergence" are gone. | §8 |

## B items

| Item | Agree? | Change | Where |
|---|---|---|---|
| B1 Q ∈ u(χ) non-standard; commutator term dead | Agree | (Q,R) ∈ End are now general. Prop 4.3(b) gives the vanishing condition, with a remark that it fails in the VC normalization unless R = 0. | §2, §4 (C1a) |
| B2 Λ inconsistency | Agree | Λ appears consistently in (3.4). | §3 |
| B3 ∂_tK equation wrong | Agree | The equation is deleted and not used. | — |
| B4 Israel sign convention | Agree | Moot: there is no junction argument. Gluing is smooth by sitting collars. | §5 |
| B5 "strict" ⊔ associativity | Agree | Deleted. The Moore concatenation is strictly associative (Lemma 5.2). | §5 |
| B6 graphon contractions undefined | Agree | Removed. | — |
| B7 ψ = R not gauge-invariant; T* breaks ψ = R | Agree | Remark 2.7. ψ is an independent datum. | §2 |
| B8 citation defects | Agree | Atiyah title per Crossref. Segal removed, being uncited after the rewrite. Verstraete–Cirac is cited only for what it contains: the definition, gauge invariance, normalization and block bound. RT is cited only for S = Area/4G. The uncited self-references are removed. The book is cited with its DataCite DOI. "Unified Grand Synthesis" is removed. Gödel 1949 added. | Bibliography |
| B9 χ scale not discussed | Agree | §6.6 (V9: CODATA via scipy). | §6.6 |
| B10 "Entropic" NEC misnomer | Agree | Renamed "null energy identity". | §3 |
| B11 redundant Riemannian metric on M | Agree | M is now only a smooth manifold. | §2 |
| B12 Zenodo description overclaims | Agree | A new `ZENODO_DESCRIPTION.md` was written. | folder |

## Confirmed items kept, with proofs

- QFI positivity: Prop 2.3(a).
- Phase, fixed-unitary and conjugation invariance: Prop 2.3(b,c), V6.
- Pointwise gauge invariance: Lemma 2.4 and Cor 2.6, V5.
- ρ_matt: Prop 3.1 (C6b).
- T_kk identity: Prop 3.2 (C5).
- Lapse lower bound: Prop 4.2(a).

## Build

pdflatex was run 3 times: 0 errors, 0 warnings, 0 overfull or underfull boxes, 0 undefined references, 10 pages. Auxiliary files were deleted.

## Open for layer 2

- Re-check Prop 4.2(b) (contour argument), Prop 6.3 (Jensen) and Thm 5.4, which are new proofs written by this corrector.
- The AI-use statement is kept verbatim as the author wrote it. It reads "solely for … compositional verification" and conflicts with the book's standard declaration. **The author must confirm it** (cf. F-21/F-29).

## Round 2 (2026-10-06)

- **Corrector:** independent session (Claude Opus). I wrote neither the paper, the audits nor the round-1 fixes. Inputs: `L2_layer2.md`, this file, the current `.tex`.
- **Backup:** `_arquivo/backup_tex_2026-10-06/Manuscritos_Avulsos/paper_functorial_tensor_field_theory/paper_functorial_tensor_field_theory_round2.tex`, logged in `MANIFESTO.tsv`.
- **Script:** `scripts/round2_checks.py` → `round2_checks.out.txt`, R1–R4, 15 checks, **0 failures**. Each has an independent oracle and a negative control.

| Item | Agree? | Change | Check |
|---|---|---|---|
| A7 (B) | Agree | Ex. 6.1 now displays n·n·(G+Λg) = 3ȧ²/(N₀²a²) − Λ. The conclusion stays valid: the constraints near the ends force Λ = 0, and then the interior value 3ȧ²/(N₀²a²) is non-zero. | R1: sympy from Christoffels; control: the display without −Λ differs by −Λ. |
| M11 (M) | Agree | Remark 5.6(b) rewritten with a proof. The field is replaced by e^{ib(t)}T, where b is smooth, b = 0 on the sitting intervals (margin ε < L/4) and b(L/2) = π. The hom-set is the same, and h is unchanged by Prop. 2.3(b) at each t. N, Nⁱ and Ψ do not involve T. The morphism differs, since ‖T′ − T‖ = 2 at L/2. Non-emptiness of the hom-set uses Lemma 2.8. The general U(t) = e^{ib(t)H} is mentioned only for invariance of the image. | R2: endpoint difference 0, Δh ≤ 1e-16, mid difference 2.000000; QFI via a fidelity oracle; control: an x-dependent phase changes h by 10.1. |
| N1 (B) | Agree | New Lemma 2.8, placed at the end of §2 so that no number changes. (a) There is no projectively immersed field if dim H ≤ 2: P(H) has real dimension ≤ 2 < 3. (b) Existence holds if M immerses in Rᵐ and dim H ≥ m + 1, via T = (e₀ + Σ ι_k e_k)/‖·‖. An immersion into R^{3K} comes from finitely many charts and bump functions, so dim H = ∞ suffices. Prop. 6.3 now assumes a field exists. | R3: QFI of the construction for ι: T³ → R⁶ is positive (min eigenvalue 1.0000, analytic oracle g = δ, fidelity oracle). Control: a C² field has min eigenvalue ~1e-16. |
| N3 (B) | Agree, partly | Added Choquet-Bruhat, *General Relativity and the Einstein Equations*, OUP 2009, ISBN 978-0-19-923072-3, DOI 10.1093/acprof:oso/9780199230723.001.0001 (Crossref: title and author match; Crossref "issued" 2008-12-04 is the online date, the print year is 2009). Fourès-Bruhat 1952 is kept as the original theorem. | Crossref chapter record: Ch. VI "Local Cauchy Problem", pp. 142–178. Its abstract lists "local existence for the full Einstein equations … and Einstein equations with field sources". |
| N4 (cosmetic) | Agree | Prop. 6.2 now proves α′ ≥ min(1 − s₀/2, (1+s₀)/2) ≥ ½ (concavity) and makes continuity of N_P an explicit hypothesis for s₀ ∈ {0, 1}. | R4: grid minimum = closed form (error 1e-16), global minimum ½; control: bound 0.6 is violated; s₀ = ½ gives α′ ∈ [¾, 9/8], as Prop. 6.3 uses. |
| N2 (author) | Done per author decision | The declarations block is replaced verbatim by `_staging/DECLARACOES_PADRAO_ARTIGOS.tex`, with "[paper/volume]" set to "paper" and the Lean sentence kept. No duplicate funding, competing-interests, AI, verification or code-availability text remains. `AI_STATEMENT_PROPOSAL.md` is not written, since the standard block is used. | grep |
| Notes | Done | `ZENODO_DESCRIPTION.md`: "dagger-compact" is now "compact". `CORRECTIONS`: item 9 now gives the correct e^{ib(t)} argument; "scripts on GitHub" is replaced by "available from the author on request"; the "layer-2 pending" line and the AI-statement line are replaced by a "Review" section stating that the corrections were independently re-checked and listing the round-2 changes. | — |

**Disagreements and limits.**
- **N3:** the task asked for a theorem number. I could not read the book's text: the OUP chapter, Internet Archive full-text search and Google Books all returned 403, 429 or paywalls. I therefore cite "Ch. VI" only, and I did not guess a theorem number. **Open item:** someone with access should pin the theorem in Ch. VI (local existence with field sources) and add it to the citation.
- **Standard block:**
  - it mentions "Conjecture", while the paper uses "Open problem", and it omits "Corollary";
  - it says "earlier versions" for the Lean files, which is close to house rule 6.
  - I kept the block verbatim as instructed. The author may want to adapt these words.

**Build:** pdflatex run 3 times, exit 0 each time. 0 errors, 0 warnings, 0 overfull or underfull boxes, 0 undefined references, 11 pages. .aux, .out, .toc and .log deleted; PDF kept.

**For re-check (four eyes):** Lemma 2.8, Remark 5.6(b), the Prop. 6.2 bound, and the A7 display.


## Round 3 (independent corrector, 2026-10-06; input: `L2b.md`)

Backup before editing: `_arquivo/backup_tex_2026-10-06/Manuscritos_Avulsos/paper_functorial_tensor_field_theory/paper_functorial_tensor_field_theory_round3.tex`, listed in `MANIFESTO.tsv`.

| Item | Change |
|---|---|
| Lemma 2.8(b), the β_k wording | The cut-offs are now β_k: M → [0,1], supported in U_k, with the sets {β_k = 1} covering M. The proof now says why the k-th block has injective differential there: a point with β_k(x) = 1 is a maximum, so dβ_k(x) = 0 and d(β_kφ_k)(x) = φ_k(x)dβ_k(x) + dφ_k(x) = dφ_k(x). This is the first fix proposed in L2b. |
| `ZENODO_DESCRIPTION.md` | "The repository's Lean files" is now "The Lean files that accompanied the first version". No repository is named. |
| Choquet-Bruhat | Unchanged: cited at chapter level (Ch. VI), as L2b confirmed. The theorem number is still open. |

**Build:** pdflatex run 3 times, exit 0 each time. 0 errors, 0 warnings, 0 overfull or underfull boxes, 0 undefined references, 11 pages. .aux, .out, .toc and .log deleted; PDF kept.

**For re-check:** the Lemma 2.8(b) sentence only.
