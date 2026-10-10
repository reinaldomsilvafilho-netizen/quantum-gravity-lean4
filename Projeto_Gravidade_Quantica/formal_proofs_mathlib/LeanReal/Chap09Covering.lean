import Mathlib.Topology.Homotopy.Lifting
import Mathlib.Topology.Subpath
import Mathlib.Topology.Covering.AddCircle
import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Topology.Instances.ZMultiples
import Mathlib.Analysis.Convex.Contractible

/-!
# Capitulo 9: desdobramento no recobrimento (`thm:unfolding`) e holonomia (`prop:holonomy`)

Fonte: `unified_quantum_gravity_book/chap09_global_homotopy_covering_spaces_jordan_loops.tex`.

## Item 9.5, `thm:unfolding`

> An immersed path `γ : [0,1] → Ω ∖ 𝒪` is *irreducible* if it contains no self-intersection
> `γ(t_a) = γ(t_b)`, `t_a < t_b`, whose intermediate loop `γ|[t_a,t_b]` is null-homotopic in
> `Ω ∖ 𝒪`. Every lift `γ̃ : [0,1] → Ω̃` (universal cover) of an irreducible immersed path is
> injective, hence an embedding.

Reducao declarada (quase fiel):
* `X` espaco topologico qualquer (no livro, o espaco livre `Ω ∖ 𝒪`); `p : E → X` so
  **continua** e `E` `SimplyConnectedSpace` (o livro usa o recobrimento universal; a prova so usa
  que `p` e continua e `E` simplesmente conexo). A forma do livro, com `p` recobrimento e o
  levantamento obtido por `IsCoveringMap.liftPath`, e o corolario `unfolding_covering`.
* "Imersao" nao entra: a prova e topologica e nao usa a derivada. A hipotese foi omitida.
* "Laco intermediario nulo-homotopico": `γ.subpath s t` (reparametrizado em `[0,1]`) homotopico
  rel pontas ao caminho constante (`Path.refl`, transportado por `Path.cast`).
* "Mergulho": `Topology.IsClosedEmbedding`, com `E` de Hausdorff (o recobrimento universal de um
  aberto do plano e Hausdorff; o livro usa isso implicitamente).
* Recíproca (nao esta no livro, mas mostra que a definicao nao e vazia): para `p` recobrimento,
  um caminho cujo levantamento e injetivo e irredutivel (`irreducible_of_lift_injective`).

## Item 9.1, `prop:holonomy`, versao do grupoide

> `ρ : F_m → SU(2)` injetiva, `A` conexao plana com holonomia `ρ`. Para caminhos `γ, γ'` de `p`
> a `q`: `Hol(γ,A) = Hol(γ',A) ⟺ [γ] = [γ']` em `π₁(Ω ∖ 𝒪, p, q)`.

Reducao declarada (categorica): a holonomia de uma conexao plana e um funtor
`Hol : π₁(X) ⥤ D` do grupoide fundamental (`Hol(γ * γ') = Hol γ · Hol γ'`, so depende da classe
rel pontas; isto e o que a prova do livro usa). O teorema abstrato: um funtor de um grupoide
conexo, injetivo no grupo de vertices de um ponto `x₀`, e fiel. NAO entram: conexoes planas,
`𝒫exp`, a serie de Dyson, `SU(2)`, a existencia de `F_m ↪ SU(2)` (Swierczkowski) nem
`π₁ ≅ F_m`. A injetividade de `ρ` entra como hipotese `hinj` sobre o funtor.
Instancia concreta (testemunha): a monodromia do recobrimento `ℝ → ℝ/ℤ`, que e a holonomia de
uma conexao plana com grupo estrutural discreto, e fiel; e o grupo de vertices nao e trivial.
-/

noncomputable section

namespace LeanReal.Chap09Covering

open unitInterval CategoryTheory Function Topology

variable {X E : Type*} [TopologicalSpace X] [TopologicalSpace E]

/-! ## Item 9.5: definicoes -/

/-- O sublaco `γ|[s,t]` e um laco (`γ s = γ t`) nulo-homotopico rel pontas em `X`
(definicao "Irreducible immersion", cap. 9, antes de `thm:unfolding`). -/
def HasNullSubloop {a b : X} (γ : Path a b) (s t : I) : Prop :=
  ∃ h : γ s = γ t, (γ.subpath s t).Homotopic ((Path.refl (γ s)).cast rfl h.symm)

/-- Caminho **irredutivel** (cap. 9): nenhuma autointersecao `γ(s) = γ(t)`, `s < t`, tem sublaco
nulo-homotopico. -/
def IsIrreducible {a b : X} (γ : Path a b) : Prop :=
  ∀ s t : I, s < t → ¬ HasNullSubloop γ s t

/-- Num espaco simplesmente conexo `E`, toda autointersecao de `Γ` da um sublaco nulo-homotopico
na imagem por `p` continua. -/
theorem hasNullSubloop_map [SimplyConnectedSpace E] {p : E → X} (hp : Continuous p)
    {ea eb : E} (Γ : Path ea eb) (s t : I) (h : Γ s = Γ t) :
    HasNullSubloop (Γ.map hp) s t := by
  refine ⟨congrArg p h, ?_⟩
  have H := SimplyConnectedSpace.paths_homotopic (Γ.subpath s t)
    ((Path.refl (Γ s)).cast rfl h.symm)
  exact H.map ⟨p, hp⟩

/-- **`thm:unfolding`** (nucleo): se `E` e simplesmente conexo, `p : E → X` continua e a imagem
`p ∘ Γ` e irredutivel, entao `Γ` e injetiva. -/
theorem lift_injective_of_irreducible [SimplyConnectedSpace E] {p : E → X} (hp : Continuous p)
    {ea eb : E} (Γ : Path ea eb) (hirr : IsIrreducible (Γ.map hp)) : Injective Γ := by
  intro s t hst
  by_contra hne
  rcases lt_or_gt_of_ne hne with h | h
  · exact hirr s t h (hasNullSubloop_map hp Γ s t hst)
  · exact hirr t s h (hasNullSubloop_map hp Γ t s hst.symm)

/-- **`thm:unfolding`**, forma com um caminho `γ` em `X` e um levantamento `Γ` qualquer
(`p ∘ Γ = γ`): se `γ` e irredutivel, `Γ` e injetiva. -/
theorem lift_injective {p : E → X} [SimplyConnectedSpace E] (hp : Continuous p)
    {a b : X} (γ : Path a b) {ea eb : E} (Γ : Path ea eb) (hlift : ∀ t, p (Γ t) = γ t)
    (hirr : IsIrreducible γ) : Injective Γ := by
  have ha : a = p ea := by rw [← γ.source, ← hlift 0, Γ.source]
  have hb : b = p eb := by rw [← γ.target, ← hlift 1, Γ.target]
  subst ha hb
  have hγ : γ = Γ.map hp := by ext t; exact (hlift t).symm
  subst hγ
  exact lift_injective_of_irreducible hp Γ hirr

/-- **`thm:unfolding`**, "hence an embedding": com `E` de Hausdorff o levantamento e um mergulho
fechado. -/
theorem lift_isClosedEmbedding {p : E → X} [SimplyConnectedSpace E] [T2Space E]
    (hp : Continuous p) {a b : X} (γ : Path a b) {ea eb : E} (Γ : Path ea eb)
    (hlift : ∀ t, p (Γ t) = γ t) (hirr : IsIrreducible γ) : IsClosedEmbedding Γ :=
  Γ.continuous.isClosedEmbedding (lift_injective hp γ Γ hlift hirr)

/-- **`thm:unfolding`, forma do livro**: `p : E → X` recobrimento, `E` simplesmente conexo e de
Hausdorff (recobrimento universal). Para todo ponto `e` sobre `γ(0)`, o levantamento de `γ` que
comeca em `e` existe e e um mergulho fechado. -/
theorem unfolding_covering {p : E → X} (cov : IsCoveringMap p) [SimplyConnectedSpace E]
    [T2Space E] {a b : X} (γ : Path a b) (hirr : IsIrreducible γ) (e : E) (he : a = p e) :
    IsClosedEmbedding (cov.liftPath γ.toContinuousMap e (by simpa using he)) := by
  set L := cov.liftPath γ.toContinuousMap e (by simpa using he)
  have hl : ∀ t, p (L t) = γ t := fun t => congrFun (cov.liftPath_lifts _ e _) t
  let Γ : Path e (L 1) := ⟨L, cov.liftPath_zero _ e _, rfl⟩
  exact lift_isClosedEmbedding cov.continuous γ Γ hl hirr

/-- **Reciproca** (fora do livro): para `p` recobrimento, se o levantamento `Γ` e injetivo, a
imagem `p ∘ Γ` e irredutivel (monodromia: lacos homotopicos levantam com o mesmo ponto final). -/
theorem irreducible_of_lift_injective {p : E → X} (cov : IsCoveringMap p) {ea eb : E}
    (Γ : Path ea eb) (hinj : Injective Γ) : IsIrreducible (Γ.map cov.continuous) := by
  rintro s t hst ⟨h, H⟩
  set γ₀ : C(I, X) := ((Γ.map cov.continuous).subpath s t).toContinuousMap
  set γ₁ : C(I, X) := ((Path.refl ((Γ.map cov.continuous) s)).cast rfl h.symm).toContinuousMap
  have h₀ : γ₀ 0 = p (Γ s) := ((Γ.map cov.continuous).subpath s t).source
  have h₁ : γ₁ 0 = p (Γ s) := rfl
  have key := cov.liftPath_apply_one_eq_of_homotopicRel (γ₀ := γ₀) (γ₁ := γ₁) H (Γ s) h₀ h₁
  have e1 : cov.liftPath γ₀ (Γ s) h₀ = (Γ.subpath s t).toContinuousMap :=
    ((cov.eq_liftPath_iff' _).mpr ⟨funext fun _ => rfl, (Γ.subpath s t).source⟩).symm
  have e2 : cov.liftPath γ₁ (Γ s) h₁ = ContinuousMap.const I (Γ s) :=
    ((cov.eq_liftPath_iff' (Γ := ContinuousMap.const I (Γ s)) _).mpr
      ⟨funext fun _ => rfl, rfl⟩).symm
  rw [e1, e2] at key
  have k1 : (Γ.subpath s t).toContinuousMap 1 = Γ t := (Γ.subpath s t).target
  rw [k1, ContinuousMap.const_apply] at key
  exact (ne_of_lt hst) (hinj key.symm)

/-- Para `p` recobrimento e `E` simplesmente conexo: `p ∘ Γ` irredutivel `↔` `Γ` injetiva. -/
theorem irreducible_iff_lift_injective {p : E → X} (cov : IsCoveringMap p)
    [SimplyConnectedSpace E] {ea eb : E} (Γ : Path ea eb) :
    IsIrreducible (Γ.map cov.continuous) ↔ Injective Γ :=
  ⟨lift_injective_of_irreducible cov.continuous Γ, irreducible_of_lift_injective cov Γ⟩

/-! ## Item 9.1: holonomia como funtor do grupoide -/

/-- **`prop:holonomy`, versao do grupoide** (abstrata): um funtor `F` de um grupoide em que todo
objeto e alcancavel a partir de `x₀`, injetivo em `End x₀`, e fiel. -/
theorem faithful_of_injective_vertex {C D : Type*} [Groupoid C] [Category D] (F : C ⥤ D)
    (x₀ : C) (hconn : ∀ x : C, Nonempty (x₀ ⟶ x))
    (hinj : Injective (fun f : x₀ ⟶ x₀ => F.map f)) : F.Faithful where
  map_injective {x y} f g hfg := by
    obtain ⟨α⟩ := hconn x
    obtain ⟨β⟩ := hconn y
    have : α ≫ f ≫ Groupoid.inv β = α ≫ g ≫ Groupoid.inv β := hinj (by simp [hfg])
    exact (cancel_mono (Groupoid.inv β)).1 ((cancel_epi α).1 this)

/-- **`prop:holonomy`** no grupoide fundamental: `X` conexo por caminhos, `Hol : π₁(X) ⥤ D`
injetivo no grupo de vertices de `x₀`. Para caminhos `γ, γ'` de `x` a `y`:
`Hol [γ] = Hol [γ'] ↔ γ ≃ γ'` rel pontas. -/
theorem holonomy_separates [PathConnectedSpace X] {D : Type*} [Category D]
    (Hol : FundamentalGroupoid X ⥤ D) (x₀ : X)
    (hinj : Injective (fun f : FundamentalGroupoid.mk x₀ ⟶ FundamentalGroupoid.mk x₀ => Hol.map f))
    {x y : X} (γ γ' : Path x y) :
    Hol.map (FundamentalGroupoid.fromPath (Path.Homotopic.Quotient.mk γ)) =
        Hol.map (FundamentalGroupoid.fromPath (Path.Homotopic.Quotient.mk γ')) ↔
      γ.Homotopic γ' := by
  have hF : Hol.Faithful := faithful_of_injective_vertex Hol _
    (fun z => ⟨FundamentalGroupoid.fromPath ⟦(PathConnectedSpace.joined x₀ z.as).somePath⟧⟩) hinj
  refine ⟨fun h => ?_, fun h => ?_⟩
  · exact (FundamentalGroupoid.fromPath_eq_iff_homotopic γ γ').1 (Hol.map_injective h)
  · exact congrArg Hol.map ((FundamentalGroupoid.fromPath_eq_iff_homotopic γ γ').2 h)

/-! ## Testemunhas: o recobrimento `ℝ → ℝ/ℤ` (`AddCircle 1`)

O circulo e o espaco livre de um unico obstaculo, a menos de homotopia; `ℝ` e o seu recobrimento
universal. -/

/-- O circulo `ℝ/ℤ`. -/
abbrev T := AddCircle (1 : ℝ)

/-- A projecao `ℝ → ℝ/ℤ` e um recobrimento (Mathlib). -/
theorem cov_circle : IsCoveringMap ((↑) : ℝ → T) := AddCircle.isCoveringMap_coe 1

/-- Levantamento `Γ(t) = 3t/2`: no circulo, uma volta e meia. -/
def Γ32 : Path (0 : ℝ) (3 / 2) where
  toFun t := 3 / 2 * (t : ℝ)
  continuous_toFun := by fun_prop
  source' := by simp
  target' := by norm_num

theorem Γ32_injective : Injective Γ32 := by
  intro s t h
  have h' : (3 / 2 : ℝ) * s = 3 / 2 * t := h
  exact Subtype.ext (by linarith)

/-- O caminho `γ = p ∘ Γ32` no circulo (uma volta e meia). -/
def γ32 : Path ((0 : ℝ) : T) ((3 / 2 : ℝ) : T) := Γ32.map cov_circle.continuous

/-- `γ32` e irredutivel (pela reciproca). -/
theorem γ32_irreducible : IsIrreducible γ32 :=
  irreducible_of_lift_injective cov_circle Γ32 Γ32_injective

/-- ... mas `γ32` NAO e injetiva: `γ(0) = γ(2/3)`. Logo a hipotese de irredutibilidade nao forca a
injetividade em `X`; o teorema so afirma injetividade no recobrimento. -/
theorem γ32_not_injective : ¬ Injective γ32 := by
  intro hinj
  have h : γ32 0 = γ32 ⟨2 / 3, by norm_num, by norm_num⟩ := by
    show (((3 / 2 : ℝ) * (0 : ℝ) : ℝ) : T) = (((3 / 2 : ℝ) * (2 / 3 : ℝ) : ℝ) : T)
    norm_num [AddCircle.coe_period]
  have := congrArg Subtype.val (hinj h)
  norm_num at this

/-- **Testemunha nao degenerada de `thm:unfolding`**: `γ32` e irredutivel, nao e injetiva no
circulo, e o seu levantamento a `ℝ` e um mergulho fechado (conclusao do teorema). -/
theorem witness_unfolding :
    IsIrreducible γ32 ∧ ¬ Injective γ32 ∧ IsClosedEmbedding Γ32 :=
  ⟨γ32_irreducible, γ32_not_injective,
    lift_isClosedEmbedding cov_circle.continuous γ32 Γ32 (fun _ => rfl) γ32_irreducible⟩

/-- A forma do livro aplicada ao circulo (o levantamento por `liftPath` existe e e mergulho). -/
example : IsClosedEmbedding (cov_circle.liftPath γ32.toContinuousMap 0 (by simp)) :=
  unfolding_covering cov_circle γ32 γ32_irreducible 0 (by simp)

/-! ## Mutantes de `thm:unfolding` provados FALSOS -/

/-- Mutante 1 (sem `E` simplesmente conexo): falso, com `E = X = ℝ/ℤ`, `p = id`, `Γ = γ32`. -/
theorem mutant_no_simply_connected_false :
    ¬ (∀ (E X : Type) [TopologicalSpace E] [TopologicalSpace X] (p : E → X) (hp : Continuous p)
        (ea eb : E) (Γ : Path ea eb), IsIrreducible (Γ.map hp) → Injective Γ) := by
  intro h
  exact γ32_not_injective (h T T id continuous_id _ _ γ32 (by rw [Path.map_id]; exact γ32_irreducible))

/-- Caminho `t ↦ t - t²` em `ℝ`, de `0` a `0`. -/
def bump : Path (0 : ℝ) 0 where
  toFun t := (t : ℝ) - (t : ℝ) ^ 2
  continuous_toFun := by fun_prop
  source' := by simp
  target' := by simp

/-- Mutante 2 (sem irredutibilidade): falso; o levantamento `id` de `bump` nao e injetivo. -/
theorem mutant_no_irreducible_false :
    ¬ (∀ (ea eb : ℝ) (Γ : Path ea eb), Injective Γ) := by
  intro h
  have := h 0 0 bump (show bump 0 = bump 1 by simp [bump])
  exact zero_ne_one this

/-! ## Testemunha de `prop:holonomy`: a monodromia de `ℝ → ℝ/ℤ` -/

/-- Ponto base `x₀ = [0]` do circulo. -/
abbrev x₀ : T := ((0 : ℝ) : T)

/-- A monodromia (holonomia do fibrado plano `ℝ → ℝ/ℤ`) como funtor do grupoide fundamental. -/
abbrev Hol : FundamentalGroupoid T ⥤ Type := cov_circle.monodromyFunctor

/-- `Hol` e injetivo no grupo de vertices de `x₀` (pois `ℝ` e simplesmente conexo). -/
theorem Hol_injective_vertex :
    Injective (fun f : FundamentalGroupoid.mk x₀ ⟶ FundamentalGroupoid.mk x₀ => Hol.map f) := by
  intro f g hfg
  apply (AddCircle.isAddQuotientCoveringMap_coe (1 : ℝ)).monodromyPerm_injective (x := x₀)
  apply Equiv.ext
  intro e
  have := congrArg (fun h => h e) hfg
  exact this

/-- O laco fundamental `t ↦ [t]` em `ℝ/ℤ`. -/
def loop : Path x₀ x₀ where
  toFun t := (((t : ℝ)) : T)
  continuous_toFun := cov_circle.continuous.comp continuous_subtype_val
  source' := rfl
  target' := by simp [AddCircle.coe_period]

/-- O levantamento de `loop` a partir de `0`. -/
def Γ01 : Path (0 : ℝ) 1 where
  toFun t := (t : ℝ)
  continuous_toFun := continuous_subtype_val
  source' := rfl
  target' := rfl

/-- `loop` nao e nulo-homotopico: o grupo de vertices de `x₀` nao e trivial. -/
theorem loop_not_null : ¬ loop.Homotopic (Path.refl x₀) := by
  intro H
  have h₀ : loop.toContinuousMap 0 = ((↑) : ℝ → T) 0 := rfl
  have h₁ : (Path.refl x₀).toContinuousMap 0 = ((↑) : ℝ → T) 0 := rfl
  have key := cov_circle.liftPath_apply_one_eq_of_homotopicRel H (0 : ℝ) h₀ h₁
  have e1 : cov_circle.liftPath loop.toContinuousMap 0 h₀ = Γ01.toContinuousMap :=
    ((cov_circle.eq_liftPath_iff' (Γ := Γ01.toContinuousMap) _).mpr ⟨funext fun _ => rfl, rfl⟩).symm
  have e2 : cov_circle.liftPath (Path.refl x₀).toContinuousMap 0 h₁ = ContinuousMap.const I 0 :=
    ((cov_circle.eq_liftPath_iff' (Γ := ContinuousMap.const I (0 : ℝ)) _).mpr
      ⟨funext fun _ => rfl, rfl⟩).symm
  rw [e1, e2] at key
  have : (1 : ℝ) = 0 := key
  exact one_ne_zero this

/-- **Testemunha nao degenerada de `prop:holonomy`**: o grupo de vertices tem dois elementos
distintos (`[loop] ≠ 1`) e a holonomia os separa, pelo teorema. -/
theorem witness_holonomy :
    (FundamentalGroupoid.fromPath (Path.Homotopic.Quotient.mk loop) ≠
        𝟙 (FundamentalGroupoid.mk x₀)) ∧
      Hol.map (FundamentalGroupoid.fromPath (Path.Homotopic.Quotient.mk loop)) ≠
        Hol.map (FundamentalGroupoid.fromPath (Path.Homotopic.Quotient.mk (Path.refl x₀))) := by
  refine ⟨fun h => loop_not_null ((FundamentalGroupoid.fromPath_eq_iff_homotopic _ _).1 h),
    fun h => loop_not_null ((holonomy_separates Hol x₀ Hol_injective_vertex _ _).1 h)⟩

/-! ## Mutante de `prop:holonomy` provado FALSO -/

/-- Mutante (sem a injetividade no grupo de vertices): falso; o funtor constante do grupoide
fundamental do circulo num ponto nao e fiel. -/
theorem mutant_no_injective_false :
    ¬ (∀ (C : Type) [Groupoid.{0} C] (F : C ⥤ Discrete PUnit.{1}) (z : C),
        (∀ x : C, Nonempty (z ⟶ x)) → F.Faithful) := by
  intro h
  have hF := h (FundamentalGroupoid T) (Functor.star _) (FundamentalGroupoid.mk x₀)
    (fun z => ⟨FundamentalGroupoid.fromPath
      (Path.Homotopic.Quotient.mk (PathConnectedSpace.joined x₀ z.as).somePath)⟩)
  have := (Functor.star (FundamentalGroupoid T)).map_injective
    (X := FundamentalGroupoid.mk x₀) (Y := FundamentalGroupoid.mk x₀)
    (a₁ := FundamentalGroupoid.fromPath (Path.Homotopic.Quotient.mk loop))
    (a₂ := 𝟙 _) (Subsingleton.elim _ _)
  exact witness_holonomy.1 this

/-! ## Axiomas -/

#print axioms hasNullSubloop_map
#print axioms lift_injective_of_irreducible
#print axioms lift_injective
#print axioms lift_isClosedEmbedding
#print axioms unfolding_covering
#print axioms irreducible_of_lift_injective
#print axioms irreducible_iff_lift_injective
#print axioms faithful_of_injective_vertex
#print axioms holonomy_separates
#print axioms witness_unfolding
#print axioms mutant_no_simply_connected_false
#print axioms mutant_no_irreducible_false
#print axioms Hol_injective_vertex
#print axioms loop_not_null
#print axioms witness_holonomy
#print axioms mutant_no_injective_false

end LeanReal.Chap09Covering
