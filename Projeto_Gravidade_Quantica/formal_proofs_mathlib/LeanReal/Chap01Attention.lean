import Mathlib.Analysis.PSeries
import Mathlib.Analysis.Normed.Ring.InfiniteSum
import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Topology.Algebra.InfiniteSum.Order
import Mathlib.LinearAlgebra.Matrix.Notation

/-!
# Capitulo 1, `thm:attention_sobolev` (item 2 do Lote B4 do `PLANO_LIVRO_A.md`):
forma de coeficientes

Fonte: `unified_quantum_gravity_book/chap01_functional_realizations_matrices_tensors.tex`,
Proposicao "Sobolev Bound for Attention Realizations" (`thm:attention_sobolev`), com a
realizacao harmonica (eq:fourier_realization) `f_A(x) = ∑_{k₁,k₂=1}^n a_{k₁k₂} e^{i(k₁x₁+k₂x₂)}`.

Enunciado do livro. Para `λ > 0` e
`R_Attn(𝒜) = ∑_{b,h} ∫_{𝕋²} (|f|² + ‖∇f‖² + λ|Δf|²) dμ`:
> (i) `sup_{𝕋²} |f_{𝒜_{b,h}}| ≤ C_λ √R_Attn(𝒜)`, `C_λ² = ∑_{k ∈ ℤ²} (1 + |k|² + λ|k|⁴)⁻¹ < ∞`;
>     `C_λ → ∞` quando `λ → 0`;
> (ii) para toda matriz de atencao softmax (entradas `≥ 0`, linhas somando `1`),
>     `f_{𝒜_{b,h}}(0,0) = ∑_{i,j} 𝒜_{b,h,i,j} = N`; logo `sup |f| ≥ N` e `R_Attn ≥ N²/C_λ²`.
Prova do livro: Parseval da `∫(|f|²+‖∇f‖²+λ|Δf|²)dμ = ∑_k w_λ(k)|a_k|²`; Cauchy–Schwarz da
`|f(x)| ≤ ∑|a_k| ≤ (∑ w_λ|a_k|²)^{1/2} C_λ`; a serie de `C_λ²` converge porque os termos sao
`O(λ⁻¹|k|⁻⁴)`; (ii) todas as exponenciais valem `1` na origem.

## Reducao declarada

* Tudo em COEFICIENTES: `energy λ a = ∑_i w_λ(k_i) |a_i|²` e a definicao usada para a energia
  de uma fatia; a identidade de Parseval com `∫_{𝕋²}` NAO e formalizada (fica G no plano). Um
  polinomio trigonometrico e `trig a freq x = ∑_i a_i e^{i(k_i·x)}` com `freq : ι → ℤ²`
  injetiva (as frequencias `(k₁,k₂) ∈ {1..n}²` do livro sao `freqN`).
* `w_λ(k) = 1 + (k₁² + k₂²) + λ(k₁² + k₂²)²`, `C_λ² = ∑' 1/w_λ` (`tsum`; vale `0` se nao
  somavel, por isso a somabilidade e provada para `λ > 0`).
* Provado: Cauchy–Schwarz ponderado; somabilidade de `1/w_λ` sobre `ℤ²` via
  `w_λ(k) ≥ min(1,4λ)(1+k₁²)(1+k₂²)`; a cota `‖f(x)‖ ≤ C_λ √energy ≤ C_λ √R`; `f(0,0) = N`
  para matrizes com linhas somando `1` (as entradas `≥ 0` nao sao usadas); `R ≥ N²/C_λ²`.
* NAO formalizado: `C_λ → ∞` quando `λ → 0` (divergencia de `∑ 1/(1+|k|²)` em `ℤ²`);
  a identificacao de `energy` com a integral.
-/

noncomputable section

namespace LeanReal.Chap01Attention

open Finset Complex

/-- Peso de Sobolev `w_λ(k) = 1 + |k|² + λ|k|⁴`, com `|k|² = k₁² + k₂²`. -/
def weight (lam : ℝ) (k : ℤ × ℤ) : ℝ :=
  1 + ((k.1 : ℝ) ^ 2 + (k.2 : ℝ) ^ 2) + lam * ((k.1 : ℝ) ^ 2 + (k.2 : ℝ) ^ 2) ^ 2

/-- Polinomio trigonometrico `f(x) = ∑_i a_i e^{i(k_i · x)}`, frequencias `freq i ∈ ℤ²`. -/
def trig {ι : Type*} [Fintype ι] (a : ι → ℂ) (freq : ι → ℤ × ℤ) (x : ℝ × ℝ) : ℂ :=
  ∑ i, a i * Complex.exp ((((freq i).1 : ℝ) * x.1 + ((freq i).2 : ℝ) * x.2 : ℝ) * Complex.I)

/-- Energia de Sobolev em coeficientes, `∑_i w_λ(k_i) |a_i|²`
(igual a `∫ |f|² + ‖∇f‖² + λ|Δf|² dμ` por Parseval, nao formalizado). -/
def energy {ι : Type*} [Fintype ι] (lam : ℝ) (a : ι → ℂ) (freq : ι → ℤ × ℤ) : ℝ :=
  ∑ i, weight lam (freq i) * ‖a i‖ ^ 2

/-- `C_λ² = ∑_{k ∈ ℤ²} 1/w_λ(k)`. -/
def Csq (lam : ℝ) : ℝ := ∑' k : ℤ × ℤ, 1 / weight lam k

/-- Penalidade `R_Attn = ∑_{(b,h)} energy` das fatias `A (b,h)`. -/
def penalty {ι β : Type*} [Fintype ι] [Fintype β] (lam : ℝ) (A : β → ι → ℂ)
    (freq : ι → ℤ × ℤ) : ℝ :=
  ∑ b, energy lam (A b) freq

/-! ## O peso e a serie `C_λ²` -/

theorem weight_pos (lam : ℝ) (hlam : 0 ≤ lam) (k : ℤ × ℤ) : 0 < weight lam k := by
  unfold weight; positivity

/-- `w_λ(k) ≥ min(1,4λ)(1 + k₁²)(1 + k₂²)`, porque `|k|⁴ ≥ 4k₁²k₂²`. -/
theorem weight_ge (lam : ℝ) (hlam : 0 < lam) (k : ℤ × ℤ) :
    min 1 (4 * lam) * ((1 + (k.1 : ℝ) ^ 2) * (1 + (k.2 : ℝ) ^ 2)) ≤ weight lam k := by
  have h1 : min 1 (4 * lam) ≤ 1 := min_le_left _ _
  have h2 : min 1 (4 * lam) ≤ 4 * lam := min_le_right _ _
  set a := (k.1 : ℝ) ^ 2 with ha
  set b := (k.2 : ℝ) ^ 2 with hb
  have ha0 : 0 ≤ a := sq_nonneg _
  have hb0 : 0 ≤ b := sq_nonneg _
  have e1 : min 1 (4 * lam) * (1 + a + b) ≤ 1 * (1 + a + b) :=
    mul_le_mul_of_nonneg_right h1 (by positivity)
  have e2 : min 1 (4 * lam) * (a * b) ≤ 4 * lam * (a * b) :=
    mul_le_mul_of_nonneg_right h2 (by positivity)
  have e3 : 0 ≤ lam * (a - b) ^ 2 := by positivity
  unfold weight
  nlinarith [e1, e2, e3]

theorem one_div_weight_le (lam : ℝ) (hlam : 0 < lam) (k : ℤ × ℤ) :
    1 / weight lam k ≤
      (min 1 (4 * lam))⁻¹ * (1 / (1 + (k.1 : ℝ) ^ 2) * (1 / (1 + (k.2 : ℝ) ^ 2))) := by
  have hm : 0 < min 1 (4 * lam) := lt_min one_pos (by linarith)
  calc 1 / weight lam k
      ≤ 1 / (min 1 (4 * lam) * ((1 + (k.1 : ℝ) ^ 2) * (1 + (k.2 : ℝ) ^ 2))) :=
        one_div_le_one_div_of_le (by positivity) (weight_ge lam hlam k)
    _ = (min 1 (4 * lam))⁻¹ * (1 / (1 + (k.1 : ℝ) ^ 2) * (1 / (1 + (k.2 : ℝ) ^ 2))) := by
        simp only [one_div, mul_inv]

/-- `∑_{n ∈ ℤ} 1/(1+n²) < ∞`. -/
theorem summable_one_div_one_add_sq : Summable (fun n : ℤ => 1 / (1 + (n : ℝ) ^ 2)) := by
  refine Summable.of_norm_bounded_eventually (g := fun n : ℤ => 1 / (n : ℝ) ^ 2) ?_ ?_
  · exact Real.summable_one_div_int_pow.mpr one_lt_two
  · have hsub : {n : ℤ | ¬ ‖1 / (1 + (n : ℝ) ^ 2)‖ ≤ 1 / (n : ℝ) ^ 2} ⊆ {0} := by
      intro n hn
      simp only [Set.mem_ofPred_eq, Set.mem_singleton_iff] at hn ⊢
      by_contra h0
      apply hn
      rw [Real.norm_eq_abs, abs_of_pos (by positivity)]
      apply one_div_le_one_div_of_le
      · have : (n : ℝ) ≠ 0 := by exact_mod_cast h0
        positivity
      · linarith [sq_nonneg (n : ℝ)]
    exact Filter.eventually_cofinite.mpr ((Set.finite_singleton 0).subset hsub)

/-- **`thm:attention_sobolev` (i), convergencia**: `∑_{k ∈ ℤ²} 1/w_λ(k) < ∞` para `λ > 0`. -/
theorem summable_one_div_weight (lam : ℝ) (hlam : 0 < lam) :
    Summable (fun k : ℤ × ℤ => 1 / weight lam k) := by
  have hprod : Summable (fun k : ℤ × ℤ => 1 / (1 + (k.1 : ℝ) ^ 2) * (1 / (1 + (k.2 : ℝ) ^ 2))) :=
    summable_one_div_one_add_sq.mul_of_nonneg summable_one_div_one_add_sq
      (fun n => by positivity) (fun n => by positivity)
  exact Summable.of_nonneg_of_le
    (fun k => by have := weight_pos lam hlam.le k; positivity)
    (fun k => one_div_weight_le lam hlam k) (hprod.mul_left _)

theorem Csq_pos (lam : ℝ) (hlam : 0 < lam) : 0 < Csq lam :=
  Summable.tsum_pos (summable_one_div_weight lam hlam)
    (fun k => by have := weight_pos lam hlam.le k; positivity) (0, 0)
    (by have := weight_pos lam hlam.le (0, 0); positivity)

/-! ## Cauchy–Schwarz ponderado e a cota do supremo -/

/-- `(∑ |a_i|)² ≤ (∑ w_λ(k_i)|a_i|²)(∑ 1/w_λ(k_i))`. -/
theorem sum_norm_sq_le {ι : Type*} [Fintype ι] (lam : ℝ) (hlam : 0 ≤ lam) (a : ι → ℂ)
    (freq : ι → ℤ × ℤ) :
    (∑ i, ‖a i‖) ^ 2 ≤ energy lam a freq * ∑ i, 1 / weight lam (freq i) := by
  have h := Finset.sum_mul_sq_le_sq_mul_sq Finset.univ
    (fun i => Real.sqrt (weight lam (freq i)) * ‖a i‖) (fun i => 1 / Real.sqrt (weight lam (freq i)))
  have e1 : ∀ i, Real.sqrt (weight lam (freq i)) * ‖a i‖ * (1 / Real.sqrt (weight lam (freq i)))
      = ‖a i‖ := by
    intro i
    have hs : Real.sqrt (weight lam (freq i)) ≠ 0 :=
      (Real.sqrt_pos.mpr (weight_pos lam hlam (freq i))).ne'
    field_simp
  have e2 : ∀ i, (Real.sqrt (weight lam (freq i)) * ‖a i‖) ^ 2 = weight lam (freq i) * ‖a i‖ ^ 2 := by
    intro i; rw [mul_pow, Real.sq_sqrt (weight_pos lam hlam (freq i)).le]
  have e3 : ∀ i, (1 / Real.sqrt (weight lam (freq i))) ^ 2 = 1 / weight lam (freq i) := by
    intro i; rw [div_pow, one_pow, Real.sq_sqrt (weight_pos lam hlam (freq i)).le]
  simp only [e1, e2, e3] at h
  exact h

/-- `|f(x)| ≤ ∑ |a_i|`. -/
theorem norm_trig_le_sum {ι : Type*} [Fintype ι] (a : ι → ℂ) (freq : ι → ℤ × ℤ) (x : ℝ × ℝ) :
    ‖trig a freq x‖ ≤ ∑ i, ‖a i‖ := by
  unfold trig
  refine (norm_sum_le _ _).trans (le_of_eq ?_)
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [norm_mul, Complex.norm_exp_ofReal_mul_I, mul_one]

/-- Soma parcial sobre frequencias distintas `≤ C_λ²`. -/
theorem sum_one_div_weight_le_Csq {ι : Type*} [Fintype ι] (lam : ℝ) (hlam : 0 < lam)
    (freq : ι → ℤ × ℤ) (hinj : Function.Injective freq) :
    ∑ i, 1 / weight lam (freq i) ≤ Csq lam := by
  rw [← Finset.sum_image (f := fun k => 1 / weight lam k) (g := freq) (s := Finset.univ)
    (fun _ _ _ _ h => hinj h)]
  exact Summable.sum_le_tsum _ (fun k _ => by have := weight_pos lam hlam.le k; positivity)
    (summable_one_div_weight lam hlam)

theorem energy_nonneg {ι : Type*} [Fintype ι] (lam : ℝ) (hlam : 0 ≤ lam) (a : ι → ℂ)
    (freq : ι → ℤ × ℤ) : 0 ≤ energy lam a freq :=
  Finset.sum_nonneg fun i _ => by have := weight_pos lam hlam (freq i); positivity

/-- **Cota de Sobolev de uma fatia**: `‖f(x)‖ ≤ C_λ √(energy)`, para `λ > 0` e frequencias
distintas. -/
theorem sup_bound {ι : Type*} [Fintype ι] (lam : ℝ) (hlam : 0 < lam) (a : ι → ℂ)
    (freq : ι → ℤ × ℤ) (hinj : Function.Injective freq) (x : ℝ × ℝ) :
    ‖trig a freq x‖ ≤ Real.sqrt (Csq lam) * Real.sqrt (energy lam a freq) := by
  have h1 := norm_trig_le_sum a freq x
  have h2 := sum_norm_sq_le lam hlam.le a freq
  have h3 := sum_one_div_weight_le_Csq lam hlam freq hinj
  have hE := energy_nonneg lam hlam.le a freq
  have h4 : (∑ i, ‖a i‖) ^ 2 ≤ energy lam a freq * Csq lam :=
    h2.trans (mul_le_mul_of_nonneg_left h3 hE)
  have h5 : ∑ i, ‖a i‖ ≤ Real.sqrt (energy lam a freq * Csq lam) := by
    rw [← Real.sqrt_sq (Finset.sum_nonneg fun i _ => norm_nonneg (a i))]
    exact Real.sqrt_le_sqrt h4
  rw [Real.sqrt_mul hE, mul_comm] at h5
  exact h1.trans h5

theorem energy_le_penalty {ι β : Type*} [Fintype ι] [Fintype β] (lam : ℝ) (hlam : 0 ≤ lam)
    (A : β → ι → ℂ) (freq : ι → ℤ × ℤ) (b : β) :
    energy lam (A b) freq ≤ penalty lam A freq :=
  Finset.single_le_sum (f := fun b => energy lam (A b) freq)
    (fun b _ => energy_nonneg lam hlam (A b) freq) (Finset.mem_univ b)

/-- **`thm:attention_sobolev` (i)**, forma de coeficientes: para cada fatia `b`,
`‖f_{A b}(x)‖ ≤ C_λ √R_Attn`. -/
theorem attention_sup_bound {ι β : Type*} [Fintype ι] [Fintype β] (lam : ℝ) (hlam : 0 < lam)
    (freq : ι → ℤ × ℤ) (hinj : Function.Injective freq) (A : β → ι → ℂ) (b : β) (x : ℝ × ℝ) :
    ‖trig (A b) freq x‖ ≤ Real.sqrt (Csq lam) * Real.sqrt (penalty lam A freq) :=
  (sup_bound lam hlam (A b) freq hinj x).trans
    (mul_le_mul_of_nonneg_left (Real.sqrt_le_sqrt (energy_le_penalty lam hlam.le A freq b))
      (Real.sqrt_nonneg _))

/-! ## (ii): o valor na origem de uma matriz estocastica por linhas -/

/-- Frequencias da realizacao (eq:fourier_realization): `(i,j) ↦ (i+1, j+1)`, `i,j ∈ Fin N`. -/
def freqN (N : ℕ) (ij : Fin N × Fin N) : ℤ × ℤ := ((ij.1 : ℤ) + 1, (ij.2 : ℤ) + 1)

theorem freqN_injective (N : ℕ) : Function.Injective (freqN N) := by
  intro ij ij' h
  simp only [freqN, Prod.mk.injEq, add_left_inj, Nat.cast_inj, Fin.val_inj] at h
  exact Prod.ext h.1 h.2

/-- Coeficientes `a_{ij} = A_{ij}` de uma matriz. -/
def coeffs {N : ℕ} (A : Matrix (Fin N) (Fin N) ℂ) (ij : Fin N × Fin N) : ℂ := A ij.1 ij.2

theorem trig_zero {ι : Type*} [Fintype ι] (a : ι → ℂ) (freq : ι → ℤ × ℤ) :
    trig a freq (0, 0) = ∑ i, a i := by
  simp [trig]

/-- **`thm:attention_sobolev` (ii)**: `f_A(0,0) = ∑_{ij} A_{ij} = N` se as linhas somam `1`.
(A positividade das entradas nao e usada.) -/
theorem value_at_origin (N : ℕ) (A : Matrix (Fin N) (Fin N) ℂ) (hrow : ∀ i, ∑ j, A i j = 1) :
    trig (coeffs A) (freqN N) (0, 0) = N := by
  rw [trig_zero]
  simp only [coeffs]
  rw [Fintype.sum_prod_type]
  simp [hrow]

/-- **`thm:attention_sobolev` (ii)**: `N ≤ sup |f| ≤ C_λ √R_Attn`. -/
theorem attention_lower_bound {β : Type*} [Fintype β] (lam : ℝ) (hlam : 0 < lam) (N : ℕ)
    (A : β → Matrix (Fin N) (Fin N) ℂ) (hrow : ∀ b i, ∑ j, A b i j = 1) (b : β) :
    (N : ℝ) ≤ Real.sqrt (Csq lam) * Real.sqrt (penalty lam (fun b => coeffs (A b)) (freqN N)) := by
  have h := attention_sup_bound lam hlam (freqN N) (freqN_injective N) (fun b => coeffs (A b)) b
    (0, 0)
  rw [value_at_origin N (A b) (hrow b)] at h
  simpa using h

/-- **`thm:attention_sobolev` (ii)**: `R_Attn ≥ N²/C_λ²`. -/
theorem penalty_ge {β : Type*} [Fintype β] (lam : ℝ) (hlam : 0 < lam) (N : ℕ)
    (A : β → Matrix (Fin N) (Fin N) ℂ) (hrow : ∀ b i, ∑ j, A b i j = 1) (b : β) :
    (N : ℝ) ^ 2 / Csq lam ≤ penalty lam (fun b => coeffs (A b)) (freqN N) := by
  have h := attention_lower_bound lam hlam N A hrow b
  have hC := Csq_pos lam hlam
  have hP : 0 ≤ penalty lam (fun b => coeffs (A b)) (freqN N) :=
    Finset.sum_nonneg fun b _ => energy_nonneg lam hlam.le _ _
  rw [div_le_iff₀ hC]
  have := pow_le_pow_left₀ (Nat.cast_nonneg N) h 2
  rwa [mul_pow, Real.sq_sqrt hC.le, Real.sq_sqrt hP, mul_comm] at this

/-! ## Testemunha: `N = 2`, `A = [[1/2,1/2],[1/2,1/2]]`, `λ = 1`, uma fatia

As linhas somam `1`, `f_A(0,0) = 2` e a energia de coeficientes e `71/2`
(`w(1,1) = 7`, `w(1,2) = w(2,1) = 31`, `w(2,2) = 73`, pesos `1/4`). -/

/-- A matriz de atencao uniforme `2 × 2`. -/
def Aw : Matrix (Fin 2) (Fin 2) ℂ := !![((1 / 2 : ℝ) : ℂ), ((1 / 2 : ℝ) : ℂ); ((1 / 2 : ℝ) : ℂ), ((1 / 2 : ℝ) : ℂ)]

theorem Aw_row (i : Fin 2) : ∑ j, Aw i j = 1 := by
  fin_cases i <;> simp [Aw, Fin.sum_univ_two] <;> norm_num

theorem witness_origin : trig (coeffs Aw) (freqN 2) (0, 0) = 2 := by
  have := value_at_origin 2 Aw Aw_row
  simpa using this

theorem witness_energy : energy 1 (coeffs Aw) (freqN 2) = 71 / 2 := by
  have h12 : ‖((1 / 2 : ℝ) : ℂ)‖ = 1 / 2 := by
    rw [Complex.norm_real, Real.norm_eq_abs, abs_of_pos (by norm_num)]
  simp only [energy, Fintype.sum_prod_type, Fin.sum_univ_two, coeffs, freqN, weight, Aw]
  simp
  norm_num

/-- Hipoteses e conclusoes do teorema na testemunha: `λ = 1 > 0`, linhas somando `1`,
`f(0,0) = 2 = N`, e `4/C_1² ≤ R = 71/2`. -/
theorem witness :
    (0 : ℝ) < 1 ∧ (∀ i, ∑ j, Aw i j = 1) ∧ trig (coeffs Aw) (freqN 2) (0, 0) = 2 ∧
    ((2 : ℕ) : ℝ) ^ 2 / Csq 1 ≤ penalty 1 (fun _ : Fin 1 => coeffs Aw) (freqN 2) ∧
    penalty 1 (fun _ : Fin 1 => coeffs Aw) (freqN 2) = 71 / 2 := by
  refine ⟨one_pos, Aw_row, witness_origin, ?_, ?_⟩
  · exact penalty_ge 1 one_pos 2 (fun _ => Aw) (fun _ => Aw_row) 0
  · simp [penalty, witness_energy]

/-! ## Mutantes provados FALSOS -/

/-- Mutante 1: sem a hipotese "linhas somam `1`", `f_A(0,0) = N` e falso (`A = 0`, `N = 1`). -/
theorem mutant_no_stochastic_false :
    ¬ (∀ (N : ℕ) (A : Matrix (Fin N) (Fin N) ℂ), trig (coeffs A) (freqN N) (0, 0) = N) := by
  intro h
  have := h 1 0
  rw [trig_zero] at this
  simp [coeffs] at this

/-- Mutante 2: a cota SEM pesos, `‖f(x)‖ ≤ (∑ |a_i|²)^{1/2}` (isto e, sem `C_λ`), e falsa:
`a = (1,1)` em duas frequencias distintas da `f(0,0) = 2 > √2`. -/
theorem mutant_unweighted_false :
    ¬ (∀ (ι : Type) [Fintype ι] (a : ι → ℂ) (freq : ι → ℤ × ℤ), Function.Injective freq →
        ∀ x : ℝ × ℝ, ‖trig a freq x‖ ≤ Real.sqrt (∑ i, ‖a i‖ ^ 2)) := by
  intro h
  have hinj : Function.Injective (fun i : Fin 2 => ((i : ℤ), (0 : ℤ))) := by
    intro i j hij
    simp only [Prod.mk.injEq, Nat.cast_inj, Fin.val_inj, and_true] at hij
    exact hij
  have := h (Fin 2) (fun _ => 1) (fun i => ((i : ℤ), (0 : ℤ))) hinj (0, 0)
  rw [trig_zero] at this
  simp at this

/-- Mutante 3: para `λ < 0` o peso nao e positivo (`w_{−1}(1,1) = −1`), e o argumento de
Cauchy–Schwarz ponderado nao se aplica. -/
theorem mutant_negative_lambda_false : ¬ (∀ (lam : ℝ) (k : ℤ × ℤ), 0 < weight lam k) := by
  intro h
  have := h (-1) (1, 1)
  norm_num [weight] at this

end LeanReal.Chap01Attention

#print axioms LeanReal.Chap01Attention.weight_ge
#print axioms LeanReal.Chap01Attention.summable_one_div_weight
#print axioms LeanReal.Chap01Attention.Csq_pos
#print axioms LeanReal.Chap01Attention.sum_norm_sq_le
#print axioms LeanReal.Chap01Attention.sup_bound
#print axioms LeanReal.Chap01Attention.attention_sup_bound
#print axioms LeanReal.Chap01Attention.value_at_origin
#print axioms LeanReal.Chap01Attention.attention_lower_bound
#print axioms LeanReal.Chap01Attention.penalty_ge
#print axioms LeanReal.Chap01Attention.witness
#print axioms LeanReal.Chap01Attention.mutant_no_stochastic_false
#print axioms LeanReal.Chap01Attention.mutant_unweighted_false
#print axioms LeanReal.Chap01Attention.mutant_negative_lambda_false
