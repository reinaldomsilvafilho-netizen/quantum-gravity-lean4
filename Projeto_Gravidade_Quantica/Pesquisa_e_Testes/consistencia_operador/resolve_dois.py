"""Resolve every DOI used in README/refs.md via Crossref (fallback DataCite) and compare the
returned title with an expected keyword.  Negative control: a deliberately wrong DOI
(10.1103/PhysRevD.16.9530) must NOT resolve to Stelle's paper."""
import json
import time
import urllib.request
import urllib.error

REFS = [
    ('Stelle1977', '10.1103/PhysRevD.16.953', 'Renormalization of higher-derivative'),
    ('Stelle1978', '10.1007/BF00760427', 'Classical gravity with higher derivatives'),
    ('LeeWick1969', '10.1016/0550-3213(69)90098-4', 'Negative metric'),
    ('LeeWick1970', '10.1103/PhysRevD.2.1033', 'Finite theory of quantum electrodynamics'),
    ('AnselmiPiva2017', '10.1007/JHEP06(2017)066', 'Lee-Wick'),
    ('Anselmi2018fakeons', '10.1007/JHEP02(2018)141', 'Fakeons'),
    ('AnselmiPiva2018causality', '10.1007/JHEP11(2018)021', 'microcausality'),
    ('DonoghueMenezes2019', '10.1103/PhysRevD.100.105006', 'Unitarity'),
    ('Salvio2018', '10.3389/fphy.2018.00077', 'Quadratic Gravity'),
    ('Woodard2015', '10.4249/scholarpedia.32243', 'Ostrogradsky'),
    ('Horava2009PRD', '10.1103/PhysRevD.79.084008', 'Lifshitz'),
    ('Horava2009PRL', '10.1103/PhysRevLett.102.161301', 'Spectral Dimension'),
    ('SVW2011PRL', '10.1103/PhysRevLett.107.131303', 'Spectral Dimension'),
    ('SVW2011PRD', '10.1103/PhysRevD.84.104018', 'dispersion relations'),
    ('CES2013', '10.1103/PhysRevD.87.124028', 'diffusion'),
    ('BPS2009extra', '10.1088/1126-6708/2009/10/029', 'extra mode'),
    ('CNPS2009', '10.1088/1126-6708/2009/08/070', 'Strong coupling'),
    ('BPS2010PRL', '10.1103/PhysRevLett.104.181302', 'Consistent Extension'),
    ('BPS2011JHEP', '10.1007/JHEP04(2011)018', 'non-relativistic quantum gravity'),
    ('PapazoglouSotiriou2010', '10.1016/j.physletb.2010.01.054', 'Strong coupling'),
    ('Collins2004', '10.1103/PhysRevLett.93.191301', 'Lorentz Invariance and Quantum Gravity'),
    ('PospelovShang2012', '10.1103/PhysRevD.85.105001', 'Lorentz violation'),
    ('GrootNibbelinkPospelov2005', '10.1103/PhysRevLett.94.081601', 'Lorentz Violation in Supersymmetric'),
    ('GW170817ApJL', '10.3847/2041-8213/aa920c', 'Gravitational Waves and Gamma-Rays'),
    ('GSS2018', '10.1103/PhysRevD.97.024032', 'GW170817'),
    ('BarvinskyEtAl2016', '10.1103/PhysRevD.93.064022', 'Renormalization of Ho'),
    # 10.1103/PhysRevLett.122.211301 was guessed from memory and resolves to an unrelated
    # paper (PBH dark matter, Bartolo et al.); replaced by the two DOIs below.
    ('BarvinskyEtAl2017PRL', '10.1103/PhysRevLett.119.211301', 'asymptotically free'),
    ('BKS2023', '10.1103/PhysRevD.108.L121503', 'Asymptotic freedom'),
    ('BlasLim2014', '10.1142/S0218271814430093', 'preferred frame'),
    ('Mattingly2005', '10.12942/lrr-2005-5', 'Lorentz Invariance'),
    ('Liberati2013', '10.1088/0264-9381/30/13/133001', 'Lorentz invariance'),
    ('Modesto2012', '10.1103/PhysRevD.86.044005', 'Super-renormalizable'),
    ('BGKM2012', '10.1103/PhysRevLett.108.031101', 'Ghost-Free Theories of Gravity'),
    ('Marcinkiewicz1939', '10.1007/BF01210677', 'de la loi de Gau'),  # Crossref stores 'Gauß' mis-encoded
    ('AGJJL2010', '10.1016/j.physletb.2010.05.054', 'CDT meets'),
    ('Ambjorn2005','10.1103/PhysRevLett.95.171301', 'Spectral Dimension'),
]
NEG = ('NEG_control_wrong_doi', '10.1103/PhysRevD.16.9530', 'Renormalization of higher-derivative')


def fetch(doi):
    for base in ('https://api.crossref.org/works/', 'https://api.datacite.org/dois/'):
        try:
            req = urllib.request.Request(base + doi, headers={'User-Agent': 'consistency-check/1.0 (mailto:none)'})
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.load(r)
            if 'crossref' in base:
                m = d['message']
                title = (m.get('title') or [''])[0]
                cont = (m.get('container-title') or [''])[0]
                yr = (m.get('issued', {}).get('date-parts') or [[None]])[0][0]
                au = ', '.join(a.get('family', '') for a in m.get('author', [])[:4])
                return 'crossref', title, cont, m.get('volume', ''), m.get('page', m.get('article-number', '')), yr, au
            a = d['data']['attributes']
            return 'datacite', a['titles'][0]['title'], a.get('publisher', ''), '', '', a.get('publicationYear'), ''
        except urllib.error.HTTPError:
            continue
        except Exception as e:  # network error
            return 'error', str(e), '', '', '', '', ''
    return 'unresolved', '', '', '', '', '', ''


ok = 0
for key, doi, kw in REFS:
    src, title, cont, vol, page, yr, au = fetch(doi)
    hit = kw.lower().replace('-', ' ') in title.lower().replace('-', ' ').replace('‐', ' ')
    ok += hit
    print(f'{"OK  " if hit else "CHK "} {key:28s} {doi:36s} [{src}] {au} ({yr}) "{title}" {cont} {vol} {page}')
    time.sleep(0.2)
src, title, *_ = fetch(NEG[1])
neg_ok = NEG[2].lower() not in title.lower()
print(f'{"PASS" if neg_ok else "FAIL"} negative control: wrong DOI {NEG[1]} -> [{src}] "{title}"')
print(f'\nSUMMARY: {ok}/{len(REFS)} titles contain the expected keyword; negative control {"PASS" if neg_ok else "FAIL"}')
