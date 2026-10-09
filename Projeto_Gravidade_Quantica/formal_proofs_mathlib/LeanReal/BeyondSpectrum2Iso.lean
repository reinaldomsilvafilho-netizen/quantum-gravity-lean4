import Mathlib.LinearAlgebra.Matrix.Charpoly.Eigs
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt

/-!
# *Beyond the Spectrum* II (vol. 2 of Zenodo concept DOI 10.5281/zenodo.22644743), item G1

Source: `Manuscritos_Avulsos/paper_geometric_measures_functional_tensors/paper_geometric_measures_functional_tensors.tex`,
Theorem `thm:isospectral_separation`, part (a), first sentence:
> Let `B` be the `3 × 3` matrix with `B₂₂ = 0` and all other entries `2`, let `P` be the
> permutation matrix exchanging the indices `1` and `2`, and let `A = PBPᵀ`. Then `A` and `B` are
> symmetric and isospectral, `σ(A) = σ(B) = {2 + 2√3, 2 − 2√3, 0}`, and [persistence diagrams].

Formal version (indices are 0-based in Lean: the paper's index 2 is `1`, the swap of 1 and 2 is
the swap of `0` and `1`).
* `A_eq`: `P B Pᵀ` equals the explicit matrix with `A₁₁ = 0` (paper indexing), others `2`.
* `P_orth`: `P Pᵀ = 1`.  `B_symm`, `A_symm`: symmetry.
* `charpoly_B`, `charpoly_A`: both characteristic polynomials equal `X³ − 4X² − 8X`.
* `spectrum_B`, `spectrum_A`: `spectrum ℝ · = {2 + 2√3, 2 − 2√3, 0}` (Mathlib's `spectrum` of the
  matrix in the algebra `Matrix (Fin 3) (Fin 3) ℝ`; the three values are distinct, so each is a
  simple root of the cubic).
* NOT covered: the step realisation `Φ_□`, persistence diagrams `Dgm₁`, persistent entropy, the
  homological lemma, and all of part (b). Mathlib has no persistent homology.
-/

namespace LeanReal.BeyondSpectrum2Iso

open Matrix Polynomial

/-- `B`: `B₂₂ = 0` (paper indexing), all other entries `2`. -/
def B : Matrix (Fin 3) (Fin 3) ℝ := !![2, 2, 2; 2, 0, 2; 2, 2, 2]

/-- Permutation matrix exchanging the first two indices. -/
def P : Matrix (Fin 3) (Fin 3) ℝ := !![0, 1, 0; 1, 0, 0; 0, 0, 1]

/-- `A = P B Pᵀ`. -/
def A : Matrix (Fin 3) (Fin 3) ℝ := P * B * Pᵀ

theorem A_eq : A = !![0, 2, 2; 2, 2, 2; 2, 2, 2] := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [A, P, B, mul_apply, Fin.sum_univ_three, transpose_apply]

theorem P_orth : P * Pᵀ = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [P, mul_apply, Fin.sum_univ_three, transpose_apply, one_apply]

theorem B_symm : Bᵀ = B := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [B, transpose_apply]

theorem A_symm : Aᵀ = A := by
  rw [A_eq]; ext i j; fin_cases i <;> fin_cases j <;> simp [transpose_apply]

theorem charpoly_B : B.charpoly = X ^ 3 - 4 * X ^ 2 - 8 * X := by
  rw [charpoly, det_fin_three]
  simp [B]
  simp only [map_ofNat]
  ring

theorem charpoly_A : A.charpoly = X ^ 3 - 4 * X ^ 2 - 8 * X := by
  rw [A_eq, charpoly, det_fin_three]
  simp
  simp only [map_ofNat]
  ring

lemma roots_cubic (μ : ℝ) :
    (X ^ 3 - 4 * X ^ 2 - 8 * X : ℝ[X]).IsRoot μ ↔
      μ = 2 + 2 * √3 ∨ μ = 2 - 2 * √3 ∨ μ = 0 := by
  have h3 : √3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hfac : μ ^ 3 - 4 * μ ^ 2 - 8 * μ = μ * (μ - (2 + 2 * √3)) * (μ - (2 - 2 * √3)) := by
    ring_nf; rw [h3]; ring
  simp only [IsRoot, eval_sub, eval_pow, eval_X, eval_mul, eval_ofNat]
  rw [hfac]
  constructor
  · intro h
    rcases mul_eq_zero.mp h with h | h
    · rcases mul_eq_zero.mp h with h | h
      · exact Or.inr (Or.inr h)
      · exact Or.inl (by linarith)
    · exact Or.inr (Or.inl (by linarith))
  · rintro (h | h | h) <;> rw [h] <;> ring

theorem spectrum_B : spectrum ℝ B = {2 + 2 * √3, 2 - 2 * √3, 0} := by
  ext μ
  rw [mem_spectrum_iff_isRoot_charpoly, charpoly_B, roots_cubic]
  simp

theorem spectrum_A : spectrum ℝ A = {2 + 2 * √3, 2 - 2 * √3, 0} := by
  ext μ
  rw [mem_spectrum_iff_isRoot_charpoly, charpoly_A, roots_cubic]
  simp

theorem isospectral : spectrum ℝ A = spectrum ℝ B := by rw [spectrum_A, spectrum_B]

/-! ## Non-vacuity: the pair is not trivial (`A ≠ B`), and `0` has the explicit eigenvector
`(1, 0, −1)` for `B`. -/

example : A ≠ B := by
  rw [A_eq]; intro h
  have := congrFun (congrFun h 0) 0
  simp [B] at this

example : B *ᵥ ![1, 0, -1] = 0 := by
  ext i; fin_cases i <;> simp [B, mulVec, dotProduct, Fin.sum_univ_three]

/-! ## Mutant: replace the eigenvalue `0` by `2`. False, because `0 ∈ σ(B)` and `0` is not in
the mutated set (`2 ± 2√3 ≠ 0` since `√3 ≠ 1`). -/

theorem spectrum_mutant_false : ¬ (spectrum ℝ B = {2 + 2 * √3, 2 - 2 * √3, 2}) := by
  intro h
  have h0 : (0 : ℝ) ∈ spectrum ℝ B := by rw [spectrum_B]; simp
  rw [h] at h0
  have h3 : √3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < √3 := Real.sqrt_pos.mpr (by norm_num)
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at h0
  rcases h0 with h0 | h0 | h0
  · linarith
  · nlinarith
  · norm_num at h0

end LeanReal.BeyondSpectrum2Iso

#print axioms LeanReal.BeyondSpectrum2Iso.A_eq
#print axioms LeanReal.BeyondSpectrum2Iso.P_orth
#print axioms LeanReal.BeyondSpectrum2Iso.A_symm
#print axioms LeanReal.BeyondSpectrum2Iso.B_symm
#print axioms LeanReal.BeyondSpectrum2Iso.charpoly_A
#print axioms LeanReal.BeyondSpectrum2Iso.charpoly_B
#print axioms LeanReal.BeyondSpectrum2Iso.spectrum_A
#print axioms LeanReal.BeyondSpectrum2Iso.spectrum_B
#print axioms LeanReal.BeyondSpectrum2Iso.isospectral
#print axioms LeanReal.BeyondSpectrum2Iso.spectrum_mutant_false
