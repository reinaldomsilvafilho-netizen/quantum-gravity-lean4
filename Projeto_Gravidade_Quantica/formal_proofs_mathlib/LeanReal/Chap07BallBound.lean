import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.Complex.Trigonometric

/-!
# Capitulo 7, `prop:ball_bound`, caso de CURVAS (item L3 do `PLANO_FORMALIZACAO.md`)

Fonte: `unified_quantum_gravity_book/chap07_*.tex`, Proposicao "Closed submanifolds cannot be
squeezed" (`prop:ball_bound`):

> Let `M^k` be a compact manifold without boundary, `k ≥ 1`, and let `f : M → ℝ^n` be a
> `C^{1,1}` immersion with `‖II‖_{L^∞(M)} ≤ κ`. If `f(M)` lies in a closed ball of radius `R`,
> then `κR ≥ 1`. Equality holds for the round sphere `S^k(R) ⊂ ℝ^{k+1}`.

## Reducao declarada (o que e formalizado e o que NAO e)

* So `k = 1` (curvas). `M = ℝ/Tℤ` e representado por uma `f : ℝ → E` periodica de periodo
  `T > 0`.
* `E` e um espaco com produto interno real qualquer; `ℝ^n = EuclideanSpace ℝ (Fin n)` e um caso
  particular (corolario `ball_bound_euclidean`). Nao se supoe dimensao finita.
* Regularidade: `f` e DUAS VEZES DIFERENCIAVEL em todo ponto (`HasDerivAt f (f' t) t` e
  `HasDerivAt f' (f'' t) t`). Isso e mais forte que `C^{1,1}` (o livro) e mais fraco que `C²`
  (nao se pede continuidade de `f''`). O caso `C^{1,1}` com `f''` so q.t.p. NAO esta coberto.
* Parametrizacao por comprimento de arco: `‖f' t‖ = 1`. Entao `|II| = ‖f''‖` e a hipotese
  `‖II‖_{L^∞} ≤ κ` vira `‖f'' t‖ ≤ κ` em todo `t`.
* Bola fechada de centro `c` arbitrario e raio `R`.

Rota (a do livro para curvas, `rem:compactness_necessity`): no ponto `t₀` de maximo de
`φ = ‖f - c‖²`, `φ'(t₀) = 0` e `φ''(t₀) ≤ 0`, isto e `⟪f - c, f''⟫ + ‖f'‖² ≤ 0`; por
Cauchy-Schwarz `1 ≤ ‖f - c‖ ‖f''‖ ≤ Rκ`. A condicao necessaria de segunda ordem
(`φ'' ≤ 0` num maximo) NAO esta na Mathlib nesta revisao (so os testes suficientes
`isLocalMax_of_deriv_deriv_neg` etc.); ela e provada abaixo em `not_isMax_of_deriv_pos`.
-/

noncomputable section

namespace LeanReal.Chap07BallBound

open Set Filter Topology

/-- Lema auxiliar (condicao necessaria de 2a ordem, forma usada): se `φ' = ψ` em toda parte,
`ψ(t₀) = 0` e `ψ'(t₀) > 0`, entao `φ` toma em algum ponto um valor maior que `φ(t₀)`. -/
theorem not_isMax_of_deriv_pos (φ ψ : ℝ → ℝ) (t₀ d : ℝ)
    (hφ : ∀ t, HasDerivAt φ (ψ t) t) (hψ : HasDerivAt ψ d t₀)
    (h0 : ψ t₀ = 0) (hd : 0 < d) : ∃ t, φ t₀ < φ t := by
  have hsl : Tendsto (slope ψ t₀) (𝓝[>] t₀) (𝓝 d) :=
    (hasDerivAt_iff_tendsto_slope.mp hψ).mono_left
      (nhdsWithin_mono _ fun x hx => Set.mem_compl_singleton_iff.mpr (ne_of_gt hx))
  have hev : ∀ᶠ x in 𝓝[>] t₀, 0 < ψ x := by
    filter_upwards [hsl.eventually (lt_mem_nhds hd), self_mem_nhdsWithin] with x hx hxt
    have hxt' : 0 < x - t₀ := sub_pos.mpr hxt
    rw [slope_def_field, h0, sub_zero] at hx
    exact (div_pos_iff_of_pos_right hxt').mp hx
  obtain ⟨u, hu, hsub⟩ := mem_nhdsGT_iff_exists_Ioo_subset.mp hev
  have hu' : t₀ < u := hu
  set t₁ := (t₀ + u) / 2 with ht₁
  have h01 : t₀ < t₁ := by rw [ht₁]; linarith
  have h1u : t₁ < u := by rw [ht₁]; linarith
  have hmono : StrictMonoOn φ (Icc t₀ t₁) := by
    refine strictMonoOn_of_deriv_pos (convex_Icc _ _) ?_ ?_
    · exact fun x _ => (hφ x).continuousAt.continuousWithinAt
    · intro x hx
      rw [interior_Icc] at hx
      rw [(hφ x).deriv]
      exact hsub ⟨hx.1, lt_trans hx.2 h1u⟩
  exact ⟨t₁, hmono ⟨le_rfl, h01.le⟩ ⟨h01.le, le_rfl⟩ h01⟩

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- **Proposicao `prop:ball_bound`, caso `k = 1`** (ver a reducao declarada no cabecalho):
uma curva fechada (periodica), parametrizada por comprimento de arco, duas vezes
diferenciavel, com curvatura `‖f''‖ ≤ κ`, contida na bola fechada de raio `R`, tem `κR ≥ 1`. -/
theorem ball_bound (f f' f'' : ℝ → E) (T κ R : ℝ) (c : E) (hT : 0 < T)
    (hper : Function.Periodic f T)
    (hf : ∀ t, HasDerivAt f (f' t) t) (hf' : ∀ t, HasDerivAt f' (f'' t) t)
    (hunit : ∀ t, ‖f' t‖ = 1) (hcurv : ∀ t, ‖f'' t‖ ≤ κ)
    (hball : ∀ t, f t ∈ Metric.closedBall c R) : 1 ≤ κ * R := by
  -- g = f - c, φ = ⟪g, g⟫, ψ = φ'
  set g : ℝ → E := fun t => f t - c with hg
  have hgd : ∀ t, HasDerivAt g (f' t) t := fun t => (hf t).sub_const c
  set φ : ℝ → ℝ := fun t => inner ℝ (g t) (g t) with hφdef
  set ψ : ℝ → ℝ := fun t => inner ℝ (g t) (f' t) + inner ℝ (f' t) (g t) with hψdef
  have hφ : ∀ t, HasDerivAt φ (ψ t) t := fun t => (hgd t).inner ℝ (hgd t)
  have hψ : ∀ t, HasDerivAt ψ ((inner ℝ (g t) (f'' t) + inner ℝ (f' t) (f' t)) +
      (inner ℝ (f' t) (f' t) + inner ℝ (f'' t) (g t))) t :=
    fun t => ((hgd t).inner ℝ (hf' t)).add ((hf' t).inner ℝ (hgd t))
  -- φ periodica, logo seu maximo em [0,T] e global
  have hφper : Function.Periodic φ T := by
    intro t; simp only [hφdef, hg, hper t]
  have hφc : Continuous φ := continuous_iff_continuousAt.mpr fun t => (hφ t).continuousAt
  obtain ⟨t₀, -, ht₀⟩ := (isCompact_Icc (a := (0:ℝ)) (b := T)).exists_isMaxOn
    (nonempty_Icc.mpr hT.le) hφc.continuousOn
  have hmax : ∀ t, φ t ≤ φ t₀ := by
    intro t
    obtain ⟨y, hy, hyt⟩ := hφper.exists_mem_Ico₀ hT t
    rw [hyt]; exact ht₀ (Ico_subset_Icc_self hy)
  -- primeira ordem: ψ(t₀) = 0
  have hlocal : IsLocalMax φ t₀ := Filter.Eventually.of_forall hmax
  have hψ0 : ψ t₀ = 0 := IsLocalMax.hasDerivAt_eq_zero hlocal (hφ t₀)
  -- segunda ordem: ψ'(t₀) ≤ 0
  have hd : (inner ℝ (g t₀) (f'' t₀) + inner ℝ (f' t₀) (f' t₀)) +
      (inner ℝ (f' t₀) (f' t₀) + inner ℝ (f'' t₀) (g t₀)) ≤ 0 := by
    by_contra hpos
    obtain ⟨t, ht⟩ := not_isMax_of_deriv_pos φ ψ t₀ _ hφ (hψ t₀) hψ0 (lt_of_not_ge hpos)
    exact absurd (hmax t) (not_le.mpr ht)
  rw [real_inner_comm (f'' t₀) (g t₀), real_inner_self_eq_norm_sq, hunit t₀] at hd
  -- Cauchy-Schwarz
  have hcs : -inner ℝ (f'' t₀) (g t₀) ≤ ‖g t₀‖ * ‖f'' t₀‖ := by
    have := real_inner_le_norm (g t₀) (-f'' t₀)
    rwa [inner_neg_right, norm_neg, real_inner_comm] at this
  have hgR : ‖g t₀‖ ≤ R := by
    have := hball t₀
    rwa [Metric.mem_closedBall, dist_eq_norm] at this
  have hR : 0 ≤ R := le_trans (norm_nonneg _) hgR
  have h2 : ‖g t₀‖ * ‖f'' t₀‖ ≤ R * κ :=
    mul_le_mul hgR (hcurv t₀) (norm_nonneg _) hR
  linarith

/-- O mesmo enunciado em `ℝⁿ = EuclideanSpace ℝ (Fin n)`, a forma literal do livro. -/
theorem ball_bound_euclidean (n : ℕ) (f f' f'' : ℝ → EuclideanSpace ℝ (Fin n))
    (T κ R : ℝ) (c : EuclideanSpace ℝ (Fin n)) (hT : 0 < T) (hper : Function.Periodic f T)
    (hf : ∀ t, HasDerivAt f (f' t) t) (hf' : ∀ t, HasDerivAt f' (f'' t) t)
    (hunit : ∀ t, ‖f' t‖ = 1) (hcurv : ∀ t, ‖f'' t‖ ≤ κ)
    (hball : ∀ t, f t ∈ Metric.closedBall c R) : 1 ≤ κ * R :=
  ball_bound f f' f'' T κ R c hT hper hf hf' hunit hcurv hball

/-! ## Testemunha de nao-vacuidade: o circulo unitario (igualdade `κR = 1`)

O plano `ℝ²` e representado por `ℂ`, visto como espaco com produto interno REAL. -/

open Complex in
/-- Circulo unitario `t ↦ e^{it}`. -/
def circ (t : ℝ) : ℂ := exp (t * I)

open Complex in
theorem circ_hasDerivAt (t : ℝ) : HasDerivAt circ (circ t * I) t := by
  have h : HasDerivAt (fun s : ℝ => (s : ℂ) * I) (1 * I) t :=
    (hasDerivAt_id t).ofReal_comp.mul_const I
  have h2 := h.cexp
  simp only [one_mul] at h2
  exact h2

theorem circ'_hasDerivAt (t : ℝ) :
    HasDerivAt (fun s => circ s * Complex.I) (circ t * Complex.I * Complex.I) t :=
  (circ_hasDerivAt t).mul_const Complex.I

theorem circ_norm (t : ℝ) : ‖circ t‖ = 1 := Complex.norm_exp_ofReal_mul_I t

theorem circ_periodic : Function.Periodic circ (2 * Real.pi) := by
  intro t
  simp only [circ]
  rw [show ((t + 2 * Real.pi : ℝ) : ℂ) * Complex.I = t * Complex.I + 2 * Real.pi * Complex.I by
    push_cast; ring, Complex.exp_add, Complex.exp_two_pi_mul_I, mul_one]

/-- Todas as hipoteses de `ball_bound` valem para o circulo unitario com `κ = R = 1`, e a
conclusao vale com igualdade (`κR = 1`): o enunciado nao e vacuo e e otimo. -/
theorem witness_unit_circle :
    (0 : ℝ) < 2 * Real.pi ∧ Function.Periodic circ (2 * Real.pi) ∧
    (∀ t, HasDerivAt circ (circ t * Complex.I) t) ∧
    (∀ t, HasDerivAt (fun s => circ s * Complex.I) (circ t * Complex.I * Complex.I) t) ∧
    (∀ t, ‖circ t * Complex.I‖ = 1) ∧ (∀ t, ‖circ t * Complex.I * Complex.I‖ ≤ 1) ∧
    (∀ t, circ t ∈ Metric.closedBall (0 : ℂ) 1) ∧ (1 : ℝ) * 1 = 1 := by
  refine ⟨by positivity, circ_periodic, circ_hasDerivAt, circ'_hasDerivAt, ?_, ?_, ?_, by norm_num⟩
  · intro t; rw [norm_mul, circ_norm, Complex.norm_I, mul_one]
  · intro t; rw [norm_mul, norm_mul, circ_norm, Complex.norm_I]; norm_num
  · intro t; rw [mem_closedBall_zero_iff, circ_norm]

/-- Aplicacao do teorema a testemunha (checa que os tipos casam). -/
example : (1 : ℝ) ≤ 1 * 1 := by
  obtain ⟨hT, hp, h1, h2, h3, h4, h5, -⟩ := witness_unit_circle
  exact ball_bound circ (fun s => circ s * Complex.I) (fun s => circ s * Complex.I * Complex.I)
    (2 * Real.pi) 1 1 0 hT hp h1 h2 h3 h4 h5

/-! ## Mutantes provados FALSOS -/

/-- Mutante 1 (conclusao estrita `1 < κR`): falso, pelo circulo unitario. -/
theorem mutant_strict_false :
    ¬ (∀ (f f' f'' : ℝ → ℂ) (T κ R : ℝ) (c : ℂ), 0 < T → Function.Periodic f T →
        (∀ t, HasDerivAt f (f' t) t) → (∀ t, HasDerivAt f' (f'' t) t) →
        (∀ t, ‖f' t‖ = 1) → (∀ t, ‖f'' t‖ ≤ κ) →
        (∀ t, f t ∈ Metric.closedBall c R) → 1 < κ * R) := by
  intro h
  obtain ⟨hT, hp, h1, h2, h3, h4, h5, -⟩ := witness_unit_circle
  have := h circ (fun s => circ s * Complex.I) (fun s => circ s * Complex.I * Complex.I)
    (2 * Real.pi) 1 1 0 hT hp h1 h2 h3 h4 h5
  norm_num at this

/-- Mutante 2 (sem a hipotese de curva FECHADA: arco num intervalo `[0, ℓ]`): falso, pelo
segmento `t ↦ t` em `[0,1]`, com `κ = 0` e a bola de centro `1/2` e raio `1/2`. -/
theorem mutant_open_arc_false :
    ¬ (∀ (f f' f'' : ℝ → ℂ) (ℓ κ R : ℝ) (c : ℂ), 0 < ℓ →
        (∀ t ∈ Icc 0 ℓ, HasDerivAt f (f' t) t) → (∀ t ∈ Icc 0 ℓ, HasDerivAt f' (f'' t) t) →
        (∀ t ∈ Icc 0 ℓ, ‖f' t‖ = 1) → (∀ t ∈ Icc 0 ℓ, ‖f'' t‖ ≤ κ) →
        (∀ t ∈ Icc 0 ℓ, f t ∈ Metric.closedBall c R) → 1 ≤ κ * R) := by
  intro h
  have := h (fun t => (t : ℂ)) (fun _ => 1) (fun _ => 0) 1 0 (1 / 2) ((1 / 2 : ℝ) : ℂ)
    one_pos
    (fun t _ => by simpa using (hasDerivAt_id t).ofReal_comp)
    (fun t _ => hasDerivAt_const t (1 : ℂ))
    (fun t _ => by simp)
    (fun t _ => by simp)
    (fun t ht => by
      rw [Metric.mem_closedBall, dist_eq_norm, ← Complex.ofReal_sub, Complex.norm_real,
        Real.norm_eq_abs, abs_le]
      constructor <;> linarith [ht.1, ht.2])
  norm_num at this

end LeanReal.Chap07BallBound

#print axioms LeanReal.Chap07BallBound.not_isMax_of_deriv_pos
#print axioms LeanReal.Chap07BallBound.ball_bound
#print axioms LeanReal.Chap07BallBound.ball_bound_euclidean
#print axioms LeanReal.Chap07BallBound.witness_unit_circle
#print axioms LeanReal.Chap07BallBound.mutant_strict_false
#print axioms LeanReal.Chap07BallBound.mutant_open_arc_false
