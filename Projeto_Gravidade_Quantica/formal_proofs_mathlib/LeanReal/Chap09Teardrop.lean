import Mathlib.Analysis.SpecialFunctions.Trigonometric.Inverse
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.Calculus.Deriv.Prod

/-!
# Capitulo 9, `prop:teardrop` (i)+(ii) e `prop:teardrop_lower` (lote B6 do `PLANO_LIVRO_B.md`)

Fonte: `unified_quantum_gravity_book/chap09_global_homotopy_covering_spaces_jordan_loops.tex`,
secao "Reversing through a narrow mouth".

* `prop:teardrop`: para `a ∈ (0,2ρ]`, `β(a) = arccos((1 + a/(2ρ))/2)`,
  `r*(a) = ρ(1 + 2 sin β(a)) = ρ(1 + √(4 - (1 + a/(2ρ))²))`; a gota `γ_a` (tres arcos de raio
  `ρ`: direita `β`, esquerda `π + 2β`, direita `β`, partindo de `(0,-a/2)` na direcao `(1,0)`).
  (i) `γ_a` e admissivel e mergulhada, termina em `(0,a/2)` com tangente `(-1,0)`, toca `{x=0}`
  so nas pontas e `max|γ_a| = r*(a)`. (ii) toda curva da familia de tres arcos `F_a` tem
  `max|γ| ≥ r*(a)`, com igualdade so para `γ_a` (e sua imagem espelhada).
* `prop:teardrop_lower`: `R ≥ ρ + √(ρ² - a²/4)` para curvas mergulhadas que evitam o disco `K`
  de diametro `[q₀,q₁]`; e, na observacao seguinte, `ρ + √(ρ² - a²/4) < r*(a)` para
  `a ∈ (0,2ρ)`.

## Reducao declarada

* `prop:teardrop` (i): o caso `a ∈ (0,2ρ)` (o livro trata `a = 2ρ` a parte, como imediato). Os
  tres arcos sao dados pelas parametrizacoes do livro (`arc1`, `arc2`, `arc3`, pelo angulo, com
  velocidade `ρ`, logo curvatura `1/ρ`). Prova-se: continuidade de posicao e de vetor tangente nas
  juncoes (a curva colada e `C¹` com tangente lipschitziana), pontas e tangentes nas pontas,
  as formulas de `|p|²` em cada arco, `cos ψ ≥ -sin β` (estrito no interior), o maximo `r*(a)`
  atingido em `ψ = 0`, a injetividade de cada arco e as intersecoes entre arcos (so nas juncoes).
  A curva colada NAO e construida como uma unica funcao de `[0,L]`; "mergulhada" significa aqui:
  cada arco injetivo e arcos distintos so se encontram nas juncoes.
* `prop:teardrop` (ii): so o padrao direita-esquerda-direita; o padrao espelhado segue pela
  reflexao `(x,y) ↦ (x,-y)` e NAO esta formalizado. A familia e parametrizada por
  `(y₀, α₁, α₂, α₃)` (`fam1`, `fam2`, `fam3`, com centros calculados como no livro); a condicao
  de tangente final `(-1,0)` e `cos(α₂ - α₁ - α₃) = -1`. "max|γ| ≥ r*" e provado na forma
  "ha um ponto do arco do meio com `|p|² ≥ r*²`"; a igualdade na forma "se todo ponto do arco do
  meio tem `|p|² ≤ r*²`, entao `(y₀,α₁,α₂,α₃) = (-a/2, β, π+2β, β)`".
* `prop:teardrop_lower`: **condicional**. O Lemma 2 de Ahn, Cheong, Matousek e Vigneron e o
  teorema da curva de Jordan nao estao na Mathlib; o disco `Δ = B̄(c,ρ)` que eles produzem entra
  pela hipotese explicita `hΔ : Δ ⊆ K ∪ D_R`, com `D_R = {x ≥ 0, |p| ≤ R}`. A condicao
  `Δ ∩ {x < 0} ⊆ K` do plano decorre de `hΔ` (pois `D_R ⊆ {x ≥ 0}`) e e dada como corolario.
  Formaliza-se o argumento das cordas e o ponto `f = c + ρ c/|c|`. Coordenadas: `ℝ × ℝ` com
  `|p|² = p.1² + p.2²` (funcao `nsq`), nao a norma do maximo de `ℝ × ℝ`.
-/

noncomputable section

namespace LeanReal.Chap09Teardrop

open Set Real Filter Topology

/-- Quadrado da norma euclidiana em `ℝ × ℝ`. -/
def nsq (p : ℝ × ℝ) : ℝ := p.1 ^ 2 + p.2 ^ 2

/-! ## Os parametros `β(a)` e `r*(a)` -/

/-- `cos β(a) = (1 + a/(2ρ))/2` (`prop:teardrop`). -/
def cb (ρ a : ℝ) : ℝ := (1 + a / (2 * ρ)) / 2

/-- `β(a) = arccos((1 + a/(2ρ))/2)` (`prop:teardrop`). -/
def beta (ρ a : ℝ) : ℝ := arccos (cb ρ a)

/-- `r*(a) = ρ(1 + 2 sin β(a))` (`prop:teardrop`). -/
def rstar (ρ a : ℝ) : ℝ := ρ * (1 + 2 * sin (beta ρ a))

/-- A segunda forma fechada `ρ(1 + √(4 - (1 + a/(2ρ))²))` (`prop:teardrop`). -/
def rstar' (ρ a : ℝ) : ℝ := ρ * (1 + √(4 - (1 + a / (2 * ρ)) ^ 2))

theorem cb_bounds {ρ a : ℝ} (hρ : 0 < ρ) (ha : 0 < a) (ha2 : a < 2 * ρ) :
    1 / 2 < cb ρ a ∧ cb ρ a < 1 := by
  have h1 : 0 < a / (2 * ρ) := by positivity
  have h2 : a / (2 * ρ) < 1 := by rw [div_lt_one (by positivity)]; exact ha2
  unfold cb; constructor <;> linarith

theorem cos_beta {ρ a : ℝ} (hρ : 0 < ρ) (ha : 0 < a) (ha2 : a < 2 * ρ) :
    cos (beta ρ a) = cb ρ a := by
  obtain ⟨h1, h2⟩ := cb_bounds hρ ha ha2
  exact cos_arccos (by linarith) h2.le

/-- `β(a) ∈ (0, π/3)` para `a ∈ (0,2ρ)`. -/
theorem beta_mem {ρ a : ℝ} (hρ : 0 < ρ) (ha : 0 < a) (ha2 : a < 2 * ρ) :
    0 < beta ρ a ∧ beta ρ a < π / 3 := by
  obtain ⟨h1, h2⟩ := cb_bounds hρ ha ha2
  refine ⟨arccos_pos.mpr h2, ?_⟩
  by_contra h
  rw [not_lt] at h
  have := cos_le_cos_of_nonneg_of_le_pi (by positivity : (0 : ℝ) ≤ π / 3) (arccos_le_pi _) h
  rw [cos_pi_div_three] at this
  have h3 := cos_beta hρ ha ha2
  unfold beta at h3
  linarith

/-- `a/2 = ρ(2 cos β - 1)` (prova de `prop:teardrop`). -/
theorem half_a {ρ a : ℝ} (hρ : 0 < ρ) (ha : 0 < a) (ha2 : a < 2 * ρ) :
    ρ * (2 * cos (beta ρ a) - 1) = a / 2 := by
  rw [cos_beta hρ ha ha2]; unfold cb; field_simp; ring

/-- `2 sin β(a) = √(4 - (1 + a/(2ρ))²)`, sem hipoteses. -/
theorem two_sin_beta (ρ a : ℝ) : 2 * sin (beta ρ a) = √(4 - (1 + a / (2 * ρ)) ^ 2) := by
  rw [beta, sin_arccos]
  have h : 4 - (1 + a / (2 * ρ)) ^ 2 = 2 ^ 2 * (1 - cb ρ a ^ 2) := by unfold cb; ring
  rw [h, sqrt_mul (by norm_num), sqrt_sq (by norm_num)]

/-- **As duas formas de `r*(a)` coincidem** (`prop:teardrop`). -/
theorem rstar_eq (ρ a : ℝ) : rstar ρ a = rstar' ρ a := by
  unfold rstar rstar'; rw [two_sin_beta]

/-! ## Os tres arcos da gota (parametro `b` = angulo dos arcos externos) -/

/-- Arco 1 (`u ∈ [0,b]`), centro `C₁ = (0,-2ρ cos b)`, angulo tangente `-u`. -/
def arc1 (ρ b u : ℝ) : ℝ × ℝ := (ρ * sin u, ρ * cos u - 2 * ρ * cos b)

/-- Arco 2 (`ψ ∈ [-π/2-b, π/2+b]`), centro `C₂ = (2ρ sin b, 0)`, angulo tangente `ψ + π/2`. -/
def arc2 (ρ b ψ : ℝ) : ℝ × ℝ := (2 * ρ * sin b + ρ * cos ψ, ρ * sin ψ)

/-- Arco 3 = reflexao `(x,y) ↦ (x,-y)` do arco 1, percorrido de `u = b` ate `u = 0`. -/
def arc3 (ρ b u : ℝ) : ℝ × ℝ := (ρ * sin u, 2 * ρ * cos b - ρ * cos u)

theorem arc1_hasDerivAt (ρ b u : ℝ) :
    HasDerivAt (arc1 ρ b) (ρ * cos u, -(ρ * sin u)) u := by
  unfold arc1
  have h := ((hasDerivAt_sin u).const_mul ρ).prodMk
    (((hasDerivAt_cos u).const_mul ρ).sub_const (2 * ρ * cos b))
  convert h using 1
  simp

theorem arc2_hasDerivAt (ρ b ψ : ℝ) :
    HasDerivAt (arc2 ρ b) (-(ρ * sin ψ), ρ * cos ψ) ψ := by
  unfold arc2
  have h := (((hasDerivAt_cos ψ).const_mul ρ).const_add (2 * ρ * sin b)).prodMk
    ((hasDerivAt_sin ψ).const_mul ρ)
  convert h using 1
  simp

theorem arc3_hasDerivAt (ρ b u : ℝ) :
    HasDerivAt (arc3 ρ b) (ρ * cos u, ρ * sin u) u := by
  unfold arc3
  have h := ((hasDerivAt_sin u).const_mul ρ).prodMk
    (((hasDerivAt_cos u).const_mul ρ).const_sub (2 * ρ * cos b))
  convert h using 1
  simp

/-- Cada arco esta no circulo de raio `ρ` em torno do seu centro (curvatura `1/ρ = κ*`). -/
theorem arcs_on_circles (ρ b t : ℝ) :
    nsq (arc1 ρ b t - (0, -2 * ρ * cos b)) = ρ ^ 2 ∧
    nsq (arc2 ρ b t - (2 * ρ * sin b, 0)) = ρ ^ 2 ∧
    nsq (arc3 ρ b t - (0, 2 * ρ * cos b)) = ρ ^ 2 := by
  have h := sin_sq_add_cos_sq t
  simp only [nsq, arc1, arc2, arc3, Prod.fst_sub, Prod.snd_sub]
  refine ⟨?_, ?_, ?_⟩ <;> linear_combination ρ ^ 2 * h

theorem cos_neg_half_pi_sub (b : ℝ) : cos (-(π / 2) - b) = -sin b := by
  rw [cos_sub, cos_neg, sin_neg, cos_pi_div_two, sin_pi_div_two]; ring

theorem sin_neg_half_pi_sub (b : ℝ) : sin (-(π / 2) - b) = -cos b := by
  rw [sin_sub, sin_neg, cos_neg, cos_pi_div_two, sin_pi_div_two]; ring

theorem cos_half_pi_add (b : ℝ) : cos (π / 2 + b) = -sin b := by
  rw [cos_add, cos_pi_div_two, sin_pi_div_two]; ring

theorem sin_half_pi_add (b : ℝ) : sin (π / 2 + b) = cos b := by
  rw [sin_add, cos_pi_div_two, sin_pi_div_two]; ring

/-- **Juncoes** (prova de `prop:teardrop`): posicao e vetor tangente coincidem nas juncoes; o
arco 3 e percorrido para tras, logo o seu tangente e `-arc3'`. Pontas e tangentes nas pontas. -/
theorem junctions (ρ b : ℝ) :
    arc1 ρ b b = arc2 ρ b (-(π / 2) - b) ∧
    ((ρ * cos b, -(ρ * sin b)) : ℝ × ℝ) =
      (-(ρ * sin (-(π / 2) - b)), ρ * cos (-(π / 2) - b)) ∧
    arc2 ρ b (π / 2 + b) = arc3 ρ b b ∧
    ((-(ρ * sin (π / 2 + b)), ρ * cos (π / 2 + b)) : ℝ × ℝ) = -(ρ * cos b, ρ * sin b) ∧
    arc1 ρ b 0 = (0, ρ - 2 * ρ * cos b) ∧ ((ρ * cos 0, -(ρ * sin 0)) : ℝ × ℝ) = (ρ, 0) ∧
    arc3 ρ b 0 = (0, 2 * ρ * cos b - ρ) ∧ (-(ρ * cos 0, ρ * sin 0) : ℝ × ℝ) = (-ρ, 0) := by
  refine ⟨Prod.ext ?_ ?_, Prod.ext ?_ ?_, Prod.ext ?_ ?_, Prod.ext ?_ ?_, Prod.ext ?_ ?_,
    Prod.ext ?_ ?_, Prod.ext ?_ ?_, Prod.ext ?_ ?_⟩
  all_goals (try simp only [arc1, arc2, arc3, cos_neg_half_pi_sub, sin_neg_half_pi_sub,
    cos_half_pi_add, sin_half_pi_add, cos_zero, sin_zero, Prod.fst_neg, Prod.snd_neg])
  all_goals ring

/-! ## Distancias a `M` -/

theorem nsq_arc1 (ρ b u : ℝ) : nsq (arc1 ρ b u) = ρ ^ 2 * (1 + 4 * cos b * (cos b - cos u)) := by
  have h := sin_sq_add_cos_sq u
  simp only [nsq, arc1]; linear_combination ρ ^ 2 * h

theorem nsq_arc2 (ρ b ψ : ℝ) : nsq (arc2 ρ b ψ) = ρ ^ 2 * (1 + 4 * sin b * (sin b + cos ψ)) := by
  have h := sin_sq_add_cos_sq ψ
  simp only [nsq, arc2]; linear_combination ρ ^ 2 * h

theorem nsq_arc3 (ρ b u : ℝ) : nsq (arc3 ρ b u) = nsq (arc1 ρ b u) := by
  simp only [nsq, arc1, arc3]; ring

/-- Hipoteses padrao sobre `b`: `0 < b < π/3`, `ρ > 0`. -/
structure Good (ρ b : ℝ) : Prop where
  hρ : 0 < ρ
  hb0 : 0 < b
  hb3 : b < π / 3

theorem Good.cos_gt {ρ b : ℝ} (h : Good ρ b) : 1 / 2 < cos b := by
  have := cos_lt_cos_of_nonneg_of_le_pi h.hb0.le (by linarith [pi_pos]) h.hb3
  rwa [cos_pi_div_three] at this

theorem Good.sin_pos {ρ b : ℝ} (h : Good ρ b) : 0 < sin b :=
  Real.sin_pos_of_pos_of_lt_pi h.hb0 (by linarith [pi_pos, h.hb3])

theorem Good.b_lt {ρ b : ℝ} (h : Good ρ b) : π / 2 + b < π := by linarith [h.hb3, pi_pos]

/-- `|p|²` cresce estritamente no arco 1, de `(ρ(2cos b - 1))²` a `ρ²`. -/
theorem arc1_strictMono {ρ b : ℝ} (h : Good ρ b) :
    StrictMonoOn (fun u => nsq (arc1 ρ b u)) (Icc 0 b) := by
  intro u hu v hv huv
  simp only [nsq_arc1]
  have hc := h.cos_gt
  have := cos_lt_cos_of_nonneg_of_le_pi hu.1 (by linarith [hv.2, h.b_lt, h.hb0]) huv
  have hρ2 : 0 < ρ ^ 2 := by have := h.hρ; positivity
  nlinarith [mul_pos hρ2 (by linarith : (0 : ℝ) < cos b)]

theorem nsq_arc1_zero (ρ b : ℝ) : nsq (arc1 ρ b 0) = (ρ * (2 * cos b - 1)) ^ 2 := by
  rw [nsq_arc1, cos_zero]; ring

theorem nsq_arc1_b (ρ b : ℝ) : nsq (arc1 ρ b b) = ρ ^ 2 := by rw [nsq_arc1]; ring

theorem nsq_arc1_le {ρ b u : ℝ} (h : Good ρ b) (hu : u ∈ Icc 0 b) : nsq (arc1 ρ b u) ≤ ρ ^ 2 := by
  rw [← nsq_arc1_b ρ b]
  exact (arc1_strictMono h).monotoneOn hu ⟨h.hb0.le, le_rfl⟩ hu.2

theorem arc1_injOn {ρ b : ℝ} (h : Good ρ b) : InjOn (arc1 ρ b) (Icc 0 b) := by
  intro u hu v hv huv
  exact (arc1_strictMono h).injOn hu hv (by simp only [huv])

theorem arc3_injOn {ρ b : ℝ} (h : Good ρ b) : InjOn (arc3 ρ b) (Icc 0 b) := by
  intro u hu v hv huv
  have h' : nsq (arc1 ρ b u) = nsq (arc1 ρ b v) := by rw [← nsq_arc3, ← nsq_arc3, huv]
  exact (arc1_strictMono h).injOn hu hv h'

/-- Arco 1: `y ≤ -a/2 < 0`, `x ≥ 0`, e `x = 0` so em `u = 0`. -/
theorem arc1_sides {ρ b u : ℝ} (h : Good ρ b) (hu : u ∈ Icc 0 b) :
    (arc1 ρ b u).2 ≤ ρ - 2 * ρ * cos b ∧ ρ - 2 * ρ * cos b < 0 ∧ 0 ≤ (arc1 ρ b u).1 ∧
    ((arc1 ρ b u).1 = 0 → u = 0) := by
  have hc := h.cos_gt
  have hρ := h.hρ
  have hub : u < π := by linarith [hu.2, h.b_lt, h.hb0]
  simp only [arc1]
  refine ⟨by nlinarith [cos_le_one u], by nlinarith, mul_nonneg hρ.le
    (sin_nonneg_of_nonneg_of_le_pi hu.1 hub.le), fun hx => ?_⟩
  rcases hu.1.lt_or_eq with hpos | hzero
  · have := Real.sin_pos_of_pos_of_lt_pi hpos hub
    nlinarith
  · exact hzero.symm

/-- `cos ψ ≥ -sin b` em `[-π/2-b, π/2+b]`, estrito no interior. -/
theorem cos_ge_neg_sin {ρ b ψ : ℝ} (h : Good ρ b) (hψ : |ψ| ≤ π / 2 + b) :
    -sin b ≤ cos ψ ∧ (|ψ| < π / 2 + b → -sin b < cos ψ) := by
  rw [← cos_abs ψ, ← cos_half_pi_add]
  refine ⟨cos_le_cos_of_nonneg_of_le_pi (abs_nonneg ψ) h.b_lt.le hψ, fun hlt => ?_⟩
  exact cos_lt_cos_of_nonneg_of_le_pi (abs_nonneg ψ) h.b_lt.le hlt

/-- Arco 2: `ρ² ≤ |p|² ≤ (ρ(1 + 2 sin b))²`, `|p|² > ρ²` no interior, `x ≥ ρ sin b > 0`. -/
theorem arc2_bounds {ρ b ψ : ℝ} (h : Good ρ b) (hψ : |ψ| ≤ π / 2 + b) :
    ρ ^ 2 ≤ nsq (arc2 ρ b ψ) ∧ nsq (arc2 ρ b ψ) ≤ (ρ * (1 + 2 * sin b)) ^ 2 ∧
    (|ψ| < π / 2 + b → ρ ^ 2 < nsq (arc2 ρ b ψ)) ∧ 0 < (arc2 ρ b ψ).1 := by
  obtain ⟨h1, h2⟩ := cos_ge_neg_sin h hψ
  have hs := h.sin_pos
  have hρ := h.hρ
  have hρ2 : 0 < ρ ^ 2 := by positivity
  rw [nsq_arc2]
  refine ⟨?_, ?_, fun hlt => ?_, ?_⟩
  · nlinarith [mul_nonneg hρ2.le (mul_nonneg hs.le (by linarith : 0 ≤ sin b + cos ψ))]
  · nlinarith [cos_le_one ψ, mul_nonneg hρ2.le hs.le]
  · have := h2 hlt
    nlinarith [mul_pos hρ2 (mul_pos hs (by linarith : 0 < sin b + cos ψ))]
  · simp only [arc2]; nlinarith

/-- O ponto mais distante: `|arc2(0)| = ρ(1 + 2 sin b)`. -/
theorem nsq_arc2_zero (ρ b : ℝ) : nsq (arc2 ρ b 0) = (ρ * (1 + 2 * sin b)) ^ 2 := by
  rw [nsq_arc2, cos_zero]; ring

/-- O arco 2 e injetivo em `[-π/2-b, π/2+b]` (gira `π + 2b < 2π`). -/
theorem arc2_injOn {ρ b : ℝ} (h : Good ρ b) :
    InjOn (arc2 ρ b) {ψ | |ψ| ≤ π / 2 + b} := by
  intro ψ₁ h₁ ψ₂ h₂ heq
  change |ψ₁| ≤ π / 2 + b at h₁
  change |ψ₂| ≤ π / 2 + b at h₂
  simp only [arc2, Prod.mk.injEq] at heq
  have hρ := h.hρ.ne'
  have hc : cos ψ₁ = cos ψ₂ := by
    have := heq.1; field_simp at this; linarith
  have hs : sin ψ₁ = sin ψ₂ := mul_left_cancel₀ hρ heq.2
  have hlt := h.b_lt
  have habs : |ψ₁| = |ψ₂| := by
    apply injOn_cos ⟨abs_nonneg _, by linarith⟩ ⟨abs_nonneg _, by linarith⟩
    rw [cos_abs, cos_abs, hc]
  rcases abs_eq_abs.mp habs with h' | h'
  · exact h'
  · rw [h', sin_neg] at hs
    have hz : sin ψ₂ = 0 := by linarith
    have hb2 := abs_le.mp h₂
    have := (sin_eq_zero_iff_of_lt_of_lt (by linarith) (by linarith)).mp hz
    rw [h', this, neg_zero]

/-- **Intersecoes**: o arco 2 encontra o arco 1 so na juncao `(u,ψ) = (b, -π/2-b)` e o arco 3
so na juncao `(u,ψ) = (b, π/2+b)`; os arcos 1 e 3 sao disjuntos. -/
theorem arcs_meet {ρ b : ℝ} (h : Good ρ b) :
    (∀ u ∈ Icc 0 b, ∀ ψ, |ψ| ≤ π / 2 + b → arc1 ρ b u = arc2 ρ b ψ →
      u = b ∧ ψ = -(π / 2) - b) ∧
    (∀ u ∈ Icc 0 b, ∀ ψ, |ψ| ≤ π / 2 + b → arc3 ρ b u = arc2 ρ b ψ →
      u = b ∧ ψ = π / 2 + b) ∧
    (∀ u ∈ Icc 0 b, ∀ v ∈ Icc 0 b, arc1 ρ b u ≠ arc3 ρ b v) := by
  have hc := h.cos_gt
  have hρ := h.hρ
  -- arco 3 tem y > 0
  have h3pos : ∀ v ∈ Icc 0 b, 0 < (arc3 ρ b v).2 := fun v hv => by
    have := (arc1_sides h hv).1
    have := (arc1_sides h hv).2.1
    simp only [arc1, arc3] at *; linarith
  -- ψ na fronteira se |arc2 ψ|² ≤ ρ²
  have hbd : ∀ ψ, |ψ| ≤ π / 2 + b → nsq (arc2 ρ b ψ) ≤ ρ ^ 2 → |ψ| = π / 2 + b := by
    intro ψ hψ hle
    by_contra hne
    have := (arc2_bounds h hψ).2.2.1 (lt_of_le_of_ne hψ hne)
    linarith
  have j := junctions ρ b
  refine ⟨fun u hu ψ hψ heq => ?_, fun u hu ψ hψ heq => ?_, fun u hu v hv heq => ?_⟩
  · have hle : nsq (arc2 ρ b ψ) ≤ ρ ^ 2 := by rw [← heq]; exact nsq_arc1_le h hu
    rcases abs_eq (by linarith [h.hb0, pi_pos] : (0 : ℝ) ≤ π / 2 + b) |>.mp
      (hbd ψ hψ hle) with hp | hn
    · exfalso
      rw [hp, j.2.2.1] at heq
      have := (arc1_sides h hu).2.1
      have := (arc1_sides h hu).1
      have := h3pos b ⟨h.hb0.le, le_rfl⟩
      rw [heq] at *; linarith
    · have hψ' : ψ = -(π / 2) - b := by linarith
      refine ⟨arc1_injOn h hu ⟨h.hb0.le, le_rfl⟩ ?_, hψ'⟩
      rw [heq, hψ', j.1]
  · have hle : nsq (arc2 ρ b ψ) ≤ ρ ^ 2 := by
      rw [← heq, nsq_arc3]; exact nsq_arc1_le h hu
    rcases abs_eq (by linarith [h.hb0, pi_pos] : (0 : ℝ) ≤ π / 2 + b) |>.mp
      (hbd ψ hψ hle) with hp | hn
    · refine ⟨arc3_injOn h hu ⟨h.hb0.le, le_rfl⟩ ?_, hp⟩
      rw [heq, hp, j.2.2.1]
    · exfalso
      have hψ' : ψ = -(π / 2) - b := by linarith
      rw [hψ', ← j.1] at heq
      have := h3pos u hu
      have := (arc1_sides h ⟨h.hb0.le, le_rfl⟩).1
      have := (arc1_sides h ⟨h.hb0.le, le_rfl⟩).2.1
      rw [heq] at *; linarith
  · have := (arc1_sides h hu).1
    have := (arc1_sides h hu).2.1
    have := h3pos v hv
    rw [heq] at *; linarith

/-! ## `prop:teardrop` (i) -/

/-- **Proposicao `prop:teardrop` (i)**, `a ∈ (0,2ρ)`, `b = β(a)`: a gota comeca em `(0,-a/2)` e
termina em `(0,a/2)`; esta em `{x ≥ 0}`; toca `{x = 0}` so nas pontas; todo ponto tem
`|p| ≤ r*(a)`, e `|arc2(0)| = r*(a)`; logo esta em `D_{r*(a)}`, e `max|γ_a| = r*(a)`. -/
theorem teardrop_i {ρ a : ℝ} (hρ : 0 < ρ) (ha : 0 < a) (ha2 : a < 2 * ρ) :
    let b := beta ρ a
    arc1 ρ b 0 = (0, -(a / 2)) ∧ arc3 ρ b 0 = (0, a / 2) ∧
    (∀ u ∈ Icc 0 b, 0 ≤ (arc1 ρ b u).1 ∧ ((arc1 ρ b u).1 = 0 → u = 0) ∧
        nsq (arc1 ρ b u) ≤ rstar ρ a ^ 2) ∧
    (∀ ψ, |ψ| ≤ π / 2 + b → 0 < (arc2 ρ b ψ).1 ∧ nsq (arc2 ρ b ψ) ≤ rstar ρ a ^ 2) ∧
    (∀ u ∈ Icc 0 b, 0 ≤ (arc3 ρ b u).1 ∧ ((arc3 ρ b u).1 = 0 → u = 0) ∧
        nsq (arc3 ρ b u) ≤ rstar ρ a ^ 2) ∧
    nsq (arc2 ρ b 0) = rstar ρ a ^ 2 := by
  intro b
  have hb := beta_mem hρ ha ha2
  have h : Good ρ b := ⟨hρ, hb.1, hb.2⟩
  have hha := half_a hρ ha ha2
  have hs := h.sin_pos
  have hρr : ρ ^ 2 ≤ rstar ρ a ^ 2 := by
    unfold rstar
    have : ρ ≤ ρ * (1 + 2 * sin (beta ρ a)) := by nlinarith
    nlinarith
  have j := junctions ρ b
  refine ⟨?_, ?_, fun u hu => ?_, fun ψ hψ => ?_, fun u hu => ?_, ?_⟩
  · rw [j.2.2.2.2.1, Prod.mk.injEq]; refine ⟨rfl, ?_⟩; linarith
  · rw [j.2.2.2.2.2.2.1, Prod.mk.injEq]; refine ⟨rfl, ?_⟩; linarith
  · obtain ⟨-, -, h3, h4⟩ := arc1_sides h hu
    exact ⟨h3, h4, (nsq_arc1_le h hu).trans hρr⟩
  · obtain ⟨-, h2, -, h4⟩ := arc2_bounds h hψ
    exact ⟨h4, h2⟩
  · obtain ⟨-, -, h3, h4⟩ := arc1_sides h hu
    refine ⟨?_, ?_, ?_⟩
    · simpa [arc1, arc3] using h3
    · simpa [arc1, arc3] using h4
    · rw [nsq_arc3]; exact (nsq_arc1_le h hu).trans hρr
  · rw [nsq_arc2_zero]; rfl

/-- **`prop:teardrop` (i), mergulho**: cada arco e injetivo, e arcos distintos so se encontram
nas juncoes (`b = β(a)`). -/
theorem teardrop_embedded {ρ a : ℝ} (hρ : 0 < ρ) (ha : 0 < a) (ha2 : a < 2 * ρ) :
    let b := beta ρ a
    InjOn (arc1 ρ b) (Icc 0 b) ∧ InjOn (arc2 ρ b) {ψ | |ψ| ≤ π / 2 + b} ∧
    InjOn (arc3 ρ b) (Icc 0 b) ∧
    (∀ u ∈ Icc 0 b, ∀ ψ, |ψ| ≤ π / 2 + b → arc1 ρ b u = arc2 ρ b ψ →
      u = b ∧ ψ = -(π / 2) - b) ∧
    (∀ u ∈ Icc 0 b, ∀ ψ, |ψ| ≤ π / 2 + b → arc3 ρ b u = arc2 ρ b ψ →
      u = b ∧ ψ = π / 2 + b) ∧
    (∀ u ∈ Icc 0 b, ∀ v ∈ Icc 0 b, arc1 ρ b u ≠ arc3 ρ b v) := by
  intro b
  have hb := beta_mem hρ ha ha2
  have h : Good ρ b := ⟨hρ, hb.1, hb.2⟩
  exact ⟨arc1_injOn h, arc2_injOn h, arc3_injOn h, arcs_meet h⟩

/-- **A gota satisfaz a hipotese de `prop:teardrop_lower`**: fora das pontas, `|p| > a/2`
(isto e, `γ_a` encontra `K = {|p| ≤ a/2}` so em `(0,∓a/2)`). -/
theorem teardrop_avoids_K {ρ a : ℝ} (hρ : 0 < ρ) (ha : 0 < a) (ha2 : a < 2 * ρ) :
    let b := beta ρ a
    (∀ u ∈ Ioc 0 b, (a / 2) ^ 2 < nsq (arc1 ρ b u)) ∧
    (∀ ψ, |ψ| ≤ π / 2 + b → (a / 2) ^ 2 < nsq (arc2 ρ b ψ)) ∧
    (∀ u ∈ Ioc 0 b, (a / 2) ^ 2 < nsq (arc3 ρ b u)) := by
  intro b
  have hb := beta_mem hρ ha ha2
  have h : Good ρ b := ⟨hρ, hb.1, hb.2⟩
  have hha := half_a hρ ha ha2
  have h1 : ∀ u ∈ Ioc 0 b, (a / 2) ^ 2 < nsq (arc1 ρ b u) := fun u hu => by
    have := (arc1_strictMono h) ⟨le_rfl, h.hb0.le⟩ ⟨hu.1.le, hu.2⟩ hu.1
    simp only at this
    rw [nsq_arc1_zero, hha] at this
    exact this
  refine ⟨h1, fun ψ hψ => ?_, fun u hu => by rw [nsq_arc3]; exact h1 u hu⟩
  have := (arc2_bounds h hψ).1
  nlinarith

/-! ## `prop:teardrop` (ii): a familia de tres arcos (padrao direita-esquerda-direita) -/

/-- Primeiro arco (direita, `u ∈ [0,α₁]`), partindo de `(0,y₀)` na direcao `(1,0)`. -/
def fam1 (ρ y0 u : ℝ) : ℝ × ℝ := (ρ * sin u, y0 - ρ + ρ * cos u)

/-- Centro do arco do meio, `C₂' = (2ρ sin α₁, y₀ - ρ + 2ρ cos α₁)`. -/
def C2f (ρ y0 α1 : ℝ) : ℝ × ℝ := (2 * ρ * sin α1, y0 - ρ + 2 * ρ * cos α1)

/-- Arco do meio (esquerda, `v ∈ [0,α₂]`), angulo tangente `v - α₁`. -/
def fam2 (ρ y0 α1 v : ℝ) : ℝ × ℝ :=
  (2 * ρ * sin α1 + ρ * sin (v - α1), y0 - ρ + 2 * ρ * cos α1 - ρ * cos (v - α1))

/-- Terceiro arco (direita, `w ∈ [0,α₃]`), angulo tangente `α₂ - α₁ - w`. -/
def fam3 (ρ y0 α1 α2 w : ℝ) : ℝ × ℝ :=
  (2 * ρ * sin α1 + 2 * ρ * sin (α2 - α1) - ρ * sin (α2 - α1 - w),
    y0 - ρ + 2 * ρ * cos α1 - 2 * ρ * cos (α2 - α1) + ρ * cos (α2 - α1 - w))

/-- Os tres arcos tem velocidade `ρ` e angulo tangente `-u`, `v - α₁`, `α₂ - α₁ - w`. -/
theorem fam_hasDerivAt (ρ y0 α1 α2 t : ℝ) :
    HasDerivAt (fam1 ρ y0) (ρ * cos (-t), ρ * sin (-t)) t ∧
    HasDerivAt (fam2 ρ y0 α1) (ρ * cos (t - α1), ρ * sin (t - α1)) t ∧
    HasDerivAt (fam3 ρ y0 α1 α2) (ρ * cos (α2 - α1 - t), ρ * sin (α2 - α1 - t)) t := by
  refine ⟨?_, ?_, ?_⟩
  all_goals (try unfold fam1)
  all_goals (try unfold fam2)
  all_goals (try unfold fam3)
  · have h := ((hasDerivAt_sin t).const_mul ρ).prodMk
      (((hasDerivAt_cos t).const_mul ρ).const_add (y0 - ρ))
    exact h.congr_deriv (by ext <;> (simp [cos_neg, sin_neg]; try ring))
  · have hl : HasDerivAt (fun v => v - α1) 1 t := (hasDerivAt_id t).sub_const α1
    have h := (((hl.sin).const_mul ρ).const_add (2 * ρ * sin α1)).prodMk
      (((hl.cos).const_mul ρ).const_sub (y0 - ρ + 2 * ρ * cos α1))
    exact h.congr_deriv (by ext <;> (simp; try ring))
  · have hl : HasDerivAt (fun w => α2 - α1 - w) (-1) t := by
      simpa using (hasDerivAt_id t).const_sub (α2 - α1)
    have h := (((hl.sin).const_mul ρ).const_sub (2 * ρ * sin α1 + 2 * ρ * sin (α2 - α1))).prodMk
      (((hl.cos).const_mul ρ).const_add (y0 - ρ + 2 * ρ * cos α1 - 2 * ρ * cos (α2 - α1)))
    exact h.congr_deriv (by ext <;> (simp; try ring))

/-- Juncoes da familia: posicoes coincidem (os tangentes coincidem por `fam_hasDerivAt`). -/
theorem fam_junctions (ρ y0 α1 α2 : ℝ) :
    fam1 ρ y0 0 = (0, y0) ∧ fam1 ρ y0 α1 = fam2 ρ y0 α1 0 ∧
    fam2 ρ y0 α1 α2 = fam3 ρ y0 α1 α2 0 := by
  simp only [fam1, fam2, fam3, sin_zero, cos_zero, zero_sub, sin_neg, cos_neg, sub_zero,
    Prod.mk.injEq]
  refine ⟨⟨by ring, by ring⟩, ⟨by ring, by ring⟩, ⟨by ring, by ring⟩⟩

/-- **Ponto final** (prova de `prop:teardrop` (ii)): se a tangente final e `(-1,0)`,
o fim e `(2ρ(sin α₁ - sin α₃), y₀ + 2ρ(cos α₁ + cos α₃ - 1))`. -/
theorem fam_end (ρ y0 α1 α2 α3 : ℝ) (hhead : cos (α2 - α1 - α3) = -1) :
    fam3 ρ y0 α1 α2 α3 =
      (2 * ρ * (sin α1 - sin α3), y0 + 2 * ρ * (cos α1 + cos α3 - 1)) := by
  have hs : sin (α2 - α1 - α3) = 0 := by
    have := sin_sq_add_cos_sq (α2 - α1 - α3)
    rw [hhead] at this; nlinarith
  have e : α2 - α1 = (α2 - α1 - α3) + α3 := by ring
  simp only [fam3, Prod.mk.injEq]
  rw [e, sin_add, cos_add, hhead, hs, add_sub_cancel_right, hhead, hs]
  constructor <;> ring

/-- `cos x = -1` com `x ∈ (-π, 2π)` implica `x = π`. -/
theorem eq_pi_of_cos {x : ℝ} (h1 : -π < x) (h2 : x < 2 * π) (hc : cos x = -1) : x = π := by
  rcases le_or_gt x π with hle | hgt
  · rcases le_or_gt 0 x with h0 | h0
    · exact injOn_cos ⟨h0, hle⟩ ⟨pi_pos.le, le_rfl⟩ (by rw [hc, cos_pi])
    · exfalso
      have := injOn_cos ⟨by linarith, by linarith⟩ ⟨pi_pos.le, le_rfl⟩
        (by rw [cos_neg, hc, cos_pi] : cos (-x) = cos π)
      linarith
  · exfalso
    have := injOn_cos ⟨by linarith, by linarith⟩ ⟨pi_pos.le, le_rfl⟩
      (by rw [cos_two_pi_sub, hc, cos_pi] : cos (2 * π - x) = cos π)
    linarith

/-- **Forma da familia** (prova de `prop:teardrop` (ii)): sob as hipoteses de `F_a`,
`α₁ = α₃ =: β'`, `β(a) ≤ β' < π/2` e `α₂ = π + 2β'`. -/
theorem family_shape {ρ a y0 α1 α2 α3 : ℝ} (hρ : 0 < ρ) (ha : 0 < a) (ha2 : a < 2 * ρ)
    (hα1 : α1 ∈ Icc 0 (π / 2)) (hα3 : α3 ∈ Icc 0 (π / 2)) (hα2 : α2 ∈ Ico 0 (2 * π))
    (hhead : cos (α2 - α1 - α3) = -1) (hx : (fam3 ρ y0 α1 α2 α3).1 = 0)
    (hy0 : y0 ∈ Icc (-(a / 2)) (a / 2))
    (hyE : (fam3 ρ y0 α1 α2 α3).2 ∈ Icc (-(a / 2)) (a / 2)) :
    α3 = α1 ∧ beta ρ a ≤ α1 ∧ α1 < π / 2 ∧ α2 = π + 2 * α1 := by
  rw [fam_end ρ y0 α1 α2 α3 hhead] at hx hyE
  simp only at hx hyE
  have hpi := pi_pos
  -- α₁ = α₃
  have hsin : sin α1 = sin α3 := by
    have : sin α1 - sin α3 = 0 := by
      rcases mul_eq_zero.mp hx with h | h
      · exfalso; linarith
      · exact h
    linarith
  have h13 : α1 = α3 :=
    injOn_sin ⟨by linarith [hα1.1], hα1.2⟩ ⟨by linarith [hα3.1], hα3.2⟩ hsin
  subst h13
  -- largura vertical
  have hspan1 : 2 * ρ * (2 * cos α1 - 1) ≤ a := by linarith [hy0.1, hyE.2]
  have hspan2 : -a ≤ 2 * ρ * (2 * cos α1 - 1) := by linarith [hy0.2, hyE.1]
  have hcb := cos_beta hρ ha ha2
  have hcos_le : cos α1 ≤ cos (beta ρ a) := by
    rw [hcb]; unfold cb
    have : 2 * cos α1 - 1 ≤ a / (2 * ρ) := by
      rw [le_div_iff₀ (by positivity)]; linarith
    linarith
  have hcos_pos : 0 < cos α1 := by
    have : -(a / (2 * ρ)) ≤ 2 * cos α1 - 1 := by
      rw [neg_le, neg_sub, le_div_iff₀ (by positivity)]; linarith
    have h2 : a / (2 * ρ) < 1 := by rw [div_lt_one (by positivity)]; exact ha2
    linarith
  have hlt : α1 < π / 2 := by
    rcases hα1.2.lt_or_eq with h | h
    · exact h
    · rw [h, cos_pi_div_two] at hcos_pos; exact absurd hcos_pos (lt_irrefl 0)
  have hbeta : beta ρ a ≤ α1 := by
    by_contra hcon
    rw [not_le] at hcon
    have := cos_lt_cos_of_nonneg_of_le_pi hα1.1 (arccos_le_pi _) hcon
    unfold beta at hcos_le this
    linarith
  refine ⟨rfl, hbeta, hlt, ?_⟩
  have := eq_pi_of_cos (x := α2 - α1 - α1) (by linarith [hα2.1]) (by linarith [hα2.2, hα1.1])
    hhead
  linarith

/-- Existe `φ ∈ [0,π]` com `X sin φ - T cos φ = √(X² + T²)` quando `X ≥ 0`. -/
theorem exists_dir (X T : ℝ) (hX : 0 ≤ X) :
    ∃ φ ∈ Icc 0 π, X * sin φ - T * cos φ = √(X ^ 2 + T ^ 2) := by
  set n := √(X ^ 2 + T ^ 2) with hn
  have hn2 : n ^ 2 = X ^ 2 + T ^ 2 := sq_sqrt (by positivity)
  have hn0 : 0 ≤ n := sqrt_nonneg _
  rcases hn0.lt_or_eq with hpos | hzero
  · have hT : (T / n) ^ 2 ≤ 1 := by
      rw [div_pow, div_le_one (by positivity)]; nlinarith
    have hT1 : -1 ≤ -T / n ∧ -T / n ≤ 1 := by
      have := abs_le_one_iff_mul_self_le_one.mpr
        (by rw [show (-T / n) * (-T / n) = (T / n) ^ 2 by ring]; exact hT)
      exact abs_le.mp this
    refine ⟨arccos (-T / n), ⟨arccos_nonneg _, arccos_le_pi _⟩, ?_⟩
    rw [cos_arccos hT1.1 hT1.2, sin_arccos]
    have h1 : 1 - (-T / n) ^ 2 = (X / n) ^ 2 := by
      field_simp; nlinarith
    rw [h1, sqrt_sq (by positivity)]
    field_simp
    nlinarith
  · refine ⟨0, ⟨le_rfl, pi_pos.le⟩, ?_⟩
    have h0 : X ^ 2 + T ^ 2 = 0 := by rw [← hn2, ← hzero]; ring
    have hX0 : X = 0 := by nlinarith [sq_nonneg X, sq_nonneg T]
    have hT0 : T = 0 := by nlinarith [sq_nonneg X, sq_nonneg T]
    rw [hX0, hT0, ← hzero]; simp

/-- O arco do meio contem o ponto `C₂' + ρ C₂'/|C₂'|`: ha `v ∈ [0, π + 2β']` com
`|fam2 v|² = (|C₂'| + ρ)²`. -/
theorem far_point (ρ y0 b' : ℝ) (hρ : 0 < ρ) (hb' : b' ∈ Icc 0 (π / 2)) :
    ∃ v ∈ Icc 0 (π + 2 * b'),
      nsq (fam2 ρ y0 b' v) = (√(nsq (C2f ρ y0 b')) + ρ) ^ 2 := by
  have hX : 0 ≤ 2 * ρ * sin b' :=
    mul_nonneg (by positivity) (sin_nonneg_of_nonneg_of_le_pi hb'.1 (by linarith [hb'.2, pi_pos]))
  obtain ⟨φ, hφ, hφeq⟩ := exists_dir (2 * ρ * sin b') (y0 - ρ + 2 * ρ * cos b') hX
  refine ⟨φ + b', ⟨by linarith [hφ.1, hb'.1], by linarith [hφ.2, hb'.1]⟩, ?_⟩
  have hn2 : √(nsq (C2f ρ y0 b')) ^ 2 = nsq (C2f ρ y0 b') :=
    sq_sqrt (by unfold nsq; positivity)
  simp only [nsq, C2f, fam2, add_sub_cancel_right] at *
  have h := sin_sq_add_cos_sq φ
  linear_combination (-1 : ℝ) * hn2 + ρ ^ 2 * h + 2 * ρ * hφeq

/-- **Proposicao `prop:teardrop` (ii), cota**: toda curva `γ ∈ F_a` (padrao
direita-esquerda-direita) tem um ponto, no arco do meio, com `|p|² ≥ r*(a)²`. -/
theorem family_lower {ρ a y0 α1 α2 α3 : ℝ} (hρ : 0 < ρ) (ha : 0 < a) (ha2 : a < 2 * ρ)
    (hα1 : α1 ∈ Icc 0 (π / 2)) (hα3 : α3 ∈ Icc 0 (π / 2)) (hα2 : α2 ∈ Ico 0 (2 * π))
    (hhead : cos (α2 - α1 - α3) = -1) (hx : (fam3 ρ y0 α1 α2 α3).1 = 0)
    (hy0 : y0 ∈ Icc (-(a / 2)) (a / 2))
    (hyE : (fam3 ρ y0 α1 α2 α3).2 ∈ Icc (-(a / 2)) (a / 2)) :
    ∃ v ∈ Icc 0 α2, rstar ρ a ^ 2 ≤ nsq (fam2 ρ y0 α1 v) := by
  obtain ⟨-, hb, hlt, h2⟩ := family_shape hρ ha ha2 hα1 hα3 hα2 hhead hx hy0 hyE
  obtain ⟨v, hv, hveq⟩ := far_point ρ y0 α1 hρ hα1
  refine ⟨v, h2 ▸ hv, ?_⟩
  rw [hveq]
  have hbm := beta_mem hρ ha ha2
  have hsin : sin (beta ρ a) ≤ sin α1 :=
    sin_le_sin_of_le_of_le_pi_div_two (by linarith [hbm.1, pi_pos]) hα1.2 hb
  have hsβ : 0 ≤ sin (beta ρ a) :=
    sin_nonneg_of_nonneg_of_le_pi hbm.1.le (by linarith [hbm.2, pi_pos])
  have hXn : 2 * ρ * sin α1 ≤ √(nsq (C2f ρ y0 α1)) := by
    apply Real.le_sqrt_of_sq_le
    simp only [nsq, C2f]; nlinarith [sq_nonneg (y0 - ρ + 2 * ρ * cos α1)]
  have h1 : 0 ≤ rstar ρ a := by unfold rstar; positivity
  have h3 : rstar ρ a ≤ √(nsq (C2f ρ y0 α1)) + ρ := by unfold rstar; nlinarith
  exact pow_le_pow_left₀ h1 h3 2

/-- **Proposicao `prop:teardrop` (ii), igualdade**: se todo ponto do arco do meio de `γ ∈ F_a`
tem `|p| ≤ r*(a)`, entao `γ = γ_a`: `(y₀, α₁, α₂, α₃) = (-a/2, β, π + 2β, β)`. -/
theorem family_eq {ρ a y0 α1 α2 α3 : ℝ} (hρ : 0 < ρ) (ha : 0 < a) (ha2 : a < 2 * ρ)
    (hα1 : α1 ∈ Icc 0 (π / 2)) (hα3 : α3 ∈ Icc 0 (π / 2)) (hα2 : α2 ∈ Ico 0 (2 * π))
    (hhead : cos (α2 - α1 - α3) = -1) (hx : (fam3 ρ y0 α1 α2 α3).1 = 0)
    (hy0 : y0 ∈ Icc (-(a / 2)) (a / 2))
    (hyE : (fam3 ρ y0 α1 α2 α3).2 ∈ Icc (-(a / 2)) (a / 2))
    (hmax : ∀ v ∈ Icc 0 α2, nsq (fam2 ρ y0 α1 v) ≤ rstar ρ a ^ 2) :
    y0 = -(a / 2) ∧ α1 = beta ρ a ∧ α3 = beta ρ a ∧ α2 = π + 2 * beta ρ a := by
  obtain ⟨h31, hb, hlt, h2⟩ := family_shape hρ ha ha2 hα1 hα3 hα2 hhead hx hy0 hyE
  obtain ⟨v, hv, hveq⟩ := far_point ρ y0 α1 hρ hα1
  have hle := hmax v (h2 ▸ hv)
  rw [hveq] at hle
  have hbm := beta_mem hρ ha ha2
  have hsin : sin (beta ρ a) ≤ sin α1 :=
    sin_le_sin_of_le_of_le_pi_div_two (by linarith [hbm.1, pi_pos]) hα1.2 hb
  have hsβ : 0 ≤ sin (beta ρ a) :=
    sin_nonneg_of_nonneg_of_le_pi hbm.1.le (by linarith [hbm.2, pi_pos])
  set n := √(nsq (C2f ρ y0 α1)) with hn
  have hn0 : 0 ≤ n := sqrt_nonneg _
  have hn2 : n ^ 2 = nsq (C2f ρ y0 α1) := sq_sqrt (by unfold nsq; positivity)
  have hXn : 2 * ρ * sin α1 ≤ n := by
    apply Real.le_sqrt_of_sq_le
    simp only [nsq, C2f]; nlinarith [sq_nonneg (y0 - ρ + 2 * ρ * cos α1)]
  have h1 : 0 ≤ rstar ρ a := by unfold rstar; positivity
  have hup : n + ρ ≤ rstar ρ a :=
    (pow_le_pow_iff_left₀ (by positivity) h1 two_ne_zero).mp hle
  unfold rstar at hup
  have hsin_eq : sin α1 = sin (beta ρ a) := by nlinarith
  have hα1β : α1 = beta ρ a :=
    injOn_sin ⟨by linarith [hα1.1, pi_pos], hα1.2⟩ ⟨by linarith [hbm.1, pi_pos],
      by linarith [hbm.2, pi_pos]⟩ hsin_eq
  have hnX : n = 2 * ρ * sin α1 := by nlinarith
  have hT : y0 - ρ + 2 * ρ * cos α1 = 0 := by
    have : n ^ 2 = (2 * ρ * sin α1) ^ 2 := by rw [hnX]
    rw [hn2] at this; simp only [nsq, C2f] at this
    nlinarith [sq_nonneg (y0 - ρ + 2 * ρ * cos α1)]
  have hha := half_a hρ ha ha2
  rw [hα1β] at hT
  refine ⟨by linarith, hα1β, h31 ▸ hα1β, by rw [h2, hα1β]⟩

/-- **A gota pertence a `F_a`** e coincide com ela, arco a arco: `fam1 = arc1`,
`fam2(v) = arc2(v - β - π/2)`, `fam3(w) = arc3(β - w)`; todas as hipoteses de `family_lower`
valem e todo ponto do arco do meio tem `|p| ≤ r*(a)` (a cota e atingida). -/
theorem teardrop_mem_family {ρ a : ℝ} (hρ : 0 < ρ) (ha : 0 < a) (ha2 : a < 2 * ρ) :
    let b := beta ρ a
    (∀ u, fam1 ρ (-(a / 2)) u = arc1 ρ b u) ∧
    (∀ v, fam2 ρ (-(a / 2)) b v = arc2 ρ b (v - b - π / 2)) ∧
    (∀ w, fam3 ρ (-(a / 2)) b (π + 2 * b) w = arc3 ρ b (b - w)) ∧
    b ∈ Icc 0 (π / 2) ∧ π + 2 * b ∈ Ico 0 (2 * π) ∧ cos (π + 2 * b - b - b) = -1 ∧
    (fam3 ρ (-(a / 2)) b (π + 2 * b) b).1 = 0 ∧
    -(a / 2) ∈ Icc (-(a / 2)) (a / 2) ∧
    (fam3 ρ (-(a / 2)) b (π + 2 * b) b).2 ∈ Icc (-(a / 2)) (a / 2) ∧
    (∀ v ∈ Icc 0 (π + 2 * b), nsq (fam2 ρ (-(a / 2)) b v) ≤ rstar ρ a ^ 2) := by
  intro b
  have hbm := beta_mem hρ ha ha2
  have hha := half_a hρ ha ha2
  have hpi := pi_pos
  have hc : cos (π + 2 * b - b - b) = -1 := by
    rw [show π + 2 * b - b - b = π by ring, cos_pi]
  have hend := fam_end ρ (-(a / 2)) b (π + 2 * b) b hc
  have hs := sin_nonneg_of_nonneg_of_le_pi hbm.1.le (by linarith [hbm.2])
  refine ⟨fun u => ?_, fun v => ?_, fun w => ?_, ⟨hbm.1.le, by linarith [hbm.2]⟩,
    ⟨by linarith [hbm.1], by linarith [hbm.2]⟩, hc, ?_, ⟨le_rfl, by linarith⟩, ?_,
    fun v _ => ?_⟩
  · simp only [fam1, arc1, Prod.mk.injEq, true_and]; linarith
  · simp only [fam2, arc2, Prod.mk.injEq]
    have e1 : cos (v - b - π / 2) = sin (v - b) := by
      rw [show v - b - π / 2 = (v - b) - π / 2 by ring, cos_sub_pi_div_two]
    have e2 : sin (v - b - π / 2) = -cos (v - b) := by
      rw [show v - b - π / 2 = (v - b) - π / 2 by ring, sin_sub_pi_div_two]
    rw [e1, e2]; constructor <;> linarith
  · simp only [fam3, arc3, Prod.mk.injEq]
    have e1 : sin (π + 2 * b - b) = -sin b := by
      rw [show π + 2 * b - b = b + π by ring, sin_add_pi]
    have e2 : cos (π + 2 * b - b) = -cos b := by
      rw [show π + 2 * b - b = b + π by ring, cos_add_pi]
    have e3 : sin (π + 2 * b - b - w) = -sin (b - w) := by
      rw [show π + 2 * b - b - w = (b - w) + π by ring, sin_add_pi]
    have e4 : cos (π + 2 * b - b - w) = -cos (b - w) := by
      rw [show π + 2 * b - b - w = (b - w) + π by ring, cos_add_pi]
    rw [e1, e2, e3, e4]; constructor <;> linarith
  · rw [hend]; simp
  · rw [hend]; simp only
    constructor <;> linarith
  · simp only [nsq, fam2]
    have h := sin_sq_add_cos_sq (v - b)
    unfold rstar
    have hT : -(a / 2) - ρ + 2 * ρ * cos b = 0 := by linarith
    have hsv := sin_le_one (v - b)
    have e : (-(a / 2) - ρ + 2 * ρ * cos b - ρ * cos (v - b)) = -(ρ * cos (v - b)) := by
      linarith
    rw [e]
    nlinarith [mul_nonneg (mul_nonneg hρ.le hρ.le) (mul_nonneg hs (by linarith : 0 ≤ 1 - sin (v - b)))]

/-! ### Mutantes de `prop:teardrop` provados FALSOS -/

/-- Mutante (i): "o arco 2 fica estritamente fora do disco `|p| ≤ ρ`" em TODO o intervalo
fechado. Falso: na juncao `ψ = π/2 + β`, `|p| = ρ` (caso `ρ = 1`, `a = 1`). -/
theorem mutant_arc2_strict_false :
    ¬ (∀ ψ, |ψ| ≤ π / 2 + beta 1 1 → (1 : ℝ) ^ 2 < nsq (arc2 1 (beta 1 1) ψ)) := by
  intro h
  have hb := beta_mem (ρ := 1) (a := 1) one_pos one_pos (by norm_num)
  have hψ : |π / 2 + beta 1 1| ≤ π / 2 + beta 1 1 := by
    rw [abs_of_pos (by linarith [pi_pos, hb.1])]
  have := h _ hψ
  rw [(junctions 1 (beta 1 1)).2.2.1, nsq_arc3, nsq_arc1_b] at this
  exact lt_irrefl _ this

/-- Mutante (ii) sem as pontas na boca `W_a`: falso. O semicirculo `α₁ = α₃ = 0`, `α₂ = π`,
`y₀ = -1` (`ρ = a = 1`) tem `|p| = 1 < r*(1)` em todo o arco do meio. -/
theorem mutant_family_no_mouth_false :
    ¬ (∀ (y0 α1 α2 α3 : ℝ), α1 ∈ Icc 0 (π / 2) → α3 ∈ Icc 0 (π / 2) →
        α2 ∈ Ico 0 (2 * π) → cos (α2 - α1 - α3) = -1 → (fam3 1 y0 α1 α2 α3).1 = 0 →
        ∃ v ∈ Icc 0 α2, rstar 1 1 ^ 2 ≤ nsq (fam2 1 y0 α1 v)) := by
  intro h
  have hpi := pi_pos
  have hc : cos (π - 0 - 0) = -1 := by simp
  obtain ⟨v, -, hv⟩ := h (-1) 0 π 0 ⟨le_rfl, by linarith⟩ ⟨le_rfl, by linarith⟩
    ⟨hpi.le, by linarith⟩ hc (by rw [fam_end 1 (-1) 0 π 0 hc]; simp)
  have hb := beta_mem (ρ := 1) (a := 1) one_pos one_pos (by norm_num)
  have hs := Real.sin_pos_of_pos_of_lt_pi hb.1 (by linarith [hb.2])
  have hn : nsq (fam2 1 (-1) 0 v) = 1 := by
    simp only [nsq, fam2]; simp; linear_combination sin_sq_add_cos_sq v
  rw [hn] at hv
  unfold rstar at hv
  nlinarith

/-- Mutante (ii) com cota estrita `r*² < |p|²` para algum ponto: falso pela propria gota. -/
theorem mutant_family_strict_false :
    ¬ (∀ (y0 α1 α2 α3 : ℝ), α1 ∈ Icc 0 (π / 2) → α3 ∈ Icc 0 (π / 2) →
        α2 ∈ Ico 0 (2 * π) → cos (α2 - α1 - α3) = -1 → (fam3 1 y0 α1 α2 α3).1 = 0 →
        y0 ∈ Icc (-(1 / 2)) (1 / 2) → (fam3 1 y0 α1 α2 α3).2 ∈ Icc (-(1 / 2)) (1 / 2) →
        ∃ v ∈ Icc 0 α2, rstar 1 1 ^ 2 < nsq (fam2 1 y0 α1 v)) := by
  intro h
  obtain ⟨-, -, -, h1, h2, h3, h4, h5, h6, h7⟩ :=
    teardrop_mem_family (ρ := 1) (a := 1) one_pos one_pos (by norm_num)
  obtain ⟨v, hv, hlt⟩ := h _ _ _ _ h1 h1 h2 h3 h4 h5 h6
  exact absurd (h7 v hv) (not_le.mpr hlt)

/-! ## `prop:teardrop_lower` (condicional) e a comparacao com `r*(a)` -/

/-- **Proposicao `prop:teardrop_lower`**, argumento das cordas, CONDICIONAL. Dados: o disco
`K = B̄((0,m₂), r_K)` com `0 ≤ r_K ≤ a/2` (diametro `[q₀,q₁]` em `{x = 0}`), as pontas
`q₀,q₁ = (0, m₂ ∓ r_K)` em `D_R`, e o disco `Δ = B̄((c₁,c₂), ρ)`.
`hΔ` (o Lemma 2 de Ahn-Cheong-Matousek-Vigneron mais Jordan, nao formalizados) diz
`Δ ⊆ K ∪ D_R`, com `D_R = {x ≥ 0, |p| ≤ R}`. Conclusao: `R ≥ ρ + √(ρ² - a²/4)`. -/
theorem teardrop_lower (ρ a R m2 rK c1 c2 : ℝ) (hρ : 0 < ρ) (ha2 : a < 2 * ρ)
    (hrK0 : 0 ≤ rK) (hrK : rK ≤ a / 2) (hR : 0 ≤ R)
    (hq0 : (m2 - rK) ^ 2 ≤ R ^ 2) (hq1 : (m2 + rK) ^ 2 ≤ R ^ 2)
    (hΔ : ∀ p : ℝ × ℝ, (p.1 - c1) ^ 2 + (p.2 - c2) ^ 2 ≤ ρ ^ 2 →
      p.1 ^ 2 + (p.2 - m2) ^ 2 ≤ rK ^ 2 ∨ (0 ≤ p.1 ∧ p.1 ^ 2 + p.2 ^ 2 ≤ R ^ 2)) :
    ρ + √(ρ ^ 2 - a ^ 2 / 4) ≤ R := by
  have hrKρ : rK < ρ := by linarith
  set d := √(ρ ^ 2 - rK ^ 2) with hd
  have hd2 : d ^ 2 = ρ ^ 2 - rK ^ 2 := sq_sqrt (by nlinarith)
  have hdpos : 0 < d := sqrt_pos.mpr (by nlinarith)
  -- passo das cordas: c₁ ≥ d
  have hc1 : d ≤ c1 := by
    by_contra hcon
    rw [not_le] at hcon
    -- escolha de t < 0 com (t - c₁)² < d²
    obtain ⟨t, ht0, htd⟩ : ∃ t : ℝ, t < 0 ∧ (t - c1) ^ 2 < d ^ 2 := by
      rcases lt_or_ge c1 0 with hneg | hnn
      · exact ⟨c1, hneg, by simp; positivity⟩
      · refine ⟨(c1 - d) / 2, by linarith, ?_⟩
        nlinarith
    set h := √(ρ ^ 2 - (t - c1) ^ 2) with hh
    have hh2 : h ^ 2 = ρ ^ 2 - (t - c1) ^ 2 := sq_sqrt (by nlinarith)
    have hp := hΔ (t, c2 + h) (by simp only; nlinarith)
    have hm := hΔ (t, c2 - h) (by simp only; nlinarith)
    simp only at hp hm
    rcases hp with hp | hp
    · rcases hm with hm | hm
      · nlinarith
      · linarith [hm.1]
    · linarith [hp.1]
  -- o ponto f = c + ρ c/|c|
  set n := √(c1 ^ 2 + c2 ^ 2) with hn
  have hn2 : n ^ 2 = c1 ^ 2 + c2 ^ 2 := sq_sqrt (by positivity)
  have hnc1 : c1 ≤ n := Real.le_sqrt_of_sq_le (by nlinarith)
  have hnpos : 0 < n := by linarith
  set l := (n + ρ) / n with hl
  have hfΔ : (l * c1 - c1) ^ 2 + (l * c2 - c2) ^ 2 ≤ ρ ^ 2 := by
    have : l - 1 = ρ / n := by rw [hl]; field_simp; ring
    have e : (l * c1 - c1) ^ 2 + (l * c2 - c2) ^ 2 = (l - 1) ^ 2 * (c1 ^ 2 + c2 ^ 2) := by ring
    exact le_of_eq (by rw [e, this, ← hn2, div_pow, div_mul_cancel₀ _ (by positivity)])
  have hfn : (l * c1) ^ 2 + (l * c2) ^ 2 = (n + ρ) ^ 2 := by
    have e : (l * c1) ^ 2 + (l * c2) ^ 2 = l ^ 2 * (c1 ^ 2 + c2 ^ 2) := by ring
    rw [e, ← hn2, hl]; field_simp
  have hfR : (n + ρ) ^ 2 ≤ R ^ 2 := by
    rcases hΔ (l * c1, l * c2) hfΔ with hK | hD
    · simp only at hK
      -- pontos de K tem |p| ≤ |m₂| + r_K ≤ R
      have habs : |l * c2 - m2| ≤ rK := by
        apply abs_le_of_sq_le_sq' _ hrK0 |>.elim (fun h1 h2 => abs_le.mpr ⟨h1, h2⟩)
        nlinarith [sq_nonneg (l * c1)]
      have hm : (|m2| + rK) ^ 2 ≤ R ^ 2 := by
        rcases abs_cases m2 with ⟨h1, _⟩ | ⟨h1, _⟩ <;> rw [h1]
        · exact hq1
        · nlinarith
      rw [← hfn]
      have h1 := abs_le.mp habs
      rcases abs_cases m2 with ⟨h2, h3⟩ | ⟨h2, h3⟩ <;> rw [h2] at hm <;>
        nlinarith [sq_nonneg (l * c1)]
    · rw [← hfn]; exact hD.2
  have hnR : n + ρ ≤ R := (pow_le_pow_iff_left₀ (by positivity) hR two_ne_zero).mp hfR
  have hsq : √(ρ ^ 2 - a ^ 2 / 4) ≤ d := Real.sqrt_le_sqrt (by nlinarith)
  linarith

/-- Forma do plano: com as duas hipoteses `Δ ⊆ K ∪ D_R` e `Δ ∩ {x < 0} ⊆ K`. A segunda nao e
usada (decorre da primeira, pois `D_R ⊆ {x ≥ 0}`). -/
theorem teardrop_lower' (ρ a R m2 rK c1 c2 : ℝ) (hρ : 0 < ρ) (ha2 : a < 2 * ρ)
    (hrK0 : 0 ≤ rK) (hrK : rK ≤ a / 2) (hR : 0 ≤ R)
    (hq0 : (m2 - rK) ^ 2 ≤ R ^ 2) (hq1 : (m2 + rK) ^ 2 ≤ R ^ 2)
    (hΔ : ∀ p : ℝ × ℝ, (p.1 - c1) ^ 2 + (p.2 - c2) ^ 2 ≤ ρ ^ 2 →
      p.1 ^ 2 + (p.2 - m2) ^ 2 ≤ rK ^ 2 ∨ (0 ≤ p.1 ∧ p.1 ^ 2 + p.2 ^ 2 ≤ R ^ 2))
    (_hneg : ∀ p : ℝ × ℝ, (p.1 - c1) ^ 2 + (p.2 - c2) ^ 2 ≤ ρ ^ 2 → p.1 < 0 →
      p.1 ^ 2 + (p.2 - m2) ^ 2 ≤ rK ^ 2) :
    ρ + √(ρ ^ 2 - a ^ 2 / 4) ≤ R :=
  teardrop_lower ρ a R m2 rK c1 c2 hρ ha2 hrK0 hrK hR hq0 hq1 hΔ

/-- **Testemunha (nitidez)**: para `0 ≤ r_K < ρ`, o disco `Δ` de centro `(√(ρ² - r_K²), 0)`
(o arco obliquo do livro, com `r_K = a/2`), `K = B̄(0, r_K)` e `R = ρ + √(ρ² - r_K²)`
satisfazem as hipoteses; `R` e exatamente o valor da cota. -/
theorem witness_lower (ρ rK : ℝ) (hρ : 0 < ρ) (hrK0 : 0 ≤ rK) (hrKρ : rK < ρ) :
    let d := √(ρ ^ 2 - rK ^ 2)
    0 ≤ ρ + d ∧ (0 - rK) ^ 2 ≤ (ρ + d) ^ 2 ∧ (0 + rK) ^ 2 ≤ (ρ + d) ^ 2 ∧
    (∀ p : ℝ × ℝ, (p.1 - d) ^ 2 + (p.2 - 0) ^ 2 ≤ ρ ^ 2 →
      p.1 ^ 2 + (p.2 - 0) ^ 2 ≤ rK ^ 2 ∨ (0 ≤ p.1 ∧ p.1 ^ 2 + p.2 ^ 2 ≤ (ρ + d) ^ 2)) := by
  intro d
  have hd2 : d ^ 2 = ρ ^ 2 - rK ^ 2 := sq_sqrt (by nlinarith)
  have hd0 : 0 ≤ d := sqrt_nonneg _
  refine ⟨by positivity, by nlinarith, by nlinarith, fun p hp => ?_⟩
  rcases lt_or_ge p.1 0 with hneg | hnn
  · left; nlinarith [mul_nonneg hd0 (by linarith : 0 ≤ -p.1)]
  · right
    refine ⟨hnn, ?_⟩
    have h1 : p.1 - d ≤ ρ := by nlinarith [sq_nonneg (p.2 - 0)]
    nlinarith

/-- A testemunha aplicada ao teorema com `r_K = a/2`: a cota vale com igualdade. -/
theorem witness_lower_sharp (ρ a : ℝ) (hρ : 0 < ρ) (ha : 0 < a) (ha2 : a < 2 * ρ) :
    ρ + √(ρ ^ 2 - a ^ 2 / 4) ≤ ρ + √(ρ ^ 2 - (a / 2) ^ 2) ∧
    ρ + √(ρ ^ 2 - (a / 2) ^ 2) = ρ + √(ρ ^ 2 - a ^ 2 / 4) := by
  obtain ⟨h0, h1, h2, h3⟩ := witness_lower ρ (a / 2) hρ (by positivity) (by linarith)
  refine ⟨teardrop_lower ρ a _ 0 (a / 2) _ 0 hρ ha2 (by positivity) le_rfl h0 h1 h2 h3, ?_⟩
  ring_nf

/-- Mutante: conclusao estrita `ρ + √(ρ² - a²/4) < R`. Falso pela testemunha (`ρ = a = 1`). -/
theorem mutant_lower_strict_false :
    ¬ (∀ (ρ a R m2 rK c1 c2 : ℝ), 0 < ρ → a < 2 * ρ → 0 ≤ rK → rK ≤ a / 2 → 0 ≤ R →
        (m2 - rK) ^ 2 ≤ R ^ 2 → (m2 + rK) ^ 2 ≤ R ^ 2 →
        (∀ p : ℝ × ℝ, (p.1 - c1) ^ 2 + (p.2 - c2) ^ 2 ≤ ρ ^ 2 →
          p.1 ^ 2 + (p.2 - m2) ^ 2 ≤ rK ^ 2 ∨ (0 ≤ p.1 ∧ p.1 ^ 2 + p.2 ^ 2 ≤ R ^ 2)) →
        ρ + √(ρ ^ 2 - a ^ 2 / 4) < R) := by
  intro h
  obtain ⟨h0, h1, h2, h3⟩ := witness_lower 1 (1 / 2) one_pos (by norm_num) (by norm_num)
  have := h 1 1 _ 0 (1 / 2) _ 0 one_pos (by norm_num) (by norm_num) (by norm_num) h0 h1 h2 h3
  norm_num at this

/-- Mutante: `D_R` sem a restricao `x ≥ 0` (disco inteiro). Falso: `Δ = B̄(0,ρ)`, `R = ρ`,
`K = B̄(0, a/2)` (`ρ = a = 1`) satisfazem as hipoteses e `1 + √(3/4) ≤ 1` e falso. -/
theorem mutant_lower_full_disc_false :
    ¬ (∀ (ρ a R m2 rK c1 c2 : ℝ), 0 < ρ → a < 2 * ρ → 0 ≤ rK → rK ≤ a / 2 → 0 ≤ R →
        (m2 - rK) ^ 2 ≤ R ^ 2 → (m2 + rK) ^ 2 ≤ R ^ 2 →
        (∀ p : ℝ × ℝ, (p.1 - c1) ^ 2 + (p.2 - c2) ^ 2 ≤ ρ ^ 2 →
          p.1 ^ 2 + (p.2 - m2) ^ 2 ≤ rK ^ 2 ∨ p.1 ^ 2 + p.2 ^ 2 ≤ R ^ 2) →
        ρ + √(ρ ^ 2 - a ^ 2 / 4) ≤ R) := by
  intro h
  have := h 1 1 1 0 (1 / 2) 0 0 one_pos (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) (fun p hp => Or.inr (by simpa using hp))
  have hs : 0 < √((1 : ℝ) ^ 2 - 1 ^ 2 / 4) := sqrt_pos.mpr (by norm_num)
  linarith

/-- Mutante: sem `r_K ≤ a/2`. Falso: `ρ = a = 1`, `r_K = 9/10` (corda `[q₀,q₁]` mais longa que
a boca); a testemunha com esse `r_K` da `R = 1 + √(19/100) < 1 + √(3/4)`. -/
theorem mutant_lower_no_rK_false :
    ¬ (∀ (ρ a R m2 rK c1 c2 : ℝ), 0 < ρ → a < 2 * ρ → 0 ≤ rK → rK < ρ → 0 ≤ R →
        (m2 - rK) ^ 2 ≤ R ^ 2 → (m2 + rK) ^ 2 ≤ R ^ 2 →
        (∀ p : ℝ × ℝ, (p.1 - c1) ^ 2 + (p.2 - c2) ^ 2 ≤ ρ ^ 2 →
          p.1 ^ 2 + (p.2 - m2) ^ 2 ≤ rK ^ 2 ∨ (0 ≤ p.1 ∧ p.1 ^ 2 + p.2 ^ 2 ≤ R ^ 2)) →
        ρ + √(ρ ^ 2 - a ^ 2 / 4) ≤ R) := by
  intro h
  obtain ⟨h0, h1, h2, h3⟩ := witness_lower 1 (9 / 10) one_pos (by norm_num) (by norm_num)
  have := h 1 1 _ 0 (9 / 10) _ 0 one_pos (by norm_num) (by norm_num) (by norm_num) h0 h1 h2 h3
  have hlt : √((1 : ℝ) ^ 2 - (9 / 10) ^ 2) < √(1 ^ 2 - 1 ^ 2 / 4) :=
    Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  linarith

/-- **Observacao apos `prop:teardrop_lower`**: para `a ∈ (0,2ρ)`,
`ρ + √(ρ² - a²/4) < r*(a)`. -/
theorem lower_lt_rstar {ρ a : ℝ} (hρ : 0 < ρ) (ha : 0 < a) (ha2 : a < 2 * ρ) :
    ρ + √(ρ ^ 2 - a ^ 2 / 4) < rstar ρ a := by
  rw [rstar_eq]
  unfold rstar'
  set u := a / (2 * ρ) with hu
  have hu1 : u < 1 := by rw [hu, div_lt_one (by positivity)]; exact ha2
  have hu0 : 0 < u := by positivity
  have ha' : a = 2 * ρ * u := by rw [hu]; field_simp
  have h1 : √(ρ ^ 2 - a ^ 2 / 4) = ρ * √(1 - u ^ 2) := by
    rw [ha', show ρ ^ 2 - (2 * ρ * u) ^ 2 / 4 = ρ ^ 2 * (1 - u ^ 2) by ring,
      sqrt_mul (by positivity), sqrt_sq hρ.le]
  rw [h1]
  have h2 : √(1 - u ^ 2) < √(4 - (1 + u) ^ 2) := Real.sqrt_lt_sqrt (by nlinarith) (by nlinarith)
  nlinarith

/-- Na ponta `a = 2ρ` as duas cotas coincidem (`= ρ`): a desigualdade estrita exige `a < 2ρ`. -/
theorem lower_eq_rstar_at_two_rho {ρ : ℝ} (hρ : 0 < ρ) :
    ρ + √(ρ ^ 2 - (2 * ρ) ^ 2 / 4) = ρ ∧ rstar' ρ (2 * ρ) = ρ := by
  constructor
  · rw [show ρ ^ 2 - (2 * ρ) ^ 2 / 4 = 0 by ring, sqrt_zero, add_zero]
  · unfold rstar'
    rw [show 4 - (1 + 2 * ρ / (2 * ρ)) ^ 2 = 0 by field_simp; norm_num, sqrt_zero]; ring

/-- Mutante: a desigualdade estrita em `a ∈ (0, 2ρ]` (intervalo fechado). Falso em `a = 2ρ`. -/
theorem mutant_gap_closed_false :
    ¬ (∀ ρ a : ℝ, 0 < ρ → 0 < a → a ≤ 2 * ρ → ρ + √(ρ ^ 2 - a ^ 2 / 4) < rstar' ρ a) := by
  intro h
  have := h 1 2 one_pos two_pos (by norm_num)
  have e := lower_eq_rstar_at_two_rho (ρ := 1) one_pos
  rw [show (2 : ℝ) = 2 * 1 by norm_num] at this
  rw [e.1, e.2] at this
  exact lt_irrefl _ this

/-- Os limites citados no livro: quando `a → 0⁺`, as cotas tendem a `2ρ` e `(1 + √3)ρ`;
quando `a → 2ρ`, ambas tendem a `ρ` (a lacuna fecha). -/
theorem limits (ρ : ℝ) (hρ : 0 < ρ) :
    Tendsto (fun a => ρ + √(ρ ^ 2 - a ^ 2 / 4)) (𝓝[>] 0) (𝓝 (2 * ρ)) ∧
    Tendsto (rstar' ρ) (𝓝[>] 0) (𝓝 ((1 + √3) * ρ)) ∧
    Tendsto (fun a => ρ + √(ρ ^ 2 - a ^ 2 / 4)) (𝓝[<] (2 * ρ)) (𝓝 ρ) ∧
    Tendsto (rstar' ρ) (𝓝[<] (2 * ρ)) (𝓝 ρ) := by
  have c1 : Continuous (fun a : ℝ => ρ + √(ρ ^ 2 - a ^ 2 / 4)) := by fun_prop
  have c2 : Continuous (rstar' ρ) := by unfold rstar'; fun_prop
  have hρ0 : ρ ≠ 0 := hρ.ne'
  refine ⟨?_, ?_, ?_, ?_⟩
  · have := (c1.tendsto 0).mono_left (nhdsWithin_le_nhds (s := Ioi 0))
    convert this using 2
    rw [show ρ ^ 2 - (0 : ℝ) ^ 2 / 4 = ρ ^ 2 by ring, sqrt_sq hρ.le]; ring
  · have := (c2.tendsto 0).mono_left (nhdsWithin_le_nhds (s := Ioi 0))
    convert this using 2
    unfold rstar'
    rw [show 4 - (1 + 0 / (2 * ρ)) ^ 2 = (3 : ℝ) by simp; norm_num]; ring
  · have := (c1.tendsto (2 * ρ)).mono_left (nhdsWithin_le_nhds (s := Iio (2 * ρ)))
    convert this using 2
    exact (lower_eq_rstar_at_two_rho hρ).1.symm
  · have := (c2.tendsto (2 * ρ)).mono_left (nhdsWithin_le_nhds (s := Iio (2 * ρ)))
    convert this using 2
    exact (lower_eq_rstar_at_two_rho hρ).2.symm

end LeanReal.Chap09Teardrop

#print axioms LeanReal.Chap09Teardrop.rstar_eq
#print axioms LeanReal.Chap09Teardrop.beta_mem
#print axioms LeanReal.Chap09Teardrop.junctions
#print axioms LeanReal.Chap09Teardrop.arcs_on_circles
#print axioms LeanReal.Chap09Teardrop.teardrop_i
#print axioms LeanReal.Chap09Teardrop.teardrop_embedded
#print axioms LeanReal.Chap09Teardrop.teardrop_avoids_K
#print axioms LeanReal.Chap09Teardrop.fam_hasDerivAt
#print axioms LeanReal.Chap09Teardrop.fam_end
#print axioms LeanReal.Chap09Teardrop.family_shape
#print axioms LeanReal.Chap09Teardrop.family_lower
#print axioms LeanReal.Chap09Teardrop.family_eq
#print axioms LeanReal.Chap09Teardrop.teardrop_mem_family
#print axioms LeanReal.Chap09Teardrop.mutant_arc2_strict_false
#print axioms LeanReal.Chap09Teardrop.mutant_family_no_mouth_false
#print axioms LeanReal.Chap09Teardrop.mutant_family_strict_false
#print axioms LeanReal.Chap09Teardrop.teardrop_lower
#print axioms LeanReal.Chap09Teardrop.teardrop_lower'
#print axioms LeanReal.Chap09Teardrop.witness_lower
#print axioms LeanReal.Chap09Teardrop.witness_lower_sharp
#print axioms LeanReal.Chap09Teardrop.mutant_lower_strict_false
#print axioms LeanReal.Chap09Teardrop.mutant_lower_full_disc_false
#print axioms LeanReal.Chap09Teardrop.mutant_lower_no_rK_false
#print axioms LeanReal.Chap09Teardrop.lower_lt_rstar
#print axioms LeanReal.Chap09Teardrop.lower_eq_rstar_at_two_rho
#print axioms LeanReal.Chap09Teardrop.mutant_gap_closed_false
#print axioms LeanReal.Chap09Teardrop.limits
