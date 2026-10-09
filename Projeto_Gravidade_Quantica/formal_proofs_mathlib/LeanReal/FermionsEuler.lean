import Mathlib.Data.Finset.Powerset
import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Data.Nat.Choose.Sum
import Mathlib.Data.Int.Interval

/-!
# Fermion-mass paper (Zenodo concept DOI 10.5281/zenodo.22373916), item F3

Source: `Manuscritos_Avulsos/paper_standard_model_masses/paper_fermion_mass_hierarchy.tex`,
Sec. "Vacuum Energy on the 4-Simplex", eq. `eq:euler`:
> The 4-simplex has `f_k = C(5,k+1)` faces of dimension `k`, namely `f_0,…,f_4 = 5,10,10,5,1`.
> `χ(Δ₄) = ∑_{k=0}^{4} (−1)^k C(5,k+1) = 1`,  `χ̃(Δ₄) = ∑_{k=−1}^{4} (−1)^k C(5,k+1) = 0`,
> `∑_{k=0}^{4} (−1)^k C(4,k) = (1−1)^4 = 0`,
> where `χ̃` is the reduced Euler characteristic, which counts the empty face `f_{−1} = 1`.

Formal version.
* `faceCount k` is DEFINED as the number of `(k+1)`-element subsets of the vertex set `Fin 5`
  (the `k`-faces of the abstract simplex), and `faceCount_eq` proves `faceCount k = C(5,k+1)`;
  `faceCount_values` gives `5,10,10,5,1`.
* `euler_char`, `reduced_euler_char`, `alt_choose_four`: the three identities over `ℤ`. The
  reduced sum runs over `k ∈ Icc (−1) 4 ⊂ ℤ`; the sign `(−1)^k` for `k = −1` is written as
  `(−1)^(k+1) · (−1)` (equal to `(−1)^k` for every integer `k`), and `C(5,k+1)` uses
  `(k+1).toNat`, which is exact on this range.
* `euler_char_simplex`: the general statement `∑_{k=0}^{n} (−1)^k C(n+1,k+1) = 1` for every `n`.
* NOT covered (and the paper says these identities carry no physics): the vacuum-energy reading,
  geometric realisation, homology of `Δ₄`, Remark `rem:cc_counting`.
-/

namespace LeanReal.FermionsEuler

open Finset

/-- Number of `k`-faces of the 4-simplex: `(k+1)`-subsets of its 5 vertices. -/
def faceCount (k : ℕ) : ℕ := ((univ : Finset (Fin 5)).powersetCard (k + 1)).card

theorem faceCount_eq (k : ℕ) : faceCount k = Nat.choose 5 (k + 1) := by
  simp [faceCount, card_powersetCard]

theorem faceCount_values :
    (faceCount 0, faceCount 1, faceCount 2, faceCount 3, faceCount 4) = (5, 10, 10, 5, 1) := by
  simp only [faceCount_eq]; decide

/-- `χ(Δ₄) = 1`. -/
theorem euler_char : ∑ k ∈ range 5, (-1 : ℤ) ^ k * (faceCount k : ℤ) = 1 := by
  simp only [faceCount_eq]; decide

/-- `χ̃(Δ₄) = 0`, summed over `k = −1,…,4`. -/
theorem reduced_euler_char :
    ∑ k ∈ Icc (-1 : ℤ) 4, (-1 : ℤ) ^ (k + 1).toNat * (-1) * (Nat.choose 5 (k + 1).toNat : ℤ) = 0 := by
  decide

/-- `∑_{k=0}^{4} (−1)^k C(4,k) = 0`. -/
theorem alt_choose_four : ∑ k ∈ range 5, (-1 : ℤ) ^ k * (Nat.choose 4 k : ℤ) = 0 := by
  decide

/-- General form: `χ(Δ_n) = 1` for every `n`. -/
theorem euler_char_simplex (n : ℕ) :
    ∑ k ∈ range (n + 1), (-1 : ℤ) ^ k * (Nat.choose (n + 1) (k + 1) : ℤ) = 1 := by
  have h := Int.alternating_sum_range_choose_of_ne (Nat.succ_ne_zero n)
  rw [sum_range_succ'] at h
  simp only [pow_zero, Nat.choose_zero_right, Nat.cast_one, mul_one, pow_succ] at h
  have : ∑ k ∈ range (n + 1), (-1 : ℤ) ^ k * (Nat.choose (n + 1) (k + 1) : ℤ)
      = -∑ k ∈ range (n + 1), (-1 : ℤ) ^ k * -1 * (Nat.choose (n + 1) (k + 1) : ℤ) := by
    rw [← sum_neg_distrib]; refine sum_congr rfl fun k _ => by ring
  linarith

/-! ## Non-vacuity: the face counts are the stated numbers, and the general form at `n = 4`
is `euler_char`. -/

example : faceCount 1 = 10 := by rw [faceCount_eq]; rfl

example : ∑ k ∈ range 5, (-1 : ℤ) ^ k * (Nat.choose 5 (k + 1) : ℤ) = 1 := euler_char_simplex 4

/-! ## Mutant: forget the empty face but keep the value `0` of the reduced characteristic. -/

theorem euler_mutant_false : ¬ (∑ k ∈ range 5, (-1 : ℤ) ^ k * (faceCount k : ℤ) = 0) := by
  rw [euler_char]; decide

end LeanReal.FermionsEuler

#print axioms LeanReal.FermionsEuler.faceCount_eq
#print axioms LeanReal.FermionsEuler.faceCount_values
#print axioms LeanReal.FermionsEuler.euler_char
#print axioms LeanReal.FermionsEuler.reduced_euler_char
#print axioms LeanReal.FermionsEuler.alt_choose_four
#print axioms LeanReal.FermionsEuler.euler_char_simplex
#print axioms LeanReal.FermionsEuler.euler_mutant_false
