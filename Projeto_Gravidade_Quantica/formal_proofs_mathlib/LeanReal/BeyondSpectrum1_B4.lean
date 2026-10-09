import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Fintype.Powerset
import Mathlib.Tactic

/-!
# *Beyond the Spectrum* I (Zenodo concept DOI 10.5281/zenodo.22644743), item B4

Source: `Manuscritos_Avulsos/paper_functional_realizations/paper_functional_realizations.tex`,
Definition "The Cut Norm" (eq. `eq:cut_norm_def`) and Theorem `thm:grothendieck_cutnorm`
("Equivalence with the `L^∞ → L^1` Operator Norm").

Paper:
> `‖W‖_□ := sup_{S,T ⊆ [0,1]} |∫_{S×T} W|`. The cut norm is equivalent to the operator norm of
> `T_W : L^∞ → L^1`: `‖W‖_□ ≤ ‖T_W‖_{∞→1} ≤ 4 ‖W‖_□`, where
> `‖T_W‖_{∞→1} := sup_{‖u‖_∞ ≤ 1, ‖v‖_∞ ≤ 1} |∬ W u v|`. [Proof: for `g, h : [0,1] → [0,1]`,
> `|∫ W g h| ≤ ‖W‖_□` since the extremum of a bilinear form over the box is attained at
> indicators; split `u = u₊ - u₋`, `v = v₊ - v₋`.] The constant `4` cannot be improved.

REDUCTION (declared). Only the FINITE-MATRIX case is formalized: `[0,1]` is replaced by a finite
index set with counting measure, `W` by a real matrix indexed by `ι × κ`, measurable sets by
finsets, `L^∞` unit balls by `[-1,1]^ι`, `[-1,1]^κ`. (For matrices this is Lemma 3.1 of
Alon–Naor, which the paper cites.) The measure-theoretic statement on `[0,1]²` is NOT formalized.

* `bil_le_vertexMax` : on `[0,1]^ι × [0,1]^κ` the bilinear form `uᵀ W v` is bounded by its
  maximum over vertices `(𝟙_S, 𝟙_T)`, which is attained (`vertexMax_attained`). This is the step
  "the extremum over the box is attained at indicators".
* `abs_bil_le_cutNorm` : `|uᵀ W v| ≤ ‖W‖_□` on `[0,1]` boxes.
* `cutNorm_le_infOne` / `infOne_le_four_cutNorm` : the two inequalities of the theorem, the
  first as "`‖W‖_□` is attained by some `u, v ∈ [-1,1]`".
* Witness: `W = !![1,-1;-1,1]` has `‖W‖_□ ≤ 1` and `u = v = (1,-1)` gives `uᵀWv = 4`, so the
  factor `4` is attained (finite analogue of the paper's sharpness example).
-/

namespace LeanReal.BeyondSpectrum1B4

open Finset

variable {ι κ : Type*} [Fintype ι] [Fintype κ] [DecidableEq ι] [DecidableEq κ]

/-- Bilinear form `uᵀ W v = ∑_{i,j} W_{ij} u_i v_j`. -/
def bil (W : Matrix ι κ ℝ) (u : ι → ℝ) (v : κ → ℝ) : ℝ := ∑ i, ∑ j, W i j * u i * v j

/-- `∑_{S × T} W`. -/
def cutSet (W : Matrix ι κ ℝ) (S : Finset ι) (T : Finset κ) : ℝ := ∑ i ∈ S, ∑ j ∈ T, W i j

/-- Indicator vector of a finset. -/
def ind {α : Type*} [DecidableEq α] (S : Finset α) (i : α) : ℝ := if i ∈ S then 1 else 0

/-- Maximum of `cutSet` over all pairs `(S, T)` (= max of the bilinear form at vertices). -/
def vertexMax (W : Matrix ι κ ℝ) : ℝ :=
  (Finset.univ : Finset (Finset ι × Finset κ)).sup' Finset.univ_nonempty
    (fun p => cutSet W p.1 p.2)

/-- Cut norm `‖W‖_□ = max_{S,T} |∑_{S×T} W|`. -/
def cutNorm (W : Matrix ι κ ℝ) : ℝ :=
  (Finset.univ : Finset (Finset ι × Finset κ)).sup' Finset.univ_nonempty
    (fun p => |cutSet W p.1 p.2|)

/-- Unit box predicates. -/
def InBox01 {α : Type*} (u : α → ℝ) : Prop := ∀ i, 0 ≤ u i ∧ u i ≤ 1
def InBoxPM1 {α : Type*} (u : α → ℝ) : Prop := ∀ i, -1 ≤ u i ∧ u i ≤ 1

lemma bil_ind (W : Matrix ι κ ℝ) (S : Finset ι) (T : Finset κ) :
    bil W (ind S) (ind T) = cutSet W S T := by
  have hS : ∀ g : ι → ℝ, ∑ i ∈ S, g i = ∑ i, if i ∈ S then g i else 0 := fun g => by
    rw [Finset.sum_ite_mem, Finset.univ_inter]
  have hT : ∀ g : κ → ℝ, ∑ j ∈ T, g j = ∑ j, if j ∈ T then g j else 0 := fun g => by
    rw [Finset.sum_ite_mem, Finset.univ_inter]
  simp only [bil, cutSet, ind, hS, hT]
  refine Finset.sum_congr rfl fun i _ => ?_
  by_cases hi : i ∈ S <;> simp [hi]

/-- One-variable step: a linear form on `[0,1]^α` is at most its value at the indicator of
`{c > 0}`. -/
lemma lin_le_pos {α : Type*} [Fintype α] (c u : α → ℝ) (hu : InBox01 u) :
    ∑ i, u i * c i ≤ ∑ i ∈ Finset.univ.filter (fun i => 0 < c i), c i := by
  rw [Finset.sum_filter]
  refine Finset.sum_le_sum fun i _ => ?_
  obtain ⟨h0, h1⟩ := hu i
  split_ifs with hc
  · nlinarith
  · have hc' := not_lt.mp hc; nlinarith

omit [DecidableEq ι] [DecidableEq κ] in
/-- **Vertex lemma.** For `u ∈ [0,1]^ι`, `v ∈ [0,1]^κ`, `uᵀ W v ≤ max_{S,T} ∑_{S×T} W`. -/
theorem bil_le_vertexMax (W : Matrix ι κ ℝ) (u : ι → ℝ) (v : κ → ℝ)
    (hu : InBox01 u) (hv : InBox01 v) : bil W u v ≤ vertexMax W := by
  set c : ι → ℝ := fun i => ∑ j, W i j * v j
  set S := Finset.univ.filter (fun i => 0 < c i)
  set d : κ → ℝ := fun j => ∑ i ∈ S, W i j
  set T := Finset.univ.filter (fun j => 0 < d j)
  have h1 : bil W u v = ∑ i, u i * c i := by
    simp only [bil, c, Finset.mul_sum]
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
    ring
  have h2 : ∑ i ∈ S, c i = ∑ j, v j * d j := by
    simp only [c, d, Finset.mul_sum]
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun j _ => Finset.sum_congr rfl fun i _ => ?_
    ring
  have h3 : ∑ j ∈ T, d j = cutSet W S T := by
    simp only [d, cutSet]
    rw [Finset.sum_comm]
  calc bil W u v = ∑ i, u i * c i := h1
    _ ≤ ∑ i ∈ S, c i := lin_le_pos c u hu
    _ = ∑ j, v j * d j := h2
    _ ≤ ∑ j ∈ T, d j := lin_le_pos d v hv
    _ = cutSet W S T := h3
    _ ≤ vertexMax W := Finset.le_sup' (fun p : Finset ι × Finset κ => cutSet W p.1 p.2)
          (Finset.mem_univ (S, T))

/-- The vertex maximum is attained at a vertex `(𝟙_S, 𝟙_T)` of the box. -/
theorem vertexMax_attained (W : Matrix ι κ ℝ) :
    ∃ S : Finset ι, ∃ T : Finset κ, InBox01 (ind S) ∧ InBox01 (ind T) ∧
      bil W (ind S) (ind T) = vertexMax W := by
  obtain ⟨p, -, hp⟩ := Finset.exists_mem_eq_sup' (Finset.univ_nonempty
    (α := Finset ι × Finset κ)) (fun p => cutSet W p.1 p.2)
  refine ⟨p.1, p.2, ?_, ?_, ?_⟩
  · intro i; unfold ind; split_ifs <;> norm_num
  · intro i; unfold ind; split_ifs <;> norm_num
  · rw [bil_ind, vertexMax, hp]

omit [Fintype ι] [Fintype κ] [DecidableEq ι] [DecidableEq κ] in
lemma cutSet_neg (W : Matrix ι κ ℝ) (S : Finset ι) (T : Finset κ) :
    cutSet (-W) S T = - cutSet W S T := by
  simp [cutSet, Finset.sum_neg_distrib]

omit [DecidableEq ι] [DecidableEq κ] in
lemma vertexMax_le_cutNorm (W : Matrix ι κ ℝ) : vertexMax W ≤ cutNorm W := by
  unfold vertexMax cutNorm
  exact Finset.sup'_mono_fun fun p _ => le_abs_self _

omit [DecidableEq ι] [DecidableEq κ] in
lemma cutNorm_neg (W : Matrix ι κ ℝ) : cutNorm (-W) = cutNorm W := by
  unfold cutNorm
  simp [cutSet_neg, abs_neg]

omit [DecidableEq ι] [DecidableEq κ] in
/-- `|uᵀ W v| ≤ ‖W‖_□` for `u, v` in the `[0,1]` boxes. -/
theorem abs_bil_le_cutNorm (W : Matrix ι κ ℝ) (u : ι → ℝ) (v : κ → ℝ)
    (hu : InBox01 u) (hv : InBox01 v) : |bil W u v| ≤ cutNorm W := by
  have hpos := (bil_le_vertexMax W u v hu hv).trans (vertexMax_le_cutNorm W)
  have hneg := (bil_le_vertexMax (-W) u v hu hv).trans (vertexMax_le_cutNorm (-W))
  rw [cutNorm_neg] at hneg
  have : bil (-W) u v = - bil W u v := by
    simp [bil, Finset.sum_neg_distrib]
  rw [this] at hneg
  exact abs_le.mpr ⟨by linarith, hpos⟩

/-- Lower inequality `‖W‖_□ ≤ ‖T_W‖_{∞→1}`: the cut norm is the value `|uᵀ W v|` at some
`u, v ∈ [-1,1]` (indicators). -/
theorem cutNorm_le_infOne (W : Matrix ι κ ℝ) :
    ∃ u : ι → ℝ, ∃ v : κ → ℝ, InBoxPM1 u ∧ InBoxPM1 v ∧ cutNorm W = |bil W u v| := by
  obtain ⟨p, -, hp⟩ := Finset.exists_mem_eq_sup' (Finset.univ_nonempty
    (α := Finset ι × Finset κ)) (fun p => |cutSet W p.1 p.2|)
  refine ⟨ind p.1, ind p.2, ?_, ?_, ?_⟩
  · intro i; unfold ind; split_ifs <;> norm_num
  · intro i; unfold ind; split_ifs <;> norm_num
  · rw [bil_ind, cutNorm, hp]

/-- Positive and negative parts of a vector in `[-1,1]` lie in `[0,1]`. -/
lemma box_parts {α : Type*} (x : α → ℝ) (hx : InBoxPM1 x) :
    InBox01 (fun i => max (x i) 0) ∧ InBox01 (fun i => max (-x i) 0) :=
  ⟨fun i => ⟨le_max_right _ _, max_le (hx i).2 zero_le_one⟩,
    fun i => ⟨le_max_right _ _, max_le (by linarith [(hx i).1]) zero_le_one⟩⟩

omit [DecidableEq ι] [DecidableEq κ] in
/-- Upper inequality `‖T_W‖_{∞→1} ≤ 4 ‖W‖_□`. -/
theorem infOne_le_four_cutNorm (W : Matrix ι κ ℝ) (u : ι → ℝ) (v : κ → ℝ)
    (hu : InBoxPM1 u) (hv : InBoxPM1 v) : |bil W u v| ≤ 4 * cutNorm W := by
  set up : ι → ℝ := fun i => max (u i) 0
  set um : ι → ℝ := fun i => max (-u i) 0
  set vp : κ → ℝ := fun j => max (v j) 0
  set vm : κ → ℝ := fun j => max (-v j) 0
  obtain ⟨hup, hum⟩ := box_parts u hu
  obtain ⟨hvp, hvm⟩ := box_parts v hv
  have split : bil W u v = bil W up vp - bil W up vm - bil W um vp + bil W um vm := by
    have hu' : ∀ i, u i = up i - um i := fun i => (max_zero_sub_max_neg_zero_eq_self (u i)).symm
    have hv' : ∀ j, v j = vp j - vm j := fun j => (max_zero_sub_max_neg_zero_eq_self (v j)).symm
    simp only [bil, ← Finset.sum_sub_distrib, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
    rw [hu' i, hv' j]
    ring
  have a1 := abs_le.mp (abs_bil_le_cutNorm W up vp hup hvp)
  have a2 := abs_le.mp (abs_bil_le_cutNorm W up vm hup hvm)
  have a3 := abs_le.mp (abs_bil_le_cutNorm W um vp hum hvp)
  have a4 := abs_le.mp (abs_bil_le_cutNorm W um vm hum hvm)
  rw [split, abs_le]
  constructor <;> linarith [a1.1, a1.2, a2.1, a2.2, a3.1, a3.2, a4.1, a4.2]

#print axioms bil_le_vertexMax
#print axioms vertexMax_attained
#print axioms abs_bil_le_cutNorm
#print axioms cutNorm_le_infOne
#print axioms infOne_le_four_cutNorm

/-! ### Non-vacuity witness and sharpness of `4` -/

/-- `W = !![1,-1;-1,1]`. -/
def Wsh : Matrix (Fin 2) (Fin 2) ℝ := !![1, -1; -1, 1]

lemma cutNorm_Wsh_le : cutNorm Wsh ≤ 1 := by
  unfold cutNorm
  refine Finset.sup'_le _ _ fun p _ => ?_
  have hS : ∀ f : Fin 2 → ℝ, ∑ i ∈ p.1, f i =
      ∑ i, (if i ∈ p.1 then f i else 0) := fun f => by rw [Finset.sum_ite_mem, Finset.univ_inter]
  have hT : ∀ f : Fin 2 → ℝ, ∑ j ∈ p.2, f j =
      ∑ j, (if j ∈ p.2 then f j else 0) := fun f => by rw [Finset.sum_ite_mem, Finset.univ_inter]
  simp only [cutSet]
  rw [hS]
  simp only [hT, Fin.sum_univ_two, Wsh]
  by_cases a : (0 : Fin 2) ∈ p.1 <;> by_cases b : (1 : Fin 2) ∈ p.1 <;>
    by_cases c : (0 : Fin 2) ∈ p.2 <;> by_cases d : (1 : Fin 2) ∈ p.2 <;>
    simp [a, b, c, d]

/-- Witness: `u = v = (1, -1) ∈ [-1,1]²` gives `uᵀ W v = 4`, while `‖W‖_□ ≤ 1`: the hypotheses
of `infOne_le_four_cutNorm` are satisfiable and the bound is attained. -/
theorem sharp_witness :
    InBoxPM1 ![(1 : ℝ), -1] ∧ bil Wsh ![1, -1] ![1, -1] = 4 ∧ cutNorm Wsh ≤ 1 := by
  refine ⟨?_, ?_, cutNorm_Wsh_le⟩
  · intro i; fin_cases i <;> norm_num
  · simp [bil, Wsh, Fin.sum_univ_two]; norm_num

/-! ### Mutant proved false
Mutant: the constant `4` can be replaced by `3`. Refuted by `Wsh`, `u = v = (1,-1)`:
`4 ≤ 3 · ‖W‖_□ ≤ 3` is false. -/
theorem mutant_three_false :
    ¬ ∀ (W : Matrix (Fin 2) (Fin 2) ℝ) (u v : Fin 2 → ℝ), InBoxPM1 u → InBoxPM1 v →
      |bil W u v| ≤ 3 * cutNorm W := by
  intro h
  obtain ⟨hb, hval, hc⟩ := sharp_witness
  have := h Wsh _ _ hb hb
  rw [hval] at this
  norm_num at this
  linarith

#print axioms sharp_witness
#print axioms mutant_three_false

end LeanReal.BeyondSpectrum1B4
