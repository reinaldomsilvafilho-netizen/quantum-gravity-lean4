import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.Calculus.Deriv.Prod
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Inverse

/-!
# Capitulo 9, `prop:mouth_halfturn` (item L4 do `PLANO_FORMALIZACAO.md`)

Fonte: `unified_quantum_gravity_book/chap09_*.tex`, Proposicao "Mouth width under a half-turn
range" (`prop:mouth_halfturn`):

> Let `γ : [0,L] → ℝ²` be admissible, with `γ(0), γ(L) ∈ W_a`, `γ'(0) = (1,0)` and
> `γ'(L) = (-1,0)`. Suppose a continuous tangent angle `θ` with `θ(0) = 0` satisfies
> `θ([0,L]) ⊂ [0,π]`. Then `y(L) - y(0) ≥ 2ρ`. In particular `a ≥ 2ρ`, whatever the balloon.

Definicoes do capitulo: `W_a = {0} × [-a/2, a/2]`; "admissible" = `C^{1,1}`, parametrizada por
comprimento de arco, `|κ| ≤ κ* = 1/ρ` q.t.p.

## Reducao declarada

* `γ = (x, y) : ℝ → ℝ × ℝ`, continua em `[0,L]`, com `γ'(s) = (cos θ(s), sin θ(s))` em
  `(0,L)`: comprimento de arco e `θ` angulo tangente.
* `θ` e DIFERENCIAVEL em todo ponto de `(0,L)` e continua em `[0,L]`, com `|θ'| ≤ 1/ρ` em
  `(0,L)`. O livro pede so `θ` Lipschitz (`C^{1,1}`), com a cota q.t.p.; esse caso NAO esta
  coberto (exigiria FTC/monotonia para funcoes absolutamente continuas). Nao se pede `θ'`
  continua: a prova usa monotonia via derivada, nao integrais.
* `γ'(0) = (1,0)` e codificado por `θ(0) = 0` (o livro escolhe assim o angulo); `γ'(L) = (-1,0)`
  e codificado por `cos θ(L) = -1` (o seno nulo segue). Daqui e de `θ(L) ∈ [0,π]` sai
  `θ(L) = π`, como no livro.
* Prova: `g = y + ρ cos θ` tem `g' = sin θ (1 - ρ θ') ≥ 0`, logo `g(0) ≤ g(L)`. E a mesma
  desigualdade `∫ sin θ ≥ ρ ∫ sin θ θ'` do livro, sem integrais.
-/

noncomputable section

namespace LeanReal.Chap09MouthHalfturn

open Set Real

/-- **Proposicao `prop:mouth_halfturn`** (primeira afirmacao), na reducao do cabecalho. -/
theorem mouth_halfturn (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L ρ : ℝ) (hL : 0 ≤ L) (hρ : 0 < ρ)
    (hγc : ContinuousOn γ (Icc 0 L))
    (hγ : ∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L)) (hθ : ∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s)
    (hκ : ∀ s ∈ Ioo 0 L, |θ' s| ≤ 1 / ρ)
    (h0 : θ 0 = 0) (hend : cos (θ L) = -1)
    (hrange : ∀ s ∈ Icc 0 L, θ s ∈ Icc 0 π) :
    (γ L).2 - (γ 0).2 ≥ 2 * ρ := by
  have hLmem : L ∈ Icc 0 L := ⟨hL, le_rfl⟩
  have h0mem : (0 : ℝ) ∈ Icc 0 L := ⟨le_rfl, hL⟩
  -- θ(L) = π
  have hθL : θ L = π :=
    injOn_cos (hrange L hLmem) ⟨pi_pos.le, le_rfl⟩ (by rw [hend, cos_pi])
  -- g = y + ρ cos θ e monotona em [0,L]
  set g : ℝ → ℝ := fun s => (γ s).2 + ρ * cos (θ s) with hg
  have hmono : MonotoneOn g (Icc 0 L) := by
    refine monotoneOn_of_hasDerivWithinAt_nonneg (f' := fun s => sin (θ s) +
        ρ * (-sin (θ s) * θ' s)) (convex_Icc 0 L) ?_ ?_ ?_
    · exact (continuous_snd.comp_continuousOn hγc).add
        (continuousOn_const.mul (continuous_cos.comp_continuousOn hθc))
    · intro s hs
      rw [interior_Icc] at hs
      have hy : HasDerivAt (fun x => (γ x).2) (sin (θ s)) s := by
        have := ((ContinuousLinearMap.snd ℝ ℝ ℝ).hasFDerivAt.comp s
          (hγ s hs).hasFDerivAt).hasDerivAt
        simp only [ContinuousLinearMap.comp_apply, ContinuousLinearMap.toSpanSingleton_apply,
          one_smul, ContinuousLinearMap.coe_snd'] at this
        exact this
      exact (hy.add (((hθ s hs).cos).const_mul ρ)).hasDerivWithinAt
    · intro s hs
      rw [interior_Icc] at hs
      have hsin : 0 ≤ sin (θ s) :=
        sin_nonneg_of_nonneg_of_le_pi (hrange s (Ioo_subset_Icc_self hs)).1
          (hrange s (Ioo_subset_Icc_self hs)).2
      have hk : ρ * θ' s ≤ 1 := by
        have h1 := (abs_le.mp (hκ s hs)).2
        rw [le_div_iff₀ hρ] at h1
        linarith
      have : sin (θ s) + ρ * (-sin (θ s) * θ' s) = sin (θ s) * (1 - ρ * θ' s) := by ring
      rw [this]
      exact mul_nonneg hsin (by linarith)
  have := hmono h0mem hLmem hL
  simp only [hg, h0, hθL, cos_zero, cos_pi] at this
  linarith

/-- **`prop:mouth_halfturn`, "in particular `a ≥ 2ρ`"**: se `γ(0), γ(L) ∈ W_a`. -/
theorem mouth_width (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L ρ a : ℝ) (hL : 0 ≤ L) (hρ : 0 < ρ)
    (hγc : ContinuousOn γ (Icc 0 L))
    (hγ : ∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L)) (hθ : ∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s)
    (hκ : ∀ s ∈ Ioo 0 L, |θ' s| ≤ 1 / ρ)
    (h0 : θ 0 = 0) (hend : cos (θ L) = -1)
    (hrange : ∀ s ∈ Icc 0 L, θ s ∈ Icc 0 π)
    (hW0 : (γ 0).1 = 0 ∧ (γ 0).2 ∈ Icc (-(a / 2)) (a / 2))
    (hWL : (γ L).1 = 0 ∧ (γ L).2 ∈ Icc (-(a / 2)) (a / 2)) :
    a ≥ 2 * ρ := by
  have := mouth_halfturn γ θ θ' L ρ hL hρ hγc hγ hθc hθ hκ h0 hend hrange
  linarith [hW0.2.1, hWL.2.2]

/-! ## Testemunha: o semicirculo de raio `1` (`ρ = 1`, `a = 2`), com igualdade -/

/-- Semicirculo `s ↦ (sin s, -cos s)`, `s ∈ [0,π]`, angulo tangente `θ(s) = s`. -/
def semi (s : ℝ) : ℝ × ℝ := (sin s, -cos s)

theorem semi_hasDerivAt (s : ℝ) : HasDerivAt semi (cos s, sin s) s := by
  have := (hasDerivAt_sin s).prodMk (hasDerivAt_cos s).neg
  rw [neg_neg] at this
  exact this

theorem witness_semicircle :
    0 ≤ π ∧ (0 : ℝ) < 1 ∧ ContinuousOn semi (Icc 0 π) ∧
    (∀ s ∈ Ioo 0 π, HasDerivAt semi (cos (id s), sin (id s)) s) ∧
    ContinuousOn id (Icc 0 π) ∧ (∀ s ∈ Ioo 0 π, HasDerivAt id ((fun _ => (1:ℝ)) s) s) ∧
    (∀ s ∈ Ioo (0:ℝ) π, |(fun _ => (1:ℝ)) s| ≤ 1 / 1) ∧
    id (0:ℝ) = 0 ∧ cos (id π) = -1 ∧ (∀ s ∈ Icc 0 π, id s ∈ Icc 0 π) ∧
    ((semi 0).1 = 0 ∧ (semi 0).2 ∈ Icc (-(2 / 2)) (2 / 2)) ∧
    ((semi π).1 = 0 ∧ (semi π).2 ∈ Icc (-(2 / 2)) (2 / 2)) ∧
    (semi π).2 - (semi 0).2 = 2 * 1 := by
  refine ⟨pi_pos.le, one_pos, ?_, fun s _ => semi_hasDerivAt s, continuousOn_id,
    fun s _ => hasDerivAt_id s, fun s _ => by norm_num, rfl, cos_pi, fun s hs => hs,
    ?_, ?_, ?_⟩
  · exact (continuous_sin.prodMk continuous_cos.neg).continuousOn
  · simp [semi]
  · simp [semi]
  · simp [semi]; norm_num

/-- Aplicacao a testemunha (os tipos casam; a conclusao vale com igualdade). -/
example : (2 : ℝ) ≥ 2 * 1 := by
  obtain ⟨hL, hρ, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, -⟩ := witness_semicircle
  exact mouth_width semi id (fun _ => 1) π 1 2 hL hρ h1 h2 h3 h4 h5 h6 h7 h8 h9 h10

/-! ## Mutantes provados FALSOS -/

/-- Mutante 1 (conclusao estrita `> 2ρ`): falso, pelo semicirculo. -/
theorem mutant_strict_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L ρ : ℝ), 0 ≤ L → 0 < ρ →
        ContinuousOn γ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s) →
        (∀ s ∈ Ioo 0 L, |θ' s| ≤ 1 / ρ) → θ 0 = 0 → cos (θ L) = -1 →
        (∀ s ∈ Icc 0 L, θ s ∈ Icc 0 π) → (γ L).2 - (γ 0).2 > 2 * ρ) := by
  intro h
  obtain ⟨hL, hρ, h1, h2, h3, h4, h5, h6, h7, h8, -, -, heq⟩ := witness_semicircle
  have := h semi id (fun _ => 1) π 1 hL hρ h1 h2 h3 h4 h5 h6 h7 h8
  linarith

/-- Mutante 2 (sem a cota de curvatura `|θ'| ≤ 1/ρ`): falso, pelo semicirculo de raio `1`
com `ρ = 2` (subida `2 < 4`). -/
theorem mutant_no_curvature_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L ρ : ℝ), 0 ≤ L → 0 < ρ →
        ContinuousOn γ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s) →
        θ 0 = 0 → cos (θ L) = -1 →
        (∀ s ∈ Icc 0 L, θ s ∈ Icc 0 π) → (γ L).2 - (γ 0).2 ≥ 2 * ρ) := by
  intro h
  obtain ⟨hL, -, h1, h2, h3, h4, -, h6, h7, h8, -, -, heq⟩ := witness_semicircle
  have := h semi id (fun _ => 1) π 2 hL two_pos h1 h2 h3 h4 h6 h7 h8
  linarith

/-- Mutante 3 (sem a hipotese de faixa `θ([0,L]) ⊂ [0,π]`): falso para a desigualdade COM SINAL
`y(L) - y(0) ≥ 2ρ`. Contraexemplo: o semicirculo refletido, `θ(s) = -s`,
`γ(s) = (sin s, cos s)`, `L = π`, `ρ = 1`, que DESCE `-2 < 2`. A reflexao `θ ↦ -θ` nao altera
`|Δy| = 2ρ`, entao este mutante nao serve para `mouth_width` (largura `a`); o contraexemplo do
livro para a largura (a gota `γ_a`, `a < 2ρ`) continua nao formalizado. -/
theorem mutant_no_range_false :
    ¬ (∀ (γ : ℝ → ℝ × ℝ) (θ θ' : ℝ → ℝ) (L ρ : ℝ), 0 ≤ L → 0 < ρ →
        ContinuousOn γ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt γ (cos (θ s), sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt θ (θ' s) s) →
        (∀ s ∈ Ioo 0 L, |θ' s| ≤ 1 / ρ) → θ 0 = 0 → cos (θ L) = -1 →
        (γ L).2 - (γ 0).2 ≥ 2 * ρ) := by
  intro h
  have := h (fun s => (sin s, cos s)) (fun s => -s) (fun _ => -1) π 1 pi_pos.le one_pos
    (continuous_sin.prodMk continuous_cos).continuousOn
    (fun s _ => by
      have := (hasDerivAt_sin s).prodMk (hasDerivAt_cos s)
      simpa [cos_neg, sin_neg] using this)
    continuous_neg.continuousOn (fun s _ => by simpa using (hasDerivAt_neg s))
    (fun s _ => by norm_num) (by simp) (by simp)
  simp at this
  linarith

end LeanReal.Chap09MouthHalfturn

#print axioms LeanReal.Chap09MouthHalfturn.mouth_halfturn
#print axioms LeanReal.Chap09MouthHalfturn.mouth_width
#print axioms LeanReal.Chap09MouthHalfturn.witness_semicircle
#print axioms LeanReal.Chap09MouthHalfturn.mutant_strict_false
#print axioms LeanReal.Chap09MouthHalfturn.mutant_no_curvature_false
#print axioms LeanReal.Chap09MouthHalfturn.mutant_no_range_false
