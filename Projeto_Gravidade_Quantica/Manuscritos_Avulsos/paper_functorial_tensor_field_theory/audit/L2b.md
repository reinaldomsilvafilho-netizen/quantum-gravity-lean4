# Layer-2b targeted re-check: round-2 fixes (functorial tensor paper)

- **Checker:** independent session (Claude Opus), 2026-10-06. I wrote neither the paper, the audits nor any fix. Skill `prova-rigorosa` followed.
- **Inputs:** `L2_layer2.md`; "Round 2" of `fixes_layer1.md`; `diff` of the current `.tex` against `_arquivo/backup_tex_2026-10-06/.../paper_functorial_tensor_field_theory_round2.tex`. There are 8 hunks, and every hunk is reviewed below. No other text changed.
- **Scripts:**
  - `scripts/L2b_checks.py` → `L2b_checks.out.txt`: 36 checks, **0 failures**. They use test data independent of `round2_checks.py`: a random entangled field in C⁵, a radial-direction immersion, and a Gauss-equation oracle. They include a fidelity-oracle convergence study (observed rates 2.000 and 2.001, expected 2).
  - `scripts/L2b_build.py` → `L2b_build.out.txt`.
- **Two of my own tests were wrong at first; I fixed the tests, not the tolerances:**
  - A "relative phase" control used a *fixed* unitary, which by Prop. 2.3(c) cannot change h. I replaced it with an x-dependent relative phase.
  - The one-sided fidelity oracle had O(h) error. I symmetrised it, giving O(h²), and verified the rate.
- No background jobs. `processos_orfaos.py`: 0 suspects.

## Items

| Item | Verdict | Evidence |
|---|---|---|
| **A7** Ex. 6.1 display and conclusion | **CONFIRMA** | **Display.** n·n·(G+Λg) = 3ȧ²/(N₀²a²) − Λ (B1). This is checked symbolically via Christoffels, and independently via the Gauss equation 2G(n,n) = R(h) + K² − K_ijK^ij with flat slices. Control: the old display without −Λ is off by Λ.<br>**Conclusion.** At the ends ȧ = 0, so the value is −Λ: Λ = 0 is forced there, and then the interior value is ≠ 0. "Solves for no Λ" is valid. |
| **M11** Rem. 5.6(b) | **CONFIRMA** | Re-derived. T′ = e^{ib(t)}T is jointly smooth. For each t the phase is constant in x, so Prop. 2.3(b) gives the same h and T′(·,t) stays projectively immersed. b = 0 on [0,ε] ∪ [L−ε,L], so T′ coincides with T on the sitting intervals: same source and target, same Hom(D,D′). N, Nⁱ and Ψ do not involve T, so the image is equal. The morphisms are pairs (L, D(·)) with no quotient, and ‖T′−T‖ = \|e^{iπ}−1\| = 2 at L/2. So F is not injective on that hom-set: not faithful. Non-emptiness: a constant path of length 1 is a non-identity morphism once a datum exists (Lemma 2.8). The U(t) = e^{ib(t)H} sentence is correct too (exp of a bounded operator, Prop. 2.3(c)).<br>B2: on the sitting intervals the endpoint difference is exactly 0; the middle difference is 2.000000000000000; Δh ≤ 1.8e-7 (fidelity oracle, \|h\| ≈ 9.6); T′ min eigenvalue 4.08. Controls: a fixed unitary moves the endpoint (1.33); an x-dependent relative phase changes h (3.09). |
| **N1** Lemma 2.8(a) | **CONFIRMA** | dim H = 0: no unit vector. dim H = 1 or 2: P(H) has real dimension 0 or 2 < 3. So the differential of the ray map has a non-zero kernel at every x, where h(v,v) = 0, and Prop. 2.3(a) applies. The identification of h with 4×(Fubini–Study pull-back) is in Def. 2.2. B3a: 20 random fields into C² and C¹ give eigenvalue ratio ≤ 7.6e-17. Control: C³ random fields are immersed (ratio ≥ 5.6e-3). |
| **N1** Lemma 2.8(b) | **CONFIRMA, one cosmetic gap** | Re-derived the first claim:<br>• P_x kills the term parallel to T;<br>• the e₀-component argument gives c = 0;<br>• then dι(v) = 0, so v = 0.<br>B3b: an immersion with dι(∂₁) ∥ ι. With e₀ the field is immersed (min eigenvalue 0.068), and the fidelity oracle equals the analytic 4·PJᵀPJ/‖f‖² to 1.7e-7. Control: **without e₀ the field is not immersed** (min eigenvalue 4e-36). So e₀ is essential, as the proof uses.<br>**Gap (cosmetic):** "on {β_k = 1} its k-th block is φ_k, whose differential is injective". This needs β_k ≡ 1 on a *neighbourhood*, or 0 ≤ β_k ≤ 1 (then dβ_k = 0 at a maximum). As written, β_k = 1 at a point with dβ_k ≠ 0 lets d(β_kφ_k) = dβ_k·φ_k + dφ_k lose rank. **Fix:** "with values in [0,1]" or "such that the interiors of {β_k = 1} cover". The standard construction gives both, so the lemma is true. |
| **N1** uses | **CONFIRMA** | • Prop. 6.3 assumes a field exists ("as it does whenever dim H = ∞"), and its proof uses exactly that field.<br>• Rem. 5.6(b) is conditioned on Path having a non-identity morphism.<br>• Ex. 6.1 supplies explicit data (dim H = 8), consistent with (a), since 8 > 2.<br>• Thm 5.4 and Lemma 5.2 need no existence (an empty category is fine).<br>• Lemma number 2.8 confirmed in the `.aux`. |
| **N4** Prop. 6.2 | **CONFIRMA** | The expanded α′ equals the derivative (sympy) and is concave. The minimum on [0,1] is min(1−s₀/2, (1+s₀)/2), matching a 2·10⁵-point grid to 1e-16. The infimum over s₀ is ½, not attained, so "≥ ½ > 0" is correct and sharp. At s₀ = ½: α′ ∈ [¾, 9/8] and ∫α′ = 1, as Prop. 6.3 uses. The statement now separates s ∈ (0,1) (no hypothesis) from the endpoints (explicit continuity), and the proof uses continuity only there. Control: a 0.6 bound fails (0.505 at s₀ = 0.01). |
| **N3** Choquet-Bruhat | **CONFIRMA (chapter-level)** | Crossref: the book DOI resolves (Choquet-Bruhat; ISBN 9780199230723; "issued" 2008-12-04 online, OUP print 2009). Ch. VI = `…003.0006` "Local Cauchy Problem", pp. 142–178. Its abstract lists "wave gauges, local existence for the full Einstein equations, …, Einstein equations with field sources". Control: a fake chapter DOI gives 404. **No theorem number can be given from resolvable metadata.** I had no full-text access either, and I do not guess one. The "Ch. VI" citation is honest. The open item stays: pin the theorem when someone has the book. |
| Declarations | **CONFIRMA** | It is verbatim equal, whitespace-normalised, to `_staging/DECLARACOES_PADRAO_ARTIGOS.tex` with "paper" and the Lean sentence (B6). Control: a mutated block differs. No GitHub URL or old AI text is left in the `.tex`. The corrector's notes stand and are left to the author:<br>• the block says "Conjecture" but the paper has Open problems;<br>• it omits "Corollary" (Cor. 2.6 and 5.5 exist);<br>• "earlier versions" is close to house rule 6. |
| `CORRECTIONS_2026-10-06.md` | **CONFIRMA** | No GitHub claim and no "pending". Item 9 now gives the correct e^{ib(t)} argument and why a fixed unitary fails. The Review section matches the diff. |
| `ZENODO_DESCRIPTION.md` | **CONFIRMA** | Says "compact", no dagger-compact claim. No GitHub, no pending. 242 words, within the ≤ 250 limit. **Cosmetic:** "The repository's Lean files" names a repository that the paper no longer mentions. Consider "The Lean files of earlier versions". |

## Build

`audit/L2b_build/`, pdflatex ×3:
- every run exited with code 0;
- 0 errors, 0 warnings, 0 overfull boxes, 0 underfull boxes, 0 undefined references;
- 11 pages.

The only "warning" string in the log is the `infwarerr` package banner.

## Close

- **Hardest step:** Lemma 2.8(b), the immersion. The β_k wording is the only gap, and it is cosmetic.
- **What would falsify:** a projectively immersed field into C² (impossible by dimension), or a phase path that changes h (excluded by Prop. 2.3(b)).
- **Literature:** Crossref resolved 10.1093/acprof:oso/9780199230723.001.0001 and the Ch. VI record …003.0006.
- **Open:** the theorem number in Choquet-Bruhat Ch. VI; the β_k wording; the Zenodo "repository" word.
