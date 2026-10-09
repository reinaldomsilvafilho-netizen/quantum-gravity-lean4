import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.Linarith

/-!
# *Functorial Bridge* (Zenodo concept DOI 10.5281/zenodo.22441676), item R3

Source: `Manuscritos_Avulsos/paper_functorial_tensor_field_theory/paper_functorial_tensor_field_theory.tex`,
Proposition `prop:noid` ("No identities"):
> Consider compact Lorentzian cobordisms between non-empty closed 3-manifolds, taken up to isometry
> relative to the boundary and composed by gluing. No morphism `e : Σ → Σ` satisfies `e∘e = e`.
> In particular, there are no identity morphisms.
> Proof (paper): `0 < Vol(e) < ∞`, volume is additive under gluing and invariant under isometry,
> so `Vol(e∘e) = 2 Vol(e) ≠ Vol(e)`.

Formal version (`no_idempotent`, `no_identity`). Declared reduction: ONLY the abstract argument.
* Objects form a type `Obj`, morphisms `Hom a b` a type family, composition `comp` a function
  (no associativity is needed or assumed), and `vol : Hom a b → ℝ` a function on morphisms.
  Hypotheses: `vol f > 0` for every morphism, and `vol (comp f g) = vol f + vol g`.
* The three geometric facts of the paper's proof enter as these hypotheses and are NOT proved:
  (i) positivity and finiteness of the volume of a compact cobordism with non-empty interior;
  (ii) additivity under gluing (the gluing hypersurface has measure zero);
  (iii) isometry invariance, which is what lets `vol` be a function on isometry CLASSES, i.e. on
  the morphisms of the paper.
* NOT covered: Lorentzian manifolds, cobordisms, gluing, the isometry quotient itself.
-/

namespace LeanReal.FunctorialBridge3

/-- A composition law on a type family of morphisms, with an additive, positive volume. -/
structure VolComp (Obj : Type*) (Hom : Obj → Obj → Type*) where
  comp : ∀ {a b c : Obj}, Hom a b → Hom b c → Hom a c
  vol : ∀ {a b : Obj}, Hom a b → ℝ
  vol_pos : ∀ {a b : Obj} (f : Hom a b), 0 < vol f
  vol_comp : ∀ {a b c : Obj} (f : Hom a b) (g : Hom b c), vol (comp f g) = vol f + vol g

variable {Obj : Type*} {Hom : Obj → Obj → Type*}

/-- Prop. `prop:noid`: no morphism `e : Σ → Σ` with `e ∘ e = e`. -/
theorem no_idempotent (C : VolComp Obj Hom) (S : Obj) : ¬ ∃ e : Hom S S, C.comp e e = e := by
  rintro ⟨e, he⟩
  have h := C.vol_comp e e
  rw [he] at h
  linarith [C.vol_pos e]

/-- "In particular, there are no identity morphisms": no `i : Σ → Σ` is a left unit, even for
endomorphisms of `Σ` alone. -/
theorem no_identity (C : VolComp Obj Hom) (S : Obj) :
    ¬ ∃ i : Hom S S, ∀ f : Hom S S, C.comp i f = f :=
  fun ⟨i, hi⟩ => no_idempotent C S ⟨i, hi i⟩

/-! ## Non-vacuity: one object, morphisms = positive reals ("lengths of cylinders"),
composition = addition, `vol` = the length. All hypotheses hold. -/

/-- The witness structure. -/
def lengths : VolComp Unit (fun _ _ => {x : ℝ // 0 < x}) where
  comp f g := ⟨f.1 + g.1, add_pos f.2 g.2⟩
  vol f := f.1
  vol_pos f := f.2
  vol_comp _ _ := rfl

example : (@VolComp.comp _ _ lengths () () () ⟨1, one_pos⟩ ⟨2, two_pos⟩).1 = 3 := by
  simp only [lengths]; norm_num

example : ¬ ∃ e : {x : ℝ // 0 < x}, @VolComp.comp _ _ lengths () () () e e = e := no_idempotent lengths ()

/-! ## Mutant: weaken `0 < vol` to `0 ≤ vol`. False: one object, one morphism, `vol = 0`,
and that morphism is idempotent. -/

/-- The mutated statement, with `0 ≤ vol` in place of `0 < vol`. -/
def MutantStatement : Prop :=
  ∀ (Hom : Unit → Unit → Type) (comp : ∀ {a b c : Unit}, Hom a b → Hom b c → Hom a c)
    (vol : ∀ {a b : Unit}, Hom a b → ℝ),
    (∀ {a b : Unit} (f : Hom a b), 0 ≤ vol f) →
    (∀ {a b c : Unit} (f : Hom a b) (g : Hom b c), vol (comp f g) = vol f + vol g) →
    ¬ ∃ e : Hom () (), comp e e = e

theorem noid_mutant_false : ¬ MutantStatement := by
  intro h
  exact h (fun _ _ => Unit) (fun _ _ => ()) (fun _ => 0) (fun _ => le_refl 0)
    (fun _ _ => by norm_num) ⟨(), rfl⟩

end LeanReal.FunctorialBridge3

#print axioms LeanReal.FunctorialBridge3.no_idempotent
#print axioms LeanReal.FunctorialBridge3.no_identity
#print axioms LeanReal.FunctorialBridge3.noid_mutant_false
