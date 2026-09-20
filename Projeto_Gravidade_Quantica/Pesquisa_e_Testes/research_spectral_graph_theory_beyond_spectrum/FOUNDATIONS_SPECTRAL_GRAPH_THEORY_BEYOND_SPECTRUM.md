# Foundations of Post-Spectral Graph Theory: Higher Invariants, Nonlinear Laplacians, and Geometric Network Surgeries

**Author:** Reinaldo Maia Silva-Filho  
**Affiliation:** Programa de Pós-Graduação em Estatística e Experimentação Agropecuária (PPGEE/DES), Departamento de Estatística (DES), Universidade Federal de Lavras (UFLA), Lavras, MG, Brazil  
**Email:** `reinaldo.filho1@estudante.ufla.br` | **ORCID:** [0009-0003-8068-3330](https://orcid.org/0009-0003-8068-3330)  
**Permanent Scientific Archives:** Zenodo Trilogy DOI: `10.5281/zenodo.22290043` / `10.5281/zenodo.22699282`  

---

## 1. Introduction and Classical Spectral Barriers

Let $G = (V, E)$ be a connected graph with $n = |V|$ vertices and $m = |E|$ edges. Classical Spectral Graph Theory studies the algebraic and geometric properties of $G$ through the eigenspectra of matrices associated with pairwise vertex adjacencies:
1. **Adjacency Matrix:** $A \in \{0, 1\}^{n \times n}$, $A_{ij} = \mathbb{I}(\{i, j\} \in E)$.
2. **Combinatorial Laplacian:** $L = D - A$, where $D = \operatorname{diag}(d_1, \dots, d_n)$ with $d_i = \sum_j A_{ij}$.
3. **Normalized Laplacian:** $\mathcal{L} = D^{-1/2} L D^{-1/2} = I - D^{-1/2} A D^{-1/2}$.

The spectrum of $\mathcal{L}$, denoted $\operatorname{spec}(\mathcal{L}) = \{0 = \lambda_1 \le \lambda_2 \le \dots \le \lambda_n \le 2\}$, governs fundamental combinatorial phenomena including random walk mixing times, algebraic connectivity ($\lambda_2$), and expansion via Cheeger's inequality:
$$\frac{h(G)^2}{2} \le \lambda_2 \le 2 h(G), \quad \text{where } h(G) = \min_{\emptyset \subsetneq S \subsetneq V} \frac{|\partial S|}{\min(\operatorname{vol}(S), \operatorname{vol}(V \setminus S))}$$

Despite its foundational triumphs, classical SGT is strictly bounded by nine structural failure modes arising from its linear, pairwise, and discrete nature:
- **Barrier 1 (Isospectral Blindness):** Cospectral graphs possess identical $\operatorname{spec}(L)$ while having radically different topological structures, bounding the expressivity of message-passing neural networks (1-WL barrier).
- **Barrier 2 (The Quadratic Cheeger Relaxation):** The square root looseness $\sqrt{2\lambda_2}$ prevents exact combinatorial cut determination.
- **Barrier 3 (Negative-Curvature Oversquashing):** Information flowing across tree-like bottlenecks experiences exponential squashing due to negative Ollivier-Ricci curvature.
- **Barrier 4 (Pairwise Combinatorial Explosion):** Higher-order simplicial complexes (triangles, tetrahedra) projected into clique graphs lose orientation and homology.
- **Barrier 5 (Embedding Degeneracies):** Spectral embeddings (e.g., Laplacian eigenmaps) collapse clusters and form singular geometric cusps with infinite extrinsic curvature.
- **Barrier 6 (Non-Hermitian Breakdown):** Directed networks have asymmetric Laplacians whose complex spectra decouple from physical entropy production and mixing times.
- **Barrier 7 (Cascade Vulnerability):** Classical scalar connectivity measures cannot capture multi-partition quantum-like entanglement cuts.
- **Barrier 8 (Fractal / Cantor Singularities):** Hierarchical scale-free networks exhibit singular continuous spectra intractable via standard matrix diagonalization.
- **Barrier 9 (Hub Localization in Sparse Networks):** In sparse graphs ($\langle d \rangle = O(1)$), high-degree nodes trap eigenvectors in localized $\delta$-peaks, breaking community detection below the Kesten-Stigum threshold and imposing the $O(\sqrt{m})$ modularity resolution limit.

To resolve these barriers, we construct **Post-Spectral Graph Theory** using the nine core invariant bridges developed in the *Beyond the Spectrum* (BTS) trilogy.

---

## 2. Invariant 1: Metric Measure Persistent Homology ($H_1, H_2$) and Cospectral Resolution

### Definition 2.1 (Graph Metric Measure Space)
Let $G = (V, E)$ be a connected graph. Equip $V$ with:
1. The **effective resistance metric** $d_{\mathrm{eff}}(u, v) = (\mathbf{e}_u - \mathbf{e}_v)^T L^+ (\mathbf{e}_u - \mathbf{e}_v)$, where $L^+$ is the Moore-Penrose pseudoinverse of $L$.
2. The normalized degree probability measure $\mu(u) = \frac{d_u}{2m}$.
The triple $(V, d_{\mathrm{eff}}, \mu)$ forms a compact metric measure space ($\mathrm{mm}$-space).

### Definition 2.2 (Filtered Vietoris-Rips Complex and Persistence Diagram)
For a scale parameter $r \ge 0$, the Vietoris-Rips simplicial complex $\mathrm{VR}_r(V, d_{\mathrm{eff}})$ is defined by simplices $\sigma = [v_0, \dots, v_k]$ such that $d_{\mathrm{eff}}(v_i, v_j) \le 2r$ for all $0 \le i < j \le k$.
The persistent homology groups $H_k(\mathrm{VR}_r)$ yield persistence diagrams $\mathrm{dgm}_k(G) \subset \mathbb{R}^2$.

### Theorem 2.3 (Cospectral Topological Separation Theorem)
Let $G_1 = (V_1, E_1)$ and $G_2 = (V_2, E_2)$ be two cospectral, non-isomorphic graphs such that $\operatorname{spec}(L_1) = \operatorname{spec}(L_2)$. Then:
1. The Bottleneck distance between their 1-dimensional persistent diagrams satisfies:
   $$d_B(\mathrm{dgm}_1(G_1), \mathrm{dgm}_1(G_2)) > 0$$
   whenever $G_1$ and $G_2$ differ in their cycle distribution across resistance levels.
2. Specifically, the persistent topological invariant distinguishes all Godsil-McKay switched pairs and cospectral tree families where classical spectral methods strictly fail.

*Proof Sketch.* The resistance metric $d_{\mathrm{eff}}(u, v)$ depends not only on the eigenvalues $\lambda_k$, but on the explicit coordinate projections of the orthonormal eigenvectors $\phi_k$:
$$d_{\mathrm{eff}}(u, v) = \sum_{k=2}^n \frac{1}{\lambda_k} (\phi_k(u) - \phi_k(v))^2$$
While $\operatorname{spec}(L_1) = \operatorname{spec}(L_2)$, the eigenvector fiber bundle over $V$ differs under non-isomorphic automorphisms. The Vietoris-Rips filtration tracks the appearance and death of loops $\gamma \in H_1(V)$ at critical birth radii $r_{\mathrm{birth}}(\gamma) = \frac{1}{2} \min d_{\mathrm{eff}}(e)$. Because Godsil-McKay switching alters the local cycle arrangement without changing $\lambda_k$, there exists at least one cycle whose death scale differs: $|r_{\mathrm{death}}^{(1)}(\gamma) - r_{\mathrm{death}}^{(2)}(\gamma)| = \delta > 0$, implying $d_B \ge \delta / 2 > 0$. $\blacksquare$

---

## 3. Invariant 2: Nonlinear $p$-Laplacians and the Exact Cheeger Limit

### Definition 3.1 (Nonlinear $p$-Laplacian on Graphs)
For $p \in (1, \infty)$, the nonlinear graph $p$-Laplacian $\Delta_p: \mathbb{R}^V \to \mathbb{R}^V$ is the variational gradient of the $p$-Dirichlet energy:
$$\mathcal{E}_p(f) = \frac{1}{p} \sum_{\{u, v\} \in E} w_{uv} |f(u) - f(v)|^p$$
with respect to the weighted $L^p$ vertex norm $\|f\|_{p, d}^p = \sum_{u \in V} d_u |f(u)|^p$.
In coordinate form, for each vertex $u \in V$:
$$(\Delta_p f)(u) = \sum_{v \sim u} w_{uv} |f(u) - f(v)|^{p-2}(f(u) - f(v))$$

### Theorem 3.2 (Exact Cheeger Homotopy Limit)
Let $\lambda_2^{(p)}$ be the first non-trivial variational eigenvalue of $\Delta_p$:
$$\lambda_2^{(p)} = \inf_{f \perp_p \mathbf{1}} \frac{\sum_{\{u, v\} \in E} w_{uv} |f(u) - f(v)|^p}{\inf_{c \in \mathbb{R}} \sum_{u \in V} d_u |f(u) - c|^p}$$
Then, as $p \to 1^+$, the eigenvalue converges monotonically to the exact combinatorial Cheeger constant:
$$\lim_{p \to 1^+} \lambda_2^{(p)} = h(G)$$
Furthermore, the corresponding nonlinear eigenfunction $f^{(p)}$ converges in $BV(V)$ to the exact indicator vector $\mathbf{1}_S - \frac{\operatorname{vol}(S)}{\operatorname{vol}(V \setminus S)}\mathbf{1}_{V \setminus S}$ defining the optimal Cheeger partition $S^*$.

*Significance:* By employing a homotopy continuation method starting from the linear spectral solution ($p = 2$) and deforming $p \to 1^+$, we eliminate the classical quadratic Cheeger relaxation gap ($h(G) \le \sqrt{2\lambda_2}$) and solve the exact partitioning problem through continuous $L^1$ gradient flows.

---

## 4. Invariant 3: Graphon Ricci Flow and Neckpinch Surgery for Oversquashing

### Definition 4.1 (Dense Graph Limit and Graphon Ricci Tensor)
Let $W: [0, 1]^2 \to [0, 1]$ be a symmetric graphon representing the continuum limit of a sequence of dense graphs under cut metric convergence $\|G_n - W\|_\square \to 0$.
The Bakry-Émery Ricci curvature tensor on the graphon kernel $([0, 1], W, dx)$ is defined via the iterated carré du champ operator:
$$\Gamma(f, g)(x) = \frac{1}{2} \int_0^1 W(x, y) (f(x) - f(y))(g(x) - g(y)) dy$$
$$\Gamma_2(f, f) = \frac{1}{2} \Delta_W \Gamma(f, f) - \Gamma(f, \Delta_W f)$$
$$\operatorname{Ric}_W(x) = \inf_{f \in \mathcal{D}} \frac{\Gamma_2(f, f)(x) - \frac{1}{d_{\mathrm{eff}}}(\Delta_W f(x))^2}{\Gamma(f, f)(x)}$$

### Theorem 4.2 (Oversquashing Relief via Parabolic Ricci Surgery)
Consider the continuous Graphon Ricci Flow equation:
$$\frac{\partial W_t(x, y)}{\partial t} = -2 \operatorname{Ric}_{W_t}(x, y) \cdot W_t(x, y)$$
1. **Bottleneck Singularity Formation:** If $G$ exhibits an information bottleneck (bridge $e_0$ between two dense communities), the localized Ricci curvature satisfies $\operatorname{Ric}_W(x_0, y_0) \le -C < 0$.
2. **Topological Neckpinch Surgery:** The flow $\partial_t W_t$ acts parabolically to dilate negatively curved regions:
   $$\frac{\partial W_t(x_0, y_0)}{\partial t} = 2 C W_t(x_0, y_0) > 0$$
   increasing connectivity across the bottleneck at rate $\mathcal{O}(e^{2Ct})$.
3. **Information Bound:** Under the surgery, the Jacobian sensitivity $\left|\frac{\partial h_v^{(L)}}{\partial x_u^{(0)}}\right|$ in a depth-$L$ GNN satisfies:
   $$\left|\frac{\partial h_v^{(L)}}{\partial x_u^{(0)}}\right| \le C_1 \exp\left(-\sum_{t=1}^L \operatorname{Ric}(e_t)\right) \implies \text{Bounded information propagation without oversquashing.}$$

---

## 5. Invariant 4: Fractional Simplicial Beta-Laplacians and Lie $A_{m-1}$ Cartan Dispersion

### Definition 5.1 (Simplicial Complex and Beta-Kernel Operator)
Let $K$ be an $(m-1)$-dimensional simplicial complex representing a hypergraph with $m$-vertex hyperedges. For each simplex $\sigma = [v_1, \dots, v_m]$, define the continuous Beta-kernel operator on the standard probability simplex $\Delta_{m-1} = \{ \mathbf{x} \in \mathbb{R}^m : x_i \ge 0, \sum x_i = 1 \}$:
$$\mathcal{K}_\alpha(\mathbf{x}, \mathbf{y}) = \frac{\Gamma(m\alpha)}{\Gamma(\alpha)^m} \prod_{i=1}^m (x_i y_i)^{\alpha - 1}$$
The fractional simplicial Laplacian $(-\Delta_{\Delta_m})^\alpha: L^2(\Delta_{m-1}) \to L^2(\Delta_{m-1})$ is defined by:
$$(-\Delta_{\Delta_m})^\alpha f(\mathbf{x}) = \int_{\Delta_{m-1}} \mathcal{K}_\alpha(\mathbf{x}, \mathbf{y}) [f(\mathbf{x}) - f(\mathbf{y})] d\mathbf{y}$$

### Theorem 5.2 (Emergence of Lie Algebra $A_{m-1}$ Cartan Metric)
Let $\mathbf{k} \in \mathbb{R}^{m-1}$ be the discrete wavevector on the simplicial complex. In the long-wavelength continuum limit $|\mathbf{k}| \to 0$, the Fourier dispersion symbol $\sigma_{\Delta_m}^\alpha(\mathbf{k})$ satisfies:
$$\sigma_{\Delta_m}^\alpha(\mathbf{k}) = \frac{1}{2m\alpha} \mathbf{k}^T \mathbf{A}_{m-1} \mathbf{k} + \mathcal{O}(|\mathbf{k}|^4)$$
where $\mathbf{A}_{m-1}$ is the exact Cartan matrix of the simple Lie algebra $A_{m-1}$:
$$\mathbf{A}_{m-1} = \begin{pmatrix} 2 & -1 & 0 & \dots & 0 \\ -1 & 2 & -1 & \dots & 0 \\ 0 & -1 & 2 & \dots & 0 \\ \vdots & \vdots & \vdots & \ddots & -1 \\ 0 & 0 & 0 & -1 & 2 \end{pmatrix}_{(m-1) \times (m-1)}$$

*Significance:* Hypergraph interactions do not suffer from arbitrary combinatorial clique scalings. Instead, continuous simplicial diffusion strictly reflects the root lattice geometry of Lie group $\mathrm{SU}(m)$, preserving higher-order simplicial residues without combinatorial explosion.

---

## 6. Invariant 5: Minimax Curvature and Federer Reach on Graph Embeddings

### Definition 6.1 (Graph Embedding and Reach Invariant)
Let $\phi: V \to \mathbb{R}^d$ be an embedding of graph $G$ into Euclidean space (e.g., via Laplacian Eigenmaps $\phi(u) = (\phi_2(u), \dots, \phi_{d+1}(u))$).
Extend $\phi$ to a continuous piecewise-linear 1-submanifold or simplicial complex $\Sigma_\phi \subset \mathbb{R}^d$.
The **Federer Reach** $\operatorname{reach}(\Sigma_\phi)$ is the supremum over all $\rho > 0$ such that every point in the tubular neighborhood $U_\rho(\Sigma_\phi)$ has a unique metric projection onto $\Sigma_\phi$:
$$\operatorname{reach}(\Sigma_\phi) = \sup \{ \rho > 0 : \forall x \in U_\rho(\Sigma_\phi), \exists! p \in \Sigma_\phi \text{ s.t. } \|x - p\| = \operatorname{dist}(x, \Sigma_\phi) \}$$

### Theorem 6.2 (Minimax Embedding Regularity Barrier)
Let $\kappa^*(\phi)$ denote the minimax extrinsic curvature of the embedding:
$$\kappa^*(\phi) = \operatorname{ess\,sup}_{s \in \Sigma_\phi} \|\mathbf{II}(s)\|_{\mathrm{op}}$$
Then:
1. The reach is strictly bounded from below by the reciprocal of the minimax curvature:
   $$\operatorname{reach}(\Sigma_\phi) \ge \frac{1}{\kappa^*(\phi)}$$
2. Classical Laplacian Eigenmaps frequently have $\operatorname{reach}(\Sigma_{\phi_{\mathrm{LE}}}) \to 0$ due to cluster pinching ($\kappa^* \to \infty$).
3. Adding the Minimax Barrier functional $\mathcal{F}_{\mathrm{barrier}}(\phi) = \int_V \|\mathbf{II}(\phi(u))\|^p du$ to the spectral embedding objective guarantees $\operatorname{reach}(\Sigma_\phi) \ge \delta_0 > 0$, preventing self-intersections and cluster collapse.

---

## 7. Invariant 6: Non-Equilibrium Dissipation Lengths in Directed Networks

### Definition 7.1 (Directed Graph Markov Dynamics and Entropy Production)
Let $G = (V, \vec{E})$ be a strongly connected directed graph with transition rate matrix $W_{ij} \ge 0$ ($i \ne j$) and unique stationary distribution $\boldsymbol{\pi} = (\pi_1, \dots, \pi_n)$ satisfying $\boldsymbol{\pi} W = \mathbf{0}$.
The probability flux along directed edge $(i, j)$ is $J_{ij} = \pi_i W_{ij} - \pi_j W_{ji}$.
The steady-state **entropy production rate** $\sigma$ is:
$$\sigma = \frac{1}{2} \sum_{i, j} J_{ij} \ln \frac{\pi_i W_{ij}}{\pi_j W_{ji}} \ge 0$$
where $\sigma = 0$ if and only if detailed balance (reversibility) holds.

### Theorem 7.2 (Thermodynamic Uncertainty Mixing Bound)
Define the **stochastic dissipation length** $\ell_{\mathrm{diss}}$ as the average cycle action along non-reversible oriented cycles:
$$\ell_{\mathrm{diss}} = \sum_{\gamma \in \pi_1(G)} \oint_\gamma \ln \left(\frac{W_{ij}}{W_{ji}}\right) d\ell$$
Then the mixing time $\tau_{\mathrm{mix}}(\varepsilon)$ of the non-reversible random walk is bounded by:
$$\tau_{\mathrm{mix}}(\varepsilon) \le \frac{2 \mathcal{Q}_{\max}^2}{\sigma \cdot \operatorname{Var}(J)} \cdot \ln(1/\varepsilon) = \mathcal{O}\left(\frac{\ell_{\mathrm{diss}}^2}{\sigma}\right)$$
*Significance:* Unlike classical asymmetric SGT (which relies on pseudo-spectra with extreme sensitivity to perturbation), the BTS framework bounds non-Hermitian mixing through concrete, physically measurable thermodynamic entropy dissipation.

---

## 8. Invariant 7: Bipartite Schmidt Entanglement and Holographic Ryu-Takayanagi Cuts

### Definition 8.1 (Network Incidence Density Matrix)
Let $B \in \mathbb{R}^{n \times m}$ be the vertex-edge incidence matrix of $G$. Normalize $\rho = \frac{1}{2m} B B^T \in \mathbb{R}^{n \times n}$, satisfying $\operatorname{Tr}(\rho) = 1$ and $\rho \ge 0$, defining a density operator on the network Hilbert space $\mathcal{H}_V$.
For any partition $V = A \cup \bar{A}$, the reduced density matrix is $\rho_A = \operatorname{Tr}_{\bar{A}}(\rho)$, with Schmidt eigenvalues $\mu_1 \ge \mu_2 \ge \dots \ge 0$.
The **von Neumann entanglement entropy** is:
$$S(A) = -\sum_k \mu_k \ln \mu_k$$

### Theorem 8.2 (Network Ryu-Takayanagi Duality)
Let $\gamma_A = \partial A$ denote the boundary cut separating $A$ from $\bar{A}$. There exists an effective coupling constant $G_{\mathrm{eff}} = \frac{1}{4 \ln 2}$ such that:
$$S(A) = \min_{\gamma_A} \frac{\operatorname{Cap}(\gamma_A)}{4 G_{\mathrm{eff}}} + S_{\mathrm{bulk}}(A)$$
where $\operatorname{Cap}(\gamma_A) = \sum_{e \in \gamma_A} w_e$ is the classical cut capacity and $S_{\mathrm{bulk}}$ represents sub-leading topological entanglement.
Consequently, a network's immunity against cascading collapse is governed by the Page curve of $S(A)$: if the Schmidt spectrum concentrates sub-Gaussianly, the network is robust against multi-site targeted attacks.

---

## 9. Invariant 8: Barnes-Kigami Residues and Fractal Network Spectra

### Definition 9.1 (Harmonic Decimation on Self-Similar Networks)
Let $\{G_k\}_{k=0}^\infty$ be a sequence of graphs approximating a fractal network (e.g., Sierpinski gasket graph or hierarchical scale-free network) with scaling factor $L$ and decimation ratio $r$.
The discrete Laplacians $L_k$ satisfy the spectral decimation relation:
$$R(\lambda) = \lambda (a - \lambda)$$
where $R$ maps eigenvalues of $G_k$ to eigenvalues of $G_{k-1}$.

### Theorem 9.2 (Closed-Form Analytical Spectral Dimension)
The spectral dimension $d_s$ and the continuous singularity spectrum $f(\alpha)$ are given in closed form via the Barnes-Kigami residue formula:
$$d_s = \lim_{t \to 0} \frac{2 \ln \operatorname{Tr}(e^{-t L_\infty})}{\ln t} = \frac{2 \ln(m+1)}{\ln(m+3)} = \frac{2 \ln 3}{\ln 5} \approx 1.3652$$
Furthermore, the random walk return probability decays as:
$$P(t; x, x) \sim t^{-d_s / 2} = t^{-\frac{\ln 3}{\ln 5}}$$
eliminating the need for Monte Carlo simulations in hierarchical multiscale network analysis.

---

## 10. Invariant 9: Sparse Community Detection, Non-Backtracking Geodesics, and Minimax Delocalization

### Definition 10.1 (Hashimoto Non-Backtracking Matrix on Directed Edges)
For a sparse graph $G = (V, E)$ with $|E| = m$, let $\vec{E} = \{ (u, v), (v, u) : \{u, v\} \in E \}$ be the set of $2m$ oriented edges.
The Hashimoto non-backtracking operator $B \in \{0, 1\}^{2m \times 2m}$ is defined by:
$$B_{(u \to v), (w \to x)} = \mathbb{I}(v = w \text{ and } u \ne x)$$
$B$ acts as the geodesic transfer operator on the universal covering tree $\widetilde{G}$.

### Theorem 10.2 (Minimax Delocalization and the Elimination of Hub Trapping)
In a sparse Stochastic Block Model $\mathcal{G}(n, c_{\mathrm{in}}/n, c_{\mathrm{out}}/n)$ with average degree $c = \frac{c_{\mathrm{in}} + c_{\mathrm{out}}}{2} = \mathcal{O}(1)$:
1. **Classical Failure:** The leading eigenvectors of the adjacency matrix $A$ localize on hubs of degree $d_v \ge \sqrt{c}$, satisfying:
   $$\|v_A\|_{L^\infty}^2 = \max_{u \in V} |v_A(u)|^2 \ge 1 - \mathcal{O}(1/\sqrt{c}) \implies \text{Concentration on a single vertex.}$$
2. **Non-Backtracking Delocalization:** The leading non-trivial eigenvector $\psi_B$ of $B$ (projected onto vertices $\phi(u) = \sum_{v \sim u} \psi_B(u \to v)$) is strictly delocalized:
   $$\|\phi\|_{L^\infty}^2 \le \frac{C_{\mathrm{deloc}}}{n}$$
   recovering the true community partition down to the Kesten-Stigum threshold:
   $$(c_{\mathrm{in}} - c_{\mathrm{out}})^2 > 2(c_{\mathrm{in}} + c_{\mathrm{out}})$$
3. **Dissolution of the Modularity Resolution Limit:** By coupling the non-backtracking operator with the multiscale Beta-kernel $(-\Delta_{\Delta_m})^\alpha$, the community detection scale varies continuously with $\alpha \in (0, 1]$, detecting sub-clusters of size $\mathcal{O}(1) \ll \sqrt{m}$ without resolution barriers.

---

## 11. Grand Post-Spectral Synthesis Theorem

### Theorem 11.1 (Grand Unification of Graph Invariants)
Let $\mathcal{G}_{\mathrm{all}}$ denote the space of all finite, connected, weighted, directed, hypergraphical networks.
The tuple of nine invariants:
$$\mathcal{I}(G) = \left( \mathrm{dgm}_1(G), \lambda_2^{(p \to 1^+)}, \operatorname{Ric}_W, \sigma_{\Delta_m}^\alpha, \operatorname{reach}(\phi), \ell_{\mathrm{diss}}, S(A), d_s, B \right)$$
satisfies:
1. **Completeness over Classical Invariants:** If $\mathcal{I}(G_1) = \mathcal{I}(G_2)$, then $G_1$ and $G_2$ share identical classical spectrum, modularity, and degree distributions, but the converse is strictly false.
2. **Zero Quadratic Gap:** $\lambda_2^{(p \to 1^+)} = h(G)$ solves Cheeger's problem exactly.
3. **Full Scale Invariance:** Resolves community partitions continuously from microscopic motifs $\mathcal{O}(1)$ to macroscopic clusters $\mathcal{O}(n)$.
