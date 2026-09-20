# Axis V: Symplectic Floer Homology and Non-Equilibrium Score Diffusions
## Exact Marginal Likelihood and Bayesian Evidence Estimation via Jarzynski Work Relations on Symplectic Phase Space

**Author:** Reinaldo Maia Silva-Filho  
**Affiliation:** PPGEE/DES, Universidade Federal de Lavras (UFLA), Brazil  
**Theoretical Heritage:** *Beyond the Spectrum* (Vol. III); *Geometry, Tensors, and Quantum Gravity on $\Delta_4 \times \Delta_2$* (Chap 11).  
**Certified Obligations:** `OBL-INF-013`, `OBL-INF-014`, `OBL-INF-015`.

---

## 1. Problem Setting: The Challenge of Bayesian Evidence Estimation

In Bayesian model comparison and hypothesis testing, the decisive quantity is the **marginal likelihood** (also known as the **Bayesian evidence**):
$$Z = p(\mathbf{y}) = \int_{\Theta} p(\mathbf{y} | \boldsymbol{\theta}) p(\boldsymbol{\theta}) \, d\boldsymbol{\theta}.$$
The Bayes Factor comparing two competing models $\mathcal{M}_1$ and $\mathcal{M}_2$ is:
$$\mathrm{BF}_{12} = \frac{p(\mathbf{y} | \mathcal{M}_1)}{p(\mathbf{y} | \mathcal{M}_2)} = \frac{Z_1}{Z_2}.$$

### The Failure of Classical Annealing and Bridge Sampling
Because high-dimensional posteriors concentrate on complex, lower-dimensional geometric submanifolds, evaluating $Z$ directly is extraordinarily difficult:
- **Naive Monte Carlo:** $\widehat{Z} = \frac{1}{M} \sum_{m=1}^M p(\mathbf{y} | \boldsymbol{\theta}^{(m)})$ with $\boldsymbol{\theta}^{(m)} \sim p(\boldsymbol{\theta})$ has exponential variance $\operatorname{Var}(\widehat{Z}) \to \infty$ in high dimensions.
- **Thermodynamic Integration (Path Sampling):** $\ln Z_1 - \ln Z_0 = \int_0^1 \mathbb{E}_{\pi_\beta}[\ln p(\mathbf{y}|\boldsymbol{\theta})] d\beta$ requires infinite quasi-static annealing steps; fast schedules cause extreme hysteresis and systematic underestimation.
- **Annealed Importance Sampling (AIS):** Prone to path trapping when passing through first-order phase transitions or multimodal energy barriers.

---

## 2. Symplectic Geometry of Underdamped Langevin Dynamics

### 2.1 Symplectic Phase Space Formulation (OBL-INF-013)
From Volume III of *Beyond the Spectrum*, we lift the parameter manifold $\mathcal{M}$ to its cotangent bundle $T^*\mathcal{M}$, forming the **Symplectic Phase Space** $(T^*\mathcal{M}, \omega)$, equipped with the canonical symplectic 2-form:
$$\omega = \sum_{i=1}^d d\theta^i \wedge dp_i.$$

Let $\boldsymbol{\theta} \in \mathcal{M}$ represent the parameter coordinates, and $\mathbf{p} \in T_{\boldsymbol{\theta}}^*\mathcal{M}$ represent auxiliary conjugate momenta with mass matrix $\mathbf{M}$.  
The time-dependent Hamiltonian is:
$$H_t(\boldsymbol{\theta}, \mathbf{p}) = \frac{1}{2} \mathbf{p}^T \mathbf{M}^{-1} \mathbf{p} + U_t(\boldsymbol{\theta}),$$
where $U_t(\boldsymbol{\theta})$ is the non-equilibrium annealed potential bridging the prior $U_0(\boldsymbol{\theta}) = -\ln p(\boldsymbol{\theta})$ to the unnormalized posterior $U_1(\boldsymbol{\theta}) = -\ln [p(\mathbf{y}|\boldsymbol{\theta})p(\boldsymbol{\theta})]$:
$$U_t(\boldsymbol{\theta}) = (1 - \lambda(t)) U_0(\boldsymbol{\theta}) + \lambda(t) U_1(\boldsymbol{\theta}), \quad \lambda(0) = 0, \; \lambda(T) = 1.$$

The dynamics is governed by the **Dissipative Symplectic Flow**:
$$\begin{aligned}
d\boldsymbol{\theta}_t &= \frac{\partial H_t}{\partial \mathbf{p}} \, dt = \mathbf{M}^{-1} \mathbf{p}_t \, dt, \\
d\mathbf{p}_t &= -\frac{\partial H_t}{\partial \boldsymbol{\theta}} \, dt - \gamma \mathbf{p}_t \, dt + \sqrt{2\gamma \mathbf{M}} \, d\mathbf{W}_t,
\end{aligned}$$
where $\gamma > 0$ is the friction coefficient and $\mathbf{W}_t$ is standard Brownian motion.

---

## 3. The Non-Equilibrium Jarzynski Work Theorem for Bayesian Evidence

### 3.1 Definition of Trajectory Work
Along any realization of the stochastic trajectory $\Gamma = \{(\boldsymbol{\theta}_t, \mathbf{p}_t)\}_{t=0}^T$, the total non-equilibrium work performed by the external annealing schedule $\lambda(t)$ is:
$$\mathcal{W}[\Gamma] = \int_0^T \frac{\partial H_t}{\partial t} \, dt = \int_0^T \dot{\lambda}(t) \left[ U_1(\boldsymbol{\theta}_t) - U_0(\boldsymbol{\theta}_t) \right] dt = - \int_0^T \dot{\lambda}(t) \ln p(\mathbf{y} | \boldsymbol{\theta}_t) \, dt.$$

### 3.2 Theorem 5.1 (Exact Jarzynski Evidence Identity — OBL-INF-014)
*Let the initial phase-space state $(\boldsymbol{\theta}_0, \mathbf{p}_0)$ be sampled from the canonical equilibrium ensemble of the prior: $(\boldsymbol{\theta}_0, \mathbf{p}_0) \sim \frac{1}{Z_0} e^{-H_0(\boldsymbol{\theta}, \mathbf{p})}$, where $Z_0 = \int e^{-U_0(\boldsymbol{\theta})} d\boldsymbol{\theta} \cdot (2\pi)^{d/2} \det(\mathbf{M})^{1/2}$.*

*For **any** finite driving protocol duration $T > 0$ and **arbitrary** speed of annealing $\dot{\lambda}(t)$, the expectation of the exponential work satisfies the exact identity:*
$$\mathbb{E}_{\Gamma} \left[ \exp\left( -\mathcal{W}[\Gamma] \right) \right] = \frac{Z_1}{Z_0} = \frac{Z_{\mathrm{posterior}}}{Z_{\mathrm{prior}}}.$$
*Consequently, the true marginal likelihood $Z = p(\mathbf{y})$ admits the strictly unbiased estimator:*
$$\widehat{Z}_{\mathrm{Jarzynski}} = \frac{Z_{\mathrm{prior}}}{N_{\mathrm{traj}}} \sum_{n=1}^{N_{\mathrm{traj}}} \exp\left( -\mathcal{W}[\Gamma^{(n)}] \right).$$

**Significance:**  
Unlike thermodynamic integration—which requires infinitely slow, adiabatic transitions ($T \to \infty$) to avoid bias—the Jarzynski equality holds **identically for fast, non-equilibrium diffusions** ($T < \infty$)! Dissipation is entirely cancelled by the exponential work weighting.

---

## 4. Symplectic Floer Homology and Topological Stability

### 4.1 The Symplectic Floer Action Functional
From *Beyond the Spectrum* (Vol. III), the space of trajectories on $T^*\mathcal{M}$ is organized by the Floer action functional:
$$\mathcal{A}_H(\gamma) = -\int_{\mathbb{D}} u^* \omega + \int_0^T H_t(\gamma(t)) \, dt.$$

### 4.2 Theorem 5.2 (Topological Stability of Evidence Estimator — OBL-INF-015)
*Let $\mathbf{s}(\boldsymbol{\theta}, t) = -\nabla U_t(\boldsymbol{\theta})$ be the score vector field driving the diffusion. Under any smooth homotopy deformation of the score field $\mathbf{s}_\tau(\boldsymbol{\theta}, t)$ that preserves the Floer cohomology groups $HF_*(T^*\mathcal{M}, \omega) \cong H_*(\mathcal{M})$:*
1. *The variance of the Jarzynski evidence estimator is uniformly bounded by the Floer spectral capacity:*
$$\operatorname{Var}\left( \frac{\widehat{Z}}{Z} \right) \le \exp\left( c_{\mathrm{Floer}}(H) \right) - 1,$$
*where $c_{\mathrm{Floer}}(H)$ is the spectral invariant associated with the fundamental class $[T^*\mathcal{M}]$.*
2. *The estimator is immune to the topological phase transitions and mode-collapse phenomena that cause exponential variance explosion in classical annealed importance sampling.*

---

## 5. Algorithmic Protocol: Symplectic Non-Equilibrium Evidence Sampler

```
Algorithm 3: Symplectic Non-Equilibrium Evidence Sampler (SNE-ES)
─────────────────────────────────────────────────────────────────────────────
Input: Data Y, Prior p(theta), Log-likelihood ln p(Y|theta), Number of paths N,
       Time steps K, Total time T, Friction gamma, Mass M
Output: Unbiased Marginal Likelihood Estimate Z_hat

1. Set time step dt = T / K
2. For path n = 1 to N:
     a. Sample theta_0 ~ p(theta)
     b. Sample p_0 ~ Normal(0, M)
     c. Initialize work: W_n = 0
     d. For step k = 0 to K-1:
          t_k = k * dt, lambda_k = k / K, dot_lambda = 1 / T
          Evaluate: delta_U = -ln p(Y | theta_k)
          Accumulate work: W_n = W_n + dot_lambda * delta_U * dt
          Update momentum (half-step): p_half = p_k - 0.5 * dt * nabla U_{t_k}(theta_k)
          Update position (full-step): theta_{k+1} = theta_k + dt * M^{-1} p_half
          Evaluate: nabla U_{t_{k+1}}(theta_{k+1})
          Update momentum (drift): p_full = p_half - 0.5 * dt * nabla U_{t_{k+1}}(theta_{k+1})
          Apply Langevin thermostat:
            xi ~ Normal(0, I)
            p_{k+1} = exp(-gamma * dt) * p_full + sqrt(1 - exp(-2*gamma*dt)) * sqrt(M) * xi
3. Compute unbiased evidence:
     Z_hat = Z_prior * (1 / N) * sum_{n=1}^N exp(-W_n)
Output: Z_hat, standard error SE(Z_hat)
─────────────────────────────────────────────────────────────────────────────
```
