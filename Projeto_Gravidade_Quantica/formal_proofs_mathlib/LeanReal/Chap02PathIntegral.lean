import Mathlib.Analysis.ODE.ExistUnique
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Matrix.Normed
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Tactic

/-!
# Chapter 2, `thm:continuous_path_integral` (iii) and the sharpness example of (ii)

Batch B5 of `PLANO_LIVRO_A.md`, item 1.

Source: `unified_quantum_gravity_book/chap02_geometric_flows_tensor_varieties.tex`, Theorem
"Continuum Path-Integral Limit and Non-Abelian Gauge Invariance" (`thm:continuous_path_integral`).

Frozen statement of (iii). Let `𝒜 ∈ C¹([0,1], 𝔤𝔩(r))` and `Ω ∈ C²([0,1], GL(r))` with
`Ω(0) = Ω(1)`. Put `𝒜^Ω = Ω⁻¹𝒜Ω − Ω⁻¹∂_sΩ`. Then
`𝒫exp∮𝒜^Ω = Ω(0)⁻¹ (𝒫exp∮𝒜) Ω(0)` and `Tr 𝒫exp∮𝒜^Ω = Tr 𝒫exp∮𝒜`.
The proof identifies `𝒫exp∫₀¹𝒜` with `U(1)`, where `U' = 𝒜U`, `U(0) = I` (`eq:matrix_ode`).

Frozen statement of the example in (ii). For `r = 1`, `𝒜 ≡ 0`, `ℛ_j ≡ M`, the error is
`(1 + M/k²)^k − 1`; it exceeds `M/k` for every `k ≥ 2` and is at most `(M/k)e^{M/k}`.

## Declared reduction

* The path-ordered exponential is read, as in the book's proof, as the value at `s = 1` of the
  solution of `X' = 𝒜X`, `X(0) = I`. The Dyson series is not formalized; `U` and `W` enter as
  given solutions on `[0,1]` (one-sided derivatives at the ends).
* The theorem is proved in any normed `ℝ`-algebra `𝔸` (non-commutative allowed); `GL(r)` is read
  as "`Ω(s)` is a unit". The matrix form, with `⁻¹` the matrix inverse and the trace, is the
  corollary `trace_holonomy_gauge_invariant` for `Matrix (Fin r) (Fin r) ℂ`.
* Regularity used: `𝒜` continuous on `[0,1]` (the book asks `C¹`), `Ω` differentiable on `[0,1]`
  with derivative `Ω'` (the book asks `C²`). Periodicity is needed only for the book's final
  form; the general law is `W(1) = Ω(1)⁻¹ U(1) Ω(0)`.
* Proof route: `Y = Ω W Ω(0)⁻¹` solves `Y' = 𝒜Y`, `Y(0) = I` (only `ΩΩ⁻¹ = 1` is used, no
  derivative of the inverse), so `Y = U` by `ODE_solution_unique_of_mem_Icc_right`.
* Items (i) and (ii) (the discrete Grönwall recursion) are not formalized; only the sharpness
  example of (ii) is.
-/

noncomputable section

namespace LeanReal.Chap02PathIntegral

open Set

section General

variable {𝔸 : Type*} [NormedRing 𝔸] [NormedAlgebra ℝ 𝔸]

/-- The gauge-transformed potential `𝒜^Ω(s) = Ω(s)⁻¹𝒜(s)Ω(s) − Ω(s)⁻¹Ω'(s)`
(`eq:continuous_gauge_field`), with `Ω'` the derivative of `Ω` and `Ring.inverse` the inverse. -/
def gaugeTransform (A Ω Ω' : ℝ → 𝔸) (s : ℝ) : 𝔸 :=
  Ring.inverse (Ω s) * A s * Ω s - Ring.inverse (Ω s) * Ω' s

/-- Uniqueness for the linear transport equation `X' = A X` on `[0,1]` with continuous `A`:
two solutions with the same value at `0` agree on `[0,1]`. -/
theorem transport_unique (A U Y : ℝ → 𝔸) (hA : ContinuousOn A (Icc 0 1))
    (hU : ∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt U (A s * U s) (Icc 0 1) s)
    (hY : ∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt Y (A s * Y s) (Icc 0 1) s)
    (h0 : U 0 = Y 0) : EqOn U Y (Icc 0 1) := by
  obtain ⟨C, hC⟩ := isCompact_Icc.exists_bound_of_continuousOn hA
  set K : NNReal := ⟨max C 0, le_max_right _ _⟩ with hK
  have hv : ∀ t ∈ Ico (0 : ℝ) 1, LipschitzOnWith K (fun X : 𝔸 => A t * X) univ := by
    intro t ht
    refine LipschitzOnWith.of_dist_le_mul fun x _ y _ => ?_
    rw [dist_eq_norm, dist_eq_norm, ← mul_sub]
    calc ‖A t * (x - y)‖ ≤ ‖A t‖ * ‖x - y‖ := norm_mul_le _ _
      _ ≤ (K : ℝ) * ‖x - y‖ := by
          gcongr
          exact (hC t (Ico_subset_Icc_self ht)).trans (le_max_left _ _)
  have cont : ∀ V : ℝ → 𝔸, (∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt V (A s * V s) (Icc 0 1) s) →
      ContinuousOn V (Icc 0 1) := fun V hV s hs => (hV s hs).continuousWithinAt
  have der : ∀ V : ℝ → 𝔸, (∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt V (A s * V s) (Icc 0 1) s) →
      ∀ t ∈ Ico (0 : ℝ) 1, HasDerivWithinAt V (A t * V t) (Ici t) t := by
    intro V hV t ht
    exact ((hV t (Ico_subset_Icc_self ht)).mono (Icc_subset_Icc ht.1 le_rfl)).mono_of_mem_nhdsWithin
      (Icc_mem_nhdsGE ht.2)
  exact ODE_solution_unique_of_mem_Icc_right (v := fun t X => A t * X) (s := fun _ => univ) hv
    (cont U hU) (der U hU) (fun _ _ => trivial) (cont Y hY) (der Y hY) (fun _ _ => trivial) h0

/-- **`thm:continuous_path_integral` (iii), pointwise form.** If `U' = 𝒜U`, `U(0) = 1` and
`W' = 𝒜^Ω W`, `W(0) = 1` on `[0,1]`, with `Ω(s)` a unit and `Ω' = ∂_sΩ`, then
`Ω(s) W(s) Ω(0)⁻¹ = U(s)` for all `s ∈ [0,1]`. -/
theorem gauge_conjugation (A Ω Ω' U W : ℝ → 𝔸) (hA : ContinuousOn A (Icc 0 1))
    (hΩ : ∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt Ω (Ω' s) (Icc 0 1) s)
    (hΩu : ∀ s ∈ Icc (0 : ℝ) 1, IsUnit (Ω s))
    (hU : ∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt U (A s * U s) (Icc 0 1) s) (hU0 : U 0 = 1)
    (hW : ∀ s ∈ Icc (0 : ℝ) 1,
      HasDerivWithinAt W (gaugeTransform A Ω Ω' s * W s) (Icc 0 1) s) (hW0 : W 0 = 1) :
    ∀ s ∈ Icc (0 : ℝ) 1, Ω s * W s * Ring.inverse (Ω 0) = U s := by
  set c := Ring.inverse (Ω 0)
  have h0mem : (0 : ℝ) ∈ Icc (0 : ℝ) 1 := ⟨le_rfl, zero_le_one⟩
  have hY : ∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt (fun t => Ω t * W t * c)
      (A s * (Ω s * W s * c)) (Icc 0 1) s := by
    intro s hs
    have e : Ω s * Ring.inverse (Ω s) = 1 := Ring.mul_inverse_cancel _ (hΩu s hs)
    refine (((hΩ s hs).fun_mul (hW s hs)).mul_const c).congr_deriv ?_
    unfold gaugeTransform
    calc (Ω' s * W s + Ω s * ((Ring.inverse (Ω s) * A s * Ω s - Ring.inverse (Ω s) * Ω' s)
          * W s)) * c
        = (Ω' s * W s + ((Ω s * Ring.inverse (Ω s)) * A s * Ω s * W s
            - (Ω s * Ring.inverse (Ω s)) * Ω' s * W s)) * c := by noncomm_ring
      _ = A s * (Ω s * W s * c) := by rw [e]; noncomm_ring
  have h0 : U 0 = Ω 0 * W 0 * c := by
    rw [hU0, hW0, mul_one]; exact (Ring.mul_inverse_cancel _ (hΩu 0 h0mem)).symm
  intro s hs
  exact (transport_unique A U (fun t => Ω t * W t * c) hA hU hY h0 hs).symm

/-- **`thm:continuous_path_integral` (iii), general law at `s = 1`:**
`W(1) = Ω(1)⁻¹ U(1) Ω(0)` (no periodicity needed). -/
theorem holonomy_gauge_general (A Ω Ω' U W : ℝ → 𝔸) (hA : ContinuousOn A (Icc 0 1))
    (hΩ : ∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt Ω (Ω' s) (Icc 0 1) s)
    (hΩu : ∀ s ∈ Icc (0 : ℝ) 1, IsUnit (Ω s))
    (hU : ∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt U (A s * U s) (Icc 0 1) s) (hU0 : U 0 = 1)
    (hW : ∀ s ∈ Icc (0 : ℝ) 1,
      HasDerivWithinAt W (gaugeTransform A Ω Ω' s * W s) (Icc 0 1) s) (hW0 : W 0 = 1) :
    W 1 = Ring.inverse (Ω 1) * U 1 * Ω 0 := by
  have h1 : (1 : ℝ) ∈ Icc (0 : ℝ) 1 := ⟨zero_le_one, le_rfl⟩
  have h0 : (0 : ℝ) ∈ Icc (0 : ℝ) 1 := ⟨le_rfl, zero_le_one⟩
  rw [← gauge_conjugation A Ω Ω' U W hA hΩ hΩu hU hU0 hW hW0 1 h1]
  calc W 1 = (Ring.inverse (Ω 1) * Ω 1) * W 1 * (Ring.inverse (Ω 0) * Ω 0) := by
        rw [Ring.inverse_mul_cancel _ (hΩu 1 h1), Ring.inverse_mul_cancel _ (hΩu 0 h0)]; simp
    _ = Ring.inverse (Ω 1) * (Ω 1 * W 1 * Ring.inverse (Ω 0)) * Ω 0 := by noncomm_ring

/-- **`thm:continuous_path_integral` (iii), book form:** for a periodic gauge transformation
(`Ω(0) = Ω(1)`), `𝒫exp∮𝒜^Ω = Ω(0)⁻¹ (𝒫exp∮𝒜) Ω(0)`. -/
theorem holonomy_gauge (A Ω Ω' U W : ℝ → 𝔸) (hA : ContinuousOn A (Icc 0 1))
    (hΩ : ∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt Ω (Ω' s) (Icc 0 1) s)
    (hΩu : ∀ s ∈ Icc (0 : ℝ) 1, IsUnit (Ω s)) (hper : Ω 0 = Ω 1)
    (hU : ∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt U (A s * U s) (Icc 0 1) s) (hU0 : U 0 = 1)
    (hW : ∀ s ∈ Icc (0 : ℝ) 1,
      HasDerivWithinAt W (gaugeTransform A Ω Ω' s * W s) (Icc 0 1) s) (hW0 : W 0 = 1) :
    W 1 = Ring.inverse (Ω 0) * U 1 * Ω 0 := by
  rw [holonomy_gauge_general A Ω Ω' U W hA hΩ hΩu hU hU0 hW hW0, hper]

end General

section MatrixForm

attribute [local instance] Matrix.linftyOpNormedRing Matrix.linftyOpNormedAlgebra

variable {r : ℕ}

/-- **`thm:continuous_path_integral` (iii), matrix form with the trace.** For
`𝒜, Ω : [0,1] → ℂ^{r×r}`, `det Ω(s) ≠ 0`, `Ω(0) = Ω(1)`, `U' = 𝒜U`, `U(0) = I`,
`W' = (Ω⁻¹𝒜Ω − Ω⁻¹Ω')W`, `W(0) = I`: `W(1) = Ω(0)⁻¹U(1)Ω(0)` and `Tr W(1) = Tr U(1)`. -/
theorem trace_holonomy_gauge_invariant (A Ω Ω' U W : ℝ → Matrix (Fin r) (Fin r) ℂ)
    (hA : ContinuousOn A (Icc 0 1))
    (hΩ : ∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt Ω (Ω' s) (Icc 0 1) s)
    (hΩu : ∀ s ∈ Icc (0 : ℝ) 1, IsUnit (Ω s).det) (hper : Ω 0 = Ω 1)
    (hU : ∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt U (A s * U s) (Icc 0 1) s) (hU0 : U 0 = 1)
    (hW : ∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt W
      (((Ω s)⁻¹ * A s * Ω s - (Ω s)⁻¹ * Ω' s) * W s) (Icc 0 1) s) (hW0 : W 0 = 1) :
    W 1 = (Ω 0)⁻¹ * U 1 * Ω 0 ∧ Matrix.trace (W 1) = Matrix.trace (U 1) := by
  have hΩu' : ∀ s ∈ Icc (0 : ℝ) 1, IsUnit (Ω s) := fun s hs =>
    (Matrix.isUnit_iff_isUnit_det _).2 (hΩu s hs)
  have hW' : ∀ s ∈ Icc (0 : ℝ) 1,
      HasDerivWithinAt W (gaugeTransform A Ω Ω' s * W s) (Icc 0 1) s := by
    intro s hs
    simpa only [gaugeTransform, Matrix.nonsing_inv_eq_ringInverse] using hW s hs
  have key := holonomy_gauge A Ω Ω' U W hA hΩ hΩu' hper hU hU0 hW' hW0
  rw [← Matrix.nonsing_inv_eq_ringInverse] at key
  refine ⟨key, ?_⟩
  have h0 : (0 : ℝ) ∈ Icc (0 : ℝ) 1 := ⟨le_rfl, zero_le_one⟩
  rw [key, Matrix.trace_mul_comm, ← mul_assoc,
    Matrix.mul_nonsing_inv _ (hΩu 0 h0), one_mul]

end MatrixForm

/-! ### Sharpness example of (ii) -/

/-- **`thm:continuous_path_integral` (ii), sharpness example.** For `r = 1`, `𝒜 ≡ 0`,
`ℛ_j ≡ M`, the cores are `A_j = 1 + M/k²`, so `Z_k − 1 = (1 + M/k²)^k − 1`; for `M > 0` and
`k ≥ 2` this exceeds `M/k` and is at most `(M/k)e^{M/k}`. The hypothesis `M > 0` is implicit in
the book (for `M = 0` the error is `0`, not `> 0`). -/
theorem sharpness_example (M : ℝ) (hM : 0 < M) (k : ℕ) (hk : 2 ≤ k) :
    (∏ _j ∈ Finset.range k, (1 + (1 / (k : ℝ)) * 0 + (1 / (k : ℝ) ^ 2) * M)) - 1
      = (1 + M / (k : ℝ) ^ 2) ^ k - 1 ∧
    M / k < (1 + M / (k : ℝ) ^ 2) ^ k - 1 ∧
    (1 + M / (k : ℝ) ^ 2) ^ k - 1 ≤ M / k * Real.exp (M / k) := by
  have hk0 : (0 : ℝ) < k := by exact_mod_cast (by omega : 0 < k)
  set x : ℝ := M / (k : ℝ) ^ 2 with hx
  have hxpos : 0 < x := by positivity
  have hkx : (k : ℝ) * x = M / k := by rw [hx]; field_simp
  refine ⟨?_, ?_, ?_⟩
  · rw [Finset.prod_const, Finset.card_range]; congr 2; ring
  · -- (1+x)^k > 1 + k x for k ≥ 2, x > 0
    obtain ⟨m, rfl⟩ : ∃ m, k = m + 1 := ⟨k - 1, by omega⟩
    have hm : (1 : ℝ) ≤ m := by exact_mod_cast (by omega : 1 ≤ m)
    have hb := one_add_mul_le_pow (a := x) (by linarith) m
    have : 1 + ((m + 1 : ℕ) : ℝ) * x < (1 + x) ^ (m + 1) := by
      rw [pow_succ]; push_cast
      nlinarith [mul_le_mul_of_nonneg_right hb (by linarith : (0 : ℝ) ≤ 1 + x),
        mul_pos (by linarith : (0 : ℝ) < m) (mul_pos hxpos hxpos)]
    linarith [hkx]
  · have h1 : (1 + x) ^ k ≤ Real.exp (M / k) := by
      calc (1 + x) ^ k ≤ (Real.exp x) ^ k := by
            gcongr; linarith [Real.add_one_le_exp x]
        _ = Real.exp (k * x) := by rw [← Real.exp_nat_mul]
        _ = Real.exp (M / k) := by rw [hkx]
    have h2 : Real.exp (M / k) - 1 ≤ M / k * Real.exp (M / k) := by
      set y := M / k
      have hy := Real.add_one_le_exp (-y)
      have he : Real.exp (-y) * Real.exp y = 1 := by rw [← Real.exp_add]; simp
      nlinarith [Real.exp_pos y]
    linarith

/-! ### Non-vacuity witnesses -/

/-- Scalar data used by the witnesses: `𝒜 ≡ 1`, `Ω(s) = 1 + s` (not periodic), so
`𝒜^Ω(s) = 1 − 1/(1+s)`, `U(s) = e^s`, `W(s) = e^s/(1+s)`. -/
theorem witness_general :
    let A : ℝ → ℝ := fun _ => 1
    let Ω : ℝ → ℝ := fun s => 1 + s
    let Ω' : ℝ → ℝ := fun _ => 1
    let U : ℝ → ℝ := fun s => Real.exp s
    let W : ℝ → ℝ := fun s => Real.exp s / (1 + s)
    ContinuousOn A (Icc 0 1) ∧
    (∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt Ω (Ω' s) (Icc 0 1) s) ∧
    (∀ s ∈ Icc (0 : ℝ) 1, IsUnit (Ω s)) ∧
    (∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt U (A s * U s) (Icc 0 1) s) ∧ U 0 = 1 ∧
    (∀ s ∈ Icc (0 : ℝ) 1,
      HasDerivWithinAt W (gaugeTransform A Ω Ω' s * W s) (Icc 0 1) s) ∧ W 0 = 1 ∧
    gaugeTransform A Ω Ω' 1 ≠ A 1 ∧
    W 1 = Ring.inverse (Ω 1) * U 1 * Ω 0 ∧ W 1 ≠ Ring.inverse (Ω 0) * U 1 * Ω 0 := by
  intro A Ω Ω' U W
  have hne : ∀ s ∈ Icc (0 : ℝ) 1, (1 + s) ≠ 0 := fun s hs => by linarith [hs.1]
  refine ⟨continuousOn_const, ?_, ?_, ?_, by simp [U], ?_, by simp [W], ?_, ?_, ?_⟩
  · intro s _
    exact ((hasDerivAt_id s).const_add 1).hasDerivWithinAt
  · intro s hs; exact isUnit_iff_ne_zero.2 (hne s hs)
  · intro s _
    simpa [A, U] using (Real.hasDerivAt_exp s).hasDerivWithinAt
  · intro s hs
    have h1 := hne s hs
    have hd : HasDerivAt W ((Real.exp s * (1 + s) - Real.exp s * 1) / (1 + s) ^ 2) s :=
      (Real.hasDerivAt_exp s).div ((hasDerivAt_id s).const_add 1) h1
    refine hd.hasDerivWithinAt.congr_deriv ?_
    simp only [gaugeTransform, A, Ω, Ω', W, Ring.inverse_eq_inv']
    field_simp
  · simp only [gaugeTransform, A, Ω, Ω', Ring.inverse_eq_inv']; norm_num
  · simp only [W, U, Ω, Ring.inverse_eq_inv']; field_simp; ring
  · simp only [W, U, Ω, Ring.inverse_eq_inv']
    have := Real.exp_pos 1
    norm_num
    intro h
    field_simp at h
    linarith

/-- Witness for the book form with a periodic, non-constant gauge: `𝒜 ≡ 1`,
`Ω(s) = 1 + s − s²` (`Ω(0) = Ω(1) = 1`), `W(s) = e^s/Ω(s)`; then `W(1) = Ω(0)⁻¹U(1)Ω(0) = e`. -/
theorem witness_periodic :
    let A : ℝ → ℝ := fun _ => 1
    let Ω : ℝ → ℝ := fun s => 1 + s - s ^ 2
    let Ω' : ℝ → ℝ := fun s => 1 - 2 * s
    let U : ℝ → ℝ := fun s => Real.exp s
    let W : ℝ → ℝ := fun s => Real.exp s / (1 + s - s ^ 2)
    (∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt Ω (Ω' s) (Icc 0 1) s) ∧
    (∀ s ∈ Icc (0 : ℝ) 1, IsUnit (Ω s)) ∧ Ω 0 = Ω 1 ∧
    (∀ s ∈ Icc (0 : ℝ) 1,
      HasDerivWithinAt W (gaugeTransform A Ω Ω' s * W s) (Icc 0 1) s) ∧ W 0 = 1 ∧
    gaugeTransform A Ω Ω' 0 ≠ A 0 ∧
    W 1 = Ring.inverse (Ω 0) * U 1 * Ω 0 := by
  intro A Ω Ω' U W
  have hpos : ∀ s ∈ Icc (0 : ℝ) 1, 0 < 1 + s - s ^ 2 := fun s hs => by
    nlinarith [hs.1, hs.2]
  refine ⟨?_, ?_, by simp [Ω], ?_, by simp [W], ?_, ?_⟩
  · intro s _
    have := (((hasDerivAt_id s).const_add 1).sub (hasDerivAt_pow 2 s))
    refine this.hasDerivWithinAt.congr_deriv ?_
    simp [Ω']
  · intro s hs; exact isUnit_iff_ne_zero.2 (hpos s hs).ne'
  · intro s hs
    have h1 := (hpos s hs).ne'
    have hΩd : HasDerivAt (fun x : ℝ => 1 + x - x ^ 2) (1 - 2 * s) s := by
      have := ((hasDerivAt_id' s).const_add 1).fun_sub (hasDerivAt_pow 2 s)
      refine this.congr_deriv ?_
      norm_num
    have hd : HasDerivAt W ((Real.exp s * (1 + s - s ^ 2) - Real.exp s * (1 - 2 * s))
        / (1 + s - s ^ 2) ^ 2) s := (Real.hasDerivAt_exp s).div hΩd h1
    refine hd.hasDerivWithinAt.congr_deriv ?_
    simp only [gaugeTransform, A, Ω, Ω', W, Ring.inverse_eq_inv']
    field_simp
  · simp only [gaugeTransform, A, Ω, Ω', Ring.inverse_eq_inv']; norm_num
  · simp only [W, U, Ω, Ring.inverse_eq_inv']; norm_num

/-- Witness for the sharpness example at `M = 1`, `k = 2`: error `9/16`, between `1/2` and
`(1/2)e^{1/2}`. -/
example : (1 : ℝ) / 2 < (1 + 1 / (2 : ℝ) ^ 2) ^ 2 - 1 ∧
    (1 + 1 / (2 : ℝ) ^ 2) ^ 2 - 1 = 9 / 16 := by
  have := (sharpness_example 1 one_pos 2 le_rfl).2.1
  norm_num at this ⊢

/-! ### Mutants (negations proved) -/

/-- Mutant 1: the general law fails if the sign of the inhomogeneous term is flipped
(`𝒜^Ω = Ω⁻¹𝒜Ω + Ω⁻¹Ω'`): with `𝒜 ≡ 1`, `Ω = 1 + s`, the solution is `W = e^s(1+s)` and
`W(1) = 2e ≠ e/2 = Ω(1)⁻¹U(1)Ω(0)`. -/
theorem mutant_wrong_sign_false :
    ¬ ∀ (A Ω Ω' U W : ℝ → ℝ), ContinuousOn A (Icc 0 1) →
      (∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt Ω (Ω' s) (Icc 0 1) s) →
      (∀ s ∈ Icc (0 : ℝ) 1, IsUnit (Ω s)) →
      (∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt U (A s * U s) (Icc 0 1) s) → U 0 = 1 →
      (∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt W
        ((Ring.inverse (Ω s) * A s * Ω s + Ring.inverse (Ω s) * Ω' s) * W s) (Icc 0 1) s) →
      W 0 = 1 → W 1 = Ring.inverse (Ω 1) * U 1 * Ω 0 := by
  intro h
  have hne : ∀ s ∈ Icc (0 : ℝ) 1, (1 + s) ≠ 0 := fun s hs => by linarith [hs.1]
  have := h (fun _ => 1) (fun s => 1 + s) (fun _ => 1) Real.exp (fun s => Real.exp s * (1 + s))
    continuousOn_const
    (fun s _ => ((hasDerivAt_id s).const_add 1).hasDerivWithinAt)
    (fun s hs => isUnit_iff_ne_zero.2 (hne s hs))
    (fun s _ => by simpa using (Real.hasDerivAt_exp s).hasDerivWithinAt) (by simp)
    (fun s hs => by
      have h1 := hne s hs
      refine ((Real.hasDerivAt_exp s).mul ((hasDerivAt_id s).const_add 1)).hasDerivWithinAt
        |>.congr_deriv ?_
      simp only [Ring.inverse_eq_inv', id]
      field_simp)
    (by simp)
  simp only [Ring.inverse_eq_inv'] at this
  have he := Real.exp_pos 1
  norm_num at this
  field_simp at this
  linarith

/-- Mutant 2: the book's periodic form `W(1) = Ω(0)⁻¹U(1)Ω(0)` fails without `Ω(0) = Ω(1)`
(data of `witness_general`). -/
theorem mutant_no_periodicity_false :
    ¬ ∀ (A Ω Ω' U W : ℝ → ℝ), ContinuousOn A (Icc 0 1) →
      (∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt Ω (Ω' s) (Icc 0 1) s) →
      (∀ s ∈ Icc (0 : ℝ) 1, IsUnit (Ω s)) →
      (∀ s ∈ Icc (0 : ℝ) 1, HasDerivWithinAt U (A s * U s) (Icc 0 1) s) → U 0 = 1 →
      (∀ s ∈ Icc (0 : ℝ) 1,
        HasDerivWithinAt W (gaugeTransform A Ω Ω' s * W s) (Icc 0 1) s) →
      W 0 = 1 → W 1 = Ring.inverse (Ω 0) * U 1 * Ω 0 := by
  intro h
  obtain ⟨h1, h2, h3, h4, h5, h6, h7, -, -, h10⟩ := witness_general
  exact h10 (h _ _ _ _ _ h1 h2 h3 h4 h5 h6 h7)

/-- Mutant 3: the sharpness example without the factor `e^{M/k}`, i.e. error `≤ M/k`, is false
(`M = 1`, `k = 2`). -/
theorem mutant_no_exp_factor_false :
    ¬ ∀ (M : ℝ), 0 < M → ∀ k : ℕ, 2 ≤ k → (1 + M / (k : ℝ) ^ 2) ^ k - 1 ≤ M / k := by
  intro h
  have := h 1 one_pos 2 le_rfl
  norm_num at this

/-- Mutant 4: the strict inequality needs `M > 0` (at `M = 0` the error is `0 = M/k`). -/
theorem mutant_M_zero_false :
    ¬ ∀ (M : ℝ), 0 ≤ M → ∀ k : ℕ, 2 ≤ k → M / k < (1 + M / (k : ℝ) ^ 2) ^ k - 1 := by
  intro h
  have := h 0 le_rfl 2 le_rfl
  norm_num at this

end LeanReal.Chap02PathIntegral

#print axioms LeanReal.Chap02PathIntegral.transport_unique
#print axioms LeanReal.Chap02PathIntegral.gauge_conjugation
#print axioms LeanReal.Chap02PathIntegral.holonomy_gauge_general
#print axioms LeanReal.Chap02PathIntegral.holonomy_gauge
#print axioms LeanReal.Chap02PathIntegral.trace_holonomy_gauge_invariant
#print axioms LeanReal.Chap02PathIntegral.sharpness_example
#print axioms LeanReal.Chap02PathIntegral.witness_general
#print axioms LeanReal.Chap02PathIntegral.witness_periodic
#print axioms LeanReal.Chap02PathIntegral.mutant_wrong_sign_false
#print axioms LeanReal.Chap02PathIntegral.mutant_no_periodicity_false
#print axioms LeanReal.Chap02PathIntegral.mutant_no_exp_factor_false
#print axioms LeanReal.Chap02PathIntegral.mutant_M_zero_false
