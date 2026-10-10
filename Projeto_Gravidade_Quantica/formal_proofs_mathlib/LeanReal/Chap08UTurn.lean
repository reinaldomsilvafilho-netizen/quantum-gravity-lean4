import LeanReal.Chap09MouthHalfturn

/-!
# Capitulo 8, `lem:euclidean_uturn` (= capitulo 7, `thm:lower_bounds`(3)) e capitulo 9,
# `prop:balloon_height` (lote B2 do `PLANO_LIVRO_B.md`)

Fontes:
* `unified_quantum_gravity_book/chap08_noneuclidean_minimax_relativity_adm.tex`, Lemma
  "Euclidean U-Turn Bound" (`lem:euclidean_uturn`): `γ ⊂ S_w = ℝ × [0,w]` U-turn que parte na
  direcao `(1,0)`, `|κ| ≤ k` q.t.p. Entao `k ≥ 2/w`; igualdade no semicirculo de diametro `w`.
* `chap07_minimax_extrinsic_curvature_submanifolds.tex`, `thm:lower_bounds`(3): o mesmo
  enunciado ("Planar U-turn").
* `chap09_global_homotopy_covering_spaces_jordan_loops.tex`, `prop:balloon_height`: toda curva
  admissivel cuja tangente vai de `(1,0)` a `(-1,0)` tem dois pontos com `|Δy| ≥ 2ρ`; se uma
  U-turn de boca esta em `D_R`, entao `R ≥ ρ`.

## Reducao declarada (a mesma de `Chap09MouthHalfturn`)

* `γ = (x, y) : ℝ → ℝ × ℝ` continua em `[0,L]`, `γ'(s) = (cos θ(s), sin θ(s))` em `(0,L)`.
* `θ` continua em `[0,L]`, DIFERENCIAVEL em `(0,L)`, `|θ'| ≤ k` em `(0,L)`. O livro pede `θ`
  Lipschitz (`C^{1,1}`) com a cota q.t.p.; esse caso NAO esta coberto.
* `γ'(0) = (1,0)` e codificado por `θ(0) = 0`; `γ'(L) = -γ'(0)` por `cos θ(L) = -1`, isto e
  `θ(L) ∈ π + 2πℤ`. NAO se supoe `θ([0,L]) ⊂ [0,π]` (essa e a diferenca para `prop:mouth_halfturn`).
* Prova: o trabalho novo e a SELECAO (`exists_halfturn_window`): `s_b` = primeiro instante com
  `θ = θ(p) + π`, `s_a` = ultimo instante antes de `s_b` com `θ = θ(p)`; em `[s_a,s_b]` o angulo
  fica em `[θ(p), θ(p)+π]`. Depois, no referencial girado de `θ(p)`, aplica-se
  `Chap09MouthHalfturn.mouth_halfturn` (funcao monotona `y + ρ cos θ`). O caso em que `θ` atinge
  `-π` primeiro e tratado pela reflexao `(x,y) ↦ (x,-y)`, `θ ↦ -θ`, como no livro.
* `rise_abs` (dois pontos com `k·|⟨γ(s₂)-γ(s₁), e⟩| ≥ 2`, `e = (-sin c, cos c)`) e reaproveitado
  por `Chap09SubloopCorridor` (`prop:subloop`).
-/

noncomputable section

namespace LeanReal.Chap08UTurn

open Set Real

/-! ## Coordenadas giradas -/

/-- Componente de `v` na direcao unitaria `e(c) = (-sin c, cos c)` (o "y" do referencial girado
de `c`). -/
def rotY (c : ℝ) (v : ℝ × ℝ) : ℝ := -sin c * v.1 + cos c * v.2

/-- A rotacao por `-c`, como aplicacao linear continua (componentes `(⟨v,(cos c, sin c)⟩,
rotY c v)`). -/
def rotCLM (c : ℝ) : ℝ × ℝ →L[ℝ] ℝ × ℝ :=
  (cos c • ContinuousLinearMap.fst ℝ ℝ ℝ + sin c • ContinuousLinearMap.snd ℝ ℝ ℝ).prod
    ((-sin c) • ContinuousLinearMap.fst ℝ ℝ ℝ + cos c • ContinuousLinearMap.snd ℝ ℝ ℝ)

theorem rotCLM_apply (c : ℝ) (v : ℝ × ℝ) :
    rotCLM c v = (cos c * v.1 + sin c * v.2, rotY c v) := by
  simp [rotCLM, rotY]

theorem rotY_zero (v : ℝ × ℝ) : rotY 0 v = v.2 := by simp [rotY]

theorem rotY_sub (c : ℝ) (v w : ℝ × ℝ) : rotY c (v - w) = rotY c v - rotY c w := by
  simp only [rotY, Prod.fst_sub, Prod.snd_sub]; ring

/-- A rotacao leva a direcao de angulo `t` na de angulo `t - c`. -/
theorem rotCLM_dir (c t : ℝ) : rotCLM c (cos t, sin t) = (cos (t - c), sin (t - c)) := by
  rw [rotCLM_apply]
  simp only [rotY, cos_sub, sin_sub, Prod.mk.injEq]
  constructor <;> ring

/-- `|rotY c v|` e no maximo a norma euclidiana de `v`. -/
theorem abs_rotY_le (c : ℝ) (v : ℝ × ℝ) : |rotY c v| ≤ √(v.1 ^ 2 + v.2 ^ 2) := by
  apply Real.abs_le_sqrt
  have h := sin_sq_add_cos_sq c
  simp only [rotY]
  nlinarith [sq_nonneg (cos c * v.1 + sin c * v.2)]

/-- Reflexao `(x,y) ↦ (x,-y)`. -/
def reflCLM : ℝ × ℝ →L[ℝ] ℝ × ℝ :=
  (ContinuousLinearMap.fst ℝ ℝ ℝ).prod (-ContinuousLinearMap.snd ℝ ℝ ℝ)

theorem reflCLM_apply (v : ℝ × ℝ) : reflCLM v = (v.1, -v.2) := by simp [reflCLM]

/-! ## Selecao do intervalo de meia-volta -/

/-- **Selecao** (o passo "`s_b = min{θ = π}`, `s_a = max{s < s_b : θ = 0}`" da prova de
`lem:euclidean_uturn`): se `φ` e continua em `[p,q]` e `φ(q) ≥ φ(p) + π`, ha `p ≤ a ≤ b ≤ q`
com `φ(a) = φ(p)`, `φ(b) = φ(p) + π` e `φ([a,b]) ⊂ [φ(p), φ(p)+π]`. -/
theorem exists_halfturn_window {φ : ℝ → ℝ} {p q : ℝ} (hpq : p ≤ q)
    (hφc : ContinuousOn φ (Icc p q)) (hrise : φ p + π ≤ φ q) :
    ∃ a b, p ≤ a ∧ a ≤ b ∧ b ≤ q ∧ φ a = φ p ∧ φ b = φ p + π ∧
      ∀ s ∈ Icc a b, φ s ∈ Icc (φ p) (φ p + π) := by
  set c := φ p with hc
  -- b: o primeiro instante com φ = c + π
  have hSb : IsClosed (Icc p q ∩ φ ⁻¹' {c + π}) :=
    hφc.preimage_isClosed_of_isClosed isClosed_Icc isClosed_singleton
  have hSbc : IsCompact (Icc p q ∩ φ ⁻¹' {c + π}) :=
    isCompact_Icc.of_isClosed_subset hSb inter_subset_left
  have hSbne : (Icc p q ∩ φ ⁻¹' {c + π}).Nonempty := by
    obtain ⟨t, ht, hft⟩ := intermediate_value_Icc hpq hφc
      (show c + π ∈ Icc (φ p) (φ q) from ⟨by linarith [pi_pos], hrise⟩)
    exact ⟨t, ht, hft⟩
  obtain ⟨b, ⟨hbI, hbv⟩, hbmin⟩ := hSbc.exists_isLeast hSbne
  simp only [mem_preimage, mem_singleton_iff] at hbv
  -- a: o ultimo instante em [p,b] com φ = c
  have hφb : ContinuousOn φ (Icc p b) := hφc.mono (Icc_subset_Icc le_rfl hbI.2)
  have hSa : IsClosed (Icc p b ∩ φ ⁻¹' {c}) :=
    hφb.preimage_isClosed_of_isClosed isClosed_Icc isClosed_singleton
  have hSac : IsCompact (Icc p b ∩ φ ⁻¹' {c}) :=
    isCompact_Icc.of_isClosed_subset hSa inter_subset_left
  have hSane : (Icc p b ∩ φ ⁻¹' {c}).Nonempty := ⟨p, ⟨le_rfl, hbI.1⟩, rfl⟩
  obtain ⟨a, ⟨haI, hav⟩, hamax⟩ := hSac.exists_isGreatest hSane
  simp only [mem_preimage, mem_singleton_iff] at hav
  refine ⟨a, b, haI.1, haI.2, hbI.2, hav, hbv, ?_⟩
  intro s hs
  have hsI : s ∈ Icc p q := ⟨haI.1.trans hs.1, hs.2.trans hbI.2⟩
  constructor
  · -- φ s ≥ c: senao haveria um zero de φ - c em (s, b], depois de a
    by_contra hlt
    rw [not_le] at hlt
    have hφsb : ContinuousOn φ (Icc s b) := hφc.mono (Icc_subset_Icc hsI.1 hbI.2)
    obtain ⟨u, hu, hfu⟩ := intermediate_value_Icc hs.2 hφsb
      (show c ∈ Icc (φ s) (φ b) from ⟨hlt.le, by rw [hbv]; linarith [pi_pos]⟩)
    have hua : u ≤ a := hamax ⟨⟨hsI.1.trans hu.1, hu.2⟩, hfu⟩
    have : u = s := le_antisymm (hua.trans hs.1) hu.1
    rw [this] at hfu
    linarith
  · -- φ s ≤ c + π: senao haveria um instante antes de b com φ = c + π
    by_contra hgt
    rw [not_le] at hgt
    have hφps : ContinuousOn φ (Icc p s) := hφc.mono (Icc_subset_Icc le_rfl hsI.2)
    obtain ⟨u, hu, hfu⟩ := intermediate_value_Icc hsI.1 hφps
      (show c + π ∈ Icc (φ p) (φ s) from ⟨by linarith [pi_pos], hgt.le⟩)
    have hbu : b ≤ u := hbmin ⟨⟨hu.1, hu.2.trans hsI.2⟩, hfu⟩
    have : s = b := le_antisymm hs.2 (hbu.trans hu.2)
    rw [this, hbv] at hgt
    linarith

/-! ## Subida minima numa meia-volta (reaproveita `Chap09MouthHalfturn`) -/

/-- Se o angulo sobe `π` em `[p,q]` com `|φ'| ≤ K`, ha dois pontos cuja diferenca tem componente
`≥ 2/K` (na forma `2 ≤ K·rotY`) na direcao `e(φ(p)) = (-sin φ(p), cos φ(p))`. -/
theorem rise_pos (γ : ℝ → ℝ × ℝ) (φ φ' : ℝ → ℝ) (p q K : ℝ) (hpq : p ≤ q)
    (hγc : ContinuousOn γ (Icc p q))
    (hγ : ∀ s ∈ Ioo p q, HasDerivAt γ (cos (φ s), sin (φ s)) s)
    (hφc : ContinuousOn φ (Icc p q)) (hφ : ∀ s ∈ Ioo p q, HasDerivAt φ (φ' s) s)
    (hK : ∀ s ∈ Ioo p q, |φ' s| ≤ K) (hrise : φ p + π ≤ φ q) :
    ∃ s₁ ∈ Icc p q, ∃ s₂ ∈ Icc p q, 2 ≤ K * rotY (φ p) (γ s₂ - γ s₁) := by
  obtain ⟨a, b, hpa, hab, hbq, ha, hb, hrange⟩ := exists_halfturn_window hpq hφc hrise
  set c := φ p with hc
  have hsub : Icc a b ⊆ Icc p q := Icc_subset_Icc hpa hbq
  have hsubo : Ioo a b ⊆ Ioo p q := Ioo_subset_Ioo hpa hbq
  have hmaps : MapsTo (fun u => a + u) (Icc 0 (b - a)) (Icc p q) := by
    intro u hu
    exact hsub ⟨by linarith [hu.1], by linarith [hu.2]⟩
  have hab' : a + (b - a) = b := by ring
  have key : ∀ ρ > 0, K ≤ 1 / ρ → rotY c (γ b) - rotY c (γ a) ≥ 2 * ρ := by
    intro ρ hρ hKρ
    have h := LeanReal.Chap09MouthHalfturn.mouth_halfturn
      (fun u => rotCLM c (γ (a + u))) (fun u => φ (a + u) - c) (fun u => φ' (a + u))
      (b - a) ρ (by linarith) hρ
      ((rotCLM c).continuous.comp_continuousOn
        (hγc.comp (continuous_const_add a).continuousOn hmaps))
      (fun u hu => by
        have hin : a + u ∈ Ioo p q := hsubo ⟨by linarith [hu.1], by linarith [hu.2]⟩
        have h1 := (hγ (a + u) hin).comp_const_add a u
        have h2 := (rotCLM c).hasFDerivAt.comp_hasDerivAt u h1
        rw [rotCLM_dir] at h2
        exact h2)
      ((hφc.comp (continuous_const_add a).continuousOn hmaps).sub continuousOn_const)
      (fun u hu => by
        have hin : a + u ∈ Ioo p q := hsubo ⟨by linarith [hu.1], by linarith [hu.2]⟩
        exact ((hφ (a + u) hin).comp_const_add a u).sub_const c)
      (fun u hu => (hK _ (hsubo ⟨by linarith [hu.1], by linarith [hu.2]⟩)).trans hKρ)
      (by simp [ha])
      (by simp only [hab', hb]; simp)
      (fun u hu => by
        have := hrange (a + u) ⟨by linarith [hu.1], by linarith [hu.2]⟩
        exact ⟨by linarith [this.1], by linarith [this.2]⟩)
    simp only [rotCLM_apply, add_zero, hab'] at h
    exact h
  refine ⟨a, hsub ⟨le_rfl, hab⟩, b, hsub ⟨hab, le_rfl⟩, ?_⟩
  rw [rotY_sub]
  rcases lt_or_ge 0 K with hKpos | hKnp
  · have h := key (1 / K) (by positivity) (by rw [one_div_one_div])
    calc (2 : ℝ) = K * (2 * (1 / K)) := by field_simp
      _ ≤ K * (rotY c (γ b) - rotY c (γ a)) := mul_le_mul_of_nonneg_left h hKpos.le
  · exfalso
    set D := rotY c (γ b) - rotY c (γ a)
    have hpos : (0 : ℝ) < |D| + 1 := by positivity
    have h := key (|D| + 1) hpos (hKnp.trans (by positivity))
    linarith [le_abs_self D, abs_nonneg D]

/-- Versao com sinal qualquer: se `|φ(q) - φ(p)| ≥ π`, ha dois pontos com
`K·|⟨γ(s₂) - γ(s₁), e(φ(p))⟩| ≥ 2`. O caso `φ(q) ≤ φ(p) - π` usa a reflexao `(x,y) ↦ (x,-y)`. -/
theorem rise_abs (γ : ℝ → ℝ × ℝ) (φ φ' : ℝ → ℝ) (p q K : ℝ) (hpq : p ≤ q)
    (hγc : ContinuousOn γ (Icc p q))
    (hγ : ∀ s ∈ Ioo p q, HasDerivAt γ (cos (φ s), sin (φ s)) s)
    (hφc : ContinuousOn φ (Icc p q)) (hφ : ∀ s ∈ Ioo p q, HasDerivAt φ (φ' s) s)
    (hK : ∀ s ∈ Ioo p q, |φ' s| ≤ K) (hturn : π ≤ |φ q - φ p|) :
    ∃ s₁ ∈ Icc p q, ∃ s₂ ∈ Icc p q, 2 ≤ K * |rotY (φ p) (γ s₂ - γ s₁)| := by
  -- K ≥ 0, pois p < q
  have hpq' : p < q := by
    rcases hpq.lt_or_eq with h | h
    · exact h
    · rw [h, sub_self, abs_zero] at hturn; linarith [pi_pos]
  have hK0 : 0 ≤ K :=
    (abs_nonneg _).trans (hK ((p + q) / 2) ⟨by linarith, by linarith⟩)
  rcases le_abs'.mp hturn with hneg | hpos
  · -- φ desce π: reflexao
    have h := rise_pos (fun s => reflCLM (γ s)) (fun s => -φ s) (fun s => -φ' s) p q K hpq
      (reflCLM.continuous.comp_continuousOn hγc)
      (fun s hs => by
        have h2 := reflCLM.hasFDerivAt.comp_hasDerivAt s (hγ s hs)
        rw [reflCLM_apply] at h2
        rw [cos_neg, sin_neg]
        exact h2)
      hφc.neg (fun s hs => (hφ s hs).neg) (fun s hs => by rw [abs_neg]; exact hK s hs)
      (by linarith)
    obtain ⟨s₁, hs₁, s₂, hs₂, h⟩ := h
    refine ⟨s₁, hs₁, s₂, hs₂, ?_⟩
    have hrefl : rotY (-φ p) (reflCLM (γ s₂) - reflCLM (γ s₁)) =
        -rotY (φ p) (γ s₂ - γ s₁) := by
      simp only [reflCLM_apply, rotY, Prod.fst_sub, Prod.snd_sub, sin_neg, cos_neg]; ring
    rw [hrefl] at h
    exact h.trans (mul_le_mul_of_nonneg_left (neg_le_abs _) hK0)
  · obtain ⟨s₁, hs₁, s₂, hs₂, h⟩ :=
      rise_pos γ φ φ' p q K hpq hγc hγ hφc hφ hK (by linarith)
    exact ⟨s₁, hs₁, s₂, hs₂, h.trans (mul_le_mul_of_nonneg_left (le_abs_self _) hK0)⟩

/-- `cos x = -1` implica `|x| ≥ π`. -/
theorem pi_le_abs_of_cos_eq_neg_one {x : ℝ} (h : cos x = -1) : π ≤ |x| := by
  by_contra hlt
  rw [not_le] at hlt
  have := injOn_cos ⟨abs_nonneg x, hlt.le⟩ ⟨pi_pos.le, le_rfl⟩ (by rw [cos_abs, h, cos_pi])
  linarith

/-- Uma U-turn (`θ(0) = 0`, `cos θ(L) = -1`, `|θ'| ≤ k`) tem dois pontos com
`k·|y(s₂) - y(s₁)| ≥ 2`. -/
theorem uturn_two_points (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L k : ℝ) (hL : 0 ≤ L)
    (hγc : ContinuousOn γ (Icc 0 L))
    (hγ : ∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L)) (hθ : ∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s)
    (hκ : ∀ s ∈ Ioo 0 L, |θ' s| ≤ k) (h0 : θ 0 = 0) (hend : cos (θ L) = -1) :
    ∃ s₁ ∈ Icc 0 L, ∃ s₂ ∈ Icc 0 L, 2 ≤ k * |(γ s₂).2 - (γ s₁).2| := by
  have hturn : π ≤ |θ L - θ 0| := by rw [h0, sub_zero]; exact pi_le_abs_of_cos_eq_neg_one hend
  obtain ⟨s₁, hs₁, s₂, hs₂, h⟩ := rise_abs γ θ θ' 0 L k hL hγc hγ hθc hθ hκ hturn
  rw [h0, rotY_zero, Prod.snd_sub] at h
  exact ⟨s₁, hs₁, s₂, hs₂, h⟩

/-- U-turn numa faixa `ℝ × [α, β]`: `2 ≤ k (β - α)`. -/
theorem uturn_strip (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L k α β : ℝ) (hL : 0 ≤ L)
    (hγc : ContinuousOn γ (Icc 0 L))
    (hγ : ∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L)) (hθ : ∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s)
    (hκ : ∀ s ∈ Ioo 0 L, |θ' s| ≤ k) (h0 : θ 0 = 0) (hend : cos (θ L) = -1)
    (hstrip : ∀ s ∈ Icc 0 L, (γ s).2 ∈ Icc α β) :
    2 ≤ k * (β - α) := by
  obtain ⟨s₁, hs₁, s₂, hs₂, h⟩ := uturn_two_points γ θ θ' L k hL hγc hγ hθc hθ hκ h0 hend
  have hk : 0 ≤ k := by
    by_contra hk; rw [not_le] at hk
    nlinarith [abs_nonneg ((γ s₂).2 - (γ s₁).2)]
  have hd : |(γ s₂).2 - (γ s₁).2| ≤ β - α := by
    have h1 := hstrip s₁ hs₁; have h2 := hstrip s₂ hs₂
    rw [abs_le]; constructor <;> linarith [h1.1, h1.2, h2.1, h2.2]
  exact h.trans (mul_le_mul_of_nonneg_left hd hk)

/-- **Lema `lem:euclidean_uturn`** (capitulo 8), na reducao do cabecalho: uma U-turn em
`S_w = ℝ × [0,w]` com `|κ| ≤ k` satisfaz `2 ≤ k w`. -/
theorem euclidean_uturn (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L k w : ℝ) (hL : 0 ≤ L)
    (hγc : ContinuousOn γ (Icc 0 L))
    (hγ : ∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L)) (hθ : ∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s)
    (hκ : ∀ s ∈ Ioo 0 L, |θ' s| ≤ k) (h0 : θ 0 = 0) (hend : cos (θ L) = -1)
    (hstrip : ∀ s ∈ Icc 0 L, (γ s).2 ∈ Icc 0 w) :
    2 ≤ k * w := by
  simpa using uturn_strip γ θ θ' L k 0 w hL hγc hγ hθc hθ hκ h0 hend hstrip

/-- **`lem:euclidean_uturn`, forma `k ≥ 2/w`** (para `w > 0`). -/
theorem euclidean_uturn_div (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L k w : ℝ) (hL : 0 ≤ L)
    (hw : 0 < w)
    (hγc : ContinuousOn γ (Icc 0 L))
    (hγ : ∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L)) (hθ : ∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s)
    (hκ : ∀ s ∈ Ioo 0 L, |θ' s| ≤ k) (h0 : θ 0 = 0) (hend : cos (θ L) = -1)
    (hstrip : ∀ s ∈ Icc 0 L, (γ s).2 ∈ Icc 0 w) :
    2 / w ≤ k := by
  rw [div_le_iff₀ hw]
  exact euclidean_uturn γ θ θ' L k w hL hγc hγ hθc hθ hκ h0 hend hstrip

/-- **`thm:lower_bounds`(3)** (capitulo 7, "Planar U-turn"): o mesmo enunciado que
`lem:euclidean_uturn`, aqui com `‖κ‖_∞ ≤ k`. -/
theorem lower_bounds_uturn (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L k w : ℝ) (hL : 0 ≤ L)
    (hw : 0 < w)
    (hγc : ContinuousOn γ (Icc 0 L))
    (hγ : ∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L)) (hθ : ∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s)
    (hκ : ∀ s ∈ Ioo 0 L, |θ' s| ≤ k) (h0 : θ 0 = 0) (hend : cos (θ L) = -1)
    (hstrip : ∀ s ∈ Icc 0 L, (γ s).2 ∈ Icc 0 w) :
    2 / w ≤ k :=
  euclidean_uturn_div γ θ θ' L k w hL hw hγc hγ hθc hθ hκ h0 hend hstrip

/-- **Proposicao `prop:balloon_height`**, primeira afirmacao: curva admissivel (`|θ'| ≤ 1/ρ`)
cuja tangente vai de `(1,0)` a `(-1,0)` tem dois pontos com `|Δy| ≥ 2ρ`. -/
theorem balloon_height (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L ρ : ℝ) (hL : 0 ≤ L) (hρ : 0 < ρ)
    (hγc : ContinuousOn γ (Icc 0 L))
    (hγ : ∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L)) (hθ : ∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s)
    (hκ : ∀ s ∈ Ioo 0 L, |θ' s| ≤ 1 / ρ) (h0 : θ 0 = 0) (hend : cos (θ L) = -1) :
    ∃ s₁ ∈ Icc 0 L, ∃ s₂ ∈ Icc 0 L, 2 * ρ ≤ |(γ s₂).2 - (γ s₁).2| := by
  obtain ⟨s₁, hs₁, s₂, hs₂, h⟩ := uturn_two_points γ θ θ' L (1 / ρ) hL hγc hγ hθc hθ hκ h0 hend
  refine ⟨s₁, hs₁, s₂, hs₂, ?_⟩
  rw [div_mul_eq_mul_div, one_mul, le_div_iff₀ hρ] at h
  linarith

/-- **`prop:balloon_height`**, consequencia: se a curva fica em
`D_R = {x ≥ 0, x² + y² ≤ R²}` (`R > 0`), entao `R ≥ ρ`. A condicao `γ(0), γ(L) ∈ W_a` do livro
nao e usada (o livro diz "for every `a`"). -/
theorem balloon_radius (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L ρ R : ℝ) (hL : 0 ≤ L) (hρ : 0 < ρ)
    (hR : 0 < R)
    (hγc : ContinuousOn γ (Icc 0 L))
    (hγ : ∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L)) (hθ : ∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s)
    (hκ : ∀ s ∈ Ioo 0 L, |θ' s| ≤ 1 / ρ) (h0 : θ 0 = 0) (hend : cos (θ L) = -1)
    (hD : ∀ s ∈ Icc 0 L, 0 ≤ (γ s).1 ∧ (γ s).1 ^ 2 + (γ s).2 ^ 2 ≤ R ^ 2) :
    ρ ≤ R := by
  obtain ⟨s₁, hs₁, s₂, hs₂, h⟩ := balloon_height γ θ θ' L ρ hL hρ hγc hγ hθc hθ hκ h0 hend
  have hy : ∀ s ∈ Icc 0 L, |(γ s).2| ≤ R := fun s hs => by
    have := (hD s hs).2
    rw [abs_le]; constructor <;> nlinarith [sq_nonneg (γ s).1]
  have := abs_sub (γ s₂).2 (γ s₁).2
  linarith [hy s₁ hs₁, hy s₂ hs₂]

/-! ## Testemunhas: arcos de circulo -/

/-- Arco de circulo de raio `r` e centro `(cx, cy)`, parametrizado por comprimento de arco,
partindo de `(cx, cy - r)` na direcao `(1,0)`; angulo tangente `s/r`. -/
def arc (cx cy r : ℝ) (s : ℝ) : ℝ × ℝ := (cx + r * sin (s / r), cy - r * cos (s / r))

theorem arc_hasDerivAt (cx cy : ℝ) {r : ℝ} (hr : r ≠ 0) (s : ℝ) :
    HasDerivAt (arc cx cy r) (cos (s / r), sin (s / r)) s := by
  have h1 : HasDerivAt (fun s => s / r) (1 / r) s := by
    simpa using (hasDerivAt_id s).div_const r
  have hx := (h1.sin.const_mul r).const_add cx
  have hy := (h1.cos.const_mul r).const_sub cy
  have := hx.prodMk hy
  unfold arc
  convert this using 1
  ext <;> field_simp

theorem arc_continuous (cx cy r : ℝ) : Continuous (arc cx cy r) := by
  unfold arc; fun_prop

theorem angle_hasDerivAt (r s : ℝ) : HasDerivAt (fun s => s / r) (1 / r) s := by
  simpa using (hasDerivAt_id s).div_const r

/-- **Testemunha (nitidez de `lem:euclidean_uturn`)**: para todo `w > 0`, o semicirculo de
diametro `w` (`r = w/2`, centro `(0, r)`) satisfaz TODAS as hipoteses de `euclidean_uturn` com
`k = 2/w`, e a conclusao vale com igualdade `k w = 2`. -/
theorem witness_uturn (w : ℝ) (hw : 0 < w) :
    0 ≤ π * (w / 2) ∧ ContinuousOn (arc 0 (w / 2) (w / 2)) (Icc 0 (π * (w / 2))) ∧
    (∀ s ∈ Ioo 0 (π * (w / 2)), HasDerivAt (arc 0 (w / 2) (w / 2))
      (cos ((fun s => s / (w / 2)) s), sin ((fun s => s / (w / 2)) s)) s) ∧
    ContinuousOn (fun s => s / (w / 2)) (Icc 0 (π * (w / 2))) ∧
    (∀ s ∈ Ioo 0 (π * (w / 2)),
      HasDerivAt (fun s => s / (w / 2)) ((fun _ => 1 / (w / 2)) s) s) ∧
    (∀ s ∈ Ioo 0 (π * (w / 2)), |(fun _ => 1 / (w / 2)) s| ≤ 2 / w) ∧
    (fun s => s / (w / 2)) 0 = 0 ∧ cos ((fun s => s / (w / 2)) (π * (w / 2))) = -1 ∧
    (∀ s ∈ Icc 0 (π * (w / 2)), (arc 0 (w / 2) (w / 2) s).2 ∈ Icc 0 w) ∧
    2 / w * w = 2 := by
  have hr : (w / 2) ≠ 0 := by positivity
  refine ⟨by positivity, (arc_continuous _ _ _).continuousOn,
    fun s _ => arc_hasDerivAt 0 _ hr s, (continuous_id.div_const _).continuousOn,
    fun s _ => angle_hasDerivAt _ s, fun s _ => ?_, by simp, ?_, fun s _ => ?_, ?_⟩
  · rw [abs_of_pos (by positivity)]; field_simp; rfl
  · simp only; rw [mul_div_cancel_right₀ _ hr, cos_pi]
  · simp only [arc]
    have h1 := neg_one_le_cos (s / (w / 2)); have h2 := cos_le_one (s / (w / 2))
    constructor <;> nlinarith
  · field_simp

/-- A testemunha aplicada ao teorema (os tipos casam), com `w = 2`. -/
example : (2 : ℝ) / 2 ≤ 2 / 2 := by
  obtain ⟨hL, h1, h2, h3, h4, h5, h6, h7, h8, -⟩ := witness_uturn 2 two_pos
  exact euclidean_uturn_div _ _ _ _ _ 2 hL two_pos h1 h2 h3 h4 h5 h6 h7 h8

/-! ## Mutantes de `lem:euclidean_uturn` provados FALSOS -/

/-- Mutante 1 (conclusao estrita `2 < k w`): falso, pelo semicirculo (`w = 2`, `k = 1`). -/
theorem mutant_strict_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L k w : ℝ), 0 ≤ L →
        ContinuousOn γ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s) →
        (∀ s ∈ Ioo 0 L, |θ' s| ≤ k) → θ 0 = 0 → cos (θ L) = -1 →
        (∀ s ∈ Icc 0 L, (γ s).2 ∈ Icc 0 w) → 2 < k * w) := by
  intro h
  obtain ⟨hL, h1, h2, h3, h4, h5, h6, h7, h8, -⟩ := witness_uturn 2 two_pos
  have := h _ _ _ _ _ 2 hL h1 h2 h3 h4 h5 h6 h7 h8
  norm_num at this

/-- Mutante 2 (sem a faixa): falso. O semicirculo de diametro `2` com `k = 1`, lido com `w = 1`:
`2 ≤ 1` e falso. -/
theorem mutant_no_strip_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L k w : ℝ), 0 ≤ L →
        ContinuousOn γ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s) →
        (∀ s ∈ Ioo 0 L, |θ' s| ≤ k) → θ 0 = 0 → cos (θ L) = -1 → 2 ≤ k * w) := by
  intro h
  obtain ⟨hL, h1, h2, h3, h4, h5, h6, h7, -, -⟩ := witness_uturn 2 two_pos
  have := h _ _ _ _ _ 1 hL h1 h2 h3 h4 h5 h6 h7
  norm_num at this

/-- Mutante 3 (sem a cota de curvatura): falso. O mesmo semicirculo com `k = 0`. -/
theorem mutant_no_curvature_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L k w : ℝ), 0 ≤ L →
        ContinuousOn γ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s) →
        θ 0 = 0 → cos (θ L) = -1 →
        (∀ s ∈ Icc 0 L, (γ s).2 ∈ Icc 0 w) → 2 ≤ k * w) := by
  intro h
  obtain ⟨hL, h1, h2, h3, h4, -, h6, h7, h8, -⟩ := witness_uturn 2 two_pos
  have := h _ _ _ _ 0 2 hL h1 h2 h3 h4 h6 h7 h8
  norm_num at this

/-- Mutante 4 (meia-volta trocada por quarto de volta, `cos θ(L) = 0`): falso. O quarto de
circulo de raio `1` (`arc 0 1 1` em `[0, π/2]`) fica em `ℝ × [0,1]` com `k = 1`, e `2 ≤ 1·1` e
falso. Mostra que a hipotese de inversao da direcao e usada. -/
theorem mutant_quarter_turn_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L k w : ℝ), 0 ≤ L →
        ContinuousOn γ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s) →
        (∀ s ∈ Ioo 0 L, |θ' s| ≤ k) → θ 0 = 0 → cos (θ L) = 0 →
        (∀ s ∈ Icc 0 L, (γ s).2 ∈ Icc 0 w) → 2 ≤ k * w) := by
  intro h
  have := h (arc 0 1 1) (fun s => s / 1) (fun _ => 1 / 1) (π / 2) 1 1 (by positivity)
    (arc_continuous _ _ _).continuousOn (fun s _ => arc_hasDerivAt 0 1 one_ne_zero s)
    (continuous_id.div_const _).continuousOn (fun s _ => angle_hasDerivAt 1 s)
    (fun s _ => by norm_num) (by simp) (by simp)
    (fun s hs => by
      simp only [arc, div_one]
      have h1 : 0 ≤ cos s := cos_nonneg_of_mem_Icc ⟨by linarith [hs.1, pi_pos], hs.2⟩
      have h2 := cos_le_one s
      constructor <;> nlinarith)
  norm_num at this

/-! ## Testemunha e mutantes de `prop:balloon_height` -/

/-- **Testemunha (nitidez de `balloon_radius`)**: para todo `ρ > 0`, o semicirculo de raio `ρ`
centrado na origem (de `(0,-ρ)` a `(0,ρ)`, em `x ≥ 0`) satisfaz as hipoteses com `R = ρ`: a cota
`R ≥ ρ` e atingida. -/
theorem witness_balloon (ρ : ℝ) (hρ : 0 < ρ) :
    0 ≤ π * ρ ∧ ContinuousOn (arc 0 0 ρ) (Icc 0 (π * ρ)) ∧
    (∀ s ∈ Ioo 0 (π * ρ), HasDerivAt (arc 0 0 ρ)
      (cos ((fun s => s / ρ) s), sin ((fun s => s / ρ) s)) s) ∧
    ContinuousOn (fun s => s / ρ) (Icc 0 (π * ρ)) ∧
    (∀ s ∈ Ioo 0 (π * ρ), HasDerivAt (fun s => s / ρ) ((fun _ => 1 / ρ) s) s) ∧
    (∀ s ∈ Ioo 0 (π * ρ), |(fun _ => 1 / ρ) s| ≤ 1 / ρ) ∧
    (fun s => s / ρ) 0 = 0 ∧ cos ((fun s => s / ρ) (π * ρ)) = -1 ∧
    (∀ s ∈ Icc 0 (π * ρ), 0 ≤ (arc 0 0 ρ s).1 ∧
      (arc 0 0 ρ s).1 ^ 2 + (arc 0 0 ρ s).2 ^ 2 ≤ ρ ^ 2) := by
  have hr : ρ ≠ 0 := hρ.ne'
  refine ⟨by positivity, (arc_continuous _ _ _).continuousOn,
    fun s _ => arc_hasDerivAt 0 0 hr s, (continuous_id.div_const _).continuousOn,
    fun s _ => angle_hasDerivAt _ s, fun s _ => ?_, by simp, ?_, fun s hs => ?_⟩
  · show |1 / ρ| ≤ 1 / ρ
    rw [abs_of_pos (by positivity)]
  · simp only; rw [mul_div_cancel_right₀ _ hr, cos_pi]
  · simp only [arc, zero_add, zero_sub]
    have hs0 : 0 ≤ s / ρ := div_nonneg hs.1 hρ.le
    have hsπ : s / ρ ≤ π := by rw [div_le_iff₀ hρ]; exact hs.2
    refine ⟨mul_nonneg hρ.le (sin_nonneg_of_nonneg_of_le_pi hs0 hsπ), ?_⟩
    have := sin_sq_add_cos_sq (s / ρ)
    nlinarith

/-- Mutante (conclusao estrita `ρ < R`): falso, pela testemunha com `ρ = R = 1`. -/
theorem mutant_balloon_strict_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L ρ R : ℝ), 0 ≤ L → 0 < ρ → 0 < R →
        ContinuousOn γ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s) →
        (∀ s ∈ Ioo 0 L, |θ' s| ≤ 1 / ρ) → θ 0 = 0 → cos (θ L) = -1 →
        (∀ s ∈ Icc 0 L, 0 ≤ (γ s).1 ∧ (γ s).1 ^ 2 + (γ s).2 ^ 2 ≤ R ^ 2) → ρ < R) := by
  intro h
  obtain ⟨hL, h1, h2, h3, h4, h5, h6, h7, h8⟩ := witness_balloon 1 one_pos
  have := h _ _ _ _ 1 1 hL one_pos one_pos h1 h2 h3 h4 h5 h6 h7 h8
  exact lt_irrefl _ this

/-- Mutante (sem a cota de curvatura): falso. O semicirculo de raio `1` em `D_1`, com `ρ = 2`. -/
theorem mutant_balloon_no_curvature_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L ρ R : ℝ), 0 ≤ L → 0 < ρ → 0 < R →
        ContinuousOn γ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s) →
        θ 0 = 0 → cos (θ L) = -1 →
        (∀ s ∈ Icc 0 L, 0 ≤ (γ s).1 ∧ (γ s).1 ^ 2 + (γ s).2 ^ 2 ≤ R ^ 2) → ρ ≤ R) := by
  intro h
  obtain ⟨hL, h1, h2, h3, h4, -, h6, h7, h8⟩ := witness_balloon 1 one_pos
  have := h _ _ _ _ 2 1 hL two_pos one_pos h1 h2 h3 h4 h6 h7 h8
  norm_num at this

end LeanReal.Chap08UTurn

#print axioms LeanReal.Chap08UTurn.exists_halfturn_window
#print axioms LeanReal.Chap08UTurn.rise_pos
#print axioms LeanReal.Chap08UTurn.rise_abs
#print axioms LeanReal.Chap08UTurn.uturn_strip
#print axioms LeanReal.Chap08UTurn.euclidean_uturn
#print axioms LeanReal.Chap08UTurn.euclidean_uturn_div
#print axioms LeanReal.Chap08UTurn.lower_bounds_uturn
#print axioms LeanReal.Chap08UTurn.balloon_height
#print axioms LeanReal.Chap08UTurn.balloon_radius
#print axioms LeanReal.Chap08UTurn.witness_uturn
#print axioms LeanReal.Chap08UTurn.witness_balloon
#print axioms LeanReal.Chap08UTurn.mutant_strict_false
#print axioms LeanReal.Chap08UTurn.mutant_no_strip_false
#print axioms LeanReal.Chap08UTurn.mutant_no_curvature_false
#print axioms LeanReal.Chap08UTurn.mutant_quarter_turn_false
#print axioms LeanReal.Chap08UTurn.mutant_balloon_strict_false
#print axioms LeanReal.Chap08UTurn.mutant_balloon_no_curvature_false
