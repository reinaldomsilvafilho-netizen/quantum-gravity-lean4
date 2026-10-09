import Mathlib.Analysis.SpecialFunctions.Trigonometric.Inverse
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.LinearAlgebra.UnitaryGroup
import Mathlib.LinearAlgebra.Matrix.Circulant

/-!
# Fermion-mass paper (Zenodo concept DOI 10.5281/zenodo.22373916)

Source: `Manuscritos_Avulsos/paper_standard_model_masses/paper_fermion_mass_hierarchy.tex`.

## Part 1. Proposition `thm:koide_exact` ("Koide ratio of a circulant spectrum")

Paper, Sec. "Charged Leptons: the Koide Relation in Circulant Form":
> Let `v = (v₀,v₁,v₂)` with `v_j = a + 2b cos(δ + 2πj/3)`, `a > 0`, `b ≥ 0`, and write
> `v = v_𝟏 + v_𝟐` with `v_𝟏 = a(1,1,1)` in the trivial representation and `v_𝟐` in the
> trace-zero plane. Then `‖v_𝟏‖² = 3a²`, `‖v_𝟐‖² = 6b²` and
> `Q := ∑ v_j² / (∑ v_j)² = 1/3 + 2b²/(3a²)`.  Consequently
> `Q = 2/3 ⟺ ‖v_𝟐‖² = ‖v_𝟏‖² ⟺ b/a = 1/√2 ⟺ ∠(v,(1,1,1)) = 45°`.

Formal version: `koide_ratio`, `norm_v1`, `norm_v2`, `v2_trace_zero`, `koide_iff_equipartition`,
`koide_iff_ratio`, `koide_iff_angle`.
* The identity holds for every real `b` and `δ` (the paper assumes `b ≥ 0`); `b ≥ 0` is used only
  in `koide_iff_ratio`, where it is needed.
* Vectors in `ℝ³` are functions `Fin 3 → ℝ`; `‖w‖²` is written out as `∑ w_j²`.
* The angle is the Euclidean angle `arccos (⟨v,𝟏⟩ / (‖v‖ ‖𝟏‖))` written out explicitly
  (`angleWithOnes`), with `⟨v,𝟏⟩ = ∑ v_j` and `‖𝟏‖ = √3`; `45°` is `π/4`.
* NOT covered: the physical reading `v_j = √m_j`, the PDG numbers, the `m_τ` prediction.

## Part 2. Remark `rem:dft` (trivial CKM matrix for two circulant sectors)

Paper, Sec. "Circulant Ansatz":
> If the up-type and the down-type mass matrices are both circulant in the same basis, they are
> diagonalized by the same unitary, and the CKM matrix is a permutation matrix up to phases.

Formal version: `ckm_entries_of_commute` and its circulant corollary `ckm_circulant`.
* Hypotheses: `U_u, U_d` unitary with `U_u† C_u U_u = diag d_u`, `U_d† C_d U_d = diag d_d`,
  and the diagonal entries pairwise DISTINCT (non-degenerate spectra). This last hypothesis is not
  written in the remark; without it the diagonalizing unitary, hence `V = U_u† U_d`, is not
  determined, and the claim is false (see the mutant `mutant_ckm_degenerate` below).
* Conclusion: in every column of `V` at most one entry is non-zero, and every entry has modulus
  `0` or `1`. For a unitary matrix this is exactly "a permutation matrix up to phases".
* The DFT matrix of the remark is not used: only `C_u C_d = C_d C_u` is, which holds for
  circulants (`Matrix.circulant_mul_comm`). The theorem is therefore stated for any commuting
  pair, and the circulant case is a corollary.
* NOT covered: the identification of `C` with the root-mass matrix of the Standard Model
  (the paper diagonalizes the Hermitian `C`, with `M = C²`); the standard parametrization of the
  CKM matrix in terms of angles.
-/

namespace LeanReal.Fermions

open Real Finset

/-! ### Part 1: Koide ratio -/

/-- `v_j = a + 2b cos(δ + 2πj/3)`, `j ∈ {0,1,2}`. -/
noncomputable def v (a b δ : ℝ) (j : Fin 3) : ℝ :=
  a + 2 * b * Real.cos (δ + 2 * π * (j : ℕ) / 3)

/-- Trivial-representation component `v_𝟏 = a(1,1,1)`. -/
def v1 (a : ℝ) (_ : Fin 3) : ℝ := a

/-- Trace-zero component `v_𝟐 = v − v_𝟏`. -/
noncomputable def v2 (a b δ : ℝ) (j : Fin 3) : ℝ := v a b δ j - v1 a j

/-- Koide ratio `Q = ∑ v_j² / (∑ v_j)²`. -/
noncomputable def koideQ (w : Fin 3 → ℝ) : ℝ := (∑ j, w j ^ 2) / (∑ j, w j) ^ 2

/-- Angle between `w` and `(1,1,1)`: `arccos (⟨w,𝟏⟩ / (‖w‖ ‖𝟏‖))`. -/
noncomputable def angleWithOnes (w : Fin 3 → ℝ) : ℝ :=
  Real.arccos ((∑ j, w j) / (Real.sqrt (∑ j, w j ^ 2) * Real.sqrt 3))

lemma cos_shift1 (δ : ℝ) :
    Real.cos (δ + 2 * π * ((1 : ℕ) : ℝ) / 3) = -(1/2) * Real.cos δ - (√3 / 2) * Real.sin δ := by
  have h : δ + 2 * π * ((1 : ℕ) : ℝ) / 3 = δ + (π - π / 3) := by push_cast; ring
  rw [h, Real.cos_add, Real.cos_pi_sub, Real.sin_pi_sub, Real.cos_pi_div_three,
    Real.sin_pi_div_three]
  ring

lemma cos_shift2 (δ : ℝ) :
    Real.cos (δ + 2 * π * ((2 : ℕ) : ℝ) / 3) = -(1/2) * Real.cos δ + (√3 / 2) * Real.sin δ := by
  have h : δ + 2 * π * ((2 : ℕ) : ℝ) / 3 = δ + (π / 3 + π) := by push_cast; ring
  rw [h, Real.cos_add, Real.cos_add_pi, Real.sin_add_pi, Real.cos_pi_div_three,
    Real.sin_pi_div_three]
  ring

/-- `∑ v_j = 3a` (from `∑ cos(δ + 2πj/3) = 0`). -/
theorem sum_v (a b δ : ℝ) : ∑ j, v a b δ j = 3 * a := by
  simp only [v, Fin.sum_univ_three, Fin.val_zero, Fin.val_one, Fin.val_two]
  rw [cos_shift1, cos_shift2]
  simp
  ring

/-- `∑ v_j² = 3a² + 6b²` (from `∑ cos²(δ + 2πj/3) = 3/2`). -/
theorem sum_sq_v (a b δ : ℝ) : ∑ j, v a b δ j ^ 2 = 3 * a ^ 2 + 6 * b ^ 2 := by
  simp only [v, Fin.sum_univ_three, Fin.val_zero, Fin.val_one, Fin.val_two]
  rw [cos_shift1, cos_shift2]
  have h3 : (√3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hp := Real.sin_sq_add_cos_sq δ
  simp
  linear_combination (6 * b ^ 2) * hp + (2 * b ^ 2 * (Real.sin δ) ^ 2) * h3

/-- `‖v_𝟏‖² = 3a²`. -/
theorem norm_v1 (a : ℝ) : ∑ j, v1 a j ^ 2 = 3 * a ^ 2 := by
  simp [v1]

/-- `v_𝟐` lies in the trace-zero plane. -/
theorem v2_trace_zero (a b δ : ℝ) : ∑ j, v2 a b δ j = 0 := by
  simp only [v2, Finset.sum_sub_distrib, sum_v]
  simp [v1]

/-- `‖v_𝟐‖² = 6b²`. -/
theorem norm_v2 (a b δ : ℝ) : ∑ j, v2 a b δ j ^ 2 = 6 * b ^ 2 := by
  have e : ∀ j, v2 a b δ j ^ 2 = v a b δ j ^ 2 - 2 * a * v a b δ j + a ^ 2 := by
    intro j; simp only [v2, v1]; ring
  simp only [e, Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum, sum_v,
    sum_sq_v]
  simp; ring

/-- Prop. `thm:koide_exact`, eq. `koide_general`: `Q = 1/3 + 2b²/(3a²)` for `a ≠ 0`. -/
theorem koide_ratio (a b δ : ℝ) (ha : a ≠ 0) :
    koideQ (v a b δ) = 1 / 3 + 2 * b ^ 2 / (3 * a ^ 2) := by
  unfold koideQ
  rw [sum_v, sum_sq_v]
  field_simp
  ring

/-- First equivalence of eq. `norm_equipartition`: `Q = 2/3 ⟺ ‖v_𝟐‖² = ‖v_𝟏‖²`. -/
theorem koide_iff_equipartition (a b δ : ℝ) (ha : 0 < a) :
    koideQ (v a b δ) = 2 / 3 ↔ ∑ j, v2 a b δ j ^ 2 = ∑ j, v1 a j ^ 2 := by
  rw [koide_ratio a b δ ha.ne', norm_v1, norm_v2]
  have ha2 : 0 < a ^ 2 := by positivity
  constructor
  · intro h
    field_simp at h
    linarith
  · intro h
    field_simp
    linarith

/-- Second equivalence: `Q = 2/3 ⟺ b/a = 1/√2` (needs `b ≥ 0`). -/
theorem koide_iff_ratio (a b δ : ℝ) (ha : 0 < a) (hb : 0 ≤ b) :
    koideQ (v a b δ) = 2 / 3 ↔ b / a = 1 / √2 := by
  rw [koide_iff_equipartition a b δ ha, norm_v1, norm_v2]
  have hs : 0 < √2 := by positivity
  have hs2 : √2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  rw [div_eq_div_iff ha.ne' hs.ne']
  constructor
  · intro h
    -- (b√2 − a)(b√2 + a) = 2b² − a² = 0 and b√2 + a > 0
    have hpos : 0 < b * √2 + a := by positivity
    have hprod : (b * √2 - a) * (b * √2 + a) = 0 := by
      have : (b * √2 - a) * (b * √2 + a) = b ^ 2 * √2 ^ 2 - a ^ 2 := by ring
      rw [this, hs2]; linarith
    rcases mul_eq_zero.mp hprod with h1 | h1
    · linarith
    · linarith
  · intro h
    have : (b * √2) ^ 2 = (1 * a) ^ 2 := by rw [h]
    nlinarith [hs2]

/-- Third equivalence: `Q = 2/3 ⟺ ∠(v,(1,1,1)) = 45°`. -/
theorem koide_iff_angle (a b δ : ℝ) (ha : 0 < a) :
    koideQ (v a b δ) = 2 / 3 ↔ angleWithOnes (v a b δ) = π / 4 := by
  unfold angleWithOnes
  rw [sum_v, sum_sq_v, koide_ratio a b δ ha.ne']
  set S := 3 * a ^ 2 + 6 * b ^ 2 with hS
  have hSpos : 0 < S := by positivity
  set r := 3 * a / (√S * √3) with hr
  have hden : 0 < √S * √3 := by positivity
  have hr0 : 0 < r := div_pos (by linarith) hden
  have hr2 : r ^ 2 = 3 * a ^ 2 / S := by
    rw [hr]; simp only [div_pow, mul_pow]
    rw [Real.sq_sqrt hSpos.le, Real.sq_sqrt (by norm_num)]
    field_simp
  have hr1 : r ≤ 1 := by
    have : r ^ 2 ≤ 1 := by
      rw [hr2, div_le_one hSpos]; nlinarith [sq_nonneg b]
    nlinarith
  have hs2 : √2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hs0 : 0 < √2 := by positivity
  have ha2 : 0 < a ^ 2 := by positivity
  -- Q = 2/3 ⟺ r² = 1/2 ⟺ r = √2/2 ⟺ arccos r = π/4
  have step1 : 1 / 3 + 2 * b ^ 2 / (3 * a ^ 2) = 2 / 3 ↔ r = √2 / 2 := by
    constructor
    · intro h
      have hb : 2 * b ^ 2 = a ^ 2 := by field_simp at h; linarith
      have : r ^ 2 = (√2 / 2) ^ 2 := by
        rw [hr2, div_pow, hs2, hS]; field_simp; nlinarith
      have h2 : 0 ≤ √2 / 2 := by positivity
      nlinarith [sq_nonneg (r - √2 / 2), sq_nonneg (r + √2 / 2)]
    · intro h
      have : r ^ 2 = 1 / 2 := by rw [h, div_pow, hs2]; norm_num
      rw [hr2, hS, div_eq_iff hSpos.ne'] at this
      field_simp
      nlinarith
  rw [step1]
  constructor
  · intro h
    rw [h, ← Real.cos_pi_div_four]
    exact Real.arccos_cos (by positivity) (by linarith [Real.pi_pos])
  · intro h
    have := Real.cos_arccos (by linarith : (-1 : ℝ) ≤ r) hr1
    rw [h, Real.cos_pi_div_four] at this
    exact this.symm

/-! Non-vacuity: the Koide value is attained (`a = √2, b = 1`). -/
example : koideQ (v (√2) 1 0) = 2 / 3 := by
  rw [koide_ratio _ _ _ (by positivity), Real.sq_sqrt (by norm_num)]
  norm_num

example : angleWithOnes (v (√2) 1 0) = π / 4 :=
  (koide_iff_angle _ _ _ (by positivity)).mp (by
    rw [koide_ratio _ _ _ (by positivity), Real.sq_sqrt (by norm_num)]; norm_num)

/-- Negative control: replacing `2b²/(3a²)` by `b²/(3a²)` gives a FALSE statement
(`a = b = 1`, `δ = 0`: the true value is `1`, the mutant claims `2/3`). -/
theorem mutant_koide_false :
    ¬ ∀ a b δ : ℝ, 0 < a → koideQ (v a b δ) = 1 / 3 + b ^ 2 / (3 * a ^ 2) := by
  intro h
  have h1 := h 1 1 0 one_pos
  rw [koide_ratio 1 1 0 one_ne_zero] at h1
  norm_num at h1

/-! ### Part 2: CKM matrix of two commuting (e.g. circulant) sectors -/

open Matrix

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- A matrix commuting with a diagonal matrix with distinct entries is diagonal. -/
lemma offdiag_zero_of_commute_diagonal {d : n → ℂ} (hd : Function.Injective d)
    {B : Matrix n n ℂ} (h : diagonal d * B = B * diagonal d) {i j : n} (hij : i ≠ j) :
    B i j = 0 := by
  have := congrFun (congrFun h i) j
  rw [diagonal_mul, mul_diagonal] at this
  have hne : d i - d j ≠ 0 := sub_ne_zero.mpr (fun e => hij (hd e))
  have : (d i - d j) * B i j = 0 := by rw [sub_mul]; rw [this]; ring
  exact (mul_eq_zero.mp this).resolve_left hne

/-- Remark `rem:dft`, general form. If `C_u C_d = C_d C_u` and unitaries `U_u, U_d`
diagonalize them with non-degenerate spectra, then `V = U_u† U_d` has, in each column, at most one
non-zero entry, and every entry has modulus `0` or `1`: `V` is a permutation matrix up to
phases. -/
theorem ckm_entries_of_commute (Cu Cd Uu Ud : Matrix n n ℂ) (du dd : n → ℂ)
    (hUu : Uu ∈ unitaryGroup n ℂ) (hUd : Ud ∈ unitaryGroup n ℂ)
    (hcomm : Cu * Cd = Cd * Cu)
    (hu : star Uu * Cu * Uu = diagonal du) (hd : star Ud * Cd * Ud = diagonal dd)
    (hdu : Function.Injective du) (hdd : Function.Injective dd) :
    (∀ i k j, (star Uu * Ud) i j ≠ 0 → (star Uu * Ud) k j ≠ 0 → i = k) ∧
    (∀ i j, ‖(star Uu * Ud) i j‖ = 0 ∨ ‖(star Uu * Ud) i j‖ = 1) := by
  have uu1 : Uu * star Uu = 1 := mem_unitaryGroup_iff.mp hUu
  have ud1 : Ud * star Ud = 1 := mem_unitaryGroup_iff.mp hUd
  have ud2 : star Ud * Ud = 1 := mem_unitaryGroup_iff'.mp hUd
  set V := star Uu * Ud with hV
  set B := star Ud * Cu * Ud with hB
  -- B commutes with diag dd, hence is diagonal
  have hBcomm : diagonal dd * B = B * diagonal dd := by
    rw [← hd, hB]
    calc star Ud * Cd * Ud * (star Ud * Cu * Ud)
        = star Ud * Cd * (Ud * star Ud) * Cu * Ud := by simp only [Matrix.mul_assoc]
      _ = star Ud * (Cd * Cu) * Ud := by rw [ud1]; simp only [Matrix.mul_one, Matrix.mul_assoc]
      _ = star Ud * (Cu * Cd) * Ud := by rw [hcomm]
      _ = star Ud * Cu * (Ud * star Ud) * Cd * Ud := by
          rw [ud1]; simp only [Matrix.mul_one, Matrix.mul_assoc]
      _ = star Ud * Cu * Ud * (star Ud * Cd * Ud) := by simp only [Matrix.mul_assoc]
  have hBoff : ∀ i j, i ≠ j → B i j = 0 := fun i j h =>
    offdiag_zero_of_commute_diagonal hdd hBcomm h
  -- diag du * V = V * B
  have hDV : diagonal du * V = V * B := by
    rw [← hu, hV, hB]
    calc star Uu * Cu * Uu * (star Uu * Ud)
        = star Uu * Cu * (Uu * star Uu) * Ud := by simp only [Matrix.mul_assoc]
      _ = star Uu * Cu * Ud := by rw [uu1, Matrix.mul_one]
      _ = star Uu * (Ud * star Ud) * Cu * Ud := by
          rw [ud1, Matrix.mul_one]
      _ = star Uu * Ud * (star Ud * Cu * Ud) := by simp only [Matrix.mul_assoc]
  have hentry : ∀ i j, du i * V i j = V i j * B j j := by
    intro i j
    have := congrFun (congrFun hDV i) j
    rw [diagonal_mul, Matrix.mul_apply] at this
    rw [this, Finset.sum_eq_single j]
    · intro k _ hk; rw [hBoff k j hk, mul_zero]
    · intro h; exact absurd (Finset.mem_univ j) h
  have hcol : ∀ i k j, V i j ≠ 0 → V k j ≠ 0 → i = k := by
    intro i k j hi hk
    have e1 : du i = B j j := mul_right_cancel₀ hi (by rw [hentry, mul_comm])
    have e2 : du k = B j j := mul_right_cancel₀ hk (by rw [hentry, mul_comm])
    exact hdu (e1.trans e2.symm)
  refine ⟨hcol, ?_⟩
  -- V is unitary: star V * V = 1, so each column has unit norm
  have hVV : star V * V = 1 := by
    rw [hV, star_mul, star_star]
    calc star Ud * Uu * (star Uu * Ud) = star Ud * (Uu * star Uu) * Ud := by
          simp only [Matrix.mul_assoc]
      _ = 1 := by rw [uu1, Matrix.mul_one, ud2]
  intro i j
  by_cases h0 : V i j = 0
  · left; rw [h0, norm_zero]
  · right
    have hjj := congrFun (congrFun hVV j) j
    rw [Matrix.mul_apply, Matrix.one_apply_eq, Finset.sum_eq_single i] at hjj
    · rw [star_apply, RCLike.star_def, ← Complex.normSq_eq_conj_mul_self] at hjj
      have hn : Complex.normSq (V i j) = 1 := by exact_mod_cast hjj
      rw [← Complex.sq_norm] at hn
      nlinarith [norm_nonneg (V i j)]
    · intro k _ hk
      have : V k j = 0 := by
        by_contra hk0; exact hk (hcol k i j hk0 h0)
      rw [this, mul_zero]
    · intro h; exact absurd (Finset.mem_univ i) h

/-- Remark `rem:dft`, circulant form: both sectors circulant (index `Fin 3`). -/
theorem ckm_circulant (cu cd : Fin 3 → ℂ) (Uu Ud : Matrix (Fin 3) (Fin 3) ℂ) (du dd : Fin 3 → ℂ)
    (hUu : Uu ∈ unitaryGroup (Fin 3) ℂ) (hUd : Ud ∈ unitaryGroup (Fin 3) ℂ)
    (hu : star Uu * circulant cu * Uu = diagonal du)
    (hd : star Ud * circulant cd * Ud = diagonal dd)
    (hdu : Function.Injective du) (hdd : Function.Injective dd) :
    ∀ i j, ‖(star Uu * Ud) i j‖ = 0 ∨ ‖(star Uu * Ud) i j‖ = 1 :=
  (ckm_entries_of_commute _ _ Uu Ud du dd hUu hUd (circulant_mul_comm cu cd) hu hd hdu hdd).2

/-! Non-vacuity and negative control use `n = 2`: `H = (1/√2)[[1,1],[1,−1]]` is unitary and
diagonalizes the circulant `circulant ![0,1] = [[0,1],[1,0]]` with eigenvalues `(1,−1)`. -/

/-- `s = 1/√2` as a complex number. -/
noncomputable def s : ℂ := ((Real.sqrt 2)⁻¹ : ℝ)

lemma s_mul_s : s * s = 1 / 2 := by
  unfold s
  rw [← Complex.ofReal_mul, ← mul_inv, Real.mul_self_sqrt (by norm_num)]
  push_cast; ring

lemma star_s : star s = s := by
  unfold s; rw [RCLike.star_def, Complex.conj_ofReal]

/-- Hadamard matrix `H`. -/
noncomputable def H : Matrix (Fin 2) (Fin 2) ℂ := !![s, s; s, -s]

lemma star_H : star H = H := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [H, star_s]

lemma H_unitary : H ∈ unitaryGroup (Fin 2) ℂ := by
  rw [mem_unitaryGroup_iff, star_H]
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [H, Matrix.mul_apply, Fin.sum_univ_two] <;> rw [s_mul_s] <;> norm_num

lemma circ01 : circulant ![(0 : ℂ), 1] = !![0, 1; 1, 0] := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [circulant_apply]

lemma H_diag : star H * circulant ![(0 : ℂ), 1] * H = diagonal ![1, -1] := by
  rw [star_H, circ01, H, Matrix.mul_fin_two, Matrix.mul_fin_two]
  ext i j; fin_cases i <;> fin_cases j <;> simp <;>
    first | linear_combination 2 * s_mul_s | linear_combination (-2) * s_mul_s

lemma inj_one_neg_one : Function.Injective (![1, -1] : Fin 2 → ℂ) := by
  intro i j h; fin_cases i <;> fin_cases j <;> simp_all <;> norm_num at h

/-- Non-vacuity: all hypotheses of `ckm_entries_of_commute` hold with two circulant sectors
(`C_u = C_d = circulant ![0,1]`, `U_u = U_d = H`). -/
example : ∀ i j, ‖(star H * H) i j‖ = 0 ∨ ‖(star H * H) i j‖ = 1 :=
  (ckm_entries_of_commute _ _ H H _ _ H_unitary H_unitary rfl H_diag H_diag
    inj_one_neg_one inj_one_neg_one).2

lemma norm_s : ‖s‖ = (Real.sqrt 2)⁻¹ := by
  unfold s; rw [Complex.norm_real, Real.norm_eq_abs, abs_of_pos (by positivity)]

/-- Negative control: without the commutation hypothesis the conclusion is FALSE.
`C_u = diag(1,−1)` (`U_u = 1`) and `C_d = [[0,1],[1,0]]` (`U_d = H`) do not commute, and
`V = H` has entries of modulus `1/√2`. -/
theorem mutant_ckm_no_commute :
    ¬ ∀ (Cu Cd Uu Ud : Matrix (Fin 2) (Fin 2) ℂ) (du dd : Fin 2 → ℂ),
      Uu ∈ unitaryGroup (Fin 2) ℂ → Ud ∈ unitaryGroup (Fin 2) ℂ →
      star Uu * Cu * Uu = diagonal du → star Ud * Cd * Ud = diagonal dd →
      Function.Injective du → Function.Injective dd →
      ∀ i j, ‖(star Uu * Ud) i j‖ = 0 ∨ ‖(star Uu * Ud) i j‖ = 1 := by
  intro h
  have := h (diagonal ![1, -1]) (circulant ![0, 1]) 1 H ![1, -1] ![1, -1]
    (one_mem _) H_unitary (by simp) H_diag inj_one_neg_one inj_one_neg_one 0 0
  have hV : (star (1 : Matrix (Fin 2) (Fin 2) ℂ) * H) 0 0 = s := by simp [H]
  rw [hV, norm_s] at this
  have h2 : (1 : ℝ) < Real.sqrt 2 := by
    rw [show (1 : ℝ) = Real.sqrt 1 by simp]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  rcases this with h0 | h1
  · exact absurd h0 (by positivity)
  · have : Real.sqrt 2 = 1 := by
      have := inv_eq_one.mp h1; exact this
    linarith

/-- Negative control: with a DEGENERATE spectrum the conclusion is FALSE even for commuting
(equal, scalar) sectors: `C_u = C_d = 1`, any unitary diagonalizes them. -/
theorem mutant_ckm_degenerate :
    ¬ ∀ (Cu Cd Uu Ud : Matrix (Fin 2) (Fin 2) ℂ) (du dd : Fin 2 → ℂ),
      Uu ∈ unitaryGroup (Fin 2) ℂ → Ud ∈ unitaryGroup (Fin 2) ℂ → Cu * Cd = Cd * Cu →
      star Uu * Cu * Uu = diagonal du → star Ud * Cd * Ud = diagonal dd →
      ∀ i j, ‖(star Uu * Ud) i j‖ = 0 ∨ ‖(star Uu * Ud) i j‖ = 1 := by
  intro h
  have hH1 : star H * 1 * H = diagonal ![1, 1] := by
    rw [Matrix.mul_one, mem_unitaryGroup_iff'.mp H_unitary]
    ext i j; fin_cases i <;> fin_cases j <;> simp
  have hI : star (1 : Matrix (Fin 2) (Fin 2) ℂ) * 1 * 1 = diagonal ![1, 1] := by
    ext i j; fin_cases i <;> fin_cases j <;> simp
  have := h 1 1 1 H ![1, 1] ![1, 1] (one_mem _) H_unitary rfl hI
    hH1 0 0
  have hV : (star (1 : Matrix (Fin 2) (Fin 2) ℂ) * H) 0 0 = s := by simp [H]
  rw [hV, norm_s] at this
  have h2 : (1 : ℝ) < Real.sqrt 2 := by
    rw [show (1 : ℝ) = Real.sqrt 1 by simp]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  rcases this with h0 | h1
  · exact absurd h0 (by positivity)
  · have : Real.sqrt 2 = 1 := inv_eq_one.mp h1
    linarith

end LeanReal.Fermions

#print axioms LeanReal.Fermions.sum_v
#print axioms LeanReal.Fermions.sum_sq_v
#print axioms LeanReal.Fermions.norm_v1
#print axioms LeanReal.Fermions.norm_v2
#print axioms LeanReal.Fermions.v2_trace_zero
#print axioms LeanReal.Fermions.koide_ratio
#print axioms LeanReal.Fermions.koide_iff_equipartition
#print axioms LeanReal.Fermions.koide_iff_ratio
#print axioms LeanReal.Fermions.koide_iff_angle
#print axioms LeanReal.Fermions.mutant_koide_false
#print axioms LeanReal.Fermions.ckm_entries_of_commute
#print axioms LeanReal.Fermions.ckm_circulant
#print axioms LeanReal.Fermions.mutant_ckm_no_commute
#print axioms LeanReal.Fermions.mutant_ckm_degenerate
