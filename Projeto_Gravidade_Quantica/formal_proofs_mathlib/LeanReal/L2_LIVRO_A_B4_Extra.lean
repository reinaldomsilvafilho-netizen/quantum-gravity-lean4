import LeanReal.Chap01Gaussian
import LeanReal.Chap04Conservation
import LeanReal.Chap04Moments

/-!
# L2 extras for batch LIVRO_A_B4 (independent reviewer)

* `gauss_const_sharp`: the book's claim in `thm:critical_scaling`(ii) that the constant `1/2`
  in `P(|Z| > s) ≤ 2 exp(-s²/2)` cannot be increased, in full: for EVERY `c > 1/2` the bound
  `P(|Z| > s) ≤ 2 exp(-c s²)` fails for some `s ≥ 0`. The writer's mutant only treats `c = 1`.
* `nlse_witness_two_sites`: a witness for the lattice NLSE conservation theorem where the
  conclusion is not automatic. Two sites, a Hermitian matrix with non-real entries
  `D = [[0, i], [-i, 0]]`, and a solution whose site densities move (`4cos²t`, `4sin²t`)
  while the total mass stays `4`. The writer's witness has one site with `|ψ| ≡ 1`.
  This witness is linear (`κ = 0`); the writer's one-site witness has `κ = 1`.
* `msd_witness_aniso`: an anisotropic `d = 2` witness for `Chap04Moments.msd` with the book's
  form `M₂ = a·Id + b·11ᵀ` (`a = b = 1`), symbol `σ(k) = ½ kᵀM₂k`, `E = exp` (`β = 1`),
  `K = 3`, `t = 2`; it checks an OFF-DIAGONAL entry, `-∂₀∂₁û(0) = 6`, which the writer's
  `d = 1` witness cannot reach.
-/

noncomputable section

namespace LeanReal.L2_LIVRO_A_B4_Extra

open MeasureTheory ProbabilityTheory Real

/-- Lower bound of the standard normal density on `[s, s+1]`, `s ≥ 0`. -/
theorem pdf_lower_shift (s x : ℝ) (hs : 0 ≤ s) (hx : x ∈ Set.Ioo s (s + 1)) :
    (Real.sqrt (2 * π))⁻¹ * Real.exp (-((s + 1) ^ 2) / 2) ≤ gaussianPDFReal 0 1 x := by
  simp only [gaussianPDFReal, NNReal.coe_one, mul_one, sub_zero]
  obtain ⟨h1, h2⟩ := hx
  have hx2 : x ^ 2 ≤ (s + 1) ^ 2 := by nlinarith
  gcongr

/-- The constant `1/2` in the Gaussian tail `2 exp(-s²/2)` cannot be increased: for every
`c > 1/2` some `s ≥ 0` violates `P(|Z| > s) ≤ 2 exp(-c s²)`. -/
theorem gauss_const_sharp (c : ℝ) (hc : 1 / 2 < c) :
    ¬ (∀ s : ℝ, 0 ≤ s → (gaussianReal 0 1).real {x | s < |x|} ≤ 2 * Real.exp (-(c * s ^ 2))) := by
  intro h
  set δ := c - 1 / 2 with hδ
  have hδpos : 0 < δ := by linarith
  set s := 3 / δ + 3 with hsdef
  have hs0 : 0 ≤ s := by positivity
  have hs3 : 3 ≤ s := by have : 0 ≤ 3 / δ := by positivity
                         linarith
  have hδs : 3 ≤ δ * s := by
    rw [hsdef, mul_add, mul_div_cancel₀ _ hδpos.ne']; nlinarith
  have hbound := h s hs0
  set S : Set ℝ := Set.Ioo s (s + 1) with hS
  have hSsub : S ⊆ {x | s < |x|} := by
    intro x hx
    simp only [hS, Set.mem_Ioo] at hx
    simp only [Set.mem_ofPred_eq]
    rw [abs_of_pos (by linarith)]; exact hx.1
  have hvolS : volume.real S = 1 := by
    rw [hS, Real.volume_real_Ioo_of_le (by linarith)]; ring
  have hvolS' : volume S ≠ ⊤ := by rw [hS, Real.volume_Ioo]; exact ENNReal.ofReal_ne_top
  have hlow : (Real.sqrt (2 * π))⁻¹ * Real.exp (-((s + 1) ^ 2) / 2) * 1 ≤
      (gaussianReal 0 1).real S := by
    have hint := setIntegral_ge_of_const_le_real (μ := volume)
      (c := (Real.sqrt (2 * π))⁻¹ * Real.exp (-((s + 1) ^ 2) / 2)) measurableSet_Ioo hvolS'
      (fun x hx => pdf_lower_shift s x hs0 hx) (integrable_gaussianPDFReal 0 1).integrableOn
    rw [hvolS] at hint
    rw [measureReal_def, gaussianReal_apply_eq_integral 0 one_ne_zero S,
      ENNReal.toReal_ofReal (integral_nonneg fun x => gaussianPDFReal_nonneg _ _ _)]
    exact hint
  have hchain := hlow.trans ((measureReal_mono hSsub).trans hbound)
  rw [mul_one] at hchain
  have hsq : Real.sqrt (2 * π) < 2.51 := by
    rw [Real.sqrt_lt' (by norm_num)]
    linarith [Real.pi_lt_d2]
  have hsqpos : 0 < Real.sqrt (2 * π) := Real.sqrt_pos.mpr (by positivity)
  -- `exp(-(s+1)²/2) ≤ 2√(2π) exp(-c s²) < e² exp(-c s²)`
  have h1 : Real.exp (-((s + 1) ^ 2) / 2) ≤ 2 * Real.sqrt (2 * π) * Real.exp (-(c * s ^ 2)) := by
    have := mul_le_mul_of_nonneg_left hchain hsqpos.le
    rw [← mul_assoc, mul_inv_cancel₀ hsqpos.ne', one_mul] at this
    linarith
  have he2 : 2 * Real.sqrt (2 * π) < Real.exp 2 := by
    have : Real.exp 2 = Real.exp 1 * Real.exp 1 := by rw [← Real.exp_add]; norm_num
    rw [this]
    nlinarith [Real.exp_one_gt_d9]
  have h2 : Real.exp (-((s + 1) ^ 2) / 2) < Real.exp (2 + -(c * s ^ 2)) := by
    rw [Real.exp_add]
    exact h1.trans_lt (mul_lt_mul_of_pos_right he2 (Real.exp_pos _))
  rw [Real.exp_lt_exp] at h2
  -- but `c s² - (s+1)²/2 - 2 = s(δ s - 1) - 5/2 ≥ 2s - 5/2 > 0`
  have hc' : c = δ + 1 / 2 := by rw [hδ]; ring
  rw [hc'] at h2
  nlinarith [hδs, hs3]

open Complex Matrix LeanReal.Chap04Conservation

/-- Two-site Hermitian hopping matrix with non-real entries. -/
def D2 : Matrix (Fin 2) (Fin 2) ℂ := !![0, I; -I, 0]

theorem D2_hermitian : D2.IsHermitian := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [D2, Matrix.conjTranspose_apply]

/-- `ψ(t) = (2 cos t, 2 sin t)`, the superposition `e^{it}(1,-i) + e^{-it}(1,i)`. -/
def ψ2 (t : ℝ) : Fin 2 → ℂ := ![((2 * Real.cos t : ℝ) : ℂ), ((2 * Real.sin t : ℝ) : ℂ)]

def ψ2' (t : ℝ) : Fin 2 → ℂ := ![((-2 * Real.sin t : ℝ) : ℂ), ((2 * Real.cos t : ℝ) : ℂ)]

theorem ψ2_hasDerivAt (t : ℝ) (j : Fin 2) : HasDerivAt (fun t => ψ2 t j) (ψ2' t j) t := by
  fin_cases j
  · have := ((Real.hasDerivAt_cos t).const_mul 2).ofReal_comp
    simpa [ψ2, ψ2'] using this
  · have := ((Real.hasDerivAt_sin t).const_mul 2).ofReal_comp
    simpa [ψ2, ψ2'] using this

/-- `i ψ' = -(D ψ)` (`ħ = 1`, `M = 1/2`, `V = 0`, `κ = 0`, `p = 1`). -/
theorem ψ2_equation (t : ℝ) (j : Fin 2) :
    Complex.I * ((1 : ℝ) : ℂ) * ψ2' t j = Hop D2 (fun _ => 0) 1 (1 / 2) 0 1 (ψ2 t) j := by
  fin_cases j <;>
    simp [Hop, ψ2, ψ2', D2, Matrix.mulVec, dotProduct, Fin.sum_univ_two]

/-- Non-automatic witness: hypotheses of `mass_conserved` hold with a non-real Hermitian `D`,
the density at site `0` moves from `4` to `0`, and the mass equals `4` for all `t`. -/
theorem nlse_witness_two_sites :
    D2.IsHermitian ∧ (∃ i j, (D2 i j).im ≠ 0) ∧
    (∀ t j, HasDerivAt (fun t => ψ2 t j) (ψ2' t j) t) ∧
    (∀ t j, Complex.I * ((1 : ℝ) : ℂ) * ψ2' t j = Hop D2 (fun _ => 0) 1 (1 / 2) 0 1 (ψ2 t) j) ∧
    normSq (ψ2 0 0) = 4 ∧ normSq (ψ2 (π / 2) 0) = 0 ∧
    (∀ t, mass (ψ2 t) = 4) := by
  refine ⟨D2_hermitian, ⟨0, 1, by simp [D2]⟩, ψ2_hasDerivAt, ψ2_equation, ?_, ?_, ?_⟩
  · simp [ψ2]; norm_num
  · simp [ψ2]
  · intro t
    rw [mass_conserved D2 (fun _ => 0) 1 (1 / 2) 0 1 ψ2 ψ2' D2_hermitian one_ne_zero
      ψ2_hasDerivAt ψ2_equation t]
    simp [mass, ψ2, Fin.sum_univ_two]; norm_num

section Moments
open ContinuousLinearMap LeanReal.Chap04Moments

/-- Coordinate functionals on `ℝ²`. -/
def P0 : (Fin 2 → ℝ) →L[ℝ] ℝ := ContinuousLinearMap.proj 0
def P1 : (Fin 2 → ℝ) →L[ℝ] ℝ := ContinuousLinearMap.proj 1

/-- `σ(k) = k₀² + k₀k₁ + k₁² = ½ kᵀ [[2,1],[1,2]] k`. -/
def σa (k : Fin 2 → ℝ) : ℝ := k 0 ^ 2 + k 0 * k 1 + k 1 ^ 2
def σa₁ (k : Fin 2 → ℝ) : (Fin 2 → ℝ) →L[ℝ] ℝ := (2 * k 0 + k 1) • P0 + (k 0 + 2 * k 1) • P1
def σa₂ : (Fin 2 → ℝ) →L[ℝ] ((Fin 2 → ℝ) →L[ℝ] ℝ) :=
  ((2 : ℝ) • P0 + P1).smulRight P0 + (P0 + (2 : ℝ) • P1).smulRight P1

/-- `M₂ = Id + 11ᵀ`. -/
def M2a : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2]

theorem σa_hasFDerivAt (k : Fin 2 → ℝ) : HasFDerivAt σa (σa₁ k) k := by
  have h0 := P0.hasFDerivAt (x := k)
  have h1 := P1.hasFDerivAt (x := k)
  have h := ((h0.mul h0).add (h0.mul h1)).add (h1.mul h1)
  refine (h.congr_fderiv ?_).congr_of_eventuallyEq (Filter.Eventually.of_forall fun x => ?_)
  · ext v; simp [σa₁, P0, P1]; ring
  · simp [σa, P0, P1, sq]

theorem σa₁_hasFDerivAt : HasFDerivAt σa₁ σa₂ 0 := by
  have hA : HasFDerivAt (fun k : Fin 2 → ℝ => 2 * P0 k + P1 k) ((2 : ℝ) • P0 + P1) 0 :=
    (P0.hasFDerivAt.const_mul 2).add P1.hasFDerivAt
  have hB : HasFDerivAt (fun k : Fin 2 → ℝ => P0 k + 2 * P1 k) (P0 + (2 : ℝ) • P1) 0 :=
    P0.hasFDerivAt.add (P1.hasFDerivAt.const_mul 2)
  exact (hA.smul_const P0).add (hB.smul_const P1)

theorem hess_σa (i j : Fin 2) : hess σa 0 i j = (1 / (1 : ℝ) ^ 2) * M2a i j := by
  unfold hess
  rw [show fderiv ℝ σa = σa₁ from funext fun k => (σa_hasFDerivAt k).fderiv,
    σa₁_hasFDerivAt.fderiv]
  fin_cases i <;> fin_cases j <;> simp [σa₂, M2a, P0, P1]

theorem Gamma_two' : Real.Gamma ((1 : ℝ) + 1) = 1 := by
  rw [Real.Gamma_add_one one_ne_zero, Real.Gamma_one]; ring

/-- Off-diagonal entry of the MSD tensor in an anisotropic `d = 2` model:
`-∂₀∂₁ û(0) = K t^β (M₂)₀₁ / (α² Γ(β+1)) = 3·2·1 = 6`. -/
theorem msd_witness_aniso :
    -(hess (uhat Real.exp (3 * (2 : ℝ) ^ (1 : ℝ)) σa) 0 0 1) = 6 := by
  rw [msd Real.exp Real.exp (fun x => Real.hasDerivAt_exp x) (Real.exp 0) (Real.hasDerivAt_exp 0)
    σa σa₁ σa_hasFDerivAt σa₂ σa₁_hasFDerivAt (by simp [σa]) (by ext v; simp [σa₁])
    3 2 1 1 one_ne_zero (by rw [Gamma_two']; exact one_ne_zero)
    (by rw [Gamma_two']; simp) M2a hess_σa 0 1]
  rw [Gamma_two']
  simp [M2a]; norm_num

end Moments

end LeanReal.L2_LIVRO_A_B4_Extra

#print axioms LeanReal.L2_LIVRO_A_B4_Extra.gauss_const_sharp
#print axioms LeanReal.L2_LIVRO_A_B4_Extra.nlse_witness_two_sites
#print axioms LeanReal.L2_LIVRO_A_B4_Extra.msd_witness_aniso
