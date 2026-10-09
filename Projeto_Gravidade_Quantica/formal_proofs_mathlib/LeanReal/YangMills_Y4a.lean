import Mathlib.RingTheory.Derivation.Basic
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Topology.Instances.Matrix
import Mathlib.Topology.MetricSpace.ProperSpace
import Mathlib.Topology.Order.Compact
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Analysis.Convex.Basic
import Mathlib.Algebra.Order.Star.Real

/-!
# Yang–Mills paper (Zenodo concept DOI 10.5281/zenodo.22301093), item Y4(a)

Source: `Manuscritos_Avulsos/paper_yang_mills_mass_gap/paper_yang_mills_mass_gap.tex`,
Lemma `lem:gz_convex` ("Convexity of the Gribov–Zwanziger additions; Galerkin truncations"), (a):

> (a) `M_N(A)` is symmetric and `A ↦ M_N(A) = M_N(0) + L(A)` is affine, with `L` linear; hence
>     `Ω_N` is an open convex set containing `0`;

with (Definition `def:galerkin`) `M_N(A) = P_N M(A) P_N|_{G_N}`,
`Ω_N = {A ∈ V_N : M_N(A) > 0}`, `V_N` a finite-dimensional space of transverse (`∂·A = 0`)
connections, `G_N` finite-dimensional and orthogonal to the constants. Proof of (a) in the paper:
> Integrating by parts on the torus, `⟨ψ, M(A)ω⟩ = ∫ ∂_μψ^a ∂_μω^a + g T(ψ,ω)` with
> `T(ψ,ω) = ∫ f^{abc} ∂_μψ^a A^b_μ ω^c`. A second integration by parts, `∂_μA^b_μ = 0` and the
> total antisymmetry of `f` give `T(ψ,ω) = −∫ f^{abc} ψ^a A^b_μ ∂_μω^c = T(ω,ψ)`. Compression by
> the orthogonal projection `P_N` preserves symmetry, and `M(A)` is affine in `A`. A convex
> combination of positive matrices is positive, so `Ω_N` is convex; it is open, and
> `M_N(0) = P_N(−∂²)P_N > 0` on `G_N`.

## Formal version (algebraic model of the torus; declared below)

* Functions: a commutative `ℝ`-algebra `𝓕` with derivations `∂_μ` (`μ : Fin d`) and an
  `ℝ`-linear "integral" `I : 𝓕 → ℝ` that kills total derivatives, `I(∂_μ u) = 0`. This is
  exactly what integration by parts on a torus without boundary uses. Colour index `a : Fin m`.
* `T A ψ ω = ∑_{a,b,c} f_{abc} ∑_μ I(∂_μψ^a A^b_μ ω^c)`, and
  `Q A ψ ω = ∑_{μ,a} I(∂_μψ^a ∂_μω^a) + g T A ψ ω` (the paper's `⟨ψ, M(A)ω⟩`).
* `T_symm` : if `∑_μ ∂_μA^b_μ = 0` for every `b` and `f_{cba} = −f_{abc}`, then
  `T(ψ,ω) = T(ω,ψ)`; `Q_symm` follows.
* `MN A = (Q A (e_i) (e_j))_{ij}` for a finite family `e` (the matrix of `P_N M(A) P_N` in an
  orthonormal basis `e` of `G_N`). `MN_isHermitian` : symmetric when `A` is divergence-free.
* `MN_affine` : `MN A = MN 0 + LN A`, with `LN` an `ℝ`-LINEAR map (`LN : Conn →ₗ[ℝ] Mat`).
* With linear coordinates `ι : E →ₗ[ℝ] Conn` of `V_N` (`E` a finite-dimensional normed space,
  every `ι x` divergence-free): `Ω = {x | MN(ι x) ≻ 0}` is CONVEX (`omega_convex`) and OPEN
  (`omega_open`), and contains `0` (`zero_mem_omega`) under two declared torus facts:
  `I(u²) ≥ 0` with equality only for `u = 0`, and no nonzero combination of the `e_i` has all
  derivatives zero (`G_N ⊥ constants`, `e` independent).
* `isOpen_posDef` (general, not in Mathlib): for continuous `F : X → Mat` with symmetric values,
  `{x | F x ≻ 0}` is open.

## Declared reductions / NOT covered

* The torus enters only through the abstract axioms on `(𝓕, ∂, I)`; that smooth functions on
  `T^d` with `∫` satisfy them is NOT formalized in general. A concrete model is built for
  `d = 1` (`CircleFun`: smooth `2π`-periodic functions, `∂ = d/dθ`, `I = ∫₀^{2π}`): there the
  axioms and both torus facts are PROVED (`Icirc_dθ`, `Icirc_sq_nonneg`, `Icirc_sq_eq_zero`),
  `witness_circle` shows `T ≠ 0`, and `witness_omega` shows `Ω` open, convex, `0 ∈ Ω` for
  `G_N = span{(sin,0,0)}`, `V_N = span{(0,1,0)}`, `su(2)` structure constants `ε_{abc}`.
* The Faddeev–Popov operator itself (`M(A) = −∂·D(A)`) and the first integration by parts
  `⟨ψ, M(A)ω⟩ = ∫ ∂ψ∂ω + gT` are not formalized: `Q` is DEFINED as the right-hand side.
* `P_N` is represented by a finite family `e` (Gram matrix); orthonormality of `e` is not used.
* Only antisymmetry of `f` in its first and third slots is used (weaker than total
  antisymmetry; `f^{acd}f^{bcd} = Nδ^{ab}` is not used).
* The two torus facts behind `M_N(0) > 0` are HYPOTHESES of `zero_mem_omega`.
-/

namespace LeanReal.YangMillsY4a

open Matrix Finset Filter Topology

set_option autoImplicit false

/-! ## The abstract (integration-by-parts) model -/

section Abstract

variable {𝓕 : Type*} [CommRing 𝓕] [Algebra ℝ 𝓕] {d m : ℕ}

/-- Connections `A^b_μ`. -/
abbrev Conn (d m : ℕ) (𝓕 : Type*) := Fin d → Fin m → 𝓕
/-- `𝔤`-valued functions `ψ^a`. -/
abbrev Fld (m : ℕ) (𝓕 : Type*) := Fin m → 𝓕

variable (D : Fin d → Derivation ℝ 𝓕 𝓕) (I : 𝓕 →ₗ[ℝ] ℝ) (f : Fin m → Fin m → Fin m → ℝ)

/-- Transversality `∂_μ A^b_μ = 0`. -/
def DivFree (A : Conn d m 𝓕) : Prop := ∀ b, ∑ μ, D μ (A μ b) = 0

/-- `T(ψ,ω) = ∫ f^{abc} ∂_μψ^a A^b_μ ω^c`. -/
def T (A : Conn d m 𝓕) (ψ ω : Fld m 𝓕) : ℝ :=
  ∑ a, ∑ b, ∑ c, f a b c * ∑ μ, I (D μ (ψ a) * A μ b * ω c)

/-- `⟨ψ, M(A)ω⟩ = ∫ ∂_μψ^a ∂_μω^a + g T(ψ,ω)`. -/
def Q (g : ℝ) (A : Conn d m 𝓕) (ψ ω : Fld m 𝓕) : ℝ :=
  ∑ μ, ∑ a, I (D μ (ψ a) * D μ (ω a)) + g * T D I f A ψ ω

omit [Algebra ℝ 𝓕] in
lemma sum3_swap {k : ℕ} (G : Fin k → Fin k → Fin k → ℝ) :
    ∑ a, ∑ b, ∑ c, G a b c = ∑ a, ∑ b, ∑ c, G c b a := by
  calc ∑ a, ∑ b, ∑ c, G a b c = ∑ b, ∑ a, ∑ c, G a b c := Finset.sum_comm
    _ = ∑ b, ∑ c, ∑ a, G a b c := Finset.sum_congr rfl fun _ _ => Finset.sum_comm
    _ = ∑ c, ∑ b, ∑ a, G a b c := Finset.sum_comm

/-- Integration by parts with a divergence-free `A`. -/
lemma ibp (hI : ∀ μ u, I (D μ u) = 0) {A : Conn d m 𝓕} (hA : DivFree D A) (u w : 𝓕)
    (b : Fin m) : ∑ μ, I (D μ u * A μ b * w) = -∑ μ, I (u * A μ b * D μ w) := by
  have key : ∀ μ, D μ u * A μ b * w =
      D μ (u * (A μ b * w)) - u * A μ b * D μ w - u * w * D μ (A μ b) := by
    intro μ
    rw [Derivation.leibniz, Derivation.leibniz]
    simp only [smul_eq_mul]
    ring
  have hsum : ∑ μ, I (u * w * D μ (A μ b)) = 0 := by
    rw [← map_sum, ← Finset.mul_sum, hA b, mul_zero, map_zero]
  simp_rw [key, map_sub, Finset.sum_sub_distrib, hI, Finset.sum_const_zero, hsum]
  ring

/-- **`lem:gz_convex`(a), symmetry of `T`.** -/
theorem T_symm (hI : ∀ μ u, I (D μ u) = 0) (hf : ∀ a b c, f c b a = -f a b c)
    {A : Conn d m 𝓕} (hA : DivFree D A) (ψ ω : Fld m 𝓕) :
    T D I f A ψ ω = T D I f A ω ψ := by
  set S : Fin m → Fin m → Fin m → ℝ := fun c b a => ∑ μ, I (D μ (ω c) * A μ b * ψ a) with hS
  have h1 : ∀ a b c, ∑ μ, I (D μ (ψ a) * A μ b * ω c) = -S c b a := by
    intro a b c
    rw [ibp D I hI hA, hS]
    congr 1
    refine Finset.sum_congr rfl fun μ _ => ?_
    congr 1
    ring
  unfold T
  simp_rw [h1]
  calc ∑ a, ∑ b, ∑ c, f a b c * -S c b a = ∑ a, ∑ b, ∑ c, f c b a * S c b a := by
        refine Finset.sum_congr rfl fun a _ => Finset.sum_congr rfl fun b _ =>
          Finset.sum_congr rfl fun c _ => ?_
        rw [hf]; ring
    _ = ∑ a, ∑ b, ∑ c, f a b c * S a b c := sum3_swap (fun a b c => f c b a * S c b a)

/-- Symmetry of `⟨ψ, M(A)ω⟩`. -/
theorem Q_symm (hI : ∀ μ u, I (D μ u) = 0) (hf : ∀ a b c, f c b a = -f a b c) (g : ℝ)
    {A : Conn d m 𝓕} (hA : DivFree D A) (ψ ω : Fld m 𝓕) :
    Q D I f g A ψ ω = Q D I f g A ω ψ := by
  unfold Q
  rw [T_symm D I f hI hf hA]
  congr 1
  refine Finset.sum_congr rfl fun μ _ => Finset.sum_congr rfl fun a _ => ?_
  rw [mul_comm]

lemma T_add (A A' : Conn d m 𝓕) (ψ ω : Fld m 𝓕) :
    T D I f (A + A') ψ ω = T D I f A ψ ω + T D I f A' ψ ω := by
  simp only [T, Pi.add_apply, mul_add, add_mul, map_add, Finset.sum_add_distrib]

lemma T_smul (r : ℝ) (A : Conn d m 𝓕) (ψ ω : Fld m 𝓕) :
    T D I f (r • A) ψ ω = r * T D I f A ψ ω := by
  simp only [T, Pi.smul_apply, mul_smul_comm, smul_mul_assoc, map_smul, smul_eq_mul,
    Finset.mul_sum]
  refine Finset.sum_congr rfl fun a _ => Finset.sum_congr rfl fun b _ =>
    Finset.sum_congr rfl fun c _ => Finset.sum_congr rfl fun μ _ => ?_
  ring

lemma T_zero (ψ ω : Fld m 𝓕) : T D I f 0 ψ ω = 0 := by
  simp [T]

variable {n : ℕ}

/-- Galerkin matrix `M_N(A)_{ij} = ⟨e_i, M(A) e_j⟩`. -/
def MN (g : ℝ) (e : Fin n → Fld m 𝓕) (A : Conn d m 𝓕) : Matrix (Fin n) (Fin n) ℝ :=
  Matrix.of fun i j => Q D I f g A (e i) (e j)

/-- The linear part `L(A)_{ij} = g T_A(e_i, e_j)`. -/
def LN (g : ℝ) (e : Fin n → Fld m 𝓕) : Conn d m 𝓕 →ₗ[ℝ] Matrix (Fin n) (Fin n) ℝ where
  toFun A := Matrix.of fun i j => g * T D I f A (e i) (e j)
  map_add' A A' := by ext i j; simp [T_add, mul_add]
  map_smul' r A := by ext i j; simp [T_smul]; ring

/-- **`lem:gz_convex`(a), symmetry of `M_N(A)`.** -/
theorem MN_isHermitian (hI : ∀ μ u, I (D μ u) = 0) (hf : ∀ a b c, f c b a = -f a b c) (g : ℝ)
    (e : Fin n → Fld m 𝓕) {A : Conn d m 𝓕} (hA : DivFree D A) :
    (MN D I f g e A).IsHermitian := by
  ext i j
  simp only [conjTranspose_apply, star_trivial, MN, of_apply]
  exact Q_symm D I f hI hf g hA _ _

/-- **`lem:gz_convex`(a), affinity**: `M_N(A) = M_N(0) + L(A)`, `L` linear. -/
theorem MN_affine (g : ℝ) (e : Fin n → Fld m 𝓕) (A : Conn d m 𝓕) :
    MN D I f g e A = MN D I f g e 0 + LN D I f g e A := by
  ext i j
  simp [MN, LN, Q, T_zero]

lemma divFree_zero : DivFree D (0 : Conn d m 𝓕) := fun b => by simp

end Abstract

/-! ## Positive-definite matrices: an open condition (general lemmas) -/

section PosDefOpen

variable {k : Type*} [Fintype k]

lemma quad_bound (B : Matrix k k ℝ) (v : k → ℝ) :
    |v ⬝ᵥ (B *ᵥ v)| ≤ (∑ i, ∑ j, |B i j|) * ‖v‖ ^ 2 := by
  have hv : ∀ i, |v i| ≤ ‖v‖ := fun i => by
    have := norm_le_pi_norm v i
    rwa [Real.norm_eq_abs] at this
  calc |v ⬝ᵥ (B *ᵥ v)| = |∑ i, ∑ j, v i * B i j * v j| := by
        simp [dotProduct, mulVec, Finset.mul_sum, mul_assoc]
    _ ≤ ∑ i, |∑ j, v i * B i j * v j| := Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ i, ∑ j, |v i * B i j * v j| :=
        Finset.sum_le_sum fun i _ => Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ i, ∑ j, |B i j| * ‖v‖ ^ 2 := by
        refine Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j _ => ?_
        rw [abs_mul, abs_mul]
        have h1 := hv i
        have h2 := hv j
        have h3 := abs_nonneg (B i j)
        have h4 := abs_nonneg (v i)
        have h5 := abs_nonneg (v j)
        calc |v i| * |B i j| * |v j| = |B i j| * (|v i| * |v j|) := by ring
          _ ≤ |B i j| * (‖v‖ * ‖v‖) :=
            mul_le_mul_of_nonneg_left (mul_le_mul h1 h2 h5 (norm_nonneg _)) h3
          _ = |B i j| * ‖v‖ ^ 2 := by ring
    _ = (∑ i, ∑ j, |B i j|) * ‖v‖ ^ 2 := by
        rw [Finset.sum_mul]
        exact Finset.sum_congr rfl fun i _ => (Finset.sum_mul _ _ _).symm

lemma posDef_coercive {M : Matrix k k ℝ} (hM : M.PosDef) :
    ∃ c > 0, ∀ v : k → ℝ, c * ‖v‖ ^ 2 ≤ v ⬝ᵥ (M *ᵥ v) := by
  rcases isEmpty_or_nonempty k with hk | hk
  · refine ⟨1, one_pos, fun v => ?_⟩
    have : v = 0 := Subsingleton.elim _ _
    simp [this]
  · have hne : (Metric.sphere (0 : k → ℝ) 1).Nonempty :=
      (NormedSpace.sphere_nonempty).mpr zero_le_one
    have hcont : Continuous fun v : k → ℝ => v ⬝ᵥ (M *ᵥ v) :=
      continuous_id.dotProduct (continuous_const.matrix_mulVec continuous_id)
    obtain ⟨v₀, hv₀, hmin⟩ :=
      (isCompact_sphere (0 : k → ℝ) 1).exists_isMinOn hne hcont.continuousOn
    have hv₀ne : v₀ ≠ 0 := by
      rintro rfl
      simp at hv₀
    refine ⟨v₀ ⬝ᵥ (M *ᵥ v₀), ?_, fun v => ?_⟩
    · have := hM.dotProduct_mulVec_pos hv₀ne
      simpa [star_trivial] using this
    · by_cases hv : v = 0
      · subst hv; simp
      · have hr : 0 < ‖v‖ := norm_pos_iff.mpr hv
        set w := ‖v‖⁻¹ • v with hw
        have hwS : w ∈ Metric.sphere (0 : k → ℝ) 1 := by
          rw [mem_sphere_zero_iff_norm, hw, norm_smul, norm_inv, norm_norm,
            inv_mul_cancel₀ hr.ne']
        have h := hmin hwS
        simp only [Set.mem_ofPred_eq] at h
        have hq : w ⬝ᵥ (M *ᵥ w) = (v ⬝ᵥ (M *ᵥ v)) / ‖v‖ ^ 2 := by
          rw [hw, mulVec_smul, dotProduct_smul, smul_dotProduct, smul_eq_mul, smul_eq_mul]
          field_simp
        rw [hq, le_div_iff₀ (by positivity)] at h
        exact h

/-- `{x | F x ≻ 0}` is open for continuous symmetric-valued `F` (not in Mathlib). -/
theorem isOpen_posDef {X : Type*} [TopologicalSpace X] (F : X → Matrix k k ℝ)
    (hF : Continuous F) (hH : ∀ x, (F x).IsHermitian) : IsOpen {x | (F x).PosDef} := by
  rw [isOpen_iff_mem_nhds]
  intro x₀ hx₀
  obtain ⟨c, hc, hcoer⟩ := posDef_coercive (k := k) hx₀
  let K : X → ℝ := fun x => ∑ i, ∑ j, |F x i j - F x₀ i j|
  have hK : Continuous K :=
    continuous_finsetSum _ fun i _ => continuous_finsetSum _ fun j _ =>
      ((hF.matrix_elem i j).sub continuous_const).abs
  have hK0 : K x₀ < c := by simp [K, hc]
  have hev : ∀ᶠ x in 𝓝 x₀, K x < c := (hK.tendsto x₀).eventually (gt_mem_nhds hK0)
  filter_upwards [hev] with x hx
  refine posDef_iff_dotProduct_mulVec.mpr ⟨hH x, fun v hv => ?_⟩
  rw [star_trivial]
  have hb := quad_bound (F x - F x₀) v
  have hsplit : v ⬝ᵥ (F x *ᵥ v) = v ⬝ᵥ (F x₀ *ᵥ v) + v ⬝ᵥ ((F x - F x₀) *ᵥ v) := by
    rw [sub_mulVec, dotProduct_sub]; ring
  have hKx : (∑ i, ∑ j, |(F x - F x₀) i j|) = K x := rfl
  rw [hKx] at hb
  have hr : 0 < ‖v‖ := norm_pos_iff.mpr hv
  have h1 := (abs_le.mp hb).1
  have h2 := hcoer v
  have h3 : 0 < (c - K x) * ‖v‖ ^ 2 := mul_pos (by linarith) (by positivity)
  rw [hsplit]
  nlinarith

omit [Fintype k] in
/-- A convex combination of positive-definite matrices is positive definite. -/
lemma posDef_convex_comb {P R : Matrix k k ℝ} (hP : P.PosDef) (hR : R.PosDef) {a b : ℝ}
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hab : a + b = 1) : (a • P + b • R).PosDef := by
  rcases ha.eq_or_lt with h | h
  · subst h
    have : b = 1 := by linarith
    subst this
    simpa using hR
  · exact (hP.smul h).add_posSemidef (hR.posSemidef.smul hb)

end PosDefOpen

/-! ## `Ω_N` in linear coordinates: convex, open, contains `0` -/

section Omega

variable {𝓕 : Type*} [CommRing 𝓕] [Algebra ℝ 𝓕] {d m n : ℕ}
  (D : Fin d → Derivation ℝ 𝓕 𝓕) (I : 𝓕 →ₗ[ℝ] ℝ) (f : Fin m → Fin m → Fin m → ℝ) (g : ℝ)
  (e : Fin n → Fld m 𝓕)
  {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] (ι : E →ₗ[ℝ] Conn d m 𝓕)

/-- `Ω_N` in the flat coordinates `ι` of `V_N`. -/
def Omega : Set E := {x | (MN D I f g e (ι x)).PosDef}

/-- **`lem:gz_convex`(a): `Ω_N` is convex.** -/
theorem omega_convex : Convex ℝ (Omega D I f g e ι) := by
  intro x hx y hy a b ha hb hab
  have hlin : MN D I f g e (ι (a • x + b • y)) =
      a • MN D I f g e (ι x) + b • MN D I f g e (ι y) := by
    rw [MN_affine, MN_affine D I f g e (ι x), MN_affine D I f g e (ι y), map_add, map_smul,
      map_smul, map_add, map_smul, map_smul]
    have : MN D I f g e 0 = a • MN D I f g e 0 + b • MN D I f g e 0 := by
      rw [← add_smul, hab, one_smul]
    conv_lhs => rw [this]
    simp only [smul_add]
    abel
  show (MN D I f g e (ι (a • x + b • y))).PosDef
  rw [hlin]
  exact posDef_convex_comb hx hy ha hb hab

/-- **`lem:gz_convex`(a): `Ω_N` is open** (finite-dimensional coordinates, divergence-free
connections). -/
theorem omega_open [FiniteDimensional ℝ E] (hI : ∀ μ u, I (D μ u) = 0)
    (hf : ∀ a b c, f c b a = -f a b c) (hdiv : ∀ x, DivFree D (ι x)) :
    IsOpen (Omega D I f g e ι) := by
  have hcont : Continuous fun x => MN D I f g e (ι x) := by
    have hlin : Continuous ((LN D I f g e).comp ι) :=
      LinearMap.continuous_of_finiteDimensional _
    have : (fun x => MN D I f g e (ι x)) = fun x => MN D I f g e 0 + ((LN D I f g e).comp ι) x :=
      funext fun x => MN_affine D I f g e (ι x)
    rw [this]
    exact continuous_const.add hlin
  exact isOpen_posDef _ hcont fun x => MN_isHermitian D I f hI hf g e (hdiv x)

/-- The Dirichlet part `B(ψ,ω) = ∑_{μ,a} I(∂_μψ^a ∂_μω^a)` as a bilinear map. -/
def dirichlet : Fld m 𝓕 →ₗ[ℝ] Fld m 𝓕 →ₗ[ℝ] ℝ :=
  LinearMap.mk₂ ℝ (fun ψ ω => ∑ μ, ∑ a, I (D μ (ψ a) * D μ (ω a)))
    (fun ψ ψ' ω => by simp [add_mul, Finset.sum_add_distrib])
    (fun r ψ ω => by simp [Finset.mul_sum])
    (fun ψ ω ω' => by simp [mul_add, Finset.sum_add_distrib])
    (fun r ψ ω => by simp [Finset.mul_sum])

lemma dirichlet_symm (ψ ω : Fld m 𝓕) : dirichlet D I ψ ω = dirichlet D I ω ψ := by
  simp only [dirichlet, LinearMap.mk₂_apply]
  exact Finset.sum_congr rfl fun μ _ => Finset.sum_congr rfl fun a _ => by rw [mul_comm]

/-- **`lem:gz_convex`(a): `0 ∈ Ω_N`, i.e. `M_N(0) ≻ 0`**, from the two torus facts (declared
hypotheses): `I(u²) ≥ 0` with equality only at `u = 0`, and no nonzero combination of the `e_i`
has all derivatives zero. -/
theorem zero_mem_omega (hI : ∀ μ u, I (D μ u) = 0) (hf : ∀ a b c, f c b a = -f a b c)
    (hIpos : ∀ u, 0 ≤ I (u * u)) (hIdef : ∀ u, I (u * u) = 0 → u = 0)
    (hgrad : ∀ v : Fin n → ℝ, v ≠ 0 → ∃ μ a, D μ (∑ i, v i • e i a) ≠ 0) :
    (0 : E) ∈ Omega D I f g e ι := by
  show (MN D I f g e (ι 0)).PosDef
  rw [map_zero]
  refine posDef_iff_dotProduct_mulVec.mpr ⟨MN_isHermitian D I f hI hf g e (divFree_zero D),
    fun v hv => ?_⟩
  rw [star_trivial]
  have hM : ∀ i j, MN D I f g e 0 i j = dirichlet D I (e i) (e j) := fun i j => by
    simp [MN, Q, T_zero, dirichlet]
  have hquad : v ⬝ᵥ (MN D I f g e 0 *ᵥ v) =
      dirichlet D I (∑ i, v i • e i) (∑ j, v j • e j) := by
    simp only [map_sum, map_smul, LinearMap.sum_apply, LinearMap.smul_apply, smul_eq_mul,
      dotProduct, mulVec, hM, Finset.mul_sum]
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
    rw [dirichlet_symm D I (e j) (e i)]
    ring
  rw [hquad]
  obtain ⟨μ₀, a₀, hne⟩ := hgrad v hv
  show 0 < ∑ μ, ∑ a, I (D μ ((∑ i, v i • e i) a) * D μ ((∑ i, v i • e i) a))
  apply Finset.sum_pos' (fun μ _ => Finset.sum_nonneg fun a _ => hIpos _)
  refine ⟨μ₀, Finset.mem_univ _, Finset.sum_pos' (fun a _ => hIpos _) ⟨a₀, Finset.mem_univ _, ?_⟩⟩
  rw [Finset.sum_apply]
  simp only [Pi.smul_apply]
  exact lt_of_le_of_ne (hIpos _) (fun h => hne (hIdef _ h.symm))

end Omega

/-! ## Concrete model: the circle `T¹` (non-vacuity) -/

section Circle

open Real
open scoped ContDiff

lemma periodic_deriv {u : ℝ → ℝ} {c : ℝ} (hu : Function.Periodic u c) :
    Function.Periodic (deriv u) c := by
  intro x
  have h : (fun y => u (y + c)) = u := funext hu
  rw [← deriv_comp_add_const, h]

/-- Smooth `2π`-periodic functions: functions on the circle `T¹`. -/
def CircleFun : Subalgebra ℝ (ℝ → ℝ) where
  carrier := {u | ContDiff ℝ ∞ u ∧ Function.Periodic u (2 * π)}
  mul_mem' ha hb := ⟨ha.1.mul hb.1, ha.2.mul hb.2⟩
  add_mem' ha hb := ⟨ha.1.add hb.1, ha.2.add hb.2⟩
  algebraMap_mem' _ := ⟨contDiff_const, fun _ => rfl⟩

lemma cf_smooth (u : CircleFun) : ContDiff ℝ ∞ (u : ℝ → ℝ) := u.2.1
lemma cf_diff (u : CircleFun) : Differentiable ℝ (u : ℝ → ℝ) :=
  (cf_smooth u).differentiable (by simp)

/-- `d/dθ` on `CircleFun`. -/
noncomputable def dθlin : CircleFun →ₗ[ℝ] CircleFun where
  toFun u := ⟨deriv u, (contDiff_infty_iff_deriv.mp (cf_smooth u)).2, periodic_deriv u.2.2⟩
  map_add' u v := by
    ext x
    simp only [Subalgebra.coe_add, Pi.add_apply]
    exact deriv_add (cf_diff u x) (cf_diff v x)
  map_smul' r u := by
    ext x
    simp only [Subalgebra.coe_smul, Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
    exact deriv_const_smul r (cf_diff u x)

noncomputable def dθ : Derivation ℝ CircleFun CircleFun :=
  Derivation.mk' dθlin fun u v => by
    ext x
    simp only [dθlin, LinearMap.coe_mk, AddHom.coe_mk, Subalgebra.coe_mul, Subalgebra.coe_add,
      smul_eq_mul, Pi.mul_apply, Pi.add_apply]
    rw [deriv_mul (cf_diff u x) (cf_diff v x)]
    ring

lemma dθ_apply (u : CircleFun) (x : ℝ) : (dθ u : ℝ → ℝ) x = deriv (u : ℝ → ℝ) x := rfl

/-- `I(u) = ∫₀^{2π} u`. -/
noncomputable def Icirc : CircleFun →ₗ[ℝ] ℝ where
  toFun u := ∫ x in (0 : ℝ)..2 * π, (u : ℝ → ℝ) x
  map_add' u v := intervalIntegral.integral_add
    ((cf_smooth u).continuous.intervalIntegrable _ _)
    ((cf_smooth v).continuous.intervalIntegrable _ _)
  map_smul' r u := by
    simp only [Subalgebra.coe_smul, Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
    exact intervalIntegral.integral_const_mul r _

/-- The torus axiom for `T¹`: `∫₀^{2π} u' = 0`. -/
theorem Icirc_dθ (u : CircleFun) : Icirc (dθ u) = 0 := by
  show ∫ x in (0 : ℝ)..2 * π, deriv (u : ℝ → ℝ) x = 0
  rw [intervalIntegral.integral_deriv_eq_sub (fun x _ => cf_diff u x)
    (((contDiff_infty_iff_deriv.mp (cf_smooth u)).2.continuous).intervalIntegrable _ _)]
  have := u.2.2 0
  rw [zero_add] at this
  rw [this, sub_self]

noncomputable def cosC : CircleFun := ⟨cos, contDiff_cos, cos_periodic⟩
noncomputable def sinC : CircleFun := ⟨sin, contDiff_sin, sin_periodic⟩

lemma dθ_cos : dθ cosC = -sinC := by
  ext x; simp [dθ_apply, cosC, sinC]

lemma dθ_sin : dθ sinC = cosC := by
  ext x; simp [dθ_apply, cosC, sinC]

lemma Icirc_sin_sin : Icirc (sinC * sinC) = π := by
  show ∫ x in (0 : ℝ)..2 * π, sin x * sin x = π
  simp_rw [← sq]
  rw [integral_sin_sq]
  simp

lemma Icirc_cos_cos : Icirc (cosC * cosC) = π := by
  show ∫ x in (0 : ℝ)..2 * π, cos x * cos x = π
  simp_rw [← sq]
  rw [integral_cos_sq]
  simp

/-- Levi-Civita symbol on `Fin 3` (structure constants of `su(2)` up to normalization). -/
def eps (a b c : Fin 3) : ℝ :=
  if (a, b, c) = (0, 1, 2) ∨ (a, b, c) = (1, 2, 0) ∨ (a, b, c) = (2, 0, 1) then 1
  else if (a, b, c) = (2, 1, 0) ∨ (a, b, c) = (0, 2, 1) ∨ (a, b, c) = (1, 0, 2) then -1 else 0

lemma eps_antisymm : ∀ a b c : Fin 3, eps c b a = -eps a b c := by
  intro a b c
  fin_cases a <;> fin_cases b <;> fin_cases c <;> norm_num [eps]

/-- The constant connection `A_θ = (0, 1, 0)` (divergence-free). -/
def A1 : Conn 1 3 CircleFun := fun _ b => if b = 1 then 1 else 0

noncomputable def ψ1 : Fld 3 CircleFun := ![cosC, 0, 0]
noncomputable def χ1 : Fld 3 CircleFun := ![0, 0, sinC]

/-- **Non-vacuity witness**: on the circle, all hypotheses of `T_symm` hold and
`T(ψ,ω) = −π ≠ 0`. -/
theorem witness_circle :
    (∀ μ u, Icirc ((fun _ : Fin 1 => dθ) μ u) = 0) ∧ (∀ a b c, eps c b a = -eps a b c) ∧
      DivFree (fun _ : Fin 1 => dθ) A1 ∧
      T (fun _ : Fin 1 => dθ) Icirc eps A1 ψ1 χ1 = -π := by
  refine ⟨fun _ u => Icirc_dθ u, eps_antisymm, fun b => ?_, ?_⟩
  · simp only [A1, Fin.sum_univ_one]
    split_ifs <;> simp
  · simp only [T, Fin.sum_univ_three, Fin.sum_univ_one, ψ1, χ1, A1]
    simp [eps, dθ_cos]
    rw [show -sinC * sinC = -(sinC * sinC) by ring, map_neg, Icirc_sin_sin]

/-- The theorem applied to the witness: `T(ω,ψ) = −π` as well. -/
example : T (fun _ : Fin 1 => dθ) Icirc eps A1 χ1 ψ1 = -π := by
  obtain ⟨h1, h2, h3, h4⟩ := witness_circle
  rw [← T_symm _ _ _ h1 h2 h3, h4]

/-- Torus fact 1 on `T¹`: `∫₀^{2π} u² ≥ 0`. -/
lemma Icirc_sq_nonneg (u : CircleFun) : 0 ≤ Icirc (u * u) := by
  show 0 ≤ ∫ x in (0 : ℝ)..2 * π, (u : ℝ → ℝ) x * (u : ℝ → ℝ) x
  exact intervalIntegral.integral_nonneg (by positivity) fun x _ => mul_self_nonneg _

/-- Torus fact 1 on `T¹`: `∫₀^{2π} u² = 0 ⇒ u = 0` (continuity and periodicity). -/
lemma Icirc_sq_eq_zero (u : CircleFun) (h : Icirc (u * u) = 0) : u = 0 := by
  have hc : Continuous fun x => (u : ℝ → ℝ) x * (u : ℝ → ℝ) x :=
    (cf_smooth u).continuous.mul (cf_smooth u).continuous
  have h' : ∫ x in (0 : ℝ)..2 * π, (u : ℝ → ℝ) x * (u : ℝ → ℝ) x = 0 := h
  rw [intervalIntegral.integral_eq_zero_iff_of_le_of_nonneg_ae (by positivity)
    (Filter.Eventually.of_forall fun x => mul_self_nonneg _) (hc.intervalIntegrable _ _)] at h'
  have hEq := MeasureTheory.Measure.eqOn_Ioc_of_ae_eq MeasureTheory.volume h' hc.continuousOn
    continuousOn_const
  ext x
  obtain ⟨y, hy, hxy⟩ := u.2.2.exists_mem_Ioc two_pi_pos x 0
  rw [zero_add] at hy
  have := hEq hy
  simp only [Pi.zero_apply, mul_self_eq_zero] at this
  simp [hxy, this]

/-- `G_N = span{(sin, 0, 0)}` (orthogonal to the constants). -/
noncomputable def e1 : Fin 1 → Fld 3 CircleFun := fun _ => ![sinC, 0, 0]

/-- `V_N = span{A1}` in the coordinate `x ↦ x A1`. -/
noncomputable def ι1 : ℝ →ₗ[ℝ] Conn 1 3 CircleFun := LinearMap.id.smulRight A1

/-- **Non-vacuity witness for `zero_mem_omega`, `omega_open`, `omega_convex`**: on `T¹` with
`G_N = span{(sin,0,0)}` and `V_N = span{A1}`, all hypotheses hold, and `Ω` is an open convex set
containing `0`. -/
theorem witness_omega :
    (∀ u : CircleFun, 0 ≤ Icirc (u * u)) ∧ (∀ u : CircleFun, Icirc (u * u) = 0 → u = 0) ∧
      (∀ v : Fin 1 → ℝ, v ≠ 0 → ∃ μ a, (fun _ : Fin 1 => dθ) μ (∑ i, v i • e1 i a) ≠ 0) ∧
      (∀ x, DivFree (fun _ : Fin 1 => dθ) (ι1 x)) ∧
      (0 : ℝ) ∈ Omega (fun _ : Fin 1 => dθ) Icirc eps 1 e1 ι1 ∧
      IsOpen (Omega (fun _ : Fin 1 => dθ) Icirc eps 1 e1 ι1) ∧
      Convex ℝ (Omega (fun _ : Fin 1 => dθ) Icirc eps 1 e1 ι1) := by
  have hgrad : ∀ v : Fin 1 → ℝ, v ≠ 0 → ∃ μ a, (fun _ : Fin 1 => dθ) μ (∑ i, v i • e1 i a) ≠ 0 := by
    intro v hv
    have hv0 : v 0 ≠ 0 := fun h => hv (funext fun i => by fin_cases i; exact h)
    refine ⟨0, 0, fun h => hv0 ?_⟩
    have := congrFun (congrArg Subtype.val h) 0
    simpa [e1, dθ_sin, dθ_apply, sinC] using this
  have hdiv : ∀ x, DivFree (fun _ : Fin 1 => dθ) (ι1 x) := by
    intro x b
    have h0 := (witness_circle).2.2.1 b
    simp only [ι1, LinearMap.smulRight_apply, LinearMap.id_apply, Pi.smul_apply,
      Fin.sum_univ_one] at h0 ⊢
    rw [Derivation.map_smul, h0, smul_zero]
  refine ⟨Icirc_sq_nonneg, Icirc_sq_eq_zero, hgrad, hdiv, ?_, ?_, omega_convex _ _ _ _ _ _⟩
  · exact zero_mem_omega _ _ _ _ _ _ (fun _ u => Icirc_dθ u) eps_antisymm Icirc_sq_nonneg
      Icirc_sq_eq_zero hgrad
  · exact omega_open _ _ _ _ _ _ (fun _ u => Icirc_dθ u) eps_antisymm hdiv

/-! ## Mutants proved FALSE -/

/-- Mutant 1 (drop transversality `∂_μA_μ = 0`): `T` is NOT symmetric. On the circle,
`A_θ = (0, cos, 0)`, `ψ = (1, 0, 0)`, `ω = (0, 0, sin)`: `T(ψ,ω) = 0` but `T(ω,ψ) = −π`. -/
theorem mutant_no_divfree_false :
    ¬ ∀ (A : Conn 1 3 CircleFun) (ψ χ : Fld 3 CircleFun),
        T (fun _ : Fin 1 => dθ) Icirc eps A ψ χ = T (fun _ : Fin 1 => dθ) Icirc eps A χ ψ := by
  intro h
  have := h (fun _ b => if b = 1 then cosC else 0) ![1, 0, 0] ![0, 0, sinC]
  simp only [T, Fin.sum_univ_three, Fin.sum_univ_one] at this
  simp [eps, dθ_sin] at this
  rw [Icirc_cos_cos] at this
  linarith [pi_pos]

/-- Mutant 2 (drop the symmetric-values hypothesis in `isOpen_posDef`): false.
`F x = [[1, x], [0, 1]]` is positive definite only at `x = 0`, and `{0}` is not open in `ℝ`. -/
theorem mutant_open_no_symm_false :
    ¬ ∀ (F : ℝ → Matrix (Fin 2) (Fin 2) ℝ), Continuous F → IsOpen {x | (F x).PosDef} := by
  intro h
  let F : ℝ → Matrix (Fin 2) (Fin 2) ℝ := fun x => !![1, x; 0, 1]
  have hF : Continuous F := by
    refine continuous_pi fun i => continuous_pi fun j => ?_
    fin_cases i <;> fin_cases j <;> simp [F] <;> fun_prop
  have hset : {x | (F x).PosDef} = {0} := by
    ext x
    simp only [Set.mem_ofPred_eq, Set.mem_singleton_iff]
    constructor
    · intro hx
      have := congrFun (congrFun hx.1 1) 0
      simpa [F, conjTranspose_apply] using this
    · rintro rfl
      have : F 0 = 1 := by ext i j; fin_cases i <;> fin_cases j <;> simp [F]
      rw [this]
      exact PosDef.one
  have := h F hF
  rw [hset] at this
  exact not_isOpen_singleton (0 : ℝ) this

/-- Mutant 3 (drop the hypothesis that no combination of the `e_i` has zero gradient):
`M_N(0) ≻ 0` fails. Model `𝓕 = ℝ`, `∂ = 0`, `I = id` (it satisfies `I(∂u) = 0`,
`I(u²) ≥ 0`, `I(u²) = 0 ⇒ u = 0`), `e_0 = (1)` constant: `M_N(0) = 0`. -/
theorem mutant_no_grad_false :
    ¬ ((∀ μ (u : ℝ), (LinearMap.id : ℝ →ₗ[ℝ] ℝ) ((fun _ : Fin 1 => (0 : Derivation ℝ ℝ ℝ)) μ u) = 0) →
        (∀ u : ℝ, 0 ≤ (LinearMap.id : ℝ →ₗ[ℝ] ℝ) (u * u)) →
        (∀ u : ℝ, (LinearMap.id : ℝ →ₗ[ℝ] ℝ) (u * u) = 0 → u = 0) →
        ∀ e : Fin 1 → Fld 1 ℝ,
          (MN (fun _ : Fin 1 => (0 : Derivation ℝ ℝ ℝ)) LinearMap.id (fun _ _ _ => 0) 1 e 0).PosDef) := by
  intro h
  have := h (fun _ _ => by simp) (fun u => mul_self_nonneg u)
    (fun u hu => by simpa using hu) (fun _ _ => 1)
  have hpos := this.2 (x := Finsupp.single 0 1) (by simp)
  simp [MN, Q, T] at hpos

end Circle

end LeanReal.YangMillsY4a

#print axioms LeanReal.YangMillsY4a.ibp
#print axioms LeanReal.YangMillsY4a.T_symm
#print axioms LeanReal.YangMillsY4a.Q_symm
#print axioms LeanReal.YangMillsY4a.MN_isHermitian
#print axioms LeanReal.YangMillsY4a.MN_affine
#print axioms LeanReal.YangMillsY4a.quad_bound
#print axioms LeanReal.YangMillsY4a.posDef_coercive
#print axioms LeanReal.YangMillsY4a.isOpen_posDef
#print axioms LeanReal.YangMillsY4a.posDef_convex_comb
#print axioms LeanReal.YangMillsY4a.omega_convex
#print axioms LeanReal.YangMillsY4a.omega_open
#print axioms LeanReal.YangMillsY4a.zero_mem_omega
#print axioms LeanReal.YangMillsY4a.Icirc_dθ
#print axioms LeanReal.YangMillsY4a.witness_circle
#print axioms LeanReal.YangMillsY4a.Icirc_sq_eq_zero
#print axioms LeanReal.YangMillsY4a.witness_omega
#print axioms LeanReal.YangMillsY4a.mutant_no_divfree_false
#print axioms LeanReal.YangMillsY4a.mutant_open_no_symm_false
#print axioms LeanReal.YangMillsY4a.mutant_no_grad_false
