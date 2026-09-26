import json, sys, urllib.request, urllib.parse
DOIS = sys.argv[1:] or [
 "10.1016/j.laa.2011.05.040", "10.1007/s00039-007-0599-6", "10.1007/BF01236935",
 "10.1080/00268976400100041", "10.1137/090752286", "10.1007/BF02097233",
 "10.1017/S0308210512001783", "10.1007/978-3-642-12245-3", "10.1137/1.9781611972030",
]
for d in DOIS:
    try:
        r = urllib.request.urlopen("https://api.crossref.org/works/" + urllib.parse.quote(d), timeout=30)
        m = json.load(r)["message"]
        au = "; ".join((a.get("family","")) for a in m.get("author", [])[:4])
        print("OK ", d, "|", au, "|", (m.get("title") or [""])[0][:90], "|", (m.get("container-title") or [""])[0][:50], "|", m.get("volume"), m.get("page"), m.get("issued",{}).get("date-parts"))
    except Exception as e:
        print("ERR", d, e)
