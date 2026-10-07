# formal_proofs_mathlib: Lean 4 + Mathlib formalization

This folder holds the **only** Lean code in this repository that verifies mathematics.
Every statement below is a Mathlib statement. It compiles with 0 errors and 0 warnings, uses no `sorry`, and
introduces no `axiom`. `#print axioms` reports only Lean's three standard axioms:
`propext`, `Classical.choice` and `Quot.sound`.

The other Lean folders (`formal_proofs_book/`, `formal_proofs_lean4/`, and the Lean folders inside
`Manuscritos_Avulsos/`) are a naming skeleton with Bool, Float or Nat placeholders. They verify no
mathematics; see the `README_SKELETON.md` in each of them.

**Scope.** Two pieces of the monograph are formalized:
- part of Chapter 3 (continuous Pascal triangle);
- the algebraic, pointwise content of one theorem of Chapter 12. The same theorem appears in the
  *Simplicial Quantum Gravity* paper.

Nothing else in the monograph or in the papers is machine-checked.

- Toolchain: `leanprover/lean4:v4.35.0-rc2` (`lean-toolchain`).
- Mathlib: commit `b1007d8abfd0c776eb8a75e8f6bf26db5eae4a69`, pinned in `lakefile.toml` and
  `lake-manifest.json`.

## Theorems

Book = *Geometry, Tensors, and Quantum Gravity* (Zenodo 10.5281/zenodo.22290043).
SQG = *Simplicial Quantum Gravity on Δ₄ × Δ₂* (Zenodo 10.5281/zenodo.22704111).

The **Axioms** column gives the `#print axioms` output. "std" means `[propext, Classical.choice, Quot.sound]`;
no `sorryAx` and no project axiom appears.

### `LeanReal/Chap03Pascal.lean` — Book, Chapter 3

`cbinom x y = Γ(x+1)·Γ(y+1)⁻¹·Γ(x−y+1)⁻¹` on ℂ. This is the Definition "Continuous Binomial Coefficient".
Mathlib's `Γ⁻¹` is 0 at the poles, so it equals the entire function `1/Γ` used in the text.

| Lean name | Statement formalized | Coverage | Axioms |
|---|---|---|---|
| `inv_Gamma_neg_nat` | `Γ(−n)⁻¹ = 0` (auxiliary: Mathlib's `Γ⁻¹` agrees with `1/Γ`) | auxiliary | std |
| `stifel` | Prop. "Global Stifel Recurrence": `C(x−1,y) + C(x−1,y−1) = C(x,y)`, all `y ∈ ℂ`, `x ∉ {0,−1,−2,…}` | full | std |
| `star_of_david` | Thm. "Continuous Star of David" (`thm:star_of_david`), eq. `sod_product` | full; holds for all `n, k ∈ ℂ`, which is stronger than the text | std |
| `cbinom_zero_of_y_neg` | Prop. "Global Meromorphic Extension and Zero Loci", zeros for `y ∈ ℤ_{<0}` | full (zero part) | std |
| `cbinom_zero_of_xy_neg` | same Prop., zeros for `x − y ∈ ℤ_{<0}` | full (zero part) | std |
| `cbinom_real_pos` | same Prop., positivity for real `x > 0`, `0 ≤ y ≤ x` | full (positivity part) | std |
| `row_sum` | discrete identity `∑ C(n,k) = 2ⁿ` quoted in Ch. 3, a classical result already in Mathlib | full (classical) | std |
| `multinomial_row_sum` | discrete identity `∑ multinomial = mⁿ` quoted in Ch. 3, classical | full (classical) | std |

The same Proposition also asserts a meromorphic extension. That part is **not** formalized.

### `LeanReal/Chap12Constraint.lean` — Book, Ch. 12, Thm. "Pointwise Constraint Bounds" (`thm:minimax_hamiltonian_regularization`)

| Lean name | Statement formalized | Coverage | Axioms |
|---|---|---|---|
| `constraint_bounds` | items (i)–(ii) for principal curvatures `k₁,k₂,k₃` with `|kᵢ| ≤ κ`: `0 ≤ ∑kᵢ² ≤ 3κ²` and `s − 6κ² ≤ s + ∑kᵢ² − (∑kᵢ)² ≤ s + 2κ²`, where `s = 2Λ + 16πGρ` | **reduced form**: the diagonalization of `K_ij` and the Hamiltonian constraint are not part of this statement; they enter as the shape of `³R` | std |
| `constraint_bounds_sharp` | both endpoints are attained by `(κ,κ,κ)` and `(κ,κ,−κ)` | reduced form | std |

### `LeanReal/Chap12ConstraintMatrix.lean` — same theorem, pointwise matrix form; also SQG Thm. `thm:minimax_shear`

This file states the theorem at one point of a spacelike hypersurface, in an orthonormal frame of `γ`:
- `K` is a real symmetric 3×3 matrix;
- `frobSq K = K_ijK^ij`;
- `shear K = σ_ij`;
- `IIBound K κ` is `∀ v, |vᵀKv| ≤ κ vᵀv`. This is the text's definition of `‖II‖ ≤ κ*` (SQG eq. `minimax_bound_def`) at that point;
- `HamiltonianConstraint` is SQG eq. `wdw_constraint`, taken as a **hypothesis**.

| Lean name | Statement formalized | Coverage | Axioms |
|---|---|---|---|
| `frobSq_shear` | `σ_ijσ^ij = K_ijK^ij − K²/3` | full | std |
| `hamiltonian_iff` | SQG form of the constraint ⟺ Book eq. `wdw_hamiltonian`: `³R + K² − K_ijK^ij = 2Λ + 16πGρ` | full | std |
| `frobSq_eq_trace_mul` | `K_ijK^ij = tr(K²)` for symmetric `K` (auxiliary) | auxiliary | std |
| `trace_mul_self_eq` | `tr(K²) = ∑ λᵢ²`, by Mathlib's spectral theorem | auxiliary | std |
| `trace_eq_sum` | `tr K = ∑ λᵢ` (auxiliary) | auxiliary | std |
| `abs_eigenvalue_le` | `IIBound K κ ⟹ |λᵢ| ≤ κ` | full | std |
| `IIBound_of_abs_eigenvalue_le` | `(∀ i, |λᵢ| ≤ κ) ⟹ IIBound K κ` (auxiliary) | auxiliary | std |
| `IIBound_iff` | `IIBound K κ ⟺ ∀ i, |λᵢ| ≤ κ` ("no further relation among the λᵢ") | full | std |
| `IIBound_of_l2_opNorm_le` | Mathlib ℓ² operator norm `‖K‖ ≤ κ ⟹ IIBound K κ`; the converse is not proved | one direction | std |
| `constraint_bounds_matrix` | (i) `0 ≤ K_ijK^ij ≤ 3κ²`, `0 ≤ σσ ≤ 3κ² − K²/3`; (ii) `2Λ+16πGρ−6κ² ≤ ³R ≤ 2Λ+16πGρ+2κ²` | pointwise, orthonormal frame, constraint as hypothesis | std |
| `constraint_bounds_opNorm` | same conclusion, hypothesis `‖K‖_op ≤ κ` | same | std |
| `constraint_bounds_vacuum` | case `ρ = 0` | same | std |
| `IIBound_diagonal` | diagonal matrices with entries in `[−κ, κ]` satisfy `IIBound` (auxiliary) | auxiliary | std |
| `constraint_bounds_matrix_sharp` | sharpness: `diag(κ,κ,κ)` and `diag(κ,κ,−κ)` are admissible, attain `KK = 3κ²` and `σσ = 3κ² − K²/3`, and satisfy the constraint with `³R` at the lower and upper endpoint | algebraic, pointwise | std |

**Not formalized:**
- the Lorentzian manifold, the ADM foliation, and the derivation of the constraint from Einstein's equations (Gauss equation);
- a general frame `γ_ij ≠ δ_ij`;
- the minimax problem `κ* = inf_Σ ‖II_Σ‖_{L∞}`;
- the converse operator-norm inequality;
- that ρ is the energy density `T_μν nᵘnᵛ` and that `³R` is the scalar curvature of `γ`. In the Lean code both are free real numbers.

Sharpness is shown at the level of matrices at a point. It is not shown at the level of spacetimes.

## Negative controls (`mutants/`)

Each mutant restates one verified theorem with a single change and reuses the original proof. Every mutated
statement is mathematically false; the counterexample is in each file's header or comment. All 14 fail to
compile, and `#print axioms` shows `sorryAx` for each one. Full output: `mutants/mutantes_saida_formal_proofs_mathlib.txt`.

| file | mutation | failure |
|---|---|---|
| `M1_KK_3para2` | `KK ≤ 2κ²` | linarith |
| `M2_shear_div3para2` | `σσ ≤ 3κ² − K²/2` | linarith |
| `M3_inferior_6para5` | `³R ≥ s − 5κ²` | linarith |
| `M4_superior_2para1` | `³R ≤ s + κ²` | linarith |
| `M5_autovalor_meio` | `|λᵢ| ≤ κ/2` | type mismatch |
| `M6_frobshear_div3para2` | `σσ = KK − K²/2` | unsolved goals |
| `M7_traco_sem_quadrado` | `tr(K²) = ∑ λᵢ` | unsolved goals |
| `M8_sharp_6para5` | `diag(κ,κ,κ)` with `³R = s − 5κ²` | unsolved goals |
| `M9_M14_chap03_chap12reduced` (m9) | Stifel with `−` | unsolved goals |
| (m10) | Star of David, `k+1 → k+2` on one side | rewrite fails |
| (m11) | positivity with `y ≤ x + 3` | linarith |
| (m12) | `∑ multinomial = mⁿ + 1` | type mismatch |
| (m13) | reduced upper bound `s + κ²` | linarith |
| (m14) | reduced `∑kᵢ² ≤ 2κ²` | linarith |

`M1`–`M8` are generated by `mutants/gerar_mutantes.py`.

## How to reproduce

On a clean machine, from this folder:

```bash
lake exe cache get   # downloads the prebuilt Mathlib .olean files for the pinned commit
lake build           # builds LeanReal; the #print axioms lines print the axiom lists
lake env lean mutants/M1_KK_3para2.lean   # each mutant must fail and show sorryAx
```

There is also `verificar.sh`, which does not use `lake`. It calls `lean` directly and reads, read-only, the
Mathlib `.olean` files already built under `../formal_proofs_book/.lake/packages`. That route only works if
that folder exists locally with the same toolchain and commit.

```bash
./verificar.sh                                   # the three modules, in dependency order
ARQ=mutants/M1_KK_3para2.lean ./verificar.sh     # one file
```

Last full run: 2026-10-07. All three modules compiled with 0 errors and 0 warnings, and all 24
`#print axioms` lines gave std. All 14 mutants failed with `sorryAx`.
