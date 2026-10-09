import Mathlib.Analysis.SpecialFunctions.Gamma.Beta
import Mathlib.Analysis.SpecialFunctions.Gamma.Deriv

/-!
# *Beyond the Spectrum* III, item T3

Source: `Manuscritos_Avulsos/paper_beyond_the_spectrum_3/paper_beyond_the_spectrum_3.tex`,
Proposition `prop:coordinate_mellin` ("Mellin transform of a vertex coordinate").

Paper (setting): `Δ_m = {u ∈ ℝ^m_{≥0} | ∑ u_i = 1}` with the Dirichlet probability measure
`dμ_α(u) = Γ(α₀)/∏Γ(α_i) ∏ u_i^{α_i−1} du`, `α_i > 0`, `α₀ = ∑ α_i`, `du` Lebesgue on the first
`m − 1` coordinates.

Paper (proposition):
> For `j ∈ {1,…,m}` and `m ≥ 2`, let `M_j(s) := ∫_{Δ_m} u_j^s dμ_α(u)`, which converges for
> `Re(s) > −α_j`. Then `M_j(s) = Γ(α₀)Γ(α_j + s)/(Γ(α_j)Γ(α₀ + s))`, which extends meromorphically
> to `ℂ`. Write `b_j := α₀ − α_j > 0`. If `b_j ∉ ℤ`, the poles are exactly `s = −α_j − k`, `k ∈ ℕ₀`,
> all simple, with residues `Res_{s=−α_j−k} M_j = (−1)^k/k! · Γ(α₀)/(Γ(α_j)Γ(b_j − k)) ≠ 0`.
> If `b_j` is a positive integer, `M_j` is a rational function with simple poles exactly at
> `s = −α_j − k`, `0 ≤ k ≤ b_j − 1`.

Formal version, with `a = α_j > 0`, `b = b_j > 0`, `α₀ = a + b`:
* `coordinate_mellin` : for `Re s > −a`,
  `Γ(a+b)/(Γ(a)Γ(b)) ∫₀¹ x^s x^{a−1}(1−x)^{b−1} dx = Γ(a+b)Γ(a+s)/(Γ(a)Γ(a+b+s))`.
  The left side is `M_j(s)` written against the Beta(`a`, `b`) law of `u_j`.
* `beta_normalization` : `∫₀¹ x^{a−1}(1−x)^{b−1} dx = Γ(a)Γ(b)/Γ(a+b)` (so the left side at `s = 0`
  is `1`: a probability measure).
* `F_differentiableAt` : the right side `F` is holomorphic at every `s` with `a + s ∉ −ℕ`
  (meromorphic continuation; the only candidate poles are `s = −a − k`).
* `F_residue` : `(s + a + k)·F(s) → (−1)^k/k! · Γ(a+b)/Γ(a) · Γ(b−k)⁻¹` as `s → −a−k`, `s ≠ −a−k`,
  for EVERY `k ∈ ℕ` (when `Γ(b−k)` has a pole, the limit is `0`, `Γ⁻¹` being entire).
* `F_residue_ne_zero` : if `b ∉ ℤ`, that limit is `≠ 0`: so each `−a−k` is a simple pole with the
  stated residue.
* `F_rational` : if `b = n ∈ ℕ`, then `F(s) = Γ(a+n)/Γ(a) · (∏_{i<n} (a+s+i))⁻¹` for `a + s ∉ −ℕ`.
REDUCTIONS (declared):
* The aggregation property of the Dirichlet law (`u_j ~ Beta(α_j, α₀ − α_j)` under `μ_α`) is NOT
  formalized: the integral over `Δ_m` is replaced by the one-dimensional Beta integral. For
  `m = 2`, `j = 1` this IS the paper's integral (`du` = Lebesgue measure on `u_1 ∈ [0,1]`).
* `α_j`, `b_j` are real (as in the paper); `Γ` is `Complex.Gamma` at real arguments.
* "Poles exactly at …" in the rational case is read off the displayed product formula; the
  absence of a pole at `−a−k`, `k ≥ n`, is not stated as a separate Lean theorem.
-/

namespace LeanReal.BeyondSpectrum3T3

open Complex Filter Topology
open scoped Nat

set_option autoImplicit false

/-- `M(s) = Γ(a+b)/(Γ(a)Γ(b)) ∫₀¹ x^s · x^{a−1}(1−x)^{b−1} dx` (Beta(`a`,`b`) law). -/
noncomputable def M (a b : ℝ) (s : ℂ) : ℂ :=
  Gamma (a + b) / (Gamma a * Gamma b) *
    ∫ x : ℝ in (0 : ℝ)..1, (x : ℂ) ^ s * ((x : ℂ) ^ ((a : ℂ) - 1) * (1 - (x : ℂ)) ^ ((b : ℂ) - 1))

/-- The paper's closed form `Γ(α₀)Γ(α_j + s)/(Γ(α_j)Γ(α₀ + s))`, `α₀ = a + b`. -/
noncomputable def F (a b : ℝ) (s : ℂ) : ℂ :=
  Gamma (a + b) * Gamma (a + s) / (Gamma a * Gamma (a + b + s))

lemma integral_eq_beta (a b : ℝ) (s : ℂ) :
    (∫ x : ℝ in (0 : ℝ)..1,
        (x : ℂ) ^ s * ((x : ℂ) ^ ((a : ℂ) - 1) * (1 - (x : ℂ)) ^ ((b : ℂ) - 1))) =
      betaIntegral (a + s) b := by
  unfold betaIntegral
  apply intervalIntegral.integral_congr_ae
  filter_upwards with x hx
  rw [Set.uIoc_of_le zero_le_one] at hx
  have hx0 : (x : ℂ) ≠ 0 := by exact_mod_cast hx.1.ne'
  rw [← mul_assoc, ← cpow_add _ _ hx0]
  congr 2
  ring

lemma re_pos_of {a : ℝ} (ha : 0 < a) : 0 < ((a : ℂ)).re := by simpa using ha

/-- Normalization: `∫₀¹ x^{a−1}(1−x)^{b−1} dx = Γ(a)Γ(b)/Γ(a+b)`. -/
theorem beta_normalization {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    betaIntegral a b = Gamma a * Gamma b / Gamma (a + b) := by
  have h := Gamma_mul_Gamma_eq_betaIntegral (re_pos_of ha) (re_pos_of hb)
  have h0 : Gamma ((a : ℂ) + b) ≠ 0 := Gamma_ne_zero_of_re_pos (by simp; linarith)
  rw [h]; field_simp

/-- **Mellin transform of a vertex coordinate** (Beta-marginal form). -/
theorem coordinate_mellin {a b : ℝ} (ha : 0 < a) (hb : 0 < b) {s : ℂ} (hs : -a < s.re) :
    M a b s = F a b s := by
  unfold M F
  rw [integral_eq_beta]
  have hre : 0 < ((a : ℂ) + s).re := by simp; linarith
  have h := Gamma_mul_Gamma_eq_betaIntegral hre (re_pos_of hb)
  have h1 : Gamma ((a : ℂ) + s + b) ≠ 0 := Gamma_ne_zero_of_re_pos (by simp; linarith)
  have h2 : Gamma (a : ℂ) ≠ 0 := Gamma_ne_zero_of_re_pos (re_pos_of ha)
  have h3 : Gamma (b : ℂ) ≠ 0 := Gamma_ne_zero_of_re_pos (re_pos_of hb)
  have hβ : betaIntegral (a + s) b = Gamma (a + s) * Gamma b / Gamma (a + s + b) := by
    rw [h]; field_simp
  have e : (a : ℂ) + b + s = a + s + b := by ring
  rw [hβ, e]
  field_simp

/-- Holomorphy of `F` off `{s : a + s ∈ −ℕ}`. -/
theorem F_differentiableAt (a b : ℝ) {s : ℂ} (hs : ∀ m : ℕ, (a : ℂ) + s ≠ -m) :
    DifferentiableAt ℂ (F a b) s := by
  have hF : F a b = fun s => Gamma (a + b) / Gamma a * Gamma (a + s) * (Gamma (a + b + s))⁻¹ := by
    funext s; unfold F; rw [div_eq_mul_inv, div_eq_mul_inv, mul_inv]; ring
  rw [hF]
  have hG : DifferentiableAt ℂ (fun s : ℂ => Gamma (a + s)) s :=
    (differentiableAt_Gamma _ hs).comp s ((differentiableAt_const _).add differentiableAt_id)
  have hI : DifferentiableAt ℂ (fun s : ℂ => (Gamma (a + b + s))⁻¹) s :=
    (differentiable_one_div_Gamma _).comp s ((differentiableAt_const _).add differentiableAt_id)
  exact ((differentiableAt_const _).mul hG).mul hI

/-- `(z + k)Γ(z) → (−1)^k/k!` as `z → −k`, `z ≠ −k`. -/
theorem tendsto_Gamma_neg_nat (k : ℕ) :
    Tendsto (fun z : ℂ => (z + k) * Gamma z) (𝓝[≠] (-(k : ℂ))) (𝓝 ((-1) ^ k / k !)) := by
  induction k with
  | zero => simpa using tendsto_self_mul_Gamma_nhds_zero
  | succ k ih =>
    have hshift : Tendsto (fun z : ℂ => z + 1) (𝓝[≠] (-((k + 1 : ℕ) : ℂ))) (𝓝[≠] (-(k : ℂ))) := by
      apply tendsto_nhdsWithin_of_tendsto_nhds_of_eventually_within
      · have : Tendsto (fun z : ℂ => z + 1) (𝓝 (-((k + 1 : ℕ) : ℂ)))
            (𝓝 (-((k + 1 : ℕ) : ℂ) + 1)) := (continuous_id.add continuous_const).tendsto _
        rw [show -((k + 1 : ℕ) : ℂ) + 1 = -(k : ℂ) by push_cast; ring] at this
        exact this.mono_left nhdsWithin_le_nhds
      · filter_upwards [self_mem_nhdsWithin] with z hz
        intro h
        apply hz
        simp only [Set.mem_singleton_iff] at h ⊢
        push_cast
        linear_combination h
    have h1 := ih.comp hshift
    have hne : (-((k + 1 : ℕ) : ℂ)) ≠ 0 := by
      push_cast; intro h; have := congrArg Complex.re h; simp at this; linarith
    have h2 : Tendsto (fun z : ℂ => z⁻¹) (𝓝[≠] (-((k + 1 : ℕ) : ℂ))) (𝓝 ((-((k + 1 : ℕ) : ℂ))⁻¹)) :=
      ((continuousAt_inv₀ hne).tendsto).mono_left nhdsWithin_le_nhds
    have h3 := h1.mul h2
    have hlim : (-1 : ℂ) ^ k / k ! * (-((k + 1 : ℕ) : ℂ))⁻¹ = (-1) ^ (k + 1) / (k + 1)! := by
      rw [Nat.factorial_succ]; push_cast
      have : (k : ℂ) + 1 ≠ 0 := by exact_mod_cast Nat.succ_ne_zero k
      have : (k ! : ℂ) ≠ 0 := by exact_mod_cast Nat.factorial_ne_zero k
      field_simp; ring
    rw [hlim] at h3
    refine h3.congr' ?_
    have hev : ∀ᶠ z in 𝓝[≠] (-((k + 1 : ℕ) : ℂ)), z ≠ 0 :=
      nhdsWithin_le_nhds ((isOpen_ne).mem_nhds hne)
    filter_upwards [hev] with z hz
    simp only [Function.comp_apply]
    rw [Gamma_add_one z hz]
    push_cast
    field_simp
    ring

/-- Residue of `F` at `s = −a − k` (limit form), for every `k ∈ ℕ`. -/
theorem F_residue (a b : ℝ) (k : ℕ) :
    Tendsto (fun s : ℂ => (s + (a + k)) * F a b s) (𝓝[≠] (-(a : ℂ) - k))
      (𝓝 ((-1) ^ k / k ! * (Gamma (a + b) / Gamma a) * (Gamma (b - k))⁻¹)) := by
  have hshift : Tendsto (fun s : ℂ => (a : ℂ) + s) (𝓝[≠] (-(a : ℂ) - k)) (𝓝[≠] (-(k : ℂ))) := by
    apply tendsto_nhdsWithin_of_tendsto_nhds_of_eventually_within
    · have : Tendsto (fun s : ℂ => (a : ℂ) + s) (𝓝 (-(a : ℂ) - k)) (𝓝 ((a : ℂ) + (-(a : ℂ) - k))) :=
        (continuous_const.add continuous_id).tendsto _
      rw [show (a : ℂ) + (-(a : ℂ) - k) = -(k : ℂ) by ring] at this
      exact this.mono_left nhdsWithin_le_nhds
    · filter_upwards [self_mem_nhdsWithin] with z hz
      intro h
      apply hz
      simp only [Set.mem_singleton_iff] at h ⊢
      linear_combination h
  have P1 := (tendsto_Gamma_neg_nat k).comp hshift
  have P2 : Tendsto (fun s : ℂ => (Gamma (a + b + s))⁻¹) (𝓝[≠] (-(a : ℂ) - k))
      (𝓝 ((Gamma (b - k))⁻¹)) := by
    have hc : Continuous fun s : ℂ => (Gamma (a + b + s))⁻¹ :=
      differentiable_one_div_Gamma.continuous.comp (continuous_const.add continuous_id)
    have := hc.tendsto (-(a : ℂ) - k)
    rw [show (a : ℂ) + b + (-(a : ℂ) - k) = b - k by ring] at this
    exact this.mono_left nhdsWithin_le_nhds
  have P := (tendsto_const_nhds (x := Gamma (a + b) / Gamma a)).mul (P1.mul P2)
  refine (P.congr' (Eventually.of_forall fun s => ?_)).trans ?_
  · simp only [Function.comp_apply]
    unfold F
    rw [div_eq_mul_inv, div_eq_mul_inv, mul_inv]
    ring
  · rw [show Gamma (↑a + ↑b) / Gamma ↑a * ((-1) ^ k / ↑k ! * (Gamma (↑b - ↑k))⁻¹) =
        (-1) ^ k / ↑k ! * (Gamma (↑a + ↑b) / Gamma ↑a) * (Gamma (↑b - ↑k))⁻¹ by ring]

/-- If `b ∉ ℤ`, the residue at `−a − k` is non-zero (so the pole is simple and present). -/
theorem F_residue_ne_zero {a b : ℝ} (ha : 0 < a) (hb : 0 < b) (hbZ : ∀ n : ℤ, b ≠ n) (k : ℕ) :
    (-1) ^ k / k ! * (Gamma (a + b) / Gamma a) * (Gamma (b - k))⁻¹ ≠ 0 := by
  have h1 : (-1 : ℂ) ^ k / k ! ≠ 0 := by
    apply div_ne_zero (pow_ne_zero _ (by norm_num))
    exact_mod_cast Nat.factorial_ne_zero k
  have h2 : Gamma ((a : ℂ) + b) ≠ 0 := Gamma_ne_zero_of_re_pos (by simp; linarith)
  have h3 : Gamma (a : ℂ) ≠ 0 := Gamma_ne_zero_of_re_pos (re_pos_of ha)
  have h4 : Gamma ((b : ℂ) - k) ≠ 0 := by
    apply Gamma_ne_zero
    intro m hm
    have hre := congrArg Complex.re hm
    simp at hre
    exact hbZ ((k : ℤ) - m) (by push_cast; linarith)
  exact mul_ne_zero (mul_ne_zero h1 (div_ne_zero h2 h3)) (inv_ne_zero h4)

/-- Rational case `b = n ∈ ℕ`: `F(s) = Γ(a+n)/Γ(a) · (∏_{i<n}(a+s+i))⁻¹` for `a + s ∉ −ℕ`. -/
theorem F_rational (a : ℝ) (n : ℕ) {s : ℂ} (hs : ∀ m : ℕ, (a : ℂ) + s ≠ -m) :
    F a n s = Gamma (a + n) / Gamma a * (∏ i ∈ Finset.range n, ((a : ℂ) + s + i))⁻¹ := by
  have hp : (ascPochhammer ℂ n).eval ((a : ℂ) + s) = ∏ i ∈ Finset.range n, ((a : ℂ) + s + i) := by
    induction n with
    | zero => simp
    | succ n ih =>
      rw [ascPochhammer_succ_right, Polynomial.eval_mul, ih, Finset.prod_range_succ]
      simp
  have hq := Gamma_add_nat_div_Gamma_eq (n := n) ((a : ℂ) + s) hs
  rw [hp] at hq
  have hG : Gamma ((a : ℂ) + s) ≠ 0 := Gamma_ne_zero hs
  unfold F
  push_cast
  rw [show (a : ℂ) + n + s = a + s + n by ring, ← hq]
  rw [div_eq_mul_inv, div_eq_mul_inv, div_eq_mul_inv, mul_inv, mul_inv, inv_inv]
  field_simp

/-! ### Non-vacuity witness (independent evaluation of both sides) -/

/-- `a = b = 1` (uniform law on `[0,1]`), `s = 1`: the integral side is computed directly as
`∫₀¹ x dx = 1/2`, and the closed form gives `Γ(2)Γ(2)/(Γ(1)Γ(3)) = 1/2`. -/
example : M 1 1 1 = 1 / 2 ∧ F 1 1 1 = 1 / 2 := by
  have hF : F 1 1 1 = 1 / 2 := by
    unfold F
    push_cast
    norm_num [Complex.Gamma_ofNat_eq_factorial, Complex.Gamma_one]
  refine ⟨?_, hF⟩
  unfold M
  have hI : (∫ x : ℝ in (0 : ℝ)..1,
      (x : ℂ) ^ (1 : ℂ) * ((x : ℂ) ^ (((1 : ℝ) : ℂ) - 1) * (1 - (x : ℂ)) ^ (((1 : ℝ) : ℂ) - 1))) =
      1 / 2 := by
    simp only [ofReal_one, sub_self, cpow_zero, mul_one, cpow_one]
    rw [intervalIntegral.integral_ofReal, integral_id]
    norm_num
  rw [hI]
  push_cast
  norm_num [Complex.Gamma_ofNat_eq_factorial, Complex.Gamma_one]

/-! ### Mutant proved false: dropping the constant `Γ(α₀)/Γ(α_j)` -/

/-- Mutant: `M(s) = Γ(a+s)/Γ(a+b+s)`. False at `a = 2`, `b = 1`, `s = 1`: the true value is
`Γ(3)Γ(3)/(Γ(2)Γ(4)) = 2/3`, the mutant gives `Γ(3)/Γ(4) = 1/3`. -/
theorem mutant_no_constant_false :
    ¬ (∀ (a b : ℝ) (s : ℂ), 0 < a → 0 < b → -a < s.re →
        M a b s = Gamma (a + s) / Gamma (a + b + s)) := by
  intro h
  have h1 := h 2 1 1 (by norm_num) (by norm_num) (by norm_num)
  rw [coordinate_mellin (by norm_num) (by norm_num) (by norm_num), F] at h1
  push_cast at h1
  norm_num [Complex.Gamma_ofNat_eq_factorial] at h1

end LeanReal.BeyondSpectrum3T3

#print axioms LeanReal.BeyondSpectrum3T3.coordinate_mellin
#print axioms LeanReal.BeyondSpectrum3T3.beta_normalization
#print axioms LeanReal.BeyondSpectrum3T3.F_differentiableAt
#print axioms LeanReal.BeyondSpectrum3T3.tendsto_Gamma_neg_nat
#print axioms LeanReal.BeyondSpectrum3T3.F_residue
#print axioms LeanReal.BeyondSpectrum3T3.F_residue_ne_zero
#print axioms LeanReal.BeyondSpectrum3T3.F_rational
#print axioms LeanReal.BeyondSpectrum3T3.mutant_no_constant_false
