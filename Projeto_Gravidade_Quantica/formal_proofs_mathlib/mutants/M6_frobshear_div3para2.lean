import LeanReal.Chap12ConstraintMatrix

-- MUTANTE M6_frobshear_div3para2: sigma.sigma = KK - K^2/2 (era /3)
namespace LeanReal.Chap12.Mutant
open Matrix LeanReal.Chap12

theorem m (K : Matrix (Fin 3) (Fin 3) ℝ) :
    frobSq (shear K) = frobSq K - K.trace ^ 2 / 2 := by
  simp only [frobSq, shear, Matrix.trace, Matrix.diag, Fin.sum_univ_three, Matrix.sub_apply,
    Matrix.smul_apply, Matrix.one_apply, smul_eq_mul]
  simp
  ring

end LeanReal.Chap12.Mutant

#print axioms LeanReal.Chap12.Mutant.m
