import LeanReal.Chap07Bounds

/-!
# L2 LIVRO B4: testemunhas extra para `Chap07Bounds` (cap. 7)

Revisao L2 independente. As testemunhas do escritor atingem todas a IGUALDADE nas cotas. Aqui:

1. `prop:gauss_bonnet_floor`: testemunhas com desigualdade ESTRITA, em que a hipotese `hop` morde
   (falha com `κ` menor): dados anisotropicos `II = diag(1, 1/4)` (`χ = 2`) e a sela real
   `II = diag(1, -1)` vista em codimensao dois (`N = ℂ`, `χ = -1`).
2. `thm:scaling_law` (2): testemunha pontual estrita (`v = (1, 0)`, `m = 2`): `∑|a_j|² = 1 > 1/2`.
3. `prop:knot_gap`, por curva: Fenchel com desigualdade estrita (circulo duplo).
4. `prop:knot_gap`, hipotese GLOBAL `hFM`: um predicado concreto `IsK3` (curva igual ao circulo
   unitario, comprimento `≥ 6π`) para o qual `hFM` e PROVADA e `knotSet` e nao vazio; a conclusao
   (a) vale com `4π/L < 1`. `IsK3` NAO e um tipo de no: so mostra que `hFM` e satisfazivel de modo
   nao vazio. A hipotese global `hFen` e o proprio teorema de Fenchel e nao e descarregada aqui.
5. Mutante: `hFM` sem o predicado de tipo de no (para toda curva fechada) e FALSA.
-/

noncomputable section

namespace LeanReal.L2_LIVRO_B4_Extra

open Set Real MeasureTheory LeanReal.Chap07Bounds

/-! ## 1. Gauss–Bonnet: testemunhas estritas -/

/-- Dados anisotropicos de codimensao um: `|II(v,v)| = v₁² + v₂²/4 ≤ 1`. -/
theorem hop_aniso (v1 v2 : ℝ) (h : v1 ^ 2 + v2 ^ 2 = 1) :
    ‖IIq (1 : ℝ) 0 (1 / 4) v1 v2‖ ≤ 1 := by
  simp only [IIq, smul_eq_mul, Real.norm_eq_abs]
  rw [abs_le]; constructor <;> nlinarith [sq_nonneg v1, sq_nonneg v2]

/-- A hipotese `hop` morde: com `κ = 1/2` ela falha em `v = e₁`. -/
theorem hop_aniso_bites : ¬ ∀ v1 v2 : ℝ, v1 ^ 2 + v2 ^ 2 = 1 →
    ‖IIq (1 : ℝ) 0 (1 / 4) v1 v2‖ ≤ 1 / 2 := by
  intro h
  have := h 1 0 (by norm_num)
  simp [IIq] at this
  norm_num at this

/-- **Testemunha estrita, `χ = 2`.** `II = diag(1, 1/4)` (`κ = 1`, `K = 1/4`), area `16π`:
`∫K = 4π = 2π·2`, e a cota da `√(2πχ/A) = 1/2 < 1 = κ`. -/
theorem witness_GB_strict_pos :
    √(2 * π * ((2 : ℤ) : ℝ) / (areaMeasure (16 * π)).real univ) = 1 / 2 ∧
    √(2 * π * ((2 : ℤ) : ℝ) / (areaMeasure (16 * π)).real univ) < 1 := by
  have hA : (0 : ℝ) ≤ 16 * π := by positivity
  have e : √(2 * π * ((2 : ℤ) : ℝ) / (areaMeasure (16 * π)).real univ) = 1 / 2 := by
    rw [areaMeasure_real_univ hA]
    have : 2 * π * ((2 : ℤ) : ℝ) / (16 * π) = (1 / 2) ^ 2 := by
      field_simp; push_cast; ring
    rw [this, Real.sqrt_sq (by norm_num)]
  exact ⟨e, by rw [e]; norm_num⟩

/-- As hipoteses de `gauss_bonnet_floor_pos` valem para os dados anisotropicos, e o teorema
se aplica (com folga, por `witness_GB_strict_pos`). -/
theorem apply_GB_strict_pos :
    √(2 * π * ((2 : ℤ) : ℝ) / (areaMeasure (16 * π)).real univ) ≤ 1 := by
  have hA : (0 : ℝ) ≤ 16 * π := by positivity
  refine gauss_bonnet_floor_pos (areaMeasure (16 * π)) (fun _ => (1 : ℝ)) (fun _ => 0)
    (fun _ => 1 / 4) 1 2 ?_ (fun _ v1 v2 h => hop_aniso v1 v2 h) (integrable_const _) ?_
    (by norm_num)
  · rw [areaMeasure_real_univ hA]; positivity
  · have : gaussK (1 : ℝ) 0 (1 / 4) = 1 / 4 := by
      simp only [gaussK, Real.inner_apply, norm_zero]; ring
    show ∫ _ : ℝ, gaussK (1 : ℝ) 0 (1 / 4) ∂(areaMeasure (16 * π)) = _
    rw [this, integral_areaMeasure_const hA]; push_cast; ring

/-- Sela real vista no plano normal `ℂ`: `II(v,v) = v₁² - v₂²`. -/
theorem hop_saddle_C (v1 v2 : ℝ) (h : v1 ^ 2 + v2 ^ 2 = 1) :
    ‖IIq (1 : ℂ) 0 (-1) v1 v2‖ ≤ 1 := by
  have e : IIq (1 : ℂ) 0 (-1) v1 v2 = ((v1 ^ 2 - v2 ^ 2 : ℝ) : ℂ) := by
    apply Complex.ext <;> simp [IIq] <;> ring
  rw [e, Complex.norm_real, Real.norm_eq_abs, abs_le]
  constructor <;> nlinarith [sq_nonneg v1, sq_nonneg v2]

/-- `K = -1` para a sela em `ℂ`. -/
theorem gaussK_saddle_C : gaussK (1 : ℂ) 0 (-1) = -1 := by
  simp [gaussK]

/-- **Testemunha estrita, codimensao dois, `χ = -1`.** A sela real em `N = ℂ` (`κ = 1`,
`K = -1`), area `2π`: hipoteses de `gauss_bonnet_floor_neg`, e a cota da `√(π/2π) = √(1/2) < 1`.
(Em codimensao dois a cota `-2κ²` so e justa para dados como os da curva complexa.) -/
theorem witness_GB_strict_neg :
    √(π * |((-1 : ℤ) : ℝ)| / (areaMeasure (2 * π)).real univ) ≤ 1 ∧
    √(π * |((-1 : ℤ) : ℝ)| / (areaMeasure (2 * π)).real univ) < 1 := by
  have hA : (0 : ℝ) ≤ 2 * π := by positivity
  refine ⟨gauss_bonnet_floor_neg (areaMeasure (2 * π)) (fun _ => (1 : ℂ)) (fun _ => 0)
    (fun _ => -1) 1 (-1) ?_ (fun _ v1 v2 h => hop_saddle_C v1 v2 h) (integrable_const _) ?_
    (by norm_num), ?_⟩
  · rw [areaMeasure_real_univ hA]; positivity
  · show ∫ _ : ℝ, gaussK (1 : ℂ) 0 (-1) ∂(areaMeasure (2 * π)) = _
    rw [gaussK_saddle_C, integral_areaMeasure_const hA]; push_cast; ring
  · rw [areaMeasure_real_univ hA]
    have : π * |((-1 : ℤ) : ℝ)| / (2 * π) = 1 / 2 := by
      push_cast; rw [abs_neg, abs_one]; field_simp
    rw [this, show (1 : ℝ) = √1 from Real.sqrt_one.symm]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)

/-! ## 2. Varios planos: testemunha pontual estrita -/

/-- Curvatura `1` da projecao `j = 0`: `v = 1`, `a = i`. -/
theorem planeCurv_one_I : planeCurv (1 : ℂ) Complex.I = 1 := by
  simp [planeCurv]

/-- **Testemunha estrita de `several_planes_pointwise`** (`m = 2`, `R₀ = 1`): `v = (1, 0)`,
`a = (i, 0)`. A hipotese de curvatura morde em `j = 0` (curvatura exatamente `1/R₀`) e e vazia em
`j = 1` (`v₁ = 0`); a conclusao vale com folga: `∑|a_j|² = 1 > 1/2 = 1/(m R₀²)`. -/
theorem witness_several_planes_strict :
    (∑ j : Fin 2, ‖(![1, 0] : Fin 2 → ℂ) j‖ ^ 2 = 1) ∧
    (∀ j : Fin 2, (![1, 0] : Fin 2 → ℂ) j ≠ 0 →
      1 / (1 : ℝ) ≤ |planeCurv ((![1, 0] : Fin 2 → ℂ) j) ((![Complex.I, 0] : Fin 2 → ℂ) j)|) ∧
    1 / ((2 : ℕ) * (1 : ℝ) ^ 2) < ∑ j : Fin 2, ‖(![Complex.I, 0] : Fin 2 → ℂ) j‖ ^ 2 := by
  refine ⟨by simp [Fin.sum_univ_two], fun j hj => ?_, by simp [Fin.sum_univ_two]; norm_num⟩
  fin_cases j
  · simp [planeCurv_one_I]
  · exact absurd rfl hj

/-- O teorema se aplica a testemunha estrita. -/
example : 1 / ((2 : ℕ) * (1 : ℝ) ^ 2) ≤ ∑ j : Fin 2, ‖(![Complex.I, 0] : Fin 2 → ℂ) j‖ ^ 2 :=
  several_planes_pointwise _ _ one_pos witness_several_planes_strict.1
    witness_several_planes_strict.2.1

/-! ## 3. Fenchel por curva, estrito -/

/-- **Testemunha estrita (Fenchel, por curva):** o circulo unitario percorrido 2 vezes
(`ℓ = L = 4π`, curvatura total `4π ≥ 2π`); `fenchel_curve_bound` da `2π/L = 1/2 ≤ 1 = k`, com
folga. -/
theorem witness_fenchel_strict :
    2 * π / (2 * π * 1 * 2) ≤ (1 : ℝ) ∧ 2 * π / (2 * π * 1 * 2) < (1 : ℝ) := by
  obtain ⟨hc, ht⟩ := circle_closedAdm one_pos (norm_one) Complex.norm_I inner_one_I 2
    (by norm_num) (L := 2 * π * 1 * 2) (by push_cast; rfl)
  simp only [div_one] at hc
  push_cast at hc ht
  refine ⟨fenchel_curve_bound hc (by rw [ht]; nlinarith [Real.pi_pos]), ?_⟩
  rw [div_lt_one (by positivity)]; nlinarith [Real.pi_pos]

/-! ## 4. `knot_gap`: a hipotese global `hFM` e satisfazivel de modo nao vazio -/

/-- Predicado concreto (NAO um tipo de no): a curva e o circulo unitario de `ℂ` e o comprimento
e `≥ 6π`. -/
def IsK3 (γ : ℝ → ℂ) (ℓ : ℝ) : Prop := 6 * π ≤ ℓ ∧ γ = circleCurve 1 (1 : ℂ) Complex.I

/-- `‖circleAcc 1 1 i‖ = 1`. -/
theorem norm_circleAcc_one (t : ℝ) : ‖circleAcc 1 (1 : ℂ) Complex.I t‖ = 1 := by
  rw [circleAcc, norm_comb norm_one Complex.norm_I inner_one_I]
  have : (-(1 / (1 : ℝ)) * Real.cos (t / 1)) ^ 2 + (-(1 / (1 : ℝ)) * Real.sin (t / 1)) ^ 2 = 1 := by
    simp only [div_one, neg_mul, one_mul, neg_sq]; exact Real.cos_sq_add_sin_sq t
  rw [this, Real.sqrt_one]

/-- **`hFM` vale para `IsK3`** (para todo `L`): toda curva fechada admissivel com `IsK3` tem
`γ'' = circleAcc` em `(0, ℓ)` (unicidade das derivadas), logo curvatura total `ℓ ≥ 6π > 4π`. -/
theorem hFM_IsK3 (L : ℝ) : ∀ k ℓ (γ γ' γ'' : ℝ → ℂ), ClosedAdm L k ℓ γ γ' γ'' → IsK3 γ ℓ →
    4 * π < totalCurv γ'' ℓ := by
  rintro k ℓ γ γ' γ'' ⟨hℓ0, -, -, -, hc⟩ ⟨hℓ, rfl⟩
  have hacc : ∀ t ∈ Ioo 0 ℓ, ‖γ'' t‖ = 1 := by
    intro t ht
    have hev : γ' =ᶠ[nhds t] circleVel 1 (1 : ℂ) Complex.I := by
      filter_upwards [Ioo_mem_nhds ht.1 ht.2] with s hs
      exact (hc s (Ioo_subset_Icc_self hs)).1.unique (circle_hasDerivAt one_ne_zero 1 _ s)
    have h2 : HasDerivAt (circleVel 1 (1 : ℂ) Complex.I) (γ'' t) t :=
      (hc t (Ioo_subset_Icc_self ht)).2.1.congr_of_eventuallyEq hev.symm
    rw [h2.unique (circleVel_hasDerivAt 1 1 _ t), norm_circleAcc_one]
  have hint : totalCurv γ'' ℓ = ℓ := by
    unfold totalCurv
    rw [intervalIntegral.integral_of_le hℓ0.le, integral_Ioc_eq_integral_Ioo,
      setIntegral_congr_fun measurableSet_Ioo (fun t ht => hacc t ht), setIntegral_const,
      Real.volume_real_Ioo_of_le hℓ0.le, smul_eq_mul, mul_one, sub_zero]
  rw [hint]; nlinarith [Real.pi_pos]

/-- O triplo circulo pertence a `knotSet IsK3 (6π)`: a classe e nao vazia. -/
theorem knotSet_IsK3_nonempty : (1 : ℝ) ∈ knotSet IsK3 (2 * π * 1 * 3) := by
  refine ⟨2 * π * 1 * 3, _, _, _, witness_knot_curve.1, ?_, rfl⟩
  nlinarith [Real.pi_pos]

/-- **Conclusao (a) de `knot_gap` para `IsK3`, sem Fenchel:** `4π/L ≤ inf knotSet`, e
`4π/L = 2/3 < 1`, valor atingido por um elemento da classe. -/
theorem knot_gap_a_IsK3 :
    4 * π / (2 * π * 1 * 3) ≤ sInf (knotSet IsK3 (2 * π * 1 * 3)) ∧
    4 * π / (2 * π * 1 * 3) < 1 := by
  refine ⟨le_csInf ⟨1, knotSet_IsK3_nonempty⟩ ?_, ?_⟩
  · rintro k ⟨ℓ, γ, γ', γ'', hc, hK⟩
    exact (knot_curve_bound hc (hFM_IsK3 _ k ℓ γ γ' γ'' hc hK)).le
  · rw [div_lt_one (by positivity)]; nlinarith [Real.pi_pos]

/-! ## 5. Mutante: Fary–Milnor sem o predicado de no -/

/-- **Mutante:** `hFM` para TODA curva fechada (sem `IsK`) e FALSA: o circulo tem curvatura
total `2π`. -/
theorem mutant_hFM_without_IsK_false :
    ¬ (∀ k ℓ (γ γ' γ'' : ℝ → ℂ), ClosedAdm (2 * π) k ℓ γ γ' γ'' → 4 * π < totalCurv γ'' ℓ) := by
  intro h
  obtain ⟨hc, ht, -⟩ := witness_fenchel
  have := h _ _ _ _ _ hc
  rw [ht] at this; nlinarith [Real.pi_pos]

end LeanReal.L2_LIVRO_B4_Extra

#print axioms LeanReal.L2_LIVRO_B4_Extra.hop_aniso_bites
#print axioms LeanReal.L2_LIVRO_B4_Extra.witness_GB_strict_pos
#print axioms LeanReal.L2_LIVRO_B4_Extra.apply_GB_strict_pos
#print axioms LeanReal.L2_LIVRO_B4_Extra.witness_GB_strict_neg
#print axioms LeanReal.L2_LIVRO_B4_Extra.witness_several_planes_strict
#print axioms LeanReal.L2_LIVRO_B4_Extra.witness_fenchel_strict
#print axioms LeanReal.L2_LIVRO_B4_Extra.hFM_IsK3
#print axioms LeanReal.L2_LIVRO_B4_Extra.knotSet_IsK3_nonempty
#print axioms LeanReal.L2_LIVRO_B4_Extra.knot_gap_a_IsK3
#print axioms LeanReal.L2_LIVRO_B4_Extra.mutant_hFM_without_IsK_false
