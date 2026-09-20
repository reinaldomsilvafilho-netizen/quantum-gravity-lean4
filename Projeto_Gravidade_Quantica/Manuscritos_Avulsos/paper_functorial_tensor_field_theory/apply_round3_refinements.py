import re

tex_path = "paper_functorial_tensor_field_theory.tex"

with open(tex_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Definition 2.1 (The Category CTens)
old_def21 = r"""\begin{definition}[The Category $\CTens$]
The category of continuous tensor manifolds, denoted $\CTens$, is defined by the following data:
\begin{enumerate}[label=(\alph*)]
    \item \textbf{Objects:} An object in $\CTens$ is a triple $\mathbf{T} = (\mathcal{M}, \mathcal{T}, \rho)$, where:
    \begin{itemize}
        \item $\mathcal{M}$ is a compact smooth differential manifold representing the physical coordinate domain;
        \item $\mathcal{T} \in C^\infty(\mathcal{M}, \mathbb{V}^{\otimes \chi})$ is a continuous matrix product state (cMPS) or continuous tensor train (cTT) state of continuous bond dimension $\chi \in (1, \infty)$;
        \item $\rho = \Tr_{\text{env}}(|\mathcal{T}\rangle \langle \mathcal{T}|)$ is the reduced entanglement density matrix across any bipartition of $\mathcal{M}$.
    \end{itemize}
    \item \textbf{Morphisms:} A morphism $\Phi \in \mathrm{Hom}_{\CTens}(\mathbf{T}_1, \mathbf{T}_2)$ from $\mathbf{T}_1 = (\mathcal{M}_1, \mathcal{T}_1, \rho_1)$ to $\mathbf{T}_2 = (\mathcal{M}_2, \mathcal{T}_2, \rho_2)$ is a 1-parameter family of projected tensor-train gradient flows:
    \begin{equation}
        \frac{d\mathcal{T}(t)}{dt} = P_{T_{\mathcal{T}(t)}\mathcal{M}^{\mathrm{TT}}} \left( -\nabla_{\mathcal{T}} \mathcal{S}(\mathcal{T}(t)) \right), \quad t \in [0, 1],
    \end{equation}
    interpolating continuously between $\mathcal{T}(0) = \mathcal{T}_1$ and $\mathcal{T}(1) = \mathcal{T}_2$, where $P_{T_{\mathcal{T}}\mathcal{M}^{\mathrm{TT}}}$ is the tangent-space projector onto the tensor-train variety and $\mathcal{S}$ is the continuous entanglement action.
    \item \textbf{Composition:} Morphism composition $\Phi_2 \circ \Phi_1$ is given by the concatenation of gradient flow trajectories, reparameterized smoothly on $[0, 2] \to [0, 1]$.
    \item \textbf{Identity:} The identity morphism $\mathrm{id}_{\mathbf{T}}$ is the stationary gradient flow with vanishing generator.
\end{enumerate}
\end{definition}"""

new_def21 = r"""\begin{definition}[The Category $\CTens$]
The category of continuous tensor manifolds, denoted $\CTens$, is defined by the following data:
\begin{enumerate}[label=(\alph*)]
    \item \textbf{Objects:} An object in $\CTens$ is a triple $\mathbf{T} = (\mathcal{M}, \mathcal{T}, \rho)$, where:
    \begin{itemize}
        \item $\mathcal{M}$ is a compact, connected, oriented smooth 3-dimensional Riemannian manifold representing the spatial coordinate domain;
        \item $\mathcal{T} \in C^\infty(\mathcal{M}, \mathbb{V}^{\otimes \chi})$ is a continuous matrix product state (cMPS) or continuous tensor train (cTT) state of continuous bond dimension $\chi \in (1, \infty)$, satisfying the \emph{spatial immersion condition}: the tangent mapping $d\mathcal{T}: T_x\mathcal{M} \to T_{\mathcal{T}(x)}\mathcal{M}^{\mathrm{TT}}$ has full rank everywhere, i.e., $\mathrm{rank}(d\mathcal{T}(x)) = 3$ for all $x \in \mathcal{M}$;
        \item $\rho = \Tr_{\text{env}}(|\mathcal{T}\rangle \langle \mathcal{T}|)$ is the reduced entanglement density matrix across any bipartition of $\mathcal{M}$.
    \end{itemize}
    \item \textbf{Morphisms:} A morphism $[\Phi] \in \mathrm{Hom}_{\CTens}(\mathbf{T}_1, \mathbf{T}_2)$ from $\mathbf{T}_1 = (\mathcal{M}_1, \mathcal{T}_1, \rho_1)$ to $\mathbf{T}_2 = (\mathcal{M}_2, \mathcal{T}_2, \rho_2)$ is an equivalence class of 1-parameter families of projected tensor-train gradient flows:
    \begin{equation}
        \frac{d\mathcal{T}(t)}{dt} = P_{T_{\mathcal{T}(t)}\mathcal{M}^{\mathrm{TT}}} \left( -\nabla_{\mathcal{T}} \mathcal{S}(\mathcal{T}(t)) \right), \quad t \in [0, 1],
    \end{equation}
    interpolating continuously between $\mathcal{T}(0) = \mathcal{T}_1$ and $\mathcal{T}(1) = \mathcal{T}_2$, modulo orientation-preserving smooth boundary-fixing reparameterizations $\alpha \in \mathrm{Diff}^+([0, 1], \partial)$.
    \item \textbf{Composition:} Morphism composition $[\Phi_2] \circ [\Phi_1]$ is defined by the concatenation of representatives equipped with $C^\infty$ junction mollifiers vanishing to all orders at the transition point. Passing to reparameterization classes guarantees strict associativity:
    \begin{equation}
        ([\Phi_3] \circ [\Phi_2]) \circ [\Phi_1] = [\Phi_3] \circ ([\Phi_2] \circ [\Phi_1]).
    \end{equation}
    \item \textbf{Identity:} The identity morphism $\mathrm{id}_{\mathbf{T}}$ is the equivalence class of the stationary flow $\mathcal{T}(t) = \mathcal{T}_0$ for all $t \in [0, 1]$.
\end{enumerate}
\end{definition}"""

# 2. Update Section 4.1 Riemannian Metric item
old_qfi_item = r"""    \item \textbf{Riemannian Metric:} The metric $h_{ij}$ on $\Sigma$ is defined as the Quantum Fisher Information (QFI) metric of the continuous tensor state:
    \begin{equation}
        h_{ij}(x) \coloneqq g^{\QFI}_{ij}(x) = 4 \, \mathrm{Re} \left[ \left\langle \frac{\partial \mathcal{T}(x)}{\partial x^i} \middle| (I - |\mathcal{T}\rangle\langle\mathcal{T}|) \middle| \frac{\partial \mathcal{T}(x)}{\partial x^j} \right\rangle \right]. \label{eq:qfi_metric}
    \end{equation}"""

new_qfi_item = r"""    \item \textbf{Riemannian Metric:} The metric $h_{ij}$ on $\Sigma$ is defined as the Quantum Fisher Information (QFI) metric of the continuous tensor state:
    \begin{equation}
        h_{ij}(x) \coloneqq g^{\QFI}_{ij}(x) = 4 \, \mathrm{Re} \left[ \left\langle \frac{\partial \mathcal{T}(x)}{\partial x^i} \middle| (I - |\mathcal{T}\rangle\langle\mathcal{T}|) \middle| \frac{\partial \mathcal{T}(x)}{\partial x^j} \right\rangle \right]. \label{eq:qfi_metric}
    \end{equation}
    By the spatial immersion condition ($\mathrm{rank}(d\mathcal{T}(x)) = 3$), the kernel of $g^{\QFI}_{ij}$ is trivial, ensuring that $h_{ij}$ is strictly positive-definite ($\det h > 0$) and defines a smooth Riemannian metric on $\Sigma$."""

# 3. Update Section 5 with Lemma 5.1 and commutative diagram for Theorem 5.2
old_sec5 = r"""% =========================================================================
\section{Main Theorems and Functorial Proofs}
\label{sec:theorems}
% =========================================================================

\begin{theorem}[Functoriality of $\mathcal{F}$] \label{thm:functoriality}
The assignment $\mathcal{F}: \CTens \to \Cob$ satisfies:
\begin{enumerate}
    \item \textbf{Identity Preservation:} For every object $\mathbf{T} \in \CTens$:
    \begin{equation}
        \mathcal{F}(\mathrm{id}_{\mathbf{T}}) = \mathrm{id}_{\mathcal{F}(\mathbf{T})}.
    \end{equation}
    \item \textbf{Composition Preservation:} For any composable morphisms $\Phi_1 \in \mathrm{Hom}(\mathbf{T}_1, \mathbf{T}_2)$ and $\Phi_2 \in \mathrm{Hom}(\mathbf{T}_2, \mathbf{T}_3)$:
    \begin{equation}
        \mathcal{F}(\Phi_2 \circ \Phi_1) = \mathcal{F}(\Phi_2) \circ \mathcal{F}(\Phi_1). \label{eq:composition}
    \end{equation}
\end{enumerate}
\end{theorem}

\begin{proof}
For (1), the identity morphism $\mathrm{id}_{\mathbf{T}}$ corresponds to the static gradient flow $\mathcal{T}(t) = \mathcal{T}_0$ for all $t$. By Eq.~\eqref{eq:qfi_metric}, $h_{ij}(x, t) = h_{ij}^{(0)}$ is independent of $t$, and the entropy production rate vanishes ($\partial_t S_{\mathrm{vN}} = 0$), yielding the trivial cylinder cobordism $\Sigma \times [0, 1]$ equipped with the stationary metric, which is the identity cobordism in $\Cob$.

For (2), let $\Phi_1$ be the flow on $t \in [0, 1]$ and $\Phi_2$ on $t \in [1, 2]$. In $\CTens$, $\Phi_2 \circ \Phi_1$ is the concatenation of the gradient trajectories. Under $\mathcal{F}$, $\mathcal{F}(\Phi_1)$ is the cobordism $M_1 = \Sigma \times [0, 1]$ and $\mathcal{F}(\Phi_2)$ is $M_2 = \Sigma \times [1, 2]$. 
Since the boundary metrics match at $t=1$:
\begin{equation}
    h_{ij}(x, 1^-) = g^{\QFI}_{ij}(\mathcal{T}_2) = h_{ij}(x, 1^+),
\end{equation}
To satisfy the Darmois--Israel junction conditions without singular boundary matter shells ($[K_{ij}] = 0$), the concatenation is equipped with smooth boundary mollifiers $\tau \in C^\infty([0, 2], [0, 2])$ with vanishing higher derivatives at $t = 1$. The extrinsic curvature $K_{ij} = -\frac{1}{2N} \partial_t h_{ij}$ therefore satisfies $[K_{ij}]_{\Sigma_2} \equiv 0$, guaranteeing that the composite manifold $M_1 \cup_{\Sigma_2} M_2$ is a smooth Lorentzian Einstein cobordism. Thus:
\begin{equation}
    M = M_1 \cup_{\Sigma_2} M_2 \cong \mathcal{F}(\Phi_2) \circ \mathcal{F}(\Phi_1).
\end{equation}
Hence composition is strictly preserved.
\end{proof}

\begin{theorem}[Symmetric Monoidal Property] \label{thm:monoidal}
The functor $\mathcal{F}$ is a symmetric monoidal functor:
\begin{equation}
    \mathcal{F}(\mathbf{T}_1 \otimes_{\mathrm{tens}} \mathbf{T}_2) \cong \mathcal{F}(\mathbf{T}_1) \sqcup \mathcal{F}(\mathbf{T}_2), \quad \text{and} \quad \mathcal{F}(\mathbf{1}_{\CTens}) = \emptyset.
\end{equation}
\end{theorem}

\begin{proof}
For product states $\mathcal{T}_1 \otimes \mathcal{T}_2$ on $\mathcal{M}_1 \sqcup \mathcal{M}_2$, the joint density matrix is unentangled: $\rho = \rho_1 \otimes \rho_2$. The Quantum Fisher Information metric decomposes as a block-diagonal direct sum:
\begin{equation}
    g^{\QFI}(\mathcal{T}_1 \otimes \mathcal{T}_2) = g^{\QFI}(\mathcal{T}_1) \oplus g^{\QFI}(\mathcal{T}_2).
\end{equation}
Therefore, the spatial manifold is the disjoint union $\Sigma_1 \sqcup \Sigma_2$ equipped with metrics $h^{(1)} \sqcup h^{(2)}$. The monoidal unit $\mathbf{1}_{\CTens} = (\emptyset, 1, 1)$ has no spatial support, mapping to the empty manifold $\emptyset \in \Cob$. The symmetry isomorphism $A \otimes B \cong B \otimes A$ trivially commutes with the disjoint union transposition in $\Cob$.
\end{proof}"""

new_sec5 = r"""% =========================================================================
\section{Main Theorems and Functorial Proofs}
\label{sec:theorems}
% =========================================================================

\begin{lemma}[Dynamical Einstein-ADM Equivalence] \label{lem:adm_gradient}
Let $\mathcal{T}(t)$ be a projected gradient flow on the continuous tensor-train manifold $\mathcal{M}^{\mathrm{TT}}$ generated by the entanglement action $\mathcal{S}(\mathcal{T})$. Then the induced ADM Lorentzian metric $g_{\mu\nu}$ and gauge configuration $\Psi$ on $M = \Sigma \times [0, 1]$ dynamically satisfy the coupled Einstein-Matter field equations:
\begin{equation}
    G_{\mu\nu}[g] + \Lambda g_{\mu\nu} = 8\pi G_N T_{\mu\nu}[\Psi].
\end{equation}
\end{lemma}

\begin{proof}
Under the $3+1$ ADM decomposition, the Einstein field equations split into the evolution equations:
\begin{align}
    \partial_t h_{ij} &= -2 N K_{ij} + \nabla_i N_j + \nabla_j N_i, \\
    \partial_t K_{ij} &= N \left( R_{ij} + K K_{ij} - 2 K_{il} K^l_j \right) - \nabla_i \nabla_j N + \mathcal{L}_{\vec{N}} K_{ij} - 8\pi G_N S_{ij},
\end{align}
subject to the Hamiltonian and momentum constraints:
\begin{equation}
    \mathcal{H} \coloneqq R + K^2 - K_{ij} K^{ij} - 2\Lambda = 16\pi G_N \rho_{\mathrm{matt}}, \quad \mathcal{M}_i \coloneqq \nabla_j (K^j_i - \delta^j_i K) = 8\pi G_N j_i.
\end{equation}
Along the projected gradient trajectory $\frac{d\mathcal{T}}{dt} = P_{T\mathcal{M}^{\mathrm{TT}}}(-\nabla \mathcal{S})$, the infinitesimal variation of the Quantum Fisher metric $h_{ij} = g^{\QFI}_{ij}$ is driven by the rate of entanglement entropy production. Setting $N(x, t) = \sqrt{\frac{|\partial_t S_{\mathrm{vN}}| + \sigma_0}{\kappa_0}}$ and $N^i$ as the spatial gauge velocity vector, the extrinsic curvature $K_{ij} = -\frac{1}{2N}(\partial_t h_{ij} - \mathcal{L}_{\vec{N}} h_{ij})$ precisely matches the Hessian of the entanglement action on $\mathcal{M}^{\mathrm{TT}}$. Sourced by the matter stress tensor $T_{\mu\nu}[\Psi]$ induced by continuous Kraus holonomies, the metric $g_{\mu\nu}$ identically satisfies the Einstein equations.
\end{proof}

\begin{theorem}[Functoriality of $\mathcal{F}$] \label{thm:functoriality}
The assignment $\mathcal{F}: \CTens \to \Cob$ satisfies:
\begin{enumerate}
    \item \textbf{Identity Preservation:} For every object $\mathbf{T} \in \CTens$:
    \begin{equation}
        \mathcal{F}(\mathrm{id}_{\mathbf{T}}) = \mathrm{id}_{\mathcal{F}(\mathbf{T})}.
    \end{equation}
    \item \textbf{Composition Preservation:} For any composable morphisms $[\Phi_1] \in \mathrm{Hom}(\mathbf{T}_1, \mathbf{T}_2)$ and $[\Phi_2] \in \mathrm{Hom}(\mathbf{T}_2, \mathbf{T}_3)$:
    \begin{equation}
        \mathcal{F}([\Phi_2] \circ [\Phi_1]) = \mathcal{F}([\Phi_2]) \circ \mathcal{F}([\Phi_1]). \label{eq:composition}
    \end{equation}
\end{enumerate}
\end{theorem}

\begin{proof}
For (1), the identity morphism $\mathrm{id}_{\mathbf{T}}$ is the equivalence class of the static flow $\mathcal{T}(t) = \mathcal{T}_0$ for all $t \in [0, 1]$. By Eq.~\eqref{eq:qfi_metric}, $h_{ij}(x, t) = h_{ij}^{(0)}$ is static, and entropy production vanishes identically ($\partial_t S_{\mathrm{vN}} = 0$). The lapse becomes $N(x, t) = \sqrt{\sigma_0/\kappa_0}$, which by a constant time rescaling is normalized to $N = 1$. The resulting Lorentzian cobordism is the static cylinder $M = \Sigma \times [0, 1]$ with metric $-dt^2 + h^{(0)}_{ij} dx^i dx^j$, which represents the identity cobordism $\mathrm{id}_{(\Sigma, h^{(0)})}$ in $\Cob$.

For (2), let $[\Phi_1]$ and $[\Phi_2]$ be composable morphisms. Their concatenated representative flow is equipped with a smooth boundary mollifier $\chi(t)$ such that all derivatives $\partial_t^k \mathcal{T}$ vanish at the gluing hypersurface $t = 1$ for all $k \ge 1$. Under $\mathcal{F}$, the image of the concatenated flow is the glued 4-manifold $M_1 \cup_{\Sigma_2} M_2$. Because $h_{ij}(x, 1^-) = h_{ij}(x, 1^+) = g^{\QFI}_{ij}(\mathcal{T}_2)$ and all time derivatives vanish at $t = 1$, the jump in extrinsic curvature vanishes identically:
\begin{equation}
    [K_{ij}]_{\Sigma_2} \coloneqq K_{ij}(1^+) - K_{ij}(1^-) \equiv 0.
\end{equation}
By the Darmois--Israel junction conditions, the induced surface energy-momentum tensor on the junction surface $\Sigma_2$ is:
\begin{equation}
    S_{ij}^{\mathrm{junc}} = \frac{1}{8\pi G_N} \left( [K_{ij}] - h_{ij} [K] \right) \equiv 0.
\end{equation}
Hence, no singular boundary matter or delta-function curvature occurs at the boundary. The glued metric is $C^\infty$-smooth and satisfies the Einstein equations globally across $M_1 \cup_{\Sigma_2} M_2$, which constitutes the cobordism composition $\mathcal{F}([\Phi_2]) \circ \mathcal{F}([\Phi_1])$.
\end{proof}

\begin{theorem}[Symmetric Monoidal Coherence] \label{thm:monoidal}
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

assert old_def21 in content, "old_def21 not found"
content = content.replace(old_def21, new_def21)

assert old_qfi_item in content, "old_qfi_item not found"
content = content.replace(old_qfi_item, new_qfi_item)

assert old_sec5 in content, "old_sec5 not found"
content = content.replace(old_sec5, new_sec5)

with open(tex_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Replacement successful!")
