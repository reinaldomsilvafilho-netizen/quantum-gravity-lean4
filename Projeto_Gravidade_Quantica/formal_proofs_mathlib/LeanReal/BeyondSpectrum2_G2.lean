import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Hermitian
import Mathlib.Analysis.Complex.Basic

/-!
# *Beyond the Spectrum* II (vol. 2), item G2

Source: `Manuscritos_Avulsos/paper_geometric_measures_functional_tensors/
paper_geometric_measures_functional_tensors.tex`, Lemma `lem:qfi_formula`
("QFI metric in an eigenbasis; classical, see [Liu et al. 2020, Thm. 2.1]").

Paper (definitions, §"The Integrated Quantum Fisher Information Volume"):
> For `ρ(x) ≻ 0`, `g^QFI_{μν}(x) := ½ Tr_χ(ρ(x){L_μ(x), L_ν(x)})`, `{A,B} = AB + BA`, where the
> SLD `L_μ` is defined implicitly by `∂_μρ = ½(ρL_μ + L_μρ)`.

Paper (lemma):
> Let `ρ(x) = ∑_i λ_i |i⟩⟨i|` with all `λ_i > 0`. Then `⟨i|L_μ|j⟩ = 2⟨i|∂_μρ|j⟩/(λ_i + λ_j)` and
> `g^QFI_{μν}(x) = 2 ∑_{i,j} Re(⟨i|∂_μρ|j⟩⟨j|∂_νρ|i⟩)/(λ_i + λ_j)`.

Formal version (pointwise in `x`; the derivatives `∂_μρ`, `∂_νρ` enter as GIVEN matrices `D`, `E`).
* `sld_entry` : in the eigenbasis (`ρ = diag λ`, `λ_i > 0`), every solution `L` of the SLD equation
  has `L_ij = 2 D_ij/(λ_i + λ_j)`. So the SLD is unique; `sld_exists` shows it exists.
* `qfi_eigen` : `½ Tr(ρ{L,M}) = 2 ∑_{i,j} D_ij E_ji/(λ_i + λ_j)`, for ANY complex `D`, `E`
  (no hermiticity needed for this complex identity).
* `qfi_eigen_re` : the paper's formula, with `Re` inside the sum, for `Re ½Tr(ρ{L,M})`.
* `qfi_im_zero` : if `D`, `E` are Hermitian (as `∂_μρ` is), then `½Tr(ρ{L,M})` is real, so `g^QFI`
  equals the paper's formula without taking a real part.
* `basis_change` : for a general `ρ = UΛUᴴ` (`UᴴU = UUᴴ = 1`), the SLD equation and `Tr(ρ{L,M})`
  are carried to the eigenbasis by `X ↦ UᴴXU`; this is the meaning of `⟨i|X|j⟩` in the paper.
REDUCTIONS (declared): no dependence on `x`, no differentiability, no `Tr ρ = 1` (not used by the
lemma). The spectral decomposition `ρ = UΛUᴴ` is taken as data, not derived (Mathlib has it:
`Matrix.IsHermitian.spectral_theorem`; it is not invoked here).
-/

namespace LeanReal.BeyondSpectrum2G2

open Matrix
open scoped BigOperators ComplexConjugate

set_option autoImplicit false

variable {χ : Type*} [Fintype χ] [DecidableEq χ]

/-- `ρ = diag(λ)` in its eigenbasis. -/
noncomputable def Λ (l : χ → ℝ) : Matrix χ χ ℂ := diagonal fun i => (l i : ℂ)

/-- SLD equation `D = ½(ρL + Lρ)`. -/
def IsSLD (ρ D L : Matrix χ χ ℂ) : Prop := D = (1 / 2 : ℂ) • (ρ * L + L * ρ)

/-- `g(L, M) = ½ Tr(ρ{L, M})`. -/
noncomputable def qfi (ρ L M : Matrix χ χ ℂ) : ℂ := (1 / 2 : ℂ) * trace (ρ * (L * M + M * L))

omit [Fintype χ] [DecidableEq χ] in
lemma den_ne {l : χ → ℝ} (hl : ∀ i, 0 < l i) (i j : χ) : ((l i : ℂ) + l j) ≠ 0 := by
  have : (0 : ℝ) < l i + l j := add_pos (hl i) (hl j)
  exact_mod_cast this.ne'

lemma Λ_mul (l : χ → ℝ) (X : Matrix χ χ ℂ) (i j : χ) : (Λ l * X) i j = l i * X i j := by
  simp [Λ, diagonal_mul]

lemma mul_Λ (l : χ → ℝ) (X : Matrix χ χ ℂ) (i j : χ) : (X * Λ l) i j = X i j * l j := by
  simp [Λ, mul_diagonal]

lemma sld_apply {l : χ → ℝ} {D L : Matrix χ χ ℂ} (h : IsSLD (Λ l) D L) (i j : χ) :
    D i j = (1 / 2 : ℂ) * ((l i : ℂ) + l j) * L i j := by
  rw [h, Matrix.smul_apply, Matrix.add_apply, Λ_mul, mul_Λ, smul_eq_mul]; ring

/-- `⟨i|L|j⟩ = 2⟨i|D|j⟩/(λ_i + λ_j)`. -/
theorem sld_entry {l : χ → ℝ} (hl : ∀ i, 0 < l i) {D L : Matrix χ χ ℂ}
    (h : IsSLD (Λ l) D L) (i j : χ) : L i j = 2 * D i j / ((l i : ℂ) + l j) := by
  rw [eq_div_iff (den_ne hl i j), sld_apply h]
  ring

/-- Existence of the SLD in the eigenbasis. -/
theorem sld_exists {l : χ → ℝ} (hl : ∀ i, 0 < l i) (D : Matrix χ χ ℂ) :
    IsSLD (Λ l) D (Matrix.of fun i j => 2 * D i j / ((l i : ℂ) + l j)) := by
  ext i j
  rw [Matrix.smul_apply, Matrix.add_apply, Λ_mul, mul_Λ, smul_eq_mul, Matrix.of_apply]
  have := den_ne hl i j
  field_simp

/-- Trace step: `Tr(Λ(LM + ML)) = ∑_{i,j} (λ_i + λ_j) L_ij M_ji`. -/
lemma trace_anticomm (l : χ → ℝ) (L M : Matrix χ χ ℂ) :
    trace (Λ l * (L * M + M * L)) =
      ∑ i, ∑ j, ((l i : ℂ) + l j) * (L i j * M j i) := by
  simp only [trace, diag, Λ_mul]
  simp only [Matrix.add_apply, mul_apply, Finset.mul_sum, mul_add,
    Finset.sum_add_distrib, add_mul]
  congr 1
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
  ring

/-- The QFI formula in the eigenbasis (complex form, no hermiticity needed). -/
theorem qfi_eigen {l : χ → ℝ} (hl : ∀ i, 0 < l i) {D E L M : Matrix χ χ ℂ}
    (hL : IsSLD (Λ l) D L) (hM : IsSLD (Λ l) E M) :
    qfi (Λ l) L M = 2 * ∑ i, ∑ j, D i j * E j i / ((l i : ℂ) + l j) := by
  rw [qfi, trace_anticomm, Finset.mul_sum, Finset.mul_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Finset.mul_sum, Finset.mul_sum]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [sld_entry hl hL i j, sld_entry hl hM j i]
  have h1 := den_ne hl i j
  have h2 : ((l j : ℂ) + l i) = (l i : ℂ) + l j := add_comm _ _
  rw [h2]
  field_simp

/-- The paper's formula, with `Re` inside the sum. -/
theorem qfi_eigen_re {l : χ → ℝ} (hl : ∀ i, 0 < l i) {D E L M : Matrix χ χ ℂ}
    (hL : IsSLD (Λ l) D L) (hM : IsSLD (Λ l) E M) :
    (qfi (Λ l) L M).re = 2 * ∑ i, ∑ j, (D i j * E j i).re / (l i + l j) := by
  rw [qfi_eigen hl hL hM]
  have h2 : ((2 : ℂ) * ∑ i, ∑ j, D i j * E j i / ((l i : ℂ) + l j)).re =
      2 * (∑ i, ∑ j, D i j * E j i / ((l i : ℂ) + l j)).re := by simp
  rw [h2, Complex.re_sum]
  congr 1
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Complex.re_sum]
  refine Finset.sum_congr rfl fun j _ => ?_
  have : ((l i : ℂ) + l j) = ((l i + l j : ℝ) : ℂ) := by push_cast; ring
  rw [this, Complex.div_ofReal_re]

/-- For Hermitian `D`, `E` (as `∂_μρ`, `∂_νρ` are), `½Tr(ρ{L,M})` is real. -/
theorem qfi_im_zero {l : χ → ℝ} (hl : ∀ i, 0 < l i) {D E L M : Matrix χ χ ℂ}
    (hD : D.IsHermitian) (hE : E.IsHermitian)
    (hL : IsSLD (Λ l) D L) (hM : IsSLD (Λ l) E M) : (qfi (Λ l) L M).im = 0 := by
  rw [qfi_eigen hl hL hM]
  set S := ∑ i, ∑ j, D i j * E j i / ((l i : ℂ) + l j) with hS
  have hd : ∀ i j, conj (D i j) = D j i := fun i j => by
    have := congrFun (congrFun hD j) i
    simpa [conjTranspose_apply] using this
  have he : ∀ i j, conj (E i j) = E j i := fun i j => by
    have := congrFun (congrFun hE j) i
    simpa [conjTranspose_apply] using this
  have hconj : conj S = S := by
    rw [hS, map_sum, Finset.sum_comm]
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [map_sum]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [map_div₀, map_mul, hd, he, map_add, Complex.conj_ofReal, Complex.conj_ofReal]
    ring
  have : S.im = 0 := Complex.conj_eq_iff_im.mp hconj
  simp [this]

/-- Change of basis: for `ρ = UΛUᴴ` with `U` unitary (`UᴴU = UUᴴ = 1`), `X ↦ UᴴXU` carries the
SLD equation and `Tr(ρ{L,M})` to the eigenbasis. -/
theorem basis_change (U : Matrix χ χ ℂ) (h1 : Uᴴ * U = 1) (h2 : U * Uᴴ = 1)
    (Λ₀ D L M : Matrix χ χ ℂ) :
    (IsSLD (U * Λ₀ * Uᴴ) D L → IsSLD Λ₀ (Uᴴ * D * U) (Uᴴ * L * U)) ∧
      qfi (U * Λ₀ * Uᴴ) L M = qfi Λ₀ (Uᴴ * L * U) (Uᴴ * M * U) := by
  have key : ∀ X Y : Matrix χ χ ℂ, Uᴴ * X * U * (Uᴴ * Y * U) = Uᴴ * (X * Y) * U := by
    intro X Y
    calc Uᴴ * X * U * (Uᴴ * Y * U) = Uᴴ * X * (U * Uᴴ) * Y * U := by simp only [Matrix.mul_assoc]
      _ = Uᴴ * (X * Y) * U := by rw [h2]; simp only [Matrix.mul_one, Matrix.mul_assoc]
  have h1' : ∀ X : Matrix χ χ ℂ, Uᴴ * (U * X) = X := fun X => by
    rw [← Matrix.mul_assoc, h1, Matrix.one_mul]
  refine ⟨fun h => ?_, ?_⟩
  · unfold IsSLD at h ⊢
    rw [h, Matrix.mul_smul, Matrix.smul_mul]
    congr 1
    simp only [Matrix.mul_add, Matrix.add_mul, Matrix.mul_assoc, h1', h1, Matrix.mul_one]
  · unfold qfi
    congr 1
    rw [key, key, ← Matrix.add_mul, ← Matrix.mul_add]
    set X := L * M + M * L
    rw [show Λ₀ * (Uᴴ * X * U) = (Λ₀ * Uᴴ * X) * U by simp only [Matrix.mul_assoc],
      trace_mul_comm (Λ₀ * Uᴴ * X)]
    simp only [Matrix.mul_assoc]

/-! ### Non-vacuity witness -/

/-- `χ = 2`, `λ = (1, 3)`, `D = [[1, 1], [1, 1]]` (Hermitian). The SLD exists, and the formula
gives `2(1/2 + 1/4 + 1/4 + 1/6) = 7/3`. -/
example : ∃ (l : Fin 2 → ℝ) (D L : Matrix (Fin 2) (Fin 2) ℂ), (∀ i, 0 < l i) ∧ D.IsHermitian ∧
    IsSLD (Λ l) D L ∧ qfi (Λ l) L L = 7 / 3 := by
  have hl : ∀ i, 0 < (![1, 3] : Fin 2 → ℝ) i := by intro i; fin_cases i <;> norm_num
  refine ⟨![1, 3], Matrix.of fun _ _ => 1, _, hl, ?_, sld_exists hl _, ?_⟩
  · ext i j; simp [conjTranspose_apply]
  · rw [qfi_eigen hl (sld_exists hl _) (sld_exists hl _)]
    simp [Fin.sum_univ_two]
    norm_num

/-! ### Mutant proved false: the formula without the factor 2 -/

/-- Mutant: `g = ∑ D_ij E_ji/(λ_i + λ_j)` (factor 2 dropped). False for `χ = 1`, `λ = 1`, `D = 1`:
the true value is `1`, the mutant gives `1/2`. -/
theorem mutant_no_two_false :
    ¬ (∀ (l : Fin 1 → ℝ) (D L : Matrix (Fin 1) (Fin 1) ℂ), (∀ i, 0 < l i) →
        IsSLD (Λ l) D L → qfi (Λ l) L L = ∑ i, ∑ j, D i j * D j i / ((l i : ℂ) + l j)) := by
  intro h
  have hl : ∀ i : Fin 1, 0 < (fun _ : Fin 1 => (1 : ℝ)) i := fun _ => one_pos
  have h1 := h (fun _ : Fin 1 => (1 : ℝ)) (1 : Matrix (Fin 1) (Fin 1) ℂ) _ hl (sld_exists hl _)
  rw [qfi_eigen hl (sld_exists hl _) (sld_exists hl _)] at h1
  norm_num at h1

end LeanReal.BeyondSpectrum2G2

#print axioms LeanReal.BeyondSpectrum2G2.sld_entry
#print axioms LeanReal.BeyondSpectrum2G2.sld_exists
#print axioms LeanReal.BeyondSpectrum2G2.qfi_eigen
#print axioms LeanReal.BeyondSpectrum2G2.qfi_eigen_re
#print axioms LeanReal.BeyondSpectrum2G2.qfi_im_zero
#print axioms LeanReal.BeyondSpectrum2G2.basis_change
#print axioms LeanReal.BeyondSpectrum2G2.mutant_no_two_false
