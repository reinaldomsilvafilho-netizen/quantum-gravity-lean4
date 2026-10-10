import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.ODE.ExistUnique
import Mathlib.Analysis.Calculus.Deriv.Prod
import Mathlib.Topology.Algebra.Module.FiniteDimension
import LeanReal.BeyondSpectrum1_B4

/-!
# Book (Zenodo concept DOI 10.5281/zenodo.22290043), chapter 2, graphon heat equation

Source: `unified_quantum_gravity_book/chap02_geometric_flows_tensor_varieties.tex`,
`thm:graphon_heat_existence` ("Global Well-Posedness and Semigroup Generation") and
`thm:heat_smoothing` ("Cut-Norm Contraction and Decay of Singular Supports").

Book, `thm:graphon_heat_existence`:
> `W₀ ∈ L^∞([0,1]²)`, `d₁(x) = ∫ W₀(x,z) dz`, `d₂(y) = ∫ W₀(z,y) dz`, `m = ∬ W₀`. The equation
> `∂_t W = Δ_⊗ W`, `Δ_⊗ W(x,y) = ∫ (W(x,z) + W(z,y) − 2W(x,y)) dz`, generates a uniformly
> continuous contraction semigroup on `L^p`, with solution
> `W(t) = e^{−2t} W₀ + (e^{−t} − e^{−2t})(d₁ + d₂) + (1 − e^{−t})² m`.
> The coefficients are non-negative and sum to `1` (the middle one counted twice), so `W(t)`
> is a convex combination and takes values in `[0,1]` whenever `W₀` does; `W(t) → m` as
> `t → ∞`.

Book, `thm:heat_smoothing`:
> (i) `‖W(t)‖_□ ≤ ‖W₀‖_□` for all `t ≥ 0`; (ii) `W(t) = e^{−2t} W₀ + K_t[W₀]`, where `K_t[W₀]`
> is continuous whenever the degree functions are, so a jump of `W₀` persists for every `t`
> with amplitude `e^{−2t}`.

## Declared reduction: the FINITE GRID (step-graphon) model

`[0,1]` is replaced by a finite nonempty vertex type `V` with `n = |V|`; the integral
`∫₀¹ f(z) dz` of a step function becomes the average `(1/n) ∑_k f(k)`. So
`P₁W(i,j) = (1/n) ∑_k W(i,k) = d₁(i)`, `P₂W(i,j) = (1/n) ∑_k W(k,j) = d₂(j)`,
`mean W = (1/n²) ∑_{i,j} W(i,j) = m`, and `Δ_⊗ W = P₁W + P₂W − 2W`.
The cut norm is the unnormalised finite one of `BeyondSpectrum1_B4`
(`max_{S,T} |∑_{S×T} W|`); the step-graphon cut norm is `1/n²` times it, so every
inequality below transfers verbatim.

* `heat_hasDerivAt`, `heat_zero`: the closed form solves `W' = Δ_⊗ W`, `W(0) = W₀`.
* `heat_unique`: any global solution of `X' = Δ_⊗ X` with `X(0) = W₀` is the closed form
  (`ODE_solution_unique_univ`; `Δ_⊗` is linear on a finite-dimensional space, hence Lipschitz).
* `heat_heat`: the semigroup law `W(s + t) = e^{tΔ}(W(s))`.
* `coeff_sum`, `coeff_nonneg`, `heat_mem_Icc`: convex combination; values in `[0,1]`.
* `heat_tendsto`: `W(t)(i,j) → m` as `t → ∞` (on a finite grid pointwise = uniform).
* `cutNorm_heat_le`, `cutNorm_heat_antitone`: `thm:heat_smoothing`(i).
* `heat_eq_smul_add_K`, `K_eq_of_deg_eq`, `heat_jump`: `thm:heat_smoothing`(ii), in the
  finite form "`W(t) − e^{−2t}W₀` depends on `(i,j)` only through `(d₁(i), d₂(j))`, so between
  two cells with the same degrees the jump of `W(t)` is exactly `e^{−2t}` times that of `W₀`".

NOT covered: `L^p([0,1]²)`, measurability, the operator-norm bound `‖e^{tΔ}‖ ≤ 1`, uniform
convergence as a statement about `[0,1]²`, and continuity of `K_t[W₀]` (meaningless on a grid).
-/

noncomputable section

namespace LeanReal.Chap02Heat

open Finset Real Set Filter Topology
open LeanReal.BeyondSpectrum1B4 (cutSet cutNorm)

variable {V : Type*} [Fintype V]

/-- `P₁W(i,j) = d₁(i) = (1/n) ∑_k W(i,k)`. -/
def P1 (W : Matrix V V ℝ) : Matrix V V ℝ := Matrix.of fun i _ => (∑ k, W i k) / Fintype.card V

/-- `P₂W(i,j) = d₂(j) = (1/n) ∑_k W(k,j)`. -/
def P2 (W : Matrix V V ℝ) : Matrix V V ℝ := Matrix.of fun _ j => (∑ k, W k j) / Fintype.card V

/-- `m = (1/n²) ∑_{i,j} W(i,j)`. -/
def mean (W : Matrix V V ℝ) : ℝ := (∑ i, ∑ j, W i j) / (Fintype.card V : ℝ) ^ 2

/-- The constant kernel. -/
def const (c : ℝ) : Matrix V V ℝ := Matrix.of fun _ _ => c

/-- `Δ_⊗ W = P₁W + P₂W − 2W`. -/
def lapT (W : Matrix V V ℝ) : Matrix V V ℝ := P1 W + P2 W - (2 : ℝ) • W

/-- The closed form `eq:graphon_heat_exact`. -/
def heat (W0 : Matrix V V ℝ) (t : ℝ) : Matrix V V ℝ :=
  exp (-2 * t) • W0 + (exp (-t) - exp (-2 * t)) • (P1 W0 + P2 W0)
    + (1 - exp (-t)) ^ 2 • const (mean W0)

/-- The "continuous part" `K_t[W₀] = W(t) − e^{−2t} W₀`. -/
def K (W0 : Matrix V V ℝ) (t : ℝ) : Matrix V V ℝ :=
  (exp (-t) - exp (-2 * t)) • (P1 W0 + P2 W0) + (1 - exp (-t)) ^ 2 • const (mean W0)

@[simp] lemma P1_apply (W : Matrix V V ℝ) (i j : V) :
    P1 W i j = (∑ k, W i k) / Fintype.card V := rfl
@[simp] lemma P2_apply (W : Matrix V V ℝ) (i j : V) :
    P2 W i j = (∑ k, W k j) / Fintype.card V := rfl
omit [Fintype V] in
@[simp] lemma const_apply (c : ℝ) (i j : V) : const c i j = c := rfl

lemma lapT_apply (W : Matrix V V ℝ) (i j : V) : lapT W i j = P1 W i j + P2 W i j - 2 * W i j := by
  simp [lapT]

lemma heat_apply (W0 : Matrix V V ℝ) (t : ℝ) (i j : V) :
    heat W0 t i j = exp (-2 * t) * W0 i j + (exp (-t) - exp (-2 * t)) * (P1 W0 i j + P2 W0 i j)
      + (1 - exp (-t)) ^ 2 * mean W0 := by
  simp only [heat, Matrix.add_apply, Matrix.smul_apply, const_apply, smul_eq_mul]

lemma K_apply (W0 : Matrix V V ℝ) (t : ℝ) (i j : V) :
    K W0 t i j = (exp (-t) - exp (-2 * t)) * (P1 W0 i j + P2 W0 i j)
      + (1 - exp (-t)) ^ 2 * mean W0 := by
  simp only [K, Matrix.add_apply, Matrix.smul_apply, const_apply, smul_eq_mul]

/-- `e^{−2t} = (e^{−t})²`, the relation `ring` cannot see. -/
lemma exp_neg_two_mul (t : ℝ) : exp (-2 * t) = exp (-t) ^ 2 := by
  rw [← exp_nat_mul]; congr 1; push_cast; ring

lemma P1_P2 (W : Matrix V V ℝ) : P1 (P2 W) = const (mean W) := by
  ext i j
  simp only [P1_apply, P2_apply, const_apply, mean]
  rw [← sum_div, sum_comm, div_div, sq]

lemma P2_P1 (W : Matrix V V ℝ) : P2 (P1 W) = const (mean W) := by
  ext i j
  simp only [P1_apply, P2_apply, const_apply, mean]
  rw [← sum_div, div_div, sq]

lemma mean_add (A B : Matrix V V ℝ) : mean (A + B) = mean A + mean B := by
  simp [mean, sum_add_distrib, add_div]

lemma mean_smul (c : ℝ) (A : Matrix V V ℝ) : mean (c • A) = c * mean A := by
  simp only [mean, Matrix.smul_apply, smul_eq_mul, ← mul_sum, mul_div_assoc]

lemma heat_zero (W0 : Matrix V V ℝ) : heat W0 0 = W0 := by
  ext i j; simp [heat_apply]

/-! ### Linearity of `P₁`, `P₂` -/

lemma P1_add (A B : Matrix V V ℝ) : P1 (A + B) = P1 A + P1 B := by
  ext i j; simp [P1, sum_add_distrib, add_div]

lemma P2_add (A B : Matrix V V ℝ) : P2 (A + B) = P2 A + P2 B := by
  ext i j; simp [P2, sum_add_distrib, add_div]

lemma P1_smul (c : ℝ) (A : Matrix V V ℝ) : P1 (c • A) = c • P1 A := by
  ext i j
  simp only [P1, Matrix.of_apply, Matrix.smul_apply, smul_eq_mul, ← mul_sum, mul_div_assoc]

lemma P2_smul (c : ℝ) (A : Matrix V V ℝ) : P2 (c • A) = c • P2 A := by
  ext i j
  simp only [P2, Matrix.of_apply, Matrix.smul_apply, smul_eq_mul, ← mul_sum, mul_div_assoc]

/-! ### The algebra of the proof: `P_i² = P_i`, `P₁P₂ = P₂P₁ = m` -/

section Nonempty

variable [Nonempty V]

lemma card_ne_zero : (Fintype.card V : ℝ) ≠ 0 := by
  exact_mod_cast Fintype.card_ne_zero

lemma card_pos : (0 : ℝ) < Fintype.card V := by
  exact_mod_cast Fintype.card_pos

lemma P1_P1 (W : Matrix V V ℝ) : P1 (P1 W) = P1 W := by
  ext i j
  simp only [P1_apply, sum_const, card_univ, nsmul_eq_mul]
  field_simp

lemma P2_P2 (W : Matrix V V ℝ) : P2 (P2 W) = P2 W := by
  ext i j
  simp only [P2_apply, sum_const, card_univ, nsmul_eq_mul]
  field_simp

lemma P1_const (c : ℝ) : P1 (const c : Matrix V V ℝ) = const c := by
  ext i j
  simp only [P1_apply, const_apply, sum_const, card_univ, nsmul_eq_mul]
  field_simp

lemma P2_const (c : ℝ) : P2 (const c : Matrix V V ℝ) = const c := by
  ext i j
  simp only [P2_apply, const_apply, sum_const, card_univ, nsmul_eq_mul]
  field_simp

lemma mean_const (c : ℝ) : mean (const c : Matrix V V ℝ) = c := by
  simp only [mean, const_apply, sum_const, card_univ, nsmul_eq_mul]
  field_simp

lemma mean_P1 (W : Matrix V V ℝ) : mean (P1 W) = mean W := by
  simp only [mean, P1_apply, sum_const, card_univ, nsmul_eq_mul, ← mul_sum, ← sum_div]
  field_simp

lemma mean_P2 (W : Matrix V V ℝ) : mean (P2 W) = mean W := by
  simp only [mean, P2_apply]
  rw [sum_comm]
  simp only [sum_const, card_univ, nsmul_eq_mul, ← mul_sum, ← sum_div]
  rw [sum_comm]
  field_simp

/-- `P₁ W(t) = e^{−t} P₁W₀ + (1 − e^{−t}) m`. -/
lemma P1_heat (W0 : Matrix V V ℝ) (t : ℝ) :
    P1 (heat W0 t) = exp (-t) • P1 W0 + (1 - exp (-t)) • const (mean W0) := by
  simp only [heat, P1_add, P1_smul, P1_P1, P1_P2, P1_const]
  ext i j
  simp only [Matrix.add_apply, Matrix.smul_apply, const_apply, smul_eq_mul, exp_neg_two_mul]
  ring

/-- `P₂ W(t) = e^{−t} P₂W₀ + (1 − e^{−t}) m`. -/
lemma P2_heat (W0 : Matrix V V ℝ) (t : ℝ) :
    P2 (heat W0 t) = exp (-t) • P2 W0 + (1 - exp (-t)) • const (mean W0) := by
  simp only [heat, P2_add, P2_smul, P2_P2, P2_P1, P2_const]
  ext i j
  simp only [Matrix.add_apply, Matrix.smul_apply, const_apply, smul_eq_mul, exp_neg_two_mul]
  ring

/-- The mean is conserved: `m(W(t)) = m(W₀)`. -/
lemma mean_heat (W0 : Matrix V V ℝ) (t : ℝ) : mean (heat W0 t) = mean W0 := by
  simp only [heat, mean_add, mean_smul, mean_P1, mean_P2, mean_const, exp_neg_two_mul]
  ring

/-! ### `thm:graphon_heat_existence`: the closed form solves the equation -/

/-- **`thm:graphon_heat_existence`, closed form**: entrywise, `d/dt W(t)(i,j) = (Δ_⊗ W(t))(i,j)`. -/
theorem heat_hasDerivAt (W0 : Matrix V V ℝ) (t : ℝ) (i j : V) :
    HasDerivAt (fun s => heat W0 s i j) (lapT (heat W0 t) i j) t := by
  have he1 : HasDerivAt (fun s : ℝ => exp (-s)) (-exp (-t)) t := by
    simpa using (hasDerivAt_neg t).exp
  have he2 : HasDerivAt (fun s : ℝ => exp (-2 * s)) (-2 * exp (-2 * t)) t := by
    have := ((hasDerivAt_id t).const_mul (-2 : ℝ)).exp
    simpa [mul_comm] using this
  have h := ((he2.mul_const (W0 i j)).add
      ((he1.sub he2).mul_const (P1 W0 i j + P2 W0 i j))).add
      (((he1.const_sub 1).pow 2).mul_const (mean W0))
  refine (h.congr_of_eventuallyEq (Eventually.of_forall fun s => ?_)).congr_deriv ?_
  · simp [heat_apply]
  · simp only [lapT_apply, P1_heat, P2_heat, heat_apply, Matrix.add_apply, Matrix.smul_apply,
      const_apply, smul_eq_mul, Nat.cast_ofNat]
    ring

/-- The same, as a derivative of the matrix-valued map (sup norm on `V → V → ℝ`). -/
theorem heat_hasDerivAt_pi (W0 : Matrix V V ℝ) (t : ℝ) :
    HasDerivAt (fun s => (heat W0 s : V → V → ℝ)) (lapT (heat W0 t) : V → V → ℝ) t :=
  hasDerivAt_pi.2 fun i => hasDerivAt_pi.2 fun j => heat_hasDerivAt W0 t i j

omit [Nonempty V] in
lemma lapT_apply' (W : Matrix V V ℝ) (i j : V) :
    lapT W i j = (∑ k, W i k) / Fintype.card V + (∑ k, W k j) / Fintype.card V - 2 * W i j := by
  rw [lapT_apply, P1_apply, P2_apply]

omit [Nonempty V] in
lemma lapT_add (A B : Matrix V V ℝ) : lapT (A + B) = lapT A + lapT B := by
  ext i j
  simp only [lapT_apply', Matrix.add_apply, sum_add_distrib, add_div]
  ring

omit [Nonempty V] in
lemma lapT_smul (c : ℝ) (A : Matrix V V ℝ) : lapT (c • A) = c • lapT A := by
  ext i j
  simp only [lapT_apply', Matrix.smul_apply, smul_eq_mul, ← mul_sum, mul_div_assoc]
  ring

/-- `Δ_⊗` as a linear map on `V → V → ℝ`. -/
def lapTₗ : (V → V → ℝ) →ₗ[ℝ] (V → V → ℝ) where
  toFun W := lapT W
  map_add' A B := lapT_add A B
  map_smul' c A := lapT_smul c A

omit [Nonempty V] in
@[simp] lemma lapTₗ_apply (W : V → V → ℝ) : lapTₗ W = lapT W := rfl

/-- **`thm:graphon_heat_existence`, uniqueness**: a global solution `X` of `X' = Δ_⊗ X` with
`X(0) = W₀` is the closed form. (`Δ_⊗` is linear on a finite-dimensional space, hence
Lipschitz; `ODE_solution_unique_univ`.) -/
theorem heat_unique (W0 : Matrix V V ℝ) (X : ℝ → V → V → ℝ)
    (hX : ∀ t, HasDerivAt X (lapT (X t)) t) (h0 : X 0 = W0) :
    ∀ t, X t = heat W0 t := by
  let L : (V → V → ℝ) →L[ℝ] (V → V → ℝ) := LinearMap.toContinuousLinearMap lapTₗ
  have hL : ∀ W, L W = lapT W := fun W => rfl
  have hlip : LipschitzWith (Real.toNNReal ‖L‖) L :=
    AddMonoidHomClass.lipschitz_of_bound L ‖L‖ fun x => L.le_opNorm x
  have := ODE_solution_unique_univ (v := fun _ x => L x) (s := fun _ => univ)
    (fun _ => hlip.lipschitzOnWith) (f := X) (g := fun t => (heat W0 t : V → V → ℝ))
    (fun t => ⟨by show HasDerivAt X (lapT (X t)) t; exact hX t, trivial⟩)
    (fun t => ⟨by
      show HasDerivAt (fun s => (heat W0 s : V → V → ℝ)) (lapT (heat W0 t) : V → V → ℝ) t
      exact heat_hasDerivAt_pi W0 t, trivial⟩)
    (t₀ := 0) (by rw [h0, heat_zero])
  intro t
  exact congrFun this t

/-! ### Semigroup law, convex combination, range, limit -/

/-- The semigroup law `e^{tΔ} e^{sΔ} W₀ = e^{(s+t)Δ} W₀`. -/
theorem heat_heat (W0 : Matrix V V ℝ) (s t : ℝ) : heat (heat W0 s) t = heat W0 (s + t) := by
  have h2 : exp (-(s + t)) = exp (-s) * exp (-t) := by
    rw [← exp_add]; ring_nf
  ext i j
  rw [heat_apply (heat W0 s), P1_heat, P2_heat, mean_heat, heat_apply W0 (s + t),
    heat_apply W0 s]
  simp only [Matrix.add_apply, Matrix.smul_apply, const_apply, smul_eq_mul, exp_neg_two_mul, h2]
  ring

/-- The coefficients sum to `1` (the middle one counted twice). -/
theorem coeff_sum (t : ℝ) :
    exp (-2 * t) + 2 * (exp (-t) - exp (-2 * t)) + (1 - exp (-t)) ^ 2 = 1 := by
  rw [exp_neg_two_mul]; ring

/-- For `t ≥ 0` the coefficients are non-negative. -/
theorem coeff_nonneg {t : ℝ} (ht : 0 ≤ t) :
    0 ≤ exp (-2 * t) ∧ 0 ≤ exp (-t) - exp (-2 * t) ∧ 0 ≤ (1 - exp (-t)) ^ 2 :=
  ⟨(exp_pos _).le, sub_nonneg.2 (exp_le_exp.2 (by linarith)), sq_nonneg _⟩

lemma P1_mem_Icc (W0 : Matrix V V ℝ) (hW : ∀ i j, W0 i j ∈ Icc (0 : ℝ) 1) (i j : V) :
    P1 W0 i j ∈ Icc (0 : ℝ) 1 := by
  rw [P1_apply]
  constructor
  · exact div_nonneg (sum_nonneg fun k _ => (hW i k).1) card_pos.le
  · rw [div_le_one card_pos]
    calc ∑ k, W0 i k ≤ ∑ _k : V, (1 : ℝ) := sum_le_sum fun k _ => (hW i k).2
      _ = Fintype.card V := by simp

lemma P2_mem_Icc (W0 : Matrix V V ℝ) (hW : ∀ i j, W0 i j ∈ Icc (0 : ℝ) 1) (i j : V) :
    P2 W0 i j ∈ Icc (0 : ℝ) 1 := by
  rw [P2_apply]
  constructor
  · exact div_nonneg (sum_nonneg fun k _ => (hW k j).1) card_pos.le
  · rw [div_le_one card_pos]
    calc ∑ k, W0 k j ≤ ∑ _k : V, (1 : ℝ) := sum_le_sum fun k _ => (hW k j).2
      _ = Fintype.card V := by simp

lemma mean_mem_Icc (W0 : Matrix V V ℝ) (hW : ∀ i j, W0 i j ∈ Icc (0 : ℝ) 1) :
    mean W0 ∈ Icc (0 : ℝ) 1 := by
  rw [mean]
  constructor
  · exact div_nonneg (sum_nonneg fun i _ => sum_nonneg fun j _ => (hW i j).1) (sq_nonneg _)
  · rw [div_le_one (pow_pos card_pos 2)]
    calc ∑ i, ∑ j, W0 i j ≤ ∑ _i : V, ∑ _j : V, (1 : ℝ) :=
          sum_le_sum fun i _ => sum_le_sum fun j _ => (hW i j).2
      _ = (Fintype.card V : ℝ) ^ 2 := by simp [sq]

/-- **`thm:graphon_heat_existence`, range**: `W(t)` takes values in `[0,1]` whenever `W₀`
does, for `t ≥ 0`. -/
theorem heat_mem_Icc (W0 : Matrix V V ℝ) (hW : ∀ i j, W0 i j ∈ Icc (0 : ℝ) 1) {t : ℝ}
    (ht : 0 ≤ t) (i j : V) : heat W0 t i j ∈ Icc (0 : ℝ) 1 := by
  obtain ⟨ha, hb, hc⟩ := coeff_nonneg ht
  have hs := coeff_sum t
  obtain ⟨h1, h2⟩ := hW i j
  obtain ⟨h3, h4⟩ := P1_mem_Icc W0 hW i j
  obtain ⟨h5, h6⟩ := P2_mem_Icc W0 hW i j
  obtain ⟨h7, h8⟩ := mean_mem_Icc W0 hW
  rw [heat_apply]
  constructor
  · have := mul_nonneg ha h1
    have := mul_nonneg hb (add_nonneg h3 h5)
    have := mul_nonneg hc h7
    linarith
  · have := mul_le_mul_of_nonneg_left h2 ha
    have := mul_le_mul_of_nonneg_left (add_le_add h4 h6) hb
    have := mul_le_mul_of_nonneg_left h8 hc
    linarith

omit [Nonempty V] in
/-- **`thm:graphon_heat_existence`, limit**: `W(t)(i,j) → m` as `t → ∞`. -/
theorem heat_tendsto (W0 : Matrix V V ℝ) (i j : V) :
    Tendsto (fun t => heat W0 t i j) atTop (𝓝 (mean W0)) := by
  have h1 : Tendsto (fun t : ℝ => exp (-t)) atTop (𝓝 0) := tendsto_exp_neg_atTop_nhds_zero
  have h2 : Tendsto (fun t : ℝ => exp (-2 * t)) atTop (𝓝 0) := by
    have h2t : Tendsto (fun t : ℝ => 2 * t) atTop atTop := tendsto_id.const_mul_atTop two_pos
    have := tendsto_exp_neg_atTop_nhds_zero.comp h2t
    refine this.congr fun t => ?_
    simp
  have key := ((h2.mul_const (W0 i j)).add
      ((h1.sub h2).mul_const (P1 W0 i j + P2 W0 i j))).add
      (((h1.const_sub 1).pow 2).mul_const (mean W0))
  simp only [zero_mul, sub_zero, zero_add, one_pow, one_mul] at key
  refine key.congr fun t => ?_
  rw [heat_apply]

end Nonempty

/-! ### `thm:heat_smoothing`(i): cut-norm contraction -/

section CutNorm

lemma abs_cutSet_le_cutNorm (W : Matrix V V ℝ) (S T : Finset V) :
    |cutSet W S T| ≤ cutNorm W :=
  Finset.le_sup' (fun p : Finset V × Finset V => |cutSet W p.1 p.2|) (mem_univ (S, T))

lemma cutNorm_nonneg (W : Matrix V V ℝ) : 0 ≤ cutNorm W :=
  (abs_nonneg _).trans (abs_cutSet_le_cutNorm W ∅ ∅)

lemma cutNorm_le_iff (W : Matrix V V ℝ) (c : ℝ) :
    cutNorm W ≤ c ↔ ∀ S T : Finset V, |cutSet W S T| ≤ c := by
  unfold cutNorm
  rw [Finset.sup'_le_iff]
  constructor
  · intro h S T; exact h (S, T) (mem_univ _)
  · intro h p _; exact h p.1 p.2

lemma cutSet_P1 (W : Matrix V V ℝ) (S T : Finset V) :
    cutSet (P1 W) S T = ((T.card : ℝ) / Fintype.card V) * cutSet W S univ := by
  simp only [cutSet, P1_apply, sum_const, nsmul_eq_mul]
  rw [mul_sum]
  refine sum_congr rfl fun i _ => ?_
  ring

lemma cutSet_P2 (W : Matrix V V ℝ) (S T : Finset V) :
    cutSet (P2 W) S T = ((S.card : ℝ) / Fintype.card V) * cutSet W univ T := by
  have hR : cutSet W univ T = ∑ j ∈ T, ∑ k, W k j := by
    simp only [cutSet]; exact sum_comm
  rw [hR]
  simp only [cutSet, P2_apply]
  conv_lhs => rw [sum_comm]
  rw [mul_sum]
  simp only [sum_const, nsmul_eq_mul]
  refine sum_congr rfl fun j _ => ?_
  ring

omit [Fintype V] in
lemma cutSet_const (c : ℝ) (S T : Finset V) :
    cutSet (const c : Matrix V V ℝ) S T = (S.card : ℝ) * T.card * c := by
  simp [cutSet, sum_const, nsmul_eq_mul]
  ring

lemma cutSet_heat (W0 : Matrix V V ℝ) (t : ℝ) (S T : Finset V) :
    cutSet (heat W0 t) S T = exp (-2 * t) * cutSet W0 S T
      + (exp (-t) - exp (-2 * t)) * (cutSet (P1 W0) S T + cutSet (P2 W0) S T)
      + (1 - exp (-t)) ^ 2 * cutSet (const (mean W0)) S T := by
  simp only [cutSet, heat_apply, const_apply, sum_add_distrib, ← mul_sum]

variable [Nonempty V]

lemma cutSet_univ_univ (W : Matrix V V ℝ) :
    cutSet W univ univ = (Fintype.card V : ℝ) ^ 2 * mean W := by
  have hn := card_ne_zero (V := V)
  rw [cutSet, mean]
  field_simp

lemma card_div_le_one (S : Finset V) : (S.card : ℝ) / Fintype.card V ≤ 1 := by
  rw [div_le_one card_pos]
  exact_mod_cast Finset.card_le_univ S

lemma abs_cutSet_P1_le (W : Matrix V V ℝ) (S T : Finset V) :
    |cutSet (P1 W) S T| ≤ cutNorm W := by
  rw [cutSet_P1, abs_mul, abs_of_nonneg (div_nonneg (Nat.cast_nonneg _) card_pos.le)]
  calc (T.card : ℝ) / Fintype.card V * |cutSet W S univ|
      ≤ 1 * cutNorm W :=
        mul_le_mul (card_div_le_one T) (abs_cutSet_le_cutNorm W S univ) (abs_nonneg _) zero_le_one
    _ = cutNorm W := one_mul _

lemma abs_cutSet_P2_le (W : Matrix V V ℝ) (S T : Finset V) :
    |cutSet (P2 W) S T| ≤ cutNorm W := by
  rw [cutSet_P2, abs_mul, abs_of_nonneg (div_nonneg (Nat.cast_nonneg _) card_pos.le)]
  calc (S.card : ℝ) / Fintype.card V * |cutSet W univ T|
      ≤ 1 * cutNorm W :=
        mul_le_mul (card_div_le_one S) (abs_cutSet_le_cutNorm W univ T) (abs_nonneg _) zero_le_one
    _ = cutNorm W := one_mul _

lemma abs_cutSet_const_mean_le (W : Matrix V V ℝ) (S T : Finset V) :
    |cutSet (const (mean W) : Matrix V V ℝ) S T| ≤ cutNorm W := by
  have hm : (S.card : ℝ) * T.card * mean W
      = ((S.card : ℝ) / Fintype.card V) * ((T.card : ℝ) / Fintype.card V) * cutSet W univ univ := by
    rw [cutSet_univ_univ]
    field_simp
  rw [cutSet_const, hm, abs_mul, abs_mul,
    abs_of_nonneg (div_nonneg (Nat.cast_nonneg _) card_pos.le),
    abs_of_nonneg (div_nonneg (Nat.cast_nonneg _) card_pos.le)]
  calc (S.card : ℝ) / Fintype.card V * ((T.card : ℝ) / Fintype.card V) * |cutSet W univ univ|
      ≤ 1 * 1 * cutNorm W := by
        gcongr
        · exact card_div_le_one S
        · exact card_div_le_one T
        · exact abs_cutSet_le_cutNorm W univ univ
    _ = cutNorm W := by ring

/-- **`thm:heat_smoothing`(i)**: `‖W(t)‖_□ ≤ ‖W₀‖_□` for `t ≥ 0`. -/
theorem cutNorm_heat_le (W0 : Matrix V V ℝ) {t : ℝ} (ht : 0 ≤ t) :
    cutNorm (heat W0 t) ≤ cutNorm W0 := by
  rw [cutNorm_le_iff]
  intro S T
  rw [cutSet_heat]
  obtain ⟨ha, hb, hc⟩ := coeff_nonneg ht
  have h0 := abs_cutSet_le_cutNorm W0 S T
  have h1 := abs_cutSet_P1_le W0 S T
  have h2 := abs_cutSet_P2_le W0 S T
  have h3 := abs_cutSet_const_mean_le W0 S T
  calc |exp (-2 * t) * cutSet W0 S T
        + (exp (-t) - exp (-2 * t)) * (cutSet (P1 W0) S T + cutSet (P2 W0) S T)
        + (1 - exp (-t)) ^ 2 * cutSet (const (mean W0)) S T|
      ≤ exp (-2 * t) * |cutSet W0 S T|
        + (exp (-t) - exp (-2 * t)) * (|cutSet (P1 W0) S T| + |cutSet (P2 W0) S T|)
        + (1 - exp (-t)) ^ 2 * |cutSet (const (mean W0)) S T| := by
        refine (abs_add_three _ _ _).trans ?_
        rw [abs_mul, abs_mul, abs_mul, abs_of_nonneg ha, abs_of_nonneg hb, abs_of_nonneg hc]
        gcongr
        exact abs_add_le _ _
    _ ≤ exp (-2 * t) * cutNorm W0
        + (exp (-t) - exp (-2 * t)) * (cutNorm W0 + cutNorm W0)
        + (1 - exp (-t)) ^ 2 * cutNorm W0 := by gcongr
    _ = (exp (-2 * t) + 2 * (exp (-t) - exp (-2 * t)) + (1 - exp (-t)) ^ 2) * cutNorm W0 := by
        ring
    _ = cutNorm W0 := by rw [coeff_sum, one_mul]

/-- The cut norm is non-increasing in `t` (semigroup property plus contraction). -/
theorem cutNorm_heat_antitone (W0 : Matrix V V ℝ) {s t : ℝ} (ht : s ≤ t) :
    cutNorm (heat W0 t) ≤ cutNorm (heat W0 s) := by
  have : heat W0 t = heat (heat W0 s) (t - s) := by
    rw [heat_heat, add_sub_cancel]
  rw [this]
  exact cutNorm_heat_le _ (sub_nonneg.2 ht)

end CutNorm

/-! ### `thm:heat_smoothing`(ii): the jump of `W₀` persists with amplitude `e^{−2t}` -/

/-- `W(t) = e^{−2t} W₀ + K_t[W₀]`. -/
theorem heat_eq_smul_add_K (W0 : Matrix V V ℝ) (t : ℝ) :
    heat W0 t = exp (-2 * t) • W0 + K W0 t := by
  ext i j; simp only [heat_apply, K_apply, Matrix.add_apply, Matrix.smul_apply, smul_eq_mul]; ring

/-- `K_t[W₀](i,j)` depends on `(i,j)` only through the degrees `(d₁(i), d₂(j))`: the finite
form of "`K_t[W₀]` is continuous when the degree functions are". -/
theorem K_eq_of_deg_eq (W0 : Matrix V V ℝ) (t : ℝ) {i j i' j' : V}
    (h1 : P1 W0 i j = P1 W0 i' j') (h2 : P2 W0 i j = P2 W0 i' j') :
    K W0 t i j = K W0 t i' j' := by
  rw [K_apply, K_apply, h1, h2]

/-- **`thm:heat_smoothing`(ii)**: between two cells with the same degrees, the jump of `W(t)`
is exactly `e^{−2t}` times the jump of `W₀`; in particular it never vanishes. -/
theorem heat_jump (W0 : Matrix V V ℝ) (t : ℝ) {i j i' j' : V}
    (h1 : P1 W0 i j = P1 W0 i' j') (h2 : P2 W0 i j = P2 W0 i' j') :
    heat W0 t i j - heat W0 t i' j' = exp (-2 * t) * (W0 i j - W0 i' j') := by
  rw [heat_apply, heat_apply, h1, h2]; ring

theorem heat_jump_ne_zero (W0 : Matrix V V ℝ) (t : ℝ) {i j i' j' : V}
    (h1 : P1 W0 i j = P1 W0 i' j') (h2 : P2 W0 i j = P2 W0 i' j') (hW : W0 i j ≠ W0 i' j') :
    heat W0 t i j ≠ heat W0 t i' j' := by
  intro h
  have := heat_jump W0 t h1 h2
  rw [h, sub_self] at this
  exact hW (sub_eq_zero.1 ((mul_eq_zero.1 this.symm).resolve_left (exp_pos _).ne'))

/-! ## Witness: the two-cell grid `V = Fin 2`, `W₀ = [[1,1],[1,0]]`
(non-regular: `d₁ = d₂ = (1, 1/2)`, `m = 3/4`; the middle term of the closed form is
visible). At `t = log 2`: `W(t) = [[15/16, 13/16], [13/16, 7/16]]`, mass `3` conserved. -/

/-- `W₀ = [[1,1],[1,0]]`. -/
def Wex : Matrix (Fin 2) (Fin 2) ℝ := !![1, 1; 1, 0]

lemma Wex_P1 : P1 Wex = !![1, 1; 1 / 2, 1 / 2] := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [Wex, Fin.sum_univ_two]

lemma Wex_P2 : P2 Wex = !![1, 1 / 2; 1, 1 / 2] := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [Wex, Fin.sum_univ_two]

lemma Wex_mean : mean Wex = 3 / 4 := by
  simp [mean, Wex, Fin.sum_univ_two]; norm_num

lemma exp_neg_log_two : exp (-log 2) = 1 / 2 := by
  rw [exp_neg, exp_log two_pos]; norm_num

lemma exp_neg_two_log_two : exp (-2 * log 2) = 1 / 4 := by
  rw [show (-2 : ℝ) * log 2 = -log 2 + -log 2 by ring, exp_add, exp_neg_log_two]; norm_num

/-- `W(log 2) = [[15/16, 13/16], [13/16, 7/16]]`. -/
theorem witness_heat_log_two : heat Wex (log 2) = !![15 / 16, 13 / 16; 13 / 16, 7 / 16] := by
  ext i j
  rw [heat_apply, Wex_P1, Wex_P2, Wex_mean, exp_neg_log_two, exp_neg_two_log_two]
  fin_cases i <;> fin_cases j <;> simp [Wex] <;> norm_num

/-- The hypotheses of `heat_mem_Icc` hold for `Wex` and the conclusion is not trivial:
all four entries of `W(log 2)` lie strictly inside `(0,1)`. -/
example : ∀ i j, heat Wex (log 2) i j ∈ Icc (0 : ℝ) 1 :=
  heat_mem_Icc Wex (fun i j => by fin_cases i <;> fin_cases j <;> simp [Wex]) (log_nonneg one_le_two)

example : heat Wex (log 2) 1 1 = 7 / 16 ∧ (0 : ℝ) < 7 / 16 ∧ (7 / 16 : ℝ) < 1 := by
  rw [witness_heat_log_two]; norm_num

/-- `thm:heat_smoothing`(ii) on the witness: cells `(0,1)` and `(1,1)` have the same column
degree but different row degrees, so the jump lemma needs cells with equal degrees. Cells
`(0,0)` and `(0,1)` share `d₁ = 1` but `d₂` differs. The clean instance is the diagonal
`W₀ = I` below, where all degrees agree. -/
def Wid : Matrix (Fin 2) (Fin 2) ℝ := 1

lemma Wid_P1 (i j : Fin 2) : P1 Wid i j = 1 / 2 := by
  fin_cases i <;> fin_cases j <;> simp [Wid, Matrix.one_apply]

lemma Wid_P2 (i j : Fin 2) : P2 Wid i j = 1 / 2 := by
  fin_cases i <;> fin_cases j <;> simp [Wid, Matrix.one_apply]

/-- For `W₀ = I` the jump between `(0,0)` and `(0,1)` is `e^{−2t}` for every `t`. -/
theorem witness_jump (t : ℝ) : heat Wid t 0 0 - heat Wid t 0 1 = exp (-2 * t) := by
  rw [heat_jump Wid t (by rw [Wid_P1, Wid_P1]) (by rw [Wid_P2, Wid_P2])]
  simp [Wid]

/-! ## Mutants proved false -/

/-- Mutant closed form: the mean-relaxation `e^{−2t} W₀ + (1 − e^{−2t}) m`, which drops the
degree term. It coincides with the true solution for regular `W₀` (constant degrees) but not
in general. -/
def heatMut (W0 : Matrix V V ℝ) (t : ℝ) : Matrix V V ℝ :=
  exp (-2 * t) • W0 + (1 - exp (-2 * t)) • const (mean W0)

/-- Mutant 1: the mean-relaxation form does not solve `W' = Δ_⊗ W` for `W₀ = Wex` (at `t = 0`,
entry `(0,0)`: its derivative is `−1/2`, while `Δ_⊗ W₀(0,0) = 0`). -/
theorem mutant_mean_relaxation_false :
    ¬ ∀ t : ℝ, ∀ i j : Fin 2,
      HasDerivAt (fun s => heatMut Wex s i j) (lapT (heatMut Wex t) i j) t := by
  intro h
  have h1 := h 0 0 0
  have he2 : HasDerivAt (fun s : ℝ => exp (-2 * s)) (-2 * exp (-2 * 0)) 0 := by
    have := ((hasDerivAt_id (0 : ℝ)).const_mul (-2 : ℝ)).exp
    simpa [mul_comm] using this
  have h2 : HasDerivAt (fun s => heatMut Wex s 0 0) (-1 / 2) 0 := by
    have := (he2.mul_const (Wex 0 0)).add ((he2.const_sub 1).mul_const (mean Wex))
    refine (this.congr_of_eventuallyEq (Eventually.of_forall fun s => ?_)).congr_deriv ?_
    · simp [heatMut]
    · rw [Wex_mean]; simp [Wex]; norm_num
  have := h1.unique h2
  rw [lapT_apply] at this
  simp [heatMut, Wex] at this
  norm_num at this

/-- Mutant 2 (drop `t ≥ 0`): for `t = −log 2 < 0` the entry `(1,1)` of `W(t)` is `−5/4`, so the
range `[0,1]` is not preserved backwards in time. -/
theorem mutant_negative_time_false :
    ¬ ∀ t : ℝ, ∀ i j : Fin 2, heat Wex t i j ∈ Icc (0 : ℝ) 1 := by
  intro h
  have h1 := (h (-log 2) 1 1).1
  have e1 : exp (-(-log 2)) = 2 := by rw [neg_neg, exp_log two_pos]
  have e2 : exp (-2 * -log 2) = 4 := by
    rw [show (-2 : ℝ) * -log 2 = log 2 + log 2 by ring, exp_add, exp_log two_pos]; norm_num
  rw [heat_apply, Wex_P1, Wex_P2, Wex_mean, e1, e2] at h1
  simp [Wex] at h1
  norm_num at h1

lemma cutNorm_Wex_le : cutNorm Wex ≤ 3 := by
  rw [cutNorm_le_iff]
  intro S T
  have hS : ∀ f : Fin 2 → ℝ, ∑ i ∈ S, f i = ∑ i, (if i ∈ S then f i else 0) := fun f => by
    rw [Finset.sum_ite_mem, Finset.univ_inter]
  have hT : ∀ f : Fin 2 → ℝ, ∑ j ∈ T, f j = ∑ j, (if j ∈ T then f j else 0) := fun f => by
    rw [Finset.sum_ite_mem, Finset.univ_inter]
  simp only [cutSet]
  rw [hS]
  simp only [hT, Fin.sum_univ_two, Wex]
  by_cases a : (0 : Fin 2) ∈ S <;> by_cases b : (1 : Fin 2) ∈ S <;>
    by_cases c : (0 : Fin 2) ∈ T <;> by_cases d : (1 : Fin 2) ∈ T <;>
    simp [a, b, c, d] <;> norm_num [abs_le]

/-- Mutant 3 (strict contraction `‖W(t)‖_□ < ‖W₀‖_□` for `t > 0`): false. For `W₀ = Wex ≥ 0`
the cut norm is the total mass `3`, which is conserved. -/
theorem mutant_strict_contraction_false :
    ¬ ∀ (W0 : Matrix (Fin 2) (Fin 2) ℝ) (t : ℝ), 0 < t → cutNorm (heat W0 t) < cutNorm W0 := by
  intro h
  have hlt := h Wex (log 2) (log_pos one_lt_two)
  have h3 : (3 : ℝ) ≤ cutNorm (heat Wex (log 2)) := by
    refine le_trans ?_ (abs_cutSet_le_cutNorm _ univ univ)
    rw [witness_heat_log_two]
    simp [cutSet, Fin.sum_univ_two]
    norm_num
  linarith [cutNorm_Wex_le]

end LeanReal.Chap02Heat

#print axioms LeanReal.Chap02Heat.heat_hasDerivAt
#print axioms LeanReal.Chap02Heat.heat_hasDerivAt_pi
#print axioms LeanReal.Chap02Heat.heat_unique
#print axioms LeanReal.Chap02Heat.heat_heat
#print axioms LeanReal.Chap02Heat.coeff_sum
#print axioms LeanReal.Chap02Heat.coeff_nonneg
#print axioms LeanReal.Chap02Heat.heat_mem_Icc
#print axioms LeanReal.Chap02Heat.heat_tendsto
#print axioms LeanReal.Chap02Heat.cutNorm_heat_le
#print axioms LeanReal.Chap02Heat.cutNorm_heat_antitone
#print axioms LeanReal.Chap02Heat.heat_eq_smul_add_K
#print axioms LeanReal.Chap02Heat.K_eq_of_deg_eq
#print axioms LeanReal.Chap02Heat.heat_jump
#print axioms LeanReal.Chap02Heat.heat_jump_ne_zero
#print axioms LeanReal.Chap02Heat.witness_heat_log_two
#print axioms LeanReal.Chap02Heat.witness_jump
#print axioms LeanReal.Chap02Heat.mutant_mean_relaxation_false
#print axioms LeanReal.Chap02Heat.mutant_negative_time_false
#print axioms LeanReal.Chap02Heat.mutant_strict_contraction_false
