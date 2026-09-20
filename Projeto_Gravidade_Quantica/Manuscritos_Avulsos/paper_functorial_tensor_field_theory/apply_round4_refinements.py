import re

tex_path = "paper_functorial_tensor_field_theory.tex"

with open(tex_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Proposition 2.2 for dagger-compact structure
old_prop22 = r"""\begin{proposition}[Monoidal Structure of $\CTens$]
$(\CTens, \otimes_{\mathrm{tens}}, \mathbf{1}_{\CTens})$ is a symmetric monoidal category, where:
\begin{equation}
    (\mathcal{M}_1, \mathcal{T}_1, \rho_1) \otimes_{\mathrm{tens}} (\mathcal{M}_2, \mathcal{T}_2, \rho_2) \coloneqq (\mathcal{M}_1 \sqcup \mathcal{M}_2, \mathcal{T}_1 \otimes \mathcal{T}_2, \rho_1 \otimes \rho_2),
\end{equation}
and the monoidal unit $\mathbf{1}_{\CTens} = (\emptyset, 1, 1)$ is the trivial vacuum tensor.
\end{proposition}"""

new_prop22 = r"""\begin{proposition}[Dagger-Compact Monoidal Structure of $\CTens$]
$(\CTens, \otimes_{\mathrm{tens}}, \mathbf{1}_{\CTens}, (\cdot)^*)$ is a dagger-compact symmetric monoidal category, where:
\begin{equation}
    (\mathcal{M}_1, \mathcal{T}_1, \rho_1) \otimes_{\mathrm{tens}} (\mathcal{M}_2, \mathcal{T}_2, \rho_2) \coloneqq (\mathcal{M}_1 \sqcup \mathcal{M}_2, \mathcal{T}_1 \otimes \mathcal{T}_2, \rho_1 \otimes \rho_2),
\end{equation}
the monoidal unit is $\mathbf{1}_{\CTens} = (\emptyset, 1, 1)$, and the dagger / dual object functor is defined by:
\begin{equation}
    \mathbf{T}^* = (\mathcal{M}, \mathcal{T}, \rho)^* \coloneqq (-\mathcal{M}, \mathcal{T}^*, \rho^T),
\end{equation}
reversing spatial orientation and applying complex conjugation to the auxiliary bond tensors.
\end{proposition}"""

# 2. Update Section 4.1 Riemannian Metric item to include gauge invariance
old_qfi = r"""    \item \textbf{Riemannian Metric:} The metric $h_{ij}$ on $\Sigma$ is defined as the Quantum Fisher Information (QFI) metric of the continuous tensor state:
    \begin{equation}
        h_{ij}(x) \coloneqq g^{\QFI}_{ij}(x) = 4 \, \mathrm{Re} \left[ \left\langle \frac{\partial \mathcal{T}(x)}{\partial x^i} \middle| (I - |\mathcal{T}\rangle\langle\mathcal{T}|) \middle| \frac{\partial \mathcal{T}(x)}{\partial x^j} \right\rangle \right]. \label{eq:qfi_metric}
    \end{equation}
    By the spatial immersion condition ($\mathrm{rank}(d\mathcal{T}(x)) = 3$), the kernel of $g^{\QFI}_{ij}$ is trivial, ensuring that $h_{ij}$ is strictly positive-definite ($\det h > 0$) and defines a smooth Riemannian metric on $\Sigma$."""

new_qfi = r"""    \item \textbf{Riemannian Metric:} The metric $h_{ij}$ on $\Sigma$ is defined as the Quantum Fisher Information (QFI) metric of the continuous tensor state:
    \begin{equation}
        h_{ij}(x) \coloneqq g^{\QFI}_{ij}(x) = 4 \, \mathrm{Re} \left[ \left\langle \frac{\partial \mathcal{T}(x)}{\partial x^i} \middle| (I - |\mathcal{T}\rangle\langle\mathcal{T}|) \middle| \frac{\partial \mathcal{T}(x)}{\partial x^j} \right\rangle \right]. \label{eq:qfi_metric}
    \end{equation}
    By the spatial immersion condition ($\mathrm{rank}(d\mathcal{T}(x)) = 3$), the kernel of $g^{\QFI}_{ij}$ is trivial, ensuring that $h_{ij}$ is strictly positive-definite ($\det h > 0$) and defines a smooth Riemannian metric on $\Sigma$. Moreover, under local gauge rotations $\mathcal{T}(x) \mapsto U(x)\mathcal{T}(x)$, the projection $(I - |\mathcal{T}\rangle\langle\mathcal{T}|)$ renders $g^{\QFI}_{ij}$ gauge-invariant, defining a gauge-independent spatial metric."""

# 3. Update Theorem 5.3 (Symmetric Monoidal & Dagger Preservation)
old_thm_mon = r"""\begin{theorem}[Symmetric Monoidal Coherence] \label{thm:monoidal}
The functor $\mathcal{F}: \CTens \to \Cob$ is a symmetric monoidal functor. Specifically, there exist natural isomorphisms:
\begin{equation}
    \Phi_{\mathbf{T}_1, \mathbf{T}_2}: \mathcal{F}(\mathbf{T}_1) \sqcup \mathcal{F}(\mathbf{T}_2) \xrightarrow{\sim} \mathcal{F}(\mathbf{T}_1 \otimes_{\mathrm{tens}} \mathbf{T}_2), \quad \text{and} \quad \Phi_0: \emptyset \xrightarrow{\sim} \mathcal{F}(\mathbf{1}_{\CTens}),
\end{equation}
satisfying Mac Lane's associativity, unitality, and braiding coherence diagrams.
\end{theorem}

\begin{proof}
For product states $\mathbf{T}_1 \otimes_{\mathrm{tens}} \mathbf{T}_2 = (\mathcal{M}_1 \sqcup \mathcal{M}_2, \mathcal{T}_1 \otimes \mathcal{T}_2, \rho_1 \otimes \rho_2)$, the joint density matrix is separable across the spatial components. Because the cross-correlations vanish between disjoint components, the Quantum Fisher Information metric decomposes into a direct sum:
\begin{equation}
    g^{\QFI}(\mathcal{T}_1 \otimes \mathcal{T}_2) = g^{\QFI}(\mathcal{T}_1) \oplus g^{\QFI}(\mathcal{T}_2) = h^{(1)} \oplus h^{(2)}.
\end{equation}
The boundary matter fields $\psi_\Sigma$ also split component-wise. This establishes the canonical object isomorphism $\Phi_{\mathbf{T}_1, \mathbf{T}_2}: (\Sigma_1, h^{(1)}) \sqcup (\Sigma_2, h^{(2)}) \xrightarrow{\sim} (\Sigma_1 \sqcup \Sigma_2, h^{(1)} \oplus h^{(2)})$. The monoidal unit $\mathbf{1}_{\CTens} = (\emptyset, 1, 1)$ maps to the empty manifold $\emptyset \in \Cob$.

To establish the symmetric monoidal property, we verify the symmetry braiding condition. In $\CTens$, the symmetry isomorphism $\beta^{\CTens}: \mathbf{T}_1 \otimes_{\mathrm{tens}} \mathbf{T}_2 \to \mathbf{T}_2 \otimes_{\mathrm{tens}} \mathbf{T}_1$ is the canonical tensor swap map. In $\Cob$, the braiding isomorphism $\beta^{\Cob}: \Sigma_1 \sqcup \Sigma_2 \to \Sigma_2 \sqcup \Sigma_1$ is the geometric diffeomorphism transposing connected components. The naturality of the braiding is governed by the commutative diagram:
\begin{equation}
\begin{tikzcd}[column sep=huge, row sep=large]
\mathcal{F}(\mathbf{T}_1) \sqcup \mathcal{F}(\mathbf{T}_2) \arrow[r, "\Phi_{\mathbf{T}_1, \mathbf{T}_2}"] \arrow[d, "\beta^{\Cob}"'] & \mathcal{F}(\mathbf{T}_1 \otimes_{\mathrm{tens}} \mathbf{T}_2) \arrow[d, "\mathcal{F}(\beta^{\CTens})"] \\
\mathcal{F}(\mathbf{T}_2) \sqcup \mathcal{F}(\mathbf{T}_1) \arrow[r, "\Phi_{\mathbf{T}_2, \mathbf{T}_1}"'] & \mathcal{F}(\mathbf{T}_2 \otimes_{\mathrm{tens}} \mathbf{T}_1)
\end{tikzcd}
\end{equation}
Commutativity follows because the tensor permutation $\mathcal{T}_1(x) \otimes \mathcal{T}_2(y) \mapsto \mathcal{T}_2(y) \otimes \mathcal{T}_1(x)$ induces an exact relabeling of the coordinate charts on $\mathcal{M}_1 \sqcup \mathcal{M}_2 \cong \mathcal{M}_2 \sqcup \mathcal{M}_1$, which coincides identically with $\beta^{\Cob}$. Associativity and unitality pentagons and triangles hold trivially by the associativity and unitality of Cartesian disjoint union and tensor products. Hence, $\mathcal{F}$ is a symmetric monoidal functor.
\end{proof}"""

new_thm_mon = r"""\begin{theorem}[Symmetric Monoidal & Dagger Functor Coherence] \label{thm:monoidal}
The functor $\mathcal{F}: \CTens \to \Cob$ is a dagger-monoidal symmetric functor. Specifically:
\begin{enumerate}
    \item There exist natural isomorphisms:
    \begin{equation}
        \Phi_{\mathbf{T}_1, \mathbf{T}_2}: \mathcal{F}(\mathbf{T}_1) \sqcup \mathcal{F}(\mathbf{T}_2) \xrightarrow{\sim} \mathcal{F}(\mathbf{T}_1 \otimes_{\mathrm{tens}} \mathbf{T}_2), \quad \text{and} \quad \Phi_0: \emptyset \xrightarrow{\sim} \mathcal{F}(\mathbf{1}_{\CTens}),
    \end{equation}
    satisfying Mac Lane's associativity, unitality, and braiding coherence diagrams.
    \item $\mathcal{F}$ preserves the dagger duality structure:
    \begin{equation}
        \mathcal{F}(\mathbf{T}^*) \cong (\mathcal{F}(\mathbf{T}))^*.
    \end{equation}
\end{enumerate}
\end{theorem}

\begin{proof}
For product states $\mathbf{T}_1 \otimes_{\mathrm{tens}} \mathbf{T}_2 = (\mathcal{M}_1 \sqcup \mathcal{M}_2, \mathcal{T}_1 \otimes \mathcal{T}_2, \rho_1 \otimes \rho_2)$, the joint density matrix is separable across the spatial components. Because the cross-correlations vanish between disjoint components, the Quantum Fisher Information metric decomposes into a direct sum:
\begin{equation}
    g^{\QFI}(\mathcal{T}_1 \otimes \mathcal{T}_2) = g^{\QFI}(\mathcal{T}_1) \oplus g^{\QFI}(\mathcal{T}_2) = h^{(1)} \oplus h^{(2)}.
\end{equation}
The boundary matter fields $\psi_\Sigma$ also split component-wise. This establishes the canonical object isomorphism $\Phi_{\mathbf{T}_1, \mathbf{T}_2}: (\Sigma_1, h^{(1)}) \sqcup (\Sigma_2, h^{(2)}) \xrightarrow{\sim} (\Sigma_1 \sqcup \Sigma_2, h^{(1)} \oplus h^{(2)})$. The monoidal unit $\mathbf{1}_{\CTens} = (\emptyset, 1, 1)$ maps to the empty manifold $\emptyset \in \Cob$.

To establish the symmetric monoidal property, we verify the symmetry braiding condition. In $\CTens$, the symmetry isomorphism $\beta^{\CTens}: \mathbf{T}_1 \otimes_{\mathrm{tens}} \mathbf{T}_2 \to \mathbf{T}_2 \otimes_{\mathrm{tens}} \mathbf{T}_1$ is the canonical tensor swap map. In $\Cob$, the braiding isomorphism $\beta^{\Cob}: \Sigma_1 \sqcup \Sigma_2 \to \Sigma_2 \sqcup \Sigma_1$ is the geometric diffeomorphism transposing connected components. The naturality of the braiding is governed by the commutative diagram:
\begin{equation}
\begin{tikzcd}[column sep=huge, row sep=large]
\mathcal{F}(\mathbf{T}_1) \sqcup \mathcal{F}(\mathbf{T}_2) \arrow[r, "\Phi_{\mathbf{T}_1, \mathbf{T}_2}"] \arrow[d, "\beta^{\Cob}"'] & \mathcal{F}(\mathbf{T}_1 \otimes_{\mathrm{tens}} \mathbf{T}_2) \arrow[d, "\mathcal{F}(\beta^{\CTens})"] \\
\mathcal{F}(\mathbf{T}_2) \sqcup \mathcal{F}(\mathbf{T}_1) \arrow[r, "\Phi_{\mathbf{T}_2, \mathbf{T}_1}"'] & \mathcal{F}(\mathbf{T}_2 \otimes_{\mathrm{tens}} \mathbf{T}_1)
\end{tikzcd}
\end{equation}
Commutativity follows because the tensor permutation $\mathcal{T}_1(x) \otimes \mathcal{T}_2(y) \mapsto \mathcal{T}_2(y) \otimes \mathcal{T}_1(x)$ induces an exact relabeling of the coordinate charts on $\mathcal{M}_1 \sqcup \mathcal{M}_2 \cong \mathcal{M}_2 \sqcup \mathcal{M}_1$, which coincides identically with $\beta^{\Cob}$. Associativity and unitality pentagons and triangles hold trivially by the associativity and unitality of Cartesian disjoint union and tensor products.

Finally, for dagger preservation, let $\mathbf{T}^* = (-\mathcal{M}, \mathcal{T}^*, \rho^T)$. Since the QFI metric $g^{\QFI}_{ij}$ is strictly invariant under complex conjugation of state vectors ($g^{\QFI}_{ij}(\mathcal{T}^*) = g^{\QFI}_{ij}(\mathcal{T})$), the spatial Riemannian metric remains invariant ($h_{ij}^* = h_{ij}$). The spatial manifold acquires the reversed orientation $-\Sigma$, and the boundary matter fields undergo charge conjugation $\psi^c$, which coincides precisely with the dual object $(\Sigma, h, \psi)^* = (-\Sigma, h, \psi^c)$ in $\Cob$. Hence $\mathcal{F}(\mathbf{T}^*) \cong (\mathcal{F}(\mathbf{T}))^*$, completing the proof.
\end{proof}"""

# 4. Update Theorem 5.4 (Category-Theoretic Sewing and Wheeler-DeWitt Constraints)
old_sewing = r"""\begin{theorem}[Category-Theoretic Sewing and Wheeler-DeWitt Isomorphism] \label{thm:sewing}
The Atiyah-Segal sewing axiom in $\Cob$:
\begin{equation}
    \int_{\Sigma} \mathcal{D}\psi \, \mathcal{Z}(M_1) \mathcal{Z}(M_2) = \mathcal{Z}(M_1 \cup_\Sigma M_2)
\end{equation}
is categorically isomorphic to:
\begin{enumerate}
    \item Continuous tensor network trace contraction $\Tr_{\chi}(\mathcal{T}_1 \mathcal{T}_2)$;
    \item The Hamiltonian constraint of the Wheeler-DeWitt equation:
    \begin{equation}
        \hat{\mathcal{H}} |\Psi_{\mathrm{WDW}}\rangle = 0.
    \end{equation}
\end{enumerate}
\end{theorem}

\begin{proof}
In $\CTens$, contractive gluing along a common boundary index $\alpha \in \{1, \dots, \chi\}$ corresponds to tracing over the shared auxiliary bond space $\mathbb{V}_\chi$. By the master duality dictionary \cite{silvafilho2026flows}, the auxiliary bond dimension $\chi$ relates to the boundary area by $\log \chi = \frac{\Area(\Sigma)}{4 G_N}$. 

Applying $\mathcal{F}$, the discrete bond contraction $\sum_{\alpha=1}^\chi A^\alpha_i B^\alpha_j$ passes in the continuous scaling limit to the path integral over the intermediate Cauchy surface metric $h_{ij}$ and matter configuration $\psi_\Sigma$. In canonical quantum gravity, integrating out the lapse function $N$ enforces the Wheeler-DeWitt Hamiltonian constraint $\mathcal{H} = G_{ijkl}\pi^{ij}\pi^{kl} - \sqrt{h}(R - 2\Lambda) = 0$. Since the lapse $N(t)$ in $\mathcal{F}$ is generated by the gradient flow of relative entropy, stationary points of the flow correspond precisely to $\hat{\mathcal{H}} = 0$. Hence, gluing in $\CTens$ is functorially equivalent to the Wheeler-DeWitt constraint in $\Cob$.
\end{proof}"""

new_sewing = r"""\begin{theorem}[Category-Theoretic Sewing and Wheeler-DeWitt Constraints Isomorphism] \label{thm:sewing}
The Atiyah-Segal sewing axiom in $\Cob$:
\begin{equation}
    \int_{\Sigma} \mathcal{D}\psi \, \mathcal{Z}(M_1) \mathcal{Z}(M_2) = \mathcal{Z}(M_1 \cup_\Sigma M_2)
\end{equation}
is categorically isomorphic to:
\begin{enumerate}
    \item Continuous tensor network trace contraction $\Tr_{\chi}(\mathcal{T}_1 \mathcal{T}_2)$;
    \item The complete set of Wheeler-DeWitt quantum gravitational constraints:
    \begin{equation}
        \hat{\mathcal{H}} |\Psi_{\mathrm{WDW}}\rangle = 0 \quad \text{and} \quad \hat{\mathcal{M}}_i |\Psi_{\mathrm{WDW}}\rangle = 0.
    \end{equation}
\end{enumerate}
\end{theorem}

\begin{proof}
In $\CTens$, contractive gluing along a common boundary index $\alpha \in \{1, \dots, \chi\}$ corresponds to tracing over the shared auxiliary bond space $\mathbb{V}_\chi$. By the master duality dictionary \cite{silvafilho2026flows}, the auxiliary bond dimension $\chi$ relates to the boundary area by $\log \chi = \frac{\Area(\Sigma)}{4 G_N}$. 

Applying $\mathcal{F}$, the discrete bond contraction $\sum_{\alpha=1}^\chi A^\alpha_i B^\alpha_j$ passes in the continuous scaling limit to the path integral over the intermediate Cauchy surface metric $h_{ij}$ and matter configuration $\psi_\Sigma$. In canonical quantum gravity, functional integration over the lapse function $N(x, t)$ and shift vector $N^i(x, t)$ enforces the Hamiltonian constraint $\hat{\mathcal{H}} \approx 0$ and the spatial momentum constraint $\hat{\mathcal{M}}_i \approx 0$, respectively. 

In $\CTens$, the shift vector $N^i(x, t)$ represents continuous gauge drift along the coordinate axes of $\mathcal{M}$. The gauge invariance of the physical tensor network trace under $\mathrm{GL}(\chi, \mathbb{C})$ gauge transformations guarantees that variations with respect to $N^i$ vanish identically, satisfying $\hat{\mathcal{M}}_i |\Psi_{\mathrm{WDW}}\rangle = 0$. Simultaneously, the lapse $N(x, t)$ is generated by the gradient flow of entanglement entropy; stationary points of the gradient flow correspond precisely to vanishing Hamiltonian constraint $\hat{\mathcal{H}} |\Psi_{\mathrm{WDW}}\rangle = 0$. Hence, gluing in $\CTens$ is functorially equivalent to the complete Wheeler-DeWitt constraint system in $\Cob$.
\end{proof}"""

assert old_prop22 in content, "old_prop22 not found"
content = content.replace(old_prop22, new_prop22)

assert old_qfi in content, "old_qfi not found"
content = content.replace(old_qfi, new_qfi)

assert old_thm_mon in content, "old_thm_mon not found"
content = content.replace(old_thm_mon, new_thm_mon)

assert old_sewing in content, "old_sewing not found"
content = content.replace(old_sewing, new_sewing)

with open(tex_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Round 4 replacements successfully applied!")
