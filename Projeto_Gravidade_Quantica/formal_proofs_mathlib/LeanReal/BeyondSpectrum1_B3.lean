import Mathlib.Analysis.Calculus.FDeriv.Mul
import Mathlib.Analysis.Calculus.FDeriv.Add
import Mathlib.Analysis.Calculus.FDeriv.Prod
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.LinearAlgebra.Matrix.DotProduct
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.Order.Interval.Finset.Fin

/-!
# *Beyond the Spectrum* I (Zenodo concept DOI 10.5281/zenodo.22644743), item B3

Source: `Manuscritos_Avulsos/paper_functional_realizations/paper_functional_realizations.tex`,
Theorem `thm:morse_matrix` ("Morse Spectrum of Quadratic Realizations"), with `f_A(x) = xᵀAx`:

> Let `n ≥ 1` and let `A ∈ Sym_n(ℝ)` have pairwise distinct eigenvalues `λ_1 < λ_2 < … < λ_n`.
> Then `f_A : S^{n−1} → ℝ` is a Morse function (all critical points are non-degenerate). Moreover:
> (i) `f_A` has exactly `2n` isolated critical points, occurring in antipodal pairs:
>     `Crit(f_A) = {±v_1, …, ±v_n}`, where `v_i` is the normalized eigenvector of `λ_i`.
> (ii) The Morse index of the critical points `±v_i` is given precisely by `γ(±v_i) = i − 1`.
> (iii) `P_t(f_A) = 2 ∑ t^{i−1}`; at `t = −1` this recovers `χ(S^{n−1}) = 1 − (−1)^n`.

## What is formalized (ALGEBRAIC part only)

* `fderiv_q` : the ambient derivative of `q(x) = xᵀAx` is `dq_x(h) = h·Ax + x·Ah`
  (`= 2 h·Ax` for symmetric `A`, `fderiv_q_symm`).
* `critical_iff_eigen` : for symmetric `A` and any `x`,
  `dq_x` vanishes on `x^⊥ = {h | h·x = 0}` ⟺ `Ax ∈ span{x}` (`∃ c, Ax = c x`).
  On the unit sphere `T_x S^{n−1} = x^⊥`, and the derivative of `f_A = q|_{S^{n−1}}` at `x` is the
  restriction of `dq_x` to `x^⊥`; so the critical points of `f_A` are exactly the unit
  eigenvectors. `lagrange_value` : the multiplier is `c = q(x)`.
* EIGEN-COORDINATES `A = diag(μ)` (spectral theorem; see the reduction below):
  - `crit_diag` : if `μ` is injective (distinct eigenvalues), the unit eigenvectors are exactly
    `±e_i` (`(i)`, the set `{±v_i}`); `crit_diag_ncard` : there are exactly `2n` of them.
  - `hessian_great_circle` : along the great circle `c(t) = cos t (±e_i) + sin t y`, `y ⊥ e_i`,
    `|y| = 1`, the function `t ↦ q(c(t))` has first derivative `0` and second derivative
    `2 H_i(y)` at `t = 0`, with `H_i(y) = ∑_j (μ_j − μ_i) y_j² = ∑_{j≠i} (μ_j − μ_i) y_j²`.
    This is the Hessian quadratic form of `f_A` at `±e_i` on `T S^{n−1} = e_i^⊥`
    (`hessForm_eq_sum_ne` drops the `j = i` term).
  - `hessForm_nondegenerate` : for distinct `μ`, `H_i` is non-degenerate on `e_i^⊥` (Morse).
  - `index_lower`, `index_upper` : the largest dimension of a subspace on which `H_i` is negative
    definite is `#{j | μ_j < μ_i}` (attained by `span{e_j | μ_j < μ_i} ⊆ e_i^⊥`; no subspace of
    any larger dimension is negative definite).
  - `card_lt_of_strictMono` : for `λ_1 < … < λ_n` (`Fin n`, 0-based), `#{j | λ_j < λ_i} = i`,
    i.e. the paper's `i − 1` in 1-based indexing. `morse_index_sorted` assembles (ii).

## Declared reductions / NOT covered

* No manifold structure: the sphere's tangent space is taken as `x^⊥` and its Hessian as the
  second derivative along great circles through the critical point (for a critical point of a
  function restricted to the round sphere these agree; this identification is not formalized).
* The index and Hessian statements are in EIGEN-COORDINATES (`A = diag μ`). For general
  symmetric `A` one conjugates by the orthogonal eigenvector matrix (Mathlib:
  `Matrix.IsHermitian.spectral_theorem`); that transfer is not formalized here.
* NOT covered: "Morse function" as a manifold notion, isolatedness of critical points as a
  topological statement, the Morse polynomial (iii) and the Euler characteristic
  `χ(S^{n−1}) = 1 − (−1)^n` (Morse theory on manifolds is not in Mathlib).
-/

namespace LeanReal.BeyondSpectrum1B3

open Matrix Finset Real

set_option autoImplicit false

section General

variable {n : Type*} [Fintype n]

/-- `f_A(x) = xᵀAx` (the paper's quadratic realization), on all of `ℝⁿ`. -/
def q (A : Matrix n n ℝ) (x : n → ℝ) : ℝ := x ⬝ᵥ (A *ᵥ x)

/-- `y ↦ Ay` as a continuous linear map. -/
noncomputable def mulVecCLM (A : Matrix n n ℝ) : (n → ℝ) →L[ℝ] (n → ℝ) :=
  LinearMap.toContinuousLinearMap (Matrix.mulVecLin A)

theorem hasFDerivAt_q (A : Matrix n n ℝ) (x : n → ℝ) :
    ∃ D : (n → ℝ) →L[ℝ] ℝ, HasFDerivAt (q A) D x ∧
      ∀ h, D h = h ⬝ᵥ (A *ᵥ x) + x ⬝ᵥ (A *ᵥ h) := by
  have hc : ∀ i, HasFDerivAt (fun y : n → ℝ => y i) (ContinuousLinearMap.proj i) x :=
    fun i => (ContinuousLinearMap.proj (R := ℝ) (φ := fun _ : n => ℝ) i).hasFDerivAt
  have hm : ∀ i, HasFDerivAt (fun y : n → ℝ => (A *ᵥ y) i)
      ((ContinuousLinearMap.proj i).comp (mulVecCLM A)) x := fun i =>
    ((ContinuousLinearMap.proj i).comp (mulVecCLM A)).hasFDerivAt
  have hs := HasFDerivAt.sum (u := Finset.univ) (fun i _ => (hc i).mul (hm i))
  have hfun : q A = ∑ i, (fun y : n → ℝ => y i) * fun y => (A *ᵥ y) i := by
    funext y; simp [q, dotProduct, Finset.sum_apply]
  rw [hfun]
  refine ⟨_, hs, fun h => ?_⟩
  simp [dotProduct, mulVecCLM, Finset.sum_add_distrib, mul_comm]
  ring

/-- The ambient derivative: `dq_x(h) = h·Ax + x·Ah` (any square `A`). -/
theorem fderiv_q (A : Matrix n n ℝ) (x h : n → ℝ) :
    fderiv ℝ (q A) x h = h ⬝ᵥ (A *ᵥ x) + x ⬝ᵥ (A *ᵥ h) := by
  obtain ⟨D, hD, hDh⟩ := hasFDerivAt_q A x
  rw [hD.fderiv, hDh]

/-- For symmetric `A`: `dq_x(h) = 2 h·Ax`. -/
theorem fderiv_q_symm {A : Matrix n n ℝ} (hA : A.IsSymm) (x h : n → ℝ) :
    fderiv ℝ (q A) x h = 2 * (h ⬝ᵥ (A *ᵥ x)) := by
  have hx : x ⬝ᵥ (A *ᵥ h) = h ⬝ᵥ (A *ᵥ x) := by
    rw [dotProduct_mulVec, ← mulVec_transpose, hA.eq, dotProduct_comm]
  rw [fderiv_q, hx]
  ring

/-- **`thm:morse_matrix`, critical points (algebraic form).** For symmetric `A`:
`dq_x` vanishes on `x^⊥` ⟺ `Ax ∈ span{x}`. -/
theorem critical_iff_eigen {A : Matrix n n ℝ} (hA : A.IsSymm) (x : n → ℝ) :
    (∀ h, h ⬝ᵥ x = 0 → fderiv ℝ (q A) x h = 0) ↔ ∃ c : ℝ, A *ᵥ x = c • x := by
  constructor
  · intro hcrit
    by_cases hx : x ⬝ᵥ x = 0
    · refine ⟨0, ?_⟩
      have : x = 0 := dotProduct_self_eq_zero.mp hx
      simp [this]
    · set c := (x ⬝ᵥ (A *ᵥ x)) / (x ⬝ᵥ x)
      refine ⟨c, ?_⟩
      set h := A *ᵥ x - c • x with hh
      have hhx : h ⬝ᵥ x = 0 := by
        rw [hh, sub_dotProduct, smul_dotProduct, dotProduct_comm (A *ᵥ x), smul_eq_mul]
        simp only [c]
        rw [div_mul_cancel₀ _ hx, sub_self]
      have h0 := hcrit h hhx
      rw [fderiv_q_symm hA] at h0
      have hAx : A *ᵥ x = h + c • x := by rw [hh]; abel
      have hhh : h ⬝ᵥ h = 0 := by
        have : h ⬝ᵥ (A *ᵥ x) = h ⬝ᵥ h := by
          rw [hAx, dotProduct_add, dotProduct_smul, hhx, smul_zero, add_zero]
        linarith
      have := dotProduct_self_eq_zero.mp hhh
      rw [hh, sub_eq_zero] at this
      exact this
  · rintro ⟨c, hc⟩ h hh
    rw [fderiv_q_symm hA, hc, dotProduct_smul, hh, smul_zero, mul_zero]

/-- The Lagrange multiplier on the unit sphere is the critical value: `c = q(x)`. -/
theorem lagrange_value {A : Matrix n n ℝ} {x : n → ℝ} {c : ℝ} (hx : x ⬝ᵥ x = 1)
    (hc : A *ᵥ x = c • x) : c = q A x := by
  rw [q, hc, dotProduct_smul, hx, smul_eq_mul, mul_one]

end General

section Diagonal

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- `e_i`. -/
def e (i : n) : n → ℝ := Pi.single i 1

/-- **(i), eigen-coordinates.** With distinct eigenvalues (`μ` injective), the unit
eigenvectors of `diag μ` are exactly `±e_i`. -/
theorem crit_diag {μ : n → ℝ} (hμ : Function.Injective μ) (x : n → ℝ) :
    (x ⬝ᵥ x = 1 ∧ ∃ c : ℝ, diagonal μ *ᵥ x = c • x) ↔ ∃ i, x = e i ∨ x = -e i := by
  constructor
  · rintro ⟨hx1, c, hc⟩
    have hcoord : ∀ j, (μ j - c) * x j = 0 := fun j => by
      have := congrFun hc j
      rw [mulVec_diagonal] at this
      simp only [Pi.smul_apply, smul_eq_mul] at this
      linarith
    -- there is a nonzero coordinate
    have hex : ∃ i, x i ≠ 0 := by
      by_contra h
      push Not at h
      have : x = 0 := funext h
      rw [this] at hx1; simp at hx1
    obtain ⟨i, hi⟩ := hex
    have hci : μ i = c := by
      have := hcoord i
      rcases mul_eq_zero.mp this with h | h
      · linarith
      · exact absurd h hi
    have hzero : ∀ j, j ≠ i → x j = 0 := fun j hj => by
      rcases mul_eq_zero.mp (hcoord j) with h | h
      · exact absurd (hμ (by linarith : μ j = μ i)) hj
      · exact h
    have hxe : x = x i • e i := by
      funext j
      by_cases hj : j = i
      · subst hj; simp [e]
      · simp [e, hj, hzero j hj]
    have hsq : x i * x i = 1 := by
      rw [hxe] at hx1
      simpa [e, dotProduct, Pi.single_apply] using hx1
    have : x i = 1 ∨ x i = -1 := by
      have : (x i - 1) * (x i + 1) = 0 := by ring_nf; linarith
      rcases mul_eq_zero.mp this with h | h
      · left; linarith
      · right; linarith
    refine ⟨i, ?_⟩
    rcases this with h | h
    · left; rw [hxe, h, one_smul]
    · right; rw [hxe, h, neg_one_smul]
  · rintro ⟨i, h | h⟩ <;> subst h
    · refine ⟨by simp [e, dotProduct, Pi.single_apply], μ i, ?_⟩
      funext j; by_cases hj : j = i
      · subst hj; simp [e, mulVec_diagonal]
      · simp [e, mulVec_diagonal, hj]
    · refine ⟨by simp [e, dotProduct, Pi.single_apply], μ i, ?_⟩
      funext j; by_cases hj : j = i
      · subst hj; simp [e, mulVec_diagonal]
      · simp [e, mulVec_diagonal, hj]

/-- **(i), count.** There are exactly `2n` critical points (`n = card` of the index type). -/
theorem crit_diag_ncard {μ : n → ℝ} (hμ : Function.Injective μ) :
    {x : n → ℝ | x ⬝ᵥ x = 1 ∧ ∃ c : ℝ, diagonal μ *ᵥ x = c • x}.ncard = 2 * Fintype.card n := by
  have hset : {x : n → ℝ | x ⬝ᵥ x = 1 ∧ ∃ c : ℝ, diagonal μ *ᵥ x = c • x} =
      Set.range (fun p : n × Bool => if p.2 then e p.1 else -e p.1) := by
    ext x
    rw [Set.mem_ofPred_eq, crit_diag hμ]
    constructor
    · rintro ⟨i, h | h⟩
      · exact ⟨(i, true), by simp [h]⟩
      · exact ⟨(i, false), by simp [h]⟩
    · rintro ⟨⟨i, b⟩, rfl⟩
      cases b
      · exact ⟨i, Or.inr rfl⟩
      · exact ⟨i, Or.inl rfl⟩
  have hinj : Function.Injective (fun p : n × Bool => if p.2 then e p.1 else -e p.1) := by
    rintro ⟨i, b⟩ ⟨j, b'⟩ h
    have hi := congrFun h i
    simp only at hi
    by_cases hij : i = j
    · subst hij
      cases b <;> cases b' <;> simp [e] at hi ⊢ <;> norm_num at hi
    · exfalso
      cases b <;> cases b' <;> simp [e, hij] at hi
  rw [hset, Set.ncard_range_of_injective hinj, Nat.card_eq_fintype_card, Fintype.card_prod,
    Fintype.card_bool, mul_comm]

/-- The Hessian quadratic form of `f_{diag μ}` at `±e_i`, on `e_i^⊥`. -/
def hessForm (μ : n → ℝ) (i : n) (y : n → ℝ) : ℝ := ∑ j, (μ j - μ i) * y j ^ 2

theorem hessForm_eq_sum_ne (μ : n → ℝ) (i : n) (y : n → ℝ) :
    hessForm μ i y = ∑ j ∈ univ.erase i, (μ j - μ i) * y j ^ 2 := by
  rw [hessForm, ← Finset.add_sum_erase _ _ (mem_univ i), sub_self, zero_mul, zero_add]

/-- Great circle through `s e_i` (`s = ±1`) with initial velocity `y`. -/
noncomputable def gc (s : ℝ) (i : n) (y : n → ℝ) (t : ℝ) : n → ℝ :=
  (s * cos t) • e i + sin t • y

lemma q_gc (μ : n → ℝ) {s : ℝ} (hs : s ^ 2 = 1) (i : n) {y : n → ℝ} (hyi : y i = 0) (t : ℝ) :
    q (diagonal μ) (gc s i y t) = μ i + sin t ^ 2 * (∑ j, μ j * y j ^ 2 - μ i) := by
  have hterm : ∀ j, gc s i y t j * (diagonal μ *ᵥ gc s i y t) j =
      (if j = i then (s * cos t) ^ 2 * μ i else 0) + sin t ^ 2 * (μ j * y j ^ 2) := by
    intro j
    rw [mulVec_diagonal]
    by_cases hj : j = i
    · subst hj; simp [gc, e, hyi]; ring
    · simp [gc, e, hj]; ring
  rw [q, dotProduct, Finset.sum_congr rfl (fun j _ => hterm j), Finset.sum_add_distrib,
    Finset.sum_ite_eq']
  simp only [Finset.mem_univ, ↓reduceIte]
  rw [← Finset.mul_sum]
  have hc : cos t ^ 2 = 1 - sin t ^ 2 := by rw [← sin_sq_add_cos_sq t]; ring
  rw [mul_pow, hs, hc]
  ring

/-- **(ii), Hessian along great circles.** For `y ⊥ e_i`, `|y| = 1`, and `s = ±1`, the function
`φ(t) = q(cos t · s e_i + sin t · y)` has `φ'(0) = 0` and `φ''(0) = 2 H_i(y)`. -/
theorem hessian_great_circle (μ : n → ℝ) {s : ℝ} (hs : s ^ 2 = 1) (i : n) {y : n → ℝ}
    (hyi : y i = 0) (hy1 : y ⬝ᵥ y = 1) :
    deriv (fun t => q (diagonal μ) (gc s i y t)) 0 = 0 ∧
      deriv (deriv (fun t => q (diagonal μ) (gc s i y t))) 0 = 2 * hessForm μ i y := by
  set K := ∑ j, μ j * y j ^ 2 - μ i with hK
  have hfun : (fun t => q (diagonal μ) (gc s i y t)) = fun t => μ i + sin t ^ 2 * K := by
    funext t; rw [q_gc μ hs i hyi t]
  have hd : ∀ t, HasDerivAt (fun t => μ i + sin t ^ 2 * K) (2 * sin t * cos t * K) t := by
    intro t
    have h1 := ((hasDerivAt_sin t).pow 2).mul_const K
    have h2 := h1.const_add (μ i)
    convert h2 using 1
    push_cast; ring
  have hderiv : deriv (fun t => μ i + sin t ^ 2 * K) = fun t => 2 * sin t * cos t * K :=
    funext fun t => (hd t).deriv
  have hd2 : HasDerivAt (fun t => 2 * sin t * cos t * K)
      (2 * (cos 0 * cos 0 - sin 0 * sin 0) * K) 0 := by
    have := (((hasDerivAt_sin 0).const_mul 2).mul (hasDerivAt_cos 0)).mul_const K
    convert this using 1
    ring
  have hH : hessForm μ i y = K := by
    have hsum : ∑ j, y j ^ 2 = 1 := by
      rw [← hy1, dotProduct]; exact Finset.sum_congr rfl fun j _ => by ring
    rw [hessForm, hK]
    simp only [sub_mul, Finset.sum_sub_distrib, ← Finset.mul_sum, hsum, mul_one]
  rw [hfun, hderiv]
  refine ⟨by simp, ?_⟩
  rw [hd2.deriv, hH]
  simp

/-- **Morse (non-degeneracy).** For distinct eigenvalues, `H_i` is non-degenerate on `e_i^⊥`:
if `y ⊥ e_i` and `∑_j (μ_j − μ_i) y_j z_j = 0` for every `z ⊥ e_i`, then `y = 0`. -/
theorem hessForm_nondegenerate {μ : n → ℝ} (hμ : Function.Injective μ) (i : n) {y : n → ℝ}
    (hyi : y i = 0) (h : ∀ z : n → ℝ, z i = 0 → ∑ j, (μ j - μ i) * y j * z j = 0) : y = 0 := by
  funext j
  by_cases hj : j = i
  · subst hj; exact hyi
  · have := h (e j) (by simp [e, Ne.symm hj])
    simp only [e, Pi.single_apply, mul_ite, mul_one, mul_zero, Finset.sum_ite_eq',
      mem_univ, ite_true] at this
    rcases mul_eq_zero.mp this with h' | h'
    · exact absurd (hμ (by linarith)) hj
    · exact h'

/-- The "lower" coordinate set `{j | μ_j < μ_i}`. -/
noncomputable def lowerSet (μ : n → ℝ) (i : n) : Finset n := univ.filter fun j => μ j < μ i

/-- **(ii), index ≥ #lower.** `N₀ = span{e_j | μ_j < μ_i}` lies in `e_i^⊥`, has dimension
`#{j | μ_j < μ_i}`, and `H_i` is negative definite on it. -/
theorem index_lower (μ : n → ℝ) (i : n) :
    let N₀ := Submodule.span ℝ (Set.range fun j : lowerSet μ i => e (j : n))
    (∀ y ∈ N₀, y i = 0) ∧ Module.finrank ℝ N₀ = (lowerSet μ i).card ∧
      ∀ y ∈ N₀, y ≠ 0 → hessForm μ i y < 0 := by
  intro N₀
  -- N₀ is inside the coordinate subspace {y | ∀ j, μ i ≤ μ j → y j = 0}
  let W : Submodule ℝ (n → ℝ) :=
    { carrier := {y | ∀ j, μ i ≤ μ j → y j = 0}
      add_mem' := fun ha hb j hj => by simp [ha j hj, hb j hj]
      zero_mem' := fun j _ => rfl
      smul_mem' := fun c y hy j hj => by simp [hy j hj] }
  have hle : N₀ ≤ W := by
    rw [Submodule.span_le]
    rintro _ ⟨⟨j, hj⟩, rfl⟩ k hk
    have hjk : (j : n) ≠ k := by
      rintro rfl
      simp [lowerSet] at hj
      linarith
    simp [e, Ne.symm hjk]
  refine ⟨fun y hy => hle hy i le_rfl, ?_, ?_⟩
  · have hli : LinearIndependent ℝ (fun j : lowerSet μ i => e (j : n)) := by
      have := (Pi.basisFun ℝ n).linearIndependent.comp (fun j : lowerSet μ i => (j : n))
        Subtype.val_injective
      convert this using 1
      funext j
      simp [e, Pi.basisFun_apply]
    rw [finrank_span_eq_card hli, Fintype.card_coe]
  · intro y hy hy0
    have hW := hle hy
    have hex : ∃ j, y j ≠ 0 := by
      by_contra h; push Not at h; exact hy0 (funext h)
    obtain ⟨j₀, hj₀⟩ := hex
    have hj₀lt : μ j₀ < μ i := by
      by_contra h; push Not at h; exact hj₀ (hW j₀ h)
    apply Finset.sum_neg'
    · intro j _
      by_cases hj : μ i ≤ μ j
      · simp [hW j hj]
      · exact mul_nonpos_of_nonpos_of_nonneg (by linarith [not_le.mp hj]) (sq_nonneg _)
    · exact ⟨j₀, mem_univ _, mul_neg_of_neg_of_pos (by linarith) (by positivity)⟩

omit [DecidableEq n] in
/-- **(ii), index ≤ #lower.** Any subspace on which `H_i` is negative definite has dimension at
most `#{j | μ_j < μ_i}`. -/
theorem index_upper (μ : n → ℝ) (i : n) (N : Submodule ℝ (n → ℝ))
    (hneg : ∀ y ∈ N, y ≠ 0 → hessForm μ i y < 0) :
    Module.finrank ℝ N ≤ (lowerSet μ i).card := by
  let π : N →ₗ[ℝ] (lowerSet μ i → ℝ) :=
    { toFun := fun y j => (y : n → ℝ) j
      map_add' := fun _ _ => rfl
      map_smul' := fun _ _ => rfl }
  have hinj : Function.Injective π := by
    rw [← LinearMap.ker_eq_bot, LinearMap.ker_eq_bot']
    intro y hy
    by_contra hy0
    have hy0' : (y : n → ℝ) ≠ 0 := fun h => hy0 (Subtype.ext h)
    have hneg' := hneg y y.2 hy0'
    have hnn : 0 ≤ hessForm μ i y := by
      apply Finset.sum_nonneg
      intro j _
      by_cases hj : μ j < μ i
      · have : (y : n → ℝ) j = 0 := congrFun hy ⟨j, by simp [lowerSet, hj]⟩
        simp [this]
      · exact mul_nonneg (by linarith [not_lt.mp hj]) (sq_nonneg _)
    linarith
  have := LinearMap.finrank_le_finrank_of_injective hinj
  rwa [Module.finrank_fintype_fun_eq_card, Fintype.card_coe] at this

end Diagonal

/-- Sorted distinct eigenvalues (`Fin k`, 0-based): `#{j | λ_j < λ_i} = i`, the paper's `i − 1`
in 1-based indexing. -/
theorem card_lt_of_strictMono {k : ℕ} {μ : Fin k → ℝ} (hμ : StrictMono μ) (i : Fin k) :
    (lowerSet μ i).card = i := by
  have : lowerSet μ i = Finset.Iio i := by
    ext j; simp [lowerSet, hμ.lt_iff_lt]
  rw [this, Fin.card_Iio]

/-- **(ii) assembled** for `λ_1 < … < λ_k` in eigen-coordinates: at `±e_i` the maximal dimension
of a negative-definite subspace of the Hessian form is `i` (0-based) `= i − 1` (1-based). -/
theorem morse_index_sorted {k : ℕ} {μ : Fin k → ℝ} (hμ : StrictMono μ) (i : Fin k) :
    (∃ N : Submodule ℝ (Fin k → ℝ), (∀ y ∈ N, y i = 0) ∧ Module.finrank ℝ N = i ∧
        ∀ y ∈ N, y ≠ 0 → hessForm μ i y < 0) ∧
      ∀ N : Submodule ℝ (Fin k → ℝ), (∀ y ∈ N, y ≠ 0 → hessForm μ i y < 0) →
        Module.finrank ℝ N ≤ i := by
  refine ⟨?_, fun N hN => card_lt_of_strictMono hμ i ▸ index_upper μ i N hN⟩
  obtain ⟨h1, h2, h3⟩ := index_lower μ i
  exact ⟨_, h1, h2.trans (card_lt_of_strictMono hμ i), h3⟩

/-! ### Non-vacuity witnesses -/

/-- A non-diagonal symmetric matrix: `A = [[0,1],[1,0]]`, `x = (1,1)` is critical
(eigenvalue `1`), and `x = (1,0)` is not (direction `h = (0,1)` gives `dq = 2`). -/
theorem witness_offdiag :
    (∀ h : Fin 2 → ℝ, h ⬝ᵥ ![1, 1] = 0 → fderiv ℝ (q !![0, 1; 1, 0]) ![1, 1] h = 0) ∧
      fderiv ℝ (q !![0, 1; 1, 0]) ![1, 0] ![0, 1] = 2 := by
  have hA : (!![0, 1; 1, 0] : Matrix (Fin 2) (Fin 2) ℝ).IsSymm := by
    ext i j; fin_cases i <;> fin_cases j <;> rfl
  refine ⟨(critical_iff_eigen hA _).mpr ⟨1, ?_⟩, ?_⟩
  · ext i; fin_cases i <;> simp [mulVec, dotProduct]
  · rw [fderiv_q_symm hA]; simp [mulVec, dotProduct]

/-- `μ = (1, 2)`, `i = 1`: the index is `1`, the Hessian along `y = e_0` is `2(1 − 2) = −2`. -/
theorem witness_index :
    (lowerSet ![(1 : ℝ), 2] 1).card = 1 ∧
      deriv (deriv (fun t => q (diagonal ![(1 : ℝ), 2]) (gc 1 1 (e 0) t))) 0 = -2 := by
  refine ⟨?_, ?_⟩
  · have : StrictMono ![(1 : ℝ), 2] := by
      intro a b hab; fin_cases a <;> fin_cases b <;> simp_all
    rw [card_lt_of_strictMono this]; rfl
  · rw [(hessian_great_circle ![(1 : ℝ), 2] (by norm_num) 1 (by simp [e]) (by simp [e, dotProduct])).2]
    simp [hessForm, e]
    norm_num

/-! ### Mutants proved FALSE -/

/-- Mutant 1 (drop symmetry of `A`): "eigenvector ⟹ critical" fails. `A = [[0,1],[0,0]]`,
`x = e_0` has `Ax = 0 = 0·x`, but `dq_x(e_1) = 1 ≠ 0` with `e_1 ⊥ e_0`. -/
theorem mutant_no_symm_false :
    ¬ ∀ (A : Matrix (Fin 2) (Fin 2) ℝ) (x : Fin 2 → ℝ), (∃ c : ℝ, A *ᵥ x = c • x) →
        ∀ h, h ⬝ᵥ x = 0 → fderiv ℝ (q A) x h = 0 := by
  intro H
  have := H !![0, 1; 0, 0] ![1, 0] ⟨0, by ext i; fin_cases i <;> simp [mulVec, dotProduct]⟩
    ![0, 1] (by simp [dotProduct])
  rw [fderiv_q] at this
  simp [mulVec, dotProduct] at this

/-- Mutant 2 (drop distinct eigenvalues): "unit eigenvectors are `±e_i`" fails for `μ = 0`:
`x = (3/5, 4/5)` is a unit eigenvector. -/
theorem mutant_no_distinct_false :
    ¬ ∀ (μ : Fin 2 → ℝ) (x : Fin 2 → ℝ), (x ⬝ᵥ x = 1 ∧ ∃ c : ℝ, diagonal μ *ᵥ x = c • x) →
        ∃ i, x = e i ∨ x = -e i := by
  intro H
  obtain ⟨i, h | h⟩ := H 0 ![3 / 5, 4 / 5]
    ⟨by simp [dotProduct]; norm_num, 0, by ext j; fin_cases j <;> simp⟩ <;>
  · have h0 := congrFun h 0
    have h1 := congrFun h 1
    fin_cases i <;> simp [e] at h0 h1

/-- Mutant 3 (index counted from above, `#{j | μ_j > μ_i}`, i.e. `n − i` instead of `i − 1`):
false for `μ = (1, 2)`, `i = 1`, where a 1-dimensional negative-definite subspace exists. -/
theorem mutant_index_from_above_false :
    ¬ ∀ (μ : Fin 2 → ℝ) (i : Fin 2) (N : Submodule ℝ (Fin 2 → ℝ)),
        (∀ y ∈ N, y ≠ 0 → hessForm μ i y < 0) →
        Module.finrank ℝ N ≤ (univ.filter fun j => μ i < μ j).card := by
  intro H
  obtain ⟨-, h2, h3⟩ := index_lower ![(1 : ℝ), 2] 1
  have := H ![(1 : ℝ), 2] 1 _ h3
  rw [h2] at this
  have hl : (lowerSet ![(1 : ℝ), 2] 1).card = 1 := witness_index.1
  rw [hl] at this
  have hu : (univ.filter fun j : Fin 2 => (![(1 : ℝ), 2] 1) < ![(1 : ℝ), 2] j).card = 0 := by
    rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
    intro j _
    fin_cases j <;> norm_num
  omega

/-- Mutant 4 (Hessian without the factor `2`): false at the witness (value `−2`, not `−1`). -/
theorem mutant_hessian_no_two_false :
    ¬ ∀ (μ : Fin 2 → ℝ) (i : Fin 2) (y : Fin 2 → ℝ), y i = 0 → y ⬝ᵥ y = 1 →
        deriv (deriv (fun t => q (diagonal μ) (gc 1 i y t))) 0 = hessForm μ i y := by
  intro H
  have := H ![(1 : ℝ), 2] 1 (e 0) (by simp [e]) (by simp [e, dotProduct])
  rw [witness_index.2] at this
  simp [hessForm, e] at this
  norm_num at this

end LeanReal.BeyondSpectrum1B3

#print axioms LeanReal.BeyondSpectrum1B3.fderiv_q
#print axioms LeanReal.BeyondSpectrum1B3.fderiv_q_symm
#print axioms LeanReal.BeyondSpectrum1B3.critical_iff_eigen
#print axioms LeanReal.BeyondSpectrum1B3.lagrange_value
#print axioms LeanReal.BeyondSpectrum1B3.crit_diag
#print axioms LeanReal.BeyondSpectrum1B3.crit_diag_ncard
#print axioms LeanReal.BeyondSpectrum1B3.hessForm_eq_sum_ne
#print axioms LeanReal.BeyondSpectrum1B3.hessian_great_circle
#print axioms LeanReal.BeyondSpectrum1B3.hessForm_nondegenerate
#print axioms LeanReal.BeyondSpectrum1B3.index_lower
#print axioms LeanReal.BeyondSpectrum1B3.index_upper
#print axioms LeanReal.BeyondSpectrum1B3.card_lt_of_strictMono
#print axioms LeanReal.BeyondSpectrum1B3.morse_index_sorted
#print axioms LeanReal.BeyondSpectrum1B3.witness_offdiag
#print axioms LeanReal.BeyondSpectrum1B3.witness_index
#print axioms LeanReal.BeyondSpectrum1B3.mutant_no_symm_false
#print axioms LeanReal.BeyondSpectrum1B3.mutant_no_distinct_false
#print axioms LeanReal.BeyondSpectrum1B3.mutant_index_from_above_false
#print axioms LeanReal.BeyondSpectrum1B3.mutant_hessian_no_two_false
