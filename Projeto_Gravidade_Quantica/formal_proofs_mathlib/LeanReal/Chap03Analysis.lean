import LeanReal.Chap03Pascal
import Mathlib.Analysis.SpecialFunctions.Gamma.Deriv
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-!
# Capitulo 3: analise leve (Lote A2, itens 1, 2 e 3 do `PLANO_LIVRO_A.md`)

Fonte: `unified_quantum_gravity_book/chap03_pascal_simplex_continuous_multinomials.tex`.
Reaproveita `LeanReal.Chap03Pascal` (`cbinom`, `cbinom_real_pos`).

## Item 1. Teorema "Alternating Row Integrals" (sem rotulo)

> For all `x > 0`, `A(x) := ∫_0^x cos(πy) binom(x,y) dy`. If `x = 2k+1` (`k ∈ ℕ₀`) is an odd
> integer, then `A(x) = 0`.

Formalizacao: `alternating_row_integral`, completa (`binom` real `rbinom`, que coincide com a
restricao de `cbinom` aos reais, `cbinom_ofReal`). A integral e a integral de intervalo de
Mathlib; a prova so usa a substituicao `y ↦ x - y`, a simetria `binom(x,x-y) = binom(x,y)` e
`cos(π(x-y)) = -cos(πy)`. A integrabilidade nao e necessaria para a identidade (em Mathlib a
integral de uma funcao nao integravel vale 0), mas o integrando e continuo
(`rbinom_continuousOn`), e isso e usado no mutante.

## Item 2. Proposicao "Global Meromorphic Extension and Zero Loci", representacao

> `binom(x,y) = -(1/π) · sin(πy) sin(π(x-y)) / sin(πx) · Γ(y-x)Γ(-y)/Γ(-x)`.

O livro nao diz onde a igualdade vale literalmente; ele observa que nos inteiros os zeros dos
senos sao "removidos" por polos dos Gamma (isto e, a formula vale como extensao por
continuidade). Formaliza-se a igualdade literal para `x, y, x - y ∉ ℤ` (`reflection`), via
`Complex.Gamma_mul_Gamma_one_sub`. A positividade e os zeros ja estao em `Chap03Pascal`; a
extensao meromorfa em `ℂ²` fica fora.

## Item 3. Corolario `cor:row_log_product`

> For real `x ≥ 0`, `E(x) := ∫_0^x ln binom(x,y) dy` equals
> `x(x+1) - x ln(2π) - x lnΓ(x+1) + 2 ln G(x+1)`, using Alexeiewsky's theorem
> `∫_0^x lnΓ(y+1) dy = x lnΓ(x+1) - ln G(x+1) + (x/2) ln(2π) - x(x+1)/2` (eq:alexeiewsky).

Mathlib nao tem a funcao `G` de Barnes. Formaliza-se:
* `E_reduction` (incondicional): `E(x) = x lnΓ(x+1) - 2∫_0^x lnΓ(y+1) dy`, a primeira linha da
  prova do livro;
* `row_log_product` (CONDICIONAL): a formula final para uma funcao `G : ℝ → ℝ` qualquer que
  satisfaca a identidade de Alexeiewsky no ponto `x` (hipotese nomeada `hAlex`). Nao se prova
  que a `G` de Barnes satisfaz `hAlex`; isso e o teorema classico citado.
* `G_witness`: uma `G` explicita que satisfaz `hAlex` para todo `x ≥ 0` e `G(1) = 1`, o que
  mostra que a hipotese e satisfazivel (nao que essa `G` seja a de Barnes).
-/

noncomputable section

namespace LeanReal.Chap03Analysis

open Real Set intervalIntegral

/-- Coeficiente binomial continuo real: `binom(x,y) = Γ(x+1)·(1/Γ)(y+1)·(1/Γ)(x-y+1)`. -/
def rbinom (x y : ℝ) : ℝ :=
  Real.Gamma (x + 1) * (Real.Gamma (y + 1))⁻¹ * (Real.Gamma (x - y + 1))⁻¹

/-- `rbinom` e a restricao de `LeanReal.Chap03.cbinom` aos argumentos reais. -/
theorem cbinom_ofReal (x y : ℝ) :
    LeanReal.Chap03.cbinom (x : ℂ) (y : ℂ) = ((rbinom x y : ℝ) : ℂ) := by
  unfold LeanReal.Chap03.cbinom rbinom
  have e1 : (x : ℂ) + 1 = ((x + 1 : ℝ) : ℂ) := by push_cast; ring
  have e2 : (y : ℂ) + 1 = ((y + 1 : ℝ) : ℂ) := by push_cast; ring
  have e3 : (x : ℂ) - y + 1 = ((x - y + 1 : ℝ) : ℂ) := by push_cast; ring
  rw [e1, e2, e3, Complex.Gamma_ofReal, Complex.Gamma_ofReal, Complex.Gamma_ofReal]
  push_cast
  ring

/-- Simetria `binom(x, x-y) = binom(x, y)`. -/
theorem rbinom_symm (x y : ℝ) : rbinom x (x - y) = rbinom x y := by
  unfold rbinom
  rw [show x - (x - y) + 1 = y + 1 by ring]
  ring

/-- Positividade em `[0,x]` (de `LeanReal.Chap03.cbinom_real_pos`). -/
theorem rbinom_pos {x y : ℝ} (hx : 0 < x) (hy0 : 0 ≤ y) (hyx : y ≤ x) : 0 < rbinom x y :=
  LeanReal.Chap03.cbinom_real_pos x y hx hy0 hyx

/-- `Γ` e continua em todo `s > 0`. -/
theorem continuousAt_Gamma_of_pos {s : ℝ} (hs : 0 < s) : ContinuousAt Real.Gamma s :=
  (Real.differentiableAt_Gamma fun m hm => by
    have : (0 : ℝ) ≤ m := m.cast_nonneg
    linarith).continuousAt

/-- `y ↦ binom(x,y)` e continua em `[0,x]` (para `x ≥ 0`). -/
theorem rbinom_continuousOn {x : ℝ} : ContinuousOn (rbinom x) (Icc 0 x) := by
  intro y hy
  apply ContinuousAt.continuousWithinAt
  have hp1 : 0 < y + 1 := by linarith [hy.1]
  have hp2 : 0 < x - y + 1 := by linarith [hy.2]
  have h1 : ContinuousAt (fun t : ℝ => Real.Gamma (t + 1)) y :=
    (continuousAt_Gamma_of_pos hp1).comp (f := fun t : ℝ => t + 1) (by fun_prop : ContinuousAt (fun t : ℝ => t + 1) y)
  have h2 : ContinuousAt (fun t : ℝ => Real.Gamma (x - t + 1)) y :=
    (continuousAt_Gamma_of_pos hp2).comp (f := fun t : ℝ => x - t + 1)
      (by fun_prop : ContinuousAt (fun t : ℝ => x - t + 1) y)
  exact (continuousAt_const.mul (h1.inv₀ (Real.Gamma_pos_of_pos hp1).ne')).mul
    (h2.inv₀ (Real.Gamma_pos_of_pos hp2).ne')

/-! ## Item 1: Alternating Row Integrals -/

/-- Integral alternada de linha `A(x) = ∫_0^x cos(πy) binom(x,y) dy`. -/
def altRow (x : ℝ) : ℝ := ∫ y in (0 : ℝ)..x, cos (π * y) * rbinom x y

/-- `cos(π(x-y)) = -cos(πy)` para `x = 2k+1`. -/
theorem cos_odd_reflect (k : ℕ) (y : ℝ) :
    cos (π * ((2 * k + 1 : ℝ) - y)) = -cos (π * y) := by
  have : π * ((2 * k + 1 : ℝ) - y) = (π - π * y) + (k : ℝ) * (2 * π) := by ring
  rw [this, cos_add_nat_mul_two_pi, cos_pi_sub]

/-- **Teorema "Alternating Row Integrals"** (cap. 3): `A(2k+1) = 0` para todo `k ∈ ℕ₀`. -/
theorem alternating_row_integral (k : ℕ) : altRow (2 * k + 1) = 0 := by
  set x : ℝ := 2 * k + 1 with hxdef
  set f : ℝ → ℝ := fun y => cos (π * y) * rbinom x y with hf
  have key : (fun y => f (x - y)) = fun y => -f y := by
    funext y
    simp only [hf]
    rw [hxdef, cos_odd_reflect, ← hxdef, rbinom_symm]
    ring
  have h := intervalIntegral.integral_comp_sub_left f (a := 0) (b := x) x
  simp only [sub_self, sub_zero] at h
  rw [key, intervalIntegral.integral_neg] at h
  have : altRow x = ∫ y in (0 : ℝ)..x, f y := rfl
  linarith

/-- Integral parcial positiva: para `0 < b ≤ x` e `b ≤ 1/2`,
`∫_0^b cos(πy) binom(x,y) dy > 0` (o integrando e positivo em `(0,b)`). -/
theorem partial_pos {x b : ℝ} (hb0 : 0 < b) (hbx : b ≤ x) (hb : b ≤ 1 / 2) :
    0 < ∫ y in (0 : ℝ)..b, cos (π * y) * rbinom x y := by
  have hx : 0 < x := lt_of_lt_of_le hb0 hbx
  apply intervalIntegral.intervalIntegral_pos_of_pos_on _ _ hb0
  · apply ContinuousOn.intervalIntegrable
    rw [uIcc_of_le hb0.le]
    exact (continuous_cos.comp (continuous_const.mul continuous_id)).continuousOn.mul
      (rbinom_continuousOn.mono (Icc_subset_Icc le_rfl hbx))
  · intro y hy
    apply mul_pos
    · apply cos_pos_of_mem_Ioo
      constructor
      · nlinarith [pi_pos, hy.1]
      · nlinarith [pi_pos, hy.2]
    · exact rbinom_pos hx hy.1.le (hy.2.le.trans hbx)

/-- Testemunha nao degenerada (`k = 0`, `x = 1`): `A(1) = 0`, embora a metade
`∫_0^{1/2} cos(πy) binom(1,y) dy` seja estritamente positiva; ha cancelamento real. -/
theorem witness_alternating :
    altRow 1 = 0 ∧ 0 < ∫ y in (0 : ℝ)..(1 / 2), cos (π * y) * rbinom 1 y := by
  refine ⟨?_, partial_pos (by norm_num) (by norm_num) le_rfl⟩
  have := alternating_row_integral 0
  simpa using this

/-- Mutante (sem a hipotese "x impar"): `A(x) = 0` para todo `x > 0` e FALSO; `A(1/2) > 0`. -/
theorem mutant_all_x_false : ¬ (∀ x : ℝ, 0 < x → altRow x = 0) := by
  intro h
  have hpos : 0 < altRow (1 / 2) := partial_pos (by norm_num) le_rfl le_rfl
  rw [h (1 / 2) (by norm_num)] at hpos
  exact lt_irrefl 0 hpos

/-- Mutante (paridade trocada, `x = 2k`): o passo-chave `cos(π(x-y)) = -cos(πy)` falha para
`x = 2`, `y = 0`. -/
theorem mutant_even_reflect_false :
    ¬ (∀ y : ℝ, cos (π * ((2 : ℝ) - y)) = -cos (π * y)) := by
  intro h
  have := h 0
  have e : π * ((2 : ℝ) - 0) = (0 : ℝ) + ((1 : ℕ) : ℝ) * (2 * π) := by push_cast; ring
  rw [e, cos_add_nat_mul_two_pi, mul_zero, cos_zero] at this
  norm_num at this

/-! ## Item 2: representacao por reflexao -/

open Complex in
/-- `sin(πz) ≠ 0` para `z ∉ ℤ`. -/
theorem sin_pi_mul_ne_zero {z : ℂ} (hz : ∀ n : ℤ, z ≠ n) : Complex.sin (π * z) ≠ 0 := by
  intro h
  rw [Complex.sin_eq_zero_iff] at h
  obtain ⟨k, hk⟩ := h
  apply hz k
  have hpi : (π : ℂ) ≠ 0 := Complex.ofReal_ne_zero.mpr Real.pi_ne_zero
  have : (π : ℂ) * z = π * k := by rw [hk]; ring
  exact mul_left_cancel₀ hpi this

/-- `Γ(z) ≠ 0` para `z ∉ ℤ`. -/
theorem Gamma_ne_zero_of_not_int {z : ℂ} (hz : ∀ n : ℤ, z ≠ n) : Complex.Gamma z ≠ 0 :=
  Complex.Gamma_ne_zero fun m hm => hz (-(m : ℤ)) (by rw [hm]; push_cast; ring)

/-- **Proposicao "Global Meromorphic Extension and Zero Loci"** (cap. 3), representacao por
reflexao, literal para `x, y, x - y ∉ ℤ`:
`binom(x,y) = -(1/π)·(sin(πy) sin(π(x-y))/sin(πx))·(Γ(y-x)Γ(-y)/Γ(-x))`. -/
theorem reflection (x y : ℂ) (hx : ∀ n : ℤ, x ≠ n) (hy : ∀ n : ℤ, y ≠ n)
    (hxy : ∀ n : ℤ, x - y ≠ n) :
    LeanReal.Chap03.cbinom x y =
      -(1 / (π : ℂ)) * (Complex.sin (π * y) * Complex.sin (π * (x - y)) / Complex.sin (π * x)) *
        (Complex.Gamma (y - x) * Complex.Gamma (-y) / Complex.Gamma (-x)) := by
  have neg_not : ∀ {z : ℂ}, (∀ n : ℤ, z ≠ n) → ∀ n : ℤ, -z ≠ n := fun hz n h =>
    hz (-n) (by push_cast; linear_combination -h)
  have add1_not : ∀ {z : ℂ}, (∀ n : ℤ, z ≠ n) → ∀ n : ℤ, z + 1 ≠ n := fun hz n h =>
    hz (n - 1) (by push_cast; rw [← h]; ring)
  have hpi : (π : ℂ) ≠ 0 := Complex.ofReal_ne_zero.mpr Real.pi_ne_zero
  have sx := sin_pi_mul_ne_zero hx
  have sy := sin_pi_mul_ne_zero hy
  have sxy := sin_pi_mul_ne_zero hxy
  have gx := Gamma_ne_zero_of_not_int (neg_not hx)
  have gy := Gamma_ne_zero_of_not_int (neg_not hy)
  have gyx : Complex.Gamma (y - x) ≠ 0 := by
    have := Gamma_ne_zero_of_not_int (neg_not hxy)
    rwa [neg_sub] at this
  have gy1 := Gamma_ne_zero_of_not_int (add1_not hy)
  have gxy1 := Gamma_ne_zero_of_not_int (add1_not hxy)
  -- as tres reflexoes
  have r1 : Complex.Gamma (-x) * Complex.Gamma (x + 1) = π / (-Complex.sin (π * x)) := by
    have := Complex.Gamma_mul_Gamma_one_sub (-x)
    rwa [show (1 : ℂ) - -x = x + 1 by ring, mul_neg, Complex.sin_neg] at this
  have r2 : Complex.Gamma (-y) * Complex.Gamma (y + 1) = π / (-Complex.sin (π * y)) := by
    have := Complex.Gamma_mul_Gamma_one_sub (-y)
    rwa [show (1 : ℂ) - -y = y + 1 by ring, mul_neg, Complex.sin_neg] at this
  have r3 : Complex.Gamma (y - x) * Complex.Gamma (x - y + 1) =
      π / (-Complex.sin (π * (x - y))) := by
    have := Complex.Gamma_mul_Gamma_one_sub (y - x)
    rwa [show (1 : ℂ) - (y - x) = x - y + 1 by ring, show (π : ℂ) * (y - x) = -(π * (x - y)) by
      ring, Complex.sin_neg] at this
  have ex : Complex.Gamma (x + 1) = π / (-Complex.sin (π * x)) / Complex.Gamma (-x) := by
    rw [← r1]; field_simp
  have ey : (Complex.Gamma (y + 1))⁻¹ = Complex.Gamma (-y) * (-Complex.sin (π * y)) / π := by
    rw [inv_eq_iff_eq_inv, ← mul_right_inj' gy, r2]
    field_simp
  have exy : (Complex.Gamma (x - y + 1))⁻¹ =
      Complex.Gamma (y - x) * (-Complex.sin (π * (x - y))) / π := by
    rw [inv_eq_iff_eq_inv, ← mul_right_inj' gyx, r3]
    field_simp
  unfold LeanReal.Chap03.cbinom
  rw [ex, ey, exy]
  field_simp

/-- `1/2 ∉ ℤ` em `ℂ`. -/
theorem half_not_int : ∀ n : ℤ, (1 / 2 : ℂ) ≠ n := by
  intro n h
  have h2 := congrArg Complex.re h
  simp at h2
  have h3 : (2 * n : ℝ) = 1 := by rw [← h2]; ring
  have h4 : (2 * n : ℤ) = 1 := by exact_mod_cast h3
  omega

/-- `1/4 ∉ ℤ` em `ℂ`. -/
theorem quarter_not_int : ∀ n : ℤ, (1 / 4 : ℂ) ≠ n := by
  intro n h
  have h2 := congrArg Complex.re h
  simp at h2
  have h3 : (4 * n : ℝ) = 1 := by rw [← h2]; ring
  have h4 : (4 * n : ℤ) = 1 := by exact_mod_cast h3
  omega

/-- Testemunha: `x = 1/2`, `y = 1/4` satisfazem as tres hipoteses e o coeficiente nao e nulo,
logo a identidade compara duas quantidades nao nulas. -/
theorem witness_reflection :
    (∀ n : ℤ, (1 / 2 : ℂ) ≠ n) ∧ (∀ n : ℤ, (1 / 4 : ℂ) ≠ n) ∧
      (∀ n : ℤ, (1 / 2 : ℂ) - 1 / 4 ≠ n) ∧ LeanReal.Chap03.cbinom (1 / 2) (1 / 4) ≠ 0 := by
  have h14 : (1 / 2 : ℂ) - 1 / 4 = 1 / 4 := by norm_num
  refine ⟨half_not_int, quarter_not_int, by rw [h14]; exact quarter_not_int, ?_⟩
  have := cbinom_ofReal (1 / 2) (1 / 4)
  push_cast at this
  rw [this, Complex.ofReal_ne_zero]
  exact (rbinom_pos (by norm_num) (by norm_num) (by norm_num)).ne'

/-- Mutante (sem `y ∉ ℤ`): falso em `x = 1/2`, `y = 0`, onde `binom = 1` e o lado direito
vale `0` (`sin 0 = 0`): os zeros do seno nao sao "removidos" na igualdade literal. -/
theorem mutant_no_y_false :
    ¬ (∀ x y : ℂ, (∀ n : ℤ, x ≠ n) → (∀ n : ℤ, x - y ≠ n) →
      LeanReal.Chap03.cbinom x y =
        -(1 / (π : ℂ)) * (Complex.sin (π * y) * Complex.sin (π * (x - y)) /
          Complex.sin (π * x)) * (Complex.Gamma (y - x) * Complex.Gamma (-y) /
            Complex.Gamma (-x))) := by
  intro h
  have := h (1 / 2) 0 half_not_int (by rw [sub_zero]; exact half_not_int)
  rw [mul_zero, Complex.sin_zero, zero_mul, zero_div, mul_zero, zero_mul] at this
  have hc := cbinom_ofReal (1 / 2) 0
  push_cast at hc
  rw [hc, Complex.ofReal_eq_zero] at this
  exact (rbinom_pos (by norm_num) le_rfl (by norm_num)).ne' this

/-- Mutante (sem `x ∉ ℤ`): falso em `x = 1`, `y = 1/2` (`sin π = 0` no denominador). -/
theorem mutant_no_x_false :
    ¬ (∀ x y : ℂ, (∀ n : ℤ, y ≠ n) → (∀ n : ℤ, x - y ≠ n) →
      LeanReal.Chap03.cbinom x y =
        -(1 / (π : ℂ)) * (Complex.sin (π * y) * Complex.sin (π * (x - y)) /
          Complex.sin (π * x)) * (Complex.Gamma (y - x) * Complex.Gamma (-y) /
            Complex.Gamma (-x))) := by
  intro h
  have h12 : (1 : ℂ) - 1 / 2 = 1 / 2 := by norm_num
  have := h 1 (1 / 2) half_not_int (by rw [h12]; exact half_not_int)
  rw [mul_one, Complex.sin_pi, div_zero, mul_zero, zero_mul] at this
  have hc := cbinom_ofReal 1 (1 / 2)
  push_cast at hc
  rw [hc, Complex.ofReal_eq_zero] at this
  exact (rbinom_pos (by norm_num) (by norm_num) (by norm_num)).ne' this

/-! ## Item 3: `cor:row_log_product` -/

/-- Entropia de linha continua `E(x) = ∫_0^x ln binom(x,y) dy`. -/
def rowEntropy (x : ℝ) : ℝ := ∫ y in (0 : ℝ)..x, Real.log (rbinom x y)

/-- `t ↦ ln Γ(t+1)` e continua em `[0, ∞)`. -/
theorem logGamma_continuousOn : ContinuousOn (fun t : ℝ => Real.log (Real.Gamma (t + 1)))
    (Ici 0) := by
  intro t ht
  have hp : 0 < t + 1 := by linarith [mem_Ici.mp ht]
  apply ContinuousAt.continuousWithinAt
  exact ((continuousAt_Gamma_of_pos hp).comp (f := fun s : ℝ => s + 1)
    (by fun_prop : ContinuousAt (fun s : ℝ => s + 1) t)).log (Real.Gamma_pos_of_pos hp).ne'

/-- **Reducao de `cor:row_log_product`** (incondicional), primeira linha da prova do livro:
`E(x) = x lnΓ(x+1) - 2 ∫_0^x lnΓ(y+1) dy` para `x ≥ 0`. -/
theorem E_reduction (x : ℝ) (hx : 0 ≤ x) :
    rowEntropy x =
      x * Real.log (Real.Gamma (x + 1)) - 2 * ∫ y in (0 : ℝ)..x, Real.log (Real.Gamma (y + 1)) := by
  set g : ℝ → ℝ := fun t => Real.log (Real.Gamma (t + 1)) with hg
  have hgc : ContinuousOn g (Icc 0 x) := logGamma_continuousOn.mono Icc_subset_Ici_self
  have hgr : ContinuousOn (fun y => g (x - y)) (Icc 0 x) := by
    refine hgc.comp (by fun_prop) ?_
    intro y hy
    exact ⟨by linarith [hy.2], by linarith [hy.1]⟩
  have hI1 : IntervalIntegrable g MeasureTheory.volume 0 x :=
    (by rwa [uIcc_of_le hx] : ContinuousOn g (uIcc 0 x)).intervalIntegrable
  have hI2 : IntervalIntegrable (fun y => g (x - y)) MeasureTheory.volume 0 x :=
    (by rwa [uIcc_of_le hx] : ContinuousOn (fun y => g (x - y)) (uIcc 0 x)).intervalIntegrable
  have hcongr : EqOn (fun y => Real.log (rbinom x y)) (fun y => (g x - g y) - g (x - y))
      (uIcc 0 x) := by
    intro y hy
    rw [uIcc_of_le hx] at hy
    have p1 := Real.Gamma_pos_of_pos (show 0 < x + 1 by linarith)
    have p2 := Real.Gamma_pos_of_pos (show 0 < y + 1 by linarith [hy.1])
    have p3 := Real.Gamma_pos_of_pos (show 0 < x - y + 1 by linarith [hy.2])
    simp only [hg, rbinom]
    rw [Real.log_mul (by positivity) (by positivity), Real.log_mul p1.ne' (by positivity),
      Real.log_inv, Real.log_inv]
    ring
  have hsub := intervalIntegral.integral_comp_sub_left g (a := 0) (b := x) x
  simp only [sub_self, sub_zero] at hsub
  unfold rowEntropy
  rw [intervalIntegral.integral_congr hcongr, intervalIntegral.integral_sub _ hI2,
    intervalIntegral.integral_sub intervalIntegrable_const hI1, intervalIntegral.integral_const,
    hsub]
  · simp only [hg, smul_eq_mul, sub_zero]
    ring
  · exact intervalIntegrable_const.sub hI1

/-- **Corolario `cor:row_log_product`** (CONDICIONAL): se `G : ℝ → ℝ` satisfaz a identidade de
Alexeiewsky (eq:alexeiewsky) no ponto `x ≥ 0` (hipotese `hAlex`), entao
`E(x) = x(x+1) - x ln(2π) - x lnΓ(x+1) + 2 ln G(x+1)`. -/
theorem row_log_product (G : ℝ → ℝ) (x : ℝ) (hx : 0 ≤ x)
    (hAlex : ∫ y in (0 : ℝ)..x, Real.log (Real.Gamma (y + 1)) =
      x * Real.log (Real.Gamma (x + 1)) - Real.log (G (x + 1)) + x / 2 * Real.log (2 * π) -
        x * (x + 1) / 2) :
    rowEntropy x = x * (x + 1) - x * Real.log (2 * π) - x * Real.log (Real.Gamma (x + 1)) +
      2 * Real.log (G (x + 1)) := by
  rw [E_reduction x hx, hAlex]
  ring

/-- Uma `G` explicita que satisfaz a hipotese de Alexeiewsky em todo `x ≥ 0` (definida para
isso; NAO e a `G` de Barnes, que Mathlib nao tem). -/
def Gw (t : ℝ) : ℝ :=
  Real.exp ((t - 1) * Real.log (Real.Gamma t) -
    (∫ y in (0 : ℝ)..(t - 1), Real.log (Real.Gamma (y + 1))) + (t - 1) / 2 * Real.log (2 * π) -
      (t - 1) * t / 2)

/-- Testemunha de satisfazibilidade de `hAlex`: `Gw` satisfaz a identidade para todo `x`, e
`Gw(1) = 1` (a normalizacao `G(1) = 1` de Barnes). -/
theorem G_witness :
    (∀ x : ℝ, ∫ y in (0 : ℝ)..x, Real.log (Real.Gamma (y + 1)) =
      x * Real.log (Real.Gamma (x + 1)) - Real.log (Gw (x + 1)) + x / 2 * Real.log (2 * π) -
        x * (x + 1) / 2) ∧ Gw 1 = 1 := by
  refine ⟨fun x => ?_, ?_⟩
  · unfold Gw
    rw [Real.log_exp, add_sub_cancel_right]
    ring
  · unfold Gw
    simp

/-- Aplicacao a testemunha em `x = 2` (as hipoteses de `row_log_product` sao satisfeitas). -/
theorem witness_row_log_product :
    rowEntropy 2 = 2 * (2 + 1) - 2 * Real.log (2 * π) - 2 * Real.log (Real.Gamma (2 + 1)) +
      2 * Real.log (Gw (2 + 1)) :=
  row_log_product Gw 2 (by norm_num) (G_witness.1 2)

/-- `Γ(3) = 2`. -/
theorem Gamma_three : Real.Gamma 3 = 2 := by
  rw [show (3 : ℝ) = 2 + 1 by norm_num, Real.Gamma_add_one (by norm_num), Real.Gamma_two]
  norm_num

/-- Mutante da reducao (coeficiente `2x lnΓ(x+1)` em vez de `x lnΓ(x+1)`): falso em `x = 2`,
porque `2 lnΓ(3) = 2 ln 2 ≠ 0`. -/
theorem mutant_reduction_coeff_false :
    ¬ (∀ x : ℝ, 0 ≤ x → rowEntropy x = 2 * x * Real.log (Real.Gamma (x + 1)) -
      2 * ∫ y in (0 : ℝ)..x, Real.log (Real.Gamma (y + 1))) := by
  intro h
  have h1 := h 2 (by norm_num)
  rw [E_reduction 2 (by norm_num)] at h1
  have h3 : Real.Gamma (2 + 1) = 2 := by rw [show (2 : ℝ) + 1 = 3 by norm_num, Gamma_three]
  rw [h3] at h1
  have : 0 < Real.log 2 := Real.log_pos one_lt_two
  linarith

/-- Mutante do corolario (`x(x-1)` em vez de `x(x+1)`): falso, pela testemunha `Gw` em `x = 1`
(daria `2 = 0`). -/
theorem mutant_corollary_false :
    ¬ (∀ (G : ℝ → ℝ) (x : ℝ), 0 ≤ x →
      (∫ y in (0 : ℝ)..x, Real.log (Real.Gamma (y + 1)) =
        x * Real.log (Real.Gamma (x + 1)) - Real.log (G (x + 1)) + x / 2 * Real.log (2 * π) -
          x * (x + 1) / 2) →
      rowEntropy x = x * (x - 1) - x * Real.log (2 * π) - x * Real.log (Real.Gamma (x + 1)) +
        2 * Real.log (G (x + 1))) := by
  intro h
  have hm := h Gw 1 (by norm_num) (G_witness.1 1)
  have ht := row_log_product Gw 1 (by norm_num) (G_witness.1 1)
  rw [ht] at hm
  norm_num at hm

end LeanReal.Chap03Analysis

#print axioms LeanReal.Chap03Analysis.cbinom_ofReal
#print axioms LeanReal.Chap03Analysis.rbinom_symm
#print axioms LeanReal.Chap03Analysis.rbinom_continuousOn
#print axioms LeanReal.Chap03Analysis.alternating_row_integral
#print axioms LeanReal.Chap03Analysis.partial_pos
#print axioms LeanReal.Chap03Analysis.witness_alternating
#print axioms LeanReal.Chap03Analysis.mutant_all_x_false
#print axioms LeanReal.Chap03Analysis.mutant_even_reflect_false
#print axioms LeanReal.Chap03Analysis.reflection
#print axioms LeanReal.Chap03Analysis.witness_reflection
#print axioms LeanReal.Chap03Analysis.mutant_no_y_false
#print axioms LeanReal.Chap03Analysis.mutant_no_x_false
#print axioms LeanReal.Chap03Analysis.E_reduction
#print axioms LeanReal.Chap03Analysis.row_log_product
#print axioms LeanReal.Chap03Analysis.G_witness
#print axioms LeanReal.Chap03Analysis.witness_row_log_product
#print axioms LeanReal.Chap03Analysis.mutant_reduction_coeff_false
#print axioms LeanReal.Chap03Analysis.mutant_corollary_false
