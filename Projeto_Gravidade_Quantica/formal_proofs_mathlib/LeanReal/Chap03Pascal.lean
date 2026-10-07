import Mathlib.Analysis.SpecialFunctions.Gamma.Beta
import Mathlib.Data.Nat.Choose.Sum
import Mathlib.Data.Nat.Choose.Multinomial

/-!
# Capitulo 3 (Pascal continuo): piloto de formalizacao real em Mathlib

Fonte: `unified_quantum_gravity_book/chap03_pascal_simplex_continuous_multinomials.tex`.

Convencao: o texto define `binom x y = Γ(x+1) · (1/Γ)(y+1) · (1/Γ)(x-y+1)`, com `1/Γ`
a funcao reciproca inteira. Em Mathlib, `Complex.Gamma (-n) = 0` para `n : ℕ`
(`Complex.Gamma_neg_nat_eq_zero`) e `0⁻¹ = 0`, logo `(Complex.Gamma s)⁻¹` coincide com
a reciproca inteira em todo `s : ℂ` (nos polos ambas valem 0). O lema `inv_Gamma_neg_nat`
abaixo registra isso. Assim a definicao `cbinom` e literalmente a do texto no dominio
`x ∉ {-1,-2,...}`.
-/

noncomputable section

namespace LeanReal.Chap03

open Complex

/-- Coeficiente binomial continuo (Definicao "Continuous Binomial Coefficient"). -/
def cbinom (x y : ℂ) : ℂ :=
  Gamma (x + 1) * (Gamma (y + 1))⁻¹ * (Gamma (x - y + 1))⁻¹

/-- `(Γ)⁻¹` de Mathlib vale 0 nos polos, como a reciproca inteira `1/Γ`. -/
theorem inv_Gamma_neg_nat (n : ℕ) : (Gamma (-(n : ℂ)))⁻¹ = 0 := by
  rw [Gamma_neg_nat_eq_zero, inv_zero]

/-- Proposicao "Global Stifel Recurrence" (cap. 3), para todo `y : ℂ` e todo `x`
tal que `x` e `x-1` estao no dominio, isto e, `x ∉ {0,-1,-2,...}`. -/
theorem stifel (x y : ℂ) (hx : ∀ n : ℕ, x ≠ -(n : ℂ)) :
    cbinom (x - 1) y + cbinom (x - 1) (y - 1) = cbinom x y := by
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

/-- Teorema "Continuous Star of David" (cap. 3), equacao (sod_product).
Vale para todos `n k : ℂ` com a convencao `(Γ)⁻¹ = 1/Γ` inteira; em particular
para `n k` reais com os seis coeficientes definidos (o enunciado do texto). -/
theorem star_of_david (n k : ℂ) :
    cbinom (n - 1) (k - 1) * cbinom n (k + 1) * cbinom (n + 1) k =
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

/-- Proposicao "Global Meromorphic Extension and Zero Loci" (cap. 3), parte dos zeros:
para `x` no dominio, `binom x y = 0` quando `y ∈ ℤ_{<0}`. -/
theorem cbinom_zero_of_y_neg (x : ℂ) (n : ℕ) :
    cbinom x (-(n : ℂ) - 1) = 0 := by
  unfold cbinom
  have : -(n : ℂ) - 1 + 1 = -(n : ℂ) := by ring
  rw [this, inv_Gamma_neg_nat]
  ring

/-- Mesma proposicao: `binom x y = 0` quando `x - y ∈ ℤ_{<0}`. -/
theorem cbinom_zero_of_xy_neg (x : ℂ) (n : ℕ) :
    cbinom x (x + n + 1) = 0 := by
  unfold cbinom
  have : x - (x + n + 1) + 1 = -(n : ℂ) := by ring
  rw [this, inv_Gamma_neg_nat]
  ring

/-- Mesma proposicao, parte de positividade: para `x > 0` real e `y ∈ [0, x]`,
o coeficiente e estritamente positivo (versao real com `Real.Gamma`). -/
theorem cbinom_real_pos (x y : ℝ) (hx : 0 < x) (hy0 : 0 ≤ y) (hyx : y ≤ x) :
    0 < Real.Gamma (x + 1) * (Real.Gamma (y + 1))⁻¹ * (Real.Gamma (x - y + 1))⁻¹ := by
  have h1 := Real.Gamma_pos_of_pos (show 0 < x + 1 by linarith)
  have h2 := Real.Gamma_pos_of_pos (show 0 < y + 1 by linarith)
  have h3 := Real.Gamma_pos_of_pos (show 0 < x - y + 1 by linarith)
  positivity

/-- Identidade discreta citada no cap. 3: soma de linha `∑ C(n,k) = 2^n`. -/
theorem row_sum (n : ℕ) : ∑ k ∈ Finset.range (n + 1), n.choose k = 2 ^ n :=
  Nat.sum_range_choose n

/-- Identidade discreta do multinomio citada no cap. 3: a soma dos coeficientes
multinomiais `n!/(k_0!...k_{m-1}!)` sobre as composicoes `k` de `n` em `m` partes vale `m^n`. -/
theorem multinomial_row_sum (m n : ℕ) :
    ∑ k ∈ Finset.piAntidiag (Finset.range m) n, Nat.multinomial (Finset.range m) k = m ^ n := by
  have h := Finset.sum_pow_eq_sum_piAntidiag (Finset.range m) (fun _ => (1 : ℕ)) n
  simpa using h.symm

end LeanReal.Chap03

#print axioms LeanReal.Chap03.stifel
#print axioms LeanReal.Chap03.star_of_david
#print axioms LeanReal.Chap03.cbinom_zero_of_y_neg
#print axioms LeanReal.Chap03.cbinom_zero_of_xy_neg
#print axioms LeanReal.Chap03.cbinom_real_pos
#print axioms LeanReal.Chap03.row_sum
#print axioms LeanReal.Chap03.multinomial_row_sum
#print axioms LeanReal.Chap03.inv_Gamma_neg_nat
