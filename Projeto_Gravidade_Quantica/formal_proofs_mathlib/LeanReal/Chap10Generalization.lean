import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Constructions.BorelSpace.Real
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.Calculus.Deriv.Mul

/-!
# Capitulo 10: `prop:degenerate`, `prop:counterexample` e a conta `‖2I - Q‖_F² ≥ d` (lote B8)

Fonte: `unified_quantum_gravity_book/chap10_information_geometry_minimax_deep_learning.tex`.

## `prop:degenerate` (10.1)

> If some `g̃`-geodesic segment of length at most `L_max` from `θ₀` to a point of `Σ*` stays in
> `Θ ∖ O_sing`, then `κ*_info = 0`.

Reducao ABSTRATA declarada: `κ*` e o infimo `sInf (F '' A)` de um funcional `F ≥ 0` (o supremo
essencial da aceleracao covariante) sobre a classe admissivel `A`. O fato classico "uma geodesica
parametrizada por comprimento de arco tem `Dγ̇/ds = 0`" entra como a hipotese NOMEADA
`h_geodesic : ∃ γ ∈ A, F γ = 0`. Nao ha metrica de Fisher, conexao de Levi-Civita nem supremo
essencial aqui. Atencao: em Lean `sInf ∅ = 0` em `ℝ`; a hipotese `h_geodesic` garante `A ≠ ∅`, e
o mutante `mutant_no_geodesic_false` mostra que sem ela a conclusao falha.

## `prop:counterexample` (10.2), texto CORRENTE (com a hipotese de posto linha cheio, F-59)

> Gaussian linear regression, `N` samples `X ∈ ℝ^{N×D}`, `D > N`, of full row rank `N`. ...
> `θ* = X⁺ y` the minimum-norm interpolant. ... (1) the loss Hessian `H = XᵀX/N` has
> `Tr H > 0`, so the bound `E[Tr H] ≤ D λ_max κ*` fails; (2) with labels `y_i ∈ {±1}` uniform and
> independent of the inputs, and the squared loss clipped to `[0,1]`, the generalization gap of
> `θ*` is at least `1/2` for every distribution of the inputs under which `X` has rank `N` a.s.
> Without this hypothesis the conclusion can fail: for `x ≡ 0`, `θ* = 0`, and training and test
> loss both equal `1`. A candidate PAC-Bayes-type bound ... equals `√(ln(2/δ)/2N)` at
> `κ* = 0`, which is `0.19` for `N = 50`, `δ = 0.05`, and is below `1/2` for all `N ≥ 8`.

Reducao declarada:
* `θ* := Xᵀ (XXᵀ)⁻¹ y` (`thetaStar`). A Mathlib nao tem a pseudoinversa de Moore-Penrose; em
  vez de identificar `θ*` com `X⁺y`, provamos as duas propriedades que a definem no caso
  consistente: interpola (`interpolates`) e tem norma minima entre os interpolantes
  (`min_norm`). Ambas usam `rank X = N`.
* Teste: para uma medida de probabilidade `μ` QUALQUER em `ℝ^D` (a lei da entrada nova), a
  perda de teste e `∫ ½(min((1-f)²,1) + min((1+f)²,1)) dμ(x)` com `f = x·θ*`. A media sobre o
  rotulo novo uniforme em `{±1}` e independente entra assim, como media de dois rotulos (exata
  para essa lei). O "q.c. sobre a amostra" e imediato: o teorema vale para cada amostra de
  posto `N`.
* O passo `κ* = 0` de 10.2 e 10.1 aplicado a um segmento reto; o fato "metrica constante ⇒
  simbolos de Christoffel nulos ⇒ retas sao geodesicas" NAO e formalizado (so
  `segment_accel_zero`: o segmento tem segunda derivada nula).
* Hipoteses do livro nao usadas em (2): `D > N` (posto `N` ja forca `N ≤ D`) e `y_i ∈ {±1}`
  (so o rotulo NOVO precisa ser `±1`). A forma do livro e o corolario `gap_ge_half_book`.
* O valor numerico "cerca de `0,70`" para entradas gaussianas e numerico, NAO formalizado.

## Observacao `‖2I - Q‖_F² = 5d - 4 tr Q ≥ d` (Remark "On the formulation")

Fiel, para `Q` real `d × d` com `QᵀQ = 1`.
-/

noncomputable section

namespace LeanReal.Chap10Generalization

open Set Real Matrix MeasureTheory

/-! ## 10.1 `prop:degenerate` (abstrato) -/

/-- `κ* = inf_{γ ∈ A} F(γ)` (definicao de `κ*_info`, com `F` o supremo essencial da aceleracao
covariante, aqui abstrato). -/
def kappaStar {P : Type*} (A : Set P) (F : P → ℝ) : ℝ := sInf (F '' A)

/-- **Proposicao `prop:degenerate`** (reducao abstrata): se `F ≥ 0` em `A` e algum caminho
admissivel tem `F = 0` (hipotese nomeada `h_geodesic`: uma geodesica admissivel tem aceleracao
covariante nula), entao `κ* = 0`. -/
theorem degenerate {P : Type*} (A : Set P) (F : P → ℝ) (hnonneg : ∀ γ ∈ A, 0 ≤ F γ)
    (h_geodesic : ∃ γ ∈ A, F γ = 0) : kappaStar A F = 0 := by
  obtain ⟨γ, hγ, hF⟩ := h_geodesic
  have hbdd : BddBelow (F '' A) := ⟨0, by rintro _ ⟨δ, hδ, rfl⟩; exact hnonneg δ hδ⟩
  apply le_antisymm
  · exact hF ▸ csInf_le hbdd ⟨γ, hγ, rfl⟩
  · exact le_csInf ⟨F γ, γ, hγ, rfl⟩ (by rintro _ ⟨δ, hδ, rfl⟩; exact hnonneg δ hδ)

/-- Testemunha nao degenerada: `A = {0, 1}`, `F = id` (um caminho curvo de custo `1` e uma
geodesica de custo `0`); `κ* = 0` embora `F` nao seja identicamente nula em `A`. -/
theorem witness_degenerate : kappaStar ({0, 1} : Set ℝ) id = 0 ∧ id (1 : ℝ) ≠ 0 :=
  ⟨degenerate _ _ (by rintro γ (rfl | rfl) <;> norm_num) ⟨0, by simp, rfl⟩, one_ne_zero⟩

/-- Mutante (sem geodesica admissivel): FALSO, `A = {1}`, `F = id` da `κ* = 1`. -/
theorem mutant_no_geodesic_false :
    ¬ (∀ (A : Set ℝ) (F : ℝ → ℝ), (∀ γ ∈ A, 0 ≤ F γ) → A.Nonempty → kappaStar A F = 0) := by
  intro h
  have := h {1} id (by simp) (by simp)
  simp [kappaStar] at this

/-- Mutante (sem `F ≥ 0`): FALSO, `A = {-1, 0}`, `F = id` da `κ* = -1`. -/
theorem mutant_no_nonneg_false :
    ¬ (∀ (A : Set ℝ) (F : ℝ → ℝ), (∃ γ ∈ A, F γ = 0) → kappaStar A F = 0) := by
  intro h
  have h1 := h {-1, 0} id ⟨0, by simp, rfl⟩
  have h2 : kappaStar ({-1, 0} : Set ℝ) id ≤ -1 :=
    csInf_le ⟨-1, by rintro _ ⟨δ, hδ, rfl⟩; rcases hδ with rfl | rfl <;> norm_num⟩
      ⟨-1, by simp, rfl⟩
  rw [h1] at h2
  norm_num at h2

/-- O segmento reto `s ↦ s • v` tem segunda derivada nula (o que, para metrica constante, e a
aceleracao covariante; a anulacao dos simbolos de Christoffel nao e formalizada). -/
theorem segment_accel_zero {D : ℕ} (v : Fin D → ℝ) (s : ℝ) :
    deriv (deriv (fun t : ℝ => t • v)) s = 0 := by
  have h1 : deriv (fun t : ℝ => t • v) = fun _ => v := by
    funext t
    simpa using ((hasDerivAt_id t).smul_const v).deriv
  rw [h1]
  exact deriv_const s v

/-! ## 10.2 `prop:counterexample` -/

variable {N D : ℕ}

/-- Posto linha cheio `N` ⇒ `XXᵀ` invertivel. -/
theorem isUnit_mul_transpose (X : Matrix (Fin N) (Fin D) ℝ) (hX : X.rank = N) :
    IsUnit (X * Xᵀ) := by
  have h1 : (X * Xᵀ).rank = N := by rw [rank_self_mul_transpose, hX]
  have h2 : LinearMap.range (X * Xᵀ).mulVecLin = ⊤ := by
    apply Submodule.eq_top_of_finrank_eq
    rw [Module.finrank_fin_fun]
    exact h1
  apply mulVec_surjective_iff_isUnit.mp
  intro v
  have hv : v ∈ LinearMap.range (X * Xᵀ).mulVecLin := h2 ▸ Submodule.mem_top
  obtain ⟨u, hu⟩ := hv
  exact ⟨u, hu⟩

/-- `θ* = Xᵀ (XXᵀ)⁻¹ y`, a formula de `X⁺y` para posto linha cheio. -/
def thetaStar (X : Matrix (Fin N) (Fin D) ℝ) (y : Fin N → ℝ) : Fin D → ℝ :=
  Xᵀ *ᵥ ((X * Xᵀ)⁻¹ *ᵥ y)

/-- **`θ*` interpola** (prova de `prop:counterexample`: "for `X` of full row rank, `θ* = X⁺y`
interpolates the data"). -/
theorem interpolates (X : Matrix (Fin N) (Fin D) ℝ) (hX : X.rank = N) (y : Fin N → ℝ) :
    X *ᵥ thetaStar X y = y := by
  have hu := isUnit_mul_transpose X hX
  have hdet : IsUnit (X * Xᵀ).det := (isUnit_iff_isUnit_det _).mp hu
  rw [thetaStar, mulVec_mulVec, mulVec_mulVec, mul_nonsing_inv _ hdet, one_mulVec]

/-- **`θ*` tem norma minima** entre os interpolantes (caracteriza `X⁺y` no caso consistente). -/
theorem min_norm (X : Matrix (Fin N) (Fin D) ℝ) (hX : X.rank = N) (y : Fin N → ℝ)
    (θ : Fin D → ℝ) (hθ : X *ᵥ θ = y) :
    thetaStar X y ⬝ᵥ thetaStar X y ≤ θ ⬝ᵥ θ := by
  have hXt : X *ᵥ thetaStar X y = y := interpolates X hX y
  have hz : thetaStar X y = ((X * Xᵀ)⁻¹ *ᵥ y) ᵥ* X := by rw [thetaStar, mulVec_transpose]
  generalize thetaStar X y = t at hXt hz ⊢
  have horth : t ⬝ᵥ (θ - t) = 0 := by
    have hXd : X *ᵥ (θ - t) = 0 := by rw [mulVec_sub, hθ, hXt, sub_self]
    calc t ⬝ᵥ (θ - t) = ((X * Xᵀ)⁻¹ *ᵥ y) ᵥ* X ⬝ᵥ (θ - t) := by rw [← hz]
      _ = (X * Xᵀ)⁻¹ *ᵥ y ⬝ᵥ X *ᵥ (θ - t) := (dotProduct_mulVec _ _ _).symm
      _ = 0 := by rw [hXd, dotProduct_zero]
  have hsq : 0 ≤ (θ - t) ⬝ᵥ (θ - t) := by
    simp only [dotProduct]
    exact Finset.sum_nonneg (fun i _ => mul_self_nonneg _)
  have e : θ ⬝ᵥ θ = t ⬝ᵥ t + 2 * (t ⬝ᵥ (θ - t)) + (θ - t) ⬝ᵥ (θ - t) := by
    simp only [dotProduct, Pi.sub_apply, Finset.mul_sum, ← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl (fun i _ => by ring)
  rw [e, horth]
  linarith

/-- `Tr(XᵀX) = ‖X‖_F² = Σ X_ij²`. -/
theorem trace_transpose_mul_self_eq (X : Matrix (Fin N) (Fin D) ℝ) :
    trace (Xᵀ * X) = ∑ i, ∑ j, X i j ^ 2 := by
  simp only [trace, diag, mul_apply, transpose_apply, sq]
  exact Finset.sum_comm

/-- **`prop:counterexample`, item (1)**: `Tr H = Tr(XᵀX/N) > 0` para `X` de posto `N ≥ 1`. -/
theorem trace_hessian_pos (X : Matrix (Fin N) (Fin D) ℝ) (hN : 0 < N) (hX : X.rank = N) :
    0 < trace ((1 / (N : ℝ)) • (Xᵀ * X)) := by
  rw [trace_smul, trace_transpose_mul_self_eq, smul_eq_mul]
  have hX0 : X ≠ 0 := by
    rintro rfl
    rw [rank_zero] at hX
    omega
  obtain ⟨i, j, hij⟩ : ∃ i j, X i j ≠ 0 := by
    by_contra hcon
    apply hX0
    ext i j
    by_contra hne
    exact hcon ⟨i, j, hne⟩
  have hpos : 0 < ∑ i, ∑ j, X i j ^ 2 := by
    apply Finset.sum_pos' (fun i _ => Finset.sum_nonneg (fun j _ => sq_nonneg _))
    refine ⟨i, Finset.mem_univ _, ?_⟩
    exact Finset.sum_pos' (fun j _ => sq_nonneg _) ⟨j, Finset.mem_univ _, by positivity⟩
  have : (0:ℝ) < 1 / N := by
    have : (0:ℝ) < N := by exact_mod_cast hN
    positivity
  positivity

/-- **`prop:counterexample`, item (1), conclusao**: a cota `E[Tr H] ≤ D λ_max κ*` falha quando
`κ* = 0`, quaisquer que sejam `D` e `λ_max`. -/
theorem hessian_bound_fails (X : Matrix (Fin N) (Fin D) ℝ) (hN : 0 < N) (hX : X.rank = N)
    (Dr lam : ℝ) : ¬ (trace ((1 / (N : ℝ)) • (Xᵀ * X)) ≤ Dr * lam * 0) := by
  rw [mul_zero, not_le]
  exact trace_hessian_pos X hN hX

/-- Perda quadratica truncada em `[0,1]`. -/
def clip (u : ℝ) : ℝ := min u 1

/-- Perda esperada sobre um rotulo novo uniforme em `{±1}`, para a previsao `f`. -/
def labelAvgLoss (f : ℝ) : ℝ := (clip ((1 - f) ^ 2) + clip ((1 + f) ^ 2)) / 2

/-- `½(min((1-f)²,1) + min((1+f)²,1)) ≥ ½` (prova de `prop:counterexample`, item (2)). -/
theorem labelAvgLoss_ge_half (f : ℝ) : 1 / 2 ≤ labelAvgLoss f := by
  unfold labelAvgLoss clip
  rcases le_total 0 f with hf | hf
  · have h1 : min ((1 + f) ^ 2) 1 = 1 := min_eq_right (by nlinarith)
    have h2 : 0 ≤ min ((1 - f) ^ 2) 1 := le_min (sq_nonneg _) zero_le_one
    rw [h1]; linarith
  · have h1 : min ((1 - f) ^ 2) 1 = 1 := min_eq_right (by nlinarith)
    have h2 : 0 ≤ min ((1 + f) ^ 2) 1 := le_min (sq_nonneg _) zero_le_one
    rw [h1]; linarith

/-- Igualdade em `f = 1` ("with equality at `f = ±1`"). -/
theorem labelAvgLoss_one : labelAvgLoss 1 = 1 / 2 := by
  norm_num [labelAvgLoss, clip]

theorem labelAvgLoss_le_one (f : ℝ) : labelAvgLoss f ≤ 1 := by
  unfold labelAvgLoss clip
  have := min_le_right ((1 - f) ^ 2) 1
  have := min_le_right ((1 + f) ^ 2) 1
  linarith

theorem labelAvgLoss_nonneg (f : ℝ) : 0 ≤ labelAvgLoss f :=
  le_trans (by norm_num) (labelAvgLoss_ge_half f)

theorem continuous_labelAvgLoss : Continuous labelAvgLoss := by
  unfold labelAvgLoss clip
  fun_prop

/-- Perda de treino truncada. -/
def trainLoss (X : Matrix (Fin N) (Fin D) ℝ) (y : Fin N → ℝ) (θ : Fin D → ℝ) : ℝ :=
  (1 / (N : ℝ)) * ∑ i, clip ((y i - (X *ᵥ θ) i) ^ 2)

/-- Perda de teste truncada, sob a lei `μ` da entrada nova (rotulo novo uniforme em `{±1}`). -/
def testLoss (μ : Measure (Fin D → ℝ)) (θ : Fin D → ℝ) : ℝ :=
  ∫ x, labelAvgLoss (x ⬝ᵥ θ) ∂μ

/-- O interpolante tem perda de treino nula. -/
theorem trainLoss_interpolant (X : Matrix (Fin N) (Fin D) ℝ) (hX : X.rank = N)
    (y : Fin N → ℝ) : trainLoss X y (thetaStar X y) = 0 := by
  simp [trainLoss, interpolates X hX y, clip]

/-- A perda de teste e `≥ 1/2` para TODA lei `μ` de probabilidade das entradas. -/
theorem testLoss_ge_half (μ : Measure (Fin D → ℝ)) [IsProbabilityMeasure μ] (θ : Fin D → ℝ) :
    1 / 2 ≤ testLoss μ θ := by
  have hc : Continuous fun x : Fin D → ℝ => labelAvgLoss (x ⬝ᵥ θ) :=
    continuous_labelAvgLoss.comp (by unfold dotProduct; fun_prop)
  have hint : Integrable (fun x : Fin D → ℝ => labelAvgLoss (x ⬝ᵥ θ)) μ := by
    refine (integrable_const (1 : ℝ)).mono' hc.aestronglyMeasurable (ae_of_all _ fun x => ?_)
    rw [Real.norm_eq_abs, abs_of_nonneg (labelAvgLoss_nonneg _)]
    exact labelAvgLoss_le_one _
  have := integral_mono (integrable_const (1 / 2 : ℝ)) hint (fun x => labelAvgLoss_ge_half _)
  simpa [testLoss] using this

/-- **`prop:counterexample`, item (2)** (texto corrente): se `X` tem posto linha cheio `N`, o gap
de generalizacao do interpolante de norma minima e `≥ 1/2`, para toda lei de probabilidade `μ`
da entrada nova. -/
theorem gap_ge_half (X : Matrix (Fin N) (Fin D) ℝ) (hX : X.rank = N) (y : Fin N → ℝ)
    (μ : Measure (Fin D → ℝ)) [IsProbabilityMeasure μ] :
    1 / 2 ≤ testLoss μ (thetaStar X y) - trainLoss X y (thetaStar X y) := by
  rw [trainLoss_interpolant X hX y, sub_zero]
  exact testLoss_ge_half μ _

/-- A forma do livro, com as hipoteses `D > N` e `y_i ∈ {±1}` (nao usadas). -/
theorem gap_ge_half_book (X : Matrix (Fin N) (Fin D) ℝ) (_hD : N < D) (hX : X.rank = N)
    (y : Fin N → ℝ) (_hy : ∀ i, y i = 1 ∨ y i = -1)
    (μ : Measure (Fin D → ℝ)) [IsProbabilityMeasure μ] :
    1 / 2 ≤ testLoss μ (thetaStar X y) - trainLoss X y (thetaStar X y) :=
  gap_ge_half X hX y μ

/-! ### Testemunha nao degenerada: `N = 1`, `D = 2`, `X = [1 0]`, gap exatamente `1/2` -/

/-- A matriz de dados `X = [1 0]`. -/
def X₁ : Matrix (Fin 1) (Fin 2) ℝ := !![1, 0]

theorem X₁_mul_transpose : X₁ * X₁ᵀ = 1 := by
  ext i j
  fin_cases i; fin_cases j
  simp [X₁, mul_apply, Fin.sum_univ_two]

theorem X₁_rank : X₁.rank = 1 := by
  rw [← rank_self_mul_transpose, X₁_mul_transpose, rank_one, Fintype.card_fin]

/-- A entrada nova `x = (1,0)` da a previsao `x·θ* = 1`. -/
theorem X₁_pred : (![1, 0] : Fin 2 → ℝ) ⬝ᵥ thetaStar X₁ (fun _ => 1) = 1 := by
  have h := congrFun (interpolates X₁ X₁_rank (fun _ => 1)) 0
  simpa [X₁, mulVec, dotProduct, Fin.sum_univ_two] using h

/-- **Testemunha**: com `μ = δ_{(1,0)}` o gap e EXATAMENTE `1/2` (a cota do livro e otima), e
todas as hipoteses de `gap_ge_half_book` valem (`D = 2 > N = 1`, posto `1`, `y = 1`). -/
theorem witness_gap_half :
    1 < 2 ∧ X₁.rank = 1 ∧ (∀ i : Fin 1, (fun _ => (1:ℝ)) i = 1 ∨ (fun _ => (1:ℝ)) i = -1) ∧
    testLoss (Measure.dirac ![1, 0]) (thetaStar X₁ (fun _ => 1)) -
      trainLoss X₁ (fun _ => 1) (thetaStar X₁ (fun _ => 1)) = 1 / 2 := by
  refine ⟨by norm_num, X₁_rank, fun _ => Or.inl rfl, ?_⟩
  rw [trainLoss_interpolant X₁ X₁_rank, sub_zero, testLoss, integral_dirac, X₁_pred,
    labelAvgLoss_one]

/-- Mutante (gap ESTRITAMENTE maior que `1/2`): FALSO pela testemunha. -/
theorem mutant_gap_strict_false :
    ¬ (∀ (X : Matrix (Fin 1) (Fin 2) ℝ), X.rank = 1 → ∀ (y : Fin 1 → ℝ)
        (μ : Measure (Fin 2 → ℝ)) [IsProbabilityMeasure μ],
        1 / 2 < testLoss μ (thetaStar X y) - trainLoss X y (thetaStar X y)) := by
  intro h
  have := h X₁ X₁_rank (fun _ => 1) (Measure.dirac ![1, 0])
  rw [witness_gap_half.2.2.2] at this
  exact lt_irrefl _ this

/-! ### Mutante: a versao ANTIGA (sem posto cheio), contraexemplo `x ≡ 0` -/

/-- **Mutante: o enunciado antigo de `prop:counterexample`(2)** ("gap `≥ 1/2` para toda
distribuicao das entradas", sem a hipotese de posto): FALSO. Contraexemplo `x ≡ 0`: `N = 1`,
`D = 2`, `X = 0`, `y = 1`, `μ = δ_0`; `θ* = 0`, perda de treino `1`, perda de teste `1`,
gap `0`. -/
theorem mutant_old_statement_false :
    ¬ (∀ (N D : ℕ) (X : Matrix (Fin N) (Fin D) ℝ), N < D → ∀ (y : Fin N → ℝ),
        (∀ i, y i = 1 ∨ y i = -1) → ∀ (μ : Measure (Fin D → ℝ)) [IsProbabilityMeasure μ],
        1 / 2 ≤ testLoss μ (thetaStar X y) - trainLoss X y (thetaStar X y)) := by
  intro h
  have := h 1 2 0 (by norm_num) (fun _ => 1) (fun _ => Or.inl rfl) (Measure.dirac 0)
  have ht : thetaStar (0 : Matrix (Fin 1) (Fin 2) ℝ) (fun _ => 1) = 0 := by
    simp [thetaStar]
  rw [ht, testLoss, integral_dirac] at this
  norm_num [trainLoss, labelAvgLoss, clip] at this

/-- Os numeros do contraexemplo `x ≡ 0`: `θ* = 0`, treino `1`, teste `1`. -/
theorem zero_data_losses :
    thetaStar (0 : Matrix (Fin 1) (Fin 2) ℝ) (fun _ => 1) = 0 ∧
    trainLoss (0 : Matrix (Fin 1) (Fin 2) ℝ) (fun _ => 1) 0 = 1 ∧
    testLoss (Measure.dirac (0 : Fin 2 → ℝ)) 0 = 1 := by
  refine ⟨by simp [thetaStar], by norm_num [trainLoss, clip], ?_⟩
  rw [testLoss, integral_dirac]
  norm_num [labelAvgLoss, clip]

/-- Mutante (interpolacao sem posto cheio): FALSO, `X = 0`, `y = 1`. -/
theorem mutant_interpolates_no_rank_false :
    ¬ (∀ (X : Matrix (Fin 1) (Fin 2) ℝ) (y : Fin 1 → ℝ), X *ᵥ thetaStar X y = y) := by
  intro h
  have := congrFun (h 0 (fun _ => 1)) 0
  simp at this

/-! ### A cota PAC-Bayes candidata -/

/-- `√((D ln(1 + L²κ²/2σ²) + ln(2/δ))/2N)`. -/
def pacBound (Dr L κ σ δ Nr : ℝ) : ℝ :=
  √((Dr * log (1 + L ^ 2 * κ ^ 2 / (2 * σ ^ 2)) + log (2 / δ)) / (2 * Nr))

/-- Em `κ* = 0` a cota vale `√(ln(2/δ)/2N)`. -/
theorem pacBound_at_zero (Dr L σ δ Nr : ℝ) :
    pacBound Dr L 0 σ δ Nr = √(log (2 / δ) / (2 * Nr)) := by
  simp [pacBound]

/-- `3,66 < ln 40 < 3,72` (via `ln 2` e `ln(5/4) ∈ [1/5, 1/4]`). -/
theorem log_forty_bounds : 3.66 < log 40 ∧ log 40 < 3.72 := by
  have h40 : log 40 = 5 * log 2 + log (5 / 4) := by
    rw [show (40:ℝ) = 2 ^ 5 * (5 / 4) by norm_num, log_mul (by norm_num) (by norm_num),
      log_pow]
    norm_num
  have hu : log (5 / 4 : ℝ) ≤ 1 / 4 := by
    have := log_le_sub_one_of_pos (by norm_num : (0:ℝ) < 5 / 4); linarith
  have hl : 1 / 5 ≤ log (5 / 4 : ℝ) := by
    have := log_le_sub_one_of_pos (by norm_num : (0:ℝ) < 4 / 5)
    rw [show (4 / 5 : ℝ) = (5 / 4)⁻¹ by norm_num, log_inv] at this
    linarith
  have h2l := log_two_gt_d9
  have h2u := log_two_lt_d9
  rw [h40]
  constructor <;> norm_num at h2l h2u ⊢ <;> linarith

/-- **"`0.19` for `N = 50` and `δ = 0.05`"**: `0,19 < √(ln 40/100) < 0,195`. -/
theorem pac_N50 : 0.19 < √(log (2 / 0.05) / (2 * 50)) ∧ √(log (2 / 0.05) / (2 * 50)) < 0.195 := by
  have h40 : (2 / 0.05 : ℝ) = 40 := by norm_num
  rw [h40]
  obtain ⟨hl, hu⟩ := log_forty_bounds
  constructor
  · rw [Real.lt_sqrt (by norm_num)]; linarith
  · rw [Real.sqrt_lt' (by norm_num)]; linarith

/-- **Limiar exato**: `√(ln 40/2N) < 1/2 ⟺ N > 2 ln 40` (para `N > 0`). -/
theorem pac_lt_half_iff (Nr : ℝ) (hN : 0 < Nr) :
    √(log 40 / (2 * Nr)) < 1 / 2 ↔ 2 * log 40 < Nr := by
  rw [Real.sqrt_lt' (by norm_num), div_lt_iff₀ (by positivity)]
  constructor <;> intro h <;> linarith

/-- **"below `1/2` for all `N ≥ 8` at `δ = 0.05`"**. -/
theorem pac_below_half (n : ℕ) (hn : 8 ≤ n) : √(log (2 / 0.05) / (2 * (n : ℝ))) < 1 / 2 := by
  have h40 : (2 / 0.05 : ℝ) = 40 := by norm_num
  rw [h40, pac_lt_half_iff _ (by positivity)]
  have : (8:ℝ) ≤ n := by exact_mod_cast hn
  linarith [log_forty_bounds.2]

/-- Mutante (`N ≥ 7` no lugar de `N ≥ 8`): FALSO, em `N = 7` a cota e `≥ 1/2`. -/
theorem mutant_N7_false :
    ¬ (∀ n : ℕ, 7 ≤ n → √(log (2 / 0.05) / (2 * (n : ℝ))) < 1 / 2) := by
  intro h
  have := h 7 le_rfl
  have h40 : (2 / 0.05 : ℝ) = 40 := by norm_num
  rw [h40, pac_lt_half_iff _ (by norm_num)] at this
  push_cast at this
  linarith [log_forty_bounds.1]

/-! ## Observacao `‖2I - Q‖_F² = 5d - 4 tr Q ≥ d` -/

/-- **Remark "On the formulation"**: para `Q` ortogonal (`QᵀQ = 1`),
`‖2I - Q‖_F² = 5d - 4 tr Q` e `≥ d`. -/
theorem frob_two_sub_orth (d : ℕ) (Q : Matrix (Fin d) (Fin d) ℝ) (hQ : Qᵀ * Q = 1) :
    ∑ i, ∑ j, ((2 : ℝ) • (1 : Matrix (Fin d) (Fin d) ℝ) - Q) i j ^ 2 = 5 * d - 4 * trace Q ∧
    (d : ℝ) ≤ ∑ i, ∑ j, ((2 : ℝ) • (1 : Matrix (Fin d) (Fin d) ℝ) - Q) i j ^ 2 := by
  -- columns have unit norm
  have hcol : ∀ j, ∑ i, Q i j ^ 2 = 1 := by
    intro j
    have := congrFun (congrFun hQ j) j
    simpa [mul_apply, sq] using this
  have hsum : ∑ i, ∑ j, Q i j ^ 2 = d := by
    rw [Finset.sum_comm]; simp [hcol]
  have hpt : ∀ i j, ((2 : ℝ) • (1 : Matrix (Fin d) (Fin d) ℝ) - Q) i j ^ 2 =
      (if i = j then 4 - 4 * Q i j else 0) + Q i j ^ 2 := by
    intro i j
    simp only [Matrix.sub_apply, Matrix.smul_apply, one_apply, smul_eq_mul]
    split_ifs <;> ring
  have heq : ∑ i, ∑ j, ((2 : ℝ) • (1 : Matrix (Fin d) (Fin d) ℝ) - Q) i j ^ 2 =
      5 * d - 4 * trace Q := by
    simp only [hpt, Finset.sum_add_distrib, Finset.sum_ite_eq, Finset.mem_univ, ite_true, hsum,
      trace, diag, Finset.sum_sub_distrib, Finset.mul_sum]
    simp
    ring
  have hdiag : ∀ i, Q i i ≤ 1 := by
    intro i
    have h1 : Q i i ^ 2 ≤ ∑ k, Q k i ^ 2 :=
      Finset.single_le_sum (f := fun k => Q k i ^ 2) (fun k _ => sq_nonneg _) (Finset.mem_univ i)
    rw [hcol] at h1
    nlinarith
  have htr : trace Q ≤ d := by
    simp only [trace, diag]
    calc ∑ i, Q i i ≤ ∑ _i : Fin d, (1 : ℝ) := Finset.sum_le_sum (fun i _ => hdiag i)
      _ = d := by simp
  refine ⟨heq, ?_⟩
  rw [heq]
  linarith

/-- Rotacao de `90°` em `ℝ²`. -/
def rot90 : Matrix (Fin 2) (Fin 2) ℝ := !![0, -1; 1, 0]

theorem rot90_orth : rot90ᵀ * rot90 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [rot90, mul_apply, Fin.sum_univ_two]

/-- **Testemunha nao degenerada**: a rotacao de `90°` (`tr Q = 0`), perda `10 ≥ 2`. -/
theorem witness_rot90 :
    ∑ i, ∑ j, ((2 : ℝ) • (1 : Matrix (Fin 2) (Fin 2) ℝ) - rot90) i j ^ 2 = 10 := by
  rw [(frob_two_sub_orth 2 rot90 rot90_orth).1]
  simp [rot90, trace, Fin.sum_univ_two]
  norm_num

/-- Mutante (sem ortogonalidade): FALSO, `Q = 2I` (`d = 1`) tem perda `0 < 1`. -/
theorem mutant_no_orth_false :
    ¬ (∀ (d : ℕ) (Q : Matrix (Fin d) (Fin d) ℝ),
        (d : ℝ) ≤ ∑ i, ∑ j, ((2 : ℝ) • (1 : Matrix (Fin d) (Fin d) ℝ) - Q) i j ^ 2) := by
  intro h
  have := h 1 ((2 : ℝ) • 1)
  simp at this
  norm_num at this

/-- Mutante (cota `d + 1`): FALSO, `Q = I` atinge `d`. -/
theorem mutant_d_plus_one_false :
    ¬ (∀ (d : ℕ) (Q : Matrix (Fin d) (Fin d) ℝ), Qᵀ * Q = 1 →
        (d : ℝ) + 1 ≤ ∑ i, ∑ j, ((2 : ℝ) • (1 : Matrix (Fin d) (Fin d) ℝ) - Q) i j ^ 2) := by
  intro h
  have := h 1 1 (by simp)
  rw [(frob_two_sub_orth 1 1 (by simp)).1] at this
  simp at this
  norm_num at this

end LeanReal.Chap10Generalization

#print axioms LeanReal.Chap10Generalization.degenerate
#print axioms LeanReal.Chap10Generalization.witness_degenerate
#print axioms LeanReal.Chap10Generalization.mutant_no_geodesic_false
#print axioms LeanReal.Chap10Generalization.mutant_no_nonneg_false
#print axioms LeanReal.Chap10Generalization.segment_accel_zero
#print axioms LeanReal.Chap10Generalization.isUnit_mul_transpose
#print axioms LeanReal.Chap10Generalization.interpolates
#print axioms LeanReal.Chap10Generalization.min_norm
#print axioms LeanReal.Chap10Generalization.trace_transpose_mul_self_eq
#print axioms LeanReal.Chap10Generalization.trace_hessian_pos
#print axioms LeanReal.Chap10Generalization.hessian_bound_fails
#print axioms LeanReal.Chap10Generalization.labelAvgLoss_ge_half
#print axioms LeanReal.Chap10Generalization.labelAvgLoss_one
#print axioms LeanReal.Chap10Generalization.trainLoss_interpolant
#print axioms LeanReal.Chap10Generalization.testLoss_ge_half
#print axioms LeanReal.Chap10Generalization.gap_ge_half
#print axioms LeanReal.Chap10Generalization.gap_ge_half_book
#print axioms LeanReal.Chap10Generalization.X₁_rank
#print axioms LeanReal.Chap10Generalization.X₁_pred
#print axioms LeanReal.Chap10Generalization.witness_gap_half
#print axioms LeanReal.Chap10Generalization.mutant_gap_strict_false
#print axioms LeanReal.Chap10Generalization.mutant_old_statement_false
#print axioms LeanReal.Chap10Generalization.zero_data_losses
#print axioms LeanReal.Chap10Generalization.mutant_interpolates_no_rank_false
#print axioms LeanReal.Chap10Generalization.pacBound_at_zero
#print axioms LeanReal.Chap10Generalization.log_forty_bounds
#print axioms LeanReal.Chap10Generalization.pac_N50
#print axioms LeanReal.Chap10Generalization.pac_lt_half_iff
#print axioms LeanReal.Chap10Generalization.pac_below_half
#print axioms LeanReal.Chap10Generalization.mutant_N7_false
#print axioms LeanReal.Chap10Generalization.frob_two_sub_orth
#print axioms LeanReal.Chap10Generalization.rot90_orth
#print axioms LeanReal.Chap10Generalization.witness_rot90
#print axioms LeanReal.Chap10Generalization.mutant_no_orth_false
#print axioms LeanReal.Chap10Generalization.mutant_d_plus_one_false
