import LeanReal.Chap03Pascal
import LeanReal.Chap12Constraint
import LeanReal.Chap12ConstraintMatrix

/-!
# Mutants proved false

Each mutant in `mutants/` restates a verified theorem with one change. A mutant that fails to
compile does not show that its statement is false. Here each mutated statement `P` is stated
verbatim and `¬ P` is proved, by an explicit counterexample with concrete numbers.

| mutant | counterexample |
|---|---|
| M1 `KK ≤ 2κ²` | `K = diag(1,1,1)`, `κ = 1`, `Λ = G = ρ = 0`, `R = −6`: `KK = 3` |
| M2 `σσ ≤ 3κ² − K²/2` | same data: `σσ = 0`, `3 − 9/2 < 0` |
| M3 `³R ≥ s − 5κ²` | same data: `R = −6 < −5` |
| M4 `³R ≤ s + κ²` | `K = diag(1,1,−1)`, `κ = 1`, `Λ = G = ρ = 0`, `R = 2 > 1` |
| M5 `|λᵢ| ≤ κ/2` | `K = diag(1,1,1)`, `κ = 1`: `∑ λᵢ = tr K = 3 > 3/2` |
| M6 `σσ = KK − K²/2` | `K = diag(1,1,1)`: `0 ≠ 3 − 9/2` |
| M7 `tr(K²) = ∑ λᵢ` | `K = diag(2,2,2)`: `tr(K²) = 12 ≠ 6 = tr K` |
| M8 `diag(κ,κ,κ)` with `³R = s − 5κ²` | `κ = 1`, `Λ = G = ρ = 0`: constraint gives `−5 + 9 − 3 = 1 ≠ 0` |
| M9 Stifel with `−` | `x = y = 1`: `C(0,1) − C(0,0) = −1 ≠ 1 = C(1,1)` |
| M10 Star of David, `k+2` on the left | `n = 2`, `k = 1`: left `C(1,0)·C(2,3)·C(3,1) = 0`, right `C(1,1)·C(2,0)·C(3,2) = 3` |
| M11 positivity with `y ≤ x + 3` | `x = 1`, `y = 5/2`: `Γ(−1/2) < 0` |
| M12 `∑ multinomial = mⁿ + 1` | `m = 1`, `n = 0`: the true sum is `1⁰ = 1 ≠ 2` |
| M13 reduced upper bound `s + κ²` | `k = (1,1,−1)`, `κ = 1`, `s = 0`: `3 − 1 = 2 > 1` |
| M14 reduced `∑ kᵢ² ≤ 2κ²` | `k = (1,1,1)`, `κ = 1`: `3 > 2` |
-/

noncomputable section

namespace LeanReal.Falsified

open Matrix LeanReal.Chap12

/-- `tr diag(1,1,1) = 3`. -/
theorem trace_diag111 : (diagonal ![(1 : ℝ), 1, 1]).trace = 3 := by
  simp [Matrix.trace, Fin.sum_univ_three]; norm_num

/-- M1 is false. -/
theorem m1_false : ¬ (∀ (K : Matrix (Fin 3) (Fin 3) ℝ), K.IsSymm → ∀ (κ R Λ G ρ : ℝ),
    IIBound K κ → HamiltonianConstraint K R Λ G ρ →
    0 ≤ frobSq K ∧ frobSq K ≤ 2 * κ ^ 2 ∧
    0 ≤ frobSq (shear K) ∧ frobSq (shear K) ≤ 3 * κ ^ 2 - K.trace ^ 2 / 3 ∧
    2 * Λ + 16 * Real.pi * G * ρ - 6 * κ ^ 2 ≤ R ∧
    R ≤ 2 * Λ + 16 * Real.pi * G * ρ + 2 * κ ^ 2) := by
  intro h
  obtain ⟨hS, hb, hF, -, hH, -⟩ := constraint_bounds_matrix_sharp 1 0 0 0 zero_le_one
  obtain ⟨-, h2, -⟩ := h _ hS 1 _ 0 0 0 hb hH
  norm_num at hF h2; linarith

/-- M2 is false. -/
theorem m2_false : ¬ (∀ (K : Matrix (Fin 3) (Fin 3) ℝ), K.IsSymm → ∀ (κ R Λ G ρ : ℝ),
    IIBound K κ → HamiltonianConstraint K R Λ G ρ →
    0 ≤ frobSq K ∧ frobSq K ≤ 3 * κ ^ 2 ∧
    0 ≤ frobSq (shear K) ∧ frobSq (shear K) ≤ 3 * κ ^ 2 - K.trace ^ 2 / 2 ∧
    2 * Λ + 16 * Real.pi * G * ρ - 6 * κ ^ 2 ≤ R ∧
    R ≤ 2 * Λ + 16 * Real.pi * G * ρ + 2 * κ ^ 2) := by
  intro h
  obtain ⟨hS, hb, -, hσ, hH, -⟩ := constraint_bounds_matrix_sharp 1 0 0 0 zero_le_one
  obtain ⟨-, -, -, h4, -⟩ := h _ hS 1 _ 0 0 0 hb hH
  rw [trace_diag111] at hσ h4
  norm_num at hσ h4; linarith

/-- M3 is false. -/
theorem m3_false : ¬ (∀ (K : Matrix (Fin 3) (Fin 3) ℝ), K.IsSymm → ∀ (κ R Λ G ρ : ℝ),
    IIBound K κ → HamiltonianConstraint K R Λ G ρ →
    0 ≤ frobSq K ∧ frobSq K ≤ 3 * κ ^ 2 ∧
    0 ≤ frobSq (shear K) ∧ frobSq (shear K) ≤ 3 * κ ^ 2 - K.trace ^ 2 / 3 ∧
    2 * Λ + 16 * Real.pi * G * ρ - 5 * κ ^ 2 ≤ R ∧
    R ≤ 2 * Λ + 16 * Real.pi * G * ρ + 2 * κ ^ 2) := by
  intro h
  obtain ⟨hS, hb, -, -, hH, -⟩ := constraint_bounds_matrix_sharp 1 0 0 0 zero_le_one
  obtain ⟨-, -, -, -, h5, -⟩ := h _ hS 1 _ 0 0 0 hb hH
  norm_num at h5

/-- M4 is false. -/
theorem m4_false : ¬ (∀ (K : Matrix (Fin 3) (Fin 3) ℝ), K.IsSymm → ∀ (κ R Λ G ρ : ℝ),
    IIBound K κ → HamiltonianConstraint K R Λ G ρ →
    0 ≤ frobSq K ∧ frobSq K ≤ 3 * κ ^ 2 ∧
    0 ≤ frobSq (shear K) ∧ frobSq (shear K) ≤ 3 * κ ^ 2 - K.trace ^ 2 / 3 ∧
    2 * Λ + 16 * Real.pi * G * ρ - 6 * κ ^ 2 ≤ R ∧
    R ≤ 2 * Λ + 16 * Real.pi * G * ρ + 1 * κ ^ 2) := by
  intro h
  obtain ⟨-, -, -, -, -, hS, hb, -, -, hH⟩ := constraint_bounds_matrix_sharp 1 0 0 0 zero_le_one
  obtain ⟨-, -, -, -, -, h6⟩ := h _ hS 1 _ 0 0 0 hb hH
  norm_num at h6

/-- M5 is false. -/
theorem m5_false : ¬ (∀ (K : Matrix (Fin 3) (Fin 3) ℝ) (hK : K.IsHermitian) (κ : ℝ),
    IIBound K κ → ∀ i : Fin 3, |hK.eigenvalues i| ≤ κ / 2) := by
  intro h
  obtain ⟨hS, hb, -⟩ := constraint_bounds_matrix_sharp 1 0 0 0 zero_le_one
  have hH : (diagonal ![(1 : ℝ), 1, 1]).IsHermitian := isHermitian_iff_isSymm.mpr hS
  have hT := trace_eq_sum hH
  rw [Fin.sum_univ_three, trace_diag111] at hT
  have e0 := (abs_le.mp (h _ hH 1 hb 0)).2
  have e1 := (abs_le.mp (h _ hH 1 hb 1)).2
  have e2 := (abs_le.mp (h _ hH 1 hb 2)).2
  linarith

/-- M6 is false. -/
theorem m6_false : ¬ (∀ K : Matrix (Fin 3) (Fin 3) ℝ,
    frobSq (shear K) = frobSq K - K.trace ^ 2 / 2) := by
  intro h
  have h1 := h (diagonal ![(1 : ℝ), 1, 1])
  rw [frobSq_shear, trace_diag111] at h1
  norm_num at h1

/-- M7 is false. -/
theorem m7_false : ¬ (∀ (K : Matrix (Fin 3) (Fin 3) ℝ) (hK : K.IsHermitian),
    (K * K).trace = ∑ i, hK.eigenvalues i) := by
  intro h
  have hH : (diagonal ![(2 : ℝ), 2, 2]).IsHermitian :=
    isHermitian_iff_isSymm.mpr (isSymm_diagonal _)
  have h1 := h _ hH
  rw [← trace_eq_sum hH, diagonal_mul_diagonal] at h1
  simp [Matrix.trace, Fin.sum_univ_three] at h1
  norm_num at h1

/-- M8 is false. -/
theorem m8_false : ¬ (∀ κ Λ G ρ : ℝ, 0 ≤ κ →
    HamiltonianConstraint (diagonal ![κ, κ, κ])
      (2 * Λ + 16 * Real.pi * G * ρ - 5 * κ ^ 2) Λ G ρ) := by
  intro h
  obtain ⟨-, -, hF, -⟩ := constraint_bounds_matrix_sharp 1 0 0 0 zero_le_one
  have h1 := h 1 0 0 0 zero_le_one
  rw [hamiltonian_iff, hF, trace_diag111] at h1
  norm_num at h1

open Complex LeanReal.Chap03

theorem cGamma_two : Gamma 2 = 1 := by
  rw [show (2 : ℂ) = ((1 : ℕ) : ℂ) + 1 by norm_num, Complex.Gamma_nat_eq_factorial]
  norm_num [Nat.factorial]

theorem cGamma_three : Gamma 3 = 2 := by
  rw [show (3 : ℂ) = ((2 : ℕ) : ℂ) + 1 by norm_num, Complex.Gamma_nat_eq_factorial]
  norm_num [Nat.factorial]

theorem cGamma_four : Gamma 4 = 6 := by
  rw [show (4 : ℂ) = ((3 : ℕ) : ℂ) + 1 by norm_num, Complex.Gamma_nat_eq_factorial]
  norm_num [Nat.factorial]

/-- `x = 1` lies in the domain of `stifel`. -/
theorem one_ne_neg_nat (n : ℕ) : (1 : ℂ) ≠ -(n : ℂ) := by
  intro hn
  have h2 : (1 : ℝ) = -(n : ℝ) := by simpa using congrArg Complex.re hn
  have : (0 : ℝ) ≤ n := Nat.cast_nonneg n
  linarith

/-- M9 is false. -/
theorem m9_false : ¬ (∀ x y : ℂ, (∀ n : ℕ, x ≠ -(n : ℂ)) →
    cbinom (x - 1) y - cbinom (x - 1) (y - 1) = cbinom x y) := by
  intro h
  have h1 := h 1 1 one_ne_neg_nat
  simp only [cbinom] at h1
  norm_num [Complex.Gamma_one, Complex.Gamma_zero, cGamma_two] at h1

/-- M10 is false. -/
theorem m10_false : ¬ (∀ n k : ℂ,
    cbinom (n - 1) (k - 1) * cbinom n (k + 2) * cbinom (n + 1) k =
      cbinom (n - 1) k * cbinom n (k - 1) * cbinom (n + 1) (k + 1)) := by
  intro h
  have h1 := h 2 1
  simp only [cbinom] at h1
  norm_num [Complex.Gamma_one, Complex.Gamma_zero, cGamma_two, cGamma_three, cGamma_four] at h1

/-- M11 is false. -/
theorem m11_false : ¬ (∀ x y : ℝ, 0 < x → 0 ≤ y → y ≤ x + 3 →
    0 < Real.Gamma (x + 1) * (Real.Gamma (y + 1))⁻¹ * (Real.Gamma (x - y + 1))⁻¹) := by
  intro h
  have h1 := h 1 (5 / 2) (by norm_num) (by norm_num) (by norm_num)
  have e : (1 : ℝ) - 5 / 2 + 1 = -1 / 2 := by norm_num
  rw [e] at h1
  have hrec := Real.Gamma_add_one (s := (-1 / 2 : ℝ)) (by norm_num)
  rw [show (-1 / 2 : ℝ) + 1 = 1 / 2 by norm_num] at hrec
  have hp : 0 < Real.Gamma (1 / 2) := Real.Gamma_pos_of_pos (by norm_num)
  have hneg : Real.Gamma (-1 / 2) < 0 := by nlinarith
  have a := Real.Gamma_pos_of_pos (show (0 : ℝ) < 1 + 1 by norm_num)
  have b := Real.Gamma_pos_of_pos (show (0 : ℝ) < 5 / 2 + 1 by norm_num)
  have c := mul_neg_of_pos_of_neg (mul_pos a (inv_pos.mpr b)) (inv_lt_zero.mpr hneg)
  linarith

/-- M12 is false (for every `m, n`; the instance `m = 1`, `n = 0` is used). -/
theorem m12_false : ¬ (∀ m n : ℕ,
    ∑ k ∈ Finset.piAntidiag (Finset.range m) n, Nat.multinomial (Finset.range m) k =
      m ^ n + 1) := by
  intro h
  have h1 := h 1 0
  rw [multinomial_row_sum] at h1
  omega

/-- M13 is false. -/
theorem m13_false : ¬ (∀ k₁ k₂ k₃ κ s : ℝ, |k₁| ≤ κ → |k₂| ≤ κ → |k₃| ≤ κ →
    s + (k₁ ^ 2 + k₂ ^ 2 + k₃ ^ 2) - (k₁ + k₂ + k₃) ^ 2 ≤ s + κ ^ 2) := by
  intro h
  have h1 := h 1 1 (-1) 1 0 (by norm_num) (by norm_num) (by norm_num)
  norm_num at h1

/-- M14 is false. -/
theorem m14_false : ¬ (∀ k₁ k₂ k₃ κ : ℝ, |k₁| ≤ κ → |k₂| ≤ κ → |k₃| ≤ κ →
    k₁ ^ 2 + k₂ ^ 2 + k₃ ^ 2 ≤ 2 * κ ^ 2) := by
  intro h
  have h1 := h 1 1 1 1 (by norm_num) (by norm_num) (by norm_num)
  norm_num at h1

end LeanReal.Falsified

#print axioms LeanReal.Falsified.m1_false
#print axioms LeanReal.Falsified.m2_false
#print axioms LeanReal.Falsified.m3_false
#print axioms LeanReal.Falsified.m4_false
#print axioms LeanReal.Falsified.m5_false
#print axioms LeanReal.Falsified.m6_false
#print axioms LeanReal.Falsified.m7_false
#print axioms LeanReal.Falsified.m8_false
#print axioms LeanReal.Falsified.m9_false
#print axioms LeanReal.Falsified.m10_false
#print axioms LeanReal.Falsified.m11_false
#print axioms LeanReal.Falsified.m12_false
#print axioms LeanReal.Falsified.m13_false
#print axioms LeanReal.Falsified.m14_false
#print axioms LeanReal.Falsified.trace_diag111
#print axioms LeanReal.Falsified.cGamma_two
#print axioms LeanReal.Falsified.cGamma_three
#print axioms LeanReal.Falsified.cGamma_four
#print axioms LeanReal.Falsified.one_ne_neg_nat
