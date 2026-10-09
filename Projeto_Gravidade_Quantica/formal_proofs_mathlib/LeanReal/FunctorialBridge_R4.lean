import Mathlib.Analysis.SpecialFunctions.SmoothTransition
import Mathlib.CategoryTheory.Category.Basic

/-!
# *Functorial Bridge* (Zenodo concept DOI 10.5281/zenodo.22441676), item R4

Source: `Manuscritos_Avulsos/paper_functorial_tensor_field_theory/paper_functorial_tensor_field_theory.tex`,
Definition `def:pathcat` and Lemma `lem:category`.

Paper:
> A morphism `D → D'` is either the formal identity `id_D`, of length `0` and only for `D' = D`,
> or a pair `(L, D(·))` with `L > 0` and `D(·)` a path of data of length `L` [...] that has
> *sitting instants*: for some `ε > 0`, `D(t) = D` for `t ∈ [0, ε]` and `D(t) = D'` for
> `t ∈ [L − ε, L]`. Composition is concatenation:
> `(L₂, D₂) ∘ (L₁, D₁) = (L₁ + L₂, D₁₂)`, `D₁₂(t) = D₁(t)` for `t ≤ L₁`, `D₂(t − L₁)` for `t ≥ L₁`,
> and `id` is a two-sided unit by definition.
>
> Lemma `lem:category`. `Path` is a category.
> Proof: `D₁₂` [...] is smooth [...] and it has sitting instants at both ends. The rank of `ρ`
> is the same on both pieces [...]. Both bracketings of a triple composite are the same function
> on `[0, L₁+L₂+L₃]`, so composition is strictly associative. Units hold by definition.

## What is formalized (option (a) of the plan, WITH smoothness)

* The space of data is an arbitrary real normed space `E`; the conditions a datum must satisfy
  (projectively immersed `𝒯`, `ρ` smooth of constant rank, ...) are an arbitrary predicate
  `Adm : E → Prop`, and a path must satisfy `Adm (f t)` for every `t ∈ [0, L]`.
* A path of length `L` is encoded as a map `f : ℝ → E` on the whole line, constant equal to `D`
  on `(-∞, ε]` and to `D'` on `[L - ε, ∞)`. Because of the sitting instants this is the same thing
  as a map on `[0, L]` (the constant extension is forced), and `ContDiff ℝ n f` on `ℝ` is the same
  as `C^n` on `[0, L]`: the forward direction is `contDiffOn_Icc` below, the converse is
  `contDiff_of_contDiffOn_Icc` (a `C^n` map on `[0, L]` with sitting instants extends to a `C^n`
  map on `ℝ`). The paper's "smooth" is `n = ⊤` (`C^∞`); every `n : ℕ∞` is covered.
* Concatenation is smooth, has sitting instants, and stays admissible (`concat`); it is strictly
  associative (`concat_assoc`); `Path` with the formal identities is a Mathlib
  `CategoryTheory.Category` (`instCategory`), so the unit and associativity laws are checked by
  Lean, not assumed.

## REDUCTION (declared)

* `E` is a NORMED space. The paper's data `(𝒯, Q, R, ρ, ψ)` are smooth fields on `ℳ`, and
  "path of data" (Definition `def:path`) means joint smoothness in `(x, t)`; that space is a
  Fréchet space, not a normed one, and the joint-smoothness notion is not modelled. The lemma's
  proof only uses that smoothness is local in `t` and that constants are smooth, which holds in
  both settings, but the Fréchet case is NOT formalized.
* The constraint "constant rank of `ρ`" is taken pointwise in `t` (inside `Adm`). The paper's
  sentence "the rank of `ρ` is the same on both pieces" is then automatic.
* The extra requirement `Ψ(·, t) = ψ(t)` of the paper is part of the datum and is not modelled
  separately.
-/

namespace LeanReal.FunctorialBridgeR4

open Set

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- A path of data of length `L > 0` from `D` to `D'` with sitting instants, of class `C^n`,
staying in the admissible set `Adm` on `[0, L]`. -/
structure SPath (n : ℕ∞) (Adm : E → Prop) (D D' : E) where
  L : ℝ
  L_pos : 0 < L
  f : ℝ → E
  smooth : ContDiff ℝ n f
  sit : ∃ ε > 0, (∀ t ≤ ε, f t = D) ∧ ∀ t, L - ε ≤ t → f t = D'
  adm : ∀ t ∈ Icc 0 L, Adm (f t)

namespace SPath

variable {n : ℕ∞} {Adm : E → Prop} {D D' D'' D''' : E}

@[ext]
theorem ext' {p q : SPath n Adm D D'} (hL : p.L = q.L) (hf : p.f = q.f) : p = q := by
  cases p; cases q; cases hL; cases hf; rfl

/-- Values before `0` and after `L` are forced. -/
theorem f_of_nonpos (p : SPath n Adm D D') {t : ℝ} (ht : t ≤ 0) : p.f t = D := by
  obtain ⟨ε, hε, h0, -⟩ := p.sit
  exact h0 t (ht.trans hε.le)

theorem f_of_ge (p : SPath n Adm D D') {t : ℝ} (ht : p.L ≤ t) : p.f t = D' := by
  obtain ⟨ε, hε, -, h1⟩ := p.sit
  exact h1 t (by linarith)

/-- The concatenated map: `p.f t` for `t ≤ p.L`, `q.f (t - p.L)` for `t > p.L`. -/
noncomputable def concatFun (p : SPath n Adm D D') (q : SPath n Adm D' D'') : ℝ → E :=
  fun t => if t ≤ p.L then p.f t else q.f (t - p.L)

/-- Concatenation (the paper's `(L₂, D₂) ∘ (L₁, D₁)`). -/
noncomputable def concat (p : SPath n Adm D D') (q : SPath n Adm D' D'') :
    SPath n Adm D D'' where
  L := p.L + q.L
  L_pos := add_pos p.L_pos q.L_pos
  f := concatFun p q
  smooth := by
    obtain ⟨ε₁, hε₁, h₁0, h₁1⟩ := p.sit
    obtain ⟨ε₂, hε₂, h₂0, h₂1⟩ := q.sit
    rw [contDiff_iff_contDiffAt]
    intro t
    by_cases ht : t < p.L + ε₂
    · -- near `t`, the concatenation equals `p.f`
      have : concatFun p q =ᶠ[nhds t] p.f := by
        filter_upwards [Iio_mem_nhds ht] with s hs
        simp only [concatFun]
        split_ifs with h
        · rfl
        · have h := lt_of_not_ge h
          rw [h₂0 _ (by simp only [mem_Iio] at hs; linarith), h₁1 _ (by linarith)]
      exact (p.smooth.contDiffAt).congr_of_eventuallyEq this
    · have ht := le_of_not_gt ht
      have : concatFun p q =ᶠ[nhds t] fun s => q.f (s - p.L) := by
        filter_upwards [Ioi_mem_nhds (show p.L - ε₁ < t by linarith)] with s hs
        simp only [concatFun]
        split_ifs with h
        · simp only [mem_Ioi] at hs
          rw [h₁1 _ hs.le, h₂0 _ (by linarith)]
        · rfl
      exact ((q.smooth.comp (contDiff_id.sub contDiff_const)).contDiffAt).congr_of_eventuallyEq
        this
  sit := by
    obtain ⟨ε₁, hε₁, h₁0, h₁1⟩ := p.sit
    obtain ⟨ε₂, hε₂, h₂0, h₂1⟩ := q.sit
    set m := min (min ε₁ ε₂) (min p.L q.L) with hm
    have hm0 : 0 < m := lt_min (lt_min hε₁ hε₂) (lt_min p.L_pos q.L_pos)
    have hm1 : m ≤ ε₁ := (min_le_left _ _).trans (min_le_left _ _)
    have hm2 : m ≤ ε₂ := (min_le_left _ _).trans (min_le_right _ _)
    have hm3 : m ≤ p.L := (min_le_right _ _).trans (min_le_left _ _)
    have hm4 : m ≤ q.L := (min_le_right _ _).trans (min_le_right _ _)
    refine ⟨m / 2, by linarith, fun t ht => ?_, fun t ht => ?_⟩
    · have h2 : t ≤ p.L := by linarith
      simp only [concatFun, h2, ite_true]
      exact h₁0 t (by linarith)
    · have h2 : ¬ t ≤ p.L := by intro h; linarith
      simp only [concatFun, h2, ite_false]
      exact h₂1 _ (by linarith)
  adm := by
    intro t ⟨h0, h1⟩
    simp only [concatFun]
    split_ifs with h
    · exact p.adm t ⟨h0, h⟩
    · have h := lt_of_not_ge h
      exact q.adm (t - p.L) ⟨by linarith, by linarith⟩

@[simp] theorem concat_L (p : SPath n Adm D D') (q : SPath n Adm D' D'') :
    (concat p q).L = p.L + q.L := rfl

@[simp] theorem concat_f (p : SPath n Adm D D') (q : SPath n Adm D' D'') :
    (concat p q).f = concatFun p q := rfl

/-- Strict associativity of concatenation: the two bracketings are equal as structures
(same length, same function on all of `ℝ`, hence on `[0, L₁+L₂+L₃]`). -/
theorem concat_assoc (p : SPath n Adm D D') (q : SPath n Adm D' D'')
    (r : SPath n Adm D'' D''') : concat (concat p q) r = concat p (concat q r) := by
  ext1
  · simp [add_assoc]
  · funext t
    simp only [concat_f, concat_L, concatFun]
    by_cases h1 : t ≤ p.L
    · have : t ≤ p.L + q.L := by linarith [q.L_pos]
      simp [h1, this]
    · by_cases h2 : t ≤ p.L + q.L
      · have h2' : t - p.L ≤ q.L := by linarith
        simp [h1, h2, h2']
      · have h2' : ¬ t - p.L ≤ q.L := by intro h; exact h2 (by linarith)
        simp only [h1, h2, h2', ite_false]
        congr 1
        ring

/-- Forward direction of the encoding: a path is `C^n` on `[0, L]` (the paper's notion). -/
theorem contDiffOn_Icc (p : SPath n Adm D D') : ContDiffOn ℝ n p.f (Icc 0 p.L) :=
  p.smooth.contDiffOn

end SPath

/-- Converse of the encoding: a map that is `C^n` on `[0, L]` and has sitting instants there
extends (constantly) to a `C^n` map on `ℝ`. So the `SPath` encoding loses nothing. -/
theorem contDiff_of_contDiffOn_Icc {n : ℕ∞} {D D' : E} {L ε : ℝ} (hε : 0 < ε) (hεL : ε < L)
    {g : ℝ → E} (hg : ContDiffOn ℝ n g (Icc 0 L))
    (h0 : ∀ t ∈ Icc 0 ε, g t = D) (h1 : ∀ t ∈ Icc (L - ε) L, g t = D') :
    ContDiff ℝ n (fun t => if t ≤ 0 then D else if L ≤ t then D' else g t) := by
  set G : ℝ → E := fun t => if t ≤ 0 then D else if L ≤ t then D' else g t with hG
  rw [contDiff_iff_contDiffAt]
  intro t
  by_cases ht0 : t < ε
  · have : G =ᶠ[nhds t] fun _ => D := by
      filter_upwards [Iio_mem_nhds ht0] with s hs
      simp only [mem_Iio] at hs
      simp only [hG]
      split_ifs with ha hb
      · rfl
      · exfalso; linarith
      · exact h0 s ⟨(lt_of_not_ge ha).le, hs.le⟩
    exact contDiffAt_const.congr_of_eventuallyEq this
  by_cases htL : L - ε < t
  · have : G =ᶠ[nhds t] fun _ => D' := by
      filter_upwards [Ioi_mem_nhds htL] with s hs
      simp only [mem_Ioi] at hs
      simp only [hG]
      split_ifs with ha hb
      · exfalso; linarith
      · rfl
      · exact h1 s ⟨hs.le, (lt_of_not_ge hb).le⟩
    exact contDiffAt_const.congr_of_eventuallyEq this
  have ht0 := le_of_not_gt ht0
  have htL := le_of_not_gt htL
  have htI : t ∈ Ioo 0 L := ⟨by linarith, by linarith⟩
  have hgt : ContDiffAt ℝ n g t :=
    (hg.mono Ioo_subset_Icc_self).contDiffAt (Ioo_mem_nhds htI.1 htI.2)
  have : G =ᶠ[nhds t] g := by
    filter_upwards [Ioo_mem_nhds htI.1 htI.2] with s hs
    simp only [hG, not_le.mpr hs.1, not_le.mpr hs.2, ite_false]
  exact hgt.congr_of_eventuallyEq this

/-! ## The category `Path` -/

/-- Objects: admissible data. -/
structure Obj (n : ℕ∞) (Adm : E → Prop) where
  D : E
  adm : Adm D

/-- Morphisms: the formal identity (only `D → D`), or a path with sitting instants. -/
inductive Mor {n : ℕ∞} {Adm : E → Prop} : Obj n Adm → Obj n Adm → Type _
  | ident (X : Obj n Adm) : Mor X X
  | path {X Y : Obj n Adm} (p : SPath n Adm X.D Y.D) : Mor X Y

namespace Mor

variable {n : ℕ∞} {Adm : E → Prop}

/-- Composition in diagrammatic order (`f ≫ g`): identities are units by definition,
two paths are concatenated. -/
noncomputable def comp : {X Y Z : Obj n Adm} → Mor X Y → Mor Y Z → Mor X Z
  | _, _, _, ident _, g => g
  | _, _, _, path p, ident _ => path p
  | _, _, _, path p, path q => path (SPath.concat p q)

end Mor

/-- **Lemma `lem:category`.** `Path` (data in `E`, admissibility `Adm`, regularity `C^n`) is a
category: the unit laws and STRICT associativity are proved by Lean. -/
noncomputable instance instCategory (n : ℕ∞) (Adm : E → Prop) :
    CategoryTheory.Category (Obj n Adm) where
  Hom := Mor
  id := Mor.ident
  comp := Mor.comp
  id_comp f := by cases f <;> rfl
  comp_id f := by cases f <;> rfl
  assoc f g h := by
    cases f with
    | ident => rfl
    | path p =>
      cases g with
      | ident => rfl
      | path q =>
        cases h with
        | ident => rfl
        | path r => exact congrArg Mor.path (SPath.concat_assoc p q r)

/-! ## Non-vacuity witness -/

/-- A smooth (`C^∞`) path in `E = ℝ` from `0` to `1` of length `3` with sitting margin `1`:
`f t = smoothTransition (t - 1)`. -/
noncomputable def witnessPath : SPath (⊤ : ℕ∞) (fun _ : ℝ => True) 0 1 where
  L := 3
  L_pos := by norm_num
  f := fun t => Real.smoothTransition (t - 1)
  smooth := Real.smoothTransition.contDiff.comp (contDiff_id.sub contDiff_const)
  sit := ⟨1, one_pos,
    fun t ht => Real.smoothTransition.zero_of_nonpos (by linarith),
    fun t ht => Real.smoothTransition.one_of_one_le (by linarith)⟩
  adm := fun _ _ => trivial

/-- The witness is not constant, so `Hom(0, 1)` contains a genuine (non-identity) morphism
between DIFFERENT objects, and composites of genuine paths exist. -/
theorem witness_nonvacuous :
    witnessPath.f 0 = 0 ∧ witnessPath.f 3 = 1 ∧
      (SPath.concat witnessPath (SPath.concat
        (⟨1, one_pos, fun _ => (1 : ℝ), contDiff_const,
          ⟨1, one_pos, fun _ _ => rfl, fun _ _ => rfl⟩, fun _ _ => trivial⟩ :
          SPath (⊤ : ℕ∞) (fun _ : ℝ => True) 1 1)
        (⟨1, one_pos, fun _ => (1 : ℝ), contDiff_const,
          ⟨1, one_pos, fun _ _ => rfl, fun _ _ => rfl⟩, fun _ _ => trivial⟩ :
          SPath (⊤ : ℕ∞) (fun _ : ℝ => True) 1 1))).L = 5 := by
  refine ⟨Real.smoothTransition.zero_of_nonpos (by norm_num),
    Real.smoothTransition.one_of_one_le (by norm_num), ?_⟩
  simp only [SPath.concat_L]
  show (3 : ℝ) + (1 + 1) = 5
  norm_num

/-! ## Mutant proved false: sitting instants are needed

Mutant: "the concatenation of two smooth paths is smooth" WITHOUT sitting instants. Counterexample
in `E = ℝ`: `f₁ t = t` on `[0, 1]` (from `0` to `1`), followed by the constant path at `1`. The
concatenation `t ↦ if t ≤ 1 then t else 1` is not even differentiable at the junction. -/

theorem mutant_no_sitting_false :
    ¬ DifferentiableAt ℝ (fun t : ℝ => if t ≤ 1 then t else (1 : ℝ)) 1 := by
  intro hd
  set g : ℝ → ℝ := fun t => if t ≤ 1 then t else 1 with hg
  have hD := hd.hasDerivAt
  -- on `Iic 1`, `g = id`, so the derivative within is `1`
  have hl : HasDerivWithinAt g 1 (Iic 1) 1 := by
    have : HasDerivWithinAt (fun t : ℝ => t) 1 (Iic 1) 1 := (hasDerivAt_id 1).hasDerivWithinAt
    refine this.congr (fun t ht => ?_) (by simp [hg])
    simp only [hg, mem_Iic] at ht ⊢
    simp [ht]
  -- on `Ici 1`, `g = 1`, so the derivative within is `0`
  have hr : HasDerivWithinAt g 0 (Ici 1) 1 := by
    have : HasDerivWithinAt (fun _ : ℝ => (1 : ℝ)) 0 (Ici 1) 1 :=
      (hasDerivAt_const (1 : ℝ) (1 : ℝ)).hasDerivWithinAt
    refine this.congr (fun t ht => ?_) (by simp [hg])
    simp only [hg, mem_Ici] at ht ⊢
    by_cases h : t ≤ 1
    · simp [le_antisymm h ht]
    · simp [h]
  have e1 : deriv g 1 = 1 :=
    (uniqueDiffWithinAt_Iic (1 : ℝ)).eq_deriv _ hD.hasDerivWithinAt hl
  have e0 : deriv g 1 = 0 :=
    (uniqueDiffWithinAt_Ici (1 : ℝ)).eq_deriv _ hD.hasDerivWithinAt hr
  rw [e1] at e0
  exact one_ne_zero e0

end LeanReal.FunctorialBridgeR4

#print axioms LeanReal.FunctorialBridgeR4.SPath.concat_assoc
#print axioms LeanReal.FunctorialBridgeR4.SPath.concat
#print axioms LeanReal.FunctorialBridgeR4.contDiff_of_contDiffOn_Icc
#print axioms LeanReal.FunctorialBridgeR4.instCategory
#print axioms LeanReal.FunctorialBridgeR4.witness_nonvacuous
#print axioms LeanReal.FunctorialBridgeR4.mutant_no_sitting_false
