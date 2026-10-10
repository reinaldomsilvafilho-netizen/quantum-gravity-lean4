import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Order.Interval.Set.Infinite
import LeanReal.Chap07Bounds

/-!
# Capitulo 7: controle com parede e principio de contato (lote B9 do `PLANO_LIVRO_B.md`)

Fonte: `unified_quantum_gravity_book/chap07_minimax_extrinsic_curvature_submanifolds.tex`.

* `lem:wall_structure`, itens (c) e (d) (o minimizador de `P_W^T`).
* `thm:obstacle_exclusion`, itens (1)-(2) para CURVAS (`k = 1`), e a conta do disco de raio
  `1/2` do mesmo enunciado.
* `prop:optimal_regularity`: so o nucleo "curvatura continua com valores em `{0, ±K̂}` e
  constante".

Nao se formaliza nenhuma conjectura (`conj:wall_contact`, `conj:saturated`).

## Reducoes declaradas

### `lem:wall_structure` (c)-(d)
* Trajetoria de `y' = θ`, `θ' = κ`, `κ' = u`, `|u| ≤ 1` (o caso `f(θ) = θ`, `B = 1`): a
  estrutura `WallTraj` pede `y`, `θ` continuas em `[0,T]`, `y' = θ` e `θ' = κ` em `(0,T)`
  (derivadas classicas) e `κ` 1-Lipschitz em `[0,T]`. Isto equivale a `κ = κ₀ + ∫u` com
  `|u| ≤ 1` q.t.p.; o controle mensuravel `u` nao aparece.
* O item (b) do lema (o estado que se anula fica na origem) usa a MINIMALIDADE e entra como
  hipotese explicita `hB`. A existencia e unicidade (item (a)) nao sao formalizadas.
* `t*` e `Z` sao definidos como no livro (`tStar`, `contactSet`).
* A conclusao "Z e finito ou uma sequencia crescente que converge a `t*`" (reformulacao
  final de (d)) nao e formalizada; formaliza-se a finitude de `Z ∩ [0, t* - ε]`.

### `thm:obstacle_exclusion` (1)-(2), `k = 1`
* `E` espaco com produto interno real. A distancia com sinal `d` entra com gradiente `gd`
  perto de `p₀`, `gd` diferenciavel em `p₀` com derivada `H`, `gd p₀ = ν` e
  `⟪H w, w⟫ = -h(w,w)` para `w ⊥ ν`. Estes fatos (Gilbarg-Trudinger, Lemma 14.16) sao
  HIPOTESES, nao derivados.
* A curva `α` e duas vezes diferenciavel em `0` com `α(0) = p₀`, `α'(0) = v`, `α''(0) = a`;
  `II_M(v,v)` e a componente normal `a - ⟪a,v⟫ v` (para `‖v‖ = 1`). "Courant-Fischer" para
  `k = 1` e a hipotese `hlam`: `lam` e cota inferior de `h` nos vetores unitarios tangentes.
* O item (4) (`C^{1,1}`) e `k ≥ 2` nao sao cobertos.

### A conta do disco
* Curva por comprimento de arco `(X, Y)` com angulo `φ` DIFERENCIAVEL e `|φ'| ≤ 1/2` em todo
  ponto de `(0, ℓ)` (o livro: q.t.p.). Prova-se que a curva entra no disco aberto de raio
  `1/2`; o argumento de continuacao ("e grafico enquanto `cos φ > 0`") e provado, nao
  suposto.

### `prop:optimal_regularity`
* So o nucleo: `κ` continua em `[0,L]` com valores em `{0, K, -K}` e constante. O teorema
  de Dubins (minimizador = caminho de Dubins, curvatura em `{0, ±K̂}`) entra como hipotese.
-/

noncomputable section

namespace LeanReal.Chap07Control

open Set Filter Topology Real

/-! ## Comparacao por derivadas (auxiliares) -/

/-- Comparacao para a direita: `|f(a)| ≤ b(a)` e `|f'| ≤ b'` em `(a,c)` dao `|f(c)| ≤ b(c)`. -/
theorem abs_le_of_deriv_right {f f' b b' : ℝ → ℝ} {a c : ℝ} (hac : a ≤ c)
    (hfc : ContinuousOn f (Icc a c)) (hbc : ContinuousOn b (Icc a c))
    (hf : ∀ x ∈ Ioo a c, HasDerivAt f (f' x) x) (hb : ∀ x ∈ Ioo a c, HasDerivAt b (b' x) x)
    (h0 : |f a| ≤ b a) (hd : ∀ x ∈ Ioo a c, |f' x| ≤ b' x) : |f c| ≤ b c := by
  have ha : a ∈ Icc a c := ⟨le_rfl, hac⟩
  have hc : c ∈ Icc a c := ⟨hac, le_rfl⟩
  have m1 : MonotoneOn (fun x => b x - f x) (Icc a c) := by
    refine monotoneOn_of_hasDerivWithinAt_nonneg (f' := fun x => b' x - f' x) (convex_Icc a c)
      (hbc.sub hfc) ?_ ?_
    · intro x hx
      rw [interior_Icc] at hx ⊢
      exact ((hb x hx).sub (hf x hx)).hasDerivWithinAt
    · intro x hx
      rw [interior_Icc] at hx
      have := hd x hx
      have := le_abs_self (f' x)
      show 0 ≤ b' x - f' x
      linarith
  have m2 : MonotoneOn (fun x => b x + f x) (Icc a c) := by
    refine monotoneOn_of_hasDerivWithinAt_nonneg (f' := fun x => b' x + f' x) (convex_Icc a c)
      (hbc.add hfc) ?_ ?_
    · intro x hx
      rw [interior_Icc] at hx ⊢
      exact ((hb x hx).add (hf x hx)).hasDerivWithinAt
    · intro x hx
      rw [interior_Icc] at hx
      have := hd x hx
      have := neg_abs_le (f' x)
      show 0 ≤ b' x + f' x
      linarith
  have e1 := m1 ha hc hac
  have e2 := m2 ha hc hac
  have := abs_le.mp h0
  simp only at e1 e2
  exact abs_le.mpr ⟨by linarith, by linarith⟩

/-- Comparacao para a esquerda: `|f(c)| ≤ b(c)` e `|f'| ≤ -b'` em `(a,c)` dao `|f(a)| ≤ b(a)`. -/
theorem abs_le_of_deriv_left {f f' b b' : ℝ → ℝ} {a c : ℝ} (hac : a ≤ c)
    (hfc : ContinuousOn f (Icc a c)) (hbc : ContinuousOn b (Icc a c))
    (hf : ∀ x ∈ Ioo a c, HasDerivAt f (f' x) x) (hb : ∀ x ∈ Ioo a c, HasDerivAt b (b' x) x)
    (h0 : |f c| ≤ b c) (hd : ∀ x ∈ Ioo a c, |f' x| ≤ -b' x) : |f a| ≤ b a := by
  have ha : a ∈ Icc a c := ⟨le_rfl, hac⟩
  have hc : c ∈ Icc a c := ⟨hac, le_rfl⟩
  have m1 : AntitoneOn (fun x => b x - f x) (Icc a c) := by
    refine antitoneOn_of_hasDerivWithinAt_nonpos (f' := fun x => b' x - f' x) (convex_Icc a c)
      (hbc.sub hfc) ?_ ?_
    · intro x hx
      rw [interior_Icc] at hx ⊢
      exact ((hb x hx).sub (hf x hx)).hasDerivWithinAt
    · intro x hx
      rw [interior_Icc] at hx
      have := hd x hx
      have := neg_abs_le (f' x)
      show b' x - f' x ≤ 0
      linarith
  have m2 : AntitoneOn (fun x => b x + f x) (Icc a c) := by
    refine antitoneOn_of_hasDerivWithinAt_nonpos (f' := fun x => b' x + f' x) (convex_Icc a c)
      (hbc.add hfc) ?_ ?_
    · intro x hx
      rw [interior_Icc] at hx ⊢
      exact ((hb x hx).add (hf x hx)).hasDerivWithinAt
    · intro x hx
      rw [interior_Icc] at hx
      have := hd x hx
      have := le_abs_self (f' x)
      show b' x + f' x ≤ 0
      linarith
  have e1 := m1 ha hc hac
  have e2 := m2 ha hc hac
  have := abs_le.mp h0
  simp only at e1 e2
  exact abs_le.mpr ⟨by linarith, by linarith⟩

/-- Derivada de `(x - t)^2`. -/
theorem hasDerivAt_sq_sub (t r : ℝ) : HasDerivAt (fun x => (x - t) ^ 2) (2 * (r - t)) r := by
  simpa using ((hasDerivAt_id' r).sub_const t).fun_pow 2

/-- Derivada de `(x - t)^3`. -/
theorem hasDerivAt_cube_sub (t r : ℝ) :
    HasDerivAt (fun x => (x - t) ^ 3) (3 * (r - t) ^ 2) r := by
  simpa using ((hasDerivAt_id' r).sub_const t).fun_pow 3

/-! ## `lem:wall_structure`: trajetorias e a estimativa de Taylor -/

/-- Trajetoria do sistema `y' = θ`, `θ' = κ`, `κ' = u`, `|u| ≤ 1` em `[0,T]`
(`def:wall_problems`, `f(θ) = θ`, `B = 1`): `κ` 1-Lipschitz equivale a `κ' = u` com
`|u| ≤ 1` q.t.p. -/
structure WallTraj (T : ℝ) (y θ κ : ℝ → ℝ) : Prop where
  cont_y : ContinuousOn y (Icc 0 T)
  cont_θ : ContinuousOn θ (Icc 0 T)
  lip_κ : LipschitzOnWith 1 κ (Icc 0 T)
  deriv_y : ∀ s ∈ Ioo 0 T, HasDerivAt y (θ s) s
  deriv_θ : ∀ s ∈ Ioo 0 T, HasDerivAt θ (κ s) s

variable {T : ℝ} {y θ κ : ℝ → ℝ}

/-- `|κ(r) - κ(t)| ≤ |r - t|` (isto e `|u| ≤ 1`). -/
theorem WallTraj.abs_κ_sub (h : WallTraj T y θ κ) {r t : ℝ} (hr : r ∈ Icc 0 T)
    (ht : t ∈ Icc 0 T) : |κ r - κ t| ≤ |r - t| := by
  have := h.lip_κ.dist_le_mul r hr t ht
  simpa [Real.dist_eq] using this

/-- Taylor de ordem 1 para `θ`, a direita. -/
theorem WallTraj.taylor1_right (h : WallTraj T y θ κ) {t s : ℝ} (ht : 0 ≤ t) (hts : t ≤ s)
    (hs : s ≤ T) : |θ s - θ t - κ t * (s - t)| ≤ (s - t) ^ 2 / 2 := by
  have hsub : Icc t s ⊆ Icc 0 T := Icc_subset_Icc ht hs
  refine abs_le_of_deriv_right (f := fun r => θ r - θ t - κ t * (r - t))
    (f' := fun r => κ r - κ t) (b := fun r => (r - t) ^ 2 / 2) (b' := fun r => r - t) hts
    ?_ ?_ ?_ ?_ ?_ ?_
  · exact ((h.cont_θ.mono hsub).sub continuousOn_const).sub
      (continuousOn_const.mul (continuousOn_id.sub continuousOn_const))
  · exact ((continuousOn_id.sub continuousOn_const).pow 2).div_const 2
  · intro r hr
    have hr' : r ∈ Ioo 0 T := ⟨lt_of_le_of_lt ht hr.1, lt_of_lt_of_le hr.2 hs⟩
    have := ((h.deriv_θ r hr').sub_const (θ t)).sub
      (((hasDerivAt_id' r).sub_const t).const_mul (κ t))
    convert this using 1
    ring
  · intro r _
    have := (hasDerivAt_sq_sub t r).div_const 2
    convert this using 1
    ring
  · simp
  · intro r hr
    have := h.abs_κ_sub (hsub ⟨hr.1.le, hr.2.le⟩) (hsub ⟨le_rfl, hts⟩)
    rwa [abs_of_pos (sub_pos.mpr hr.1)] at this

/-- Taylor de ordem 1 para `θ`, a esquerda. -/
theorem WallTraj.taylor1_left (h : WallTraj T y θ κ) {t s : ℝ} (hs : 0 ≤ s) (hst : s ≤ t)
    (ht : t ≤ T) : |θ s - θ t - κ t * (s - t)| ≤ (s - t) ^ 2 / 2 := by
  have hsub : Icc s t ⊆ Icc 0 T := Icc_subset_Icc hs ht
  refine abs_le_of_deriv_left (f := fun r => θ r - θ t - κ t * (r - t))
    (f' := fun r => κ r - κ t) (b := fun r => (r - t) ^ 2 / 2) (b' := fun r => r - t) hst
    ?_ ?_ ?_ ?_ ?_ ?_
  · exact ((h.cont_θ.mono hsub).sub continuousOn_const).sub
      (continuousOn_const.mul (continuousOn_id.sub continuousOn_const))
  · exact ((continuousOn_id.sub continuousOn_const).pow 2).div_const 2
  · intro r hr
    have hr' : r ∈ Ioo 0 T := ⟨lt_of_le_of_lt hs hr.1, lt_of_lt_of_le hr.2 ht⟩
    have := ((h.deriv_θ r hr').sub_const (θ t)).sub
      (((hasDerivAt_id' r).sub_const t).const_mul (κ t))
    convert this using 1
    ring
  · intro r _
    have := (hasDerivAt_sq_sub t r).div_const 2
    convert this using 1
    ring
  · simp
  · intro r hr
    have := h.abs_κ_sub (hsub ⟨hr.1.le, hr.2.le⟩) (hsub ⟨hst, le_rfl⟩)
    rw [abs_of_neg (sub_neg.mpr hr.2)] at this
    linarith

/-- Taylor de ordem 2 para `y`, a direita: `|y(s) - y(t) - θ(t)(s-t) - κ(t)(s-t)²/2| ≤ (s-t)³/6`. -/
theorem WallTraj.taylor_right (h : WallTraj T y θ κ) {t s : ℝ} (ht : 0 ≤ t) (hts : t ≤ s)
    (hs : s ≤ T) :
    |y s - y t - θ t * (s - t) - κ t * (s - t) ^ 2 / 2| ≤ (s - t) ^ 3 / 6 := by
  have hsub : Icc t s ⊆ Icc 0 T := Icc_subset_Icc ht hs
  refine abs_le_of_deriv_right
    (f := fun r => y r - y t - θ t * (r - t) - κ t * (r - t) ^ 2 / 2)
    (f' := fun r => θ r - θ t - κ t * (r - t)) (b := fun r => (r - t) ^ 3 / 6)
    (b' := fun r => (r - t) ^ 2 / 2) hts ?_ ?_ ?_ ?_ ?_ ?_
  · exact (((h.cont_y.mono hsub).sub continuousOn_const).sub
      (continuousOn_const.mul (continuousOn_id.sub continuousOn_const))).sub
      ((continuousOn_const.mul ((continuousOn_id.sub continuousOn_const).pow 2)).div_const 2)
  · exact ((continuousOn_id.sub continuousOn_const).pow 3).div_const 6
  · intro r hr
    have hr' : r ∈ Ioo 0 T := ⟨lt_of_le_of_lt ht hr.1, lt_of_lt_of_le hr.2 hs⟩
    have := (((h.deriv_y r hr').sub_const (y t)).sub
      (((hasDerivAt_id' r).sub_const t).const_mul (θ t))).sub
      (((hasDerivAt_sq_sub t r).const_mul (κ t)).div_const 2)
    convert this using 1
    ring
  · intro r _
    have := (hasDerivAt_cube_sub t r).div_const 6
    convert this using 1
    ring
  · simp
  · intro r hr
    exact h.taylor1_right ht hr.1.le (hr.2.le.trans hs)

/-- Taylor de ordem 2 para `y`, a esquerda. -/
theorem WallTraj.taylor_left (h : WallTraj T y θ κ) {t s : ℝ} (hs : 0 ≤ s) (hst : s ≤ t)
    (ht : t ≤ T) :
    |y s - y t - θ t * (s - t) - κ t * (s - t) ^ 2 / 2| ≤ -(s - t) ^ 3 / 6 := by
  have hsub : Icc s t ⊆ Icc 0 T := Icc_subset_Icc hs ht
  refine abs_le_of_deriv_left
    (f := fun r => y r - y t - θ t * (r - t) - κ t * (r - t) ^ 2 / 2)
    (f' := fun r => θ r - θ t - κ t * (r - t)) (b := fun r => -(r - t) ^ 3 / 6)
    (b' := fun r => -((r - t) ^ 2 / 2)) hst ?_ ?_ ?_ ?_ ?_ ?_
  · exact (((h.cont_y.mono hsub).sub continuousOn_const).sub
      (continuousOn_const.mul (continuousOn_id.sub continuousOn_const))).sub
      ((continuousOn_const.mul ((continuousOn_id.sub continuousOn_const).pow 2)).div_const 2)
  · exact (((continuousOn_id.sub continuousOn_const).pow 3).neg).div_const 6
  · intro r hr
    have hr' : r ∈ Ioo 0 T := ⟨lt_of_le_of_lt hs hr.1, lt_of_lt_of_le hr.2 ht⟩
    have := (((h.deriv_y r hr').sub_const (y t)).sub
      (((hasDerivAt_id' r).sub_const t).const_mul (θ t))).sub
      (((hasDerivAt_sq_sub t r).const_mul (κ t)).div_const 2)
    convert this using 1
    ring
  · intro r _
    have := ((hasDerivAt_cube_sub t r).neg).div_const 6
    convert this using 1
    ring
  · simp
  · intro r hr
    have := h.taylor1_left (hs.trans hr.1.le) hr.2.le ht
    simpa using this

/-- **Estimativa de Taylor de `lem:wall_structure`(d)**, forma geral:
`|y(s) - y(t) - θ(t)(s-t) - κ(t)(s-t)²/2| ≤ |s-t|³/6` para `s, t ∈ [0,T]`. -/
theorem WallTraj.taylor (h : WallTraj T y θ κ) {t s : ℝ} (hs : s ∈ Icc 0 T)
    (ht : t ∈ Icc 0 T) :
    |y s - y t - θ t * (s - t) - κ t * (s - t) ^ 2 / 2| ≤ |s - t| ^ 3 / 6 := by
  rcases le_total t s with hts | hst
  · rw [abs_of_nonneg (sub_nonneg.mpr hts)]
    exact h.taylor_right ht.1 hts hs.2
  · rw [abs_of_nonpos (sub_nonpos.mpr hst)]
    have := h.taylor_left hs.1 hst ht.2
    have e : (-(s - t)) ^ 3 / 6 = -(s - t) ^ 3 / 6 := by ring
    rwa [e]

/-- **Forma do livro** (`lem:wall_structure`(d)): num ponto com `y(t) = θ(t) = 0`,
`|y(s) - κ(t)(s-t)²/2| ≤ |s-t|³/6`. -/
theorem WallTraj.taylor_contact (h : WallTraj T y θ κ) {t s : ℝ} (hs : s ∈ Icc 0 T)
    (ht : t ∈ Icc 0 T) (hy0 : y t = 0) (hθ0 : θ t = 0) :
    |y s - κ t * (s - t) ^ 2 / 2| ≤ |s - t| ^ 3 / 6 := by
  have := h.taylor hs ht
  rw [hy0, hθ0] at this
  simpa using this

/-! ## `lem:wall_structure`(d): sinal da curvatura e isolamento -/

/-- **`lem:wall_structure`(d), sinal**: num contato `y(t) = θ(t) = 0` com `t < T`, estado
nao nulo (`κ(t) ≠ 0`) e restricao `y ≥ 0`, vale `κ(t) > 0`. -/
theorem WallTraj.kappa_pos_of_contact (h : WallTraj T y θ κ)
    (hnn : ∀ s ∈ Icc 0 T, 0 ≤ y s) {t : ℝ} (ht0 : 0 ≤ t) (htT : t < T) (hy0 : y t = 0)
    (hθ0 : θ t = 0) (hκ0 : κ t ≠ 0) : 0 < κ t := by
  rcases lt_or_gt_of_ne hκ0 with hneg | hpos
  · exfalso
    set r := min (T - t) (-κ t) with hr
    have hr0 : 0 < r := lt_min (by linarith) (by linarith)
    have hrT : r ≤ T - t := min_le_left _ _
    have hrk : r ≤ -κ t := min_le_right _ _
    have hs : t + r ∈ Icc 0 T := ⟨by linarith, by linarith⟩
    have hT := h.taylor_contact hs ⟨ht0, htT.le⟩ hy0 hθ0
    have e : t + r - t = r := by ring
    rw [e, abs_of_pos hr0] at hT
    have hup := (abs_le.mp hT).2
    have hnnv := hnn _ hs
    have hprod : 0 < r ^ 2 * (-(3 * κ t + r)) := mul_pos (by positivity) (by linarith)
    nlinarith
  · exact hpos

/-- **`lem:wall_structure`(d), raio explicito**: num contato `y(t) = θ(t) = 0` com
`κ(t) > 0`, `y(s) > 0` para `0 < |s - t| < 3κ(t)`. -/
theorem WallTraj.pos_near_contact (h : WallTraj T y θ κ) {t : ℝ} (ht : t ∈ Icc 0 T)
    (hy0 : y t = 0) (hθ0 : θ t = 0) :
    ∀ s ∈ Icc 0 T, s ≠ t → |s - t| < 3 * κ t → 0 < y s := by
  intro s hs hst hd
  have hT := h.taylor_contact hs ht hy0 hθ0
  have ha : 0 < |s - t| := abs_pos.mpr (sub_ne_zero.mpr hst)
  have hsq : (s - t) ^ 2 = |s - t| ^ 2 := (sq_abs _).symm
  rw [hsq] at hT
  have hlow := (abs_le.mp hT).1
  have hprod : 0 < |s - t| ^ 2 * (3 * κ t - |s - t|) := mul_pos (by positivity) (by linarith)
  nlinarith

/-- **`lem:wall_structure`(d), isolamento**: um zero `t ∈ [0,T)` de `y ≥ 0` em que o estado
nao se anula e isolado (de fato `y > 0` num intervalo furado em torno de `t`). -/
theorem WallTraj.contact_isolated (h : WallTraj T y θ κ)
    (hnn : ∀ s ∈ Icc 0 T, 0 ≤ y s) {t : ℝ} (ht0 : 0 ≤ t) (htT : t < T) (hy0 : y t = 0)
    (hstate : ¬ (θ t = 0 ∧ κ t = 0)) :
    ∃ δ > 0, ∀ s ∈ Icc 0 T, s ≠ t → |s - t| < δ → 0 < y s := by
  by_cases hθ : θ t = 0
  · have hκ : κ t ≠ 0 := fun hk => hstate ⟨hθ, hk⟩
    have hk := h.kappa_pos_of_contact hnn ht0 htT hy0 hθ hκ
    exact ⟨3 * κ t, by linarith, h.pos_near_contact ⟨ht0, htT.le⟩ hy0 hθ⟩
  · have hθa : 0 < |θ t| := abs_pos.mpr hθ
    have hden : 0 < |κ t| + 1 := by positivity
    refine ⟨min 1 (|θ t| / (|κ t| + 1)), lt_min one_pos (div_pos hθa hden), ?_⟩
    intro s hs hst hd
    rcases (hnn s hs).lt_or_eq with hpos | hzero
    · exact hpos
    · exfalso
      set a := |s - t| with ha_def
      have ha : 0 < a := abs_pos.mpr (sub_ne_zero.mpr hst)
      have ha1 : a < 1 := lt_of_lt_of_le hd (min_le_left _ _)
      have haθ : a * (|κ t| + 1) < |θ t| := by
        have := lt_of_lt_of_le hd (min_le_right _ _)
        rwa [lt_div_iff₀ hden] at this
      have hT := h.taylor hs ⟨ht0, htT.le⟩
      rw [← hzero, hy0] at hT
      have e0 : (0 : ℝ) - 0 - θ t * (s - t) - κ t * (s - t) ^ 2 / 2
          = -(θ t * (s - t) + κ t * (s - t) ^ 2 / 2) := by ring
      rw [e0, abs_neg] at hT
      have e1 : |θ t * (s - t)| = |θ t| * a := abs_mul _ _
      have e2 : |κ t * (s - t) ^ 2 / 2| = |κ t| * a ^ 2 / 2 := by
        rw [abs_div, abs_mul, abs_pow, abs_two]
      have tri : |θ t * (s - t)| ≤ |θ t * (s - t) + κ t * (s - t) ^ 2 / 2|
          + |κ t * (s - t) ^ 2 / 2| := by
        have := abs_add_le (θ t * (s - t) + κ t * (s - t) ^ 2 / 2) (-(κ t * (s - t) ^ 2 / 2))
        rwa [abs_neg, add_neg_cancel_right] at this
      rw [e1, e2] at tri
      have h3 : a ^ 3 ≤ a ^ 2 := by nlinarith [mul_pos ha ha]
      have hm := mul_lt_mul_of_pos_left haθ ha
      nlinarith [abs_nonneg (κ t), mul_pos ha ha]

/-- **`lem:wall_structure`(d), contato interior**: um zero interior `t ∈ (0,T)` de `y ≥ 0`
tem `θ(t) = y'(t) = 0`. -/
theorem WallTraj.theta_zero_of_interior (h : WallTraj T y θ κ)
    (hnn : ∀ s ∈ Icc 0 T, 0 ≤ y s) {t : ℝ} (ht : t ∈ Ioo 0 T) (hy0 : y t = 0) : θ t = 0 := by
  have hmin : IsLocalMin y t :=
    Filter.eventually_of_mem (Icc_mem_nhds ht.1 ht.2) (fun s hs => by rw [hy0]; exact hnn s hs)
  exact hmin.hasDerivAt_eq_zero (h.deriv_y t ht)

/-- **`lem:wall_structure`(d), finitude**: se `c < T` e o estado nao se anula em nenhum zero
de `y` em `[0,c]`, entao `{t ∈ [0,c] : y(t) = 0}` e finito (compacto de pontos isolados). -/
theorem WallTraj.zero_set_finite (h : WallTraj T y θ κ) (hnn : ∀ s ∈ Icc 0 T, 0 ≤ y s)
    {c : ℝ} (hc : c < T) (hstate : ∀ t ∈ Icc 0 c, y t = 0 → ¬ (θ t = 0 ∧ κ t = 0)) :
    (Icc 0 c ∩ y ⁻¹' {0}).Finite := by
  by_contra hinf
  have hsub : Icc 0 c ∩ y ⁻¹' {0} ⊆ Icc 0 c := inter_subset_left
  obtain ⟨x, hx, hacc⟩ := Set.Infinite.exists_accPt_of_subset_isCompact hinf isCompact_Icc hsub
  have hclosed : IsClosed (Icc 0 c ∩ y ⁻¹' {0}) :=
    (h.cont_y.mono (Icc_subset_Icc le_rfl hc.le)).preimage_isClosed_of_isClosed isClosed_Icc
      isClosed_singleton
  have hfreq := accPt_iff_frequently.mp hacc
  have hxcl : x ∈ closure (Icc 0 c ∩ y ⁻¹' {0}) :=
    mem_closure_iff_frequently.mpr (hfreq.mono fun z hz => hz.2)
  rw [hclosed.closure_eq] at hxcl
  have hyx : y x = 0 := hxcl.2
  obtain ⟨δ, hδ, hiso⟩ := h.contact_isolated hnn hx.1 (lt_of_le_of_lt hx.2 hc) hyx
    (hstate x hx hyx)
  have hball : ∀ᶠ z in 𝓝 x, z ∈ Metric.ball x δ := Metric.ball_mem_nhds x hδ
  obtain ⟨z, ⟨hzx, hzS⟩, hzb⟩ := (hfreq.and_eventually hball).exists
  have hzT : z ∈ Icc 0 T := ⟨hzS.1.1, hzS.1.2.trans hc.le⟩
  have hdz : |z - x| < δ := by rw [← Real.dist_eq]; exact hzb
  have := hiso z hzT hzx hdz
  have hz0 : y z = 0 := hzS.2
  linarith

/-! ## `lem:wall_structure` (c)-(d) com `t*` e `Z` como no livro -/

/-- O estado `(y, θ, κ)` se anula em `t`. -/
def StateZero (y θ κ : ℝ → ℝ) (t : ℝ) : Prop := y t = 0 ∧ θ t = 0 ∧ κ t = 0

/-- Tempos `t ∈ [0,T]` a partir dos quais o estado fica na origem. -/
def restSet (T : ℝ) (y θ κ : ℝ → ℝ) : Set ℝ :=
  {t | t ∈ Icc 0 T ∧ ∀ s ∈ Icc t T, StateZero y θ κ s}

/-- Tempo de chegada `t* = min{t : estado ≡ 0 em [t,T]}` (`def:wall_problems`). -/
def tStar (T : ℝ) (y θ κ : ℝ → ℝ) : ℝ := sInf (restSet T y θ κ)

/-- Conjunto de contato `Z = {t ∈ [0,t*) : y(t) = 0}` (`def:wall_problems`). -/
def contactSet (T : ℝ) (y θ κ : ℝ → ℝ) : Set ℝ :=
  {t | t ∈ Icc 0 T ∧ t < tStar T y θ κ ∧ y t = 0}

theorem restSet_bddBelow : BddBelow (restSet T y θ κ) := ⟨0, fun _ ht => ht.1.1⟩

theorem T_mem_restSet (hT : 0 ≤ T) (hend : StateZero y θ κ T) : T ∈ restSet T y θ κ := by
  refine ⟨⟨hT, le_rfl⟩, fun s hs => ?_⟩
  have : s = T := le_antisymm hs.2 hs.1
  rw [this]; exact hend

theorem tStar_le (hT : 0 ≤ T) (hend : StateZero y θ κ T) : tStar T y θ κ ≤ T :=
  csInf_le restSet_bddBelow (T_mem_restSet hT hend)

/-- Com o item (b) do lema (`hB`), o estado nao se anula antes de `t*`. -/
theorem not_stateZero_of_lt_tStar
    (hB : ∀ τ ∈ Icc 0 T, StateZero y θ κ τ → ∀ s ∈ Icc τ T, StateZero y θ κ s)
    {t : ℝ} (ht : t ∈ Icc 0 T) (hlt : t < tStar T y θ κ) : ¬ StateZero y θ κ t := by
  intro hz
  have hmem : t ∈ restSet T y θ κ := ⟨ht, hB t ht hz⟩
  have := csInf_le restSet_bddBelow hmem
  unfold tStar at hlt
  linarith

/-- **`lem:wall_structure`(c)**: com o item (b) como hipotese `hB`, todo arco de fronteira
`[a,b]` (`a < b`, `y ≡ 0`) esta contido em `[t*, T]`. -/
theorem wall_structure_c (h : WallTraj T y θ κ)
    (hB : ∀ τ ∈ Icc 0 T, StateZero y θ κ τ → ∀ s ∈ Icc τ T, StateZero y θ κ s)
    {a b : ℝ} (hab : a < b) (h0a : 0 ≤ a) (hbT : b ≤ T) (harc : ∀ t ∈ Icc a b, y t = 0) :
    Icc a b ⊆ Icc (tStar T y θ κ) T := by
  have hsub : Icc a b ⊆ Icc 0 T := Icc_subset_Icc h0a hbT
  have hIoo : ∀ t ∈ Ioo a b, Ioo 0 T ∈ 𝓝 t ∧ Ioo a b ∈ 𝓝 t := fun t ht =>
    ⟨Ioo_mem_nhds (lt_of_le_of_lt h0a ht.1) (lt_of_lt_of_le ht.2 hbT), Ioo_mem_nhds ht.1 ht.2⟩
  -- θ = 0 em (a,b)
  have hθ0 : ∀ t ∈ Ioo a b, θ t = 0 := by
    intro t ht
    have hev : (fun _ : ℝ => (0 : ℝ)) =ᶠ[𝓝 t] y :=
      Filter.eventually_of_mem (hIoo t ht).2 fun s hs => (harc s ⟨hs.1.le, hs.2.le⟩).symm
    have hd0 : HasDerivAt y 0 t := (hasDerivAt_const t (0 : ℝ)).congr_of_eventuallyEq hev.symm
    exact (h.deriv_y t ⟨lt_of_le_of_lt h0a ht.1, lt_of_lt_of_le ht.2 hbT⟩).unique hd0
  -- κ = 0 em (a,b)
  have hκ0 : ∀ t ∈ Ioo a b, κ t = 0 := by
    intro t ht
    have hev : (fun _ : ℝ => (0 : ℝ)) =ᶠ[𝓝 t] θ :=
      Filter.eventually_of_mem (hIoo t ht).2 fun s hs => (hθ0 s hs).symm
    have hd0 : HasDerivAt θ 0 t := (hasDerivAt_const t (0 : ℝ)).congr_of_eventuallyEq hev.symm
    exact (h.deriv_θ t ⟨lt_of_le_of_lt h0a ht.1, lt_of_lt_of_le ht.2 hbT⟩).unique hd0
  -- extremos por continuidade
  have hcl : Icc a b ⊆ closure (Ioo a b) := by rw [closure_Ioo hab.ne]
  have hθI : EqOn θ (fun _ => (0 : ℝ)) (Icc a b) :=
    Set.EqOn.of_subset_closure (fun t ht => hθ0 t ht) (h.cont_θ.mono hsub) continuousOn_const
      Ioo_subset_Icc_self hcl
  have hκI : EqOn κ (fun _ => (0 : ℝ)) (Icc a b) :=
    Set.EqOn.of_subset_closure (fun t ht => hκ0 t ht) (h.lip_κ.continuousOn.mono hsub)
      continuousOn_const Ioo_subset_Icc_self hcl
  intro t ht
  have hz : StateZero y θ κ t := ⟨harc t ht, hθI ht, hκI ht⟩
  have hmem : t ∈ restSet T y θ κ := ⟨hsub ht, hB t (hsub ht) hz⟩
  exact ⟨csInf_le restSet_bddBelow hmem, (hsub ht).2⟩

/-- **`lem:wall_structure`(d)**, com o item (b) como hipotese `hB` e a condicao final
`estado(T) = 0`: (i) todo ponto de `Z` e isolado; (ii) `θ(t) = 0 < κ(t)` em `Z ∩ (0,t*)`;
(iii) `Z ∩ [0, t* - ε]` e finito para todo `ε > 0`. -/
theorem wall_structure_d (h : WallTraj T y θ κ) (hnn : ∀ s ∈ Icc 0 T, 0 ≤ y s)
    (hB : ∀ τ ∈ Icc 0 T, StateZero y θ κ τ → ∀ s ∈ Icc τ T, StateZero y θ κ s)
    (hT : 0 ≤ T) (hend : StateZero y θ κ T) :
    (∀ t ∈ contactSet T y θ κ, ∃ δ > 0, ∀ s ∈ Icc 0 T, s ≠ t → |s - t| < δ → 0 < y s) ∧
    (∀ t ∈ contactSet T y θ κ, 0 < t → θ t = 0 ∧ 0 < κ t) ∧
    (∀ ε > 0, (contactSet T y θ κ ∩ Icc 0 (tStar T y θ κ - ε)).Finite) := by
  have hle := tStar_le hT hend
  have hns : ∀ t ∈ Icc 0 T, t < tStar T y θ κ → y t = 0 → ¬ (θ t = 0 ∧ κ t = 0) :=
    fun t ht hlt hy hθκ => not_stateZero_of_lt_tStar hB ht hlt ⟨hy, hθκ⟩
  refine ⟨?_, ?_, ?_⟩
  · rintro t ⟨ht, hlt, hy⟩
    exact h.contact_isolated hnn ht.1 (lt_of_lt_of_le hlt hle) hy (hns t ht hlt hy)
  · rintro t ⟨ht, hlt, hy⟩ ht0
    have hθ := h.theta_zero_of_interior hnn ⟨ht0, lt_of_lt_of_le hlt hle⟩ hy
    have hκ : κ t ≠ 0 := fun hk => hns t ht hlt hy ⟨hθ, hk⟩
    exact ⟨hθ, h.kappa_pos_of_contact hnn ht.1 (lt_of_lt_of_le hlt hle) hy hθ hκ⟩
  · intro ε hε
    have hc : tStar T y θ κ - ε < T := by linarith
    have hfin := h.zero_set_finite hnn hc (fun t ht hy => by
      have htT : t ∈ Icc 0 T := ⟨ht.1, by linarith [ht.2]⟩
      exact hns t htT (by linarith [ht.2]) hy)
    refine hfin.subset ?_
    rintro t ⟨⟨_, _, hy⟩, ht2⟩
    exact ⟨ht2, hy⟩

/-! ### Testemunha A (item (d)): toque isolado em `t = 1`, chegada em `t* = T = 2`

`y = w³(1-w)²/150`, `w = 2 - t`, isto e `y = (t-1)²(2-t)³/150 ≥ 0`. Aqui `|y'''| ≤ 1`,
`y(1) = θ(1) = 0`, `κ(1) = 2/150 > 0`, e o estado so se anula em `t = 2`. -/

/-- Derivada de `(2 - x)^(n+1)`. -/
theorem hasDerivAt_w_pow (n : ℕ) (t : ℝ) :
    HasDerivAt (fun x => (2 - x) ^ (n + 1)) (-((n + 1) * (2 - t) ^ n)) t := by
  have := ((hasDerivAt_id' t).const_sub 2).fun_pow (n + 1)
  convert this using 1
  rw [Nat.add_sub_cancel]
  push_cast
  ring

/-- Altura da testemunha A. -/
def yA (t : ℝ) : ℝ := ((2 - t) ^ (2 + 1) - 2 * (2 - t) ^ (3 + 1) + (2 - t) ^ (4 + 1)) / 150

/-- Angulo da testemunha A (`= yA'`). -/
def θA (t : ℝ) : ℝ := -(3 * (2 - t) ^ 2 - 8 * (2 - t) ^ 3 + 5 * (2 - t) ^ 4) / 150

/-- Curvatura da testemunha A (`= θA'`). -/
def κA (t : ℝ) : ℝ := (6 * (2 - t) - 24 * (2 - t) ^ 2 + 20 * (2 - t) ^ 3) / 150

theorem yA_deriv (t : ℝ) : HasDerivAt yA (θA t) t := by
  have := (((hasDerivAt_w_pow 2 t).fun_sub ((hasDerivAt_w_pow 3 t).const_mul 2)).fun_add
    (hasDerivAt_w_pow 4 t)).div_const 150
  unfold yA
  convert this using 1
  simp only [θA]
  push_cast
  ring

theorem θA_deriv (t : ℝ) : HasDerivAt θA (κA t) t := by
  have := ((((hasDerivAt_w_pow 1 t).const_mul 3).fun_sub
    ((hasDerivAt_w_pow 2 t).const_mul 8)).fun_add
    ((hasDerivAt_w_pow 3 t).const_mul 5)).fun_neg.div_const 150
  have e : θA = fun x => -(3 * (2 - x) ^ (1 + 1) - 8 * (2 - x) ^ (2 + 1)
      + 5 * (2 - x) ^ (3 + 1)) / 150 := by
    funext x; simp only [θA]
  rw [e]
  convert this using 1
  simp only [κA]
  push_cast
  ring

theorem yA_eq (t : ℝ) : yA t = (t - 1) ^ 2 * (2 - t) ^ 3 / 150 := by
  simp only [yA]; ring

theorem κA_lip : LipschitzOnWith 1 κA (Icc 0 2) := by
  apply LipschitzOnWith.of_dist_le_mul
  intro s hs t ht
  simp only [Real.dist_eq, NNReal.coe_one, one_mul, κA]
  have key : (6 * (2 - s) - 24 * (2 - s) ^ 2 + 20 * (2 - s) ^ 3) / 150
      - (6 * (2 - t) - 24 * (2 - t) ^ 2 + 20 * (2 - t) ^ 3) / 150
      = (s - t) * (-(6 - 24 * ((2 - s) + (2 - t))
        + 20 * ((2 - s) ^ 2 + (2 - s) * (2 - t) + (2 - t) ^ 2)) / 150) := by ring
  rw [key, abs_mul]
  have ha0 : 0 ≤ 2 - s := by linarith [hs.2]
  have ha2 : 2 - s ≤ 2 := by linarith [hs.1]
  have hb0 : 0 ≤ 2 - t := by linarith [ht.2]
  have hb2 : 2 - t ≤ 2 := by linarith [ht.1]
  have hP : |(-(6 - 24 * ((2 - s) + (2 - t))
        + 20 * ((2 - s) ^ 2 + (2 - s) * (2 - t) + (2 - t) ^ 2)) / 150)| ≤ 1 := by
    rw [abs_le]
    constructor
    · nlinarith [mul_nonneg ha0 (sub_nonneg.mpr ha2), mul_nonneg hb0 (sub_nonneg.mpr hb2),
        sq_nonneg ((2 - s) - (2 - t))]
    · nlinarith [mul_nonneg ha0 hb0, sq_nonneg (2 - s), sq_nonneg (2 - t)]
  calc |s - t| * _ ≤ |s - t| * 1 := mul_le_mul_of_nonneg_left hP (abs_nonneg _)
    _ = |s - t| := mul_one _

theorem wallTraj_A : WallTraj 2 yA θA κA where
  cont_y := (continuous_iff_continuousAt.mpr fun t => (yA_deriv t).continuousAt).continuousOn
  cont_θ := (continuous_iff_continuousAt.mpr fun t => (θA_deriv t).continuousAt).continuousOn
  lip_κ := κA_lip
  deriv_y := fun s _ => yA_deriv s
  deriv_θ := fun s _ => θA_deriv s

theorem yA_nonneg : ∀ s ∈ Icc (0 : ℝ) 2, 0 ≤ yA s := by
  intro s hs
  rw [yA_eq]
  have : 0 ≤ 2 - s := by linarith [hs.2]
  positivity

theorem stateZero_A_iff {τ : ℝ} (hτ : τ ∈ Icc (0 : ℝ) 2) : StateZero yA θA κA τ ↔ τ = 2 := by
  constructor
  · rintro ⟨hy, -, hk⟩
    rw [yA_eq] at hy
    have : (τ - 1) ^ 2 * (2 - τ) ^ 3 = 0 := by linarith
    rcases mul_eq_zero.mp this with h1 | h2
    · have h1' : τ = 1 := by nlinarith [pow_eq_zero_iff (n := 2) (two_ne_zero) |>.mp h1]
      subst h1'
      norm_num [κA] at hk
    · have := pow_eq_zero_iff (n := 3) (by norm_num) |>.mp h2
      linarith
  · rintro rfl
    refine ⟨?_, ?_, ?_⟩ <;> norm_num [yA, θA, κA]

theorem hB_A : ∀ τ ∈ Icc (0 : ℝ) 2, StateZero yA θA κA τ → ∀ s ∈ Icc τ 2,
    StateZero yA θA κA s := by
  intro τ hτ hz s hs
  have h2 : τ = 2 := (stateZero_A_iff hτ).mp hz
  have hs2 : s = 2 := le_antisymm hs.2 (h2 ▸ hs.1)
  rw [hs2]
  exact (stateZero_A_iff ⟨by norm_num, le_rfl⟩).mpr rfl

theorem restSet_A : restSet 2 yA θA κA = {2} := by
  ext t
  constructor
  · rintro ⟨ht, hall⟩
    exact (stateZero_A_iff ht).mp (hall t ⟨le_rfl, ht.2⟩)
  · rintro rfl
    exact T_mem_restSet (by norm_num) ((stateZero_A_iff ⟨by norm_num, le_rfl⟩).mpr rfl)

theorem tStar_A : tStar 2 yA θA κA = 2 := by
  unfold tStar; rw [restSet_A, csInf_singleton]

/-- **Testemunha A**: todas as hipoteses de `wall_structure_d` valem, `Z` contem `t = 1`
(nao vazio), e o teorema da `θ(1) = 0 < κ(1)`. -/
theorem witness_A :
    WallTraj 2 yA θA κA ∧ (∀ s ∈ Icc (0 : ℝ) 2, 0 ≤ yA s) ∧
    StateZero yA θA κA 2 ∧ (1 : ℝ) ∈ contactSet 2 yA θA κA ∧ θA 1 = 0 ∧ 0 < κA 1 := by
  have hZ : (1 : ℝ) ∈ contactSet 2 yA θA κA := by
    refine ⟨⟨by norm_num, by norm_num⟩, ?_, by norm_num [yA]⟩
    rw [tStar_A]; norm_num
  have hd := (wall_structure_d wallTraj_A yA_nonneg hB_A (by norm_num)
    ((stateZero_A_iff ⟨by norm_num, le_rfl⟩).mpr rfl)).2.1 1 hZ one_pos
  exact ⟨wallTraj_A, yA_nonneg, (stateZero_A_iff ⟨by norm_num, le_rfl⟩).mpr rfl, hZ, hd⟩

/-! ### Testemunha B (item (c)): arco de fronteira `[1,2]`, `t* = 1`

`w = max(1 - t, 0)`, `y = w³/6`, `θ = -w²/2`, `κ = w`: estado inicial `(1/6, -1/2, 1) ≠ 0`,
repouso na origem em `[1,2]`. -/

/-- Colagem de derivadas em `c`: `f = p` em `(-∞, c]`, `f = q` em `[c, ∞)`, `p'(c) = q'(c)`. -/
theorem hasDerivAt_glue {f p q p' q' : ℝ → ℝ} {c : ℝ}
    (hp : ∀ x, HasDerivAt p (p' x) x) (hq : ∀ x, HasDerivAt q (q' x) x)
    (hfp : ∀ x ≤ c, f x = p x) (hfq : ∀ x, c ≤ x → f x = q x) (hd : p' c = q' c) (t : ℝ) :
    HasDerivAt f (if t ≤ c then p' t else q' t) t := by
  rcases lt_trichotomy t c with htc | rfl | htc
  · simp only [htc.le, ↓reduceIte]
    exact (hp t).congr_of_eventuallyEq
      (Filter.eventually_of_mem (Iio_mem_nhds htc) fun x hx => hfp x (le_of_lt hx))
  · simp only [le_refl, ↓reduceIte]
    have hL : HasDerivWithinAt f (p' t) (Iic t) t :=
      (hp t).hasDerivWithinAt.congr_of_mem (fun x hx => hfp x hx) self_mem_Iic
    have hR : HasDerivWithinAt f (p' t) (Ici t) t := by
      rw [hd]
      exact (hq t).hasDerivWithinAt.congr_of_mem (fun x hx => hfq x hx) self_mem_Ici
    have := hL.union hR
    rwa [Iic_union_Ici, hasDerivWithinAt_univ] at this
  · simp only [not_le.mpr htc, ↓reduceIte]
    exact (hq t).congr_of_eventuallyEq
      (Filter.eventually_of_mem (Ioi_mem_nhds htc) fun x hx => hfq x (le_of_lt hx))

/-- `w(t) = max(1 - t, 0)`. -/
def wB (t : ℝ) : ℝ := max (1 - t) 0

def yB (t : ℝ) : ℝ := wB t ^ 3 / 6
def θB (t : ℝ) : ℝ := -(wB t ^ 2 / 2)
def κB (t : ℝ) : ℝ := wB t

theorem wB_of_le {t : ℝ} (h : t ≤ 1) : wB t = 1 - t := max_eq_left (by linarith)
theorem wB_of_ge {t : ℝ} (h : 1 ≤ t) : wB t = 0 := max_eq_right (by linarith)

theorem yB_deriv (t : ℝ) : HasDerivAt yB (θB t) t := by
  have hp : ∀ x, HasDerivAt (fun x : ℝ => (1 - x) ^ 3 / 6) (-((1 - x) ^ 2 / 2)) x := by
    intro x
    have := (((hasDerivAt_id' x).const_sub 1).fun_pow 3).div_const 6
    convert this using 1
    norm_num
    ring
  have := hasDerivAt_glue (f := yB) (c := 1) hp (fun x => hasDerivAt_const x (0 : ℝ))
    (fun x hx => by simp only [yB, wB_of_le hx])
    (fun x hx => by simp only [yB, wB_of_ge hx]; norm_num) (by norm_num) t
  convert this using 1
  by_cases ht : t ≤ 1
  · simp only [ht, ↓reduceIte]; rw [θB, wB_of_le ht]
  · simp only [ht, ↓reduceIte]; rw [θB, wB_of_ge (le_of_lt (not_le.mp ht))]; norm_num

theorem θB_deriv (t : ℝ) : HasDerivAt θB (κB t) t := by
  have hp : ∀ x, HasDerivAt (fun x : ℝ => -((1 - x) ^ 2 / 2)) (1 - x) x := by
    intro x
    have := ((((hasDerivAt_id' x).const_sub 1).fun_pow 2).div_const 2).fun_neg
    convert this using 1
    norm_num
    ring
  have := hasDerivAt_glue (f := θB) (c := 1) hp (fun x => hasDerivAt_const x (0 : ℝ))
    (fun x hx => by simp only [θB, wB_of_le hx])
    (fun x hx => by simp only [θB, wB_of_ge hx]; norm_num) (by norm_num) t
  convert this using 1
  by_cases ht : t ≤ 1
  · simp only [ht, ↓reduceIte]; rw [κB, wB_of_le ht]
  · simp only [ht, ↓reduceIte]; rw [κB, wB_of_ge (le_of_lt (not_le.mp ht))]

theorem wallTraj_B : WallTraj 2 yB θB κB where
  cont_y := (continuous_iff_continuousAt.mpr fun t => (yB_deriv t).continuousAt).continuousOn
  cont_θ := (continuous_iff_continuousAt.mpr fun t => (θB_deriv t).continuousAt).continuousOn
  lip_κ := by
    apply LipschitzOnWith.of_dist_le_mul
    intro s _ t _
    simp only [Real.dist_eq, NNReal.coe_one, one_mul, κB, wB]
    have := abs_max_sub_max_le_abs (1 - s) (1 - t) 0
    have e : |1 - s - (1 - t)| = |s - t| := by rw [show 1 - s - (1 - t) = -(s - t) by ring, abs_neg]
    linarith
  deriv_y := fun s _ => yB_deriv s
  deriv_θ := fun s _ => θB_deriv s

theorem stateZero_B_iff (τ : ℝ) : StateZero yB θB κB τ ↔ 1 ≤ τ := by
  constructor
  · rintro ⟨-, -, hk⟩
    by_contra hlt
    rw [κB, wB_of_le (le_of_lt (not_le.mp hlt))] at hk
    linarith [not_le.mp hlt]
  · intro h1
    refine ⟨?_, ?_, ?_⟩ <;> simp [yB, θB, κB, wB_of_ge h1]

theorem hB_B : ∀ τ ∈ Icc (0 : ℝ) 2, StateZero yB θB κB τ → ∀ s ∈ Icc τ 2,
    StateZero yB θB κB s := by
  intro τ _ hz s hs
  exact (stateZero_B_iff s).mpr (le_trans ((stateZero_B_iff τ).mp hz) hs.1)

theorem restSet_B : restSet 2 yB θB κB = Icc 1 2 := by
  ext t
  constructor
  · rintro ⟨ht, hall⟩
    exact ⟨(stateZero_B_iff t).mp (hall t ⟨le_rfl, ht.2⟩), ht.2⟩
  · rintro ⟨h1, h2⟩
    exact ⟨⟨by linarith, h2⟩, fun s hs => (stateZero_B_iff s).mpr (h1.trans hs.1)⟩

theorem tStar_B : tStar 2 yB θB κB = 1 := by
  unfold tStar; rw [restSet_B, csInf_Icc (by norm_num)]

/-- **Testemunha B**: estado inicial nao nulo, `y ≡ 0` no arco `[1,2]` de comprimento
positivo, e o teorema coloca esse arco em `[t*, T] = [1, 2]`. -/
theorem witness_B :
    WallTraj 2 yB θB κB ∧ ¬ StateZero yB θB κB 0 ∧ (∀ t ∈ Icc (1 : ℝ) 2, yB t = 0) ∧
    tStar 2 yB θB κB = 1 ∧ Icc (1 : ℝ) 2 ⊆ Icc (tStar 2 yB θB κB) 2 := by
  have harc : ∀ t ∈ Icc (1 : ℝ) 2, yB t = 0 := fun t ht => by simp [yB, wB_of_ge ht.1]
  refine ⟨wallTraj_B, fun h0 => by linarith [(stateZero_B_iff 0).mp h0], harc, tStar_B,
    wall_structure_c wallTraj_B hB_B (by norm_num) (by norm_num) le_rfl harc⟩

/-! ### Mutantes de `lem:wall_structure` provados FALSOS -/

/-- Mutante 1: sem a restricao de estado `y ≥ 0`, o sinal `κ(t) > 0` falha
(`y = -t²/2`, `θ = -t`, `κ = -1`, `t = 0`). -/
theorem mutant_no_state_constraint_false :
    ¬ (∀ (T : ℝ) (y θ κ : ℝ → ℝ) (t : ℝ), WallTraj T y θ κ → 0 ≤ t → t < T → y t = 0 →
        θ t = 0 → κ t ≠ 0 → 0 < κ t) := by
  intro hm
  have hW : WallTraj 1 (fun t => -(t ^ 2 / 2)) (fun t => -t) (fun _ => -1) := {
    cont_y := by fun_prop
    cont_θ := by fun_prop
    lip_κ := (LipschitzWith.const (-1 : ℝ)).lipschitzOnWith.weaken (by norm_num)
    deriv_y := fun s _ => by
      have := ((hasDerivAt_id' s).fun_pow 2).div_const 2 |>.fun_neg
      convert this using 1; norm_num
    deriv_θ := fun s _ => by simpa using (hasDerivAt_id' s).fun_neg }
  have := hm 1 _ _ _ 0 hW le_rfl one_pos (by norm_num) (by norm_num) (by norm_num)
  norm_num at this

/-- Mutante 2: o raio `3κ(t)` de `pos_near_contact` e otimo; com `4κ(t)` o enunciado falha
(`y = s²/2 - s³/6` em `[0,3]`, `t = 0`, `κ(0) = 1`, `y(3) = 0`). -/
theorem mutant_radius_four_false :
    ¬ (∀ (T : ℝ) (y θ κ : ℝ → ℝ) (t : ℝ), WallTraj T y θ κ → (∀ s ∈ Icc 0 T, 0 ≤ y s) →
        t ∈ Icc 0 T → y t = 0 → θ t = 0 → 0 < κ t →
        ∀ s ∈ Icc 0 T, s ≠ t → |s - t| < 4 * κ t → 0 < y s) := by
  intro hm
  have hW : WallTraj 3 (fun s => s ^ 2 / 2 - s ^ 3 / 6) (fun s => s - s ^ 2 / 2)
      (fun s => 1 - s) := {
    cont_y := by fun_prop
    cont_θ := by fun_prop
    lip_κ := by
      apply LipschitzOnWith.of_dist_le_mul
      intro s _ t _
      simp only [Real.dist_eq, NNReal.coe_one, one_mul]
      rw [show 1 - s - (1 - t) = -(s - t) by ring, abs_neg]
    deriv_y := fun s _ => by
      have := (((hasDerivAt_id' s).fun_pow 2).div_const 2).fun_sub
        (((hasDerivAt_id' s).fun_pow 3).div_const 6)
      convert this using 1; norm_num; ring
    deriv_θ := fun s _ => by
      have := (hasDerivAt_id' s).fun_sub (((hasDerivAt_id' s).fun_pow 2).div_const 2)
      convert this using 1; norm_num }
  have hnn : ∀ s ∈ Icc (0 : ℝ) 3, 0 ≤ s ^ 2 / 2 - s ^ 3 / 6 := by
    intro s hs
    have : s ^ 2 / 2 - s ^ 3 / 6 = s ^ 2 * (3 - s) / 6 := by ring
    rw [this]
    have : 0 ≤ 3 - s := by linarith [hs.2]
    positivity
  have := hm 3 _ _ _ 0 hW hnn ⟨le_rfl, by norm_num⟩ (by norm_num) (by norm_num) (by norm_num)
    3 ⟨by norm_num, le_rfl⟩ (by norm_num) (by norm_num)
  norm_num at this

/-- Mutante 3 (finitude sem "estado nao nulo nos zeros"): falso, `y ≡ 0` em `[0,2]`. -/
theorem mutant_finite_without_state_false :
    ¬ (∀ (T : ℝ) (y θ κ : ℝ → ℝ) (c : ℝ), WallTraj T y θ κ → (∀ s ∈ Icc 0 T, 0 ≤ y s) →
        c < T → (Icc 0 c ∩ y ⁻¹' {0}).Finite) := by
  intro hm
  have hW : WallTraj 2 (fun _ => 0) (fun _ => 0) (fun _ => 0) := {
    cont_y := continuousOn_const
    cont_θ := continuousOn_const
    lip_κ := (LipschitzWith.const (0 : ℝ)).lipschitzOnWith.weaken (by norm_num)
    deriv_y := fun s _ => hasDerivAt_const s (0 : ℝ)
    deriv_θ := fun s _ => hasDerivAt_const s (0 : ℝ) }
  have hfin := hm 2 _ _ _ 1 hW (fun _ _ => le_rfl) (by norm_num)
  have heq : Icc (0 : ℝ) 1 ∩ (fun _ : ℝ => (0 : ℝ)) ⁻¹' {0} = Icc 0 1 := by
    ext t; simp
  rw [heq] at hfin
  exact Set.Icc_infinite (by norm_num : (0 : ℝ) < 1) hfin

/-- Mutante 4 (item (c) sem `a < b`): falso; na testemunha A o "arco" degenerado `[1,1]`
(o toque) nao esta em `[t*, T] = [2,2]`. -/
theorem mutant_arc_degenerate_false :
    ¬ (∀ (T : ℝ) (y θ κ : ℝ → ℝ) (a b : ℝ), WallTraj T y θ κ →
        (∀ τ ∈ Icc 0 T, StateZero y θ κ τ → ∀ s ∈ Icc τ T, StateZero y θ κ s) →
        a ≤ b → 0 ≤ a → b ≤ T → (∀ t ∈ Icc a b, y t = 0) → Icc a b ⊆ Icc (tStar T y θ κ) T) := by
  intro hm
  have := hm 2 yA θA κA 1 1 wallTraj_A hB_A le_rfl (by norm_num) (by norm_num)
    (fun t ht => by rw [le_antisymm ht.2 ht.1]; norm_num [yA])
  have h1 := (this ⟨le_rfl, le_rfl⟩).1
  rw [tStar_A] at h1
  norm_num at h1

/-! ## `thm:obstacle_exclusion` (1)-(2) para curvas -/

/-- Condicao necessaria de 2a ordem, forma local: minimo local de `φ`, `φ' = ψ` perto de
`t₀`, `ψ(t₀) = 0` e `ψ'(t₀) = d` dao `d ≥ 0`. (A versao global esta em `Chap07BallBound`.) -/
theorem second_order_min {φ ψ : ℝ → ℝ} {t₀ d : ℝ} (hmin : IsLocalMin φ t₀)
    (hφ : ∀ᶠ t in 𝓝 t₀, HasDerivAt φ (ψ t) t) (hψ : HasDerivAt ψ d t₀) (h0 : ψ t₀ = 0) :
    0 ≤ d := by
  by_contra hneg
  push Not at hneg
  have hsl : Tendsto (slope ψ t₀) (𝓝[>] t₀) (𝓝 d) :=
    (hasDerivAt_iff_tendsto_slope.mp hψ).mono_left
      (nhdsWithin_mono _ fun x hx => Set.mem_compl_singleton_iff.mpr (ne_of_gt hx))
  have hev : ∀ᶠ x in 𝓝[>] t₀, ψ x < 0 := by
    filter_upwards [hsl.eventually (gt_mem_nhds hneg), self_mem_nhdsWithin] with x hx hxt
    have hxt' : 0 < x - t₀ := sub_pos.mpr hxt
    rw [slope_def_field, h0, sub_zero] at hx
    by_contra hc
    push Not at hc
    have := div_nonneg hc hxt'.le
    linarith
  have hall : ∀ᶠ x in 𝓝[>] t₀, ψ x < 0 ∧ HasDerivAt φ (ψ x) x ∧ φ t₀ ≤ φ x :=
    hev.and ((hφ.filter_mono nhdsWithin_le_nhds).and (hmin.filter_mono nhdsWithin_le_nhds))
  obtain ⟨u, hu, hsub⟩ := mem_nhdsGT_iff_exists_Ioo_subset.mp hall
  have hu' : t₀ < u := hu
  set t₁ := (t₀ + u) / 2 with ht₁
  have h01 : t₀ < t₁ := by rw [ht₁]; linarith
  have h1u : t₁ < u := by rw [ht₁]; linarith
  have hanti : StrictAntiOn φ (Icc t₀ t₁) := by
    refine strictAntiOn_of_deriv_neg (convex_Icc _ _) ?_ ?_
    · intro x hx
      rcases eq_or_lt_of_le hx.1 with hxe | hlt
      · rw [← hxe]; exact hφ.self_of_nhds.continuousAt.continuousWithinAt
      · exact (hsub ⟨hlt, lt_of_le_of_lt hx.2 h1u⟩).2.1.continuousAt.continuousWithinAt
    · intro x hx
      rw [interior_Icc] at hx
      have hS := hsub ⟨hx.1, lt_trans hx.2 h1u⟩
      rw [hS.2.1.deriv]
      exact hS.1
  have hlt := hanti ⟨le_rfl, h01.le⟩ ⟨h01.le, le_rfl⟩ h01
  have hge := (hsub ⟨h01, h1u⟩).2.2
  linarith

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- **`thm:obstacle_exclusion`(1), `k = 1`**: se a curva `α` (com `α(0) = p₀`, `α'(0) = v`,
`α''(0) = a`) fica em `Ω̄ = {d ≥ 0}` perto de `0`, entao `v ∈ T_{p₀}∂Ω` (`⟪ν, v⟫ = 0`) e
`⟪ν, a⟫ ≥ h(v,v)`. Os fatos sobre a distancia com sinal (`∇d = gd`, `∇d(p₀) = ν`,
`∇²d(p₀) = -h` em `ν^⊥`) sao as hipoteses `hd`, `hgd`, `hν`, `hHess`. -/
theorem contact_principle_curve {d : E → ℝ} {gd : E → E} {H : E →L[ℝ] E} {p₀ ν v a : E}
    {hq : E → ℝ} {α α' : ℝ → E}
    (hd : ∀ᶠ x in 𝓝 p₀, HasFDerivAt d (innerSL ℝ (gd x)) x)
    (hgd : HasFDerivAt gd H p₀) (hν : gd p₀ = ν)
    (hHess : ∀ w, inner ℝ ν w = 0 → inner ℝ (H w) w = -hq w)
    (hd0 : d p₀ = 0) (hα0 : α 0 = p₀) (hα : ∀ᶠ t in 𝓝 (0 : ℝ), HasDerivAt α (α' t) t)
    (hα' : HasDerivAt α' a 0) (hv : α' 0 = v) (hin : ∀ᶠ t in 𝓝 (0 : ℝ), 0 ≤ d (α t)) :
    inner ℝ ν v = 0 ∧ hq v ≤ inner ℝ ν a := by
  have hαc : Tendsto α (𝓝 0) (𝓝 p₀) := by
    rw [← hα0]; exact hα.self_of_nhds.continuousAt.tendsto
  have hφ : ∀ᶠ t in 𝓝 (0 : ℝ), HasDerivAt (fun t => d (α t)) (inner ℝ (gd (α t)) (α' t)) t := by
    filter_upwards [hαc.eventually hd, hα] with t h1 h2
    have := h1.comp_hasDerivAt t h2
    rwa [innerSL_apply_apply] at this
  rw [← hα0] at hgd
  have hψ : HasDerivAt (fun t => inner ℝ (gd (α t)) (α' t))
      (inner ℝ (gd (α 0)) a + inner ℝ (H (α' 0)) (α' 0)) 0 :=
    (hgd.comp_hasDerivAt 0 hα.self_of_nhds).inner ℝ hα'
  have hmin : IsLocalMin (fun t => d (α t)) 0 := by
    filter_upwards [hin] with t ht
    simp only [hα0, hd0]
    exact ht
  have h1 : inner ℝ (gd (α 0)) (α' 0) = 0 := hmin.hasDerivAt_eq_zero hφ.self_of_nhds
  rw [hα0, hν, hv] at h1
  have h2 := second_order_min hmin hφ hψ (by rw [hα0, hν, hv]; exact h1)
  rw [hα0, hν, hv, hHess v h1] at h2
  exact ⟨h1, by linarith⟩

/-- A componente normal `a - ⟪a,v⟫v` tem o mesmo produto com `ν` que `a` quando `ν ⊥ v`. -/
theorem inner_normalPart {ν v a : E} (h : inner ℝ ν v = 0) :
    inner ℝ ν (a - inner ℝ a v • v) = inner ℝ ν a := by
  rw [inner_sub_right, inner_smul_right, h, mul_zero, sub_zero]

/-- **`thm:obstacle_exclusion`(2), `k = 1`**: com `‖ν‖ = ‖v‖ = 1` e `lam` cota inferior de `h`
nos vetores unitarios tangentes (`hlam`, Courant-Fischer para `k = 1`), a curvatura
`II(v,v) = a - ⟪a,v⟫v` satisfaz `‖II‖ ≥ max(0, lam)`. -/
theorem contact_curvature_bound {d : E → ℝ} {gd : E → E} {H : E →L[ℝ] E} {p₀ ν v a : E}
    {hq : E → ℝ} {α α' : ℝ → E} {lam : ℝ}
    (hd : ∀ᶠ x in 𝓝 p₀, HasFDerivAt d (innerSL ℝ (gd x)) x)
    (hgd : HasFDerivAt gd H p₀) (hν : gd p₀ = ν)
    (hHess : ∀ w, inner ℝ ν w = 0 → inner ℝ (H w) w = -hq w)
    (hd0 : d p₀ = 0) (hα0 : α 0 = p₀) (hα : ∀ᶠ t in 𝓝 (0 : ℝ), HasDerivAt α (α' t) t)
    (hα' : HasDerivAt α' a 0) (hv : α' 0 = v) (hin : ∀ᶠ t in 𝓝 (0 : ℝ), 0 ≤ d (α t))
    (hν1 : ‖ν‖ = 1) (hv1 : ‖v‖ = 1)
    (hlam : ∀ w, inner ℝ ν w = 0 → ‖w‖ = 1 → lam ≤ hq w) :
    max 0 lam ≤ ‖a - inner ℝ a v • v‖ := by
  obtain ⟨h1, h2⟩ := contact_principle_curve hd hgd hν hHess hd0 hα0 hα hα' hv hin
  have h3 := hlam v h1 hv1
  have h4 : inner ℝ ν (a - inner ℝ a v • v) ≤ ‖a - inner ℝ a v • v‖ := by
    have := real_inner_le_norm ν (a - inner ℝ a v • v)
    rwa [hν1, one_mul] at this
  rw [inner_normalPart h1] at h4
  exact max_le (norm_nonneg _) (by linarith)

/-! ### Testemunha: o circulo unitario dentro do disco unitario (igualdade)

`ℝ² = ℂ`. `Ω` = disco unitario, `d(x) = (1 - ‖x‖²)/2` (mesmo nivel zero, mesma normal e
mesma 2a forma em `p₀ = 1` que a distancia com sinal), `gd(x) = -x`, `H = -id`, `ν = -1`,
`h(w,w) = ‖w‖²` (raio `1`). A curva e o proprio circulo `e^{it}` de `Chap07Bounds`. -/

open LeanReal.Chap07Bounds in
/-- Distancia "com sinal" de segunda ordem para o disco unitario. -/
def dDisk (x : ℂ) : ℝ := (1 / 2) * (1 - ‖x‖ ^ 2)

theorem dDisk_hasFDerivAt (x : ℂ) : HasFDerivAt dDisk (innerSL ℝ (-x)) x := by
  have h0 : HasFDerivAt (fun y : ℂ => ‖y‖ ^ 2) (2 • innerSL ℝ x) x :=
    (hasStrictFDerivAt_norm_sq x).hasFDerivAt
  have h1 : HasFDerivAt (fun y : ℂ => 1 - ‖y‖ ^ 2) (-(2 • innerSL ℝ x)) x := h0.const_sub 1
  have h := h1.const_mul (1 / 2 : ℝ)
  unfold dDisk
  convert h using 1
  refine ContinuousLinearMap.ext fun w => ?_
  simp [two_smul]
  ring

theorem neg_hasFDerivAt (x : ℂ) :
    HasFDerivAt (fun z : ℂ => -z) (-ContinuousLinearMap.id ℝ ℂ) x :=
  (hasFDerivAt_id x).neg

open LeanReal.Chap07Bounds in
/-- **Testemunha do principio de contato**: o circulo unitario toca o bordo do disco unitario
em `p₀ = 1`; todas as hipoteses valem e as conclusoes (1)-(2) valem com IGUALDADE
(`⟪ν, a⟫ = h(v,v) = 1`, `‖II‖ = lam = 1`). -/
theorem witness_circle :
    inner ℝ (-1 : ℂ) (arcC' 0) = 0 ∧ ‖arcC' 0‖ ^ 2 ≤ inner ℝ (-1 : ℂ) (arcC'' 0) ∧
    inner ℝ (-1 : ℂ) (arcC'' 0) = 1 ∧ ‖arcC' 0‖ ^ 2 = 1 ∧
    max 0 1 ≤ ‖arcC'' 0 - inner ℝ (arcC'' 0) (arcC' 0) • arcC' 0‖ ∧
    ‖arcC'' 0 - inner ℝ (arcC'' 0) (arcC' 0) • arcC' 0‖ = 1 := by
  have hd : ∀ᶠ x in 𝓝 (1 : ℂ), HasFDerivAt dDisk (innerSL ℝ ((fun z : ℂ => -z) x)) x :=
    Filter.Eventually.of_forall dDisk_hasFDerivAt
  have hHess : ∀ w : ℂ, inner ℝ (-1 : ℂ) w = 0 →
      inner ℝ ((-ContinuousLinearMap.id ℝ ℂ) w) w = -(‖w‖ ^ 2) := by
    intro w _
    show inner ℝ (-w) w = -(‖w‖ ^ 2)
    rw [inner_neg_left, real_inner_self_eq_norm_sq]
  have hα0 : arcC 0 = 1 := by simp [arcC]
  have hin : ∀ᶠ t in 𝓝 (0 : ℝ), 0 ≤ dDisk (arcC t) :=
    Filter.Eventually.of_forall fun t => by simp [dDisk, norm_arcC]
  have hdd0 : dDisk 1 = 0 := by simp [dDisk]
  have hA := Filter.Eventually.of_forall (f := 𝓝 (0 : ℝ)) arcC_hasDerivAt
  obtain ⟨h1, h2⟩ := contact_principle_curve hd (neg_hasFDerivAt 1) rfl hHess hdd0 hα0 hA
    (arcC'_hasDerivAt 0) rfl hin
  have hv0 : arcC' 0 = Complex.I := by simp [arcC', arcC]
  have ha0 : arcC'' 0 = -1 := by simp [arcC'', arcC]
  have hII : arcC'' 0 - inner ℝ (arcC'' 0) (arcC' 0) • arcC' 0 = -1 := by
    rw [hv0, ha0]; simp [Complex.inner]
  have hlam : ∀ w : ℂ, inner ℝ (-1 : ℂ) w = 0 → ‖w‖ = 1 → (1 : ℝ) ≤ ‖w‖ ^ 2 := by
    intro w _ hw; rw [hw]; norm_num
  have h3 := contact_curvature_bound hd (neg_hasFDerivAt 1) rfl hHess hdd0 hα0 hA
    (arcC'_hasDerivAt 0) rfl hin (by simp) (by rw [hv0]; simp) hlam
  refine ⟨h1, h2, ?_, ?_, h3, ?_⟩
  · rw [ha0]; simp
  · rw [hv0]; simp
  · rw [hII]; simp

/-! ### Mutantes do principio de contato provados FALSOS -/

/-- A reta tangente `1 + t i` sai do disco unitario: `d(1 + t i) = -t²/2 < 0` para `t ≠ 0`. -/
theorem dDisk_tangent_line (t : ℝ) : dDisk (1 + t * Complex.I) = -(t ^ 2 / 2) := by
  have : ‖(1 : ℂ) + t * Complex.I‖ ^ 2 = 1 + t ^ 2 := by
    rw [Complex.sq_norm, Complex.normSq_apply]; simp; ring
  simp only [dDisk, this]; ring

theorem line_hasDerivAt (t : ℝ) :
    HasDerivAt (fun s : ℝ => (1 : ℂ) + s * Complex.I) Complex.I t := by
  have h : HasDerivAt (fun s : ℝ => (s : ℂ) * Complex.I) (1 * Complex.I) t :=
    (hasDerivAt_id t).ofReal_comp.mul_const Complex.I
  simpa using h.const_add 1

/-- Mutante 1 (sem `M ⊂ Ω̄`, isto e sem `hin`): falso. A reta tangente ao disco unitario em
`1` satisfaz as demais hipoteses, mas `⟪ν, a⟫ = 0 < 1 = h(v,v)`. -/
theorem mutant_no_inclusion_false :
    ¬ (∀ (α α' : ℝ → ℂ) (v a : ℂ), α 0 = 1 → (∀ᶠ t in 𝓝 (0 : ℝ), HasDerivAt α (α' t) t) →
        HasDerivAt α' a 0 → α' 0 = v → ‖v‖ ^ 2 ≤ inner ℝ (-1 : ℂ) a) := by
  intro hm
  have := hm (fun s => 1 + s * Complex.I) (fun _ => Complex.I) Complex.I 0 (by simp)
    (Filter.Eventually.of_forall line_hasDerivAt) (hasDerivAt_const 0 _) rfl
  norm_num at this

/-- Mutante 2 (`‖II‖ ≥ |lam|` em vez de `max(0, lam)`): falso. Exterior do disco unitario
(`d = (‖x‖² - 1)/2`, `ν = 1`, `h = -‖w‖²`, `lam = -1`): a reta tangente fica em `Ω̄` com
`II = 0 < 1 = |lam|` (observacao "Convex obstacles" do livro). -/
theorem mutant_abs_lambda_false :
    ¬ (∀ (d : ℂ → ℝ) (gd : ℂ → ℂ) (H : ℂ →L[ℝ] ℂ) (p₀ ν v a : ℂ) (hq : ℂ → ℝ)
        (α α' : ℝ → ℂ) (lam : ℝ),
        (∀ᶠ x in 𝓝 p₀, HasFDerivAt d (innerSL ℝ (gd x)) x) → HasFDerivAt gd H p₀ →
        gd p₀ = ν → (∀ w, inner ℝ ν w = 0 → inner ℝ (H w) w = -hq w) → d p₀ = 0 →
        α 0 = p₀ → (∀ᶠ t in 𝓝 (0 : ℝ), HasDerivAt α (α' t) t) → HasDerivAt α' a 0 →
        α' 0 = v → (∀ᶠ t in 𝓝 (0 : ℝ), 0 ≤ d (α t)) → ‖ν‖ = 1 → ‖v‖ = 1 →
        (∀ w, inner ℝ ν w = 0 → ‖w‖ = 1 → lam ≤ hq w) →
        |lam| ≤ ‖a - inner ℝ a v • v‖) := by
  intro hm
  have hd : ∀ᶠ x in 𝓝 (1 : ℂ), HasFDerivAt (fun x => -dDisk x) (innerSL ℝ (id x)) x :=
    Filter.Eventually.of_forall fun x => by
      have := (dDisk_hasFDerivAt x).neg
      convert this using 1
      refine ContinuousLinearMap.ext fun w => ?_
      simp
  have hHess : ∀ w : ℂ, inner ℝ (1 : ℂ) w = 0 →
      inner ℝ ((ContinuousLinearMap.id ℝ ℂ) w) w = -(-(‖w‖ ^ 2)) := by
    intro w _
    simp only [ContinuousLinearMap.id_apply, real_inner_self_eq_norm_sq, neg_neg]
  have hin : ∀ᶠ t : ℝ in 𝓝 (0 : ℝ), 0 ≤ -dDisk (1 + (t : ℂ) * Complex.I) :=
    Filter.Eventually.of_forall fun t => by rw [dDisk_tangent_line, neg_neg]; positivity
  have := hm (fun x => -dDisk x) id (ContinuousLinearMap.id ℝ ℂ) 1 1 Complex.I 0
    (fun w => -(‖w‖ ^ 2)) (fun s => 1 + s * Complex.I) (fun _ => Complex.I) (-1) hd
    (hasFDerivAt_id 1) rfl hHess (by simp [dDisk]) (by simp)
    (Filter.Eventually.of_forall line_hasDerivAt) (hasDerivAt_const 0 _) rfl hin (by simp)
    (by simp) (fun w _ hw => by rw [hw]; norm_num)
  norm_num at this

/-! ## A conta do disco de raio `1/2` (`thm:obstacle_exclusion`, paragrafo final)

`p = (-1,0)`, `q = (1,0)`, tangente inicial `(1,0)`, `|κ| ≤ 1/2`: a curva entra no disco
aberto de raio `1/2` centrado na origem; logo, com esse obstaculo, `κ* ≥ 1/2`. -/

/-- Fecho pela esquerda: `f ≤ c` em `[0,σ)` da `f(σ) ≤ c`. -/
theorem le_of_forall_Ico {f : ℝ → ℝ} {σ ℓ c : ℝ} (hσ : 0 < σ) (hσℓ : σ ≤ ℓ)
    (hf : ContinuousOn f (Icc 0 ℓ)) (h : ∀ s ∈ Ico 0 σ, f s ≤ c) : f σ ≤ c := by
  have hcl : σ ∈ closure (Ico 0 σ) := by
    rw [closure_Ico hσ.ne]; exact ⟨hσ.le, le_rfl⟩
  have hcw : ContinuousWithinAt f (Ico 0 σ) σ :=
    (hf σ ⟨hσ.le, hσℓ⟩).mono fun x hx => ⟨hx.1, hx.2.le.trans hσℓ⟩
  exact hcw.closure_le hcl continuousWithinAt_const h

section Disk

variable {X Y φ κ : ℝ → ℝ} {ℓ : ℝ}

/-- Enquanto `cos φ ≥ 0`, `|sin φ| ≤ (X + 1)/2` (de `|d(sin φ)/dx| = |κ| ≤ 1/2`). -/
theorem sin_bound (hX : ContinuousOn X (Icc 0 ℓ)) (hφ : ContinuousOn φ (Icc 0 ℓ))
    (hdX : ∀ s ∈ Ioo 0 ℓ, HasDerivAt X (cos (φ s)) s)
    (hdφ : ∀ s ∈ Ioo 0 ℓ, HasDerivAt φ (κ s) s) (hκ : ∀ s ∈ Ioo 0 ℓ, |κ s| ≤ 1 / 2)
    (hX0 : X 0 = -1) (hφ0 : φ 0 = 0) {τ : ℝ} (hτ : τ ∈ Icc 0 ℓ)
    (hcos : ∀ r ∈ Ioo 0 τ, 0 ≤ cos (φ r)) : |sin (φ τ)| ≤ (X τ + 1) / 2 := by
  have hsub : Icc 0 τ ⊆ Icc 0 ℓ := Icc_subset_Icc le_rfl hτ.2
  have hIoo : ∀ r ∈ Ioo 0 τ, r ∈ Ioo 0 ℓ := fun r hr => ⟨hr.1, lt_of_lt_of_le hr.2 hτ.2⟩
  have h0 : (0 : ℝ) ∈ Icc 0 τ := ⟨le_rfl, hτ.1⟩
  have hτ' : τ ∈ Icc 0 τ := ⟨hτ.1, le_rfl⟩
  have hc1 : ContinuousOn (fun r => sin (φ r)) (Icc 0 τ) :=
    continuous_sin.comp_continuousOn (hφ.mono hsub)
  have hc2 : ContinuousOn (fun r => (X r + 1) / 2) (Icc 0 τ) :=
    ((hX.mono hsub).add continuousOn_const).div_const 2
  have a1 : AntitoneOn (fun r => sin (φ r) - (X r + 1) / 2) (Icc 0 τ) := by
    refine antitoneOn_of_hasDerivWithinAt_nonpos
      (f' := fun r => cos (φ r) * κ r - cos (φ r) / 2) (convex_Icc 0 τ) (hc1.sub hc2) ?_ ?_
    · intro r hr
      rw [interior_Icc] at hr ⊢
      have := ((hdφ r (hIoo r hr)).sin).sub (((hdX r (hIoo r hr)).add_const 1).div_const 2)
      exact this.hasDerivWithinAt
    · intro r hr
      rw [interior_Icc] at hr
      have hk := (abs_le.mp (hκ r (hIoo r hr))).2
      have hc := hcos r hr
      show cos (φ r) * κ r - cos (φ r) / 2 ≤ 0
      nlinarith
  have a2 : AntitoneOn (fun r => -sin (φ r) - (X r + 1) / 2) (Icc 0 τ) := by
    refine antitoneOn_of_hasDerivWithinAt_nonpos
      (f' := fun r => -(cos (φ r) * κ r) - cos (φ r) / 2) (convex_Icc 0 τ) (hc1.neg.sub hc2) ?_ ?_
    · intro r hr
      rw [interior_Icc] at hr ⊢
      have := ((hdφ r (hIoo r hr)).sin).neg.sub
        (((hdX r (hIoo r hr)).add_const 1).div_const 2)
      exact this.hasDerivWithinAt
    · intro r hr
      rw [interior_Icc] at hr
      have hk := (abs_le.mp (hκ r (hIoo r hr))).1
      have hc := hcos r hr
      show -(cos (φ r) * κ r) - cos (φ r) / 2 ≤ 0
      nlinarith
  have e1 := a1 h0 hτ' hτ.1
  have e2 := a2 h0 hτ' hτ.1
  simp only [hX0, hφ0, sin_zero] at e1 e2
  exact abs_le.mpr ⟨by linarith, by linarith⟩

/-- **A conta do disco** (`thm:obstacle_exclusion`, paragrafo final): uma curva por
comprimento de arco de `(-1,0)`, com tangente inicial `(1,0)` e `|κ| ≤ 1/2`, que alcanca a
abscissa `1`, entra no disco aberto de raio `1/2` centrado na origem. -/
theorem disk_obstacle (hℓ : 0 ≤ ℓ)
    (hX : ContinuousOn X (Icc 0 ℓ)) (hY : ContinuousOn Y (Icc 0 ℓ))
    (hφ : ContinuousOn φ (Icc 0 ℓ))
    (hdX : ∀ s ∈ Ioo 0 ℓ, HasDerivAt X (cos (φ s)) s)
    (hdY : ∀ s ∈ Ioo 0 ℓ, HasDerivAt Y (sin (φ s)) s)
    (hdφ : ∀ s ∈ Ioo 0 ℓ, HasDerivAt φ (κ s) s) (hκ : ∀ s ∈ Ioo 0 ℓ, |κ s| ≤ 1 / 2)
    (hX0 : X 0 = -1) (hY0 : Y 0 = 0) (hφ0 : φ 0 = 0) (hXℓ : X ℓ = 1) :
    ∃ s ∈ Icc 0 ℓ, X s ^ 2 + Y s ^ 2 < (1 / 2) ^ 2 := by
  -- primeira passagem por `x = -1/4`
  set Sh := Icc 0 ℓ ∩ X ⁻¹' Ici (-1 / 4) with hSh
  have hShc : IsClosed Sh := hX.preimage_isClosed_of_isClosed isClosed_Icc isClosed_Ici
  have hShne : Sh.Nonempty := ⟨ℓ, ⟨hℓ, le_rfl⟩, show -1 / 4 ≤ X ℓ by rw [hXℓ]; norm_num⟩
  have hShb : BddBelow Sh := ⟨0, fun _ hs => hs.1.1⟩
  set s₀ := sInf Sh with hs₀
  have hs₀mem : s₀ ∈ Sh := hShc.csInf_mem hShne hShb
  have hs₀ℓ : s₀ ∈ Icc 0 ℓ := hs₀mem.1
  have hbefore : ∀ s ∈ Ico 0 s₀, X s ≤ -1 / 4 := by
    intro s hs
    by_contra hc
    push Not at hc
    have : s ∈ Sh := ⟨⟨hs.1, hs.2.le.trans hs₀ℓ.2⟩, le_of_lt hc⟩
    have := csInf_le hShb this
    linarith [hs.2]
  have hs₀pos : 0 < s₀ := by
    rcases hs₀ℓ.1.lt_or_eq with h | h
    · exact h
    · exfalso
      have : -1 / 4 ≤ X s₀ := hs₀mem.2
      rw [← h, hX0] at this
      norm_num at this
  have hXs₀ : X s₀ = -1 / 4 :=
    le_antisymm (le_of_forall_Ico hs₀pos hs₀ℓ.2 hX hbefore) hs₀mem.2
  have hXle : ∀ r ∈ Icc 0 s₀, X r ≤ -1 / 4 := by
    intro r hr
    rcases hr.2.lt_or_eq with h | h
    · exact hbefore r ⟨hr.1, h⟩
    · rw [h, hXs₀]
  have hsubs : Icc 0 s₀ ⊆ Icc 0 ℓ := Icc_subset_Icc le_rfl hs₀ℓ.2
  -- `cos φ > 0` em `[0, s₀]` (argumento de continuacao)
  have hcos : ∀ r ∈ Icc 0 s₀, 0 < cos (φ r) := by
    by_contra hneg
    push Not at hneg
    set Sc := Icc 0 s₀ ∩ (fun r => cos (φ r)) ⁻¹' Iic 0 with hSc
    have hcc : ContinuousOn (fun r => cos (φ r)) (Icc 0 ℓ) := continuous_cos.comp_continuousOn hφ
    have hScc : IsClosed Sc :=
      (hcc.mono hsubs).preimage_isClosed_of_isClosed isClosed_Icc isClosed_Iic
    obtain ⟨r₀, hr₀, hr₀c⟩ := hneg
    have hScne : Sc.Nonempty := ⟨r₀, hr₀, hr₀c⟩
    have hScb : BddBelow Sc := ⟨0, fun _ hs => hs.1.1⟩
    set σ := sInf Sc with hσ
    have hσmem : σ ∈ Sc := hScc.csInf_mem hScne hScb
    have hσpos : 0 < σ := by
      rcases hσmem.1.1.lt_or_eq with h | h
      · exact h
      · exfalso
        have : cos (φ σ) ≤ 0 := hσmem.2
        rw [← h, hφ0, cos_zero] at this
        norm_num at this
    have hpos : ∀ r ∈ Ico 0 σ, 0 < cos (φ r) := by
      intro r hr
      by_contra hc
      push Not at hc
      have : r ∈ Sc := ⟨⟨hr.1, hr.2.le.trans hσmem.1.2⟩, hc⟩
      have := csInf_le hScb this
      linarith [hr.2]
    have hσℓ : σ ≤ ℓ := hσmem.1.2.trans hs₀ℓ.2
    have hge : 0 ≤ cos (φ σ) := by
      have : -cos (φ σ) ≤ 0 := le_of_forall_Ico (f := fun r => -cos (φ r)) hσpos hσℓ hcc.neg
        (fun r hr => by have := hpos r hr; show -cos (φ r) ≤ 0; linarith)
      linarith
    have hzero : cos (φ σ) = 0 := le_antisymm hσmem.2 hge
    have hsb := sin_bound hX hφ hdX hdφ hκ hX0 hφ0 ⟨hσpos.le, hσℓ⟩
      (fun r hr => (hpos r ⟨hr.1.le, hr.2⟩).le)
    have hXσ := hXle σ hσmem.1
    have hsq := sin_sq_add_cos_sq (φ σ)
    rw [hzero] at hsq
    have habs : |sin (φ σ)| ≤ 3 / 8 := by linarith
    have : sin (φ σ) ^ 2 ≤ (3 / 8) ^ 2 := by
      rw [← sq_abs]; exact pow_le_pow_left₀ (abs_nonneg _) habs 2
    nlinarith
  -- cota `|sin φ| ≤ (X+1)/2` em `[0, s₀]`
  have hsin : ∀ r ∈ Icc 0 s₀, |sin (φ r)| ≤ (X r + 1) / 2 := fun r hr =>
    sin_bound hX hφ hdX hdφ hκ hX0 hφ0 (hsubs hr)
      (fun q hq => (hcos q ⟨hq.1.le, hq.2.le.trans hr.2⟩).le)
  -- comparacao para `Y` com `G = 2 - √(4 - (X+1)²)`
  have hIoo : ∀ r ∈ Ioo 0 s₀, r ∈ Ioo 0 ℓ := fun r hr => ⟨hr.1, lt_of_lt_of_le hr.2 hs₀ℓ.2⟩
  have hu : ∀ r ∈ Icc 0 s₀, 0 ≤ X r + 1 ∧ X r + 1 ≤ 3 / 4 := fun r hr =>
    ⟨by linarith [abs_nonneg (sin (φ r)), hsin r hr], by linarith [hXle r hr]⟩
  have hpos4 : ∀ r ∈ Icc 0 s₀, 0 < 4 - (X r + 1) ^ 2 := fun r hr => by
    nlinarith [(hu r hr).1, (hu r hr).2]
  have hGd : ∀ r ∈ Ioo 0 s₀, HasDerivAt (fun x => 2 - √(4 - (X x + 1) ^ 2))
      ((X r + 1) * cos (φ r) / √(4 - (X r + 1) ^ 2)) r := by
    intro r hr
    have hrI : r ∈ Icc 0 s₀ := ⟨hr.1.le, hr.2.le⟩
    have h1 := (((hdX r (hIoo r hr)).add_const 1).fun_pow 2).const_sub 4
    have h2 := (h1.sqrt (hpos4 r hrI).ne').const_sub 2
    convert h2 using 1
    have hsq : 0 < √(4 - (X r + 1) ^ 2) := Real.sqrt_pos.mpr (hpos4 r hrI)
    field_simp
    ring
  have hkey : ∀ r ∈ Ioo 0 s₀, |sin (φ r)| ≤ (X r + 1) * cos (φ r) / √(4 - (X r + 1) ^ 2) := by
    intro r hr
    have hrI : r ∈ Icc 0 s₀ := ⟨hr.1.le, hr.2.le⟩
    set u := X r + 1
    set w := √(4 - u ^ 2) with hw
    have hw0 : 0 < w := Real.sqrt_pos.mpr (hpos4 r hrI)
    have hw2 : w ^ 2 = 4 - u ^ 2 := Real.sq_sqrt (hpos4 r hrI).le
    have hc := hcos r hrI
    have hs := hsin r hrI
    have hsc := sin_sq_add_cos_sq (φ r)
    have hs2 : sin (φ r) ^ 2 ≤ (u / 2) ^ 2 := by
      rw [← sq_abs]; exact pow_le_pow_left₀ (abs_nonneg _) hs 2
    have hcw : w / 2 ≤ cos (φ r) := by nlinarith
    rw [le_div_iff₀ hw0]
    have hu0 := (hu r hrI).1
    nlinarith [abs_nonneg (sin (φ r)), mul_le_mul_of_nonneg_left hcw hu0,
      mul_le_mul_of_nonneg_right hs hw0.le]
  have hY0' : |Y 0| ≤ 2 - √(4 - (X 0 + 1) ^ 2) := by
    rw [hY0, hX0]
    have : √(4 : ℝ) = 2 := by
      rw [show (4 : ℝ) = 2 ^ 2 by norm_num, Real.sqrt_sq (by norm_num)]
    norm_num [this]
  have hYb := abs_le_of_deriv_right (f := Y) (f' := fun r => sin (φ r))
    (b := fun x => 2 - √(4 - (X x + 1) ^ 2))
    (b' := fun r => (X r + 1) * cos (φ r) / √(4 - (X r + 1) ^ 2)) hs₀ℓ.1
    (hY.mono hsubs)
    (continuousOn_const.sub (continuousOn_const.sub
      (((hX.mono hsubs).add continuousOn_const).pow 2)).sqrt)
    (fun r hr => hdY r (hIoo r hr)) hGd hY0' hkey
  rw [hXs₀] at hYb
  have hsq55 : (37 / 20 : ℝ) ≤ √(4 - (-1 / 4 + 1) ^ 2) := by
    have := Real.sqrt_le_sqrt (show ((37 / 20 : ℝ)) ^ 2 ≤ 4 - (-1 / 4 + 1) ^ 2 by norm_num)
    rwa [Real.sqrt_sq (by norm_num)] at this
  have hYs : |Y s₀| ≤ 3 / 20 := by linarith
  have hY2 : Y s₀ ^ 2 ≤ (3 / 20) ^ 2 := by
    rw [← sq_abs]; exact pow_le_pow_left₀ (abs_nonneg _) hYs 2
  refine ⟨s₀, hs₀ℓ, ?_⟩
  rw [hXs₀]
  nlinarith

end Disk

/-- A desigualdade numerica do livro: `2 - √(4 - 9/16) < √(1/4 - 1/16)` (`0.146 < 0.433`). -/
theorem disk_numeric : 2 - √(4 - 9 / 16 : ℝ) < √(1 / 4 - 1 / 16 : ℝ) := by
  have h1 : (37 / 20 : ℝ) ≤ √(4 - 9 / 16 : ℝ) := by
    have := Real.sqrt_le_sqrt (show ((37 / 20 : ℝ)) ^ 2 ≤ 4 - 9 / 16 by norm_num)
    rwa [Real.sqrt_sq (by norm_num)] at this
  have h2 : (2 / 5 : ℝ) ≤ √(1 / 4 - 1 / 16 : ℝ) := by
    have := Real.sqrt_le_sqrt (show ((2 / 5 : ℝ)) ^ 2 ≤ 1 / 4 - 1 / 16 by norm_num)
    rwa [Real.sqrt_sq (by norm_num)] at this
  linarith

/-! ### Testemunha e mutante da conta do disco: o arco de raio `2` (`κ ≡ 1/2`)

`X = -1 + 2 sin(s/2)`, `Y = 2 - 2 cos(s/2)`, `φ = s/2`, `ℓ = π`: satisfaz as hipoteses com
`|κ| = 1/2` (o caso extremo) e chega a `(1, 2)`. -/

def Xarc (s : ℝ) : ℝ := -1 + 2 * sin (s / 2)
def Yarc (s : ℝ) : ℝ := 2 - 2 * cos (s / 2)

theorem Xarc_deriv (s : ℝ) : HasDerivAt Xarc (cos (s / 2)) s := by
  unfold Xarc
  have := (((hasDerivAt_id' s).div_const 2).sin.const_mul 2).const_add (-1)
  convert this using 1
  ring

theorem Yarc_deriv (s : ℝ) : HasDerivAt Yarc (sin (s / 2)) s := by
  unfold Yarc
  have := (((hasDerivAt_id' s).div_const 2).cos.const_mul 2).const_sub 2
  convert this using 1
  ring

theorem φarc_deriv (s : ℝ) : HasDerivAt (fun s : ℝ => s / 2) (1 / 2) s :=
  (hasDerivAt_id' s).div_const 2

/-- Hipoteses de `disk_obstacle` para o arco de raio `2`. -/
theorem arc_hyps :
    ContinuousOn Xarc (Icc 0 π) ∧ ContinuousOn Yarc (Icc 0 π) ∧
    ContinuousOn (fun s : ℝ => s / 2) (Icc 0 π) ∧ Xarc 0 = -1 ∧ Yarc 0 = 0 ∧
    Xarc π = 1 := by
  refine ⟨(continuous_iff_continuousAt.mpr fun s => (Xarc_deriv s).continuousAt).continuousOn,
    (continuous_iff_continuousAt.mpr fun s => (Yarc_deriv s).continuousAt).continuousOn,
    (continuous_id.div_const 2).continuousOn, by simp [Xarc], by simp [Yarc], ?_⟩
  simp [Xarc, sin_pi_div_two]
  norm_num

/-- **Testemunha**: o arco de raio `2` satisfaz todas as hipoteses (com `|κ| = 1/2`), logo
entra no disco de raio `1/2`. -/
theorem witness_arc : ∃ s ∈ Icc 0 π, Xarc s ^ 2 + Yarc s ^ 2 < (1 / 2) ^ 2 := by
  obtain ⟨h1, h2, h3, h4, h5, h6⟩ := arc_hyps
  exact disk_obstacle (κ := fun _ => 1 / 2) pi_pos.le h1 h2 h3 (fun s _ => Xarc_deriv s)
    (fun s _ => Yarc_deriv s) (fun s _ => φarc_deriv s) (fun _ _ => by norm_num) h4 h5
    (by simp) h6

/-- O arco de raio `2` fica fora do disco de raio `1/10`: `X² + Y² = 9 - 4 sin - 8 cos ≥ 9 - 4√5`. -/
theorem arc_avoids_small_disk (s : ℝ) : (1 / 10) ^ 2 ≤ Xarc s ^ 2 + Yarc s ^ 2 := by
  have e : Xarc s ^ 2 + Yarc s ^ 2 = 9 - 4 * sin (s / 2) - 8 * cos (s / 2) := by
    simp only [Xarc, Yarc]
    nlinarith [sin_sq_add_cos_sq (s / 2)]
  rw [e]
  nlinarith [sin_sq_add_cos_sq (s / 2), sq_nonneg (2 * sin (s / 2) - cos (s / 2)),
    sq_nonneg (sin (s / 2) + 2 * cos (s / 2) - 9 / 4)]

/-- **Mutante** (raio `1/10` em vez de `1/2`): falso, pelo arco de raio `2`. -/
theorem mutant_small_disk_false :
    ¬ (∀ (X Y φ κ : ℝ → ℝ) (ℓ : ℝ), 0 ≤ ℓ → ContinuousOn X (Icc 0 ℓ) →
        ContinuousOn Y (Icc 0 ℓ) → ContinuousOn φ (Icc 0 ℓ) →
        (∀ s ∈ Ioo 0 ℓ, HasDerivAt X (cos (φ s)) s) →
        (∀ s ∈ Ioo 0 ℓ, HasDerivAt Y (sin (φ s)) s) →
        (∀ s ∈ Ioo 0 ℓ, HasDerivAt φ (κ s) s) → (∀ s ∈ Ioo 0 ℓ, |κ s| ≤ 1 / 2) →
        X 0 = -1 → Y 0 = 0 → φ 0 = 0 → X ℓ = 1 →
        ∃ s ∈ Icc 0 ℓ, X s ^ 2 + Y s ^ 2 < (1 / 10) ^ 2) := by
  intro hm
  obtain ⟨h1, h2, h3, h4, h5, h6⟩ := arc_hyps
  obtain ⟨s, -, hs⟩ := hm Xarc Yarc (fun s => s / 2) (fun _ => 1 / 2) π pi_pos.le h1 h2 h3
    (fun s _ => Xarc_deriv s) (fun s _ => Yarc_deriv s) (fun s _ => φarc_deriv s)
    (fun _ _ => by norm_num) h4 h5 (by simp) h6
  linarith [arc_avoids_small_disk s]

/-! ## `prop:optimal_regularity`: o nucleo -/

/-- **Nucleo de `prop:optimal_regularity`**: uma funcao continua em `[0,L]` com valores em
`{0, K, -K}` e constante. -/
theorem continuous_three_values_const {κ : ℝ → ℝ} {L K : ℝ} (hL : 0 ≤ L)
    (hc : ContinuousOn κ (Icc 0 L)) (hv : ∀ s ∈ Icc 0 L, κ s = 0 ∨ κ s = K ∨ κ s = -K) :
    ∀ s ∈ Icc 0 L, κ s = κ 0 := by
  have h0 : (0 : ℝ) ∈ Icc 0 L := ⟨le_rfl, hL⟩
  have hoc : (κ '' Icc 0 L).OrdConnected := (isPreconnected_Icc.image κ hc).ordConnected
  have hfin : (κ '' Icc 0 L).Finite := by
    refine ({0, K, -K} : Set ℝ).toFinite.subset ?_
    rintro _ ⟨s, hs, rfl⟩
    rcases hv s hs with h | h | h <;> simp [h]
  intro s hs
  by_contra hne
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · exact Set.Icc_infinite hlt (hfin.subset (hoc.out (mem_image_of_mem κ hs)
      (mem_image_of_mem κ h0)))
  · exact Set.Icc_infinite hgt (hfin.subset (hoc.out (mem_image_of_mem κ h0)
      (mem_image_of_mem κ hs)))

/-- **`prop:optimal_regularity`, passo final**: se a curvatura de um minimizador `C²` e
continua, toma valores em `{0, ±K}` (teorema de Dubins, hipotese `hDubins`) e o minimizador
nao e um segmento (`hnotseg`), entao e um unico arco: `κ ≡ K` ou `κ ≡ -K`. -/
theorem c2_minimizer_single_arc {κ : ℝ → ℝ} {L K : ℝ} (hL : 0 ≤ L)
    (hc : ContinuousOn κ (Icc 0 L))
    (hDubins : ∀ s ∈ Icc 0 L, κ s = 0 ∨ κ s = K ∨ κ s = -K)
    (hnotseg : ∃ s ∈ Icc 0 L, κ s ≠ 0) :
    (∀ s ∈ Icc 0 L, κ s = K) ∨ (∀ s ∈ Icc 0 L, κ s = -K) := by
  have hconst := continuous_three_values_const hL hc hDubins
  obtain ⟨s₁, hs₁, hne⟩ := hnotseg
  rcases hDubins 0 ⟨le_rfl, hL⟩ with h | h | h
  · exact absurd (by rw [hconst s₁ hs₁, h]) hne
  · exact Or.inl fun s hs => by rw [hconst s hs, h]
  · exact Or.inr fun s hs => by rw [hconst s hs, h]

/-- Perfil de curvatura de um caminho de Dubins `CS` com `K̂ = 1`: arco em `[0,1/2]`, segmento
depois. -/
def κCS (s : ℝ) : ℝ := if s ≤ 1 / 2 then 1 else 0

/-- **Testemunha** (o teorema morde): o perfil `CS` tem valores em `{0, ±1}` e nao e um
segmento; pelo teorema, NAO e continuo, isto e, nao e a curvatura de uma curva `C²`. -/
theorem witness_CS_not_continuous : ¬ ContinuousOn κCS (Icc 0 1) := by
  intro hc
  have hv : ∀ s ∈ Icc (0 : ℝ) 1, κCS s = 0 ∨ κCS s = 1 ∨ κCS s = -1 := by
    intro s _
    unfold κCS
    split_ifs <;> simp
  have := continuous_three_values_const zero_le_one hc hv 1 ⟨zero_le_one, le_rfl⟩
  norm_num [κCS] at this

/-- **Testemunha** (hipoteses satisfeitas): o arco unico `κ ≡ 1`. -/
theorem witness_single_arc :
    (∀ s ∈ Icc (0 : ℝ) 1, (fun _ : ℝ => (1 : ℝ)) s = 1) ∨
    (∀ s ∈ Icc (0 : ℝ) 1, (fun _ : ℝ => (1 : ℝ)) s = -1) :=
  c2_minimizer_single_arc zero_le_one continuousOn_const (fun _ _ => Or.inr (Or.inl rfl))
    ⟨0, ⟨le_rfl, zero_le_one⟩, one_ne_zero⟩

/-- Mutante 1 (sem continuidade): falso, pelo perfil `CS`. -/
theorem mutant_no_continuity_false :
    ¬ (∀ (κ : ℝ → ℝ) (L K : ℝ), 0 ≤ L → (∀ s ∈ Icc 0 L, κ s = 0 ∨ κ s = K ∨ κ s = -K) →
        ∀ s ∈ Icc 0 L, κ s = κ 0) := by
  intro hm
  have := hm κCS 1 1 zero_le_one (by intro s _; unfold κCS; split_ifs <;> simp) 1
    ⟨zero_le_one, le_rfl⟩
  norm_num [κCS] at this

/-- Mutante 2 (valores no intervalo `[-K, K]` em vez de `{0, ±K}`): falso, `κ(s) = s`. -/
theorem mutant_interval_values_false :
    ¬ (∀ (κ : ℝ → ℝ) (L K : ℝ), 0 ≤ L → ContinuousOn κ (Icc 0 L) →
        (∀ s ∈ Icc 0 L, κ s ∈ Icc (-K) K) → ∀ s ∈ Icc 0 L, κ s = κ 0) := by
  intro hm
  have := hm id 1 1 zero_le_one continuousOn_id
    (fun s hs => ⟨show -1 ≤ s by linarith [hs.1], hs.2⟩) 1 ⟨zero_le_one, le_rfl⟩
  norm_num at this

end LeanReal.Chap07Control

#print axioms LeanReal.Chap07Control.abs_le_of_deriv_right
#print axioms LeanReal.Chap07Control.abs_le_of_deriv_left
#print axioms LeanReal.Chap07Control.WallTraj.taylor
#print axioms LeanReal.Chap07Control.WallTraj.taylor_contact
#print axioms LeanReal.Chap07Control.WallTraj.kappa_pos_of_contact
#print axioms LeanReal.Chap07Control.WallTraj.pos_near_contact
#print axioms LeanReal.Chap07Control.WallTraj.contact_isolated
#print axioms LeanReal.Chap07Control.WallTraj.theta_zero_of_interior
#print axioms LeanReal.Chap07Control.WallTraj.zero_set_finite
#print axioms LeanReal.Chap07Control.wall_structure_c
#print axioms LeanReal.Chap07Control.wall_structure_d
#print axioms LeanReal.Chap07Control.witness_A
#print axioms LeanReal.Chap07Control.witness_B
#print axioms LeanReal.Chap07Control.mutant_no_state_constraint_false
#print axioms LeanReal.Chap07Control.mutant_radius_four_false
#print axioms LeanReal.Chap07Control.mutant_finite_without_state_false
#print axioms LeanReal.Chap07Control.mutant_arc_degenerate_false
#print axioms LeanReal.Chap07Control.second_order_min
#print axioms LeanReal.Chap07Control.contact_principle_curve
#print axioms LeanReal.Chap07Control.contact_curvature_bound
#print axioms LeanReal.Chap07Control.witness_circle
#print axioms LeanReal.Chap07Control.mutant_no_inclusion_false
#print axioms LeanReal.Chap07Control.mutant_abs_lambda_false
#print axioms LeanReal.Chap07Control.sin_bound
#print axioms LeanReal.Chap07Control.disk_obstacle
#print axioms LeanReal.Chap07Control.disk_numeric
#print axioms LeanReal.Chap07Control.witness_arc
#print axioms LeanReal.Chap07Control.mutant_small_disk_false
#print axioms LeanReal.Chap07Control.continuous_three_values_const
#print axioms LeanReal.Chap07Control.c2_minimizer_single_arc
#print axioms LeanReal.Chap07Control.witness_CS_not_continuous
#print axioms LeanReal.Chap07Control.witness_single_arc
#print axioms LeanReal.Chap07Control.mutant_no_continuity_false
#print axioms LeanReal.Chap07Control.mutant_interval_values_false
