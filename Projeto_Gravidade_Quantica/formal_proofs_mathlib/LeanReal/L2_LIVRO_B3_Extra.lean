import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.Real.Pi.Bounds

/-!
# L2 LIVRO B3: mutantes extra para os numeros do cap. 13

Revisao L2 de `Chap13Numbers`. O mutante do escritor `mutant_H_three_digits_false` usa `r = 0.036`
exatamente, fora da hipotese estrita do livro (`r < 0.036`). Aqui mostramos que as formas literais
do livro falham ja DENTRO da hipotese `r < 0.036`:

* "`H_inf ≤ 4.7 × 10¹³` GeV": ha `r < 0.036` com `H = 4.702 × 10¹³` GeV;
* "`|α_t| ≤ 3.7 × 10⁻¹⁰` para `M_* = M_red`": no mesmo ponto `|α_t| > 3.7 × 10⁻¹⁰`.

Unidades naturais: `H`, `M_P` em GeV; `r`, `A_s`, `α_t` adimensionais.
-/

noncomputable section
namespace LeanReal.L2_LIVRO_B3_Extra
open Real

/-- A relacao `2H²/(π² M_red²) = 16 H²/(π M_P²)` com `M_red = M_P/√(8π)`. -/
theorem rel_eq (H MP : ℝ) (hMP : 0 < MP) :
    2 * H ^ 2 / (π ^ 2 * (MP / √(8 * π)) ^ 2) = 16 * H ^ 2 / (π * MP ^ 2) := by
  have hpi := pi_pos
  rw [div_pow, sq_sqrt (by positivity)]
  field_simp
  ring

/-- O valor de `r` que produz `H` pela relacao do livro (`A_s = 2.1 × 10⁻⁹`,
`M_P = 1.22089 × 10¹⁹` GeV). -/
def rOf (H : ℝ) : ℝ := 16 * H ^ 2 / (π * (1.22089e19 : ℝ) ^ 2) / 2.1e-9

theorem rOf_rel (H : ℝ) :
    2 * H ^ 2 / (π ^ 2 * ((1.22089e19 : ℝ) / √(8 * π)) ^ 2) = rOf H * 2.1e-9 := by
  rw [rel_eq _ _ (by norm_num), rOf]
  field_simp

theorem rOf_lt : rOf 4.702e13 < 0.036 := by
  have h := pi_gt_d2
  have hpi := pi_pos
  unfold rOf
  rw [div_div, div_lt_iff₀ (by positivity)]
  nlinarith

/-- Mutante (forma literal do livro, "`H_inf ≤ 4.7 × 10¹³` GeV" sob `r < 0.036`): FALSA.
Testemunha `H = 4.702 × 10¹³` GeV, `r ≈ 0.03597 < 0.036`. -/
theorem mutant_H_book_literal_false :
    ¬ (∀ H r : ℝ, 0 < H → r < 0.036 →
        2 * H ^ 2 / (π ^ 2 * ((1.22089e19 : ℝ) / √(8 * π)) ^ 2) = r * 2.1e-9 → H ≤ 4.7e13) := by
  intro h
  have := h 4.702e13 (rOf 4.702e13) (by norm_num) rOf_lt (rOf_rel _)
  norm_num at this

/-- Mutante (forma literal do livro, "`|α_t| ≤ 3.7 × 10⁻¹⁰` para `M_* = M_red`" sob `r < 0.036`):
FALSA no mesmo ponto `H = 4.702 × 10¹³` GeV, onde `|α_t| ≈ 3.728 × 10⁻¹⁰`. -/
theorem mutant_alpha_red_book_literal_false :
    ¬ (∀ H r : ℝ, 0 < H → r < 0.036 →
        2 * H ^ 2 / (π ^ 2 * ((1.22089e19 : ℝ) / √(8 * π)) ^ 2) = r * 2.1e-9 →
        (H / (1.22089e19 / √(8 * π))) ^ 2 / (1 + (H / (1.22089e19 / √(8 * π))) ^ 2) ≤ 3.7e-10) := by
  intro h
  have hle := h 4.702e13 (rOf 4.702e13) (by norm_num) rOf_lt (rOf_rel _)
  have hpi := pi_pos
  have h314 := pi_gt_d2
  have hx : ((4.702e13 : ℝ) / (1.22089e19 / √(8 * π))) ^ 2 =
      8 * π * (4.702e13 : ℝ) ^ 2 / (1.22089e19 : ℝ) ^ 2 := by
    rw [div_pow, div_pow, sq_sqrt (by positivity)]
    field_simp
  set X : ℝ := 8 * π * (4.702e13 : ℝ) ^ 2 / (1.22089e19 : ℝ) ^ 2 with hX
  have hXlb : (3.7001e-10 : ℝ) < X := by
    rw [hX, lt_div_iff₀ (by positivity)]
    nlinarith
  have hXpos : 0 < 1 + X := by linarith
  rw [hx, div_le_iff₀ hXpos] at hle
  linarith

end LeanReal.L2_LIVRO_B3_Extra

#print axioms LeanReal.L2_LIVRO_B3_Extra.rel_eq
#print axioms LeanReal.L2_LIVRO_B3_Extra.rOf_lt
#print axioms LeanReal.L2_LIVRO_B3_Extra.mutant_H_book_literal_false
#print axioms LeanReal.L2_LIVRO_B3_Extra.mutant_alpha_red_book_literal_false
