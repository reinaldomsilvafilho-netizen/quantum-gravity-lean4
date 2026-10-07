import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# Capitulo 12, Teorema "Pointwise Constraint Bounds" (thm:minimax_hamiltonian_regularization)

FORMA REDUZIDA (enfraquecimento declarado). O texto parte de um espaco-tempo e de uma
hipersuperficie; aqui formaliza-se apenas o nucleo algebrico pontual, depois de dois passos
que NAO estao formalizados:
  (a) diagonalizar `K_ij` num referencial ortonormal de `γ` em `x`, com curvaturas principais
      `k₁ k₂ k₃`, de modo que `‖II‖_{L∞} ≤ κ` da `|kᵢ| ≤ κ`, `K_ij K^ij = Σ kᵢ²`, `K = Σ kᵢ`;
  (b) o vinculo hamiltoniano `³R + K² − K_ij K^ij = 16πGρ + 2Λ`, que da
      `³R = 2Λ + 16πGρ + Σ kᵢ² − (Σ kᵢ)²`.
O teorema abaixo prova (i), (ii) e a otimalidade ("both endpoints attained") nessa forma.
-/

namespace LeanReal.Chap12

/-- Itens (i) e (ii), forma reduzida. `s` abrevia `2Λ + 16πGρ`. -/
theorem constraint_bounds (k₁ k₂ k₃ κ s : ℝ)
    (h₁ : |k₁| ≤ κ) (h₂ : |k₂| ≤ κ) (h₃ : |k₃| ≤ κ) :
    0 ≤ k₁ ^ 2 + k₂ ^ 2 + k₃ ^ 2 ∧
    k₁ ^ 2 + k₂ ^ 2 + k₃ ^ 2 ≤ 3 * κ ^ 2 ∧
    s - 6 * κ ^ 2 ≤ s + (k₁ ^ 2 + k₂ ^ 2 + k₃ ^ 2) - (k₁ + k₂ + k₃) ^ 2 ∧
    s + (k₁ ^ 2 + k₂ ^ 2 + k₃ ^ 2) - (k₁ + k₂ + k₃) ^ 2 ≤ s + 2 * κ ^ 2 := by
  obtain ⟨a₁, b₁⟩ := abs_le.mp h₁
  obtain ⟨a₂, b₂⟩ := abs_le.mp h₂
  obtain ⟨a₃, b₃⟩ := abs_le.mp h₃
  have hκ : 0 ≤ κ := le_trans (abs_nonneg _) h₁
  have p₁ : 0 ≤ (κ - k₁) * (κ - k₂) := mul_nonneg (by linarith) (by linarith)
  have p₂ : 0 ≤ (κ + k₁) * (κ + k₂) := mul_nonneg (by linarith) (by linarith)
  have q₁ : 0 ≤ (κ - k₁) * (κ - k₂) * (κ - k₃) := mul_nonneg p₁ (by linarith)
  have q₂ : 0 ≤ (κ + k₁) * (κ + k₂) * (κ + k₃) := mul_nonneg p₂ (by linarith)
  refine ⟨by positivity, ?_, ?_, ?_⟩
  · nlinarith [sq_le_sq' a₁ b₁, sq_le_sq' a₂ b₂, sq_le_sq' a₃ b₃]
  · nlinarith [mul_nonneg (show 0 ≤ κ - k₁ by linarith) (show 0 ≤ κ + k₂ by linarith),
               mul_nonneg (show 0 ≤ κ + k₁ by linarith) (show 0 ≤ κ - k₂ by linarith),
               mul_nonneg (show 0 ≤ κ - k₁ by linarith) (show 0 ≤ κ + k₃ by linarith),
               mul_nonneg (show 0 ≤ κ + k₁ by linarith) (show 0 ≤ κ - k₃ by linarith),
               mul_nonneg (show 0 ≤ κ - k₂ by linarith) (show 0 ≤ κ + k₃ by linarith),
               mul_nonneg (show 0 ≤ κ + k₂ by linarith) (show 0 ≤ κ - k₃ by linarith)]
  · -- k₁k₂ + k₁k₃ + k₂k₃ ≥ -κ²: somar q₁ e q₂ da 2κ³ + 2κ(k₁k₂+k₁k₃+k₂k₃) ≥ 0
    rcases hκ.lt_or_eq with hpos | hzero
    · nlinarith [q₁, q₂]
    · subst hzero
      have : k₁ = 0 := by linarith
      have : k₂ = 0 := by linarith
      have : k₃ = 0 := by linarith
      subst_vars; norm_num

/-- Otimalidade de (i) e dos dois extremos de (ii): atingidos por `(κ,κ,κ)` e `(κ,κ,−κ)`. -/
theorem constraint_bounds_sharp (κ s : ℝ) :
    κ ^ 2 + κ ^ 2 + κ ^ 2 = 3 * κ ^ 2 ∧
    s + (κ ^ 2 + κ ^ 2 + κ ^ 2) - (κ + κ + κ) ^ 2 = s - 6 * κ ^ 2 ∧
    s + (κ ^ 2 + κ ^ 2 + (-κ) ^ 2) - (κ + κ + -κ) ^ 2 = s + 2 * κ ^ 2 := by
  refine ⟨by ring, by ring, by ring⟩

end LeanReal.Chap12

#print axioms LeanReal.Chap12.constraint_bounds
#print axioms LeanReal.Chap12.constraint_bounds_sharp
