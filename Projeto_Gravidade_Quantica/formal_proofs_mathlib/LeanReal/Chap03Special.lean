import LeanReal.Chap03Analysis
import Mathlib.Analysis.SpecialFunctions.Gamma.Digamma
import Mathlib.NumberTheory.Real.GoldenRatio
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Analysis.SpecialFunctions.Pow.Deriv
import Mathlib.Analysis.SpecialFunctions.Pow.Continuity
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.Calculus.Deriv.Shift
import Mathlib.Topology.Order.IntermediateValue

/-!
# Capitulo 3: funcoes especiais (Lote B3 do `PLANO_LIVRO_A.md`)

Fonte: `unified_quantum_gravity_book/chap03_pascal_simplex_continuous_multinomials.tex`.
Reaproveita `LeanReal.Chap03.cbinom` (coeficiente binomial continuo complexo) e
`LeanReal.Chap03Analysis.rbinom` (versao real), com `cbinom_ofReal`, `rbinom_pos`,
`rbinom_symm` e `rbinom_continuousOn`.

## Item 1. Proposicao "Digamma Partial Differential Equation System" (sem rotulo)

> `ψ = Γ'/Γ`. No aberto onde nenhum de `x+1`, `y+1`, `x-y+1` esta em `ℤ_{≤0}`:
> `∂_x binom(x,y) = binom(x,y)[ψ(x+1) - ψ(x-y+1)]` (eq:pde_x),
> `∂_y binom(x,y) = binom(x,y)[ψ(x-y+1) - ψ(y+1)]` (eq:pde_y),
> e a soma e a equacao de transporte `(∂_x + ∂_y) binom = binom[ψ(x+1) - ψ(y+1)]`,
> que vale literalmente sempre que `y+1 ∉ ℤ_{≤0}`. Exemplo: em `y = -1` a (eq:pde_y)
> estendida da `∂_y binom(x,y) = 1/(x+1)`.

Formalizacao sobre `ℂ`, com `Complex.digamma = logDeriv Gamma` da Mathlib. As derivadas
parciais sao `HasDerivAt` nas funcoes de uma variavel `x ↦ binom(x,y)` e `y ↦ binom(x,y)`;
a hipotese "fora dos polos" e `∀ m : ℕ, s ≠ -m` para cada um dos tres argumentos
(`pde_x`, `pde_y`, `pde_sum`). A equacao de transporte e a derivada de `t ↦ binom(x+t, y+t)`
em `t = 0` (`transport`), provada so com `x+1, y+1 ∉ ℤ_{≤0}`, como o livro afirma. O exemplo
`y = -1` e `deriv_y_at_neg_one`, e serve de mutante: sem a hipotese sobre `y+1`, a (eq:pde_y)
literal e falsa. A extensao holomorfa dos produtos nas outras retas fica fora.

## Item 2. Teorema `thm:fibonacci`, nucleo algebrico

> `F_cont(x) = ∫_0^{x/2} binom(x-y, y) dy ~ φ^{x+1}/√5`. Na prova: `S(ξ) = (1-ξ)ln(1-ξ) -
> ξ ln ξ - (1-2ξ) ln(1-2ξ)`, `S'(ξ) = ln((1-2ξ)²/(ξ(1-ξ)))`, `S'(ξ*) = 0 ⇔ (1-2ξ*)² = ξ*(1-ξ*)`,
> raiz unica em `[0,1/2]`: `ξ* = (5-√5)/10`; `S(ξ*) = ln φ`; `S''(ξ*) = -5√5`; e
> `x e^{xS(ξ*)} / √(2πxξ*(1-2ξ*)/(1-ξ*)) · √(2π/(x|S''(ξ*)|)) = φ^{x+1}/√5`.
> Raio geral `α > 0`: `S_α(ξ) = u ln u - ξ ln ξ - w ln w`, `u = 1-αξ`, `w = 1-(α+1)ξ`,
> `S_α' = -α ln u - ln ξ + (α+1) ln w`, `S_α'' = α²/u - 1/ξ - (α+1)²/w < 0` (Cauchy–Schwarz),
> maximizador unico `ξ*` caracterizado por `w*^{α+1} = ξ* u*^α`, `S_α(ξ*) = ln(u*/w*)`,
> `z = u*/w*` satisfaz `z^α(z-1) = 1`, e `λ_α > 1` e a unica raiz `z > 1` disso.

Formalizado: todas as identidades acima (derivadas como `HasDerivAt`, valores em `ξ*`, a
identidade do prefator de Laplace para `x > 0`); para `α` geral, a concavidade estrita, a
caracterizacao do ponto critico, `S_α(ξ*) = ln(u*/w*)`, `z^α(z-1) = 1`, a unicidade do ponto
critico (por `S_α'` estritamente decrescente), a existencia e unicidade de `λ_α`.
NAO formalizado: Stirling, o metodo de Laplace e a assintotica `~`; a existencia do
maximizador para `α ≠ 1` (os limites de `S_α'` nas pontas).

## Item 3. Proposicao `prop:fractional_props`, (1) e (2) para `m = 2`

> `K_α(y) = Γ(α+1)/∏_{j=1}^m Γ(y_j+1)` em `Δ_{m-1}(α)` (com `y_m = α - ∑_{j<m} y_j`).
> (1) `K_α` e `C^∞` e estritamente positivo no interior, com `K_α(0) = 1`.
> (2) Para `f` limitada e uniformemente continua, `lim_{α→0⁺} D^α f(x) = f(x)`, onde
> `D^α f(x) = (1/I(α)) ∫_0^α binom(α,y) f(x-y) dy` e `I(α) = ∫_0^α binom(α,y) dy` (`m = 2`).
> (3) `D^α e^{λx} = e^{λx} G_α(λ)`, `G_α` inteira, `G_α(0) = 1`.

Formalizado: `K` no vetor baricentrico completo `y ∈ ℝ^m` (`K_zero`, `K_pos`, e `K_two`
liga `m = 2` a `rbinom`); em 1D, `I α > 0`, a estimativa `|D^α f(x) - f(x)| ≤ sup_{[0,α]}
|f(x-y) - f(x)|` (`D_sub_le`) e o limite (`identity_limit`), que so precisa de `f` continua;
a forma do livro (limitada, uniformemente continua) e o corolario `identity_limit_book`,
com a limitacao nao usada. (3) para `λ` REAL (`D_exp`, `G_zero`); o caso `λ ∈ ℂ` e a
analiticidade de `G_α` ficam fora, assim como a suavidade `C^∞` de `K_α` e o caso `m ≥ 3` de (2).
-/

noncomputable section

namespace LeanReal.Chap03Special

open Set

/-! ## Item 1: sistema de EDPs do digama -/

section Digamma

open LeanReal.Chap03 (cbinom)

/-- Fora dos polos, `Γ` tem derivada `Γ(s)·ψ(s)` em `s` (`ψ = logDeriv Γ`). -/
theorem hasDerivAt_Gamma_digamma {s : ℂ} (hs : ∀ m : ℕ, s ≠ -(m : ℂ)) :
    HasDerivAt Complex.Gamma (Complex.Gamma s * Complex.digamma s) s := by
  have hd := (Complex.differentiableAt_Gamma s hs).hasDerivAt
  have hG : Complex.Gamma s ≠ 0 := Complex.Gamma_ne_zero hs
  have : Complex.Gamma s * Complex.digamma s = deriv Complex.Gamma s := by
    rw [Complex.digamma_def, logDeriv_apply]
    field_simp
  rw [this]
  exact hd

/-- Derivada de `s ↦ Γ(a + s)⁻¹` fora dos polos: `-ψ(a+s)/Γ(a+s)`, versao com `g` afim. -/
theorem hasDerivAt_inv_Gamma_comp {g : ℂ → ℂ} {g' s : ℂ} (hg : HasDerivAt g g' s)
    (h : ∀ m : ℕ, g s ≠ -(m : ℂ)) :
    HasDerivAt (fun z => (Complex.Gamma (g z))⁻¹)
      (-(g' * Complex.digamma (g s)) / Complex.Gamma (g s)) s := by
  have hG : Complex.Gamma (g s) ≠ 0 := Complex.Gamma_ne_zero h
  have hc : HasDerivAt (fun z => Complex.Gamma (g z))
      (Complex.Gamma (g s) * Complex.digamma (g s) * g') s :=
    (hasDerivAt_Gamma_digamma h).comp s hg
  have := hc.inv hG
  convert this using 1
  field_simp

/-- Um numero complexo de parte real positiva nao e um inteiro `≤ 0`. -/
theorem ne_neg_nat_of_re_pos {z : ℂ} (hz : 0 < z.re) : ∀ m : ℕ, z ≠ -(m : ℂ) := by
  intro m h
  have := congrArg Complex.re h
  simp at this
  have : (0 : ℝ) ≤ m := m.cast_nonneg
  linarith

/-- **Proposicao "Digamma PDE System"**, (eq:pde_x): fora dos polos de `x+1` e `x-y+1`,
`∂_x binom(x,y) = binom(x,y)[ψ(x+1) - ψ(x-y+1)]`. -/
theorem pde_x (x y : ℂ) (hx : ∀ m : ℕ, x + 1 ≠ -(m : ℂ))
    (hxy : ∀ m : ℕ, x - y + 1 ≠ -(m : ℂ)) :
    HasDerivAt (fun x => cbinom x y)
      (cbinom x y * (Complex.digamma (x + 1) - Complex.digamma (x - y + 1))) x := by
  have hG2 : Complex.Gamma (x - y + 1) ≠ 0 := Complex.Gamma_ne_zero hxy
  have h1 : HasDerivAt (fun x : ℂ => Complex.Gamma (x + 1))
      (Complex.Gamma (x + 1) * Complex.digamma (x + 1)) x :=
    (hasDerivAt_Gamma_digamma hx).comp_add_const x 1
  have h3 : HasDerivAt (fun x : ℂ => (Complex.Gamma (x - y + 1))⁻¹)
      (-(1 * Complex.digamma (x - y + 1)) / Complex.Gamma (x - y + 1)) x :=
    hasDerivAt_inv_Gamma_comp (((hasDerivAt_id x).sub_const y).add_const 1) hxy
  have := (h1.mul_const (Complex.Gamma (y + 1))⁻¹).mul h3
  unfold cbinom
  convert this using 1
  field_simp
  ring

/-- **Proposicao "Digamma PDE System"**, (eq:pde_y): fora dos polos de `y+1` e `x-y+1`,
`∂_y binom(x,y) = binom(x,y)[ψ(x-y+1) - ψ(y+1)]`. -/
theorem pde_y (x y : ℂ) (hy : ∀ m : ℕ, y + 1 ≠ -(m : ℂ))
    (hxy : ∀ m : ℕ, x - y + 1 ≠ -(m : ℂ)) :
    HasDerivAt (fun y => cbinom x y)
      (cbinom x y * (Complex.digamma (x - y + 1) - Complex.digamma (y + 1))) y := by
  have hG1 : Complex.Gamma (y + 1) ≠ 0 := Complex.Gamma_ne_zero hy
  have hG2 : Complex.Gamma (x - y + 1) ≠ 0 := Complex.Gamma_ne_zero hxy
  have h2 : HasDerivAt (fun y : ℂ => (Complex.Gamma (y + 1))⁻¹)
      (-(1 * Complex.digamma (y + 1)) / Complex.Gamma (y + 1)) y :=
    hasDerivAt_inv_Gamma_comp ((hasDerivAt_id y).add_const 1) hy
  have h3 : HasDerivAt (fun y : ℂ => (Complex.Gamma (x - y + 1))⁻¹)
      (-(-1 * Complex.digamma (x - y + 1)) / Complex.Gamma (x - y + 1)) y :=
    hasDerivAt_inv_Gamma_comp (((hasDerivAt_id y).const_sub x).add_const 1) hxy
  have := ((hasDerivAt_const y (Complex.Gamma (x + 1))).mul h2).mul h3
  unfold cbinom
  convert this using 1
  simp only [Pi.mul_apply]
  field_simp
  ring

/-- Soma de (eq:pde_x) e (eq:pde_y) no aberto: os dois valores de derivada somam
`binom(x,y)[ψ(x+1) - ψ(y+1)]` (equacao de transporte advectivo). -/
theorem pde_sum (x y : ℂ) :
    cbinom x y * (Complex.digamma (x + 1) - Complex.digamma (x - y + 1)) +
      cbinom x y * (Complex.digamma (x - y + 1) - Complex.digamma (y + 1)) =
    cbinom x y * (Complex.digamma (x + 1) - Complex.digamma (y + 1)) := by
  ring

/-- **Equacao de transporte literal**: a derivada de `t ↦ binom(x+t, y+t)` em `t = 0` e
`binom(x,y)[ψ(x+1) - ψ(y+1)]`, so com `x+1, y+1 ∉ ℤ_{≤0}` (nenhuma hipotese sobre `x-y`,
como o livro afirma: "holds literally whenever `y+1 ∉ ℤ_{≤0}`"). -/
theorem transport (x y : ℂ) (hx : ∀ m : ℕ, x + 1 ≠ -(m : ℂ))
    (hy : ∀ m : ℕ, y + 1 ≠ -(m : ℂ)) :
    HasDerivAt (fun t => cbinom (x + t) (y + t))
      (cbinom x y * (Complex.digamma (x + 1) - Complex.digamma (y + 1))) 0 := by
  have hG1 : Complex.Gamma (y + 1) ≠ 0 := Complex.Gamma_ne_zero hy
  have hfun : (fun t => cbinom (x + t) (y + t)) = fun t =>
      Complex.Gamma (x + t + 1) * (Complex.Gamma (y + t + 1))⁻¹ *
        (Complex.Gamma (x - y + 1))⁻¹ := by
    funext t
    unfold cbinom
    rw [show x + t - (y + t) + 1 = x - y + 1 by ring]
  rw [hfun]
  have h1 : HasDerivAt (fun t : ℂ => Complex.Gamma (x + t + 1))
      (Complex.Gamma (x + 1) * Complex.digamma (x + 1)) 0 := by
    have hx' : ∀ m : ℕ, x + 0 + 1 ≠ -(m : ℂ) := by simpa using hx
    have := (hasDerivAt_Gamma_digamma hx').comp (0 : ℂ)
      (((hasDerivAt_id' (0 : ℂ)).const_add x).add_const 1)
    simpa [Function.comp_def] using this
  have h2 : HasDerivAt (fun t : ℂ => (Complex.Gamma (y + t + 1))⁻¹)
      (-(Complex.digamma (y + 1)) / Complex.Gamma (y + 1)) 0 := by
    have hg : HasDerivAt (fun t : ℂ => y + t + 1) 1 0 :=
      ((hasDerivAt_id' (0 : ℂ)).const_add y).add_const 1
    have := hasDerivAt_inv_Gamma_comp hg (fun m => by simpa using hy m)
    simpa using this
  have := (h1.mul h2).mul_const (Complex.Gamma (x - y + 1))⁻¹
  refine this.congr_deriv ?_
  unfold cbinom
  simp only [add_zero, div_eq_mul_inv]
  ring

/-- Derivada de `s ↦ (Γ(s+1))⁻¹` em `s = -1`: vale `1`, porque `(Γ)⁻¹(s) = s·(Γ(s+1))⁻¹`
e `Γ(1) = 1`. -/
theorem hasDerivAt_inv_Gamma_succ_at_neg_one :
    HasDerivAt (fun s : ℂ => (Complex.Gamma (s + 1))⁻¹) 1 (-1) := by
  have hfun : (fun s : ℂ => (Complex.Gamma (s + 1))⁻¹) =
      fun s => (s + 1) * (Complex.Gamma (s + 1 + 1))⁻¹ := by
    funext s
    exact Complex.one_div_Gamma_eq_self_mul_one_div_Gamma_add_one (s + 1)
  rw [hfun]
  have hd : DifferentiableAt ℂ (fun s : ℂ => (Complex.Gamma (s + 1 + 1))⁻¹) (-1) := by
    have h := Complex.differentiable_one_div_Gamma.differentiableAt
      (x := (-1 : ℂ) + 1 + 1)
    have hf : DifferentiableAt ℂ (fun s : ℂ => s + 1 + 1) (-1) := by fun_prop
    have hc := h.comp (-1) hf
    exact hc
  have := ((hasDerivAt_id' (-1 : ℂ)).add_const 1).mul hd.hasDerivAt
  refine this.congr_deriv ?_
  norm_num [Complex.Gamma_one]

/-- **Exemplo do livro**: em `y = -1`, `∂_y binom(x,y) = 1/(x+1)` para `x+1 ∉ ℤ_{≤0}`.
Aqui `binom(x,-1) = 0` e `ψ(0)` tem polo; a derivada vem da reciproca inteira `1/Γ`. -/
theorem deriv_y_at_neg_one (x : ℂ) (hx : ∀ m : ℕ, x + 1 ≠ -(m : ℂ)) :
    HasDerivAt (fun y => cbinom x y) (1 / (x + 1)) (-1) := by
  have hx0 : x + 1 ≠ 0 := by simpa using hx 0
  have hG1 : Complex.Gamma (x + 1) ≠ 0 := Complex.Gamma_ne_zero hx
  have hG2 : Complex.Gamma (x + 1 + 1) = (x + 1) * Complex.Gamma (x + 1) :=
    Complex.Gamma_add_one (x + 1) hx0
  have h3 : DifferentiableAt ℂ (fun y : ℂ => (Complex.Gamma (x - y + 1))⁻¹) (-1) := by
    have h := Complex.differentiable_one_div_Gamma.differentiableAt
      (x := x - (-1 : ℂ) + 1)
    have hf : DifferentiableAt ℂ (fun y : ℂ => x - y + 1) (-1) := by fun_prop
    have hc := h.comp (-1) hf
    exact hc
  have := ((hasDerivAt_const (-1 : ℂ) (Complex.Gamma (x + 1))).mul
    hasDerivAt_inv_Gamma_succ_at_neg_one).mul h3.hasDerivAt
  unfold cbinom
  refine this.congr_deriv ?_
  simp only [Pi.mul_apply]
  rw [show x - (-1 : ℂ) + 1 = x + 1 + 1 by ring, hG2, neg_add_cancel, Complex.Gamma_zero,
    inv_zero]
  field_simp
  ring

/-- `ψ(2) - ψ(3/2) = 2 ln 2 - 1`, pela recorrencia e por `ψ(1)`, `ψ(1/2)` da Mathlib. -/
theorem digamma_two_sub_three_halves :
    Complex.digamma 2 - Complex.digamma (3 / 2) = 2 * Complex.log 2 - 1 := by
  have h1 : Complex.digamma 2 = Complex.digamma 1 + 1⁻¹ := by
    have := Complex.digamma_apply_add_one 1 (ne_neg_nat_of_re_pos (by norm_num))
    rw [← this]
    norm_num
  have h2 : Complex.digamma (3 / 2) = Complex.digamma (1 / 2) + (1 / 2 : ℂ)⁻¹ := by
    have := Complex.digamma_apply_add_one (1 / 2) (ne_neg_nat_of_re_pos (by norm_num))
    rw [← this]
    norm_num
  rw [h1, h2, Complex.digamma_one, Complex.digamma_one_half]
  ring

/-- `2 ln 2 - 1 ≠ 0` em `ℂ` (porque `ln 2 > 0.69`). -/
theorem two_log_two_sub_one_ne_zero : (2 * Complex.log 2 - 1 : ℂ) ≠ 0 := by
  have hl : Complex.log 2 = ((Real.log 2 : ℝ) : ℂ) := by
    rw [Complex.ofReal_log (by norm_num : (0 : ℝ) ≤ 2)]
    norm_num
  have hcast : (2 * Complex.log 2 - 1 : ℂ) = ((2 * Real.log 2 - 1 : ℝ) : ℂ) := by
    rw [hl]; push_cast; ring
  rw [hcast, Complex.ofReal_ne_zero]
  have := Real.log_two_gt_d9
  intro h
  linarith

/-- Testemunha nao degenerada de `pde_x`: `x = 1`, `y = 1/2`. As tres hipoteses valem,
`binom(1,1/2) = 4/π ≠ 0` e `ψ(2) - ψ(3/2) = 2 ln 2 - 1 ≠ 0`, logo a derivada e nao nula. -/
theorem witness_pde_x :
    (∀ m : ℕ, (1 : ℂ) + 1 ≠ -(m : ℂ)) ∧ (∀ m : ℕ, (1 / 2 : ℂ) + 1 ≠ -(m : ℂ)) ∧
      (∀ m : ℕ, (1 : ℂ) - 1 / 2 + 1 ≠ -(m : ℂ)) ∧
      cbinom 1 (1 / 2) * (Complex.digamma (1 + 1) - Complex.digamma (1 - 1 / 2 + 1)) ≠ 0 := by
  refine ⟨ne_neg_nat_of_re_pos (by norm_num), ne_neg_nat_of_re_pos (by norm_num),
    ne_neg_nat_of_re_pos (by norm_num), ?_⟩
  have hb : cbinom 1 (1 / 2) ≠ 0 := by
    have := LeanReal.Chap03Analysis.cbinom_ofReal 1 (1 / 2)
    push_cast at this
    rw [this, Complex.ofReal_ne_zero]
    exact (LeanReal.Chap03Analysis.rbinom_pos (by norm_num) (by norm_num) (by norm_num)).ne'
  rw [show (1 : ℂ) + 1 = 2 by norm_num, show (1 : ℂ) - 1 / 2 + 1 = 3 / 2 by norm_num,
    digamma_two_sub_three_halves]
  exact mul_ne_zero hb two_log_two_sub_one_ne_zero

/-- Mutante (sinal trocado em (eq:pde_x)): falso na testemunha, por unicidade da derivada. -/
theorem mutant_pde_x_sign_false :
    ¬ (∀ x y : ℂ, (∀ m : ℕ, x + 1 ≠ -(m : ℂ)) → (∀ m : ℕ, x - y + 1 ≠ -(m : ℂ)) →
      HasDerivAt (fun x => cbinom x y)
        (cbinom x y * (Complex.digamma (x - y + 1) - Complex.digamma (x + 1))) x) := by
  intro h
  obtain ⟨h1, -, h3, hne⟩ := witness_pde_x
  have hm := h 1 (1 / 2) h1 h3
  have ht := pde_x 1 (1 / 2) h1 h3
  have := ht.unique hm
  apply hne
  linear_combination this / 2

/-- Mutante (sem a hipotese `y+1 ∉ ℤ_{≤0}` em (eq:pde_y)): falso em `x = 0`, `y = -1`, onde
`binom(0,-1) = 0` (logo o lado direito e `0`, com `ψ(0) = 0` na convencao da Mathlib) mas a
derivada vale `1/(0+1) = 1`. E o ponto 5 das "Suspeitas" do plano: o enunciado precisa do
dominio. -/
theorem mutant_pde_y_no_pole_false :
    ¬ (∀ x y : ℂ, (∀ m : ℕ, x + 1 ≠ -(m : ℂ)) → (∀ m : ℕ, x - y + 1 ≠ -(m : ℂ)) →
      HasDerivAt (fun y => cbinom x y)
        (cbinom x y * (Complex.digamma (x - y + 1) - Complex.digamma (y + 1))) y) := by
  intro h
  have hx : ∀ m : ℕ, (0 : ℂ) + 1 ≠ -(m : ℂ) := ne_neg_nat_of_re_pos (by norm_num)
  have hxy : ∀ m : ℕ, (0 : ℂ) - (-1) + 1 ≠ -(m : ℂ) := ne_neg_nat_of_re_pos (by norm_num)
  have hm := h 0 (-1) hx hxy
  have ht := deriv_y_at_neg_one 0 hx
  have hu := ht.unique hm
  have hz : cbinom 0 (-1) = 0 := by
    have := LeanReal.Chap03.cbinom_zero_of_y_neg 0 0
    simpa using this
  rw [hz, zero_mul] at hu
  norm_num at hu

end Digamma

/-! ## Item 2: nucleo algebrico de `thm:fibonacci` -/

section Fibonacci

open Real

/-- Potencial de entropia `S(ξ) = (1-ξ)ln(1-ξ) - ξ ln ξ - (1-2ξ) ln(1-2ξ)` (prova de
`thm:fibonacci`, `α = 1`). -/
def S (ξ : ℝ) : ℝ :=
  (1 - ξ) * Real.log (1 - ξ) - ξ * Real.log ξ - (1 - 2 * ξ) * Real.log (1 - 2 * ξ)

/-- `S'(ξ) = -ln(1-ξ) - ln ξ + 2 ln(1-2ξ)`. -/
def S₁ (ξ : ℝ) : ℝ := -Real.log (1 - ξ) - Real.log ξ + 2 * Real.log (1 - 2 * ξ)

/-- `S''(ξ) = 1/(1-ξ) - 1/ξ - 4/(1-2ξ)`. -/
def S₂ (ξ : ℝ) : ℝ := 1 / (1 - ξ) - 1 / ξ - 4 / (1 - 2 * ξ)

/-- O ponto de sela `ξ* = (5-√5)/10`. -/
def ξstar : ℝ := (5 - Real.sqrt 5) / 10

/-- `S` tem derivada `S'` em `(0, 1/2)`. -/
theorem S_hasDerivAt {ξ : ℝ} (h0 : 0 < ξ) (h2 : ξ < 1 / 2) : HasDerivAt S (S₁ ξ) ξ := by
  have ha : 1 - ξ ≠ 0 := by intro h; linarith
  have hc : 1 - 2 * ξ ≠ 0 := by intro h; linarith
  have h1 : HasDerivAt (fun ξ : ℝ => 1 - ξ) (-1) ξ := (hasDerivAt_id' ξ).const_sub 1
  have h3 : HasDerivAt (fun ξ : ℝ => 1 - 2 * ξ) (-(2 * 1)) ξ :=
    ((hasDerivAt_id' ξ).const_mul 2).const_sub 1
  have hA := h1.mul (h1.log ha)
  have hB := (hasDerivAt_id' ξ).mul (Real.hasDerivAt_log h0.ne')
  have hC := h3.mul (h3.log hc)
  have := (hA.sub hB).sub hC
  unfold S S₁
  convert this using 1
  have e1 : (1 - ξ) * (-1 / (1 - ξ)) = -1 := by field_simp
  have e2 : ξ * ξ⁻¹ = 1 := mul_inv_cancel₀ h0.ne'
  have e3 : (1 - 2 * ξ) * (-(2 * 1) / (1 - 2 * ξ)) = -2 := by field_simp
  rw [e1, e2, e3]
  ring

/-- `S'` tem derivada `S''` em `(0, 1/2)`. -/
theorem S₁_hasDerivAt {ξ : ℝ} (h0 : 0 < ξ) (h2 : ξ < 1 / 2) : HasDerivAt S₁ (S₂ ξ) ξ := by
  have ha : 1 - ξ ≠ 0 := by intro h; linarith
  have hc : 1 - 2 * ξ ≠ 0 := by intro h; linarith
  have h1 : HasDerivAt (fun ξ : ℝ => 1 - ξ) (-1) ξ := (hasDerivAt_id' ξ).const_sub 1
  have h3 : HasDerivAt (fun ξ : ℝ => 1 - 2 * ξ) (-(2 * 1)) ξ :=
    ((hasDerivAt_id' ξ).const_mul 2).const_sub 1
  have := ((h1.log ha).neg.sub (Real.hasDerivAt_log h0.ne')).add ((h3.log hc).const_mul 2)
  unfold S₁ S₂
  convert this using 1
  field_simp
  ring

/-- `S'(ξ) = ln((1-2ξ)²/(ξ(1-ξ)))` em `(0, 1/2)`. -/
theorem S₁_eq_log {ξ : ℝ} (h0 : 0 < ξ) (h2 : ξ < 1 / 2) :
    S₁ ξ = Real.log ((1 - 2 * ξ) ^ 2 / (ξ * (1 - ξ))) := by
  have ha : 0 < 1 - ξ := by linarith
  have hc : 0 < 1 - 2 * ξ := by linarith
  unfold S₁
  rw [Real.log_div (by positivity) (by positivity), Real.log_pow,
    Real.log_mul h0.ne' ha.ne']
  push_cast
  ring

/-- `S'(ξ) = 0 ⇔ (1-2ξ)² = ξ(1-ξ)` em `(0, 1/2)`. -/
theorem S₁_eq_zero_iff {ξ : ℝ} (h0 : 0 < ξ) (h2 : ξ < 1 / 2) :
    S₁ ξ = 0 ↔ (1 - 2 * ξ) ^ 2 = ξ * (1 - ξ) := by
  have ha : 0 < 1 - ξ := by linarith
  have hc : 0 < 1 - 2 * ξ := by linarith
  have hq : 0 < (1 - 2 * ξ) ^ 2 / (ξ * (1 - ξ)) := by positivity
  rw [S₁_eq_log h0 h2, Real.log_eq_zero]
  constructor
  · rintro (h | h | h)
    · exact absurd h hq.ne'
    · rwa [div_eq_one_iff_eq (by positivity)] at h
    · linarith
  · intro h
    right; left
    rw [div_eq_one_iff_eq (by positivity)]
    exact h

/-- `0 < ξ* < 1/2`. -/
theorem ξstar_mem : 0 < ξstar ∧ ξstar < 1 / 2 := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
  unfold ξstar
  constructor <;> nlinarith

/-- `ξ*` resolve `(1-2ξ)² = ξ(1-ξ)`. -/
theorem ξstar_crit : (1 - 2 * ξstar) ^ 2 = ξstar * (1 - ξstar) := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  unfold ξstar
  nlinarith

/-- `S'(ξ*) = 0`. -/
theorem S₁_ξstar : S₁ ξstar = 0 :=
  (S₁_eq_zero_iff ξstar_mem.1 ξstar_mem.2).mpr ξstar_crit

/-- Unicidade: `ξ*` e a unica raiz de `(1-2ξ)² = ξ(1-ξ)` em `[0, 1/2]`. -/
theorem crit_unique {ξ : ℝ} (_h0 : 0 ≤ ξ) (h2 : ξ ≤ 1 / 2) (h : (1 - 2 * ξ) ^ 2 = ξ * (1 - ξ)) :
    ξ = ξstar := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
  have hprod : (10 * ξ - 5 + Real.sqrt 5) * (10 * ξ - 5 - Real.sqrt 5) = 0 := by nlinarith
  rcases mul_eq_zero.mp hprod with h | h
  · unfold ξstar; linarith
  · exfalso; linarith

/-- `φ⁻¹ = φ - 1`. -/
theorem goldenRatio_inv_eq : goldenRatio⁻¹ = goldenRatio - 1 := by
  rw [inv_goldenRatio, ← one_sub_goldenRatio]
  ring

/-- `2φ - 1 = √5`. -/
theorem two_goldenRatio_sub_one : 2 * goldenRatio - 1 = Real.sqrt 5 := by
  unfold goldenRatio; ring

/-- `1 - ξ* = φ/√5`, `ξ* = φ⁻¹/√5`, `1 - 2ξ* = 1/√5`. -/
theorem ξstar_golden :
    1 - ξstar = goldenRatio / Real.sqrt 5 ∧ ξstar = goldenRatio⁻¹ / Real.sqrt 5 ∧
      1 - 2 * ξstar = 1 / Real.sqrt 5 := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
  rw [goldenRatio_inv_eq]
  unfold ξstar goldenRatio
  refine ⟨?_, ?_, ?_⟩ <;> field_simp <;> nlinarith

/-- **`S(ξ*) = ln φ`** (prova de `thm:fibonacci`). -/
theorem S_ξstar : S ξstar = Real.log goldenRatio := by
  obtain ⟨ha, hb, hc⟩ := ξstar_golden
  have hpos : 0 < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
  have hφ : 0 < goldenRatio := goldenRatio_pos
  have hinv : goldenRatio⁻¹ = goldenRatio - 1 := goldenRatio_inv_eq
  have h2φ : 2 * goldenRatio - 1 = Real.sqrt 5 := two_goldenRatio_sub_one
  unfold S
  rw [ha, hc, hb, Real.log_div hφ.ne' hpos.ne', Real.log_div (by positivity) hpos.ne',
    Real.log_inv, Real.log_div one_ne_zero hpos.ne', Real.log_one]
  rw [hinv]
  field_simp
  rw [← h2φ]
  ring

/-- **`S''(ξ*) = -5√5`** (prova de `thm:fibonacci`). -/
theorem S₂_ξstar : S₂ ξstar = -5 * Real.sqrt 5 := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
  have h1 : (1 - ξstar) ≠ 0 := by linarith [ξstar_mem.2]
  have h2 : ξstar ≠ 0 := ξstar_mem.1.ne'
  have h3 : (1 - 2 * ξstar) ≠ 0 := by linarith [ξstar_mem.2]
  unfold S₂
  rw [div_sub_div _ _ h1 h2, div_sub_div _ _ (mul_ne_zero h1 h2) h3, div_eq_iff (by positivity)]
  unfold ξstar
  nlinarith

/-- **A constante `C₁`**: `√((1-ξ*)/(ξ*(1-2ξ*)·|S''(ξ*)|)) = φ/√5`. -/
theorem const_ξstar :
    Real.sqrt ((1 - ξstar) / (ξstar * (1 - 2 * ξstar) * |S₂ ξstar|)) =
      goldenRatio / Real.sqrt 5 := by
  obtain ⟨ha, hb, hc⟩ := ξstar_golden
  have hpos : 0 < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
  have hφ : 0 < goldenRatio := goldenRatio_pos
  have habs : |S₂ ξstar| = 5 * Real.sqrt 5 := by
    rw [S₂_ξstar, abs_of_neg (by nlinarith)]; ring
  obtain ⟨h0, h2⟩ := ξstar_mem
  have hnum : 0 ≤ (1 - ξstar) / (ξstar * (1 - 2 * ξstar) * (5 * Real.sqrt 5)) := by
    apply div_nonneg (by linarith)
    exact mul_nonneg (mul_nonneg h0.le (by linarith)) (by positivity)
  rw [habs, Real.sqrt_eq_iff_eq_sq hnum (div_pos hφ hpos).le]
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have h53 : Real.sqrt 5 ^ 3 = 5 * Real.sqrt 5 := by rw [pow_succ, h5]
  have h54 : Real.sqrt 5 ^ 4 = 25 := by nlinarith
  have hden : ξstar * (1 - 2 * ξstar) * (5 * Real.sqrt 5) ≠ 0 :=
    (mul_pos (mul_pos h0 (by linarith)) (by positivity)).ne'
  rw [div_eq_iff hden, div_pow, h5]
  unfold ξstar goldenRatio
  nlinarith [h5, h53, h54]

/-- **Identidade do prefator de Laplace** (ultima linha da prova de `thm:fibonacci`): para
`x > 0`, `x e^{xS(ξ*)} / √(2πxξ*(1-2ξ*)/(1-ξ*)) · √(2π/(x|S''(ξ*)|)) = φ^{x+1}/√5`.
A assintotica `F_cont(x) ~ ...` (Stirling + Laplace) NAO esta formalizada. -/
theorem laplace_prefactor {x : ℝ} (hx : 0 < x) :
    x * Real.exp (x * S ξstar) / Real.sqrt (2 * π * x * ξstar * (1 - 2 * ξstar) / (1 - ξstar)) *
      Real.sqrt (2 * π / (x * |S₂ ξstar|)) = goldenRatio ^ (x + 1) / Real.sqrt 5 := by
  obtain ⟨h0, h2⟩ := ξstar_mem
  have ha : 0 < 1 - ξstar := by linarith
  have hc : 0 < 1 - 2 * ξstar := by linarith
  have habs : 0 < |S₂ ξstar| := by rw [S₂_ξstar]; positivity
  have hφ : 0 < goldenRatio := goldenRatio_pos
  have hpos : 0 < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
  -- `e^{x S(ξ*)} = φ^x`
  have hexp : Real.exp (x * S ξstar) = goldenRatio ^ x := by
    rw [S_ξstar, Real.rpow_def_of_pos hφ, mul_comm]
  -- o quociente das duas raizes
  have hA : 0 < 2 * π * x * ξstar * (1 - 2 * ξstar) / (1 - ξstar) := by positivity
  have hB : 0 ≤ 2 * π / (x * |S₂ ξstar|) := by positivity
  have hC2 : goldenRatio / Real.sqrt 5 =
      Real.sqrt ((1 - ξstar) / (ξstar * (1 - 2 * ξstar) * |S₂ ξstar|)) := const_ξstar.symm
  have hsq : (goldenRatio / Real.sqrt 5) ^ 2 =
      (1 - ξstar) / (ξstar * (1 - 2 * ξstar) * |S₂ ξstar|) := by
    rw [hC2, Real.sq_sqrt (by positivity)]
  have hratio : Real.sqrt (2 * π / (x * |S₂ ξstar|)) /
      Real.sqrt (2 * π * x * ξstar * (1 - 2 * ξstar) / (1 - ξstar)) =
      goldenRatio / Real.sqrt 5 / x := by
    rw [← Real.sqrt_div' _ hA.le, Real.sqrt_eq_iff_eq_sq (by positivity) (by positivity),
      div_pow, hsq]
    field_simp
  rw [hexp, Real.rpow_add hφ, Real.rpow_one]
  calc x * goldenRatio ^ x / Real.sqrt (2 * π * x * ξstar * (1 - 2 * ξstar) / (1 - ξstar)) *
        Real.sqrt (2 * π / (x * |S₂ ξstar|))
      = x * goldenRatio ^ x * (Real.sqrt (2 * π / (x * |S₂ ξstar|)) /
          Real.sqrt (2 * π * x * ξstar * (1 - 2 * ξstar) / (1 - ξstar))) := by ring
    _ = x * goldenRatio ^ x * (goldenRatio / Real.sqrt 5 / x) := by rw [hratio]
    _ = goldenRatio ^ x * goldenRatio / Real.sqrt 5 := by field_simp

/-- Mutante (constante sem o fator `φ`): `√(...) = 1/√5` e falso, pois `φ ≠ 1`. -/
theorem mutant_constant_false :
    Real.sqrt ((1 - ξstar) / (ξstar * (1 - 2 * ξstar) * |S₂ ξstar|)) ≠ 1 / Real.sqrt 5 := by
  rw [const_ξstar]
  intro h
  have hpos : 0 < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
  rw [div_eq_div_iff hpos.ne' hpos.ne'] at h
  have := mul_pos (sub_pos.mpr one_lt_goldenRatio) hpos
  nlinarith

/-- Mutante (a outra raiz da quadratica, `(5+√5)/10`): nao esta em `[0, 1/2]`. -/
theorem mutant_other_root_false :
    (1 - 2 * ((5 + Real.sqrt 5) / 10)) ^ 2 = (5 + Real.sqrt 5) / 10 * (1 - (5 + Real.sqrt 5) / 10)
      ∧ ¬ ((5 + Real.sqrt 5) / 10 ≤ 1 / 2) := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
  constructor
  · nlinarith
  · intro h; linarith

/-! ### Raio geral `α > 0` -/

/-- `S_α(ξ) = u ln u - ξ ln ξ - w ln w`, `u = 1 - αξ`, `w = 1 - (α+1)ξ`. -/
def Sα (α ξ : ℝ) : ℝ :=
  (1 - α * ξ) * Real.log (1 - α * ξ) - ξ * Real.log ξ -
    (1 - (α + 1) * ξ) * Real.log (1 - (α + 1) * ξ)

/-- `S_α'(ξ) = -α ln u - ln ξ + (α+1) ln w`. -/
def Sα₁ (α ξ : ℝ) : ℝ :=
  -α * Real.log (1 - α * ξ) - Real.log ξ + (α + 1) * Real.log (1 - (α + 1) * ξ)

/-- `S_α''(ξ) = α²/u - 1/ξ - (α+1)²/w`. -/
def Sα₂ (α ξ : ℝ) : ℝ :=
  α ^ 2 / (1 - α * ξ) - 1 / ξ - (α + 1) ^ 2 / (1 - (α + 1) * ξ)

/-- Para `α > 0` e `0 < ξ < 1/(α+1)`: `w > 0` e `u > 0`. -/
theorem uw_pos {α ξ : ℝ} (hα : 0 < α) (_h0 : 0 < ξ) (h1 : ξ < 1 / (α + 1)) :
    0 < 1 - (α + 1) * ξ ∧ 0 < 1 - α * ξ := by
  have : (α + 1) * ξ < 1 := by
    rwa [lt_div_iff₀ (by linarith), mul_comm] at h1
  constructor <;> nlinarith

/-- `S_α` tem derivada `S_α'`. -/
theorem Sα_hasDerivAt {α ξ : ℝ} (hα : 0 < α) (h0 : 0 < ξ) (h1 : ξ < 1 / (α + 1)) :
    HasDerivAt (Sα α) (Sα₁ α ξ) ξ := by
  obtain ⟨hw, hu⟩ := uw_pos hα h0 h1
  have hU : HasDerivAt (fun ξ : ℝ => 1 - α * ξ) (-(α * 1)) ξ :=
    ((hasDerivAt_id' ξ).const_mul α).const_sub 1
  have hW : HasDerivAt (fun ξ : ℝ => 1 - (α + 1) * ξ) (-((α + 1) * 1)) ξ :=
    ((hasDerivAt_id' ξ).const_mul (α + 1)).const_sub 1
  have hA := hU.mul (hU.log hu.ne')
  have hB := (hasDerivAt_id' ξ).mul (Real.hasDerivAt_log h0.ne')
  have hC := hW.mul (hW.log hw.ne')
  have := (hA.sub hB).sub hC
  unfold Sα Sα₁
  convert this using 1
  have hu' : 1 - α * ξ ≠ 0 := hu.ne'
  have hw' : 1 - (α + 1) * ξ ≠ 0 := hw.ne'
  have e1 : (1 - α * ξ) * (-(α * 1) / (1 - α * ξ)) = -α := by field_simp
  have e2 : ξ * ξ⁻¹ = 1 := mul_inv_cancel₀ h0.ne'
  have e3 : (1 - (α + 1) * ξ) * (-((α + 1) * 1) / (1 - (α + 1) * ξ)) = -(α + 1) := by
    field_simp
  rw [e1, e2, e3]
  ring

/-- `S_α'` tem derivada `S_α''`. -/
theorem Sα₁_hasDerivAt {α ξ : ℝ} (hα : 0 < α) (h0 : 0 < ξ) (h1 : ξ < 1 / (α + 1)) :
    HasDerivAt (Sα₁ α) (Sα₂ α ξ) ξ := by
  obtain ⟨hw, hu⟩ := uw_pos hα h0 h1
  have hU : HasDerivAt (fun ξ : ℝ => 1 - α * ξ) (-(α * 1)) ξ :=
    ((hasDerivAt_id' ξ).const_mul α).const_sub 1
  have hW : HasDerivAt (fun ξ : ℝ => 1 - (α + 1) * ξ) (-((α + 1) * 1)) ξ :=
    ((hasDerivAt_id' ξ).const_mul (α + 1)).const_sub 1
  have := (((hU.log hu.ne').const_mul (-α)).sub (Real.hasDerivAt_log h0.ne')).add
    ((hW.log hw.ne').const_mul (α + 1))
  unfold Sα₁ Sα₂
  convert this using 1
  field_simp
  ring

/-- **Cauchy–Schwarz do livro**: com `u = w + ξ`, `(α+2)²/u ≤ 1/ξ + (α+1)²/w`. -/
theorem cauchy_schwarz_step {α ξ w : ℝ} (h0 : 0 < ξ) (hw : 0 < w) :
    (α + 2) ^ 2 / (w + ξ) ≤ 1 / ξ + (α + 1) ^ 2 / w := by
  have key : 1 / ξ + (α + 1) ^ 2 / w - (α + 2) ^ 2 / (w + ξ) =
      (w - (α + 1) * ξ) ^ 2 / (ξ * w * (w + ξ)) := by
    field_simp
    ring
  have : 0 ≤ (w - (α + 1) * ξ) ^ 2 / (ξ * w * (w + ξ)) := by positivity
  linarith

/-- **`S_α'' < 0`** em `(0, 1/(α+1))`, para `α > 0`. -/
theorem Sα₂_neg {α ξ : ℝ} (hα : 0 < α) (h0 : 0 < ξ) (h1 : ξ < 1 / (α + 1)) :
    Sα₂ α ξ < 0 := by
  obtain ⟨hw, hu⟩ := uw_pos hα h0 h1
  have hcs := cauchy_schwarz_step (α := α) h0 hw
  have hrw : 1 - (α + 1) * ξ + ξ = 1 - α * ξ := by ring
  rw [hrw] at hcs
  have hlt : α ^ 2 / (1 - α * ξ) < (α + 2) ^ 2 / (1 - α * ξ) := by
    apply div_lt_div_of_pos_right _ hu
    nlinarith
  unfold Sα₂
  linarith

/-- **Caracterizacao do ponto critico**: `S_α'(ξ) = 0 ⇔ w^{α+1} = ξ u^α` (potencias reais). -/
theorem Sα₁_eq_zero_iff {α ξ : ℝ} (hα : 0 < α) (h0 : 0 < ξ) (h1 : ξ < 1 / (α + 1)) :
    Sα₁ α ξ = 0 ↔ (1 - (α + 1) * ξ) ^ (α + 1) = ξ * (1 - α * ξ) ^ α := by
  obtain ⟨hw, hu⟩ := uw_pos hα h0 h1
  have hL : Sα₁ α ξ = Real.log ((1 - (α + 1) * ξ) ^ (α + 1)) - Real.log (ξ * (1 - α * ξ) ^ α) := by
    unfold Sα₁
    rw [Real.log_rpow hw, Real.log_mul h0.ne' (Real.rpow_pos_of_pos hu α).ne', Real.log_rpow hu]
    ring
  rw [hL, sub_eq_zero]
  constructor
  · intro h
    exact Real.log_injOn_pos (Set.mem_Ioi.mpr (Real.rpow_pos_of_pos hw _))
      (Set.mem_Ioi.mpr (mul_pos h0 (Real.rpow_pos_of_pos hu α))) h
  · intro h
    rw [h]

/-- **`S_α(ξ*) = ln(u*/w*)`** no ponto critico. -/
theorem Sα_crit {α ξ : ℝ} (hα : 0 < α) (h0 : 0 < ξ) (h1 : ξ < 1 / (α + 1))
    (hcrit : (1 - (α + 1) * ξ) ^ (α + 1) = ξ * (1 - α * ξ) ^ α) :
    Sα α ξ = Real.log ((1 - α * ξ) / (1 - (α + 1) * ξ)) := by
  obtain ⟨hw, hu⟩ := uw_pos hα h0 h1
  have hlog : Real.log ξ = (α + 1) * Real.log (1 - (α + 1) * ξ) - α * Real.log (1 - α * ξ) := by
    have := congrArg Real.log hcrit
    rw [Real.log_rpow hw, Real.log_mul h0.ne' (Real.rpow_pos_of_pos hu α).ne',
      Real.log_rpow hu] at this
    linarith
  unfold Sα
  rw [hlog, Real.log_div hu.ne' hw.ne']
  ring

/-- **`z = u*/w*` satisfaz `z^α(z-1) = 1`** no ponto critico. -/
theorem lambda_eq {α ξ : ℝ} (hα : 0 < α) (h0 : 0 < ξ) (h1 : ξ < 1 / (α + 1))
    (hcrit : (1 - (α + 1) * ξ) ^ (α + 1) = ξ * (1 - α * ξ) ^ α) :
    ((1 - α * ξ) / (1 - (α + 1) * ξ)) ^ α * ((1 - α * ξ) / (1 - (α + 1) * ξ) - 1) = 1 := by
  obtain ⟨hw, hu⟩ := uw_pos hα h0 h1
  have hw' : 1 - (α + 1) * ξ ≠ 0 := hw.ne'
  have hz : (1 - α * ξ) / (1 - (α + 1) * ξ) - 1 = ξ / (1 - (α + 1) * ξ) := by
    rw [div_sub_one hw']
    congr 1
    ring
  have hwa : (1 - (α + 1) * ξ) ^ (α + 1) = (1 - (α + 1) * ξ) ^ α * (1 - (α + 1) * ξ) := by
    rw [Real.rpow_add hw, Real.rpow_one]
  rw [hwa] at hcrit
  have hwα : 0 < (1 - (α + 1) * ξ) ^ α := Real.rpow_pos_of_pos hw α
  rw [hz, Real.div_rpow hu.le hw.le, div_mul_div_comm, div_eq_one_iff_eq (mul_pos hwα hw).ne']
  linear_combination hcrit.symm

/-- `λ_α = u*/w* > 1`. -/
theorem lambda_gt_one {α ξ : ℝ} (hα : 0 < α) (h0 : 0 < ξ) (h1 : ξ < 1 / (α + 1)) :
    1 < (1 - α * ξ) / (1 - (α + 1) * ξ) := by
  obtain ⟨hw, hu⟩ := uw_pos hα h0 h1
  rw [lt_div_iff₀ hw]
  nlinarith

/-- `z ↦ z^α(z-1)` e estritamente crescente em `z > 1` (para `α > 0`). -/
theorem strictMonoOn_lambda_fn {α : ℝ} (hα : 0 < α) :
    StrictMonoOn (fun z : ℝ => z ^ α * (z - 1)) (Ioi 1) := by
  intro a ha b hb hab
  have ha1 : (1 : ℝ) < a := ha
  have hb1 : (1 : ℝ) < b := hb
  have h1 : a ^ α < b ^ α := Real.rpow_lt_rpow (by linarith) hab hα
  have h2 : a - 1 < b - 1 := by linarith
  have h3 : 0 < a ^ α := Real.rpow_pos_of_pos (by linarith) α
  have h4 : 0 < a - 1 := by linarith
  simp only
  nlinarith

/-- **Unicidade de `λ_α`**: duas raizes `z > 1` de `z^α(z-1) = 1` coincidem. -/
theorem lambda_unique {α z₁ z₂ : ℝ} (hα : 0 < α) (h1 : 1 < z₁) (h2 : 1 < z₂)
    (e1 : z₁ ^ α * (z₁ - 1) = 1) (e2 : z₂ ^ α * (z₂ - 1) = 1) : z₁ = z₂ :=
  (strictMonoOn_lambda_fn hα).injOn h1 h2
    (by show z₁ ^ α * (z₁ - 1) = z₂ ^ α * (z₂ - 1); rw [e1, e2])

/-- **Existencia de `λ_α`**: ha `z ∈ (1, 2]` com `z^α(z-1) = 1` (valor intermediario). -/
theorem lambda_exists {α : ℝ} (hα : 0 < α) :
    ∃ z : ℝ, 1 < z ∧ z ≤ 2 ∧ z ^ α * (z - 1) = 1 := by
  have hcont : ContinuousOn (fun z : ℝ => z ^ α * (z - 1)) (Icc 1 2) :=
    ((Real.continuous_rpow_const hα.le).mul (continuous_id.sub continuous_const)).continuousOn
  have hivt := intermediate_value_Icc (by norm_num : (1 : ℝ) ≤ 2) hcont
  have h2 : (1 : ℝ) ≤ (2 : ℝ) ^ α * (2 - 1) := by
    have := Real.one_le_rpow (by norm_num : (1 : ℝ) ≤ 2) hα.le
    linarith
  obtain ⟨z, hz, hzv⟩ := hivt ⟨by simp, h2⟩
  refine ⟨z, ?_, hz.2, hzv⟩
  rcases hz.1.lt_or_eq with h | h
  · exact h
  · exfalso
    rw [← h] at hzv
    simp at hzv

/-- **Unicidade do ponto critico** de `S_α` em `(0, 1/(α+1))`: `S_α'` e estritamente
decrescente (porque `S_α'' < 0`), logo tem no maximo um zero. -/
theorem Sα₁_strictAntiOn {α : ℝ} (hα : 0 < α) :
    StrictAntiOn (Sα₁ α) (Ioo 0 (1 / (α + 1))) := by
  apply strictAntiOn_of_deriv_neg (convex_Ioo _ _)
  · intro ξ hξ
    exact (Sα₁_hasDerivAt hα hξ.1 hξ.2).continuousAt.continuousWithinAt
  · intro ξ hξ
    rw [interior_Ioo] at hξ
    rw [(Sα₁_hasDerivAt hα hξ.1 hξ.2).deriv]
    exact Sα₂_neg hα hξ.1 hξ.2

theorem crit_unique_general {α ξ₁ ξ₂ : ℝ} (hα : 0 < α)
    (h₁ : ξ₁ ∈ Ioo 0 (1 / (α + 1))) (h₂ : ξ₂ ∈ Ioo 0 (1 / (α + 1)))
    (e₁ : Sα₁ α ξ₁ = 0) (e₂ : Sα₁ α ξ₂ = 0) : ξ₁ = ξ₂ :=
  (Sα₁_strictAntiOn hα).injOn h₁ h₂ (by rw [e₁, e₂])

/-- Testemunha (`α = 1`): `ξ*` e ponto critico de `S_1` no sentido da potencia real, e
`λ_1 = u*/w* = φ` (o livro: "For `α = 1`, `C₁ = φ/√5` and `λ₁ = φ`"). -/
theorem witness_alpha_one :
    (0 : ℝ) < 1 ∧ 0 < ξstar ∧ ξstar < 1 / (1 + 1) ∧
      (1 - (1 + 1) * ξstar) ^ ((1 : ℝ) + 1) = ξstar * (1 - 1 * ξstar) ^ (1 : ℝ) ∧
      (1 - 1 * ξstar) / (1 - (1 + 1) * ξstar) = goldenRatio := by
  obtain ⟨h0, h2⟩ := ξstar_mem
  obtain ⟨ha, hb, hc⟩ := ξstar_golden
  have hpos : 0 < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
  refine ⟨one_pos, h0, by norm_num [h2], ?_, ?_⟩
  · rw [show ((1 : ℝ) + 1) = ((2 : ℕ) : ℝ) by norm_num, Real.rpow_natCast, Real.rpow_one]
    have := ξstar_crit
    rw [one_mul]
    convert this using 2
  · rw [one_mul, show (1 + 1 : ℝ) = 2 by norm_num, ha, hc]
    field_simp

/-- Mutante (concavidade trocada): `S_α'' > 0` e falso, por exemplo em `α = 1`, `ξ = ξ*`. -/
theorem mutant_convex_false : ¬ (∀ α ξ : ℝ, 0 < α → 0 < ξ → ξ < 1 / (α + 1) → 0 < Sα₂ α ξ) := by
  intro h
  obtain ⟨h0, h2⟩ := ξstar_mem
  have := h 1 ξstar one_pos h0 (by norm_num [h2])
  have hneg := Sα₂_neg one_pos h0 (by norm_num [h2] : ξstar < 1 / (1 + 1))
  linarith

/-- Mutante (`λ = φ²` em vez de `φ`): `φ²(φ² - 1) = φ³ ≠ 1`. -/
theorem mutant_lambda_sq_false :
    ¬ ((goldenRatio ^ 2) ^ (1 : ℝ) * (goldenRatio ^ 2 - 1) = 1) := by
  rw [Real.rpow_one]
  have hsq : goldenRatio ^ 2 = goldenRatio + 1 := goldenRatio_sq
  have h1 := one_lt_goldenRatio
  nlinarith

end Fibonacci

/-! ## Item 3: `prop:fractional_props`, (1) e (2) em `m = 2` -/

section Fractional

open LeanReal.Chap03Analysis (rbinom rbinom_pos rbinom_symm rbinom_continuousOn)
open intervalIntegral

/-- Nucleo `K_α(y) = Γ(α+1) / ∏_j Γ(y_j+1)` no vetor baricentrico completo `y ∈ ℝ^m`
(na simplex, `∑_j y_j = α`). -/
def K {m : ℕ} (α : ℝ) (y : Fin m → ℝ) : ℝ :=
  Real.Gamma (α + 1) * ∏ j, (Real.Gamma (y j + 1))⁻¹

/-- **`prop:fractional_props` (1), `K_α(0) = 1`**: no vertice `y = (0,…,0,α)`. -/
theorem K_zero (m : ℕ) {α : ℝ} (hα : 0 < α) :
    K α (Pi.single (Fin.last m) α : Fin (m + 1) → ℝ) = 1 := by
  unfold K
  rw [Finset.prod_eq_single (Fin.last m)]
  · simp only [Pi.single_eq_same]
    exact mul_inv_cancel₀ (Real.Gamma_pos_of_pos (by linarith)).ne'
  · intro b _ hb
    rw [Pi.single_eq_of_ne hb, zero_add, Real.Gamma_one, inv_one]
  · intro h
    exact absurd (Finset.mem_univ _) h

/-- **`prop:fractional_props` (1), positividade**: `K_α(y) > 0` para `y_j ≥ 0` (em
particular no interior da simplex). -/
theorem K_pos {m : ℕ} {α : ℝ} (hα : 0 < α) {y : Fin m → ℝ} (hy : ∀ j, 0 ≤ y j) :
    0 < K α y := by
  unfold K
  apply mul_pos (Real.Gamma_pos_of_pos (by linarith))
  apply Finset.prod_pos
  intro j _
  exact inv_pos.mpr (Real.Gamma_pos_of_pos (by linarith [hy j]))

/-- Em `m = 2`, `K_α(y, α-y) = binom(α, y)` (o nucleo 1D do livro). -/
theorem K_two (α y : ℝ) : K α ![y, α - y] = rbinom α y := by
  unfold K rbinom
  rw [Fin.prod_univ_two]
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
  ring

/-- `I(α) = ∫_0^α binom(α,y) dy`. -/
def I (α : ℝ) : ℝ := ∫ y in (0 : ℝ)..α, rbinom α y

/-- Operador de media `D^α f(x) = (1/I(α)) ∫_0^α binom(α,y) f(x-y) dy` (Definicao "1D
Beta-Kernel Averaging Operator"). -/
def D (α : ℝ) (f : ℝ → ℝ) (x : ℝ) : ℝ :=
  (1 / I α) * ∫ y in (0 : ℝ)..α, rbinom α y * f (x - y)

/-- `y ↦ binom(α,y)` e integravel em `[0,α]`. -/
theorem rbinom_intervalIntegrable {α : ℝ} (hα : 0 ≤ α) :
    IntervalIntegrable (rbinom α) MeasureTheory.volume 0 α := by
  apply ContinuousOn.intervalIntegrable
  rw [uIcc_of_le hα]
  exact rbinom_continuousOn

/-- `y ↦ binom(α,y) g(y)` e integravel em `[0,α]` para `g` continua. -/
theorem rbinom_mul_intervalIntegrable {α : ℝ} (hα : 0 ≤ α) {g : ℝ → ℝ} (hg : Continuous g) :
    IntervalIntegrable (fun y => rbinom α y * g y) MeasureTheory.volume 0 α := by
  apply ContinuousOn.intervalIntegrable
  rw [uIcc_of_le hα]
  exact rbinom_continuousOn.mul hg.continuousOn

/-- `I(α) > 0` para `α > 0`. -/
theorem I_pos {α : ℝ} (hα : 0 < α) : 0 < I α := by
  unfold I
  apply intervalIntegral_pos_of_pos_on (rbinom_intervalIntegrable hα.le) _ hα
  intro y hy
  exact rbinom_pos hα hy.1.le hy.2.le

/-- `D^α` preserva constantes: o nucleo normalizado e uma densidade de probabilidade. -/
theorem D_const {α : ℝ} (hα : 0 < α) (c x : ℝ) : D α (fun _ => c) x = c := by
  unfold D
  simp only [integral_mul_const]
  have := I_pos hα
  unfold I at this ⊢
  field_simp

/-- **Estimativa da prova de (2)**: se `|f(x-y) - f(x)| ≤ ε` em `y ∈ [0,α]`, entao
`|D^α f(x) - f(x)| ≤ ε`. -/
theorem D_sub_le {α : ℝ} (hα : 0 < α) {f : ℝ → ℝ} (hf : Continuous f) {x ε : ℝ}
    (hε : ∀ y ∈ Icc 0 α, |f (x - y) - f x| ≤ ε) : |D α f x - f x| ≤ ε := by
  have hI := I_pos hα
  have hg : Continuous (fun y => f (x - y)) := hf.comp (continuous_const.sub continuous_id)
  have hg2 : Continuous (fun _ : ℝ => f x) := continuous_const
  have hint1 := rbinom_mul_intervalIntegrable hα.le hg
  have hint2 := rbinom_mul_intervalIntegrable hα.le hg2
  have hint3 := rbinom_intervalIntegrable hα.le
  -- `D f x - f x = (1/I) ∫ b (f(x-y) - f x)`
  have hrepr : D α f x - f x =
      (1 / I α) * ∫ y in (0 : ℝ)..α, rbinom α y * (f (x - y) - f x) := by
    have : ∫ y in (0 : ℝ)..α, rbinom α y * (f (x - y) - f x) =
        (∫ y in (0 : ℝ)..α, rbinom α y * f (x - y)) - (∫ y in (0 : ℝ)..α, rbinom α y) * f x := by
      rw [← integral_mul_const, ← integral_sub hint1 hint2]
      congr 1; funext y; ring
    rw [this]
    unfold D I at *
    field_simp
  have hint4 := rbinom_mul_intervalIntegrable hα.le (hg.sub hg2)
  rw [hrepr, abs_mul, abs_of_pos (by positivity : 0 < 1 / I α)]
  have hbound : |∫ y in (0 : ℝ)..α, rbinom α y * (f (x - y) - f x)| ≤ ε * I α := by
    calc |∫ y in (0 : ℝ)..α, rbinom α y * (f (x - y) - f x)|
        ≤ ∫ y in (0 : ℝ)..α, |rbinom α y * (f (x - y) - f x)| :=
          abs_integral_le_integral_abs hα.le
      _ ≤ ∫ y in (0 : ℝ)..α, rbinom α y * ε := by
          apply integral_mono_on hα.le
          · exact hint4.abs
          · exact hint3.mul_const ε
          · intro y hy
            rw [abs_mul, abs_of_pos (rbinom_pos hα hy.1 hy.2)]
            exact mul_le_mul_of_nonneg_left (hε y hy) (rbinom_pos hα hy.1 hy.2).le
      _ = ε * I α := by rw [integral_mul_const]; unfold I; ring
  calc 1 / I α * |∫ y in (0 : ℝ)..α, rbinom α y * (f (x - y) - f x)|
      ≤ 1 / I α * (ε * I α) := mul_le_mul_of_nonneg_left hbound (by positivity)
    _ = ε := by field_simp

/-- **`prop:fractional_props` (2), `m = 2`**: `D^α f(x) → f(x)` quando `α → 0⁺`, para `f`
continua (a continuidade em `x` e o que a prova usa; limitacao e continuidade uniforme nao
sao necessarias). -/
theorem identity_limit {f : ℝ → ℝ} (hf : Continuous f) (x : ℝ) :
    Filter.Tendsto (fun α => D α f x) (nhdsWithin 0 (Ioi 0)) (nhds (f x)) := by
  rw [Metric.tendsto_nhdsWithin_nhds]
  intro ε hε
  obtain ⟨δ, hδ, hδf⟩ := Metric.continuousAt_iff.mp hf.continuousAt (ε / 2) (by linarith)
  refine ⟨δ, hδ, fun α hα hαδ => ?_⟩
  have hα0 : 0 < α := hα
  have hαδ' : α < δ := by
    rw [Real.dist_eq, sub_zero, abs_of_pos hα0] at hαδ
    exact hαδ
  have hb : |D α f x - f x| ≤ ε / 2 := by
    apply D_sub_le hα0 hf
    intro y hy
    have : dist (x - y) x < δ := by
      rw [Real.dist_eq, show x - y - x = -y by ring, abs_neg, abs_of_nonneg hy.1]
      linarith [hy.2]
    exact (le_of_lt (by simpa [Real.dist_eq] using hδf this))
  rw [Real.dist_eq]
  linarith

/-- **Forma do livro** de (2): `f` limitada e uniformemente continua. A limitacao `hbdd` nao
e usada; a continuidade uniforme so entra pela continuidade. -/
theorem identity_limit_book {f : ℝ → ℝ} (hf : UniformContinuous f)
    (_hbdd : ∃ M : ℝ, ∀ t, |f t| ≤ M) (x : ℝ) :
    Filter.Tendsto (fun α => D α f x) (nhdsWithin 0 (Ioi 0)) (nhds (f x)) :=
  identity_limit hf.continuous x

/-- Simbolo `G_α(λ) = (1/I(α)) ∫_0^α binom(α,y) e^{-λy} dy` (versao com `λ` real). -/
def G (α lam : ℝ) : ℝ := (1 / I α) * ∫ y in (0 : ℝ)..α, rbinom α y * Real.exp (-lam * y)

/-- **`prop:fractional_props` (3)**, `λ` real: `D^α e^{λ·}(x) = e^{λx} G_α(λ)`. O caso
`λ ∈ ℂ` e a analiticidade de `G_α` nao estao formalizados. -/
theorem D_exp (α lam x : ℝ) : D α (fun t => Real.exp (lam * t)) x = Real.exp (lam * x) * G α lam := by
  unfold D G
  have : ∀ y, rbinom α y * Real.exp (lam * (x - y)) =
      Real.exp (lam * x) * (rbinom α y * Real.exp (-lam * y)) := by
    intro y
    rw [show lam * (x - y) = lam * x + -lam * y by ring, Real.exp_add]
    ring
  simp_rw [this]
  rw [integral_const_mul]
  ring

/-- `G_α(0) = 1`. -/
theorem G_zero {α : ℝ} (hα : 0 < α) : G α 0 = 1 := by
  have := D_const hα 1 0
  unfold D at this
  unfold G
  simpa using this

/-- `∫_0^α y binom(α,y) dy = (α/2) I(α)`, pela simetria `binom(α, α-y) = binom(α, y)`. -/
theorem integral_mul_rbinom {α : ℝ} (hα : 0 < α) :
    ∫ y in (0 : ℝ)..α, rbinom α y * y = α / 2 * I α := by
  have hint1 : IntervalIntegrable (fun y => rbinom α y * y) MeasureTheory.volume 0 α :=
    rbinom_mul_intervalIntegrable hα.le continuous_id
  have hint3 := rbinom_intervalIntegrable hα.le
  have hsub := integral_comp_sub_left (fun y => rbinom α y * y) (a := 0) (b := α) α
  simp only [sub_self, sub_zero] at hsub
  have hJ : ∫ y in (0 : ℝ)..α, rbinom α (α - y) * (α - y) =
      α * (∫ y in (0 : ℝ)..α, rbinom α y) - ∫ y in (0 : ℝ)..α, rbinom α y * y := by
    rw [← integral_const_mul, ← integral_sub (hint3.const_mul α) hint1]
    congr 1; funext y
    rw [rbinom_symm]; ring
  unfold I
  linarith

/-- **Testemunha nao degenerada** de `identity_limit`: `D^α id(x) = x - α/2`, logo
`D^α id ≠ id` para todo `α > 0` (o limite e conteudo real, nao uma identidade). -/
theorem D_id {α : ℝ} (hα : 0 < α) (x : ℝ) : D α id x = x - α / 2 := by
  have hI := I_pos hα
  have hint1 : IntervalIntegrable (fun y => rbinom α y * y) MeasureTheory.volume 0 α :=
    rbinom_mul_intervalIntegrable hα.le continuous_id
  have hint3 := rbinom_intervalIntegrable hα.le
  unfold D
  have : ∫ y in (0 : ℝ)..α, rbinom α y * id (x - y) =
      (∫ y in (0 : ℝ)..α, rbinom α y) * x - ∫ y in (0 : ℝ)..α, rbinom α y * y := by
    rw [← integral_mul_const, ← integral_sub (hint3.mul_const x) hint1]
    congr 1; funext y; simp only [id]; ring
  rw [this, integral_mul_rbinom hα]
  unfold I at *
  field_simp

/-- A testemunha: `D^1 id(0) = -1/2 ≠ id 0`, enquanto `D^α id(0) → 0`. -/
theorem witness_identity_limit :
    D 1 id 0 = -1 / 2 ∧ D 1 id 0 ≠ id 0 ∧
      Filter.Tendsto (fun α => D α id 0) (nhdsWithin 0 (Ioi 0)) (nhds (id 0)) := by
  refine ⟨?_, ?_, identity_limit continuous_id 0⟩
  · rw [D_id one_pos]; norm_num
  · rw [D_id one_pos]; norm_num

/-- Mutante (sem o limite: `D^α f = f` para `α > 0` fixo): falso para `f = id`, `α = 1`. -/
theorem mutant_D_eq_id_false :
    ¬ (∀ α : ℝ, 0 < α → ∀ f : ℝ → ℝ, Continuous f → ∀ x, D α f x = f x) := by
  intro h
  have := h 1 one_pos id continuous_id 0
  rw [D_id one_pos] at this
  norm_num at this

/-- Mutante de (1) (vetor nulo em `ℝ^m`, ignorando `y_m = α`): `K_α(0,…,0) = Γ(α+1) ≠ 1`
em `α = 2`. -/
theorem mutant_K_zero_vector_false :
    ¬ (∀ (m : ℕ) (α : ℝ), 0 < α → K α (0 : Fin (m + 1) → ℝ) = 1) := by
  intro h
  have := h 0 2 two_pos
  unfold K at this
  simp only [Pi.zero_apply, zero_add, Real.Gamma_one, inv_one, Finset.prod_const_one,
    mul_one] at this
  rw [show (2 : ℝ) + 1 = (2 : ℕ) + 1 by norm_num, Real.Gamma_nat_eq_factorial] at this
  norm_num at this

end Fractional

end LeanReal.Chap03Special

#print axioms LeanReal.Chap03Special.pde_x
#print axioms LeanReal.Chap03Special.pde_y
#print axioms LeanReal.Chap03Special.pde_sum
#print axioms LeanReal.Chap03Special.transport
#print axioms LeanReal.Chap03Special.deriv_y_at_neg_one
#print axioms LeanReal.Chap03Special.witness_pde_x
#print axioms LeanReal.Chap03Special.mutant_pde_x_sign_false
#print axioms LeanReal.Chap03Special.mutant_pde_y_no_pole_false
#print axioms LeanReal.Chap03Special.S_hasDerivAt
#print axioms LeanReal.Chap03Special.S₁_hasDerivAt
#print axioms LeanReal.Chap03Special.S₁_eq_zero_iff
#print axioms LeanReal.Chap03Special.S₁_ξstar
#print axioms LeanReal.Chap03Special.crit_unique
#print axioms LeanReal.Chap03Special.S_ξstar
#print axioms LeanReal.Chap03Special.S₂_ξstar
#print axioms LeanReal.Chap03Special.const_ξstar
#print axioms LeanReal.Chap03Special.laplace_prefactor
#print axioms LeanReal.Chap03Special.mutant_constant_false
#print axioms LeanReal.Chap03Special.mutant_other_root_false
#print axioms LeanReal.Chap03Special.Sα_hasDerivAt
#print axioms LeanReal.Chap03Special.Sα₁_hasDerivAt
#print axioms LeanReal.Chap03Special.Sα₂_neg
#print axioms LeanReal.Chap03Special.Sα₁_eq_zero_iff
#print axioms LeanReal.Chap03Special.Sα_crit
#print axioms LeanReal.Chap03Special.lambda_eq
#print axioms LeanReal.Chap03Special.lambda_gt_one
#print axioms LeanReal.Chap03Special.lambda_unique
#print axioms LeanReal.Chap03Special.lambda_exists
#print axioms LeanReal.Chap03Special.crit_unique_general
#print axioms LeanReal.Chap03Special.witness_alpha_one
#print axioms LeanReal.Chap03Special.mutant_convex_false
#print axioms LeanReal.Chap03Special.mutant_lambda_sq_false
#print axioms LeanReal.Chap03Special.K_zero
#print axioms LeanReal.Chap03Special.K_pos
#print axioms LeanReal.Chap03Special.K_two
#print axioms LeanReal.Chap03Special.I_pos
#print axioms LeanReal.Chap03Special.D_const
#print axioms LeanReal.Chap03Special.D_sub_le
#print axioms LeanReal.Chap03Special.identity_limit
#print axioms LeanReal.Chap03Special.identity_limit_book
#print axioms LeanReal.Chap03Special.D_exp
#print axioms LeanReal.Chap03Special.G_zero
#print axioms LeanReal.Chap03Special.D_id
#print axioms LeanReal.Chap03Special.witness_identity_limit
#print axioms LeanReal.Chap03Special.mutant_D_eq_id_false
#print axioms LeanReal.Chap03Special.mutant_K_zero_vector_false
