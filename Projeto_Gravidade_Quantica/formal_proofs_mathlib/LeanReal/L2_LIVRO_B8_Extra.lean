import LeanReal.Chap10Generalization
import LeanReal.Chap09WindingBounds

/-!
# L2 do lote LIVRO_B8: forma quase certa do gap e varredura angular estrita

Verificador independente (L2).

* `gap_ge_half_ae`: a forma do livro "para toda lei das entradas sob a qual `X` tem posto `N`
  quase certamente". A amostra e uma variavel aleatoria `ω ↦ (X ω, y ω)` sob uma lei `P`
  qualquer; se `rank (X ω) = N` para `P`-quase todo `ω`, o gap e `≥ 1/2` para `P`-quase todo
  `ω`, para toda lei `μ` da entrada nova.
* `mutant_ae_no_rank_false`: sem a hipotese de posto q.c. a conclusao q.c. falha (amostra
  constante `X = 0`, lei de Dirac).
* `angular_sweep_bound_strict`: a integracao na forma ESTRITA do livro,
  `|Δφ| < Δt/(3√3M)`, quando `a < b`. Com `winding_count_bound_strict` do escritor, fecha a
  cadeia estrita do Remark do estilingue.
-/

noncomputable section

namespace LeanReal.L2_LIVRO_B8_Extra

open Set Real Matrix MeasureTheory LeanReal.Chap10Generalization LeanReal.Chap09WindingBounds

/-! ## 10.2(2): posto `N` quase certamente -/

/-- **`prop:counterexample` (2), forma q.c.**: se a amostra aleatoria tem posto linha cheio
`N` quase certamente, o gap de generalizacao do interpolante de norma minima e `≥ 1/2` quase
certamente, para toda lei de probabilidade `μ` da entrada nova. -/
theorem gap_ge_half_ae {N D : ℕ} {Ω : Type*} [MeasurableSpace Ω] (P : Measure Ω)
    (X : Ω → Matrix (Fin N) (Fin D) ℝ) (y : Ω → Fin N → ℝ)
    (hrank : ∀ᵐ ω ∂P, (X ω).rank = N) (μ : Measure (Fin D → ℝ)) [IsProbabilityMeasure μ] :
    ∀ᵐ ω ∂P, 1 / 2 ≤ testLoss μ (thetaStar (X ω) (y ω)) -
      trainLoss (X ω) (y ω) (thetaStar (X ω) (y ω)) :=
  hrank.mono fun ω h => gap_ge_half (X ω) h (y ω) μ

/-- Mutante: sem posto q.c. (amostra constante `X = 0` sob uma lei de Dirac), a conclusao
q.c. e FALSA: o gap vale `1 - 1 = 0`. -/
theorem mutant_ae_no_rank_false :
    ¬ (∀ᵐ _ω ∂(Measure.dirac (0 : ℝ)),
        1 / 2 ≤ testLoss (Measure.dirac (0 : Fin 2 → ℝ))
            (thetaStar (0 : Matrix (Fin 1) (Fin 2) ℝ) (fun _ => 1)) -
          trainLoss (0 : Matrix (Fin 1) (Fin 2) ℝ) (fun _ => 1)
            (thetaStar (0 : Matrix (Fin 1) (Fin 2) ℝ) (fun _ => 1))) := by
  obtain ⟨h0, htr, hte⟩ := zero_data_losses
  rw [h0, htr, hte, Filter.eventually_const]
  norm_num

/-! ## Estilingue: integracao estrita -/

/-- **Remark apos `conj:slingshot`**, forma estrita: ao longo de uma curva tipo-tempo futura no
plano equatorial de Schwarzschild, fora do horizonte, com `a < b`,
`|φ(b) - φ(a)| < (t(b) - t(a))/(3√3M)`. -/
theorem angular_sweep_bound_strict (M a b : ℝ) (t φ ρ t' φ' ρ' : ℝ → ℝ) (hM : 0 < M)
    (hab : a < b)
    (htc : ContinuousOn t (Icc a b)) (hφc : ContinuousOn φ (Icc a b))
    (ht : ∀ s ∈ Ioo a b, HasDerivAt t (t' s) s) (hφ : ∀ s ∈ Ioo a b, HasDerivAt φ (φ' s) s)
    (hρ : ∀ s ∈ Ioo a b, 2 * M < ρ s)
    (hfut : ∀ s ∈ Ioo a b, 0 < t' s)
    (htl : ∀ s ∈ Ioo a b, -(1 - 2 * M / ρ s) * t' s ^ 2 + ρ' s ^ 2 / (1 - 2 * M / ρ s) +
      ρ s ^ 2 * φ' s ^ 2 < 0) :
    |φ b - φ a| < (t b - t a) / (3 * √3 * M) := by
  set K := 1 / (3 * √3 * M) with hK
  have hpt : ∀ s ∈ Ioo a b, |φ' s| < K * t' s := by
    intro s hs
    have hρ0 : 0 < ρ s := by linarith [hρ s hs]
    have hf : 0 < 1 - 2 * M / ρ s := by
      rw [sub_pos, div_lt_one hρ0]; exact hρ s hs
    have h1 := timelike_angular_rate _ _ _ _ _ hf hρ0 (htl s hs)
    rw [abs_of_pos (hfut s hs)] at h1
    have h2 := orbital_rate_max M (ρ s) hM (hρ s hs)
    have h3 : √(1 - 2 * M / ρ s) / ρ s * t' s ≤ K * t' s :=
      mul_le_mul_of_nonneg_right h2 (hfut s hs).le
    linarith
  have mono : ∀ σ : ℝ, σ = 1 ∨ σ = -1 → σ * (φ b - φ a) < K * (t b - t a) := by
    intro σ hσ
    have hmon : StrictMonoOn (fun s => K * t s - σ * φ s) (Icc a b) := by
      refine strictMonoOn_of_hasDerivWithinAt_pos (f' := fun s => K * t' s - σ * φ' s)
        (convex_Icc a b) ((htc.const_smul K).sub (hφc.const_smul σ)) ?_ ?_
      · intro s hs
        rw [interior_Icc] at hs
        exact (((ht s hs).const_mul K).sub ((hφ s hs).const_mul σ)).hasDerivWithinAt
      · intro s hs
        rw [interior_Icc] at hs
        have := hpt s hs
        rcases hσ with rfl | rfl
        · have := le_abs_self (φ' s); show 0 < K * t' s - (1:ℝ) * φ' s; linarith
        · have := neg_abs_le (φ' s); show 0 < K * t' s - (-1:ℝ) * φ' s; linarith
    have := hmon ⟨le_rfl, hab.le⟩ ⟨hab.le, le_rfl⟩ hab
    simp only at this
    linarith
  have hp := mono 1 (Or.inl rfl)
  have hn := mono (-1) (Or.inr rfl)
  rw [abs_lt]
  have : K * (t b - t a) = (t b - t a) / (3 * √3 * M) := by rw [hK]; ring
  constructor <;> linarith

/-- Testemunha da forma estrita: a orbita do escritor (`r = 3`, `M = 1`, `φ̇ = 1/10`). -/
theorem witness_sweep_strict :
    |(fun s : ℝ => s / 10) 1 - (fun s : ℝ => s / 10) 0| < ((id 1 : ℝ) - id 0) / (3 * √3 * 1) :=
  angular_sweep_bound_strict 1 0 1 id (fun s => s / 10) (fun _ => 3) (fun _ => 1)
    (fun _ => 1 / 10) (fun _ => 0) one_pos zero_lt_one continuousOn_id
    (continuous_id.div_const 10).continuousOn (fun s _ => hasDerivAt_id s)
    (fun s _ => by simpa using (hasDerivAt_id s).div_const 10) (fun _ _ => by norm_num)
    (fun _ _ => one_pos) (fun _ _ => by norm_num)

/-- Mutante: com `a = b` a forma estrita e FALSA (`0 < 0`), logo `a < b` e necessario. -/
theorem mutant_strict_degenerate_false :
    ¬ (∀ (t φ : ℝ → ℝ), |φ 0 - φ 0| < (t 0 - t 0) / (3 * √3 * 1)) := by
  intro h
  have := h id id
  simp at this

end LeanReal.L2_LIVRO_B8_Extra

#print axioms LeanReal.L2_LIVRO_B8_Extra.gap_ge_half_ae
#print axioms LeanReal.L2_LIVRO_B8_Extra.mutant_ae_no_rank_false
#print axioms LeanReal.L2_LIVRO_B8_Extra.angular_sweep_bound_strict
#print axioms LeanReal.L2_LIVRO_B8_Extra.witness_sweep_strict
#print axioms LeanReal.L2_LIVRO_B8_Extra.mutant_strict_degenerate_false
