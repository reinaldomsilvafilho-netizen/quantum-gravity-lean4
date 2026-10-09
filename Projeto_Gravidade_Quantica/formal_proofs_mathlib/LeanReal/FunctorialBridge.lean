import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Topology.Order.DenselyOrdered

/-!
# *Functorial Bridge* (Zenodo concept DOI 10.5281/zenodo.22441676)

Source: `Manuscritos_Avulsos/paper_functorial_tensor_field_theory/paper_functorial_tensor_field_theory.tex`,
Proposition `prop:cov-nogo` ("No covariant positive lapse on constant paths"):
> Suppose a rule assigns to each path `P` on `[0,1]` a lapse `N_P` such that
> `N_{P∘α}(x,s) = α'(s) N_P(x,α(s))` for all `P` and `α ∈ Diff⁺([0,1])`. Then `N_P(x,s) = 0` for every
> constant path `P` and every `s ∈ (0,1)`. If moreover `N_P(x,·)` is continuous on `[0,1]`, then
> `N_P ≡ 0`.

Formal version (`no_covariant_lapse`, `no_covariant_lapse_continuous`).
* For a constant path `P∘α = P`, so the hypothesis becomes `N(s) = α'(s) N(α(s))` with
  `N = N_P(x,·) : ℝ → ℝ` at a fixed `x`. Only constant paths are used, exactly as in the proof.
* `IsDiffPlus α` asks: `α` smooth on `ℝ`, `α 0 = 0`, `α 1 = 1`, `α' > 0` on `[0,1]`. Its
  restriction to `[0,1]` is an element of `Diff⁺([0,1])`, so this class is a SUBSET of `Diff⁺`;
  requiring covariance only for it is a weaker hypothesis, and the formal theorem is at least as
  strong as the paper's.
* The proof uses the paper's `α(s) = s + ½ s(1−s)(s−s₀)` and proves `α ∈ IsDiffPlus`,
  `α(s₀) = s₀` and `α'(s₀) = 1 + ½ s₀(1−s₀) ≠ 1`.
* NOT covered: the cMPS paths themselves, the lapse formula of the paper, smoothness in `x`.
-/

namespace LeanReal.FunctorialBridge

open Set

/-- Restriction to `[0,1]` lies in `Diff⁺([0,1])`. -/
def IsDiffPlus (α : ℝ → ℝ) : Prop :=
  ContDiff ℝ (⊤ : ℕ∞) α ∧ α 0 = 0 ∧ α 1 = 1 ∧ ∀ s ∈ Icc (0 : ℝ) 1, 0 < deriv α s

/-- The paper's reparametrization, expanded. -/
noncomputable def alpha (s₀ : ℝ) (s : ℝ) : ℝ := s + 1 / 2 * ((1 + s₀) * s ^ 2 - s₀ * s - s ^ 3)

lemma alpha_eq_paper (s₀ s : ℝ) : alpha s₀ s = s + 1 / 2 * s * (1 - s) * (s - s₀) := by
  unfold alpha; ring

lemma hasDerivAt_alpha (s₀ s : ℝ) :
    HasDerivAt (alpha s₀) (1 + 1 / 2 * (-3 * s ^ 2 + 2 * (1 + s₀) * s - s₀)) s := by
  have h := (hasDerivAt_id' s).add
    (((((hasDerivAt_pow 2 s).const_mul (1 + s₀)).sub ((hasDerivAt_id' s).const_mul s₀)).sub
      (hasDerivAt_pow 3 s)).const_mul (1 / 2))
  convert h using 1
  · funext x; simp only [alpha, Pi.add_apply, Pi.sub_apply]
  · norm_num; ring

lemma deriv_alpha (s₀ s : ℝ) :
    deriv (alpha s₀) s = 1 + 1 / 2 * (-3 * s ^ 2 + 2 * (1 + s₀) * s - s₀) :=
  (hasDerivAt_alpha s₀ s).deriv

lemma alpha_isDiffPlus {s₀ : ℝ} (h : s₀ ∈ Ioo (0 : ℝ) 1) : IsDiffPlus (alpha s₀) := by
  obtain ⟨h0, h1⟩ := h
  refine ⟨?_, by simp [alpha], by simp [alpha], ?_⟩
  · unfold alpha; fun_prop
  · intro s ⟨hs0, hs1⟩
    rw [deriv_alpha]
    nlinarith [mul_nonneg (sub_nonneg.mpr hs1) hs0, mul_nonneg hs0 h0.le,
      mul_nonneg (sub_nonneg.mpr hs1) (sub_nonneg.mpr h1.le)]

/-- Prop. `prop:cov-nogo`, first part. -/
theorem no_covariant_lapse (N : ℝ → ℝ)
    (hcov : ∀ α, IsDiffPlus α → ∀ s ∈ Icc (0 : ℝ) 1, N s = deriv α s * N (α s)) :
    ∀ s₀ ∈ Ioo (0 : ℝ) 1, N s₀ = 0 := by
  intro s₀ hs
  have h := hcov (alpha s₀) (alpha_isDiffPlus hs) s₀ ⟨hs.1.le, hs.2.le⟩
  have hfix : alpha s₀ s₀ = s₀ := by unfold alpha; ring
  rw [hfix, deriv_alpha] at h
  have hne : 1 / 2 * s₀ * (1 - s₀) ≠ 0 := by
    have := hs.1; have := hs.2
    exact ne_of_gt (by positivity)
  have : (1 / 2 * s₀ * (1 - s₀)) * N s₀ = 0 := by linear_combination -h
  exact (mul_eq_zero.mp this).resolve_left hne

/-- Prop. `prop:cov-nogo`, second part: with continuity on `[0,1]`, `N ≡ 0` there. -/
theorem no_covariant_lapse_continuous (N : ℝ → ℝ)
    (hcov : ∀ α, IsDiffPlus α → ∀ s ∈ Icc (0 : ℝ) 1, N s = deriv α s * N (α s))
    (hc : ContinuousOn N (Icc 0 1)) :
    ∀ s ∈ Icc (0 : ℝ) 1, N s = 0 := by
  have hEq : EqOn N (fun _ => (0 : ℝ)) (Ioo 0 1) := no_covariant_lapse N hcov
  have := hEq.of_subset_closure hc continuousOn_const Ioo_subset_Icc_self
    (by rw [closure_Ioo (by norm_num : (0 : ℝ) ≠ 1)])
  exact this

/-! Non-vacuity: the class `IsDiffPlus` is inhabited (`α = alpha (1/2)`), and the hypothesis is
satisfiable (`N ≡ 0`). -/
example : IsDiffPlus (alpha (1 / 2)) := alpha_isDiffPlus ⟨by norm_num, by norm_num⟩

example : ∀ α, IsDiffPlus α → ∀ s ∈ Icc (0 : ℝ) 1,
    (fun _ : ℝ => (0 : ℝ)) s = deriv α s * (fun _ : ℝ => (0 : ℝ)) (α s) := by
  intros; simp

/-- Negative control: without the factor `α'(s)` (plain invariance `N(s) = N(α(s))`) the
conclusion is FALSE: `N ≡ 1` is invariant and non-zero. -/
theorem mutant_no_jacobian :
    ¬ ∀ N : ℝ → ℝ, (∀ α, IsDiffPlus α → ∀ s ∈ Icc (0 : ℝ) 1, N s = N (α s)) →
      ∀ s₀ ∈ Ioo (0 : ℝ) 1, N s₀ = 0 := by
  intro h
  have := h (fun _ => 1) (fun _ _ _ _ => rfl) (1 / 2) ⟨by norm_num, by norm_num⟩
  norm_num at this

end LeanReal.FunctorialBridge

#print axioms LeanReal.FunctorialBridge.alpha_isDiffPlus
#print axioms LeanReal.FunctorialBridge.no_covariant_lapse
#print axioms LeanReal.FunctorialBridge.no_covariant_lapse_continuous
#print axioms LeanReal.FunctorialBridge.mutant_no_jacobian
