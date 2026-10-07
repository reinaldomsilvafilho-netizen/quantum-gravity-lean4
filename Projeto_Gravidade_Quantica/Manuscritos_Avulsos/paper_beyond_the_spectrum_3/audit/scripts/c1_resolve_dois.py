"""Resolve every DOI in the Vol. III bibliography via Crossref / DataCite and
print title, first author, year, container. Negative control: a mutated DOI
must fail to resolve."""
import json, os, re, sys, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.normpath(os.path.join(HERE, '..', '..', 'paper_beyond_the_spectrum_3.tex'))
tex = open(TEX, encoding='utf-8').read()
bib = tex.split('\\begin{thebibliography}')[1]
items = re.split(r'\\bibitem\{', bib)[1:]
UA = {'User-Agent': 'blind-audit-script/1.0 (mailto:audit@example.org)'}


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def resolve(doi):
    try:
        m = fetch('https://api.crossref.org/works/' + urllib.parse.quote(doi))['message']
        au = m.get('author', [{}])
        first = (au[0].get('family', '') if au else '')
        yr = (m.get('issued', {}).get('date-parts', [[None]])[0][0])
        return 'crossref', (m.get('title') or [''])[0], first, yr, (m.get('container-title') or [''])[0], m.get('volume'), m.get('page')
    except urllib.error.HTTPError:
        pass
    try:
        a = fetch('https://api.datacite.org/dois/' + urllib.parse.quote(doi))['data']['attributes']
        return 'datacite', a['titles'][0]['title'], a['creators'][0].get('name'), a.get('publicationYear'), a.get('publisher'), None, None
    except urllib.error.HTTPError as e:
        return 'FAIL', str(e), None, None, None, None, None


import urllib.parse
cited = set(re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]*)\}', tex))
cited = set(k.strip() for c in cited for k in c.split(','))
fails = 0
for it in items:
    key = it.split('}', 1)[0]
    m = re.search(r'doi\.org/([^}]+)\}', it)
    doi = m.group(1) if m else None
    print('==', key, '| cited in text:', key in cited, '| DOI:', doi)
    if doi:
        r = resolve(doi)
        print('   ', r)
        if r[0] == 'FAIL':
            fails += 1
neg = resolve('10.1007/BF01444643999')
print('NEG CONTROL mutated DOI ->', neg[0])
if neg[0] != 'FAIL':
    fails += 1
print('unresolved:', fails)
