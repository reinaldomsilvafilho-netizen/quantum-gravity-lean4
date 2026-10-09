import LeanReal.BeyondSpectrum1
import Mathlib.Algebra.Order.Rearrangement

/-!
# *Beyond the Spectrum* I (Zenodo concept DOI 10.5281/zenodo.22644743), item B2

Source: `Manuscritos_Avulsos/paper_functional_realizations/paper_functional_realizations.tex`,
Proposition `prop:optimal_permutation` ("Optimal permutation for the Dirichlet energy").

Paper:
> For `A ∈ ℝ^{n×n}`, define `w_i := ∑_{j=1}^n (a_{ij}² + a_{ji}²)` and let `τ ∈ S_n` be any
> permutation with `w_{τ(1)} ≥ w_{τ(2)} ≥ … ≥ w_{τ(n)}`. Then
> `min_π 𝓔(f_{P_π A P_πᵀ}) = min_π ∑_i π(i)² w_i = ∑_k k² w_{τ(k)}`, and `π = τ⁻¹` attains it.
> The minimum and a minimizer are computed in `O(n log n)` time by sorting `w`.

Formal version (definitions `freq`, `energy` reused from `LeanReal.BeyondSpectrum1`).
* REDUCTION (as in `BeyondSpectrum1`): `energy` is DEFINED as the coefficient sum
  `∑ (k₁² + k₂²) a²`; the Parseval step `𝓔(f_A) = ∑ (k₁²+k₂²)|a|²` is not formalized.
* Indices are `Fin n`, frequency `k = i + 1` (`freq`). `P_π A P_πᵀ` has entries
  `a_{π⁻¹(i)π⁻¹(j)}`, i.e. it is `A.submatrix σ σ` with `σ = π⁻¹`; we quantify over `σ`.
* `energy_perm_eq_weighted` : `𝓔(A.submatrix σ σ) = ∑_i freq(σ⁻¹ i)² w_i` (paper's first equality,
  with `π = σ⁻¹`).
* `optimal_permutation` : if `w ∘ τ` is antitone, then `∑_k k² w_{τ(k)} ≤ 𝓔(A.submatrix σ σ)` for
  every `σ`, with equality at `σ = τ` (i.e. `π = τ⁻¹`). This is the min statement.
* The `O(n log n)` complexity claim is NOT formalized.
-/

namespace LeanReal.BeyondSpectrum1B2

open Finset LeanReal.BeyondSpectrum1

variable {n : ℕ}

/-- `w_i = ∑_j (a_{ij}² + a_{ji}²)`. -/
def weight (A : Matrix (Fin n) (Fin n) ℝ) (i : Fin n) : ℝ := ∑ j, (A i j ^ 2 + A j i ^ 2)

/-- Paper's first equality: `𝓔(P A Pᵀ) = ∑_i π(i)² w_i` with `π = σ⁻¹`. -/
theorem energy_perm_eq_weighted (A : Matrix (Fin n) (Fin n) ℝ) (σ : Equiv.Perm (Fin n)) :
    energy (A.submatrix σ σ) = ∑ i, freq (σ.symm i) ^ 2 * weight A i := by
  rw [energy_perm]
  simp only [weight, add_mul, mul_add, Finset.sum_add_distrib, Finset.mul_sum]
  congr 1
  exact Finset.sum_comm

/-- `freq` is strictly monotone, hence so is `freq ^ 2`. -/
lemma freq_sq_strictMono : StrictMono (fun i : Fin n => freq i ^ 2) := by
  intro i j hij
  have h1 : freq i < freq j := by
    unfold freq
    have : (i : ℕ) < j := hij
    exact_mod_cast Nat.add_lt_add_right this 1
  have h0 : 0 ≤ freq i := le_trans zero_le_one (freq_pos i)
  exact pow_lt_pow_left₀ h1 h0 two_ne_zero

/-- **Prop. `prop:optimal_permutation`.** If `w_{τ(1)} ≥ … ≥ w_{τ(n)}`, then for every permutation
the energy is at least `∑_k k² w_{τ(k)}`, and the value is attained at `σ = τ` (`π = τ⁻¹`). -/
theorem optimal_permutation (A : Matrix (Fin n) (Fin n) ℝ) (τ : Equiv.Perm (Fin n))
    (hτ : Antitone (fun k => weight A (τ k))) :
    (∀ σ : Equiv.Perm (Fin n),
        ∑ k, freq k ^ 2 * weight A (τ k) ≤ energy (A.submatrix σ σ)) ∧
      energy (A.submatrix τ τ) = ∑ k, freq k ^ 2 * weight A (τ k) := by
  have hanti : Antivary (fun k : Fin n => freq k ^ 2) (fun k => weight A (τ k)) := by
    intro i j hij
    have hji : j < i := by
      by_contra h
      exact absurd (hτ (not_lt.mp h)) (not_le.mpr hij)
    exact (freq_sq_strictMono hji).le
  have hτeq : energy (A.submatrix τ τ) = ∑ k, freq k ^ 2 * weight A (τ k) := by
    rw [energy_perm_eq_weighted,
      ← Equiv.sum_comp τ (fun i => freq (τ.symm i) ^ 2 * weight A i)]
    simp
  refine ⟨fun σ => ?_, hτeq⟩
  rw [energy_perm_eq_weighted,
    ← Equiv.sum_comp τ (fun i => freq (σ.symm i) ^ 2 * weight A i)]
  have := hanti.sum_smul_le_sum_comp_perm_smul (σ := σ.symm * τ)
  simpa [smul_eq_mul, Equiv.Perm.mul_apply] using this

#print axioms energy_perm_eq_weighted
#print axioms optimal_permutation

/-! ### Non-vacuity witness
`n = 2`, `A = E₁₁ = !![1,0;0,0]`: `w = (2, 0)`, `τ = id` is a valid sorting permutation and the
minimum `1²·2 + 2²·0 = 2` equals `𝓔(A)`. -/
example : Antitone (fun k : Fin 2 => weight !![(1 : ℝ), 0; 0, 0] ((1 : Equiv.Perm (Fin 2)) k)) ∧
    ∑ k : Fin 2, freq k ^ 2 * weight !![(1 : ℝ), 0; 0, 0] ((1 : Equiv.Perm (Fin 2)) k) = 2 := by
  refine ⟨?_, ?_⟩
  · intro i j hij
    fin_cases i <;> fin_cases j <;> simp_all [weight, Fin.sum_univ_two]
  · simp [weight, freq, Fin.sum_univ_two]; norm_num

/-! ### Mutant proved false
Mutant: sorting `w` in INCREASING order (`w ∘ τ` monotone) gives a lower bound.
Counterexample: `n = 2`, `A = E₁₁`, `τ = swap 0 1` (`w ∘ τ = (0, 2)`, monotone):
`∑_k k² w_{τ(k)} = 8 > 2 = 𝓔(A)` (take `σ = id`). -/
theorem mutant_increasing_false :
    ¬ ∀ (A : Matrix (Fin 2) (Fin 2) ℝ) (τ : Equiv.Perm (Fin 2)),
      Monotone (fun k => weight A (τ k)) → ∀ σ : Equiv.Perm (Fin 2),
        ∑ k, freq k ^ 2 * weight A (τ k) ≤ energy (A.submatrix σ σ) := by
  intro h
  have hm : Monotone (fun k => weight !![(1 : ℝ), 0; 0, 0] (Equiv.swap (0 : Fin 2) 1 k)) := by
    intro i j hij
    fin_cases i <;> fin_cases j <;> simp_all [weight, Fin.sum_univ_two]
  have := h _ _ hm 1
  simp [weight, freq, energy, Fin.sum_univ_two] at this
  norm_num at this

#print axioms mutant_increasing_false

end LeanReal.BeyondSpectrum1B2
