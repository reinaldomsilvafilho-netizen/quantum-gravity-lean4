import LeanReal.Chap12ConstraintMatrix

-- MUTANTE M5_autovalor_meio: |lambda_i| <= k/2 (era k)
namespace LeanReal.Chap12.Mutant
open Matrix LeanReal.Chap12

theorem m {K : Matrix (Fin 3) (Fin 3) ℝ} (hK : K.IsHermitian) {κ : ℝ}
    (hb : IIBound K κ) (i : Fin 3) : |hK.eigenvalues i| ≤ κ / 2 := by
  have hnorm : ‖hK.eigenvectorBasis i‖ = 1 := hK.eigenvectorBasis.orthonormal.1 i
  have hvv : (⇑(hK.eigenvectorBasis i) : Fin 3 → ℝ) ⬝ᵥ ⇑(hK.eigenvectorBasis i) = 1 := by
    have h := real_inner_self_eq_norm_sq (hK.eigenvectorBasis i)
    rw [EuclideanSpace.inner_eq_star_dotProduct, hnorm] at h
    simpa using h
  have h := hb ⇑(hK.eigenvectorBasis i)
  rw [hK.mulVec_eigenvectorBasis i, dotProduct_smul, hvv] at h
  simpa using h

end LeanReal.Chap12.Mutant

#print axioms LeanReal.Chap12.Mutant.m
