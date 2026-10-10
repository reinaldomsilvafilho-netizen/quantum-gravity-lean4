import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

/-!
# Capitulo 6, `assump:kigami_decimation` (item 3 do Lote A1, `PLANO_LIVRO_A.md`)

Fonte: `unified_quantum_gravity_book/chap06_sierpinski_fractal_resolvents_spectral_reduction.tex`,
Proposicao "Harmonic Decimation Renormalization Factor" (`assump:kigami_decimation`).

Enunciado congelado. `Γ₀` = grafo completo em `p₁,…,p_{m+1}` com condutancias unitarias. `Γ₁` =
rede de nivel um: vertices `p_i` e pontos medios `p_{ij} = p_{ji}` (`i ≠ j`); cada celula
`F_i(K)` carrega um grafo completo com condutancias unitarias em `{p_i} ∪ {p_{ij} : j ≠ i}`.
Afirmacao: o traco (complemento de Schur) de `Γ₁` em `{p₁,…,p_{m+1}}` e o grafo completo com
condutancias `(m+1)/(m+3)`; logo `ρ = (m+3)/(m+1)` e `r_m = (m+1)ρ = m+3` (`r₂ = 5`).
Prova do livro: por simetria, `u(p_{1j}) = a`, `u(p_{jk}) = b`; harmonicidade da
`2ma = 1 + (m-1)a + (m-1)b`, `2mb = 2a + 2(m-2)b`; logo `b = a/2`, `a = 2/(m+3)`; corrente
`m(1-a) = m(m+1)/(m+3) = mc`.

## Reducao declarada

* `m = 2` (6 vertices) e `m = 3` (10 vertices): o laplaciano de `Γ₁` e GERADO a partir da regra
  do livro (vertice `p_{ij}` ↔ par `(i,j)`, `i ≤ j`, com `p_i = (i,i)`; dois vertices distintos
  estao ligados na celula `i` sse ambos contem `i`; a condutancia e o numero de celulas comuns),
  e o complemento de Schur `L_BB - L_BI L_II⁻¹ L_IB` e calculado exatamente em `ℚ`. Isto e o
  enunciado completo para esses `m`.
* `m` geral: so a algebra do livro (o ansatz resolve o sistema 2×2, que tem solucao unica, e a
  corrente). A reducao por simetria (que a extensao harmonica tem a forma `(a, b)`) NAO e
  formalizada para `m` geral; para `m = 2, 3` ela e conferida (`harmonic_ext_m2/m3`).
* A identificacao `r_m = (m+1)ρ` com o fator de renormalizacao do laplaciano de Kigami e
  so a aritmetica.
-/

noncomputable section

namespace LeanReal.Chap06Kigami

open Matrix Finset

/-- Condutancia entre vertices `u = (u₁,u₂)`, `v = (v₁,v₂)` de `Γ₁`: numero de celulas `i` com
`i ∈ u` e `i ∈ v` (zero se `u = v`). -/
def cond {N : ℕ} (u v : Fin N × Fin N) : ℕ :=
  if u = v then 0 else (univ.filter fun i => (i = u.1 ∨ i = u.2) ∧ (i = v.1 ∨ i = v.2)).card

/-- Matriz de condutancias de uma enumeracao `vs` dos vertices. -/
def condM {N K : ℕ} (vs : Fin K → Fin N × Fin N) : Matrix (Fin K) (Fin K) ℕ :=
  fun a b => cond (vs a) (vs b)

/-- Laplaciano de rede `L = D - C` (em `ℚ`). -/
def lap {K : ℕ} (C : Matrix (Fin K) (Fin K) ℕ) : Matrix (Fin K) (Fin K) ℚ :=
  fun a b => if a = b then ∑ w, (C a w : ℚ) else -(C a b : ℚ)

/-- Traco (complemento de Schur) de `L` no conjunto `bd`, eliminando `it`. -/
def schur {K p q : ℕ} (L : Matrix (Fin K) (Fin K) ℚ) (bd : Fin p → Fin K) (it : Fin q → Fin K) :
    Matrix (Fin p) (Fin p) ℚ :=
  L.submatrix bd bd - L.submatrix bd it * (L.submatrix it it)⁻¹ * L.submatrix it bd

/-- Laplaciano do grafo completo `K_N` com condutancia `1`. -/
def lapK (N : ℕ) : Matrix (Fin N) (Fin N) ℚ := fun i j => if i = j then (N - 1 : ℚ) else -1

/-! ## `m = 2` -/

/-- Vertices de `Γ₁` para `m = 2`: `p₀,p₁,p₂` e depois `p₀₁,p₀₂,p₁₂`. -/
def verts2 : Fin 6 → Fin 3 × Fin 3 := ![(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]

/-- A enumeracao e fiel: injetiva e cobre exatamente os pares `i ≤ j`. -/
theorem verts2_faithful : Function.Injective verts2 ∧
    ∀ p : Fin 3 × Fin 3, p.1 ≤ p.2 ↔ ∃ a, verts2 a = p := by
  refine ⟨by decide, by decide⟩

theorem condM2 : condM verts2 = !![0, 0, 0, 1, 1, 0; 0, 0, 0, 1, 0, 1; 0, 0, 0, 0, 1, 1;
    1, 1, 0, 0, 1, 1; 1, 0, 1, 1, 0, 1; 0, 1, 1, 1, 1, 0] := by
  decide

def bd2 : Fin 3 → Fin 6 := Fin.castAdd 3
def it2 : Fin 3 → Fin 6 := Fin.natAdd 3

theorem L2_II : (lap (condM verts2)).submatrix it2 it2 = !![4, -1, -1; -1, 4, -1; -1, -1, 4] := by
  rw [condM2]; ext i j; fin_cases i <;> fin_cases j <;>
    simp [lap, it2, Fin.sum_univ_succ] <;> norm_num

theorem L2_BI : (lap (condM verts2)).submatrix bd2 it2 = !![-1, -1, 0; -1, 0, -1; 0, -1, -1] := by
  rw [condM2]; ext i j; fin_cases i <;> fin_cases j <;>
    simp [lap, bd2, it2]

theorem L2_IB : (lap (condM verts2)).submatrix it2 bd2 = !![-1, -1, 0; -1, 0, -1; 0, -1, -1] := by
  rw [condM2]; ext i j; fin_cases i <;> fin_cases j <;>
    simp [lap, bd2, it2]

theorem L2_BB : (lap (condM verts2)).submatrix bd2 bd2 = !![2, 0, 0; 0, 2, 0; 0, 0, 2] := by
  rw [condM2]; ext i j; fin_cases i <;> fin_cases j <;>
    simp [lap, bd2, Fin.sum_univ_succ] <;> norm_num

theorem L2_II_inv : (lap (condM verts2)).submatrix it2 it2 =
    !![4, -1, -1; -1, 4, -1; -1, -1, 4] ∧
    (!![4, -1, -1; -1, 4, -1; -1, -1, 4] : Matrix (Fin 3) (Fin 3) ℚ)⁻¹ =
      !![3/10, 1/10, 1/10; 1/10, 3/10, 1/10; 1/10, 1/10, 3/10] := by
  refine ⟨L2_II, ?_⟩
  apply Matrix.inv_eq_left_inv
  ext i j; fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_succ] <;> norm_num

/-- **`assump:kigami_decimation`, `m = 2`**: o traco de `Γ₁` nos vertices `p_i` e o grafo
completo `K₃` com condutancia `3/5 = (m+1)/(m+3)`. -/
theorem schur_m2 : schur (lap (condM verts2)) bd2 it2 = (3 / 5 : ℚ) • lapK 3 := by
  unfold schur
  rw [L2_BB, L2_BI, L2_IB, L2_II_inv.1, L2_II_inv.2]
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [lapK] <;> norm_num

/-- Extensao harmonica para `m = 2` com `u(p₀) = 1`, `u(p₁) = u(p₂) = 0`:
`u_I = -L_II⁻¹ L_IB e₀ = (a, a, b)` com `a = 2/5 = 2/(m+3)`, `b = 1/5 = a/2` (o ansatz do livro). -/
theorem harmonic_ext_m2 :
    -(((lap (condM verts2)).submatrix it2 it2)⁻¹ * (lap (condM verts2)).submatrix it2 bd2) *ᵥ
      ![1, 0, 0] = ![2 / 5, 2 / 5, 1 / 5] := by
  rw [L2_IB, L2_II_inv.1, L2_II_inv.2]
  ext i; fin_cases i <;>
    simp [Matrix.mulVec, dotProduct, Fin.sum_univ_succ] <;> norm_num

/-! ## `m = 3` -/

/-- Vertices de `Γ₁` para `m = 3`: `p₀,…,p₃` e depois `p₀₁,p₀₂,p₀₃,p₁₂,p₁₃,p₂₃`. -/
def verts3 : Fin 10 → Fin 4 × Fin 4 :=
  ![(0, 0), (1, 1), (2, 2), (3, 3), (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

theorem verts3_faithful : Function.Injective verts3 ∧
    ∀ p : Fin 4 × Fin 4, p.1 ≤ p.2 ↔ ∃ a, verts3 a = p := by
  refine ⟨by decide, by decide⟩

theorem condM3 : condM verts3 = !![
    0, 0, 0, 0, 1, 1, 1, 0, 0, 0;
    0, 0, 0, 0, 1, 0, 0, 1, 1, 0;
    0, 0, 0, 0, 0, 1, 0, 1, 0, 1;
    0, 0, 0, 0, 0, 0, 1, 0, 1, 1;
    1, 1, 0, 0, 0, 1, 1, 1, 1, 0;
    1, 0, 1, 0, 1, 0, 1, 1, 0, 1;
    1, 0, 0, 1, 1, 1, 0, 0, 1, 1;
    0, 1, 1, 0, 1, 1, 0, 0, 1, 1;
    0, 1, 0, 1, 1, 0, 1, 1, 0, 1;
    0, 0, 1, 1, 0, 1, 1, 1, 1, 0] := by
  decide

def bd3 : Fin 4 → Fin 10 := Fin.castAdd 6
def it3 : Fin 6 → Fin 10 := Fin.natAdd 4

def D3 : Matrix (Fin 6) (Fin 6) ℚ := !![
    6, -1, -1, -1, -1, 0;
    -1, 6, -1, -1, 0, -1;
    -1, -1, 6, 0, -1, -1;
    -1, -1, 0, 6, -1, -1;
    -1, 0, -1, -1, 6, -1;
    0, -1, -1, -1, -1, 6]

def N3 : Matrix (Fin 6) (Fin 6) ℚ := !![
    5/24, 1/16, 1/16, 1/16, 1/16, 1/24;
    1/16, 5/24, 1/16, 1/16, 1/24, 1/16;
    1/16, 1/16, 5/24, 1/24, 1/16, 1/16;
    1/16, 1/16, 1/24, 5/24, 1/16, 1/16;
    1/16, 1/24, 1/16, 1/16, 5/24, 1/16;
    1/24, 1/16, 1/16, 1/16, 1/16, 5/24]

def C3 : Matrix (Fin 6) (Fin 4) ℚ := !![
    -1, -1, 0, 0;
    -1, 0, -1, 0;
    -1, 0, 0, -1;
    0, -1, -1, 0;
    0, -1, 0, -1;
    0, 0, -1, -1]

theorem L3_II : (lap (condM verts3)).submatrix it3 it3 = D3 := by
  rw [condM3]; ext i j; fin_cases i <;> fin_cases j <;>
    simp [lap, it3, D3, Fin.sum_univ_succ] <;> norm_num

theorem L3_IB : (lap (condM verts3)).submatrix it3 bd3 = C3 := by
  rw [condM3]; ext i j; fin_cases i <;> fin_cases j <;>
    simp [lap, bd3, it3, C3]

theorem L3_BI : (lap (condM verts3)).submatrix bd3 it3 = C3ᵀ := by
  rw [condM3]; ext i j; fin_cases i <;> fin_cases j <;>
    simp [lap, bd3, it3, C3]

theorem L3_BB : (lap (condM verts3)).submatrix bd3 bd3 = (3 : ℚ) • (1 : Matrix (Fin 4) (Fin 4) ℚ) := by
  rw [condM3]; ext i j; fin_cases i <;> fin_cases j <;>
    simp [lap, bd3, Fin.sum_univ_succ] <;> norm_num

theorem D3_inv : D3⁻¹ = N3 := by
  apply Matrix.inv_eq_left_inv
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [N3, D3, Matrix.mul_apply, Fin.sum_univ_succ] <;> norm_num

/-- **`assump:kigami_decimation`, `m = 3`**: o traco de `Γ₁` nos vertices `p_i` e o grafo
completo `K₄` com condutancia `2/3 = (m+1)/(m+3)`. -/
theorem schur_m3 : schur (lap (condM verts3)) bd3 it3 = (2 / 3 : ℚ) • lapK 4 := by
  unfold schur
  rw [L3_BB, L3_BI, L3_IB, L3_II, D3_inv]
  ext i j; fin_cases i <;> fin_cases j <;>
    simp [N3, C3, Matrix.mul_apply, Fin.sum_univ_succ, lapK] <;> norm_num

/-- Extensao harmonica para `m = 3` com `u(p₀) = 1`: `u_I = (a,a,a,b,b,b)`, `a = 1/3 = 2/(m+3)`,
`b = 1/6 = a/2`. -/
theorem harmonic_ext_m3 :
    -(((lap (condM verts3)).submatrix it3 it3)⁻¹ * (lap (condM verts3)).submatrix it3 bd3) *ᵥ
      ![1, 0, 0, 0] = ![1 / 3, 1 / 3, 1 / 3, 1 / 6, 1 / 6, 1 / 6] := by
  rw [L3_IB, L3_II, D3_inv]
  ext i; fin_cases i <;>
    simp [N3, C3, Matrix.mulVec, dotProduct, Fin.sum_univ_succ] <;> norm_num

/-! ## `m` geral: a algebra da prova do livro -/

/-- **Prova de `assump:kigami_decimation`, `m` geral**: o sistema harmonico reduzido por simetria
`2ma = 1 + (m-1)a + (m-1)b`, `2mb = 2a + 2(m-2)b` tem a solucao unica `a = 2/(m+3)`, `b = a/2`. -/
theorem ansatz_unique (m : ℕ) (a b : ℚ) :
    (2 * m * a = 1 + (m - 1) * a + (m - 1) * b ∧ 2 * m * b = 2 * a + 2 * (m - 2) * b) ↔
      (a = 2 / (m + 3) ∧ b = a / 2) := by
  have hm : (0 : ℚ) < m + 3 := by positivity
  constructor
  · rintro ⟨h1, h2⟩
    have hb : b = a / 2 := by linarith
    refine ⟨?_, hb⟩
    rw [hb] at h1
    field_simp
    nlinarith
  · rintro ⟨ha, hb⟩
    subst hb; subst ha
    constructor <;> field_simp <;> ring

/-- Corrente `m(1-a) = m(m+1)/(m+3) = m·c` com `c = (m+1)/(m+3)`; `ρ = 1/c` e `r_m = (m+1)ρ = m+3`. -/
theorem current_and_factor (m : ℕ) :
    (m : ℚ) * (1 - 2 / (m + 3)) = m * ((m + 1) / (m + 3)) ∧
      ((m : ℚ) + 1) * (1 / ((m + 1) / (m + 3))) = m + 3 := by
  have h3 : (m : ℚ) + 3 ≠ 0 := by positivity
  have h1 : (m : ℚ) + 1 ≠ 0 := by positivity
  constructor
  · field_simp; ring
  · field_simp

/-- `r₂ = 5`. -/
example : ((2 : ℕ) : ℚ) + 3 = 5 := by norm_num

/-! ## Testemunha de nao trivialidade -/

/-- O traco nao e degenerado: para `m = 2` a entrada diagonal e `6/5` e a fora da diagonal `-3/5`
(nao e zero nem multiplo da identidade). -/
example : schur (lap (condM verts2)) bd2 it2 0 0 = 6 / 5 ∧
    schur (lap (condM verts2)) bd2 it2 0 1 = -3 / 5 := by
  rw [schur_m2]; simp [lapK]; norm_num

/-! ## Mutantes provados FALSOS -/

/-- Mutante 1: condutancia `(m+1)/(m+2) = 3/4` para `m = 2`. Falso. -/
theorem mutant_conductance_m2_false : schur (lap (condM verts2)) bd2 it2 ≠ (3 / 4 : ℚ) • lapK 3 := by
  intro h
  have := congrFun (congrFun h 0) 1
  rw [schur_m2] at this
  simp [lapK] at this
  norm_num at this

/-- Mutante 2: condutancia `(m+1)/(m+2) = 4/5` para `m = 3`. Falso. -/
theorem mutant_conductance_m3_false : schur (lap (condM verts3)) bd3 it3 ≠ (4 / 5 : ℚ) • lapK 4 := by
  intro h
  have := congrFun (congrFun h 0) 1
  rw [schur_m3] at this
  simp [lapK] at this
  norm_num at this

/-- Mutante 3: "o traco e `Γ₀` sem renormalizar" (condutancia `1`). Falso para `m = 2`. -/
theorem mutant_unrenormalized_false : schur (lap (condM verts2)) bd2 it2 ≠ lapK 3 := by
  intro h
  have := congrFun (congrFun h 0) 1
  rw [schur_m2] at this
  simp [lapK] at this
  norm_num at this

/-- Mutante 4 (ansatz): `b = a` em vez de `b = a/2` nao resolve o sistema (para `m = 2`). -/
theorem mutant_ansatz_false :
    ¬ (2 * (2 : ℕ) * (2 / 5 : ℚ) = 1 + ((2 : ℕ) - 1) * (2 / 5) + ((2 : ℕ) - 1) * (2 / 5) ∧
      2 * (2 : ℕ) * (2 / 5 : ℚ) = 2 * (2 / 5) + 2 * ((2 : ℕ) - 2) * (2 / 5)) := by
  norm_num

end LeanReal.Chap06Kigami

#print axioms LeanReal.Chap06Kigami.verts2_faithful
#print axioms LeanReal.Chap06Kigami.schur_m2
#print axioms LeanReal.Chap06Kigami.harmonic_ext_m2
#print axioms LeanReal.Chap06Kigami.verts3_faithful
#print axioms LeanReal.Chap06Kigami.schur_m3
#print axioms LeanReal.Chap06Kigami.harmonic_ext_m3
#print axioms LeanReal.Chap06Kigami.ansatz_unique
#print axioms LeanReal.Chap06Kigami.current_and_factor
#print axioms LeanReal.Chap06Kigami.mutant_conductance_m2_false
#print axioms LeanReal.Chap06Kigami.mutant_conductance_m3_false
#print axioms LeanReal.Chap06Kigami.mutant_unrenormalized_false
#print axioms LeanReal.Chap06Kigami.mutant_ansatz_false
