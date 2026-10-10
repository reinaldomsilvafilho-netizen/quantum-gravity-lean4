import LeanReal.Chap04Modulational
import LeanReal.Chap05Barycentric

/-!
# L2 extras for batch LIVRO_A1 (book ch. 4 and ch. 5)

Written by the independent L2 reviewer, not by the batch writer.

* Ch. 4, Theorem "Simplicial Modulational Instability": in the book the symbol satisfies
  `σ(k) ≥ 0`, with `σ(k) = 0` only at `k = 0`. The writer's mutant uses `σ = 0`; here the
  mutant is restated inside the book's range `σ ≥ 0`, and the corrected criterion is given
  in the form "σ ≠ 0 (i.e. k ≠ 0) and σ < 4Mc/ħ²". A witness on the stable side of the band
  shows that the threshold bites.
* Ch. 5, Prop. "Inversion": a non-degenerate witness of `deconvolution` (non-constant,
  non-real kernel values that do not vanish).
-/

noncomputable section

namespace LeanReal.L2_LIVRO_A1_Extra

open LeanReal.Chap04Modulational

/-- Ch. 4: for `σ ≥ 0` (the book's range of the symbol), `Ω² < 0` iff `σ ≠ 0` and
`σ < 4Mc/ħ²`. Since `σ(k) = 0` exactly at `k = 0`, this is the criterion "`k ≠ 0` and
`σ(k) < 4Mc/ħ²`". -/
theorem unstable_iff_of_nonneg (ħ M c σ : ℝ) (hħ : 0 < ħ) (hM : 0 < M) (hc : 0 < c)
    (hσ : 0 ≤ σ) :
    omegaSqHbar (eps ħ M σ) c / ħ ^ 2 < 0 ↔ σ ≠ 0 ∧ σ < 4 * M * c / ħ ^ 2 := by
  rw [unstable_iff ħ M c σ hħ hM hc]
  constructor
  · rintro ⟨h1, h2⟩
    exact ⟨h1.ne', h2⟩
  · rintro ⟨h1, h2⟩
    exact ⟨lt_of_le_of_ne hσ (Ne.symm h1), h2⟩

/-- Ch. 4 mutant restricted to the book's range `σ ≥ 0`: the printed criterion
"`σ < 4Mc/ħ²` ⇒ `Ω² < 0`" is still false (at `σ = 0`, i.e. `k = 0`). -/
theorem mutant_book_criterion_nonneg_false :
    ¬ ∀ ħ M c σ : ℝ, 0 < ħ → 0 < M → 0 < c → 0 ≤ σ → σ < 4 * M * c / ħ ^ 2 →
      omegaSqHbar (eps ħ M σ) c / ħ ^ 2 < 0 := by
  intro h
  have := h 1 1 1 0 one_pos one_pos one_pos le_rfl (by norm_num)
  norm_num [omegaSqHbar, eps] at this

/-- Ch. 4 witness on the stable side: `ħ = M = c = 1`, `σ = 5 > 4 = 4Mc/ħ²` gives
`ħ²Ω² = (5/2)(1/2) > 0`. -/
example : ¬ (omegaSqHbar (eps 1 1 5) 1 / 1 ^ 2 < 0) := by
  norm_num [omegaSqHbar, eps]

open LeanReal.Chap05Barycentric

/-- Ch. 5 witness of `deconvolution` with non-vanishing, non-constant, non-real kernel
values `K̂ = (2, i)`: from `ĥ = K̂ f̂` one recovers `f̂ = (3, 1)`. -/
example : (![3, 1] : Fin 2 → ℂ) =
    fun k => (![6, Complex.I] : Fin 2 → ℂ) k / (![2, Complex.I] : Fin 2 → ℂ) k := by
  refine deconvolution (![2, Complex.I] : Fin 2 → ℂ) ![3, 1] ![6, Complex.I] ?_ ?_
  · intro k
    fin_cases k
    · simp
    · simp [Complex.I_ne_zero]
  · intro k
    fin_cases k
    · simp; norm_num
    · simp

end LeanReal.L2_LIVRO_A1_Extra

#print axioms LeanReal.L2_LIVRO_A1_Extra.unstable_iff_of_nonneg
#print axioms LeanReal.L2_LIVRO_A1_Extra.mutant_book_criterion_nonneg_false
