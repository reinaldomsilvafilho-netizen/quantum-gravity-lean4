import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.SpecialFunctions.ExpDeriv

/-!
# Book (Zenodo concept DOI 10.5281/zenodo.22290043), chapter 5, coupled 3D–2D–1D system

Source: `unified_quantum_gravity_book/chap05_interdimensional_transforms_barnes_lie.tex`,
Definition "Coupled Inter-Dimensional Transport System" (eq. `eq:coupled_system`, interface
condition `eq:interface_condition`) and Proposition "Conservation of Total Mass and Energy
Dissipation; formal computation" (no label):
> `∂ₜu = Δu − E(λ(Ru − v))`, `∂ₜv = Δ_Γ v + λ(Ru − v) − F(κ(Sv − w))`, `∂ₜw = ∂²w + κ(Sv − w)`,
> with `E = R*`, `F = S*`, `R𝟏_Ω = 1` on `Γ`, Neumann conditions. For a smooth solution:
> (1) `∫u + ∫v + ∫w` is constant for `t ≥ 0`;
> (2) `dℰ/dt = −‖∇u‖² − ‖∇_Γ v‖² − ‖∂_z w‖² − λ‖Ru − v‖² − κ‖Sv − w‖² ≤ 0`,
>     `ℰ = ½‖u‖² + ½‖v‖² + ½‖w‖²`.

Formal version (declared reduction): ABSTRACT real inner product spaces `Hb, Hg, Hs` in place of
`L²(Ω), L²(Γ), L²(Σ)`; integrals `∫u` are `⟪u, 𝟙⟫` for given vectors `𝟙Ω, 𝟙Γ, 𝟙Σ`; `R, E, S, F`
and the three Laplacians are linear maps. Every analytic fact the book uses enters as an
explicit named hypothesis:
* `hNb, hNg, hNs` : `⟪L x, 𝟙⟫ = 0` ("the Laplacian terms integrate to zero by Neumann");
* `hGb, hGg, hGs` : `⟪x, L x⟫ = −‖G x‖²` (Green's identity under Neumann, `G` the gradient);
* `hRE, hSF` : `⟪x, E φ⟫ = ⟪R x, φ⟫`, `⟪y, F ψ⟫ = ⟪S y, ψ⟫` (the book's exact adjoint relation);
* `hR1, hS1` : `R 𝟙Ω = 𝟙Γ`, `S 𝟙Γ = 𝟙Σ` (consequence of the interface condition);
* `0 ≤ λ, 0 ≤ κ` only for the sign in (2) (the book assumes `λ, κ > 0`).
Results:
* `mass_flux_zero`, `energy_flux` : the two algebraic identities on the vector field;
* `mass_conserved` : `M(t) = M(0)` for `t ≥ 0`, for any solution differentiable on `[0, ∞)`;
* `energy_hasDerivAt`, `energy_antitone` : the book's formula for `dℰ/dt` and monotonicity.
NOT covered: the real trace and extension operators, the interface condition itself, the
Laplacians on domains, Green's formula, existence and regularity of solutions.
-/

namespace LeanReal.Chap05Coupled

open Set

variable {Hb Hg Hs Vb Vg Vs : Type*}
  [NormedAddCommGroup Hb] [InnerProductSpace ℝ Hb]
  [NormedAddCommGroup Hg] [InnerProductSpace ℝ Hg]
  [NormedAddCommGroup Hs] [InnerProductSpace ℝ Hs]
  [NormedAddCommGroup Vb] [NormedAddCommGroup Vg] [NormedAddCommGroup Vs]

/-- Bulk equation of `eq:coupled_system`: `u' = Δu − E(λ(Ru − v))`. -/
def fieldU (Lb : Hb →ₗ[ℝ] Hb) (R : Hb →ₗ[ℝ] Hg) (E : Hg →ₗ[ℝ] Hb) (lam : ℝ)
    (u : Hb) (v : Hg) : Hb :=
  Lb u - E (lam • (R u - v))

/-- Interface equation of `eq:coupled_system`:
`v' = Δ_Γ v + λ(Ru − v) − F(κ(Sv − w))`. -/
def fieldV (Lg : Hg →ₗ[ℝ] Hg) (R : Hb →ₗ[ℝ] Hg) (S : Hg →ₗ[ℝ] Hs) (F : Hs →ₗ[ℝ] Hg)
    (lam kap : ℝ) (u : Hb) (v : Hg) (w : Hs) : Hg :=
  Lg v + lam • (R u - v) - F (kap • (S v - w))

/-- Filament equation of `eq:coupled_system`: `w' = ∂²w + κ(Sv − w)`. -/
def fieldW (Ls : Hs →ₗ[ℝ] Hs) (S : Hg →ₗ[ℝ] Hs) (kap : ℝ) (v : Hg) (w : Hs) : Hs :=
  Ls w + kap • (S v - w)

/-- Mass flux: `⟪u', 𝟙Ω⟫ + ⟪v', 𝟙Γ⟫ + ⟪w', 𝟙Σ⟫ = 0` at every state, under the Neumann
hypotheses, the adjoint relations and `R𝟙Ω = 𝟙Γ`, `S𝟙Γ = 𝟙Σ` (proof of item 1). -/
theorem mass_flux_zero (Lb : Hb →ₗ[ℝ] Hb) (Lg : Hg →ₗ[ℝ] Hg) (Ls : Hs →ₗ[ℝ] Hs)
    (R : Hb →ₗ[ℝ] Hg) (E : Hg →ₗ[ℝ] Hb) (S : Hg →ₗ[ℝ] Hs) (F : Hs →ₗ[ℝ] Hg)
    (oneb : Hb) (oneg : Hg) (ones : Hs) (lam kap : ℝ)
    (hNb : ∀ x, inner ℝ (Lb x) oneb = 0) (hNg : ∀ y, inner ℝ (Lg y) oneg = 0)
    (hNs : ∀ z, inner ℝ (Ls z) ones = 0)
    (hRE : ∀ x φ, inner ℝ x (E φ) = inner ℝ (R x) φ)
    (hSF : ∀ y ψ, inner ℝ y (F ψ) = inner ℝ (S y) ψ)
    (hR1 : R oneb = oneg) (hS1 : S oneg = ones)
    (u : Hb) (v : Hg) (w : Hs) :
    inner ℝ (fieldU Lb R E lam u v) oneb + inner ℝ (fieldV Lg R S F lam kap u v w) oneg
      + inner ℝ (fieldW Ls S kap v w) ones = 0 := by
  have hE : ∀ φ, inner ℝ (E φ) oneb = inner ℝ φ oneg := fun φ => by
    rw [real_inner_comm, hRE, hR1, real_inner_comm]
  have hF : ∀ ψ, inner ℝ (F ψ) oneg = inner ℝ ψ ones := fun ψ => by
    rw [real_inner_comm, hSF, hS1, real_inner_comm]
  simp only [fieldU, fieldV, fieldW, inner_sub_left, inner_add_left, hE, hF, hNb, hNg, hNs]
  ring

/-- Energy flux: `⟪u, u'⟫ + ⟪v, v'⟫ + ⟪w, w'⟫
= −‖Gb u‖² − ‖Gg v‖² − ‖Gs w‖² − λ‖Ru − v‖² − κ‖Sv − w‖²` (proof of item 2). -/
theorem energy_flux (Lb : Hb →ₗ[ℝ] Hb) (Lg : Hg →ₗ[ℝ] Hg) (Ls : Hs →ₗ[ℝ] Hs)
    (R : Hb →ₗ[ℝ] Hg) (E : Hg →ₗ[ℝ] Hb) (S : Hg →ₗ[ℝ] Hs) (F : Hs →ₗ[ℝ] Hg)
    (Gb : Hb → Vb) (Gg : Hg → Vg) (Gs : Hs → Vs) (lam kap : ℝ)
    (hGb : ∀ x, inner ℝ x (Lb x) = -‖Gb x‖ ^ 2) (hGg : ∀ y, inner ℝ y (Lg y) = -‖Gg y‖ ^ 2)
    (hGs : ∀ z, inner ℝ z (Ls z) = -‖Gs z‖ ^ 2)
    (hRE : ∀ x φ, inner ℝ x (E φ) = inner ℝ (R x) φ)
    (hSF : ∀ y ψ, inner ℝ y (F ψ) = inner ℝ (S y) ψ)
    (u : Hb) (v : Hg) (w : Hs) :
    inner ℝ u (fieldU Lb R E lam u v) + inner ℝ v (fieldV Lg R S F lam kap u v w)
      + inner ℝ w (fieldW Ls S kap v w)
      = -‖Gb u‖ ^ 2 - ‖Gg v‖ ^ 2 - ‖Gs w‖ ^ 2 - lam * ‖R u - v‖ ^ 2
        - kap * ‖S v - w‖ ^ 2 := by
  have h1 : ‖R u - v‖ ^ 2 = inner ℝ (R u) (R u) - inner ℝ (R u) v - inner ℝ v (R u)
      + inner ℝ v v := by
    rw [← real_inner_self_eq_norm_sq, inner_sub_left, inner_sub_right, inner_sub_right]; ring
  have h2 : ‖S v - w‖ ^ 2 = inner ℝ (S v) (S v) - inner ℝ (S v) w - inner ℝ w (S v)
      + inner ℝ w w := by
    rw [← real_inner_self_eq_norm_sq, inner_sub_left, inner_sub_right, inner_sub_right]; ring
  simp only [fieldU, fieldV, fieldW, inner_sub_right, inner_add_right, hRE, hSF,
    real_inner_smul_right, hGb, hGg, hGs]
  linear_combination lam * h1 + kap * h2

/-- Item 1 of the Proposition, integrated: the total mass
`M(t) = ⟪u t, 𝟙Ω⟫ + ⟪v t, 𝟙Γ⟫ + ⟪w t, 𝟙Σ⟫` satisfies `M(t) = M(0)` for all `t ≥ 0`, for any
solution of `eq:coupled_system` that is differentiable at every `t ≥ 0`. -/
theorem mass_conserved (Lb : Hb →ₗ[ℝ] Hb) (Lg : Hg →ₗ[ℝ] Hg) (Ls : Hs →ₗ[ℝ] Hs)
    (R : Hb →ₗ[ℝ] Hg) (E : Hg →ₗ[ℝ] Hb) (S : Hg →ₗ[ℝ] Hs) (F : Hs →ₗ[ℝ] Hg)
    (oneb : Hb) (oneg : Hg) (ones : Hs) (lam kap : ℝ)
    (hNb : ∀ x, inner ℝ (Lb x) oneb = 0) (hNg : ∀ y, inner ℝ (Lg y) oneg = 0)
    (hNs : ∀ z, inner ℝ (Ls z) ones = 0)
    (hRE : ∀ x φ, inner ℝ x (E φ) = inner ℝ (R x) φ)
    (hSF : ∀ y ψ, inner ℝ y (F ψ) = inner ℝ (S y) ψ)
    (hR1 : R oneb = oneg) (hS1 : S oneg = ones)
    (u : ℝ → Hb) (v : ℝ → Hg) (w : ℝ → Hs)
    (hu : ∀ t, 0 ≤ t → HasDerivAt u (fieldU Lb R E lam (u t) (v t)) t)
    (hv : ∀ t, 0 ≤ t → HasDerivAt v (fieldV Lg R S F lam kap (u t) (v t) (w t)) t)
    (hw : ∀ t, 0 ≤ t → HasDerivAt w (fieldW Ls S kap (v t) (w t)) t) :
    ∀ t, 0 ≤ t → inner ℝ (u t) oneb + inner ℝ (v t) oneg + inner ℝ (w t) ones
      = inner ℝ (u 0) oneb + inner ℝ (v 0) oneg + inner ℝ (w 0) ones := by
  set M : ℝ → ℝ := fun t => inner ℝ (u t) oneb + inner ℝ (v t) oneg + inner ℝ (w t) ones
    with hMdef
  have hM : ∀ t, 0 ≤ t → HasDerivAt M 0 t := by
    intro t ht
    have h := (((hu t ht).inner ℝ (hasDerivAt_const t oneb)).add
      ((hv t ht).inner ℝ (hasDerivAt_const t oneg))).add
      ((hw t ht).inner ℝ (hasDerivAt_const t ones))
    convert h using 1
    simp only [inner_zero_right, zero_add]
    rw [mass_flux_zero Lb Lg Ls R E S F oneb oneg ones lam kap hNb hNg hNs hRE hSF hR1 hS1]
  intro t ht
  have hcont : ContinuousOn M (Icc 0 t) := fun x hx =>
    (hM x hx.1).continuousAt.continuousWithinAt
  have hderiv : ∀ x ∈ Ico (0 : ℝ) t, HasDerivWithinAt M 0 (Ici x) x := fun x hx =>
    (hM x hx.1).hasDerivWithinAt
  exact constant_of_has_deriv_right_zero hcont hderiv t ⟨ht, le_rfl⟩

/-- Item 2 of the Proposition: `ℰ(t) = ½‖u‖² + ½‖v‖² + ½‖w‖²` has derivative
`−‖Gb u‖² − ‖Gg v‖² − ‖Gs w‖² − λ‖Ru − v‖² − κ‖Sv − w‖²` at every `t ≥ 0`. -/
theorem energy_hasDerivAt (Lb : Hb →ₗ[ℝ] Hb) (Lg : Hg →ₗ[ℝ] Hg) (Ls : Hs →ₗ[ℝ] Hs)
    (R : Hb →ₗ[ℝ] Hg) (E : Hg →ₗ[ℝ] Hb) (S : Hg →ₗ[ℝ] Hs) (F : Hs →ₗ[ℝ] Hg)
    (Gb : Hb → Vb) (Gg : Hg → Vg) (Gs : Hs → Vs) (lam kap : ℝ)
    (hGb : ∀ x, inner ℝ x (Lb x) = -‖Gb x‖ ^ 2) (hGg : ∀ y, inner ℝ y (Lg y) = -‖Gg y‖ ^ 2)
    (hGs : ∀ z, inner ℝ z (Ls z) = -‖Gs z‖ ^ 2)
    (hRE : ∀ x φ, inner ℝ x (E φ) = inner ℝ (R x) φ)
    (hSF : ∀ y ψ, inner ℝ y (F ψ) = inner ℝ (S y) ψ)
    (u : ℝ → Hb) (v : ℝ → Hg) (w : ℝ → Hs) (t : ℝ)
    (hu : HasDerivAt u (fieldU Lb R E lam (u t) (v t)) t)
    (hv : HasDerivAt v (fieldV Lg R S F lam kap (u t) (v t) (w t)) t)
    (hw : HasDerivAt w (fieldW Ls S kap (v t) (w t)) t) :
    HasDerivAt (fun s => ‖u s‖ ^ 2 / 2 + ‖v s‖ ^ 2 / 2 + ‖w s‖ ^ 2 / 2)
      (-‖Gb (u t)‖ ^ 2 - ‖Gg (v t)‖ ^ 2 - ‖Gs (w t)‖ ^ 2 - lam * ‖R (u t) - v t‖ ^ 2
        - kap * ‖S (v t) - w t‖ ^ 2) t := by
  have h := ((hu.norm_sq.div_const 2).add (hv.norm_sq.div_const 2)).add
    (hw.norm_sq.div_const 2)
  convert h using 1
  rw [← energy_flux Lb Lg Ls R E S F Gb Gg Gs lam kap hGb hGg hGs hRE hSF]
  ring

/-- Item 2, monotone form: for `λ, κ ≥ 0` the energy is non-increasing on `[0, ∞)`. -/
theorem energy_antitone (Lb : Hb →ₗ[ℝ] Hb) (Lg : Hg →ₗ[ℝ] Hg) (Ls : Hs →ₗ[ℝ] Hs)
    (R : Hb →ₗ[ℝ] Hg) (E : Hg →ₗ[ℝ] Hb) (S : Hg →ₗ[ℝ] Hs) (F : Hs →ₗ[ℝ] Hg)
    (Gb : Hb → Vb) (Gg : Hg → Vg) (Gs : Hs → Vs) (lam kap : ℝ)
    (hlam : 0 ≤ lam) (hkap : 0 ≤ kap)
    (hGb : ∀ x, inner ℝ x (Lb x) = -‖Gb x‖ ^ 2) (hGg : ∀ y, inner ℝ y (Lg y) = -‖Gg y‖ ^ 2)
    (hGs : ∀ z, inner ℝ z (Ls z) = -‖Gs z‖ ^ 2)
    (hRE : ∀ x φ, inner ℝ x (E φ) = inner ℝ (R x) φ)
    (hSF : ∀ y ψ, inner ℝ y (F ψ) = inner ℝ (S y) ψ)
    (u : ℝ → Hb) (v : ℝ → Hg) (w : ℝ → Hs)
    (hu : ∀ t, 0 ≤ t → HasDerivAt u (fieldU Lb R E lam (u t) (v t)) t)
    (hv : ∀ t, 0 ≤ t → HasDerivAt v (fieldV Lg R S F lam kap (u t) (v t) (w t)) t)
    (hw : ∀ t, 0 ≤ t → HasDerivAt w (fieldW Ls S kap (v t) (w t)) t) :
    AntitoneOn (fun s => ‖u s‖ ^ 2 / 2 + ‖v s‖ ^ 2 / 2 + ‖w s‖ ^ 2 / 2) (Ici 0) := by
  have hD : ∀ t, 0 ≤ t → HasDerivAt (fun s => ‖u s‖ ^ 2 / 2 + ‖v s‖ ^ 2 / 2 + ‖w s‖ ^ 2 / 2)
      (-‖Gb (u t)‖ ^ 2 - ‖Gg (v t)‖ ^ 2 - ‖Gs (w t)‖ ^ 2 - lam * ‖R (u t) - v t‖ ^ 2
        - kap * ‖S (v t) - w t‖ ^ 2) t := fun t ht =>
    energy_hasDerivAt Lb Lg Ls R E S F Gb Gg Gs lam kap hGb hGg hGs hRE hSF u v w t
      (hu t ht) (hv t ht) (hw t ht)
  refine antitoneOn_of_deriv_nonpos (convex_Ici 0) ?_ ?_ ?_
  · exact fun x hx => (hD x hx).continuousAt.continuousWithinAt
  · intro x hx
    rw [interior_Ici] at hx
    exact (hD x (le_of_lt hx)).differentiableAt.differentiableWithinAt
  · intro x hx
    rw [interior_Ici] at hx
    rw [(hD x (le_of_lt hx)).deriv]
    have := mul_nonneg hlam (sq_nonneg ‖R (u x) - v x‖)
    have := mul_nonneg hkap (sq_nonneg ‖S (v x) - w x‖)
    nlinarith [sq_nonneg ‖Gb (u x)‖, sq_nonneg ‖Gg (v x)‖, sq_nonneg ‖Gs (w x)‖]

/-! ## Non-vacuity witness: the scalar chain `Ω = Γ = Σ = ℝ`, `R = E = S = F = id`,
`L = 0`, `G = 0`, `𝟙 = 1`, `λ = κ = 1`. The system is `u' = −(u − v)`,
`v' = (u − v) − (v − w)`, `w' = v − w`, with explicit solution
`u = 1 + e^{−t}`, `v = 1`, `w = 1 − e^{−t}`. The masses of `u` and `w` change, the total mass
`3` does not, and the energy `(3 + 2e^{−2t})/2` strictly decreases: the hypotheses bite. -/

/-- The identity map on `ℝ`, as a linear map. -/
abbrev idR : ℝ →ₗ[ℝ] ℝ := LinearMap.id

lemma idR_adj : ∀ x φ : ℝ, inner ℝ x (idR φ) = inner ℝ (idR x) φ := fun _ _ => rfl

/-- Witness solution, bulk component. -/
noncomputable def uW (t : ℝ) : ℝ := 1 + Real.exp (-t)
/-- Witness solution, filament component. -/
noncomputable def wW (t : ℝ) : ℝ := 1 - Real.exp (-t)

lemma uW_deriv (t : ℝ) :
    HasDerivAt uW (fieldU (0 : ℝ →ₗ[ℝ] ℝ) idR idR 1 (uW t) 1) t := by
  have h := ((Real.hasDerivAt_exp (-t)).comp t ((hasDerivAt_id t).neg)).const_add 1
  exact h.congr_deriv (by simp [fieldU, uW])

lemma vW_deriv (t : ℝ) :
    HasDerivAt (fun _ : ℝ => (1 : ℝ))
      (fieldV (0 : ℝ →ₗ[ℝ] ℝ) idR idR idR 1 1 (uW t) 1 (wW t)) t := by
  exact (hasDerivAt_const t (1 : ℝ)).congr_deriv (by simp [fieldV, uW, wW])

lemma wW_deriv (t : ℝ) :
    HasDerivAt wW (fieldW (0 : ℝ →ₗ[ℝ] ℝ) idR 1 1 (wW t)) t := by
  have h := ((Real.hasDerivAt_exp (-t)).comp t ((hasDerivAt_id t).neg)).const_sub 1
  exact h.congr_deriv (by simp [fieldW, wW])

/-- The witness satisfies every hypothesis of `mass_conserved`, and the conclusion is the
non-trivial identity `(1 + e^{−t}) + 1 + (1 − e^{−t}) = 3`. -/
example (t : ℝ) (ht : 0 ≤ t) :
    inner ℝ (uW t) (1 : ℝ) + inner ℝ (1 : ℝ) (1 : ℝ) + inner ℝ (wW t) (1 : ℝ)
      = inner ℝ (uW 0) (1 : ℝ) + inner ℝ (1 : ℝ) (1 : ℝ) + inner ℝ (wW 0) (1 : ℝ) :=
  mass_conserved (0 : ℝ →ₗ[ℝ] ℝ) 0 0 idR idR idR idR 1 1 1 1 1
    (fun _ => by simp) (fun _ => by simp) (fun _ => by simp) idR_adj idR_adj rfl rfl
    uW (fun _ => 1) wW (fun s _ => uW_deriv s) (fun s _ => vW_deriv s)
    (fun s _ => wW_deriv s) t ht

/-- In the witness the bulk mass alone is NOT conserved (`u(0) = 2`, `u(1) = 1 + e^{−1}`): the
conservation is a genuine cancellation between the three components. -/
example : uW 1 ≠ uW 0 := by
  simp only [uW, neg_zero, Real.exp_zero]
  have : Real.exp (-1) < 1 := by
    rw [← Real.exp_zero]; exact Real.exp_lt_exp.mpr (by norm_num)
  linarith

/-- In the witness the energy strictly decreases between `t = 0` and `t = 1`, as given by
`energy_antitone` (here `‖Ru − v‖ = e^{−t} > 0`). -/
example : (‖uW 1‖ ^ 2 / 2 + ‖(1 : ℝ)‖ ^ 2 / 2 + ‖wW 1‖ ^ 2 / 2)
    < ‖uW 0‖ ^ 2 / 2 + ‖(1 : ℝ)‖ ^ 2 / 2 + ‖wW 0‖ ^ 2 / 2 := by
  simp only [uW, wW, neg_zero, Real.exp_zero, Real.norm_eq_abs, sq_abs]
  have h0 : 0 < Real.exp (-1) := Real.exp_pos _
  have h1 : Real.exp (-1) < 1 := by rw [← Real.exp_zero]; exact Real.exp_lt_exp.mpr (by norm_num)
  nlinarith

example : AntitoneOn (fun s => ‖uW s‖ ^ 2 / 2 + ‖(fun _ : ℝ => (1 : ℝ)) s‖ ^ 2 / 2
    + ‖wW s‖ ^ 2 / 2) (Ici 0) :=
  energy_antitone (0 : ℝ →ₗ[ℝ] ℝ) 0 0 idR idR idR idR (fun _ : ℝ => (0 : ℝ))
    (fun _ : ℝ => (0 : ℝ)) (fun _ : ℝ => (0 : ℝ)) 1 1 zero_le_one zero_le_one
    (fun _ => by simp) (fun _ => by simp) (fun _ => by simp) idR_adj idR_adj
    uW (fun _ => 1) wW (fun s _ => uW_deriv s) (fun s _ => vW_deriv s)
    (fun s _ => wW_deriv s)

/-! ## Second witness, with a NON-ZERO Neumann Laplacian on the bulk.
Bulk `Hb = ℂ ≅ ℝ²` (two cells, real inner product `⟪w, z⟫ = w.re z.re + w.im z.im`), with the
two-cell Neumann Laplacian `L(a, b) = (b − a, a − b)`, gradient `G(a, b) = a − b`,
`𝟙 = (1, 1)`, restriction `R(a, b) = (a + b)/2` (an average, so `R𝟙 = 1`) and its adjoint
`E φ = (φ/2, φ/2)`; interface and filament are `ℝ` with `L = 0`, `S = F = id`. Every hypothesis
of `mass_flux_zero` and `energy_flux` holds, and at `u = (2, 0)`, `v = w = 0` the bulk flux alone
is `−1 ≠ 0` while the energy flux is `−5`, with the Laplacian contributing `−4`. -/

/-- Two-cell Neumann Laplacian on `ℂ ≅ ℝ²`. -/
def Lc : ℂ →ₗ[ℝ] ℂ where
  toFun z := ⟨z.im - z.re, z.re - z.im⟩
  map_add' x y := by apply Complex.ext <;> simp <;> ring
  map_smul' r x := by apply Complex.ext <;> simp <;> ring

/-- Averaging restriction `R(a, b) = (a + b)/2`. -/
noncomputable def Rc : ℂ →ₗ[ℝ] ℝ where
  toFun z := (z.re + z.im) / 2
  map_add' x y := by simp; ring
  map_smul' r x := by simp; ring

/-- Its adjoint `E φ = (φ/2, φ/2)`. -/
noncomputable def Ec : ℝ →ₗ[ℝ] ℂ where
  toFun φ := ⟨φ / 2, φ / 2⟩
  map_add' x y := by apply Complex.ext <;> simp <;> ring
  map_smul' r x := by apply Complex.ext <;> simp <;> ring

/-- Discrete gradient `G(a, b) = a − b`. -/
def Gc (z : ℂ) : ℝ := z.re - z.im

lemma Lc_neumann : ∀ z, inner ℝ (Lc z) (⟨1, 1⟩ : ℂ) = 0 := by
  intro z; simp [Lc, Complex.inner]

lemma Lc_green : ∀ z, inner ℝ z (Lc z) = -‖Gc z‖ ^ 2 := by
  intro z; simp [Lc, Gc, Complex.inner, Real.norm_eq_abs, sq_abs]; ring

lemma RcEc_adj : ∀ z φ, inner ℝ z (Ec φ) = inner ℝ (Rc z) φ := by
  intro z φ; simp [Ec, Rc, Complex.inner]; ring

lemma Rc_one : Rc ⟨1, 1⟩ = 1 := by simp [Rc]

example : inner ℝ (fieldU Lc Rc Ec 1 ⟨2, 0⟩ 0) (⟨1, 1⟩ : ℂ)
    + inner ℝ (fieldV (0 : ℝ →ₗ[ℝ] ℝ) Rc idR idR 1 1 ⟨2, 0⟩ 0 0) (1 : ℝ)
    + inner ℝ (fieldW (0 : ℝ →ₗ[ℝ] ℝ) idR 1 0 0) (1 : ℝ) = 0 :=
  mass_flux_zero Lc 0 0 Rc Ec idR idR ⟨1, 1⟩ 1 1 1 1 Lc_neumann (fun _ => by simp)
    (fun _ => by simp) RcEc_adj idR_adj Rc_one rfl ⟨2, 0⟩ 0 0

example : inner ℝ (fieldU Lc Rc Ec 1 ⟨2, 0⟩ 0) (⟨1, 1⟩ : ℂ) = -1 := by
  simp [fieldU, Lc, Rc, Ec, Complex.inner]; norm_num

example : inner ℝ (⟨2, 0⟩ : ℂ) (fieldU Lc Rc Ec 1 ⟨2, 0⟩ 0)
    + inner ℝ (0 : ℝ) (fieldV (0 : ℝ →ₗ[ℝ] ℝ) Rc idR idR 1 1 ⟨2, 0⟩ 0 0)
    + inner ℝ (0 : ℝ) (fieldW (0 : ℝ →ₗ[ℝ] ℝ) idR 1 0 0) = -5 := by
  rw [energy_flux Lc 0 0 Rc Ec idR idR Gc (fun _ : ℝ => (0 : ℝ)) (fun _ : ℝ => (0 : ℝ)) 1 1
    Lc_green (fun _ => by simp) (fun _ => by simp) RcEc_adj idR_adj]
  simp [Gc, Rc]; norm_num

/-! ## Mutants. -/

/-- Mutant 1 (drop `R𝟙Ω = 𝟙Γ`, the consequence of the interface condition): with
`R = E = ½·id` (still adjoint), the mass flux is non-zero. The book itself says mass is not
conserved without `eq:interface_condition`. -/
theorem mass_mutant_false :
    ¬ (∀ (R E : ℝ →ₗ[ℝ] ℝ), (∀ x φ, inner ℝ x (E φ) = inner ℝ (R x) φ) →
        ∀ u v : ℝ,
        inner ℝ (fieldU (0 : ℝ →ₗ[ℝ] ℝ) R E 1 u v) (1 : ℝ)
          + inner ℝ (fieldV (0 : ℝ →ₗ[ℝ] ℝ) R idR idR 1 1 u v v) (1 : ℝ)
          + inner ℝ (fieldW (0 : ℝ →ₗ[ℝ] ℝ) idR 1 v v) (1 : ℝ) = 0) := by
  intro h
  have := h ((1 / 2 : ℝ) • LinearMap.id) ((1 / 2 : ℝ) • LinearMap.id)
    (fun x φ => by simp; ring) 2 0
  simp [fieldU, fieldV, fieldW] at this
  norm_num at this

/-- Mutant 2 (drop `λ ≥ 0`): with `λ = −1` the energy flux is positive at `u = 1, v = 0`. -/
theorem energy_mutant_false :
    ¬ (∀ lam : ℝ, ∀ u v : ℝ,
        inner ℝ u (fieldU (0 : ℝ →ₗ[ℝ] ℝ) idR idR lam u v)
          + inner ℝ v (fieldV (0 : ℝ →ₗ[ℝ] ℝ) idR idR idR lam 1 u v v)
          + inner ℝ v (fieldW (0 : ℝ →ₗ[ℝ] ℝ) idR 1 v v) ≤ 0) := by
  intro h
  have := h (-1) 1 0
  simp [fieldU, fieldV, fieldW] at this
  norm_num at this

end LeanReal.Chap05Coupled

#print axioms LeanReal.Chap05Coupled.mass_flux_zero
#print axioms LeanReal.Chap05Coupled.energy_flux
#print axioms LeanReal.Chap05Coupled.mass_conserved
#print axioms LeanReal.Chap05Coupled.energy_hasDerivAt
#print axioms LeanReal.Chap05Coupled.energy_antitone
#print axioms LeanReal.Chap05Coupled.mass_mutant_false
#print axioms LeanReal.Chap05Coupled.energy_mutant_false
