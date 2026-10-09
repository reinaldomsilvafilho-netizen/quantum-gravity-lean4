import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# Book (Zenodo concept DOI 10.5281/zenodo.22290043), chapter 2, item L2

Source: `unified_quantum_gravity_book/chap02_geometric_flows_tensor_varieties.tex`,
Definition "Graphon Laplacian" (eq. `eq:graphon_laplacian`) and
Proposition "Dirichlet Energy of the Graphon Laplacian" (eq. `eq:graphon_dirichlet`):
> `(L_W u)(x) = d_W(x)u(x) − ∫₀¹ W(x,y)u(y)dy = ∫₀¹ W(x,y)(u(x) − u(y))dy`.
> Assume in addition that `0 ≤ W ∈ L^∞([0,1]²)`. Then `L_W` is bounded with `‖L_W‖ ≤ 2‖W‖_∞`,
> self-adjoint, and positive semi-definite on `L²([0,1])`. Its quadratic form satisfies
> `E_W(u) = ⟨u, L_W u⟩ = ½ ∬ W(x,y)(u(x) − u(y))² dx dy ≥ 0`.

Formal version: the FINITE-GRAPH case (declared reduction). `[0,1]` is replaced by a finite
vertex type `V`, integrals by sums, `W` by a real matrix with `W i j = W j i`.
* `lap_eq`: the two forms of the Laplacian agree (`d_W u − W u`).
* `dirichlet_identity`: `⟨u, L_W u⟩ = ½ ∑_{i,j} W_ij (u_i − u_j)²` for symmetric `W`
  (no sign condition).
* `dirichlet_nonneg`: `⟨u, L_W u⟩ ≥ 0` if moreover `W ≥ 0` entrywise.
* `lap_selfAdjoint`: `⟨v, L_W u⟩ = ⟨L_W v, u⟩` for symmetric `W`.
* Weighting each vertex by `1/|V|` (the step-graphon reading) multiplies both sides of the
  identity by `1/|V|²`, so it is not formalized separately.
* NOT covered: `L^2([0,1])`, `L^∞` kernels, measurability, the operator bound `‖L_W‖ ≤ 2‖W‖_∞`,
  and the paper's unbounded-degree counterexample.
-/

namespace LeanReal.Chap02Graphon

open Finset

variable {V : Type*} [Fintype V]

/-- Degree `d_W(i) = ∑_j W_ij`. -/
def deg (W : Matrix V V ℝ) (i : V) : ℝ := ∑ j, W i j

/-- `(L_W u)_i = ∑_j W_ij (u_i − u_j)`. -/
def lap (W : Matrix V V ℝ) (u : V → ℝ) (i : V) : ℝ := ∑ j, W i j * (u i - u j)

/-- `⟨u, v⟩ = ∑_i u_i v_i`. -/
def inner (u v : V → ℝ) : ℝ := ∑ i, u i * v i

theorem lap_eq (W : Matrix V V ℝ) (u : V → ℝ) (i : V) :
    lap W u i = deg W i * u i - ∑ j, W i j * u j := by
  simp only [lap, deg, mul_sub, sum_sub_distrib, sum_mul]

/-- Eq. `eq:graphon_dirichlet`, finite graph. -/
theorem dirichlet_identity (W : Matrix V V ℝ) (hW : ∀ i j, W i j = W j i) (u : V → ℝ) :
    inner u (lap W u) = 1 / 2 * ∑ i, ∑ j, W i j * (u i - u j) ^ 2 := by
  have hswap : ∑ i, ∑ j, W i j * (u i * (u i - u j))
      = ∑ i, ∑ j, W i j * (- u j * (u i - u j)) := by
    rw [sum_comm]
    refine sum_congr rfl fun i _ => sum_congr rfl fun j _ => ?_
    rw [hW j i]; ring
  have h1 : inner u (lap W u) = ∑ i, ∑ j, W i j * (u i * (u i - u j)) := by
    simp only [inner, lap, mul_sum]
    exact sum_congr rfl fun i _ => sum_congr rfl fun j _ => by ring
  have h2 : ∑ i, ∑ j, W i j * (u i - u j) ^ 2
      = ∑ i, ∑ j, W i j * (u i * (u i - u j)) + ∑ i, ∑ j, W i j * (- u j * (u i - u j)) := by
    rw [← sum_add_distrib]
    exact sum_congr rfl fun i _ => by rw [← sum_add_distrib]; exact sum_congr rfl fun j _ => by ring
  rw [h1, h2, ← hswap]; ring

theorem dirichlet_nonneg (W : Matrix V V ℝ) (hW : ∀ i j, W i j = W j i)
    (hpos : ∀ i j, 0 ≤ W i j) (u : V → ℝ) : 0 ≤ inner u (lap W u) := by
  rw [dirichlet_identity W hW u]
  have : 0 ≤ ∑ i, ∑ j, W i j * (u i - u j) ^ 2 :=
    sum_nonneg fun i _ => sum_nonneg fun j _ => mul_nonneg (hpos i j) (sq_nonneg _)
  linarith

theorem lap_selfAdjoint (W : Matrix V V ℝ) (hW : ∀ i j, W i j = W j i) (u v : V → ℝ) :
    inner v (lap W u) = inner (lap W v) u := by
  have h1 : inner v (lap W u)
      = ∑ i, ∑ j, W i j * v i * u i - ∑ i, ∑ j, W i j * v i * u j := by
    simp only [inner, lap, mul_sum, ← sum_sub_distrib]
    exact sum_congr rfl fun i _ => sum_congr rfl fun j _ => by ring
  have h2 : inner (lap W v) u
      = ∑ i, ∑ j, W i j * v i * u i - ∑ i, ∑ j, W i j * v j * u i := by
    simp only [inner, lap, sum_mul, ← sum_sub_distrib]
    exact sum_congr rfl fun i _ => sum_congr rfl fun j _ => by ring
  have h3 : ∑ i, ∑ j, W i j * v i * u j = ∑ i, ∑ j, W i j * v j * u i := by
    rw [sum_comm]
    exact sum_congr rfl fun i _ => sum_congr rfl fun j _ => by rw [hW j i]
  rw [h1, h2, h3]

/-! ## Non-vacuity: path graph on 3 vertices, `W₀₁ = W₁₀ = W₁₂ = W₂₁ = 1`, `u = (0,1,3)`.
Then `E = (1−0)² + (3−1)² = 5`. -/

def Wp : Matrix (Fin 3) (Fin 3) ℝ := !![0, 1, 0; 1, 0, 1; 0, 1, 0]
def up : Fin 3 → ℝ := ![0, 1, 3]

lemma Wp_symm : ∀ i j, Wp i j = Wp j i := by
  intro i j; fin_cases i <;> fin_cases j <;> rfl

example : inner up (lap Wp up) = 5 := by
  simp [inner, lap, Wp, up, Fin.sum_univ_three]; norm_num

example : 1 / 2 * ∑ i, ∑ j, Wp i j * (up i - up j) ^ 2 = 5 := by
  rw [← dirichlet_identity Wp Wp_symm up]
  simp [inner, lap, Wp, up, Fin.sum_univ_three]; norm_num

/-! ## Mutants (both hypotheses are needed, as the book says).
1. Drop `W ≥ 0`: `W ≡ −1` on two vertices, `u = (1,−1)`, gives `E = −4`.
2. Drop symmetry in the identity: `W = [[0,1],[0,0]]`, `u = (1,0)` gives `⟨u,Lu⟩ = 1 ≠ ½`. -/

theorem nonneg_mutant_false :
    ¬ (∀ (W : Matrix (Fin 2) (Fin 2) ℝ), (∀ i j, W i j = W j i) →
        ∀ u : Fin 2 → ℝ, 0 ≤ inner u (lap W u)) := by
  intro h
  have := h (fun _ _ => -1) (fun _ _ => rfl) ![1, -1]
  simp [inner, lap, Fin.sum_univ_two] at this
  norm_num at this

theorem symm_mutant_false :
    ¬ (∀ (W : Matrix (Fin 2) (Fin 2) ℝ) (u : Fin 2 → ℝ),
        inner u (lap W u) = 1 / 2 * ∑ i, ∑ j, W i j * (u i - u j) ^ 2) := by
  intro h
  have := h !![0, 1; 0, 0] ![1, 0]
  simp [inner, lap, Fin.sum_univ_two] at this

end LeanReal.Chap02Graphon

#print axioms LeanReal.Chap02Graphon.lap_eq
#print axioms LeanReal.Chap02Graphon.dirichlet_identity
#print axioms LeanReal.Chap02Graphon.dirichlet_nonneg
#print axioms LeanReal.Chap02Graphon.lap_selfAdjoint
#print axioms LeanReal.Chap02Graphon.nonneg_mutant_false
#print axioms LeanReal.Chap02Graphon.symm_mutant_false
