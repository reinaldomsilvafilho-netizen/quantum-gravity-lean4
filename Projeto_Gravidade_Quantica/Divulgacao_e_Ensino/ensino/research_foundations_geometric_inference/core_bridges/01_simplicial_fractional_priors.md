# Axis I: Simplicial Fractional Priors and Non-Local Compositional Inference
## Non-Local Beta-Laplacian Random Fields, Cartan Metrics, and Isomorphic Sub-Compositional Traces

**Author:** Reinaldo Maia Silva-Filho  
**Affiliation:** PPGEE/DES, Universidade Federal de Lavras (UFLA), Brazil  
**Theoretical Heritage:** *Geometry, Tensors, and Quantum Gravity on $\Delta_4 \times \Delta_2$* (Chaps 03, 04, 05); *Beyond the Spectrum* (Vol. I).  
**Certified Obligations:** `OBL-INF-001`, `OBL-INF-002`, `OBL-INF-003`.

---

## 1. Motivation and Problem Setting in Statistical Inference

### 1.1 The Compositional Data Dilemma
In modern agronomic, environmental, microbiome, and genetic studies, observations frequently take the form of compositions: vectors whose components are strictly non-negative and sum to a constant (typically 1):
$$\Delta_m = \left\{ \mathbf{x} = (x_1, \dots, x_{m+1})^T \in \mathbb{R}_{\ge 0}^{m+1} : \sum_{i=1}^{m+1} x_i = 1 \right\}.$$

The classical approach pioneered by John Aitchison (1986) projects $\Delta_m$ to Euclidean space $\mathbb{R}^m$ via log-ratio transformations:
- **Additive Log-Ratio (ALR):** $\mathrm{alr}_i(\mathbf{x}) = \ln(x_i / x_{m+1})$.
- **Centered Log-Ratio (CLR):** $\mathrm{clr}_i(\mathbf{x}) = \ln(x_i / g(\mathbf{x}))$, where $g(\mathbf{x}) = (\prod x_i)^{1/(m+1)}$.
- **Isometric Log-Ratio (ILR):** $\mathrm{ilr}(\mathbf{x}) = \mathbf{\Psi}^T \ln(\mathbf{x})$ for an orthonormal basis $\mathbf{\Psi}$.

#### The Fatal Failure Mode: Boundary Singularities
When empirical data contain true or detection-limit zeros (e.g., zero abundance of a microbial taxon, absence of a soil mineral fraction, or zero mutation count), the log-ratio maps diverge:
$$\lim_{x_i \to 0^+} \ln(x_i) = -\infty.$$
Standard practice relies on ad-hoc *pseudocount imputation* ($x_i \leftarrow x_i + \delta$), which arbitrarily distorts the covariance structure, introduces spurious correlations, and breaks statistical equivariance. Furthermore, when defining spatial Gaussian Processes (GPs) or spatial priors for compositional fields, Euclidean Matérn kernels on log-ratios fail to respect the intrinsic boundary reflections of the simplex polytope.

---

## 2. Mathematical Formulation: Simplicial Beta-Kernel Random Fields

### 2.1 The Simplicial Beta-Laplacian Operator
From Chapter 03 and Chapter 04 of the *Treatise*, let $\Delta_m$ be equipped with barycentric coordinates $\mathbf{x} = (x_1, \dots, x_{m+1})$. The continuous multinomial density induces a non-local Beta-kernel convolution operator:
$$\mathcal{K}_\alpha[f](\mathbf{x}) = \frac{1}{B(\alpha, \dots, \alpha)} \int_{\Delta_m} \left( \prod_{i=1}^{m+1} |x_i - y_i|^{\alpha - 1} \right) f(\mathbf{y}) \, d\mu_\Delta(\mathbf{y}),$$
where $d\mu_\Delta$ is the normalized Lebesgue measure on $\Delta_m$.

The infinitesimal generator of this non-local diffusion defines the **Simplicial Fractional Laplacian**:
$$(-\Delta_{\Delta_m})^\alpha f(\mathbf{x}) = \lim_{t \to 0^+} \frac{f(\mathbf{x}) - \mathcal{K}_\alpha^t[f](\mathbf{x})}{t^\alpha} = \mathrm{P.V.} \int_{\Delta_m} \frac{f(\mathbf{x}) - f(\mathbf{y})}{\|\mathbf{x} - \mathbf{y}\|_{\Delta}^{m + 2\alpha}} \, d\mu_\Delta(\mathbf{y}).$$

### 2.2 Theorem 1.1 (Simplicial GMRF Precision Operator — OBL-INF-001)
*Let $\mathcal{H} = L^2(\Delta_m, d\mu_\Delta)$. For any $\alpha > 0$ and screening parameter $\kappa > 0$, the operator*
$$\mathcal{Q}_\alpha = (-\Delta_{\Delta_m} + \kappa^2 \mathbf{I})^\alpha$$
*is a strictly positive-definite, self-adjoint pseudo-differential operator on $\mathcal{H}$. The Gaussian random field $u \sim \mathcal{GP}(0, \mathbf{\Sigma})$ on $\Delta_m$ with precision operator $\mathcal{Q}_\alpha$ satisfies:*
1. *Barycentric boundary regularity: For any $\mathbf{x} \in \partial \Delta_m$, the field variance $\operatorname{Var}[u(\mathbf{x})]$ remains finite and bounded: $\sup_{\mathbf{x} \in \Delta_m} \operatorname{Var}[u(\mathbf{x})] < \infty$.*
2. *Elimination of Gibbs boundary oscillations: The algebraic roll-off of the continuous Beta-kernel ensures that sample paths $u(\mathbf{x})$ have Hölder regularity $C^{0, \gamma}(\Delta_m)$ for any $\gamma < \min(1, \alpha)$.*

**Proof Sketch:**  
Self-adjointness follows from the symmetry of the integral kernel $\|\mathbf{x} - \mathbf{y}\|_\Delta = \|\mathbf{x} - \mathbf{y}\|_2$ on the closed convex polytope $\Delta_m$. Positive definiteness is established via the quadratic form:
$$\langle f, \mathcal{Q}_\alpha f \rangle_{\mathcal{H}} = \kappa^{2\alpha} \|f\|_{\mathcal{H}}^2 + \frac{1}{2} \int_{\Delta_m} \int_{\Delta_m} \frac{|f(\mathbf{x}) - f(\mathbf{y})|^2}{\|\mathbf{x} - \mathbf{y}\|_\Delta^{m+2\alpha}} \, d\mu_\Delta(\mathbf{x}) d\mu_\Delta(\mathbf{y}) > 0, \quad \forall f \ne 0.$$
Because the boundary $\partial \Delta_m$ is formed by smooth $(m-1)$-dimensional simplicial faces intersecting at finite dihedral angles, the Dirichlet and Neumann extensions do not develop corner singularities under fractional powers $\alpha < 1$. Hence, the green's function $G_\alpha(\mathbf{x}, \mathbf{y}) = \mathcal{Q}_\alpha^{-1}(\mathbf{x}, \mathbf{y})$ is bounded at the boundary, avoiding the log-ratio singularity. $\blacksquare$

---

## 3. Asymptotic Emergence of the Lie Algebra $A_{m-1}$ Cartan Covariance

### 3.1 Theorem 1.2 (Cartan Metric Equicorrelation — OBL-INF-002)
*In the long-wavelength continuum limit $|\mathbf{k}| \to 0$, the Fourier dispersion symbol $\sigma_{\Delta_m}^\alpha(\mathbf{k})$ of the fractional simplicial Laplacian satisfies:*
$$\sigma_{\Delta_m}^\alpha(\mathbf{k}) = \frac{1}{2m\alpha} \mathbf{k}^T \mathbf{A}_{m-1} \mathbf{k} + \mathcal{O}(|\mathbf{k}|^4),$$
*where $\mathbf{A}_{m-1}$ is the Cartan matrix of the simple Lie algebra $A_{m-1}$:*
$$\mathbf{A}_{m-1} = \begin{pmatrix} 2 & -1 & 0 & \dots & 0 \\ -1 & 2 & -1 & \dots & 0 \\ \vdots & \ddots & \ddots & \ddots & \vdots \\ 0 & \dots & -1 & 2 & -1 \\ 0 & \dots & 0 & -1 & 2 \end{pmatrix}_{(m-1) \times (m-1)}.$$
*Consequently, the macroscopic covariance tensor of the simplicial field fluctuations matches the canonical equal-weight Dirichlet covariance:*
$$\operatorname{Cov}(x_j, x_k) = \frac{1}{m+1}\delta_{jk} - \frac{1}{(m+1)^2}, \quad \text{for } j, k \in \{1, \dots, m+1\}.$$

**Proof:**  
From Chapter 03 (Thm 5.7) and Chapter 04 (Thm 2.3), the dispersion symbol on the torus-projected simplicial lattice is given by the multinomial Taylor series:
$$\sigma_{\Delta_m}^\alpha(\mathbf{k}) = \frac{1}{\alpha^2} \left[ 1 - \left| \frac{1}{m+1} \sum_{j=1}^{m+1} e^{i \mathbf{k} \cdot \mathbf{e}_j} \right|^\alpha \right].$$
Expanding the exponential terms around $\mathbf{k} = \mathbf{0}$:
$$\sum_{j=1}^{m+1} e^{i \mathbf{k} \cdot \mathbf{e}_j} = (m+1) + i \mathbf{k} \cdot \sum \mathbf{e}_j - \frac{1}{2} \sum_{j=1}^{m+1} (\mathbf{k} \cdot \mathbf{e}_j)^2 + \mathcal{O}(|\mathbf{k}|^3).$$
Under the simplex closure constraint $\sum_{j=1}^{m+1} \mathbf{e}_j = \mathbf{0}$, the linear imaginary term vanishes identically. The quadratic form evaluates to:
$$\sum_{j=1}^{m+1} (\mathbf{k} \cdot \mathbf{e}_j)^2 = \mathbf{k}^T \left( \sum_{j=1}^{m+1} \mathbf{e}_j \mathbf{e}_j^T \right) \mathbf{k} = \frac{1}{m} \mathbf{k}^T \mathbf{A}_{m-1} \mathbf{k}.$$
Taking the fractional power $(1 - z)^\alpha = 1 - \alpha z + \mathcal{O}(z^2)$ yields the Cartan quadratic form. The inverse of the Cartan matrix is the Dynkin covariance matrix whose off-diagonal entries are strictly negative: $\operatorname{Cov}(x_j, x_k) = -1/(m+1)^2$ for $j \ne k$. This proves that the simplex closure condition $\sum x_i = 1$ naturally and inevitably induces the Cartan metric of the Lie group $\mathrm{SU}(m+1)$. $\blacksquare$

---

## 4. Sub-Compositional Aggregation and the Critical Isomorphic Trace

### 4.1 Aggregating Compositions in High Dimensions
In microbiome analysis, bacterial species are grouped into genera, families, and phyla. In agronomic soils, fine particle fractions are aggregated into clay, silt, and sand. Mathematically, this corresponds to an inter-dimensional projection operator:
$$\mathcal{P}_{m \to n} : \Delta_m \to \Delta_n, \quad n < m.$$
Under classical Gaussian processes, restricting a random field to a lower-dimensional submanifold causes a loss of $\frac{m-n}{2}$ derivatives in Sobolev space (standard Sobolev Trace Theorem).

### 4.2 Theorem 1.3 (Critical Isomorphic Trace for Priors — OBL-INF-003)
*Let $\mathcal{R}_{m \to n}^\alpha$ be the simplicial inter-dimensional Radon-Beta transform defined by:*
$$\mathcal{R}_{m \to n}^\alpha f(\mathbf{y}) = \int_{\mathcal{P}_{m \to n}^{-1}(\mathbf{y})} \mathcal{K}_\alpha(\mathbf{x}, \mathbf{y}) f(\mathbf{x}) \, d\mathcal{H}^{m-n}(\mathbf{x}).$$
*For the critical fractional parameter:*
$$\alpha^* = \frac{m - n}{2},$$
*the trace operator defines an exact topological isomorphism between Sobolev spaces of the same regularity:*
$$\mathcal{R}_{m \to n}^{\alpha^*} : H^s(\Delta_m) \xrightarrow{\sim} H^s(\Delta_n), \quad \forall s \ge 0.$$

**Significance for Bayesian Statistics:**  
When placing a prior on high-dimensional species ($m = 1000$) and aggregating into broad phyla ($n = 10$), setting $\alpha = \alpha^* = 495$ ensures that the aggregated prior on phyla retains the exact same smoothness, regularity, and predictive sharpness as the base prior, with zero derivative loss and zero variance explosion.

---

## 5. Summary: Operational Impact on Statistical Modeling

| Problem in Standard Statistics | Cause under Euclidean / Log-Ratio Modeling | Solution via Simplicial Beta-Laplacian |
| :--- | :--- | :--- |
| **Boundary Zero Divergence** | $\ln(0) = -\infty$ in ALR/CLR/ILR transformations. | Direct formulation on $\Delta_m$ via bounded Green's functions. |
| **Spurious Correlations** | Arbitrary pseudocount additions ($x_i + \epsilon$). | Intrinsic Cartan negative equicorrelation $-1/(m+1)^2$. |
| **Multi-Scale Inconsistency** | Hierarchical aggregation loses smoothness ($H^s \to H^{s - \frac{m-n}{2}}$). | Critical trace $\alpha^* = \frac{m-n}{2}$ preserves smoothness ($H^s \to H^s$). |
| **Matrix-Variate Extensions** | Ad-hoc diagonal log-normal covariance priors. | Siegel-Wishart matrix Beta operators $\mathcal{G}_{\mathbf{A}, \mathbf{B}}$ on $\mathcal{S}_{++}^m$. |
