# Ramo E: mixing from the symmetries of Δ₂ (draft, unverified)

2026-09-28. Written by Claude and not yet checked by an independent verifier. Every number below comes from the scripts in this folder.

## Question
The fermion paper makes the charged-lepton mass matrix circulant, which leaves a residual Z₃ (rotation of the triangle Δ₂). In flavour theory, the PMNS matrix is then fixed by which residual Z₂ the neutrino mass matrix keeps. Which Z₂'s does the geometry of Δ₂ offer, and which of them survive the data?

## Results

| Residual Z₂ in the neutrino sector | Fixed PMNS column | Best χ² (3 data, 2 free) | Status |
|---|---|---|---|
| a vertex transposition (element of S₃) | (1/√2, 1/√2, 0) | 692 | **excluded**: forces a zero entry |
| sign flip at two vertices | (1,1,1)/√3, which is TM2 | 17.8 | disfavoured: sin²θ₁₂ = 0.341, +2.8σ |
| transposition composed with a sign flip at the other two vertices | (2,1,1)/√6, which is TM1 | 1.3 | **compatible** |

Each column comes from 6 of the 48 signed permutations. Scripts: `residual_symmetries.py`, `signed_scan.py`, with outputs in `*.out.txt`.

1. **The S₃ of the triangle alone is excluded.** With circulant charged leptons, a residual transposition always produces a zero in the PMNS matrix (numerical, with an analytic oracle). The Δ₂ geometry as it stands in the paper therefore cannot produce viable mixing.
2. **Adding an orientation sign at each vertex fixes this.** That enlarges the group to the signed permutations B₃ ≅ S₄ × Z₂. The involution "reflection of the triangle times a sign flip" gives TM1, which fits the data.
3. **TM1 predictions:**
   - sin²θ₁₂ = 1 − 2/(3 cos²θ₁₃) = 0.318 at the measured θ₁₃. This is +0.9σ from NuFIT 6.0. JUNO will measure sin²θ₁₂ to well below 1%, so it can confirm or exclude this. *Check the published JUNO first result before citing.*
   - cos δ_CP = −cot 2θ₂₃ (1 − 5s₁₃²) / (2√2 s₁₃ √(1 − 3s₁₃²)), giving δ ≈ 286° (or 74°) for s²₂₃ = 0.56 and δ ≈ 262° (or 98°) for s²₂₃ = 0.47 (`tm1_delta.out.txt`). DUNE and Hyper-K test this.

Checks:
- oracle: the closed-form TM1/TM2 sum rules agree with the numerical fit;
- negative controls: a matrix with no symmetry gives no fixed column, and the fixed column (1,0,0) gives χ² = 1657.

## Honest labels
- **Prior art (not new).** The following are known results:
  - TM1/TM2 and their sum rules: Albright and Rodejohann (2009); King and Luhn (2012–2013).
  - TM1 from S₄ with residual Z₂ = SU: Varzielas and Lavoura (2012), among others.

  *Resolve the DOIs with `audit/scripts/check_references.py` before citing.* The candidate new part is only the **geometric reading**: B₃ as "the triangle with oriented vertices".
- **Open (the real conjecture).**
  - (a) Why would vertex orientations be physical? One candidate is spin structure or orientation of the simplex; this needs a derivation.
  - (b) Why would the neutrinos keep exactly "reflection × sign" while the charged leptons keep Z₃? This is the vacuum-alignment problem that every flavour model has.
  - Without (a) and (b), TM1 is a choice, not a prediction.
- **Parameter count.** TM1 has 2 free parameters (θ, φ) for 4 observables (θ₁₂, θ₁₃, θ₂₃, δ). That leaves 2 genuine predictions: θ₁₂ and δ as functions of the other two.

## Via 1: absolute neutrino masses (`neutrino_masses.py`, output `neutrino_masses.out.txt`)

The fermion paper has no neutrino mass structure, so two extensions were tested.

**H1: neutrino Koide, Q = 2/3 (circulant with b/a = 1/√2).**
- Normal ordering (NO): a solution exists only with a negative root for m₁. All-positive roots cannot reach Q = 2/3; this is negative control 1 and it passes. The solution is m = (0.36, 8.66, 50.34) meV, giving:
  - Σm = 59.4 meV;
  - m_β = 8.9 meV;
  - m_ββ ∈ [1.4, 4.0] meV (TM1, Majorana phases free).
- Inverted ordering (IO): Σm = 102.6 meV. That is above the DESI DR2 + CMB bound Σm < 64.2 meV (PRD 112, 083515), so **H1 plus cosmology predicts normal ordering**. If JUNO or DUNE find IO, H1 is dead.
- Oracle: an independent circulant fit recovers b/a = 0.70711 with residual about 10⁻³².
- Weakness: Σm = 59.4 meV is essentially the NO minimum (Q = 0.60 gives 59.0 meV, so negative control 2 is only marginally discriminating). m_ββ of a few meV lies below LEGEND-1000 and nEXO, and m_β lies below Project 8's target. The only test within reach is **the ordering**.
- Prior art: a neutrino Koide relation with a negative root was proposed by Brannen (2006). Resolve the reference before citing.

**H2: the same circulant phase as the charged leptons.**
- The charged leptons give δ_l = 0.22222 rad = 2/9 to five digits, which is Brannen's known observation.
- With δ_ν = δ_l, the model predicts Δm²₂₁/Δm²₃₁ = 0.0035, against 0.0296 in the data. **H2 is excluded** (factor 8.4).
- With δ_ν = δ_l + π/12 (Brannen's ad hoc shift), the ratio is 0.0308, +1.6σ from the data (ratio uncertainty ≈ 2.7%). The H1 solution has δ_ν = 0.478 rad, against δ_l + π/12 = 0.484 rad.
- The π/12 is prior art and has no derivation. Deriving it from Δ₂ geometry is a well-posed conjecture: a zero-parameter prediction of the ratio.

## Via 2: CKM from B₃ (`ckm_scan.py`, output `ckm_scan.out.txt`)

B₃ has 62 abelian subgroups, and 33 of them fix the eigenbasis completely. Pairs of these subgroups (H_u, H_d) give exactly 7 fixed |V| patterns. Their moduli are:
- {0, 1}
- {0, ½, 1/√2}
- {0.211, 0.577, 0.789}
- {0, 1/√2, 1}
- {⅓, ⅔}
- {1/√3}
- {0, 0.408, 0.577, 0.707, 0.816}

**All 7 are excluded**; the smallest χ² is about 2·10⁵, for the identity pattern.

If one sector keeps only a Z₂, one angle is free, so |V_us| is fitted rather than predicted. **B₃ gives no zero-parameter Cabibbo angle.** At leading order the best it offers is V = 1, the same as the paper's circulant result, and the Cabibbo angle must come from symmetry breaking.

Checks:
- oracles: circulant with circulant gives a permutation matrix, and circulant with the Klein group gives all entries 1/√3;
- negative control: random unitaries give χ² ≈ 10⁷.

Reading: the oriented-vertex group that rescues the leptons (TM1) does **not** explain the quarks. Residual-symmetry predictions of θ_C in the literature need larger groups; for example the dihedral D₇ gives sin(π/14) = 0.2225. Resolve the references before citing. The paper's Gatto–Sartori–Tonin relation, a mass-mixing relation rather than a symmetry one, remains the only quark-mixing handle.

## Next steps
1. Independent verification of the scripts and of the claim that S₃ alone is excluded (four-eyes rule).
2. Literature search: has anyone read S₄ or B₃ as oriented-simplex symmetry, or as a hyperoctahedral flavour group?
3. Try to derive (a): does the construction of Δ₄×Δ₂ in the paper carry a natural Z₂ per vertex?
4. Quarks: does the same structure give a non-trivial CKM matrix? The circulant CKM is trivial today.

## After independent verification (VERIFICACAO.md, 2026-09-28)
Result: 21 CONFIRMA, 1 REFUTA, 3 INCERTO.
- **REFUTA:** the data mix two NuFIT 6.0 analyses (IC19 without SK and IC24 with SK). The effect on the numbers is below 0.5%, but the θ₂₃ octant changes the δ prediction. Redo the fit with a single dataset.
- **Sources confirmed by the verifier:**
  - JUNO first result: sin²θ₁₂ = 0.3092 ± 0.0087 (arXiv:2511.14593). TM1 (0.318) is at +1.0σ and TM2 (0.341) at +3.7σ.
  - DESI DR2: Σm_ν < 0.0642 eV (PRD 112, 083515). H1 in NO (59.4 meV) is allowed; H1 in IO (102.6 meV) is excluded.
- **Data fixed (B13):** all inputs now come from the NuFIT 6.0 IC19 analysis without SK-atm (Esteban et al., JHEP 12 (2024) 216), Δm²₃₁ = 2.534·10⁻³ and Δm²₃₂(IO) = −2.510·10⁻³ eV². With IC24 + SK-atm, θ₂₃ is in the lower octant (s²₂₃ = 0.470) and TM1 gives δ ≈ 262° or 98° instead of 286° or 74° (`tm1_delta.out.txt`); the δ prediction therefore depends on the octant, which DUNE and Hyper-K will settle.
