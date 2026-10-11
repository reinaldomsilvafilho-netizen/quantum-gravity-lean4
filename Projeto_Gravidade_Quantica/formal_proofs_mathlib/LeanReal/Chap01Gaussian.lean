import Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Independence
import Mathlib.Probability.Moments.Variance
import Mathlib.Probability.Moments.Basic
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Analysis.Real.Pi.Bounds

/-!
# Capitulo 1, `thm:critical_scaling` (ii) (item 1 do Lote B4 do `PLANO_LIVRO_A.md`):
`u` fixo, gaussianidade exata e cauda

Fonte: `unified_quantum_gravity_book/chap01_functional_realizations_matrices_tensors.tex`,
Teorema "Critical Multilinear Scaling and Sub-Gaussian Concentration" (`thm:critical_scaling`).

Enunciado do livro (ii). `𝒯 ∈ (ℝ^d)^{⊗k}` com entradas i.i.d. `N(0,1)`;
`f̂_𝒯(u¹,…,u^k) = d^{−1/2} ∑_{j₁…j_k} 𝒯_{j₁…j_k} u¹_{j₁} ⋯ u^k_{j_k}`, `u^α ∈ 𝕊^{d−1}`.
> Para `(u¹,…,u^k)` aleatorios em `𝕊^{d−1}`, com qualquer lei conjunta, independentes de `𝒯`,
> `√d f̂_𝒯(u)` e exatamente `N(0,1)`, e portanto
> `P(|f̂_𝒯(u)| > ε) ≤ 2 exp(−dε²/2)`, `ε > 0`.
> A constante `1/2` nao depende de `k` e nao pode ser aumentada.
Prova do livro: para `v` fixo, `X(v) = ∑ 𝒯_j v_j` e combinacao linear de gaussianas
independentes com variancia `∑_j ∏_α (v^α_{j_α})² = ∏_α ‖v^α‖² = 1`; condicionando em `u`, a
lei condicional nao depende de `u`; cauda `P(Z > s) ≤ e^{−s²/2}`.

## Reducao declarada

* `u = v` FIXO (deterministico). O caso de `u` aleatorio independente de `𝒯` (condicionamento)
  NAO esta formalizado (G no plano).
* As entradas sao `T : (Fin k → Fin d) → Ω → ℝ`, indexadas por multi-indices ordenados, com
  `HasLaw (T j) (gaussianReal 0 1) P` e `iIndepFun T P`. `X v = ∑_j (∏_α v_α (j_α)) T_j`.
* Provado: a identidade de variancia `∑_j ∏_α (v_α(j_α))² = ∏_α ∑_i v_α(i)²` (algebrica);
  `X v ~ N(0, ∑_j c_j²)`, logo `N(0,1)` quando `‖v^α‖ = 1` para todo `α`
  (`iIndepFun.hasGaussianLaw_fun_sum` + media e variancia); a cauda
  `P(s < |Z|) ≤ 2 e^{−s²/2}` para `Z ~ N(0,1)` via Chernoff (`measure_ge_le_exp_mul_mgf`),
  e a forma do livro com `s = ε√d`.
* "Nao pode ser aumentada": NAO formalizado como assintotica. O mutante
  `mutant_exponent_one_false` mostra que o expoente `−dε²` (constante `1` em vez de `1/2`) e
  falso ja em `d = 1`, `ε = 3`.
-/

noncomputable section

namespace LeanReal.Chap01Gaussian

open MeasureTheory ProbabilityTheory Finset Real

variable {Ω : Type*} [MeasurableSpace Ω] {P : Measure Ω} {d k : ℕ}

/-- Coeficiente `c_j(v) = ∏_α v_α(j_α)` do multi-indice ordenado `j`. -/
def coeff (v : Fin k → Fin d → ℝ) (j : Fin k → Fin d) : ℝ := ∏ a, v a (j a)

/-- A avaliacao multilinear `X(v) = ∑_j c_j(v) 𝒯_j = √d f̂_𝒯(v)`. -/
def X (T : (Fin k → Fin d) → Ω → ℝ) (v : Fin k → Fin d → ℝ) (ω : Ω) : ℝ :=
  ∑ j, coeff v j * T j ω

/-! ## A identidade de variancia -/

/-- `∑_j ∏_α (v_α(j_α))² = ∏_α ‖v_α‖²` (a conta de variancia do livro). -/
theorem sum_coeff_sq (v : Fin k → Fin d → ℝ) :
    ∑ j, coeff v j ^ 2 = ∏ a, ∑ i, v a i ^ 2 := by
  have h := Finset.prod_univ_sum (fun _ : Fin k => (univ : Finset (Fin d)))
    (fun a i => v a i ^ 2)
  rw [Fintype.piFinset_univ] at h
  rw [h]
  refine Finset.sum_congr rfl fun j _ => ?_
  rw [coeff, Finset.prod_pow]

/-- Com `‖v_α‖ = 1` para todo `α`, `∑_j c_j² = 1`. -/
theorem sum_coeff_sq_eq_one (v : Fin k → Fin d → ℝ) (hunit : ∀ a, ∑ i, v a i ^ 2 = 1) :
    ∑ j, coeff v j ^ 2 = 1 := by
  rw [sum_coeff_sq]; simp [hunit]

/-! ## Gaussianidade exata para `v` fixo -/

/-- **`thm:critical_scaling` (ii), lei de `X(v)` para `v` fixo**: combinacao linear de
gaussianas `N(0,1)` independentes e `N(0, ∑ c_j²)`. -/
theorem hasLaw_X [IsProbabilityMeasure P] (T : (Fin k → Fin d) → Ω → ℝ)
    (hT : ∀ j, HasLaw (T j) (gaussianReal 0 1) P)
    (hind : iIndepFun T P) (v : Fin k → Fin d → ℝ) :
    HasLaw (X T v) (gaussianReal 0 (∑ j, coeff v j ^ 2).toNNReal) P := by
  -- as parcelas `Y j = c_j T_j`
  set Y : (Fin k → Fin d) → Ω → ℝ := fun j ω => coeff v j * T j ω with hY
  have hYg : ∀ j, HasGaussianLaw (Y j) P := fun j => by
    have := (hT j).hasGaussianLaw.fun_smul (coeff v j)
    simpa [hY, smul_eq_mul] using this
  have hYind : iIndepFun Y P := by
    have := hind.comp (fun j x => coeff v j * x) (fun j => measurable_const_mul _)
    simpa [hY, Function.comp_def] using this
  have hXg : HasGaussianLaw (X T v) P := by
    have := hYind.hasGaussianLaw_fun_sum hYg
    convert this using 1
    funext ω; simp [X, hY]
  have hmap := hXg.map_eq_gaussianReal
  -- media
  have hmean : P[X T v] = 0 := by
    have hint : ∀ j ∈ (univ : Finset (Fin k → Fin d)), Integrable (Y j) P :=
      fun j _ => (hYg j).integrable
    have : P[X T v] = ∑ j, P[Y j] := by
      simp only [X, hY]
      exact integral_finsetSum _ hint
    rw [this]
    refine Finset.sum_eq_zero fun j _ => ?_
    simp only [hY]
    rw [integral_const_mul, (hT j).integral_eq, integral_id_gaussianReal, mul_zero]
  -- variancia
  have hvar : Var[X T v; P] = ∑ j, coeff v j ^ 2 := by
    have h1 : Var[X T v; P] = Var[∑ j, Y j; P] := by
      congr 1; funext ω; simp [X, hY, Finset.sum_apply]
    rw [h1, IndepFun.variance_sum (fun j _ => (hYg j).memLp_two)
      (fun i _ j _ hij => hYind.indepFun hij)]
    refine Finset.sum_congr rfl fun j _ => ?_
    simp only [hY]
    rw [variance_const_mul, (hT j).variance_eq, variance_id_gaussianReal]
    simp
  refine ⟨hXg.aemeasurable, ?_⟩
  rw [hmap, hmean, hvar]

/-- **`thm:critical_scaling` (ii), gaussianidade exata**: com `‖v_α‖ = 1` para todo `α`,
`X(v) = √d f̂_𝒯(v) ~ N(0,1)`. -/
theorem hasLaw_X_unit [IsProbabilityMeasure P] (T : (Fin k → Fin d) → Ω → ℝ)
    (hT : ∀ j, HasLaw (T j) (gaussianReal 0 1) P) (hind : iIndepFun T P)
    (v : Fin k → Fin d → ℝ) (hunit : ∀ a, ∑ i, v a i ^ 2 = 1) :
    HasLaw (X T v) (gaussianReal 0 1) P := by
  have := hasLaw_X T hT hind v
  rwa [sum_coeff_sq_eq_one v hunit, Real.toNNReal_one] at this

/-! ## Cauda gaussiana -/

/-- Cauda superior de `N(0,1)` por Chernoff: `P(s ≤ Z) ≤ e^{−s²/2}` para `s ≥ 0`. -/
theorem upper_tail (Z : Ω → ℝ) (hZ : HasLaw Z (gaussianReal 0 1) P) (s : ℝ) (hs : 0 ≤ s) :
    P.real {ω | s ≤ Z ω} ≤ Real.exp (-(s ^ 2) / 2) := by
  have : IsProbabilityMeasure P := hZ.hasGaussianLaw.isProbabilityMeasure
  have hint : Integrable (fun ω => Real.exp (s * Z ω)) P := by
    rw [← mgf_pos_iff, mgf_gaussianReal hZ]; exact Real.exp_pos _
  have h := measure_ge_le_exp_mul_mgf s hs hint
  rw [mgf_gaussianReal hZ, ← Real.exp_add] at h
  refine h.trans (le_of_eq ?_)
  congr 1
  simp; ring

/-- Cauda inferior de `N(0,1)`: `P(Z ≤ −s) ≤ e^{−s²/2}` para `s ≥ 0`. -/
theorem lower_tail (Z : Ω → ℝ) (hZ : HasLaw Z (gaussianReal 0 1) P) (s : ℝ) (hs : 0 ≤ s) :
    P.real {ω | Z ω ≤ -s} ≤ Real.exp (-(s ^ 2) / 2) := by
  have : IsProbabilityMeasure P := hZ.hasGaussianLaw.isProbabilityMeasure
  have hint : Integrable (fun ω => Real.exp (-s * Z ω)) P := by
    rw [← mgf_pos_iff, mgf_gaussianReal hZ]; exact Real.exp_pos _
  have h := measure_le_le_exp_mul_mgf (-s) (t := -s) (by linarith) hint
  rw [mgf_gaussianReal hZ, ← Real.exp_add] at h
  refine h.trans (le_of_eq ?_)
  congr 1
  simp; ring

/-- **Cauda bilateral**: `P(s < |Z|) ≤ 2 e^{−s²/2}` para `Z ~ N(0,1)`, `s ≥ 0`. -/
theorem two_sided_tail (Z : Ω → ℝ) (hZ : HasLaw Z (gaussianReal 0 1) P) (s : ℝ) (hs : 0 ≤ s) :
    P.real {ω | s < |Z ω|} ≤ 2 * Real.exp (-(s ^ 2) / 2) := by
  have : IsProbabilityMeasure P := hZ.hasGaussianLaw.isProbabilityMeasure
  have hsub : {ω | s < |Z ω|} ⊆ {ω | s ≤ Z ω} ∪ {ω | Z ω ≤ -s} := by
    intro ω hω
    simp only [Set.mem_ofPred_eq, Set.mem_union] at hω ⊢
    rcases le_or_gt 0 (Z ω) with h | h
    · left; rw [abs_of_nonneg h] at hω; exact hω.le
    · right; rw [abs_of_neg h] at hω; linarith
  calc P.real {ω | s < |Z ω|} ≤ P.real ({ω | s ≤ Z ω} ∪ {ω | Z ω ≤ -s}) :=
        measureReal_mono hsub
    _ ≤ P.real {ω | s ≤ Z ω} + P.real {ω | Z ω ≤ -s} := measureReal_union_le _ _
    _ ≤ Real.exp (-(s ^ 2) / 2) + Real.exp (-(s ^ 2) / 2) :=
        add_le_add (upper_tail Z hZ s hs) (lower_tail Z hZ s hs)
    _ = 2 * Real.exp (-(s ^ 2) / 2) := by ring

/-- **`thm:critical_scaling` (ii), desigualdade (eq:concentration_inequality)** para `v` fixo:
`P(|f̂_𝒯(v)| > ε) ≤ 2 exp(−dε²/2)`, com `f̂ = X/√d`. -/
theorem concentration [IsProbabilityMeasure P] (T : (Fin k → Fin d) → Ω → ℝ)
    (hT : ∀ j, HasLaw (T j) (gaussianReal 0 1) P) (hind : iIndepFun T P)
    (v : Fin k → Fin d → ℝ) (hunit : ∀ a, ∑ i, v a i ^ 2 = 1) (ε : ℝ) (hε : 0 < ε) :
    P.real {ω | ε < |X T v ω / Real.sqrt d|} ≤ 2 * Real.exp (-(d * ε ^ 2) / 2) := by
  have hZ := hasLaw_X_unit T hT hind v hunit
  rcases Nat.eq_zero_or_pos d with hd | hd
  · -- `d = 0`: `X/√0 = 0`, e o conjunto e vazio
    subst hd
    have : {ω | ε < |X T v ω / Real.sqrt (0 : ℕ)|} = ∅ := by
      ext ω; simp [hε.le]
    rw [this]; simp [measureReal_empty]
  have hsd : 0 < Real.sqrt d := Real.sqrt_pos.mpr (by exact_mod_cast hd)
  have hset : {ω | ε < |X T v ω / Real.sqrt d|} = {ω | ε * Real.sqrt d < |X T v ω|} := by
    ext ω
    simp only [Set.mem_ofPred_eq, abs_div, abs_of_pos hsd, lt_div_iff₀ hsd]
  rw [hset]
  have h := two_sided_tail (X T v) hZ (ε * Real.sqrt d) (by positivity)
  refine h.trans (le_of_eq ?_)
  congr 2
  rw [mul_pow, Real.sq_sqrt (Nat.cast_nonneg d)]; ring

/-! ## Testemunha: `d = 2`, `k = 2`, `v¹ = v² = (3/5, 4/5)`, produto de gaussianas

O espaco e `(Fin 2 → Fin 2) → ℝ` com `Measure.pi` de `N(0,1)`; `T_j = eval j`. Os coeficientes sao
`9/25, 12/25, 12/25, 16/25`, com soma de quadrados `1`: a hipotese `‖v_α‖ = 1` e verificada com
dados nao triviais e `X(v)` e uma combinacao genuina de quatro gaussianas. -/

/-- Medida produto de `N(0,1)` em `ι → ℝ`. -/
def gaussPi (ι : Type*) [Fintype ι] : Measure (ι → ℝ) :=
  Measure.pi fun _ : ι => gaussianReal 0 1

instance (ι : Type*) [Fintype ι] : IsProbabilityMeasure (gaussPi ι) := by
  unfold gaussPi; infer_instance

/-- As coordenadas sao independentes sob `gaussPi`. -/
theorem iIndepFun_eval (ι : Type*) [Fintype ι] :
    iIndepFun (fun j (ω : ι → ℝ) => ω j) (gaussPi ι) := by
  have := iIndepFun_pi (μ := fun _ : ι => gaussianReal 0 1) (X := fun _ => id)
    (fun _ => aemeasurable_id)
  simpa [gaussPi] using this

/-- Cada coordenada tem lei `N(0,1)` sob `gaussPi`. -/
theorem hasLaw_eval (ι : Type*) [Fintype ι] (j : ι) :
    HasLaw (fun ω : ι → ℝ => ω j) (gaussianReal 0 1) (gaussPi ι) :=
  ⟨(measurable_pi_apply j).aemeasurable,
    (measurePreserving_eval (fun _ : ι => gaussianReal 0 1) j).map_eq⟩

/-- O vetor unitario `(3/5, 4/5)` em cada um dos `k = 2` fatores. -/
def vw : Fin 2 → Fin 2 → ℝ := fun _ => ![3 / 5, 4 / 5]

theorem vw_unit : ∀ a, ∑ i, vw a i ^ 2 = 1 := by
  intro a; simp [vw, Fin.sum_univ_two]; norm_num

theorem vw_coeff_ne : coeff vw ![0, 1] = 12 / 25 := by
  simp [coeff, vw, Fin.prod_univ_two]; norm_num

/-- Na testemunha, `X(v) ~ N(0,1)` exatamente. -/
theorem witness :
    (∀ j, HasLaw (fun ω : (Fin 2 → Fin 2) → ℝ => ω j) (gaussianReal 0 1) (gaussPi _)) ∧
    iIndepFun (fun j (ω : (Fin 2 → Fin 2) → ℝ) => ω j) (gaussPi _) ∧
    (∀ a, ∑ i, vw a i ^ 2 = 1) ∧
    HasLaw (X (fun j (ω : (Fin 2 → Fin 2) → ℝ) => ω j) vw) (gaussianReal 0 1) (gaussPi _) :=
  ⟨hasLaw_eval _, iIndepFun_eval _, vw_unit,
    hasLaw_X_unit _ (hasLaw_eval _) (iIndepFun_eval _) vw vw_unit⟩

/-! ## Mutantes provados FALSOS -/

/-- Mutante 1: sem `‖v_α‖ = 1`, a lei nao e `N(0,1)`. Contraexemplo: `d = k = 1`, `v = 2`,
`X = 2T ~ N(0,4)`. -/
theorem mutant_no_unit_false :
    ¬ (∀ (d k : ℕ) (T : (Fin k → Fin d) → ((Fin k → Fin d) → ℝ) → ℝ),
        (∀ j, HasLaw (T j) (gaussianReal 0 1) (gaussPi (Fin k → Fin d))) →
        iIndepFun T (gaussPi (Fin k → Fin d)) →
        ∀ v : Fin k → Fin d → ℝ, HasLaw (X T v) (gaussianReal 0 1) (gaussPi (Fin k → Fin d))) := by
  intro h
  have h1 := h 1 1 (fun j ω => ω j) (hasLaw_eval _) (iIndepFun_eval _) (fun _ _ => 2)
  have h2 := hasLaw_X (P := gaussPi (Fin 1 → Fin 1)) (fun j ω => ω j) (hasLaw_eval _)
    (iIndepFun_eval _) (fun _ _ => 2)
  have hv : (∑ j : Fin 1 → Fin 1, coeff (fun _ _ => (2 : ℝ)) j ^ 2) = 4 := by
    simp [coeff]; norm_num
  rw [hv] at h2
  have := h1.map_eq.symm.trans h2.map_eq
  rw [gaussianReal_ext_iff] at this
  have h4 := this.2
  rw [← NNReal.coe_inj] at h4
  norm_num at h4

/-- A densidade de `N(0,1)` e `≥ (√(2π))⁻¹ e^{−8}` em `[−4,−3] ∪ [3,4]`. -/
theorem pdf_lower (x : ℝ) (hx : |x| ≤ 4) :
    (Real.sqrt (2 * π))⁻¹ * Real.exp (-8) ≤ gaussianPDFReal 0 1 x := by
  simp only [gaussianPDFReal, NNReal.coe_one, mul_one, sub_zero]
  have hx2 : x ^ 2 ≤ 16 := by
    have := abs_le.mp hx
    nlinarith [this.1, this.2]
  gcongr
  linarith

/-- Mutante 2 (o `1/2` do expoente nao pode virar `1`): `P(3 < |Z|) ≤ 2e^{−9}` e FALSO para
`Z ~ N(0,1)`, porque `P(3 < |Z|) ≥ 2 (√(2π))⁻¹ e^{−8}` e `e > √(2π)`. -/
theorem mutant_exponent_one_false :
    ¬ (∀ s : ℝ, 0 ≤ s → (gaussianReal 0 1).real {x | s < |x|} ≤ 2 * Real.exp (-(s ^ 2))) := by
  intro h
  have h3 := h 3 (by norm_num)
  norm_num at h3
  set S : Set ℝ := Set.Ioo (-4) (-3) ∪ Set.Ioo 3 4 with hS
  have hSabs : ∀ x ∈ S, |x| ≤ 4 := by
    intro x hx
    simp only [hS, Set.mem_union, Set.mem_Ioo] at hx
    rw [abs_le]
    rcases hx with ⟨h1, h2⟩ | ⟨h1, h2⟩ <;> constructor <;> linarith
  have hSsub : S ⊆ {x | 3 < |x|} := by
    intro x hx
    simp only [hS, Set.mem_union, Set.mem_Ioo] at hx
    simp only [Set.mem_ofPred_eq]
    rcases hx with ⟨h1, h2⟩ | ⟨h1, h2⟩
    · rw [abs_of_neg (by linarith)]; linarith
    · rw [abs_of_pos (by linarith)]; linarith
  have hmeas : MeasurableSet S := measurableSet_Ioo.union measurableSet_Ioo
  have hdisj : Disjoint (Set.Ioo (-4 : ℝ) (-3)) (Set.Ioo 3 4) := by
    rw [Set.disjoint_left]
    intro x hx1 hx2
    simp only [Set.mem_Ioo] at hx1 hx2
    linarith [hx1.2, hx2.1]
  have hvolS : volume.real S = 2 := by
    rw [hS, measureReal_union hdisj measurableSet_Ioo (h₁ := by simp) (h₂ := by simp)]
    simp; norm_num
  have hvolS' : volume S ≠ ⊤ := by
    rw [hS]
    exact ((measure_union_le _ _).trans_lt (ENNReal.add_lt_top.mpr
      ⟨by simp [Real.volume_Ioo], by simp [Real.volume_Ioo]⟩)).ne
  -- cota inferior por integral da densidade
  have hlow : (Real.sqrt (2 * π))⁻¹ * Real.exp (-8) * 2 ≤ (gaussianReal 0 1).real S := by
    have hint := setIntegral_ge_of_const_le_real (μ := volume)
      (c := (Real.sqrt (2 * π))⁻¹ * Real.exp (-8)) hmeas hvolS'
      (fun x hx => pdf_lower x (hSabs x hx)) (integrable_gaussianPDFReal 0 1).integrableOn
    rw [hvolS] at hint
    rw [measureReal_def, gaussianReal_apply_eq_integral 0 one_ne_zero S,
      ENNReal.toReal_ofReal (integral_nonneg fun x => gaussianPDFReal_nonneg _ _ _)]
    exact hint
  have hmono : (gaussianReal 0 1).real S ≤ (gaussianReal 0 1).real {x | 3 < |x|} :=
    measureReal_mono hSsub
  have hchain := hlow.trans (hmono.trans h3)
  -- `e^{−8}/√(2π) ≤ e^{−9}` forca `e ≤ √(2π) < 2.51`, absurdo
  have hsq : Real.sqrt (2 * π) < 2.51 := by
    rw [Real.sqrt_lt' (by norm_num)]
    linarith [Real.pi_lt_d2]
  have hsqpos : 0 < Real.sqrt (2 * π) := Real.sqrt_pos.mpr (by positivity)
  have he : Real.exp (-8) = Real.exp (-9) * Real.exp 1 := by rw [← Real.exp_add]; norm_num
  rw [he] at hchain
  have h9 : 0 < Real.exp (-9) := Real.exp_pos _
  have hkey : Real.exp 1 ≤ Real.sqrt (2 * π) := by
    have h1 : (Real.sqrt (2 * π))⁻¹ * (Real.exp (-9) * Real.exp 1) * 2 ≤ 2 * Real.exp (-9) :=
      hchain
    have h2 : Real.exp (-9) * Real.exp 1 ≤ Real.exp (-9) * Real.sqrt (2 * π) := by
      have := mul_le_mul_of_nonneg_left h1 hsqpos.le
      rw [show Real.sqrt (2 * π) * ((Real.sqrt (2 * π))⁻¹ * (Real.exp (-9) * Real.exp 1) * 2)
          = (Real.sqrt (2 * π) * (Real.sqrt (2 * π))⁻¹) * (Real.exp (-9) * Real.exp 1) * 2
          by ring, mul_inv_cancel₀ hsqpos.ne', one_mul] at this
      linarith
    exact le_of_mul_le_mul_left h2 h9
  linarith [Real.exp_one_gt_d9]

end LeanReal.Chap01Gaussian

#print axioms LeanReal.Chap01Gaussian.sum_coeff_sq
#print axioms LeanReal.Chap01Gaussian.hasLaw_X
#print axioms LeanReal.Chap01Gaussian.hasLaw_X_unit
#print axioms LeanReal.Chap01Gaussian.upper_tail
#print axioms LeanReal.Chap01Gaussian.two_sided_tail
#print axioms LeanReal.Chap01Gaussian.concentration
#print axioms LeanReal.Chap01Gaussian.witness
#print axioms LeanReal.Chap01Gaussian.mutant_no_unit_false
#print axioms LeanReal.Chap01Gaussian.mutant_exponent_one_false
