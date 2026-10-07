"""Gera os mutantes (controle negativo) de LeanReal/Chap12ConstraintMatrix.lean.

Cada mutante reenuncia um teorema com UMA constante alterada e reusa a prova original.
Todo mutante e matematicamente falso; deve falhar ao compilar (erro + sorryAx).
Rodar cada arquivo com o mesmo `lean` + LEAN_PATH de `verificar.sh`, acrescentando
`.olean_local` (onde ficam os .olean de LeanReal.Chap12Constraint e ...Matrix).
"""
from pathlib import Path

HEAD = """import LeanReal.Chap12ConstraintMatrix

-- MUTANTE {nome}: {desc}
namespace LeanReal.Chap12.Mutant
open Matrix LeanReal.Chap12
"""
TAIL = "\nend LeanReal.Chap12.Mutant\n\n#print axioms LeanReal.Chap12.Mutant.m\n"

MAIN_PROOF = """  have hH' : K.IsHermitian := isHermitian_iff_isSymm.mpr hK
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
"""

def main_stmt(kk="3", sh="3 * κ ^ 2 - K.trace ^ 2 / 3", lo="6", hi="2"):
    return f"""theorem m (K : Matrix (Fin 3) (Fin 3) ℝ) (hK : K.IsSymm) (κ R Λ G ρ : ℝ)
    (hb : IIBound K κ) (hH : HamiltonianConstraint K R Λ G ρ) :
    0 ≤ frobSq K ∧ frobSq K ≤ {kk} * κ ^ 2 ∧
    0 ≤ frobSq (shear K) ∧ frobSq (shear K) ≤ {sh} ∧
    2 * Λ + 16 * Real.pi * G * ρ - {lo} * κ ^ 2 ≤ R ∧
    R ≤ 2 * Λ + 16 * Real.pi * G * ρ + {hi} * κ ^ 2 := by
""" + MAIN_PROOF

MUTANTS = {
    "M1_KK_3para2": ("K_ijK^ij <= 2k^2 (era 3)", main_stmt(kk="2")),
    "M2_shear_div3para2": ("sigma.sigma <= 3k^2 - K^2/2 (era /3)",
                           main_stmt(sh="3 * κ ^ 2 - K.trace ^ 2 / 2")),
    "M3_inferior_6para5": ("R >= s - 5k^2 (era 6)", main_stmt(lo="5")),
    "M4_superior_2para1": ("R <= s + 1k^2 (era 2)", main_stmt(hi="1")),
    "M5_autovalor_meio": ("|lambda_i| <= k/2 (era k)", """theorem m {K : Matrix (Fin 3) (Fin 3) ℝ} (hK : K.IsHermitian) {κ : ℝ}
    (hb : IIBound K κ) (i : Fin 3) : |hK.eigenvalues i| ≤ κ / 2 := by
  have hnorm : ‖hK.eigenvectorBasis i‖ = 1 := hK.eigenvectorBasis.orthonormal.1 i
  have hvv : (⇑(hK.eigenvectorBasis i) : Fin 3 → ℝ) ⬝ᵥ ⇑(hK.eigenvectorBasis i) = 1 := by
    have h := real_inner_self_eq_norm_sq (hK.eigenvectorBasis i)
    rw [EuclideanSpace.inner_eq_star_dotProduct, hnorm] at h
    simpa using h
  have h := hb ⇑(hK.eigenvectorBasis i)
  rw [hK.mulVec_eigenvectorBasis i, dotProduct_smul, hvv] at h
  simpa using h
"""),
    "M6_frobshear_div3para2": ("sigma.sigma = KK - K^2/2 (era /3)", """theorem m (K : Matrix (Fin 3) (Fin 3) ℝ) :
    frobSq (shear K) = frobSq K - K.trace ^ 2 / 2 := by
  simp only [frobSq, shear, Matrix.trace, Matrix.diag, Fin.sum_univ_three, Matrix.sub_apply,
    Matrix.smul_apply, Matrix.one_apply, smul_eq_mul]
  simp
  ring
"""),
    "M7_traco_sem_quadrado": ("tr(KK) = sum lambda_i (era lambda_i^2)", """theorem m {K : Matrix (Fin 3) (Fin 3) ℝ} (hK : K.IsHermitian) :
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
"""),
    "M8_sharp_6para5": ("diag(k,k,k) atinge R = s - 5k^2 (era 6)", """theorem m (κ Λ G ρ : ℝ) (hκ : 0 ≤ κ) :
    HamiltonianConstraint (diagonal ![κ, κ, κ])
      (2 * Λ + 16 * Real.pi * G * ρ - 5 * κ ^ 2) Λ G ρ := by
  rw [hamiltonian_iff]; simp [frobSq, Matrix.trace, Fin.sum_univ_three, diagonal_apply]; ring
"""),
}

if __name__ == "__main__":
    here = Path(__file__).parent
    for nome, (desc, body) in MUTANTS.items():
        (here / f"{nome}.lean").write_text(
            HEAD.format(nome=nome, desc=desc) + "\n" + body + TAIL, encoding="utf-8")
        print(nome)
