import Mathlib.LinearAlgebra.CrossProduct
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Analysis.Complex.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-!
# *Beyond the Spectrum* II (vol. 2), item G3: "Cocycles on `𝕋²`", combinatorial part

Source: `Manuscritos_Avulsos/paper_geometric_measures_functional_tensors/
paper_geometric_measures_functional_tensors.tex`, Proposition "Cocycles on `𝕋²`"
(`prop:cocycle`), and the first sentence of Remark `rem:tau_not_topological`.

Paper (setting, `d = 2`): `𝓗 = L²(𝕋², ℂ²)`, `𝓓 = i γ^μ ∂_μ` with `γ¹ = σ₁`, `γ² = σ₂` (Pauli),
grading `γ := -i γ¹γ² = σ₃`; `[𝓓, M_Φ] = i γ^μ ∂_μΦ`;
`τ₂(A₀,A₁,A₂) := Tr_ω(Φ₀ [𝓓,Φ₁][𝓓,Φ₂] |𝓓|⁻²)`, `τ₂^γ(A₀,A₁,A₂) := Tr_ω(γ Φ₀ [𝓓,Φ₁][𝓓,Φ₂] |𝓓|⁻²)`.

Paper (proposition):
> (a) `τ₂(A₀,A₁,A₂) = -(1/2π) ∫_{𝕋²} Φ₀ ∇Φ₁·∇Φ₂ dx`;
> (b) `τ₂^γ(A₀,A₁,A₂) = -(i/2π) ∫_{𝕋²} Φ₀ dΦ₁ ∧ dΦ₂`;
> (c) if `Φ₀² + Φ₁² + Φ₂² = 1`, so `F = (Φ₀,Φ₁,Φ₂) : 𝕋² → 𝕊²`, then
>     `(i/4) ∑_{σ ∈ S₃} sgn σ · τ₂^γ(A_{σ0}, A_{σ1}, A_{σ2}) = deg F ∈ ℤ`.

Paper's proof: Connes' trace theorem gives `Tr_ω(M_G |𝓓|⁻²) = (1/(2(2π)²))·2π ∫ tr G = (1/4π)∫ tr G`
for the smooth matrix function `G = Φ₀ (iγ^μ∂_μΦ₁)(iγ^ν∂_νΦ₂)`; then `tr(γ^μγ^ν) = 2δ^{μν}`,
`tr(γγ^μγ^ν) = 2iε^{μν}`, the antisymmetrisation `∑ sgn σ F^{σ0} dF^{σ1}∧dF^{σ2} = 2F·(∂₁F×∂₂F)`,
and `∫ F·(∂₁F×∂₂F) = 4π deg F`.

## What is formalized (the combinatorial / algebraic part)

* `clifford`, `grading_eq`, `grading_anticomm`: the Pauli matrices satisfy the Clifford relations,
  `-i γ¹γ² = σ₃`, and `σ₃` anticommutes with `γ^μ` (proved, `fin_cases`).
* `trace_gam_mul`, `trace_grading_gam_mul`: `tr(γ^μγ^ν) = 2δ^{μν}`, `tr(σ₃γ^μγ^ν) = 2iε^{μν}`.
* `trace_symbolG`, `trace_grading_symbolG`: POINTWISE, for `G = Φ₀ (i γ·p)(i γ·q)` with real
  `Φ₀` and real gradients `p = ∇Φ₁(x)`, `q = ∇Φ₂(x)`: `tr G = -2Φ₀ p·q` and
  `tr(σ₃G) = -2iΦ₀(p₁q₂ - p₂q₁)`.
* `connesConst_eq`: `(1/(2(2π)²))·|𝕊¹| = 1/(4π)` with `|𝕊¹| = 2π`.
* `cocycle_a`, `cocycle_b`: (a) and (b), for ANY measure space `(X, μ)` in place of `(𝕋², dx)`,
  CONDITIONAL on the named hypothesis `h_connes` / `h_connes_graded` (Connes' trace theorem in
  the form `τ = (1/4π)∫ tr G`). The Dixmier trace, `|𝓓|⁻²` and Connes' trace theorem are NOT in
  Mathlib and are NOT formalized.
* `antisymm_perm_three`: `∑_{σ∈S₃} sgn σ · F_{σ0}(a_{σ1}b_{σ2} - a_{σ2}b_{σ1}) = 2 F·(a×b)`.
* `cocycle_c`: (c), conditional on `h_connes_graded`, on integrability `h_int` (true for smooth
  `Φ_j` on the compact `𝕋²`), and on the named hypothesis `h_degree :
  ∫ F·(∂₁F × ∂₂F) = 4π deg F` (Mathlib has no Brouwer degree). The sphere condition
  `|F| = 1` enters ONLY through `h_degree`; the algebra does not use it, so it is not a
  separate hypothesis here.
* `ungraded_antisymm_zero`: Remark `rem:tau_not_topological`, first claim: the antisymmetrised
  ungraded `τ₂` vanishes identically (its formula is symmetric in the last two slots).

Non-vacuity: `witness_degree_one` (one-point space with mass `4π`, `F = e₀`, `∂₁F = e₁`,
`∂₂F = e₂`; all hypotheses hold and the conclusion is `1`). This only shows the hypotheses are
jointly satisfiable; it is not a map `𝕋² → 𝕊²`.
Mutants proved false: normalisation `i/2` (`mutant_half_false`), ungraded cocycle in (c)
(`mutant_ungraded_false`), sign of (b) flipped (`mutant_sign_b_false`), trace identity
`tr(σ₃γ^μγ^ν) = 2iδ^{μν}` (`mutant_trace_delta_false`).
-/

noncomputable section

namespace LeanReal.BeyondSpectrum2_G3

open Matrix Complex MeasureTheory

/-! ## Pauli matrices -/

/-- The gamma matrices for `d = 2`: `γ¹ = σ₁` (index `0`) and `γ² = σ₂` (index `1`). -/
def gam : Fin 2 → Matrix (Fin 2) (Fin 2) ℂ
  | 0 => !![0, 1; 1, 0]
  | 1 => !![0, -I; I, 0]

/-- The grading `γ = σ₃`. -/
def grading : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]

/-- Clifford relations `γ^μγ^ν + γ^νγ^μ = 2δ^{μν}`. -/
theorem clifford (μ ν : Fin 2) :
    gam μ * gam ν + gam ν * gam μ = (if μ = ν then 2 else 0) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  fin_cases μ <;> fin_cases ν <;> ext i j <;> fin_cases i <;> fin_cases j <;>
    simp [gam] <;> norm_num

/-- The paper's grading `γ := -iγ¹γ²` is `σ₃`. -/
theorem grading_eq : -I • (gam 0 * gam 1) = grading := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [gam, grading]

/-- `σ₃` anticommutes with each `γ^μ` (hence with the Dirac operator). -/
theorem grading_anticomm (μ : Fin 2) : grading * gam μ = -(gam μ * grading) := by
  fin_cases μ <;> ext i j <;> fin_cases i <;> fin_cases j <;> simp [gam, grading]

/-- `tr(γ^μγ^ν) = 2δ^{μν}`. -/
theorem trace_gam_mul (μ ν : Fin 2) : trace (gam μ * gam ν) = if μ = ν then 2 else 0 := by
  fin_cases μ <;> fin_cases ν <;> simp [gam, Matrix.trace_fin_two] <;> norm_num

/-- The Levi-Civita symbol `ε^{μν}` on `Fin 2`, with `ε^{01} = 1`. -/
def eps (μ ν : Fin 2) : ℂ := if μ = 0 ∧ ν = 1 then 1 else if μ = 1 ∧ ν = 0 then -1 else 0

/-- `tr(γγ^μγ^ν) = 2iε^{μν}`. -/
theorem trace_grading_gam_mul (μ ν : Fin 2) :
    trace (grading * (gam μ * gam ν)) = 2 * I * eps μ ν := by
  fin_cases μ <;> fin_cases ν <;> simp [gam, grading, eps, Matrix.trace_fin_two] <;> ring

/-! ## The pointwise symbol `G = Φ₀ [𝓓,Φ₁][𝓓,Φ₂]` -/

/-- `γ·p = ∑_μ p_μ γ^μ` for a real covector `p` (a gradient `∇Φ(x)`). -/
def slash (p : Fin 2 → ℝ) : Matrix (Fin 2) (Fin 2) ℂ := ∑ μ, (p μ : ℂ) • gam μ

/-- `G = Φ₀ (iγ·p)(iγ·q)`: the multiplication symbol of `Φ₀[𝓓,Φ₁][𝓓,Φ₂]` at one point, with
`p = ∇Φ₁(x)`, `q = ∇Φ₂(x)` (since `[𝓓, M_Φ] = iγ^μ∂_μΦ`). -/
def symbolG (φ₀ : ℝ) (p q : Fin 2 → ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  (φ₀ : ℂ) • ((I • slash p) * (I • slash q))

/-- `tr G = -2Φ₀ ∇Φ₁·∇Φ₂` (pointwise). -/
theorem trace_symbolG (φ₀ : ℝ) (p q : Fin 2 → ℝ) :
    trace (symbolG φ₀ p q) = ((-2 * φ₀ * (p ⬝ᵥ q) : ℝ) : ℂ) := by
  simp [symbolG, slash, gam, Matrix.trace_fin_two, Fin.sum_univ_two, dotProduct]
  ring_nf
  try simp [I_sq]
  try ring

/-- `tr(σ₃G) = -2iΦ₀(∂₁Φ₁∂₂Φ₂ - ∂₂Φ₁∂₁Φ₂)` (pointwise), i.e. `-2iΦ₀ dΦ₁∧dΦ₂ / dx₁∧dx₂`. -/
theorem trace_grading_symbolG (φ₀ : ℝ) (p q : Fin 2 → ℝ) :
    trace (grading * symbolG φ₀ p q) = -2 * I * ((φ₀ * (p 0 * q 1 - p 1 * q 0) : ℝ) : ℂ) := by
  simp [symbolG, slash, gam, grading, Matrix.trace_fin_two, Fin.sum_univ_two]
  ring_nf
  try simp
  try ring

/-! ## Connes' constant in `d = 2` -/

/-- Connes' normalisation `(1/(d(2π)^d))·|𝕊^{d-1}|` at `d = 2`, with `|𝕊¹| = 2π`
(`tr Id` is kept inside `tr G`). -/
def connesConst : ℂ := 1 / (2 * (2 * Real.pi) ^ 2) * (2 * Real.pi)

theorem connesConst_eq : connesConst = 1 / (4 * Real.pi) := by
  have : (Real.pi : ℂ) ≠ 0 := ofReal_ne_zero.mpr Real.pi_ne_zero
  unfold connesConst
  field_simp
  ring

/-! ## (a) and (b), conditional on Connes' trace theorem -/

variable {X : Type*} [MeasurableSpace X]

/-- `∫ (f x : ℂ) = ((∫ f x : ℝ) : ℂ)` (specialisation of `integral_ofReal`). -/
theorem integral_ofReal_complex (μ : Measure X) (f : X → ℝ) :
    ∫ x, (f x : ℂ) ∂μ = ((∫ x, f x ∂μ : ℝ) : ℂ) :=
  integral_ofReal

/-- **(a)**. `X` with measure `μ` stands for `(𝕋², dx)`; `Φ j : X → ℝ` are the realisations and
`dΦ j x : Fin 2 → ℝ` their gradients (given data; no differentiation is formalized).
`h_connes` is Connes' trace theorem for `M_G|𝓓|⁻²`, NOT proved here. -/
theorem cocycle_a (μ : Measure X) (Φ : Fin 3 → X → ℝ) (dΦ : Fin 3 → X → Fin 2 → ℝ)
    (τ : Fin 3 → Fin 3 → Fin 3 → ℂ)
    (h_connes : ∀ i j k, τ i j k =
      connesConst * ∫ x, trace (symbolG (Φ i x) (dΦ j x) (dΦ k x)) ∂μ)
    (i j k : Fin 3) :
    τ i j k = -(1 / (2 * Real.pi)) * ((∫ x, Φ i x * (dΦ j x ⬝ᵥ dΦ k x) ∂μ : ℝ) : ℂ) := by
  have hπ : (Real.pi : ℂ) ≠ 0 := ofReal_ne_zero.mpr Real.pi_ne_zero
  rw [h_connes, connesConst_eq]
  simp_rw [trace_symbolG]
  rw [integral_ofReal_complex]
  have : (∫ x, -2 * Φ i x * (dΦ j x ⬝ᵥ dΦ k x) ∂μ) = -2 * ∫ x, Φ i x * (dΦ j x ⬝ᵥ dΦ k x) ∂μ := by
    rw [← integral_const_mul]; congr 1; ext x; ring
  rw [this]
  push_cast
  field_simp
  ring

/-- **(b)**, conditional on `h_connes_graded` (Connes' trace theorem for `M_{γG}|𝓓|⁻²`). -/
theorem cocycle_b (μ : Measure X) (Φ : Fin 3 → X → ℝ) (dΦ : Fin 3 → X → Fin 2 → ℝ)
    (τγ : Fin 3 → Fin 3 → Fin 3 → ℂ)
    (h_connes_graded : ∀ i j k, τγ i j k =
      connesConst * ∫ x, trace (grading * symbolG (Φ i x) (dΦ j x) (dΦ k x)) ∂μ)
    (i j k : Fin 3) :
    τγ i j k = -(I / (2 * Real.pi)) *
      ((∫ x, Φ i x * (dΦ j x 0 * dΦ k x 1 - dΦ j x 1 * dΦ k x 0) ∂μ : ℝ) : ℂ) := by
  have hπ : (Real.pi : ℂ) ≠ 0 := ofReal_ne_zero.mpr Real.pi_ne_zero
  rw [h_connes_graded, connesConst_eq]
  simp_rw [trace_grading_symbolG]
  rw [integral_const_mul, integral_ofReal_complex]
  field_simp
  ring

/-! ## (c): the antisymmetrisation and the degree -/

/-- `∑_{σ∈S₃} sgn σ · F_{σ0}(a_{σ1}b_{σ2} - a_{σ2}b_{σ1}) = 2 F·(a × b)`. -/
theorem antisymm_perm_three (F a b : Fin 3 → ℝ) :
    ∑ σ : Equiv.Perm (Fin 3), ((Equiv.Perm.sign σ : ℤ) : ℝ) * (F (σ 0) *
      (a (σ 1) * b (σ 2) - a (σ 2) * b (σ 1))) = 2 * (F ⬝ᵥ (a ⨯₃ b)) := by
  have h1 : ∑ σ : Equiv.Perm (Fin 3), ((Equiv.Perm.sign σ : ℤ) : ℝ) * (F (σ 0) * a (σ 1) * b (σ 2))
      = F ⬝ᵥ (a ⨯₃ b) := by
    have e : F ⬝ᵥ (a ⨯₃ b) = (Matrix.of ![F, a, b])ᵀ.det := by
      rw [Matrix.det_transpose, triple_product_eq_det]; rfl
    rw [e, Matrix.det_apply']
    refine Finset.sum_congr rfl fun σ _ => ?_
    simp [Fin.prod_univ_three, Matrix.transpose_apply]
  have h2 : ∑ σ : Equiv.Perm (Fin 3), ((Equiv.Perm.sign σ : ℤ) : ℝ) * (F (σ 0) * b (σ 1) * a (σ 2))
      = F ⬝ᵥ (b ⨯₃ a) := by
    have e : F ⬝ᵥ (b ⨯₃ a) = (Matrix.of ![F, b, a])ᵀ.det := by
      rw [Matrix.det_transpose, triple_product_eq_det]; rfl
    rw [e, Matrix.det_apply']
    refine Finset.sum_congr rfl fun σ _ => ?_
    simp [Fin.prod_univ_three, Matrix.transpose_apply]
  rw [← cross_anticomm, dotProduct_neg] at h2
  have : ∀ σ : Equiv.Perm (Fin 3), ((Equiv.Perm.sign σ : ℤ) : ℝ) * (F (σ 0) *
      (a (σ 1) * b (σ 2) - a (σ 2) * b (σ 1)))
      = ((Equiv.Perm.sign σ : ℤ) : ℝ) * (F (σ 0) * a (σ 1) * b (σ 2)) -
        ((Equiv.Perm.sign σ : ℤ) : ℝ) * (F (σ 0) * b (σ 1) * a (σ 2)) := fun σ => by ring
  simp only [this, Finset.sum_sub_distrib, h1, h2]
  ring

/-- **(c)**, conditional on Connes' trace theorem (`h_connes_graded`), integrability (`h_int`),
and the degree formula `∫ F·(∂₁F×∂₂F) = 4π deg F` (`h_degree`, standing in for Brouwer degree
theory, absent from Mathlib). Here `F x = (Φ₀ x, Φ₁ x, Φ₂ x)`, `∂_μF x = (dΦ₀ x μ, dΦ₁ x μ, dΦ₂ x μ)`. -/
theorem cocycle_c (μ : Measure X) (Φ : Fin 3 → X → ℝ) (dΦ : Fin 3 → X → Fin 2 → ℝ)
    (τγ : Fin 3 → Fin 3 → Fin 3 → ℂ)
    (h_connes_graded : ∀ i j k, τγ i j k =
      connesConst * ∫ x, trace (grading * symbolG (Φ i x) (dΦ j x) (dΦ k x)) ∂μ)
    (h_int : ∀ i j k, Integrable (fun x => Φ i x * (dΦ j x 0 * dΦ k x 1)) μ)
    (deg : ℤ)
    (h_degree : ∫ x, (fun j => Φ j x) ⬝ᵥ ((fun j => dΦ j x 0) ⨯₃ (fun j => dΦ j x 1)) ∂μ
      = 4 * Real.pi * deg) :
    I / 4 * ∑ σ : Equiv.Perm (Fin 3),
      ((Equiv.Perm.sign σ : ℤ) : ℂ) * τγ (σ 0) (σ 1) (σ 2) = deg := by
  have hπ : (Real.pi : ℂ) ≠ 0 := ofReal_ne_zero.mpr Real.pi_ne_zero
  set f : Fin 3 → Fin 3 → Fin 3 → X → ℝ :=
    fun i j k x => Φ i x * (dΦ j x 0 * dΦ k x 1 - dΦ j x 1 * dΦ k x 0) with hf
  have hfi : ∀ i j k, Integrable (f i j k) μ := fun i j k =>
    ((h_int i j k).sub ((h_int i k j))).congr (ae_of_all _ fun x => by simp only [hf, Pi.sub_apply]; ring)
  have hb := cocycle_b μ Φ dΦ τγ h_connes_graded
  -- the real sum of integrals
  have hsum : ∑ σ : Equiv.Perm (Fin 3), ((Equiv.Perm.sign σ : ℤ) : ℝ) * ∫ x, f (σ 0) (σ 1) (σ 2) x ∂μ
      = 2 * (4 * Real.pi * deg) := by
    calc ∑ σ : Equiv.Perm (Fin 3), ((Equiv.Perm.sign σ : ℤ) : ℝ) * ∫ x, f (σ 0) (σ 1) (σ 2) x ∂μ
        = ∑ σ : Equiv.Perm (Fin 3), ∫ x, ((Equiv.Perm.sign σ : ℤ) : ℝ) * f (σ 0) (σ 1) (σ 2) x ∂μ := by
          simp_rw [integral_const_mul]
      _ = ∫ x, ∑ σ : Equiv.Perm (Fin 3), ((Equiv.Perm.sign σ : ℤ) : ℝ) * f (σ 0) (σ 1) (σ 2) x ∂μ :=
          (integral_finsetSum _ fun σ _ => (hfi _ _ _).const_mul _).symm
      _ = ∫ x, 2 * ((fun j => Φ j x) ⬝ᵥ ((fun j => dΦ j x 0) ⨯₃ (fun j => dΦ j x 1))) ∂μ := by
          congr 1; ext x
          rw [← antisymm_perm_three (fun j => Φ j x) (fun j => dΦ j x 0) (fun j => dΦ j x 1)]
          refine Finset.sum_congr rfl fun σ _ => ?_
          simp only [hf]
          ring
      _ = 2 * (4 * Real.pi * deg) := by rw [integral_const_mul, h_degree]
  have : ∑ σ : Equiv.Perm (Fin 3), ((Equiv.Perm.sign σ : ℤ) : ℂ) * τγ (σ 0) (σ 1) (σ 2)
      = -(I / (2 * Real.pi)) * ((2 * (4 * Real.pi * deg) : ℝ) : ℂ) := by
    rw [← hsum]
    simp only [hb]
    push_cast
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl fun σ _ => ?_
    simp only [hf]
    ring
  rw [this]
  push_cast
  field_simp
  ring_nf
  simp [I_sq]

/-- **Remark `rem:tau_not_topological`, first claim**: under `h_connes` the antisymmetrised
ungraded cochain vanishes, so `τ₂` cannot detect the degree. -/
theorem ungraded_antisymm_zero (μ : Measure X) (Φ : Fin 3 → X → ℝ) (dΦ : Fin 3 → X → Fin 2 → ℝ)
    (τ : Fin 3 → Fin 3 → Fin 3 → ℂ)
    (h_connes : ∀ i j k, τ i j k =
      connesConst * ∫ x, trace (symbolG (Φ i x) (dΦ j x) (dΦ k x)) ∂μ) :
    ∑ σ : Equiv.Perm (Fin 3), ((Equiv.Perm.sign σ : ℤ) : ℂ) * τ (σ 0) (σ 1) (σ 2) = 0 := by
  have hsym : ∀ i j k, τ i j k = τ i k j := by
    intro i j k
    rw [cocycle_a μ Φ dΦ τ h_connes, cocycle_a μ Φ dΦ τ h_connes]
    simp_rw [dotProduct_comm (dΦ j _)]
  set S := ∑ σ : Equiv.Perm (Fin 3), ((Equiv.Perm.sign σ : ℤ) : ℂ) * τ (σ 0) (σ 1) (σ 2) with hS
  have h := Equiv.sum_comp (Equiv.mulRight (Equiv.swap (1 : Fin 3) 2))
    (fun σ : Equiv.Perm (Fin 3) => ((Equiv.Perm.sign σ : ℤ) : ℂ) * τ (σ 0) (σ 1) (σ 2))
  have hneg : S = -S := by
    calc S = ∑ σ : Equiv.Perm (Fin 3),
          ((Equiv.Perm.sign (σ * Equiv.swap (1 : Fin 3) 2) : ℤ) : ℂ) *
            τ ((σ * Equiv.swap (1 : Fin 3) 2) 0) ((σ * Equiv.swap (1 : Fin 3) 2) 1)
              ((σ * Equiv.swap (1 : Fin 3) 2) 2) := by rw [hS]; exact h.symm
      _ = ∑ σ : Equiv.Perm (Fin 3), -(((Equiv.Perm.sign σ : ℤ) : ℂ) * τ (σ 0) (σ 1) (σ 2)) := by
          refine Finset.sum_congr rfl fun σ _ => ?_
          rw [Equiv.Perm.sign_mul, Equiv.Perm.sign_swap (by decide)]
          have e0 : Equiv.swap (1 : Fin 3) 2 0 = 0 := by decide
          have e1 : Equiv.swap (1 : Fin 3) 2 1 = 2 := by decide
          have e2 : Equiv.swap (1 : Fin 3) 2 2 = 1 := by decide
          simp only [Equiv.Perm.coe_mul, Function.comp_apply, e0, e1, e2]
          rw [hsym (σ 0) (σ 2) (σ 1)]
          push_cast
          ring
      _ = -S := by rw [Finset.sum_neg_distrib, hS]
  have : (2 : ℂ) * S = 0 := by linear_combination hneg
  simpa using this

/-! ## Non-vacuity witness: a one-point space of mass `4π` with `F = e₀`, `∂₁F = e₁`, `∂₂F = e₂` -/

/-- The witness measure: `4π · δ_{()}` on `Unit`. -/
def wμ : Measure Unit := ENNReal.ofReal (4 * Real.pi) • Measure.dirac ()

/-- `Φ_j = δ_{j0}` (so `F = e₀`, on the unit sphere). -/
def wΦ : Fin 3 → Unit → ℝ := fun j _ => if j = 0 then 1 else 0

/-- `∂_μΦ_j = δ_{j,μ+1}` (so `∂₁F = e₁`, `∂₂F = e₂`). -/
def wdΦ : Fin 3 → Unit → Fin 2 → ℝ := fun j _ μ => if (j : ℕ) = (μ : ℕ) + 1 then 1 else 0

/-- The graded cochain defined by Connes' formula on the witness data. -/
def wτγ : Fin 3 → Fin 3 → Fin 3 → ℂ := fun i j k =>
  connesConst * ∫ x, trace (grading * symbolG (wΦ i x) (wdΦ j x) (wdΦ k x)) ∂wμ

/-- The ungraded cochain defined by Connes' formula on the witness data. -/
def wτ : Fin 3 → Fin 3 → Fin 3 → ℂ := fun i j k =>
  connesConst * ∫ x, trace (symbolG (wΦ i x) (wdΦ j x) (wdΦ k x)) ∂wμ

instance : IsFiniteMeasure wμ := ⟨by simp [wμ]; finiteness⟩

theorem w_int : ∀ i j k, Integrable (fun x => wΦ i x * (wdΦ j x 0 * wdΦ k x 1)) wμ :=
  fun _ _ _ => Integrable.of_finite

theorem w_sphere (x : Unit) : wΦ 0 x ^ 2 + wΦ 1 x ^ 2 + wΦ 2 x ^ 2 = 1 := by
  simp [wΦ]

theorem w_degree : ∫ x, (fun j => wΦ j x) ⬝ᵥ ((fun j => wdΦ j x 0) ⨯₃ (fun j => wdΦ j x 1)) ∂wμ
    = 4 * Real.pi * ((1 : ℤ) : ℝ) := by
  rw [wμ, integral_smul_measure, integral_dirac]
  simp [wΦ, wdΦ, cross_apply, dotProduct, Real.pi_pos.le]

/-- **Witness**: all hypotheses of `cocycle_c` hold on the witness data with `deg = 1`, and the
conclusion `(i/4)∑ sgn σ τ^γ = 1` follows. -/
theorem witness_degree_one :
    I / 4 * ∑ σ : Equiv.Perm (Fin 3),
      ((Equiv.Perm.sign σ : ℤ) : ℂ) * wτγ (σ 0) (σ 1) (σ 2) = ((1 : ℤ) : ℂ) :=
  cocycle_c wμ wΦ wdΦ wτγ (fun _ _ _ => rfl) w_int 1 w_degree

/-! ## Mutants proved false -/

/-- Mutant 1: normalisation `i/2` instead of `i/4` in (c). False (witness gives `2 ≠ 1`). -/
theorem mutant_half_false :
    ¬ (∀ (μ : Measure Unit) (Φ : Fin 3 → Unit → ℝ) (dΦ : Fin 3 → Unit → Fin 2 → ℝ)
        (τγ : Fin 3 → Fin 3 → Fin 3 → ℂ),
        (∀ i j k, τγ i j k =
          connesConst * ∫ x, trace (grading * symbolG (Φ i x) (dΦ j x) (dΦ k x)) ∂μ) →
        (∀ i j k, Integrable (fun x => Φ i x * (dΦ j x 0 * dΦ k x 1)) μ) →
        ∀ deg : ℤ, (∫ x, (fun j => Φ j x) ⬝ᵥ ((fun j => dΦ j x 0) ⨯₃ (fun j => dΦ j x 1)) ∂μ
          = 4 * Real.pi * deg) →
        I / 2 * ∑ σ : Equiv.Perm (Fin 3),
          ((Equiv.Perm.sign σ : ℤ) : ℂ) * τγ (σ 0) (σ 1) (σ 2) = deg) := by
  intro h
  have h1 := h wμ wΦ wdΦ wτγ (fun _ _ _ => rfl) w_int 1 w_degree
  have h2 := witness_degree_one
  have : I / 2 * ∑ σ : Equiv.Perm (Fin 3), ((Equiv.Perm.sign σ : ℤ) : ℂ) * wτγ (σ 0) (σ 1) (σ 2)
      = 2 * (I / 4 * ∑ σ : Equiv.Perm (Fin 3),
        ((Equiv.Perm.sign σ : ℤ) : ℂ) * wτγ (σ 0) (σ 1) (σ 2)) := by ring
  rw [this, h2] at h1
  norm_num at h1

/-- Mutant 2: the UNGRADED cochain in (c). False: its antisymmetrisation is `0`, while the
witness has degree `1`. -/
theorem mutant_ungraded_false :
    ¬ (∀ (μ : Measure Unit) (Φ : Fin 3 → Unit → ℝ) (dΦ : Fin 3 → Unit → Fin 2 → ℝ)
        (τ : Fin 3 → Fin 3 → Fin 3 → ℂ),
        (∀ i j k, τ i j k =
          connesConst * ∫ x, trace (symbolG (Φ i x) (dΦ j x) (dΦ k x)) ∂μ) →
        (∀ i j k, Integrable (fun x => Φ i x * (dΦ j x 0 * dΦ k x 1)) μ) →
        ∀ deg : ℤ, (∫ x, (fun j => Φ j x) ⬝ᵥ ((fun j => dΦ j x 0) ⨯₃ (fun j => dΦ j x 1)) ∂μ
          = 4 * Real.pi * deg) →
        I / 4 * ∑ σ : Equiv.Perm (Fin 3),
          ((Equiv.Perm.sign σ : ℤ) : ℂ) * τ (σ 0) (σ 1) (σ 2) = deg) := by
  intro h
  have h1 := h wμ wΦ wdΦ wτ (fun _ _ _ => rfl) w_int 1 w_degree
  rw [ungraded_antisymm_zero wμ wΦ wdΦ wτ (fun _ _ _ => rfl)] at h1
  norm_num at h1

/-- Mutant 3: (b) with the opposite sign, `τ^γ = +(i/2π)∫Φ₀dΦ₁∧dΦ₂`. False on the witness
(`τ^γ(0,1,2) = -2i ≠ 2i`). -/
theorem mutant_sign_b_false :
    ¬ (∀ (μ : Measure Unit) (Φ : Fin 3 → Unit → ℝ) (dΦ : Fin 3 → Unit → Fin 2 → ℝ)
        (τγ : Fin 3 → Fin 3 → Fin 3 → ℂ),
        (∀ i j k, τγ i j k =
          connesConst * ∫ x, trace (grading * symbolG (Φ i x) (dΦ j x) (dΦ k x)) ∂μ) →
        ∀ i j k, τγ i j k = (I / (2 * Real.pi)) *
          ((∫ x, Φ i x * (dΦ j x 0 * dΦ k x 1 - dΦ j x 1 * dΦ k x 0) ∂μ : ℝ) : ℂ)) := by
  intro h
  have hπ : (Real.pi : ℂ) ≠ 0 := ofReal_ne_zero.mpr Real.pi_ne_zero
  have h1 := h wμ wΦ wdΦ wτγ (fun _ _ _ => rfl) 0 1 2
  rw [cocycle_b wμ wΦ wdΦ wτγ (fun _ _ _ => rfl) 0 1 2] at h1
  have hval : (∫ x, wΦ 0 x * (wdΦ 1 x 0 * wdΦ 2 x 1 - wdΦ 1 x 1 * wdΦ 2 x 0) ∂wμ) = 4 * Real.pi := by
    rw [wμ, integral_smul_measure, integral_dirac]
    simp [wΦ, wdΦ, Real.pi_pos.le]
  rw [hval] at h1
  have : (I / (2 * Real.pi)) * ((4 * Real.pi : ℝ) : ℂ) = 2 * I := by
    push_cast; field_simp; ring
  rw [neg_mul, this] at h1
  have h3 : (4 : ℂ) * I = 0 := by linear_combination -h1
  simp at h3

/-- Mutant 4: `tr(σ₃γ^μγ^ν) = 2iδ^{μν}` (delta instead of epsilon). False at `μ = ν = 0`. -/
theorem mutant_trace_delta_false :
    ¬ (∀ μ ν : Fin 2, trace (grading * (gam μ * gam ν)) = 2 * I * (if μ = ν then 1 else 0)) := by
  intro h
  have h1 := h 0 0
  rw [trace_grading_gam_mul] at h1
  simp [eps] at h1

end LeanReal.BeyondSpectrum2_G3

#print axioms LeanReal.BeyondSpectrum2_G3.clifford
#print axioms LeanReal.BeyondSpectrum2_G3.grading_eq
#print axioms LeanReal.BeyondSpectrum2_G3.grading_anticomm
#print axioms LeanReal.BeyondSpectrum2_G3.trace_gam_mul
#print axioms LeanReal.BeyondSpectrum2_G3.trace_grading_gam_mul
#print axioms LeanReal.BeyondSpectrum2_G3.trace_symbolG
#print axioms LeanReal.BeyondSpectrum2_G3.trace_grading_symbolG
#print axioms LeanReal.BeyondSpectrum2_G3.connesConst_eq
#print axioms LeanReal.BeyondSpectrum2_G3.cocycle_a
#print axioms LeanReal.BeyondSpectrum2_G3.cocycle_b
#print axioms LeanReal.BeyondSpectrum2_G3.antisymm_perm_three
#print axioms LeanReal.BeyondSpectrum2_G3.cocycle_c
#print axioms LeanReal.BeyondSpectrum2_G3.ungraded_antisymm_zero
#print axioms LeanReal.BeyondSpectrum2_G3.w_sphere
#print axioms LeanReal.BeyondSpectrum2_G3.w_degree
#print axioms LeanReal.BeyondSpectrum2_G3.witness_degree_one
#print axioms LeanReal.BeyondSpectrum2_G3.mutant_half_false
#print axioms LeanReal.BeyondSpectrum2_G3.mutant_ungraded_false
#print axioms LeanReal.BeyondSpectrum2_G3.mutant_sign_b_false
#print axioms LeanReal.BeyondSpectrum2_G3.mutant_trace_delta_false
