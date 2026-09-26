# Final correction and integration pass (2026-09-26)

**Corrector/integrator:** Claude subagent. I did not write the current text or the earlier reports.
**Inputs:** `L2_F45-F50.md` (open items), `L2_residual_2026-09-25.md` §"Rodada 2" (B observations, ch9/ch10), `fixes_F45-F50.md` ("Items left open"), `WORKPLAN.md` rows F-20 and F-51.
**Files edited:** `chap01`, `chap03`, `chap04`, `chap06`, `chap09`, `chap10`, `chap12` (text), `chap02`, `chap04`–`chap06`, `chap08`–`chap13` (bibliography only), `DICTIONARY_TERMS_AND_SYMBOLS.tex`, `master_book_unified_quantum_gravity.tex`. `WORKPLAN.md`, `CHANGELOG.md` and the Lean files were not touched.
**Scripts** (kept in the session scratchpad; `audit/` is read-only for this pass except for this log): `ch06_problem23_KxK.py` (reproduced in full below), `fix_bib.py`, `fix_master.py`, `shorten_dict.py`, `xref.py`, `check_build.py`.

## Table

| File | Item | Source | Assessment | Action |
|---|---|---|---|---|
| chap06 | Problem 2.3: cell-local forms make the problem trivially negative | L2 F-50 item 1 (M) | **Agree.** I reran `scripts/L2_ch06_decimation_remainder_problem.py`: `FAILURES: none`. E_k(1_{F₁K}) = 0 exactly for k = 1…4, while Kigami's renormalized energies of the indicator are 4(5/3)^n. | The forms now integrate over **K×K** with kernel κ_{α_k}(2^k(x−y)) and are defined on L²(K,μ). The paragraph after the problem was rewritten: bounded forms; only pairs at distance O(α_k2^{-k}) interact, and these include neighbouring cells; an explanation of why the cell-local version fails (indicator, 4(5/3)^n, Mosco liminf); the scaling heuristic c_k ≍ ((m+1)(m+3))^k; comparison with Kumagai–Sturm (non-local forms, subsequential Γ-limits); and the two features that keep the question open (convergence of the whole sequence to E_K itself, and the anisotropic support of κ_α, whose symmetry group S_m×Z₂ cannot contain the S_{m+1} of K). New reference: Kumagai–Sturm 2005, DOI 10.1215/kjm/1250281992 (Crossref: title, both authors, vol. 45, no. 2, 2005; Crossref gives no pages, and the pages 307–327 come from the journal). **Check** (`ch06_problem23_KxK.py`, gasket, 7000 μ-samples, α = 0.7, c_k = 15^k): **not trivially false**, since E_k(1_{F₁}) = 0.178, 0.302, 0.461, 0.703, 1.58 for k = 1…5 is > 0 and grows (ratios 1.69, 1.53, 1.53, 2.25, compared with 5/3 for Kigami); the negative control (the old cell-local form) gives exactly 0. **Not trivially true**, since the three harmonic functions h_j have equal Kigami energy 2 but E_k(h_j) differ (spread max/min = 2.03, 1.84, 1.69, 1.58, 1.52 for k = 1…5): identifying the limit with E_K is a real question. The E_k(h_j) stay bounded (0.011–0.033), consistent with the normalization. `FAILURES: none`. |
| chap04 | Rem 2.5(b) "Only for smooth ∂Ω …" is false | L2 F-46 item 3 (B) | **Agree.** On the square and the equilateral triangle, odd reflection shows that the domain of (−Δ_D)² is the Navier H⁴ space. | Restated: equality holds for smooth ∂Ω and also on a rectangle or an equilateral triangle (reflections tile the plane). On a general triangle a corner with π/ω < 3 not an integer carries r^{π/ω}sin(πθ/ω) ∉ H⁴ (Grisvard), so H⁴ fails on a general simplex. The Grisvard domain statement for convex domains and the Navier/clamped distinction are kept. |
| chap01 | §6.4 "singular-vector equations of Lim and Qi" + Qi 2005 | L2 F-47 item 11 (B) | **Agree**; Thm 5.1 already has the right attribution. | "Lim's singular-vector equations~\cite{lim2005singular}". `qi2005eigenvalues` is still cited in Thm 5.1 (Z-eigenvalues), so the bibitem stays. |
| chap09 | No reference for "character of a two-generator group is determined by (tr A, tr B, tr AB)" | L2 residual Rodada 2, 9.1b obs. (B) | **Agree.** | Added "(Fricke; see \cite{goldman2009trace})". Goldman, *Trace coordinates on Fricke spaces of some simple hyperbolic surfaces*, Handbook of Teichmüller Theory II, EMS 2009, pp. 611–684, DOI **10.4171/055-1/16**. Crossref confirms the title, author (Goldman), pages 611–684 and 2009. The nearby DOI 10.4171/055-1/15 is Benedetti–Bonsante, a different chapter, which I checked and rejected. |
| chap10 | 48/72/96 are minima over directions; "loss above ε" | L2 residual Rodada 2, 10.2 obs. (B) | **Agree** (the referee measured 48 to 150 steps over 360 directions at r = 10⁻²). | "need at least about 48, 72 and 96 steps …; these are minima over the direction of the start, and slower directions need more"; "critical points with loss at least ε". |
| chap03 | Rem 7.3: norm of "5.33" unspecified | L2 F-45 obs. (B) | **Agree.** Hand check: since L Cov Lᵀ = Cov, LM₂Lᵀ − M₂ = (α²/m²)(L11ᵀLᵀ − 11ᵀ); for m = 3, α = 4, j = 1, L1 = (−2,1), so the difference is (16/9)[[3,−3],[−3,0]]. The max entry is 16/3 ≈ 5.33 and the spectral norm is (16/9)(3+√45)/2 = (8/3)(1+√5) ≈ 8.63, matching the referee's 5.33 and 8.63. | The Remark now shows the matrix and states both norms. |
| chap03 | Def 1.1 domain excludes y ∈ Z_{<0} but Prop 1.4 has zeros there | L2 F-45 obs. (B) | **Agree.** | Def 1.1: x ∉ {−1,−2,…}, y ∈ C, with the coefficient written as Γ(x+1)·(1/Γ(y+1))·(1/Γ(x−y+1)) using the entire 1/Γ, so it is entire in y and vanishes when y or x−y is a negative integer. The Beta-function form is stated where it is defined. Consistent with Prop 1.4 ("for x ∉ Z_{<0} …"). |
| chap02, 11, 12, 13 | Chapter-1 title in bibliographies = the Zenodo title of *Beyond the Spectrum*, with trilogy DOI 10.5281/zenodo.22699282 | F-48 item 12; F-51; decision delegated by the author | Every use of `silvafilho2026functional` (ch2 l.111, l.505; ch11 l.117; ch12 l.126, 342, 436; ch13 l.56) refers to chapter 1 of this treatise (e.g. its Thm 5.6 and §4 coarea), not to the trilogy. DataCite: 22699282 is a *version* of the trilogy concept record 22644743 ("Beyond the Spectrum: The Complete Three-Volume Monograph …"), so the DOI did not identify chapter 1. | All four entries now read *Functional Realizations of Matrices and Hypertensors: Emergent Invariants and Geometric Measures*, Chapter 1 of *Geometry, Tensors, and Quantum Gravity*, UFLA, 2026, with no trilogy DOI. No passage in the editable files means the trilogy, so "Beyond the Spectrum" and DOI 22644743 appear nowhere. |
| chap02, 04–06, 08–13 | Cross-chapter entries `silvafilho2026*` (24 in total) | F-51 | Mismatches: ch7 cited under an old title in ch8, ch9 and ch10 ("The L^∞ Minimax Extrinsic Curvature Problem …"); ch12 cited as "A Unified Geometric and Algebraic Theory …" in ch11; ch11 cited with "—Established Results…" in ch12 and ch13; the venue varied ("Treatise Chapter NN", "Preprint", or the nonexistent "Treatise on Multilinear Geometry and Quantum Gravity, Vol. 1"). | Rewritten by `fix_bib.py` in one format: R. M. Silva-Filho, *\title of chapter N*, Chapter N of *Geometry, Tensors, and Quantum Gravity*, Universidade Federal de Lavras, 2026. Every title equals the chapter's `\title`, with line breaks removed. |
| master | Chapter titles differ from the chapter files (e.g. ch5 "… Barnes G-Function, and A_{m−1} Lie Algebra", ch11 "… Thermodynamics of Quantum Entanglement", ch7 "… C1,1 Regularity") | F-51; fixes_F45-F50 open item 3 | **Agree**; all 13 differed in the TOC entry, in the heading, or in both. | Each `\chapter{…}` is now the exact `\title` of its file (TOC and heading), with a short `\chaptermark` for running heads. The part pages (`\part` titles only) and the Dictionary chapter were checked and need no change; there is no other chapter list. The preface's `audit/scripts/` path was replaced by "the auxiliary checking scripts of the repository" (house style); the same change was made in the Dictionary. |
| chap12 | Kac–Rice rate "exp(Nθ(k))" | F-51; fixes_F45-F50 open 2 | **Agree.** | Now: for the isotropic model with i.i.d. Gaussian couplings, (1/N)log E[N_crit] → θ(k) = ½log(k−1) for k ≥ 3 (Auffinger–Ben Arous–Černý), and exactly 2N critical points for k = 2. `auffinger2013random` was added to the ch12 bibliography (DOI 10.1002/cpa.21422; Crossref: CPAM 66(2), 165–201). The Conj. 7.1 wording (θ(k)) is consistent. |
| chap12 | "I_m(x) = m^x J_m(x)" suggested an oscillatory representation | F-51 | **Agree.** | Now: I_m grows like m^x; with J_m := m^{−x}I_m, Thm 3.2 of Ch. 3 proves J_m → 1 by Laplace's method; a trigonometric integral exists only for J₂ (Thm 2.1 of Ch. 3); for m ≥ 3 the torus integral does not represent I_m. |
| chap12 | "rests on an imported decimation constant" | F-51 | **Agree** (ch6 Prop 2.2 proves r_m = m+3). | Now: "combines the renormalization factor m+3 derived there (Proposition 2.2 of Chapter 6) with the Kigami–Lapidus theorem". |
| all | "Theorem X.Y of Chapter N" and similar references | item 9 | `xref.py` resolved 30 textual cross-chapter references (patterns "T X.Y of Chapter N", "Chapter N, T X.Y", "Ch. N T X.Y", "T X.Y of \cite{…}", "\cite[T X.Y]{…}") against fresh `.aux` files from a scratch compilation. 28 match a label of the same type and number. The other 2 are "Rem. 7.3" of Ch. 3 (in ch4 and the Dictionary), an unlabeled remark; `pdftotext` of the fresh ch3 PDF shows "Remark 7.3 (On the A_{m−1} Gram structure)", which is correct. No stale reference was found. | None needed. |
| chap12, chap13, Dictionary | F-20: forms of d_s and α_t | WORKPLAN F-20 | ch12 and ch13 already agreed algebraically, but ch12 wrote M_P and ch13 wrote M_*. ch12 did not say that d_s(p) is a Padé interpolation rather than the closed form d_s(τ). The Dictionary still had the comoving-k form α_t(k), the obsolete magnitude \|α_t\| ≲ 10⁻¹¹⁵, dispersion delays "10⁻⁶²–10⁻⁶¹ s, 57 orders" (chapters: 6·10⁻⁶²–1.2·10⁻⁶⁰ s, 56–57 orders), and "ξ = 1 in the diffusion model" (ch12: the diffusion model does not fix ξ). | **One form everywhere:** d_s(τ) = −2 d ln P/d ln τ, with the same erfc closed form (ch12 eq. analytical_ds_formula, ch13 eq. ds_tau, Dictionary Box 6); momentum interpolation d_s(p) = 2 + 2/(1+(p/M_*)²), explicitly a two-point Padé form; α_t = ½(d_s(p) − 4) = −(p/M_*)²/(1+(p/M_*)²), with p = H_inf the physical momentum at horizon exit and M_* = M_P in the estimates. ch12 now introduces M_* and the Padé caveat. Dictionary rows α_t, d_s, ξ and Box 7 updated; \|α_t\| ≈ (H_inf/M_P)² ≲ 1.5·10⁻¹¹ (checked: (4.7·10¹³/1.22·10¹⁹)² = 1.48·10⁻¹¹, dimensionless). |
| Dictionary | Entries contradicting corrected chapters | item 11 | Found and checked against the chapter source: (i) Box 1 gave a P.V. singular-kernel definition ∏y_j^{−α}\|y\|^{−(m−1+2α)}, but ch3 Def. 7.1 is a bounded Beta-kernel average of second differences; (ii) "M₂ … (S_m-invariant)" contradicts ch3 Rem 7.3; (iii) the σ row ("yielding A_{m−1} Cartan metric") contradicts the ch3 Gram remark; (iv) the Δ row "H^{2α} → L²" should be a bounded operator on L²; (v) the R and E rows used α where the chapter has γ, and the E domain was wrong (ch5 Thm: H^t → H^{t+γ−(n−m)/2}, t < 0); (vi) Box 2 had the wrong Fourier formula (missing constant, kernel outside the integral with the wrong argument), γ ≤ 1 instead of γ = 1, and no inversion; (vii) the Φ_David row said "Stokes theorem" (ch3 Rem 5.2: the additive split is the reason); (viii) the I_m row lacked J_m; (ix) no Kac–Rice entry; (x) Δ_Kigami did not mention Problem 2.3. The g^F row does not contradict ch10 Conj. 3.1. | All corrected against the chapter statements: Box 1 now has the ch3 definition, the S_{m−1}×{±1} invariance, the Gram form only under Σk_j = 0, and the Cartan matrix exactly in the barycentric Hessian (Ch. 12 Prop 2.2); Box 2 has the ch5 definition, the Fourier representation, γ = 1, and the inversion f = F⁻¹[ĥ/K̂(−k)] with its caveats. Added a θ(k) row (½log(k−1), k ≥ 3; 2N for k = 2). Rows were shortened so that the Greek table fits the page (the first compile gave "Float too large" and a 1.6 pt overfull). |

## Build

A scratch compilation (three passes, outside the book folder) of ch1–ch13 and the Dictionary gives 0 errors, 0 LaTeX/Package/Class warnings, 0 overfull boxes and 0 undefined references for every file. **Official build** (`python ../build_pdfs_safe.py`, final run): all 13 chapters, the Dictionary and the master were UPDATED with err=0, warn=0 and overfull=0 (the three non-book targets are also clean). The first official run showed one overfull box in the master (9.5 pt): the ch11 TOC line did not break at "Holonomies,". I fixed it with a hyphenation hint (`Holo\-no\-mies`) in the optional TOC argument only; the printed title text is unchanged. A scratch recompilation of the master shows 0 undefined references.

## Lean vs. book (F-20; the Lean file was not edited)

`formal_proofs_lean4/SpectralDimension.lean` is not consistent with the book:
1. The header gives d_s(k) = 2 + 2/(1 + k/M_P), linear in k/M_P. The book uses (p/M_*)². The Lean rationals (4+2k)/(1+k) and α_t = −k/(1+k) coincide with the book only if the Lean variable k is read as x = (p/M_*)², which the file does not say.
2. `k : Int`, so only integer values of that ratio are covered. The statements are integer identities about numerators and denominators (`omega`), not statements about the real functions.
3. Theorems 4.8 and 4.9 (`ir_heat_kernel_quadratic_cancellation`, `uv_heat_kernel_exact`) are identities that hold for every X and tail_error. They do not involve the erfc closed form d_s(τ) of ch12 and ch13, and 4.9 inserts the UV value 2 by hand (tail_error = −2).
4. The header cites "Chapters 06 & 13" and the paper title "Observational Signatures and Experimental Testbeds of Unified Quantum Gravity". Neither matches: the formula is in ch12 and ch13, and ch13's title is "Observational Signatures of a Running Spectral Dimension: Parametrization and Order-of-Magnitude Assessment". The physical-momentum convention p = H_inf is absent.
The book text is now the single source of truth for F-20. The Lean file needs a separate fix (WORKPLAN F-24/W1).

## Items left open

1. **ch6 Problem 2.3** is open mathematics, as intended. The numerical check shows only that it is neither trivially false nor trivially true.
2. **Lean `SpectralDimension.lean`** is inconsistent with the book in notation and scope (see above). It is not editable in this pass.
3. **Master preface, "Use of generative AI tools":** "These audits found substantive errors … In the present version such errors have been corrected …" is revision-history wording. It is part of the author's COPE disclosure, so I left it for the author to decide.
4. **Kumagai–Sturm pages (307–327)** come from the journal, because the Crossref record has no page field. The DOI, title, authors, volume, issue and year are verified.
5. The `.bak` copies of the chapters and the `DICTIONARY_TERMS_AND_SYMBOLS.md` twin were not updated. The `.md` Dictionary still contains the old 10⁻¹¹⁵ magnitude and/or the "Stokes" wording (grep: 2 hits); it is not a build input.
6. **WORKPLAN.md** rows F-20, F-45–F-51 and the diary need their status updated by the consolidator. Proposed status: F-20 resolved in the book, Lean pending; F-51 resolved; F-47, F-48, F-46, F-50 B/M residues fixed, pending Camada 2 on this pass.

## Script `ch06_problem23_KxK.py` (verbatim)

```python
"""Check of the reformulated ch6 Problem 2.3 (forms over K x K, kernel kappa_alpha(2^k (x-y))).

Gasket m = 2, Cartesian vertices P0=(0,0), P1=(1,0), P2=(1/2, sqrt3/2); mu = self-similar measure,
sampled by random addresses.  E_k(u) = c_k * iint_{KxK} kappa_alpha(2^k (x-y)) |u(x)-u(y)|^2 dmu dmu,
with c_k = ((m+1)(m+3))^k = 15^k and alpha fixed.

T1  no trivial counterexample: E_k(1_{F_1 K}) > 0 and grows with k (ratio near 5/3), consistent with
    Kigami's E_n(1_F1) = 4 (5/3)^n -> infinity.   Negative control: the cell-local form of the old
    statement gives exactly 0 on 1_{F_1 K}.
T2  not trivially true: for the three harmonic functions h_j (boundary data e_j), Kigami's energy is
    the same (=2) by symmetry, but E_k(h_j) are compared; the anisotropic Beta kernel (support in the
    cone y >= 0 and its negative) weighs the three directions differently, so identifying the limit
    with E_K itself is a genuine question.  Also, E_k(h_j) stays bounded (does not blow up like 1_F1).
"""
import math
import numpy as np
from scipy.special import gammaln

rng = np.random.default_rng(12345)
P = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, math.sqrt(3) / 2]])
N, depth = 7000, 22
W = rng.integers(0, 3, size=(N, depth))
X = np.zeros((N, 2))
for j in range(depth - 1, -1, -1):
    X = 0.5 * X + 0.5 * P[W[:, j]]


def harmonic(v):
    vals = np.tile(np.asarray(v, float), (N, 1))
    for j in range(depth):
        i = W[:, j]
        new = np.empty_like(vals)
        for t in range(3):
            vi = vals[np.arange(N), i]
            vt = vals[:, t]
            vl = vals.sum(axis=1) - vi - vt
            mid = (2 * vi + 2 * vt + vl) / 5
            new[:, t] = np.where(i == t, vi, mid)
        vals = new
    return vals.mean(axis=1)


h = [harmonic(e) for e in np.eye(3)]
ind = (W[:, 0] == 0).astype(float)
alpha = 0.7


def Kbeta(y):
    y1, y2 = y[..., 0], y[..., 1]
    ok = (y1 >= 0) & (y2 >= 0) & (y1 + y2 <= alpha)
    out = np.zeros(y1.shape)
    a, b = y1[ok], y2[ok]
    out[ok] = np.exp(gammaln(alpha + 1) - gammaln(a + 1) - gammaln(b + 1) - gammaln(alpha - a - b + 1))
    return out


def kappa(z):
    return 0.5 * (Kbeta(z) + Kbeta(-z))


funcs = {"1_F1": ind, "h0": h[0], "h1": h[1], "h2": h[2]}
FAIL = []


def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + ("  | " + str(info) if info != "" else ""))
    if not ok:
        FAIL.append(name)


res = {k: {n: 0.0 for n in funcs} for k in range(1, 6)}
loc = {k: 0.0 for k in range(1, 6)}
B = 700
for k in range(1, 6):
    for s in range(0, N, B):
        Z = (2 ** k) * (X[s:s + B, None, :] - X[None, :, :])
        kap = kappa(Z)
        same = np.all(W[s:s + B, None, :k] == W[None, :, :k], axis=2)
        for n, u in funcs.items():
            res[k][n] += np.sum(kap * (u[s:s + B, None] - u[None, :]) ** 2)
        loc[k] += np.sum(same * kap * (ind[s:s + B, None] - ind[None, :]) ** 2)
    for n in funcs:
        res[k][n] *= 15.0 ** k / N ** 2
    print("k=%d  " % k + "  ".join("%s=%.4f" % (n, res[k][n]) for n in funcs) + "  cell-local(1_F1)=%.1e" % loc[k])

e_ind = [res[k]["1_F1"] for k in range(1, 6)]
ratios = [e_ind[i + 1] / e_ind[i] for i in range(4)]
check("T1 E_k(1_F1) > 0 for all k (no trivial counterexample)", all(e > 0 for e in e_ind), [round(e, 4) for e in e_ind])
check("T1 E_k(1_F1) grows geometrically (ratios > 1.3), like Kigami's (5/3)^n", all(r > 1.3 for r in ratios), [round(r, 3) for r in ratios])
check("T1-ctrl cell-local (old) form vanishes on 1_F1", all(loc[k] == 0 for k in loc))
eh = np.array([[res[k][f"h{j}"] for j in range(3)] for k in range(1, 6)])
check("T2 harmonic energies stay bounded (max/min over k < 3)", all(eh[:, j].max() / eh[:, j].min() < 3 for j in range(3)), np.round(eh, 4).tolist())
spread = eh.max(axis=1) / eh.min(axis=1)
print("   anisotropy spread max_j/min_j E_k(h_j):", np.round(spread, 3).tolist())
print("\nFAILURES:", FAIL if FAIL else "none")
```
