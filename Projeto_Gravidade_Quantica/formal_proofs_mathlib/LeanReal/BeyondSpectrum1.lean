import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Basic.Real.Basic

/-!
# *Beyond the Spectrum* I (Zenodo concept DOI 10.5281/zenodo.22644743) and Book Ch. 1

Theorem `thm:dirichlet_blindness` ("Spectral Blindness to Spatial Energy") appears in
`Manuscritos_Avulsos/paper_functional_realizations/paper_functional_realizations.tex`
(Sec. `subsec:sobolev`) and in Book Ch. 1 (`chap01_functional_realizations_matrices_tensors.tex`).

Paper:
> For every matrix `A ∈ ℝ^{n×n}`, the Dirichlet energy of the realization `f_A` is
> `𝓔(f_A) = ∑_{k₁,k₂=1}^n (k₁² + k₂²)|a_{k₁k₂}|² = ‖DA‖_F² + ‖AD‖_F²`, `D = diag(1,…,n)`.
> Moreover, for every `n ≥ 2` there exist a non-zero symmetric matrix `A` and permutation matrices
> `P₁, P₂` such that `A₁ = P₁AP₁ᵀ`, `A₂ = P₂AP₂ᵀ` satisfy `σ(A₁) = σ(A₂)`, `rank A₁ = rank A₂`,
> `‖A₁‖_F = ‖A₂‖_F = ‖A‖_F`, yet `𝓔(f_{A₂})/𝓔(f_{A₁}) = n²`. For every `A ≠ 0` and all permutation
> matrices `P₁, P₂` the ratio lies in `[n⁻², n²]`, so `n²` is the largest possible value.

Formal version.
* REDUCTION. The first equality `𝓔(f_A) = ∑(k₁²+k₂²)|a|²` is Parseval's identity on `𝕋²`
  (termwise differentiation of a trigonometric polynomial). It is NOT formalized: `energy A` is
  DEFINED as the coefficient sum. Everything after that equality is formalized.
* Indices are `Fin m`; the frequency of index `i` is `k = i + 1` (`freq`).
* `P A Pᵀ` for the permutation matrix of `σ` is `A.submatrix σ σ` (entry `(i,j)` is
  `a_{σ(i)σ(j)}`). "Same spectrum" is proved as equality of characteristic polynomials.
* `energy_eq_frob` : `𝓔 = ‖DA‖_F² + ‖AD‖_F²`.
* `energy_bounds` : `2‖A‖_F² ≤ 𝓔 ≤ 2m²‖A‖_F²`.
* `ratio_le` : `𝓔(A₂) ≤ m² 𝓔(A₁)` for all permutations (the ratio bound, in multiplied-out form,
  which needs no `A ≠ 0`).
* `blindness_sharp` : for every `m = n+1 ≥ 1`, `A = E₁₁` and the transposition `(1 m)` give
  `𝓔(A₂) = m² 𝓔(A₁)`, with `𝓔(A₁) = 2 ≠ 0`, equal characteristic polynomials, ranks and Frobenius
  norms; `A` is symmetric and non-zero. (The paper asks `n ≥ 2`; for `m = 1` the ratio is `1 = 1²`.)
-/

namespace LeanReal.BeyondSpectrum1

open Matrix Finset

variable {m : ℕ}

/-- Frequency `k = i + 1` of the index `i : Fin m`. -/
def freq (i : Fin m) : ℝ := (i : ℕ) + 1

/-- Squared Frobenius norm. -/
def frobSq (A : Matrix (Fin m) (Fin m) ℝ) : ℝ := ∑ i, ∑ j, A i j ^ 2

/-- Coefficient form of the Dirichlet energy, `∑ (k₁² + k₂²) a_{k₁k₂}²`. -/
def energy (A : Matrix (Fin m) (Fin m) ℝ) : ℝ := ∑ i, ∑ j, (freq i ^ 2 + freq j ^ 2) * A i j ^ 2

/-- `D = diag(1, …, m)`. -/
def Dm : Matrix (Fin m) (Fin m) ℝ := diagonal freq

lemma freq_pos (i : Fin m) : 1 ≤ freq i := by
  unfold freq; have : (0 : ℝ) ≤ (i : ℕ) := Nat.cast_nonneg _; linarith

lemma freq_le (i : Fin m) : freq i ≤ m := by
  unfold freq
  have : (i : ℕ) + 1 ≤ m := i.isLt
  exact_mod_cast this

/-- Eq. `dirichlet_energy_formula`, second equality: `𝓔 = ‖DA‖_F² + ‖AD‖_F²`. -/
theorem energy_eq_frob (A : Matrix (Fin m) (Fin m) ℝ) :
    energy A = frobSq (Dm * A) + frobSq (A * Dm) := by
  unfold energy frobSq Dm
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [diagonal_mul, mul_diagonal]
  ring

/-- `2‖A‖_F² ≤ 𝓔 ≤ 2m²‖A‖_F²`. -/
theorem energy_bounds (A : Matrix (Fin m) (Fin m) ℝ) :
    2 * frobSq A ≤ energy A ∧ energy A ≤ 2 * (m : ℝ) ^ 2 * frobSq A := by
  unfold energy frobSq
  rw [Finset.mul_sum, Finset.mul_sum]
  constructor
  · refine Finset.sum_le_sum fun i _ => ?_
    rw [Finset.mul_sum]
    refine Finset.sum_le_sum fun j _ => ?_
    have hi := freq_pos i; have hj := freq_pos j
    have : 2 ≤ freq i ^ 2 + freq j ^ 2 := by nlinarith
    nlinarith [sq_nonneg (A i j)]
  · refine Finset.sum_le_sum fun i _ => ?_
    rw [Finset.mul_sum]
    refine Finset.sum_le_sum fun j _ => ?_
    have hi := freq_pos i; have hj := freq_pos j
    have hi' := freq_le i; have hj' := freq_le j
    have : freq i ^ 2 + freq j ^ 2 ≤ 2 * (m : ℝ) ^ 2 := by nlinarith
    nlinarith [sq_nonneg (A i j)]

/-- Permutation conjugation preserves `‖A‖_F`. -/
theorem frobSq_perm (A : Matrix (Fin m) (Fin m) ℝ) (σ : Equiv.Perm (Fin m)) :
    frobSq (A.submatrix σ σ) = frobSq A := by
  unfold frobSq
  simp only [submatrix_apply]
  rw [← Equiv.sum_comp σ (fun i => ∑ j, A i j ^ 2)]
  refine Finset.sum_congr rfl fun i _ => ?_
  exact Equiv.sum_comp σ (fun j => A (σ i) j ^ 2)

/-- Permutation conjugation preserves the characteristic polynomial (hence the spectrum). -/
theorem charpoly_perm (A : Matrix (Fin m) (Fin m) ℝ) (σ : Equiv.Perm (Fin m)) :
    (A.submatrix σ σ).charpoly = A.charpoly := by
  have := charpoly_reindex σ.symm A
  rwa [reindex_apply, Equiv.symm_symm] at this

/-- Permutation conjugation preserves the rank. -/
theorem rank_perm (A : Matrix (Fin m) (Fin m) ℝ) (σ : Equiv.Perm (Fin m)) :
    (A.submatrix σ σ).rank = A.rank := by
  have := rank_reindex σ.symm σ.symm A
  rwa [reindex_apply, Equiv.symm_symm] at this

/-- The ratio bound: `𝓔(P₂AP₂ᵀ) ≤ m² 𝓔(P₁AP₁ᵀ)` for all permutations. -/
theorem ratio_le (A : Matrix (Fin m) (Fin m) ℝ) (σ τ : Equiv.Perm (Fin m)) :
    energy (A.submatrix τ τ) ≤ (m : ℝ) ^ 2 * energy (A.submatrix σ σ) := by
  have h1 := (energy_bounds (A.submatrix τ τ)).2
  have h2 := (energy_bounds (A.submatrix σ σ)).1
  rw [frobSq_perm] at h1 h2
  have : 0 ≤ (m : ℝ) ^ 2 := by positivity
  nlinarith

/-- Energy of a permuted matrix, reindexed. -/
lemma energy_perm (A : Matrix (Fin m) (Fin m) ℝ) (σ : Equiv.Perm (Fin m)) :
    energy (A.submatrix σ σ) =
      ∑ i, ∑ j, (freq (σ.symm i) ^ 2 + freq (σ.symm j) ^ 2) * A i j ^ 2 := by
  unfold energy
  simp only [submatrix_apply]
  rw [← Equiv.sum_comp σ.symm]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [← Equiv.sum_comp σ.symm]
  simp

lemma one_symm_apply (i : Fin m) : (Equiv.symm (1 : Equiv.Perm (Fin m))) i = i := rfl

lemma submatrix_one (A : Matrix (Fin m) (Fin m) ℝ) :
    A.submatrix (1 : Equiv.Perm (Fin m)) (1 : Equiv.Perm (Fin m)) = A := by
  ext i j; rfl

/-- `E₁₁`. -/
def E11 (n : ℕ) : Matrix (Fin (n + 1)) (Fin (n + 1)) ℝ := single 0 0 1

lemma energy_E11_perm (n : ℕ) (σ : Equiv.Perm (Fin (n + 1))) :
    energy ((E11 n).submatrix σ σ) = 2 * freq (σ.symm 0) ^ 2 := by
  rw [energy_perm]
  rw [Finset.sum_eq_single 0]
  · rw [Finset.sum_eq_single 0]
    · simp [E11]; ring
    · intro j _ hj; simp [E11, Ne.symm hj]
    · simp
  · intro i _ hi
    refine Finset.sum_eq_zero fun j _ => ?_
    simp [E11, Ne.symm hi]
  · simp

/-- Sharpness (`thm:dirichlet_blindness`, "Moreover" part), for `m = n + 1`. -/
theorem blindness_sharp (n : ℕ) :
    let A := E11 n
    let σ₁ : Equiv.Perm (Fin (n + 1)) := 1
    let σ₂ : Equiv.Perm (Fin (n + 1)) := Equiv.swap 0 (Fin.last n)
    A ≠ 0 ∧ Aᵀ = A ∧
    (A.submatrix σ₁ σ₁).charpoly = (A.submatrix σ₂ σ₂).charpoly ∧
    (A.submatrix σ₁ σ₁).rank = (A.submatrix σ₂ σ₂).rank ∧
    frobSq (A.submatrix σ₁ σ₁) = frobSq A ∧ frobSq (A.submatrix σ₂ σ₂) = frobSq A ∧
    energy (A.submatrix σ₁ σ₁) = 2 ∧
    energy (A.submatrix σ₂ σ₂) = ((n + 1 : ℕ) : ℝ) ^ 2 * energy (A.submatrix σ₁ σ₁) := by
  intro A σ₁ σ₂
  refine ⟨?_, ?_, ?_, ?_, frobSq_perm _ _, frobSq_perm _ _, ?_, ?_⟩
  · intro h
    have := congrFun (congrFun h 0) 0
    simp [A, E11] at this
  · ext i j; simp [A, E11, single_apply, and_comm, eq_comm]
  · rw [charpoly_perm, charpoly_perm]
  · rw [rank_perm, rank_perm]
  · rw [energy_E11_perm, show σ₁.symm 0 = 0 from rfl]; simp [freq]
  · rw [energy_E11_perm, energy_E11_perm, show σ₁.symm 0 = 0 from rfl]
    simp only [σ₂, Equiv.symm_swap, Equiv.swap_apply_left]
    simp [freq]
    ring

/-! Non-vacuity: `m = 3`; `A₂ = E₃₃` has energy `18 = 3² · 2`. -/
example : energy ((E11 2).submatrix (Equiv.swap 0 (Fin.last 2)) (Equiv.swap 0 (Fin.last 2))) = 18 := by
  rw [energy_E11_perm]; simp [freq]; norm_num

/-- Negative control: the constant `m²` in `ratio_le` cannot be lowered to `m² − 1`
(`m = 2`, `A = E₁₁`: `8 ≤ 3·2` is false). -/
theorem mutant_ratio :
    ¬ ∀ (A : Matrix (Fin 2) (Fin 2) ℝ) (σ τ : Equiv.Perm (Fin 2)),
      energy (A.submatrix τ τ) ≤ ((2 : ℝ) ^ 2 - 1) * energy (A.submatrix σ σ) := by
  intro h
  have := h (E11 1) 1 (Equiv.swap 0 (Fin.last 1))
  rw [energy_E11_perm, energy_E11_perm, one_symm_apply] at this
  simp [freq] at this
  norm_num at this

/-- Negative control: the energy is NOT invariant under permutation conjugation (this is the
content of "spectral blindness"); the mutated invariance statement is false. -/
theorem mutant_energy_invariant :
    ¬ ∀ (A : Matrix (Fin 2) (Fin 2) ℝ) (σ : Equiv.Perm (Fin 2)),
      energy (A.submatrix σ σ) = energy A := by
  intro h
  have h1 := h (E11 1) (Equiv.swap 0 (Fin.last 1))
  have h2 : energy (E11 1) =
      energy ((E11 1).submatrix (1 : Equiv.Perm (Fin 2)) (1 : Equiv.Perm (Fin 2))) := by
    rw [submatrix_one]
  rw [h2, energy_E11_perm, energy_E11_perm, one_symm_apply] at h1
  simp [freq] at h1
  norm_num at h1

end LeanReal.BeyondSpectrum1

#print axioms LeanReal.BeyondSpectrum1.energy_eq_frob
#print axioms LeanReal.BeyondSpectrum1.energy_bounds
#print axioms LeanReal.BeyondSpectrum1.frobSq_perm
#print axioms LeanReal.BeyondSpectrum1.charpoly_perm
#print axioms LeanReal.BeyondSpectrum1.rank_perm
#print axioms LeanReal.BeyondSpectrum1.ratio_le
#print axioms LeanReal.BeyondSpectrum1.blindness_sharp
#print axioms LeanReal.BeyondSpectrum1.mutant_ratio
#print axioms LeanReal.BeyondSpectrum1.mutant_energy_invariant
