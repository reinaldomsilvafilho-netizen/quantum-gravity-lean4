# Version note, 2026-09-25: `paper_fermion_mass_hierarchy.tex`

New title: *An S3-Circulant Parametrization of Fermion Masses and Mixing and a Simplicial Vacuum-Energy Ansatz: Relations, Fits, and Parameter Count*.

This is a correction pass that brings the paper in line with Chapter 12, Section 7 of the monograph *Geometry, Tensors, and Quantum Gravity* (doi:10.5281/zenodo.22290043) as that chapter stands now, and with findings F-04, F-22 and F-42 of the monograph's workplan. Every number is recomputed by `verify_fermion_paper_numbers.py`, which saves its output to `verify_fermion_paper_numbers.out.txt`. The inputs are PDG 2024 (summary tables and CKM review, read from the PDG PDFs) and Planck 2018. Each block of the script checks against an independent oracle and runs a negative control. All checks pass.

Compilation: `pdflatex -interaction=nonstopmode`, run twice. Result: 0 errors, 0 LaTeX/Package/Class warnings, 0 overfull boxes, 9 pages.

## Corrections

| # | Item | Problem | Evidence | Action |
|---|---|---|---|---|
| 1 | Title, abstract | Framed as "geometric framework" with "genuine prediction" of m_tau, a "mechanism" for neutrinos, and a vacuum energy "consistency check" | Items below | Rewrote both. The abstract now says which statements are identities, known relations, fits or predictions, and gives the parameter balance |
| 2 | Intro: "nineteen flavor parameters" | The SM has 19 parameters in total. Its flavor sector has 13 with massless neutrinos, plus at least 7 more for massive neutrinos | Standard count | Corrected the count |
| 3 | Intro: "10^120 orders of magnitude"; M_P^4 ≈ 10^74 GeV^4 | "10^120 orders" is wrong: it is a factor of about 10^120. M_P^4 depends on the convention | M_P^4 = 2.2e76 GeV^4 (G_N^-1/2); reduced 3.5e73; rho_L/M_P^4 = 1.1e-123 to 7.2e-121 (script block 6) | Gave both conventions |
| 4 | Sec. 2: "V = 1 ⊕ 2 topologically dictates three generations" | False. R^n = 1 ⊕ (n-1) holds for every n. Three generations is an input (the choice of Delta_2) | Representation theory | Neutral statement: N_g is an input |
| 5 | Sec. 2: "gauge invariance restricts Yukawa to circulant" | False. Gauge invariance allows any complex 3x3 Yukawa matrix | SM | Circulant form stated as an assumption |
| 6 | Sec. 2: M_l = (v/√2) Y with eigenvalues a+2b cos, used for **root** masses | Inconsistent: the eigenvalues were masses in one place and root masses in another | Algebra | Circulant C now has eigenvalues √m_k. M = C², and Y_circ = (√2/v) C² (still circulant, matching the book's notation) |
| 7 | Circulant ansatz vs. mixing | If Y_u and Y_d are both circulant, one DFT matrix diagonalizes both, so the CKM matrix is trivial. The ansatz cannot give the Cabibbo angle. The old figure caption said it "determines mixing angles" | Algebra | New Remark 2.1. Caption rewritten |
| 8 | Dirac operator on Delta_4 x Delta_2 | Missing. The book uses D⊗1 + γ5⊗M (Chamseddine–Connes–Marcolli). Without γ5 the spectrum is ±\|k\|+m and there is no mass gap | ch12 §7 (F-42 item) | Added the γ5 product and the gap argument. States that boundary conditions are unspecified, as the book does |
| 9 | Thm "Norm equipartition": "circulant orbit condition imposes b/a = 1/√2 … Q = 2/3" | Circular. Q = 1/3 + 2b²/(3a²) holds for every circulant, and every Q in [1/3, 1] occurs. Q = 2/3 is Koide's relation restated as a 45° angle | Script block 1: Q(b/a) for 4 values; identity check; negative control | Turned into a Proposition (an identity, with proof) plus a Status remark. Koide 1982 is cited, as in the book |
| 10 | m_tau "prediction" = 1776.88 MeV, 0.012σ; PDG 1776.86 ± 0.12; K_exp = 0.66666051 | Numbers wrong or outdated. The Koide solution is 1776.969 MeV (brentq and closed form agree). PDG 2024 gives 1776.93 ± 0.09, a pull of +0.43σ. Q_exp = 0.6666645 ± 5.1e-6 | Script block 1 | Corrected. Labelled as Koide's own 1982–83 prediction |
| 11 | Quark ratio Q_q ≈ (2/3)(1+α_s/√3), attributed to "Casimir C_F = 4/3" | No derivation. 1/√3 is not C_F; with C_F the value is 0.700. Scheme dependent: Q_cbt is 0.720 in MS-bar at M_Z and 0.648 with pole masses. The quark triplet was not specified | Script block 2: our 2-loop running gives 0.718, checked against the 4-loop values of Huang–Zhou 2021 | Replaced by the book's wording: a numerical fit with no evidential weight. The triplet is now (c,b,t) |
| 12 | "Theorem: Analytical Cabibbo angle" from a "barycentric projection" | No derivation given. GST is a known 1968 relation. The (1+α_s/4π) factor (0.94%) is ad hoc and about the size of the input error (0.86%). Without the factor, √(m_d/m_s) = 0.2242 ± 0.0019 matches \|V_us\| = 0.22431 better. The old paper quoted \|V_us\| = 0.2243 ± 0.0005; PDG 2024 gives ± 0.00085 | Script block 3 | Replaced the theorem with the known relation and a remark |
| 13 | "Seesaw-free" neutrino mass via R_{3→1} | v²/M is the Weinberg-operator/seesaw scaling, not "seesaw-free". R_{3→1} is not defined in the cited book (Ch. 5 has T_{m→n}, and no neutrino mass). M is a free scale; M = 1.2e15 GeV reproduces m_3 | Script block 5. Dimensions: GeV²/GeV = GeV | Relabelled as a one-parameter order-of-magnitude estimate. Cited Weinberg 1979 |
| 14 | PMNS "isotropic delocalization": sin²θ12 = 1/3, sin²θ23 = 1/2, sinθ13 = sinθC/√2 = 0.159 | Known ansätze (Harrison–Perkins–Scott 2002; King 2012). Against PDG 2024 the pulls are +2.0σ, −2.8σ and +4.5 to +5.1σ. The θ13 relation was left out of the old table | Script block 5 | Stated as known ansätze with their pulls. θ13 marked as disfavored |
| 15 | δ_CP = π/3 + α_s/√3 via "color-shifted orientation" with undefined ε_QCD | Ansatz with no derivation. The circulant phase does not enter the CKM matrix. PDG 2024 fit: δ = 1.147 ± 0.026 rad, so the pull is −1.2σ (the old paper said 65.5 ± 1.5°, 1.1σ) | Script block 4 | Stated as an ansatz |
| 16 | J_CP = 3.08e-5 "exact within 1σ" in the table | Consistency check only. J is proportional to the empirical inputs s23 and s13. PDG 2024 J = 3.12 (+0.13/−0.12)e-5; the model gives 3.09e-5 with PDG 2024 s23 and s13 | Script block 4: oracle is Im of the quartet from the explicit unitary matrix. The F-04 mass formula gives 1.2e-17 GeV^-3 (recorded; it does not appear in this paper) | Relabelled. Added the book's sentence that there is no geometric expression for J |
| 17 | "Simplicial Euler–Maclaurin" identity: Σ(−1)^k C(5,k+1) Vol(Δ_k) M_P^4 ≡ 0 | False. With unit edges the volume-weighted sum is −1.236. It also mixes dimensions | Script block 6 | Removed |
| 18 | Theorem "Exact quartic divergence cancellation" | Uses χ(Δ4) = 1 but then computes a different sum, Σ(−1)^k C(4,k) = 0. The figure writes "Σ_{k=0}^4 … = 1−5+10−10+5−1 ≡ 0", which mixes up χ = 1 and the reduced χ̃ = 0. Nothing derives that zero-point energy is a signed face count | Script block 6 | Kept the identities (χ = 1, χ̃ = 0). Remark 8.1 says they have no physical content by themselves. Figure relabelled and boundary maps renumbered ∂4…∂1 |
| 19 | ρ_Λ = M_P^4 exp(−2π/(α E∞)) "≈ (2.28 meV)^4", α_eff = α_GUT/(Vol·C) ≈ 0.116 ≈ 0.115 | α = 0.115 gives 2.37 meV (with G_N^-1/2), not 2.28. The formula value α = 0.11605 gives 4.49 meV, which is 16× in ρ. Reproducing ρ_Λ needs α = 0.1149, i.e. C = 15.25. d ln ρ/dα ≈ 2.5e3, so a 1% change in α changes ρ by 17×. C_geom has no definition. Observed value: ρ_Λ = (2.239 meV)^4 = 2.52e-47 GeV^4 = 5.8e-30 g/cm³ (the paper had 0.68e-29) | Script block 6: oracle is ρ_c from G_N vs the PDG ρ_c/h² expression. Negative control: E = ln 2 | Relabelled as a one-parameter fit. Numbers corrected |
| 20 | "Master Parameter Table": "Exact", "Exact Order", "Exact (10^-122)" | Overclaims. Fits and inputs were listed as agreements. The θ13 row was missing | All of the above | Replaced by Table 1 (class and pull per observable) and Table 2 (parameter count) |
| 21 | "Formal Verification in Lean 4"; "100% passing rate" | The Lean files do not verify the mathematics. `Book/ChapFermionHierarchy/FermionHierarchy.lean` puts each claim into a structure field (e.g. `h_koide_ratio`) and restates it as a theorem. The "canonical instance" uses the numbers 2000/3000. It has no Mathlib. `BookReal` holds only Chap01 | Direct reading of the files | Section replaced by "Computational Reproducibility", which says nothing has been formally verified |
| 22 | Data availability: DOI 10.5281/zenodo.22441676 | That record is the functorial-bridge paper, which is unrelated | DataCite lookup | Removed. Monograph bibitem title updated to its DataCite title |
| 23 | No conclusion section | — | — | Added a Conclusion that lists open problems |
| 24 | Not present in this paper (checked) | The J_CP mass formula (F-04), m_H = v/2 + Δλ (F-22), and Tr(P)/‖P‖_F² = 2/3 do not occur in this paper | grep | No action. The script records the F-04 value (1.2e-17) and the Higgs fit (Δλ = 0.00428 for m_H = 125.20 GeV) |

New references, each DOI resolved with the Crossref API: Koide 1982 (10.1007/BF02817096); Chamseddine–Connes–Marcolli 2007 (10.4310/ATMP.2007.v11.n6.a3); Harrison–Perkins–Scott 2002 (10.1016/S0370-2693(02)01336-9); King 2012 (10.1016/j.physletb.2012.10.028); Huang–Zhou 2021 (10.1103/PhysRevD.103.016010); Weinberg 1979 (10.1103/PhysRevLett.43.1566). All existing DOIs also resolve with matching metadata.

## Parameter count

| Category | Count | Items |
|---|---|---|
| Free model parameters | 4 | a, δ (lepton circulant); neutrino scale M; α in the vacuum ansatz (or C) |
| Measured inputs | 5 | α_s(M_Z); m_d/m_s; s23; s13; M_P (plus a choice of convention) |
| Discrete choices | ≥ 8 | b/a = 1/√2; factor 1/√3 (used twice); offset π/3; PMNS values 1/3, 1/2, 1/√2; numerator 2π and constant E∞; the (c,b,t) triplet |
| **Observables compared** | **12** | m_e, m_μ, m_τ, Q_cbt, \|V_us\|, δ_CKM, J_CP, m_3, θ12, θ23, θ13, ρ_Λ |
| Used for calibration | 4 | m_e, m_μ, m_3, ρ_Λ |
| Not independent of inputs | 2 | J_CP (∝ s23 s13); Q_cbt (scheme spread 0.65–0.72 exceeds the claimed agreement) |
| Remaining tests | 6 | m_τ +0.4σ and \|V_us\| 0.0σ both pass, and both are known relations (1982–83 and 1968); δ −1.2σ; θ12 +2.0σ; θ23 −2.8σ; θ13 +4.5 to +5.1σ |

Balance: 9 continuous inputs plus at least 8 discrete choices, against 12 observables. After calibration, the only passing tests are the known Koide and GST relations. The one new sharp relation, sin θ13 = sin θC/√2, is disfavored at more than 4σ.

## Items left open

1. There is no derivation of b/a = 1/√2 (Koide) from a dynamical principle.
2. There is no mixing mechanism beyond the circulant ansatz, which gives a trivial CKM matrix.
3. The vacuum energy has no definition of face weights that would make the Δ4 identities a statement about a quantum field. C_geom is undefined.
4. The Dirac operator on the simplex Δ4 needs boundary conditions. As in the book, these are not specified.
5. For the book's agents (read-only here): ch12 §7 writes M_f = (v/√2) Y_circ, and then applies the circulant form a + 2b cos(...) to the root masses. The paper resolves this with M = C²; the book should state which one it means.
6. The script's two-loop running overshoots m_c(M_Z) by 6% against the 4-loop literature. This is tolerated, because Q_cbt changes by only 0.002. A 4-loop implementation (e.g. RunDec) would remove the tolerance.
7. The cover letter, checklist, FOUNDATIONS_*.md and PROOF_AUDIT_FERMIONS_*.md in this folder still contain the old claims. They were not edited (out of scope).
8. Zenodo record 22837696 (v2.0 of this paper) has the old title and claims. This note is intended as its version note.
