"""Apply the verified bibliography corrections found by check_references.py (2026-09-24)."""
import glob
import re

fixes = [
    # Koide: DOI pointed to an unrelated paper; correct title/pages/DOI (Crossref-verified)
    (r'\emph{Fermion-boson two-body model of quarks and leptons and energy subscales}',
     r'\emph{Fermion-boson two-body model of quarks and leptons and Cabibbo mixing}'),
    (r'Lettere al Nuovo Cimento, \textbf{34} (1982), 201--203,', r'Lettere al Nuovo Cimento, \textbf{34} (1982), 201--205,'),
    ('10.1007/BF02817094', '10.1007/BF02817096'),
    # LiteBIRD: last digit of DOI wrong
    ('10.1007/s10909-019-02150-1', '10.1007/s10909-019-02150-5'),
    # Ambjorn-Jurkiewicz-Loll 2005: correct title
    (r'\emph{Spectral dimension of the universe},', r'\emph{The spectral dimension of the universe is scale dependent},'),
    # Ryu-Takayanagi 2006: full title
    (r'\emph{Holographic derivation of entanglement entropy from AdS/CFT}',
     r'\emph{Holographic derivation of entanglement entropy from the anti-de Sitter space/conformal field theory correspondence}'),
    # Hirani thesis: SSRN DOI belonged to another work; Caltech thesis DOI (DataCite-verified)
    (r'\href{https://doi.org/10.2139/ssrn.4079384}{doi:10.2139/ssrn.4079384}',
     r'\href{https://doi.org/10.7907/ZHY8-V329}{doi:10.7907/ZHY8-V329}'),
    # Azagra-Ferrera: title/journal did not match the DOI; use the Crossref record of the DOI
    (r'\emph{Inf-sup regularization and infimal convolution on Riemannian manifolds},' + '\n' +
     r'Rev. Mat. Iberoam. \textbf{23} (2007), no. 3, 903--937,',
     r'\emph{Inf-convolution and regularization of convex functions on Riemannian manifolds of nonpositive curvature},' + '\n' +
     r'Rev. Mat. Complut. \textbf{19} (2006), no. 2, 323--345,'),
    # Samko et al.: DOI does not resolve; keep ISBN only
    ('\\doi{10.4324/9780203755143}.', ''),
]
willmore_doi = re.compile(r',?\s*\\href\{https://doi\.org/10\.1017/9781108885478\.006\}\{doi:10\.1017/9781108885478\.006\}')

for f in sorted(glob.glob('chap*.tex')):
    s0 = s = open(f, encoding='utf-8').read()
    for a, b in fixes:
        s = s.replace(a, b)
    s = willmore_doi.sub('', s)          # Willmore 1965 has no DOI; the one given is a 2021 book chapter
    if s != s0:
        open(f, 'w', encoding='utf-8', newline='').write(s)
        print('fixed', f)
