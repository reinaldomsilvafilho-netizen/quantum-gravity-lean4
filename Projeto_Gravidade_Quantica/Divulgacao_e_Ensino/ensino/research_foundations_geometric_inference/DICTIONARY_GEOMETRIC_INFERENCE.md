# Master Dictionary: Differential Geometry, Mathematical Physics, and Statistical Inference
## A Bilingual Conceptual and Formal Rosetta Stone

**Author:** Reinaldo Maia Silva-Filho  
**Affiliation:** PPGEE/DES, Universidade Federal de Lavras (UFLA)  

---

## 1. Simplicial Calculus and Compositional Data (Axis I)

| Mathematical Physics & Geometry (Treatise & BTS) | Statistical Inference Counterpart | Exact Mathematical Formulation | Operational Significance in Statistics |
| :--- | :--- | :--- | :--- |
| **Continuous Simplex $\Delta_m$** | **Compositional Parameter Space / Simplex $S^D$** | $\Delta_m = \{ \mathbf{x} \in \mathbb{R}_{\ge 0}^{m+1} : \sum_{i=1}^{m+1} x_i = 1 \}$ | Space of proportions, microbiome taxa frequencies, agronomic soil fractions, Dirichlet priors. |
| **Beta-Kernel Fractional Laplacian $(-\Delta_{\Delta_m})^\alpha$** | **Non-Local Precision Operator of Simplicial GMRF** | $\mathcal{Q}_\alpha = (-\Delta_{\Delta_m} + \kappa^2)^\alpha$, with covariance $\mathbf{\Sigma} = \mathcal{Q}_\alpha^{-1}$ | Replaces Euclidean Matérn kernels. Avoids boundary singularities of log-ratios without ad-hoc pseudocounts. |
| **Simplicial Fourier Dispersion Symbol $\sigma_{\Delta_m}^\alpha(\mathbf{k})$** | **Spectral Density / Frequency Response of Spatial Prior** | $\sigma_{\Delta_m}^\alpha(\mathbf{k}) = \frac{1}{\alpha^2}[1 - R(\mathbf{k})^\alpha \cos(\alpha \Theta(\mathbf{k}))]$ | Controls spatial correlation decay rate along barycentric directions; isotropic limit recovers Matérn. |
| **Emergent $A_{m-1}$ Cartan Metric** | **Covariance Matrix of Equal-Weight Dirichlet Fluctuations** | $\mathbf{A}_{m-1} = 2\mathbf{I} - \mathbf{1}\mathbf{1}^T + \dots$, $\mathrm{Cov}(x_j, x_k) = -\frac{1}{m^2}$ | Canonical negative equicorrelation induced strictly by the simplex closure constraint $\sum x_i = 1$. |
| **Inter-Dimensional Trace $\mathcal{R}_{m \to n}^\alpha$** | **Marginalization / Aggregation Operator of Sub-compositions** | $\mathcal{R}_{m \to n}^\alpha : H^s(\Delta_m) \to H^{s + \alpha - \frac{m-n}{2}}(\Delta_n)$ | Projecting higher-order taxonomies to sub-classes without losing differentiability at $\alpha^* = \frac{m-n}{2}$. |
| **Siegel-Wishart Matrix Beta Operator $\mathcal{G}_{\mathbf{A},\mathbf{B}}$** | **Matrix-Variate Beta Conjugate Prior on Covariances** | $\mathcal{G}_{\mathbf{A},\mathbf{B}} \mathbf{X} \sim \mathcal{B}_m(\mathbf{A}, \mathbf{B})$ on $\mathcal{S}_{++}^m$ | Generalizes univariate Beta priors to full covariance matrices in Wishart random effects models. |

---

## 2. Metric Measure Geometry, Obstacles, and MCMC Ergodicity (Axis II)

| Mathematical Physics & Geometry (Treatise & BTS) | Statistical Inference Counterpart | Exact Mathematical Formulation | Operational Significance in Statistics |
| :--- | :--- | :--- | :--- |
| **Federer Reach $\operatorname{reach}(\Omega)$** | **Boundary Curvature Margin for Constrained Parameters** | $\operatorname{reach}(\Omega) = \sup \{ r > 0 : \forall x \in U_r(\Omega), \exists! \pi_\Omega(x) \}$ | Minimum radius of curvature of the parameter constraint boundary. Prevents self-intersection of normal rays. |
| **Minimax Extrinsic Curvature $\kappa^*$** | **Worst-Case Directional Constraint Penalty** | $\kappa^* = \sup_{p \in \partial\Omega} \|\mathrm{II}(p)\|_{\mathrm{op}} = \frac{1}{\operatorname{reach}(\Omega)}$ | Quantifies maximum boundary curvature. Determines Langevin reflection stability and discretization step size. |
| **Caffarelli $C^{1,1}$ Free Boundary Barrier** | **Optimal Smoothness of Regularized Non-Smooth Priors** | $\nabla^2 U_\epsilon(x) \in L^\infty$, finite jump across $\partial \Omega$ | Represents exact regularized potentials for Lasso ($\ell_1$), Elastic Net, and box-constrained posteriors. |
| **Bakry-Émery Curvature $\mathrm{Ric}_\infty \ge K$** | **Log-Sobolev / Poincaré Constant for Target Density** | $\mathrm{Ric}_\infty = \mathrm{Ric} + \nabla^2 U \ge K \mathbf{I}$ on Riemannian manifold | Guarantees exponential contraction in Wasserstein distance $W_2$ and rapid convergence of MCMC chains. |
| **Poincaré Spectral Gap $\lambda_1$** | **Asymptotic Exponential MCMC Mixing Rate** | $\mathrm{Var}_\pi(f) \le \frac{1}{\lambda_1} \int \|\nabla f\|^2 d\pi$ | Rate at which Markov chain autocorrelation decays. Mixing time $\tau_{\mathrm{mix}} \le \frac{1}{\lambda_1}\ln(1/\epsilon)$. |
| **Moreau-Yosida Normal Bundle Envelope** | **Interior-Exterior Smoothing of Hard Inequality Constraints** | $U_\lambda(x) = \inf_{y \in \Omega} \{ U(y) + \frac{1}{2\lambda} \|x - y\|^2 \}$ | Transforms discontinuous hard boundaries into Lipschitz-gradient Langevin drift fields. |

---

## 3. Information Geometry and Variational Optimization (Axis III)

| Mathematical Physics & Geometry (Treatise & BTS) | Statistical Inference Counterpart | Exact Mathematical Formulation | Operational Significance in Statistics |
| :--- | :--- | :--- | :--- |
| **Fisher-Rao Metric Tensor $g^F(\theta)$** | **Riemannian Metric on Statistical Manifold $\mathcal{M}$** | $g_{ij}^F(\theta) = \mathbb{E}_{p_\theta}\left[ \frac{\partial \ln p_\theta}{\partial \theta^i} \frac{\partial \ln p_\theta}{\partial \theta^j} \right]$ | Invariant metric under parameter reparametrizations; measures intrinsic informational distance. |
| **Macroscopic 2-Wasserstein Metric $W_2$** | **Optimal Transport Distance between Probability Measures** | $W_2^2(\mu, \nu) = \inf_{\gamma \in \Pi(\mu,\nu)} \int \|x - y\|^2 d\gamma(x,y)$ | Measures geodesic distance between variational posteriors $q_\theta$ and exact targets $p(\cdot|y)$. |
| **Natural Gradient $\widetilde{\nabla} \mathcal{L}(\theta)$** | **Steepest Descent Direction in Distribution Space** | $\widetilde{\nabla} \mathcal{L}(\theta) = [g^F(\theta)]^{-1} \nabla_\theta \mathcal{L}(\theta)$ | Invariant optimization step; moves along the manifold of distributions rather than coordinate artifacts. |
| **Barren Plateau Phenomenon** | **Exponentially Vanishing Gradient Variance in Deep Models** | $\operatorname{Var}_\theta[\partial_k \mathcal{L}] \le \mathcal{O}(2^{-n})$ due to Haar measure concentration | Failure of gradient descent in overparameterized variational families (quantum circuits, deep VI). |
| **Stiefel Dynamical Isometry** | **Orthogonal Weight Transport Bypassing Vanishing Gradients** | $\mathbf{W} \in \operatorname{St}(p, n) = \{ \mathbf{W} \in \mathbb{R}^{n \times p} : \mathbf{W}^T \mathbf{W} = \mathbf{I}_p \}$ | Preserves singular value spectrum of Jacobian across layers, guaranteeing polynomial training time. |
| **PAC-Bayesian Curvature Bound** | **Generalization Error Controlled by Trajectory Curvature** | $\mathcal{R}(q_\theta) \le \widehat{\mathcal{R}}(q_\theta) + \sqrt{\frac{\operatorname{Tr}(g^F) \cdot \kappa^*_{\mathrm{info}} + \ln(2/\delta)}{2N}}$ | Connects optimization geometry directly to test-set risk and overfitting prevention. |

---

## 4. Continuous Tensor Varieties and High-Dimensional Likelihoods (Axis IV)

| Mathematical Physics & Geometry (Treatise & BTS) | Statistical Inference Counterpart | Exact Mathematical Formulation | Operational Significance in Statistics |
| :--- | :--- | :--- | :--- |
| **Continuous Tensor Variety $\mathcal{V}_r$** | **Low-Rank Surrogate Model for Likelihood Tensors** | $L(x_1, \dots, x_D) = \sum_{k=1}^r A_1^k(x_1) \cdots A_D^k(x_D)$ | Compresses factorial likelihood surfaces from exponential $\mathcal{O}(S^D)$ to linear $\mathcal{O}(D S r^2)$. |
| **Functional Realization in $L^2(\mathbb{T}^d)$** | **Continuous Limit of Large Multi-Factor Design Matrices** | $T : L^2(\mathbb{T}^d) \to L^2(\mathbb{T}^d)$, $(Tf)(x) = \int K(x,y)f(y)dy$ | Enables mesh-independent modeling of agricultural field trials and continuous spatial treatments. |
| **Simplicial Residues $\operatorname{Res}_\Delta(T)$** | **Truncation Error and Topological Defect of Tensor Approximation** | $\operatorname{Res}_\Delta(T) = \oint_{\partial \Delta} \operatorname{Tr}(T^{-1} dT)$ | Analytical error bound certifying exactness of low-rank likelihood contractions. |
| **Tensor-Train (cTT) Decomposition** | **Chain-Structured Representation of Joint Likelihoods** | $L(\boldsymbol{\theta}) = \mathbf{G}_1(\theta_1) \mathbf{G}_2(\theta_2) \cdots \mathbf{G}_D(\theta_D)$ | Evaluates marginal integrals $\int L(\boldsymbol{\theta}) d\boldsymbol{\theta}$ as sequential matrix multiplications. |
| **Toda Lattice Gradient Flow** | **Continuous Isospectral Sorting / Covariance Diagonalization** | $\frac{d\mathbf{L}}{dt} = [\mathbf{B}(\mathbf{L}), \mathbf{L}]$, where $\mathbf{B} = \mathbf{L}_- - \mathbf{L}_+^T$ | Dynamically diagonalizes ill-conditioned high-dimensional covariance matrices while preserving eigenvalues. |

---

## 5. Symplectic Floer Homology and Evidence Diffusions (Axis V)

| Mathematical Physics & Geometry (Treatise & BTS) | Statistical Inference Counterpart | Exact Mathematical Formulation | Operational Significance in Statistics |
| :--- | :--- | :--- | :--- |
| **Symplectic Phase Space $(T^* \mathcal{M}, \omega)$** | **Hamiltonian Phase Space for Extended MCMC / HMC** | $\omega = \sum dq^i \wedge dp_i$, with coordinates $(\theta, p)$ | Position $\theta$ (parameters) and conjugate momentum $p$ (auxiliary Gaussian kinetic variables). |
| **Floer Action Functional $\mathcal{A}_H$** | **Annealed Log-Likelihood Action along Diffusion Path** | $\mathcal{A}_H(\gamma) = -\int_{\mathbb{D}} u^* \omega + \int_0^1 H_t(\gamma(t)) dt$ | Trajectory action whose critical points correspond to maximum a posteriori (MAP) annealing paths. |
| **Jarzynski Equality (Non-Equilibrium)** | **Unbiased Estimator of Marginal Likelihood (Evidence $Z$)** | $\mathbb{E}\left[ \exp\left( -\int_0^T \frac{\partial U_t}{\partial t} dt \right) \right] = \frac{Z_1}{Z_0}$ | Computes normalising constant $Z = \int p(y|\theta)p(\theta)d\theta$ along fast non-equilibrium diffusion trajectories without asymptotic annealing. |
| **Score Matching Vector Field $\mathbf{s}(\theta, t)$** | **Gradient of Log Marginal Density in Generative Diffusion** | $\mathbf{s}(\theta, t) = \nabla_\theta \ln p_t(\theta)$ | Vector field driving reverse-time diffusion to generate posterior draws. |
| **Symplectic Momentum Dissipation** | **Underdamped Langevin Diffusion for Sampling Curved Posteriors** | $d\theta = \mathbf{M}^{-1} p \, dt$, $dp = -\nabla U(\theta)dt - \gamma p \, dt + \sqrt{2\gamma} d\mathbf{W}_t$ | Overcomes narrow ravines and high-curvature ridges faster than overdamped Langevin sampling. |
