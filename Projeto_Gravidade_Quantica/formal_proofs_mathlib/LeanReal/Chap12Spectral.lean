import Mathlib.MeasureTheory.Measure.Haar.NormedSpace
import Mathlib.MeasureTheory.Constructions.HaarToSphere
import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar
import Mathlib.Analysis.SpecialFunctions.Gaussian.GaussianIntegral
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.LinearAlgebra.Matrix.Cartan.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic
import Mathlib.Analysis.Calculus.MeanValue

/-!
# Capitulo 12: dimensao espectral, metrica de Cartan, decaimento (lote LIVRO B3)

Fonte: `unified_quantum_gravity_book/chap12_grand_unification_quantum_gravity_treatise.tex`.
Itens 12.1, 12.2 (parte algebrica) e 12.6 do `PLANO_LIVRO_B.md`.

## 12.1 `thm:running_spectral_dimension`

> Para `α > 0`, seja `P(τ;x,y)` o nucleo do calor de `∂_τ u + (-Δ)^α u = 0` em `ℝ^m` e
> `d_s := -2 d log P(τ;x,x) / d log τ`. Entao `d_s(α,m) = m/α` para todo `τ > 0`.
> Em particular `d_s(1,4) = 4`, `d_s(2,4) = 2`.

**Reducao declarada.** A diagonal do nucleo e DEFINIDA pela formula de Fourier da prova do livro,
`P(τ) := (2π)^{-m} ∫_{ℝ^m} exp(-τ‖k‖^{2α}) dk` (`heatDiag`). Que isso seja a diagonal do nucleo
da EDP nao e formalizado (exigiria a teoria de multiplicadores de Fourier). `m ≥ 1`. A derivada
em `log τ` e a derivada de `s ↦ log P(e^s)` em `s = log τ` (`specDim`). Tudo o mais e provado:
a escala `P(τ) = τ^{-m/(2α)} P(1)` (mudanca de variaveis de Haar), `0 < P(1) < ∞`
(integrabilidade radial + integral Gama), e a derivada.

## 12.2 `thm:cartan_metric_emergence` (parte algebrica e de calculo)

> `t* = (x/m,…,x/m)`, `v` no hiperplano soma zero. `log binom(x, t*+v) = log binom(x,t*) - Q(v)
> + O(|v|^3)`, `Q(v) = ψ'(x/m+1)/2 ∑ v_i^2`. Escrevendo `v = ∑_j c_j α_j`, `α_j = e_j - e_{j+1}`,
> `∑ v_i^2 = cᵀ A_{m-1} c` com `A_{m-1}` a matriz de Cartan.

**Coberto.** (a) Ao longo da reta `s ↦ t* + s v`, a funcao `G(s) = ∑ f(x/m + s v_i)` (com
`f = log Γ(·+1)`, de modo que `log binom = log Γ(x+1) - G`) tem `G'(0) = 0` quando `∑ v_i = 0`,
e `G''(0) = f''(x/m) ∑ v_i^2`: termo linear nulo e Hessiana isotropica. `f` e generica com
derivadas dadas como hipoteses (`hf`, `hf1`); a identificacao `f'' = ψ'` e a assintotica
`ψ'(z+1) = 1/z + O(z^{-2})` NAO sao formalizadas (a Mathlib nao tem trigama). O resto `O(|v|^3)`
de Taylor tambem nao. (b) A identidade de Gram `|∑ c_j α_j|^2 = cᵀ A c` com a matriz
`CartanMatrix.A n` da Mathlib (tridiagonal 2, -1), `n = m - 1`, raizes em `ℝ^{n+1}`.
A existencia das coordenadas `c` (as raizes simples sao base do hiperplano) nao e formalizada;
o livro tambem a pressupoe ("writing v = …").

## 12.6 `thm:neckpinch_condensation` (texto atual, com "almost every")

> `W(t)` solucao de `∂_t W = 2 κ_W W` em `[0,T]`, `W_0 ≥ 0`, `B ⊂ [0,1]^2` de medida positiva com
> `κ_{W(s)}(x,y) ≤ -c < 0` para `s ∈ [0,T]`. Entao para `(x,y) ∈ B`, `t ∈ [0,T]`:
> `0 ≤ W(t,x,y) ≤ W_0(x,y) e^{-2ct}`; e para todo `δ ∈ (0, ‖W_0‖_{L∞(B)})`, `W(t,x,y) ≤ δ` para
> quase todo `(x,y) ∈ B` e todo `t ∈ [t_δ, T]`, `t_δ = (1/2c) ln(‖W_0‖_{L∞(B)}/δ)` (se `t_δ ≤ T`).

**Reducao declarada.** Ponto a ponto: `t ↦ W(t,p)` continua em `[0,T]` com derivada a direita
`2 κ(t,p) W(t,p)` em `[0,T)`, e `t ↦ κ(t,p)` CONTINUA em `[0,T]` (o livro diz so "solucao" e
usa `∫ κ`; continuidade e a hipotese de regularidade que tornamos explicita). `κ` e um dado
(nao se define a curvatura de Ollivier). `‖W_0‖_{L∞(B)}` e `eLpNorm (W 0) ∞ (volume.restrict B)`,
com `W 0` fortemente mensuravel q.t.p. em `B` e `B` mensuravel. A conclusao q.t.p. e
`∀ᵐ p ∂(volume.restrict B)`. O dominio `[0,1]^2` nao e usado (vale em `ℝ×ℝ`).
-/

noncomputable section

namespace LeanReal.Chap12Spectral

open Real Set MeasureTheory Filter Topology Module Matrix
open scoped ENNReal

/-! ## 12.1 Dimensao espectral de um simbolo homogeneo -/

/-- Diagonal do nucleo do calor do simbolo `|k|^{2α}` em `ℝ^m`, pela formula de Fourier da prova
de `thm:running_spectral_dimension`: `P(τ) = (2π)^{-m} ∫ exp(-τ‖k‖^{2α}) dk`. -/
def heatDiag (m : ℕ) (α τ : ℝ) : ℝ :=
  ((2 * π) ^ m)⁻¹ * ∫ k : EuclideanSpace ℝ (Fin m), exp (-(τ * ‖k‖ ^ (2 * α)))

/-- Dimensao espectral `d_s(τ) = -2 d log P / d log τ`, como derivada de `s ↦ log P(e^s)` em
`s = log τ` (`thm:running_spectral_dimension`). -/
def specDim (m : ℕ) (α τ : ℝ) : ℝ :=
  -2 * deriv (fun s => log (heatDiag m α (exp s))) (log τ)

/-- `k ↦ exp(-‖k‖^{2α})` e integravel em `ℝ^m` (`m ≥ 1`, `α > 0`): coordenadas polares
(`integrable_fun_norm_addHaar`) e a integral Gama. -/
theorem integrable_kernel (m : ℕ) (hm : 1 ≤ m) {α : ℝ} (hα : 0 < α) :
    Integrable (fun k : EuclideanSpace ℝ (Fin m) => exp (-‖k‖ ^ (2 * α))) := by
  have : Nontrivial (EuclideanSpace ℝ (Fin m)) := by
    apply Module.nontrivial_of_finrank_pos (R := ℝ)
    simp only [finrank_euclideanSpace, Fintype.card_fin]
    omega
  rw [integrable_fun_norm_addHaar (volume : Measure (EuclideanSpace ℝ (Fin m)))
    (f := fun y : ℝ => exp (-y ^ (2 * α)))]
  have h := integrableOn_rpow_mul_exp_neg_rpow
    (s := ((finrank ℝ (EuclideanSpace ℝ (Fin m)) - 1 : ℕ) : ℝ))
    (by have : (0:ℝ) ≤ ((finrank ℝ (EuclideanSpace ℝ (Fin m)) - 1 : ℕ) : ℝ) := Nat.cast_nonneg _
        linarith)
    (by positivity : (0:ℝ) < 2 * α)
  refine h.congr_fun (fun y hy => ?_) measurableSet_Ioi
  simp only [smul_eq_mul, Real.rpow_natCast]

/-- Lei de escala: `∫ exp(-τ‖k‖^{2α}) = τ^{-m/(2α)} ∫ exp(-‖k‖^{2α})`, por `k ↦ τ^{1/(2α)} k`. -/
theorem integral_scaling (m : ℕ) {α τ : ℝ} (hα : 0 < α) (hτ : 0 < τ) :
    ∫ k : EuclideanSpace ℝ (Fin m), exp (-(τ * ‖k‖ ^ (2 * α))) =
      τ ^ (-((m : ℝ) / (2 * α))) * ∫ k : EuclideanSpace ℝ (Fin m), exp (-‖k‖ ^ (2 * α)) := by
  set R : ℝ := τ ^ (1 / (2 * α)) with hR
  have hRpos : 0 < R := rpow_pos_of_pos hτ _
  have h := Measure.integral_comp_smul (volume : Measure (EuclideanSpace ℝ (Fin m)))
    (fun k => exp (-‖k‖ ^ (2 * α))) R
  have hfun : (fun k : EuclideanSpace ℝ (Fin m) => exp (-‖R • k‖ ^ (2 * α))) =
      fun k => exp (-(τ * ‖k‖ ^ (2 * α))) := by
    funext k
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos hRpos,
      mul_rpow hRpos.le (norm_nonneg _), hR, ← rpow_mul hτ.le,
      one_div_mul_cancel (by positivity), rpow_one]
  simp only [hfun] at h
  rw [h, finrank_euclideanSpace, Fintype.card_fin, smul_eq_mul]
  congr 1
  rw [abs_of_pos (inv_pos.2 (pow_pos hRpos m)), hR, ← rpow_natCast, ← rpow_mul hτ.le,
    ← rpow_neg hτ.le]
  congr 1
  field_simp

/-- `P(1) > 0`. -/
theorem heatDiag_one_pos (m : ℕ) (hm : 1 ≤ m) {α : ℝ} (hα : 0 < α) :
    0 < ∫ k : EuclideanSpace ℝ (Fin m), exp (-‖k‖ ^ (2 * α)) :=
  integral_exp_pos (integrable_kernel m hm hα)

/-- `P(τ) = τ^{-m/(2α)} · (2π)^{-m} ∫ exp(-‖k‖^{2α})`: a forma `C(m,α) τ^{-m/(2α)}` da prova. -/
theorem heatDiag_eq (m : ℕ) {α τ : ℝ} (hα : 0 < α) (hτ : 0 < τ) :
    heatDiag m α τ = heatDiag m α 1 * τ ^ (-((m : ℝ) / (2 * α))) := by
  unfold heatDiag
  rw [integral_scaling m hα hτ]
  simp only [one_mul]
  ring

/-- **`thm:running_spectral_dimension`** (reducao do cabecalho): para `m ≥ 1`, `α > 0` e todo
`τ > 0`, `s ↦ log P(e^s)` tem derivada `-m/(2α)` em `log τ`. -/
theorem hasDerivAt_logP (m : ℕ) (hm : 1 ≤ m) {α τ : ℝ} (hα : 0 < α) (_hτ : 0 < τ) :
    HasDerivAt (fun s => log (heatDiag m α (exp s))) (-((m : ℝ) / (2 * α))) (log τ) := by
  have hC : 0 < heatDiag m α 1 := by
    unfold heatDiag
    simp only [one_mul]
    exact mul_pos (inv_pos.2 (pow_pos (by positivity) m))
      (by simpa using heatDiag_one_pos m hm hα)
  have hfun : (fun s => log (heatDiag m α (exp s))) =
      fun s => log (heatDiag m α 1) + (-((m : ℝ) / (2 * α))) * s := by
    funext s
    rw [heatDiag_eq m hα (exp_pos s), log_mul hC.ne' (rpow_pos_of_pos (exp_pos s) _).ne',
      log_rpow (exp_pos s), log_exp]
  rw [hfun]
  simpa using ((hasDerivAt_id (log τ)).const_mul (-((m : ℝ) / (2 * α)))).const_add
    (log (heatDiag m α 1))

/-- **`thm:running_spectral_dimension`**: `d_s(α,m) = m/α` para todo `τ > 0`. -/
theorem specDim_eq (m : ℕ) (hm : 1 ≤ m) {α τ : ℝ} (hα : 0 < α) (hτ : 0 < τ) :
    specDim m α τ = m / α := by
  unfold specDim
  rw [(hasDerivAt_logP m hm hα hτ).deriv]
  field_simp

/-- Casos do livro: `d_s(1,4) = 4` e `d_s(2,4) = 2`, para todo `τ > 0`. -/
theorem specDim_book_cases {τ : ℝ} (hτ : 0 < τ) :
    specDim 4 1 τ = 4 ∧ specDim 4 2 τ = 2 := by
  constructor
  · rw [specDim_eq 4 (by norm_num) one_pos hτ]; norm_num
  · rw [specDim_eq 4 (by norm_num) two_pos hτ]; norm_num

/-- Testemunha nao degenerada: `P` NAO e constante (em `m = 4`, `α = 1`, `P(1) ≠ P(2)`), de modo
que a derivada nula seria falsa; e `P(1) > 0`. -/
theorem witness_heatDiag : 0 < heatDiag 4 1 1 ∧ heatDiag 4 1 2 ≠ heatDiag 4 1 1 := by
  have hC : 0 < heatDiag 4 1 1 := by
    unfold heatDiag
    simp only [one_mul]
    exact mul_pos (inv_pos.2 (pow_pos (by positivity) 4))
      (by simpa using heatDiag_one_pos 4 (by norm_num) one_pos)
  refine ⟨hC, ?_⟩
  rw [heatDiag_eq 4 one_pos two_pos]
  intro h
  have h2 : (2 : ℝ) ^ (-((4 : ℕ) : ℝ) / (2 * 1)) = 1 := by
    have := mul_left_cancel₀ hC.ne' (h.trans (mul_one _).symm)
    simpa [neg_div] using this
  have : (2 : ℝ) ^ (-((4 : ℕ) : ℝ) / (2 * 1)) = 1 / 4 := by
    norm_num [rpow_neg, show (-(4:ℝ)) / 2 = -2 by norm_num]
  rw [this] at h2
  norm_num at h2

/-- Mutante 1 (`d_s = m/(2α)`, esquecendo o fator `2` da definicao): falso (em `m=4`, `α=1`). -/
theorem mutant_half_false :
    ¬ (∀ (m : ℕ) (α τ : ℝ), 1 ≤ m → 0 < α → 0 < τ → specDim m α τ = m / (2 * α)) := by
  intro h
  have h1 := h 4 1 1 (by norm_num) one_pos one_pos
  rw [specDim_eq 4 (by norm_num) one_pos one_pos] at h1
  norm_num at h1

/-- Mutante 2 (`d_s = m`, independente de `α`): falso (em `m = 4`, `α = 2`). -/
theorem mutant_no_alpha_false :
    ¬ (∀ (m : ℕ) (α τ : ℝ), 1 ≤ m → 0 < α → 0 < τ → specDim m α τ = m) := by
  intro h
  have h1 := h 4 2 1 (by norm_num) two_pos one_pos
  rw [specDim_eq 4 (by norm_num) two_pos one_pos] at h1
  norm_num at h1

/-! ## 12.2 Hessiana baricentrica e a metrica de raizes `A_{m-1}` -/

/-- Raiz simples `α_j = e_j - e_{j+1}` de `A_n` em `ℝ^{n+1}` (`j : Fin n`, `n = m - 1`). -/
def simpleRoot (n : ℕ) (j : Fin n) : Fin (n + 1) → ℝ :=
  fun a => (if a = j.castSucc then 1 else 0) - (if a = j.succ then 1 else 0)

/-- Matriz de Gram das raizes simples = matriz de Cartan `CartanMatrix.A n` da Mathlib
(`thm:cartan_metric_emergence`, passo final da prova). -/
theorem gram_simpleRoot (n : ℕ) (i j : Fin n) :
    ∑ a, simpleRoot n i a * simpleRoot n j a = ((CartanMatrix.A n i j : ℤ) : ℝ) := by
  simp only [simpleRoot, mul_sub, mul_ite, mul_one, mul_zero, Finset.sum_sub_distrib,
    Finset.sum_ite_eq', Finset.mem_univ, ite_true]
  simp only [CartanMatrix.A, Matrix.of_apply, Fin.ext_iff, Fin.val_castSucc, Fin.val_succ]
  split_ifs <;> (try norm_num) <;> omega

/-- **`thm:cartan_metric_emergence`** (identidade de Gram): se `v = ∑_j c_j α_j`, entao
`∑_i v_i^2 = cᵀ A_{m-1} c`. -/
theorem sum_sq_eq_cartan (n : ℕ) (c : Fin n → ℝ) :
    ∑ a, (∑ j, c j * simpleRoot n j a) ^ 2 =
      c ⬝ᵥ (((CartanMatrix.A n).map (Int.cast : ℤ → ℝ)) *ᵥ c) := by
  calc ∑ a, (∑ j, c j * simpleRoot n j a) ^ 2
      = ∑ a, ∑ i, ∑ j, c i * c j * (simpleRoot n i a * simpleRoot n j a) := by
        refine Finset.sum_congr rfl (fun a _ => ?_)
        rw [sq, Finset.sum_mul_sum]
        exact Finset.sum_congr rfl (fun i _ => Finset.sum_congr rfl (fun j _ => by ring))
    _ = ∑ i, ∑ j, c i * c j * ∑ a, simpleRoot n i a * simpleRoot n j a := by
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl (fun i _ => ?_)
        rw [Finset.sum_comm]
        exact Finset.sum_congr rfl (fun j _ => by rw [Finset.mul_sum])
    _ = c ⬝ᵥ (((CartanMatrix.A n).map (Int.cast : ℤ → ℝ)) *ᵥ c) := by
        simp only [gram_simpleRoot, dotProduct, Matrix.mulVec, Matrix.map_apply, Finset.mul_sum]
        exact Finset.sum_congr rfl (fun i _ => Finset.sum_congr rfl (fun j _ => by ring))

/-- Os vetores `∑ c_j α_j` estao no hiperplano soma zero `T_{t*} Δ_{m-1}`. -/
theorem simpleRoot_comb_sum_zero (n : ℕ) (c : Fin n → ℝ) :
    ∑ a, ∑ j, c j * simpleRoot n j a = 0 := by
  rw [Finset.sum_comm]
  refine Finset.sum_eq_zero (fun j _ => ?_)
  rw [← Finset.mul_sum]
  simp [simpleRoot, Finset.sum_sub_distrib]

/-- **`thm:cartan_metric_emergence`** (termo linear e Hessiana ao longo de uma reta).
Seja `G(s) = ∑_i f(b + s v_i)` (com `f = log Γ(·+1)`, `b = x/m`, `log binom(x, t*+sv) =
log Γ(x+1) - G(s)`). Se `f' = f1` perto de `b`, `f1'(b) = f2` e `∑ v_i = 0`, entao
`G'(0) = 0` (termo linear nulo) e `G''(0) = f2 ∑ v_i^2` (Hessiana `f2 · Id` no hiperplano). -/
theorem barycentric_line (m : ℕ) (f f1 : ℝ → ℝ) (b f2 : ℝ)
    (hf : ∀ᶠ y in 𝓝 b, HasDerivAt f (f1 y) y) (hf1 : HasDerivAt f1 f2 b)
    (v : Fin m → ℝ) (hv : ∑ i, v i = 0) :
    (∀ᶠ s in 𝓝 (0:ℝ), HasDerivAt (fun s => ∑ i, f (b + s * v i))
        (∑ i, f1 (b + s * v i) * v i) s) ∧
    ∑ i, f1 (b + 0 * v i) * v i = 0 ∧
    HasDerivAt (fun s => ∑ i, f1 (b + s * v i) * v i) (f2 * ∑ i, v i ^ 2) 0 := by
  have hline : ∀ i, HasDerivAt (fun s : ℝ => b + s * v i) (v i) 0 ∧
      ∀ s, HasDerivAt (fun s : ℝ => b + s * v i) (v i) s := by
    intro i
    have h : ∀ s, HasDerivAt (fun s : ℝ => b + s * v i) (v i) s := fun s => by
      simpa using ((hasDerivAt_id s).mul_const (v i)).const_add b
    exact ⟨h 0, h⟩
  refine ⟨?_, ?_, ?_⟩
  · have hev : ∀ i, ∀ᶠ s in 𝓝 (0:ℝ), HasDerivAt f (f1 (b + s * v i)) (b + s * v i) := by
      intro i
      have ht : Tendsto (fun s : ℝ => b + s * v i) (𝓝 0) (𝓝 b) := by
        have := ((hline i).1).continuousAt.tendsto
        simpa using this
      exact ht.eventually hf
    filter_upwards [Filter.eventually_all.2 hev] with s hs
    have := HasDerivAt.fun_sum (u := Finset.univ) (fun i _ => (hs i).comp s ((hline i).2 s))
    simpa using this
  · simp [← Finset.mul_sum, hv]
  · have := HasDerivAt.fun_sum (u := Finset.univ)
      (fun i _ => (((show HasDerivAt f1 f2 (b + 0 * v i) by simpa using hf1).comp (0:ℝ)
        (hline i).1).mul_const (v i)))
    convert this using 1
    · funext s; simp
    · rw [Finset.mul_sum]
      exact Finset.sum_congr rfl (fun i _ => by ring)

/-- Testemunha (Gram, nao degenerada): `n = 2` (`m = 3`), `c = (1,1)`, `v = (1,0,-1)`,
`∑ v_i^2 = 2 = cᵀ A_2 c`, enquanto `|c|^2 = 2`... e com `c = (1,2)`: `v = (1,1,-2)`, `∑ v^2 = 6`,
`cᵀ A_2 c = 2 - 4 + 8 = 6`, mas `|c|^2 = 5`: a metrica NAO e a euclidiana em `c`. -/
theorem witness_gram :
    ∑ a, (∑ j, (![1, 2] : Fin 2 → ℝ) j * simpleRoot 2 j a) ^ 2 = 6 ∧
    (![1, 2] : Fin 2 → ℝ) ⬝ᵥ (![1, 2] : Fin 2 → ℝ) = 5 := by
  constructor
  · have hv : ∀ a : Fin 3, ∑ j, (![1, 2] : Fin 2 → ℝ) j * simpleRoot 2 j a = ![1, 1, -2] a := by
      intro a
      fin_cases a <;> simp [simpleRoot, Fin.sum_univ_two]
      norm_num
    simp only [hv]
    simp [Fin.sum_univ_succ]
    norm_num
  · simp [dotProduct, Fin.sum_univ_succ]
    norm_num

/-- Testemunha (`barycentric_line`, hipoteses mordem): `f(y) = y^3`, `b = 1`, `v = (1,-1)`:
`G'(0) = 0` e `G''(0) = 6 · 2 = 12 ≠ 0`. -/
theorem witness_barycentric :
    HasDerivAt (fun s => ∑ i : Fin 2, (fun y : ℝ => 3 * y ^ 2) (1 + s * (![1, -1] : Fin 2 → ℝ) i)
        * (![1, -1] : Fin 2 → ℝ) i) 12 0 := by
  have h := (barycentric_line 2 (fun y => y ^ 3) (fun y => 3 * y ^ 2) 1 6
    (Eventually.of_forall (fun y => by simpa using hasDerivAt_pow 3 y))
    (by convert (hasDerivAt_pow 2 (1:ℝ)).const_mul 3 using 1; norm_num)
    ![1, -1] (by simp)).2.2
  convert h using 1
  simp [Fin.sum_univ_succ]
  norm_num

/-- Mutante (sem `∑ v_i = 0`, termo linear nulo): falso para `f(y) = y`, `v = (1,1)`. -/
theorem mutant_linear_term_false :
    ¬ (∀ (f1 : ℝ → ℝ) (b : ℝ) (v : Fin 2 → ℝ), (∀ i j, f1 (b + 0 * v i) = f1 (b + 0 * v j)) →
        ∑ i, f1 (b + 0 * v i) * v i = 0) := by
  intro h
  have := h (fun _ => 1) 0 ![1, 1] (fun _ _ => rfl)
  simp [Fin.sum_univ_succ] at this

/-- Mutante (Gram com a identidade em vez de Cartan, `∑ v_i^2 = |c|^2`): falso pela testemunha. -/
theorem mutant_gram_identity_false :
    ¬ (∀ (n : ℕ) (c : Fin n → ℝ), ∑ a, (∑ j, c j * simpleRoot n j a) ^ 2 = c ⬝ᵥ c) := by
  intro h
  have h1 := h 2 ![1, 2]
  rw [witness_gram.1, witness_gram.2] at h1
  norm_num at h1

/-! ## 12.6 Decaimento exponencial das entradas de curvatura negativa -/

/-- Lema pontual (prova de `thm:neckpinch_condensation`, `(x,y)` fixo): se `W` e continua em
`[0,T]`, `W' = 2κW` a direita em `[0,T)`, `κ` continua em `[0,T]` com `κ ≤ -c` e `W(0) ≥ 0`,
entao `0 ≤ W(t) ≤ W(0) e^{-2ct}` em `[0,T]`. (Vale para todo `c` real; o livro tem `c > 0`.) -/
theorem decay_pointwise (W κ : ℝ → ℝ) (T c : ℝ) (hT : 0 ≤ T)
    (hκc : ContinuousOn κ (Icc 0 T)) (hWc : ContinuousOn W (Icc 0 T))
    (hW : ∀ t ∈ Ico 0 T, HasDerivWithinAt W (2 * κ t * W t) (Ici t) t)
    (hκ : ∀ s ∈ Icc 0 T, κ s ≤ -c) (hW0 : 0 ≤ W 0) :
    ∀ t ∈ Icc 0 T, 0 ≤ W t ∧ W t ≤ W 0 * exp (-2 * c * t) := by
  -- extensao continua de κ a ℝ
  set κ' : ℝ → ℝ := fun s => κ (projIcc 0 T hT s) with hκ'def
  have hκ'c : Continuous κ' :=
    hκc.comp_continuous (continuous_subtype_val.comp continuous_projIcc) (fun s => (projIcc 0 T hT s).2)
  have hκ'eq : ∀ s ∈ Icc 0 T, κ' s = κ s := fun s hs => by
    simp [hκ'def, projIcc_of_mem hT hs]
  set K : ℝ → ℝ := fun t => ∫ s in (0:ℝ)..t, κ' s with hKdef
  have hK : ∀ t, HasDerivAt K (κ' t) t := fun t => (hκ'c.integral_hasStrictDerivAt 0 t).hasDerivAt
  set H : ℝ → ℝ := fun t => W t * exp (-2 * K t) with hHdef
  have hHc : ContinuousOn H (Icc 0 T) :=
    hWc.mul ((continuous_exp.comp (continuous_const.mul
      (continuous_iff_continuousAt.2 fun t => (hK t).continuousAt))).continuousOn)
  have hH : ∀ t ∈ Ico 0 T, HasDerivWithinAt H 0 (Ici t) t := by
    intro t ht
    have hE : HasDerivAt (fun t => exp (-2 * K t)) (exp (-2 * K t) * (-2 * κ' t)) t :=
      ((hK t).const_mul (-2)).exp
    have := (hW t ht).mul hE.hasDerivWithinAt
    rw [hκ'eq t (Ico_subset_Icc_self ht)] at this
    convert this using 1
    ring
  have hconst := constant_of_has_deriv_right_zero hHc hH
  have hK0 : K 0 = 0 := by simp [hKdef]
  intro t ht
  have hWt : W t = W 0 * exp (2 * K t) := by
    have h1 := hconst t ht
    simp only [hHdef, hK0, mul_zero, exp_zero, mul_one] at h1
    have : W t = W t * exp (-2 * K t) * exp (2 * K t) := by
      rw [mul_assoc, ← exp_add]; simp
    rw [this, h1]
  have hKle : K t ≤ -c * t := by
    have hint := intervalIntegral.integral_mono_on ht.1 (hκ'c.intervalIntegrable (μ := volume) 0 t)
      (continuous_const.intervalIntegrable (μ := volume) 0 t)
      (fun s hs => by
        have hs' : s ∈ Icc 0 T := ⟨hs.1, hs.2.trans ht.2⟩
        rw [hκ'eq s hs']; exact hκ s hs')
    simpa [hKdef, intervalIntegral.integral_const, smul_eq_mul, mul_comm] using hint
  refine ⟨by rw [hWt]; positivity, ?_⟩
  rw [hWt]
  exact mul_le_mul_of_nonneg_left (exp_le_exp.2 (by linarith)) hW0

/-- Norma `‖W_0‖_{L∞(B)}` (supremo essencial em `B`), como numero real. -/
def essSupOn (f : ℝ × ℝ → ℝ) (B : Set (ℝ × ℝ)) : ℝ :=
  (eLpNorm f ∞ (volume.restrict B)).toReal

/-- Tempo de condensacao `t_δ = (1/2c) ln(‖W_0‖_{L∞(B)}/δ)`. -/
def tDelta (c M δ : ℝ) : ℝ := 1 / (2 * c) * log (M / δ)

/-- **`thm:neckpinch_condensation`** (texto atual): sob as hipoteses pontuais em cada `p ∈ B`,
para todo `δ ∈ (0, ‖W_0‖_{L∞(B)})` com `t_δ ≤ T`, vale `W(t,p) ≤ δ` para quase todo `p ∈ B` e
todo `t ∈ [t_δ, T]`. A primeira parte (`0 ≤ W ≤ W_0 e^{-2ct}` em todo `p ∈ B`) e
`decay_pointwise`. -/
theorem neckpinch_condensation (W κ : ℝ → ℝ × ℝ → ℝ) (B : Set (ℝ × ℝ)) (T c : ℝ)
    (hT : 0 ≤ T) (hc : 0 < c) (hB : MeasurableSet B)
    (hmeas : AEStronglyMeasurable (W 0) (volume.restrict B))
    (hκc : ∀ p ∈ B, ContinuousOn (fun s => κ s p) (Icc 0 T))
    (hWc : ∀ p ∈ B, ContinuousOn (fun t => W t p) (Icc 0 T))
    (hW : ∀ p ∈ B, ∀ t ∈ Ico 0 T, HasDerivWithinAt (fun t => W t p) (2 * κ t p * W t p) (Ici t) t)
    (hκ : ∀ p ∈ B, ∀ s ∈ Icc 0 T, κ s p ≤ -c) (hW0 : ∀ p ∈ B, 0 ≤ W 0 p)
    {δ : ℝ} (hδ : 0 < δ) (hδM : δ < essSupOn (W 0) B) :
    ∀ᵐ p ∂(volume.restrict B), ∀ t ∈ Icc (tDelta c (essSupOn (W 0) B) δ) T, W t p ≤ δ := by
  set M := essSupOn (W 0) B with hMdef
  have hMpos : 0 < M := hδ.trans hδM
  have hfin : eLpNorm (W 0) ∞ (volume.restrict B) ≠ ⊤ := by
    intro h; simp [hMdef, essSupOn, h] at hMpos
  have htδ0 : 0 ≤ tDelta c M δ := by
    unfold tDelta
    have : 0 ≤ log (M / δ) := log_nonneg (by rw [le_div_iff₀ hδ]; linarith)
    positivity
  filter_upwards [ae_restrict_mem hB,
    ae_le_eLpNormEssSup (f := W 0) (μ := volume.restrict B)] with p hpB hp
  -- W_0(p) ≤ M
  have hWM : W 0 p ≤ M := by
    have h1 : (‖W 0 p‖ₑ).toReal ≤ (eLpNormEssSup (W 0) (volume.restrict B)).toReal := by
      rw [← eLpNorm_exponent_top hmeas] at hp ⊢
      exact ENNReal.toReal_mono hfin hp
    rw [toReal_enorm, ← eLpNorm_exponent_top hmeas] at h1
    exact (le_abs_self _).trans ((Real.norm_eq_abs _).symm ▸ h1)
  intro t ht
  have htI : t ∈ Icc 0 T := ⟨htδ0.trans ht.1, ht.2⟩
  have hdec := (decay_pointwise (fun t => W t p) (fun s => κ s p) T c hT (hκc p hpB) (hWc p hpB)
    (hW p hpB) (hκ p hpB) (hW0 p hpB) t htI).2
  calc W t p ≤ W 0 p * exp (-2 * c * t) := hdec
    _ ≤ M * exp (-2 * c * tDelta c M δ) := by
        apply mul_le_mul hWM (exp_le_exp.2 (by nlinarith [ht.1])) (exp_pos _).le hMpos.le
    _ = δ := by
        unfold tDelta
        rw [show -2 * c * (1 / (2 * c) * log (M / δ)) = -log (M / δ) by field_simp,
          exp_neg, exp_log (div_pos hMpos hδ)]
        field_simp

/-- Forma do livro, com a ressalva "(provided `t_δ ≤ T`)". A hipotese `_htδ` nao e usada: se
`t_δ > T` o intervalo `[t_δ, T]` e vazio e a conclusao e trivial. -/
theorem neckpinch_condensation_source (W κ : ℝ → ℝ × ℝ → ℝ) (B : Set (ℝ × ℝ)) (T c : ℝ)
    (hT : 0 ≤ T) (hc : 0 < c) (hB : MeasurableSet B)
    (hmeas : AEStronglyMeasurable (W 0) (volume.restrict B))
    (hκc : ∀ p ∈ B, ContinuousOn (fun s => κ s p) (Icc 0 T))
    (hWc : ∀ p ∈ B, ContinuousOn (fun t => W t p) (Icc 0 T))
    (hW : ∀ p ∈ B, ∀ t ∈ Ico 0 T, HasDerivWithinAt (fun t => W t p) (2 * κ t p * W t p) (Ici t) t)
    (hκ : ∀ p ∈ B, ∀ s ∈ Icc 0 T, κ s p ≤ -c) (hW0 : ∀ p ∈ B, 0 ≤ W 0 p)
    {δ : ℝ} (hδ : 0 < δ) (hδM : δ < essSupOn (W 0) B)
    (_htδ : tDelta c (essSupOn (W 0) B) δ ≤ T) :
    (∀ p ∈ B, ∀ t ∈ Icc 0 T, 0 ≤ W t p ∧ W t p ≤ W 0 p * exp (-2 * c * t)) ∧
    ∀ᵐ p ∂(volume.restrict B), ∀ t ∈ Icc (tDelta c (essSupOn (W 0) B) δ) T, W t p ≤ δ :=
  ⟨fun p hp => decay_pointwise (fun t => W t p) (fun s => κ s p) T c hT (hκc p hp) (hWc p hp)
      (hW p hp) (hκ p hp) (hW0 p hp),
    neckpinch_condensation W κ B T c hT hc hB hmeas hκc hWc hW hκ hW0 hδ hδM⟩

/-! ### Testemunhas e mutantes de 12.6 -/

/-- Testemunha pontual (hipoteses mordem, `κ` nao constante): `κ(t) = -1 - t`, `c = 1`, `T = 1`,
`W(t) = 3 e^{-2t - t^2}`. Conclusao: `0 ≤ W(1) ≤ 3 e^{-2}`, com `W(1) = 3e^{-3} < 3e^{-2}`. -/
theorem witness_pointwise :
    ∀ t ∈ Icc (0:ℝ) 1, 0 ≤ 3 * exp (-2 * t - t ^ 2) ∧
      3 * exp (-2 * t - t ^ 2) ≤ 3 * exp (-2 * 0 - 0 ^ 2) * exp (-2 * 1 * t) := by
  have := decay_pointwise (fun t => 3 * exp (-2 * t - t ^ 2)) (fun t => -1 - t) 1 1 zero_le_one
    (by fun_prop) (by fun_prop)
    (fun t _ => by
      have h : HasDerivAt (fun t => 3 * exp (-2 * t - t ^ 2))
          (3 * (exp (-2 * t - t ^ 2) * (-2 - 2 * t))) t := by
        have h1 : HasDerivAt (fun t : ℝ => -2 * t - t ^ 2) (-2 - 2 * t) t := by
          convert ((hasDerivAt_id' t).const_mul (-2)).sub (hasDerivAt_pow 2 t) using 1
          norm_num
        exact (h1.exp).const_mul 3
      convert h.hasDerivWithinAt using 1
      ring)
    (fun s hs => by linarith [hs.1]) (by positivity)
  simpa using this

/-- Mutante pontual 1 (sem `W_0 ≥ 0`): `0 ≤ W` falha para `W(t) = -e^{-2t}`, `κ ≡ -1`. -/
theorem mutant_no_nonneg_false :
    ¬ (∀ (W κ : ℝ → ℝ) (T c : ℝ), 0 ≤ T → ContinuousOn κ (Icc 0 T) → ContinuousOn W (Icc 0 T) →
        (∀ t ∈ Ico 0 T, HasDerivWithinAt W (2 * κ t * W t) (Ici t) t) →
        (∀ s ∈ Icc 0 T, κ s ≤ -c) → ∀ t ∈ Icc 0 T, 0 ≤ W t) := by
  intro h
  have := h (fun t => -exp (-2 * t)) (fun _ => -1) 1 1 zero_le_one (by fun_prop) (by fun_prop)
    (fun t _ => by
      have h1 : HasDerivAt (fun t => -exp (-2 * t)) (-(exp (-2 * t) * (-2 * 1))) t :=
        (((hasDerivAt_id t).const_mul (-2)).exp).neg
      convert h1.hasDerivWithinAt using 1; ring)
    (fun _ _ => le_rfl) 0 ⟨le_rfl, zero_le_one⟩
  simp at this
  linarith

/-- Mutante pontual 2 (taxa `3c` em vez de `2c`): falso para `κ ≡ -1`, `W = e^{-2t}`. -/
theorem mutant_rate_false :
    ¬ (∀ (W κ : ℝ → ℝ) (T c : ℝ), 0 ≤ T → ContinuousOn κ (Icc 0 T) → ContinuousOn W (Icc 0 T) →
        (∀ t ∈ Ico 0 T, HasDerivWithinAt W (2 * κ t * W t) (Ici t) t) →
        (∀ s ∈ Icc 0 T, κ s ≤ -c) → 0 ≤ W 0 →
        ∀ t ∈ Icc 0 T, W t ≤ W 0 * exp (-3 * c * t)) := by
  intro h
  have := h (fun t => exp (-2 * t)) (fun _ => -1) 1 1 zero_le_one (by fun_prop) (by fun_prop)
    (fun t _ => by
      have h1 : HasDerivAt (fun t => exp (-2 * t)) (exp (-2 * t) * (-2 * 1)) t :=
        ((hasDerivAt_id t).const_mul (-2)).exp
      convert h1.hasDerivWithinAt using 1; ring)
    (fun _ _ => le_rfl) (exp_pos _).le 1 ⟨zero_le_one, le_rfl⟩
  simp at this
  linarith [exp_lt_exp.2 (show (-3:ℝ) < -2 by norm_num)]

/-- O quadrado `B₀ = [0,1]^2`. -/
def B01 : Set (ℝ × ℝ) := Icc 0 1 ×ˢ Icc 0 1

theorem volume_B01 : (volume : Measure (ℝ × ℝ)) B01 = 1 := by
  rw [B01, Measure.volume_eq_prod, Measure.prod_prod]
  simp [Real.volume_Icc]

theorem measurableSet_B01 : MeasurableSet B01 := measurableSet_Icc.prod measurableSet_Icc

/-- `‖f‖_{L∞(B₀)} = 1` para toda `f` igual a `1` q.t.p. em `B₀`. -/
theorem essSupOn_eq_one {f : ℝ × ℝ → ℝ} (hf : f =ᵐ[volume.restrict B01] fun _ => 1) :
    essSupOn f B01 = 1 := by
  have hμ : (volume.restrict B01 : Measure (ℝ × ℝ)) ≠ 0 := by
    rw [Ne, Measure.restrict_eq_zero, volume_B01]; exact one_ne_zero
  rw [essSupOn, eLpNorm_congr_ae hf, eLpNorm_exponent_top aestronglyMeasurable_const,
    eLpNormEssSup_const _ hμ]
  simp

/-- Hipoteses pontuais para `W(t,p) = f(p) e^{-2t}`, `κ ≡ -1`, em `[0,1]`. -/
theorem expData_hyps (f : ℝ × ℝ → ℝ) (p : ℝ × ℝ) :
    ContinuousOn (fun _ : ℝ => (-1 : ℝ)) (Icc 0 1) ∧
    ContinuousOn (fun t => f p * exp (-2 * t)) (Icc 0 1) ∧
    ∀ t ∈ Ico (0:ℝ) 1, HasDerivWithinAt (fun t => f p * exp (-2 * t))
      (2 * (-1) * (f p * exp (-2 * t))) (Ici t) t := by
  refine ⟨continuousOn_const, by fun_prop, fun t _ => ?_⟩
  have h1 : HasDerivAt (fun t => f p * exp (-2 * t)) (f p * (exp (-2 * t) * (-2 * 1))) t :=
    (((hasDerivAt_id t).const_mul (-2)).exp).const_mul (f p)
  convert h1.hasDerivWithinAt using 1; ring

/-- `t_δ` para `c = 1`, `‖W_0‖ = 1`, `δ = 1/2`: `t_δ = (log 2)/2 ∈ (0,1)`. -/
theorem tDelta_half : tDelta 1 1 (1 / 2) = log 2 / 2 ∧ 0 < log 2 / 2 ∧ log 2 / 2 ≤ 1 := by
  refine ⟨by unfold tDelta; norm_num; ring, by positivity, ?_⟩
  have := Real.log_le_sub_one_of_pos (show (0:ℝ) < 2 by norm_num)
  linarith

/-- Testemunha nao degenerada de `neckpinch_condensation`: `W(t,p) = e^{-2t}`, `κ ≡ -1`, `c = 1`,
`T = 1`, `B = [0,1]^2`, `δ = 1/2`. As hipoteses valem (`‖W_0‖ = 1`), a conclusao vale em
`[t_δ, 1]` com `t_δ = (log 2)/2 > 0`, e FALHA em `t = 0` (`W(0) = 1 > 1/2`): o tempo `t_δ` morde. -/
theorem witness_neckpinch :
    essSupOn (fun _ => exp (-2 * 0)) B01 = 1 ∧
    (∀ᵐ _p ∂(volume.restrict B01), ∀ t ∈ Icc (tDelta 1 (essSupOn (fun _ => exp (-2 * 0)) B01)
      (1 / 2)) 1, exp (-2 * t) ≤ 1 / 2) ∧
    0 < tDelta 1 1 (1 / 2) ∧ ¬ (exp (-2 * (0:ℝ)) ≤ 1 / 2) := by
  have hM : essSupOn (fun _ => exp (-2 * 0)) B01 = 1 :=
    essSupOn_eq_one (Eventually.of_forall (fun _ => by simp))
  refine ⟨hM, ?_, by rw [tDelta_half.1]; exact tDelta_half.2.1, by simp; norm_num⟩
  have h := neckpinch_condensation (fun t _ => 1 * exp (-2 * t)) (fun _ _ => -1) B01 1 1
    zero_le_one one_pos measurableSet_B01 aestronglyMeasurable_const
    (fun p _ => (expData_hyps (fun _ => 1) p).1) (fun p _ => (expData_hyps (fun _ => 1) p).2.1)
    (fun p _ => (expData_hyps (fun _ => 1) p).2.2) (fun _ _ _ _ => le_rfl)
    (fun _ _ => by positivity) (δ := 1 / 2) (by norm_num) (by simp at hM ⊢; rw [hM]; norm_num)
  simpa using h

/-- Mutante (S2: "para todo `(x,y) ∈ B`" em vez de "quase todo"): FALSO. Contraexemplo:
`W_0 = 1` em `B₀ = [0,1]^2` exceto `W_0(0,0) = 2`; o supremo essencial e `1`, `δ = 1/2`,
`t_δ = (log 2)/2`, mas `W(t_δ,(0,0)) = 2 e^{-log 2} = 1 > 1/2`. -/
theorem mutant_everywhere_false :
    ¬ (∀ (W κ : ℝ → ℝ × ℝ → ℝ) (B : Set (ℝ × ℝ)) (T c : ℝ), 0 ≤ T → 0 < c → MeasurableSet B →
        AEStronglyMeasurable (W 0) (volume.restrict B) →
        (∀ p ∈ B, ContinuousOn (fun s => κ s p) (Icc 0 T)) →
        (∀ p ∈ B, ContinuousOn (fun t => W t p) (Icc 0 T)) →
        (∀ p ∈ B, ∀ t ∈ Ico 0 T,
          HasDerivWithinAt (fun t => W t p) (2 * κ t p * W t p) (Ici t) t) →
        (∀ p ∈ B, ∀ s ∈ Icc 0 T, κ s p ≤ -c) → (∀ p ∈ B, 0 ≤ W 0 p) →
        ∀ δ : ℝ, 0 < δ → δ < essSupOn (W 0) B →
        ∀ p ∈ B, ∀ t ∈ Icc (tDelta c (essSupOn (W 0) B) δ) T, W t p ≤ δ) := by
  intro h
  set f : ℝ × ℝ → ℝ := fun p => if p = ((0:ℝ), (0:ℝ)) then 2 else 1 with hfdef
  have hf_meas : Measurable f :=
    Measurable.ite (measurableSet_singleton _) measurable_const measurable_const
  have h0 : (volume : Measure (ℝ × ℝ)) {((0:ℝ), (0:ℝ))} = 0 := by
    rw [← Set.singleton_prod_singleton, Measure.volume_eq_prod, Measure.prod_prod]; simp
  have hae : (fun p => f p * exp (-2 * 0)) =ᵐ[volume.restrict B01] fun _ => 1 := by
    apply ae_restrict_of_ae
    have : ∀ᵐ p ∂(volume : Measure (ℝ × ℝ)), p ≠ ((0:ℝ), (0:ℝ)) := by
      rw [ae_iff]; simp [h0]
    filter_upwards [this] with p hp
    simp [hfdef, hp]
  have hM : essSupOn (fun p => f p * exp (-2 * 0)) B01 = 1 := essSupOn_eq_one hae
  have h0B : ((0:ℝ), (0:ℝ)) ∈ B01 := ⟨⟨le_rfl, zero_le_one⟩, ⟨le_rfl, zero_le_one⟩⟩
  have := h (fun t p => f p * exp (-2 * t)) (fun _ _ => -1) B01 1 1 zero_le_one one_pos
    measurableSet_B01 (hf_meas.mul measurable_const).aestronglyMeasurable
    (fun p _ => (expData_hyps f p).1) (fun p _ => (expData_hyps f p).2.1)
    (fun p _ => (expData_hyps f p).2.2) (fun _ _ _ _ => le_rfl)
    (fun p _ => by simp only [hfdef]; split_ifs <;> positivity)
    (1 / 2) (by norm_num) (by rw [hM]; norm_num) _ h0B (log 2 / 2)
    (by rw [hM, tDelta_half.1]; exact ⟨le_rfl, tDelta_half.2.2⟩)
  simp only [hfdef, ite_true] at this
  rw [show -2 * (log 2 / 2) = -log 2 by ring, exp_neg, exp_log two_pos] at this
  norm_num at this

end LeanReal.Chap12Spectral

#print axioms LeanReal.Chap12Spectral.integral_scaling
#print axioms LeanReal.Chap12Spectral.hasDerivAt_logP
#print axioms LeanReal.Chap12Spectral.specDim_eq
#print axioms LeanReal.Chap12Spectral.specDim_book_cases
#print axioms LeanReal.Chap12Spectral.witness_heatDiag
#print axioms LeanReal.Chap12Spectral.mutant_half_false
#print axioms LeanReal.Chap12Spectral.mutant_no_alpha_false
#print axioms LeanReal.Chap12Spectral.gram_simpleRoot
#print axioms LeanReal.Chap12Spectral.sum_sq_eq_cartan
#print axioms LeanReal.Chap12Spectral.simpleRoot_comb_sum_zero
#print axioms LeanReal.Chap12Spectral.barycentric_line
#print axioms LeanReal.Chap12Spectral.witness_gram
#print axioms LeanReal.Chap12Spectral.witness_barycentric
#print axioms LeanReal.Chap12Spectral.mutant_linear_term_false
#print axioms LeanReal.Chap12Spectral.mutant_gram_identity_false
#print axioms LeanReal.Chap12Spectral.decay_pointwise
#print axioms LeanReal.Chap12Spectral.neckpinch_condensation
#print axioms LeanReal.Chap12Spectral.neckpinch_condensation_source
#print axioms LeanReal.Chap12Spectral.witness_pointwise
#print axioms LeanReal.Chap12Spectral.mutant_no_nonneg_false
#print axioms LeanReal.Chap12Spectral.mutant_rate_false
#print axioms LeanReal.Chap12Spectral.witness_neckpinch
#print axioms LeanReal.Chap12Spectral.mutant_everywhere_false
