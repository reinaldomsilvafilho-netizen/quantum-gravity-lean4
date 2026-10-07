import LeanReal.Chap12ConstraintMatrix

-- MUTANTE M8_sharp_6para5: diag(k,k,k) atinge R = s - 5k^2 (era 6)
namespace LeanReal.Chap12.Mutant
open Matrix LeanReal.Chap12

theorem m (κ Λ G ρ : ℝ) (hκ : 0 ≤ κ) :
    HamiltonianConstraint (diagonal ![κ, κ, κ])
      (2 * Λ + 16 * Real.pi * G * ρ - 5 * κ ^ 2) Λ G ρ := by
  rw [hamiltonian_iff]; simp [frobSq, Matrix.trace, Fin.sum_univ_three, diagonal_apply]; ring

end LeanReal.Chap12.Mutant

#print axioms LeanReal.Chap12.Mutant.m
