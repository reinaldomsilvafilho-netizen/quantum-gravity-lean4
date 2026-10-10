import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul

/-!
# Capitulo 8, algebra pontual de RG (Lote B1 do `PLANO_LIVRO_B.md`)

Fonte: `unified_quantum_gravity_book/chap08_noneuclidean_minimax_relativity_adm.tex`.
Itens 8.2, 8.7, 8.8, 8.10, 8.11 da tabela do capitulo 8. Tudo aqui e algebra num ponto (ou num
referencial ortonormal); nenhuma variedade, conexao ou tensor de Einstein e construido.

## Reducoes declaradas (hipoteses que substituem teoria ausente)

* **8.2** (Theorem "Sectional-Extrinsic Coupling", sem rotulo). Espaco tangente `E` e espaco
  normal `N` sao espacos com produto interno reais; `II : E → E → N`. A equacao de Gauss e a
  HIPOTESE `hGauss`; a curvatura ambiente e a da forma espacial, `spaceFormCurv K̄`. A parte de
  Codazzi (`κ` constante em hipersuperficies umbilicas conexas) NAO e formalizada.
* **8.7** (`prop:raychaudhuri`). A equacao de Raychaudhuri e a HIPOTESE `hRay`, em cada ponto de
  um aberto `U ⊆ ℝ` do parametro (tempo proprio) ao longo de uma curva da congruencia. As
  componentes estao num referencial ortonormal adaptado com `V = e₀` (metrica
  `diag(-1,1,1,1)`); "shear espacial" e `σ μ 0 = 0` com `σ` simetrico.
* **8.8** (`prop:rn_horizon`). So o nucleo algebrico: `β² = 1 - f`, `f(r₊) = 0`, `β(r₊) = 1`,
  `r₊ > Q²/(2M)`, e `θ_l = 2/r - K + K_ss = 2(1-β)/r` com as componentes de `K` como DADOS
  (`hKrr`, `hKθθ`, `hKφφ`: `K^r_r = β'`, `K^θ_θ = K^φ_φ = β/r`; `hdiv`: `D_i s^i = 2/r`).
  A geometria (fatia plana, `K = Dβ`) nao entra.
* **8.10** (`prop:wormhole_throat`). As formulas `8πGρ = b'/r²`,
  `8πG p_r = -b/r³ + 2(1-b/r)Φ'/r` em `r₀` sao as HIPOTESES `hρ`, `hpr`. `K_Gauss(S₀) = 1/r₀²`
  entra como definicao (esfera redonda de raio `r₀`), nao como teorema. O item (1) (fatia
  totalmente geodesica) nao e formalizado.
* **8.11** (`prop:proper_accel`). Algebra linear em `ℝ⁴` com a forma `diag(-1,1,1,1)`, num ponto;
  `u` e `a` sao vetores, sem curva. A identidade "norma de operador = |a|_g" NAO e formalizada
  (depende da Definicao `def:opnorm`(c)); formaliza-se `II(u,u) = a` (projecao tangencial nula),
  `g(a,a) ≥ 0` e `g(a,a) = 0 ↔ a = 0`.
-/

noncomputable section

namespace LeanReal.Chap08Pointwise

open Real InnerProductSpace Finset

/-! ## 8.2 Acoplamento seccional-extrinseco -/

section Umbilic

variable {E N : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [NormedAddCommGroup N] [InnerProductSpace ℝ N]

/-- Tensor de curvatura `g(R̄(X,Y)Z, W) = K̄ (g(Y,Z) g(X,W) - g(X,Z) g(Y,W))` de uma forma
espacial de curvatura seccional `K̄`. -/
def spaceFormCurv (Kbar : ℝ) (X Y Z W : E) : ℝ :=
  Kbar * (⟪Y, Z⟫_ℝ * ⟪X, W⟫_ℝ - ⟪X, Z⟫_ℝ * ⟪Y, W⟫_ℝ)

/-- **Theorem "Sectional-Extrinsic Coupling"** (cap. 8, sem rotulo; item 8.2). Se `II` e umbilica,
`II(X,Y) = κ g(X,Y) ν` com `‖ν‖ = 1`, e `R` satisfaz a equacao de Gauss (HIPOTESE `hGauss`)
sobre a forma espacial de curvatura `K̄`, entao para `X, Y` ortonormais
`K_M(X,Y) = g(R(X,Y)Y,X) = K̄ + κ²`. -/
theorem sectional_extrinsic_coupling (R : E → E → E → E → ℝ) (II : E → E → N) (ν : N)
    (Kbar κ : ℝ) (hν : ‖ν‖ = 1) (hUmb : ∀ X Y, II X Y = (κ * ⟪X, Y⟫_ℝ) • ν)
    (hGauss : ∀ X Y Z W, R X Y Z W =
      spaceFormCurv Kbar X Y Z W + ⟪II Y Z, II X W⟫_ℝ - ⟪II X Z, II Y W⟫_ℝ)
    (X Y : E) (hX : ‖X‖ = 1) (hY : ‖Y‖ = 1) (hXY : ⟪X, Y⟫_ℝ = 0) :
    R X Y Y X = Kbar + κ ^ 2 := by
  have hYX : ⟪Y, X⟫_ℝ = 0 := by rw [real_inner_comm]; exact hXY
  have hνν : ⟪ν, ν⟫_ℝ = 1 := by rw [real_inner_self_eq_norm_sq, hν]; norm_num
  have hXX : ⟪X, X⟫_ℝ = 1 := by rw [real_inner_self_eq_norm_sq, hX]; norm_num
  have hYY : ⟪Y, Y⟫_ℝ = 1 := by rw [real_inner_self_eq_norm_sq, hY]; norm_num
  rw [hGauss, hUmb, hUmb, hUmb]
  simp only [spaceFormCurv, real_inner_smul_left, real_inner_smul_right, hνν, hXX, hYY, hXY, hYX]
  ring

/-- Modelo: curvatura constante `K̄ + κ²` (esfera geodesica/horosfera). Satisfaz a equacao de
Gauss com `II` umbilica para TODOS os `X, Y, Z, W` (nao so ortonormais). -/
theorem gauss_holds_for_model (II : E → E → N) (ν : N) (Kbar κ : ℝ) (hν : ‖ν‖ = 1)
    (hUmb : ∀ X Y, II X Y = (κ * ⟪X, Y⟫_ℝ) • ν) (X Y Z W : E) :
    spaceFormCurv (Kbar + κ ^ 2) X Y Z W =
      spaceFormCurv Kbar X Y Z W + ⟪II Y Z, II X W⟫_ℝ - ⟪II X Z, II Y W⟫_ℝ := by
  have hνν : ⟪ν, ν⟫_ℝ = 1 := by rw [real_inner_self_eq_norm_sq, hν]; norm_num
  simp only [hUmb, spaceFormCurv, real_inner_smul_left, real_inner_smul_right, hνν]
  ring

end Umbilic

/-- Vetores ortonormais concretos em `ℝ²`. -/
abbrev e2 (i : Fin 2) : EuclideanSpace ℝ (Fin 2) := EuclideanSpace.single i 1

lemma e2_norm (i : Fin 2) : ‖e2 i‖ = 1 := by simp [e2]

lemma e2_inner_01 : ⟪e2 0, e2 1⟫_ℝ = 0 := by simp [e2, EuclideanSpace.inner_single_left]

/-- **Testemunha nao degenerada (8.2)**: `E = ℝ²`, `N = ℝ`, `ν = 1`, `K̄ = 1`, `κ = 2`
(esfera umbilica em `S³(1)`), `R = spaceFormCurv 5`; todas as hipoteses valem e
`K_M(e₀,e₁) = 5 = K̄ + κ²`, com `K̄ ≠ 0` e `κ ≠ 0`. -/
theorem witness_coupling :
    let II : EuclideanSpace ℝ (Fin 2) → EuclideanSpace ℝ (Fin 2) → ℝ :=
      fun X Y => (2 * ⟪X, Y⟫_ℝ) • (1 : ℝ)
    let R : EuclideanSpace ℝ (Fin 2) → EuclideanSpace ℝ (Fin 2) →
        EuclideanSpace ℝ (Fin 2) → EuclideanSpace ℝ (Fin 2) → ℝ := spaceFormCurv 5
    ‖(1 : ℝ)‖ = 1 ∧ (∀ X Y, II X Y = (2 * ⟪X, Y⟫_ℝ) • (1 : ℝ)) ∧
      (∀ X Y Z W, R X Y Z W =
        spaceFormCurv 1 X Y Z W + ⟪II Y Z, II X W⟫_ℝ - ⟪II X Z, II Y W⟫_ℝ) ∧
      ‖e2 0‖ = 1 ∧ ‖e2 1‖ = 1 ∧ ⟪e2 0, e2 1⟫_ℝ = 0 ∧ R (e2 0) (e2 1) (e2 1) (e2 0) = 5 := by
  intro II R
  have hν : ‖(1 : ℝ)‖ = 1 := by simp
  have hU : ∀ X Y, II X Y = (2 * ⟪X, Y⟫_ℝ) • (1 : ℝ) := fun _ _ => rfl
  refine ⟨hν, hU, ?_, e2_norm 0, e2_norm 1, e2_inner_01, ?_⟩
  · intro X Y Z W
    have := gauss_holds_for_model II (1 : ℝ) 1 2 hν hU X Y Z W
    norm_num at this
    exact this
  · have := sectional_extrinsic_coupling R II (1 : ℝ) 1 2 hν hU
      (fun X Y Z W => by
        have := gauss_holds_for_model II (1 : ℝ) 1 2 hν hU X Y Z W
        norm_num at this
        exact this)
      (e2 0) (e2 1) (e2_norm 0) (e2_norm 1) e2_inner_01
    norm_num at this
    exact this

/-- **Mutante 8.2a** (sinal trocado, `K_M = K̄ - κ²`): FALSO, pela testemunha (`5 ≠ 1 - 4`). -/
theorem mutant_coupling_minus_false :
    ¬ (∀ (R : EuclideanSpace ℝ (Fin 2) → EuclideanSpace ℝ (Fin 2) →
          EuclideanSpace ℝ (Fin 2) → EuclideanSpace ℝ (Fin 2) → ℝ)
        (II : EuclideanSpace ℝ (Fin 2) → EuclideanSpace ℝ (Fin 2) → ℝ) (ν : ℝ) (Kbar κ : ℝ),
        ‖ν‖ = 1 → (∀ X Y, II X Y = (κ * ⟪X, Y⟫_ℝ) • ν) →
        (∀ X Y Z W, R X Y Z W =
          spaceFormCurv Kbar X Y Z W + ⟪II Y Z, II X W⟫_ℝ - ⟪II X Z, II Y W⟫_ℝ) →
        ∀ X Y, ‖X‖ = 1 → ‖Y‖ = 1 → ⟪X, Y⟫_ℝ = 0 → R X Y Y X = Kbar - κ ^ 2) := by
  intro h
  obtain ⟨hν, hU, hG, h0, h1, h01, h5⟩ := witness_coupling
  have := h _ _ 1 1 2 hν hU hG (e2 0) (e2 1) h0 h1 h01
  rw [h5] at this
  norm_num at this

/-- **Mutante 8.2b** (sem ortogonalidade, `X = Y` unitario): FALSO; `R(X,X,X,X) = 0 ≠ 5`. -/
theorem mutant_coupling_no_orth_false :
    ¬ (∀ (R : EuclideanSpace ℝ (Fin 2) → EuclideanSpace ℝ (Fin 2) →
          EuclideanSpace ℝ (Fin 2) → EuclideanSpace ℝ (Fin 2) → ℝ)
        (II : EuclideanSpace ℝ (Fin 2) → EuclideanSpace ℝ (Fin 2) → ℝ) (ν : ℝ) (Kbar κ : ℝ),
        ‖ν‖ = 1 → (∀ X Y, II X Y = (κ * ⟪X, Y⟫_ℝ) • ν) →
        (∀ X Y Z W, R X Y Z W =
          spaceFormCurv Kbar X Y Z W + ⟪II Y Z, II X W⟫_ℝ - ⟪II X Z, II Y W⟫_ℝ) →
        ∀ X Y, ‖X‖ = 1 → ‖Y‖ = 1 → R X Y Y X = Kbar + κ ^ 2) := by
  intro h
  obtain ⟨hν, hU, hG, h0, -, -, -⟩ := witness_coupling
  have := h _ _ 1 1 2 hν hU hG (e2 0) (e2 0) h0 h0
  simp only [spaceFormCurv] at this
  norm_num at this

/-! ## 8.7 Obstrucao de Raychaudhuri -/

/-- Metrica de Minkowski diagonal `η = diag(-1,1,1,1)` num referencial ortonormal. -/
def eta (μ : Fin 4) : ℝ := if μ = 0 then -1 else 1

/-- Contracao total `σ_{μν} σ^{μν} = Σ_{μ,ν} η_μ η_ν σ_{μν}²` (indices levantados com `η`). -/
def sqContract (σ : Fin 4 → Fin 4 → ℝ) : ℝ := ∑ μ, ∑ ν, eta μ * eta ν * σ μ ν ^ 2

/-- A definicao concorda com a contracao `η^{μα} η^{νβ} σ_{μν} σ_{αβ}` escrita com a matriz
diagonal (`η⁻¹ = η`). -/
lemma sqContract_eq_full (σ : Fin 4 → Fin 4 → ℝ) :
    sqContract σ = ∑ μ, ∑ ν, ∑ α, ∑ β,
      Matrix.diagonal eta μ α * Matrix.diagonal eta ν β * σ μ ν * σ α β := by
  simp only [sqContract, Matrix.diagonal_apply, ite_mul, zero_mul, mul_ite, mul_zero]
  simp [Finset.sum_ite_eq, pow_two]
  apply Finset.sum_congr rfl; intro μ _; apply Finset.sum_congr rfl; intro ν _; ring

/-- Com `σ` simetrico e espacial (`σ_{μ0} = 0`), `σ_{μν}σ^{μν}` e a soma dos quadrados das
componentes espaciais. -/
lemma sqContract_spatial (σ : Fin 4 → Fin 4 → ℝ) (hsymm : ∀ μ ν, σ μ ν = σ ν μ)
    (hV : ∀ μ, σ μ 0 = 0) :
    sqContract σ = σ 1 1 ^ 2 + σ 1 2 ^ 2 + σ 1 3 ^ 2 + σ 2 1 ^ 2 + σ 2 2 ^ 2 + σ 2 3 ^ 2 +
      σ 3 1 ^ 2 + σ 3 2 ^ 2 + σ 3 3 ^ 2 := by
  have h0 : ∀ ν, σ 0 ν = 0 := fun ν => by rw [hsymm]; exact hV ν
  simp [sqContract, Fin.sum_univ_four, eta, h0, hV]
  ring

lemma sqContract_nonneg (σ : Fin 4 → Fin 4 → ℝ) (hsymm : ∀ μ ν, σ μ ν = σ ν μ)
    (hV : ∀ μ, σ μ 0 = 0) : 0 ≤ sqContract σ := by
  rw [sqContract_spatial σ hsymm hV]; positivity

lemma sqContract_eq_zero_iff (σ : Fin 4 → Fin 4 → ℝ) (hsymm : ∀ μ ν, σ μ ν = σ ν μ)
    (hV : ∀ μ, σ μ 0 = 0) : sqContract σ = 0 ↔ σ = 0 := by
  constructor
  · intro h
    rw [sqContract_spatial σ hsymm hV] at h
    have h0 : ∀ ν, σ 0 ν = 0 := fun ν => by rw [hsymm]; exact hV ν
    funext μ ν
    simp only [Pi.zero_apply]
    fin_cases μ <;> fin_cases ν <;> simp [h0, hV] <;> nlinarith [sq_nonneg (σ 1 1),
      sq_nonneg (σ 1 2), sq_nonneg (σ 1 3), sq_nonneg (σ 2 1), sq_nonneg (σ 2 2),
      sq_nonneg (σ 2 3), sq_nonneg (σ 3 1), sq_nonneg (σ 3 2), sq_nonneg (σ 3 3)]
  · rintro rfl; simp [sqContract]

/-- **Proposicao `prop:raychaudhuri`** (item 8.7). Ao longo de uma curva da congruencia, com
`θ ≡ 0` num aberto `U`, vorticidade nula e shear simetrico espacial, a equacao de Raychaudhuri
(HIPOTESE `hRay`, `θ' = -θ²/3 - σσ + ωω - R_{μν}V^μV^ν`) da, em cada `τ ∈ U`,
`R_{μν}V^μV^ν = -σσ ≤ 0`, estrito onde `σ ≠ 0`. -/
theorem raychaudhuri_obstruction (U : Set ℝ) (hU : IsOpen U) (θ RicVV : ℝ → ℝ)
    (σ ω : ℝ → Fin 4 → Fin 4 → ℝ)
    (hRay : ∀ τ ∈ U, deriv θ τ =
      -(θ τ) ^ 2 / 3 - sqContract (σ τ) + sqContract (ω τ) - RicVV τ)
    (hθ : ∀ τ ∈ U, θ τ = 0) (hω : ∀ τ ∈ U, ω τ = 0)
    (hsymm : ∀ τ ∈ U, ∀ μ ν, σ τ μ ν = σ τ ν μ) (hV : ∀ τ ∈ U, ∀ μ, σ τ μ 0 = 0)
    (τ : ℝ) (hτ : τ ∈ U) :
    RicVV τ = -sqContract (σ τ) ∧ RicVV τ ≤ 0 ∧ (σ τ ≠ 0 → RicVV τ < 0) := by
  have hev : θ =ᶠ[nhds τ] fun _ => 0 :=
    Filter.eventuallyEq_of_mem (hU.mem_nhds hτ) (fun s hs => hθ s hs)
  have hd : deriv θ τ = 0 := by rw [hev.deriv_eq]; simp
  have hR := hRay τ hτ
  rw [hd, hθ τ hτ, hω τ hτ] at hR
  have hω0 : sqContract (0 : Fin 4 → Fin 4 → ℝ) = 0 := by simp [sqContract]
  rw [hω0] at hR
  have hRic : RicVV τ = -sqContract (σ τ) := by linarith
  have hnn := sqContract_nonneg (σ τ) (hsymm τ hτ) (hV τ hτ)
  refine ⟨hRic, by linarith, fun hne => ?_⟩
  have : sqContract (σ τ) ≠ 0 := fun h0 =>
    hne ((sqContract_eq_zero_iff (σ τ) (hsymm τ hτ) (hV τ hτ)).mp h0)
  have : 0 < sqContract (σ τ) := lt_of_le_of_ne hnn (Ne.symm this)
  linarith

/-- Shear sem traco concreto `diag(0, 1, -1, 0)`. -/
def shearW : Fin 4 → Fin 4 → ℝ := fun μ ν => if μ = ν then (if μ = 1 then 1 else
  if μ = 2 then -1 else 0) else 0

lemma sqContract_shearW : sqContract shearW = 2 := by
  simp [sqContract, shearW, Fin.sum_univ_four, eta]; norm_num

/-- **Testemunha nao degenerada (8.7)**: `U = ℝ`, `θ ≡ 0`, `ω ≡ 0`, shear `diag(0,1,-1,0)`
(nao nulo, sem traco, espacial), `R_{μν}V^μV^ν ≡ -2`; `hRay` vale e a conclusao estrita bite. -/
theorem witness_raychaudhuri :
    (∀ τ ∈ (Set.univ : Set ℝ), deriv (fun _ : ℝ => (0 : ℝ)) τ =
      -((fun _ : ℝ => (0 : ℝ)) τ) ^ 2 / 3 - sqContract shearW +
        sqContract (0 : Fin 4 → Fin 4 → ℝ) - (-2)) ∧
    (∀ μ ν, shearW μ ν = shearW ν μ) ∧ (∀ μ, shearW μ 0 = 0) ∧ shearW ≠ 0 ∧
    (-2 : ℝ) < 0 := by
  refine ⟨fun τ _ => by simp only [sqContract_shearW]; simp [sqContract], ?_, ?_, ?_,
    by norm_num⟩
  · intro μ ν; unfold shearW; split_ifs <;> simp_all
  · intro μ; fin_cases μ <;> simp [shearW]
  · intro h; have := congrFun (congrFun h 1) 1; simp [shearW] at this

example : (-2 : ℝ) = -sqContract shearW ∧ (-2 : ℝ) ≤ 0 ∧ (shearW ≠ 0 → (-2 : ℝ) < 0) := by
  obtain ⟨h1, h2, h3, -, -⟩ := witness_raychaudhuri
  exact raychaudhuri_obstruction Set.univ isOpen_univ (fun _ => 0) (fun _ => -2)
    (fun _ => shearW) (fun _ => 0) h1 (fun _ _ => rfl) (fun _ _ => rfl) (fun _ _ => h2)
    (fun _ _ => h3) 0 trivial

/-- **Mutante 8.7a** (sem `σ ⟂ V`): `σσ ≥ 0` para `σ` simetrico qualquer e FALSO;
`σ_{01} = σ_{10} = 1` da `σσ = -2`. -/
theorem mutant_shear_not_spatial_false :
    ¬ (∀ σ : Fin 4 → Fin 4 → ℝ, (∀ μ ν, σ μ ν = σ ν μ) → 0 ≤ sqContract σ) := by
  intro h
  have := h (fun μ ν => if (μ = 0 ∧ ν = 1) ∨ (μ = 1 ∧ ν = 0) then 1 else 0)
    (fun μ ν => by fin_cases μ <;> fin_cases ν <;> simp)
  simp [sqContract, Fin.sum_univ_four, eta] at this
  norm_num at this

/-- **Mutante 8.7b** (estrito sem `σ ≠ 0`): FALSO; com `σ = 0`, `R_{μν}V^μV^ν = 0`. -/
theorem mutant_strict_without_shear_false :
    ¬ (∀ (θ RicVV : ℝ → ℝ) (σ ω : ℝ → Fin 4 → Fin 4 → ℝ),
        (∀ τ, deriv θ τ = -(θ τ) ^ 2 / 3 - sqContract (σ τ) + sqContract (ω τ) - RicVV τ) →
        (∀ τ, θ τ = 0) → (∀ τ, ω τ = 0) → (∀ τ μ ν, σ τ μ ν = σ τ ν μ) →
        (∀ τ μ, σ τ μ 0 = 0) → RicVV 0 < 0) := by
  intro h
  have := h (fun _ => 0) (fun _ => 0) (fun _ => 0) (fun _ => 0)
    (fun τ => by simp [sqContract]) (fun _ => rfl) (fun _ => rfl) (fun _ _ _ => rfl)
    (fun _ _ => rfl)
  simp at this

/-! ## 8.8 Reissner–Nordstrom em Painleve–Gullstrand (nucleo algebrico) -/

/-- Raio do horizonte externo `r₊ = M + √(M² - Q²)`. -/
def rPlus (M Q : ℝ) : ℝ := M + √(M ^ 2 - Q ^ 2)

/-- `f(r) = 1 - 2M/r + Q²/r²`. -/
def fRN (M Q r : ℝ) : ℝ := 1 - 2 * M / r + Q ^ 2 / r ^ 2

/-- `β(r) = √(2M/r - Q²/r²)`. -/
def betaPG (M Q r : ℝ) : ℝ := √(2 * M / r - Q ^ 2 / r ^ 2)

/-- `prop:rn_horizon`: o radicando de `β` e positivo exatamente para `r > Q²/(2M)` (`r > 0`). -/
lemma betaPG_radicand_pos {M Q r : ℝ} (hM : 0 < M) (hr : Q ^ 2 / (2 * M) < r) :
    0 < 2 * M / r - Q ^ 2 / r ^ 2 := by
  have hr0 : 0 < r := lt_of_le_of_lt (by positivity) hr
  rw [div_lt_iff₀ (by positivity)] at hr
  have : 2 * M / r - Q ^ 2 / r ^ 2 = (2 * M * r - Q ^ 2) / r ^ 2 := by field_simp
  rw [this]; apply div_pos (by nlinarith) (by positivity)

/-- `β² = 1 - f` no dominio `r > Q²/(2M)`. -/
lemma betaPG_sq {M Q r : ℝ} (hM : 0 < M) (hr : Q ^ 2 / (2 * M) < r) :
    betaPG M Q r ^ 2 = 1 - fRN M Q r := by
  rw [betaPG, sq_sqrt (betaPG_radicand_pos hM hr).le, fRN]; ring

/-- `r₊ > Q²/(2M)` para `M > 0`, `|Q| ≤ M`: `r₊` esta no dominio da carta PG. -/
lemma rPlus_gt {M Q : ℝ} (hM : 0 < M) (hQ : |Q| ≤ M) : Q ^ 2 / (2 * M) < rPlus M Q := by
  have hQ2 : Q ^ 2 ≤ M ^ 2 := by
    have := sq_le_sq' (abs_le.mp hQ).1 (abs_le.mp hQ).2; simpa using this
  have hs : 0 ≤ √(M ^ 2 - Q ^ 2) := sqrt_nonneg _
  rw [div_lt_iff₀ (by positivity), rPlus]; nlinarith

/-- `f(r₊) = 0`. -/
lemma fRN_rPlus {M Q : ℝ} (hM : 0 < M) (hQ : |Q| ≤ M) : fRN M Q (rPlus M Q) = 0 := by
  have hQ2 : Q ^ 2 ≤ M ^ 2 := by
    have := sq_le_sq' (abs_le.mp hQ).1 (abs_le.mp hQ).2; simpa using this
  have hs2 : √(M ^ 2 - Q ^ 2) ^ 2 = M ^ 2 - Q ^ 2 := sq_sqrt (by linarith)
  have hr : 0 < rPlus M Q := by unfold rPlus; positivity
  unfold fRN
  rw [show (1 : ℝ) - 2 * M / rPlus M Q + Q ^ 2 / rPlus M Q ^ 2 =
      (rPlus M Q ^ 2 - 2 * M * rPlus M Q + Q ^ 2) / rPlus M Q ^ 2 by field_simp]
  apply div_eq_zero_iff.mpr; left
  unfold rPlus; nlinarith

/-- `β(r₊) = 1`. -/
theorem betaPG_rPlus {M Q : ℝ} (hM : 0 < M) (hQ : |Q| ≤ M) : betaPG M Q (rPlus M Q) = 1 := by
  have h := betaPG_sq hM (rPlus_gt hM hQ)
  rw [fRN_rPlus hM hQ, sub_zero] at h
  have hnn : 0 ≤ betaPG M Q (rPlus M Q) := sqrt_nonneg _
  nlinarith [h]

/-- **Proposicao `prop:rn_horizon`(2)**, nucleo algebrico (item 8.8). Com as componentes de
`K` como DADOS (`K^r_r = β'`, `K^θ_θ = K^φ_φ = β/r`, `K = traco`, `K_ss = K^r_r`) e
`D_i s^i = 2/r`, a expansao `θ_l = D_i s^i - K + K_ss` vale `2(1-β)/r`. O valor de
`K^r_r` (`= β'` no livro) cancela entre `-K` e `K_ss`; por isso `K^r_r` e um real ARBITRARIO
aqui (nenhuma hipotese `K^r_r = β'` e necessaria). -/
theorem theta_l_formula (r β divS Krr Kθθ Kφφ trK Kss θl : ℝ) (hdiv : divS = 2 / r)
    (hKθθ : Kθθ = β / r) (hKφφ : Kφφ = β / r)
    (htr : trK = Krr + Kθθ + Kφφ) (hss : Kss = Krr) (hθl : θl = divS - trK + Kss) :
    θl = 2 * (1 - β) / r := by
  subst hdiv hKθθ hKφφ htr hss hθl; ring

/-- **`prop:rn_horizon`(2)**: o horizonte `r = r₊` e MOTS, `θ_l = 0`, para `M > 0`, `|Q| ≤ M`,
qualquer `β'`. -/
theorem rn_horizon_mots {M Q : ℝ} (hM : 0 < M) (hQ : |Q| ≤ M)
    (divS Krr Kθθ Kφφ trK Kss θl : ℝ) (hdiv : divS = 2 / rPlus M Q)
    (hKθθ : Kθθ = betaPG M Q (rPlus M Q) / rPlus M Q)
    (hKφφ : Kφφ = betaPG M Q (rPlus M Q) / rPlus M Q)
    (htr : trK = Krr + Kθθ + Kφφ) (hss : Kss = Krr) (hθl : θl = divS - trK + Kss) :
    θl = 0 := by
  rw [theta_l_formula _ _ divS Krr Kθθ Kφφ trK Kss θl hdiv hKθθ hKφφ htr hss hθl,
    betaPG_rPlus hM hQ]; simp

/-- **Testemunha nao degenerada (8.8)**: `M = 1`, `Q = 1/2` (carregado, nao extremo),
`r₊ = 1 + √3/2`; `r₊ > Q²/(2M) = 1/8`, `β(r₊) = 1`, e `θ_l(r₊) = 0` com `β' = 7`. -/
example : rPlus 1 (1 / 2) = 1 + √3 / 2 ∧ (1 / 2 : ℝ) ^ 2 / (2 * 1) < rPlus 1 (1 / 2) ∧
    betaPG 1 (1 / 2) (rPlus 1 (1 / 2)) = 1 ∧
    (2 / rPlus 1 (1 / 2) - (7 + betaPG 1 (1 / 2) (rPlus 1 (1 / 2)) / rPlus 1 (1 / 2) +
      betaPG 1 (1 / 2) (rPlus 1 (1 / 2)) / rPlus 1 (1 / 2)) + 7 = 0) := by
  have hQ : |(1 / 2 : ℝ)| ≤ 1 := by rw [abs_of_pos (by norm_num)]; norm_num
  refine ⟨?_, rPlus_gt one_pos hQ, betaPG_rPlus one_pos hQ, ?_⟩
  · rw [rPlus, show (1 : ℝ) ^ 2 - (1 / 2) ^ 2 = 3 / 4 by norm_num, sqrt_div' _ (by norm_num),
      show (4 : ℝ) = 2 ^ 2 by norm_num, sqrt_sq (by norm_num)]
  · exact rn_horizon_mots one_pos hQ _ 7 _ _ _ _ _ rfl rfl rfl rfl rfl rfl

/-- **Mutante 8.8** ("o horizonte de Schwarzschild `r = 2M` e MOTS tambem com carga"):
FALSO; `M = Q = 1` da `β(2) = √(3/4) ≠ 1`. -/
theorem mutant_schwarzschild_radius_false :
    ¬ (∀ M Q : ℝ, 0 < M → |Q| ≤ M → betaPG M Q (2 * M) = 1) := by
  intro h
  have := h 1 1 one_pos (by simp)
  rw [betaPG, sqrt_eq_one] at this
  norm_num at this

/-! ## 8.10 Garganta de Morris–Thorne -/

/-- **`prop:wormhole_throat`(2)**: as curvaturas principais `√(1 - b/r)/r` das esferas
`r = const` anulam-se na garganta `b(r₀) = r₀`. -/
theorem throat_minimal (b : ℝ → ℝ) (r₀ : ℝ) (hr : 0 < r₀) (hb : b r₀ = r₀) :
    √(1 - b r₀ / r₀) / r₀ = 0 := by
  rw [hb, div_self hr.ne']; simp

/-- Curvatura de Gauss da esfera redonda de raio `r₀` (definicao, nao teorema). -/
def KGauss (r₀ : ℝ) : ℝ := 1 / r₀ ^ 2

/-- **`prop:wormhole_throat`(3)**, primeira parte (item 8.10). Com as componentes do tensor de
Einstein como HIPOTESES `hρ`, `hpr`, na garganta: `ρ + p_r = -(1 - b')/(8πG r₀²) < 0`. -/
theorem throat_nec (b Φ : ℝ → ℝ) (r₀ G ρ pr : ℝ) (hr : 0 < r₀) (hG : 0 < G)
    (hb : b r₀ = r₀) (hflare : deriv b r₀ < 1)
    (hρ : 8 * π * G * ρ = deriv b r₀ / r₀ ^ 2)
    (hpr : 8 * π * G * pr = -b r₀ / r₀ ^ 3 + 2 * (1 - b r₀ / r₀) * deriv Φ r₀ / r₀) :
    ρ + pr = -(1 - deriv b r₀) / (8 * π * G * r₀ ^ 2) ∧ ρ + pr < 0 := by
  have hc : 0 < 8 * π * G := by positivity
  simp only [hb, div_self hr.ne', sub_self, mul_zero, zero_mul, zero_div, add_zero] at hpr
  have hsum : 8 * π * G * (ρ + pr) = (deriv b r₀ - 1) / r₀ ^ 2 := by
    rw [mul_add, hρ, hpr]; field_simp; ring
  have heq : ρ + pr = -(1 - deriv b r₀) / (8 * π * G * r₀ ^ 2) := by
    rw [eq_div_iff (by positivity)]
    have : (deriv b r₀ - 1) / r₀ ^ 2 * r₀ ^ 2 = deriv b r₀ - 1 := by field_simp
    nlinarith [hsum, this]
  refine ⟨heq, ?_⟩
  rw [heq]; apply div_neg_of_neg_of_pos (by linarith) (by positivity)

/-- `ρ(r₀) ≥ 0 ↔ b'(r₀) ≥ 0` (sob `hρ`). -/
lemma rho_nonneg_iff (b : ℝ → ℝ) (r₀ G ρ : ℝ) (hr : 0 < r₀) (hG : 0 < G)
    (hρ : 8 * π * G * ρ = deriv b r₀ / r₀ ^ 2) : 0 ≤ ρ ↔ 0 ≤ deriv b r₀ := by
  have hc : 0 < 8 * π * G := by positivity
  have hr2 : 0 < r₀ ^ 2 := by positivity
  have hdb : deriv b r₀ = 8 * π * G * ρ * r₀ ^ 2 := by rw [hρ]; field_simp
  constructor
  · intro h; rw [hdb]; positivity
  · intro h
    by_contra hneg
    have hneg : ρ < 0 := lt_of_not_ge hneg
    have : 8 * π * G * ρ * r₀ ^ 2 < 0 :=
      mul_neg_of_neg_of_pos (mul_neg_of_pos_of_neg hc hneg) hr2
    linarith

/-- **`prop:wormhole_throat`(3)**, cota (item 8.10). Se ainda `b'(r₀) ≥ 0`, entao
`ρ + p_r ≥ -K_Gauss(S₀)/(8πG)`, com igualdade sse `b'(r₀) = 0`. -/
theorem throat_nec_bound (b Φ : ℝ → ℝ) (r₀ G ρ pr : ℝ) (hr : 0 < r₀) (hG : 0 < G)
    (hb : b r₀ = r₀) (hflare : deriv b r₀ < 1) (hb0 : 0 ≤ deriv b r₀)
    (hρ : 8 * π * G * ρ = deriv b r₀ / r₀ ^ 2)
    (hpr : 8 * π * G * pr = -b r₀ / r₀ ^ 3 + 2 * (1 - b r₀ / r₀) * deriv Φ r₀ / r₀) :
    -(1 / (8 * π * G)) * KGauss r₀ ≤ ρ + pr ∧
      (ρ + pr = -(1 / (8 * π * G)) * KGauss r₀ ↔ deriv b r₀ = 0) := by
  obtain ⟨heq, -⟩ := throat_nec b Φ r₀ G ρ pr hr hG hb hflare hρ hpr
  have hd : 0 < 8 * π * G * r₀ ^ 2 := by positivity
  have hK : -(1 / (8 * π * G)) * KGauss r₀ = -1 / (8 * π * G * r₀ ^ 2) := by
    unfold KGauss; field_simp
  rw [hK, heq]
  constructor
  · apply div_le_div_of_nonneg_right (by linarith) hd.le
  · constructor
    · intro h
      have := (div_left_inj' hd.ne').mp h
      linarith
    · intro h; rw [h]; ring_nf

/-- **Testemunha nao degenerada (8.10)**: `r₀ = 1`, `G = 1`, `b(r) = r/2 + 1/2`
(`b' = 1/2 ∈ (0,1)`), `Φ(r) = 3r` (`Φ' ≠ 0`), `ρ = 1/(16π)`, `p_r = -1/(8π)`. -/
theorem witness_throat :
    let b : ℝ → ℝ := fun r => r / 2 + 1 / 2
    let Φ : ℝ → ℝ := fun r => 3 * r
    b 1 = 1 ∧ deriv b 1 = 1 / 2 ∧ deriv Φ 1 = 3 ∧
      8 * π * 1 * (1 / (16 * π)) = deriv b 1 / 1 ^ 2 ∧
      8 * π * 1 * (-1 / (8 * π)) = -b 1 / 1 ^ 3 + 2 * (1 - b 1 / 1) * deriv Φ 1 / 1 := by
  intro b Φ
  have hπ : π ≠ 0 := pi_ne_zero
  have hdb : deriv b 1 = 1 / 2 := by
    have : HasDerivAt b (1 / 2) 1 := by
      have h := ((hasDerivAt_id (1 : ℝ)).div_const 2).add_const (1 / 2 : ℝ)
      exact h
    exact this.deriv
  have hdΦ : deriv Φ 1 = 3 := by
    have : HasDerivAt Φ 3 1 := by
      have h := (hasDerivAt_id (1 : ℝ)).const_mul (3 : ℝ)
      rw [mul_one] at h
      exact h
    exact this.deriv
  refine ⟨by norm_num [b], hdb, hdΦ, ?_, ?_⟩
  · rw [hdb]; field_simp; ring
  · rw [hdΦ]; simp only [b]; field_simp; ring

example : (1 / (16 * π) + -1 / (8 * π) : ℝ) < 0 ∧
    -(1 / (8 * π * 1)) * KGauss 1 < 1 / (16 * π) + -1 / (8 * π) := by
  obtain ⟨h1, h2, -, h4, h5⟩ := witness_throat
  have hf : deriv (fun r : ℝ => r / 2 + 1 / 2) 1 < 1 := by rw [h2]; norm_num
  have h0 : 0 ≤ deriv (fun r : ℝ => r / 2 + 1 / 2) 1 := by rw [h2]; norm_num
  obtain ⟨-, hlt⟩ := throat_nec _ _ 1 1 _ _ one_pos one_pos h1 hf h4 h5
  obtain ⟨hle, hiff⟩ := throat_nec_bound _ _ 1 1 _ _ one_pos one_pos h1 hf h0 h4 h5
  refine ⟨hlt, lt_of_le_of_ne hle fun h => ?_⟩
  have := hiff.mp h.symm
  rw [h2] at this; norm_num at this

/-- **Mutante 8.10a** (sem `b'(r₀) ≥ 0`): a cota `ρ + p_r ≥ -K_Gauss/(8πG)` e FALSA;
`b(r) = 2 - r`, `r₀ = G = 1`, `b' = -1`: `ρ + p_r = -2/(8π) < -1/(8π)`. -/
theorem mutant_bound_without_rho_nonneg_false :
    ¬ (∀ (b Φ : ℝ → ℝ) (r₀ G ρ pr : ℝ), 0 < r₀ → 0 < G → b r₀ = r₀ → deriv b r₀ < 1 →
        8 * π * G * ρ = deriv b r₀ / r₀ ^ 2 →
        8 * π * G * pr = -b r₀ / r₀ ^ 3 + 2 * (1 - b r₀ / r₀) * deriv Φ r₀ / r₀ →
        -(1 / (8 * π * G)) * KGauss r₀ ≤ ρ + pr) := by
  intro h
  have hπ : 0 < π := pi_pos
  have hdb : deriv (fun r : ℝ => 2 - r) 1 = -1 := by
    have : HasDerivAt (fun r : ℝ => 2 - r) (-1) 1 := by
      exact (hasDerivAt_id (1 : ℝ)).const_sub (2 : ℝ)
    exact this.deriv
  have := h (fun r => 2 - r) (fun _ => 0) 1 1 (-1 / (8 * π)) (-1 / (8 * π)) one_pos one_pos
    (by norm_num) (by rw [hdb]; norm_num) (by rw [hdb]; field_simp)
    (by norm_num; field_simp)
  unfold KGauss at this
  have e1 : -(1 / (8 * π * 1)) * (1 / 1 ^ 2) = -(1 / (8 * π)) := by ring
  have e2 : -1 / (8 * π) + -1 / (8 * π) = -(1 / (8 * π)) - 1 / (8 * π) := by ring
  have h8 : 0 < 1 / (8 * π) := by positivity
  rw [e1, e2] at this
  linarith

/-- **Mutante 8.10b** (sem flare-out `b' < 1`): `ρ + p_r < 0` e FALSO; `b = id`, `b' = 1`,
`ρ = 1/(8π)`, `p_r = -1/(8π)`. -/
theorem mutant_no_flare_false :
    ¬ (∀ (b Φ : ℝ → ℝ) (r₀ G ρ pr : ℝ), 0 < r₀ → 0 < G → b r₀ = r₀ →
        8 * π * G * ρ = deriv b r₀ / r₀ ^ 2 →
        8 * π * G * pr = -b r₀ / r₀ ^ 3 + 2 * (1 - b r₀ / r₀) * deriv Φ r₀ / r₀ →
        ρ + pr < 0) := by
  intro h
  have hπ : 0 < π := pi_pos
  have := h id (fun _ => 0) 1 1 (1 / (8 * π)) (-1 / (8 * π)) one_pos one_pos rfl
    (by rw [deriv_id]; field_simp) (by norm_num; field_simp)
  have : (1 / (8 * π) + -1 / (8 * π) : ℝ) = 0 := by ring
  linarith

/-! ## 8.11 Aceleracao propria em `ℝ^{1,3}` -/

/-- Forma de Minkowski `g = diag(-1,1,1,1)` em `ℝ⁴`. -/
def mink (x y : Fin 4 → ℝ) : ℝ := -x 0 * y 0 + x 1 * y 1 + x 2 * y 2 + x 3 * y 3

/-- Identidade de Lagrange com assinatura de Lorentz: sob `g(u,u) = -1`, `g(a,u) = 0`,
`u₀² g(a,a) = |ā|² + Σ_{i<j} (a_i u_j - a_j u_i)²`. -/
lemma mink_key (u a : Fin 4 → ℝ) (hu : mink u u = -1) (ha : mink a u = 0) :
    u 0 ^ 2 * mink a a = (a 1 ^ 2 + a 2 ^ 2 + a 3 ^ 2) + (a 1 * u 2 - a 2 * u 1) ^ 2 +
      (a 1 * u 3 - a 3 * u 1) ^ 2 + (a 2 * u 3 - a 3 * u 2) ^ 2 := by
  unfold mink at *
  linear_combination (-(a 1 ^ 2 + a 2 ^ 2 + a 3 ^ 2)) * hu +
    (a 1 * u 1 + a 2 * u 2 + a 3 * u 3 + a 0 * u 0) * ha

/-- **Proposicao `prop:proper_accel`** (item 8.11), parte "espacial ou nula": `g(u,u) = -1` e
`g(a,u) = 0` implicam `g(a,a) ≥ 0`. -/
theorem accel_nonneg (u a : Fin 4 → ℝ) (hu : mink u u = -1) (ha : mink a u = 0) :
    0 ≤ mink a a := by
  have hk := mink_key u a hu ha
  have hu0 : 1 ≤ u 0 ^ 2 := by
    unfold mink at hu
    nlinarith [sq_nonneg (u 1), sq_nonneg (u 2), sq_nonneg (u 3)]
  have hR : 0 ≤ u 0 ^ 2 * mink a a := by rw [hk]; positivity
  nlinarith

/-- `g(a,a) = 0 ↔ a = 0` sob as mesmas hipoteses (so `a = 0` e nulo). -/
theorem accel_null_iff (u a : Fin 4 → ℝ) (hu : mink u u = -1) (ha : mink a u = 0) :
    mink a a = 0 ↔ a = 0 := by
  constructor
  · intro h0
    have hk := mink_key u a hu ha
    rw [h0, mul_zero] at hk
    have h1 : a 1 = 0 := by
      nlinarith [sq_nonneg (a 1), sq_nonneg (a 2), sq_nonneg (a 3),
        sq_nonneg (a 1 * u 2 - a 2 * u 1), sq_nonneg (a 1 * u 3 - a 3 * u 1),
        sq_nonneg (a 2 * u 3 - a 3 * u 2)]
    have h2 : a 2 = 0 := by
      nlinarith [sq_nonneg (a 1), sq_nonneg (a 2), sq_nonneg (a 3),
        sq_nonneg (a 1 * u 2 - a 2 * u 1), sq_nonneg (a 1 * u 3 - a 3 * u 1),
        sq_nonneg (a 2 * u 3 - a 3 * u 2)]
    have h3 : a 3 = 0 := by
      nlinarith [sq_nonneg (a 1), sq_nonneg (a 2), sq_nonneg (a 3),
        sq_nonneg (a 1 * u 2 - a 2 * u 1), sq_nonneg (a 1 * u 3 - a 3 * u 1),
        sq_nonneg (a 2 * u 3 - a 3 * u 2)]
    have hu0 : u 0 ≠ 0 := by
      intro hz; unfold mink at hu; rw [hz] at hu
      nlinarith [sq_nonneg (u 1), sq_nonneg (u 2), sq_nonneg (u 3)]
    have h0' : a 0 = 0 := by
      unfold mink at ha; rw [h1, h2, h3] at ha
      have : a 0 * u 0 = 0 := by linarith
      exact (mul_eq_zero.mp this).resolve_right hu0
    funext i; fin_cases i <;> simp [h0', h1, h2, h3]
  · rintro rfl; simp [mink]

/-- `II(u,u) = a`: a projecao tangencial `g(a,u) u / g(u,u)` de `a` e nula. -/
theorem accel_normal (u a : Fin 4 → ℝ) (ha : mink a u = 0) :
    a - (mink a u / mink u u) • u = a := by
  rw [ha, zero_div, zero_smul, sub_zero]

/-- **Testemunha nao degenerada (8.11)**: `u = (5/3, 4/3, 0, 0)` (boost, `g(u,u) = -1`),
`a = (4, 5, 1, 0)` com `a₀ ≠ 0`, `g(a,u) = 0` e `g(a,a) = 10 > 0`. -/
theorem witness_accel :
    mink ![5/3, 4/3, 0, 0] ![5/3, 4/3, 0, 0] = -1 ∧ mink ![4, 5, 1, 0] ![5/3, 4/3, 0, 0] = 0 ∧
      mink ![4, 5, 1, 0] ![4, 5, 1, 0] = 10 := by
  refine ⟨?_, ?_, ?_⟩ <;> simp [mink] <;> norm_num

example : 0 ≤ mink ![4, 5, 1, 0] ![4, 5, 1, 0] :=
  accel_nonneg _ _ witness_accel.1 witness_accel.2.1

/-- **Mutante 8.11a** (curva espacial, `g(u,u) = +1`): `g(a,a) ≥ 0` e FALSO;
`u = e₁`, `a = e₀`, `g(a,a) = -1`. -/
theorem mutant_spacelike_curve_false :
    ¬ (∀ u a : Fin 4 → ℝ, mink u u = 1 → mink a u = 0 → 0 ≤ mink a a) := by
  intro h
  have := h ![0, 1, 0, 0] ![1, 0, 0, 0] (by simp [mink]) (by simp [mink])
  simp [mink] at this
  linarith

/-- **Mutante 8.11b** (curva nula, `g(u,u) = 0`): `g(a,a) = 0 → a = 0` e FALSO; `a = u`
nulo nao nulo. -/
theorem mutant_null_curve_false :
    ¬ (∀ u a : Fin 4 → ℝ, mink u u = 0 → mink a u = 0 → mink a a = 0 → a = 0) := by
  intro h
  have := h ![1, 1, 0, 0] ![1, 1, 0, 0] (by simp [mink]) (by simp [mink]) (by simp [mink])
  have := congrFun this 0
  simp at this

end LeanReal.Chap08Pointwise

#print axioms LeanReal.Chap08Pointwise.sectional_extrinsic_coupling
#print axioms LeanReal.Chap08Pointwise.gauss_holds_for_model
#print axioms LeanReal.Chap08Pointwise.witness_coupling
#print axioms LeanReal.Chap08Pointwise.mutant_coupling_minus_false
#print axioms LeanReal.Chap08Pointwise.mutant_coupling_no_orth_false
#print axioms LeanReal.Chap08Pointwise.sqContract_eq_full
#print axioms LeanReal.Chap08Pointwise.raychaudhuri_obstruction
#print axioms LeanReal.Chap08Pointwise.witness_raychaudhuri
#print axioms LeanReal.Chap08Pointwise.mutant_shear_not_spatial_false
#print axioms LeanReal.Chap08Pointwise.mutant_strict_without_shear_false
#print axioms LeanReal.Chap08Pointwise.betaPG_sq
#print axioms LeanReal.Chap08Pointwise.rPlus_gt
#print axioms LeanReal.Chap08Pointwise.betaPG_rPlus
#print axioms LeanReal.Chap08Pointwise.theta_l_formula
#print axioms LeanReal.Chap08Pointwise.rn_horizon_mots
#print axioms LeanReal.Chap08Pointwise.mutant_schwarzschild_radius_false
#print axioms LeanReal.Chap08Pointwise.throat_minimal
#print axioms LeanReal.Chap08Pointwise.throat_nec
#print axioms LeanReal.Chap08Pointwise.rho_nonneg_iff
#print axioms LeanReal.Chap08Pointwise.throat_nec_bound
#print axioms LeanReal.Chap08Pointwise.witness_throat
#print axioms LeanReal.Chap08Pointwise.mutant_bound_without_rho_nonneg_false
#print axioms LeanReal.Chap08Pointwise.mutant_no_flare_false
#print axioms LeanReal.Chap08Pointwise.accel_nonneg
#print axioms LeanReal.Chap08Pointwise.accel_null_iff
#print axioms LeanReal.Chap08Pointwise.accel_normal
#print axioms LeanReal.Chap08Pointwise.witness_accel
#print axioms LeanReal.Chap08Pointwise.mutant_spacelike_curve_false
#print axioms LeanReal.Chap08Pointwise.mutant_null_curve_false
