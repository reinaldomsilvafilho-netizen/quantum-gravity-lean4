# Adversarial Mathematical Audit Report: Chapter 05

**Target:** *Inter-Dimensional Simplicial Transforms, Fractional Boundary Traces, and Grassmannian Beta-Kernels* (Author: Reinaldo Maia Silva-Filho)
**Date:** September 2026
**Overall Verdict:** REVISE

## Summary of Findings

The audit reveals that while the topological and functional-analytic frameworks (e.g., multiscale energy dissipation, barycentric preservation) are robust, there are **CRITICAL** mathematical flaws in the Fourier representations, exact inversion formulas, and matrix calculus definitions. The numerical and formal tests passed because they contained mirroring tautologies or tested scalar proxies rather than the explicit manifold formulations. 

### Severity Breakdown
- **CRITICAL:** Fourier Multiplier Representation (OBL-C05-001) incorrectly assumes kernel separability.
- **CRITICAL:** Grassmannian Dual Inversion (OBL-C05-007) commutes non-commuting operations.
- **CRITICAL:** Siegel-Wishart Operators (OBL-C05-010, 011) contain algebraically undefined matrix exponents.
- **PASS:** Coupled Mass/Energy (OBL-C05-005, 006), Barycentric Preservation (OBL-C05-009).

---

## Detailed Breakdown & Exact Mathematical Fixes

### 1. OBL-C05-001 & OBL-C05-002 (Prop 2.2 & Thm 3.1): Fourier Multiplier Representation
**Severity:** CRITICAL
**Location:** Proposition 2.2 (Eq. 2.4) and Theorem 3.1 (Lines 102, 144)

**Explanation:**
The derivation of the Fourier multiplier incorrectly factors the fractional Beta-kernel symbol $\widehat{\mathcal{K}}_\alpha$ outside the integral over $\operatorname{ker}(\mathbf{P})$. When transforming coordinates to the projected space via $\mathbf{k} = \mathbf{P}^T \boldsymbol{\xi} + \boldsymbol{\eta}$, the kernel evaluates at $-\mathbf{P}^T \boldsymbol{\xi} - \boldsymbol{\eta}$, which explicitly depends on the transverse fiber variable $\boldsymbol{\eta}$. Furthermore, the coordinate transformation is missing the Jacobian factor $(2\pi)^{n-m} \sqrt{\det(\mathbf{P}\mathbf{P}^T)}$. In Theorem 3.1, incorporating $\widehat{\mathcal{K}}_\alpha$ inside the integral actually *strengthens* the Sobolev proof, as the $\boldsymbol{\eta}$-decay of the kernel ensures convergence for all $s$ rather than just $s > \frac{m-n}{2}$.

**Exact Mathematical Fix:**
Replace Eq. 2.4 with the exact coupled fiber integral:
$$ \widehat{\mathcal{R}_{m \to n}^\alpha f}(\boldsymbol{\xi}) = (2\pi)^{n-m} \sqrt{\det(\mathbf{P}\mathbf{P}^T)} \int_{\operatorname{ker}(\mathbf{P})} \widehat{f}(\mathbf{P}^T \boldsymbol{\xi} + \boldsymbol{\eta}) \widehat{\mathcal{K}}_\alpha(-\mathbf{P}^T \boldsymbol{\xi} - \boldsymbol{\eta}) d\boldsymbol{\eta} $$

### 2. OBL-C05-007 (Thm 5.1): Grassmannian Dual Inversion Formula
**Severity:** CRITICAL
**Location:** Theorem 5.1 (Eq. 5.2)

**Explanation:**
The exact dual inversion formula incorrectly divides the $n$-dimensional slice projection $\widehat{g}_\theta(\boldsymbol{\xi})$ by the kernel symbol $\widehat{\mathcal{K}}_\alpha(\mathbf{P}_\theta^T \boldsymbol{\xi})$. Because the fractional Beta-transform is an $m$-dimensional spatial convolution prior to the affine slice projection, the frequencies in $\operatorname{ker}(\mathbf{P}_\theta)$ have already been irreversibly integrated out. One cannot perform a scalar deconvolution on the $n$-dimensional projection slices. The deconvolution must be performed in the full $m$-dimensional space *after* the Grassmannian backprojection has lifted the signal back to $\mathbb{R}^m$.

**Exact Mathematical Fix:**
Rewrite the inversion formula such that the Beta-kernel deconvolution occurs outside the slice integration:
$$ f(\mathbf{x}) = \frac{1}{(2\pi)^m} \int_{\mathbb{R}^m} e^{i \mathbf{k} \cdot \mathbf{x}} \frac{1}{\widehat{\mathcal{K}}_\alpha(-\mathbf{k})} \mathcal{F}_{\mathbb{R}^m}\left\{ \int_{\operatorname{Gr}(n,m)} d\mu(\theta) \int_{\mathbb{R}^n} e^{i \boldsymbol{\xi} \cdot \mathbf{P}_\theta \mathbf{w}} |\boldsymbol{\xi}|^{m-n} \widehat{g}_\theta(\boldsymbol{\xi}) d\boldsymbol{\xi} \right\}(\mathbf{k}) d\mathbf{k} $$

### 3. OBL-C05-010 & OBL-C05-011 (Def 7.1 & Thm 7.2): Siegel-Wishart Operator Parameters
**Severity:** CRITICAL
**Location:** Definition 7.1 (Eq. 7.2, 7.3) and Theorem 7.2 (Eq. 7.5)

**Explanation:**
The parameters $\mathbf{A}, \mathbf{B}$ are defined as positive-definite matrices $\operatorname{Sym}_m^+(\mathbb{R})$, but are then used as exponents for scalar determinants: $(\det \mathbf{Y})^{\mathbf{A} - \frac{m+1}{2}}$. Raising a scalar to a matrix power inside a scalar measure integral is algebraically ill-defined. Furthermore, the multivariate Gamma function $\Gamma_m$ is applied to a matrix, which requires diagonal invariance that does not hold for general positive-definite matrices. The classical Siegel-Wishart Beta operator acts on matrices but relies on *scalar* shape parameters $a, b \in \mathbb{R}$.

**Exact Mathematical Fix:**
1. Re-define the parameters as scalars: $a, b \in \mathbb{R}$ with $a, b > \frac{m-1}{2}$.
2. Update the measure in Eq. 7.2 to: 
   $$ (\det \mathbf{Y})^{a - \frac{m+1}{2}} (\det(\mathbf{I}_m - \mathbf{Y}))^{b - \frac{m+1}{2}} d\mathbf{Y} $$
3. Update the normalization constant in Eq. 7.3 to use the scalar argument:
   $$ \Gamma_m(a) = \pi^{m(m-1)/4}\prod_{j=1}^m \Gamma\left(a - \frac{j-1}{2}\right) $$
4. In Theorem 7.2 (Eq. 7.5), replace the matrix Pochhammer $[\mathbf{A}]_\lambda$ with the standard generalized multivariate Pochhammer symbol:
   $$ (a)_\lambda = \prod_{j=1}^m \frac{\Gamma\left(a - \frac{j-1}{2} + \lambda_j\right)}{\Gamma\left(a - \frac{j-1}{2}\right)} $$
   Yielding the eigenvalue ratio: $\frac{(a)_\lambda}{(a+b)_\lambda}$.
