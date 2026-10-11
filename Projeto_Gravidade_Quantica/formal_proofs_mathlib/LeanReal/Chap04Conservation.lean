import Mathlib.Analysis.Calculus.Deriv.Star
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.SpecialFunctions.Pow.Deriv
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Complex.RealDeriv
import Mathlib.Analysis.Complex.Trigonometric
import Mathlib.LinearAlgebra.Matrix.Hermitian
import Mathlib.LinearAlgebra.Matrix.Notation

/-!
# Capitulo 4, Teorema "Global Conservation of Mass and Energy" (item 3 do Lote B4 do
`PLANO_LIVRO_A.md`): reticulado finito

Fonte: `unified_quantum_gravity_book/chap04_simplicial_waves_porous_transport.tex`, subsecao
"Fundamental Conservation Laws".

Enunciado do livro. Para a NLSE simplicial (eq:nlse_main)
`iħ ∂_t ψ = −(ħ²/2M) Δ^α ψ + V ψ − κ |ψ|^{2p} ψ`, com `V` real independente de `t`, `ψ` solucao
suave com decaimento rapido no infinito:
> 1. `N[ψ(t)] = ∫ |ψ|² dx = N[ψ(0)]`;
> 2. `E[ψ(t)] = (ħ²/2M) ∫ σ |ψ̂|² dk + ∫ V |ψ|² dx − (κ/(p+1)) ∫ |ψ|^{2p+2} dx = E[ψ(0)]`,
> onde `∫ σ |ψ̂|² = ⟨ψ, −Δ^α ψ⟩`.
Prova do livro: (1) `(ħ/2) ∂_t|ψ|² = Im(−(ħ²/2M) ψ* Δψ)`, integra e usa `⟨ψ, Δψ⟩ ∈ ℝ`;
(2) `dE/dt = 2 Re ∫ ψ_t* (Hψ) = 2 Re(−(1/iħ)‖Hψ‖²) = 0`.

## Reducao declarada

* Reticulado FINITO: `ψ(t) : Fin n → ℂ`; o operador `Δ^α` e uma matriz HERMITIANA `D`
  (`Matrix.IsHermitian`), `⟨ψ, −Dψ⟩ = ∑_j conj(ψ_j)(−(Dψ)_j)` substitui `∫ σ |ψ̂|²`.
  `L²(ℝ^{m−1})`, o decaimento no infinito e a identidade de Plancherel ficam FORA.
* `V : Fin n → ℝ` (real, independente de `t`); `ħ, M, κ, p` reais; `|ψ|^{2p} = (normSq ψ)^p` com
  potencia real (`Real.rpow`); exige-se `0 < p` (o livro) e, para a massa, `ħ ≠ 0`.
* `ψ` derivavel em todo `t ∈ ℝ`, coordenada a coordenada (`hψ`), e resolve a equacao em todo
  `t` (`heq`). O livro pede "smooth"; so a diferenciabilidade e usada.
* Conteudo provado: as derivadas de `N` e `E` sao `2 Re ∑ conj(ψ_j) ψ'_j` e
  `2 Re ∑ conj(ψ'_j) (Hψ)_j`; com a equacao e a hermiticidade, ambas sao `0`; logo `N` e `E`
  sao constantes (`is_const_of_deriv_eq_zero`).
-/

noncomputable section

namespace LeanReal.Chap04Conservation

open Complex Matrix Finset ComplexConjugate

variable {n : ℕ}

/-- O lado direito da NLSE: `(Hψ)_j = −(ħ²/2M)(Dψ)_j + V_j ψ_j − κ |ψ_j|^{2p} ψ_j`. -/
def Hop (D : Matrix (Fin n) (Fin n) ℂ) (V : Fin n → ℝ) (ħ M κ p : ℝ) (ψ : Fin n → ℂ)
    (j : Fin n) : ℂ :=
  -((ħ ^ 2 / (2 * M) : ℝ) : ℂ) * (D.mulVec ψ) j + (V j : ℂ) * ψ j
    - (κ : ℂ) * ((normSq (ψ j) ^ p : ℝ) : ℂ) * ψ j

/-- Massa `N[ψ] = ∑_j |ψ_j|²`. -/
def mass (ψ : Fin n → ℂ) : ℝ := ∑ j, normSq (ψ j)

/-- Energia cinetica `⟨ψ, −Dψ⟩ = ∑_j conj(ψ_j)(−(Dψ)_j)` (parte real; e real se `D` e hermitiana). -/
def kinetic (D : Matrix (Fin n) (Fin n) ℂ) (ψ : Fin n → ℂ) : ℝ :=
  (∑ j, conj (ψ j) * (-((D.mulVec ψ) j))).re

/-- Energia `E[ψ] = (ħ²/2M)⟨ψ,−Dψ⟩ + ∑ V_j|ψ_j|² − (κ/(p+1)) ∑ |ψ_j|^{2p+2}`. -/
def energy (D : Matrix (Fin n) (Fin n) ℂ) (V : Fin n → ℝ) (ħ M κ p : ℝ) (ψ : Fin n → ℂ) : ℝ :=
  ħ ^ 2 / (2 * M) * kinetic D ψ + ∑ j, V j * normSq (ψ j)
    - κ / (p + 1) * ∑ j, normSq (ψ j) ^ (p + 1)

/-! ## Hermiticidade -/

/-- Para `D` hermitiana, `∑ conj(φ_j)(Dχ)_j = conj(∑ conj(χ_j)(Dφ)_j)`. -/
theorem herm_swap {D : Matrix (Fin n) (Fin n) ℂ} (hD : D.IsHermitian) (φ χ : Fin n → ℂ) :
    ∑ j, conj (φ j) * (D.mulVec χ) j = conj (∑ j, conj (χ j) * (D.mulVec φ) j) := by
  simp only [Matrix.mulVec, dotProduct, map_sum, map_mul, Complex.conj_conj, Finset.mul_sum]
  conv_lhs => rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun j _ => Finset.sum_congr rfl fun k _ => ?_
  have hDjk : (starRingEnd ℂ) (D j k) = D k j := by rw [starRingEnd_apply]; exact hD.apply k j
  rw [hDjk]; ring

/-- `⟨ψ, Dψ⟩ ∈ ℝ` para `D` hermitiana. -/
theorem inner_D_im {D : Matrix (Fin n) (Fin n) ℂ} (hD : D.IsHermitian) (ψ : Fin n → ℂ) :
    (∑ j, conj (ψ j) * (D.mulVec ψ) j).im = 0 :=
  Complex.conj_eq_iff_im.mp (herm_swap hD ψ ψ).symm

/-- `⟨ψ, Hψ⟩` em forma explicita. -/
theorem inner_Hop (D : Matrix (Fin n) (Fin n) ℂ) (V : Fin n → ℝ) (ħ M κ p : ℝ) (ψ : Fin n → ℂ) :
    ∑ j, conj (ψ j) * Hop D V ħ M κ p ψ j =
      -((ħ ^ 2 / (2 * M) : ℝ) : ℂ) * (∑ j, conj (ψ j) * (D.mulVec ψ) j)
        + ((∑ j, V j * normSq (ψ j) : ℝ) : ℂ)
        - ((κ * ∑ j, normSq (ψ j) ^ p * normSq (ψ j) : ℝ) : ℂ) := by
  simp only [Hop, Complex.ofReal_sum, Complex.ofReal_mul, Finset.mul_sum, ← Finset.sum_add_distrib,
    ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [Complex.normSq_eq_conj_mul_self]
  ring

/-- `⟨ψ, Hψ⟩ ∈ ℝ` (`D` hermitiana, `V` real): o passo "`⟨ψ, Δψ⟩ ∈ ℝ`" da prova do livro. -/
theorem inner_Hop_im {D : Matrix (Fin n) (Fin n) ℂ} (hD : D.IsHermitian) (V : Fin n → ℝ)
    (ħ M κ p : ℝ) (ψ : Fin n → ℂ) : (∑ j, conj (ψ j) * Hop D V ħ M κ p ψ j).im = 0 := by
  rw [inner_Hop, neg_mul, Complex.sub_im, Complex.add_im, Complex.neg_im, Complex.im_ofReal_mul,
    inner_D_im hD ψ, Complex.ofReal_im, Complex.ofReal_im]
  ring

/-! ## Derivadas -/

theorem hasDerivAt_conj {f : ℝ → ℂ} {f' : ℂ} {t : ℝ} (hf : HasDerivAt f f' t) :
    HasDerivAt (fun t => conj (f t)) (conj f') t := by
  simpa only [starRingEnd_apply] using hf.star

/-- `d/dt |f|² = 2 Re(conj(f) f')`. -/
theorem hasDerivAt_normSq {f : ℝ → ℂ} {f' : ℂ} {t : ℝ} (hf : HasDerivAt f f' t) :
    HasDerivAt (fun t => normSq (f t)) (2 * (conj (f t) * f').re) t := by
  have h := (hasDerivAt_conj hf).mul hf
  have h2 := Complex.reCLM.hasFDerivAt.comp_hasDerivAt t h
  have e : (fun t => normSq (f t)) = Complex.reCLM ∘ (fun t => conj (f t) * f t) := by
    funext t
    simp only [Function.comp, Complex.reCLM_apply, ← Complex.normSq_eq_conj_mul_self,
      Complex.ofReal_re]
  rw [e]
  refine h2.congr_deriv ?_
  simp only [Complex.reCLM_apply, Complex.add_re, Complex.mul_re, Complex.conj_re, Complex.conj_im]
  ring

/-- `d/dt |f|^{2(p+1)} = (p+1)|f|^{2p} · 2 Re(conj(f) f')`, para `p + 1 ≥ 1`. -/
theorem hasDerivAt_normSq_rpow {f : ℝ → ℂ} {f' : ℂ} {t : ℝ} (hf : HasDerivAt f f' t) (p : ℝ)
    (hp : 0 ≤ p) :
    HasDerivAt (fun t => normSq (f t) ^ (p + 1))
      ((p + 1) * normSq (f t) ^ p * (2 * (conj (f t) * f').re)) t := by
  have := (hasDerivAt_normSq hf).rpow_const (p := p + 1) (Or.inr (by linarith))
  rw [add_sub_cancel_right] at this
  exact this.congr_deriv (by ring)

variable (D : Matrix (Fin n) (Fin n) ℂ) (V : Fin n → ℝ) (ħ M κ p : ℝ)
  (ψ ψ' : ℝ → Fin n → ℂ)

/-- Derivada de `(Dψ)_j`. -/
theorem hasDerivAt_mulVec (hψ : ∀ t j, HasDerivAt (fun t => ψ t j) (ψ' t j) t) (t : ℝ)
    (j : Fin n) : HasDerivAt (fun t => (D.mulVec (ψ t)) j) ((D.mulVec (ψ' t)) j) t := by
  have := HasDerivAt.fun_sum (u := Finset.univ) (fun k _ => (hψ t k).const_mul (D j k))
  simpa [Matrix.mulVec, dotProduct] using this

/-- **Derivada da massa**: `dN/dt = 2 Re ∑_j conj(ψ_j) ψ'_j`. -/
theorem mass_hasDerivAt (hψ : ∀ t j, HasDerivAt (fun t => ψ t j) (ψ' t j) t) (t : ℝ) :
    HasDerivAt (fun t => mass (ψ t)) (2 * (∑ j, conj (ψ t j) * ψ' t j).re) t := by
  have := HasDerivAt.fun_sum (u := Finset.univ) (fun j _ => hasDerivAt_normSq (hψ t j))
  refine this.congr_deriv ?_
  simp only [Complex.re_sum, Finset.mul_sum]

/-- **Derivada da energia**: `dE/dt = 2 Re ∑_j conj(ψ'_j) (Hψ)_j`. -/
theorem energy_hasDerivAt (hD : D.IsHermitian) (hp : 0 < p)
    (hψ : ∀ t j, HasDerivAt (fun t => ψ t j) (ψ' t j) t) (t : ℝ) :
    HasDerivAt (fun t => energy D V ħ M κ p (ψ t))
      (2 * (∑ j, conj (ψ' t j) * Hop D V ħ M κ p (ψ t) j).re) t := by
  -- cinetica
  have hk0 : HasDerivAt (fun t => ∑ j, conj (ψ t j) * (-((D.mulVec (ψ t)) j)))
      (∑ j, (conj (ψ' t j) * (-((D.mulVec (ψ t)) j)) + conj (ψ t j) * (-((D.mulVec (ψ' t)) j)))) t :=
    HasDerivAt.fun_sum (u := Finset.univ) fun j _ =>
      (hasDerivAt_conj (hψ t j)).mul (hasDerivAt_mulVec D ψ ψ' hψ t j).neg
  have hk : HasDerivAt (fun t => kinetic D (ψ t))
      (2 * (∑ j, conj (ψ' t j) * (-((D.mulVec (ψ t)) j))).re) t := by
    have h2 := Complex.reCLM.hasFDerivAt.comp_hasDerivAt t hk0
    refine h2.congr_deriv ?_
    have key : ∑ j, conj (ψ t j) * (-((D.mulVec (ψ' t)) j)) =
        conj (∑ j, conj (ψ' t j) * (-((D.mulVec (ψ t)) j))) := by
      simp only [mul_neg, Finset.sum_neg_distrib, map_neg]
      rw [herm_swap hD]
    rw [Complex.reCLM_apply, Finset.sum_add_distrib, Complex.add_re, key, Complex.conj_re]
    ring
  -- potencial
  have hv : HasDerivAt (fun t => ∑ j, V j * normSq (ψ t j))
      (∑ j, V j * (2 * (conj (ψ t j) * ψ' t j).re)) t :=
    HasDerivAt.fun_sum (u := Finset.univ) fun j _ => (hasDerivAt_normSq (hψ t j)).const_mul (V j)
  -- nao linear
  have hn : HasDerivAt (fun t => ∑ j, normSq (ψ t j) ^ (p + 1))
      (∑ j, (p + 1) * normSq (ψ t j) ^ p * (2 * (conj (ψ t j) * ψ' t j).re)) t :=
    HasDerivAt.fun_sum (u := Finset.univ) fun j _ => hasDerivAt_normSq_rpow (hψ t j) p hp.le
  have htot := ((hk.const_mul (ħ ^ 2 / (2 * M))).add hv).sub (hn.const_mul (κ / (p + 1)))
  refine htot.congr_deriv ?_
  have hp1 : p + 1 ≠ 0 := by linarith
  simp only [Complex.re_sum, Finset.mul_sum, ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl fun j _ => ?_
  have hcancel : κ / (p + 1) * ((p + 1) * normSq (ψ t j) ^ p * (2 * (conj (ψ t j) * ψ' t j).re))
      = κ * normSq (ψ t j) ^ p * (2 * (conj (ψ t j) * ψ' t j).re) := by
    field_simp
  rw [hcancel]
  simp only [Hop, Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im, Complex.sub_re,
    Complex.sub_im, Complex.neg_re, Complex.neg_im, Complex.ofReal_re, Complex.ofReal_im,
    Complex.conj_re, Complex.conj_im]
  ring

/-! ## Conservacao -/

/-- **Teorema "Global Conservation", item 1 (massa), forma infinitesimal**: `dN/dt = 0`. -/
theorem mass_deriv_zero (hD : D.IsHermitian) (hħ : ħ ≠ 0)
    (hψ : ∀ t j, HasDerivAt (fun t => ψ t j) (ψ' t j) t)
    (heq : ∀ t j, Complex.I * (ħ : ℂ) * ψ' t j = Hop D V ħ M κ p (ψ t) j) (t : ℝ) :
    HasDerivAt (fun t => mass (ψ t)) 0 t := by
  refine (mass_hasDerivAt ψ ψ' hψ t).congr_deriv ?_
  set Z := ∑ j, conj (ψ t j) * ψ' t j with hZ
  have hW : Complex.I * (ħ : ℂ) * Z = ∑ j, conj (ψ t j) * Hop D V ħ M κ p (ψ t) j := by
    rw [hZ, Finset.mul_sum]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [← heq t j]; ring
  have him := inner_Hop_im hD V ħ M κ p (ψ t)
  rw [← hW] at him
  simp only [Complex.mul_im, Complex.mul_re, Complex.I_re, Complex.I_im, Complex.ofReal_re,
    Complex.ofReal_im, zero_mul, mul_zero, one_mul, sub_zero, zero_add] at him
  have : ħ * Z.re = 0 := by linarith
  rcases mul_eq_zero.mp this with h | h
  · exact absurd h hħ
  · rw [h]; ring

/-- **Teorema "Global Conservation", item 1 (massa)**: `N[ψ(t)] = N[ψ(0)]`. -/
theorem mass_conserved (hD : D.IsHermitian) (hħ : ħ ≠ 0)
    (hψ : ∀ t j, HasDerivAt (fun t => ψ t j) (ψ' t j) t)
    (heq : ∀ t j, Complex.I * (ħ : ℂ) * ψ' t j = Hop D V ħ M κ p (ψ t) j) (t : ℝ) :
    mass (ψ t) = mass (ψ 0) :=
  is_const_of_deriv_eq_zero
    (fun s => (mass_deriv_zero D V ħ M κ p ψ ψ' hD hħ hψ heq s).differentiableAt)
    (fun s => (mass_deriv_zero D V ħ M κ p ψ ψ' hD hħ hψ heq s).deriv) t 0

/-- **Teorema "Global Conservation", item 2 (energia), forma infinitesimal**: `dE/dt = 0`.
Aqui `ħ ≠ 0` nao e necessario: `conj(ψ'_j)(Hψ)_j = iħ |ψ'_j|²` e imaginario puro. -/
theorem energy_deriv_zero (hD : D.IsHermitian) (hp : 0 < p)
    (hψ : ∀ t j, HasDerivAt (fun t => ψ t j) (ψ' t j) t)
    (heq : ∀ t j, Complex.I * (ħ : ℂ) * ψ' t j = Hop D V ħ M κ p (ψ t) j) (t : ℝ) :
    HasDerivAt (fun t => energy D V ħ M κ p (ψ t)) 0 t := by
  refine (energy_hasDerivAt D V ħ M κ p ψ ψ' hD hp hψ t).congr_deriv ?_
  have : ∑ j, conj (ψ' t j) * Hop D V ħ M κ p (ψ t) j =
      Complex.I * (ħ : ℂ) * ((∑ j, normSq (ψ' t j) : ℝ) : ℂ) := by
    rw [Complex.ofReal_sum, Finset.mul_sum]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [← heq t j, Complex.normSq_eq_conj_mul_self]; ring
  rw [this]
  simp

/-- **Teorema "Global Conservation", item 2 (energia)**: `E[ψ(t)] = E[ψ(0)]`. -/
theorem energy_conserved (hD : D.IsHermitian) (hp : 0 < p)
    (hψ : ∀ t j, HasDerivAt (fun t => ψ t j) (ψ' t j) t)
    (heq : ∀ t j, Complex.I * (ħ : ℂ) * ψ' t j = Hop D V ħ M κ p (ψ t) j) (t : ℝ) :
    energy D V ħ M κ p (ψ t) = energy D V ħ M κ p (ψ 0) :=
  is_const_of_deriv_eq_zero
    (fun s => (energy_deriv_zero D V ħ M κ p ψ ψ' hD hp hψ heq s).differentiableAt)
    (fun s => (energy_deriv_zero D V ħ M κ p ψ ψ' hD hp hψ heq s).deriv) t 0

/-! ## Testemunha: um sitio, `D = [1]`, `V = 0`, `ħ = 1`, `M = 1/2`, `κ = 1`, `p = 1`

A equacao e `iψ' = −ψ − |ψ|²ψ`, resolvida por `ψ(t) = e^{2it}`: a parte linear e a nao linear
estao ambas ativas, `N = 1`, `E = −3/2`. -/

/-- `ψ_w(t) = e^{2it}` em um sitio. -/
def ψw (t : ℝ) : Fin 1 → ℂ := fun _ => exp (((2 * t : ℝ) : ℂ) * I)

/-- `ψ_w'(t) = 2i e^{2it}`. -/
def ψw' (t : ℝ) : Fin 1 → ℂ := fun _ => exp (((2 * t : ℝ) : ℂ) * I) * (2 * I)

theorem ψw_hasDerivAt (t : ℝ) (j : Fin 1) : HasDerivAt (fun t => ψw t j) (ψw' t j) t := by
  have h1 : HasDerivAt (fun t : ℝ => ((2 * t : ℝ) : ℂ) * I) (((2 * 1 : ℝ) : ℂ) * I) t :=
    (((hasDerivAt_id t).const_mul 2).ofReal_comp).mul_const I
  have h2 := h1.cexp
  unfold ψw ψw'
  convert h2 using 1
  push_cast; ring

theorem normSq_ψw (t : ℝ) (j : Fin 1) : normSq (ψw t j) = 1 := by
  rw [Complex.normSq_eq_norm_sq, ψw, Complex.norm_exp_ofReal_mul_I]; norm_num

theorem Dw_hermitian : (!![(1 : ℂ)] : Matrix (Fin 1) (Fin 1) ℂ).IsHermitian :=
  Matrix.IsHermitian.ext fun i j => by fin_cases i; fin_cases j; simp

theorem witness_equation (t : ℝ) (j : Fin 1) :
    Complex.I * ((1 : ℝ) : ℂ) * ψw' t j =
      Hop !![(1 : ℂ)] (fun _ => 0) 1 (1 / 2) 1 1 (ψw t) j := by
  have h := normSq_ψw t j
  simp only [Hop, Matrix.mulVec, dotProduct, Fin.sum_univ_one, h, Real.rpow_one]
  fin_cases j
  simp [ψw, ψw']
  ring_nf
  simp

theorem witness_mass (t : ℝ) : mass (ψw t) = 1 := by
  simp [mass, normSq_ψw]

theorem witness_energy (t : ℝ) : energy !![(1 : ℂ)] (fun _ => 0) 1 (1 / 2) 1 1 (ψw t) = -3 / 2 := by
  have h0 : normSq (ψw t 0) = 1 := normSq_ψw t 0
  have hk : kinetic !![(1 : ℂ)] (ψw t) = -1 := by
    simp only [kinetic, Matrix.mulVec, dotProduct, Fin.sum_univ_one]
    have : (starRingEnd ℂ) (ψw t 0) * -(!![(1 : ℂ)] 0 0 * ψw t 0) =
        -((normSq (ψw t 0) : ℝ) : ℂ) := by
      rw [Complex.normSq_eq_conj_mul_self]; simp
    rw [this, h0]; simp
  simp only [energy, hk, Fin.sum_univ_one, h0]
  norm_num

/-- As hipoteses do teorema valem na testemunha, e as conclusoes sao `N = 1`, `E = −3/2`. -/
theorem witness :
    (!![(1 : ℂ)] : Matrix (Fin 1) (Fin 1) ℂ).IsHermitian ∧ (1 : ℝ) ≠ 0 ∧ (0 : ℝ) < 1 ∧
    (∀ t j, HasDerivAt (fun t => ψw t j) (ψw' t j) t) ∧
    (∀ t j, Complex.I * ((1 : ℝ) : ℂ) * ψw' t j =
      Hop !![(1 : ℂ)] (fun _ => 0) 1 (1 / 2) 1 1 (ψw t) j) ∧
    (∀ t, mass (ψw t) = 1) ∧
    (∀ t, energy !![(1 : ℂ)] (fun _ => 0) 1 (1 / 2) 1 1 (ψw t) = -3 / 2) :=
  ⟨Dw_hermitian, one_ne_zero, one_pos, ψw_hasDerivAt, witness_equation, witness_mass,
    witness_energy⟩

/-! ## Mutantes provados FALSOS: sem a hermiticidade de `D`

`D = [1 + i]`, `ħ = 1`, `M = 1/2`, `V = 0`, `κ = 0`: a equacao `iψ' = −(1+i)ψ` tem a solucao
`ψ(t) = e^{(i−1)t}`, com `N(t) = e^{−2t}` e `E(t) = −e^{−2t}`, nao constantes. -/

/-- `ψ_m(t) = e^{(i−1)t}`. -/
def ψm (t : ℝ) : Fin 1 → ℂ := fun _ => exp ((I - 1) * (t : ℂ))

/-- `ψ_m'(t) = (i−1) e^{(i−1)t}`. -/
def ψm' (t : ℝ) : Fin 1 → ℂ := fun _ => exp ((I - 1) * (t : ℂ)) * (I - 1)

theorem ψm_hasDerivAt (t : ℝ) (j : Fin 1) : HasDerivAt (fun t => ψm t j) (ψm' t j) t := by
  have h1 : HasDerivAt (fun t : ℝ => (I - 1) * (t : ℂ)) ((I - 1) * ((1 : ℝ) : ℂ)) t :=
    (hasDerivAt_id t).ofReal_comp.const_mul (I - 1)
  have h2 := h1.cexp
  unfold ψm ψm'
  convert h2 using 1
  push_cast; ring

theorem ψm_equation (t : ℝ) (j : Fin 1) :
    Complex.I * ((1 : ℝ) : ℂ) * ψm' t j =
      Hop !![(1 + I : ℂ)] (fun _ => 0) 1 (1 / 2) 0 1 (ψm t) j := by
  simp only [Hop, Matrix.mulVec, dotProduct, Fin.sum_univ_one]
  fin_cases j
  simp [ψm, ψm']
  ring_nf
  simp [Complex.ext_iff]
  all_goals (try constructor) <;> ring

theorem normSq_ψm (t : ℝ) (j : Fin 1) : normSq (ψm t j) = Real.exp (-2 * t) := by
  rw [Complex.normSq_eq_norm_sq, ψm, Complex.norm_exp, ← Real.exp_nat_mul]
  congr 1
  simp [Complex.mul_re]

theorem exp_neg_two_ne_one : Real.exp (-2 * 1) ≠ 1 := by
  have := Real.exp_lt_exp.mpr (show (-2 * 1 : ℝ) < 0 by norm_num)
  rw [Real.exp_zero] at this
  exact this.ne

/-- Mutante 1: sem `D` hermitiana, a massa NAO e conservada. -/
theorem mutant_mass_no_hermitian_false :
    ¬ (∀ (D : Matrix (Fin 1) (Fin 1) ℂ) (V : Fin 1 → ℝ) (ħ M κ p : ℝ) (ψ ψ' : ℝ → Fin 1 → ℂ),
        ħ ≠ 0 → 0 < p → (∀ t j, HasDerivAt (fun t => ψ t j) (ψ' t j) t) →
        (∀ t j, Complex.I * (ħ : ℂ) * ψ' t j = Hop D V ħ M κ p (ψ t) j) →
        ∀ t, mass (ψ t) = mass (ψ 0)) := by
  intro h
  have := h !![(1 + I : ℂ)] (fun _ => 0) 1 (1 / 2) 0 1 ψm ψm' one_ne_zero one_pos ψm_hasDerivAt
    ψm_equation 1
  simp only [mass, Fin.sum_univ_one, normSq_ψm] at this
  norm_num [Real.exp_eq_one_iff] at this

/-- Mutante 2: sem `D` hermitiana, a energia NAO e conservada. -/
theorem mutant_energy_no_hermitian_false :
    ¬ (∀ (D : Matrix (Fin 1) (Fin 1) ℂ) (V : Fin 1 → ℝ) (ħ M κ p : ℝ) (ψ ψ' : ℝ → Fin 1 → ℂ),
        0 < p → (∀ t j, HasDerivAt (fun t => ψ t j) (ψ' t j) t) →
        (∀ t j, Complex.I * (ħ : ℂ) * ψ' t j = Hop D V ħ M κ p (ψ t) j) →
        ∀ t, energy D V ħ M κ p (ψ t) = energy D V ħ M κ p (ψ 0)) := by
  intro h
  have := h !![(1 + I : ℂ)] (fun _ => 0) 1 (1 / 2) 0 1 ψm ψm' one_pos ψm_hasDerivAt
    ψm_equation 1
  have hk : ∀ t, kinetic !![(1 + I : ℂ)] (ψm t) = -Real.exp (-2 * t) := by
    intro t
    simp only [kinetic, Matrix.mulVec, dotProduct, Fin.sum_univ_one]
    have e : (starRingEnd ℂ) (ψm t 0) * -(!![(1 + I : ℂ)] 0 0 * ψm t 0) =
        -((1 + I) * ((normSq (ψm t 0) : ℝ) : ℂ)) := by
      have hD00 : (!![(1 + I : ℂ)] : Matrix (Fin 1) (Fin 1) ℂ) 0 0 = 1 + I := by simp
      rw [hD00, Complex.normSq_eq_conj_mul_self]; ring
    rw [e, normSq_ψm]
    simp only [Complex.neg_re, Complex.mul_re, Complex.add_re, Complex.add_im, Complex.one_re,
      Complex.one_im, Complex.I_re, Complex.I_im, Complex.ofReal_re, Complex.ofReal_im]
    ring
  simp only [energy, hk, Fin.sum_univ_one] at this
  norm_num [Real.exp_eq_one_iff] at this

end LeanReal.Chap04Conservation

#print axioms LeanReal.Chap04Conservation.herm_swap
#print axioms LeanReal.Chap04Conservation.inner_Hop_im
#print axioms LeanReal.Chap04Conservation.mass_hasDerivAt
#print axioms LeanReal.Chap04Conservation.energy_hasDerivAt
#print axioms LeanReal.Chap04Conservation.mass_deriv_zero
#print axioms LeanReal.Chap04Conservation.mass_conserved
#print axioms LeanReal.Chap04Conservation.energy_deriv_zero
#print axioms LeanReal.Chap04Conservation.energy_conserved
#print axioms LeanReal.Chap04Conservation.witness
#print axioms LeanReal.Chap04Conservation.mutant_mass_no_hermitian_false
#print axioms LeanReal.Chap04Conservation.mutant_energy_no_hermitian_false
