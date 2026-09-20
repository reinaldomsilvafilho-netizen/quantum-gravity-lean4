# Axis II: Federer Reach, Caffarelli Obstacle Regularity, and MCMC Ergodicity
## Guaranteed Spectral Gaps, Uniform Bakry-Émery Bounds, and Polynomial Mixing Times for Constrained Sampling

**Author:** Reinaldo Maia Silva-Filho  
**Affiliation:** PPGEE/DES, Universidade Federal de Lavras (UFLA), Brazil  
**Theoretical Heritage:** *Geometry, Tensors, and Quantum Gravity on $\Delta_4 \times \Delta_2$* (Chaps 07, 08); *Beyond the Spectrum* (Vols. II & III).  
**Certified Obligations:** `OBL-INF-004`, `OBL-INF-005`, `OBL-INF-006`.

---

## 1. Problem Setting: The Curse of Boundary Geometry in MCMC

In modern Bayesian inference, parameter spaces are rarely unconstrained Euclidean spaces $\mathbb{R}^d$. Ubiquitous applications impose strict geometric barriers:
1. **Physical and Biological Feasibility:** Positive variance components ($\sigma^2 > 0$), bounded correlation coefficients ($\rho \in (-1, 1)$), rate parameters, and capacity limits.
2. **Sparsity-Inducing Priors:** The Bayesian Lasso prior $p(\theta) \propto \exp(-\lambda \|\theta\|_1)$ and Elastic Net induce sharp, non-differentiable cusps at coordinate planes.
3. **Truncated Posteriors & Inequality Constraints:** Models with order constraints ($\theta_1 \le \theta_2 \le \dots \le \theta_d$), support constraints in survival analysis, or non-convex obstacles (e.g. multi-modal mixture separations).

When standard Langevin MCMC algorithms—such as Unadjusted Langevin Algorithm (ULA) or Metropolis-Adjusted Langevin Algorithm (MALA)—encounter boundaries or non-smooth cusps, three catastrophic failures occur:
- **Boundary Sticking and Projection Bias:** Projecting proposals back onto the boundary $\partial \Omega$ accumulates unphysical mass at the boundaries.
- **Infinite Reflection Frequencies:** Exact reflected Brownian motion $dX_t = -\nabla U(X_t)dt + \sqrt{2}dW_t + \mathbf{n}(X_t) dL_t$ requires an infinite number of boundary touches in finite time, causing severe discretization bias.
- **Degenerate Spectral Gaps:** Without geometric regularity of $\partial \Omega$, the Poincaré constant collapses, leading to exponential mixing times $\tau_{\mathrm{mix}} = \mathcal{O}(e^d)$.

---

## 2. Geometric Foundations: Federer Reach and Caffarelli Obstacles

### 2.1 The Federer Reach Invariant
From Herbert Federer (1959) and Chapter 07 of the *Treatise*, the **reach** of a closed subset $\Omega \subset \mathbb{R}^d$, denoted $\operatorname{reach}(\Omega)$, is the supremum of distances $r > 0$ such that every point $x$ within the $r$-tubular neighborhood $U_r(\Omega) = \{ x \in \mathbb{R}^d : \operatorname{dist}(x, \Omega) < r \}$ has a **unique metric projection** onto $\Omega$:
$$\pi_\Omega(x) = \arg\min_{y \in \Omega} \|x - y\|_2.$$

### 2.2 Theorem 2.1 (Reach-Curvature Duality — OBL-INF-004)
*If $\partial \Omega$ is a $C^2$ hypersurface, the Federer reach is reciprocal to the minimax extrinsic curvature $\kappa^*$ of the boundary:*
$$\operatorname{reach}(\Omega) = \frac{1}{\kappa^*}, \quad \text{where } \kappa^* = \sup_{p \in \partial \Omega} \|\mathrm{II}_{\partial \Omega}(p)\|_{\mathrm{op}}.$$
*For general closed sets with non-smooth boundaries (including polyhedra and obstacle complements), $\operatorname{reach}(\Omega) \ge R > 0$ guarantees that the normal cone satisfies a uniform exterior ball condition of radius $R$.*

### 2.3 The Caffarelli $C^{1,1}$ Free Boundary Barrier (OBL-INF-005)
Consider the hard-constrained posterior density $\pi(x) \propto e^{-U(x)} \mathbf{1}_{\Omega}(x)$. Rather than simulating discontinuous reflections, we construct the **Moreau-Yosida envelope** of the potential:
$$U_\lambda(x) = \inf_{y \in \Omega} \left\{ U(y) + \frac{1}{2\lambda} \|x - y\|^2 \right\}, \quad \lambda > 0.$$

By the Caffarelli Regularity Barrier Theorem (Chapter 07, Thm 5.2):
1. The regularized potential $U_\lambda$ is continuously differentiable: $\nabla U_\lambda(x) = \frac{1}{\lambda}(x - \pi_\Omega(x))$.
2. The gradient $\nabla U_\lambda$ is Lipschitz continuous with constant $L_\lambda = \max(L_U, \frac{1}{\lambda})$.
3. Across the detachment boundary $\partial \Omega$, the Hessian $\nabla^2 U_\lambda(x)$ exhibits an optimal, finite jump discontinuity but remains uniformly bounded in $L^\infty$:
$$\nabla^2 U_\lambda(x) \ge -\frac{1}{\operatorname{reach}(\Omega)} \mathbf{I} = -\kappa^* \mathbf{I}, \quad \text{a.e. } x \in U_r(\Omega).$$
Thus, the Caffarelli barrier regularizes hard inequality constraints into a smooth, uniformly semi-convex drift field without loss of convexity beyond the curvature of the boundary!

---

## 3. Bakry-Émery Curvature and Guaranteed Spectral Gaps

### 3.1 The Bakry-Émery Ricci Curvature on Constrained Domains
Let $\pi_\lambda(x) \propto e^{-U_\lambda(x)}$ be the smoothed posterior on $\mathbb{R}^d$, and let $\Omega$ have diameter $D = \operatorname{diam}(\Omega) < \infty$. The Bakry-Émery curvature-dimension condition $\operatorname{CD}(K, \infty)$ requires:
$$\operatorname{Ric}_\infty(x) = \nabla^2 U_\lambda(x) \ge K \mathbf{I}.$$
When $U$ is $\mu$-strongly convex on $\Omega$ ($\mu > 0$), the presence of the boundary obstacle reduces the effective curvature by the extrinsic curvature $\kappa^*$:
$$K_{\mathrm{eff}} = \mu - \kappa^* = \mu - \frac{1}{\operatorname{reach}(\Omega)}.$$

### 3.2 Theorem 2.2 (Non-Asymptotic Poincaré Spectral Gap — OBL-INF-004)
*Let $\Omega \subset \mathbb{R}^d$ be a domain with Federer reach $\operatorname{reach}(\Omega) \ge R > 0$ and diameter $D$. Let the target density $\pi(x) \propto e^{-U(x)}\mathbf{1}_\Omega(x)$ satisfy $\nabla^2 U \ge \mu \mathbf{I}$. Then, for the Moreau-smoothed Langevin generator $\mathcal{L}_\lambda f = \Delta f - \nabla U_\lambda \cdot \nabla f$, the first non-trivial Poincaré eigenvalue $\lambda_1$ satisfies the sharp lower bound:*
$$\lambda_1(\mathcal{L}_\lambda) \ge \frac{K_{\mathrm{eff}}}{1 - \exp\left( -K_{\mathrm{eff}} D^2 \right)} \ge \frac{\mu - \kappa^*}{1 - \exp\left( -(\mu - \kappa^*) D^2 \right)} > 0,$$
*provided $\mu > \kappa^*$. If $\mu \le \kappa^*$, the Payne-Weinberger / Andrews-Clutterbuck bound yields:*
$$\lambda_1(\mathcal{L}_\lambda) \ge \frac{\pi^2}{D^2} \exp\left( -2 \kappa^* D \right).$$

**Significance:**  
Unlike heuristic boundary projections that collapse the spectral gap to zero, the Federer reach bound guarantees that $\lambda_1$ remains strictly bounded away from zero by an explicit geometric constant!

---

## 4. Polynomial Mixing Time for Constrained Langevin MCMC

### 4.1 Reflected Langevin Algorithm with Moreau Drift (RLA-M)
The discrete-time Langevin algorithm with step-size $\gamma > 0$ is defined as:
$$X_{k+1} = X_k - \gamma \nabla U_\lambda(X_k) + \sqrt{2\gamma} \boldsymbol{\xi}_k, \quad \boldsymbol{\xi}_k \sim \mathcal{N}(\mathbf{0}, \mathbf{I}_d).$$

### 4.2 Theorem 2.3 (Polynomial Mixing Time Bound — OBL-INF-006)
*Let $\epsilon \in (0, 1)$ be the target total variation error: $\|\operatorname{Law}(X_k) - \pi\|_{\mathrm{TV}} \le \epsilon$. Under the reach bound $\operatorname{reach}(\Omega) \ge R = 1/\kappa^*$ and Moreau regularization parameter $\lambda = \mathcal{O}(\epsilon / \kappa^*)$, the iteration complexity of RLA-M satisfies:*
$$K(\epsilon) \le \mathcal{O}\left( \frac{d \cdot (\kappa^*)^2}{\lambda_1^2 \cdot \epsilon^2} \ln\left( \frac{1}{\epsilon} \right) \right).$$
*Specifically, the mixing time scales polynomially with dimension $d$ and quadratically with the boundary curvature $\kappa^*$, completely eliminating the exponential $\mathcal{O}(e^d)$ curse of naive rejection sampling.*

---

## 5. Comparative Paradigm Summary

| Dimension of Comparison | Classical Rejection MCMC | Naive Projected Langevin | Reach-Bounded Moreau MCMC (This Work) |
| :--- | :--- | :--- | :--- |
| **Boundary Treatment** | Discards out-of-bounds proposals. | Snaps proposals to boundary $\partial \Omega$. | Smooth Caffarelli $C^{1,1}$ normal gradient drift. |
| **Hessian Regularity** | Ill-defined at boundary. | Dirac delta singularity at $\partial \Omega$. | Uniformly bounded: $\nabla^2 U_\lambda \ge -\kappa^* \mathbf{I}$. |
| **Discretization Bias** | Exact, but zero acceptance rate in high $d$. | $\mathcal{O}(\sqrt{\gamma})$ large boundary bias. | $\mathcal{O}(\gamma)$ optimal Euclidean Langevin rate. |
| **Spectral Gap Guarantee** | None (can be arbitrarily small). | Unknown / broken ergodicity. | Explicit non-asymptotic bound via $\operatorname{reach}(\Omega)$. |
| **Dimensional Scaling** | Exponential $\mathcal{O}(e^d)$. | Unknown (often diverges). | **Strictly Polynomial $\mathcal{O}(d \cdot (\kappa^*)^2)$**. |
