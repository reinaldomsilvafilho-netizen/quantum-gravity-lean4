import LeanReal.Chap01Hypergraphon

/-!
# L2 review, final round: complement to `Chap01Hypergraphon`

Book ch. 1, `thm:hypergraphon_compactness`(i) is stated for hypergraphons `W` with values in
`[0,1]`. For a nonnegative kernel the multilinear operator norm equals the cut norm (constant `1`),
so the constant `2^k` of the theorem, and its sharpness (`Chap01Hypergraphon.opNorm_Wsh`), only
matter for signed kernels such as the differences `U - W^ψ` that enter the cut distance.

* `opNorm_eq_cutNorm_of_nonneg`: `W ≥ 0` gives `opNorm W = cutNorm W` (finite `k`-linear case).
* `mutant_nonneg_dropped_false`: without `W ≥ 0` the equality fails (`Wsh 1`: `2 ≠ 1`).
-/

namespace LeanReal.L2_LIVRO_FINAL_Extra

open Finset LeanReal.Chap01Hypergraphon

noncomputable section

variable {A : Type*} [Fintype A] [DecidableEq A]
  {ι : A → Type*} [∀ a, Fintype (ι a)] [∀ a, DecidableEq (ι a)]

omit [∀ a, DecidableEq (ι a)] in
/-- For a nonnegative kernel, `|W(u)| ≤ ∑_j W_j` on the `[-1,1]` boxes. -/
theorem abs_multBil_le_total_of_nonneg (W : (∀ a, ι a) → ℝ) (hW : ∀ j, 0 ≤ W j)
    (u : ∀ a, ι a → ℝ) (hu : ∀ a, InBoxPM1 (u a)) :
    |multBil W u| ≤ cutSet W (fun _ => univ) := by
  unfold multBil cutSet
  rw [Fintype.piFinset_univ]
  refine (Finset.abs_sum_le_sum_abs _ _).trans (Finset.sum_le_sum fun j _ => ?_)
  rw [abs_mul, abs_of_nonneg (hW j), Finset.abs_prod]
  have hp : ∏ a, |u a (j a)| ≤ 1 :=
    Finset.prod_le_one₀ (fun a _ => abs_nonneg _) (fun a _ => abs_le.mpr (hu a (j a)))
  exact mul_le_of_le_one_right (hW j) hp

/-- Book class `W ≥ 0`: the operator norm equals the cut norm (constant `1`, not `2^k`). -/
theorem opNorm_eq_cutNorm_of_nonneg (W : (∀ a, ι a) → ℝ) (hW : ∀ j, 0 ≤ W j) :
    opNorm W = cutNorm W := by
  refine le_antisymm ?_ (cutNorm_le_opNorm W)
  refine csSup_le ⟨_, ⟨fun _ _ => 0, fun a i => by norm_num, rfl⟩⟩ ?_
  rintro _ ⟨v, hv, rfl⟩
  refine (abs_multBil_le_total_of_nonneg W hW v hv).trans ?_
  exact (le_abs_self _).trans
    (Finset.le_sup' (fun S => |cutSet W S|) (mem_univ fun _ => univ))

/-- Mutant: dropping `W ≥ 0`, the equality fails for the signed kernel `Wsh 1`. -/
theorem mutant_nonneg_dropped_false :
    ¬ ∀ W : (Fin 1 → Fin 2) → ℝ, opNorm W = cutNorm W := by
  intro h
  have h1 := h (Wsh 1)
  rw [opNorm_Wsh, cutNorm_Wsh] at h1
  norm_num at h1

/-- Non-vacuity: `Wsh 1` really is signed, so the mutant does not contradict the theorem. -/
theorem Wsh_one_not_nonneg : ¬ ∀ j, 0 ≤ Wsh 1 j := by
  intro h
  have := h (fun _ => 1)
  simp [Wsh, sgn] at this
  linarith

#print axioms opNorm_eq_cutNorm_of_nonneg
#print axioms mutant_nonneg_dropped_false
#print axioms Wsh_one_not_nonneg

end

end LeanReal.L2_LIVRO_FINAL_Extra
