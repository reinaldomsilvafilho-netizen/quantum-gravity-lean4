import Mathlib.Topology.MetricSpace.ProperSpace
import Mathlib.Analysis.Normed.Group.Basic
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Algebra.BigOperators.Pi
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Topology.Order.Compact

/-!
# Book (Zenodo concept DOI 10.5281/zenodo.22290043), chapter 1, `thm:tensor_weierstrass`

Source: `unified_quantum_gravity_book/chap01_functional_realizations_matrices_tensors.tex`,
Theorem `thm:tensor_weierstrass` ("Functional Well-Posedness over Compact Product Manifolds"):
> `Φ(T)(u¹, …, uᵏ) = ∑_J T_J u¹_{j₁} ⋯ uᵏ_{jₖ}` on `M = ∏_α S^{d_α − 1}`.
> (i) `σ_max(T) = sup_M Φ(T)` is attained; (ii) critical points satisfy
> `T(u¹, …, ·, …, uᵏ) = σ u^α` for every `α`, with ONE common `σ`; and a best rank-one
> approximation `σ_max u*¹ ⊗ ⋯ ⊗ u*ᵏ` exists. The proof uses
> `‖T − λ u¹ ⊗ ⋯ ⊗ uᵏ‖²_F = ‖T‖²_F − 2λΦ(u) + λ²` on `M`.

Formal version, `k`-th order real tensors `T : (∀ α : Fin k, Fin (d α)) → ℝ`, factors
`u : ∀ α, Fin (d α) → ℝ`, `M = {u | ∀ α, ∑ⱼ (u α j)² = 1}`:
* `isCompact_sphereProd`, `sphereProd_nonempty`, `exists_max`: item (i) (needs `d α ≥ 1`);
* `euler`: `⟨u^α, ∇_α Φ⟩ = Φ(u)` (multilinear Euler identity);
* `multipliers_eq`: item (ii), the algebraic step only: if `∇_α Φ(u) = μ_α u^α` for all `α`
  and `u ∈ M`, then `μ_α = Φ(u)` for all `α`. The existence of the multipliers at a constrained
  critical point (Lagrange multiplier theorem on `M`) is NOT formalized: it enters as the
  hypothesis `hcrit`;
* `rank_one_identity`: the Frobenius identity used in the proof;
* `best_rank_one`: for `k ≥ 1` and all `d α ≥ 1`, there is `u* ∈ M` with
  `‖T − Φ(u*) u*⊗‖² ≤ ‖T − λ v⊗‖²` for every `λ` and every `v ∈ M`, and `Φ(u*) = σ_max`.
NOT covered: the smooth structure of `M` and `Φ ∈ C^∞(M)`, the Lagrange multiplier theorem,
the Z-eigenvalue remark for symmetric tensors.
-/

namespace LeanReal.Chap01Tensor

open Finset

variable {k : ℕ} {d : Fin k → ℕ}

/-- The multilinear form `Φ(T)(u) = ∑_J T_J ∏_α u^α_{J α}`. -/
def Phi (T : (∀ α : Fin k, Fin (d α)) → ℝ) (u : ∀ α : Fin k, Fin (d α) → ℝ) : ℝ :=
  ∑ J : (∀ α, Fin (d α)), T J * ∏ α, u α (J α)

/-- The product of unit spheres `M = ∏_α S^{d_α − 1}`. -/
def sphereProd (d : Fin k → ℕ) : Set (∀ α : Fin k, Fin (d α) → ℝ) :=
  {u | ∀ α, ∑ j, u α j ^ 2 = 1}

/-- The partial gradient `(∇_α Φ)_j = ∑_{J : J α = j} T_J ∏_{β ≠ α} u^β_{J β}`, i.e. the
vector `T(u¹, …, u^{α−1}, ·, u^{α+1}, …, uᵏ)` of `eq:tensor_critical`. -/
def partialGrad (T : (∀ α : Fin k, Fin (d α)) → ℝ) (u : ∀ α : Fin k, Fin (d α) → ℝ)
    (α : Fin k) (j : Fin (d α)) : ℝ :=
  ∑ J : (∀ β, Fin (d β)), if J α = j then T J * ∏ β ∈ univ.erase α, u β (J β) else 0

/-- `Φ(T)` is continuous (a polynomial in the entries). -/
theorem continuous_Phi (T : (∀ α : Fin k, Fin (d α)) → ℝ) : Continuous (Phi T) := by
  unfold Phi
  fun_prop

/-- `M` is compact (closed and bounded in a finite-dimensional space). -/
theorem isCompact_sphereProd (d : Fin k → ℕ) : IsCompact (sphereProd d) := by
  apply Metric.isCompact_of_isClosed_isBounded
  · have : sphereProd d = ⋂ α, {u : ∀ α : Fin k, Fin (d α) → ℝ | ∑ j, u α j ^ 2 = 1} := by
      ext u; simp [sphereProd]
    rw [this]
    exact isClosed_iInter fun α => isClosed_eq (by fun_prop) continuous_const
  · refine (Metric.isBounded_closedBall (x := (0 : ∀ α : Fin k, Fin (d α) → ℝ)) (r := 1)).subset ?_
    intro u hu
    rw [Metric.mem_closedBall, dist_zero_right, pi_norm_le_iff_of_nonneg zero_le_one]
    intro α
    rw [pi_norm_le_iff_of_nonneg zero_le_one]
    intro j
    rw [Real.norm_eq_abs, ← sq_le_one_iff_abs_le_one]
    calc u α j ^ 2 ≤ ∑ i, u α i ^ 2 :=
          single_le_sum (f := fun i => u α i ^ 2) (fun i _ => sq_nonneg _) (mem_univ j)
      _ = 1 := hu α

/-- `M` is non-empty when every `d α ≥ 1`. -/
theorem sphereProd_nonempty (hd : ∀ α, 0 < d α) : (sphereProd d).Nonempty := by
  refine ⟨fun α j => if (j : ℕ) = 0 then 1 else 0, fun α => ?_⟩
  rw [Finset.sum_eq_single (⟨0, hd α⟩ : Fin (d α))]
  · simp
  · intro b _ hb
    have : (b : ℕ) ≠ 0 := fun h => hb (Fin.ext h)
    simp [this]
  · simp

/-- Item (i): `σ_max(T) = sup_M Φ(T)` is attained. -/
theorem exists_max (T : (∀ α : Fin k, Fin (d α)) → ℝ) (hd : ∀ α, 0 < d α) :
    ∃ u ∈ sphereProd d, IsMaxOn (Phi T) (sphereProd d) u :=
  (isCompact_sphereProd d).exists_isMaxOn (sphereProd_nonempty hd)
    (continuous_Phi T).continuousOn

/-- Multilinear Euler identity: `⟨u^α, ∇_α Φ(u)⟩ = Φ(u)`. -/
theorem euler (T : (∀ α : Fin k, Fin (d α)) → ℝ) (u : ∀ α : Fin k, Fin (d α) → ℝ)
    (α : Fin k) : ∑ j, u α j * partialGrad T u α j = Phi T u := by
  simp only [partialGrad, mul_sum, Phi]
  rw [sum_comm]
  refine sum_congr rfl fun J _ => ?_
  rw [sum_eq_single (J α)]
  · simp only [↓reduceIte]
    rw [← mul_prod_erase univ (fun β => u β (J β)) (mem_univ α)]
    ring
  · intro b _ hb; simp [Ne.symm hb]
  · simp

/-- Item (ii), algebraic step: if `∇_α Φ(u) = μ_α u^α` for every `α` and `u ∈ M`, then all
multipliers equal `Φ(u)`; so the singular-value equations share one `σ = Φ(u)`. -/
theorem multipliers_eq (T : (∀ α : Fin k, Fin (d α)) → ℝ) (u : ∀ α : Fin k, Fin (d α) → ℝ)
    (hu : u ∈ sphereProd d) (μ : Fin k → ℝ)
    (hcrit : ∀ α j, partialGrad T u α j = μ α * u α j) (α : Fin k) : μ α = Phi T u := by
  rw [← euler T u α]
  simp only [hcrit]
  have : ∑ j, u α j * (μ α * u α j) = μ α * ∑ j, u α j ^ 2 := by
    rw [mul_sum]; exact sum_congr rfl fun j _ => by ring
  rw [this, hu α, mul_one]

/-- Squared Frobenius norm. -/
def frobSq (X : (∀ α : Fin k, Fin (d α)) → ℝ) : ℝ := ∑ J, X J ^ 2

/-- The rank-one tensor `λ u¹ ⊗ ⋯ ⊗ uᵏ`. -/
def rankOne (lam : ℝ) (u : ∀ α : Fin k, Fin (d α) → ℝ) : (∀ α : Fin k, Fin (d α)) → ℝ :=
  fun J => lam * ∏ α, u α (J α)

/-- The identity in the proof: on `M`, `‖T − λu⊗‖² = ‖T‖² − 2λΦ(u) + λ²`. -/
theorem rank_one_identity (T : (∀ α : Fin k, Fin (d α)) → ℝ) (u : ∀ α : Fin k, Fin (d α) → ℝ)
    (hu : u ∈ sphereProd d) (lam : ℝ) :
    frobSq (fun J => T J - rankOne lam u J) = frobSq T - 2 * lam * Phi T u + lam ^ 2 := by
  have hprod : ∑ J : (∀ α, Fin (d α)), ∏ α, u α (J α) ^ 2 = 1 := by
    rw [← Fintype.prod_sum (fun α j => u α j ^ 2)]
    exact prod_eq_one fun α _ => hu α
  have e : ∀ J : (∀ α, Fin (d α)), (T J - rankOne lam u J) ^ 2
      = T J ^ 2 - 2 * lam * (T J * ∏ α, u α (J α)) + lam ^ 2 * ∏ α, u α (J α) ^ 2 := by
    intro J; simp only [rankOne, prod_pow]; ring
  simp only [frobSq, e, sum_add_distrib, sum_sub_distrib, ← mul_sum, hprod, Phi]
  ring

/-- Flipping the sign of the first factor negates `Φ` and stays in `M` (`k ≥ 1`). -/
lemma flip_mem_neg (T : (∀ α : Fin k, Fin (d α)) → ℝ) (hk : 0 < k)
    (v : ∀ α : Fin k, Fin (d α) → ℝ) (hv : v ∈ sphereProd d) :
    ∃ w ∈ sphereProd d, Phi T w = -Phi T v := by
  set α₀ : Fin k := ⟨0, hk⟩
  let c : Fin k → ℝ := fun α => if α = α₀ then -1 else 1
  refine ⟨fun α j => c α * v α j, fun α => ?_, ?_⟩
  · have hc : c α ^ 2 = 1 := by simp only [c]; split_ifs <;> norm_num
    simp only [mul_pow, hc, one_mul]; exact hv α
  · have hc : ∏ α, c α = -1 := by
      simp only [c]; rw [prod_ite_eq' univ α₀ (fun _ => (-1 : ℝ))]; simp
    simp only [Phi, prod_mul_distrib, hc, ← sum_neg_distrib]
    exact sum_congr rfl fun J _ => by ring

/-- Best rank-one approximation: for `k ≥ 1` and all `d α ≥ 1` there is `u* ∈ M` with
`Φ(u*) = σ_max` (`IsMaxOn`) and `‖T − σ_max u*⊗‖ ≤ ‖T − λ v⊗‖` for all `λ` and `v ∈ M`. -/
theorem best_rank_one (T : (∀ α : Fin k, Fin (d α)) → ℝ) (hk : 0 < k) (hd : ∀ α, 0 < d α) :
    ∃ u ∈ sphereProd d, IsMaxOn (Phi T) (sphereProd d) u ∧
      ∀ lam : ℝ, ∀ v ∈ sphereProd d,
        frobSq (fun J => T J - rankOne (Phi T u) u J) ≤ frobSq (fun J => T J - rankOne lam v J) := by
  obtain ⟨u, hu, hmax⟩ := exists_max T hd
  refine ⟨u, hu, hmax, fun lam v hv => ?_⟩
  rw [rank_one_identity T u hu, rank_one_identity T v hv]
  have h1 : Phi T v ≤ Phi T u := hmax hv
  obtain ⟨w, hw, hwv⟩ := flip_mem_neg T hk v hv
  have h2 : -Phi T v ≤ Phi T u := hwv ▸ hmax hw
  nlinarith [sq_nonneg (lam - Phi T v), sq_nonneg (Phi T u - Phi T v),
    sq_nonneg (Phi T u + Phi T v)]

/-! ## Witness: the matrix case `k = 2`, `d = (2, 2)`, `T = diag(1, 2)`.
At `u = (e₁, e₁)` (second basis vector, index `1`): `Φ = 2`, `∇_α Φ = 2 u^α` for both `α`, so
`multipliers_eq` forces `μ = (2, 2)`; at `u = (e₀, e₀)`, `Φ = 1 < 2`, so `σ_max ≥ 2` is not
attained everywhere: the maximization is not trivial. -/

/-- `T = diag(1, 2)` as an order-2 tensor. -/
def Tw : (∀ α : Fin 2, Fin ((fun _ => 2) α)) → ℝ :=
  fun J => if J 0 = J 1 then (J 0 : ℝ) + 1 else 0

/-- `u = (e_i, e_i)`. -/
def ue (i : Fin 2) : ∀ α : Fin 2, Fin ((fun _ => 2) α) → ℝ := fun _ j => if j = i then 1 else 0

/-- Sums over `∀ α : Fin 2, Fin 2` are double sums. -/
lemma sum_pi_two (f : (∀ α : Fin 2, Fin ((fun _ => 2) α)) → ℝ) :
    ∑ J, f J = ∑ a : Fin 2, ∑ b : Fin 2, f ![a, b] := by
  rw [← (Fin.consEquiv (fun _ : Fin 2 => Fin 2)).sum_comp]
  rw [Fintype.sum_prod_type]
  refine sum_congr rfl fun a _ => ?_
  rw [← (Fin.consEquiv (fun _ : Fin 1 => Fin 2)).sum_comp]
  rw [Fintype.sum_prod_type]
  simp only [Fintype.sum_unique]
  refine sum_congr rfl fun b _ => ?_
  congr 1

lemma erase_zero_two : (univ : Finset (Fin 2)).erase 0 = {1} := by decide
lemma erase_one_two : (univ : Finset (Fin 2)).erase 1 = {0} := by decide

lemma ue_mem (i : Fin 2) : ue i ∈ sphereProd (fun _ : Fin 2 => 2) := by
  intro α; fin_cases i <;> simp [ue]

example : Phi Tw (ue 1) = 2 := by
  rw [Phi, sum_pi_two]; simp [Tw, ue]; norm_num

example : Phi Tw (ue 0) = 1 := by
  rw [Phi, sum_pi_two]; simp [Tw, ue]

lemma grad_ue1 : ∀ α j, partialGrad Tw (ue 1) α j = 2 * ue 1 α j := by
  intro α j
  rw [partialGrad, sum_pi_two]
  fin_cases α <;> fin_cases j <;>
    simp [Tw, ue, erase_zero_two, erase_one_two] <;> norm_num

example : ∀ α, (fun _ : Fin 2 => (2 : ℝ)) α = Phi Tw (ue 1) :=
  multipliers_eq Tw (ue 1) (ue_mem 1) _ grad_ue1

/-- `best_rank_one` applies to the witness (`k = 2 ≥ 1`, `d = (2, 2)`); the optimal value is at
least `Φ(e₁, e₁) = 2`. -/
example : ∃ u ∈ sphereProd (fun _ : Fin 2 => 2), IsMaxOn (Phi Tw) (sphereProd _) u ∧
    2 ≤ Phi Tw u := by
  obtain ⟨u, hu, hmax, -⟩ := best_rank_one Tw (by norm_num) (fun _ => by norm_num)
  refine ⟨u, hu, hmax, ?_⟩
  have h2 : Phi Tw (ue 1) = 2 := by
    rw [Phi, sum_pi_two]; simp [Tw, ue]; norm_num
  exact h2 ▸ hmax (ue_mem 1)

/-! ## Mutants -/

/-- Mutant (drop `d α ≥ 1` in `exists_max`): with `k = 1`, `d = (0)` the set `M` is empty, so no
maximizer exists. -/
theorem exists_max_mutant_false :
    ¬ (∀ T : (∀ α : Fin 1, Fin ((fun _ => 0) α)) → ℝ,
        ∃ u ∈ sphereProd (fun _ : Fin 1 => 0), IsMaxOn (Phi T) (sphereProd _) u) := by
  intro h
  obtain ⟨u, hu, -⟩ := h (fun _ => 0)
  have := hu 0
  simp at this

/-- Mutant (drop `u ∈ M` in `multipliers_eq`): `u = 2(e₁, e₁)` gives `∇_α Φ = 4e₁ = 2·(2e₁)`
(`μ = 2`) while `Φ = 8`. -/
theorem multipliers_mutant_false :
    ¬ (∀ (u : ∀ α : Fin 2, Fin ((fun _ => 2) α) → ℝ) (μ : Fin 2 → ℝ),
        (∀ α j, partialGrad Tw u α j = μ α * u α j) → ∀ α, μ α = Phi Tw u) := by
  intro h
  have hg : ∀ α j, partialGrad Tw (fun α j => 2 * ue 1 α j) α j
      = (fun _ => (2 : ℝ)) α * (fun α j => 2 * ue 1 α j) α j := by
    intro α j
    rw [partialGrad, sum_pi_two]
    fin_cases α <;> fin_cases j <;>
      simp [Tw, ue, erase_zero_two, erase_one_two] <;> norm_num
  have := h _ _ hg 0
  rw [Phi, sum_pi_two] at this
  simp [Tw, ue] at this
  norm_num at this

/-- Mutant (drop `u ∈ M` in `rank_one_identity`): `T = 0`, `λ = 1`, `u = 2(e₁, e₁)` gives
`‖λu⊗‖² = 16 ≠ λ² = 1`. -/
theorem rank_one_mutant_false :
    ¬ (∀ (u : ∀ α : Fin 2, Fin ((fun _ => 2) α) → ℝ) (lam : ℝ),
        frobSq (d := fun _ : Fin 2 => 2) (fun J => (0 : ℝ) - rankOne lam u J)
          = frobSq (d := fun _ : Fin 2 => 2) (fun _ => (0 : ℝ))
            - 2 * lam * Phi (d := fun _ : Fin 2 => 2) (fun _ => 0) u + lam ^ 2) := by
  intro h
  have := h (fun α j => 2 * ue 1 α j) 1
  rw [frobSq, frobSq, sum_pi_two, sum_pi_two] at this
  simp [rankOne, ue, Phi, Fin.sum_univ_two] at this
  norm_num at this

end LeanReal.Chap01Tensor

#print axioms LeanReal.Chap01Tensor.continuous_Phi
#print axioms LeanReal.Chap01Tensor.isCompact_sphereProd
#print axioms LeanReal.Chap01Tensor.sphereProd_nonempty
#print axioms LeanReal.Chap01Tensor.exists_max
#print axioms LeanReal.Chap01Tensor.euler
#print axioms LeanReal.Chap01Tensor.multipliers_eq
#print axioms LeanReal.Chap01Tensor.rank_one_identity
#print axioms LeanReal.Chap01Tensor.best_rank_one
#print axioms LeanReal.Chap01Tensor.exists_max_mutant_false
#print axioms LeanReal.Chap01Tensor.multipliers_mutant_false
#print axioms LeanReal.Chap01Tensor.rank_one_mutant_false
