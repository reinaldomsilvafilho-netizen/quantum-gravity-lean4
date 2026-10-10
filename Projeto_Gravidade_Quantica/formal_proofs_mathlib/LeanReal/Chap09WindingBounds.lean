import LeanReal.Chap09Winding
import Mathlib.Analysis.Real.Pi.Bounds

/-!
# Lote B8: cotas de enrolamento (cap. 9, `thm:loop_bounding`(1); cap. 8, estilingue)

## Parte 1. Capitulo 9, `thm:loop_bounding`, item (1)

Fonte: `unified_quantum_gravity_book/chap09_global_homotopy_covering_spaces_jordan_loops.tex`,
Proposicao "Finitely many classes under a length bound" (`thm:loop_bounding`), item (1):

> Every path `γ` in `F` from `p` to `q` of length at most `V` has winding numbers
> `|w_i(γ)| ≤ (V/ρ_i + |Δθ_i(γ₀)|)/2π`, where `θ_i = arg(· - c_i)` and `B(c_i, ρ_i) ⊂ int O_i`.

### Reducao declarada

* Um obstaculo de cada vez (o item vale para cada `i` separadamente): centro `c`, raio `ρ > 0`.
* `γ : ℝ → ℝ × ℝ` parametrizada por comprimento de arco em `[0,ℓ]`: `γ' = (cos φ, sin φ)` em
  `(0,ℓ)` (so derivabilidade; nenhuma hipotese de curvatura e usada, como no livro).
* "`γ` esta em `F`" entra apenas pelo que a prova usa: `γ` evita a bola aberta `B(c, ρ)`
  (`hfree : ρ² ≤ |γ - c|²` em `[0,ℓ]`).
* "`θ = arg(γ - c)` determinacao continua" e codificado como em `Chap09Winding`:
  `γ = c + r(cos θ, sin θ)` com `r > 0` (`hpolar`, `hr`), `θ` continua em `[0,ℓ]`.
* Hipotese NOMEADA `h_lift`: `θ` e derivavel em `(0,ℓ)` (para `γ` de classe `C¹` isso e
  consequencia da teoria de levantamentos, nao invocada aqui).
* Hipotese NOMEADA `h_winding : Δθ(γ) - Δθ(γ₀) = 2πw` (a identidade da prova do livro, que
  depende da teoria de homotopia do espaco livre e dos geradores `a_j`; nao formalizada).
* O item (2) (finitude das classes: Arzela-Ascoli e retrato de vizinhanca euclidiana) NAO e
  formalizado.

Prova: `r θ' = sin(φ - θ)` (`Chap09Winding.radial_identity`) da `|θ'| ≤ 1/r ≤ 1/ρ`; o teorema
do valor medio da `|Δθ(γ)| ≤ ℓ/ρ ≤ V/ρ`; desigualdade triangular.

## Parte 2. Capitulo 8, observacao apos `conj:slingshot` (estilingue relativistico planar)

Fonte: `unified_quantum_gravity_book/chap08_noneuclidean_minimax_relativity_adm.tex`, Remark
apos `conj:slingshot`:

> Along a future-directed timelike curve in the equatorial plane,
> `-f ṫ² + f⁻¹ ṙ² + r² φ̇² < 0` with `f = 1 - 2M/r`, so
> `|dφ/dt| < √f/r ≤ max_{r > 2M} √f/r = 1/(3√3 M)`, attained at `r = 3M`. ...
> a worldline of winding number `W` has `|φ_q - φ_p + 2πW| < Δt/(3√3 M)`, hence
> `|W| < Δt/(6√3 π M) + 1/2`. For `Δt = 100M` this gives `|W| ≤ 3`.

### Cobertura

* `orbital_rate_max`, `orbital_rate_max_attained`: o maximo `1/(3√3M)` e onde e atingido.
* `timelike_angular_rate`: a desigualdade pontual `|φ̇| < (√f/r)|ṫ|` (algebra).
* `angular_sweep_bound`: a integracao ao longo da linha de mundo, na forma NAO estrita
  `|Δφ| ≤ Δt/(3√3M)` (o livro escreve `<`; a forma estrita exigiria um argumento de
  compacidade a mais). Reducao: `t, φ` continuas em `[a,b]`, derivaveis em `(a,b)`, `ṫ > 0`
  (futuro), `r > 2M`; `r` e `ṙ` sao funcoes arbitrarias (so aparecem na condicao tipo-tempo).
  A identificacao de `Δφ` com `φ_q - φ_p + 2πW` (levantamento do angulo) NAO e formalizada.
* `winding_count_bound_strict` (forma do livro) e `winding_count_bound` (forma `≤`): a conta
  `|W| < Δt/(6√3πM) + 1/2`.
* `winding_le_three`: `Δt = 100M ⇒ |W| ≤ 3`.
-/

noncomputable section

namespace LeanReal.Chap09WindingBounds

open Set Real

/-! ## Parte 1: `thm:loop_bounding`(1) -/

/-- **Proposicao `thm:loop_bounding`, item (1)**, para um obstaculo, na reducao do cabecalho:
`|w| ≤ (V/ρ + |Δθ(γ₀)|)/2π`. Condicional as hipoteses nomeadas `h_lift` (o levantamento `θ` e
derivavel) e `h_winding` (`Δθ(γ) - Δθ(γ₀) = 2πw`). -/
theorem loop_bounding_winding (γ : ℝ → ℝ × ℝ) (c : ℝ × ℝ) (r θ θ' φ : ℝ → ℝ)
    (ℓ ρ V Δ₀ : ℝ) (w : ℤ) (hℓ : 0 ≤ ℓ) (hρ : 0 < ρ)
    (hγ : ∀ s ∈ Ioo 0 ℓ, HasDerivAt γ (cos (φ s), sin (φ s)) s)
    (hr : ∀ s ∈ Icc 0 ℓ, 0 < r s)
    (hpolar : ∀ s ∈ Icc 0 ℓ, γ s = (c.1 + r s * cos (θ s), c.2 + r s * sin (θ s)))
    (hθc : ContinuousOn θ (Icc 0 ℓ)) (h_lift : ∀ s ∈ Ioo 0 ℓ, HasDerivAt θ (θ' s) s)
    (hfree : ∀ s ∈ Icc 0 ℓ, ρ ^ 2 ≤ ((γ s).1 - c.1) ^ 2 + ((γ s).2 - c.2) ^ 2)
    (hV : ℓ ≤ V)
    (h_winding : (θ ℓ - θ 0) - Δ₀ = 2 * π * w) :
    |(w : ℝ)| ≤ (V / ρ + |Δ₀|) / (2 * π) := by
  -- |θ'| ≤ 1/ρ no interior
  have hder : ∀ s ∈ Ioo 0 ℓ, |θ' s| ≤ 1 / ρ := by
    intro s hs
    have hsI : s ∈ Icc 0 ℓ := Ioo_subset_Icc_self hs
    have hrad := LeanReal.Chap09Winding.radial_identity γ c r θ θ' φ ℓ s hs (hγ s hs)
      (h_lift s hs) hpolar
    have hrs := hr s hsI
    have hsq : ((γ s).1 - c.1) ^ 2 + ((γ s).2 - c.2) ^ 2 = r s ^ 2 := by
      rw [hpolar s hsI]
      dsimp only
      linear_combination (r s) ^ 2 * sin_sq_add_cos_sq (θ s)
    have hρr : ρ ≤ r s := by
      have h2 := hfree s hsI
      rw [hsq] at h2
      exact (pow_le_pow_iff_left₀ hρ.le hrs.le two_ne_zero).mp h2
    have hθ'r : |θ' s| * r s ≤ 1 := by
      have : |r s * θ' s| ≤ 1 := by rw [hrad]; exact abs_sin_le_one _
      rw [abs_mul, abs_of_pos hrs] at this
      linarith
    rw [le_div_iff₀ hρ]
    calc |θ' s| * ρ ≤ |θ' s| * r s := mul_le_mul_of_nonneg_left hρr (abs_nonneg _)
      _ ≤ 1 := hθ'r
  -- |Δθ(γ)| ≤ ℓ/ρ
  have hnet : |θ ℓ - θ 0| ≤ ℓ / ρ := by
    rcases hℓ.eq_or_lt with h0 | hpos
    · rw [← h0]; simp
    · obtain ⟨x, hx, hslope⟩ := exists_hasDerivAt_eq_slope θ θ' hpos hθc h_lift
      have : θ ℓ - θ 0 = θ' x * ℓ := by
        rw [hslope, sub_zero]; field_simp
      rw [this, abs_mul, abs_of_pos hpos, div_eq_mul_one_div ℓ ρ, mul_comm ℓ]
      exact mul_le_mul_of_nonneg_right (hder x hx) hpos.le
  have hVρ : ℓ / ρ ≤ V / ρ := div_le_div_of_nonneg_right hV hρ.le
  have hw : 2 * π * |(w : ℝ)| = |(θ ℓ - θ 0) - Δ₀| := by
    rw [h_winding, abs_mul, abs_of_pos (by positivity : (0:ℝ) < 2 * π)]
  have htri : |(θ ℓ - θ 0) - Δ₀| ≤ |θ ℓ - θ 0| + |Δ₀| := abs_sub _ _
  rw [le_div_iff₀ (by positivity : (0:ℝ) < 2 * π)]
  linarith

/-! ### Testemunha: a circunferencia unitaria percorrida uma vez (`w = 1`), com igualdade -/

/-- A circunferencia `s ↦ (cos s, sin s)` em torno de `c = 0`. -/
def circ (s : ℝ) : ℝ × ℝ := (cos s, sin s)

/-- A circunferencia satisfaz todas as hipoteses de `loop_bounding_winding` com `c = 0`,
`r = 1`, `θ = id`, `θ' = 1`, `φ = id + π/2`, `ℓ = V = 2π`, `ρ = 1`, `Δ₀ = 0` (laco de
referencia constante), `w = 1`. -/
theorem circ_hyps :
    (∀ s ∈ Ioo 0 (2 * π), HasDerivAt circ (cos (s + π / 2), sin (s + π / 2)) s) ∧
    (∀ s ∈ Icc 0 (2 * π), circ s = ((0 : ℝ × ℝ).1 + 1 * cos (id s), (0 : ℝ × ℝ).2 + 1 * sin (id s))) ∧
    (∀ s ∈ Icc 0 (2 * π), (1 : ℝ) ^ 2 ≤ ((circ s).1 - (0 : ℝ × ℝ).1) ^ 2 +
      ((circ s).2 - (0 : ℝ × ℝ).2) ^ 2) ∧
    (id (2 * π) - id 0) - 0 = 2 * π * ((1 : ℤ) : ℝ) := by
  refine ⟨fun s _ => ?_, fun s _ => by simp [circ], fun s _ => ?_, by simp⟩
  · have := (hasDerivAt_cos s).prodMk (hasDerivAt_sin s)
    rw [cos_add_pi_div_two, sin_add_pi_div_two]
    exact this
  · simp only [circ, Prod.fst_zero, Prod.snd_zero, sub_zero]
    nlinarith [sin_sq_add_cos_sq s]

/-- **Testemunha de nao vacuidade** (com igualdade `1 ≤ 1`): o teorema aplicado a
circunferencia. As hipoteses mordem: com `ρ` maior, ou `V` menor, a conclusao falha (mutantes). -/
theorem witness_circle : |((1 : ℤ) : ℝ)| ≤ (2 * π / 1 + |(0:ℝ)|) / (2 * π) := by
  obtain ⟨h1, h2, h3, h4⟩ := circ_hyps
  exact loop_bounding_winding circ 0 (fun _ => 1) id (fun _ => 1) (fun s => s + π / 2)
    (2 * π) 1 (2 * π) 0 1 (by positivity) one_pos h1 (fun _ _ => one_pos) h2
    continuousOn_id (fun s _ => hasDerivAt_id s) h3 le_rfl h4

/-- A cota e atingida na testemunha: `(2π/1 + 0)/(2π) = 1 = |w|`. -/
theorem witness_circle_equality : (2 * π / 1 + |(0:ℝ)|) / (2 * π) = |((1 : ℤ) : ℝ)| := by
  have : (2 * π) ≠ 0 := by positivity
  simp [this]

/-! ### Mutantes provados falsos -/

/-- Enunciado (parametrizado pelo raio usado na cota) para os mutantes. -/
def LoopBoundWith (ρ V : ℝ) (strict : Bool) : Prop :=
  ∀ (γ : ℝ → ℝ × ℝ) (c : ℝ × ℝ) (r θ θ' φ : ℝ → ℝ) (ℓ Δ₀ : ℝ) (w : ℤ), 0 ≤ ℓ →
    (∀ s ∈ Ioo 0 ℓ, HasDerivAt γ (cos (φ s), sin (φ s)) s) →
    (∀ s ∈ Icc 0 ℓ, 0 < r s) →
    (∀ s ∈ Icc 0 ℓ, γ s = (c.1 + r s * cos (θ s), c.2 + r s * sin (θ s))) →
    ContinuousOn θ (Icc 0 ℓ) → (∀ s ∈ Ioo 0 ℓ, HasDerivAt θ (θ' s) s) →
    (∀ s ∈ Icc 0 ℓ, 1 ≤ ((γ s).1 - c.1) ^ 2 + ((γ s).2 - c.2) ^ 2) →
    ℓ = 2 * π →
    (θ ℓ - θ 0) - Δ₀ = 2 * π * w →
    if strict then |(w : ℝ)| < (V / ρ + |Δ₀|) / (2 * π)
    else |(w : ℝ)| ≤ (V / ρ + |Δ₀|) / (2 * π)

theorem circ_instance (ρ V : ℝ) (strict : Bool) (h : LoopBoundWith ρ V strict) :
    if strict then |((1:ℤ) : ℝ)| < (V / ρ + |(0:ℝ)|) / (2 * π)
    else |((1:ℤ) : ℝ)| ≤ (V / ρ + |(0:ℝ)|) / (2 * π) := by
  obtain ⟨h1, h2, h3, h4⟩ := circ_hyps
  exact h circ 0 (fun _ => 1) id (fun _ => 1) (fun s => s + π / 2) (2 * π) 0 1 (by positivity)
    h1 (fun _ _ => one_pos) h2 continuousOn_id (fun s _ => hasDerivAt_id s)
    (by simpa using h3) rfl h4

/-- Mutante 1 (conclusao estrita): FALSO, a circunferencia atinge a cota. -/
theorem mutant_strict_false : ¬ LoopBoundWith 1 (2 * π) true := by
  intro h
  have := circ_instance 1 (2 * π) true h
  simp only [↓reduceIte] at this
  rw [witness_circle_equality] at this
  exact lt_irrefl _ this

/-- Mutante 2 (sem a hipotese `hfree` de que `γ` evita `B(c,ρ)`: a cota usada com `ρ = 2`
para uma curva a distancia `1` de `c`): FALSO, daria `1 ≤ 1/2`. -/
theorem mutant_no_free_false : ¬ LoopBoundWith 2 (2 * π) false := by
  intro h
  have := circ_instance 2 (2 * π) false h
  simp only [Bool.false_eq_true, ↓reduceIte] at this
  have e : (2 * π / 2 + |(0:ℝ)|) / (2 * π) = 1 / 2 := by
    have : π ≠ 0 := pi_ne_zero
    rw [abs_zero, add_zero]; field_simp
  rw [e] at this
  norm_num at this

/-- Mutante 3 (sem a cota de comprimento `ℓ ≤ V`: a cota usada com `V = π < ℓ = 2π`): FALSO,
daria `1 ≤ 1/2`. -/
theorem mutant_no_length_false : ¬ LoopBoundWith 1 π false := by
  intro h
  have := circ_instance 1 π false h
  simp only [Bool.false_eq_true, ↓reduceIte] at this
  have e : (π / 1 + |(0:ℝ)|) / (2 * π) = 1 / 2 := by
    have : π ≠ 0 := pi_ne_zero
    rw [abs_zero, add_zero]; field_simp
  rw [e] at this
  norm_num at this

/-! ## Parte 2: as contas do estilingue (cap. 8) -/

/-- **`max_{r > 2M} √(1 - 2M/r)/r = 1/(3√3M)`**, parte "`≤`" (Remark apos `conj:slingshot`). -/
theorem orbital_rate_max (M r : ℝ) (hM : 0 < M) (hr : 2 * M < r) :
    √(1 - 2 * M / r) / r ≤ 1 / (3 * √3 * M) := by
  have hr0 : 0 < r := by linarith
  have h3 : (0:ℝ) < √3 := by positivity
  have hs3 : √3 ^ 2 = 3 := sq_sqrt (by norm_num)
  rw [div_le_iff₀ hr0]
  rw [show 1 / (3 * √3 * M) * r = r / (3 * √3 * M) by ring]
  apply Real.sqrt_le_iff.mpr
  refine ⟨by positivity, ?_⟩
  rw [div_pow, mul_pow, mul_pow, hs3, sub_le_iff_le_add]
  -- 1 ≤ r²/(27M²) + 2M/r, i.e. (r - 3M)²(r + 6M) ≥ 0
  have hp : 0 < r + 6 * M := by linarith
  have key : 0 ≤ (r - 3 * M) ^ 2 * (r + 6 * M) / (27 * M ^ 2 * r) :=
    div_nonneg (mul_nonneg (sq_nonneg _) hp.le) (by positivity)
  have e : r ^ 2 / (3 ^ 2 * 3 * M ^ 2) + 2 * M / r - 1 =
      (r - 3 * M) ^ 2 * (r + 6 * M) / (27 * M ^ 2 * r) := by
    field_simp; ring
  linarith

/-- O maximo e atingido em `r = 3M` (Remark apos `conj:slingshot`). -/
theorem orbital_rate_max_attained (M : ℝ) (hM : 0 < M) :
    √(1 - 2 * M / (3 * M)) / (3 * M) = 1 / (3 * √3 * M) := by
  have h : 1 - 2 * M / (3 * M) = 1 / 3 := by field_simp; ring
  rw [h, sqrt_div' 1 (by norm_num : (0:ℝ) ≤ 3), sqrt_one]
  have : √3 ≠ 0 := by positivity
  field_simp

/-- **Condicao tipo-tempo, pontual**: `-f ṫ² + f⁻¹ ṙ² + r² φ̇² < 0`, `f > 0`, `r > 0` ⇒
`|φ̇| < (√f/r)|ṫ|` (Remark apos `conj:slingshot`). -/
theorem timelike_angular_rate (f r T R P : ℝ) (hf : 0 < f) (hr : 0 < r)
    (htl : -f * T ^ 2 + R ^ 2 / f + r ^ 2 * P ^ 2 < 0) :
    |P| < √f / r * |T| := by
  have hR : 0 ≤ R ^ 2 / f := by positivity
  have h1 : (r * |P|) ^ 2 < f * T ^ 2 := by rw [mul_pow, sq_abs]; linarith
  have h2 : r * |P| < √(f * T ^ 2) := Real.lt_sqrt (by positivity) |>.mpr h1
  rw [sqrt_mul hf.le, sqrt_sq_eq_abs] at h2
  rw [div_mul_eq_mul_div, lt_div_iff₀ hr]
  linarith

/-- **Integracao ao longo da linha de mundo** (forma nao estrita): `|Δφ| ≤ Δt/(3√3M)` para
uma curva tipo-tempo, orientada para o futuro (`ṫ > 0`), no plano equatorial, com `r > 2M`. -/
theorem angular_sweep_bound (M a b : ℝ) (t φ ρ t' φ' ρ' : ℝ → ℝ) (hM : 0 < M) (hab : a ≤ b)
    (htc : ContinuousOn t (Icc a b)) (hφc : ContinuousOn φ (Icc a b))
    (ht : ∀ s ∈ Ioo a b, HasDerivAt t (t' s) s) (hφ : ∀ s ∈ Ioo a b, HasDerivAt φ (φ' s) s)
    (hρ : ∀ s ∈ Ioo a b, 2 * M < ρ s)
    (hfut : ∀ s ∈ Ioo a b, 0 < t' s)
    (htl : ∀ s ∈ Ioo a b, -(1 - 2 * M / ρ s) * t' s ^ 2 + ρ' s ^ 2 / (1 - 2 * M / ρ s) +
      ρ s ^ 2 * φ' s ^ 2 < 0) :
    |φ b - φ a| ≤ (t b - t a) / (3 * √3 * M) := by
  set K := 1 / (3 * √3 * M) with hK
  have hpt : ∀ s ∈ Ioo a b, |φ' s| ≤ K * t' s := by
    intro s hs
    have hρ0 : 0 < ρ s := by linarith [hρ s hs]
    have hf : 0 < 1 - 2 * M / ρ s := by
      rw [sub_pos, div_lt_one hρ0]; exact hρ s hs
    have h1 := timelike_angular_rate _ _ _ _ _ hf hρ0 (htl s hs)
    rw [abs_of_pos (hfut s hs)] at h1
    have h2 := orbital_rate_max M (ρ s) hM (hρ s hs)
    nlinarith [hfut s hs]
  have mono : ∀ σ : ℝ, σ = 1 ∨ σ = -1 → σ * (φ b - φ a) ≤ K * (t b - t a) := by
    intro σ hσ
    have hmon : MonotoneOn (fun s => K * t s - σ * φ s) (Icc a b) := by
      refine monotoneOn_of_hasDerivWithinAt_nonneg (f' := fun s => K * t' s - σ * φ' s)
        (convex_Icc a b) ((htc.const_smul K).sub (hφc.const_smul σ)) ?_ ?_
      · intro s hs
        rw [interior_Icc] at hs
        exact (((ht s hs).const_mul K).sub ((hφ s hs).const_mul σ)).hasDerivWithinAt
      · intro s hs
        rw [interior_Icc] at hs
        have := hpt s hs
        rcases hσ with rfl | rfl
        · have := le_abs_self (φ' s); show 0 ≤ K * t' s - (1:ℝ) * φ' s; linarith
        · have := neg_abs_le (φ' s); show 0 ≤ K * t' s - (-1:ℝ) * φ' s; linarith
    have := hmon ⟨le_rfl, hab⟩ ⟨hab, le_rfl⟩ hab
    simp only at this
    linarith
  have hp := mono 1 (Or.inl rfl)
  have hn := mono (-1) (Or.inr rfl)
  rw [abs_le]
  have : K * (t b - t a) = (t b - t a) / (3 * √3 * M) := by rw [hK]; ring
  constructor <;> linarith

/-- **Conta do numero de voltas** (forma do livro, estrita): se `Δφ₀ ∈ (-π, π]` e
`|Δφ₀ + 2πW| < Δt/(3√3M)`, entao `|W| < Δt/(6√3πM) + 1/2`. -/
theorem winding_count_bound_strict (M Δt Δφ₀ : ℝ) (W : ℤ) (hM : 0 < M)
    (hφ₀ : Δφ₀ ∈ Ioc (-π) π) (h : |Δφ₀ + 2 * π * W| < Δt / (3 * √3 * M)) :
    |(W : ℝ)| < Δt / (6 * √3 * π * M) + 1 / 2 := by
  have h0 : |Δφ₀| ≤ π := abs_le.mpr ⟨hφ₀.1.le, hφ₀.2⟩
  have htri : 2 * π * |(W : ℝ)| ≤ |Δφ₀ + 2 * π * W| + |Δφ₀| := by
    have e1 : 2 * π * |(W : ℝ)| = |(Δφ₀ + 2 * π * W) - Δφ₀| := by
      rw [add_sub_cancel_left, abs_mul, abs_of_pos (by positivity : (0:ℝ) < 2 * π)]
    rw [e1]
    exact abs_sub _ _
  have hpos : (0:ℝ) < 2 * π := by positivity
  have e : Δt / (6 * √3 * π * M) + 1 / 2 = (Δt / (3 * √3 * M) + π) / (2 * π) := by
    have : √3 ≠ 0 := by positivity
    have : M ≠ 0 := hM.ne'
    have : π ≠ 0 := pi_ne_zero
    field_simp; ring
  rw [e, lt_div_iff₀ hpos]
  linarith

/-- A mesma conta na forma nao estrita (a que `angular_sweep_bound` fornece). -/
theorem winding_count_bound (M Δt Δφ₀ : ℝ) (W : ℤ) (hM : 0 < M)
    (hφ₀ : Δφ₀ ∈ Ioc (-π) π) (h : |Δφ₀ + 2 * π * W| ≤ Δt / (3 * √3 * M)) :
    |(W : ℝ)| ≤ Δt / (6 * √3 * π * M) + 1 / 2 := by
  have h0 : |Δφ₀| ≤ π := abs_le.mpr ⟨hφ₀.1.le, hφ₀.2⟩
  have htri : 2 * π * |(W : ℝ)| ≤ |Δφ₀ + 2 * π * W| + |Δφ₀| := by
    have e1 : 2 * π * |(W : ℝ)| = |(Δφ₀ + 2 * π * W) - Δφ₀| := by
      rw [add_sub_cancel_left, abs_mul, abs_of_pos (by positivity : (0:ℝ) < 2 * π)]
    rw [e1]
    exact abs_sub _ _
  have hpos : (0:ℝ) < 2 * π := by positivity
  have e : Δt / (6 * √3 * π * M) + 1 / 2 = (Δt / (3 * √3 * M) + π) / (2 * π) := by
    have : √3 ≠ 0 := by positivity
    have : M ≠ 0 := hM.ne'
    have : π ≠ 0 := pi_ne_zero
    field_simp; ring
  rw [e, le_div_iff₀ hpos]
  linarith

/-- `100/(6√3π) + 1/2 < 4`. -/
theorem hundred_bound : (100 : ℝ) / (6 * √3 * π) + 1 / 2 < 4 := by
  have h3 : (1.732 : ℝ) < √3 := by
    rw [Real.lt_sqrt (by norm_num)]; norm_num
  have hπ : (3.14 : ℝ) < π := pi_gt_d2
  have hden : (0:ℝ) < 6 * √3 * π := by positivity
  rw [← lt_sub_iff_add_lt, div_lt_iff₀ hden]
  nlinarith [mul_lt_mul'' h3 hπ (by norm_num) (by norm_num)]

/-- **`Δt = 100M ⇒ |W| ≤ 3`** (Remark apos `conj:slingshot`), a partir da forma nao estrita
(a estrita implica a nao estrita). -/
theorem winding_le_three (M Δφ₀ : ℝ) (W : ℤ) (hM : 0 < M) (hφ₀ : Δφ₀ ∈ Ioc (-π) π)
    (h : |Δφ₀ + 2 * π * W| ≤ 100 * M / (3 * √3 * M)) : |W| ≤ 3 := by
  have h1 := winding_count_bound M (100 * M) Δφ₀ W hM hφ₀ h
  have e : 100 * M / (6 * √3 * π * M) = 100 / (6 * √3 * π) := by
    have : M ≠ 0 := hM.ne'
    field_simp
  rw [e] at h1
  have h2 : |(W : ℝ)| < 4 := lt_of_le_of_lt h1 hundred_bound
  have h3 : |W| < 4 := by exact_mod_cast h2
  omega

/-! ### Testemunhas e mutantes das contas do estilingue -/

/-- `18√3π < 100`, i.e. `6π < 100/(3√3)`: a classe `W = 3` NAO e excluida pela conta. -/
theorem three_allowed : |(0:ℝ) + 2 * π * ((3:ℤ):ℝ)| < 100 * 1 / (3 * √3 * 1) := by
  have h3 : √3 < (1.7321 : ℝ) := by
    rw [Real.sqrt_lt' (by norm_num)]; norm_num
  have hπ : π < (3.1416 : ℝ) := pi_lt_d4
  have hs0 : (0:ℝ) < √3 := by positivity
  rw [abs_of_pos (by push_cast; positivity), lt_div_iff₀ (by positivity)]
  push_cast
  nlinarith [mul_lt_mul'' h3 hπ hs0.le pi_pos.le]

/-- Mutante (a cota do livro nao pode ser melhorada para `|W| ≤ 2` com `Δt = 100M`): FALSO,
`W = 3`, `Δφ₀ = 0`, `M = 1` satisfaz a hipotese ESTRITA. -/
theorem mutant_le_two_false :
    ¬ (∀ (M Δφ₀ : ℝ) (W : ℤ), 0 < M → Δφ₀ ∈ Ioc (-π) π →
        |Δφ₀ + 2 * π * W| < 100 * M / (3 * √3 * M) → |W| ≤ 2) := by
  intro h
  have := h 1 0 3 one_pos ⟨by linarith [pi_pos], pi_pos.le⟩ three_allowed
  norm_num at this

/-- Mutante (maximo `1/(6M)` em vez de `1/(3√3M)`): FALSO em `r = 3M`, pois `3√3 < 6`. -/
theorem mutant_rate_sixM_false :
    ¬ (∀ M r : ℝ, 0 < M → 2 * M < r → √(1 - 2 * M / r) / r ≤ 1 / (6 * M)) := by
  intro h
  have h1 := h 1 3 one_pos (by norm_num)
  have h2 := orbital_rate_max_attained 1 one_pos
  norm_num at h1 h2
  rw [h2] at h1
  have h3 : √3 < 2 := by rw [Real.sqrt_lt' (by norm_num)]; norm_num
  have hs : 0 < √3 := by positivity
  have hinv : √3 * (√3)⁻¹ = 1 := mul_inv_cancel₀ hs.ne'
  have hip : 0 < (√3)⁻¹ := inv_pos.mpr hs
  nlinarith [mul_le_mul_of_nonneg_left h1 hs.le]

/-- Mutante (maximo ESTRITO para todo `r > 2M`): FALSO, a igualdade vale em `r = 3M`. -/
theorem mutant_rate_strict_false :
    ¬ (∀ M r : ℝ, 0 < M → 2 * M < r → √(1 - 2 * M / r) / r < 1 / (3 * √3 * M)) := by
  intro h
  have h1 := h 1 (3 * 1) one_pos (by norm_num)
  rw [orbital_rate_max_attained 1 one_pos] at h1
  exact lt_irrefl _ h1

/-- **Testemunha nao degenerada de `angular_sweep_bound`**: a linha de mundo circular
`r = 3`, `t = s`, `φ = s/10`, `M = 1`, em `[0,1]`: e tipo-tempo (`-1/3 + 9/100 < 0`) e gira
(`Δφ = 1/10 ≠ 0`). -/
theorem witness_sweep :
    |(fun s : ℝ => s / 10) 1 - (fun s : ℝ => s / 10) 0| ≤ ((id 1 : ℝ) - id 0) / (3 * √3 * 1) := by
  refine angular_sweep_bound 1 0 1 id (fun s => s / 10) (fun _ => 3) (fun _ => 1)
    (fun _ => 1 / 10) (fun _ => 0) one_pos zero_le_one continuousOn_id
    (continuous_id.div_const 10).continuousOn (fun s _ => hasDerivAt_id s)
    (fun s _ => by simpa using (hasDerivAt_id s).div_const 10) (fun _ _ => by norm_num)
    (fun _ _ => one_pos) (fun _ _ => by norm_num)

/-- Mutante (constante `1/(6M)` no lugar de `1/(3√3M)` na integracao): FALSO, pela linha de
mundo circular `r = 3`, `M = 1`, `φ̇ = 9/50 > 1/6`, ainda tipo-tempo (`-1/3 + 729/2500 < 0`). -/
theorem mutant_sweep_sixM_false :
    ¬ (∀ (M a b : ℝ) (t φ ρ t' φ' ρ' : ℝ → ℝ), 0 < M → a ≤ b →
        ContinuousOn t (Icc a b) → ContinuousOn φ (Icc a b) →
        (∀ s ∈ Ioo a b, HasDerivAt t (t' s) s) → (∀ s ∈ Ioo a b, HasDerivAt φ (φ' s) s) →
        (∀ s ∈ Ioo a b, 2 * M < ρ s) → (∀ s ∈ Ioo a b, 0 < t' s) →
        (∀ s ∈ Ioo a b, -(1 - 2 * M / ρ s) * t' s ^ 2 + ρ' s ^ 2 / (1 - 2 * M / ρ s) +
          ρ s ^ 2 * φ' s ^ 2 < 0) →
        |φ b - φ a| ≤ (t b - t a) / (6 * M)) := by
  intro h
  have := h 1 0 1 id (fun s => 9 * s / 50) (fun _ => 3) (fun _ => 1) (fun _ => 9 / 50)
    (fun _ => 0) one_pos zero_le_one continuousOn_id
    ((continuous_const.mul continuous_id).div_const 50).continuousOn
    (fun s _ => hasDerivAt_id s)
    (fun s _ => by simpa using ((hasDerivAt_id s).const_mul 9).div_const 50)
    (fun _ _ => by norm_num) (fun _ _ => one_pos) (fun _ _ => by norm_num)
  norm_num at this

end LeanReal.Chap09WindingBounds

#print axioms LeanReal.Chap09WindingBounds.loop_bounding_winding
#print axioms LeanReal.Chap09WindingBounds.circ_hyps
#print axioms LeanReal.Chap09WindingBounds.witness_circle
#print axioms LeanReal.Chap09WindingBounds.witness_circle_equality
#print axioms LeanReal.Chap09WindingBounds.mutant_strict_false
#print axioms LeanReal.Chap09WindingBounds.mutant_no_free_false
#print axioms LeanReal.Chap09WindingBounds.mutant_no_length_false
#print axioms LeanReal.Chap09WindingBounds.orbital_rate_max
#print axioms LeanReal.Chap09WindingBounds.orbital_rate_max_attained
#print axioms LeanReal.Chap09WindingBounds.timelike_angular_rate
#print axioms LeanReal.Chap09WindingBounds.angular_sweep_bound
#print axioms LeanReal.Chap09WindingBounds.winding_count_bound_strict
#print axioms LeanReal.Chap09WindingBounds.winding_count_bound
#print axioms LeanReal.Chap09WindingBounds.hundred_bound
#print axioms LeanReal.Chap09WindingBounds.winding_le_three
#print axioms LeanReal.Chap09WindingBounds.three_allowed
#print axioms LeanReal.Chap09WindingBounds.mutant_le_two_false
#print axioms LeanReal.Chap09WindingBounds.mutant_rate_sixM_false
#print axioms LeanReal.Chap09WindingBounds.mutant_rate_strict_false
#print axioms LeanReal.Chap09WindingBounds.witness_sweep
#print axioms LeanReal.Chap09WindingBounds.mutant_sweep_sixM_false
