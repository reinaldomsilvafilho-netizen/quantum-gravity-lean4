import LeanReal.Chap03Pascal
import LeanReal.Chap12Constraint
import LeanReal.Chap12ConstraintMatrix

/-!
# Non-vacuity witnesses

For each theorem with hypotheses, a `theorem …_nonvacuous` proves that concrete data satisfy
ALL of its hypotheses at once, so the theorem is not vacuously true. Theorems without
hypotheses cannot be vacuous; for them an `example` applies the theorem to concrete data.

The matrix witness is the non-diagonal symmetric matrix
`Kw = [[0,1,0],[1,0,0],[0,0,1]]` (eigenvalues `1, −1, 1`), with `κ = 1`, `‖Kw‖_{ℓ²→ℓ²} ≤ 1`,
`tr Kw = 1`, `K_ijK^ij = 3`, and the Hamiltonian constraint holds with `Λ = G = ρ = 1`,
`³R = 4 + 16π`. This `³R` is the upper endpoint `2Λ + 16πGρ + 2κ²` of item (ii).
-/

noncomputable section

namespace LeanReal.Witnesses

/-! ## Chapter 3 -/

section Chap03
open Complex LeanReal.Chap03

theorem one_ne_neg_nat (n : ℕ) : (1 : ℂ) ≠ -(n : ℂ) := by
  intro hn
  have h2 : (1 : ℝ) = -(n : ℝ) := by simpa using congrArg Complex.re hn
  have : (0 : ℝ) ≤ n := Nat.cast_nonneg n
  linarith

/-- `stifel`: its hypothesis `∀ n, x ≠ −n` holds at `x = 1`. -/
theorem stifel_nonvacuous : ∃ x : ℂ, ∀ n : ℕ, x ≠ -(n : ℂ) := ⟨1, one_ne_neg_nat⟩

example : cbinom (1 - 1) (1 / 2) + cbinom (1 - 1) (1 / 2 - 1) = cbinom 1 (1 / 2) :=
  stifel 1 (1 / 2) one_ne_neg_nat

/-- `cbinom_real_pos`: `x = 1`, `y = 1/2` satisfy `0 < x`, `0 ≤ y`, `y ≤ x`. -/
theorem cbinom_real_pos_nonvacuous : ∃ x y : ℝ, 0 < x ∧ 0 ≤ y ∧ y ≤ x :=
  ⟨1, 1 / 2, by norm_num, by norm_num, by norm_num⟩

example : 0 < Real.Gamma (1 + 1) * (Real.Gamma (1 / 2 + 1))⁻¹ * (Real.Gamma (1 - 1 / 2 + 1))⁻¹ :=
  cbinom_real_pos 1 (1 / 2) (by norm_num) (by norm_num) (by norm_num)

-- Theorems without hypotheses: instances at concrete data.
example : cbinom (3 - 1) (1 - 1) * cbinom 3 (1 + 1) * cbinom (3 + 1) 1 =
    cbinom (3 - 1) 1 * cbinom 3 (1 - 1) * cbinom (3 + 1) (1 + 1) := star_of_david 3 1
example : cbinom (1 / 2) (-((2 : ℕ) : ℂ) - 1) = 0 := cbinom_zero_of_y_neg (1 / 2) 2
example : cbinom (1 / 2) (1 / 2 + ((2 : ℕ) : ℂ) + 1) = 0 := cbinom_zero_of_xy_neg (1 / 2) 2
example : (Gamma (-((3 : ℕ) : ℂ)))⁻¹ = 0 := inv_Gamma_neg_nat 3
example : ∑ k ∈ Finset.range (4 + 1), Nat.choose 4 k = 2 ^ 4 := row_sum 4
example : ∑ k ∈ Finset.piAntidiag (Finset.range 3) 2, Nat.multinomial (Finset.range 3) k =
    3 ^ 2 := multinomial_row_sum 3 2

end Chap03

/-! ## Chapter 12, reduced form -/

section Chap12Reduced
open LeanReal.Chap12

/-- `constraint_bounds`: `k = (1/2, −1, 0)`, `κ = 1` satisfy `|kᵢ| ≤ κ`. -/
theorem constraint_bounds_nonvacuous :
    ∃ k₁ k₂ k₃ κ : ℝ, |k₁| ≤ κ ∧ |k₂| ≤ κ ∧ |k₃| ≤ κ :=
  ⟨1 / 2, -1, 0, 1, by norm_num [abs_of_pos], by norm_num, by norm_num⟩

example := constraint_bounds (1 / 2) (-1) 0 1 7 (by norm_num [abs_of_pos]) (by norm_num)
  (by norm_num)

example := constraint_bounds_sharp 1 7

end Chap12Reduced

/-! ## Chapter 12, matrix form -/

section Chap12Matrix
open Matrix LeanReal.Chap12

/-- The non-diagonal symmetric witness matrix. -/
def Kw : Matrix (Fin 3) (Fin 3) ℝ := !![0, 1, 0; 1, 0, 0; 0, 0, 1]

theorem Kw_isSymm : Kw.IsSymm := by
  unfold Matrix.IsSymm
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

theorem Kw_isHermitian : Kw.IsHermitian := isHermitian_iff_isSymm.mpr Kw_isSymm

theorem Kw_IIBound : IIBound Kw 1 := by
  intro v
  simp only [Kw, mulVec, dotProduct, Fin.sum_univ_three]
  simp
  rw [abs_le]
  constructor <;> nlinarith [sq_nonneg (v 0 - v 1), sq_nonneg (v 0 + v 1), sq_nonneg (v 2)]

theorem Kw_trace : Kw.trace = 1 := by
  simp [Kw, Matrix.trace, Fin.sum_univ_three]

theorem Kw_frobSq : frobSq Kw = 3 := by
  simp [frobSq, Kw, Fin.sum_univ_three]; norm_num

/-- `Kw` satisfies the Hamiltonian constraint with `Λ = G = ρ = 1`, `³R = 4 + 16π`. -/
theorem Kw_hamiltonian : HamiltonianConstraint Kw (4 + 16 * Real.pi) 1 1 1 := by
  rw [hamiltonian_iff, Kw_trace, Kw_frobSq]; ring

open scoped Matrix.Norms.L2Operator in
/-- The Mathlib `ℓ²` operator norm of `Kw` is at most 1. -/
theorem Kw_opNorm_le : ‖Kw‖ ≤ 1 := by
  rw [← l2_opNorm_toEuclideanCLM]
  refine ContinuousLinearMap.opNorm_le_bound _ zero_le_one fun x => ?_
  refine (sq_le_sq₀ (norm_nonneg _) (by positivity)).mp ?_
  rw [EuclideanSpace.norm_sq_eq, one_mul, EuclideanSpace.norm_sq_eq]
  simp [Kw, mulVec, dotProduct, Fin.sum_univ_three]
  nlinarith [sq_nonneg (x 0), sq_nonneg (x 1), sq_nonneg (x 2)]

/-- `constraint_bounds_matrix`: all hypotheses (`K` symmetric, `IIBound K κ`, Hamiltonian
constraint) hold at once for `Kw`, `κ = 1`, `R = 4 + 16π`, `Λ = G = ρ = 1`. -/
theorem constraint_bounds_matrix_nonvacuous :
    ∃ (K : Matrix (Fin 3) (Fin 3) ℝ) (κ R Λ G ρ : ℝ),
      K.IsSymm ∧ IIBound K κ ∧ HamiltonianConstraint K R Λ G ρ :=
  ⟨Kw, 1, 4 + 16 * Real.pi, 1, 1, 1, Kw_isSymm, Kw_IIBound, Kw_hamiltonian⟩

open scoped Matrix.Norms.L2Operator in
/-- `constraint_bounds_opNorm`: all hypotheses (`K` symmetric, `‖K‖ ≤ κ` in the `ℓ²` operator
norm, Hamiltonian constraint) hold at once for the same data. -/
theorem constraint_bounds_opNorm_nonvacuous :
    ∃ (K : Matrix (Fin 3) (Fin 3) ℝ) (κ R Λ G ρ : ℝ),
      K.IsSymm ∧ ‖K‖ ≤ κ ∧ HamiltonianConstraint K R Λ G ρ :=
  ⟨Kw, 1, 4 + 16 * Real.pi, 1, 1, 1, Kw_isSymm, Kw_opNorm_le, Kw_hamiltonian⟩

/-- `constraint_bounds_vacuum`: `Kw`, `κ = 1`, `Λ = 1`, `³R = 4`. -/
theorem constraint_bounds_vacuum_nonvacuous :
    ∃ (K : Matrix (Fin 3) (Fin 3) ℝ) (κ R Λ : ℝ),
      K.IsSymm ∧ IIBound K κ ∧ R + K.trace ^ 2 - frobSq K = 2 * Λ :=
  ⟨Kw, 1, 4, 1, Kw_isSymm, Kw_IIBound, by rw [Kw_trace, Kw_frobSq]; norm_num⟩

/-- `abs_eigenvalue_le`, `IIBound_iff`, `frobSq_eq_trace_mul`, `trace_mul_self_eq`,
`trace_eq_sum`: `Kw` is Hermitian and satisfies `IIBound Kw 1`. -/
theorem abs_eigenvalue_le_nonvacuous :
    ∃ (K : Matrix (Fin 3) (Fin 3) ℝ) (κ : ℝ), K.IsHermitian ∧ IIBound K κ :=
  ⟨Kw, 1, Kw_isHermitian, Kw_IIBound⟩

/-- `IIBound_of_abs_eigenvalue_le`: the eigenvalues of `Kw` satisfy `|λᵢ| ≤ 1`. -/
theorem IIBound_of_abs_eigenvalue_le_nonvacuous :
    ∃ (K : Matrix (Fin 3) (Fin 3) ℝ) (hK : K.IsHermitian) (κ : ℝ), ∀ i, |hK.eigenvalues i| ≤ κ :=
  ⟨Kw, Kw_isHermitian, 1, abs_eigenvalue_le Kw_isHermitian Kw_IIBound⟩

open scoped Matrix.Norms.L2Operator in
/-- `IIBound_of_l2_opNorm_le`: `‖Kw‖ ≤ 1`. -/
theorem IIBound_of_l2_opNorm_le_nonvacuous :
    ∃ (K : Matrix (Fin 3) (Fin 3) ℝ) (κ : ℝ), ‖K‖ ≤ κ :=
  ⟨Kw, 1, Kw_opNorm_le⟩

/-- `IIBound_diagonal`: `d = (1, −1, 1/2)`, `κ = 1`. -/
theorem IIBound_diagonal_nonvacuous : ∃ (d : Fin 3 → ℝ) (κ : ℝ), ∀ i, |d i| ≤ κ := by
  refine ⟨![1, -1, 1 / 2], 1, fun i => ?_⟩
  fin_cases i <;> norm_num [abs_of_pos]

/-- `constraint_bounds_matrix_sharp`: `κ = 1` satisfies `0 ≤ κ`. -/
theorem constraint_bounds_matrix_sharp_nonvacuous : ∃ κ : ℝ, 0 ≤ κ := ⟨1, zero_le_one⟩

-- The main theorem applied to the witness: `³R = 4 + 16π` meets the upper endpoint.
example := constraint_bounds_matrix Kw Kw_isSymm 1 _ 1 1 1 Kw_IIBound Kw_hamiltonian
example := constraint_bounds_opNorm Kw Kw_isSymm 1 _ 1 1 1 Kw_opNorm_le Kw_hamiltonian
example : 4 + 16 * Real.pi = 2 * 1 + 16 * Real.pi * 1 * 1 + 2 * 1 ^ 2 := by ring

end Chap12Matrix

end LeanReal.Witnesses

#print axioms LeanReal.Witnesses.stifel_nonvacuous
#print axioms LeanReal.Witnesses.cbinom_real_pos_nonvacuous
#print axioms LeanReal.Witnesses.constraint_bounds_nonvacuous
#print axioms LeanReal.Witnesses.Kw_isSymm
#print axioms LeanReal.Witnesses.Kw_IIBound
#print axioms LeanReal.Witnesses.Kw_hamiltonian
#print axioms LeanReal.Witnesses.Kw_opNorm_le
#print axioms LeanReal.Witnesses.constraint_bounds_matrix_nonvacuous
#print axioms LeanReal.Witnesses.constraint_bounds_opNorm_nonvacuous
#print axioms LeanReal.Witnesses.constraint_bounds_vacuum_nonvacuous
#print axioms LeanReal.Witnesses.abs_eigenvalue_le_nonvacuous
#print axioms LeanReal.Witnesses.IIBound_of_abs_eigenvalue_le_nonvacuous
#print axioms LeanReal.Witnesses.IIBound_of_l2_opNorm_le_nonvacuous
#print axioms LeanReal.Witnesses.IIBound_diagonal_nonvacuous
#print axioms LeanReal.Witnesses.constraint_bounds_matrix_sharp_nonvacuous
#print axioms LeanReal.Witnesses.one_ne_neg_nat
#print axioms LeanReal.Witnesses.Kw_isHermitian
#print axioms LeanReal.Witnesses.Kw_trace
#print axioms LeanReal.Witnesses.Kw_frobSq
