# Universal Discrete Structures: Canonical Arithmetization, Functorial Embeddings, and Master Invariant Tuples

**Author:** Reinaldo Maia Silva-Filho (PPGEE / DES / ABI / UFLA)  
**Date:** September 2026  
**Status:** Canonical Foundation & Rigorous Implementation Suite  

---

## Abstract

We establish the **Universal Arithmetization Framework** for discrete mathematics, constructing a faithful, canonical functor:
$$\mathfrak{U} : \mathbf{DiscStruct} \longrightarrow \mathbb{N}_{\ge 1}$$
from the mega-category of finite discrete structures modulo isomorphism to the positive natural numbers. We systematically unify nine foundational domains:
1. **Matrices** $\mathcal{M}_{m \times n}(\mathbb{Z})$ under elementary equivalence, similarity, and congruence (Smith Normal Form, Hermite Normal Form, Rational Canonical Form).
2. **Graphs & Hypergraphs** $\mathcal{H}_{n, r}$ under permutation orbits (Post-Spectral Invariant Sieve, Ryu--Takayanagi multiscale cut capacities, and Chen non-Abelian holonomies).
3. **Higher-Order Tensors & Hypertensors** $\mathcal{T} \in \mathbb{R}^{n_1 \times \dots \times n_d}$ (HOSVD multilinear ranks, Cayley $2 \times 2 \times 2$ Hyperdeterminants, and Lim--Qi $H$-/$Z$-eigenvalues).
4. **Knots, Links, and Braids** $\mathcal{K}$ up to ambient isotopy (Planar Diagrams, Tait signed medial graphs, Seifert matrices, Alexander--Conway and Jones polynomials).
5. **Finite Topological Spaces & Posets** $\mathbf{FinTop}_0 \cong \mathbf{FinPoset}$ under homeomorphism/order-isomorphism (Alexandroff specialization preorders, Birkhoff distributive lattices, and incidence Möbius functions).
6. **Abstract Simplicial Complexes** $\mathbf{SimpComp}$ (face lattices, Stanley--Reisner rings, and $f$-/$h$-polynomials).
7. **Matroids & Combinatorial Geometries** $\mathbf{Matroid}$ (bases, circuits, geometric lattices, and Tutte polynomials).
8. **Finite Groups & Permutations** $\mathbf{FinGroup}$ (Cayley color digraphs, character tables, and Robinson--Schensted--Knuth Young tableaux).
9. **The Universal Digital Fingerprint of Natural Numbers** $\mathcal{D}(N)$ mapping each $N \in \mathbb{N}_{\ge 1}$ simultaneously to its arithmetic, spectral, post-spectral, tensor, and generating function avatars.

---

## 1. Categorical Architecture: The Grand Unified Web

The fundamental commutative diagram connecting all discrete categories through the canonical graph hub $\mathbf{FinGraph}$ and natural numbers $\mathbb{N}_{\ge 1}$ is:

```
                  ┌────────────────────────┐
                  │    MATRICES (M)        │
                  │   & HYPERTENSORS (T)   │
                  │ (Smith/Hermite/Cayley) │
                  └───────────┬────────────┘
                              │ Bipartite / HOSVD Unfoldings
                              ▼
  ┌─────────────────┐    ┌────────────────┐    ┌──────────────────┐
  │  KNOTS / LINKS  │───>│     FINITE     │<───│ FINITE TOPOLOGIES│
  │ (Tait / Seifert)│    │   GRAPHS (G)   │    │  (Alexandroff)   │
  └─────────────────┘    └────────┬───────┘    └──────────────────┘
                              ▲   │
        Simplicial Chains /   │   │ Adaptive Invariant Sieve /
        Incidence Hypergraph  │   │ Dyadic Arithmetization
                              │   ▼
                   ┌──────────┴───────────┐
                   │   NATURAL NUMBERS    │
                   │  Phi(X) in N_{>=1}   │
                   │ (Sabidussi-Cartesian)│
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  UNIVERSAL DIGITAL   │
                   │   FINGERPRINT D(N)   │
                   │ (Spec + Post-Spec +  │
                   │  Tensor + Zeta Fn)   │
                   └──────────────────────┘
```

---

## 2. Canonical Domain Bridges

### 2.1 Bridge 1: Matrices $\longleftrightarrow$ Graphs $\longleftrightarrow$ Numbers
Let $M \in \mathbb{Z}^{m \times n}$.
1. **Canonical Forms:**
   - Equivalence under unimodular transformations $P M Q = S$: **Smith Normal Form** $\operatorname{SNF}(M) = \operatorname{diag}(s_1, \dots, s_k, 0, \dots, 0)$ where $s_i \mid s_{i+1}$.
   - Row equivalence: **Hermite Normal Form** $\operatorname{HNF}(M)$.
   - Similarity over a field $P M P^{-1} = C$: **Rational Canonical Form (Frobenius)** $\bigoplus C(p_i(t))$.
2. **Canonical Graph Functor $\mathfrak{G}_{\text{Mat}}(M)$:**
   - Bipartite vertex set $V = \{u_1, \dots, u_m\} \sqcup \{v_1, \dots, v_n\}$ with signed weighted edges $M_{ij}$.
   - Coates Signal-Flow Digraph $D(M)$ whose cycle weight polynomials generate $\det(M)$ and $\operatorname{perm}(M)$.
3. **Canonical Tuple & Generating Function:**
   $$\mathcal{T}_{\text{Mat}}(M) = \left( \operatorname{SNF}(M), \; p_M(t) = \det(t I - M), \; \operatorname{Tr}(M^k)_{k=1}^n, \; \operatorname{perm}(M) \right)$$
   $$\mathcal{Z}_M(t) \coloneqq \exp\left( \sum_{k=1}^\infty \frac{\operatorname{Tr}(M^k)}{k} t^k \right) = \frac{1}{\det(I - t M)}.$$

---

### 2.2 Bridge 2: Higher-Order Tensors & Hypertensors
Let $\mathcal{T} \in \mathbb{R}^{n_1 \times n_2 \times \dots \times n_d}$ be a tensor of order $d \ge 3$.
1. **HOSVD and Multilinear Ranks:**
   - Mode-$n$ matricization (unfolding) $\mathcal{T}_{(n)} \in \mathbb{R}^{n_n \times \prod_{j \ne n} n_j}$.
   - The **multilinear rank tuple** $\mathbf{r} = (r_1, r_2, \dots, r_d)$ where $r_n = \operatorname{rank}(\mathcal{T}_{(n)})$.
2. **Cayley's $2 \times 2 \times 2$ Hyperdeterminant $\operatorname{Det}(\mathcal{T})$:**
   - For $a_{ijk} \in \mathbb{R}$ ($i, j, k \in \{0, 1\}$), Arthur Cayley (1845) discovered the fundamental $\operatorname{SL}_2 \times \operatorname{SL}_2 \times \operatorname{SL}_2$ invariant of degree 4:
     $$\begin{aligned}
     \operatorname{Det}(\mathcal{T}) &= a_{000}^2 a_{111}^2 + a_{001}^2 a_{110}^2 + a_{010}^2 a_{101}^2 + a_{011}^2 a_{100}^2 \\
     &\quad - 2\big( a_{000} a_{001} a_{110} a_{111} + a_{000} a_{010} a_{101} a_{111} + a_{000} a_{011} a_{100} a_{111} \\
     &\quad\qquad + a_{001} a_{010} a_{101} a_{110} + a_{001} a_{011} a_{100} a_{110} + a_{010} a_{011} a_{100} a_{101} \big) \\
     &\quad + 4\big( a_{000} a_{011} a_{101} a_{110} + a_{001} a_{010} a_{100} a_{111} \big).
     \end{aligned}$$
   - **Quantum Entanglement Separation:** In tripartite quantum state geometry, $\operatorname{Det}(\mathcal{T})$ is the **3-tangle** $\tau(A:B:C)$, strictly separating the maximally entangled GHZ state ($\operatorname{Det}(\mathcal{T}_{\text{GHZ}}) = 0.25 > 0$) from the W state ($\operatorname{Det}(\mathcal{T}_{\text{W}}) = 0.00$).
3. **Lim--Qi Hypergraph Tensor Eigenvalues:**
   For an $r$-uniform hypergraph $H$, its symmetric adjacency tensor $\mathcal{A}$ satisfies the eigenvalue equation:
   $$\mathcal{A} x^{r-1} = \lambda x^{[r-1]}, \quad (\mathcal{A} x^{r-1})_i \coloneqq \sum_{i_2, \dots, i_r} \mathcal{A}_{i, i_2, \dots, i_r} x_{i_2} \dots x_{i_r}.$$
4. **Canonical Tuple & Arithmetization:**
   $$\mathcal{T}_{\text{Tensor}}(\mathcal{T}) = \left( \operatorname{shape}(\mathcal{T}), \ \|\mathcal{T}\|_F, \ \mathbf{r}_{\text{multilinear}}, \ \operatorname{Det}_{2\times 2\times 2}(\mathcal{T}), \ \operatorname{Tr}_{\text{slices}}(\mathcal{T}) \right)$$
   $$\Phi_{\text{Tensor}}(\mathcal{T}) \in \mathbb{N}_{\ge 1}.$$

---

### 2.3 Bridge 3: Knots, Links & Braids $\longleftrightarrow$ Graphs $\longleftrightarrow$ Numbers
Let $K$ be an oriented knot or link in $S^3$.
1. **Planar Diagram & Tait Signed Graph:**
   - Checkerboard 2-coloring of regions yields the **Tait Medial Graph** $G_T(K)$ with crossing signs $\pm 1$.
2. **Seifert Surface & Matrix:**
   - Bilinear linking pairings on homology basis define the **Seifert Matrix** $V \in \mathbb{Z}^{2g \times 2g}$.
3. **Canonical Invariant Tuple:**
   $$\mathcal{T}_{\text{Knot}}(K) = \left( \operatorname{det}(K) = |\det(V + V^T)|, \ \Delta_K(t) = \det(V - t V^T), \ V_K(q), \ \operatorname{signature}(V + V^T) \right).$$

---

### 2.4 Bridge 4: Finite Topological Spaces $\longleftrightarrow$ Posets $\longleftrightarrow$ DAGs
Let $(X, \tau)$ be a finite topological space.
1. **The Alexandroff Correspondence Theorem:**
   - Finite $T_0$ spaces are strictly isomorphic to finite posets $(X, \le)$ via specialization preorder:
     $$\mathbf{FinTop}_0 \cong \mathbf{FinPoset}.$$
2. **Incidence Algebra & Möbius Inversion:**
   - Zeta Matrix $\zeta(x, y) = \mathbb{I}(x \le y)$ and Möbius matrix $\mu = \zeta^{-1}$.
3. **Canonical Tuple:**
   $$\mathcal{T}_{\text{Top}}(X) = \left( |X|, \ |\tau|, \ \operatorname{Tr}(\mu), \ \sum \mu, \ \mathbf{f}(\Delta(P)) \right).$$

---

### 2.5 Bridge 5: Simplicial Complexes $\longleftrightarrow$ Matroids $\longleftrightarrow$ Numbers
1. **Simplicial Complexes $\Delta$:**
   - $f$-vector $\mathbf{f}(\Delta) = (f_0, \dots, f_d)$, $h$-vector $\mathbf{h}(\Delta)$, and Euler characteristic $\chi(\Delta) = \sum (-1)^i f_i$.
2. **Matroids $M = (E, \mathcal{B})$:**
   - Universal Tutte polynomial $T_M(x, y) = \sum (x-1)^{r(E)-r(A)} (y-1)^{|A|-r(A)}$.
   - $\mathcal{T}_{\text{Matroid}}(M) = (|E|, r(M), |\mathcal{B}|, T_M(1, 0), T_M(0, 1))$.

---

### 2.6 Bridge 6: Finite Groups & Combinatorics
- Finite Groups $G$: Cayley tables, conjugacy classes, element orders, and Molien series:
  $$M_G(t) = \frac{1}{|G|} \sum_{g \in G} \frac{1}{\det(I - t \rho(g))}.$$
- Permutations: Lehmer factoradic codes and Robinson--Schensted--Knuth (RSK) Young tableaux.

---

## 3. The Master Digital Fingerprint of Natural Numbers $\mathcal{D}(N)$

Every positive integer $N \in \mathbb{N}_{\ge 1}$ is decoded via the inverse dyadic map $\Phi^{-1}(N) = (b_1, \dots, b_k) \in \{0, 1\}^*$ into a canonical combinatorial graph $G_N$, adjacency matrix $A_N$, and hypertensor $\mathcal{T}_N$.

The **Universal Digital Fingerprint** $\mathcal{D}(N)$ is the structured master tuple:

$$\mathcal{D}(N) \coloneqq \Big\langle \operatorname{Arith}(N), \ \operatorname{Spec}(G_N), \ \operatorname{PostSpec}(G_N), \ \operatorname{Tensor}(\mathcal{T}_N), \ \mathbf{\mathcal{Z}}_N \Big\rangle$$

### 3.1 Components of the Digital Fingerprint

1. **Arithmetic Avatar $\operatorname{Arith}(N)$:**
   - Prime factorization: $N = p_1^{a_1} \dots p_m^{a_m}$;
   - Number of divisors $d(N)$, sum of divisors $\sigma(N)$, Euler totient $\varphi(N)$.
2. **Matrix Spectral Avatar $\operatorname{Spec}(G_N)$:**
   - Adjacency spectrum: $\spec(A_N) = (\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_n)$;
   - Laplacian spectrum: $\spec(L_N) = (0 = \mu_1 \le \mu_2 \le \dots \le \mu_n)$;
   - Fiedler algebraic connectivity gap: $\mu_2(G_N)$;
   - Total spectral energy: $E(G_N) = \sum_{i=1}^n |\lambda_i|$.
3. **Post-Spectral Avatar $\operatorname{PostSpec}(G_N)$ (Beyond the Spectrum):**
   - Multiscale cut capacities: $\min_{|S|=k} |\partial S|$;
   - Non-Abelian Chen iterated path integral holonomy $\mathcal{I}_{\text{Chen}}(G_N)$;
   - 1D Persistent Homology Betti cycle count $\beta_1(G_N) = |E| - |V| + 1$.
4. **Hypertensor Avatar $\operatorname{Tensor}(\mathcal{T}_N)$:**
   - Canonical 3-tensor $\mathcal{T}_N \in \mathbb{R}^{2 \times 2 \times 2}$ constructed from the bitstring of $N$;
   - HOSVD multilinear ranks $(r_1, r_2, r_3)$;
   - Cayley Hyperdeterminant $\operatorname{Det}_{2\times 2\times 2}(\mathcal{T}_N)$ (3-tangle).
5. **The Function Constellation $\mathbf{\mathcal{Z}}_N$ (Families of Generating Functions):**
   - Characteristic polynomial: $p_N(t) = \det(t I - A_N)$;
   - Ihara Zeta Function: $\zeta_{G_N}(u) = (1-u^2)^{-\chi(G_N)} \det(I - A_N u + Q u^2)^{-1}$;
   - Local Riemann--Dirichlet seed: $D_N(s) = \sum_{d \mid N} d^{-s}$;
   - Additive partition factor: $P_N(q) = \prod_{k=1}^N (1 - q^k)^{-1}$.

---

## 4. Master Invariant Tuples Across All Domains

| Object Domain $X$ | Canonical Invariant Tuple $\mathcal{T}(X)$ | Canonical Generating Function $\mathcal{Z}_X(t)$ |
| :--- | :--- | :--- |
| **Natural Number $N \in \mathbb{N}_{\ge 1}$** | $\mathcal{D}(N) = (\text{Arith}, \spec(A), \spec(L), \text{PostSpec}, \operatorname{Det}(\mathcal{T}))$ | Ihara $\zeta_{G_N}(u)$ & Dirichlet $D_N(s) = \sum_{d \mid N} d^{-s}$ |
| **Hypertensor $\mathcal{T} \in \mathbb{R}^{n_1 \times \dots \times n_d}$** | $(\operatorname{shape}, \|\mathcal{T}\|_F, \mathbf{r}_{\text{HOSVD}}, \operatorname{Det}_{2\times 2\times 2}, \operatorname{Tr}_{\text{slices}})$ | Characteristic tensor eigenvalue polynomial |
| **Matrix $M \in \mathbb{Z}^{m \times n}$** | $(\operatorname{SNF}(M), \spec(M M^T), \det(M), \operatorname{Tr}(M^k)_{k=1}^4)$ | $\mathcal{Z}_M(t) = \det(I - t M)^{-1}$ |
| **Graph $G = (V, E)$** | $(\spec(A), \spec(L), \mathcal{I}_{\text{Chen}}(G), \mathcal{S}_{\le r}(G), \operatorname{Aut}(G))$ | Ihara Zeta $\zeta_G(u) = (1-u^2)^{-\chi(G)} \det(I - A u + Q u^2)^{-1}$ |
| **Knot $K \subset S^3$** | $(\Delta_K(t), V_K(q), \operatorname{det}(K), \operatorname{sig}(K), \operatorname{Vol}_{\text{hyp}})$ | Alexander-Conway $\sum a_n z^n = \nabla_K(z)$ |
| **Poset / Topology $P$** | $(|P|, \mu_P, \operatorname{Tr}(\mu), \sum \mu, \mathbf{f}(\Delta(P)))$ | Zeta polynomial $Z_P(n) = \sum e_k(P) \binom{n}{k}$ |
| **Simplicial Complex $\Delta$** | $(\mathbf{f}(\Delta), \mathbf{h}(\Delta), \chi(\Delta), \beta_0, \beta_1, \dots)$ | Hilbert Series $H(\Delta; t) = \sum h_i t^i / (1-t)^d$ |
| **Matroid $M$** | $(|E|, r(M), |\mathcal{B}|, T_M(1, 0), T_M(0, 1))$ | Tutte Polynomial $T_M(x, y)$ |
| **Finite Group $G$** | $(|G|, \text{Abelian?}, \text{Classes}(G), \text{Orders}(G))$ | Molien Series $M_G(t) = \frac{1}{\|G\|} \sum \det(I - t \rho(g))^{-1}$ |

---

## 5. Sabidussi--Vizing Graph Arithmetic on All Discrete Structures

Because the Cartesian product of connected graphs $G_1 \mathbin{\square} G_2$ is associative, commutative, and has $K_1$ as unique identity:
$$\mathbf{FinGraph}_{\text{conn}} / {\cong} \;\cong\; \bigoplus_{P \in \mathcal{P}_{\text{Sabidussi}}} \mathbb{N}.$$

Under the Grand Gödel--Sabidussi Functor:
$$\Psi(P_1^{e_1} \mathbin{\square} \dots \mathbin{\square} P_k^{e_k}) \coloneqq \prod_{i=1}^k p_{\Phi(P_i)}^{e_i} \in \mathbb{N}_{\ge 1},$$
every discrete structure (matrix, hypertensor, knot, topology, matroid, group) inherits a **unique prime factorization**!
