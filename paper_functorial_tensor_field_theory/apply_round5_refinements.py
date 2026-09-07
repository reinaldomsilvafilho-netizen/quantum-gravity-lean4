import re

tex_path = "paper_functorial_tensor_field_theory.tex"

with open(tex_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Clean phantom limit in Eq. (4.2)
old_psi = r"""    \item \textbf{Matter Field Sections:} The boundary matter field $\psi_\Sigma$ is defined via the local entanglement spectrum invariants:
    \begin{equation}
        \psi_\Sigma(x) \coloneqq \lim_{\epsilon \to 0} \Tr_{\chi} \left( \mathcal{T}(x) \gamma^a A_a(x) \right),
    \end{equation}
    where $\gamma^a$ are the Dirac matrices on the tangent bundle $T\Sigma$."""

new_psi = r"""    \item \textbf{Matter Field Sections:} The boundary matter field $\psi_\Sigma$ is defined via the local entanglement spectrum invariants:
    \begin{equation}
        \psi_\Sigma(x) \coloneqq \Tr_{\chi} \left( \mathcal{T}(x) \gamma^a A_a(x) \right),
    \end{equation}
    where $\gamma^a$ are the Dirac matrices on the tangent bundle $T\Sigma$."""

# 2. Add morphism naturality in Theorem 5.3
old_braiding_block = r"""To establish the symmetric monoidal property, we verify the symmetry braiding condition. In $\CTens$, the symmetry isomorphism $\beta^{\CTens}: \mathbf{T}_1 \otimes_{\mathrm{tens}} \mathbf{T}_2 \to \mathbf{T}_2 \otimes_{\mathrm{tens}} \mathbf{T}_1$ is the canonical tensor swap map. In $\Cob$, the braiding isomorphism $\beta^{\Cob}: \Sigma_1 \sqcup \Sigma_2 \to \Sigma_2 \sqcup \Sigma_1$ is the geometric diffeomorphism transposing connected components. The naturality of the braiding is governed by the commutative diagram:
\begin{equation}
\begin{tikzcd}[column sep=huge, row sep=large]
\mathcal{F}(\mathbf{T}_1) \sqcup \mathcal{F}(\mathbf{T}_2) \arrow[r, "\Phi_{\mathbf{T}_1, \mathbf{T}_2}"] \arrow[d, "\beta^{\Cob}"'] & \mathcal{F}(\mathbf{T}_1 \otimes_{\mathrm{tens}} \mathbf{T}_2) \arrow[d, "\mathcal{F}(\beta^{\CTens})"] \\
\mathcal{F}(\mathbf{T}_2) \sqcup \mathcal{F}(\mathbf{T}_1) \arrow[r, "\Phi_{\mathbf{T}_2, \mathbf{T}_1}"'] & \mathcal{F}(\mathbf{T}_2 \otimes_{\mathrm{tens}} \mathbf{T}_1)
\end{tikzcd}
\end{equation}
Commutativity follows because the tensor permutation $\mathcal{T}_1(x) \otimes \mathcal{T}_2(y) \mapsto \mathcal{T}_2(y) \otimes \mathcal{T}_1(x)$ induces an exact relabeling of the coordinate charts on $\mathcal{M}_1 \sqcup \mathcal{M}_2 \cong \mathcal{M}_2 \sqcup \mathcal{M}_1$, which coincides identically with $\beta^{\Cob}$. Associativity and unitality pentagons and triangles hold trivially by the associativity and unitality of Cartesian disjoint union and tensor products."""

new_braiding_block = r"""Furthermore, $\Phi$ is natural on morphisms: for any pairs $[\Phi_1] \in \mathrm{Hom}(\mathbf{T}_1, \mathbf{T}_1')$ and $[\Phi_2] \in \mathrm{Hom}(\mathbf{T}_2, \mathbf{T}_2')$, the entanglement action decouples as $\mathcal{S}(\mathcal{T}_1 \otimes \mathcal{T}_2) = \mathcal{S}_1(\mathcal{T}_1) + \mathcal{S}_2(\mathcal{T}_2)$, yielding orthogonal 4-metrics $g^{(1)} \oplus g^{(2)}$ and making the following naturality square strictly commutative:
\begin{equation}
\begin{tikzcd}[column sep=huge, row sep=large]
\mathcal{F}(\mathbf{T}_1) \sqcup \mathcal{F}(\mathbf{T}_2) \arrow[r, "\Phi_{\mathbf{T}_1, \mathbf{T}_2}"] \arrow[d, "{\mathcal{F}([\Phi_1]) \sqcup \mathcal{F}([\Phi_2])}"'] & \mathcal{F}(\mathbf{T}_1 \otimes_{\mathrm{tens}} \mathbf{T}_2) \arrow[d, "{\mathcal{F}([\Phi_1] \otimes [\Phi_2])}"] \\
\mathcal{F}(\mathbf{T}_1') \sqcup \mathcal{F}(\mathbf{T}_2') \arrow[r, "\Phi_{\mathbf{T}_1', \mathbf{T}_2'}"'] & \mathcal{F}(\mathbf{T}_1' \otimes_{\mathrm{tens}} \mathbf{T}_2')
\end{tikzcd}
\end{equation}

To establish the symmetric monoidal property, we verify the symmetry braiding condition. In $\CTens$, the symmetry isomorphism $\beta^{\CTens}: \mathbf{T}_1 \otimes_{\mathrm{tens}} \mathbf{T}_2 \to \mathbf{T}_2 \otimes_{\mathrm{tens}} \mathbf{T}_1$ is the canonical tensor swap map. In $\Cob$, the braiding isomorphism $\beta^{\Cob}: \Sigma_1 \sqcup \Sigma_2 \to \Sigma_2 \sqcup \Sigma_1$ is the geometric diffeomorphism transposing connected components. The naturality of the braiding is governed by the commutative diagram:
\begin{equation}
\begin{tikzcd}[column sep=huge, row sep=large]
\mathcal{F}(\mathbf{T}_1) \sqcup \mathcal{F}(\mathbf{T}_2) \arrow[r, "\Phi_{\mathbf{T}_1, \mathbf{T}_2}"] \arrow[d, "\beta^{\Cob}"'] & \mathcal{F}(\mathbf{T}_1 \otimes_{\mathrm{tens}} \mathbf{T}_2) \arrow[d, "\mathcal{F}(\beta^{\CTens})"] \\
\mathcal{F}(\mathbf{T}_2) \sqcup \mathcal{F}(\mathbf{T}_1) \arrow[r, "\Phi_{\mathbf{T}_2, \mathbf{T}_1}"'] & \mathcal{F}(\mathbf{T}_2 \otimes_{\mathrm{tens}} \mathbf{T}_1)
\end{tikzcd}
\end{equation}
Commutativity follows because the tensor permutation $\mathcal{T}_1(x) \otimes \mathcal{T}_2(y) \mapsto \mathcal{T}_2(y) \otimes \mathcal{T}_1(x)$ induces an exact relabeling of the coordinate charts on $\mathcal{M}_1 \sqcup \mathcal{M}_2 \cong \mathcal{M}_2 \sqcup \mathcal{M}_1$, which coincides identically with $\beta^{\Cob}$. Associativity and unitality pentagons and triangles hold by standard Cartesian properties."""

# 3. Add Corollary 5.5 after Theorem 5.4
old_end_sewing = r"""In $\CTens$, the shift vector $N^i(x, t)$ represents continuous gauge drift along the coordinate axes of $\mathcal{M}$. The gauge invariance of the physical tensor network trace under $\mathrm{GL}(\chi, \mathbb{C})$ gauge transformations guarantees that variations with respect to $N^i$ vanish identically, satisfying $\hat{\mathcal{M}}_i |\Psi_{\mathrm{WDW}}\rangle = 0$. Simultaneously, the lapse $N(x, t)$ is generated by the gradient flow of entanglement entropy; stationary points of the gradient flow correspond precisely to vanishing Hamiltonian constraint $\hat{\mathcal{H}} |\Psi_{\mathrm{WDW}}\rangle = 0$. Hence, gluing in $\CTens$ is functorially equivalent to the complete Wheeler-DeWitt constraint system in $\Cob$.
\end{proof}"""

new_end_sewing = r"""In $\CTens$, the shift vector $N^i(x, t)$ represents continuous gauge drift along the coordinate axes of $\mathcal{M}$. The gauge invariance of the physical tensor network trace under $\mathrm{GL}(\chi, \mathbb{C})$ gauge transformations guarantees that variations with respect to $N^i$ vanish identically, satisfying $\hat{\mathcal{M}}_i |\Psi_{\mathrm{WDW}}\rangle = 0$. Simultaneously, the lapse $N(x, t)$ is generated by the gradient flow of entanglement entropy; stationary points of the gradient flow correspond precisely to vanishing Hamiltonian constraint $\hat{\mathcal{H}} |\Psi_{\mathrm{WDW}}\rangle = 0$. Hence, gluing in $\CTens$ is functorially equivalent to the complete Wheeler-DeWitt constraint system in $\Cob$.
\end{proof}

\begin{corollary}[Physical Hilbert Space Representation Functor] \label{cor:tqft_composition}
Let $\mathcal{Z}: \Cob \to \Hilb$ be Atiyah's axiomatic Topological Quantum Field Theory functor. Then the composite functor:
\begin{equation}
    \mathcal{Z}_{\mathrm{eff}} \coloneqq \mathcal{Z} \circ \mathcal{F} : \CTens \longrightarrow \Hilb
\end{equation}
assigns to each continuous tensor manifold $\mathbf{T} = (\mathcal{M}, \mathcal{T}, \rho)$ the physical quantum state $|\Psi_{\mathcal{T}}\rangle \in \mathcal{H}_\Sigma$, and to each morphism $[\Phi]$ the gravitational transition propagator $\langle \Psi_2 | \exp(-i \hat{H} \Delta t) | \Psi_1 \rangle$, directly bridging multilinear tensor variety flows to non-perturbative quantum gravity amplitudes.
\end{corollary}"""

assert old_psi in content, "old_psi not found"
content = content.replace(old_psi, new_psi)

assert old_braiding_block in content, "old_braiding_block not found"
content = content.replace(old_braiding_block, new_braiding_block)

assert old_end_sewing in content, "old_end_sewing not found"
content = content.replace(old_end_sewing, new_end_sewing)

with open(tex_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Round 5 replacements successfully applied!")
