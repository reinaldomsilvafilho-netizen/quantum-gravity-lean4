import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.Matrix.ToLin

/-!
# Yang–Mills paper (Zenodo concept DOI 10.5281/zenodo.22301093), item Y5

Source: `Manuscritos_Avulsos/paper_yang_mills_mass_gap/paper_yang_mills_mass_gap.tex`,
Proposition `prop:tight_binding` ("Tight-binding model").

Paper:
> The operator `Ĥ_top = E₀𝟏 − Δ_inst (T̂ + T̂†)`, `Δ_inst > 0`, on `ℓ²(ℤ)` has the generalized
> eigenvectors `|θ⟩ = ∑_n e^{inθ}|n⟩` with eigenvalues `E(θ) = E₀ − 2Δ_inst cos θ`. Its spectrum is
> `[E₀ − 2Δ_inst, E₀ + 2Δ_inst]`.  (`T̂|n⟩ = |n+1⟩`.)

Formal version. REDUCTIONS (declared):
* `gen_eigen_Z` : the generalized-eigenvector identity on `ℤ`, coefficientwise: for
  `ψ(n) = e^{inθ}` (not in `ℓ²`), `E₀ψ(n) − Δ(ψ(n−1) + ψ(n+1)) = (E₀ − 2Δ cos θ) ψ(n)`
  (the coefficient of `|n⟩` in `T̂|θ⟩` is `ψ(n−1)`). Faithful to the paper's proof line.
* `range_E` : the set of values of `E(θ)` is `[E₀ − 2Δ, E₀ + 2Δ]`. The identification of this set
  with the SPECTRUM of `Ĥ_top` on `ℓ²(ℤ)` (Fourier transform `ℓ²(ℤ) → L²(S¹)`, spectrum of a
  multiplication operator) is NOT formalized.
* `ring_eigen` : the FINITE analogue (plan item "anel finito"): on the ring `ℤ/Nℤ` the circulant
  matrix `H = E₀·1 − Δ(T + Tᴴ)` has the eigenvectors `v_k(m) = e^{2πikm/N}` (`v_k ≠ 0`) with
  eigenvalues `E₀ − 2Δ cos(2πk/N)`, for every `N ≥ 1` and every `k`. This finite statement is
  NOT in the paper; it is the plan's finite-dimensional surrogate.
Nothing here says anything about the physical θ-vacuum (paper's Remark "Scope").
-/

namespace LeanReal.YangMillsY5

open Complex Matrix
open scoped Real

set_option autoImplicit false

/-- `E(θ) = E₀ − 2Δ cos θ`. -/
noncomputable def E (E₀ Δ θ : ℝ) : ℝ := E₀ - 2 * Δ * Real.cos θ

/-- Algebraic core: if `a₋ = a e^{-iθ}` and `a₊ = a e^{iθ}`, then
`E₀ a − Δ(a₋ + a₊) = E(θ) a`. -/
lemma eig_step (E₀ Δ θ : ℝ) (a am ap : ℂ) (hm : am = a * exp (-(θ : ℂ) * I))
    (hp : ap = a * exp ((θ : ℂ) * I)) :
    (E₀ : ℂ) * a - Δ * (am + ap) = (E E₀ Δ θ : ℂ) * a := by
  have hc : exp ((θ : ℂ) * I) + exp (-(θ : ℂ) * I) = 2 * Complex.cos θ :=
    (Complex.two_cos (x := (θ : ℂ))).symm
  have hE : ((E E₀ Δ θ : ℝ) : ℂ) = E₀ - 2 * Δ * Complex.cos θ := by
    unfold E; push_cast; ring
  rw [hm, hp, hE]
  linear_combination (-(Δ : ℂ) * a) * hc

/-- Generalized eigenvector identity on `ℤ`. -/
theorem gen_eigen_Z (E₀ Δ θ : ℝ) (n : ℤ) :
    (E₀ : ℂ) * exp (n * θ * I) - Δ * (exp ((n - 1 : ℤ) * θ * I) + exp ((n + 1 : ℤ) * θ * I)) =
      (E E₀ Δ θ : ℂ) * exp (n * θ * I) := by
  apply eig_step
  · rw [← Complex.exp_add]; congr 1; push_cast; ring
  · rw [← Complex.exp_add]; congr 1; push_cast; ring

/-- Values of `E`: `range E = [E₀ − 2Δ, E₀ + 2Δ]` for `Δ > 0`. -/
theorem range_E (E₀ Δ : ℝ) (hΔ : 0 < Δ) :
    Set.range (E E₀ Δ) = Set.Icc (E₀ - 2 * Δ) (E₀ + 2 * Δ) := by
  ext x
  constructor
  · rintro ⟨θ, rfl⟩
    have := Real.neg_one_le_cos θ
    have := Real.cos_le_one θ
    unfold E
    constructor <;> nlinarith
  · rintro ⟨h1, h2⟩
    have hc : (E₀ - x) / (2 * Δ) ∈ Set.range Real.cos := by
      rw [Real.range_cos]
      constructor
      · rw [le_div_iff₀ (by positivity)]; linarith
      · rw [div_le_iff₀ (by positivity)]; linarith
    obtain ⟨θ, hθ⟩ := hc
    refine ⟨θ, ?_⟩
    unfold E
    rw [hθ]
    field_simp
    ring

/-! ### Finite ring `ℤ/Nℤ` -/

variable {N : ℕ} [NeZero N]

/-- Cyclic shift `T e_j = e_{j+1}`: `T i j = 1` iff `i = j + 1`. -/
def T : Matrix (ZMod N) (ZMod N) ℂ := fun i j => if i = j + 1 then 1 else 0

/-- `H = E₀·1 − Δ(T + Tᴴ)`. -/
noncomputable def H (E₀ Δ : ℝ) : Matrix (ZMod N) (ZMod N) ℂ :=
  (E₀ : ℂ) • (1 : Matrix (ZMod N) (ZMod N) ℂ) - (Δ : ℂ) • (T + Tᴴ)

/-- `e(m) = exp(2πi k m / N)` on integers. -/
noncomputable def e (N : ℕ) (k : ℤ) (m : ℤ) : ℂ := exp (2 * π * I * k * m / N)

/-- Eigenvector `v_k(m) = e^{2πikm/N}`. -/
noncomputable def v (k : ℤ) (x : ZMod N) : ℂ := e N k (x.val : ℤ)

lemma e_periodic (k a b : ℤ) (h : (N : ℤ) ∣ b - a) : e N k b = e N k a := by
  obtain ⟨t, ht⟩ := h
  have hN : (N : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr (NeZero.ne N)
  have hb : (b : ℂ) = a + N * t := by
    have : b = a + N * t := by linarith
    rw [this]; push_cast; ring
  unfold e
  rw [hb]
  have : (2 * π * I * k * (a + N * t) / N : ℂ) =
      2 * π * I * k * a / N + ((k * t : ℤ) : ℂ) * (2 * π * I) := by
    push_cast; field_simp
  rw [this, Complex.exp_add, Complex.exp_int_mul_two_pi_mul_I, mul_one]

lemma v_eq (k : ℤ) (x : ZMod N) (z : ℤ) (hz : (z : ZMod N) = x) : v k x = e N k z := by
  unfold v
  apply e_periodic
  exact (ZMod.intCast_eq_intCast_iff_dvd_sub z (x.val : ℤ) N).mp (by
    rw [hz]; push_cast; exact (ZMod.natCast_zmod_val x).symm)

omit [NeZero N] in
lemma e_succ (k m : ℤ) : e N k (m + 1) = e N k m * exp ((2 * π * k / N : ℝ) * I) := by
  unfold e; rw [← Complex.exp_add]; congr 1; push_cast; ring

omit [NeZero N] in
lemma e_pred (k m : ℤ) : e N k (m - 1) = e N k m * exp (-(2 * π * k / N : ℝ) * I) := by
  unfold e; rw [← Complex.exp_add]; congr 1; push_cast; ring

lemma T_mulVec (w : ZMod N → ℂ) (x : ZMod N) : (T *ᵥ w) x = w (x - 1) := by
  simp only [mulVec, dotProduct, T, ite_mul, one_mul, zero_mul]
  rw [Finset.sum_eq_single (x - 1)]
  · simp
  · intro j _ hj
    have : ¬ (x = j + 1) := fun h => hj (by rw [h]; ring)
    simp [this]
  · simp

lemma TH_mulVec (w : ZMod N → ℂ) (x : ZMod N) : (Tᴴ *ᵥ w) x = w (x + 1) := by
  simp only [mulVec, dotProduct, conjTranspose_apply, T]
  rw [Finset.sum_eq_single (x + 1)]
  · simp
  · intro j _ hj; simp [hj]
  · simp

/-- **Finite ring analogue.** `H v_k = (E₀ − 2Δ cos(2πk/N)) v_k` and `v_k ≠ 0`. -/
theorem ring_eigen (E₀ Δ : ℝ) (k : ℤ) :
    H (N := N) E₀ Δ *ᵥ v k = (E E₀ Δ (2 * π * k / N) : ℂ) • v k ∧ v (N := N) k ≠ 0 := by
  refine ⟨?_, ?_⟩
  · funext x
    have hm : v k (x - 1) = v k x * exp (-((2 * π * k / N : ℝ) : ℂ) * I) := by
      rw [v_eq k _ ((x.val : ℤ) - 1) (by push_cast; simp), e_pred]; rfl
    have hp : v k (x + 1) = v k x * exp (((2 * π * k / N : ℝ) : ℂ) * I) := by
      rw [v_eq k _ ((x.val : ℤ) + 1) (by push_cast; simp), e_succ]; rfl
    have hH : (H E₀ Δ *ᵥ v k) x = (E₀ : ℂ) * v k x - Δ * (v k (x - 1) + v k (x + 1)) := by
      simp only [H, sub_mulVec, smul_mulVec, add_mulVec, one_mulVec, Pi.sub_apply,
        Pi.smul_apply, Pi.add_apply, T_mulVec, TH_mulVec, smul_eq_mul]
    rw [hH, Pi.smul_apply, smul_eq_mul]
    exact eig_step E₀ Δ _ _ _ _ hm hp
  · intro h
    have := congrFun h 0
    simp [v, e] at this

#print axioms gen_eigen_Z
#print axioms range_E
#print axioms ring_eigen

/-! ### Non-vacuity witness
`N = 2`, `k = 1`, `E₀ = 0`, `Δ = 1`: the eigenvalue is `−2 cos π = 2`. -/
example : H (N := 2) 0 1 *ᵥ v 1 = ((2 : ℝ) : ℂ) • v 1 ∧ v (N := 2) 1 ≠ 0 := by
  obtain ⟨h1, h2⟩ := ring_eigen (N := 2) 0 1 1
  refine ⟨?_, h2⟩
  have hval : E 0 1 (2 * π * ((1 : ℤ) : ℝ) / ((2 : ℕ) : ℝ)) = 2 := by
    unfold E
    rw [show (2 * π * ((1 : ℤ) : ℝ) / ((2 : ℕ) : ℝ)) = π by push_cast; ring, Real.cos_pi]
    ring
  rw [h1, hval]

/-! ### Mutant proved false
Mutant: eigenvalue `E₀ + 2Δ cos(2πk/N)` (sign flipped). Refuted on `N = 1`, `k = 0`, `E₀ = 0`,
`Δ = 1`: the true eigenvalue is `−2`, and `v_0 ≠ 0`, so `−2 v = 2 v` is impossible. -/
theorem mutant_sign_false :
    ¬ ∀ (E₀ Δ : ℝ) (k : ℤ),
      H (N := 1) E₀ Δ *ᵥ v k = ((E₀ + 2 * Δ * Real.cos (2 * π * k / 1) : ℝ) : ℂ) • v k := by
  intro h
  have hm := h 0 1 0
  obtain ⟨ht, hne⟩ := ring_eigen (N := 1) 0 1 0
  rw [ht] at hm
  have h0 := congrFun hm 0
  norm_num [E, v, e] at h0

#print axioms mutant_sign_false

end LeanReal.YangMillsY5
