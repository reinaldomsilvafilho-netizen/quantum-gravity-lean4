import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Analysis.Complex.Basic

/-!
# *Functorial Bridge* (Zenodo concept DOI 10.5281/zenodo.22441676), item R2

Source: `Manuscritos_Avulsos/paper_functorial_tensor_field_theory/paper_functorial_tensor_field_theory.tex`,
Proposition `prop:nec` ("Null energy identity"), with `T_{μν}` defined in eq. `eq:tmunu`:
> `X_{μν} = Re Tr(∂_μΨ† ∂_νΨ)`,
> `T_{μν}[Ψ] = X_{μν} − ½ g_{μν}(g^{αβ}X_{αβ} + Tr V(Ψ))`.
> For every null vector `k` (`g_{μν}k^μk^ν = 0`), every smooth `Ψ` and every potential `V`,
> `T_{μν}[Ψ]k^μk^ν = ‖k^μ∂_μΨ‖²_HS ≥ 0`.

Formal version (`null_energy_identity`, `null_energy_nonneg`). Declared reduction:
* The identity is POINTWISE. At a fixed spacetime point the data are: the `n` matrices
  `dΨ μ = ∂_μΨ ∈ Mat_χ(ℂ)` (arbitrary, not derived from a field), arbitrary real matrices `g` and
  `gInv` (no symmetry, invertibility, signature or `gInv = g⁻¹` is assumed, so this is more
  general than the paper), and the real number `trV` standing for `Tr V(Ψ)` (real because `V` is
  Hermitian-valued). The spacetime dimension `n` is arbitrary (the paper has `n = 4`).
* `‖A‖²_HS` is written out as `∑_{i,j} |A_{ij}|²`; we also prove it equals `Re Tr(A†A)`.
* NOT covered: manifolds, smoothness of `Ψ`, the Hilbert-tensor derivation of `T_{μν}`, the ADM
  densities, any Einstein equation.
-/

namespace LeanReal.FunctorialBridge2

open Matrix BigOperators

variable {n χ : ℕ}

/-- `X_{μν} = Re Tr(∂_μΨ† ∂_νΨ)`. -/
noncomputable def X (dΨ : Fin n → Matrix (Fin χ) (Fin χ) ℂ) (μ ν : Fin n) : ℝ :=
  (trace ((dΨ μ)ᴴ * dΨ ν)).re

/-- Eq. `eq:tmunu`. -/
noncomputable def T (g gInv : Matrix (Fin n) (Fin n) ℝ) (trV : ℝ)
    (dΨ : Fin n → Matrix (Fin χ) (Fin χ) ℂ) (μ ν : Fin n) : ℝ :=
  X dΨ μ ν - 1 / 2 * g μ ν * ((∑ α, ∑ β, gInv α β * X dΨ α β) + trV)

/-- `k^μ ∂_μΨ`. -/
noncomputable def kDeriv (k : Fin n → ℝ) (dΨ : Fin n → Matrix (Fin χ) (Fin χ) ℂ) :
    Matrix (Fin χ) (Fin χ) ℂ :=
  ∑ μ, ((k μ : ℂ)) • dΨ μ

/-- Squared Hilbert–Schmidt norm, written out. -/
noncomputable def hsSq (A : Matrix (Fin χ) (Fin χ) ℂ) : ℝ := ∑ i, ∑ j, Complex.normSq (A i j)

lemma hsSq_eq_re_trace (A : Matrix (Fin χ) (Fin χ) ℂ) : hsSq A = (trace (Aᴴ * A)).re := by
  simp only [hsSq, trace, diag, mul_apply, conjTranspose_apply, Complex.re_sum]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
  rw [Complex.normSq_apply]
  simp [Complex.mul_re]

lemma X_symm (dΨ : Fin n → Matrix (Fin χ) (Fin χ) ℂ) (μ ν : Fin n) : X dΨ μ ν = X dΨ ν μ := by
  have h : (dΨ ν)ᴴ * dΨ μ = ((dΨ μ)ᴴ * dΨ ν)ᴴ := by
    rw [conjTranspose_mul, conjTranspose_conjTranspose]
  simp only [X, h, trace_conjTranspose, Complex.star_def, Complex.conj_re]

lemma kk_X (k : Fin n → ℝ) (dΨ : Fin n → Matrix (Fin χ) (Fin χ) ℂ) :
    ∑ μ, ∑ ν, X dΨ μ ν * k μ * k ν = (trace ((kDeriv k dΨ)ᴴ * kDeriv k dΨ)).re := by
  simp only [kDeriv, conjTranspose_sum, conjTranspose_smul, Finset.sum_mul, Finset.mul_sum,
    trace_sum, Complex.re_sum, Complex.star_def, Complex.conj_ofReal, smul_mul_smul_comm,
    trace_smul, smul_eq_mul, X]
  refine Finset.sum_congr rfl fun μ _ => Finset.sum_congr rfl fun ν _ => ?_
  rw [← Complex.ofReal_mul, Complex.re_ofReal_mul]
  have := X_symm dΨ μ ν
  simp only [X] at this
  rw [this]; ring

/-- Prop. `prop:nec`: `T_{μν}k^μk^ν = ‖k^μ∂_μΨ‖²_HS` for `g_{μν}k^μk^ν = 0`. -/
theorem null_energy_identity (g gInv : Matrix (Fin n) (Fin n) ℝ) (trV : ℝ)
    (dΨ : Fin n → Matrix (Fin χ) (Fin χ) ℂ) (k : Fin n → ℝ)
    (hnull : ∑ μ, ∑ ν, g μ ν * k μ * k ν = 0) :
    ∑ μ, ∑ ν, T g gInv trV dΨ μ ν * k μ * k ν = hsSq (kDeriv k dΨ) := by
  rw [hsSq_eq_re_trace, ← kk_X]
  set S := (∑ α, ∑ β, gInv α β * X dΨ α β) + trV
  have h : ∑ μ, ∑ ν, T g gInv trV dΨ μ ν * k μ * k ν
      = ∑ μ, ∑ ν, X dΨ μ ν * k μ * k ν - 1 / 2 * S * ∑ μ, ∑ ν, g μ ν * k μ * k ν := by
    simp only [T, Finset.mul_sum, ← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl fun μ _ => Finset.sum_congr rfl fun ν _ => ?_
    ring
  rw [h, hnull]; ring

/-- The inequality part of Prop. `prop:nec`. -/
theorem null_energy_nonneg (g gInv : Matrix (Fin n) (Fin n) ℝ) (trV : ℝ)
    (dΨ : Fin n → Matrix (Fin χ) (Fin χ) ℂ) (k : Fin n → ℝ)
    (hnull : ∑ μ, ∑ ν, g μ ν * k μ * k ν = 0) :
    0 ≤ ∑ μ, ∑ ν, T g gInv trV dΨ μ ν * k μ * k ν := by
  rw [null_energy_identity g gInv trV dΨ k hnull]
  exact Finset.sum_nonneg fun i _ => Finset.sum_nonneg fun j _ => Complex.normSq_nonneg _

/-! ## Non-vacuity: Minkowski `η = diag(−1,1,1,1)`, `k = (1,1,0,0)`, `χ = 1`, `∂₀Ψ = 1`, other
`∂_μΨ = 0`, `Tr V = 7`. Then `k` is null, `k^μ∂_μΨ = 1`, and both sides equal `1 ≠ 0`. -/

noncomputable def eta : Matrix (Fin 4) (Fin 4) ℝ := Matrix.diagonal ![-1, 1, 1, 1]
def kW : Fin 4 → ℝ := ![1, 1, 0, 0]
noncomputable def dΨW : Fin 4 → Matrix (Fin 1) (Fin 1) ℂ := ![1, 0, 0, 0]

lemma witness_null : ∑ μ, ∑ ν, eta μ ν * kW μ * kW ν = 0 := by
  simp [eta, kW, Fin.sum_univ_four, Matrix.diagonal]

lemma witness_value : hsSq (kDeriv kW dΨW) = 1 := by
  simp [hsSq, kDeriv, kW, dΨW, Fin.sum_univ_four]

example : ∑ μ, ∑ ν, T eta eta 7 dΨW μ ν * kW μ * kW ν = 1 := by
  rw [null_energy_identity eta eta 7 dΨW kW witness_null, witness_value]

/-! ## Mutant: drop the null condition. False: `n = χ = 1`, `g = gInv = 1`, `k = 1`, `∂Ψ = 0`,
`Tr V = 1` gives `T₀₀ k k = −½` but `‖k∂Ψ‖² = 0`. -/
theorem nec_mutant_false :
    ¬ (∀ (g gInv : Matrix (Fin 1) (Fin 1) ℝ) (trV : ℝ)
        (dΨ : Fin 1 → Matrix (Fin 1) (Fin 1) ℂ) (k : Fin 1 → ℝ),
        ∑ μ, ∑ ν, T g gInv trV dΨ μ ν * k μ * k ν = hsSq (kDeriv k dΨ)) := by
  intro h
  have := h 1 1 1 0 1
  simp [T, X, hsSq, kDeriv] at this

end LeanReal.FunctorialBridge2

#print axioms LeanReal.FunctorialBridge2.null_energy_identity
#print axioms LeanReal.FunctorialBridge2.null_energy_nonneg
#print axioms LeanReal.FunctorialBridge2.nec_mutant_false
