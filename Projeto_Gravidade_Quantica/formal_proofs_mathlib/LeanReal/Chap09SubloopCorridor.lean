import LeanReal.Chap08UTurn

/-!
# Capitulo 9, `prop:subloop` e `prop:corridor_gap` (lote B2 do `PLANO_LIVRO_B.md`)

Fonte: `unified_quantum_gravity_book/chap09_global_homotopy_covering_spaces_jordan_loops.tex`.

* `prop:subloop` ("Confinement of closed sub-loops"): `γ` plana `C^{1,1}` com `|κ| ≤ K` q.t.p.,
  `K > 0`, e `γ(a) = γ(b)`, `a < b`. Entao `γ([a,b])` tem largura `≥ 2/K` em alguma direcao, logo
  diametro `≥ 2/K`; uma curva em `Ω̄` com sub-laco fechado tem `‖κ‖_∞ ≥ 2/diam Ω`.
* `prop:corridor_gap` ("No curvature gap in the benchmark"): no canal
  `Ω_H = {|y| ≤ H} \ B_{R₀}(0)`, `R₀ = 1`, `H = 1.62`, todo caminho admissivel tem
  `‖κ‖_∞ ≥ 1/H`; o valor e atingido pelas construcoes (semicirculos de raio `H`).

## Reducao declarada (a de `Chap08UTurn` / `Chap09MouthHalfturn`)

* Angulo tangente `φ` continuo em `[a,b]`, DIFERENCIAVEL em `(a,b)`, `|φ'| ≤ K` em `(a,b)`;
  `γ' = (cos φ, sin φ)` em `(a,b)`. O caso Lipschitz (`C^{1,1}`, cota q.t.p.) NAO esta coberto.
* `prop:subloop`: o passo "`∫T = 0` ⇒ amplitude de `φ` ≥ `π`" e feito sem integrais: se a
  amplitude fosse `< π`, a projecao de `γ` na direcao media seria estritamente crescente,
  contra `γ(a) = γ(b)`. Depois, `Chap08UTurn.rise_abs` (selecao + `mouth_halfturn` girado).
  "Largura na direcao `e`" = `|⟨γ(s₂) - γ(s₁), e⟩|` para dois pontos do laco, `e = (-sin c, cos c)`.
* `prop:corridor_gap`: a cota inferior e `Chap08UTurn.uturn_strip` na faixa `[-H, H]`. As
  construcoes formalizadas sao SO os arcos (o semicirculo de raio `H` centrado em `(-c,0)`,
  `c > H + 1`, e o centrado na origem, e a circunferencia completa de raio `H`): ficam na faixa,
  fora de `B̄₁(0)`, com curvatura `1/H`. NAO formalizados: os segmentos de entrada e saida e a
  colagem `C^{1,1}`, a classe de homotopia `w`, o mergulho, a cota de comprimento `V`.
-/

noncomputable section

namespace LeanReal.Chap09SubloopCorridor

open Set Real LeanReal.Chap08UTurn

/-! ## `prop:subloop` -/

/-- Num laco fechado (`γ(a) = γ(b)`, `a < b`) o angulo tangente varia pelo menos `π`. Prova sem
integrais: se `φ([a,b])` coubesse num intervalo de comprimento `< π`, a projecao de `γ` na
direcao media teria derivada `cos(φ - c) > 0`. -/
theorem exists_turn_of_loop (γ : ℝ → ℝ × ℝ) (φ : ℝ → ℝ) (a b : ℝ) (hab : a < b)
    (hγc : ContinuousOn γ (Icc a b))
    (hγ : ∀ s ∈ Ioo a b, HasDerivAt γ (cos (φ s), sin (φ s)) s)
    (hφc : ContinuousOn φ (Icc a b)) (hloop : γ a = γ b) :
    ∃ s ∈ Icc a b, ∃ t ∈ Icc a b, π ≤ |φ t - φ s| := by
  by_contra hcon0
  have hcon : ∀ s ∈ Icc a b, ∀ t ∈ Icc a b, |φ t - φ s| < π :=
    fun s hs t ht => lt_of_not_ge (fun h => hcon0 ⟨s, hs, t, ht, h⟩)
  have hne : (Icc a b).Nonempty := nonempty_Icc.2 hab.le
  obtain ⟨x₀, hx₀, hmin⟩ := isCompact_Icc.exists_isMinOn hne hφc
  obtain ⟨x₁, hx₁, hmax⟩ := isCompact_Icc.exists_isMaxOn hne hφc
  have hMm : φ x₁ - φ x₀ < π := (le_abs_self _).trans_lt (hcon x₀ hx₀ x₁ hx₁)
  set c := (φ x₀ + φ x₁) / 2 with hc
  set f : ℝ → ℝ := fun u => (rotCLM c (γ u)).1 with hf
  have hmono : StrictMonoOn f (Icc a b) := by
    refine strictMonoOn_of_hasDerivWithinAt_pos (f' := fun u => cos (φ u - c)) (convex_Icc a b)
      ((continuous_fst.comp (rotCLM c).continuous).comp_continuousOn hγc) ?_ ?_
    · intro u hu
      rw [interior_Icc] at hu
      have h2 := (rotCLM c).hasFDerivAt.comp_hasDerivAt u (hγ u hu)
      rw [rotCLM_dir] at h2
      have h3 := (ContinuousLinearMap.fst ℝ ℝ ℝ).hasFDerivAt.comp_hasDerivAt u h2
      simp only [ContinuousLinearMap.coe_fst'] at h3
      exact h3.hasDerivWithinAt
    · intro u hu
      rw [interior_Icc] at hu
      have hu' : u ∈ Icc a b := Ioo_subset_Icc_self hu
      have h1 : φ x₀ ≤ φ u := hmin hu'
      have h2 : φ u ≤ φ x₁ := hmax hu'
      exact cos_pos_of_mem_Ioo ⟨by rw [hc]; linarith, by rw [hc]; linarith⟩
  have := hmono ⟨le_rfl, hab.le⟩ ⟨hab.le, le_rfl⟩ hab
  simp only [hf, hloop] at this
  exact lt_irrefl _ this

/-- Versao de `rise_abs` para um subintervalo `[p,q] ⊂ [a,b]`. -/
theorem rise_abs_sub (γ : ℝ → ℝ × ℝ) (φ φ' : ℝ → ℝ) (a b p q K : ℝ) (hap : a ≤ p) (hpq : p ≤ q)
    (hqb : q ≤ b) (hγc : ContinuousOn γ (Icc a b))
    (hγ : ∀ s ∈ Ioo a b, HasDerivAt γ (cos (φ s), sin (φ s)) s)
    (hφc : ContinuousOn φ (Icc a b)) (hφ : ∀ s ∈ Ioo a b, HasDerivAt φ (φ' s) s)
    (hK : ∀ s ∈ Ioo a b, |φ' s| ≤ K) (hturn : π ≤ |φ q - φ p|) :
    ∃ s₁ ∈ Icc a b, ∃ s₂ ∈ Icc a b, 2 ≤ K * |rotY (φ p) (γ s₂ - γ s₁)| := by
  have hI : Icc p q ⊆ Icc a b := Icc_subset_Icc hap hqb
  have hO : Ioo p q ⊆ Ioo a b := Ioo_subset_Ioo hap hqb
  obtain ⟨s₁, hs₁, s₂, hs₂, h⟩ := rise_abs γ φ φ' p q K hpq (hγc.mono hI)
    (fun s hs => hγ s (hO hs)) (hφc.mono hI) (fun s hs => hφ s (hO hs))
    (fun s hs => hK s (hO hs)) hturn
  exact ⟨s₁, hI hs₁, s₂, hI hs₂, h⟩

/-- **Proposicao `prop:subloop`** (largura), na reducao do cabecalho: um sub-laco fechado com
`|κ| ≤ K` tem, numa direcao unitaria `e = (-sin c, cos c)`, dois pontos com
`K·|⟨γ(s₂) - γ(s₁), e⟩| ≥ 2`, isto e, largura `≥ 2/K` nessa direcao. -/
theorem subloop_width (γ : ℝ → ℝ × ℝ) (φ φ' : ℝ → ℝ) (a b K : ℝ) (hab : a < b)
    (hγc : ContinuousOn γ (Icc a b))
    (hγ : ∀ s ∈ Ioo a b, HasDerivAt γ (cos (φ s), sin (φ s)) s)
    (hφc : ContinuousOn φ (Icc a b)) (hφ : ∀ s ∈ Ioo a b, HasDerivAt φ (φ' s) s)
    (hK : ∀ s ∈ Ioo a b, |φ' s| ≤ K) (hloop : γ a = γ b) :
    ∃ c : ℝ, ∃ s₁ ∈ Icc a b, ∃ s₂ ∈ Icc a b, 2 ≤ K * |rotY c (γ s₂ - γ s₁)| := by
  obtain ⟨s, hs, t, ht, hst⟩ := exists_turn_of_loop γ φ a b hab hγc hγ hφc hloop
  rcases le_total s t with h | h
  · exact ⟨φ s, rise_abs_sub γ φ φ' a b s t K hs.1 h ht.2 hγc hγ hφc hφ hK hst⟩
  · rw [abs_sub_comm] at hst
    exact ⟨φ t, rise_abs_sub γ φ φ' a b t s K ht.1 h hs.2 hγc hγ hφc hφ hK hst⟩

/-- **`prop:subloop`** (diametro): para `K > 0`, ha dois pontos do laco a distancia euclidiana
`≥ 2/K`. -/
theorem subloop_diam (γ : ℝ → ℝ × ℝ) (φ φ' : ℝ → ℝ) (a b K : ℝ) (hab : a < b) (hKpos : 0 < K)
    (hγc : ContinuousOn γ (Icc a b))
    (hγ : ∀ s ∈ Ioo a b, HasDerivAt γ (cos (φ s), sin (φ s)) s)
    (hφc : ContinuousOn φ (Icc a b)) (hφ : ∀ s ∈ Ioo a b, HasDerivAt φ (φ' s) s)
    (hK : ∀ s ∈ Ioo a b, |φ' s| ≤ K) (hloop : γ a = γ b) :
    ∃ s₁ ∈ Icc a b, ∃ s₂ ∈ Icc a b,
      2 / K ≤ √(((γ s₂).1 - (γ s₁).1) ^ 2 + ((γ s₂).2 - (γ s₁).2) ^ 2) := by
  obtain ⟨c, s₁, hs₁, s₂, hs₂, h⟩ := subloop_width γ φ φ' a b K hab hγc hγ hφc hφ hK hloop
  refine ⟨s₁, hs₁, s₂, hs₂, ?_⟩
  have := abs_rotY_le c (γ s₂ - γ s₁)
  simp only [Prod.fst_sub, Prod.snd_sub] at this
  rw [div_le_iff₀ hKpos]
  nlinarith

/-- **`prop:subloop`, "in particular"**: se o laco fica num conjunto de diametro euclidiano
`≤ D`, entao `2 ≤ K D`, isto e, `‖κ‖_∞ ≥ 2/D`. -/
theorem subloop_domain (γ : ℝ → ℝ × ℝ) (φ φ' : ℝ → ℝ) (a b K D : ℝ) (hab : a < b)
    (hγc : ContinuousOn γ (Icc a b))
    (hγ : ∀ s ∈ Ioo a b, HasDerivAt γ (cos (φ s), sin (φ s)) s)
    (hφc : ContinuousOn φ (Icc a b)) (hφ : ∀ s ∈ Ioo a b, HasDerivAt φ (φ' s) s)
    (hK : ∀ s ∈ Ioo a b, |φ' s| ≤ K) (hloop : γ a = γ b)
    (hdiam : ∀ s ∈ Icc a b, ∀ t ∈ Icc a b,
      √(((γ t).1 - (γ s).1) ^ 2 + ((γ t).2 - (γ s).2) ^ 2) ≤ D) :
    2 ≤ K * D := by
  obtain ⟨c, s₁, hs₁, s₂, hs₂, h⟩ := subloop_width γ φ φ' a b K hab hγc hγ hφc hφ hK hloop
  have hK0 : 0 ≤ K :=
    (abs_nonneg _).trans (hK ((a + b) / 2) ⟨by linarith, by linarith⟩)
  have h1 := abs_rotY_le c (γ s₂ - γ s₁)
  simp only [Prod.fst_sub, Prod.snd_sub] at h1
  exact h.trans (mul_le_mul_of_nonneg_left (h1.trans (hdiam s₁ hs₁ s₂ hs₂)) hK0)

/-! ### Testemunha: a circunferencia de raio `1` (`K = 1`), diametro exatamente `2` -/

/-- Pontos da circunferencia unitaria distam no maximo `2`. -/
theorem circle_dist_le (s t : ℝ) :
    √(((arc 0 0 1 t).1 - (arc 0 0 1 s).1) ^ 2 + ((arc 0 0 1 t).2 - (arc 0 0 1 s).2) ^ 2) ≤ 2 := by
  simp only [arc, div_one, zero_add, zero_sub, one_mul]
  have h1 := sin_sq_add_cos_sq s; have h2 := sin_sq_add_cos_sq t
  have h3 := neg_one_le_cos (t - s); rw [cos_sub] at h3
  have h4 : (sin t - sin s) ^ 2 + (-cos t - -cos s) ^ 2 ≤ 2 ^ 2 := by nlinarith
  calc _ ≤ √(2 ^ 2) := Real.sqrt_le_sqrt h4
    _ = 2 := Real.sqrt_sq (by norm_num)

/-- **Testemunha de `prop:subloop`** (nao degenerada, e com a cota atingida): a circunferencia
de raio `1` em `[0, 2π]` satisfaz todas as hipoteses com `K = 1`, e seu diametro e `≤ 2 = 2/K`
(o livro: "a circle of radius `1/K` has diameter exactly `2/K`"). -/
theorem witness_circle :
    (0 : ℝ) < 2 * π ∧ ContinuousOn (arc 0 0 1) (Icc 0 (2 * π)) ∧
    (∀ s ∈ Ioo 0 (2 * π), HasDerivAt (arc 0 0 1)
      (cos ((fun s => s / 1) s), sin ((fun s => s / 1) s)) s) ∧
    ContinuousOn (fun s => s / 1) (Icc 0 (2 * π)) ∧
    (∀ s ∈ Ioo 0 (2 * π), HasDerivAt (fun s => s / 1) ((fun _ => 1 / 1) s) s) ∧
    (∀ s ∈ Ioo 0 (2 * π), |(fun _ => (1 : ℝ) / 1) s| ≤ 1) ∧
    arc 0 0 1 0 = arc 0 0 1 (2 * π) ∧
    (∀ s ∈ Icc 0 (2 * π), ∀ t ∈ Icc 0 (2 * π),
      √(((arc 0 0 1 t).1 - (arc 0 0 1 s).1) ^ 2 + ((arc 0 0 1 t).2 - (arc 0 0 1 s).2) ^ 2)
        ≤ 2) := by
  refine ⟨by positivity, (arc_continuous _ _ _).continuousOn,
    fun s _ => arc_hasDerivAt 0 0 one_ne_zero s, (continuous_id.div_const _).continuousOn,
    fun s _ => angle_hasDerivAt _ s, fun s _ => by norm_num, ?_,
    fun s _ t _ => circle_dist_le s t⟩
  simp [arc]

/-- A testemunha aplicada a `subloop_domain` (os tipos casam): `2 ≤ 1·2`, com igualdade. -/
example : (2 : ℝ) ≤ 1 * 2 := by
  obtain ⟨hab, h1, h2, h3, h4, h5, h6, h7⟩ := witness_circle
  exact subloop_domain _ _ _ 0 (2 * π) 1 2 hab h1 h2 h3 h4 h5 h6 h7

/-- Na circunferencia unitaria, toda componente direcional de uma corda e `≤ 2`. -/
theorem circle_rotY_le (c s t : ℝ) : |rotY c (arc 0 0 1 t - arc 0 0 1 s)| ≤ 2 := by
  have := abs_rotY_le c (arc 0 0 1 t - arc 0 0 1 s)
  simp only [Prod.fst_sub, Prod.snd_sub] at this
  exact this.trans (circle_dist_le s t)

/-! ### Mutantes de `prop:subloop` provados FALSOS -/

/-- Mutante 1 (largura estrita `> 2/K`): falso, pela circunferencia unitaria. -/
theorem mutant_subloop_strict_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (φ φ' : ℝ → ℝ) (a b K : ℝ), a < b →
        ContinuousOn γ (Icc a b) → (∀ s ∈ Ioo a b, HasDerivAt γ (cos (φ s), sin (φ s)) s) →
        ContinuousOn φ (Icc a b) → (∀ s ∈ Ioo a b, HasDerivAt φ (φ' s) s) →
        (∀ s ∈ Ioo a b, |φ' s| ≤ K) → γ a = γ b →
        ∃ c : ℝ, ∃ s₁ ∈ Icc a b, ∃ s₂ ∈ Icc a b, 2 < K * |rotY c (γ s₂ - γ s₁)|) := by
  intro h
  obtain ⟨hab, h1, h2, h3, h4, h5, h6, -⟩ := witness_circle
  obtain ⟨c, s₁, -, s₂, -, hc⟩ := h _ _ _ 0 (2 * π) 1 hab h1 h2 h3 h4 h5 h6
  have := circle_rotY_le c s₁ s₂
  linarith

/-- Mutante 2 (sem a cota de curvatura): falso. A circunferencia unitaria (curvatura `1`) com
`K = 1/2` exigiria uma corda de comprimento `≥ 4`. -/
theorem mutant_subloop_no_curvature_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (φ φ' : ℝ → ℝ) (a b K : ℝ), a < b →
        ContinuousOn γ (Icc a b) → (∀ s ∈ Ioo a b, HasDerivAt γ (cos (φ s), sin (φ s)) s) →
        ContinuousOn φ (Icc a b) → (∀ s ∈ Ioo a b, HasDerivAt φ (φ' s) s) →
        γ a = γ b →
        ∃ c : ℝ, ∃ s₁ ∈ Icc a b, ∃ s₂ ∈ Icc a b, 2 ≤ K * |rotY c (γ s₂ - γ s₁)|) := by
  intro h
  obtain ⟨hab, h1, h2, h3, h4, -, h6, -⟩ := witness_circle
  obtain ⟨c, s₁, -, s₂, -, hc⟩ := h _ _ _ 0 (2 * π) (1 / 2) hab h1 h2 h3 h4 h6
  have := circle_rotY_le c s₁ s₂
  linarith

/-- Mutante 3 (sem o laco fechado `γ(a) = γ(b)`): falso. O segmento `s ↦ (s, 0)` em `[0,1]`,
com `φ ≡ 0` e `K = 0`. -/
theorem mutant_subloop_no_loop_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (φ φ' : ℝ → ℝ) (a b K : ℝ), a < b →
        ContinuousOn γ (Icc a b) → (∀ s ∈ Ioo a b, HasDerivAt γ (cos (φ s), sin (φ s)) s) →
        ContinuousOn φ (Icc a b) → (∀ s ∈ Ioo a b, HasDerivAt φ (φ' s) s) →
        (∀ s ∈ Ioo a b, |φ' s| ≤ K) →
        ∃ c : ℝ, ∃ s₁ ∈ Icc a b, ∃ s₂ ∈ Icc a b, 2 ≤ K * |rotY c (γ s₂ - γ s₁)|) := by
  intro h
  obtain ⟨c, s₁, -, s₂, -, hc⟩ := h (fun s => (s, 0)) (fun _ => 0) (fun _ => 0) 0 1 0
    one_pos (continuous_id.prodMk continuous_const).continuousOn
    (fun s _ => by
      rw [cos_zero, sin_zero]
      exact (hasDerivAt_id s).prodMk (hasDerivAt_const s (0 : ℝ)))
    continuousOn_const (fun s _ => hasDerivAt_const s (0 : ℝ)) (fun s _ => by simp)
  norm_num at hc

/-! ## `prop:corridor_gap` -/

/-- **Proposicao `prop:corridor_gap`**, cota inferior: todo caminho admissivel no canal
`|y| ≤ H` que entra para a direita (`θ(0) = 0`) e sai para a esquerda (`cos θ(L) = -1`) tem
`|κ| ≤ k` so se `k ≥ 1/H`. O obstaculo `B_{R₀}(0)` nao e usado. -/
theorem corridor_lower_bound (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L k H : ℝ) (hL : 0 ≤ L)
    (hH : 0 < H)
    (hγc : ContinuousOn γ (Icc 0 L))
    (hγ : ∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L)) (hθ : ∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s)
    (hκ : ∀ s ∈ Ioo 0 L, |θ' s| ≤ k) (h0 : θ 0 = 0) (hend : cos (θ L) = -1)
    (hchan : ∀ s ∈ Icc 0 L, |(γ s).2| ≤ H) :
    1 / H ≤ k := by
  have := uturn_strip γ θ θ' L k (-H) H hL hγc hγ hθc hθ hκ h0 hend
    (fun s hs => abs_le.mp (hchan s hs))
  rw [div_le_iff₀ hH]
  linarith

/-- Pertinencia ao canal `Ω_H` com obstaculo de raio `1` (aqui com folga: fora da bola FECHADA). -/
def InChannel (H : ℝ) (p : ℝ × ℝ) : Prop := |p.2| ≤ H ∧ 1 < p.1 ^ 2 + p.2 ^ 2

/-- Construcao `w = 0`: o semicirculo de raio `H` centrado em `(-c, 0)`, `c > H + 1`, fica em
`Ω_H` (`x ≤ -c + H < -1`). -/
theorem arc_w0_in_channel (H c s : ℝ) (hH : 0 < H) (hc : H + 1 < c) :
    InChannel H (arc (-c) 0 H s) := by
  simp only [InChannel, arc, zero_sub, abs_neg]
  have h1 := sin_le_one (s / H); have h2 := abs_cos_le_one (s / H)
  refine ⟨by rw [abs_mul, abs_of_pos hH]; nlinarith, ?_⟩
  have hx : -c + H * sin (s / H) < -1 := by nlinarith
  nlinarith [sq_nonneg (H * cos (s / H))]

/-- Construcoes `w = 1` e `w ≥ 2`: a circunferencia de raio `H > 1` centrada na origem (toda
ela, logo tambem o semicirculo e as voltas inteiras inseridas) fica em `Ω_H`. -/
theorem arc_origin_in_channel (H s : ℝ) (hH : 1 < H) : InChannel H (arc 0 0 H s) := by
  simp only [InChannel, arc, zero_sub, abs_neg, zero_add]
  have h2 := abs_cos_le_one (s / H)
  have h3 := sin_sq_add_cos_sq (s / H)
  refine ⟨by rw [abs_mul, abs_of_pos (by linarith)]; nlinarith, ?_⟩
  have e : (H * sin (s / H)) ^ 2 + (-(H * cos (s / H))) ^ 2 =
      H ^ 2 * (sin (s / H) ^ 2 + cos (s / H) ^ 2) := by ring
  rw [e, h3]
  nlinarith

/-- **Testemunha de `prop:corridor_gap`** (valor atingido): para `H > 1` e qualquer centro
`cx`, o semicirculo `arc cx 0 H` em `[0, πH]` satisfaz todas as hipoteses de
`corridor_lower_bound` com `k = 1/H` (igualdade). -/
theorem witness_corridor (H cx : ℝ) (hH : 1 < H) :
    0 ≤ π * H ∧ ContinuousOn (arc cx 0 H) (Icc 0 (π * H)) ∧
    (∀ s ∈ Ioo 0 (π * H), HasDerivAt (arc cx 0 H)
      (cos ((fun s => s / H) s), sin ((fun s => s / H) s)) s) ∧
    ContinuousOn (fun s => s / H) (Icc 0 (π * H)) ∧
    (∀ s ∈ Ioo 0 (π * H), HasDerivAt (fun s => s / H) ((fun _ => 1 / H) s) s) ∧
    (∀ s ∈ Ioo 0 (π * H), |(fun _ => 1 / H) s| ≤ 1 / H) ∧
    (fun s => s / H) 0 = 0 ∧ cos ((fun s => s / H) (π * H)) = -1 ∧
    (∀ s ∈ Icc 0 (π * H), |(arc cx 0 H s).2| ≤ H) := by
  have hH0 : 0 < H := by linarith
  have hr : H ≠ 0 := hH0.ne'
  refine ⟨by positivity, (arc_continuous _ _ _).continuousOn,
    fun s _ => arc_hasDerivAt cx 0 hr s, (continuous_id.div_const _).continuousOn,
    fun s _ => angle_hasDerivAt _ s, fun s _ => ?_, by simp, ?_, fun s _ => ?_⟩
  · show |1 / H| ≤ 1 / H
    rw [abs_of_pos (by positivity)]
  · simp only; rw [mul_div_cancel_right₀ _ hr, cos_pi]
  · simp only [arc, zero_sub, abs_neg, abs_mul, abs_of_pos hH0]
    have := abs_cos_le_one (s / H)
    nlinarith

/-- O benchmark do livro: `H = 1.62`, `R₀ = 1`, `c = 3 > H + 1`. Os dois semicirculos (classes
`w = 0` e `w = 1`) ficam em `Ω_H`, e a cota `1/H` do `corridor_lower_bound` e atingida por eles. -/
theorem benchmark_constructions :
    (∀ s, InChannel (81 / 50) (arc (-3) 0 (81 / 50) s)) ∧
    (∀ s, InChannel (81 / 50) (arc 0 0 (81 / 50) s)) ∧
    (∀ (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L k : ℝ), 0 ≤ L →
        ContinuousOn γ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s) →
        (∀ s ∈ Ioo 0 L, |θ' s| ≤ k) → θ 0 = 0 → cos (θ L) = -1 →
        (∀ s ∈ Icc 0 L, |(γ s).2| ≤ 81 / 50) → 1 / (81 / 50) ≤ k) ∧
    (∀ s ∈ Ioo 0 (π * (81 / 50)), |(fun _ => (1 : ℝ) / (81 / 50)) s| ≤ 1 / (81 / 50)) := by
  refine ⟨fun s => arc_w0_in_channel _ _ s (by norm_num) (by norm_num),
    fun s => arc_origin_in_channel _ s (by norm_num),
    fun γ θ θ' L k hL h1 h2 h3 h4 h5 h6 h7 h8 =>
      corridor_lower_bound γ θ θ' L k _ hL (by norm_num) h1 h2 h3 h4 h5 h6 h7 h8,
    (witness_corridor (81 / 50) 0 (by norm_num)).2.2.2.2.2.1⟩

/-- A testemunha aplicada ao teorema (os tipos casam), no benchmark `H = 1.62`, classe `w = 1`. -/
example : (1 : ℝ) / (81 / 50) ≤ 1 / (81 / 50) := by
  obtain ⟨hL, h1, h2, h3, h4, h5, h6, h7, h8⟩ := witness_corridor (81 / 50) 0 (by norm_num)
  exact corridor_lower_bound _ _ _ _ _ _ hL (by norm_num) h1 h2 h3 h4 h5 h6 h7 h8

/-! ### Mutantes de `prop:corridor_gap` provados FALSOS -/

/-- Mutante 1 (lacuna estrita `k > 1/H`): falso; o semicirculo de raio `H` atinge `1/H`. -/
theorem mutant_corridor_strict_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L k H : ℝ), 0 ≤ L → 0 < H →
        ContinuousOn γ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s) →
        (∀ s ∈ Ioo 0 L, |θ' s| ≤ k) → θ 0 = 0 → cos (θ L) = -1 →
        (∀ s ∈ Icc 0 L, |(γ s).2| ≤ H) → 1 / H < k) := by
  intro h
  obtain ⟨hL, h1, h2, h3, h4, h5, h6, h7, h8⟩ := witness_corridor (81 / 50) 0 (by norm_num)
  have := h _ _ _ _ _ _ hL (by norm_num) h1 h2 h3 h4 h5 h6 h7 h8
  exact lt_irrefl _ this

/-- Mutante 2 (cota com a largura `H` em vez de `2H`, isto e `k ≥ 2/H`): falso, pelo mesmo
semicirculo. -/
theorem mutant_corridor_half_width_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L k H : ℝ), 0 ≤ L → 0 < H →
        ContinuousOn γ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s) →
        (∀ s ∈ Ioo 0 L, |θ' s| ≤ k) → θ 0 = 0 → cos (θ L) = -1 →
        (∀ s ∈ Icc 0 L, |(γ s).2| ≤ H) → 2 / H ≤ k) := by
  intro h
  obtain ⟨hL, h1, h2, h3, h4, h5, h6, h7, h8⟩ := witness_corridor (81 / 50) 0 (by norm_num)
  have := h _ _ _ _ _ _ hL (by norm_num) h1 h2 h3 h4 h5 h6 h7 h8
  norm_num at this

end LeanReal.Chap09SubloopCorridor

#print axioms LeanReal.Chap09SubloopCorridor.exists_turn_of_loop
#print axioms LeanReal.Chap09SubloopCorridor.subloop_width
#print axioms LeanReal.Chap09SubloopCorridor.subloop_diam
#print axioms LeanReal.Chap09SubloopCorridor.subloop_domain
#print axioms LeanReal.Chap09SubloopCorridor.witness_circle
#print axioms LeanReal.Chap09SubloopCorridor.mutant_subloop_strict_false
#print axioms LeanReal.Chap09SubloopCorridor.mutant_subloop_no_curvature_false
#print axioms LeanReal.Chap09SubloopCorridor.mutant_subloop_no_loop_false
#print axioms LeanReal.Chap09SubloopCorridor.corridor_lower_bound
#print axioms LeanReal.Chap09SubloopCorridor.arc_w0_in_channel
#print axioms LeanReal.Chap09SubloopCorridor.arc_origin_in_channel
#print axioms LeanReal.Chap09SubloopCorridor.witness_corridor
#print axioms LeanReal.Chap09SubloopCorridor.benchmark_constructions
#print axioms LeanReal.Chap09SubloopCorridor.mutant_corridor_strict_false
#print axioms LeanReal.Chap09SubloopCorridor.mutant_corridor_half_width_false
