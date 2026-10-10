import LeanReal.Chap08UTurn
import Mathlib.Analysis.SpecialFunctions.Arsinh
import Mathlib.Analysis.SpecialFunctions.Trigonometric.InverseDeriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds

/-!
# Capitulo 8, `prop:space_form_uturn` (lote B6 do `PLANO_LIVRO_B.md`, item 8.4)

Fonte: `unified_quantum_gravity_book/chap08_noneuclidean_minimax_relativity_adm.tex`, Teorema
"U-turns in tubes of space forms" (`prop:space_form_uturn`): seja `w > 0` (`w < π/c` em
`𝕊²(+c²)`). Uma U-turn no tubo `T_w = {|y| ≤ w/2}` (coordenadas de Fermi
`g = dy² + G(y)² dx²`, `G = cosh(c y)` em `ℍ²(-c²)`, `cos(c y)` em `𝕊²(+c²)`), com
`γ'(0) = e_x`, `γ'(L) = -e_x` e `|κ| ≤ k` q.t.p., satisfaz `k ≥ c coth(cw/2)` em `ℍ²` e
`k ≥ c cot(cw/2)` em `𝕊²`; as cotas sao atingidas pelo semicirculo geodesico de raio `w/2`.

## Reducao declarada (coordenadas de Fermi)

* A curva entra so pelas funcoes `y(s)` (distancia com sinal a geodesica `σ`), `θ(s)` (angulo com
  o referencial `(e_x, e_y)`), `u(s) = g(γ', ∂_x)` e `κ(s)` (curvatura geodesica), em `[0,L]`.
* Hipoteses: `y' = sin θ` em `(0,L)` (derivada classica); `θ` continua; `θ(0) = 0` e
  `cos θ(L) = -1` (tangentes `e_x` e `-e_x`); `|κ| ≤ k` em `(0,L)`; `|y| ≤ w/2` em `[0,L]`.
* **Hipotese que substitui teoria ausente:** `hClairaut`, a identidade de Clairaut/Killing
  `u = G(y) cos θ`, `u' = -κ G(y) sin θ` (eq. `eq:clairaut`). Ela vem da conexao de Levi-Civita e
  do campo de Killing `∂_x`, que NAO sao derivados aqui (a Mathlib nao tem a geometria
  riemanniana necessaria). Pede-se `u` derivavel em todo ponto de `(0,L)`; o livro pede so
  Lipschitz com a identidade q.t.p. (caso nao coberto).
* Prova: a selecao da meia-volta (`Chap08UTurn.exists_halfturn_window`) e a monotonia de
  `k F(y) + u` (com `F' = G`), que da `G(a) + G(b) ≤ k ∫_a^b G` sem integrais. Depois as
  identidades `cosh`/`cos` de soma e produto e a monotonia de `coth`/`cot` (sem `coth` na
  Mathlib: a conclusao e escrita `c cosh(cw/2) ≤ k sinh(cw/2)`, e a forma com divisao e dada).
* O nucleo `warped_uturn_core` vale para qualquer `G ≥ 0` com primitiva `F` (a observacao do
  livro sobre tubos com metrica `dy² + G(y)²dx²`); `G ≡ 1` da de novo `lem:euclidean_uturn`.
* Testemunhas: o semicirculo geodesico, escrito explicitamente em coordenadas de Fermi
  (`sinh(c y) = -sinh(cw/2) cos(c s / sinh(cw/2))` em `ℍ²`, o analogo com `sin` em `𝕊²`), com
  `κ` constante igual a cota: todas as hipoteses valem e a conclusao vale com igualdade. Que essas
  funcoes descrevem o circulo geodesico de `ℍ²`/`𝕊²` nao e provado aqui (seria geometria); o que
  se prova e que satisfazem as hipoteses da reducao.
-/

noncomputable section

namespace LeanReal.Chap08SpaceForms

open Set Real

/-- Monotonia via derivada num intervalo fechado. -/
theorem le_of_deriv_nonneg' {f f' : ℝ → ℝ} {a b : ℝ} (hab : a ≤ b)
    (hc : ContinuousOn f (Icc a b)) (hd : ∀ s ∈ Ioo a b, HasDerivAt f (f' s) s)
    (hnn : ∀ s ∈ Ioo a b, 0 ≤ f' s) : f a ≤ f b := by
  have := monotoneOn_of_hasDerivWithinAt_nonneg (convex_Icc a b) hc
    (fun s hs => by rw [interior_Icc] at hs; exact (hd s hs).hasDerivWithinAt)
    (fun s hs => by rw [interior_Icc] at hs; exact hnn s hs)
  exact this ⟨le_rfl, hab⟩ ⟨hab, le_rfl⟩ hab

/-! ## O nucleo: tubo com metrica `dy² + G(y)² dx²` -/

/-- **Nucleo de `prop:space_form_uturn`** (e da observacao sobre tubos gerais): para `G ≥ 0`
no tubo, com primitiva `F`, uma U-turn na reducao de Fermi tem `-w/2 ≤ lo ≤ hi ≤ w/2` com
`G(lo) + G(hi) ≤ k (F(hi) - F(lo))`, isto e `G(a) + G(b) ≤ k ∫_a^b G`. -/
theorem warped_uturn_core (G F : ℝ → ℝ) (y θ u κ : ℝ → ℝ) (L k w : ℝ) (hL : 0 ≤ L)
    (hF : ∀ t ∈ Icc (-(w / 2)) (w / 2), HasDerivAt F (G t) t)
    (hG : ∀ t ∈ Icc (-(w / 2)) (w / 2), 0 ≤ G t)
    (hyc : ContinuousOn y (Icc 0 L)) (hy : ∀ s ∈ Ioo 0 L, HasDerivAt y (sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L)) (huc : ContinuousOn u (Icc 0 L))
    (hu : ∀ s ∈ Icc 0 L, u s = G (y s) * cos (θ s))
    (hClairaut : ∀ s ∈ Ioo 0 L, HasDerivAt u (-(κ s * G (y s) * sin (θ s))) s)
    (hκ : ∀ s ∈ Ioo 0 L, |κ s| ≤ k) (h0 : θ 0 = 0) (hend : cos (θ L) = -1)
    (htube : ∀ s ∈ Icc 0 L, y s ∈ Icc (-(w / 2)) (w / 2)) :
    ∃ lo hi, -(w / 2) ≤ lo ∧ lo ≤ hi ∧ hi ≤ w / 2 ∧ G lo + G hi ≤ k * (F hi - F lo) := by
  have hFc : ContinuousOn F (Icc (-(w / 2)) (w / 2)) :=
    fun t ht => (hF t ht).continuousAt.continuousWithinAt
  have hturn : π ≤ |θ L - θ 0| := by
    rw [h0, sub_zero]; exact LeanReal.Chap08UTurn.pi_le_abs_of_cos_eq_neg_one hend
  have hFy : ∀ s ∈ Ioo 0 L, HasDerivAt (fun s => F (y s)) (G (y s) * sin (θ s)) s :=
    fun s hs => (hF (y s) (htube s (Ioo_subset_Icc_self hs))).comp s (hy s hs)
  have hFyc : ContinuousOn (fun s => F (y s)) (Icc 0 L) :=
    hFc.comp hyc (fun s hs => htube s hs)
  rcases le_abs'.mp hturn with hneg | hpos
  · -- θ desce `π`: janela para `-θ`
    have hrise : (fun s => -θ s) 0 + π ≤ (fun s => -θ s) L := by simp only; linarith
    obtain ⟨a, b, h0a, hab, hbL, ha, hb, hrange⟩ :=
      LeanReal.Chap08UTurn.exists_halfturn_window hL hθc.neg hrise
    simp only [Pi.neg_apply, h0, neg_zero, zero_add] at ha hb hrange
    have hS : Icc a b ⊆ Icc 0 L := Icc_subset_Icc h0a hbL
    have hSo : Ioo a b ⊆ Ioo 0 L := Ioo_subset_Ioo h0a hbL
    have hsin : ∀ s ∈ Ioo a b, sin (θ s) ≤ 0 := fun s hs => by
      have h1 := hrange s (Ioo_subset_Icc_self hs)
      have h2 := sin_nonneg_of_nonneg_of_le_pi h1.1 h1.2
      rw [sin_neg] at h2; linarith
    have hy_ab : y b ≤ y a := by
      have := le_of_deriv_nonneg' (f := fun s => -y s) (f' := fun s => -sin (θ s)) hab
        (hyc.neg.mono hS) (fun s hs => (hy s (hSo hs)).neg)
        (fun s hs => by linarith [hsin s hs])
      linarith
    have hH := le_of_deriv_nonneg' (f := fun s => u s - k * F (y s))
        (f' := fun s => -(κ s * G (y s) * sin (θ s)) - k * (G (y s) * sin (θ s))) hab
        ((huc.mono hS).sub (continuousOn_const.mul (hFyc.mono hS)))
        (fun s hs => (hClairaut s (hSo hs)).sub ((hFy s (hSo hs)).const_mul k))
        (fun s hs => by
          have hk := abs_le.mp (hκ s (hSo hs))
          have hGs := hG (y s) (htube s (hS (Ioo_subset_Icc_self hs)))
          have := hsin s hs
          have e : -(κ s * G (y s) * sin (θ s)) - k * (G (y s) * sin (θ s)) =
              (κ s + k) * G (y s) * (-sin (θ s)) := by ring
          rw [e]; exact mul_nonneg (mul_nonneg (by linarith) hGs) (by linarith))
    try simp only at hH
    rw [hu a (hS ⟨le_rfl, hab⟩), hu b (hS ⟨hab, le_rfl⟩)] at hH
    have hθa : θ a = 0 := by linarith
    have hθb : θ b = -π := by linarith
    rw [hθa, hθb, cos_zero, cos_neg, cos_pi] at hH
    exact ⟨y b, y a, (htube b (hS ⟨hab, le_rfl⟩)).1, hy_ab, (htube a (hS ⟨le_rfl, hab⟩)).2,
      by linarith⟩
  · -- θ sobe `π`
    have hrise : θ 0 + π ≤ θ L := by linarith
    obtain ⟨a, b, h0a, hab, hbL, ha, hb, hrange⟩ :=
      LeanReal.Chap08UTurn.exists_halfturn_window hL hθc hrise
    rw [h0] at ha hb hrange
    simp only [zero_add] at hb hrange
    have hS : Icc a b ⊆ Icc 0 L := Icc_subset_Icc h0a hbL
    have hSo : Ioo a b ⊆ Ioo 0 L := Ioo_subset_Ioo h0a hbL
    have hsin : ∀ s ∈ Ioo a b, 0 ≤ sin (θ s) := fun s hs => by
      have h1 := hrange s (Ioo_subset_Icc_self hs)
      exact sin_nonneg_of_nonneg_of_le_pi h1.1 h1.2
    have hy_ab : y a ≤ y b :=
      le_of_deriv_nonneg' (f := y) (f' := fun s => sin (θ s)) hab (hyc.mono hS)
        (fun s hs => hy s (hSo hs)) hsin
    have hH := le_of_deriv_nonneg' (f := fun s => k * F (y s) + u s)
        (f' := fun s => k * (G (y s) * sin (θ s)) + -(κ s * G (y s) * sin (θ s))) hab
        ((continuousOn_const.mul (hFyc.mono hS)).add (huc.mono hS))
        (fun s hs => ((hFy s (hSo hs)).const_mul k).add (hClairaut s (hSo hs)))
        (fun s hs => by
          have hk := abs_le.mp (hκ s (hSo hs))
          have hGs := hG (y s) (htube s (hS (Ioo_subset_Icc_self hs)))
          have := hsin s hs
          have e : k * (G (y s) * sin (θ s)) + -(κ s * G (y s) * sin (θ s)) =
              (k - κ s) * G (y s) * sin (θ s) := by ring
          rw [e]; exact mul_nonneg (mul_nonneg (by linarith) hGs) this)
    try simp only at hH
    rw [hu a (hS ⟨le_rfl, hab⟩), hu b (hS ⟨hab, le_rfl⟩), ha, hb, cos_zero, cos_pi] at hH
    exact ⟨y a, y b, (htube a (hS ⟨le_rfl, hab⟩)).1, hy_ab, (htube b (hS ⟨hab, le_rfl⟩)).2,
      by linarith⟩

/-! ## `ℍ²(-c²)`: `G = cosh(c y)` -/

/-- Passo trigonometrico em `ℍ²`: de `c cosh(cA) + c cosh(cB) ≤ k (sinh(cB) - sinh(cA))` com
`-w/2 ≤ A ≤ B ≤ w/2` segue `c cosh(cw/2) ≤ k sinh(cw/2)` (identidades de soma e produto e
`coth` decrescente). -/
theorem hyperbolic_step {c k lo hi w : ℝ} (hc : 0 < c) (hlo : -(w / 2) ≤ lo) (hlh : lo ≤ hi)
    (hhi : hi ≤ w / 2)
    (h : c * cosh (c * lo) + c * cosh (c * hi) ≤ k * (sinh (c * hi) - sinh (c * lo))) :
    c * cosh (c * (w / 2)) ≤ k * sinh (c * (w / 2)) := by
  set m := c * (lo + hi) / 2 with hm
  set d := c * (hi - lo) / 2 with hd
  have hA : c * lo = m - d := by rw [hm, hd]; ring
  have hB : c * hi = m + d := by rw [hm, hd]; ring
  rw [hA, hB, cosh_sub, cosh_add, sinh_add, sinh_sub] at h
  have hcm := cosh_pos m
  have h1 : (2 * cosh m) * (c * cosh d) ≤ (2 * cosh m) * (k * sinh d) := by nlinarith [h]
  have hc1 : c * cosh d ≤ k * sinh d := le_of_mul_le_mul_left h1 (by positivity)
  have hd0 : 0 ≤ d := by rw [hd]; have := sub_nonneg.mpr hlh; positivity
  set D := c * (w / 2) with hD
  have hdD : d ≤ D := by rw [hd, hD]; nlinarith
  have hdpos : 0 < d := by
    rcases hd0.lt_or_eq with h' | h'
    · exact h'
    · exfalso; rw [← h', cosh_zero, sinh_zero] at hc1; linarith
  have hsd : 0 < sinh d := sinh_pos_iff.mpr hdpos
  have hsD : 0 < sinh D := sinh_pos_iff.mpr (by linarith)
  have hDd : 0 ≤ sinh (D - d) := sinh_nonneg_iff.mpr (by linarith)
  rw [sinh_sub] at hDd
  have h2 : c * cosh D * sinh d ≤ k * sinh D * sinh d := by
    nlinarith [mul_le_mul_of_nonneg_left hDd hc.le, mul_le_mul_of_nonneg_right hc1 hsD.le]
  exact le_of_mul_le_mul_right h2 hsd

/-- **Teorema `prop:space_form_uturn`, caso `ℍ²(-c²)`**, na reducao de Fermi do cabecalho:
`c cosh(cw/2) ≤ k sinh(cw/2)`, isto e `k ≥ c coth(cw/2)`. -/
theorem hyperbolic_uturn (c : ℝ) (y θ u κ : ℝ → ℝ) (L k w : ℝ) (hc : 0 < c) (hL : 0 ≤ L)
    (hyc : ContinuousOn y (Icc 0 L)) (hy : ∀ s ∈ Ioo 0 L, HasDerivAt y (sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L))
    (hu : ∀ s ∈ Icc 0 L, u s = cosh (c * y s) * cos (θ s))
    (hClairaut : ∀ s ∈ Ioo 0 L, HasDerivAt u (-(κ s * cosh (c * y s) * sin (θ s))) s)
    (hκ : ∀ s ∈ Ioo 0 L, |κ s| ≤ k) (h0 : θ 0 = 0) (hend : cos (θ L) = -1)
    (htube : ∀ s ∈ Icc 0 L, y s ∈ Icc (-(w / 2)) (w / 2)) :
    c * cosh (c * (w / 2)) ≤ k * sinh (c * (w / 2)) := by
  have huc : ContinuousOn u (Icc 0 L) := by
    refine ContinuousOn.congr ?_ hu
    exact ((continuous_cosh.comp_continuousOn (continuousOn_const.mul hyc))).mul
      (continuous_cos.comp_continuousOn hθc)
  obtain ⟨lo, hi, h1, h2, h3, h4⟩ := warped_uturn_core (fun t => c * cosh (c * t))
    (fun t => sinh (c * t)) y θ (fun s => c * u s) κ L k w hL
    (fun t _ => by
      have := (hasDerivAt_sinh (c * t)).comp t ((hasDerivAt_id t).const_mul c)
      simp only [Function.comp_def, mul_one] at this
      convert this using 1; ring)
    (fun t _ => by positivity)
    hyc hy hθc (continuousOn_const.mul huc)
    (fun s hs => by show c * u s = _; rw [hu s hs]; ring)
    (fun s hs => by
      have := (hClairaut s hs).const_mul c
      convert this using 1; ring)
    hκ h0 hend htube
  exact hyperbolic_step hc h1 h2 h3 h4

/-- **`prop:space_form_uturn`, `ℍ²`, forma `k ≥ c coth(cw/2)`** (`coth = cosh/sinh`), `w > 0`. -/
theorem hyperbolic_uturn_coth (c : ℝ) (y θ u κ : ℝ → ℝ) (L k w : ℝ) (hc : 0 < c) (hw : 0 < w)
    (hL : 0 ≤ L)
    (hyc : ContinuousOn y (Icc 0 L)) (hy : ∀ s ∈ Ioo 0 L, HasDerivAt y (sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L))
    (hu : ∀ s ∈ Icc 0 L, u s = cosh (c * y s) * cos (θ s))
    (hClairaut : ∀ s ∈ Ioo 0 L, HasDerivAt u (-(κ s * cosh (c * y s) * sin (θ s))) s)
    (hκ : ∀ s ∈ Ioo 0 L, |κ s| ≤ k) (h0 : θ 0 = 0) (hend : cos (θ L) = -1)
    (htube : ∀ s ∈ Icc 0 L, y s ∈ Icc (-(w / 2)) (w / 2)) :
    c * (cosh (c * w / 2) / sinh (c * w / 2)) ≤ k := by
  have h := hyperbolic_uturn c y θ u κ L k w hc hL hyc hy hθc hu hClairaut hκ h0 hend htube
  have hs : 0 < sinh (c * w / 2) := sinh_pos_iff.mpr (by positivity)
  rw [show c * (w / 2) = c * w / 2 by ring] at h
  rw [← mul_div_assoc, div_le_iff₀ hs]
  exact h

/-! ## `𝕊²(+c²)`: `G = cos(c y)`, `w < π/c` -/

/-- Passo trigonometrico em `𝕊²` (identidades de soma e produto, `cos((A+B)/2) > 0` e `cot`
decrescente em `(0, π/2)`). -/
theorem spherical_step {c k lo hi w : ℝ} (hc : 0 < c) (hcw : c * w < π) (hlo : -(w / 2) ≤ lo)
    (hlh : lo ≤ hi) (hhi : hi ≤ w / 2)
    (h : c * cos (c * lo) + c * cos (c * hi) ≤ k * (sin (c * hi) - sin (c * lo))) :
    c * cos (c * (w / 2)) ≤ k * sin (c * (w / 2)) := by
  set m := c * (lo + hi) / 2 with hm
  set d := c * (hi - lo) / 2 with hd
  have hA : c * lo = m - d := by rw [hm, hd]; ring
  have hB : c * hi = m + d := by rw [hm, hd]; ring
  rw [hA, hB, cos_sub, cos_add, sin_add, sin_sub] at h
  set D := c * (w / 2) with hD
  have hDpi : D < π / 2 := by rw [hD]; linarith
  have hm1 : -(π / 2) < m := by rw [hm]; nlinarith
  have hm2 : m < π / 2 := by rw [hm]; nlinarith
  have hcm : 0 < cos m := cos_pos_of_mem_Ioo ⟨hm1, hm2⟩
  have h1 : (2 * cos m) * (c * cos d) ≤ (2 * cos m) * (k * sin d) := by nlinarith [h]
  have hc1 : c * cos d ≤ k * sin d := le_of_mul_le_mul_left h1 (by positivity)
  have hd0 : 0 ≤ d := by rw [hd]; have := sub_nonneg.mpr hlh; positivity
  have hdD : d ≤ D := by rw [hd, hD]; nlinarith
  have hdpos : 0 < d := by
    rcases hd0.lt_or_eq with h' | h'
    · exact h'
    · exfalso; rw [← h', cos_zero, sin_zero] at hc1; linarith
  have hpi := pi_pos
  have hsd : 0 < sin d := Real.sin_pos_of_pos_of_lt_pi hdpos (by linarith)
  have hsD : 0 < sin D := Real.sin_pos_of_pos_of_lt_pi (by linarith) (by linarith)
  have hDd : 0 ≤ sin (D - d) := sin_nonneg_of_nonneg_of_le_pi (by linarith) (by linarith)
  rw [sin_sub] at hDd
  have h2 : c * cos D * sin d ≤ k * sin D * sin d := by
    nlinarith [mul_le_mul_of_nonneg_left hDd hc.le, mul_le_mul_of_nonneg_right hc1 hsD.le]
  exact le_of_mul_le_mul_right h2 hsd

/-- **Teorema `prop:space_form_uturn`, caso `𝕊²(+c²)`** (`w < π/c`), na reducao de Fermi:
`c cos(cw/2) ≤ k sin(cw/2)`, isto e `k ≥ c cot(cw/2)`. -/
theorem spherical_uturn (c : ℝ) (y θ u κ : ℝ → ℝ) (L k w : ℝ) (hc : 0 < c) (hcw : c * w < π)
    (hL : 0 ≤ L)
    (hyc : ContinuousOn y (Icc 0 L)) (hy : ∀ s ∈ Ioo 0 L, HasDerivAt y (sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L))
    (hu : ∀ s ∈ Icc 0 L, u s = cos (c * y s) * cos (θ s))
    (hClairaut : ∀ s ∈ Ioo 0 L, HasDerivAt u (-(κ s * cos (c * y s) * sin (θ s))) s)
    (hκ : ∀ s ∈ Ioo 0 L, |κ s| ≤ k) (h0 : θ 0 = 0) (hend : cos (θ L) = -1)
    (htube : ∀ s ∈ Icc 0 L, y s ∈ Icc (-(w / 2)) (w / 2)) :
    c * cos (c * (w / 2)) ≤ k * sin (c * (w / 2)) := by
  have huc : ContinuousOn u (Icc 0 L) := by
    refine ContinuousOn.congr ?_ hu
    exact ((continuous_cos.comp_continuousOn (continuousOn_const.mul hyc))).mul
      (continuous_cos.comp_continuousOn hθc)
  have hpi := pi_pos
  obtain ⟨lo, hi, h1, h2, h3, h4⟩ := warped_uturn_core (fun t => c * cos (c * t))
    (fun t => sin (c * t)) y θ (fun s => c * u s) κ L k w hL
    (fun t _ => by
      have := (hasDerivAt_sin (c * t)).comp t ((hasDerivAt_id t).const_mul c)
      simp only [Function.comp_def, mul_one] at this
      convert this using 1; ring)
    (fun t ht => by
      have h1 : -(π / 2) ≤ c * t := by nlinarith [ht.1]
      have h2 : c * t ≤ π / 2 := by nlinarith [ht.2]
      exact mul_nonneg hc.le (cos_nonneg_of_mem_Icc ⟨h1, h2⟩))
    hyc hy hθc (continuousOn_const.mul huc)
    (fun s hs => by show c * u s = _; rw [hu s hs]; ring)
    (fun s hs => by
      have := (hClairaut s hs).const_mul c
      convert this using 1; ring)
    hκ h0 hend htube
  exact spherical_step hc hcw h1 h2 h3 h4

/-- **`prop:space_form_uturn`, `𝕊²`, forma `k ≥ c cot(cw/2)`** (`cot = cos/sin`), `w > 0`. -/
theorem spherical_uturn_cot (c : ℝ) (y θ u κ : ℝ → ℝ) (L k w : ℝ) (hc : 0 < c) (hw : 0 < w)
    (hcw : c * w < π) (hL : 0 ≤ L)
    (hyc : ContinuousOn y (Icc 0 L)) (hy : ∀ s ∈ Ioo 0 L, HasDerivAt y (sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L))
    (hu : ∀ s ∈ Icc 0 L, u s = cos (c * y s) * cos (θ s))
    (hClairaut : ∀ s ∈ Ioo 0 L, HasDerivAt u (-(κ s * cos (c * y s) * sin (θ s))) s)
    (hκ : ∀ s ∈ Ioo 0 L, |κ s| ≤ k) (h0 : θ 0 = 0) (hend : cos (θ L) = -1)
    (htube : ∀ s ∈ Icc 0 L, y s ∈ Icc (-(w / 2)) (w / 2)) :
    c * (cos (c * w / 2) / sin (c * w / 2)) ≤ k := by
  have h := spherical_uturn c y θ u κ L k w hc hcw hL hyc hy hθc hu hClairaut hκ h0 hend htube
  have hs : 0 < sin (c * w / 2) :=
    Real.sin_pos_of_pos_of_lt_pi (by positivity) (by linarith [pi_pos])
  rw [show c * (w / 2) = c * w / 2 by ring] at h
  rw [← mul_div_assoc, div_le_iff₀ hs]
  exact h

/-! ## `ℝ²`: `G ≡ 1` (segunda prova de `lem:euclidean_uturn`, observacao apos o teorema) -/

/-- **`G ≡ 1`**: `2 ≤ k (b - a) ≤ k w`. -/
theorem euclidean_uturn_fermi (y θ u κ : ℝ → ℝ) (L k w : ℝ) (hL : 0 ≤ L)
    (hyc : ContinuousOn y (Icc 0 L)) (hy : ∀ s ∈ Ioo 0 L, HasDerivAt y (sin (θ s)) s)
    (hθc : ContinuousOn θ (Icc 0 L))
    (hu : ∀ s ∈ Icc 0 L, u s = cos (θ s))
    (hClairaut : ∀ s ∈ Ioo 0 L, HasDerivAt u (-(κ s * sin (θ s))) s)
    (hκ : ∀ s ∈ Ioo 0 L, |κ s| ≤ k) (h0 : θ 0 = 0) (hend : cos (θ L) = -1)
    (htube : ∀ s ∈ Icc 0 L, y s ∈ Icc (-(w / 2)) (w / 2)) :
    2 ≤ k * w := by
  have huc : ContinuousOn u (Icc 0 L) :=
    ContinuousOn.congr (continuous_cos.comp_continuousOn hθc) hu
  obtain ⟨lo, hi, h1, h2, h3, h4⟩ := warped_uturn_core (fun _ => 1) (fun t => t) y θ u κ L k w
    hL (fun t _ => hasDerivAt_id t) (fun _ _ => zero_le_one) hyc hy hθc huc
    (fun s hs => by rw [hu s hs]; ring)
    (fun s hs => by convert hClairaut s hs using 1; ring)
    hκ h0 hend htube
  try simp only at h4
  have hk : 0 ≤ k := by
    by_contra hk; rw [not_le] at hk; nlinarith
  nlinarith

/-! ## Comparacao com o caso euclidiano (observacao apos o teorema) -/

/-- `x cot x < 1` em `(0, π/2)`: curvatura positiva baixa a cota abaixo de `2/w`. -/
theorem x_cot_lt_one {x : ℝ} (h1 : 0 < x) (h2 : x < π / 2) : x * cos x < sin x := by
  have ht := lt_tan h1 h2
  have hc : 0 < cos x := cos_pos_of_mem_Ioo ⟨by linarith, h2⟩
  rw [tan_eq_sin_div_cos, lt_div_iff₀ hc] at ht
  exact ht

/-- `x coth x > 1` para `x > 0`: curvatura negativa sobe a cota acima de `2/w`. -/
theorem sinh_lt_x_cosh {x : ℝ} (h1 : 0 < x) : sinh x < x * cosh x := by
  have hmono : StrictMonoOn (fun t => t * cosh t - sinh t) (Ici 0) := by
    apply strictMonoOn_of_deriv_pos (convex_Ici 0)
    · fun_prop
    · intro t ht
      rw [interior_Ici] at ht
      have hd : HasDerivAt (fun t => t * cosh t - sinh t) (t * sinh t) t := by
        have := ((hasDerivAt_id t).mul (hasDerivAt_cosh t)).sub (hasDerivAt_sinh t)
        exact this.congr_deriv (by simp only [id, one_mul]; ring)
      rw [hd.deriv]
      exact mul_pos ht (sinh_pos_iff.mpr ht)
  have := hmono (mem_Ici.mpr le_rfl) (le_of_lt h1 : (0 : ℝ) ≤ x) h1
  simp at this
  linarith

/-! ## Testemunha em `ℍ²`: o semicirculo geodesico em coordenadas de Fermi -/

section Hyp

variable (c S : ℝ)

/-- `y(s) = -arsinh(S cos(c s/S))/c`, com `S = sinh(cw/2)`. -/
def hY (s : ℝ) : ℝ := -arsinh (S * cos (c * s / S)) / c

/-- `Q(s) = √(1 + (S cos(c s/S))²) = cosh(c y(s))`. -/
def hQ (s : ℝ) : ℝ := √(1 + (S * cos (c * s / S)) ^ 2)

/-- `θ(s) = arccos(C cos(c s/S)/Q(s))`, `C = √(1 + S²) = cosh(cw/2)`. -/
def hTheta (s : ℝ) : ℝ := arccos (√(1 + S ^ 2) * cos (c * s / S) / hQ c S s)

/-- `u(s) = C cos(c s/S)`. -/
def hU (s : ℝ) : ℝ := √(1 + S ^ 2) * cos (c * s / S)

variable {c S}

theorem hQ_pos (s : ℝ) : 0 < hQ c S s := by unfold hQ; positivity

theorem cosh_hY (hc : 0 < c) (s : ℝ) : cosh (c * hY c S s) = hQ c S s := by
  unfold hY hQ
  rw [show c * (-arsinh (S * cos (c * s / S)) / c) = -arsinh (S * cos (c * s / S)) by
    field_simp, cosh_neg, cosh_arsinh]

theorem hZ_sq_le (s : ℝ) : (√(1 + S ^ 2) * cos (c * s / S) / hQ c S s) ^ 2 ≤ 1 := by
  have hq := hQ_pos (c := c) (S := S) s
  rw [div_pow, div_le_one (by positivity), mul_pow, sq_sqrt (by positivity), hQ,
    sq_sqrt (by positivity)]
  nlinarith [cos_sq_le_one (c * s / S)]

theorem cos_hTheta (s : ℝ) :
    cos (hTheta c S s) = √(1 + S ^ 2) * cos (c * s / S) / hQ c S s := by
  have h := hZ_sq_le (c := c) (S := S) s
  have h' := abs_le.mp ((sq_le_one_iff_abs_le_one _).mp h)
  exact cos_arccos h'.1 h'.2

theorem sin_hTheta (s : ℝ) (hs : 0 ≤ sin (c * s / S)) :
    sin (hTheta c S s) = sin (c * s / S) / hQ c S s := by
  unfold hTheta
  rw [sin_arccos]
  have hq := hQ_pos (c := c) (S := S) s
  have hq0 : hQ c S s ^ 2 ≠ 0 := by positivity
  have hq2 : hQ c S s ^ 2 = 1 + (S * cos (c * s / S)) ^ 2 := by
    unfold hQ; rw [sq_sqrt (by positivity)]
  have hC2 : √(1 + S ^ 2) ^ 2 = 1 + S ^ 2 := sq_sqrt (by positivity)
  have e : 1 - (√(1 + S ^ 2) * cos (c * s / S) / hQ c S s) ^ 2 =
      (sin (c * s / S) / hQ c S s) ^ 2 := by
    rw [div_pow, div_pow, eq_div_iff hq0, sub_mul, one_mul, div_mul_cancel₀ _ hq0]
    linear_combination hq2 - cos (c * s / S) ^ 2 * hC2 - sin_sq_add_cos_sq (c * s / S)
  rw [e, sqrt_sq (div_nonneg hs hq.le)]

/-- **Testemunha (nitidez em `ℍ²`)**: para `c > 0`, `S > 0` (`w = 2 arsinh(S)/c`,
`L = π S/c`, `k = c √(1+S²)/S = c coth(cw/2)`), os dados `(hY, hTheta, hU, κ ≡ k)` satisfazem
TODAS as hipoteses de `hyperbolic_uturn`, e a conclusao vale com igualdade. -/
theorem witness_hyperbolic (hc : 0 < c) (hS : 0 < S) :
    let L := π * S / c
    let w := 2 * arsinh S / c
    let k := c * √(1 + S ^ 2) / S
    0 ≤ L ∧ ContinuousOn (hY c S) (Icc 0 L) ∧
    (∀ s ∈ Ioo 0 L, HasDerivAt (hY c S) (sin (hTheta c S s)) s) ∧
    ContinuousOn (hTheta c S) (Icc 0 L) ∧
    (∀ s ∈ Icc 0 L, hU c S s = cosh (c * hY c S s) * cos (hTheta c S s)) ∧
    (∀ s ∈ Ioo 0 L, HasDerivAt (hU c S)
      (-((fun _ => k) s * cosh (c * hY c S s) * sin (hTheta c S s))) s) ∧
    (∀ s ∈ Ioo 0 L, |(fun _ => k) s| ≤ k) ∧ hTheta c S 0 = 0 ∧ cos (hTheta c S L) = -1 ∧
    (∀ s ∈ Icc 0 L, hY c S s ∈ Icc (-(w / 2)) (w / 2)) ∧
    c * cosh (c * (w / 2)) = k * sinh (c * (w / 2)) := by
  intro L w k
  have hc0 := hc.ne'
  have hS0 := hS.ne'
  have hpi := pi_pos
  have hC : 0 < √(1 + S ^ 2) := by positivity
  -- t(s) = c s/S ∈ [0, π] em [0, L]
  have ht : ∀ s ∈ Icc 0 L, c * s / S ∈ Icc 0 π := fun s hs => by
    constructor
    · exact div_nonneg (mul_nonneg hc.le hs.1) hS.le
    · rw [div_le_iff₀ hS]
      have := hs.2
      have : c * s ≤ c * L := mul_le_mul_of_nonneg_left this hc.le
      calc c * s ≤ c * L := this
        _ = π * S := by simp only [L]; field_simp
  have hY_deriv : ∀ s, HasDerivAt (hY c S) (sin (c * s / S) / hQ c S s) s := fun s => by
    have h1 : HasDerivAt (fun s => c * s / S) (c / S) s := by
      simpa using ((hasDerivAt_id s).const_mul c).div_const S
    have h2 := ((h1.cos).const_mul S).arsinh.neg.div_const c
    unfold hY
    refine h2.congr_deriv ?_
    rw [smul_eq_mul]
    unfold hQ
    field_simp
  have hQc : Continuous (hQ c S) := by unfold hQ; fun_prop
  refine ⟨by positivity, ?_, fun s hs => ?_, ?_, fun s hs => ?_, fun s hs => ?_,
    fun s _ => ?_, ?_, ?_, fun s hs => ?_, ?_⟩
  · exact (continuous_iff_continuousAt.mpr
      (fun s => (hY_deriv s).continuousAt)).continuousOn
  · rw [sin_hTheta s (sin_nonneg_of_nonneg_of_le_pi (ht s (Ioo_subset_Icc_self hs)).1
      (ht s (Ioo_subset_Icc_self hs)).2)]
    exact hY_deriv s
  · unfold hTheta
    exact (continuous_arccos.comp ((by fun_prop : Continuous fun s =>
      √(1 + S ^ 2) * cos (c * s / S)).div hQc (fun s => (hQ_pos s).ne'))).continuousOn
  · rw [cosh_hY hc, cos_hTheta, hU]
    field_simp [(hQ_pos (c := c) (S := S) s).ne']
  · have hsin := sin_nonneg_of_nonneg_of_le_pi (ht s (Ioo_subset_Icc_self hs)).1
      (ht s (Ioo_subset_Icc_self hs)).2
    have h1 : HasDerivAt (fun s => c * s / S) (c / S) s := by
      simpa using ((hasDerivAt_id s).const_mul c).div_const S
    have h2 := (h1.cos).const_mul (√(1 + S ^ 2))
    unfold hU
    refine h2.congr_deriv ?_
    simp only [k]
    rw [cosh_hY hc, sin_hTheta s hsin]
    field_simp [(hQ_pos (c := c) (S := S) s).ne']
  · simp only [k]
    rw [abs_of_pos (by positivity)]
  · unfold hTheta hQ
    rw [show c * 0 / S = 0 by simp, cos_zero, mul_one, mul_one,
      div_self (by positivity), arccos_one]
  · rw [cos_hTheta]
    unfold hQ
    rw [show c * L / S = π by simp only [L]; field_simp, cos_pi,
      show (S * -1) ^ 2 = S ^ 2 by ring, mul_neg_one, neg_div, div_self hC.ne']
  · have hw2 : w / 2 = arsinh S / c := by simp only [w]; ring
    rw [hw2]
    unfold hY
    have hcs1 := neg_one_le_cos (c * s / S)
    have hcs2 := cos_le_one (c * s / S)
    have hl : -S ≤ S * cos (c * s / S) := by nlinarith
    have hr : S * cos (c * s / S) ≤ S := by nlinarith
    have a1 := arsinh_le_arsinh.mpr hl
    have a2 := arsinh_le_arsinh.mpr hr
    rw [arsinh_neg] at a1
    constructor
    · rw [neg_div, neg_le_neg_iff]; exact div_le_div_of_nonneg_right a2 hc.le
    · rw [neg_div, neg_le, ← neg_div]; exact div_le_div_of_nonneg_right (by linarith) hc.le
  · have hw2 : c * (w / 2) = arsinh S := by simp only [w]; field_simp
    rw [hw2, cosh_arsinh, sinh_arsinh]
    simp only [k]
    field_simp

/-- A testemunha aplicada ao teorema (`c = S = 1`): os tipos casam. -/
example : 1 * cosh (1 * ((2 * arsinh 1 / 1) / 2)) ≤
    1 * √(1 + 1 ^ 2) / 1 * sinh (1 * ((2 * arsinh 1 / 1) / 2)) := by
  obtain ⟨hL, h1, h2, h3, h4, h5, h6, h7, h8, h9, -⟩ :=
    witness_hyperbolic (c := 1) (S := 1) one_pos one_pos
  exact hyperbolic_uturn 1 _ _ _ _ _ _ _ one_pos hL h1 h2 h3 h4 h5 h6 h7 h8 h9

end Hyp

/-! ## Testemunha em `𝕊²` -/

section Sph

variable (c S : ℝ)

/-- `y(s) = -arcsin(S cos(c s/S))/c`, com `S = sin(cw/2) ∈ (0,1)`. -/
def sY (s : ℝ) : ℝ := -arcsin (S * cos (c * s / S)) / c

/-- `Q(s) = √(1 - (S cos(c s/S))²) = cos(c y(s))`. -/
def sQ (s : ℝ) : ℝ := √(1 - (S * cos (c * s / S)) ^ 2)

/-- `θ(s) = arccos(C cos(c s/S)/Q(s))`, `C = √(1 - S²) = cos(cw/2)`. -/
def sTheta (s : ℝ) : ℝ := arccos (√(1 - S ^ 2) * cos (c * s / S) / sQ c S s)

/-- `u(s) = C cos(c s/S)`. -/
def sU (s : ℝ) : ℝ := √(1 - S ^ 2) * cos (c * s / S)

variable {c S}

theorem sQ_sq (hS : 0 < S) (hS1 : S < 1) (s : ℝ) :
    sQ c S s ^ 2 = 1 - (S * cos (c * s / S)) ^ 2 := by
  have hS1' : S ^ 2 < 1 := by nlinarith
  unfold sQ
  rw [sq_sqrt]
  nlinarith [cos_sq_le_one (c * s / S), mul_pow S (cos (c * s / S)) 2, sq_nonneg S]

theorem sQ_pos (hS : 0 < S) (hS1 : S < 1) (s : ℝ) : 0 < sQ c S s := by
  unfold sQ
  apply sqrt_pos.mpr
  have : (S * cos (c * s / S)) ^ 2 ≤ S ^ 2 := by
    rw [mul_pow]; nlinarith [cos_sq_le_one (c * s / S), sq_nonneg S]
  nlinarith

theorem cos_sY (hc : 0 < c) (s : ℝ) : cos (c * sY c S s) = sQ c S s := by
  unfold sY sQ
  rw [show c * (-arcsin (S * cos (c * s / S)) / c) = -arcsin (S * cos (c * s / S)) by
    field_simp, cos_neg, cos_arcsin]

theorem sZ_sq_le (hS : 0 < S) (hS1 : S < 1) (s : ℝ) :
    (√(1 - S ^ 2) * cos (c * s / S) / sQ c S s) ^ 2 ≤ 1 := by
  have hq := sQ_pos (c := c) hS hS1 s
  rw [div_pow, div_le_one (by positivity), mul_pow, sq_sqrt (by nlinarith), sQ_sq hS hS1]
  nlinarith [cos_sq_le_one (c * s / S)]

theorem cos_sTheta (hS : 0 < S) (hS1 : S < 1) (s : ℝ) :
    cos (sTheta c S s) = √(1 - S ^ 2) * cos (c * s / S) / sQ c S s := by
  have h := sZ_sq_le (c := c) hS hS1 s
  have h' := abs_le.mp ((sq_le_one_iff_abs_le_one _).mp h)
  exact cos_arccos h'.1 h'.2

theorem sin_sTheta (hS : 0 < S) (hS1 : S < 1) (s : ℝ) (hs : 0 ≤ sin (c * s / S)) :
    sin (sTheta c S s) = sin (c * s / S) / sQ c S s := by
  unfold sTheta
  rw [sin_arccos]
  have hq := sQ_pos (c := c) hS hS1 s
  have hq0 : sQ c S s ^ 2 ≠ 0 := by positivity
  have hq2 := sQ_sq (c := c) hS hS1 s
  have hC2 : √(1 - S ^ 2) ^ 2 = 1 - S ^ 2 := sq_sqrt (by nlinarith)
  have e : 1 - (√(1 - S ^ 2) * cos (c * s / S) / sQ c S s) ^ 2 =
      (sin (c * s / S) / sQ c S s) ^ 2 := by
    rw [div_pow, div_pow, eq_div_iff hq0, sub_mul, one_mul, div_mul_cancel₀ _ hq0]
    linear_combination hq2 - cos (c * s / S) ^ 2 * hC2 - sin_sq_add_cos_sq (c * s / S)
  rw [e, sqrt_sq (div_nonneg hs hq.le)]

/-- **Testemunha (nitidez em `𝕊²`)**: para `c > 0`, `S ∈ (0,1)` (`w = 2 arcsin(S)/c < π/c`,
`L = π S/c`, `k = c √(1-S²)/S = c cot(cw/2)`), os dados `(sY, sTheta, sU, κ ≡ k)` satisfazem
TODAS as hipoteses de `spherical_uturn`, e a conclusao vale com igualdade. -/
theorem witness_spherical (hc : 0 < c) (hS : 0 < S) (hS1 : S < 1) :
    let L := π * S / c
    let w := 2 * arcsin S / c
    let k := c * √(1 - S ^ 2) / S
    c * w < π ∧ 0 ≤ L ∧ ContinuousOn (sY c S) (Icc 0 L) ∧
    (∀ s ∈ Ioo 0 L, HasDerivAt (sY c S) (sin (sTheta c S s)) s) ∧
    ContinuousOn (sTheta c S) (Icc 0 L) ∧
    (∀ s ∈ Icc 0 L, sU c S s = cos (c * sY c S s) * cos (sTheta c S s)) ∧
    (∀ s ∈ Ioo 0 L, HasDerivAt (sU c S)
      (-((fun _ => k) s * cos (c * sY c S s) * sin (sTheta c S s))) s) ∧
    (∀ s ∈ Ioo 0 L, |(fun _ => k) s| ≤ k) ∧ sTheta c S 0 = 0 ∧ cos (sTheta c S L) = -1 ∧
    (∀ s ∈ Icc 0 L, sY c S s ∈ Icc (-(w / 2)) (w / 2)) ∧
    c * cos (c * (w / 2)) = k * sin (c * (w / 2)) := by
  intro L w k
  have hc0 := hc.ne'
  have hS0 := hS.ne'
  have hpi := pi_pos
  have hC : 0 < √(1 - S ^ 2) := sqrt_pos.mpr (by nlinarith)
  have ht : ∀ s ∈ Icc 0 L, c * s / S ∈ Icc 0 π := fun s hs => by
    constructor
    · exact div_nonneg (mul_nonneg hc.le hs.1) hS.le
    · rw [div_le_iff₀ hS]
      have : c * s ≤ c * L := mul_le_mul_of_nonneg_left hs.2 hc.le
      calc c * s ≤ c * L := this
        _ = π * S := by simp only [L]; field_simp
  have hne : ∀ s, S * cos (c * s / S) ≠ -1 ∧ S * cos (c * s / S) ≠ 1 := fun s => by
    have h1 := neg_one_le_cos (c * s / S)
    have h2 := cos_le_one (c * s / S)
    constructor <;> intro h <;> nlinarith
  have hY_deriv : ∀ s, HasDerivAt (sY c S) (sin (c * s / S) / sQ c S s) s := fun s => by
    have h1 : HasDerivAt (fun s => c * s / S) (c / S) s := by
      simpa using ((hasDerivAt_id s).const_mul c).div_const S
    have h2 := (((Real.hasDerivAt_arcsin (hne s).1 (hne s).2).comp s
      ((h1.cos).const_mul S)).neg).div_const c
    unfold sY
    refine h2.congr_deriv ?_
    unfold sQ
    have hq := sQ_pos (c := c) hS hS1 s
    unfold sQ at hq
    field_simp
  have hQc : Continuous (sQ c S) := by unfold sQ; fun_prop
  refine ⟨?_, by positivity, ?_, fun s hs => ?_, ?_, fun s hs => ?_, fun s hs => ?_,
    fun s _ => ?_, ?_, ?_, fun s hs => ?_, ?_⟩
  · have : arcsin S < π / 2 := arcsin_lt_pi_div_two.mpr hS1
    simp only [w]
    rw [show c * (2 * arcsin S / c) = 2 * arcsin S by field_simp]
    linarith
  · exact (continuous_iff_continuousAt.mpr
      (fun s => (hY_deriv s).continuousAt)).continuousOn
  · rw [sin_sTheta hS hS1 s (sin_nonneg_of_nonneg_of_le_pi (ht s (Ioo_subset_Icc_self hs)).1
      (ht s (Ioo_subset_Icc_self hs)).2)]
    exact hY_deriv s
  · unfold sTheta
    exact (continuous_arccos.comp ((by fun_prop : Continuous fun s =>
      √(1 - S ^ 2) * cos (c * s / S)).div hQc (fun s => (sQ_pos hS hS1 s).ne'))).continuousOn
  · rw [cos_sY hc, cos_sTheta hS hS1, sU]
    field_simp [(sQ_pos (c := c) hS hS1 s).ne']
  · have hsin := sin_nonneg_of_nonneg_of_le_pi (ht s (Ioo_subset_Icc_self hs)).1
      (ht s (Ioo_subset_Icc_self hs)).2
    have h1 : HasDerivAt (fun s => c * s / S) (c / S) s := by
      simpa using ((hasDerivAt_id s).const_mul c).div_const S
    have h2 := (h1.cos).const_mul (√(1 - S ^ 2))
    unfold sU
    refine h2.congr_deriv ?_
    simp only [k]
    rw [cos_sY hc, sin_sTheta hS hS1 s hsin]
    field_simp [(sQ_pos (c := c) hS hS1 s).ne']
  · simp only [k]
    rw [abs_of_pos (by positivity)]
  · unfold sTheta sQ
    rw [show c * 0 / S = 0 by simp, cos_zero, mul_one, mul_one, div_self hC.ne', arccos_one]
  · rw [cos_sTheta hS hS1]
    unfold sQ
    rw [show c * L / S = π by simp only [L]; field_simp, cos_pi,
      show (S * -1) ^ 2 = S ^ 2 by ring, mul_neg_one, neg_div, div_self hC.ne']
  · have hw2 : w / 2 = arcsin S / c := by simp only [w]; ring
    rw [hw2]
    unfold sY
    have hcs1 := neg_one_le_cos (c * s / S)
    have hcs2 := cos_le_one (c * s / S)
    have hl : -S ≤ S * cos (c * s / S) := by nlinarith
    have hr : S * cos (c * s / S) ≤ S := by nlinarith
    have a1 := arcsin_le_arcsin hl
    have a2 := arcsin_le_arcsin hr
    rw [arcsin_neg] at a1
    constructor
    · rw [neg_div, neg_le_neg_iff]; exact div_le_div_of_nonneg_right a2 hc.le
    · rw [neg_div, neg_le, ← neg_div]; exact div_le_div_of_nonneg_right (by linarith) hc.le
  · have hw2 : c * (w / 2) = arcsin S := by simp only [w]; field_simp
    rw [hw2, cos_arcsin, sin_arcsin (by linarith) hS1.le]
    simp only [k]
    field_simp

end Sph

/-! ## Mutantes de `prop:space_form_uturn` provados FALSOS -/

/-- Mutante 1 (`ℍ²`, conclusao estrita): falso pela testemunha (`c = S = 1`). -/
theorem mutant_hyp_strict_false :
    ¬ (∀ (c : ℝ) (y θ u κ : ℝ → ℝ) (L k w : ℝ), 0 < c → 0 ≤ L →
        ContinuousOn y (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt y (sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) →
        (∀ s ∈ Icc 0 L, u s = cosh (c * y s) * cos (θ s)) →
        (∀ s ∈ Ioo 0 L, HasDerivAt u (-(κ s * cosh (c * y s) * sin (θ s))) s) →
        (∀ s ∈ Ioo 0 L, |κ s| ≤ k) → θ 0 = 0 → cos (θ L) = -1 →
        (∀ s ∈ Icc 0 L, y s ∈ Icc (-(w / 2)) (w / 2)) →
        c * cosh (c * (w / 2)) < k * sinh (c * (w / 2))) := by
  intro h
  obtain ⟨hL, h1, h2, h3, h4, h5, h6, h7, h8, h9, heq⟩ :=
    witness_hyperbolic (c := 1) (S := 1) one_pos one_pos
  have := h 1 _ _ _ _ _ _ _ one_pos hL h1 h2 h3 h4 h5 h6 h7 h8 h9
  rw [heq] at this
  exact lt_irrefl _ this

/-- Mutante 2 (`ℍ²`, sem a identidade de Clairaut `hClairaut`): falso. Os mesmos `y, θ, u` da
testemunha com `κ ≡ 0`, `k = 0` dariam `cosh(arsinh 1) ≤ 0`. -/
theorem mutant_hyp_no_clairaut_false :
    ¬ (∀ (c : ℝ) (y θ u κ : ℝ → ℝ) (L k w : ℝ), 0 < c → 0 ≤ L →
        ContinuousOn y (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt y (sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) →
        (∀ s ∈ Icc 0 L, u s = cosh (c * y s) * cos (θ s)) →
        (∀ s ∈ Ioo 0 L, |κ s| ≤ k) → θ 0 = 0 → cos (θ L) = -1 →
        (∀ s ∈ Icc 0 L, y s ∈ Icc (-(w / 2)) (w / 2)) →
        c * cosh (c * (w / 2)) ≤ k * sinh (c * (w / 2))) := by
  intro h
  obtain ⟨hL, h1, h2, h3, h4, -, -, h7, h8, h9, -⟩ :=
    witness_hyperbolic (c := 1) (S := 1) one_pos one_pos
  have := h 1 _ _ _ (fun _ => 0) _ 0 _ one_pos hL h1 h2 h3 h4 (fun s _ => by simp) h7 h8 h9
  rw [zero_mul] at this
  linarith [cosh_pos (1 * ((2 * arsinh 1 / 1) / 2))]

/-- Mutante 3 (`ℍ²`, sem o tubo: `w` livre). Falso: a testemunha `c = S = 1` (`k = √2`,
`D = arsinh 1`) lida com `w = D` daria `cosh(D/2) ≤ √2 sinh(D/2)`, mas
`sinh(D - D/2) > 0` da `√2 sinh(D/2) < cosh(D/2)`. -/
theorem mutant_hyp_no_tube_false :
    ¬ (∀ (c : ℝ) (y θ u κ : ℝ → ℝ) (L k w : ℝ), 0 < c → 0 ≤ L →
        ContinuousOn y (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt y (sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) →
        (∀ s ∈ Icc 0 L, u s = cosh (c * y s) * cos (θ s)) →
        (∀ s ∈ Ioo 0 L, HasDerivAt u (-(κ s * cosh (c * y s) * sin (θ s))) s) →
        (∀ s ∈ Ioo 0 L, |κ s| ≤ k) → θ 0 = 0 → cos (θ L) = -1 →
        c * cosh (c * (w / 2)) ≤ k * sinh (c * (w / 2))) := by
  intro h
  obtain ⟨hL, h1, h2, h3, h4, h5, h6, h7, h8, -, -⟩ :=
    witness_hyperbolic (c := 1) (S := 1) one_pos one_pos
  set D := arsinh (1 : ℝ) with hD
  have := h 1 _ _ _ _ _ _ D one_pos hL h1 h2 h3 h4 h5 h6 h7 h8
  simp only [one_mul, div_one] at this
  have hDpos : 0 < D := arsinh_pos_iff.mpr one_pos
  have hsub := sinh_pos_iff.mpr (by linarith : 0 < D - D / 2)
  rw [sinh_sub] at hsub
  rw [hD, sinh_arsinh, cosh_arsinh] at hsub
  rw [← hD] at hsub
  norm_num at this hsub
  linarith

/-- Mutante 4 (cota euclidiana `2 ≤ k w` em `𝕊²`): falso. A testemunha esferica (`c = 1`,
`S = 1/2`, `D = arcsin(1/2)`) tem `k w = 2 D cot D < 2`, por `x cos x < sin x` em `(0,π/2)`.
Mostra que a curvatura positiva baixa a cota otima abaixo de `2/w`. -/
theorem mutant_sph_euclidean_false :
    ¬ (∀ (c : ℝ) (y θ u κ : ℝ → ℝ) (L k w : ℝ), 0 < c → c * w < π → 0 ≤ L →
        ContinuousOn y (Icc 0 L) → (∀ s ∈ Ioo 0 L, HasDerivAt y (sin (θ s)) s) →
        ContinuousOn θ (Icc 0 L) →
        (∀ s ∈ Icc 0 L, u s = cos (c * y s) * cos (θ s)) →
        (∀ s ∈ Ioo 0 L, HasDerivAt u (-(κ s * cos (c * y s) * sin (θ s))) s) →
        (∀ s ∈ Ioo 0 L, |κ s| ≤ k) → θ 0 = 0 → cos (θ L) = -1 →
        (∀ s ∈ Icc 0 L, y s ∈ Icc (-(w / 2)) (w / 2)) → 2 ≤ k * w) := by
  intro h
  have hS : (0 : ℝ) < 1 / 2 := by norm_num
  have hS1 : (1 : ℝ) / 2 < 1 := by norm_num
  obtain ⟨hcw, hL, h1, h2, h3, h4, h5, h6, h7, h8, h9, heq⟩ :=
    witness_spherical (c := 1) (S := 1 / 2) one_pos hS hS1
  have hkw := h 1 _ _ _ _ _ _ _ one_pos hcw hL h1 h2 h3 h4 h5 h6 h7 h8 h9
  set D := arcsin (1 / 2 : ℝ) with hD
  have hDpos : 0 < D := arcsin_pos.mpr hS
  have hDlt : D < π / 2 := arcsin_lt_pi_div_two.mpr hS1
  have hlt := x_cot_lt_one hDpos hDlt
  rw [hD, sin_arcsin (by norm_num) hS1.le, cos_arcsin] at hlt
  rw [← hD] at hlt
  simp only [one_mul, div_one] at hkw
  have hC : 0 < √(1 - (1 / 2 : ℝ) ^ 2) := sqrt_pos.mpr (by norm_num)
  -- k w = 2 D √(3/4) / (1/2) = 4 D √(3/4); hlt : D √(3/4) < 1/2
  have e : √(1 - (1 / 2 : ℝ) ^ 2) / (1 / 2) * (2 * D) = 4 * (D * √(1 - (1 / 2 : ℝ) ^ 2)) := by
    ring
  rw [e] at hkw
  linarith

end LeanReal.Chap08SpaceForms

#print axioms LeanReal.Chap08SpaceForms.warped_uturn_core
#print axioms LeanReal.Chap08SpaceForms.hyperbolic_step
#print axioms LeanReal.Chap08SpaceForms.hyperbolic_uturn
#print axioms LeanReal.Chap08SpaceForms.hyperbolic_uturn_coth
#print axioms LeanReal.Chap08SpaceForms.spherical_step
#print axioms LeanReal.Chap08SpaceForms.spherical_uturn
#print axioms LeanReal.Chap08SpaceForms.spherical_uturn_cot
#print axioms LeanReal.Chap08SpaceForms.euclidean_uturn_fermi
#print axioms LeanReal.Chap08SpaceForms.x_cot_lt_one
#print axioms LeanReal.Chap08SpaceForms.sinh_lt_x_cosh
#print axioms LeanReal.Chap08SpaceForms.witness_hyperbolic
#print axioms LeanReal.Chap08SpaceForms.witness_spherical
#print axioms LeanReal.Chap08SpaceForms.mutant_hyp_strict_false
#print axioms LeanReal.Chap08SpaceForms.mutant_hyp_no_clairaut_false
#print axioms LeanReal.Chap08SpaceForms.mutant_hyp_no_tube_false
#print axioms LeanReal.Chap08SpaceForms.mutant_sph_euclidean_false
