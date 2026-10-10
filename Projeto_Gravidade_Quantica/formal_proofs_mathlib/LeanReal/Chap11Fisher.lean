import LeanReal.BeyondSpectrum3_T2
import LeanReal.BeyondSpectrum2_G2
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.SpecialFunctions.Log.Deriv

/-!
# Chapter 11: relative-entropy Hessian, first law, and Kubo–Mori versus SLD (batch B7)

Source: `unified_quantum_gravity_book/chap11_emergent_spacetime_tensor_networks_holonomies.tex`,
section "Quantum information geometry" (finite dimension, full-rank states), items:

* `prop:relative_entropy_hessian` (plan 11.1). For `ρ(λ) = ρ₀ + λX`, `X = X†`, `Tr X = 0`:
  `d/dλ S(ρ(λ)‖ρ₀)|₀ = 0` and `d²/dλ² S(ρ(λ)‖ρ₀)|₀ = g^BKM_{ρ₀}(X, X)`,
  with `S(ρ‖σ) = Tr ρ log ρ − Tr ρ log σ`.
* `thm:first_law_entanglement` (plan 11.2). For `ρ = σ + δρ`, `Tr δρ = 0`, the first-order variation
  of the von Neumann entropy is `δS = Tr(δρ H_σ)`, `H_σ = −log σ`.
* `rem:sld_vs_bkm`. In an eigenbasis `ρ₀ = ∑ p_i |i⟩⟨i|`:
  `g^SLD(X,X) = ∑_{ij} 2/(p_i+p_j) |X_ij|²`,
  `g^BKM(X,X) = ∑_{ij} (log p_i − log p_j)/(p_i − p_j) |X_ij|²` (read as `1/p_i` when `p_i = p_j`);
  `g^BKM(X,X) ≥ g^SLD(X,X)`, with equality iff `X_ij = 0` whenever `p_i ≠ p_j`, i.e. `[ρ₀, X] = 0`.

## Declared reductions

* **11.1 and 11.2: commuting case only.** `ρ₀ = diag p` (`p_i > 0`) and `X = diag x` (`x` real) in
  the same basis. Then `S(ρ(λ)‖ρ₀) = ∑ q_i log q_i − q_i log p_i` with `q = p + λx` (Kullback–Leibler),
  and the von Neumann entropy is `∑ negMulLog q_i` (`vnS_diagonal` of `BeyondSpectrum3_T2`). The
  general, non-commuting case needs the Fréchet derivative of the matrix logarithm, which Mathlib
  lacks; it is NOT covered.
* `g^BKM` is formalised through the remark's eigenbasis formula (`gBKM`), not through the
  integral `∫₀^∞ Tr(X(s+ρ)⁻¹X(s+ρ)⁻¹) ds` of `prop:relative_entropy_hessian`; the equality of the two
  forms is not proved here. In the commuting case the Hessian is shown equal to `gBKM p (diag x)`.
* `g^SLD` is the remark's eigenbasis formula (`gSLD`); `gSLD_eq_qfi` links it to the book's
  definition `½ Tr(ρ{L, L})` (SLD equation) via the eigenbasis lemma of `BeyondSpectrum2_G2`.
* The book assumes `Tr ρ₀ = 1`. This is not used by any proof below; the source form with
  `∑ p_i = 1` is given as a corollary (`relEnt_hessian_commuting_density`).
* No hypothesis stands in for missing theory: operator monotonicity and Petz's classification are
  not needed for the eigenbasis inequality, which is the scalar inequality
  "logarithmic mean < arithmetic mean", proved here.

## Finding (imprecision in `rem:sld_vs_bkm`)

"In that case both reduce to the classical Fisher–Rao metric `∑ X_ii²/p_i`" holds in an eigenbasis
that also diagonalises `X`; it is false in an arbitrary eigenbasis of a degenerate `ρ₀`:
`p = (1/2, 1/2)`, `X = [[0,1],[1,0]]` commutes with `ρ₀`, `g^SLD = g^BKM = 4`, but `∑ X_ii²/p_i = 0`
(`fisherRao_needs_joint_basis`).
-/

noncomputable section

namespace LeanReal.Chap11Fisher

open Matrix Real Filter Topology LeanReal.BeyondSpectrum3T2
open scoped ComplexConjugate

variable {n : Type*} [Fintype n] [DecidableEq n]

/-! ## 1. Relative entropy in the commuting case (`prop:relative_entropy_hessian`) -/

/-- Relative entropy of commuting (simultaneously diagonal) states `diag q`, `diag p`:
`S(q‖p) = ∑ q_i log q_i − q_i log p_i`, i.e. `Tr ρ log ρ − Tr ρ log σ` in a common eigenbasis. -/
def relEntDiag (p q : n → ℝ) : ℝ := ∑ i, (q i * Real.log (q i) - q i * Real.log (p i))

/-- Link to the entropy API: `S(q‖p) = −S_vN(diag q) − ∑ q_i log p_i`. -/
theorem relEntDiag_eq_vnS (p q : n → ℝ) :
    relEntDiag p q = -vnS (diagonal fun i => (q i : ℂ)) - ∑ i, q i * Real.log (p i) := by
  rw [vnS_diagonal, relEntDiag, Finset.sum_sub_distrib]
  simp [negMulLog, Finset.sum_neg_distrib]

/-- Kubo–Mori kernel `(log a − log b)/(a − b)`, read as `1/a` when `a = b`. -/
def logMeanInv (a b : ℝ) : ℝ := if a = b then 1 / a else (Real.log a - Real.log b) / (a - b)

/-- Kubo–Mori (BKM) metric in an eigenbasis, `∑_{ij} logMeanInv(p_i, p_j) |X_ij|²`
(`rem:sld_vs_bkm`). -/
def gBKM (p : n → ℝ) (X : Matrix n n ℂ) : ℝ :=
  ∑ i, ∑ j, logMeanInv (p i) (p j) * Complex.normSq (X i j)

/-- SLD metric in an eigenbasis, `∑_{ij} 2/(p_i + p_j) |X_ij|²` (`rem:sld_vs_bkm`). -/
def gSLD (p : n → ℝ) (X : Matrix n n ℂ) : ℝ :=
  ∑ i, ∑ j, 2 / (p i + p j) * Complex.normSq (X i j)

/-- On a diagonal `X = diag x`, the BKM metric is the Fisher–Rao form `∑ x_i²/p_i`. -/
theorem gBKM_diagonal (p x : n → ℝ) :
    gBKM p (diagonal fun i => (x i : ℂ)) = ∑ i, x i ^ 2 / p i := by
  unfold gBKM
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Finset.sum_eq_single i]
  · simp [logMeanInv, Complex.normSq_ofReal]; ring
  · intro j _ hji; simp [diagonal_apply_ne _ (Ne.symm hji)]
  · simp

omit [DecidableEq n] in
/-- First derivative of `λ ↦ S(p + λx ‖ p)` at any `λ` where `p + λx > 0` (no trace condition). -/
theorem hasDerivAt_relEnt (p x : n → ℝ) (t : ℝ) (ht : ∀ i, 0 < p i + t * x i) :
    HasDerivAt (fun s => relEntDiag p (fun i => p i + s * x i))
      (∑ i, x i * (Real.log (p i + t * x i) + 1 - Real.log (p i))) t := by
  unfold relEntDiag
  refine HasDerivAt.fun_sum (A := fun i s => (p i + s * x i) * Real.log (p i + s * x i) -
    (p i + s * x i) * Real.log (p i)) fun i _ => ?_
  have hq : HasDerivAt (fun s => p i + s * x i) (x i) t := by
    simpa using ((hasDerivAt_id t).mul_const (x i)).const_add (p i)
  have h1 := (Real.hasDerivAt_mul_log (ht i).ne').comp t hq
  have h2 := hq.mul_const (Real.log (p i))
  have e : x i * (Real.log (p i + t * x i) + 1 - Real.log (p i)) =
      (Real.log (p i + t * x i) + 1) * x i - x i * Real.log (p i) := by ring
  rw [e]
  exact h1.sub h2

omit [DecidableEq n] in
/-- Second derivative: the derivative of the first-derivative expression. -/
theorem hasDerivAt_relEnt' (p x : n → ℝ) (t : ℝ) (ht : ∀ i, 0 < p i + t * x i) :
    HasDerivAt (fun s => ∑ i, x i * (Real.log (p i + s * x i) + 1 - Real.log (p i)))
      (∑ i, x i * (x i / (p i + t * x i))) t := by
  apply HasDerivAt.fun_sum
  intro i _
  have hq : HasDerivAt (fun s => p i + s * x i) (x i) t := by
    simpa using ((hasDerivAt_id t).mul_const (x i)).const_add (p i)
  have h1 := ((hq.log (ht i).ne').add_const 1).sub_const (Real.log (p i))
  exact h1.const_mul (x i)

omit [DecidableEq n] in
/-- The set of `λ` with `p + λx > 0` is a neighbourhood of `0` when `p > 0`. -/
theorem eventually_pos (p x : n → ℝ) (hp : ∀ i, 0 < p i) :
    ∀ᶠ s in 𝓝 (0 : ℝ), ∀ i, 0 < p i + s * x i := by
  rw [eventually_all]
  intro i
  have hc : Continuous fun s : ℝ => p i + s * x i := by fun_prop
  have := hc.continuousAt (x := 0) |>.eventually (lt_mem_nhds (a := 0) (by simpa using hp i))
  exact this

/-- **`prop:relative_entropy_hessian`, commuting case, general form** (no trace condition):
`f(λ) = S(p + λx ‖ p)` has `f'(0) = ∑ x_i` and `f''(0) = ∑ x_i²/p_i = g^BKM(diag x, diag x)`. -/
theorem relEnt_derivs (p x : n → ℝ) (hp : ∀ i, 0 < p i) :
    HasDerivAt (fun s => relEntDiag p (fun i => p i + s * x i)) (∑ i, x i) 0 ∧
    HasDerivAt (deriv fun s => relEntDiag p (fun i => p i + s * x i))
      (gBKM p (diagonal fun i => (x i : ℂ))) 0 := by
  have h0 : ∀ i, 0 < p i + 0 * x i := by simpa using hp
  refine ⟨?_, ?_⟩
  · convert hasDerivAt_relEnt p x 0 h0 using 1
    simp
  · have hev : (deriv fun s => relEntDiag p (fun i => p i + s * x i)) =ᶠ[𝓝 0]
        (fun s => ∑ i, x i * (Real.log (p i + s * x i) + 1 - Real.log (p i))) :=
      (eventually_pos p x hp).mono fun s hs => (hasDerivAt_relEnt p x s hs).deriv
    have h2 := (hasDerivAt_relEnt' p x 0 h0).congr_of_eventuallyEq hev
    convert h2 using 1
    rw [gBKM_diagonal]
    refine Finset.sum_congr rfl fun i _ => ?_
    simp; ring

/-- **`prop:relative_entropy_hessian`, commuting case** (`ρ₀ = diag p`, `X = diag x`,
`p_i > 0`, `Tr X = ∑ x_i = 0`): `d/dλ S(ρ(λ)‖ρ₀)|₀ = 0` and
`d²/dλ² S(ρ(λ)‖ρ₀)|₀ = g^BKM_{ρ₀}(X, X)`. -/
theorem relEnt_hessian_commuting (p x : n → ℝ) (hp : ∀ i, 0 < p i) (hx : ∑ i, x i = 0) :
    HasDerivAt (fun s => relEntDiag p (fun i => p i + s * x i)) 0 0 ∧
    HasDerivAt (deriv fun s => relEntDiag p (fun i => p i + s * x i))
      (gBKM p (diagonal fun i => (x i : ℂ))) 0 := by
  have h := relEnt_derivs p x hp
  exact ⟨hx ▸ h.1, h.2⟩

/-- Source form of `prop:relative_entropy_hessian` (with the unused hypothesis `Tr ρ₀ = 1`). -/
theorem relEnt_hessian_commuting_density (p x : n → ℝ) (hp : ∀ i, 0 < p i)
    (_hp1 : ∑ i, p i = 1) (hx : ∑ i, x i = 0) :
    HasDerivAt (fun s => relEntDiag p (fun i => p i + s * x i)) 0 0 ∧
    HasDerivAt (deriv fun s => relEntDiag p (fun i => p i + s * x i))
      (gBKM p (diagonal fun i => (x i : ℂ))) 0 :=
  relEnt_hessian_commuting p x hp hx

/-! ## 2. First law of entanglement, commuting case (`thm:first_law_entanglement`) -/

/-- Modular Hamiltonian `H_σ = −log σ` of `σ = diag p`. -/
def modHam (p : n → ℝ) : Matrix n n ℂ := diagonal fun i => ((-Real.log (p i) : ℝ) : ℂ)

/-- `Tr(δρ H_σ) = ∑ x_i (−log p_i)` for `δρ = diag x`. -/
theorem trace_mul_modHam (p x : n → ℝ) :
    (trace ((diagonal fun i => (x i : ℂ)) * modHam p)).re = ∑ i, x i * (-Real.log (p i)) := by
  simp [modHam, diagonal_mul_diagonal, trace_diagonal, Complex.re_sum]

/-- First variation of the von Neumann entropy along `σ + λ diag x`, without a trace condition:
`δS = ∑ x_i(−log p_i) − ∑ x_i`. -/
theorem hasDerivAt_vnS_path (p x : n → ℝ) (hp : ∀ i, 0 < p i) :
    HasDerivAt (fun s => vnS (diagonal fun i => ((p i + s * x i : ℝ) : ℂ)))
      (∑ i, x i * (-Real.log (p i)) - ∑ i, x i) 0 := by
  simp_rw [vnS_diagonal]
  have : (∑ i, x i * (-Real.log (p i)) - ∑ i, x i) =
      ∑ i, (-Real.log (p i + 0 * x i) - 1) * x i := by
    rw [← Finset.sum_sub_distrib]
    refine Finset.sum_congr rfl fun i _ => ?_
    simp; ring
  rw [this]
  apply HasDerivAt.fun_sum
  intro i _
  have hq : HasDerivAt (fun s => p i + s * x i) (x i) 0 := by
    simpa using ((hasDerivAt_id (0 : ℝ)).mul_const (x i)).const_add (p i)
  have hne : p i + 0 * x i ≠ 0 := by simpa using (hp i).ne'
  exact (Real.hasDerivAt_negMulLog hne).comp 0 hq

/-- **`thm:first_law_entanglement`, commuting case** (`σ = diag p`, `p_i > 0`,
`δρ = diag x`, `Tr δρ = 0`): `d/dλ S(σ + λ δρ)|₀ = Tr(δρ H_σ)` with `H_σ = −log σ`. -/
theorem first_law_commuting (p x : n → ℝ) (hp : ∀ i, 0 < p i) (hx : ∑ i, x i = 0) :
    HasDerivAt (fun s => vnS (diagonal fun i => ((p i + s * x i : ℝ) : ℂ)))
      (trace ((diagonal fun i => (x i : ℂ)) * modHam p)).re 0 := by
  rw [trace_mul_modHam]
  have h := hasDerivAt_vnS_path p x hp
  rwa [hx, sub_zero] at h

/-! ## 3. Kubo–Mori versus SLD (`rem:sld_vs_bkm`) -/

/-- Logarithmic mean below arithmetic mean, strict form: for `0 < b < a`,
`2/(a+b) < (log a − log b)/(a − b)`. Proof: `ψ(a) = (a+b)(log a − log b) − 2(a − b)` vanishes at
`a = b` and has `ψ'(a) = log(a/b) + b/a − 1 > 0` for `a > b`. -/
theorem two_div_lt_logMean {a b : ℝ} (hb : 0 < b) (hab : b < a) :
    2 / (a + b) < (Real.log a - Real.log b) / (a - b) := by
  set ψ : ℝ → ℝ := fun y => (y + b) * (Real.log y - Real.log b) - 2 * (y - b) with hψ
  have hderiv : ∀ y, 0 < y → HasDerivAt ψ
      (1 * (Real.log y - Real.log b) + (y + b) * y⁻¹ - 2 * 1) y := by
    intro y hy
    have h1 : HasDerivAt (fun y : ℝ => y + b) 1 y := (hasDerivAt_id y).add_const b
    have h2 : HasDerivAt (fun y : ℝ => Real.log y - Real.log b) y⁻¹ y :=
      (Real.hasDerivAt_log hy.ne').sub_const _
    have h3 : HasDerivAt (fun y : ℝ => y - b) 1 y := (hasDerivAt_id y).sub_const b
    exact (h1.mul h2).sub (h3.const_mul 2)
  have hmono : StrictMonoOn ψ (Set.Ici b) := by
    apply strictMonoOn_of_deriv_pos (convex_Ici b)
    · intro y hy
      have hy0 : 0 < y := lt_of_lt_of_le hb hy
      exact (hderiv y hy0).continuousAt.continuousWithinAt
    · intro y hy
      rw [interior_Ici] at hy
      have hy0 : 0 < y := hb.trans hy
      rw [(hderiv y hy0).deriv]
      have hlog := Real.log_lt_sub_one_of_pos (div_pos hb hy0) (by
        intro h; rw [div_eq_one_iff_eq hy0.ne'] at h; exact (ne_of_lt (Set.mem_Ioi.mp hy)) h)
      rw [Real.log_div hb.ne' hy0.ne'] at hlog
      have : (y + b) * y⁻¹ = 1 + b / y := by field_simp
      rw [this]
      linarith
  have hψa := hmono (Set.mem_Ici.mpr le_rfl) (Set.mem_Ici.mpr hab.le) hab
  have hψb : ψ b = 0 := by simp [hψ]
  rw [hψb] at hψa
  simp only [hψ] at hψa
  have hs : 0 < a + b := by linarith
  have hd : 0 < a - b := by linarith
  rw [div_lt_div_iff₀ hs hd]
  linarith

theorem logMeanInv_comm (a b : ℝ) : logMeanInv a b = logMeanInv b a := by
  unfold logMeanInv
  by_cases h : a = b
  · subst h; rfl
  · simp only [h, Ne.symm h, ↓reduceIte]
    rw [← neg_div_neg_eq]
    congr 1 <;> ring

/-- Entrywise inequality with strictness: for `a, b > 0`, `a ≠ b`,
`2/(a+b) < logMeanInv a b`. -/
theorem two_div_lt_logMeanInv {a b : ℝ} (ha : 0 < a) (hb : 0 < b) (hab : a ≠ b) :
    2 / (a + b) < logMeanInv a b := by
  rcases lt_or_gt_of_ne hab with h | h
  · rw [logMeanInv_comm, add_comm]
    simp only [logMeanInv, Ne.symm hab, ↓reduceIte]
    exact two_div_lt_logMean ha h
  · simp only [logMeanInv, hab, ↓reduceIte]
    exact two_div_lt_logMean hb h

/-- Entrywise inequality `2/(a+b) ≤ logMeanInv a b` for `a, b > 0` (equality at `a = b`). -/
theorem two_div_le_logMeanInv {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    2 / (a + b) ≤ logMeanInv a b := by
  by_cases hab : a = b
  · subst hab
    rw [logMeanInv, ite_eq_left_of_eq_true _ _ (eq_self _)]
    have : a + a = 2 * a := by ring
    rw [this, div_mul_eq_div_div, div_self two_ne_zero]
  · exact (two_div_lt_logMeanInv ha hb hab).le

omit [DecidableEq n] in
/-- **`rem:sld_vs_bkm`, inequality**: `g^BKM(X,X) ≥ g^SLD(X,X)` for full-rank `ρ₀ = diag p`
and every matrix `X`. -/
theorem gSLD_le_gBKM (p : n → ℝ) (hp : ∀ i, 0 < p i) (X : Matrix n n ℂ) :
    gSLD p X ≤ gBKM p X :=
  Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j _ =>
    mul_le_mul_of_nonneg_right (two_div_le_logMeanInv (hp i) (hp j)) (Complex.normSq_nonneg _)

omit [DecidableEq n] in
/-- In the eigenbasis, `[diag p, X] = 0` iff `X_ij = 0` whenever `p_i ≠ p_j`. -/
theorem commute_diagonal_iff (p : n → ℝ) (X : Matrix n n ℂ) [DecidableEq n] :
    (diagonal fun i => (p i : ℂ)) * X = X * (diagonal fun i => (p i : ℂ)) ↔
      ∀ i j, p i ≠ p j → X i j = 0 := by
  constructor
  · intro h i j hij
    have hij' := congrFun (congrFun h i) j
    rw [diagonal_mul, mul_diagonal] at hij'
    have : ((p i : ℂ) - p j) * X i j = 0 := by rw [sub_mul, hij', mul_comm]; ring
    rcases mul_eq_zero.mp this with h0 | h0
    · exact absurd (by exact_mod_cast sub_eq_zero.mp h0) hij
    · exact h0
  · intro h
    ext i j
    rw [diagonal_mul, mul_diagonal]
    by_cases hij : p i = p j
    · rw [hij, mul_comm]
    · rw [h i j hij]; simp

omit [DecidableEq n] in
/-- **`rem:sld_vs_bkm`, equality case**: for full-rank `ρ₀ = diag p`,
`g^BKM(X,X) = g^SLD(X,X)` iff `X_ij = 0` whenever `p_i ≠ p_j`. -/
theorem gBKM_eq_gSLD_iff (p : n → ℝ) (hp : ∀ i, 0 < p i) (X : Matrix n n ℂ) :
    gBKM p X = gSLD p X ↔ ∀ i j, p i ≠ p j → X i j = 0 := by
  have hterm : ∀ i j, 0 ≤ logMeanInv (p i) (p j) * Complex.normSq (X i j) -
      2 / (p i + p j) * Complex.normSq (X i j) := fun i j => by
    rw [← sub_mul]
    exact mul_nonneg (sub_nonneg.mpr (two_div_le_logMeanInv (hp i) (hp j)))
      (Complex.normSq_nonneg _)
  have hdiff : gBKM p X - gSLD p X = ∑ i, ∑ j, (logMeanInv (p i) (p j) *
      Complex.normSq (X i j) - 2 / (p i + p j) * Complex.normSq (X i j)) := by
    simp only [gBKM, gSLD, ← Finset.sum_sub_distrib]
  constructor
  · intro h i j hij
    have h0 : ∑ i, ∑ j, (logMeanInv (p i) (p j) * Complex.normSq (X i j) -
        2 / (p i + p j) * Complex.normSq (X i j)) = 0 := by rw [← hdiff, h, sub_self]
    have hi := (Finset.sum_eq_zero_iff_of_nonneg (fun i _ =>
      Finset.sum_nonneg fun j _ => hterm i j)).mp h0 i (Finset.mem_univ _)
    have hij0 := (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => hterm i j)).mp hi j
      (Finset.mem_univ _)
    rw [← sub_mul] at hij0
    have hpos := sub_pos.mpr (two_div_lt_logMeanInv (hp i) (hp j) hij)
    rcases mul_eq_zero.mp hij0 with h1 | h1
    · exact absurd h1 hpos.ne'
    · exact Complex.normSq_eq_zero.mp h1
  · intro h
    have : gBKM p X - gSLD p X = 0 := by
      rw [hdiff]
      refine Finset.sum_eq_zero fun i _ => Finset.sum_eq_zero fun j _ => ?_
      by_cases hij : p i = p j
      · rw [← sub_mul, hij, logMeanInv, ite_eq_left_of_eq_true _ _ (eq_self _)]
        have : p j + p j = 2 * p j := by ring
        rw [this, div_mul_eq_div_div, div_self two_ne_zero]; ring
      · rw [h i j hij]; simp
    linarith

/-- **`rem:sld_vs_bkm`, equality case in commutator form**: `g^BKM = g^SLD` iff `[ρ₀, X] = 0`. -/
theorem gBKM_eq_gSLD_iff_commute (p : n → ℝ) (hp : ∀ i, 0 < p i) (X : Matrix n n ℂ) :
    gBKM p X = gSLD p X ↔
      (diagonal fun i => (p i : ℂ)) * X = X * (diagonal fun i => (p i : ℂ)) := by
  rw [gBKM_eq_gSLD_iff p hp, commute_diagonal_iff]

/-- Link to the book's definition `g^SLD = ½ Tr(ρ{L, L})` with `X = ½(ρL + Lρ)`: for Hermitian
`X` the eigenbasis formula `gSLD` equals the SLD quantum Fisher information
(via `qfi_eigen_re` of `BeyondSpectrum2_G2`). -/
theorem gSLD_eq_qfi (p : n → ℝ) (hp : ∀ i, 0 < p i) {X L : Matrix n n ℂ} (hX : X.IsHermitian)
    (hL : LeanReal.BeyondSpectrum2G2.IsSLD (LeanReal.BeyondSpectrum2G2.Λ p) X L) :
    gSLD p X = (LeanReal.BeyondSpectrum2G2.qfi (LeanReal.BeyondSpectrum2G2.Λ p) L L).re := by
  rw [LeanReal.BeyondSpectrum2G2.qfi_eigen_re hp hL hL, gSLD, Finset.mul_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun j _ => ?_
  have hji : X j i = conj (X i j) := by
    have := congrFun (congrFun hX j) i
    simpa [conjTranspose_apply] using this.symm
  rw [hji, Complex.mul_conj, Complex.ofReal_re]
  ring

/-! ## 4. Witnesses -/

/-- Off-diagonal test matrix `[[0,1],[1,0]]`. -/
def Xoff : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]

/-- Non-degenerate spectrum `p = (1/4, 3/4)`. -/
def pw : Fin 2 → ℝ := ![1 / 4, 3 / 4]

theorem pw_pos : ∀ i, 0 < pw i := by intro i; fin_cases i <;> norm_num [pw]

theorem gSLD_pw_Xoff : gSLD pw Xoff = 4 := by
  simp [gSLD, pw, Xoff, Fin.sum_univ_two]; norm_num

/-- **Witness for `rem:sld_vs_bkm`** (hypotheses bite, strict case): `p = (1/4, 3/4)`,
`X = [[0,1],[1,0]]` (Hermitian, does not commute with `diag p`): `g^SLD = 4 < g^BKM`. -/
theorem witness_strict : Xoff.IsHermitian ∧ gSLD pw Xoff = 4 ∧ gSLD pw Xoff < gBKM pw Xoff := by
  refine ⟨?_, gSLD_pw_Xoff, ?_⟩
  · ext i j; fin_cases i <;> fin_cases j <;> simp [Xoff, conjTranspose_apply]
  · refine lt_of_le_of_ne (gSLD_le_gBKM pw pw_pos Xoff) fun h => ?_
    have := (gBKM_eq_gSLD_iff pw pw_pos Xoff).mp h.symm 0 1 (by norm_num [pw])
    simp [Xoff] at this

/-- **Witness for 11.1** (commuting case): `p = (1/4, 3/4)`, `x = (1, −1)` (traceless, non-zero):
`f'(0) = 0` and `f''(0) = g^BKM = 4 + 4/3 = 16/3 ≠ 0`. -/
theorem witness_hessian :
    HasDerivAt (fun s => relEntDiag pw (fun i => pw i + s * (![1, -1] : Fin 2 → ℝ) i)) 0 0 ∧
    HasDerivAt (deriv fun s => relEntDiag pw (fun i => pw i + s * (![1, -1] : Fin 2 → ℝ) i))
      (16 / 3) 0 := by
  have h := relEnt_hessian_commuting pw ![1, -1] pw_pos (by simp [Fin.sum_univ_two])
  refine ⟨h.1, ?_⟩
  convert h.2 using 1
  rw [gBKM_diagonal]
  simp [pw, Fin.sum_univ_two]; norm_num

/-- **Witness for 11.2** (commuting case): `p = (1/4, 3/4)`, `δρ = diag(1, −1)`:
`δS = Tr(δρ H_σ) = −log(1/4) + log(3/4) = log 3 > 0`. -/
theorem witness_first_law :
    HasDerivAt (fun s => vnS (diagonal fun i => ((pw i + s * (![1, -1] : Fin 2 → ℝ) i : ℝ) : ℂ)))
      (Real.log 3) 0 ∧ 0 < Real.log 3 := by
  have h := first_law_commuting pw ![1, -1] pw_pos (by simp [Fin.sum_univ_two])
  refine ⟨?_, Real.log_pos (by norm_num)⟩
  convert h using 1
  rw [trace_mul_modHam]
  simp [pw, Fin.sum_univ_two]
  rw [Real.log_div (by norm_num) (by norm_num)]
  ring

/-! ## 5. Mutants proved false -/

/-- **Mutant 1 (11.1 without `Tr X = 0`)**: `f'(0) = 0` fails for `p = 1`, `x = 1` on one level
(`f(λ) = (1+λ) log(1+λ)`, `f'(0) = 1`). -/
theorem mutant_hessian_no_trace_false :
    ¬ ∀ p x : Fin 1 → ℝ, (∀ i, 0 < p i) →
      HasDerivAt (fun s => relEntDiag p (fun i => p i + s * x i)) 0 0 := by
  intro h
  have h1 := h (fun _ => 1) (fun _ => 1) (fun _ => one_pos)
  have h2 := (relEnt_derivs (fun _ : Fin 1 => (1 : ℝ)) (fun _ => 1) (fun _ => one_pos)).1
  have := h1.unique h2
  simp at this

/-- **Mutant 2 (11.1, wrong Hessian `∑ x_i²`, i.e. dropping `1/p_i`)**: false at the witness,
where `f''(0) = 16/3 ≠ 2`. -/
theorem mutant_hessian_no_inv_false :
    ¬ ∀ p x : Fin 2 → ℝ, (∀ i, 0 < p i) → ∑ i, x i = 0 →
      HasDerivAt (deriv fun s => relEntDiag p (fun i => p i + s * x i)) (∑ i, x i ^ 2) 0 := by
  intro h
  have h1 := h pw ![1, -1] pw_pos (by simp [Fin.sum_univ_two])
  have := h1.unique witness_hessian.2
  simp [Fin.sum_univ_two] at this
  norm_num at this

/-- **Mutant 3 (11.2 without `Tr δρ = 0`)**: `δS = Tr(δρ H_σ)` fails for `σ = 1`, `δρ = 1` on one
level (`S(λ) = negMulLog(1+λ)`, `δS = −1`, while `Tr(δρ H_σ) = −log 1 = 0`). -/
theorem mutant_first_law_no_trace_false :
    ¬ ∀ p x : Fin 1 → ℝ, (∀ i, 0 < p i) →
      HasDerivAt (fun s => vnS (diagonal fun i => ((p i + s * x i : ℝ) : ℂ)))
        (trace ((diagonal fun i => (x i : ℂ)) * modHam p)).re 0 := by
  intro h
  have h1 := h (fun _ => 1) (fun _ => 1) (fun _ => one_pos)
  have h2 := hasDerivAt_vnS_path (fun _ : Fin 1 => (1 : ℝ)) (fun _ => 1) (fun _ => one_pos)
  have := h1.unique h2
  rw [trace_mul_modHam] at this
  simp at this

/-- **Mutant 4 (`rem:sld_vs_bkm` reversed)**: `g^BKM ≤ g^SLD` for all full-rank `p` is false
(strict witness). -/
theorem mutant_reversed_false :
    ¬ ∀ (p : Fin 2 → ℝ) (X : Matrix (Fin 2) (Fin 2) ℂ), (∀ i, 0 < p i) → gBKM p X ≤ gSLD p X := by
  intro h
  have := h pw Xoff pw_pos
  linarith [witness_strict.2.2]

/-- **Mutant 5 (full rank dropped)**: the entrywise inequality fails at `a = 0`, `b = 1`:
`2/(0+1) = 2 > 0 = logMeanInv 0 1` (`log 0 = 0` in Mathlib, and `log 1 = 0`). -/
theorem mutant_no_full_rank_false :
    ¬ ∀ a b : ℝ, 0 ≤ a → 0 ≤ b → 2 / (a + b) ≤ logMeanInv a b := by
  intro h
  have := h 0 1 le_rfl zero_le_one
  simp [logMeanInv] at this
  norm_num at this

/-! ## 6. Finding: Fisher–Rao reduction needs a joint eigenbasis -/

/-- `p = (1/2, 1/2)`, `X = [[0,1],[1,0]]`: `X` commutes with `diag p` and `g^SLD = g^BKM = 4`, but
the Fisher–Rao expression `∑ X_ii²/p_i` computed in this eigenbasis is `0`. The remark's
"both reduce to `∑ X_ii²/p_i`" needs an eigenbasis that also diagonalises `X`. -/
theorem fisherRao_needs_joint_basis :
    (diagonal fun i => ((![1 / 2, 1 / 2] : Fin 2 → ℝ) i : ℂ)) * Xoff =
      Xoff * (diagonal fun i => ((![1 / 2, 1 / 2] : Fin 2 → ℝ) i : ℂ)) ∧
    gBKM ![1 / 2, 1 / 2] Xoff = 4 ∧ gSLD ![1 / 2, 1 / 2] Xoff = 4 ∧
    ∑ i, Complex.normSq (Xoff i i) / (![1 / 2, 1 / 2] : Fin 2 → ℝ) i = 0 := by
  have hp : ∀ i, 0 < (![1 / 2, 1 / 2] : Fin 2 → ℝ) i := by intro i; fin_cases i <;> norm_num
  have hc : (diagonal fun i => ((![1 / 2, 1 / 2] : Fin 2 → ℝ) i : ℂ)) * Xoff =
      Xoff * (diagonal fun i => ((![1 / 2, 1 / 2] : Fin 2 → ℝ) i : ℂ)) :=
    (commute_diagonal_iff _ _).mpr fun i j hij => by
      fin_cases i <;> fin_cases j <;> simp at hij
  have hS : gSLD ![1 / 2, 1 / 2] Xoff = 4 := by
    simp [gSLD, Xoff, Fin.sum_univ_two]; norm_num
  refine ⟨hc, ?_, hS, ?_⟩
  · rw [(gBKM_eq_gSLD_iff_commute _ hp Xoff).mpr hc, hS]
  · simp [Xoff, Fin.sum_univ_two]

end LeanReal.Chap11Fisher

#print axioms LeanReal.Chap11Fisher.relEntDiag_eq_vnS
#print axioms LeanReal.Chap11Fisher.gBKM_diagonal
#print axioms LeanReal.Chap11Fisher.relEnt_derivs
#print axioms LeanReal.Chap11Fisher.relEnt_hessian_commuting
#print axioms LeanReal.Chap11Fisher.relEnt_hessian_commuting_density
#print axioms LeanReal.Chap11Fisher.first_law_commuting
#print axioms LeanReal.Chap11Fisher.two_div_lt_logMean
#print axioms LeanReal.Chap11Fisher.gSLD_le_gBKM
#print axioms LeanReal.Chap11Fisher.gBKM_eq_gSLD_iff
#print axioms LeanReal.Chap11Fisher.gBKM_eq_gSLD_iff_commute
#print axioms LeanReal.Chap11Fisher.gSLD_eq_qfi
#print axioms LeanReal.Chap11Fisher.witness_strict
#print axioms LeanReal.Chap11Fisher.witness_hessian
#print axioms LeanReal.Chap11Fisher.witness_first_law
#print axioms LeanReal.Chap11Fisher.mutant_hessian_no_trace_false
#print axioms LeanReal.Chap11Fisher.mutant_hessian_no_inv_false
#print axioms LeanReal.Chap11Fisher.mutant_first_law_no_trace_false
#print axioms LeanReal.Chap11Fisher.mutant_reversed_false
#print axioms LeanReal.Chap11Fisher.mutant_no_full_rank_false
#print axioms LeanReal.Chap11Fisher.fisherRao_needs_joint_basis
