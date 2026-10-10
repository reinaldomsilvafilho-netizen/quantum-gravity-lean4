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
