import LeanReal.BeyondSpectrum2_G3
import LeanReal.Chap09Winding

/-!
# L2 review, round 5: extra witnesses and mutants (G3 and L5)

Written by the independent layer-2 reviewer (`L2_FIDELIDADE_RODADA5.md`). The two reviewed
modules are not modified.

* G3: a mutant for part (a) (sign flipped), which the module did not have; and a witness of
  degree `-1` (orientation reversed), so `cocycle_c` is seen to track the sign of the degree.
* L5: a witness with NON-ZERO curvature and NON-ZERO winding (the unit circle about `c = 0`,
  one full turn), for `winding_total_curvature` and for `winding_bound` with `w = 1`; the
  module's line witness has `κ = 0`.
-/

noncomputable section

namespace LeanReal.L2_Rodada5_Extra

section G3
open MeasureTheory Complex Matrix
open LeanReal.BeyondSpectrum2_G3

/-! ## G3 -/

/-- Mutant: (a) with the opposite sign, `τ₂ = +(1/2π)∫Φ₀∇Φ₁·∇Φ₂`. False on the module's witness
at `(i,j,k) = (0,1,1)`: there `∫Φ₀∇Φ₁·∇Φ₂ = 4π`, so (a) gives `-2` and the mutant `+2`. -/
theorem mutant_sign_a_false :
    ¬ (∀ (μ : Measure Unit) (Φ : Fin 3 → Unit → ℝ) (dΦ : Fin 3 → Unit → Fin 2 → ℝ)
        (τ : Fin 3 → Fin 3 → Fin 3 → ℂ),
        (∀ i j k, τ i j k =
          connesConst * ∫ x, trace (symbolG (Φ i x) (dΦ j x) (dΦ k x)) ∂μ) →
        ∀ i j k, τ i j k = (1 / (2 * Real.pi)) *
          ((∫ x, Φ i x * (dΦ j x ⬝ᵥ dΦ k x) ∂μ : ℝ) : ℂ)) := by
  intro h
  have hπ : (Real.pi : ℂ) ≠ 0 := ofReal_ne_zero.mpr Real.pi_ne_zero
  have h1 := h wμ wΦ wdΦ wτ (fun _ _ _ => rfl) 0 1 1
  rw [cocycle_a wμ wΦ wdΦ wτ (fun _ _ _ => rfl) 0 1 1] at h1
  have hval : (∫ x, wΦ 0 x * (wdΦ 1 x ⬝ᵥ wdΦ 1 x) ∂wμ) = 4 * Real.pi := by
    rw [wμ, integral_smul_measure, integral_dirac]
    simp [wΦ, wdΦ, dotProduct, Real.pi_pos.le]
  rw [hval] at h1
  have e : (1 / (2 * Real.pi) : ℂ) * ((4 * Real.pi : ℝ) : ℂ) = 2 := by
    push_cast; field_simp; ring
  rw [neg_mul, e] at h1
  have h3 : (4 : ℂ) = 0 := by linear_combination -h1
  norm_num at h3

/-- Witness data with reversed orientation: `F = e₀`, `∂₁F = e₂`, `∂₂F = e₁`. -/
def vdΦ : Fin 3 → Unit → Fin 2 → ℝ := fun j _ μ => if (j : ℕ) = 2 - (μ : ℕ) then 1 else 0

def vτγ : Fin 3 → Fin 3 → Fin 3 → ℂ := fun i j k =>
  connesConst * ∫ x, trace (grading * symbolG (wΦ i x) (vdΦ j x) (vdΦ k x)) ∂wμ

theorem v_degree : ∫ x, (fun j => wΦ j x) ⬝ᵥ ((fun j => vdΦ j x 0) ⨯₃ (fun j => vdΦ j x 1)) ∂wμ
    = 4 * Real.pi * ((-1 : ℤ) : ℝ) := by
  rw [wμ, integral_smul_measure, integral_dirac]
  simp [wΦ, vdΦ, cross_apply, dotProduct, Real.pi_pos.le]

/-- **Witness of degree `-1`**: `cocycle_c` applies and gives `(i/4)∑ sgn σ τ^γ = -1`. -/
theorem witness_degree_minus_one :
    I / 4 * ∑ σ : Equiv.Perm (Fin 3),
      ((Equiv.Perm.sign σ : ℤ) : ℂ) * vτγ (σ 0) (σ 1) (σ 2) = ((-1 : ℤ) : ℂ) :=
  cocycle_c wμ wΦ vdΦ vτγ (fun _ _ _ => rfl) (fun _ _ _ => Integrable.of_finite) (-1) v_degree

end G3

/-! ## L5: the unit circle about `c = 0` -/

open Real Set MeasureTheory

section Circle
open LeanReal.Chap09Winding

/-- All hypotheses of `winding_total_curvature` for `γ(s) = (cos s, sin s)`, `c = 0`, `r = 1`,
`θ = s`, `θ' = 1`, `φ = s + π/2`, `κ = 1`, on `[0, ℓ]` for every `ℓ ≥ 0`. -/
theorem circle_hyps (ℓ : ℝ) :
    ContinuousOn (fun s : ℝ => (cos s, sin s)) (Icc 0 ℓ) ∧
    (∀ s ∈ Ioo 0 ℓ, HasDerivAt (fun s : ℝ => (cos s, sin s))
      (cos ((fun t => t + π / 2) s), sin ((fun t => t + π / 2) s)) s) ∧
    ContinuousOn (fun t : ℝ => t + π / 2) (Icc 0 ℓ) ∧
    (∀ s ∈ Ioo 0 ℓ, HasDerivAt (fun t : ℝ => t + π / 2) ((fun _ => (1:ℝ)) s) s) ∧
    ContinuousOn (fun _ : ℝ => (1:ℝ)) (Icc 0 ℓ) ∧
    (∀ s ∈ Icc 0 ℓ, (0:ℝ) < (fun _ => (1:ℝ)) s) ∧
    (∀ s ∈ Icc 0 ℓ, (fun s : ℝ => (cos s, sin s)) s =
      ((0 : ℝ × ℝ).1 + (fun _ => (1:ℝ)) s * cos (id s),
       (0 : ℝ × ℝ).2 + (fun _ => (1:ℝ)) s * sin (id s))) ∧
    ContinuousOn (id : ℝ → ℝ) (Icc 0 ℓ) ∧
    (∀ s ∈ Ioo 0 ℓ, HasDerivAt (id : ℝ → ℝ) ((fun _ => (1:ℝ)) s) s) ∧
    ContinuousOn (fun _ : ℝ => (1:ℝ)) (Icc 0 ℓ) := by
  refine ⟨(continuous_cos.prodMk continuous_sin).continuousOn, ?_,
    (continuous_id.add continuous_const).continuousOn, fun s _ => (hasDerivAt_id s).add_const _,
    continuousOn_const, fun _ _ => one_pos, fun s _ => by simp, continuous_id.continuousOn,
    fun s _ => hasDerivAt_id s, continuousOn_const⟩
  intro s _
  have := (hasDerivAt_cos s).prodMk (hasDerivAt_sin s)
  rw [cos_add_pi_div_two, sin_add_pi_div_two]
  exact this

/-- `winding_total_curvature` on one full turn of the unit circle (`κ ≡ 1 ≠ 0`):
`2π ≤ 2π + π`. -/
theorem witness_circle :
    ∫ s in (0:ℝ)..(2 * π), |(fun _ : ℝ => (1:ℝ)) s| ≤
      (∫ s in (0:ℝ)..(2 * π), |(fun _ : ℝ => (1:ℝ)) s|) + π := by
  obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9, h10⟩ := circle_hyps (2 * π)
  exact winding_total_curvature (fun s => (cos s, sin s)) 0 (fun _ => 1) id (fun _ => 1)
    (fun t => t + π / 2) (fun _ => 1) (2 * π) (by positivity) h1 h2 h3 h4 h5 h6 h7 h8 h9 h10

/-- `winding_bound` with NON-ZERO winding `w = 1` (`Δ₀ = 0`, `K = 1`, `V = 2π`): `h_winding`
holds since `θ(2π) - θ(0) = 2π`, and the conclusion is `2π ≤ 2π + π`. -/
theorem witness_circle_winding : 2 * π * |((1 : ℤ) : ℝ)| ≤ 2 * π * 1 + π + |(0:ℝ)| := by
  obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9, h10⟩ := circle_hyps (2 * π)
  exact winding_bound (fun s => (cos s, sin s)) 0 (fun _ => 1) id (fun _ => 1)
    (fun t => t + π / 2) (fun _ => 1) (2 * π) (by positivity) h1 h2 h3 h4 h5 h6 h7 h8 h9 h10
    1 (2 * π) 0 1 (fun _ _ => by simp) zero_le_one le_rfl (by simp)

end Circle

end LeanReal.L2_Rodada5_Extra

#print axioms LeanReal.L2_Rodada5_Extra.mutant_sign_a_false
#print axioms LeanReal.L2_Rodada5_Extra.witness_degree_minus_one
#print axioms LeanReal.L2_Rodada5_Extra.circle_hyps
#print axioms LeanReal.L2_Rodada5_Extra.witness_circle
#print axioms LeanReal.L2_Rodada5_Extra.witness_circle_winding
