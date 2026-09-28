"""Resolve every DOI in refs.md via Crossref (fallback DataCite for arXiv 10.48550 DOIs) and compare
the returned title with an expected keyword.  Negative controls: a wrong DOI must not resolve to the
expected title, and a right DOI with a wrong keyword must fail the title match."""
import json
import re
import time
import urllib.request
import urllib.parse

REFS = [
    # fakeon / Lee-Wick / quadratic gravity
    ('AnselmiPiva2017', '10.1007/JHEP06(2017)066', 'new formulation of Lee'),
    ('AnselmiPiva2017PRD', '10.1103/PhysRevD.96.045009', 'Perturbative unitarity of Lee'),
    ('Anselmi2018', '10.1007/JHEP02(2018)141', 'Fakeons and Lee'),
    ('AnselmiPiva2018', '10.1007/JHEP11(2018)021', 'fakeons and microcausality'),
    ('Anselmi2019', '10.1088/1361-6382/ab04c8', 'classical limit of quantum gravity'),
    ('AnselmiMarino2020', '10.1088/1361-6382/ab78d2', 'light cones'),
    ('Anselmi2021', '10.1007/JHEP11(2021)030', 'Diagrammar'),
    ('ABP2020', '10.1007/JHEP07(2020)211', 'Weyl-squared'),
    ('Anselmi2021JCAP', '10.1088/1475-7516/2021/01/048', 'renormalization-group flow'),
    ('Stelle1977', '10.1103/PhysRevD.16.953', 'Renormalization of higher-derivative'),
    ('Stelle1978', '10.1007/BF00760427', 'Classical gravity with higher derivatives'),
    ('Starobinsky1980', '10.1016/0370-2693(80)90670-X', 'isotropic cosmological models'),
    ('Salvio2018', '10.3389/fphy.2018.00077', 'Quadratic Gravity'),
    ('Buoninfante2025', '10.1007/JHEP07(2025)175', 'Strict renormalizability'),
    ('HoldomRen2016', '10.1103/PhysRevD.93.124030', 'QCD analogy'),
    ('LeeWick1969', '10.1016/0550-3213(69)90098-4', 'Negative metric'),
    ('LeeWick1970', '10.1103/PhysRevD.2.1033', 'Finite theory of quantum electrodynamics'),
    ('Nakanishi1971', '10.1103/PhysRevD.3.811', 'Lorentz Noninvariance'),
    ('GOW2008', '10.1103/PhysRevD.77.025012', 'Lee-Wick standard model'),
    ('KuboKugo2023', '10.1093/ptep/ptad143', 'Unitarity violation'),
    ('DonoghueMenezes2019PRL', '10.1103/PhysRevLett.123.171601', 'Arrow of Causality'),
    ('DonoghueMenezes2019PRD', '10.1103/PhysRevD.100.105006', 'Unitarity, stability'),
    ('LiuModestoCalcagni2023', '10.1007/JHEP02(2023)140', 'ghost pairs'),
    # nonlocal
    ('Tomboulis1997', '10.48550/arXiv.hep-th/9702146', 'Superrenormalizable'),
    ('Tomboulis2015', '10.1103/PhysRevD.92.125037', 'Nonlocal and quasilocal'),
    ('Modesto2012', '10.1103/PhysRevD.86.044005', 'Super-renormalizable'),
    ('ModestoRachwal2014', '10.1016/j.nuclphysb.2014.10.015', 'finite gravitational theories'),
    ('BGKM2012', '10.1103/PhysRevLett.108.031101', 'Ghost-Free Theories of Gravity'),
    ('BrisceseModesto2019', '10.1103/PhysRevD.99.104043', 'Cutkosky rules'),
    ('PiusSen2016', '10.1007/JHEP10(2016)024', 'Cutkosky rules for superstring'),
    ('KoshelevTokareva2021', '10.1103/PhysRevD.104.025016', 'Unitarity of Minkowski nonlocal'),
    ('BCMN2024', '10.1007/JHEP08(2024)204', 'Form factors, spectral'),
    ('CMN2016', '10.1142/S0218271816500589', 'Quantum spectral dimension'),
    # causal sets
    ('BenincasaDowker2010', '10.1103/PhysRevLett.104.181301', 'Scalar Curvature of a Causal Set'),
    ('ASS2014', '10.1007/JHEP06(2014)024', 'Generalized causal set'),
    ('BBL2015', '10.1007/JHEP03(2015)036', 'Nonlocal scalar quantum field theory from causal sets'),
    ('BBMM2016', '10.1103/PhysRevD.93.044017', 'Spectral dimension from nonlocal dynamics'),
    ('BBD2016', '10.1088/0264-9381/33/24/245018', 'continuum limit of a 4-dimensional causal set'),
    ('EichhornMizera2014', '10.1088/0264-9381/31/12/125007', 'Spectral dimension in causal set'),
    ('Carlip2015', '10.1088/0264-9381/32/23/232001', 'Dimensional reduction in causal set'),
    ('BBLMMO2016', '10.1103/PhysRevLett.116.161303', 'Optomechanical'),
    ('BBLMMO2017', '10.1103/PhysRevD.95.026012', 'optomechanical experiments'),
    ('Sorkin2009', '10.1017/CBO9780511575549.004', 'Does locality fail'),
    # PT / Pais-Uhlenbeck
    ('BenderMannheim2008', '10.1103/PhysRevLett.100.110402', 'No-Ghost Theorem'),
    ('Smilga2009', '10.3842/SIGMA.2009.017', 'Pais-Uhlenbeck'),
    ('SalvioStrumia2016', '10.1140/epjc/s10052-016-4079-8', '4-derivative theories'),
    # asymptotic safety
    ('LauscherReuter2005', '10.1088/1126-6708/2005/10/050', 'Fractal spacetime structure'),
    ('ReuterSaueressig2011', '10.1007/JHEP12(2011)012', 'Fractal space-times under the microscope'),
    ('PlataniaWetterich2020', '10.1016/j.physletb.2020.135911', 'fictitious ghosts'),
    ('Platania2022', '10.1007/JHEP09(2022)167', 'Causality, unitarity and stability'),
    ('DKRS2020PRL', '10.1103/PhysRevLett.125.181301', 'No Strings Attached'),
    ('DKRS2020JHEP', '10.1007/JHEP11(2020)136', 'Graviton-mediated scattering'),
    ('BDPR2022', '10.21468/SciPostPhys.12.1.001', 'Reconstructing the graviton'),
    ('FLPR2023', '10.1103/PhysRevLett.130.081501', 'Graviton Spectral Function'),
    # Horava, multifractional
    ('Horava2009PRD', '10.1103/PhysRevD.79.084008', 'Lifshitz'),
    ('Horava2009PRL', '10.1103/PhysRevLett.102.161301', 'Spectral Dimension'),
    ('BPS2011', '10.1007/JHEP04(2011)018', 'non-relativistic quantum gravity'),
    ('Calcagni2017', '10.1007/JHEP03(2017)138', 'Multifractional theories'),
    ('Calcagni2021', '10.1142/S021773232140006X', 'Multifractional theories'),
    # NCG, CDT, simplicial
    ('ChamseddineConnes1997', '10.1007/s002200050126', 'Spectral Action Principle'),
    ('CCM2007', '10.4310/ATMP.2007.v11.n6.a3', 'neutrino mixing'),
    ('LSS2013', '10.1088/1475-7516/2013/12/020', 'Gravity Probe B'),
    ('AJL2005', '10.1103/PhysRevLett.95.171301', 'Spectral Dimension'),
    ('AGJJL2010', '10.1016/j.physletb.2010.05.054', 'CDT meets'),
    ('CoumbeJurkiewicz2015', '10.1007/JHEP03(2015)151', 'dimensional reduction'),
    ('Loll2019', '10.1088/1361-6382/ab57c7', 'causal dynamical triangulations'),
    ('HamberWilliams1984', '10.1016/0550-3213(84)90603-5', 'Higher derivative quantum gravity on a simplicial'),
    # general
    ('OS1973', '10.1007/BF01645738', 'Axioms for Euclidean'),
    ('Lehmann1954', '10.1007/BF02783624', 'Ausbreitungsfunktionen'),
    ('CES2013', '10.1103/PhysRevD.87.124028', 'diffusion'),
    ('SVW2011', '10.1103/PhysRevD.84.104018', 'dispersion relations'),
    # observations
    ('Planck2018X', '10.1051/0004-6361/201833887', 'Constraints on inflation'),
    ('BK2021', '10.1103/PhysRevLett.127.151301', 'Primordial Gravitational Waves'),
    ('Tristram2022', '10.1103/PhysRevD.105.083524', 'tensor-to-scalar ratio'),
    ('LiteBIRD2023', '10.1093/ptep/ptac150', 'LiteBIRD'),
    ('ACT_DR6_Louis', '10.48550/arXiv.2503.14452', 'DR6 Power Spectra'),
    ('ACT_DR6_Calabrese', '10.48550/arXiv.2503.14454', 'Extended Cosmological Models'),
    ('Lee2020', '10.1103/PhysRevLett.124.101101', 'Law at Separations down to'),
]
NEG = [('NEG_wrong_doi', '10.1103/PhysRevD.16.9530', 'Renormalization of higher-derivative'),
       ('NEG_wrong_keyword', '10.1007/JHEP07(2020)211', 'Lee-Wick standard model')]


def fetch(doi):
    q = urllib.parse.quote(doi, safe='/()')
    for base in ('https://api.crossref.org/works/', 'https://api.datacite.org/dois/'):
        for attempt in range(3):
            try:
                req = urllib.request.Request(base + q, headers={'User-Agent': 'survey/1.0 (mailto:none@example.org)'})
                with urllib.request.urlopen(req, timeout=40) as r:
                    d = json.load(r)
                if 'crossref' in base:
                    m = d['message']
                    t = (m.get('title') or [''])[0]
                    if m.get('subtitle'):
                        t += ': ' + m['subtitle'][0]
                    return base, t, (m.get('container-title') or [''])[0]
                a = d['data']['attributes']
                return base, a['titles'][0]['title'], a.get('publisher', '')
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    time.sleep(5); continue
                break
            except Exception:
                time.sleep(2)
    return None, None, None


def norm(s):
    s = re.sub(r'<[^>]+>', '', s)
    return ' '.join(s.lower().replace('‐', '-').replace('–', '-').replace('’', "'").split())


ok = 0
for key, doi, kw in REFS:
    src, title, cont = fetch(doi)
    good = title is not None and norm(kw) in norm(title)
    ok += good
    print(f"[{'OK ' if good else 'BAD'}] {key:24s} {doi:40s} {('crossref' if src and 'crossref' in src else 'datacite') if src else '-':8s} | {norm(title) if title else None} | {cont}")
    time.sleep(0.4)
print(f"\n{ok}/{len(REFS)} DOIs resolved with matching title")
for key, doi, kw in NEG:
    src, title, cont = fetch(doi)
    good = title is not None and norm(kw) in norm(title)
    print(f"[{'NEG-PASS' if not good else 'NEG-FAIL'}] {key} {doi} -> {title}")
