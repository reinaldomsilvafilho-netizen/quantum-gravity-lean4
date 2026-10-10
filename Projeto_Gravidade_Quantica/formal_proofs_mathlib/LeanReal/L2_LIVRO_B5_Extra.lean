import LeanReal.Chap09Covering
import LeanReal.Chap08Chronology

/-!
# L2 LIVRO B5: complementos para `Chap09Covering` e `Chap08Chronology`

Revisao L2 independente. Tres pressupostos tacitos apontados pelo escritor sao aqui DESCARREGADOS
(mostram-se inofensivos):

1. `thm:unfolding` (cap. 9): a hipotese `T2Space E` sobre o recobrimento segue de `T2Space X`
   (todo recobrimento de um espaco de Hausdorff e de Hausdorff). Logo a forma do livro vale com
   Hausdorff so na base `Ω ∖ 𝒪`, que e um aberto do plano.
2. `prop:dubins_duality` (cap. 7): a hipotese `hne` (existe curva de comprimento `≤ L`) e
   dispensavel. Sem ela, os DOIS conjuntos cujo infimo se toma sao vazios, de modo que a
   igualdade vale em qualquer convencao para `inf ∅` (no livro, `+∞ = +∞`; em Lean, `0 = 0`).
3. `prop:causal_constraints` (2) (cap. 8): o escritor provou `κ*_wl = +∞` sobre a classe das
   curvas CAUSAIS; a classe do livro e a das curvas TIPO TEMPO, que esta contida nela (`I ⊆ J`).
   Aqui a forma com curvas tipo tempo.
-/

noncomputable section

namespace LeanReal.L2_LIVRO_B5_Extra

open Set Topology

/-! ## 1. Recobrimento de espaco de Hausdorff e de Hausdorff -/

/-- Um recobrimento `p : E → X` com `X` de Hausdorff tem `E` de Hausdorff. -/
theorem t2Space_of_isCoveringMap {E X : Type*} [TopologicalSpace E] [TopologicalSpace X]
    [T2Space X] {p : E → X} (cov : IsCoveringMap p) : T2Space E := by
  refine ⟨fun e₁ e₂ hne => ?_⟩
  by_cases h : p e₁ = p e₂
  · obtain ⟨s₁, s₂, h1, h2, m1, m2, hd⟩ := cov.isSeparatedMap e₁ e₂ h hne
    exact ⟨s₁, s₂, h1, h2, m1, m2, hd⟩
  · obtain ⟨u, v, hu, hv, mu, mv, hd⟩ := t2_separation h
    exact ⟨p ⁻¹' u, p ⁻¹' v, hu.preimage cov.continuous, hv.preimage cov.continuous, mu, mv,
      hd.preimage p⟩

/-- **`thm:unfolding`, forma do livro com Hausdorff so na base**: `p` recobrimento, `E`
simplesmente conexo, `X` de Hausdorff. O levantamento de um caminho irredutivel e um mergulho
fechado. -/
theorem unfolding_covering_T2base {E X : Type*} [TopologicalSpace E] [TopologicalSpace X]
    [T2Space X] {p : E → X} (cov : IsCoveringMap p) [SimplyConnectedSpace E] {a b : X}
    (γ : Path a b) (hirr : LeanReal.Chap09Covering.IsIrreducible γ) (e : E) (he : a = p e) :
    IsClosedEmbedding (cov.liftPath γ.toContinuousMap e (by simpa using he)) :=
  haveI := t2Space_of_isCoveringMap cov
  LeanReal.Chap09Covering.unfolding_covering cov γ hirr e he

/-- Aplicacao ao circulo (`ℝ/ℤ` e de Hausdorff). -/
example : IsClosedEmbedding
    (LeanReal.Chap09Covering.cov_circle.liftPath LeanReal.Chap09Covering.γ32.toContinuousMap 0
      (by simp)) :=
  unfolding_covering_T2base LeanReal.Chap09Covering.cov_circle LeanReal.Chap09Covering.γ32
    LeanReal.Chap09Covering.γ32_irreducible 0 (by simp)

/-! ## 2. Dualidade de Dubins sem `hne` -/

section Dubins

open LeanReal.Chap08Chronology

variable {Γ : Type*} {len peak : Γ → ℝ}

/-- Sem curva de comprimento `≤ L`, o conjunto `{κ > 0 : d κ ≤ L}` e VAZIO (usa `hDubins`). -/
theorem dubins_set_empty (hlen : ∀ γ, 0 ≤ len γ)
    (hDubins : ∀ κ, 0 < κ → ∃ γ, peak γ ≤ κ ∧ len γ = dubinsLength len peak κ)
    {L : ℝ} (hno : ¬ ∃ γ, len γ ≤ L) :
    {κ | 0 < κ ∧ dubinsLength len peak κ ≤ L} = ∅ := by
  refine eq_empty_of_forall_notMem fun κ hκ => hno ?_
  obtain ⟨γ, hl, -⟩ := (exists_admissible_iff hlen hDubins hκ.1).2 hκ.2
  exact ⟨γ, hl⟩

/-- **`prop:dubins_duality` (a) sem `hne`**: a igualdade vale sempre. -/
theorem dubins_duality_no_hne (hpeak : ∀ γ, 0 ≤ peak γ) (hlen : ∀ γ, 0 ≤ len γ)
    (hDubins : ∀ κ, 0 < κ → ∃ γ, peak γ ≤ κ ∧ len γ = dubinsLength len peak κ) (L : ℝ) :
    minimaxCurv len peak L = sInf {κ | 0 < κ ∧ dubinsLength len peak κ ≤ L} := by
  by_cases hne : ∃ γ, len γ ≤ L
  · exact dubins_duality hpeak hlen hDubins hne
  · have h1 : peak '' {γ | len γ ≤ L} = ∅ := by
      refine eq_empty_of_forall_notMem ?_
      rintro _ ⟨γ, hγ, rfl⟩
      exact hne ⟨γ, hγ⟩
    rw [minimaxCurv, h1, dubins_set_empty hlen hDubins hne]

end Dubins

/-! ## 3. `κ*_wl = +∞` sobre a classe TIPO TEMPO (a do livro) -/

section Chronology

open LeanReal.Chap08Chronology

variable {M : Type*}

/-- **`prop:causal_constraints` (2)**, classe do livro: com `I ⊆ J` e `J` transitiva, se
`p ∈ 𝓑` e `q ∉ 𝓑`, o infimo de qualquer custo sobre as curvas tipo tempo de `p` a `q` e `⊤`. -/
theorem kappa_wl_timelike_eq_top (I J : M → M → Prop) (hIJ : ∀ x y, I x y → J x y)
    (hJrefl : ∀ x, J x x) (hJtrans : ∀ x y z, J x y → J y z → J x z)
    (S : Set M) {p q : M} (hp : ¬ ∃ s ∈ S, J p s) (hq : ∃ s ∈ S, J q s)
    (cost : (ℝ → M) → ENNReal) :
    ⨅ (γ : ℝ → M) (_ : ∃ a b, a ≤ b ∧ γ a = p ∧ γ b = q ∧ IsTimelikeOn I γ a b), cost γ = ⊤ := by
  refine iInf_eq_top.2 fun γ => iInf_eq_top.2 fun h => ?_
  obtain ⟨a, b, hab, hpa, hqb, hγ⟩ := h
  refine absurd ?_ (not_J_of_mem_B J hJtrans S hp hq)
  have := (timelike_mem_J I J hIJ hJrefl hγ b ⟨hab, le_rfl⟩).1
  rwa [hpa, hqb] at this

end Chronology

#print axioms t2Space_of_isCoveringMap
#print axioms unfolding_covering_T2base
#print axioms dubins_set_empty
#print axioms dubins_duality_no_hne
#print axioms kappa_wl_timelike_eq_top

end LeanReal.L2_LIVRO_B5_Extra
