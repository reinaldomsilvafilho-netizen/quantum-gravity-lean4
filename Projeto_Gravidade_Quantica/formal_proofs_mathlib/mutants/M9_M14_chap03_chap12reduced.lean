import LeanReal.Chap03Pascal
import LeanReal.Chap12Constraint

/-!
Negative controls for `Chap03Pascal` and `Chap12Constraint` (reduced form).
Each theorem restates one verified result with ONE change and reuses the original
proof. Every mutated statement is mathematically false (counterexample in the
comment), so each must fail to compile and `#print axioms` must show `sorryAx`.
-/

noncomputable section

namespace LeanReal.Mutant

open Complex LeanReal.Chap03

-- M9: Stifel with `+` replaced by `-`. Counterexample: x = 2, y = 1 gives 1 - 1 = 0 ≠ 2.
theorem m9 (x y : ℂ) (hx : ∀ n : ℕ, x ≠ -(n : ℂ)) :
    cbinom (x - 1) y - cbinom (x - 1) (y - 1) = cbinom x y := by
  have hx0 : x ≠ 0 := by simpa using hx 0
  have hy : (Gamma y)⁻¹ = y * (Gamma (y + 1))⁻¹ := by
    simpa [one_div] using one_div_Gamma_eq_self_mul_one_div_Gamma_add_one y
  have hxy : (Gamma (x - y))⁻¹ = (x - y) * (Gamma (x - y + 1))⁻¹ := by
    simpa [one_div] using one_div_Gamma_eq_self_mul_one_div_Gamma_add_one (x - y)
  have hG : Gamma (x + 1) = x * Gamma x := Gamma_add_one x hx0
  unfold cbinom
  have e1 : x - 1 + 1 = x := by ring
  have e2 : x - 1 - y + 1 = x - y := by ring
  have e3 : y - 1 + 1 = y := by ring
  have e4 : x - 1 - (y - 1) + 1 = x - y + 1 := by ring
  rw [e1, e2, e3, e4, hy, hxy, hG]
  ring

-- M10: Star of David with `k + 1` replaced by `k + 2` on the left only.
-- Counterexample: n = 3, k = 1: altered left C(2,0)·C(3,3)·C(4,1) = 4, right C(2,1)·C(3,0)·C(4,2) = 12.
theorem m10 (n k : ℂ) :
    cbinom (n - 1) (k - 1) * cbinom n (k + 2) * cbinom (n + 1) k =
      cbinom (n - 1) k * cbinom n (k - 1) * cbinom (n + 1) (k + 1) := by
  unfold cbinom
  have a1 : n - 1 + 1 = n := by ring
  have a2 : k - 1 + 1 = k := by ring
  have a3 : n - 1 - (k - 1) + 1 = n - k + 1 := by ring
  have a4 : n - (k + 1) + 1 = n - k := by ring
  have a5 : n + 1 - k + 1 = n - k + 2 := by ring
  have a6 : n - 1 - k + 1 = n - k := by ring
  have a7 : n - (k - 1) + 1 = n - k + 2 := by ring
  have a8 : n + 1 - (k + 1) + 1 = n - k + 1 := by ring
  rw [a1, a2, a3, a4, a5, a6, a7, a8]
  ring

-- M11: positivity with `y ≤ x` relaxed to `y ≤ x + 3`.
-- Counterexample: x = 1, y = 5/2: Γ(x - y + 1) = Γ(-1/2) < 0, so the product is negative.
theorem m11 (x y : ℝ) (hx : 0 < x) (hy0 : 0 ≤ y) (hyx : y ≤ x + 3) :
    0 < Real.Gamma (x + 1) * (Real.Gamma (y + 1))⁻¹ * (Real.Gamma (x - y + 1))⁻¹ := by
  have h1 := Real.Gamma_pos_of_pos (show 0 < x + 1 by linarith)
  have h2 := Real.Gamma_pos_of_pos (show 0 < y + 1 by linarith)
  have h3 := Real.Gamma_pos_of_pos (show 0 < x - y + 1 by linarith)
  positivity

-- M12: multinomial row sum off by one. Counterexample: m = 1, n = 0 gives 1 ≠ 2.
theorem m12 (m n : ℕ) :
    ∑ k ∈ Finset.piAntidiag (Finset.range m) n, Nat.multinomial (Finset.range m) k = m ^ n + 1 := by
  have h := Finset.sum_pow_eq_sum_piAntidiag (Finset.range m) (fun _ => (1 : ℕ)) n
  simpa using h.symm

-- M13: reduced constraint bound with upper endpoint `2κ²` replaced by `κ²`.
-- Counterexample: (k₁, k₂, k₃) = (1, 1, -1), κ = 1: s + 3 - 1 = s + 2 > s + 1.
theorem m13 (k₁ k₂ k₃ κ s : ℝ)
    (h₁ : |k₁| ≤ κ) (h₂ : |k₂| ≤ κ) (h₃ : |k₃| ≤ κ) :
    s + (k₁ ^ 2 + k₂ ^ 2 + k₃ ^ 2) - (k₁ + k₂ + k₃) ^ 2 ≤ s + κ ^ 2 := by
  obtain ⟨a₁, b₁⟩ := abs_le.mp h₁
  obtain ⟨a₂, b₂⟩ := abs_le.mp h₂
  obtain ⟨a₃, b₃⟩ := abs_le.mp h₃
  have hκ : 0 ≤ κ := le_trans (abs_nonneg _) h₁
  have p₁ : 0 ≤ (κ - k₁) * (κ - k₂) := mul_nonneg (by linarith) (by linarith)
  have p₂ : 0 ≤ (κ + k₁) * (κ + k₂) := mul_nonneg (by linarith) (by linarith)
  have q₁ : 0 ≤ (κ - k₁) * (κ - k₂) * (κ - k₃) := mul_nonneg p₁ (by linarith)
  have q₂ : 0 ≤ (κ + k₁) * (κ + k₂) * (κ + k₃) := mul_nonneg p₂ (by linarith)
  rcases hκ.lt_or_eq with hpos | hzero
  · nlinarith [q₁, q₂]
  · subst hzero
    have : k₁ = 0 := by linarith
    have : k₂ = 0 := by linarith
    have : k₃ = 0 := by linarith
    subst_vars; norm_num

-- M14: reduced bound `Σ kᵢ² ≤ 3κ²` replaced by `≤ 2κ²`. Counterexample: k = (1, 1, 1), κ = 1.
theorem m14 (k₁ k₂ k₃ κ : ℝ)
    (h₁ : |k₁| ≤ κ) (h₂ : |k₂| ≤ κ) (h₃ : |k₃| ≤ κ) :
    k₁ ^ 2 + k₂ ^ 2 + k₃ ^ 2 ≤ 2 * κ ^ 2 := by
  obtain ⟨a₁, b₁⟩ := abs_le.mp h₁
  obtain ⟨a₂, b₂⟩ := abs_le.mp h₂
  obtain ⟨a₃, b₃⟩ := abs_le.mp h₃
  nlinarith [sq_le_sq' a₁ b₁, sq_le_sq' a₂ b₂, sq_le_sq' a₃ b₃]

end LeanReal.Mutant

#print axioms LeanReal.Mutant.m9
#print axioms LeanReal.Mutant.m10
#print axioms LeanReal.Mutant.m11
#print axioms LeanReal.Mutant.m12
#print axioms LeanReal.Mutant.m13
#print axioms LeanReal.Mutant.m14
