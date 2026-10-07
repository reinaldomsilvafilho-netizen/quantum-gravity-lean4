# Layer-2 re-check: functorial tensor paper (concept DOI 10.5281/zenodo.22441676), v2.0.0 candidate

- **Checker:** independent session (Claude Opus), 2026-10-06. I wrote neither the paper, `blind_layer1.md` nor `fixes_layer1.md`. Protocol: `unified_quantum_gravity_book/audit/verify/PROTOCOL.md` (Camada 2) and skill `prova-rigorosa`.
- **Inputs read:** current `.tex` (535 lines) and PDF, the pre-fix backup (466 lines; every theorem-level statement compared), `blind_layer1.md` (36 items: A1–A10, M1–M14, B1–B12), `fixes_layer1.md`, `CORRECTIONS_2026-10-06.md`, `ZENODO_DESCRIPTION.md`, `scripts/fixes_checks.py`.
- **Scripts:**
  - `scripts/L2_checks.py` → `L2_checks.out.txt`: L1–L9, **0 failures**. Each check has an independent oracle and a negative control; L2 and L3 include refinement studies (L3 observed rate 2.00, 2.00, 2.00).
  - `scripts/L2_doi_check.py` → `L2_doi_check.out.txt`: 7 DOIs resolved (Crossref, DataCite for Zenodo); title, first author, year, volume and first page all match the printed bibliography. Controls: fake DOI 404; mutated volume detected. **0 failures**.
  - Re-run: `math_checks.py` (C1–C8) and `fixes_checks.py` (V1–V9), both exit 0 with byte-identical outputs.
  - One threshold note: the first run of L6 failed because my control threshold (jump > 1e-2) was arbitrary; I replaced it by the analytic one-sided jump (6.4303e-3 predicted, 6.4305e-3 observed). No parameter was tuned to make a test of the paper pass.
- **Build** (`audit/L2_build/`, pdflatex ×3): exit 0 each run, 0 errors, 0 warnings, 0 overfull/underfull boxes, 0 undefined references, 10 pages. The output (585 806 bytes) has the same size as the PDF in the folder.

## 1. The new proofs, line by line

### Prop. 4.2(b): smoothness of the entropy-rate lapse at locally constant rank. CONFIRMA

1. **Spectral localisation.** Write r for the locally constant rank. Weyl gives |λ_k(ρ(p)) − λ_k(ρ(p₀))| ≤ ‖ρ(p) − ρ(p₀)‖.
   - The r largest eigenvalues stay ≥ λ_*/2 once ‖ρ(p) − ρ(p₀)‖ < λ_*/2.
   - The other χ − r eigenvalues are 0, by constant rank and positivity.
   - All eigenvalues are ≤ 1, because the trace is 1.
   - So on U the spectrum lies in {0} ∪ [λ_*/2, 1]. ✓
2. **Contour.** Centre c = ½ + λ_*/8, radius exactly ½ (the formula simplifies).
   - It crosses the real axis at λ_*/8 and 1 + λ_*/8.
   - Distances: λ_*/8 from 0, 3λ_*/8 from λ_*/2, λ_*/8 from 1. These are the paper's claims (L1, symbolic).
   - It lies in Re z > 0, where −z log z is holomorphic. ✓
   - Control: without the +λ_*/8 term the circle passes through the eigenvalue 1.
3. **Cauchy formula.** Σ_{λ_k≠0} f(λ_k) = (2πi)⁻¹∮ f(z) Tr(z−ρ)⁻¹ dz holds because the zero eigenvalues lie outside Γ.
   - L2: random ρ of rank 2, 3, 4 with χ = 4. The trapezoid error falls from 1e-4 to 1e-16 as the node count goes 64 → 1024.
   - Control: f = +z log z is off by ≥ 1.3.
4. **Differentiation under the integral.** (z − ρ(p))⁻¹ is jointly C^∞ on U × Γ, since its norm is ≤ 8/λ_*, and Γ is compact. ✓ The outer map u ↦ ((u²+σ₀²)/κ₀²)^{1/4} is real-analytic. ✓
   - L3: S″ along a rank-2 path in χ = 4 converges at rate 2 to the analytic oracle.
   - Control: at a rank change, |S″| grows like 1/t.
5. **Parts (a) and (c).** (a) is immediate. (c): S′ = log((1−t)/t), the right derivative is +∞, and N ≥ |S′|^{1/2}/√κ₀. ✓ The units are consistent: σ₀ and κ₀ have the dimension of ∂_tS, so N is dimensionless.

### Prop. 6.3: dependence on the representative (strict Jensen). CONFIRMA

1. **Choice of χ.** log χ > 2σ₀ + ½ gives S(s) = ¼ + 2σ₀s ∈ [¼, ¼ + 2σ₀] ⊂ (0, log χ).
   - dS/dp = log((1−p)/((χ−1)p)) < 0 on (1/χ, 1), with S(1/χ) = log χ and S(1) = 0. So p(s) exists, is smooth, and ρ has full rank. ✓
2. **Volume.** √(−g) = N√h. The shift drops out of the volume, and N^i is constant. N(P∘α) = κ₀^{-1/2}(c²α′² + σ₀²)^{1/4}, so Vol = Vol_h ∫φ(α′). ✓
3. **Second derivative.** φ″ = ½c²κ₀^{-1/2}w^{-7/4}(σ₀² − ½c²u²) (L4, symbolic). It is < 0 for u ≥ ¾, since c²u² ≥ 9σ₀²/4 > 2σ₀². ✓
4. **The reparametrisation.** α′ = 9/8 − (3/2)(s − ½)² ∈ [¾, 9/8], it is non-constant, and ∫α′ = 1. ✓ Strict Jensen applies. ✓
5. **Numerical check (L4).** The lapse is built from the actual matrices: p(s) by root finding, S by eigenvalues, d/ds by finite differences. For σ₀ = 0.05, 0.3 and 1:
   - Vol(α) < Vol(id);
   - both agree with the closed form to ≤ 3e-11.
   - Control: c = σ₀/2 makes φ convex on [¾, 9/8], and the inequality reverses.
6. **Prop. 6.2 (bundled).** α′ ≥ ½ for all s₀ (L5). The paper's bound "1 − ½·5/4" is weaker but true, and α′(s₀) − 1 = s₀(1−s₀)/2 ≠ 0. ✓ Extending to s₀ ∈ {0, 1} uses continuity of N_P, which is implicit in "assigns a lapse" (cosmetic).

### Thm 5.4, Lemma 5.2, Def. 5.3, Cor. 5.5: Moore-path functor. CONFIRMA

- **Path_M is a category (Lemma 5.2).**
  - Hom-sets: the endpoints of (L, D(·)) are determined by D(0) and D(L), so the hom-sets are disjoint.
  - Composition is well defined on the stated class. D₁₂ is constant on (L₁ − ε, L₁ + ε), so it is smooth. It is projectively immersed at each t. The rank of ρ is constant on the composite because both pieces share D(L₁). It sits at both ends.
  - Concatenation of functions is strictly associative (L6: exact 0 on 301 points).
  - The formal identities are two-sided units by fiat, and a non-identity composite has length L₁ + L₂ > 0, so the identities never collide with real paths. ✓
- **Cyl_M (Def. 5.3).** It is a category by the same argument. The gluing is smooth because of the t-independent collars. ✓
- **F is well defined.** On the sitting intervals ∂_tS = 0, so N = (σ₀²/κ₀²)^{1/4} = N₀. Also h(t) = g^QFI(T_D) and N^i = X_D. So the image sits at F(D) and F(D′). h is Riemannian (Prop. 2.3a), N > 0 and smooth (Prop. 4.2), and N^i is smooth. ✓
- **Functoriality.** h, N^i and Ψ are pointwise in t, and N depends on a one-sided t-derivative. On the relatively open sets [0, L₁) and (L₁, L₁+L₂] the composite equals one piece, and at L₁ both pieces are constant.
  - L6: toy datum (product-qubit field on T³, ρ = diag(p, 1−p), R = r(t)(2+cos x₁)^{1/2}E₁₁, bump paths). F(D₁₂) = concat(F(D₁), F(D₂)) exactly on a grid that includes the junction.
  - Control: non-sitting paths make the lapse jump at the junction by the analytic amount.
  - F(id) = id holds by definition. ✓
- **Cor. 5.5.** It contains the identities. Closure under composition holds because the Einstein equations are local and every point of a composite has a neighbourhood equal to an open subset of one piece. ✓ It is a subcategory with all objects; that is fine.
- **Honesty.** The introduction says "close to tautological", and Remark 5.6(a) says that no field equation is used. The abstract does not use that phrase, but it does not overclaim: it immediately states that image metrics need not solve Einstein. ✓
- **Remark 5.6(e).** Reversal is involutive and contravariant on concatenation, and (∂_tS)² is invariant. The sign flip of the shift under t′ = L − t is correct. ✓
- **Remark 5.6(b) is wrong as argued.** See M11.

## 2. The 36 layer-1 items

Verdict key: C = CONFIRMA (resolved, correct, no over-correction); P = PROBLEMA.

| Item | Verdict | Evidence / remark |
|---|---|---|
| A1 CTensMan not a category | C | Prop. 6.4 is correct: a locally Lipschitz flow line that is constant on an interval sits at an equilibrium, so by uniqueness it is constant. Remark 6.5(a–c) is correct. The repair is §1 above. |
| A2 ⊗, unit leave category | C | Remark 6.6(a–c). No monoidal claim remains anywhere, including the abstract and the conclusion. |
| A3 dagger-compact false | C | Compactness fails (Remark 6.6). The dagger on Path_M is correct (Remark 5.6(e)), so this is not an over-correction. |
| A4 Cob not a category | C | Prop. 6.7: e∘e = e ⇒ 2V = V ⇒ V = 0, impossible for a non-empty compact Lorentzian manifold with boundary. The C⁰-gluing remark is correct. |
| A5 lapse not smooth | C | §1, Prop. 4.2. |
| A6 F ill-defined on classes | C | §1, Props. 6.2–6.3. See also N1. |
| A7 Lemma 5.1 false | **P (B)** | The deletion is right, and Example 6.1 is correct in substance: h = sin²2θ δ (V1), image FRW, conclusion "no Λ" valid. However, the display "n^μn^ν(G_μν + Λg_μν) = 3ȧ²/(N₀²a²)" is false for Λ ≠ 0. The correct value is 3ȧ²/(N₀²a²) − Λ (L8, sympy Christoffel route). **Fix:** write "with Λ = 0" or add −Λ. The disclaimer "not a cMPS realization" is honest. |
| A8 Thm 5.2/5.3 fail | C | Thm 5.4 and Cor. 5.5 are proved (§1). Remark 6.8: N_1 = −½ sin x₁, K₁₁ = −cos x₁/(2N₀) (V7). Isometries rel. boundary preserve the second fundamental form. ✓ |
| A9 j_i sign | C | Re-derived: h_i^ν = δ_i^ν because n_i = 0, so j_i = −Re Tr(π†∂_iψ). ρ_matt: γ^{00} = γ^{0i} = 0 checked from the ADM inverse. The Hilbert tensor and the momentum-constraint sign (K = −∇n, p_i = −T(n,e_i)) are consistent. |
| A10 formal verification false | C | The section is removed. The "Verification status" paragraph is accurate. See N2 for the AI statement. |
| M1 on-shell K | C | K is defined from the path (eq. 3.4 context). |
| M2 S unspecified | C | Gradient flows dropped; Remark 6.5(c) is correct: S strictly decreases. |
| M3 Prop 2.2 unproved | C | Deleted. |
| M4 ρ₁⊗ρ₂ size mismatch | C | Remark 6.6(b). |
| M5 Hessian type mismatch | C | Deleted with the lemma. |
| M6 ∇T = 0 unjustified | C | No conservation is claimed; Open problem 7.1 asks for the matter equation. |
| M7 ρ(x,t) undefined | C | Part of the path data (Def. 4.1). |
| M8 F on products, dual in Cob | C | No claim remains; Open problems 7.2–7.3. |
| M9 Prop 5.4 heuristic | C | Unnumbered paragraph. 2 log χ is the VC two-cut bound (in nats). ℓ_P² = 2.612e-70 m² and A/(8ℓ_P²) = 4.785e68, dimensionless (L9). |
| M10 Cor 5.5 amplitude | C | Deleted. Open problem 7.4 only notes that Z∘F is a functor. |
| M11 faithfulness unproved | **P (M)** | Remark 5.6(b) does not prove non-faithfulness. Replacing T(·,t) by UT(·,t) for a fixed U changes the source and target (|UT(0) − T(0)| = 1.15 in L7), so the two morphisms lie in different hom-sets, and faithfulness is injectivity on each Hom(D, D′). The conclusion is nevertheless true, so nothing should be weakened. **Fix:** use a t-dependent unitary U(t) = exp(i b(t)H) with b = 0 near both ends. Endpoints and h(t) are unchanged (end difference 7e-16, QFI difference 6e-13) while the morphism changes (mid difference 1.15) (L7). The same wording is repeated in `CORRECTIONS` item 9. |
| M12 NEC ⇏ no CTCs | C | Gödel dust: T = ρuu, so T_kk = ρ(u·k)² ≥ 0; DOI verified. |
| M13 abstract/intro overclaim | C | Every claim (i)–(iv) and every listed counterexample matches a proved body statement. The title is accurate. |
| M14 conclusion | C | It restates only proved results and the stated failures. |
| B1 Q ∈ u(χ); dead term | C | Prop. 4.3(b) re-derived ([Q,∂Q]† = [∂Q,Q] for anti-Hermitian Q). Remark 2.7: Q + Q† = −R†R, which is 0 iff R = 0. ✓ |
| B2 Λ inconsistency | C | Λ is present in (3.4). |
| B3 ∂_tK equation | C | Deleted, unused. |
| B4 Israel convention | C | Moot (collars). |
| B5 strict ⊔ | C | Deleted. |
| B6 graphon | C | Removed. |
| B7 ψ = R not gauge-invariant | C | Remark 2.7; Lemma 2.4 and Cor. 2.6 re-derived (cyclicity; V5). |
| B8 citations | C | Atiyah title correct, Segal removed, VC used only for definition, gauge, normalization and block bound, RT only for S = A/4G, book DOI and Gödel added (L2_doi_check). See N3. |
| B9 χ scale | C | §6.6 (L9). |
| B10 "Entropic" | C | Renamed. |
| B11 redundant metric on M | C | M is a bare smooth manifold. |
| B12 Zenodo overclaims | C | The new description has no sewing or "100 % rigor" claim (see §4). |

**Counts:** 34 CONFIRMA, 2 PROBLEMA (A7: B; M11: M), 0 INCERTO.

**Diff check against the backup:**
- Nothing true was lost. The QFI positivity and phase invariance, ρ_matt, the T_kk identity and the lapse lower bound are all kept, now with proofs.
- What was removed is false, unproved or uncited: Segal, the self-citations, Wilson loops.
- No statement is weakened beyond what is needed. In particular, the dagger on Path_M is kept.

## 3. New observations (not among the 36)

| ID | Severity | Observation |
|---|---|---|
| N1 | B | **Existence of data is implicit.** Prop. 6.3 ("there are a path P") and Path_M being non-empty need a projectively immersed field T: M → H to exist. H is only "a separable complex Hilbert space". For H = C² no immersion exists, because P(C²) has real dimension 2 < 3, so the existence claim fails as stated. **Fix:** assume dim H = ∞ (then every compact M admits one, e.g. Gaussian wave packets after a Whitney embedding), or take M = T³ and H ⊇ (C²)^⊗3 as in Example 6.1. |
| N2 | M (author) | **The AI statement is now inaccurate.** It says "solely for … compositional verification" and "all … mathematical proofs represent the original academic work of the author". Prop. 4.2(b), Prop. 6.3, Thm 5.4, Lemma 5.2 and the counterexample propositions of this version were drafted by an AI corrector session, and "verification" by AI conflicts with the honest Verification-status paragraph. It must be rewritten by the author (F-21/F-29). The fix log already flags this. |
| N3 | B | **Fourès-Bruhat 1952 coverage (Open problem 7.1).** The citation supports local existence for "Einstein–matter" data. The 1952 paper applies its general theorem explicitly to the vacuum case. Einstein–scalar in harmonic gauge falls under the same quasi-diagonal hyperbolic theorem, but a direct reference (Choquet-Bruhat, *General Relativity and the Einstein Equations*, OUP 2009) would be safer. INCERTO-level; non-blocking. |
| N4 | cosmetic | Prop. 6.2: the bound α′ ≥ 1 − ½·5/4 is valid but not sharp (the sharp bound is ½), and it uses continuity of N_P at s₀ ∈ {0,1} without saying so. |

**House style:** no "version", "withdrawn", "corrected" or audit path occurs in the `.tex`. The Lean statement is accurate.

**Affiliation:** "Master's student, Postgraduate Program in Statistics and Agricultural Experimentation (PPGEE/DES), Department of Statistics (DES), UFLA, Lavras, MG, Brazil" matches the canonical form.

**CAPES line:** correct ("Finance Code 001").

## 4. Zenodo notes

**`ZENODO_DESCRIPTION.md`: accurate, with one wording note.** Every "Proved" bullet matches the body, "close to tautological" is stated, and the no-formal-verification sentence is correct. One wording issue: "The proposed monoidal and dagger-compact structures do not exist as stated." The new Path_M does carry a dagger (Remark 5.6(e)); only the compact and monoidal parts fail. Suggest "The proposed monoidal and compact structures …" or "(version-1) dagger-compact structure".

**`CORRECTIONS_2026-10-06.md`: accurate in substance, needs three edits before upload (items 1, 3, 4 below; item 2 is a no-change note).**
1. Item 9 repeats the invalid non-faithfulness argument (M11). It should point to the corrected Remark 5.6(b).
2. Item 4 quotes n·n·G correctly (no Λ), so it is fine. If the paper's display is fixed (A7), no change is needed here.
3. "Scripts: these are in `audit/scripts/` in the GitHub repository" is **currently false**. `git status` shows `Manuscritos_Avulsos/paper_functorial_tensor_field_theory/` as untracked. The same applies to the paper's "Code availability: Sources and scripts are available at …". The folder (source, notes, `audit/`) must be committed and pushed before the Zenodo upload, or the sentence changed.
4. "Review: a layer-2 review … is pending" becomes stale once this report is consolidated. Replace it with the outcome.

The notes otherwise claim nothing the paper does not prove.

## 5. Close (prova-rigorosa)

- **Hardest step:** the composition clause of Thm 5.4 at t = L₁. It relies on the lapse depending only on a one-sided t-derivative, which the sitting collars make equal on both sides. L6 shows that it fails without collars.
- **What would falsify the results:** a datum path whose image is not smooth at the junction despite sitting instants. That is impossible, since the image is constant there. For Prop. 6.3, a concave-region failure; the control shows the inequality does reverse in the convex regime, as theory predicts.
- **Missing before release:**
  - fix A7 (Λ in the display) and M11 (U(t) construction), plus N1;
  - author rewrite of the AI statement (N2);
  - commit and push the paper folder;
  - update `CORRECTIONS` items 9 and "Review", and the dagger wording in `ZENODO_DESCRIPTION`.
  - Per the four-eyes rule, these fixes go to another session.
- **Literature (DOIs resolved in `L2_doi_check.out.txt`):** Atiyah 1988 (10.1007/BF02698547); Verstraete–Cirac 2010 (10.1103/PhysRevLett.104.190405); Ryu–Takayanagi 2006 (10.1103/PhysRevLett.96.181602); Fourès-Bruhat 1952 (10.1007/BF02392131); Bousso et al. 2016 (10.1103/PhysRevD.93.024017); Gödel 1949 (10.1103/RevModPhys.21.447); book (10.5281/zenodo.22290043).
