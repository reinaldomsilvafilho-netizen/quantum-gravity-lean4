import LeanReal.Chap12ConstraintMatrix

-- MUTANTE M7_traco_sem_quadrado: tr(KK) = sum lambda_i (era lambda_i^2)
namespace LeanReal.Chap12.Mutant
open Matrix LeanReal.Chap12

theorem m {K : Matrix (Fin 3) (Fin 3) ℝ} (hK : K.IsHermitian) :
    (K * K).trace = ∑ i, hK.eigenvalues i := by
  have hs := hK.spectral_theorem
  rw [Unitary.conjStarAlgAut_apply] at hs
  have hU : (star hK.eigenvectorUnitary : Matrix (Fin 3) (Fin 3) ℝ) * hK.eigenvectorUnitary = 1 :=
    Unitary.coe_star_mul_self _
  generalize (star hK.eigenvectorUnitary : Matrix (Fin 3) (Fin 3) ℝ) = V at hs hU
  generalize (hK.eigenvectorUnitary : Matrix (Fin 3) (Fin 3) ℝ) = U at hs hU
  have h2 : K * K = U * diagonal (RCLike.ofReal ∘ hK.eigenvalues) * V *
      (U * diagonal (RCLike.ofReal ∘ hK.eigenvalues) * V) := congrArg₂ (· * ·) hs hs
  rw [h2]
  have h3 : U * diagonal (RCLike.ofReal ∘ hK.eigenvalues) * V *
      (U * diagonal (RCLike.ofReal ∘ hK.eigenvalues) * V) =
      U * (diagonal (RCLike.ofReal ∘ hK.eigenvalues) * (V * U) *
        diagonal (RCLike.ofReal ∘ hK.eigenvalues)) * V := by
    simp only [Matrix.mul_assoc]
  rw [h3, hU, Matrix.mul_one, trace_mul_cycle, hU, Matrix.one_mul, diagonal_mul_diagonal,
    trace_diagonal]
  simp [sq]

end LeanReal.Chap12.Mutant

#print axioms LeanReal.Chap12.Mutant.m
