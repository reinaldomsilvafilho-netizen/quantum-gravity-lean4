import LeanReal.Chap02Heat
import LeanReal.Chap02Flows

/-!
# L2 of batch LIVRO_A_B2: extra mutants and the complex projector

Independent L2 reviewer.

* `mutant_jump_no_degree_false`: without equal degrees, the jump law of `heat_jump` fails.
* `mutant_unique_no_initial_false`: without the initial condition, `heat_unique` fails.
* `community_exceeds_one`: item (ii) of `thm:ricci_neckpinch` in the book's words: with
  `c₁ > 0`, the community entry leaves `[0,1]` for every `t ∈ (0,T)`.
* `witness_community`: non-constant curvature `k = 1 + t` for `ricci_neckpinch_community`.
* `mutant_community_no_curvature_false`: without `k ≥ c₁`, item (ii) fails.
* `projC`, `energy_decrease_complex`: `thm:cmps_energy_flow`(ii) with the book's COMPLEX
  projector `x ↦ x − ⟨ψ|x⟩ψ` on a complex inner product space and a complex-linear hermitian
  `H`. The writer's `energy_decrease` uses `proj0 ψ x = x − Re⟨ψ|x⟩ψ`, which equals the book's
  projector only in a real Hilbert space; `projC_phase` and `proj0_phase` show the difference
  (the phase direction `iψ` is killed by `projC`, not by `proj0`).
-/

noncomputable section

namespace LeanReal.L2_LIVRO_A_B2_Extra

open Real Set Filter Matrix

/-! ## Heat equation on the finite grid -/

section HeatExtra

open LeanReal.Chap02Heat

/-- Mutant of `heat_jump`: without equal row and column averages at the two cells, the jump of
`W(t)` is NOT `e^{−2t}` times the jump of `W₀` (`Wex`, cells `(0,0)` and `(1,1)`, `t = log 2`:
`1/2` against `1/4`). -/
theorem mutant_jump_no_degree_false :
    ¬ ∀ (W0 : Matrix (Fin 2) (Fin 2) ℝ) (t : ℝ) (i j i' j' : Fin 2),
      heat W0 t i j - heat W0 t i' j' = exp (-2 * t) * (W0 i j - W0 i' j') := by
  intro h
  have := h Wex (log 2) 0 0 1 1
  rw [witness_heat_log_two, exp_neg_two_log_two] at this
  simp [Wex] at this
  norm_num at this

/-- Mutant of `heat_unique`: without `X 0 = W₀`, a global solution need not be `heat W₀`
(`X = heat (const 1)`, `W₀ = Wex`, entry `(1,1)` at `t = 0`). -/
theorem mutant_unique_no_initial_false :
    ¬ ∀ (W0 : Matrix (Fin 2) (Fin 2) ℝ) (X : ℝ → Fin 2 → Fin 2 → ℝ),
      (∀ t, HasDerivAt X (lapT (X t)) t) → ∀ t, X t = heat W0 t := by
  intro h
  have h1 := h Wex (fun s => (heat (const 1 : Matrix (Fin 2) (Fin 2) ℝ) s : Fin 2 → Fin 2 → ℝ))
    (fun t => heat_hasDerivAt_pi _ t) 0
  have h2 := congrFun (congrFun h1 1) 1
  simp only [heat_zero] at h2
  simp [Wex, const] at h2

end HeatExtra

/-! ## Ricci flow as a scalar ODE -/

section RicciExtra

open LeanReal.Chap02Flows

/-- `thm:ricci_neckpinch`(ii), last clause: with `c₁ > 0` the community entry exceeds `1` for
every `t ∈ (0,T)`, so the unnormalized flow does not preserve `[0,1]`-valued graphons. -/
theorem community_exceeds_one (W k : ℝ → ℝ) (T c₁ : ℝ) (hc1 : 0 < c₁) (hk : Continuous k)
    (hWc : ContinuousOn W (Ico 0 T)) (hW : ∀ t ∈ Ioo 0 T, HasDerivAt W (2 * k t * W t) t)
    (hW0 : W 0 = 1) (hc : ∀ s ∈ Ico 0 T, c₁ ≤ k s) {t : ℝ} (ht : t ∈ Ioo 0 T) :
    1 < W t := by
  have h := ricci_neckpinch_community W k T c₁ hk hWc hW hW0 hc ⟨ht.1.le, ht.2⟩
  have h1 : 1 < exp (2 * c₁ * t) := by
    rw [← exp_zero]; exact exp_lt_exp.2 (by nlinarith [ht.1])
  linarith

/-- Witness with non-constant curvature: `k(t) = 1 + t`, `W(t) = e^{2t + t²}`, `c₁ = 1`,
`T = 1`. -/
theorem witness_community :
    ∀ t ∈ Ico (0 : ℝ) 1, exp (2 * 1 * t) ≤ exp (2 * t + t ^ 2) := by
  have hd : ∀ t : ℝ, HasDerivAt (fun s : ℝ => exp (2 * s + s ^ 2))
      (2 * (1 + t) * exp (2 * t + t ^ 2)) t := by
    intro t
    have h : HasDerivAt (fun s : ℝ => 2 * s + s ^ 2) (2 * 1 + ((2 : ℕ) : ℝ) * t ^ (2 - 1)) t :=
      ((hasDerivAt_id t).const_mul (2 : ℝ)).add (hasDerivAt_pow 2 t)
    refine h.exp.congr_deriv ?_
    simp only [Nat.cast_ofNat]
    ring
  intro t ht
  exact ricci_neckpinch_community (fun s => exp (2 * s + s ^ 2)) (fun s => 1 + s) 1 1
    (by fun_prop) (by fun_prop) (fun t _ => hd t) (by simp)
    (fun s hs => by linarith [hs.1]) ht

/-- Mutant of `ricci_neckpinch_community`: without the curvature bound `k ≥ c₁` the growth
bound fails (`k ≡ −1`, `W = e^{−2t}`, `c₁ = 0`, `t = 1`). -/
theorem mutant_community_no_curvature_false :
    ¬ ∀ (W k : ℝ → ℝ) (T c₁ : ℝ), Continuous k → ContinuousOn W (Ico 0 T) →
      (∀ t ∈ Ioo 0 T, HasDerivAt W (2 * k t * W t) t) → W 0 = 1 →
      ∀ t ∈ Ico 0 T, exp (2 * c₁ * t) ≤ W t := by
  intro h
  have hd : ∀ t : ℝ, HasDerivAt (fun s : ℝ => exp (-2 * s)) (2 * (-1) * exp (-2 * t)) t := by
    intro t
    have := ((hasDerivAt_id t).const_mul (-2 : ℝ)).exp
    refine this.congr_deriv ?_
    simp only [id]
    ring
  have := h (fun s => exp (-2 * s)) (fun _ => -1) 2 0 continuous_const (by fun_prop)
    (fun t _ => hd t) (by simp) 1 (by norm_num)
  have he : exp (-2 * 1 : ℝ) < 1 := exp_lt_one_iff.2 (by norm_num)
  simp only [mul_zero, zero_mul, exp_zero] at this
  linarith

end RicciExtra

/-! ## McLachlan flow with the complex projector -/

section ComplexProjector

open LeanReal.Chap02Flows ComplexConjugate

attribute [local instance] InnerProductSpace.complexToReal

variable {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℂ F] {d : ℕ}

/-- The book's projector `Id − |ψ⟩⟨ψ|` on a complex inner product space. -/
def projC (ψ x : F) : F := x - (inner ℂ ψ x) • ψ

lemma real_inner_eq_re (x y : F) : inner ℝ x y = (inner ℂ x y).re := rfl

/-- For a hermitian `H` and a unit vector `ψ`, `(H − E)ψ` is complex-orthogonal to `ψ`. -/
lemma inner_C_resid (H : F →L[ℂ] F) (hH : ∀ x y, inner ℂ (H x) y = inner ℂ x (H y))
    (ψ : F) (hψ : ‖ψ‖ = 1) : inner ℂ ψ (resid (H.restrictScalars ℝ) ψ) = 0 := by
  have hreal : conj (inner ℂ ψ (H ψ)) = inner ℂ ψ (H ψ) := by
    rw [inner_conj_symm, hH]
  have hre := Complex.conj_eq_iff_re.1 hreal
  have hpp : inner ℂ ψ ψ = (1 : ℂ) := by
    rw [inner_self_eq_norm_sq_to_K, hψ]; norm_num
  simp only [resid, ContinuousLinearMap.coe_restrictScalars']
  rw [inner_sub_right, RCLike.real_smul_eq_coe_smul (K := ℂ), inner_smul_right, hpp, mul_one,
    real_inner_eq_re]
  exact sub_eq_zero.2 hre.symm

lemma inner_projC_resid (H : F →L[ℂ] F) (hH : ∀ x y, inner ℂ (H x) y = inner ℂ x (H y))
    (ψ x : F) (hψ : ‖ψ‖ = 1) :
    inner ℝ (projC ψ x) (resid (H.restrictScalars ℝ) ψ)
      = inner ℝ x (resid (H.restrictScalars ℝ) ψ) := by
  rw [real_inner_eq_re, real_inner_eq_re, projC, inner_sub_left, inner_smul_left,
    inner_C_resid H hH ψ hψ, mul_zero, sub_zero]

/-- **`thm:cmps_energy_flow`(ii) with the book's complex projector**: on a complex inner
product space with a bounded complex-linear hermitian `H`, if the unit curve's velocity is
`∑ θ̇^α v_α` and `θ̇` solves the normal equations for `u_α = (Id − |Φ⟩⟨Φ|) v_α`,
`w = (H − E)Φ`, then `d⟨H⟩/dτ = −2 θ̇ᵀ g θ̇` with `g_{αβ} = Re⟨u_α|u_β⟩`. -/
theorem energy_decrease_complex (H : F →L[ℂ] F)
    (hH : ∀ x y, inner ℂ (H x) y = inner ℂ x (H y))
    (Φ : ℝ → F) (τ : ℝ) (v : Fin d → F) (θ' : Fin d → ℝ)
    (hΦ : HasDerivAt Φ (vel v θ') τ) (hnorm : ∀ s, ‖Φ s‖ = 1)
    (hnormal : gram (fun a => projC (Φ τ) (v a)) *ᵥ θ'
      = -(rhs (fun a => projC (Φ τ) (v a)) (resid (H.restrictScalars ℝ) (Φ τ)))) :
    HasDerivAt (fun s => inner ℝ (Φ s) (H (Φ s)))
      (-2 * (θ' ⬝ᵥ (gram (fun a => projC (Φ τ) (v a)) *ᵥ θ'))) τ := by
  have hHR : ∀ x y, inner ℝ (H.restrictScalars ℝ x) y = inner ℝ x (H.restrictScalars ℝ y) := by
    intro x y
    simp only [ContinuousLinearMap.coe_restrictScalars', real_inner_eq_re, hH]
  refine (energy_deriv (H.restrictScalars ℝ) hHR Φ (vel v θ') τ hΦ hnorm).congr_deriv ?_
  rw [hnormal, dotProduct_neg, dot_rhs, inner_vel_left, inner_vel_left]
  simp only [inner_projC_resid H hH (Φ τ) _ (hnorm τ)]
  ring

/-- The phase direction `iψ` lies in the kernel of the book's projector. -/
lemma projC_phase (ψ : F) (hψ : ‖ψ‖ = 1) : projC ψ (Complex.I • ψ) = 0 := by
  have hpp : inner ℂ ψ ψ = (1 : ℂ) := by
    rw [inner_self_eq_norm_sq_to_K, hψ]; norm_num
  rw [projC, inner_smul_right, hpp, mul_one, sub_self]

/-- The writer's real projector `proj0` does NOT kill the phase direction: on `ℂ`,
`proj0 1 i = i ≠ 0`. -/
lemma proj0_phase : proj0 (1 : ℂ) (Complex.I • (1 : ℂ)) = Complex.I := by
  simp [proj0, Complex.inner]

end ComplexProjector

end LeanReal.L2_LIVRO_A_B2_Extra

#print axioms LeanReal.L2_LIVRO_A_B2_Extra.mutant_jump_no_degree_false
#print axioms LeanReal.L2_LIVRO_A_B2_Extra.mutant_unique_no_initial_false
#print axioms LeanReal.L2_LIVRO_A_B2_Extra.community_exceeds_one
#print axioms LeanReal.L2_LIVRO_A_B2_Extra.witness_community
#print axioms LeanReal.L2_LIVRO_A_B2_Extra.mutant_community_no_curvature_false
#print axioms LeanReal.L2_LIVRO_A_B2_Extra.energy_decrease_complex
#print axioms LeanReal.L2_LIVRO_A_B2_Extra.projC_phase
#print axioms LeanReal.L2_LIVRO_A_B2_Extra.proj0_phase
