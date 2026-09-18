/-
Volume II - Bridge 13: Foundations of Graph Number Theory
Author: Reinaldo Maia Silva-Filho (PPGEE/DES/UFLA)
Formal Proof of Dyadic Arithmetization Injectivity and Sabidussi-Vizing Prime Graph Arithmetic
-/

namespace SpectralGraph

-- Dyadic Arithmetization of Binary Sieve Addresses:
-- Every path in the adaptive decision tree is a list of Bool (0 = false, 1 = true).
-- Prepending a leading 1 bit maps any binary string bijectively into Nat_{>= 1}.
def dyadic_val : List Bool → Nat
  | [] => 1
  | false :: bs => 2 * dyadic_val bs
  | true  :: bs => 2 * dyadic_val bs + 1

-- Dyadic value is strictly positive for any binary address
theorem dyadic_val_pos (bs : List Bool) : dyadic_val bs > 0 := by
  induction bs with
  | nil =>
    dsimp [dyadic_val]
    omega
  | cons b rest ih =>
    cases b <;> dsimp [dyadic_val] <;> omega

-- Injectivity: distinct binary paths yield distinct graph numbers
theorem dyadic_val_injective (p1 p2 : List Bool) :
    dyadic_val p1 = dyadic_val p2 → p1 = p2 := by
  induction p1 generalizing p2 with
  | nil =>
    intro h
    cases p2 with
    | nil => rfl
    | cons b rest =>
      have hrest := dyadic_val_pos rest
      cases b <;> dsimp [dyadic_val] at h <;> omega
  | cons b1 rest1 ih1 =>
    intro h
    cases p2 with
    | nil =>
      have hrest1 := dyadic_val_pos rest1
      cases b1 <;> dsimp [dyadic_val] at h <;> omega
    | cons b2 rest2 =>
      cases b1 <;> cases b2 <;> dsimp [dyadic_val] at h
      · have h_eq : dyadic_val rest1 = dyadic_val rest2 := by omega
        have h_rest := ih1 rest2 h_eq
        rw [h_rest]
      · exfalso; omega
      · exfalso; omega
      · have h_eq : dyadic_val rest1 = dyadic_val rest2 := by omega
        have h_rest := ih1 rest2 h_eq
        rw [h_rest]

-- Graph Number Bijectivity Corollary:
-- If the adaptive sieve assigns distinct binary cut paths to non-isomorphic graphs G1 and G2,
-- their canonical graph numbers are strictly distinct.
theorem graph_number_distinct (p1 p2 : List Bool) (h_diff : p1 ≠ p2) :
    dyadic_val p1 ≠ dyadic_val p2 := by
  intro h_eq
  have h_same := dyadic_val_injective p1 p2 h_eq
  exact h_diff h_same

-- Prime Definition in Pure Lean 4:
-- A natural number p is prime if p >= 2 and any factorization p = a * b implies a = 1 or b = 1.
def IsPrime (p : Nat) : Prop :=
  p ≥ 2 ∧ ∀ a b : Nat, p = a * b → a = 1 ∨ b = 1

-- Sabidussi-Vizing Cartesian Graph Arithmetic:
-- The vertex count of the Cartesian product G1 square G2 is |V1| * |V2|.
structure CartesianProduct where
  v1 : Nat
  v2 : Nat
  v_prod : Nat
  h_v1_ge_2 : v1 ≥ 2
  h_v2_ge_2 : v2 ≥ 2
  h_prod : v_prod = v1 * v2

-- Auxiliary lemma on product growth
theorem mul_ge_two_gt (a b : Nat) (ha : a ≥ 2) (hb : b ≥ 2) : a * b > a := by
  have hb1 : b = (b - 1) + 1 := by omega
  rw [hb1, Nat.mul_add, Nat.mul_one]
  have : a * (b - 1) ≥ a * 1 := by
    apply Nat.mul_le_mul_left
    omega
  rw [Nat.mul_one] at this
  omega

-- Composite graphs have strictly larger vertex count than their factors
theorem cartesian_composite_vertex_bound (cp : CartesianProduct) :
    cp.v_prod > cp.v1 ∧ cp.v_prod > cp.v2 := by
  have h1 := cp.h_v1_ge_2
  have h2 := cp.h_v2_ge_2
  have hp := cp.h_prod
  rw [hp]
  constructor
  · exact mul_ge_two_gt cp.v1 cp.v2 h1 h2
  · rw [Nat.mul_comm]
    exact mul_ge_two_gt cp.v2 cp.v1 h2 h1

-- Prime Order Implies Cartesian Primality:
-- If a connected graph G has a prime number of vertices p,
-- it cannot be factored as G1 square G2 non-trivially.
theorem prime_order_is_cartesian_prime (p : Nat) (hp_prime : IsPrime p)
    (cp : CartesianProduct) (h_eq : cp.v_prod = p) : False := by
  have hp := cp.h_prod
  have h1 := cp.h_v1_ge_2
  have h2 := cp.h_v2_ge_2
  have h_fact := hp_prime.2 cp.v1 cp.v2
  have h_decomp : p = cp.v1 * cp.v2 := by rw [← h_eq, hp]
  have h_cases := h_fact h_decomp
  cases h_cases with
  | inl h_one => omega
  | inr h_two => omega

end SpectralGraph
