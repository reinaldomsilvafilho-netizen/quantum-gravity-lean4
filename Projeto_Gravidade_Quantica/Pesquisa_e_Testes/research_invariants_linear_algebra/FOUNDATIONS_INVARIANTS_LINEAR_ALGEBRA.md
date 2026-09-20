# Foundations of Geometric Invariants in Linear Algebra & Tensor Analysis

**Author**: Reinaldo M. Silva-Filho  
**Affiliation**: Programa de Pós-Graduação em Estatística e Experimentação Agropecuária (PPGEE/DES), Departamento de Estatística (DES), Universidade Federal de Lavras (UFLA), Lavras, MG, Brazil  
**Funding**: CAPES Finance Code 001  

---

## 1. Motivation: The Geometric Invariant Paradigm

Classical Numerical Linear Algebra (NLA) formulates algorithms in flat Euclidean matrix spaces $\mathbb{R}^{m \times n}$ equipped with the Frobenius norm $\|\mathbf{A}\|_F = \sqrt{\operatorname{tr}(\mathbf{A}^T \mathbf{A})}$. However, fundamental linear algebraic structures are intrinsically non-Euclidean:
1. **Low-rank matrices and tensors** form stratified algebraic varieties $\mathcal{M}_{\le r}$ whose singular boundaries exhibit positive normal reach $\mu > 0$.
2. **Positive-definite covariance and metric matrices** $\mathcal{S}_{++}^m$ form a non-positively curved symmetric Cartan-Hadamard Riemannian manifold under the Fisher-Rao / Affine-Invariant metric $ds^2 = \operatorname{tr}((\mathbf{A}^{-1} d\mathbf{A})^2)$.
3. **Continuous operators and multilinear mappings** reside on continuous functional Hilbert spaces, where discrete tensor contractions are continuous tensor-trains (cTT / cMPS) with gauge invariance under $\operatorname{GL}(r_k)$.
4. **Graph and manifold Laplacians** with zero-modes require non-local Simplicial Beta-kernel resolvents $((-\Delta_{\Delta_m})^\alpha + \lambda \mathbf{I})^{-1}$ to preserve exact global mass conservation.
5. **Non-Hermitian ill-conditioned linear systems** with multiply-connected spectra in $\mathbb{C} \setminus \{0\}$ undergo condition relief $\kappa_H^* = \sqrt{(\kappa_E^*)^2 - |c|^2}$ when foliated into negative-curvature space forms $(\mathbb{H}^n, g_c)$, unrolling Krylov stagnation via universal covering spaces $\widetilde{\Omega}$.

---

## 2. Pillar I: The Steiner-Federer Lipschitz-Continuous Pseudoinverse ($\mathbf{A}_\mu^\dagger$)

### 2.1 The Classical Discontinuity of the Moore-Penrose Inverse
The classical Moore-Penrose pseudoinverse $\mathbf{A}^\dagger = \mathbf{V} \boldsymbol{\Sigma}^\dagger \mathbf{U}^T$ is inherently discontinuous across rank boundaries. Specifically, if $\mathbf{A} \in \mathbb{R}^{m \times n}$ has rank $r$ and singular values $\sigma_1 \ge \dots \ge \sigma_r > 0$, a perturbation $\mathbf{E}$ of size $\|\mathbf{E}\|_2 = \varepsilon \to 0$ can yield:
$$\|(\mathbf{A} + \mathbf{E})^\dagger - \mathbf{A}^\dagger\|_2 = \mathcal{O}\left(\frac{1}{\varepsilon}\right) \to \infty$$
whenever $\operatorname{rank}(\mathbf{A} + \mathbf{E}) > r$.

### 2.2 Tubular Inf-Convolution & Positive Reach Regularization
Let $\mathcal{M}_r = \{\mathbf{X} \in \mathbb{R}^{m \times n} : \operatorname{rank}(\mathbf{X}) = r\}$. For any compact domain $\mathcal{K} \subset \mathcal{M}_r$, the normal reach $\operatorname{reach}(\mathcal{K}) \ge \mu > 0$ defines an open tubular neighborhood:
$$\mathcal{U}_\mu(\mathcal{M}_r) \coloneqq \{\mathbf{Y} \in \mathbb{R}^{m \times n} : \operatorname{dist}(\mathbf{Y}, \mathcal{M}_r) < \mu\}$$
Within $\mathcal{U}_\mu(\mathcal{M}_r)$, the metric projection $\pi_{\mathcal{M}_r}(\mathbf{Y})$ is uniquely defined and continuously differentiable.

**Definition 2.1 (Steiner-Federer Pseudoinverse)**. For $\mu > 0$ and $\mathbf{A} \in \mathbb{R}^{m \times n}$ with SVD $\mathbf{A} = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^T$, the Steiner pseudoinverse $\mathbf{A}_\mu^\dagger: \mathbb{R}^m \to \mathbb{R}^n$ is defined by:
$$\mathbf{A}_\mu^\dagger \coloneqq \mathbf{V} \boldsymbol{\Sigma}_\mu^\dagger \mathbf{U}^T, \quad \left(\boldsymbol{\Sigma}_\mu^\dagger\right)_{ii} = \frac{\sigma_i}{\sigma_i^2 + \mu^2}$$

**Theorem 2.1 (Everywhere Lipschitz Continuity & Operator Bound)**.
1. The operator norm of the Steiner pseudoinverse satisfies:
   $$\|\mathbf{A}_\mu^\dagger\|_{\mathrm{op}} = \max_{i} \frac{\sigma_i}{\sigma_i^2 + \mu^2} \le \frac{1}{2\mu} < \infty$$
   with equality attained at $\sigma_i = \mu$.
2. The mapping $\mathbf{A} \mapsto \mathbf{A}_\mu^\dagger$ is globally Lipschitz continuous on $\mathbb{R}^{m \times n}$:
   $$\|\mathbf{A}_\mu^\dagger - \mathbf{B}_\mu^\dagger\|_{\mathrm{op}} \le \frac{1}{\mu^2} \|\mathbf{A} - \mathbf{B}\|_{\mathrm{op}}$$
3. For any fixed matrix $\mathbf{A}$ and perturbation $\mathbf{E}$ with $\|\mathbf{E}\|_2 < \mu$:
   $$\|\mathbf{A}_\mu^\dagger - (\mathbf{A} + \mathbf{E})_\mu^\dagger\|_{\mathrm{op}} \le \frac{\|\mathbf{E}\|_{\mathrm{op}}}{\mu^2}$$
   completely eliminating the $\mathcal{O}(1/\varepsilon)$ discontinuous rank jump.

---

## 3. Pillar II: Geodesic Isometric Inversion on Riemannian Symmetric Cones

### 3.1 Affine-Invariant Fisher-Rao Geometry on $\mathcal{S}_{++}^m$
The open cone of positive-definite $m \times m$ real symmetric matrices $\mathcal{S}_{++}^m$ is equipped with the affine-invariant Riemannian metric:
$$g_{\mathbf{A}}(\mathbf{U}, \mathbf{V}) = \operatorname{tr}\left( \mathbf{A}^{-1} \mathbf{U} \mathbf{A}^{-1} \mathbf{V} \right), \quad \forall \mathbf{U}, \mathbf{V} \in T_{\mathbf{A}}\mathcal{S}_{++}^m \cong \operatorname{Sym}(m)$$
This endows $\mathcal{S}_{++}^m$ with a complete Riemannian symmetric space of non-positive sectional curvature $K(\mathbf{U}, \mathbf{V}) \le 0$.

### 3.2 Exact Isometric Inversion
**Theorem 3.1 (Riemannian Inversion Isometry)**.
The matrix inversion map $\operatorname{Inv}: \mathcal{S}_{++}^m \to \mathcal{S}_{++}^m, \mathbf{A} \mapsto \mathbf{A}^{-1}$ is an **exact Riemannian isometry**:
$$\operatorname{dist}_{\mathcal{S}_{++}^m}(\mathbf{A}^{-1}, \mathbf{B}^{-1}) = \operatorname{dist}_{\mathcal{S}_{++}^m}(\mathbf{A}, \mathbf{B}) = \sqrt{\sum_{i=1}^m \ln^2 \lambda_i(\mathbf{A}^{-1}\mathbf{B})}$$
In particular, for the identity matrix $\mathbf{I}_m$:
$$\operatorname{dist}_{\mathcal{S}_{++}^m}(\mathbf{A}^{-1}, \mathbf{I}_m) = \operatorname{dist}_{\mathcal{S}_{++}^m}(\mathbf{A}, \mathbf{I}_m)$$

### 3.3 Geodesic Midpoint Inversion Algorithm
The unique Riemannian geodesic joining $\mathbf{A}$ and $\mathbf{B}$ is given by:
$$\gamma(t) = \mathbf{A}^{1/2} \left( \mathbf{A}^{-1/2} \mathbf{B} \mathbf{A}^{-1/2} \right)^t \mathbf{A}^{1/2}, \quad t \in [0, 1]$$
Since $\operatorname{Inv}(\mathbf{A}) = \exp_{\mathbf{I}}(-\log \mathbf{A})$, computing matrix inversion in the Lie algebra $\mathfrak{sym}(m)$ via logarithmic spectral decomposition guarantees that condition numbers act as translation shifts in $\ln \lambda$ rather than multiplicative scales, preventing floating-point underflow/overflow even for $\kappa(\mathbf{A}) \ge 10^{14}$.

---

## 4. Pillar III: Simplicial Beta-Kernel Fractional Resolvents

### 4.1 Singular Laplacians and Mass Dissipation
For a graph Laplacian $\mathbf{L} = \mathbf{D} - \mathbf{W}$ or continuous Laplacian $-\Delta$, the fundamental zero-mode $\mathbf{L}\mathbf{1} = \mathbf{0}$ creates a non-invertible kernel. Standard Tikhonov regularization replaces $\mathbf{L}$ with $\mathbf{L}_\varepsilon = \mathbf{L} + \varepsilon \mathbf{I}$, solving $\mathbf{x}_\varepsilon = (\mathbf{L} + \varepsilon \mathbf{I})^{-1}\mathbf{b}$. However, this violates the fundamental mass conservation constraint:
$$\mathbf{1}^T \mathbf{x}_\varepsilon = \frac{1}{\varepsilon} \mathbf{1}^T \mathbf{b} \ne \mathbf{1}^T \mathbf{b}$$
causing total mass explosion as $\varepsilon \to 0$.

### 4.2 Simplicial Beta-Kernel Fractional Resolvents
On the standard simplex $\Delta_{m-1} = \{\mathbf{x} \in \mathbb{R}_+^m : \sum_{i=1}^m x_i = 1\}$, the fractional Simplicial Beta operator $(-\Delta_{\Delta_m})^\alpha$ for $\alpha \in (0, 1)$ generates the non-local resolvent:
$$\mathcal{R}_\lambda^\alpha \coloneqq \left( (-\Delta_{\Delta_m})^\alpha + \lambda \mathbf{I} \right)^{-1} = \int_0^\infty e^{-\lambda t} e^{-t (-\Delta_{\Delta_m})^\alpha} dt$$

**Theorem 4.1 (Exact Global Mass Conservation & Energy Monotonicity)**.
1. For any test function $f \in L^1(\Delta_{m-1})$, the resolvent $\mathcal{R}_\lambda^\alpha$ satisfies exact total mass conservation:
   $$\int_{\Delta_{m-1}} \mathcal{R}_\lambda^\alpha[f](\mathbf{x}) \, d\mu(\mathbf{x}) = \frac{1}{\lambda} \int_{\Delta_{m-1}} f(\mathbf{x}) \, d\mu(\mathbf{x})$$
2. For $\lambda = 1$, $\int_{\Delta_{m-1}} \mathcal{R}_1^\alpha[f] d\mu = \int_{\Delta_{m-1}} f d\mu$ unconditionally.
3. The Dirichlet energy functional $\mathcal{E}[u] = \frac{1}{2}\langle (-\Delta_{\Delta_m})^\alpha u, u \rangle_{L^2}$ dissipates monotonically along the resolvent flow:
   $$\frac{d}{dt}\mathcal{E}[e^{-t(-\Delta_{\Delta_m})^\alpha} u_0] = - 2 \|(-\Delta_{\Delta_m})^\alpha u(t)\|_{L^2}^2 \le 0$$
   preserving physical invariants without heuristic diagonal shifts.

---

## 5. Pillar IV: Continuous Tensor-Train (cTT) & Functional Maxvol Cross-Decomposition

### 5.1 Continuous Matrix Product States
For a multivariate continuous function $f \in C([a_1, b_1] \times \dots \times [a_d, b_d])$, the continuous Tensor-Train (cTT / cMPS) representation of rank $\mathbf{r} = (r_0, r_1, \dots, r_d)$ with $r_0 = r_d = 1$ is:
$$f(\mathbf{x}_1, \dots, \mathbf{x}_d) \approx \mathbf{G}_1(x_1) \mathbf{G}_2(x_2) \cdots \mathbf{G}_d(x_d)$$
where each core $\mathbf{G}_k(x_k) \in C([a_k, b_k], \mathbb{R}^{r_{k-1} \times r_k})$.

### 5.2 The Continuous Maximum Volume (cMaxvol) Algorithm
The continuous cross-interpolation selects optimal sets of interpolation fibers $\mathcal{I}_k = \{x_k^{(1)}, \dots, x_k^{(r_k)}\}$ by maximizing the modulus of the continuous Gram determinant:
$$\operatorname{det}\left( \mathbf{G}_k(x_k^{(i)}) \right)_{i=1}^{r_k} \to \max$$

**Theorem 5.1 (Quasi-Optimality & Sample Complexity)**.
1. The continuous cross-interpolation operator $\mathcal{I}_{\mathbf{r}}[f]$ satisfies the uniform error bound:
   $$\|f - \mathcal{I}_{\mathbf{r}}[f]\|_{L^\infty} \le \sum_{k=1}^{d-1} (1 + r_k) \sigma_{k, r_k+1}(f)$$
   where $\sigma_{k, j}(f)$ is the $j$-th continuous singular value of the $k$-th matricization unfolding of $f$.
2. The sample complexity of the cTT-Cross algorithm scales as:
   $$\mathcal{N}_{\text{samples}} = \mathcal{O}\left( d \cdot r_{\max}^2 \cdot n_0 \right)$$
   where $n_0$ is the 1D Chebyshev polynomial quadrature degree, breaking the exponential curse $\mathcal{O}(n_0^d)$.

---

## 6. Pillar V: Hyperbolic Space-Form Preconditioning & Homotopic Solvers

### 6.1 Extrinsic Curvature Relief in Space Forms $(\mathbb{H}^n, g_c)$
Consider solving the large non-Hermitian linear system $\mathbf{A} \mathbf{x} = \mathbf{b}$ with spectral condition number $\kappa_E(\mathbf{A}) = \frac{\sigma_{\max}(\mathbf{A})}{\sigma_{\min}(\mathbf{A})}$. Embedding the solution manifold into a hyperbolic space form $\mathbb{H}^n(c)$ with sectional curvature $c < 0$ yields extrinsic curvature relief:

**Theorem 6.1 (Hyperbolic Condition Number Compression)**.
The extrinsic principal curvatures $\kappa_H$ in $\mathbb{H}^n(c)$ satisfy:
$$\kappa_H^* = \sqrt{(\kappa_E^*)^2 - |c|^2} < \kappa_E^*$$
Consequently, the hyperbolic preconditioned system satisfies:
$$\kappa(\mathbf{P}_H^{-1}\mathbf{A}) \le \sqrt{\kappa_E(\mathbf{A})^2 - |c|^2} < \kappa_E(\mathbf{A})$$

### 6.2 Universal Covering Space Homotopy Solvers
When the numerical range or pseudospectrum $\Lambda_\varepsilon(\mathbf{A})$ surrounds the origin in a multiply-connected domain $\Omega \setminus \{0\}$, Krylov subspace methods (GMRES/BiCGStab) exhibit polynomial stagnation.

Lifting the residual flow $\mathbf{r}(t) = \mathbf{b} - \mathbf{A}\mathbf{x}(t)$ to the universal covering space $\pi: \widetilde{\Omega} \to \Omega \setminus \{0\}$ unrolls non-trivial winding trajectories into simply connected sheets $\widetilde{\Omega}_k$.

**Theorem 6.2 (Homotopic GMRES Convergence Bound)**.
1. The maximum topological winding number of the residual trajectory is bounded by:
   $$K_{\max} = \left\lceil \frac{\kappa_E^* D_\Omega}{2\pi} \right\rceil + 1$$
   where $D_\Omega$ is the spectral diameter.
2. The homotopic Krylov algorithm decomposes the search into $K_{\max}$ unrolled sheets, achieving linear residual reduction $\|\mathbf{r}_k\| \le \rho^k \|\mathbf{r}_0\|$ with convergence rate $\rho = \frac{\kappa_H^* - 1}{\kappa_H^* + 1} < \frac{\kappa_E^* - 1}{\kappa_E^* + 1}$, with strictly zero stagnation.

---
