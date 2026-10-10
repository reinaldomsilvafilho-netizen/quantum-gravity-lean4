import LeanReal.Chap02Toda
import LeanReal.Chap02Tangent

/-!
# L2 of batch LIVRO_A3: two gap fills

Independent layer-2 reviewer. Neither item changes a verdict; both make a step of the book's
proof that the writer's batch leaves out, or a hypothesis it keeps, visible in Lean.

* `piSo_split`, `qr_closed_eq`: the step of the proof of `thm:toda_qr`(iii) leading to
  `eq:toda_closed_Q`. If `QᵀQ = I`, `R` is invertible, `A₀QR = Q'R + QR'` (the derivative of
  `exp(tA₀) = QR` at one time), `QᵀQ'` is skew and `R'R⁻¹` is upper triangular, then
  `Q' = Q Π_so(QᵀA₀Q)`. Pointwise algebra only (no ODE).
* `tangentProj_fix_general`: `P` of `eq:tangent_proj_formula` fixes every `UA + BVᵀ` once
  `UᵀU = I` and `VᵀV = I`. The constraints `U_pᵀU = 0`, `V_pᵀV = 0` that `tangentProj_fix`
  carries are not needed for the fixing step (they matter for the uniqueness of the
  parametrization, `param_recover`).
-/

namespace LeanReal.L2_LIVRO_A3_Extra

open Matrix LeanReal.Chap02Toda LeanReal.Chap02Tangent

variable {n : ℕ}

/-- `Π_so(S + U) = S` for `S` skew and `U` upper triangular. -/
theorem piSo_split (S U : Matrix (Fin n) (Fin n) ℝ) (hS : Sᵀ = -S) (hU : IsUpper U) :
    piSo (S + U) = S := by
  have hlin : piSo (S + U) = piSo S + piSo U := by
    ext a b; simp [piSo, lowerPart]; split_ifs <;> ring
  rw [hlin, piSo_of_skew S hS, piSo_of_upper U hU, add_zero]

/-- The step to `eq:toda_closed_Q`, at one time: from `A₀QR = Q'R + QR'`, `QᵀQ = I`,
`R` invertible, `QᵀQ'` skew and `R'R⁻¹` upper triangular, `Q' = Q Π_so(QᵀA₀Q)`. -/
theorem qr_closed_eq (A₀ Q R Q' R' : Matrix (Fin n) (Fin n) ℝ) (hQ : Qᵀ * Q = 1)
    (hR : IsUnit R.det) (hd : A₀ * Q * R = Q' * R + Q * R')
    (hskew : (Qᵀ * Q')ᵀ = -(Qᵀ * Q')) (hup : IsUpper (R' * R⁻¹)) :
    Q' = Q * piSo (Qᵀ * A₀ * Q) := by
  have hRR : R * R⁻¹ = 1 := Matrix.mul_nonsing_inv R hR
  have hQQ : Q * Qᵀ = 1 := (mul_eq_one_comm).mp hQ
  have key : Qᵀ * A₀ * Q = Qᵀ * Q' + R' * R⁻¹ := by
    have h1 : Qᵀ * (A₀ * Q * R) * R⁻¹ = Qᵀ * (Q' * R + Q * R') * R⁻¹ := by rw [hd]
    simp only [Matrix.mul_add, Matrix.add_mul, Matrix.mul_assoc, hRR, Matrix.mul_one] at h1
    rw [← Matrix.mul_assoc Qᵀ Q (R' * R⁻¹), hQ, Matrix.one_mul] at h1
    rw [Matrix.mul_assoc, h1]
  rw [key, piSo_split _ _ hskew hup, ← Matrix.mul_assoc, hQQ, Matrix.one_mul]

/-- Witness for `qr_closed_eq` that bites: `n = 2`, `A₀ = [[0, 1], [1, 0]]`, `Q = I`, `R = I`
(time `0` of `exp(tA₀) = QR`), `Q' = Π_so(A₀) = [[0, −1], [1, 0]]`, `R' = A₀ − Q' =
[[0, 2], [0, 0]]` (upper). Then `Q' ≠ 0`, and the theorem recovers it. -/
example :
    let A₀ : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; 1, 0]
    let Q' : Matrix (Fin 2) (Fin 2) ℝ := !![0, -1; 1, 0]
    Q' = 1 * piSo (1ᵀ * A₀ * 1) ∧ Q' ≠ 0 := by
  intro A₀ Q'
  let R' : Matrix (Fin 2) (Fin 2) ℝ := !![0, 2; 0, 0]
  refine ⟨qr_closed_eq A₀ 1 1 Q' R' (by simp) (by simp)
    (by simp only [A₀, Q', R', Matrix.mul_one, Matrix.one_mul]
        ext a b; fin_cases a <;> fin_cases b <;> (simp; try norm_num))
    (by ext a b; fin_cases a <;> fin_cases b <;> simp [Q'])
    (by intro a b h; fin_cases a <;> fin_cases b <;> simp_all [R']), ?_⟩
  intro h; have := congrFun (congrFun h 1) 0; simp [Q'] at this

/-- Mutant: without `R'R⁻¹` upper triangular the conclusion fails (`R' = A₀`, `Q' = 0`). -/
theorem qr_closed_mutant_false :
    ¬ (∀ (A₀ Q R Q' R' : Matrix (Fin 2) (Fin 2) ℝ), Qᵀ * Q = 1 → IsUnit R.det →
        A₀ * Q * R = Q' * R + Q * R' → (Qᵀ * Q')ᵀ = -(Qᵀ * Q') →
        Q' = Q * piSo (Qᵀ * A₀ * Q)) := by
  intro h
  have := h !![0, 1; 1, 0] 1 1 0 !![0, 1; 1, 0] (by simp) (by simp) (by simp) (by simp)
  have := congrFun (congrFun this 1) 0
  simp [piSo, lowerPart] at this

/-- `P` fixes `UA + BVᵀ` for any `A`, `B` when `UᵀU = I`, `VᵀV = I`. -/
theorem tangentProj_fix_general {m n' r : Type*} [Fintype m] [Fintype n'] [Fintype r]
    [DecidableEq m] [DecidableEq n'] [DecidableEq r] (U : Matrix m r ℝ) (V : Matrix n' r ℝ)
    (hU : Uᵀ * U = 1) (hV : Vᵀ * V = 1) (A : Matrix r n' ℝ) (B : Matrix m r ℝ) :
    tangentProj U V (U * A + B * Vᵀ) = U * A + B * Vᵀ := by
  rw [tangentProj_eq_sub]
  have h1 : (1 - U * Uᵀ) * U = 0 := by
    rw [Matrix.sub_mul, Matrix.one_mul, Matrix.mul_assoc, hU, Matrix.mul_one, sub_self]
  have h2 : Vᵀ * (1 - V * Vᵀ) = 0 := by
    rw [Matrix.mul_sub, Matrix.mul_one, ← Matrix.mul_assoc, hV, Matrix.one_mul, sub_self]
  have : (1 - U * Uᵀ) * (U * A + B * Vᵀ) * (1 - V * Vᵀ) = 0 := by
    rw [Matrix.mul_add, Matrix.add_mul, ← Matrix.mul_assoc, h1, Matrix.zero_mul,
      Matrix.zero_mul, zero_add, Matrix.mul_assoc, Matrix.mul_assoc, h2, Matrix.mul_zero,
      Matrix.mul_zero]
  rw [this, sub_zero]

end LeanReal.L2_LIVRO_A3_Extra

#print axioms LeanReal.L2_LIVRO_A3_Extra.piSo_split
#print axioms LeanReal.L2_LIVRO_A3_Extra.qr_closed_eq
#print axioms LeanReal.L2_LIVRO_A3_Extra.qr_closed_mutant_false
#print axioms LeanReal.L2_LIVRO_A3_Extra.tangentProj_fix_general
