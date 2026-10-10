import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Complex.Basic

/-!
# Capitulo 4, Teorema "Simplicial Modulational Instability": nucleo algebrico
(item 2 do Lote A1, `PLANO_LIVRO_A.md`)

Fonte: `unified_quantum_gravity_book/chap04_simplicial_waves_porous_transport.tex`, subsecao
"Modulational Instability" (teorema sem rotulo).

Enunciado congelado. Com `V ≡ 0`, fundo `ψ₀ = √ρ₀ e^{-iμ₀t/ħ}`, `μ₀ = -κρ₀^p`, e perturbacoes
`(δu, δv) ∝ e^{i(k·x - Ωt)}`, o livro afirma:
* `ħ²Ω² = ε(ε - 2κpρ₀^p)`, com `ε = ħ²σ(k)/(2M)`;
* no regime focalizante `κ > 0`, instabilidade (`Ω² < 0`) para `σ(k) < 4Mκpρ₀^p/ħ²`;
* taxa maxima `γ_max = κpρ₀^p/ħ`, atingida em `σ(k) = 2Mκpρ₀^p/ħ²`.
A prova do livro: a linearizacao da `ħ∂_t δu = ε δv`, `ħ∂_t δv = -(ε - 2c) δu` (`c = κpρ₀^p`),
dai `ħ²Ω² = ε(ε - 2c)`, minimizado em `ε = c` com valor `-c²`.

## Reducao declarada

* A linearizacao da EDP (expansao de `|ψ|^{2p}` ate primeira ordem) NAO e formalizada: parte-se
  do sistema linear 2×2 do livro. (Conferi a mao que ele sai da NLSE com `-Δ ↦ σ`.)
* Um modo `(u,v) e^{-iΩt}` com `w = ħΩ ∈ ℂ` resolve o sistema sse `(-iw)u = εv` e
  `(-iw)v = -(ε-2c)u`. O teorema `mode_iff_dispersion` diz: existe modo nao nulo sse
  `w² = ε(ε-2c)`.
* "Instavel" = `Ω² < 0` (com `Ω² = ε(ε-2c)/ħ²` real). "Taxa de crescimento" = `|Im Ω|`.
* `σ(k)` entra como um numero real `σ ≥ 0`; a continuidade do simbolo e o conjunto ressonante
  ficam fora.

## Achado (registrado, o livro NAO foi editado)

O criterio do livro "instavel se `σ(k) < 4Mκpρ₀^p/ħ²`" omite `σ(k) > 0`: em `σ = 0`, `Ω = 0`
(o proprio livro observa isso para `k = 0`). O criterio correto e `0 < σ < 4Mc/ħ²`
(`unstable_iff`); `mutant_book_criterion_false` mostra que a versao sem `0 < σ` e falsa. A frase
"para `4Mc/ħ² > sup σ` todo `k ≠ 0` e instavel" precisa, pelo mesmo motivo, de `σ(k) > 0` para
`k ≠ 0`.
-/

noncomputable section

namespace LeanReal.Chap04Modulational

open Complex

/-- **Relacao de dispersao** (Teorema "Simplicial Modulational Instability", primeira afirmacao):
o sistema linearizado `(-iw)u = εv`, `(-iw)v = -(ε-2c)u` (com `w = ħΩ`) tem solucao nao nula
sse `w² = ε(ε - 2c)`. -/
theorem mode_iff_dispersion (ε c : ℝ) (w : ℂ) :
    (∃ u v : ℂ, (u ≠ 0 ∨ v ≠ 0) ∧ -I * w * u = ε * v ∧ -I * w * v = -((ε : ℂ) - 2 * c) * u) ↔
      w ^ 2 = ε * (ε - 2 * c) := by
  constructor
  · rintro ⟨u, v, huv, h1, h2⟩
    have hu : (w ^ 2 - ε * (ε - 2 * c)) * u = 0 := by
      linear_combination (I * w) * h1 - (ε : ℂ) * h2 + w ^ 2 * u * I_sq
    have hv : (w ^ 2 - ε * (ε - 2 * c)) * v = 0 := by
      linear_combination (I * w) * h2 + ((ε : ℂ) - 2 * c) * h1 + w ^ 2 * v * I_sq
    rcases huv with hu0 | hv0
    · exact sub_eq_zero.mp ((mul_eq_zero.mp hu).resolve_right hu0)
    · exact sub_eq_zero.mp ((mul_eq_zero.mp hv).resolve_right hv0)
  · intro hw
    by_cases hε : (ε : ℂ) = 0
    · have hw0 : w = 0 := by
        rw [hε, zero_mul] at hw; exact pow_eq_zero_iff (n := 2) (by norm_num) |>.mp hw
      exact ⟨0, 1, Or.inr one_ne_zero, by simp [hw0, hε], by simp [hw0]⟩
    · refine ⟨ε, -I * w, Or.inl hε, by ring, ?_⟩
      linear_combination w ^ 2 * I_sq - hw

/-- `ħ²Ω²` em funcao de `ε = ħ²σ/(2M)` e `c = κpρ₀^p`. -/
def omegaSqHbar (ε c : ℝ) : ℝ := ε * (ε - 2 * c)

/-- `ε = ħ²σ/(2M)`. -/
def eps (ħ M σ : ℝ) : ℝ := ħ ^ 2 * σ / (2 * M)

/-- `c = κpρ₀^p > 0` no regime focalizante. -/
theorem c_pos (κ p ρ₀ : ℝ) (hκ : 0 < κ) (hp : 0 < p) (hρ : 0 < ρ₀) : 0 < κ * p * ρ₀ ^ p := by
  have := Real.rpow_pos_of_pos hρ p
  positivity

/-- **Instabilidade**: para `c > 0`, `ħ²Ω² < 0` sse `0 < ε < 2c`. -/
theorem omegaSq_neg_iff (ε c : ℝ) (hc : 0 < c) : omegaSqHbar ε c < 0 ↔ 0 < ε ∧ ε < 2 * c := by
  unfold omegaSqHbar
  constructor
  · intro h
    rcases lt_trichotomy ε 0 with hn | hz | hp
    · nlinarith
    · subst hz; simp at h
    · exact ⟨hp, by nlinarith⟩
  · rintro ⟨h1, h2⟩; nlinarith

/-- **Instabilidade em termos do simbolo**: com `ħ, M, c > 0`, `Ω² < 0` sse
`0 < σ < 4Mc/ħ²` (o livro escreve so a cota superior; ver o achado no cabecalho). -/
theorem unstable_iff (ħ M c σ : ℝ) (hħ : 0 < ħ) (hM : 0 < M) (hc : 0 < c) :
    omegaSqHbar (eps ħ M σ) c / ħ ^ 2 < 0 ↔ 0 < σ ∧ σ < 4 * M * c / ħ ^ 2 := by
  have hħ2 : 0 < ħ ^ 2 := by positivity
  rw [div_lt_iff₀ hħ2, zero_mul, omegaSq_neg_iff _ _ hc]
  unfold eps
  have e1 : 0 < ħ ^ 2 * σ / (2 * M) ↔ 0 < σ := by
    rw [div_pos_iff_of_pos_right (by positivity)]
    exact ⟨fun h => pos_of_mul_pos_right h hħ2.le, fun h => mul_pos hħ2 h⟩
  have e2 : ħ ^ 2 * σ / (2 * M) < 2 * c ↔ σ < 4 * M * c / ħ ^ 2 := by
    rw [div_lt_iff₀ (by positivity), lt_div_iff₀ hħ2]
    constructor <;> intro h <;> nlinarith
  rw [e1, e2]

/-- **Minimo de `ħ²Ω²`**: `ε(ε - 2c) ≥ -c²`, com igualdade sse `ε = c`. -/
theorem omegaSq_ge (ε c : ℝ) : -c ^ 2 ≤ omegaSqHbar ε c := by
  unfold omegaSqHbar; nlinarith [sq_nonneg (ε - c)]

theorem omegaSq_eq_min_iff (ε c : ℝ) : omegaSqHbar ε c = -c ^ 2 ↔ ε = c := by
  unfold omegaSqHbar
  constructor
  · intro h
    have : (ε - c) ^ 2 = 0 := by linear_combination h
    exact sub_eq_zero.mp (pow_eq_zero_iff (n := 2) (by norm_num) |>.mp this)
  · rintro rfl; ring

/-- **Taxa maxima** `γ_max = c/ħ`: se `(ħΩ)² = ε(ε - 2c)`, entao `|Im Ω| ≤ c/ħ` (`c ≥ 0`). -/
theorem growth_le (ħ ε c : ℝ) (hħ : 0 < ħ) (hc : 0 ≤ c) (Ω : ℂ)
    (hΩ : ((ħ : ℂ) * Ω) ^ 2 = ε * (ε - 2 * c)) : |Ω.im| ≤ c / ħ := by
  have h := hΩ
  simp only [Complex.ext_iff, sq, Complex.mul_re, Complex.mul_im, Complex.ofReal_re,
    Complex.ofReal_im, zero_mul, sub_zero, add_zero, Complex.sub_re, Complex.sub_im,
    Complex.re_ofNat, Complex.im_ofNat, mul_zero] at h
  obtain ⟨hre, him⟩ := h
  have key : (ħ * Ω.im) ^ 2 ≤ c ^ 2 := by
    rcases eq_or_ne Ω.im 0 with h0 | h0
    · rw [h0, mul_zero, sq, mul_zero]; positivity
    · have ha : Ω.re = 0 := by
        by_contra hne
        have : ħ * Ω.re * (ħ * Ω.im) + ħ * Ω.im * (ħ * Ω.re) ≠ 0 := by
          have : ħ * Ω.re * (ħ * Ω.im) + ħ * Ω.im * (ħ * Ω.re) = 2 * ħ ^ 2 * Ω.re * Ω.im := by
            ring
          rw [this]; have := hħ.ne'; positivity
        exact this (by linarith [him])
      rw [ha] at hre
      nlinarith [sq_nonneg (ε - c)]
  rw [le_div_iff₀ hħ]
  have h2 : |ħ * Ω.im| ≤ c := abs_le_of_sq_le_sq' key hc |> fun h => abs_le.mpr h
  rwa [abs_mul, abs_of_pos hħ, mul_comm] at h2

/-- **Taxa maxima atingida** em `ε = c`: `Ω = i c/ħ` satisfaz a relacao de dispersao. -/
theorem growth_attained (ħ c : ℝ) (hħ : 0 < ħ) :
    ((ħ : ℂ) * (I * (c / ħ))) ^ 2 = (c : ℂ) * (c - 2 * c) ∧ (I * ((c : ℂ) / ħ)).im = c / ħ := by
  have hħ' : (ħ : ℂ) ≠ 0 := by exact_mod_cast hħ.ne'
  constructor
  · field_simp
    linear_combination (c : ℂ) ^ 2 * I_sq
  · simp [Complex.div_re, Complex.div_im]
    field_simp

/-! ## Testemunha nao degenerada

`ħ = M = κ = p = ρ₀ = 1` (logo `c = 1`), `σ = 2` (logo `ε = 1 = c`): o modo `(u,v) = (1,1)`
com `w = i` resolve o sistema, `Ω² = -1 < 0` (instavel) e `Im Ω = 1 = c/ħ` (taxa maxima). -/

example : (1 : ℝ) * 1 * (1 : ℝ) ^ (1 : ℝ) = 1 ∧ eps 1 1 2 = 1 ∧
    (-I * I * 1 = ((1 : ℝ) : ℂ) * 1 ∧ -I * I * 1 = -(((1 : ℝ) : ℂ) - 2 * ((1 : ℝ) : ℂ)) * 1) ∧
    omegaSqHbar (eps 1 1 2) 1 / 1 ^ 2 < 0 ∧ (0 < (2:ℝ) ∧ (2:ℝ) < 4 * 1 * 1 / 1 ^ 2) := by
  refine ⟨by simp, by norm_num [eps], ⟨by simp, by push_cast; ring_nf; simp⟩, ?_, by norm_num⟩
  norm_num [omegaSqHbar, eps]

/-- O modo da testemunha via o teorema (direcao `←`), com `ε = c = 1`, `w = i`. -/
example : ∃ u v : ℂ, (u ≠ 0 ∨ v ≠ 0) ∧ -I * I * u = ((1:ℝ):ℂ) * v ∧
    -I * I * v = -(((1:ℝ):ℂ) - 2 * ((1:ℝ):ℂ)) * u :=
  (mode_iff_dispersion 1 1 I).mpr (by push_cast; ring_nf; simp)

/-! ## Mutantes provados FALSOS -/

/-- Mutante 1 (criterio do livro sem `0 < σ`): "`σ < 4Mc/ħ²` implica `Ω² < 0`" e falso em
`σ = 0`. -/
theorem mutant_book_criterion_false :
    ¬ ∀ ħ M c σ : ℝ, 0 < ħ → 0 < M → 0 < c → σ < 4 * M * c / ħ ^ 2 →
      omegaSqHbar (eps ħ M σ) c / ħ ^ 2 < 0 := by
  intro h
  have := h 1 1 1 0 one_pos one_pos one_pos (by norm_num)
  norm_num [omegaSqHbar, eps] at this

/-- Mutante 2 (taxa maxima `2c/ħ` atingida): falso; a cota e `c/ħ`. Em `ħ = c = 1`, `ε = c`,
`Ω = i`, `|Im Ω| = 1 < 2`, e nenhum `Ω` com a relacao atinge `2`. -/
theorem mutant_double_rate_false :
    ¬ ∃ (ε : ℝ) (Ω : ℂ), ((1 : ℂ) * Ω) ^ 2 = ε * (ε - 2 * 1) ∧ |Ω.im| = 2 * 1 / 1 := by
  rintro ⟨ε, Ω, h1, h2⟩
  have := growth_le 1 ε 1 one_pos zero_le_one Ω (by simpa using h1)
  rw [h2] at this; norm_num at this

/-- Mutante 3 (relacao com sinal trocado, `w² = ε(ε + 2c)`): falso; o modo da testemunha
(`ε = c = 1`, `w = i`) existe, mas `i² = -1 ≠ 3`. -/
theorem mutant_sign_false :
    ¬ ∀ (ε c : ℝ) (w : ℂ),
      (∃ u v : ℂ, (u ≠ 0 ∨ v ≠ 0) ∧ -I * w * u = ε * v ∧ -I * w * v = -((ε : ℂ) - 2 * c) * u) →
        w ^ 2 = ε * (ε + 2 * c) := by
  intro h
  have := h 1 1 I ⟨1, 1, Or.inl one_ne_zero, by simp, by push_cast; ring_nf; simp⟩
  have := congrArg Complex.re this
  norm_num at this

end LeanReal.Chap04Modulational

#print axioms LeanReal.Chap04Modulational.mode_iff_dispersion
#print axioms LeanReal.Chap04Modulational.c_pos
#print axioms LeanReal.Chap04Modulational.omegaSq_neg_iff
#print axioms LeanReal.Chap04Modulational.unstable_iff
#print axioms LeanReal.Chap04Modulational.omegaSq_ge
#print axioms LeanReal.Chap04Modulational.omegaSq_eq_min_iff
#print axioms LeanReal.Chap04Modulational.growth_le
#print axioms LeanReal.Chap04Modulational.growth_attained
#print axioms LeanReal.Chap04Modulational.mutant_book_criterion_false
#print axioms LeanReal.Chap04Modulational.mutant_double_rate_false
#print axioms LeanReal.Chap04Modulational.mutant_sign_false
