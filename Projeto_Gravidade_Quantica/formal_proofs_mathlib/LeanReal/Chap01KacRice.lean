import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Data.Nat.Choose.Vandermonde
import Mathlib.Data.Nat.Choose.Central
import Mathlib.Data.Fintype.Pi
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-!
# Capitulo 1, `thm:kac_rice_tensors`: nucleos algebricos (item 5 do Lote A1, `PLANO_LIVRO_A.md`)

Fonte: `unified_quantum_gravity_book/chap01_functional_realizations_matrices_tensors.tex`,
Teorema "Complexity of the Isotropic Tensor Landscape" (`thm:kac_rice_tensors`).

Enunciado congelado (so as partes formalizadas):

* (i) Para `𝒯 ∈ (ℝⁿ)^{⊗d}` com entradas independentes `N(0,1)` e `f(x) = 𝒯(x,…,x)`,
  `E[f(x) f(y)] = (x·y)^d`. A prova do livro: `E[f(x)f(y)] = ∑_{i ∈ [n]^d} ∏_α x_{i_α} y_{i_α}`
  (covariancia `E[𝒯_i 𝒯_j] = δ_{ij}`) e essa soma vale `(x·y)^d`.
* (iv) No modelo simetrico com entradas independentes de variancia comum `1`, indexadas por
  multiconjuntos, `Var f(x) = ∑_𝐦 mult(𝐦)² x^{2𝐦}`; `Var f(e₁) = 1`;
  `Var f((e₁+e₂)/√2) = 2^{-d} ∑_{j=0}^d C(d,j)² = 2^{-d} C(2d,d)`, que vale `3/2` (d = 2) e
  `5/2` (d = 3); logo o campo nao e isotropico para `n ≥ 2`.

## Reducao declarada

* A parte probabilistica (gaussianidade, independencia) NAO e formalizada. Em (i), a
  covariancia das entradas entra como a matriz `δ_{ij}` (hipotese `hcov`, explicita) e prova-se
  a identidade algebrica `∑_{i,j} C_{ij} x^i y^j = (x·y)^d`, que e o passo do livro.
* Em (iv), a formula `Var f(x) = ∑_𝐦 mult(𝐦)² x^{2𝐦}` e tomada do livro (soma de variancias de
  termos independentes). Nos pontos `x = t₁e₁ + t₂e₂`, so contam multiconjuntos com `j` copias
  de `1` e `d-j` de `2`, com `mult = C(d,j)`; a soma fica `∑_j C(d,j)² (t₁²)^j (t₂²)^{d-j}`.
  Essa e a funcao `varSym` abaixo (reducao a `n = 2` coordenadas nao nulas).
* Partes (ii), (iii) e a cota de Cartwright–Sturmfels ficam fora.
-/

noncomputable section

namespace LeanReal.Chap01KacRice

open Finset

/-- **`thm:kac_rice_tensors` (i), passo algebrico**: `∑_{i ∈ [n]^d} ∏_α x_{i_α} y_{i_α} = (x·y)^d`. -/
theorem sum_multiindex_eq_pow (n d : ℕ) (x y : Fin n → ℝ) :
    ∑ i : Fin d → Fin n, ∏ a, x (i a) * y (i a) = (∑ j, x j * y j) ^ d := by
  have h := Finset.prod_univ_sum (fun _ : Fin d => (univ : Finset (Fin n)))
    (fun _ j => x j * y j)
  rw [Fintype.piFinset_univ] at h
  rw [← h, Finset.prod_const, Finset.card_univ, Fintype.card_fin]

/-- O polinomio `x^i = ∏_α x_{i_α}` associado ao multi-indice ordenado `i ∈ [n]^d`. -/
def mono {n d : ℕ} (x : Fin n → ℝ) (i : Fin d → Fin n) : ℝ := ∏ a, x (i a)

/-- **`thm:kac_rice_tensors` (i)**: se a covariancia das entradas e `δ_{ij}` (hipotese `hcov`,
que substitui "entradas independentes `N(0,1)`"), a covariancia
`∑_{i,j} C_{ij} x^i y^j` de `f(x) = ∑_i 𝒯_i x^i` vale `(x·y)^d`. -/
theorem covariance_eq_pow (n d : ℕ) (C : (Fin d → Fin n) → (Fin d → Fin n) → ℝ)
    (hcov : ∀ i j, C i j = if i = j then 1 else 0) (x y : Fin n → ℝ) :
    ∑ i, ∑ j, C i j * (mono x i * mono y j) = (∑ k, x k * y k) ^ d := by
  rw [← sum_multiindex_eq_pow]
  refine Finset.sum_congr rfl fun i _ => ?_
  simp only [hcov, ite_mul, one_mul, zero_mul, Finset.sum_ite_eq, Finset.mem_univ, ite_true,
    mono, ← Finset.prod_mul_distrib]

/-- Variancia do modelo simetrico (iv) em `x = t₁e₁ + t₂e₂`:
`∑_{j=0}^d C(d,j)² (t₁²)^j (t₂²)^{d-j}` (multiconjuntos com `j` uns e `d-j` dois). -/
def varSym (d : ℕ) (t₁ t₂ : ℝ) : ℝ :=
  ∑ j ∈ range (d + 1), ((d.choose j : ℕ) : ℝ) ^ 2 * (t₁ ^ 2) ^ j * (t₂ ^ 2) ^ (d - j)

/-- **(iv)** `Var f(e₁) = 1`. -/
theorem varSym_e1 (d : ℕ) : varSym d 1 0 = 1 := by
  unfold varSym
  rw [Finset.sum_eq_single d]
  · simp
  · intro j hj hjd
    have : 0 < d - j := by
      have := Finset.mem_range.mp hj
      omega
    simp [zero_pow this.ne']
  · intro h; exact absurd (Finset.mem_range.mpr (Nat.lt_succ_self d)) h

/-- **(iv)** `∑_{j=0}^d C(d,j)² = C(2d,d)` (Vandermonde). -/
theorem sum_choose_sq (d : ℕ) : ∑ j ∈ range (d + 1), (d.choose j) ^ 2 = (2 * d).choose d :=
  Nat.sum_range_choose_sq d

/-- **(iv)** `Var f((e₁+e₂)/√2) = 2^{-d} C(2d,d)`. -/
theorem varSym_diag (d : ℕ) :
    varSym d (1 / Real.sqrt 2) (1 / Real.sqrt 2) = ((2 * d).choose d : ℝ) / 2 ^ d := by
  have h2 : (1 / Real.sqrt 2) ^ 2 = (1 / 2 : ℝ) := by
    rw [div_pow, Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2)]; norm_num
  unfold varSym
  rw [h2]
  have : ∀ j ∈ range (d + 1), ((d.choose j : ℕ) : ℝ) ^ 2 * (1 / 2 : ℝ) ^ j * (1 / 2) ^ (d - j)
      = ((d.choose j : ℕ) : ℝ) ^ 2 / 2 ^ d := by
    intro j hj
    have hj' : j ≤ d := Nat.lt_succ_iff.mp (Finset.mem_range.mp hj)
    rw [mul_assoc, ← pow_add, Nat.add_sub_cancel' hj', one_div, inv_pow, div_eq_mul_inv]
  rw [Finset.sum_congr rfl this]
  simp_rw [div_eq_mul_inv]
  rw [← Finset.sum_mul]
  congr 1
  rw [← sum_choose_sq]; push_cast; rfl

/-- **(iv)** valor `3/2` para `d = 2`. -/
theorem varSym_diag_two : varSym 2 (1 / Real.sqrt 2) (1 / Real.sqrt 2) = 3 / 2 := by
  rw [varSym_diag]; norm_num [Nat.choose]

/-- **(iv)** valor `5/2` para `d = 3`. -/
theorem varSym_diag_three : varSym 3 (1 / Real.sqrt 2) (1 / Real.sqrt 2) = 5 / 2 := by
  rw [varSym_diag]; norm_num [Nat.choose]

/-- `2^d < C(2d,d)` para `d ≥ 2`. -/
theorem two_pow_lt_centralBinom (d : ℕ) (hd : 2 ≤ d) : 2 ^ d < (2 * d).choose d := by
  rw [← Nat.centralBinom_eq_two_mul_choose]
  induction d, hd using Nat.le_induction with
  | base => decide
  | succ k hk ih =>
    have h := Nat.succ_mul_centralBinom_succ k
    have : 2 * (k + 1) * Nat.centralBinom k ≤ (k + 1) * Nat.centralBinom (k + 1) := by
      rw [h]; exact Nat.mul_le_mul_right _ (by omega)
    have h3 : 2 * Nat.centralBinom k ≤ Nat.centralBinom (k + 1) := by
      have : (k + 1) * (2 * Nat.centralBinom k) ≤ (k + 1) * Nat.centralBinom (k + 1) := by
        linarith
      exact Nat.le_of_mul_le_mul_left this (Nat.succ_pos k)
    rw [pow_succ]; omega

/-- **(iv), consequencia**: para todo `d ≥ 2`, `Var f((e₁+e₂)/√2) > 1 = Var f(e₁)`; o modelo
simetrico com variancias comuns nao e isotropico. -/
theorem not_isotropic (d : ℕ) (hd : 2 ≤ d) :
    varSym d 1 0 < varSym d (1 / Real.sqrt 2) (1 / Real.sqrt 2) := by
  rw [varSym_e1, varSym_diag, lt_div_iff₀ (by positivity), one_mul]
  exact_mod_cast two_pow_lt_centralBinom d hd

/-! ## Testemunhas nao degeneradas -/

/-- Testemunha de (i): `n = 2`, `d = 3`, `x = (1,2)`, `y = (3,-1)`: `(x·y)^3 = 1`, e a soma
sobre os `8` multi-indices da o mesmo valor; `x ⊥̸ y` e as parcelas nao sao todas nulas. -/
example : ∑ i : Fin 3 → Fin 2, ∏ a, ![1, 2] (i a) * ![(3:ℝ), -1] (i a) = 1 := by
  rw [sum_multiindex_eq_pow]; simp [Fin.sum_univ_two]; norm_num

/-- Testemunha de (i) com a hipotese de covariancia instanciada (`C = δ`). -/
example : ∑ i : Fin 2 → Fin 2, ∑ j : Fin 2 → Fin 2,
    (if i = j then (1:ℝ) else 0) * (mono ![1, 2] i * mono ![(3:ℝ), 1] j) = 25 := by
  rw [covariance_eq_pow 2 2 _ (fun _ _ => rfl)]; simp [Fin.sum_univ_two]; norm_num

/-! ## Mutantes provados FALSOS -/

/-- Mutante 1: "o modelo simetrico e isotropico" (`Var f((e₁+e₂)/√2) = Var f(e₁)` para todo
`d ≥ 2`): falso em `d = 2`. -/
theorem mutant_isotropic_false :
    ¬ ∀ d : ℕ, 2 ≤ d → varSym d (1 / Real.sqrt 2) (1 / Real.sqrt 2) = varSym d 1 0 := by
  intro h
  have := h 2 le_rfl
  rw [varSym_diag_two, varSym_e1] at this
  norm_num at this

/-- Mutante 2: sem o fator `2^{-d}` (`Var = C(2d,d)`), falso em `d = 2` (`3/2 ≠ 6`). -/
theorem mutant_no_normalization_false :
    ¬ ∀ d : ℕ, varSym d (1 / Real.sqrt 2) (1 / Real.sqrt 2) = ((2 * d).choose d : ℝ) := by
  intro h
  have := h 2
  rw [varSym_diag_two] at this
  norm_num [Nat.choose] at this

/-- Mutante 3: covariancia `(x·y)^{d+1}` no lugar de `(x·y)^d`: falso (`n = 1`, `d = 1`,
`x = y = 2`, com `C = δ`). -/
theorem mutant_power_shift_false :
    ¬ ∀ (n d : ℕ) (x y : Fin n → ℝ),
      ∑ i : Fin d → Fin n, ∏ a, x (i a) * y (i a) = (∑ j, x j * y j) ^ (d + 1) := by
  intro h
  have := h 1 1 (fun _ => 2) (fun _ => 2)
  simp at this
  norm_num at this

end LeanReal.Chap01KacRice

#print axioms LeanReal.Chap01KacRice.sum_multiindex_eq_pow
#print axioms LeanReal.Chap01KacRice.covariance_eq_pow
#print axioms LeanReal.Chap01KacRice.varSym_e1
#print axioms LeanReal.Chap01KacRice.varSym_diag
#print axioms LeanReal.Chap01KacRice.varSym_diag_two
#print axioms LeanReal.Chap01KacRice.varSym_diag_three
#print axioms LeanReal.Chap01KacRice.not_isotropic
#print axioms LeanReal.Chap01KacRice.mutant_isotropic_false
#print axioms LeanReal.Chap01KacRice.mutant_no_normalization_false
#print axioms LeanReal.Chap01KacRice.mutant_power_shift_false
