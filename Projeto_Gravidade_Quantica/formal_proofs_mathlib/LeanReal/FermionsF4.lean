import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-!
# Fermion-mass paper (Zenodo concept DOI 10.5281/zenodo.22373916), item F4

Source: `Manuscritos_Avulsos/paper_standard_model_masses/paper_fermion_mass_hierarchy.tex`,
Remark `rem:cc_counting`:
> Weighting the faces by their volumes, `Vol(Δ_k) = √(k+1)/(k! 2^{k/2})` for unit edge length,
> gives `∑_{k=0}^{4} (−1)^k f_k Vol(Δ_k) = −1.236 ≠ 0`.

Here `f_k = C(5, k+1)` are the face numbers of the 4-simplex (eq. `eq:euler`; see also
`LeanReal.FermionsEuler.faceCount_eq`).

Formal version.
* `vol k := √(k+1) / (k! · (√2)^k)`, with `(√2)^k = 2^{k/2}` proved in `sqrt_two_pow_eq_rpow`.
* `vol_values`: `Vol(Δ_0), …, Vol(Δ_4) = 1, 1, √3/4, √2/12, √5/96` (the unit segment, the unit
  equilateral triangle and the regular tetrahedron of edge `1` have these volumes).
* `altVolSum_eq`: the sum equals `−5 + (5/2)√3 − (5/12)√2 + √5/96`.
* `altVolSum_bounds`: `−1.2359 < ∑ < −1.2358`, so the sum rounds to `−1.236` and is `≠ 0`
  (`altVolSum_ne_zero`). The interval bounds for `√2, √3, √5` are proved from squares.
* NOT covered (and the paper says these numbers carry no physics by themselves): any reading of
  the sum as a vacuum energy, and the length scale needed to add volumes of different dimensions.
* Mutant: with `2^k` in place of `2^{k/2}` the sum is `> −1`, so it does not lie in the window
  (`mutant_vol_pow_false`).
-/

namespace LeanReal.FermionsF4

open Finset

noncomputable section

/-- `Vol(Δ_k) = √(k+1) / (k! · 2^{k/2})` for a regular `k`-simplex of unit edge, with
`2^{k/2}` written as `(√2)^k`. -/
def vol (k : ℕ) : ℝ := Real.sqrt (k + 1) / (k.factorial * Real.sqrt 2 ^ k)

/-- `(√2)^k = 2^{k/2}` (real power), so `vol` is the paper's formula. -/
lemma sqrt_two_pow_eq_rpow (k : ℕ) : Real.sqrt 2 ^ k = (2 : ℝ) ^ ((k : ℝ) / 2) := by
  rw [Real.sqrt_eq_rpow, ← Real.rpow_natCast, ← Real.rpow_mul (by norm_num)]
  congr 1; ring

/-- Face numbers of `Δ₄`: `f_k = C(5, k+1)`. -/
def f (k : ℕ) : ℕ := Nat.choose 5 (k + 1)

lemma f_values : f 0 = 5 ∧ f 1 = 10 ∧ f 2 = 10 ∧ f 3 = 5 ∧ f 4 = 1 := by decide

/-- `∑_{k=0}^{4} (−1)^k f_k Vol(Δ_k)`. -/
def altVolSum : ℝ := ∑ k ∈ range 5, (-1 : ℝ) ^ k * (f k : ℝ) * vol k

lemma sqrt_two_pos : (0 : ℝ) < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)

lemma sqrt_two_sq : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)

lemma sqrt_four : Real.sqrt 4 = 2 := by
  rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]

lemma vol_zero : vol 0 = 1 := by simp [vol]

lemma vol_one : vol 1 = 1 := by
  rw [vol]; push_cast
  rw [show (1 : ℝ) + 1 = 2 by norm_num]
  simp [sqrt_two_pos.ne']

lemma vol_two : vol 2 = Real.sqrt 3 / 4 := by
  rw [vol]; push_cast
  rw [show (2 : ℝ) + 1 = 3 by norm_num, sqrt_two_sq]
  norm_num

lemma sqrt_two_pow_four : Real.sqrt 2 ^ 4 = 4 := by
  rw [show (4 : ℕ) = 2 * 2 from rfl, pow_mul, sqrt_two_sq]; norm_num

lemma vol_three : vol 3 = Real.sqrt 2 / 12 := by
  rw [vol]; push_cast
  rw [show (3 : ℝ) + 1 = 4 by norm_num, sqrt_four, pow_succ, sqrt_two_sq,
    div_eq_div_iff (by positivity) (by norm_num)]
  norm_num [Nat.factorial]
  nlinarith [sqrt_two_sq]

lemma vol_four : vol 4 = Real.sqrt 5 / 96 := by
  rw [vol]; push_cast
  rw [show (4 : ℝ) + 1 = 5 by norm_num, sqrt_two_pow_four]
  norm_num [Nat.factorial]

/-- `Vol(Δ_0), …, Vol(Δ_4) = 1, 1, √3/4, √2/12, √5/96`. -/
theorem vol_values :
    vol 0 = 1 ∧ vol 1 = 1 ∧ vol 2 = Real.sqrt 3 / 4 ∧ vol 3 = Real.sqrt 2 / 12 ∧
      vol 4 = Real.sqrt 5 / 96 :=
  ⟨vol_zero, vol_one, vol_two, vol_three, vol_four⟩

/-- Closed form: `∑ = −5 + (5/2)√3 − (5/12)√2 + √5/96`. -/
theorem altVolSum_eq :
    altVolSum = -5 + 5 / 2 * Real.sqrt 3 - 5 / 12 * Real.sqrt 2 + Real.sqrt 5 / 96 := by
  obtain ⟨h0, h1, h2, h3, h4⟩ := f_values
  simp only [altVolSum, Finset.sum_range_succ, Finset.sum_range_zero, h0, h1, h2, h3, h4,
    vol_zero, vol_one, vol_two, vol_three, vol_four]
  push_cast
  ring

lemma sqrt_two_bounds : 1.41421 < Real.sqrt 2 ∧ Real.sqrt 2 < 1.41422 :=
  ⟨by rw [Real.lt_sqrt (by norm_num)]; norm_num, by rw [Real.sqrt_lt' (by norm_num)]; norm_num⟩

lemma sqrt_three_bounds : 1.73205 < Real.sqrt 3 ∧ Real.sqrt 3 < 1.73206 :=
  ⟨by rw [Real.lt_sqrt (by norm_num)]; norm_num, by rw [Real.sqrt_lt' (by norm_num)]; norm_num⟩

lemma sqrt_five_bounds : 2.23606 < Real.sqrt 5 ∧ Real.sqrt 5 < 2.23607 :=
  ⟨by rw [Real.lt_sqrt (by norm_num)]; norm_num, by rw [Real.sqrt_lt' (by norm_num)]; norm_num⟩

/-- **`rem:cc_counting`, the number:** `−1.2359 < ∑_{k=0}^{4} (−1)^k f_k Vol(Δ_k) < −1.2358`,
so the sum is `−1.236` to three decimals. -/
theorem altVolSum_bounds : -1.2359 < altVolSum ∧ altVolSum < -1.2358 := by
  rw [altVolSum_eq]
  obtain ⟨a1, a2⟩ := sqrt_two_bounds
  obtain ⟨b1, b2⟩ := sqrt_three_bounds
  obtain ⟨c1, c2⟩ := sqrt_five_bounds
  constructor <;> linarith

/-- The volume-weighted alternating sum is not `0` (unlike the unit-weight reduced sum). -/
theorem altVolSum_ne_zero : altVolSum ≠ 0 := by
  have := altVolSum_bounds.2; intro h; rw [h] at this; norm_num at this

#print axioms vol_values
#print axioms altVolSum_eq
#print axioms altVolSum_bounds
#print axioms altVolSum_ne_zero

/-! ### Mutant proved false -/

/-- Mutated volume: `2^k` in place of `2^{k/2}`. -/
def volBad (k : ℕ) : ℝ := Real.sqrt (k + 1) / (k.factorial * 2 ^ k)

/-- The mutated sum. -/
def altVolSumBad : ℝ := ∑ k ∈ range 5, (-1 : ℝ) ^ k * (f k : ℝ) * volBad k

lemma altVolSumBad_eq :
    altVolSumBad = 5 - 5 * Real.sqrt 2 + 5 / 4 * Real.sqrt 3 - 5 / 24 + Real.sqrt 5 / 384 := by
  obtain ⟨h0, h1, h2, h3, h4⟩ := f_values
  simp only [altVolSumBad, Finset.sum_range_succ, Finset.sum_range_zero, h0, h1, h2, h3, h4,
    volBad]
  push_cast
  rw [show (0 : ℝ) + 1 = 1 by norm_num, show (1 : ℝ) + 1 = 2 by norm_num,
    show (2 : ℝ) + 1 = 3 by norm_num, show (3 : ℝ) + 1 = 4 by norm_num,
    show (4 : ℝ) + 1 = 5 by norm_num, sqrt_four, Real.sqrt_one]
  norm_num [Nat.factorial]
  ring

/-- Mutant: with `2^k` the sum is `> −1`, hence not in the window `(−1.2359, −1.2358)`. -/
theorem mutant_vol_pow_false : ¬ (-1.2359 < altVolSumBad ∧ altVolSumBad < -1.2358) := by
  rw [altVolSumBad_eq]
  obtain ⟨a1, a2⟩ := sqrt_two_bounds
  obtain ⟨b1, b2⟩ := sqrt_three_bounds
  obtain ⟨c1, c2⟩ := sqrt_five_bounds
  intro h
  linarith [h.2]

#print axioms mutant_vol_pow_false

end

end LeanReal.FermionsF4
