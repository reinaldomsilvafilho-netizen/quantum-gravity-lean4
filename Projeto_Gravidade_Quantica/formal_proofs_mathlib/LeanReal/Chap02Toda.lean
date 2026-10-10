import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.LinearAlgebra.Matrix.Charpoly.Coeff

/-!
# Book (Zenodo concept DOI 10.5281/zenodo.22290043), chapter 2, `thm:toda_qr` (algebraic core)

Source: `unified_quantum_gravity_book/chap02_geometric_flows_tensor_varieties.tex`,
the decomposition `X = Π_so(X) + Π_b(X)`, `Π_so(X) = X_{<0} − X_{<0}ᵀ`, Definition
"The Continuous Toda Lattice Flow" (`eq:toda_flow`) and Theorem `thm:toda_qr`:
> (i) the Toda flow is isospectral; (ii) the solution of `Q' = QΠ_so(A)`, `Q(0) = I`, lies in
> `O(n)` and `A(t) = Q(t)ᵀA₀Q(t)`; (iii) `exp(tA₀) = Q(t)R(t)` (QR) gives the same `Q`, and
> `e^{A(1)} = R(1)Q(1)`.

Formal version (declared reduction): the ALGEBRAIC and pointwise-differential steps of the
book's proof, with `n × n` real matrices indexed by `Fin n`. Derivatives of matrix curves are
taken ENTRYWISE (`∀ a b, HasDerivAt (fun s => Q s a b) (Q' a b) t`), so no matrix norm is used.
* `piSo_skew`, `piSo_of_skew`, `piSo_of_upper`, `sub_piSo_upper`, `skew_upper_eq_zero`: the
  decomposition `𝔰𝔬(n) ⊕ 𝔟` and the formula for `Π_so`, with uniqueness;
* `isospectral`: `QQᵀ = I → charpoly(QᵀA₀Q) = charpoly A₀` (the "proof of (i)" step);
* `orth_deriv_zero`, `orth_preserved`: if `Q' = QK` with `Kᵀ = −K`, then `(QQᵀ)' = 0`, and
  `Q(0) = I` gives `Q(t)Q(t)ᵀ = I` for all `t` (the "proof of (ii)" step);
* `conj_deriv`: `B = QᵀA₀Q` satisfies `B' = BK − KB` (the "proof of (ii)" step);
* `qr_step`: `QᵀQ = I` and `e^{A₀} = QR` give `e^{QᵀA₀Q} = RQ` (last display of the proof; the
  triangularity of `R` is not needed for this step).
NOT covered: existence, uniqueness and global existence of the ODE solutions (Picard–Lindelöf,
the identification `A = B` by uniqueness for the linear equation `eq:toda_linear`), the
existence, uniqueness and smoothness of the QR factorization, and the time-shift argument.
-/

namespace LeanReal.Chap02Toda

open Matrix

variable {n : ℕ}

/-! ## The decomposition `𝔰𝔬(n) ⊕ 𝔟` -/

/-- Strictly lower-triangular part `X_{<0}`. -/
def lowerPart (X : Matrix (Fin n) (Fin n) ℝ) : Matrix (Fin n) (Fin n) ℝ :=
  Matrix.of fun a b => if b < a then X a b else 0

/-- `Π_so(X) = X_{<0} − X_{<0}ᵀ`. -/
def piSo (X : Matrix (Fin n) (Fin n) ℝ) : Matrix (Fin n) (Fin n) ℝ :=
  lowerPart X - (lowerPart X)ᵀ

/-- Upper triangular: zero strictly below the diagonal. -/
def IsUpper (X : Matrix (Fin n) (Fin n) ℝ) : Prop := ∀ a b, b < a → X a b = 0

/-- `Π_so(X)` is skew-symmetric. -/
theorem piSo_skew (X : Matrix (Fin n) (Fin n) ℝ) : (piSo X)ᵀ = -piSo X := by
  ext a b; simp [piSo]

/-- `Π_so` fixes skew-symmetric matrices. -/
theorem piSo_of_skew (K : Matrix (Fin n) (Fin n) ℝ) (hK : Kᵀ = -K) : piSo K = K := by
  ext a b
  have hab : K b a = -K a b := by
    have := congrFun (congrFun hK a) b; simpa using this
  have haa : K a a = 0 := by
    have := congrFun (congrFun hK a) a; simp at this; linarith
  simp only [piSo, lowerPart, Matrix.sub_apply, transpose_apply, of_apply]
  rcases lt_trichotomy a b with h | h | h
  · simp [h, not_lt.mpr h.le, hab]
  · subst h; simp [haa]
  · simp [h, not_lt.mpr h.le]

/-- `Π_so` annihilates upper-triangular matrices. -/
theorem piSo_of_upper (U : Matrix (Fin n) (Fin n) ℝ) (hU : IsUpper U) : piSo U = 0 := by
  ext a b
  simp only [piSo, lowerPart, Matrix.sub_apply, transpose_apply, of_apply, Matrix.zero_apply]
  split_ifs with h1 h2 h2
  · exact absurd (h1.trans h2) (lt_irrefl _)
  · rw [hU a b h1, sub_zero]
  · rw [hU b a h2, zero_sub, neg_zero]
  · simp

/-- `Π_b(X) = X − Π_so(X)` is upper triangular. -/
theorem sub_piSo_upper (X : Matrix (Fin n) (Fin n) ℝ) : IsUpper (X - piSo X) := by
  intro a b h
  simp [piSo, lowerPart, h, not_lt.mpr h.le]

/-- Uniqueness of the decomposition: `𝔰𝔬(n) ∩ 𝔟 = {0}`. -/
theorem skew_upper_eq_zero (K : Matrix (Fin n) (Fin n) ℝ) (hK : Kᵀ = -K) (hU : IsUpper K) :
    K = 0 := by
  rw [← piSo_of_skew K hK, piSo_of_upper K hU]

/-! ## Isospectrality -/

/-- Proof of (i): for `QQᵀ = I`, `QᵀA₀Q` has the characteristic polynomial of `A₀`. -/
theorem isospectral (Q A : Matrix (Fin n) (Fin n) ℝ) (hQ : Q * Qᵀ = 1) :
    (Qᵀ * A * Q).charpoly = A.charpoly := by
  rw [Matrix.mul_assoc, charpoly_mul_comm, Matrix.mul_assoc, hQ, Matrix.mul_one]

/-! ## Entrywise derivatives of matrix products -/

/-- Product rule for matrix curves, entrywise. -/
lemma hasDerivAt_mul_entry {k l p : Type*} [Fintype l]
    (M : ℝ → Matrix k l ℝ) (N : ℝ → Matrix l p ℝ) (M' : Matrix k l ℝ) (N' : Matrix l p ℝ)
    (t : ℝ) (hM : ∀ a b, HasDerivAt (fun s => M s a b) (M' a b) t)
    (hN : ∀ a b, HasDerivAt (fun s => N s a b) (N' a b) t) (a : k) (b : p) :
    HasDerivAt (fun s => (M s * N s) a b) ((M' * N t + M t * N') a b) t := by
  have h := HasDerivAt.fun_sum (u := Finset.univ) (A := fun c s => M s a c * N s c b)
    (A' := fun c => M' a c * N t c b + M t a c * N' c b) (fun c _ => (hM a c).fun_mul (hN c b))
  convert h using 1
  · funext s; rw [mul_apply]
  · rw [Matrix.add_apply, mul_apply, mul_apply, ← Finset.sum_add_distrib]

/-- Transpose, entrywise. -/
lemma hasDerivAt_transpose_entry {k l : Type*} (M : ℝ → Matrix k l ℝ) (M' : Matrix k l ℝ)
    (t : ℝ) (hM : ∀ a b, HasDerivAt (fun s => M s a b) (M' a b) t) (a : l) (b : k) :
    HasDerivAt (fun s => (M s)ᵀ a b) (M'ᵀ a b) t := hM b a

/-- Proof of (ii): if `Q' = QK` with `Kᵀ = −K`, then `(QQᵀ)' = QK Qᵀ + Q(QK)ᵀ = 0`. -/
theorem orth_deriv_zero (Q : ℝ → Matrix (Fin n) (Fin n) ℝ) (K : Matrix (Fin n) (Fin n) ℝ)
    (hK : Kᵀ = -K) (t : ℝ) (hQ : ∀ a b, HasDerivAt (fun s => Q s a b) ((Q t * K) a b) t)
    (a b : Fin n) : HasDerivAt (fun s => (Q s * (Q s)ᵀ) a b) 0 t := by
  have h := hasDerivAt_mul_entry Q (fun s => (Q s)ᵀ) (Q t * K) (Q t * K)ᵀ t hQ
    (hasDerivAt_transpose_entry Q (Q t * K) t hQ) a b
  have hz : Q t * K * (Q t)ᵀ + Q t * (Q t * K)ᵀ = 0 := by
    rw [transpose_mul, hK, Matrix.neg_mul, Matrix.mul_neg, ← Matrix.mul_assoc, add_neg_cancel]
  rw [hz] at h
  exact h

/-- Proof of (ii), integrated: with `Q(0) = I` and `Q' = QK(t)` (`K(t)` skew) for all `t`,
`Q(t)Q(t)ᵀ = I` for all `t`. -/
theorem orth_preserved (Q : ℝ → Matrix (Fin n) (Fin n) ℝ) (K : ℝ → Matrix (Fin n) (Fin n) ℝ)
    (hK : ∀ t, (K t)ᵀ = -K t)
    (hQ : ∀ t a b, HasDerivAt (fun s => Q s a b) ((Q t * K t) a b) t) (hQ0 : Q 0 = 1)
    (t : ℝ) : Q t * (Q t)ᵀ = 1 := by
  ext a b
  have hd : ∀ s, HasDerivAt (fun s => (Q s * (Q s)ᵀ) a b) 0 s := fun s =>
    orth_deriv_zero Q (K s) (hK s) s (hQ s) a b
  have hc := is_const_of_deriv_eq_zero (fun s => (hd s).differentiableAt)
    (fun s => (hd s).deriv) t 0
  simp only [hQ0, transpose_one, Matrix.mul_one] at hc
  exact hc

/-- Proof of (ii): `B = QᵀA₀Q` satisfies `B' = BK − KB` when `Q' = QK` and `Kᵀ = −K`. -/
theorem conj_deriv (Q : ℝ → Matrix (Fin n) (Fin n) ℝ) (K A₀ : Matrix (Fin n) (Fin n) ℝ)
    (hK : Kᵀ = -K) (t : ℝ) (hQ : ∀ a b, HasDerivAt (fun s => Q s a b) ((Q t * K) a b) t)
    (a b : Fin n) :
    HasDerivAt (fun s => ((Q s)ᵀ * A₀ * Q s) a b)
      (((Q t)ᵀ * A₀ * Q t * K - K * ((Q t)ᵀ * A₀ * Q t)) a b) t := by
  have hQT := hasDerivAt_transpose_entry Q (Q t * K) t hQ
  have hc : ∀ a b, HasDerivAt (fun _ : ℝ => A₀ a b) ((0 : Matrix (Fin n) (Fin n) ℝ) a b) t :=
    fun a b => hasDerivAt_const t _
  have h1 := hasDerivAt_mul_entry (fun s => (Q s)ᵀ) (fun _ => A₀) (Q t * K)ᵀ 0 t hQT hc
  have h2 := hasDerivAt_mul_entry (fun s => (Q s)ᵀ * A₀) Q _ (Q t * K) t h1 hQ a b
  refine h2.congr_deriv ?_
  rw [transpose_mul, hK]
  simp only [Matrix.mul_zero, add_zero, Matrix.neg_mul, Matrix.mul_assoc]
  rw [neg_add_eq_sub]

/-! ## The QR step -/

/-- Last display of the proof of (iii): if `QᵀQ = I` and `e^{A₀} = QR`, then
`e^{QᵀA₀Q} = RQ` (one unshifted QR step on `e^{A₀}`). -/
theorem qr_step (Q R A₀ : Matrix (Fin n) (Fin n) ℝ) (hQ : Qᵀ * Q = 1)
    (hexp : NormedSpace.exp A₀ = Q * R) :
    NormedSpace.exp (Qᵀ * A₀ * Q) = R * Q := by
  have hinv : Q⁻¹ = Qᵀ := Matrix.inv_eq_left_inv hQ
  have hunit : IsUnit Q := by
    rw [Matrix.isUnit_iff_isUnit_det]
    have hd := congrArg Matrix.det hQ
    rw [det_mul, det_transpose, det_one] at hd
    exact isUnit_iff_ne_zero.mpr (left_ne_zero_of_mul_eq_one hd)
  rw [← hinv, Matrix.exp_conj' Q A₀ hunit, hexp, hinv, ← Matrix.mul_assoc, hQ,
    Matrix.one_mul]

/-! ## Witnesses -/

/-- Quarter rotation `[[0, −1], [1, 0]]`, a non-trivial orthogonal matrix. -/
def Qrot : Matrix (Fin 2) (Fin 2) ℝ := !![0, -1; 1, 0]

lemma Qrot_orth : Qrot * Qrotᵀ = 1 := by
  ext a b; fin_cases a <;> fin_cases b <;> simp [Qrot, mul_apply, Fin.sum_univ_two]

/-- Isospectrality witness: `Qᵀ diag(1, 2) Q = diag(2, 1) ≠ diag(1, 2)`, same charpoly. -/
example : (Qrotᵀ * !![1, 0; 0, 2] * Qrot).charpoly = (!![(1 : ℝ), 0; 0, 2]).charpoly :=
  isospectral Qrot _ Qrot_orth

example : Qrotᵀ * !![1, 0; 0, 2] * Qrot ≠ !![(1 : ℝ), 0; 0, 2] := by
  intro h
  have := congrFun (congrFun h 0) 0
  simp [Qrot, mul_apply, Fin.sum_univ_two] at this

/-- Rotation curve `Q(t) = [[cos t, −sin t], [sin t, cos t]]`, solving `Q' = QK` with the
skew `K = [[0, −1], [1, 0]]`. -/
noncomputable def Qt (t : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cos t, -Real.sin t; Real.sin t, Real.cos t]

lemma Krot_skew : Qrotᵀ = -Qrot := by
  ext a b; fin_cases a <;> fin_cases b <;> simp [Qrot]

lemma Qt_deriv (t : ℝ) (a b : Fin 2) :
    HasDerivAt (fun s => Qt s a b) ((Qt t * Qrot) a b) t := by
  fin_cases a <;> fin_cases b <;>
    simp [Qt, Qrot, mul_apply, Fin.sum_univ_two]
  · exact Real.hasDerivAt_cos t
  · exact (Real.hasDerivAt_sin t).neg
  · exact Real.hasDerivAt_sin t
  · exact Real.hasDerivAt_cos t

/-- `orth_preserved` on the rotation curve gives `cos² t + sin² t = 1` entrywise. -/
example (t : ℝ) : Qt t * (Qt t)ᵀ = 1 :=
  orth_preserved Qt (fun _ => Qrot) (fun _ => Krot_skew) (fun s => Qt_deriv s)
    (by ext a b; fin_cases a <;> fin_cases b <;> simp [Qt]) t

/-- QR-step witness: `A₀ = diag(0, 1)`, `Q` the swap (orthogonal), `R = Qᵀe^{A₀}`. Then
`e^{QᵀA₀Q} = RQ = diag(e, 1)`. -/
def Qswap : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; 1, 0]

lemma Qswap_orth : Qswapᵀ * Qswap = 1 := by
  ext a b; fin_cases a <;> fin_cases b <;> simp [Qswap, mul_apply, Fin.sum_univ_two]

example : NormedSpace.exp (Qswapᵀ * diagonal ![0, 1] * Qswap)
    = (Qswapᵀ * NormedSpace.exp (diagonal ![(0 : ℝ), 1])) * Qswap :=
  qr_step Qswap _ _ Qswap_orth (by
    rw [← Matrix.mul_assoc, show Qswap * Qswapᵀ = 1 from (mul_eq_one_comm).mp Qswap_orth,
      Matrix.one_mul])

/-! ## Mutants -/

/-- Mutant (drop `QQᵀ = I` in `isospectral`): `Q = 2I`, `A = I` give traces `8 ≠ 2`, so the
characteristic polynomials differ. -/
theorem isospectral_mutant_false :
    ¬ (∀ Q A : Matrix (Fin 2) (Fin 2) ℝ, (Qᵀ * A * Q).charpoly = A.charpoly) := by
  intro h
  have h1 := congrArg (fun p => -(Polynomial.coeff p (Fintype.card (Fin 2) - 1)))
    (h ((2 : ℝ) • 1) 1)
  rw [← trace_eq_neg_charpoly_coeff, ← trace_eq_neg_charpoly_coeff] at h1
  simp [transpose_smul, trace] at h1
  norm_num at h1

/-- Mutant (drop `Kᵀ = −K` in `orth_deriv_zero`): `Q = I`, `K = I` give
`QKQᵀ + Q(QK)ᵀ = 2I ≠ 0`. -/
theorem orth_mutant_false :
    ¬ (∀ Q K : Matrix (Fin 2) (Fin 2) ℝ, Q * K * Qᵀ + Q * (Q * K)ᵀ = 0) := by
  intro h
  have := congrFun (congrFun (h 1 1) 0) 0
  simp at this

/-- Mutant (wrong sign in `Π_so`): `X_{<0} + X_{<0}ᵀ` is not skew (`X = E₁₀`). -/
theorem piSo_sign_mutant_false :
    ¬ (∀ X : Matrix (Fin 2) (Fin 2) ℝ,
        (lowerPart X + (lowerPart X)ᵀ)ᵀ = -(lowerPart X + (lowerPart X)ᵀ)) := by
  intro h
  have := congrFun (congrFun (h !![0, 0; 1, 0]) 1) 0
  simp [lowerPart] at this
  norm_num at this

/-- Mutant (drop `QᵀQ = I` in `qr_step`): `Q = 2I`, `A₀ = 0`, `R = ½I` satisfy `e^{A₀} = QR`
but `e^{QᵀA₀Q} = I` while `RQ = I` holds too; with `A₀ = I` instead,
`e^{QᵀA₀Q} = e^{4}I ≠ eI = RQ`. -/
theorem qr_mutant_false :
    ¬ (∀ Q R A₀ : Matrix (Fin 2) (Fin 2) ℝ, NormedSpace.exp A₀ = Q * R →
        NormedSpace.exp (Qᵀ * A₀ * Q) = R * Q) := by
  intro h
  have h4 : ((2 : ℝ) • (1 : Matrix (Fin 2) (Fin 2) ℝ))ᵀ * 1 * ((2 : ℝ) • 1)
      = diagonal fun _ => 4 := by
    ext a b; fin_cases a <;> fin_cases b <;> simp [diagonal] <;> norm_num
  have hQR : ((2 : ℝ) • (1 : Matrix (Fin 2) (Fin 2) ℝ))
      * ((1 / 2 : ℝ) • NormedSpace.exp (1 : Matrix (Fin 2) (Fin 2) ℝ))
      = NormedSpace.exp (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
    rw [Matrix.smul_mul, Matrix.one_mul, smul_smul]; norm_num
  have hRQ : ((1 / 2 : ℝ) • NormedSpace.exp (1 : Matrix (Fin 2) (Fin 2) ℝ))
      * ((2 : ℝ) • (1 : Matrix (Fin 2) (Fin 2) ℝ))
      = NormedSpace.exp (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
    rw [Matrix.mul_smul, Matrix.mul_one, smul_smul]; norm_num
  have key := h ((2 : ℝ) • 1) ((1 / 2 : ℝ) • NormedSpace.exp 1) 1 hQR.symm
  rw [hRQ, h4, ← diagonal_one, Matrix.exp_diagonal, Matrix.exp_diagonal] at key
  have := congrFun (congrFun key 0) 0
  simp only [diagonal_apply_eq, Pi.coe_exp, ← Real.exp_eq_exp_ℝ] at this
  have h14 : Real.exp 1 < Real.exp 4 := Real.exp_lt_exp.mpr (by norm_num)
  linarith

end LeanReal.Chap02Toda

#print axioms LeanReal.Chap02Toda.piSo_skew
#print axioms LeanReal.Chap02Toda.piSo_of_skew
#print axioms LeanReal.Chap02Toda.piSo_of_upper
#print axioms LeanReal.Chap02Toda.sub_piSo_upper
#print axioms LeanReal.Chap02Toda.skew_upper_eq_zero
#print axioms LeanReal.Chap02Toda.isospectral
#print axioms LeanReal.Chap02Toda.orth_deriv_zero
#print axioms LeanReal.Chap02Toda.orth_preserved
#print axioms LeanReal.Chap02Toda.conj_deriv
#print axioms LeanReal.Chap02Toda.qr_step
#print axioms LeanReal.Chap02Toda.isospectral_mutant_false
#print axioms LeanReal.Chap02Toda.orth_mutant_false
#print axioms LeanReal.Chap02Toda.piSo_sign_mutant_false
#print axioms LeanReal.Chap02Toda.qr_mutant_false
