import LeanReal.Chap07Control

/-!
# Complementos L2 do lote LIVRO_B9 (`Chap07Control`)

Tres complementos a revisao de fidelidade:

1. `kappa_pos_of_radius`: a condicao de raio `0 < |s-t| < 3κ(t)` ja implica `κ(t) > 0`, o que
   justifica a retirada dessa hipotese em `WallTraj.pos_near_contact`.
2. `mutant_radius_gt_three_false`: para TODO `c > 3`, o raio `c κ(t)` falha (a mesma
   trajetoria `y = s²/2 - s³/6`, que e o controle extremo `u ≡ -1`). Isto e a afirmacao
   "o raio `3κ` e otimo" em forma geral, nao so para `c = 4`.
3. `mutant_wall_structure_d_no_hB_false`: sem a hipotese `hB` (item (b) do lema, a unica
   entrada da minimalidade), o item (d)(ii) falha: a trajetoria `y = (1-cos(t-1))²/10` em
   `[0, 1+2π]` e admissivel (`|y'''| ≤ 1`, `y ≥ 0`, estado final nulo), tem estado nulo em
   `t = 1 < t*`, e la `κ(1) = 0`. Logo `hB` e portadora de conteudo, nao decorativa.
-/

noncomputable section

namespace LeanReal.L2_LIVRO_B9_Extra

open Set Filter Topology Real LeanReal.Chap07Control

/-- A condicao de raio do livro forca o sinal: `0 < |s-t| < 3κ(t)` implica `κ(t) > 0`. -/
theorem kappa_pos_of_radius {κt s t : ℝ} (hst : s ≠ t) (hd : |s - t| < 3 * κt) : 0 < κt := by
  have := abs_pos.mpr (sub_ne_zero.mpr hst)
  linarith

/-- Para todo `c > 3`, "`y(s) > 0` para `0 < |s-t| < c κ(t)`" e falso: `y = s²/2 - s³/6` em
`[0,3]`, `t = 0`, `κ(0) = 1`, `y(3) = 0` e `3 < c`. -/
theorem mutant_radius_gt_three_false (c : ℝ) (hc : 3 < c) :
    ¬ (∀ (T : ℝ) (y θ κ : ℝ → ℝ) (t : ℝ), WallTraj T y θ κ → (∀ s ∈ Icc 0 T, 0 ≤ y s) →
        t ∈ Icc 0 T → y t = 0 → θ t = 0 → 0 < κ t →
        ∀ s ∈ Icc 0 T, s ≠ t → |s - t| < c * κ t → 0 < y s) := by
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
    3 ⟨by norm_num, le_rfl⟩ (by norm_num) (by norm_num; linarith)
  norm_num at this

/-! ## Trajetoria com estado nulo antes de `t*`: `y = (1 - cos(t-1))²/10` -/

def yC (t : ℝ) : ℝ := (1 - cos (t - 1)) ^ 2 / 10
def θC (t : ℝ) : ℝ := 2 * (1 - cos (t - 1)) * sin (t - 1) / 10
def κC (t : ℝ) : ℝ := (2 * sin (t - 1) ^ 2 + 2 * (1 - cos (t - 1)) * cos (t - 1)) / 10
def uC (t : ℝ) : ℝ := (8 * sin (t - 1) * cos (t - 1) - 2 * sin (t - 1)) / 10

theorem s_deriv (t : ℝ) : HasDerivAt (fun x : ℝ => x - 1) 1 t := (hasDerivAt_id' t).sub_const 1

theorem oneSubCos_deriv (t : ℝ) :
    HasDerivAt (fun x : ℝ => 1 - cos (x - 1)) (sin (t - 1)) t := by
  have := ((s_deriv t).cos).const_sub 1
  convert this using 1; ring

theorem yC_deriv (t : ℝ) : HasDerivAt yC (θC t) t := by
  have := ((oneSubCos_deriv t).fun_pow 2).div_const 10
  unfold yC
  convert this using 1
  simp only [θC]
  norm_num

theorem θC_deriv (t : ℝ) : HasDerivAt θC (κC t) t := by
  have := (((oneSubCos_deriv t).const_mul 2).mul ((s_deriv t).sin)).div_const 10
  unfold θC
  convert this using 1
  simp only [κC]
  ring

theorem κC_deriv (t : ℝ) : HasDerivAt κC (uC t) t := by
  have h1 := (((s_deriv t).sin).fun_pow 2).const_mul 2
  have h2 := ((oneSubCos_deriv t).const_mul 2).mul ((s_deriv t).cos)
  have := (h1.add h2).div_const 10
  unfold κC
  convert this using 1
  simp only [uC]
  norm_num
  ring

theorem abs_uC_le (t : ℝ) : |uC t| ≤ 1 := by
  unfold uC
  rw [abs_le]
  constructor <;>
    nlinarith [sin_sq_add_cos_sq (t - 1), neg_one_le_sin (t - 1), sin_le_one (t - 1),
      neg_one_le_cos (t - 1), cos_le_one (t - 1), sq_nonneg (sin (t - 1) - cos (t - 1)),
      sq_nonneg (sin (t - 1) + cos (t - 1))]

theorem κC_lip : LipschitzWith 1 κC := by
  refine lipschitzWith_of_nnnorm_deriv_le (fun t => (κC_deriv t).differentiableAt) fun t => ?_
  rw [(κC_deriv t).deriv]
  have h := abs_uC_le t
  rw [← NNReal.coe_le_coe, coe_nnnorm, Real.norm_eq_abs, NNReal.coe_one]
  exact h

theorem wallTraj_C : WallTraj (1 + 2 * π) yC θC κC where
  cont_y := (continuous_iff_continuousAt.mpr fun t => (yC_deriv t).continuousAt).continuousOn
  cont_θ := (continuous_iff_continuousAt.mpr fun t => (θC_deriv t).continuousAt).continuousOn
  lip_κ := κC_lip.lipschitzOnWith
  deriv_y := fun s _ => yC_deriv s
  deriv_θ := fun s _ => θC_deriv s

theorem yC_nonneg : ∀ s ∈ Icc (0 : ℝ) (1 + 2 * π), 0 ≤ yC s := by
  intro s _
  unfold yC
  positivity

theorem stateZero_C_T : StateZero yC θC κC (1 + 2 * π) := by
  have e : (1 + 2 * π) - 1 = 2 * π := by ring
  refine ⟨?_, ?_, ?_⟩ <;> simp [yC, θC, κC, e]

theorem stateZero_C_one : StateZero yC θC κC 1 := by
  refine ⟨?_, ?_, ?_⟩ <;> simp [yC, θC, κC]

theorem yC_one_add_pi : yC (1 + π) = 2 / 5 := by
  have e : (1 + π) - 1 = π := by ring
  simp [yC, e]
  norm_num

theorem tStar_C_ge : 1 + π ≤ tStar (1 + 2 * π) yC θC κC := by
  unfold tStar
  refine le_csInf ⟨1 + 2 * π, T_mem_restSet (by positivity) stateZero_C_T⟩ ?_
  intro t ht
  by_contra hlt
  push Not at hlt
  have hmem : (1 + π) ∈ Icc t (1 + 2 * π) := ⟨hlt.le, by linarith [pi_pos]⟩
  have := (ht.2 (1 + π) hmem).1
  rw [yC_one_add_pi] at this
  norm_num at this

theorem one_mem_contact_C : (1 : ℝ) ∈ contactSet (1 + 2 * π) yC θC κC :=
  ⟨⟨by norm_num, by linarith [pi_pos]⟩, by linarith [tStar_C_ge, pi_pos], stateZero_C_one.1⟩

/-- Sem `hB`, o item (d)(ii) e falso: `t = 1 ∈ Z ∩ (0, t*)` com `κ(1) = 0`. -/
theorem mutant_wall_structure_d_no_hB_false :
    ¬ (∀ (T : ℝ) (y θ κ : ℝ → ℝ), WallTraj T y θ κ → (∀ s ∈ Icc 0 T, 0 ≤ y s) →
        0 ≤ T → StateZero y θ κ T →
        ∀ t ∈ contactSet T y θ κ, 0 < t → θ t = 0 ∧ 0 < κ t) := by
  intro hm
  have := (hm (1 + 2 * π) yC θC κC wallTraj_C yC_nonneg (by positivity) stateZero_C_T
    1 one_mem_contact_C one_pos).2
  rw [stateZero_C_one.2.2] at this
  exact lt_irrefl _ this

/-- A mesma trajetoria mostra que `hB` falha nela: o estado se anula em `1` mas nao em `1 + π`. -/
theorem hB_fails_C :
    ¬ (∀ τ ∈ Icc (0 : ℝ) (1 + 2 * π), StateZero yC θC κC τ →
        ∀ s ∈ Icc τ (1 + 2 * π), StateZero yC θC κC s) := by
  intro hB
  have := (hB 1 ⟨by norm_num, by linarith [pi_pos]⟩ stateZero_C_one (1 + π)
    ⟨by linarith [pi_pos], by linarith [pi_pos]⟩).1
  rw [yC_one_add_pi] at this
  norm_num at this

end LeanReal.L2_LIVRO_B9_Extra

#print axioms LeanReal.L2_LIVRO_B9_Extra.kappa_pos_of_radius
#print axioms LeanReal.L2_LIVRO_B9_Extra.mutant_radius_gt_three_false
#print axioms LeanReal.L2_LIVRO_B9_Extra.wallTraj_C
#print axioms LeanReal.L2_LIVRO_B9_Extra.mutant_wall_structure_d_no_hB_false
#print axioms LeanReal.L2_LIVRO_B9_Extra.hB_fails_C
