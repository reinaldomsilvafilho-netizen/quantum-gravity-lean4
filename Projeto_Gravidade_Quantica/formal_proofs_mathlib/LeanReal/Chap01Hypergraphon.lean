import Mathlib.Data.Fintype.Pi
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Order.ConditionallyCompleteLattice.Basic
import Mathlib.Tactic

/-!
# Book, Chapter 1, `thm:hypergraphon_compactness`(i): multilinear cut norm vs. operator norm

Source: `unified_quantum_gravity_book/chap01_*.tex`, Definition "k-Hypergraphon and Multilinear
Cut Norm" (eq. `eq:hypergraphon_cutnorm`) and Theorem `thm:hypergraphon_compactness`, item (i):

> `‖W‖_{□,k} := sup_{S_1,…,S_k ⊆ [0,1]} |∫_{S_1 × ⋯ × S_k} W|`, and
> `‖W‖_{□,k} ≤ ‖T_W‖_{L^∞ × ⋯ × L^∞ → ℝ} ≤ 2^k ‖W‖_{□,k}`.
> [Proof: split each `u^{(α)} = u_+^{(α)} − u_−^{(α)}` into `2^k` signed orthant integrals; the
> form with `0 ≤ u^{(α)} ≤ 1` is affine in each factor separately, so, fixing all factors but
> one, that factor can be replaced by an indicator `𝟙_{S_α}` without decreasing the value; doing
> this for `α = 1,…,k` in turn bounds each orthant integral by `|∫_{S_1 × ⋯ × S_k} W| ≤ ‖W‖_{□,k}`.]

REDUCTION (declared). Only the FINITE `k`-LINEAR case is formalized, extending
`BeyondSpectrum1_B4` (the bilinear case `k = 2`): `[0,1]` is replaced by finite index sets `ι a`,
one per factor `a : A` (`A` finite, `k = card A`), with counting measure; `W` by a real array
`(∀ a, ι a) → ℝ`; measurable sets by finsets; the `L^∞` unit balls by the boxes `[-1,1]^{ι a}`.
Item (ii) (compactness of the quotient space) is NOT formalized.

Main statements.
* `multBil_le_vertexMax` : for `u a ∈ [0,1]^{ι a}` the form `W(u) = ∑_j W_j ∏_a u_a(j_a)` is at
  most its maximum over tuples of indicators `(𝟙_{S_a})_a` (the book's "replace one factor at a
  time by an indicator"; `exists_vertex_ge` is the one-factor-at-a-time induction).
* `abs_multBil_le_cutNorm` : `|W(u)| ≤ ‖W‖_□` on the `[0,1]` boxes.
* `cutNorm_le_infOne` : `‖W‖_□ = |W(u)|` for some `u` in the `[-1,1]` boxes (lower inequality).
* `infOne_le_pow_cutNorm` : `|W(u)| ≤ 2^{card A} ‖W‖_□` on the `[-1,1]` boxes (upper
  inequality, by splitting one factor at a time: each split doubles the constant).
* `hypergraphon_duality` : both inequalities with `opNorm W := sup |W(u)|` over the `[-1,1]`
  boxes, as in the book.
* Witness `Wsh k = (1,-1)^{⊗k}` on `(Fin k → Fin 2)`: `‖Wsh k‖_□ = 1` and `opNorm (Wsh k) = 2^k`,
  so the constant `2^k` is attained for every `k` (finite analogue of the sharpness of `4` for
  `k = 2`).
* Mutants: no constant `c < 2^k` works (`mutant_const_lt_false`); the indicator step fails on
  the `[-1,1]` boxes, i.e. `|W(u)| ≤ ‖W‖_□` is false there (`mutant_pm1_indicator_false`).
-/

namespace LeanReal.Chap01Hypergraphon

open Finset

noncomputable section

variable {A : Type*} [Fintype A] [DecidableEq A]
  {ι : A → Type*} [∀ a, Fintype (ι a)] [∀ a, DecidableEq (ι a)]

/-- The `k`-linear form `W(u) = ∑_j W_j ∏_a u_a(j_a)`, the finite analogue of
`∫ W u^{(1)} ⊗ ⋯ ⊗ u^{(k)}`. -/
def multBil (W : (∀ a, ι a) → ℝ) (u : ∀ a, ι a → ℝ) : ℝ := ∑ j, W j * ∏ a, u a (j a)

/-- `∑_{S_1 × ⋯ × S_k} W`: the sum of `W` over the product set `Fintype.piFinset S`. -/
def cutSet (W : (∀ a, ι a) → ℝ) (S : ∀ a, Finset (ι a)) : ℝ := ∑ j ∈ Fintype.piFinset S, W j

/-- Indicator vector of a finset. -/
def ind {α : Type*} [DecidableEq α] (S : Finset α) (i : α) : ℝ := if i ∈ S then 1 else 0

/-- Maximum of `cutSet` over all tuples `S` (the value of the form at tuples of indicators). -/
def vertexMax (W : (∀ a, ι a) → ℝ) : ℝ :=
  (univ : Finset (∀ a, Finset (ι a))).sup' univ_nonempty (fun S => cutSet W S)

/-- Multilinear cut norm `‖W‖_{□,k} = max_S |∑_{S_1 × ⋯ × S_k} W|` (eq. `eq:hypergraphon_cutnorm`,
finite case). -/
def cutNorm (W : (∀ a, ι a) → ℝ) : ℝ :=
  (univ : Finset (∀ a, Finset (ι a))).sup' univ_nonempty (fun S => |cutSet W S|)

/-- `u ∈ [0,1]^α`. -/
def InBox01 {α : Type*} (u : α → ℝ) : Prop := ∀ i, 0 ≤ u i ∧ u i ≤ 1

/-- `u ∈ [-1,1]^α` (the `L^∞` unit ball). -/
def InBoxPM1 {α : Type*} (u : α → ℝ) : Prop := ∀ i, -1 ≤ u i ∧ u i ≤ 1

/-- The operator norm `‖T_W‖_{L^∞ × ⋯ × L^∞ → ℝ} = sup { |W(u)| : u_a ∈ [-1,1]^{ι a} }`. -/
def opNorm (W : (∀ a, ι a) → ℝ) : ℝ :=
  sSup ((fun u : ∀ a, ι a → ℝ => |multBil W u|) '' {u | ∀ a, InBoxPM1 (u a)})

lemma ind_box {α : Type*} [DecidableEq α] (S : Finset α) : InBox01 (ind S) := by
  intro i; unfold ind; split_ifs <;> norm_num

lemma ind_boxPM {α : Type*} [DecidableEq α] (S : Finset α) : InBoxPM1 (ind S) := by
  intro i; unfold ind; split_ifs <;> norm_num

/-- At a tuple of indicators the form is the sum over the product set. -/
lemma multBil_ind (W : (∀ a, ι a) → ℝ) (S : ∀ a, Finset (ι a)) :
    multBil W (fun a => ind (S a)) = cutSet W S := by
  have h : ∀ j : ∀ a, ι a, (∏ a, ind (S a) (j a)) = if j ∈ Fintype.piFinset S then 1 else 0 := by
    intro j
    unfold ind
    rw [Fintype.prod_boole]
    simp [Fintype.mem_piFinset]
  simp only [multBil, cutSet, h, mul_ite, mul_one, mul_zero]
  rw [Finset.sum_ite_mem, Finset.univ_inter]

/-- Coefficient of the factor `a` once the other factors are frozen at `u`:
`W(u[a ↦ t]) = ∑_i t_i · coef W u a i`. -/
def coef (W : (∀ a, ι a) → ℝ) (u : ∀ a, ι a → ℝ) (a : A) (i : ι a) : ℝ :=
  ∑ j, if j a = i then W j * ∏ b ∈ univ.erase a, u b (j b) else 0

/-- The form is linear in each factor separately ("affine in each factor"). -/
lemma multBil_update (W : (∀ a, ι a) → ℝ) (u : ∀ a, ι a → ℝ) (a : A) (t : ι a → ℝ) :
    multBil W (Function.update u a t) = ∑ i, t i * coef W u a i := by
  have hp : ∀ j : ∀ a, ι a,
      (∏ b, Function.update u a t b (j b)) = t (j a) * ∏ b ∈ univ.erase a, u b (j b) := by
    intro j
    have : (fun b => Function.update u a t b (j b)) =
        Function.update (fun b => u b (j b)) a (t (j a)) := by
      ext b
      by_cases hb : b = a
      · subst hb; simp
      · simp [Function.update_of_ne hb]
    rw [this, Finset.prod_update_of_mem (mem_univ a), Finset.sdiff_singleton_eq_erase]
  simp only [multBil, coef, hp, Finset.mul_sum]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun j _ => ?_
  simp only [mul_ite, mul_zero, Finset.sum_ite_eq, Finset.mem_univ, ite_true]
  ring

/-- One-variable step: a linear form on `[0,1]^α` is at most its value at the indicator of
`{c > 0}`. -/
lemma lin_le_pos {α : Type*} [Fintype α] [DecidableEq α] (c u : α → ℝ) (hu : InBox01 u) :
    ∑ i, u i * c i ≤ ∑ i, ind (univ.filter (fun i => 0 < c i)) i * c i := by
  refine Finset.sum_le_sum fun i _ => ?_
  obtain ⟨h0, h1⟩ := hu i
  unfold ind
  simp only [Finset.mem_filter, Finset.mem_univ, true_and]
  split_ifs with hc
  · nlinarith
  · have hc' := not_lt.mp hc; nlinarith

/-- Replacing the factor `a ∈ [0,1]^{ι a}` by an indicator does not decrease the form. -/
theorem step_update (W : (∀ a, ι a) → ℝ) (u : ∀ a, ι a → ℝ) (a : A) (hu : InBox01 (u a)) :
    ∃ S : Finset (ι a), multBil W u ≤ multBil W (Function.update u a (ind S)) := by
  refine ⟨univ.filter (fun i => 0 < coef W u a i), ?_⟩
  have h1 : multBil W u = multBil W (Function.update u a (u a)) := by
    rw [Function.update_eq_self]
  rw [h1, multBil_update, multBil_update]
  exact lin_le_pos _ _ hu

/-- Doing the indicator step for every factor in `B`: the form at `u` is at most its value at a
tuple that is an indicator on `B` and still in the `[0,1]` boxes. -/
theorem exists_vertex_ge (W : (∀ a, ι a) → ℝ) (B : Finset A) :
    ∀ u : ∀ a, ι a → ℝ, (∀ a, InBox01 (u a)) →
      ∃ u' : ∀ a, ι a → ℝ, (∀ a, InBox01 (u' a)) ∧
        (∀ a ∈ B, ∃ S : Finset (ι a), u' a = ind S) ∧ multBil W u ≤ multBil W u' := by
  induction B using Finset.induction_on with
  | empty => intro u hu; exact ⟨u, hu, by simp, le_rfl⟩
  | @insert a B ha ih =>
    intro u hu
    obtain ⟨u', hu', hB, hle⟩ := ih u hu
    obtain ⟨S, hS⟩ := step_update W u' a (hu' a)
    refine ⟨Function.update u' a (ind S), ?_, ?_, hle.trans hS⟩
    · intro b
      by_cases hb : b = a
      · subst hb; simp only [Function.update_self]; exact ind_box S
      · rw [Function.update_of_ne hb]; exact hu' b
    · intro b hb
      rw [Finset.mem_insert] at hb
      rcases hb with rfl | hb
      · exact ⟨S, by simp⟩
      · have hba : b ≠ a := fun h => ha (h ▸ hb)
        rw [Function.update_of_ne hba]; exact hB b hb

/-- **Vertex lemma.** For `u a ∈ [0,1]^{ι a}`, `W(u) ≤ max_S ∑_{S_1 × ⋯ × S_k} W`. -/
theorem multBil_le_vertexMax (W : (∀ a, ι a) → ℝ) (u : ∀ a, ι a → ℝ)
    (hu : ∀ a, InBox01 (u a)) : multBil W u ≤ vertexMax W := by
  obtain ⟨u', -, hB, hle⟩ := exists_vertex_ge W univ u hu
  choose S hS using fun a => hB a (mem_univ a)
  have : u' = fun a => ind (S a) := funext hS
  rw [this, multBil_ind] at hle
  exact hle.trans (Finset.le_sup' (fun S => cutSet W S) (mem_univ S))

/-- The vertex maximum is attained at a tuple of indicators. -/
theorem vertexMax_attained (W : (∀ a, ι a) → ℝ) :
    ∃ S : ∀ a, Finset (ι a), (∀ a, InBox01 (ind (S a))) ∧
      multBil W (fun a => ind (S a)) = vertexMax W := by
  obtain ⟨S, -, hS⟩ := Finset.exists_mem_eq_sup' (Finset.univ_nonempty
    (α := ∀ a, Finset (ι a))) (fun S => cutSet W S)
  exact ⟨S, fun a => ind_box _, by rw [multBil_ind, vertexMax, hS]⟩

omit [∀ a, Fintype (ι a)] [∀ a, DecidableEq (ι a)] in
lemma cutSet_neg (W : (∀ a, ι a) → ℝ) (S : ∀ a, Finset (ι a)) :
    cutSet (-W) S = - cutSet W S := by
  simp [cutSet, Finset.sum_neg_distrib]

omit [∀ a, DecidableEq (ι a)] in
lemma multBil_neg (W : (∀ a, ι a) → ℝ) (u : ∀ a, ι a → ℝ) :
    multBil (-W) u = - multBil W u := by
  simp [multBil, Finset.sum_neg_distrib]

omit [∀ a, DecidableEq (ι a)] in
lemma vertexMax_le_cutNorm (W : (∀ a, ι a) → ℝ) : vertexMax W ≤ cutNorm W := by
  unfold vertexMax cutNorm
  exact Finset.sup'_mono_fun fun p _ => le_abs_self _

omit [∀ a, DecidableEq (ι a)] in
lemma cutNorm_neg (W : (∀ a, ι a) → ℝ) : cutNorm (-W) = cutNorm W := by
  unfold cutNorm
  simp [cutSet_neg, abs_neg]

/-- `|W(u)| ≤ ‖W‖_□` for `u` in the `[0,1]` boxes (the bound on one orthant term). -/
theorem abs_multBil_le_cutNorm (W : (∀ a, ι a) → ℝ) (u : ∀ a, ι a → ℝ)
    (hu : ∀ a, InBox01 (u a)) : |multBil W u| ≤ cutNorm W := by
  have hpos := (multBil_le_vertexMax W u hu).trans (vertexMax_le_cutNorm W)
  have hneg := (multBil_le_vertexMax (-W) u hu).trans (vertexMax_le_cutNorm (-W))
  rw [cutNorm_neg, multBil_neg] at hneg
  exact abs_le.mpr ⟨by linarith, hpos⟩

/-- Lower inequality `‖W‖_□ ≤ ‖T_W‖`: the cut norm is the value `|W(u)|` at some `u` in the
`[-1,1]` boxes (a tuple of indicators). -/
theorem cutNorm_le_infOne (W : (∀ a, ι a) → ℝ) :
    ∃ u : ∀ a, ι a → ℝ, (∀ a, InBoxPM1 (u a)) ∧ cutNorm W = |multBil W u| := by
  obtain ⟨S, -, hS⟩ := Finset.exists_mem_eq_sup' (Finset.univ_nonempty
    (α := ∀ a, Finset (ι a))) (fun S => |cutSet W S|)
  exact ⟨fun a => ind (S a), fun a => ind_boxPM _, by rw [multBil_ind, cutNorm, hS]⟩

/-- Positive and negative parts of a vector in `[-1,1]` lie in `[0,1]`. -/
lemma box_parts {α : Type*} (x : α → ℝ) (hx : InBoxPM1 x) :
    InBox01 (fun i => max (x i) 0) ∧ InBox01 (fun i => max (-x i) 0) :=
  ⟨fun i => ⟨le_max_right _ _, max_le (hx i).2 zero_le_one⟩,
    fun i => ⟨le_max_right _ _, max_le (by linarith [(hx i).1]) zero_le_one⟩⟩

/-- Splitting the factors in `B` into positive and negative parts, one at a time: if `u a ∈ [-1,1]`
for `a ∈ B` and `u a ∈ [0,1]` otherwise, then `|W(u)| ≤ 2^{#B} ‖W‖_□`. -/
theorem abs_multBil_le_pow (W : (∀ a, ι a) → ℝ) (B : Finset A) :
    ∀ u : ∀ a, ι a → ℝ, (∀ a ∈ B, InBoxPM1 (u a)) → (∀ a ∉ B, InBox01 (u a)) →
      |multBil W u| ≤ 2 ^ B.card * cutNorm W := by
  induction B using Finset.induction_on with
  | empty =>
    intro u _ h01
    simpa using abs_multBil_le_cutNorm W u (fun a => h01 a (by simp))
  | @insert a B ha ih =>
    intro u hpm h01
    set p : ι a → ℝ := fun i => max (u a i) 0 with hp_def
    set m : ι a → ℝ := fun i => max (-u a i) 0 with hm_def
    obtain ⟨hp, hm⟩ := box_parts (u a) (hpm a (mem_insert_self a B))
    have hsplit : multBil W u =
        multBil W (Function.update u a p) - multBil W (Function.update u a m) := by
      rw [multBil_update, multBil_update, ← Finset.sum_sub_distrib]
      conv_lhs => rw [← Function.update_eq_self a u, multBil_update]
      refine Finset.sum_congr rfl fun i _ => ?_
      have h := max_zero_sub_max_neg_zero_eq_self (u a i)
      simp only [hp_def, hm_def]
      linear_combination (-(coef W u a i)) * h
    have h1 := ih (Function.update u a p)
      (fun b hb => by
        rw [Function.update_of_ne (ne_of_mem_of_not_mem hb ha)]
        exact hpm b (mem_insert_of_mem hb))
      (fun b hb => by
        by_cases hba : b = a
        · subst hba; simpa using hp
        · rw [Function.update_of_ne hba]
          exact h01 b (by simp [hba, hb]))
    have h2 := ih (Function.update u a m)
      (fun b hb => by
        rw [Function.update_of_ne (ne_of_mem_of_not_mem hb ha)]
        exact hpm b (mem_insert_of_mem hb))
      (fun b hb => by
        by_cases hba : b = a
        · subst hba; simpa using hm
        · rw [Function.update_of_ne hba]
          exact h01 b (by simp [hba, hb]))
    rw [hsplit, Finset.card_insert_of_notMem ha, pow_succ]
    obtain ⟨h1l, h1r⟩ := abs_le.mp h1
    obtain ⟨h2l, h2r⟩ := abs_le.mp h2
    exact abs_le.mpr ⟨by linarith, by linarith⟩

/-- Upper inequality `‖T_W‖ ≤ 2^k ‖W‖_□`: `|W(u)| ≤ 2^{card A} ‖W‖_□` on the `[-1,1]` boxes. -/
theorem infOne_le_pow_cutNorm (W : (∀ a, ι a) → ℝ) (u : ∀ a, ι a → ℝ)
    (hu : ∀ a, InBoxPM1 (u a)) : |multBil W u| ≤ 2 ^ Fintype.card A * cutNorm W := by
  have := abs_multBil_le_pow W univ u (fun a _ => hu a) (fun a ha => absurd (mem_univ a) ha)
  simpa [Finset.card_univ] using this

lemma opNorm_bddAbove (W : (∀ a, ι a) → ℝ) :
    BddAbove ((fun u : ∀ a, ι a → ℝ => |multBil W u|) '' {u | ∀ a, InBoxPM1 (u a)}) :=
  ⟨2 ^ Fintype.card A * cutNorm W, by
    rintro _ ⟨v, hv, rfl⟩
    exact infOne_le_pow_cutNorm W v hv⟩

/-- `‖W‖_□ ≤ ‖T_W‖`. -/
theorem cutNorm_le_opNorm (W : (∀ a, ι a) → ℝ) : cutNorm W ≤ opNorm W := by
  obtain ⟨u, hu, h⟩ := cutNorm_le_infOne W
  rw [h]
  exact le_csSup (opNorm_bddAbove W) ⟨u, hu, rfl⟩

/-- `‖T_W‖ ≤ 2^k ‖W‖_□`. -/
theorem opNorm_le_pow_cutNorm (W : (∀ a, ι a) → ℝ) :
    opNorm W ≤ 2 ^ Fintype.card A * cutNorm W := by
  refine csSup_le ⟨_, ⟨fun _ _ => 0, fun a i => by norm_num, rfl⟩⟩ ?_
  rintro _ ⟨v, hv, rfl⟩
  exact infOne_le_pow_cutNorm W v hv

/-- **`thm:hypergraphon_compactness`(i), finite `k`-linear case:**
`‖W‖_{□,k} ≤ ‖T_W‖ ≤ 2^k ‖W‖_{□,k}` with `k = card A`. -/
theorem hypergraphon_duality (W : (∀ a, ι a) → ℝ) :
    cutNorm W ≤ opNorm W ∧ opNorm W ≤ 2 ^ Fintype.card A * cutNorm W :=
  ⟨cutNorm_le_opNorm W, opNorm_le_pow_cutNorm W⟩

omit [∀ a, DecidableEq (ι a)] in
/-- The cut norm is nonnegative. -/
theorem cutNorm_nonneg (W : (∀ a, ι a) → ℝ) : 0 ≤ cutNorm W :=
  (abs_nonneg _).trans (Finset.le_sup' (fun S => |cutSet W S|) (mem_univ fun _ => ∅))

#print axioms multBil_le_vertexMax
#print axioms vertexMax_attained
#print axioms abs_multBil_le_cutNorm
#print axioms cutNorm_le_infOne
#print axioms infOne_le_pow_cutNorm
#print axioms hypergraphon_duality

/-! ### Non-vacuity witness: the rank-one sign tensor `(1,-1)^{⊗k}`, where `2^k` is attained -/

/-- `sgn = (1, -1)`. -/
def sgn : Fin 2 → ℝ := ![1, -1]

/-- `Wsh k = sgn^{⊗k}`, an array on `(Fin k → Fin 2)`. -/
def Wsh (k : ℕ) : (Fin k → Fin 2) → ℝ := fun j => ∏ a, sgn (j a)

lemma sgn_zero : sgn 0 = 1 := rfl
lemma sgn_one : sgn 1 = -1 := rfl

/-- On a rank-one array the form factorizes. -/
lemma multBil_Wsh (k : ℕ) (u : Fin k → Fin 2 → ℝ) :
    multBil (Wsh k) u = ∏ a, ∑ i, sgn i * u a i := by
  unfold multBil Wsh
  rw [Fintype.prod_sum]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [Finset.prod_mul_distrib]

lemma sgn_ind_abs_le (S : Finset (Fin 2)) : |∑ i, sgn i * ind S i| ≤ 1 := by
  rw [Fin.sum_univ_two, sgn_zero, sgn_one]
  unfold ind
  split_ifs <;> norm_num

lemma cutNorm_Wsh_le (k : ℕ) : cutNorm (Wsh k) ≤ 1 := by
  unfold cutNorm
  refine Finset.sup'_le _ _ fun S _ => ?_
  rw [← multBil_ind, multBil_Wsh, Finset.abs_prod]
  exact Finset.prod_le_one₀ (fun a _ => abs_nonneg _) (fun a _ => sgn_ind_abs_le (S a))

lemma cutSet_Wsh_zero (k : ℕ) : cutSet (Wsh k) (fun _ => {0}) = 1 := by
  rw [← multBil_ind, multBil_Wsh]
  refine Finset.prod_eq_one fun a _ => ?_
  rw [Fin.sum_univ_two, sgn_zero, sgn_one]
  unfold ind
  norm_num

/-- `‖Wsh k‖_□ = 1`. -/
theorem cutNorm_Wsh (k : ℕ) : cutNorm (Wsh k) = 1 := by
  refine le_antisymm (cutNorm_Wsh_le k) ?_
  have := Finset.le_sup' (fun S : Fin k → Finset (Fin 2) => |cutSet (Wsh k) S|)
    (mem_univ fun _ => ({0} : Finset (Fin 2)))
  rw [cutSet_Wsh_zero, abs_one] at this
  exact this

lemma sgn_boxPM : InBoxPM1 sgn := by
  intro i; fin_cases i <;> norm_num [sgn]

/-- `Wsh k (sgn, …, sgn) = 2^k`. -/
theorem multBil_Wsh_sgn (k : ℕ) : multBil (Wsh k) (fun _ => sgn) = 2 ^ k := by
  rw [multBil_Wsh]
  simp only [Fin.sum_univ_two, sgn_zero, sgn_one]
  norm_num [Finset.prod_const]

/-- Witness: `u_a = (1,-1) ∈ [-1,1]²` for every `a` gives `W(u) = 2^k`, while `‖Wsh k‖_□ = 1`:
the hypotheses of `infOne_le_pow_cutNorm` are satisfiable and the bound is attained. -/
theorem sharp_witness (k : ℕ) :
    (∀ a : Fin k, InBoxPM1 ((fun _ => sgn) a)) ∧ multBil (Wsh k) (fun _ => sgn) = 2 ^ k ∧
      cutNorm (Wsh k) = 1 :=
  ⟨fun _ => sgn_boxPM, multBil_Wsh_sgn k, cutNorm_Wsh k⟩

/-- `‖T_{Wsh k}‖ = 2^k = 2^k ‖Wsh k‖_□`: the upper inequality is an equality. -/
theorem opNorm_Wsh (k : ℕ) : opNorm (Wsh k) = 2 ^ k := by
  refine le_antisymm ?_ ?_
  · have := opNorm_le_pow_cutNorm (Wsh k)
    rwa [cutNorm_Wsh, mul_one, Fintype.card_fin] at this
  · have h : |multBil (Wsh k) (fun _ => sgn)| ≤ opNorm (Wsh k) :=
      le_csSup (opNorm_bddAbove (Wsh k)) ⟨fun _ => sgn, fun _ => sgn_boxPM, rfl⟩
    rwa [multBil_Wsh_sgn, abs_of_pos (by positivity)] at h

/-! ### Mutants proved false -/

/-- Mutant: the constant `2^k` can be replaced by some `c < 2^k`. Refuted by `Wsh k` and
`u = (sgn, …, sgn)`: `2^k ≤ c · 1 < 2^k`. -/
theorem mutant_const_lt_false (k : ℕ) (c : ℝ) (hc : c < 2 ^ k) :
    ¬ ∀ (W : (Fin k → Fin 2) → ℝ) (u : Fin k → Fin 2 → ℝ), (∀ a, InBoxPM1 (u a)) →
      |multBil W u| ≤ c * cutNorm W := by
  intro h
  obtain ⟨hb, hval, hcn⟩ := sharp_witness k
  have := h (Wsh k) _ hb
  rw [hval, hcn, mul_one, abs_of_pos (by positivity)] at this
  linarith

/-- Mutant: the indicator step holds on the `[-1,1]` boxes, i.e. `|W(u)| ≤ ‖W‖_□` there (this
is the gap a proof has if it applies the vertex argument to `u_±` without the `[0,1]`
restriction, or skips the splitting). Refuted for every `k ≥ 1` by `Wsh k`: `2^k > 1`. -/
theorem mutant_pm1_indicator_false (k : ℕ) (hk : 1 ≤ k) :
    ¬ ∀ (W : (Fin k → Fin 2) → ℝ) (u : Fin k → Fin 2 → ℝ), (∀ a, InBoxPM1 (u a)) →
      |multBil W u| ≤ cutNorm W := by
  intro h
  obtain ⟨hb, hval, hcn⟩ := sharp_witness k
  have := h (Wsh k) _ hb
  rw [hval, hcn, abs_of_pos (by positivity)] at this
  have h2 : (2 : ℝ) ^ 1 ≤ 2 ^ k := pow_le_pow_right₀ (by norm_num) hk
  linarith

#print axioms sharp_witness
#print axioms opNorm_Wsh
#print axioms mutant_const_lt_false
#print axioms mutant_pm1_indicator_false

end

end LeanReal.Chap01Hypergraphon
