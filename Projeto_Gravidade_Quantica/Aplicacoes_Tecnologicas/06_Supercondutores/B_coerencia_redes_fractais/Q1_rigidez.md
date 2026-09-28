# Q1: phase stiffness and ordering temperature near the threshold d_s → 2⁺

Draft of 2026-09-28. **Status: draft, not verified.** An independent verifier has not yet checked it (four-eyes rule).
Scripts and outputs are in `scripts/`; the figures are the `fig_q1_*.png` files in this folder.

Labels used: **[proved]** means a complete proof is given here; **[classical]** means a known result, restated;
**[numerical]** means computed, with an oracle and a negative control; **[heuristic]** means a non-rigorous estimate;
**[conjecture]** means an open statement.

## 0. Setting and notation

- G is a graph with bounded degree. L = D − A is the combinatorial Laplacian with unit bonds.
- A finite piece of G with N sites is given a Dirichlet ("grounded") boundary: the three corners of the gasket, the four tips of the Vicsek cross, the outer faces of the grid fractals. Alternatively it has no boundary at all (torus, or a product with a ring), and then L⁺ (the pseudo-inverse) is used.
- Harmonic (spin-wave) XY model: H_sw = (J/2) Σ_⟨ij⟩ (θ_i − θ_j)² = (J/2) θᵀLθ. Then

  ⟨δθ_x²⟩ = (T/J) G(x,x),  with G = L_D⁻¹,

  and the site average is

  **Ḡ_N = (1/N) Tr L_D⁻¹ = ∫ dN_N(λ)/λ**,

  where N_N is the normalized eigenvalue counting function (IDOS) of L_D.
- Ḡ_∞ = lim Ḡ_N < ∞ is, up to the constants of bounded degree, the condition that the walk is "transient on average" (TOA) in the sense of Cassi and of Burioni–Cassi–Vezzani (items 1–3 of `literatura.md`). Ḡ_∞ is therefore the natural quantitative measure of the distance from the Mermin–Wagner threshold. Their theorem is a dichotomy between TOA and ROA; the question here is **how** Ḡ_∞ degenerates at the threshold.

## 1. Threshold asymptotics with a log-periodic factor [proved]

**Hypothesis (H).** For 0 < λ ≤ λ₀ the IDOS of the infinite graph has the form

  N(λ) = λ^{d_s/2} [ p(ln λ) + r(λ) ],

where:
- p is periodic with period ln R (R is the spectral scaling factor; R = 5 for the gasket), p ∈ L²(0, ln R), and its mean is ⟨p⟩ = (1/ln R)∫₀^{ln R} p > 0;
- |r(λ)| ≤ C_r λ^δ for some δ > 0.

For p.c.f. self-similar fractals, a form of this type with a periodic p is the Kigami–Lapidus result (the book, ch. 6). For lattices p is constant: p = 1/(4π) in 2D, and 1/(6π²) in 3D (Weyl).

**Proposition 1.** Let ε = d_s/2 − 1 > 0 and write ω_k = 2πk/ln R. Then

  Ḡ_∞ = ⟨p⟩ λ₀^ε / ε + B,  with |B| ≤ N(λ₀)/λ₀ + λ₀^ε ‖p‖₂ √(ln R) / (2√3) + C_r λ₀^{ε+δ}/(ε+δ) + ∫_{λ₀}^∞ dN/λ.

In particular, along any family with uniformly bounded (p, C_r, δ, λ₀):

  **Ḡ_∞ = ⟨p⟩/ε + O(1) = 2⟨p⟩/(d_s − 2) + O(1)  as d_s → 2⁺.**

The log-periodic factor enters the leading term only through its mean ⟨p⟩. Its oscillating harmonics contribute only O(1).

*Proof.*
1. Split the integral at λ₀. The part above λ₀ is bounded by N(λ₀)/λ₀.
2. Integrate by parts on (0, λ₀]: ∫ dN/λ = N(λ₀)/λ₀ + ∫₀^{λ₀} N(λ) λ⁻² dλ. The boundary term at 0 vanishes, because N(λ)/λ = O(λ^ε).
3. Substitute u = ln λ. The main term becomes ∫_{−∞}^{u₀} e^{εu} p(u) du, with u₀ = ln λ₀.
4. Expand p in its Fourier series, p(u) = Σ_k p_k e^{iω_k u}. It converges in L². The integral against the integrable weight e^{εu} on (−∞, u₀] can be exchanged with the sum, which gives

   ∫_{−∞}^{u₀} e^{εu} p(u) du = Σ_k p_k e^{(ε+iω_k)u₀}/(ε + iω_k).

5. The k = 0 term is ⟨p⟩λ₀^ε/ε.
6. For k ≠ 0, |ε + iω_k| ≥ |ω_k|. By Cauchy–Schwarz,

   Σ_{k≠0} |p_k|/|ω_k| ≤ (Σ|p_k|²)^{1/2} (Σ_{k≠0} ω_k⁻²)^{1/2} = ‖p‖₂ (ln R)^{−1/2} · (ln R/2π)(π/√3),

   using Σ_{k≠0} k⁻² = π²/3 and Parseval with the normalization ‖p‖₂² = ∫₀^{ln R}|p|² = ln R Σ|p_k|². This bound is independent of ε.
7. The remainder r contributes at most C_r ∫₀^{λ₀} λ^{ε+δ−1} dλ = C_r λ₀^{ε+δ}/(ε+δ). ∎

For ε ≤ 0 the same computation with a lower cutoff λ_min gives the other two regimes:
- ε = 0: Ḡ ≈ ⟨p⟩ ln(1/λ_min);
- ε < 0: Ḡ ≈ λ_min^{ε} · F(ln λ_min)/|ε|, where F is a log-periodic function whose oscillation does **not** average out. On the fractal it is invisible only because the sizes are sampled at whole generations.

A single interpolating form, which is the truncation of the k = 0 term, is

  Ḡ_N ≈ Ḡ_∞ − (⟨p⟩/ε) λ_min^ε,  with λ_min ≍ N^{−2/d_s}.   (★)

For ε → 0 it reduces to ⟨p⟩ ln(1/λ_min) = (2⟨p⟩/d_s) ln N.

Status of the parts:
- Proposition 1 is proved, given (H).
- The identification λ_min ≍ N^{−2/d_s} and the use of the truncated infinite-volume IDOS for a finite graph are **[heuristic]**. This concerns the finite-size law (★); it is tested numerically in §3.

## 2. Consequences for stiffness and ordering

**2a. Coherence length for d_s < 2 [heuristic, tested by MC in §4].**
- In the harmonic model ⟨δθ²⟩ = (T/J)Ḡ_N with Ḡ_N ≍ N^{2/d_s−1}.
- Phase coherence is therefore lost beyond N_ξ ≍ (J/T)^{d_s/(2−d_s)} sites.
- In length: ξ ≍ (J/T)^{1/(d_w−d_f)}, using d_s = 2d_f/d_w.
- Gasket: d_w − d_f = log₂(5/3) ≈ 0.737, so ξ ∝ (J/T)^{1.357}.

**2b. Twist (helicity) stiffness [classical, restated].** A phase difference Δφ imposed across a sample of linear size ℓ costs, in the Gaussian model,

  E_twist = (J/2) Δφ² C(ℓ),

where C is the effective conductance between the two terminals. On a self-similar network C(ℓ) ≍ ℓ^{d_f − d_w} (the Einstein relation), and

  **d_f − d_w = d_w (d_s − 2)/2.**

So the macroscopic twist stiffness grows with ℓ exactly when d_s > 2, the same threshold as Cassi's. Near the threshold the growth exponent vanishes linearly in d_s − 2.

The face-to-face resistances computed in `q1_green_scaling.py` give:
- carpet: R_{n+1}/R_n → 1.2503, so d_w = 2.096 and d_s = 1.806 (the stiffness decays as ℓ^{−0.20});
- Menger sponge: R ratio 0.536, so d_w = 2.159 and d_s = 2.526 (the stiffness grows as ℓ^{+0.57}).

These estimates of d_s come from resistance and are independent of the Green-function data.

**2c. Ordering temperature.**
- Spherical model (n → ∞): the critical temperature is T_c = J/Ḡ_∞, where Ḡ_∞ is the spatial average of the coincident Green function. This is the standard saddle-point equation; for graphs see Burioni–Cassi (PRL 76, 1091 (1996), DOI 10.1103/PhysRevLett.76.1091, title checked on Crossref; **abstract not read in this session: confirm that the T_c formula is stated there before citing it for it**).
- Combined with Proposition 1: **T_c^{sph} = J (d_s − 2)/(2⟨p⟩) · (1 + O(d_s − 2))**, a linear vanishing at the threshold. This is **[proved]** for the spherical model under (H).
- For O(n) with unit spins, the large-n estimate is T_n ≈ J/(n Ḡ_∞) **[heuristic]**. For the XY model (n = 2) on the cubic lattice it gives 1/(2·0.25273) = 1.978 J; our Monte Carlo gives about 2.2 J (§4). The estimate is therefore about 10 % low, with the same order of magnitude.
- **[conjecture]** For O(n ≥ 3) on graph families with the same p, T_c ∝ (d_s − 2) as d_s → 2⁺. This agrees with the 2+ε expansion of the nonlinear sigma model on lattices, which is suggestive only.
- For **XY (n = 2)** this form is doubtful. At d_s = 2 the square lattice has a BKT phase with finite stiffness (T_BKT ≈ 0.89 J), carried by vortex physics that Ḡ does not see. What vanishes linearly in the Gaussian theory is the true long-range-order scale. Whether the stiffness scale vanishes depends on the cycle and vortex structure of the family, not on d_s alone. This is an open point: a family of graphs with d_s → 2⁺ and equal cycle structure is needed to test it.

## 3. Numerics: Ḡ_N versus size

(filled in below from `out_q1_*.txt`)
