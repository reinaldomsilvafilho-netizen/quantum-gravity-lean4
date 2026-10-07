"""Step 0: Zenodo version check for Beyond the Spectrum (concept 22644743)."""
import json, hashlib, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'beyond_the_spectrum_files'))


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


rec = get('https://zenodo.org/api/records/22866175')
m = rec['metadata']
print('record', rec['id'], m.get('publication_date'), 'version=', m.get('version'))
print('title:', m['title'])
for f in rec['files']:
    print('  file', f['key'], f['size'], f['checksum'])
alls = get('https://zenodo.org/api/records?q=conceptrecid:22644743&all_versions=true&size=25')
print('all versions:', alls['hits']['total'])
for h in sorted(alls['hits']['hits'], key=lambda h: h['id']):
    hm = h['metadata']
    print(h['id'], hm.get('publication_date'), hm.get('version'), [(f['key'], f['size'], f['checksum']) for f in h['files']])
print('local md5:')
for fn in sorted(os.listdir(FILES)):
    if fn.endswith('.pdf'):
        p = os.path.join(FILES, fn)
        print('  ', fn, os.path.getsize(p), 'md5:' + hashlib.md5(open(p, 'rb').read()).hexdigest())
