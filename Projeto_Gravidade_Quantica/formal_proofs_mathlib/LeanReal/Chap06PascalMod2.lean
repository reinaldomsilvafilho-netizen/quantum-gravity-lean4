import Mathlib.Data.Nat.Choose.Lucas
import Mathlib.RingTheory.Binomial
import Mathlib.Algebra.Ring.NegOnePow
import Mathlib.Tactic

/-!
# Chapter 6, `prop:pascal_mod2`: the combinatorial core

Batch B5 of `PLANO_LIVRO_A.md`, item 2.

Source: `unified_quantum_gravity_book/chap06_sierpinski_fractal_resolvents_spectral_reduction.tex`,
Proposition "Box-counting dimension of Pascal's triangle modulo 2; classical"
(`prop:pascal_mod2`), its proof, and the identity just before it.

Frozen statement. `P_k = {2^{-k}(n,j) : 0 ≤ j ≤ n < 2^k, C(n,j) odd}`. Then `P_k → 𝒮` in the
Hausdorff metric, `𝒮` affinely equivalent to the Sierpinski gasket, and
`dim_box 𝒮 = dim_H 𝒮 = ln 3/ln 2`; the same for the parity pattern of `C(−a,j)`,
`1 ≤ a ≤ 2^k`, `0 ≤ j`, `a + j ≤ 2^k`. Proof steps: Lucas; the block decomposition
`P_k = Φ₁(P_{k−1}) ∪ Φ₂(P_{k−1}) ∪ Φ₃(P_{k−1})` with `Φ₁z = z/2`, `Φ₂z = z/2 + (1/2,0)`,
`Φ₃z = z/2 + (1/2,1/2)`; `#P_k = 3^k`; `C(−a,j) = (−1)^j C(a+j−1,j)` for `a ≥ 1`, `j ≥ 0`.

## Declared reduction

Formalized: the top-bit Lucas step (`odd_choose_top`), the block decomposition at the level of
integer indices (`S_succ`) and in `ℝ²` for the rescaled sets (`P_succ`, three maps `Φ_i`),
`#P_k = 3^k` (`card_P`), the identity `C(−a,j) = (−1)^j C(a+j−1,j)` over `ℤ` with `Ring.choose`
(`choose_neg_int`), and `#(odd entries of C(−a,j) in the stated range) = 3^k` (`card_T`).
Not formalized (Mathlib lacks them): Hausdorff convergence (Hutchinson), the open set condition
and the box and Hausdorff dimensions of the attractor.
-/

noncomputable section

namespace LeanReal.Chap06PascalMod2

open Finset

/-- Integer indices of `P_k`: pairs `(n,j)` with `j ≤ n < 2^k` and `C(n,j)` odd. -/
def S (k : ℕ) : Finset (ℕ × ℕ) :=
  ((range (2 ^ k)) ×ˢ (range (2 ^ k))).filter (fun p => p.2 ≤ p.1 ∧ Odd (p.1.choose p.2))

/-- The book's `P_k ⊂ ℝ²`: the rescaled points `2^{-k}(n,j)`, `(n,j) ∈ S k`. -/
def P (k : ℕ) : Finset (ℝ × ℝ) :=
  (S k).image (fun p => ((p.1 : ℝ) / 2 ^ k, (p.2 : ℝ) / 2 ^ k))

/-- The three contractions of the proof. -/
def Φ₁ (z : ℝ × ℝ) : ℝ × ℝ := (z.1 / 2, z.2 / 2)
/-- Second contraction, `z/2 + (1/2, 0)`. -/
def Φ₂ (z : ℝ × ℝ) : ℝ × ℝ := (z.1 / 2 + 1 / 2, z.2 / 2)
/-- Third contraction, `z/2 + (1/2, 1/2)`. -/
def Φ₃ (z : ℝ × ℝ) : ℝ × ℝ := (z.1 / 2 + 1 / 2, z.2 / 2 + 1 / 2)

/-- Lucas' theorem mod 2, lowest binary digit: `C(n,j)` is odd iff `C(n mod 2, j mod 2)` and
`C(⌊n/2⌋, ⌊j/2⌋)` are odd. -/
theorem odd_choose_low (n j : ℕ) :
    Odd (n.choose j) ↔ Odd ((n % 2).choose (j % 2)) ∧ Odd ((n / 2).choose (j / 2)) := by
  have h := Choose.choose_modEq_choose_mod_mul_choose_div_nat (n := n) (k := j) (p := 2)
  rw [← Nat.odd_mul, Nat.odd_iff, Nat.odd_iff, h]

/-- Lucas' theorem mod 2, highest binary digit (the step of the book's proof): for
`n', j' < 2^k`, `C(2^k e + n', 2^k f + j')` is odd iff `C(e,f)` and `C(n',j')` are odd. -/
theorem odd_choose_top (k : ℕ) : ∀ (e f n' j' : ℕ), n' < 2 ^ k → j' < 2 ^ k →
    (Odd ((2 ^ k * e + n').choose (2 ^ k * f + j')) ↔
      Odd (e.choose f) ∧ Odd (n'.choose j')) := by
  induction k with
  | zero =>
    intro e f n' j' hn hj
    simp only [pow_zero, Nat.lt_one_iff] at hn hj
    subst hn; subst hj; simp
  | succ k ih =>
    intro e f n' j' hn hj
    have e1 : 2 ^ (k + 1) * e + n' = n' + 2 * (2 ^ k * e) := by ring
    have e2 : 2 ^ (k + 1) * f + j' = j' + 2 * (2 ^ k * f) := by ring
    rw [e1, e2, odd_choose_low, Nat.add_mul_mod_self_left, Nat.add_mul_mod_self_left,
      Nat.add_mul_div_left _ _ two_pos, Nat.add_mul_div_left _ _ two_pos,
      add_comm (n' / 2), add_comm (j' / 2),
      ih e f (n' / 2) (j' / 2) (by rw [pow_succ] at hn; omega) (by rw [pow_succ] at hj; omega),
      odd_choose_low n' j']
    tauto

private lemma odd_choose_le {n j : ℕ} (h : Odd (n.choose j)) : j ≤ n := by
  by_contra hc
  rw [Nat.choose_eq_zero_of_lt (by omega)] at h
  exact (Nat.not_odd_zero h)

/-- Block decomposition of the proof at the level of indices:
`S_{k+1} = S_k ∪ (S_k + (2^k,0)) ∪ (S_k + (2^k,2^k))`; the middle block is removed. -/
theorem S_succ (k : ℕ) :
    S (k + 1) = S k ∪ (S k).image (fun p => (p.1 + 2 ^ k, p.2)) ∪
      (S k).image (fun p => (p.1 + 2 ^ k, p.2 + 2 ^ k)) := by
  ext ⟨n, j⟩
  simp only [S, mem_union, mem_image, mem_filter, mem_product, mem_range, Prod.mk.injEq,
    Prod.exists]
  have hp : 2 ^ (k + 1) = 2 * 2 ^ k := by ring
  have hpos : 0 < 2 ^ k := pow_pos two_pos k
  constructor
  · rintro ⟨⟨hn, hj⟩, hjn, hodd⟩
    rcases lt_or_ge n (2 ^ k) with h1 | h1
    · left; left; exact ⟨⟨h1, by omega⟩, hjn, hodd⟩
    · rcases lt_or_ge j (2 ^ k) with h2 | h2
      · -- second block: e = 1, f = 0
        left; right
        refine ⟨n - 2 ^ k, j, ⟨⟨by omega, h2⟩, ?_⟩, by omega, rfl⟩
        have := (odd_choose_top k 1 0 (n - 2 ^ k) j (by omega) h2).1
          (by convert hodd using 2 <;> [omega; omega])
        exact ⟨odd_choose_le this.2, this.2⟩
      · -- third block: e = 1, f = 1
        right
        refine ⟨n - 2 ^ k, j - 2 ^ k, ⟨⟨by omega, by omega⟩, ?_⟩, by omega, by omega⟩
        have := (odd_choose_top k 1 1 (n - 2 ^ k) (j - 2 ^ k) (by omega) (by omega)).1
          (by convert hodd using 2 <;> [omega; omega])
        exact ⟨odd_choose_le this.2, this.2⟩
  · rintro ((⟨⟨hn, hj⟩, hjn, hodd⟩ | ⟨a, b, ⟨⟨ha, hb⟩, hba, hodd⟩, rfl, rfl⟩) |
      ⟨a, b, ⟨⟨ha, hb⟩, hba, hodd⟩, rfl, rfl⟩)
    · exact ⟨⟨by omega, by omega⟩, hjn, hodd⟩
    · refine ⟨⟨by omega, by omega⟩, by omega, ?_⟩
      have := (odd_choose_top k 1 0 a b ha hb).2 ⟨by simp, hodd⟩
      convert this using 2 <;> omega
    · refine ⟨⟨by omega, by omega⟩, by omega, ?_⟩
      have := (odd_choose_top k 1 1 a b ha hb).2 ⟨by simp, hodd⟩
      convert this using 2 <;> omega

/-- `#S_k = 3^k`. -/
theorem card_S (k : ℕ) : (S k).card = 3 ^ k := by
  induction k with
  | zero => decide
  | succ k ih =>
    have hpos : 0 < 2 ^ k := pow_pos two_pos k
    have bound : ∀ p ∈ S k, p.1 < 2 ^ k ∧ p.2 ≤ p.1 := by
      intro p hp
      simp only [S, mem_filter, mem_product, mem_range] at hp
      exact ⟨hp.1.1, hp.2.1⟩
    have inj2 : Set.InjOn (fun p : ℕ × ℕ => (p.1 + 2 ^ k, p.2)) (S k) := by
      intro p _ q _ h; simp only [Prod.mk.injEq] at h; ext <;> omega
    have inj3 : Set.InjOn (fun p : ℕ × ℕ => (p.1 + 2 ^ k, p.2 + 2 ^ k)) (S k) := by
      intro p _ q _ h; simp only [Prod.mk.injEq] at h; ext <;> omega
    rw [S_succ, card_union_of_disjoint, card_union_of_disjoint, card_image_of_injOn inj2,
      card_image_of_injOn inj3, ih, pow_succ]
    · ring
    · rw [disjoint_left]
      intro x hx hx'
      obtain ⟨p, hp, rfl⟩ := mem_image.1 hx'
      have h1 : p.1 + 2 ^ k < 2 ^ k := (bound _ hx).1
      omega
    · rw [disjoint_left]
      intro x hx hx'
      obtain ⟨q, hq, rfl⟩ := mem_image.1 hx'
      have hq' := bound q hq
      rcases mem_union.1 hx with hx | hx
      · have h1 : q.1 + 2 ^ k < 2 ^ k := (bound _ hx).1
        omega
      · obtain ⟨p, hp, hpq⟩ := mem_image.1 hx
        have := bound p hp
        simp only [Prod.mk.injEq] at hpq
        omega

/-- **`#P_k = 3^k`** (the count stated in the proof of `prop:pascal_mod2`). -/
theorem card_P (k : ℕ) : (P k).card = 3 ^ k := by
  rw [P, card_image_of_injective, card_S]
  intro p q h
  simp only [Prod.mk.injEq] at h
  have h2 : (2 : ℝ) ^ k ≠ 0 := pow_ne_zero _ two_ne_zero
  obtain ⟨h1, h3⟩ := h
  rw [div_left_inj' h2] at h1 h3
  ext
  · exact_mod_cast h1
  · exact_mod_cast h3

/-- **Block decomposition in `ℝ²`:** `P_{k+1} = Φ₁(P_k) ∪ Φ₂(P_k) ∪ Φ₃(P_k)`. -/
theorem P_succ (k : ℕ) :
    P (k + 1) = (P k).image Φ₁ ∪ (P k).image Φ₂ ∪ (P k).image Φ₃ := by
  have h2 : (2 : ℝ) ^ k ≠ 0 := pow_ne_zero _ two_ne_zero
  set g : ℕ × ℕ → ℝ × ℝ := fun p => ((p.1 : ℝ) / 2 ^ k, (p.2 : ℝ) / 2 ^ k) with hg
  have e1 : (fun p : ℕ × ℕ => ((p.1 : ℝ) / 2 ^ (k + 1), (p.2 : ℝ) / 2 ^ (k + 1))) = Φ₁ ∘ g := by
    funext p
    simp only [hg, Function.comp_apply, Φ₁, pow_succ, Prod.mk.injEq]
    constructor <;> field_simp
  have e2 : (fun p : ℕ × ℕ => ((p.1 : ℝ) / 2 ^ (k + 1), (p.2 : ℝ) / 2 ^ (k + 1))) ∘
      (fun p : ℕ × ℕ => (p.1 + 2 ^ k, p.2)) = Φ₂ ∘ g := by
    funext p
    simp only [hg, Function.comp_apply, Φ₂, pow_succ, Nat.cast_add, Nat.cast_pow,
      Nat.cast_ofNat, Prod.mk.injEq]
    constructor <;> field_simp
  have e3 : (fun p : ℕ × ℕ => ((p.1 : ℝ) / 2 ^ (k + 1), (p.2 : ℝ) / 2 ^ (k + 1))) ∘
      (fun p : ℕ × ℕ => (p.1 + 2 ^ k, p.2 + 2 ^ k)) = Φ₃ ∘ g := by
    funext p
    simp only [hg, Function.comp_apply, Φ₃, pow_succ, Nat.cast_add, Nat.cast_pow,
      Nat.cast_ofNat, Prod.mk.injEq]
    constructor <;> field_simp
  rw [P, P, S_succ, image_union, image_union, image_image, image_image, image_image,
    image_image, e2, e3, e1, image_image]

/-! ### Negative upper index -/

/-- `C(−a,j) = (−1)^j C(a+j−1,j)` for `a ≥ 1`, with the generalized binomial `Ring.choose`. -/
theorem choose_neg_int (a j : ℕ) (ha : 1 ≤ a) :
    Ring.choose (-(a : ℤ)) j = (-1) ^ j * ((a + j - 1).choose j : ℤ) := by
  have hc : ((a : ℤ) + j - 1) = ((a + j - 1 : ℕ) : ℤ) := by push_cast [Nat.cast_sub (by omega : 1 ≤ a + j)]; ring
  rw [Ring.choose_neg, hc, Ring.choose_natCast, Units.smul_def, Int.coe_negOnePow_natCast,
    smul_eq_mul]

/-- Parity transfer: `C(−a,j)` is odd iff `C(a+j−1,j)` is odd (`a ≥ 1`). -/
theorem odd_choose_neg_iff (a j : ℕ) (ha : 1 ≤ a) :
    Odd (Ring.choose (-(a : ℤ)) j) ↔ Odd ((a + j - 1).choose j) := by
  rw [choose_neg_int a j ha]
  rcases neg_one_pow_eq_or ℤ j with h | h <;> rw [h] <;> simp [Int.odd_coe_nat]

/-- Integer indices of the negative-upper-index pattern: `1 ≤ a`, `0 ≤ j`, `a + j ≤ 2^k`,
`C(−a,j)` odd. -/
def T (k : ℕ) : Finset (ℕ × ℕ) :=
  ((Icc 1 (2 ^ k)) ×ˢ (range (2 ^ k))).filter
    (fun p => p.1 + p.2 ≤ 2 ^ k ∧ Odd (Ring.choose (-(p.1 : ℤ)) p.2))

/-- **Negative upper index:** the affine map `(a,j) ↦ (a+j−1, j)` is a bijection from `T k`
onto `S k`, so the pattern has `3^k` odd entries. -/
theorem card_T (k : ℕ) : (T k).card = 3 ^ k := by
  rw [← card_S k]
  refine card_nbij' (fun p => (p.1 + p.2 - 1, p.2)) (fun q => (q.1 - q.2 + 1, q.2)) ?_ ?_ ?_ ?_
  · intro p hp
    simp only [T, coe_filter, mem_product, mem_Icc, mem_range, Set.mem_ofPred_eq] at hp
    simp only [S, coe_filter, mem_product, mem_range, Set.mem_ofPred_eq]
    obtain ⟨⟨⟨h1, _⟩, _⟩, hs, hodd⟩ := hp
    exact ⟨⟨by omega, by omega⟩, by omega, (odd_choose_neg_iff _ _ h1).1 hodd⟩
  · intro q hq
    simp only [S, coe_filter, mem_product, mem_range, Set.mem_ofPred_eq] at hq
    simp only [T, coe_filter, mem_product, mem_Icc, mem_range, Set.mem_ofPred_eq]
    obtain ⟨⟨hn, _⟩, hjn, hodd⟩ := hq
    refine ⟨⟨⟨by omega, by omega⟩, by omega⟩, by omega, ?_⟩
    rw [odd_choose_neg_iff _ _ (by omega)]
    convert hodd using 2; omega
  · intro p hp
    simp only [T, coe_filter, mem_product, mem_Icc, mem_range, Set.mem_ofPred_eq] at hp
    refine Prod.ext ?_ rfl
    dsimp only
    omega
  · intro q hq
    simp only [S, coe_filter, mem_product, mem_range, Set.mem_ofPred_eq] at hq
    refine Prod.ext ?_ rfl
    dsimp only
    omega

/-! ### Non-vacuity witnesses -/

/-- Witness: `S_2` is the explicit 9-point pattern; the middle-block point `(2,1)` is absent
(`C(2,1) = 2`), so the triangle is not full. -/
theorem witness_S2 :
    S 2 = {(0, 0), (1, 0), (1, 1), (2, 0), (2, 2), (3, 0), (3, 1), (3, 2), (3, 3)} ∧
    (2, 1) ∉ S 2 := by
  constructor <;> decide

/-- Witness for the negative index: `(1,1)` and `(2,2)` lie in `T 2`
(`C(−1,1) = −1`, `C(−2,2) = 3`), `(2,1)` does not (`C(−2,1) = −2`). -/
theorem witness_T2 : (1, 1) ∈ T 2 ∧ (2, 2) ∈ T 2 ∧ (2, 1) ∉ T 2 := by
  simp only [T, mem_filter, mem_product, mem_Icc, mem_range]
  refine ⟨⟨by norm_num, by norm_num, ?_⟩, ⟨by norm_num, by norm_num, ?_⟩, ?_⟩
  · simp
  · rw [odd_choose_neg_iff 2 2 (by norm_num)]; decide
  · rw [odd_choose_neg_iff 2 1 (by norm_num)]; decide

/-! ### Mutants (negations proved) -/

/-- Mutant 1: "every entry of the triangle is odd" (`#S_k = 2^k(2^k+1)/2`) is false at `k = 2`. -/
theorem mutant_full_triangle_false :
    ¬ ∀ k : ℕ, (S k).card = 2 ^ k * (2 ^ k + 1) / 2 := by
  intro h; have := h 2; rw [card_S] at this; norm_num at this

/-- Mutant 2: placing the third block at `(0, 2^k)` instead of `(2^k, 2^k)` is false (`k = 1`). -/
theorem mutant_wrong_block_false :
    ¬ ∀ k : ℕ, S (k + 1) = S k ∪ (S k).image (fun p => (p.1 + 2 ^ k, p.2)) ∪
      (S k).image (fun p => (p.1, p.2 + 2 ^ k)) := by
  intro h; have := h 1; revert this; decide

/-- Mutant 3: dropping the shift, "`C(−a,j)` odd iff `C(a,j)` odd", is false (`a = 1`, `j = 2`:
`C(−1,2) = 1`, `C(1,2) = 0`). -/
theorem mutant_no_shift_false :
    ¬ ∀ a j : ℕ, 1 ≤ a → (Odd (Ring.choose (-(a : ℤ)) j) ↔ Odd (a.choose j)) := by
  intro h
  have := h 1 2 le_rfl
  rw [odd_choose_neg_iff 1 2 le_rfl] at this
  revert this; decide

end LeanReal.Chap06PascalMod2

#print axioms LeanReal.Chap06PascalMod2.odd_choose_low
#print axioms LeanReal.Chap06PascalMod2.odd_choose_top
#print axioms LeanReal.Chap06PascalMod2.S_succ
#print axioms LeanReal.Chap06PascalMod2.card_S
#print axioms LeanReal.Chap06PascalMod2.card_P
#print axioms LeanReal.Chap06PascalMod2.P_succ
#print axioms LeanReal.Chap06PascalMod2.choose_neg_int
#print axioms LeanReal.Chap06PascalMod2.odd_choose_neg_iff
#print axioms LeanReal.Chap06PascalMod2.card_T
#print axioms LeanReal.Chap06PascalMod2.witness_S2
#print axioms LeanReal.Chap06PascalMod2.witness_T2
#print axioms LeanReal.Chap06PascalMod2.mutant_full_triangle_false
#print axioms LeanReal.Chap06PascalMod2.mutant_wrong_block_false
#print axioms LeanReal.Chap06PascalMod2.mutant_no_shift_false
