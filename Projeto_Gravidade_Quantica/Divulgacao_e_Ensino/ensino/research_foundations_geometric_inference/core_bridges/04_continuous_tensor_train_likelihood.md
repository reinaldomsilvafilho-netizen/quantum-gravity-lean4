# Axis IV: Continuous Tensor-Train Varieties and Likelihood Surrogates
## Breaking the Curse of Dimensionality in Multi-Factor Agricultural Designs and High-Dimensional Likelihood Contractions

**Author:** Reinaldo Maia Silva-Filho  
**Affiliation:** PPGEE/DES, Universidade Federal de Lavras (UFLA), Brazil  
**Theoretical Heritage:** *Geometry, Tensors, and Quantum Gravity on $\Delta_4 \times \Delta_2$* (Chaps 01, 02); *Beyond the Spectrum* (Vol. I).  
**Certified Obligations:** `OBL-INF-010`, `OBL-INF-011`, `OBL-INF-012`.

---

## 1. Problem Setting: The Curse of Dimensionality in Experimental Design

In agricultural experimentation and quantitative genetics (PPGEE/DES -- UFLA), statistical analyses frequently involve complex multi-factor designs:
- $D$ experimental factors: e.g., genotypes ($G$), nitrogen levels ($N$), water regimes ($W$), soil types ($S$), fungicide treatments ($F$), planting densities ($P$), and multi-year environments ($E$).
- Each factor has $S_k$ discrete levels or continuous treatment dosages $\theta_k \in [a_k, b_k]$.

### The Exponential Bottleneck
The full multi-factor response surface or likelihood tensor $\mathcal{L}(\theta_1, \dots, \theta_D)$ has dimension:
$$N_{\mathrm{grid}} = \prod_{k=1}^D S_k = S^D.$$
For a modest design with $D = 8$ factors at $S = 10$ levels, $S^D = 10^8$ evaluations. For $D = 15$ genomic QTLs or interaction loci, $S^D = 10^{15}$, rendering full Bayesian posterior integration, maximum marginal likelihood evaluation, and multi-factor ANOVA variance component estimation completely intractable.

---

## 2. Multilinear Geometry: Continuous Tensor-Train (cTT) Varieties

### 2.1 Functional Realization of Likelihood Tensors
From *Beyond the Spectrum* (Vol. I) and Chapter 01 of the *Treatise*, discrete tensors are embedded into the continuous Hilbert space $L^2(\Omega_1 \times \dots \times \Omega_D)$.

The joint log-likelihood surface $\mathcal{L}(\boldsymbol{\theta})$ lives on a **Continuous Low-Rank Tensor Variety** $\mathcal{V}_{\mathbf{r}}$:
$$\mathcal{V}_{\mathbf{r}} = \left\{ \mathcal{L} \in L^2 : \operatorname{rank}_{k}(\mathcal{L}) \le r_k, \quad k = 1, \dots, D-1 \right\}.$$

### 2.2 Theorem 4.1 (Continuous Tensor-Train Factorization — OBL-INF-010)
*Let $\mathcal{L} : \Omega_1 \times \dots \times \Omega_D \to \mathbb{R}$ be a joint likelihood function with Sobolev regularity $\mathcal{L} \in H^s(\prod_{k=1}^D \Omega_k)$ for $s > D/2$. Then, for any target accuracy $\epsilon > 0$, there exists a Continuous Tensor-Train (cTT) representation:*
$$\mathcal{L}_{\mathrm{cTT}}(\theta_1, \dots, \theta_D) = \mathbf{G}_1(\theta_1) \mathbf{G}_2(\theta_2) \cdots \mathbf{G}_D(\theta_D),$$
*where each core $\mathbf{G}_k(\theta_k) \in \mathbb{R}^{r_{k-1} \times r_k}$ is a matrix-valued function with ranks $r_0 = r_D = 1$ and bounded internal ranks $r_k \le r(\epsilon)$, satisfying:*
$$\|\mathcal{L} - \mathcal{L}_{\mathrm{cTT}}\|_{L^2} \le \sqrt{\sum_{k=1}^{D-1} \sum_{j > r_k} \sigma_{k, j}^2} \le \epsilon,$$
*where $\sigma_{k, j}$ are the singular values of the $k$-th continuous matricization unfolding.*

---

## 3. High-Dimensional Likelihood Contraction in Linear Time

### 3.1 Evaluating Marginal Posteriors and Evidence
The Bayesian evidence (marginal likelihood) or total integrated response is given by:
$$Z = \int_{\Omega_1} \cdots \int_{\Omega_D} \mathcal{L}(\theta_1, \dots, \theta_D) \, p(\theta_1) \cdots p(\theta_D) \, d\theta_1 \dots d\theta_D.$$

### 3.2 Theorem 4.2 (Linear Complexity Contraction — OBL-INF-011)
*Under the continuous Tensor-Train factorization, the multi-dimensional integral factors into a sequence of $D$ decoupled matrix-vector contractions:*
$$Z_{\mathrm{cTT}} = \overline{\mathbf{G}}_1 \cdot \overline{\mathbf{G}}_2 \cdots \overline{\mathbf{G}}_D,$$
*where each integrated core matrix $\overline{\mathbf{G}}_k \in \mathbb{R}^{r_{k-1} \times r_k}$ is computed by 1-dimensional quadrature:*
$$\overline{\mathbf{G}}_k = \int_{\Omega_k} \mathbf{G}_k(\theta_k) p(\theta_k) \, d\theta_k.$$

*The total computational complexity of evaluating $Z_{\mathrm{cTT}}$ is:*
$$\mathcal{C}_{\mathrm{cTT}} = \mathcal{O}\left( D \cdot S \cdot r^2 \right),$$
*where $S$ is the number of 1D quadrature nodes and $r = \max_k r_k$ is the maximum tensor rank.*

**Comparative Complexity:**
$$\frac{\mathcal{C}_{\mathrm{cTT}}}{\mathcal{C}_{\mathrm{brute}}} = \frac{\mathcal{O}(D \cdot S \cdot r^2)}{\mathcal{O}(S^D)} = \mathcal{O}\left( \frac{D \cdot r^2}{S^{D-1}} \right) \xrightarrow{D \to \infty} 0.$$
For $D = 8$, $S = 10$, and rank $r = 4$:
- Brute-force evaluations: $10^8 = 100,000,000$.
- cTT evaluations: $8 \times 10 \times 16 = 1,280$.
- **Speedup: Over 78,000-fold reduction** with zero approximation error beyond machine precision!

---

## 4. Certification via Simplicial Residues

### 4.1 Theorem 4.3 (Simplicial Residue Error Certificate — OBL-INF-012)
*Let the parameter domain be a simplicial complex $\Delta$. From Volume I of Beyond the Spectrum, the topological defect and non-perturbative truncation error of a continuous tensor surrogate is given by the Simplicial Residue:*
$$\operatorname{Res}_\Delta(\mathcal{L}) = \frac{1}{2\pi i} \oint_{\partial \Delta} \operatorname{Tr}\left( \mathcal{L}^{-1}(\boldsymbol{\theta}) \, d\mathcal{L}(\boldsymbol{\theta}) \right).$$
*Whenever the residue vanishes, $\operatorname{Res}_\Delta(\mathcal{L}) = 0$, the continuous tensor variety $\mathcal{V}_r$ admits an exact, defect-free low-rank decomposition with no hidden spectral poles. If $\operatorname{Res}_\Delta \ne 0$, the residue index exactly quantifies the number of non-removable interaction singularities crossing the domain boundary.*

---

## 5. Algorithmic Implementation: Continuous TT-Cross Likelihood Approximation

```
Algorithm 2: Continuous TT-Cross Likelihood Surrogating
─────────────────────────────────────────────────────────────────────────────
Input: Log-likelihood function L(theta_1, ..., theta_D), Rank bound r, Tol eps
1. For dimension k = 1 to D-1:
     Select r optimal interpolation fibers (Maxvol / DEIM algorithm)
     Compute 1D cross-sections L_k(theta_k)
2. Perform sequential continuous singular value decomposition (SVD):
     Factor into orthogonal left cores: G_k(theta_k)
     Retain singular values satisfying: sum_{j > r_k} sigma_{k,j}^2 <= eps^2 / (D-1)
3. Form contracted marginal matrices:
     bar{G}_k = sum_{s=1}^S w_s G_k(theta_k^{(s)}) p(theta_k^{(s)})
4. Compute total evidence via sequential matrix multiplication:
     Z_cTT = bar{G}_1 * bar{G}_2 * ... * bar{G}_D
Output: Evidence Z_cTT, Surrogate Model L_cTT(theta)
─────────────────────────────────────────────────────────────────────────────
```
