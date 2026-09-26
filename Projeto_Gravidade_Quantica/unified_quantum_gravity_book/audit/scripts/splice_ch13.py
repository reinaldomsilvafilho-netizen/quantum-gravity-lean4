"""One-off: replace the body of chapter 13 with audit/_ch13_body.tex and add references."""
p = 'chap13_experimental_observational_signatures_quantum_gravity.tex'
s = open(p, encoding='utf-8').read()
start = s.index('\\title{')
end = s.index('\\begin{acknowledgments}')
s = s[:start] + open('audit/_ch13_body.tex', encoding='utf-8').read() + s[end:]
new_refs = r"""\bibitem{abbott2017gw170817}
B.~P. Abbott et~al. (LIGO Scientific Collaboration, Virgo Collaboration, Fermi GBM, INTEGRAL),
\emph{Gravitational waves and gamma-rays from a binary neutron star merger: GW170817 and GRB 170817A},
Astrophys. J. Lett., \textbf{848} (2017), L13,
\doi{10.3847/2041-8213/aa920c}.

\bibitem{horava2009spectral}
P.~Ho\v{r}ava,
\emph{Spectral dimension of the universe in quantum gravity at a Lifshitz point},
Phys. Rev. Lett., \textbf{102} (2009), 161301,
\doi{10.1103/PhysRevLett.102.161301}.

\bibitem{sotiriou2011spectral}
T.~P. Sotiriou, M.~Visser, and S.~Weinfurtner,
\emph{Spectral dimension as a probe of the ultraviolet continuum regime of causal dynamical triangulations},
Phys. Rev. Lett., \textbf{107} (2011), 131303,
\doi{10.1103/PhysRevLett.107.131303}.

"""
if 'abbott2017gw170817}\n' not in s.split('\\begin{thebibliography}')[1]:
    s = s.replace('\\bibitem{abazajian2016cmb}', new_refs + '\\bibitem{abazajian2016cmb}', 1)
old = r'\emph{A Unified Geometric and Algebraic Theory of Quantum Gravity: From Simplicial Fractional Calculus and Minimax Foliations to Emergent Holographic Spacetime}'
new = r'\emph{Emergent Spacetime, Holographic Entanglement, and Quantum Geometry: Proved Results, Conjectures, and Observational Limits}'
s = s.replace(old, new)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
