import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.Calculus.Deriv.Prod
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.InverseDeriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

/-!
# Capitulo 9, `prop:winding_total_curvature` (item L5 do `PLANO_FORMALIZACAO.md`)

Fonte: `unified_quantum_gravity_book/chap09_global_homotopy_covering_spaces_jordan_loops.tex`,
Proposicao "Winding and total curvature" (`prop:winding_total_curvature`):

> Let `γ : [0,ℓ] → ℝ² ∖ {c}` be a unit-speed `C^{1,1}` curve and `θ` a continuous determination
> of `arg(γ - c)`. Then `∫_0^ℓ |θ'| ds ≤ ∫_0^ℓ |κ| ds + π`, and the constant `π` is sharp.
> Consequently, in the setting of Proposition `thm:loop_bounding`, every path of length at most
> `V` satisfies `2π|w_i(γ)| ≤ V‖κ‖_∞ + π + |Δθ_i(γ₀)|`.

## Reducao declarada

* `γ = (x, y) : ℝ → ℝ × ℝ`, continua em `[0,ℓ]`, com `γ' = (cos φ, sin φ)` em `(0,ℓ)`
  (comprimento de arco; `φ` = angulo tangente). `φ` tem derivada `κ` (curvatura com sinal) em
  `(0,ℓ)` e `κ` e CONTINUA em `[0,ℓ]`: curva `C²`. O caso do livro, `C^{1,1}` (`κ ∈ L^∞`), NAO
  esta coberto (exigiria FTC e regra da cadeia para funcoes absolutamente continuas).
* "`θ` determinacao continua de `arg(γ - c)`" e codificado por `γ = c + r(cos θ, sin θ)` em
  `[0,ℓ]` com `r > 0` (`hpolar`, `hr`), `θ` continua em `[0,ℓ]`.
* Hipotese NOMEADA `h_lift_C1` (+ `hθ'c`): `θ` e derivavel em `(0,ℓ)` com derivada `θ'` continua
  em `[0,ℓ]`. Para `γ` de classe `C¹` isso e consequencia da teoria de levantamentos
  (o levantamento de uma funcao `C¹` em `𝕊¹` e `C¹`), que nao e invocada aqui.
* `r` NAO e suposta continua nem derivavel: a continuidade sai de `r = (γ - c)·(cos θ, sin θ)`,
  e a identidade `r θ' = sin(φ - θ)` (`radial_identity`) sai de derivar
  `-(x - c₁) sin θ + (y - c₂) cos θ ≡ 0`.

## Prova (diferente da do livro)

O livro usa `G(x) = ∫_0^x sgn(sin t) dt` e a regra da cadeia de Lipschitz. Aqui usa-se a
suavizacao `G_a(x) = arccos(a cos x)`, `0 ≤ a < 1`, que e suave, tem valores em `[0,π]` e
derivada `g_a(x) = a sin x / √(1 - a² cos² x)` com `|g_a| ≤ 1` e `g_a · sin ≥ 0`. Com
`ψ = φ - θ`, `r θ' = sin ψ` e `r ≥ r₀ > 0` (compacidade), obtem-se
`|θ'| - |κ| ≤ -(G_a∘ψ)' + E(a)/r₀`, `E(a) = (1-a) + √(1-a²)` (`key_bound`), logo
`∫|θ'| ≤ ∫|κ| + π + ℓ E(a)/r₀`; faz-se `a → 1⁻`.

## Conteudo

* `winding_total_curvature` : a desigualdade principal.
* `net_angle_bound` : `|θ(ℓ) - θ(0)| ≤ ∫|κ| + π`.
* `winding_bound` : a consequencia, CONDICIONAL a hipotese nomeada `h_winding :
  Δθ(γ) - Δθ(γ₀) = 2πw` (a identidade da prova de `thm:loop_bounding`(1), que depende da
  teoria de homotopia do espaco livre, nao formalizada). Usa `|κ| ≤ K` e `ℓ ≤ V`.
* `pi_sharp` : o `π` e otimo: para todo `C < π` a desigualdade com `C` no lugar de `π` e FALSA
  (reta `x = 1` a distancia `1` de `c = 0`, comprimento `L` grande: `∫|θ'| = 2 arctan(L/2)`).
* Testemunha: `line_hyps` (a reta satisfaz todas as hipoteses) e `witness_line`.
* Mutantes provados falsos: `mutant_const_zero_false` (constante `0`) e
  `mutant_half_pi_false` (constante `π/2`), ambos casos de `pi_sharp`.
-/

noncomputable section

namespace LeanReal.Chap09Winding

open Set Real Filter Topology MeasureTheory intervalIntegral

/-! ## A identidade radial `r θ' = sin(φ - θ)` -/

/-- Se `γ = c + r(cos θ, sin θ)` perto de `s` e `γ'(s) = (cos φ(s), sin φ(s))`, entao
`r(s) θ'(s) = sin(φ(s) - θ(s))`. Prova: `f = -(x - c₁) sin θ + (y - c₂) cos θ` e nula perto de `s`. -/
theorem radial_identity (γ : ℝ → ℝ × ℝ) (c : ℝ × ℝ) (r θ θ' φ : ℝ → ℝ) (ℓ s : ℝ)
    (hs : s ∈ Ioo 0 ℓ) (hγ : HasDerivAt γ (cos (φ s), sin (φ s)) s)
    (hθ : HasDerivAt θ (θ' s) s)
    (hpolar : ∀ t ∈ Icc 0 ℓ, γ t = (c.1 + r t * cos (θ t), c.2 + r t * sin (θ t))) :
    r s * θ' s = sin (φ s - θ s) := by
  have hx : HasDerivAt (fun t => (γ t).1) (cos (φ s)) s := by
    have := ((ContinuousLinearMap.fst ℝ ℝ ℝ).hasFDerivAt.comp s hγ.hasFDerivAt).hasDerivAt
    simp only [ContinuousLinearMap.comp_apply, ContinuousLinearMap.toSpanSingleton_apply,
      one_smul, ContinuousLinearMap.coe_fst'] at this
    exact this
  have hy : HasDerivAt (fun t => (γ t).2) (sin (φ s)) s := by
    have := ((ContinuousLinearMap.snd ℝ ℝ ℝ).hasFDerivAt.comp s hγ.hasFDerivAt).hasDerivAt
    simp only [ContinuousLinearMap.comp_apply, ContinuousLinearMap.toSpanSingleton_apply,
      one_smul, ContinuousLinearMap.coe_snd'] at this
    exact this
  have h1 := ((hx.sub_const c.1).neg.mul hθ.sin).add ((hy.sub_const c.2).mul hθ.cos)
  have heq : (fun t => -((γ t).1 - c.1) * sin (θ t) + ((γ t).2 - c.2) * cos (θ t))
      =ᶠ[𝓝 s] fun _ => (0 : ℝ) := by
    filter_upwards [Icc_mem_nhds hs.1 hs.2] with t ht
    rw [hpolar t ht]
    ring
  have h0 : HasDerivAt (fun t => -((γ t).1 - c.1) * sin (θ t) + ((γ t).2 - c.2) * cos (θ t))
      0 s := (hasDerivAt_const s (0 : ℝ)).congr_of_eventuallyEq heq
  have hu := h1.unique h0
  simp only [Pi.neg_apply] at hu
  rw [hpolar s (Ioo_subset_Icc_self hs)] at hu
  dsimp only at hu
  rw [sin_sub]
  linear_combination (-1 : ℝ) * hu - (r s * θ' s) * sin_sq_add_cos_sq (θ s)

/-! ## A cota pontual da suavizacao -/

/-- Para `0 ≤ a < 1` e `S² + C² = 1`: `|S| - a S²/√(1 - (aC)²) ≤ (1 - a) + √(1 - a²)`. -/
theorem key_bound (a S C : ℝ) (ha0 : 0 ≤ a) (ha1 : a < 1) (hSC : S ^ 2 + C ^ 2 = 1) :
    |S| - a * S ^ 2 / √(1 - (a * C) ^ 2) ≤ (1 - a) + √(1 - a ^ 2) := by
  have ha2 : a ^ 2 < 1 := by nlinarith
  have hC2 : C ^ 2 ≤ 1 := by nlinarith [sq_nonneg S]
  have haC : (a * C) ^ 2 ≤ a ^ 2 := by
    rw [mul_pow]; nlinarith [sq_nonneg a]
  have hpos : 0 < 1 - (a * C) ^ 2 := by linarith
  set D := √(1 - (a * C) ^ 2) with hDdef
  set η := √(1 - a ^ 2) with hηdef
  have hD2 : D ^ 2 = 1 - (a * C) ^ 2 := Real.sq_sqrt hpos.le
  have hDpos : 0 < D := Real.sqrt_pos.2 hpos
  have hη0 : 0 ≤ η := Real.sqrt_nonneg _
  have hη2 : η ^ 2 = 1 - a ^ 2 := Real.sq_sqrt (by linarith)
  have hts : |S| ^ 2 = S ^ 2 := sq_abs S
  set t := |S| with htdef
  have ht0 : 0 ≤ t := abs_nonneg S
  have ht1 : t ≤ 1 := by nlinarith [sq_nonneg C]
  have hDup : D ≤ t + η := by
    rw [hDdef, Real.sqrt_le_iff]
    refine ⟨by linarith, ?_⟩
    have : a ^ 2 * S ^ 2 ≤ S ^ 2 := by nlinarith [sq_nonneg S]
    nlinarith [mul_nonneg ht0 hη0]
  have hmain : (t - (1 - a) - η) * D ≤ a * t ^ 2 := by
    rcases le_or_gt (t - (1 - a) - η) 0 with hneg | hposm
    · nlinarith [mul_nonpos_of_nonpos_of_nonneg hneg hDpos.le, sq_nonneg t]
    · have h1 : (t - (1 - a) - η) * D ≤ (t - (1 - a) - η) * (t + η) :=
        mul_le_mul_of_nonneg_left hDup hposm.le
      nlinarith [mul_nonneg (by linarith : (0:ℝ) ≤ 1 - a) hη0, sq_nonneg η,
        mul_nonneg (by linarith : (0:ℝ) ≤ 1 - a) (mul_nonneg ht0 (by linarith : (0:ℝ) ≤ 1 - t))]
  have h2 : t - (1 - a) - η ≤ a * t ^ 2 / D := (le_div_iff₀ hDpos).2 hmain
  rw [← hts]
  linarith

/-! ## O enunciado principal -/

/-- **Proposicao `prop:winding_total_curvature`** (desigualdade), na reducao `C²` do cabecalho:
`∫_0^ℓ |θ'| ≤ ∫_0^ℓ |κ| + π`. -/
theorem winding_total_curvature (γ : ℝ → ℝ × ℝ) (c : ℝ × ℝ) (r θ θ' φ κ : ℝ → ℝ) (ℓ : ℝ)
    (hℓ : 0 ≤ ℓ)
    (hγc : ContinuousOn γ (Icc 0 ℓ))
    (hγ : ∀ s ∈ Ioo 0 ℓ, HasDerivAt γ (cos (φ s), sin (φ s)) s)
    (hφc : ContinuousOn φ (Icc 0 ℓ)) (hφ : ∀ s ∈ Ioo 0 ℓ, HasDerivAt φ (κ s) s)
    (hκc : ContinuousOn κ (Icc 0 ℓ))
    (hr : ∀ s ∈ Icc 0 ℓ, 0 < r s)
    (hpolar : ∀ s ∈ Icc 0 ℓ, γ s = (c.1 + r s * cos (θ s), c.2 + r s * sin (θ s)))
    (hθc : ContinuousOn θ (Icc 0 ℓ))
    (h_lift_C1 : ∀ s ∈ Ioo 0 ℓ, HasDerivAt θ (θ' s) s) (hθ'c : ContinuousOn θ' (Icc 0 ℓ)) :
    ∫ s in (0:ℝ)..ℓ, |θ' s| ≤ (∫ s in (0:ℝ)..ℓ, |κ s|) + π := by
  have hrad : ∀ s ∈ Ioo 0 ℓ, r s * θ' s = sin (φ s - θ s) := fun s hs =>
    radial_identity γ c r θ θ' φ ℓ s hs (hγ s hs) (h_lift_C1 s hs) hpolar
  -- `r` e continua: `r = (γ - c)·(cos θ, sin θ)` em `[0,ℓ]`
  have hrc : ContinuousOn r (Icc 0 ℓ) := by
    have hf : ContinuousOn (fun t => ((γ t).1 - c.1) * cos (θ t) + ((γ t).2 - c.2) * sin (θ t))
        (Icc 0 ℓ) :=
      (((continuous_fst.comp_continuousOn hγc).sub continuousOn_const).mul
        (continuous_cos.comp_continuousOn hθc)).add
      (((continuous_snd.comp_continuousOn hγc).sub continuousOn_const).mul
        (continuous_sin.comp_continuousOn hθc))
    refine hf.congr fun t ht => ?_
    show r t = ((γ t).1 - c.1) * cos (θ t) + ((γ t).2 - c.2) * sin (θ t)
    rw [hpolar t ht]
    dsimp only
    linear_combination (-(r t)) * sin_sq_add_cos_sq (θ t)
  -- `r ≥ r₀ > 0` por compacidade
  obtain ⟨s₀, hs₀, hmin⟩ := isCompact_Icc.exists_isMinOn (nonempty_Icc.2 hℓ) hrc
  have hr₀ : 0 < r s₀ := hr s₀ hs₀
  have hr₀le : ∀ s ∈ Icc 0 ℓ, r s₀ ≤ r s := fun s hs => isMinOn_iff.mp hmin s hs
  have hθi : IntervalIntegrable (fun s => |θ' s|) volume 0 ℓ :=
    hθ'c.abs.intervalIntegrable_of_Icc hℓ
  have hκi : IntervalIntegrable (fun s => |κ s|) volume 0 ℓ :=
    hκc.abs.intervalIntegrable_of_Icc hℓ
  -- a cota suavizada, para cada `a ∈ [0,1)`
  have key : ∀ a ∈ Ico (0:ℝ) 1, ∫ s in (0:ℝ)..ℓ, |θ' s| ≤
      (∫ s in (0:ℝ)..ℓ, |κ s|) + π + ((1 - a) + √(1 - a ^ 2)) / r s₀ * ℓ := by
    intro a ha
    set E := (1 - a) + √(1 - a ^ 2) with hE
    have hE0 : 0 ≤ E := add_nonneg (by linarith [ha.2]) (Real.sqrt_nonneg _)
    have hlt : ∀ x : ℝ, |a * cos x| < 1 := fun x => by
      rw [abs_mul, abs_of_nonneg ha.1]
      calc a * |cos x| ≤ a * 1 := mul_le_mul_of_nonneg_left (abs_cos_le_one x) ha.1
        _ < 1 := by linarith [ha.2]
    set g : ℝ → ℝ := fun s => -arccos (a * cos (φ s - θ s)) + E / r s₀ * s with hg
    set g' : ℝ → ℝ := fun s => -(-(1 / √(1 - (a * cos (φ s - θ s)) ^ 2)) *
      (a * (-sin (φ s - θ s) * (κ s - θ' s)))) + E / r s₀ * 1 with hg'
    have hgc : ContinuousOn g (Icc 0 ℓ) :=
      ((continuous_arccos.comp_continuousOn (continuousOn_const.mul
        (continuous_cos.comp_continuousOn (hφc.sub hθc)))).neg).add
        (continuousOn_const.mul continuousOn_id)
    have hder : ∀ s ∈ Ioo 0 ℓ, HasDerivAt g (g' s) s := by
      intro s hs
      have hψ : HasDerivAt (fun t => φ t - θ t) (κ s - θ' s) s := (hφ s hs).sub (h_lift_C1 s hs)
      have hu : HasDerivAt (fun t => a * cos (φ t - θ t))
          (a * (-sin (φ s - θ s) * (κ s - θ' s))) s := hψ.cos.const_mul a
      have h1 : a * cos (φ s - θ s) ≠ -1 := by
        intro h; have := hlt (φ s - θ s); rw [h] at this; norm_num at this
      have h2 : a * cos (φ s - θ s) ≠ 1 := by
        intro h; have := hlt (φ s - θ s); rw [h] at this; norm_num at this
      exact ((Real.hasDerivAt_arccos h1 h2).comp s hu).neg.add
        ((hasDerivAt_id s).const_mul (E / r s₀))
    have hpt : ∀ s ∈ Ioo 0 ℓ, |θ' s| - |κ s| ≤ g' s := by
      intro s hs
      have hsI : s ∈ Icc 0 ℓ := Ioo_subset_Icc_self hs
      set S := sin (φ s - θ s) with hS
      set C := cos (φ s - θ s) with hC
      have hrs : 0 < r s := hr s hsI
      have hpos : 0 < 1 - (a * C) ^ 2 := by
        have := hlt (φ s - θ s)
        rw [← hC] at this
        have h' : (a * C) ^ 2 < 1 := by
          rw [← sq_abs]; nlinarith [abs_nonneg (a * C)]
        linarith
      set D := √(1 - (a * C) ^ 2) with hD
      have hDpos : 0 < D := Real.sqrt_pos.2 hpos
      have hθ'eq : θ' s = S / r s := by
        rw [eq_div_iff hrs.ne', mul_comm]; exact hrad s hs
      have hb := key_bound a S C ha.1 ha.2 (sin_sq_add_cos_sq _)
      rw [← hD] at hb
      have hq : |a * S / D| ≤ 1 := by
        rw [abs_div, abs_of_pos hDpos, div_le_one hDpos, abs_mul, abs_of_nonneg ha.1]
        have hSC := sin_sq_add_cos_sq (φ s - θ s)
        rw [← hS, ← hC] at hSC
        have hsum : a ^ 2 * S ^ 2 + a ^ 2 * C ^ 2 = a ^ 2 := by rw [← mul_add, hSC, mul_one]
        have ha2 : a ^ 2 < 1 := by nlinarith [ha.1, ha.2]
        have hle : |a * S| ≤ D := Real.abs_le_sqrt (by rw [mul_pow, mul_pow]; linarith)
        rwa [abs_mul, abs_of_nonneg ha.1] at hle
      have e1 : |θ' s| - (a * S / D) * θ' s = (|S| - a * S ^ 2 / D) / r s := by
        rw [hθ'eq, abs_div, abs_of_pos hrs]
        field_simp
      have e2 : (|S| - a * S ^ 2 / D) / r s ≤ E / r s₀ :=
        calc (|S| - a * S ^ 2 / D) / r s ≤ E / r s := div_le_div_of_nonneg_right hb hrs.le
          _ ≤ E / r s₀ := div_le_div_of_nonneg_left hE0 hr₀ (hr₀le s hsI)
      have e3 : (a * S / D) * κ s ≤ |κ s| :=
        calc (a * S / D) * κ s ≤ |(a * S / D) * κ s| := le_abs_self _
          _ = |a * S / D| * |κ s| := by rw [abs_mul]
          _ ≤ 1 * |κ s| := mul_le_mul_of_nonneg_right hq (abs_nonneg _)
          _ = |κ s| := one_mul _
      have e4 : g' s = -(a * S / D) * κ s + (a * S / D) * θ' s + E / r s₀ := by
        simp only [hg', ← hS, ← hC, ← hD]
        ring
      rw [e4]
      linarith
    have hint := integral_le_sub_of_hasDeriv_right_of_le (φ := fun s => |θ' s| - |κ s|) hℓ hgc
      (fun s hs => (hder s hs).hasDerivWithinAt)
      ((hθ'c.abs.sub hκc.abs).integrableOn_Icc) hpt
    rw [integral_sub hθi hκi] at hint
    have hgb : g ℓ - g 0 ≤ π + E / r s₀ * ℓ := by
      simp only [hg, mul_zero]
      linarith [arccos_nonneg (a * cos (φ ℓ - θ ℓ)), arccos_le_pi (a * cos (φ 0 - θ 0))]
    linarith
  -- limite `a → 1⁻`
  have hlim : Tendsto (fun a : ℝ => (∫ s in (0:ℝ)..ℓ, |κ s|) + π +
      ((1 - a) + √(1 - a ^ 2)) / r s₀ * ℓ) (𝓝[<] 1) (𝓝 ((∫ s in (0:ℝ)..ℓ, |κ s|) + π)) := by
    have hcont : Continuous (fun a : ℝ => (∫ s in (0:ℝ)..ℓ, |κ s|) + π +
        ((1 - a) + √(1 - a ^ 2)) / r s₀ * ℓ) := by fun_prop
    have := (hcont.tendsto 1).mono_left (nhdsWithin_le_nhds (s := Iio 1))
    simpa using this
  exact ge_of_tendsto hlim (eventually_of_mem (Ico_mem_nhdsLT (by norm_num : (0:ℝ) < 1)) key)

/-! ## Consequencias -/

/-- `|θ(ℓ) - θ(0)| ≤ ∫|κ| + π` (variacao liquida do argumento). -/
theorem net_angle_bound (γ : ℝ → ℝ × ℝ) (c : ℝ × ℝ) (r θ θ' φ κ : ℝ → ℝ) (ℓ : ℝ)
    (hℓ : 0 ≤ ℓ)
    (hγc : ContinuousOn γ (Icc 0 ℓ))
    (hγ : ∀ s ∈ Ioo 0 ℓ, HasDerivAt γ (cos (φ s), sin (φ s)) s)
    (hφc : ContinuousOn φ (Icc 0 ℓ)) (hφ : ∀ s ∈ Ioo 0 ℓ, HasDerivAt φ (κ s) s)
    (hκc : ContinuousOn κ (Icc 0 ℓ))
    (hr : ∀ s ∈ Icc 0 ℓ, 0 < r s)
    (hpolar : ∀ s ∈ Icc 0 ℓ, γ s = (c.1 + r s * cos (θ s), c.2 + r s * sin (θ s)))
    (hθc : ContinuousOn θ (Icc 0 ℓ))
    (h_lift_C1 : ∀ s ∈ Ioo 0 ℓ, HasDerivAt θ (θ' s) s) (hθ'c : ContinuousOn θ' (Icc 0 ℓ)) :
    |θ ℓ - θ 0| ≤ (∫ s in (0:ℝ)..ℓ, |κ s|) + π := by
  have hftc : ∫ s in (0:ℝ)..ℓ, θ' s = θ ℓ - θ 0 :=
    integral_eq_sub_of_hasDerivAt_of_le hℓ hθc h_lift_C1 (hθ'c.intervalIntegrable_of_Icc hℓ)
  rw [← hftc]
  exact (abs_integral_le_integral_abs hℓ).trans
    (winding_total_curvature γ c r θ θ' φ κ ℓ hℓ hγc hγ hφc hφ hκc hr hpolar hθc h_lift_C1 hθ'c)

/-- **Consequencia de `prop:winding_total_curvature`**: `2π|w| ≤ V K + π + |Δ₀|`, se `|κ| ≤ K`,
`ℓ ≤ V`, e CONDICIONAL a hipotese nomeada `h_winding : Δθ(γ) - Δθ(γ₀) = 2πw` (identidade da prova
de `thm:loop_bounding`(1); a teoria de homotopia do espaco livre nao esta formalizada). -/
theorem winding_bound (γ : ℝ → ℝ × ℝ) (c : ℝ × ℝ) (r θ θ' φ κ : ℝ → ℝ) (ℓ : ℝ)
    (hℓ : 0 ≤ ℓ)
    (hγc : ContinuousOn γ (Icc 0 ℓ))
    (hγ : ∀ s ∈ Ioo 0 ℓ, HasDerivAt γ (cos (φ s), sin (φ s)) s)
    (hφc : ContinuousOn φ (Icc 0 ℓ)) (hφ : ∀ s ∈ Ioo 0 ℓ, HasDerivAt φ (κ s) s)
    (hκc : ContinuousOn κ (Icc 0 ℓ))
    (hr : ∀ s ∈ Icc 0 ℓ, 0 < r s)
    (hpolar : ∀ s ∈ Icc 0 ℓ, γ s = (c.1 + r s * cos (θ s), c.2 + r s * sin (θ s)))
    (hθc : ContinuousOn θ (Icc 0 ℓ))
    (h_lift_C1 : ∀ s ∈ Ioo 0 ℓ, HasDerivAt θ (θ' s) s) (hθ'c : ContinuousOn θ' (Icc 0 ℓ))
    (K V Δ₀ : ℝ) (w : ℤ) (hK : ∀ s ∈ Icc 0 ℓ, |κ s| ≤ K) (hK0 : 0 ≤ K) (hV : ℓ ≤ V)
    (h_winding : (θ ℓ - θ 0) - Δ₀ = 2 * π * w) :
    2 * π * |(w : ℝ)| ≤ V * K + π + |Δ₀| := by
  have hnet := net_angle_bound γ c r θ θ' φ κ ℓ hℓ hγc hγ hφc hφ hκc hr hpolar hθc h_lift_C1 hθ'c
  have hκK : ∫ s in (0:ℝ)..ℓ, |κ s| ≤ ℓ * K := by
    have := integral_mono_on (μ := volume) hℓ (hκc.abs.intervalIntegrable_of_Icc hℓ)
      intervalIntegrable_const hK
    simpa using this
  have hw : 2 * π * |(w : ℝ)| = |(θ ℓ - θ 0) - Δ₀| := by
    rw [h_winding, abs_mul, abs_of_pos (by positivity : (0:ℝ) < 2 * π)]
  have htri : |(θ ℓ - θ 0) - Δ₀| ≤ |θ ℓ - θ 0| + |Δ₀| := abs_sub _ _
  have hVK : ℓ * K ≤ V * K := mul_le_mul_of_nonneg_right hV hK0
  linarith

/-! ## Testemunha: a reta `x = 1`, `c = 0`, comprimento `L` -/

/-- A reta `s ↦ (1, s - L/2)`, `s ∈ [0,L]`, com `φ = π/2`, `κ = 0`. -/
def lineγ (L : ℝ) (s : ℝ) : ℝ × ℝ := (1, s - L / 2)
/-- `θ = arg(γ - 0) = arctan(s - L/2)`. -/
def lineθ (L : ℝ) (s : ℝ) : ℝ := arctan (s - L / 2)
/-- `θ' = 1/(1 + (s - L/2)²)`. -/
def lineθ' (L : ℝ) (s : ℝ) : ℝ := 1 / (1 + (s - L / 2) ^ 2)
/-- `r = |γ - 0| = √(1 + (s - L/2)²)`. -/
def liner (L : ℝ) (s : ℝ) : ℝ := √(1 + (s - L / 2) ^ 2)

/-- A reta satisfaz TODAS as hipoteses de `winding_total_curvature` (com `c = 0`). -/
theorem line_hyps (L : ℝ) :
    ContinuousOn (lineγ L) (Icc 0 L) ∧
    (∀ s ∈ Ioo 0 L, HasDerivAt (lineγ L) (cos ((fun _ => π / 2) s), sin ((fun _ => π / 2) s)) s) ∧
    ContinuousOn (fun _ => π / 2) (Icc 0 L) ∧
    (∀ s ∈ Ioo 0 L, HasDerivAt (fun _ : ℝ => π / 2) ((fun _ => (0:ℝ)) s) s) ∧
    ContinuousOn (fun _ : ℝ => (0:ℝ)) (Icc 0 L) ∧
    (∀ s ∈ Icc 0 L, 0 < liner L s) ∧
    (∀ s ∈ Icc 0 L, lineγ L s = ((0 : ℝ × ℝ).1 + liner L s * cos (lineθ L s),
      (0 : ℝ × ℝ).2 + liner L s * sin (lineθ L s))) ∧
    ContinuousOn (lineθ L) (Icc 0 L) ∧
    (∀ s ∈ Ioo 0 L, HasDerivAt (lineθ L) (lineθ' L s) s) ∧
    ContinuousOn (lineθ' L) (Icc 0 L) := by
  have hpos : ∀ s, 0 < 1 + (s - L / 2) ^ 2 := fun s => by positivity
  refine ⟨?_, ?_, continuousOn_const, fun s _ => hasDerivAt_const s _, continuousOn_const,
    fun s _ => Real.sqrt_pos.2 (hpos s), ?_, ?_, ?_, ?_⟩
  · exact (continuous_const.prodMk (continuous_id.sub continuous_const)).continuousOn
  · intro s _
    have := (hasDerivAt_const s (1:ℝ)).prodMk ((hasDerivAt_id s).sub_const (L / 2))
    simp only [cos_pi_div_two, sin_pi_div_two]
    exact this
  · intro s _
    have hne : √(1 + (s - L / 2) ^ 2) ≠ 0 := (Real.sqrt_pos.2 (hpos s)).ne'
    simp only [lineγ, liner, lineθ, cos_arctan, sin_arctan, Prod.fst_zero, Prod.snd_zero,
      zero_add]
    ext
    · simp only; field_simp
    · simp only; field_simp
  · exact (continuous_arctan.comp (continuous_id.sub continuous_const)).continuousOn
  · intro s _
    have := (Real.hasDerivAt_arctan (s - L / 2)).comp s ((hasDerivAt_id s).sub_const (L / 2))
    rw [mul_one] at this
    exact this
  · exact (continuous_const.div (continuous_const.add
      ((continuous_id.sub continuous_const).pow 2)) fun s => (hpos s).ne').continuousOn

/-- `∫_0^L |θ'| = 2 arctan(L/2)` na reta. -/
theorem line_integral (L : ℝ) (hL : 0 ≤ L) :
    ∫ s in (0:ℝ)..L, |lineθ' L s| = 2 * arctan (L / 2) := by
  obtain ⟨-, -, -, -, -, -, -, h8, h9, h10⟩ := line_hyps L
  have habs : (fun s => |lineθ' L s|) = lineθ' L := funext fun s => abs_of_pos (by
    unfold lineθ'; positivity)
  rw [habs, integral_eq_sub_of_hasDerivAt_of_le hL h8 h9 (h10.intervalIntegrable_of_Icc hL)]
  simp only [lineθ]
  rw [show (0:ℝ) - L / 2 = -(L / 2) by ring, arctan_neg, show L - L / 2 = L / 2 by ring]
  ring

/-- **Testemunha de nao vacuidade** (`L = 2`): o teorema se aplica a reta e da
`π/2 = 2 arctan 1 ≤ 0 + π`. -/
theorem witness_line : ∫ s in (0:ℝ)..2, |lineθ' 2 s| ≤
    (∫ s in (0:ℝ)..2, |(fun _ : ℝ => (0:ℝ)) s|) + π := by
  obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9, h10⟩ := line_hyps 2
  exact winding_total_curvature (lineγ 2) 0 (liner 2) (lineθ 2) (lineθ' 2) (fun _ => π / 2)
    (fun _ => 0) 2 (by norm_num) h1 h2 h3 h4 h5 h6 h7 h8 h9 h10

/-! ## Otimalidade de `π` e mutantes provados FALSOS -/

/-- **`π` e otimo** (afirmacao "the constant `π` is sharp"): para todo `C < π`, a desigualdade
com `C` no lugar de `π` e falsa. -/
theorem pi_sharp (C : ℝ) (hC : C < π) :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (c : ℝ × ℝ) (r θ θ' φ κ : ℝ → ℝ) (ℓ : ℝ), 0 ≤ ℓ →
        ContinuousOn γ (Icc 0 ℓ) → (∀ s ∈ Ioo 0 ℓ, HasDerivAt γ (cos (φ s), sin (φ s)) s) →
        ContinuousOn φ (Icc 0 ℓ) → (∀ s ∈ Ioo 0 ℓ, HasDerivAt φ (κ s) s) →
        ContinuousOn κ (Icc 0 ℓ) → (∀ s ∈ Icc 0 ℓ, 0 < r s) →
        (∀ s ∈ Icc 0 ℓ, γ s = (c.1 + r s * cos (θ s), c.2 + r s * sin (θ s))) →
        ContinuousOn θ (Icc 0 ℓ) → (∀ s ∈ Ioo 0 ℓ, HasDerivAt θ (θ' s) s) →
        ContinuousOn θ' (Icc 0 ℓ) →
        ∫ s in (0:ℝ)..ℓ, |θ' s| ≤ (∫ s in (0:ℝ)..ℓ, |κ s|) + C) := by
  intro h
  have ht : Tendsto (fun L : ℝ => 2 * arctan (L / 2)) atTop (𝓝 π) := by
    have h1 := (tendsto_arctan_atTop.mono_right nhdsWithin_le_nhds).comp
      (tendsto_id.atTop_div_const (by norm_num : (0:ℝ) < 2))
    have hπ2 : π = 2 * (π / 2) := by ring
    rw [hπ2]
    exact h1.const_mul 2
  obtain ⟨L, hLC, hL0⟩ := ((ht.eventually (lt_mem_nhds hC)).and (eventually_ge_atTop 0)).exists
  obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9, h10⟩ := line_hyps L
  have := h (lineγ L) 0 (liner L) (lineθ L) (lineθ' L) (fun _ => π / 2) (fun _ => 0) L hL0
    h1 h2 h3 h4 h5 h6 h7 h8 h9 h10
  rw [line_integral L hL0] at this
  simp at this
  linarith

/-- Mutante 1 (constante `0`: "o argumento nao gira mais que a tangente"): FALSO. -/
theorem mutant_const_zero_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (c : ℝ × ℝ) (r θ θ' φ κ : ℝ → ℝ) (ℓ : ℝ), 0 ≤ ℓ →
        ContinuousOn γ (Icc 0 ℓ) → (∀ s ∈ Ioo 0 ℓ, HasDerivAt γ (cos (φ s), sin (φ s)) s) →
        ContinuousOn φ (Icc 0 ℓ) → (∀ s ∈ Ioo 0 ℓ, HasDerivAt φ (κ s) s) →
        ContinuousOn κ (Icc 0 ℓ) → (∀ s ∈ Icc 0 ℓ, 0 < r s) →
        (∀ s ∈ Icc 0 ℓ, γ s = (c.1 + r s * cos (θ s), c.2 + r s * sin (θ s))) →
        ContinuousOn θ (Icc 0 ℓ) → (∀ s ∈ Ioo 0 ℓ, HasDerivAt θ (θ' s) s) →
        ContinuousOn θ' (Icc 0 ℓ) →
        ∫ s in (0:ℝ)..ℓ, |θ' s| ≤ (∫ s in (0:ℝ)..ℓ, |κ s|) + 0) :=
  pi_sharp 0 pi_pos

/-- Mutante 2 (constante `π/2`): FALSO. -/
theorem mutant_half_pi_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (c : ℝ × ℝ) (r θ θ' φ κ : ℝ → ℝ) (ℓ : ℝ), 0 ≤ ℓ →
        ContinuousOn γ (Icc 0 ℓ) → (∀ s ∈ Ioo 0 ℓ, HasDerivAt γ (cos (φ s), sin (φ s)) s) →
        ContinuousOn φ (Icc 0 ℓ) → (∀ s ∈ Ioo 0 ℓ, HasDerivAt φ (κ s) s) →
        ContinuousOn κ (Icc 0 ℓ) → (∀ s ∈ Icc 0 ℓ, 0 < r s) →
        (∀ s ∈ Icc 0 ℓ, γ s = (c.1 + r s * cos (θ s), c.2 + r s * sin (θ s))) →
        ContinuousOn θ (Icc 0 ℓ) → (∀ s ∈ Ioo 0 ℓ, HasDerivAt θ (θ' s) s) →
        ContinuousOn θ' (Icc 0 ℓ) →
        ∫ s in (0:ℝ)..ℓ, |θ' s| ≤ (∫ s in (0:ℝ)..ℓ, |κ s|) + π / 2) :=
  pi_sharp (π / 2) (by linarith [pi_pos])

end LeanReal.Chap09Winding

#print axioms LeanReal.Chap09Winding.radial_identity
#print axioms LeanReal.Chap09Winding.key_bound
#print axioms LeanReal.Chap09Winding.winding_total_curvature
#print axioms LeanReal.Chap09Winding.net_angle_bound
#print axioms LeanReal.Chap09Winding.winding_bound
#print axioms LeanReal.Chap09Winding.line_hyps
#print axioms LeanReal.Chap09Winding.line_integral
#print axioms LeanReal.Chap09Winding.witness_line
#print axioms LeanReal.Chap09Winding.pi_sharp
#print axioms LeanReal.Chap09Winding.mutant_const_zero_false
#print axioms LeanReal.Chap09Winding.mutant_half_pi_false
