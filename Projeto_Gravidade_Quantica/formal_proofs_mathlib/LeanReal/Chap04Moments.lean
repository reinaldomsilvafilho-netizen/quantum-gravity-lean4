import Mathlib.Analysis.Calculus.FDeriv.Mul
import Mathlib.Analysis.Calculus.FDeriv.Pi
import Mathlib.Analysis.Calculus.Deriv.Comp
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Gamma.Basic
import Mathlib.LinearAlgebra.Matrix.Notation

/-!
# Capitulo 4, `thm:msd` (item 4 do Lote B4 do `PLANO_LIVRO_A.md`): versao condicional

Fonte: `unified_quantum_gravity_book/chap04_simplicial_waves_porous_transport.tex`, Teorema
"Anisotropic Mean Squared Displacement" (`thm:msd`).

Enunciado do livro. Com `u₀ = δ` e `û(k,t) = E_β(−K σ(k) t^β)` (Teorema "Closed-Form Solution"):
> 1. `⟨x(t)⟩ = 0`;
> 2. `⟨x xᵀ⟩(t) = ∫ x xᵀ u(x,t) dx = K/(α² Γ(β+1)) · M₂(α) · t^β`, exatamente para todo `t > 0`,
> onde `M₂(α) = a Id + b 11ᵀ` e a matriz de segundos momentos do `thm:dispersion`.
Prova do livro: `⟨x_j⟩ = i ∂_j û(0)`, `⟨x_i x_j⟩ = −∂_i∂_j û(0)`; `∂_j û = E_β'(−Kσt^β)(−Kt^β ∂_jσ)`,
nulo em `k = 0` porque `∇σ(0) = 0` (σ par); `∂_i∂_j û(0) = −E_β'(0) K t^β ∂_i∂_jσ(0)`, com
`E_β'(0) = 1/Γ(β+1)` e `∂_i∂_jσ(0) = α⁻²(M₂)_{ij}`.

## Reducao declarada (CONDICIONAL)

* A Mathlib nao tem Mittag-Leffler nem derivada de Caputo. `E : ℝ → ℝ` e uma funcao dada,
  derivavel em toda parte com derivada `E₁`, e `E₁` derivavel em `0`. O valor
  `E₁ 0 = 1/Γ(β+1)` entra como HIPOTESE `hE10`.
* `σ : ℝ^d → ℝ` e uma funcao dada, Frechet-derivavel em toda parte com derivada `σ₁`, e `σ₁`
  Frechet-derivavel em `0` com derivada `σ₂` (a Hessiana de `σ` em `0`); `σ 0 = 0`, `σ₁ 0 = 0`.
  Que o simbolo do `thm:dispersion` tem essas propriedades, e que `Hess σ(0) = α⁻² M₂`, NAO e
  formalizado: a ultima igualdade entra como hipotese `hHess`, com `M₂` uma matriz dada.
* `c = K t^β` e um real. A ponte "momento de `u` = derivada de `û` em `0`" (a identidade
  `⟨x_i x_j⟩ = −∂_i∂_j û(0)`) NAO e formalizada: o teorema fala de `−∂_i∂_j û(0)` diretamente.
* O que a Lean prova: a regra da cadeia duas vezes, com o termo `E''·∇σ⊗∇σ` eliminado por
  `∇σ(0) = 0`; o gradiente de `û` em `0` e nulo; e a algebra final `K t^β/(α² Γ(β+1)) (M₂)_{ij}`.
* `ℝ^d` e `Fin d → ℝ` com a norma do sup; `∂_i∂_j f(0) = D²f(0)(e_i)(e_j)`.
-/

noncomputable section

namespace LeanReal.Chap04Moments

open ContinuousLinearMap

variable {d : ℕ}

/-- A transformada `û(k) = E(−c σ(k))`, com `c = K t^β` (Teorema "Closed-Form Solution"). -/
def uhat (E : ℝ → ℝ) (c : ℝ) (σ : (Fin d → ℝ) → ℝ) (k : Fin d → ℝ) : ℝ := E (-(c * σ k))

/-- Entrada `(i,j)` da Hessiana de `f` em `k`: `D²f(k)(e_i)(e_j)`. -/
def hess (f : (Fin d → ℝ) → ℝ) (k : Fin d → ℝ) (i j : Fin d) : ℝ :=
  fderiv ℝ (fderiv ℝ f) k (Pi.single i 1) (Pi.single j 1)

/-- Regra da cadeia: `Dû(k) = −c E'(−cσ(k)) Dσ(k)`. -/
theorem hasFDerivAt_uhat (E E₁ : ℝ → ℝ) (hE1 : ∀ x, HasDerivAt E (E₁ x) x) (c : ℝ)
    (σ : (Fin d → ℝ) → ℝ) (σ₁ : (Fin d → ℝ) → ((Fin d → ℝ) →L[ℝ] ℝ))
    (hσ1 : ∀ k, HasFDerivAt σ (σ₁ k) k) (k : Fin d → ℝ) :
    HasFDerivAt (uhat E c σ) ((-(c * E₁ (-(c * σ k)))) • σ₁ k) k := by
  have h1 : HasFDerivAt (fun k => -(c * σ k)) (-(c • σ₁ k)) k := ((hσ1 k).const_mul c).neg
  have h2 := (hE1 (-(c * σ k))).comp_hasFDerivAt k h1
  refine h2.congr_fderiv ?_
  ext v
  simp [smul_neg, mul_left_comm, mul_assoc]

/-- `Dû(k)` como funcao de `k`. -/
theorem fderiv_uhat (E E₁ : ℝ → ℝ) (hE1 : ∀ x, HasDerivAt E (E₁ x) x) (c : ℝ)
    (σ : (Fin d → ℝ) → ℝ) (σ₁ : (Fin d → ℝ) → ((Fin d → ℝ) →L[ℝ] ℝ))
    (hσ1 : ∀ k, HasFDerivAt σ (σ₁ k) k) :
    fderiv ℝ (uhat E c σ) = fun k => (-(c * E₁ (-(c * σ k)))) • σ₁ k :=
  funext fun k => (hasFDerivAt_uhat E E₁ hE1 c σ σ₁ hσ1 k).fderiv

/-- **`thm:msd` (1), deriva media**: `∇û(0) = 0` quando `∇σ(0) = 0`; logo
`⟨x_j⟩ = i ∂_j û(0) = 0`. -/
theorem fderiv_uhat_zero (E E₁ : ℝ → ℝ) (hE1 : ∀ x, HasDerivAt E (E₁ x) x) (c : ℝ)
    (σ : (Fin d → ℝ) → ℝ) (σ₁ : (Fin d → ℝ) → ((Fin d → ℝ) →L[ℝ] ℝ))
    (hσ1 : ∀ k, HasFDerivAt σ (σ₁ k) k) (hσ10 : σ₁ 0 = 0) :
    fderiv ℝ (uhat E c σ) 0 = 0 := by
  rw [fderiv_uhat E E₁ hE1 c σ σ₁ hσ1]
  simp [hσ10]

/-- **`thm:msd` (1)** na forma do livro: `i ∂_j û(0) = 0` para cada `j`. -/
theorem mean_drift (E E₁ : ℝ → ℝ) (hE1 : ∀ x, HasDerivAt E (E₁ x) x) (c : ℝ)
    (σ : (Fin d → ℝ) → ℝ) (σ₁ : (Fin d → ℝ) → ((Fin d → ℝ) →L[ℝ] ℝ))
    (hσ1 : ∀ k, HasFDerivAt σ (σ₁ k) k) (hσ10 : σ₁ 0 = 0) (j : Fin d) :
    Complex.I * (fderiv ℝ (uhat E c σ) 0 (Pi.single j 1) : ℂ) = 0 := by
  rw [fderiv_uhat_zero E E₁ hE1 c σ σ₁ hσ1 hσ10]
  simp

/-- **Hessiana de `û` em `0`**: `D²û(0) = −c E'(0) D²σ(0)`. E o passo central da prova do livro:
o termo `E''(0) (c ∇σ(0)) ⊗ (c ∇σ(0))` desaparece porque `∇σ(0) = 0`. -/
theorem fderiv_fderiv_uhat_zero (E E₁ : ℝ → ℝ) (hE1 : ∀ x, HasDerivAt E (E₁ x) x)
    (E₂0 : ℝ) (hE2 : HasDerivAt E₁ E₂0 0) (c : ℝ)
    (σ : (Fin d → ℝ) → ℝ) (σ₁ : (Fin d → ℝ) → ((Fin d → ℝ) →L[ℝ] ℝ))
    (hσ1 : ∀ k, HasFDerivAt σ (σ₁ k) k)
    (σ₂ : (Fin d → ℝ) →L[ℝ] ((Fin d → ℝ) →L[ℝ] ℝ)) (hσ2 : HasFDerivAt σ₁ σ₂ 0)
    (hσ0 : σ 0 = 0) (hσ10 : σ₁ 0 = 0) :
    fderiv ℝ (fderiv ℝ (uhat E c σ)) 0 = (-(c * E₁ 0)) • σ₂ := by
  rw [fderiv_uhat E E₁ hE1 c σ σ₁ hσ1]
  -- a funcao escalar `a k = −c E'(−cσ(k))`
  have ha0 : HasFDerivAt (fun k => -(c * σ k)) (-(c • σ₁ 0)) 0 := ((hσ1 0).const_mul c).neg
  have hE2' : HasDerivAt E₁ E₂0 (-(c * σ 0)) := by simpa [hσ0] using hE2
  have ha : HasFDerivAt (fun k => -(c * E₁ (-(c * σ k))))
      (-(c • (E₂0 • (-(c • σ₁ 0))))) 0 :=
    ((hE2'.comp_hasFDerivAt 0 ha0).const_mul c).neg
  have h : HasFDerivAt (fun k => (-(c * E₁ (-(c * σ k)))) • σ₁ k)
      ((-(c * E₁ (-(c * σ 0)))) • σ₂ + (-(c • (E₂0 • (-(c • σ₁ 0))))).smulRight (σ₁ 0)) 0 :=
    ha.smul hσ2
  rw [h.fderiv]
  ext v w
  simp [hσ0, hσ10]

/-- **`thm:msd` (2)**, condicional: com `E'(0) = 1/Γ(β+1)` (`hE10`) e
`∂_i∂_jσ(0) = α⁻²(M₂)_{ij}` (`hHess`), para `c = K t^β`:
`−∂_i∂_j û(0) = K/(α² Γ(β+1)) (M₂)_{ij} t^β`. -/
theorem msd (E E₁ : ℝ → ℝ) (hE1 : ∀ x, HasDerivAt E (E₁ x) x)
    (E₂0 : ℝ) (hE2 : HasDerivAt E₁ E₂0 0)
    (σ : (Fin d → ℝ) → ℝ) (σ₁ : (Fin d → ℝ) → ((Fin d → ℝ) →L[ℝ] ℝ))
    (hσ1 : ∀ k, HasFDerivAt σ (σ₁ k) k)
    (σ₂ : (Fin d → ℝ) →L[ℝ] ((Fin d → ℝ) →L[ℝ] ℝ)) (hσ2 : HasFDerivAt σ₁ σ₂ 0)
    (hσ0 : σ 0 = 0) (hσ10 : σ₁ 0 = 0)
    (K t β α : ℝ) (hα : α ≠ 0) (hΓ : Real.Gamma (β + 1) ≠ 0)
    (hE10 : E₁ 0 = 1 / Real.Gamma (β + 1))
    (M₂ : Matrix (Fin d) (Fin d) ℝ) (hHess : ∀ i j, hess σ 0 i j = (1 / α ^ 2) * M₂ i j)
    (i j : Fin d) :
    -(hess (uhat E (K * t ^ β) σ) 0 i j) =
      K / (α ^ 2 * Real.Gamma (β + 1)) * M₂ i j * t ^ β := by
  have hσ2' : fderiv ℝ (fderiv ℝ σ) 0 = σ₂ := by
    rw [show fderiv ℝ σ = σ₁ from funext fun k => (hσ1 k).fderiv]
    exact hσ2.fderiv
  have hM : σ₂ (Pi.single i 1) (Pi.single j 1) = (1 / α ^ 2) * M₂ i j := by
    rw [← hHess i j, hess, hσ2']
  unfold hess
  rw [fderiv_fderiv_uhat_zero E E₁ hE1 E₂0 hE2 _ σ σ₁ hσ1 σ₂ hσ2 hσ0 hσ10]
  simp only [smul_apply, smul_eq_mul, hM, hE10]
  field_simp

/-! ## Testemunha: `d = 1`, `E = exp`, `σ(k) = k²`, `c = 1` (`K = α = β = t = 1`, `M₂ = [2]`)

Aqui `û(k) = e^{−k²}`, `û''(0) = −2 ≠ 0`: a Hessiana nao e trivial, e `E'(0) = 1 = 1/Γ(2)`. -/

/-- A projecao `k ↦ k 0` em `Fin 1 → ℝ`. -/
def L1 : (Fin 1 → ℝ) →L[ℝ] ℝ := ContinuousLinearMap.proj 0

/-- `σ(k) = k₀²`. -/
def σsq (k : Fin 1 → ℝ) : ℝ := k 0 ^ 2

/-- `Dσ(k) = 2k₀ · proj₀`. -/
def σsq₁ (k : Fin 1 → ℝ) : (Fin 1 → ℝ) →L[ℝ] ℝ := (2 * k 0) • L1

/-- `D²σ = 2 proj₀ ⊗ proj₀`. -/
def σsq₂ : (Fin 1 → ℝ) →L[ℝ] ((Fin 1 → ℝ) →L[ℝ] ℝ) := ((2 : ℝ) • L1).smulRight L1

theorem σsq_hasFDerivAt (k : Fin 1 → ℝ) : HasFDerivAt σsq (σsq₁ k) k := by
  have h : HasFDerivAt (fun k : Fin 1 → ℝ => L1 k * L1 k) (L1 k • L1 + L1 k • L1) k :=
    L1.hasFDerivAt.mul L1.hasFDerivAt
  refine (h.congr_fderiv ?_).congr_of_eventuallyEq (Filter.Eventually.of_forall fun x => ?_)
  · ext v; simp [σsq₁, L1]; ring
  · simp [σsq, L1, sq]

theorem σsq₁_hasFDerivAt : HasFDerivAt σsq₁ σsq₂ 0 := by
  have h : HasFDerivAt (fun k : Fin 1 → ℝ => 2 * L1 k) ((2 : ℝ) • L1) 0 :=
    L1.hasFDerivAt.const_mul 2
  exact h.smul_const L1

theorem σsq₂_apply : σsq₂ (Pi.single 0 1) (Pi.single 0 1) = 2 := by
  simp [σsq₂, L1]

theorem Gamma_two : Real.Gamma ((1 : ℝ) + 1) = 1 := by
  rw [Real.Gamma_add_one one_ne_zero, Real.Gamma_one]; ring

theorem witness_hypotheses :
    (∀ x, HasDerivAt Real.exp (Real.exp x) x) ∧ HasDerivAt Real.exp (Real.exp 0) 0 ∧
    (∀ k, HasFDerivAt σsq (σsq₁ k) k) ∧ HasFDerivAt σsq₁ σsq₂ 0 ∧
    σsq 0 = 0 ∧ σsq₁ 0 = 0 ∧ (1 : ℝ) ≠ 0 ∧ Real.Gamma ((1 : ℝ) + 1) ≠ 0 ∧
    Real.exp 0 = 1 / Real.Gamma ((1 : ℝ) + 1) ∧
    (∀ i j, hess σsq 0 i j = (1 / (1 : ℝ) ^ 2) * (!![2] : Matrix (Fin 1) (Fin 1) ℝ) i j) := by
  refine ⟨fun x => Real.hasDerivAt_exp x, Real.hasDerivAt_exp 0, σsq_hasFDerivAt,
    σsq₁_hasFDerivAt, by simp [σsq], by simp [σsq₁], one_ne_zero, ?_, ?_, ?_⟩
  · rw [Gamma_two]; exact one_ne_zero
  · rw [Gamma_two]; simp
  · intro i j
    have hi : i = 0 := Subsingleton.elim _ _
    have hj : j = 0 := Subsingleton.elim _ _
    subst hi hj
    unfold hess
    rw [show fderiv ℝ σsq = σsq₁ from funext fun k => (σsq_hasFDerivAt k).fderiv,
      σsq₁_hasFDerivAt.fderiv, σsq₂_apply]
    simp

/-- Na testemunha, `−û''(0) = 2`: valor concreto da conclusao do teorema. -/
theorem witness_value :
    -(hess (uhat Real.exp (1 * (1 : ℝ) ^ (1 : ℝ)) σsq) 0 0 0) = 2 := by
  obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9, h10⟩ := witness_hypotheses
  rw [msd Real.exp Real.exp h1 (Real.exp 0) h2 σsq σsq₁ h3 σsq₂ h4 h5 h6 1 1 1 1 h7 h8 h9
    !![2] h10 0 0]
  rw [Gamma_two]
  simp

/-! ## Mutantes provados FALSOS -/

/-- `σ(k) = k₀` (gradiente NAO nulo em `0`), `Dσ = proj₀` constante, `D²σ = 0`. -/
def σlin (k : Fin 1 → ℝ) : ℝ := k 0

theorem σlin_hasFDerivAt (k : Fin 1 → ℝ) : HasFDerivAt σlin L1 k := L1.hasFDerivAt

/-- Mutante 1: sem a hipotese `∇σ(0) = 0`, a formula `D²û(0) = −c E'(0) D²σ(0)` e falsa.
Contraexemplo: `E = exp`, `σ(k) = k₀`, `c = 1`: `û = e^{−k₀}`, `û''(0) = 1`, mas `D²σ = 0`. -/
theorem mutant_no_gradient_false :
    ¬ (∀ (E E₁ : ℝ → ℝ), (∀ x, HasDerivAt E (E₁ x) x) → ∀ (E₂0 : ℝ), HasDerivAt E₁ E₂0 0 →
        ∀ (c : ℝ) (σ : (Fin 1 → ℝ) → ℝ) (σ₁ : (Fin 1 → ℝ) → ((Fin 1 → ℝ) →L[ℝ] ℝ)),
        (∀ k, HasFDerivAt σ (σ₁ k) k) →
        ∀ (σ₂ : (Fin 1 → ℝ) →L[ℝ] ((Fin 1 → ℝ) →L[ℝ] ℝ)), HasFDerivAt σ₁ σ₂ 0 → σ 0 = 0 →
        fderiv ℝ (fderiv ℝ (uhat E c σ)) 0 = (-(c * E₁ 0)) • σ₂) := by
  intro h
  have := h Real.exp Real.exp (fun x => Real.hasDerivAt_exp x) (Real.exp 0) (Real.hasDerivAt_exp 0)
    1 σlin (fun _ => L1) σlin_hasFDerivAt 0 (hasFDerivAt_const _ _) (by simp [σlin])
  -- calculo direto de `D²û(0)` para `û = e^{−k₀}`
  have hD : fderiv ℝ (uhat Real.exp 1 σlin) = fun k => (-(1 * Real.exp (-(1 * σlin k)))) • L1 :=
    fderiv_uhat Real.exp Real.exp (fun x => Real.hasDerivAt_exp x) 1 σlin (fun _ => L1)
      σlin_hasFDerivAt
  have ha : HasFDerivAt (fun k => -(1 * Real.exp (-(1 * σlin k))))
      (-((1 : ℝ) • (Real.exp (-(1 * σlin 0)) • (-((1 : ℝ) • L1))))) 0 :=
    (((Real.hasDerivAt_exp _).comp_hasFDerivAt 0
      ((σlin_hasFDerivAt 0).const_mul 1).neg).const_mul 1).neg
  have h2 : fderiv ℝ (fun k => (-(1 * Real.exp (-(1 * σlin k)))) • L1) 0 =
      (-((1 : ℝ) • (Real.exp (-(1 * σlin 0)) • (-((1 : ℝ) • L1))))).smulRight L1 :=
    (ha.smul_const L1).fderiv
  rw [hD, h2] at this
  have := congrArg (fun T => T (Pi.single 0 1) (Pi.single 0 1)) this
  simp [σlin, L1] at this

/-- Mutante 2: sem o fator `E'(0)` (formula `D²û(0) = −c D²σ(0)`), falso para `E(x) = e^{2x}`
(`E'(0) = 2`) com a testemunha `σ(k) = k₀²`: `−4 ≠ −2`. -/
theorem mutant_no_Eprime_false :
    ¬ (∀ (E E₁ : ℝ → ℝ), (∀ x, HasDerivAt E (E₁ x) x) → ∀ (E₂0 : ℝ), HasDerivAt E₁ E₂0 0 →
        ∀ (c : ℝ) (σ : (Fin 1 → ℝ) → ℝ) (σ₁ : (Fin 1 → ℝ) → ((Fin 1 → ℝ) →L[ℝ] ℝ)),
        (∀ k, HasFDerivAt σ (σ₁ k) k) →
        ∀ (σ₂ : (Fin 1 → ℝ) →L[ℝ] ((Fin 1 → ℝ) →L[ℝ] ℝ)), HasFDerivAt σ₁ σ₂ 0 → σ 0 = 0 →
        σ₁ 0 = 0 → fderiv ℝ (fderiv ℝ (uhat E c σ)) 0 = (-c) • σ₂) := by
  intro h
  have hE : ∀ x, HasDerivAt (fun x => Real.exp (2 * x)) (2 * Real.exp (2 * x)) x := by
    intro x
    have := ((hasDerivAt_id x).const_mul 2).exp
    simpa [mul_comm] using this
  have hE' : HasDerivAt (fun x => 2 * Real.exp (2 * x)) (2 * (2 * Real.exp (2 * 0))) 0 :=
    (hE 0).const_mul 2
  have h1 := h (fun x => Real.exp (2 * x)) (fun x => 2 * Real.exp (2 * x)) hE _ hE' 1 σsq σsq₁
    σsq_hasFDerivAt σsq₂ σsq₁_hasFDerivAt (by simp [σsq]) (by simp [σsq₁])
  have h2 := fderiv_fderiv_uhat_zero (fun x => Real.exp (2 * x)) (fun x => 2 * Real.exp (2 * x))
    hE _ hE' 1 σsq σsq₁ σsq_hasFDerivAt σsq₂ σsq₁_hasFDerivAt (by simp [σsq]) (by simp [σsq₁])
  rw [h2] at h1
  have := congrArg (fun T => T (Pi.single 0 1) (Pi.single 0 1)) h1
  simp only [smul_apply, smul_eq_mul, σsq₂_apply] at this
  norm_num at this

end LeanReal.Chap04Moments

#print axioms LeanReal.Chap04Moments.hasFDerivAt_uhat
#print axioms LeanReal.Chap04Moments.fderiv_uhat_zero
#print axioms LeanReal.Chap04Moments.mean_drift
#print axioms LeanReal.Chap04Moments.fderiv_fderiv_uhat_zero
#print axioms LeanReal.Chap04Moments.msd
#print axioms LeanReal.Chap04Moments.witness_hypotheses
#print axioms LeanReal.Chap04Moments.witness_value
#print axioms LeanReal.Chap04Moments.mutant_no_gradient_false
#print axioms LeanReal.Chap04Moments.mutant_no_Eprime_false
