import LeanReal.BeyondSpectrum3_T2
import LeanReal.YangMills_Y4a

/-!
# L2 review of rounds 4A/4B: extra non-vacuity witnesses

Written by the independent layer-2 reviewer (not by the authors of the reviewed modules).

1. `BeyondSpectrum3_T2`: the hypothesis `SSA ι ι κ` of `reflected_ge_mutualInfo_of_SSA` is
   satisfiable. It is PROVED here for `ι = Fin 1`, `κ = Fin 2` (the dimensions of the module's
   witness `rho0`), where SSA holds with equality by reindexing, and the conditional theorem is
   then applied to `rho0`. (SSA in general is the Lieb–Ruskai theorem, which is true, so the
   hypothesis is never vacuous; it is simply not proved in Lean beyond this trivial case.)
2. `YangMills_Y4a`: the module's witness `witness_omega` has `L ≡ 0` (`G_N = span{(sin,0,0)}`
   gives `f_{0b0} = 0`), so its `Ω` is all of `ℝ`. Here `G_N = span{(cos,0,0), (0,0,sin)}`,
   `V_N = span{A1}` gives `M_N(x A1) = [[π, −xπ], [−xπ, π]]`: `0 ∈ Ω` and `2 ∉ Ω`, so `Ω` is a
   PROPER subset and the linear part `L` is non-zero.
-/

namespace LeanReal.L2Rodada4Extra

open Matrix

section T2

open LeanReal.BeyondSpectrum3T2

/-- SSA holds (with equality) on `(Fin 1 × Fin 1) × Fin 2`. -/
theorem SSA_fin1_fin1_fin2 : SSA (Fin 1) (Fin 1) (Fin 2) := by
  intro τ _
  have hA : trMid τ = reindex
      (Equiv.prodCongr (Equiv.prodUnique (Fin 1) (Fin 1)) (Equiv.refl (Fin 2)))
      (Equiv.prodCongr (Equiv.prodUnique (Fin 1) (Fin 1)) (Equiv.refl (Fin 2))) τ := by
    ext x y
    simp only [trMid, reindex_apply, submatrix_apply, Fin.sum_univ_one]
    rfl
  have hB : ptr2 (ptr2 τ) = reindex (Equiv.prodUnique (Fin 1) (Fin 1))
      (Equiv.prodUnique (Fin 1) (Fin 1)) (ptr2 τ) := by
    ext i j
    simp [ptr2, reindex_apply, Fin.default_eq_zero]
  rw [hA, hB, vnS_reindex, vnS_reindex]
  linarith

/-- The conditional bound applied at the module's witness, with its hypothesis discharged. -/
theorem bound_at_rho0 : mutualInfo rho0 ≤ SR rho0 :=
  reflected_ge_mutualInfo_of_SSA SSA_fin1_fin1_fin2 rho0_isDensity

end T2

section Y4a

open LeanReal.YangMillsY4a Real

/-- `G_N = span{(cos,0,0), (0,0,sin)}`. -/
noncomputable def e2 : Fin 2 → Fld 3 CircleFun := ![ψ1, χ1]

lemma T_A1_00 : T (fun _ : Fin 1 => dθ) Icirc eps A1 ψ1 ψ1 = 0 := by
  simp [T, Fin.sum_univ_three, ψ1, A1, eps]

lemma T_A1_11 : T (fun _ : Fin 1 => dθ) Icirc eps A1 χ1 χ1 = 0 := by
  simp [T, Fin.sum_univ_three, χ1, A1, eps]

lemma T_A1_01 : T (fun _ : Fin 1 => dθ) Icirc eps A1 ψ1 χ1 = -π :=
  witness_circle.2.2.2

lemma T_A1_10 : T (fun _ : Fin 1 => dθ) Icirc eps A1 χ1 ψ1 = -π := by
  obtain ⟨h1, h2, h3, h4⟩ := witness_circle
  rw [← T_symm _ _ _ h1 h2 h3, h4]

lemma dir_00 : ∑ μ : Fin 1, ∑ a : Fin 3,
    Icirc ((fun _ : Fin 1 => dθ) μ (ψ1 a) * (fun _ : Fin 1 => dθ) μ (ψ1 a)) = π := by
  simp [Fin.sum_univ_three, ψ1, dθ_cos]
  convert Icirc_sin_sin using 2
  ring

lemma dir_11 : ∑ μ : Fin 1, ∑ a : Fin 3,
    Icirc ((fun _ : Fin 1 => dθ) μ (χ1 a) * (fun _ : Fin 1 => dθ) μ (χ1 a)) = π := by
  simp [Fin.sum_univ_three, χ1, dθ_sin]
  exact Icirc_cos_cos

lemma dir_01 : ∑ μ : Fin 1, ∑ a : Fin 3,
    Icirc ((fun _ : Fin 1 => dθ) μ (ψ1 a) * (fun _ : Fin 1 => dθ) μ (χ1 a)) = 0 := by
  simp [Fin.sum_univ_three, ψ1, χ1]

lemma dir_10 : ∑ μ : Fin 1, ∑ a : Fin 3,
    Icirc ((fun _ : Fin 1 => dθ) μ (χ1 a) * (fun _ : Fin 1 => dθ) μ (ψ1 a)) = 0 := by
  simp [Fin.sum_univ_three, ψ1, χ1]

lemma ι1_apply (x : ℝ) : ι1 x = x • A1 := by
  simp [ι1]

/-- `M_N(x A1) = [[π, −xπ], [−xπ, π]]`. -/
theorem MN_e2 (x : ℝ) :
    MN (fun _ : Fin 1 => dθ) Icirc eps 1 e2 (ι1 x) = !![π, -(x * π); -(x * π), π] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp only [MN, Q, of_apply, ι1_apply, T_smul, e2, Matrix.cons_val_zero, Matrix.cons_val_one,
      Fin.zero_eta, Fin.mk_one, Matrix.cons_val', Matrix.empty_val', Matrix.cons_val_fin_one,
      dir_00, dir_11, dir_01, dir_10, T_A1_00, T_A1_11, T_A1_01, T_A1_10] <;>
    ring

/-- Non-trivial `Ω`: `0 ∈ Ω`, `2 ∉ Ω` (so `L ≠ 0` and `Ω ≠ ℝ`). -/
theorem omega_proper :
    (0 : ℝ) ∈ Omega (fun _ : Fin 1 => dθ) Icirc eps 1 e2 ι1 ∧
      (2 : ℝ) ∉ Omega (fun _ : Fin 1 => dθ) Icirc eps 1 e2 ι1 := by
  refine ⟨?_, ?_⟩
  · show (MN (fun _ : Fin 1 => dθ) Icirc eps 1 e2 (ι1 0)).PosDef
    rw [MN_e2]
    have : (!![π, -(0 * π); -(0 * π), π] : Matrix (Fin 2) (Fin 2) ℝ) = π • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
      ext i j; fin_cases i <;> fin_cases j <;> simp
    rw [this]
    exact PosDef.one.smul pi_pos
  · intro h
    change (MN (fun _ : Fin 1 => dθ) Icirc eps 1 e2 (ι1 2)).PosDef at h
    rw [MN_e2] at h
    have hv : 0 < star (![1, 1] : Fin 2 → ℝ) ⬝ᵥ
        ((!![π, -(2 * π); -(2 * π), π] : Matrix (Fin 2) (Fin 2) ℝ) *ᵥ ![1, 1]) :=
      (posDef_iff_dotProduct_mulVec.mp h).2 (by
      intro h0
      have := congrFun h0 0
      simp at this)
    simp [dotProduct, mulVec, Fin.sum_univ_two] at hv
    nlinarith [pi_pos]

end Y4a

end LeanReal.L2Rodada4Extra

#print axioms LeanReal.L2Rodada4Extra.SSA_fin1_fin1_fin2
#print axioms LeanReal.L2Rodada4Extra.bound_at_rho0
#print axioms LeanReal.L2Rodada4Extra.MN_e2
#print axioms LeanReal.L2Rodada4Extra.omega_proper
