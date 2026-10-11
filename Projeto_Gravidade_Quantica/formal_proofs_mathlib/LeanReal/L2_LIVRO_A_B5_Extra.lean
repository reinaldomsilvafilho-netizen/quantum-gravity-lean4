import LeanReal.Chap02PathIntegral

/-!
# L2 do lote LIVRO_A_B5: testemunha nao comutativa para `trace_holonomy_gauge_invariant`

Revisao L2 de `LeanReal.Chap02PathIntegral`. As testemunhas do modulo revisado sao todas
escalares (`𝔸 = ℝ`), de modo que o termo de conjugacao `Ω⁻¹𝒜Ω` coincide com `𝒜` e so o termo
`−Ω⁻¹Ω'` e exercitado. Aqui a forma matricial e instanciada em `ℂ^{2×2}` com dados que nao
comutam: `𝒜 ≡ N = [[0,1],[0,0]]` (`N² = 0`), `Ω ≡ P = [[1,0],[1,1]]` (constante, logo periodica),
`U(s) = 1 + sN`, `W(s) = 1 + sN'` com `N' = P⁻¹NP = [[1,1],[−1,−1]]`. Entao `Ω⁻¹𝒜Ω ≠ 𝒜`,
`W(1) ≠ U(1)` (a holonomia muda), mas `Tr W(1) = Tr U(1) = 2`, como o teorema preve.
Nenhuma lacuna de prova; so os axiomas padrao.
-/

noncomputable section

namespace LeanReal.L2_LIVRO_A_B5_Extra

open Set LeanReal.Chap02PathIntegral

attribute [local instance] Matrix.linftyOpNormedRing Matrix.linftyOpNormedAlgebra

/-- `M2 = ℂ^{2×2}`. -/
abbrev M2 := Matrix (Fin 2) (Fin 2) ℂ

/-- The nilpotent potential `N = [[0,1],[0,0]]`. -/
def N : M2 := !![0, 1; 0, 0]
/-- The constant gauge `P = [[1,0],[1,1]]`. -/
def P : M2 := !![1, 0; 1, 1]
/-- `Q = P⁻¹ = [[1,0],[−1,1]]`. -/
def Q : M2 := !![1, 0; -1, 1]
/-- `N' = P⁻¹NP = [[1,1],[−1,−1]]`. -/
def N' : M2 := !![1, 1; -1, -1]

lemma N_sq : N * N = 0 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [N, Matrix.mul_apply, Fin.sum_univ_two]

lemma N'_sq : N' * N' = 0 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [N', Matrix.mul_apply, Fin.sum_univ_two]

lemma Q_mul_P : Q * P = 1 := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [Q, P, Matrix.mul_apply, Fin.sum_univ_two]

lemma P_inv : P⁻¹ = Q := Matrix.inv_eq_left_inv Q_mul_P

lemma QNP : Q * N * P = N' := by
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [Q, N, P, N', Matrix.mul_apply, Fin.sum_univ_two]

lemma det_P : P.det = 1 := by simp [P, Matrix.det_fin_two_of]

/-- Derivative of the affine path `s ↦ 1 + s•X` in `M2`. -/
lemma hasDerivAt_affine (X : M2) (s : ℝ) :
    HasDerivAt (fun t : ℝ => (1 : M2) + t • X) X s := by
  have h : HasDerivAt (fun t : ℝ => t • X) ((1 : ℝ) • X) s := (hasDerivAt_id' s).smul_const X
  rw [one_smul] at h
  exact h.const_add (1 : M2)

/-- **Non-commutative witness** for `trace_holonomy_gauge_invariant`: all hypotheses hold for
`𝒜 ≡ N`, `Ω ≡ P`, `U = 1 + sN`, `W = 1 + sN'`; the conjugation is non-trivial
(`P⁻¹NP ≠ N`), the holonomy changes (`W(1) ≠ U(1)`) and the traces agree. -/
theorem witness_matrix :
    let A : ℝ → M2 := fun _ => N
    let Ω : ℝ → M2 := fun _ => P
    let Ω' : ℝ → M2 := fun _ => 0
    let U : ℝ → M2 := fun s => 1 + s • N
    let W : ℝ → M2 := fun s => 1 + s • N'
    ContinuousOn A (Icc 0 1) ∧
    (∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt Ω (Ω' s) (Icc 0 1) s) ∧
    (∀ s ∈ Icc (0 : ℝ) 1, IsUnit (Ω s).det) ∧ Ω 0 = Ω 1 ∧
    (∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt U (A s * U s) (Icc 0 1) s) ∧ U 0 = 1 ∧
    (∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt W
      (((Ω s)⁻¹ * A s * Ω s - (Ω s)⁻¹ * Ω' s) * W s) (Icc 0 1) s) ∧ W 0 = 1 ∧
    (Ω 0)⁻¹ * A 0 * Ω 0 ≠ A 0 ∧ W 1 ≠ U 1 ∧ Matrix.trace (W 1) = Matrix.trace (U 1) := by
  intro A Ω Ω' U W
  refine ⟨continuousOn_const, fun s _ => (hasDerivWithinAt_const _ _ _), ?_, rfl, ?_, by simp [U],
    ?_, by simp [W], ?_, ?_, ?_⟩
  · intro s _; simp only [Ω, det_P]; exact isUnit_one
  · intro s _
    refine (hasDerivAt_affine N s).hasDerivWithinAt.congr_deriv ?_
    simp only [A, U, mul_add, mul_one, mul_smul_comm, N_sq, smul_zero, add_zero]
  · intro s _
    refine (hasDerivAt_affine N' s).hasDerivWithinAt.congr_deriv ?_
    simp only [A, Ω, Ω', W, P_inv, QNP, mul_zero, sub_zero, mul_add, mul_one, mul_smul_comm,
      N'_sq, smul_zero, add_zero]
  · simp only [Ω, A, P_inv, QNP]
    intro h
    have := congrFun (congrFun h 0) 0
    simp [N', N] at this
  · simp only [W, U, one_smul]
    intro h
    have := congrFun (congrFun h 0) 0
    simp [N', N] at this
  · simp only [W, U, one_smul, Matrix.trace, Matrix.diag, Fin.sum_univ_two, N, N']
    norm_num

/-- The conclusion of `trace_holonomy_gauge_invariant` on these data, checked directly:
`W(1) = P⁻¹ U(1) P` and `Tr W(1) = Tr U(1)`. -/
theorem matrix_instance :
    (1 : M2) + (1 : ℝ) • N' = P⁻¹ * ((1 : M2) + (1 : ℝ) • N) * P ∧
      Matrix.trace ((1 : M2) + (1 : ℝ) • N') = Matrix.trace ((1 : M2) + (1 : ℝ) • N) := by
  obtain ⟨hA, hΩ, hΩu, hper, hU, hU0, hW, hW0, -, -, -⟩ := witness_matrix
  exact trace_holonomy_gauge_invariant _ _ _ _ _ hA hΩ hΩu hper hU hU0 hW hW0

end LeanReal.L2_LIVRO_A_B5_Extra

#print axioms LeanReal.L2_LIVRO_A_B5_Extra.witness_matrix
#print axioms LeanReal.L2_LIVRO_A_B5_Extra.matrix_instance
