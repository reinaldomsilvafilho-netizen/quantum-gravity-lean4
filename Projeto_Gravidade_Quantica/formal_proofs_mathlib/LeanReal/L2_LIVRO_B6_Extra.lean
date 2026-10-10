import LeanReal.Chap08SpaceForms
import LeanReal.Chap09Teardrop

/-!
# L2 do lote LIVRO_B6: testemunhas com desigualdade estrita

Verificador independente (L2). As testemunhas do escritor atingem todas a igualdade. Aqui:

* `hyperbolic_strict`, `spherical_strict`: o semicirculo geodesico num tubo mais largo que o seu
  diametro; todas as hipoteses de `hyperbolic_uturn`/`spherical_uturn` valem e a conclusao vale
  com desigualdade ESTRITA (`3 < 4` em `ℍ²`, `1 < √3` em `𝕊²`).
* `euclidean_witness`: testemunha de `euclidean_uturn_fermi` (`G ≡ 1`), que o escritor nao deu,
  com igualdade (`w = 2`) e com desigualdade estrita (`w = 4`).
* `family_strict`: uma curva de `F_a` diferente de `γ_a` (`ρ = a = 1`, `α₁ = α₃ = π/4`,
  `y₀ = 1 - √2`): as hipoteses de `family_lower` valem e algum ponto do arco do meio tem
  `|p|² > r*(a)²` (via `family_eq`, pois `cos(π/4) ≠ 3/4`).
* `witness_lower_offcentre`, `lower_strict`: `prop:teardrop_lower` com `K` fora do centro
  (`m₂ ≠ 0`), `r_K < a/2` e `Δ` com `c₂ ≠ 0`; a conclusao vale estritamente (`8 < 5 + √17`).
-/

noncomputable section

namespace LeanReal.L2_LIVRO_B6_Extra

open Set Real LeanReal.Chap08SpaceForms LeanReal.Chap09Teardrop

/-! ## 8.4: testemunhas estritas -/

/-- `ℍ²`, `c = S = 1`, tubo de largura `w' = 4 arsinh 1` (o dobro do diametro do semicirculo):
hipoteses de `hyperbolic_uturn` e conclusao estrita `cosh(w'/2) < √2 sinh(w'/2)`. -/
theorem hyperbolic_strict :
    let w' := 4 * arsinh 1
    let k := 1 * √(1 + 1 ^ 2) / 1
    (∀ s ∈ Icc 0 (π * 1 / 1), hY 1 1 s ∈ Icc (-(w' / 2)) (w' / 2)) ∧
    1 * cosh (1 * (w' / 2)) < k * sinh (1 * (w' / 2)) := by
  intro w' k
  obtain ⟨hL, h1, h2, h3, h4, h5, h6, h7, h8, h9, -⟩ :=
    witness_hyperbolic (c := 1) (S := 1) one_pos one_pos
  have hA : 0 < arsinh (1 : ℝ) := arsinh_pos_iff.mpr one_pos
  have htube : ∀ s ∈ Icc 0 (π * 1 / 1), hY 1 1 s ∈ Icc (-(w' / 2)) (w' / 2) := fun s hs => by
    have := h9 s hs
    simp only [w'] at *
    constructor <;> nlinarith [this.1, this.2]
  refine ⟨htube, ?_⟩
  -- a conclusao do teorema (nao estrita) vale; mostramos a estrita
  have _ := hyperbolic_uturn 1 _ _ _ _ _ k w' one_pos hL h1 h2 h3 h4 h5 h6 h7 h8 htube
  have e : 1 * (w' / 2) = 2 * arsinh 1 := by simp only [w']; ring
  rw [e, cosh_two_mul, sinh_two_mul, cosh_arsinh, sinh_arsinh]
  have h2' : √(1 + (1 : ℝ) ^ 2) ^ 2 = 2 := by rw [sq_sqrt (by norm_num)]; norm_num
  have hm : √(1 + (1 : ℝ) ^ 2) * √(1 + 1 ^ 2) = 2 := by
    rw [Real.mul_self_sqrt (by norm_num)]; norm_num
  simp only [k]
  norm_num
  nlinarith [Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num), Real.sqrt_nonneg 2]

/-- `𝕊²`, `c = 1`, `S = 1/2` (semicirculo de diametro `2 arcsin(1/2)`), tubo de largura
`w' = π/2`: hipoteses de `spherical_uturn` e conclusao estrita. -/
theorem spherical_strict :
    let w' := π / 2
    let k := 1 * √(1 - (1 / 2 : ℝ) ^ 2) / (1 / 2)
    1 * w' < π ∧
    (∀ s ∈ Icc 0 (π * (1 / 2) / 1), sY 1 (1 / 2) s ∈ Icc (-(w' / 2)) (w' / 2)) ∧
    1 * cos (1 * (w' / 2)) < k * sin (1 * (w' / 2)) := by
  intro w' k
  have hS : (0 : ℝ) < 1 / 2 := by norm_num
  have hS1 : (1 : ℝ) / 2 < 1 := by norm_num
  obtain ⟨hcw, hL, h1, h2, h3, h4, h5, h6, h7, h8, h9, -⟩ :=
    witness_spherical (c := 1) (S := 1 / 2) one_pos hS hS1
  have hpi := pi_pos
  -- arcsin(1/2) ≤ π/4, pois 1/2 ≤ sin(π/4) = √2/2
  have hA : arcsin (1 / 2 : ℝ) ≤ π / 4 := by
    rw [arcsin_le_iff_le_sin' ⟨by linarith, by linarith⟩, sin_pi_div_four]
    have : (1 : ℝ) < √2 := by
      rw [show (1 : ℝ) = √1 by simp]; exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
    linarith
  have hA0 : 0 ≤ arcsin (1 / 2 : ℝ) := arcsin_nonneg.mpr hS.le
  have htube : ∀ s ∈ Icc 0 (π * (1 / 2) / 1), sY 1 (1 / 2) s ∈ Icc (-(w' / 2)) (w' / 2) :=
    fun s hs => by
      have := h9 s hs
      simp only [w'] at *
      constructor <;> nlinarith [this.1, this.2]
  have hcw' : 1 * w' < π := by simp only [w']; linarith
  refine ⟨hcw', htube, ?_⟩
  have _ := spherical_uturn 1 _ _ _ _ _ k w' one_pos hcw' hL h1 h2 h3 h4 h5 h6 h7 h8 htube
  have e : 1 * (w' / 2) = π / 4 := by simp only [w']; ring
  rw [e, cos_pi_div_four, sin_pi_div_four]
  have hk : k = √3 := by
    simp only [k]
    rw [show (1 : ℝ) - (1 / 2) ^ 2 = 3 / 4 by norm_num, sqrt_div' _ (by norm_num : (0:ℝ) ≤ 4),
      show (4 : ℝ) = 2 ^ 2 by norm_num, sqrt_sq (by norm_num)]
    ring
  rw [hk]
  have h3 : (1 : ℝ) < √3 := by
    rw [show (1 : ℝ) = √1 by simp]; exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have h2p : 0 < √2 := by positivity
  nlinarith

/-- Testemunha de `euclidean_uturn_fermi` (`G ≡ 1`): o semicirculo `y = -cos s`, `θ = s`,
`u = cos s`, `κ ≡ 1` em `[0, π]`; com `w = 2` a conclusao `2 ≤ k w` vale com igualdade e, no
tubo `w = 4`, estritamente. -/
theorem euclidean_witness_hyps (w : ℝ) (hw : 2 ≤ w) :
    (0 : ℝ) ≤ π ∧ ContinuousOn (fun s => -cos s) (Icc 0 π) ∧
    (∀ s ∈ Ioo 0 π, HasDerivAt (fun s => -cos s) (sin ((fun s => s) s)) s) ∧
    ContinuousOn (fun s : ℝ => s) (Icc 0 π) ∧
    (∀ s ∈ Icc 0 π, cos s = cos ((fun s : ℝ => s) s)) ∧
    (∀ s ∈ Ioo 0 π, HasDerivAt cos (-((fun _ => (1 : ℝ)) s * sin ((fun s : ℝ => s) s))) s) ∧
    (∀ s ∈ Ioo 0 π, |(fun _ => (1 : ℝ)) s| ≤ 1) ∧ (fun s : ℝ => s) 0 = 0 ∧
    cos ((fun s : ℝ => s) π) = -1 ∧
    (∀ s ∈ Icc 0 π, (fun s => -cos s) s ∈ Icc (-(w / 2)) (w / 2)) := by
  refine ⟨pi_pos.le, continuous_cos.neg.continuousOn,
    fun s _ => by convert (hasDerivAt_cos s).neg using 1; simp, continuous_id.continuousOn,
    fun s _ => rfl, fun s _ => by simpa using hasDerivAt_cos s, fun s _ => by simp, rfl,
    by simp, fun s _ => ⟨?_, ?_⟩⟩
  · simp only; nlinarith [cos_le_one s]
  · simp only; nlinarith [neg_one_le_cos s]

/-- A testemunha aplicada: `w = 2` (igualdade `2 = 1·2`) e `w = 4` (estrita `2 < 1·4`). -/
theorem euclidean_witness :
    (2 ≤ (1 : ℝ) * 2 ∧ (2 : ℝ) = 1 * 2) ∧ (2 ≤ (1 : ℝ) * 4 ∧ (2 : ℝ) < 1 * 4) := by
  have app : ∀ w : ℝ, 2 ≤ w → 2 ≤ (1 : ℝ) * w := fun w hw => by
    obtain ⟨hL, h1, h2, h3, h4, h5, h6, h7, h8, h9⟩ := euclidean_witness_hyps w hw
    exact euclidean_uturn_fermi _ _ cos _ π 1 w hL h1 h2 h3 h4 h5 h6 h7 h8 h9
  exact ⟨⟨app 2 le_rfl, by norm_num⟩, ⟨app 4 (by norm_num), by norm_num⟩⟩

/-! ## 9.7 (ii): uma curva de `F_a` com desigualdade estrita -/

/-- `ρ = a = 1`, `(y₀, α₁, α₂, α₃) = (1 - √2, π/4, 3π/2, π/4)`: todas as hipoteses de
`family_lower` valem, a curva nao e `γ_a`, e algum ponto do arco do meio tem `|p|² > r*(1)²`. -/
theorem family_strict :
    let y0 := 1 - √2
    π / 4 ∈ Icc 0 (π / 2) ∧ 3 * π / 2 ∈ Ico 0 (2 * π) ∧
    cos (3 * π / 2 - π / 4 - π / 4) = -1 ∧ (fam3 1 y0 (π / 4) (3 * π / 2) (π / 4)).1 = 0 ∧
    y0 ∈ Icc (-(1 / 2)) (1 / 2) ∧
    (fam3 1 y0 (π / 4) (3 * π / 2) (π / 4)).2 ∈ Icc (-(1 / 2)) (1 / 2) ∧
    π / 4 ≠ beta 1 1 ∧
    ∃ v ∈ Icc 0 (3 * π / 2), rstar 1 1 ^ 2 < nsq (fam2 1 y0 (π / 4) v) := by
  intro y0
  have hpi := pi_pos
  have hs2 : √2 ^ 2 = 2 := sq_sqrt (by norm_num)
  have hs2a : (1.4 : ℝ) < √2 := by
    rw [show (1.4 : ℝ) = √(1.4 ^ 2) by rw [sqrt_sq (by norm_num)]]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have hs2b : √2 < (1.5 : ℝ) := by
    rw [show (1.5 : ℝ) = √(1.5 ^ 2) by rw [sqrt_sq (by norm_num)]]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have hα : π / 4 ∈ Icc 0 (π / 2) := ⟨by positivity, by linarith⟩
  have hα2 : 3 * π / 2 ∈ Ico 0 (2 * π) := ⟨by positivity, by linarith⟩
  have hc : cos (3 * π / 2 - π / 4 - π / 4) = -1 := by
    rw [show 3 * π / 2 - π / 4 - π / 4 = π by ring, cos_pi]
  have hend := fam_end 1 y0 (π / 4) (3 * π / 2) (π / 4) hc
  have hx : (fam3 1 y0 (π / 4) (3 * π / 2) (π / 4)).1 = 0 := by rw [hend]; simp
  have hy0 : y0 ∈ Icc (-(1 / 2)) (1 / 2) := by
    simp only [y0]; constructor <;> linarith
  have hyE : (fam3 1 y0 (π / 4) (3 * π / 2) (π / 4)).2 ∈ Icc (-(1 / 2)) (1 / 2) := by
    rw [hend]; simp only [y0, cos_pi_div_four]; constructor <;> linarith
  have hne : π / 4 ≠ beta 1 1 := by
    intro h
    have hcb := cos_beta (ρ := 1) (a := 1) one_pos one_pos (by norm_num)
    rw [← h, cos_pi_div_four] at hcb
    unfold cb at hcb
    nlinarith
  refine ⟨hα, hα2, hc, hx, hy0, hyE, hne, ?_⟩
  by_contra hcon
  simp only [not_exists, not_and, not_lt] at hcon
  obtain ⟨-, h1, -, -⟩ := family_eq (ρ := 1) (a := 1) one_pos one_pos (by norm_num) hα hα hα2
    hc hx hy0 hyE hcon
  exact hne h1

/-! ## 9.10: testemunha fora do centro, com desigualdade estrita -/

/-- Para `0 ≤ r_K < ρ` e qualquer `m₂`: `Δ = B̄((d, m₂), ρ)` com `d = √(ρ² - r_K²)`,
`K = B̄((0, m₂), r_K)` e `R = ρ + √(d² + m₂²)` satisfazem `hΔ` (Cauchy-Schwarz para os pontos com
`x ≥ 0`, o argumento das cordas para `x < 0`). -/
theorem witness_lower_offcentre (ρ rK m2 : ℝ) (hρ : 0 < ρ) (hrK0 : 0 ≤ rK) (hrKρ : rK < ρ) :
    let d := √(ρ ^ 2 - rK ^ 2)
    let R := ρ + √(d ^ 2 + m2 ^ 2)
    0 ≤ R ∧ (∀ p : ℝ × ℝ, (p.1 - d) ^ 2 + (p.2 - m2) ^ 2 ≤ ρ ^ 2 →
      p.1 ^ 2 + (p.2 - m2) ^ 2 ≤ rK ^ 2 ∨ (0 ≤ p.1 ∧ p.1 ^ 2 + p.2 ^ 2 ≤ R ^ 2)) := by
  intro d R
  have hd2 : d ^ 2 = ρ ^ 2 - rK ^ 2 := sq_sqrt (by nlinarith)
  have hd0 : 0 ≤ d := sqrt_nonneg _
  set n := √(d ^ 2 + m2 ^ 2) with hn
  have hn2 : n ^ 2 = d ^ 2 + m2 ^ 2 := sq_sqrt (by positivity)
  have hn0 : 0 ≤ n := sqrt_nonneg _
  refine ⟨by positivity, fun p hp => ?_⟩
  rcases lt_or_ge p.1 0 with hneg | hnn
  · left; nlinarith [mul_nonneg hd0 (by linarith : 0 ≤ -p.1)]
  · right
    refine ⟨hnn, ?_⟩
    -- q = ⟨p - c, c⟩ ≤ |p - c| |c| ≤ ρ n
    set q := (p.1 - d) * d + (p.2 - m2) * m2 with hq
    have hcs : q ^ 2 ≤ ((p.1 - d) ^ 2 + (p.2 - m2) ^ 2) * n ^ 2 := by
      rw [hn2, hq]; nlinarith [sq_nonneg ((p.1 - d) * m2 - (p.2 - m2) * d)]
    have hq2 : q ^ 2 ≤ (ρ * n) ^ 2 := by
      calc q ^ 2 ≤ ((p.1 - d) ^ 2 + (p.2 - m2) ^ 2) * n ^ 2 := hcs
        _ ≤ ρ ^ 2 * n ^ 2 := mul_le_mul_of_nonneg_right hp (by positivity)
        _ = (ρ * n) ^ 2 := by ring
    have hqle : q ≤ ρ * n := by
      exact (abs_le_of_sq_le_sq' hq2 (by positivity)).2
    have e : p.1 ^ 2 + p.2 ^ 2 = ((p.1 - d) ^ 2 + (p.2 - m2) ^ 2) + 2 * q + n ^ 2 := by
      rw [hn2, hq]; ring
    simp only [R]
    rw [e]
    nlinarith

/-- **Instancia estrita**, `ρ = 5`, `a = 8`, `r_K = 3 < a/2`, `m₂ = 1` (`q₀ = (0,-2)`,
`q₁ = (0,4)` em `W_8`), `Δ` de centro `(4, 1)`, `R = 5 + √17`: todas as hipoteses de
`teardrop_lower` valem e `ρ + √(ρ² - a²/4) = 8 < R`. -/
theorem lower_strict :
    let R := (5 : ℝ) + √(√((5 : ℝ) ^ 2 - 3 ^ 2) ^ 2 + 1 ^ 2)
    (1 - 3 : ℝ) ^ 2 ≤ R ^ 2 ∧ (1 + 3 : ℝ) ^ 2 ≤ R ^ 2 ∧
    (5 : ℝ) + √(5 ^ 2 - 8 ^ 2 / 4) ≤ R ∧ (5 : ℝ) + √(5 ^ 2 - 8 ^ 2 / 4) < R := by
  intro R
  obtain ⟨hR, hΔ⟩ := witness_lower_offcentre 5 3 1 (by norm_num) (by norm_num) (by norm_num)
  have hd : √((5 : ℝ) ^ 2 - 3 ^ 2) = 4 := by
    rw [show (5 : ℝ) ^ 2 - 3 ^ 2 = 4 ^ 2 by norm_num, sqrt_sq (by norm_num)]
  have h8 : √((5 : ℝ) ^ 2 - 8 ^ 2 / 4) = 3 := by
    rw [show (5 : ℝ) ^ 2 - 8 ^ 2 / 4 = 3 ^ 2 by norm_num, sqrt_sq (by norm_num)]
  have h17 : (4 : ℝ) < √(√((5 : ℝ) ^ 2 - 3 ^ 2) ^ 2 + 1 ^ 2) := by
    rw [hd, show (4 : ℝ) = √(4 ^ 2) by rw [sqrt_sq (by norm_num)]]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have hRge : (5 : ℝ) + 4 < R := by simp only [R]; linarith
  have hq0 : (1 - 3 : ℝ) ^ 2 ≤ R ^ 2 := by nlinarith
  have hq1 : (1 + 3 : ℝ) ^ 2 ≤ R ^ 2 := by nlinarith
  refine ⟨hq0, hq1, teardrop_lower 5 8 R 1 3 _ 1 (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) hR hq0 hq1 hΔ, ?_⟩
  rw [h8]; linarith

end LeanReal.L2_LIVRO_B6_Extra

#print axioms LeanReal.L2_LIVRO_B6_Extra.hyperbolic_strict
#print axioms LeanReal.L2_LIVRO_B6_Extra.spherical_strict
#print axioms LeanReal.L2_LIVRO_B6_Extra.euclidean_witness_hyps
#print axioms LeanReal.L2_LIVRO_B6_Extra.euclidean_witness
#print axioms LeanReal.L2_LIVRO_B6_Extra.family_strict
#print axioms LeanReal.L2_LIVRO_B6_Extra.witness_lower_offcentre
#print axioms LeanReal.L2_LIVRO_B6_Extra.lower_strict
