import LeanReal.Chap12ConstraintMatrix

-- MUTANTE M1_KK_3para2: K_ijK^ij <= 2k^2 (era 3)
namespace LeanReal.Chap12.Mutant
open Matrix LeanReal.Chap12

theorem m (K : Matrix (Fin 3) (Fin 3) ℝ) (hK : K.IsSymm) (κ R Λ G ρ : ℝ)
    (hb : IIBound K κ) (hH : HamiltonianConstraint K R Λ G ρ) :
    0 ≤ frobSq K ∧ frobSq K ≤ 2 * κ ^ 2 ∧
    0 ≤ frobSq (shear K) ∧ frobSq (shear K) ≤ 3 * κ ^ 2 - K.trace ^ 2 / 3 ∧
    2 * Λ + 16 * Real.pi * G * ρ - 6 * κ ^ 2 ≤ R ∧
    R ≤ 2 * Λ + 16 * Real.pi * G * ρ + 2 * κ ^ 2 := by
  have hH' : K.IsHermitian := isHermitian_iff_isSymm.mpr hK
  have hR := (hamiltonian_iff K R Λ G ρ).mp hH
  have hF := frobSq_eq_trace_mul hH'
  rw [trace_mul_self_eq hH', Fin.sum_univ_three] at hF
  have hT := trace_eq_sum hH'
  rw [Fin.sum_univ_three] at hT
  obtain ⟨-, b1, b2, b3⟩ := constraint_bounds (hH'.eigenvalues 0) (hH'.eigenvalues 1)
    (hH'.eigenvalues 2) κ (2 * Λ + 16 * Real.pi * G * ρ) (abs_eigenvalue_le hH' hb 0)
    (abs_eigenvalue_le hH' hb 1) (abs_eigenvalue_le hH' hb 2)
  have h0 : 0 ≤ frobSq (shear K) := by
    unfold frobSq; positivity
  rw [frobSq_shear] at h0 ⊢
  refine ⟨by unfold frobSq; positivity, by linarith, h0, by linarith, ?_, ?_⟩
  · rw [hF, hT] at hR; linarith
  · rw [hF, hT] at hR; linarith

end LeanReal.Chap12.Mutant

#print axioms LeanReal.Chap12.Mutant.m
