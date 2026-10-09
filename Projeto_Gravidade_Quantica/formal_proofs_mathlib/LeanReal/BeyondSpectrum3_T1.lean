import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Analysis.Complex.Basic

/-!
# *Beyond the Spectrum* III (Zenodo concept DOI 10.5281/zenodo.22644743), item T1

Source: `Manuscritos_Avulsos/paper_beyond_the_spectrum_3/paper_beyond_the_spectrum_3.tex`,
Proposition `thm:modular_hamiltonian_spec` ("OBL-014: Partial trace and modular Hamiltonian"),
items (1) and (2).

Paper:
> On `Ω = Ω₁ × Ω₂`, let `ρ_{Ω₁}` be the operator on `L²(Ω₁)` with kernel
> `ρ_{Ω₁}(x₁, y₁) := ∫_{Ω₂} K_A(x₁, z₂; y₁, z₂) dz₂`. Assume `A ≠ 0`.
> (1) `ρ_{Ω₁}` is self-adjoint, positive semi-definite and trace class, with `Tr ρ_{Ω₁} = Tr(A)`.
> (2) If each `ψ_k` has finite Schmidt rank `m_k`, that is, `ψ_k = ∑_{l=1}^{m_k} a_{kl} ⊗ b_{kl}`,
> then `rank ρ_{Ω₁} ≤ ∑_{k=1}^n m_k`.

REDUCTION (declared). Only the FINITE-DIMENSIONAL analogue is formalized:
* `Ω₁`, `Ω₂` are finite index types `ι`, `κ` with counting measure; `L²(Ωᵢ)` becomes `ι → ℂ`,
  `κ → ℂ`; the integral `∫_{Ω₂} dz₂` becomes `∑ z : κ`. The operator `T_A` on `L²(Ω₁ × Ω₂)`
  becomes a matrix `K` indexed by `ι × κ`. Trace class, the integral-operator setting, Mercer and
  items (3)–(4) are NOT formalized.
* (1) is proved for EVERY matrix `K` (trace identity) and every PSD `K` (PSD preservation and
  self-adjointness). `Tr K = Tr(A)` for `K = K_A` is the earlier proposition
  `prop:kernel_codomain_psd` and is NOT re-proved here; `trace_ptr` gives `Tr ρ = Tr K`.
* (2): the frame `ψ_k : ι × κ → ℂ` is written as an `ι × κ` matrix, and `K_A` is the kernel
  `K_A((x,z),(y,w)) = ∑_{j,k} A_{jk} ψ_j(x,z) conj(ψ_k(y,w))` (paper's `K_A(x,y) = ∑ A_{jk} ψ_j(x)
  \overline{ψ_k(y)}`). No hypothesis on `A` is needed for the rank bound (in particular `A ≠ 0`
  is not used).
-/

namespace LeanReal.BeyondSpectrum3T1

open Matrix Finset
open scoped ComplexOrder

variable {ι κ : Type*} [Fintype ι] [Fintype κ]

/-- Partial trace over the second factor: `(Tr₂ K)(x, y) = ∑_z K((x,z),(y,z))`. -/
def ptr (K : Matrix (ι × κ) (ι × κ) ℂ) : Matrix ι ι ℂ :=
  fun x y => ∑ z, K (x, z) (y, z)

/-- Item (1), trace: `Tr(Tr₂ K) = Tr K`. -/
theorem trace_ptr (K : Matrix (ι × κ) (ι × κ) ℂ) : (ptr K).trace = K.trace := by
  simp only [Matrix.trace, Matrix.diag, ptr]
  rw [Fintype.sum_prod_type]

omit [Fintype ι] in
/-- Item (1), self-adjointness: `Tr₂` maps Hermitian matrices to Hermitian matrices. -/
theorem ptr_isHermitian {K : Matrix (ι × κ) (ι × κ) ℂ} (hK : K.IsHermitian) :
    (ptr K).IsHermitian := by
  ext x y
  simp only [conjTranspose_apply, ptr, star_sum]
  refine Finset.sum_congr rfl fun z _ => ?_
  exact hK.apply (x, z) (y, z)

/-- Product vector `x ⊗ e_z`. -/
def prodVec [DecidableEq κ] (v : ι → ℂ) (z : κ) : ι × κ → ℂ :=
  fun p => if p.2 = z then v p.1 else 0

lemma quad_prodVec [DecidableEq κ] (K : Matrix (ι × κ) (ι × κ) ℂ) (v : ι → ℂ) (z : κ) :
    star (prodVec v z) ⬝ᵥ (K *ᵥ prodVec v z) =
      ∑ x, ∑ y, star (v x) * K (x, z) (y, z) * v y := by
  simp only [dotProduct, mulVec, prodVec, Fintype.sum_prod_type, Pi.star_apply]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [Finset.sum_eq_single z]
  · simp only [ite_true, Finset.mul_sum]
    refine Finset.sum_congr rfl fun y _ => ?_
    rw [Finset.sum_eq_single z]
    · simp [mul_assoc]
    · intro w _ hw; simp [hw]
    · simp
  · intro w _ hw; simp [hw]
  · simp

/-- Item (1), positivity: `Tr₂` preserves positive semi-definiteness. -/
theorem ptr_posSemidef {K : Matrix (ι × κ) (ι × κ) ℂ} (hK : K.PosSemidef) :
    (ptr K).PosSemidef := by
  classical
  rw [posSemidef_iff_dotProduct_mulVec] at hK ⊢
  refine ⟨ptr_isHermitian hK.1, fun v => ?_⟩
  have key : star v ⬝ᵥ (ptr K *ᵥ v) =
      ∑ z, star (prodVec v z) ⬝ᵥ (K *ᵥ prodVec v z) := by
    calc star v ⬝ᵥ (ptr K *ᵥ v)
        = ∑ x, ∑ y, ∑ z, star (v x) * K (x, z) (y, z) * v y := by
          simp only [dotProduct, mulVec, ptr, Pi.star_apply, Finset.mul_sum, Finset.sum_mul]
          refine Finset.sum_congr rfl fun x _ => Finset.sum_congr rfl fun y _ =>
            Finset.sum_congr rfl fun z _ => ?_
          ring
      _ = ∑ x, ∑ z, ∑ y, star (v x) * K (x, z) (y, z) * v y :=
          Finset.sum_congr rfl fun x _ => Finset.sum_comm
      _ = ∑ z, ∑ x, ∑ y, star (v x) * K (x, z) (y, z) * v y := Finset.sum_comm
      _ = ∑ z, star (prodVec v z) ⬝ᵥ (K *ᵥ prodVec v z) := by simp only [quad_prodVec]
  rw [key]
  exact Finset.sum_nonneg fun z _ => hK.2 _

/-- The kernel `K_A((x,z),(y,w)) = ∑_{j,k} A_{jk} ψ_j(x,z) conj(ψ_k(y,w))` of the frame `ψ`. -/
def kernelA {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) (ψ : Fin n → Matrix ι κ ℂ) :
    Matrix (ι × κ) (ι × κ) ℂ :=
  fun p q => ∑ j, ∑ k, A j k * ψ j p.1 p.2 * star (ψ k q.1 q.2)

/-- Item (2): if `ψ_k = ∑_{l < m_k} a_{kl} ⊗ b_{kl}` (Schmidt rank at most `m_k`), then
`rank Tr₂ K_A ≤ ∑_k m_k`. Proof: `Tr₂ K_A = Ψ Y` with `Ψ` the `ι × (Σ k, Fin m_k)` matrix whose
columns are the `a_{kl}`. -/
theorem rank_ptr_le {n : ℕ} (A : Matrix (Fin n) (Fin n) ℂ) (ψ : Fin n → Matrix ι κ ℂ)
    (m : Fin n → ℕ) (a : (k : Fin n) → Fin (m k) → ι → ℂ) (b : (k : Fin n) → Fin (m k) → κ → ℂ)
    (hψ : ∀ k x z, ψ k x z = ∑ l, a k l x * b k l z) :
    (ptr (kernelA A ψ)).rank ≤ ∑ k, m k := by
  let Ψ : Matrix ι (Σ k, Fin (m k)) ℂ := fun x p => a p.1 p.2 x
  let Y : Matrix (Σ k, Fin (m k)) ι ℂ :=
    fun p y => ∑ z, ∑ k, A p.1 k * b p.1 p.2 z * star (ψ k y z)
  have hfac : ptr (kernelA A ψ) = Ψ * Y := by
    ext x y
    rw [Matrix.mul_apply, Fintype.sum_sigma]
    simp only [ptr, kernelA, hψ, Ψ, Y, Finset.sum_mul, Finset.mul_sum]
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun j _ => ?_
    conv_lhs => enter [2, z]; rw [Finset.sum_comm]
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl fun l _ => Finset.sum_congr rfl fun z _ =>
      Finset.sum_congr rfl fun k _ => ?_
    ring
  rw [hfac]
  calc (Ψ * Y).rank ≤ Ψ.rank := rank_mul_le_left _ _
    _ ≤ Fintype.card (Σ k, Fin (m k)) := rank_le_card_width _
    _ = ∑ k, m k := by simp

#print axioms trace_ptr
#print axioms ptr_isHermitian
#print axioms ptr_posSemidef
#print axioms rank_ptr_le

/-! ### Non-vacuity witnesses -/

/-- Concrete `2 × 2`-on-`Fin 2 × Fin 2` PSD matrix (identity) satisfying the hypotheses;
its partial trace is `diag(2,2)`, with trace `4 = Tr K`. -/
example : ((1 : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ)).PosSemidef ∧
    ptr (1 : Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℂ) = diagonal (fun _ => (2 : ℂ)) := by
  refine ⟨PosSemidef.one, ?_⟩
  ext x y
  fin_cases x <;> fin_cases y <;>
    simp [ptr, one_apply]

/-- Witness for (2): `n = 1`, product frame `ψ_1 = a ⊗ b` (`m_1 = 1`), `A = (1)`; hypotheses
hold and the bound gives `rank ≤ 1`. -/
example : (ptr (kernelA (1 : Matrix (Fin 1) (Fin 1) ℂ)
    (fun _ => fun x z => (if x = (0 : Fin 2) then 1 else 0) * (if z = (0 : Fin 2) then 1 else 0)))).rank
      ≤ 1 :=
  rank_ptr_le (1 : Matrix (Fin 1) (Fin 1) ℂ) _ (fun _ => 1)
    (fun _ _ x => if x = (0 : Fin 2) then 1 else 0) (fun _ _ z => if z = (0 : Fin 2) then 1 else 0)
    (fun _ _ _ => by simp)

/-! ### Mutant proved false
Mutant: "`Tr(Tr₂ K) = Tr K / dim Ω₂`" (normalized partial trace confused with the partial trace).
Refuted on `K = 1` over `Fin 1 × Fin 2`: `Tr(Tr₂ 1) = 2 ≠ 1 = 2/2`. -/
theorem mutant_trace_div_false :
    ¬ ∀ K : Matrix (Fin 1 × Fin 2) (Fin 1 × Fin 2) ℂ, (ptr K).trace = K.trace / 2 := by
  intro h
  have := h 1
  rw [trace_ptr] at this
  have h2 : (1 : Matrix (Fin 1 × Fin 2) (Fin 1 × Fin 2) ℂ).trace = 2 := by
    simp [trace_one]
  rw [h2] at this
  norm_num at this

#print axioms mutant_trace_div_false

end LeanReal.BeyondSpectrum3T1
