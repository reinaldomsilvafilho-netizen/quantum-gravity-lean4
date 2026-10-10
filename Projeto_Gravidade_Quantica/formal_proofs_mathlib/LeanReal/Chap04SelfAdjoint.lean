import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.ZMod.Basic
import Mathlib.Basic.Complex.BigOperators
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# Book (Zenodo concept DOI 10.5281/zenodo.22290043), chapter 4, Self-Adjointness and Positivity

Source: `unified_quantum_gravity_book/chap04_simplicial_waves_porous_transport.tex`,
Definition "Fractional Simplicial Laplacian" (eq. `eq:simplicial_laplacian_def`) and
Proposition "Self-Adjointness and Positivity" (no label):
> `Δu(x) = (2α²I)⁻¹ ∫_{Δ(α)} K(y) [u(x+y) − 2u(x) + u(x−y)] dy`, and `−Δ` is linear, symmetric
> and positive semi-definite on `L²(ℝ^{m−1})`:
> `⟨u, −Δu⟩ = (2α²I)⁻¹ ∫ dx ∫_{Δ(α)} K(y) |u(x+y) − u(x)|² dy ≥ 0`.

Formal version (declared reduction): `ℝ^{m−1}` is replaced by a FINITE additive commutative
group `G` (for instance `ZMod N` or the discrete torus `(ZMod N)^{m−1}`), integrals by sums,
the kernel by an arbitrary weight `K : G → ℝ`, and the normalization `(2α²I)⁻¹` by a real
constant `c`. Functions are complex valued, `⟨u, v⟩ = ∑ₓ conj(u x) v x`.
* `lap_add`, `lap_smul`: linearity.
* `lap_symm`: `⟨v, Δu⟩ = ⟨Δv, u⟩` for every real `K` and `c` (translation invariance only).
* `form_identity`: `⟨u, −Δu⟩ = c ∑ₓ ∑_y K(y) |u(x+y) − u(x)|²`, the book's identity, for every
  real `K` and `c` (no sign condition).
* `form_nonneg`: the real number on the right is `≥ 0` when `c ≥ 0` and `K ≥ 0`.
* `form_eq_zero_of_const`: on a finite group constants are in the kernel, so the book's strict
  positivity (which uses Plancherel on `L²(ℝ^{m−1})` and the absence of constants there) has no
  finite analogue; the mutant `strict_mutant_false` records this.
* NOT covered: `L²(ℝ^{m−1})`, measurability and integrability, the Beta-kernel itself,
  Plancherel, the strict positivity on `L²(ℝ^{m−1})`, and the bound `−Δ ≤ 2/α²`.
-/

namespace LeanReal.Chap04SelfAdjoint

open Finset ComplexConjugate

variable {G : Type*} [AddCommGroup G] [Fintype G]

/-- Finite analogue of `eq:simplicial_laplacian_def`:
`Δu(x) = c ∑_y K(y) (u(x+y) − 2u(x) + u(x−y))`, with `c` standing for `(2α²I)⁻¹`. -/
def lap (c : ℝ) (K : G → ℝ) (u : G → ℂ) (x : G) : ℂ :=
  (c : ℂ) * ∑ y, (K y : ℂ) * (u (x + y) - 2 * u x + u (x - y))

/-- The `L²` inner product `⟨u, v⟩ = ∑ₓ conj(u x) v x` (conjugate-linear in the first slot). -/
def inner (u v : G → ℂ) : ℂ := ∑ x, conj (u x) * v x

/-- The Dirichlet form on the right of the book's identity:
`c ∑ₓ ∑_y K(y) |u(x+y) − u(x)|²`. -/
def form (c : ℝ) (K : G → ℝ) (u : G → ℂ) : ℝ :=
  c * ∑ x, ∑ y, K y * Complex.normSq (u (x + y) - u x)

/-- Linearity of `Δ` (additivity), Proposition "Self-Adjointness and Positivity". -/
theorem lap_add (c : ℝ) (K : G → ℝ) (u v : G → ℂ) (x : G) :
    lap c K (u + v) x = lap c K u x + lap c K v x := by
  simp only [lap, Pi.add_apply, ← mul_add, ← sum_add_distrib]
  congr 1; exact sum_congr rfl fun y _ => by ring

/-- Linearity of `Δ` (homogeneity), Proposition "Self-Adjointness and Positivity". -/
theorem lap_smul (c : ℝ) (K : G → ℝ) (a : ℂ) (u : G → ℂ) (x : G) :
    lap c K (a • u) x = a * lap c K u x := by
  simp only [lap, Pi.smul_apply, smul_eq_mul, mul_sum]
  exact sum_congr rfl fun y _ => by ring

/-- Translation invariance of a sum over a finite group. -/
lemma sum_shift (f : G → ℂ) (y : G) : ∑ x, f (x + y) = ∑ x, f x :=
  Fintype.sum_equiv (Equiv.addRight y) _ _ (fun _ => rfl)

/-- Expansion of `⟨v, Δu⟩` shift by shift. -/
lemma inner_lap (c : ℝ) (K : G → ℝ) (u v : G → ℂ) :
    inner v (lap c K u)
      = (c : ℂ) * ∑ y, (K y : ℂ) * ∑ x, conj (v x) * (u (x + y) - 2 * u x + u (x - y)) := by
  simp only [inner, lap, mul_sum]
  rw [sum_comm]
  exact sum_congr rfl fun y _ => sum_congr rfl fun x _ => by ring

/-- Expansion of `⟨Δv, u⟩` shift by shift (`c` and `K` are real). -/
lemma lap_inner (c : ℝ) (K : G → ℝ) (u v : G → ℂ) :
    inner (lap c K v) u
      = (c : ℂ) * ∑ y, (K y : ℂ) * ∑ x, conj (v (x + y) - 2 * v x + v (x - y)) * u x := by
  simp only [inner, lap, map_mul, map_sum, Complex.conj_ofReal, mul_sum, sum_mul]
  rw [sum_comm]
  exact sum_congr rfl fun y _ => sum_congr rfl fun x _ => by ring

/-- Symmetry of `Δ`: `⟨v, Δu⟩ = ⟨Δv, u⟩` for every real kernel and constant.
Proposition "Self-Adjointness and Positivity" ("symmetric"). -/
theorem lap_symm (c : ℝ) (K : G → ℝ) (u v : G → ℂ) :
    inner v (lap c K u) = inner (lap c K v) u := by
  -- per shift `y`: `∑ₓ v̄(x)(u(x+y) − 2u(x) + u(x−y)) = ∑ₓ conj(v(x+y) − 2v(x) + v(x−y)) u(x)`
  have key : ∀ y : G, ∑ x, conj (v x) * (u (x + y) - 2 * u x + u (x - y))
      = ∑ x, conj (v (x + y) - 2 * v x + v (x - y)) * u x := by
    intro y
    have h1 : ∑ x, conj (v x) * u (x + y) = ∑ x, conj (v (x - y)) * u x := by
      rw [← sum_shift (fun x => conj (v (x - y)) * u x) y]
      simp only [add_sub_cancel_right]
    have h2 : ∑ x, conj (v x) * u (x - y) = ∑ x, conj (v (x + y)) * u x := by
      rw [← sum_shift (fun x => conj (v x) * u (x - y)) y]
      simp only [add_sub_cancel_right]
    have e1 : ∑ x, conj (v x) * (u (x + y) - 2 * u x + u (x - y))
        = ∑ x, conj (v x) * u (x + y) - 2 * ∑ x, conj (v x) * u x
          + ∑ x, conj (v x) * u (x - y) := by
      rw [mul_sum, ← sum_sub_distrib, ← sum_add_distrib]
      exact sum_congr rfl fun x _ => by ring
    have e2 : ∑ x, conj (v (x + y) - 2 * v x + v (x - y)) * u x
        = ∑ x, conj (v (x + y)) * u x - 2 * ∑ x, conj (v x) * u x
          + ∑ x, conj (v (x - y)) * u x := by
      rw [mul_sum, ← sum_sub_distrib, ← sum_add_distrib]
      refine sum_congr rfl fun x _ => ?_
      simp only [map_add, map_sub, map_mul, map_ofNat]
      ring
    rw [e1, e2, h1, h2]; ring
  rw [inner_lap, lap_inner]
  congr 1
  exact sum_congr rfl fun y _ => by rw [key y]

/-- The book's identity, Proposition "Self-Adjointness and Positivity":
`⟨u, −Δu⟩ = c ∑ₓ ∑_y K(y) |u(x+y) − u(x)|²`, for every real `K` and `c`. -/
theorem form_identity (c : ℝ) (K : G → ℝ) (u : G → ℂ) :
    inner u (fun x => - lap c K u x) = (form c K u : ℂ) := by
  -- per shift `y`: `∑ₓ ū(x)(u(x+y) − 2u(x) + u(x−y)) = −∑ₓ |u(x+y) − u(x)|²`
  have key : ∀ y : G, ∑ x, conj (u x) * (u (x + y) - 2 * u x + u (x - y))
      = -∑ x, (Complex.normSq (u (x + y) - u x) : ℂ) := by
    intro y
    have h1 : ∑ x, conj (u (x + y)) * u (x + y) = ∑ x, conj (u x) * u x :=
      sum_shift (fun x => conj (u x) * u x) y
    have h2 : ∑ x, conj (u x) * u (x - y) = ∑ x, conj (u (x + y)) * u x := by
      rw [← sum_shift (fun x => conj (u x) * u (x - y)) y]
      simp only [add_sub_cancel_right]
    have e1 : ∑ x, conj (u x) * (u (x + y) - 2 * u x + u (x - y))
        = ∑ x, conj (u x) * u (x + y) - 2 * ∑ x, conj (u x) * u x
          + ∑ x, conj (u x) * u (x - y) := by
      rw [mul_sum, ← sum_sub_distrib, ← sum_add_distrib]
      exact sum_congr rfl fun x _ => by ring
    have e2 : ∑ x, (Complex.normSq (u (x + y) - u x) : ℂ)
        = ∑ x, conj (u (x + y)) * u (x + y) + ∑ x, conj (u x) * u x
          - ∑ x, conj (u x) * u (x + y) - ∑ x, conj (u (x + y)) * u x := by
      rw [← sum_add_distrib, ← sum_sub_distrib, ← sum_sub_distrib]
      refine sum_congr rfl fun x _ => ?_
      rw [Complex.normSq_eq_conj_mul_self]
      simp only [map_sub]; ring
    rw [e1, e2, h1, h2]; ring
  have hneg : inner u (fun x => - lap c K u x) = -inner u (lap c K u) := by
    simp only [inner, mul_neg, sum_neg_distrib]
  have hf : (form c K u : ℂ)
      = (c : ℂ) * ∑ y, (K y : ℂ) * ∑ x, (Complex.normSq (u (x + y) - u x) : ℂ) := by
    simp only [form]; push_cast
    rw [sum_comm]; simp only [mul_sum]
  rw [hneg, inner_lap, hf, ← mul_neg, ← sum_neg_distrib]
  congr 1
  exact sum_congr rfl fun y _ => by rw [key y]; ring

/-- Positivity, Proposition "Self-Adjointness and Positivity": the Dirichlet form is `≥ 0` when
the normalization `c` and the kernel `K` are non-negative. -/
theorem form_nonneg (c : ℝ) (K : G → ℝ) (hc : 0 ≤ c) (hK : ∀ y, 0 ≤ K y) (u : G → ℂ) :
    0 ≤ form c K u :=
  mul_nonneg hc (sum_nonneg fun _ _ => sum_nonneg fun y _ =>
    mul_nonneg (hK y) (Complex.normSq_nonneg _))

/-- Combined statement: `⟨u, −Δu⟩` is a non-negative real number. -/
theorem form_re_nonneg_im_zero (c : ℝ) (K : G → ℝ) (hc : 0 ≤ c) (hK : ∀ y, 0 ≤ K y)
    (u : G → ℂ) :
    0 ≤ (inner u (fun x => - lap c K u x)).re ∧ (inner u (fun x => - lap c K u x)).im = 0 := by
  rw [form_identity]
  exact ⟨by simpa using form_nonneg c K hc hK u, by simp⟩

/-- On a finite group, constants lie in the kernel of the form (no finite analogue of the
book's strict positivity, which uses that non-zero constants are not in `L²(ℝ^{m−1})`). -/
theorem form_eq_zero_of_const (c : ℝ) (K : G → ℝ) (a : ℂ) : form c K (fun _ => a) = 0 := by
  simp [form]

/-! ## Non-vacuity witness on `ZMod 4`: `K = 𝟙_{y=1}`, `c = 1/2`, `u = i·δ₀`.
Then `|u(x+1) − u(x)|² = 1` for `x = 0` and `x = 3`, and `0` otherwise, so the form is `1`,
strictly positive: the hypotheses bite and the conclusion is not the trivial `0`. -/

/-- Kernel supported at the shift `1`. -/
def Kw : ZMod 4 → ℝ := fun y => if y = 1 then 1 else 0

/-- `u = i·δ₀`, a genuinely complex test function. -/
def uw : ZMod 4 → ℂ := fun x => if x = 0 then Complex.I else 0

lemma Kw_nonneg : ∀ y, 0 ≤ Kw y := by
  intro y; unfold Kw; split_ifs <;> norm_num

/-- Sums over `ZMod 4` (definitionally `Fin 4`). -/
lemma sum_zmod4 {M : Type*} [AddCommMonoid M] (f : ZMod 4 → M) :
    ∑ x, f x = f 0 + f 1 + f 2 + f 3 :=
  Fin.sum_univ_four f

theorem witness_form : form (1 / 2) Kw uw = 1 := by
  simp only [form, Kw, uw, sum_zmod4]
  simp (config := {decide := true}) [Complex.normSq_apply]
  norm_num

example : inner uw (fun x => - lap (1 / 2) Kw uw x) = 1 := by
  rw [form_identity, witness_form]; simp

example : 0 < form (1 / 2) Kw uw := by rw [witness_form]; norm_num

/-! ## Mutants. -/

/-- Mutant 1 (drop `K ≥ 0`): with `K = −𝟙_{y=1}` the form is negative. -/
theorem nonneg_mutant_false :
    ¬ (∀ (K : ZMod 4 → ℝ) (u : ZMod 4 → ℂ), 0 ≤ form (1 / 2) K u) := by
  intro h
  have h1 := h (fun y => - Kw y) uw
  have h2 : form (1 / 2) (fun y => - Kw y) uw = - form (1 / 2) Kw uw := by
    simp only [form, neg_mul, sum_neg_distrib, mul_neg]
  rw [h2, witness_form] at h1
  norm_num at h1

/-- Mutant 2 (wrong constant): `⟨u, −Δu⟩ = 2c ∑∑ K|Δ_y u|²` is false. -/
theorem constant_mutant_false :
    ¬ (∀ (K : ZMod 4 → ℝ) (u : ZMod 4 → ℂ),
        inner u (fun x => - lap (1 / 2) K u x) = (form 1 K u : ℂ)) := by
  intro h
  have h1 := h Kw uw
  rw [form_identity, witness_form] at h1
  have h2 : form 1 Kw uw = 2 * form (1 / 2) Kw uw := by
    simp only [form]; ring
  rw [h2, witness_form] at h1
  norm_num at h1

/-- Mutant 3 (strict positivity on a finite group): `u ≠ 0 → ⟨u, −Δu⟩ > 0` fails, since the
constant `1` is a non-zero element of the kernel. -/
theorem strict_mutant_false :
    ¬ (∀ u : ZMod 4 → ℂ, u ≠ 0 → 0 < form (1 / 2) Kw u) := by
  intro h
  have h1 := h (fun _ => 1) (by
    intro h0; have := congrFun h0 0; simp at this)
  rw [form_eq_zero_of_const] at h1
  exact lt_irrefl _ h1

/-- One-sided difference operator `Du(x) = ∑_y K(y)(u(x+y) − u(x))`, used only as a mutant:
the book's operator is the symmetric second difference. -/
def fwd (K : G → ℝ) (u : G → ℂ) (x : G) : ℂ := ∑ y, (K y : ℂ) * (u (x + y) - u x)

/-- Mutant 4 (replace the symmetric second difference by a one-sided difference): symmetry
fails, with `K = 𝟙_{y=1}`, `u = δ₀`, `v = δ₃` on `ZMod 4` (`⟨v, Du⟩ = 1`, `⟨Dv, u⟩ = 0`). -/
theorem symm_mutant_false :
    ¬ (∀ (K : ZMod 4 → ℝ) (u v : ZMod 4 → ℂ), inner v (fwd K u) = inner (fwd K v) u) := by
  intro h
  have h1 := h Kw (fun x => if x = 0 then 1 else 0) (fun x => if x = 3 then 1 else 0)
  simp only [inner, fwd, Kw, sum_zmod4] at h1
  simp (config := {decide := true}) at h1

end LeanReal.Chap04SelfAdjoint

#print axioms LeanReal.Chap04SelfAdjoint.lap_add
#print axioms LeanReal.Chap04SelfAdjoint.lap_smul
#print axioms LeanReal.Chap04SelfAdjoint.lap_symm
#print axioms LeanReal.Chap04SelfAdjoint.form_identity
#print axioms LeanReal.Chap04SelfAdjoint.form_nonneg
#print axioms LeanReal.Chap04SelfAdjoint.form_re_nonneg_im_zero
#print axioms LeanReal.Chap04SelfAdjoint.form_eq_zero_of_const
#print axioms LeanReal.Chap04SelfAdjoint.witness_form
#print axioms LeanReal.Chap04SelfAdjoint.nonneg_mutant_false
#print axioms LeanReal.Chap04SelfAdjoint.constant_mutant_false
#print axioms LeanReal.Chap04SelfAdjoint.strict_mutant_false
#print axioms LeanReal.Chap04SelfAdjoint.symm_mutant_false
