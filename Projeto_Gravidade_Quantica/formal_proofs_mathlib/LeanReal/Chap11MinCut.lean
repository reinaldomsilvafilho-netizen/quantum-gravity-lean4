import LeanReal.BeyondSpectrum3_T2

/-!
# Chapter 11, `prop:mincut` (book plan item 11.4, batch B7)

Source: `unified_quantum_gravity_book/chap11_emergent_spacetime_tensor_networks_holonomies.tex`,
Proposition "Min-cut bound" (`prop:mincut`):

> Let `|Ψ⟩` be a tensor network state on a graph whose internal bonds have dimension `χ`, and let
> `A` be a set of open legs. For every cut `C` (set of bonds) separating `A` from its complement,
> `S_A ≤ |C| log χ`. Hence `S_A ≤ log χ · min_C |C|`.
> Proof: contracting the network on each side of `C` writes
> `|Ψ⟩ = ∑_{α ∈ [χ]^{|C|}} |φ_α⟩_A ⊗ |ψ_α⟩_{Ā}`, so the Schmidt rank across `A : Ā` is at most
> `χ^{|C|}`, and the von Neumann entropy is at most the logarithm of the Schmidt rank.

## Declared reduction

* Finite dimensions: `H_A = ℂ^a`, `H_Ā = ℂ^b`; `|Ψ⟩` is a vector `v : a × b → ℂ` with
  `∑ |v|² = 1` (the book silently assumes a normalised state; mutant 2 shows this is needed).
* The tensor network itself (a graph and its contraction) is NOT modelled. What the book's proof
  extracts from the contraction on each side of the cut, namely the factorisation
  `|Ψ⟩ = ∑_α |φ_α⟩ ⊗ |ψ_α⟩` over an index set of size `χ^{|C|}`, enters as data: the coefficient
  matrix factors as `coef v = U V` with `U : a × r`, `V : r × b`, `|r| = χ^{|C|}`
  (`U_{xα} = ⟨x|φ_α⟩`, `V_{αy} = ⟨y|ψ_α⟩`). This is a modelling reduction, not a missing
  classical fact; no extra hypothesis stands in for missing theory.
* `S_A` is the entropy `vnS` of `ρ_A = Tr_Ā |Ψ⟩⟨Ψ|` from `BeyondSpectrum3_T2` (sum of
  `negMulLog` over the roots of the characteristic polynomial).
* Proof used (equivalent to the book's Schmidt-rank argument): with `S = (V Vᴴ)^{1/2}`,
  `ρ_A = (U S)(U S)ᴴ`, so `S(ρ_A) = S((U S)ᴴ(U S))`, the entropy of a density matrix of size `|r|`,
  which is at most `log |r|`.

## Main statements

* `vnS_marginal_le_log_card_of_factor`: `S(ρ_A) ≤ log |r|` whenever `coef v = U V` through `r`.
* `mincut_bound`: `S_A ≤ |C| log χ` for a cut of size `k = |C|` (`|r| = χ^k`).
* `mincut_bound_min`: `S_A ≤ log χ · min_C |C|` over a nonempty finite family of cuts.
* Witness: the Bell state, `S_A = log 2 = 1 · log 2` (the bound is attained).
* Mutants proved false: the bound with `|C| = 0` (no cut), and the bound without normalisation.
-/

namespace LeanReal.Chap11MinCut

open Matrix Real LeanReal.BeyondSpectrum3T2
open scoped ComplexOrder MatrixOrder

variable {a b r : Type*} [Fintype a] [DecidableEq a] [Fintype b] [DecidableEq b]
  [Fintype r] [DecidableEq r]

omit [DecidableEq a] [DecidableEq b] [Fintype r] [DecidableEq r] in
/-- The norm condition `∑ |v_p|² = 1` gives `Tr ρ_A = 1`. -/
theorem trace_ptr2_proj (v : a × b → ℂ) :
    (ptr2 (proj v)).trace = ∑ p, v p * star (v p) := by
  rw [ptr2_proj, trace_mul_conjTranspose_self]
  rfl

omit [DecidableEq a] [DecidableEq b] [Fintype r] [DecidableEq r] in
/-- The reduced state `ρ_A = Tr_Ā |v⟩⟨v|` of a normalised vector is a density matrix. -/
theorem ptr2_proj_isDensity {v : a × b → ℂ} (hv : ∑ p, v p * star (v p) = 1) :
    IsDensity (ptr2 (proj v)) := by
  refine ⟨?_, by rw [trace_ptr2_proj, hv]⟩
  rw [ptr2_proj]
  exact posSemidef_self_mul_conjTranspose _

omit [DecidableEq b] in
/-- **Schmidt-rank bound** (the core of `prop:mincut`): if the coefficient matrix of the
normalised state `v` on `a × b` factors through an index set `r`, `coef v = U V`, then
`S(ρ_A) ≤ log |r|`. -/
theorem vnS_marginal_le_log_card_of_factor {v : a × b → ℂ} (hv : ∑ p, v p * star (v p) = 1)
    (U : Matrix a r ℂ) (V : Matrix r b ℂ) (hUV : coef v = U * V) :
    vnS (ptr2 (proj v)) ≤ Real.log (Fintype.card r) := by
  set W : Matrix r r ℂ := V * Vᴴ with hW
  have hWpsd : W.PosSemidef := posSemidef_self_mul_conjTranspose V
  set S : Matrix r r ℂ := CFC.sqrt W with hS
  have hSS : S * S = W := CFC.sqrt_mul_sqrt_self W hWpsd.nonneg
  have hSh : Sᴴ = S := (CFC.sqrt_nonneg W).posSemidef.isHermitian
  have hρ : ptr2 (proj v) = (U * S) * (U * S)ᴴ := by
    rw [ptr2_proj, hUV, conjTranspose_mul, conjTranspose_mul, hSh]
    calc U * V * (Vᴴ * Uᴴ) = U * (V * Vᴴ) * Uᴴ := by simp only [Matrix.mul_assoc]
      _ = U * (S * S) * Uᴴ := by rw [hSS]
      _ = U * S * (S * Uᴴ) := by simp only [Matrix.mul_assoc]
  have hdens : IsDensity ((U * S)ᴴ * (U * S)) := by
    refine ⟨posSemidef_conjTranspose_mul_self _, ?_⟩
    rw [trace_mul_comm, ← hρ]
    exact (ptr2_proj_isDensity hv).2
  rw [hρ, vnS_mul_comm]
  exact vnS_le_log_card hdens

omit [DecidableEq b] in
/-- **`prop:mincut`, first statement**: `S_A ≤ |C| log χ`. A cut with `k = |C|` bonds of
dimension `χ` gives the factorisation `coef v = U V` through an index set of size `χ^k`. -/
theorem mincut_bound {v : a × b → ℂ} (hv : ∑ p, v p * star (v p) = 1) (χ k : ℕ)
    (hr : Fintype.card r = χ ^ k)
    (U : Matrix a r ℂ) (V : Matrix r b ℂ) (hUV : coef v = U * V) :
    vnS (ptr2 (proj v)) ≤ k * Real.log χ := by
  have h := vnS_marginal_le_log_card_of_factor hv U V hUV
  rwa [hr, Nat.cast_pow, Real.log_pow] at h

omit [DecidableEq b] [Fintype r] [DecidableEq r] in
/-- **`prop:mincut`, "hence"**: `S_A ≤ log χ · min_C |C|`, over a nonempty finite family of cuts,
each of which yields a factorisation through `[χ]^{|C|}`. -/
theorem mincut_bound_min {ι : Type*} {v : a × b → ℂ} (hv : ∑ p, v p * star (v p) = 1) (χ : ℕ)
    (cuts : Finset ι) (hne : cuts.Nonempty) (size : ι → ℕ)
    (hfac : ∀ C ∈ cuts, ∃ U : Matrix a (Fin (χ ^ size C)) ℂ, ∃ V : Matrix (Fin (χ ^ size C)) b ℂ,
      coef v = U * V) :
    vnS (ptr2 (proj v)) ≤ Real.log χ * (cuts.inf' hne size : ℕ) := by
  obtain ⟨C, hC, hCeq⟩ := Finset.exists_mem_eq_inf' hne size
  obtain ⟨U, V, hUV⟩ := hfac C hC
  have h := mincut_bound hv χ (size C) (Fintype.card_fin _) U V hUV
  rw [hCeq, mul_comm]
  exact h

/-! ## Witness: maximally entangled two-qubit states -/

/-- `v_t = √t (|00⟩ + |11⟩)`; `t = 1/2` is the normalised Bell state. -/
noncomputable def bellT (t : ℝ) : Fin 2 × Fin 2 → ℂ :=
  fun p => if p.1 = p.2 then ((Real.sqrt t : ℝ) : ℂ) else 0

theorem sqrt_mul_star {t : ℝ} (ht : 0 ≤ t) :
    ((Real.sqrt t : ℝ) : ℂ) * star ((Real.sqrt t : ℝ) : ℂ) = ((t : ℝ) : ℂ) := by
  rw [Complex.star_def, Complex.conj_ofReal, ← Complex.ofReal_mul, Real.mul_self_sqrt ht]

theorem sqrt_mul_sqrt_c {t : ℝ} (ht : 0 ≤ t) :
    ((Real.sqrt t : ℝ) : ℂ) * ((Real.sqrt t : ℝ) : ℂ) = ((t : ℝ) : ℂ) := by
  rw [← Complex.ofReal_mul, Real.mul_self_sqrt ht]

theorem norm_bellT {t : ℝ} (ht : 0 ≤ t) :
    ∑ p, bellT t p * star (bellT t p) = ((2 * t : ℝ) : ℂ) := by
  simp only [Fintype.sum_prod_type, Fin.sum_univ_two, bellT]
  simp [sqrt_mul_sqrt_c ht]
  ring

theorem ptr2_bellT {t : ℝ} (ht : 0 ≤ t) :
    ptr2 (proj (bellT t)) = diagonal fun _ => ((t : ℝ) : ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [ptr2, proj, vecMulVec_apply, bellT, sqrt_mul_sqrt_c ht]

theorem vnS_ptr2_bellT {t : ℝ} (ht : 0 ≤ t) :
    vnS (ptr2 (proj (bellT t))) = 2 * negMulLog t := by
  rw [ptr2_bellT ht, vnS_diagonal]
  simp

theorem bell_normalised : ∑ p, bellT (1 / 2) p * star (bellT (1 / 2) p) = 1 := by
  rw [norm_bellT (by norm_num)]
  norm_num

theorem vnS_bell : vnS (ptr2 (proj (bellT (1 / 2)))) = Real.log 2 := by
  rw [vnS_ptr2_bellT (by norm_num), negMulLog, one_div, Real.log_inv]
  ring

/-- The Bell state factors through one bond of dimension `2` (`U = coef v`, `V = 1`). -/
theorem bell_factor : coef (bellT (1 / 2)) = coef (bellT (1 / 2)) * (1 : Matrix (Fin 2) (Fin 2) ℂ) :=
  (Matrix.mul_one _).symm

/-- **Non-vacuity witness.** The Bell state is normalised, factors through a single bond of
dimension `χ = 2` (`|C| = 1`), and attains the bound: `S_A = log 2 = 1 · log 2`. Since `log 2 > 0`,
the conclusion is not automatic. -/
theorem witness_bell :
    (∑ p, bellT (1 / 2) p * star (bellT (1 / 2) p) = 1) ∧
    coef (bellT (1 / 2)) = coef (bellT (1 / 2)) * (1 : Matrix (Fin 2) (Fin 2) ℂ) ∧
    vnS (ptr2 (proj (bellT (1 / 2)))) = ((1 : ℕ) : ℝ) * Real.log (2 : ℕ) ∧
    0 < Real.log 2 := by
  refine ⟨bell_normalised, bell_factor, ?_, Real.log_pos (by norm_num)⟩
  rw [vnS_bell]; push_cast; ring

/-- The theorem applies to the witness (types and hypotheses match). -/
example : vnS (ptr2 (proj (bellT (1 / 2)))) ≤ ((1 : ℕ) : ℝ) * Real.log (2 : ℕ) :=
  mincut_bound bell_normalised 2 1 (by simp) _ _ bell_factor

/-! ## Mutants proved false -/

/-- **Mutant 1** (a cut with no bonds, `|C| = 0`, i.e. dropping the factorisation): the claim
`S_A ≤ 0` for every normalised two-qubit state is false (Bell state, `S_A = log 2`). -/
theorem mutant_no_cut_false :
    ¬ ∀ v : Fin 2 × Fin 2 → ℂ, ∑ p, v p * star (v p) = 1 →
      vnS (ptr2 (proj v)) ≤ ((0 : ℕ) : ℝ) * Real.log 2 := by
  intro h
  have h1 := h _ bell_normalised
  rw [vnS_bell] at h1
  have : (0 : ℝ) < Real.log 2 := Real.log_pos (by norm_num)
  simp at h1
  linarith

/-- **Mutant 2** (normalisation dropped): `v = √(1/3)(|00⟩ + |11⟩)` factors through one bond of
dimension `2` but has `S_A = (2/3) log 3 > log 2 = 1 · log 2`, since `9 > 8`. -/
theorem mutant_no_norm_false :
    ¬ ∀ v : Fin 2 × Fin 2 → ℂ, ∀ U V : Matrix (Fin 2) (Fin 2) ℂ, coef v = U * V →
      vnS (ptr2 (proj v)) ≤ ((1 : ℕ) : ℝ) * Real.log 2 := by
  intro h
  have h1 := h (bellT (1 / 3)) _ 1 (Matrix.mul_one _).symm
  rw [vnS_ptr2_bellT (by norm_num), negMulLog, one_div, Real.log_inv] at h1
  have h98 : Real.log 8 < Real.log 9 := Real.log_lt_log (by norm_num) (by norm_num)
  have h8 : Real.log 8 = 3 * Real.log 2 := by
    rw [show (8 : ℝ) = 2 ^ 3 by norm_num, Real.log_pow]; norm_num
  have h9 : Real.log 9 = 2 * Real.log 3 := by
    rw [show (9 : ℝ) = 3 ^ 2 by norm_num, Real.log_pow]; norm_num
  push_cast at h1
  linarith

end LeanReal.Chap11MinCut

#print axioms LeanReal.Chap11MinCut.vnS_marginal_le_log_card_of_factor
#print axioms LeanReal.Chap11MinCut.mincut_bound
#print axioms LeanReal.Chap11MinCut.mincut_bound_min
#print axioms LeanReal.Chap11MinCut.witness_bell
#print axioms LeanReal.Chap11MinCut.mutant_no_cut_false
#print axioms LeanReal.Chap11MinCut.mutant_no_norm_false
