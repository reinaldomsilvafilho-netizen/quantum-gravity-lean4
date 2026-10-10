import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-!
# Capitulo 1, Proposicao "Spectral and Critical Correspondence", item (i) (Lote A2, item 5)

Fonte: `unified_quantum_gravity_book/chap01_functional_realizations_matrices_tensors.tex`,
Proposicao "Spectral and Critical Correspondence" (sem rotulo):

> Let `A ∈ Sym_n(ℝ)` be symmetric with eigendecomposition `A = V Λ Vᵀ`,
> `Λ = diag(λ_1, …, λ_n)`, `λ_1 ≤ … ≤ λ_n`. Then (i) the global extrema of `f_A|_{S^{n-1}}`
> satisfy `min_{S^{n-1}} f_A = λ_1`, `max_{S^{n-1}} f_A = λ_n`, where `f_A(x) = xᵀAx`.

## Reducao declarada

* `S^{n-1}` e o conjunto `{x : Fin n → ℝ | x ⬝ᵥ x = 1}`; `f_A(x) = x ⬝ᵥ (A *ᵥ x)`.
* "Simetrica" e `Matrix.IsSymm A` (`Aᵀ = A`). Pede-se `n ≥ 1` (`[NeZero n]`), que o livro supoe
  em silencio (para `n = 0` a esfera e vazia e nao ha minimo).
* `λ_1` e `λ_n` sao lidos de forma intrinseca: o menor e o maior elemento do espectro real
  `spectrum ℝ A`. Isso dispensa a ordenacao `λ_1 ≤ … ≤ λ_n` (o livro so a usa para nomear o
  menor e o maior autovalor). A versao com `Finset.inf'`/`Finset.sup'` dos autovalores de Mathlib
  (`Matrix.IsHermitian.eigenvalues`) tambem e dada.
* Prova: teorema espectral de Mathlib, `A = U diag(λ) Uᵀ` com `U Uᵀ = 1`; com `c = Uᵀx`,
  `f_A(x) = ∑ λ_i c_i²` e `∑ c_i² = x ⬝ᵥ x`. O item (ii) (pontos criticos) ja esta em
  `BeyondSpectrum1_B3` (`critical_iff_eigen`) e nao e repetido.
-/

noncomputable section

namespace LeanReal.Chap01Rayleigh

open Matrix Finset

variable {n : ℕ}

/-- Realizacao quadratica `f_A(x) = xᵀAx` (eq. `eq:quad_form`). -/
def fA (A : Matrix (Fin n) (Fin n) ℝ) (x : Fin n → ℝ) : ℝ := x ⬝ᵥ (A *ᵥ x)

/-- Esfera unitaria `S^{n-1} = {x | ‖x‖₂ = 1}`, escrita como `x ⬝ᵥ x = 1`. -/
def sphere (n : ℕ) : Set (Fin n → ℝ) := {x | x ⬝ᵥ x = 1}

/-- Uma matriz real simetrica e hermitiana. -/
theorem isHermitian_of_isSymm {A : Matrix (Fin n) (Fin n) ℝ} (hA : A.IsSymm) :
    A.IsHermitian := by
  unfold IsHermitian
  rw [conjTranspose_eq_transpose_of_trivial]
  exact hA

/-- Forma quadratica de `U diag(d) Uᵀ`: `xᵀ(U diag(d) Uᵀ)x = ∑ d_i (Uᵀx)_i²`. -/
theorem quad_conj (U : Matrix (Fin n) (Fin n) ℝ) (d x : Fin n → ℝ) :
    x ⬝ᵥ ((U * diagonal d * Uᵀ) *ᵥ x) = ∑ i, d i * (Uᵀ *ᵥ x) i ^ 2 := by
  rw [← mulVec_mulVec, ← mulVec_mulVec, dotProduct_mulVec, ← mulVec_transpose]
  simp only [dotProduct, mulVec_diagonal]
  refine Finset.sum_congr rfl fun i _ => ?_
  ring

/-- Se `U Uᵀ = 1`, entao `∑ (Uᵀx)_i² = x ⬝ᵥ x`. -/
theorem norm_conj (U : Matrix (Fin n) (Fin n) ℝ) (hU : U * Uᵀ = 1) (x : Fin n → ℝ) :
    ∑ i, (Uᵀ *ᵥ x) i ^ 2 = x ⬝ᵥ x := by
  have h : ∑ i, (Uᵀ *ᵥ x) i ^ 2 = (Uᵀ *ᵥ x) ⬝ᵥ (Uᵀ *ᵥ x) := by
    simp only [dotProduct, sq]
  rw [h, mulVec_transpose, ← dotProduct_mulVec, ← mulVec_transpose, mulVec_mulVec, hU,
    one_mulVec]

/-- Forma espectral de `f_A`: com `U` a matriz unitaria de autovetores de Mathlib e `c = Uᵀx`,
`f_A(x) = ∑ λ_i c_i²` e `∑ c_i² = x ⬝ᵥ x`. -/
theorem fA_eq_sum {A : Matrix (Fin n) (Fin n) ℝ} (hA : A.IsHermitian) (x : Fin n → ℝ) :
    fA A x = ∑ i, hA.eigenvalues i *
        ((hA.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℝ)ᵀ *ᵥ x) i ^ 2 ∧
      ∑ i, ((hA.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℝ)ᵀ *ᵥ x) i ^ 2 = x ⬝ᵥ x := by
  set U : Matrix (Fin n) (Fin n) ℝ := (hA.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℝ) with hUdef
  have hUs : star U = Uᵀ := by
    rw [star_eq_conjTranspose, conjTranspose_eq_transpose_of_trivial]
  have hUU : U * Uᵀ = 1 := by
    rw [← hUs]
    exact Unitary.mul_star_self_of_mem hA.eigenvectorUnitary.2
  have hspec : A = U * diagonal hA.eigenvalues * Uᵀ := by
    have h := hA.spectral_theorem
    rw [Unitary.conjStarAlgAut_apply] at h
    rw [← hUs]
    simpa using h
  refine ⟨?_, norm_conj U hUU x⟩
  unfold fA
  conv_lhs => rw [hspec]
  exact quad_conj U _ x

/-- Cotas de Rayleigh: para `x ∈ S^{n-1}`, `min λ ≤ f_A(x) ≤ max λ`. -/
theorem rayleigh_bounds [NeZero n] {A : Matrix (Fin n) (Fin n) ℝ} (hA : A.IsHermitian)
    {x : Fin n → ℝ} (hx : x ∈ sphere n) :
    univ.inf' univ_nonempty hA.eigenvalues ≤ fA A x ∧
      fA A x ≤ univ.sup' univ_nonempty hA.eigenvalues := by
  obtain ⟨hf, hc⟩ := fA_eq_sum hA x
  have hx1 : x ⬝ᵥ x = 1 := hx
  set c := ((hA.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℝ)ᵀ *ᵥ x)
  rw [hx1] at hc
  constructor
  · rw [hf]
    calc univ.inf' univ_nonempty hA.eigenvalues
        = ∑ i, univ.inf' univ_nonempty hA.eigenvalues * c i ^ 2 := by
          rw [← Finset.mul_sum, hc, mul_one]
      _ ≤ _ := Finset.sum_le_sum fun i _ =>
          mul_le_mul_of_nonneg_right (Finset.inf'_le _ (mem_univ i)) (sq_nonneg _)
  · rw [hf]
    calc ∑ i, hA.eigenvalues i * c i ^ 2
        ≤ ∑ i, univ.sup' univ_nonempty hA.eigenvalues * c i ^ 2 :=
          Finset.sum_le_sum fun i _ =>
            mul_le_mul_of_nonneg_right (Finset.le_sup' _ (mem_univ i)) (sq_nonneg _)
      _ = _ := by rw [← Finset.mul_sum, hc, mul_one]

/-- Cada autovetor normalizado de Mathlib esta na esfera e realiza seu autovalor. -/
theorem eigenvector_attains {A : Matrix (Fin n) (Fin n) ℝ} (hA : A.IsHermitian) (i : Fin n) :
    (⇑(hA.eigenvectorBasis i) : Fin n → ℝ) ∈ sphere n ∧
      fA A ⇑(hA.eigenvectorBasis i) = hA.eigenvalues i := by
  set U : Matrix (Fin n) (Fin n) ℝ := (hA.eigenvectorUnitary : Matrix (Fin n) (Fin n) ℝ)
  have hUs : star U = Uᵀ := by
    rw [star_eq_conjTranspose, conjTranspose_eq_transpose_of_trivial]
  have hUtU : Uᵀ * U = 1 := by
    rw [← hUs]
    exact Unitary.star_mul_self_of_mem hA.eigenvectorUnitary.2
  have hv : (⇑(hA.eigenvectorBasis i) : Fin n → ℝ) ⬝ᵥ ⇑(hA.eigenvectorBasis i) = 1 := by
    have h := congrFun (congrFun hUtU i) i
    simpa [Matrix.mul_apply, dotProduct, U] using h
  refine ⟨hv, ?_⟩
  unfold fA
  rw [hA.mulVec_eigenvectorBasis, dotProduct_smul, hv, smul_eq_mul, mul_one]

/-- **Proposicao "Spectral and Critical Correspondence" (i)**, forma com autovalores de
Mathlib: `min_{S^{n-1}} f_A = min_i λ_i` e `max_{S^{n-1}} f_A = max_i λ_i`. -/
theorem rayleigh_extrema_eigenvalues [NeZero n] {A : Matrix (Fin n) (Fin n) ℝ}
    (hA : A.IsHermitian) :
    IsLeast (fA A '' sphere n) (univ.inf' univ_nonempty hA.eigenvalues) ∧
      IsGreatest (fA A '' sphere n) (univ.sup' univ_nonempty hA.eigenvalues) := by
  obtain ⟨i, -, hi⟩ := Finset.exists_mem_eq_inf' (univ_nonempty (α := Fin n)) hA.eigenvalues
  obtain ⟨j, -, hj⟩ := Finset.exists_mem_eq_sup' (univ_nonempty (α := Fin n)) hA.eigenvalues
  refine ⟨⟨⟨_, (eigenvector_attains hA i).1, by rw [(eigenvector_attains hA i).2, hi]⟩, ?_⟩,
    ⟨⟨_, (eigenvector_attains hA j).1, by rw [(eigenvector_attains hA j).2, hj]⟩, ?_⟩⟩
  · rintro _ ⟨x, hx, rfl⟩
    exact (rayleigh_bounds hA hx).1
  · rintro _ ⟨x, hx, rfl⟩
    exact (rayleigh_bounds hA hx).2

/-- **Proposicao "Spectral and Critical Correspondence" (i)**, forma intrinseca: para `A`
real simetrica e `n ≥ 1`, o minimo de `f_A` na esfera existe e e o menor elemento do espectro
real de `A` (`λ_1`), e o maximo existe e e o maior elemento do espectro (`λ_n`). -/
theorem rayleigh_extrema [NeZero n] {A : Matrix (Fin n) (Fin n) ℝ} (hA : A.IsSymm) :
    ∃ lmin lmax : ℝ, IsLeast (fA A '' sphere n) lmin ∧ IsLeast (spectrum ℝ A) lmin ∧
      IsGreatest (fA A '' sphere n) lmax ∧ IsGreatest (spectrum ℝ A) lmax := by
  have hH := isHermitian_of_isSymm hA
  obtain ⟨h1, h2⟩ := rayleigh_extrema_eigenvalues hH
  refine ⟨_, _, h1, ?_, h2, ?_⟩
  · rw [hH.spectrum_real_eq_range_eigenvalues]
    refine ⟨?_, ?_⟩
    · obtain ⟨i, -, hi⟩ :=
        Finset.exists_mem_eq_inf' (univ_nonempty (α := Fin n)) hH.eigenvalues
      exact ⟨i, hi.symm⟩
    · rintro _ ⟨i, rfl⟩
      exact Finset.inf'_le _ (mem_univ i)
  · rw [hH.spectrum_real_eq_range_eigenvalues]
    refine ⟨?_, ?_⟩
    · obtain ⟨i, -, hi⟩ :=
        Finset.exists_mem_eq_sup' (univ_nonempty (α := Fin n)) hH.eigenvalues
      exact ⟨i, hi.symm⟩
    · rintro _ ⟨i, rfl⟩
      exact Finset.le_sup' _ (mem_univ i)

/-! ## Testemunha: `M = [[2,1],[1,2]]` (nao diagonal), espectro `{1,3}` -/

/-- A matriz da testemunha. -/
def M : Matrix (Fin 2) (Fin 2) ℝ := !![2, 1; 1, 2]

theorem M_isSymm : M.IsSymm := by
  unfold IsSymm M
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

/-- Elementos do espectro de `M` sao raizes de `(μ-2)² = 1`, logo `μ ∈ {1,3}`. -/
theorem M_spectrum {μ : ℝ} (hμ : μ ∈ spectrum ℝ M) : μ = 1 ∨ μ = 3 := by
  rw [spectrum.mem_iff, Matrix.isUnit_iff_isUnit_det, isUnit_iff_ne_zero, not_not] at hμ
  have h : (μ - 2) * (μ - 2) - 1 = 0 := by
    rw [← hμ, Matrix.det_fin_two]
    simp [M, Algebra.algebraMap_eq_smul_one]
  have : (μ - 1) * (μ - 3) = 0 := by linarith [h]
  rcases mul_eq_zero.mp this with h1 | h3
  · left; linarith
  · right; linarith

/-- Testemunha nao degenerada: pelo teorema, na esfera `1 ≤ xᵀMx ≤ 3` (desigualdade nao
trivial: equivale a `|2x₀x₁| ≤ x₀² + x₁²`), e os valores `1` e `3` sao atingidos. -/
theorem witness_M :
    (∀ x ∈ sphere 2, 1 ≤ fA M x ∧ fA M x ≤ 3) ∧
      (∃ x ∈ sphere 2, fA M x = 1) ∧ (∃ x ∈ sphere 2, fA M x = 3) := by
  obtain ⟨lmin, lmax, hmin, hsmin, hmax, hsmax⟩ := rayleigh_extrema M_isSymm
  -- valores de teste: (3/5, -4/5) e (3/5, 4/5)
  have t1 : (![3/5, -4/5] : Fin 2 → ℝ) ∈ sphere 2 := by
    simp [sphere, dotProduct, Fin.sum_univ_two]; norm_num
  have t2 : (![3/5, 4/5] : Fin 2 → ℝ) ∈ sphere 2 := by
    simp [sphere, dotProduct, Fin.sum_univ_two]; norm_num
  have f1 : fA M ![3/5, -4/5] = 26 / 25 := by
    simp [fA, M, dotProduct, Fin.sum_univ_two, mulVec]
    norm_num
  have f2 : fA M ![3/5, 4/5] = 74 / 25 := by
    simp [fA, M, dotProduct, Fin.sum_univ_two, mulVec]
    norm_num
  have hlmin : lmin = 1 := by
    rcases M_spectrum hsmin.1 with h | h
    · exact h
    · exfalso
      have := hmin.2 ⟨_, t1, f1⟩
      rw [h] at this; norm_num at this
  have hlmax : lmax = 3 := by
    rcases M_spectrum hsmax.1 with h | h
    · exfalso
      have := hmax.2 ⟨_, t2, f2⟩
      rw [h] at this; norm_num at this
    · exact h
  refine ⟨fun x hx => ⟨?_, ?_⟩, ?_, ?_⟩
  · rw [← hlmin]; exact hmin.2 ⟨x, hx, rfl⟩
  · rw [← hlmax]; exact hmax.2 ⟨x, hx, rfl⟩
  · obtain ⟨x, hx, hfx⟩ := hmin.1
    exact ⟨x, hx, hfx.trans hlmin⟩
  · obtain ⟨x, hx, hfx⟩ := hmax.1
    exact ⟨x, hx, hfx.trans hlmax⟩

/-! ## Mutantes provados FALSOS -/

/-- Mutante 1 (sem simetria): para `N = [[0,1],[0,0]]` o espectro real e `{0}`, mas
`f_N(3/5, 4/5) = 12/25 > 0`; logo o maximo na esfera nao e o maior autovalor. -/
theorem mutant_no_symmetry_false :
    ¬ (∀ A : Matrix (Fin 2) (Fin 2) ℝ, ∃ lmax : ℝ,
        IsGreatest (fA A '' sphere 2) lmax ∧ IsGreatest (spectrum ℝ A) lmax) := by
  intro h
  obtain ⟨lmax, hf, hs⟩ := h !![0, 1; 0, 0]
  have h0 : lmax = 0 := by
    have hμ := hs.1
    rw [spectrum.mem_iff, Matrix.isUnit_iff_isUnit_det, isUnit_iff_ne_zero, not_not] at hμ
    rw [Matrix.det_fin_two] at hμ
    simp [Algebra.algebraMap_eq_smul_one] at hμ
    exact hμ
  have t2 : (![3/5, 4/5] : Fin 2 → ℝ) ∈ sphere 2 := by
    simp [sphere, dotProduct, Fin.sum_univ_two]; norm_num
  have f2 : fA !![0, 1; 0, 0] ![3/5, 4/5] = 12 / 25 := by
    simp [fA, dotProduct, Fin.sum_univ_two, mulVec]
    norm_num
  have := hf.2 ⟨_, t2, f2⟩
  rw [h0] at this
  norm_num at this

/-- Mutante 2 (confundir o maximo de Rayleigh com a maior entrada diagonal): falso para `M`,
cuja diagonal e `2` mas cujo maximo na esfera e `3`. -/
theorem mutant_diagonal_false :
    ¬ (∀ x ∈ sphere 2, fA M x ≤ 2) := by
  intro h
  obtain ⟨-, -, x, hx, hfx⟩ := witness_M
  have := h x hx
  linarith

end LeanReal.Chap01Rayleigh

#print axioms LeanReal.Chap01Rayleigh.quad_conj
#print axioms LeanReal.Chap01Rayleigh.norm_conj
#print axioms LeanReal.Chap01Rayleigh.fA_eq_sum
#print axioms LeanReal.Chap01Rayleigh.rayleigh_bounds
#print axioms LeanReal.Chap01Rayleigh.eigenvector_attains
#print axioms LeanReal.Chap01Rayleigh.rayleigh_extrema_eigenvalues
#print axioms LeanReal.Chap01Rayleigh.rayleigh_extrema
#print axioms LeanReal.Chap01Rayleigh.M_spectrum
#print axioms LeanReal.Chap01Rayleigh.witness_M
#print axioms LeanReal.Chap01Rayleigh.mutant_no_symmetry_false
#print axioms LeanReal.Chap01Rayleigh.mutant_diagonal_false
