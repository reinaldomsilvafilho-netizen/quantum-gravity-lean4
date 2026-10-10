import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.SpecialFunctions.Complex.Arg
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
import Mathlib.Algebra.Order.Chebyshev
import Mathlib.Tactic.Module

/-!
# Capitulo 7: cotas algebricas (lote B4 do `PLANO_LIVRO_B.md`)

Fonte: `unified_quantum_gravity_book/chap07_minimax_extrinsic_curvature_submanifolds.tex`.

## Conteudo e reducoes declaradas

1. `prop:gauss_bonnet_floor` (secoes 1–2). Nucleo pontual COMPLETO: num referencial ortonormal
   `(e₁,e₂)`, `II` e dada por tres vetores normais `h11 h12 h22 ∈ N` (`N` espaco com produto
   interno real qualquer = espaco normal); `‖II‖_{L^∞} ≤ κ` e lida como `|II(v,v)| ≤ κ` para todo
   `v` unitario (a norma operador do capitulo, cf. a conta do toro produto); `K` e definida pela
   equacao de Gauss. Provados: `|II(e₁,e₂)| ≤ κ` (polarizacao), `-2κ² ≤ K ≤ κ²` e, em codimensao
   um (`N = ℝ`), `K ≥ -κ²` (sem diagonalizar). Passo integral: a superficie e um espaco de medida
   finita `(M, μ)` de area `A = μ(M)`; o teorema de Gauss–Bonnet `∫ K = 2πχ` entra como HIPOTESE
   `hGB` (Mathlib nao tem superficies, segunda forma fundamental nem Gauss–Bonnet), e tambem a
   integrabilidade `hKint`. NAO formalizado: que `(M, μ, h)` venha de uma superficie `C²`.
2. `thm:scaling_law` (secao 3). (1) o circulo diagonal em `ℂ^m = EuclideanSpace ℂ (Fin m)`,
   com derivadas, velocidade, curvatura, projecoes e `γ'' = -ω²γ`. (2) a cota inferior, pontual
   e para curvas (`C²` substituida por "duas vezes derivavel em `s`"), e o caso de IGUALDADE
   (iff). A curvatura de `P_jγ` e a formula classica `(x'y'' - y'x'')/|v|³`.
3. `thm:monotonicity` (secao 4), so CURVAS (`k = 1`): a classe admissivel e a de curvas por
   comprimento de arco, duas vezes derivaveis em `[0,ℓ]` (derivadas bilaterais nas pontas), em
   `K` (papel de `Ω̄`), comprimento `≤ V`, pontas `p, q` (`Σ = {p,q}`). Forma abstrata para
   qualquer isometria linear e forma do livro com `i(x) = (x,0)`, `ℝⁿ → ℝ^{n+1}`, e o cilindro
   `K × [-d,d]` (o fecho de `Ω × (-d,d)` quando `K = Ω̄`, `d > 0`; essa identidade de fechos NAO
   e provada). O infimo e `sInf` real com classe nao vazia (o livro: `inf ∅ = +∞`).
4. `prop:knot_gap` (secao 5), CONDICIONAL: Fary–Milnor (curvatura total `> 4π` para curvas de
   tipo `K`) e Fenchel (`≥ 2π`) entram como hipoteses; o tipo de no e um predicado abstrato
   `IsK`. Provados: `∫|κ| ≤ ℓ‖κ‖_∞`, as cotas por curva, `κ*_Imm(L) = 2π/L` (circulo) e
   `κ*_K(L) ≥ 4π/L = κ*_Imm(L) + 2π/L`. NAO formalizado: a afirmacao sobre classes de homotopia
   regular.
5. Tabela `tab:universal_classification` e observacao "Calibration does not force isotropy"
   (secao 6): `‖II‖_op = √m/R` do toro produto a partir da formula `II(v,v)_j = v_j²/r` do livro
   (a derivacao dessa formula a partir da imersao NAO e formalizada); para a curva complexa,
   `|II(v,v)| = |a|`, `‖II‖_F = 2|a|`, e a isotropia `‖II‖_op = ‖II‖_F/√2` e falsa.

Sem lacunas nem axiomas extras. Testemunhas nao degeneradas (com igualdade nas cotas) e mutantes
provados falsos em cada secao.
-/

noncomputable section

namespace LeanReal.Chap07Bounds

open Set Real MeasureTheory

/-! ## 1. `prop:gauss_bonnet_floor`: nucleo pontual -/

section Pointwise

variable {N : Type*} [NormedAddCommGroup N] [InnerProductSpace ℝ N]

/-- A segunda forma fundamental `II(v,v)` de uma superficie, num referencial ortonormal
`(e₁,e₂)` do plano tangente: para `v = v₁e₁ + v₂e₂`,
`II(v,v) = v₁² II(e₁,e₁) + 2v₁v₂ II(e₁,e₂) + v₂² II(e₂,e₂)`, com valores no espaco normal `N`. -/
def IIq (h11 h12 h22 : N) (v1 v2 : ℝ) : N :=
  (v1 ^ 2) • h11 + (2 * v1 * v2) • h12 + (v2 ^ 2) • h22

/-- Curvatura de Gauss pela equacao de Gauss (`prop:gauss_bonnet_floor`, prova):
`K = ⟨II(e₁,e₁), II(e₂,e₂)⟩ - |II(e₁,e₂)|²`. -/
def gaussK (h11 h12 h22 : N) : ℝ := inner ℝ h11 h22 - ‖h12‖ ^ 2

@[simp] theorem IIq_one_zero (h11 h12 h22 : N) : IIq h11 h12 h22 1 0 = h11 := by
  simp [IIq]

@[simp] theorem IIq_zero_one (h11 h12 h22 : N) : IIq h11 h12 h22 0 1 = h22 := by
  simp [IIq]

/-- Polarizacao (`prop:gauss_bonnet_floor`, prova): `|II(v,v)| ≤ κ` para todo `v` unitario
implica `|II(e₁,e₂)| ≤ κ`. -/
theorem norm_h12_le {h11 h12 h22 : N} {κ : ℝ}
    (hop : ∀ v1 v2 : ℝ, v1 ^ 2 + v2 ^ 2 = 1 → ‖IIq h11 h12 h22 v1 v2‖ ≤ κ) : ‖h12‖ ≤ κ := by
  set s : ℝ := √(1 / 2) with hs
  have hs2 : s ^ 2 = 1 / 2 := Real.sq_sqrt (by norm_num)
  have hunit1 : s ^ 2 + s ^ 2 = 1 := by rw [hs2]; norm_num
  have hunit2 : s ^ 2 + (-s) ^ 2 = 1 := by rw [neg_sq, hs2]; norm_num
  have e : (2 : ℝ) • h12 = IIq h11 h12 h22 s s - IIq h11 h12 h22 s (-s) := by
    have h2s : 2 * s * s = 1 := by nlinarith [hs2]
    have h2s' : 2 * s * (-s) = -1 := by nlinarith [hs2]
    simp only [IIq, neg_sq, hs2, h2s, h2s']
    module
  have h := norm_sub_le (IIq h11 h12 h22 s s) (IIq h11 h12 h22 s (-s))
  rw [← e, norm_smul, Real.norm_two] at h
  linarith [hop s s hunit1, hop s (-s) hunit2]

/-- Cota superior pontual: `K ≤ κ²`. -/
theorem gaussK_le {h11 h12 h22 : N} {κ : ℝ}
    (hop : ∀ v1 v2 : ℝ, v1 ^ 2 + v2 ^ 2 = 1 → ‖IIq h11 h12 h22 v1 v2‖ ≤ κ) :
    gaussK h11 h12 h22 ≤ κ ^ 2 := by
  have h1 : ‖h11‖ ≤ κ := by simpa using hop 1 0 (by norm_num)
  have h2 : ‖h22‖ ≤ κ := by simpa using hop 0 1 (by norm_num)
  have hi := real_inner_le_norm h11 h22
  have : ‖h11‖ * ‖h22‖ ≤ κ * κ :=
    mul_le_mul h1 h2 (norm_nonneg _) (le_trans (norm_nonneg _) h1)
  unfold gaussK
  nlinarith [sq_nonneg ‖h12‖]

/-- Cota inferior pontual em codimensao qualquer: `K ≥ -2κ²`. -/
theorem neg_two_mul_le_gaussK {h11 h12 h22 : N} {κ : ℝ}
    (hop : ∀ v1 v2 : ℝ, v1 ^ 2 + v2 ^ 2 = 1 → ‖IIq h11 h12 h22 v1 v2‖ ≤ κ) :
    -2 * κ ^ 2 ≤ gaussK h11 h12 h22 := by
  have h1 : ‖h11‖ ≤ κ := by simpa using hop 1 0 (by norm_num)
  have h2 : ‖h22‖ ≤ κ := by simpa using hop 0 1 (by norm_num)
  have h3 := norm_h12_le hop
  have hk : 0 ≤ κ := le_trans (norm_nonneg _) h1
  have hi : -(‖h11‖ * ‖h22‖) ≤ inner ℝ h11 h22 := by
    have := abs_real_inner_le_norm h11 h22
    linarith [neg_abs_le (inner ℝ h11 h22)]
  have : ‖h11‖ * ‖h22‖ ≤ κ * κ := mul_le_mul h1 h2 (norm_nonneg _) hk
  have : ‖h12‖ ^ 2 ≤ κ ^ 2 := pow_le_pow_left₀ (norm_nonneg _) h3 2
  unfold gaussK
  nlinarith

/-- Cota inferior pontual em CODIMENSAO UM (`N = ℝ`): `K = κ₁κ₂ ≥ -κ²`. O livro usa as
curvaturas principais; aqui, sem diagonalizar, usa-se o par ortonormal `(u, u⊥)` com
`u = (cos t, sin t)`, `2t = arg(α + i b)`, `α = (a - c)/2`, em que
`II(u,u) - II(u⊥,u⊥) = 2√(α² + b²)`. -/
theorem neg_sq_le_gaussK_real {a b c κ : ℝ}
    (hop : ∀ v1 v2 : ℝ, v1 ^ 2 + v2 ^ 2 = 1 → ‖IIq a b c v1 v2‖ ≤ κ) :
    -κ ^ 2 ≤ gaussK a b c := by
  have hop' : ∀ v1 v2 : ℝ, v1 ^ 2 + v2 ^ 2 = 1 →
      |v1 ^ 2 * a + 2 * v1 * v2 * b + v2 ^ 2 * c| ≤ κ := by
    intro v1 v2 h; simpa [IIq, Real.norm_eq_abs, smul_eq_mul] using hop v1 v2 h
  have hK : gaussK a b c = a * c - b ^ 2 := by
    simp [gaussK, Real.norm_eq_abs, sq_abs, mul_comm]
  rw [hK]
  set α : ℝ := (a - c) / 2 with hα
  set z : ℂ := ⟨α, b⟩ with hz
  have hk : 0 ≤ κ := le_trans (abs_nonneg _) (hop' 1 0 (by norm_num))
  -- r = ‖z‖ ≤ κ
  have hr : ‖z‖ ≤ κ := by
    by_cases hz0 : z = 0
    · rw [hz0, norm_zero]; exact hk
    set t : ℝ := Complex.arg z / 2 with ht
    have hc2 : Real.cos t ^ 2 - Real.sin t ^ 2 = α / ‖z‖ := by
      have := Complex.cos_arg hz0
      rw [show Complex.arg z = 2 * t by rw [ht]; ring, Real.cos_two_mul] at this
      have hs := Real.sin_sq_add_cos_sq t
      simp only [hz] at this ⊢
      nlinarith [this]
    have hs2 : 2 * Real.sin t * Real.cos t = b / ‖z‖ := by
      have := Complex.sin_arg z
      rw [show Complex.arg z = 2 * t by rw [ht]; ring, Real.sin_two_mul] at this
      simpa [hz] using this
    have hu1 : Real.cos t ^ 2 + Real.sin t ^ 2 = 1 := by rw [add_comm]; exact Real.sin_sq_add_cos_sq t
    have hu2 : (-Real.sin t) ^ 2 + Real.cos t ^ 2 = 1 := by rw [neg_sq]; exact Real.sin_sq_add_cos_sq t
    have A := hop' (Real.cos t) (Real.sin t) hu1
    have B := hop' (-Real.sin t) (Real.cos t) hu2
    have hdiff : (Real.cos t ^ 2 * a + 2 * Real.cos t * Real.sin t * b + Real.sin t ^ 2 * c) -
        ((-Real.sin t) ^ 2 * a + 2 * (-Real.sin t) * Real.cos t * b + Real.cos t ^ 2 * c) =
        2 * ‖z‖ := by
      have hzpos : 0 < ‖z‖ := norm_pos_iff.mpr hz0
      have hnz : ‖z‖ ^ 2 = α ^ 2 + b ^ 2 := by
        rw [Complex.sq_norm, Complex.normSq_apply]; simp [hz]; ring
      have e1 : (Real.cos t ^ 2 * a + 2 * Real.cos t * Real.sin t * b + Real.sin t ^ 2 * c) -
          ((-Real.sin t) ^ 2 * a + 2 * (-Real.sin t) * Real.cos t * b + Real.cos t ^ 2 * c) =
          2 * α * (Real.cos t ^ 2 - Real.sin t ^ 2) + 2 * b * (2 * Real.sin t * Real.cos t) := by
        rw [hα]; ring
      rw [e1, hc2, hs2]
      field_simp
      nlinarith [hnz]
    have := abs_le.mp A
    have := abs_le.mp B
    linarith
  have hnz : ‖z‖ ^ 2 = α ^ 2 + b ^ 2 := by
    rw [Complex.sq_norm, Complex.normSq_apply]; simp [hz]; ring
  have : ‖z‖ ^ 2 ≤ κ ^ 2 := pow_le_pow_left₀ (norm_nonneg _) hr 2
  have e : a * c - b ^ 2 = ((a + c) / 2) ^ 2 - (α ^ 2 + b ^ 2) := by rw [hα]; ring
  rw [e]
  nlinarith [sq_nonneg ((a + c) / 2)]

end Pointwise

/-! ## 2. `prop:gauss_bonnet_floor`: passo integral, condicional a Gauss–Bonnet -/

section Integral

variable {N : Type*} [NormedAddCommGroup N] [InnerProductSpace ℝ N]
variable {M : Type*} [MeasurableSpace M]

/-- `∫ K ≤ A κ²`. -/
theorem integral_gaussK_le (μ : Measure M) [IsFiniteMeasure μ] (h11 h12 h22 : M → N) (κ : ℝ)
    (hop : ∀ x v1 v2, v1 ^ 2 + v2 ^ 2 = 1 → ‖IIq (h11 x) (h12 x) (h22 x) v1 v2‖ ≤ κ)
    (hKint : Integrable (fun x => gaussK (h11 x) (h12 x) (h22 x)) μ) :
    ∫ x, gaussK (h11 x) (h12 x) (h22 x) ∂μ ≤ μ.real univ * κ ^ 2 := by
  have := integral_mono hKint (integrable_const (κ ^ 2)) (fun x => gaussK_le (hop x))
  simpa [integral_const, smul_eq_mul] using this

/-- `A (-2κ²) ≤ ∫ K`. -/
theorem le_integral_gaussK (μ : Measure M) [IsFiniteMeasure μ] (h11 h12 h22 : M → N) (κ : ℝ)
    (hop : ∀ x v1 v2, v1 ^ 2 + v2 ^ 2 = 1 → ‖IIq (h11 x) (h12 x) (h22 x) v1 v2‖ ≤ κ)
    (hKint : Integrable (fun x => gaussK (h11 x) (h12 x) (h22 x)) μ) :
    μ.real univ * (-2 * κ ^ 2) ≤ ∫ x, gaussK (h11 x) (h12 x) (h22 x) ∂μ := by
  have := integral_mono (integrable_const (-2 * κ ^ 2)) hKint
    (fun x => neg_two_mul_le_gaussK (hop x))
  simpa [integral_const, smul_eq_mul] using this

/-- Codimensao um: `A (-κ²) ≤ ∫ K`. -/
theorem le_integral_gaussK_real (μ : Measure M) [IsFiniteMeasure μ] (h11 h12 h22 : M → ℝ)
    (κ : ℝ)
    (hop : ∀ x v1 v2, v1 ^ 2 + v2 ^ 2 = 1 → ‖IIq (h11 x) (h12 x) (h22 x) v1 v2‖ ≤ κ)
    (hKint : Integrable (fun x => gaussK (h11 x) (h12 x) (h22 x)) μ) :
    μ.real univ * (-κ ^ 2) ≤ ∫ x, gaussK (h11 x) (h12 x) (h22 x) ∂μ := by
  have := integral_mono (integrable_const (-κ ^ 2)) hKint
    (fun x => neg_sq_le_gaussK_real (hop x))
  simpa [integral_const, smul_eq_mul] using this

omit [InnerProductSpace ℝ N] in
/-- Area positiva da um ponto, logo `κ ≥ 0`. -/
theorem nonneg_of_hop (μ : Measure M) (h11 : M → N) (κ : ℝ) (hA : 0 < μ.real univ)
    (hop : ∀ x, ‖h11 x‖ ≤ κ) : 0 ≤ κ := by
  have hne : (univ : Set M).Nonempty :=
    nonempty_of_measure_ne_zero (μ := μ) (fun h : μ univ = 0 => by simp [Measure.real, h] at hA)
  obtain ⟨x, -⟩ := hne
  exact le_trans (norm_nonneg _) (hop x)

/-- **`prop:gauss_bonnet_floor`, caso `χ > 0`**, condicional ao teorema de Gauss–Bonnet.
Dados: uma "superficie" `(M, μ)` de area `A = μ(M) > 0` (medida finita) e, em cada ponto, a
segunda forma fundamental num referencial ortonormal (`h11 h12 h22 : M → N`) com
`|II(v,v)| ≤ κ` para todo `v` unitario (isto e `‖II‖_{L^∞} ≤ κ` na norma operador do
capitulo). Hipotese que substitui teoria ausente na Mathlib: `hGB : ∫ K dμ = 2πχ`
(Gauss–Bonnet), com `K` dada pela equacao de Gauss. Conclusao: `κ ≥ √(2πχ/A)` (para
`χ ≤ 0` e trivial, pois `√` de um numero nao positivo e `0`; a forma do livro, com `χ > 0`, e
`gauss_bonnet_floor_pos`). -/
theorem gauss_bonnet_floor_any_sign (μ : Measure M) [IsFiniteMeasure μ]
    (h11 h12 h22 : M → N) (κ : ℝ) (χ : ℤ) (hA : 0 < μ.real univ)
    (hop : ∀ x v1 v2, v1 ^ 2 + v2 ^ 2 = 1 → ‖IIq (h11 x) (h12 x) (h22 x) v1 v2‖ ≤ κ)
    (hKint : Integrable (fun x => gaussK (h11 x) (h12 x) (h22 x)) μ)
    (hGB : ∫ x, gaussK (h11 x) (h12 x) (h22 x) ∂μ = 2 * π * χ) :
    √(2 * π * χ / μ.real univ) ≤ κ := by
  have hk := nonneg_of_hop μ h11 κ hA (fun x => by simpa using hop x 1 0 (by norm_num))
  have h := integral_gaussK_le μ h11 h12 h22 κ hop hKint
  rw [hGB] at h
  calc √(2 * π * χ / μ.real univ) ≤ √(κ ^ 2) :=
        Real.sqrt_le_sqrt (by rw [div_le_iff₀ hA]; linarith)
    _ = κ := Real.sqrt_sq hk

/-- A forma literal do livro (`χ > 0`). A hipotese `χ > 0` nao e usada: para `χ ≤ 0` o lado
esquerdo e `√(nao positivo) = 0` (ver `gauss_bonnet_floor_any_sign`). -/
theorem gauss_bonnet_floor_pos (μ : Measure M) [IsFiniteMeasure μ] (h11 h12 h22 : M → N)
    (κ : ℝ) (χ : ℤ) (hA : 0 < μ.real univ)
    (hop : ∀ x v1 v2, v1 ^ 2 + v2 ^ 2 = 1 → ‖IIq (h11 x) (h12 x) (h22 x) v1 v2‖ ≤ κ)
    (hKint : Integrable (fun x => gaussK (h11 x) (h12 x) (h22 x)) μ)
    (hGB : ∫ x, gaussK (h11 x) (h12 x) (h22 x) ∂μ = 2 * π * χ) (_hχ : 0 < χ) :
    √(2 * π * χ / μ.real univ) ≤ κ :=
  gauss_bonnet_floor_any_sign μ h11 h12 h22 κ χ hA hop hKint hGB

/-- **`prop:gauss_bonnet_floor`, caso `χ < 0`, codimensao qualquer**, condicional a
Gauss–Bonnet (`hGB`): `κ ≥ √(π|χ|/A)`. -/
theorem gauss_bonnet_floor_neg (μ : Measure M) [IsFiniteMeasure μ] (h11 h12 h22 : M → N)
    (κ : ℝ) (χ : ℤ) (hA : 0 < μ.real univ)
    (hop : ∀ x v1 v2, v1 ^ 2 + v2 ^ 2 = 1 → ‖IIq (h11 x) (h12 x) (h22 x) v1 v2‖ ≤ κ)
    (hKint : Integrable (fun x => gaussK (h11 x) (h12 x) (h22 x)) μ)
    (hGB : ∫ x, gaussK (h11 x) (h12 x) (h22 x) ∂μ = 2 * π * χ) (hχ : χ < 0) :
    √(π * |(χ : ℝ)| / μ.real univ) ≤ κ := by
  have hk := nonneg_of_hop μ h11 κ hA (fun x => by simpa using hop x 1 0 (by norm_num))
  have h := le_integral_gaussK μ h11 h12 h22 κ hop hKint
  rw [hGB] at h
  have hχr : (χ : ℝ) < 0 := by exact_mod_cast hχ
  rw [abs_of_neg hχr]
  calc √(π * -(χ : ℝ) / μ.real univ) ≤ √(κ ^ 2) :=
        Real.sqrt_le_sqrt (by rw [div_le_iff₀ hA]; nlinarith [Real.pi_pos])
    _ = κ := Real.sqrt_sq hk

/-- **`prop:gauss_bonnet_floor`, caso `χ < 0` em codimensao um** (`N = ℝ`, superficies em
`ℝ³`), condicional a Gauss–Bonnet: `κ ≥ √(2π|χ|/A)`. -/
theorem gauss_bonnet_floor_neg_codim_one (μ : Measure M) [IsFiniteMeasure μ]
    (h11 h12 h22 : M → ℝ) (κ : ℝ) (χ : ℤ) (hA : 0 < μ.real univ)
    (hop : ∀ x v1 v2, v1 ^ 2 + v2 ^ 2 = 1 → ‖IIq (h11 x) (h12 x) (h22 x) v1 v2‖ ≤ κ)
    (hKint : Integrable (fun x => gaussK (h11 x) (h12 x) (h22 x)) μ)
    (hGB : ∫ x, gaussK (h11 x) (h12 x) (h22 x) ∂μ = 2 * π * χ) (hχ : χ < 0) :
    √(2 * π * |(χ : ℝ)| / μ.real univ) ≤ κ := by
  have hk := nonneg_of_hop μ h11 κ hA (fun x => by simpa using hop x 1 0 (by norm_num))
  have h := le_integral_gaussK_real μ h11 h12 h22 κ hop hKint
  rw [hGB] at h
  have hχr : (χ : ℝ) < 0 := by exact_mod_cast hχ
  rw [abs_of_neg hχr]
  calc √(2 * π * -(χ : ℝ) / μ.real univ) ≤ √(κ ^ 2) :=
        Real.sqrt_le_sqrt (by rw [div_le_iff₀ hA]; nlinarith [Real.pi_pos])
    _ = κ := Real.sqrt_sq hk

end Integral

/-! ### Testemunhas de nao-vacuidade (todas com IGUALDADE na cota) e mutantes

Modelo de "superficie": `M = ℝ` com `μ = volume` restrita a `[0, A]` (area `A`) e dados
pontuais constantes. A hipotese `hGB` e entao uma conta de integral; cada testemunha mostra que
as hipoteses sao satisfaziveis e que a cota e atingida. -/

section Witnesses

/-- Medida de area `A` em `ℝ`. -/
def areaMeasure (A : ℝ) : Measure ℝ := volume.restrict (Icc 0 A)

/-- `areaMeasure A` e finita. -/
instance (A : ℝ) : IsFiniteMeasure (areaMeasure A) :=
  isFiniteMeasure_restrict.mpr measure_Icc_lt_top.ne

/-- A area total de `areaMeasure A` e `A`. -/
theorem areaMeasure_real_univ {A : ℝ} (hA : 0 ≤ A) : (areaMeasure A).real univ = A := by
  rw [areaMeasure, measureReal_restrict_apply_univ, Real.volume_real_Icc_of_le hA, sub_zero]

/-- Integral de uma constante: `A c`. -/
theorem integral_areaMeasure_const {A : ℝ} (hA : 0 ≤ A) (c : ℝ) :
    ∫ _ : ℝ, c ∂(areaMeasure A) = A * c := by
  rw [integral_const, areaMeasure_real_univ hA, smul_eq_mul]

/-- **Testemunha 1 (esfera redonda de raio `r`, codimensao um).** Dados pontuais da esfera:
`II = (1/r) Id`, `K = 1/r²`, area `4πr²`, `χ = 2`. As hipoteses de `gauss_bonnet_floor_pos`
valem com `κ = 1/r`, e a cota e atingida: `√(2πχ/A) = 1/r`. -/
theorem witness_round_sphere (r : ℝ) (hr : 0 < r) :
    (∀ (x : ℝ) (v1 v2 : ℝ), v1 ^ 2 + v2 ^ 2 = 1 →
      ‖IIq ((fun _ : ℝ => 1 / r) x) ((fun _ : ℝ => (0 : ℝ)) x) ((fun _ : ℝ => 1 / r) x) v1 v2‖
        ≤ 1 / r) ∧
    0 < (areaMeasure (4 * π * r ^ 2)).real univ ∧
    ∫ x, gaussK ((fun _ : ℝ => 1 / r) x) ((fun _ : ℝ => (0 : ℝ)) x) ((fun _ : ℝ => 1 / r) x)
      ∂(areaMeasure (4 * π * r ^ 2)) = 2 * π * ((2 : ℤ) : ℝ) ∧
    √(2 * π * ((2 : ℤ) : ℝ) / (areaMeasure (4 * π * r ^ 2)).real univ) = 1 / r := by
  have hA : 0 ≤ 4 * π * r ^ 2 := by positivity
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro _ v1 v2 h
    have : IIq (1 / r) (0 : ℝ) (1 / r) v1 v2 = 1 / r := by
      simp only [IIq, smul_eq_mul]
      calc v1 ^ 2 * (1 / r) + 2 * v1 * v2 * 0 + v2 ^ 2 * (1 / r)
          = (v1 ^ 2 + v2 ^ 2) * (1 / r) := by ring
        _ = 1 / r := by rw [h, one_mul]
    simp only [this, Real.norm_eq_abs, abs_of_pos (one_div_pos.mpr hr), le_refl]
  · rw [areaMeasure_real_univ hA]; positivity
  · have : gaussK (1 / r) (0 : ℝ) (1 / r) = 1 / r ^ 2 := by
      simp only [gaussK, Real.inner_apply, norm_zero]; ring
    beta_reduce; rw [this, integral_areaMeasure_const hA]
    field_simp
    push_cast; ring
  · rw [areaMeasure_real_univ hA]
    have : 2 * π * ((2 : ℤ) : ℝ) / (4 * π * r ^ 2) = (1 / r) ^ 2 := by
      field_simp; push_cast; ring
    rw [this, Real.sqrt_sq (one_div_pos.mpr hr).le]

/-- Dados pontuais de uma curva complexa em `ℂ²` (observacao "Calibration does not force
isotropy"), com `a = 1`: `II(e₁,e₁) = 1`, `II(e₁,Je₁) = i`, `II(Je₁,Je₁) = -1`, no plano normal
`N = ℂ`. Entao `II(v,v) = (v₁ + i v₂)²`. -/
theorem IIq_complex_curve (v1 v2 : ℝ) :
    IIq (1 : ℂ) Complex.I (-1) v1 v2 = ((v1 : ℂ) + v2 * Complex.I) ^ 2 := by
  apply Complex.ext <;> simp [IIq, pow_two] <;> ring

/-- Para `v` unitario, `|II(v,v)| = 1` (dados da curva complexa). -/
theorem norm_IIq_complex_curve (v1 v2 : ℝ) (h : v1 ^ 2 + v2 ^ 2 = 1) :
    ‖IIq (1 : ℂ) Complex.I (-1) v1 v2‖ = 1 := by
  rw [IIq_complex_curve, norm_pow]
  have : ‖(v1 : ℂ) + v2 * Complex.I‖ = 1 := by
    have h2 : ‖(v1 : ℂ) + v2 * Complex.I‖ ^ 2 = 1 := by
      rw [Complex.sq_norm, Complex.normSq_apply]; simp; nlinarith [h]
    have h0 := norm_nonneg ((v1 : ℂ) + v2 * Complex.I)
    nlinarith [h2, h0]
  rw [this, one_pow]

/-- `K = -2` para os dados da curva complexa. -/
theorem gaussK_complex_curve : gaussK (1 : ℂ) Complex.I (-1) = -2 := by
  simp [gaussK]; norm_num

/-- **Testemunha 2 (codimensao dois, `χ < 0`).** Dados da curva complexa (`K = -2`, `κ = 1`),
area `A = π` e `χ = -1`: as hipoteses de `gauss_bonnet_floor_neg` valem e a cota e atingida,
`√(π|χ|/A) = 1`. Pontualmente `K = -2κ²`: a cota `-2κ²` e otima. -/
theorem witness_codim_two :
    (∀ (x : ℝ) (v1 v2 : ℝ), v1 ^ 2 + v2 ^ 2 = 1 →
      ‖IIq ((fun _ : ℝ => (1 : ℂ)) x) ((fun _ : ℝ => Complex.I) x) ((fun _ : ℝ => (-1 : ℂ)) x)
        v1 v2‖ ≤ 1) ∧
    0 < (areaMeasure π).real univ ∧
    ∫ x, gaussK ((fun _ : ℝ => (1 : ℂ)) x) ((fun _ : ℝ => Complex.I) x)
      ((fun _ : ℝ => (-1 : ℂ)) x) ∂(areaMeasure π) = 2 * π * ((-1 : ℤ) : ℝ) ∧
    √(π * |((-1 : ℤ) : ℝ)| / (areaMeasure π).real univ) = 1 := by
  refine ⟨fun _ v1 v2 h => (norm_IIq_complex_curve v1 v2 h).le, ?_, ?_, ?_⟩
  · rw [areaMeasure_real_univ Real.pi_pos.le]; exact Real.pi_pos
  · simp only [gaussK_complex_curve]
    rw [integral_areaMeasure_const Real.pi_pos.le]; push_cast; ring
  · rw [areaMeasure_real_univ Real.pi_pos.le]
    have : π * |((-1 : ℤ) : ℝ)| / π = 1 := by
      push_cast; rw [abs_neg, abs_one, mul_one, div_self Real.pi_ne_zero]
    rw [this, Real.sqrt_one]

/-- **Testemunha 3 (sela em codimensao um, `χ < 0`).** `II = diag(1,-1)`, `K = -1 = -κ²`,
area `2π`, `χ = -1`: hipoteses de `gauss_bonnet_floor_neg_codim_one` e igualdade
`√(2π|χ|/A) = 1`. -/
theorem witness_saddle_codim_one :
    (∀ (x : ℝ) (v1 v2 : ℝ), v1 ^ 2 + v2 ^ 2 = 1 →
      ‖IIq ((fun _ : ℝ => (1 : ℝ)) x) ((fun _ : ℝ => (0 : ℝ)) x) ((fun _ : ℝ => (-1 : ℝ)) x)
        v1 v2‖ ≤ 1) ∧
    0 < (areaMeasure (2 * π)).real univ ∧
    ∫ x, gaussK ((fun _ : ℝ => (1 : ℝ)) x) ((fun _ : ℝ => (0 : ℝ)) x)
      ((fun _ : ℝ => (-1 : ℝ)) x) ∂(areaMeasure (2 * π)) = 2 * π * ((-1 : ℤ) : ℝ) ∧
    √(2 * π * |((-1 : ℤ) : ℝ)| / (areaMeasure (2 * π)).real univ) = 1 := by
  have hA : (0 : ℝ) ≤ 2 * π := by positivity
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro _ v1 v2 h
    simp only [IIq, smul_eq_mul, Real.norm_eq_abs]
    rw [abs_le]; constructor <;> nlinarith [sq_nonneg v1, sq_nonneg v2]
  · rw [areaMeasure_real_univ hA]; positivity
  · have : gaussK (1 : ℝ) 0 (-1) = -1 := by
      simp only [gaussK, Real.inner_apply, norm_zero]; ring
    beta_reduce; rw [this, integral_areaMeasure_const hA]; push_cast; ring
  · rw [areaMeasure_real_univ hA]
    have : 2 * π * |((-1 : ℤ) : ℝ)| / (2 * π) = 1 := by
      push_cast; rw [abs_neg, abs_one, mul_one, div_self (by positivity)]
    rw [this, Real.sqrt_one]

/-- Aplicacao do teorema a testemunha 1 (os tipos casam). -/
example (r : ℝ) (hr : 0 < r) :
    √(2 * π * ((2 : ℤ) : ℝ) / (areaMeasure (4 * π * r ^ 2)).real univ) ≤ 1 / r := by
  obtain ⟨hop, hA, hGB, -⟩ := witness_round_sphere r hr
  exact gauss_bonnet_floor_pos (areaMeasure (4 * π * r ^ 2)) (fun _ => 1 / r) (fun _ => 0)
    (fun _ => 1 / r) (1 / r) 2 hA hop (integrable_const _) hGB (by norm_num)

/-- **Mutante 1 (pontual):** a cota de codimensao um `K ≥ -κ²` e FALSA em codimensao dois
(curva complexa: `K = -2`, `κ = 1`). -/
theorem mutant_codim_one_pointwise_false :
    ¬ (∀ (h11 h12 h22 : ℂ) (κ : ℝ),
        (∀ v1 v2 : ℝ, v1 ^ 2 + v2 ^ 2 = 1 → ‖IIq h11 h12 h22 v1 v2‖ ≤ κ) →
        -κ ^ 2 ≤ gaussK h11 h12 h22) := by
  intro h
  have := h 1 Complex.I (-1) 1 (fun v1 v2 hv => (norm_IIq_complex_curve v1 v2 hv).le)
  rw [gaussK_complex_curve] at this; norm_num at this

/-- **Mutante 2 (integral):** a cota de codimensao um `√(2π|χ|/A)` e FALSA em codimensao dois:
na testemunha 2 ela daria `√2 ≤ 1`. -/
theorem mutant_codim_one_floor_false :
    ¬ (∀ (h11 h12 h22 : ℝ → ℂ) (κ : ℝ) (χ : ℤ),
        0 < (areaMeasure π).real univ →
        (∀ x v1 v2, v1 ^ 2 + v2 ^ 2 = 1 → ‖IIq (h11 x) (h12 x) (h22 x) v1 v2‖ ≤ κ) →
        Integrable (fun x => gaussK (h11 x) (h12 x) (h22 x)) (areaMeasure π) →
        ∫ x, gaussK (h11 x) (h12 x) (h22 x) ∂(areaMeasure π) = 2 * π * χ → χ < 0 →
        √(2 * π * |(χ : ℝ)| / (areaMeasure π).real univ) ≤ κ) := by
  intro h
  obtain ⟨hop, hA, hGB, -⟩ := witness_codim_two
  have := h (fun _ => 1) (fun _ => Complex.I) (fun _ => -1) 1 (-1) hA hop
    (integrable_const _) hGB (by norm_num)
  rw [areaMeasure_real_univ Real.pi_pos.le] at this
  have e : 2 * π * |((-1 : ℤ) : ℝ)| / π = 2 := by
    push_cast; rw [abs_neg, abs_one]; field_simp
  rw [e] at this
  have : (1 : ℝ) < √2 := by
    rw [show (1 : ℝ) = √1 from Real.sqrt_one.symm]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  linarith

/-- **Mutante 3:** a cota estrita `√(2πχ/A) < κ` e FALSA (a esfera atinge a igualdade). -/
theorem mutant_strict_floor_false :
    ¬ (∀ (h11 h12 h22 : ℝ → ℝ) (κ : ℝ) (χ : ℤ),
        0 < (areaMeasure (4 * π)).real univ →
        (∀ x v1 v2, v1 ^ 2 + v2 ^ 2 = 1 → ‖IIq (h11 x) (h12 x) (h22 x) v1 v2‖ ≤ κ) →
        Integrable (fun x => gaussK (h11 x) (h12 x) (h22 x)) (areaMeasure (4 * π)) →
        ∫ x, gaussK (h11 x) (h12 x) (h22 x) ∂(areaMeasure (4 * π)) = 2 * π * χ → 0 < χ →
        √(2 * π * χ / (areaMeasure (4 * π)).real univ) < κ) := by
  intro h
  obtain ⟨hop, hA, hGB, heq⟩ := witness_round_sphere 1 one_pos
  simp only [one_pow, mul_one, div_one] at hop hA hGB heq
  have := h (fun _ => 1) (fun _ => 0) (fun _ => 1) 1 2 hA hop (integrable_const _) hGB
    (by norm_num)
  rw [heq] at this
  exact lt_irrefl _ this

end Witnesses

/-! ## 3. `thm:scaling_law` ("Curves curved in several planes; conditional")

`ℝ^{2m} = ℂ^m` e `EuclideanSpace ℂ (Fin m)` (norma `‖x‖² = ∑ |x_j|²`, a norma euclidiana de
`ℝ^{2m}`); `P_j` e a coordenada complexa `j`. -/

section ScalingLaw

open Complex in
/-- Curvatura com sinal de uma curva plana (em `ℂ ≅ ℝ²`) com velocidade `v` e aceleracao `a`:
`κ = (v_x a_y - v_y a_x)/|v|³` (a formula classica para curvas regulares nao parametrizadas
por comprimento de arco). -/
def planeCurv (v a : ℂ) : ℝ := (v.re * a.im - v.im * a.re) / ‖v‖ ^ 3

/-- `planeCurv v a = Im(conj(v) a)/|v|³`. -/
theorem planeCurv_eq_im (v a : ℂ) :
    planeCurv v a = ((starRingEnd ℂ) v * a).im / ‖v‖ ^ 3 := by
  simp [planeCurv, Complex.mul_im]; ring

/-- Identidade de Lagrange em `ℝ²`: `det(v,a)² + ⟨v,a⟩² = |v|²|a|²`. -/
theorem det_sq_add_dot_sq (v a : ℂ) :
    (v.re * a.im - v.im * a.re) ^ 2 + (v.re * a.re + v.im * a.im) ^ 2 = ‖v‖ ^ 2 * ‖a‖ ^ 2 := by
  rw [Complex.sq_norm, Complex.sq_norm, Complex.normSq_apply, Complex.normSq_apply]; ring

/-- Se `P_jγ` tem curvatura `≥ 1/R₀`, a componente de `a` normal a `v` tem modulo
`|det(v,a)|/|v| ≥ |v|²/R₀` (prova de (2): "magnitude `κ_j|v_j|² ≥ |v_j|²/R₀`"). -/
theorem det_ge {v a : ℂ} {R0 : ℝ} (hv : v ≠ 0)
    (hk : 1 / R0 ≤ |planeCurv v a|) : ‖v‖ ^ 3 / R0 ≤ |v.re * a.im - v.im * a.re| := by
  have hv3 : 0 < ‖v‖ ^ 3 := pow_pos (norm_pos_iff.mpr hv) 3
  rw [planeCurv, abs_div, abs_of_pos hv3, le_div_iff₀ hv3] at hk
  calc ‖v‖ ^ 3 / R0 = 1 / R0 * ‖v‖ ^ 3 := by ring
    _ ≤ _ := hk

/-- Consequencia pontual: `|v|⁴/R₀² ≤ |a|²` (vale tambem para `v = 0`). -/
theorem sq_norm_sq_div_le {v a : ℂ} {R0 : ℝ} (hR : 0 < R0)
    (hk : v ≠ 0 → 1 / R0 ≤ |planeCurv v a|) : (‖v‖ ^ 2) ^ 2 / R0 ^ 2 ≤ ‖a‖ ^ 2 := by
  by_cases hv : v = 0
  · simp [hv]
  have h1 := det_ge hv (hk hv)
  have hvpos : 0 < ‖v‖ ^ 2 := pow_pos (norm_pos_iff.mpr hv) 2
  have key : ‖v‖ ^ 2 * ((‖v‖ ^ 2) ^ 2 / R0 ^ 2) ≤ ‖v‖ ^ 2 * ‖a‖ ^ 2 := by
    calc ‖v‖ ^ 2 * ((‖v‖ ^ 2) ^ 2 / R0 ^ 2) = (‖v‖ ^ 3 / R0) ^ 2 := by
          field_simp
      _ ≤ (v.re * a.im - v.im * a.re) ^ 2 := by
          rw [← sq_abs (v.re * a.im - v.im * a.re)]
          exact pow_le_pow_left₀ (by positivity) h1 2
      _ ≤ ‖v‖ ^ 2 * ‖a‖ ^ 2 := by
          nlinarith [det_sq_add_dot_sq v a, sq_nonneg (v.re * a.re + v.im * a.im)]
  exact le_of_mul_le_mul_left key hvpos

/-- Cauchy–Schwarz usado em (2): se `∑ x_j = 1` (`m` termos) entao `1/m ≤ ∑ x_j²`; e `m ≠ 0`. -/
theorem one_div_card_le_sum_sq {m : ℕ} (x : Fin m → ℝ) (h : ∑ j, x j = 1) :
    (m : ℝ) ≠ 0 ∧ 1 / (m : ℝ) ≤ ∑ j, x j ^ 2 := by
  have h2 := sq_sum_le_card_mul_sum_sq (s := Finset.univ) (f := x)
  simp only [Finset.card_univ, Fintype.card_fin, h, one_pow] at h2
  have hm : (m : ℝ) ≠ 0 := by intro hm; rw [hm, zero_mul] at h2; linarith
  have hmpos : (0 : ℝ) < m := lt_of_le_of_ne (Nat.cast_nonneg m) (Ne.symm hm)
  refine ⟨hm, ?_⟩
  rw [div_le_iff₀ hmpos]; linarith

/-- **`thm:scaling_law` (2), forma pontual.** Em `ℂ^m`, com `v_j = P_jγ'(s)`, `a_j = P_jγ''(s)`,
`∑ |v_j|² = 1` (velocidade unitaria) e, para cada `j` com `v_j ≠ 0`, curvatura de `P_jγ`
`≥ 1/R₀`: entao `|γ''(s)|² = ∑ |a_j|² ≥ 1/(m R₀²)`. -/
theorem several_planes_pointwise {m : ℕ} (v a : Fin m → ℂ) {R0 : ℝ} (hR : 0 < R0)
    (hunit : ∑ j, ‖v j‖ ^ 2 = 1)
    (hcurv : ∀ j, v j ≠ 0 → 1 / R0 ≤ |planeCurv (v j) (a j)|) :
    1 / (m * R0 ^ 2) ≤ ∑ j, ‖a j‖ ^ 2 := by
  obtain ⟨hm, hcs⟩ := one_div_card_le_sum_sq (fun j => ‖v j‖ ^ 2) hunit
  have h1 : ∀ j, (‖v j‖ ^ 2) ^ 2 / R0 ^ 2 ≤ ‖a j‖ ^ 2 := fun j => sq_norm_sq_div_le hR (hcurv j)
  have hR2 : 0 < R0 ^ 2 := by positivity
  calc 1 / (m * R0 ^ 2) = (1 / (m : ℝ)) / R0 ^ 2 := by rw [div_div]
    _ ≤ (∑ j, (‖v j‖ ^ 2) ^ 2) / R0 ^ 2 := div_le_div_of_nonneg_right hcs hR2.le
    _ = ∑ j, (‖v j‖ ^ 2) ^ 2 / R0 ^ 2 := Finset.sum_div _ _ _
    _ ≤ ∑ j, ‖a j‖ ^ 2 := Finset.sum_le_sum fun j _ => h1 j

/-- **Caso de igualdade de (2)** (livro: "with equality if and only if `|v_j|² = 1/m` for all
`j` and each `P_jγ''(s)` is normal to `v_j` with magnitude `|v_j|²/R₀`"), sob as hipoteses de
(2). Normalidade: `⟨v_j, a_j⟩ = Re(v_j) Re(a_j) + Im(v_j) Im(a_j) = 0`. -/
theorem several_planes_eq_iff {m : ℕ} (v a : Fin m → ℂ) {R0 : ℝ} (hR : 0 < R0)
    (hunit : ∑ j, ‖v j‖ ^ 2 = 1)
    (hcurv : ∀ j, v j ≠ 0 → 1 / R0 ≤ |planeCurv (v j) (a j)|) :
    ∑ j, ‖a j‖ ^ 2 = 1 / (m * R0 ^ 2) ↔
      (∀ j, ‖v j‖ ^ 2 = 1 / m) ∧ (∀ j, (v j).re * (a j).re + (v j).im * (a j).im = 0) ∧
      (∀ j, ‖a j‖ = ‖v j‖ ^ 2 / R0) := by
  obtain ⟨hm, hcs⟩ := one_div_card_le_sum_sq (fun j => ‖v j‖ ^ 2) hunit
  have hmpos : (0 : ℝ) < m := lt_of_le_of_ne (Nat.cast_nonneg m) (Ne.symm hm)
  have hR2 : 0 < R0 ^ 2 := by positivity
  have h1 : ∀ j, (‖v j‖ ^ 2) ^ 2 / R0 ^ 2 ≤ ‖a j‖ ^ 2 := fun j => sq_norm_sq_div_le hR (hcurv j)
  constructor
  · intro heq
    -- (i) cada termo e justo: |a_j|² = |v_j|⁴/R₀², e ∑ |v_j|⁴ = 1/m
    have hlow : 1 / (m * R0 ^ 2) ≤ ∑ j, (‖v j‖ ^ 2) ^ 2 / R0 ^ 2 := by
      calc 1 / (m * R0 ^ 2) = (1 / (m : ℝ)) / R0 ^ 2 := by rw [div_div]
        _ ≤ (∑ j, (‖v j‖ ^ 2) ^ 2) / R0 ^ 2 := div_le_div_of_nonneg_right hcs hR2.le
        _ = ∑ j, (‖v j‖ ^ 2) ^ 2 / R0 ^ 2 := Finset.sum_div _ _ _
    have hz : ∑ j, (‖a j‖ ^ 2 - (‖v j‖ ^ 2) ^ 2 / R0 ^ 2) = 0 := by
      have hnn : 0 ≤ ∑ j, (‖a j‖ ^ 2 - (‖v j‖ ^ 2) ^ 2 / R0 ^ 2) :=
        Finset.sum_nonneg fun j _ => sub_nonneg.mpr (h1 j)
      rw [Finset.sum_sub_distrib] at hnn ⊢
      linarith
    have ha : ∀ j, ‖a j‖ ^ 2 = (‖v j‖ ^ 2) ^ 2 / R0 ^ 2 := by
      intro j
      have := (Finset.sum_eq_zero_iff_of_nonneg
        (fun j _ => sub_nonneg.mpr (h1 j))).mp hz j (Finset.mem_univ j)
      linarith
    have hsum4 : ∑ j, (‖v j‖ ^ 2) ^ 2 = 1 / m := by
      have : ∑ j, (‖v j‖ ^ 2) ^ 2 / R0 ^ 2 = 1 / (m * R0 ^ 2) := by
        rw [← heq]; exact Finset.sum_congr rfl fun j _ => (ha j).symm
      rw [← Finset.sum_div, div_eq_div_iff hR2.ne' (by positivity)] at this
      field_simp at this ⊢
      nlinarith [this]
    -- (ii) igualdade em Cauchy–Schwarz: todos os `|v_j|²` iguais a `1/m`
    have hvar : ∑ j, (‖v j‖ ^ 2 - 1 / m) ^ 2 = 0 := by
      have e : ∀ j, (‖v j‖ ^ 2 - 1 / (m : ℝ)) ^ 2 =
          (‖v j‖ ^ 2) ^ 2 - 2 / m * ‖v j‖ ^ 2 + 1 / (m : ℝ) ^ 2 := fun j => by ring
      simp only [e, Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum, hunit,
        hsum4, Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
      field_simp
      ring
    have hv : ∀ j, ‖v j‖ ^ 2 = 1 / m := by
      intro j
      have := (Finset.sum_eq_zero_iff_of_nonneg
        (fun j _ => sq_nonneg (‖v j‖ ^ 2 - 1 / (m : ℝ)))).mp hvar j (Finset.mem_univ j)
      have := pow_eq_zero_iff (n := 2) (by norm_num) |>.mp this
      linarith
    refine ⟨hv, ?_, ?_⟩
    · -- (iii) normalidade
      intro j
      have hvj : v j ≠ 0 := by
        intro h0; have := hv j; rw [h0, norm_zero] at this
        have : (0 : ℝ) < 1 / m := by positivity
        linarith [show (0 : ℝ) ^ 2 = 0 by norm_num]
      have hd := det_ge hvj (hcurv j hvj)
      have hd2 : (‖v j‖ ^ 3 / R0) ^ 2 ≤ ((v j).re * (a j).im - (v j).im * (a j).re) ^ 2 := by
        rw [← sq_abs ((v j).re * (a j).im - (v j).im * (a j).re)]
        exact pow_le_pow_left₀ (by positivity) hd 2
      have hL := det_sq_add_dot_sq (v j) (a j)
      rw [ha j] at hL
      have e : (‖v j‖ ^ 3 / R0) ^ 2 = ‖v j‖ ^ 2 * ((‖v j‖ ^ 2) ^ 2 / R0 ^ 2) := by
        field_simp
      have hdot : ((v j).re * (a j).re + (v j).im * (a j).im) ^ 2 ≤ 0 := by nlinarith
      exact pow_eq_zero_iff (n := 2) (by norm_num) |>.mp
        (le_antisymm hdot (sq_nonneg _))
    · intro j
      have h := ha j
      rw [show (‖v j‖ ^ 2) ^ 2 / R0 ^ 2 = (‖v j‖ ^ 2 / R0) ^ 2 by ring] at h
      exact (pow_left_inj₀ (norm_nonneg _) (by positivity) two_ne_zero).mp h
  · rintro ⟨hv, -, ha⟩
    have : ∀ j, ‖a j‖ ^ 2 = (1 / (m : ℝ)) ^ 2 / R0 ^ 2 := by
      intro j; rw [ha j, hv j]; ring
    simp only [this, Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    field_simp

/-- A projecao `P_jγ` tem derivada `P_j γ'`: liga as hipoteses de curvatura de (2), escritas
com as derivadas da curva projetada, aos dados de `γ`. -/
theorem hasDerivAt_component {m : ℕ} {γ : ℝ → EuclideanSpace ℂ (Fin m)}
    {γ' : EuclideanSpace ℂ (Fin m)} {s : ℝ} (h : HasDerivAt γ γ' s) (j : Fin m) :
    HasDerivAt (fun t => γ t j) (γ' j) s := by
  have := ((EuclideanSpace.proj j : EuclideanSpace ℂ (Fin m) →L[ℂ] ℂ).restrictScalars
    ℝ).hasFDerivAt.comp_hasDerivAt s h
  exact this

/-- **`thm:scaling_law` (2), forma do livro.** `γ : ℝ → ℂ^m` duas vezes derivavel em `s`, com
`|γ'(s)| = 1`; para cada `j`, se `P_jγ` tem derivadas `w = (P_jγ)'(s) ≠ 0` e
`w' = (P_jγ')'(s)`, sua curvatura e `≥ 1/R₀`. Entao `|γ''(s)| ≥ 1/(√m R₀)`. -/
theorem several_planes_lower_bound {m : ℕ} (γ γ' γ'' : ℝ → EuclideanSpace ℂ (Fin m))
    {R0 : ℝ} (hR : 0 < R0) (s : ℝ)
    (hγ : HasDerivAt γ (γ' s) s) (hγ' : HasDerivAt γ' (γ'' s) s) (hunit : ‖γ' s‖ = 1)
    (hcurv : ∀ j (w w' : ℂ), HasDerivAt (fun t => γ t j) w s →
      HasDerivAt (fun t => γ' t j) w' s → w ≠ 0 → 1 / R0 ≤ |planeCurv w w'|) :
    1 / (√m * R0) ≤ ‖γ'' s‖ := by
  have hsum : ∑ j, ‖γ' s j‖ ^ 2 = 1 := by
    rw [← EuclideanSpace.norm_sq_eq, hunit, one_pow]
  have h := several_planes_pointwise (fun j => γ' s j) (fun j => γ'' s j) hR hsum
    (fun j hj => hcurv j _ _ (hasDerivAt_component hγ j) (hasDerivAt_component hγ' j) hj)
  rw [← EuclideanSpace.norm_sq_eq] at h
  have hm : (0 : ℝ) ≤ m := Nat.cast_nonneg m
  have e : (1 / (√m * R0)) ^ 2 = 1 / (m * R0 ^ 2) := by
    rw [div_pow, mul_pow, Real.sq_sqrt hm, one_pow]
  rw [← e] at h
  exact (pow_le_pow_iff_left₀ (by positivity) (norm_nonneg _) two_ne_zero).mp h

/-! ### (1) O circulo diagonal -/

/-- O vetor de fases `w = ∑_j e^{iφ_j} e_j ∈ ℂ^m`. -/
def phaseVec {m : ℕ} (φ : Fin m → ℝ) : EuclideanSpace ℂ (Fin m) :=
  WithLp.toLp 2 (fun j => Complex.exp (φ j * Complex.I))

/-- `|w| = √m`. -/
theorem norm_phaseVec {m : ℕ} (φ : Fin m → ℝ) : ‖phaseVec φ‖ = √m := by
  rw [EuclideanSpace.norm_eq]
  simp [phaseVec, Complex.norm_exp_ofReal_mul_I]

/-- O circulo diagonal `γ(s) = R₀ e^{iωs} w`, isto e `P_jγ(s) = R₀ e^{i(ωs + φ_j)}`
(`thm:scaling_law` (1)). -/
def diagCircle {m : ℕ} (R0 ω : ℝ) (φ : Fin m → ℝ) (s : ℝ) : EuclideanSpace ℂ (Fin m) :=
  ((R0 : ℂ) * Complex.exp (((ω * s : ℝ) : ℂ) * Complex.I)) • phaseVec φ

/-- Componentes: `P_jγ(s) = R₀ e^{i(ωs + φ_j)}`, a forma do livro. -/
theorem diagCircle_apply {m : ℕ} (R0 ω : ℝ) (φ : Fin m → ℝ) (s : ℝ) (j : Fin m) :
    diagCircle R0 ω φ s j = R0 * Complex.exp (((ω * s + φ j : ℝ) : ℂ) * Complex.I) := by
  simp only [diagCircle, phaseVec, PiLp.smul_apply, smul_eq_mul]
  rw [mul_assoc, ← Complex.exp_add]
  push_cast; ring_nf

/-- Velocidade do circulo diagonal. -/
def diagVel {m : ℕ} (R0 ω : ℝ) (φ : Fin m → ℝ) (s : ℝ) : EuclideanSpace ℂ (Fin m) :=
  ((R0 : ℂ) * ((ω : ℂ) * Complex.I) * Complex.exp (((ω * s : ℝ) : ℂ) * Complex.I)) • phaseVec φ

/-- Aceleracao do circulo diagonal. -/
def diagAcc {m : ℕ} (R0 ω : ℝ) (φ : Fin m → ℝ) (s : ℝ) : EuclideanSpace ℂ (Fin m) :=
  ((R0 : ℂ) * ((ω : ℂ) * Complex.I) * ((ω : ℂ) * Complex.I) *
    Complex.exp (((ω * s : ℝ) : ℂ) * Complex.I)) • phaseVec φ

/-- Derivada de `s ↦ e^{iωs}`. -/
theorem hasDerivAt_expω (ω s : ℝ) :
    HasDerivAt (fun t : ℝ => Complex.exp (((ω * t : ℝ) : ℂ) * Complex.I))
      ((ω : ℂ) * Complex.I * Complex.exp (((ω * s : ℝ) : ℂ) * Complex.I)) s := by
  have h1 : HasDerivAt (fun t : ℝ => ((ω * t : ℝ) : ℂ) * Complex.I) ((ω : ℂ) * Complex.I) s := by
    have := ((hasDerivAt_id s).const_mul ω).ofReal_comp.mul_const Complex.I
    simpa using this
  have := h1.cexp
  convert this using 1; ring

/-- `γ' = diagVel`. -/
theorem diagCircle_hasDerivAt {m : ℕ} (R0 ω : ℝ) (φ : Fin m → ℝ) (s : ℝ) :
    HasDerivAt (diagCircle R0 ω φ) (diagVel R0 ω φ s) s := by
  have := ((hasDerivAt_expω ω s).const_mul (R0 : ℂ)).smul_const (phaseVec φ)
  refine this.congr_deriv ?_
  rw [diagVel]; congr 1; ring

/-- `γ'' = diagAcc`. -/
theorem diagVel_hasDerivAt {m : ℕ} (R0 ω : ℝ) (φ : Fin m → ℝ) (s : ℝ) :
    HasDerivAt (diagVel R0 ω φ) (diagAcc R0 ω φ s) s := by
  have := ((hasDerivAt_expω ω s).const_mul ((R0 : ℂ) * ((ω : ℂ) * Complex.I))).smul_const
    (phaseVec φ)
  refine this.congr_deriv ?_
  rw [diagAcc]; congr 1; ring

/-- `|e^{ix}| = 1`. -/
theorem norm_exp_ofReal_mul_I' (x : ℝ) : ‖Complex.exp ((x : ℂ) * Complex.I)‖ = 1 :=
  Complex.norm_exp_ofReal_mul_I x

/-- **`thm:scaling_law` (1).** Para `m ≥ 1`, `R₀ > 0`, fases quaisquer e `ω = 1/(√m R₀)`:
velocidade unitaria, curvatura constante `|γ''| = 1/(√m R₀)`, cada `P_jγ` no circulo de raio
`R₀`, `|γ| = √m R₀` e `γ'' = -ω² γ` (circulo plano de raio `√m R₀` centrado na origem). -/
theorem diag_circle {m : ℕ} (hm : 1 ≤ m) {R0 : ℝ} (hR : 0 < R0) (φ : Fin m → ℝ) (s : ℝ) :
    let ω := 1 / (√m * R0)
    ‖diagVel R0 ω φ s‖ = 1 ∧ ‖diagAcc R0 ω φ s‖ = 1 / (√m * R0) ∧
    (∀ j, ‖diagCircle R0 ω φ s j‖ = R0) ∧ ‖diagCircle R0 ω φ s‖ = √m * R0 ∧
    diagAcc R0 ω φ s = (-(ω : ℂ) ^ 2) • diagCircle R0 ω φ s := by
  intro ω
  have hsm : 0 < √(m : ℝ) := Real.sqrt_pos.mpr (by exact_mod_cast hm)
  have hω : 0 < ω := by positivity
  have hsq : √(m : ℝ) ^ 2 = m := Real.sq_sqrt (Nat.cast_nonneg m)
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · rw [diagVel, norm_smul, norm_phaseVec]
    simp only [norm_mul, norm_exp_ofReal_mul_I', Complex.norm_I, Complex.norm_real,
      Real.norm_of_nonneg hR.le, Real.norm_of_nonneg hω.le, mul_one]
    simp only [ω]; field_simp
  · rw [diagAcc, norm_smul, norm_phaseVec]
    simp only [norm_mul, norm_exp_ofReal_mul_I', Complex.norm_I, Complex.norm_real,
      Real.norm_of_nonneg hR.le, Real.norm_of_nonneg hω.le, mul_one]
    simp only [ω]; field_simp
  · intro j
    rw [diagCircle_apply, norm_mul, norm_exp_ofReal_mul_I', Complex.norm_real,
      Real.norm_of_nonneg hR.le, mul_one]
  · rw [diagCircle, norm_smul, norm_phaseVec, norm_mul, norm_exp_ofReal_mul_I',
      Complex.norm_real, Real.norm_of_nonneg hR.le]
    ring
  · rw [diagAcc, diagCircle, smul_smul]
    congr 1
    have hI : Complex.I * Complex.I = -1 := Complex.I_mul_I
    linear_combination (R0 : ℂ) * (ω : ℂ) ^ 2 *
      Complex.exp (((ω * s : ℝ) : ℂ) * Complex.I) * hI

/-! ### Testemunhas e mutantes de (2)

Dados pontuais do circulo diagonal com `m = 2`, `R₀ = 1`, `s = 0`, `φ = 0`:
`v_j = ωi`, `a_j = -ω²` com `ω² = 1/2`. -/

/-- `ω₀ = √(1/2)`. -/
def ω0 : ℝ := √(1 / 2)

/-- `ω₀² = 1/2`. -/
theorem ω0_sq : ω0 ^ 2 = 1 / 2 := Real.sq_sqrt (by norm_num)

/-- `ω₀ > 0`. -/
theorem ω0_pos : 0 < ω0 := Real.sqrt_pos.mpr (by norm_num)

/-- `∑|v_j|² = 1` para a testemunha. -/
theorem witness_vel_unit : ∑ j : Fin 2, ‖(fun _ : Fin 2 => (ω0 : ℂ) * Complex.I) j‖ ^ 2 = 1 := by
  simp [Complex.norm_real, Real.norm_of_nonneg ω0_pos.le, ω0_sq]

/-- Curvatura `1` de cada projecao na testemunha. -/
theorem witness_planeCurv :
    planeCurv ((ω0 : ℂ) * Complex.I) (-((ω0 : ℂ) ^ 2)) = 1 := by
  have h3 : ‖(ω0 : ℂ) * Complex.I‖ ^ 3 = ω0 ^ 3 := by
    rw [norm_mul, Complex.norm_I, Complex.norm_real, Real.norm_of_nonneg ω0_pos.le, mul_one]
  rw [planeCurv, h3]
  have hvr : ((ω0 : ℂ) * Complex.I).re = 0 := by simp
  have hvi : ((ω0 : ℂ) * Complex.I).im = ω0 := by simp
  have har : (-((ω0 : ℂ) ^ 2)).re = -ω0 ^ 2 := by simp [pow_two]
  have hai : (-((ω0 : ℂ) ^ 2)).im = 0 := by simp [pow_two]
  rw [hvr, hvi, har, hai, div_eq_one_iff_eq (pow_pos ω0_pos 3).ne']
  ring

/-- **Testemunha de (2) com IGUALDADE** (`m = 2`, `R₀ = 1`): hipoteses validas, curvatura de
cada projecao exatamente `1 = 1/R₀`, e `∑|a_j|² = 1/2 = 1/(m R₀²)`. -/
theorem witness_several_planes :
    (∑ j : Fin 2, ‖(fun _ : Fin 2 => (ω0 : ℂ) * Complex.I) j‖ ^ 2 = 1) ∧
    (∀ j : Fin 2, (fun _ : Fin 2 => (ω0 : ℂ) * Complex.I) j ≠ 0 →
      1 / (1 : ℝ) ≤ |planeCurv ((fun _ : Fin 2 => (ω0 : ℂ) * Complex.I) j)
        ((fun _ : Fin 2 => -((ω0 : ℂ) ^ 2)) j)|) ∧
    ∑ j : Fin 2, ‖(fun _ : Fin 2 => -((ω0 : ℂ) ^ 2)) j‖ ^ 2 = 1 / ((2 : ℕ) * (1 : ℝ) ^ 2) := by
  refine ⟨witness_vel_unit, fun j _ => ?_, ?_⟩
  · simp only [witness_planeCurv, abs_one, div_one, le_refl]
  · simp [norm_pow, Complex.norm_real, Real.norm_of_nonneg ω0_pos.le]
    rw [show ω0 ^ 2 = 1 / 2 from ω0_sq]; norm_num

/-- **Mutante (2a):** sem o fator `√m` (`|γ''|² ≥ 1/R₀²`) o enunciado e FALSO: o circulo
diagonal com `m = 2` tem `∑|a_j|² = 1/2 < 1`. -/
theorem mutant_no_sqrt_m_false :
    ¬ (∀ (v a : Fin 2 → ℂ) (R0 : ℝ), 0 < R0 → ∑ j, ‖v j‖ ^ 2 = 1 →
        (∀ j, v j ≠ 0 → 1 / R0 ≤ |planeCurv (v j) (a j)|) → 1 / R0 ^ 2 ≤ ∑ j, ‖a j‖ ^ 2) := by
  intro h
  obtain ⟨h1, h2, h3⟩ := witness_several_planes
  have := h _ _ 1 one_pos h1 h2
  rw [h3] at this; norm_num at this

/-- **Mutante (2b):** com `∑|v_j|² ≤ 1` em vez de `= 1` (curva que tambem anda numa direcao
real extra; observacao apos a proposicao) a cota cai: `v = a = 0`, `m = 1`. -/
theorem mutant_le_one_false :
    ¬ (∀ (v a : Fin 1 → ℂ) (R0 : ℝ), 0 < R0 → ∑ j, ‖v j‖ ^ 2 ≤ 1 →
        (∀ j, v j ≠ 0 → 1 / R0 ≤ |planeCurv (v j) (a j)|) →
        1 / ((1 : ℕ) * R0 ^ 2) ≤ ∑ j, ‖a j‖ ^ 2) := by
  intro h
  have := h (fun _ => 0) (fun _ => 0) 1 one_pos (by simp) (fun j hj => absurd rfl hj)
  norm_num at this

/-- **Mutante (1) (a armadilha do livro, `rem:` "Two pitfalls"):** com amplitude `R₀/√m` em
vez de `R₀` e a mesma frequencia unitaria, a curvatura e `1/R₀`, nao `1/(√m R₀)`. Aqui:
`m = 4`, `R₀ = 1`, curva `(1/2) e^{i 1·s} (1,1,1,1)` (velocidade `1`): `|γ''| = 1 ≠ 1/2`. -/
theorem pitfall_amplitude :
    ‖diagVel (1 / 2) 1 (fun _ : Fin 4 => 0) 0‖ = 1 ∧
      ‖diagAcc (1 / 2) 1 (fun _ : Fin 4 => 0) 0‖ = 1 ∧ (1 : ℝ) ≠ 1 / (√(4 : ℕ) * 1) := by
  have h4 : √((4 : ℕ) : ℝ) = 2 := by
    rw [show ((4 : ℕ) : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
  refine ⟨?_, ?_, ?_⟩
  · rw [diagVel, norm_smul, norm_phaseVec, h4]; simp
  · rw [diagAcc, norm_smul, norm_phaseVec, h4]; simp
  · rw [h4]; norm_num

/-- Cada projecao `P_jγ` do circulo diagonal tem curvatura `1/R₀` (para todo `ω > 0`). -/
theorem planeCurv_diag {m : ℕ} (R0 ω : ℝ) (hR : 0 < R0) (hω : 0 < ω) (φ : Fin m → ℝ)
    (s : ℝ) (j : Fin m) :
    planeCurv (diagVel R0 ω φ s j) (diagAcc R0 ω φ s j) = 1 / R0 := by
  set z : ℂ := Complex.exp (((ω * s : ℝ) : ℂ) * Complex.I) * Complex.exp (φ j * Complex.I)
    with hz
  have hzn : ‖z‖ = 1 := by
    rw [hz, norm_mul, norm_exp_ofReal_mul_I', Complex.norm_exp_ofReal_mul_I, one_mul]
  have hz1 : z.re ^ 2 + z.im ^ 2 = 1 := by
    have h2 := Complex.sq_norm z
    rw [hzn, Complex.normSq_apply] at h2; nlinarith [h2]
  have hv : diagVel R0 ω φ s j = ((R0 : ℂ) * ((ω : ℂ) * Complex.I)) * z := by
    simp only [diagVel, phaseVec, PiLp.smul_apply, smul_eq_mul, hz]; ring
  have ha : diagAcc R0 ω φ s j =
      ((R0 : ℂ) * ((ω : ℂ) * Complex.I) * ((ω : ℂ) * Complex.I)) * z := by
    simp only [diagAcc, phaseVec, PiLp.smul_apply, smul_eq_mul, hz]; ring
  have hnv : ‖diagVel R0 ω φ s j‖ = R0 * ω := by
    rw [hv, norm_mul, hzn, norm_mul, norm_mul, Complex.norm_I, Complex.norm_real,
      Complex.norm_real, Real.norm_of_nonneg hR.le, Real.norm_of_nonneg hω.le]
    ring
  rw [planeCurv, hnv, hv, ha]
  simp only [Complex.mul_re, Complex.mul_im, Complex.ofReal_re, Complex.ofReal_im,
    Complex.I_re, Complex.I_im]
  rw [div_eq_div_iff (by positivity) hR.ne']
  linear_combination R0 ^ 3 * ω ^ 3 * hz1

/-- **Testemunha de `several_planes_lower_bound` numa curva** (o circulo diagonal, qualquer
`m ≥ 1`, `R₀ > 0`, fases e `s`): as hipoteses sao descarregadas (curvatura das projecoes
calculada pelas derivadas de `P_jγ`, unicas) e a cota vale com IGUALDADE. -/
theorem witness_several_planes_curve {m : ℕ} (hm : 1 ≤ m) {R0 : ℝ} (hR : 0 < R0)
    (φ : Fin m → ℝ) (s : ℝ) :
    1 / (√m * R0) ≤ ‖diagAcc R0 (1 / (√m * R0)) φ s‖ ∧
      ‖diagAcc R0 (1 / (√m * R0)) φ s‖ = 1 / (√m * R0) := by
  have hsm : 0 < √(m : ℝ) := Real.sqrt_pos.mpr (by exact_mod_cast hm)
  have hω : 0 < 1 / (√m * R0) := by positivity
  have hdc := diag_circle hm hR φ s
  simp only at hdc
  obtain ⟨hunit, hacc, -, -, -⟩ := hdc
  refine ⟨several_planes_lower_bound (diagCircle R0 _ φ) (diagVel R0 _ φ) (diagAcc R0 _ φ) hR s
    (diagCircle_hasDerivAt R0 _ φ s) (diagVel_hasDerivAt R0 _ φ s) hunit ?_, hacc⟩
  intro j w w' hw hw' _
  have e1 := hw.unique (hasDerivAt_component (diagCircle_hasDerivAt R0 _ φ s) j)
  have e2 := hw'.unique (hasDerivAt_component (diagVel_hasDerivAt R0 _ φ s) j)
  rw [e1, e2, planeCurv_diag R0 _ hR hω φ s j, abs_of_pos (one_div_pos.mpr hR)]


end ScalingLaw

/-! ## 4. `thm:monotonicity` (Dimensional Monotonicity), caso de CURVAS (`k = 1`)

Classe admissivel de curvas: `γ : [0,ℓ] → K` (`K` faz o papel de `Ω̄`), parametrizada por
comprimento de arco (`‖γ'‖ = 1`), duas vezes derivavel, com `‖γ''‖ ≤ κ`, comprimento
`ℓ ≤ V` e bordo `∂M = Σ = {p, q}` (pontas `γ(0) = p`, `γ(ℓ) = q`). -/

section Monotonicity

variable {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [NormedAddCommGroup F] [InnerProductSpace ℝ F]

/-- Curva admissivel de comprimento `ℓ` com pico de curvatura `≤ κ` (`k = 1`). -/
def CurveAdm (K : Set E) (p q : E) (V κ ℓ : ℝ) (γ γ' γ'' : ℝ → E) : Prop :=
  0 ≤ ℓ ∧ ℓ ≤ V ∧ γ 0 = p ∧ γ ℓ = q ∧
    ∀ t ∈ Icc 0 ℓ, HasDerivAt γ (γ' t) t ∧ HasDerivAt γ' (γ'' t) t ∧ ‖γ' t‖ = 1 ∧
      ‖γ'' t‖ ≤ κ ∧ γ t ∈ K

/-- Os valores `κ` atingiveis: `κ*` e o seu infimo. -/
def curvSet (K : Set E) (p q : E) (V : ℝ) : Set ℝ :=
  {κ | ∃ ℓ γ γ' γ'', CurveAdm K p q V κ ℓ γ γ' γ''}

/-- `κ*_{n,1}(Ω, Σ, V)` para curvas (`sInf` real; o livro usa `inf ∅ = +∞`, por isso os
teoremas abaixo pedem `curvSet` nao vazio ou sao enunciados como inclusao). -/
def kappaStar (K : Set E) (p q : E) (V : ℝ) : ℝ := sInf (curvSet K p q V)

/-- Todo `κ` atingivel e `≥ 0`. -/
theorem curvSet_nonneg {K : Set E} {p q : E} {V κ : ℝ} (h : κ ∈ curvSet K p q V) : 0 ≤ κ := by
  obtain ⟨ℓ, γ, γ', γ'', h0, -, -, -, h⟩ := h
  exact le_trans (norm_nonneg _) (h 0 ⟨le_rfl, h0⟩).2.2.2.1

/-- Passo central da prova do livro: a imagem por uma isometria linear `ι` de uma curva
admissivel em `K` e admissivel em qualquer `K'` que contenha `ι(K)`, com o mesmo `κ` e o mesmo
comprimento. -/
theorem CurveAdm.map (ι : E →ₗᵢ[ℝ] F) {K : Set E} {K' : Set F} (hK : ι '' K ⊆ K')
    {p q : E} {V κ ℓ : ℝ} {γ γ' γ'' : ℝ → E} (h : CurveAdm K p q V κ ℓ γ γ' γ'') :
    CurveAdm K' (ι p) (ι q) V κ ℓ (ι ∘ γ) (ι ∘ γ') (ι ∘ γ'') := by
  obtain ⟨h0, hV, hp, hq, h⟩ := h
  refine ⟨h0, hV, by simp [hp], by simp [hq], fun t ht => ?_⟩
  obtain ⟨d1, d2, u, c, k⟩ := h t ht
  exact ⟨ι.toContinuousLinearMap.hasFDerivAt.comp_hasDerivAt t d1,
    ι.toContinuousLinearMap.hasFDerivAt.comp_hasDerivAt t d2,
    by simp [u], by simpa using c, hK ⟨_, k, rfl⟩⟩

/-- Inclusao dos conjuntos de `κ` atingiveis sob `ι` (valida mesmo se vazios). -/
theorem curvSet_mono (ι : E →ₗᵢ[ℝ] F) {K : Set E} {K' : Set F} (hK : ι '' K ⊆ K')
    (p q : E) (V : ℝ) : curvSet K p q V ⊆ curvSet K' (ι p) (ι q) V := by
  rintro κ ⟨ℓ, γ, γ', γ'', h⟩
  exact ⟨ℓ, _, _, _, h.map ι hK⟩

/-- **Monotonia, forma abstrata:** `κ*(K') ≤ κ*(K)` se `ι` e isometria linear e `ι(K) ⊆ K'`. -/
theorem kappaStar_mono (ι : E →ₗᵢ[ℝ] F) {K : Set E} {K' : Set F} (hK : ι '' K ⊆ K')
    (p q : E) (V : ℝ) (hne : (curvSet K p q V).Nonempty) :
    kappaStar K' (ι p) (ι q) V ≤ kappaStar K p q V :=
  csInf_le_csInf ⟨0, fun _ hκ => curvSet_nonneg hκ⟩ hne (curvSet_mono ι hK p q V)

end Monotonicity

/-- A inclusao canonica `i(x) = (x, 0)` de `ℝⁿ` em `ℝ^{n+1}`, como mapa linear. -/
def inclL (n : ℕ) : EuclideanSpace ℝ (Fin n) →ₗ[ℝ] EuclideanSpace ℝ (Fin (n + 1)) where
  toFun x := WithLp.toLp 2 (Fin.snoc (α := fun _ => ℝ) (WithLp.ofLp x) 0)
  map_add' x y := by
    ext i; refine Fin.lastCases ?_ (fun j => ?_) i <;> simp
  map_smul' c x := by
    ext i; refine Fin.lastCases ?_ (fun j => ?_) i <;> simp

/-- `i(x) = (x, 0)` e uma isometria linear `ℝⁿ → ℝ^{n+1}`. -/
def incl (n : ℕ) : EuclideanSpace ℝ (Fin n) →ₗᵢ[ℝ] EuclideanSpace ℝ (Fin (n + 1)) :=
  { inclL n with
    norm_map' := fun x => by
      rw [EuclideanSpace.norm_eq, EuclideanSpace.norm_eq, Fin.sum_univ_castSucc]
      simp [inclL] }

/-- `Ω̄ × [-d, d] ⊂ ℝ^{n+1}`, o fecho de `Ω̃ = Ω × (-d,d)` quando `K = Ω̄` e `d > 0`. -/
def cyl {n : ℕ} (K : Set (EuclideanSpace ℝ (Fin n))) (d : ℝ) :
    Set (EuclideanSpace ℝ (Fin (n + 1))) :=
  {y | WithLp.toLp 2 (fun i => y (Fin.castSucc i)) ∈ K ∧ |y (Fin.last n)| ≤ d}

/-- `i(K) ⊆ K × [-d,d]` para `d ≥ 0`. -/
theorem incl_image_subset_cyl {n : ℕ} (K : Set (EuclideanSpace ℝ (Fin n))) {d : ℝ}
    (hd : 0 ≤ d) : incl n '' K ⊆ cyl K d := by
  rintro _ ⟨x, hx, rfl⟩
  refine ⟨?_, ?_⟩
  · convert hx using 1
    ext i; simp [incl, inclL]
  · simpa [incl, inclL] using hd

/-- **`thm:monotonicity` para curvas** (`k = 1`): com `Ω̄ = K ⊂ ℝⁿ`, `Ω̃` com fecho
`K × [-d,d]` e `Σ̃ = i(Σ)`: `κ*_{n+1}(Ω̃, Σ̃, V) ≤ κ*_n(Ω, Σ, V)`. A hipotese `hne` substitui a
convencao `inf ∅ = +∞` do livro (sem ela a forma de inclusao `curvSet_mono` continua valendo). -/
theorem monotonicity {n : ℕ} (K : Set (EuclideanSpace ℝ (Fin n))) (p q : EuclideanSpace ℝ (Fin n))
    (V d : ℝ) (hd : 0 ≤ d) (hne : (curvSet K p q V).Nonempty) :
    kappaStar (cyl K d) (incl n p) (incl n q) V ≤ kappaStar K p q V :=
  kappaStar_mono (incl n) (incl_image_subset_cyl K hd) p q V hne

/-! ### Testemunha: meia-volta do circulo unitario em `ℝ²`, levada a `ℝ³` -/

/-- O circulo unitario `t ↦ e^{it}` em `ℂ ≅ ℝ²` e suas derivadas. -/
def arcC (t : ℝ) : ℂ := Complex.exp (t * Complex.I)

/-- Velocidade `i e^{it}`. -/
def arcC' (t : ℝ) : ℂ := arcC t * Complex.I

/-- Aceleracao `-e^{it}`. -/
def arcC'' (t : ℝ) : ℂ := arcC t * Complex.I * Complex.I

/-- `arcC' ` e a derivada de `arcC`. -/
theorem arcC_hasDerivAt (t : ℝ) : HasDerivAt arcC (arcC' t) t := by
  have h : HasDerivAt (fun s : ℝ => (s : ℂ) * Complex.I) (1 * Complex.I) t :=
    (hasDerivAt_id t).ofReal_comp.mul_const Complex.I
  have h2 := h.cexp
  simp only [one_mul] at h2
  exact h2

/-- `arcC''` e a derivada de `arcC'`. -/
theorem arcC'_hasDerivAt (t : ℝ) : HasDerivAt arcC' (arcC'' t) t :=
  (arcC_hasDerivAt t).mul_const Complex.I

/-- `|e^{it}| = 1`. -/
theorem norm_arcC (t : ℝ) : ‖arcC t‖ = 1 := Complex.norm_exp_ofReal_mul_I t

/-- A meia-volta `e^{it}`, `t ∈ [0,π]`, de `1` a `-1`, na bola unitaria fechada, comprimento
`π`, curvatura `1`: admissivel com `κ = 1`. -/
theorem arcC_adm :
    CurveAdm (Metric.closedBall (0 : ℂ) 1) 1 (-1) π 1 π arcC arcC' arcC'' := by
  refine ⟨Real.pi_pos.le, le_rfl, by simp [arcC], ?_, fun t _ => ⟨arcC_hasDerivAt t,
    arcC'_hasDerivAt t, ?_, ?_, ?_⟩⟩
  · simp only [arcC]; rw [Complex.exp_pi_mul_I]
  · rw [arcC', norm_mul, norm_arcC, Complex.norm_I, mul_one]
  · rw [arcC'', norm_mul, norm_mul, norm_arcC, Complex.norm_I]; norm_num
  · rw [mem_closedBall_zero_iff, norm_arcC]

/-- A mesma curva NAO e admissivel com `κ = 1/2` (a hipotese de curvatura morde). -/
theorem arcC_not_adm_half :
    ¬ CurveAdm (Metric.closedBall (0 : ℂ) 1) 1 (-1) π (1 / 2) π arcC arcC' arcC'' := by
  rintro ⟨-, -, -, -, h⟩
  have := (h 0 ⟨le_rfl, Real.pi_pos.le⟩).2.2.2.1
  rw [arcC'', norm_mul, norm_mul, norm_arcC, Complex.norm_I] at this; norm_num at this

/-- `ℂ ≅ ℝ²` isometricamente. -/
def toR2 : ℂ →ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 2) :=
  Complex.orthonormalBasisOneI.repr.toLinearIsometry

/-- **Testemunha de `monotonicity`** (`n = 2`, `K` = disco unitario, `d = 1`): a meia-volta
pertence a `curvSet` em `ℝ²` (com `κ = 1`) e, levada a `ℝ³`, a `curvSet` do cilindro; logo o
infimo em `ℝ³` e `≤ 1`. -/
theorem witness_monotonicity :
    (1 : ℝ) ∈ curvSet (toR2 '' Metric.closedBall 0 1) (toR2 1) (toR2 (-1)) π ∧
    (1 : ℝ) ∈ curvSet (cyl (toR2 '' Metric.closedBall 0 1) 1) (incl 2 (toR2 1))
      (incl 2 (toR2 (-1))) π ∧
    kappaStar (cyl (toR2 '' Metric.closedBall 0 1) 1) (incl 2 (toR2 1)) (incl 2 (toR2 (-1))) π
      ≤ kappaStar (toR2 '' Metric.closedBall 0 1) (toR2 1) (toR2 (-1)) π := by
  have h2 : (1 : ℝ) ∈ curvSet (toR2 '' Metric.closedBall 0 1) (toR2 1) (toR2 (-1)) π :=
    ⟨π, _, _, _, arcC_adm.map toR2 subset_rfl⟩
  exact ⟨h2, curvSet_mono (incl 2) (incl_image_subset_cyl _ zero_le_one) _ _ _ h2,
    monotonicity _ _ _ π 1 zero_le_one ⟨1, h2⟩⟩

/-- **Mutante 1 (sem isometria):** para o mapa linear `2·id` (nao isometrico) a imagem de uma
curva admissivel NAO e admissivel (a velocidade dobra). -/
theorem mutant_not_isometry_false :
    ¬ (∀ (L : ℂ →L[ℝ] ℂ) (K : Set ℂ) (p q : ℂ) (V κ ℓ : ℝ) (γ γ' γ'' : ℝ → ℂ),
        CurveAdm K p q V κ ℓ γ γ' γ'' →
        CurveAdm (L '' K) (L p) (L q) V κ ℓ (L ∘ γ) (L ∘ γ') (L ∘ γ'')) := by
  intro h
  obtain ⟨-, -, -, -, h'⟩ := h ((2 : ℝ) • ContinuousLinearMap.id ℝ ℂ) _ _ _ _ _ _ _ _ _ arcC_adm
  have := (h' 0 ⟨le_rfl, Real.pi_pos.le⟩).2.2.1
  simp only [Function.comp_apply, smul_apply, ContinuousLinearMap.id_apply,
    norm_smul, arcC', norm_mul, norm_arcC, Complex.norm_I] at this
  norm_num at this

/-- **Mutante 2 (`d < 0`):** o cilindro e vazio e a inclusao `curvSet K ⊆ curvSet (cyl K d)`
FALHA. -/
theorem mutant_negative_d_false :
    ¬ (∀ d : ℝ, curvSet (toR2 '' Metric.closedBall 0 1) (toR2 1) (toR2 (-1)) π ⊆
        curvSet (cyl (toR2 '' Metric.closedBall 0 1) d) (incl 2 (toR2 1))
          (incl 2 (toR2 (-1))) π) := by
  intro h
  obtain ⟨ℓ, γ, γ', γ'', h0, -, -, -, hc⟩ := h (-1) witness_monotonicity.1
  have := (hc 0 ⟨le_rfl, h0⟩).2.2.2.2.2
  linarith [abs_nonneg (γ 0 (Fin.last 2))]

/-! ## 5. `prop:knot_gap`, condicional a Fary–Milnor e a Fenchel -/

section KnotGap

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- Curvatura total `∫₀^ℓ |κ| ds` de uma curva por comprimento de arco (`|κ| = ‖γ''‖`). -/
def totalCurv (γ'' : ℝ → E) (ℓ : ℝ) : ℝ := ∫ s in (0 : ℝ)..ℓ, ‖γ'' s‖

omit [InnerProductSpace ℝ E] in
/-- `∫₀^ℓ |κ| ≤ ℓ ‖κ‖_∞` (passo da prova do livro). Nao exige integrabilidade: se `‖γ''‖` nao
for integravel a integral de Bochner vale `0`. -/
theorem totalCurv_le {γ'' : ℝ → E} {ℓ k : ℝ} (hℓ : 0 ≤ ℓ) (hk : ∀ s ∈ Icc 0 ℓ, ‖γ'' s‖ ≤ k) :
    totalCurv γ'' ℓ ≤ ℓ * k := by
  have h := intervalIntegral.norm_integral_le_of_norm_le_const (a := 0) (b := ℓ)
    (f := fun s => ‖γ'' s‖) (C := k) (fun s hs => by
      rw [norm_norm]; rw [Set.uIoc_of_le hℓ] at hs; exact hk s (Ioc_subset_Icc_self hs))
  rw [sub_zero, abs_of_nonneg hℓ, Real.norm_eq_abs] at h
  unfold totalCurv
  linarith [le_abs_self (∫ s in (0 : ℝ)..ℓ, ‖γ'' s‖)]

/-- Curva FECHADA admissivel (`C¹` fechada: `γ(ℓ) = γ(0)`, `γ'(ℓ) = γ'(0)`), comprimento
`0 < ℓ ≤ L`, por comprimento de arco, duas vezes derivavel, `‖γ''‖ ≤ k`. -/
def ClosedAdm (L k ℓ : ℝ) (γ γ' γ'' : ℝ → E) : Prop :=
  0 < ℓ ∧ ℓ ≤ L ∧ γ ℓ = γ 0 ∧ γ' ℓ = γ' 0 ∧
    ∀ t ∈ Icc 0 ℓ, HasDerivAt γ (γ' t) t ∧ HasDerivAt γ' (γ'' t) t ∧ ‖γ' t‖ = 1 ∧
      ‖γ'' t‖ ≤ k

/-- **`prop:knot_gap`, por curva:** se a curvatura total excede `4π` (Fary–Milnor, hipotese
`hFM`), entao `‖κ‖_∞ > 4π/L`. -/
theorem knot_curve_bound {L k ℓ : ℝ} {γ γ' γ'' : ℝ → E} (h : ClosedAdm L k ℓ γ γ' γ'')
    (hFM : 4 * π < totalCurv γ'' ℓ) : 4 * π / L < k := by
  obtain ⟨hℓ, hℓL, -, -, hc⟩ := h
  have hk0 : 0 ≤ k := le_trans (norm_nonneg _) (hc 0 ⟨le_rfl, hℓ.le⟩).2.2.2
  have h1 := totalCurv_le hℓ.le (fun s hs => (hc s hs).2.2.2)
  rw [div_lt_iff₀ (lt_of_lt_of_le hℓ hℓL)]
  nlinarith

/-- **Fenchel, por curva:** curvatura total `≥ 2π` (hipotese `hF`) da `‖κ‖_∞ ≥ 2π/L`. -/
theorem fenchel_curve_bound {L k ℓ : ℝ} {γ γ' γ'' : ℝ → E} (h : ClosedAdm L k ℓ γ γ' γ'')
    (hF : 2 * π ≤ totalCurv γ'' ℓ) : 2 * π / L ≤ k := by
  obtain ⟨hℓ, hℓL, -, -, hc⟩ := h
  have hk0 : 0 ≤ k := le_trans (norm_nonneg _) (hc 0 ⟨le_rfl, hℓ.le⟩).2.2.2
  have h1 := totalCurv_le hℓ.le (fun s hs => (hc s hs).2.2.2)
  rw [div_le_iff₀ (lt_of_lt_of_le hℓ hℓL)]
  nlinarith

/-- Valores de `‖κ‖_∞` de curvas fechadas imersas de comprimento `≤ L`. -/
def immSet (E' : Type*) [NormedAddCommGroup E'] [InnerProductSpace ℝ E'] (L : ℝ) : Set ℝ :=
  {k | ∃ (ℓ : ℝ) (γ γ' γ'' : ℝ → E'), ClosedAdm L k ℓ γ γ' γ''}

/-- Idem, restrito a curvas com um predicado de "tipo de no" `IsK` (o tipo de no nao e
definido aqui; so entra pela hipotese de Fary–Milnor). -/
def knotSet (IsK : (ℝ → E) → ℝ → Prop) (L : ℝ) : Set ℝ :=
  {k | ∃ (ℓ : ℝ) (γ γ' γ'' : ℝ → E), ClosedAdm L k ℓ γ γ' γ'' ∧ IsK γ ℓ}

/-- O circulo `γ(s) = r cos(s/r) e₁ + r sin(s/r) e₂` (`e₁ ⊥ e₂` unitarios). -/
def circleCurve (r : ℝ) (e1 e2 : E) (s : ℝ) : E :=
  (r * Real.cos (s / r)) • e1 + (r * Real.sin (s / r)) • e2

/-- Velocidade do circulo. -/
def circleVel (r : ℝ) (e1 e2 : E) (s : ℝ) : E :=
  (-Real.sin (s / r)) • e1 + Real.cos (s / r) • e2

/-- Aceleracao do circulo. -/
def circleAcc (r : ℝ) (e1 e2 : E) (s : ℝ) : E :=
  (-(1 / r) * Real.cos (s / r)) • e1 + (-(1 / r) * Real.sin (s / r)) • e2

/-- `|a e₁ + b e₂| = √(a² + b²)` para `e₁, e₂` ortonormais. -/
theorem norm_comb {e1 e2 : E} (h1 : ‖e1‖ = 1) (h2 : ‖e2‖ = 1) (h12 : inner ℝ e1 e2 = 0)
    (a b : ℝ) : ‖a • e1 + b • e2‖ = √(a ^ 2 + b ^ 2) := by
  rw [← Real.sqrt_sq (norm_nonneg _), norm_add_sq_real, norm_smul, norm_smul, h1, h2,
    real_inner_smul_left, real_inner_smul_right, h12]
  simp [Real.norm_eq_abs, sq_abs]

/-- `circleVel` e a derivada de `circleCurve`. -/
theorem circle_hasDerivAt {r : ℝ} (hr : r ≠ 0) (e1 e2 : E) (s : ℝ) :
    HasDerivAt (circleCurve r e1 e2) (circleVel r e1 e2 s) s := by
  have hd : HasDerivAt (fun t : ℝ => t / r) (1 / r) s := (hasDerivAt_id s).div_const r
  have hc := ((Real.hasDerivAt_cos (s / r)).comp s hd).const_mul r
  have hs := ((Real.hasDerivAt_sin (s / r)).comp s hd).const_mul r
  have := (hc.smul_const e1).add (hs.smul_const e2)
  refine this.congr_deriv ?_
  simp only [circleVel]
  congr 1 <;> congr 1 <;> field_simp

/-- `circleAcc` e a derivada de `circleVel`. -/
theorem circleVel_hasDerivAt (r : ℝ) (e1 e2 : E) (s : ℝ) :
    HasDerivAt (circleVel r e1 e2) (circleAcc r e1 e2 s) s := by
  have hd : HasDerivAt (fun t : ℝ => t / r) (1 / r) s := (hasDerivAt_id s).div_const r
  have hc := ((Real.hasDerivAt_sin (s / r)).comp s hd).neg
  have hs := (Real.hasDerivAt_cos (s / r)).comp s hd
  have := (hc.smul_const e1).add (hs.smul_const e2)
  refine this.congr_deriv ?_
  simp only [circleAcc]
  congr 1 <;> congr 1 <;> ring

/-- O circulo de raio `r > 0` percorrido `N ≥ 1` vezes (comprimento `ℓ = 2πrN`) e uma curva
fechada admissivel com `k = 1/r`, para todo `L ≥ ℓ`; e sua curvatura total e `2πN`. -/
theorem circle_closedAdm {r : ℝ} (hr : 0 < r) {e1 e2 : E} (h1 : ‖e1‖ = 1) (h2 : ‖e2‖ = 1)
    (h12 : inner ℝ e1 e2 = 0) (N : ℕ) (hN : 1 ≤ N) {L : ℝ} (hL : 2 * π * r * N ≤ L) :
    ClosedAdm L (1 / r) (2 * π * r * N) (circleCurve r e1 e2) (circleVel r e1 e2)
      (circleAcc r e1 e2) ∧
    totalCurv (circleAcc r e1 e2) (2 * π * r * N) = 2 * π * N := by
  have hN' : (1 : ℝ) ≤ N := by exact_mod_cast hN
  have hper : 2 * π * r * N / r = N * (2 * π) := by field_simp
  have hcos : Real.cos (2 * π * r * N / r) = 1 := by rw [hper, Real.cos_nat_mul_two_pi]
  have hsin : Real.sin (2 * π * r * N / r) = 0 := by
    rw [hper, show (N : ℝ) * (2 * π) = ((2 * N : ℕ) : ℝ) * π by push_cast; ring,
      Real.sin_nat_mul_pi]
  have hacc : ∀ s, ‖circleAcc r e1 e2 s‖ = 1 / r := by
    intro s
    rw [circleAcc, norm_comb h1 h2 h12]
    rw [show (-(1 / r) * Real.cos (s / r)) ^ 2 + (-(1 / r) * Real.sin (s / r)) ^ 2 =
      (1 / r) ^ 2 by rw [mul_pow, mul_pow, ← mul_add, Real.cos_sq_add_sin_sq]; ring]
    exact Real.sqrt_sq (by positivity)
  refine ⟨⟨by positivity, hL, ?_, ?_, fun t _ => ⟨circle_hasDerivAt hr.ne' e1 e2 t,
    circleVel_hasDerivAt r e1 e2 t, ?_, (hacc t).le⟩⟩, ?_⟩
  · simp [circleCurve, hcos, hsin]
  · simp [circleVel, hcos, hsin]
  · rw [circleVel, norm_comb h1 h2 h12, neg_sq, Real.sin_sq_add_cos_sq, Real.sqrt_one]
  · simp only [totalCurv, hacc, intervalIntegral.integral_const, sub_zero, smul_eq_mul]
    field_simp

/-- **`prop:knot_gap`** (curvas, condicional). Para `L > 0`:
(a) com Fary–Milnor como hipotese (`hFM`: curvatura total `> 4π` para curvas de tipo `K`),
`κ*_K(L) ≥ 4π/L` (se a classe for nao vazia; vazia, `κ*_K = +∞` no livro);
(b) com Fenchel como hipotese (`hFen`: curvatura total `≥ 2π` para toda curva fechada),
`κ*_Imm(L) = 2π/L`, atingido pelo circulo de comprimento `L`;
(c) `4π/L = κ*_Imm(L) + 2π/L`.
`e₁, e₂` ortonormais garantem que o espaco tem um plano para o circulo. -/
theorem knot_gap (IsK : (ℝ → E) → ℝ → Prop) {L : ℝ} (hL : 0 < L) {e1 e2 : E}
    (h1 : ‖e1‖ = 1) (h2 : ‖e2‖ = 1) (h12 : inner ℝ e1 e2 = 0)
    (hFM : ∀ k ℓ (γ γ' γ'' : ℝ → E), ClosedAdm L k ℓ γ γ' γ'' → IsK γ ℓ →
      4 * π < totalCurv γ'' ℓ)
    (hFen : ∀ k ℓ (γ γ' γ'' : ℝ → E), ClosedAdm L k ℓ γ γ' γ'' → 2 * π ≤ totalCurv γ'' ℓ)
    (hne : (knotSet IsK L).Nonempty) :
    4 * π / L ≤ sInf (knotSet IsK L) ∧ sInf (immSet E L) = 2 * π / L ∧
      4 * π / L = sInf (immSet E L) + 2 * π / L := by
  have hImm : sInf (immSet E L) = 2 * π / L := by
    apply IsLeast.csInf_eq
    refine ⟨?_, ?_⟩
    · have hr : 0 < L / (2 * π) := by positivity
      have hlen : 2 * π * (L / (2 * π)) * ((1 : ℕ) : ℝ) = L := by push_cast; field_simp
      obtain ⟨hc, -⟩ := circle_closedAdm hr h1 h2 h12 1 le_rfl (L := L) (by rw [hlen])
      have hk : 1 / (L / (2 * π)) = 2 * π / L := by field_simp
      rw [hlen, hk] at hc
      exact ⟨L, _, _, _, hc⟩
    · rintro k ⟨ℓ, γ, γ', γ'', hc⟩
      exact fenchel_curve_bound hc (hFen k ℓ γ γ' γ'' hc)
  refine ⟨le_csInf hne ?_, hImm, by rw [hImm]; ring⟩
  rintro k ⟨ℓ, γ, γ', γ'', hc, hK⟩
  exact (knot_curve_bound hc (hFM k ℓ γ γ' γ'' hc hK)).le

end KnotGap

/-! ### Testemunhas e mutantes de `prop:knot_gap` (em `ℂ ≅ ℝ²`, `e₁ = 1`, `e₂ = i`) -/

/-- `1 ⊥ i` em `ℂ ≅ ℝ²`. -/
theorem inner_one_I : inner ℝ (1 : ℂ) Complex.I = 0 := by simp [Complex.inner]

/-- **Testemunha (Fenchel, por curva)**: o circulo de raio `1` (`ℓ = L = 2π`) satisfaz as
hipoteses de `fenchel_curve_bound` com curvatura total exatamente `2π`, e a cota e atingida:
`2π/L = 1 = k`. -/
theorem witness_fenchel :
    ClosedAdm (2 * π) 1 (2 * π) (circleCurve 1 (1 : ℂ) Complex.I) (circleVel 1 1 Complex.I)
      (circleAcc 1 1 Complex.I) ∧
    totalCurv (circleAcc 1 (1 : ℂ) Complex.I) (2 * π) = 2 * π ∧ 2 * π / (2 * π) = (1 : ℝ) := by
  obtain ⟨hc, ht⟩ := circle_closedAdm one_pos (norm_one) Complex.norm_I inner_one_I 1 le_rfl
    (L := 2 * π) (by simp)
  simp only [Nat.cast_one, mul_one, div_one] at hc ht
  exact ⟨hc, ht, div_self (by positivity)⟩

/-- **Testemunha (Fary–Milnor, por curva)**: o circulo de raio `1` percorrido 3 vezes
(`ℓ = L = 6π`) tem curvatura total `6π > 4π`; as hipoteses de `knot_curve_bound` valem e a
conclusao `4π/6π < 1` nao e trivial. -/
theorem witness_knot_curve :
    ClosedAdm (2 * π * 1 * 3) 1 (2 * π * 1 * 3) (circleCurve 1 (1 : ℂ) Complex.I)
      (circleVel 1 1 Complex.I) (circleAcc 1 1 Complex.I) ∧
    4 * π < totalCurv (circleAcc 1 (1 : ℂ) Complex.I) (2 * π * 1 * 3) := by
  obtain ⟨hc, ht⟩ := circle_closedAdm one_pos (norm_one) Complex.norm_I inner_one_I 3
    (by norm_num) (L := 2 * π * 1 * 3) (by push_cast; rfl)
  simp only [div_one] at hc
  push_cast at hc ht
  refine ⟨hc, ?_⟩
  rw [ht]; nlinarith [Real.pi_pos]

/-- **Mutante 1:** a cota de Fenchel estrita `2π/L < k` e FALSA (circulo). -/
theorem mutant_fenchel_strict_false :
    ¬ (∀ (L k ℓ : ℝ) (γ γ' γ'' : ℝ → ℂ), ClosedAdm L k ℓ γ γ' γ'' →
        2 * π ≤ totalCurv γ'' ℓ → 2 * π / L < k) := by
  intro h
  obtain ⟨hc, ht, he⟩ := witness_fenchel
  have := h _ _ _ _ _ _ hc ht.ge
  rw [he] at this; exact lt_irrefl _ this

/-- **Mutante 2 (sem a cota de comprimento `ℓ ≤ L`):** FALSO; o circulo triplo (`ℓ = 6π`)
com `L = 1` daria `4π < 1`. -/
theorem mutant_no_length_bound_false :
    ¬ (∀ (L k ℓ : ℝ) (γ γ' γ'' : ℝ → ℂ), 0 < L → ClosedAdm ℓ k ℓ γ γ' γ'' →
        4 * π < totalCurv γ'' ℓ → 4 * π / L < k) := by
  intro h
  obtain ⟨hc, ht⟩ := witness_knot_curve
  have := h 1 _ _ _ _ _ one_pos hc ht
  nlinarith [Real.two_le_pi]

/-! ## 6. Contas da tabela `tab:universal_classification` e da observacao sobre calibracao -/

/-- `II(v,v)` do toro produto `(R/√m)(e^{iu₁},…,e^{iu_m})` para o vetor unitario
`v = ∑ v_j ∂_{u_j}/r`, `r = R/√m`, nas coordenadas normais `(ν_j)`: componente `j` igual a
`v_j²/r` (a formula do livro, `|II(v,v)|² = ∑ v_j⁴/r²`; a derivacao a partir da imersao NAO e
formalizada). -/
def torusII {m : ℕ} (r : ℝ) (v : Fin m → ℝ) : EuclideanSpace ℝ (Fin m) :=
  WithLp.toLp 2 (fun j => v j ^ 2 / r)

/-- `∑ v_j⁴ ≤ (∑ v_j²)² = 1`. -/
theorem sum_pow_four_le {m : ℕ} (v : Fin m → ℝ) (h : ∑ j, v j ^ 2 = 1) :
    ∑ j, (v j ^ 2) ^ 2 ≤ 1 := by
  have hle : ∀ j, v j ^ 2 ≤ 1 := fun j => by
    rw [← h]
    exact Finset.single_le_sum (f := fun j => v j ^ 2) (fun i _ => sq_nonneg (v i))
      (Finset.mem_univ j)
  calc ∑ j, (v j ^ 2) ^ 2 ≤ ∑ j, v j ^ 2 :=
        Finset.sum_le_sum fun j _ => by nlinarith [sq_nonneg (v j), hle j]
    _ = 1 := h

/-- **Toro produto, `‖II‖_op = √m/R`:** `|II(v,v)| ≤ 1/r` para todo `v` unitario, com
igualdade na direcao coordenada `e_j`, e `1/r = √m/R` para `r = R/√m`. -/
theorem product_torus {m : ℕ} {R : ℝ} (hR : 0 < R) (hm : 1 ≤ m) :
    let r := R / √m
    (∀ v : Fin m → ℝ, ∑ j, v j ^ 2 = 1 → ‖torusII r v‖ ≤ 1 / r) ∧
    (∀ j : Fin m, ‖torusII r (Pi.single j 1)‖ = 1 / r) ∧ 1 / r = √m / R := by
  intro r
  have hsm : 0 < √(m : ℝ) := Real.sqrt_pos.mpr (by exact_mod_cast hm)
  have hr : 0 < r := by positivity
  refine ⟨fun v hv => ?_, fun j => ?_, by simp only [r]; field_simp⟩
  · rw [EuclideanSpace.norm_eq]
    have e : ∑ j, ‖(torusII r v) j‖ ^ 2 = (∑ j, (v j ^ 2) ^ 2) / r ^ 2 := by
      rw [Finset.sum_div]
      refine Finset.sum_congr rfl fun j _ => ?_
      simp [torusII, Real.norm_eq_abs, abs_of_pos hr, div_pow]
    rw [e]
    calc √((∑ j, (v j ^ 2) ^ 2) / r ^ 2) ≤ √(1 / r ^ 2) :=
          Real.sqrt_le_sqrt (div_le_div_of_nonneg_right (sum_pow_four_le v hv) (by positivity))
      _ = 1 / r := by rw [one_div, Real.sqrt_inv, Real.sqrt_sq hr.le, one_div]
  · rw [EuclideanSpace.norm_eq]
    have e : ∑ i, ‖(torusII r (Pi.single j 1)) i‖ ^ 2 = 1 / r ^ 2 := by
      rw [Finset.sum_eq_single j]
      · simp [torusII, Real.norm_eq_abs, sq_abs]
      · intro i _ hij; simp [torusII, Pi.single_apply, hij]
      · simp
    rw [e, one_div, Real.sqrt_inv, Real.sqrt_sq hr.le, one_div]

/-- **Mutante (toro):** a cota estrita `|II(v,v)| < 1/r` e FALSA (direcao coordenada). -/
theorem mutant_torus_strict_false :
    ¬ (∀ v : Fin 2 → ℝ, ∑ j, v j ^ 2 = 1 → ‖torusII 1 v‖ < 1 / 1) := by
  intro h
  have hv : ∑ j, (Pi.single (0 : Fin 2) (1 : ℝ) : Fin 2 → ℝ) j ^ 2 = 1 := by
    simp [Fin.sum_univ_two]
  have := h _ hv
  obtain ⟨-, h2, -⟩ := product_torus (m := 2) (R := √2) (by positivity) (by norm_num)
  have h2' := h2 0
  have hr : √2 / √((2 : ℕ) : ℝ) = 1 := by push_cast; exact div_self (by positivity)
  simp only [hr] at h2'
  rw [h2'] at this; exact lt_irrefl _ this

/-- Curva complexa em `ℂ²` com `II(e₁,e₁) = a`, `II(e₁,Je₁) = ia`, `II(Je₁,Je₁) = -a`:
`II(v,v) = (v₁ + i v₂)² a`. -/
theorem IIq_complex_curve_a (a : ℂ) (v1 v2 : ℝ) :
    IIq a (Complex.I * a) (-a) v1 v2 = ((v1 : ℂ) + v2 * Complex.I) ^ 2 * a := by
  apply Complex.ext <;> simp [IIq, pow_two] <;> ring

/-- Norma de Frobenius `‖II‖_F² = |II₁₁|² + 2|II₁₂|² + |II₂₂|²` (referencial ortonormal). -/
def frobSq {N : Type*} [NormedAddCommGroup N] (h11 h12 h22 : N) : ℝ :=
  ‖h11‖ ^ 2 + 2 * ‖h12‖ ^ 2 + ‖h22‖ ^ 2

/-- **"Calibration does not force isotropy"**: para a curva complexa, `|II(v,v)| = |a|` para
todo `v` unitario (logo `‖II‖_op = |a|`) e `‖II‖_F = 2|a|`: `‖II‖_op = ‖II‖_F/2`. -/
theorem complex_curve_isotropy (a : ℂ) :
    (∀ v1 v2 : ℝ, v1 ^ 2 + v2 ^ 2 = 1 → ‖IIq a (Complex.I * a) (-a) v1 v2‖ = ‖a‖) ∧
    √(frobSq a (Complex.I * a) (-a)) = 2 * ‖a‖ := by
  refine ⟨fun v1 v2 h => ?_, ?_⟩
  · rw [IIq_complex_curve_a, norm_mul, norm_pow]
    have : ‖(v1 : ℂ) + v2 * Complex.I‖ = 1 := by
      have h2 : ‖(v1 : ℂ) + v2 * Complex.I‖ ^ 2 = 1 := by
        rw [Complex.sq_norm, Complex.normSq_apply]; simp; nlinarith [h]
      nlinarith [h2, norm_nonneg ((v1 : ℂ) + v2 * Complex.I)]
    rw [this, one_pow, one_mul]
  · rw [frobSq, norm_mul, Complex.norm_I, one_mul, norm_neg,
      show ‖a‖ ^ 2 + 2 * ‖a‖ ^ 2 + ‖a‖ ^ 2 = (2 * ‖a‖) ^ 2 by ring,
      Real.sqrt_sq (by positivity)]

/-- **Mutante (isotropia):** a igualdade "isotropica" `‖II‖_op = ‖II‖_F/√c` com `c = 2` e
FALSA para a curva complexa com `a = 1` (daria `1 = √2`). -/
theorem mutant_isotropy_false :
    ¬ (∀ a : ℂ, ‖a‖ = √(frobSq a (Complex.I * a) (-a)) / √2) := by
  intro h
  have h1 := h 1
  rw [(complex_curve_isotropy 1).2, norm_one, mul_one] at h1
  have hs : (0 : ℝ) < √2 := by positivity
  have : √2 * √2 = 2 := Real.mul_self_sqrt (by norm_num)
  field_simp at h1
  nlinarith

end LeanReal.Chap07Bounds

#print axioms LeanReal.Chap07Bounds.norm_h12_le
#print axioms LeanReal.Chap07Bounds.gaussK_le
#print axioms LeanReal.Chap07Bounds.neg_two_mul_le_gaussK
#print axioms LeanReal.Chap07Bounds.neg_sq_le_gaussK_real
#print axioms LeanReal.Chap07Bounds.integral_gaussK_le
#print axioms LeanReal.Chap07Bounds.le_integral_gaussK
#print axioms LeanReal.Chap07Bounds.le_integral_gaussK_real
#print axioms LeanReal.Chap07Bounds.nonneg_of_hop
#print axioms LeanReal.Chap07Bounds.gauss_bonnet_floor_any_sign
#print axioms LeanReal.Chap07Bounds.gauss_bonnet_floor_pos
#print axioms LeanReal.Chap07Bounds.gauss_bonnet_floor_neg
#print axioms LeanReal.Chap07Bounds.gauss_bonnet_floor_neg_codim_one
#print axioms LeanReal.Chap07Bounds.areaMeasure_real_univ
#print axioms LeanReal.Chap07Bounds.integral_areaMeasure_const
#print axioms LeanReal.Chap07Bounds.witness_round_sphere
#print axioms LeanReal.Chap07Bounds.IIq_complex_curve
#print axioms LeanReal.Chap07Bounds.norm_IIq_complex_curve
#print axioms LeanReal.Chap07Bounds.gaussK_complex_curve
#print axioms LeanReal.Chap07Bounds.witness_codim_two
#print axioms LeanReal.Chap07Bounds.witness_saddle_codim_one
#print axioms LeanReal.Chap07Bounds.mutant_codim_one_pointwise_false
#print axioms LeanReal.Chap07Bounds.mutant_codim_one_floor_false
#print axioms LeanReal.Chap07Bounds.mutant_strict_floor_false
#print axioms LeanReal.Chap07Bounds.planeCurv_eq_im
#print axioms LeanReal.Chap07Bounds.det_sq_add_dot_sq
#print axioms LeanReal.Chap07Bounds.det_ge
#print axioms LeanReal.Chap07Bounds.sq_norm_sq_div_le
#print axioms LeanReal.Chap07Bounds.one_div_card_le_sum_sq
#print axioms LeanReal.Chap07Bounds.several_planes_pointwise
#print axioms LeanReal.Chap07Bounds.several_planes_eq_iff
#print axioms LeanReal.Chap07Bounds.hasDerivAt_component
#print axioms LeanReal.Chap07Bounds.several_planes_lower_bound
#print axioms LeanReal.Chap07Bounds.norm_phaseVec
#print axioms LeanReal.Chap07Bounds.diagCircle_apply
#print axioms LeanReal.Chap07Bounds.hasDerivAt_expω
#print axioms LeanReal.Chap07Bounds.diagCircle_hasDerivAt
#print axioms LeanReal.Chap07Bounds.diagVel_hasDerivAt
#print axioms LeanReal.Chap07Bounds.norm_exp_ofReal_mul_I'
#print axioms LeanReal.Chap07Bounds.diag_circle
#print axioms LeanReal.Chap07Bounds.ω0_sq
#print axioms LeanReal.Chap07Bounds.ω0_pos
#print axioms LeanReal.Chap07Bounds.witness_vel_unit
#print axioms LeanReal.Chap07Bounds.witness_planeCurv
#print axioms LeanReal.Chap07Bounds.witness_several_planes
#print axioms LeanReal.Chap07Bounds.mutant_no_sqrt_m_false
#print axioms LeanReal.Chap07Bounds.mutant_le_one_false
#print axioms LeanReal.Chap07Bounds.pitfall_amplitude
#print axioms LeanReal.Chap07Bounds.planeCurv_diag
#print axioms LeanReal.Chap07Bounds.witness_several_planes_curve
#print axioms LeanReal.Chap07Bounds.curvSet_nonneg
#print axioms LeanReal.Chap07Bounds.CurveAdm.map
#print axioms LeanReal.Chap07Bounds.curvSet_mono
#print axioms LeanReal.Chap07Bounds.kappaStar_mono
#print axioms LeanReal.Chap07Bounds.incl_image_subset_cyl
#print axioms LeanReal.Chap07Bounds.monotonicity
#print axioms LeanReal.Chap07Bounds.arcC_hasDerivAt
#print axioms LeanReal.Chap07Bounds.arcC'_hasDerivAt
#print axioms LeanReal.Chap07Bounds.norm_arcC
#print axioms LeanReal.Chap07Bounds.arcC_adm
#print axioms LeanReal.Chap07Bounds.arcC_not_adm_half
#print axioms LeanReal.Chap07Bounds.witness_monotonicity
#print axioms LeanReal.Chap07Bounds.mutant_not_isometry_false
#print axioms LeanReal.Chap07Bounds.mutant_negative_d_false
#print axioms LeanReal.Chap07Bounds.totalCurv_le
#print axioms LeanReal.Chap07Bounds.knot_curve_bound
#print axioms LeanReal.Chap07Bounds.fenchel_curve_bound
#print axioms LeanReal.Chap07Bounds.norm_comb
#print axioms LeanReal.Chap07Bounds.circle_hasDerivAt
#print axioms LeanReal.Chap07Bounds.circleVel_hasDerivAt
#print axioms LeanReal.Chap07Bounds.circle_closedAdm
#print axioms LeanReal.Chap07Bounds.knot_gap
#print axioms LeanReal.Chap07Bounds.inner_one_I
#print axioms LeanReal.Chap07Bounds.witness_fenchel
#print axioms LeanReal.Chap07Bounds.witness_knot_curve
#print axioms LeanReal.Chap07Bounds.mutant_fenchel_strict_false
#print axioms LeanReal.Chap07Bounds.mutant_no_length_bound_false
#print axioms LeanReal.Chap07Bounds.sum_pow_four_le
#print axioms LeanReal.Chap07Bounds.product_torus
#print axioms LeanReal.Chap07Bounds.mutant_torus_strict_false
#print axioms LeanReal.Chap07Bounds.IIq_complex_curve_a
#print axioms LeanReal.Chap07Bounds.complex_curve_isotropy
#print axioms LeanReal.Chap07Bounds.mutant_isotropy_false
