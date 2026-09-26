"""Re-resolve DOI-UNRESOLVED entries of audit/references.json sequentially (rate-limit safe)."""
import json
import time
import urllib.parse
import urllib.request

import check_references as cr

entries = json.load(open('audit/references.json', encoding='utf-8'))
for e in entries:
    if e['status'] != 'DOI-UNRESOLVED':
        continue
    for attempt in range(3):
        time.sleep(1.5)
        d = e['doi']
        j = cr.get_json('https://doi.org/api/handles/' + urllib.parse.quote(d))   # handle exists?
        exists = j.get('responseCode') == 1
        cj = cr.get_json('https://api.crossref.org/works/' + urllib.parse.quote(d))
        t = (cj.get('message', {}).get('title') or [''])[0] if '_error' not in cj else ''
        if t or exists:
            break
    e['handle_exists'] = exists
    e['resolved_title'] = t
    if t:
        r = cr.sim(e['title'], t)
        e['score'] = round(r, 2)
        e['status'] = 'ok' if r >= 0.8 else ('check' if r >= 0.5 else 'DOI-TITLE-MISMATCH')
    elif exists:
        e['status'] = 'doi-exists-no-crossref-title'
    print(f"{e['file'][:6]} {e['key']:28s} {e['status']:30s} {e.get('score','')} {t[:70]}")
json.dump(entries, open('audit/references.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
