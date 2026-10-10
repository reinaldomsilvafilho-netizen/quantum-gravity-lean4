import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.InnerProductSpace.LinearMap
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Matrix.Basis

/-!
# Book (Zenodo concept DOI 10.5281/zenodo.22290043), chapter 2, projected gradient flows

Source: `unified_quantum_gravity_book/chap02_geometric_flows_tensor_varieties.tex`.

**Part A (batch A3).** `thm:tt_tangent_proj`(iii) and `thm:rank_preservation`(ii):
> for the projected flow `dT/dt = −P_{T(t)}(∇L(T(t)))`, with `P` the orthogonal projection onto
> the tangent space (`P² = P = P*`), `d/dt L(T(t)) = −‖P ∇L‖²_F ≤ 0`.
Formal version (declared reduction): ABSTRACT. `E` is any real inner product space, the
projection is a family `P t` of linear maps with `P t ∘ P t = P t` and `⟪P t x, y⟫ = ⟪x, P t y⟫`,
and `L` has gradient `g` (`HasFDerivAt L ⟪g x, ·⟫ x`). The manifold, the fact that `P t` is the
projection onto `T_{T(t)}M`, the invariance of the manifold (rank preservation, item (i)), and
the book's `C²`/Lipschitz hypotheses (not used by item (ii)) are not formalized.
* `flow_chain_rule`: `(L ∘ T)' = −⟪g, P g⟫` for any linear `P` (no projector hypothesis);
* `proj_flow_deriv`: `(L ∘ T)' = −‖P g‖²` for an orthogonal projector;
* `proj_flow_antitone`: `L ∘ T` is non-increasing on any interval where the flow holds.

The book's example in the proof of `thm:rank_preservation`: `L(A) = ⟨E₁₁, A⟩_F`,
`A₀ = E₁₁`, `r = 1`, flow `A(t) = (1 − t)E₁₁`, `T* = 1`. Formalized for `m × n` real matrices
(`E₁₁ = single i j 1`), with `P` the formula `eq:tangent_proj_formula` at the thin SVD
`U = e_i`, `V = e_j`:
* `example_svd`, `example_proj_fixed`, `example_flow`, `example_loss`, `example_rank_pos`,
  `example_rank_one`: `A(t) = U(1 − t)Vᵀ`; `P(E₁₁) = E₁₁`; `A` solves the projected flow
  entrywise; `L(A(t))` has derivative `−‖P E₁₁‖²_F = −1`; `rank A(t) = 1` for `t ≠ 1` and
  `rank A(1) = 0`.

**Part B (batch B1, item 1).** `prop:tangent_proj_mr`, the matrix algebra only:
for `UᵀU = I_r`, `VᵀV = I_r`, `P(Z) = UUᵀZ + ZVVᵀ − UUᵀZVVᵀ`:
* `tangentProj_eq_sub`: `P(Z) = Z − (I − UUᵀ)Z(I − VVᵀ)`;
* `tangentProj_idem`: `P ∘ P = P`;
* `tangentProj_selfAdjoint`: `tr(P(Z)ᵀW) = tr(ZᵀP(W))` (needs no hypothesis on `U, V`);
* `tangentProj_fix`: `P` fixes `UMVᵀ + U_pVᵀ + UV_pᵀ` when `U_pᵀU = 0`, `V_pᵀV = 0`;
* `tangentProj_range`: `P(Z)` has that form, with `M = UᵀZV`, `U_p = (I − UUᵀ)ZV`,
  `V_p = (I − VVᵀ)ZᵀU`, and these satisfy the constraints;
* `param_recover`: `M`, `U_p`, `V_p` are recovered from `X` (injectivity of the
  parametrization, as in the book's sketch).
NOT covered: the manifold structure of `M_r`, the identification of the set with `T_A M_r`,
and the dimension `r(m + n − r)`.
-/

namespace LeanReal.Chap02Tangent

open Set Matrix

/-! ## Part A: abstract projected gradient flow -/

section Abstract

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- Chain rule along a flow `T' = −P g(T)`: `(L ∘ T)'(t) = −⟪g, P g⟫` at `g = g(T t)`.
No hypothesis on `P` (used for the mutant). -/
theorem flow_chain_rule (P : E →ₗ[ℝ] E) (L : E → ℝ) (g : E → E) (T : ℝ → E) (t : ℝ)
    (hL : HasFDerivAt L (innerSL ℝ (g (T t))) (T t))
    (hT : HasDerivAt T (-(P (g (T t)))) t) :
    HasDerivAt (fun s => L (T s)) (-inner ℝ (g (T t)) (P (g (T t)))) t := by
  have h := hL.comp_hasDerivAt t hT
  refine h.congr_deriv ?_
  simp [innerSL_apply_apply, inner_neg_right]

/-- `thm:tt_tangent_proj`(iii) and `thm:rank_preservation`(ii): along the projected gradient
flow `T' = −P_t ∇L(T)`, with `P_t` an orthogonal projector (`P_t² = P_t = P_t*`),
`d/dt L(T(t)) = −‖P_t ∇L(T(t))‖²`. -/
theorem proj_flow_deriv (P : ℝ → E →ₗ[ℝ] E) (hidem : ∀ t x, P t (P t x) = P t x)
    (hsymm : ∀ t x y, inner ℝ (P t x) y = inner ℝ x (P t y))
    (L : E → ℝ) (g : E → E) (T : ℝ → E) (t : ℝ)
    (hL : HasFDerivAt L (innerSL ℝ (g (T t))) (T t))
    (hT : HasDerivAt T (-(P t (g (T t)))) t) :
    HasDerivAt (fun s => L (T s)) (-‖P t (g (T t))‖ ^ 2) t := by
  refine (flow_chain_rule (P t) L g T t hL hT).congr_deriv ?_
  rw [← hidem t (g (T t)), ← hsymm, hidem, real_inner_self_eq_norm_sq]

/-- Monotone form: on any interval `D` (for instance `[0, T_max)`) where the projected flow
holds, `L ∘ T` is non-increasing. -/
theorem proj_flow_antitone (P : ℝ → E →ₗ[ℝ] E) (hidem : ∀ t x, P t (P t x) = P t x)
    (hsymm : ∀ t x y, inner ℝ (P t x) y = inner ℝ x (P t y))
    (L : E → ℝ) (g : E → E) (hL : ∀ x, HasFDerivAt L (innerSL ℝ (g x)) x)
    (T : ℝ → E) (D : Set ℝ) (hD : Convex ℝ D)
    (hT : ∀ t ∈ D, HasDerivAt T (-(P t (g (T t)))) t) :
    AntitoneOn (fun s => L (T s)) D := by
  have hd : ∀ t ∈ D, HasDerivAt (fun s => L (T s)) (-‖P t (g (T t))‖ ^ 2) t :=
    fun t ht => proj_flow_deriv P hidem hsymm L g T t (hL _) (hT t ht)
  refine antitoneOn_of_deriv_nonpos hD ?_ ?_ ?_
  · exact fun x hx => (hd x hx).continuousAt.continuousWithinAt
  · exact fun x hx => (hd x (interior_subset hx)).differentiableAt.differentiableWithinAt
  · intro x hx
    rw [(hd x (interior_subset hx)).deriv]
    exact neg_nonpos.mpr (sq_nonneg _)

end Abstract

/-! ### Witness for Part A: `E = ℂ` as a real inner product space (`≅ ℝ²`), `P` the orthogonal
projection onto the real axis, `L(z) = ⟪1 + i, z⟫ = re z + im z`, `T(t) = −t + 5i`.
Then `T' = −1 = −P(∇L)` and `(L ∘ T)' = −1 = −‖P ∇L‖²`, while `‖∇L‖² = 2`: the projector bites. -/

/-- Orthogonal projection of `ℂ ≅ ℝ²` onto the real axis. -/
noncomputable def Pre : ℂ →ₗ[ℝ] ℂ where
  toFun z := (z.re : ℂ)
  map_add' x y := by simp
  map_smul' r x := by apply Complex.ext <;> simp

lemma Pre_idem : ∀ (_ : ℝ) (x : ℂ), Pre (Pre x) = Pre x := by
  intro _ x; simp [Pre]

lemma Pre_symm : ∀ (_ : ℝ) (x y : ℂ), inner ℝ (Pre x) y = inner ℝ x (Pre y) := by
  intro _ x y; simp [Pre, Complex.inner]

/-- Gradient of `L`, the constant `1 + i`. -/
def g0 : ℂ := ⟨1, 1⟩

/-- The witness trajectory `T(t) = −t + 5i`. -/
def Tw (t : ℝ) : ℂ := ⟨-t, 5⟩

lemma L_hasFDeriv (x : ℂ) :
    HasFDerivAt (fun z => inner ℝ g0 z) (innerSL ℝ ((fun _ => g0) x)) x := by
  simpa [innerSL_apply_apply] using (innerSL ℝ g0).hasFDerivAt

lemma Tw_deriv (t : ℝ) : HasDerivAt Tw (-(Pre ((fun _ => g0) (Tw t)))) t := by
  have hT : Tw = fun s : ℝ => Complex.ofRealCLM (-s) + (5 : ℂ) * Complex.I := by
    funext s; apply Complex.ext <;> simp [Tw]
  rw [hT]
  have h1 := (Complex.ofRealCLM.hasFDerivAt (x := -t)).comp_hasDerivAt t (hasDerivAt_neg t)
  exact (h1.add_const ((5 : ℂ) * Complex.I)).congr_deriv
    (by apply Complex.ext <;> simp [Pre, g0])

example (t : ℝ) :
    HasDerivAt (fun s => inner ℝ g0 (Tw s)) (-‖Pre ((fun _ => g0) (Tw t))‖ ^ 2) t :=
  proj_flow_deriv (fun _ => Pre) Pre_idem Pre_symm (fun z => inner ℝ g0 z) (fun _ => g0) Tw t
    (L_hasFDeriv _) (Tw_deriv t)

example : ‖Pre g0‖ ^ 2 = 1 ∧ ‖g0‖ ^ 2 = 2 := by
  constructor
  · simp [Pre, g0]
  · rw [Complex.sq_norm]; simp [g0, Complex.normSq_apply]; norm_num

example : AntitoneOn (fun s => inner ℝ g0 (Tw s)) univ :=
  proj_flow_antitone (fun _ => Pre) Pre_idem Pre_symm (fun z => inner ℝ g0 z) (fun _ => g0)
    L_hasFDeriv Tw univ convex_univ (fun t _ => Tw_deriv t)

/-- Mutant (drop self-adjointness): the oblique idempotent `Q(a + bi) = a − 2b` makes
`(L ∘ T)' = −⟪g, Qg⟫ = +1 > 0` for `g = 1 + i`: the loss increases. -/
noncomputable def Qob : ℂ →ₗ[ℝ] ℂ where
  toFun z := ((z.re - 2 * z.im : ℝ) : ℂ)
  map_add' x y := by apply Complex.ext <;> simp; ring
  map_smul' r x := by apply Complex.ext <;> simp; ring

theorem symm_mutant_false :
    ¬ (∀ Q : ℂ →ₗ[ℝ] ℂ, (∀ x, Q (Q x) = Q x) → ∀ g : ℂ, 0 ≤ inner ℝ g (Q g)) := by
  intro h
  have := h Qob (fun x => by apply Complex.ext <;> simp [Qob]) g0
  simp [Qob, g0, Complex.inner] at this

/-! ### The example of `thm:rank_preservation`: `A(t) = (1 − t)E₁₁`. -/

section Example

variable {m n : Type*} [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]

/-- The tangent-space projection `eq:tangent_proj_formula`,
`P(Z) = UUᵀZ + ZVVᵀ − UUᵀZVVᵀ`. -/
def tangentProj {r : Type*} [Fintype r] (U : Matrix m r ℝ) (V : Matrix n r ℝ)
    (Z : Matrix m n ℝ) : Matrix m n ℝ :=
  U * Uᵀ * Z + Z * V * Vᵀ - U * Uᵀ * Z * V * Vᵀ

/-- Frobenius inner product `⟨X, Y⟩_F = tr(XᵀY)`. -/
def frob (X Y : Matrix m n ℝ) : ℝ := trace (Xᵀ * Y)

/-- The flow of the example: `A(t) = (1 − t)E₁₁`. -/
def Aex (i : m) (j : n) (t : ℝ) : Matrix m n ℝ := (1 - t) • single i j 1

/-- Thin SVD of `A(t)`: `A(t) = U Σ Vᵀ` with `U = e_i`, `V = e_j`, `Σ = (1 − t)`,
`UᵀU = VᵀV = I₁`. -/
theorem example_svd (i : m) (j : n) (t : ℝ) :
    Aex i j t = single i (0 : Fin 1) (1 : ℝ) * ((1 - t) • (1 : Matrix (Fin 1) (Fin 1) ℝ))
        * (single j (0 : Fin 1) (1 : ℝ))ᵀ
    ∧ (single i (0 : Fin 1) (1 : ℝ))ᵀ * single i (0 : Fin 1) (1 : ℝ) = 1
    ∧ (single j (0 : Fin 1) (1 : ℝ))ᵀ * single j (0 : Fin 1) (1 : ℝ) = 1 := by
  refine ⟨?_, ?_, ?_⟩
  · rw [Matrix.mul_smul, Matrix.mul_one, Matrix.smul_mul, transpose_single,
      single_mul_single_same, mul_one]
    rfl
  · rw [transpose_single, single_mul_single_same, mul_one]
    ext a b; fin_cases a; fin_cases b; simp
  · rw [transpose_single, single_mul_single_same, mul_one]
    ext a b; fin_cases a; fin_cases b; simp

/-- `P(E₁₁) = E₁₁` at the thin SVD of `A(t)` (any `t < 1`). -/
theorem example_proj_fixed (i : m) (j : n) :
    tangentProj (single i (0 : Fin 1) (1 : ℝ)) (single j (0 : Fin 1) (1 : ℝ)) (single i j 1)
      = single i j 1 := by
  simp only [tangentProj, transpose_single, single_mul_single_same, mul_one]
  abel

/-- `A(t) = (1 − t)E₁₁` solves the projected flow `A' = −P(∇L) = −P(E₁₁)` (entrywise). -/
theorem example_flow (i : m) (j : n) (t : ℝ) (a : m) (b : n) :
    HasDerivAt (fun s => Aex i j s a b)
      (-(tangentProj (single i (0 : Fin 1) (1 : ℝ)) (single j (0 : Fin 1) (1 : ℝ))
          (single i j 1)) a b) t := by
  rw [example_proj_fixed]
  have h := ((hasDerivAt_id t).const_sub 1).mul_const (single i j (1 : ℝ) a b)
  refine (h.congr_deriv (by simp)).congr_of_eventuallyEq ?_
  exact Filter.Eventually.of_forall fun s => by simp [Aex]

/-- The loss `L(A) = ⟨E₁₁, A⟩_F` along the flow has derivative `−‖P(E₁₁)‖²_F = −1`. -/
theorem example_loss (i : m) (j : n) (t : ℝ) :
    HasDerivAt (fun s => frob (single i j 1) (Aex i j s))
      (-frob (tangentProj (single i (0 : Fin 1) (1 : ℝ)) (single j (0 : Fin 1) (1 : ℝ))
          (single i j 1))
        (tangentProj (single i (0 : Fin 1) (1 : ℝ)) (single j (0 : Fin 1) (1 : ℝ))
          (single i j 1))) t := by
  rw [example_proj_fixed]
  have hv : ∀ s, frob (single i j (1 : ℝ)) (Aex i j s) = 1 - s := by
    intro s
    simp [frob, Aex, transpose_single, trace_single_eq_same]
  have hc : frob (single i j (1 : ℝ)) (single i j 1) = 1 := by
    simp [frob, transpose_single, trace_single_eq_same]
  rw [hc]
  have h := (hasDerivAt_id t).const_sub 1
  refine (h.congr_deriv (by simp)).congr_of_eventuallyEq ?_
  exact Filter.Eventually.of_forall fun s => hv s

omit [Fintype m] in
/-- `rank A(t) = 1` for `t ≠ 1`, in particular on `[0, T*) = [0, 1)`. -/
theorem example_rank_one (i : m) (j : n) (t : ℝ) (ht : t ≠ 1) : (Aex i j t).rank = 1 := by
  apply le_antisymm
  · have hfac : Aex i j t = single i (0 : Fin 1) (1 - t) * single (0 : Fin 1) j (1 : ℝ) := by
      rw [single_mul_single_same, mul_one, Aex, smul_single, smul_eq_mul, mul_one]
    rw [hfac]
    exact (rank_mul_le_left _ _).trans ((rank_le_card_width _).trans (by simp))
  · have hsub : ((Aex i j t).submatrix (fun _ : Fin 1 => i) (fun _ : Fin 1 => j)).rank = 1 := by
      have := rank_of_det_ne_zero (A := (Aex i j t).submatrix (fun _ : Fin 1 => i)
        (fun _ : Fin 1 => j)) (by
          rw [det_fin_one]; simp [Aex]; exact sub_ne_zero.mpr (Ne.symm ht))
      simpa using this
    rw [← hsub]
    exact rank_submatrix_le _ _ _

omit [Fintype m] in
/-- `rank A(1) = 0`: at `T* = 1` the flow reaches the lower stratum. -/
theorem example_rank_zero (i : m) (j : n) : (Aex i j 1).rank = 0 := by
  simp [Aex, rank_zero]

end Example

/-! ## Part B: `prop:tangent_proj_mr`, the projector algebra -/

section Projector

variable {m n r : Type*} [Fintype m] [Fintype n] [Fintype r]
  [DecidableEq m] [DecidableEq n] [DecidableEq r]

omit [DecidableEq m] in
/-- `UᵀU = I` cancels on the left: `Uᵀ(UX) = X`. -/
lemma orth_cancel (U : Matrix m r ℝ) (hU : Uᵀ * U = 1) {k : Type*} [Fintype k]
    (X : Matrix r k ℝ) : Uᵀ * (U * X) = X := by
  rw [← Matrix.mul_assoc, hU, Matrix.one_mul]

omit [DecidableEq r] in
/-- `AB = 0` gives `A(BX) = 0`. -/
lemma zero_cancel {p q : Type*} [Fintype q] (A : Matrix p q ℝ) (B : Matrix q r ℝ)
    (h : A * B = 0) {k : Type*} [Fintype k] (X : Matrix r k ℝ) : A * (B * X) = 0 := by
  rw [← Matrix.mul_assoc, h, Matrix.zero_mul]

omit [Fintype r] [DecidableEq r] in
/-- Transposing `U_pᵀU = 0`. -/
lemma transpose_zero_of {p : Type*} [Fintype p] (A : Matrix p r ℝ) (B : Matrix p r ℝ)
    (h : Aᵀ * B = 0) : Bᵀ * A = 0 := by
  rw [← transpose_transpose (Bᵀ * A), transpose_mul, transpose_transpose, h, transpose_zero]

omit [DecidableEq r] in
/-- `P(Z) = Z − (I − UUᵀ)Z(I − VVᵀ)` (form used in the book's proof). -/
theorem tangentProj_eq_sub (U : Matrix m r ℝ) (V : Matrix n r ℝ) (Z : Matrix m n ℝ) :
    tangentProj U V Z = Z - (1 - U * Uᵀ) * Z * (1 - V * Vᵀ) := by
  simp only [tangentProj, Matrix.sub_mul, Matrix.mul_sub, Matrix.one_mul, Matrix.mul_one,
    Matrix.mul_assoc]
  abel

omit [DecidableEq m] [DecidableEq n] in
/-- `prop:tangent_proj_mr`: `P` is idempotent when `UᵀU = I` and `VᵀV = I`. -/
theorem tangentProj_idem (U : Matrix m r ℝ) (V : Matrix n r ℝ)
    (hU : Uᵀ * U = 1) (hV : Vᵀ * V = 1) (Z : Matrix m n ℝ) :
    tangentProj U V (tangentProj U V Z) = tangentProj U V Z := by
  simp only [tangentProj, Matrix.mul_add, Matrix.add_mul, Matrix.mul_sub, Matrix.sub_mul,
    Matrix.mul_assoc, orth_cancel U hU, orth_cancel V hV]
  abel

omit [DecidableEq m] [DecidableEq n] [DecidableEq r] in
/-- `prop:tangent_proj_mr`: `P` is self-adjoint for the Frobenius inner product,
`tr(P(Z)ᵀW) = tr(ZᵀP(W))`. No hypothesis on `U`, `V` is needed. -/
theorem tangentProj_selfAdjoint (U : Matrix m r ℝ) (V : Matrix n r ℝ) (Z W : Matrix m n ℝ) :
    frob (tangentProj U V Z) W = frob Z (tangentProj U V W) := by
  simp only [frob, tangentProj, transpose_sub, transpose_add, transpose_mul,
    transpose_transpose, Matrix.mul_add, Matrix.add_mul, Matrix.mul_sub, Matrix.sub_mul,
    trace_add, trace_sub, Matrix.mul_assoc]
  have h1 : trace (V * (Vᵀ * (Zᵀ * W))) = trace (Zᵀ * (W * (V * Vᵀ))) := by
    rw [trace_mul_comm, Matrix.mul_assoc, trace_mul_comm, Matrix.mul_assoc]
    simp only [Matrix.mul_assoc]
  have h2 : trace (V * (Vᵀ * (Zᵀ * (U * (Uᵀ * W)))))
      = trace (Zᵀ * (U * (Uᵀ * (W * (V * Vᵀ))))) := by
    rw [trace_mul_comm, Matrix.mul_assoc, trace_mul_comm]
    simp only [Matrix.mul_assoc]
  rw [h1, h2]

omit [DecidableEq m] [DecidableEq n] in
/-- `prop:tangent_proj_mr`: `P` fixes every `X = UMVᵀ + U_pVᵀ + UV_pᵀ` with `U_pᵀU = 0`,
`V_pᵀV = 0` (given `UᵀU = I`, `VᵀV = I`). -/
theorem tangentProj_fix (U : Matrix m r ℝ) (V : Matrix n r ℝ)
    (hU : Uᵀ * U = 1) (hV : Vᵀ * V = 1)
    (M : Matrix r r ℝ) (Up : Matrix m r ℝ) (Vp : Matrix n r ℝ)
    (hUp : Upᵀ * U = 0) (hVp : Vpᵀ * V = 0) :
    tangentProj U V (U * M * Vᵀ + Up * Vᵀ + U * Vpᵀ) = U * M * Vᵀ + Up * Vᵀ + U * Vpᵀ := by
  simp only [tangentProj, Matrix.mul_add, Matrix.add_mul, 
    Matrix.mul_assoc, orth_cancel U hU, orth_cancel V hV, zero_cancel _ _ (transpose_zero_of _ _ hUp),
    zero_cancel _ _ hVp, Matrix.mul_zero, Matrix.zero_mul]
  abel

/-- `prop:tangent_proj_mr`: the range of `P` lies in the set: `P(Z) = UMVᵀ + U_pVᵀ + UV_pᵀ`
with `M = UᵀZV`, `U_p = (I − UUᵀ)ZV`, `V_p = (I − VVᵀ)ZᵀU`, and `U_pᵀU = 0`, `V_pᵀV = 0`. -/
theorem tangentProj_range (U : Matrix m r ℝ) (V : Matrix n r ℝ)
    (hU : Uᵀ * U = 1) (hV : Vᵀ * V = 1) (Z : Matrix m n ℝ) :
    tangentProj U V Z = U * (Uᵀ * Z * V) * Vᵀ + ((1 - U * Uᵀ) * Z * V) * Vᵀ
        + U * ((1 - V * Vᵀ) * Zᵀ * U)ᵀ
    ∧ ((1 - U * Uᵀ) * Z * V)ᵀ * U = 0 ∧ ((1 - V * Vᵀ) * Zᵀ * U)ᵀ * V = 0 := by
  refine ⟨?_, ?_, ?_⟩
  · simp only [tangentProj, transpose_mul, transpose_sub, 
      transpose_transpose, Matrix.mul_sub, Matrix.sub_mul,
      Matrix.one_mul, Matrix.mul_assoc]
    abel
  · simp only [transpose_mul, transpose_sub, transpose_transpose,
      Matrix.sub_mul, Matrix.one_mul, Matrix.mul_assoc, 
      ]
    simp only [← Matrix.mul_assoc, hU, Matrix.mul_one, sub_self]
  · simp only [transpose_mul, transpose_sub, transpose_transpose,
      Matrix.sub_mul, Matrix.one_mul, Matrix.mul_assoc]
    simp only [← Matrix.mul_assoc, hV, Matrix.mul_one, sub_self]

/-- Injectivity of the parametrization in the book's sketch: from
`X = UMVᵀ + U_pVᵀ + UV_pᵀ` one recovers `M = UᵀXV`, `U_p = (I − UUᵀ)XV`,
`V_p = (I − VVᵀ)XᵀU`. -/
theorem param_recover (U : Matrix m r ℝ) (V : Matrix n r ℝ)
    (hU : Uᵀ * U = 1) (hV : Vᵀ * V = 1)
    (M : Matrix r r ℝ) (Up : Matrix m r ℝ) (Vp : Matrix n r ℝ)
    (hUp : Upᵀ * U = 0) (hVp : Vpᵀ * V = 0) :
    let X := U * M * Vᵀ + Up * Vᵀ + U * Vpᵀ
    Uᵀ * X * V = M ∧ (1 - U * Uᵀ) * X * V = Up ∧ (1 - V * Vᵀ) * Xᵀ * U = Vp := by
  intro X
  have hVpV : Vpᵀ * V = 0 := hVp
  have hUpU : Upᵀ * U = 0 := hUp
  refine ⟨?_, ?_, ?_⟩
  · simp only [X, Matrix.mul_add, Matrix.add_mul, Matrix.mul_assoc, orth_cancel U hU, zero_cancel _ _ (transpose_zero_of _ _ hUp), hV,
      Matrix.mul_one, Matrix.zero_mul]
    simp only [hVpV, add_zero]
  · simp only [X, Matrix.mul_add, Matrix.add_mul, Matrix.sub_mul, 
      Matrix.one_mul, Matrix.mul_assoc, orth_cancel U hU, zero_cancel _ _ (transpose_zero_of _ _ hUp), hV, Matrix.mul_one, Matrix.mul_zero,
      sub_zero]
    simp only [hVpV, Matrix.mul_zero]
    abel
  · simp only [X, transpose_add, transpose_mul, transpose_transpose, Matrix.mul_add,
      Matrix.add_mul, Matrix.sub_mul, Matrix.one_mul, Matrix.mul_assoc, orth_cancel V hV,
      zero_cancel _ _ (transpose_zero_of _ _ hVp), hU, Matrix.mul_one, Matrix.mul_zero, sub_zero]
    simp only [hUpU, Matrix.mul_zero]
    abel

end Projector

/-! ### Witness for Part B: `m = n = 3`, `r = 1`, `U = e₀`, `V = e₁` (so `r < min(m, n)`),
`Z` the all-ones matrix: `P(Z)` keeps row `0` and column `1` and kills the rest
(`P(Z) ≠ Z`, `P(Z) ≠ 0`). -/

/-- `U = e₀ ∈ ℝ^{3×1}`. -/
def Uw : Matrix (Fin 3) (Fin 1) ℝ := single 0 0 1
/-- `V = e₁ ∈ ℝ^{3×1}`. -/
def Vw : Matrix (Fin 3) (Fin 1) ℝ := single 1 0 1

lemma Uw_orth : Uwᵀ * Uw = 1 := by
  rw [Uw, transpose_single, single_mul_single_same]; ext a b; fin_cases a; fin_cases b; simp
lemma Vw_orth : Vwᵀ * Vw = 1 := by
  rw [Vw, transpose_single, single_mul_single_same]; ext a b; fin_cases a; fin_cases b; simp

example : tangentProj Uw Vw (Matrix.of fun _ _ => 1) = !![1, 1, 1; 0, 1, 0; 0, 1, 0] := by
  ext a b
  fin_cases a <;> fin_cases b <;>
    simp [tangentProj, Uw, Vw, mul_apply, single, transpose_apply, Finset.filter_eq,
      ]

example (Z : Matrix (Fin 3) (Fin 3) ℝ) :
    tangentProj Uw Vw (tangentProj Uw Vw Z) = tangentProj Uw Vw Z :=
  tangentProj_idem Uw Vw Uw_orth Vw_orth Z

/-! ### Mutants for Part B. -/

/-- For `U = V = (2)` (`1 × 1`), `P(Z) = 4Z + 4Z − 16Z = −8Z`. -/
lemma tangentProj_two (Z : Matrix (Fin 1) (Fin 1) ℝ) :
    tangentProj ((2 : ℝ) • (1 : Matrix (Fin 1) (Fin 1) ℝ)) ((2 : ℝ) • 1) Z = (-8 : ℝ) • Z := by
  simp only [tangentProj, transpose_smul, transpose_one, Matrix.smul_mul, Matrix.mul_smul,
    Matrix.one_mul, Matrix.mul_one, smul_smul]
  ext a b; simp; ring

/-- Mutant (drop `UᵀU = I` and `VᵀV = I`): with `U = V = (2)` (`1 × 1`),
`P(Z) = −8Z`, not idempotent. -/
theorem idem_mutant_false :
    ¬ (∀ (U V : Matrix (Fin 1) (Fin 1) ℝ) (Z : Matrix (Fin 1) (Fin 1) ℝ),
        tangentProj U V (tangentProj U V Z) = tangentProj U V Z) := by
  intro h
  have := h ((2 : ℝ) • 1) ((2 : ℝ) • 1) 1
  rw [tangentProj_two, tangentProj_two] at this
  have := congrFun (congrFun this 0) 0
  simp at this
  norm_num at this

/-- Mutant (fixing the set without orthonormality): with `U = V = (2)`, `M = 1`,
`U_p = V_p = 0`, `P(UMVᵀ) = −8·UMVᵀ ≠ UMVᵀ`. -/
theorem fix_mutant_false :
    ¬ (∀ (U V M : Matrix (Fin 1) (Fin 1) ℝ),
        tangentProj U V (U * M * Vᵀ) = U * M * Vᵀ) := by
  intro h
  have := h ((2 : ℝ) • 1) ((2 : ℝ) • 1) 1
  rw [tangentProj_two] at this
  have := congrFun (congrFun this 0) 0
  simp at this
  norm_num at this

/-- Mutant (self-adjointness for an oblique idempotent): `Q = [[1, 1], [0, 0]]` satisfies
`Q² = Q` but `tr((QZ)ᵀW) ≠ tr(ZᵀQW)` for `Z = E₀₀`, `W = E₁₀`. So the symmetric form
`UUᵀ` in `eq:tangent_proj_formula` matters. -/
theorem selfAdjoint_mutant_false :
    ¬ (∀ Q : Matrix (Fin 2) (Fin 2) ℝ, Q * Q = Q →
        ∀ Z W : Matrix (Fin 2) (Fin 2) ℝ, frob (Q * Z) W = frob Z (Q * W)) := by
  intro h
  have hQ : !![(1 : ℝ), 1; 0, 0] * !![1, 1; 0, 0] = !![1, 1; 0, 0] := by
    ext a b; fin_cases a <;> fin_cases b <;> simp [mul_apply, Fin.sum_univ_two]
  have := h _ hQ !![1, 0; 0, 0] !![0, 0; 1, 0]
  simp [frob, trace, mul_apply, Fin.sum_univ_two, transpose_apply] at this

/-- Mutant (recovery formula without `U_pᵀU = 0`): `U = V = (1)`, `M = 0`, `U_p = (1)`,
`V_p = 0` give `UᵀXV = 1 ≠ M`. -/
theorem recover_mutant_false :
    ¬ (∀ (U V M Up Vp : Matrix (Fin 1) (Fin 1) ℝ), Uᵀ * U = 1 → Vᵀ * V = 1 →
        Vpᵀ * V = 0 → Uᵀ * (U * M * Vᵀ + Up * Vᵀ + U * Vpᵀ) * V = M) := by
  intro h
  have := congrFun (congrFun (h 1 1 0 1 0 (by simp) (by simp) (by simp)) 0) 0
  simp at this

end LeanReal.Chap02Tangent

#print axioms LeanReal.Chap02Tangent.flow_chain_rule
#print axioms LeanReal.Chap02Tangent.proj_flow_deriv
#print axioms LeanReal.Chap02Tangent.proj_flow_antitone
#print axioms LeanReal.Chap02Tangent.symm_mutant_false
#print axioms LeanReal.Chap02Tangent.example_svd
#print axioms LeanReal.Chap02Tangent.example_proj_fixed
#print axioms LeanReal.Chap02Tangent.example_flow
#print axioms LeanReal.Chap02Tangent.example_loss
#print axioms LeanReal.Chap02Tangent.example_rank_one
#print axioms LeanReal.Chap02Tangent.example_rank_zero
#print axioms LeanReal.Chap02Tangent.tangentProj_eq_sub
#print axioms LeanReal.Chap02Tangent.tangentProj_idem
#print axioms LeanReal.Chap02Tangent.tangentProj_selfAdjoint
#print axioms LeanReal.Chap02Tangent.tangentProj_fix
#print axioms LeanReal.Chap02Tangent.tangentProj_range
#print axioms LeanReal.Chap02Tangent.param_recover
#print axioms LeanReal.Chap02Tangent.idem_mutant_false
#print axioms LeanReal.Chap02Tangent.fix_mutant_false
#print axioms LeanReal.Chap02Tangent.selfAdjoint_mutant_false
#print axioms LeanReal.Chap02Tangent.recover_mutant_false
