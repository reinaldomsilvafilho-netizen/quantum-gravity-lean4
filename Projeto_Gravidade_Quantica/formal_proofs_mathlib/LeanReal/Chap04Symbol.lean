import Mathlib.MeasureTheory.Integral.Bochner.ContinuousLinearMap
import Mathlib.MeasureTheory.Measure.Dirac.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.LinearAlgebra.Matrix.DotProduct
import Mathlib.Analysis.Real.Pi.Bounds

/-!
# Cap. 3 `thm:laplacian_symbol` e cap. 4 `thm:dispersion` (Lote A2, item 4)

Fontes:
* `chap03_pascal_simplex_continuous_multinomials.tex`, Teorema "Fourier Symbol and Long-Wavelength
  Expansion" (`thm:laplacian_symbol`);
* `chap04_simplicial_waves_porous_transport.tex`, Teorema "Dispersion Symbol and Long-Wavelength
  Metric" (`thm:dispersion`), que repete o simbolo do cap. 3 e acrescenta, entre parenteses, a
  algebra do multinomio reticulado.

Enunciado do livro (cap. 3). Com
`Δu(x) = (1/(2α² I_m(α))) ∫_{Δ_{m-1}(α)} binom(α,y) [u(x+y) - 2u(x) + u(x-y)] dy`:
> For `k ∈ ℝ^{m-1}`, `Δ e^{ik·x} = -σ(k) e^{ik·x}` with
> `σ(k) = α⁻²[1 - Re 𝒢_α(ik)] = α⁻² ∫ K̃_α(y)(1 - cos(k·y)) dy ∈ [0, 2/α²]`.
> As `|k| → 0`, `σ(k) = (1/(2α²)) kᵀM₂k + O(|k|⁴)`, `M₂ = ∫ K̃_α y yᵀ dy`, and by the
> `S_m`-symmetry of the density `M₂ = a I + b 11ᵀ` with scalars `a > 0`, `b`.
Cap. 4 acrescenta: `σ` e par; para o multinomio reticulado o limite de pequeno `k` e
`S²/(2m²) + (Q - S²/m)/(2mα)` (`S = ∑ k_j`, `Q = |k|²`), que so se reduz a
`(1/(2mα)) kᵀ(I + 11ᵀ)k` sob `S = 0`, onde ambos valem `Q/(2mα)`.

## Reducao declarada

* A medida normalizada `K̃_α(y) dy` e substituida por uma MEDIDA DE PROBABILIDADE abstrata `μ`
  em `ℝ^d` (`d = m-1`, tipo `Fin d → ℝ`). Toda a parte "simbolo e cotas" so usa que `μ` e de
  probabilidade; o fato de que `K̃_α dy` o e (positividade e normalizacao por `I_m(α)`) nao e
  formalizado aqui (positividade esta em `Chap03Pascal`).
* `α` e um real qualquer (a hipotese `α > 0` do livro nao e usada; com `α = 0` ambos os lados
  valem `0` em Lean).
* O termo `O(|k|⁴)`: prova-se a cota explicita `|σ(k) - (1/(2α²))∫(k·y)² dμ| ≤
  (5/96) α⁻² ∫(k·y)⁴ dμ` quando `|k·y| ≤ 1` `μ`-q.t.p. (`symbol_quartic`), e a cota de um lado
  `σ(k) ≤ (1/(2α²))∫(k·y)² dμ` sem restricao (`symbol_le_quadratic`). Para `μ` de suporte em
  `|y| ≤ R` isso da `O(|k|⁴)` com constante `(5/96)R⁴/α²` para `|k| ≤ 1/R`; essa ultima
  passagem (Cauchy-Schwarz) nao e escrita.
* `M₂ = aI + b11ᵀ`: deduzido da invariancia de `μ` pelas permutacoes de coordenadas de `ℝ^d`
  (hipotese `hperm`), que e o que a prova do livro usa para as `m-1` primeiras coordenadas. Que
  a densidade multinomial tenha essa invariancia nao e formalizado. `a ≥ 0` e provado, via
  `a = ½∫(y_i - y_j)²`; `a > 0` exige que `μ` nao se concentre em `{y_i = y_j}` e nao e provado.
* Algebra do reticulado (cap. 4): identidades exatas em `Q`, `S`, `α`, `m`.
-/

noncomputable section

namespace LeanReal.Chap04Symbol

open MeasureTheory Real Matrix Finset

variable {d : ℕ}

/-! ## Simbolo e cotas para uma medida de probabilidade -/

/-- Simbolo `σ(k) = α⁻² ∫ (1 - cos(k·y)) dμ(y)`. -/
def symbol (μ : Measure (Fin d → ℝ)) (α : ℝ) (k : Fin d → ℝ) : ℝ :=
  (α ^ 2)⁻¹ * ∫ y, (1 - Real.cos (k ⬝ᵥ y)) ∂μ

/-- Laplaciano de diferencas centradas `Δu(x) = (1/(2α²)) ∫ [u(x+y) - 2u(x) + u(x-y)] dμ(y)`. -/
def lap (μ : Measure (Fin d → ℝ)) (α : ℝ) (u : (Fin d → ℝ) → ℂ) (x : Fin d → ℝ) : ℂ :=
  (1 / (2 * (α : ℂ) ^ 2)) * ∫ y, (u (x + y) - 2 * u x + u (x - y)) ∂μ

/-- Onda plana `e_k(x) = exp(i k·x)`. -/
def wave (k : Fin d → ℝ) (x : Fin d → ℝ) : ℂ := Complex.exp (Complex.I * ((k ⬝ᵥ x : ℝ) : ℂ))

/-- O colchete da prova: `e^{it} - 2 + e^{-it} = -2(1 - cos t)`. -/
theorem bracket (t : ℝ) :
    Complex.exp (Complex.I * t) - 2 + Complex.exp (-(Complex.I * t)) =
      -2 * ((1 - Real.cos t : ℝ) : ℂ) := by
  have h := Complex.cos_add_sin_I (t : ℂ)
  have h' := Complex.cos_sub_sin_I (t : ℂ)
  rw [show Complex.I * t = (t : ℂ) * Complex.I by ring, ← h,
    show -((t : ℂ) * Complex.I) = -(t : ℂ) * Complex.I by ring, ← Complex.cos_add_sin_I,
    Complex.cos_neg, Complex.sin_neg]
  push_cast
  ring

/-- **`thm:laplacian_symbol` / `thm:dispersion`, autofuncao**: `Δ e_k = -σ(k) e_k`, para
qualquer medida `μ` (sem hipotese de integrabilidade: a identidade e linear). -/
theorem lap_wave (μ : Measure (Fin d → ℝ)) (α : ℝ) (k x : Fin d → ℝ) :
    lap μ α (wave k) x = -((symbol μ α k : ℝ) : ℂ) * wave k x := by
  have hint : (fun y => wave k (x + y) - 2 * wave k x + wave k (x - y)) =
      fun y => (-2 * wave k x) * ((1 - Real.cos (k ⬝ᵥ y) : ℝ) : ℂ) := by
    funext y
    have e := bracket (k ⬝ᵥ y)
    have w1 : wave k (x + y) = wave k x * Complex.exp (Complex.I * ((k ⬝ᵥ y : ℝ) : ℂ)) := by
      simp only [wave, dotProduct_add]
      rw [← Complex.exp_add]
      congr 1
      push_cast
      ring
    have w2 : wave k (x - y) = wave k x * Complex.exp (-(Complex.I * ((k ⬝ᵥ y : ℝ) : ℂ))) := by
      simp only [wave, dotProduct_sub]
      rw [← Complex.exp_add]
      congr 1
      push_cast
      ring
    rw [w1, w2]
    linear_combination (wave k x) * e
  unfold lap symbol
  rw [hint, integral_const_mul, integral_complex_ofReal]
  push_cast
  field_simp

/-- O simbolo e par: `σ(-k) = σ(k)`. -/
theorem symbol_even (μ : Measure (Fin d → ℝ)) (α : ℝ) (k : Fin d → ℝ) :
    symbol μ α (-k) = symbol μ α k := by
  unfold symbol
  simp only [neg_dotProduct, Real.cos_neg]

/-- O integrando `1 - cos(k·y)` e integravel para `μ` finita. -/
theorem integrable_one_sub_cos (μ : Measure (Fin d → ℝ)) [IsFiniteMeasure μ] (k : Fin d → ℝ) :
    Integrable (fun y => 1 - Real.cos (k ⬝ᵥ y)) μ := by
  refine Integrable.of_bound (by fun_prop) 2 (Filter.Eventually.of_forall fun y => ?_)
  rw [Real.norm_eq_abs, abs_le]
  constructor <;> linarith [Real.cos_le_one (k ⬝ᵥ y), Real.neg_one_le_cos (k ⬝ᵥ y)]

/-- **Cotas `σ(k) ∈ [0, 2/α²]`** para uma medida de probabilidade. -/
theorem symbol_bounds (μ : Measure (Fin d → ℝ)) [IsProbabilityMeasure μ] (α : ℝ)
    (k : Fin d → ℝ) : 0 ≤ symbol μ α k ∧ symbol μ α k ≤ 2 / α ^ 2 := by
  have h0 : 0 ≤ ∫ y, (1 - Real.cos (k ⬝ᵥ y)) ∂μ :=
    integral_nonneg fun y => sub_nonneg.mpr (Real.cos_le_one _)
  have h2 : ∫ y, (1 - Real.cos (k ⬝ᵥ y)) ∂μ ≤ 2 := by
    have := integral_mono (integrable_one_sub_cos μ k) (integrable_const (2 : ℝ))
      (fun y => by simp only; linarith [Real.neg_one_le_cos (k ⬝ᵥ y)])
    simpa using this
  unfold symbol
  constructor
  · exact mul_nonneg (inv_nonneg.mpr (sq_nonneg α)) h0
  · rw [div_eq_inv_mul]
    exact mul_le_mul_of_nonneg_left h2 (inv_nonneg.mpr (sq_nonneg α))

/-- Forma `σ(k) = α⁻²[1 - Re 𝒢(ik)]`, `𝒢(ik) = ∫ exp(-i k·y) dμ`, para `μ` de probabilidade. -/
theorem symbol_re_form (μ : Measure (Fin d → ℝ)) [IsProbabilityMeasure μ] (α : ℝ)
    (k : Fin d → ℝ) :
    symbol μ α k = (α ^ 2)⁻¹ *
      (1 - (∫ y, Complex.exp (-(Complex.I * ((k ⬝ᵥ y : ℝ) : ℂ))) ∂μ).re) := by
  have hexp : Integrable (fun y => Complex.exp (-(Complex.I * ((k ⬝ᵥ y : ℝ) : ℂ)))) μ := by
    refine Integrable.of_bound (by fun_prop) 1 (Filter.Eventually.of_forall fun y => ?_)
    rw [show -(Complex.I * ((k ⬝ᵥ y : ℝ) : ℂ)) = ((-(k ⬝ᵥ y) : ℝ) : ℂ) * Complex.I by
      push_cast; ring, Complex.norm_exp_ofReal_mul_I]
  have hcos : Integrable (fun y => Real.cos (k ⬝ᵥ y)) μ := by
    refine Integrable.of_bound (by fun_prop) 1 (Filter.Eventually.of_forall fun y => ?_)
    rw [Real.norm_eq_abs]
    exact Real.abs_cos_le_one _
  have hre : (∫ y, Complex.exp (-(Complex.I * ((k ⬝ᵥ y : ℝ) : ℂ))) ∂μ).re =
      ∫ y, Real.cos (k ⬝ᵥ y) ∂μ := by
    have h := integral_re hexp
    simp only [RCLike.re_to_complex] at h
    rw [← h]
    congr 1
    funext y
    rw [show -(Complex.I * ((k ⬝ᵥ y : ℝ) : ℂ)) = ((-(k ⬝ᵥ y) : ℝ) : ℂ) * Complex.I by
      push_cast; ring, Complex.exp_ofReal_mul_I_re, Real.cos_neg]
  unfold symbol
  rw [hre, integral_sub (integrable_const 1) hcos, integral_const]
  simp

/-- **Termo quadratico, cota de um lado**: `σ(k) ≤ (1/(2α²)) ∫ (k·y)² dμ`, se o segundo
momento existe (`hM2`). -/
theorem symbol_le_quadratic (μ : Measure (Fin d → ℝ)) [IsFiniteMeasure μ] (α : ℝ)
    (k : Fin d → ℝ) (hM2 : Integrable (fun y => (k ⬝ᵥ y) ^ 2) μ) :
    symbol μ α k ≤ (1 / (2 * α ^ 2)) * ∫ y, (k ⬝ᵥ y) ^ 2 ∂μ := by
  have h := integral_mono (integrable_one_sub_cos μ k) (hM2.div_const 2)
    (fun y => by
      simp only
      linarith [Real.one_sub_sq_div_two_le_cos (x := k ⬝ᵥ y)])
  rw [integral_div] at h
  unfold symbol
  have hi : 0 ≤ (α ^ 2)⁻¹ := inv_nonneg.mpr (sq_nonneg α)
  calc (α ^ 2)⁻¹ * ∫ y, (1 - Real.cos (k ⬝ᵥ y)) ∂μ
      ≤ (α ^ 2)⁻¹ * ((∫ y, (k ⬝ᵥ y) ^ 2 ∂μ) / 2) := mul_le_mul_of_nonneg_left h hi
    _ = (1 / (2 * α ^ 2)) * ∫ y, (k ⬝ᵥ y) ^ 2 ∂μ := by
        rcases eq_or_ne α 0 with h0 | h0
        · subst h0; simp
        · field_simp

/-- **Termo quadratico com resto explicito**: se `|k·y| ≤ 1` `μ`-q.t.p., entao
`|σ(k) - (1/(2α²))∫(k·y)² dμ| ≤ (5/96) α⁻² ∫(k·y)⁴ dμ` (via `Real.cos_bound`). -/
theorem symbol_quartic (μ : Measure (Fin d → ℝ)) [IsFiniteMeasure μ] (α : ℝ)
    (k : Fin d → ℝ) (hsmall : ∀ᵐ y ∂μ, |k ⬝ᵥ y| ≤ 1) :
    |symbol μ α k - (1 / (2 * α ^ 2)) * ∫ y, (k ⬝ᵥ y) ^ 2 ∂μ| ≤
      (α ^ 2)⁻¹ * ((5 / 96) * ∫ y, (k ⬝ᵥ y) ^ 4 ∂μ) := by
  have hq2 : Integrable (fun y => (k ⬝ᵥ y) ^ 2) μ := by
    refine Integrable.of_bound (by fun_prop) 1 (hsmall.mono fun y hy => ?_)
    rw [Real.norm_eq_abs, abs_pow]
    exact pow_le_one₀ (abs_nonneg _) hy
  have hq4 : Integrable (fun y => (k ⬝ᵥ y) ^ 4) μ := by
    refine Integrable.of_bound (by fun_prop) 1 (hsmall.mono fun y hy => ?_)
    rw [Real.norm_eq_abs, abs_pow]
    exact pow_le_one₀ (abs_nonneg _) hy
  have hc := integrable_one_sub_cos μ k
  have hdiff : symbol μ α k - (1 / (2 * α ^ 2)) * ∫ y, (k ⬝ᵥ y) ^ 2 ∂μ =
      (α ^ 2)⁻¹ * ∫ y, ((1 - Real.cos (k ⬝ᵥ y)) - (k ⬝ᵥ y) ^ 2 / 2) ∂μ := by
    rw [integral_sub hc (hq2.div_const 2), integral_div]
    unfold symbol
    rcases eq_or_ne α 0 with h0 | h0
    · subst h0; simp
    · field_simp
  rw [hdiff, abs_mul, abs_of_nonneg (inv_nonneg.mpr (sq_nonneg α))]
  apply mul_le_mul_of_nonneg_left _ (inv_nonneg.mpr (sq_nonneg α))
  calc |∫ y, ((1 - Real.cos (k ⬝ᵥ y)) - (k ⬝ᵥ y) ^ 2 / 2) ∂μ|
      ≤ ∫ y, |(1 - Real.cos (k ⬝ᵥ y)) - (k ⬝ᵥ y) ^ 2 / 2| ∂μ := by
        rw [← Real.norm_eq_abs]
        exact (norm_integral_le_integral_norm _).trans (le_of_eq (by simp [Real.norm_eq_abs]))
    _ ≤ ∫ y, (5 / 96) * (k ⬝ᵥ y) ^ 4 ∂μ := by
        apply integral_mono_ae ((hc.sub (hq2.div_const 2)).abs) (hq4.const_mul _)
        filter_upwards [hsmall] with y hy
        show |(1 - Real.cos (k ⬝ᵥ y)) - (k ⬝ᵥ y) ^ 2 / 2| ≤ (5 / 96) * (k ⬝ᵥ y) ^ 4
        have hb := Real.cos_bound hy
        rw [show (1 - Real.cos (k ⬝ᵥ y)) - (k ⬝ᵥ y) ^ 2 / 2 =
          -(Real.cos (k ⬝ᵥ y) - (1 - (k ⬝ᵥ y) ^ 2 / 2)) by ring, abs_neg]
        calc |Real.cos (k ⬝ᵥ y) - (1 - (k ⬝ᵥ y) ^ 2 / 2)| ≤ |k ⬝ᵥ y| ^ 4 * (5 / 96) := hb
          _ = (5 / 96) * (k ⬝ᵥ y) ^ 4 := by
            rw [(by decide : Even 4).pow_abs]; ring
    _ = (5 / 96) * ∫ y, (k ⬝ᵥ y) ^ 4 ∂μ := integral_const_mul _ _

/-! ## Matriz de segundos momentos -/

/-- `M₂ = ∫ y yᵀ dμ`. -/
def M2 (μ : Measure (Fin d → ℝ)) : Matrix (Fin d) (Fin d) ℝ := fun i j => ∫ y, y i * y j ∂μ

/-- `∫ (k·y)² dμ = kᵀ M₂ k`, se os segundos momentos existem (`hM`). -/
theorem quadratic_eq_M2 (μ : Measure (Fin d → ℝ)) (k : Fin d → ℝ)
    (hM : ∀ i j, Integrable (fun y : Fin d → ℝ => y i * y j) μ) :
    ∫ y, (k ⬝ᵥ y) ^ 2 ∂μ = ∑ i, ∑ j, k i * k j * M2 μ i j := by
  have hexp : (fun y : Fin d → ℝ => (k ⬝ᵥ y) ^ 2) =
      fun y => ∑ i, ∑ j, k i * k j * (y i * y j) := by
    funext y
    simp only [dotProduct, sq, Finset.sum_mul_sum]
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
    ring
  rw [hexp, integral_finsetSum _ fun i _ => integrable_finsetSum _ fun j _ =>
    (hM i j).const_mul _]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [integral_finsetSum _ fun j _ => (hM i j).const_mul _]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [integral_const_mul]
  rfl

/-- Algebra: uma matriz invariante por todas as permutacoes simultaneas de linhas e colunas
tem a forma `M i j = a·[i = j] + b`, com `b = M i₀ i₁` e `a = M i₀ i₀ - M i₀ i₁`. -/
theorem perm_invariant_form (M : Matrix (Fin d) (Fin d) ℝ)
    (hM : ∀ (σ : Equiv.Perm (Fin d)) (i j : Fin d), M (σ i) (σ j) = M i j)
    (i₀ i₁ : Fin d) (h01 : i₀ ≠ i₁) (i j : Fin d) :
    M i j = (if i = j then M i₀ i₀ - M i₀ i₁ else 0) + M i₀ i₁ := by
  split_ifs with hij
  · subst hij
    have := hM (Equiv.swap i₀ i) i₀ i₀
    rw [Equiv.swap_apply_left] at this
    rw [this]; ring
  · -- primeiro leva i em i₀
    set τ := Equiv.swap i₀ i with hτ
    have h1 := hM τ i₀ (τ j)
    rw [Equiv.swap_apply_left, Equiv.swap_apply_self] at h1
    have hj' : τ j ≠ i₀ := by
      intro h
      apply hij
      have := congrArg τ h
      rw [Equiv.swap_apply_self, Equiv.swap_apply_left] at this
      exact this.symm
    -- depois leva τ j em i₁ fixando i₀
    have h2 := hM (Equiv.swap i₁ (τ j)) i₀ i₁
    rw [Equiv.swap_apply_of_ne_of_ne h01 hj'.symm, Equiv.swap_apply_left] at h2
    rw [zero_add, h1, h2]

/-- **`M₂ = aI + b11ᵀ`** a partir da invariancia de `μ` pelas permutacoes de coordenadas
(`hperm`), com `a = M₂ i₀ i₀ - M₂ i₀ i₁`, `b = M₂ i₀ i₁`. -/
theorem M2_form (μ : Measure (Fin d → ℝ))
    (hperm : ∀ σ : Equiv.Perm (Fin d), μ.map (fun y => y ∘ σ) = μ)
    (i₀ i₁ : Fin d) (h01 : i₀ ≠ i₁) (i j : Fin d) :
    M2 μ i j = (if i = j then M2 μ i₀ i₀ - M2 μ i₀ i₁ else 0) + M2 μ i₀ i₁ := by
  apply perm_invariant_form _ _ i₀ i₁ h01
  intro σ p q
  have hmeas : Measurable (fun y : Fin d → ℝ => y ∘ σ) :=
    (continuous_pi fun a => continuous_apply (σ a)).measurable
  unfold M2
  conv_rhs => rw [← hperm σ]
  rw [integral_map hmeas.aemeasurable (by fun_prop)]
  rfl

/-- `a ≥ 0`: sob a invariancia, `a = ½ ∫ (y_{i₀} - y_{i₁})² dμ`. -/
theorem M2_a_nonneg (μ : Measure (Fin d → ℝ))
    (hperm : ∀ σ : Equiv.Perm (Fin d), μ.map (fun y => y ∘ σ) = μ)
    (hM : ∀ i j, Integrable (fun y : Fin d → ℝ => y i * y j) μ)
    (i₀ i₁ : Fin d) (h01 : i₀ ≠ i₁) :
    M2 μ i₀ i₀ - M2 μ i₀ i₁ = (1 / 2) * ∫ y, (y i₀ - y i₁) ^ 2 ∂μ ∧
      0 ≤ M2 μ i₀ i₀ - M2 μ i₀ i₁ := by
  have h11 : M2 μ i₁ i₁ = M2 μ i₀ i₀ := by
    have := M2_form μ hperm i₀ i₁ h01 i₁ i₁
    simp only [↓reduceIte] at this; rw [this]; ring
  have h10 : M2 μ i₁ i₀ = M2 μ i₀ i₁ := by
    have := M2_form μ hperm i₀ i₁ h01 i₁ i₀
    simp only [h01.symm, ↓reduceIte] at this; rw [this]; ring
  have hexp : (fun y : Fin d → ℝ => (y i₀ - y i₁) ^ 2) =
      fun y => (y i₀ * y i₀ - y i₀ * y i₁) - (y i₁ * y i₀ - y i₁ * y i₁) := by
    funext y; ring
  have hint : ∫ y, (y i₀ - y i₁) ^ 2 ∂μ = 2 * (M2 μ i₀ i₀ - M2 μ i₀ i₁) := by
    have hA : ∫ y, (y i₀ * y i₀ - y i₀ * y i₁) ∂μ = M2 μ i₀ i₀ - M2 μ i₀ i₁ :=
      integral_sub (hM i₀ i₀) (hM i₀ i₁)
    have hB : ∫ y, (y i₁ * y i₀ - y i₁ * y i₁) ∂μ = M2 μ i₁ i₀ - M2 μ i₁ i₁ :=
      integral_sub (hM i₁ i₀) (hM i₁ i₁)
    have hAB : ∫ y, ((y i₀ * y i₀ - y i₀ * y i₁) - (y i₁ * y i₀ - y i₁ * y i₁)) ∂μ =
        ∫ y, (y i₀ * y i₀ - y i₀ * y i₁) ∂μ - ∫ y, (y i₁ * y i₀ - y i₁ * y i₁) ∂μ :=
      integral_sub (f := fun y : Fin d → ℝ => y i₀ * y i₀ - y i₀ * y i₁)
        (g := fun y : Fin d → ℝ => y i₁ * y i₀ - y i₁ * y i₁)
        ((hM i₀ i₀).sub (hM i₀ i₁)) ((hM i₁ i₀).sub (hM i₁ i₁))
    rw [hexp, hAB, hA, hB, h11, h10]; ring
  refine ⟨by rw [hint]; ring, ?_⟩
  have : 0 ≤ ∫ y, (y i₀ - y i₁) ^ 2 ∂μ := integral_nonneg fun y => sq_nonneg _
  linarith

/-! ## Algebra do multinomio reticulado (cap. 4, `thm:dispersion`) -/

/-- Forma quadratica de `aI + b11ᵀ`: `kᵀ(aI + b11ᵀ)k = a Q + b S²`. -/
theorem quadForm_aI_b11 (a b : ℝ) (k : Fin d → ℝ) :
    ∑ i, ∑ j, k i * k j * ((if i = j then a else 0) + b) =
      a * ∑ i, k i ^ 2 + b * (∑ i, k i) ^ 2 := by
  have h1 : ∀ i, ∑ j, k i * k j * ((if i = j then a else 0) + b) =
      a * k i ^ 2 + b * (k i * ∑ j, k j) := by
    intro i
    simp only [mul_add, Finset.sum_add_distrib, mul_ite, mul_zero, Finset.sum_ite_eq,
      Finset.mem_univ, ↓reduceIte, Finset.mul_sum]
    congr 1
    · ring
    · exact Finset.sum_congr rfl fun j _ => by ring
  simp only [h1, Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.sum_mul, sq]

/-- **Limite do multinomio reticulado** (cap. 4): com `M₂ = (α/m) I + (α²/m² - α/m²) 11ᵀ`
(covariancia `α(I/m - 11ᵀ/m²)` mais a media `α/m`), `(1/(2α²)) kᵀM₂k =
S²/(2m²) + (Q - S²/m)/(2mα)`, para `α ≠ 0`, `m ≠ 0`. -/
theorem lattice_limit (α m : ℝ) (hα : α ≠ 0) (hm : m ≠ 0) (k : Fin d → ℝ) :
    (1 / (2 * α ^ 2)) * ∑ i, ∑ j, k i * k j *
        ((if i = j then α / m else 0) + (α ^ 2 / m ^ 2 - α / m ^ 2)) =
      (∑ i, k i) ^ 2 / (2 * m ^ 2) + (∑ i, k i ^ 2 - (∑ i, k i) ^ 2 / m) / (2 * m * α) := by
  rw [quadForm_aI_b11]
  field_simp
  ring

/-- A identidade escalar do plano: `½α⁻²(α(Q/m - S²/m²) + α²S²/m²) =
S²/(2m²) + (Q - S²/m)/(2mα)`. -/
theorem lattice_identity (α m Q S : ℝ) (hα : α ≠ 0) (hm : m ≠ 0) :
    (1 / (2 * α ^ 2)) * (α * (Q / m - S ^ 2 / m ^ 2) + α ^ 2 * S ^ 2 / m ^ 2) =
      S ^ 2 / (2 * m ^ 2) + (Q - S ^ 2 / m) / (2 * m * α) := by
  field_simp
  ring

/-- Sob `S = ∑ k_j = 0`, o limite reticulado e a forma de Gram `(1/(2mα)) kᵀ(I + 11ᵀ)k`
coincidem e valem `Q/(2mα)`. -/
theorem lattice_zero_sum (α m : ℝ) (k : Fin d → ℝ) (hS : ∑ i, k i = 0) :
    (∑ i, k i) ^ 2 / (2 * m ^ 2) + (∑ i, k i ^ 2 - (∑ i, k i) ^ 2 / m) / (2 * m * α) =
        (∑ i, k i ^ 2) / (2 * m * α) ∧
      (1 / (2 * m * α)) * ∑ i, ∑ j, k i * k j * ((if i = j then 1 else 0) + 1) =
        (∑ i, k i ^ 2) / (2 * m * α) := by
  rw [quadForm_aI_b11, hS]
  constructor <;> ring

/-! ## Testemunhas -/

/-- Testemunha do simbolo: `μ = δ_{(1,0)}` em `ℝ²`, `α = 1`. Em `k = (π,0)` o simbolo vale `2`
(a cota superior `2/α²` e atingida) e em `k = (π/2, 0)` vale `1`; logo `σ` nao e constante. -/
theorem witness_symbol :
    symbol (Measure.dirac ![1, 0]) 1 ![π, 0] = 2 ∧
      symbol (Measure.dirac ![1, 0]) 1 ![π / 2, 0] = 1 ∧
      symbol (Measure.dirac ![1, 0]) 1 ![π, 0] ≤ 2 / 1 ^ 2 := by
  refine ⟨?_, ?_, ?_⟩
  · simp [symbol, integral_dirac, dotProduct, Fin.sum_univ_two]
    norm_num
  · simp [symbol, integral_dirac, dotProduct, Fin.sum_univ_two]
  · exact (symbol_bounds _ 1 _).2

/-- Medida de tres pontos `⅓(δ_{(1,0)} + δ_{(0,1)} + δ_{(1,1)})`, invariante pela troca das
coordenadas, com `M₂ = [[2/3,1/3],[1/3,2/3]]` (`a = b = 1/3`, ambos nao nulos). -/
def mu3 : Measure (Fin 2 → ℝ) :=
  (1 / 3 : ENNReal) • (Measure.dirac ![1, 0] + Measure.dirac ![0, 1] + Measure.dirac ![1, 1])

theorem perm_fin_two (σ : Equiv.Perm (Fin 2)) : σ = 1 ∨ σ = Equiv.swap 0 1 := by
  revert σ; decide

theorem mu3_perm : ∀ σ : Equiv.Perm (Fin 2), mu3.map (fun y => y ∘ σ) = mu3 := by
  intro σ
  have hmeas : Measurable (fun y : Fin 2 → ℝ => y ∘ σ) :=
    (continuous_pi fun a => continuous_apply (σ a)).measurable
  rcases perm_fin_two σ with rfl | rfl
  · simp
  · unfold mu3
    rw [Measure.map_smul, Measure.map_add _ _ hmeas, Measure.map_add _ _ hmeas,
      Measure.map_dirac' hmeas, Measure.map_dirac' hmeas, Measure.map_dirac' hmeas]
    have e1 : (![1, 0] : Fin 2 → ℝ) ∘ Equiv.swap 0 1 = ![0, 1] := by
      funext t; fin_cases t <;> simp
    have e2 : (![0, 1] : Fin 2 → ℝ) ∘ Equiv.swap 0 1 = ![1, 0] := by
      funext t; fin_cases t <;> simp
    have e3 : (![1, 1] : Fin 2 → ℝ) ∘ Equiv.swap 0 1 = ![1, 1] := by
      funext t; fin_cases t <;> simp
    rw [e1, e2, e3, add_comm (Measure.dirac ![0, 1])]
    exact hmeas.aemeasurable

theorem mu3_integral (f : (Fin 2 → ℝ) → ℝ) :
    ∫ y, f y ∂mu3 = (1 / 3) * (f ![1, 0] + f ![0, 1] + f ![1, 1]) := by
  have i1 : Integrable f (Measure.dirac ![1, 0]) := integrable_dirac (by simp)
  have i2 : Integrable f (Measure.dirac ![0, 1]) := integrable_dirac (by simp)
  have i3 : Integrable f (Measure.dirac ![1, 1]) := integrable_dirac (by simp)
  unfold mu3
  rw [integral_smul_measure, integral_add_measure (i1.add_measure i2) i3,
    integral_add_measure i1 i2, integral_dirac, integral_dirac, integral_dirac]
  simp [ENNReal.toReal_inv]

/-- Testemunha de `M2_form`: para `mu3`, `M₂ 0 0 = 2/3` e `M₂ 0 1 = 1/3`, logo `a = b = 1/3`
(forma `aI + b11ᵀ` com `a` e `b` nao nulos), e as hipoteses `hperm` valem. -/
theorem witness_M2 :
    (∀ σ : Equiv.Perm (Fin 2), mu3.map (fun y => y ∘ σ) = mu3) ∧
      M2 mu3 0 0 = 2 / 3 ∧ M2 mu3 0 1 = 1 / 3 ∧ M2 mu3 1 1 = 2 / 3 ∧ M2 mu3 1 0 = 1 / 3 := by
  refine ⟨mu3_perm, ?_, ?_, ?_, ?_⟩ <;>
  · simp only [M2]
    rw [mu3_integral]
    simp
    try norm_num

/-- Aplicacao de `M2_form` a `mu3`: a entrada diagonal `M₂ 1 1` e recuperada como `a + b`. -/
example : M2 mu3 1 1 = (M2 mu3 0 0 - M2 mu3 0 1) + M2 mu3 0 1 := by
  have := M2_form mu3 mu3_perm 0 1 (by decide) 1 1
  simpa using this

/-! ## Mutantes provados FALSOS -/

/-- Mutante 1 (sinal trocado na autofuncao, `Δe_k = +σ e_k`): falso para `μ = δ_{(1,0)}`,
`α = 1`, `k = (π,0)`, `x = 0` (daria `2 = -2`). -/
theorem mutant_sign_false :
    ¬ (∀ (μ : Measure (Fin 2 → ℝ)) (α : ℝ) (k x : Fin 2 → ℝ),
      lap μ α (wave k) x = ((symbol μ α k : ℝ) : ℂ) * wave k x) := by
  intro h
  have h1 := h (Measure.dirac ![1, 0]) 1 ![π, 0] 0
  rw [lap_wave, (witness_symbol).1] at h1
  have hw : wave ![π, 0] 0 = 1 := by simp [wave]
  rw [hw] at h1
  norm_num at h1

/-- Mutante 2 (cota `σ ≤ 1/α²`): falso, a testemunha atinge `2/α²`. -/
theorem mutant_bound_half_false :
    ¬ (∀ (μ : Measure (Fin 2 → ℝ)) [IsProbabilityMeasure μ] (α : ℝ) (k : Fin 2 → ℝ),
      symbol μ α k ≤ 1 / α ^ 2) := by
  intro h
  have := h (Measure.dirac ![1, 0]) 1 ![π, 0]
  rw [(witness_symbol).1] at this
  norm_num at this

/-- Mutante 3 (sem "probabilidade"): para `μ = 2 δ_{(1,0)}` a cota `σ ≤ 2/α²` falha
(`σ(π,0) = 4`). -/
theorem mutant_not_probability_false :
    ¬ (∀ (μ : Measure (Fin 2 → ℝ)) [IsFiniteMeasure μ] (α : ℝ) (k : Fin 2 → ℝ),
      symbol μ α k ≤ 2 / α ^ 2) := by
  intro h
  have : IsFiniteMeasure ((2 : ENNReal) • Measure.dirac (![1, 0] : Fin 2 → ℝ)) :=
    ⟨by simp⟩
  have := h ((2 : ENNReal) • Measure.dirac ![1, 0]) 1 ![π, 0]
  simp [symbol, integral_smul_measure, integral_dirac, dotProduct, Fin.sum_univ_two] at this
  norm_num at this

/-- Mutante 4 (desigualdade quadratica invertida, `σ ≥ (1/(2α²))∫(k·y)²`): falso para
`δ_{(1,0)}`, `α = 1`, `k = (π,0)`: `2 < π²/2`. -/
theorem mutant_quadratic_reverse_false :
    ¬ (∀ (μ : Measure (Fin 2 → ℝ)) (α : ℝ) (k : Fin 2 → ℝ),
      (1 / (2 * α ^ 2)) * ∫ y, (k ⬝ᵥ y) ^ 2 ∂μ ≤ symbol μ α k) := by
  intro h
  have := h (Measure.dirac ![1, 0]) 1 ![π, 0]
  rw [(witness_symbol).1] at this
  simp [integral_dirac, dotProduct, Fin.sum_univ_two] at this
  nlinarith [Real.pi_gt_three]

/-- Mutante 5 (`M₂ = aI + b11ᵀ` sem a invariancia `hperm`): falso para `δ_{(1,0)}`, cujo
`M₂ = [[1,0],[0,0]]` tem diagonal nao constante. -/
theorem mutant_no_perm_false :
    ¬ (∀ (μ : Measure (Fin 2 → ℝ)) (i j : Fin 2),
      M2 μ i j = (if i = j then M2 μ 0 0 - M2 μ 0 1 else 0) + M2 μ 0 1) := by
  intro h
  have := h (Measure.dirac ![1, 0]) 1 1
  simp [M2, integral_dirac] at this

/-- Mutante 6 (`b = 0`, isto e `M₂` escalar): falso para `mu3`. -/
theorem mutant_scalar_false : ¬ (M2 mu3 0 1 = 0) := by
  rw [witness_M2.2.2.1]; norm_num

/-- Mutante 7 (cap. 4: a forma de Gram vale sem `S = 0`): falso para `m = 2`, `α = 1`,
`k = (1,0)`: limite reticulado `1/4`, forma de Gram `1/2`. -/
theorem mutant_gram_without_zero_sum_false :
    ¬ (∀ (α m : ℝ) (k : Fin 2 → ℝ), α ≠ 0 → m ≠ 0 →
      (∑ i, k i) ^ 2 / (2 * m ^ 2) + (∑ i, k i ^ 2 - (∑ i, k i) ^ 2 / m) / (2 * m * α) =
        (1 / (2 * m * α)) * ∑ i, ∑ j, k i * k j * ((if i = j then 1 else 0) + 1)) := by
  intro h
  have := h 1 2 ![1, 0] one_ne_zero two_ne_zero
  rw [quadForm_aI_b11] at this
  simp [Fin.sum_univ_two] at this
  norm_num at this

end LeanReal.Chap04Symbol

#print axioms LeanReal.Chap04Symbol.bracket
#print axioms LeanReal.Chap04Symbol.lap_wave
#print axioms LeanReal.Chap04Symbol.symbol_even
#print axioms LeanReal.Chap04Symbol.symbol_bounds
#print axioms LeanReal.Chap04Symbol.symbol_re_form
#print axioms LeanReal.Chap04Symbol.symbol_le_quadratic
#print axioms LeanReal.Chap04Symbol.symbol_quartic
#print axioms LeanReal.Chap04Symbol.quadratic_eq_M2
#print axioms LeanReal.Chap04Symbol.perm_invariant_form
#print axioms LeanReal.Chap04Symbol.M2_form
#print axioms LeanReal.Chap04Symbol.M2_a_nonneg
#print axioms LeanReal.Chap04Symbol.quadForm_aI_b11
#print axioms LeanReal.Chap04Symbol.lattice_limit
#print axioms LeanReal.Chap04Symbol.lattice_identity
#print axioms LeanReal.Chap04Symbol.lattice_zero_sum
#print axioms LeanReal.Chap04Symbol.witness_symbol
#print axioms LeanReal.Chap04Symbol.mu3_perm
#print axioms LeanReal.Chap04Symbol.mu3_integral
#print axioms LeanReal.Chap04Symbol.witness_M2
#print axioms LeanReal.Chap04Symbol.mutant_sign_false
#print axioms LeanReal.Chap04Symbol.mutant_bound_half_false
#print axioms LeanReal.Chap04Symbol.mutant_not_probability_false
#print axioms LeanReal.Chap04Symbol.mutant_quadratic_reverse_false
#print axioms LeanReal.Chap04Symbol.mutant_no_perm_false
#print axioms LeanReal.Chap04Symbol.mutant_scalar_false
#print axioms LeanReal.Chap04Symbol.mutant_gram_without_zero_sum_false
