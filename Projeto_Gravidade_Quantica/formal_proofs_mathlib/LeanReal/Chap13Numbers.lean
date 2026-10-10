import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.Real.Pi.Bounds
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

/-!
# Capitulo 13: contas exatas e numeros fisicos (lote LIVRO B3, itens r2 e r4)

Fonte: `unified_quantum_gravity_book/chap13_experimental_observational_signatures_quantum_gravity.tex`.
O capitulo nao tem teoremas; formalizamos as contas exatas e alguns numeros fisicos.

## r2, eq. `ds_tau`

> `P(τ) = (1/(32π²ℓ²τ)) [1 - √π z e^{z²} erfc z]`, `z = √τ/(2ℓ)`, e
> `d_s(τ) := -2 d ln P / d ln τ = 1 - τ/(2ℓ²) + [1 - (√(πτ)/(2ℓ)) e^{τ/4ℓ²} erfc(√τ/(2ℓ))]^{-1}`.

**Coberto.** (a) Forma do plano: se `P(σ) = C σ⁻¹ (1 - g(√σ/(2ℓ)))` e `g' = g/z + 2zg - 2z` em `z`,
entao `d_s = 1 - 2z² + 1/(1-g)` com `2z² = τ/(2ℓ²)` (`ds_formula_of_ode`). (b) A EDO NAO fica como
hipotese: `erfc` e definida pela formula padrao `erfc z = 1 - (2/√π) ∫₀^z e^{-t²} dt` e a EDO de
`g(z) = √π z e^{z²} erfc z` e provada (`g_ode`); daqui a eq. `ds_tau` na forma exata do livro para
a forma fechada de `P` (`ds_tau`). Hipotese restante: o colchete `1 - g(z)` e nao nulo (de fato e
positivo para `z > 0`, mas isso exige a cota de Mills e nao e provado; a testemunha o verifica em
`z = 1/8`). **Nao coberto:** a igualdade da forma fechada com a integral `∫ u e^{-τu-τℓ²u²} du`
(eq. `heat_kernel_exact`, item r1) e os limites `d_s → 2, 4` (r3).

## r4, eq. `tensor_running`

> `α_t = ½(d_s(p) - 4) = -(p/M_*)²/(1+(p/M_*)²)` com `d_s(p) = 2 + 2/(1+(p/M_*)²)`.

## Numeros fisicos (unidades naturais `ħ = c = 1` quando se fala em GeV)

Constantes usadas (CODATA 2018): `M_P c² = 1.22089 × 10¹⁹ GeV`, `ℓ_P = 1.616255 × 10⁻³⁵ m`,
`ħc = 1.973269804 × 10⁻¹⁶ GeV·m = 1.973269804 × 10⁻⁷ eV·m`, `m_P = 2.176434 × 10⁻⁸ kg`,
`c = 299792458 m/s`, `u = 1.66053906660 × 10⁻²⁷ kg`, `m(⁸⁷Sr) = 86.9088775 u`.
Os valores entram como hipoteses de igualdade nomeadas, para que a dependencia fique visivel.
-/

noncomputable section

namespace LeanReal.Chap13Numbers

open Real Set

/-! ## r2: a dimensao espectral do nucleo de duas escalas -/

/-- Funcao erro complementar, pela definicao padrao `erfc z = 1 - (2/√π) ∫₀^z e^{-t²} dt`
(a Mathlib nao tem `erfc`). -/
def erfc (z : ℝ) : ℝ := 1 - 2 / √π * ∫ t in (0:ℝ)..z, exp (-t ^ 2)

theorem hasDerivAt_erfc (z : ℝ) : HasDerivAt erfc (-(2 / √π) * exp (-z ^ 2)) z := by
  have hc : Continuous fun t : ℝ => exp (-t ^ 2) := by fun_prop
  have := ((hc.integral_hasStrictDerivAt 0 z).hasDerivAt.const_mul (2 / √π)).const_sub 1
  show HasDerivAt (fun z => 1 - 2 / √π * ∫ t in (0:ℝ)..z, exp (-t ^ 2)) _ z
  convert this using 1
  ring

/-- `g(z) = √π z e^{z²} erfc z`, o termo do colchete de `heat_kernel_exact`. -/
def gFun (z : ℝ) : ℝ := √π * z * exp (z ^ 2) * erfc z

/-- EDO de `g`: `g'(z) = g(z)/z + 2z g(z) - 2z` para `z ≠ 0` (usada na derivacao de `ds_tau`). -/
theorem g_ode {z : ℝ} (hz : z ≠ 0) :
    HasDerivAt gFun (gFun z / z + 2 * z * gFun z - 2 * z) z := by
  have hpi : √π ≠ 0 := (Real.sqrt_pos.2 pi_pos).ne'
  have h1 : HasDerivAt (fun z => √π * z) (√π) z := by
    simpa using (hasDerivAt_id z).const_mul √π
  have h2 : HasDerivAt (fun z : ℝ => exp (z ^ 2)) (exp (z ^ 2) * (2 * z)) z := by
    have := (hasDerivAt_pow 2 z).exp
    convert this using 1; simp
  have h : HasDerivAt (fun z => √π * z * exp (z ^ 2) * erfc z)
      ((√π * exp (z ^ 2) + √π * z * (exp (z ^ 2) * (2 * z))) * erfc z +
        √π * z * exp (z ^ 2) * (-(2 / √π) * exp (-z ^ 2))) z :=
    (h1.mul h2).mul (hasDerivAt_erfc z)
  refine h.congr_deriv ?_
  unfold gFun
  have hee : exp (z ^ 2) * exp (-z ^ 2) = 1 := by rw [← exp_add]; simp
  have e1 : √π * z * exp (z ^ 2) * erfc z / z = √π * exp (z ^ 2) * erfc z := by
    field_simp
  have e2 : √π * z * exp (z ^ 2) * (-(2 / √π) * exp (-z ^ 2)) =
      -2 * z * (exp (z ^ 2) * exp (-z ^ 2)) := by
    field_simp
  rw [e1, e2, hee]
  ring

/-- Dimensao espectral a partir de `P`: `d_s(τ) = -2 · d/ds log P(e^s)` em `s = log τ`. -/
def dsOf (P : ℝ → ℝ) (τ : ℝ) : ℝ := -2 * deriv (fun s => log (P (exp s))) (log τ)

/-- **r2, forma do plano** (eq. `ds_tau`): se `P(σ) = C σ⁻¹ (1 - g(√σ/(2ℓ)))` para `σ > 0` e `g`
satisfaz `g' = g/z + 2zg - 2z` em `z = √τ/(2ℓ)`, com `1 - g(z) ≠ 0`, entao
`d_s(τ) = 1 - τ/(2ℓ²) + 1/(1 - g(z))`. -/
theorem ds_formula_of_ode (P g : ℝ → ℝ) (C ℓ τ : ℝ) (hC : C ≠ 0) (hℓ : 0 < ℓ) (hτ : 0 < τ)
    (hP : ∀ σ, 0 < σ → P σ = C * σ⁻¹ * (1 - g (√σ / (2 * ℓ))))
    (hg : HasDerivAt g (g (√τ / (2 * ℓ)) / (√τ / (2 * ℓ)) + 2 * (√τ / (2 * ℓ)) *
      g (√τ / (2 * ℓ)) - 2 * (√τ / (2 * ℓ))) (√τ / (2 * ℓ)))
    (h1g : 1 - g (√τ / (2 * ℓ)) ≠ 0) :
    dsOf P τ = 1 - τ / (2 * ℓ ^ 2) + (1 - g (√τ / (2 * ℓ)))⁻¹ := by
  set z := √τ / (2 * ℓ) with hzdef
  have hsq : √τ ^ 2 = τ := sq_sqrt hτ.le
  have hzpos : 0 < z := div_pos (Real.sqrt_pos.2 hτ) (by positivity)
  have hz2 : z ^ 2 = τ / (4 * ℓ ^ 2) := by rw [hzdef, div_pow, hsq]; ring
  -- reescrita da funcao em s
  have hfun : (fun s => log (P (exp s))) =
      fun s => log (C * exp (-s) * (1 - g (exp (s / 2) / (2 * ℓ)))) := by
    funext s
    rw [hP _ (exp_pos s), exp_neg, exp_half]
  -- derivadas
  have hzs : HasDerivAt (fun s => exp (s / 2) / (2 * ℓ)) (exp (log τ / 2) * (1 / 2) / (2 * ℓ))
      (log τ) := by
    exact (((hasDerivAt_id' (log τ)).div_const 2).exp).div_const (2 * ℓ)
  have hzval : exp (log τ / 2) / (2 * ℓ) = z := by rw [exp_half, exp_log hτ]
  have hgz : HasDerivAt (fun s => g (exp (s / 2) / (2 * ℓ)))
      ((z⁻¹ * g z + 2 * z * g z - 2 * z) * (z / 2)) (log τ) := by
    have hg' : HasDerivAt g (g z / z + 2 * z * g z - 2 * z) (exp (log τ / 2) / (2 * ℓ)) := by
      rw [hzval]; exact hg
    refine (hg'.comp (log τ) hzs).congr_deriv ?_
    rw [show exp (log τ / 2) * (1 / 2) / (2 * ℓ) = z / 2 by rw [← hzval]; ring]
    ring
  have hE : HasDerivAt (fun s => C * exp (-s)) (C * (exp (-log τ) * (-1))) (log τ) :=
    ((hasDerivAt_neg (log τ)).exp).const_mul C
  have hprod := hE.mul ((hasDerivAt_const (log τ) (1:ℝ)).sub hgz)
  have hval : C * exp (-log τ) * (1 - g (exp (log τ / 2) / (2 * ℓ))) ≠ 0 := by
    rw [hzval]; exact mul_ne_zero (mul_ne_zero hC (exp_pos _).ne') h1g
  have hd := (hprod.log hval).deriv
  simp only [Pi.mul_apply, Pi.sub_apply, hzval] at hd
  unfold dsOf
  rw [hfun, hd]
  have hz0 : z ≠ 0 := hzpos.ne'
  have hexp : exp (-log τ) ≠ 0 := (exp_pos _).ne'
  have hτz : τ / (2 * ℓ ^ 2) = 2 * z ^ 2 := by rw [hz2]; field_simp; ring
  rw [hτz]
  field_simp
  ring

/-- Forma fechada de `heat_kernel_exact`:
`P(σ) = (1/(32π²ℓ²σ)) [1 - √π z e^{z²} erfc z]`, `z = √σ/(2ℓ)`. Unidades: `σ` e `ℓ²` tem a mesma
dimensao (comprimento² com `ħ = c = 1`), `z` e adimensional, `P` tem dimensao comprimento⁻⁴. -/
def Pclosed (ℓ σ : ℝ) : ℝ :=
  1 / (32 * π ^ 2 * ℓ ^ 2 * σ) * (1 - √π * (√σ / (2 * ℓ)) * exp ((√σ / (2 * ℓ)) ^ 2) *
    erfc (√σ / (2 * ℓ)))

/-- **r2, eq. `ds_tau`** na forma exata do livro, para a forma fechada de `P`:
`d_s(τ) = 1 - τ/(2ℓ²) + [1 - (√(πτ)/(2ℓ)) e^{τ/(4ℓ²)} erfc(√τ/(2ℓ))]^{-1}`, para `τ, ℓ > 0` com
o colchete nao nulo. Unidades: `τ/ℓ²` adimensional; `d_s` adimensional. -/
theorem ds_tau (ℓ τ : ℝ) (hℓ : 0 < ℓ) (hτ : 0 < τ)
    (h1 : 1 - √(π * τ) / (2 * ℓ) * exp (τ / (4 * ℓ ^ 2)) * erfc (√τ / (2 * ℓ)) ≠ 0) :
    dsOf (Pclosed ℓ) τ =
      1 - τ / (2 * ℓ ^ 2) + (1 - √(π * τ) / (2 * ℓ) * exp (τ / (4 * ℓ ^ 2)) *
        erfc (√τ / (2 * ℓ)))⁻¹ := by
  have hb : gFun (√τ / (2 * ℓ)) =
      √(π * τ) / (2 * ℓ) * exp (τ / (4 * ℓ ^ 2)) * erfc (√τ / (2 * ℓ)) := by
    unfold gFun
    rw [Real.sqrt_mul pi_pos.le, div_pow, sq_sqrt hτ.le]
    ring_nf
  have hz0 : √τ / (2 * ℓ) ≠ 0 := (div_pos (Real.sqrt_pos.2 hτ) (by positivity)).ne'
  rw [← hb] at h1 ⊢
  refine ds_formula_of_ode (Pclosed ℓ) gFun (1 / (32 * π ^ 2 * ℓ ^ 2)) ℓ τ
    (by positivity) hℓ hτ (fun σ hσ => ?_) (g_ode hz0) h1
  unfold Pclosed gFun
  field_simp

/-- `erfc z ≤ 1` para `z ≥ 0`. -/
theorem erfc_le_one {z : ℝ} (hz : 0 ≤ z) : erfc z ≤ 1 := by
  unfold erfc
  have : 0 ≤ ∫ t in (0:ℝ)..z, exp (-t ^ 2) :=
    intervalIntegral.integral_nonneg hz (fun t _ => (exp_pos _).le)
  have : 0 ≤ 2 / √π * ∫ t in (0:ℝ)..z, exp (-t ^ 2) := by positivity
  linarith

/-- Testemunha nao degenerada de `ds_tau`: em `ℓ = 1`, `τ = 1/16` (`z = 1/8`) o colchete
`1 - g(1/8)` e positivo (`g(1/8) ≤ (√π/8) e^{1/64} < 1/2`), entao a hipotese `h1` vale e
`d_s(1/16) = 1 - 1/32 + 1/(1 - g(1/8))`. -/
theorem witness_ds_tau :
    0 < 1 - gFun (1 / 8) ∧
    dsOf (Pclosed 1) (1 / 16) = 1 - (1 / 16) / (2 * 1 ^ 2) + (1 - gFun (1 / 8))⁻¹ := by
  have hg : gFun (1 / 8) < 1 / 2 := by
    unfold gFun
    have he := erfc_le_one (show (0:ℝ) ≤ 1 / 8 by norm_num)
    have hsq : √π < 2 := by
      rw [show (2:ℝ) = √4 by rw [show (4:ℝ) = 2 ^ 2 by norm_num, sqrt_sq (by norm_num)]]
      exact Real.sqrt_lt_sqrt pi_pos.le (by linarith [pi_lt_d2])
    have hexp : exp ((1 / 8 : ℝ) ^ 2) < 64 / 63 := by
      have := Real.exp_bound_div_one_sub_of_interval' (x := 1 / 64) (by norm_num) (by norm_num)
      norm_num at this ⊢; linarith
    have hpos : 0 ≤ √π * (1 / 8) * exp ((1 / 8 : ℝ) ^ 2) := by positivity
    have hle : √π * (1 / 8) * exp ((1 / 8 : ℝ) ^ 2) * erfc (1 / 8) ≤
        √π * (1 / 8) * exp ((1 / 8 : ℝ) ^ 2) := by
      nlinarith
    have : √π * (1 / 8) * exp ((1 / 8 : ℝ) ^ 2) < 2 * (1 / 8) * (64 / 63) := by
      have := Real.sqrt_nonneg π
      have := exp_pos ((1 / 8 : ℝ) ^ 2)
      nlinarith
    linarith
  have hz : √(1 / 16 : ℝ) / (2 * 1) = 1 / 8 := by
    rw [show (1 / 16 : ℝ) = (1 / 4) ^ 2 by norm_num, sqrt_sq (by norm_num)]; norm_num
  have hpos : 0 < 1 - gFun (1 / 8) := by linarith
  refine ⟨hpos, ?_⟩
  have hb : gFun (√(1 / 16 : ℝ) / (2 * 1)) =
      √(π * (1 / 16)) / (2 * 1) * exp ((1 / 16) / (4 * 1 ^ 2)) * erfc (√(1 / 16) / (2 * 1)) := by
    unfold gFun
    rw [Real.sqrt_mul pi_pos.le, div_pow, sq_sqrt (by norm_num)]
    ring_nf
  have h := ds_tau 1 (1 / 16) one_pos (by norm_num) (by rw [← hb, hz]; exact hpos.ne')
  rw [← hb, hz] at h
  exact h

/-- Mutante 1 (sem a EDO de `g`): falso. Com `g ≡ 0`, `C = ℓ = τ = 1`, `P(σ) = σ⁻¹` tem
`d_s = 2`, mas a formula daria `1 - 1/2 + 1 = 3/2`. -/
theorem mutant_no_ode_false :
    ¬ (∀ (P g : ℝ → ℝ) (C ℓ τ : ℝ), C ≠ 0 → 0 < ℓ → 0 < τ →
        (∀ σ, 0 < σ → P σ = C * σ⁻¹ * (1 - g (√σ / (2 * ℓ)))) →
        1 - g (√τ / (2 * ℓ)) ≠ 0 →
        dsOf P τ = 1 - τ / (2 * ℓ ^ 2) + (1 - g (√τ / (2 * ℓ)))⁻¹) := by
  intro h
  have h1 := h (fun σ => σ⁻¹) (fun _ => 0) 1 1 1 one_ne_zero one_pos one_pos
    (fun σ _ => by ring) (by norm_num)
  have hd : dsOf (fun σ => σ⁻¹) 1 = 2 := by
    unfold dsOf
    have hf : (fun s => log ((exp s)⁻¹)) = fun s => -s := by
      funext s; rw [log_inv, log_exp]
    simp only [hf, log_one, deriv_neg'']
    norm_num
  rw [hd] at h1
  norm_num at h1

/-- Mutante 2 (sinal de `τ/(2ℓ²)` trocado): falso na testemunha. -/
theorem mutant_sign_false :
    ¬ (dsOf (Pclosed 1) (1 / 16) = 1 + (1 / 16) / (2 * 1 ^ 2) + (1 - gFun (1 / 8))⁻¹) := by
  rw [witness_ds_tau.2]
  norm_num

/-! ## r4: `tensor_running` -/

/-- **r4, eq. `tensor_running`**: com `d_s(p) = 2 + 2/(1+x)`, `x = (p/M_*)² ≥ 0`,
`½(d_s(p) - 4) = -x/(1+x)`. Unidades: `p` e `M_*` em GeV, `x` adimensional. -/
theorem tensor_running (x : ℝ) (hx : 0 ≤ x) :
    1 / 2 * ((2 + 2 / (1 + x)) - 4) = -(x / (1 + x)) := by
  have : (1 + x) ≠ 0 := by positivity
  field_simp
  ring

/-- `|α_t| = x/(1+x)` satisfaz `0 ≤ |α_t| ≤ x` e `|α_t| < 1` ("satura em 1"). -/
theorem alpha_t_bounds (x : ℝ) (hx : 0 ≤ x) :
    0 ≤ x / (1 + x) ∧ x / (1 + x) ≤ x ∧ x / (1 + x) < 1 := by
  have h1 : 0 < 1 + x := by linarith
  refine ⟨by positivity, ?_, ?_⟩
  · rw [div_le_iff₀ h1]; nlinarith
  · rw [div_lt_one h1]; linarith

/-- Mutante (`α_t = ½(d_s - 2)`): falso em `x = 1`. -/
theorem mutant_tensor_false :
    ¬ (∀ x : ℝ, 0 ≤ x → 1 / 2 * ((2 + 2 / (1 + x)) - 2) = -(x / (1 + x))) := by
  intro h
  have := h 1 zero_le_one
  norm_num at this

/-! ## Numeros fisicos do capitulo 13 -/

/-- **`H_inf ≤ 4.7 × 10¹³ GeV`** (texto do "Tensor-tilt running"). Unidades naturais
(`ħ = c = 1`): `H_inf` e `M_P` em GeV; `r` e `A_s` adimensionais; a relacao
`2H²/(π² M_red²) = r A_s` e adimensional (GeV²/GeV²). Com `M_P = 1.22089 × 10¹⁹ GeV`,
`A_s = 2.1 × 10⁻⁹`, `r < 0.036` e `M_red = M_P/√(8π)`: `H_inf < 4.71 × 10¹³ GeV`. -/
theorem H_inf_bound (H r As MP : ℝ) (hMP : MP = 1.22089e19) (hAs : As = 2.1e-9)
    (hr : r < 0.036) (hH : 0 < H)
    (hrel : 2 * H ^ 2 / (π ^ 2 * (MP / √(8 * π)) ^ 2) = r * As) :
    H < 4.71e13 := by
  have hpi := pi_pos
  have e : 2 * H ^ 2 / (π ^ 2 * (MP / √(8 * π)) ^ 2) = 16 * H ^ 2 / (π * MP ^ 2) := by
    rw [div_pow, sq_sqrt (by positivity)]
    subst hMP
    field_simp
    ring
  rw [e, div_eq_iff (by subst hMP; positivity)] at hrel
  subst hMP hAs
  have hlt : 16 * H ^ 2 < 0.036 * 2.1e-9 * (3.1416 * 1.22089e19 ^ 2) := by
    rw [hrel]
    have h1 : r * 2.1e-9 * (π * 1.22089e19 ^ 2) < 0.036 * 2.1e-9 * (π * 1.22089e19 ^ 2) := by
      have : 0 < 2.1e-9 * (π * (1.22089e19 : ℝ) ^ 2) := by positivity
      nlinarith
    have h2 : 0.036 * 2.1e-9 * (π * 1.22089e19 ^ 2) <
        0.036 * 2.1e-9 * (3.1416 * (1.22089e19 : ℝ) ^ 2) := by
      have := pi_lt_d4
      nlinarith
    linarith
  by_contra hc
  replace hc := not_lt.1 hc
  nlinarith

/-- Nitidez: em `r = 0.036` (o limite do BICEP/Keck) `H_inf > 4.70 × 10¹³ GeV`; o "≤ 4.7 × 10¹³"
do livro e o arredondamento a dois algarismos de `4.70…`. (Unidades como em `H_inf_bound`.) -/
theorem H_inf_at_bound (H MP : ℝ) (hMP : MP = 1.22089e19) (hH : 0 < H)
    (hrel : 2 * H ^ 2 / (π ^ 2 * (MP / √(8 * π)) ^ 2) = 0.036 * 2.1e-9) :
    4.70e13 < H := by
  have hpi := pi_pos
  have e : 2 * H ^ 2 / (π ^ 2 * (MP / √(8 * π)) ^ 2) = 16 * H ^ 2 / (π * MP ^ 2) := by
    rw [div_pow, sq_sqrt (by positivity)]
    subst hMP
    field_simp
    ring
  rw [e, div_eq_iff (by subst hMP; positivity)] at hrel
  subst hMP
  have h2 : 0.036 * 2.1e-9 * (3.1415 * (1.22089e19 : ℝ) ^ 2) <
      0.036 * 2.1e-9 * (π * 1.22089e19 ^ 2) := by
    have := pi_gt_d4
    nlinarith
  by_contra hc
  replace hc := not_lt.1 hc
  nlinarith

/-- Mutante (a cota com tres algarismos, `H_inf ≤ 4.70 × 10¹³`): falsa em `r = 0.036`. -/
theorem mutant_H_three_digits_false (H MP : ℝ) (hMP : MP = 1.22089e19) (hH : 0 < H)
    (hrel : 2 * H ^ 2 / (π ^ 2 * (MP / √(8 * π)) ^ 2) = 0.036 * 2.1e-9) :
    ¬ (H ≤ 4.70e13) :=
  not_le.2 (H_inf_at_bound H MP hMP hH hrel)

/-- **`|α_t| ≈ (H_inf/M_P)² ≤ 1.5 × 10⁻¹¹`** e **`3.7 × 10⁻¹⁰` para `M_* = M_red`**.
Unidades: `H`, `M_P` em GeV; `x = (H/M_*)²` e `α_t` adimensionais. -/
theorem alpha_t_numbers (H MP : ℝ) (hMP : MP = 1.22089e19) (hH : 0 < H) (hHb : H < 4.71e13) :
    (H / MP) ^ 2 / (1 + (H / MP) ^ 2) < 1.5e-11 ∧
    (H / (MP / √(8 * π))) ^ 2 / (1 + (H / (MP / √(8 * π))) ^ 2) < 3.75e-10 := by
  subst hMP
  have hpi := pi_pos
  have hH2 : H ^ 2 < (4.71e13) ^ 2 := by nlinarith
  have hx1 : (H / 1.22089e19) ^ 2 < 1.5e-11 := by
    rw [div_pow, div_lt_iff₀ (by positivity)]
    nlinarith
  have hx2 : (H / (1.22089e19 / √(8 * π))) ^ 2 < 3.75e-10 := by
    rw [div_pow, div_pow, sq_sqrt (by positivity), div_div_eq_mul_div,
      div_lt_iff₀ (by positivity)]
    have := pi_lt_d4
    nlinarith
  exact ⟨lt_of_le_of_lt (alpha_t_bounds _ (sq_nonneg _)).2.1 hx1,
    lt_of_le_of_lt (alpha_t_bounds _ (sq_nonneg _)).2.1 hx2⟩

/-- Janela `4.1 × 10¹⁴ ≤ M_*` GeV: `|α_t| < 0.014` ("no maximo da ordem de `10⁻²`").
Unidades: `H`, `M_*` em GeV; `α_t` adimensional. -/
theorem alpha_t_window (H M : ℝ) (hH : 0 < H) (hHb : H < 4.71e13) (hM : 4.1e14 ≤ M) :
    (H / M) ^ 2 / (1 + (H / M) ^ 2) < 0.014 := by
  have hMpos : 0 < M := by linarith
  have hx : (H / M) ^ 2 < 0.014 := by
    rw [div_pow, div_lt_iff₀ (by positivity)]
    have : (4.1e14 : ℝ) ^ 2 ≤ M ^ 2 := by nlinarith
    nlinarith
  exact lt_of_le_of_lt (alpha_t_bounds _ (sq_nonneg _)).2.1 hx

/-- Mutante (`|α_t| < 1.4 × 10⁻¹¹` para todo `H < 4.71 × 10¹³`): falso em `H = 4.70 × 10¹³`. -/
theorem mutant_alpha_false :
    ¬ (∀ H : ℝ, 0 < H → H < 4.71e13 → (H / 1.22089e19) ^ 2 < 1.4e-11) := by
  intro h
  have := h 4.70e13 (by norm_num) (by norm_num)
  norm_num at this

/-- Escalas do texto "Graviton dispersion". Unidades: energias em GeV, comprimentos em m,
tempos em s; razoes adimensionais.
(1) `ℓ_*/ℓ_P = E_P/E_*` com `E_P = 1.22089 × 10¹⁹ GeV`, `E_* = 10¹⁰ GeV`:
`(ℓ_*/ℓ_P)² ∈ (1.49, 1.50) × 10¹⁸` ("≈ 1.5 × 10¹⁸"); os atrasos `6 × 10⁻⁶²` e `1.2 × 10⁻⁶⁰` s
reescalam para `(8.9 × 10⁻⁴⁴, 1.8 × 10⁻⁴²)` s ("∼ 10⁻⁴³–10⁻⁴² s").
(2) `ħc/ℓ_*` com `ħc = 1.973269804 × 10⁻⁷ eV·m`, `ℓ_* = 3.0 × 10⁻⁷ m`: `∈ (0.65, 0.66)` eV
("≈ 0.7 eV", um algarismo).
(3) Atraso `Δt ∝ ℓ_*²` a partir de `Δt(ℓ_P) = 3 × 10⁻⁶¹` s (desvio para o vermelho 3),
`ℓ_P = 1.616255 × 10⁻³⁵ m`: em `ℓ_* = 3.0 × 10⁻⁷ m`, `Δt ∈ (1.0, 1.04) × 10⁻⁴` s. -/
theorem dispersion_scales :
    (1.49e18 : ℝ) < (1.22089e19 / 1e10) ^ 2 ∧ (1.22089e19 / 1e10 : ℝ) ^ 2 < 1.50e18 ∧
    (8.9e-44 : ℝ) < 6e-62 * (1.22089e19 / 1e10) ^ 2 ∧
    (1.2e-60 : ℝ) * (1.22089e19 / 1e10) ^ 2 < 1.8e-42 ∧
    (0.65 : ℝ) < 1.973269804e-7 / 3.0e-7 ∧ (1.973269804e-7 / 3.0e-7 : ℝ) < 0.66 ∧
    (1.0e-4 : ℝ) < 3e-61 * (3.0e-7 / 1.616255e-35) ^ 2 ∧
    (3e-61 : ℝ) * (3.0e-7 / 1.616255e-35) ^ 2 < 1.04e-4 := by
  norm_num

/-- Mutante (atraso linear em `ℓ_*` em vez de quadratico): com `Δt ∝ ℓ_*`, `ℓ_* = 3.0 × 10⁻⁷ m`
daria `Δt < 10⁻²⁰` s, longe de `10⁻⁴` s. -/
theorem mutant_linear_delay_false : ¬ ((1.0e-4 : ℝ) < 3e-61 * (3.0e-7 / 1.616255e-35)) := by
  norm_num

/-- **Cota de fotons** (Crab, `ξ = 1`): `ħc/ℓ_* > 4.1 × 10¹⁴ GeV` com `ħc = 1.973269804 × 10⁻¹⁶
GeV·m` da `ℓ_* < 4.82 × 10⁻³¹ m`. Unidades: `ℓ` em m, `E` em GeV. -/
theorem photon_bound (ℓ : ℝ) (hℓ : 0 < ℓ) (hE : 4.1e14 < 1.973269804e-16 / ℓ) :
    ℓ < 4.82e-31 := by
  rw [lt_div_iff₀ hℓ] at hE
  nlinarith

/-- Mutante (o "`ℓ_* < 4.8 × 10⁻³¹ m`" literal do livro): nao segue de `ħc/ℓ_* > 4.1 × 10¹⁴ GeV`;
`ℓ_* = 4.81 × 10⁻³¹ m` da `ħc/ℓ_* ≈ 4.1024 × 10¹⁴ GeV`. A cota exata e `4.813 × 10⁻³¹ m`. -/
theorem mutant_photon_false :
    ¬ (∀ ℓ : ℝ, 0 < ℓ → 4.1e14 < 1.973269804e-16 / ℓ → ℓ < 4.8e-31) := by
  intro h
  have := h 4.81e-31 (by norm_num) (by norm_num)
  norm_num at this

/-- **Interferometria atomica**: `ℓ_P/λ_dB = m v ℓ_P/(2πħ) = m v/(2π m_P c) = k v`, com
`m = 86.9088775 u` (⁸⁷Sr), `u = 1.66053906660 × 10⁻²⁷ kg`, `m_P = 2.176434 × 10⁻⁸ kg`,
`c = 299792458 m/s`. Unidades: `k` em s/m, `v` em m/s, a razao e adimensional.
`k ∈ (3.50, 3.53) × 10⁻²⁷ s/m` ("≈ 3.5 × 10⁻²⁷") e `45 k < 2 × 10⁻²⁵` ("abaixo de 2 × 10⁻²⁵"
para `v ≤ 45 m/s`). -/
theorem atom_ratio :
    (3.50e-27 : ℝ) < 86.9088775 * 1.66053906660e-27 / (2 * π * 2.176434e-8 * 299792458) ∧
    86.9088775 * 1.66053906660e-27 / (2 * π * 2.176434e-8 * 299792458) < (3.53e-27 : ℝ) ∧
    45 * (86.9088775 * 1.66053906660e-27 / (2 * π * 2.176434e-8 * 299792458)) < (2e-25 : ℝ) := by
  have h1 := pi_gt_d4
  have h2 := pi_lt_d4
  have hpos : (0 : ℝ) < 2 * π * 2.176434e-8 * 299792458 := by positivity
  refine ⟨?_, ?_, ?_⟩
  · rw [lt_div_iff₀ hpos]; nlinarith
  · rw [div_lt_iff₀ hpos]; nlinarith
  · rw [← mul_div_assoc, div_lt_iff₀ hpos]; nlinarith

/-- Mutante (`45 k < 1.5 × 10⁻²⁵`): falso, pois `45 k > 1.57 × 10⁻²⁵`. -/
theorem mutant_atom_false :
    ¬ (45 * (86.9088775 * 1.66053906660e-27 / (2 * π * 2.176434e-8 * 299792458)) <
      (1.5e-25 : ℝ)) := by
  have := atom_ratio.1
  intro h
  linarith

end LeanReal.Chap13Numbers

#print axioms LeanReal.Chap13Numbers.hasDerivAt_erfc
#print axioms LeanReal.Chap13Numbers.g_ode
#print axioms LeanReal.Chap13Numbers.ds_formula_of_ode
#print axioms LeanReal.Chap13Numbers.ds_tau
#print axioms LeanReal.Chap13Numbers.witness_ds_tau
#print axioms LeanReal.Chap13Numbers.mutant_no_ode_false
#print axioms LeanReal.Chap13Numbers.mutant_sign_false
#print axioms LeanReal.Chap13Numbers.tensor_running
#print axioms LeanReal.Chap13Numbers.alpha_t_bounds
#print axioms LeanReal.Chap13Numbers.mutant_tensor_false
#print axioms LeanReal.Chap13Numbers.H_inf_bound
#print axioms LeanReal.Chap13Numbers.H_inf_at_bound
#print axioms LeanReal.Chap13Numbers.mutant_H_three_digits_false
#print axioms LeanReal.Chap13Numbers.alpha_t_numbers
#print axioms LeanReal.Chap13Numbers.alpha_t_window
#print axioms LeanReal.Chap13Numbers.mutant_alpha_false
#print axioms LeanReal.Chap13Numbers.dispersion_scales
#print axioms LeanReal.Chap13Numbers.mutant_linear_delay_false
#print axioms LeanReal.Chap13Numbers.photon_bound
#print axioms LeanReal.Chap13Numbers.mutant_photon_false
#print axioms LeanReal.Chap13Numbers.atom_ratio
#print axioms LeanReal.Chap13Numbers.mutant_atom_false
