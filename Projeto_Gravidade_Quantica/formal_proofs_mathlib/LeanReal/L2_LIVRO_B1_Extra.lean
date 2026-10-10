import LeanReal.Chap08Pointwise

/-!
# L2, Lote LIVRO_B1: testemunha e mutante extras para `Chap08Pointwise` (item 8.8)

* `book_form_rn_horizon_mots`: o enunciado na forma do livro, COM a hipotese `K^r_r = β'`
  (`β'` real arbitrario), segue de `rn_horizon_mots`. Logo retirar a hipotese so generaliza.
* `mutant_no_Kss_false`: sem o termo `K_ss` (`θ_l = D_i s^i - K`), `θ_l(r₊) = 0` e FALSO
  (`M = 1`, `Q = 1/2`, `K^r_r = 7` da `θ_l = -7`). O cancelamento de `K^r_r` vem do termo
  `K_ss = K^r_r`, nao de uma hipotese vacua.
-/

noncomputable section

namespace LeanReal.L2_LIVRO_B1_Extra

open Real LeanReal.Chap08Pointwise

/-- Forma do livro (`prop:rn_horizon`(2)) com `K^r_r = β'` mantida. -/
theorem book_form_rn_horizon_mots {M Q : ℝ} (hM : 0 < M) (hQ : |Q| ≤ M)
    (β' divS Krr Kθθ Kφφ trK Kss θl : ℝ) (_hKrr : Krr = β') (hdiv : divS = 2 / rPlus M Q)
    (hKθθ : Kθθ = betaPG M Q (rPlus M Q) / rPlus M Q)
    (hKφφ : Kφφ = betaPG M Q (rPlus M Q) / rPlus M Q)
    (htr : trK = Krr + Kθθ + Kφφ) (hss : Kss = Krr) (hθl : θl = divS - trK + Kss) :
    θl = 0 :=
  rn_horizon_mots hM hQ divS Krr Kθθ Kφφ trK Kss θl hdiv hKθθ hKφφ htr hss hθl

/-- Mutante 8.8b: sem o termo `K_ss`, a conclusao MOTS e falsa. -/
theorem mutant_no_Kss_false :
    ¬ (∀ (M Q Krr : ℝ), 0 < M → |Q| ≤ M →
        2 / rPlus M Q - (Krr + betaPG M Q (rPlus M Q) / rPlus M Q +
          betaPG M Q (rPlus M Q) / rPlus M Q) = 0) := by
  intro h
  have hQ : |(1 / 2 : ℝ)| ≤ 1 := by rw [abs_of_pos (by norm_num)]; norm_num
  have := h 1 (1 / 2) 7 one_pos hQ
  rw [betaPG_rPlus one_pos hQ] at this
  have hr : 0 < rPlus 1 (1 / 2) := lt_trans (by norm_num) (rPlus_gt one_pos hQ)
  have e : 2 / rPlus 1 (1 / 2) - (7 + 1 / rPlus 1 (1 / 2) + 1 / rPlus 1 (1 / 2)) = -7 := by
    field_simp; ring
  rw [e] at this; norm_num at this

end LeanReal.L2_LIVRO_B1_Extra

#print axioms LeanReal.L2_LIVRO_B1_Extra.book_form_rn_horizon_mots
#print axioms LeanReal.L2_LIVRO_B1_Extra.mutant_no_Kss_false
