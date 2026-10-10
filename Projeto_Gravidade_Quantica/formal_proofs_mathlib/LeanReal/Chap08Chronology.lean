import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Basic.ENNReal.Basic
import Mathlib.Order.ConditionallyCompleteLattice.Basic

/-!
# Ordem: cronologia (caps. 8 e 12) e dualidade de Dubins (cap. 7), versoes abstratas

Fontes: `unified_quantum_gravity_book/chap08_noneuclidean_minimax_relativity_adm.tex`,
`chap12_grand_unification_quantum_gravity_treatise.tex`, `chap07_minimax_extrinsic_curvature_submanifolds.tex`.

## Item 8.13, `prop:causal_constraints`, itens (1) e (2)

> (1) Every future-directed timelike curve from `p` to `q` lies in `J⁺(p) ∩ J⁻(q)`, its interior
> points lie in `I⁺(p) ∩ I⁻(q)`, and it is injective.
> (2) If `p ∈ 𝓑` and `q ∉ 𝓑` (`𝓑 = 𝓜 ∖ J⁻(𝓘⁺)`), there is no future-directed causal curve from
> `p` to `q`; the admissible class is empty and `κ*_wl = +∞` by convention.

## Item 12.4, `thm:jordan_chronology`

> In a chronological spacetime (no closed timelike curves) every timelike curve is injective.

Reducao declarada (abstrata): o espaco-tempo e um tipo `M` com duas relacoes `I` (cronologica,
`x ≪ y`) e `J` (causal, `x ≤ y`). Uma curva tipo tempo futura em `[a,b]` e codificada pela sua
propriedade de ordem: `s < t ⇒ γ(s) ≪ γ(t)` (`IsTimelikeOn`); uma curva causal: `s ≤ t ⇒ γ(s) ≤ γ(t)`
(`IsCausalOn`). Que curvas lorentzianas tipo tempo tenham essa propriedade (cada sub-arco e tipo
tempo) e a DEFINICAO de `I`; nao se formaliza geometria lorentziana. Hipoteses nomeadas:
`hIJ : I ⊆ J`, `hJrefl` (convencao `p ∈ J⁺(p)`), `hJtrans` (transitividade de `J`),
`hchron : ∀ x, ¬ x ≪ x` (cronologia: `p ∉ I⁺(p)`, i.e. nao ha curva tipo tempo fechada).
O livro deriva a cronologia de "fortemente causal" no item (1); aqui ela entra direto como
`hchron` (fortemente causal ⇒ causal ⇒ cronologico e classico e nao e formalizado).
O item (3) (`κ*_wl < ∞`, arredondamento de quinas lorentziano) NAO e formalizado.
Testemunha: Minkowski `ℝ^{1,1}` com `I(x,y) ⇔ |y₂ - x₂| < y₁ - x₁`.

## Item 7.2, `prop:dubins_duality`

> `d_κ` = comprimento minimo de uma curva `C^{1,1}` entre os dados orientados com `|κ| ≤ κ` q.t.p.
> (Dubins: o minimo existe). Entao `κ*(L) = inf{κ > 0 : d_κ ≤ L}`, e para `κ > κ*(L)` o caminho
> de Dubins de cota `κ` e admissivel (comprimento `≤ L`).

Reducao declarada (ordinal): uma classe abstrata `Γ` de curvas com `len, peak : Γ → ℝ` (`peak` =
`‖κ‖_{L^∞}`), `d κ := inf {len γ : peak γ ≤ κ}`, `κ*(L) := inf {peak γ : len γ ≤ L}`.
O teorema de existencia de Dubins entra como hipotese nomeada `hDubins`: para todo `κ > 0` ha
uma curva de pico `≤ κ` cujo comprimento atinge `d κ`. NAO entram: a estrutura CSC/CCC, a
afirmacao "curvatura so toma os valores `0, ±κ`", nem a geometria das curvas planas.
-/

noncomputable section

namespace LeanReal.Chap08Chronology

open Set

/-! ## Itens 8.13 e 12.4: curvas tipo tempo e causais abstratas -/

section Chronology

variable {M : Type*}

/-- Curva tipo tempo futura (abstrata) em `[a,b]`: `s < t ⇒ γ(s) ≪ γ(t)`. -/
def IsTimelikeOn (I : M → M → Prop) (γ : ℝ → M) (a b : ℝ) : Prop :=
  ∀ s ∈ Icc a b, ∀ t ∈ Icc a b, s < t → I (γ s) (γ t)

/-- Curva causal futura (abstrata) em `[a,b]`: `s ≤ t ⇒ γ(s) ≤ γ(t)`. -/
def IsCausalOn (J : M → M → Prop) (γ : ℝ → M) (a b : ℝ) : Prop :=
  ∀ s ∈ Icc a b, ∀ t ∈ Icc a b, s ≤ t → J (γ s) (γ t)

/-- **`prop:causal_constraints` (1), primeira parte**: uma curva tipo tempo de `p = γ(a)` a
`q = γ(b)` fica em `J⁺(p) ∩ J⁻(q)`. -/
theorem timelike_mem_J (I J : M → M → Prop) (hIJ : ∀ x y, I x y → J x y)
    (hJrefl : ∀ x, J x x) {γ : ℝ → M} {a b : ℝ} (hγ : IsTimelikeOn I γ a b) :
    ∀ t ∈ Icc a b, J (γ a) (γ t) ∧ J (γ t) (γ b) := by
  intro t ht
  have ha : a ∈ Icc a b := ⟨le_rfl, ht.1.trans ht.2⟩
  have hb : b ∈ Icc a b := ⟨ht.1.trans ht.2, le_rfl⟩
  constructor
  · rcases eq_or_lt_of_le ht.1 with h | h
    · rw [← h]; exact hJrefl _
    · exact hIJ _ _ (hγ a ha t ht h)
  · rcases eq_or_lt_of_le ht.2 with h | h
    · rw [h]; exact hJrefl _
    · exact hIJ _ _ (hγ t ht b hb h)

/-- **`prop:causal_constraints` (1), segunda parte**: os pontos interiores ficam em
`I⁺(p) ∩ I⁻(q)`. -/
theorem timelike_interior_mem_I (I : M → M → Prop) {γ : ℝ → M} {a b : ℝ}
    (hγ : IsTimelikeOn I γ a b) : ∀ t ∈ Ioo a b, I (γ a) (γ t) ∧ I (γ t) (γ b) := by
  intro t ht
  have hab : a ≤ b := (ht.1.trans ht.2).le
  exact ⟨hγ a ⟨le_rfl, hab⟩ t (Ioo_subset_Icc_self ht) ht.1,
    hγ t (Ioo_subset_Icc_self ht) b ⟨hab, le_rfl⟩ ht.2⟩

/-- **`thm:jordan_chronology`** e **`prop:causal_constraints` (1), injetividade**: num
espaco-tempo cronologico (`hchron : ∀ x, ¬ x ≪ x`) toda curva tipo tempo e injetiva. -/
theorem timelike_injOn (I : M → M → Prop) (hchron : ∀ x, ¬ I x x) {γ : ℝ → M} {a b : ℝ}
    (hγ : IsTimelikeOn I γ a b) : InjOn γ (Icc a b) := by
  intro s hs t ht hst
  by_contra hne
  rcases lt_or_gt_of_ne hne with h | h
  · exact hchron (γ s) (by simpa [hst] using hγ s hs t ht h)
  · exact hchron (γ t) (by simpa [hst] using hγ t ht s hs h)

/-- **`prop:causal_constraints` (2)**: com `𝓑 = {x | x ∉ J⁻(S)}` (`S` no lugar de `𝓘⁺`), se
`p ∈ 𝓑` e `q ∉ 𝓑` entao `¬ J p q`. -/
theorem not_J_of_mem_B (J : M → M → Prop) (hJtrans : ∀ x y z, J x y → J y z → J x z)
    (S : Set M) {p q : M} (hp : ¬ ∃ s ∈ S, J p s) (hq : ∃ s ∈ S, J q s) : ¬ J p q := by
  intro hpq
  obtain ⟨s, hs, hqs⟩ := hq
  exact hp ⟨s, hs, hJtrans _ _ _ hpq hqs⟩

/-- **`prop:causal_constraints` (2)**, forma de curvas: nao ha curva causal de `p ∈ 𝓑` a
`q ∉ 𝓑`. -/
theorem no_causal_curve (J : M → M → Prop) (hJtrans : ∀ x y z, J x y → J y z → J x z)
    (S : Set M) {p q : M} (hp : ¬ ∃ s ∈ S, J p s) (hq : ∃ s ∈ S, J q s) :
    ¬ ∃ (γ : ℝ → M) (a b : ℝ), a ≤ b ∧ γ a = p ∧ γ b = q ∧ IsCausalOn J γ a b := by
  rintro ⟨γ, a, b, hab, rfl, rfl, hγ⟩
  exact not_J_of_mem_B J hJtrans S hp hq (hγ a ⟨le_rfl, hab⟩ b ⟨hab, le_rfl⟩ hab)

/-- **`prop:causal_constraints` (2)**, "`κ*_wl = +∞` por convencao": o infimo, em `ℝ≥0∞`, de
qualquer custo sobre a classe admissivel (curvas causais de `p` a `q`) e `⊤`. -/
theorem kappa_wl_eq_top (J : M → M → Prop) (hJtrans : ∀ x y z, J x y → J y z → J x z)
    (S : Set M) {p q : M} (hp : ¬ ∃ s ∈ S, J p s) (hq : ∃ s ∈ S, J q s)
    (cost : (ℝ → M) → ENNReal) :
    ⨅ (γ : ℝ → M) (_ : ∃ a b, a ≤ b ∧ γ a = p ∧ γ b = q ∧ IsCausalOn J γ a b), cost γ = ⊤ := by
  refine iInf_eq_top.2 fun γ => iInf_eq_top.2 fun h => ?_
  obtain ⟨a, b, h⟩ := h
  exact absurd ⟨γ, a, b, h⟩ (no_causal_curve J hJtrans S hp hq)

end Chronology

/-! ### Testemunha: Minkowski `ℝ^{1,1}` -/

/-- Relacao cronologica de Minkowski `ℝ^{1,1}` (coordenadas `(t, x)`). -/
def Imink (u v : ℝ × ℝ) : Prop := |v.2 - u.2| < v.1 - u.1

/-- Relacao causal de Minkowski `ℝ^{1,1}`. -/
def Jmink (u v : ℝ × ℝ) : Prop := |v.2 - u.2| ≤ v.1 - u.1

theorem Imink_sub_Jmink : ∀ u v, Imink u v → Jmink u v := fun _ _ h => le_of_lt h

theorem Jmink_refl : ∀ u, Jmink u u := fun u => by simp [Jmink]

theorem Jmink_trans : ∀ u v w, Jmink u v → Jmink v w → Jmink u w := by
  intro u v w h1 h2
  unfold Jmink at *
  calc |w.2 - u.2| = |(w.2 - v.2) + (v.2 - u.2)| := by ring_nf
    _ ≤ |w.2 - v.2| + |v.2 - u.2| := abs_add_le _ _
    _ ≤ w.1 - u.1 := by linarith

theorem Imink_irrefl : ∀ u, ¬ Imink u u := fun u => by simp [Imink]

/-- Curva `γ(s) = (2s, s - s²)`: a projecao espacial NAO e injetiva (`x(0) = x(1) = 0`). -/
def γmink (s : ℝ) : ℝ × ℝ := (2 * s, s - s ^ 2)

theorem γmink_timelike : IsTimelikeOn Imink γmink 0 1 := by
  intro s hs t ht hst
  unfold Imink γmink
  simp only
  have e : t - t ^ 2 - (s - s ^ 2) = (t - s) * (1 - t - s) := by ring
  rw [e, abs_mul, abs_of_pos (by linarith : (0:ℝ) < t - s)]
  have h1 : |1 - t - s| ≤ 1 := abs_le.2 ⟨by linarith [hs.1, hs.2, ht.1, ht.2],
    by linarith [hs.1, ht.1]⟩
  nlinarith [abs_nonneg (1 - t - s)]

/-- **Testemunha nao degenerada (8.13 (1), 12.4)**: `γmink` e tipo tempo, a sua parte espacial
nao e injetiva, e mesmo assim `γmink` e injetiva (pelo teorema), com os pontos interiores em
`I⁺(p) ∩ I⁻(q)`. -/
theorem witness_minkowski :
    γmink 0 ≠ γmink 1 ∧ (γmink 0).2 = (γmink 1).2 ∧ InjOn γmink (Icc 0 1) ∧
      (∀ t ∈ Ioo (0:ℝ) 1, Imink (γmink 0) (γmink t) ∧ Imink (γmink t) (γmink 1)) ∧
      (∀ t ∈ Icc (0:ℝ) 1, Jmink (γmink 0) (γmink t) ∧ Jmink (γmink t) (γmink 1)) := by
  refine ⟨?_, by simp [γmink], timelike_injOn Imink Imink_irrefl γmink_timelike,
    timelike_interior_mem_I Imink γmink_timelike,
    timelike_mem_J Imink Jmink Imink_sub_Jmink Jmink_refl γmink_timelike⟩
  intro h
  have := congrArg Prod.fst h
  simp [γmink] at this

/-- **Testemunha de 8.13 (2)** em Minkowski: `S = {0}` (toy de `𝓘⁺`), `p = (1,0) ∈ 𝓑`,
`q = (-1,0) ∉ 𝓑`; nao ha relacao causal de `p` a `q`. -/
theorem witness_B :
    (¬ ∃ s ∈ ({(0, 0)} : Set (ℝ × ℝ)), Jmink (1, 0) s) ∧
      (∃ s ∈ ({(0, 0)} : Set (ℝ × ℝ)), Jmink (-1, 0) s) ∧ ¬ Jmink (1, 0) (-1, 0) := by
  have hp : ¬ ∃ s ∈ ({(0, 0)} : Set (ℝ × ℝ)), Jmink (1, 0) s := by
    rintro ⟨s, hs, h⟩
    rw [mem_singleton_iff] at hs
    subst hs
    unfold Jmink at h
    norm_num at h
  have hq : ∃ s ∈ ({(0, 0)} : Set (ℝ × ℝ)), Jmink (-1, 0) s :=
    ⟨(0, 0), rfl, by unfold Jmink; norm_num⟩
  exact ⟨hp, hq, not_J_of_mem_B Jmink Jmink_trans _ hp hq⟩

/-! ### Mutantes provados FALSOS -/

/-- Mutante 1 (12.4 sem cronologia): falso; `I = ⊤` e transitiva, a curva constante e "tipo
tempo" e nao e injetiva (modelo de curva tipo tempo fechada). -/
theorem mutant_no_chronology_false :
    ¬ (∀ (I : ℝ → ℝ → Prop) (_ : ∀ x y z, I x y → I y z → I x z) (γ : ℝ → ℝ),
        IsTimelikeOn I γ 0 1 → InjOn γ (Icc 0 1)) := by
  intro h
  have := h (fun _ _ => True) (fun _ _ _ _ _ => trivial) (fun _ => 0)
    (fun _ _ _ _ _ => trivial) (⟨le_rfl, zero_le_one⟩ : (0:ℝ) ∈ Icc 0 1)
    (⟨zero_le_one, le_rfl⟩ : (1:ℝ) ∈ Icc 0 1) rfl
  exact zero_ne_one this

/-- Mutante 2 (8.13 (1) com o intervalo FECHADO no lugar do interior): falso em Minkowski,
`γ(0) ≪ γ(0)` falha. -/
theorem mutant_closed_interval_false :
    ¬ (∀ t ∈ Icc (0:ℝ) 1, Imink (γmink 0) (γmink t)) := by
  intro h
  exact Imink_irrefl _ (h 0 ⟨le_rfl, zero_le_one⟩)

/-- Mutante 3 (8.13 (2) sem transitividade de `J`): falso; em `Fin 3` com `J = {(0,1),(1,2)}`,
`S = {2}`, `p = 0 ∈ 𝓑`, `q = 1 ∉ 𝓑`, mas `J 0 1`. -/
theorem mutant_no_transitivity_false :
    ¬ (∀ (J : Fin 3 → Fin 3 → Prop) (S : Set (Fin 3)) (p q : Fin 3),
        (¬ ∃ s ∈ S, J p s) → (∃ s ∈ S, J q s) → ¬ J p q) := by
  intro h
  let J : Fin 3 → Fin 3 → Prop := fun x y => (x = 0 ∧ y = 1) ∨ (x = 1 ∧ y = 2)
  refine h J {2} 0 1 ?_ ⟨2, rfl, Or.inr ⟨rfl, rfl⟩⟩ (Or.inl ⟨rfl, rfl⟩)
  rintro ⟨s, hs, h'⟩
  rw [mem_singleton_iff] at hs
  subst hs
  rcases h' with ⟨_, h2⟩ | ⟨h1, _⟩
  · exact absurd h2 (by decide)
  · exact absurd h1 (by decide)

/-! ## Item 7.2: dualidade de Dubins (abstrata) -/

section Dubins

variable {Γ : Type*} (len peak : Γ → ℝ)

/-- `d κ = inf {len γ : peak γ ≤ κ}` (comprimento minimo de Dubins para a cota `κ`). -/
def dubinsLength (κ : ℝ) : ℝ := sInf (len '' {γ | peak γ ≤ κ})

/-- `κ*(L) = inf {peak γ : len γ ≤ L}` (curvatura minimax sob a cota de comprimento `L`). -/
def minimaxCurv (L : ℝ) : ℝ := sInf (peak '' {γ | len γ ≤ L})

variable {len peak}

/-- `κ ↦ d κ` e nao crescente (onde a classe de pico `≤ κ` e nao vazia). -/
theorem dubinsLength_antitone (hlen : ∀ γ, 0 ≤ len γ) {κ κ' : ℝ} (hκ : κ ≤ κ')
    (hne : ∃ γ, peak γ ≤ κ) : dubinsLength len peak κ' ≤ dubinsLength len peak κ := by
  obtain ⟨γ, hγ⟩ := hne
  refine csInf_le_csInf ⟨0, ?_⟩ ⟨len γ, γ, hγ, rfl⟩ ?_
  · rintro _ ⟨g, -, rfl⟩; exact hlen g
  · rintro _ ⟨g, hg, rfl⟩; exact ⟨g, (show peak g ≤ κ from hg).trans hκ, rfl⟩

/-- Nucleo da prova de `prop:dubins_duality`: para `κ > 0`, existe curva admissivel
(`len ≤ L`) de pico `≤ κ` sse `d κ ≤ L`. Usa `hDubins` (o minimo de Dubins e atingido). -/
theorem exists_admissible_iff (hlen : ∀ γ, 0 ≤ len γ)
    (hDubins : ∀ κ, 0 < κ → ∃ γ, peak γ ≤ κ ∧ len γ = dubinsLength len peak κ)
    {κ L : ℝ} (hκ : 0 < κ) :
    (∃ γ, len γ ≤ L ∧ peak γ ≤ κ) ↔ dubinsLength len peak κ ≤ L := by
  constructor
  · rintro ⟨γ, hL, hp⟩
    refine le_trans (csInf_le ⟨0, ?_⟩ ⟨γ, hp, rfl⟩) hL
    rintro _ ⟨g, -, rfl⟩; exact hlen g
  · intro hd
    obtain ⟨γ, hp, hl⟩ := hDubins κ hκ
    exact ⟨γ, hl ▸ hd, hp⟩

/-- **`prop:dubins_duality`**, primeira afirmacao: `κ*(L) = inf {κ > 0 : d κ ≤ L}`, desde que
haja alguma curva de comprimento `≤ L`. -/
theorem dubins_duality (hpeak : ∀ γ, 0 ≤ peak γ) (hlen : ∀ γ, 0 ≤ len γ)
    (hDubins : ∀ κ, 0 < κ → ∃ γ, peak γ ≤ κ ∧ len γ = dubinsLength len peak κ)
    {L : ℝ} (hne : ∃ γ, len γ ≤ L) :
    minimaxCurv len peak L = sInf {κ | 0 < κ ∧ dubinsLength len peak κ ≤ L} := by
  obtain ⟨γ₀, hγ₀⟩ := hne
  have hAne : (peak '' {γ | len γ ≤ L}).Nonempty := ⟨peak γ₀, γ₀, hγ₀, rfl⟩
  have hAbdd : BddBelow (peak '' {γ | len γ ≤ L}) := ⟨0, by rintro _ ⟨g, -, rfl⟩; exact hpeak g⟩
  have hBbdd : BddBelow {κ | 0 < κ ∧ dubinsLength len peak κ ≤ L} := ⟨0, fun _ h => h.1.le⟩
  have hBne : {κ | 0 < κ ∧ dubinsLength len peak κ ≤ L}.Nonempty :=
    ⟨peak γ₀ + 1, by linarith [hpeak γ₀],
      (exists_admissible_iff hlen hDubins (by linarith [hpeak γ₀])).1 ⟨γ₀, hγ₀, by linarith⟩⟩
  apply le_antisymm
  · refine le_csInf hBne fun b hb => ?_
    obtain ⟨γ, hl, hp⟩ := (exists_admissible_iff hlen hDubins hb.1).2 hb.2
    exact (csInf_le hAbdd ⟨γ, hl, rfl⟩).trans hp
  · refine le_csInf hAne ?_
    rintro _ ⟨γ, hγ, rfl⟩
    refine le_of_forall_pos_le_add fun ε hε => csInf_le hBbdd ⟨by linarith [hpeak γ], ?_⟩
    exact (exists_admissible_iff hlen hDubins (by linarith [hpeak γ])).1
      ⟨γ, hγ, by linarith⟩

/-- **`prop:dubins_duality`**, segunda afirmacao: para `κ > κ*(L)`, o caminho de Dubins de cota
`κ` (curva de pico `≤ κ` de comprimento `d κ`) e admissivel: `d κ ≤ L`. -/
theorem dubins_path_admissible (hpeak : ∀ γ, 0 ≤ peak γ) (hlen : ∀ γ, 0 ≤ len γ)
    (hDubins : ∀ κ, 0 < κ → ∃ γ, peak γ ≤ κ ∧ len γ = dubinsLength len peak κ)
    {L κ : ℝ} (hne : ∃ γ, len γ ≤ L) (hκ : minimaxCurv len peak L < κ) :
    ∃ γ, peak γ ≤ κ ∧ len γ = dubinsLength len peak κ ∧ len γ ≤ L := by
  obtain ⟨γ₀, hγ₀⟩ := hne
  obtain ⟨_, ⟨γ₁, hγ₁, rfl⟩, hlt⟩ :=
    exists_lt_of_csInf_lt (s := peak '' {γ | len γ ≤ L}) ⟨peak γ₀, γ₀, hγ₀, rfl⟩ hκ
  have hκpos : 0 < κ := lt_of_le_of_lt (hpeak γ₁) hlt
  have hd := (exists_admissible_iff hlen hDubins hκpos).1 ⟨γ₁, hγ₁, hlt.le⟩
  obtain ⟨γ, hp, hl⟩ := hDubins κ hκpos
  exact ⟨γ, hp, hl, hl ▸ hd⟩

end Dubins

/-! ### Testemunha de 7.2: semicirculos de raio `r` (pico `1/r`, comprimento `π r`) -/

/-- Classe toy: semicirculos de raio `r > 0`. -/
abbrev Semi := {r : ℝ // 0 < r}

/-- Comprimento `π r`. -/
def lenS (r : Semi) : ℝ := Real.pi * r.1

/-- Pico de curvatura `1/r`. -/
def peakS (r : Semi) : ℝ := 1 / r.1

theorem dubinsLength_semi {κ : ℝ} (hκ : 0 < κ) : dubinsLength lenS peakS κ = Real.pi / κ := by
  apply IsLeast.csInf_eq
  refine ⟨⟨⟨1 / κ, by positivity⟩, by simp [peakS], by simp [lenS, div_eq_mul_inv]⟩, ?_⟩
  rintro _ ⟨r, hr, rfl⟩
  have hr' : 1 / r.1 ≤ κ := hr
  have h1 : 1 ≤ κ * r.1 := by rwa [div_le_iff₀ r.2] at hr'
  unfold lenS
  rw [div_le_iff₀ hκ]
  nlinarith [Real.pi_pos]

theorem hDubins_semi : ∀ κ, 0 < κ → ∃ γ, peakS γ ≤ κ ∧ lenS γ = dubinsLength lenS peakS κ :=
  fun κ hκ => ⟨⟨1 / κ, by positivity⟩, by simp [peakS],
    by rw [dubinsLength_semi hκ]; simp [lenS, div_eq_mul_inv]⟩

/-- `κ*(π) = 1` na classe toy. -/
theorem minimaxCurv_semi : minimaxCurv lenS peakS Real.pi = 1 := by
  apply IsLeast.csInf_eq
  refine ⟨⟨⟨1, one_pos⟩, by simp [lenS], by simp [peakS]⟩, ?_⟩
  rintro _ ⟨r, hr, rfl⟩
  have hr' : Real.pi * r.1 ≤ Real.pi := hr
  have h1 : r.1 ≤ 1 := by nlinarith [Real.pi_pos]
  unfold peakS
  rw [le_div_iff₀ r.2]
  linarith

/-- **Testemunha nao degenerada de `prop:dubins_duality`**: todas as hipoteses valem e o valor
comum e `1` (`κ*(π) = inf{κ > 0 : π/κ ≤ π} = 1`). -/
theorem witness_dubins :
    sInf {κ | 0 < κ ∧ dubinsLength lenS peakS κ ≤ Real.pi} = 1 := by
  rw [← dubins_duality (fun r => by unfold peakS; exact (one_div_pos.2 r.2).le)
    (fun r => by unfold lenS; exact mul_nonneg Real.pi_pos.le r.2.le) hDubins_semi
    ⟨⟨1, one_pos⟩, by simp [lenS]⟩]
  exact minimaxCurv_semi

/-! ### Mutante de 7.2 provado FALSO: sem a existencia do minimo de Dubins -/

/-- Classe toy sem minimo atingido: `γ ≤ 0` tem pico `2` e comprimento `1`; `γ > 0` tem pico `0`
e comprimento `1 + γ` (infimo `1` nao atingido). -/
def lenM (γ : ℝ) : ℝ := if γ ≤ 0 then 1 else 1 + γ

/-- Pico da classe toy do mutante. -/
def peakM (γ : ℝ) : ℝ := if γ ≤ 0 then 2 else 0

theorem dubinsLength_M_le : dubinsLength lenM peakM 1 ≤ 1 := by
  refine le_of_forall_pos_lt_add fun ε hε => ?_
  have hmem : 1 + ε / 2 ∈ lenM '' {γ | peakM γ ≤ 1} :=
    ⟨ε / 2, by simp [peakM, not_le.2 (half_pos hε)], by simp [lenM, not_le.2 (half_pos hε)]⟩
  have hbdd : BddBelow (lenM '' {γ | peakM γ ≤ 1}) := ⟨0, by
    rintro _ ⟨g, -, rfl⟩; unfold lenM; split_ifs with h <;> linarith⟩
  exact lt_of_le_of_lt (csInf_le hbdd hmem) (by linarith)

theorem minimaxCurv_M : minimaxCurv lenM peakM 1 = 2 := by
  apply IsLeast.csInf_eq
  refine ⟨⟨0, by simp [lenM], by simp [peakM]⟩, ?_⟩
  rintro _ ⟨g, hg, rfl⟩
  have hg' : lenM g ≤ 1 := hg
  unfold lenM at hg'
  unfold peakM
  split_ifs at hg' ⊢ with h
  · exact le_rfl
  · linarith [not_le.1 h]

/-- Mutante (sem `hDubins`, mantendo a existencia de curvas de pico `≤ κ` para todo `κ > 0`):
a dualidade e falsa (`κ*(1) = 2`, mas `1 ∈ {κ > 0 : d κ ≤ 1}`). -/
theorem mutant_no_dubins_false :
    ¬ (∀ (len peak : ℝ → ℝ) (L : ℝ), (∀ γ, 0 ≤ peak γ) → (∀ γ, 0 ≤ len γ) →
        (∀ κ, 0 < κ → ∃ γ, peak γ ≤ κ) → (∃ γ, len γ ≤ L) →
        minimaxCurv len peak L = sInf {κ | 0 < κ ∧ dubinsLength len peak κ ≤ L}) := by
  intro h
  have hpk : ∀ γ, 0 ≤ peakM γ := fun γ => by unfold peakM; split_ifs <;> norm_num
  have hln : ∀ γ, 0 ≤ lenM γ := fun γ => by unfold lenM; split_ifs with h <;> linarith
  have heq := h lenM peakM 1 hpk hln
    (fun κ hκ => ⟨1, by unfold peakM; split_ifs with h1 <;> [exact absurd h1 (by norm_num); exact hκ.le]⟩) ⟨0, by simp [lenM]⟩
  rw [minimaxCurv_M] at heq
  have hle : sInf {κ | 0 < κ ∧ dubinsLength lenM peakM κ ≤ 1} ≤ 1 :=
    csInf_le ⟨0, fun _ h => h.1.le⟩ ⟨one_pos, dubinsLength_M_le⟩
  linarith

/-- Mutante do nucleo (sem `hDubins`): `d 1 ≤ 1`, mas nao ha curva de comprimento `≤ 1` com pico
`≤ 1`. -/
theorem mutant_core_false :
    ¬ (dubinsLength lenM peakM 1 ≤ 1 → ∃ γ, lenM γ ≤ 1 ∧ peakM γ ≤ 1) := by
  intro h
  obtain ⟨γ, hl, hp⟩ := h dubinsLength_M_le
  unfold lenM at hl
  unfold peakM at hp
  split_ifs at hl hp with hγ
  · norm_num at hp
  · linarith [not_le.1 hγ]

/-! ## Axiomas -/

#print axioms timelike_mem_J
#print axioms timelike_interior_mem_I
#print axioms timelike_injOn
#print axioms not_J_of_mem_B
#print axioms no_causal_curve
#print axioms kappa_wl_eq_top
#print axioms witness_minkowski
#print axioms witness_B
#print axioms mutant_no_chronology_false
#print axioms mutant_closed_interval_false
#print axioms mutant_no_transitivity_false
#print axioms dubinsLength_antitone
#print axioms exists_admissible_iff
#print axioms dubins_duality
#print axioms dubins_path_admissible
#print axioms witness_dubins
#print axioms mutant_no_dubins_false
#print axioms mutant_core_false

end LeanReal.Chap08Chronology
