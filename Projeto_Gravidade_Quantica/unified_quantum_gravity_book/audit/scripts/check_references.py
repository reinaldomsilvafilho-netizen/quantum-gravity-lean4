"""Audit every \\bibitem in the chapters (WORKPLAN W5).

For each entry: extract the DOI (if any) and the cited title (first \\emph{...}); resolve the DOI
via Crossref (or DataCite for arXiv/Zenodo DOIs) and compare titles; for entries without DOI,
run a Crossref bibliographic search and report the best match.
Writes audit/references_report.md and audit/references.json.
Usage: python audit/scripts/check_references.py
"""
import concurrent.futures as cf
import difflib
import glob
import json
import re
import urllib.parse
import urllib.request

UA = {'User-Agent': 'book-reference-audit/1.0'}


def get_json(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            return json.load(r)
    except Exception as e:  # noqa: BLE001
        return {'_error': str(e)}


def delatex(s):
    s = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?', ' ', s)
    s = s.replace('{', '').replace('}', '').replace('~', ' ').replace('$', '')
    s = re.sub(r'\\.', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def norm(s):
    return re.sub(r'[^a-z0-9 ]', '', delatex(s).lower())


def sim(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def parse(path):
    s = open(path, encoding='utf-8').read()
    m = re.search(r'\\begin\{thebibliography\}.*?\n(.*?)\\end\{thebibliography\}', s, re.S)
    if not m:
        return []
    out = []
    for block in re.split(r'(?=\\bibitem)', m.group(1)):
        k = re.match(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}', block)
        if not k:
            continue
        doi = re.search(r'(?:doi\.org/|doi:\s*|\\doi\{)(10\.\d{4,9}/[^\s},]+)', block, re.I)
        title = re.search(r'\\emph\{((?:[^{}]|\{[^{}]*\})*)\}', block)
        out.append(dict(file=path, key=k.group(1), doi=doi.group(1).rstrip('.').rstrip(')') if doi and doi.group(1).count('(') < doi.group(1).count(')') else (doi.group(1).rstrip('.') if doi else None),
                        title=delatex(title.group(1)) if title else '', raw=delatex(block)[:300]))
    return out


def check(e):
    if e['key'].startswith('silvafilho'):
        e['status'] = 'self-citation'
        return e
    if e['doi']:
        d = e['doi']
        if d.lower().startswith(('10.48550', '10.5281')):
            j = get_json('https://api.datacite.org/dois/' + urllib.parse.quote(d))
            t = (j.get('data', {}).get('attributes', {}).get('titles') or [{}])[0].get('title', '') if '_error' not in j else ''
        else:
            j = get_json('https://api.crossref.org/works/' + urllib.parse.quote(d))
            t = (j.get('message', {}).get('title') or [''])[0] if '_error' not in j else ''
        e['resolved_title'] = t
        if not t:
            e['status'] = 'DOI-UNRESOLVED'
        else:
            r = sim(e['title'], t) if e['title'] else 0
            e['score'] = round(r, 2)
            e['status'] = 'ok' if r >= 0.8 else ('check' if r >= 0.5 else 'DOI-TITLE-MISMATCH')
    else:
        q = urllib.parse.quote(e['raw'][:250])
        j = get_json(f'https://api.crossref.org/works?query.bibliographic={q}&rows=1')
        items = j.get('message', {}).get('items', []) if '_error' not in j else []
        if items:
            it = items[0]
            t = (it.get('title') or [''])[0]
            e['resolved_title'] = t
            e['suggested_doi'] = it.get('DOI')
            r = sim(e['title'], t) if e['title'] else 0
            e['score'] = round(r, 2)
            e['status'] = 'no-doi:match' if r >= 0.8 else 'no-doi:unverified'
        else:
            e['status'] = 'no-doi:unverified'
    return e


def main():
    entries = []
    for f in sorted(glob.glob('chap*.tex')):
        entries += parse(f)
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        entries = list(ex.map(check, entries))
    json.dump(entries, open('audit/references.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    from collections import Counter
    cnt = Counter(e['status'] for e in entries)
    lines = ['# Reference audit', '', f'Total entries: {len(entries)}', '', '| status | n |', '|---|---|']
    lines += [f'| {k} | {v} |' for k, v in sorted(cnt.items())]
    lines += ['', '## Entries needing attention', '', '| file | key | status | cited title | registered title | score | DOI / suggestion |', '|---|---|---|---|---|---|---|']
    for e in entries:
        if e['status'] in ('ok', 'self-citation', 'no-doi:match'):
            continue
        lines.append('| {} | {} | {} | {} | {} | {} | {} |'.format(
            e['file'][:6], e['key'], e['status'], e['title'][:70].replace('|', '/'),
            e.get('resolved_title', '')[:70].replace('|', '/'), e.get('score', ''), e.get('doi') or e.get('suggested_doi', '')))
    lines += ['', '## Matched without DOI (DOI could be added)', '']
    for e in entries:
        if e['status'] == 'no-doi:match':
            lines.append(f"- {e['file'][:6]} `{e['key']}` -> {e.get('suggested_doi')}")
    open('audit/references_report.md', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print(dict(cnt))


if __name__ == '__main__':
    main()
