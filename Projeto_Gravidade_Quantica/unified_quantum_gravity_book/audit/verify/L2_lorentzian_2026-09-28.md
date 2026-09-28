# L2 re-check: ch. 12, "Lorentzian Completion" (sec:lorentzian_completion), 2026-09-28

Layer-2 targeted re-check. Four eyes: I did not write the subsection, the fix log, the research note or
VERIFICACAO.md. I did not edit any `.tex` file.

- **Target:** `chap12_grand_unification_quantum_gravity_treatise.tex`, lines 527–566 and bib lines 725–790.
- **Log checked:** `audit/verify/fixes_lorentzian_2026-09-28.md`.
- **Source of truth:** `Pesquisa_e_Testes/completamento_lorentziano/VERIFICACAO.md`.

## Summary

**30 CONFIRMA, 9 REFUTA, 2 INCERTO (41 items).**

The layer-1 constraints were respected:
- Lee–Wick is not called excluded.
- Pais–Uhlenbeck is absent.
- No layer-1 INCERTO item is asserted.

All numbers reproduce. The REFUTA items are:
- misattributions: #6 BBMM, #17 microcausality scale;
- internal inconsistencies with the rest of ch. 12: #9, #10, #26, #32;
- imprecise mathematical statements: #5, #29, #30.

REFUTA list, one line each:
- **R1 (#5)** "P(τ) ≳ τ⁻² as τ→0, i.e. d_s(τ) ≥ 4 for every τ". The pointwise claim is true: my check gives a minimum of 4.000002, and the Chebyshev argument of VERIFICACAO #1 proves it. But it does not follow from the sketched argument, which gives only the UV lower bound on P. Either add the Chebyshev step or state the UV version.
- **R2 (#6)** BBMM2016 does not say "folklore". In the arXiv text the Weinberg argument (his §10.7, p. 460) is in §V (Conclusions), not §IV, and it concerns the propagator fall-off, not a d_s bound.
- **R3 (#9)** "Hořava–Lifshitz gives up Lorentz invariance *below* M_*" is inverted. By the dispersion relation at l. 512, the Lorentz violation dominates at k ≳ M_* (above M_*, or at lengths below 1/M_*).
- **R4 (#10)** Citing `modesto2012` as the d_s = 2 entire-form-factor route (l. 542, l. 557) contradicts l. 512. There the d_s = 2 family is "a different family from Modesto's", which gives d_s ≤ 4/5. "Asymptotic positivity of the spectral density" is also unsupported: entire form factors have no Stieltjes form (VERIFICACAO #24).
- **R5 (#17)** Anselmi–Piva 2018 (abstract; §5, eq. 5.4; §7) put the microcausality violation at centre-of-mass energies above m_χ, at distances or time intervals below **1/|Γ_χ|**. Here Γ_χ is the negative fakeon width, with Γ_χ ∝ m_χ³/M_Pl² ≪ m_χ. The scale is not "ℓ, the fakeon's Compton wavelength".
- **R6 (#26)** The fakeon route "would fix the scale ℓ_* of eq. graviton_dispersion". That equation is the Lorentz-violating ξ-term, and l. 608 itself says the isotropic symbol gives ξ = 0 and that ξ ≠ 0 needs a preferred frame. A Lorentz-invariant fakeon completion predicts ξ = 0; it does not give a value of ℓ_*.
- **R7 (#29)** "An explicit complex-conjugate pair in the symbol needs n ≥ 3" is false as stated, because it needs the massless pole. S = z² + z + 1 has n = 2, a complex pair, and d_s(UV) = 2.0001 (script). The fix is to add "together with the massless (graviton) pole z = 0", as in VERIFICACAO #5.
- **R8 (#30)** "Each gives up a different one of locality, Lorentz invariance and positivity" fails. There are four routes and three properties, and Lee–Wick and the fakeon both give up positivity: they have the same tree-level symbol and the same residue −1. They differ only in the pole prescription.
- **R9 (#32)** The Conjecture writes ℓ_P = 1/m_2, but in ch. 12 ℓ_P is the physical Planck length (l. 608: "ℓ_* ≳ 10³–10⁹ ℓ_P"). Taken literally, it gives m_χ = M_Pl ≈ 4.5×10⁵ m_φ. Then N²r = 12(1 − 2.5×10⁻¹²), which is Starobinsky, so the single-scale case (8/N², ℓ ≈ 4.4×10⁵ ℓ_P) is excluded under the Conjecture.
  - The Remark's "(b) would also fix, or leave undetermined, m_χ/m_φ" misses this: A_s already fixes m_φ.
  - Suggested fix: state the Conjecture with the free symbol scale ℓ_* = 1/m_2, not ℓ_P, or state the consequence explicitly.

## Scripts (independent of e1–e3 and v1–v3)

| Script | Result | Oracle | Negative control |
|---|---|---|---|
| `scripts/L2_lorentzian_numbers.py` (`.out.txt`) | 18/18 | mpmath quadrature in z (breakpoints at masses, shifted weight) for 12 random Stieltjes G × 9 τ; numerical slow roll of the exact Starobinsky potential (not the closed form); CODATA 2018 ħc, G, ħ | book symbol goes below 4 (min 2.0009); swapped-mass r formula misses the 4/3 edge (0.727); non-reduced M_Pl in the A_s formula gives ℓ = 1.44×10⁻³⁰ m (outside) |
| `scripts/L2_lorentzian_dois.py` (`.out.txt`) | 11/11 Crossref | Crossref API: title, authors, venue, volume, issue, pages | mutated DOI 10.1103/PhysRevD.93.0440179 → HTTP 404 |

**Note on the first run.** A first scipy run with quadrature in ln z gave a spurious d_s = 3.74 for a gapped measure. The high-precision mpmath recomputation gave 4.41 at the same τ. The script now uses the mpmath oracle and passes: the minimum is 4.000002 on the massless branch.

**Papers read** (arXiv full text via pdftotext):
- 1507.00330 (BBMM)
- 1806.03605 (AP 2018)
- 2109.06889 (Anselmi 2021)
- 2005.10293 (ABP 2020)
- 1801.00915 (Anselmi 2018)

## Table

| # | Item (line) | Verdict | Evidence |
|---|---|---|---|
| 1 | l. 530: the chapter is Euclidean only; nothing supplies Lorentzian dynamics with d_s = 2 | CONFIRMA | Consistent with l. 512 ("assumed" symbol, "None of these is derived here") and l. 525. |
| 2 | "structural obstruction, not a gap" | CONFIRMA | Holds under the KL hypotheses (see #3). |
| 3 | KL hypotheses: "two-point function of a Lorentz-invariant, reflection-positive Euclidean field theory" | INCERTO (imprecise) | Missing: scalar field, or a positive-metric component; P(τ) < ∞; d_s is that of the Euclidean heat kernel of S = 1/G (VERIFICACAO #1). Covariant-gauge graviton propagators with indefinite metric are not covered, which matters because the target is the graviton. |
| 4 | Lehmann 1954 for KL; OS 1973 for reconstruction | CONFIRMA | Crossref metadata match. OS reconstruction is standard. Note: the 1973 paper has a known gap repaired in OS 1975 (CMP 42, 281); citing both would be cleaner. |
| 5 | "zG non-decreasing ⇒ S ≤ z/c ⇒ P ≳ τ⁻² … i.e. d_s(τ) ≥ 4 for every τ" | **REFUTA** (inference) | The steps up to P ≳ τ⁻² are correct. They give a UV log-ratio bound, not the pointwise log-derivative bound. The pointwise statement is true: my check gives min 4.000002 over 12 random measures × 9 τ, and it follows from Chebyshev under Gamma(3) (VERIFICACAO #1), a step the text does not give. |
| 6 | "Weinberg's; … recorded as such (folklore) in §IV of BBMM2016" | **REFUTA** | arXiv 1507.00330: §IV is "Discussion", with no Weinberg. The Weinberg remark is in §V "Conclusions": "As was explicitly stated by Weinberg (see Ref. [25] Section 10.7, p. 460) … the propagator cannot vanish … faster than … 1/k²". The word "folklore" does not occur, and BBMM state no d_s ≥ 4 bound. They only report that Aslanbeigi–Saravani with ρ ≥ 0 "starts off at 4". The published section numbering was not checked. |
| 7 | ρ = δ(μ²) − δ(μ² − ℓ_P⁻²) for k² + ℓ_P²k⁴; the only evasion is the weight −1 | CONFIRMA | 1/(z(1+ℓ²z)) = 1/z − 1/(z + ℓ⁻²). NC in the script: min d_s = 2.0009. |
| 8 | Trichotomy: positivity / locality / Lorentz invariance | CONFIRMA, with a caveat | Correct in substance. The "locality" clause ("not representable by KL, nor polynomial") overlaps with positivity; the wording could be tightened. |
| 9 | "HL z = 3 … gives up Lorentz invariance below M_*" | **REFUTA** | l. 512: ω² = c²k² + ak⁴/M_*² + k⁶/M_*⁴. The Lorentz-violating terms dominate for k ≳ M_*, so the violation is above M_*; Lorentz invariance is recovered in the IR. |
| 10 | "entire form factors [modesto2012] keep Lorentz invariance and asymptotic positivity … the two ghost-free routes discussed above" (also l. 557) | **REFUTA** | l. 512 says the d_s = 2 entire-form-factor operator is "a different family from Modesto's", while Modesto gives d_s ≤ 4/5. Citing modesto2012 for the d_s = 2 route contradicts the chapter. "Asymptotic positivity of the spectral density" has no support: an entire S_T is not Stieltjes, since \|1/S_T(5i)\| ~ 10^20927 (VERIFICACAO #24). |
| 11 | The fakeon paragraph is framed conditionally: "none of it is established, or claimed, by this book" | CONFIRMA | Honest label; no theorem. |
| 12 | "fakeon prescription of Anselmi and Piva [Anselmi2018, AnselmiPiva2018, Anselmi2021]" | CONFIRMA | All three papers are by Anselmi, or Anselmi–Piva. Minor: the prescription originates in Anselmi 2017 and Anselmi–Piva 2017, which are not cited. |
| 13 | Removed "by a non-analytic Wick rotation of the Euclidean theory" | CONFIRMA | Anselmi 2018 abstract: "We formulate them by (nonanalytically) Wick rotating their Euclidean versions". |
| 14 | The symbol, the closed form and d_s are unchanged | CONFIRMA | These are Euclidean objects (VERIFICACAO #7). |
| 15 | Lorentz-invariant and local | CONFIRMA | AP 2018 intro: the Lagrangian is polynomial and the action is "strictly renormalizable". |
| 16 | Renormalizable by power counting [Stelle1977], compatible with the fakeon [ABP2020] | CONFIRMA | Anselmi 2018 abstract: "If standard power counting constraints are fulfilled, the models are also renormalizable". AP 2018: renormalization "is not affected by the fakeon prescription". |
| 17 | "violation of microcausality at distances ≲ ℓ, where ℓ is the fakeon's Compton wavelength [AnselmiPiva2018]" | **REFUTA** | AP 2018 abstract: "violation of causality at energies larger than the fakeon mass". §7: "at distances or time intervals smaller than 1/\|Γ_χ\|". §5 (eq. 5.4): Γ_χ ∝ C·m_χ·(m_χ²/M_Pl²), so 1/\|Γ_χ\| ≫ 1/m_χ. The scale is the inverse width, not the Compton wavelength. |
| 18 | "unitarity is proved perturbatively, to all orders, via a spectral optical theorem [Anselmi2021]" | CONFIRMA | Anselmi 2021 abstract and intro: spectral optical theorem for arbitrarily many loops, "which proves unitarity". "Perturbatively unitary to all orders" is verbatim in the Anselmi 2018 abstract. Note: AP 2018 qualifies it as "up to the effects due to the cosmological constant"; this is not stated in the text, but it is not an overclaim for flat space. |
| 19 | TT operator k²(1 + k²/m₂²) [Stelle1978]; ℓ = 1/m₂ | CONFIRMA | Spin-2 propagator 1/k² − 1/(k² + m₂²) (VERIFICACAO #36). The propagator itself is in Stelle 1977; Stelle 1978 has the linearized masses. Either citation is acceptable. |
| 20 | m_χ > m_φ/4; r = 24m_χ²/[N²(m_φ² + 2m_χ²)]; 4/3 < N²r < 12 [ABP2020] | CONFIRMA | Read in arXiv 2005.10293: abstract ("m_χ > m_φ/4", "4/3 < N²r < 12") and eq. 7.3. |
| 21 | N = 60 window [3.7×10⁻⁴, 3.3×10⁻³] | CONFIRMA | Script: 3.7037×10⁻⁴ and 3.3333×10⁻³. NC (swapped masses) fails the 4/3 edge. |
| 22 | Single scale: N²r = 8, r ≈ 2.2×10⁻³ | CONFIRMA | 2.2222×10⁻³. The m_χ = m_φ modelling choice is stated as a "special case". |
| 23 | 2.2σ from zero at LiteBIRD δr ≈ 10⁻³; 1.1σ from 12/N²; "weak test" | CONFIRMA | 2.222σ and 1.111σ. The hedged wording matches VERIFICACAO #17 (no "detection" claim). |
| 24 | ℓ ≈ 7×10⁻³⁰ m ≈ 4.4×10⁵ ℓ_P | CONFIRMA | Numerical slow roll (N = 60, A_s = e^3.044×10⁻¹⁰, M_red from CODATA 2018): m_φ = 2.730×10¹³ GeV, ℓ = 7.23×10⁻³⁰ m = 4.47×10⁵ ℓ_P. Closed form: 6.9×10⁻³⁰ m. Order of magnitude: m_φ/M_Pl = 2.2×10⁻⁶. Clarity note: the text writes ħc/m_χ, but the value uses m_χ = m_φ (single scale), normalized to A_s at N = 60; neither is stated. |
| 25 | Dimensional check [ħc]/[mc²] = m | CONFIRMA | Correct. |
| 26 | "would fix the scale ℓ_* of eq. graviton_dispersion" | **REFUTA** | graviton_dispersion (l. 605) is the Lorentz-violating ξ-dispersion. l. 608: the isotropic symbol continued to Lorentzian signature gives ξ = 0, and "any ξ ≠ 0 presupposes a preferred frame". A Lorentz-invariant fakeon completion therefore gives ξ = 0 (no dispersion signal); it does not fix ℓ_* there. |
| 27 | ℓ < 2.9×10⁻²⁹ m from m_χ > m_φ/4 | CONFIRMA | 4ℓ = 2.891×10⁻²⁹ m. |
| 28 | Lee–Wick shares the tree-level symbol; the complex pair comes from the resummed width | CONFIRMA | Respects VERIFICACAO R1. LeeWick1970 and GOW2008 metadata match. |
| 29 | "explicit complex-conjugate pair in the symbol itself needs degree n ≥ 3 ⇒ d_s ≤ 4/3" | **REFUTA** (missing hypothesis) | This is true only if the massless pole is kept: z(z² + z + 1) gives d_s = 1.3335. Without it, z² + z + 1 has n = 2, a complex pair, and d_s(UV) = 2.0001 (script). VERIFICACAO #5 has the hypothesis "par complexo **e polo sem massa**" (complex pair **and massless pole**). |
| 30 | "each gives up a different one of locality, Lorentz invariance and positivity" | **REFUTA** | There are four routes and three properties. Lee–Wick and the fakeon both give up positivity (same symbol, same residue −1); they differ only in the prescription (VERIFICACAO #4). |
| 31 | d_s(UV) = 4/n for a polynomial of degree n | CONFIRMA | Standard; script values 2.0001 and 1.3335. |
| 32 | Conjecture: "ℓ_P = 1/m_2"; Remark: "(b) would also fix, or leave undetermined, m_χ/m_φ" | **REFUTA** (consistency) | ℓ_P is the physical Planck length in ch. 12 (l. 608). Literal ℓ_P = 1/m_2 gives m_χ = M_Pl = 4.47×10⁵ m_φ, and then 1 − N²r/12 = 2.5×10⁻¹² (script). So the Conjecture excludes the single-scale case (8/N², ℓ ≈ 4.4×10⁵ ℓ_P) presented just before it, and m_φ is already fixed by A_s. Neither consequence is stated. |
| 33 | Conjecture labelled as a conjecture; no theorem claimed | CONFIRMA | Honest label. |
| 34 | Precision of the Conjecture ("in the continuum limit of the simplicial construction … coincides, up to normalization") | INCERTO | "Continuum limit" and "simplicial construction" are not defined objects in ch. 12. The symbol is introduced at l. 512 as "assumed", not as derived from a simplicial action. The statement is a programme rather than a falsifiable mathematical claim. The Remark partly compensates. |
| 35 | Conjecture consequence: the fakeon applies "without altering the symbol, closed form, d_s" | CONFIRMA | Consistent with #14 and with the Euclidean heat-kernel reading as the proved core. |
| 36 | Remark (a)–(c): what would be needed; "None of (a)–(c) is attempted here" | CONFIRMA | Honest. Minor: "simplicial/minimax construction of Chapters 2–9" is vague. |
| 37 | The layer-1 INCERTO items (Buoninfante scrutiny, CMB-S4, nonlocal unitarity, LiteBIRD "detection") are not asserted; Pais–Uhlenbeck is absent | CONFIRMA | Checked by reading lines 527–566. |
| 38 | House style: no "corrected / earlier / withdrawn / version", no audit paths | CONFIRMA | grep over lines 527–566: 0 hits. |
| 39 | 11 DOIs resolve | CONFIRMA | Crossref 11/11. Title, authors, venue, volume, issue and pages all match the bibitems. NC 404. |
| 40 | Fix-log statements (lines, items respected) | CONFIRMA | The log is accurate as to what was written. It does not note R1–R9. |
| 41 | Build gate | CONFIRMA | Temp copy, pdflatex ×3: ch. 12 has 0 errors, 0 warnings, 0 overfull boxes, 0 undefined references (20 pp); the master, with the fresh ch. 12 PDF, has the same counts (197 pp). |

## Recommended corrections (for an independent corrector; not applied)

- **R1:** replace "i.e." with the Chebyshev step, or write "d_s → ≥ 4 in the UV" and cite the pointwise version separately.
- **R2:** cite Weinberg, *QFT I*, §10.7, directly. For BBMM, write "§V" and drop "folklore".
- **R3:** write "above M_*".
- **R4:** replace `modesto2012` in l. 542 and l. 557 with the d_s = 2 entire-form-factor family of l. 512, and delete "asymptotic positivity of the spectral density".
- **R5:** write "at energies above m_χ and time scales below 1/|Γ_χ|, where Γ_χ < 0 is the fakeon width".
- **R6:** write "would predict ξ = 0 in eq. graviton_dispersion (no dispersion signal) and fix the fakeon scale".
- **R7:** add "together with the massless pole".
- **R8:** write "Lee–Wick and the fakeon both give up positivity and differ in the prescription; the other two give up locality and Lorentz invariance respectively".
- **R9:** write the Conjecture with ℓ_* = 1/m_2, or state that ℓ_* = ℓ_P implies r = 12/N² to 10⁻¹².
- **#3:** add "scalar (or positive-metric component)" and "P(τ) < ∞".

## Round 2 re-check (2026-09-28)

Layer-2 re-check of the Round-2 correction (`fixes_lorentzian_2026-09-28.md`, section "Round 2"). Four eyes: I did not write the subsection, either fix log, or the Round-1 L2 report. No `.tex` file edited. Target: `chap12_grand_unification_quantum_gravity_treatise.tex` l. 527-570 and bibitem `Weinberg1995` (l. 741-745).

**Summary: 10 CONFIRMA, 1 REFUTA (new, house style), 2 INCERTO (minor). All 9 Round-1 REFUTA and both INCERTO items are resolved.**

Script: `scripts/L2r2_lorentzian_check.py` (`.out.txt`), 16/16 PASS. Oracles: closed limits of N²r(x), x = m_χ/m_φ; m_φ from an independent numerical slow roll of the exact Starobinsky potential normalised to A_s = e^3.044×10⁻¹⁰, N = 60 (m_φ = 2.73×10¹³ GeV), CODATA 2018 ħc, G, ħ; mpmath heat-kernel log-derivative at τ = 10⁻⁷ for 6 random positive Stieltjes G; Crossref API. Negative controls (all fail as required): swapped-mass r formula (11.6 ≠ 4/3 at x = 1/4); reduced Planck mass for m_χ (defect 6.3×10⁻¹¹ ≠ 2.5×10⁻¹²); ghost symbol z + z² (UV d_s = 2.0003 < 4); mutated DOI → 404.

| Item | Verdict | Evidence |
|---|---|---|
| R1 (#5) KL bound now UV-only, eq. `kl_bound` "lim_{τ→0} d_s ≥ 4" | CONFIRMA, with a note | The sketched argument (zG non-decreasing ⇒ S ≤ z/c on [z₀,∞) ⇒ P ≥ Cτ⁻²) now supports what is claimed; the pointwise version is explicitly flagged as needing a Chebyshev step not carried out. Script: UV d_s ≥ 4.00000 for 6 random measures; NC ghost symbol 2.0003. **Note (INCERTO, minor):** P ≥ Cτ⁻² gives liminf of the log-ratio −2 ln P/ln τ ≥ 4; it gives the log-derivative limit only if that limit exists. Suggest "whenever the limit exists" or a liminf. |
| #3 KL hypotheses: scalar or positive-metric component, reflection positivity, Lorentz invariance, P(τ) < ∞; covariant-gauge caveat | CONFIRMA | These are the missing hypotheses listed in Round 1 (VERIFICACAO #1). The caveat correctly says indefinite-metric covariant-gauge graviton propagators are not covered. |
| R2 (#6) Weinberg citation, §10.7 p. 460; BBMM §V | CONFIRMA (citation) / **REFUTA (house style)** | Crossref: DOI 10.1017/CBO9781139644167 = *The Quantum Theory of Fields*, CUP, Weinberg, 1995-06-30, ISBN 9780521550017 (Vol. I). The section and page match BBMM's own pointer ("Ref. [25] Section 10.7, p. 460"); I did not check them against the book. "The argument is Weinberg's" is fair for the propagator fall-off bound; the d_s translation is not his, and the text does not say it is. **REFUTA:** "BBMM record it, without a "folklore" label" is a trace of the correction history (it denies a label no reader has seen) and breaks convention 6. It also uses ASCII `"` quotes, which pdflatex typesets as closing quotes on both sides. Fix: "and BBMM record it in §V of \cite{BBMM2016}". |
| R3 (#9) HL "above M_*" | CONFIRMA | Agrees with ω² = c²k² + ak⁴/M_*² + k⁶/M_*⁴ (l. 512). |
| R4 (#10) entire form factors ≠ Modesto; positivity left open | CONFIRMA | l. 542 and l. 557 now match l. 512 (d_s = 2 family distinct from Modesto's d_s ≤ 4/5). The unsupported positivity claim is gone. |
| R5 (#17) microcausality at E > m_χ, scales < 1/\|Γ_χ\|, Γ_χ < 0, Γ_χ ∝ m_χ³/M_P² ≪ m_χ | CONFIRMA | Matches AP 2018 (abstract, §5 eq. 5.4, §7) as read in Round 1. With a negative constant, "∝" is consistent with Γ_χ < 0. |
| R6 (#26) fakeon gives ξ = 0 and does not fix ℓ_*; ℓ = 1/m_χ separate | CONFIRMA | Consistent with l. 612 (massless branch ξ = 0; ξ ≠ 0 needs a preferred frame) and with the benchmark ℓ_* = ℓ_P (l. 612-616). The two scales are stated as distinct. |
| R7 (#29) massless pole added | CONFIRMA | z(z²+z+1): d_s = 4/3; bare pair n = 2, d_s = 2 (Round-1 script). |
| R8 (#30) LW and fakeon both give up positivity | CONFIRMA | Stated explicitly, with the prescription as the only difference. |
| R9 (#32) Conjecture with m₂ free; Remark 2: ℓ = ℓ_P vs one-scale | CONFIRMA | Script: N²r(1/4) = 4/3, N²r(1) = 8, N²r(∞) = 12, monotone. m_χ = M_P (non-reduced, 1.22×10¹⁹ GeV, as l. 623 uses it) gives M_P/m_φ = 4.47×10⁵ and 1 − N²r/12 = 2.5×10⁻¹². So the two specializations are mutually exclusive (N²r = 8 vs 12 − 3×10⁻¹¹). Remark 1 on (b) fixing m_χ/m_φ is now correct. The 2.5×10⁻¹² figure is specific to the non-reduced M_P (NC: 6.3×10⁻¹¹ with M_red); the text says "physical Planck mass", consistent with l. 623. |
| #34 "(a limit not constructed here)" | CONFIRMA | Honest flag, consistent with "None of (a)-(c) is attempted here". It remains a programme rather than a sharp statement; that is acceptable for a conjecture. |
| Cross-reference l. 557: "Hořava–Lifshitz z = 3 completion (\eqref{eq:graviton_dispersion} above)" | INCERTO (minor, new) | `graviton_dispersion` is at l. 609, *below*, and it is the ξ-ansatz, not the z = 3 operator (that is at l. 512, and the z = 3 branch is discussed at l. 612). Suggest "(Section~\ref{sec:analytical_solutions}; see also the $z=3$ branch below \eqref{eq:graviton_dispersion})". |
| No overclaim; house style otherwise; consistency with ch. 12 | CONFIRMA | The fakeon is conditional; the Conjecture is labelled; the Euclidean heat-kernel formula remains the proved core ("unchanged", l. 544, l. 562); ℓ_* = ℓ_P is kept as the benchmark (l. 555, l. 612). Apart from "folklore", grep finds no "corrected/earlier/withdrawn/version" and no audit paths. |
| Build gate | CONFIRMA | Temp copy (snapshot of `build_pdfs_safe`, own driver, no PDF copied back), pdflatex ×3. Ch. 12: 0 errors, 0 warnings, 0 overfull boxes, 0 undefined references. Master with the fresh ch. 12 PDF: the same counts, 197 pp. |

**Remaining action (for an independent corrector):** delete ', without a "folklore" label,' at l. 542. Optional: liminf wording in `kl_bound`, and fix the l. 557 cross-reference.
