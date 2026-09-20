# ADVERSARIAL MATHEMATICAL AUDIT REPORT (PAPER 1)

**Paper Title:** *Bakry-Émery Ricci Curvature, Poincaré Spectral Gaps, and Guaranteed MCMC Ergodicity in High-Dimensional Bayesian Generalized Linear Models*  
**Author:** Reinaldo M. Silva-Filho  
**Affiliation:** Programa de Pós-Graduação em Estatística e Experimentação Agropecuária (PPGEE/DES), Departamento de Estatística (DES), Universidade Federal de Lavras (UFLA), Lavras, MG, Brazil  
**Funding:** Coordenação de Aperfeiçoamento de Pessoal de Nível Superior – Brasil (CAPES) – Código de Financiamento 001  
**Target Journal:** *Journal of the Royal Statistical Society: Series B (Statistical Methodology)*  
**Auditor:** Independent Adversarial Mathematical Proof & Soundness Auditor  
**Date of Audit:** September 11, 2026  
**Audited Artifacts:**
1. LaTeX Manuscript: `paper1_bayesian_glms.tex`
2. Proof Obligation Ledger: `LEDGER_PAPER1.md`
3. Numerical & Inverse Verification Engine: `verify_paper1_numerical.py`
4. Lean 4 Formalization: `BakryEmery.lean` (`GeometricStatistics/BakryEmery.lean`)

---

## 1. Executive Summary & Verdict

### Official Verdict: **REVISE (Major Mathematical & Formal Revisions Required)**

The core conceptual thesis of the paper—that complete separation in Bayesian Generalized Linear Models corresponds geometrically to a Ricci curvature collapse on the posterior metric-measure space, and that a geometrically conjugate information prior enforces an unconditional Bakry-Émery curvature bound $\mathrm{Ric}_\infty \succeq \lambda_0 \mathbf{I}_p > \mathbf{0}$—is **fundamentally sound, mathematically brilliant, and original**. The derivation of the Bochner-Weitzenböck identity (Proposition 2.2), the uniform $CD(K^*, \infty)$ bound (Theorem 3.1), and the pathwise synchronous coupling contraction in $W_2$ distance (Theorem 3.3) are mathematically correct.

However, an unsparing adversarial audit has uncovered **multiple critical and major defects** across the manuscript proofs, the numerical test harness, and the Lean 4 formalization:

1. **CRITICAL FORMAL DEFECT (CV-04 / CV-06 Semantic Vacuity in Lean 4):**  
   The Lean 4 formal proof file `BakryEmery.lean` does **not** formalize the mathematical theorems of Paper 1. Every single theorem is declared over the natural numbers (`Nat`), substituting deep differential geometry, Sobolev spaces, and SDE coupling with elementary Presburger arithmetic tautologies (e.g., `norm_sq ≥ 0 := by omega`). While `lake build` exits with code 0 and 0 `sorry`, this is a **symbolic surrogate mock** that possesses zero mathematical fidelity to the paper.
2. **MAJOR PROOF GAP IN THEOREM 3.2 (Eigenfunction Compact Support Fallacy):**  
   The proof of Theorem 3.2 (Poincaré spectral gap) begins with the premise: *"Let $f \in C_c^\infty(\mathbb{R}^p)$ be an eigenfunction of $-\mathcal{L}$ with eigenvalue $\lambda_1$..."*. By the classical Aronszajn/Hörmander unique continuation principle for elliptic operators, **no non-trivial eigenfunction of $-\mathcal{L} = -\Delta + \langle \nabla U, \nabla \cdot \rangle$ can have compact support in $\mathbb{R}^p$**. If an eigenfunction vanishes outside a compact ball, it vanishes identically everywhere. The proof must be restructured via Bakry-Émery semigroup variance interpolation on arbitrary $C_c^\infty$ test functions, rather than positing compactly supported eigenfunctions.
3. **MAJOR FLAW IN THEOREM 3.4 (Conflation of MALA and ULA; Measure-Theoretic Nonsense):**  
   - **Discretization Bias in TV Bound:** Equation (369) asserts that the Total Variation distance between the discrete MALA iterate and $\pi$ is bounded by $(1 - \frac{1}{4}\gamma K^*)^k + \mathcal{O}(\gamma^{3/2} p^{1/2})$. Because MALA includes an exact Metropolis-Hastings acceptance filter, its stationary distribution is **exactly** $\pi$. The non-vanishing bias $\mathcal{O}(\gamma^{3/2} p^{1/2})$ is characteristic of *Unadjusted* Langevin Algorithms (ULA), not MALA.
   - **Omission of Dimension Dependence in Step Size:** Theorem 3.4 assumes $\gamma \le \frac{K^*}{2L^2}$ without dimensional restriction. However, Dwyer et al. (2019) and Chewi et al. (2021) prove that maintaining a non-vanishing acceptance rate in high dimensions requires $\gamma = \mathcal{O}(p^{-1/3})$. In high dimensions ($p = 4,800$), a step size independent of $p$ causes the rejection probability to approach 1, collapsing the spectral gap.
   - **Measure-Theoretic Blunder:** Writing $\sqrt{\chi^2(\delta_{\boldsymbol{\theta}_0} \mid \pi)}$ is mathematically undefined; a Dirac delta measure has infinite $\chi^2$-divergence ($\chi^2 = +\infty$) relative to any absolutely continuous probability measure on $\mathbb{R}^p$.
4. **MAJOR CODE DEFECT IN NUMERICAL BATTERY 5 (Metropolis-Hastings Bypass):**  
   In `verify_paper1_numerical.py`, Battery 5 (lines 251-253) completely omits the Metropolis-Hastings accept/reject ratio, unconditionally accepting every proposal (`theta = theta_prop; accepted += 1`). Battery 5 tested an unadjusted Euler-Maruyama discretization, not Algorithm 4.1.

---

## 2. Summary Classification of Findings

| Severity | Count | Affected Obligations / Files | Core Issue |
| :--- | :---: | :--- | :--- |
| **CRITICAL** | 1 | `BakryEmery.lean` (OBL-001 to 007) | 100% semantic vacuity; all 7 theorems formalized over `Nat` with zero differential geometry or measure theory. |
| **MAJOR** | 4 | OBL-P01-004 (Thm 3.2), OBL-P01-006 (Thm 3.4), OBL-P01-007 (Alg 4.1), `verify_paper1_numerical.py` | Elliptic unique continuation violation in Thm 3.2; MALA/ULA conflation, step-size dimension blindness, and $\chi^2(\delta_{\boldsymbol{\theta}_0}\mid \pi)=\infty$ in Thm 3.4; MH acceptance bypass in Battery 5. |
| **MINOR** | 2 | OBL-P01-007 (Alg 4.1), OBL-P01-003 (Thm 3.1) | Metric tensor derivative (Christoffel correction) omitted in Alg 4.1 without explicit approximation disclaimer; rank-deficiency of Fisher term when $p > n$ needs explicit statement that $K^* = \lambda_0$. |
| **COSMETIC** | 2 | LaTeX References, Table 1 | Double-counting determinant notation in Eq. (433); citation keys formatting. |

---

## 3. Detailed Obligation-by-Obligation Mathematical Audit

### OBL-P01-001: Weighted Metric-Measure Space & Carré du Champ (Def 2.1)
- **Status:** **PASS WITH ADVISORY**
- **Mathematical Examination:**  
  The weighted metric-measure space $(\mathbb{R}^p, g_{\mathrm{Euclid}}, \pi)$ with $d\pi = \frac{1}{Z} e^{-U(\boldsymbol{\theta})} d\boldsymbol{\theta}$ and infinitesimal generator $\mathcal{L} f = \Delta f - \langle \nabla U, \nabla f \rangle$ is scrutinized.
  1. *Integration by Parts (IBP):*  
     We verify:
     $$\int_{\mathbb{R}^p} f (\mathcal{L} g) d\pi = \frac{1}{Z} \int_{\mathbb{R}^p} f \nabla \cdot \left( e^{-U} \nabla g \right) d\boldsymbol{\theta} = -\frac{1}{Z} \int_{\mathbb{R}^p} \langle \nabla f, \nabla g \rangle e^{-U} d\boldsymbol{\theta} = -\int_{\mathbb{R}^p} \Gamma(f, g) d\pi.$$
     Symmetry $\int f (\mathcal{L} g) d\pi = \int g (\mathcal{L} f) d\pi$ holds identically for all test functions $f, g \in C_c^\infty(\mathbb{R}^p)$.
  2. *Noise Normalization:*  
     The Langevin SDE $d\boldsymbol{\theta}_t = -\nabla U(\boldsymbol{\theta}_t) dt + \sqrt{2} d\mathbf{B}_t$ has quadratic covariation $d[\theta_i, \theta_j]_t = 2 \delta_{ij} dt$. By Itô's formula, the Itô correction is $\frac{1}{2} \sum_{i,j} \partial_{ij} f (2 \delta_{ij}) = \Delta f$. The drift is $-\langle \nabla U, \nabla f \rangle$. The generator is $\mathcal{L} f = \Delta f - \langle \nabla U, \nabla f \rangle$. The factor $\sqrt{2}$ matches the unscaled Laplacian $\Delta$ exactly.
  3. *Carré du Champ:*  
     $\Gamma(f, g) = \frac{1}{2}[\mathcal{L}(fg) - f\mathcal{L}g - g\mathcal{L}f] = \langle \nabla f, \nabla g \rangle$. Derivation is exact.
- **Advisory:**  
  The manuscript should explicitly note that because $U$ is strongly convex ($\nabla^2 U \succeq \lambda_0 \mathbf{I}_p$), $-\mathcal{L}$ is essentially self-adjoint on $C_c^\infty(\mathbb{R}^p)$ (Bakry, Gentil, Ledoux, 2014, Proposition 3.2.1).

---

### OBL-P01-002: Bochner-Weitzenböck Identity on Weighted Spaces (Prop 2.2)
- **Status:** **WATERTIGHT (PASS)**
- **Mathematical Examination:**  
  The identity states that for all $f \in C_c^\infty(\mathbb{R}^p)$:
  $$\Gamma_2(f, f) = \|\nabla^2 f\|_{\mathrm{HS}}^2 + \langle \nabla f, \nabla^2 U \nabla f \rangle.$$
  Let us scrutinize the exact cancellation of terms:
  - First term: $\frac{1}{2}\mathcal{L}\|\nabla f\|^2 = \frac{1}{2}\Delta \|\nabla f\|^2 - \frac{1}{2}\langle \nabla U, \nabla \|\nabla f\|^2 \rangle$.
    Since $\nabla \|\nabla f\|^2 = 2 \nabla^2 f \nabla f$:
    $$\frac{1}{2}\mathcal{L}\|\nabla f\|^2 = \|\nabla^2 f\|_{\mathrm{HS}}^2 + \langle \nabla f, \nabla(\Delta f) \rangle - \langle \nabla^2 f \nabla U, \nabla f \rangle.$$
  - Second term: $\Gamma(f, \mathcal{L}f) = \langle \nabla f, \nabla(\mathcal{L}f) \rangle$.
    $$\nabla(\mathcal{L}f) = \nabla(\Delta f) - \nabla \langle \nabla U, \nabla f \rangle = \nabla(\Delta f) - \nabla^2 U \nabla f - \nabla^2 f \nabla U.$$
    Taking the inner product with $\nabla f$:
    $$\Gamma(f, \mathcal{L}f) = \langle \nabla f, \nabla(\Delta f) \rangle - \langle \nabla f, \nabla^2 U \nabla f \rangle - \langle \nabla f, \nabla^2 f \nabla U \rangle.$$
  - Subtracting:
    $$\Gamma_2(f, f) = \frac{1}{2}\mathcal{L}\|\nabla f\|^2 - \Gamma(f, \mathcal{L}f) = \|\nabla^2 f\|_{\mathrm{HS}}^2 + \langle \nabla f, \nabla^2 U \nabla f \rangle.$$
    The high-order third derivative term $\langle \nabla f, \nabla(\Delta f) \rangle$ cancels identically.
    The drift cross-term $-\langle \nabla^2 f \nabla U, \nabla f \rangle - (-\langle \nabla f, \nabla^2 f \nabla U \rangle)$ cancels identically by the symmetry of the Hessian tensor $\nabla^2 f = (\nabla^2 f)^T$.
  - The remaining sign on $\langle \nabla f, \nabla^2 U \nabla f \rangle$ is strictly positive.
- **Verdict:** Watertight. Signs, indices, and cancellations are verified with zero flaws.

---

### OBL-P01-003: Uniform $CD(K^*, \infty)$ Bound under Complete Separation (Thm 3.1)
- **Status:** **PASS WITH ADVISORY**
- **Mathematical Examination:**  
  The posterior potential is $U(\boldsymbol{\theta}) = -\ell(\boldsymbol{\theta}) + V_0(\boldsymbol{\theta})$.
  - Likelihood Hessian: $\nabla^2(-\ell(\boldsymbol{\theta})) = \mathbf{X}^T \mathbf{W}(\boldsymbol{\theta}) \mathbf{X}$, where $\mathbf{W}(\boldsymbol{\theta}) = \operatorname{diag}\left(\frac{b''(\mathbf{x}_i^T \boldsymbol{\theta})}{a(\phi)}\right)$. For canonical logistic regression, $b''(\eta) = \frac{e^\eta}{(1+e^\eta)^2} > 0$.
  - Under complete separation, along the open ray $\boldsymbol{\theta} = c \boldsymbol{\beta}^*$ with $c \to \infty$:
    $$\mathbf{x}_i^T \boldsymbol{\beta}^* > 0 \implies \eta_i \to +\infty \implies b''(\eta_i) \to 0,$$
    $$\mathbf{x}_i^T \boldsymbol{\beta}^* < 0 \implies \eta_i \to -\infty \implies b''(\eta_i) \to 0.$$
    Hence $\lim_{c \to \infty} \mathbf{X}^T \mathbf{W}(c \boldsymbol{\beta}^*) \mathbf{X} = \mathbf{0}$.
  - Under the Geometrically Conjugate Prior:
    $$\nabla^2 V_0(\boldsymbol{\theta}) \succeq \lambda_0 \mathbf{I}_p + \kappa_0 \mathbf{X}^T \mathbf{X}, \quad \lambda_0 > 0, \kappa_0 \ge 0.$$
    The total Hessian satisfies:
    $$\nabla^2 U(\boldsymbol{\theta}) \succeq \lambda_0 \mathbf{I}_p + \mathbf{X}^T (\mathbf{W}(\boldsymbol{\theta}) + \kappa_0 \mathbf{I}_n) \mathbf{X}.$$
    Since $b'' \ge 0$ and $\kappa_0 \ge 0$, the matrix $\mathbf{W}(\boldsymbol{\theta}) + \kappa_0 \mathbf{I}_n \succeq \mathbf{0}$, which implies that $\mathbf{X}^T (\mathbf{W}(\boldsymbol{\theta}) + \kappa_0 \mathbf{I}_n) \mathbf{X} \succeq \mathbf{0}$ for all $\boldsymbol{\theta} \in \mathbb{R}^p$.
    Therefore, for any unit vector $\mathbf{v} \in \mathbb{R}^p$:
    $$\mathbf{v}^T \nabla^2 U(\boldsymbol{\theta}) \mathbf{v} \ge \lambda_0 \|\mathbf{v}\|_2^2 + 0 = \lambda_0 > 0.$$
    Taking the infimum over $\boldsymbol{\theta} \in \mathbb{R}^p$:
    $$K^* = \inf_{\boldsymbol{\theta} \in \mathbb{R}^p} \lambda_{\min}(\nabla^2 U(\boldsymbol{\theta})) \ge \lambda_0 > 0.$$
  - *Proper Prior Check:* The canonical prior $\pi_0 = \mathcal{N}(\mathbf{0}, (\lambda_0 \mathbf{I}_p + \kappa_0 \mathbf{X}^T \mathbf{X})^{-1})$ has precision matrix $\boldsymbol{\Sigma}_0^{-1} \succeq \lambda_0 \mathbf{I}_p \succ \mathbf{0}$. Because $\lambda_0 > 0$, $\boldsymbol{\Sigma}_0$ exists, is finite, and defines a strictly proper Gaussian measure on $\mathbb{R}^p$ with finite normalizing constant.
- **Advisory:**  
  When $p > n$, $\operatorname{rank}(\mathbf{X}) \le n < p$. Thus $\mathbf{X}^T (\mathbf{W}(\boldsymbol{\theta}) + \kappa_0 \mathbf{I}_n) \mathbf{X}$ has at least $p - n$ zero eigenvalues in $\ker(\mathbf{X})$. Consequently, when $p > n$, the term $\inf_{\boldsymbol{\theta}} \lambda_{\min}(\mathbf{X}^T(\mathbf{W} + \kappa_0 \mathbf{I})\mathbf{X})$ is identically 0. Thus $K^* = \lambda_0$ exactly. The text in equation (238) should explicitly state:
  *"When $p > n$, $\lambda_{\min}(\mathbf{X}^T(\mathbf{W} + \kappa_0 \mathbf{I}_n)\mathbf{X}) = 0$, yielding $K^* = \lambda_0$."*

---

### OBL-P01-004: Lichnerowicz-Bakry-Émery Poincaré Spectral Gap (Thm 3.2)
- **Status:** **MAJOR REVISION REQUIRED (PROOF GAP IDENTIFIED)**
- **Mathematical Examination:**  
  The theorem claims:
  $$\lambda_1(-\mathcal{L}) \ge K^* \ge \lambda_0 > 0 \implies \|\mathcal{P}_t f - \mathbb{E}_\pi[f]\|_{L^2(\pi)} \le e^{-K^* t} \|f - \mathbb{E}_\pi[f]\|_{L^2(\pi)}.$$
  The stated bound is mathematically true, but the proof presented in lines 283–303 contains a fatal mathematical gap:
  1. *The Eigenfunction Compact Support Fallacy:*  
     Line 283 states: *"Let $f \in C_c^\infty(\mathbb{R}^p)$ be an eigenfunction of $-\mathcal{L}$ with eigenvalue $\lambda_1$, so that $-\mathcal{L} f = \lambda_1 f$, with $\mathbb{E}_\pi[f] = 0$."*  
     **This assumption is mathematically impossible on $\mathbb{R}^p$.**  
     The eigenvalue equation is:
     $$\Delta f - \langle \nabla U, \nabla f \rangle + \lambda_1 f = 0.$$
     This is a second-order linear elliptic partial differential equation with smooth coefficients on $\mathbb{R}^p$. By the classical **Aronszajn-Cordes Unique Continuation Theorem** (Aronszajn, 1957, *J. Math. Pures Appl.*), if a smooth solution $f$ to an elliptic PDE vanishes on any non-empty open set (which is required if $f$ has compact support, i.e., $f \equiv 0$ on $\mathbb{R}^p \setminus B_R(\mathbf{0})$), then $f$ must vanish identically everywhere on $\mathbb{R}^p$ ($f \equiv 0$). Therefore, **no non-trivial eigenfunction of $-\mathcal{L}$ can belong to $C_c^\infty(\mathbb{R}^p)$**.
  2. *Unjustified Boundary Terms:*  
     Because true eigenfunctions on $\mathbb{R}^p$ have unbounded support (e.g., Hermite polynomials for the Ornstein-Uhlenbeck process), one cannot assert $\int \mathcal{L}\Gamma(f, f) d\pi = 0$ without verifying that the boundary flux at infinity vanishes:
     $$\lim_{R \to \infty} \int_{\partial B_R} \langle \nabla \Gamma(f, f), \mathbf{n} \rangle e^{-U} d\mathcal{H}^{p-1} = 0.$$
- **Required Remediation:**  
  The proof must not appeal to compactly supported eigenfunctions. Instead, prove the Poincaré inequality directly for *arbitrary* test functions $f \in C_c^\infty(\mathbb{R}^p)$ using the standard Bakry-Émery semigroup variance interpolation:
  - Define $\phi(s) = \mathbb{E}_\pi[(\mathcal{P}_s f)^2] - (\mathbb{E}_\pi[f])^2$.
  - Show $\phi'(s) = -2 \int \Gamma(\mathcal{P}_s f, \mathcal{P}_s f) d\pi$.
  - Define $\psi(s) = \int \Gamma(\mathcal{P}_s f, \mathcal{P}_s f) d\pi$. By the Bochner identity and $CD(K^*, \infty)$, show $\psi'(s) \le -2 K^* \psi(s)$, which integrates to $\psi(s) \le e^{-2 K^* s} \psi(0)$.
  - Integrate $\phi'(s)$ from $0$ to $\infty$:
    $$\operatorname{Var}_\pi(f) = -\int_0^\infty \phi'(s) ds = 2 \int_0^\infty \psi(s) ds \le 2 \psi(0) \int_0^\infty e^{-2 K^* s} ds = \frac{1}{K^*} \int \Gamma(f, f) d\pi.$$
  This establishes $\operatorname{Var}_\pi(f) \le \frac{1}{K^*} \int \|\nabla f\|^2 d\pi$ for all $f \in C_c^\infty(\mathbb{R}^p)$ without any eigenfunction assumptions.

---

### OBL-P01-005: Non-Asymptotic 2-Wasserstein Exponential Contraction (Thm 3.3)
- **Status:** **WATERTIGHT (PASS)**
- **Mathematical Examination:**  
  The synchronous coupling of two Langevin diffusions driven by identical Brownian motion $\mathbf{B}_t$:
  $$d\boldsymbol{\theta}_t = -\nabla U(\boldsymbol{\theta}_t) dt + \sqrt{2} d\mathbf{B}_t, \quad d\boldsymbol{\psi}_t = -\nabla U(\boldsymbol{\psi}_t) dt + \sqrt{2} d\mathbf{B}_t.$$
  The difference vector $\boldsymbol{\delta}_t = \boldsymbol{\theta}_t - \boldsymbol{\psi}_t$ satisfies the pathwise random ODE:
  $$\frac{d\boldsymbol{\delta}_t}{dt} = -(\nabla U(\boldsymbol{\theta}_t) - \nabla U(\boldsymbol{\psi}_t)).$$
  Differentiating the squared Euclidean distance:
  $$\frac{d}{dt}\|\boldsymbol{\delta}_t\|_2^2 = -2 \langle \boldsymbol{\theta}_t - \boldsymbol{\psi}_t, \nabla U(\boldsymbol{\theta}_t) - \nabla U(\boldsymbol{\psi}_t) \rangle.$$
  By the mean value theorem along the line segment:
  $$\nabla U(\boldsymbol{\theta}_t) - \nabla U(\boldsymbol{\psi}_t) = \left[ \int_0^1 \nabla^2 U((1-s)\boldsymbol{\psi}_t + s \boldsymbol{\theta}_t) ds \right] (\boldsymbol{\theta}_t - \boldsymbol{\psi}_t).$$
  Since $\nabla^2 U(\mathbf{z}) \succeq K^* \mathbf{I}_p$ uniformly for all $\mathbf{z} \in \mathbb{R}^p$, the integrated matrix satisfies $\int_0^1 \nabla^2 U ds \succeq K^* \mathbf{I}_p$. Thus:
  $$\langle \boldsymbol{\theta}_t - \boldsymbol{\psi}_t, \nabla U(\boldsymbol{\theta}_t) - \nabla U(\boldsymbol{\psi}_t) \rangle \ge K^* \|\boldsymbol{\theta}_t - \boldsymbol{\psi}_t\|_2^2.$$
  This yields the strict differential inequality:
  $$\frac{d}{dt} \|\boldsymbol{\delta}_t\|_2^2 \le -2 K^* \|\boldsymbol{\delta}_t\|_2^2 \implies \|\boldsymbol{\delta}_t\|_2 \le e^{-K^* t} \|\boldsymbol{\delta}_0\|_2 \quad \text{almost surely}.$$
  Taking the expectation over an optimal coupling $(\boldsymbol{\theta}_0, \boldsymbol{\psi}_0) \sim \Pi^*(\mu, \nu)$ achieving $W_2^2(\mu, \nu) = \mathbb{E}[\|\boldsymbol{\theta}_0 - \boldsymbol{\psi}_0\|_2^2]$:
  $$W_2^2(\mathcal{P}_t \mu, \mathcal{P}_t \nu) \le \mathbb{E}[\|\boldsymbol{\theta}_t - \boldsymbol{\psi}_t\|_2^2] \le e^{-2 K^* t} \mathbb{E}[\|\boldsymbol{\theta}_0 - \boldsymbol{\psi}_0\|_2^2] = e^{-2 K^* t} W_2^2(\mu, \nu).$$
  Taking the square root proves $W_2(\mathcal{P}_t \mu, \mathcal{P}_t \nu) \le e^{-K^* t} W_2(\mu, \nu)$.
- **Verdict:** Watertight. The argument is classical, rigorous, and completely free of gaps.

---

### OBL-P01-006: Discrete MALA Total Variation Mixing Complexity (Thm 3.4)
- **Status:** **MAJOR REVISION REQUIRED (THEORETICAL FLAW IDENTIFIED)**
- **Mathematical Examination:**  
  Theorem 3.4 contains three distinct mathematical errors:
  1. *Conflation of MALA with ULA:*  
     Equation (369) bounds the Total Variation error by:
     $$\|\mathcal{T}_\gamma^k(\boldsymbol{\theta}_0, \cdot) - \pi\|_{\mathrm{TV}} \le \frac{1}{2}\sqrt{\chi^2(\delta_{\boldsymbol{\theta}_0}\mid \pi)}\left(1 - \frac{1}{4}\gamma K^*\right)^k + \mathcal{O}\left(\gamma^{3/2} p^{1/2}\right).$$
     In Unadjusted Langevin Algorithms (ULA), discretization bias causes the stationary measure $\pi_\gamma$ to differ from $\pi$, leaving a non-vanishing asymptotic bias $\mathcal{O}(\gamma \sqrt{p})$.  
     **However, MALA has an exact Metropolis-Hastings acceptance filter.** Reversibility with respect to $\pi$ guarantees that $\pi$ is the **exact invariant distribution** of $\mathcal{T}_\gamma$. Therefore:
     $$\lim_{k \to \infty} \|\mathcal{T}_\gamma^k(\boldsymbol{\theta}_0, \cdot) - \pi\|_{\mathrm{TV}} = 0.$$
     Adding an additive bias $+\mathcal{O}(\gamma^{3/2} p^{1/2})$ to the upper bound of a Metropolis-adjusted chain is a theoretical error resulting from conflating ULA discretization analysis with MALA geometric ergodicity.
  2. *Omission of High-Dimensional Step Size Scaling:*  
     The hypothesis specifies only $\gamma \le \frac{K^*}{2L^2}$, with no dependence on dimension $p$.  
     In high dimensions, the proposal increment has norm $\|\boldsymbol{\theta}^* - \boldsymbol{\theta}\| \approx \sqrt{2\gamma p}$. By the Taylor expansion of the log-acceptance ratio (Dwivedi et al., 2019; Chewi et al., 2021):
     $$\mathbb{E}[1 - \alpha(\boldsymbol{\theta}, \boldsymbol{\theta}^*)] = \mathcal{O}\left(\gamma^{3/2} p^{1/2}\right).$$
     To keep the acceptance rate bounded away from 0 (e.g., $\mathbb{E}[\alpha] \ge 0.5$), the step size must satisfy:
     $$\gamma = \mathcal{O}\left(p^{-1/3}\right).$$
     If $\gamma$ is chosen as a constant independent of $p$ (e.g., $\gamma = K^*/(2L^2)$), then for the paper's application where $p = 4,800$, $\gamma^{3/2} p^{1/2} \gg 1$, the acceptance rate collapses to 0, and the Markov chain stagnates. The condition $\gamma = \mathcal{O}(\min\{K^*/L^2, p^{-1/3}\})$ is mandatory.
  3. *Dirac Mass $\chi^2$-Divergence Singularity:*  
     The term $\sqrt{\chi^2(\delta_{\boldsymbol{\theta}_0} \mid \pi)}$ is written in (369). The $\chi^2$-divergence of a point mass $\delta_{\boldsymbol{\theta}_0}$ with respect to a Lebesgue-continuous distribution $\pi$ is:
     $$\chi^2(\delta_{\boldsymbol{\theta}_0} \mid \pi) = \int_{\mathbb{R}^p} \left(\frac{d\delta_{\boldsymbol{\theta}_0}}{d\pi}\right)^2 d\pi - 1 = +\infty.$$
     The bound as written evaluates to $\infty$ for any deterministic initialization $\boldsymbol{\theta}_0$. The initial distribution must be a warm start $\mu_0$ satisfying $\chi^2(\mu_0 \mid \pi) < \infty$, or the bound must be stated via $W_2$ coupling or relative entropy $D_{\mathrm{KL}}(\mu_0 \parallel \pi)$.

---

### OBL-P01-007: CIG-Langevin Algorithm & Metric Tensor (Alg 4.1)
- **Status:** **PASS WITH ADVISORY & CODE PATCH REQUIRED**
- **Mathematical Examination:**  
  1. *Metric Positive Definiteness:*  
     $$\mathbf{G}_k = \mathbf{X}^T (\mathbf{W}_k + \kappa_0 \mathbf{I}_n) \mathbf{X} + \lambda_0 \mathbf{I}_p.$$
     Because $\mathbf{W}_k \succeq \mathbf{0}$, $\kappa_0 \ge 0$, and $\lambda_0 > 0$, we have $\lambda_{\min}(\mathbf{G}_k) \ge \lambda_0 > 0$. The Cholesky factor $\mathbf{L}_k$ is guaranteed to exist and be strictly well-conditioned with condition number $\kappa(\mathbf{G}_k) \le \frac{\lambda_{\max}(\mathbf{G}_k)}{\lambda_0} < \infty$.
  2. *Metric Derivative Discrepancy:*  
     In exact Riemannian Manifold MALA (Girolami & Calderhead, 2011), the Langevin drift on a manifold $(\mathbb{R}^p, \mathbf{G})$ contains a Christoffel correction term:
     $$[\mathbf{m}(\boldsymbol{\theta})]_i = \theta_i - \gamma [\mathbf{G}^{-1}(\boldsymbol{\theta}) \nabla U(\boldsymbol{\theta})]_i + \gamma |\mathbf{G}(\boldsymbol{\theta})|^{-1/2} \sum_j \frac{\partial}{\partial \theta_j} \left( |\mathbf{G}(\boldsymbol{\theta})|^{1/2} G^{ij}(\boldsymbol{\theta}) \right).$$
     Algorithm 4.1 omits the second-order metric derivative term. While this is standard in simplified "quasi-Newton" or position-dependent Langevin algorithms, the manuscript must explicitly clarify that Algorithm 4.1 uses a simplified drift, whose non-reversibility is fully corrected by the Metropolis-Hastings step.
  3. *MH Ratio Determinant Formulation:*  
     In equation (433), the acceptance ratio is written as:
     $$\alpha = \min\left(1, \frac{\exp(-U(\boldsymbol{\theta}^*)) \det(\mathbf{L}^*) q(\boldsymbol{\theta}_k \mid \boldsymbol{\theta}^*)}{\exp(-U(\boldsymbol{\theta}_k)) \det(\mathbf{L}_k) q(\boldsymbol{\theta}^* \mid \boldsymbol{\theta}_k)}\right).$$
     If $q(\boldsymbol{\theta}^* \mid \boldsymbol{\theta}_k)$ is the Gaussian density with respect to Lebesgue measure, its normalizing constant already includes $(\det \mathbf{G}_k)^{1/2} = \det \mathbf{L}_k$. Writing $\det(\mathbf{L}^*)$ outside $q$ double-counts the volume element unless $q$ is defined as the unnormalized exponential $\exp(-\frac{1}{4\gamma}(\boldsymbol{\theta}^* - \mathbf{m}_k)^T \mathbf{G}_k (\boldsymbol{\theta}^* - \mathbf{m}_k))$. This definition must be clarified in the text.

---

## 4. Anti-Vacuity & Semantic Soundness Audit: Lean 4 Formalization

### 4.1 Audit against Lean 4 Cheat Vector Matrix (CV-01 to CV-06)

| Vector ID | Pattern / Vector | Automated Detection | Status | Audit Finding |
| :--- | :--- | :--- | :---: | :--- |
| **CV-01** | `sorry` / `admit` | `\b(sorry\|admit)\b` | **CLEAN** | 0 instances found in `BakryEmery.lean`. |
| **CV-02** | Unapproved Axioms | `\baxiom\s+\w+` | **CLEAN** | 0 unapproved axioms declared. |
| **CV-03** | Vacuous Hypothesis | `(\bh\s*:\s*False\|\b0\s*=\s*1\b)` | **CLEAN** | No explicit inconsistent hypotheses. |
| **CV-04** | Tautological Triviality | RHS == LHS or unconstrained def | **FAIL** | All theorems are Presburger arithmetic tautologies over `Nat`. |
| **CV-05** | Circular Reasoning | Cycle in lemma dependencies | **CLEAN** | Dependency graph is acyclic. |
| **CV-06** | Model Drift | Proves different statement from paper | **FATAL** | Complete disconnect between Lean code and LaTeX manuscript. |

### 4.2 Deep Semantic Analysis of `BakryEmery.lean`

The Lean 4 file `BakryEmery.lean` claims to certify OBL-P01-001 through OBL-P01-007 with "0 Sorry". However, examination of the actual types reveals total semantic vacuity:

```lean
-- CLAIMED: OBL-P01-001: Positivity of the Hilbert-Schmidt norm of the Hessian
theorem hessian_hilbert_schmidt_nonneg (norm_sq : Nat) :
    norm_sq ≥ 0 := by
  omega
```
*Adversarial Critique:*  
This theorem does **not** take a function $f: \mathbb{R}^p \to \mathbb{R}$, does **not** compute a Hessian $\nabla^2 f$, and does **not** compute a Hilbert-Schmidt norm. It merely asserts that any natural number $n \in \mathbb{N}$ is non-negative. This is an intrinsic property of the inductive type `Nat` (`Nat.zero_le`), completely vacuous of any differential geometry.

```lean
-- CLAIMED: OBL-P01-005: 2-Wasserstein synchronous coupling exponential contraction
theorem wasserstein_contraction_positivity (w2_0 k_star : Nat)
    (h_w2 : w2_0 > 0)
    (h_k : k_star > 0) :
    w2_0 * k_star > 0 := by
  exact Nat.mul_pos h_w2 h_k
```
*Adversarial Critique:*  
This theorem proves that the product of two positive natural numbers is positive. It has zero connection to the Wasserstein metric $W_2(\mu, \nu)$, optimal transport, Brownian motion, or the exponential contraction factor $e^{-K^* t}$.

### 4.3 Anti-Vacuity Verdict: **REJECT (MOCK FORMALIZATION)**
The current Lean 4 formalization is a **place-holder mock** that trivializes the mathematical obligations into trivial inequalities on `Nat`. For genuine formal certification, the obligations must be formalized over `Real` ($\mathbb{R}$) and real inner product spaces, utilizing Mathlib 4 types (`InnerProductSpace ℝ E`, `ContDiff ℝ 2 f`, positive semi-definite bilinear forms).

---

## 5. Adversarial Audit of Numerical Verification Engine (`verify_paper1_numerical.py`)

### 5.1 Battery-by-Battery Scrutiny

- **Battery 1 (Curvature Uniformity under Separation Sweep):**  
  *Audit:* Sweeps 30 scales along separation ray $c \in [1, 10^5]$ for $n=200, p=50$, $\kappa(\mathbf{X})=500$.  
  *Result:* Verified $\lambda_{\min}(\mathbf{H}) \ge \lambda_0 = 0.500000$. Genuine and rigorous.
- **Battery 2 (Spectral Gap Rayleigh Quotient Lower Bound):**  
  *Audit:* Evaluates $\mathbf{v}^T \mathbf{H} \mathbf{v}$ over 1,000 directions.  
  *Critique:* Evaluates the pointwise curvature quadratic form $\Gamma_2$, but does not simulate or estimate the actual spectral gap $\lambda_1(-\mathcal{L})$ of the Markov transition operator.
- **Battery 3 (Synchronous SDE Coupling & $W_2$ Contraction):**  
  *Audit:* Simulates two Langevin trajectories with shared Brownian increments $d\mathbf{B}_t$.  
  *Result:* Particle distance contracted from $23.78$ to $1.186 \le 1.956$ ($e^{-K^* t}$ bound). Genuine simulation.
- **Battery 4 (Adversarial Inverse Stress Engine):**  
  *Audit:* Runs L-BFGS-B from 10 diverse initial configurations to find $\boldsymbol{\theta}$ minimizing $\lambda_{\min}(\nabla^2 U)$.  
  *Result:* Optimizer converged to $0.400002 \ge \lambda_0 = 0.400000$. Verifies non-emptiness and rigidity of the curvature floor.
- **Battery 5 (CIG-Langevin Ergodicity & Acceptance Rates):**  
  *CRITICAL AUDIT FINDING:*  
  In lines 251-253 of `verify_paper1_numerical.py`:
  ```python
  # Accept/Reject
  theta = theta_prop
  accepted += 1
  trajectory.append(theta.copy())
  ```
  **The Metropolis-Hastings acceptance ratio is never evaluated.** Proposals are unconditionally accepted (100% acceptance rate). Battery 5 executes unadjusted Langevin dynamics (ULA), not MALA/CIG-Langevin. The acceptance ratio calculation and random test $u \le \alpha$ were completely bypassed.

---

## 6. Actionable Remediation Plan

To elevate Paper 1 to the standards of the *Journal of the Royal Statistical Society: Series B*, the author must execute the following remediation steps:

### Action Item 1: Fix Proof of Theorem 3.2 in `paper1_bayesian_glms.tex`
- **Replace** lines 283–303 with the semigroup variance decay proof:
  ```latex
  \begin{proof}
  For any test function $f \in C_c^\infty(\R^p)$, let $\phi(t) = \operatorname{Var}_\pi(\mathcal{P}_t f) = \int_{\R^p} (\mathcal{P}_t f)^2 d\pi - (\int_{\R^p} f d\pi)^2$.
  Differentiating under the semigroup:
  \begin{equation}
  \phi'(t) = 2 \int_{\R^p} (\mathcal{P}_t f) \mathcal{L}(\mathcal{P}_t f) d\pi = -2 \int_{\R^p} \Gamma(\mathcal{P}_t f, \mathcal{P}_t f) d\pi = -2 \psi(t),
  \end{equation}
  where $\psi(t) \coloneqq \int_{\R^p} \|\nabla \mathcal{P}_t f\|^2 d\pi$. Differentiating $\psi(t)$ and applying the Bochner identity (\ref{eq:bochner_formula}) with the $CD(K^*, \infty)$ condition:
  \begin{equation}
  \psi'(t) = -2 \int_{\R^p} \Gamma_2(\mathcal{P}_t f, \mathcal{P}_t f) d\pi \le -2 K^* \int_{\R^p} \Gamma(\mathcal{P}_t f, \mathcal{P}_t f) d\pi = -2 K^* \psi(t).
  \end{equation}
  By Gr\"onwall's inequality, $\psi(t) \le e^{-2 K^* t} \psi(0)$. Since $\lim_{t \to \infty} \phi(t) = 0$, integrating $\phi'(t)$ from $0$ to $\infty$ yields:
  \begin{equation}
  \operatorname{Var}_\pi(f) = -\int_0^\infty \phi'(t) dt = 2 \int_0^\infty \psi(t) dt \le 2 \psi(0) \int_0^\infty e^{-2 K^* t} dt = \frac{1}{K^*} \int_{\R^p} \|\nabla f\|^2 d\pi.
  \end{equation}
  Taking the infimum over all non-constant $f \in C_c^\infty(\R^p)$ establishes $\lambda_1(-\mathcal{L}) \ge K^* \ge \lambda_0 > 0$.
  \end{proof}
  ```

### Action Item 2: Correct Theorem 3.4 (MALA TV Mixing)
1. **Remove** the additive bias $+\mathcal{O}(\gamma^{3/2} p^{1/2})$ from equation (369).
2. **Add** the dimensional condition $\gamma \le \mathcal{O}(p^{-1/3})$ to the theorem hypothesis:
   $$\gamma \le \min\left( \frac{K^*}{2 L^2}, \frac{c_0}{p^{1/3}} \right).$$
3. **Replace** $\sqrt{\chi^2(\delta_{\boldsymbol{\theta}_0} \mid \pi)}$ with a warm start distribution $\mu_0$ satisfying $\chi^2(\mu_0 \mid \pi) \le M < \infty$.

### Action Item 3: Repair Battery 5 in `verify_paper1_numerical.py`
- Implement the exact Metropolis-Hastings acceptance ratio $\alpha(\boldsymbol{\theta}_k, \boldsymbol{\theta}^*)$ with proposal density evaluation:
  ```python
  # Compute proposal log-densities
  diff_fwd = theta_prop - m
  log_q_fwd = -0.5 * diff_fwd.T @ G @ diff_fwd + np.sum(np.log(np.diag(L)))
  
  # Backward drift and metric
  eta_prop = X @ theta_prop
  prob_prop = 1.0 / (1.0 + np.exp(-np.clip(eta_prop, -50, 50)))
  W_prop = prob_prop * (1.0 - prob_prop)
  G_prop = X.T @ (W_prop[:, None] * X) + (lambda_0 * np.eye(p) + kappa_0 * (X.T @ X))
  L_prop = np.linalg.cholesky(G_prop)
  grad_prop = -X.T @ (y - prob_prop) + (lambda_0 * np.eye(p) + kappa_0 * (X.T @ X)) @ theta_prop
  m_prop = theta_prop - gamma * scipy.linalg.cho_solve((L_prop, True), grad_prop)
  
  diff_bwd = theta - m_prop
  log_q_bwd = -0.5 * diff_bwd.T @ G_prop @ diff_bwd + np.sum(np.log(np.diag(L_prop)))
  
  # Log-posterior ratio
  log_alpha = (-U_prop + log_q_bwd) - (-U_curr + log_q_fwd)
  if np.log(np.random.rand()) <= log_alpha:
      theta = theta_prop
      accepted += 1
  ```

### Action Item 4: Refactor Lean 4 Formalization (`BakryEmery.lean`)
- Upgrade definitions from `Nat` to `Real` ($\mathbb{R}$).
- Represent Hessian quadratic forms and matrix lower bounds using Mathlib 4's `Matrix` and `LinearMap` positive-definiteness predicates (`posDef`, `PosSemidef`), ensuring that theorems state and prove actual properties of real quadratic forms.

---

## 7. Official Sign-Off

| Milestone | Status | Auditor Recommendation |
| :--- | :---: | :--- |
| **Conceptual Novelty & Scientific Merit** | **OUTSTANDING** | Recommend publication in JRSS-B once proof repairs are made. |
| **Mathematical Derivations (Props 2.2, Thm 3.1, Thm 3.3)** | **WATERTIGHT** | Approved without changes. |
| **Proof Rigor (Thm 3.2, Thm 3.4)** | **REQUIRES REPAIR** | Must incorporate semigroup variance proof and $p^{-1/3}$ step size. |
| **Numerical Engine (`verify_paper1_numerical.py`)** | **CONDITIONALLY APPROVED** | Must activate true MH accept/reject in Battery 5. |
| **Formal Lean 4 Verification (`BakryEmery.lean`)** | **REJECTED (VACUOUS)** | Must upgrade from `Nat` mocks to authentic `Real` types. |

**Final Recommendation:** **REVISE**. The paper possesses exceptional scientific value and directly solves an important problem in Bayesian computational statistics. Addressing the four specific remediation items above will make the manuscript mathematically unassailable.
