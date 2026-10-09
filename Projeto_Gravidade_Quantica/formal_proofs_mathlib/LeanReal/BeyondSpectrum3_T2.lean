import Mathlib.Analysis.Matrix.Order
import Mathlib.Analysis.SpecialFunctions.Log.NegMulLog

/-!
# *Beyond the Spectrum* III (Zenodo concept DOI 10.5281/zenodo.22644743), item T2

Source: `Manuscritos_Avulsos/paper_beyond_the_spectrum_3/paper_beyond_the_spectrum_3.tex`,
Theorem `thm:reflected_entropy_prop` ("OBL-015: Canonical Purification, Symmetry and the
Mutual-Information Bound for the Reflected Entropy").

Paper:
> Assume that `ρ_{Ω₁}` and `ρ_{Ω₂}` have finite rank [...] so that `H_supp^(1)` and `H_supp^(2)`
> are finite-dimensional. Let `ρ₁₂ := T_A / Tr(A)`, a density operator supported on
> `H_supp^(1) ⊗ H_supp^(2)`, and let `|√ρ₁₂⟩ ∈ (H^(1) ⊗ H^(2)) ⊗ (H^(1*) ⊗ H^(2*))` be its
> canonical GNS purification. The reflected entropy
> `S_R(Ω₁ : Ω₂) := −Tr(σ_{11*} log σ_{11*})`, `σ_{11*} := Tr_{22*}(|√ρ₁₂⟩⟨√ρ₁₂|)`
> is non-negative, symmetric `S_R(Ω₁ : Ω₂) = S_R(Ω₂ : Ω₁)`, and satisfies the universal lower
> bound `S_R(Ω₁ : Ω₂) ≥ I(Ω₁ : Ω₂) := S(Ω₁) + S(Ω₂) − S(Ω₁Ω₂)`.
> Proof: [...] `S(11*2) = S(2*) = S(2)`, so `S_R = S(11*) = I(11* : 2)`, and
> `I(11*:2) ≥ I(1:2)` by monotonicity of mutual information under discarding `1*`, which is strong
> subadditivity [Lieb–Ruskai 1973].

## Mathlib status (revision of 2026-09-19)

There is NO von Neumann entropy in Mathlib (searched: `vonNeumann`, `von Neumann entropy`,
`quantumEntropy`; the only `vonNeumann` is the ZFC hierarchy), no partial trace, and no strong
subadditivity (SSA). Available and used: `Real.negMulLog` (`-x log x`), `Matrix.charpoly`,
`Matrix.charpoly_mul_comm'` (`X^|n| χ(AB) = X^|m| χ(BA)`), `Matrix.IsHermitian.eigenvalues`,
`IsHermitian.roots_charpoly_eq_eigenvalues`, `CFC.sqrt` for matrices.

## What is formalized

1. **Entropy API.** `vnS M := ∑_{z ∈ roots(charpoly M)} negMulLog (Re z)`. For Hermitian `M`
   this is `∑ᵢ negMulLog λᵢ` (`vnS_eq_sum_eigenvalues`). Proved: invariance under unitary
   conjugation, reindexing, transposition; `vnS (AB) = vnS (BA)` for RECTANGULAR `A, B`;
   diagonal case = Shannon entropy; `0 ≤ S(ρ) ≤ log n` for density matrices.
2. **Pure-state lemma.** For any vector `ψ` on `a × b`, the two reduced states of `|ψ⟩⟨ψ|` have
   the same entropy (`pure_marginals_entropy_eq`).
3. **Reflected entropy.** `σ_{11*}` is defined from `CFC.sqrt ρ` exactly as in the paper
   (and shown to equal `Tr_{22*}|√ρ⟩⟨√ρ|`). Proved: `σ_{11*}` is a density matrix, `S_R ≥ 0`,
   `S_R ≤ 2 log |ι|`, and the SYMMETRY `S_R(ρ) = S_R(swap ρ)` (unconditional).
4. **The bound `S_R ≥ I`.** Proved unconditionally: `S_R = I(11* : 2)` for the purified state
   (the identity `S(11*2) = S(2)` included). The inequality itself is proved CONDITIONALLY on
   strong subadditivity, which enters as an explicit hypothesis `SSA ι ι κ` (a `Prop` stating
   Lieb–Ruskai for every density matrix on `ι × ι × κ`); it is NOT an axiom and NOT proved here.

## REDUCTION (declared)

* Only the finite-dimensional setting: `H^(1) = ℂ^ι`, `H^(2) = ℂ^κ`; `ρ` is ANY density matrix
  on `ι × κ` (the construction `ρ₁₂ = T_A / Tr A` from the kernel is not re-done).
* The canonical purification is taken in the convention
  `|√ρ⟩ = ∑_{x,y} (√ρ)_{x y} |x⟩ ⊗ |y⟩`, `x, y ∈ ι × κ`; other conventions (complex conjugation
  on the starred copy) give unitarily equivalent reduced states, not proved here.
* **SSA is missing** from Mathlib; the inequality `S_R ≥ I` is therefore conditional
  (`reflected_ge_mutualInfo_of_SSA`). A proof of SSA (Lieb concavity / operator convexity,
  or Petz recoverability) is far beyond the current matrix-analysis API.
-/

namespace LeanReal.BeyondSpectrum3T2

open Matrix Polynomial Real
open scoped ComplexOrder MatrixOrder

/-! ## 1. Entropy API -/

section Entropy

variable {n m : Type*} [Fintype n] [DecidableEq n] [Fintype m] [DecidableEq m]

/-- Von Neumann entropy through the characteristic polynomial: `∑_{roots z} −Re z log Re z`. -/
noncomputable def vnS (M : Matrix n n ℂ) : ℝ :=
  (M.charpoly.roots.map (fun z : ℂ => negMulLog z.re)).sum

/-- If `χ_M = ∏ᵢ (X − qᵢ)` with `qᵢ` real, then `vnS M = ∑ᵢ negMulLog qᵢ`. -/
theorem vnS_of_charpoly_prod {M : Matrix n n ℂ} (q : n → ℝ)
    (h : M.charpoly = ∏ i, (X - C (q i : ℂ))) : vnS M = ∑ i, negMulLog (q i) := by
  rw [vnS, h, roots_prod _ _ (by simp [Finset.prod_ne_zero_iff, X_sub_C_ne_zero])]
  simp only [roots_X_sub_C, Multiset.bind_singleton, Multiset.map_map, Function.comp_def,
    Complex.ofReal_re]
  rfl

theorem vnS_eq_sum_eigenvalues {A : Matrix n n ℂ} (hA : A.IsHermitian) :
    vnS A = ∑ i, negMulLog (hA.eigenvalues i) :=
  vnS_of_charpoly_prod _ hA.charpoly_eq

theorem vnS_of_charpoly_eq {A : Matrix n n ℂ} {B : Matrix m m ℂ}
    (h : A.charpoly = B.charpoly) : vnS A = vnS B := by
  simp only [vnS, h]

theorem vnS_transpose (A : Matrix n n ℂ) : vnS Aᵀ = vnS A :=
  vnS_of_charpoly_eq (charpoly_transpose A)

theorem vnS_reindex (e : n ≃ m) (A : Matrix n n ℂ) : vnS (reindex e e A) = vnS A :=
  vnS_of_charpoly_eq (charpoly_reindex e A)

/-- `vnS (A B) = vnS (B A)` for rectangular `A : m × n`, `B : n × m`
(the extra zero eigenvalues contribute `negMulLog 0 = 0`). -/
theorem vnS_mul_comm (A : Matrix m n ℂ) (B : Matrix n m ℂ) : vnS (A * B) = vnS (B * A) := by
  have h := charpoly_mul_comm' A B
  have hr := congrArg Polynomial.roots h
  rw [roots_mul (by
        exact mul_ne_zero (pow_ne_zero _ X_ne_zero) (charpoly_monic _).ne_zero),
      roots_mul (by
        exact mul_ne_zero (pow_ne_zero _ X_ne_zero) (charpoly_monic _).ne_zero),
      roots_X_pow, roots_X_pow] at hr
  have hs := congrArg (fun s : Multiset ℂ => (s.map (fun z : ℂ => negMulLog z.re)).sum) hr
  simpa [vnS, Multiset.map_add, Multiset.sum_add, Multiset.map_nsmul, Multiset.sum_nsmul] using hs

/-- Unitary invariance. -/
theorem vnS_unitary_conj (U : Matrix n n ℂ) (hU : U ∈ unitaryGroup n ℂ) (A : Matrix n n ℂ) :
    vnS (U * A * star U) = vnS A := by
  rw [vnS_mul_comm (U * A) (star U), ← Matrix.mul_assoc,
    (Matrix.mem_unitaryGroup_iff').mp hU, Matrix.one_mul]

/-- Diagonal case: the von Neumann entropy of `diag p` is the Shannon entropy of `p`. -/
theorem vnS_diagonal (p : n → ℝ) :
    vnS (diagonal fun i => (p i : ℂ)) = ∑ i, negMulLog (p i) :=
  vnS_of_charpoly_prod p (charpoly_diagonal _)

/-- Density matrices: positive semidefinite with unit trace. -/
def IsDensity (ρ : Matrix n n ℂ) : Prop := ρ.PosSemidef ∧ ρ.trace = 1

theorem IsDensity.eigenvalues_le_one {ρ : Matrix n n ℂ} (hρ : IsDensity ρ) (i : n) :
    hρ.1.isHermitian.eigenvalues i ≤ 1 := by
  have hsum : ∑ j, hρ.1.isHermitian.eigenvalues j = 1 := by
    have h := hρ.1.isHermitian.trace_eq_sum_eigenvalues
    have h' := congrArg Complex.re (h.symm.trans hρ.2)
    simpa [Complex.re_sum] using h'
  rw [← hsum]
  exact Finset.single_le_sum (fun j _ => hρ.1.eigenvalues_nonneg j) (Finset.mem_univ i)

/-- `S(ρ) ≥ 0`. -/
theorem vnS_nonneg {ρ : Matrix n n ℂ} (hρ : IsDensity ρ) : 0 ≤ vnS ρ := by
  rw [vnS_eq_sum_eigenvalues hρ.1.isHermitian]
  exact Finset.sum_nonneg fun i _ =>
    negMulLog_nonneg (hρ.1.eigenvalues_nonneg i) (hρ.eigenvalues_le_one i)

/-- Scalar lemma for the `log n` bound: `negMulLog x ≤ x log N + 1/N − x` for `x ≥ 0`, `N > 0`. -/
theorem negMulLog_le_aux {x N : ℝ} (hx : 0 ≤ x) (hN : 0 < N) :
    negMulLog x ≤ x * Real.log N + 1 / N - x := by
  rcases hx.eq_or_lt with rfl | hx
  · simp [hN.le]
  · have hNx : 0 < N * x := mul_pos hN hx
    have hlog := Real.one_sub_inv_le_log_of_pos hNx
    rw [Real.log_mul hN.ne' hx.ne'] at hlog
    have : x * (1 - (N * x)⁻¹) = x - 1 / N := by field_simp
    rw [negMulLog]
    nlinarith [mul_le_mul_of_nonneg_left hlog hx.le]

/-- `S(ρ) ≤ log n`. -/
theorem vnS_le_log_card {ρ : Matrix n n ℂ} (hρ : IsDensity ρ) :
    vnS ρ ≤ Real.log (Fintype.card n) := by
  have hsum : ∑ j, hρ.1.isHermitian.eigenvalues j = 1 := by
    have h := hρ.1.isHermitian.trace_eq_sum_eigenvalues
    have h' := congrArg Complex.re (h.symm.trans hρ.2)
    simpa [Complex.re_sum] using h'
  have hN : 0 < (Fintype.card n : ℝ) := by
    rcases isEmpty_or_nonempty n with hn | hn
    · simp at hsum
    · exact_mod_cast Fintype.card_pos
  rw [vnS_eq_sum_eigenvalues hρ.1.isHermitian]
  calc ∑ i, negMulLog (hρ.1.isHermitian.eigenvalues i)
      ≤ ∑ i, (hρ.1.isHermitian.eigenvalues i * Real.log (Fintype.card n)
          + 1 / (Fintype.card n) - hρ.1.isHermitian.eigenvalues i) :=
        Finset.sum_le_sum fun i _ => negMulLog_le_aux (hρ.1.eigenvalues_nonneg i) hN
    _ = Real.log (Fintype.card n) := by
        rw [Finset.sum_sub_distrib, Finset.sum_add_distrib, ← Finset.sum_mul, hsum]
        have h1 : (∑ _i : n, 1 / (Fintype.card n : ℝ)) = 1 := by
          rw [Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
          field_simp
        rw [h1]
        ring

end Entropy

/-! ## 2. Partial traces and the pure-state lemma -/

section Pure

variable {a b c : Type*} [Fintype a] [DecidableEq a] [Fintype b] [DecidableEq b]
  [Fintype c] [DecidableEq c]

/-- Partial trace over the second factor, `Tr_b`. -/
def ptr2 (M : Matrix (a × b) (a × b) ℂ) : Matrix a a ℂ := fun x y => ∑ z, M (x, z) (y, z)

/-- Partial trace over the first factor, `Tr_a`. -/
def ptr1 (M : Matrix (a × b) (a × b) ℂ) : Matrix b b ℂ := fun x y => ∑ z, M (z, x) (z, y)

/-- Partial trace over the MIDDLE factor of `(a × b) × c`, giving the `ac` marginal. -/
def trMid (M : Matrix ((a × b) × c) ((a × b) × c) ℂ) : Matrix (a × c) (a × c) ℂ :=
  fun x y => ∑ z, M ((x.1, z), x.2) ((y.1, z), y.2)

/-- The rank-one operator `|v⟩⟨v|`. -/
def proj {d : Type*} (v : d → ℂ) : Matrix d d ℂ := vecMulVec v (star v)

/-- Coefficient matrix of a vector on `a × b`. -/
def coef (v : a × b → ℂ) : Matrix a b ℂ := of fun x y => v (x, y)

omit [Fintype a] [DecidableEq a] [DecidableEq b] in
theorem ptr2_proj (v : a × b → ℂ) : ptr2 (proj v) = coef v * (coef v)ᴴ := by
  ext x y
  simp [ptr2, proj, coef, vecMulVec_apply, mul_apply]

omit [DecidableEq a] [Fintype b] [DecidableEq b] in
theorem ptr1_proj (v : a × b → ℂ) : ptr1 (proj v) = ((coef v)ᴴ * coef v)ᵀ := by
  ext x y
  simp [ptr1, proj, coef, vecMulVec_apply, mul_apply, mul_comm]

/-- **Pure-state lemma.** For a pure state `|v⟩⟨v|` on `a × b`, the two marginals have the same
von Neumann entropy (they have the same non-zero spectrum). -/
theorem pure_marginals_entropy_eq (v : a × b → ℂ) :
    vnS (ptr2 (proj v)) = vnS (ptr1 (proj v)) := by
  rw [ptr2_proj, ptr1_proj, vnS_transpose, vnS_mul_comm]

/-- `Tr (M Mᴴ) = ∑ |Mₓᵧ|²` (as a sum over the product index). -/
theorem trace_mul_conjTranspose_self {d e : Type*} [Fintype d] [Fintype e] (M : Matrix d e ℂ) :
    (M * Mᴴ).trace = ∑ p : d × e, M p.1 p.2 * star (M p.1 p.2) := by
  simp [trace, mul_apply, Fintype.sum_prod_type]

end Pure

/-! ## 3. Reflected entropy -/

section Reflected

variable {ι κ : Type*} [Fintype ι] [DecidableEq ι] [Fintype κ] [DecidableEq κ]

/-- The canonical purification `|√ρ⟩`, with components
`Ψ((i, i'), (k, k')) = (√ρ)_{(i,k),(i',k')}`: the factors are regrouped as `(1 1*) (2 2*)`. -/
noncomputable def purif (ρ : Matrix (ι × κ) (ι × κ) ℂ) : (ι × ι) × (κ × κ) → ℂ :=
  fun p => CFC.sqrt ρ (p.1.1, p.2.1) (p.1.2, p.2.2)

/-- `σ_{11*} = Tr_{22*} |√ρ⟩⟨√ρ|`. -/
noncomputable def sigma11 (ρ : Matrix (ι × κ) (ι × κ) ℂ) : Matrix (ι × ι) (ι × ι) ℂ :=
  ptr2 (proj (purif ρ))

/-- Reflected entropy `S_R(1 : 2) = S(σ_{11*})`. -/
noncomputable def SR (ρ : Matrix (ι × κ) (ι × κ) ℂ) : ℝ := vnS (sigma11 ρ)

/-- Mutual information `I(1 : 2) = S(1) + S(2) − S(12)`. -/
noncomputable def mutualInfo (ρ : Matrix (ι × κ) (ι × κ) ℂ) : ℝ :=
  vnS (ptr2 ρ) + vnS (ptr1 ρ) - vnS ρ

/-- The swapped state on `κ × ι` (roles of `Ω₁`, `Ω₂` exchanged). -/
def swapM (ρ : Matrix (ι × κ) (ι × κ) ℂ) : Matrix (κ × ι) (κ × ι) ℂ :=
  ρ.submatrix (Equiv.prodComm κ ι) (Equiv.prodComm κ ι)

section sqrtFacts

variable {ρ : Matrix (ι × κ) (ι × κ) ℂ}

theorem sqrt_herm (ρ : Matrix (ι × κ) (ι × κ) ℂ) : (CFC.sqrt ρ)ᴴ = CFC.sqrt ρ :=
  (CFC.sqrt_nonneg ρ).posSemidef.isHermitian

theorem sqrt_mul_sqrt (hρ : ρ.PosSemidef) : CFC.sqrt ρ * CFC.sqrt ρ = ρ :=
  CFC.sqrt_mul_sqrt_self ρ hρ.nonneg

/-- `ρ = S Sᴴ`, entrywise. -/
theorem rho_apply_eq (hρ : ρ.PosSemidef) (x y : ι × κ) :
    ρ x y = ∑ z, CFC.sqrt ρ x z * star (CFC.sqrt ρ y z) := by
  conv_lhs => rw [← sqrt_mul_sqrt hρ]
  rw [mul_apply]
  refine Finset.sum_congr rfl fun z _ => ?_
  congr 1
  have := congrFun (congrFun (sqrt_herm ρ) z) y
  rw [conjTranspose_apply] at this
  exact this.symm

end sqrtFacts

theorem coef_purif (ρ : Matrix (ι × κ) (ι × κ) ℂ) :
    coef (purif ρ) = of fun (x : ι × ι) (y : κ × κ) => CFC.sqrt ρ (x.1, y.1) (x.2, y.2) := rfl

/-- `Tr σ_{11*} = Tr ρ`. -/
theorem trace_sigma11 {ρ : Matrix (ι × κ) (ι × κ) ℂ} (hρ : ρ.PosSemidef) :
    (sigma11 ρ).trace = ρ.trace := by
  rw [sigma11, ptr2_proj, trace_mul_conjTranspose_self]
  have h : ρ.trace = (CFC.sqrt ρ * (CFC.sqrt ρ)ᴴ).trace := by rw [sqrt_herm, sqrt_mul_sqrt hρ]
  rw [h, trace_mul_conjTranspose_self]
  exact Fintype.sum_equiv (Equiv.prodProdProdComm ι ι κ κ) _ _ (fun p => rfl)

/-- `σ_{11*}` is a density matrix. -/
theorem sigma11_isDensity {ρ : Matrix (ι × κ) (ι × κ) ℂ} (hρ : IsDensity ρ) :
    IsDensity (sigma11 ρ) := by
  refine ⟨?_, (trace_sigma11 hρ.1).trans hρ.2⟩
  rw [sigma11, ptr2_proj]
  exact posSemidef_self_mul_conjTranspose _

/-- **Non-negativity** `S_R ≥ 0`. -/
theorem SR_nonneg {ρ : Matrix (ι × κ) (ι × κ) ℂ} (hρ : IsDensity ρ) : 0 ≤ SR ρ :=
  vnS_nonneg (sigma11_isDensity hρ)

/-- Upper bound `S_R ≤ 2 log |ι|`. -/
theorem SR_le {ρ : Matrix (ι × κ) (ι × κ) ℂ} (hρ : IsDensity ρ) :
    SR ρ ≤ 2 * Real.log (Fintype.card ι) := by
  have h := vnS_le_log_card (sigma11_isDensity hρ)
  rcases isEmpty_or_nonempty ι with hι | hι
  · simp [SR] at h ⊢
    simpa using h
  have hc : (0 : ℝ) < Fintype.card ι := by exact_mod_cast Fintype.card_pos
  rw [Fintype.card_prod, Nat.cast_mul, Real.log_mul hc.ne' hc.ne'] at h
  unfold SR; linarith

/-- `√(swap ρ) = swap (√ρ)` (uniqueness of the positive square root). -/
theorem sqrt_swapM {ρ : Matrix (ι × κ) (ι × κ) ℂ} (hρ : ρ.PosSemidef) :
    CFC.sqrt (swapM ρ) = swapM (CFC.sqrt ρ) := by
  apply CFC.sqrt_unique
  · rw [swapM, swapM, submatrix_mul_equiv, sqrt_mul_sqrt hρ]
  · exact ((CFC.sqrt_nonneg ρ).posSemidef.submatrix _).nonneg

/-- **Symmetry** `S_R(Ω₁ : Ω₂) = S_R(Ω₂ : Ω₁)`. -/
theorem SR_swap {ρ : Matrix (ι × κ) (ι × κ) ℂ} (hρ : ρ.PosSemidef) :
    SR (swapM ρ) = SR ρ := by
  have hC : coef (purif (swapM ρ)) = (coef (purif ρ))ᵀ := by
    ext x y
    simp only [coef, purif, of_apply, transpose_apply]
    rw [sqrt_swapM hρ]
    simp [swapM]
  rw [SR, SR, sigma11, sigma11, ptr2_proj, ptr2_proj, hC, vnS_mul_comm]
  rw [← vnS_transpose (coef (purif ρ) * (coef (purif ρ))ᴴ)]
  congr 1
  ext x y
  simp [mul_apply, mul_comm]

end Reflected

/-! ## 4. `S_R = I(11* : 2)` and the bound `S_R ≥ I(1 : 2)` conditional on SSA -/

section Bound

variable {ι κ : Type*} [Fintype ι] [DecidableEq ι] [Fintype κ] [DecidableEq κ]

/-- **Strong subadditivity** (Lieb–Ruskai 1973) for density matrices on `(a × b) × c`, in the form
`S(abc) + S(a) ≤ S(ab) + S(ac)`. NOT proved here (absent from Mathlib); used only as an explicit
hypothesis. -/
def SSA (a b c : Type*) [Fintype a] [DecidableEq a] [Fintype b] [DecidableEq b]
    [Fintype c] [DecidableEq c] : Prop :=
  ∀ τ : Matrix ((a × b) × c) ((a × b) × c) ℂ, IsDensity τ →
    vnS τ + vnS (ptr2 (ptr2 τ)) ≤ vnS (ptr2 τ) + vnS (trMid τ)

/-- The purification `|√ρ⟩` regrouped as `((1 1*) 2) 2*`. -/
noncomputable def purif3 (ρ : Matrix (ι × κ) (ι × κ) ℂ) : ((ι × ι) × κ) × κ → ℂ :=
  fun p => CFC.sqrt ρ (p.1.1.1, p.1.2) (p.1.1.2, p.2)

/-- The reduced state on `1 1* 2`: `τ = Tr_{2*} |√ρ⟩⟨√ρ|`. -/
noncomputable def tau (ρ : Matrix (ι × κ) (ι × κ) ℂ) : Matrix ((ι × ι) × κ) ((ι × ι) × κ) ℂ :=
  ptr2 (proj (purif3 ρ))

variable {ρ : Matrix (ι × κ) (ι × κ) ℂ}

/-- `τ` is a density matrix. -/
theorem tau_isDensity (hρ : IsDensity ρ) : IsDensity (tau ρ) := by
  refine ⟨?_, ?_⟩
  · rw [tau, ptr2_proj]; exact posSemidef_self_mul_conjTranspose _
  · rw [tau, ptr2_proj, trace_mul_conjTranspose_self, ← hρ.2]
    have h : ρ.trace = (CFC.sqrt ρ * (CFC.sqrt ρ)ᴴ).trace := by
      rw [sqrt_herm, sqrt_mul_sqrt hρ.1]
    rw [h, trace_mul_conjTranspose_self]
    exact Fintype.sum_equiv
      ((Equiv.prodAssoc (ι × ι) κ κ).trans (Equiv.prodProdProdComm ι ι κ κ)) _ _ (fun p => rfl)

/-- Marginal of `τ` on `1 1*` is `σ_{11*}`. -/
theorem ptr2_tau : ptr2 (tau ρ) = sigma11 ρ := by
  ext x y
  simp [tau, sigma11, ptr2, proj, purif3, purif, vecMulVec_apply, Fintype.sum_prod_type]

/-- Marginal of `τ` on `1 2` is `ρ` itself. -/
theorem trMid_tau (hρ : ρ.PosSemidef) : trMid (tau ρ) = ρ := by
  ext x y
  rw [rho_apply_eq hρ x y]
  simp [tau, trMid, ptr2, proj, purif3, vecMulVec_apply, Fintype.sum_prod_type]

/-- Marginal of `τ` on `1` is `ρ₁ = Tr₂ ρ`. -/
theorem ptr2_ptr2_tau (hρ : ρ.PosSemidef) : ptr2 (ptr2 (tau ρ)) = ptr2 ρ := by
  ext i j
  simp only [ptr2]
  simp_rw [rho_apply_eq hρ]
  simp only [tau, ptr2, proj, purif3, vecMulVec_apply, Pi.star_apply, Fintype.sum_prod_type]
  exact Finset.sum_comm

/-- Marginal of `τ` on `2` is `ρ₂ = Tr₁ ρ`. -/
theorem ptr1_tau (hρ : ρ.PosSemidef) : ptr1 (tau ρ) = ptr1 ρ := by
  ext k l
  simp only [ptr1]
  simp_rw [rho_apply_eq hρ]
  simp [tau, ptr2, proj, purif3, vecMulVec_apply, Fintype.sum_prod_type]

/-- `S(1 1* 2) = S(2)` (the paper's `S(11*2) = S(2*) = S(2)`). -/
theorem vnS_tau (hρ : ρ.PosSemidef) : vnS (tau ρ) = vnS (ptr1 ρ) := by
  rw [tau, pure_marginals_entropy_eq, ← vnS_transpose (ptr1 ρ)]
  congr 1
  ext k l
  simp only [ptr1, transpose_apply]
  simp_rw [rho_apply_eq hρ]
  simp only [proj, purif3, vecMulVec_apply, Pi.star_apply, Fintype.sum_prod_type]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun i' _ =>
    Finset.sum_congr rfl fun k' _ => ?_
  have h1 := congrFun (congrFun (sqrt_herm ρ) (i', k')) (i, k)
  have h2 := congrFun (congrFun (sqrt_herm ρ) (i, l)) (i', k')
  rw [conjTranspose_apply] at h1 h2
  rw [← h1, h2, mul_comm]

/-- **`S_R = I(11* : 2)`** for the purified state (unconditional): `S_R = S(11*) + S(2) − S(11*2)`,
where `τ` is the `11*2` marginal of `|√ρ⟩⟨√ρ|` and its `2` marginal is `Tr₁ ρ`. -/
theorem SR_eq_mutualInfo_purif (hρ : ρ.PosSemidef) :
    SR ρ = vnS (ptr2 (tau ρ)) + vnS (ptr1 (tau ρ)) - vnS (tau ρ) := by
  rw [ptr2_tau, ptr1_tau hρ, vnS_tau hρ, SR]
  ring

/-- **The mutual-information bound** `S_R(Ω₁ : Ω₂) ≥ I(Ω₁ : Ω₂)`, CONDITIONAL on strong
subadditivity (explicit hypothesis `hSSA`, not proved in Lean). -/
theorem reflected_ge_mutualInfo_of_SSA (hSSA : SSA ι ι κ) (hρ : IsDensity ρ) :
    mutualInfo ρ ≤ SR ρ := by
  have h := hSSA (tau ρ) (tau_isDensity hρ)
  rw [ptr2_ptr2_tau hρ.1, ptr2_tau, trMid_tau hρ.1, vnS_tau hρ.1] at h
  unfold mutualInfo SR
  linarith

end Bound

/-! ## 5. Non-vacuity witness and mutants proved false -/

section Witness

/-- `ρ₀ = 1 ⊗ (I/2)` on `ℂ¹ ⊗ ℂ²` (diagonal with entries `1/2`). -/
noncomputable def rho0 : Matrix (Fin 1 × Fin 2) (Fin 1 × Fin 2) ℂ :=
  diagonal fun _ => ((1 / 2 : ℝ) : ℂ)

theorem rho0_isDensity : IsDensity rho0 := by
  refine ⟨?_, ?_⟩
  · rw [rho0, posSemidef_diagonal_iff]
    intro i
    exact_mod_cast (by norm_num : (0 : ℝ) ≤ 1 / 2)
  · simp [rho0, trace_diagonal]

theorem negMulLog_half : negMulLog (2⁻¹ : ℝ) = Real.log 2 / 2 := by
  simp [negMulLog, Real.log_inv]
  ring

theorem vnS_rho0 : vnS rho0 = Real.log 2 := by
  rw [rho0, vnS_diagonal]
  simp only [one_div, Finset.sum_const, Finset.card_univ, Fintype.card_prod, Fintype.card_fin,
    negMulLog_half, nsmul_eq_mul]
  push_cast
  ring

theorem ptr1_rho0 : ptr1 rho0 = diagonal fun _ : Fin 2 => ((1 / 2 : ℝ) : ℂ) := by
  ext k l
  by_cases h : k = l
  · subst h; simp [ptr1, rho0]
  · simp [ptr1, rho0, h]

theorem ptr2_rho0 : ptr2 rho0 = diagonal fun _ : Fin 1 => ((1 : ℝ) : ℂ) := by
  ext i j
  have hij : i = j := Subsingleton.elim i j
  subst hij
  simp [ptr2, rho0]

theorem vnS_ptr1_rho0 : vnS (ptr1 rho0) = Real.log 2 := by
  rw [ptr1_rho0, vnS_diagonal]
  simp only [one_div, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    negMulLog_half, nsmul_eq_mul]
  push_cast
  ring

theorem vnS_ptr2_rho0 : vnS (ptr2 rho0) = 0 := by
  rw [ptr2_rho0, vnS_diagonal]
  simp

theorem SR_rho0 : SR rho0 = 0 := by
  have h1 := SR_nonneg rho0_isDensity
  have h2 := SR_le rho0_isDensity
  simp at h2
  linarith

/-- Non-vacuity: `ρ₀` satisfies every hypothesis of the unconditional results, and the quantities
are computed: `S_R(ρ₀) = 0 = I(ρ₀)`, `S(ρ₁) = 0`, `S(ρ₂) = S(ρ₁₂) = log 2`. -/
theorem witness :
    IsDensity rho0 ∧ SR rho0 = 0 ∧ mutualInfo rho0 = 0 ∧ vnS (ptr1 rho0) = Real.log 2 := by
  refine ⟨rho0_isDensity, SR_rho0, ?_, vnS_ptr1_rho0⟩
  rw [mutualInfo, vnS_ptr2_rho0, vnS_ptr1_rho0, vnS_rho0]
  ring

/-- **Mutant 1 proved false.** Dropping `−S(Ω₁Ω₂)` from the mutual information, i.e. claiming
`S_R ≥ S(Ω₁) + S(Ω₂)`, fails at `ρ₀`: it would give `0 ≥ log 2`. -/
theorem mutant_drop_joint_false :
    ¬ ∀ ρ : Matrix (Fin 1 × Fin 2) (Fin 1 × Fin 2) ℂ, IsDensity ρ →
      vnS (ptr2 ρ) + vnS (ptr1 ρ) ≤ SR ρ := by
  intro h
  have := h rho0 rho0_isDensity
  rw [vnS_ptr2_rho0, vnS_ptr1_rho0, SR_rho0] at this
  have : (0 : ℝ) < Real.log 2 := Real.log_pos (by norm_num)
  linarith

/-- **Mutant 2 proved false.** Non-negativity needs unit trace: `diag(2)` is positive
semidefinite and `S = −2 log 2 < 0`. -/
theorem mutant_nonneg_without_trace_false :
    ¬ ∀ M : Matrix (Fin 1) (Fin 1) ℂ, M.PosSemidef → 0 ≤ vnS M := by
  intro h
  have hpsd : (diagonal fun _ : Fin 1 => ((2 : ℝ) : ℂ)).PosSemidef := by
    rw [posSemidef_diagonal_iff]
    intro i
    exact_mod_cast (by norm_num : (0 : ℝ) ≤ 2)
  have := h _ hpsd
  rw [vnS_diagonal] at this
  simp [negMulLog] at this
  have : (0 : ℝ) < Real.log 2 := Real.log_pos (by norm_num)
  linarith

end Witness

end LeanReal.BeyondSpectrum3T2

#print axioms LeanReal.BeyondSpectrum3T2.vnS_unitary_conj
#print axioms LeanReal.BeyondSpectrum3T2.vnS_mul_comm
#print axioms LeanReal.BeyondSpectrum3T2.vnS_diagonal
#print axioms LeanReal.BeyondSpectrum3T2.vnS_nonneg
#print axioms LeanReal.BeyondSpectrum3T2.vnS_le_log_card
#print axioms LeanReal.BeyondSpectrum3T2.pure_marginals_entropy_eq
#print axioms LeanReal.BeyondSpectrum3T2.sigma11_isDensity
#print axioms LeanReal.BeyondSpectrum3T2.SR_nonneg
#print axioms LeanReal.BeyondSpectrum3T2.SR_le
#print axioms LeanReal.BeyondSpectrum3T2.SR_swap
#print axioms LeanReal.BeyondSpectrum3T2.SR_eq_mutualInfo_purif
#print axioms LeanReal.BeyondSpectrum3T2.reflected_ge_mutualInfo_of_SSA
#print axioms LeanReal.BeyondSpectrum3T2.witness
#print axioms LeanReal.BeyondSpectrum3T2.mutant_drop_joint_false
#print axioms LeanReal.BeyondSpectrum3T2.mutant_nonneg_without_trace_false
