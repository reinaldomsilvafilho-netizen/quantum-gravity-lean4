import LeanReal.Chap08UTurn
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

/-!
# L2 do lote LIVRO_B2: testemunha e mutantes extras

Arquivo do verificador L2 (nao do escritor). Acrescenta:
* `mutant_uturn_no_start_false`: sem `θ(0) = 0` (direcao inicial `(1,0)`), `lem:euclidean_uturn`
  e falso (quarto de circulo de `(0,1)`-direcao ate `(-1,0)`).
* `mutant_window_no_rise_false`: sem a hipotese de subida `φ(p) + π ≤ φ(q)`, a selecao
  `exists_halfturn_window` e falsa.
* `witness_uturn_angle_leaves`: uma U-turn cujo angulo SAI de `[0,π]` (`θ(s) = s² - s`), logo fora
  do alcance de `Chap09MouthHalfturn.mouth_halfturn`, satisfaz todas as hipoteses de
  `Chap08UTurn.uturn_strip`; a curva e definida por integrais do angulo.
-/

noncomputable section

namespace LeanReal.L2_LIVRO_B2_Extra

open Set Real LeanReal.Chap08UTurn

/-- Mutante: sem `θ 0 = 0`, o lema da U-turn e falso. Curva `s ↦ (cos s, sin s)` em `[0, π/2]`,
angulo `s + π/2` (de `π/2` ate `π`), `k = 1`, faixa `ℝ × [0,1]`: `2 ≤ 1·1` e falso. -/
theorem mutant_uturn_no_start_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L k w : ℝ), 0 ≤ L →
        ContinuousOn γ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s) →
        (∀ s ∈ Ioo 0 L, |θ' s| ≤ k) → cos (θ L) = -1 →
        (∀ s ∈ Icc 0 L, (γ s).2 ∈ Icc 0 w) → 2 ≤ k * w) := by
  intro h
  have := h (fun s => (cos s, sin s)) (fun s => s + π / 2) (fun _ => 1) (π / 2) 1 1
    (by positivity) (by fun_prop)
    (fun s _ => by
      rw [cos_add_pi_div_two, sin_add_pi_div_two]
      exact (hasDerivAt_cos s).prodMk (hasDerivAt_sin s))
    (by fun_prop)
    (fun s _ => by simpa using (hasDerivAt_id s).add_const (π / 2))
    (fun s _ => by norm_num)
    (by rw [add_halves, cos_pi])
    (fun s hs => ⟨sin_nonneg_of_nonneg_of_le_pi hs.1 (by linarith [hs.2, pi_pos]),
      sin_le_one s⟩)
  norm_num at this

/-- Mutante: sem `φ p + π ≤ φ q`, a selecao e falsa (`φ ≡ 0`, `p = q = 0`). -/
theorem mutant_window_no_rise_false :
    ¬ (∀ (φ : ℝ → ℝ) (p q : ℝ), p ≤ q → ContinuousOn φ (Icc p q) →
        ∃ a b, p ≤ a ∧ a ≤ b ∧ b ≤ q ∧ φ a = φ p ∧ φ b = φ p + π ∧
          ∀ s ∈ Icc a b, φ s ∈ Icc (φ p) (φ p + π)) := by
  intro h
  obtain ⟨a, b, -, -, -, -, hb, -⟩ := h (fun _ => 0) 0 0 le_rfl continuousOn_const
  simp only [zero_add] at hb
  exact pi_pos.ne' hb.symm

/-! ## Testemunha com angulo fora de `[0, π]` -/

/-- Angulo tangente `θ(s) = s² - s` (negativo em `(0,1)`). -/
def th (s : ℝ) : ℝ := s ^ 2 - s

/-- Comprimento: a raiz positiva de `L² - L = π`. -/
def Lw : ℝ := (1 + √(1 + 4 * π)) / 2

/-- A curva de angulo `th`, definida por integrais. -/
def gam (s : ℝ) : ℝ × ℝ := (∫ t in (0 : ℝ)..s, cos (th t), ∫ t in (0 : ℝ)..s, sin (th t))

theorem th_continuous : Continuous th := by unfold th; fun_prop

theorem gam_hasDerivAt (s : ℝ) : HasDerivAt gam (cos (th s), sin (th s)) s := by
  have h1 := ((continuous_cos.comp th_continuous).integral_hasStrictDerivAt 0 s).hasDerivAt
  have h2 := ((continuous_sin.comp th_continuous).integral_hasStrictDerivAt 0 s).hasDerivAt
  exact h1.prodMk h2

theorem th_hasDerivAt (s : ℝ) : HasDerivAt th (2 * s - 1) s := by
  show HasDerivAt (fun s => s ^ 2 - s) _ s
  have := (hasDerivAt_pow 2 s).sub (hasDerivAt_id' s)
  convert this using 1
  norm_num

theorem one_le_Lw : 1 ≤ Lw := by
  unfold Lw
  have : 1 ≤ √(1 + 4 * π) := by
    have h := Real.sqrt_le_sqrt (show (1 : ℝ) ≤ 1 + 4 * π by linarith [pi_pos])
    rwa [Real.sqrt_one] at h
  linarith

theorem th_Lw : th Lw = π := by
  unfold th Lw
  have hs := Real.sq_sqrt (show (0 : ℝ) ≤ 1 + 4 * π by linarith [pi_pos])
  nlinarith [hs]

/-- **Testemunha L2**: o angulo sai de `[0, π]` (`θ(1/2) < 0`), e a curva satisfaz todas as
hipoteses de `uturn_strip` com `k = 2L - 1`, faixa `[-L, L]`. -/
theorem witness_uturn_angle_leaves :
    th (1 / 2) < 0 ∧ (1 / 2 : ℝ) ∈ Icc 0 Lw ∧ 2 ≤ (2 * Lw - 1) * (Lw - -Lw) := by
  have hL1 := one_le_Lw
  refine ⟨by norm_num [th], ⟨by norm_num, by linarith⟩, ?_⟩
  refine uturn_strip gam th (fun s => 2 * s - 1) Lw (2 * Lw - 1) (-Lw) Lw (by linarith)
    (continuous_iff_continuousAt.2 fun s => (gam_hasDerivAt s).continuousAt).continuousOn
    (fun s _ => gam_hasDerivAt s) th_continuous.continuousOn
    (fun s _ => th_hasDerivAt s)
    (fun s hs => by rw [abs_le]; constructor <;> linarith [hs.1, hs.2])
    (by norm_num [th]) (by rw [th_Lw, cos_pi]) ?_
  intro s hs
  have hb : ‖∫ t in (0 : ℝ)..s, sin (th t)‖ ≤ 1 * |s - 0| :=
    intervalIntegral.norm_integral_le_of_norm_le_const (fun t _ => by
      simpa using abs_sin_le_one (th t))
  rw [Real.norm_eq_abs, sub_zero, abs_of_nonneg hs.1, one_mul] at hb
  have := abs_le.mp hb
  exact ⟨by simp only [gam]; linarith [this.1, hs.2], by simp only [gam]; linarith [this.2, hs.2]⟩

end LeanReal.L2_LIVRO_B2_Extra

#print axioms LeanReal.L2_LIVRO_B2_Extra.mutant_uturn_no_start_false
#print axioms LeanReal.L2_LIVRO_B2_Extra.mutant_window_no_rise_false
#print axioms LeanReal.L2_LIVRO_B2_Extra.witness_uturn_angle_leaves
