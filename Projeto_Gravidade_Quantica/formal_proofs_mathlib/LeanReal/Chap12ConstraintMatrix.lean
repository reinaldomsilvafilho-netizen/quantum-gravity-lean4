import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Analysis.CStarAlgebra.Matrix
import LeanReal.Chap12Constraint

/-!
# Capitulo 12 / SQG Thm. `thm:minimax_shear`: forma matricial pontual

Nivel de formalizacao: um ponto `x` de uma hipersuperficie espacial `Σ`, num referencial
ortonormal de `γ` em `x` (`γ_ij = δ_ij`). Nesse referencial:

* a curvatura extrinseca e uma matriz real simetrica `K : Matrix (Fin 3) (Fin 3) ℝ`;
* `K = γ^ij K_ij` e `Matrix.trace K`;
* `K_ij K^ij` e a norma de Frobenius ao quadrado `∑ᵢ ∑ⱼ K i j ^ 2` (`frobSq`);
* `σ_ij = K_ij − (K/3) γ_ij` e `shear K = K − (tr K / 3) • 1`;
* a hipotese `‖II‖_{L∞} ≤ κ*` do texto, `sup_{v≠0} |II(v,v)| / γ(v,v) ≤ κ*`, avaliada no
  ponto, e `IIBound K κ : ∀ v, |v ⬝ᵥ K v| ≤ κ (v ⬝ᵥ v)` (identica, sem enfraquecimento);
* o vinculo hamiltoniano e a forma do texto (SQG eq. `wdw_constraint`):
  `³R − 2Λ + (2/3)K² − σ_ijσ^ij − 16πGρ = 0`, tomado como HIPOTESE pontual.

O que e provado aqui (e nao suposto): diagonalizacao de `K` pelo teorema espectral da Mathlib,
`|λᵢ| ≤ κ` a partir de `IIBound`, `tr K = ∑ λᵢ`, `K_ijK^ij = ∑ λᵢ²`, `σσ = KK − K²/3`, as
cotas (i) e (ii) e a otimalidade com matrizes diagonais explicitas.

O que NAO e formalizado: a variedade lorentziana, a folheacao ADM e a deducao do vinculo a
partir das equacoes de Einstein (equacao de Gauss); o problema minimax `κ* = inf_Σ ‖II_Σ‖`.
-/

namespace LeanReal.Chap12

open Matrix

/-- `K_ij K^ij` num referencial ortonormal: quadrado da norma de Frobenius. -/
def frobSq (K : Matrix (Fin 3) (Fin 3) ℝ) : ℝ := ∑ i, ∑ j, K i j ^ 2

/-- Cisalhamento sem traco `σ_ij = K_ij − (K/3) δ_ij`. -/
noncomputable def shear (K : Matrix (Fin 3) (Fin 3) ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  K - (K.trace / 3) • (1 : Matrix (Fin 3) (Fin 3) ℝ)

/-- `‖II‖ ≤ κ` no ponto, na definicao do texto: `|II(v,v)| ≤ κ γ(v,v)` para todo `v`. -/
def IIBound (K : Matrix (Fin 3) (Fin 3) ℝ) (κ : ℝ) : Prop :=
  ∀ v : Fin 3 → ℝ, |v ⬝ᵥ (K *ᵥ v)| ≤ κ * (v ⬝ᵥ v)

/-- Vinculo hamiltoniano pontual na forma do texto (SQG eq. `wdw_constraint`). -/
def HamiltonianConstraint (K : Matrix (Fin 3) (Fin 3) ℝ) (R Λ G ρ : ℝ) : Prop :=
  R - 2 * Λ + (2 / 3) * K.trace ^ 2 - frobSq (shear K) - 16 * Real.pi * G * ρ = 0

/-- `σ_ijσ^ij = K_ijK^ij − K²/3`. -/
theorem frobSq_shear (K : Matrix (Fin 3) (Fin 3) ℝ) :
    frobSq (shear K) = frobSq K - K.trace ^ 2 / 3 := by
  simp only [frobSq, shear, Matrix.trace, Matrix.diag, Fin.sum_univ_three, Matrix.sub_apply,
    Matrix.smul_apply, Matrix.one_apply, smul_eq_mul]
  simp
  ring

/-- As duas formas do vinculo coincidem: `³R + K² − K_ijK^ij = 2Λ + 16πGρ`. -/
theorem hamiltonian_iff (K : Matrix (Fin 3) (Fin 3) ℝ) (R Λ G ρ : ℝ) :
    HamiltonianConstraint K R Λ G ρ ↔
      R + K.trace ^ 2 - frobSq K = 2 * Λ + 16 * Real.pi * G * ρ := by
  unfold HamiltonianConstraint
  rw [frobSq_shear]
  constructor <;> intro h <;> linarith

/-- `K_ijK^ij = tr(K K)` para `K` simetrica. -/
theorem frobSq_eq_trace_mul {K : Matrix (Fin 3) (Fin 3) ℝ} (hK : K.IsHermitian) :
    frobSq K = (K * K).trace := by
  simp only [frobSq, Matrix.trace, Matrix.diag, Matrix.mul_apply, sq]
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
  have h : K j i = K i j := by simpa using hK.apply i j
  rw [h]

/-- Diagonalizacao (teorema espectral): `tr(K K) = ∑ λᵢ²`. -/
theorem trace_mul_self_eq {K : Matrix (Fin 3) (Fin 3) ℝ} (hK : K.IsHermitian) :
    (K * K).trace = ∑ i, hK.eigenvalues i ^ 2 := by
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

/-- Diagonalizacao: `K = tr K = ∑ λᵢ`. -/
theorem trace_eq_sum {K : Matrix (Fin 3) (Fin 3) ℝ} (hK : K.IsHermitian) :
    K.trace = ∑ i, hK.eigenvalues i := by
  simpa using hK.trace_eq_sum_eigenvalues

/-- `‖II‖ ≤ κ` (forma quadratica) da `|λᵢ| ≤ κ` para cada curvatura principal. -/
theorem abs_eigenvalue_le {K : Matrix (Fin 3) (Fin 3) ℝ} (hK : K.IsHermitian) {κ : ℝ}
    (hb : IIBound K κ) (i : Fin 3) : |hK.eigenvalues i| ≤ κ := by
  have hnorm : ‖hK.eigenvectorBasis i‖ = 1 := hK.eigenvectorBasis.orthonormal.1 i
  have hvv : (⇑(hK.eigenvectorBasis i) : Fin 3 → ℝ) ⬝ᵥ ⇑(hK.eigenvectorBasis i) = 1 := by
    have h := real_inner_self_eq_norm_sq (hK.eigenvectorBasis i)
    rw [EuclideanSpace.inner_eq_star_dotProduct, hnorm] at h
    simpa using h
  have h := hb ⇑(hK.eigenvectorBasis i)
  rw [hK.mulVec_eigenvectorBasis i, dotProduct_smul, hvv] at h
  simpa using h

/-- **Teorema (forma matricial pontual).** `K` real simetrica 3×3 com `‖II‖ ≤ κ`, e o vinculo
hamiltoniano no ponto. Entao (i) `0 ≤ KK ≤ 3κ²` e `0 ≤ σσ ≤ 3κ² − K²/3`; (ii)
`2Λ + 16πGρ − 6κ² ≤ ³R ≤ 2Λ + 16πGρ + 2κ²`. -/
theorem constraint_bounds_matrix (K : Matrix (Fin 3) (Fin 3) ℝ) (hK : K.IsSymm) (κ R Λ G ρ : ℝ)
    (hb : IIBound K κ) (hH : HamiltonianConstraint K R Λ G ρ) :
    0 ≤ frobSq K ∧ frobSq K ≤ 3 * κ ^ 2 ∧
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

/-- Caso de vacuo (`ρ = 0`), na forma do enunciado: `³R + K² − K_ijK^ij = 2Λ`. -/
theorem constraint_bounds_vacuum (K : Matrix (Fin 3) (Fin 3) ℝ) (hK : K.IsSymm) (κ R Λ : ℝ)
    (hb : IIBound K κ) (hH : R + K.trace ^ 2 - frobSq K = 2 * Λ) :
    frobSq (shear K) ≤ 3 * κ ^ 2 - K.trace ^ 2 / 3 ∧
    2 * Λ - 6 * κ ^ 2 ≤ R ∧ R ≤ 2 * Λ + 2 * κ ^ 2 := by
  have hH' : HamiltonianConstraint K R Λ 0 0 := (hamiltonian_iff K R Λ 0 0).mpr (by simpa using hH)
  obtain ⟨-, -, -, h1, h2, h3⟩ := constraint_bounds_matrix K hK κ R Λ 0 0 hb hH'
  refine ⟨h1, by simpa using h2, by simpa using h3⟩

/-- Matrizes diagonais com entradas em `[-κ, κ]` satisfazem `‖II‖ ≤ κ`. -/
theorem IIBound_diagonal (d : Fin 3 → ℝ) (κ : ℝ) (hd : ∀ i, |d i| ≤ κ) :
    IIBound (diagonal d) κ := by
  intro v
  simp only [mulVec_diagonal, dotProduct, Fin.sum_univ_three]
  obtain ⟨a0, b0⟩ := abs_le.mp (hd 0)
  obtain ⟨a1, b1⟩ := abs_le.mp (hd 1)
  obtain ⟨a2, b2⟩ := abs_le.mp (hd 2)
  have s0 := mul_self_nonneg (v 0)
  have s1 := mul_self_nonneg (v 1)
  have s2 := mul_self_nonneg (v 2)
  rw [abs_le]
  constructor
  · nlinarith [mul_le_mul_of_nonneg_right a0 s0, mul_le_mul_of_nonneg_right a1 s1,
      mul_le_mul_of_nonneg_right a2 s2]
  · nlinarith [mul_le_mul_of_nonneg_right b0 s0, mul_le_mul_of_nonneg_right b1 s1,
      mul_le_mul_of_nonneg_right b2 s2]

/-- **Otimalidade.** Para `κ ≥ 0`: `diag(κ,κ,κ)` e `diag(κ,κ,−κ)` sao simetricas, satisfazem
`‖II‖ ≤ κ`, atingem `KK = 3κ²` e `σσ = 3κ² − K²/3`; com elas o vinculo vale exatamente com
`³R` no extremo inferior `2Λ + 16πGρ − 6κ²` e no superior `2Λ + 16πGρ + 2κ²`. -/
theorem constraint_bounds_matrix_sharp (κ Λ G ρ : ℝ) (hκ : 0 ≤ κ) :
    (diagonal ![κ, κ, κ]).IsSymm ∧ IIBound (diagonal ![κ, κ, κ]) κ ∧
    frobSq (diagonal ![κ, κ, κ]) = 3 * κ ^ 2 ∧
    frobSq (shear (diagonal ![κ, κ, κ])) = 3 * κ ^ 2 - (diagonal ![κ, κ, κ]).trace ^ 2 / 3 ∧
    HamiltonianConstraint (diagonal ![κ, κ, κ])
      (2 * Λ + 16 * Real.pi * G * ρ - 6 * κ ^ 2) Λ G ρ ∧
    (diagonal ![κ, κ, -κ]).IsSymm ∧ IIBound (diagonal ![κ, κ, -κ]) κ ∧
    frobSq (diagonal ![κ, κ, -κ]) = 3 * κ ^ 2 ∧
    frobSq (shear (diagonal ![κ, κ, -κ])) = 3 * κ ^ 2 - (diagonal ![κ, κ, -κ]).trace ^ 2 / 3 ∧
    HamiltonianConstraint (diagonal ![κ, κ, -κ])
      (2 * Λ + 16 * Real.pi * G * ρ + 2 * κ ^ 2) Λ G ρ := by
  have hk : |κ| ≤ κ := (abs_of_nonneg hκ).le
  have hk' : |-κ| ≤ κ := by rw [abs_neg]; exact hk
  refine ⟨isSymm_diagonal _, IIBound_diagonal _ _ ?_, ?_, ?_, ?_,
    isSymm_diagonal _, IIBound_diagonal _ _ ?_, ?_, ?_, ?_⟩
  · intro i; fin_cases i <;> simpa using hk
  · simp [frobSq, Fin.sum_univ_three, diagonal_apply]; ring
  · rw [frobSq_shear]; simp [frobSq, Fin.sum_univ_three, diagonal_apply]; ring
  · rw [hamiltonian_iff]; simp [frobSq, Matrix.trace, Fin.sum_univ_three, diagonal_apply]; ring
  · intro i; fin_cases i <;> simp [hk]
  · simp [frobSq, Fin.sum_univ_three, diagonal_apply]; ring
  · rw [frobSq_shear]; simp [frobSq, Fin.sum_univ_three, diagonal_apply]; ring
  · rw [hamiltonian_iff]; simp [frobSq, Matrix.trace, Fin.sum_univ_three, diagonal_apply]; ring

/-- Reciproca: se cada curvatura principal tem `|λᵢ| ≤ κ`, entao `‖II‖ ≤ κ`. Junto com
`abs_eigenvalue_le`, `IIBound K κ ↔ ∀ i, |λᵢ| ≤ κ`: a cota nao impoe outra relacao entre os
`λᵢ` (afirmacao usada na prova do texto). -/
theorem IIBound_of_abs_eigenvalue_le {K : Matrix (Fin 3) (Fin 3) ℝ} (hK : K.IsHermitian) {κ : ℝ}
    (h : ∀ i, |hK.eigenvalues i| ≤ κ) : IIBound K κ := by
  have hs := hK.spectral_theorem
  rw [Unitary.conjStarAlgAut_apply] at hs
  have hUV : (hK.eigenvectorUnitary : Matrix (Fin 3) (Fin 3) ℝ) *
      (star hK.eigenvectorUnitary : Matrix (Fin 3) (Fin 3) ℝ) = 1 :=
    Unitary.coe_mul_star_self _
  have hV : (star hK.eigenvectorUnitary : Matrix (Fin 3) (Fin 3) ℝ) =
      (hK.eigenvectorUnitary : Matrix (Fin 3) (Fin 3) ℝ)ᵀ := by
    rw [star_eq_conjTranspose, conjTranspose_eq_transpose_of_trivial]
  have hD := IIBound_diagonal (RCLike.ofReal ∘ hK.eigenvalues) κ (by intro i; simpa using h i)
  generalize (star hK.eigenvectorUnitary : Matrix (Fin 3) (Fin 3) ℝ) = V at hs hUV hV
  generalize (hK.eigenvectorUnitary : Matrix (Fin 3) (Fin 3) ℝ) = U at hs hUV hV
  generalize diagonal ((RCLike.ofReal : ℝ → ℝ) ∘ hK.eigenvalues) = D at hs hD
  intro v
  have key : ∀ x, v ⬝ᵥ (U *ᵥ x) = (V *ᵥ v) ⬝ᵥ x := by
    intro x; rw [hV, mulVec_transpose, dotProduct_mulVec]
  have e1 : v ⬝ᵥ (K *ᵥ v) = (V *ᵥ v) ⬝ᵥ (D *ᵥ (V *ᵥ v)) := by
    rw [hs, ← mulVec_mulVec, ← mulVec_mulVec, key]
  have e2 : v ⬝ᵥ v = (V *ᵥ v) ⬝ᵥ (V *ᵥ v) := by
    rw [← key, mulVec_mulVec, hUV, one_mulVec]
  rw [e1, e2]
  exact hD _

/-- `‖II‖ ≤ κ` equivale a `|λᵢ| ≤ κ` para as tres curvaturas principais. -/
theorem IIBound_iff {K : Matrix (Fin 3) (Fin 3) ℝ} (hK : K.IsHermitian) (κ : ℝ) :
    IIBound K κ ↔ ∀ i, |hK.eigenvalues i| ≤ κ :=
  ⟨fun hb i => abs_eigenvalue_le hK hb i, IIBound_of_abs_eigenvalue_le hK⟩

open scoped Matrix.Norms.L2Operator in
/-- A norma de operador `ℓ²` da Mathlib (`Matrix.Norms.L2Operator`) `‖K‖ ≤ κ` implica `‖II‖ ≤ κ`. -/
theorem IIBound_of_l2_opNorm_le {K : Matrix (Fin 3) (Fin 3) ℝ} {κ : ℝ} (hK : ‖K‖ ≤ κ) :
    IIBound K κ := by
  intro v
  have h3 := K.l2_opNorm_mulVec (WithLp.toLp 2 v)
  set x : EuclideanSpace ℝ (Fin 3) := WithLp.toLp 2 v
  set y : EuclideanSpace ℝ (Fin 3) := (EuclideanSpace.equiv (Fin 3) ℝ).symm (K *ᵥ x)
  have h1 : v ⬝ᵥ (K *ᵥ v) = inner ℝ x y := by
    simp [x, y, EuclideanSpace.inner_eq_star_dotProduct, dotProduct_comm]
  have h2 : v ⬝ᵥ v = ‖x‖ ^ 2 := by
    rw [← real_inner_self_eq_norm_sq, EuclideanSpace.inner_toLp_toLp]; simp
  rw [h1, h2]
  calc |inner ℝ x y| ≤ ‖x‖ * ‖y‖ := abs_real_inner_le_norm x y
    _ ≤ ‖x‖ * (κ * ‖x‖) :=
        mul_le_mul_of_nonneg_left (h3.trans (mul_le_mul_of_nonneg_right hK (norm_nonneg x)))
          (norm_nonneg x)
    _ = κ * ‖x‖ ^ 2 := by ring

open scoped Matrix.Norms.L2Operator in
/-- O teorema com a hipotese na norma de operador `ℓ²` da Mathlib. -/
theorem constraint_bounds_opNorm (K : Matrix (Fin 3) (Fin 3) ℝ) (hK : K.IsSymm) (κ R Λ G ρ : ℝ)
    (hb : ‖K‖ ≤ κ) (hH : HamiltonianConstraint K R Λ G ρ) :
    0 ≤ frobSq K ∧ frobSq K ≤ 3 * κ ^ 2 ∧
    0 ≤ frobSq (shear K) ∧ frobSq (shear K) ≤ 3 * κ ^ 2 - K.trace ^ 2 / 3 ∧
    2 * Λ + 16 * Real.pi * G * ρ - 6 * κ ^ 2 ≤ R ∧
    R ≤ 2 * Λ + 16 * Real.pi * G * ρ + 2 * κ ^ 2 :=
  constraint_bounds_matrix K hK κ R Λ G ρ (IIBound_of_l2_opNorm_le hb) hH

end LeanReal.Chap12

#print axioms LeanReal.Chap12.IIBound_iff
#print axioms LeanReal.Chap12.IIBound_of_l2_opNorm_le
#print axioms LeanReal.Chap12.constraint_bounds_opNorm
#print axioms LeanReal.Chap12.frobSq_shear
#print axioms LeanReal.Chap12.hamiltonian_iff
#print axioms LeanReal.Chap12.trace_mul_self_eq
#print axioms LeanReal.Chap12.abs_eigenvalue_le
#print axioms LeanReal.Chap12.constraint_bounds_matrix
#print axioms LeanReal.Chap12.constraint_bounds_vacuum
#print axioms LeanReal.Chap12.IIBound_diagonal
#print axioms LeanReal.Chap12.constraint_bounds_matrix_sharp
#print axioms LeanReal.Chap12.frobSq_eq_trace_mul
#print axioms LeanReal.Chap12.trace_eq_sum
#print axioms LeanReal.Chap12.IIBound_of_abs_eigenvalue_le
