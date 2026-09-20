# Adversarial Audit: Lean 4 Formal Proofs & Python Numerical Simulations

## 1. Lean 4 Formal Hygiene

**Mechanical hygiene is clean**: no `sorry`, `admit`, or `axiom` keywords anywhere in the corpus. Universe levels in `Category.lean` (`u, v`, `Type (max u v)` for `Path`) are handled correctly. That said, "zero axioms, zero sorries" is a much weaker claim than the Main.lean banner implies, because of how the *content* is structured:

**a) The categorical tier (`CTensMan.lean`, `Cobordism.lean`, `EmergentFunctor.lean`, `MonoidalCoherence.lean`) is largely physics-independent boilerplate.**
`ContinuousTensorVariety` and `CauchyHypersurface` carry fields like `adm_on_shell`, `qfi_nondegenerate`, `einstein_satisfied`, `adm_lapse_smooth` — but these are **unconstrained `Bool`s that never appear in any proof obligation**. `id_comp`, `comp_id`, and `assoc` are proved purely via `pathConcat`/`Path` induction, which holds for *any* `Step` type regardless of its field values. Concretely:

- `map_id_preservation` and `map_comp_preservation` (Theorem 5.2, "Functoriality") only ever unfold `mapPath`/`pathConcat`. They would go through identically if `stepMap` set `einstein_satisfied := false` for every step. The theorem is a generic fact about free-path-category functors, dressed in physics vocabulary — it does **not** certify that gradient flows assemble into Einstein-satisfying cobordisms.
- `object_monoidal_isomorphism` reduces via `dsimp` to `a && b = a && b` (both sides compute the same Boolean AND), and `braiding_naturality` reduces to `true = true` since both `stepMap` and `cobordismTranspose` hardcode `adm_lapse_smooth := true`. These are not proofs of geometric/categorical coherence (no pentagon/hexagon diagrams, no actual metric isomorphism) — they're tautologies about literal constants.

This is the single biggest finding: **the "0 axioms" categorical tier doesn't formalize ADM constraint propagation or Einstein's equations at all — it formalizes that free path categories compose associatively**, which is textbook and has nothing to do with tensor networks specifically.

**b) `SpectralDimension.lean` and `WheelerDeWitt.lean` encode physics claims as definitions, then prove arithmetic about the definitions.**
`ds_num k := 4 + 2*k`, `ds_den k := 1 + k` are *asserted* to represent the spectral dimension — not derived from an actual heat-kernel trace computation. Every subsequent theorem (`spectral_dim_ir`, `strictly_above_two`, `le_four`, `strictly_decreasing`) is proved by `omega` on this hand-picked rational function — real theorems, but about arithmetic, not about a computed spectrum. Theorem 4.8 ("Exact Quadratic Cancellation in the IR Heat Kernel") is literally `(1-X)+(X+3+err) = 4+err`, an algebraic tautology with no heat kernel, diffusion equation, or Bessel function anywhere in sight.

Similarly, `contracted_extrinsic_x3 := 3*shear_sq + tr_K*tr_K` in `WheelerDeWitt.lean` is *defined* to make the "Shear-Trace Decomposition" trivially true; `ExtrinsicCurvatureData` is just two free integers with no actual tensor `K_ij`, no metric `γ_ij`, no traceless-part construction. `lapse_variation_x2 := -(volume_factor * H_val)` similarly begs the question that this equals `δS/δN`.

This pattern is fine as a *sanity check that the claimed closed-form formulas are internally self-consistent*, but it should not be represented (as Main.lean's banner does) as mechanically proving Wheeler-DeWitt stationarity or spectral-dimension RG flow from first principles.

**c) `SimplicialHodge.lean` is the strongest module.** It genuinely derives coboundary nilpotency, self-adjointness of up/down/Hodge Laplacians, the energy decomposition, and positive semi-definiteness from abstract `PreHilbertSpace`/`AdjointPair` axioms — real, nontrivial, Mathlib-style abstract algebra, internally consistent (note it correctly proves only *semi*-definiteness, matching the non-strict `inner_nonneg` hypothesis). Its concrete inhabited model, however, uses the **zero operator** (`op := fun _ => 0`) on `Nat` — the most degenerate possible witness, proving only that the axioms aren't vacuous, not that they're satisfiable by a genuine simplicial chain complex with real ℤ-valued incidence matrices.

**d) `NullEnergy.lean`** correctly proves sum-of-squares non-negativity by induction — legitimate but a drastic toy simplification of the actual quantum NEC (real Hilbert-Schmidt norms on operator spaces, not `List Int`).

## 2. Python Numerical Validity

The 13 chapter scripts mix genuinely solid numerics with weak or tautological "verifications":

**Solid, independently cross-validated tests:**
- Ch.11 Battery 1 (BKM/Fisher-information Hessian of relative entropy via finite differences vs. analytic formula) — a real, nontrivial quantum-information computation.
- Ch.02 Toda flow isospectrality + QR interpolation, Ch.05 adjoint-duality tests, Ch.08 Schwarzschild geodesic/Christoffel calculations (Keplerian orbit acceleration vanishing is a real, falsifiable check) — legitimate.
- Ch.01 cut-norm duality (exhaustive over 2^6 subsets) — correct brute-force method.

**Tautological / self-referential "obligations"** (construct data from the formula being tested, then check it matches the formula):
- Ch.07 Battery 1 (`curvatures[in_arc] = kappa_star_true` then assert `peak_curv == kappa_star_true`), Battery 2 (`max(a,b) >= a and >= b`, trivially true), Battery 3 (Chebyshev "equioscillation" built via `sign(sin(theta))`, then checked against itself), Battery 6 (`kappa_0/sqrt(c)` asserted monotonic — true by inspection of the formula), Battery 7 (round-trip `R=1/k; k=1/R` inversion). None of these solve an actual constrained curve-shortening/obstacle-avoidance variational problem; they algebraically restate the claim and check equality.
- Ch.12/13 spectral-dimension battery: `P(t) = 1/(4πt(1+t/t_cross))` is a hand-picked ansatz (not derived from an actual computed Laplacian spectrum), then its known asymptotics (2 at t→0, 4 at t→∞) are numerically confirmed — this mirrors the Lean issue above.
- Ch.02 Battery 5 (Ollivier-Ricci "neckpinch"): `w1_bridge` is computed as a total-variation-style proxy for Wasserstein-1 distance, then multiplied by an **ad hoc factor of `2.0`** with the comment "distance across bridge" — this looks like a fudge inserted specifically to flip the sign to negative curvature, rather than a principled optimal-transport computation (e.g., via linear programming on the actual graph metric). This should be redone with a real OT solver.

**Other concerns:**
- `test_tensor_operator_norm_scaling` (Ch.01) uses a heuristic power-iteration (not exact — best rank-1 tensor approximation is NP-hard for order ≥3) with a very loose acceptance band (`1.0 < normalized < 4.5`), which would pass under many incorrect scaling laws too.
- `np.random.seed(42)` fixed globally throughout all 13 scripts — deterministic and reproducible, but no seed-sweep/variance reporting anywhere, so "verified" really means "true for one draw."
- LQG area-spectrum monotonicity (Ch.11 Battery 6) is nearly tautological: `sqrt(j(j+1))` times a positive prefactor is trivially increasing in `j`.

## 3. Alignment with Physics

There's a systematic gap between what's *claimed* (functorial emergence of Einstein-satisfying spacetime, spectral-dimension RG flow 4→2, Wheeler-DeWitt stationarity, minimax curvature obstacle theory) and what's *mechanically checked* (generic path-category algebra, arithmetic identities of hand-asserted formulas, or self-referential construction-then-check patterns). The strongest, most physically faithful pieces are the ones that actually import real formulas from established physics/math and cross-check them independently: Ch.11's BKM metric, Ch.08's Schwarzschild geodesics, Ch.06's Sierpinski gasket decimation spectrum (genuine Fukushima-Shima eigenvalues), and `SimplicialHodge.lean`. The weakest are exactly the modules making the largest claims (spacetime emergence functoriality, spectral dimension flow, minimax obstacle curvature) — these substitute definitional fiat for derivation.

## 4. General Feedback

**Strengths**: clean Lean hygiene (no cheats), well-organized abstract algebra in `SimplicialHodge.lean`, some genuinely rigorous cross-validated numerics (Ch.02, Ch.05, Ch.08, Ch.11), consistent reproducibility practices (fixed seeds, explicit tolerances).

**Vulnerabilities/improvements**:
1. Replace the unconstrained `Bool` fields in `CTensMan`/`Cobordism`/`EmergentFunctor` with actual propositions that participate in the proofs (e.g., real ADM constraint equations as hypotheses used inside `map_comp_preservation`), or stop calling the current result "Functoriality of the Emergent Spacetime Functor" — it's functoriality of an arbitrary free-category map.
2. In `SpectralDimension.lean`/`WheelerDeWitt.lean`, either derive the formulas from a genuine heat-kernel/ADM computation, or relabel the theorems as "self-consistency of the proposed closed-form ansatz" rather than "exact IR/UV limits" — the current naming overstates what's proven.
3. Fix the Ollivier-Ricci neckpinch test to use an actual optimal-transport solver instead of an ad hoc ×2 multiplier.
4. Replace tautological Ch.07/09 "batteries" (construct-then-check-equal) with actual numerical solves of the underlying constrained variational problems.
5. Strengthen `SimplicialHodge.lean`'s concrete model beyond the zero operator — use a real small simplicial complex with integer incidence matrices.
6. Tighten loose assertion bounds (e.g., the 1.0–4.5 tensor-norm band) and run seed-sweeps rather than a single fixed seed for stochastic/heuristic tests.

## 5. Final Verdict

This codebase demonstrates good software hygiene and contains some genuinely rigorous sub-results, but **it does not establish a robust formal or numerical foundation for the treatise's central quantum-gravity/unification claims**. The category-theoretic "functoriality" and "coherence" theorems are generic facts about free path categories that hold regardless of the (unconstrained) physics-labeled fields — they don't encode Einstein's equations or ADM constraints in any falsifiable way. The spectral-dimension and Wheeler-DeWitt Lean modules prove arithmetic tautologies about hand-asserted formulas rather than deriving those formulas from more primitive physics. The Python suite is a mix of legitimate independent numerical checks and self-referential "construct the answer, then verify it matches" batteries that would pass under many incorrect theories. The "0 sorry / 0 axioms / 100% PASS" framing in `Main.lean` is technically accurate but substantially overstates the depth of what has actually been mechanically verified relative to the stated physical claims. I'd characterize the current state as **credible scaffolding/proof-of-concept**, not a validated formal-and-numerical foundation — the genuinely strong pieces (`SimplicialHodge.lean`, Ch.11 BKM metric, Ch.08 GR geodesics) should be the model for reworking the weaker categorical and spectral-dimension/ADM tiers.
