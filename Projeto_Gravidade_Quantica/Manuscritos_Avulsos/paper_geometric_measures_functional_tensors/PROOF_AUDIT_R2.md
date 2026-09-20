## Round 2 Adversarial Audit — "Beyond the Spectrum II"

### 1. Verification of the Four Primary Fixes

**Issue 1 (Thm — Isospectral Separation, formerly Thm 3.2): STRUCTURALLY RESOLVED, but contains a new arithmetic error.**

The annulus-vs-L-shape construction is now geometrically sound: removing the center cell from a 3×3 grid genuinely produces a square annulus ($\beta_1=1$), while removing a corner cell produces a star-shaped, contractible staircase region ($\beta_1=0$). The permutation computation $A = PBP^T$ is correct — I recomputed it entry-by-entry and it matches the stated $A$.

However, **the stated spectrum is wrong**. The paper claims
$$\sigma(A)=\sigma(B)=\{2+\sqrt6,\,2-\sqrt6,\,0\}.$$
Cross-checking via $\operatorname{tr}(B)=4$ and $\operatorname{tr}(B^2)=\|B\|_F^2=32$ (since $B$ is symmetric): if the eigenvalues are $\{\lambda_1,\lambda_2,0\}$ with $\lambda_1+\lambda_2=4$, then $\lambda_1^2+\lambda_2^2=32$ forces $\lambda_1\lambda_2=-8$, giving $\lambda_{1,2}=2\pm2\sqrt3$, **not** $2\pm\sqrt6$. Direct expansion of $\det(B-\lambda I)=-\lambda(\lambda^2-4\lambda-8)$ confirms this. The quoted $\|A\|_F=\|B\|_F=\sqrt{32}$ is correct — only the explicit eigenvalue values are miscalculated.

This is a **non-fatal but real correctness bug**: the theorem's logical validity (isospectrality via orthogonal similarity) never depends on the numeric eigenvalues, so the topological-separation argument survives untouched. But a rigorous paper cannot ship an incorrect explicit spectral computation. **Must fix**: replace $2\pm\sqrt6$ with $2\pm2\sqrt3$.

Separately, a **residual rigor gap**: Section 3's setup requires $\Phi(A)\in C^0(\Omega)$, but the pixel-realization used in the proof is piecewise-constant (discontinuous). The proof invokes "smoothed approximations via mollification $\Phi_\epsilon = \Phi * \eta_\epsilon$" without showing that $d_B(\mathrm{Dgm}_1(\Phi_\epsilon(A)),\mathrm{Dgm}_1(\Phi(A)))\to 0$ preserves the *strict* empty-vs-nonempty separation as $\epsilon\to0$. This is almost certainly true (the bottleneck stability theorem proved earlier in the same paper gives exactly this control, since the persistence gap is $\Theta(1)$), but the one-line citation to that theorem is missing here. Minor, easily patched.

**Issue 2 (Thm 4.1b, Willmore scaling): RESOLVED.** I recomputed both scaling regimes from the prototype $\Phi(A_k)=\epsilon_k\sin(kx_1)\sin(kx_2)$: gradient $\sim\epsilon_k k$, Hessian $\sim \epsilon_k k^2$, curvature $H\sim k$ (amplitude-independent), Willmore $\sim \epsilon_k k^3$. Substituting $\epsilon_k=\Theta(1/k)$ (Frobenius-normalized) gives Dirichlet $\Theta(1)$ / Willmore $\Theta(k^2)$; substituting $\epsilon_k=\Theta(1)$ gives $\|A_k\|_F=\Theta(k)$ / Willmore $\Theta(k^3)$. Both are now internally consistent — no contradiction remains.

**Issue 3 (Thm 6.2, QFI faithfulness): RESOLVED.** The added hypothesis $\lambda_{\min}(\rho(x))\ge\epsilon_0>0$ correctly forces SLD denominators $\ge 2\epsilon_0$, and the derived bound $g^{\mathrm{QFI}}_{\mu\mu}\ge\frac12\|\partial_\mu\rho\|_{\mathrm{HS}}^2$ is algebraically correct (I verified the SLD component formula against the standard quantum-metrology identity). The faithfulness iff-claim is now airtight on the interior of state space, with the boundary case properly deferred to Safránek via remark rather than swept under the rug.

**Issue 4 (Section 6 domain): RESOLVED**, with one loose end. Moving to $\mathbb{T}^d$ correctly supplies a compact boundaryless spin manifold for the Dirac spectral triple. Not explicitly stated: the algebra-generating realizations $\Phi(A)$ (e.g., the kernel realization $\boldsymbol\psi(x)^TA\boldsymbol\psi(x)$ from Section 2, built on $[0,1]^d$) need their basis functions $\psi_i$ taken periodic to actually descend to well-defined smooth functions on $\mathbb{T}^d$. This is a one-sentence fix, not a structural problem.

### 2. Remaining Issues (5–13)

All confirmed closed: the $\diam(\Omega)/\sqrt2$ constant now derives correctly from the TV-normalization identity; Neumann + flat-boundary hypotheses are explicit in Bakry–Émery; the Gibbs/Gaussian example rigorously exhibits $\kappa_{\mathrm{BE}}=\lambda_{\min}(A)>0$; tameness is now an explicit hypothesis in bottleneck stability; the $d\ge2$ Willmore integrability threshold has an explicit (if heuristic) radial-scaling justification; the closed-level-set caveat is present (if a little informal); $\tau$ vs. $t$ are decoupled; the empty-diagram convention is defined; the fractal Besov remark is properly hedged as conjectural.

### 3. Final Verdict

**Not yet a clean FINAL PASS.** The four critical/global vulnerabilities are conceptually and structurally resolved — none of the original logical gaps survive. But this round surfaces **one genuine new correctness defect** (the $2\pm\sqrt6$ eigenvalue error, which I verified independently via the Frobenius-norm/trace cross-check and is unambiguously wrong) plus two minor rigor loose ends (mollification-limit citation; periodicity of $\psi_i$ on $\mathbb{T}^d$).

Recommendation: **one more micro-revision** — (1) correct the spectrum to $2\pm2\sqrt3$, (2) add one sentence invoking the bottleneck stability theorem to justify the mollification limit, (3) add one clause requiring periodic $\psi_i$ in Section 6. None of these require new mathematics; all are direct edits to existing text. Once applied, I would grant FINAL PASS.
