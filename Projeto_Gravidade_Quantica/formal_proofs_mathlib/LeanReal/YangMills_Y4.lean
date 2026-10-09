import Mathlib.Analysis.Matrix.Order
import Mathlib.Analysis.MeanInequalities
import Mathlib.Analysis.Convex.SpecificFunctions.Basic

/-!
# Yang–Mills paper (Zenodo concept DOI 10.5281/zenodo.22301093), item Y4

Source: `Manuscritos_Avulsos/paper_yang_mills_mass_gap/paper_yang_mills_mass_gap.tex`,
Lemma `lem:gz_convex` ("Convexity of the Gribov–Zwanziger additions; Galerkin truncations"), (b).

Paper:
> (a) `M_N(A)` is symmetric and `A ↦ M_N(A) = M_N(0) + L(A)` is affine, with `L` linear; hence
>     `Ω_N` is an open convex set containing `0`;
> (b) `−log det M_N` is convex on `Ω_N`, strictly convex if and only if `L` is injective, and tends
>     to `+∞` at `∂Ω_N`.
(`Ω_N = {A ∈ V_N : M_N(A) > 0}`, `V_N` finite-dimensional, `M_N(A)` a real symmetric matrix.)

Mathlib (revision of 2026-09-19) has no concavity of `log det` on the positive-definite cone, and
no Minkowski determinant inequality (searched: `logDet`, `log_det`, `Real.log` with `det`).
It is proved here.

Formal version:
* `det_geom_le` : for real positive-definite `A`, `B` and `t ∈ [0,1]`,
  `det A^{1−t} · det B^t ≤ det((1−t)A + tB)`.
  Proof: `S = √A` (Mathlib's `CFC.sqrt`), `C = S⁻¹BS⁻¹ ≻ 0`, `(1−t)A + tB = S((1−t)I + tC)S`,
  spectral theorem for `C`, and the weighted AM–GM `μ^t ≤ (1−t) + tμ` for each eigenvalue.
  (The paper argues by the second derivative along lines; the route here is different but proves
  the same convexity.)
* `det_geom_lt` : strict inequality when `A ≠ B` and `0 < t < 1`.
* `neg_log_det_convexOn`, `neg_log_det_strictConvexOn` : `−log det` is (strictly) convex on the
  cone `{A | A.PosDef}`.
* `gz_convex_b` : the Galerkin form of (b), convexity part: for any real vector space `V`, any
  matrix `M₀` and any linear `L : V → Mat`, `x ↦ −log det(M₀ + L x)` is convex on
  `Ω = {x | M₀ + L x ≻ 0}` (and `Ω` is convex).
* `gz_convex_b_strict_iff` : if `M₀ ≻ 0` (i.e. `0 ∈ Ω`, as in the paper), the function is strictly
  convex on `Ω` iff `L` is injective.
REDUCTIONS (declared):
* `M₀` and `L` are arbitrary data: the construction of `M_N` from the Faddeev–Popov operator
  (part (a): symmetry, affinity) is NOT formalized. Symmetry of `M₀ + L x` is not assumed; on `Ω`
  it is part of `PosDef`.
* The boundary behaviour "`−log det M_N → +∞` at `∂Ω_N`" is NOT formalized.
-/

namespace LeanReal.YangMillsY4

open Matrix
open scoped MatrixOrder

set_option autoImplicit false

variable {n : Type*} [Fintype n] [DecidableEq n]

lemma det_unitary_conj {U : Matrix n n ℝ} (hU : U ∈ unitary (Matrix n n ℝ)) (X : Matrix n n ℝ) :
    (U * X * star U).det = X.det := by
  rw [det_mul, det_mul, mul_comm U.det, mul_assoc, ← det_mul, Unitary.mul_star_self_of_mem hU,
    det_one, mul_one]

/-- Spectral step: for `C ≻ 0` there are a unitary `U` and eigenvalues `μ_i > 0` with
`(1−t)I + tC = U diag((1−t) + tμ_i) Uᴴ` and `det C = ∏ μ_i`. -/
lemma spectral_data (C : Matrix n n ℝ) (hC : C.PosDef) :
    ∃ (U : Matrix n n ℝ) (μ : n → ℝ), U ∈ unitary (Matrix n n ℝ) ∧ (∀ i, 0 < μ i) ∧
      C = U * diagonal μ * star U := by
  refine ⟨hC.1.eigenvectorUnitary, hC.1.eigenvalues, hC.1.eigenvectorUnitary.2,
    hC.eigenvalues_pos, ?_⟩
  have hspec := hC.1.spectral_theorem
  simp only [Unitary.conjStarAlgAut_apply] at hspec
  have hD : (RCLike.ofReal ∘ hC.1.eigenvalues : n → ℝ) = hC.1.eigenvalues := by
    funext i; simp
  rwa [hD] at hspec

lemma affine_diag {U : Matrix n n ℝ} (hU : U ∈ unitary (Matrix n n ℝ)) (μ : n → ℝ) (t : ℝ) :
    (1 - t) • (1 : Matrix n n ℝ) + t • (U * diagonal μ * star U) =
      U * diagonal (fun i => (1 - t) + t * μ i) * star U := by
  have h1 : U * star U = 1 := Unitary.mul_star_self_of_mem hU
  have hd : diagonal (fun i => (1 - t) + t * μ i) = (1 - t) • (1 : Matrix n n ℝ) + t • diagonal μ := by
    ext i j; by_cases h : i = j <;> simp [diagonal, one_apply, h]
  rw [hd]
  simp only [Matrix.mul_add, Matrix.add_mul, Matrix.mul_smul, Matrix.smul_mul, Matrix.mul_one, h1]

/-- `det C ^ t ≤ det((1−t)I + tC)` for `C ≻ 0`, `t ∈ [0,1]`; strict if `C ≠ 1` and `0 < t < 1`. -/
lemma det_rpow_le (C : Matrix n n ℝ) (hC : C.PosDef) {t : ℝ} (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    C.det ^ t ≤ ((1 - t) • (1 : Matrix n n ℝ) + t • C).det := by
  obtain ⟨U, μ, hU, hμ, hCeq⟩ := spectral_data C hC
  have hdetC : C.det = ∏ i, μ i := by
    rw [hCeq, det_unitary_conj hU, det_diagonal]
  rw [hdetC, hCeq, affine_diag hU, det_unitary_conj hU, det_diagonal,
    ← Real.finsetProd_rpow _ _ (fun i _ => (hμ i).le)]
  apply Finset.prod_le_prod₀ (fun i _ => Real.rpow_nonneg (hμ i).le _)
  intro i _
  have := Real.geom_mean_le_arith_mean2_weighted (w₁ := 1 - t) (w₂ := t) (p₁ := 1) (p₂ := μ i)
    (by linarith) ht0 zero_le_one (hμ i).le (by ring)
  rwa [Real.one_rpow, one_mul, mul_one] at this

lemma det_rpow_lt (C : Matrix n n ℝ) (hC : C.PosDef) (hC1 : C ≠ 1) {t : ℝ} (ht0 : 0 < t)
    (ht1 : t < 1) : C.det ^ t < ((1 - t) • (1 : Matrix n n ℝ) + t • C).det := by
  obtain ⟨U, μ, hU, hμ, hCeq⟩ := spectral_data C hC
  have hdetC : C.det = ∏ i, μ i := by
    rw [hCeq, det_unitary_conj hU, det_diagonal]
  have hex : ∃ i, μ i ≠ 1 := by
    by_contra h
    push Not at h
    apply hC1
    have : diagonal μ = 1 := by
      ext i j; by_cases hij : i = j <;> simp [diagonal, one_apply, hij, h]
    rw [hCeq, this, Matrix.mul_one, Unitary.mul_star_self_of_mem hU]
  obtain ⟨i₀, hi₀⟩ := hex
  rw [hdetC, hCeq, affine_diag hU, det_unitary_conj hU, det_diagonal,
    ← Real.finsetProd_rpow _ _ (fun i _ => (hμ i).le)]
  apply Finset.prod_lt_prod₀ (fun i _ => Real.rpow_pos_of_pos (hμ i) _)
  · intro i _
    have := Real.geom_mean_le_arith_mean2_weighted (w₁ := 1 - t) (w₂ := t) (p₁ := 1) (p₂ := μ i)
      (by linarith) ht0.le zero_le_one (hμ i).le (by ring)
    rwa [Real.one_rpow, one_mul, mul_one] at this
  · refine ⟨i₀, Finset.mem_univ _, ?_⟩
    have h := rpow_one_add_lt_one_add_mul_self (s := μ i₀ - 1) (by linarith [hμ i₀])
      (sub_ne_zero.mpr hi₀) ht0 ht1
    rw [show 1 + (μ i₀ - 1) = μ i₀ by ring] at h
    linarith

/-- Congruence data: `A = SS`, `B = SCS` with `C ≻ 0`, `S` symmetric, `S = √A`. -/
lemma congr_data {A B : Matrix n n ℝ} (hA : A.PosDef) (hB : B.PosDef) :
    ∃ S C : Matrix n n ℝ, C.PosDef ∧ S * S = A ∧ S * C * S = B := by
  set S := CFC.sqrt A
  have hSS : S * S = A := CFC.sqrt_mul_sqrt_self A hA.posSemidef.nonneg
  have hSh : Sᴴ = S := (CFC.sqrt_nonneg A).posSemidef.isHermitian
  have hdA := hA.det_pos
  have hdS : S.det * S.det = A.det := by rw [← det_mul, hSS]
  have hSne : S.det ≠ 0 := by intro h; rw [h, zero_mul] at hdS; linarith
  have hSu : IsUnit S.det := isUnit_iff_ne_zero.mpr hSne
  have hTS : S⁻¹ * S = 1 := nonsing_inv_mul S hSu
  have hST : S * S⁻¹ = 1 := mul_nonsing_inv S hSu
  have hTh : (S⁻¹)ᴴ = S⁻¹ := by rw [conjTranspose_nonsing_inv, hSh]
  have hTinj : Function.Injective (S⁻¹).mulVec :=
    mulVec_injective_iff_isUnit.mpr ((isUnit_iff_isUnit_det _).mpr (isUnit_nonsing_inv_det S hSu))
  refine ⟨S, S⁻¹ * B * S⁻¹, ?_, hSS, ?_⟩
  · have := hB.conjTranspose_mul_mul_same hTinj
    rwa [hTh] at this
  · simp only [← Matrix.mul_assoc, hST, Matrix.one_mul]
    rw [Matrix.mul_assoc, hTS, Matrix.mul_one]

/-- **Determinant inequality**: `det A^{1−t} det B^t ≤ det((1−t)A + tB)` on the PD cone. -/
theorem det_geom_le {A B : Matrix n n ℝ} (hA : A.PosDef) (hB : B.PosDef) {t : ℝ} (ht0 : 0 ≤ t)
    (ht1 : t ≤ 1) : A.det ^ (1 - t) * B.det ^ t ≤ ((1 - t) • A + t • B).det := by
  obtain ⟨S, C, hC, hSS, hSCS⟩ := congr_data hA hB
  have hdA := hA.det_pos
  have hdB := hB.det_pos
  have hrec : S * ((1 - t) • 1 + t • C) * S = (1 - t) • A + t • B := by
    simp only [Matrix.mul_add, Matrix.add_mul, Matrix.mul_smul, Matrix.smul_mul, Matrix.mul_one,
      hSS, hSCS]
  have hdS : S.det * S.det = A.det := by rw [← det_mul, hSS]
  have hdC : B.det = A.det * C.det := by rw [← hSCS, det_mul, det_mul, ← hdS]; ring
  have hCd : C.det = B.det / A.det := by rw [hdC]; field_simp
  rw [← hrec, det_mul, det_mul]
  have key := det_rpow_le C hC ht0 ht1
  rw [hCd] at key
  calc A.det ^ (1 - t) * B.det ^ t = A.det * (B.det / A.det) ^ t := by
        rw [Real.div_rpow hdB.le hdA.le, Real.rpow_sub hdA, Real.rpow_one]
        have : 0 < A.det ^ t := Real.rpow_pos_of_pos hdA t
        field_simp
    _ ≤ A.det * ((1 - t) • 1 + t • C).det := mul_le_mul_of_nonneg_left key hdA.le
    _ = S.det * ((1 - t) • 1 + t • C).det * S.det := by rw [← hdS]; ring

/-- Strict version: `A ≠ B`, `0 < t < 1`. -/
theorem det_geom_lt {A B : Matrix n n ℝ} (hA : A.PosDef) (hB : B.PosDef) (hAB : A ≠ B) {t : ℝ}
    (ht0 : 0 < t) (ht1 : t < 1) : A.det ^ (1 - t) * B.det ^ t < ((1 - t) • A + t • B).det := by
  obtain ⟨S, C, hC, hSS, hSCS⟩ := congr_data hA hB
  have hC1 : C ≠ 1 := by
    intro h; apply hAB; rw [← hSCS, h, Matrix.mul_one, hSS]
  have hdA := hA.det_pos
  have hdB := hB.det_pos
  have hrec : S * ((1 - t) • 1 + t • C) * S = (1 - t) • A + t • B := by
    simp only [Matrix.mul_add, Matrix.add_mul, Matrix.mul_smul, Matrix.smul_mul, Matrix.mul_one,
      hSS, hSCS]
  have hdS : S.det * S.det = A.det := by rw [← det_mul, hSS]
  have hdC : B.det = A.det * C.det := by rw [← hSCS, det_mul, det_mul, ← hdS]; ring
  have hCd : C.det = B.det / A.det := by rw [hdC]; field_simp
  rw [← hrec, det_mul, det_mul]
  have key := det_rpow_lt C hC hC1 ht0 ht1
  rw [hCd] at key
  calc A.det ^ (1 - t) * B.det ^ t = A.det * (B.det / A.det) ^ t := by
        rw [Real.div_rpow hdB.le hdA.le, Real.rpow_sub hdA, Real.rpow_one]
        have : 0 < A.det ^ t := Real.rpow_pos_of_pos hdA t
        field_simp
    _ < A.det * ((1 - t) • 1 + t • C).det := mul_lt_mul_of_pos_left key hdA
    _ = S.det * ((1 - t) • 1 + t • C).det * S.det := by rw [← hdS]; ring

omit [Fintype n] [DecidableEq n] in
/-- The positive-definite cone is convex. -/
theorem posDef_convex : Convex ℝ {A : Matrix n n ℝ | A.PosDef} := by
  intro A hA B hB a b ha hb hab
  simp only [Set.mem_ofPred_eq] at hA hB ⊢
  rcases ha.eq_or_lt with rfl | ha'
  · rw [zero_add] at hab; subst hab; simpa using hB
  · exact (hA.smul ha').add_posSemidef (hB.posSemidef.smul hb)

/-- `−log det` is convex on the positive-definite cone. -/
theorem neg_log_det_convexOn :
    ConvexOn ℝ {A : Matrix n n ℝ | A.PosDef} (fun A => -Real.log A.det) := by
  refine ⟨posDef_convex, ?_⟩
  intro A hA B hB a b ha hb hab
  simp only [Set.mem_ofPred_eq] at hA hB
  obtain rfl : a = 1 - b := by linarith
  have h := det_geom_le hA hB hb (by linarith)
  have hdA := hA.det_pos
  have hdB := hB.det_pos
  have hpos : 0 < A.det ^ (1 - b) * B.det ^ b :=
    mul_pos (Real.rpow_pos_of_pos hdA _) (Real.rpow_pos_of_pos hdB _)
  have hl := Real.log_le_log hpos h
  rw [Real.log_mul (Real.rpow_pos_of_pos hdA _).ne' (Real.rpow_pos_of_pos hdB _).ne',
    Real.log_rpow hdA, Real.log_rpow hdB] at hl
  simp only [smul_eq_mul]
  linarith

/-- `−log det` is strictly convex on the positive-definite cone. -/
theorem neg_log_det_strictConvexOn :
    StrictConvexOn ℝ {A : Matrix n n ℝ | A.PosDef} (fun A => -Real.log A.det) := by
  refine ⟨posDef_convex, ?_⟩
  intro A hA B hB hAB a b ha hb hab
  simp only [Set.mem_ofPred_eq] at hA hB
  obtain rfl : a = 1 - b := by linarith
  have h := det_geom_lt hA hB hAB hb (by linarith)
  have hdA := hA.det_pos
  have hdB := hB.det_pos
  have hpos : 0 < A.det ^ (1 - b) * B.det ^ b :=
    mul_pos (Real.rpow_pos_of_pos hdA _) (Real.rpow_pos_of_pos hdB _)
  have hl := Real.log_lt_log hpos h
  rw [Real.log_mul (Real.rpow_pos_of_pos hdA _).ne' (Real.rpow_pos_of_pos hdB _).ne',
    Real.log_rpow hdA, Real.log_rpow hdB] at hl
  simp only [smul_eq_mul]
  linarith

section Galerkin

variable {V : Type*} [AddCommGroup V] [Module ℝ V]

omit [Fintype n] [DecidableEq n] in
lemma affine_comb (M₀ : Matrix n n ℝ) (L : V →ₗ[ℝ] Matrix n n ℝ) (x y : V) {a b : ℝ}
    (hab : a + b = 1) : M₀ + L (a • x + b • y) = a • (M₀ + L x) + b • (M₀ + L y) := by
  rw [map_add, map_smul, map_smul, smul_add, smul_add]
  have : M₀ = a • M₀ + b • M₀ := by rw [← add_smul, hab, one_smul]
  conv_lhs => rw [this]
  abel

/-- **Lemma `gz_convex`(b), convexity part** (Galerkin form). -/
theorem gz_convex_b (M₀ : Matrix n n ℝ) (L : V →ₗ[ℝ] Matrix n n ℝ) :
    ConvexOn ℝ {x | (M₀ + L x).PosDef} (fun x => -Real.log (M₀ + L x).det) := by
  refine ⟨?_, ?_⟩
  · intro x hx y hy a b ha hb hab
    simp only [Set.mem_ofPred_eq] at hx hy ⊢
    rw [affine_comb M₀ L x y hab]
    exact posDef_convex hx hy ha hb hab
  · intro x hx y hy a b ha hb hab
    simp only [Set.mem_ofPred_eq] at hx hy
    simp only
    rw [affine_comb M₀ L x y hab]
    exact neg_log_det_convexOn.2 hx hy ha hb hab

/-- **Lemma `gz_convex`(b), strictness**: with `M₀ ≻ 0` (`0 ∈ Ω`), strictly convex iff `L`
injective. -/
theorem gz_convex_b_strict_iff (M₀ : Matrix n n ℝ) (h0 : M₀.PosDef) (L : V →ₗ[ℝ] Matrix n n ℝ) :
    StrictConvexOn ℝ {x | (M₀ + L x).PosDef} (fun x => -Real.log (M₀ + L x).det) ↔
      Function.Injective L := by
  constructor
  · intro hs
    rw [injective_iff_map_eq_zero]
    intro v hv
    by_contra hv0
    have h0' : (0 : V) ∈ {x | (M₀ + L x).PosDef} := by simpa using h0
    have hv' : v ∈ {x | (M₀ + L x).PosDef} := by simpa [hv] using h0
    have := hs.2 h0' hv' (Ne.symm hv0) (by norm_num : (0 : ℝ) < 1 / 2) (by norm_num : (0 : ℝ) < 1 / 2)
      (by norm_num)
    simp [hv, map_smul] at this
    linarith
  · intro hinj
    refine ⟨(gz_convex_b M₀ L).1, ?_⟩
    intro x hx y hy hxy a b ha hb hab
    simp only [Set.mem_ofPred_eq] at hx hy
    simp only
    rw [affine_comb M₀ L x y hab]
    have hne : M₀ + L x ≠ M₀ + L y := fun h => hxy (hinj (add_left_cancel h))
    exact neg_log_det_strictConvexOn.2 hx hy hne ha hb hab

end Galerkin

/-! ### Non-vacuity witness -/

/-- `n = 1`, `V = ℝ`, `M₀ = I`, `L x = x·I`: `Ω = {x > −1}` contains `0` and `1`, and the function
`x ↦ −log(1 + x)` is strictly convex there (`L` is injective). -/
example :
    let L : ℝ →ₗ[ℝ] Matrix (Fin 1) (Fin 1) ℝ := LinearMap.smulRight LinearMap.id 1
    (0 : ℝ) ∈ {x | (1 + L x).PosDef} ∧ (1 : ℝ) ∈ {x | (1 + L x).PosDef} ∧
      StrictConvexOn ℝ {x | (1 + L x).PosDef} (fun x => -Real.log (1 + L x).det) := by
  intro L
  have hL : ∀ x, L x = x • (1 : Matrix (Fin 1) (Fin 1) ℝ) := fun x => rfl
  refine ⟨?_, ?_, (gz_convex_b_strict_iff 1 PosDef.one L).2 ?_⟩
  · simp only [Set.mem_ofPred_eq, hL, zero_smul, add_zero]; exact PosDef.one
  · simp only [Set.mem_ofPred_eq, hL, one_smul]
    have := (PosDef.one (n := Fin 1) (R := ℝ)).smul (a := (2 : ℝ)) (by norm_num)
    rwa [two_smul] at this
  · intro x y h
    have := congrFun (congrFun h 0) 0
    simpa [hL] using this

/-! ### Mutant proved false: `log det` (sign flipped) is convex -/

/-- Mutant: `log det` convex on the PD cone. False for `n = 1`: `A = I`, `B = 4I`, `a = b = 1/2`
gives `log(5/2) ≤ ½ log 4 = log 2`, i.e. `5/2 ≤ 2`. -/
theorem mutant_log_det_convex_false :
    ¬ ConvexOn ℝ {A : Matrix (Fin 1) (Fin 1) ℝ | A.PosDef} (fun A => Real.log A.det) := by
  intro h
  have h1 : (1 : Matrix (Fin 1) (Fin 1) ℝ) ∈ {A : Matrix (Fin 1) (Fin 1) ℝ | A.PosDef} :=
    PosDef.one
  have h4 : ((4 : ℝ) • (1 : Matrix (Fin 1) (Fin 1) ℝ)) ∈ {A : Matrix (Fin 1) (Fin 1) ℝ | A.PosDef} :=
    PosDef.one.smul (by norm_num)
  have := h.2 h1 h4 (by norm_num : (0 : ℝ) ≤ 1 / 2) (by norm_num : (0 : ℝ) ≤ 1 / 2) (by norm_num)
  simp only [smul_eq_mul] at this
  rw [show (1 / 2 : ℝ) • (1 : Matrix (Fin 1) (Fin 1) ℝ) + (1 / 2 : ℝ) • (4 : ℝ) • 1 =
      (5 / 2 : ℝ) • 1 by rw [smul_smul, ← add_smul]; norm_num] at this
  simp only [det_smul, det_one, Fintype.card_fin, pow_one, mul_one, Real.log_one, mul_zero,
    zero_add] at this
  have hlog4 : Real.log 4 = 2 * Real.log 2 := by
    rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.log_pow]; norm_num
  rw [hlog4, show 1 / 2 * (2 * Real.log 2) = Real.log 2 by ring] at this
  have := (Real.log_le_log_iff (by norm_num) (by norm_num)).mp this
  norm_num at this

end LeanReal.YangMillsY4

#print axioms LeanReal.YangMillsY4.det_geom_le
#print axioms LeanReal.YangMillsY4.det_geom_lt
#print axioms LeanReal.YangMillsY4.neg_log_det_convexOn
#print axioms LeanReal.YangMillsY4.neg_log_det_strictConvexOn
#print axioms LeanReal.YangMillsY4.gz_convex_b
#print axioms LeanReal.YangMillsY4.gz_convex_b_strict_iff
#print axioms LeanReal.YangMillsY4.mutant_log_det_convex_false
