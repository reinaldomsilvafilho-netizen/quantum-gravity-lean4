"""Resolve every DOI printed in the Zenodo Vol II bibliography (and the local-tex variants) via Crossref.
Negative control: a mutated DOI must fail to resolve."""
import json, urllib.request, urllib.error, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
dois = {
 "Bakry-Emery 1985": "10.1007/BFb0075847",
 "Benamou-Brenier 2000 (Zenodo print)": "10.1007/s002110050475",
 "Bengtsson-Zyczkowski 2017": "10.1017/9781139207010",
 "Chazal et al 2016": "10.1007/978-3-319-42545-0",
 "Edelsbrunner-Harer 2010": "10.1090/mbk/069",
 "Hormander 2003": "10.1007/978-3-642-61497-2",
 "Safranek 2017 (Zenodo: 052320)": "10.1103/PhysRevA.95.052320",
 "Safranek 2017 (local tex: 062320)": "10.1103/PhysRevA.95.062320",
 "Verstraete-Cirac 2010": "10.1103/PhysRevLett.104.190405",
 "Villani 2009": "10.1007/978-3-540-71050-9",
 "von Renesse-Sturm 2005": "10.1002/cpa.20060",
 "Willmore 1993": "10.1093/oso/9780198532538.001.0001",
 "Cohen-Steiner-Edelsbrunner-Harer 2007 (not cited; classical stability)": "10.1007/s00454-006-1276-5",
 "NEGATIVE CONTROL mutated": "10.1103/PhysRevA.95.999999",
}
out = []
for k, d in dois.items():
    try:
        with urllib.request.urlopen("https://api.crossref.org/works/" + d, timeout=60) as r:
            m = json.load(r)["message"]
        t = (m.get("title") or [""])[0]
        a = ", ".join((x.get("family", "") for x in m.get("author", [])[:4]))
        ct = (m.get("container-title") or [""])
        y = m.get("issued", {}).get("date-parts", [[None]])[0][0]
        out.append("OK  %-55s %s | %s | %s | %s | %s vol %s pages %s" % (k, d, t[:90], a, y, ct[0] if ct else "", m.get("volume"), m.get("page")))
    except urllib.error.HTTPError as e:
        out.append("FAIL %-55s %s HTTP %s" % (k, d, e.code))
    except Exception as e:
        out.append("ERR %-55s %s %r" % (k, d, e))
txt = "\n".join(out); print(txt.encode("ascii", "replace").decode())
open(os.path.join(HERE, "crossref_check.out.txt"), "w", encoding="utf8").write(txt)
