import LeanReal.Chap11MinCut
import LeanReal.Chap11Fisher

/-!
# L2 do lote LIVRO_B7: testemunha de compressao e forma basis-free do caso comutante

Verificador independente (L2).

* `witness_rank2`: em `ℂ³ ⊗ ℂ³`, um estado de posto de Schmidt 2 fatorado por uma ligacao de
  dimensao `2 = 2^1`. As hipoteses de `mincut_bound` valem com uma fatoracao NAO trivial
  (o indice interno e menor que `a` e `b`), a conclusao `S_A ≤ log 2` e atingida e e
  estritamente melhor que a cota trivial `log 3` de `vnS_le_log_card`. A testemunha do escritor
  (Bell, `r = b`) nao separa as duas cotas.
* `gBKM_eq_trace_of_commute`, `gSLD_eq_trace_of_commute`: se `[ρ₀, X] = 0` (forma
  `X_ij = 0` quando `p_i ≠ p_j`), ambas as metricas valem `∑_{ij} |X_ij|²/p_i =
  Re Tr(ρ₀⁻¹ X Xᴴ)`, numa base propria QUALQUER de `ρ₀`. E a forma correta da frase de
  `rem:sld_vs_bkm`; `fisherRao_needs_joint_basis` do escritor mostra que `∑ |X_ii|²/p_i` falha.
* `trace_form_ne_diag_form`: no exemplo degenerado do escritor, a forma basis-free da `4`,
  e a soma diagonal da `0`.
-/

noncomputable section

namespace LeanReal.L2_LIVRO_B7_Extra

open Matrix Real LeanReal.BeyondSpectrum3T2 LeanReal.Chap11MinCut LeanReal.Chap11Fisher

/-! ## 11.4: fatoracao nao trivial -/

/-- Amplitude `√(1/2)`. -/
def s : ℂ := ((Real.sqrt (1 / 2) : ℝ) : ℂ)

/-- `(|00⟩ + |11⟩)/√2` dentro de `ℂ³ ⊗ ℂ³`. -/
def v3 : Fin 3 × Fin 3 → ℂ := fun p => if p.1 = p.2 ∧ p.1.val < 2 then s else 0

/-- Fator esquerdo `3 × 2`. -/
def U3 : Matrix (Fin 3) (Fin 2) ℂ := fun i α => if i.val = α.val then s else 0

/-- Fator direito `2 × 3`. -/
def V3 : Matrix (Fin 2) (Fin 3) ℂ := fun α j => if α.val = j.val then 1 else 0

theorem s_mul_star : s * star s = ((1 / 2 : ℝ) : ℂ) := sqrt_mul_star (by norm_num)

theorem s_mul_conj : s * (starRingEnd ℂ) s = 2⁻¹ := by
  have h := s_mul_star
  rw [Complex.star_def] at h
  rw [h]; push_cast; norm_num

theorem v3_normalised : ∑ p, v3 p * star (v3 p) = 1 := by
  simp only [Fintype.sum_prod_type, Fin.sum_univ_three, v3]
  simp [s_mul_conj]
  norm_num

theorem v3_factor : coef v3 = U3 * V3 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [coef, v3, U3, V3, mul_apply, Fin.sum_univ_two]

theorem ptr2_v3 :
    ptr2 (proj v3) = diagonal fun i => (((![1 / 2, 1 / 2, 0] : Fin 3 → ℝ) i : ℝ) : ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [ptr2, proj, vecMulVec_apply, v3, s_mul_conj]

theorem vnS_v3 : vnS (ptr2 (proj v3)) = Real.log 2 := by
  rw [ptr2_v3, vnS_diagonal]
  simp [Fin.sum_univ_three, negMulLog, one_div, Real.log_inv]
  ring

/-- Hipoteses de `mincut_bound` com `χ = 2`, `k = 1`, `r = Fin 2` menor que `a = b = Fin 3`;
a cota `1 · log 2` e atingida e e estritamente menor que a cota trivial `log 3`. -/
theorem witness_rank2 :
    (∑ p, v3 p * star (v3 p) = 1) ∧ coef v3 = U3 * V3 ∧
    vnS (ptr2 (proj v3)) ≤ ((1 : ℕ) : ℝ) * Real.log (2 : ℕ) ∧
    vnS (ptr2 (proj v3)) = Real.log 2 ∧
    Real.log 2 < Real.log (Fintype.card (Fin 3)) := by
  refine ⟨v3_normalised, v3_factor,
    mincut_bound v3_normalised 2 1 (by simp) U3 V3 v3_factor, vnS_v3, ?_⟩
  simp only [Fintype.card_fin, Nat.cast_ofNat]
  exact Real.log_lt_log (by norm_num) (by norm_num)

/-- Mutante: a mesma cota com uma ligacao de dimensao `1` (`k = 0`) e falsa para `v3`;
logo nenhum fator `coef v3 = U V` passa por um indice de cardinal `1`. -/
theorem mutant_rank2_no_factor_dim1 :
    ¬ ∃ (U : Matrix (Fin 3) (Fin 1) ℂ) (V : Matrix (Fin 1) (Fin 3) ℂ), coef v3 = U * V := by
  rintro ⟨U, V, h⟩
  have hb := mincut_bound (r := Fin 1) v3_normalised 2 0 (by simp) U V h
  rw [vnS_v3] at hb
  have : (0 : ℝ) < Real.log 2 := Real.log_pos (by norm_num)
  simp at hb
  linarith

/-! ## `rem:sld_vs_bkm`: forma basis-free do caso de igualdade -/

/-- Caso comutante: `g^BKM(X,X) = ∑_{ij} |X_ij|²/p_i` numa base propria qualquer de `ρ₀`. -/
theorem gBKM_eq_sum_of_commute {n : Type*} [Fintype n] (p : n → ℝ) (X : Matrix n n ℂ)
    (hc : ∀ i j, p i ≠ p j → X i j = 0) :
    gBKM p X = ∑ i, ∑ j, Complex.normSq (X i j) / p i := by
  unfold gBKM
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
  by_cases hij : p i = p j
  · rw [logMeanInv, ite_eq_left_of_eq_true _ _ (eq_true hij)]; ring
  · rw [hc i j hij]; simp

/-- Caso comutante: `g^SLD(X,X)` tem o mesmo valor. -/
theorem gSLD_eq_sum_of_commute {n : Type*} [Fintype n] (p : n → ℝ) (hp : ∀ i, 0 < p i)
    (X : Matrix n n ℂ) (hc : ∀ i j, p i ≠ p j → X i j = 0) :
    gSLD p X = ∑ i, ∑ j, Complex.normSq (X i j) / p i := by
  rw [← gBKM_eq_sum_of_commute p X hc]
  exact ((gBKM_eq_gSLD_iff p hp X).mpr hc).symm

/-- `∑_{ij} |X_ij|²/p_i = Re Tr(ρ₀⁻¹ X Xᴴ)`, com `ρ₀ = diag p`: a forma basis-free. -/
theorem sum_eq_trace {n : Type*} [Fintype n] [DecidableEq n] (p : n → ℝ) (X : Matrix n n ℂ) :
    ∑ i, ∑ j, Complex.normSq (X i j) / p i =
      (trace (diagonal (fun i => ((p i)⁻¹ : ℂ)) * X * Xᴴ)).re := by
  unfold trace
  rw [Complex.re_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [diag_apply, Matrix.mul_assoc, diagonal_mul, mul_apply]
  have h : ∀ j, X i j * Xᴴ j i = ((Complex.normSq (X i j) : ℝ) : ℂ) := fun j => by
    rw [conjTranspose_apply, Complex.star_def, Complex.mul_conj]
  simp_rw [h]
  rw [← Complex.ofReal_sum, ← Complex.ofReal_inv, ← Complex.ofReal_mul, Complex.ofReal_re,
    Finset.mul_sum]
  exact Finset.sum_congr rfl fun j _ => by ring

/-- No exemplo degenerado do escritor (`p = (1/2,1/2)`, `X = σ_x`, que comuta com `ρ₀`), a forma
correta vale `4 = g^BKM = g^SLD`, e a soma diagonal `∑ |X_ii|²/p_i` vale `0`. -/
theorem trace_form_ne_diag_form :
    gBKM ![1 / 2, 1 / 2] Xoff = ∑ i, ∑ j, Complex.normSq (Xoff i j) / (![1 / 2, 1 / 2] : Fin 2 → ℝ) i ∧
    ∑ i, ∑ j, Complex.normSq (Xoff i j) / (![1 / 2, 1 / 2] : Fin 2 → ℝ) i = 4 ∧
    ∑ i, Complex.normSq (Xoff i i) / (![1 / 2, 1 / 2] : Fin 2 → ℝ) i = 0 := by
  refine ⟨gBKM_eq_sum_of_commute _ _ fun i j hij => by
      fin_cases i <;> fin_cases j <;> simp at hij, ?_, ?_⟩
  · simp [Xoff, Fin.sum_univ_two]; norm_num
  · simp [Xoff, Fin.sum_univ_two]

end LeanReal.L2_LIVRO_B7_Extra

#print axioms LeanReal.L2_LIVRO_B7_Extra.witness_rank2
#print axioms LeanReal.L2_LIVRO_B7_Extra.mutant_rank2_no_factor_dim1
#print axioms LeanReal.L2_LIVRO_B7_Extra.gBKM_eq_sum_of_commute
#print axioms LeanReal.L2_LIVRO_B7_Extra.gSLD_eq_sum_of_commute
#print axioms LeanReal.L2_LIVRO_B7_Extra.sum_eq_trace
#print axioms LeanReal.L2_LIVRO_B7_Extra.trace_form_ne_diag_form
