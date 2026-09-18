# Executive Taxonomy & Landscape of Theories of Everything and Quantum Gravity

**Author**: Reinaldo M. Silva-Filho  
**Institution**: PPGEE/DES, Universidade Federal de Lavras (UFLA)  
**Support**: CAPES Finance Code 001  
**Monograph DOI**: [10.5281/zenodo.22290043](https://doi.org/10.5281/zenodo.22290043)  
**Universe Lagrangian Record**: [10.5281/zenodo.22441676](https://doi.org/10.5281/zenodo.22441676)

---

## 1. The Foundational Crisis of Modern Physics

Contemporary fundamental physics is bifurcated across two incompatible pillars, each empirically validated with extraordinary precision within its own domain:
1. **General Relativity (GR)**: A deterministic, background-independent classical field theory describing gravity as the intrinsic curvature of a continuous 4D pseudo-Riemannian pseudo-manifold $(\mathcal{M}, g_{\mu\nu})$. Its action is the Einstein-Hilbert functional:
   $$\mathcal{S}_{\mathrm{EH}} = \frac{1}{16\pi G} \int_{\mathcal{M}} (R - 2\Lambda) \sqrt{-g} \, d^4x$$
2. **The Standard Model of Particle Physics (SM)**: A linear, background-dependent quantum field theory (QFT) based on the gauge group $G_{\mathrm{SM}} = \mathrm{SU}(3)_c \times \mathrm{SU}(2)_L \times \mathrm{U}(1)_Y$ formulated on a rigid flat Minkowski metric $\eta_{\mu\nu}$, containing 19 to 26 arbitrary empirical parameters.

When standard perturbative quantization is applied to the Einstein-Hilbert action ($g_{\mu\nu} = \eta_{\mu\nu} + \sqrt{16\pi G} h_{\mu\nu}$), the coupling constant carries negative mass dimension $[G] = M^{-2}$, causing loop diagrams to diverge quadratically and quartically:
$$\int^\Lambda \frac{k^3 dk}{k^2} \sim \Lambda^2, \quad \int^\Lambda \frac{k^7 dk}{(k^2)^2} \sim \Lambda^4$$
This generates infinitely many independent counterterms at each perturbative order, rendering perturbative quantum gravity **perturbatively non-renormalizable**.

Simultaneously, the smooth continuum assumption inevitably produces:
- **Spacetime Singularities**: Penrose-Hawking theorems guarantee geodesic incompleteness and infinite curvature ($R \to \infty$) at the Big Bang and in black hole cores.
- **The Cosmological Constant Catastrophe**: Summing quantum zero-point energies yields $\rho_{\mathrm{vac}} \sim M_P^4 \approx 10^{74}\text{ GeV}^4$, which is $10^{120}$ times larger than the observed value $\rho_\Lambda \approx 2.7 \times 10^{-47}\text{ GeV}^4$.
- **The Black Hole Information Paradox**: Semi-classical thermal Hawking radiation breaks the unitarity of quantum mechanics.
- **The Measurement Problem**: Linear unitary Schrödinger evolution conflicts with non-unitary wavefunction collapse upon macroscopic detection.

---

## 2. Taxonomy of Candidate Frameworks Across 4 Historical Eras

Over the past five decades, theoretical physics has generated a diverse spectrum of proposals to resolve this crisis. These models can be grouped into four grand eras:

```
Era 1: Traditional Flagships (1970s–1990s)
├── Superstring Theory / M-Theory (10D/11D, SUSY, Braneworlds)
└── Canonical Loop Quantum Gravity (LQG) / Spin Foams (SU(2) Holonomies, Area Quantization)

Era 2: Discretizations, Fixed Points & Non-Commutativity (1990s–2000s)
├── Causal Dynamical Triangulations (CDT) (Lorentzian Regge Sums, ds = 2 -> 4)
├── Causal Sets (Discrete Posets, Causal Order)
├── Asymptotic Safety (Non-Gaussian UV Fixed Point, Wetterich RG Flow)
└── Connes' Noncommutative Geometry (Almost-Commutative Spectral Triples)

Era 3: Holographic, Entropic & Information-Theoretic Gravity (2000s–2010s)
├── Entropic / Thermodynamic Gravity (Jacobson, Verlinde)
└── Holographic Tensor Networks (AdS/CFT, MERA, HaPPY, ER = EPR)

Era 4: Contemporary Frontier Models (2013–2024)
├── Postquantum Gravity / Hybrid Classical-Quantum (Oppenheim, 2023)
├── Positive Geometries & The Amplituhedron (Arkani-Hamed et al., 2013–2024)
├── Wolfram Physics Project (Hypergraph Rewrite Systems, 2020)
└── Gauge-Gravity Double Copy (BCJ Duality: Gravity = Gauge^2)

The Unified Simplicial Paradigm
└── Unified Simplicial Quantum Gravity on Δ4 × Δ2 (Silva-Filho, 2024–2026)
```

---

## 3. Master Comparative Landscape Table

The table below contrasts the 11 candidate frameworks across key physical, mathematical, and epistemic criteria:

| Framework | Core Mathematical Ontology | Spacetime Dim | SM Matter Integration | Background Independence | Singularity Resolution | Free Parameter Count | Experimental Testability |
| :--- | :--- | :---: | :--- | :---: | :--- | :---: | :--- |
| **Superstring / M-Theory** | 1D strings, 2D worldsheets, p-branes | 10D / 11D | Tacked on via Calabi-Yau compactification | No (mostly perturbative on fixed backgrounds) | String size cutoff $\ell_s = \sqrt{\alpha'}$, but singularities remain in many vacua | $> 10^{500}$ (Anthropic Landscape) | Practically unfeasible (Planck desert $\sim 10^{19}\text{ GeV}$) |
| **Canonical LQG / Spin Foams** | $\mathrm{SU}(2)$ Ashtekar connections, spin networks | 4D | Difficult; coupled ad-hoc via fermions on graph vertices | Yes (strict canonical) | Resolved in LQC bounce; interior still debated in full 4D | $\ge 2$ ($\gamma_{\mathrm{BI}}$, $\Lambda$) + SM inputs | Inconclusive; Lorentz invariance violation bounds |
| **CDT (Causal Dyn. Triang.)** | Lorentzian simplicial path integrals $\sum e^{iS_{\mathrm{Regge}}}$ | 4D | Pure gravity; matter coupling numerically unstable | Yes | Quantum bounce observed in Monte Carlo ensemble | Cosmological parameters | Numerical bounds on spectral dimension |
| **Causal Sets** | Locally finite partially ordered sets (posets) | Emergent 4D | Unsolved; fermions require non-local discrete operators | Yes | Singularity replaced by discrete poset cutoff | Poisson intensity $\rho$ + SM inputs | Poissonian spacetime fluctuations (LIV) |
| **Asymptotic Safety** | Metric functional RG flow $\Gamma_k[g_{\mu\nu}]$ | 4D | Coupled via standard QFT action $\Gamma_k[g, A, \psi, \phi]$ | Partially (background field method) | Weakened by running Newton constant $G(k) \to 0$ | Finite set of UV critical exponents | Running of couplings; precision Higgs mass bounds |
| **Noncommutative Geometry** | Spectral triples $(\mathcal{A}, \mathcal{H}, \mathcal{D})$ | $4\mathrm{D} \times \text{finite}$ | Natural: SM gauge group derived from algebra $\mathcal{A}$ | Metric-independent spectral action | Regularizes Dirac operator; metric singularities unresolved | Standard Model Yukawa couplings | Unification scale relations (Higgs mass discrepancy) |
| **Entropic / Emergent Gravity** | Holographic screen thermodynamics & entanglement | Emergent 4D | Matter is primary; gravity is emergent thermodynamic gradient | Yes (relational) | Not fundamentally addressed at micro-scale | Standard thermodynamic variables | Galaxy rotation curves (MOND-like scaling) |
| **Postquantum Gravity (Oppenheim)** | Hybrid classical-quantum CPTP master equations | 4D | Classical metric coupled stochastically to quantum fields | Yes | Not resolved; classical curvature singularities remain | Diffusion constants $D_{\mu\nu\rho\sigma}$ | Laboratory precision interferometry (gravitational decoherence) |
| **Amplituhedron / Pos. Geom.** | Differential forms on Grassmannian polytopes | Momentum / Twistor space | Scattering amplitudes only; masses and symmetry breaking hard | Yes (dual conformal) | Singularity-free scattering (no Feynman divergences) | Couplings of planar $\mathcal{N}=4$ SYM | High-energy collider amplitude calculations |
| **Wolfram Physics Project** | Combinatorial hypergraph rewrite rules | Emergent integer/fractal | Conjectured; fermion chirality and gauge sectors unproven | Yes (purely combinatorial) | Causal graph continues through high-density events | Choice of rewrite rule $R$ | Microscopic discreteness noise |
| **Simplicial QG ($\Delta_4 \times \Delta_2$)** | Continuous Simplicial Beta-Laplacian $(-\Delta)^\alpha$ & Reach Ceiling $\kappa^*$ | $\Delta_4 \times \Delta_2$ (4D bulk + 2D flavor) | Exact: SM gauge group and 3 fermion generations derived from $\Delta_2$ | Yes (intrinsic simplicial foliation) | Deterministic quantum bounce via Planck pressure $P_{\mathrm{top}}$ | **3 fundamental constants** ($\hbar, c, \ell_P$); 0 arbitrary SM inputs | **5 near-term signatures** (LISA, LiteBIRD, MAGIS-100, $\nu_R$ line) |

---

## 4. Roadmap to the Thematic Comparative Modules

This comparative folder is organized into 7 specialized analytic documents:

1. **[`01_SIMPLICIAL_QG_VS_STRING_M_THEORY.md`](./01_SIMPLICIAL_QG_VS_STRING_M_THEORY.md)**: String Landscape vs. Simplicial Uniqueness, compactification vs. $\Delta_4 \times \Delta_2$, supersymmetries, and UV finiteness.
2. **[`02_SIMPLICIAL_QG_VS_LOOP_QUANTUM_GRAVITY.md`](./02_SIMPLICIAL_QG_VS_LOOP_QUANTUM_GRAVITY.md)**: Spin networks vs. simplicial continuous fields, the Barbero-Immirzi parameter, matter coupling, and the Hamiltonian constraint.
3. **[`03_SIMPLICIAL_QG_VS_CDT_AND_CAUSAL_SETS.md`](./03_SIMPLICIAL_QG_VS_CDT_AND_CAUSAL_SETS.md)**: Discrete path integrals vs. minimax variational actions, Monte Carlo sampling vs. analytical resolvents, and causal poset structures.
4. **[`04_SIMPLICIAL_QG_VS_ASYMPTOTIC_SAFETY_AND_NONCOMMUTATIVE_GEOMETRY.md`](./04_SIMPLICIAL_QG_VS_ASYMPTOTIC_SAFETY_AND_NONCOMMUTATIVE_GEOMETRY.md)**: Running couplings vs. running spectral dimensions, spectral triples vs. simplicial boundaries, and the Higgs sector.
5. **[`05_SIMPLICIAL_QG_VS_EMERGENT_AND_THERMODYNAMIC_GRAVITY.md`](./05_SIMPLICIAL_QG_VS_EMERGENT_AND_THERMODYNAMIC_GRAVITY.md)**: Jacobson-Verlinde entropic forces, AdS/CFT tensor networks (MERA, HaPPY), and holographic Mean Curvature Flow.
6. **[`06_SIMPLICIAL_QG_VS_CONTEMPORARY_FRONTIER_MODELS.md`](./06_SIMPLICIAL_QG_VS_CONTEMPORARY_FRONTIER_MODELS.md)**: In-depth confrontation with Oppenheim's Postquantum Gravity, Arkani-Hamed's Positive Geometries, Wolfram's Hypergraphs, and the BCJ Double Copy.
7. **[`07_MASTER_SCORECARD_AND_HONEST_LIMITATIONS.md`](./07_MASTER_SCORECARD_AND_HONEST_LIMITATIONS.md)**: The definitive 12-criterion scorecard, accompanied by an honest, peer-review examination of the open mathematical challenges, computational bottlenecks, and experimental hurdles facing the Simplicial Framework.
