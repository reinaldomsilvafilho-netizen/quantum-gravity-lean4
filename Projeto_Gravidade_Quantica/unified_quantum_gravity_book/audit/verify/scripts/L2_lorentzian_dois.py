"""Resolve the 11 new ch12 DOIs via Crossref; print title/authors/venue/vol/page. NC: a mutated DOI must 404."""
import json, urllib.request, urllib.error
DOIS = {"Lehmann1954": "10.1007/BF02783624", "OS1973": "10.1007/BF01645738",
        "BBMM2016": "10.1103/PhysRevD.93.044017", "Anselmi2018": "10.1007/JHEP02(2018)141",
        "AnselmiPiva2018": "10.1007/JHEP11(2018)021", "Anselmi2021": "10.1007/JHEP11(2021)030",
        "ABP2020": "10.1007/JHEP07(2020)211", "Stelle1977": "10.1103/PhysRevD.16.953",
        "Stelle1978": "10.1007/BF00760427", "LeeWick1970": "10.1103/PhysRevD.2.1033",
        "GOW2008": "10.1103/PhysRevD.77.025012", "NEG_mutated": "10.1103/PhysRevD.93.0440179"}
ok = 0
for k, d in DOIS.items():
    try:
        r = urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/" + urllib.request.quote(d),
                                   headers={"User-Agent": "L2-audit (mailto:none@example.org)"}), timeout=30)
        m = json.load(r)["message"]
        au = "; ".join(a.get("family", "") for a in m.get("author", []))
        print(f"{k}: OK | {m['title'][0]} | {au} | {m.get('container-title',[''])[0]} {m.get('volume','')} {m.get('issue','')} {m.get('page', m.get('article-number',''))} | {m.get('issued',{}).get('date-parts')}")
        ok += k != "NEG_mutated"
    except urllib.error.HTTPError as e:
        print(f"{k}: HTTP {e.code}" + ("  (NC PASS)" if k == "NEG_mutated" else "  FAIL"))
print(f"{ok}/11 resolved")
