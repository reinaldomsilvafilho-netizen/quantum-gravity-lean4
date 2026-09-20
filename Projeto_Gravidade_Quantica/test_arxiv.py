import urllib.request, urllib.parse
query_str = 'Cosmic Explorer The US contribution to'
query = urllib.parse.quote(f'ti:"{query_str}"', safe=':')
url = f'http://export.arxiv.org/api/query?search_query={query}&max_results=1'
print('URL:', url)
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Antigravity/1.0'})
    resp = urllib.request.urlopen(req)
    print(resp.status)
except Exception as e:
    print('Error:', e)
