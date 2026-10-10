import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Analysis.Complex.RealDeriv
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Topology.Algebra.Module.FiniteDimension
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.DotProduct

/-!
# Book (Zenodo concept DOI 10.5281/zenodo.22290043), chapter 2, two flows

Source: `unified_quantum_gravity_book/chap02_geometric_flows_tensor_varieties.tex`.

## Part A. `thm:ricci_neckpinch` ("Curvature-Controlled Decay and Growth")

Book:
> Let `W(t)` solve the graphon Ricci flow `∂_t W = 2 κ_W W` on `[0,T)` from the two-block datum
> `W₀ = 1` on the blocks, `ε` on the bridge, and suppose that along the flow `κ ≤ −c₂ < 0` on
> the bridge and `κ ≥ c₁ > 0` inside the communities. Then for `t < T`:
> (i) on the bridge `ε e^{−2Ct} ≤ W(t) ≤ ε e^{−2c₂t}`, where `−C` is any lower bound of `κ`;
> in particular the bridge does not vanish in finite time;
> (ii) inside the communities `W(t) ≥ e^{2c₁t}`.
> Proof: for fixed `(x,y)`, `W(t) = W₀ exp(2∫₀ᵗ κ)`.

Declared reduction: the SCALAR ODE at a fixed point `(x,y)`. The curvature along the flow
enters as a given continuous function `k : ℝ → ℝ` (the book does not say how `κ_{W(t)}(x,y)`
depends on `t`; the proof only integrates it), the solution is `W : ℝ → ℝ`, continuous on
`[0,T)` and differentiable on `(0,T)` with `W' = 2 k W`.
* `linear_ode_solution`: `W(t) = W(0) exp(2∫₀ᵗ k)` on `[0,T)` (mean value theorem on
  `W e^{−2∫k}`, fundamental theorem of calculus for `∫k`).
* `ode_upper_bound`, `ode_lower_bound`: `W(0) ≥ 0`, `k ≤ b` (resp. `a ≤ k`) on `[0,T)` give
  `W(t) ≤ W(0) e^{2bt}` (resp. `W(0) e^{2at} ≤ W(t)`).
* `ricci_neckpinch_bridge` (= (i)), `ricci_neckpinch_bridge_pos`, `ricci_neckpinch_community`
  (= (ii)).
NOT covered: the Ollivier curvature, its dependence on `W(t)`, the metric on `[0,1]`, and the
existence of the flow (the book takes them as hypotheses too; see its Remark).

## Part B. `thm:cmps_energy_flow` ("Projected Imaginary-Time Evolution on cMPS; Formal Derivation")

Book:
> `Ψ(θ)`, `‖Ψ‖ = 1`, `E = ⟨Ψ|H|Ψ⟩`. Choose `θ̇` minimizing the McLachlan functional
> `‖(Id − |Ψ⟩⟨Ψ|) ∑_α ∂_αΨ θ̇^α + (H − E)Ψ‖²`. Then (i) the minimizers are the solutions of
> `g θ̇ = −½ ∇_θ⟨H⟩`, `g_{αβ} = Re⟨∂_αΨ|(Id − |Ψ⟩⟨Ψ|)|∂_βΨ⟩`; `g` may be degenerate, but the
> system is consistent because `∇⟨H⟩` vanishes on `ker g`, and every solution gives the same
> projected velocity; (ii) `d⟨H⟩/dτ = −2 θ̇ᵀ g θ̇ = −2‖Π_Ψ(H − E)Ψ‖² ≤ 0`.

Declared reduction: the FINITE-PARAMETER, real-inner-product core. `E` is a real inner product
space (the complex Hilbert space seen as a real one, so `Re⟨·|·⟩` is the inner product);
`u_α = (Id − |ψ⟩⟨ψ|)∂_αΨ`, `α ∈ Fin d`, and `w = (H − E)ψ` are given vectors; `H` is a
continuous linear map, symmetric for the inner product; the parameter curve is replaced by a
curve `Φ : ℝ → E` with `‖Φ‖ ≡ 1` and velocity `∑ θ̇^α v_α`.
* `mcl_expand`, `isMin_of_normal`, `normal_of_isMin`: the minimizers of the McLachlan
  functional are exactly the solutions of the normal equations `g θ = −b`, `b_α = ⟪u_α, w⟫`.
* `rhs_eq_of_ker`: `b` vanishes on `ker g` (the book's consistency argument);
  `exists_normal_solution`: the system has a solution (orthogonal projection of `w` on the
  span of the `u_α`); `vel_eq_of_normal`, `vel_unique`: every solution has the same velocity
  `−Π w`.
* `energy_deriv`: `d/dτ ⟪Φ, HΦ⟫ = 2⟪Φ', (H − E)Φ⟫` for a unit-norm curve and symmetric `H`.
* `energy_decrease`, `energy_decrease_nonpos`, `energy_decrease_eq_proj`: along a McLachlan
  velocity, `d⟨H⟩/dτ = −2 θ̇ᵀ g θ̇ = −2‖Π w‖² ≤ 0`.
NOT covered: the cMPS state `eq:cmps_state`, the Lieb–Liniger Hamiltonian (unbounded), the
gauge directions, differentiability of `θ ↦ Ψ(θ)`, and the existence of the flow (the book
calls the derivation formal and lists these as unproved).
-/

noncomputable section

namespace LeanReal.Chap02Flows

open Set Real Filter Topology intervalIntegral MeasureTheory

/-! ## Part A: `thm:ricci_neckpinch`, the scalar ODE `W' = 2kW` -/

section Ricci

/-- Solution formula for `W' = 2 k W` on `[0,T)`: `W(t) = W(0) · exp(2∫₀ᵗ k)`.
Hypotheses: `k` continuous, `W` continuous on `[0,T)` and differentiable on `(0,T)` with the
pointwise equation. -/
theorem linear_ode_solution (W k : ℝ → ℝ) (T : ℝ) (hk : Continuous k)
    (hWc : ContinuousOn W (Ico 0 T)) (hW : ∀ t ∈ Ioo 0 T, HasDerivAt W (2 * k t * W t) t)
    {t : ℝ} (ht : t ∈ Ico 0 T) :
    W t = W 0 * exp (2 * ∫ s in (0 : ℝ)..t, k s) := by
  set F : ℝ → ℝ := fun s => ∫ x in (0 : ℝ)..s, k x with hF
  have hF' : ∀ s, HasDerivAt F (k s) s := fun s => (hk.integral_hasStrictDerivAt 0 s).hasDerivAt
  have hF0 : F 0 = 0 := by simp [hF]
  have hFc : Continuous F := continuous_iff_continuousAt.2 fun s => (hF' s).continuousAt
  set g : ℝ → ℝ := fun s => W s * exp (-2 * F s) with hg
  rcases eq_or_lt_of_le ht.1 with h0 | hpos
  · rw [← h0]; simp
  · have hgc : ContinuousOn g (Icc 0 t) :=
      (hWc.mono (Icc_subset_Ico_right ht.2)).mul
        ((continuous_exp.comp (continuous_const.mul hFc)).continuousOn)
    have hgd : ∀ s ∈ Ioo 0 t, HasDerivAt g 0 s := by
      intro s hs
      have hs' : s ∈ Ioo 0 T := ⟨hs.1, hs.2.trans ht.2⟩
      have := (hW s hs').mul (((hF' s).const_mul (-2)).exp)
      refine this.congr_deriv ?_
      ring
    obtain ⟨c, -, hc⟩ := exists_hasDerivAt_eq_slope g (fun _ => (0 : ℝ)) hpos hgc hgd
    have hgt : g t = g 0 := by
      have h1 : (g t - g 0) / (t - 0) = 0 := hc.symm
      rw [div_eq_zero_iff] at h1
      rcases h1 with h1 | h1
      · linarith
      · linarith
    simp only [hg, hF0, mul_zero, exp_zero, mul_one] at hgt
    have hpos' := exp_pos (-2 * F t)
    calc W t = W t * exp (-2 * F t) * exp (2 * F t) := by
          rw [mul_assoc, ← exp_add]; ring_nf; simp
      _ = W 0 * exp (2 * F t) := by rw [hgt]

/-- Upper bound: `k ≤ b` on `[0,T)` and `W(0) ≥ 0` give `W(t) ≤ W(0) e^{2bt}`. -/
theorem ode_upper_bound (W k : ℝ → ℝ) (T b : ℝ) (hk : Continuous k)
    (hWc : ContinuousOn W (Ico 0 T)) (hW : ∀ t ∈ Ioo 0 T, HasDerivAt W (2 * k t * W t) t)
    (hW0 : 0 ≤ W 0) (hb : ∀ s ∈ Ico 0 T, k s ≤ b) {t : ℝ} (ht : t ∈ Ico 0 T) :
    W t ≤ W 0 * exp (2 * b * t) := by
  rw [linear_ode_solution W k T hk hWc hW ht]
  have hint : ∫ s in (0 : ℝ)..t, k s ≤ b * t := by
    have hki : IntervalIntegrable k volume 0 t := hk.intervalIntegrable 0 t
    have hbi : IntervalIntegrable (fun _ => b) volume 0 t := intervalIntegrable_const
    have := integral_mono_on ht.1 hki hbi (fun s hs => hb s ⟨hs.1, lt_of_le_of_lt hs.2 ht.2⟩)
    simpa [intervalIntegral.integral_const, mul_comm] using this
  exact mul_le_mul_of_nonneg_left (exp_le_exp.2 (by linarith)) hW0

/-- Lower bound: `a ≤ k` on `[0,T)` and `W(0) ≥ 0` give `W(0) e^{2at} ≤ W(t)`. -/
theorem ode_lower_bound (W k : ℝ → ℝ) (T a : ℝ) (hk : Continuous k)
    (hWc : ContinuousOn W (Ico 0 T)) (hW : ∀ t ∈ Ioo 0 T, HasDerivAt W (2 * k t * W t) t)
    (hW0 : 0 ≤ W 0) (ha : ∀ s ∈ Ico 0 T, a ≤ k s) {t : ℝ} (ht : t ∈ Ico 0 T) :
    W 0 * exp (2 * a * t) ≤ W t := by
  rw [linear_ode_solution W k T hk hWc hW ht]
  have hint : a * t ≤ ∫ s in (0 : ℝ)..t, k s := by
    have hki : IntervalIntegrable k volume 0 t := hk.intervalIntegrable 0 t
    have hai : IntervalIntegrable (fun _ => a) volume 0 t := intervalIntegrable_const
    have := integral_mono_on ht.1 hai hki (fun s hs => ha s ⟨hs.1, lt_of_le_of_lt hs.2 ht.2⟩)
    simpa [intervalIntegral.integral_const, mul_comm] using this
  exact mul_le_mul_of_nonneg_left (exp_le_exp.2 (by linarith)) hW0

/-- **`thm:ricci_neckpinch`(i)**, at a fixed bridge point: `W(0) = ε ≥ 0`, `−C ≤ k ≤ −c₂` on
`[0,T)` give `ε e^{−2Ct} ≤ W(t) ≤ ε e^{−2c₂t}` for `t ∈ [0,T)`. -/
theorem ricci_neckpinch_bridge (W k : ℝ → ℝ) (T ε c₂ C : ℝ) (hε : 0 ≤ ε) (hk : Continuous k)
    (hWc : ContinuousOn W (Ico 0 T)) (hW : ∀ t ∈ Ioo 0 T, HasDerivAt W (2 * k t * W t) t)
    (hW0 : W 0 = ε) (hupper : ∀ s ∈ Ico 0 T, k s ≤ -c₂) (hlower : ∀ s ∈ Ico 0 T, -C ≤ k s)
    {t : ℝ} (ht : t ∈ Ico 0 T) :
    ε * exp (-2 * C * t) ≤ W t ∧ W t ≤ ε * exp (-2 * c₂ * t) := by
  have h1 := ode_lower_bound W k T (-C) hk hWc hW (hW0 ▸ hε) hlower ht
  have h2 := ode_upper_bound W k T (-c₂) hk hWc hW (hW0 ▸ hε) hupper ht
  rw [hW0] at h1 h2
  refine ⟨?_, ?_⟩
  · calc ε * exp (-2 * C * t) = ε * exp (2 * -C * t) := by ring_nf
      _ ≤ W t := h1
  · calc W t ≤ ε * exp (2 * -c₂ * t) := h2
      _ = ε * exp (-2 * c₂ * t) := by ring_nf

/-- "The bridge does not vanish in finite time": `W(t) > 0` for `ε > 0`. -/
theorem ricci_neckpinch_bridge_pos (W k : ℝ → ℝ) (T ε C : ℝ) (hε : 0 < ε) (hk : Continuous k)
    (hWc : ContinuousOn W (Ico 0 T)) (hW : ∀ t ∈ Ioo 0 T, HasDerivAt W (2 * k t * W t) t)
    (hW0 : W 0 = ε) (hlower : ∀ s ∈ Ico 0 T, -C ≤ k s) {t : ℝ} (ht : t ∈ Ico 0 T) :
    0 < W t := by
  have h1 := ode_lower_bound W k T (-C) hk hWc hW (hW0 ▸ hε.le) hlower ht
  rw [hW0] at h1
  exact lt_of_lt_of_le (mul_pos hε (exp_pos _)) h1

/-- **`thm:ricci_neckpinch`(ii)**, at a fixed community point: `W(0) = 1`, `k ≥ c₁` on `[0,T)`
give `W(t) ≥ e^{2c₁t}`. -/
theorem ricci_neckpinch_community (W k : ℝ → ℝ) (T c₁ : ℝ) (hk : Continuous k)
    (hWc : ContinuousOn W (Ico 0 T)) (hW : ∀ t ∈ Ioo 0 T, HasDerivAt W (2 * k t * W t) t)
    (hW0 : W 0 = 1) (hc : ∀ s ∈ Ico 0 T, c₁ ≤ k s) {t : ℝ} (ht : t ∈ Ico 0 T) :
    exp (2 * c₁ * t) ≤ W t := by
  have h1 := ode_lower_bound W k T c₁ hk hWc hW (hW0 ▸ zero_le_one) hc ht
  rwa [hW0, one_mul] at h1

/-! ### Witness for Part A: `k(t) = −1 − t` (non-constant), `W(t) = ½ e^{−2t − t²}`, `T = 1`,
`ε = ½`, `c₂ = 1`, `C = 2`. The bounds `½e^{−4t} ≤ W ≤ ½e^{−2t}` are strict for `0 < t < 1`. -/

/-- `W(t) = ½ exp(−2t − t²)`. -/
def Wex (t : ℝ) : ℝ := 1 / 2 * exp (-2 * t - t ^ 2)

/-- `k(t) = −1 − t`. -/
def kex (t : ℝ) : ℝ := -1 - t

lemma kex_continuous : Continuous kex := by
  unfold kex; fun_prop

lemma Wex_continuous : Continuous Wex := by
  unfold Wex; fun_prop

lemma Wex_hasDerivAt (t : ℝ) : HasDerivAt Wex (2 * kex t * Wex t) t := by
  have h : HasDerivAt (fun s : ℝ => -2 * s - s ^ 2) (-2 * 1 - ((2 : ℕ) : ℝ) * t ^ (2 - 1)) t :=
    ((hasDerivAt_id t).const_mul (-2 : ℝ)).sub (hasDerivAt_pow 2 t)
  have := h.exp.const_mul (1 / 2 : ℝ)
  refine this.congr_deriv ?_
  simp only [Wex, kex, Nat.cast_ofNat]
  ring

theorem witness_bridge :
    ∀ t ∈ Ico (0 : ℝ) 1,
      1 / 2 * exp (-2 * 2 * t) ≤ Wex t ∧ Wex t ≤ 1 / 2 * exp (-2 * 1 * t) := fun t ht =>
  ricci_neckpinch_bridge Wex kex 1 (1 / 2) 1 2 (by norm_num) kex_continuous
    Wex_continuous.continuousOn (fun t _ => Wex_hasDerivAt t) (by simp [Wex])
    (fun s hs => by simp only [kex]; linarith [hs.1]) (fun s hs => by simp only [kex]; linarith [hs.2])
    ht

/-- The upper bound is not attained at `t = 1/2`: `W(1/2) = ½e^{−5/4} < ½e^{−1}`. -/
example : Wex (1 / 2) < 1 / 2 * exp (-2 * 1 * (1 / 2)) := by
  simp only [Wex]
  have : exp (-2 * (1 / 2 : ℝ) - (1 / 2) ^ 2) < exp (-2 * 1 * (1 / 2)) := exp_lt_exp.2 (by norm_num)
  linarith

/-! ### Mutants for Part A -/

/-- Mutant A1 (drop the bridge hypothesis `k ≤ −c₂`): the upper bound fails. Counterexample:
`k ≡ 0`, `W ≡ ½`, `c₂ = 1`, `t = 1`: `½ ≤ ½ e^{−2}` is false. -/
theorem mutant_no_upper_curvature_false :
    ¬ ∀ (W k : ℝ → ℝ) (T ε c₂ : ℝ), 0 ≤ ε → Continuous k → ContinuousOn W (Ico 0 T) →
      (∀ t ∈ Ioo 0 T, HasDerivAt W (2 * k t * W t) t) → W 0 = ε →
      ∀ t ∈ Ico 0 T, W t ≤ ε * exp (-2 * c₂ * t) := by
  intro h
  have := h (fun _ => 1 / 2) (fun _ => 0) 2 (1 / 2) 1 (by norm_num) continuous_const
    continuousOn_const (fun t _ => by simpa using hasDerivAt_const t (1 / 2 : ℝ)) rfl 1
    (by norm_num)
  have he : exp (-2 * 1 * 1) < 1 := exp_lt_one_iff.2 (by norm_num)
  have := mul_lt_mul_of_pos_left he (by norm_num : (0 : ℝ) < 1 / 2)
  linarith

/-- Mutant A2 (factor `2` dropped from the flow, `W' = kW`): the rate `e^{−2c₂t}` fails.
Counterexample: `k ≡ −1`, `W = ½e^{−t}`, `c₂ = 1`, `t = 1`: `½e^{−1} ≤ ½e^{−2}` is false. -/
theorem mutant_factor_two_false :
    ¬ ∀ (W k : ℝ → ℝ) (T ε c₂ : ℝ), 0 ≤ ε → Continuous k → ContinuousOn W (Ico 0 T) →
      (∀ t ∈ Ioo 0 T, HasDerivAt W (k t * W t) t) → W 0 = ε →
      (∀ s ∈ Ico 0 T, k s ≤ -c₂) → ∀ t ∈ Ico 0 T, W t ≤ ε * exp (-2 * c₂ * t) := by
  intro h
  have hd : ∀ t : ℝ, HasDerivAt (fun s : ℝ => 1 / 2 * exp (-s)) ((-1) * (1 / 2 * exp (-t))) t := by
    intro t
    have := ((hasDerivAt_neg t).exp).const_mul (1 / 2 : ℝ)
    refine this.congr_deriv ?_
    ring
  have := h (fun s => 1 / 2 * exp (-s)) (fun _ => -1) 2 (1 / 2) 1 (by norm_num) continuous_const
    (by fun_prop) (fun t _ => hd t) (by simp) (fun s _ => le_rfl) 1 (by norm_num)
  have he : exp (-2 * 1 * 1) < exp (-(1 : ℝ)) := exp_lt_exp.2 (by norm_num)
  have := mul_lt_mul_of_pos_left he (by norm_num : (0 : ℝ) < 1 / 2)
  linarith

end Ricci

/-! ## Part B: `thm:cmps_energy_flow`, McLachlan's principle in finite parameter dimension -/

section McLachlan

open Matrix Finset

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] {d : ℕ}

/-- Gram matrix `g_{αβ} = ⟪u_α, u_β⟫` of the projected tangent vectors. -/
def gram (u : Fin d → E) : Matrix (Fin d) (Fin d) ℝ := Matrix.of fun a b => inner ℝ (u a) (u b)

/-- `b_α = ⟪u_α, w⟫` (one half of `∂_α⟨H⟩` in the book). -/
def rhs (u : Fin d → E) (w : E) : Fin d → ℝ := fun a => inner ℝ (u a) (w)

/-- Projected velocity `∑_α θ^α u_α`. -/
def vel (u : Fin d → E) (θ : Fin d → ℝ) : E := ∑ a, θ a • u a

/-- McLachlan functional `‖∑_α θ^α u_α + w‖²`. -/
def mcl (u : Fin d → E) (w : E) (θ : Fin d → ℝ) : ℝ := ‖vel u θ + w‖ ^ 2

@[simp] lemma gram_apply (u : Fin d → E) (a b : Fin d) : gram u a b = inner ℝ (u a) (u b) := rfl

lemma inner_vel_left (u : Fin d → E) (θ : Fin d → ℝ) (x : E) :
    inner ℝ (vel u θ) (x) = ∑ a, θ a * inner ℝ (u a) (x) := by
  simp [vel, sum_inner, real_inner_smul_left]

lemma inner_vel_right (u : Fin d → E) (θ : Fin d → ℝ) (x : E) :
    inner ℝ (x) (vel u θ) = ∑ a, θ a * inner ℝ (x) (u a) := by
  simp [vel, inner_sum, real_inner_smul_right]

lemma vel_add (u : Fin d → E) (θ η : Fin d → ℝ) : vel u (θ + η) = vel u θ + vel u η := by
  simp [vel, add_smul, sum_add_distrib]

lemma vel_smul (u : Fin d → E) (c : ℝ) (θ : Fin d → ℝ) : vel u (c • θ) = c • vel u θ := by
  simp [vel, smul_sum, smul_smul]

lemma mulVec_gram_apply (u : Fin d → E) (θ : Fin d → ℝ) (a : Fin d) :
    (gram u *ᵥ θ) a = inner ℝ (u a) (vel u θ) := by
  simp [mulVec, dotProduct, inner_vel_right, mul_comm]

/-- `θ ⬝ (g η) = ⟪vel θ, vel η⟫`. -/
lemma dot_gram_mulVec (u : Fin d → E) (θ η : Fin d → ℝ) :
    θ ⬝ᵥ (gram u *ᵥ η) = inner ℝ (vel u θ) (vel u η) := by
  simp [dotProduct, mulVec_gram_apply, inner_vel_left]

/-- The quadratic form of `g` is the squared norm of the projected velocity. -/
lemma quad_eq (u : Fin d → E) (θ : Fin d → ℝ) : θ ⬝ᵥ (gram u *ᵥ θ) = ‖vel u θ‖ ^ 2 := by
  rw [dot_gram_mulVec, real_inner_self_eq_norm_sq]

lemma dot_rhs (u : Fin d → E) (w : E) (θ : Fin d → ℝ) : θ ⬝ᵥ rhs u w = inner ℝ (vel u θ) (w) := by
  simp [dotProduct, rhs, inner_vel_left]

/-- `mcl(θ) = θᵀ g θ + 2 θ·b + ‖w‖²`. -/
theorem mcl_expand (u : Fin d → E) (w : E) (θ : Fin d → ℝ) :
    mcl u w θ = θ ⬝ᵥ (gram u *ᵥ θ) + 2 * (θ ⬝ᵥ rhs u w) + ‖w‖ ^ 2 := by
  rw [mcl, quad_eq, dot_rhs, norm_add_sq_real]

/-- Second-order expansion: `mcl(θ + η) = mcl(θ) + 2 η·(gθ + b) + ‖vel η‖²`. -/
theorem mcl_add (u : Fin d → E) (w : E) (θ η : Fin d → ℝ) :
    mcl u w (θ + η) = mcl u w θ + 2 * (η ⬝ᵥ (gram u *ᵥ θ + rhs u w)) + ‖vel u η‖ ^ 2 := by
  rw [mcl, mcl, vel_add, add_right_comm, norm_add_sq_real, inner_add_left, dotProduct_add,
    dot_gram_mulVec, dot_rhs, real_inner_comm (vel u θ), real_inner_comm w]

/-- **`thm:cmps_energy_flow`(i), "if"**: a solution of the normal equations `g θ = −b`
minimizes the McLachlan functional. -/
theorem isMin_of_normal (u : Fin d → E) (w : E) (θ : Fin d → ℝ)
    (h : gram u *ᵥ θ = -(rhs u w)) : ∀ η, mcl u w θ ≤ mcl u w η := by
  intro η
  have := mcl_add u w θ (η - θ)
  rw [add_sub_cancel, h, neg_add_cancel, dotProduct_zero, mul_zero, add_zero] at this
  rw [this]
  exact le_add_of_nonneg_right (sq_nonneg _)

/-- **`thm:cmps_energy_flow`(i), "only if"**: a minimizer of the McLachlan functional solves
the normal equations. -/
theorem normal_of_isMin (u : Fin d → E) (w : E) (θ : Fin d → ℝ)
    (hmin : ∀ η, mcl u w θ ≤ mcl u w η) : gram u *ᵥ θ = -(rhs u w) := by
  set r := gram u *ᵥ θ + rhs u w with hr
  by_contra hne
  have hr0 : r ≠ 0 := by
    intro h0
    exact hne (eq_neg_of_add_eq_zero_left h0)
  have hrr : 0 < r ⬝ᵥ r := by
    have hnn : 0 ≤ r ⬝ᵥ r := Finset.sum_nonneg fun i _ => mul_self_nonneg (r i)
    rcases hnn.lt_or_eq with h | h
    · exact h
    · exact absurd (dotProduct_self_eq_zero.1 h.symm) hr0
  set Q := ‖vel u r‖ ^ 2 with hQ
  have hQ0 : 0 ≤ Q := sq_nonneg _
  set s := (r ⬝ᵥ r) / (Q + 1) with hs
  have hs0 : 0 < s := div_pos hrr (by linarith)
  have hsQ : s * Q < r ⬝ᵥ r := by
    rw [hs, div_mul_eq_mul_div, div_lt_iff₀ (by linarith)]
    nlinarith
  have key := hmin (θ + (-s) • r)
  rw [mcl_add, vel_smul, norm_smul, mul_pow, Real.norm_eq_abs, sq_abs, neg_sq, ← hQ,
    smul_dotProduct, smul_eq_mul] at key
  have := mul_lt_mul_of_pos_left hsQ hs0
  nlinarith

/-- The book's consistency argument: `b` vanishes on `ker g`, because `g v = 0` forces
`vel v = 0`. -/
theorem vel_eq_zero_of_mulVec_eq_zero (u : Fin d → E) (v : Fin d → ℝ) (hv : gram u *ᵥ v = 0) :
    vel u v = 0 := by
  have : ‖vel u v‖ ^ 2 = 0 := by rw [← quad_eq, hv, dotProduct_zero]
  exact norm_eq_zero.1 (pow_eq_zero_iff two_ne_zero |>.1 this)

theorem rhs_eq_of_ker (u : Fin d → E) (w : E) (v : Fin d → ℝ) (hv : gram u *ᵥ v = 0) :
    v ⬝ᵥ rhs u w = 0 := by
  rw [dot_rhs, vel_eq_zero_of_mulVec_eq_zero u v hv, inner_zero_left]

/-- The real span of the projected tangent vectors (the tangent space `T_Ψ` of the book). -/
def tangent (u : Fin d → E) : Submodule ℝ E := Submodule.span ℝ (Set.range u)

instance (u : Fin d → E) : FiniteDimensional ℝ (tangent u) :=
  FiniteDimensional.span_of_finite ℝ (Set.finite_range u)

instance (u : Fin d → E) : CompleteSpace (tangent u) := FiniteDimensional.complete ℝ (tangent u)

lemma inner_tangent_eq_zero (u : Fin d → E) (x : E) (hx : ∀ a, inner ℝ (u a) (x) = 0) {y : E}
    (hy : y ∈ tangent u) : inner ℝ (y) (x) = 0 := by
  obtain ⟨c, rfl⟩ := (Submodule.mem_span_range_iff_exists_fun ℝ).1 hy
  rw [← vel, inner_vel_left]
  simp [hx]

/-- **`thm:cmps_energy_flow`(i), consistency**: the normal equations `g θ = −b` always have a
solution, although `g` may be degenerate. -/
theorem exists_normal_solution (u : Fin d → E) (w : E) : ∃ θ, gram u *ᵥ θ = -(rhs u w) := by
  obtain ⟨θ, hθ⟩ := (Submodule.mem_span_range_iff_exists_fun ℝ).1
    ((tangent u).starProjection_apply_mem w)
  refine ⟨-θ, ?_⟩
  ext a
  have horth : inner ℝ (u a) (w - (tangent u).starProjection w) = 0 := by
    rw [real_inner_comm]
    exact (tangent u).starProjection_inner_eq_zero w (u a) (Submodule.subset_span ⟨a, rfl⟩)
  rw [mulVec_neg, Pi.neg_apply, mulVec_gram_apply, Pi.neg_apply, rhs, inner_sub_right] at *
  rw [show vel u θ = (tangent u).starProjection w from hθ]
  linarith

/-- **`thm:cmps_energy_flow`(i), projected velocity**: every solution of the normal equations
has velocity `−Π w`, the negative orthogonal projection of `w` on the tangent space. -/
theorem vel_eq_of_normal (u : Fin d → E) (w : E) (θ : Fin d → ℝ)
    (h : gram u *ᵥ θ = -(rhs u w)) : vel u θ = -((tangent u).starProjection w) := by
  set x := vel u θ + (tangent u).starProjection w with hx
  have hxmem : x ∈ tangent u := by
    refine (tangent u).add_mem ?_ ((tangent u).starProjection_apply_mem w)
    exact Submodule.sum_mem _ fun a _ =>
      (tangent u).smul_mem _ (Submodule.subset_span ⟨a, rfl⟩)
  have hperp : ∀ a, inner ℝ (u a) (x) = 0 := by
    intro a
    have h1 := congrFun h a
    rw [mulVec_gram_apply, Pi.neg_apply] at h1
    have h2 : inner ℝ (u a) (w - (tangent u).starProjection w) = 0 := by
      rw [real_inner_comm]
      exact (tangent u).starProjection_inner_eq_zero w (u a) (Submodule.subset_span ⟨a, rfl⟩)
    rw [hx, inner_add_right, h1, rhs]
    rw [inner_sub_right] at h2
    linarith
  have : inner ℝ (x) (x) = 0 := inner_tangent_eq_zero u x hperp hxmem
  rw [inner_self_eq_zero] at this
  exact eq_neg_of_add_eq_zero_left this

/-- Two solutions of the normal equations give the same projected velocity. -/
theorem vel_unique (u : Fin d → E) (w : E) (θ₁ θ₂ : Fin d → ℝ)
    (h₁ : gram u *ᵥ θ₁ = -(rhs u w)) (h₂ : gram u *ᵥ θ₂ = -(rhs u w)) :
    vel u θ₁ = vel u θ₂ := by
  rw [vel_eq_of_normal u w θ₁ h₁, vel_eq_of_normal u w θ₂ h₂]

/-- `θᵀ g θ = ‖Π w‖²` for a solution of the normal equations. -/
theorem quad_eq_proj (u : Fin d → E) (w : E) (θ : Fin d → ℝ)
    (h : gram u *ᵥ θ = -(rhs u w)) :
    θ ⬝ᵥ (gram u *ᵥ θ) = ‖(tangent u).starProjection w‖ ^ 2 := by
  rw [quad_eq, vel_eq_of_normal u w θ h, norm_neg]

/-! ### Item (ii): the energy derivative -/

/-- The projection `(Id − |ψ⟩⟨ψ|) x = x − ⟪ψ, x⟫ ψ`. -/
def proj0 (ψ x : E) : E := x - inner ℝ (ψ) (x) • ψ

/-- The residual `(H − E)ψ` with `E = ⟪ψ, Hψ⟫`. -/
def resid (H : E →L[ℝ] E) (ψ : E) : E := H ψ - inner ℝ (ψ) (H ψ) • ψ

/-- `(H − E)ψ ⊥ ψ` when `‖ψ‖ = 1`. -/
lemma inner_resid (H : E →L[ℝ] E) (ψ : E) (hψ : ‖ψ‖ = 1) : inner ℝ (ψ) (resid H ψ) = 0 := by
  simp [resid, inner_sub_right, real_inner_smul_right, hψ]

/-- `⟪(Id − |ψ⟩⟨ψ|) x, (H − E)ψ⟫ = ⟪x, (H − E)ψ⟫`: the projector may be dropped against the
residual. -/
lemma inner_proj0_resid (H : E →L[ℝ] E) (ψ x : E) (hψ : ‖ψ‖ = 1) :
    inner ℝ (proj0 ψ x) (resid H ψ) = inner ℝ (x) (resid H ψ) := by
  simp [proj0, inner_sub_left, real_inner_smul_left, inner_resid H ψ hψ]

/-- Along a unit-norm curve `Φ`, `⟪Φ', Φ⟫ = 0`. -/
lemma inner_deriv_self (Φ : ℝ → E) (Φ' : E) (τ : ℝ) (hΦ : HasDerivAt Φ Φ' τ)
    (hnorm : ∀ s, ‖Φ s‖ = 1) : inner ℝ (Φ') (Φ τ) = 0 := by
  have h1 : HasDerivAt (fun s => inner ℝ (Φ s) (Φ s)) (inner ℝ (Φ τ) (Φ') + inner ℝ (Φ') (Φ τ)) τ := hΦ.inner ℝ hΦ
  have h2 : HasDerivAt (fun s => inner ℝ (Φ s) (Φ s)) 0 τ := by
    have : (fun s => inner ℝ (Φ s) (Φ s)) = fun _ => (1 : ℝ) := by
      funext s; rw [real_inner_self_eq_norm_sq, hnorm s]; norm_num
    rw [this]; exact hasDerivAt_const τ 1
  have := h1.unique h2
  rw [real_inner_comm (Φ τ)] at this ⊢
  linarith

/-- **`thm:cmps_energy_flow`(ii), first identity**: for a unit-norm curve `Φ` and a symmetric
`H`, `d/dτ ⟪Φ, HΦ⟫ = 2 ⟪Φ', (H − E)Φ⟫`. -/
theorem energy_deriv (H : E →L[ℝ] E) (hH : ∀ x y, inner ℝ (H x) (y) = inner ℝ (x) (H y))
    (Φ : ℝ → E) (Φ' : E) (τ : ℝ) (hΦ : HasDerivAt Φ Φ' τ) (hnorm : ∀ s, ‖Φ s‖ = 1) :
    HasDerivAt (fun s => inner ℝ (Φ s) (H (Φ s))) (2 * inner ℝ (Φ') (resid H (Φ τ))) τ := by
  have hHΦ : HasDerivAt (fun s => H (Φ s)) (H Φ') τ := H.hasFDerivAt.comp_hasDerivAt τ hΦ
  refine (hΦ.inner ℝ hHΦ).congr_deriv ?_
  rw [resid, inner_sub_right, real_inner_smul_right, inner_deriv_self Φ Φ' τ hΦ hnorm,
    ← hH (Φ τ) Φ', real_inner_comm Φ']
  ring

/-- **`thm:cmps_energy_flow`(ii)**: if the curve's velocity is `∑ θ̇^α v_α` and `θ̇` solves the
normal equations for `u_α = (Id − |Φ⟩⟨Φ|) v_α`, `w = (H − E)Φ`, then
`d⟨H⟩/dτ = −2 θ̇ᵀ g θ̇`. -/
theorem energy_decrease (H : E →L[ℝ] E) (hH : ∀ x y, inner ℝ (H x) (y) = inner ℝ (x) (H y))
    (Φ : ℝ → E) (τ : ℝ) (v : Fin d → E) (θ' : Fin d → ℝ)
    (hΦ : HasDerivAt Φ (vel v θ') τ) (hnorm : ∀ s, ‖Φ s‖ = 1)
    (hnormal : gram (fun a => proj0 (Φ τ) (v a)) *ᵥ θ'
      = -(rhs (fun a => proj0 (Φ τ) (v a)) (resid H (Φ τ)))) :
    HasDerivAt (fun s => inner ℝ (Φ s) (H (Φ s)))
      (-2 * (θ' ⬝ᵥ (gram (fun a => proj0 (Φ τ) (v a)) *ᵥ θ'))) τ := by
  refine (energy_deriv H hH Φ (vel v θ') τ hΦ hnorm).congr_deriv ?_
  rw [hnormal, dotProduct_neg, dot_rhs, inner_vel_left, inner_vel_left]
  simp only [inner_proj0_resid H (Φ τ) _ (hnorm τ)]
  ring

theorem energy_decrease_nonpos (u : Fin d → E) (θ' : Fin d → ℝ) :
    -2 * (θ' ⬝ᵥ (gram u *ᵥ θ')) ≤ 0 := by
  rw [quad_eq]; nlinarith [sq_nonneg ‖vel u θ'‖]

/-- `−2 θ̇ᵀ g θ̇ = −2 ‖Π_Ψ (H − E)Ψ‖²`. -/
theorem energy_decrease_eq_proj (u : Fin d → E) (w : E) (θ' : Fin d → ℝ)
    (h : gram u *ᵥ θ' = -(rhs u w)) :
    -2 * (θ' ⬝ᵥ (gram u *ᵥ θ')) = -2 * ‖(tangent u).starProjection w‖ ^ 2 := by
  rw [quad_eq_proj u w θ' h]

end McLachlan

/-! ### Witness for Part B: `E = ℂ` as a real inner product space, `d = 2`.
`ψ = 1`, raw tangent vectors `v = (1 + i, 2i)`, projected `u = (i, 2i)` (so `g = [[1,2],[2,4]]`
is DEGENERATE), `H(x + iy) = (x + 3y) + (3x + y)i` (symmetric), `E = 1`, `w = 3i`.
Normal equations `θ₀ + 2θ₁ = −3`, `2θ₀ + 4θ₁ = −6`: consistent, non-unique
(`θ = (−3 − 2s, s)`), velocity always `−3i = −w`. Curve `Φ(τ) = e^{−3iτ}`,
`Φ'(0) = −3i = vel v (0, −3/2)`; `d⟨H⟩/dτ(0) = −18 = −2‖w‖²`. -/

section Witness

open Matrix Complex

/-- The symmetric operator `H(x + iy) = (x + 3y) + (3x + y)i` on `ℂ ≅ ℝ²`. -/
def Hw : ℂ →ₗ[ℝ] ℂ where
  toFun z := ⟨z.re + 3 * z.im, 3 * z.re + z.im⟩
  map_add' x y := by apply Complex.ext <;> simp <;> ring
  map_smul' r x := by apply Complex.ext <;> simp <;> ring

/-- `Hw` as a continuous linear map. -/
def HwL : ℂ →L[ℝ] ℂ := LinearMap.toContinuousLinearMap Hw

lemma HwL_apply (z : ℂ) : HwL z = ⟨z.re + 3 * z.im, 3 * z.re + z.im⟩ := rfl

lemma HwL_symm : ∀ x y : ℂ, inner ℝ (HwL x) (y) = inner ℝ (x) (HwL y) := by
  intro x y; simp [HwL_apply, Complex.inner]; ring

/-- Raw tangent vectors `v = (1 + i, 2i)`. -/
def vw : Fin 2 → ℂ := ![⟨1, 1⟩, ⟨0, 2⟩]

/-- Projected tangent vectors `u = (i, 2i)`. -/
def uw : Fin 2 → ℂ := ![⟨0, 1⟩, ⟨0, 2⟩]

lemma uw_eq_proj0 : (fun a => proj0 (1 : ℂ) (vw a)) = uw := by
  funext a; fin_cases a <;> apply Complex.ext <;> simp only [proj0, Complex.inner] <;>
    norm_num [vw, uw, Complex.mul_re, Complex.conj_re, Complex.conj_im]

/-- `w = (H − E)·1 = 3i`. -/
lemma resid_one : resid HwL 1 = ⟨0, 3⟩ := by
  apply Complex.ext <;> simp only [resid, Complex.inner] <;>
    norm_num [HwL_apply, Complex.mul_re, Complex.conj_re, Complex.conj_im]

lemma gram_uw : gram uw = !![1, 2; 2, 4] := by
  ext a b; fin_cases a <;> fin_cases b <;> simp only [gram_apply, Complex.inner] <;>
    norm_num [uw, Complex.mul_re, Complex.conj_re, Complex.conj_im]

lemma rhs_uw : rhs uw ⟨0, 3⟩ = ![3, 6] := by
  funext a; fin_cases a <;> simp only [rhs, Complex.inner] <;>
    norm_num [uw, Complex.mul_re, Complex.conj_re, Complex.conj_im]

/-- `g` is degenerate (`det g = 0`), as the book says. -/
example : (gram uw).det = 0 := by
  rw [gram_uw, Matrix.det_fin_two_of]; norm_num

/-- `θ = (0, −3/2)` solves the normal equations. -/
theorem witness_normal : gram uw *ᵥ ![0, -3 / 2] = -(rhs uw ⟨0, 3⟩) := by
  rw [gram_uw, rhs_uw]
  funext a; fin_cases a <;> norm_num [mulVec, dotProduct, Fin.sum_univ_two]

/-- A second solution `θ = (−3, 0)`: the minimizer is not unique, but the velocity is. -/
theorem witness_normal' : gram uw *ᵥ ![-3, 0] = -(rhs uw ⟨0, 3⟩) := by
  rw [gram_uw, rhs_uw]
  funext a; fin_cases a <;> norm_num [mulVec, dotProduct, Fin.sum_univ_two]

example : vel uw ![0, -3 / 2] = vel uw ![-3, 0] :=
  vel_unique uw ⟨0, 3⟩ _ _ witness_normal witness_normal'

/-- The McLachlan functional vanishes at the solution and equals `9` at `θ = 0`. -/
example : mcl uw ⟨0, 3⟩ ![0, -3 / 2] = 0 ∧ mcl uw ⟨0, 3⟩ 0 = 9 := by
  constructor
  · have : vel uw ![0, -3 / 2] + (⟨0, 3⟩ : ℂ) = 0 := by
      apply Complex.ext <;> norm_num [vel, uw, Fin.sum_univ_two]
    simp [mcl, this]
  · have : vel uw 0 + (⟨0, 3⟩ : ℂ) = ⟨0, 3⟩ := by simp [vel]
    rw [mcl, this, Complex.sq_norm, Complex.normSq_apply]; norm_num

/-- The curve `Φ(τ) = exp(−3iτ)`, of unit norm. -/
def Φw (τ : ℝ) : ℂ := Complex.exp ((-3 * τ : ℝ) * Complex.I)

lemma Φw_norm (τ : ℝ) : ‖Φw τ‖ = 1 := Complex.norm_exp_ofReal_mul_I _

lemma Φw_zero : Φw 0 = 1 := by simp [Φw]

lemma Φw_hasDerivAt_zero : HasDerivAt Φw (vel vw ![0, -3 / 2]) 0 := by
  have h1 : HasDerivAt (fun z : ℂ => Complex.exp (-3 * z * Complex.I))
      (Complex.exp (-3 * (0 : ℂ) * Complex.I) * (-3 * Complex.I)) 0 := by
    have := (Complex.hasDerivAt_exp (-3 * (0 : ℂ) * Complex.I)).comp (0 : ℂ)
      (((hasDerivAt_id (0 : ℂ)).const_mul (-3 : ℂ)).mul_const Complex.I)
    simpa [Function.comp_def] using this
  have h2 := h1.comp_ofReal (z := 0)
  have h3 : (fun y : ℝ => Complex.exp (-3 * (y : ℂ) * Complex.I)) = Φw := by
    funext y; simp [Φw]
  rw [h3] at h2
  refine h2.congr_deriv ?_
  apply Complex.ext <;> norm_num [vel, vw, Fin.sum_univ_two]

/-- `thm:cmps_energy_flow`(ii) on the witness: `d⟨H⟩/dτ(0) = −18`. -/
theorem witness_energy :
    HasDerivAt (fun s => inner ℝ (Φw s) (HwL (Φw s))) (-18) 0 := by
  have h := energy_decrease HwL HwL_symm Φw 0 vw ![0, -3 / 2] Φw_hasDerivAt_zero Φw_norm
    (by rw [Φw_zero, uw_eq_proj0, resid_one]; exact witness_normal)
  rw [Φw_zero, uw_eq_proj0, gram_uw] at h
  refine h.congr_deriv ?_
  simp [mulVec, dotProduct, Fin.sum_univ_two]
  norm_num

/-- And `−18 = −2‖Π w‖² = −2‖w‖²` since `w = 3i` lies in the tangent span. -/
example : -2 * (![0, -3 / 2] ⬝ᵥ (gram uw *ᵥ ![0, -3 / 2]))
    = -2 * ‖(tangent uw).starProjection ⟨0, 3⟩‖ ^ 2 :=
  energy_decrease_eq_proj uw ⟨0, 3⟩ _ witness_normal

end Witness

/-! ### Mutants for Part B -/

section Mutants

open Matrix Complex

/-- Mutant B1 (sign dropped in the normal equations, `g θ = +b`): such a `θ` need not minimize.
On the witness, `θ = (0, 3/2)` solves `g θ = b` but `mcl = 36 > 0 = mcl(0, −3/2)`. -/
theorem mutant_normal_sign_false :
    ¬ ∀ (u : Fin 2 → ℂ) (w : ℂ) (θ : Fin 2 → ℝ), gram u *ᵥ θ = rhs u w →
      ∀ η, mcl u w θ ≤ mcl u w η := by
  intro h
  have hθ : gram uw *ᵥ ![0, 3 / 2] = rhs uw ⟨0, 3⟩ := by
    rw [gram_uw, rhs_uw]
    funext a; fin_cases a <;> norm_num [mulVec, dotProduct, Fin.sum_univ_two]
  have := h uw ⟨0, 3⟩ _ hθ ![0, -3 / 2]
  have h1 : vel uw ![0, 3 / 2] + (⟨0, 3⟩ : ℂ) = ⟨0, 6⟩ := by
    apply Complex.ext <;> norm_num [vel, uw, Fin.sum_univ_two]
  have h2 : vel uw ![0, -3 / 2] + (⟨0, 3⟩ : ℂ) = 0 := by
    apply Complex.ext <;> norm_num [vel, uw, Fin.sum_univ_two]
  rw [mcl, mcl, h1, h2, Complex.sq_norm, Complex.normSq_apply] at this
  simp at this
  norm_num at this

/-- Mutant B2 (consistency without the structure `b_α = ⟪u_α, w⟫`): a degenerate symmetric
`g` with an arbitrary right-hand side is in general inconsistent: `[[1,2],[2,4]] θ = (1, 0)` has
no solution. So `exists_normal_solution` has content beyond linear algebra of `g` alone. -/
theorem mutant_consistency_false :
    ¬ ∃ θ : Fin 2 → ℝ, (!![1, 2; 2, 4] : Matrix (Fin 2) (Fin 2) ℝ) *ᵥ θ = ![1, 0] := by
  rintro ⟨θ, h⟩
  have h0 := congrFun h 0
  have h1 := congrFun h 1
  simp [mulVec, dotProduct, Fin.sum_univ_two] at h0 h1
  linarith

/-- The rotation `J z = i z`, antisymmetric for the real inner product. -/
def Jw : ℂ →L[ℝ] ℂ := LinearMap.toContinuousLinearMap (LinearMap.mulLeft ℝ Complex.I)

lemma Jw_apply (z : ℂ) : Jw z = Complex.I * z := rfl

/-- The unit circle `τ ↦ e^{iτ}`. -/
def Φc (τ : ℝ) : ℂ := Complex.exp ((τ : ℂ) * Complex.I)

lemma Φc_norm (τ : ℝ) : ‖Φc τ‖ = 1 := Complex.norm_exp_ofReal_mul_I _

lemma Φc_hasDerivAt_zero : HasDerivAt Φc Complex.I 0 := by
  have h1 : HasDerivAt (fun z : ℂ => Complex.exp (z * Complex.I))
      (Complex.exp ((0 : ℂ) * Complex.I) * Complex.I) 0 := by
    have := (Complex.hasDerivAt_exp ((0 : ℂ) * Complex.I)).comp (0 : ℂ)
      ((hasDerivAt_id (0 : ℂ)).mul_const Complex.I)
    simpa [Function.comp_def] using this
  have h2 := h1.comp_ofReal (z := 0)
  have h3 : (fun y : ℝ => Complex.exp ((y : ℂ) * Complex.I)) = Φc := by
    funext y; simp [Φc]
  rw [h3] at h2
  refine h2.congr_deriv ?_
  simp

/-- Mutant B3 (drop the symmetry of `H` in `energy_deriv`): false. For `J z = iz` and the unit
circle, `⟪Φ, JΦ⟫ ≡ 0` has derivative `0`, while `2⟪Φ', (J − E)Φ⟫ = 2` at `τ = 0`. -/
theorem mutant_energy_nonsymmetric_false :
    ¬ ∀ (H : ℂ →L[ℝ] ℂ) (Φ : ℝ → ℂ) (Φ' : ℂ) (τ : ℝ), HasDerivAt Φ Φ' τ → (∀ s, ‖Φ s‖ = 1) →
      HasDerivAt (fun s => inner ℝ (Φ s) (H (Φ s))) (2 * inner ℝ (Φ') (resid H (Φ τ))) τ := by
  intro h
  have h1 := h Jw Φc Complex.I 0 Φc_hasDerivAt_zero Φc_norm
  have hzero : (fun s => inner ℝ (Φc s) (Jw (Φc s))) = fun _ => (0 : ℝ) := by
    funext s; simp [Jw_apply, Complex.inner]; ring
  rw [hzero] at h1
  have h2 := h1.unique (hasDerivAt_const 0 (0 : ℝ))
  have hΦ0 : Φc 0 = 1 := by simp [Φc]
  rw [hΦ0] at h2
  simp [resid, Jw_apply, Complex.inner] at h2

end Mutants

end LeanReal.Chap02Flows

#print axioms LeanReal.Chap02Flows.linear_ode_solution
#print axioms LeanReal.Chap02Flows.ode_upper_bound
#print axioms LeanReal.Chap02Flows.ode_lower_bound
#print axioms LeanReal.Chap02Flows.ricci_neckpinch_bridge
#print axioms LeanReal.Chap02Flows.ricci_neckpinch_bridge_pos
#print axioms LeanReal.Chap02Flows.ricci_neckpinch_community
#print axioms LeanReal.Chap02Flows.witness_bridge
#print axioms LeanReal.Chap02Flows.mutant_no_upper_curvature_false
#print axioms LeanReal.Chap02Flows.mutant_factor_two_false
#print axioms LeanReal.Chap02Flows.mcl_expand
#print axioms LeanReal.Chap02Flows.mcl_add
#print axioms LeanReal.Chap02Flows.isMin_of_normal
#print axioms LeanReal.Chap02Flows.normal_of_isMin
#print axioms LeanReal.Chap02Flows.rhs_eq_of_ker
#print axioms LeanReal.Chap02Flows.exists_normal_solution
#print axioms LeanReal.Chap02Flows.vel_eq_of_normal
#print axioms LeanReal.Chap02Flows.vel_unique
#print axioms LeanReal.Chap02Flows.quad_eq_proj
#print axioms LeanReal.Chap02Flows.energy_deriv
#print axioms LeanReal.Chap02Flows.energy_decrease
#print axioms LeanReal.Chap02Flows.energy_decrease_nonpos
#print axioms LeanReal.Chap02Flows.energy_decrease_eq_proj
#print axioms LeanReal.Chap02Flows.witness_normal
#print axioms LeanReal.Chap02Flows.witness_energy
#print axioms LeanReal.Chap02Flows.mutant_normal_sign_false
#print axioms LeanReal.Chap02Flows.mutant_consistency_false
#print axioms LeanReal.Chap02Flows.mutant_energy_nonsymmetric_false
