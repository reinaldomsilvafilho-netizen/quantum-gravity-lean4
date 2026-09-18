import urllib.request, json
import textwrap

dois = [
    '10.5281/zenodo.22290043', 
    '10.5281/zenodo.22699282', 
    '10.5281/zenodo.22699843', 
    '10.5281/zenodo.22707110', 
    '10.5281/zenodo.22707125', 
    '10.5281/zenodo.22441676'
]

results = []

for doi in dois:
    record_id = doi.split('.')[-1]
    url = f'https://zenodo.org/api/records/{record_id}'
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            title = data['metadata'].get('title', 'N/A')
            desc = data['metadata'].get('description', 'N/A')
            results.append(f"DOI: {doi}\nTitle: {title}\nDescription: {textwrap.shorten(desc, width=200)}\n")
    except Exception as e:
        results.append(f"DOI: {doi} - Error: {e}\n")

with open('zenodo_records.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(results))
