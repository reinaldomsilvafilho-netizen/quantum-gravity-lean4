import json, sys, urllib.request, urllib.parse
for q in sys.argv[1:]:
    url = "https://api.crossref.org/works?rows=5&query.bibliographic=" + urllib.parse.quote(q)
    m = json.load(urllib.request.urlopen(url, timeout=30))["message"]["items"]
    print("==", q)
    for it in m:
        au = "; ".join(a.get("family","") for a in it.get("author", [])[:3])
        print("  ", it["DOI"], "|", au, "|", (it.get("title") or [""])[0][:80], "|", (it.get("container-title") or [""])[0][:40], "|", it.get("issued",{}).get("date-parts"))
