"""Corrector's DOI check for the corrected Vol. II bibliography.
Crossref for publisher DOIs, DataCite for Zenodo DOIs. Prints title, authors, year, container.
Negative control: a mutated DOI must fail."""
import json, os, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__))
crossref = {
    "Bakry-Emery 1985": "10.1007/BFb0075847",
    "Benamou-Brenier 2000 (corrected)": "10.1007/s002110050002",
    "Bengtsson-Zyczkowski 2017": "10.1017/9781139207010",
    "Chazal et al 2016": "10.1007/978-3-319-42545-0",
    "Edelsbrunner-Harer 2010": "10.1090/mbk/069",
    "Hormander 2003": "10.1007/978-3-642-61497-2",
    "Safranek 2017": "10.1103/PhysRevA.95.052320",
    "Verstraete-Cirac 2010": "10.1103/PhysRevLett.104.190405",
    "Villani 2009": "10.1007/978-3-540-71050-9",
    "von Renesse-Sturm 2005": "10.1002/cpa.20060",
    "Cohen-Steiner-Edelsbrunner-Harer 2007": "10.1007/s00454-006-1276-5",
    "Cheeger 1970": "10.1515/9781400869312-013",
    "White 1973": "10.1090/S0002-9939-1973-0324603-1",
    "Caffarelli 2000": "10.1007/s002200000257",
    "Memoli 2011": "10.1007/s10208-011-9093-5",
    "Lovasz 2012": "10.1090/coll/060",
    "Evans-Gariepy 2015": "10.1201/b18333",
    "McCann 1997": "10.1006/aima.1997.1634",
    "Otto-Villani 2000": "10.1006/jfan.1999.3557",
    "Ambrosio-Gigli-Savare 2008": "10.1007/978-3-7643-8722-8",
    "Connes 1988": "10.1007/BF01218391",
    "Bakry-Gentil-Ledoux 2014": "10.1007/978-3-319-00227-9",
    "Crawley-Boevey 2015": "10.1142/S0219498815500668",
    "Chen-Vidal 2014": "10.1088/1742-5468/2014/10/P10011",
    "NEGATIVE CONTROL mutated": "10.1007/s002110059999",
}
datacite = {
    "Vol I DOI printed in v2": "10.5281/zenodo.22441676",
    "Beyond the Spectrum concept": "10.5281/zenodo.22644743",
    "Book concept": "10.5281/zenodo.22290043",
    "NEGATIVE CONTROL mutated": "10.5281/zenodo.0000001",
}
out = []
def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)
for k, d in crossref.items():
    try:
        m = get("https://api.crossref.org/works/" + d)["message"]
        t = (m.get("title") or [""])[0]
        a = ", ".join(x.get("family", x.get("name", "")) for x in m.get("author", [])[:4])
        if not a:
            a = "eds: " + ", ".join(x.get("family", "") for x in m.get("editor", [])[:3])
        y = m.get("issued", {}).get("date-parts", [[None]])[0][0]
        ct = (m.get("container-title") or [""])[0]
        out.append("OK   %-36s %s | %s | %s | %s | %s vol %s pp %s" % (k, d, t[:100], a, y, ct, m.get("volume"), m.get("page")))
    except urllib.error.HTTPError as e:
        out.append("FAIL %-36s %s HTTP %s" % (k, d, e.code))
    except Exception as e:
        out.append("ERR  %-36s %s %r" % (k, d, e))
for k, d in datacite.items():
    try:
        m = get("https://api.datacite.org/dois/" + d)["data"]["attributes"]
        t = m["titles"][0]["title"]
        a = ", ".join(c.get("name", "") for c in m.get("creators", [])[:3])
        out.append("OK   %-36s %s | %s | %s | %s | version %s" % (k, d, t[:110], a, m.get("publicationYear"), m.get("version")))
    except urllib.error.HTTPError as e:
        out.append("FAIL %-36s %s HTTP %s" % (k, d, e.code))
    except Exception as e:
        out.append("ERR  %-36s %s %r" % (k, d, e))
txt = "\n".join(out)
open(os.path.join(HERE, "doi_check_corrector.out.txt"), "w", encoding="utf8").write(txt)
print(txt.encode("ascii", "replace").decode())
