import LeanReal.Chap03Special

/-!
# L2 do lote LIVRO_A_B3: testemunhas e mutante extras para `transport`

Revisao L2 de `LeanReal.Chap03Special`. O modulo revisado prova a equacao de transporte
literal (`transport`) com `x+1, y+1 ∉ ℤ_{≤0}`, mas nao tem testemunha nem mutante proprios.
Aqui:
* `witness_transport`: em `x = 1`, `y = 1/2` as hipoteses valem e a derivada e nao nula;
* `transport_on_line`: em `x = 0`, `y = 1` (reta `x - y = -1`) a hipotese de `pde_x` sobre
  `x-y+1` falha, mas `transport` se aplica (o livro: "needs no extension");
* `mutant_transport_no_hy_false`: sem a hipotese `y+1 ∉ ℤ_{≤0}` a equacao de transporte
  literal e falsa em `x = 0`, `y = -1`: `t ↦ binom(t, t-1)` tem derivada `1` em `0`, mas o
  lado direito e `binom(0,-1)·(...) = 0`.
-/

noncomputable section

namespace LeanReal.L2_LIVRO_A_B3_Extra

open LeanReal.Chap03 (cbinom)
open LeanReal.Chap03Special

/-- Testemunha nao degenerada de `transport`: `x = 1`, `y = 1/2`; as hipoteses valem e o valor
`binom(1,1/2)[ψ(2) - ψ(3/2)]` da derivada e nao nulo. -/
theorem witness_transport :
    (∀ m : ℕ, (1 : ℂ) + 1 ≠ -(m : ℂ)) ∧ (∀ m : ℕ, (1 / 2 : ℂ) + 1 ≠ -(m : ℂ)) ∧
      HasDerivAt (fun t => cbinom (1 + t) (1 / 2 + t))
        (cbinom 1 (1 / 2) * (Complex.digamma (1 + 1) - Complex.digamma (1 / 2 + 1))) 0 ∧
      cbinom 1 (1 / 2) * (Complex.digamma (1 + 1) - Complex.digamma (1 / 2 + 1)) ≠ 0 := by
  obtain ⟨h1, h2, -, hne⟩ := witness_pde_x
  refine ⟨h1, h2, transport 1 (1 / 2) h1 h2, ?_⟩
  rw [show (1 : ℂ) / 2 + 1 = 1 - 1 / 2 + 1 by norm_num]
  exact hne

/-- Na reta `x - y = -1` (`x = 0`, `y = 1`) a hipotese `x-y+1 ∉ ℤ_{≤0}` de `pde_x` falha, mas
`transport` se aplica: a equacao de transporte literal vale ali sem extensao. -/
theorem transport_on_line :
    ¬ (∀ m : ℕ, (0 : ℂ) - 1 + 1 ≠ -(m : ℂ)) ∧
      HasDerivAt (fun t => cbinom (0 + t) (1 + t))
        (cbinom 0 1 * (Complex.digamma (0 + 1) - Complex.digamma (1 + 1))) 0 := by
  refine ⟨fun h => h 0 (by norm_num), transport 0 1 ?_ ?_⟩
  · exact ne_neg_nat_of_re_pos (by norm_num)
  · exact ne_neg_nat_of_re_pos (by norm_num)

/-- `t ↦ binom(t, t-1)` tem derivada `1` em `t = 0`. -/
theorem hasDerivAt_diag_neg_one :
    HasDerivAt (fun t : ℂ => cbinom (0 + t) (-1 + t)) 1 0 := by
  have hfun : (fun t : ℂ => cbinom (0 + t) (-1 + t)) = fun t =>
      Complex.Gamma (t + 1) * (Complex.Gamma ((t - 1) + 1))⁻¹ * (Complex.Gamma 2)⁻¹ := by
    funext t
    unfold cbinom
    rw [show (0 : ℂ) + t + 1 = t + 1 by ring, show -1 + t + 1 = t - 1 + 1 by ring,
      show (0 : ℂ) + t - (-1 + t) + 1 = 2 by ring]
  rw [hfun]
  have h1 : HasDerivAt (fun t : ℂ => Complex.Gamma (t + 1))
      (Complex.Gamma (0 + 1) * Complex.digamma (0 + 1)) 0 :=
    (hasDerivAt_Gamma_digamma (ne_neg_nat_of_re_pos (by norm_num))).comp_add_const 0 1
  have hh : HasDerivAt (fun s : ℂ => (Complex.Gamma (s + 1))⁻¹) 1 ((fun t : ℂ => t - 1) 0) := by
    simpa using hasDerivAt_inv_Gamma_succ_at_neg_one
  have h2' := HasDerivAt.comp (h₂ := fun s : ℂ => (Complex.Gamma (s + 1))⁻¹)
    (h := fun t : ℂ => t - 1) (0 : ℂ) hh ((hasDerivAt_id' (0 : ℂ)).sub_const 1)
  have h2 : HasDerivAt (fun t : ℂ => (Complex.Gamma ((t - 1) + 1))⁻¹) (1 * 1) 0 := h2'
  have := (h1.mul h2).mul_const (Complex.Gamma 2)⁻¹
  refine this.congr_deriv ?_
  simp [Complex.Gamma_zero, Complex.Gamma_one]

/-- Mutante (equacao de transporte literal sem `y+1 ∉ ℤ_{≤0}`): falso em `x = 0`, `y = -1`. -/
theorem mutant_transport_no_hy_false :
    ¬ (∀ x y : ℂ, (∀ m : ℕ, x + 1 ≠ -(m : ℂ)) →
      HasDerivAt (fun t => cbinom (x + t) (y + t))
        (cbinom x y * (Complex.digamma (x + 1) - Complex.digamma (y + 1))) 0) := by
  intro h
  have hx : ∀ m : ℕ, (0 : ℂ) + 1 ≠ -(m : ℂ) := ne_neg_nat_of_re_pos (by norm_num)
  have hu := hasDerivAt_diag_neg_one.unique (h 0 (-1) hx)
  have hz : cbinom 0 (-1) = 0 := by
    simpa using LeanReal.Chap03.cbinom_zero_of_y_neg 0 0
  rw [hz, zero_mul] at hu
  exact one_ne_zero hu

end LeanReal.L2_LIVRO_A_B3_Extra

#print axioms LeanReal.L2_LIVRO_A_B3_Extra.witness_transport
#print axioms LeanReal.L2_LIVRO_A_B3_Extra.transport_on_line
#print axioms LeanReal.L2_LIVRO_A_B3_Extra.hasDerivAt_diag_neg_one
#print axioms LeanReal.L2_LIVRO_A_B3_Extra.mutant_transport_no_hy_false
