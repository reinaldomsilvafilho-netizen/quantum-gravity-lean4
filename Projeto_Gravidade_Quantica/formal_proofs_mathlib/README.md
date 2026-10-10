# formal_proofs_mathlib: Lean 4 + Mathlib formalization

This folder holds the **only** Lean code in this repository that verifies mathematics.
Every statement below is a Mathlib statement. It compiles with 0 errors and 0 warnings, uses no `sorry`, and
introduces no `axiom`. `#print axioms` reports only Lean's three standard axioms:
`propext`, `Classical.choice` and `Quot.sound`.

The other Lean folders (`formal_proofs_book/`, `formal_proofs_lean4/`, and the Lean folders inside
`Manuscritos_Avulsos/`) are a naming skeleton with Bool, Float or Nat placeholders. They verify no
mathematics; see the `README_SKELETON.md` in each of them.

**Scope.** The following pieces are formalized:
- part of Chapter 3 (continuous Pascal triangle);
- the algebraic, pointwise content of one theorem of Chapter 12. The same theorem appears in the
  *Simplicial Quantum Gravity* paper;
- since 2026-10-09: elementary statements of four Zenodo works. These are the fermion-mass paper
  (Koide identity, CKM of two commuting sectors), the Yang–Mills paper (convexity of the truncated
  Gribov region, unique nearest point in its closure, tree-level bound), *Beyond the Spectrum* I
  together with Book Ch. 1 (the algebraic part of `thm:dirichlet_blindness`), and *Functorial Bridge*
  (`prop:cov-nogo`). See "Zenodo papers" below and `FORMALIZACAO_ZENODO_2026-10-09.md`.

Nothing else in the monograph or in the papers is machine-checked. The plan for further statements is in
`PLANO_FORMALIZACAO.md`.

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

| Lean name | Statement formalized | Coverage | Axioms | Non-vacuity witness |
|---|---|---|---|---|
| `inv_Gamma_neg_nat` | `Γ(−n)⁻¹ = 0` (auxiliary: Mathlib's `Γ⁻¹` agrees with `1/Γ`) | auxiliary | std | no hypotheses (instance as `example`) |
| `stifel` | Prop. "Global Stifel Recurrence": `C(x−1,y) + C(x−1,y−1) = C(x,y)`, all `y ∈ ℂ`, `x ∉ {0,−1,−2,…}` | full | std | `stifel_nonvacuous` (x = 1) |
| `star_of_david` | Thm. "Continuous Star of David" (`thm:star_of_david`), eq. `sod_product` | full; holds for all `n, k ∈ ℂ`, which is stronger than the text | std | no hypotheses (instance as `example`) |
| `cbinom_zero_of_y_neg` | Prop. "Global Meromorphic Extension and Zero Loci", zeros for `y ∈ ℤ_{<0}` | full (zero part) | std | no hypotheses (instance as `example`) |
| `cbinom_zero_of_xy_neg` | same Prop., zeros for `x − y ∈ ℤ_{<0}` | full (zero part) | std | no hypotheses (instance as `example`) |
| `cbinom_real_pos` | same Prop., positivity for real `x > 0`, `0 ≤ y ≤ x` | full (positivity part) | std | `cbinom_real_pos_nonvacuous` (x = 1, y = 1/2) |
| `row_sum` | discrete identity `∑ C(n,k) = 2ⁿ` quoted in Ch. 3, a classical result already in Mathlib | full (classical) | std | no hypotheses (instance as `example`) |
| `multinomial_row_sum` | discrete identity `∑ multinomial = mⁿ` quoted in Ch. 3, classical | full (classical) | std | no hypotheses (instance as `example`) |

The same Proposition also asserts a meromorphic extension. That part is **not** formalized.

### `LeanReal/Chap12Constraint.lean` — Book, Ch. 12, Thm. "Pointwise Constraint Bounds" (`thm:minimax_hamiltonian_regularization`)

| Lean name | Statement formalized | Coverage | Axioms | Non-vacuity witness |
|---|---|---|---|---|
| `constraint_bounds` | items (i)–(ii) for principal curvatures `k₁,k₂,k₃` with `|kᵢ| ≤ κ`: `0 ≤ ∑kᵢ² ≤ 3κ²` and `s − 6κ² ≤ s + ∑kᵢ² − (∑kᵢ)² ≤ s + 2κ²`, where `s = 2Λ + 16πGρ` | **reduced form**: the diagonalization of `K_ij` and the Hamiltonian constraint are not part of this statement; they enter as the shape of `³R` | std | `constraint_bounds_nonvacuous` (k = (1/2, −1, 0), κ = 1) |
| `constraint_bounds_sharp` | both endpoints are attained by `(κ,κ,κ)` and `(κ,κ,−κ)` | reduced form | std | no hypotheses (instance as `example`) |

### `LeanReal/Chap12ConstraintMatrix.lean` — same theorem, pointwise matrix form; also SQG Thm. `thm:minimax_shear`

This file states the theorem at one point of a spacelike hypersurface, in an orthonormal frame of `γ`:
- `K` is a real symmetric 3×3 matrix;
- `frobSq K = K_ijK^ij`;
- `shear K = σ_ij`;
- `IIBound K κ` is `∀ v, |vᵀKv| ≤ κ vᵀv`. This is the text's definition of `‖II‖ ≤ κ*` (SQG eq. `minimax_bound_def`) at that point;
- `HamiltonianConstraint` is SQG eq. `wdw_constraint`, taken as a **hypothesis**.

| Lean name | Statement formalized | Coverage | Axioms | Non-vacuity witness |
|---|---|---|---|---|
| `frobSq_shear` | `σ_ijσ^ij = K_ijK^ij − K²/3` | full | std | no hypotheses |
| `hamiltonian_iff` | SQG form of the constraint ⟺ Book eq. `wdw_hamiltonian`: `³R + K² − K_ijK^ij = 2Λ + 16πGρ` | full | std | no hypotheses |
| `frobSq_eq_trace_mul` | `K_ijK^ij = tr(K²)` for symmetric `K` (auxiliary) | auxiliary | std | `abs_eigenvalue_le_nonvacuous` (`Kw` Hermitian) |
| `trace_mul_self_eq` | `tr(K²) = ∑ λᵢ²`, by Mathlib's spectral theorem | auxiliary | std | `abs_eigenvalue_le_nonvacuous` |
| `trace_eq_sum` | `tr K = ∑ λᵢ` (auxiliary) | auxiliary | std | `abs_eigenvalue_le_nonvacuous` |
| `abs_eigenvalue_le` | `IIBound K κ ⟹ |λᵢ| ≤ κ` | full | std | `abs_eigenvalue_le_nonvacuous` (`Kw`, κ = 1) |
| `IIBound_of_abs_eigenvalue_le` | `(∀ i, |λᵢ| ≤ κ) ⟹ IIBound K κ` (auxiliary) | auxiliary | std | `IIBound_of_abs_eigenvalue_le_nonvacuous` |
| `IIBound_iff` | `IIBound K κ ⟺ ∀ i, |λᵢ| ≤ κ` ("no further relation among the λᵢ") | full | std | `abs_eigenvalue_le_nonvacuous` |
| `IIBound_of_l2_opNorm_le` | Mathlib ℓ² operator norm `‖K‖ ≤ κ ⟹ IIBound K κ`; the converse is not proved | one direction | std | `IIBound_of_l2_opNorm_le_nonvacuous` (‖Kw‖ ≤ 1) |
| `constraint_bounds_matrix` | (i) `0 ≤ K_ijK^ij ≤ 3κ²`, `0 ≤ σσ ≤ 3κ² − K²/3`; (ii) `2Λ+16πGρ−6κ² ≤ ³R ≤ 2Λ+16πGρ+2κ²` | pointwise, orthonormal frame, constraint as hypothesis | std | `constraint_bounds_matrix_nonvacuous` (`Kw`, κ = 1, Λ = G = ρ = 1, ³R = 4 + 16π) |
| `constraint_bounds_opNorm` | same conclusion, hypothesis `‖K‖_op ≤ κ` | same | std | `constraint_bounds_opNorm_nonvacuous` (same data, ‖Kw‖ ≤ 1) |
| `constraint_bounds_vacuum` | case `ρ = 0` | same | std | `constraint_bounds_vacuum_nonvacuous` (`Kw`, κ = 1, Λ = 1, ³R = 4) |
| `IIBound_diagonal` | diagonal matrices with entries in `[−κ, κ]` satisfy `IIBound` (auxiliary) | auxiliary | std | `IIBound_diagonal_nonvacuous` (d = (1, −1, 1/2)) |
| `constraint_bounds_matrix_sharp` | sharpness: `diag(κ,κ,κ)` and `diag(κ,κ,−κ)` are admissible, attain `KK = 3κ²` and `σσ = 3κ² − K²/3`, and satisfy the constraint with `³R` at the lower and upper endpoint | algebraic, pointwise | std | `constraint_bounds_matrix_sharp_nonvacuous` (κ = 1) |

**Not formalized:**
- the Lorentzian manifold, the ADM foliation, and the derivation of the constraint from Einstein's equations (Gauss equation);
- a general frame `γ_ij ≠ δ_ij`;
- the minimax problem `κ* = inf_Σ ‖II_Σ‖_{L∞}`;
- the converse operator-norm inequality;
- that ρ is the energy density `T_μν nᵘnᵛ` and that `³R` is the scalar curvature of `γ`. In the Lean code both are free real numbers.

Sharpness is shown at the level of matrices at a point. It is not shown at the level of spacetimes.

## Zenodo papers (added 2026-10-09)

Each module quotes the paper's statement and location in its header and lists what it does not cover.
Non-vacuity witnesses are `example`s inside each module. Each mutant (`mutant_*`) is a mutated statement
whose negation is proved there, by an explicit counterexample.

### `LeanReal/Fermions.lean` — fermion-mass paper (10.5281/zenodo.22373916)

| Lean name | Statement formalized | Coverage | Axioms |
|---|---|---|---|
| `sum_v`, `sum_sq_v` | `∑ v_j = 3a`, `∑ v_j² = 3a² + 6b²` for `v_j = a + 2b cos(δ + 2πj/3)` | full | std |
| `norm_v1`, `norm_v2`, `v2_trace_zero` | `‖v_𝟏‖² = 3a²`, `‖v_𝟐‖² = 6b²`, `v_𝟐` trace-zero (Prop. `thm:koide_exact`) | full | std |
| `koide_ratio` | `Q = 1/3 + 2b²/(3a²)` (eq. `koide_general`) | full; any real `b, δ`, `a ≠ 0` | std |
| `koide_iff_equipartition`, `koide_iff_ratio`, `koide_iff_angle` | the three equivalences of eq. `norm_equipartition` | full; the angle is `arccos(⟨v,𝟏⟩/(‖v‖‖𝟏‖))` written out | std |
| `ckm_entries_of_commute` | Remark `rem:dft`: if `C_uC_d = C_dC_u` and unitaries diagonalize them with **distinct** eigenvalues, then each column of `V = U_u†U_d` has at most one non-zero entry, and every `|V_ij|` is 0 or 1 | the hypothesis of a non-degenerate spectrum is added; it is not in the remark | std |
| `ckm_circulant` | the modulus part |V_ij| ∈ {0,1}, for two circulant 3×3 sectors with non-degenerate spectra | as above | std |
| `mutant_koide_false`, `mutant_ckm_no_commute`, `mutant_ckm_degenerate` | negations of mutants: `2b² → b²`; drop commutation; drop non-degeneracy | negative controls | std |

### `LeanReal/YangMills.lean` — Yang–Mills paper (10.5281/zenodo.22301093)

| Lean name | Statement formalized | Coverage | Axioms |
|---|---|---|---|
| `gribov_convex`, `zero_mem_gribov` | Prop. `prop:gribov_region`(a): `Ω = {A : M₀ + L(A) > 0}` is convex, and `0 ∈ Ω` if `M₀ > 0` | abstract affine pencil, any real vector space; `M₀ > 0` is a hypothesis | std |
| `unique_nearest_of_closed_convex`, `gribov_closure_unique_nearest` | Prop. `prop:gribov_region`(d): every point has a unique nearest point in `Ω̄` (Federer's `reach = +∞`) | complete real inner-product space; Federer's reach itself is not in Mathlib | std |
| `tree_level_bound`, `tree_level_eq_iff`, `propagator_max` | Prop. `prop:amgm_tree`: `k² + λ⁴/k² ≥ 2λ²`, equality iff `k = λ`, and `D(k) = k²/(k⁴+λ⁴)` is maximal exactly at `k = λ` | algebraic; the GZ quadratic form is not derived | std |
| `mutant_gribov_nonaffine`, `mutant_tree_level` | negations: convexity for a non-affine pencil; constant `2 → 3` | negative controls | std |

The Yang–Mills mass gap is not touched. Items (b), (c), openness of `Ω` and `reach(Ω) = 0` are not formalized.

### `LeanReal/BeyondSpectrum1.lean` — *Beyond the Spectrum* I (10.5281/zenodo.22644743) and Book Ch. 1, `thm:dirichlet_blindness`

| Lean name | Statement formalized | Coverage | Axioms |
|---|---|---|---|
| `energy_eq_frob` | `∑(k₁²+k₂²)a² = ‖DA‖_F² + ‖AD‖_F²` | the Parseval step `𝓔(f_A) = ∑…` is **not** formalized; `energy` is defined as the sum | std |
| `energy_bounds`, `ratio_le` | `2‖A‖² ≤ 𝓔 ≤ 2n²‖A‖²`; `𝓔(P₂AP₂ᵀ) ≤ n²𝓔(P₁AP₁ᵀ)` | full (coefficient form) | std |
| `frobSq_perm`, `charpoly_perm`, `rank_perm` | permutation conjugation keeps `‖·‖_F`, characteristic polynomial, rank | full | std |
| `blindness_sharp` | `A = E₁₁` and the transposition `(1 n)` attain the ratio `n²` | full (coefficient form), every `n ≥ 1` | std |
| `mutant_ratio`, `mutant_energy_invariant` | negations: `n² → n² − 1`; energy invariant under conjugation | negative controls | std |

### `LeanReal/FunctorialBridge.lean` — *Functorial Bridge* (10.5281/zenodo.22441676), `prop:cov-nogo`

| Lean name | Statement formalized | Coverage | Axioms |
|---|---|---|---|
| `no_covariant_lapse` | `N(s) = α'(s)N(α(s))` for all `α` in a subclass of `Diff⁺([0,1])` ⟹ `N = 0` on `(0,1)` | constant paths, fixed `x`; the subclass only weakens the hypothesis | std |
| `no_covariant_lapse_continuous` | with continuity on `[0,1]`: `N ≡ 0` there | same | std |
| `alpha_isDiffPlus` | the paper's `α(s) = s + ½s(1−s)(s−s₀)` is admissible (`α' > 0` on `[0,1]`) | full | std |
| `mutant_no_jacobian` | negation: without the factor `α'` the conclusion fails (`N ≡ 1`) | negative control | std |

## Non-vacuity witnesses (`LeanReal/Witnesses.lean`)

For each theorem with hypotheses, a `…_nonvacuous` theorem proves that concrete data satisfy all its
hypotheses at once (last column of the tables above). Theorems without hypotheses cannot be vacuous; for
them an `example` applies the theorem to concrete data. The matrix witness is the non-diagonal symmetric
`Kw = [[0,1,0],[1,0,0],[0,0,1]]` (eigenvalues 1, −1, 1): `IIBound Kw 1`, Mathlib's ℓ² operator norm
`‖Kw‖ ≤ 1` (`Kw_opNorm_le`), `tr Kw = 1`, `K_ijK^ij = 3`, and the Hamiltonian constraint with
`Λ = G = ρ = 1`, `³R = 4 + 16π` (`Kw_hamiltonian`), which is the upper endpoint of item (ii).

## Negative controls (`mutants/`)

Each mutant restates one verified theorem with a single change and reuses the original proof. All 14 fail to
compile, and `#print axioms` shows `sorryAx` for each one. Full output: `mutants/mutantes_saida_formal_proofs_mathlib.txt`.

Failing to compile does not show that a statement is false. So `LeanReal/Falsified.lean` states each mutated
statement verbatim and proves its negation, `¬ (∀ …, mutated)`, by an explicit counterexample with concrete
numbers (`norm_num`, `simp`, `linarith`, `omega`; no `decide`, no `native_decide`). The counterexamples are
listed in that file's header. All 14 negations compile, and `#print axioms` gives std for each.

| file | mutation | failure | proved false by (`Falsified.lean`) |
|---|---|---|---|
| `M1_KK_3para2` | `KK ≤ 2κ²` | linarith | `m1_false` |
| `M2_shear_div3para2` | `σσ ≤ 3κ² − K²/2` | linarith | `m2_false` |
| `M3_inferior_6para5` | `³R ≥ s − 5κ²` | linarith | `m3_false` |
| `M4_superior_2para1` | `³R ≤ s + κ²` | linarith | `m4_false` |
| `M5_autovalor_meio` | `|λᵢ| ≤ κ/2` | type mismatch | `m5_false` |
| `M6_frobshear_div3para2` | `σσ = KK − K²/2` | unsolved goals | `m6_false` |
| `M7_traco_sem_quadrado` | `tr(K²) = ∑ λᵢ` | unsolved goals | `m7_false` |
| `M8_sharp_6para5` | `diag(κ,κ,κ)` with `³R = s − 5κ²` | unsolved goals | `m8_false` |
| `M9_M14_chap03_chap12reduced` (m9) | Stifel with `−` | unsolved goals | `m9_false` |
| (m10) | Star of David, `k+1 → k+2` on one side | rewrite fails | `m10_false` |
| (m11) | positivity with `y ≤ x + 3` | linarith | `m11_false` |
| (m12) | `∑ multinomial = mⁿ + 1` | type mismatch | `m12_false` |
| (m13) | reduced upper bound `s + κ²` | linarith | `m13_false` |
| (m14) | reduced `∑kᵢ² ≤ 2κ²` | linarith | `m14_false` |

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
./verificar.sh                                   # the nine modules in dependency order, then LeanReal.lean
ARQ=mutants/M1_KK_3para2.lean ./verificar.sh     # one file
```

Last full run: 2026-10-09. All nine modules and `LeanReal.lean` compiled with 0 errors and 0 warnings,
and all 98 `#print axioms` lines gave only propext, Classical.choice and Quot.sound (independent fidelity
review: `L2_FIDELIDADE_2026-10-09.md`). The GitHub Actions workflow repeats the build, the axiom scan and a
leanchecker kernel replay on every push. All 14 mutants failed with `sorryAx` (run of 2026-10-07), and all 14 mutated
statements are proved false in `Falsified.lean`.

Run of 2026-10-09 for the four Zenodo modules (`Fermions`, `YangMills`, `BeyondSpectrum1`,
`FunctorialBridge`), followed by `LeanReal.lean`: 0 errors, 0 warnings, and all 36 `#print axioms`
lines gave std.

## Round 2 (2026-10-09)

Fidelity review: `L2_FIDELIDADE_RODADA2.md`, with blind back-translation. F3 is faithful; the others are declared reductions. All 48 `#print axioms` lines show only the standard axioms. Every module has a non-vacuity witness and a mutant proved false.

| Module | Work and statement | Coverage |
|---|---|---|
| `FunctorialBridge2` | *Functorial Bridge*, `prop:nec`: `T_{μν}k^μk^ν = ‖k^μ∂_μΨ‖²_HS` for null `k` | pointwise linear algebra; the `∂_μΨ` are given matrices, with no manifold |
| `FunctorialBridge3` | *Functorial Bridge*, `prop:noid`: no idempotent cobordism | abstract argument; the additivity and positivity of the volume are hypotheses |
| `FermionsEuler` | fermion paper, eq. `euler` (alternating binomial sums) | full (combinatorics); says nothing about vacuum energy |
| `BeyondSpectrum2Iso` | *Beyond the Spectrum* II, `thm:isospectral_separation`(a): the 3×3 isospectral pair and its spectrum | spectrum only; persistence diagrams are not formalized |
| `Chap02Graphon` | Book ch. 2, the Dirichlet energy of the graph Laplacian: `⟨u, L_W u⟩ = ½∑W_ij(u_i−u_j)²` | finite graph, symmetric `W`; the `L^∞([0,1]²)` graphon case is not included |
| `BeyondSpectrum3_T1` | *Beyond the Spectrum* III, OBL-014: partial trace, `Tr Tr₂K = Tr K`, `Tr₂` preserves PSD, a rank bound | finite-dimensional analogue only |
| `BeyondSpectrum1_B2` | *Beyond the Spectrum* I, `prop:optimal_permutation` (rearrangement) | full for the reduced sum; it builds on `BeyondSpectrum1` |
| `BeyondSpectrum1_B4` | cut norm: the maximum of a bilinear form on `[0,1]ⁿ` is attained at vertices, with sharp constant 4 | finite matrices |
| `YangMills_Y5` | Yang–Mills `prop:tight_binding`: the range of `E(θ) = −2t cos θ`, and the finite circulant ring | the spectrum on `ℓ²(ℤ)` is not proved |

## Round 3 (2026-10-09)

Fidelity review: `L2_FIDELIDADE_RODADA3.md`, with blind back-translation. G2 is faithful; the others are declared reductions. Only the standard axioms appear.

| Module | Source and statement | Coverage |
|---|---|---|
| `Chap07BallBound` | Book ch. 7, `prop:ball_bound` for curves: a closed curve with `|f''| ≤ κ` inside a ball of radius `R` has `κR ≥ 1`; equality for the circle | twice-differentiable closed curves (`k = 1`), a subclass of the chapter's `C^{1,1}` immersions. The lemma "maximum ⇒ second derivative ≤ 0", which Mathlib lacks, is proved here |
| `Chap09MouthHalfturn` | Book ch. 9, `prop:mouth_halfturn`: `y(L) − y(0) ≥ 2ρ`, and also `a ≥ 2ρ`; equality for the semicircle | differentiable tangent angle in `[0, π]`; the chapter allows Lipschitz. The range hypothesis is shown necessary for the signed inequality (`mutant_no_range_false`); the teardrop counterexample for the width is not formalized |
| `YangMills_Y4` | Yang–Mills `lem:gz_convex`(b): `−log det` is convex and strictly convex on the PD cone; on a Galerkin pencil it is strict iff `L` is injective (with `M₀ ≻ 0`) | part (a) and the boundary limit are not included |
| `BeyondSpectrum3_T3` | *Beyond the Spectrum* III, Mellin transform of a vertex coordinate: Beta formula, holomorphy, residues, rational case | the Dirichlet aggregation is not included |
| `BeyondSpectrum2_G2` | *Beyond the Spectrum* II, QFI metric in an eigenbasis: SLD entries, QFI formula, reality, change of basis | full, for full-rank `ρ` (the paper's hypothesis) |

## Round 4 (2026-10-09)

Fidelity review: `L2_FIDELIDADE_RODADA4.md`, with blind back-translation. All four modules are
declared reductions; only the standard axioms appear.

| Module | Source and statement | Coverage |
|---|---|---|
| `BeyondSpectrum3_T2` | *Beyond the Spectrum* III, `thm:reflected_entropy_prop`: a von Neumann entropy API (defined here; Mathlib has none); the reflected entropy `S_R` of the canonical purification is non-negative and symmetric, and `S_R = I(11*:2)`; `S_R ≥ I(1:2)` | finite dimensions, any density matrix. `S_R ≥ I` is proved **conditionally on strong subadditivity** (Lieb–Ruskai), an explicit hypothesis that is not proved in Lean |
| `FunctorialBridge_R4` | Functorial Bridge, `def:pathcat` and `lem:category`: Moore paths with sitting instants form a category with strictly associative concatenation (a Mathlib `Category` instance), for every `C^n` including `C^∞` | data in a **normed** space `E`, with the conditions on a datum as an arbitrary pointwise predicate. The paper's Fréchet space of fields on `ℳ`, joint smoothness in `(x,t)`, and rank constant along the path are not modelled. The last one is recovered by one instance per rank |
| `YangMills_Y4a` | Yang–Mills `lem:gz_convex`(a): `M_N(A)` is symmetric and affine, and `Ω_N` is open, convex and contains `0` | an abstract integration-by-parts model (derivations and an integral killing derivatives). `0 ∈ Ω_N` assumes two torus facts as hypotheses. The model and both facts are proved only for the circle `T¹`. The Faddeev–Popov operator is not formalized |
| `BeyondSpectrum1_B3` | *Beyond the Spectrum* I, `thm:morse_matrix`, algebraic part: critical points of `xᵀAx` on the sphere are the unit eigenvectors; `2n` of them for distinct eigenvalues; the Hessian along great circles is non-degenerate with index `i − 1` | eigen-coordinates (`A = diag λ`) for the count and the index. No manifold Morse theory: the Morse polynomial (iii) and `χ(S^{n−1})` are not included |

Extra non-vacuity witnesses from the fidelity review (SSA in the smallest case; `0 ∈ Ω`, `2 ∉ Ω` on the circle) are in `LeanReal/L2_Rodada4_Extra.lean`.

## Round 5 (2026-10-09)

Fidelity review: `L2_FIDELIDADE_RODADA5.md`, with blind back-translation. Both modules are declared reductions; only the standard axioms appear. Extra mutant and witnesses: `LeanReal/L2_Rodada5_Extra.lean`.

| Module | Source and statement | Coverage |
|---|---|---|
| `BeyondSpectrum2_G3` | *Beyond the Spectrum* II, `prop:cocycle` ("Cocycles on 𝕋²") and the first claim of `rem:tau_not_topological`: the Pauli/Clifford trace identities, `tr G = −2Φ₀∇Φ₁·∇Φ₂` and `tr(σ₃G) = −2iΦ₀ dΦ₁∧dΦ₂` pointwise, the constant `1/(4π)`, the `S₃` antisymmetrisation `= 2F·(∂₁F×∂₂F)`, hence the forms of (a), (b), (c) and the vanishing of the antisymmetrised ungraded cochain | **algebraic part only**, on an arbitrary measure space with the gradients as free data. (a)–(c) are **conditional**: Connes' trace theorem (with `[𝓓,Φ] = iγ·∇Φ`) is assumed in the form `τ = (1/4π)∫ tr G`, and in (c) `deg F` is *defined* by `∫F·(∂₁F×∂₂F) = 4π deg`. The Dixmier trace, the torus, differentiation and Brouwer degree are not formalized. Witness: a one-point space (degrees `1` and `−1`), not a map `𝕋² → 𝕊²` |
| `Chap09Winding` | Book ch. 9, `prop:winding_total_curvature`: `∫|θ'| ≤ ∫|κ| + π` for a unit-speed curve avoiding `c`, the constant `π` is sharp (for every `C < π` the inequality fails), and the winding bound `2π|w| ≤ VK + π + |Δ₀|` | **`C²` curves** (the book states `C^{1,1}`); the `C¹` regularity of the argument lift is a named hypothesis. The winding bound is conditional on the identity `Δθ(γ) − Δθ(γ₀) = 2πw` from `thm:loop_bounding`(1); homotopy classes are not formalized. Witnesses: a straight line (`κ = 0`) and a full circle (`κ = 1`, `w = 1`) |

## Book batch B1 (2026-10-10)

Fidelity review: `L2_FIDELIDADE_LIVRO_B1.md`, with blind back-translation; only the standard axioms appear. Hypotheses that stand in for missing theory are explicit and named.

| Module | Source and statement | Coverage |
|---|---|---|
| `Chap08Pointwise` (8.2) | Book ch. 8, Theorem "Sectional-Extrinsic Coupling": `K_M(X,Y) = K̄ + κ²` for orthonormal `X, Y` on an umbilic hypersurface of a space form | **pointwise algebra**; the Gauss equation is a named hypothesis; constancy of `K_M` and the Codazzi part are not formalized. Witness `K̄ = 1`, `κ = 2` |
| `Chap08Pointwise` (8.7) | Book ch. 8, `prop:raychaudhuri`: `θ ≡ 0`, `ω = 0` on an open set ⇒ `R_{μν}V^μV^ν = −σσ ≤ 0`, strict where `σ ≠ 0` | along one curve, in the adapted orthonormal frame `V = e₀`; the Raychaudhuri equation is a named hypothesis; proved: `θ' = 0` from `θ ≡ 0` on an open set and `σσ ≥ 0`, `= 0 ⇔ σ = 0` for symmetric spatial `σ` |
| `Chap08Pointwise` (8.8) | Book ch. 8, `prop:rn_horizon`(2): `β(r₊) = 1`, `r₊` in the PG chart, `θ_l = 2(1−β)/r`, so the RN horizon is a MOTS | **algebraic core of (2)**; the components of `K` (`K^θ_θ = K^φ_φ = β/r`, `K_ss = K^r_r`) and `D_is^i = 2/r` are data; `K^r_r` is arbitrary (it cancels, so the book's `K^r_r = β'` is implied). Item (1) (flat slices, curvatures `1/r₊`) and `K_ij = D_(iβ_j)` are not formalized |
| `Chap08Pointwise` (8.10) | Book ch. 8, `prop:wormhole_throat`(2)–(3): principal curvatures vanish at the throat; `ρ + p_r = −(1−b')/(8πG r₀²) < 0`; if `b' ≥ 0` (⇔ `ρ ≥ 0`), `ρ + p_r ≥ −K_Gauss/(8πG)` with equality iff `b' = 0` | **pointwise at `r₀`**; the Einstein-tensor components `8πGρ`, `8πGp_r` are named hypotheses; the curvature formula `√(1−b/r)/r` is evaluated, not derived; `K_Gauss = 1/r₀²` is a definition; item (1) not formalized |
| `Chap08Pointwise` (8.11) | Book ch. 8, `prop:proper_accel`: `g(u,u) = −1`, `g(a,u) = 0` ⇒ `a` spacelike or zero, and `II(u,u) = a` | **linear algebra in Minkowski `ℝ^{1,3}` at one point**; `g(a,u) = 0` is assumed (not derived from a curve); `‖II_γ‖_op = |a|_g` not formalized |

## Book batch B2 (2026-10-10)

Fidelity review: `L2_FIDELIDADE_LIVRO_B2.md`, with blind back-translation; only the standard axioms appear. Hypotheses that stand in for missing theory are explicit and named.

| Module | Source and statement | Coverage |
|---|---|---|
| `Chap08UTurn` (8.3 = 7.5(3)) | Book ch. 8, `lem:euclidean_uturn`, and ch. 7, `thm:lower_bounds`(3): a U-turn in the strip `ℝ × [0,w]` starting in direction `(1,0)` with `\|κ\| ≤ k` has `k ≥ 2/w`; equality for the semicircle of diameter `w` | differentiable tangent angle with `\|θ'\| ≤ k` at every point; the book's `C^{1,1}` (Lipschitz, a.e. bound) case is not covered. No range condition on `θ`: the selection step (`exists_halfturn_window`) is proved, then the rotated `mouth_halfturn`. Witness: semicircle (equality); L2 witness with `θ` leaving `[0, π]` |
| `Chap08UTurn` (9.9) | Book ch. 9, `prop:balloon_height`: an admissible curve whose tangent turns from `(1,0)` to `(−1,0)` has two points with `\|Δy\| ≥ 2ρ`; a mouth U-turn in `D_R` forces `R ≥ ρ` | same reduction; the mouth condition `γ(0), γ(L) ∈ W_a` is not needed (statement generalizes). Witness: half circle of radius `ρ` in `D_ρ` (equality) |
| `Chap09SubloopCorridor` (9.2) | Book ch. 9, `prop:subloop`: a closed sub-loop with `\|κ\| ≤ K` has width `≥ 2/K` in some direction, diameter `≥ 2/K`, and `‖κ‖_∞ ≥ 2/diam Ω` | same reduction; width read as the component of a chord along a unit direction (implies the set width); `K > 0` needed only for the diameter form. The "range ≥ π" step is proved without integrals. Witness: unit circle (equality) |
| `Chap09SubloopCorridor` (9.6) | Book ch. 9, `prop:corridor_gap`: in `Ω_H = {\|y\| ≤ H} \ B_1(0)`, every path that reverses direction has `‖κ‖_∞ ≥ 1/H`; the value is attained | lower bound: same reduction (the obstacle is not used). Attainment: **only the arcs** (semicircles of radius `H` centred at `(−c,0)`, `c > H+1`, and at the origin; full circle for `w ≥ 2`) lie in `Ω_H` with curvature `1/H`; entry/exit segments and gluing, homotopy classes `w`, embedding and the length bound `V` are not formalized. Benchmark `H = 1.62` |

## Book batch A1 (2026-10-10)

Fidelity review: `L2_FIDELIDADE_LIVRO_A1.md`, with blind back-translation; only the standard axioms appear. Hypotheses that stand in for missing theory are explicit and named.

| Module | Source and statement | Coverage |
|---|---|---|
| `Chap01KacRice` | Book ch. 1, `thm:kac_rice_tensors` (i) and (iv): `∑_{i∈[n]^d}∏ x_{i_a}y_{i_a} = (x·y)^d`, hence covariance `(x·y)^d` for iid entries; for the symmetric model with common variance, `Var f(e₁) = 1` and `Var f((e₁+e₂)/√2) = 2^{-d}C(2d,d)` (`3/2`, `5/2` for `d = 2, 3`), and non-isotropy for every `d ≥ 2` | **algebraic core**. Gaussianity and independence are replaced by the named hypothesis `hcov : C = δ`. The variance formula `∑ mult(𝐦)² x^{2𝐦}` is taken as the definition `varSym`, restricted to `span(e₁,e₂)`. Not formalized: (ii), (iii) and the Cartwright–Sturmfels bound. Witnesses: `x = (1,2)`, `y = (3,−1)`, `d = 3` |
| `Chap04Modulational` | Book ch. 4, Theorem "Simplicial Modulational Instability": `ħ²Ω² = ε(ε−2c)` (`ε = ħ²σ/2M`, `c = κpρ₀^p`), instability `Ω² < 0 ⟺ 0 < σ < 4Mc/ħ²`, minimum `−c²` exactly at `ε = c`, growth rate `\|Im Ω\| ≤ c/ħ`, attained | **after linearization**: the 2×2 system `ħu_t = εv`, `ħv_t = −(ε−2c)u` is data, not derived from the NLSE. The book's criterion omits `k ≠ 0` (`σ(0) = 0` gives `Ω = 0`); the printed form is proved false (`mutant_book_criterion_false`). Witness `ħ = M = κ = p = ρ₀ = 1`, `σ = 2` (maximal rate) |
| `Chap05Barycentric` | Book ch. 5, `thm:barycentric_ratio`: `dist(Φ_α c₁, Φ_α c₂) ≤ α/(α+m)·dist(c₁,c₂)`, equality without sign change in the fibres (in particular `π` injective), `α/(α+m) ≤ 1 − m/α + m²/α²`, no lower bound (the book's `4 → 2` example); and Prop. "Inversion": `P P⁺ = I`, `P⁺P` an orthogonal projection, `h(x) = g_θ(P x)` for `x ∈ ran P⁺`, and `f̂ = ĥ/K̂` | **full** for the Lipschitz theorem, stronger than the text (all `c ∈ ℝ^m`, `α ≥ 0`, `π` not required surjective). Inversion: **finite-dimensional algebra**; the Fourier/convolution theorem is not formalized, and `K̂_α ≠ 0` enters as the explicit hypothesis `hK`, as in the book. Whether it holds for the Beta kernel is open: no zero found numerically for `m = 2`, uncertified. Witnesses: `m = 3 → 2`, `α = 1`; `P = (1 1)` |
| `Chap06Kigami` | Book ch. 6, `assump:kigami_decimation`: the trace of the level-one network `Γ₁` on the corners is `K_{m+1}` with conductance `(m+1)/(m+3)`, harmonic extension `a = 2/(m+3)`, `b = a/2`, and `r_m = m+3` | **exact computation for `m = 2, 3`**: the Schur complement of the Laplacian of `Γ₁` is built from the book's rule and equals `(3/5)L_{K₃}` and `(2/3)L_{K₄}`. For general `m`, only the symmetry-reduced equations are formalized (`a = 2/(m+3)`, `b = a/2`, `r_m = m+3`); the symmetry and uniqueness of the harmonic extension are not |
| `L2_LIVRO_A1_Extra` | L2 extras for book chs. 4–5 | ch. 4: the corrected criterion for `σ ≥ 0` (`Ω² < 0 ⟺ σ ≠ 0 ∧ σ < 4Mc/ħ²`), with the printed criterion false even on `σ ≥ 0`; a stable-side witness; ch. 5: a `deconvolution` witness with `K̂ = (2, i)` |

## Book batch B3 (2026-10-10)

Fidelity review: `L2_FIDELIDADE_LIVRO_B3.md`, with blind back-translation; only the standard axioms appear. Hypotheses that stand in for missing theory are explicit and named.

| Module | Source and statement | Coverage |
|---|---|---|
| `Chap12Spectral` (12.1) | Book ch. 12, `thm:running_spectral_dimension`: `d_s = m/α` for every `τ > 0`, `d_s(1,4) = 4`, `d_s(2,4) = 2` | **declared reduction:** the heat-kernel diagonal is *defined* by the Fourier formula of the proof, `P(τ) = (2π)^{-m}∫exp(-τ‖k‖^{2α})dk`; that this is the diagonal of the kernel of `∂_τu + (-Δ)^α u = 0` is not formalized (no Fourier-multiplier theory). Scaling law, `0 < P(1) < ∞` and the log-derivative are proved; `m ≥ 1`. Witness: `P(2) ≠ P(1)` |
| `Chap12Spectral` (12.2) | Book ch. 12, `thm:cartan_metric_emergence`: Gram matrix of `e_j − e_{j+1}` is `CartanMatrix.A`, `∑v_i² = cᵀAc`; zero linear term and Hessian `f''(b)∑v_i²` along `t* + sv` when `∑v_i = 0` | algebraic and calculus core for a generic `f` with given derivatives; `f = log Γ(·+1)`, `f'' = ψ'`, the asymptotics of `ψ'` and the `O(\|v\|³)` remainder are not formalized |
| `Chap12Spectral` (12.6) | Book ch. 12, `thm:neckpinch_condensation`: `0 ≤ W ≤ W_0e^{−2ct}` on `B`, and `W(t) ≤ δ` for a.e. `p ∈ B`, `t ∈ [t_δ, T]` | pointwise linear ODE with `κ` given data, **continuous in `t`** (Ollivier curvature not defined); `B`, `W_0` measurable; positive measure and `t_δ ≤ T` not needed. The "for every `p`" version is proved false |
| `Chap13Numbers` (r2) | Book ch. 13, `eq:ds_tau` (= ch. 12 `eq:analytical_ds_formula`): `d_s(τ) = 1 − τ/2ℓ² + [1 − (√(πτ)/2ℓ)e^{τ/4ℓ²}erfc(√τ/2ℓ)]^{-1}` for the closed form of `P` | `erfc` defined by the standard integral (Mathlib has none); ODE of `√π z e^{z²}erfc z` proved; remaining hypothesis: bracket `≠ 0` (always true by Mills' inequality, not proved; checked at `z = 1/8`). **Not covered:** closed form = heat-kernel integral (`eq:heat_kernel_exact`), limits `d_s → 2, 4` |
| `Chap13Numbers` (r4, numbers) | Book ch. 13 (and ch. 12 §experimental): `eq:tensor_running`; `H_inf < 4.71×10¹³` GeV from `r < 0.036`; `\|α_t\| < 1.5×10⁻¹¹` (`M_P`), `< 3.75×10⁻¹⁰` (`M_red`), `< 0.014` (`M_* ≥ 4.1×10¹⁴` GeV); `ℓ_* < 4.82×10⁻³¹` m; rescaled delays; `⁸⁷Sr` ratio | arithmetic with CODATA 2018 inputs; delays `D_2(z)` taken as data. The book's literal "`≤ 4.7×10¹³`", "`3.7×10⁻¹⁰`" and "`< 4.8×10⁻³¹` m" are proved **not** to follow (rounding of upper bounds downward) |
| `L2_LIVRO_B3_Extra` | L2 mutants for ch. 13 | the literal bounds `H_inf ≤ 4.7×10¹³` and `\|α_t\|(M_red) ≤ 3.7×10⁻¹⁰` fail at `H = 4.702×10¹³` GeV with `r ≈ 0.03597 < 0.036` |

## Book batch B4 (2026-10-10)

Fidelity review: `L2_FIDELIDADE_LIVRO_B4.md`, with blind back-translation; only the standard axioms appear. Hypotheses that stand in for missing theory are explicit and named.

| Module | Source and statement | Coverage |
|---|---|---|
| `Chap07Bounds` (7.14) | Book ch. 7, `prop:gauss_bonnet_floor`: `κ ≥ √(2πχ/A)` (χ > 0), `κ ≥ √(π\|χ\|/A)` (χ < 0), `√(2π\|χ\|/A)` in codimension one; pointwise `\|II(e₁,e₂)\| ≤ κ`, `−2κ² ≤ K ≤ κ²`, `K ≥ −κ²` for `N = ℝ` | pointwise Gauss-equation algebra complete (any normal space `N`; `‖II‖` = operator norm `sup_{\|v\|=1}\|II(v,v)\|`). Integral step **conditional on Gauss–Bonnet** (hypothesis `hGB : ∫K = 2πχ`) with the surface modelled as a finite measure space carrying frame data; that the data come from a closed `C²` surface is not formalized. Equality and strict witnesses; `−2κ²` sharp (complex curve) |
| `Chap07Bounds` (7.13) | Book ch. 7, `thm:scaling_law`: diagonal circle (unit speed, curvature `1/(√m R₀)`, `\|P_jγ\| = R₀`, `\|γ\| = √m R₀`, `γ'' = −ω²γ`); lower bound `\|γ''(s)\| ≥ 1/(√m R₀)` with the book's equality iff | complete at one `s`, "`C²`" weakened to "twice differentiable at `s`"; projected curvature `(x'y''−y'x'')/\|v\|³`. Planarity of the circle is by definition, not stated as a theorem |
| `Chap07Bounds` (7.12) | Book ch. 7, `thm:monotonicity`: `κ*_{n+1}(Ω×(−d,d), i(Σ), V) ≤ κ*_n(Ω, Σ, V)` | **curves only (`k = 1`)**, class = unit-speed curves twice differentiable on `[0,ℓ]` with bounded `γ''`, `Σ = {p,q}`; `Ω̄` replaced by a set `K`, cylinder `K×[−d,d]` (closure identity not proved); non-empty class assumed (book: `inf ∅ = +∞`). Also abstract form for any linear isometry |
| `Chap07Bounds` (7.1) | Book ch. 7, `prop:knot_gap`: `κ*_K(L) ≥ 4π/L = κ*_Imm(L) + 2π/L` | **conditional:** Fenchel (`hFen`, total curvature `≥ 2π` for every closed curve) is a hypothesis **not discharged in Lean**; Fáry–Milnor (`hFM`, `> 4π`) is a hypothesis for an abstract predicate `IsK`, which must encode "embedded, of non-trivial knot type K in ℝ³" (the curve class has no injectivity). Class: twice-differentiable closed curves (`γ, γ'` periodic), a strict subclass of `C^{1,1}`, so the lower bound is weaker than the book's. Proved: `∫\|κ\| ≤ ℓ‖κ‖_∞`, per-curve bounds, `κ*_Imm = 2π/L` attained by the circle. Regular-homotopy sentence not formalized |
| `Chap07Bounds` (table) | Book ch. 7, `tab:universal_classification` and "Calibration does not force isotropy": product torus `‖II‖_op = √m/R`; complex curve `\|II(v,v)\| = \|a\|`, `‖II‖_F = 2\|a\|` | torus: the book's formula `II(v,v)_j = v_j²/r` taken as definition (derivation from the immersion not formalized); complex curve: from the book's frame data; isotropy `‖II‖_op = ‖II‖_F/√2` proved false |
| `L2_LIVRO_B4_Extra` | L2 witnesses for ch. 7 | strict witnesses where the hypotheses bite (Gauss–Bonnet χ = 2 anisotropic, codimension-two saddle χ = −1; several planes `v = (1,0)`; Fenchel double circle); `hFM` proved for a concrete non-knot predicate with non-empty class (shows satisfiability, not Fáry–Milnor); `hFM` without `IsK` proved false |

## Book batch B5 (2026-10-10)

Fidelity review: `L2_FIDELIDADE_LIVRO_B5.md`, with blind back-translation; only the standard axioms appear. Hypotheses that stand in for missing theory are explicit and named.

| Module | Source and statement | Coverage |
|---|---|---|
| `Chap09Covering` (9.5) | Book ch. 9, `thm:unfolding`: every lift to a simply connected cover of an irreducible path (no sub-loop null-homotopic rel endpoints) is injective, hence a closed embedding; book form via `IsCoveringMap.liftPath` | **generalizes** the book: any continuous `p` from a simply connected `E`, any continuous path (immersion not needed); Hausdorff of `E` assumed (discharged from Hausdorff base in `L2_LIVRO_B5_Extra`). Converse for coverings proved. Witness: one and a half turns on `ℝ/ℤ` (irreducible, not injective, lift is an embedding) |
| `Chap09Covering` (9.1) | Book ch. 9, `prop:holonomy`, groupoid version: a functor from the fundamental groupoid of a path-connected space, injective on the vertex group at `x₀`, separates homotopy classes rel endpoints | **categorical core only**: flat connections, path-ordered exponential, `SU(2)`, `π₁ ≅ F_m` and the existence of a faithful `ρ` are not formalized; injectivity of `ρ` is the hypothesis `hinj`. Witness: monodromy of `ℝ → ℝ/ℤ` (`hinj` proved, non-trivial vertex group) |
| `Chap08Chronology` (8.13, 12.4) | Book ch. 8, `prop:causal_constraints` (1)–(2), and ch. 12, `thm:jordan_chronology`: timelike curves lie in `J⁺(p) ∩ J⁻(q)`, interior in `I⁺(p) ∩ I⁻(q)`, injective under chronology; no causal curve from `𝓑` to its complement, `κ*_wl = +∞` | **order-theoretic skeleton**: abstract relations `I ⊆ J`, `J` reflexive and transitive, chronology as irreflexivity of `I`; curves encoded by their order property. Lorentzian geometry, strong causality ⇒ chronology, and item (3) not formalized. Witness: Minkowski `ℝ^{1,1}` |
| `Chap08Chronology` (7.2) | Book ch. 7, `prop:dubins_duality`: `κ*(L) = inf{κ > 0 : d_κ ≤ L}`; for `κ > κ*(L)` the Dubins path is admissible | **ordinal reduction**: abstract class with `len`, `peak`; Dubins' existence theorem is the hypothesis `hDubins` (shown necessary by a proved mutant). CSC/CCC structure and the values `0, ±κ` not formalized. Witness: semicircle toy class |
| `L2_LIVRO_B5_Extra` | L2 complements for ch. 7, 8, 9 | a covering of a Hausdorff space is Hausdorff, so `thm:unfolding` needs Hausdorff only on the base; Dubins duality without the hypothesis "some curve has length ≤ L" (both sets empty otherwise); `κ*_wl = +∞` over the book's timelike class |

## Book batch A2 (2026-10-10)

Fidelity review: `L2_FIDELIDADE_LIVRO_A2.md`, with blind back-translation; only the standard axioms appear. Hypotheses that stand in for missing theory are explicit and named.

| Module | Source and statement | Coverage |
|---|---|---|
| `Chap01Rayleigh` | Book ch. 1, Prop. "Spectral and Critical Correspondence" (i): for symmetric real `A` (n ≥ 1), `min_{S^{n−1}} xᵀAx` and `max_{S^{n−1}} xᵀAx` exist and equal the least and greatest elements of `spectrum ℝ A` | **full** for (i), finite-dimensional; the ordering `λ₁ ≤ … ≤ λ_n` is replaced by min/max of the spectrum. (ii) is in `BeyondSpectrum1_B3`. Witness `[[2,1],[1,2]]` (values 1 and 3 attained); symmetry is necessary (`[[0,1],[0,0]]`) |
| `Chap03Analysis` | Book ch. 3: Thm. "Alternating Row Integrals" (`∫₀^{2k+1} cos(πy)C(2k+1,y)dy = 0`); Prop. "Global Meromorphic Extension", reflection formula `C(x,y) = −(1/π)·sin(πy)sin(π(x−y))/sin(πx)·Γ(y−x)Γ(−y)/Γ(−x)`; `cor:row_log_product` (`E(x) = x(x+1) − x ln 2π − x lnΓ(x+1) + 2 ln G(x+1)`, x ≥ 0) | alternating integral: **full**. Reflection: **literal identity for x, y, x−y ∉ ℤ**; the meromorphic extension and removable singularities are not formalized. Row entropy: the reduction `E(x) = x lnΓ(x+1) − 2∫₀ˣ lnΓ(y+1)dy` is unconditional; the Barnes form is **conditional** on the Alexeiewsky identity (DLMF 5.17.4) as the named hypothesis `hAlex`, which is equivalent to the conclusion. Barnes' G is not in Mathlib; the witness `Gw` is built to satisfy `hAlex` and is not proved to be Barnes' G |
| `Chap04Symbol` | Book ch. 3 `thm:laplacian_symbol` and ch. 4 `thm:dispersion`: `Δe_k = −σ(k)e_k`, σ even, `σ = α⁻²(1 − Re∫e^{−ik·y}) ∈ [0, 2/α²]`, `|σ − (1/2α²)kᵀM₂k| ≤ (5/96)α⁻²∫(k·y)⁴` when `\|k·y\| ≤ 1`, `M₂ = a·Id + b·11ᵀ` with `a = ½∫(y_i−y_j)² ≥ 0`; lattice limit `S²/(2m²) + (Q − S²/m)/(2mα)`, equal to `(1/2mα)kᵀ(I+11ᵀ)k` only when `S = 0` | **reduction to an abstract probability measure μ** in place of the Beta kernel. Permutation invariance enters as the named hypothesis `hperm` (S_{m−1}, m ≥ 3), not proved for the Beta kernel. The O(\|k\|⁴) is in quantitative form only; "entire in k" is not formalized. a > 0 is in `L2_LIVRO_A2_Extra`. Witnesses δ_{(1,0)} (bound 2/α² attained) and `mu3` (a = b = 1/3) |
| `L2_LIVRO_A2_Extra` | L2 extras for book chs. 3–4 | `M2_a_pos`: `a > 0` (ch. 3, `thm:laplacian_symbol`) for permutation-invariant μ not a.s. concentrated on `y_i = y_j`, with witness `mu3` and a proved-false mutant without that condition (δ_{(1,1)}); `row_log_product_iff`: `hAlex` at x ⟺ the corollary's conclusion, so the Barnes content is exactly the cited classical theorem |

## Book batch B6 (2026-10-10)

Fidelity review: `L2_FIDELIDADE_LIVRO_B6.md`, with blind back-translation; only the standard axioms appear. Hypotheses that stand in for missing theory are explicit and named.

| Module | Source and statement | Coverage |
|---|---|---|
| `Chap08SpaceForms` (8.4) | Book ch. 8, `prop:space_form_uturn`: a U-turn in the tube `\|y\| ≤ w/2` of `ℍ²(-c²)` (resp. `𝕊²(+c²)`, `w < π/c`) with `\|κ\| ≤ k` has `k ≥ c coth(cw/2)` (resp. `c cot(cw/2)`); `G ≡ 1` gives `2 ≤ kw`; general warped tubes give `G(a)+G(b) ≤ k∫_a^b G` | **Fermi-coordinate reduction**: the curve enters only through `(y, θ, u, κ)` with classical derivatives on `(0,L)`; the Clairaut/Killing identity `eq:clairaut` is the explicit hypothesis `hClairaut` (classical, shown necessary by a proved mutant). Riemannian geometry, Fermi coordinates and the `C^{1,1}` a.e. case not formalized. Witnesses: the geodesic semicircle in Fermi form (equality) and in a wider tube (strict, `L2_LIVRO_B6_Extra`) |
| `Chap09Teardrop` (9.7) | Book ch. 9, `prop:teardrop`: (i) the three-arc teardrop `γ_a` starts at `(0,-a/2)`, ends at `(0,a/2)` with reversed tangent, lies in `x ≥ 0` touching `x = 0` only at its ends, is embedded, and `max\|γ_a\| = r*(a) = ρ(1+2 sin β(a))`; (ii) every right–left–right three-arc curve in `F_a` has `max\|γ\| ≥ r*(a)`, with equality only for `γ_a` | (i) for `a ∈ (0,2ρ)` only (`a = 2ρ` not covered); embedded = each arc injective and arcs meet only at junctions (the glued `C^{1,1}` curve is not built as one function). (ii) right–left–right pattern only; the mirror pattern is not formalized. Equality case proved under a hypothesis on the middle arc alone. Witnesses: `γ_a ∈ F_a` (equality) and a non-teardrop member of `F_1` (strict, `L2_LIVRO_B6_Extra`) |
| `Chap09Teardrop` (9.10) | Book ch. 9, `prop:teardrop_lower` and the remark after it: `R ≥ ρ + √(ρ² - a²/4)`; for `a ∈ (0,2ρ)`, `ρ + √(ρ² - a²/4) < r*(a)`, with the four limits | **conditional, final step only**: Ahn–Cheong–Matoušek–Vigneron Lemma 2, the Jordan curve theorem and the region argument enter as the hypothesis `hΔ : Δ ⊆ K ∪ D_R` (no curve appears in the Lean statement); the chord argument and the far point `f` are proved. The comparison with `r*(a)` and the limits are unconditional. Witnesses: the oblique arc (equality) and an off-centre `K` with `r_K < a/2` (strict, `L2_LIVRO_B6_Extra`) |
| `L2_LIVRO_B6_Extra` | L2 complements for ch. 8 and 9 (batch B6) | strict-inequality witnesses for the `ℍ²` and `𝕊²` U-turn bounds (semicircle in a wider tube) and for `F_a` (a three-arc curve other than `γ_a`); a witness for the `G ≡ 1` case; an off-centre witness for `hΔ` (Cauchy–Schwarz) with `R` strictly above the bound |

## Book batch B7 (2026-10-10)

Fidelity review: `L2_FIDELIDADE_LIVRO_B7.md`, with blind back-translation; only the standard axioms appear. Hypotheses that stand in for missing theory are explicit and named.

| Module | Source and statement | Coverage |
|---|---|---|
| `Chap11MinCut` (11.4) | Book ch. 11, `prop:mincut`: for a normalized pure state whose coefficient matrix factors as `UV` through an index of size `χ^{\|C\|}`, `S_A ≤ \|C\| log χ`; over a finite family of such factorizations, `S_A ≤ log χ · min_C \|C\|` | **linear-algebra half only**: the tensor network, its graph and the contraction across a cut are not modelled; the factorization `coef v = U V` that the contraction produces enters as a hypothesis, and the cut size is a bare natural number tied to it only through that hypothesis. Lean proves `S_A ≤ log` (inner dimension), i.e. entropy ≤ log Schmidt rank; the minimum over cuts is immediate. Witnesses: Bell state (equality) and a Schmidt-rank-2 state in `ℂ³⊗ℂ³` with a nontrivial factorization beating the trivial `log 3` bound (`L2_LIVRO_B7_Extra`) |
| `Chap11Fisher` (11.1, 11.2) | Book ch. 11, `prop:relative_entropy_hessian` and `thm:first_law_entanglement`: `d/dλ S(ρ(λ)‖ρ₀)\|₀ = 0`, `d²/dλ² = g^BKM(X,X)`; `δS = Tr(δρ H_σ)` | **commuting case only**: `ρ₀ = diag p` (full rank), `X = δρ = diag x` in the same basis, `Tr X = 0`; there the Hessian is `∑ x_i²/p_i`, which equals both `g^BKM` and `g^SLD`, so the BKM/SLD distinction is not tested. The non-commuting case (Fréchet derivative of the matrix logarithm) is not formalized |
| `Chap11Fisher` (`rem:sld_vs_bkm`) | Book ch. 11, `rem:sld_vs_bkm`: `g^BKM(X,X) ≥ g^SLD(X,X)` with equality iff `[ρ₀,X] = 0` | full for full-rank `ρ₀` in its eigenbasis, both metrics given by their eigenbasis formulas; `g^SLD` is tied to `½Tr(ρ{L,L})` via `BeyondSpectrum2_G2` (the integral form of `g^BKM` is not). Proves that "both reduce to `∑ X_ii²/p_i`" fails for degenerate `ρ₀` outside a joint eigenbasis; the correct common value `∑_{ij}\|X_ij\|²/p_i = Tr(ρ₀⁻¹X²)` is in `L2_LIVRO_B7_Extra`. Unbounded ratio and the numerical statistics not formalized |
| `L2_LIVRO_B7_Extra` | L2 complements for ch. 11 (batch B7) | a Schmidt-rank-2 witness for `mincut_bound` with a nontrivial factorization and a proof that it admits no rank-1 factorization; the basis-free value `Tr(ρ₀⁻¹X²)` of `g^BKM = g^SLD` in the commuting case and its gap from `∑ X_ii²/p_i` in the degenerate example |

## Book batch A3 (2026-10-10)

Fidelity review: `L2_FIDELIDADE_LIVRO_A3.md`, with blind back-translation; only the standard axioms appear. Hypotheses that stand in for missing theory are explicit and named.

| Module | Source and statement | Coverage |
|---|---|---|
| `Chap04SelfAdjoint` | 12 | sim |
| `Chap05Coupled` | 7 | sim |
| `Chap02Tangent` | 20 | sim |
| `Chap02Toda` | 14 | sim |
| `Chap01Tensor` | 11 | sim |
| `L2_LIVRO_A3_Extra` | 4 | sim |
| `Chap04SelfAdjoint` | Book ch. 4, Prop. "Self-Adjointness and Positivity": `−Δ` (`eq:simplicial_laplacian_def`) is linear, symmetric and `⟨u, −Δu⟩ = (2α²I)⁻¹∫∫K(y)\|u(x+y) − u(x)\|² ≥ 0` | **reduction to a finite abelian group `G`** (e.g. `(ZMod N)^{m−1}`) with sums, an arbitrary real kernel `K` and constant `c` in place of `ℝ^{m−1}`, the Beta kernel and `(2α²I)⁻¹`. Linearity, symmetry and the identity hold for every real `K`, `c`; `≥ 0` for `K, c ≥ 0`. Strict positivity on `L²(ℝ^{m−1})` (Plancherel) and `−Δ ≤ 2/α²` not covered; on finite `G` constants are in the kernel (proved). Witness on `ZMod 4` with complex `u` (form = 1) |
| `Chap05Coupled` | Book ch. 5, Prop. "Conservation of Total Mass and Energy Dissipation; formal computation" for `eq:coupled_system`: `∫u + ∫v + ∫w` constant for `t ≥ 0`; `dℰ/dt = −‖∇u‖² − ‖∇_Γv‖² − ‖∂_zw‖² − λ‖Ru − v‖² − κ‖Sv − w‖² ≤ 0` | **abstract real inner-product spaces and linear maps**, `∫u = ⟨u, 𝟙⟩`. Neumann (`⟨Lx, 𝟙⟩ = 0`), Green (`⟨x, Lx⟩ = −‖Gx‖²`), the exact adjoint relations and `R𝟙 = 𝟙`, `S𝟙 = 𝟙` (from `eq:interface_condition`) enter as named hypotheses, each a statement of the book about one operator; the flux cancellation, the dissipation formula and the integration in time are proved. Trace/extension operators, Green's formula, existence and regularity not covered. Witnesses: explicit scalar solution and a two-cell Neumann Laplacian; mutants show `R𝟙 = 𝟙` and `λ ≥ 0` are needed |
| `Chap02Tangent` | Book ch. 2, `thm:tt_tangent_proj`(iii), `thm:rank_preservation`(ii) and its example `A(t) = (1 − t)E₁₁`: along `T' = −P∇L(T)` with `P² = P = P*`, `d/dt L(T) = −‖P∇L‖² ≤ 0`; and `prop:tangent_proj_mr`: `P(Z) = UUᵀZ + ZVVᵀ − UUᵀZVVᵀ = Z − (I − UUᵀ)Z(I − VVᵀ)` is idempotent, Frobenius self-adjoint, fixes `UMVᵀ + U_pVᵀ + UV_pᵀ`, has range of that form, and the parametrization is injective | flow part **abstract** (inner-product space, projector family as hypotheses; the manifold, rank preservation (i) and (iii) not covered); the example is formalized in full for `m × n` matrices (`T* = 1`, rank 1 then 0). Projector part: **full matrix algebra** of the sketch; the manifold structure of `M_r`, the identification with `T_A M_r` and the dimension `r(m+n−r)` (cited to Vandereycken) not covered. Witnesses `ℂ ≅ ℝ²` and `3 × 3`, `r = 1` |
| `Chap02Toda` | Book ch. 2, `thm:toda_qr`: decomposition `𝔰𝔬(n) ⊕ 𝔟` with `Π_so(X) = X_{<0} − X_{<0}ᵀ`; isospectrality; `Q' = QK`, `K` skew, `Q(0) = I` ⇒ `QQᵀ = I`; `B = QᵀA₀Q` solves `B' = BK − KB`; `e^{A₀} = QR` ⇒ `e^{QᵀA₀Q} = RQ` | **algebraic and pointwise-derivative steps only** (entrywise derivatives). Existence, uniqueness and global existence of the ODE solutions, `A = B` by uniqueness, existence/uniqueness/smoothness of QR and the time shift not covered. The step to `eq:toda_closed_Q` is in `L2_LIVRO_A3_Extra` |
| `Chap01Tensor` | Book ch. 1, `thm:tensor_weierstrass`: (i) `σ_max = sup_M Φ(T)` attained on `M = ∏S^{d_α−1}`; (ii) critical points satisfy Lim's equations with one common `σ`; a best rank-one approximation `σ_max u*⊗` exists | (i) **full** for `d_α ≥ 1`; (ii) **algebraic step only**: the Lagrange multipliers enter as `hcrit` (Euler–Lagrange with separate `μ_α`), and `μ_α = Φ(u)` is proved via the multilinear Euler identity. Best rank-one: proved optimal among all `λv⊗`, `v ∈ M`, for `k ≥ 1` (uses `max Φ = max\|Φ\|`). `C^∞` structure and the Z-eigenvalue remark not covered. Witness `diag(1,2)` |
| `L2_LIVRO_A3_Extra` | L2 complements for ch. 2 (batch A3) | `qr_closed_eq`: `QᵀQ = I`, `A₀QR = Q'R + QR'`, `QᵀQ'` skew, `R'R⁻¹` upper ⇒ `Q' = QΠ_so(QᵀA₀Q)` (the step to `eq:toda_closed_Q`), with a non-zero witness and a proved-false mutant without triangularity; `tangentProj_fix_general`: `P` fixes every `UA + BVᵀ` when `UᵀU = VᵀV = I` |

## Book batch B8 (2026-10-10)

Fidelity review: `L2_FIDELIDADE_LIVRO_B8.md`, with blind back-translation; only the standard axioms appear. Hypotheses that stand in for missing theory are explicit and named.

| Module | Source and statement | Coverage |
|---|---|---|
| `Chap10Generalization` (10.1, 10.2) | Book ch. 10, `prop:degenerate` and `prop:counterexample`: `κ*_info = 0` when an admissible geodesic exists; for full-row-rank `X ∈ ℝ^{N×D}` the minimum-norm interpolant `θ* = Xᵀ(XXᵀ)⁻¹y` interpolates, has minimal norm, `Tr(XᵀX/N) > 0`, and with uniform `±1` test labels and squared loss clipped to `[0,1]` its generalization gap is `≥ 1/2` for every input law `μ` (exactly `1/2` for `X = [1 0]`); without the rank hypothesis (`x ≡ 0`) it fails; the candidate PAC-Bayes bound at `κ* = 0` is `√(ln(2/δ)/2N)`, in `(0.19, 0.195)` for `N = 50`, `δ = 0.05`, and `< 1/2` iff `N > 2 ln 40`, i.e. for all `N ≥ 8` | 10.1 **abstract**: `κ*` is `inf F(A)` with `F ≥ 0`; "a geodesic has zero covariant acceleration" is the named hypothesis `h_geodesic` (no Fisher metric, Levi-Civita or ess sup). 10.2: the rank hypothesis is explicit (`hX : X.rank = N`) and is the only one used on the sample; the a.s.-rank form over a random sample is `L2_LIVRO_B8_Extra.gap_ge_half_ae`; the fresh label enters as the two-label average; `θ* = X⁺y` is characterised (interpolation + minimal norm), not identified with Moore–Penrose; "density ⇒ rank `N` a.s.", "constant metric ⇒ straight geodesics" and the `≈ 0.70` Gaussian value are not formalized; the PAC numbers are dimensionless (scale of the clipped loss) |
| `Chap10Generalization` (`On the formulation`) | Book ch. 10, Remark "On the formulation": `‖2I − Q‖_F² = 5d − 4 tr Q ≥ d` for `Q ∈ O(d)` | full; equality at `Q = I`; witness: 90° rotation (value 10) |
| `Chap09WindingBounds` (9.3(1)) | Book ch. 9, `thm:loop_bounding`(1): `\|w_i\| ≤ (V/ρ_i + \|Δθ_i(γ₀)\|)/2π` for paths of length `≤ V` in the free space | one obstacle at a time, **unit-speed curves differentiable on the interior** with a polar representation `r > 0` and a differentiable angle lift; the homotopy identity `Δθ(γ) − Δθ(γ₀) = 2πw` is the hypothesis `h_winding`; item (2) (finiteness of classes) not formalized. Witness: unit circle, `w = 1`, equality |
| `Chap09WindingBounds` (slingshot) | Book ch. 8, Remark after `conj:slingshot`: `\|dφ/dt\| < √f/r ≤ 1/(3√3M)` (max at `r = 3M`), `\|Δφ\| < Δt/(3√3M)`, `\|W\| < Δt/(6√3πM) + 1/2`, and `\|W\| ≤ 3` for `Δt = 100M` | full for the pointwise rate and its maximum; the sweep bound is integrated along any future-directed timelike equatorial curve in `r > 2M` (non-strict here, strict for `a < b` in `L2_LIVRO_B8_Extra`); the identification `Δφ = φ_q − φ_p + 2πW` via the angle lift is not formalized (the count bound takes it as input); realizability of each `\|W\| ≤ 3` not claimed |
| `L2_LIVRO_B8_Extra` | L2 complements for ch. 10 and the slingshot (batch B8) | the almost-sure form of the gap bound (rank `N` a.s. over a random sample under any law `P`) with its mutant (constant `X = 0`); the strict sweep bound `\|Δφ\| < Δt/(3√3M)` for `a < b`, with witness and a mutant showing `a < b` is needed |

## Book batch A-B2, graphon heat and flows (2026-10-10)

Fidelity review: `L2_FIDELIDADE_LIVRO_A_B2.md`, with blind back-translation; only the standard axioms appear. Hypotheses that stand in for missing theory are explicit and named.

| Module | Source and statement | Coverage |
|---|---|---|
| `Chap02Heat` | Book ch. 2, `thm:graphon_heat_existence` and `thm:heat_smoothing`: the closed form `W(t) = e^{−2t}W₀ + (e^{−t}−e^{−2t})(d₁+d₂) + (1−e^{−t})²m` solves `∂_tW = Δ_⊗W` and is the unique solution, with the semigroup law, coefficients summing to 1 and non-negative for `t ≥ 0`, `[0,1]` preserved, `W(t) → m`; cut-norm contraction and monotonicity; `W(t) = e^{−2t}W₀ + K_t` with `K_t` a function of the degrees, and jumps between cells with equal degrees persist with amplitude exactly `e^{−2t}` | **finite grid** (step graphon on `n` equal cells, unnormalized finite cut norm of `BeyondSpectrum1_B4`); the `L^p` contraction semigroup, the continuum `[0,1]²` and continuity of `K_t` are not formalized ("continuous" becomes "depends only on the degrees"). Witness `[[1,1],[1,0]]` (non-constant degrees, `W(log 2)` explicit); mutants: relaxation without the degree term, negative time, strict contraction; more in `L2_LIVRO_A_B2_Extra` |
| `Chap02Flows` (A) | Book ch. 2, `thm:ricci_neckpinch`: for `W' = 2κW`, `W(t) = W₀exp(2∫₀ᵗκ)`, bridge bounds `εe^{−2Ct} ≤ W ≤ εe^{−2c₂t}`, positivity, community bound `W ≥ e^{2c₁t}` | **scalar ODE at a fixed `(x,y)`**, the curvature along the flow is a given function `k`, assumed continuous on all of `ℝ` (the book does not state its regularity); the Ollivier curvature, the metric, persistence of the bounds and existence of the flow are hypotheses, as in the book. Witness `k = −1−t`; mutants: no upper curvature bound, factor 2 dropped |
| `Chap02Flows` (B) | Book ch. 2, `thm:cmps_energy_flow`: minimizers of the McLachlan functional are exactly the solutions of `gθ̇ = −b`, the system is consistent (`b` vanishes on `ker g`, a solution exists), every solution has the same velocity `−Πw`, and `d⟨H⟩/dτ = −2θ̇ᵀgθ̇ = −2‖Πw‖² ≤ 0` | **finite-parameter core**, bounded symmetric `H`. Item (i) is abstract in a real inner product space. Item (ii) (`energy_decrease`) uses the REAL projector `x − Re⟨ψ\|x⟩ψ`, i.e. a real Hilbert space; the book's complex projector `Id − \|Ψ⟩⟨Ψ\|` is in `L2_LIVRO_A_B2_Extra.energy_decrease_complex`. Not formalized: cMPS states, the unbounded Lieb–Liniger `H`, gauge and phase directions in `ker g`, existence of the flow. Witness: degenerate `g = [[1,2],[2,4]]` with two solutions; mutants: sign, consistency without `b = ⟪u,w⟫`, non-symmetric `H` |
| `L2_LIVRO_A_B2_Extra` | L2 complements for ch. 2 (batch A-B2) | mutants for `heat_jump` (unequal degrees) and `heat_unique` (no initial condition); item (ii) of `thm:ricci_neckpinch` as `W(t) > 1` for `c₁ > 0`, with a non-constant-curvature witness and a mutant; `thm:cmps_energy_flow`(ii) with the book's complex projector on a complex inner product space with hermitian `H` (no non-degenerate witness), and the phase direction `iψ` in its kernel, which is not in the kernel of the real projector |

## Book batch A-B3, special functions (2026-10-10)

Fidelity review: `L2_FIDELIDADE_LIVRO_A_B3.md`, with blind back-translation; only the standard axioms appear. Hypotheses that stand in for missing theory are explicit and named.

| Module | Source and statement | Coverage |
|---|---|---|
| `Chap03Special` (A) | Book ch. 3, Prop. "Digamma Partial Differential Equation System": over `ℂ`, `∂_x C(x,y) = C(x,y)[ψ(x+1) − ψ(x−y+1)]` for `x+1, x−y+1 ∉ ℤ_{≤0}`; `∂_y C(x,y) = C(x,y)[ψ(x−y+1) − ψ(y+1)]` for `y+1, x−y+1 ∉ ℤ_{≤0}`; the literal transport equation `d/dt C(x+t,y+t)\|₀ = C(x,y)[ψ(x+1) − ψ(y+1)]` for `x+1, y+1 ∉ ℤ_{≤0}` (no condition on `x−y`); the example `∂_y C(x,·)(−1) = 1/(x+1)` | **off the poles**, complex derivatives (`HasDerivAt` in one variable), `ψ = Complex.digamma`; each PDE needs only two of the book's three conditions; transport is the directional derivative along `(1,1)` (its identification with `∂_x + ∂_y` via joint holomorphy is not formalized); the holomorphic extension of the products `C·ψ` across the lines `y ∈ ℤ_{<0}`, `x−y ∈ ℤ_{<0}` is not formalized. Witness `(1, 1/2)` (derivative `(4/π)(2ln2 − 1) ≠ 0`); mutants: sign, `pde_y` without `y+1 ∉ ℤ_{≤0}`; transport witness and mutant in `L2_LIVRO_A_B3_Extra` |
| `Chap03Special` (B) | Book ch. 3, `thm:fibonacci`, algebraic core: `S'`, `S''`, `S'(ξ) = ln((1−2ξ)²/(ξ(1−ξ)))`, unique critical point `ξ* = (5−√5)/10` in `[0,1/2]`, `S(ξ*) = ln φ`, `S''(ξ*) = −5√5`, `C₁ = φ/√5`, and the Laplace-prefactor identity `= φ^{x+1}/√5` for `x > 0`; for general `α > 0`: `S_α'' < 0` (Cauchy–Schwarz step), `S_α' = 0 ⇔ w^{α+1} = ξu^α`, `S_α(ξ*) = ln(u*/w*)`, `z = u*/w*` solves `z^α(z−1) = 1`, `λ_α > 1` exists and is unique, at most one critical point, `λ₁ = φ` | **algebraic core only**: Stirling, Laplace's method and both asymptotics `~` are not formalized, nor existence of `ξ*` for `α ≠ 1` or the general prefactor `C_α` (asymptotics checked numerically by the L2 reviewer). Witness `α = 1`, `ξ*`; mutants: constant `1/√5`, the other root `(5+√5)/10`, convex `S_α`, `λ = φ²` |
| `Chap03Special` (C) | Book ch. 3, `prop:fractional_props`: (1) `K_α(0,…,0,α) = 1` and `K_α > 0` for `y_j ≥ 0`, `K_α(y, α−y) = C(α,y)`; (2) for `m = 2`, `D^α f(x) → f(x)` as `α → 0⁺` for continuous `f` (book form: bounded uniformly continuous, as a corollary), with `\|D^α f(x) − f(x)\| ≤ sup_{[0,α]}\|f(x−y) − f(x)\|`; (3) `D^α e^{λ·} = e^{λx}G_α(λ)`, `G_α(0) = 1` | (2) only for **`m = 2`** (1D Beta-kernel operator); (3) only for **real `λ`**; `C^∞` of `K_α`, `m ≥ 3`, complex `λ` and analyticity of `G_α` are not formalized. Witness `D^α id(x) = x − α/2` (so `D^1 id ≠ id`, and `id` is unbounded); mutants: `D^α = Id` at fixed `α`, `K_α` at the zero vector of `ℝ^{m+1}` |
| `L2_LIVRO_A_B3_Extra` | L2 complements for ch. 3 (batch A-B3) | for the literal transport equation: a non-degenerate witness at `(1, 1/2)`; at `(0,1)` (line `x−y = −1`) the hypothesis of `pde_x` fails but `transport` applies; mutant: without `y+1 ∉ ℤ_{≤0}` it is false at `(0,−1)` (`t ↦ C(t,t−1)` has derivative 1, right-hand side 0) |

## Book batch B9, control and obstacle (2026-10-10)

Fidelity review: `L2_FIDELIDADE_LIVRO_B9.md`, with blind back-translation; only the standard axioms appear. Hypotheses that stand in for missing theory are explicit and named.

| Module | Source and statement | Coverage |
|---|---|---|
| `Chap07Control` (7.3) | Book ch. 7, `lem:wall_structure` (c)–(d) for the linear wall problem `y' = θ`, `θ' = κ`, `\|κ'\| ≤ 1`: every boundary arc lies in `[t*, T]`; every contact point `t ∈ Z` is an isolated zero of `y` with `y > 0` for `0 < \|s−t\| < 3κ(t)`; `θ(t) = 0 < κ(t)` on `Z ∩ (0, t*)`; `Z ∩ [0, t*−ε]` finite; Taylor `\|y(s) − y(t) − θ(t)(s−t) − κ(t)(s−t)²/2\| ≤ \|s−t\|³/6` | trajectories = `y, θ` continuous, `y' = θ`, `θ' = κ` on `(0,T)`, `κ` 1-Lipschitz (the measurable control `u` does not appear); **item (b) ("a vanishing state rests at the origin", the only input from minimality) is the named hypothesis `hB`**, items (a)–(b) and the cost functional are not formalized; `t*` and `Z` defined as in the book; the closing sentence of (d) ("finite or an increasing sequence → `t*`") not formalized. Witnesses: `y = (t−1)²(2−t)³/150` (`Z = {1}`, `κ(1) = 1/75`) and `y = max(1−t,0)³/6` (rest arc `[1,2]`). Mutants: no state constraint, radius `4κ` (`y = s²/2 − s³/6`, so `3κ` is sharp), `y ≡ 0`, degenerate arc `[1,1]` |
| `Chap07Control` (7.4) | Book ch. 7, `thm:obstacle_exclusion` (1)–(2) for curves (`k = 1`): at a contact point of a curve in `Ω̄`, `⟨ν, v⟩ = 0` and `⟨ν, α''(0)⟩ ≥ h(v,v)`; `‖II‖ ≥ max(0, λ₁)`; plus the local second-order test "`f ≥ 0`, `f(0) = 0` ⇒ `f''(0) ≥ 0`" | real inner-product space; the signed distance enters through its gradient `gd` near `p₀`, `gd` differentiable at `p₀`, `∇d(p₀) = ν`, `⟨∇²d(p₀)w, w⟩ = −h(w,w)` on `ν^⊥` (Gilbarg–Trudinger 14.16 as **hypotheses**, weaker than `C²`); `M ⊂ Ω̄` as `d∘α ≥ 0` near `0`; Courant–Fischer for `k = 1` is the hypothesis `lam ≤ h` on unit tangent vectors; `II(v,v) = a − ⟨a,v⟩v` for `‖v‖ = 1`; items (3)–(4) and `k ≥ 2` not covered. Witness: unit circle in the unit disc (equality in both). Mutants: without `M ⊂ Ω̄` (tangent line); `‖II‖ ≥ \|λ₁\|` false for a convex obstacle (book's Remark "Convex obstacles") |
| `Chap07Control` (7.4, disc) | Book ch. 7, `thm:obstacle_exclusion`, closing computation: an arc-length curve from `(−1,0)` with initial tangent `(1,0)`, `\|κ\| ≤ 1/2`, that reaches `x = 1` enters the open disc of radius `1/2` about the origin; `2 − √(4 − 9/16) < √(3/16)` | **`C²` curves** (`φ` differentiable on `(0,ℓ)` with pointwise `\|φ'\| ≤ 1/2`), not the book's `C^{1,1}` a.e. bound; the continuation "graph while `cos φ > 0`" is proved, not assumed; the inference "hence `κ* ≥ 1/2`" (infimum over the class) not formalized. Witness: the arc of radius `2` (`κ ≡ 1/2`). Mutant: radius `1/10` false (the same arc stays at distance `≥ 1/10`) |
| `Chap07Control` (7.9) | Book ch. 7, `prop:optimal_regularity`, core step: a continuous curvature with values in `{0, ±K̂}` is constant; if not identically `0`, it is `≡ K̂` or `≡ −K̂` (a single arc) | only the sentence "continuous, hence constant, hence a single piece, not a segment"; Dubins' theorem (values in `{0, ±K̂}`), `κ*(L)` as a minimum, hypothesis (H), and "not a segment" (`∃ s, κ(s) ≠ 0`) are hypotheses; the "if and only if" and `κ* > 0` not formalized. Witness: the `CS` profile is shown not continuous. Mutants: no continuity; values in `[−K, K]` |
| `L2_LIVRO_B9_Extra` | L2 complements for ch. 7 (batch B9) | `0 < \|s−t\| < 3κ(t)` forces `κ(t) > 0` (the dropped hypothesis is redundant); the radius `cκ(t)` fails for **every** `c > 3` (sharpness of `3κ`); an admissible trajectory `y = (1 − cos(t−1))²/10` on `[0, 1+2π]` (`\|y'''\| ≤ 1`, `y ≥ 0`, final state `0`) with a vanishing state at `t = 1 < t*` and `κ(1) = 0`, proving that (d)(ii) fails without `hB` and that `hB` is genuinely load-bearing |
