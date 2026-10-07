# Version note: *Beyond the Spectrum*, Vol. I (Functional Realizations), 2026-10-06

This is a major revision of Volume I, compared with the text in Zenodo version 2 (2026-09-11), which is also the text in the trilogy record of 2026-09-21. An independent referee report found 5 mathematical errors, 9 gaps or wrong labels, and about 12 wording or citation issues. Every item was checked before any change, the numerical ones with new scripts, and the corrections were then re-checked independently. The results that survive are unchanged in substance; the claims that failed are corrected or withdrawn below.

## Mathematical corrections

1. **Harmonic realization (Construction 3.7).**
   - The identity ‖f_A‖_{L²} = ‖A‖_F was false for n > 1, because the 1/n factor and Lebesgue measure give (2π/n)‖A‖_F.
   - The realization is now f_A = Σ a_{k₁k₂} e^{i k·x} on the torus with the normalized measure dx/(2π)². With that convention the identity is exact.
2. **Dirichlet energy (Theorem 4.1).**
   - The energy formula now matches the convention of item 1.
   - It is also written as ‖DA‖²_F + ‖AD‖²_F, with D = diag(1, …, n).
   - The claim that a ratio Θ(n²) exists for *every* A ≠ 0 was false: for A = I_n and A = J_n every permutation gives ratio 1.
   - The theorem now states that for every n ≥ 2 some symmetric A attains the ratio n², and that n² is the maximum possible ratio.
3. **Checkerboard (Example 4.5).** The energy is (2/3)n⁴ + O(n³), not Θ(n³). The mass is spread over all frequencies, not concentrated at (n, n). The value is the same as for the all-ones matrix, so the harmonic energy does not detect sign oscillation; the total variation does (4(n−1) against 0).
4. **Tensor landscape complexity (Theorem 5.7).**
   - The exponent is ½ log(d−1) (Auffinger–Ben Arous–Černý, CPAM 66 (2013), eq. (2.20)), not Θ(d).
   - That result holds for the isotropic model, with couplings i.i.d. over ordered tuples.
   - The previously stated model, i.i.d. per multiset, is not isotropic. For it only the Cartwright–Sturmfels bound is stated.
   - For d = 2 there are exactly 2n critical points.
5. **De Silva–Lim (§6.4, abstract, Table 1).**
   - Compactness of the product of spheres gives best rank-one approximations only.
   - For rank r ≥ 2 the ill-posedness persists. Remark 5.2 gives an explicit sequence with unit-norm factors and weights of order t.
   - The claim of "circumventing" the pathology is withdrawn.
6. **Critical scaling (Theorem 5.9).**
   - The v2 statement inverted the limits for exponents β ≠ ½.
   - It also gave a k-dependent tail constant; for Gaussian entries the evaluation is exactly N(0,1), with tail 2e^{−dε²/2}.
   - The theorem is now stated for Gaussian entries, with a complete proof and explicit constants 1/√3 ≤ E sup ≤ 2√(2k log(1+4k) + 2 log 2).
   - Sub-Gaussian entries are treated in Remark 5.10.

## Gaps closed or relabelled

- **Theorem 4.7:** sign-saturation step written out.
- **Theorem 4.12:**
  - reduction to indicator functions proved;
  - sharpness of the constant 4 shown;
  - "Grothendieck" removed from the title.
- **Theorem 4.13:**
  - quotient by weak isomorphism;
  - symmetric matrices, rescaled to [0, 1];
  - measurable limit;
  - citation corrected to Lovász–Szegedy, GAFA 17 (2007).
- **Hypergraphon compactness:** no longer a theorem. It is Remark 5.5, a cited sketch (Zhao 2015, §3), and an open problem.
- **Attention bound:** now Proposition 5.6. It needs λ > 0, the constant is explicit, and the bound cannot be uniform in the sequence length. The hallucination claim is removed.
- **Section 6:**
  - learning applications stated as proposals;
  - replica symmetry breaking stated as a conjecture;
  - network "embedding" and "time derivatives" corrected;
  - anisotropic and isotropic total variation distinguished.
- **Classical results named as such:** Proposition 3.3, Theorem 4.9 and Theorem 5.1.
- **Abstract, introduction, Table 1 and conclusion:** rewritten to claim only what is proved. Removed: "unreachable by matrix algebra", "handlebody decompositions" and "paradigm-shifting".

## Other changes

- The "Formal Verification" section is removed. The paper now states that no result is formally verified; the Lean files are a placeholder skeleton without Mathlib.
- Author affiliation updated, CAPES Finance Code 001 acknowledged, and declarations added (funding, competing interests, AI use, verification status, code availability).
- Section titles that overclaimed were renamed:
  - §4 "Emerging Invariants: Spatial, Topological and Asymptotic Quantities". A new opening paragraph says that §4.1–4.2 treat quantities that change under simultaneous permutation of rows and columns, and §4.3–4.4 permutation-invariant ones.
  - §6.4 "Computational Multilinear Algebra: Well-Posed Rank-One Approximation and the De Silva–Lim Pathology".
  - §6.5 "Biomedical Imaging: Hausdorff Perimeters of Level Sets". Its display now restricts the reduced boundary to the open square, as in Theorem 4.8.
- **Abstract, introduction and conclusion:** they no longer list Morse indices and graphon cut distances among quantities that are not permutation-invariant. Dirichlet energy and total variation change under a relabelling of the indices. Morse indices are fixed by the order of the eigenvalues, and the cut distance is invariant under relabelling by construction; both are now described as permutation-invariant readings.
- References added, each DOI resolved via Crossref or DataCite:
  - De Silva–Lim (SIMAX 2008);
  - Hillar–Lim (J. ACM 2013);
  - Lovász–Szegedy (GAFA 2007);
  - Fleming–Rishel (1960);
  - Zhao (RSA 2015);
  - Cartwright–Sturmfels (LAA 2013);
  - Adler–Taylor (2007);
  - Vershynin (2018);
  - the author's monograph (doi:10.5281/zenodo.22290043), which shares most of this material in its Chapter 1.

## Resolved before release (2026-10-07)

- **References:** the bibliography grows from 19 to 56 items. Every DOI, arXiv id and ISBN was resolved; see `audit/references_audit.md` and `audit/scripts/refs_resolve.py`. The only fix to an existing entry is the Adler–Taylor ISBN, which was added. A Related-work paragraph was added, and citations were placed at the claims.
- **Open problem 1 resolved (independent corrector):** confirmed by a separate session: the double sum collapses to Σ_i π(i)² w_i, a linear assignment solved exactly by the rearrangement inequality, not a genuine QAP. Replaced by Proposition 4.3 with proof in §4.1, plus Remark 4.4 explaining why it is not a true QAP; checked against brute force over all n! permutations for n ≤ 8 with a negative control (opposite-direction pairing fails, and no permutation scores below the sorted value), `audit/scripts/verify_op1_sorting.py`. Table 1 and the conclusion's list of proved results updated; item removed from the open-problems list. See `audit/fixes_op1.md`.
- **Declarations (independent corrector):** no longer mention earlier versions; they now say that the Lean 4 files in the author's repository associated with this work are a placeholder skeleton without Mathlib and verify none of the statements. See `audit/fixes_prerelease.md`.
- **Archiving sentence:** now says that DOI 10.5281/zenodo.22644743 is the Zenodo record of the three-volume series.

## Still open

- **Hypergraphon compactness:** the box cut norm case for k ≥ 3 is not written out.
- **Volumes II and III:** corrected separately in the same release.
- **Book Chapter 1:** it should cite this volume in return. The book was not edited here.
- **Scripts:** the numerical check scripts are available from the author on request.
