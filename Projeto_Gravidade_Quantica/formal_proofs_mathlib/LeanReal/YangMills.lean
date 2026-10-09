import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Algebra.Order.Star.Real
import Mathlib.Analysis.InnerProductSpace.Projection.Minimal

/-!
# Yang–Mills paper (Zenodo concept DOI 10.5281/zenodo.22301093)

Source: `Manuscritos_Avulsos/paper_yang_mills_mass_gap/paper_yang_mills_mass_gap.tex`.
The paper's main result is CONDITIONAL; nothing below concerns the mass gap. Only two elementary
statements are formalized.

## Part 1. Proposition `prop:gribov_region`, items (a) and (d), on a Galerkin truncation

Paper:
> On a finite torus (or a finite-dimensional Galerkin truncation): (a) `Ω` is convex and contains
> `0`; ... (d) for the `L²` distance, the closure `Ω̄` satisfies `reach(Ω̄) = +∞` in the sense of
> Federer.
Proof of (a) in the paper: `𝓜(tA + (1−t)B) = t𝓜(A) + (1−t)𝓜(B)`, and a convex combination of
positive operators is positive. Lemma `lem:gz_convex`(a): `𝓜_N(A) = 𝓜_N(0) + L(A)`, `L` linear,
`𝓜_N(0) > 0`.

Formal version (`gribov`, `gribov_convex`, `zero_mem_gribov`, `gribov_closure_unique_nearest`):
* `E` is any real vector space (the Galerkin space `V_N`), `M₀` a real `n×n` matrix (`𝓜_N(0)`),
  `L : E →ₗ Matrix n n ℝ` linear, and `Ω = {A | (M₀ + L A).PosDef}`; `PosDef` includes symmetry.
  Convexity holds for every such `E`, which covers the finite-dimensional truncation.
* `0 ∈ Ω` is proved from the hypothesis `M₀.PosDef` (the paper proves `𝓜_N(0) = P_N(−∂²)P_N > 0`;
  that computation is NOT formalized).
* (d) Federer's reach is not defined in Mathlib. What is proved is the property that defines
  `reach = +∞` (Federer 1959, Def. 4.1): EVERY point `x` of the space has a UNIQUE nearest point
  in `Ω̄`. `E` is assumed to be a complete real inner-product space (finite-dimensional `V_N` with
  the `L²` product is one).
* NOT covered: the construction of `𝓜_N` from the Faddeev–Popov operator `−∂·D(A)` on a torus,
  its symmetry, items (b) and (c) (cited results), openness of `Ω` and `reach(Ω) = 0`,
  and anything in infinite dimensions beyond what the abstract statement gives.

## Part 2. Proposition `prop:amgm_tree` (tree-level estimate at `A = 0`)

Paper:
> Its kernel satisfies `k² + λ⁴/k² ≥ 2λ²`, with equality exactly at `k = λ`, which is also the
> maximum of `D(k)` [`D(k) = k²/(k⁴+λ⁴)`].
Formal version: `tree_level_bound`, `tree_level_eq_iff`, `propagator_max`.
* `k > 0`, `λ > 0` are real numbers (momentum modulus and Gribov mass).
* The maximum of `D` is proved directly (`D(k) ≤ D(λ)` for all `k > 0`, with equality iff
  `k = λ`); the paper argues via `D'(λ) = 0`. The formal statement is a global maximum on
  `k > 0`, which implies the paper's claim.
* NOT covered: the derivation of the quadratic part of the GZ action (integration over auxiliary
  fields, `f^{abc}f^{dbc} = Nδ^{ad}`, Fourier normalisation).
-/

namespace LeanReal.YangMills

open Matrix

/-! ### Part 1: convexity of the truncated Gribov region -/

section Gribov

variable {E : Type*} [AddCommGroup E] [Module ℝ E] {n : Type*} [Fintype n]

/-- Truncated Gribov region `Ω_N = {A | 𝓜_N(0) + L(A) > 0}`. -/
def gribov (M₀ : Matrix n n ℝ) (L : E →ₗ[ℝ] Matrix n n ℝ) : Set E :=
  {A | (M₀ + L A).PosDef}

omit [Fintype n] in
/-- Prop. `prop:gribov_region`(a), convexity. -/
theorem gribov_convex (M₀ : Matrix n n ℝ) (L : E →ₗ[ℝ] Matrix n n ℝ) :
    Convex ℝ (gribov M₀ L) := by
  intro x hx y hy a b ha hb hab
  have hx' : (M₀ + L x).PosDef := hx
  have hy' : (M₀ + L y).PosDef := hy
  show (M₀ + L (a • x + b • y)).PosDef
  have e : M₀ + L (a • x + b • y) = a • (M₀ + L x) + b • (M₀ + L y) := by
    rw [map_add, map_smul, map_smul, smul_add, smul_add]
    have h0 : M₀ = a • M₀ + b • M₀ := by rw [← add_smul, hab, one_smul]
    conv_lhs => rw [h0]
    abel
  rw [e]
  rcases ha.lt_or_eq with ha' | ha'
  · exact (hx'.smul ha').add_posSemidef (hy'.posSemidef.smul hb)
  · subst ha'
    have hb1 : b = 1 := by linarith
    subst hb1
    simpa using hy'

omit [Fintype n] in
/-- Prop. `prop:gribov_region`(a), `0 ∈ Ω`, from `𝓜_N(0) > 0`. -/
theorem zero_mem_gribov (M₀ : Matrix n n ℝ) (L : E →ₗ[ℝ] Matrix n n ℝ) (h₀ : M₀.PosDef) :
    (0 : E) ∈ gribov M₀ L := by
  show (M₀ + L 0).PosDef
  simpa using h₀

end Gribov

section Reach

variable {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℝ F] [CompleteSpace F]

/-- Unique nearest point in a nonempty closed convex subset of a real Hilbert space. -/
theorem unique_nearest_of_closed_convex {K : Set F} (hne : K.Nonempty) (hcl : IsClosed K)
    (hK : Convex ℝ K) (x : F) :
    ∃! y, y ∈ K ∧ ‖x - y‖ = ⨅ w : K, ‖x - (w : F)‖ := by
  obtain ⟨v, hv, hmin⟩ := exists_norm_eq_iInf_of_complete_convex hne hcl.isComplete hK x
  refine ⟨v, ⟨hv, hmin⟩, ?_⟩
  rintro y ⟨hy, hymin⟩
  have h1 := (norm_eq_iInf_iff_real_inner_le_zero hK hv).mp hmin y hy
  have h2 := (norm_eq_iInf_iff_real_inner_le_zero hK hy).mp hymin v hv
  have e1 : x - v = (x - y) + (y - v) := by abel
  have e2 : v - y = -(y - v) := by abel
  rw [e1, inner_add_left] at h1
  rw [e2, inner_neg_right] at h2
  have : inner ℝ (y - v) (y - v) ≤ 0 := by linarith
  exact sub_eq_zero.mp (real_inner_self_nonpos.mp this)

variable {n : Type*} [Fintype n]

omit [Fintype n] in
/-- Prop. `prop:gribov_region`(d): every point has a unique nearest point in `Ω̄`
(Federer's `reach(Ω̄) = +∞`). -/
theorem gribov_closure_unique_nearest (M₀ : Matrix n n ℝ) (L : F →ₗ[ℝ] Matrix n n ℝ)
    (h₀ : M₀.PosDef) (x : F) :
    ∃! y, y ∈ closure (gribov M₀ L) ∧
      ‖x - y‖ = ⨅ w : closure (gribov M₀ L), ‖x - (w : F)‖ :=
  unique_nearest_of_closed_convex ⟨0, subset_closure (zero_mem_gribov M₀ L h₀)⟩
    isClosed_closure (gribov_convex M₀ L).closure x

end Reach

/-! Non-vacuity: `E = ℝ`, `n = 1`, `M₀ = 1`, `L(a) = a·1`: `Ω = (−1, ∞)`. -/

/-- The linear map `a ↦ a • 1`. -/
noncomputable def Lex : ℝ →ₗ[ℝ] Matrix (Fin 1) (Fin 1) ℝ :=
  LinearMap.smulRight LinearMap.id 1

lemma mem_gribov_ex (a : ℝ) : a ∈ gribov (1 : Matrix (Fin 1) (Fin 1) ℝ) Lex ↔ -1 < a := by
  have e : (1 : Matrix (Fin 1) (Fin 1) ℝ) + Lex a = diagonal (fun _ => 1 + a) := by
    ext i j; fin_cases i; fin_cases j; simp [Lex]
  show (1 + Lex a).PosDef ↔ _
  rw [e, posDef_diagonal_iff]
  constructor
  · intro h; linarith [h 0]
  · intro h _; linarith

example : (0 : ℝ) ∈ gribov (1 : Matrix (Fin 1) (Fin 1) ℝ) Lex ∧
    (5 : ℝ) ∈ gribov (1 : Matrix (Fin 1) (Fin 1) ℝ) Lex ∧
    (-2 : ℝ) ∉ gribov (1 : Matrix (Fin 1) (Fin 1) ℝ) Lex := by
  refine ⟨(mem_gribov_ex 0).mpr (by norm_num), (mem_gribov_ex 5).mpr (by norm_num), ?_⟩
  rw [mem_gribov_ex]; norm_num

example (x : ℝ) : ∃! y, y ∈ closure (gribov (1 : Matrix (Fin 1) (Fin 1) ℝ) Lex) ∧
    ‖x - y‖ = ⨅ w : closure (gribov (1 : Matrix (Fin 1) (Fin 1) ℝ) Lex), ‖x - (w : ℝ)‖ :=
  gribov_closure_unique_nearest _ Lex PosDef.one x

/-- Negative control: convexity FAILS if the pencil is not affine. With `𝓜(x) = diag(x² − 1)`
the set `{x | 𝓜(x) > 0} = {|x| > 1}` contains `±2` but not `0`. -/
theorem mutant_gribov_nonaffine :
    ¬ ∀ f : ℝ → Matrix (Fin 1) (Fin 1) ℝ, Convex ℝ {x | (f x).PosDef} := by
  intro h
  have hc := h (fun x => diagonal (fun _ => x ^ 2 - 1))
  have m2 : (2 : ℝ) ∈ {x : ℝ | (diagonal (fun _ : Fin 1 => x ^ 2 - 1)).PosDef} := by
    show (diagonal _).PosDef
    rw [posDef_diagonal_iff]; intro; norm_num
  have mm2 : (-2 : ℝ) ∈ {x : ℝ | (diagonal (fun _ : Fin 1 => x ^ 2 - 1)).PosDef} := by
    show (diagonal _).PosDef
    rw [posDef_diagonal_iff]; intro; norm_num
  have := hc m2 mm2 (by norm_num : (0 : ℝ) ≤ 1 / 2) (by norm_num : (0 : ℝ) ≤ 1 / 2)
    (by norm_num)
  have hz : (1 / 2 : ℝ) • (2 : ℝ) + (1 / 2 : ℝ) • (-2 : ℝ) = 0 := by norm_num
  rw [hz] at this
  have := (posDef_diagonal_iff.mp this) 0
  norm_num at this

/-! ### Part 2: tree-level estimate -/

/-- Prop. `prop:amgm_tree`: `k² + λ⁴/k² ≥ 2λ²`. -/
theorem tree_level_bound (k l : ℝ) (hk : 0 < k) : 2 * l ^ 2 ≤ k ^ 2 + l ^ 4 / k ^ 2 := by
  have hk2 : 0 < k ^ 2 := by positivity
  rw [← sub_nonneg]
  have e : k ^ 2 + l ^ 4 / k ^ 2 - 2 * l ^ 2 = (k ^ 2 - l ^ 2) ^ 2 / k ^ 2 := by
    field_simp; ring
  rw [e]; positivity

/-- Equality exactly at `k = λ` (for `k, λ > 0`). -/
theorem tree_level_eq_iff (k l : ℝ) (hk : 0 < k) (hl : 0 < l) :
    k ^ 2 + l ^ 4 / k ^ 2 = 2 * l ^ 2 ↔ k = l := by
  have hk2 : 0 < k ^ 2 := by positivity
  have e : k ^ 2 + l ^ 4 / k ^ 2 - 2 * l ^ 2 = (k ^ 2 - l ^ 2) ^ 2 / k ^ 2 := by
    field_simp; ring
  constructor
  · intro h
    have h0 : (k ^ 2 - l ^ 2) ^ 2 / k ^ 2 = 0 := by rw [← e]; linarith
    have h1 : (k ^ 2 - l ^ 2) ^ 2 = 0 := by
      rcases div_eq_zero_iff.mp h0 with h | h
      · exact h
      · exact absurd h hk2.ne'
    have h2 : k ^ 2 = l ^ 2 := by nlinarith [pow_eq_zero_iff (n := 2) (two_ne_zero) |>.mp h1]
    nlinarith [sq_nonneg (k - l), sq_nonneg (k + l)]
  · rintro rfl
    field_simp; ring

/-- Tree-level propagator `D(k) = k²/(k⁴+λ⁴)`. -/
noncomputable def D (l k : ℝ) : ℝ := k ^ 2 / (k ^ 4 + l ^ 4)

/-- `D` has its maximum over `k > 0` exactly at `k = λ`. -/
theorem propagator_max (k l : ℝ) (hk : 0 < k) (hl : 0 < l) :
    D l k ≤ D l l ∧ (D l k = D l l ↔ k = l) := by
  have hden : 0 < k ^ 4 + l ^ 4 := by positivity
  have hl4 : 0 < l ^ 4 + l ^ 4 := by positivity
  have key : D l l - D l k = (k ^ 2 - l ^ 2) ^ 2 / (2 * l ^ 2 * (k ^ 4 + l ^ 4)) := by
    unfold D; field_simp; ring
  have hden2 : 0 < 2 * l ^ 2 * (k ^ 4 + l ^ 4) := by positivity
  refine ⟨?_, ?_⟩
  · have : 0 ≤ D l l - D l k := by rw [key]; positivity
    linarith
  · constructor
    · intro h
      have h0 : (k ^ 2 - l ^ 2) ^ 2 / (2 * l ^ 2 * (k ^ 4 + l ^ 4)) = 0 := by
        rw [← key]; linarith
      have h1 : (k ^ 2 - l ^ 2) ^ 2 = 0 := by
        rcases div_eq_zero_iff.mp h0 with h | h
        · exact h
        · exact absurd h hden2.ne'
      have h2 : k ^ 2 = l ^ 2 := by nlinarith [pow_eq_zero_iff (n := 2) (two_ne_zero) |>.mp h1]
      nlinarith [sq_nonneg (k - l), sq_nonneg (k + l)]
    · rintro rfl; rfl

/-! Non-vacuity: `λ = 1`, `k = 2`: `4 + 1/4 > 2`; `k = λ = 3`: equality. -/
example : 2 * (1 : ℝ) ^ 2 < 2 ^ 2 + 1 ^ 4 / 2 ^ 2 := by norm_num
example : (3 : ℝ) ^ 2 + 3 ^ 4 / 3 ^ 2 = 2 * 3 ^ 2 := (tree_level_eq_iff 3 3 (by norm_num) (by norm_num)).mpr rfl

/-- Negative control: the constant `2` cannot be raised to `3` (`k = λ = 1`). -/
theorem mutant_tree_level :
    ¬ ∀ k l : ℝ, 0 < k → 3 * l ^ 2 ≤ k ^ 2 + l ^ 4 / k ^ 2 := by
  intro h
  have := h 1 1 one_pos
  norm_num at this

end LeanReal.YangMills

#print axioms LeanReal.YangMills.gribov_convex
#print axioms LeanReal.YangMills.zero_mem_gribov
#print axioms LeanReal.YangMills.unique_nearest_of_closed_convex
#print axioms LeanReal.YangMills.gribov_closure_unique_nearest
#print axioms LeanReal.YangMills.mutant_gribov_nonaffine
#print axioms LeanReal.YangMills.tree_level_bound
#print axioms LeanReal.YangMills.tree_level_eq_iff
#print axioms LeanReal.YangMills.propagator_max
#print axioms LeanReal.YangMills.mutant_tree_level
