# B: superconducting coherence on fractal networks via the spectral dimension

## Physical problem
Granular superconductors, Josephson-junction arrays and percolating films have fractal or network geometry. Superconductivity requires long-range phase coherence, that is, the breaking of a continuous U(1) symmetry.

## Known ingredients (check each)
- **A generalized Mermin–Wagner theorem on graphs** (Cassi; Burioni–Cassi–Vezzani): continuous symmetries break spontaneously only on "transient on average" graphs. For "regular" fractals this means d_s > 2. This is the statement to confirm, including its precise hypotheses.
- **Experiments** with Josephson-junction arrays on Sierpinski gaskets (Gordon, Goldman, Whitehead: PRL 56, 2280 (1986); PRL 59, 2311 (1987); confirmed via Crossref in `literatura.md`).
- **Flat bands.** Fractal lattices have highly degenerate localized eigenstates. In a flat band the superfluid weight is controlled by the quantum metric (Peotta–Törmä 2015), and T_c can grow linearly with the coupling. *Confirm.*
- The Sierpinski gasket has d_s = 2 log 3 / log 5 ≈ 1.365 < 2, so no coherence is expected at T > 0. The Sierpinski carpet and other fractals can have d_s > 2.

## Link to the book
- ch. 6: Kigami Laplacian, spectral decimation, the d_s law, Γ-convergence of discretizations.
- ch. 12: heat kernel and return probability, P(τ) ~ τ^{−d_s/2}.

The contribution would be a **criterion** of the form: "network family X admits (or does not admit) superconducting coherence, with d_s computed exactly by spectral decimation or by the book's methods", plus predictions of how T_c or the superfluid stiffness scales with the fractal generation.

## Questions
1. What exactly does Cassi's theorem require (recurrence on average, bounded degree)? Does it apply to the XY model and hence to Josephson arrays?
2. Which fractal families with d_s > 2 are realizable (3D carpets, Menger sponge, fractals built in cold atoms or photonic lattices)?
3. For d_s slightly above 2, how does the stiffness scale? Is there a formula in d_s?
4. Flat bands of fractals plus the quantum metric: is there a T_c prediction for fractal lattices that can be tested (cold atoms, electronic circuits, photonic lattices)?

## Steps
1. Literature (sonnet agent): `literatura.md`.
2. Numerics: the XY model on the Sierpinski gasket and carpet (Monte Carlo or harmonic spin waves), compared with the d_s prediction. The oracle is spectral decimation for the gasket; the negative control is the square lattice (d_s = 2, BKT).
3. If a regime appears that nobody has explored: formulate and prove it.
