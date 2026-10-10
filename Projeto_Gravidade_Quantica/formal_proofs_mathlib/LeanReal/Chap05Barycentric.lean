import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Analysis.Complex.Basic
import Mathlib.Tactic

/-!
# Capitulo 5: `thm:barycentric_ratio` e a Prop. "Inversion" (parte linear)
(itens 1 e 4 do Lote A1, `PLANO_LIVRO_A.md`)

Fonte: `unified_quantum_gravity_book/chap05_interdimensional_transforms_barnes_lie.tex`.

## Parte A: `def:induced_barycentric_map` e `thm:barycentric_ratio`

Enunciado congelado. `π : {1..m} ↠ {1..n}`, fibras `G_k = π⁻¹(k)`,
`Φ_α(c)_k = (α ∑_{j∈G_k} c_j + |G_k|)/(α+m)`, `dist_Δ(c,c') = ½‖c-c'‖₁`. Para
`c₁, c₂ ∈ Δ^{m-1}`: `dist_Δ(Φc₁, Φc₂) ≤ α/(α+m) · dist_Δ(c₁,c₂)`; igualdade quando `c₁-c₂` nao
troca de sinal em nenhuma fibra (em particular se `π = id`); a razao e `≤ 1 - m/α + O(α^{-2})`;
para `m = 4 → n = 2`, `G₁ = {1,2}`, `G₂ = {3,4}`, `c₁ = (½,0,½,0)`, `c₂ = (0,½,0,½)`, a razao e
`0`, e nao ha cota inferior (bi-Lipschitz). O livro supoe `α > 0`.

Reducao: nenhuma; e o enunciado completo em dimensao finita. Notas de fidelidade:
* a cota vale para TODOS `c₁, c₂ ∈ ℝ^m` (nao so no simplexo) e para `α ≥ 0`; a sobrejetividade
  de `π` nao e usada na cota nem na inclusao `Φ(Δ^{m-1}) ⊂ Δ^{n-1}`; foi omitida;
* "`O(α^{-2})`" e dado com constante explicita: `α/(α+m) ≤ 1 - m/α + m²/α²` para `α > 0`.

## Parte B: Prop. "Inversion", parte linear

Enunciado congelado. `P ∈ ℝ^{n×m}` de posto `n`, `P⁺ = Pᵀ(PPᵀ)⁻¹`, `θ = ran P⁺`,
`g_θ(z) = h(P⁺z)`. Para `x ∈ θ`: `h(x) = g_θ(Px)`. Alem disso, se `K̂_α(k) ≠ 0` para todo `k`,
`ĥ(k) = K̂_α(-k) f̂(k)` determina `f̂ = ĥ/K̂_α(-·)`.

Reducao: a parte linear e completa (`PP⁺ = I`, `P⁺P` idempotente e simetrica,
`ran P⁺ = ran Pᵀ`, `P⁺Px = x` em `θ`, e `h(x) = g_θ(Px)`). O teorema da convolucao NAO e
formalizado; a deconvolucao entra como algebra pontual: `hK` (nao anulamento) e uma hipotese
EXPLICITA. `mutant_no_nonvanishing_false` mostra que sem ela a recuperacao falha.
Sobre essa hipotese para o Beta-kernel, ver o relatorio `RODADA_LIVRO_A1_2026-10-10.md`.
-/

noncomputable section

namespace LeanReal.Chap05Barycentric

open Finset

/-! ## Parte A -/

/-- Mapa baricentrico induzido `Φ_α` (`def:induced_barycentric_map`, eq. `eq:induced_map`). -/
def Phi {m n : ℕ} (α : ℝ) (π : Fin m → Fin n) (c : Fin m → ℝ) (k : Fin n) : ℝ :=
  (α * ∑ j ∈ univ.filter (fun j => π j = k), c j + ((univ.filter (fun j => π j = k)).card : ℝ))
    / (α + m)

/-- Metrica `dist_Δ(c,c') = ½‖c-c'‖₁`. -/
def distΔ {m : ℕ} (c c' : Fin m → ℝ) : ℝ := (1 / 2) * ∑ j, |c j - c' j|

/-- O simplexo `Δ^{m-1}`. -/
def InSimplex {m : ℕ} (c : Fin m → ℝ) : Prop := (∀ j, 0 ≤ c j) ∧ ∑ j, c j = 1

theorem Phi_sub {m n : ℕ} (α : ℝ) (π : Fin m → Fin n) (c₁ c₂ : Fin m → ℝ) (k : Fin n) :
    Phi α π c₁ k - Phi α π c₂ k =
      α / (α + m) * ∑ j ∈ univ.filter (fun j => π j = k), (c₁ j - c₂ j) := by
  unfold Phi
  rw [Finset.sum_sub_distrib]
  ring

/-- `Φ_α` leva o simplexo no simplexo (`def:induced_barycentric_map`, ultima frase), para
`α ≥ 0` e `α + m > 0`. -/
theorem Phi_mem_simplex {m n : ℕ} (α : ℝ) (hα : 0 ≤ α) (hαm : 0 < α + m) (π : Fin m → Fin n)
    (c : Fin m → ℝ) (hc : InSimplex c) : InSimplex (Phi α π c) := by
  refine ⟨fun k => ?_, ?_⟩
  · unfold Phi
    have : 0 ≤ ∑ j ∈ univ.filter (fun j => π j = k), c j := Finset.sum_nonneg fun j _ => hc.1 j
    positivity
  · unfold Phi
    rw [← Finset.sum_div, Finset.sum_add_distrib, ← Finset.mul_sum,
      Finset.sum_fiberwise univ π c, hc.2]
    have hcard : ∑ k : Fin n, ((univ.filter (fun j => π j = k)).card : ℝ) = m := by
      have := Finset.sum_fiberwise (univ : Finset (Fin m)) π (fun _ => (1 : ℝ))
      simpa using this
    rw [hcard, mul_one, div_self hαm.ne']

/-- **`thm:barycentric_ratio`, eq. `eq:sharp_contraction`**: para `α ≥ 0` e quaisquer
`c₁, c₂ ∈ ℝ^m` (em particular no simplexo), `dist_Δ(Φc₁,Φc₂) ≤ α/(α+m) · dist_Δ(c₁,c₂)`. -/
theorem lipschitz {m n : ℕ} (α : ℝ) (hα : 0 ≤ α) (π : Fin m → Fin n) (c₁ c₂ : Fin m → ℝ) :
    distΔ (Phi α π c₁) (Phi α π c₂) ≤ α / (α + m) * distΔ c₁ c₂ := by
  have hr : 0 ≤ α / (α + m) := by positivity
  unfold distΔ
  simp_rw [Phi_sub, abs_mul, abs_of_nonneg hr]
  rw [← Finset.mul_sum, ← Finset.sum_fiberwise univ π (fun j => |c₁ j - c₂ j|)]
  have : ∑ k, |∑ j ∈ univ.filter (fun j => π j = k), (c₁ j - c₂ j)| ≤
      ∑ k, ∑ j ∈ univ.filter (fun j => π j = k), |c₁ j - c₂ j| :=
    Finset.sum_le_sum fun k _ => Finset.abs_sum_le_sum_abs _ _
  nlinarith

/-- **`thm:barycentric_ratio`, nitidez**: se `c₁ - c₂` nao troca de sinal em nenhuma fibra,
vale a igualdade. -/
theorem lipschitz_eq_of_no_sign_change {m n : ℕ} (α : ℝ) (hα : 0 ≤ α) (π : Fin m → Fin n)
    (c₁ c₂ : Fin m → ℝ)
    (hsign : ∀ k, (∀ j, π j = k → 0 ≤ c₁ j - c₂ j) ∨ (∀ j, π j = k → c₁ j - c₂ j ≤ 0)) :
    distΔ (Phi α π c₁) (Phi α π c₂) = α / (α + m) * distΔ c₁ c₂ := by
  have hr : 0 ≤ α / (α + m) := by positivity
  unfold distΔ
  simp_rw [Phi_sub, abs_mul, abs_of_nonneg hr]
  rw [← Finset.mul_sum, ← Finset.sum_fiberwise univ π (fun j => |c₁ j - c₂ j|)]
  have : ∀ k, |∑ j ∈ univ.filter (fun j => π j = k), (c₁ j - c₂ j)| =
      ∑ j ∈ univ.filter (fun j => π j = k), |c₁ j - c₂ j| := by
    intro k
    rcases hsign k with h | h
    · rw [abs_of_nonneg (Finset.sum_nonneg fun j hj => h j (Finset.mem_filter.mp hj).2)]
      exact Finset.sum_congr rfl fun j hj => (abs_of_nonneg (h j (Finset.mem_filter.mp hj).2)).symm
    · rw [abs_of_nonpos (Finset.sum_nonpos fun j hj => h j (Finset.mem_filter.mp hj).2),
        ← Finset.sum_neg_distrib]
      exact Finset.sum_congr rfl fun j hj => (abs_of_nonpos (h j (Finset.mem_filter.mp hj).2)).symm
  simp_rw [this]
  ring

/-- **`thm:barycentric_ratio`, caso `π` injetivo (por exemplo `π = id`, `n = m`)**: igualdade. -/
theorem lipschitz_eq_of_injective {m n : ℕ} (α : ℝ) (hα : 0 ≤ α) (π : Fin m → Fin n)
    (hπ : Function.Injective π) (c₁ c₂ : Fin m → ℝ) :
    distΔ (Phi α π c₁) (Phi α π c₂) = α / (α + m) * distΔ c₁ c₂ := by
  refine lipschitz_eq_of_no_sign_change α hα π c₁ c₂ fun k => ?_
  by_cases hk : ∃ j, π j = k
  · obtain ⟨j₀, hj₀⟩ := hk
    rcases le_total 0 (c₁ j₀ - c₂ j₀) with h | h
    · left; intro j hj; rwa [hπ (hj.trans hj₀.symm)]
    · right; intro j hj; rwa [hπ (hj.trans hj₀.symm)]
  · push Not at hk
    left; intro j hj; exact absurd hj (hk j)

/-- **`thm:barycentric_ratio`, expansao em `α → ∞`**, com constante explicita:
`1 - m/α ≤ α/(α+m) ≤ 1 - m/α + m²/α²` para `α > 0`. -/
theorem ratio_expansion (m : ℕ) (α : ℝ) (hα : 0 < α) :
    1 - m / α ≤ α / (α + m) ∧ α / (α + m) ≤ 1 - m / α + (m : ℝ) ^ 2 / α ^ 2 := by
  have hm : (0 : ℝ) ≤ m := Nat.cast_nonneg m
  have hαm : 0 < α + m := by linarith
  have key : α / (α + m) = 1 - m / α + (m : ℝ) ^ 2 / (α * (α + m)) := by
    field_simp; ring
  rw [key]
  constructor
  · have : 0 ≤ (m : ℝ) ^ 2 / (α * (α + m)) := by positivity
    linarith
  · have : (m : ℝ) ^ 2 / (α * (α + m)) ≤ (m : ℝ) ^ 2 / α ^ 2 := by
      apply div_le_div_of_nonneg_left (by positivity) (by positivity)
      nlinarith
    linarith

/-! ### O contraexemplo do livro (`m = 4 → n = 2`) -/

/-- Agrupamento `G₁ = {1,2}`, `G₂ = {3,4}` (indices de `Fin` a partir de `0`). -/
def π42 : Fin 4 → Fin 2 := ![0, 0, 1, 1]
def c₁ex : Fin 4 → ℝ := ![1 / 2, 0, 1 / 2, 0]
def c₂ex : Fin 4 → ℝ := ![0, 1 / 2, 0, 1 / 2]

theorem c₁ex_mem : InSimplex c₁ex := by
  refine ⟨fun j => ?_, ?_⟩
  · fin_cases j <;> norm_num [c₁ex]
  · simp [c₁ex, Fin.sum_univ_four]; norm_num

theorem c₂ex_mem : InSimplex c₂ex := by
  refine ⟨fun j => ?_, ?_⟩
  · fin_cases j <;> norm_num [c₂ex]
  · simp [c₂ex, Fin.sum_univ_four]; norm_num

theorem dist_ex : distΔ c₁ex c₂ex = 1 := by
  simp [distΔ, c₁ex, c₂ex, Fin.sum_univ_four]; norm_num

/-- **Contraexemplo do livro**: `Φ_α(c₁) = Φ_α(c₂)` para todo `α`, com `dist_Δ(c₁,c₂) = 1`. -/
theorem Phi_ex_eq (α : ℝ) : Phi α π42 c₁ex = Phi α π42 c₂ex := by
  funext k
  have : Phi α π42 c₁ex k - Phi α π42 c₂ex k = 0 := by
    rw [Phi_sub, Finset.sum_filter]
    fin_cases k <;> simp [Fin.sum_univ_four, π42, c₁ex, c₂ex]
  linarith

/-- **Sem cota inferior (bi-Lipschitz)**: nao existe `L > 0` com
`L·dist_Δ(c₁,c₂) ≤ dist_Δ(Φc₁,Φc₂)` no simplexo, para o agrupamento `4 → 2`, qualquer `α`. -/
theorem no_lower_bound (α : ℝ) :
    ¬ ∃ L > 0, ∀ c c' : Fin 4 → ℝ, InSimplex c → InSimplex c' →
      L * distΔ c c' ≤ distΔ (Phi α π42 c) (Phi α π42 c') := by
  rintro ⟨L, hL, h⟩
  have := h c₁ex c₂ex c₁ex_mem c₂ex_mem
  rw [Phi_ex_eq, dist_ex] at this
  simp [distΔ] at this
  linarith

/-! ### Testemunhas nao degeneradas (`m = 3 → n = 2`, `α = 1`, `G₁ = {1,2}`, `G₂ = {3}`) -/

def π32 : Fin 3 → Fin 2 := ![0, 0, 1]

/-- Igualdade com fibra nao trivial e sem troca de sinal: `c₁ = (½,½,0)`, `c₂ = (0,0,1)`;
`dist_Δ(Φc₁,Φc₂) = ¼ = (1/4)·1`. -/
example : distΔ (Phi 1 π32 ![1 / 2, 1 / 2, 0]) (Phi 1 π32 ![0, 0, 1]) = 1 / 4 ∧
    distΔ (![1 / 2, 1 / 2, 0] : Fin 3 → ℝ) ![0, 0, 1] = 1 := by
  constructor
  · rw [lipschitz_eq_of_no_sign_change 1 zero_le_one π32 _ _ ?_]
    · simp [distΔ, Fin.sum_univ_three]; norm_num
    · intro k; fin_cases k
      · left; intro j hj; fin_cases j <;> simp_all [π32]
      · right; intro j hj; fin_cases j <;> simp_all [π32]
  · simp [distΔ, Fin.sum_univ_three]; norm_num

/-- Desigualdade estrita (cancelamento na fibra `G₁`): `c₁ = (1,0,0)`, `c₂ = (0,1,0)`;
`dist_Δ(Φc₁,Φc₂) = 0 < ¼ = (1/4)·dist_Δ(c₁,c₂)`. A conclusao nao e automatica. -/
example : distΔ (Phi 1 π32 ![1, 0, 0]) (Phi 1 π32 ![0, 1, 0]) = 0 ∧
    (1 : ℝ) / (1 + (3 : ℕ)) * distΔ (![1, 0, 0] : Fin 3 → ℝ) ![0, 1, 0] = 1 / 4 := by
  constructor
  · have h : Phi 1 π32 ![1, 0, 0] = Phi 1 π32 ![0, 1, 0] := by
      funext k
      have : Phi 1 π32 ![1, 0, 0] k - Phi 1 π32 ![0, 1, 0] k = 0 := by
        rw [Phi_sub, Finset.sum_filter]
        fin_cases k <;> simp [Fin.sum_univ_three, π32]
      linarith
    rw [h]; simp [distΔ]
  · simp [distΔ, Fin.sum_univ_three]; norm_num

/-! ### Mutantes provados FALSOS -/

/-- Mutante 1 (plano): constante `α/(α+m+1)` no lugar de `α/(α+m)`. Falso: `m = n = 2`,
`π = id`, `α = 1`, `c₁ = (1,0)`, `c₂ = (0,1)`: `⅓ > ¼`. -/
theorem mutant_constant_false :
    ¬ ∀ (α : ℝ), 0 < α → ∀ c c' : Fin 2 → ℝ, InSimplex c → InSimplex c' →
      distΔ (Phi α id c) (Phi α id c') ≤ α / (α + 2 + 1) * distΔ c c' := by
  intro h
  have hc : InSimplex (![1, 0] : Fin 2 → ℝ) := ⟨fun j => by fin_cases j <;> simp, by simp⟩
  have hc' : InSimplex (![0, 1] : Fin 2 → ℝ) := ⟨fun j => by fin_cases j <;> simp, by simp⟩
  have := h 1 one_pos _ _ hc hc'
  rw [lipschitz_eq_of_injective 1 zero_le_one id Function.injective_id] at this
  simp [distΔ] at this
  norm_num at this

/-- Mutante 2: "igualdade sempre" (razao identicamente `α/(α+m)`). Falso pelo contraexemplo
`4 → 2` com `α = 1`. -/
theorem mutant_always_equal_false :
    ¬ ∀ c c' : Fin 4 → ℝ, InSimplex c → InSimplex c' →
      distΔ (Phi 1 π42 c) (Phi 1 π42 c') = 1 / (1 + (4 : ℕ)) * distΔ c c' := by
  intro h
  have := h c₁ex c₂ex c₁ex_mem c₂ex_mem
  rw [Phi_ex_eq, dist_ex] at this
  simp [distΔ] at this
  norm_num at this

/-! ## Parte B: Prop. "Inversion", parte linear -/

open Matrix

variable {n m : ℕ}

/-- Pseudoinversa de Moore–Penrose para posto linha cheio: `P⁺ = Pᵀ(PPᵀ)⁻¹`. -/
def pinv (P : Matrix (Fin n) (Fin m) ℝ) : Matrix (Fin m) (Fin n) ℝ := Pᵀ * (P * Pᵀ)⁻¹

/-- `PP⁺ = I` (hipotese `hP`: `PPᵀ` invertivel, isto e, posto `P = n`). -/
theorem mul_pinv (P : Matrix (Fin n) (Fin m) ℝ) (hP : IsUnit (P * Pᵀ)) : P * pinv P = 1 := by
  unfold pinv
  rw [← Matrix.mul_assoc]
  exact Matrix.mul_nonsing_inv _ ((Matrix.isUnit_iff_isUnit_det _).mp hP)

/-- `P⁺P` e idempotente. -/
theorem pinv_mul_idem (P : Matrix (Fin n) (Fin m) ℝ) (hP : IsUnit (P * Pᵀ)) :
    (pinv P * P) * (pinv P * P) = pinv P * P := by
  rw [Matrix.mul_assoc, ← Matrix.mul_assoc P, mul_pinv P hP, Matrix.one_mul]

/-- `P⁺P` e simetrica: `P⁺P` e a projecao ortogonal sobre `θ`. -/
theorem pinv_mul_symm (P : Matrix (Fin n) (Fin m) ℝ) :
    (pinv P * P)ᵀ = pinv P * P := by
  unfold pinv
  rw [Matrix.transpose_mul, Matrix.transpose_mul, Matrix.transpose_transpose,
    Matrix.transpose_nonsing_inv, Matrix.transpose_mul, Matrix.transpose_transpose,
    Matrix.mul_assoc]

/-- `ran P⁺ ⊂ ran Pᵀ`. -/
theorem range_pinv_sub (P : Matrix (Fin n) (Fin m) ℝ) (z : Fin n → ℝ) :
    ∃ y, pinv P *ᵥ z = Pᵀ *ᵥ y :=
  ⟨(P * Pᵀ)⁻¹ *ᵥ z, by unfold pinv; rw [Matrix.mulVec_mulVec]⟩

/-- `ran Pᵀ ⊂ ran P⁺` (com `hP`); junto com o anterior, `θ = ran P⁺ = ran Pᵀ`. -/
theorem range_transpose_sub (P : Matrix (Fin n) (Fin m) ℝ) (hP : IsUnit (P * Pᵀ))
    (y : Fin n → ℝ) : ∃ z, Pᵀ *ᵥ y = pinv P *ᵥ z := by
  refine ⟨(P * Pᵀ) *ᵥ y, ?_⟩
  unfold pinv
  rw [Matrix.mulVec_mulVec, Matrix.mul_assoc, Matrix.nonsing_inv_mul _
    ((Matrix.isUnit_iff_isUnit_det _).mp hP), Matrix.mul_one]

/-- `P⁺Px = x` para `x ∈ θ = ran P⁺`. -/
theorem pinv_mul_apply_of_mem (P : Matrix (Fin n) (Fin m) ℝ) (hP : IsUnit (P * Pᵀ))
    (z : Fin n → ℝ) : pinv P *ᵥ (P *ᵥ (pinv P *ᵥ z)) = pinv P *ᵥ z := by
  rw [Matrix.mulVec_mulVec, Matrix.mulVec_mulVec, Matrix.mul_assoc, mul_pinv P hP, Matrix.mul_one]

/-- **Prop. "Inversion", primeira afirmacao**: para `x ∈ θ = ran P⁺` e qualquer campo `h`, com
`g_θ(z) := h(P⁺z)` (Definicao `def:radon_beta`), vale `h(x) = g_θ(Px)`. -/
theorem inversion_restriction (P : Matrix (Fin n) (Fin m) ℝ) (hP : IsUnit (P * Pᵀ))
    (h : (Fin m → ℝ) → ℂ) (x : Fin m → ℝ) (hx : ∃ z, x = pinv P *ᵥ z) :
    h x = (fun z => h (pinv P *ᵥ z)) (P *ᵥ x) := by
  obtain ⟨z, rfl⟩ := hx
  simp only [pinv_mul_apply_of_mem P hP z]

/-- **Prop. "Inversion", deconvolucao (algebra pontual)**: se `ĥ(k) = K̂(-k) f̂(k)` e
`K̂(-k) ≠ 0` para todo `k` (hipotese `hK`, a do livro), entao `f̂ = ĥ/K̂(-·)`. Aqui `Kr k`
representa `K̂_α(-k)`; o teorema da convolucao nao e formalizado. -/
theorem deconvolution {ι : Type*} (Kr fhat hhat : ι → ℂ) (hK : ∀ k, Kr k ≠ 0)
    (hconv : ∀ k, hhat k = Kr k * fhat k) : fhat = fun k => hhat k / Kr k := by
  funext k
  rw [hconv k, mul_div_cancel_left₀ _ (hK k)]

/-! ### Testemunha nao degenerada: `n = 1`, `m = 2`, `P = (1 1)` -/

def P12 : Matrix (Fin 1) (Fin 2) ℝ := !![1, 1]

theorem P12_PPt : P12 * P12ᵀ = !![2] := by
  ext i j; fin_cases i; fin_cases j
  simp [P12, Matrix.mul_apply, Fin.sum_univ_two]; norm_num

theorem P12_unit : IsUnit (P12 * P12ᵀ) := by
  rw [Matrix.isUnit_iff_isUnit_det, P12_PPt, Matrix.det_unique]
  exact isUnit_iff_ne_zero.mpr (by norm_num)

theorem pinv_P12 : pinv P12 = !![1 / 2; 1 / 2] := by
  have hinv : (P12 * P12ᵀ)⁻¹ = !![1 / 2] := by
    rw [P12_PPt]
    apply Matrix.inv_eq_left_inv
    ext i j; fin_cases i; fin_cases j; simp
  unfold pinv; rw [hinv]
  ext i j; fin_cases i <;> fin_cases j <;> simp [P12, Matrix.mul_apply]

/-- `x = (3,3) ∈ θ` e recuperado, e `P⁺P ≠ I` (a projecao nao e trivial: `P⁺P(1,0) = (½,½)`). -/
example : (P12 *ᵥ ![3, 3] = ![6]) ∧ pinv P12 *ᵥ ![6] = ![3, 3] ∧
    pinv P12 *ᵥ (P12 *ᵥ ![1, 0]) = ![1 / 2, 1 / 2] := by
  rw [pinv_P12]
  refine ⟨?_, ?_, ?_⟩
  · ext i; fin_cases i; simp [P12, Matrix.mulVec, dotProduct, Fin.sum_univ_two]; norm_num
  · ext i; fin_cases i <;> simp [Matrix.mulVec, dotProduct] <;> norm_num
  · ext i; fin_cases i <;> simp [P12, Matrix.mulVec, dotProduct, Fin.sum_univ_two]

/-- A afirmacao `h(x) = g_θ(Px)` instanciada em `x = (3,3)`, `h(x) = x₁`. -/
example : ∃ z, (![3, 3] : Fin 2 → ℝ) = pinv P12 *ᵥ z ∧
    (fun x : Fin 2 → ℝ => (x 0 : ℂ)) ![3, 3] =
      (fun z => (fun x : Fin 2 → ℝ => (x 0 : ℂ)) (pinv P12 *ᵥ z)) (P12 *ᵥ ![3, 3]) := by
  have hz : (![3, 3] : Fin 2 → ℝ) = pinv P12 *ᵥ ![6] := by
    rw [pinv_P12]; ext i; fin_cases i <;> simp [Matrix.mulVec, dotProduct] <;> norm_num
  exact ⟨![6], hz, inversion_restriction P12 P12_unit (fun x => (x 0 : ℂ)) _ ⟨_, hz⟩⟩

/-! ### Mutantes provados FALSOS (Parte B) -/

/-- Mutante 3: "`P⁺Px = x` para todo `x`" (sem `x ∈ θ`). Falso para `P = (1 1)`, `x = (1,0)`. -/
theorem mutant_all_x_false :
    ¬ ∀ x : Fin 2 → ℝ, pinv P12 *ᵥ (P12 *ᵥ x) = x := by
  intro h
  have := congrFun (h ![1, 0]) 1
  rw [pinv_P12] at this
  simp [P12, Matrix.mulVec, dotProduct, Fin.sum_univ_two] at this

/-- Mutante 4: deconvolucao sem `hK`. Falso: com `K̂(-k₀) = 0` (um zero, como os do analogo
1D do Beta-kernel, ver o relatorio), `f̂ = 0` e `f̂ = 1` dao o mesmo `ĥ = 0`. -/
theorem mutant_no_nonvanishing_false :
    ¬ ∀ (Kr fhat hhat : Unit → ℂ), (∀ k, hhat k = Kr k * fhat k) →
      fhat = fun k => hhat k / Kr k := by
  intro h
  have := congrFun (h (fun _ => 0) (fun _ => 1) (fun _ => 0) (fun _ => by simp)) ()
  simp at this

end LeanReal.Chap05Barycentric

#print axioms LeanReal.Chap05Barycentric.Phi_sub
#print axioms LeanReal.Chap05Barycentric.Phi_mem_simplex
#print axioms LeanReal.Chap05Barycentric.lipschitz
#print axioms LeanReal.Chap05Barycentric.lipschitz_eq_of_no_sign_change
#print axioms LeanReal.Chap05Barycentric.lipschitz_eq_of_injective
#print axioms LeanReal.Chap05Barycentric.ratio_expansion
#print axioms LeanReal.Chap05Barycentric.Phi_ex_eq
#print axioms LeanReal.Chap05Barycentric.no_lower_bound
#print axioms LeanReal.Chap05Barycentric.mutant_constant_false
#print axioms LeanReal.Chap05Barycentric.mutant_always_equal_false
#print axioms LeanReal.Chap05Barycentric.mul_pinv
#print axioms LeanReal.Chap05Barycentric.pinv_mul_idem
#print axioms LeanReal.Chap05Barycentric.pinv_mul_symm
#print axioms LeanReal.Chap05Barycentric.range_pinv_sub
#print axioms LeanReal.Chap05Barycentric.range_transpose_sub
#print axioms LeanReal.Chap05Barycentric.pinv_mul_apply_of_mem
#print axioms LeanReal.Chap05Barycentric.inversion_restriction
#print axioms LeanReal.Chap05Barycentric.deconvolution
#print axioms LeanReal.Chap05Barycentric.mutant_all_x_false
#print axioms LeanReal.Chap05Barycentric.mutant_no_nonvanishing_false
