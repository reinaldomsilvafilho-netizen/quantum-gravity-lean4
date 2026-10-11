import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Asymptotics
import Mathlib.Analysis.SpecialFunctions.Gamma.Basic
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.Asymptotics.Lemmas
import Mathlib.Analysis.Asymptotics.SpecificAsymptotics
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Tactic

/-!
# Chapter 6, `thm:multifractal`: conditional asymptotic algebra of the row entropy

Batch B5 of `PLANO_LIVRO_A.md`, item 3.

Source: `unified_quantum_gravity_book/chap06_sierpinski_fractal_resolvents_spectral_reduction.tex`,
Proposition "Asymptotics of the Continuous Row Entropy" (`thm:multifractal`).

Frozen statement. With `ℰ(x) = x(x+1) − x ln(2π) − x lnΓ(x+1) + 2 ln G(x+1)`, as `x → ∞`,
`ℰ(x) = x²/2 − (x/2)ln x + (1 − ln(2π)/2)x − (1/6)ln x + 2ζ'(−1) − 1/12 − 1/(180x²) + O(x^{−4})`,
and `ℰ(x)/x² → 1/2`. The proof inserts Stirling's series
`lnΓ(x+1) = x ln x − x + ½ln(2πx) + 1/(12x) − 1/(360x³) + O(x^{−5})` and the Barnes series
`ln G(x+1) = (x²/2)ln x − 3x²/4 + (x/2)ln(2π) − (1/12)ln x + ζ'(−1) − 1/(240x²) + O(x^{−4})`.

## Declared reduction (conditional)

* `lnΓ(x+1)` and `ln G(x+1)` enter as arbitrary real functions `lg`, `lG`; the two classical
  series are the named hypotheses `hStir` and `hBarnes` (`IsBigO` at `atTop`). Mathlib has neither
  the Barnes `G`-function nor Stirling's series with the `1/(12x) − 1/(360x³)` terms.
  `row_entropy_expansion_Gamma` is the instance `lg x = log Γ(x+1)` with Mathlib's `Real.Gamma`.
* The constant `ζ'(−1)` is a free real parameter `κ`: the computation only carries it from
  `hBarnes` to the conclusion. The book's statement is the case `κ = ζ'(−1)`.
* The closed form of `ℰ` as the integral `∫₀ˣ ln C(x,y) dy` (Chapter 3) is not used: `ℰ` is
  defined by the closed form, as in the statement.
* What Lean proves beyond the hypotheses: the exact cancellation of the `x²ln x` terms, every
  coefficient down to `x^{−2}` (`−1/6`, `2κ − 1/12`, `−1/180`), the absorption of `−x·O(x^{−5})`
  into `O(x^{−4})`, and the limit `ℰ(x)/x² → 1/2`.
-/

noncomputable section

namespace LeanReal.Chap06Multifractal

open Real Filter Asymptotics Topology

/-- The row entropy in closed form, `ℰ(x) = x(x+1) − x ln(2π) − x·lg(x) + 2·lG(x)`, where
`lg` stands for `ln Γ(x+1)` and `lG` for `ln G(x+1)` (`thm:multifractal`). -/
def rowEntropy (lg lG : ℝ → ℝ) (x : ℝ) : ℝ :=
  x * (x + 1) - x * log (2 * π) - x * lg x + 2 * lG x

/-- Stirling's series truncated after `−1/(360x³)`. -/
def stirTrunc (x : ℝ) : ℝ :=
  x * log x - x + 1 / 2 * log (2 * π * x) + 1 / (12 * x) - 1 / (360 * x ^ 3)

/-- The Barnes series for `ln G(x+1)` truncated after `−1/(240x²)`, with constant `κ`. -/
def barnesTrunc (κ x : ℝ) : ℝ :=
  x ^ 2 / 2 * log x - 3 * x ^ 2 / 4 + x / 2 * log (2 * π) - 1 / 12 * log x + κ - 1 / (240 * x ^ 2)

/-- The book's expansion of `ℰ(x)` up to and including the `x^{−2}` term. -/
def expansion (κ x : ℝ) : ℝ :=
  x ^ 2 / 2 - x / 2 * log x + (1 - log (2 * π) / 2) * x - 1 / 6 * log x + 2 * κ - 1 / 12
    - 1 / (180 * x ^ 2)

/-- The exact algebraic identity behind the proof: for `x > 0`,
`ℰ − expansion = −x·(lg − Stirling) + 2·(lG − Barnes)`. -/
theorem remainder_identity (lg lG : ℝ → ℝ) (κ x : ℝ) (hx : 0 < x) :
    rowEntropy lg lG x - expansion κ x
      = -x * (lg x - stirTrunc x) + 2 * (lG x - barnesTrunc κ x) := by
  have hl : log (2 * π * x) = log (2 * π) + log x :=
    Real.log_mul (by positivity) hx.ne'
  simp only [rowEntropy, expansion, stirTrunc, barnesTrunc, hl]
  field_simp
  ring

/-- **`thm:multifractal`, conditional on Stirling's and Barnes' series.**
`ℰ(x) − [x²/2 − (x/2)ln x + (1 − ln(2π)/2)x − (1/6)ln x + 2κ − 1/12 − 1/(180x²)] = O(x^{−4})`. -/
theorem row_entropy_expansion (lg lG : ℝ → ℝ) (κ : ℝ)
    (hStir : (fun x => lg x - stirTrunc x) =O[atTop] (fun x => 1 / x ^ 5))
    (hBarnes : (fun x => lG x - barnesTrunc κ x) =O[atTop] (fun x => 1 / x ^ 4)) :
    (fun x => rowEntropy lg lG x - expansion κ x) =O[atTop] (fun x => 1 / x ^ 4) := by
  have h1 : (fun x => -x * (lg x - stirTrunc x)) =O[atTop] (fun x => 1 / x ^ 4) := by
    have := (isBigO_refl (fun x : ℝ => -x) atTop).mul hStir
    refine this.trans (IsBigO.of_bound 1 ?_)
    filter_upwards [eventually_gt_atTop 0] with x hx
    rw [one_mul, norm_mul, norm_neg, norm_div, norm_div, norm_one, norm_pow, norm_pow,
      Real.norm_of_nonneg hx.le]
    apply le_of_eq
    field_simp
  have h2 := (hBarnes.const_mul_left 2)
  refine (h1.add h2).congr' ?_ EventuallyEq.rfl
  filter_upwards [eventually_gt_atTop 0] with x hx
  exact (remainder_identity lg lG κ x hx).symm

/-- Instance with Mathlib's Gamma function: `lg x = log Γ(x+1)`. Stirling's series stays a named
hypothesis (classical; not in Mathlib in this form). -/
theorem row_entropy_expansion_Gamma (lG : ℝ → ℝ) (κ : ℝ)
    (hStir : (fun x => log (Gamma (x + 1)) - stirTrunc x) =O[atTop] (fun x => 1 / x ^ 5))
    (hBarnes : (fun x => lG x - barnesTrunc κ x) =O[atTop] (fun x => 1 / x ^ 4)) :
    (fun x => rowEntropy (fun y => log (Gamma (y + 1))) lG x - expansion κ x)
      =O[atTop] (fun x => 1 / x ^ 4) :=
  row_entropy_expansion _ lG κ hStir hBarnes

/-- **`thm:multifractal`, "in particular":** `ℰ(x)/x² → 1/2`, under the same hypotheses. -/
theorem row_entropy_div_sq (lg lG : ℝ → ℝ) (κ : ℝ)
    (hStir : (fun x => lg x - stirTrunc x) =O[atTop] (fun x => 1 / x ^ 5))
    (hBarnes : (fun x => lG x - barnesTrunc κ x) =O[atTop] (fun x => 1 / x ^ 4)) :
    Tendsto (fun x => rowEntropy lg lG x / x ^ 2) atTop (𝓝 (1 / 2)) := by
  have h12 : (fun x : ℝ => x) =o[atTop] (fun x => x ^ 2) := by
    simpa using isLittleO_pow_pow_atTop_of_lt (𝕜 := ℝ) (show 1 < 2 by norm_num)
  have h02 : (fun _ : ℝ => (1 : ℝ)) =o[atTop] (fun x => x ^ 2) := by
    simp
  have hlog : (fun x : ℝ => log x) =o[atTop] (fun x => x) := isLittleO_log_id_atTop
  have hlog2 := hlog.trans h12
  have hxlog : (fun x : ℝ => x * log x) =o[atTop] (fun x => x ^ 2) := by
    have := (isBigO_refl (fun x : ℝ => x) atTop).mul_isLittleO hlog
    simpa [sq] using this
  have hconst : ∀ c : ℝ, (fun _ : ℝ => c) =o[atTop] (fun x => x ^ 2) := fun c =>
    (isBigO_const_one ℝ c atTop).trans_isLittleO h02
  have hsmall : ∀ n : ℕ, 1 ≤ n → (fun x : ℝ => 1 / x ^ n) =o[atTop] (fun x => x ^ 2) := by
    intro n hn
    refine (IsBigO.of_bound 1 ?_).trans_isLittleO h02
    filter_upwards [eventually_ge_atTop 1] with x hx
    simp only [norm_div, norm_one, norm_pow, mul_one, Real.norm_of_nonneg (by linarith : (0 : ℝ) ≤ x)]
    exact div_le_one_of_le₀ (one_le_pow₀ hx) (by positivity)
  have hexp : (fun x => expansion κ x - x ^ 2 / 2) =o[atTop] (fun x => x ^ 2) := by
    have := ((hxlog.const_mul_left (-1 / 2)).add (h12.const_mul_left (1 - log (2 * π) / 2))).add
      ((hlog2.const_mul_left (-1 / 6)).add ((hconst (2 * κ - 1 / 12)).add
        ((hsmall 2 (by norm_num)).const_mul_left (-1 / 180))))
    refine this.congr' ?_ EventuallyEq.rfl
    filter_upwards [eventually_gt_atTop 0] with x hx
    simp only [expansion]
    field_simp
    ring
  have hrem := (row_entropy_expansion lg lG κ hStir hBarnes).trans_isLittleO
    (hsmall 4 (by norm_num))
  have hall : (fun x => rowEntropy lg lG x - x ^ 2 / 2) =o[atTop] (fun x => x ^ 2) := by
    refine (hrem.add hexp).congr' ?_ EventuallyEq.rfl
    exact Eventually.of_forall fun x => by ring
  have ht := (hall.tendsto_div_nhds_zero).add_const (1 / 2)
  rw [zero_add] at ht
  refine ht.congr' ?_
  filter_upwards [eventually_gt_atTop 0] with x hx
  field_simp
  ring

/-! ### Non-vacuity witness -/

/-- Witness with non-zero remainders: `lg = Stirling + x^{−5}`, `lG = Barnes + x^{−4}`. Both
hypotheses hold, and `ℰ − expansion = x^{−4}`, which is not identically zero. -/
theorem witness (κ : ℝ) :
    let lg : ℝ → ℝ := fun x => stirTrunc x + 1 / x ^ 5
    let lG : ℝ → ℝ := fun x => barnesTrunc κ x + 1 / x ^ 4
    ((fun x => lg x - stirTrunc x) =O[atTop] (fun x => 1 / x ^ 5)) ∧
    ((fun x => lG x - barnesTrunc κ x) =O[atTop] (fun x => 1 / x ^ 4)) ∧
    rowEntropy lg lG 2 - expansion κ 2 = 1 / 16 := by
  intro lg lG
  refine ⟨?_, ?_, ?_⟩
  · exact (isBigO_refl (fun x : ℝ => 1 / x ^ 5) atTop).congr_left (fun x => by simp only [lg]; ring)
  · exact (isBigO_refl (fun x : ℝ => 1 / x ^ 4) atTop).congr_left (fun x => by simp only [lG]; ring)
  · rw [remainder_identity lg lG κ 2 two_pos]
    simp only [lg, lG]
    norm_num

/-! ### Mutants (negations proved) -/

/-- A function bounded below by `a/x²` (`a > 0`) is not `O(x^{−4})`. -/
theorem not_isBigO_inv4 (f : ℝ → ℝ) (a : ℝ) (ha : 0 < a)
    (hf : ∀ᶠ x in atTop, a / x ^ 2 ≤ |f x|) : ¬ f =O[atTop] (fun x => 1 / x ^ 4) := by
  intro h
  obtain ⟨C, hC⟩ := h.bound
  obtain ⟨N, hN⟩ := eventually_atTop.1 (hf.and (hC.and (eventually_ge_atTop (1 : ℝ))))
  set x := max N (max 1 ((|C| + 1) / a)) with hxdef
  obtain ⟨h1, h2, h3⟩ := hN x (le_max_left _ _)
  have hx1 : 1 ≤ x := le_trans (le_max_left _ _) (le_max_right _ _)
  have hxa : (|C| + 1) / a ≤ x := le_trans (le_max_right _ _) (le_max_right _ _)
  have hxpos : 0 < x := by linarith
  rw [Real.norm_eq_abs, norm_div, norm_one, norm_pow, Real.norm_of_nonneg hxpos.le] at h2
  have h4 : a / x ^ 2 ≤ C * (1 / x ^ 4) := h1.trans h2
  have hx4 : 0 < x ^ 4 := by positivity
  have h5 : a * x ^ 2 ≤ C := by
    have := mul_le_mul_of_nonneg_right h4 hx4.le
    have e1 : a / x ^ 2 * x ^ 4 = a * x ^ 2 := by field_simp
    have e2 : C * (1 / x ^ 4) * x ^ 4 = C := by field_simp
    linarith
  have h6 : |C| + 1 ≤ a * x := by
    have := (div_le_iff₀ ha).1 hxa; linarith
  have h7 : a * x ≤ a * x ^ 2 := by
    have : x ≤ x ^ 2 := by nlinarith
    exact mul_le_mul_of_nonneg_left this ha.le
  linarith [le_abs_self C]

/-- Mutant 1: the naive coefficient `−1/(240x²)` (Barnes alone, forgetting the Stirling term
`−x·(−1/(360x³))`) in place of `−1/(180x²)` makes the statement false. -/
theorem mutant_coeff_240_false :
    ¬ ∀ (lg lG : ℝ → ℝ) (κ : ℝ),
      (fun x => lg x - stirTrunc x) =O[atTop] (fun x => 1 / x ^ 5) →
      (fun x => lG x - barnesTrunc κ x) =O[atTop] (fun x => 1 / x ^ 4) →
      (fun x => rowEntropy lg lG x - (expansion κ x + 1 / (180 * x ^ 2) - 1 / (240 * x ^ 2)))
        =O[atTop] (fun x => 1 / x ^ 4) := by
  intro h
  have z5 : (fun _ : ℝ => (0 : ℝ)) =O[atTop] (fun x : ℝ => 1 / x ^ 5) := isBigO_zero _ _
  have z4 : (fun _ : ℝ => (0 : ℝ)) =O[atTop] (fun x : ℝ => 1 / x ^ 4) := isBigO_zero _ _
  have := h stirTrunc (barnesTrunc 0) 0 (z5.congr_left fun x => (sub_self _).symm)
    (z4.congr_left fun x => (sub_self _).symm)
  refine not_isBigO_inv4 _ (1 / 720) (by norm_num) ?_ this
  filter_upwards [eventually_gt_atTop 0] with x hx
  have e : rowEntropy stirTrunc (barnesTrunc 0) x
      - (expansion 0 x + 1 / (180 * x ^ 2) - 1 / (240 * x ^ 2)) = -(1 / 720 / x ^ 2) := by
    have := remainder_identity stirTrunc (barnesTrunc 0) 0 x hx
    simp only [sub_self, mul_zero, add_zero] at this
    have e2 : rowEntropy stirTrunc (barnesTrunc 0) x - (expansion 0 x + 1 / (180 * x ^ 2)
        - 1 / (240 * x ^ 2)) = (rowEntropy stirTrunc (barnesTrunc 0) x - expansion 0 x)
        - 1 / (180 * x ^ 2) + 1 / (240 * x ^ 2) := by ring
    rw [e2, this]
    field_simp
    ring
  rw [e, abs_neg, abs_of_pos (by positivity)]

/-- Mutant 2: replacing `−(1/6)ln x` by `−(1/12)ln x` (the remark in the proof) is false. -/
theorem mutant_log_coeff_false :
    ¬ ∀ (lg lG : ℝ → ℝ) (κ : ℝ),
      (fun x => lg x - stirTrunc x) =O[atTop] (fun x => 1 / x ^ 5) →
      (fun x => lG x - barnesTrunc κ x) =O[atTop] (fun x => 1 / x ^ 4) →
      (fun x => rowEntropy lg lG x - (expansion κ x + 1 / 6 * log x - 1 / 12 * log x))
        =O[atTop] (fun x => 1 / x ^ 4) := by
  intro h
  have z5 : (fun _ : ℝ => (0 : ℝ)) =O[atTop] (fun x : ℝ => 1 / x ^ 5) := isBigO_zero _ _
  have z4 : (fun _ : ℝ => (0 : ℝ)) =O[atTop] (fun x : ℝ => 1 / x ^ 4) := isBigO_zero _ _
  have := h stirTrunc (barnesTrunc 0) 0 (z5.congr_left fun x => (sub_self _).symm)
    (z4.congr_left fun x => (sub_self _).symm)
  refine not_isBigO_inv4 _ (1 / 12) (by norm_num) ?_ this
  filter_upwards [eventually_ge_atTop (3 : ℝ)] with x hx
  have hx0 : 0 < x := by linarith
  have e : rowEntropy stirTrunc (barnesTrunc 0) x
      - (expansion 0 x + 1 / 6 * log x - 1 / 12 * log x) = -(1 / 12 * log x) := by
    have := remainder_identity stirTrunc (barnesTrunc 0) 0 x hx0
    simp only [sub_self, mul_zero, add_zero] at this
    linarith
  have hlog : 1 ≤ log x := by
    rw [Real.le_log_iff_exp_le hx0]
    linarith [Real.exp_one_lt_d9]
  have hx2 : 1 ≤ x ^ 2 := one_le_pow₀ (by linarith)
  rw [e, abs_neg, abs_of_nonneg (by positivity)]
  calc 1 / 12 / x ^ 2 ≤ 1 / 12 := div_le_self (by norm_num) hx2
    _ ≤ 1 / 12 * log x := by linarith

end LeanReal.Chap06Multifractal

#print axioms LeanReal.Chap06Multifractal.remainder_identity
#print axioms LeanReal.Chap06Multifractal.row_entropy_expansion
#print axioms LeanReal.Chap06Multifractal.row_entropy_expansion_Gamma
#print axioms LeanReal.Chap06Multifractal.row_entropy_div_sq
#print axioms LeanReal.Chap06Multifractal.witness
#print axioms LeanReal.Chap06Multifractal.not_isBigO_inv4
#print axioms LeanReal.Chap06Multifractal.mutant_coeff_240_false
#print axioms LeanReal.Chap06Multifractal.mutant_log_coeff_false
