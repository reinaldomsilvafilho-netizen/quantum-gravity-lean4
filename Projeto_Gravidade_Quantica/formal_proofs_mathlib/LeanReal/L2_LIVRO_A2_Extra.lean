import LeanReal.Chap03Analysis
import LeanReal.Chap04Symbol

/-!
# L2 extras for batch LIVRO_A2 (book chapters 3 and 4)

Written by the independent layer-2 reviewer. No gaps, no extra axioms.

* Chapter 3, `thm:laplacian_symbol`: the book asserts `a(α) > 0` for
  `M₂ = a·Id + b·11ᵀ`. `M2_a_pos` proves `a > 0` for any coordinate-permutation
  invariant measure that is not concentrated on the diagonal `y i₀ = y i₁`
  (true for the Beta kernel, whose law is absolutely continuous).
  `mutant_a_pos_without_spread_false`: without that condition `a > 0` fails
  (a Dirac mass at `(1,1)` is permutation invariant and gives `a = 0`).
* Chapter 3, `cor:row_log_product`: `row_log_product_iff` shows that, for any `G`,
  the hypothesis `hAlex` at the point `x` is *equivalent* to the conclusion.
  So the Lean content of the corollary is `E_reduction`; the Barnes-G content is
  exactly the classical Alexeiewsky theorem, which stays a named hypothesis.
-/

noncomputable section

namespace LeanReal.L2_LIVRO_A2

open MeasureTheory Real Matrix
open LeanReal.Chap04Symbol LeanReal.Chap03Analysis

/-- `thm:laplacian_symbol` (ch. 3), `a(α) > 0`: for a permutation-invariant measure with
integrable second moments that is not almost surely concentrated on `y i₀ = y i₁`,
the diagonal excess `a = M₂ i₀ i₀ − M₂ i₀ i₁` is strictly positive. -/
theorem M2_a_pos {d : ℕ} (μ : Measure (Fin d → ℝ))
    (hperm : ∀ σ : Equiv.Perm (Fin d), μ.map (fun y => y ∘ σ) = μ)
    (hM : ∀ i j, Integrable (fun y : Fin d → ℝ => y i * y j) μ)
    (i₀ i₁ : Fin d) (h01 : i₀ ≠ i₁)
    (hspread : ¬ (∀ᵐ y ∂μ, y i₀ = y i₁)) :
    0 < M2 μ i₀ i₀ - M2 μ i₀ i₁ := by
  obtain ⟨ha, -⟩ := M2_a_nonneg μ hperm hM i₀ i₁ h01
  rw [ha]
  have hint : Integrable (fun y : Fin d → ℝ => (y i₀ - y i₁) ^ 2) μ := by
    have h := (((hM i₀ i₀).sub (hM i₀ i₁)).sub ((hM i₁ i₀).sub (hM i₁ i₁)))
    refine h.congr (Filter.Eventually.of_forall fun y => ?_)
    simp only [Pi.sub_apply]
    ring
  have hpos : 0 < ∫ y, (y i₀ - y i₁) ^ 2 ∂μ := by
    rw [integral_pos_iff_support_of_nonneg (fun y => sq_nonneg _) hint]
    have hsupp : Function.support (fun y : Fin d → ℝ => (y i₀ - y i₁) ^ 2) =
        {y | ¬ (y i₀ = y i₁)} := by
      ext y
      simp [sub_eq_zero]
    rw [hsupp, pos_iff_ne_zero]
    intro h0
    exact hspread (ae_iff.mpr h0)
  positivity

/-- The Dirac mass at `(1,1)` is invariant under the coordinate permutations of `Fin 2`. -/
theorem dirac11_perm :
    ∀ σ : Equiv.Perm (Fin 2),
      (Measure.dirac (![1, 1] : Fin 2 → ℝ)).map (fun y => y ∘ σ) = Measure.dirac ![1, 1] := by
  intro σ
  have hmeas : Measurable (fun y : Fin 2 → ℝ => y ∘ σ) :=
    (continuous_pi fun a => continuous_apply (σ a)).measurable
  rw [Measure.map_dirac' hmeas]
  have h1 : ∀ s : Fin 2, (![1, 1] : Fin 2 → ℝ) s = 1 := by
    intro s; fin_cases s <;> rfl
  congr 1
  funext t
  rw [Function.comp_apply, h1, h1]

/-- Mutant: dropping the non-concentration hypothesis, `a > 0` is false. -/
theorem mutant_a_pos_without_spread_false :
    ¬ (∀ (μ : Measure (Fin 2 → ℝ)),
        (∀ σ : Equiv.Perm (Fin 2), μ.map (fun y => y ∘ σ) = μ) →
        0 < M2 μ 0 0 - M2 μ 0 1) := by
  intro h
  have := h (Measure.dirac ![1, 1]) dirac11_perm
  simp [M2, integral_dirac] at this

/-- Non-vacuity of `M2_a_pos`: the measure `mu3` of `Chap04Symbol` is not concentrated
on the diagonal (the atom `(1,0)` has mass `1/3`), and indeed `a = 1/3 > 0`. -/
theorem mu3_spread : ¬ (∀ᵐ y ∂mu3, y 0 = y 1) := by
  intro h
  rw [ae_iff] at h
  have hsub : ({![1, 0]} : Set (Fin 2 → ℝ)) ⊆ {a | ¬ (a 0 = a 1)} := by
    intro y hy
    rw [Set.mem_singleton_iff] at hy
    subst hy
    simp
  have hle := measure_mono (μ := mu3) hsub
  rw [h, nonpos_iff_eq_zero] at hle
  have : mu3 {![1, 0]} ≠ 0 := by
    unfold mu3
    simp [Measure.add_apply]
  exact this hle

theorem witness_M2_a_pos : 0 < M2 mu3 0 0 - M2 mu3 0 1 := by
  rw [witness_M2.2.1, witness_M2.2.2.1]
  norm_num

/-- `cor:row_log_product`: for any `G`, the hypothesis `hAlex` at the single point `x`
is equivalent to the conclusion. The corollary therefore adds nothing to `E_reduction`
beyond the classical Alexeiewsky theorem, which remains a named hypothesis. -/
theorem row_log_product_iff (G : ℝ → ℝ) (x : ℝ) (hx : 0 ≤ x) :
    (∫ y in (0 : ℝ)..x, Real.log (Real.Gamma (y + 1)) =
        x * Real.log (Real.Gamma (x + 1)) - Real.log (G (x + 1)) + x / 2 * Real.log (2 * π) -
          x * (x + 1) / 2) ↔
      rowEntropy x = x * (x + 1) - x * Real.log (2 * π) - x * Real.log (Real.Gamma (x + 1)) +
        2 * Real.log (G (x + 1)) := by
  rw [E_reduction x hx]
  constructor <;> intro h <;> linarith

end LeanReal.L2_LIVRO_A2

#print axioms LeanReal.L2_LIVRO_A2.M2_a_pos
#print axioms LeanReal.L2_LIVRO_A2.dirac11_perm
#print axioms LeanReal.L2_LIVRO_A2.mutant_a_pos_without_spread_false
#print axioms LeanReal.L2_LIVRO_A2.mu3_spread
#print axioms LeanReal.L2_LIVRO_A2.witness_M2_a_pos
#print axioms LeanReal.L2_LIVRO_A2.row_log_product_iff
